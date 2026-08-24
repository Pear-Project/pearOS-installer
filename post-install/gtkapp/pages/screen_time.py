"""Screen Time: only persists the on/off choice.

This page runs as the live 'default' user, before the real account exists,
so actually installing/starting the collector here would write into
'default's home and start a systemd --user unit that dies with 'default' on
next boot - all for nothing. post_setup drops the collector/KWin-script/
systemd-unit files (see first_login_assets/) into the real user's home, and
schedules activation (which needs a live X11/D-Bus session) for that user's
first login, same mechanism it already uses for the theme switch."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title

NOTE_TEXT = (
    "Screen Time shows how much time you spend in each app, so you can "
    "see your usage patterns and set limits if you want to.\n\n"
    "You can change this later in System Settings."
)


class ScreenTimePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Screen Time")
        content.append(self.title)

        self.toggle = Gtk.CheckButton(label="Enable Screen Time")
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
        self.app.go_to("analytics")

    def _on_continue(self):
        self.app.state.save_screentime(self.toggle.get_active())
        self.app.go_to("piri")
