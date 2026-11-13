"""Shared Warder family header: true local time, bounded timers, native skins."""
import importlib.util
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import ast

PKG = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class Label:
    def __init__(self, text=""):
        self.text = text
    def setText(self, text):
        self.text = text


class Timer:
    def __init__(self):
        self.listeners = []
        self.timeout = types.SimpleNamespace(get=lambda: self.listeners)
        self.running = False
        self.ms = None
    def start(self, ms, single=False):
        self.running = True
        self.ms = ms
    def stop(self):
        self.running = False
    def fire(self):
        if self.running:
            for callback in self.listeners[:]:
                callback()


class Screen(dict):
    def __init__(self):
        super().__init__()
        self.onShown = []
        self.onShow = []
        self.onHide = []
        self.onClose = []


@contextmanager
def header_module():
    root = types.ModuleType("_warder_header_test")
    root.__path__ = [str(PKG)]
    module_label = types.ModuleType("Components.Label")
    module_label.Label = Label
    components = types.ModuleType("Components")
    components.__path__ = []
    enigma = types.ModuleType("enigma")
    enigma.eTimer = Timer
    core = types.ModuleType("_warder_header_test.update_core")
    core.CURRENT_VERSION = "0.0.8~test23"
    language = types.ModuleType("_warder_header_test.i18n")
    language.language_code = lambda: "sk"
    mocked = {
        "_warder_header_test": root,
        "_warder_header_test.update_core": core,
        "_warder_header_test.i18n": language,
        "Components": components,
        "Components.Label": module_label,
        "enigma": enigma
    }
    spec = importlib.util.spec_from_file_location(
        "_warder_header_test.header_ui", PKG / "header_ui.py"
    )
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, mocked):
        spec.loader.exec_module(module)
        yield module


class HeaderTests(unittest.TestCase):
    def test_date_and_clock_use_local_language_and_seconds(self):
        with header_module() as m:
            t = datetime(2026, 11, 13, 11, 46, 38)
            self.assertEqual(
                m.header_strings(t, "sk"),
                ("Piatok", "13. novembra 2026", "11:46:38", "Verzia:")
            )
            self.assertEqual(m.header_strings(t, "cs")[0], "Pátek")
            self.assertEqual(m.header_strings(t, "de")[0], "Freitag")

    def test_one_second_timer_stops_when_hidden_and_closes_cleanly(self):
        with header_module() as m:
            sc = Screen()
            c = m.add_header(sc)
            self.assertEqual(len(sc), 6)
            self.assertIs(sc._warder_header, c)
            self.assertEqual(sc["hdr_version"].text, "0.0.8~test23")
            self.assertIn("Verzia:", sc["hdr_version_label"].text)
            self.assertIsNone(c.timer)
            for callback in sc.onShown:
                callback()
            self.assertTrue(c.timer.running)
            self.assertEqual(c.timer.ms, 1000)
            self.assertEqual(len(c.timer.listeners), 1)
            for callback in sc.onHide:
                callback()
            self.assertFalse(c.timer.running)
            for callback in sc.onShow:
                callback()
            self.assertTrue(c.timer.running)
            for callback in sc.onClose:
                callback()
            self.assertTrue(c.closed)
            self.assertEqual(c.timer, None)
            for callback in sc.onClose:
                callback()
            self.assertTrue(c.closed)

    def test_header_uses_the_owner_original_emblem_not_a_second_drawn_skull(self):
        artwork = (PKG / "images" / "warder_skull.png").read_bytes()
        self.assertEqual(artwork[:8], bytes((137, 80, 78, 71, 13, 10, 26, 10)))
        self.assertEqual(
            (int.from_bytes(artwork[16:20], "big"),
             int.from_bytes(artwork[20:24], "big")),
            (384, 429)
        )
        source = (PKG.parents[3] / "tools" / "warder_header_art.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('warder_skull.png', source)
        self.assertNotIn("Warder metallic cyber skull", source)
        self.assertNotIn("cx, cy = 94, 66", source)

    def test_full_original_source_and_whole_header_are_sha256_pinned(self):
        import hashlib
        tools_dir = PKG.parents[3] / "tools"
        spec = importlib.util.spec_from_file_location(
            "_warder_art_single_banner_test", str(tools_dir / "warder_header_art.py")
        )
        art = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(art)
        original = (PKG / "images/warder_skull.png").read_bytes()
        self.assertEqual((int.from_bytes(original[16:20], "big"),
                          int.from_bytes(original[20:24], "big")), (384, 429))
        self.assertEqual(hashlib.sha256(original).hexdigest(),
                         art.FULL_WARDER_SOURCE_SHA256)
        header = art.render_header()
        self.assertEqual(header[:8], bytes((137, 80, 78, 71, 13, 10, 26, 10)))
        self.assertEqual((int.from_bytes(header[16:20], "big"),
                          int.from_bytes(header[20:24], "big")), (1920, 152))
        self.assertEqual(header[24:26], bytes((8, 2)))
        self.assertEqual(hashlib.sha256(header).hexdigest(), art.FINAL_BANNER_SHA256)

    def test_signature_and_metallic_title_are_clean_single_png_not_old_masks(self):
        tools_dir = PKG.parents[3] / "tools"
        generator = (tools_dir / "render_full_header.py").read_text(encoding="utf-8")
        loader = (tools_dir / "warder_header_art.py").read_text(encoding="utf-8")
        builder = (tools_dir / "build_test_ipk.py").read_text(encoding="utf-8")
        for text in (loader, generator, builder):
            self.assertNotIn("warder_title_masks.py", text)
            self.assertNotIn("TITLE_MASK_B64", text)
            self.assertNotIn("BY_MASK_B64", text)
        self.assertIn('"YouTube Warder "', generator)
        self.assertIn('"Evolution"', generator)
        self.assertIn('"by Warder"', generator)
        self.assertIn("skull.resize((124,139)", generator)
        self.assertIn("complete original warder skull", loader.lower())
        # The complete image is committed once and consumed as a single RGB
        # PNG by all 12 screens, with live date/clock/version widgets separate.
        self.assertIn('images/warder_header.png', (PKG / "skin.py").read_text())

    def test_all_screens_use_two_compact_rows_above_planet_horizon(self):
        source = (PKG / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        skins = [ast.literal_eval(stmt.value)
                 for stmt in tree.body
                 if isinstance(stmt, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                         for t in stmt.targets)]
        self.assertEqual(len(skins), 12)
        for xml in skins:
            root = ET.fromstring(xml)
            nodes = {w.attrib.get("name"): w.attrib
                     for w in root.findall("widget")}
            for label, value in (("hdr_day", "hdr_date"),
                                 ("hdr_version_label", "hdr_version")):
                title_y = int(nodes[label]["position"].split(",")[1])
                title_h = int(nodes[label]["size"].split(",")[1])
                second_y = int(nodes[value]["position"].split(",")[1])
                second_h = int(nodes[value]["size"].split(",")[1])
                self.assertGreaterEqual(second_y, title_y + title_h)
                self.assertLessEqual(second_y - (title_y + title_h), 3)
                self.assertLessEqual(second_y + second_h, 110,
                                     (root.attrib["name"], value))
            clock_y = int(nodes["hdr_clock"]["position"].split(",")[1])
            clock_h = int(nodes["hdr_clock"]["size"].split(",")[1])
            self.assertLessEqual(clock_y + clock_h, 110,
                                 root.attrib["name"])

    def test_all_twelve_screens_have_standard_bottom_rule_and_key_bar(self):
        source = (PKG / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        skins = [ast.literal_eval(stmt.value)
                 for stmt in tree.body
                 if isinstance(stmt, ast.Assign)
                 and any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                         for t in stmt.targets)]
        self.assertEqual(len(skins), 12)
        accents = {"red": ("150", "#FF526A"),
                   "green": ("620", "#36E884"),
                   "yellow": ("1090", "#FFE065"),
                   "blue": ("1560", "#60BCFF")}
        for xml in skins:
            root = ET.fromstring(xml)
            self.assertEqual(root.attrib["backgroundColor"], "#08182D")
            labels = [x.attrib for x in root.findall("eLabel")]
            cyan = [x for x in labels if x.get("position") == "0,150"
                    and x.get("size") == "1920,3"]
            self.assertEqual(len(cyan), 1, root.attrib["name"])
            self.assertEqual(cyan[0]["backgroundColor"], "#1BEFF0")
            foot = [x for x in labels if x.get("size", "").startswith("1920,")
                    and int(x.get("position", "0,0").split(",")[1]) > 900]
            self.assertEqual(len(foot), 1, root.attrib["name"])
            self.assertEqual(foot[0]["backgroundColor"], "#08182D")
            widgets = {x.attrib.get("name"): x.attrib
                       for x in root.findall("widget")}
            key_prefix = ("warder_key_" if
                          root.attrib["name"] == "WarderNativeSearchKeyboard"
                          else "key_")
            for color, (x, rgb) in accents.items():
                bars = [el for el in labels if
                        el.get("position") == x + ",1070" and
                        el.get("size") == "195,3" and
                        el.get("backgroundColor") == rgb]
                self.assertEqual(len(bars), 1, (root.attrib["name"], color))
                key = widgets.get(key_prefix + color)
                self.assertIsNotNone(key, (root.attrib["name"], color))
                self.assertEqual(key["backgroundColor"], "#08182D")
                key_bottom = (int(key["position"].split(",")[1]) +
                              int(key["size"].split(",")[1]))
                self.assertLess(key_bottom, 1070)
            self.assertNotIn(',1003" size="195,3"', xml)

    def test_every_screen_uses_same_static_header_without_renderers(self):
        source = (PKG / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        skins = [
            ast.literal_eval(stmt.value)
            for stmt in tree.body if isinstance(stmt, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id.endswith("_SKIN")
                    for t in stmt.targets)
        ]
        self.assertEqual(len(skins), 12)
        for xml in skins:
            root = ET.fromstring(xml)
            pixmaps = [x for x in root.findall("ePixmap")
                       if "warder_header.png" in x.attrib.get("pixmap", "")]
            self.assertEqual(len(pixmaps), 1, root.attrib["name"])
            self.assertEqual(pixmaps[0].attrib["size"], "1920,152")
            clock = root.find('widget[@name="hdr_clock"]')
            self.assertEqual(clock.attrib["font"], "Regular;60")
            self.assertEqual(clock.attrib["valign"], "center")
            names = {x.attrib["name"] for x in root.findall("widget")}
            self.assertTrue({"hdr_day", "hdr_date", "hdr_clock", "hdr_seconds",
                             "hdr_version", "hdr_version_label"} <= names)
            self.assertFalse({"hdr_name", "hdr_evolution", "hdr_by"} & names)
            self.assertNotIn('render="', xml)


if __name__ == "__main__":
    unittest.main()
