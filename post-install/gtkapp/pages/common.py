"""Shared bits for the three list-based pages (language/keymap/timezone),
which all reproduce the same `.list` <select size=9> markup."""
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf

from .. import state as state_mod

WORLDMAP_PATH = __import__("os").path.join(state_mod.RESOURCES_DIR, "country.png")


def make_worldmap():
    # GtkPicture.measure() reports the source image's *intrinsic* size
    # (360x360) as its natural size no matter what set_size_request() or
    # Gtk.Overflow.HIDDEN say - overflow only clips painting/allocation,
    # it does not change what the widget asks for during layout, so a
    # naive "wrap it in a 70x70 clipping box" doesn't actually stop this
    # from asking for 360px of width. Pre-scaling the pixbuf to the exact
    # display size is what actually fixes it: now its intrinsic size *is*
    # 70x70, so there's nothing left to overflow in the first place.
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(WORLDMAP_PATH, 70, 70, True)
    pic = Gtk.Picture.new_for_pixbuf(pixbuf)
    pic.set_content_fit(Gtk.ContentFit.CONTAIN)
    pic.set_can_shrink(True)
    pic.set_hexpand(False)
    pic.set_vexpand(False)

    box = Gtk.Box()
    box.set_size_request(70, 70)
    box.set_halign(Gtk.Align.CENTER)
    box.set_margin_top(50)
    box.append(pic)
    return box


class SelectList:
    """A scrollable single-select list, sized/styled like the original
    `<select class="list" size=9>` (350x200, centered)."""

    def __init__(self, items):
        """items: list of (value, display_text)."""
        self.items = list(items)
        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("wizard-list")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        for _value, text in self.items:
            row = Gtk.ListBoxRow()
            # GtkListBoxRow defaults to activatable=True, which several
            # themes (Adwaita, Breeze) render with a hover chevron hinting
            # "activating this navigates elsewhere" - wrong here, this is
            # a single-select list (SelectionMode.SINGLE), not navigation.
            row.set_activatable(False)
            label = Gtk.Label(label=text)
            label.set_halign(Gtk.Align.START)
            label.set_margin_start(10)
            label.set_margin_top(3)
            label.set_margin_bottom(3)
            row.set_child(label)
            self.listbox.append(row)

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_child(self.listbox)
        # min/max-content-* (not set_size_request) are what actually caps a
        # GtkScrolledWindow: size_request alone is only a floor, so a tall
        # GtkListBox (18 languages, etc.) was pushing the whole page past the
        # 800x600 card and off the bottom of the window.
        scroller.set_propagate_natural_width(False)
        scroller.set_propagate_natural_height(False)
        scroller.set_min_content_width(520)
        scroller.set_max_content_width(520)
        scroller.set_min_content_height(220)
        scroller.set_max_content_height(220)
        scroller.set_halign(Gtk.Align.CENTER)
        scroller.set_vexpand(False)
        scroller.set_margin_top(10)
        self.widget = scroller

    def set_items(self, items):
        self.items = list(items)
        child = self.listbox.get_row_at_index(0)
        while child is not None:
            self.listbox.remove(child)
            child = self.listbox.get_row_at_index(0)
        for _value, text in self.items:
            row = Gtk.ListBoxRow()
            # GtkListBoxRow defaults to activatable=True, which several
            # themes (Adwaita, Breeze) render with a hover chevron hinting
            # "activating this navigates elsewhere" - wrong here, this is
            # a single-select list (SelectionMode.SINGLE), not navigation.
            row.set_activatable(False)
            label = Gtk.Label(label=text)
            label.set_halign(Gtk.Align.START)
            label.set_margin_start(10)
            label.set_margin_top(3)
            label.set_margin_bottom(3)
            row.set_child(label)
            self.listbox.append(row)
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
