# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from enigma import getDesktop
from .ui import WarderYouTubeHome
from .i18n import tr as _

def main(session, **kwargs):
    session.open(WarderYouTubeHome)

def _plugin_icon():
    # Follow the working Warder PiconHub icon-resolution convention.
    try:
        return "images/plugin_fhd.png" if getDesktop(0).size().width() > 1900 else "images/plugin.png"
    except Exception:
        return "images/plugin.png"


def main_menu(menuid, **kwargs):
    """An optional shortcut in the receiver's Enigma2 main menu."""
    if menuid != "mainmenu":
        return []
    # Do not initialize YouTube traffic or a screen during menu discovery.
    try:
        from Components.config import config
        user = getattr(getattr(config, "plugins", None), "warderyoutube", None)
        toggle = getattr(user, "show_main_menu", None)
        if getattr(toggle, "value", False) is not True:
            return []
    except (ImportError, AttributeError, TypeError):
        return []
    return [("YouTube Warder Evolution", main, "warder_youtube_mainmenu", 55)]


def Plugins(**kwargs):
    return [PluginDescriptor(icon=_plugin_icon(), needsRestart=False,
                             name="YouTube Warder Evolution",
                             description=_("YouTube search and native Enigma2 video playback"),
                             where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main),
            PluginDescriptor(needsRestart=False,
                             name="YouTube Warder Evolution",
                             description=_("Optional Enigma2 main menu shortcut"),
                             where=PluginDescriptor.WHERE_MENU, fnc=main_menu)]
