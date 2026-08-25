/* === This file is part of Calamares - <https://calamares.io> ===
 *
 *   pearOS addition - see RemoteControl.h for what this is and why.
 *
 *   Wire protocol: newline-delimited JSON objects, both directions.
 *
 *   Client -> Calamares commands:
 *     {"cmd":"next"}       - same as clicking the Next button
 *     {"cmd":"back"}       - same as clicking the Back button
 *     {"cmd":"minimize"}   - minimize the main window
 *     {"cmd":"restore"}    - un-minimize, raise, and focus the main window
 *     {"cmd":"ping"}       - replied to with {"event":"pong"}
 *
 *   Calamares -> client events (broadcast to every connected client):
 *     {"event":"progress","percent":0.42,"label":"Formatting partition..."}
 *     {"event":"finished"}
 *     {"event":"failed","message":"...","details":"..."}
 *     {"event":"next_enabled","value":true}
 *     {"event":"pong"}
 */
#include "RemoteControl.h"

#include "JobQueue.h"
#include "ViewManager.h"
#include "utils/Logger.h"

#include <QJsonDocument>
#include <QLocalSocket>
#include <QWidget>

static const char* CONTROL_SOCKET_PATH = "/tmp/pearos-calamares-control.sock";

RemoteControl::RemoteControl( QWidget* mainWindow, QObject* parent )
    : QObject( parent )
    , m_mainWindow( mainWindow )
{
    // A stale socket file from a Calamares instance that didn't exit
    // cleanly would otherwise make listen() fail forever after.
    QLocalServer::removeServer( QString::fromLatin1( CONTROL_SOCKET_PATH ) );

    connect( &m_server, &QLocalServer::newConnection, this, &RemoteControl::onNewConnection );

    if ( !m_server.listen( QString::fromLatin1( CONTROL_SOCKET_PATH ) ) )
    {
        cWarning() << "RemoteControl: could not listen on" << CONTROL_SOCKET_PATH << "-"
                   << m_server.errorString() << "- remote control unavailable, Calamares otherwise unaffected.";
        return;
    }

    cDebug() << "RemoteControl: listening on" << CONTROL_SOCKET_PATH;

    if ( Calamares::ViewManager::instance() )
    {
        connect( Calamares::ViewManager::instance(),
                 &Calamares::ViewManager::nextEnabledChanged,
                 this,
                 &RemoteControl::onNextEnabledChanged );
    }
    ensureJobQueueConnected();
}

void
RemoteControl::ensureJobQueueConnected()
{
    // JobQueue::instance() only becomes non-null once initJobQueue() has
    // run; RemoteControl is constructed after that in initView(), but this
    // guard keeps things safe if that ordering ever changes.
    if ( m_jobQueueConnected || !Calamares::JobQueue::instance() )
    {
        return;
    }
    connect( Calamares::JobQueue::instance(), &Calamares::JobQueue::progress, this, &RemoteControl::onJobProgress );
    connect( Calamares::JobQueue::instance(), &Calamares::JobQueue::finished, this, &RemoteControl::onJobFinished );
    connect( Calamares::JobQueue::instance(), &Calamares::JobQueue::failed, this, &RemoteControl::onJobFailed );
    m_jobQueueConnected = true;
}

void
RemoteControl::onNewConnection()
{
    while ( m_server.hasPendingConnections() )
    {
        QLocalSocket* client = m_server.nextPendingConnection();
        connect( client, &QLocalSocket::readyRead, this, &RemoteControl::onClientReadyRead );
        connect( client, &QLocalSocket::disconnected, this, &RemoteControl::onClientDisconnected );
        m_clients.append( client );
        cDebug() << "RemoteControl: client connected, now" << m_clients.count();
    }
}

void
RemoteControl::onClientReadyRead()
{
    auto* client = qobject_cast< QLocalSocket* >( sender() );
    if ( !client )
    {
        return;
    }
    while ( client->canReadLine() )
    {
        handleLine( client, client->readLine().trimmed() );
    }
}

void
RemoteControl::onClientDisconnected()
{
    auto* client = qobject_cast< QLocalSocket* >( sender() );
    m_clients.removeAll( QPointer< QLocalSocket >( client ) );
    if ( client )
    {
        client->deleteLater();
    }
}

void
RemoteControl::handleLine( QLocalSocket* client, const QByteArray& line )
{
    if ( line.isEmpty() )
    {
        return;
    }
    QJsonParseError parseError;
    QJsonDocument doc = QJsonDocument::fromJson( line, &parseError );
    if ( parseError.error != QJsonParseError::NoError || !doc.isObject() )
    {
        cWarning() << "RemoteControl: ignoring malformed command:" << line;
        return;
    }

    const QString cmd = doc.object().value( QStringLiteral( "cmd" ) ).toString();
    if ( cmd == QLatin1String( "next" ) )
    {
        if ( Calamares::ViewManager::instance() )
        {
            Calamares::ViewManager::instance()->next();
        }
        ensureJobQueueConnected();  // exec phase may only just now have created the JobQueue
    }
    else if ( cmd == QLatin1String( "back" ) )
    {
        if ( Calamares::ViewManager::instance() )
        {
            Calamares::ViewManager::instance()->back();
        }
    }
    else if ( cmd == QLatin1String( "minimize" ) )
    {
        if ( m_mainWindow )
        {
            m_mainWindow->showMinimized();
        }
    }
    else if ( cmd == QLatin1String( "restore" ) )
    {
        if ( m_mainWindow )
        {
            m_mainWindow->showNormal();
            m_mainWindow->raise();
            m_mainWindow->activateWindow();
        }
    }
    else if ( cmd == QLatin1String( "ping" ) )
    {
        QJsonObject pong;
        pong.insert( QStringLiteral( "event" ), QStringLiteral( "pong" ) );
        QByteArray bytes = QJsonDocument( pong ).toJson( QJsonDocument::Compact ) + '\n';
        client->write( bytes );
    }
    else
    {
        cWarning() << "RemoteControl: unknown command:" << cmd;
    }
}

void
RemoteControl::broadcast( const QJsonObject& event )
{
    QByteArray bytes = QJsonDocument( event ).toJson( QJsonDocument::Compact ) + '\n';
    for ( const QPointer< QLocalSocket >& client : std::as_const( m_clients ) )
    {
        if ( client )
        {
            client->write( bytes );
        }
    }
}

void
RemoteControl::onJobProgress( qreal percent, const QString& prettyName )
{
    QJsonObject event;
    event.insert( QStringLiteral( "event" ), QStringLiteral( "progress" ) );
    event.insert( QStringLiteral( "percent" ), percent );
    event.insert( QStringLiteral( "label" ), prettyName );
    broadcast( event );
}

void
RemoteControl::onJobFinished()
{
    QJsonObject event;
    event.insert( QStringLiteral( "event" ), QStringLiteral( "finished" ) );
    broadcast( event );
}

void
RemoteControl::onJobFailed( const QString& message, const QString& details )
{
    QJsonObject event;
    event.insert( QStringLiteral( "event" ), QStringLiteral( "failed" ) );
    event.insert( QStringLiteral( "message" ), message );
    event.insert( QStringLiteral( "details" ), details );
    broadcast( event );
}

void
RemoteControl::onNextEnabledChanged( bool enabled )
{
    QJsonObject event;
    event.insert( QStringLiteral( "event" ), QStringLiteral( "next_enabled" ) );
    event.insert( QStringLiteral( "value" ), enabled );
    broadcast( event );
}
