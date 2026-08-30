"""Selectable world map for the timezone page - real country-boundary
polygons (simplified from a public world.geo.json dataset, see
world_polygons.json) with one dot per entry in state.COMMON_TIMEZONES,
clickable, kept in sync with the SelectList next to it.

Projection: plain equirectangular (x = lon, y = -lat), which is exactly
what the (lon, lat) polygons and TIMEZONE_COORDS below are already in, so
mapping to widget pixels is one shared linear scale for both."""
import json
import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk

MAP_WIDTH = 480
MAP_HEIGHT = 240

_POLYGONS_PATH = os.path.join(os.path.dirname(__file__), "world_polygons.json")
with open(_POLYGONS_PATH) as _f:
    _CONTINENTS = json.load(_f)

# One representative (lat, lon) per COMMON_TIMEZONES entry (state.py) -
# the zone's principal city, close enough for a click-to-pick map.
TIMEZONE_COORDS = {
    "Africa/Cairo": (30.0, 31.2),
    "Africa/Johannesburg": (-26.2, 28.0),
    "Africa/Lagos": (6.5, 3.4),
    "Africa/Nairobi": (-1.3, 36.8),
    "America/Anchorage": (61.2, -149.9),
    "America/Argentina/Buenos_Aires": (-34.6, -58.4),
    "America/Bogota": (4.7, -74.1),
    "America/Chicago": (41.9, -87.6),
    "America/Denver": (39.7, -105.0),
    "America/Los_Angeles": (34.0, -118.2),
    "America/Mexico_City": (19.4, -99.1),
    "America/New_York": (40.7, -74.0),
    "America/Sao_Paulo": (-23.5, -46.6),
    "America/Toronto": (43.7, -79.4),
    "America/Vancouver": (49.3, -123.1),
    "Asia/Bangkok": (13.8, 100.5),
    "Asia/Dubai": (25.2, 55.3),
    "Asia/Hong_Kong": (22.3, 114.2),
    "Asia/Istanbul": (41.0, 29.0),
    "Asia/Jakarta": (-6.2, 106.8),
    "Asia/Jerusalem": (31.8, 35.2),
    "Asia/Kolkata": (22.6, 88.4),
    "Asia/Seoul": (37.6, 127.0),
    "Asia/Shanghai": (31.2, 121.5),
    "Asia/Singapore": (1.35, 103.8),
    "Asia/Tokyo": (35.7, 139.7),
    "Atlantic/Reykjavik": (64.1, -21.9),
    "Australia/Melbourne": (-37.8, 145.0),
    "Australia/Perth": (-32.0, 115.9),
    "Australia/Sydney": (-33.9, 151.2),
    "Europe/Amsterdam": (52.4, 4.9),
    "Europe/Athens": (38.0, 23.7),
    "Europe/Berlin": (52.5, 13.4),
    "Europe/Bucharest": (44.4, 26.1),
    "Europe/Budapest": (47.5, 19.1),
    "Europe/Dublin": (53.35, -6.3),
    "Europe/Helsinki": (60.2, 24.9),
    "Europe/Lisbon": (38.7, -9.1),
    "Europe/London": (51.5, -0.1),
    "Europe/Madrid": (40.4, -3.7),
    "Europe/Moscow": (55.75, 37.6),
    "Europe/Paris": (48.9, 2.35),
    "Europe/Prague": (50.1, 14.4),
    "Europe/Rome": (41.9, 12.5),
    "Europe/Stockholm": (59.3, 18.1),
    "Europe/Vienna": (48.2, 16.4),
    "Europe/Warsaw": (52.2, 21.0),
    "Europe/Zurich": (47.4, 8.5),
    "Pacific/Auckland": (-36.85, 174.76),
    "Pacific/Honolulu": (21.3, -157.9),
}

_HIT_RADIUS = 14


class WorldMapWidget(Gtk.DrawingArea):
    """A dot per timezone on a stylized world silhouette. `on_pick(tz)` is
    called when the user clicks near a dot; `set_selected(tz)` lets the
    caller (the paired SelectList) push a selection the other way."""

    def __init__(self, on_pick):
        super().__init__()
        self._on_pick = on_pick
        self._selected = None
        self.set_content_width(MAP_WIDTH)
        self.set_content_height(MAP_HEIGHT)
        self.set_halign(Gtk.Align.CENTER)
        self.set_margin_top(14)
        self.set_draw_func(self._draw)

        click = Gtk.GestureClick()
        click.connect("released", self._on_click)
        self.add_controller(click)

        motion = Gtk.EventControllerMotion()
        motion.connect("motion", self._on_motion)
        motion.connect("leave", self._on_leave)
        self.add_controller(motion)
        self._hover = None

    def set_selected(self, tz):
        if tz != self._selected:
            self._selected = tz
            self.queue_draw()

    @staticmethod
    def _project(lon, lat):
        x = (lon + 180.0) / 360.0 * MAP_WIDTH
        y = (90.0 - lat) / 180.0 * MAP_HEIGHT
        return x, y

    def _nearest_tz(self, x, y):
        best_tz, best_dist = None, _HIT_RADIUS
        for tz, (lat, lon) in TIMEZONE_COORDS.items():
            px, py = self._project(lon, lat)
            dist = ((px - x) ** 2 + (py - y) ** 2) ** 0.5
            if dist < best_dist:
                best_tz, best_dist = tz, dist
        return best_tz

    def _on_click(self, _gesture, _n_press, x, y):
        tz = self._nearest_tz(x, y)
        if tz is not None:
            self._selected = tz
            self.queue_draw()
            self._on_pick(tz)

    def _on_motion(self, _controller, x, y):
        tz = self._nearest_tz(x, y)
        cursor_name = "pointer" if tz else "default"
        self.set_cursor(Gdk.Cursor.new_from_name(cursor_name))
        if tz != self._hover:
            self._hover = tz
            self.queue_draw()

    def _on_leave(self, _controller):
        if self._hover is not None:
            self._hover = None
            self.queue_draw()

    def _draw(self, _area, cr, width, height):
        scale_x = width / MAP_WIDTH
        scale_y = height / MAP_HEIGHT

        for poly in _CONTINENTS:
            cr.new_path()
            for i, (lon, lat) in enumerate(poly):
                x, y = self._project(lon, lat)
                x, y = x * scale_x, y * scale_y
                if i == 0:
                    cr.move_to(x, y)
                else:
                    cr.line_to(x, y)
            cr.close_path()
            cr.set_source_rgb(0.78, 0.78, 0.78)
            cr.fill()

        if self._selected is not None and self._selected in TIMEZONE_COORDS:
            lat, lon = TIMEZONE_COORDS[self._selected]
            x, y = self._project(lon, lat)
            x, y = x * scale_x, y * scale_y
            cr.set_source_rgb(0.03, 0.52, 1.0)
            cr.arc(x, y, 3.5, 0, 6.2832)
            cr.fill()

        for tz, (lat, lon) in TIMEZONE_COORDS.items():
            x, y = self._project(lon, lat)
            x, y = x * scale_x, y * scale_y
            if tz == self._hover and tz != self._selected:
                cr.set_source_rgba(0.03, 0.52, 1.0, 0.5)
                cr.arc(x, y, 3.0, 0, 6.2832)
                cr.fill()
