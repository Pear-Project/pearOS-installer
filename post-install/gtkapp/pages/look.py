"""Port of templates/look.html + initLookPicker()/saveLook()."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title


def _make_preview(mode):
    box = Gtk.Box()
    box.add_css_class("look-preview")
    box.add_css_class("look-preview-%s" % mode)
    box.set_size_request(160, 100)
    return box


class LookPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        self.title = make_title("Choose Your Look")
        content.append(self.title)

        picker = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        picker.set_halign(Gtk.Align.CENTER)
        picker.set_margin_top(10)

        self.options = {}
        for mode, label_text in (("light", "Light"), ("dark", "Dark")):
            option = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            option.add_css_class("look-option")
            option.append(_make_preview(mode))
            label = Gtk.Label(label=label_text)
            label.add_css_class("look-option-label")
            option.append(label)

            click = Gtk.GestureClick()
            click.connect("released", self._on_option_clicked, mode)
            option.add_controller(click)

            picker.append(option)
            self.options[mode] = option

        content.append(picker)

        self.note = Gtk.Label(
            label=(
                "Select a light or dark appearance and see how the Dock, menus, "
                "buttons, and windows adjust depending on which one you choose.\n\n"
                "You can change this later in System Settings."
            )
        )
        self.note.add_css_class("look-note")
        self.note.set_wrap(True)
        self.note.set_justify(Gtk.Justification.CENTER)
        self.note.set_max_width_chars(60)
        self.note.set_margin_top(10)
        content.append(self.note)

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
            self.app.state.save_look(mode)
            self.app.set_dark_mode(mode == "dark")

    def _on_back(self):
        self.app.go_to("piri")

    def _on_continue(self):
        mode = getattr(self, "_selected_mode", "light")
        self.app.state.save_look(mode)
        self.app.go_to("finish")
