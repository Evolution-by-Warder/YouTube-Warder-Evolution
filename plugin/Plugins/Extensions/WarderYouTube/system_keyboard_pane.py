# -*- coding: utf-8 -*-
"""Embed the real Enigma2 VirtualKeyBoard *components* in Warder's Home panel.

No hand-built keys, graphics, locale tables or second modal Screen are used.
The firmware's own VirtualKeyBoard creates the eListboxPythonMultiContent
keyboard and Components.Input. Those exact objects are attached to Home's
skin; a detached backend object retains native key rendering and semantics.

OpenATV uses Screens.VirtualKeyBoard.VirtualKeyboard (aliased as
VirtualKeyBoard); OpenPLi exposes VirtualKeyBoard directly.
"""
from .i18n import tr as _


class SystemKeyboardPane:
    def __init__(self, session, on_submit, on_cancel):
        # Import only when constructing Home, so another image which lacks
        # the system keyboard cannot break plugin startup at import time.
        from Screens.VirtualKeyBoard import VirtualKeyBoard

        class DetachedKeyboard(VirtualKeyBoard):
            def __init__(self, session):
                self._warder_submit = on_submit
                self._warder_cancel = on_cancel
                # The genuine firmware keyboard owns its layout, locale,
                # Input component, and key selection/navigation logic.
                VirtualKeyBoard.__init__(
                    self, session, title=_("Enter your YouTube search"),
                    text="", maxSize=False
                )

            def save(self):
                self._warder_submit(self["text"].getText())

            def cancel(self):
                self._warder_cancel()

        self.backend = DetachedKeyboard(session)
        self.list = self.backend["list"]
        self.input = self.backend["text"]
        self.ready = False

    def layout_finished(self):
        if self.ready:
            return
        # The system MenuList/Input GUI widgets already exist in the *Home*
        # screen; this matches firmware onLayoutFinish but does not open or
        # execute the detached keyboard screen.
        backend = self.backend
        callback = getattr(backend, "layoutFinished", None)
        if callback is None:
            callback = getattr(backend, "buildVirtualKeyBoard", None)
        if callback is None:
            raise RuntimeError("The firmware keyboard has no supported builder")
        callback()
        self.ready = True
        self._center_original_list()

    def _center_original_list(self):
        # Make only the native eListbox's *viewport* fit the right pane.
        # Individual key graphics, fonts and locale layouts are unchanged.
        backend = self.backend
        rows = int(getattr(backend, "keyboardHeight", 0) or 0)
        cols = int(getattr(backend, "keyboardWidth", 0) or 0)
        if not (3 <= rows <= 9 and 10 <= cols <= 20):
            return
        width = int(getattr(backend, "width", 45) or 45) * max(14, cols) + 12
        height = int(getattr(backend, "height", 45) or 45) * rows + 12
        if not (480 <= width <= 1350 and 150 <= height <= 525):
            return
        # Home right panel: x 394..1884, y 173..978.
        x = 1138 - width // 2
        y = 355 + max(0, (435 - height) // 2)
        try:
            from enigma import ePoint, eSize
            instance = getattr(self.list, "instance", None)
            if instance is not None:
                instance.resize(eSize(width, height))
                instance.move(ePoint(x, y))
        except (ImportError, RuntimeError, TypeError, AttributeError):
            # The skin's fixed right-pane fallback remains functional.
            pass

    def show(self):
        self.list.show()
        self.input.show()

    def hide(self):
        self.list.hide()
        self.input.hide()

    def navigate(self, direction):
        # Exactly the firmware's own navigation/selected-key handling.
        getattr(self.backend, direction)()

    def is_left_edge(self):
        width = int(getattr(self.backend, "keyboardWidth", 0) or 0)
        selected = int(getattr(self.backend, "selectedKey", 0) or 0)
        return bool(width) and selected % width == 0

    def press(self):
        self.backend.processSelect()

    def delete(self):
        self.backend.backSelected()

    def space(self):
        self.input.char(" ")

    def shift(self):
        self.backend.capsLockSelected()

    def value(self):
        return self.input.getText()

    def reset(self):
        """Clear the real Enigma2 Input AND refresh its on-screen widget.

        Enigma2 Input.deleteAllChars() only changes its internal buffer; it
        does not call update(), so old text stays visible in the right pane.
        Input.setText("") clears the value, resets the cursor and redraws
        the widget on both OpenATV and OpenPLi.
        """
        self.input.setText("")

    def cleanup(self):
        sms = getattr(self.backend, "sms", None)
        if sms is not None:
            try:
                sms.stopTimer()
            except (AttributeError, RuntimeError):
                pass
