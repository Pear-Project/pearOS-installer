"""Cairo redraw of the "current location" navigation-arrow glyph macOS
uses for Location Services - a thin outlined dart/kite shape, no matching
icon in the system's icon theme (breeze's compass-symbolic is a full
compass face, a different glyph entirely)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)


class LocationArrowIcon(Gtk.DrawingArea):
    def __init__(self, size=76):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(w * 0.055)
        cr.set_line_join(1)
        cr.set_line_cap(1)

        tip_x, tip_y = w * 0.62, h * 0.12
        left_x, left_y = w * 0.20, h * 0.88
        right_x, right_y = w * 0.62, h * 0.62
        notch_x, notch_y = w * 0.88, h * 0.88

        cr.move_to(tip_x, tip_y)
        cr.line_to(notch_x, notch_y)
        cr.line_to(right_x, right_y)
        cr.line_to(left_x, left_y)
        cr.close_path()
        cr.stroke()
