"""Dot-path string resolution from app/i18n/*.json, plus rebranding via
osrelease.rebrand() - same convention as post-install's i18n.py, sized down
for this app's 3 locales (en/ro/cs) instead of a large discoverable set."""
import json
import os

from .osrelease import OS_RELEASE

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(_APP_DIR, "app", "i18n")

LOCALES = ["en", "ro", "cs"]


class I18n:
    def __init__(self, lng="en"):
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
        val = self.get(key)
        if val is None:
            val = default
        return OS_RELEASE.rebrand(val) if val is not None else val

    def read_text_asset(self, filename):
        """Reads a plain-text asset referenced from the locale JSON (e.g. the
        EULA body, too large/awkward to inline as a JSON string value)."""
        path = os.path.join(I18N_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            return ""
