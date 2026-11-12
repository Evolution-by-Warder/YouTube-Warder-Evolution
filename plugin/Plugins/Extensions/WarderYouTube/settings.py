# -*- coding: utf-8 -*-
"""Small blue settings screen; no account tokens or keys are committed to Git."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.config import ConfigSelection, ConfigSubsection, ConfigText, config, configfile
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

try:
    from Screens.VirtualKeyBoard import VirtualKeyboard
except ImportError:
    from Screens.VirtualKeyBoard import VirtualKeyBoard as VirtualKeyboard

from .skin import SETTINGS_SKIN
from .resolver import is_available

if not hasattr(config.plugins, "warderyoutube"):
    config.plugins.warderyoutube = ConfigSubsection()
if not hasattr(config.plugins.warderyoutube, "api_key"):
    config.plugins.warderyoutube.api_key = ConfigText(default="", fixed_size=False)
if not hasattr(config.plugins.warderyoutube, "max_quality"):
    config.plugins.warderyoutube.max_quality = ConfigSelection(
        choices=[("360", "360p"), ("720", "720p")], default="720"
    )


def get_api_key():
    return config.plugins.warderyoutube.api_key.value.strip()


def get_quality():
    value = config.plugins.warderyoutube.max_quality.value
    return value if value in ("360", "720") else "720"


class WarderYouTubeSettings(Screen):
    skin = SETTINGS_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self["title"] = Label("YouTube Warder Evolution / Settings")
        self["description"] = Label(
            "Vyhľadávanie: API kľúč alebo yt-dlp. "
            "Prehrávanie: vlastný resolver Warder Radio; yt-dlp iba záloha."
        )
        self["key_state"] = Label("")
        self["quality"] = Label("")
        self["resolver_state"] = Label("")
        self["warning"] = Label(
            "API kľúč je uložený v Enigma2 bez šifrovania. "
            "Pri jeho zadávaní nezdieľajte snímky obrazovky."
        )
        self["footer"] = Label(
            "OK/ZELENÉ: API kľúč   MODRÉ: 360/720p   ŽLTÉ: vymazať   EXIT: späť"
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
        self["key_state"].setText(
            "API kľúč: nastavený" if get_api_key() else "API kľúč: nenastavený (vyhľadávanie cez yt-dlp)"
        )
        self["quality"].setText("Preferovaná kvalita videa: %sp" % get_quality())
        self["resolver_state"].setText(
            "yt-dlp: dostupný (vyhľadávanie aj záložné prehrávanie)" if is_available() else
            "yt-dlp: nenainštalovaný (na prehrávanie nie je nutný)"
        )

    def toggle_quality(self):
        setting = config.plugins.warderyoutube.max_quality
        setting.value = "360" if get_quality() == "720" else "720"
        setting.save()
        configfile.save()
        self.refresh()

    def prompt_key(self):
        # Never reveal a stored key when opening the keyboard.
        self.session.openWithCallback(
            self.key_received, VirtualKeyboard,
            title="Vložte YouTube Data API kľúč (nahradí pôvodný)",
            text=""
        )

    def key_received(self, value):
        if value is None:
            return
        value = value.strip()
        if not value or any(c.isspace() for c in value) or len(value) > 256:
            self.session.open(
                MessageBox, "Neplatný alebo prázdny kľúč. Pôvodný zostal zachovaný.",
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
            "Odstrániť uložený YouTube API kľúč z prijímača?",
            type=MessageBox.TYPE_YESNO, default=False
        )

    def clear_key(self, confirmed):
        if confirmed:
            config.plugins.warderyoutube.api_key.value = ""
            config.plugins.warderyoutube.api_key.save()
            configfile.save()
            self.refresh()
