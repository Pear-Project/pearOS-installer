import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)


class AnalyticsIcon(Gtk.DrawingArea):
    def __init__(self, size=76):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cr.set_source_rgb(*_BLUE)
        bar_w = w * 0.13
        gap = w * 0.07
        heights = [0.34, 0.56, 0.86, 0.62]
        base_y = h * 0.76
        total_w = len(heights) * bar_w + (len(heights) - 1) * gap
        x = (w - total_w) / 2
        for frac in heights:
            bh = h * frac
            cr.rectangle(x, base_y - bh, bar_w, bh)
            cr.fill()
            x += bar_w + gap
        cr.rectangle((w - total_w) / 2, base_y, total_w, h * 0.045)
        cr.fill()
