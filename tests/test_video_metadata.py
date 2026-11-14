"""Host tests for on-demand YouTube video metadata. No live API usage."""
import importlib.util
import io
import json
from pathlib import Path
import unittest
import sys
import types
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

FILE = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube/video_metadata.py")
package = types.ModuleType("_test_meta52")
package.__path__ = [str(FILE.parent)]
sys.modules["_test_meta52"] = package
spec = importlib.util.spec_from_file_location("_test_meta52.video_metadata", str(FILE))
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)


class Reply:
    def __init__(self, payload):
        self.io = io.BytesIO(payload)

    def read(self, n):
        return self.io.read(n)

    def close(self):
        pass


def payload(id="abcdefghijk"):
    return {"items": [{
        "id": id,
        "snippet": {"title": "Hello &amp; world",
                    "channelTitle": "My &lt;Channel&gt;",
                    "description": "Short description",
                    "publishedAt": "2026-11-12T12:00:00Z"},
        "contentDetails": {"duration": "PT1H2M3S"},
        "statistics": {"viewCount": "1234567"}
    }]}


class MetadataTests(unittest.TestCase):
    def test_duration_formatter(self):
        self.assertEqual(metadata.display_duration("PT2M3S"), "2:03")
        self.assertEqual(metadata.display_duration("PT15S"), "0:15")
        self.assertEqual(metadata.display_duration("PT1H2M3S"), "1:02:03")
        self.assertEqual(metadata.display_duration("P1DT5S"), "24:00:05")
        self.assertEqual(metadata.display_duration("PT0S"), "0:00")
        for bad in ("", "P", "P1W", "nonsense", None):
            with self.subTest(input=bad):
                self.assertEqual(metadata.display_duration(bad), "Neznáma")

    def test_parsed_data(self):
        data = metadata.parse_video_info(payload(), "abcdefghijk")
        self.assertEqual(data["duration"], "1:02:03")
        self.assertEqual(data["views"], "1 234 567")
        self.assertEqual(data["title"], "Hello & world")
        self.assertEqual(data["channel"], "My <Channel>")
        self.assertEqual(data["description"], "Short description")

    def test_missing_and_invalid_data(self):
        with self.assertRaises(metadata.VideoInfoError):
            metadata.parse_video_info({}, "abcdefghijk")
        with self.assertRaises(metadata.VideoInfoError):
            metadata.parse_video_info(payload(), "abcdefghijl")
        for data in ({"items": [{"id": "abcdefghijk", "snippet": "bad"}]},):
            with self.assertRaises(metadata.VideoInfoError):
                metadata.parse_video_info(data, "abcdefghijk")

    def test_official_request(self):
        captured = []
        def opener(request, timeout):
            captured.append((request.full_url, timeout))
            return Reply(json.dumps(payload()).encode("utf-8"))
        data = metadata.fetch_video_info("abcdefghijk", "test-key", opener=opener)
        self.assertEqual(data["video_id"], "abcdefghijk")
        url, timeout = captured[0]
        self.assertEqual(urlparse(url).hostname, "www.googleapis.com")
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["part"], ["snippet,contentDetails,statistics"])
        self.assertEqual(params["id"], ["abcdefghijk"])
        self.assertEqual(params["key"], ["test-key"])
        self.assertEqual(timeout, 8)

    def test_secret_not_in_error(self):
        secret = "private-super-key"
        def opener(request, timeout):
            raise HTTPError(request.full_url, 403, "denied", None, None)
        with self.assertRaises(metadata.VideoInfoError) as captured:
            metadata.fetch_video_info("abcdefghijk", secret, opener=opener)
        self.assertNotIn(secret, str(captured.exception))
        self.assertNotIn("https://", str(captured.exception))

    def test_key_and_id_validation(self):
        for bad in ("bad", "too-long-video-id", "ab/cdefghij", None):
            with self.assertRaises(metadata.VideoInfoError):
                metadata.fetch_video_info(bad, "key", opener=lambda *a, **k: None)
        with self.assertRaises(metadata.VideoInfoError):
            metadata.fetch_video_info("abcdefghijk", "")

    def test_oversize(self):
        def opener(*args, **kwargs):
            return Reply(b"x" * (metadata.MAX_RESPONSE_BYTES + 1))
        with self.assertRaises(metadata.VideoInfoError):
            metadata.fetch_video_info("abcdefghijk", "key", opener=opener)


if __name__ == "__main__":
    unittest.main()
