"""Full-width one-line chip rail and near-edge-to-edge video card checks."""
import ast
import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

ROOT = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube")
spec = importlib.util.spec_from_file_location("_chip_layout_test", ROOT / "chip_layout.py")
rail = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rail)


def xml_skins():
    module = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
    return {
        target.id: ET.fromstring(ast.literal_eval(node.value))
        for node in module.body if isinstance(node, ast.Assign)
        for target in node.targets if isinstance(target, ast.Name)
        and target.id in ("HOME_SKIN", "GRID_SKIN")
    }


class ChipLayoutTests(unittest.TestCase):
    def test_long_categories_fit_with_fewer_visible_slots_without_wrap(self):
        chips = ["Všetko", "Nové odbery", "DŘEVOSTAVBY", "Florida Filip",
                 "Florida Filip Family", "Jiří Stuchlý", "Marphy", "Technika"]
        offset, slots, before, after = rail.layout_chips(chips, 0, 0)
        self.assertEqual(offset, 0)
        self.assertGreaterEqual(len(slots), 2)
        self.assertLess(len(slots), 7)  # genuinely fewer labels fit
        self.assertFalse(before)
        self.assertTrue(after)
        for index, x, width in slots:
            self.assertGreaterEqual(x, rail.CHIP_LEFT)
            self.assertLessEqual(x + width, rail.CHIP_RIGHT)
            self.assertGreaterEqual(width, rail.chip_width(chips[index]))
        # Navigate across all items; selected label never disappears.
        for selected in range(len(chips)):
            offset, slots, before, after = rail.layout_chips(
                chips, selected, offset)
            self.assertIn(selected, [idx for idx, _, _ in slots])
            self.assertLessEqual(slots[-1][1] + slots[-1][2], rail.CHIP_RIGHT)
        self.assertFalse(after)

    def test_wide_single_label_uses_its_own_slot(self):
        chips = ["Všetko", "This is a longer localized category name",
                 "Kanal A", "Kanal B"]
        offset, slots, _, _ = rail.layout_chips(chips, 1)
        self.assertEqual(offset, 0)
        self.assertIn(1, [i for i, _, _ in slots])
        self.assertLessEqual(slots[-1][1] + slots[-1][2], rail.CHIP_RIGHT)

    def test_home_and_grid_thumbnails_fill_card_width_without_side_strips(self):
        skins = xml_skins()
        home = {item.get("name"): item for item in skins["HOME_SKIN"].findall("widget")}
        grid = {item.get("name"): item for item in skins["GRID_SKIN"].findall("widget")}
        for i in range(6):
            picture = home["preview_thumb%d" % i]
            panel = home["preview_panel%d" % i]
            x1, y1 = map(int, picture.get("position").split(","))
            x2, y2 = map(int, panel.get("position").split(","))
            pw, ph = map(int, picture.get("size").split(","))
            ww, wh = map(int, panel.get("size").split(","))
            self.assertEqual(x1, x2)
            self.assertEqual(x1 + pw, x2 + ww)
            self.assertAlmostEqual(pw / float(ph), 16 / 9, delta=0.02)
            self.assertEqual(picture.get("zPosition"), "4")
            gthumb = grid["thumb%d" % i]
            self.assertEqual(gthumb.get("size"), "491,276")
            self.assertEqual(gthumb.get("zPosition"), "2")


if __name__ == "__main__":
    unittest.main()
