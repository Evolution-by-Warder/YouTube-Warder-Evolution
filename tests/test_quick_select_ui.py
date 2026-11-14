"""Quick MENU modal: category vs subscription labels and long native list."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube")


class Widget:
    def __init__(self, text=""):
        self.text = text


class NativeList:
    def __init__(self, rows):
        self.rows = list(rows)
        self.index = 0
        self.instance = None
    def moveToIndex(self, index):
        self.index = max(0, min(len(self.rows) - 1, index))
    def getCurrentIndex(self):
        return self.index
    def up(self):
        self.moveToIndex(self.index - 1)
    def down(self):
        self.moveToIndex(self.index + 1)
    def pageUp(self):
        self.moveToIndex(self.index - 9)
    def pageDown(self):
        self.moveToIndex(self.index + 9)


class FakeScreen(dict):
    def __init__(self, session):
        super().__init__()
        self.onLayoutFinish = []
        self.closed_value = None
    def close(self, value):
        self.closed_value = value


def load():
    package = types.ModuleType("_quick_select_test")
    package.__path__ = [str(ROOT)]
    def mod(name, **values):
        m = types.ModuleType(name)
        for k, v in values.items():
            setattr(m, k, v)
        return m
    modules = {
        "_quick_select_test": package,
        "_quick_select_test.i18n": mod(
            "_quick_select_test.i18n", tr=lambda s: s),
        "Components": mod("Components"),
        "Components.ActionMap": mod("Components.ActionMap",
                                     ActionMap=lambda *a, **kw: Widget()),
        "Components.Label": mod("Components.Label", Label=Widget),
        "Components.MenuList": mod("Components.MenuList", MenuList=NativeList),
        "Screens": mod("Screens"),
        "Screens.Screen": mod("Screens.Screen", Screen=FakeScreen),
    }
    modules["Screens"].__path__ = []
    modules["Components"].__path__ = []
    spec = importlib.util.spec_from_file_location(
        "_quick_select_test.quick_select_ui", ROOT / "quick_select_ui.py")
    result = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(result)
    return result


class QuickChooserTests(unittest.TestCase):
    def test_home_has_select_category_and_stable_ids(self):
        mod = load()
        chips = [
            {"id": "all", "label": "Všetko"},
            {"id": "topic:gaming", "label": "Hry"},
            {"id": "topic:music", "label": "Hudba"}
        ]
        ui = mod.WarderYouTubeQuickSelect(None, chips, selected=1)
        self.assertEqual(ui["heading"].text, "Select category")
        self.assertEqual(ui["choices"].rows, ["Všetko", "Hry", "Hudba"])
        self.assertIn('size="750,690"', ui.skin)
        ui.onLayoutFinish[0]()
        self.assertEqual(ui["choices"].getCurrentIndex(), 1)
        ui.down()
        ui.choose()
        self.assertEqual(ui.closed_value, "topic:music")

    def test_odbery_has_select_subscription_and_full_channel_titles(self):
        mod = load()
        chips = [{"id": "latest", "kind": "recent",
                  "label": "Najnovšie", "title": "Najnovšie"}]
        for i in range(53):
            chips.append({"id": "channel:UC" + chr(97 + i % 26) * 22 + str(i),
                          "kind": "channel",
                          "label": "Florida Filip…",
                          "title": "Florida Filip Family Episode %d" % i})
        ui = mod.WarderYouTubeQuickSelect(None, chips, subscriptions=True)
        self.assertEqual(ui["heading"].text, "Select subscription")
        self.assertEqual(len(ui["choices"].rows), 54)
        self.assertEqual(ui["choices"].rows[1], "Florida Filip Family Episode 0")
        ui.page_down()
        self.assertGreater(ui["choices"].getCurrentIndex(), 0)
        ui.choose()
        self.assertEqual(ui.closed_value, chips[9]["id"])

    def test_cancel_does_not_change_selected_chip(self):
        mod = load()
        ui = mod.WarderYouTubeQuickSelect(
            None, [{"id": "all", "label": "Všetko"}], subscriptions=False)
        ui.cancel()
        self.assertIsNone(ui.closed_value)


if __name__ == "__main__":
    unittest.main()
