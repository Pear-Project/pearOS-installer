#!/usr/bin/env python3
import dbus, dbus.service, subprocess, json, os, time
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DATA_FILE = os.path.expanduser("~/.local/share/pearos-settings/screentime.json")
FLUSH_INTERVAL = 15

def load():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except Exception:
        return {}

def save(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, DATA_FILE)

def is_locked():
    try:
        out = subprocess.run(
            ["qdbus6", "org.freedesktop.ScreenSaver", "/ScreenSaver",
             "org.freedesktop.ScreenSaver.GetActive"],
            capture_output=True, text=True, timeout=2)
        return out.stdout.strip() == "true"
    except Exception:
        return False

class Collector(dbus.service.Object):
    def __init__(self, bus):
        dbus.service.Object.__init__(self, bus, "/Collector")
        self.current = ""
        self.last_ts = time.time()

    def _flush(self, now):
        if self.current and not is_locked():
            elapsed = int(now - self.last_ts)
            if elapsed > 0:
                data = load()
                today = time.strftime("%Y-%m-%d")
                day = data.setdefault(today, {})
                day[self.current] = day.get(self.current, 0) + elapsed
                save(data)
        self.last_ts = now

    @dbus.service.method("org.pearos.ScreenTime.Collector", in_signature="s")
    def reportActiveWindow(self, class_name):
        now = time.time()
        self._flush(now)
        self.current = str(class_name) if class_name else ""

    def periodic_flush(self):
        self._flush(time.time())
        return True

def main():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    bus_name = dbus.service.BusName("org.pearos.ScreenTime", bus)  # noqa: F841
    collector = Collector(bus)
    GLib.timeout_add_seconds(FLUSH_INTERVAL, collector.periodic_flush)
    GLib.MainLoop().run()

if __name__ == "__main__":
    main()
