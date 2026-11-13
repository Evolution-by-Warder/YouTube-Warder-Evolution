"""Source checks for GUI thread safety and native screen declarations."""
import ast
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "plugin/Plugins/Extensions/WarderYouTube"


class UiTests(unittest.TestCase):
    def test_native_xml_screens(self):
        module = ast.parse((PKG / "skin.py").read_text(encoding="utf-8"))
        values = {
            target.id: ast.literal_eval(node.value)
            for node in module.body if isinstance(node, ast.Assign)
            for target in node.targets if isinstance(target, ast.Name)
            and target.id.endswith("_SKIN")
        }
        self.assertEqual(set(values), {"HOME_SKIN", "SEARCH_SKIN", "SETTINGS_SKIN", "GRID_SKIN", "UPDATE_SKIN", "UPDATE_CHECK_SKIN", "LIBRARY_SKIN", "KEYBOARD_SKIN", "CONTEXT_SKIN", "CONFIRM_SKIN", "INFO_SKIN"})
        for name, xml in values.items():
            screen = ET.fromstring(xml)
            self.assertEqual(screen.attrib["size"], "1920,1080")
            self.assertEqual(screen.attrib["backgroundColor"], "#08182D")
            self.assertNotIn("<widget render=", xml, name)

    def test_worker_used_for_network(self):
        source = (PKG / "search.py").read_text(encoding="utf-8")
        self.assertIn("deferToThread(", source)
        self.assertIn("search_videos, self.query", source)
        self.assertIn("search_with_ytdlp, self.query", source)
        self.assertIn("self.closed", source)
        self.assertIn("request_version", source)

    def test_no_key_committed_or_logged(self):
        settings = (PKG / "settings.py").read_text(encoding="utf-8")
        self.assertIn("ConfigText(default=\"\", fixed_size=False)", settings)
        self.assertIn('value=""', settings)
        self.assertIn("secret=True", settings)
        self.assertNotIn("VirtualKeyBoard", settings)
        for name in ("settings.py", "search.py", "api.py"):
            self.assertNotIn("print(", (PKG / name).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
