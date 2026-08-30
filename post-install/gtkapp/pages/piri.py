"""Piri: matches macOS's real "Apple Intelligence" Setup Assistant screen,
rebranded - gradient app-tile icon with a BETA badge, title/paragraph,
three icon+bold-title+description feature rows, an "About Piri &
Privacy..." link, and 'Set Up Later' / 'Set Up Piri' buttons in opposite
bottom corners (same shape as touchid_enable.py's own skip button).
Persists the real show_icon flag (piri_backend.py) - the actual
speech-model download happens on first real login, not during the
wizard (see piri_backend.py's docstring for why)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import piri_backend as backend
from ..osrelease import OS_RELEASE
from ..widgets import page_root
from .piri_icons import LockIcon, OrbitIcon, PiriAppIcon, SparkleIcon
from .privacy_icon import InfoIcon

_LEFT_MARGIN = 176


class _FeatureRow:
    def __init__(self, icon_widget, title_text, desc_text):
        self.widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        icon_widget.set_valign(Gtk.Align.START)
        icon_widget.set_margin_top(2)
        self.widget.append(icon_widget)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        text_box.set_valign(Gtk.Align.CENTER)
        label = Gtk.Label(label=title_text)
        label.add_css_class("summary-row-label")
        label.set_halign(Gtk.Align.START)
        text_box.append(label)

        value = Gtk.Label(label=desc_text)
        value.add_css_class("summary-row-value")
        value.set_halign(Gtk.Align.START)
        value.set_wrap(True)
        value.set_justify(Gtk.Justification.LEFT)
        value.set_max_width_chars(52)
        text_box.append(value)

        self.widget.append(text_box)


class PiriPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = PiriAppIcon(size=64)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(60)
        content.append(icon)

        self.title = Gtk.Label(label="Piri")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(20)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Intelligence that understands your personal context. "
                "Connect to Wi-Fi and power to prepare for Piri."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(6)
        self.description.set_max_width_chars(52)
        content.append(self.description)

        rows_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        rows_box.set_halign(Gtk.Align.START)
        rows_box.set_margin_start(_LEFT_MARGIN)
        rows_box.set_margin_top(18)
        content.append(rows_box)

        rows = (
            _FeatureRow(
                SparkleIcon(size=24),
                "New Ways to Express Yourself",
                "Enhance your writing, create personalized images, and "
                "express yourself in more ways than ever.",
            ),
            _FeatureRow(
                OrbitIcon(size=24),
                "The Start of a New Era for Piri",
                "Piri is more natural, contextually relevant, and "
                "personal to you.",
            ),
            _FeatureRow(
                LockIcon(size=24),
                "Built for Privacy",
                "Powerful intelligence without sharing your data with "
                f"{OS_RELEASE.rebrand(OS_RELEASE.pretty_name)}.",
            ),
        )
        for row in rows:
            rows_box.append(row.widget)

        link_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        link_row.set_halign(Gtk.Align.START)
        link_row.set_margin_start(_LEFT_MARGIN)
        link_row.set_margin_top(20)
        info_icon = InfoIcon(size=14)
        info_icon.set_valign(Gtk.Align.CENTER)
        link_row.append(info_icon)
        link_label = Gtk.Label(label="About Piri & Privacy...")
        link_label.add_css_class("privacy-learn-more")
        link_row.append(link_label)
        content.append(link_row)

        self.widget, self.card = page_root(
            content,
            on_back=self._on_back,
            on_forward=self._on_continue,
            forward_label="Set Up Piri",
        )

        self.later_btn = Gtk.Button(label="Set Up Later")
        self.later_btn.add_css_class("nav-button")
        self.later_btn.set_halign(Gtk.Align.START)
        self.later_btn.set_valign(Gtk.Align.END)
        self.later_btn.set_margin_start(20)
        self.later_btn.set_margin_bottom(20)
        self.later_btn.connect("clicked", self._on_later_clicked)
        self.card.overlay.add_overlay(self.later_btn)

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("screen_time")

    def _on_later_clicked(self, _btn):
        backend.set_enabled(False)
        self.app.go_to("look")

    def _on_continue(self):
        backend.set_enabled(True)
        self.app.go_to("look")
