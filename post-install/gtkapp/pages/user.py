"""Port of templates/user.html + the user-related parts of engine.js
(validateUser, saveUser, check_passwords_match, checkFormValidity,
load_profile_pictures) - matches macOS's real "Create a Mac Account"
layout: left-aligned title/paragraph, avatar row, then the same
pill-shaped .textbox fields pearid.py's sign-in uses (a closer screenshot
showed a focused field with a clear rounded-pill border and blue focus
ring, not the plain underline an earlier, blurrier one looked like) -
measured off a real screenshot of this exact page. No "Allow computer
account password to be reset with your Apple Account" checkbox: there's
no PearID-linked local-password-reset feature behind it to offer.

Unlike the reference, this keeps a Hostname field: real macOS asks for
the computer's network name on a separate "Name Your Mac" screen, which
this app doesn't have a place for elsewhere, so it stays here rather than
going unset."""
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, GdkPixbuf

from ..widgets import page_root

# Measured off a real macOS Setup Assistant screenshot of this exact page
# (text/avatars/fields all started at x=158 in a 723-wide card, and the
# field/avatar-row width was ~410px) and scaled to this app's 800-wide
# card (factor 799/723 ~= 1.105) - same values as the other "detail page"
# layouts (migration_assistant.py etc) and country.py's list width.
_LEFT_MARGIN = 176
_FIELD_WIDTH = 453
_AVATAR_SIZE = 56


class UserPage:
    def __init__(self, app):
        self.app = app

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)

        self.title = Gtk.Label(label="Create a Computer Account")
        self.title.add_css_class("title")
        self.title.set_halign(Gtk.Align.START)
        self.title.set_margin_start(_LEFT_MARGIN)
        self.title.set_margin_top(70)
        content.append(self.title)

        self.description = Gtk.Label(
            label="Fill out the following informations to create your computer account."
        )
        self.description.add_css_class("description")
        self.description.set_wrap(True)
        self.description.set_justify(Gtk.Justification.LEFT)
        self.description.set_halign(Gtk.Align.START)
        self.description.set_margin_start(_LEFT_MARGIN)
        self.description.set_margin_top(4)
        self.description.set_max_width_chars(56)
        content.append(self.description)

        self.pictures_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=17)
        self.pictures_row.set_halign(Gtk.Align.START)

        # macOS's own picker scrolls horizontally with rubber-band overscroll
        # rather than just laying every avatar out edge to edge - GTK4's
        # ScrolledWindow already does kinetic/elastic overscroll natively,
        # this is just wiring it up. PolicyType.NEVER on vertical since this
        # never needs to scroll that way; EXTERNAL keeps the horizontal
        # scrollbar chrome from ever reserving space/being drawn, matching
        # how macOS hides it here too.
        self.pictures_scroller = Gtk.ScrolledWindow()
        self.pictures_scroller.set_policy(Gtk.PolicyType.EXTERNAL, Gtk.PolicyType.NEVER)
        self.pictures_scroller.set_min_content_width(_FIELD_WIDTH)
        self.pictures_scroller.set_max_content_width(_FIELD_WIDTH)
        self.pictures_scroller.set_min_content_height(_AVATAR_SIZE + 12)
        self.pictures_scroller.set_halign(Gtk.Align.START)
        self.pictures_scroller.set_margin_start(_LEFT_MARGIN)
        self.pictures_scroller.set_margin_top(26)
        self.pictures_scroller.set_child(self.pictures_row)
        content.append(self.pictures_scroller)
        self._picture_buttons = []
        self.selected_picture = None

        form = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        form.set_halign(Gtk.Align.START)
        form.set_margin_start(_LEFT_MARGIN)
        form.set_margin_top(14)

        def _field(placeholder):
            entry = Gtk.Entry(placeholder_text=placeholder)
            entry.add_css_class("textbox")
            entry.set_size_request(_FIELD_WIDTH, -1)
            return entry

        self.full_name = _field("Full Name")
        form.append(self.full_name)

        self.account_name = _field("Account Name")
        form.append(self.account_name)

        self.account_hint = Gtk.Label(label="This will be the name of your home folder")
        self.account_hint.add_css_class("account-name-hint")
        self.account_hint.set_halign(Gtk.Align.START)
        form.append(self.account_hint)

        # Kept alive (pre-filled, just never added to the visible form) for
        # save_user() below, which still needs a hostname - not shown per
        # explicit instruction, since it's always this fixed default and
        # there's no real reason for a user to want to change it here.
        self.hostname = Gtk.Entry(text="pearOS-machine")

        password_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        password_row.set_margin_top(8)
        half_width = (_FIELD_WIDTH - 15) // 2
        self.password = Gtk.PasswordEntry(placeholder_text="Password", show_peek_icon=True)
        self.password.add_css_class("textbox")
        self.password.set_size_request(half_width, -1)
        self.password_confirm = Gtk.PasswordEntry(
            placeholder_text="Verify Password", show_peek_icon=True
        )
        self.password_confirm.add_css_class("textbox")
        self.password_confirm.set_size_request(half_width, -1)
        password_row.append(self.password)
        password_row.append(self.password_confirm)
        form.append(password_row)

        self.password_check = Gtk.Label(label="")
        self.password_check.add_css_class("password-check")
        self.password_check.set_halign(Gtk.Align.START)
        form.append(self.password_check)

        content.append(form)

        for entry in (self.full_name, self.account_name, self.hostname):
            entry.connect("changed", self._on_form_changed)
        self.password.connect("changed", self._on_password_changed)
        self.password_confirm.connect("changed", self._on_password_changed)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue"
        )

    def on_show(self):
        self.title.set_label(self.app.t("user.title", "Create a Computer Account"))
        self.description.set_label(
            self.app.t(
                "user.description",
                "Fill out the following informations to create your computer account.",
            )
        )
        self.card.forward_button.set_label(self.app.t("user.continue", "Continue"))
        self.full_name.set_placeholder_text(self.app.t("user.fullNamePlaceholder", "Full Name"))
        self.account_name.set_placeholder_text(
            self.app.t("user.accountNamePlaceholder", "Account Name")
        )
        self.account_hint.set_label(
            self.app.t("user.accountNameHint", "This will be the name of your home folder")
        )
        self.password.set_property(
            "placeholder-text", self.app.t("user.passwordPlaceholder", "Password")
        )
        self.password_confirm.set_property(
            "placeholder-text", self.app.t("user.verifyPasswordPlaceholder", "Verify Password")
        )
        self._load_profile_pictures()
        self._update_form_validity()

    def _load_profile_pictures(self):
        if self._picture_buttons:
            return
        paths = self.app.state.list_profile_pictures()
        for path in paths:
            btn = Gtk.ToggleButton()
            btn.add_css_class("flat")
            btn.add_css_class("profile-picture-item")
            # "flat" alone wasn't enough - the theme's :checked state still
            # painted its own square-cornered background/indicator behind
            # our content (visible as a colored wedge on the selected
            # avatar only, since that's the only one in the checked state).
            # border-radius in CSS only clips this widget's own background/
            # border, not arbitrary painting underneath a child - forcing
            # overflow clipping on the button itself is what actually
            # confines *everything* drawn inside it to the circle, theme
            # decoration included.
            btn.set_overflow(Gtk.Overflow.HIDDEN)
            # GtkPicture.measure() reports the source image's intrinsic size
            # (these are 128x128) as its natural size no matter what
            # set_size_request() says - that's only a minimum, not a cap,
            # and Gtk.Overflow.HIDDEN on a wrapping box only clips painting,
            # not layout, so it doesn't stop the natural-size request from
            # propagating either (see make_worldmap() in common.py for the
            # same bug/fix). With 8 of these side by side that alone was
            # enough to blow the whole card way past 800px wide. Pre-scaling
            # the pixbuf to the exact display size is what actually fixes
            # it: its intrinsic size *is* the target size now, nothing left
            # to clip.
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                path, _AVATAR_SIZE, _AVATAR_SIZE, True
            )
            pic = Gtk.Picture.new_for_pixbuf(pixbuf)
            pic.set_content_fit(Gtk.ContentFit.COVER)
            pic.set_can_shrink(True)
            btn.set_child(pic)
            btn.connect("toggled", self._on_picture_toggled, path, btn)
            self.pictures_row.append(btn)
            self._picture_buttons.append(btn)
        if self._picture_buttons:
            self._picture_buttons[0].set_active(True)

    def _on_picture_toggled(self, btn, path, this_btn):
        if not btn.get_active():
            return
        for other in self._picture_buttons:
            if other is not this_btn:
                other.set_active(False)
            other.remove_css_class("selected")
        this_btn.add_css_class("selected")
        self.selected_picture = path
        self.app.state.select_profile_picture(path)
        self._update_form_validity()

    def _on_password_changed(self, _entry):
        p1 = self.password.get_text()
        p2 = self.password_confirm.get_text()
        self.password_check.remove_css_class("match")
        self.password_check.remove_css_class("mismatch")
        if p1 == "" and p2 == "":
            self.password_check.set_label("")
        elif p1 == p2 and p1 != "":
            self.password_check.set_label("✓ Passwords match")
            self.password_check.add_css_class("match")
        elif p2 != "":
            self.password_check.set_label("✗ Passwords do not match")
            self.password_check.add_css_class("mismatch")
        else:
            self.password_check.set_label("")
        self._update_form_validity()

    def _on_form_changed(self, _entry):
        self._update_form_validity()

    def _update_form_validity(self):
        ok = (
            self.full_name.get_text().strip() != ""
            and self.account_name.get_text().strip() != ""
            and self.hostname.get_text().strip() != ""
            and self.password.get_text() != ""
            and self.password_confirm.get_text() != ""
            and self.password.get_text() == self.password_confirm.get_text()
            and self.selected_picture is not None
        )
        self.card.forward_button.set_sensitive(ok)

    def _on_back(self):
        self.app.go_to("pearid")

    def _on_continue(self):
        err = self.app.state.save_user(
            self.full_name.get_text(),
            self.account_name.get_text(),
            self.hostname.get_text(),
            self.password.get_text(),
            self.password_confirm.get_text(),
            self.selected_picture,
        )
        if err:
            self.app.show_alert(err)
            return
        self.app.go_to("touchid_enable")
