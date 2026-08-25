"""Port of page_menu.html: the "Recovery" menu - 4 single-select rows
(packup-restore stub / installer / browser / gparted). Double-click an item
= immediate action (handleMenuAction); Continue = act on whichever is
selected (handleMenuContinue). The installer path now routes through the
confirm page's welcome/EULA/disk-select flow instead of launching Calamares
directly - Calamares itself is launched from the disk-select tab's own
Continue button (see confirm.py)."""
import subprocess

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import make_card, centered_overlay, load_scaled_picture
from ..navbar import Navbar

_ITEMS = [
    ("packup", "packup-logo.png", "menu.packup"),
    ("installer", "nicec0re-logo.png", "menu.installer"),
    ("browser", "firefox-logo.png", "menu.browser"),
    ("gparted", "gparted.svg", "menu.gparted"),
]


def _open_gparted():
    try:
        subprocess.Popen(["gparted"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass


def _open_browser():
    for argv in (["pafari"], ["xdg-open", "http://www.google.com"], ["firefox"]):
        try:
            subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except OSError:
            continue


def _open_packup():
    # TODO in the original too: packup restore isn't implemented yet.
    try:
        subprocess.Popen(["packup"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass


class MenuPage:
    def __init__(self, app):
        self.app = app
        self._selected = "packup"
        self._rows = {}

        card = make_card(500, 500, "menu-card")

        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        list_box.set_margin_start(20)
        list_box.set_margin_end(20)
        list_box.set_margin_top(20)

        for key, icon, i18n_prefix in _ITEMS:
            row = self._build_row(key, icon)
            self._rows[key] = row
            list_box.append(row["widget"])

        card.append(list_box)

        buttons = Gtk.Box()
        buttons.set_halign(Gtk.Align.END)
        buttons.set_valign(Gtk.Align.END)
        buttons.set_vexpand(True)
        self.continue_btn = Gtk.Button(label="Continue")
        self.continue_btn.add_css_class("install-button-agreement")
        self.continue_btn.set_margin_end(20)
        self.continue_btn.set_margin_bottom(20)
        self.continue_btn.connect("clicked", lambda _b: self._on_continue())
        buttons.append(self.continue_btn)
        card.append(buttons)

        overlay = centered_overlay(card)
        self.navbar = Navbar(app, app.quit)
        self.navbar.set_app_name("Recovery")
        overlay.add_overlay(self.navbar)

        self.widget = overlay
        self._select(self._selected)

    def _build_row(self, key, icon_file):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.add_css_class("menu-row")
        row.set_size_request(-1, 80)

        pic = load_scaled_picture(icon_file, 50)
        row.append(pic)

        text_col = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        text_col.set_valign(Gtk.Align.CENTER)
        title = Gtk.Label(label="")
        title.add_css_class("menu-row-title")
        title.set_halign(Gtk.Align.START)
        desc = Gtk.Label(label="")
        desc.add_css_class("menu-row-desc")
        desc.set_halign(Gtk.Align.START)
        desc.set_wrap(True)
        text_col.append(title)
        text_col.append(desc)
        row.append(text_col)

        click = Gtk.GestureClick()
        click.connect("released", lambda *_a: self._select(key))
        row.add_controller(click)

        double_click = Gtk.GestureClick()
        double_click.set_button(1)
        double_click.connect("pressed", lambda _g, n, *_a: self._on_action(key) if n == 2 else None)
        row.add_controller(double_click)

        return {"widget": row, "title": title, "desc": desc}

    def on_show(self):
        i18n = self.app.i18n_for(self.app.current_locale)
        for key, icon, i18n_prefix in _ITEMS:
            row = self._rows[key]
            row["title"].set_label(i18n.t(i18n_prefix + ".title", key))
            row["desc"].set_label(i18n.t(i18n_prefix + ".desc", ""))
        self.continue_btn.set_label(i18n.t("menu.continue", "Continue"))

    def _select(self, key):
        self._selected = key
        for k, row in self._rows.items():
            if k == key:
                row["widget"].add_css_class("checked")
            else:
                row["widget"].remove_css_class("checked")

    def _on_action(self, key):
        self._select(key)
        if key == "packup":
            _open_packup()
        elif key == "installer":
            # Goes to the confirm page's welcome/EULA/disk-select flow
            # first - Calamares itself is launched from there (disk tab's
            # own Continue), not directly from this menu anymore.
            self.app.go_to("confirm")
        elif key == "browser":
            _open_browser()
        elif key == "gparted":
            _open_gparted()

    def _on_continue(self):
        key = self._selected
        if key == "packup":
            _open_packup()
        elif key == "installer":
            self.app.go_to("confirm")
        elif key == "browser":
            _open_browser()
        elif key == "gparted":
            _open_gparted()
