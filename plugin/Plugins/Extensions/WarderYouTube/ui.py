# -*- coding: utf-8 -*-
"""Remote-first native UI: search and settings are now wired in."""
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from .skin import HOME_SKIN
from .update_core import CURRENT_VERSION


class WarderYouTubeHome(Screen):
    skin = HOME_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.sections = [
            ("Home", "Recommendations will be enabled after a catalogue is validated."),
            ("Search", "Search YouTube using your API key or optional installed yt-dlp."),
            ("Subscriptions", "Subscriptions need secure account authorization."),
            ("History", "Local viewing history will follow verified playback."),
            ("Playlists", "Playlist browsing is planned after search and playback."),
            ("Favourites", "Local favourite videos and channels are planned."),
            ("Settings", "Optional Google API key; yt-dlp can search without one."),
            ("Updates", "Check the verified Warder release channel.")
        ]
        self["brand"] = Label("YouTube Warder Evolution")
        self["version"] = Label(CURRENT_VERSION + " / Enigma2")
        self["menu"] = MenuList([name for name, desc in self.sections])
        self["heading"] = Label("")
        self["description"] = Label("")
        self["status"] = Label("Search: API key or yt-dlp. Native playback is experimental.")
        self["footer"] = Label("UP/DOWN: Select      OK: Open      EXIT: Close")
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions"],
            {"ok": self.open_section, "cancel": self.close, "red": self.close},
            -1
        )
        self["menu"].onSelectionChanged.append(self.selection_changed)
        self.selection_changed()

    def selection_changed(self):
        index = self["menu"].getCurrentIndex()
        if 0 <= index < len(self.sections):
            self["heading"].setText(self.sections[index][0])
            self["description"].setText(self.sections[index][1])

    def open_section(self):
        index = self["menu"].getCurrentIndex()
        if index == 1:
            from .search import WarderYouTubeSearch
            self.session.open(WarderYouTubeSearch)
        elif index == 6:
            from .settings import WarderYouTubeSettings
            self.session.open(WarderYouTubeSettings)
        elif index == 7:
            from .update_ui import WarderYouTubeUpdateCheck
            self.session.open(WarderYouTubeUpdateCheck)
        else:
            self.session.open(
                MessageBox,
                "This section is planned. Search and Settings are available. Playback is experimental.",
                type=MessageBox.TYPE_INFO, timeout=5
            )
