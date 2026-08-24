"""Port of app/js/wallpaper.js: find the user's current KDE Plasma wallpaper,
falling back to the bundled resources/background image."""
import os
import re

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_WALLPAPER = os.path.join(_APP_DIR, "app", "resources", "background.png")

_SECTION_RE = re.compile(r"^\[(.+)\]$")
_IMAGE_RE = re.compile(r"^Image=(.*)$")


def _read_image_from_ini_file(file_path, section_suffix):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return None

    in_section = False
    found = None
    for line in content.split("\n"):
        m = _SECTION_RE.match(line)
        if m:
            name = m.group(1)
            in_section = (
                name == section_suffix
                or (("]" + section_suffix) in name)
                or name[-len(section_suffix):] == section_suffix
            )
            continue
        if in_section:
            m2 = _IMAGE_RE.match(line)
            if m2 and not found:
                found = m2.group(1).strip()
    return found


def _read_user_wallpaper_override():
    config_path = os.path.join(
        os.path.expanduser("~"), ".config", "plasma-org.kde.plasma.desktop-appletsrc"
    )
    return _read_image_from_ini_file(config_path, "Wallpaper][org.kde.image][General")


def _read_look_and_feel_wallpaper():
    kdeglobals = os.path.join(os.path.expanduser("~"), ".config", "kdeglobals")
    try:
        with open(kdeglobals, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return None
    m = re.search(r"^LookAndFeelPackage=(.+)$", content, re.MULTILINE)
    if not m:
        return None
    theme_id = m.group(1).strip()

    defaults_paths = [
        os.path.join(
            os.path.expanduser("~"),
            ".local/share/plasma/look-and-feel",
            theme_id,
            "contents/defaults",
        ),
        os.path.join("/usr/share/plasma/look-and-feel", theme_id, "contents/defaults"),
    ]
    for p in defaults_paths:
        val = _read_image_from_ini_file(p, "Wallpaper")
        if val:
            return val
    return None


def _file_uri_to_path(uri):
    if uri.startswith("file://"):
        from urllib.parse import unquote
        return unquote(uri[len("file://"):])
    return uri


def _candidate_paths(value):
    if value.startswith("file://") or value.startswith("/"):
        return [_file_uri_to_path(value)]
    return [
        os.path.join(os.path.expanduser("~"), ".local/share/wallpapers", value),
        os.path.join("/usr/share/wallpapers", value),
    ]


def _resolve_image_file(p):
    if os.path.isfile(p):
        return p
    if not os.path.isdir(p):
        return None

    images_dir = os.path.join(p, "contents", "images")
    try:
        candidates = os.listdir(images_dir)
    except OSError:
        return None
    if not candidates:
        return None

    def area(name):
        m = re.search(r"(\d+)x(\d+)", name)
        return int(m.group(1)) * int(m.group(2)) if m else 0

    candidates.sort(key=area, reverse=True)
    return os.path.join(images_dir, candidates[0])


def _resolve_wallpaper(value):
    for candidate in _candidate_paths(value):
        resolved = _resolve_image_file(candidate)
        if resolved:
            return resolved
    return None


def find_wallpaper():
    """Return an absolute path to the live wallpaper, or the bundled default."""
    raw = _read_user_wallpaper_override() or _read_look_and_feel_wallpaper()
    if raw:
        resolved = _resolve_wallpaper(raw)
        if resolved:
            return resolved
    return DEFAULT_WALLPAPER
