"""Select Your Time Zone - matches macOS's real layout: centered title and
instructions, a "set automatically" checkbox, the clickable world map, and
a Time Zone/Closest City info block below it (a dropdown, not the list
this used to show) - measured off a real screenshot of this exact page."""
import json
import threading
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Pango

from .. import state as state_mod
from ..widgets import page_root
from .worldmap import WorldMapWidget


def _detect_geoip_timezone():
    try:
        with urllib.request.urlopen("https://ipwho.is/", timeout=8) as resp:
            data = json.loads(resp.read().decode())
        if not data.get("success", True):
            return None
        return data.get("timezone", {}).get("id")
    except Exception:
        return None


def _city_label(tz):
    return tz.split("/")[-1].replace("_", " ")


def _tz_display(tz):
    try:
        offset = datetime.now(ZoneInfo(tz)).strftime("%z")
        sign = offset[0]
        return f"{_city_label(tz)} Time (UTC{sign}{offset[1:3]}:{offset[3:]})"
    except Exception:
        return tz


class TimezonePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        self.title = Gtk.Label(label="Select Your Time Zone")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(176)
        self.title.set_margin_top(40)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "To select a time zone, click the map near your location and "
                "choose a city from the Closest City menu.\nYou can also have "
                "the time zone change automatically, if possible, based on "
                "your current location."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.CENTER)
        self.description.set_halign(Gtk.Align.CENTER)
        self.description.set_margin_top(16)
        self.description.set_max_width_chars(72)
        content.append(self.description)

        self.auto_check = Gtk.CheckButton(label="Set time zone automatically using current location")
        self.auto_check.set_halign(Gtk.Align.CENTER)
        self.auto_check.set_margin_top(14)
        self.auto_check.connect("toggled", self._on_auto_toggled)
        content.append(self.auto_check)

        self.map = WorldMapWidget(on_pick=self._on_map_pick)
        self.map.set_margin_top(20)
        content.append(self.map)

        info = Gtk.Grid()
        info.set_halign(Gtk.Align.CENTER)
        info.set_margin_top(16)
        info.set_row_spacing(6)
        info.set_column_spacing(10)

        tz_label = Gtk.Label(label="Time Zone:")
        tz_label.add_css_class("account-name-hint")
        tz_label.set_halign(Gtk.Align.END)
        info.attach(tz_label, 0, 0, 1, 1)
        self.tz_value = Gtk.Label(label="")
        self.tz_value.add_css_class("description")
        self.tz_value.set_halign(Gtk.Align.START)
        info.attach(self.tz_value, 1, 0, 1, 1)

        city_label = Gtk.Label(label="Closest City:")
        city_label.add_css_class("account-name-hint")
        city_label.set_halign(Gtk.Align.END)
        info.attach(city_label, 0, 1, 1, 1)

        self._tz_list = list(state_mod.COMMON_TIMEZONES)
        self.city_dropdown = Gtk.DropDown.new_from_strings(
            [_city_label(tz) for tz in self._tz_list]
        )
        self.city_dropdown.add_css_class("timezone-dropdown")
        self.city_dropdown.set_halign(Gtk.Align.START)
        self.city_dropdown.set_size_request(140, -1)
        factory = Gtk.SignalListItemFactory()
        factory.connect("setup", self._setup_city_row)
        factory.connect("bind", self._bind_city_row)
        self.city_dropdown.set_factory(factory)
        self.city_dropdown.connect("notify::selected", self._on_dropdown_changed)
        info.attach(self.city_dropdown, 1, 1, 1, 1)
        content.append(info)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def _select_tz(self, tz, from_dropdown=False, from_map=False):
        self._current_tz = tz
        self.tz_value.set_label(_tz_display(tz))
        self.map.set_selected(tz)
        if not from_dropdown and tz in self._tz_list:
            self.city_dropdown.set_selected(self._tz_list.index(tz))

    def _setup_city_row(self, _factory, list_item):
        label = Gtk.Label(xalign=0)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_width_chars(14)
        label.set_max_width_chars(14)
        list_item.set_child(label)

    def _bind_city_row(self, _factory, list_item):
        label = list_item.get_child()
        label.set_label(list_item.get_item().get_string())

    def _on_map_pick(self, tz):
        self._select_tz(tz, from_map=True)

    def _on_dropdown_changed(self, dropdown, _pspec):
        idx = dropdown.get_selected()
        if 0 <= idx < len(self._tz_list):
            self._select_tz(self._tz_list[idx], from_dropdown=True)

    def _on_auto_toggled(self, check):
        auto = check.get_active()
        self.map.set_sensitive(not auto)
        self.city_dropdown.set_sensitive(not auto)
        if auto:
            threading.Thread(target=self._detect_geoip_async, daemon=True).start()

    def _detect_geoip_async(self):
        tz = _detect_geoip_timezone()
        GLib.idle_add(self._apply_geoip_result, tz)

    def _apply_geoip_result(self, tz):
        if tz and self.auto_check.get_active():
            self._select_tz(tz)
        return False

    def on_show(self):
        tz = self.app.state.timezone or self._tz_list[0]
        self._select_tz(tz)

    def _on_back(self):
        self.app.go_to("location_services")

    def _on_continue(self):
        tz = self._current_tz
        windows_detected = self.app.state.detect_windows_dual_boot()
        err = self.app.state.save_timezone(tz, not windows_detected)
        if err:
            self.app.show_alert(err)
            return
        self.app.go_to("analytics")
