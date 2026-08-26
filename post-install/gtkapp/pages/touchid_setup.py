"""Touch ID, page 2: real fingerprint enrollment via fprintd-enroll
(touchid_backend.EnrollSession), streaming live status - not a mockup.

Scanning has to happen live here (that's the whole point of this page), but
the wizard still runs as the 'default' live user - the real account the
wizard is naming on the "Create a Computer Account" page doesn't exist as a
Unix user yet (useradd happens later, in post_setup). So fprintd-enroll
necessarily enrolls the print under 'default'. post_setup, after creating
the real user, copies fprintd's on-disk print data from 'default' to the
new username (same handoff as the profile picture) so it isn't lost when
'default' is deleted on next boot."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from .. import touchid_backend as backend
from ..widgets import page_root, make_title
from .fingerprint_widget import FingerprintWidget


class TouchIDSetupPage:
    def __init__(self, app):
        self.app = app
        self._session = None
        self._enrolled = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Touch ID")
        content.append(self.title)

        self.fingerprint = FingerprintWidget()
        self.fingerprint.set_halign(Gtk.Align.CENTER)
        self.fingerprint.set_margin_top(12)
        content.append(self.fingerprint)

        self.status = Gtk.Label(label="Place your finger on the sensor to begin.")
        self.status.add_css_class("description")
        self.status.set_wrap(True)
        self.status.set_justify(Gtk.Justification.CENTER)
        self.status.set_max_width_chars(50)
        self.status.set_margin_top(10)
        content.append(self.status)

        self.start_btn = Gtk.Button(label="Start Enrollment")
        self.start_btn.add_css_class("nav-button")
        self.start_btn.set_halign(Gtk.Align.CENTER)
        self.start_btn.set_margin_top(16)
        self.start_btn.connect("clicked", self._on_start_clicked)
        content.append(self.start_btn)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )
        self.card.forward_button.set_sensitive(False)

        self.later_btn = Gtk.Button(label="Set Up Later in Settings")
        self.later_btn.add_css_class("nav-button")
        self.later_btn.set_halign(Gtk.Align.START)
        self.later_btn.set_valign(Gtk.Align.END)
        self.later_btn.set_margin_start(20)
        self.later_btn.set_margin_bottom(20)
        self.later_btn.connect("clicked", self._on_later_clicked)
        self.card.overlay.add_overlay(self.later_btn)

    def on_show(self):
        pass

    def _on_start_clicked(self, _btn):
        self.start_btn.set_sensitive(False)
        self.status.set_label("Place your finger on the sensor...")
        self.fingerprint.reset()
        self.fingerprint.start_scanning()
        self._session = backend.EnrollSession(
            "right-index-finger", self._on_status, self._on_done, on_stage=self._on_stage
        )
        self._session.start()

    def _on_status(self, text):
        GLib.idle_add(self.status.set_label, text)

    def _on_stage(self):
        GLib.idle_add(self.fingerprint.advance)

    def _on_done(self, success, error):
        def apply():
            self.start_btn.set_sensitive(True)
            self.fingerprint.set_done(success)
            if success:
                self._enrolled = True
                self.app.state.save_touchid(True)
                self.status.set_label("Done! Your fingerprint has been enrolled.")
                self.start_btn.set_visible(False)
                self.card.forward_button.set_sensitive(True)
            else:
                self.status.set_label(error or "Enrollment failed. Try again.")
            return False

        GLib.idle_add(apply)

    def _on_back(self):
        if self._session:
            self._session.cancel()
        self.app.go_to("touchid_enable")

    def _on_later_clicked(self, _btn):
        if self._session:
            self._session.cancel()
        if not self._enrolled:
            self.app.state.save_touchid(False)
        self.app.go_to("agreement")

    def _on_continue(self):
        self.app.go_to("agreement")
