"""Cairo redraw of macOS's "Transfer Your Data" glyph: two overlapping
rounded squares (a stack, implying "from one machine to another") with a
downward arrow on the front square - no matching icon exists in the
system's icon theme (checked breeze's actions/preferences sets), so this
follows the same approach as widgets.py's BackArrow: draw it directly
instead of shipping a new image asset."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class TransferIcon(Gtk.DrawingArea):
    def __init__(self, size=92):
        super().__init__()
        self._size = size
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        s = min(w, h) / 100.0

        def rounded_square(x, y, side, radius):
            cr.new_sub_path()
            cr.arc(x + side - radius, y + radius, radius, -1.5708, 0)
            cr.arc(x + side - radius, y + side - radius, radius, 0, 1.5708)
            cr.arc(x + radius, y + side - radius, radius, 1.5708, 3.14159)
            cr.arc(x + radius, y + radius, radius, 3.14159, 4.71239)
            cr.close_path()

        # Back square, offset down-right, slightly darker/translucent to
        # read as "behind" the front one.
        cr.set_source_rgba(0.0784, 0.4627, 0.9647, 0.55)  # #1476fa @ 55%
        rounded_square(24 * s, 24 * s, 62 * s, 14 * s)
        cr.fill()

        # Front square.
        cr.set_source_rgb(0.0784, 0.4627, 0.9647)  # #1476fa
        rounded_square(14 * s, 14 * s, 62 * s, 14 * s)
        cr.fill()

        # Downward arrow, white, centered on the front square.
        cx = (14 + 31) * s
        top = 26 * s
        bottom = 56 * s
        cr.set_source_rgb(1, 1, 1)
        cr.set_line_width(6 * s)
        cr.set_line_cap(1)  # round
        cr.set_line_join(1)  # round
        cr.move_to(cx, top)
        cr.line_to(cx, bottom)
        cr.stroke()
        head = 11 * s
        cr.move_to(cx - head, bottom - head)
        cr.line_to(cx, bottom)
        cr.line_to(cx + head, bottom - head)
        cr.stroke()
