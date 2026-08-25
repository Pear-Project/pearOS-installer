"""Load the bundled "Sen" TTF font without installing it system-wide.

Equivalent of assistant-styles.css's @font-face rule. Uses the standard
Linux trick of registering a font file directly with fontconfig
(FcConfigAppFontAddFile), so Pango/Cairo can address it by family name
immediately, in-process, without touching /usr/share/fonts.
"""
import ctypes
import ctypes.util
import os

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(_APP_DIR, "app", "fonts")

SEN_FONT = os.path.join(FONTS_DIR, "pearOS-Font-Regular.ttf")

_fc = None


def _load_fontconfig():
    global _fc
    if _fc is not None:
        return _fc
    lib_name = ctypes.util.find_library("fontconfig") or "libfontconfig.so.1"
    lib = ctypes.CDLL(lib_name)
    lib.FcConfigGetCurrent.restype = ctypes.c_void_p
    lib.FcConfigAppFontAddFile.restype = ctypes.c_int
    lib.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    _fc = lib
    return lib


def register_app_font(path):
    """Register a font file with the current process's fontconfig config.

    Returns True on success. Safe to call even if the file is missing.
    """
    if not os.path.isfile(path):
        return False
    lib = _load_fontconfig()
    config = lib.FcConfigGetCurrent()
    ok = lib.FcConfigAppFontAddFile(config, path.encode("utf-8"))
    return bool(ok)


def register_all():
    register_app_font(SEN_FONT)
