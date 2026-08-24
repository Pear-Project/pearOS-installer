"""PearID sign-in, ported from dpkg/system-settings/backend/pearidmanager.cpp
to plain subprocess calls onto the same shell scripts it uses
(state.sh/login_and_sync.sh/get_user_info.sh/exit.sh) - same account.pearos.xyz
backend, no reimplementation of the actual API protocol here."""
import os
import subprocess

_CANDIDATE_DIRS = [
    "/usr/share/extras/system-settings/pearID",
    os.path.expanduser("~/Desktop/dpkg/system-settings/pearID"),
]


def _script_dir():
    for d in _CANDIDATE_DIRS:
        if os.path.isdir(d):
            return d
    return _CANDIDATE_DIRS[0]


def _script(name):
    return os.path.join(_script_dir(), name)


def _run(argv, timeout=20):
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def check_state():
    """Returns 'loggedin', 'loggedout', or 'unknown' (network/server hiccup -
    state.sh returns 300/500 in that case, same as the C++ manager)."""
    script = _script("state.sh")
    if not os.path.isfile(script):
        return "loggedout"
    result = _run(["bash", script])
    if result is None:
        return "unknown"
    out = result.stdout.strip()
    if out == "true":
        return "loggedin"
    if out == "false":
        return "loggedout"
    return "unknown"


def get_user_info():
    script = _script("get_user_info.sh")
    if not os.path.isfile(script):
        return {}
    result = _run(["bash", script, "--first-name", "--last-name", "--email"])
    if result is None:
        return {}
    lines = [l.strip() for l in result.stdout.split("\n") if l.strip()]
    first = lines[0] if len(lines) > 0 else ""
    last = lines[1] if len(lines) > 1 else ""
    email = lines[2] if len(lines) > 2 else ""
    name = (first + " " + last).strip() or email
    return {"name": name, "email": email}


def login(email, password):
    script = _script("login_and_sync.sh")
    if not os.path.isfile(script):
        return False, "Login script not found"
    result = _run(["bash", script, email, password], timeout=30)
    if result is None:
        return False, "Login failed"
    ok = (
        result.returncode == 0
        or "Authentication successful" in result.stdout
        or "Authenticated" in result.stdout
    )
    return ok, (None if ok else "Login failed. Check your credentials.")


def logout():
    script = _script("exit.sh")
    if os.path.isfile(script):
        _run(["bash", script])
