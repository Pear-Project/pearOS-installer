"""Cairo redraw of the classic "globe with meridian/latitude grid lines"
glyph macOS uses for "Written and Spoken Languages" - a circle, a vertical
ellipse (meridian curves), a horizontal ellipse (latitude curves), and a
straight vertical/horizontal diameter pair. No icon in the system's icon
theme matched this (checked breeze's locale/network/web-browser sets),
same situation as migration_icon.py - drawn directly instead."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class GlobeGridIcon(Gtk.DrawingArea):
    def __init__(self, size=64, color=(0.0784, 0.4627, 0.9647)):
        super().__init__()
        self._color = color
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2.0, h / 2.0
        r = min(w, h) * 0.42
        cr.set_source_rgb(*self._color)
        cr.set_line_width(max(1.6, min(w, h) * 0.045))
        cr.set_line_cap(1)  # round

        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.stroke()

        cr.save()
        cr.translate(cx, cy)
        cr.scale(0.5, 1.0)
        cr.arc(0, 0, r, 0, 2 * math.pi)
        cr.restore()
        cr.stroke()

        cr.save()
        cr.translate(cx, cy)
        cr.scale(1.0, 0.5)
        cr.arc(0, 0, r, 0, 2 * math.pi)
        cr.restore()
        cr.stroke()

        cr.move_to(cx, cy - r)
        cr.line_to(cx, cy + r)
        cr.stroke()

        cr.move_to(cx - r, cy)
        cr.line_to(cx + r, cy)
        cr.stroke()
