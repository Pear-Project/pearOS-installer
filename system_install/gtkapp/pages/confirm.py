"""Port of page_confirm.html: a welcome + EULA carousel, movement.js-style
(prev/next disable at the first/last tab).

Originally unreachable from the main navigation graph (matching the
original Electron app, where nothing linked here either) - now deliberately
linked from menu.py's "Install" action/Continue, per explicit user request:
Install -> this page's welcome/EULA flow -> Continue launches Calamares,
which does its own disk selection internally. Still also reachable via the
dev QA-start override for direct-to-tab testing.

Three further deliberate departures from a byte-literal port, all confirmed
with the user:
- The original's "empty spacer" tab (dead markup even in the original) and
  its own dead disk-select tab (page2.html never existed) are both dropped
  from navigation entirely - Continue on the EULA now goes straight to
  Calamares, which handles disk selection itself; a separate picker here
  would just be redundant/inconsistent with whatever the user actually
  does inside Calamares.
- Continue on the last tab calls installer_backend.launch_install() instead
  of the original's link to a nonexistent page2.html.

Back always returns to "menu" (where this page is now actually entered
from), not to a `.pop()` through the tab carousel - matches the original's
own onclick behavior of jumping straight to one fixed destination
regardless of the active tab, just updated to the new real entry point
instead of the original's language-select target (which only made sense
when this page had no real caller).
"""
import os

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .. import installer_backend
from ..widgets import make_card, centered_overlay, make_text_nav_button, load_scaled_picture
from ..navbar import Navbar

_EULA_FILES = {"en": "eula_en.txt", "ro": "eula_en.txt", "cs": "eula_cs.txt"}


class ConfirmPage:
    def __init__(self, app):
        self.app = app
        self._tab_index = 0

        card = make_card(800, 600, "app")

        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_transition_type(Gtk.StackTransitionType.NONE)

        self.stack.add_named(self._build_welcome_tab(), "welcome")
        self.stack.add_named(self._build_eula_tab(), "eula")
        self._tab_names = ["welcome", "eula"]

        card.append(self.stack)

        # Shared footer (divider + Back/Continue) - real macOS Setup
        # Assistant/Installer only uses this multi-step footer from the
        # second screen onward; the very first "welcome" screen has no
        # Back (nothing to go back to yet) and a single centered accent
        # button instead of a bottom-right pill, no divider. Toggled by
        # tab index in _update_footer().
        # Footer vertical margins measured directly against a real
        # screenshot (divider sat 24px too high without these bumps -
        # confirmed by a pixel-diff scan, not eyeballed).
        self.footer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        divider = Gtk.Separator()
        divider.set_margin_top(16)
        self.footer.append(divider)

        buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        buttons.set_halign(Gtk.Align.END)
        buttons.set_margin_top(20)
        buttons.set_margin_end(20)
        buttons.set_margin_bottom(32)
        self.back_btn = make_text_nav_button("Back", on_click=self._on_back)
        self.forward_btn = make_text_nav_button("Continue", on_click=self._on_forward, primary=True)
        buttons.append(self.back_btn)
        buttons.append(self.forward_btn)
        self.footer.append(buttons)
        card.append(self.footer)

        overlay = centered_overlay(card)
        self.navbar = Navbar(app, app.quit)
        overlay.add_overlay(self.navbar)

        self.widget = overlay

    def _build_welcome_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_valign(Gtk.Align.CENTER)
        box.set_vexpand(True)
        logo = load_scaled_picture("nicec0re-logo.png", 350)
        box.append(logo)
        self.welcome_title = Gtk.Label(label="pearOS NiceC0re")
        self.welcome_title.add_css_class("title")
        self.welcome_title.add_css_class("welcome-title")
        box.append(self.welcome_title)
        self.welcome_text = Gtk.Label(label="")
        self.welcome_text.add_css_class("setup-text")
        self.welcome_text.set_wrap(True)
        box.append(self.welcome_text)

        self.welcome_continue_btn = Gtk.Button(label="Continue")
        self.welcome_continue_btn.add_css_class("welcome-continue-button")
        self.welcome_continue_btn.set_halign(Gtk.Align.CENTER)
        self.welcome_continue_btn.set_margin_top(16)
        self.welcome_continue_btn.connect("clicked", lambda _b: self._on_forward())
        box.append(self.welcome_continue_btn)
        return box

    def _build_eula_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_margin_top(8)
        self.eula_title = Gtk.Label(label="Terms and Conditions")
        self.eula_title.add_css_class("title")
        box.append(self.eula_title)
        self.eula_desc = Gtk.Label(label="")
        self.eula_desc.add_css_class("eula-description")
        self.eula_desc.set_wrap(True)
        self.eula_desc.set_justify(Gtk.Justification.CENTER)
        box.append(self.eula_desc)

        scroller = Gtk.ScrolledWindow()
        scroller.set_min_content_width(640)
        scroller.set_min_content_height(300)
        scroller.set_margin_top(8)
        textview = Gtk.TextView()
        textview.add_css_class("license-text")
        textview.set_editable(False)
        textview.set_cursor_visible(False)
        textview.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        textview.set_left_margin(8)
        textview.set_right_margin(8)
        self.eula_buffer = textview.get_buffer()
        scroller.set_child(textview)
        box.append(scroller)
        return box

    def on_show(self):
        i18n = self.app.i18n_for(self.app.current_locale)
        self.welcome_title.set_label(i18n.t("confirm.welcome.title", "pearOS NiceC0re"))
        self.welcome_text.set_label(i18n.t("confirm.welcome.text", ""))
        self.eula_title.set_label(i18n.t("confirm.eula.title", "Terms and Conditions"))
        self.eula_desc.set_label(i18n.t("confirm.eula.description", ""))
        eula_file = _EULA_FILES.get(self.app.current_locale, "eula_en.txt")
        self.eula_buffer.set_text(i18n.read_text_asset(eula_file))
        self.back_btn.set_label(i18n.t("confirm.back", "Back"))
        self.forward_btn.set_label(i18n.t("confirm.continue", "Continue"))
        self.welcome_continue_btn.set_label(i18n.t("confirm.continue", "Continue"))

        # Dev/QA only, mirrors GTKAPP_QA_START: jump straight to one of
        # this page's own tabs instead of clicking Continue through them.
        qa_tab = os.environ.get("GTKAPP_QA_CONFIRM_TAB")
        start_index = int(qa_tab) if qa_tab is not None else 0

        self._tab_index = start_index
        self.stack.set_visible_child_name(self._tab_names[start_index])
        self._update_footer()

    def _update_footer(self):
        # Tab 0 (welcome): single centered accent button, no Back, no
        # divider - matches the real macOS first-run screen. Every other
        # tab keeps the shared Back/Continue footer.
        on_welcome = self._tab_index == 0
        self.footer.set_visible(not on_welcome)
        self.welcome_continue_btn.set_visible(on_welcome)
        self.back_btn.set_sensitive(self._tab_index > 0)
        self.forward_btn.set_sensitive(True)

    def _on_back(self):
        # Always exits to menu, on every tab - see module docstring.
        self.app.go_to("menu")

    def _on_forward(self):
        if self._tab_index < len(self._tab_names) - 1:
            self._tab_index += 1
            self.stack.set_visible_child_name(self._tab_names[self._tab_index])
            self._update_footer()
        else:
            # Calamares does its own disk selection internally - no need
            # for a separate picker here.
            installer_backend.launch_install()
