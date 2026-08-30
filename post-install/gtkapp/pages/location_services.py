"""Location Services - matches macOS's real layout: left-aligned icon/
title/paragraph, a single checkbox, and an "About Location Services &
Privacy..." link near the bottom with a small info icon - same "detail
page" layout as migration_assistant.py/written_spoken.py/etc.

Real toggle: enables/disables the geoclue.service systemd unit (KDE's own
location backend), not just an in-memory flag like
dpkg/system-settings/backend/privacymanager.cpp's setLocationServices()
(which never actually persists anything - this goes one step further)."""
import subprocess

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root
from .location_icon import LocationArrowIcon
from .privacy_icon import InfoIcon

_LEFT_MARGIN = 176


def _set_geoclue_enabled(enabled):
    action = ["--now", "enable"] if enabled else ["--now", "disable"]
    try:
        subprocess.Popen(["sudo", "systemctl"] + action + ["geoclue.service"])
    except OSError:
        pass


class LocationServicesPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = LocationArrowIcon(size=76)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Enable Location Services")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Location Services allows apps like Maps and services like "
                "Spotlight Suggestions to gather and use data including your "
                "approximate location."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(4)
        self.description.set_max_width_chars(56)
        content.append(self.description)

        self.toggle = Gtk.CheckButton(label="Enable Location Services on this pearOS Computer")
        self.toggle.set_active(False)
        self.toggle.set_halign(Gtk.Align.START)
        self.toggle.set_margin_start(_LEFT_MARGIN)
        self.toggle.set_margin_top(28)
        content.append(self.toggle)

        link_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        link_row.set_halign(Gtk.Align.START)
        link_row.set_margin_start(_LEFT_MARGIN)
        link_row.set_margin_top(196)
        info_icon = InfoIcon(size=14)
        info_icon.set_valign(Gtk.Align.CENTER)
        link_row.append(info_icon)
        link_label = Gtk.Label(label="About Location Services & Privacy...")
        link_label.add_css_class("privacy-learn-more")
        link_row.append(link_label)
        content.append(link_row)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("agreement")

    def _on_continue(self):
        _set_geoclue_enabled(self.toggle.get_active())
        self.app.go_to("timezone")
