"""Native Warder TV keyboard, actions and confirmation smoke tests with mocked Enigma."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import ast

ROOT = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube")


class Label:
    def __init__(self, text=""):
        self.text = text
        self.visible = True
    def setText(self, value):
        self.text = value
    def hide(self):
        self.visible = False
    def show(self):
        self.visible = True


class MenuList:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0
    def getCurrentIndex(self):
        return self.index


class Screen(dict):
    def __init__(self, session):
        self.session = session
        self.onLayoutFinish = []
        self.onClose = []
        self.closed_args = None
    def close(self, *args):
        self.closed_args = args
        for callback in self.onClose:
            callback()


def mod(name, **kwargs):
    obj = types.ModuleType(name)
    for key, value in kwargs.items():
        setattr(obj, key, value)
    return obj


def load(name):
    package = mod("_test_warder_design")
    package.__path__ = [str(ROOT)]
    components = mod("Components")
    components.__path__ = []
    screens = mod("Screens")
    screens.__path__ = []
    fake = {
        "_test_warder_design": package,
        "_test_warder_design.i18n": mod(
            "_test_warder_design.i18n", tr=lambda message: message,
            language_code=lambda: "sk"
        ),
        "_test_warder_design.skin": mod(
            "_test_warder_design.skin",
            KEYBOARD_SKIN="<screen/>", CONTEXT_SKIN="<screen/>",
            CONFIRM_SKIN="<screen/>", INFO_SKIN="<screen/>"
        ),
        "Components": components,
        "Components.ActionMap": mod(
            "Components.ActionMap", ActionMap=lambda *args, **kwargs: Label()
        ),
        "Components.Label": mod("Components.Label", Label=Label),
        "Components.MenuList": mod("Components.MenuList", MenuList=MenuList),
        "Screens": screens,
        "Screens.Screen": mod("Screens.Screen", Screen=Screen),
    }
    spec = importlib.util.spec_from_file_location(
        "_test_warder_design." + name, str(ROOT / (name + ".py"))
    )
    item = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(item)
    return item


class WarderNativeUiTests(unittest.TestCase):
    def test_keyboard_uses_receiver_language_layout(self):
        m = load("keyboard")
        for locale, row, first in (
            ("sk_SK", "áčďéíľňšťž", "qwertyuiop"),
            ("cs_CZ", "áčďéěíňřšť", "qwertyuiop"),
            ("de_DE", "äöüßéèàâêî", "qwertzuiop"),
            ("en_GB", "@#:/_()+*?", "qwertyuiop"),
            ("fr_FR", "@#:/_()+*?", "qwertyuiop"),
        ):
            with self.subTest(locale=locale):
                rows = m.keyboard_rows(locale)
                self.assertEqual(len(rows), 5)
                self.assertTrue(all(len(part) == 10 for part in rows))
                self.assertEqual(rows[-1], row)
                self.assertEqual(rows[1], first)

    def test_keyboard_locale_and_numeric_entry_stay_native(self):
        m = load("keyboard")
        with patch.object(m, "keyboard_rows", return_value=m.keyboard_rows("de_DE")):
            k = m.WarderYouTubeKeyboard(None, value="test", limit=10)
        for fn in k.onLayoutFinish:
            fn()
        self.assertEqual(k["letter15"].text, "z")
        k._select(15)
        k.press_letter()
        self.assertEqual(k.value, "testz")
        k.toggle_case()
        self.assertEqual(k["letter15"].text, "Z")
        k.press_letter()
        self.assertEqual(k.value, "testzZ")
        k.delete()
        self.assertEqual(k.value, "testz")

    def test_keyboard_is_plugin_native_with_real_selection_and_typing(self):
        m = load("keyboard")
        k = m.WarderYouTubeKeyboard(None)
        for fn in k.onLayoutFinish:
            fn()
        self.assertTrue(k["focus10"].visible)
        self.assertFalse(k["focus11"].visible)
        k.press_letter()  # 'q'
        self.assertEqual(k.value, "q")
        k.right()
        k.press_letter()  # 'w'
        k.space()
        k.append("A")
        k.delete()
        self.assertEqual(k.value, "qw ")
        k.submit()
        self.assertEqual(k.closed_args, ("qw",))

    def test_keyboard_red_cancels_and_secret_value_is_masked(self):
        m = load("keyboard")
        k = m.WarderYouTubeKeyboard(None, value="", secret=True, limit=6)
        for fn in k.onLayoutFinish:
            fn()
        k.append("secret")
        self.assertEqual(k.value, "secret")
        self.assertNotIn("secret", k["input"].text)
        k.append("x")  # max length is respected
        self.assertEqual(k.value, "secret")
        k.cancel()
        self.assertEqual(k.closed_args, (None,))

    def test_keyboard_vertical_wrap_and_uppercase(self):
        m = load("keyboard")
        k = m.WarderYouTubeKeyboard(None)
        for fn in k.onLayoutFinish:
            fn()
        k.up()  # from q to numeric row
        self.assertEqual(k.position, 0)
        k.toggle_case()
        self.assertEqual(k["letter10"].text, "Q")

    def test_context_menu_never_saves_on_open(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(None, {"title": "Adele - Hello"}, False)
        self.assertEqual(len(screen.options), 4)
        self.assertEqual(screen.options[1][0], "favorite")
        self.assertIn("Add", screen.options[1][1])
        self.assertIsNone(screen.closed_args)
        screen["menu"].index = 1
        screen.choose()
        self.assertEqual(screen.closed_args, ("favorite",))

    def test_context_from_history_exposes_remove_and_clear(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(None, {"title": "One"}, True, "history")
        self.assertEqual([action for action, _ in screen.options],
                         ["play", "favorite", "info", "remove", "clear"])
        screen["menu"].index = 3
        screen.choose()
        self.assertEqual(screen.closed_args, ("remove",))

    def test_native_confirmation_defaults_to_no(self):
        m = load("confirm_ui")
        screen = m.WarderYouTubeConfirm(None, "Install test7?")
        self.assertEqual(screen["menu"].index, 0)
        screen.choose()
        self.assertEqual(screen.closed_args, (False,))
        other = m.WarderYouTubeConfirm(None, "Install test7?")
        other.accept()
        self.assertEqual(other.closed_args, (True,))

    def test_info_screen_is_full_native_and_bounded(self):
        m = load("info_ui")
        screen = m.WarderYouTubeInfo(None, "Video\n" + "A" * 5000)
        self.assertEqual(len(screen["body"].text), 2500)
        screen.close()
        self.assertEqual(screen.closed_args, ())

    def test_every_screen_has_four_colored_key_slots(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        specs = [ast.literal_eval(stmt.value)
                 for stmt in tree.body
                 if isinstance(stmt, ast.Assign) and
                 any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                     for t in stmt.targets)]
        self.assertEqual(len(specs), 11)
        for xml in specs:
            root = ET.fromstring(xml)
            names = {w.attrib["name"] for w in root.findall("widget")}
            self.assertTrue({"key_red", "key_green", "key_yellow", "key_blue"}.issubset(names),
                            root.attrib["name"])
            self.assertNotIn('render="', xml)


if __name__ == "__main__":
    unittest.main()
