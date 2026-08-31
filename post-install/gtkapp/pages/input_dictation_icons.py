import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)


def _rounded_rect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -1.5708, 0)
    cr.arc(x + w - r, y + h - r, r, 0, 1.5708)
    cr.arc(x + r, y + h - r, r, 1.5708, 3.14159)
    cr.arc(x + r, y + r, r, 3.14159, 4.71239)
    cr.close_path()


class KeyboardIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 24.0
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.6 * s)
        _rounded_rect(cr, 2 * s, 5 * s, 20 * s, 14 * s, 2.4 * s)
        cr.stroke()

        key_r = 0.9 * s
        rows = (7.7 * s, 12 * s, 16.3 * s)
        for ry in rows:
            for rx in (5.5 * s, 9 * s, 12.5 * s, 16 * s, 19.5 * s):
                cr.arc(rx, ry, key_r * 0.6, 0, 6.2832)
                cr.fill()


class MicrophoneIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 24.0
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.6 * s)
        cr.set_line_cap(1)
        cr.set_line_join(1)

        cap_w, cap_h = 6 * s, 12 * s
        cap_x, cap_y = 9 * s, 2 * s
        _rounded_rect(cr, cap_x, cap_y, cap_w, cap_h, cap_w / 2)
        cr.stroke()

        cr.new_sub_path()
        cr.arc(12 * s, 13 * s, 6 * s, 0.3, 3.14159 - 0.3)
        cr.stroke()

        cr.move_to(12 * s, 19 * s)
        cr.line_to(12 * s, 22 * s)
        cr.stroke()

        cr.move_to(8 * s, 22 * s)
        cr.line_to(16 * s, 22 * s)
        cr.stroke()
