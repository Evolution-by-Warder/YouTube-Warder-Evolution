# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from enigma import getDesktop
from .ui import WarderYouTubeHome

def main(session, **kwargs):
    session.open(WarderYouTubeHome)

def _plugin_icon():
    # Follow the working Warder PiconHub icon-resolution convention.
    try:
        return "images/plugin_fhd.png" if getDesktop(0).size().width() > 1900 else "images/plugin.png"
    except Exception:
        return "images/plugin.png"


def Plugins(**kwargs):
    return [PluginDescriptor(icon=_plugin_icon(), needsRestart=False,
                             name="YouTube Warder Evolution",
                             description="Native blue YouTube search and experimental playback",
                             where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
