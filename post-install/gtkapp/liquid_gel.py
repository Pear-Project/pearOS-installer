"""Real-time 'Liquid Gel' text: a GPU fragment shader (Gsk.GLShader) that
refracts the sharp wallpaper directly behind the letters, restricted to the
animated stroke, and lights it like a solid glass rod (directional
highlight on one side, shaded on the other — see Apple's macOS 26 'hello'
onboarding art and the physical acrylic sign it's modeled on).

Two masks are used, not one, which is the difference between this looking
like a crisp glass tube and looking like a soft neon glow (an earlier
version drove *opacity* off the same blurred field used for the lens
gradient, so the boundary itself faded out over many pixels instead of
being a clean edge):
- a *hard* mask (single stroke, no blur) decides exactly where the tube is
  — this is what the final alpha/coverage comes from, so the silhouette
  stays crisp no matter how strong the lens/lighting effect is.
- a *soft* mask (same stroke, blurred across roughly its own width) decides
  the lens/lighting gradient *inside* that silhouette — least distortion on
  the centerline, most near the rim, like a real round cross-section.

Requires GTK's legacy "gl" renderer (see __main__.py's GSK_RENDERER=gl) —
the newer default "ngl" renderer does not support Gsk.GLShader at all. If
shader compilation fails for any reason (old GTK, software rendering,
renderer forced back to ngl/vulkan by the environment, ...), pages/hello.py
falls back to a flat frosted look instead — this class never raises out of
do_snapshot().
"""
import cairo
import gi
import numpy as np

gi.require_version("Gtk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Graphene", "1.0")
from gi.repository import Gdk, GLib, Graphene, Gsk, Gtk

from .svgpath import path_to_cairo

_SHADER_SRC = b"""
uniform sampler2D u_texture1; // sharp wallpaper, pre-cropped to this widget's bounds
uniform sampler2D u_texture2; // HARD mask: crisp stroke coverage - decides
                               // the silhouette (final alpha), full stop.
uniform sampler2D u_texture3; // SOFT mask: same stroke, blurred - decides
                               // the lens/lighting gradient *inside* that
                               // silhouette, never the silhouette itself.
uniform float u_normal_pow;
uniform float u_refraction;
uniform float u_fringing;
uniform float u_specular;
uniform float u_shade;
uniform float u_frost; // blur radius, in pixels, applied to the refracted
                        // wallpaper sample - frosted glass, not a clear pane

vec3 frostedSample(sampler2D tex, vec2 center, vec2 texel) {
    // Two rings (half and full radius) x 8 directions: a 5-tap blur at a
    // large radius just looks like 4 faint ghosts, not frosted glass - this
    // is closer to a real soft-focus average.
    vec3 sum = GskTexture(tex, center).rgb * 4.0;
    for (int ring = 1; ring <= 2; ring++) {
        float rr = u_frost * (float(ring) / 2.0);
        for (int i = 0; i < 8; i++) {
            float a = float(i) * 0.7853981634; // pi/4
            vec2 off = vec2(cos(a), sin(a)) * rr * texel;
            sum += GskTexture(tex, center + off).rgb;
        }
    }
    return sum / 20.0;
}

void mainImage(out vec4 fragColor,
               in vec2 fragCoord,
               in vec2 resolution,
               in vec2 uv) {
    float hardCoverage = GskTexture(u_texture2, uv).a;
    if (hardCoverage < 0.02) {
        fragColor = vec4(0.0);
        return;
    }

    vec2 texel = 1.0 / resolution;
    float sC = GskTexture(u_texture3, uv).a;
    float sL = GskTexture(u_texture3, uv - vec2(texel.x, 0.0)).a;
    float sR = GskTexture(u_texture3, uv + vec2(texel.x, 0.0)).a;
    float sT = GskTexture(u_texture3, uv - vec2(0.0, texel.y)).a;
    float sB = GskTexture(u_texture3, uv + vec2(0.0, texel.y)).a;
    vec2 grad = vec2(sR - sL, sB - sT);
    float gradLen = length(grad);
    vec2 normal = grad / max(gradLen, 1e-4);
    // Right on the centerline the coverage field is at a flat maximum, so
    // its gradient (and therefore 'normal') is near-zero and numerically
    // unstable - normalizing noise there flips direction pixel to pixel and
    // shows up as a spurious bright seam down the middle of the tube.
    // Fading every normal-dependent effect out smoothly as gradLen -> 0
    // (instead of a hard branch) kills that seam instead of just hiding it.
    float normalConfidence = smoothstep(0.0, 0.04, gradLen);

    // A round glass rod bends light across its *entire* width, not just at
    // its silhouette: least in the middle (looking straight through), most
    // near the rim (grazing angle).
    float lens = pow(1.0 - sC, u_normal_pow) * normalConfidence;

    // u_refraction is a *pixel* displacement at the rim (lens == 1),
    // converted to uv space via texel so it stays sane regardless of the
    // canvas' size.
    float strengthPixels = lens * u_refraction;
    vec2 refractOffsetR = normal * (strengthPixels * (1.0 + u_fringing)) * texel;
    vec2 refractOffsetG = normal * strengthPixels * texel;
    vec2 refractOffsetB = normal * (strengthPixels * (1.0 - u_fringing)) * texel;

    float r = frostedSample(u_texture1, uv - refractOffsetR, texel).r;
    float g = frostedSample(u_texture1, uv - refractOffsetG, texel).g;
    float b = frostedSample(u_texture1, uv - refractOffsetB, texel).b;
    vec3 color = vec3(r, g, b);

    // Directional lighting, like a real glass rod lit from above. One
    // *continuous* gradient (smoothstep of N.L, not a high pow() term) run
    // the whole way around the curve, from dark on the shadowed side to
    // bright on the lit side - a high pow() here only lights up the handful
    // of points where the tangent happens to line up with the light,
    // leaving patchy, disconnected glints instead of a smooth glossy rim.
    vec2 lightDir = normalize(vec2(-0.35, -1.0));
    float NdotL = dot(normal, lightDir);
    float smoothLight = smoothstep(-1.0, 1.0, NdotL);
    float brightnessMul = mix(1.0, mix(u_shade, 1.0 + u_specular, smoothLight), lens);
    color = min(color * brightnessMul, vec3(1.0));

    // hardCoverage (not sC) drives the final alpha: a crisp silhouette
    // regardless of how soft the internal lighting gradient is.
    fragColor = vec4(color, hardCoverage) * hardCoverage;
}
"""


def _surface_to_texture(surface):
    w, h = surface.get_width(), surface.get_height()
    pixbuf = Gdk.pixbuf_get_from_surface(surface, 0, 0, w, h)
    return Gdk.Texture.new_for_pixbuf(pixbuf)


def _box_blur_1d(a, radius, axis):
    """Box blur via cumulative sum (edge-replicated), one axis at a time."""
    r = max(1, int(radius))
    pad_width = [(0, 0)] * a.ndim
    pad_width[axis] = (r, r)
    padded = np.pad(a, pad_width, mode="edge")
    csum = np.cumsum(padded, axis=axis, dtype=np.float32)
    zero_shape = list(csum.shape)
    zero_shape[axis] = 1
    csum = np.concatenate([np.zeros(zero_shape, dtype=np.float32), csum], axis=axis)
    window = 2 * r + 1
    n = a.shape[axis]
    hi = np.take(csum, np.arange(window, window + n), axis=axis)
    lo = np.take(csum, np.arange(0, n), axis=axis)
    return (hi - lo) / window


def _soften(surface, radius_px):
    """Blur an ARGB32 surface at full resolution, all 4 channels together
    (three box-blur passes, a cheap near-Gaussian)."""
    surface.flush()
    w, h = surface.get_width(), surface.get_height()
    stride = surface.get_stride()
    buf = surface.get_data()
    view = np.ndarray(shape=(h, stride // 4, 4), dtype=np.uint8, buffer=buf)
    arr = view[:, :w, :].astype(np.float32)

    for _ in range(3):
        arr = _box_blur_1d(arr, radius_px, axis=1)
        arr = _box_blur_1d(arr, radius_px, axis=0)

    view[:, :w, :] = np.clip(arr, 0, 255).astype(np.uint8)
    surface.mark_dirty()


def _ops_bbox(ops):
    xs, ys = [], []
    for op in ops:
        coords = op[1:]
        for i in range(0, len(coords), 2):
            xs.append(coords[i])
            ys.append(coords[i + 1])
    return min(xs), max(xs), min(ys), max(ys)


class LiquidGelText(Gtk.Widget):
    """duration_s/mask_ops/dash_len/translate/viewbox describe the animated
    stroke exactly like stroke_anim.AnimatedCanvas + svgpath — see
    pages/hello.py for how the path is built.

    zoom_start_ops: if set, the camera opens zoomed in on just the bounding
    box of mask_ops[:zoom_start_ops] (e.g. the first letter's worth of path
    commands) and eases out to the normal full-word framing over the first
    zoom_fraction of the animation - a "focus on the first letter, then pull
    back" opening shot, on top of the existing stroke-writing reveal (which
    keeps running the whole duration_s, unaffected by this)."""

    def __init__(
        self, duration_s, mask_ops, dash_len, translate, viewbox, easing,
        zoom_start_ops=None, zoom_factor=2.2, zoom_fraction=0.35,
    ):
        super().__init__()
        self._duration = duration_s
        self._ops = mask_ops
        self._dash_len = dash_len
        self._translate = translate
        self._viewbox = viewbox
        self._easing = easing
        self._progress = 0.0
        self._cam_t = 1.0
        self._zoom_factor = zoom_factor
        self._zoom_fraction = max(1e-3, zoom_fraction)
        self._open_bbox = _ops_bbox(mask_ops[:zoom_start_ops]) if zoom_start_ops else None
        self._start_us = None
        self._shader = None
        self._shader_ok = None  # None = untried, True/False after first attempt
        self._wallpaper_pixbuf = None
        self._on_shader_result = None
        self._crop_cache_key = None
        self._crop_cache_texture = None

    def set_wallpaper(self, pixbuf):
        self._wallpaper_pixbuf = pixbuf

    def set_shader_result_callback(self, callback):
        """callback(bool) is invoked once, the first time we know whether the
        shader compiled — pages/hello.py uses it to decide whether to keep
        this widget or swap in the flat-frosted fallback drawing instead."""
        self._on_shader_result = callback

    def start(self):
        self._start_us = None
        self.add_tick_callback(self._tick)

    def _tick(self, widget, frame_clock):
        now = frame_clock.get_frame_time()
        if self._start_us is None:
            self._start_us = now
        elapsed = (now - self._start_us) / 1_000_000.0
        raw = min(1.0, elapsed / self._duration) if self._duration > 0 else 1.0
        self._progress = self._easing(raw)
        if self._open_bbox is not None:
            cam_raw = min(1.0, elapsed / (self._duration * self._zoom_fraction))
            self._cam_t = self._easing(cam_raw)
        widget.queue_draw()
        return raw < 1.0

    def _ensure_shader(self):
        if self._shader_ok is not None:
            return self._shader_ok
        native = self.get_native()
        if native is None:
            return False
        renderer = native.get_renderer()
        self._shader = Gsk.GLShader.new_from_bytes(GLib.Bytes.new(_SHADER_SRC))
        try:
            self._shader.compile(renderer)
            self._shader_ok = True
        except GLib.Error:
            self._shader_ok = False
        if self._on_shader_result:
            self._on_shader_result(self._shader_ok)
            self._on_shader_result = None
        return self._shader_ok

    def _cropped_wallpaper_texture(self, w, h):
        if self._wallpaper_pixbuf is None:
            return None

        window = self.get_root()
        win_w = window.get_width() if window else w
        win_h = window.get_height() if window else h
        result = self.translate_coordinates(window, 0, 0) if window else None
        cx, cy = result if result else (0, 0)

        # Cached, but keyed on the actual geometry: on first paint the
        # window may still be at its pre-fullscreen natural size
        # (fullscreen() is requested via idle_add in __main__.py, one tick
        # after present()), so caching unconditionally on the very first
        # call would freeze in a wrong, tiny-window crop forever. Keying on
        # (win_w, win_h, cx, cy, w, h) instead means it recomputes for as
        # long as the geometry is actually still settling, then reuses the
        # same texture for the rest of the ~4s reveal instead of re-doing a
        # full cairo paint + texture upload on every single frame - this
        # (plus _surface_to_texture()'s MemoryTexture switch) is most of
        # what was keeping this well under 60fps.
        key = (round(win_w), round(win_h), round(cx), round(cy), w, h)
        if key == self._crop_cache_key:
            return self._crop_cache_texture

        iw, ih = self._wallpaper_pixbuf.get_width(), self._wallpaper_pixbuf.get_height()
        scale = max(win_w / iw, win_h / ih)
        offset_x = (win_w - iw * scale) / 2.0
        offset_y = (win_h - ih * scale) / 2.0

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max(1, int(w)), max(1, int(h)))
        cr = cairo.Context(surface)
        cr.set_matrix(cairo.Matrix(xx=scale, yy=scale, x0=offset_x - cx, y0=offset_y - cy))
        Gdk.cairo_set_source_pixbuf(cr, self._wallpaper_pixbuf, 0, 0)
        # PAD instead of the default NONE: if the alignment is off by a
        # pixel or two at the very edge, clamp to the nearest wallpaper
        # pixel instead of sampling fully-transparent black — a mismatched
        # crop should look slightly wrong, never make the letters vanish.
        cr.get_source().set_extend(cairo.Extend.PAD)
        cr.paint()

        self._crop_cache_key = key
        self._crop_cache_texture = _surface_to_texture(surface)
        return self._crop_cache_texture

    def _fit_transform(self, w, h):
        """scale/offset that centers the whole word in (w, h) with a 10%
        margin - shared by the mask drawing and the opening zoom-in, so the
        two always agree on where things land."""
        scale = min(w / self._viewbox[0], h / self._viewbox[1]) * 0.9
        ox = (w - self._viewbox[0] * scale) / 2
        oy = (h - self._viewbox[1] * scale) / 2
        return scale, ox, oy

    def _camera(self, w, h):
        """Returns (zoom, focus_x, focus_y) in widget-pixel space for the
        opening zoom-in/pull-back. zoom == 1.0 (the fully-pulled-back,
        no-op case) once _cam_t reaches 1 or there's no configured opening
        region."""
        if self._open_bbox is None or self._cam_t >= 1.0:
            return 1.0, 0.0, 0.0
        scale, ox, oy = self._fit_transform(w, h)
        x0, x1, y0, y1 = self._open_bbox
        cx = (x0 + x1) / 2.0 + self._translate[0]
        cy = (y0 + y1) / 2.0 + self._translate[1]
        focus_x = ox + scale * cx
        focus_y = oy + scale * cy
        zoom = self._zoom_factor + (1.0 - self._zoom_factor) * self._cam_t
        return zoom, focus_x, focus_y

    def _stroke_path(self, cr, w, h):
        scale, ox, oy = self._fit_transform(w, h)
        cr.translate(ox, oy)
        cr.scale(scale, scale)
        cr.translate(*self._translate)
        path_to_cairo(cr, self._ops)
        cr.set_line_width(35)
        cr.set_line_cap(1)
        cr.set_line_join(1)
        offset = self._dash_len * (1.0 - self._progress)
        cr.set_dash([self._dash_len, self._dash_len], offset)
        cr.set_source_rgba(1, 1, 1, 1)
        cr.stroke()

    def _mask_textures(self, w, h):
        """Returns (hard, soft) textures - see the module docstring for why
        two are needed instead of one."""
        hard_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max(1, int(w)), max(1, int(h)))
        self._stroke_path(cairo.Context(hard_surface), w, h)

        soft_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, max(1, int(w)), max(1, int(h)))
        self._stroke_path(cairo.Context(soft_surface), w, h)
        # ~1/5 of the 35px stroke width: enough that the whole cross-section
        # reads as a rounded tube (per the reference photos - a solid glass
        # rod, not a flat panel with a thin bevel), without merging nearby
        # strands where cursive loops run close together (radius_px=14,
        # tried earlier, did exactly that and blobbed the letters).
        _soften(soft_surface, radius_px=7.0)

        return _surface_to_texture(hard_surface), _surface_to_texture(soft_surface)

    def do_snapshot(self, snapshot):
        w, h = self.get_width(), self.get_height()
        if w <= 0 or h <= 0:
            return
        bounds = Graphene.Rect()
        bounds.init(0, 0, w, h)

        if not self._ensure_shader():
            return

        tex1 = self._cropped_wallpaper_texture(w, h)
        if tex1 is None:
            return
        tex2, tex3 = self._mask_textures(w, h)

        builder = Gsk.ShaderArgsBuilder.new(self._shader, None)
        builder.set_float(0, 1.0)  # normal_pow - lower = distortion spread
                                     # across more of the tube, not just a
                                     # thin rim, so bent background is
                                     # actually visible, not just tinted
        builder.set_float(1, 46.0)  # refraction strength, in pixels at the rim
        builder.set_float(2, 0.15)  # RGB fringing (subtle - reference photos are
                                     # tinted by the background, not rainbowy)
        builder.set_float(3, 0.7)  # brightness boost on the lit side of the smooth gradient
        builder.set_float(4, 0.55)  # shade factor on the far side from the light
        builder.set_float(5, 26.0)  # frost blur radius, in pixels
        args = builder.to_args()

        # Opening zoom-in/pull-back: an outer scale+translate around the
        # shader node, centered on the opening letter's focus point. The
        # shader itself keeps rendering in the same (0, 0, w, h) local space
        # either way - it has no idea it's being magnified, so none of its
        # texel/refraction math needs to change for this.
        zoom, focus_x, focus_y = self._camera(w, h)
        zoomed = zoom != 1.0
        if zoomed:
            snapshot.save()
            snapshot.translate(Graphene.Point().init(focus_x * (1.0 - zoom), focus_y * (1.0 - zoom)))
            snapshot.scale(zoom, zoom)

        try:
            snapshot.push_gl_shader(self._shader, bounds, args)
            for tex in (tex1, tex2, tex3):
                snapshot.append_texture(tex, bounds)
                snapshot.gl_shader_pop_texture()
            snapshot.pop()
        except GLib.Error:
            self._shader_ok = False

        if zoomed:
            snapshot.restore()
