"""Selectable world map for the timezone page - a stylized (not
geographically precise) equirectangular continent silhouette with one dot
per entry in state.COMMON_TIMEZONES, clickable, kept in sync with the
SelectList next to it. Matches Calamares' own timezone page layout (map +
list together), just without KPMcore's SVG map data, which lives in a
package this app doesn't depend on - the continents below are a hand-drawn
approximation, good enough to recognize at a glance and to click into the
right region; the actual timezone precision comes from the dot coordinates
and the list, not the coastlines.

Projection: plain equirectangular (x = lon, y = -lat), which is exactly
what the (lon, lat) polygons and TIMEZONE_COORDS below are already in, so
mapping to widget pixels is one shared linear scale for both."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk

MAP_WIDTH = 440
MAP_HEIGHT = 220

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

# Rough, simplified continent silhouettes as (lon, lat) point lists - not
# real coastline data, just enough shape to be recognizable at map scale.
_CONTINENTS = [
    # North America
    [
        (-165, 68), (-140, 70), (-125, 55), (-125, 48), (-124, 40),
        (-117, 32), (-105, 20), (-97, 18), (-90, 16), (-86, 13),
        (-83, 9), (-80, 9), (-81, 22), (-81, 31), (-75, 35), (-70, 41),
        (-67, 45), (-60, 50), (-65, 60), (-80, 62), (-90, 68),
        (-110, 72), (-130, 70), (-165, 68),
    ],
    # South America
    [
        (-80, 10), (-77, 5), (-70, -5), (-70, -18), (-72, -30),
        (-70, -40), (-68, -52), (-65, -55), (-58, -52), (-53, -35),
        (-48, -25), (-40, -10), (-35, -5), (-45, 0), (-50, 5),
        (-60, 8), (-70, 10), (-80, 10),
    ],
    # Europe
    [
        (-10, 36), (-9, 43), (0, 49), (5, 51), (10, 54), (15, 55),
        (20, 54), (25, 60), (30, 60), (38, 66), (30, 70), (20, 70),
        (10, 63), (5, 58), (-2, 58), (-8, 50), (-10, 43), (-10, 36),
    ],
    # Africa
    [
        (-17, 15), (-16, 12), (-13, 7), (-10, 5), (-5, 5), (0, 6),
        (9, 4), (9, -3), (12, -6), (13, -10), (15, -17), (18, -25),
        (20, -30), (25, -34), (30, -30), (33, -25), (35, -20),
        (40, -15), (42, -5), (48, 0), (45, 10), (43, 12), (40, 15),
        (38, 18), (35, 25), (33, 31), (25, 32), (15, 32), (10, 30),
        (0, 20), (-10, 20), (-17, 15),
    ],
    # Asia (incl. Middle East, Russia, India, SE Asia)
    [
        (28, 40), (29, 45), (40, 45), (48, 42), (50, 45), (60, 55),
        (55, 60), (45, 55), (35, 55), (30, 58), (30, 70), (60, 70),
        (90, 75), (140, 75), (170, 68), (180, 66), (170, 60),
        (160, 55), (140, 45), (130, 42), (122, 30), (120, 23),
        (110, 18), (105, 10), (100, 5), (95, 5), (90, 15), (88, 22),
        (80, 8), (77, 8), (72, 20), (68, 24), (61, 25), (50, 25),
        (48, 30), (40, 37), (35, 37), (28, 40),
    ],
    # Australia
    [
        (113, -22), (114, -33), (118, -35), (130, -32), (137, -35),
        (140, -38), (147, -38), (150, -37), (153, -28), (150, -22),
        (145, -16), (142, -11), (135, -12), (130, -14), (126, -14),
        (122, -18), (113, -22),
    ],
]

_HIT_RADIUS = 14  # px, generous click target around each small dot


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

        # Ocean background - a soft rounded panel, not flat-transparent, so
        # the map reads as its own element against the card behind it.
        cr.save()
        cr.set_source_rgba(0.35, 0.55, 0.75, 0.10)
        cr.rectangle(0, 0, width, height)
        cr.fill()
        cr.restore()

        cr.set_line_width(1.0)
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
            cr.set_source_rgba(0.55, 0.62, 0.72, 0.45)
            cr.fill_preserve()
            cr.set_source_rgba(0.75, 0.80, 0.88, 0.55)
            cr.stroke()

        for tz, (lat, lon) in TIMEZONE_COORDS.items():
            x, y = self._project(lon, lat)
            x, y = x * scale_x, y * scale_y
            if tz == self._selected:
                cr.set_source_rgba(0.03, 0.52, 1.0, 0.25)
                cr.arc(x, y, 8, 0, 6.2832)
                cr.fill()
                cr.set_source_rgb(0.03, 0.52, 1.0)
                cr.arc(x, y, 4, 0, 6.2832)
                cr.fill()
            elif tz == self._hover:
                cr.set_source_rgba(1.0, 1.0, 1.0, 0.9)
                cr.arc(x, y, 3.2, 0, 6.2832)
                cr.fill()
            else:
                cr.set_source_rgba(1.0, 1.0, 1.0, 0.55)
                cr.arc(x, y, 2.2, 0, 6.2832)
                cr.fill()
