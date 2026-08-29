"""Migration Assistant - matches macOS's real "Transfer Your Data to This
Mac" screen: left-aligned icon+title+paragraph, then a labeled list of
radio options below - not a centered icon-grid picker. Visual only for now
(per explicit instruction): selectable source, no actual transfer
implemented yet.

Only 3 options instead of the reference's 4: pearOS has no phone/tablet
device ecosystem for a "Set up with iPhone or iPad"-equivalent option to
mean anything, so it's dropped rather than inventing a fictional pearOS
device to fill the slot - the other three all map to something real."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root
from .migration_icon import TransferIcon

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (left column started at x=159 in a 723-wide card) and scaled to this
# app's 800-wide card (factor 799/723 ~= 1.105).
_LEFT_MARGIN = 176

OPTIONS = [
    ("pearos", "From a pearOS Computer, Time Machine, or startup disk"),
    ("windows", "From a Windows PC"),
    ("new", "Set Up as New"),
]


class MigrationAssistantPage:
    def __init__(self, app):
        self.app = app
        self._selected = OPTIONS[0][0]

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = TransferIcon(size=92)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Transfer Your Data to This pearOS Computer")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "You can transfer your data from another pearOS computer or "
                "a Windows PC. If you don't want to transfer from a "
                "computer, you can use a backup or startup disk, or set up "
                "this pearOS Computer without transferring any data."
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

        self.question = Gtk.Label(label="How do you want to transfer your information?")
        self.question.add_css_class("migration-question")
        self.question.set_halign(Gtk.Align.START)
        self.question.set_margin_start(_LEFT_MARGIN)
        self.question.set_margin_top(72)
        content.append(self.question)

        radios = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        radios.set_halign(Gtk.Align.START)
        radios.set_margin_start(_LEFT_MARGIN)
        radios.set_margin_top(10)
        content.append(radios)

        first_button = None
        self._buttons = {}
        for key, label_text in OPTIONS:
            btn = Gtk.CheckButton(label=label_text)
            btn.add_css_class("migration-radio")
            if first_button is None:
                first_button = btn
            else:
                btn.set_group(first_button)
            btn.connect("toggled", self._on_toggled, key)
            radios.append(btn)
            self._buttons[key] = btn
        first_button.set_active(True)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_toggled(self, btn, key):
        if btn.get_active():
            self._selected = key

    def _on_back(self):
        self.app.state.wifi_entry_forward = False
        self.app.go_to("wifi")

    def _on_continue(self):
        self.app.go_to("written_spoken")
