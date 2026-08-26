"""Real Wi-Fi scanning/connection via nmcli (NetworkManager's CLI) - same
connectivity check style as post_setup's has_internet()."""
import json
import subprocess
import urllib.error
import urllib.request


def _run(argv, timeout=15):
    try:
        return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None


def has_internet():
    result = _run(["ping", "-c", "1", "-W", "3", "8.8.8.8"], timeout=5)
    if result and result.returncode == 0:
        return True
    result = _run(["curl", "-s", "--max-time", "3", "https://www.debian.org"], timeout=5)
    return bool(result and result.returncode == 0)


def has_wifi_device():
    result = _run(["nmcli", "-t", "-f", "TYPE", "device"], timeout=5)
    if not result or result.returncode != 0:
        return False
    return "wifi" in result.stdout.splitlines()


def scan_networks(rescan=True):
    """Returns a list of {ssid, signal, security, active}, strongest first,
    de-duplicated by SSID (nmcli lists one row per BSSID)."""
    argv = ["nmcli", "-t", "-f", "ACTIVE,SSID,SIGNAL,SECURITY", "device", "wifi", "list"]
    if rescan:
        argv.append("--rescan")
        argv.append("yes")
    result = _run(argv, timeout=20)
    if not result or result.returncode != 0:
        return []

    best = {}
    for line in result.stdout.splitlines():
        parts = line.split(":")
        if len(parts) < 4:
            continue
        active, ssid, signal, security = parts[0], parts[1], parts[2], ":".join(parts[3:])
        if not ssid:
            continue
        try:
            signal_i = int(signal)
        except ValueError:
            signal_i = 0
        entry = {
            "ssid": ssid,
            "signal": signal_i,
            "security": security,
            "active": active == "yes",
        }
        existing = best.get(ssid)
        if existing is None or signal_i > existing["signal"] or entry["active"]:
            best[ssid] = entry

    return sorted(best.values(), key=lambda e: (-e["active"], -e["signal"]))


def geolocate_country():
    """Best-effort IP-based country guess for country.py's "most likely"
    suggestions - returns the country name (matching country.py's own
    COUNTRIES list spelling) or None if the lookup fails for any reason
    (offline, API down, rate-limited, name doesn't match our list, ...).
    Blocking (network I/O) - callers run this off the GTK main thread.

    ip-api.com's free tier is plain HTTP (no HTTPS, no key) and permits
    unlimited non-commercial use, which is why it's used here (a one-off
    lookup per OOBE run isn't the kind of case that needs an API key)."""
    try:
        with urllib.request.urlopen("http://ip-api.com/json/?fields=status,country", timeout=4) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None
    if data.get("status") != "success":
        return None
    country = data.get("country")
    return country if isinstance(country, str) and country else None


def connect(ssid, password=None):
    argv = ["nmcli", "device", "wifi", "connect", ssid]
    if password:
        argv += ["password", password]
    result = _run(argv, timeout=30)
    if result is None:
        return False, "nmcli is not available"
    if result.returncode == 0:
        return True, None
    message = (result.stderr or result.stdout or "Connection failed").strip()
    return False, message
