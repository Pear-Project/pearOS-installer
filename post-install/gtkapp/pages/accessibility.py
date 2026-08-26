"""Accessibility: 4 categories (Vision/Motor/Hearing/Cognitive).

This page runs as the live 'default' user, before the real account exists
(useradd happens near the end of post_setup) - so it can't apply these
settings live (kwriteconfig6/xkbset would land on 'default' and be lost
when that account is deleted on next boot). It only collects the choice;
post_setup applies it for the real username afterwards (kdeglobals/
kcminputrc directly, xkbset AccessX controls on the new user's first login,
since those need a live X11 session - see post_setup's apply-first-*.sh)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import page_root, make_title

CATEGORIES = ["Vision", "Motor", "Hearing", "Cognitive"]


class AccessibilityPage:
    def __init__(self, app):
        self.app = app
        self._checks = {}

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Accessibility")
        content.append(self.title)

        tabs = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        tabs.set_halign(Gtk.Align.CENTER)
        tabs.set_margin_top(6)
        tabs.set_margin_bottom(10)
        content.append(tabs)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_halign(Gtk.Align.CENTER)
        content.append(self.stack)

        self._tab_buttons = {}
        first = None
        for name in CATEGORIES:
            btn = Gtk.ToggleButton(label=name)
            btn.add_css_class("nav-button")
            if first is None:
                first = btn
            else:
                btn.set_group(first)
            btn.connect("toggled", self._on_tab_toggled, name)
            tabs.append(btn)
            self._tab_buttons[name] = btn

        self.stack.add_named(self._build_vision(), "Vision")
        self.stack.add_named(self._build_motor(), "Motor")
        self.stack.add_named(self._build_hearing(), "Hearing")
        self.stack.add_named(self._build_cognitive(), "Cognitive")

        first.set_active(True)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def _panel(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.set_size_request(400, 140)
        return box

    def _check_row(self, box, key, label_text, default=False):
        check = Gtk.CheckButton(label=label_text)
        check.set_active(default)
        box.append(check)
        self._checks.setdefault(key, []).append(check)
        return check

    def _build_vision(self):
        box = self._panel()
        self._check_row(box, "reduce_motion", "Reduce Motion")
        self._check_row(box, "increase_contrast", "Increase Contrast")
        self._check_row(box, "larger_cursor", "Larger Cursor")
        return box

    def _build_motor(self):
        box = self._panel()
        self._check_row(box, "sticky_keys", "Sticky Keys")
        self._check_row(box, "slow_keys", "Slow Keys")
        self._check_row(box, "bounce_keys", "Bounce Keys")
        self._check_row(box, "mouse_keys", "Mouse Keys")
        return box

    def _build_hearing(self):
        box = self._panel()
        self._check_row(box, "audible_bell", "Play Alert Sound (Audible Bell)", default=True)
        return box

    def _build_cognitive(self):
        box = self._panel()
        note = Gtk.Label(label="Reduce visual motion to make the interface calmer.")
        note.add_css_class("description")
        note.set_wrap(True)
        box.append(note)
        # Same underlying setting as the Vision tab (legitimately relevant
        # here too), tracked as a second checkbox under the same key so
        # either one turning it on is enough - see _on_continue().
        self._check_row(box, "reduce_motion", "Reduce Motion")
        return box

    def _on_tab_toggled(self, btn, name):
        if btn.get_active():
            self.stack.set_visible_child_name(name)

    def on_show(self):
        self.title.set_label(self.app.t("accessibility.title", "Accessibility"))

    def _on_back(self):
        self.app.go_to("written_spoken")

    def _on_continue(self):
        prefs = {
            key: any(c.get_active() for c in checks)
            for key, checks in self._checks.items()
        }
        self.app.state.save_accessibility(prefs)
        self.app.go_to("data_privacy")
