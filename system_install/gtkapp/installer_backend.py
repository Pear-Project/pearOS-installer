"""Single isolated entry point for "actually start the install" - today
this is exactly what engine.js's open_installer() did (spawn Calamares's
own launcher, detached, and forget about it). Both menu.py's "Install"
action and confirm.py's disk-select Continue button call this same
function, so redirecting it to a custom setup script later (per the user's
stated plan) is a one-function edit here, not a UI change anywhere."""
from . import state


def launch_install(disk=None):
    """disk: optional {name, path, size, model} from disk_backend.py - not
    used yet (Calamares does its own disk selection internally), but
    accepted now so callers/this function's future replacement don't need
    a signature change later."""
    if state.IS_TEST_MODE:
        print(f"[test mode] would run: sudo /usr/bin/calamares-install-debian (disk={disk})")
        return
    state.run_detached(["sudo", "/usr/bin/calamares-install-debian"])
