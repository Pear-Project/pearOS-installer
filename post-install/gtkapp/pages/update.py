"""Update: matches macOS's real "Update Mac Automatically" Setup
Assistant screen - left-aligned gear icon/title/paragraph, same "detail
page" convention as location_services.py/analytics.py, with an "Only
Download Automatically" button in the opposite bottom corner from
Continue (same shape as touchid_enable.py's own skip button). Comes
right after look.py, before finish.py.

Persists the choice the same way analytics.py/save_look() do: this page
runs as the live 'default' user, before the real account exists, so it
can't enable the real apt/unattended-upgrades config directly (that
would land in a systemd/apt state that has nothing to do with the
account being created) - it only records the choice; post_setup applies
it for real afterwards."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root
from .update_icon import GearIcon

_LEFT_MARGIN = 176


class UpdatePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = GearIcon(size=76)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Update pearOS Computer Automatically")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Future software updates will be automatically downloaded "
                "and installed for you as they're released. You can manage "
                "this in Software Update settings."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(8)
        self.description.set_max_width_chars(56)
        content.append(self.description)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

        self.download_only_btn = Gtk.Button(label="Only Download Automatically")
        self.download_only_btn.add_css_class("nav-button")
        self.download_only_btn.set_halign(Gtk.Align.START)
        self.download_only_btn.set_valign(Gtk.Align.END)
        self.download_only_btn.set_margin_start(20)
        self.download_only_btn.set_margin_bottom(20)
        self.download_only_btn.connect("clicked", self._on_download_only_clicked)
        self.card.overlay.add_overlay(self.download_only_btn)

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("look")

    def _on_download_only_clicked(self, _btn):
        self.app.state.save_auto_update("download_only")
        self.app.go_to("welcome")

    def _on_continue(self):
        self.app.state.save_auto_update("full")
        self.app.go_to("welcome")
