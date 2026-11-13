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


def keyboard_geometry(key_width, key_height, columns, rows):
    """Compute a tight, centered Enigma2 listbox around the actual keys.

    Enigma2 key images use image/skin-dependent dimensions, not the XML
    widget width. The previous fixed 1495px listbox left a translucent
    rectangle to the right of the last character.
    """
    width = int(key_width) * max(14, int(columns)) + 8
    height = int(key_height) * int(rows) + 8
    if not (450 <= width <= 1450 and 160 <= height <= 450):
        raise ValueError("unsupported native keyboard dimensions")
    # Warder blue panel spans x=168..1752; center is x=960.
    x = 960 - width // 2
    # Key area is between input field and locale/status line.
    y = 350 + (470 - height) // 2
    return x, y, width, height


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
        # Enigma2 uses StaticText sources for its native colour key labels.
        # Keep those original sources/actions untouched; plain native Labels
        # below make the Warder footer visible without a custom renderer.
        self["warder_key_red"] = Label(_("Cancel"))
        self["warder_key_green"] = Label(_("Confirm"))
        self["warder_key_yellow"] = Label(_("Shift"))
        self["warder_key_blue"] = Label("Aa")
        self["warder_key_hint"] = Label(_("Language from Enigma2"))
        # Run *after* the firmware callback has populated keyboardWidth,
        # keyboardHeight and the native list. Works on OpenATV and OpenPLi.
        if hasattr(self, "onLayoutFinish"):
            self.onLayoutFinish.append(self._align_native_keys)

    def setLocale(self):
        # Preserve the original keyboard's locale/keymap logic, but avoid
        # long translated country names spilling into a clipped second line.
        VirtualKeyBoard.setLocale(self)
        self._compact_locale_labels()

    def _compact_locale_labels(self):
        locale = str(getattr(self, "locale", None) or
                     getattr(self, "lang", None) or "Enigma2")[:24]
        self["locale"].setText(_("Keyboard layout") + ": " + locale)
        self["language"].setText(_("Language from Enigma2"))

    def _align_native_keys(self):
        # This modifies only the listbox inside this dialog; the system
        # keyboard/skin and all global windowstyles remain unchanged.
        self._compact_locale_labels()
        try:
            x, y, width, height = keyboard_geometry(
                self.width, self.height,
                self.keyboardWidth, self.keyboardHeight
            )
            from enigma import ePoint, eSize
            widget = getattr(self["list"], "instance", None)
            if widget is not None:
                widget.resize(eSize(width, height))
                widget.move(ePoint(x, y))
        except (AttributeError, ImportError, RuntimeError, TypeError, ValueError):
            # Safe centered XML default for unsupported vendor builds.
            return
