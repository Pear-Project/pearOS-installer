"""Port of the old page_install_progress.html + progress.js, which existed
in this app's git history but was deleted by the "remove online install,
port to debian" commit - that commit replaced the whole disk-formatting
pipeline (a 'setup' binary reading/writing /tmp/disk-to-install and
/tmp/progress) with a direct handoff to Calamares, which has its own
progress UI. This page's old data source (the 'setup' binary) no longer
exists, so this is a fresh UI-only rebuild, not a byte-for-byte port of the
old JS - kept per the user's explicit request ("o sa ne trebuiasca", we'll
need it later), for a future custom setup script per installer_backend.py's
own stated plan (see its docstring).

Not wired into the current install flow - confirm.py's disk-select
Continue still launches Calamares directly, which owns its own progress
window while it runs. This page is reachable only via the dev QA-start
override until something in installer_backend.py actually drives it
(update_progress/set_disk/show_finished/show_failed below)."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..widgets import make_card, centered_overlay, load_scaled_picture
from ..navbar import Navbar


class InstallProgressPage:
    def __init__(self, app):
        self.app = app
        self._i18n = None
        self._disk = None

        card = make_card(800, 600, "app")

        logo = load_scaled_picture("nicec0re-logo.png", 200)
        logo.set_valign(Gtk.Align.START)
        logo.set_margin_top(40)
        card.append(logo)

        self.title = Gtk.Label(label="pearOS NiceC0re")
        self.title.add_css_class("title")
        self.title.set_margin_top(16)
        card.append(self.title)

        self.status_label = Gtk.Label(label="")
        self.status_label.add_css_class("setup-text")
        self.status_label.set_wrap(True)
        self.status_label.set_justify(Gtk.Justification.CENTER)
        self.status_label.set_margin_top(8)
        card.append(self.status_label)

        # The disk being installed to (icon + name), matching the old
        # progress.js's disk_logo_progress + disk_title markup and the
        # confirm page's own disk-select tile styling. Hidden until
        # set_disk() gives it a real disk to show.
        self.disk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.disk_box.set_halign(Gtk.Align.CENTER)
        self.disk_box.set_margin_top(16)
        self.disk_box.set_visible(False)
        self.disk_icon_slot = Gtk.Box()
        self.disk_icon_slot.set_halign(Gtk.Align.CENTER)
        self.disk_box.append(self.disk_icon_slot)
        self.disk_name_label = Gtk.Label(label="")
        self.disk_name_label.add_css_class("disk-title")
        self.disk_box.append(self.disk_name_label)
        card.append(self.disk_box)

        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.add_css_class("install-progress-bar")
        self.progress_bar.set_size_request(350, -1)
        self.progress_bar.set_halign(Gtk.Align.CENTER)
        self.progress_bar.set_margin_top(24)
        card.append(self.progress_bar)

        self.eta_label = Gtk.Label(label="")
        self.eta_label.add_css_class("license-text")
        self.eta_label.set_margin_top(10)
        card.append(self.eta_label)

        spacer = Gtk.Box()
        spacer.set_vexpand(True)
        card.append(spacer)

        footer = Gtk.Box()
        footer.set_halign(Gtk.Align.END)
        footer.set_margin_end(20)
        footer.set_margin_bottom(16)
        self.close_btn = Gtk.Button(label="Close")
        self.close_btn.add_css_class("install-button-agreement")
        self.close_btn.connect("clicked", lambda _b: self.app.quit())
        footer.append(self.close_btn)
        card.append(footer)

        overlay = centered_overlay(card)
        self.navbar = Navbar(app, app.quit)
        self.navbar.set_app_name("Installer")
        overlay.add_overlay(self.navbar)

        self.widget = overlay

    def _t(self, key, default):
        return self._i18n.t(key, default) if self._i18n else default

    def _disk_install_text(self):
        model = self._disk["model"] if self._disk else ""
        key = "progress.disk_text_named" if model else "progress.disk_text"
        default = (
            f'pearOS NiceC0re will be installed on the disk "{model}":'
            if model
            else "pearOS NiceC0re will be installed on the disk:"
        )
        text = self._t(key, default)
        return text.format(disk=model) if model else text

    def on_show(self):
        self._i18n = self.app.i18n_for(self.app.current_locale)
        self.title.set_label(self._t("progress.title", "pearOS NiceC0re"))
        self.close_btn.set_label(self._t("progress.close", "Close"))
        self._disk = None
        self.disk_box.set_visible(False)
        self.progress_bar.set_fraction(0.0)
        self.progress_bar.set_visible(True)
        self.eta_label.set_label(self._t("progress.eta_calculating", "Estimated time remaining: Calculating..."))
        self.eta_label.set_visible(True)
        self.status_label.remove_css_class("progress-status-success")
        self.status_label.remove_css_class("progress-status-warning")
        self.status_label.remove_css_class("progress-status-error")
        self.status_label.set_label(self._disk_install_text())

        # No real caller has picked a disk yet (this page isn't wired into
        # the live flow) - preview the first real disk so QA-start=progress
        # shows something meaningful instead of a blank spot, matching
        # confirm.py's own disk-select tab, which already lists real disks
        # the same way.
        from .. import disk_backend
        disks = disk_backend.list_disks()
        if disks:
            self.set_disk(disks[0])

    # ── Public API for a future backend to drive this page ─────────────
    def set_disk(self, disk):
        """disk: {name, path, size, model} from disk_backend.py, or None
        to clear the disk display."""
        self._disk = disk
        self.status_label.set_label(self._disk_install_text())
        child = self.disk_icon_slot.get_first_child()
        if child is not None:
            self.disk_icon_slot.remove(child)
        if disk:
            self.disk_icon_slot.append(load_scaled_picture("disk.png", 60))
            self.disk_name_label.set_label(f"{disk['model']}\n{disk['size']}")
        self.disk_box.set_visible(bool(disk))

    def update_progress(self, percent, eta_text=None):
        """percent: 0-100. eta_text: pre-formatted remaining-time string,
        or None while there isn't enough data yet to estimate one."""
        self.progress_bar.set_fraction(max(0.0, min(100.0, percent)) / 100.0)
        if eta_text:
            self.eta_label.set_label(self._t("progress.eta_prefix", "Estimated time remaining: {time}").format(time=eta_text))
        else:
            self.eta_label.set_label(self._t("progress.eta_calculating", "Estimated time remaining: Calculating..."))

    def show_finished(self, warnings=0):
        self.progress_bar.set_visible(False)
        self.eta_label.set_visible(False)
        if warnings:
            self.status_label.add_css_class("progress-status-warning")
            text = self._t(
                "progress.finished_warnings",
                "Installation finished with {count} warning(s).\n"
                "Some packages failed to install. You can close this window and reboot, "
                "or check the logs: /home/liveuser/Desktop/install.log and /tmp/failed_packages.log",
            )
            self.status_label.set_label(text.format(count=warnings))
        else:
            self.status_label.add_css_class("progress-status-success")
            self.status_label.set_label(self._t(
                "progress.finished_ok",
                "Installation finished successfully!\n"
                "You can close this window and reboot your new pearintosh, "
                "or check the log located on the desktop.",
            ))

    def show_failed(self, error_message):
        self.progress_bar.set_visible(False)
        self.eta_label.set_visible(False)
        self.status_label.add_css_class("progress-status-error")
        text = self._t(
            "progress.failed",
            "Installation Failed!\nError: {error}\n"
            "Please check /home/liveuser/Desktop/install.log for details. "
            "You may need to restart the installer or check your disk.",
        )
        self.status_label.set_label(text.format(error=error_message))
