"""Native page indicators for Home, Odbery and Search result galleries."""
import ast
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET


ROOT = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube")
spec = importlib.util.spec_from_file_location(
    "_tile_scrollbars_unit", ROOT / "tile_scrollbar.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class Widget:
    def __init__(self):
        self.visible = True
        self.instance = None

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


class Native:
    def __init__(self):
        self.size = None
        self.position = None

    def resize(self, size):
        self.size = size

    def move(self, pos):
        self.position = pos


class TileScrollbarTests(unittest.TestCase):
    def test_hidden_without_multiple_pages(self):
        track, thumb = Widget(), Widget()
        bar = mod.TilePageScrollbar(track, thumb, 1800, 220, 5, 650)
        self.assertFalse(track.visible)
        self.assertFalse(thumb.visible)
        bar.update(0, 1)
        self.assertFalse(track.visible)
        bar.update(0, 2)
        self.assertTrue(track.visible)
        self.assertTrue(thumb.visible)
        bar.update(0, 1)
        self.assertFalse(thumb.visible)

    def test_thumb_moves_down_and_reaches_bottom(self):
        track, thumb = Widget(), Widget()
        thumb.instance = Native()
        bar = mod.TilePageScrollbar(track, thumb, 1800, 220, 5, 650)
        fake = types.ModuleType("enigma")
        fake.eSize = lambda w, h: (w, h)
        fake.ePoint = lambda x, y: (x, y)
        with patch.dict(sys.modules, {"enigma": fake}):
            bar.update(0, 4)
            top0 = thumb.instance.position[1]
            self.assertEqual(top0, 220)
            self.assertEqual(thumb.instance.size[0], 5)
            bar.update(1, 4)
            self.assertGreater(thumb.instance.position[1], top0)
            bar.update(3, 4)
            self.assertEqual(
                thumb.instance.position[1] + thumb.instance.size[1],
                220 + 650
            )

    def test_page_number_is_safely_clamped(self):
        track, thumb = Widget(), Widget()
        bar = mod.TilePageScrollbar(track, thumb, 1800, 220, 5, 650)
        bar.update(300, 3)
        self.assertEqual(bar.page, 2)
        self.assertEqual(bar.pages, 3)
        bar.update(-20, 3)
        self.assertEqual(bar.page, 0)

    def test_home_and_search_skins_have_matching_native_scrollbars(self):
        tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
        skins = {
            target.id: ET.fromstring(ast.literal_eval(stmt.value))
            for stmt in tree.body if isinstance(stmt, ast.Assign)
            for target in stmt.targets
            if isinstance(target, ast.Name) and
            target.id in ("HOME_SKIN", "GRID_SKIN")
        }
        self.assertEqual(set(skins), {"HOME_SKIN", "GRID_SKIN"})
        for name, root in skins.items():
            nodes = {node.attrib.get("name"): node.attrib for node in root.findall("widget")}
            self.assertIn("video_scroll_track", nodes)
            self.assertIn("video_scroll_thumb", nodes)
            self.assertEqual(nodes["video_scroll_thumb"]["backgroundColor"], "#54D6FF")
            self.assertEqual(nodes["video_scroll_thumb"]["transparent"], "0")
            self.assertFalse(any("render" in attrs for attrs in nodes.values()))

    def test_home_and_search_code_uses_one_shared_indicator(self):
        for name in ("ui.py", "grid.py", "subscriptions_ui.py"):
            source = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("TilePageScrollbar", source)
            self.assertIn("page_scroll.update(", source)


if __name__ == "__main__":
    unittest.main()
