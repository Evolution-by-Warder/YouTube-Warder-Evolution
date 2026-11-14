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

    def test_real_channels_produce_thematic_and_channel_chips(self):
        chips = mod.build_home_chips(
            channels=[channel("a", "Music & Radio"),
                      channel("b", "Nature World"),
                      channel("c", "Games Factory")],
            authenticated=True)
        ids = [c["id"] for c in chips]
        self.assertEqual(ids[:5], [
            "all", "recent", "topic:music", "topic:gaming", "topic:nature"
        ])
        self.assertIn("channel:UC" + "a" * 22, ids)
        self.assertIn("channel:UC" + "b" * 22, ids)
        self.assertNotIn("history", ids)
        self.assertNotIn("favourites", ids)
        self.assertFalse(any("mix" in c["label"].lower() for c in chips))
        self.assertEqual(
            chips[3]["channels"], ("UC" + "c" * 22,)
        )

    def test_deduplicate_channels_ignore_invalid_id_and_bound_size(self):
        source = [channel("a", "Nature"),
                  channel("a", "Old duplicate"),
                  {"channel_id": "bad", "title": "Games"}]
        source.extend(channel(chr(98 + j), "Channel %d" % j) for j in range(12))
        chips = mod.build_home_chips(source, authenticated=True)
        channel_chips = [c for c in chips if c["kind"] == "channel"]
        self.assertEqual(len(channel_chips), 12)
        self.assertEqual(channel_chips[0]["title"], "Nature")
        self.assertEqual(len(set(c["id"] for c in chips)), len(chips))
        self.assertLessEqual(len(chips), 1 + 1 + mod.MAX_TOPIC_CHIPS + 12)

    def test_no_unsupported_topic_from_unknown_channel_name(self):
        chips = mod.build_home_chips(
            [channel("a", "ZXCV Company Limited")], authenticated=True)
        self.assertFalse(any(c["kind"] == "topic" for c in chips))
        self.assertEqual(chips[-1]["title"], "ZXCV Company Limited")

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
