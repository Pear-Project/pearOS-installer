"""Port of the 12-blade CSS clock spinner (.spinner/.spinner-blade,
spinner-fade keyframes) on the "examining volumes" page - 12 bars
arranged radially, each fading #69717d -> transparent over 1s linear
infinite, staggered 0.083s apart so the fade chases around the circle."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLADE_COLOR = (0x69 / 255, 0x71 / 255, 0x7D / 255)
_BLADE_COUNT = 12
_STAGGER_S = 0.083
_CYCLE_S = 1.0


def _rounded_bar(cr, cx, cy, w, h, r):
    cr.new_path()
    cr.arc(cx - w / 2 + r, cy - h / 2 + r, r, math.pi, 1.5 * math.pi)
    cr.arc(cx + w / 2 - r, cy - h / 2 + r, r, 1.5 * math.pi, 2 * math.pi)
    cr.arc(cx + w / 2 - r, cy + h / 2 - r, r, 0, 0.5 * math.pi)
    cr.arc(cx - w / 2 + r, cy + h / 2 - r, r, 0.5 * math.pi, math.pi)
    cr.close_path()


class SpinnerWidget(Gtk.DrawingArea):
    def __init__(self, size=25):
        super().__init__()
        self._size = size
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)
        self._start_us = None

    def start(self):
        self._start_us = None
        self.add_tick_callback(self._tick)

    def _tick(self, widget, frame_clock):
        widget.queue_draw()
        return True

    def _draw(self, area, cr, w, h):
        frame_clock = self.get_frame_clock()
        now_us = frame_clock.get_frame_time() if frame_clock else 0
        if self._start_us is None:
            self._start_us = now_us
        elapsed = (now_us - self._start_us) / 1_000_000.0

        cx, cy = w / 2.0, h / 2.0
        blade_w = w * 0.074
        blade_h = h * 0.28
        radius_inner = h * 0.22

        r, g, b = _BLADE_COLOR
        for i in range(_BLADE_COUNT):
            angle = math.radians(i * 30)
            delay = i * _STAGGER_S
            t = ((elapsed - delay) % _CYCLE_S) / _CYCLE_S
            alpha = max(0.0, 1.0 - t)
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(angle)
            bar_cy = -(radius_inner + blade_h / 2.0)
            _rounded_bar(cr, 0, bar_cy, blade_w, blade_h, blade_w / 2.0)
            cr.set_source_rgba(r, g, b, alpha)
            cr.fill()
            cr.restore()
