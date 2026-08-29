"""Shared bits for the three list-based pages (language/keymap/timezone),
which all reproduce the same `.list` <select size=9> markup."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


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
    return row


class SelectList:
    """A scrollable single-select list, matching macOS Setup Assistant's
    compact ~350x200 country/language/timezone picker (tight single-line
    rows in a bordered box), not a full-height touch-style list."""

    def __init__(self, items):
        """items: list of (value, display_text)."""
        self.items = list(items)
        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("wizard-list")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        for _value, text in self.items:
            self.listbox.append(_make_row(text))

        scroller = Gtk.ScrolledWindow()
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
        # 420px, with no visible scrollbar/border framing to match.
        scroller.set_propagate_natural_width(True)
        scroller.set_propagate_natural_height(True)
        scroller.set_min_content_width(420)
        scroller.set_max_content_width(420)
        scroller.set_min_content_height(200)
        scroller.set_max_content_height(200)
        # Belt-and-suspenders: min/max-content-* alone was observed to be
        # ignored (the scroller kept shrinking to ~190px, the listbox's own
        # minimum) - set_size_request is a hard floor GTK always honors
        # regardless of what's driving that discrepancy.
        scroller.set_size_request(420, 200)
        scroller.set_halign(Gtk.Align.CENTER)
        scroller.set_vexpand(False)
        scroller.set_margin_top(40)
        self.widget = scroller

    def set_items(self, items):
        self.items = list(items)
        child = self.listbox.get_row_at_index(0)
        while child is not None:
            self.listbox.remove(child)
            child = self.listbox.get_row_at_index(0)
        for _value, text in self.items:
            self.listbox.append(_make_row(text))
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
