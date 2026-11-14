# -*- coding: utf-8 -*-
"""Small blue settings screen; no account tokens or keys are committed to Git."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import ConfigSelection, ConfigSubsection, ConfigText, config, configfile
from Screens.Screen import Screen

from .skin import SETTINGS_SKIN
from .resolver import is_available
from .i18n import tr as _
from .api_key_file import read_manual_key
from .data_auth import account_available

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
    """Account-first, simple settings: no personal API-key editor in the UI."""
    skin = SETTINGS_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        add_header(self)
        self["title"] = Label("YouTube Warder Evolution / " + _("Settings"))
        self["section_search"] = Label(_("YouTube account").upper())
        self["section_playback"] = Label(_("Playback").upper())
        self["section_privacy"] = Label(_("Privacy").upper())
        self["description"] = Label(
            _("About settings") + "\n" + _("Language from Enigma2")
        )
        self["key_state"] = Label("")
        self["quality"] = Label("")
        self["resolver_state"] = Label("")
        self["warning"] = Label("")
        self["status"] = Label("")
        self["footer"] = Label("")
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Manage account"))
        self["key_yellow"] = Label(_("Player"))
        self["key_blue"] = Label(_("Change quality"))
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions"],
            {"ok": self.primary_action, "green": self.primary_action,
             "yellow": self.toggle_player, "blue": self.toggle_quality,
             "red": self.back, "cancel": self.back},
            -1
        )
        self.refresh()

    def refresh(self):
        connected = account_available()
        self["key_green"].setText(
            _("Manage account") if connected else _("Sign in to YouTube"))
        self["key_state"].setText(
            _("Signed in") + "\n" + _("Your YouTube subscriptions are available.")
            if connected else _("Not signed in") + "\n" + _("Sign in using a TV code."))
        self["quality"].setText(
            _("Maximum video quality") + ": %sp" % get_quality())
        available = available_player_modes()
        selected = get_player_mode()
        effective = selected if selected in available else "auto"
        self["resolver_state"].setText(
            _("Player") + ": " + _(PLAYER_LABELS[effective]) +
            (" (" + _("Unavailable; using Automatic") + ")"
             if selected != effective else "") + "\n" +
            ("yt-dlp: " + (_("Available") if is_available()
                          else _("Not installed")))
        )
        self["warning"].setText(
            _("Your Google password is never entered in this plugin.") + "\n" +
            _("Account access is stored locally on this receiver."))
        self["status"].setText(
            _("Playback settings apply to all video sections."))
        self["footer"].setText(
            _("OK/Green: account   Yellow: player   Blue: quality   Exit: back"))

    def primary_action(self):
        # Home will switch to the account management in the Odbery pane.
        self.close("account")

    def back(self):
        self.close()

    def toggle_player(self):
        choices = available_player_modes()
        current = get_player_mode()
        if current not in choices:
            current = "auto"
        setting = config.plugins.warderyoutube.player_mode
        setting.value = choices[(choices.index(current) + 1) % len(choices)]
        setting.save()
        configfile.save()
        self.refresh()

    def toggle_quality(self):
        setting = config.plugins.warderyoutube.max_quality
        current = get_quality()
        setting.value = QUALITY_VALUES[
            (QUALITY_VALUES.index(current) + 1) % len(QUALITY_VALUES)
        ]
        setting.save()
        configfile.save()
        self.refresh()
