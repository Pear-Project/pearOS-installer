import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import background
from ..background import Background
from ..liquid_gel import LiquidGelText
from ..svgpath import parse_path, path_to_cairo
from ..stroke_anim import AnimatedCanvas, ease_out_cubic, path_length

with open(os.path.join(os.path.dirname(__file__), "welcome_path.txt")) as _f:
    _D = _f.read()
_OPS = parse_path(_D)


def _ops_bbox(ops):
    xs, ys = [], []
    for op in ops:
        coords = op[1:]
        for i in range(0, len(coords), 2):
            xs.append(coords[i])
            ys.append(coords[i + 1])
    return min(xs), max(xs), min(ys), max(ys)


_X0, _X1, _Y0, _Y1 = _ops_bbox(_OPS)
_TRANSLATE = (-_X0, -_Y0)
_VIEWBOX = (_X1 - _X0, _Y1 - _Y0)
_LINE_WIDTH = 2.8
_DASH_LEN = path_length(_OPS) + 100.0
_DURATION_S = 4.0


def _flat_draw_frame(cr, w, h, t):
    scale = min(w / _VIEWBOX[0], h / _VIEWBOX[1]) * 0.9
    ox = (w - _VIEWBOX[0] * scale) / 2
    oy = (h - _VIEWBOX[1] * scale) / 2
    cr.save()
    cr.translate(ox, oy)
    cr.scale(scale, scale)
    cr.translate(*_TRANSLATE)
    path_to_cairo(cr, _OPS)
    cr.set_line_width(_LINE_WIDTH)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    offset = _DASH_LEN * (1.0 - t)
    cr.set_dash([_DASH_LEN, _DASH_LEN], offset)
    cr.set_source_rgba(1, 1, 1, 0.85)
    cr.stroke()
    cr.restore()


class WelcomePage:
    def __init__(self, app):
        self.app = app
        self.bg = Background(sharp=True)

        self.column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.column.set_halign(Gtk.Align.CENTER)
        self.column.set_valign(Gtk.Align.CENTER)
        self.column.set_hexpand(True)
        self.column.set_vexpand(True)

        self.canvas = LiquidGelText(
            _DURATION_S, _OPS, _DASH_LEN, _TRANSLATE, _VIEWBOX, ease_out_cubic,
            line_width=_LINE_WIDTH,
        )
        self.canvas.set_wallpaper(background.load_pixbuf())
        self.canvas.set_shader_result_callback(self._on_shader_result)
        self.canvas.set_size_request(900, 300)
        self.column.append(self.canvas)

        self.bg.add_overlay(self.column)

        continue_btn = Gtk.Button(label="Continue")
        continue_btn.add_css_class("nav-button")
        continue_btn.set_halign(Gtk.Align.CENTER)
        continue_btn.set_valign(Gtk.Align.END)
        continue_btn.set_margin_bottom(48)
        continue_btn.connect("clicked", self._on_continue)
        self.bg.add_overlay(continue_btn)

        self.widget = self.bg

    def on_show(self):
        self.canvas.start()

    def _on_shader_result(self, ok):
        if ok:
            return
        self.column.remove(self.canvas)
        fallback = AnimatedCanvas(_DURATION_S, _flat_draw_frame, easing=ease_out_cubic)
        fallback.set_content_width(900)
        fallback.set_content_height(300)
        self.column.prepend(fallback)
        fallback.start()
        self.canvas = fallback

    def _on_continue(self, _btn):
        self.bg.transition_to_blurred(0.8, on_complete=lambda: self.app.go_to("finish"))
