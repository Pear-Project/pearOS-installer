"""Port of app/js/navbar.js: the fixed macOS-style top taskbar injected on
every real page except language-select (index.html never loads navbar.js -
reproduced by simply not adding this widget on that page). Logo dropdown
(Shutdown/Restart/Live Environment), app-name dropdown (About/Show Log/Show
Disks/Quit), live clock, About modal."""
import datetime

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from . import state
from .widgets import load_scaled_picture

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _format_datetime(now):
    date_str = f"{_MONTHS[now.month - 1]} {now.day}"
    hour12 = now.hour % 12 or 12
    ampm = "PM" if now.hour >= 12 else "AM"
    time_str = f"{hour12}:{now.minute:02d} {ampm}"
    return date_str, time_str


def _menu_button(label, on_click):
    btn = Gtk.Button(label=label)
    btn.add_css_class("flat")
    btn.add_css_class("logo-menu-item")
    btn.set_halign(Gtk.Align.FILL)
    child = btn.get_child()
    if child is not None:
        child.set_halign(Gtk.Align.START)
    btn.connect("clicked", lambda _b: on_click())
    return btn


def _menubar_item(label, popover=None):
    """A top-level File/Edit/Utilities/Window-style menu bar entry. With no
    popover it's inert (matches real macOS Recovery, where Edit/Window carry
    no working commands either - they're standard menu-bar furniture, not
    dead buttons we invented)."""
    btn = Gtk.Button(label=label)
    btn.add_css_class("flat")
    btn.add_css_class("menubar-item")
    btn.set_valign(Gtk.Align.CENTER)
    if popover is not None:
        popover.set_parent(btn)
        btn.connect("clicked", lambda _b: popover.popup())
    return btn


class Navbar(Gtk.Box):
    def __init__(self, app, quit_callback):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        self.app = app
        self._quit_callback = quit_callback
        self.add_css_class("taskbar")
        # 24px: matches both the officially documented, long-standing
        # NSStatusBar.system.thickness AND direct pixel measurement off
        # the user's real Sonoma-era Recovery screenshots (all references
        # given are that era, not Tahoe - see style.css's card-radius
        # comment for the same correction). The original Electron CSS used
        # 2.5em (35px) here instead.
        self.set_size_request(-1, 24)
        self.set_hexpand(True)
        self.set_valign(Gtk.Align.START)

        left = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        left.set_hexpand(True)
        left.set_valign(Gtk.Align.CENTER)
        left.set_margin_start(8)

        logo_btn = Gtk.Button()
        logo_btn.add_css_class("flat")
        logo_btn.set_valign(Gtk.Align.CENTER)
        # Sized to fit well inside the 24px bar (see set_size_request above)
        # with room to spare, matching real menu-bar icon proportions.
        logo_pic = load_scaled_picture("pear-logo.svg", (12, 16))
        logo_btn.set_child(logo_pic)
        left.append(logo_btn)

        self.app_name_label = Gtk.Label(label="pearOS Installer")
        self.app_name_label.add_css_class("taskbar-label")
        self.app_name_label.add_css_class("taskbar-app-name")
        self.app_name_label.set_valign(Gtk.Align.CENTER)
        left.append(self.app_name_label)

        # Real macOS-style menu bar entries (File/Edit/Utilities/Window) -
        # not present in the original Electron app (which only had the two
        # dropdown buttons below), added to match how the real recovery
        # menu bar actually looks. Every action the original exposed is
        # still here, just redistributed into these menus instead of
        # invented from scratch.
        self.file_menu_btn = _menubar_item("File")
        left.append(self.file_menu_btn)
        left.append(_menubar_item("Edit"))
        self.utilities_menu_btn = _menubar_item("Utilities")
        left.append(self.utilities_menu_btn)
        left.append(_menubar_item("Window"))

        self.append(left)

        right = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        right.set_valign(Gtk.Align.CENTER)
        self.date_label = Gtk.Label(label="")
        self.date_label.add_css_class("taskbar-label")
        self.time_label = Gtk.Label(label="")
        self.time_label.add_css_class("taskbar-label")
        right.append(self.date_label)
        right.append(self.time_label)
        right.set_margin_end(16)
        self.append(right)

        self._build_logo_menu(logo_btn)
        self._build_file_menu()
        self._build_utilities_menu()
        self._build_about_modal()

        self._tick_clock()
        GLib.timeout_add_seconds(1, self._tick_clock)

    def set_app_name(self, name):
        self.app_name_label.set_label(name)

    def _tick_clock(self):
        date_str, time_str = _format_datetime(datetime.datetime.now())
        self.date_label.set_label(date_str)
        self.time_label.set_label(time_str)
        return True

    def _build_logo_menu(self, anchor):
        popover = Gtk.Popover()
        popover.set_parent(anchor)
        popover.add_css_class("logo-menu")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(_menu_button("Shutdown", lambda: (popover.popdown(), state.shutdown())))
        box.append(_menu_button("Restart", lambda: (popover.popdown(), state.restart())))
        box.append(_menu_button(
            "Go to Live Environment", lambda: (popover.popdown(), self._quit_callback())
        ))
        popover.set_child(box)
        anchor.connect("clicked", lambda _b: popover.popup())

    @staticmethod
    def _link_open_state(popover, button):
        """Highlight a menu-bar item only while its own popover is open -
        real macOS menu-bar items light up on click, not on hover."""
        popover.connect("show", lambda _p: button.add_css_class("open"))
        popover.connect("closed", lambda _p: button.remove_css_class("open"))

    def _build_file_menu(self):
        popover = Gtk.Popover()
        popover.add_css_class("logo-menu")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(_menu_button(
            "Quit pearOS Installer", lambda: (popover.popdown(), self._quit_callback())
        ))
        popover.set_child(box)
        popover.set_parent(self.file_menu_btn)
        self.file_menu_btn.connect("clicked", lambda _b: popover.popup())
        self._link_open_state(popover, self.file_menu_btn)

    def _build_utilities_menu(self):
        popover = Gtk.Popover()
        popover.add_css_class("logo-menu")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(_menu_button(
            "About pearOS Installer", lambda: (popover.popdown(), self._about_modal.present())
        ))
        box.append(_menu_button("Show Log", lambda: (popover.popdown(), state.show_log())))
        box.append(_menu_button("Show Disks", lambda: (popover.popdown(), state.show_disks())))
        popover.set_child(box)
        popover.set_parent(self.utilities_menu_btn)
        self.utilities_menu_btn.connect("clicked", lambda _b: popover.popup())
        self._link_open_state(popover, self.utilities_menu_btn)

    def _build_about_modal(self):
        win = Gtk.Window()
        win.set_modal(True)
        win.set_decorated(False)
        win.add_css_class("about-modal")
        win.set_default_size(400, -1)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(32)
        box.set_margin_bottom(32)
        box.set_margin_start(32)
        box.set_margin_end(32)

        title = Gtk.Label(label="About pearOS Installer")
        title.add_css_class("about-modal-title")
        box.append(title)

        for text in (
            "Build: 2026.03.05 - dualboot",
            "Author: Pear Software and Services",
            "Email: alex@pear-software.com",
        ):
            label = Gtk.Label(label=text)
            label.add_css_class("about-modal-text")
            box.append(label)

        close_btn = Gtk.Button(label="Close")
        close_btn.add_css_class("modal-button")
        close_btn.set_halign(Gtk.Align.CENTER)
        close_btn.set_margin_top(8)
        close_btn.connect("clicked", lambda _b: win.close())
        box.append(close_btn)

        win.set_child(box)
        self._about_modal = win

    def attach_to(self, window):
        self._about_modal.set_transient_for(window)
