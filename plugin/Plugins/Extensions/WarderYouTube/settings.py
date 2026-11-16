# -*- coding: utf-8 -*-
"""Small blue settings screen; no account tokens or keys are committed to Git."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Components.config import ConfigSelection, ConfigSubsection, ConfigText, ConfigYesNo, config, configfile
from Screens.Screen import Screen

from .skin import SETTINGS_SKIN
from .resolver import is_available
from .i18n import tr as _
from .api_key_file import read_manual_key
from .data_auth import account_available
from .menu_compat import selected_index

QUALITY_VALUES = ("360", "480", "720", "1080", "1440", "2160")
PLAYER_VALUES = ("auto", "gst", "exte")
PLAYER_LABELS = {"auto": "Automaticky", "gst": "gstplayer", "exte": "exteplayer3"}

if not hasattr(config.plugins, "warderyoutube"):
    config.plugins.warderyoutube = ConfigSubsection()
if not hasattr(config.plugins.warderyoutube, "api_key"):
    config.plugins.warderyoutube.api_key = ConfigText(default="", fixed_size=False)
if not hasattr(config.plugins.warderyoutube, "max_quality"):
    config.plugins.warderyoutube.max_quality = ConfigSelection(
        choices=[(value, value + "p") for value in QUALITY_VALUES], default="720"
    )


if not hasattr(config.plugins.warderyoutube, "player_mode"):
    config.plugins.warderyoutube.player_mode = ConfigSelection(
        choices=[("auto", "Automaticky"), ("gst", "gstplayer"), ("exte", "exteplayer3")],
        default="auto"
    )


if not hasattr(config.plugins.warderyoutube, "show_main_menu"):
    config.plugins.warderyoutube.show_main_menu = ConfigYesNo(default=False)


def get_player_mode():
    value = config.plugins.warderyoutube.player_mode.value
    return value if value in PLAYER_VALUES else "auto"


def available_player_modes():
    """Only installed and registered receivers' players; auto always works."""
    try:
        from .player import service_player_available
        return ("auto",) + tuple(
            mode for mode in ("gst", "exte") if service_player_available(mode))
    except (ImportError, AttributeError, RuntimeError, TypeError):
        return ("auto",)


def get_api_key():
    # Enigma2 settings take precedence. A root-owned, mode 0600 manual file
    # is read on demand when the GUI setting is empty (including at startup).
    configured = config.plugins.warderyoutube.api_key.value.strip()
    return configured or read_manual_key()


def get_quality():
    value = config.plugins.warderyoutube.max_quality.value
    return value if value in QUALITY_VALUES else "720"


class WarderYouTubeSettings(Screen):
    """Native Enigma2 list with the same menu semantics as Warder Radio."""
    skin = SETTINGS_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        add_header(self)
        self["title"] = Label("YouTube Warder Evolution / " + _("Settings"))
        self["description"] = Label(_("Choose a setting and press OK to change it."))
        self["options"] = MenuList([])
        # Retain legacy status labels, but put values in the actual list.
        for name in ("section_search", "section_playback", "section_privacy",
                     "key_state", "quality", "resolver_state", "warning", "footer"):
            self[name] = Label("")
        self["status"] = Label("")
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Select"))
        self["key_yellow"] = Label(_("Player"))
        self["key_blue"] = Label(_("Change quality"))
        self._notice = ""
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "DirectionActions"],
            {"ok": self.primary_action, "green": self.primary_action,
             "yellow": self.toggle_player, "blue": self.toggle_quality,
             "up": self.up, "down": self.down,
             "red": self.back, "cancel": self.back}, -1)
        self.refresh()

    def _index(self):
        index = selected_index(self["options"])
        return min(3, max(0, index))

    def refresh(self):
        index = self._index()
        signed_in = account_available()
        mode = get_player_mode()
        enabled = config.plugins.warderyoutube.show_main_menu.value is True
        self["options"].setList([
            _("YouTube account") + ": " + (_("Signed in") if signed_in else _("Not signed in")),
            _("Player") + ": " + _(PLAYER_LABELS[mode]),
            _("Maximum video quality") + ": " + get_quality() + "p",
            _("Show in Enigma2 main menu") + ": " + (_("Yes") if enabled else _("No")),
        ])
        self["options"].moveToIndex(index)
        self["key_state"].setText(_("Signed in") if signed_in else _("Not signed in"))
        self["quality"].setText(_("Maximum video quality") + ": " + get_quality() + "p")
        unavailable = mode != "auto" and mode not in available_player_modes()
        self["resolver_state"].setText(
            _("Player") + ": " + _(PLAYER_LABELS[mode]) +
            (" (" + _("Unavailable; using Automatic") + ")" if unavailable else "") +
            "\n" + "yt-dlp: " + (_("Available") if is_available() else _("Not installed")))
        self["warning"].setText(
            _("Your Google password is never entered in this plugin.") +
            "\n" + _("Account access is stored locally on this receiver."))
        self["footer"].setText(_("OK/Green: select  Yellow: player  Blue: quality  Exit: back"))
        self.show_notice()

    def show_notice(self):
        self["status"].setText(
            self._notice or _("OK/Green: select  Yellow: player  Blue: quality  Exit: back"))

    def up(self):
        self["options"].up()
        self._notice = ""
        self.show_notice()

    def down(self):
        self["options"].down()
        self._notice = ""
        self.show_notice()

    def primary_action(self):
        index = self._index()
        if index == 0:
            self.close("account")
        elif index == 1:
            self.toggle_player()
        elif index == 2:
            self.toggle_quality()
        else:
            self.toggle_main_menu()

    def toggle_main_menu(self):
        setting = config.plugins.warderyoutube.show_main_menu
        setting.value = not (setting.value is True)
        setting.save()
        configfile.save()
        self._notice = _("Restart GUI to apply main menu change.")
        self.refresh()

    def toggle_player(self):
        current = get_player_mode()
        setting = config.plugins.warderyoutube.player_mode
        setting.value = PLAYER_VALUES[(PLAYER_VALUES.index(current) + 1) % len(PLAYER_VALUES)]
        setting.save()
        configfile.save()
        self._notice = ""
        self.refresh()

    def toggle_quality(self):
        current = get_quality()
        setting = config.plugins.warderyoutube.max_quality
        setting.value = QUALITY_VALUES[(QUALITY_VALUES.index(current) + 1) % len(QUALITY_VALUES)]
        setting.save()
        configfile.save()
        self._notice = ""
        self.refresh()

    def back(self):
        self.close()
