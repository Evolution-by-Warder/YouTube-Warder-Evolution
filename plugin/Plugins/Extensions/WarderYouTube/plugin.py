# -*- coding: utf-8 -*-
from Plugins.Plugin import PluginDescriptor
from .ui import WarderYouTubeHome

def main(session, **kwargs):
    session.open(WarderYouTubeHome)

def Plugins(**kwargs):
    return [PluginDescriptor(name="YouTube - Warder Evolution",
                             description="Native blue UI prototype, no video playback",
                             where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]
