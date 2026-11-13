"""Offline regression checks for the genuine regional YouTube Home feed."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class FakeResponse:
    def __init__(self, payload):
        self.content = io.BytesIO(json.dumps(payload).encode("utf-8"))
        self.closed = False

    def read(self, size):
        return self.content.read(size)

    def close(self):
        self.closed = True


def load():
    package = types.ModuleType("_warder_feed")
    package.__path__ = [str(ROOT)]
    with patch.dict(sys.modules, {"_warder_feed": package}):
        path = ROOT / "home_feed.py"
        spec = importlib.util.spec_from_file_location("_warder_feed.home_feed", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def sample():
    return {"items": [
        {"id": "abcdefghijk",
         "snippet": {"title": "Cats &amp; Dogs", "channelTitle": "Hello &lt;World&gt;",
                     "publishedAt": "2026-11-13T09:00:00Z"}},
        {"id": "BAD", "snippet": {"title": "Should ignore"}},
        {"id": "01234567890", "snippet": {"title": "Second video", "channelTitle": "Channel"}},
    ]}


class HomeFeedTests(unittest.TestCase):
    def test_official_regional_chart_and_bounded_count(self):
        mod = load()
        requests = []
        def opener(request, timeout):
            requests.append((request.full_url, timeout))
            return FakeResponse(sample())
        videos = mod.popular_videos("private-key", opener=opener)
        self.assertEqual(len(videos), 2)
        self.assertEqual(videos[0]["title"], "Cats & Dogs")
        self.assertEqual(videos[0]["channel"], "Hello <World>")
        self.assertEqual(videos[0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")
        parsed = urlparse(requests[0][0])
        q = parse_qs(parsed.query)
        self.assertEqual(parsed.netloc, "www.googleapis.com")
        self.assertEqual(parsed.path, "/youtube/v3/videos")
        self.assertEqual(q["chart"], ["mostPopular"])
        self.assertEqual(q["regionCode"], ["SK"])
        self.assertEqual(q["part"], ["snippet"])
        self.assertEqual(q["maxResults"], ["12"])
        self.assertEqual(requests[0][1], 8)

    def test_errors_keep_key_out_of_user_message(self):
        mod = load()
        def rejected(request, timeout):
            raise HTTPError(request.full_url, 403, "Rejected", None, None)
        with self.assertRaises(mod.SearchError) as caught:
            mod.popular_videos("secret-key", opener=rejected)
        self.assertNotIn("secret-key", str(caught.exception))
        self.assertNotIn("http", str(caught.exception))

    def test_reject_missing_key_and_malformed_response(self):
        mod = load()
        with self.assertRaises(mod.SearchError):
            mod.popular_videos("")
        with self.assertRaises(mod.SearchError):
            mod.parse_popular_response({"items": None})
        with self.assertRaises(mod.SearchError):
            mod.parse_popular_response({"error": {}, "items": []})

    def test_never_uses_untrusted_thumbnail_url(self):
        mod = load()
        data = sample()
        data["items"][0]["snippet"]["thumbnails"] = {
            "medium": {"url": "http://evil.invalid/stolen.jpg"}}
        item = mod.parse_popular_response(data)[0]
        self.assertEqual(item["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")


if __name__ == "__main__":
    unittest.main()
