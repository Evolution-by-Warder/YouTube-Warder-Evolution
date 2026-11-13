# -*- coding: utf-8 -*-
"""Native full-screen Warder keyboard, not the image's black VirtualKeyboard.

One lightweight label per key; navigation uses standard remote actions. No
renderer, no external widgets, no virtual keyboard popup over the live-TV image.
"""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Screens.Screen import Screen

from .i18n import tr as _
from .skin import KEYBOARD_SKIN

ROWS = (
    "1234567890", "qwertyuiop", "asdfghjkl-",
    "zxcvbnm.,?", "áčďéíľňšťž"
)
COLUMNS = 10


class WarderYouTubeKeyboard(Screen):
    skin = KEYBOARD_SKIN

    def __init__(self, session, value="", title=None, secret=False, limit=160):
        Screen.__init__(self, session)
        self.value = str(value or "")[:limit]
        self.limit = limit
        self.secret = bool(secret)
        self.position = 10
        self.upper = False
        self["title"] = Label(title or _("Enter your YouTube search"))
        self["brand"] = Label("YouTube Warder Evolution  /  " + _("Search videos"))
        self["input"] = Label("")
        self["hint"] = Label(_("Press OK to type a letter"))
        self["legend"] = Label(_("Space") + " · " + _("Delete") + " · MENU: Aa")
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Confirm"))
        self["key_yellow"] = Label(_("Delete"))
        self["key_blue"] = Label(_("Space"))
        for index, char in enumerate("".join(ROWS)):
            self["letter%d" % index] = Label(char)
            self["focus%d" % index] = Label("")
        self["actions"] = ActionMap([
            "NavigationActions", "OkCancelActions", "ColorActions",
            "MenuActions", "NumberActions"
        ], {
            "left": self.left, "right": self.right,
            "up": self.up, "down": self.down,
            "ok": self.press_letter, "cancel": self.cancel,
            "red": self.cancel, "green": self.submit,
            "yellow": self.delete, "blue": self.space,
            "menu": self.toggle_case,
            **{str(n): (lambda n=n: self.append(str(n))) for n in range(10)}
        }, -1)
        self.onLayoutFinish.append(self._ready)

    def _ready(self):
        self._refresh()
        for index in range(len("".join(ROWS))):
            self["focus%d" % index].hide()
        self["focus%d" % self.position].show()

    def _refresh(self):
        masked = "•" * len(self.value) if self.secret else self.value
        self["input"].setText(masked[-160:] or _("Search is empty"))

    def _select(self, index):
        before = self.position
        self.position = index % 50
        if before != self.position:
            self["focus%d" % before].hide()
            self["focus%d" % self.position].show()

    def left(self):
        self._select(self.position - 1 if self.position % COLUMNS else self.position + COLUMNS - 1)

    def right(self):
        self._select(self.position + 1 if self.position % COLUMNS < COLUMNS - 1 else self.position - COLUMNS + 1)

    def up(self):
        self._select(self.position - COLUMNS)

    def down(self):
        self._select(self.position + COLUMNS)

    def append(self, char):
        if len(self.value) >= self.limit:
            return
        self.value += char
        self._refresh()

    def press_letter(self):
        char = "".join(ROWS)[self.position]
        self.append(char.upper() if self.upper else char)

    def toggle_case(self):
        self.upper = not self.upper
        for i, char in enumerate("".join(ROWS)):
            self["letter%d" % i].setText(char.upper() if self.upper else char)

    def space(self):
        self.append(" ")

    def delete(self):
        self.value = self.value[:-1]
        self._refresh()

    def submit(self):
        self.close(self.value.strip() or None)

    def cancel(self):
        self.close(None)
