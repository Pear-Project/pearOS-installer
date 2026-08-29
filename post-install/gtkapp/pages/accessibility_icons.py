"""Cairo redraws of the 4 category glyphs (eye / pointing hand / ear /
head) macOS's Accessibility screen uses - no matching icons exist in the
system's icon theme (checked eye/hand/ear/brain-named ones), same
situation as migration_icon.py and globe_grid_icon.py. Simplified outline
shapes, not anatomically precise, at the same visual weight as the
reference's thin gray line icons."""
import math

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_GRAY = (0.35, 0.35, 0.37)
_BLUE = (0.0784, 0.4627, 0.9647)


class UniversalAccessIcon(Gtk.DrawingArea):
    """Circle outline + stick figure - the header glyph macOS uses for the
    whole Accessibility screen (distinct from the 4 small gray category
    icons below it, and from breeze's own accessibility icon, which is a
    filled circle + wheelchair symbol, not this outline + standing figure)."""

    def __init__(self, size=76):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) * 0.46
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(min(w, h) * 0.06)
        cr.set_line_cap(1)
        cr.set_line_join(1)

        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.stroke()

        head_r = h * 0.09
        head_cy = cy - h * 0.20
        cr.arc(cx, head_cy, head_r, 0, 2 * math.pi)
        cr.fill()

        torso_top = head_cy + head_r * 0.9
        arm_y = torso_top + h * 0.06
        cr.move_to(cx - w * 0.19, arm_y)
        cr.line_to(cx + w * 0.19, arm_y)
        cr.stroke()

        hip = torso_top + h * 0.20
        cr.move_to(cx, torso_top)
        cr.line_to(cx, hip)
        cr.stroke()

        foot_y = hip + h * 0.20
        cr.move_to(cx, hip)
        cr.line_to(cx - w * 0.11, foot_y)
        cr.stroke()
        cr.move_to(cx, hip)
        cr.line_to(cx + w * 0.11, foot_y)
        cr.stroke()


class CategoryIcon(Gtk.DrawingArea):
    def __init__(self, kind, size=40):
        super().__init__()
        self._kind = kind
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cr.set_source_rgb(*_GRAY)
        cr.set_line_width(max(1.4, min(w, h) * 0.05))
        cr.set_line_cap(1)
        cr.set_line_join(1)
        getattr(self, "_draw_" + self._kind)(cr, w, h)

    def _draw_vision(self, cr, w, h):
        cx, cy = w / 2, h / 2
        rx, ry = w * 0.42, h * 0.26
        cr.save()
        cr.translate(cx, cy)
        cr.scale(rx, ry)
        cr.arc(0, 0, 1, 0, 2 * math.pi)
        cr.restore()
        cr.stroke()
        cr.arc(cx, cy, w * 0.11, 0, 2 * math.pi)
        cr.stroke()

    def _draw_motor(self, cr, w, h):
        # Palm: rounded blob. Index finger: a rounded rect angled up-right,
        # roughly matching the reference's "tap/point" hand gesture.
        cx, cy = w / 2, h * 0.58
        cr.arc(cx, cy, w * 0.22, 0, 2 * math.pi)
        cr.stroke()
        fx0, fy0 = cx + w * 0.02, cy - h * 0.04
        fx1, fy1 = cx + w * 0.20, cy - h * 0.44
        cr.move_to(fx0 - w * 0.06, fy0)
        cr.line_to(fx1 - w * 0.06, fy1)
        cr.arc(fx1, fy1, w * 0.06, math.pi, 2 * math.pi)
        cr.line_to(fx0 + w * 0.06, fy0)
        cr.stroke()

    def _draw_hearing(self, cr, w, h):
        cx, cy = w / 2, h / 2
        cr.save()
        cr.translate(cx, cy)
        cr.scale(w * 0.30, h * 0.42)
        cr.arc(0, 0, 1, math.pi * 0.35, math.pi * 2.15)
        cr.restore()
        cr.stroke()
        cr.move_to(cx + w * 0.02, cy - h * 0.10)
        cr.curve_to(
            cx + w * 0.20, cy - h * 0.05,
            cx + w * 0.18, cy + h * 0.20,
            cx - w * 0.02, cy + h * 0.22,
        )
        cr.stroke()

    def _draw_cognitive(self, cr, w, h):
        cx, cy = w / 2, h * 0.44
        r = w * 0.28
        cr.arc(cx, cy, r, math.pi * 1.05, math.pi * 2.55)
        cr.stroke()
        cr.move_to(cx + r * math.cos(math.pi * 2.55), cy + r * math.sin(math.pi * 2.55))
        cr.line_to(cx + w * 0.12, cy + h * 0.30)
        cr.line_to(cx - w * 0.20, cy + h * 0.30)
        cr.close_path()
        cr.stroke()
        for dx, dy, rr in ((-0.05, -0.06, 0.05), (0.10, -0.02, 0.04), (0.0, 0.10, 0.04)):
            cr.arc(cx + w * dx, cy + h * dy, w * rr, 0, 2 * math.pi)
            cr.stroke()
