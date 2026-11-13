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
        self.assertTrue({"menu", "heading", "description", "status", "footer"}.issubset(
            {w.attrib.get("name") for w in screen.findall("widget")}))
        self.assertNotIn("ePixmap", xml)

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
