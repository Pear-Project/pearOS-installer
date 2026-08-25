"""Port of page_confirm.html: a 4-tab carousel (welcome / empty spacer /
EULA / disk-select), movement.js-style (prev/next disable at the first/last
tab).

Originally unreachable from the main navigation graph (matching the
original Electron app, where nothing linked here either) - now deliberately
linked from menu.py's "Install" action/Continue, per explicit user request:
Install -> this page's welcome/EULA/disk-select flow -> disk tab's own
Continue launches Calamares. Still also reachable via the dev QA-start
override for direct-to-tab testing.

Two further deliberate departures from a byte-literal port, both confirmed
with the user:
- The disk-select tab now lists real disks (disk_backend.py) instead of
  being empty dead markup.
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

from .. import disk_backend, disk_utility_backend, installer_backend
from ..widgets import make_card, centered_overlay, make_text_nav_button, load_scaled_picture
from ..navbar import Navbar

_EULA_FILES = {"en": "eula_en.txt", "ro": "eula_en.txt", "cs": "eula_cs.txt"}


class ConfirmPage:
    def __init__(self, app):
        self.app = app
        self._tab_index = 0
        self._selected_disk = None
        self._disk_buttons = []

        card = make_card(800, 600, "app")

        self.stack = Gtk.Stack()
        self.stack.set_vexpand(True)
        self.stack.set_transition_type(Gtk.StackTransitionType.NONE)

        self.stack.add_named(self._build_welcome_tab(), "welcome")
        self.stack.add_named(Gtk.Box(), "spacer")
        self.stack.add_named(self._build_eula_tab(), "eula")
        self.stack.add_named(self._build_disk_tab(), "disk")
        self._tab_names = ["welcome", "spacer", "eula", "disk"]

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

    def _build_disk_tab(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_valign(Gtk.Align.CENTER)
        box.set_vexpand(True)
        logo = load_scaled_picture("nicec0re-logo.png", 200)
        box.append(logo)
        self.disk_title = Gtk.Label(label="pearOS NiceC0re")
        self.disk_title.add_css_class("title")
        box.append(self.disk_title)
        self.disk_text = Gtk.Label(label="")
        self.disk_text.add_css_class("setup-text")
        self.disk_text.set_wrap(True)
        box.append(self.disk_text)

        self.disk_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        self.disk_row.set_halign(Gtk.Align.CENTER)
        self.disk_row.set_margin_top(20)
        box.append(self.disk_row)

        # Shown instead of disk_row when Disk Utility already made the
        # choice (disk_utility_backend.has_pending_choice()) - nothing left
        # to pick here, just a confirmation of what was already decided.
        self.disk_utility_summary_label = Gtk.Label(label="")
        self.disk_utility_summary_label.add_css_class("setup-text")
        self.disk_utility_summary_label.set_wrap(True)
        self.disk_utility_summary_label.set_margin_top(20)
        self.disk_utility_summary_label.set_visible(False)
        box.append(self.disk_utility_summary_label)
        return box

    def _load_disks(self):
        # Disk Utility already picked (and validated) a disk + action -
        # nothing to re-pick here, just show what was decided.
        if disk_utility_backend.has_pending_choice():
            choice = disk_utility_backend.get_pending_choice()
            i18n = self.app.i18n_for(self.app.current_locale)
            self.disk_row.set_visible(False)
            self.disk_utility_summary_label.set_visible(True)
            self.disk_utility_summary_label.set_label(
                i18n.t(
                    "confirm.disk.disk_utility_summary",
                    "Ready to install ({choice}) on {device}",
                ).format(
                    choice=choice.get("installChoice", "?"),
                    device=choice.get("deviceName") or choice.get("device", "?"),
                )
            )
            return

        self.disk_row.set_visible(True)
        self.disk_utility_summary_label.set_visible(False)

        for child in self._disk_buttons:
            self.disk_row.remove(child)
        self._disk_buttons = []
        self._selected_disk = None

        disks = disk_backend.list_disks()
        for disk in disks:
            btn = Gtk.Button()
            btn.add_css_class("flat")
            btn.add_css_class("disk-button")
            btn.set_size_request(150, 200)
            col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            col.set_valign(Gtk.Align.CENTER)
            pic = load_scaled_picture("disk.png", 60)
            col.append(pic)
            label = Gtk.Label(label=f"{disk['model']}\n{disk['size']}")
            label.add_css_class("disk-title")
            label.set_justify(Gtk.Justification.CENTER)
            col.append(label)
            btn.set_child(col)
            btn.connect("clicked", lambda _b, d=disk, b=btn: self._select_disk(d, b))
            self.disk_row.append(btn)
            self._disk_buttons.append(btn)

    def _select_disk(self, disk, btn):
        self._selected_disk = disk
        for b in self._disk_buttons:
            b.remove_css_class("selected")
        btn.add_css_class("selected")

    def on_show(self):
        i18n = self.app.i18n_for(self.app.current_locale)
        self.welcome_title.set_label(i18n.t("confirm.welcome.title", "pearOS NiceC0re"))
        self.welcome_text.set_label(i18n.t("confirm.welcome.text", ""))
        self.eula_title.set_label(i18n.t("confirm.eula.title", "Terms and Conditions"))
        self.eula_desc.set_label(i18n.t("confirm.eula.description", ""))
        eula_file = _EULA_FILES.get(self.app.current_locale, "eula_en.txt")
        self.eula_buffer.set_text(i18n.read_text_asset(eula_file))
        self.disk_title.set_label(i18n.t("confirm.disk.title", "pearOS NiceC0re"))
        self.disk_text.set_label(i18n.t("confirm.disk.text", ""))
        self.back_btn.set_label(i18n.t("confirm.back", "Back"))
        self.forward_btn.set_label(i18n.t("confirm.continue", "Continue"))
        self.welcome_continue_btn.set_label(i18n.t("confirm.continue", "Continue"))

        # Dev/QA only, mirrors GTKAPP_QA_START: jump straight to one of
        # this page's own 4 tabs instead of clicking Continue through them.
        qa_tab = os.environ.get("GTKAPP_QA_CONFIRM_TAB")
        start_index = int(qa_tab) if qa_tab is not None else 0

        self._tab_index = start_index
        self.stack.set_visible_child_name(self._tab_names[start_index])
        self._update_footer()
        self._load_disks()

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
        elif disk_utility_backend.has_pending_choice():
            # Disk Utility already validated a choice on a live, minimized
            # Calamares - continue driving that same session through to a
            # real install instead of starting a separate one.
            self.app.go_to("progress")
            disk_utility_backend.proceed_with_install(
                on_progress=self._on_install_progress,
                on_finished=self._on_install_finished,
                on_failed=self._on_install_failed,
                on_stuck=self._on_install_stuck,
            )
        else:
            installer_backend.launch_install(disk=self._selected_disk)

    def _progress_page(self):
        return self.app.pages["progress"]

    def _on_install_progress(self, percent, label):
        self._progress_page().update_progress(percent * 100.0, label or None)

    def _on_install_finished(self):
        self._progress_page().show_finished()

    def _on_install_failed(self, message, details):
        self._progress_page().show_failed(message or details or "")

    def _on_install_stuck(self):
        # Something on a locale/keyboard/summary page needs real
        # interaction that couldn't happen while Calamares was hidden -
        # its window has already been restored by disk_utility_backend at
        # this point, so surface that instead of leaving our own progress
        # page looking stalled with no explanation.
        i18n = self.app.i18n_for(self.app.current_locale)
        self._progress_page().show_failed(
            i18n.t(
                "progress.stuck",
                "Calamares needs your attention - its window has been restored, please continue there.",
            )
        )
