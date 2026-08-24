"""Best-effort crash-log sharing: on a failed post_setup run, upload the
log text to a plain-text paste host and render a QR code pointing at it, so
someone hitting a failure can scan it and drop the link into a GitHub
issue / the pearOS Discord / r/pearos without having to type or copy
anything by hand.

Entirely optional and non-fatal by design: if there's no network, `curl`
or `qrencode` aren't installed, or every paste host is down, callers just
get None back and fall back to the plain in-app log view that already
existed. Nothing here should ever raise.

Requires (both apt packages, no pip deps, matching this project's other
system-tool integrations): `curl`, `qrencode`.
"""
import os
import subprocess
import tempfile

_CURL_TIMEOUT = 15
_QRENCODE_TIMEOUT = 10


def _try_paste_rs(path):
    try:
        out = subprocess.run(
            ["curl", "-fsSL", "--max-time", "10", "--data-binary", "@" + path, "https://paste.rs/"],
            capture_output=True, text=True, timeout=_CURL_TIMEOUT,
        )
        url = out.stdout.strip()
        if out.returncode == 0 and url.startswith("http"):
            return url
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def _try_0x0(path):
    try:
        out = subprocess.run(
            ["curl", "-fsSL", "--max-time", "10", "-F", "file=@%s;filename=post-install.log" % path, "https://0x0.st"],
            capture_output=True, text=True, timeout=_CURL_TIMEOUT,
        )
        url = out.stdout.strip()
        if out.returncode == 0 and url.startswith("http"):
            return url
    except (OSError, subprocess.TimeoutExpired):
        pass
    return None


def upload_log(text):
    """Uploads `text` to a paste host, trying a couple of hosts in order.
    Returns a URL string, or None if nothing worked. Safe to call from a
    background thread (does blocking network I/O)."""
    if not text or not text.strip():
        return None
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".log", delete=False, encoding="utf-8"
        ) as f:
            f.write(text)
            tmp_path = f.name
        for uploader in (_try_paste_rs, _try_0x0):
            url = uploader(tmp_path)
            if url:
                return url
        return None
    except OSError:
        return None
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


def redact(text, replacements):
    """Replaces each non-empty value in `replacements` (an iterable of
    (value, placeholder) pairs) with its placeholder, longest value first
    so a short value (e.g. a one-letter hostname) can't clobber part of a
    longer one before it gets its turn. Exact literal matches only - this
    runs on the copy of the log that leaves the machine (see finish.py),
    to keep the password, account username, and hostname out of a paste
    anyone with the link/QR code can read; the in-app log view shown to
    the person debugging their own machine is left untouched."""
    if not text:
        return text
    pairs = sorted(
        ((v, p) for v, p in replacements if v), key=lambda vp: len(vp[0]), reverse=True
    )
    for value, placeholder in pairs:
        text = text.replace(value, placeholder)
    return text


def generate_qr(url, out_path):
    """Renders a PNG QR code for `url` at out_path via qrencode. Returns
    True on success, False if qrencode isn't installed or fails."""
    try:
        result = subprocess.run(
            ["qrencode", "-o", out_path, "-s", "8", "-m", "2", url],
            capture_output=True, timeout=_QRENCODE_TIMEOUT,
        )
        return result.returncode == 0 and os.path.exists(out_path)
    except (OSError, subprocess.TimeoutExpired):
        return False


# A QR code (version 40, byte mode, error-correction L - the loosest level,
# chosen deliberately here to maximize how much text fits) tops out around
# 2953 bytes. Leave margin for the "...[truncated]..." notice and for
# UTF-8 characters that encode to more than one byte each.
_MAX_QR_TEXT_BYTES = 2800


def _truncate_for_qr(text, max_bytes=_MAX_QR_TEXT_BYTES):
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    notice = "...[truncated - showing the end of the log]...\n"
    keep = max_bytes - len(notice.encode("utf-8"))
    # Slicing raw UTF-8 bytes can land mid-character; errors="ignore" just
    # drops that one partial character at the cut point.
    tail = encoded[-keep:].decode("utf-8", errors="ignore")
    return notice + tail


def generate_qr_from_text(text, out_path):
    """Encodes `text` directly into a PNG QR code at out_path - no paste
    host, no URL, nothing leaves the machine. Used when there's no network
    to upload the log to (see upload_log()): the log itself, truncated to
    fit a QR code's capacity if needed, becomes the QR code. Returns True
    on success, False if qrencode isn't installed, fails, or the text
    doesn't fit anything qrencode can produce."""
    if not text or not text.strip():
        return False
    payload = _truncate_for_qr(text)
    try:
        result = subprocess.run(
            ["qrencode", "-o", out_path, "-s", "5", "-m", "2", "-l", "L", "-8", payload],
            capture_output=True, timeout=_QRENCODE_TIMEOUT,
        )
        return result.returncode == 0 and os.path.exists(out_path)
    except (OSError, subprocess.TimeoutExpired):
        return False
