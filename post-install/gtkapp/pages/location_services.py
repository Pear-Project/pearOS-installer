"""Location Services - real toggle: enables/disables the geoclue.service
systemd unit (KDE's own location backend), not just an in-memory flag like
dpkg/system-settings/backend/privacymanager.cpp's setLocationServices()
(which never actually persists anything - this goes one step further)."""
import subprocess

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title

NOTE_TEXT = (
    "Location Services uses GPS, Bluetooth, and crowd-sourced Wi-Fi hotspot "
    "locations to determine your approximate location, used for things "
    "like time zone, weather, and maps.\n\n"
    "You can change this later in System Settings."
)


def _set_geoclue_enabled(enabled):
    action = ["--now", "enable"] if enabled else ["--now", "disable"]
    try:
        subprocess.Popen(["sudo", "systemctl"] + action + ["geoclue.service"])
    except OSError:
        pass


class LocationServicesPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Location Services")
        content.append(self.title)

        self.toggle = Gtk.CheckButton(label="Enable Location Services")
        self.toggle.set_active(True)
        self.toggle.set_halign(Gtk.Align.CENTER)
        self.toggle.set_margin_top(16)
        content.append(self.toggle)

        note = Gtk.Label(label=NOTE_TEXT)
        note.add_css_class("look-note")
        note.set_wrap(True)
        note.set_justify(Gtk.Justification.CENTER)
        note.set_max_width_chars(60)
        note.set_margin_top(10)
        content.append(note)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("agreement")

    def _on_continue(self):
        _set_geoclue_enabled(self.toggle.get_active())
        self.app.go_to("timezone")
