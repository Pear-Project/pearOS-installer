/* === This file is part of Calamares - <https://calamares.io> ===
 *
 *   pearOS addition: a small local-socket control channel so an external
 *   process (the pearOS Python installer) can drive Calamares while its
 *   window is minimized/hidden - send "next" instead of clicking the
 *   Next button, minimize/restore the window, and receive exec-phase
 *   progress/finished/failed events instead of only updating Calamares'
 *   own (now-hidden) progress page.
 *
 *   Not an upstream Calamares feature - added specifically for pearOS's
 *   "Disk Utility" flow (see pearOS-installer's disk_utility_backend.py
 *   and install_progress.py).
 */

#ifndef CALAMARES_REMOTECONTROL_H
#define CALAMARES_REMOTECONTROL_H

#include <QJsonObject>
#include <QList>
#include <QLocalServer>
#include <QObject>
#include <QPointer>

class QLocalSocket;
class QWidget;

class RemoteControl : public QObject
{
    Q_OBJECT
public:
    /** @brief Starts listening on the fixed control socket path.
     *
     * @p mainWindow is the window minimize/restore commands act on.
     * Failure to start listening (e.g. a stale socket another process
     * still owns) is logged and otherwise harmless - Calamares works
     * exactly as normal without remote control available.
     */
    explicit RemoteControl( QWidget* mainWindow, QObject* parent = nullptr );

private Q_SLOTS:
    void onNewConnection();
    void onClientReadyRead();
    void onClientDisconnected();

    void onJobProgress( qreal percent, const QString& prettyName );
    void onJobFinished();
    void onJobFailed( const QString& message, const QString& details );
    void onNextEnabledChanged( bool enabled );

private:
    void handleLine( QLocalSocket* client, const QByteArray& line );
    void broadcast( const QJsonObject& event );

    QLocalServer m_server;
    QPointer< QWidget > m_mainWindow;
    QList< QPointer< QLocalSocket > > m_clients;
    bool m_jobQueueConnected = false;

    void ensureJobQueueConnected();
};

#endif
