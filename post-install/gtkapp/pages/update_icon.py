"""Cairo redraw of macOS's real "Update Mac Automatically" gear glyph: a
solid blue cog with a hollow center - no matching icon in the system
icon theme, so drawn directly like the other custom glyphs in this
package (migration_icon.py, privacy_icon.py, screen_time_icons.py)."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)  # #1476fa

_N_TEETH = 10


class GearIcon(Gtk.DrawingArea):
    def __init__(self, size=76):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        outer_r = min(w, h) / 2.0 - 1
        inner_r = outer_r * 0.74
        tooth_half_angle = (math.pi / _N_TEETH) * 0.42

        cr.set_source_rgb(*_BLUE)
        cr.new_path()
        for i in range(_N_TEETH):
            a0 = (2 * math.pi / _N_TEETH) * i
            a_mid = a0 + (math.pi / _N_TEETH)
            body_r = inner_r

            p0 = a0 + tooth_half_angle
            p1 = a_mid - tooth_half_angle
            p2 = a_mid + tooth_half_angle
            p3 = a0 + (2 * math.pi / _N_TEETH) - tooth_half_angle

            def pt(radius, angle):
                return cx + radius * math.cos(angle), cy + radius * math.sin(angle)

            if i == 0:
                cr.move_to(*pt(body_r, a0))
            cr.line_to(*pt(body_r, p0))
            cr.line_to(*pt(outer_r, p1))
            cr.line_to(*pt(outer_r, p2))
            cr.line_to(*pt(body_r, p3))
        cr.close_path()
        cr.fill()

        # Hollow center: overpaint with the card's own white instead of
        # relying on Operator.CLEAR, which isn't safe on every backend.
        cr.set_source_rgb(1, 1, 1)
        cr.arc(cx, cy, inner_r * 0.42, 0, 2 * math.pi)
        cr.fill()
