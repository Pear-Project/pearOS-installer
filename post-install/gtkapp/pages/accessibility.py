"""Accessibility: 4 categories (Vision/Motor/Hearing/Cognitive), matching
macOS's real layout - left-aligned icon+title+paragraph, then a row of 4
selectable category cards (not the plain toggle-button tabs this used to
have), each revealing that category's settings panel below the grid. The
button is labeled "Not Now" like the reference, since this screen has no
separate skip action - continuing past it already means "not now" for
whatever wasn't turned on.

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

from ..widgets import page_root
from .accessibility_icons import CategoryIcon, UniversalAccessIcon

CATEGORIES = ["Vision", "Motor", "Hearing", "Cognitive"]
_ICON_KINDS = {"Vision": "vision", "Motor": "motor", "Hearing": "hearing", "Cognitive": "cognitive"}

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (icon/title/paragraph/cards all started at x=73-77 in a 723-wide card,
# noticeably further left than migration_assistant.py/written_spoken.py's
# 159px - each of these detail screens apparently has its own margin in
# the real app, not one shared constant) and scaled to this app's
# 800-wide card (factor 799/723 ~= 1.105).
_LEFT_MARGIN = 81
_CARD_SIZE = 141
_CARD_GAP = 12


class AccessibilityPage:
    def __init__(self, app):
        self.app = app
        self._checks = {}

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        icon = UniversalAccessIcon(size=76)
        icon.set_halign(Gtk.Align.START)
        icon.set_margin_start(_LEFT_MARGIN)
        icon.set_margin_top(70)
        content.append(icon)

        self.title = Gtk.Label(label="Accessibility")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(24)
        content.append(self.title)

        self.description = Gtk.Label(
            label=(
                "Accessibility features adapt this pearOS Computer to your "
                "individual needs. You can turn them on now to help you "
                "finish setting up, and further customize them later in "
                "System Settings. See what's available in each of the "
                "categories below."
            )
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(8)
        self.description.set_max_width_chars(58)
        content.append(self.description)

        cards = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=_CARD_GAP)
        cards.set_halign(Gtk.Align.START)
        cards.set_margin_start(_LEFT_MARGIN)
        cards.set_margin_top(26)
        content.append(cards)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_halign(Gtk.Align.START)
        self.stack.set_margin_start(_LEFT_MARGIN)
        self.stack.set_margin_top(20)
        content.append(self.stack)

        self._card_boxes = {}
        first = None
        for name in CATEGORIES:
            card = self._make_card(name)
            click = Gtk.GestureClick()
            click.connect("released", self._on_card_clicked, name)
            card.add_controller(click)
            cards.append(card)
            self._card_boxes[name] = card
            if first is None:
                first = name

        self.stack.add_named(self._build_vision(), "Vision")
        self.stack.add_named(self._build_motor(), "Motor")
        self.stack.add_named(self._build_hearing(), "Hearing")
        self.stack.add_named(self._build_cognitive(), "Cognitive")

        self._select_card(first)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Not Now"
        )

    def _make_card(self, name):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box.add_css_class("accessibility-card")
        box.set_size_request(_CARD_SIZE, _CARD_SIZE)
        box.set_halign(Gtk.Align.CENTER)
        box.set_valign(Gtk.Align.CENTER)

        icon = CategoryIcon(_ICON_KINDS[name], size=40)
        icon.set_halign(Gtk.Align.CENTER)
        icon.set_margin_top(14)
        box.append(icon)

        label = Gtk.Label(label=name)
        label.add_css_class("accessibility-card-label")
        box.append(label)
        return box

    def _select_card(self, name):
        for n, box in self._card_boxes.items():
            if n == name:
                box.add_css_class("selected")
            else:
                box.remove_css_class("selected")
        self.stack.set_visible_child_name(name)

    def _on_card_clicked(self, _gesture, _n_press, _x, _y, name):
        self._select_card(name)

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
