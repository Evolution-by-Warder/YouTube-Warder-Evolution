"""Native settings list stays inside Warder's existing three-zone layout."""
import ast
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

SRC = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/skin.py"

class SettingsLayoutTests(unittest.TestCase):
    def test_settings_use_one_native_list_with_room_for_additional_options(self):
        parsed = ast.parse(SRC.read_text(encoding="utf-8"))
        xml = next(ast.literal_eval(node.value) for node in parsed.body
                   if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "SETTINGS_SKIN"
                           for t in node.targets))
        root = ET.fromstring(xml)
        self.assertEqual(root.attrib["size"], "1920,1080")
        widgets = {w.get("name"): w for w in root.findall("widget")}
        options = widgets["options"]
        self.assertEqual(options.get("position"), "76,320")
        self.assertEqual(options.get("size"), "1755,388")
        self.assertEqual(options.get("itemHeight"), "76")
        self.assertEqual(options.get("backgroundColorSelected"), "#2B70A8")
        self.assertEqual(widgets["key_green"].get("size"), "381,45")
        self.assertLess(320 + 388, int(widgets["status"].get("position").split(",")[1]))
        self.assertTrue(any("warder_header.png" in el.get("pixmap", "")
                            for el in root.findall("ePixmap")))
        self.assertEqual(len(root.findall("widget[@name='options']")), 1)


if __name__ == "__main__":
    unittest.main()
