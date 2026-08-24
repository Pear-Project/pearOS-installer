"""Wi-Fi: only shown when there's no internet yet (matches post_setup's own
has_internet() check) - real scan/connect via nmcli (network_backend.py),
not a mockup list."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from .. import network_backend as netbackend
from ..widgets import page_root, make_title, make_description


class WifiPage:
    def __init__(self, app):
        self.app = app
        self._skip_next_show = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        content.set_vexpand(True)
        self.title = make_title("Select a Wi-Fi Network")
        content.append(self.title)
        self.status = make_description("Scanning for networks...")
        content.append(self.status)

        self.listbox = Gtk.ListBox()
        self.listbox.add_css_class("wizard-list")
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self._on_row_activated)

        scroller = Gtk.ScrolledWindow()
        scroller.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroller.set_child(self.listbox)
        scroller.set_propagate_natural_width(False)
        scroller.set_propagate_natural_height(False)
        scroller.set_min_content_width(520)
        scroller.set_max_content_width(520)
        scroller.set_min_content_height(180)
        scroller.set_max_content_height(180)
        scroller.set_halign(Gtk.Align.CENTER)
        scroller.set_margin_top(10)
        content.append(scroller)

        password_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        password_row.set_halign(Gtk.Align.CENTER)
        password_row.set_margin_top(10)
        self.password_entry = Gtk.PasswordEntry(placeholder_text="Password", show_peek_icon=True)
        self.password_entry.add_css_class("textbox")
        self.password_entry.set_visible(False)
        self.connect_btn = Gtk.Button(label="Join")
        self.connect_btn.add_css_class("nav-button")
        self.connect_btn.set_visible(False)
        self.connect_btn.connect("clicked", self._on_join_clicked)
        password_row.append(self.password_entry)
        password_row.append(self.connect_btn)
        content.append(password_row)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )
        self._selected_ssid = None

    def on_show(self):
        if self._skip_next_show:
            self._skip_next_show = False
            return
        if netbackend.has_internet():
            self.app.go_to("data_privacy")
            return
        self._refresh()

    def _refresh(self):
        self.status.set_label("Scanning for networks...")
        child = self.listbox.get_row_at_index(0)
        while child is not None:
            self.listbox.remove(child)
            child = self.listbox.get_row_at_index(0)

        def scan_thread():
            networks = netbackend.scan_networks()
            GLib.idle_add(self._populate, networks)

        import threading

        threading.Thread(target=scan_thread, daemon=True).start()

    def _populate(self, networks):
        if not networks:
            self.status.set_label("No networks found. You can continue without Wi-Fi.")
            return False
        self.status.set_label("Select a network to join, or skip for now.")
        for net in networks:
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            box.set_margin_top(4)
            box.set_margin_bottom(4)
            box.set_margin_start(10)
            label_text = net["ssid"]
            if net["active"]:
                label_text += "  (Connected)"
            label = Gtk.Label(label=label_text)
            label.set_halign(Gtk.Align.START)
            label.set_hexpand(True)
            box.append(label)
            lock = "🔒" if net["security"] and net["security"] != "--" else ""
            meta = Gtk.Label(label=lock + " " + str(net["signal"]) + "%")
            meta.set_margin_end(10)
            box.append(meta)
            row.set_child(box)
            row.ssid = net["ssid"]
            row.secured = bool(net["security"] and net["security"] != "--")
            self.listbox.append(row)
        return False

    def _on_row_activated(self, _listbox, row):
        self._selected_ssid = row.ssid
        if row.secured:
            self.password_entry.set_visible(True)
            self.connect_btn.set_visible(True)
            self.password_entry.grab_focus()
        else:
            self.password_entry.set_visible(False)
            self.connect_btn.set_visible(True)

    def _on_join_clicked(self, _btn):
        if not self._selected_ssid:
            return
        password = self.password_entry.get_text() or None
        self.status.set_label("Connecting to " + self._selected_ssid + "...")
        self.connect_btn.set_sensitive(False)

        def do_connect():
            ok, error = netbackend.connect(self._selected_ssid, password)
            GLib.idle_add(self._on_connect_result, ok, error)

        import threading

        threading.Thread(target=do_connect, daemon=True).start()

    def _on_connect_result(self, ok, error):
        self.connect_btn.set_sensitive(True)
        if ok:
            self.status.set_label("Connected.")
            self._skip_next_show = True
            self.app.go_to("data_privacy")
        else:
            self.status.set_label("Could not connect: " + (error or "unknown error"))
        return False

    def _on_back(self):
        self.app.go_to("accessibility")

    def _on_continue(self):
        self.app.go_to("data_privacy")
