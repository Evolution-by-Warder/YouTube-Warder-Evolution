"""The Home rail must show real YouTube labels, never keyword guesses."""
import importlib.util
from pathlib import Path
import unittest

PATH = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube/home_personalization.py")
spec = importlib.util.spec_from_file_location("warder_home_personalization_test", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class DynamicChipsTests(unittest.TestCase):
    def test_fallback_is_honest_regional_chart_not_fake_personalization(self):
        self.assertEqual(mod.build_home_chips(), [
            {"id": "all", "kind": "all", "label": "Populárne SK",
             "title": "Populárne na Slovensku"}])

    def test_only_exact_live_labels_and_order_from_youtube(self):
        rows = [
            {"id": "yt:a", "kind": "live", "label": "Všetko",
             "title": "Všetko", "selected": True},
            {"id": "yt:b", "kind": "live", "label": "Hudba",
             "continuation": "serverToken"},
            {"id": "yt:c", "kind": "live", "label": "Mixy",
             "continuation": "serverToken2"},
            {"id": "yt:d", "kind": "live", "label": "Domáci majstri",
             "params": "serverParams"},
        ]
        actual = mod.build_home_chips(rows, authenticated=True)
        self.assertEqual([chip["label"] for chip in actual],
                         ["Všetko", "Hudba", "Mixy", "Domáci majstri"])
        self.assertEqual(actual[1]["continuation"], "serverToken")
        self.assertEqual(actual[0]["selected"], True)

    def test_subscribed_channel_names_cannot_generate_topics(self):
        self.assertEqual(mod.build_home_chips(
            authenticated=True, channels=[
                {"channel_id": "UC" + "a" * 22, "title": "Stavba Dielňa Autá"}]),
            mod.build_home_chips())
        self.assertEqual(mod.build_home_chips([
            {"id": "yt:a", "kind": "live", "label": "Music",
             "continuation": "ok"}], authenticated=False),
            mod.build_home_chips())

    def test_duplicate_invalid_and_unusable_server_chips_are_rejected(self):
        raw = [
            {"id": "yt:1", "kind": "live", "label": "Nature", "params": "a"},
            {"id": "yt:1", "kind": "live", "label": "Fake duplicate", "params": "b"},
            {"id": "topic:cars", "kind": "topic", "label": "Autá"},
            {"id": "yt:2", "kind": "live", "label": "No action"},
        ]
        self.assertEqual([c["label"] for c in mod.build_home_chips(raw, True)],
                         ["Nature"])

    def test_only_real_youtube_ids_in_video_grid(self):
        rows = mod.dedupe_videos([
            {"video_id": "abcdefghijk"}, {"video_id": "bad"},
            {"video_id": "abcdefghijk"}, {"video_id": "01234567890"}
        ])
        self.assertEqual([v["video_id"] for v in rows],
                         ["abcdefghijk", "01234567890"])


if __name__ == "__main__":
    unittest.main()
