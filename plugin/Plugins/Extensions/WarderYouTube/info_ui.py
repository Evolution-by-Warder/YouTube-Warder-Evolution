# -*- coding: utf-8 -*-
"""Native Warder information dialog with reliable manual text navigation.

Uses the original working Enigma2 Label, not the ScrollLabel widget which
rendered a blank body on the GigaBlue/OpenATV receiver. All content is retained
in memory and exposed line-by-line; no timers, custom renderer or animation.
"""
import textwrap
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Screens.Screen import Screen
from .i18n import tr as _
from .skin import INFO_SKIN


# Chosen conservatively for the existing 1660 x 556 rectangle, Regular 30.
# Keeping fewer rows than the theoretical maximum avoids the original cut-off.
LINE_WIDTH = 84
VISIBLE_LINES = 12


def wrap_info_lines(message, width=LINE_WIDTH):
    lines = []
    for paragraph in str(message or "").replace("\r", "").split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(
            paragraph, width=width, expand_tabs=True,
            replace_whitespace=True, drop_whitespace=True,
            break_long_words=True, break_on_hyphens=False,
        ) or [""])
    return lines or [""]


class WarderYouTubeInfo(Screen):
    skin = INFO_SKIN

    def __init__(self, session, message, title=None):
        Screen.__init__(self, session)
        add_header(self)
        self._info_lines = wrap_info_lines(str(message)[:2500])
        self._top_line = 0
        self["brand"] = Label("YouTube Warder Evolution")
        self["title"] = Label(title or _("Video details"))
        self["body"] = Label(self._visible_text())
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Close"))
        self["key_yellow"] = Label(_("Scroll up"))
        self["key_blue"] = Label(_("Scroll down"))
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "DirectionActions", "NavigationActions"],
            {
                "ok": self.close, "cancel": self.close,
                "red": self.close, "green": self.close,
                "up": self.scroll_up, "down": self.scroll_down,
                "pageUp": self.page_up, "pageDown": self.page_down,
                "yellow": self.page_up, "blue": self.page_down,
            }, -1)

    def _max_top_line(self):
        return max(0, len(self._info_lines) - VISIBLE_LINES)

    def _visible_text(self):
        return "\n".join(self._info_lines[
            self._top_line:self._top_line + VISIBLE_LINES
        ])

    def _move(self, amount):
        new_top = max(0, min(self._max_top_line(), self._top_line + amount))
        if new_top != self._top_line:
            self._top_line = new_top
            self["body"].setText(self._visible_text())

    def scroll_up(self):
        self._move(-1)

    def scroll_down(self):
        self._move(1)

    def page_up(self):
        self._move(-VISIBLE_LINES)

    def page_down(self):
        self._move(VISIBLE_LINES)
