"""Port of index.html: language select. No navbar (index.html never loads
navbar.js), no back button (single forward arrow only)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import make_card, centered_overlay, ArrowButton, load_scaled_picture

LANGUAGES = ["English", "Romanian", "Czech"]
_LOCALE_BY_LABEL = {"English": "en", "Romanian": "ro", "Czech": "cs"}


class LanguagePage:
    def __init__(self, app):
        self.app = app

        card = make_card(800, 600, "app")

        title = Gtk.Label(label="Language")
        title.add_css_class("title")
        title.set_margin_top(20)
        card.append(title)

        worldmap = load_scaled_picture("languages-icon.png", 70)
        worldmap.set_halign(Gtk.Align.CENTER)
        card.append(worldmap)

        list_scroller = Gtk.ScrolledWindow()
        list_scroller.add_css_class("wizard-list")
        list_scroller.set_min_content_width(230)
        list_scroller.set_max_content_width(230)
        # Sized to fit exactly the 3 rows this list actually has - a fixed
        # 200px (the original Electron CSS's own number, presumably tuned
        # for a longer real language list) left a large dead black area
        # below "Czech" with nothing in it.
        list_scroller.set_min_content_height(132)
        list_scroller.set_max_content_height(132)
        list_scroller.set_propagate_natural_height(True)
        list_scroller.set_halign(Gtk.Align.CENTER)
        list_scroller.set_margin_top(8)

        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        for lang in LANGUAGES:
            row_label = Gtk.Label(label=lang)
            row_label.set_halign(Gtk.Align.CENTER)
            self.list_box.append(row_label)
        self.list_box.select_row(self.list_box.get_row_at_index(0))
        list_scroller.set_child(self.list_box)
        card.append(list_scroller)

        # The arrow button lives inside the card itself (pushed to the
        # bottom by a vexpand spacer), not floated over the whole window -
        # anchoring it to the window's own corner instead of the card
        # left it visibly stranded once the card stopped filling the
        # window height.
        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        card.append(spacer)

        footer = Gtk.Box()
        footer.set_halign(Gtk.Align.END)
        footer.set_margin_end(20)
        footer.set_margin_bottom(16)
        forward_btn = ArrowButton(on_click=self._on_continue)
        footer.append(forward_btn)
        card.append(footer)

        overlay = centered_overlay(card)
        self.widget = overlay

    def on_show(self):
        pass

    def _on_continue(self):
        row = self.list_box.get_selected_row()
        label = row.get_child().get_label() if row else "English"
        locale = _LOCALE_BY_LABEL.get(label, "en")
        self.app.go_to("examining", locale=locale)
