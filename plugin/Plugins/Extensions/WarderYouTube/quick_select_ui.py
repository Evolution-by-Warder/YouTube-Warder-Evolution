# -*- coding: utf-8 -*-
"""Compact native Enigma2 choice list for Home categories and Odbery channels.

The 750x690 popup contains the exact chips currently visible in the right pane.
Arrow keys scroll the full list without returning through video pages; OK
returns a stable chip ID, not an index that could change on account refresh.
"""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.Screen import Screen

from .i18n import tr as _
from .skin import QUICK_SELECT_SKIN


class WarderYouTubeQuickSelect(Screen):
    skin = QUICK_SELECT_SKIN

    def __init__(self, session, chips, selected=0, subscriptions=False):
        Screen.__init__(self, session)
        self.subscriptions = bool(subscriptions)
        self.chips = [dict(chip) for chip in chips
                      if isinstance(chip, dict)
                      and isinstance(chip.get("id"), str)
                      and chip.get("id") and isinstance(chip.get("label"), str)]
        self["heading"] = Label(_("Select subscription") if self.subscriptions
                                else _("Select category"))
        # Do not abbreviate channel names in the popup as the horizontal
        # Home rail does; users should see the actual full channel title.
        self["choices"] = MenuList([
            _(chip.get("title") or chip["label"]) if self.subscriptions
            else _(chip["label"]) for chip in self.chips
        ])
        self["hint"] = Label(_("Arrows: select · OK: confirm · EXIT: cancel"))
        self["actions"] = ActionMap(
            ["NavigationActions", "DirectionActions", "OkCancelActions",
             "ColorActions"],
            {"up": self.up, "down": self.down,
             "left": self.page_up, "right": self.page_down,
             "ok": self.choose, "green": self.choose,
             "red": self.cancel, "cancel": self.cancel},
            -1
        )
        self.initial_index = max(0, min(int(selected), len(self.chips) - 1))
        self.onLayoutFinish.append(self._position)

    def _position(self):
        self._move_index(self.initial_index)

    def _move_index(self, index):
        control = self["choices"]
        if hasattr(control, "moveToIndex"):
            control.moveToIndex(index)
        elif getattr(control, "instance", None) is not None:
            instance = control.instance
            if hasattr(instance, "moveSelectionTo"):
                instance.moveSelectionTo(index)

    def up(self):
        control = self["choices"]
        if hasattr(control, "up"):
            control.up()
        else:
            self._move_index(max(0, control.getCurrentIndex() - 1))

    def down(self):
        control = self["choices"]
        if hasattr(control, "down"):
            control.down()
        else:
            self._move_index(min(len(self.chips) - 1, control.getCurrentIndex() + 1))

    def page_up(self):
        control = self["choices"]
        if hasattr(control, "pageUp"):
            control.pageUp()
        else:
            self._move_index(max(0, control.getCurrentIndex() - 8))

    def page_down(self):
        control = self["choices"]
        if hasattr(control, "pageDown"):
            control.pageDown()
        else:
            self._move_index(min(len(self.chips) - 1, control.getCurrentIndex() + 8))

    def choose(self):
        if not self.chips:
            self.close(None)
            return
        index = self["choices"].getCurrentIndex()
        if 0 <= index < len(self.chips):
            self.close(self.chips[index]["id"])

    def cancel(self):
        self.close(None)
