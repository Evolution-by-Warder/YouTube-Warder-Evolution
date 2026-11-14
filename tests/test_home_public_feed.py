"""Anonymous YouTube website feed parsing without credentials or receiver."""
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load():
    pkg = types.ModuleType("_warder_public")
    pkg.__path__ = [str(ROOT)]
    api = types.ModuleType("_warder_public.api")
    api.SearchError = type("SearchError", (Exception,), {})
    api.VIDEO_ID = __import__("re").compile(r"^[a-zA-Z0-9_-]{11}$")
    api.MAX_RESPONSE_BYTES = 1_000_000
    with patch.dict(sys.modules, {"_warder_public": pkg, "_warder_public.api": api}):
        spec = importlib.util.spec_from_file_location(
            "_warder_public.home_feed", str(ROOT / "home_feed.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


class FakeResponse:
    def __init__(self, body):
        self.body = body
        self.closed = False

    def read(self, count):
        return self.body[:count]

    def geturl(self):
        return "https://www.youtube.com/"

    def close(self):
        self.closed = True


class PublicFeedTests(unittest.TestCase):
    def test_nested_home_video_cards_deduped_and_bounded(self):
        mod = load()
        payload = {
            "contents": [{"videoRenderer": {
                "videoId": "abcdefghijk",
                "title": {"runs": [{"text": "Public &amp; Popular"}]},
                "ownerText": {"runs": [{"text": "SK Creator"}]}
            }}, {"videoRenderer": {"videoId": "abcdefghijk", "title": {"simpleText": "Duplicate"}}},
                {"gridVideoRenderer": {
                    "videoId": "01234567890", "title": {"simpleText": "Another real video"}}},
                {"videoRenderer": {"videoId": "bad", "title": {"simpleText": "Invalid"}}}]
        }
        html = "<html><script>var ytInitialData = " + json.dumps(payload) + ";</script></html>"
        videos = mod.parse_public_home(html)
        self.assertEqual(len(videos), 2)
        self.assertEqual(videos[0]["title"], "Public & Popular")
        self.assertEqual(videos[0]["channel"], "SK Creator")
        self.assertEqual(videos[0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")

    def test_missing_data_fails_cleanly(self):
        mod = load()
        for text in ("<html></html>", "ytInitialData = {broken", "ytInitialData = {}"):
            with self.subTest(text=text):
                with self.assertRaises(mod.SearchError):
                    mod.parse_public_home(text)

    def test_real_public_request_uses_no_key_or_account(self):
        mod = load()
        payload = {"contents": [{"videoRenderer": {
            "videoId": "abcdefghijk", "title": {"simpleText": "Real card"},
            "ownerText": {"simpleText": "Channel"}
        }}]}
        web = ("ytInitialData = " + json.dumps(payload) + ";").encode()
        captured = []
        def opener(req, timeout):
            captured.append((req.full_url, timeout, req.headers))
            return FakeResponse(web)
        videos = mod.public_home_videos(opener=opener)
        self.assertEqual(len(videos), 1)
        self.assertEqual(len(captured), 1)
        self.assertIn("youtube.com", captured[0][0])
        self.assertNotIn("key=", captured[0][0].lower())
        self.assertNotIn("Authorization", captured[0][2])


if __name__ == "__main__":
    unittest.main()
