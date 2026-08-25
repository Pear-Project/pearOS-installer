"""Entry point for the "Disk Utility" menu action (former GParted button).

Disk Utility is now literally step 1 of a real install, not a standalone
repair tool: it launches the exact same full Calamares sequence
calamares-install-debian does (system /etc/calamares/settings.conf -
partition, locale, keyboard, summary, then exec: mount/unpackfs/.../
bootloader), just with our patched partition module giving it the macOS
Disk Utility UI (see deb-iso's customize.sh for how that module gets
installed system-wide). Nothing is written to disk merely by picking an
action here - that only happens if proceed_with_install() is later called
(normally via the "Install pearOS" button) all the way through to exec.

Flow: launch_disk_utility() starts Calamares and connects to its
pearOS-only remote-control socket (RemoteControl.h/.cpp in calamares-src).
The moment a valid partitioning choice is made (next_enabled fires true),
the choice snapshot ChoicePage.cpp just wrote is read, the window is
minimized, and on_ready(choice) is called so the caller (confirm.py) can
show it to the user. Later, proceed_with_install() sends `next` and keeps
driving Calamares' remaining show-phase pages (locale/keyboard/summary)
automatically - all while it stays minimized - until exec starts, at which
point progress/finished/failed events get forwarded to the caller's own
callbacks (install_progress.py). A watchdog restores the window if nothing
happens for a while, on the assumption something needs real interaction
that can't be seen while hidden, rather than hanging forever."""
import json
import os
import threading

from gi.repository import GLib

from . import state
from .calamares_remote import CalamaresRemote

_CHOICE_SNAPSHOT_PATH = "/tmp/pearos-disk-utility-choice.json"
_AUTO_ADVANCE_TIMEOUT_S = 8

_remote = None
_pending_choice = None
_on_ready_cb = None
_progress_cbs = None  # (on_progress, on_finished, on_failed, on_stuck) once proceed_with_install() is called
_exec_started = False
_watchdog_id = None


def launch_disk_utility(on_ready=None):
    """on_ready(choice_dict) is called (on the GTK main thread) once the
    user has picked a valid partitioning action in Disk Utility and its
    window has been minimized. choice_dict is whatever ChoicePage.cpp's
    writeChoiceSnapshot() wrote: {"installChoice", "device", "deviceName"}."""
    global _remote, _pending_choice, _on_ready_cb, _progress_cbs, _exec_started
    _pending_choice = None
    _on_ready_cb = on_ready
    _progress_cbs = None
    _exec_started = False

    if state.IS_TEST_MODE:
        print("[test mode] would run: pkexec calamares")
        return

    # Same xhost dance calamares-install-debian uses - pkexec runs
    # Calamares as root, which otherwise can't attach to the caller's
    # X/XWayland display.
    state.run_detached(
        ["sh", "-c", "xhost +si:localuser:root; pkexec calamares; xhost -si:localuser:root"]
    )

    _remote = CalamaresRemote()
    threading.Thread(target=_connect_and_listen, daemon=True).start()


def _connect_and_listen():
    # pkexec + Calamares startup takes a few seconds; connect() retries
    # internally for up to this long before giving up.
    if _remote.connect(timeout=30.0):
        _remote.start_listening(_on_event)


def _on_event(event):
    global _pending_choice, _exec_started

    kind = event.get("event")
    if kind == "next_enabled":
        if not event.get("value"):
            return
        if _progress_cbs is None:
            # Still on the partition step - a choice just became valid.
            _load_choice_snapshot()
            _remote.send_cmd("minimize")
            if _on_ready_cb:
                _on_ready_cb(_pending_choice)
        elif not _exec_started:
            # Auto-advancing through locale/keyboard/summary.
            _cancel_watchdog()
            _remote.send_cmd("next")
            _arm_watchdog()
    elif kind == "progress":
        _exec_started = True
        _cancel_watchdog()
        if _progress_cbs:
            _progress_cbs[0](event.get("percent", 0.0), event.get("label", ""))
    elif kind == "finished":
        _cancel_watchdog()
        if _progress_cbs:
            _progress_cbs[1]()
    elif kind == "failed":
        _cancel_watchdog()
        if _progress_cbs:
            _progress_cbs[2](event.get("message", ""), event.get("details", ""))


def _load_choice_snapshot():
    global _pending_choice
    try:
        with open(_CHOICE_SNAPSHOT_PATH, "r") as f:
            _pending_choice = json.load(f)
    except (OSError, ValueError):
        _pending_choice = None


def has_pending_choice():
    return _remote is not None and _remote.connected and _pending_choice is not None


def get_pending_choice():
    return _pending_choice


def proceed_with_install(on_progress=None, on_finished=None, on_failed=None, on_stuck=None):
    """Returns False (does nothing) if there's no live Disk Utility
    session with a choice already made - the caller should fall back to
    installer_backend.launch_install() (a fresh, independent install) in
    that case, e.g. when "Install pearOS" is used without going through
    Disk Utility first."""
    global _progress_cbs
    if not has_pending_choice():
        return False
    _progress_cbs = (
        on_progress or (lambda *a: None),
        on_finished or (lambda: None),
        on_failed or (lambda *a: None),
        on_stuck or (lambda: None),
    )
    _remote.send_cmd("next")  # leaves the partition step
    _arm_watchdog()
    return True


def _arm_watchdog():
    global _watchdog_id
    _cancel_watchdog()
    _watchdog_id = GLib.timeout_add_seconds(_AUTO_ADVANCE_TIMEOUT_S, _on_watchdog_fired)


def _cancel_watchdog():
    global _watchdog_id
    if _watchdog_id is not None:
        GLib.source_remove(_watchdog_id)
        _watchdog_id = None


def _on_watchdog_fired():
    global _watchdog_id
    _watchdog_id = None
    # Nothing happened for a while - probably a show-phase page that
    # needs real interaction we can't see while minimized. Surface the
    # window instead of leaving the user staring at a stalled progress
    # page with no explanation.
    if _remote:
        _remote.send_cmd("restore")
    if _progress_cbs:
        _progress_cbs[3]()
    return GLib.SOURCE_REMOVE
