"""Port of app/js/os-release.js: read /etc/os-release at runtime so the UI
shows the real installed distro name instead of a hardcoded one."""
import re

_LEGACY_NAME_PATTERN = re.compile(r"pearOS\s+NiceC0re")

_PATHS = ["/etc/os-release", "/usr/lib/os-release"]


def _parse_os_release(content):
    data = {}
    for line in content.split("\n"):
        m = re.match(r"^([A-Z_]+)=(.*)$", line)
        if not m:
            continue
        value = m.group(2).strip()
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        data[m.group(1)] = value
    return data


def _read_os_release():
    for path in _PATHS:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return _parse_os_release(f.read())
        except OSError:
            continue
    return {}


class _OSRelease:
    def __init__(self):
        raw = _read_os_release()
        self.id = raw.get("ID", "pearos")
        self.name = raw.get("NAME", "pearOS")
        self.pretty_name = raw.get("PRETTY_NAME", raw.get("NAME", "pearOS"))
        self.version = raw.get("VERSION", "")
        self.version_codename = raw.get("VERSION_CODENAME", "")
        self.build_id = raw.get("BUILD_ID", "")
        self.image_id = raw.get("IMAGE_ID", "")
        self.image_version = raw.get("IMAGE_VERSION", "")
        self.logo = raw.get("LOGO", "")
        self.home_url = raw.get("HOME_URL", "")
        self.documentation_url = raw.get("DOCUMENTATION_URL", "")
        self.support_url = raw.get("SUPPORT_URL", "")
        self.bug_report_url = raw.get("BUG_REPORT_URL", "")

    def rebrand(self, text):
        if not isinstance(text, str):
            return text
        return _LEGACY_NAME_PATTERN.sub(self.pretty_name, text)


OS_RELEASE = _OSRelease()
