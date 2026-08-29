"""Touch ID, ported from dpkg/system-settings/backend/touchidmanager.cpp:
device detection via lsusb, enrollment/listing/deletion via fprintd - no
D-Bus needed, same as the C++ manager."""
import os
import re
import subprocess

_USERNAME = os.environ.get("USER") or os.environ.get("LOGNAME") or ""


def has_device():
    try:
        result = subprocess.run(
            "lsusb 2>/dev/null | grep -i -e finger -e fprint -e biom | head -1",
            shell=True, capture_output=True, text=True, timeout=5,
        )
        return bool(result.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        return False


def list_fingerprints(username=None):
    username = username or _USERNAME
    try:
        result = subprocess.run(
            ["fprintd-list", username], capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    fingers = re.findall(r"-\s*#\d+:\s*(\S+)", result.stdout)
    return [{"finger": f, "label": f.replace("-", " ")} for f in fingers]


def delete_fingerprint(finger, username=None):
    username = username or _USERNAME
    try:
        subprocess.run(
            ["fprintd-delete", username, "-f", finger],
            capture_output=True, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass


class EnrollSession:
    """Streams fprintd-enroll output line by line via on_status(text), then
    calls on_done(success) - mirrors TouchIDManager's enrollFingerprint().
    on_stage() (optional) fires once per detected swipe/stage line, so the
    UI can drive a fill-up fingerprint animation without re-parsing text."""

    def __init__(self, finger, on_status, on_done, username=None, on_stage=None):
        self._on_status = on_status
        self._on_done = on_done
        self._on_stage = on_stage
        self._proc = None
        self._finger = finger
        self._username = username or _USERNAME

    def start(self):
        try:
            self._proc = subprocess.Popen(
                ["fprintd-enroll", self._username, self._finger],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1,
            )
        except OSError as exc:
            self._on_done(False, str(exc))
            return

        import threading

        def read_output():
            for line in self._proc.stdout:
                line = line.strip()
                if not line:
                    continue
                if "done" in line.lower() or "enrolled" in line.lower():
                    self._on_status("Fingerprint enrolled successfully!")
                elif "stage" in line.lower() or "swipe" in line.lower():
                    self._on_status("Swipe detected — keep going...")
                    if self._on_stage:
                        self._on_stage()
                else:
                    self._on_status(line)
            code = self._proc.wait()
            self._on_done(code == 0, None if code == 0 else "Enrollment failed or cancelled.")

        threading.Thread(target=read_output, daemon=True).start()

    def cancel(self):
        if self._proc:
            try:
                self._proc.terminate()
            except OSError:
                pass
