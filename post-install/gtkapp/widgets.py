"""Shared page-chrome widgets: the 800x600 '.app' card, back/continue
buttons, title/description labels — reused by every wizard step page,
mirroring the markup shared by all templates/*.html."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .svgpath import parse_path, path_to_cairo
from .background import Background

BACK_ARROW_D = "M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"
_BACK_ARROW_OPS = parse_path(BACK_ARROW_D)


# The back button (see make_back_button below) is a 40x40 icon + 12px CSS
# padding + a 12px overlay margin -> occupies roughly x:[12,76] y:[12,76].
# Every page except "language" has one, so the title's left margin is fixed
# here (not per-page) to always clear it, with "language" getting the same
# indent for consistency even though it has no button - past behavior had
# the title start at the same x as the button, which is what put the back
# arrow glyph directly on top of the title text on every page that has one.
_TITLE_MARGIN_START = 84


def make_title(text):
    label = Gtk.Label(label=text)
    label.add_css_class("title")
    label.set_halign(Gtk.Align.START)
    label.set_margin_top(20)
    label.set_margin_start(_TITLE_MARGIN_START)
    return label


def make_description(text):
    label = Gtk.Label(label=text)
    label.add_css_class("description")
    label.set_wrap(True)
    label.set_justify(Gtk.Justification.CENTER)
    label.set_halign(Gtk.Align.CENTER)
    # A wrap-enabled label's *natural* width, by GTK's own definition, is
    # however wide it'd be on one unbroken line - wrapping only happens once
    # something allocates it less than that. Nothing above this label in the
    # tree does (the card is center-aligned in a fullscreen window with
    # plenty of room to give it its natural size), so long description text
    # was ballooning the whole card past 800px, exactly like the two
    # set_size_request()-isn't-a-cap bugs above. Every individual page that
    # builds its own long note label already caps it at 60 chars (see
    # look.py, piri.py, etc.) - doing it here too closes the gap for
    # anything that goes through the shared helper instead, agreement.py's
    # description included, and for any i18n string that runs longer than
    # its English source.
    label.set_max_width_chars(60)
    return label


class BackArrow(Gtk.DrawingArea):
    """Cairo redraw of the inline SVG back-arrow (viewBox 0 0 24 24)."""

    def __init__(self):
        super().__init__()
        self.add_css_class("back-arrow")
        self.set_content_width(40)
        self.set_content_height(40)
        self.set_draw_func(self._draw)

    def _draw(self, area, cr, w, h):
        cr.save()
        cr.scale(w / 24.0, h / 24.0)
        path_to_cairo(cr, _BACK_ARROW_OPS)
        cr.close_path()
        rgba = self.get_color()
        cr.set_source_rgba(rgba.red, rgba.green, rgba.blue, rgba.alpha)
        cr.fill()
        cr.restore()


def make_back_button(on_click):
    btn = Gtk.Button()
    btn.add_css_class("back-button")
    btn.add_css_class("flat")
    btn.set_child(BackArrow())
    btn.set_halign(Gtk.Align.START)
    btn.set_valign(Gtk.Align.START)
    btn.set_margin_top(12)
    btn.set_margin_start(12)
    if on_click:
        btn.connect("clicked", lambda b: on_click())
    return btn


def make_nav_button(label, on_click=None):
    btn = Gtk.Button(label=label)
    btn.add_css_class("nav-button")
    btn.set_halign(Gtk.Align.END)
    btn.set_valign(Gtk.Align.END)
    btn.set_margin_end(20)
    btn.set_margin_bottom(20)
    if on_click:
        btn.connect("clicked", lambda b: on_click())
    return btn


class AppCard:
    """Builds the .app card overlay: content + optional back button + a
    forward/continue button pinned at the bottom-right, exactly like the
    .movement-buttons / #move-back-btn / #move-forward-btn markup shared by
    every templates/*.html page."""

    def __init__(self, content, on_back, on_forward, forward_label="Continue"):
        self.overlay = Gtk.Overlay()
        card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        card.add_css_class("app")
        card.set_size_request(800, 600)
        card.set_hexpand(False)
        card.set_vexpand(False)
        card.set_halign(Gtk.Align.CENTER)
        card.set_valign(Gtk.Align.CENTER)
        card.append(content)
        self.overlay.set_child(card)

        if on_back:
            self.overlay.add_overlay(make_back_button(on_back))

        self.forward_button = make_nav_button(forward_label, on_forward)
        self.overlay.add_overlay(self.forward_button)

    @property
    def widget(self):
        return self.overlay


def page_root(content_widget, on_back, on_forward, forward_label="Continue"):
    """Full page: blurred wallpaper background + centered .app card."""
    bg = Background(sharp=False)
    card = AppCard(content_widget, on_back, on_forward, forward_label)
    centering = Gtk.Box()
    centering.set_halign(Gtk.Align.CENTER)
    centering.set_valign(Gtk.Align.CENTER)
    centering.set_hexpand(True)
    centering.set_vexpand(True)
    centering.append(card.widget)
    bg.add_overlay(centering)
    return bg, card
