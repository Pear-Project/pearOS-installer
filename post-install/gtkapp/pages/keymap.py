"""Port of templates/keymap.html."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title
from .common import SelectList, make_worldmap

LAYOUTS = [
    ("us", "US"), ("fr", "French"), ("de", "German"), ("el", "Greek"),
    ("hu", "Hungarian"), ("it", "Italian"), ("pl", "Polish"),
    ("ru", "Russian"), ("es", "Spanish"),
]


class KeymapPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)
        content.append(make_worldmap())
        self.title = make_title("Select Your Keyboard Layout")
        content.append(self.title)

        self.select_list = SelectList(LAYOUTS)
        content.append(self.select_list.widget)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        self.title.set_label(self.app.t("keymap.title", "Select Your Keyboard Layout"))
        self.card.forward_button.set_label(self.app.t("keymap.continue", "Continue"))

    def _on_back(self):
        self.app.go_to("written_spoken")

    def _on_continue(self):
        layout = self.select_list.selected_value()
        err = self.app.state.save_keymap(layout)
        if err:
            self.app.show_alert(err)
            return
        self.app.go_to("written_spoken")
