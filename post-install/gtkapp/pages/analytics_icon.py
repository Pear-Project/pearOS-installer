import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)

_BAR_FRACS = [0.73, 1.0, 0.855, 0.597]
_TALLEST_FRAC = 0.92


class AnalyticsIcon(Gtk.DrawingArea):
    def __init__(self, width=84, height=75):
        super().__init__()
        self.set_content_width(width)
        self.set_content_height(height)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cr.set_source_rgb(*_BLUE)
        n = len(_BAR_FRACS)
        bar_w = w / (n + (n - 1) * 8 / 15)
        gap = bar_w * 8 / 15
        underline_h = h * 0.045
        base_y = h - underline_h
        x = 0.0
        for frac in _BAR_FRACS:
            bh = h * _TALLEST_FRAC * frac
            cr.rectangle(x, base_y - bh, bar_w, bh)
            cr.fill()
            x += bar_w + gap
        cr.rectangle(0, base_y, w, underline_h)
        cr.fill()
