"""Cairo redraw of macOS's real "Choose Your Look" preview tiles: a tiny
window mockup (traffic-light dots, sidebar + content pane) sitting on a
soft gradient backdrop, with a small dock strip along the bottom edge.
"Auto" draws two overlapping windows (light behind, dark in front) to
represent both appearances at once - no matching asset exists in the
system icon theme, so drawn directly like the other custom glyphs in
this package."""
import cairo
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

_LIGHT_BG = (0.937, 0.945, 0.965)
_LIGHT_BG2 = (0.812, 0.847, 0.902)
_DARK_BG = (0.169, 0.184, 0.220)
_DARK_BG2 = (0.082, 0.090, 0.110)

_DOTS = ((0.996, 0.373, 0.341), (0.996, 0.741, 0.204), (0.204, 0.780, 0.349))


def _rounded_rect(cr, x, y, w, h, r):
    cr.new_sub_path()
    cr.arc(x + w - r, y + r, r, -1.5708, 0)
    cr.arc(x + w - r, y + h - r, r, 0, 1.5708)
    cr.arc(x + r, y + h - r, r, 1.5708, 3.14159)
    cr.arc(x + r, y + r, r, 3.14159, 4.71239)
    cr.close_path()


def _draw_window(cr, x, y, w, h, dark, dot_scale=1.0):
    titlebar_h = h * 0.22
    if dark:
        titlebar = (0.235, 0.251, 0.294)
        body = (0.106, 0.114, 0.137)
        sidebar = (0.161, 0.173, 0.204)
    else:
        titlebar = (0.929, 0.937, 0.949)
        body = (1.0, 1.0, 1.0)
        sidebar = (0.847, 0.867, 0.898)

    _rounded_rect(cr, x, y, w, h, h * 0.09)
    cr.set_source_rgb(*body)
    cr.fill_preserve()
    cr.clip()

    cr.rectangle(x, y, w, titlebar_h)
    cr.set_source_rgb(*titlebar)
    cr.fill()

    r = titlebar_h * 0.22 * dot_scale
    cx = x + titlebar_h * 0.45
    cy = y + titlebar_h / 2
    for i, color in enumerate(_DOTS):
        cr.set_source_rgb(*color)
        cr.arc(cx + i * r * 2.6, cy, r, 0, 6.2832)
        cr.fill()

    sidebar_w = w * 0.32
    cr.rectangle(x, y + titlebar_h, sidebar_w, h - titlebar_h)
    cr.set_source_rgb(*sidebar)
    cr.fill()

    cr.reset_clip()


class LookPreview(Gtk.DrawingArea):
    def __init__(self, mode, width=160, height=100):
        super().__init__()
        self.mode = mode
        self.set_content_width(width)
        self.set_content_height(height)
        self.set_draw_func(self._draw)

    def _draw(self, _area, cr, w, h):
        _rounded_rect(cr, 0, 0, w, h, h * 0.08)
        cr.clip()

        if self.mode == "dark":
            grad_a, grad_b = _DARK_BG, _DARK_BG2
        else:
            grad_a, grad_b = _LIGHT_BG, _LIGHT_BG2

        grad = cairo.LinearGradient(0, 0, w, h)
        grad.add_color_stop_rgb(0.0, *grad_a)
        grad.add_color_stop_rgb(1.0, *grad_b)
        cr.set_source(grad)
        cr.rectangle(0, 0, w, h)
        cr.fill()

        dock_h = h * 0.15
        win_top = h * 0.06
        win_bottom = h - dock_h - h * 0.03

        if self.mode == "auto":
            win_w = w * 0.58
            _draw_window(cr, w * 0.04, win_top, win_w, win_bottom - win_top, False, 0.85)
            win_w2 = w * 0.6
            _draw_window(
                cr, w - win_w2 - w * 0.04, win_top + h * 0.05, win_w2,
                win_bottom - win_top - h * 0.03, True, 0.85,
            )
        else:
            _draw_window(
                cr, w * 0.06, win_top, w * 0.88, win_bottom - win_top,
                self.mode == "dark",
            )

        # Dock strip.
        dock_w = w * 0.7
        dock_x = (w - dock_w) / 2
        dock_y = h - dock_h - h * 0.02
        _rounded_rect(cr, dock_x, dock_y, dock_w, dock_h, dock_h * 0.3)
        cr.set_source_rgba(1, 1, 1, 0.55 if self.mode != "dark" else 0.18)
        cr.fill()

        n_icons = 6
        pad = dock_h * 0.16
        icon_size = dock_h - pad * 2
        gap = (dock_w - pad * 2 - n_icons * icon_size) / (n_icons - 1)
        ix = dock_x + pad
        for i in range(n_icons):
            _rounded_rect(cr, ix, dock_y + pad, icon_size, icon_size, icon_size * 0.28)
            cr.set_source_rgba(0.4, 0.55, 0.75, 0.65)
            cr.fill()
            ix += icon_size + gap
