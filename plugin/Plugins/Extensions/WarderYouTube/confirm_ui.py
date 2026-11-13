# -*- coding: utf-8 -*-
"""Warder-styled native yes/no dialog; never opens a foreign Enigma popup."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Screen import Screen

from .i18n import tr as _
from .skin import CONFIRM_SKIN


class WarderYouTubeConfirm(Screen):
    skin = CONFIRM_SKIN

    def __init__(self, session, question):
        Screen.__init__(self, session)
        add_header(self)
        self["brand"] = Label("YouTube Warder Evolution")
        self["heading"] = Label(_("Confirm"))
        self["question"] = Label(str(question)[:500])
        self["menu"] = MenuList([_("No"), _("Yes")])
        self["hint"] = Label(_("Choose an action"))
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Confirm"))
        self["key_yellow"] = Label(_("No"))
        self["key_blue"] = Label(_("Back"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.choose, "green": self.accept,
            "cancel": self.cancel, "red": self.cancel,
            "yellow": self.cancel, "blue": self.cancel
        }, -1)

    def choose(self):
        self.close(self["menu"].getCurrentIndex() == 1)

    def accept(self):
        self.close(True)

    def cancel(self):
        self.close(False)
