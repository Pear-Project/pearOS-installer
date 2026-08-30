"""Cairo redraws of the four small glyphs on macOS's real Screen Time
setup screen (Weekly Reports / Downtime and App Limits / Content & Privacy
Restrictions / Screen Time Passcode) - no matching icons in the system's
icon theme, so drawn directly like the other custom glyphs in this
package (migration_icon.py, privacy_icon.py, etc). All share the same
outline weight/blue as those."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_BLUE = (0.0784, 0.4627, 0.9647)  # #1476fa


class HourglassIcon(Gtk.DrawingArea):
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

        top, bottom, left, right, mid = 4 * s, 20 * s, 6 * s, 18 * s, 12 * s
        # top bar
        cr.move_to(left, top)
        cr.line_to(right, top)
        cr.stroke()
        # bottom bar
        cr.move_to(left, bottom)
        cr.line_to(right, bottom)
        cr.stroke()
        # bowtie outline
        cr.move_to(left, top)
        cr.line_to(right, top)
        cr.line_to(mid, mid)
        cr.line_to(right, bottom)
        cr.line_to(left, bottom)
        cr.line_to(mid, mid)
        cr.close_path()
        cr.stroke()
        # sand in the top triangle
        cr.new_sub_path()
        cr.move_to(left + 2.6 * s, top + 2.4 * s)
        cr.line_to(right - 2.6 * s, top + 2.4 * s)
        cr.line_to(mid, mid - 0.6 * s)
        cr.close_path()
        cr.fill()


class ClockIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2.0 - 1.2
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.6)
        cr.set_line_cap(1)
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.stroke()
        cr.move_to(cx, cy)
        cr.line_to(cx, cy - r * 0.55)
        cr.stroke()
        cr.move_to(cx, cy)
        cr.line_to(cx + r * 0.4, cy + r * 0.15)
        cr.stroke()


class NoEntryIcon(Gtk.DrawingArea):
    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2.0 - 1.2
        cr.set_source_rgb(*_BLUE)
        cr.set_line_width(1.6)
        cr.set_line_cap(1)
        cr.arc(cx, cy, r, 0, 6.2832)
        cr.stroke()
        d = r * 0.72
        cr.move_to(cx - d, cy - d)
        cr.line_to(cx + d, cy + d)
        cr.stroke()


class PasscodeGridIcon(Gtk.DrawingArea):
    """A 4x3 grid of filled dots, matching the reference's Screen Time
    Passcode glyph."""

    def __init__(self, size=24):
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 24.0
        cr.set_source_rgb(*_BLUE)
        r = 1.5 * s
        cols = (5 * s, 12 * s, 19 * s)
        rows = (5 * s, 12 * s, 19 * s)
        for y in rows:
            for x in cols:
                cr.arc(x, y, r, 0, 6.2832)
                cr.fill()
