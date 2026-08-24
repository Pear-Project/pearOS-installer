"""Reusable frame-synced Cairo animation canvas + easing helpers.

Used by pages/hello.py and pages/finish.py to reproduce the CSS
stroke-dasharray/stroke-dashoffset "handwriting" animations
(anim__hello / anim__welcome / drawStroke+fillFade in the original CSS)
with cairo.Context.set_dash(), which supports the exact same dash/offset
model natively.
"""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - pow(1 - t, 3)


def linear(t):
    return max(0.0, min(1.0, t))


def flatten_cubic(p0, p1, p2, p3, out, tolerance=0.5, depth=0):
    """Recursive De Casteljau flattening, used to estimate path length for
    dash-array sizing (mirrors what a browser computes for stroke-dasharray)."""
    if depth > 16:
        out.append(p3)
        return
    # Flatness test: distance of control points from the p0-p3 chord.
    dx, dy = p3[0] - p0[0], p3[1] - p0[1]
    d1 = abs((p1[0] - p3[0]) * dy - (p1[1] - p3[1]) * dx)
    d2 = abs((p2[0] - p3[0]) * dy - (p2[1] - p3[1]) * dx)
    if (d1 + d2) ** 2 < tolerance * (dx * dx + dy * dy):
        out.append(p3)
        return

    def mid(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    p01, p12, p23 = mid(p0, p1), mid(p1, p2), mid(p2, p3)
    p012, p123 = mid(p01, p12), mid(p12, p23)
    p0123 = mid(p012, p123)
    flatten_cubic(p0, p01, p012, p0123, out, tolerance, depth + 1)
    flatten_cubic(p0123, p123, p23, p3, out, tolerance, depth + 1)


def path_length(ops):
    """Approximate the total length of parsed svgpath ops (see svgpath.py)."""
    length = 0.0
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    for op in ops:
        if op[0] == "M":
            cur = (op[1], op[2])
            start = cur
        elif op[0] == "L":
            nxt = (op[1], op[2])
            length += ((nxt[0] - cur[0]) ** 2 + (nxt[1] - cur[1]) ** 2) ** 0.5
            cur = nxt
        elif op[0] == "C":
            p1, p2, p3 = (op[1], op[2]), (op[3], op[4]), (op[5], op[6])
            pts = []
            flatten_cubic(cur, p1, p2, p3, pts)
            prev = cur
            for pt in pts:
                length += ((pt[0] - prev[0]) ** 2 + (pt[1] - prev[1]) ** 2) ** 0.5
                prev = pt
            cur = p3
        elif op[0] == "Z":
            length += ((start[0] - cur[0]) ** 2 + (start[1] - cur[1]) ** 2) ** 0.5
            cur = start
    return length


class AnimatedCanvas(Gtk.DrawingArea):
    """A DrawingArea that calls draw_func(cr, width, height, progress) once per
    frame for `duration_s` seconds, using the widget's frame clock (smoother
    and cheaper than a manual GLib.timeout_add poll loop)."""

    def __init__(self, duration_s, draw_func, easing=linear, on_complete=None):
        super().__init__()
        self._duration = duration_s
        self._draw_func = draw_func
        self._easing = easing
        self._on_complete = on_complete
        self._progress = 0.0
        self._start_us = None
        self.set_draw_func(self._on_draw)

    def _on_draw(self, area, cr, w, h):
        self._draw_func(cr, w, h, self._progress)

    def start(self):
        self._start_us = None
        self.add_tick_callback(self._tick)

    def _tick(self, widget, frame_clock):
        now = frame_clock.get_frame_time()
        if self._start_us is None:
            self._start_us = now
        elapsed = (now - self._start_us) / 1_000_000.0
        raw = min(1.0, elapsed / self._duration) if self._duration > 0 else 1.0
        self._progress = self._easing(raw)
        widget.queue_draw()
        if raw >= 1.0:
            if self._on_complete:
                self._on_complete()
            return False
        return True
