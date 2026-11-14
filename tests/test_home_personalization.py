"""Account-derived Home chips without fake YouTube web personalization."""
import importlib.util
from pathlib import Path
import unittest

PATH = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube/home_personalization.py")
spec = importlib.util.spec_from_file_location("warder_home_personalization_test", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def channel(letter, name):
    return {"channel_id": "UC" + letter * 22, "title": name}


class DynamicChipsTests(unittest.TestCase):
    def test_unconnected_receiver_stays_safe_and_plain(self):
        self.assertEqual(
            [c["id"] for c in mod.build_home_chips()],
            ["all"]
        )

    def test_topics_appear_without_duplicate_odbery_or_channel_names(self):
        chips = mod.build_home_chips(
            channels=[channel("a", "Music & Radio"),
                      channel("b", "Nature World"),
                      channel("c", "Games Factory")],
            authenticated=True)
        ids = [c["id"] for c in chips]
        self.assertEqual(ids, [
            "all", "topic:music", "topic:gaming", "topic:nature"
        ])
        self.assertNotIn("recent", ids)
        self.assertFalse(any(item.startswith("channel:") for item in ids))
        self.assertNotIn("history", ids)
        self.assertNotIn("favourites", ids)
        self.assertFalse(any("mix" in c["label"].lower() for c in chips))
        self.assertEqual(chips[2]["channels"], ("UC" + "c" * 22,))

    def test_dedupe_channels_and_limit_real_topic_results(self):
        source = [channel("a", "Nature"),
                  channel("a", "Old duplicate"),
                  {"channel_id": "bad", "title": "Games"}]
        source.extend(channel(chr(98 + j), "Channel %d" % j) for j in range(12))
        chips = mod.build_home_chips(source, authenticated=True)
        self.assertEqual([c["id"] for c in chips], ["all", "topic:nature"])
        self.assertEqual(chips[1]["channels"], ("UC" + "a" * 22,))
        self.assertEqual(len(set(c["id"] for c in chips)), len(chips))
        self.assertLessEqual(len(chips), 1 + mod.MAX_TOPIC_CHIPS)

    def test_unknown_subscription_titles_never_create_fake_topics(self):
        chips = mod.build_home_chips(
            [channel("a", "ZXCV Company Limited")], authenticated=True)
        self.assertEqual([c["id"] for c in chips], ["all"])
        self.assertEqual(chips[0]["title"], "Populárne na Slovensku")

    def test_only_real_youtube_ids_in_video_grid(self):
        def video(value):
            return {"video_id": value, "title": value}
        rows = mod.dedupe_videos([
            video("abcdefghijk"), video("bad"), video("abcdefghijk"),
            video("01234567890"), {"junk": "data"}, None
        ])
        self.assertEqual(
            [v["video_id"] for v in rows], ["abcdefghijk", "01234567890"])


if __name__ == "__main__":
    unittest.main()
