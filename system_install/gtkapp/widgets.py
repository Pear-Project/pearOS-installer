"""Shared page-chrome widgets: the sized card (.app 800x600 / .menu-card
500x500), the PNG-swapped arrow nav buttons, the text "Back"/"Continue"
buttons used on the confirm page - reused by pages/*.py, mirroring the
markup shared by the original HTML pages.

Unlike post-install's uniform AppCard (every page has the same back+forward
chrome), this app's 4 real screens each lay out navigation differently in
the original markup (icon-only forward arrow / disabled icon pair / single
text Continue / text Back+Continue with a divider) - so this module offers
building blocks, not one fixed template; each page in pages/*.py assembles
its own movement-buttons row to match its original page exactly.
"""
import os

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf, Gdk

_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(_APP_DIR, "app", "resources")


def load_scaled_picture(filename, size, content_fit=Gtk.ContentFit.CONTAIN):
    """Loads an image resource pre-scaled to `size` (int, for a square
    target, or (w, h)), returned as a small Gtk.Box wrapping the picture
    (not the bare Gtk.Picture) - treat the return value as an opaque
    widget, not specifically a Picture.

    Two separate GtkPicture quirks made that wrapper necessary:
    1. Several of this app's source PNGs are shipped much bigger than where
       they're actually displayed (e.g. a 1024x1024 logo shown at 350px) -
       GtkPicture.measure() reports the source's *intrinsic* size as its
       natural size no matter what set_size_request() says (that's only a
       minimum, not a cap). Pre-scaling the pixbuf here means its intrinsic
       size *is* the target size, so there's nothing left to overflow.
    2. Separately (verified empirically, not documented anywhere obvious):
       a Gtk.Picture *anywhere* in a widget subtree that's added to a
       Gtk.Overlay via add_overlay() (which is how every card in this app
       is centered, see centered_overlay()) makes that whole overlay child
       get allocated as if it were hexpand/vexpand=True, regardless of what
       expand/align flags are actually set on it or its ancestors - even a
       single 350x350 Picture nested inside an 800x600 card blew the card's
       real allocation up past 1000px tall. Wrapping the Picture in its own
       Gtk.Box with Gtk.Overflow.HIDDEN + a matching fixed size_request (and
       explicit hexpand/vexpand=False) isolates that quirk so it stops
       propagating to the card's own allocation."""
    w, h = size if isinstance(size, tuple) else (size, size)
    path = os.path.join(RESOURCES_DIR, filename)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(path, w, h, False)
    picture = Gtk.Picture.new_for_pixbuf(pixbuf)
    picture.set_content_fit(content_fit)
    picture.set_can_shrink(True)
    picture.set_hexpand(False)
    picture.set_vexpand(False)

    wrapper = Gtk.Box()
    wrapper.set_size_request(w, h)
    wrapper.set_hexpand(False)
    wrapper.set_vexpand(False)
    # Without these, a parent that offers more space than this wrapper's
    # natural size (e.g. a full-width VERTICAL tab box) stretches it to
    # FILL - and since the wrapper is itself a plain Box, its one child
    # then packs at the start (left) of that stretched-out area instead of
    # staying centered (the same start-packing quirk documented on
    # centered_overlay()). Pinning the wrapper itself to its natural size
    # and centering it is what actually keeps the image centered.
    wrapper.set_halign(Gtk.Align.CENTER)
    wrapper.set_valign(Gtk.Align.CENTER)
    wrapper.set_overflow(Gtk.Overflow.HIDDEN)
    wrapper.append(picture)
    return wrapper


def _load_texture(filename, rotate_180=False):
    path = os.path.join(RESOURCES_DIR, filename)
    pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
    if rotate_180:
        pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.UPSIDEDOWN)
    return Gdk.Texture.new_for_pixbuf(pixbuf)


class ArrowButton(Gtk.Button):
    """Reproduces .arrow-button's 4-state PNG swap (normal/focus/pressed/
    focus+pressed) - GTK CSS can't declaratively swap a Gtk.Picture's image
    per pseudo-class the way the original's background-image rules did, so
    this tracks state-flags-changed and swaps the texture itself.

    rotate_180=True is the back button: the original reuses the *same*
    arrowbutton.png rotated 180deg via CSS transform rather than a separate
    asset - reproduced here by rotating the loaded pixbuf once, up front.
    """

    def __init__(self, rotate_180=False, on_click=None):
        super().__init__()
        self.add_css_class("flat")
        self.add_css_class("arrow-button")
        self.set_size_request(30, 30)

        self._normal = _load_texture("arrowbutton.png", rotate_180)
        self._focus = _load_texture("arrowbuttonFocus.png", rotate_180)
        self._pressed = _load_texture("arrowbuttonPressed.png", rotate_180)
        self._focus_pressed = _load_texture("arrowbuttonFocusPressed.png", rotate_180)

        self._picture = Gtk.Picture()
        self._picture.set_paintable(self._normal)
        self._picture.set_content_fit(Gtk.ContentFit.FILL)
        self._picture.set_can_shrink(True)
        self._picture.set_size_request(30, 30)
        self.set_child(self._picture)

        self.connect("state-flags-changed", lambda *_: self._update())
        self._update()

        if on_click:
            self.connect("clicked", lambda _b: on_click())

    def _update(self):
        flags = self.get_state_flags()
        focused = bool(flags & Gtk.StateFlags.FOCUSED)
        pressed = bool(flags & Gtk.StateFlags.ACTIVE)
        if pressed and focused:
            tex = self._focus_pressed
        elif pressed:
            tex = self._pressed
        elif focused:
            tex = self._focus
        else:
            tex = self._normal
        self._picture.set_paintable(tex)


def make_text_nav_button(label, on_click=None, primary=False):
    """The confirm page's "Back"/"Continue" pill buttons. Real macOS wizard
    footers give the primary/default action (Continue) the accent-blue
    fill and leave the secondary one (Back) neutral - both being the same
    plain white was a real gap, not a style choice."""
    btn = Gtk.Button(label=label)
    btn.add_css_class("nav-button-primary" if primary else "nav-button")
    if on_click:
        btn.connect("clicked", lambda _b: on_click())
    return btn


def make_card(width, height, css_class):
    card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    card.add_css_class(css_class)
    card.set_size_request(width, height)
    card.set_hexpand(False)
    card.set_vexpand(False)
    card.set_halign(Gtk.Align.CENTER)
    card.set_valign(Gtk.Align.CENTER)
    return card


def centered_overlay(card_widget):
    """The .flex-container: centers a card over the full window.

    Tried and rejected first: a plain Gtk.Box does NOT center a single
    non-expanding child along its packing axis (packs it at the start,
    leftover space trails after it, regardless of halign). Tried and
    rejected second: Gtk.CenterBox, including nesting a vertical one around
    a horizontal one - verified empirically (real allocation, not just
    measure()) that CenterBox does not respect a non-expanding child's own
    valign along its *cross* axis and stretches it to fill regardless,
    even with vexpand=False/valign=CENTER explicitly set on the child.

    What actually works, and is the same mechanism post-install's
    Background(Gtk.Overlay) already relies on: a card added as an *overlay
    child* (add_overlay), not the main child. GtkOverlay positions overlay
    children at their own natural size according to halign/valign, with no
    stretching - the main child here is just an empty full-bleed anchor
    that gives the Overlay something to size itself against.

    Real macOS installer/Setup Assistant windows sit noticeably above dead
    center, not exactly centered (verified against reference screenshots) -
    an asymmetric margin (bottom > top) shifts the centering point upward
    within the reduced allocation GTK centers the card in, without needing
    to know the actual screen size."""
    overlay = Gtk.Overlay()
    overlay.set_hexpand(True)
    overlay.set_vexpand(True)
    anchor = Gtk.Box()
    anchor.set_hexpand(True)
    anchor.set_vexpand(True)
    overlay.set_child(anchor)
    card_widget.set_margin_bottom(card_widget.get_margin_bottom() + 144)
    overlay.add_overlay(card_widget)
    return overlay
