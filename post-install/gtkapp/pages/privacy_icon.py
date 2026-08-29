"""Cairo redraw of macOS's "Data & Privacy" glyph: two simplified person
silhouettes shaking hands, one darker blue (this device/you) and one
lighter blue (the feature/service on the other end) - no matching icon in
the system's icon theme (checked people/users/handshake-named ones), same
situation as the other custom icons in this package."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_DARK_BLUE = (0.0784, 0.4627, 0.9647)  # #1476fa
_LIGHT_BLUE = (0.4392, 0.6588, 0.9333)  # #70a8ee


def _person(cr, cx, top, color):
    cr.set_source_rgb(*color)
    head_r = 8
    cr.arc(cx, top + head_r, head_r, 0, 6.2832)
    cr.fill()
    body_top = top + head_r * 2 + 2
    body_h = 26
    half_top_w = 9
    half_bottom_w = 13
    cr.move_to(cx - half_top_w, body_top)
    cr.line_to(cx + half_top_w, body_top)
    cr.line_to(cx + half_bottom_w, body_top + body_h)
    cr.curve_to(
        cx + half_bottom_w, body_top + body_h + 6,
        cx - half_bottom_w, body_top + body_h + 6,
        cx - half_bottom_w, body_top + body_h,
    )
    cr.close_path()
    cr.fill()


class InfoIcon(Gtk.DrawingArea):
    """Small blue circle-i, for the "Learn More..." link - no "-symbolic"
    (recolorable) info icon exists in the system's icon theme, only a
    colored one at a fixed size."""

    def __init__(self, size=14):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2.0
        cr.set_source_rgb(*_DARK_BLUE)
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.fill()
        cr.set_source_rgb(1, 1, 1)
        cr.arc(cx, cy - r * 0.42, r * 0.14, 0, 6.2832)
        cr.fill()
        cr.set_line_width(r * 0.32)
        cr.set_line_cap(1)
        cr.move_to(cx, cy - r * 0.05)
        cr.line_to(cx, cy + r * 0.5)
        cr.stroke()


class PrivacyIcon(Gtk.DrawingArea):
    def __init__(self, size=76):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 76.0
        cr.save()
        cr.translate((w - 76 * s) / 2, (h - 76 * s) / 2)
        cr.scale(s, s)
        _person(cr, 28, 12, _DARK_BLUE)
        _person(cr, 48, 12, _LIGHT_BLUE)
        cr.restore()
