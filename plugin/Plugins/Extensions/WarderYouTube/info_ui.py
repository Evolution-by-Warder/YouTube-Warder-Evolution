# -*- coding: utf-8 -*-
"""Native Warder information dialog that stays within the plugin palette."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Screens.Screen import Screen
from .i18n import tr as _
from .skin import INFO_SKIN


class WarderYouTubeInfo(Screen):
    skin = INFO_SKIN

    def __init__(self, session, message, title=None):
        Screen.__init__(self, session)
        add_header(self)
        self["brand"] = Label("YouTube Warder Evolution")
        self["title"] = Label(title or _("Video details"))
        self["body"] = ScrollLabel(str(message)[:2500])
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Close"))
        self["key_yellow"] = Label(_("Scroll up"))
        self["key_blue"] = Label(_("Scroll down"))
        # Native ScrollLabel keeps long text inside the existing INFO panel.
        # All scrolling is manual: no timers, effects or custom renderers.
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions", "NavigationActions"], {
            "ok": self.close, "cancel": self.close, "red": self.close,
            "green": self.close,
            "up": self["body"].pageUp, "down": self["body"].pageDown,
            "pageUp": self["body"].pageUp, "pageDown": self["body"].pageDown,
            "yellow": self["body"].pageUp, "blue": self["body"].pageDown,
        }, -1)
