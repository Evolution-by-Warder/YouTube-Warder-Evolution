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


class ScrollLabel(Label):
    def __init__(self, text=""):
        super().__init__(text)
        self.page_up_calls = 0
        self.page_down_calls = 0

    def pageUp(self):
        self.page_up_calls += 1

    def pageDown(self):
        self.page_down_calls += 1


class ActionBindings(Label):
    def __init__(self, contexts, bindings, *args, **kwargs):
        super().__init__()
        self.contexts = contexts
        self.bindings = bindings


class MenuList:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0
        self.onSelectionChanged = []
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


class SystemKeyboard(Screen):
    def __init__(self, session, title=None, text="", maxSize=False):
        Screen.__init__(self, session)
        self.skinName = ["VirtualKeyboard", "VirtualKeyBoard"]
        self.system_title = title
        self.system_text = text
        self.system_limit = maxSize


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
        "_test_warder_design.header_ui": mod("_test_warder_design.header_ui", add_header=lambda sc: sc.__setitem__("hdr_version", Label())),
        "_test_warder_design": package,
        "_test_warder_design.i18n": mod(
            "_test_warder_design.i18n", tr=lambda message: message,
            language_code=lambda: "sk"
        ),
        "_test_warder_design.skin": mod(
            "_test_warder_design.skin",
            KEYBOARD_SKIN="<screen/>", CONTEXT_SKIN="<screen/>",
            CONFIRM_SKIN="<screen/>", INFO_SKIN="<screen/>",
            HOME_SKIN="<screen/>", NATIVE_SEARCH_KEYBOARD_SKIN="<screen/>"
        ),
        "Components": components,
        "Components.ActionMap": mod(
            "Components.ActionMap", ActionMap=ActionBindings
        ),
        "Components.Label": mod("Components.Label", Label=Label),
        "Components.ScrollLabel": mod("Components.ScrollLabel", ScrollLabel=ScrollLabel),
        "Screens.MessageBox": mod("Screens.MessageBox", MessageBox=object),
        "_test_warder_design.update_core": mod(
            "_test_warder_design.update_core", CURRENT_VERSION="0.0.8~test7"
        ),
        "Components.MenuList": mod("Components.MenuList", MenuList=MenuList),
        "Screens": screens,
        "Screens.Screen": mod("Screens.Screen", Screen=Screen),
        "Screens.VirtualKeyBoard": mod(
            "Screens.VirtualKeyBoard", VirtualKeyBoard=SystemKeyboard
        ),
    }
    spec = importlib.util.spec_from_file_location(
        "_test_warder_design." + name, str(ROOT / (name + ".py"))
    )
    item = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(item)
    return item


class WarderNativeUiTests(unittest.TestCase):
    def test_real_system_keyboard_keeps_firmware_logic_and_warder_skin(self):
        native = load("native_keyboard")
        keyboard = native.WarderNativeSearchKeyboard(
            None, value="adele", title="Search videos", limit=160
        )
        self.assertIsInstance(keyboard, SystemKeyboard)
        self.assertEqual(keyboard.system_text, "adele")
        self.assertEqual(keyboard.system_title, "Search videos")
        self.assertIs(keyboard.system_limit, False)
        self.assertEqual(keyboard._warder_limit, 160)
        self.assertEqual(keyboard.skinName, ["WarderNativeSearchKeyboard"])
        self.assertEqual(keyboard["warder_brand"].text, "YouTube Warder Evolution")
        self.assertEqual(keyboard["warder_key_red"].text, "Cancel")
        self.assertEqual(keyboard["warder_key_green"].text, "Confirm")
        self.assertEqual(keyboard["warder_key_yellow"].text, "Shift")
        self.assertEqual(keyboard["warder_key_blue"].text, "Aa")

    def test_keyboard_geometry_is_centered_on_native_key_dimensions(self):
        m = load("native_keyboard")
        left, top, width, height = m.keyboard_geometry(67, 67, 14, 5)
        self.assertEqual((left, width), (487, 946))
        self.assertEqual(left + width // 2, 960)
        self.assertGreaterEqual(top, 350)
        self.assertLessEqual(top + height, 820)
        for bad in ((0, 67, 14, 5), (140, 67, 14, 5),
                    (67, 100, 14, 5), (67, 67, 50, 5)):
            with self.assertRaises(ValueError):
                m.keyboard_geometry(*bad)

    def test_layout_repositions_list_and_shows_only_one_line_of_locale(self):
        m = load("native_keyboard")
        keyboard = m.WarderNativeSearchKeyboard(None)
        keyboard.width = 67
        keyboard.height = 67
        keyboard.keyboardWidth = 14
        keyboard.keyboardHeight = 5
        keyboard.locale = "sk_SK"
        keyboard["locale"] = Label("")
        keyboard["language"] = Label("")
        positions = {}
        class ListWidget:
            def resize(self, size):
                positions["size"] = size
            def move(self, point):
                positions["point"] = point
        keyboard["list"] = types.SimpleNamespace(instance=ListWidget())
        with patch.dict(sys.modules, {
            "enigma": mod("enigma",
                          ePoint=lambda x, y: (x, y),
                          eSize=lambda w, h: (w, h))
        }):
            keyboard._align_native_keys()
        self.assertEqual(positions["size"], (946, 343))
        self.assertEqual(positions["point"][0], 487)
        self.assertEqual(keyboard["locale"].text, "Keyboard layout: sk_SK")
        self.assertEqual(keyboard["language"].text, "Language from Enigma2")
        self.assertNotIn("\\n", keyboard["locale"].text)
        self.assertNotIn("\\n", keyboard["language"].text)

    def test_real_system_keyboard_does_not_expose_api_key(self):
        native = load("native_keyboard")
        with self.assertRaises(ValueError):
            native.WarderNativeSearchKeyboard(
                None, value="AIzafake-secret", secret=True
            )

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

    def test_home_has_eight_direct_navigation_rows(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        home = next(ast.literal_eval(stmt.value) for stmt in tree.body
                    if isinstance(stmt, ast.Assign) and any(
                        isinstance(target, ast.Name) and target.id == "HOME_SKIN"
                        for target in stmt.targets))
        screen = ET.fromstring(home)
        names = {w.attrib["name"] for w in screen.findall("widget")}
        self.assertTrue({"nav0", "nav7", "preview_thumb0", "preview_thumb5",
                         "preview_message", "heading"}.issubset(names))
        self.assertNotIn("nav_title", names)
        self.assertNotIn("card1_title", names)

    def test_context_highlight_tracks_selected_action(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(None, {"title": "Adele"}, False)
        for callback in screen.onLayoutFinish:
            callback()
        self.assertTrue(screen["context_focus0"].visible)
        screen.down()
        screen.down()
        self.assertFalse(screen["context_focus0"].visible)
        self.assertTrue(screen["context_focus2"].visible)
        self.assertFalse(screen["context_focus4"].visible)
        screen.choose()
        self.assertEqual(screen.closed_args, ("info",))

    def test_all_native_widgets_have_explicit_foreground_layer(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        for stmt in tree.body:
            if not isinstance(stmt, ast.Assign) or not any(
                isinstance(target, ast.Name) and target.id.endswith("_SKIN")
                for target in stmt.targets
            ):
                continue
            root = ET.fromstring(ast.literal_eval(stmt.value))
            for widget in root.findall("widget"):
                name = widget.attrib["name"]
                self.assertIn("zPosition", widget.attrib,
                              (root.attrib["name"], name))
                # Existing grid focus underlays and bottom button-bar
                # footers deliberately live below the content layer.
                if name.startswith(("focus", "preview_border")) or name == "footer":
                    continue
                self.assertGreaterEqual(
                    int(widget.attrib["zPosition"]), 2,
                    (root.attrib["name"], name)
                )

    def test_context_menu_never_saves_on_open(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(None, {"title": "Adele - Hello"}, False)
        self.assertEqual(len(screen.options), 4)
        self.assertEqual(screen.options[1][0], "favorite")
        self.assertIn("Add", screen.options[1][1])
        self.assertIsNone(screen.closed_args)
        screen.down()
        screen.choose()
        self.assertEqual(screen.closed_args, ("favorite",))

    def test_context_from_history_exposes_remove_and_clear(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(None, {"title": "One"}, True, "history")
        self.assertEqual([action for action, _ in screen.options],
                         ["play", "favorite", "info", "remove", "clear"])
        for _ in range(3):
            screen.down()
        screen.choose()
        self.assertEqual(screen.closed_args, ("remove",))

    def test_favourites_menu_has_no_duplicate_remove_action(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(
            None, {"title": "Saved song"}, True, "favourites"
        )
        # The user-confirmed test24 has two equivalent single-item actions.
        # Keep 'Remove video from favourites' but never show a duplicate delete.
        self.assertEqual([action for action, _ in screen.options],
                         ["play", "favorite", "info", "clear"])
        self.assertEqual(screen.options[1][1], "Remove video from favourites")
        self.assertEqual(screen.options[3][1], "Clear all favourite videos")
        self.assertEqual(screen["key_blue"].text, "Clear all favourite videos")
        self.assertNotIn("remove", [action for action, _ in screen.options])
        self.assertNotIn("Delete", [label for _, label in screen.options])
        self.assertEqual(screen["context_row4"].text, "")
        self.assertFalse(screen["context_focus4"].visible)
        screen.down()
        screen.choose()
        self.assertEqual(screen.closed_args, ("favorite",))

    def test_favourites_clear_all_is_separate_confirmation_action(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(
            None, {"title": "Saved song"}, True, "favourites"
        )
        for _ in range(3):
            screen.down()
        self.assertTrue(screen["context_focus3"].visible)
        self.assertFalse(screen["context_focus4"].visible)
        screen.choose()
        self.assertEqual(screen.closed_args, ("clear",))

    def test_history_still_has_distinct_single_record_delete(self):
        m = load("context_menu")
        screen = m.WarderYouTubeContext(
            None, {"title": "Watched song"}, False, "history"
        )
        self.assertEqual([action for action, _ in screen.options],
                         ["play", "favorite", "info", "remove", "clear"])
        self.assertEqual(screen.options[3][1], "Delete video from history")
        self.assertEqual(screen.options[4][1], "Clear entire history")
        self.assertEqual(screen["key_blue"].text, "Clear entire history")

    def test_every_video_context_action_identifies_exact_target(self):
        m = load("context_menu")
        for mode, favourite, expected in (
            ("search", False, ["Play video", "Add video to favourites",
                               "Video details", "New search"]),
            ("favourites", True, ["Play video", "Remove video from favourites",
                                  "Video details", "Clear all favourite videos"]),
            ("history", False, ["Play video", "Add video to favourites",
                                "Video details", "Delete video from history",
                                "Clear entire history"])
        ):
            with self.subTest(mode=mode):
                screen = m.WarderYouTubeContext(
                    None, {"title": "Example video"}, favourite, mode
                )
                self.assertEqual([label for _, label in screen.options], expected)
                self.assertNotIn("Delete", [label for _, label in screen.options])
                self.assertNotIn("Clear", [label for _, label in screen.options])
                self.assertNotIn("Clear all", [label for _, label in screen.options])
                self.assertNotIn("Remove", [label for _, label in screen.options])

    def test_native_confirmation_defaults_to_no(self):
        m = load("confirm_ui")
        screen = m.WarderYouTubeConfirm(None, "Install test7?")
        self.assertEqual(screen.selected, 0)
        self.assertTrue(screen["confirm_focus0"].visible)
        screen.down()
        self.assertTrue(screen["confirm_focus1"].visible)
        screen.up()
        self.assertTrue(screen["confirm_focus0"].visible)
        screen.choose()
        self.assertEqual(screen.closed_args, (False,))
        other = m.WarderYouTubeConfirm(None, "Install test7?")
        other.accept()
        self.assertEqual(other.closed_args, (True,))

    def test_info_screen_is_full_native_and_bounded(self):
        m = load("info_ui")
        screen = m.WarderYouTubeInfo(None, "Video\n" + "A" * 5000)
        self.assertIsInstance(screen["body"], ScrollLabel)
        self.assertEqual(len(screen["body"].text), 2500)
        self.assertEqual(screen["key_yellow"].text, "Scroll up")
        self.assertEqual(screen["key_blue"].text, "Scroll down")
        controls = screen["actions"]
        self.assertIn("DirectionActions", controls.contexts)
        for key in ("up", "yellow", "pageUp"):
            controls.bindings[key]()
        for key in ("down", "blue", "pageDown"):
            controls.bindings[key]()
        self.assertEqual(screen["body"].page_up_calls, 3)
        self.assertEqual(screen["body"].page_down_calls, 3)
        controls.bindings["ok"]()
        self.assertEqual(screen.closed_args, ())

    def test_all_twelve_screens_use_colored_text_and_thin_lines_not_rectangles(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        specs = [ast.literal_eval(stmt.value)
                 for stmt in tree.body if isinstance(stmt, ast.Assign) and
                 any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                     for t in stmt.targets)]
        self.assertEqual(len(specs), 12)
        for xml in specs:
            root = ET.fromstring(xml)
            lines = [item for item in root.findall("eLabel")
                     if item.attrib.get("size") == "195,3"
                     and item.attrib.get("position", "").endswith(",1070")]
            self.assertEqual(len(lines), 4, root.attrib["name"])
            self.assertFalse(any(item.attrib.get("size") == "415,58"
                                 for item in root.findall("eLabel")))
            keys = {w.attrib["name"]: w for w in root.findall("widget")}
            for name, color in (("red", "#FE637D"), ("green", "#4CE58B"),
                                ("yellow", "#FFD367"), ("blue", "#5EBEFF")):
                key = ("warder_key_" if root.attrib["name"] == "WarderNativeSearchKeyboard"
                       else "key_") + name
                self.assertEqual(keys[key].attrib["foregroundColor"], color)
                self.assertEqual(keys[key].attrib["halign"], "center")
                self.assertEqual(keys[key].attrib["transparent"], "1")
                self.assertEqual(keys[key].attrib["backgroundColor"], "#08182D")
                self.assertLess(int(keys[key].attrib["position"].split(",")[1]) +
                                int(keys[key].attrib["size"].split(",")[1]), 1070)

    def test_context_and_confirm_use_opaque_native_selection_not_listbox(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        for stmt in tree.body:
            if not isinstance(stmt, ast.Assign):
                continue
            if not any(isinstance(t, ast.Name) and t.id in ("CONTEXT_SKIN", "CONFIRM_SKIN")
                       for t in stmt.targets):
                continue
            root = ET.fromstring(ast.literal_eval(stmt.value))
            names = {w.attrib["name"]: w for w in root.findall("widget")}
            self.assertNotIn("menu", names)
            prefix = "context" if root.attrib["name"] == "WarderYouTubeContext" else "confirm"
            count = 5 if prefix == "context" else 2
            for i in range(count):
                self.assertEqual(names["%s_focus%d" % (prefix, i)].attrib["transparent"], "0")
                self.assertIn("backgroundColor", names["%s_focus%d" % (prefix, i)].attrib)
                self.assertIn("%s_row%d" % (prefix, i), names)

    def test_every_screen_has_four_colored_key_slots(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        specs = [ast.literal_eval(stmt.value)
                 for stmt in tree.body
                 if isinstance(stmt, ast.Assign) and
                 any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                     for t in stmt.targets)]
        self.assertEqual(len(specs), 12)
        for xml in specs:
            root = ET.fromstring(xml)
            names = {w.attrib["name"] for w in root.findall("widget")}
            expected = ({"warder_key_red", "warder_key_green",
                         "warder_key_yellow", "warder_key_blue"}
                        if root.attrib["name"] == "WarderNativeSearchKeyboard"
                        else {"key_red", "key_green", "key_yellow", "key_blue"})
            self.assertTrue(expected.issubset(names), root.attrib["name"])
            self.assertNotIn('render="', xml)


if __name__ == "__main__":
    unittest.main()
