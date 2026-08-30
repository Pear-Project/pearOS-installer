"""Port of templates/look.html + initLookPicker()/saveLook() - matches
macOS's real "Choose Your Look" layout: left-aligned title/paragraph,
then Light/Auto/Dark preview tiles (window mockup + dock strip, see
look_preview.py) instead of the old flat-color rectangles, same
"detail page" convention as migration_assistant.py/analytics.py.
'Auto' just follows the system's own light/dark switch (detect_default_
look_mode already reads that for the initial preselect), so it maps to
the same save_look("dark")/set_dark_mode() calls as an explicit choice
made at whatever the system currently is - macOS's Auto is dynamic
(follows sunrise/sunset), which this app has no equivalent mechanism
for."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root
from .look_preview import LookPreview

_LEFT_MARGIN = 176


class LookPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        self.title = Gtk.Label(label="Choose Your Look")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(73)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Select an appearance and see how the Dock, menus, buttons, "
                "and windows adjust depending on which one you choose."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(8)
        self.description.set_max_width_chars(64)
        content.append(self.description)

        self.note = Gtk.Label(label="You can change this later in System Settings.")
        self.note.add_css_class("description")
        self.note.set_halign(Gtk.Align.START)
        self.note.set_margin_start(_LEFT_MARGIN)
        self.note.set_margin_top(16)
        content.append(self.note)

        picker = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        picker.set_halign(Gtk.Align.CENTER)
        picker.set_margin_top(28)
        content.append(picker)

        self.options = {}
        for mode, label_text in (("light", "Light"), ("auto", "Auto"), ("dark", "Dark")):
            option = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            option.add_css_class("look-option")
            option.append(LookPreview(mode))
            label = Gtk.Label(label=label_text)
            label.add_css_class("look-option-label")
            option.append(label)

            click = Gtk.GestureClick()
            click.connect("released", self._on_option_clicked, mode)
            option.add_controller(click)

            picker.append(option)
            self.options[mode] = option

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        self.title.set_label(self.app.t("look.title", "Choose Your Look"))
        self.card.forward_button.set_label(self.app.t("look.continue", "Continue"))
        preselect = self.app.state.detect_default_look_mode()
        self._select(preselect, persist=False)

    def _on_option_clicked(self, _gesture, _n_press, _x, _y, mode):
        self._select(mode, persist=True)

    def _select(self, mode, persist):
        for m, option in self.options.items():
            if m == mode:
                option.add_css_class("selected")
            else:
                option.remove_css_class("selected")
        self._selected_mode = mode
        if persist:
            dark = mode == "dark"
            self.app.state.save_look("dark" if dark else "light")
            self.app.set_dark_mode(dark)

    def _on_back(self):
        self.app.go_to("piri")

    def _on_continue(self):
        mode = getattr(self, "_selected_mode", "light")
        self.app.state.save_look("dark" if mode == "dark" else "light")
        self.app.go_to("update")
