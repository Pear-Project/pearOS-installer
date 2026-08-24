"""Port of app/js/i18n.js: dot-path string resolution from the JSON files in
app/i18n/, plus rebranding via osrelease.rebrand()."""
import json
import os
import re

from .osrelease import OS_RELEASE

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(_APP_DIR, "app", "i18n")

LOCALE_CODE_RE = re.compile(r"^[a-z]{2,3}_[A-Z]{2}$")


def list_languages():
    """Return [{code, displayName}] sorted by displayName, like list_languages()."""
    try:
        files = os.listdir(I18N_DIR)
    except OSError:
        files = []

    languages = []
    for f in files:
        if not f.endswith(".json"):
            continue
        code = f[:-5]
        if not LOCALE_CODE_RE.match(code):
            continue
        display_name = code
        try:
            with open(os.path.join(I18N_DIR, f), "r", encoding="utf-8") as fh:
                data = json.load(fh)
            meta = data.get("_meta") or {}
            if meta.get("displayName"):
                display_name = meta["displayName"]
        except (OSError, ValueError):
            pass
        languages.append({"code": code, "displayName": display_name})

    languages.sort(key=lambda l: l["displayName"].lower())
    return languages


class I18n:
    def __init__(self, lng="en_US"):
        self.lng = lng
        self.strings = {}
        self.load(lng)

    def load(self, lng):
        self.lng = lng
        path = os.path.join(I18N_DIR, lng + ".json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.strings = json.load(f)
        except (OSError, ValueError):
            self.strings = {}

    def get(self, key):
        node = self.strings
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return None
            node = node[part]
        return node

    def t(self, key, default=None):
        """Resolve + rebrand, with a fallback default (usually the English text
        already embedded in the page, mirroring how the HTML templates carried
        their own English fallback text before i18n.load() overwrote it)."""
        val = self.get(key)
        if val is None:
            val = default
        return OS_RELEASE.rebrand(val) if val is not None else val
