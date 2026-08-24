"""A small Cairo-drawn fingerprint glyph (concentric arcs, not an icon-theme
dependency) that pulses while scanning and fills up ring by ring as
touchid_backend.EnrollSession reports each swipe/stage."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_RINGS = 6
_IDLE_COLOR = (0.75, 0.75, 0.76)
_FILLED_COLOR = (0.02, 0.53, 1.0)  # matches the app's accent blue
_DONE_COLOR = (0.16, 0.66, 0.27)


class FingerprintWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_content_width(120)
        self.set_content_height(120)
        self.set_draw_func(self._draw)
        self._filled = 0
        self._total = _RINGS
        self._scanning = False
        self._done = False
        self._pulse_t = 0.0

    def set_total_stages(self, total):
        self._total = max(1, total)
        self.queue_draw()

    def start_scanning(self):
        self._scanning = True
        self._done = False
        self._filled = 0
        self.add_tick_callback(self._tick)
        self.queue_draw()

    def advance(self):
        self._filled = min(self._total, self._filled + 1)
        self.queue_draw()

    def set_done(self, success):
        self._scanning = False
        self._done = success
        if success:
            self._filled = self._total
        self.queue_draw()

    def reset(self):
        self._scanning = False
        self._done = False
        self._filled = 0
        self.queue_draw()

    def _tick(self, widget, frame_clock):
        self._pulse_t = (frame_clock.get_frame_time() / 1_000_000.0) % 2.0
        widget.queue_draw()
        return self._scanning

    def _draw(self, area, cr, w, h):
        cx, cy = w / 2.0, h / 2.0
        pulse = 0.0
        if self._scanning:
            pulse = (1 - math.cos(self._pulse_t * math.pi)) / 2.0  # 0..1..0

        max_radius = min(w, h) / 2.0 - 6
        step = max_radius / (_RINGS + 1)

        for i in range(_RINGS):
            radius = step * (i + 1.6)
            filled = i < self._filled
            if self._done and self._filled >= self._total:
                color = _DONE_COLOR
            elif filled:
                color = _FILLED_COLOR
            else:
                color = _IDLE_COLOR

            extra = 1.5 * pulse if (self._scanning and i == self._filled) else 0.0
            cr.set_line_width(4.5)
            cr.set_line_cap(1)
            cr.set_source_rgba(*color, 0.95)
            # A fingerprint-like nested-arc glyph: each ring is an open arc
            # (not a full circle) mimicking a ridge line, alternating which
            # side stays open.
            start = math.radians(200 if i % 2 == 0 else -20)
            end = math.radians(340 if i % 2 == 0 else 120)
            cr.arc(cx, cy, radius + extra, start, end)
            cr.stroke()

        # Center dot
        dot_color = _DONE_COLOR if self._done else (_FILLED_COLOR if self._scanning else _IDLE_COLOR)
        cr.set_source_rgba(*dot_color, 0.95)
        cr.arc(cx, cy, 4 + 2 * pulse, 0, 2 * math.pi)
        cr.fill()
