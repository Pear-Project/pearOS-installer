"""'Written and Spoken Languages' - matches macOS's real layout: left-
aligned icon+title+paragraph, then a list of icon+label+value rows
(Preferred Languages / Input Sources / Dictation), measured off a real
screenshot of this exact page. A bottom-left 'Customize Settings' button
jumps to the keyboard-layout picker (pages/keymap.py) for the one piece
that's actually user-adjustable right now."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import i18n as i18n_mod
from ..widgets import page_root
from .globe_grid_icon import GlobeGridIcon
from .keymap import LAYOUTS

_LAYOUT_NAMES = dict(LAYOUTS)

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (left column started at x=159 in a 723-wide card) and scaled to this
# app's 800-wide card (factor 799/723 ~= 1.105) - same value as
# migration_assistant.py's left column, both being this "detail page"
# layout rather than the centered list-picker one.
_LEFT_MARGIN = 176


def _language_display_name(lng_code):
    for lang in i18n_mod.list_languages():
        if lang["code"] == lng_code:
            return lang["displayName"]
    return lng_code


class _SummaryRow:
    """One icon + bold label + gray value row, matching the reference's
    Preferred Languages / Input Sources / Dictation rows."""

    def __init__(self, icon_widget, label_text):
        self.widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        icon_widget.set_valign(Gtk.Align.CENTER)
        self.widget.append(icon_widget)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        text_box.set_valign(Gtk.Align.CENTER)
        self.label = Gtk.Label(label=label_text)
        self.label.add_css_class("summary-row-label")
        self.label.set_halign(Gtk.Align.START)
        text_box.append(self.label)
        self.value = Gtk.Label(label="")
        self.value.add_css_class("summary-row-value")
        self.value.set_halign(Gtk.Align.START)
        text_box.append(self.value)
        self.widget.append(text_box)

    def set_value(self, text):
        self.value.set_label(text)


class WrittenSpokenPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = GlobeGridIcon(size=76)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Written and Spoken Languages")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "The following languages are commonly used in your region. "
                "You can set up this pearOS Computer to use these settings, "
                "or customize them individually."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(8)
        self.description.set_max_width_chars(48)
        content.append(self.description)

        rows_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        rows_box.set_halign(Gtk.Align.START)
        rows_box.set_margin_start(_LEFT_MARGIN)
        rows_box.set_margin_top(26)
        content.append(rows_box)

        self.preferred_row = _SummaryRow(GlobeGridIcon(size=26), "Preferred Languages")
        self.input_row = _SummaryRow(
            Gtk.Image.new_from_icon_name("input-keyboard-symbolic"), "Input Sources"
        )
        self.input_row.widget.get_first_child().set_pixel_size(24)
        self.input_row.widget.get_first_child().add_css_class("summary-row-icon")
        self.dictation_row = _SummaryRow(
            Gtk.Image.new_from_icon_name("audio-input-microphone-symbolic"), "Dictation"
        )
        self.dictation_row.widget.get_first_child().set_pixel_size(24)
        self.dictation_row.widget.get_first_child().add_css_class("summary-row-icon")
        for row in (self.preferred_row, self.input_row, self.dictation_row):
            rows_box.append(row.widget)

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
        self.preferred_row.set_value(display_lang)

        layout = self.app.state.keymap
        layout_name = _LAYOUT_NAMES.get(layout, layout) if layout else "US"
        self.input_row.set_value(layout_name)

        self.dictation_row.set_value(display_lang)

    def _on_back(self):
        self.app.go_to("migration_assistant")

    def _on_continue(self):
        self.app.go_to("accessibility")
