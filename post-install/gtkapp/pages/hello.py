"""Port of app/hello.html: hand-drawn stroke animation of the pearOS
wordmark over the clean, untouched desktop wallpaper.

The wordmark itself is rendered as 'liquid glass': a GPU shader
(liquid_glass.LiquidGlassText) refracts + chromatically-aberrates the sharp
wallpaper directly behind each letter, restricted to the stroke shape — nothing
else on the page is touched. If the shader can't compile (old GTK, no GL
renderer, ...), this falls back to a flat semi-transparent stroke instead, so
the page always renders correctly either way.
"""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import background
from ..background import Background
from ..liquid_glass import LiquidGlassText
from ..svgpath import parse_path, path_to_cairo
from ..stroke_anim import AnimatedCanvas, ease_out_cubic

_D = (
    "M-293.58-104.62S-103.61-205.49-60-366.25c9.13-32.45,9-58.31,0-74-10.72-18.82-49.69-33.21-75.55,"
    "31.94-27.82,70.11-52.22,377.24-44.11,322.48s34-176.24,99.89-183.19c37.66-4,49.55,23.58,52.83,"
    "47.92a117.06,117.06,0,0,1-3,45.32c-7.17,27.28-20.47,97.67,33.51,96.86,66.93-1,131.91-53.89,"
    "159.55-84.49,31.1-36.17,31.1-70.64,19.27-90.25-16.74-29.92-69.47-33-92.79,16.73C62.78-179.86,"
    "98.7-93.8,159-81.63S302.7-99.55,393.3-269.92c29.86-58.16,52.85-114.71,46.14-150.08-7.44-39.21-"
    "59.74-54.5-92.87-8.7-47,65-61.78,266.62-34.74,308.53S416.62-58,481.52-130.31s133.2-188.56,"
    "146.54-256.23c14-71.15-56.94-94.64-88.4-47.32C500.53-375,467.58-229.49,503.3-127a73.73,73.73,0,"
    "0,0,23.43,33.67c25.49,20.23,55.1,16,77.46,6.32a111.25,111.25,0,0,0,30.44-19.87c37.73-34.23,"
    "29-36.71,64.58-127.53C724-284.3,785-298.63,821-259.13a71,71,0,0,1,13.69,22.56c17.68,46,6.81,80-"
    "6.81,107.89-12,24.62-34.56,42.72-61.45,47.91-23.06,4.45-48.37-.35-66.48-24.27a78.88,78.88,0,0,1-"
    "12.66-25.8c-14.75-51,4.14-88.76,11-101.41,6.18-11.39,37.26-69.61,103.42-42.24,55.71,23.05,"
    "100.66-23.31,100.66-23.31"
)
_OPS = parse_path(_D)
_TRANSLATE = (311.08, 476.02)
_VIEWBOX = (1230.94, 414.57)
_DASH_LEN = 5000.0
_DURATION_S = 4.0


def _flat_draw_frame(cr, w, h, t):
    """Fallback used only if the liquid-glass shader fails to compile."""
    scale = min(w / _VIEWBOX[0], h / _VIEWBOX[1]) * 0.9
    ox = (w - _VIEWBOX[0] * scale) / 2
    oy = (h - _VIEWBOX[1] * scale) / 2
    cr.save()
    cr.translate(ox, oy)
    cr.scale(scale, scale)
    cr.translate(*_TRANSLATE)
    path_to_cairo(cr, _OPS)
    cr.set_line_width(35)
    cr.set_line_cap(1)
    cr.set_line_join(1)
    offset = _DASH_LEN * (1.0 - t)
    cr.set_dash([_DASH_LEN, _DASH_LEN], offset)
    cr.set_source_rgba(1, 1, 1, 0.85)
    cr.stroke()
    cr.restore()


class HelloPage:
    def __init__(self, app):
        self.app = app
        self.bg = Background(sharp=True)

        self.column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.column.set_halign(Gtk.Align.CENTER)
        self.column.set_valign(Gtk.Align.CENTER)
        self.column.set_hexpand(True)
        self.column.set_vexpand(True)

        self.canvas = LiquidGlassText(
            _DURATION_S, _OPS, _DASH_LEN, _TRANSLATE, _VIEWBOX, ease_out_cubic
        )
        self.canvas.set_wallpaper(background.load_pixbuf())
        self.canvas.set_shader_result_callback(self._on_shader_result)
        self.canvas.set_size_request(900, 300)
        self.column.append(self.canvas)

        self.bg.add_overlay(self.column)

        # Pinned near the bottom of the screen on its own, rather than
        # packed into the same vertically-centered column as the wordmark
        # (the original Electron page centered both together instead) -
        # matches how every other page in the wizard anchors its Continue
        # button independently of the page's main content.
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
        # Shader unavailable on this system: swap in the flat fallback
        # canvas so the page still renders (Background stays untouched
        # either way — only the wordmark rendering changes).
        self.column.remove(self.canvas)
        fallback = AnimatedCanvas(_DURATION_S, _flat_draw_frame, easing=ease_out_cubic)
        fallback.set_content_width(900)
        fallback.set_content_height(300)
        self.column.prepend(fallback)
        fallback.start()
        self.canvas = fallback

    def _on_continue(self, _btn):
        self.bg.transition_to_blurred(0.8, on_complete=lambda: self.app.go_to("language"))
