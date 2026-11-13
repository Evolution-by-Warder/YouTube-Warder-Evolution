"""Source-only tests, no imports from an actual Enigma2 runtime."""
import ast
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "plugin/Plugins/Extensions/WarderYouTube"

class Tests(unittest.TestCase):
    def test_python_sources(self):
        for p in SRC.glob("*.py"):
            ast.parse(p.read_text(encoding="utf-8"), filename=str(p))

    def test_native_skin(self):
        module = ast.parse((SRC / "skin.py").read_text())
        value = next(n.value for n in module.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "HOME_SKIN" for t in n.targets))
        xml = ast.literal_eval(value)
        screen = ET.fromstring(xml)
        self.assertEqual(screen.attrib["size"], "1920,1080")
        self.assertEqual(screen.attrib["backgroundColor"], "#08182D")
        self.assertTrue({"nav0", "nav7", "heading", "subtitle", "status", "preview_thumb0", "preview_thumb5", "preview_message"}.issubset(
            {w.attrib.get("name") for w in screen.findall("widget")}))
        self.assertIn("images/warder_header.png", xml)
        self.assertEqual(xml.count("<ePixmap"), 9)
        self.assertIn('name="hdr_clock"', xml)
        self.assertIn('name="hdr_version"', xml)
        icons = [p.attrib["pixmap"] for p in screen.findall("ePixmap")
                 if "/nav_" in p.attrib.get("pixmap", "")]
        self.assertEqual(len(icons), 8)
        self.assertEqual(set(icons), {
            "/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_%d.png" % i
            for i in range(8)
        })
        widgets = {w.attrib.get("name"): w for w in screen.findall("widget")}
        for i in range(8):
            self.assertIn("/nav_focus.png", widgets["nav_focus%d" % i].attrib["pixmap"])
            self.assertEqual(widgets["nav_focus%d" % i].attrib["zPosition"], "2")
        for i in range(6):
            self.assertIn("/video_focus.png", widgets["preview_focus%d" % i].attrib["pixmap"])
            self.assertEqual(widgets["preview_focus%d" % i].attrib["zPosition"], "8")
        self.assertEqual(widgets["status"].attrib["position"], "427,938")
        self.assertEqual(widgets["status"].attrib["size"], "1410,28")
        self.assertEqual(widgets["hdr_clock"].attrib["font"], "Regular;51")
        self.assertEqual(widgets["hdr_clock"].attrib["valign"], "bottom")

    def test_no_fake_youtube(self):
        readme = (ROOT / "README.md").read_text().lower()
        self.assertIn("0.0.8~test5", readme)
        self.assertIn("favourites", readme)
        self.assertIn("history", readme)
        self.assertIn("no stable release", readme)
        self.assertIn("owner-installed test5 does not include these changes", readme)
        self.assertIn("WarderYouTubeLibrary", (SRC / "ui.py").read_text())
        self.assertIn("WarderYouTubeKeyboard", (SRC / "search.py").read_text())
        self.assertIn("fairbird", (ROOT / "docs/ASSIMILATION.md").read_text())

if __name__ == "__main__":
    unittest.main()
