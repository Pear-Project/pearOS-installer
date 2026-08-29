"""'Data & Privacy' - matches macOS's real layout: icon slightly left of
center above a left-aligned title/paragraphs block, plus a "Learn More..."
link with a small info icon - measured off a real screenshot of this
exact page. Informational screen (matches the real macOS Setup Assistant
step of the same name): explains what leaves the device and why, no
toggles here (those live on the later Location Services / Analytics
pages) - just acknowledgement + Continue. "Learn More..." has nowhere
real to link to yet (no privacy-policy page exists in this app), so it's
inert for now - matches how touchid_setup.py etc handle not-yet-real
features, not a broken link."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..osrelease import OS_RELEASE
from ..widgets import page_root
from .privacy_icon import InfoIcon, PrivacyIcon

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (text column started at x=159 in a 723-wide card, same as
# migration_assistant.py/written_spoken.py) and scaled to this app's
# 800-wide card (factor 799/723 ~= 1.105).
_LEFT_MARGIN = 176
# The icon's own center measured ~41px left of the card's true center in
# the same reference (320 vs 361.5 in the 723-wide crop) - the same kind
# of off-center icon placement already measured and reproduced on
# country.py, scaled the same way.
_ICON_MARGIN_END = 90

PARAGRAPHS = [
    "This icon appears when a {name} feature asks to use your personal information.",
    "You won't see this with every feature since {name} collects this "
    "information only when needed to enable features, secure our "
    "services, or personalize your experience.",
    "{name} believes privacy is a fundamental human right, so every "
    "{name} product is designed to minimize the collection and use of "
    "your data, use on-device processing whenever possible, and provide "
    "transparency and control over your information.",
]


class DataPrivacyPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = PrivacyIcon(size=76)
        icon.set_halign(Gtk.Align.CENTER)
        icon.set_margin_top(70)
        icon.set_margin_end(_ICON_MARGIN_END)
        content.append(icon)

        self.title = Gtk.Label(label="Data & Privacy")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        name = OS_RELEASE.rebrand(OS_RELEASE.pretty_name)
        paragraphs_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        paragraphs_box.set_halign(Gtk.Align.START)
        paragraphs_box.set_margin_start(_LEFT_MARGIN)
        paragraphs_box.set_margin_top(8)
        for text in PARAGRAPHS:
            label = Gtk.Label(label=text.format(name=name))
            label.add_css_class("description")
            label.set_wrap(True)
            label.set_justify(Gtk.Justification.LEFT)
            label.set_halign(Gtk.Align.START)
            label.set_max_width_chars(56)
            paragraphs_box.append(label)
        content.append(paragraphs_box)

        learn_more = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        learn_more.set_halign(Gtk.Align.START)
        learn_more.set_margin_start(_LEFT_MARGIN)
        learn_more.set_margin_top(14)
        info_icon = InfoIcon(size=14)
        info_icon.set_valign(Gtk.Align.CENTER)
        learn_more.append(info_icon)
        link_label = Gtk.Label(label="Learn More...")
        link_label.add_css_class("privacy-learn-more")
        learn_more.append(link_label)
        content.append(learn_more)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("accessibility")

    def _on_continue(self):
        self.app.go_to("pearid")
