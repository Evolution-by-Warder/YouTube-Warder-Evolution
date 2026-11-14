"""Owner-requested official Home categories and daily deterministic rotation."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"
pkg = types.ModuleType("_category_test")
pkg.__path__ = [str(ROOT)]
with patch.dict(sys.modules, {"_category_test": pkg}):
    spec = importlib.util.spec_from_file_location("_category_test.home_personalization", ROOT / "home_personalization.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

class GeneralCategoriesTests(unittest.TestCase):
    def test_all_always_first_and_six_distinct_real_categories(self):
        for day in range(200):
            rows = mod.build_home_chips(day=day)
            self.assertEqual(rows[0]["id"], "category:0")
            self.assertEqual(rows[0]["label"], "All")
            self.assertEqual(len(rows), 7)
            self.assertEqual(len({r["id"] for r in rows}), 7)
            self.assertTrue(all(r["kind"] == "general" for r in rows[1:]))
    def test_daily_rotation_is_deterministic_and_varies(self):
        self.assertEqual(mod.build_home_chips(day=1), mod.build_home_chips(day=1))
        self.assertNotEqual(mod.build_home_chips(day=1), mod.build_home_chips(day=2))
    def test_subscriptions_and_auth_cannot_invent_home_topics(self):
        self.assertEqual(mod.build_home_chips(day=4), mod.build_home_chips(
            day=4, authenticated=True, channels=[{"title": "Autá Stavba Dielňa"}]))
    def test_invalid_video_ids_and_duplicates_rejected(self):
        data=[{"video_id": "abcdefghijk"}, {"video_id": "bad"},
              {"video_id": "abcdefghijk"}, {"video_id": "01234567890"}]
        self.assertEqual([r["video_id"] for r in mod.dedupe_videos(data)],
                         ["abcdefghijk", "01234567890"])
