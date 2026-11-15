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
    def test_all_updater_messages_have_non_english_system_translations(self):
        for lang in ("sk", "cs", "de"):
            for message in UPDATE_MESSAGES:
                if message in ("Enigma2",):
                    continue
                with self.subTest(lang=lang, message=message):
                    with patch.object(i18n, "language_code", return_value=lang):
                        result = i18n.tr(message)
                    if lang == "sk":
                        # Existing Slovak source literals legitimately remain unchanged.
                        if message in i18n.MESSAGES["en"] and (
                                i18n.MESSAGES["en"][message] != message):
                            self.assertNotEqual(result, message)
                    elif message in i18n.MESSAGES["en"]:
                        self.assertNotEqual(result, message,
                                            "Missing system-language message")

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
