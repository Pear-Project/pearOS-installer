"""Port of app/js/engine.js: wizard state, navigation, validation, file
writes to /tmp/*, and the final commit()/post_setup invocation.

Behavioral parity notes (see the approved plan):
- The same /tmp/* files are written, with the same content/quoting, as the
  Electron version, so anything else that might read them keeps working.
- The final post_setup invocation uses the same 9 positional arguments in
  the same order, and the same explicit PATH override, as main.js.
"""
import os
import re
import subprocess

import gi

gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.join(APP_ROOT, "app")
RESOURCES_DIR = os.path.join(APP_DIR, "resources")
PROFILES_DIR = os.path.join(RESOURCES_DIR, "profiles")

USERNAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")
MAX_USERNAME_LEN = 32

IS_TEST_MODE = os.environ.get("POST_INSTALL_TEST") == "1"

COMMON_TIMEZONES = [
    "Africa/Cairo", "Africa/Johannesburg", "Africa/Lagos", "Africa/Nairobi",
    "America/Anchorage", "America/Argentina/Buenos_Aires", "America/Bogota",
    "America/Chicago", "America/Denver", "America/Los_Angeles", "America/Mexico_City",
    "America/New_York", "America/Sao_Paulo", "America/Toronto", "America/Vancouver",
    "Asia/Bangkok", "Asia/Dubai", "Asia/Hong_Kong", "Asia/Istanbul", "Asia/Jakarta",
    "Asia/Jerusalem", "Asia/Kolkata", "Asia/Seoul", "Asia/Shanghai", "Asia/Singapore",
    "Asia/Tokyo",
    "Atlantic/Reykjavik",
    "Australia/Melbourne", "Australia/Perth", "Australia/Sydney",
    "Europe/Amsterdam", "Europe/Athens", "Europe/Berlin", "Europe/Bucharest",
    "Europe/Budapest", "Europe/Dublin", "Europe/Helsinki", "Europe/Lisbon",
    "Europe/London", "Europe/Madrid", "Europe/Moscow", "Europe/Paris",
    "Europe/Prague", "Europe/Rome", "Europe/Stockholm", "Europe/Vienna",
    "Europe/Warsaw", "Europe/Zurich",
    "Pacific/Auckland", "Pacific/Honolulu",
    "UTC",
]


def _load_reserved_usernames():
    path = os.path.join(APP_ROOT, "reserved_usernames")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip() and not l.startswith("#")]
    except OSError:
        return []


RESERVED_USERNAMES = _load_reserved_usernames()


def write_tmp(name, content):
    with open("/tmp/" + name, "w", encoding="utf-8") as f:
        f.write(content)


def read_tmp(name):
    try:
        with open("/tmp/" + name, "r", encoding="utf-8") as f:
            return f.read().strip().strip("'")
    except OSError:
        return ""


class WizardState:
    def __init__(self):
        self.lng = "en_US"
        self.keymap = None
        self.locale = None
        self.timezone = None
        self.utc_enabled = None
        self.full_name = None
        self.account_name = None
        self.hostname = "pearOS-machine"
        self.password = None
        self.profile_picture = None
        self.theme_mode = "light"
        self.country = None
        # Set by country.py (True) / migration_assistant.py (False) right
        # before navigating to "wifi" - lets that page's own skip-if-
        # online-or-no-wifi-hardware check know which neighbor to bounce
        # onward to, since it sits between them in both directions.
        self.wifi_entry_forward = True

    # ── Language selection ───────────────────────────────────────────
    def select_language(self, locale_code):
        """locale_code is e.g. 'en_US.UTF-8', as chosen from the language list."""
        self.locale = locale_code
        write_tmp("locale", locale_code)
        self.lng = locale_code.replace(".UTF-8", "")

    # ── Country/region ────────────────────────────────────────────────
    def select_country(self, country_name):
        self.country = country_name
        write_tmp("country", country_name)

    # ── Keymap ──────────────────────────────────────────────────────
    def save_keymap(self, layout):
        if not layout:
            return "You must choose one Keyboard Layout from the list"
        self.keymap = layout
        write_tmp("keymap", layout)
        try:
            subprocess.Popen(
                ["setxkbmap", layout],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            pass
        return None

    # ── Timezone ──────────────────────────────────────────────────────
    def detect_windows_dual_boot(self):
        windows_detected = False
        try:
            out = subprocess.run(
                ["efibootmgr"], capture_output=True, timeout=5, text=True
            ).stdout
            if re.search(r"windows boot manager", out, re.IGNORECASE):
                windows_detected = True
        except (OSError, subprocess.TimeoutExpired):
            pass
        if not windows_detected:
            try:
                out = subprocess.run(
                    ["os-prober"], capture_output=True, timeout=15, text=True
                ).stdout
                if re.search(r"windows", out, re.IGNORECASE):
                    windows_detected = True
            except (OSError, subprocess.TimeoutExpired):
                pass
        return windows_detected

    def save_timezone(self, tz_text, utc_enabled):
        if not tz_text:
            return "You must choose one Time Zone from the list"
        self.timezone = tz_text
        self.utc_enabled = bool(utc_enabled)
        write_tmp("timezone", tz_text)
        write_tmp("utc_enabled", "true" if utc_enabled else "false")
        return None

    # ── User ──────────────────────────────────────────────────────────
    def validate_user(self, full_name, account_name, hostname, password, password_confirm):
        if not full_name or not full_name.strip():
            return "Full name cannot be empty"
        if not account_name or not account_name.strip():
            return "Username cannot be empty"
        if not USERNAME_RE.match(account_name):
            return (
                "The username must start with a lowercase letter and contain "
                "only lowercase letters, digits, and hyphens."
            )
        if len(account_name) > MAX_USERNAME_LEN:
            return "Username too long (max %d chars)" % MAX_USERNAME_LEN
        if account_name in RESERVED_USERNAMES:
            return "This username is reserved"
        if not password:
            return "Password cannot be empty"
        if password != password_confirm:
            return "Passwords do not match"
        return None

    def save_user(self, full_name, account_name, hostname, password, password_confirm, profile_picture_path):
        err = self.validate_user(full_name, account_name, hostname, password, password_confirm)
        if err:
            return err
        self.full_name = full_name
        self.account_name = account_name
        self.hostname = hostname or "pearOS-machine"
        self.password = password
        write_tmp("fullname", "'" + full_name + "'")
        write_tmp("username", account_name)
        write_tmp("hostname", self.hostname)
        write_tmp("password", password)
        if profile_picture_path:
            self.profile_picture = profile_picture_path
            write_tmp("profile_picture", profile_picture_path)
        return None

    # ── Look ──────────────────────────────────────────────────────────
    def detect_default_look_mode(self):
        try:
            with open(
                "/usr/share/extras/system-settings/themeswitcher/state", "r", encoding="utf-8"
            ) as f:
                state = f.read().strip().lower()
            if state in ("dark", "light"):
                return state
        except OSError:
            pass
        return "light"

    def save_look(self, mode):
        self.theme_mode = "dark" if mode == "dark" else "light"
        write_tmp("theme_mode", self.theme_mode)
        return None

    # ── Deferred per-user settings ────────────────────────────────────
    # These pages (Accessibility, Analytics, Screen Time, Touch ID) run as
    # the live 'default' user, before the real account even exists (useradd
    # happens near the end of post_setup) — anything they'd apply directly
    # (kwriteconfig6 into ~/.config, systemctl --user, fprintd-enroll) would
    # land on 'default' and be lost when it's deleted on next boot. So, same
    # as the profile-picture handoff via /tmp/profile_picture, they only
    # persist the *choice* here; post_setup (root, after creating the real
    # user) is what actually applies it for the correct username.
    def save_accessibility(self, prefs):
        """prefs: dict of str -> bool/int, e.g. {'reduce_motion': True,
        'sticky_keys': False, 'cursor_size': 48, ...}."""
        lines = "\n".join(f"{k}={v}" for k, v in prefs.items())
        write_tmp("accessibility_prefs", lines)

    def save_analytics(self, send_diagnostics, share_crash_data):
        write_tmp(
            "analytics_prefs",
            f"send_diagnostics={send_diagnostics}\nshare_crash_data={share_crash_data}",
        )

    def save_screentime(self, enabled):
        write_tmp("screentime_enabled", "true" if enabled else "false")

    def save_touchid(self, enabled):
        write_tmp("touchid_enabled", "true" if enabled else "false")

    def save_location_services(self, enabled):
        write_tmp("location_services_enabled", "true" if enabled else "false")

    def save_auto_update(self, mode):
        """mode: 'full' (download + install automatically) or
        'download_only' (download automatically, install manually)."""
        write_tmp("auto_update_mode", mode)

    # ── Profile pictures ────────────────────────────────────────────
    def list_profile_pictures(self):
        exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"}
        try:
            files = sorted(os.listdir(PROFILES_DIR))
        except OSError:
            return []
        return [
            os.path.join(PROFILES_DIR, f)
            for f in files
            if os.path.splitext(f)[1].lower() in exts
        ]

    def select_profile_picture(self, path):
        self.profile_picture = path
        write_tmp("profile_picture", path)
        if not IS_TEST_MODE:
            for dest in (
                "/usr/share/sddm/themes/pearOS/faces/.face.icon",
                "/usr/share/sddm/themes/pearOS-dark/faces/.face.icon",
            ):
                try:
                    subprocess.Popen(["sudo", "cp", path, dest])
                except OSError:
                    pass

    # ── Commit ──────────────────────────────────────────────────────
    def build_cfg(self):
        return {
            "keymap": read_tmp("keymap"),
            "locale": read_tmp("locale"),
            "timezone": read_tmp("timezone"),
            "fullname": read_tmp("fullname"),
            "username": read_tmp("username"),
            "hostname": read_tmp("hostname") or "pearOS-machine",
            "password": read_tmp("password"),
            "utc_enabled": "true" if read_tmp("utc_enabled") == "true" else "false",
            "theme_mode": "dark" if read_tmp("theme_mode") == "dark" else "light",
        }

    def log_settings(self, cfg):
        print("")
        print("==========================================")
        print("  Selected Configuration Settings")
        print("==========================================")
        print("Keyboard Layout:     " + cfg["keymap"])
        print("Locale:              " + cfg["locale"])
        print("Timezone:            " + cfg["timezone"])
        print("Full Name:           " + cfg["fullname"])
        print("Username:            " + cfg["username"])
        print("Hostname:            " + cfg["hostname"])
        print("Look:                " + cfg["theme_mode"])
        print("==========================================")
        print("")


def start_post_setup(cfg, on_output, on_done, on_error):
    """Launch `sudo /usr/local/bin/post_setup <9 args>`, streaming stdout+stderr
    line-by-line via on_output(line), then on_done() or on_error(message).

    Mirrors main.js's 'run-post-setup' IPC handler: same explicit PATH (sudo's
    secure_path doesn't include /usr/local/bin on this image), same argument
    order, same exit-code handling.
    """
    env = os.environ.copy()
    env["PATH"] = "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

    argv = [
        "sudo", "/usr/local/bin/post_setup",
        cfg["keymap"], cfg["locale"], cfg["timezone"], cfg["password"],
        cfg["fullname"], cfg["username"], cfg["hostname"],
        cfg["utc_enabled"], cfg["theme_mode"],
    ]

    launcher = Gio.SubprocessLauncher.new(
        Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_MERGE
    )
    launcher.set_environ([f"{k}={v}" for k, v in env.items()])
    try:
        proc = launcher.spawnv(argv)
    except GLib.Error as e:
        on_error(str(e))
        return

    stdout = proc.get_stdout_pipe()
    stream = Gio.DataInputStream.new(stdout)

    def read_line():
        stream.read_line_async(GLib.PRIORITY_DEFAULT, None, on_line)

    def on_line(source, result):
        try:
            line, _len = source.read_line_finish_utf8(result)
        except GLib.Error:
            line = None
        if line is None:
            return
        on_output(line + "\n")
        read_line()

    read_line()

    def on_exit(source, result):
        try:
            source.wait_check_finish(result)
            on_done()
        except GLib.Error:
            err_msg = "Script exit code: %d" % source.get_exit_status()
            try:
                with open("/tmp/post-install-error", "r", encoding="utf-8") as f:
                    file_msg = f.read().strip()
                if file_msg:
                    err_msg = file_msg
            except OSError:
                pass
            on_error(err_msg + "\nCheck /home/default/Desktop/post-install.log")

    proc.wait_check_async(None, on_exit)
