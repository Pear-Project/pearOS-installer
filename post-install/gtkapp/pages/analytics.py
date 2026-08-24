"""Analytics: two settings, same keys dpkg/system-settings/backend/
privacymanager.cpp's sendDiagnostics writes (kdeglobals Privacy group).

This page runs as the live 'default' user, before the real account exists,
so it can't kwriteconfig6 directly (that would land in 'default's home and
be lost when the account is deleted on next boot) - it only persists the
choice; post_setup applies it into the real user's kdeglobals afterwards,
same handoff as save_look()/save_accessibility()."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..osrelease import OS_RELEASE
from ..widgets import page_root, make_title


class AnalyticsPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Analytics")
        content.append(self.title)

        checks = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        checks.set_halign(Gtk.Align.CENTER)
        checks.set_margin_top(16)

        name = OS_RELEASE.pretty_name
        self.analytics_check = Gtk.CheckButton(
            label="Share " + name + " Analytics with " + name + " Software and Services"
        )
        self.analytics_check.set_active(True)
        checks.append(self.analytics_check)

        self.crash_check = Gtk.CheckButton(
            label="Share Crash and Usage Data with App Developers"
        )
        self.crash_check.set_active(True)
        checks.append(self.crash_check)

        content.append(checks)

        note = Gtk.Label(
            label="This data is collected anonymously and helps improve "
            + name + ". You can change this later in System Settings."
        )
        note.add_css_class("look-note")
        note.set_wrap(True)
        note.set_justify(Gtk.Justification.CENTER)
        note.set_max_width_chars(60)
        note.set_margin_top(10)
        content.append(note)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("location_services")

    def _on_continue(self):
        self.app.state.save_analytics(
            self.analytics_check.get_active(), self.crash_check.get_active()
        )
        self.app.go_to("screen_time")
