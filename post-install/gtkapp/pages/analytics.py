"""Analytics: matches macOS's real layout - left-aligned icon/title/
paragraphs plus an "About Device Analytics & Privacy..." link, same
"detail page" convention as migration_assistant.py/location_services.py.
No toggle here (matches the reference: sharing is on by default and only
adjustable later in System Settings), same keys dpkg/system-settings/
backend/privacymanager.cpp's sendDiagnostics writes (kdeglobals Privacy
group).

This page runs as the live 'default' user, before the real account
exists, so it can't kwriteconfig6 directly (that would land in
'default's home and be lost when the account is deleted on next boot) -
it only persists the choice; post_setup applies it into the real user's
kdeglobals afterwards, same handoff as save_look()/save_accessibility()."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..osrelease import OS_RELEASE
from ..widgets import page_root
from .analytics_icon import AnalyticsIcon
from .privacy_icon import InfoIcon

_LEFT_MARGIN = 176


class AnalyticsPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)
        content.set_vexpand(True)

        icon = AnalyticsIcon(size=76)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Analytics")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        name = OS_RELEASE.rebrand(OS_RELEASE.pretty_name)

        self.subtitle = Gtk.Label(
            label=f"Help {name} and app developers improve their products "
            "and services automatically."
        )
        self.subtitle.add_css_class("description")
        self.subtitle.set_wrap(True)
        self.subtitle.set_justify(Gtk.Justification.LEFT)
        self.subtitle.set_halign(Gtk.Align.START)
        self.subtitle.set_margin_start(_LEFT_MARGIN)
        self.subtitle.set_margin_top(8)
        self.subtitle.set_max_width_chars(56)
        content.append(self.subtitle)

        self.detail = Gtk.Label(
            label=f"To help {name} improve its products and services, "
            f"pre-release beta versions of {name} automatically send "
            "diagnostics and usage data. This can be changed in the "
            "Privacy & Security pane of System Settings. Diagnostic data "
            "may include location information."
        )
        self.detail.add_css_class("description")
        self.detail.set_wrap(True)
        self.detail.set_justify(Gtk.Justification.LEFT)
        self.detail.set_halign(Gtk.Align.START)
        self.detail.set_margin_start(_LEFT_MARGIN)
        self.detail.set_margin_top(16)
        self.detail.set_max_width_chars(56)
        content.append(self.detail)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        content.append(spacer)

        link_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        link_row.set_halign(Gtk.Align.START)
        link_row.set_margin_start(_LEFT_MARGIN)
        link_row.set_margin_bottom(96)
        info_icon = InfoIcon(size=14)
        info_icon.set_valign(Gtk.Align.CENTER)
        link_row.append(info_icon)
        link_label = Gtk.Label(label="About Device Analytics & Privacy...")
        link_label.add_css_class("privacy-learn-more")
        link_row.append(link_label)
        content.append(link_row)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("timezone")

    def _on_continue(self):
        self.app.state.save_analytics(True, True)
        self.app.go_to("screen_time")
