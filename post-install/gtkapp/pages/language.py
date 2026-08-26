"""Port of app/index.html + engine.js's list_languages()/select_language()."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import i18n as i18n_mod
from ..widgets import page_root, make_title
from .common import SelectList, make_worldmap


class LanguagePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)
        content.append(make_worldmap())
        content.append(make_title("Select Your Language"))

        languages = i18n_mod.list_languages()
        items = [(lang["code"] + ".UTF-8", lang["displayName"]) for lang in languages]
        self.select_list = SelectList(items)
        content.append(self.select_list.widget)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("written_spoken")

    def _on_continue(self):
        locale = self.select_list.selected_value()
        if not locale:
            self.app.show_alert("You must select one language from the list")
            return
        self.app.state.select_language(locale)
        self.app.set_locale(self.app.state.lng)
        self.app.go_to("keymap")
