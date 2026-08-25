"""Entry point: GTK4 Application replacing main.js. Fullscreen, undecorated
window; a Gtk.Stack holds the 4 real pages; single-instance behavior comes
for free from GApplication's application-id uniqueness (mirrors
requestSingleInstanceLock() + 'second-instance' focus-stealing in main.js)."""
import os
import sys

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk

from . import fonts
from . import state as state_mod
from .i18n import I18n
from .osrelease import OS_RELEASE

_HERE = os.path.dirname(os.path.abspath(__file__))
_STYLE_CSS = os.path.join(_HERE, "style.css")

PAGE_ORDER = ["language", "examining", "menu", "confirm", "progress"]


class InstallerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.pearos.systeminstall")
        self.window = None
        self.pages = {}
        self.stack = None
        self.current_locale = "en"
        self._i18n_cache = {}

    def i18n_for(self, locale):
        i18n = self._i18n_cache.get(locale)
        if i18n is None:
            i18n = I18n(locale)
            self._i18n_cache[locale] = i18n
        return i18n

    def go_to(self, name, locale=None):
        if locale is not None:
            self.current_locale = locale
        self.stack.set_visible_child_name(name)
        page = self.pages[name]
        on_show = getattr(page, "on_show", None)
        if on_show:
            on_show()

    # ── GApplication lifecycle ────────────────────────────────────────
    def do_activate(self):
        if self.window is not None:
            self.window.present()
            return

        fonts.register_all()

        provider = Gtk.CssProvider()
        provider.load_from_path(_STYLE_CSS)
        # USER, not APPLICATION: the desktop's own GTK theme (Breeze on
        # this KDE session) was winning the cascade against our focus-ring
        # removal rules at APPLICATION priority - verified by screenshot,
        # the ring persisted with every outline/box-shadow variant tried
        # at APPLICATION. USER outranks both THEME and APPLICATION.
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title(OS_RELEASE.rebrand("pearOS NiceC0re Installer"))
        self.window.set_decorated(False)
        self.window.set_resizable(False)

        monitors = Gdk.Display.get_default().get_monitors()
        if monitors.get_n_items() > 0:
            geo = monitors.get_item(0).get_geometry()
            self.window.set_default_size(geo.width, geo.height)

        root_overlay = Gtk.Overlay()
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.NONE)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        root_overlay.set_child(self.stack)

        self._build_pages()

        if state_mod.IS_TEST_MODE:
            # Bottom-left corner, out of the way of each page's own navbar
            # (which lives at the top of the window too, on every page but
            # language - a full-width top banner collided with it there).
            banner = Gtk.Label(label="Test mode — no real disk/system actions.")
            banner.add_css_class("test-banner")
            banner.set_valign(Gtk.Align.END)
            banner.set_halign(Gtk.Align.START)
            banner.set_margin_start(12)
            banner.set_margin_bottom(12)
            root_overlay.add_overlay(banner)

        self.window.set_child(root_overlay)
        self.window.fullscreen()
        self.window.present()
        GLib.idle_add(lambda: (self.window.fullscreen(), False)[1])

        for page in self.pages.values():
            attach = getattr(page, "navbar", None)
            if attach is not None:
                attach.attach_to(self.window)

        # Only used by developers doing manual/visual QA to jump straight to
        # one page instead of clicking through the whole flow.
        start_page = os.environ.get("GTKAPP_QA_START", "language")
        self.go_to(start_page)

    def _build_pages(self):
        from .pages.language import LanguagePage
        from .pages.examining import ExaminingPage
        from .pages.menu import MenuPage
        from .pages.confirm import ConfirmPage
        from .pages.install_progress import InstallProgressPage

        page_classes = {
            "language": LanguagePage,
            "examining": ExaminingPage,
            "menu": MenuPage,
            "confirm": ConfirmPage,
            "progress": InstallProgressPage,
        }
        for name in PAGE_ORDER:
            page = page_classes[name](self)
            self.pages[name] = page
            self.stack.add_named(page.widget, name)


def main():
    app = InstallerApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
