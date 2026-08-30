"""Screen Time: matches macOS's real Setup Assistant layout - left-
aligned title/paragraph followed by four icon+bold-title+description
rows (Weekly Reports / Downtime and App Limits / Content & Privacy
Restrictions / Screen Time Passcode), measured off a real screenshot of
this exact page. Same icon+label+value row shape as written_spoken.py's
_SummaryRow, just with a wrapping multi-line value instead of a single-
line one. 'Set Up Later' sits left of 'Continue' like pearid.py's own
skip button.

This page runs as the live 'default' user, before the real account
exists, so it can't actually install/start the collector here - see
first_login_assets/ - it only persists the on/off choice; post_setup
drops the collector/KWin-script/systemd-unit files into the real user's
home and schedules activation for that user's first login, same handoff
as the theme switch."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root
from .screen_time_icons import ClockIcon, HourglassIcon, NoEntryIcon, PasscodeGridIcon

_LEFT_MARGIN = 176


class _FeatureRow:
    def __init__(self, icon_widget, title_text, desc_text):
        self.widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        icon_widget.set_valign(Gtk.Align.START)
        icon_widget.set_margin_top(2)
        self.widget.append(icon_widget)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        text_box.set_valign(Gtk.Align.CENTER)
        self.label = Gtk.Label(label=title_text)
        self.label.add_css_class("summary-row-label")
        self.label.set_halign(Gtk.Align.START)
        text_box.append(self.label)

        self.value = Gtk.Label(label=desc_text)
        self.value.add_css_class("summary-row-value")
        self.value.set_halign(Gtk.Align.START)
        self.value.set_wrap(True)
        self.value.set_justify(Gtk.Justification.LEFT)
        self.value.set_max_width_chars(52)
        text_box.append(self.value)

        self.widget.append(text_box)


class ScreenTimePage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        self.title = Gtk.Label(label="Screen Time")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(73)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Get a weekly report with insights about your screen time, "
                "and set time limits for apps and websites you want to "
                "manage. Adults can also set parental controls for a "
                "child's device."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(8)
        self.description.set_max_width_chars(52)
        content.append(self.description)

        rows_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        rows_box.set_halign(Gtk.Align.START)
        rows_box.set_margin_start(_LEFT_MARGIN)
        rows_box.set_margin_top(24)
        content.append(rows_box)

        rows = (
            _FeatureRow(
                HourglassIcon(size=24),
                "Weekly Reports",
                "View daily and weekly charts and get insights about your "
                "screen time.",
            ),
            _FeatureRow(
                ClockIcon(size=24),
                "Downtime and App Limits",
                "Schedule time away from the screen and set daily time "
                "limits for apps or app categories.",
            ),
            _FeatureRow(
                NoEntryIcon(size=24),
                "Content & Privacy Restrictions",
                "Restrict settings for contacts, explicit content, "
                "purchases and downloads, and privacy.",
            ),
            _FeatureRow(
                PasscodeGridIcon(size=24),
                "Screen Time Passcode",
                "Manage screen time for children from your Mac or iOS "
                "device, or use a screen time passcode on your child's "
                "device.",
            ),
        )
        for row in rows:
            rows_box.append(row.widget)

        self.widget, self.card = page_root(
            content,
            on_back=self._on_back,
            on_forward=self._on_continue,
            forward_label="Continue",
        )

        self.later_btn = Gtk.Button(label="Set Up Later")
        self.later_btn.add_css_class("nav-button")
        self.later_btn.set_halign(Gtk.Align.END)
        self.later_btn.set_valign(Gtk.Align.END)
        self.later_btn.set_margin_end(145)
        self.later_btn.set_margin_bottom(20)
        self.later_btn.connect("clicked", self._on_later_clicked)
        self.card.overlay.add_overlay(self.later_btn)

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("analytics")

    def _on_later_clicked(self, _btn):
        self.app.state.save_screentime(False)
        self.app.go_to("piri")

    def _on_continue(self):
        self.app.state.save_screentime(True)
        self.app.go_to("piri")
