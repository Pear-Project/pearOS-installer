"""Sign in with PearID: real state check + login against account.pearos.xyz
(see pearid_backend.py), with a bottom-left 'Set Up Later' skip - Continue
only enables once actually signed in."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from .. import pearid_backend as backend
from ..widgets import page_root, make_title, make_description


class PearIDPage:
    def __init__(self, app):
        self.app = app
        self._logged_in = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Sign In with PearID")
        content.append(self.title)
        self.description = make_description(
            "Sign in with your PearID to access iCloud-style sync, the App "
            "Store, and more across your pearOS devices."
        )
        content.append(self.description)

        self.form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.form.set_halign(Gtk.Align.CENTER)
        self.form.set_margin_top(16)
        self.email_entry = Gtk.Entry(placeholder_text="Email or Phone Number")
        self.email_entry.add_css_class("textbox")
        self.password_entry = Gtk.PasswordEntry(placeholder_text="Password", show_peek_icon=True)
        self.password_entry.add_css_class("textbox")
        self.form.append(self.email_entry)
        self.form.append(self.password_entry)

        self.signin_btn = Gtk.Button(label="Sign In")
        self.signin_btn.add_css_class("nav-button")
        self.signin_btn.set_margin_top(8)
        self.signin_btn.set_halign(Gtk.Align.CENTER)
        self.signin_btn.connect("clicked", self._on_signin_clicked)
        self.form.append(self.signin_btn)
        content.append(self.form)

        self.status_label = Gtk.Label(label="")
        self.status_label.add_css_class("password-check")
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
        self.later_btn.connect("clicked", lambda b: self.app.go_to("agreement"))
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
        self.form.set_visible(False)
        name = info.get("name") or info.get("email") or "your PearID"
        self.status_label.set_label("Signed in as " + name)
        self.card.forward_button.set_sensitive(True)

    def _on_signin_clicked(self, _btn):
        email = self.email_entry.get_text().strip()
        password = self.password_entry.get_text()
        if not email or not password:
            self.status_label.set_label("Enter your email and password.")
            return
        self.signin_btn.set_sensitive(False)
        self.status_label.set_label("Signing in...")

        def do_login():
            ok, error = backend.login(email, password)
            GLib.idle_add(self._on_login_result, ok, error)

        import threading

        threading.Thread(target=do_login, daemon=True).start()

    def _on_login_result(self, ok, error):
        self.signin_btn.set_sensitive(True)
        if ok:
            info = backend.get_user_info()
            self._show_signed_in(info)
        else:
            self.status_label.set_label(error or "Sign in failed.")
        return False

    def _on_back(self):
        self.app.go_to("migration_assistant")

    def _on_continue(self):
        self.app.go_to("agreement")
