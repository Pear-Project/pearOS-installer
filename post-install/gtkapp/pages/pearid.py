"""Sign in with PearID: matches macOS's real "Sign In to Your Apple
Account" layout - icon cluster, left-aligned title/paragraph, a single
email field that reveals the password field on Enter (not both fields
shown at once, and no separate "Sign In" button - submission happens via
Enter/Continue), quick links, and a small two-person "this account will
be linked" note - measured off a real screenshot of this exact page.
Real state check + login against account.pearos.xyz (see
pearid_backend.py); Continue only enables once actually signed in."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from .. import pearid_backend as backend
from ..widgets import page_root
from .pearid_icons import AccountServicesIcon, TwoPersonIcon

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (text column started at x=159 in a 723-wide card) and scaled to this
# app's 800-wide card (factor 799/723 ~= 1.105) - same value as the other
# "detail page" layouts.
_LEFT_MARGIN = 176
_FIELD_WIDTH = 453


class PearIDPage:
    def __init__(self, app):
        self.app = app
        self._logged_in = False
        self._password_shown = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = AccountServicesIcon(height=48)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN + 25)
        icon.set_margin_top(65)
        content.append(icon)

        self.title = Gtk.Label(label="Sign In with Your PearID")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(22)
        content.append(self.title)

        self.description = Gtk.Label(
            label="Sign in to sync your data, access the App Store, and more."
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(4)
        self.description.set_max_width_chars(56)
        content.append(self.description)

        self.email_entry = Gtk.Entry(placeholder_text="Email or Phone Number")
        self.email_entry.add_css_class("textbox")
        self.email_entry.set_size_request(_FIELD_WIDTH, -1)
        self.email_entry.set_halign(Gtk.Align.START)
        self.email_entry.set_margin_start(_LEFT_MARGIN)
        self.email_entry.set_margin_top(26)
        self.email_entry.connect("activate", self._on_email_activate)
        content.append(self.email_entry)

        self.password_entry = Gtk.PasswordEntry(placeholder_text="Password", show_peek_icon=True)
        self.password_entry.add_css_class("textbox")
        self.password_entry.set_size_request(_FIELD_WIDTH, -1)
        self.password_entry.set_halign(Gtk.Align.START)
        self.password_entry.set_margin_start(_LEFT_MARGIN)
        self.password_entry.set_margin_top(8)
        self.password_entry.set_visible(False)
        self.password_entry.connect("activate", self._on_password_activate)
        content.append(self.password_entry)

        links = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        links.set_halign(Gtk.Align.START)
        links.set_margin_start(_LEFT_MARGIN)
        links.set_margin_top(10)
        # Plain labels, not real links - same as data_privacy.py's
        # "Learn More...": no destination exists for either yet
        # (account creation/password reset both live on account.pearos.xyz,
        # not in this app), styled to read as a link without behaving like
        # a broken one.
        self.create_link = Gtk.Label(label="Create new PearID...")
        self.create_link.add_css_class("privacy-learn-more")
        self.forgot_link = Gtk.Label(label="Forgot password?")
        self.forgot_link.add_css_class("privacy-learn-more")
        for link in (self.create_link, self.forgot_link):
            link.set_halign(Gtk.Align.START)
            links.append(link)
        content.append(links)

        note_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        note_row.set_halign(Gtk.Align.START)
        note_row.set_margin_start(_LEFT_MARGIN)
        note_row.set_margin_top(153)
        note_icon = TwoPersonIcon(size=24)
        note_icon.set_valign(Gtk.Align.START)
        note_icon.set_margin_top(2)
        note_row.append(note_icon)
        self.note_label = Gtk.Label(
            label=(
                "This pearOS Computer will be linked to your PearID and data "
                "such as photos, contacts, and documents will be synced so "
                "you can access them on other devices."
            )
        )
        self.note_label.add_css_class("description")
        self.note_label.set_wrap(True)
        self.note_label.set_justify(Gtk.Justification.LEFT)
        self.note_label.set_halign(Gtk.Align.START)
        self.note_label.set_max_width_chars(50)
        note_row.append(self.note_label)
        content.append(note_row)

        self.status_label = Gtk.Label(label="")
        self.status_label.add_css_class("password-check")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_margin_start(_LEFT_MARGIN)
        self.status_label.set_margin_top(6)
        content.append(self.status_label)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

        self.later_btn = Gtk.Button(label="Set Up Later")
        self.later_btn.add_css_class("nav-button")
        self.later_btn.set_halign(Gtk.Align.START)
        self.later_btn.set_valign(Gtk.Align.END)
        self.later_btn.set_margin_start(20)
        self.later_btn.set_margin_bottom(20)
        self.later_btn.connect("clicked", lambda b: self.app.go_to("user"))
        self.card.overlay.add_overlay(self.later_btn)

    def on_show(self):
        self.card.forward_button.set_sensitive(False)
        self.status_label.set_label("Checking sign-in status...")

        def check():
            state = backend.check_state()
            GLib.idle_add(self._on_state_checked, state)

        import threading

        threading.Thread(target=check, daemon=True).start()

    def _on_state_checked(self, state):
        if state == "loggedin":
            info = backend.get_user_info()
            self._show_signed_in(info)
        else:
            self.status_label.set_label("")
        return False

    def _show_signed_in(self, info):
        self._logged_in = True
        self.email_entry.set_visible(False)
        self.password_entry.set_visible(False)
        name = info.get("name") or info.get("email") or "your PearID"
        self.status_label.set_label("Signed in as " + name)
        self.card.forward_button.set_sensitive(True)

    def _on_email_activate(self, _entry):
        if not self.email_entry.get_text().strip():
            self.status_label.set_label("Enter your email or phone number.")
            return
        if not self._password_shown:
            self._password_shown = True
            self.password_entry.set_visible(True)
            self.password_entry.grab_focus()
            self.status_label.set_label("")
        else:
            self._attempt_login()

    def _on_password_activate(self, _entry):
        self._attempt_login()

    def _attempt_login(self):
        email = self.email_entry.get_text().strip()
        password = self.password_entry.get_text()
        if not email or not password:
            self.status_label.set_label("Enter your email and password.")
            return
        self.email_entry.set_sensitive(False)
        self.password_entry.set_sensitive(False)
        self.status_label.set_label("Signing in...")

        def do_login():
            ok, error = backend.login(email, password)
            GLib.idle_add(self._on_login_result, ok, error)

        import threading

        threading.Thread(target=do_login, daemon=True).start()

    def _on_login_result(self, ok, error):
        self.email_entry.set_sensitive(True)
        self.password_entry.set_sensitive(True)
        if ok:
            info = backend.get_user_info()
            self._show_signed_in(info)
        else:
            self.status_label.set_label(error or "Sign in failed.")

    def _on_back(self):
        self.app.go_to("data_privacy")

    def _on_continue(self):
        self.app.go_to("user")
