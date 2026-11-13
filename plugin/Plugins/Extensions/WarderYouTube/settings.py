# -*- coding: utf-8 -*-
"""Small blue settings screen; no account tokens or keys are committed to Git."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import ConfigSelection, ConfigSubsection, ConfigText, config, configfile
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

from .skin import SETTINGS_SKIN
from .resolver import is_available
from .i18n import tr as _
from .confirm_ui import WarderYouTubeConfirm
from .api_key_file import read_manual_key, VALID_KEY

QUALITY_VALUES = ("360", "480", "720", "1080", "1440", "2160")

if not hasattr(config.plugins, "warderyoutube"):
    config.plugins.warderyoutube = ConfigSubsection()
if not hasattr(config.plugins.warderyoutube, "api_key"):
    config.plugins.warderyoutube.api_key = ConfigText(default="", fixed_size=False)
if not hasattr(config.plugins.warderyoutube, "max_quality"):
    config.plugins.warderyoutube.max_quality = ConfigSelection(
        choices=[(value, value + "p") for value in QUALITY_VALUES], default="720"
    )


def get_api_key():
    # Enigma2 settings take precedence. A root-owned, mode 0600 manual file
    # is read on demand when the GUI setting is empty (including at startup).
    configured = config.plugins.warderyoutube.api_key.value.strip()
    return configured or read_manual_key()


def get_quality():
    value = config.plugins.warderyoutube.max_quality.value
    return value if value in QUALITY_VALUES else "720"


class WarderYouTubeSettings(Screen):
    skin = SETTINGS_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self["title"] = Label("YouTube Warder Evolution / " + _("Settings"))
        self["section_search"] = Label(_("Search").upper())
        self["section_playback"] = Label(_("Playback").upper())
        self["section_privacy"] = Label(_("Privacy").upper())
        self["status"] = Label(_("Keep live TV audio"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("API key"))
        self["key_yellow"] = Label(_("Delete saved key"))
        self["key_blue"] = Label(_("Change quality"))
        self["description"] = Label(
            _("About settings") + "\n" + _("Language from Enigma2")
        )
        self["key_state"] = Label("")
        self._key_dialog_open = False
        self["quality"] = Label("")
        self["resolver_state"] = Label("")
        self["warning"] = Label(
            _("API stored unencrypted") + "\n" +
            _("API key visible while typing")
        )
        self["footer"] = Label(
            _("OK/Green: API key   Blue: quality   Yellow: remove key   Exit: back")
        )
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions"],
            {"ok": self.prompt_key, "green": self.prompt_key,
             "yellow": self.confirm_clear, "blue": self.toggle_quality,
             "red": self.close,
             "cancel": self.close},
            -1
        )
        self.refresh()

    def refresh(self):
        in_config = bool(config.plugins.warderyoutube.api_key.value.strip())
        in_file = bool(read_manual_key()) if not in_config else False
        # Never put a saved credential into a GUI Label, even when the user
        # selects the API key row. Fixed-length stars do not expose key length.
        self["key_state"].setText(
            _("API key") + ": ********" + (" (" + _("manual file") + ")" if in_file else "")
            if in_config or in_file else
            _("API kľúč: nenastavený (vyhľadávanie cez yt-dlp)")
        )
        self["quality"].setText(_("Maximum video quality") + ": %sp" % get_quality())
        self["resolver_state"].setText(
            _("yt-dlp: dostupný (vyhľadávanie aj záložné prehrávanie)") if is_available() else
            _("yt-dlp: nenainštalovaný (na prehrávanie nie je nutný)")
        )

    def toggle_quality(self):
        setting = config.plugins.warderyoutube.max_quality
        current = get_quality()
        setting.value = QUALITY_VALUES[
            (QUALITY_VALUES.index(current) + 1) % len(QUALITY_VALUES)
        ]
        setting.save()
        configfile.save()
        self.refresh()

    def prompt_key(self):
        if self._key_dialog_open:
            return
        # Show the saved value ONLY as asterisks. Changing it is an explicit
        # second action; cancelling the confirmation leaves the key intact.
        if get_api_key():
            self._key_dialog_open = True
            try:
                self.session.openWithCallback(
                    self._key_change_confirmed, WarderYouTubeConfirm,
                    _("API key") + ": ********" + "\\n" +
                    _("Change saved API key?"))
            except Exception:
                self._key_dialog_open = False
        else:
            self._open_key_editor()

    def _key_change_confirmed(self, confirmed):
        self._key_dialog_open = False
        if confirmed:
            self._open_key_editor()

    def _open_key_editor(self):
        if self._key_dialog_open:
            return
        # Newly typed text is visible and editable until GREEN/Confirm.
        # The previously saved credential is never prefilled or shown.
        from .keyboard import WarderYouTubeKeyboard
        try:
            from .native_keyboard import WarderNativeSearchKeyboard
        except ImportError:
            WarderNativeSearchKeyboard = None
        editor = WarderNativeSearchKeyboard or WarderYouTubeKeyboard
        self._key_dialog_open = True
        try:
            self.session.openWithCallback(
                self.key_received, editor,
                value="", title=_("Enter API key"), secret=False, limit=160
            )
        except Exception:
            self._key_dialog_open = False

    def key_received(self, value):
        self._key_dialog_open = False
        if value is None:
            return
        value = value.strip()
        if not VALID_KEY.fullmatch(value):
            self["status"].setText(_("Invalid API key format."))
            return
        config.plugins.warderyoutube.api_key.value = value
        config.plugins.warderyoutube.api_key.save()
        configfile.save()
        self.refresh()

    def confirm_clear(self):
        self.session.openWithCallback(
            self.clear_key, WarderYouTubeConfirm,
            _("Delete saved key") + "?"
        )

    def clear_key(self, confirmed):
        if confirmed:
            config.plugins.warderyoutube.api_key.value = ""
            config.plugins.warderyoutube.api_key.save()
            configfile.save()
            self.refresh()
            if read_manual_key():
                self["status"].setText(_("Manual API key file remains active."))
