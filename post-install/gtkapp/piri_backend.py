"""Piri - ported from dpkg/system-settings/backend/pirimanager.cpp. Only
persists the same SHOW_ICON_FILE flag the real PiriManager reads
(/usr/share/extras/piri/show_icon); the actual speech-model download
(hundreds of MB from cdn.pearos.xyz, via pkexec + unzip in the C++ manager)
is deliberately NOT started here - post_setup reboots the machine right
after this wizard finishes, which would just kill an in-progress download
for nothing. The real system-settings app downloads it on first real login
instead, same as this wizard already defers Liquid Gel/theme setup via
autostart entries in post_setup."""
import subprocess

SHOW_ICON_FILE = "/usr/share/extras/piri/show_icon"
MODEL_DIR = "/usr/share/extras/piri/model"


def model_exists():
    import os

    try:
        return os.path.isdir(MODEL_DIR) and bool(os.listdir(MODEL_DIR))
    except OSError:
        return False


def set_enabled(enabled):
    value = "true" if enabled else "false"
    cmd = (
        f'mkdir -p "$(dirname {SHOW_ICON_FILE})" && '
        f'echo -n "{value}" > {SHOW_ICON_FILE}'
    )
    try:
        subprocess.Popen(["sudo", "bash", "-c", cmd])
    except OSError:
        pass
