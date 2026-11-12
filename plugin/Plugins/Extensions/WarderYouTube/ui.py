# -*- coding: utf-8 -*-
"""Remote-first original native UI, no live YouTube content yet."""
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from .skin import HOME_SKIN

class WarderYouTubeHome(Screen):
    skin = HOME_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.sections = [
            ("Domov", "Video recommendations will be added after search/backend verification."),
            ("Hľadanie", "The Enigma2 keyboard and video search are planned."),
            ("Odbery", "Subscriptions need secure optional account authorization."),
            ("História", "Local viewing history will follow verified playback."),
            ("Playlisty", "Playlist browsing is not yet implemented."),
            ("Obľúbené", "Local favourite videos and channels will be available."),
            ("Nastavenia", "Playback, privacy, cache and language options are planned.")
        ]
        self["brand"] = Label("YouTube - Warder Evolution")
        self["version"] = Label("0.0.1-dev / Enigma2")
        self["menu"] = MenuList([name for name, desc in self.sections])
        self["heading"] = Label("")
        self["description"] = Label("")
        self["status"] = Label("Prototype only: video search and playback are not implemented")
        self["footer"] = Label("UP/DOWN: Select      OK: Info      EXIT: Close")
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                                    {"ok": self.open_section, "cancel": self.close, "red": self.close}, -1)
        self["menu"].onSelectionChanged.append(self.selection_changed)
        self.selection_changed()

    def selection_changed(self):
        i = self["menu"].getSelectionIndex()
        if 0 <= i < len(self.sections):
            self["heading"].setText(self.sections[i][0])
            self["description"].setText(self.sections[i][1])

    def open_section(self):
        self.session.open(MessageBox,
                          "This feature is planned but not yet implemented.",
                          type=MessageBox.TYPE_INFO, timeout=5)
