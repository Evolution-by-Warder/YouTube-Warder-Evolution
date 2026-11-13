# -*- coding: utf-8 -*-
"""Native Warder dashboard, designed for the remote and system language."""
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from .skin import HOME_SKIN
from .update_core import CURRENT_VERSION
from .i18n import tr as _


class WarderYouTubeHome(Screen):
    skin = HOME_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.sections = [
            (_("Home"), _("Your own YouTube on Enigma2")),
            (_("Search"), _("Search the video catalogue")),
            (_("Subscriptions"), _("Subscriptions") + " • " + _("Optional")),
            (_("History"), _("Watch previously opened videos")),
            (_("Playlists"), _("Playlists") + " • " + _("Optional")),
            (_("Favourites"), _("Save videos without an account")),
            (_("Settings"), _("About settings")),
            (_("Updates"), _("Check for updates")),
        ]
        self["brand"] = Label("YouTube Warder Evolution")
        self["version"] = Label(CURRENT_VERSION + "  •  Enigma2")
        self["nav_title"] = Label(_("Quick access").upper())
        self["overline"] = Label("WARDER  /  ENIGMA2")
        self["menu"] = MenuList([name for name, description in self.sections])
        for index in range(len(self.sections)):
            self["nav_focus%d" % index] = Label(" ")
        for index in range(3):
            self["card_focus%d" % index] = Label(" ")
        self["heading"] = Label("")
        self["description"] = Label("")
        self["card1_title"] = Label(_("Search").upper())
        self["card1_body"] = Label(_("Search the video catalogue"))
        self["card2_title"] = Label(_("Favourites").upper())
        self["card2_body"] = Label(_("Save videos without an account"))
        self["card3_title"] = Label(_("History").upper())
        self["card3_body"] = Label(_("Watch previously opened videos"))
        self["status"] = Label(_("No external renderer"))
        self["footer"] = Label("OK: " + _("Open") + "    •    ↑↓: " + _("Select"))
        self["key_red"] = Label(_("Close"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("History"))
        self["key_blue"] = Label(_("Updates"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.open_section, "green": self.open_section,
            "cancel": self.close, "red": self.close,
            "yellow": lambda: self.open_index(3),
            "blue": lambda: self.open_index(7),
        }, -1)
        self["menu"].onSelectionChanged.append(self.selection_changed)
        self.onLayoutFinish.append(self.selection_changed)
        self.selection_changed()

    def selection_changed(self):
        index = self["menu"].getCurrentIndex()
        for row in range(len(self.sections)):
            focus = self["nav_focus%d" % row]
            if row == index:
                focus.show()
            else:
                focus.hide()
        card_for_section = {1: 0, 5: 1, 3: 2}
        for card in range(3):
            focus = self["card_focus%d" % card]
            if card_for_section.get(index) == card:
                focus.show()
            else:
                focus.hide()
        if 0 <= index < len(self.sections):
            self["heading"].setText(self.sections[index][0])
            self["description"].setText(self.sections[index][1])

    def open_section(self):
        self.open_index(self["menu"].getCurrentIndex())

    def open_index(self, index):
        if index == 1:
            from .search import WarderYouTubeSearch
            self.session.open(WarderYouTubeSearch)
        elif index in (3, 5):
            from .library_ui import WarderYouTubeLibrary
            self.session.open(WarderYouTubeLibrary,
                              "history" if index == 3 else "favourites")
        elif index == 6:
            from .settings import WarderYouTubeSettings
            self.session.open(WarderYouTubeSettings)
        elif index == 7:
            from .update_ui import WarderYouTubeUpdateCheck
            self.session.open(WarderYouTubeUpdateCheck)
        elif index == 0:
            self["status"].setText(_("Your own YouTube on Enigma2"))
        else:
            self["status"].setText(self.sections[index][0] + " • " + _("Optional"))
