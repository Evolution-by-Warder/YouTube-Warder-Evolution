"""Live Enigma2 language selection drives Warder UI without user overrides."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

P = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/i18n.py"
spec = importlib.util.spec_from_file_location("_warder_locales", P)
lang = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lang)


class LanguageTests(unittest.TestCase):
    def translate(self, code, phrase):
        components = types.ModuleType("Components")
        components.__path__ = []
        language = types.ModuleType("Components.Language")
        language.language = types.SimpleNamespace(getLanguage=lambda: code)
        with patch.dict(sys.modules, {"Components": components, "Components.Language": language}):
            return lang.tr(phrase)

    def test_language_is_read_from_enigma2(self):
        self.assertEqual(self.translate("sk_SK", "Search"), "Hľadať")
        self.assertEqual(self.translate("cs_CZ", "Search"), "Hledat")
        self.assertEqual(self.translate("de_DE", "Search"), "Suche")
        self.assertEqual(self.translate("en_GB", "Search"), "Search")

    def test_single_favourite_removal_is_distinct_from_clear_all(self):
        strings = {
            "sk_SK": ("Odobrať z obľúbených", "Vymazať všetky obľúbené",
                      "Vymazať celú históriu", "Vymazať všetko"),
            "cs_CZ": ("Odebrat z oblíbených", "Vymazat všechny oblíbené",
                      "Vymazat celou historii", "Vymazat vše"),
            "de_DE": ("Aus Favoriten entfernen", "Alle Favoriten löschen",
                      "Gesamten Verlauf löschen", "Alles löschen"),
            "en_GB": ("Remove from favourites", "Clear all favourites",
                      "Clear entire history", "Clear all")
        }
        for locale, expected in strings.items():
            with self.subTest(locale=locale):
                values = tuple(self.translate(locale, key) for key in (
                    "Remove from favourites", "Clear all favourites",
                    "Clear entire history", "Clear all"
                ))
                self.assertEqual(values, expected)

    def test_all_destructive_actions_specify_their_target_in_every_language(self):
        keys = (
            "Remove video from favourites", "Clear all favourite videos",
            "Delete video from history", "Clear entire history",
            "Clear favourites", "Clear history", "Delete from history",
            "Delete character", "Add video to favourites",
        )
        values = {
            "sk_SK": (
                "Odobrať video z obľúbených", "Vymazať všetky obľúbené videá",
                "Zmazať video z histórie", "Vymazať celú históriu",
                "Vymazať obľúbené", "Vymazať históriu",
                "Zmazať z histórie", "Zmazať znak", "Pridať video do obľúbených",
            ),
            "cs_CZ": (
                "Odebrat video z oblíbených", "Vymazat všechna oblíbená videa",
                "Smazat video z historie", "Vymazat celou historii",
                "Vymazat oblíbené", "Vymazat historii",
                "Smazat z historie", "Smazat znak", "Přidat video do oblíbených",
            ),
            "de_DE": (
                "Video aus Favoriten entfernen", "Alle Favoritenvideos löschen",
                "Video aus Verlauf löschen", "Gesamten Verlauf löschen",
                "Favoriten löschen", "Verlauf löschen",
                "Aus Verlauf löschen", "Zeichen löschen",
                "Video zu Favoriten hinzufügen",
            ),
            "en_GB": keys,
        }
        for language, expected in values.items():
            with self.subTest(language=language):
                translated = tuple(self.translate(language, label) for label in keys)
                self.assertEqual(translated, expected)

    def test_library_key_legends_name_history_or_favourites(self):
        keys = (
            "OK: play · INFO: details · MENU: actions · YELLOW: remove favourite · BLUE: clear favourites · EXIT: home",
            "OK: play · INFO: details · MENU: actions · YELLOW: delete from history · BLUE: clear history · EXIT: home",
        )
        for language in ("sk_SK", "cs_CZ", "de_DE", "en_GB"):
            with self.subTest(language=language):
                favourite, history = tuple(self.translate(language, key) for key in keys)
                self.assertNotEqual(favourite, history)
                self.assertTrue(favourite)
                self.assertTrue(history)
                self.assertNotIn("YELLOW: delete from history", favourite)
                self.assertNotIn("BLUE: clear favourites", history)

    def test_key_legends_follow_receiver_language(self):
        self.assertEqual(self.translate("sk_SK", "Updates"), "Aktualizácie")
        self.assertEqual(self.translate("cs_CZ", "Updates"), "Aktualizace")
        self.assertEqual(self.translate("de_DE", "Updates"), "Updates")
        self.assertEqual(self.translate("en_GB", "Updates"), "Updates")

    def test_settings_slovak_string_falls_back_to_english(self):
        source = "API kľúč: nastavený"
        self.assertEqual(self.translate("sk_SK", source), source)
        self.assertEqual(self.translate("en_GB", source), "API key: configured")
        self.assertEqual(self.translate("pl_PL", source), "API key: configured")

    def test_default_german_and_czech_status(self):
        source = "Testovací kanál: používate najnovšiu dostupnú verziu."
        self.assertIn("Testkanal", self.translate("de_DE", source))
        self.assertIn("Testovací", self.translate("cs_CZ", source))

    def test_unknown_keys_stay_human_readable(self):
        self.assertEqual(self.translate("en_GB", "Warder Evolution"), "Warder Evolution")


if __name__ == "__main__":
    unittest.main()
