"""Shared wallpaper background: the blurred/dimmed backdrop behind every page
(body::before/::after + .hello-page/.welcome-page/.blur-transition rules in
assistant-styles.css). Uses the wallpaper resolved by wallpaper.find_wallpaper().
"""
import gi
import numpy as np

gi.require_version("Gtk", "4.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, GLib, Gdk

from . import wallpaper

# Downscale before blurring (a 4000px+ wallpaper doesn't need to be blurred
# at full resolution - the result is smoothed out either way), but only
# moderately: Gtk.Picture's own COVER scaling handles the rest at render
# time with proper (GPU) filtering. A much more aggressive downscale here
# used to be paired with a *second* GdkPixbuf.scale_simple() back up to full
# size - at that kind of extreme scale factor (~20x), bilinear upscaling
# stops looking like blur and starts looking like visible blocks, which is
# what made this pixelated.
_BLUR_MAX_DIMENSION = 640
_BLUR_RADIUS_PX = 10


def load_pixbuf():
    """Load the current wallpaper (see wallpaper.find_wallpaper()). Exposed
    publicly so pages/hello.py can paint the exact same image the letters
    should sample a blurred patch of."""
    path = wallpaper.find_wallpaper()
    try:
        return GdkPixbuf.Pixbuf.new_from_file(path)
    except GLib.Error:
        return GdkPixbuf.Pixbuf.new_from_file(wallpaper.DEFAULT_WALLPAPER)


def _box_blur_1d(a, radius, axis):
    r = max(1, int(radius))
    n = a.shape[axis]
    pad_width = [(0, 0)] * a.ndim
    pad_width[axis] = (r, r)
    padded = np.pad(a, pad_width, mode="edge")
    csum = np.cumsum(padded, axis=axis, dtype=np.float32)
    window = 2 * r + 1

    sl_hi = [slice(None)] * a.ndim
    sl_hi[axis] = slice(window - 1, window - 1 + n)
    hi = csum[tuple(sl_hi)]

    lo = np.zeros_like(hi)
    if n > 1:
        sl_lo_dst = [slice(None)] * a.ndim
        sl_lo_dst[axis] = slice(1, n)
        sl_lo_src = [slice(None)] * a.ndim
        sl_lo_src[axis] = slice(0, n - 1)
        lo[tuple(sl_lo_dst)] = csum[tuple(sl_lo_src)]

    return (hi - lo) / window


def make_blurred(pixbuf):
    w, h = pixbuf.get_width(), pixbuf.get_height()
    scale = min(1.0, _BLUR_MAX_DIMENSION / max(w, h))
    sw, sh = max(1, int(w * scale)), max(1, int(h * scale))
    small = pixbuf.scale_simple(sw, sh, GdkPixbuf.InterpType.BILINEAR)

    channels = small.get_n_channels()
    arr = np.frombuffer(small.get_pixels(), dtype=np.uint8)
    arr = arr.reshape(sh, small.get_rowstride())[:, : sw * channels]
    arr = arr.reshape(sh, sw, channels).astype(np.float32)

    radius = max(1, int(_BLUR_RADIUS_PX * scale))
    for _ in range(3):
        arr = _box_blur_1d(arr, radius, axis=1)
        arr = _box_blur_1d(arr, radius, axis=0)

    out = np.clip(arr, 0, 255).astype(np.uint8)
    return GdkPixbuf.Pixbuf.new_from_bytes(
        GLib.Bytes.new(out.tobytes()),
        GdkPixbuf.Colorspace.RGB,
        small.get_has_alpha(),
        8,
        sw,
        sh,
        sw * channels,
    )


class Background(Gtk.Overlay):
    """sharp=True reproduces .hello-page/.welcome-page (blur 0, dim 0.1);
    sharp=False (default) reproduces the normal wizard pages (blur 8px, dim 0.3)."""

    def __init__(self, sharp=False):
        super().__init__()
        self._pixbuf = load_pixbuf()
        self._blurred_pixbuf = make_blurred(self._pixbuf)

        self.sharp_picture = Gtk.Picture.new_for_pixbuf(self._pixbuf)
        self.sharp_picture.set_content_fit(Gtk.ContentFit.COVER)
        self.sharp_picture.set_can_shrink(True)
        self.sharp_picture.set_hexpand(True)
        self.sharp_picture.set_vexpand(True)

        self.blurred_picture = Gtk.Picture.new_for_pixbuf(self._blurred_pixbuf)
        self.blurred_picture.set_content_fit(Gtk.ContentFit.COVER)
        self.blurred_picture.set_can_shrink(True)
        self.blurred_picture.set_hexpand(True)
        self.blurred_picture.set_vexpand(True)

        self.dim = Gtk.Box()
        self.dim.set_hexpand(True)
        self.dim.set_vexpand(True)

        self.set_child(self.sharp_picture)
        self.add_overlay(self.blurred_picture)
        self.add_overlay(self.dim)

        self._dim_provider = Gtk.CssProvider()
        self.dim.get_style_context().add_provider(
            self._dim_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self._blur_opacity = 0.0 if sharp else 1.0
        self._dim_alpha = 0.1 if sharp else 0.3
        self.blurred_picture.set_opacity(self._blur_opacity)
        self._apply_dim(self._dim_alpha)

    def _apply_dim(self, alpha):
        css = ("box { background-color: rgba(0,0,0,%.3f); }" % alpha).encode()
        self._dim_provider.load_from_data(css)

    def transition_to_blurred(self, duration_s=0.8, on_complete=None):
        """Animate blur-in + darken, matching .blur-transition (0.8s ease-in-out)."""
        start_blur = self._blur_opacity
        start_dim = self._dim_alpha
        target_blur, target_dim = 1.0, 0.3
        start_time = GLib.get_monotonic_time()

        def tick(widget, frame_clock):
            now = frame_clock.get_frame_time()
            t = min(1.0, (now - start_time) / 1_000_000.0 / duration_s)
            eased = 1 - pow(1 - t, 3)
            self.blurred_picture.set_opacity(start_blur + (target_blur - start_blur) * eased)
            self._apply_dim(start_dim + (target_dim - start_dim) * eased)
            if t >= 1.0:
                self._blur_opacity, self._dim_alpha = target_blur, target_dim
                if on_complete:
                    on_complete()
                return False
            return True

        self.add_tick_callback(tick)
