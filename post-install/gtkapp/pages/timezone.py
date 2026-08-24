"""Port of templates/timezone.html."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import state as state_mod
from ..widgets import page_root, make_title
from .common import SelectList, make_worldmap


class TimezonePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)
        content.append(make_worldmap())
        self.title = make_title("Select Your Time Zone")
        content.append(self.title)

        items = [(tz, tz) for tz in state_mod.COMMON_TIMEZONES]
        self.select_list = SelectList(items)
        content.append(self.select_list.widget)

        utc_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        utc_box.add_css_class("utc-toggle")
        utc_box.set_halign(Gtk.Align.CENTER)
        utc_box.set_margin_top(10)
        self.utc_check = Gtk.CheckButton()
        self.utc_label = Gtk.Label(
            label="Hardware clock is set to UTC (recommended unless dual-booting Windows)"
        )
        self.utc_label.set_wrap(True)
        self.utc_label.set_max_width_chars(50)
        utc_box.append(self.utc_check)
        utc_box.append(self.utc_label)
        content.append(utc_box)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        self.title.set_label(self.app.t("timezone.title", "Select Your Time Zone"))
        self.card.forward_button.set_label(self.app.t("timezone.continue", "Continue"))
        self.utc_label.set_label(
            self.app.t(
                "timezone.utcLabel",
                "Hardware clock is set to UTC (recommended unless dual-booting Windows)",
            )
        )
        windows_detected = self.app.state.detect_windows_dual_boot()
        self.utc_check.set_active(not windows_detected)

    def _on_back(self):
        self.app.go_to("written_spoken")

    def _on_continue(self):
        tz = self.select_list.selected_value()
        err = self.app.state.save_timezone(tz, self.utc_check.get_active())
        if err:
            self.app.show_alert(err)
            return
        self.app.go_to("accessibility")
