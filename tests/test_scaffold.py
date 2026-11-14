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
        self.assertTrue({"nav0", "nav6", "heading", "subtitle", "status", "preview_thumb0", "preview_thumb5", "preview_message"}.issubset(
            {w.attrib.get("name") for w in screen.findall("widget")}))
        self.assertIn("images/warder_header.png", xml)
        self.assertEqual(xml.count("<ePixmap"), 8)
        self.assertIn('name="hdr_clock"', xml)
        # Search must display the actual system VirtualKeyBoard list/Input,
        # not a second fake 50-letter matrix made from Warder Labels.
        self.assertIn('name="kb_system_list"', xml)
        self.assertIn('name="kb_system_input"', xml)
        self.assertNotIn('name="kb_key0"', xml)
        self.assertNotIn('name="kb_focus0"', xml)
        self.assertNotIn('name="kb_input"', xml)
        home_source = (SRC / "ui.py").read_text(encoding="utf-8")
        system_source = (SRC / "system_keyboard_pane.py").read_text(encoding="utf-8")
        self.assertIn("SystemKeyboardPane(", home_source)
        self.assertNotIn("kb_characters", home_source)
        self.assertIn("from Screens.VirtualKeyBoard import VirtualKeyBoard", system_source)
        self.assertIn('backend["list"]', system_source)
        self.assertIn('backend["text"]', system_source)
        self.assertIn("backend.processSelect()", system_source)
        self.assertIn('name="hdr_version"', xml)
        icons = [p.attrib["pixmap"] for p in screen.findall("ePixmap")
                 if "/nav_" in p.attrib.get("pixmap", "")]
        self.assertEqual(len(icons), 7)
        self.assertEqual(set(icons), {
            "/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_%d.png" % i
            for i in (0, 1, 2, 3, 5, 6, 7)
        })
        widgets = {w.attrib.get("name"): w for w in screen.findall("widget")}
        for i in range(7):
            self.assertIn("/nav_focus.png", widgets["nav_focus%d" % i].attrib["pixmap"])
            self.assertEqual(widgets["nav_focus%d" % i].attrib["zPosition"], "2")
        for i in range(6):
            self.assertIn("/video_focus.png", widgets["preview_focus%d" % i].attrib["pixmap"])
            self.assertEqual(widgets["preview_focus%d" % i].attrib["zPosition"], "8")
        self.assertEqual(widgets["status"].attrib["position"], "427,939")
        self.assertEqual(widgets["status"].attrib["size"], "1410,28")
        self.assertEqual(widgets["hdr_clock"].attrib["font"], "Regular;60")
        self.assertEqual(widgets["hdr_clock"].attrib["valign"], "center")

    def test_inactive_video_borders_are_thin_dark_and_focus_is_bright(self):
        parsed = ast.parse((SRC / "skin.py").read_text(encoding="utf-8"))
        layouts = {}
        for stmt in parsed.body:
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Name) and target.id in ("HOME_SKIN", "GRID_SKIN"):
                        layouts[target.id] = ET.fromstring(ast.literal_eval(stmt.value))
        self.assertEqual(set(layouts), {"HOME_SKIN", "GRID_SKIN"})
        home = layouts["HOME_SKIN"]
        home_widgets = {w.attrib["name"]: w for w in home.findall("widget")}
        for i in range(6):
            border = home_widgets["preview_border%d" % i]
            panel = home_widgets["preview_panel%d" % i]
            focus = home_widgets["preview_focus%d" % i]
            self.assertEqual(border.attrib["backgroundColor"], "#0D5273")
            self.assertEqual(panel.attrib["size"], "473,320")
            self.assertEqual(focus.attrib["zPosition"], "8")
            self.assertIn("video_focus.png", focus.attrib["pixmap"])
        grid = layouts["GRID_SKIN"]
        grid_widgets = {w.attrib["name"]: w for w in grid.findall("widget")}
        for i in range(6):
            focus = grid_widgets["focus%d" % i]
            self.assertEqual(focus.attrib["zPosition"], "8")
            self.assertEqual(focus.attrib["alphatest"], "on")
            self.assertIn("grid_focus.png", focus.attrib["pixmap"])
            self.assertNotIn("backgroundColor", focus.attrib)
        subtle_borders = [item for item in grid.findall("eLabel")
                          if item.attrib.get("backgroundColor") == "#0D536F"]
        self.assertEqual(len(subtle_borders), 24)
        self.assertTrue(all(item.attrib["size"].startswith(("491,1", "1,355"))
                            for item in subtle_borders))
        self.assertNotIn('backgroundColor="#1AB4D5"', ET.tostring(grid, encoding="unicode"))

    def test_readme_reports_actual_owner_accepted_test24(self):
        readme = (ROOT / "README.md").read_text().lower()
        self.assertIn("0.0.8~test24", readme)
        self.assertIn("owner-confirmed", readme)
        self.assertIn("favourites", readme)
        self.assertIn("history", readme)
        self.assertIn("no stable release", readme)
        self.assertIn("original firmware virtualkeyboard", readme)
        self.assertIn("93b509055bfe63e1126ccca27f324829d8a2e0c6bbdd3d10976b30d7cf70935c", readme)
        self.assertIn("b7692b1ecd681b60e653f894d062c06a5bbf08ab5363594ecf2a353d6e79f459", readme)
        self.assertIn("WarderYouTubeLibrary", (SRC / "ui.py").read_text())
        self.assertIn("WarderYouTubeKeyboard", (SRC / "search.py").read_text())
        self.assertIn("fairbird", (ROOT / "docs/ASSIMILATION.md").read_text())

if __name__ == "__main__":
    unittest.main()
