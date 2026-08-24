"""Port of templates/finish.html + app/aa/{script.js,style.css} + the
commit()/run-post-setup handling from engine.js and main.js."""
import math
import os
import re
import tempfile
import threading

import cairo
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Gtk, Pango, PangoCairo, GLib

from .. import log_upload
from .. import state as state_mod
from ..background import Background

WORD = "welcome"
CANVAS_W, CANVAS_H = 1100, 420
FONT_SIZE = 220

RAINBOW_STOPS = [
    (0.0, (0xFF, 0x3B, 0x30)),
    (0.2, (0xFF, 0x95, 0x00)),
    (0.4, (0xFF, 0xCC, 0x00)),
    (0.6, (0x34, 0xC7, 0x59)),
    (0.8, (0x00, 0x7A, 0xFF)),
    (1.0, (0xAF, 0x52, 0xDE)),
]

ORB_1 = (150, 150, (0x93, 0xC5, 0xFD), 0.35)  # top-left, blue-300
ORB_2 = (CANVAS_W - 150, CANVAS_H - 100, (0xD8, 0xB4, 0xFE), 0.35)  # bottom-right, purple-300


def _flat_path_length(flat_path):
    length = 0.0
    cur = None
    start = None
    for ptype, points in flat_path:
        if ptype == cairo.PATH_MOVE_TO:
            cur = points
            start = points
        elif ptype == cairo.PATH_LINE_TO:
            nxt = points
            if cur is not None:
                length += math.hypot(nxt[0] - cur[0], nxt[1] - cur[1])
            cur = nxt
        elif ptype == cairo.PATH_CLOSE_PATH:
            if cur is not None and start is not None:
                length += math.hypot(start[0] - cur[0], start[1] - cur[1])
            cur = start
    return length


def _rainbow_gradient(x0, x1, alpha=1.0):
    grad = cairo.LinearGradient(x0, 0, x1, 0)
    for offset, (r, g, b) in RAINBOW_STOPS:
        grad.add_color_stop_rgba(offset, r / 255.0, g / 255.0, b / 255.0, alpha)
    return grad


def _draw_orb(cr, cx, cy, color, alpha):
    r, g, b = color
    radius = 200
    grad = cairo.RadialGradient(cx, cy, 0, cx, cy, radius)
    grad.add_color_stop_rgba(0.0, r / 255.0, g / 255.0, b / 255.0, alpha)
    grad.add_color_stop_rgba(0.6, r / 255.0, g / 255.0, b / 255.0, alpha * 0.4)
    grad.add_color_stop_rgba(1.0, r / 255.0, g / 255.0, b / 255.0, 0.0)
    cr.save()
    cr.set_source(grad)
    cr.arc(cx, cy, radius, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


class WelcomeCanvas(Gtk.DrawingArea):
    """Reproduces aa/script.js's resetAnimation() + aa/style.css's
    drawStroke/fillFade keyframes: the word strokes in over `duration`
    seconds (ease-in-out), then the rainbow fill fades in over 2s starting
    at 85% of the stroke duration, while the stroke width shrinks to 0."""

    def __init__(self):
        super().__init__()
        self.set_content_width(CANVAS_W)
        self.set_content_height(CANVAS_H)
        self.set_draw_func(self._on_draw)
        self._start_time = None

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1, 1)
        cr = cairo.Context(surface)
        layout = PangoCairo.create_layout(cr)
        layout.set_font_description(Pango.FontDescription("Borel %d" % FONT_SIZE))
        layout.set_text(WORD, -1)
        lw, lh = layout.get_pixel_size()
        cr.new_path()
        PangoCairo.layout_path(cr, layout)
        self._flat_path = cr.copy_path_flat()
        self._total_length = max(1.0, _flat_path_length(self._flat_path))
        self._text_w, self._text_h = lw, lh
        self._tx = (CANVAS_W - lw) / 2.0
        self._ty = (CANVAS_H - lh) / 2.0

        buffer_len = 50.0
        writing_speed = 150.0
        self._duration = max(2.5, min(8.0, (self._total_length + buffer_len) / writing_speed))
        self._fill_delay = self._duration * 0.85
        self._fill_duration = 2.0

    def start(self):
        self._start_time = None
        self.add_tick_callback(self._tick)

    def _tick(self, widget, frame_clock):
        now = frame_clock.get_frame_time()
        if self._start_time is None:
            self._start_time = now
        elapsed = (now - self._start_time) / 1_000_000.0
        widget.queue_draw()
        total_run = self._fill_delay + self._fill_duration
        return elapsed < total_run

    def _on_draw(self, area, cr, w, h):
        _draw_orb(cr, *ORB_1[:3], ORB_1[3])
        _draw_orb(cr, *ORB_2[:3], ORB_2[3])

        elapsed = 0.0
        if self._start_time is not None:
            elapsed = self.get_frame_clock().get_frame_time()
            elapsed = (elapsed - self._start_time) / 1_000_000.0

        stroke_t = max(0.0, min(1.0, elapsed / self._duration))
        # ease-in-out
        stroke_t = stroke_t * stroke_t * (3 - 2 * stroke_t)
        fill_raw = max(0.0, min(1.0, (elapsed - self._fill_delay) / self._fill_duration))
        fill_t = 1 - pow(1 - fill_raw, 3)  # ease-out

        cr.save()
        cr.translate(self._tx, self._ty)

        if fill_t > 0.0:
            cr.new_path()
            cr.append_path(self._flat_path)
            cr.set_fill_rule(cairo.FILL_RULE_WINDING)
            cr.set_source(_rainbow_gradient(0, self._text_w, fill_t))
            cr.fill()

        stroke_width = 4.0 * (1.0 - fill_t)
        if stroke_t > 0.0 and stroke_width > 0.01:
            cr.new_path()
            cr.append_path(self._flat_path)
            cr.set_line_width(stroke_width)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            offset = self._total_length * (1.0 - stroke_t)
            cr.set_dash([self._total_length + 1, self._total_length + 1], offset)
            cr.set_source(_rainbow_gradient(0, self._text_w, 1.0))
            cr.stroke()

        cr.restore()


class FinishPage:
    def __init__(self, app):
        self.app = app
        self.bg = Background(sharp=False)

        center = Gtk.Box()
        center.set_halign(Gtk.Align.CENTER)
        center.set_valign(Gtk.Align.CENTER)
        center.set_hexpand(True)
        center.set_vexpand(True)
        self.canvas = WelcomeCanvas()
        center.append(self.canvas)
        self.bg.add_overlay(center)

        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.panel.add_css_class("progress-panel")
        self.panel.set_valign(Gtk.Align.END)
        self.panel.set_hexpand(True)

        self.status_label = Gtk.Label(label="")
        self.status_label.add_css_class("progress-status")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        self.panel.append(self.status_label)

        expander = Gtk.Expander(label="Show log")
        expander.add_css_class("progress-log-toggle")
        log_scroller = Gtk.ScrolledWindow()
        log_scroller.set_size_request(-1, 120)
        self.log_view = Gtk.TextView()
        self.log_view.add_css_class("progress-log")
        self.log_view.set_editable(False)
        self.log_view.set_cursor_visible(False)
        self.log_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        log_scroller.set_child(self.log_view)
        expander.set_child(log_scroller)
        self.panel.append(expander)

        self.error_label = None
        self.bg.add_overlay(self.panel)

        self.widget = self.bg
        self._started = False

    def on_show(self):
        self.canvas.start()
        if self._started:
            return
        self._started = True
        GLib.idle_add(self._commit)

    def _commit(self):
        cfg = self.app.state.build_cfg()
        self.app.state.log_settings(cfg)
        print("Starting post-installation setup...")
        if state_mod.IS_TEST_MODE:
            print("Test mode: post_setup not running, system unchanged.")
            GLib.timeout_add(500, lambda: (self.app.quit(), False)[1])
            return False
        state_mod.start_post_setup(cfg, self._on_output, self._on_done, self._on_error)
        return False

    def _on_output(self, line):
        buf = self.log_view.get_buffer()
        buf.insert(buf.get_end_iter(), line)
        self.log_view.scroll_mark_onscreen(buf.get_insert())
        trimmed = re.sub(r"^\++\s*", "", line.strip())
        if trimmed and not trimmed.startswith("#") and len(trimmed) > 2:
            self.status_label.set_label(trimmed[:100])

    def _on_done(self):
        self.app.quit()

    def _on_error(self, msg):
        if self.error_label is not None:
            return
        self.error_label = Gtk.Label(label="Post-install failed\n\n" + msg)
        self.error_label.add_css_class("error-box")
        self.error_label.set_wrap(True)
        self.error_label.set_xalign(0)
        self.panel.append(self.error_label)

        self.debug_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.debug_box.add_css_class("debug-share-box")
        uploading_label = Gtk.Label(label="Uploading log for debugging…")
        uploading_label.add_css_class("debug-share-body")
        uploading_label.set_xalign(0)
        self.debug_box.append(uploading_label)
        self.panel.append(self.debug_box)

        buf = self.log_view.get_buffer()
        log_text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        log_text = (log_text + "\n\n" + msg).strip()

        # Only the copy that leaves the machine gets scrubbed - the local
        # "Show log" view above stays exactly as post_setup produced it,
        # matching the Electron original's behavior for local debugging.
        cfg = self.app.state.build_cfg()
        upload_text = log_upload.redact(log_text, [
            (cfg.get("password"), "[REDACTED-PASSWORD]"),
            (cfg.get("username"), "[REDACTED-USERNAME]"),
            (cfg.get("hostname"), "[REDACTED-HOSTNAME]"),
            (cfg.get("fullname"), "[REDACTED-NAME]"),
        ])
        threading.Thread(
            target=self._upload_log_and_show, args=(upload_text,), daemon=True
        ).start()

    def _upload_log_and_show(self, log_text):
        url = log_upload.upload_log(log_text)
        qr_path = os.path.join(
            tempfile.gettempdir(), "pearos-post-install-error-qr.png"
        )
        if url:
            # Online: QR points at the paste, link is short and scannable
            # at a comfortable size.
            mode = "link" if log_upload.generate_qr(url, qr_path) else "link-no-qr"
        else:
            # Offline (or every paste host unreachable/down): no link to
            # point at, so the log itself - truncated to fit - becomes the
            # QR code. Nothing leaves the machine in this path.
            mode = "embedded" if log_upload.generate_qr_from_text(log_text, qr_path) else "none"
        GLib.idle_add(
            self._show_debug_share, mode, url, qr_path if mode in ("link", "embedded") else None
        )

    def _show_debug_share(self, mode, url, qr_path):
        child = self.debug_box.get_first_child()
        while child is not None:
            nxt = child.get_next_sibling()
            self.debug_box.remove(child)
            child = nxt

        if mode == "none":
            fallback = Gtk.Label(
                label=(
                    "Couldn't upload the log automatically (no internet?) or "
                    "generate a QR code for it. You can find it at "
                    "/home/default/Desktop/post-install.log and share it "
                    "manually in the GitHub Issues tab, the pearOS Discord, "
                    "or r/pearos."
                )
            )
            fallback.add_css_class("debug-share-body")
            fallback.set_wrap(True)
            fallback.set_xalign(0)
            self.debug_box.append(fallback)
            return False

        title = Gtk.Label(
            label="No internet - scan to read the log"
            if mode == "embedded"
            else "Need help? Share this with us"
        )
        title.add_css_class("debug-share-title")
        title.set_xalign(0)
        self.debug_box.append(title)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=14)
        if qr_path:
            qr_frame = Gtk.Box()
            qr_frame.add_css_class("debug-share-qr")
            qr_picture = Gtk.Picture.new_for_filename(qr_path)
            qr_picture.set_content_fit(Gtk.ContentFit.CONTAIN)
            qr_picture.set_size_request(120, 120)
            qr_picture.set_can_shrink(True)
            qr_frame.append(qr_picture)
            row.append(qr_frame)

        text_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_col.set_valign(Gtk.Align.CENTER)
        if mode == "embedded":
            instructions = Gtk.Label(
                label=(
                    "This machine isn't connected to the internet, so the "
                    "error log itself is encoded in this QR code (if it was "
                    "long, only the end of it fits). Scan it with your "
                    "phone, then share what you see in one of these places "
                    "so we can help debug this:\n"
                    "• the Issues tab on GitHub\n"
                    "• the pearOS Discord\n"
                    "• r/pearos"
                )
            )
        else:
            instructions = Gtk.Label(
                label=(
                    "Scan the QR code (or open the link below), then share it in "
                    "one of these places so we can help debug this:\n"
                    "• the Issues tab on GitHub\n"
                    "• the pearOS Discord\n"
                    "• r/pearos"
                )
            )
        instructions.add_css_class("debug-share-body")
        instructions.set_wrap(True)
        instructions.set_xalign(0)
        instructions.set_justify(Gtk.Justification.LEFT)
        text_col.append(instructions)

        if mode in ("link", "link-no-qr") and url:
            url_label = Gtk.Label(label=url)
            url_label.add_css_class("debug-share-url")
            url_label.set_xalign(0)
            url_label.set_selectable(True)
            url_label.set_wrap(True)
            text_col.append(url_label)

        row.append(text_col)
        self.debug_box.append(row)
        return False
