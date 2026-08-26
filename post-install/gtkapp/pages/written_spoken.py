"""'Written and Spoken Languages' - a brief, read-only summary of what was
derived from the Language/Country choices (Preferred Languages, Input
Sources, Dictation), with a bottom-left 'Customize Settings' button that
jumps to the keyboard-layout picker (pages/keymap.py) for the one piece
that's actually user-adjustable right now."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import i18n as i18n_mod
from ..widgets import page_root, make_title
from .keymap import LAYOUTS

_LAYOUT_NAMES = dict(LAYOUTS)


def _language_display_name(lng_code):
    for lang in i18n_mod.list_languages():
        if lang["code"] == lng_code:
            return lang["displayName"]
    return lng_code


def _summary_row(label_text):
    row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
    row.set_halign(Gtk.Align.CENTER)
    label = Gtk.Label(label=label_text)
    label.add_css_class("description")
    label.set_halign(Gtk.Align.START)
    label.set_xalign(0)
    row.append(label)
    return row, label


class WrittenSpokenPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        content.set_hexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        content.set_vexpand(True)
        self.title = make_title("Written and Spoken Languages")
        self.title.set_margin_bottom(10)
        content.append(self.title)

        summary = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        summary.set_halign(Gtk.Align.CENTER)

        row1, self.preferred_label = _summary_row("")
        row2, self.input_label = _summary_row("")
        row3, self.dictation_label = _summary_row("")
        summary.append(row1)
        summary.append(row2)
        summary.append(row3)
        content.append(summary)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

        self.customize_btn = Gtk.Button(label="Customize Settings")
        self.customize_btn.add_css_class("nav-button")
        self.customize_btn.set_halign(Gtk.Align.START)
        self.customize_btn.set_valign(Gtk.Align.END)
        self.customize_btn.set_margin_start(20)
        self.customize_btn.set_margin_bottom(20)
        self.customize_btn.connect("clicked", lambda b: self.app.go_to("language"))
        self.card.overlay.add_overlay(self.customize_btn)

    def on_show(self):
        display_lang = _language_display_name(self.app.state.lng)
        self.preferred_label.set_label("Preferred Languages: " + display_lang)

        layout = self.app.state.keymap
        layout_name = _LAYOUT_NAMES.get(layout, layout) if layout else "US"
        self.input_label.set_label("Input Sources: " + layout_name)

        self.dictation_label.set_label("Dictation: " + display_lang)

    def _on_back(self):
        self.app.go_to("migration_assistant")

    def _on_continue(self):
        self.app.go_to("accessibility")
