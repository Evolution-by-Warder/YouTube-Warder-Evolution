# -*- coding: utf-8 -*-
"""Small blue settings screen; no account tokens or keys are committed to Git."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import ConfigSubsection, ConfigText, config, configfile
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

try:
    from Screens.VirtualKeyBoard import VirtualKeyboard
except ImportError:
    from Screens.VirtualKeyBoard import VirtualKeyBoard as VirtualKeyboard

from .skin import SETTINGS_SKIN

if not hasattr(config.plugins, "warderyoutube"):
    config.plugins.warderyoutube = ConfigSubsection()
if not hasattr(config.plugins.warderyoutube, "api_key"):
    config.plugins.warderyoutube.api_key = ConfigText(default="", fixed_size=False)


def get_api_key():
    return config.plugins.warderyoutube.api_key.value.strip()


class WarderYouTubeSettings(Screen):
    skin = SETTINGS_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self["title"] = Label("YouTube - Warder Evolution / Settings")
        self["description"] = Label(
            "Search currently uses the official YouTube Data API. "
            "API key is optional when yt-dlp is installed. "
            "Playback is experimental and depends on installed yt-dlp."
        )
        self["key_state"] = Label("")
        self["warning"] = Label(
            "The key is stored in the receiver's Enigma2 settings without encryption. "
            "Do not share screenshots while entering it."
        )
        self["footer"] = Label("OK/GREEN: Enter or replace key     YELLOW: Clear key     EXIT: Back")
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions"],
            {"ok": self.prompt_key, "green": self.prompt_key,
             "yellow": self.confirm_clear, "red": self.close,
             "cancel": self.close},
            -1
        )
        self.refresh()

    def refresh(self):
        self["key_state"].setText(
            "API key: configured" if get_api_key() else "API key: not configured (yt-dlp alternative)"
        )

    def prompt_key(self):
        # Never reveal a stored key when opening the keyboard.
        self.session.openWithCallback(
            self.key_received, VirtualKeyboard,
            title="Paste your YouTube Data API key (replaces existing)",
            text=""
        )

    def key_received(self, value):
        if value is None:
            return
        value = value.strip()
        if not value or any(c.isspace() for c in value) or len(value) > 256:
            self.session.open(
                MessageBox, "Invalid or empty key. Existing settings were kept.",
                type=MessageBox.TYPE_ERROR, timeout=5
            )
            return
        config.plugins.warderyoutube.api_key.value = value
        config.plugins.warderyoutube.api_key.save()
        configfile.save()
        self.refresh()

    def confirm_clear(self):
        self.session.openWithCallback(
            self.clear_key, MessageBox,
            "Remove the saved API key from this receiver?",
            type=MessageBox.TYPE_YESNO, default=False
        )

    def clear_key(self, confirmed):
        if confirmed:
            config.plugins.warderyoutube.api_key.value = ""
            config.plugins.warderyoutube.api_key.save()
            configfile.save()
            self.refresh()
