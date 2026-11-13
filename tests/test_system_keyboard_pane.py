"""Enigma2-system keyboard embedding contract without importing C++ receivers.

The real GigaBlue UI will use Screens.VirtualKeyBoard.VirtualKeyBoard,
including its native firmware keymap, Input, list renderer and actions.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

SRC = (Path(__file__).resolve().parents[1] /
       "plugin/Plugins/Extensions/WarderYouTube/system_keyboard_pane.py")


class Component:
    def __init__(self, text=""):
        self.text = text
        self.visible = True
        self.instance = None

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def char(self, char):
        self.text += char

    def deleteBackward(self):
        self.text = self.text[:-1]

    def getText(self):
        return self.text


class OriginalSystemKeyboard(dict):
    def __init__(self, session, title="", text="", maxSize=False):
        self["list"] = Component()
        self["text"] = Component(text)
        self.title = title
        self.session = session
        self.native_calls = []
        self.selectedKey = 14
        self.keyboardWidth = 14
        self.keyboardHeight = 5
        self.width = 45
        self.height = 45
        self.sms = types.SimpleNamespace(stopTimer=self.cleanup)
        self.cleaned = False
        self.initialized = False

    def layoutFinished(self):
        self.initialized = True

    def processSelect(self):
        self.native_calls.append("processSelect")
        self["text"].char("a")

    def backSelected(self):
        self.native_calls.append("backSelected")
        self["text"].deleteBackward()

    def capsLockSelected(self):
        self.native_calls.append("capsLockSelected")

    def left(self):
        self.native_calls.append("left")
        self.selectedKey = 14

    def right(self):
        self.native_calls.append("right")
        self.selectedKey = 15

    def up(self):
        self.native_calls.append("up")

    def down(self):
        self.native_calls.append("down")

    def cleanup(self):
        self.cleaned = True


class OpenPliKeyboard(OriginalSystemKeyboard):
    layoutFinished = None

    def buildVirtualKeyBoard(self):
        self.initialized = True


def load(native):
    package = types.ModuleType("_warder_pane")
    package.__path__ = [str(SRC.parent)]
    i18n = types.ModuleType("_warder_pane.i18n")
    i18n.tr = lambda value: value
    screens = types.ModuleType("Screens")
    screens.__path__ = []
    system = types.ModuleType("Screens.VirtualKeyBoard")
    system.VirtualKeyBoard = native
    modules = {
        "_warder_pane": package,
        "_warder_pane.i18n": i18n,
        "Screens": screens,
        "Screens.VirtualKeyBoard": system
    }
    spec = importlib.util.spec_from_file_location(
        "_warder_pane.system_keyboard_pane", SRC
    )
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
        result = module.SystemKeyboardPane
        # The production code imports Screens.VirtualKeyBoard lazily.
        # Pass the mock keyboard through construction while the patch is active.
        yield result


class SystemKeyboardPaneTests(unittest.TestCase):
    def test_genuine_components_and_all_native_key_methods(self):
        for constructor in load(OriginalSystemKeyboard):
            submitted, canceled = [], []
            pane = constructor(None, submitted.append, lambda: canceled.append(True))
            self.assertIs(pane.list, pane.backend["list"])
            self.assertIs(pane.input, pane.backend["text"])
            pane.layout_finished()
            self.assertTrue(pane.ready)
            self.assertTrue(pane.backend.initialized)
            pane.hide()
            self.assertFalse(pane.list.visible)
            self.assertFalse(pane.input.visible)
            pane.show()
            self.assertTrue(pane.list.visible)
            self.assertTrue(pane.input.visible)
            self.assertTrue(pane.is_left_edge())
            pane.navigate("right")
            self.assertFalse(pane.is_left_edge())
            pane.press()
            self.assertEqual(pane.value(), "a")
            pane.space()
            self.assertEqual(pane.value(), "a ")
            pane.delete()
            self.assertEqual(pane.value(), "a")
            pane.shift()
            self.assertEqual(pane.backend.native_calls,
                             ["right", "processSelect", "backSelected", "capsLockSelected"])
            pane.backend.save()
            pane.backend.cancel()
            self.assertEqual(submitted, ["a"])
            self.assertEqual(canceled, [True])
            pane.cleanup()
            self.assertTrue(pane.backend.cleaned)

    def test_openpli_original_builder_is_supported_without_reimplementing_keys(self):
        for constructor in load(OpenPliKeyboard):
            pane = constructor(None, lambda x: None, lambda: None)
            pane.layout_finished()
            self.assertTrue(pane.backend.initialized)
            self.assertTrue(pane.ready)
            pane.navigate("left")
            self.assertEqual(pane.backend.native_calls, ["left"])


if __name__ == "__main__":
    unittest.main()
