"""Piri: persists the real show_icon flag (piri_backend.py) - the actual
speech-model download happens on first real login, not during the wizard
(see piri_backend.py's docstring for why)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import piri_backend as backend
from ..widgets import page_root, make_title

NOTE_TEXT = (
    "Piri is pearOS's built-in assistant. Its language model will "
    "download automatically the first time you sign in.\n\n"
    "You can change this later in System Settings."
)


class PiriPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Piri")
        content.append(self.title)

        self.toggle = Gtk.CheckButton(label="Enable Piri")
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
        self.app.go_to("screen_time")

    def _on_continue(self):
        backend.set_enabled(self.toggle.get_active())
        self.app.go_to("look")
