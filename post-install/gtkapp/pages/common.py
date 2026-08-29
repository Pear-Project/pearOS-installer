"""Shared bits for the three list-based pages (language/keymap/timezone),
which all reproduce the same `.list` <select size=9> markup."""
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Pango", "1.0")
from gi.repository import Gtk, Pango

# Sentinel used as the "value" of a separator entry in a SelectList's items
# (e.g. country.py's suggested-countries-then-divider-then-everything-else
# layout) - rendered as a plain rule, not selectable/activatable, and
# skipped by selected_value()/selected_text() the same way any other
# non-selected index would be.
SEPARATOR = object()

def _selected_attrs():
    attrs = Pango.AttrList.new()
    attrs.insert(Pango.attr_foreground_new(0xFFFF, 0xFFFF, 0xFFFF))
    attrs.insert(Pango.attr_weight_new(Pango.Weight.BOLD))
    return attrs


def make_worldmap():
    # macOS's own "Select Your Country or Region" glyph is a circle outline
    # with continent silhouettes inside - "globe-symbolic" (shipped by the
    # breeze icon theme this OS already depends on) is the closest match
    # available without commissioning new vector art: same circle+continents
    # composition, unlike the flat 2-tone raster globe this used to be.
    # Symbolic icons render in whatever color is set on them, so the blue
    # tint comes from the "globe-icon" CSS class, not the icon data itself.
    icon = Gtk.Image.new_from_icon_name("globe-symbolic")
    icon.set_pixel_size(76)
    icon.add_css_class("globe-icon")

    box = Gtk.Box()
    box.set_halign(Gtk.Align.CENTER)
    box.set_margin_top(55)
    # Measured off the reference screenshot: the globe glyph's center sits
    # ~5% of the card's width left of true center (icon bbox center 325 vs
    # card center 361.5 in a 723-wide reference card), not dead-centered -
    # reproduced here via asymmetric margins so centering still shifts left
    # by the same fraction on this card's width.
    box.set_margin_end(80)
    box.append(icon)
    return box


def _make_row(text):
    row = Gtk.ListBoxRow()
    # GtkListBoxRow defaults to activatable=True, which several themes
    # (Adwaita, Breeze) render with a hover chevron hinting "activating this
    # navigates elsewhere" - wrong here, this is a single-select list
    # (SelectionMode.SINGLE), not navigation.
    row.set_activatable(False)
    label = Gtk.Label(label=text)
    label.set_halign(Gtk.Align.START)
    label.set_margin_start(10)
    label.set_margin_top(0)
    label.set_margin_bottom(0)
    row.set_child(label)
    row._label = label  # noqa: SLF001 - read back in SelectList's selection handler
    return row


def _make_separator_row():
    row = Gtk.ListBoxRow()
    row.set_activatable(False)
    row.set_selectable(False)
    row.set_focusable(False)
    separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
    separator.set_margin_top(4)
    separator.set_margin_bottom(4)
    row.set_child(separator)
    row._label = None  # noqa: SLF001
    return row


def _row_for(value, text):
    return _make_separator_row() if value is SEPARATOR else _make_row(text)


class SelectList:
    """A scrollable single-select list, matching macOS Setup Assistant's
    compact ~350x200 country/language/timezone picker (tight single-line
    rows in a bordered box), not a full-height touch-style list."""

    def __init__(self, items):
        """items: list of (value, display_text)."""
        self.items = list(items)
        self._selected_label = None
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-selected", self._on_row_selected)
        for value, text in self.items:
            self.listbox.append(_row_for(value, text))

        scroller = Gtk.ScrolledWindow()
        # The framed-box border/radius/background belongs on the scroller
        # (the actually-bounded viewport), not the listbox - the listbox is
        # as tall as its full, unclipped row count, so a border drawn on it
        # was only ever visible on 3 sides; the "open at the bottom" look
        # every earlier screenshot had was this, not a sizing issue.
        scroller.add_css_class("wizard-list")
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_child(self.listbox)
        # Without this, the first/last row's square background corners
        # poke out past the box's rounded border corners.
        scroller.set_overflow(Gtk.Overflow.HIDDEN)
        # propagate_natural_* + matching min/max-content-* is the idiomatic
        # GTK4 way to pin a GtkScrolledWindow to an exact size regardless of
        # its child's own size - propagate=False alone (the previous code
        # here) only floors the *minimum* size and left the actual width
        # shrunk to the child's own minimum, ~190px instead of the intended
        # width, with no visible scrollbar/border framing to match.
        scroller.set_propagate_natural_width(True)
        scroller.set_propagate_natural_height(True)
        # Measured directly off a real macOS Setup Assistant screenshot
        # (410x206 in a 723-wide card) and scaled to this app's 800-wide
        # card (factor 799/723 ~= 1.105).
        scroller.set_min_content_width(453)
        scroller.set_max_content_width(453)
        scroller.set_min_content_height(228)
        scroller.set_max_content_height(228)
        # Belt-and-suspenders: min/max-content-* alone was observed to be
        # ignored (the scroller kept shrinking to ~190px, the listbox's own
        # minimum) - set_size_request is a hard floor GTK always honors
        # regardless of what's driving that discrepancy.
        scroller.set_size_request(453, 228)
        scroller.set_halign(Gtk.Align.CENTER)
        scroller.set_vexpand(False)
        scroller.set_margin_top(50)
        self.widget = scroller

    def _on_row_selected(self, _listbox, row):
        # CSS alone (`row:selected { color: ... }`, even re-declared on the
        # child `label` directly) measurably did not reach the label's
        # rendered text on this system's theme - background-color from the
        # very same rule did apply (confirmed by exact-matching sampled
        # pixels), only color didn't, for reasons that didn't resolve after
        # several targeted CSS overrides. Pango attributes on the label
        # itself bypass that entirely and are guaranteed to render.
        if self._selected_label is not None:
            self._selected_label.set_attributes(Pango.AttrList.new())
            self._selected_label = None
        label = getattr(row, "_label", None) if row is not None else None
        if label is not None:
            label.set_attributes(_selected_attrs())
            self._selected_label = label

    def set_items(self, items):
        self.items = list(items)
        child = self.listbox.get_row_at_index(0)
        while child is not None:
            self.listbox.remove(child)
            child = self.listbox.get_row_at_index(0)
        self._selected_label = None
        for value, text in self.items:
            self.listbox.append(_row_for(value, text))
        # Rebuilding the row set (country.py's IP-suggestion reorder is the
        # only caller) can leave stale paint behind under VirtualBox's
        # software renderer, which doesn't always repaint the old rows'
        # damage region correctly when they're removed mid-session - force
        # a full re-layout/repaint instead of trusting incremental damage.
        self.listbox.queue_resize()
        self.listbox.queue_draw()

    def selected_value(self):
        row = self.listbox.get_selected_row()
        if row is None:
            return None
        idx = row.get_index()
        if 0 <= idx < len(self.items):
            return self.items[idx][0]
        return None

    def selected_text(self):
        row = self.listbox.get_selected_row()
        if row is None:
            return None
        idx = row.get_index()
        if 0 <= idx < len(self.items):
            return self.items[idx][1]
        return None

    def select_index(self, idx):
        row = self.listbox.get_row_at_index(idx)
        if row is not None:
            self.listbox.select_row(row)

    def select_value(self, value):
        for i, (v, _t) in enumerate(self.items):
            if v == value:
                self.select_index(i)
                return
