"""System-language regression tests for update messages shown in the right pane."""
import importlib.util
import ast
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
I18N = ROOT / "plugin/Plugins/Extensions/WarderYouTube/i18n.py"
INLINE = ROOT / "plugin/Plugins/Extensions/WarderYouTube/inline_update.py"

spec = importlib.util.spec_from_file_location("_warder_system_language", I18N)
i18n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i18n)

UPDATE_MESSAGES = sorted({
    node.args[0].value
    for node in ast.walk(ast.parse(INLINE.read_text(encoding="utf-8")))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    and node.func.id == "_" and node.args
    and isinstance(node.args[0], ast.Constant)
    and isinstance(node.args[0].value, str)
})


class InlineUpdateLanguageTests(unittest.TestCase):
    def test_english_updater_statuses_are_translated_for_non_english_images(self):
        messages = (
            "Updates are checked only on request.",
            "Press OK to check updates.",
            "Update failed",
            "Installation completed.",
            "You are up to date.",
            "Checking updates",
            "New version available",
            "Download finished: 100%",
        )
        self.assertTrue(set(messages).issubset(set(UPDATE_MESSAGES)))
        for lang in ("sk", "cs", "de"):
            for message in messages:
                with self.subTest(lang=lang, message=message):
                    with patch.object(i18n, "language_code", return_value=lang):
                        self.assertNotEqual(i18n.tr(message), message)

    def test_up_to_date_status_and_last_line_in_each_system_language(self):
        expected = {
            "sk": ("Používaš najnovšiu verziu.",
                   "Aktualizácie sa kontrolujú iba na vyžiadanie."),
            "cs": ("Používáš nejnovější verzi.",
                   "Aktualizace se kontrolují pouze na vyžádání."),
            "en": ("You are up to date.",
                   "Updates are checked only on request."),
            "de": ("Du verwendest die neueste Version.",
                   "Updates werden nur auf Anfrage geprüft."),
        }
        for lang, (status, hint) in expected.items():
            with self.subTest(lang=lang):
                with patch.object(i18n, "language_code", return_value=lang):
                    self.assertEqual(i18n.tr("You are up to date."), status)
                    self.assertEqual(
                        i18n.tr("Updates are checked only on request."), hint)

    def test_embedded_firmware_keyboard_has_opaque_pane_background(self):
        import ast
        import xml.etree.ElementTree as ET
        source = (I18N.parent / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        home = next(ast.literal_eval(node.value) for node in tree.body
                    if isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "HOME_SKIN"
                            for target in node.targets))
        keyboard = next(widget for widget in ET.fromstring(home).findall("widget")
                        if widget.get("name") == "kb_system_list")
        self.assertEqual(keyboard.get("transparent"), "0")
        self.assertEqual(keyboard.get("backgroundColor"), "#10263E")
        self.assertEqual(keyboard.get("scrollbarMode"), "showNever")

    def test_failure_and_installation_text_are_localized(self):
        for lang in ("sk", "cs", "de"):
            with patch.object(i18n, "language_code", return_value=lang):
                self.assertNotEqual(i18n.tr("Update failed"), "Update failed")
                self.assertNotEqual(i18n.tr("Installation completed."),
                                    "Installation completed.")
                self.assertNotEqual(i18n.tr("Press OK to check updates."),
                                    "Press OK to check updates.")


if __name__ == "__main__":
    unittest.main()
