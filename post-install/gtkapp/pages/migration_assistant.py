"""Migration Assistant - visual only for now (per explicit instruction): two
selectable source options, no actual transfer implemented yet."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title, make_description

OPTIONS = [
    ("pearos", "From a pearOS Machine or Backup",
     "Transfer information from another pearOS computer, an external "
     "drive, or a Time Machine-style backup."),
    ("windows", "From a Windows PC",
     "Transfer information from a Windows computer on the same network."),
    ("setup_new", "Set Up as New",
     "Don't transfer any information now - you can do this later from "
     "System Settings."),
]

_ICON_NAMES = {
    "pearos": "drive-harddisk-symbolic",
    "windows": "computer-symbolic",
    "setup_new": "document-new-symbolic",
}


class MigrationAssistantPage:
    def __init__(self, app):
        self.app = app
        self._selected = None

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Migration Assistant")
        content.append(self.title)
        self.description = make_description(
            "If you have another computer, you can transfer your information to this one."
        )
        content.append(self.description)

        picker = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        picker.set_halign(Gtk.Align.CENTER)
        picker.set_margin_top(20)
        content.append(picker)

        self._option_boxes = {}
        for key, label_text, desc_text in OPTIONS:
            option = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            option.add_css_class("look-option")
            option.set_size_request(200, 160)

            icon = Gtk.Image.new_from_icon_name(_ICON_NAMES[key])
            icon.set_pixel_size(48)
            icon.set_margin_top(10)
            option.append(icon)

            label = Gtk.Label(label=label_text)
            label.add_css_class("look-option-label")
            label.set_wrap(True)
            label.set_justify(Gtk.Justification.CENTER)
            label.set_max_width_chars(20)
            option.append(label)

            desc = Gtk.Label(label=desc_text)
            desc.add_css_class("description")
            desc.set_wrap(True)
            desc.set_justify(Gtk.Justification.CENTER)
            desc.set_max_width_chars(22)
            option.append(desc)

            click = Gtk.GestureClick()
            click.connect("released", self._on_option_clicked, key)
            option.add_controller(click)

            picker.append(option)
            self._option_boxes[key] = option

        note = Gtk.Label(
            label="You can also transfer your information later from System Settings."
        )
        note.add_css_class("look-note")
        note.set_wrap(True)
        note.set_justify(Gtk.Justification.CENTER)
        note.set_margin_top(16)
        content.append(note)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_option_clicked(self, _gesture, _n_press, _x, _y, key):
        for k, box in self._option_boxes.items():
            if k == key:
                box.add_css_class("selected")
            else:
                box.remove_css_class("selected")
        self._selected = key

    def _on_back(self):
        self.app.state.wifi_entry_forward = False
        self.app.go_to("wifi")

    def _on_continue(self):
        self.app.go_to("written_spoken")
