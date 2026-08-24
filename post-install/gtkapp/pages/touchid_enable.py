"""Touch ID, page 1: shown only if a fingerprint sensor is actually
detected (touchid_backend.has_device(), same lsusb check as the C++
TouchIDManager) - skipped straight to finish otherwise. If a fingerprint is
already enrolled for the live user (touchid_backend.list_fingerprints()),
there's nothing to set up either - Touch ID is marked enabled (so post_setup
still migrates the existing print to the real account) and we skip straight
to finish too. 'Continue' goes to the enrollment page; 'Set Up Later' skips
straight to finish too."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import touchid_backend as backend
from ..widgets import page_root, make_title, make_description


class TouchIDEnablePage:
    def __init__(self, app):
        self.app = app
        self._skip_next_show = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Touch ID")
        content.append(self.title)
        self.description = make_description(
            "Touch ID lets you unlock your computer and authenticate with "
            "just your fingerprint, instead of typing your password."
        )
        content.append(self.description)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

        self.later_btn = Gtk.Button(label="Set Up Later in Settings")
        self.later_btn.add_css_class("nav-button")
        self.later_btn.set_halign(Gtk.Align.START)
        self.later_btn.set_valign(Gtk.Align.END)
        self.later_btn.set_margin_start(20)
        self.later_btn.set_margin_bottom(20)
        self.later_btn.connect("clicked", self._on_later_clicked)
        self.card.overlay.add_overlay(self.later_btn)

    def on_show(self):
        if self._skip_next_show:
            self._skip_next_show = False
            return
        if not backend.has_device():
            self.app.state.save_touchid(False)
            self.app.go_to("finish")
            return
        if backend.list_fingerprints():
            self.app.state.save_touchid(True)
            self.app.go_to("finish")

    def _on_back(self):
        self.app.go_to("piri")

    def _on_later_clicked(self, _btn):
        self.app.state.save_touchid(False)
        self.app.go_to("finish")

    def _on_continue(self):
        self.app.go_to("touchid_setup")
