"""Ensure the stable YouTube package has a single consistent version."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PKG = ROOT / "plugin/Plugins/Extensions/WarderYouTube"

class StableReleaseConsistencyTests(unittest.TestCase):
    def test_source_control_readme_release_notes_are_all_102(self):
        control = (ROOT / "packaging/CONTROL/control").read_text()
        self.assertIn("Version: 1.0.2\n", control)
        source = (PKG / "update_core.py").read_text()
        self.assertIn('CURRENT_VERSION = "1.0.2"', source)
        self.assertTrue((ROOT / "RELEASE_NOTES_1.0.2.md").is_file())
        self.assertIn("Stable release: 1.0.2", (ROOT / "README.md").read_text())
        self.assertIn("1.0.2_all.ipk", (ROOT / "RELEASE_NOTES_1.0.2.md").read_text())

    def test_test_builder_remains_separate_and_main_menu_opt_in(self):
        source = (ROOT / "tools/build_test_ipk.py").read_text()
        self.assertIn('VERSION = "1.0.2~test1"', source)
        self.assertIn('CURRENT_VERSION = "1.0.2"', source)
        settings = (PKG / "settings.py").read_text()
        self.assertIn("ConfigYesNo(default=False)", settings)
        entry = (PKG / "plugin.py").read_text()
        self.assertIn("PluginDescriptor.WHERE_MENU", entry)
        self.assertIn('menuid != "mainmenu"', entry)

if __name__ == "__main__":
    unittest.main()
