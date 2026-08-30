"""Cairo redraws of macOS's real "Apple Intelligence" setup screen glyphs,
rebranded for Piri: the big gradient app-tile icon with its "BETA" badge,
plus the three small blue glyphs next to each feature row (sparkle / orbit
/ lock). No matching assets exist in the system icon theme or this
package, so drawn directly like the other custom glyphs here (migration_
icon.py, privacy_icon.py, screen_time_icons.py)."""
import cairo
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Pango, PangoCairo

_BLUE = (0.0784, 0.4627, 0.9647)  # #1476fa


def _rounded_rect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -1.5708, 0)
    cr.arc(x + w - r, y + h - r, r, 0, 1.5708)
    cr.arc(x + r, y + h - r, r, 1.5708, 3.14159)
    cr.arc(x + r, y + r, r, 3.14159, 4.71239)
    cr.close_path()


def _sparkle(cr, cx, cy, r, color=(1, 1, 1)):
    """A 4-point "twinkle" glyph: two overlapping teardrop petals, the
    shape macOS uses for Apple Intelligence."""
    cr.save()
    cr.set_source_rgb(*color)
    for angle in (0, 1.5708):
        cr.save()
        cr.translate(cx, cy)
        cr.rotate(angle)
        cr.move_to(0, -r)
        cr.curve_to(r * 0.22, -r * 0.22, r * 0.22, -r * 0.22, r, 0)
        cr.curve_to(r * 0.22, r * 0.22, r * 0.22, r * 0.22, 0, r)
        cr.curve_to(-r * 0.22, r * 0.22, -r * 0.22, r * 0.22, -r, 0)
        cr.curve_to(-r * 0.22, -r * 0.22, -r * 0.22, -r * 0.22, 0, -r)
        cr.close_path()
        cr.fill()
        cr.restore()
    cr.restore()


class PiriAppIcon(Gtk.DrawingArea):
    """The big rounded-square gradient tile with a white sparkle glyph and
    a black "BETA" badge overlapping its bottom-right corner."""

    def __init__(self, size=76):
        super().__init__()
        # The BETA badge overlaps the tile's bottom-right corner and
        # spills outside it, same as the real icon - the draw area is
        # sized a bit larger than the tile itself so that badge isn't
        # clipped by the widget's own bounds.
        self.set_content_width(int(size * 1.14))
        self.set_content_height(int(size * 1.1))
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, _h):
        s = w / (76 * 1.14)
        tile = 76 * s

        _rounded_rect(cr, 0, 0, tile, tile, 17 * s)
        grad = cairo.LinearGradient(0, 0, tile, tile)
        grad.add_color_stop_rgb(0.0, 1.0, 0.482, 0.373)   # coral
        grad.add_color_stop_rgb(0.4, 1.0, 0.376, 0.635)   # pink
        grad.add_color_stop_rgb(0.72, 0.639, 0.365, 1.0)  # purple
        grad.add_color_stop_rgb(1.0, 0.353, 0.553, 1.0)   # blue
        cr.set_source(grad)
        cr.fill()

        _sparkle(cr, tile / 2, tile / 2, tile * 0.24)

        badge_h = 15 * s
        cr.set_source_rgb(0.1, 0.1, 0.1)

        layout = PangoCairo.create_layout(cr)
        weight_desc = Pango.FontDescription()
        weight_desc.set_family("Sen")
        weight_desc.set_weight(Pango.Weight.BOLD)
        weight_desc.set_size(int(8 * s * Pango.SCALE))
        layout.set_font_description(weight_desc)
        layout.set_text("BETA", -1)
        lw, lh = layout.get_pixel_size()

        badge_w = lw + 12 * s
        bx, by = tile - badge_w * 0.62, tile - badge_h * 0.55
        _rounded_rect(cr, bx, by, badge_w, badge_h, badge_h / 2)
        cr.fill()
        cr.save()
        cr.translate(bx + (badge_w - lw) / 2, by + (badge_h - lh) / 2)
        cr.set_source_rgb(1, 1, 1)
        PangoCairo.show_layout(cr, layout)
        cr.restore()


class SparkleIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2.0 - 1.5
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.5)
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.stroke()
        _sparkle(cr, cx, cy, r * 0.55, color=_BLUE)


class OrbitIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2.0 - 1.5
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.4)
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.stroke()
        cr.save()
        cr.translate(cx, cy)
        cr.rotate(-0.5)
        cr.scale(1.0, 0.48)
        cr.arc(0, 0, r * 0.85, 0, 6.2832)
        cr.restore()
        cr.stroke()


class LockIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 24.0
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.7 * s)
        cr.set_line_join(1)

        body_x, body_y = 5 * s, 11 * s
        body_w, body_h = 14 * s, 10 * s
        _rounded_rect(cr, body_x, body_y, body_w, body_h, 2.4 * s)
        cr.stroke()

        cr.new_sub_path()
        cr.arc(12 * s, 9 * s, 5 * s, 3.14159, 6.2832)
        cr.stroke()

        cr.arc(12 * s, 15.5 * s, 1.3 * s, 0, 6.2832)
        cr.fill()
