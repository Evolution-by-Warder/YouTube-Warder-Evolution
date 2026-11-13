# -*- coding: utf-8 -*-
"""Use the receiver's real Enigma2 keyboard logic inside a Warder-blue screen.

No duplicated key matrix, input engine or global skin overrides. Import only
where Enigma2 provides the built-in VirtualKeyBoard; Search has a safe fallback
for older / vendor-specific images.
"""
from Components.Label import Label
from Screens.VirtualKeyBoard import VirtualKeyBoard

from .skin import NATIVE_SEARCH_KEYBOARD_SKIN
from .i18n import tr as _


class WarderNativeSearchKeyboard(VirtualKeyBoard):
    """System keyboard, branded local skin, unchanged Enigma2 key handling."""
    skin = NATIVE_SEARCH_KEYBOARD_SKIN

    def __init__(self, session, value="", title=None, secret=False, limit=160):
        if secret:
            # Input.PIN in Enigma2 accepts numbers only. Never use it for an
            # alphanumeric YouTube API key or silently display a secret.
            raise ValueError("Use the masked Warder editor for secret input")
        max_size = max(1, min(256, int(limit)))
        VirtualKeyBoard.__init__(
            self, session, title=title or _("Enter your YouTube search"),
            text=str(value or "")[:max_size], maxSize=max_size
        )
        # Built-in class names would resolve to the system skin before our
        # embedded skin. A unique name guarantees the blue Warder panel,
        # without altering any other Enigma2 keyboard or current GUI skin.
        self.skinName = ["WarderNativeSearchKeyboard"]
        self["warder_brand"] = Label("YouTube Warder Evolution")
        self["warder_caption"] = Label(_("Search videos"))
