# -*- coding: utf-8 -*-
"""Native in-plugin contextual actions for the current video selection."""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Screen import Screen

from .i18n import tr as _
from .skin import CONTEXT_SKIN


class WarderYouTubeContext(Screen):
    skin = CONTEXT_SKIN

    def __init__(self, session, video=None, is_favourite=False):
        Screen.__init__(self, session)
        self.options = [
            ("play", _("Play video")),
            ("favorite", _("Remove from favourites") if is_favourite else _("Add to favourites")),
            ("info", _("Video details")),
            ("search", _("New search"))
        ]
        self["brand"] = Label("YouTube Warder Evolution")
        self["heading"] = Label(_("Video actions"))
        self["video"] = Label(str((video or {}).get("title") or _("No video selected"))[:155])
        self["menu"] = MenuList([name for key, name in self.options])
        self["hint"] = Label(_("Choose an action"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("Details"))
        self["key_blue"] = Label(_("New search"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.choose, "green": self.choose,
            "cancel": self.cancel, "red": self.cancel,
            "yellow": lambda: self.close("info"),
            "blue": lambda: self.close("search")
        }, -1)

    def choose(self):
        index = self["menu"].getCurrentIndex()
        if 0 <= index < len(self.options):
            self.close(self.options[index][0])

    def cancel(self):
        self.close(None)
