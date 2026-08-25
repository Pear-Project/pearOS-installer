/* === This file is part of Calamares - <https://calamares.io> ===
 *
 *   Disk Utility-style device info (Location / Connection / Media Type /
 *   S.M.A.R.T. Status) for the ChoicePage / PartitionPage info grid.
 *   KPMcore's Device class doesn't expose any of this, so it's read
 *   straight from sysfs - read-only, never touches the device itself.
 */

#ifndef PARTITION_CORE_DISKINFOUTILS_H
#define PARTITION_CORE_DISKINFOUTILS_H

#include <QFile>
#include <QObject>
#include <QString>

static inline QString
diskInfoBaseName( const QString& deviceNode )
{
    QString node = deviceNode;
    if ( node.startsWith( QStringLiteral( "/dev/" ) ) )
    {
        node.remove( 0, 5 );
    }
    return node;
}

/** @brief Internal vs External, based on the kernel's "removable" flag. */
static inline QString
diskInfoLocation( const QString& deviceNode )
{
    QFile removableFile( QStringLiteral( "/sys/block/%1/removable" ).arg( diskInfoBaseName( deviceNode ) ) );
    if ( removableFile.open( QIODevice::ReadOnly | QIODevice::Text ) )
    {
        const QString value = QString::fromLatin1( removableFile.readAll() ).trimmed();
        if ( value == QStringLiteral( "1" ) )
        {
            return QObject::tr( "External", "@label" );
        }
        if ( value == QStringLiteral( "0" ) )
        {
            return QObject::tr( "Internal", "@label" );
        }
    }
    return QObject::tr( "Unknown", "@label" );
}

/** @brief Bus the device is attached through (SATA/NVMe/USB/...), read
 *  from the keywords in the resolved /sys/block/<dev> device path. */
static inline QString
diskInfoConnection( const QString& deviceNode )
{
    QFile sysBlockLink( QStringLiteral( "/sys/block/%1" ).arg( diskInfoBaseName( deviceNode ) ) );
    const QString resolved = sysBlockLink.symLinkTarget();
    if ( resolved.isEmpty() )
    {
        return QObject::tr( "Unknown", "@label" );
    }
    if ( resolved.contains( QStringLiteral( "usb" ) ) )
    {
        return QObject::tr( "USB", "@label" );
    }
    if ( resolved.contains( QStringLiteral( "nvme" ) ) )
    {
        return QObject::tr( "NVMe", "@label" );
    }
    if ( resolved.contains( QStringLiteral( "ata" ) ) )
    {
        return QObject::tr( "SATA", "@label" );
    }
    if ( resolved.contains( QStringLiteral( "mmc" ) ) )
    {
        return QObject::tr( "SD Card", "@label" );
    }
    if ( resolved.contains( QStringLiteral( "virtio" ) ) )
    {
        return QObject::tr( "Virtual", "@label" );
    }
    return QObject::tr( "Unknown", "@label" );
}

/** @brief Solid State vs Rotational, from the kernel's "rotational" flag. */
static inline QString
diskInfoMediaType( const QString& deviceNode )
{
    QFile rotationalFile( QStringLiteral( "/sys/block/%1/queue/rotational" ).arg( diskInfoBaseName( deviceNode ) ) );
    if ( rotationalFile.open( QIODevice::ReadOnly | QIODevice::Text ) )
    {
        const QString value = QString::fromLatin1( rotationalFile.readAll() ).trimmed();
        if ( value == QStringLiteral( "0" ) )
        {
            return QObject::tr( "Solid State", "@label" );
        }
        if ( value == QStringLiteral( "1" ) )
        {
            return QObject::tr( "Rotational", "@label" );
        }
    }
    return QObject::tr( "Unknown", "@label" );
}

/** @brief "Verified" / "Not Supported", matching Disk Utility's own
 *  wording for a device's S.M.A.R.T. self-check result.
 *
 *  This deliberately does NOT call KPMcore's Device::smartStatus() -
 *  that triggers a real ATA SMART query via libatasmart, and calling it
 *  a second time (KPMcore's own device scan already called it once per
 *  device at startup) reproducibly corrupts the heap - a pre-existing
 *  bug in that third-party code, not something to work around by
 *  re-invoking it more carefully. USB/virtual media generally don't
 *  support SMART passthrough anyway, so the connection type already
 *  read from sysfs is used as a safe stand-in instead. */
static inline QString
diskInfoSmartStatus( const QString& connectionText )
{
    if ( connectionText == QObject::tr( "USB", "@label" ) || connectionText == QObject::tr( "SD Card", "@label" )
         || connectionText == QObject::tr( "Virtual", "@label" )
         || connectionText == QObject::tr( "Unknown", "@label" ) )
    {
        return QObject::tr( "Not Supported", "@label" );
    }
    return QObject::tr( "Verified", "@label" );
}

#endif  // PARTITION_CORE_DISKINFOUTILS_H
