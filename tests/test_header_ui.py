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
    core.CURRENT_VERSION = "0.0.8~test12"
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
            self.assertEqual(len(sc), 5)
            self.assertIs(sc._warder_header, c)
            self.assertEqual(sc["hdr_version"].text, "0.0.8~test12")
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
            (104, 100)
        )
        source = (PKG.parents[3] / "tools" / "warder_header_art.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('warder_skull.png', source)
        self.assertNotIn("Warder metallic cyber skull", source)
        self.assertNotIn("cx, cy = 94, 66", source)

    def test_compact_original_title_masks_and_single_banner(self):
        import base64
        import zlib
        tools_dir = PKG.parents[3] / "tools"
        mask_code = (tools_dir / "warder_title_masks.py").read_text(encoding="utf-8")
        masks_spec = importlib.util.spec_from_file_location(
            "warder_title_masks_test", tools_dir / "warder_title_masks.py"
        )
        masks = importlib.util.module_from_spec(masks_spec)
        masks_spec.loader.exec_module(masks)
        for encoded, w, h in (
            (masks.TITLE_MASK_B64, masks.TITLE_WIDTH, masks.TITLE_HEIGHT),
            (masks.BY_MASK_B64, masks.BY_WIDTH, masks.BY_HEIGHT)
        ):
            decoded = zlib.decompress(base64.b64decode(encoded))
            self.assertEqual(len(decoded), (w*h+7)//8)
        artwork_code = (tools_dir / "warder_header_art.py").read_text(encoding="utf-8")
        self.assertIn('warder_title_masks.py', artwork_code)
        self.assertIn('warder_skull.png', artwork_code)
        self.assertNotIn('cx, cy = 94, 66', artwork_code)

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
            self.assertEqual(pixmaps[0].attrib["size"], "1920,134")
            names = {x.attrib["name"] for x in root.findall("widget")}
            self.assertTrue({"hdr_day", "hdr_date", "hdr_clock",
                             "hdr_version", "hdr_version_label"} <= names)
            self.assertFalse({"hdr_name", "hdr_evolution", "hdr_by"} & names)
            self.assertNotIn('render="', xml)


if __name__ == "__main__":
    unittest.main()
