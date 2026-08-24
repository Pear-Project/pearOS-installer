"""'Data & Privacy' - informational screen (matches the real macOS Setup
Assistant step of the same name): explains what leaves the device and why,
no toggles here (those live on the later Location Services / Analytics
pages) - just acknowledgement + Continue."""
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..osrelease import OS_RELEASE
from ..widgets import page_root, make_title

BODY_TEXT = (
    "Protecting your data and respecting your privacy are built into "
    "{name}. Some features require an Internet connection and rely on "
    "data to work, such as looking up locations, dates, or other "
    "information.\n\n"
    "Data associated with your account may be processed by {name} and "
    "used to, for example, enable features you request, improve our "
    "products and services, and enhance your experience. Data that "
    "could be used to identify you personally will be handled as "
    "described in the {name} Privacy Policy.\n\n"
    "You can review what data is shared on later screens (Location "
    "Services, Analytics), and change these choices at any time in "
    "System Settings."
)


class DataPrivacyPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        content.set_hexpand(True)
        content.set_vexpand(True)
        content.set_valign(Gtk.Align.CENTER)
        self.title = make_title("Data & Privacy")
        content.append(self.title)

        body_text = OS_RELEASE.rebrand(BODY_TEXT.format(name=OS_RELEASE.pretty_name))
        self.body = Gtk.Label(label=body_text)
        self.body.add_css_class("description")
        self.body.set_wrap(True)
        self.body.set_justify(Gtk.Justification.CENTER)
        self.body.set_max_width_chars(64)
        self.body.set_margin_top(16)
        self.body.set_margin_start(40)
        self.body.set_margin_end(40)
        self.body.set_halign(Gtk.Align.CENTER)
        content.append(self.body)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        pass

    def _on_back(self):
        self.app.go_to("wifi")

    def _on_continue(self):
        self.app.go_to("migration_assistant")
