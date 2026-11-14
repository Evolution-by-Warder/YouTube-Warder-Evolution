# -*- coding: utf-8 -*-
"""Native in-plugin contextual actions for the current video selection."""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Screens.Screen import Screen

from .i18n import tr as _
from .skin import CONTEXT_SKIN


class WarderYouTubeContext(Screen):
    skin = CONTEXT_SKIN

    def __init__(self, session, video=None, is_favourite=False, mode="search"):
        Screen.__init__(self, session)
        add_header(self)
        self.options = [
            ("play", _("Play video")),
            ("favorite", _("Remove video from favourites") if is_favourite else _("Add video to favourites")),
            ("info", _("Video details")),
        ]
        if mode == "search":
            self.options.append(("search", _("New search")))
        elif mode == "favourites":
            # In Favourites, "Remove video from favourites" already removes this
            # video. A second single-video delete would do exactly the same thing.
            # Keep only the distinct, confirmation-protected clear-all action.
            self.options.append(("clear", _("Clear all favourite videos")))
        elif mode == "history":
            # In History, "Delete video from history" removes only that record;
            # "Remove from favourites" is a separate, optional operation.
            self.options.append(("remove", _("Delete video from history")))
            self.options.append(("clear", _("Clear entire history")))
        self["brand"] = Label("YouTube Warder Evolution")
        self["heading"] = Label(_("Video actions"))
        self["video"] = Label(str((video or {}).get("title") or _("No video selected"))[:155])
        self.selected = 0
        for index in range(5):
            self["context_focus%d" % index] = Label(" ")
            self["context_row%d" % index] = Label(
                self.options[index][1] if index < len(self.options) else ""
            )
        self["hint"] = Label(_("Choose an action"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("Details"))
        self["key_blue"] = Label(
            _("New search") if mode == "search" else
            _("Clear favourites") if mode == "favourites" else
            _("Clear history")
        )
        self.mode = mode
        self["actions"] = ActionMap(["NavigationActions", "OkCancelActions", "ColorActions"], {
            "up": self.up, "down": self.down,
            "ok": self.choose, "green": self.choose,
            "cancel": self.cancel, "red": self.cancel,
            "yellow": lambda: self.close("info"),
            "blue": lambda: self.close("search" if self.mode == "search" else "clear")
        }, -1)
        self.onLayoutFinish.append(self.update_focus)
        self.update_focus()

    def update_focus(self):
        current = self.selected
        for index in range(5):
            focus = self["context_focus%d" % index]
            if index == current and index < len(self.options):
                focus.show()
            else:
                focus.hide()

    def up(self):
        self.selected = (self.selected - 1) % len(self.options)
        self.update_focus()

    def down(self):
        self.selected = (self.selected + 1) % len(self.options)
        self.update_focus()

    def choose(self):
        if 0 <= self.selected < len(self.options):
            self.close(self.options[self.selected][0])

    def cancel(self):
        self.close(None)
