# -*- coding: utf-8 -*-
"""Warder-styled native yes/no dialog; never opens a foreign Enigma popup."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
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
        self.selected = 0
        self["confirm_focus0"] = Label(" ")
        self["confirm_focus1"] = Label(" ")
        self["confirm_row0"] = Label(_("No"))
        self["confirm_row1"] = Label(_("Yes"))
        self["hint"] = Label(_("Choose an action"))
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Confirm"))
        self["key_yellow"] = Label(_("No"))
        self["key_blue"] = Label(_("Back"))
        self["actions"] = ActionMap(["NavigationActions", "OkCancelActions", "ColorActions"], {
            "up": self.up, "down": self.down,
            "ok": self.choose, "green": self.accept,
            "cancel": self.cancel, "red": self.cancel,
            "yellow": self.cancel, "blue": self.cancel
        }, -1)
        self.onLayoutFinish.append(self.update_focus)
        self.update_focus()

    def update_focus(self):
        for index in range(2):
            widget = self["confirm_focus%d" % index]
            if index == self.selected:
                widget.show()
            else:
                widget.hide()

    def up(self):
        self.selected = (self.selected - 1) % 2
        self.update_focus()

    def down(self):
        self.selected = (self.selected + 1) % 2
        self.update_focus()

    def choose(self):
        self.close(self.selected == 1)

    def accept(self):
        self.close(True)

    def cancel(self):
        self.close(False)
