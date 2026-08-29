"""'Select Your Country or Region' - now the second real page (right after
the hello animation), matching the real macOS Setup Assistant flow this
wizard's design is modeled on. If online, the two most likely countries
(IP geolocation, then the installed locale's own region as a second
guess) are floated to the top of the list and the first is preselected -
purely a convenience reorder, every other country is still right there
below, unchanged and just as selectable."""
import threading

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

from .. import network_backend as netbackend
from ..widgets import page_root, make_title
from .common import SEPARATOR, SelectList, make_worldmap

# Only needs entries for the locales this app actually ships translations
# for (see i18n's I18N_DIR) - a country.py-spelling lookup for the second,
# locale-based guess, not a general-purpose region-code table.
_LOCALE_REGION_TO_COUNTRY = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada",
    "AU": "Australia", "FR": "France", "PT": "Portugal", "HU": "Hungary",
    "MX": "Mexico", "RU": "Russia", "JP": "Japan", "RO": "Romania",
    "SE": "Sweden", "IT": "Italy", "DE": "Germany", "ES": "Spain",
    "BR": "Brazil", "CZ": "Czech Republic", "CN": "China",
}

COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina",
    "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
    "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon",
    "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia",
    "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador",
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany",
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India",
    "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Mauritania", "Mauritius", "Mexico", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria",
    "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru",
    "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Samoa", "San Marino", "Saudi Arabia", "Senegal", "Serbia",
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Korea",
    "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand",
    "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay",
    "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam",
    "Yemen", "Zambia", "Zimbabwe",
]


class CountryPage:
    def __init__(self, app):
        self.app = app
        self._suggestions_applied = False

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        content.set_hexpand(True)
        content.append(make_worldmap())
        self.title = make_title("Select Your Country or Region")
        content.append(self.title)

        items = [(c, c) for c in COUNTRIES]
        self.select_list = SelectList(items)
        content.append(self.select_list.widget)

        self.widget, self.card = page_root(
            content, on_back=self._on_back, on_forward=self._on_continue, forward_label="Continue",
            show_accessibility_footer=True,
        )

    def on_show(self):
        if self.app.state.country:
            self.select_list.select_value(self.app.state.country)
            return
        if self._suggestions_applied:
            return
        self._suggestions_applied = True
        if not netbackend.has_internet():
            return
        threading.Thread(target=self._geolocate, daemon=True).start()

    def _geolocate(self):
        guess = netbackend.geolocate_country()
        GLib.idle_add(self._apply_suggestions, guess)

    def _locale_guess(self):
        lng = getattr(self.app.state, "lng", None) or ""
        region = lng.split("_")[-1].split(".")[0].upper() if "_" in lng else None
        return _LOCALE_REGION_TO_COUNTRY.get(region)

    def _apply_suggestions(self, ip_guess):
        # Locale guess first (e.g. "United States" for an en_US install),
        # then the IP-geolocated one, then a divider before the full
        # alphabetical list - matching order requested over IP-guess-first.
        top = []
        for candidate in (self._locale_guess(), ip_guess):
            if candidate in COUNTRIES and candidate not in top:
                top.append(candidate)
        if not top:
            return False
        rest = [c for c in COUNTRIES if c not in top]
        items = [(c, c) for c in top]
        items.append((SEPARATOR, None))
        items.extend((c, c) for c in rest)
        self.select_list.set_items(items)
        self.select_list.select_value(top[0])
        return False

    def _on_back(self):
        self.app.go_to("hello")

    def _on_continue(self):
        country = self.select_list.selected_value()
        if not country:
            self.app.show_alert("You must select one country or region from the list")
            return
        self.app.state.select_country(country)
        self.app.state.wifi_entry_forward = True
        self.app.go_to("wifi")
