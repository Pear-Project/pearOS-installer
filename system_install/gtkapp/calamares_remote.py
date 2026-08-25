"""Client for Calamares' pearOS-only remote-control socket (see
calamares-src's src/calamares/RemoteControl.{h,cpp} for the C++ side and
the wire protocol). Newline-delimited JSON both ways over a Unix domain
socket at CONTROL_SOCKET_PATH - commands out (next/back/minimize/restore/
ping), events in (progress/finished/failed/next_enabled/pong).

Threading: connect() and the read loop run on a background thread (socket
I/O blocks); every event callback is marshalled onto the GTK main thread
via GLib.idle_add, so callers can safely touch widgets directly from their
callbacks."""
import json
import socket
import threading
import time

from gi.repository import GLib

CONTROL_SOCKET_PATH = "/tmp/pearos-calamares-control.sock"


class CalamaresRemote:
    def __init__(self):
        self._sock = None
        self._thread = None
        self._stop = threading.Event()
        self._lock = threading.Lock()

    def connect(self, timeout=20.0, retry_interval=0.3):
        """Blocking - retries until timeout since Calamares takes a moment
        to start up and begin listening after being launched. Returns True
        if connected, False on timeout. Safe to call from a background
        thread (it's meant to be)."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._stop.is_set():
                return False
            try:
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(CONTROL_SOCKET_PATH)
                with self._lock:
                    self._sock = sock
                return True
            except OSError:
                time.sleep(retry_interval)
        return False

    @property
    def connected(self):
        with self._lock:
            return self._sock is not None

    def send_cmd(self, cmd, **kwargs):
        payload = {"cmd": cmd, **kwargs}
        data = (json.dumps(payload) + "\n").encode()
        with self._lock:
            if self._sock is None:
                return False
            try:
                self._sock.sendall(data)
                return True
            except OSError:
                return False

    def start_listening(self, on_event):
        """on_event(dict) is called on the GTK main thread for every event
        Calamares sends. Starts a background reader thread; safe to call
        once, after connect() succeeded."""
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._reader_loop, args=(on_event,), daemon=True)
        self._thread.start()

    def _reader_loop(self, on_event):
        buf = b""
        while not self._stop.is_set():
            with self._lock:
                sock = self._sock
            if sock is None:
                return
            try:
                data = sock.recv(4096)
            except OSError:
                return
            if not data:
                return
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                except ValueError:
                    continue

                def _dispatch(ev=event):
                    on_event(ev)
                    return GLib.SOURCE_REMOVE

                GLib.idle_add(_dispatch)

    def close(self):
        self._stop.set()
        with self._lock:
            if self._sock is not None:
                try:
                    self._sock.close()
                except OSError:
                    pass
                self._sock = None
