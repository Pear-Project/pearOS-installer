"""Port of page_examining.html: a 2-second fake spinner (examine.js's whole
job is a single setTimeout, no real disk probing happens here) that
auto-advances to the recovery menu. Both nav buttons are disabled/dead in
the original (hardcoded `disabled` attribute, not driven by movement.js's
tab-boundary logic - there's only one tab on this page)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from ..widgets import make_card, centered_overlay, ArrowButton
from ..navbar import Navbar
from ..spinner_widget import SpinnerWidget

_EXAMINE_DELAY_MS = 2000


class ExaminingPage:
    def __init__(self, app):
        self.app = app

        card = make_card(800, 600, "app")
        card.add_css_class("page-install-wrapper")

        # .middle is position:absolute in the original, which takes it out
        # of normal flow - the h1 is the *first normal-flow* element in
        # the card underneath it, so it lands at the top (default h1
        # margin-top:20px), not the bottom.
        self.title = Gtk.Label(label="pearOS Recovery")
        self.title.add_css_class("examining-title")
        self.title.set_halign(Gtk.Align.CENTER)
        self.title.set_valign(Gtk.Align.START)
        self.title.set_margin_top(20)
        card.append(self.title)

        middle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        middle.set_halign(Gtk.Align.CENTER)
        middle.set_valign(Gtk.Align.CENTER)
        middle.set_vexpand(True)

        self.spinner = SpinnerWidget(size=25)
        self.spinner.set_halign(Gtk.Align.CENTER)
        middle.append(self.spinner)

        self.status_label = Gtk.Label(label="Examining volumes...")
        self.status_label.add_css_class("examining-status")
        middle.append(self.status_label)
        card.append(middle)

        # Both arrows live inside the card, right under the (vexpand)
        # middle box - not floated over the whole window, which stranded
        # them away from the card once it stopped filling the window
        # height (same fix as language.py's forward arrow).
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer.set_halign(Gtk.Align.CENTER)
        footer.set_margin_bottom(16)
        back_btn = ArrowButton(rotate_180=True)
        back_btn.set_sensitive(False)
        footer.append(back_btn)
        forward_btn = ArrowButton()
        forward_btn.set_sensitive(False)
        footer.append(forward_btn)
        card.append(footer)

        overlay = centered_overlay(card)

        self.navbar = Navbar(app, app.quit)
        self.navbar.set_app_name("Recovery")
        overlay.add_overlay(self.navbar)

        self.widget = overlay
        self._advanced = False

    def on_show(self):
        self._advanced = False
        self.spinner.start()
        i18n = self.app.i18n_for(self.app.current_locale)
        self.title.set_label(i18n.t("examining.title", "pearOS Recovery"))
        self.status_label.set_label(i18n.t("examining.status", "Examining volumes..."))
        GLib.timeout_add(_EXAMINE_DELAY_MS, self._advance)

    def _advance(self):
        if not self._advanced:
            self._advanced = True
            self.app.go_to("menu")
        return False
