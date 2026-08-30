"""Cairo redraws of the small glyph cluster macOS shows above "Sign In to
Your Apple Account" (cloud/notes/music/messages, one rounded-square tile
each) - no matching icon set exists for this, drawn directly like the
other custom icons in this package. Also the small two-person "this
device will be linked to your account" glyph below the links."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)
_LIGHT_BLUE = (0.4392, 0.6588, 0.9333)


def _tile(cr, x, y, size, radius):
    cr.new_sub_path()
    cr.arc(x + size - radius, y + radius, radius, -math.pi / 2, 0)
    cr.arc(x + size - radius, y + size - radius, radius, 0, math.pi / 2)
    cr.arc(x + radius, y + size - radius, radius, math.pi / 2, math.pi)
    cr.arc(x + radius, y + radius, radius, math.pi, math.pi * 1.5)
    cr.close_path()


class AccountServicesIcon(Gtk.DrawingArea):
    _STEP_FACTOR = 0.98
    _RISE_FACTOR = 0.12

    def __init__(self, tile=40):
        super().__init__()
        step = tile * self._STEP_FACTOR
        rise = tile * self._RISE_FACTOR
        self.set_content_width(int(tile + step * 3))
        self.set_content_height(int(tile + rise * 3))
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        tile = h / (1 + 3 * self._RISE_FACTOR)
        step = tile * self._STEP_FACTOR
        rise = tile * self._RISE_FACTOR
        x = 0
        y = h - tile

        # Cloud
        _tile(cr, x, y, tile, tile * 0.28)
        cr.set_source_rgb(*_BLUE)
        cr.fill()
        cr.new_path()
        cr.set_source_rgb(1, 1, 1)
        cx, cy, r = x + tile * 0.5, y + tile * 0.58, tile * 0.16
        cr.arc(cx - r * 0.7, cy, r * 0.8, 0, 2 * math.pi)
        cr.arc(cx + r * 0.4, cy - r * 0.3, r, 0, 2 * math.pi)
        cr.arc(cx - r * 0.05, cy + r * 0.1, r * 0.95, 0, 2 * math.pi)
        cr.fill()

        # Notes/pencil
        x += step
        y -= rise
        _tile(cr, x, y, tile, tile * 0.28)
        cr.set_source_rgb(1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(tile * 0.09)
        cr.stroke()
        cr.move_to(x + tile * 0.3, y + tile * 0.7)
        cr.line_to(x + tile * 0.65, y + tile * 0.3)
        cr.set_line_width(tile * 0.1)
        cr.set_line_cap(1)
        cr.stroke()

        # Music note
        x += step
        y -= rise
        _tile(cr, x, y, tile, tile * 0.28)
        cr.set_source_rgb(*_BLUE)
        cr.fill()
        cr.set_source_rgb(1, 1, 1)
        nx, ny = x + tile * 0.4, y + tile * 0.35
        cr.arc(nx, ny + tile * 0.3, tile * 0.11, 0, 2 * math.pi)
        cr.fill()
        cr.set_line_width(tile * 0.06)
        cr.move_to(nx + tile * 0.1, ny + tile * 0.3)
        cr.line_to(nx + tile * 0.1, ny)
        cr.line_to(nx + tile * 0.35, ny - tile * 0.08)
        cr.line_to(nx + tile * 0.35, ny + tile * 0.22)
        cr.stroke()

        # Message bubble
        x += step
        y -= rise
        _tile(cr, x, y, tile, tile * 0.28)
        cr.set_source_rgb(1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgb(*_LIGHT_BLUE)
        cr.set_line_width(tile * 0.09)
        cr.stroke()
        cr.new_path()
        cr.set_source_rgb(*_LIGHT_BLUE)
        bx, by, br = x + tile * 0.5, y + tile * 0.44, tile * 0.22
        cr.arc(bx, by, br, 0, 2 * math.pi)
        cr.fill()
        cr.new_path()
        cr.move_to(bx - br * 0.5, by + br * 0.75)
        cr.line_to(bx - br * 0.1, by + br * 0.5)
        cr.line_to(bx - br * 0.6, by + br * 1.3)
        cr.close_path()
        cr.fill()


class TwoPersonIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        def person(cx, color, scale):
            cr.set_source_rgb(*color)
            head_r = h * 0.16 * scale
            head_cy = h * 0.28
            cr.arc(cx, head_cy, head_r, 0, 2 * math.pi)
            cr.fill()
            body_top = head_cy + head_r * 0.9
            cr.new_sub_path()
            cr.arc(cx, body_top + h * 0.22 * scale, h * 0.22 * scale, math.pi, 2 * math.pi)
            cr.line_to(cx + h * 0.22 * scale, h * 0.78)
            cr.line_to(cx - h * 0.22 * scale, h * 0.78)
            cr.close_path()
            cr.fill()

        person(w * 0.36, _BLUE, 1.0)
        person(w * 0.66, _LIGHT_BLUE, 0.9)
