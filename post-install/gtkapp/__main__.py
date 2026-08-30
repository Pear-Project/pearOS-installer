"""Entry point: GTK4 Application replacing main.js. Fullscreen, undecorated
window; a Gtk.Stack holds one page per wizard step; single-instance behavior
comes for free from GApplication's application-id uniqueness (mirrors
requestSingleInstanceLock() + 'second-instance' focus-stealing in main.js)."""
import os
import subprocess
import sys

# Gsk.GLShader (used by pages/hello.py for the liquid-gel lettering effect)
# only works with GTK4's legacy "gl" renderer — the "ngl" renderer that is
# now the default (GTK >= 4.14) reports "renderer does not support gl
# shaders" at compile time. Must be set before GDK connects. hello.py still
# works without this (falls back to a flat frosted look) if some future GTK
# drops the gl renderer entirely.
os.environ.setdefault("GSK_RENDERER", "gl")

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gdk

from . import fonts
from . import state as state_mod
from .i18n import I18n
from .osrelease import OS_RELEASE

_HERE = os.path.dirname(os.path.abspath(__file__))
_STYLE_CSS = os.path.join(_HERE, "style.css")

PAGE_ORDER = [
    "hello", "country", "wifi", "migration_assistant", "written_spoken",
    "language", "keymap", "accessibility", "data_privacy", "pearid", "user",
    "touchid_enable", "touchid_setup", "agreement", "location_services",
    "timezone", "analytics", "screen_time", "piri", "look", "update", "welcome", "finish",
]


class WizardApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.pearos.postinstall")
        self.window = None
        self.state = state_mod.WizardState()
        self.i18n = I18n("en_US")
        self.pages = {}
        self.stack = None
        # Matches system_install's own installer window - kill the
        # desktop shell while this wizard's own fullscreen window is up,
        # bring it back however this app eventually exits (finishing the
        # wizard normally, Quit, or an abnormal window close all funnel
        # through GApplication's "shutdown" signal).
        self.connect("shutdown", self._on_shutdown)

    # ── i18n / theming helpers used by page modules ──────────────────
    def t(self, key, default=None):
        return self.i18n.t(key, default)

    def set_locale(self, lng):
        self.i18n.load(lng)

    def set_dark_mode(self, enabled):
        if enabled:
            self.window.add_css_class("dark-mode")
        else:
            self.window.remove_css_class("dark-mode")

    def show_alert(self, message):
        dialog = Gtk.AlertDialog()
        dialog.set_message(message)
        dialog.set_modal(True)
        dialog.show(self.window)

    def go_to(self, name):
        self.stack.set_visible_child_name(name)
        page = self.pages[name]
        on_show = getattr(page, "on_show", None)
        if on_show:
            on_show()

    def _on_shutdown(self, _app):
        if state_mod.IS_TEST_MODE:
            return
        subprocess.Popen(
            ["plasmashell"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True
        )

    # ── GApplication lifecycle ────────────────────────────────────────
    def do_activate(self):
        if self.window is not None:
            self.window.present()
            return

        if not state_mod.IS_TEST_MODE:
            subprocess.run(["killall", "plasmashell"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        fonts.register_all()

        # macOS's scrollbar here is always drawn, not GTK's default
        # overlay-style one that only appears on hover/scroll and fades out
        # otherwise (which is invisible in a static screenshot, unlike the
        # reference) - classic mode keeps it permanently visible; the
        # thin-pill-not-thick-bar look itself comes from the .wizard-list
        # scrollbar/trough/slider rules in style.css, not from this.
        Gtk.Settings.get_default().set_property("gtk-overlay-scrolling", False)

        provider = Gtk.CssProvider()
        provider.load_from_path(_STYLE_CSS)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_title(OS_RELEASE.rebrand("pearOS NiceC0re Installer"))
        self.window.set_decorated(False)
        self.window.set_resizable(False)

        # set_default_size() as a fallback: fullscreen() below can race the
        # Wayland surface configure on first map, leaving the window sized to
        # content only. Pre-sizing to the monitor geometry means that even if
        # the fullscreen request is briefly ignored, the window still covers
        # the screen instead of shrink-wrapping its content.
        monitors = Gdk.Display.get_default().get_monitors()
        if monitors.get_n_items() > 0:
            geo = monitors.get_item(0).get_geometry()
            self.window.set_default_size(geo.width, geo.height)

        theme_mode = state_mod.read_tmp("theme_mode")
        if theme_mode is None:
            # No explicit choice made yet (the "look" page hasn't been
            # reached/completed) - every page up to that point used to
            # default to light regardless, clashing with the session's
            # actual dark native widgets (checkboxes, comboboxes, ...).
            # look.py's own on_show() already calls this same method to
            # preselect its light/dark option; __main__ just never did,
            # for the window-wide dark-mode class itself.
            theme_mode = self.state.detect_default_look_mode()
        self.set_dark_mode(theme_mode == "dark")

        root_overlay = Gtk.Overlay()
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        root_overlay.set_child(self.stack)

        self._build_pages()

        if state_mod.IS_TEST_MODE:
            banner = Gtk.Label(label="Test mode — system unchanged.")
            banner.add_css_class("test-banner")
            banner.set_valign(Gtk.Align.START)
            banner.set_hexpand(True)
            root_overlay.add_overlay(banner)

        self.window.set_child(root_overlay)
        self.window.fullscreen()
        self.window.present()
        GLib.idle_add(lambda: (self.window.fullscreen(), False)[1])

        # Only used by developers doing manual/visual QA (see the plan's
        # verification section) to jump straight to one page instead of
        # clicking through the whole wizard.
        start_page = os.environ.get("GTKAPP_QA_START", "hello")
        self.go_to(start_page)

    def _build_pages(self):
        # Local imports: page modules import from this package, avoid cycles.
        from .pages.hello import HelloPage
        from .pages.language import LanguagePage
        from .pages.country import CountryPage
        from .pages.written_spoken import WrittenSpokenPage
        from .pages.keymap import KeymapPage
        from .pages.timezone import TimezonePage
        from .pages.accessibility import AccessibilityPage
        from .pages.wifi import WifiPage
        from .pages.data_privacy import DataPrivacyPage
        from .pages.migration_assistant import MigrationAssistantPage
        from .pages.pearid import PearIDPage
        from .pages.user import UserPage
        from .pages.location_services import LocationServicesPage
        from .pages.analytics import AnalyticsPage
        from .pages.screen_time import ScreenTimePage
        from .pages.piri import PiriPage
        from .pages.touchid_enable import TouchIDEnablePage
        from .pages.touchid_setup import TouchIDSetupPage
        from .pages.look import LookPage
        from .pages.update import UpdatePage
        from .pages.welcome import WelcomePage
        from .pages.agreement import AgreementPage
        from .pages.finish import FinishPage

        page_classes = {
            "hello": HelloPage,
            "language": LanguagePage,
            "country": CountryPage,
            "written_spoken": WrittenSpokenPage,
            "keymap": KeymapPage,
            "timezone": TimezonePage,
            "accessibility": AccessibilityPage,
            "wifi": WifiPage,
            "data_privacy": DataPrivacyPage,
            "migration_assistant": MigrationAssistantPage,
            "pearid": PearIDPage,
            "user": UserPage,
            "location_services": LocationServicesPage,
            "analytics": AnalyticsPage,
            "screen_time": ScreenTimePage,
            "piri": PiriPage,
            "touchid_enable": TouchIDEnablePage,
            "touchid_setup": TouchIDSetupPage,
            "look": LookPage,
            "update": UpdatePage,
            "welcome": WelcomePage,
            "agreement": AgreementPage,
            "finish": FinishPage,
        }
        for name in PAGE_ORDER:
            page = page_classes[name](self)
            self.pages[name] = page
            self.stack.add_named(page.widget, name)


def main():
    app = WizardApp()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
