"""Tests for public YouTube search JSON without network or Enigma2 imports."""
import importlib.util
import io
import json
from pathlib import Path
import unittest
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

API = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/api.py"
spec = importlib.util.spec_from_file_location("warderyoutube_api", str(API))
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


def sample(video_id="abcdefghijk"):
    return {
        "items": [
            {"id": {"kind": "youtube#video", "videoId": video_id},
             "snippet": {
                 "title": "Cats &amp; Dogs",
                 "channelTitle": "My &lt;Channel&gt;",
                 "publishedAt": "2026-11-12T12:00:00Z",
                 "thumbnails": {"medium": {"url": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id}}
             }}
        ],
        "nextPageToken": "NEXT"
    }


class FakeResponse:
    def __init__(self, data):
        self.data = io.BytesIO(data)
        self.closed = False

    def read(self, count):
        return self.data.read(count)

    def close(self):
        self.closed = True


class ApiTests(unittest.TestCase):
    def test_parse_valid_and_unescape(self):
        data = api.parse_search_response(sample())
        self.assertEqual(data["next_page_token"], "NEXT")
        self.assertEqual(data["items"][0]["video_id"], "abcdefghijk")
        self.assertEqual(data["items"][0]["title"], "Cats & Dogs")
        self.assertEqual(data["items"][0]["channel"], "My <Channel>")

    def test_skip_bad_ids_and_unsafe_thumbnail(self):
        raw = sample("not a valid ID")
        self.assertEqual(api.parse_search_response(raw)["items"], [])
        raw = sample()
        raw["items"][0]["snippet"]["thumbnails"]["medium"]["url"] = "http://evil.example/test"
        self.assertEqual(api.parse_search_response(raw)["items"][0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")

    def test_api_uses_canonical_jpeg_when_thumbnail_missing_or_webp(self):
        for thumbnail in (None, {}, {"medium": {"url": "https://i.ytimg.com/vi_webp/abcdefghijk/hqdefault.webp"}}):
            with self.subTest(thumbnail=thumbnail):
                raw = sample()
                if thumbnail is None:
                    raw["items"][0]["snippet"].pop("thumbnails")
                else:
                    raw["items"][0]["snippet"]["thumbnails"] = thumbnail
                video = api.parse_search_response(raw)["items"][0]
                self.assertEqual(video["thumbnail_url"],
                                 "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")

    def test_missing_items_is_error(self):
        with self.assertRaises(api.SearchError):
            api.parse_search_response({})

    def test_search_builds_encoded_official_request(self):
        captured = []
        def opener(request, timeout):
            captured.append((request.full_url, timeout))
            return FakeResponse(json.dumps(sample()).encode("utf-8"))
        got = api.search_videos("Música & tech", "my-test-KEY", "TOKEN", opener=opener)
        self.assertEqual(len(got["items"]), 1)
        url, timeout = captured[0]
        self.assertEqual(urlparse(url).netloc, "www.googleapis.com")
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["q"], ["Música & tech"])
        self.assertEqual(params["part"], ["snippet"])
        self.assertEqual(params["type"], ["video"])
        self.assertEqual(params["pageToken"], ["TOKEN"])
        self.assertEqual(params["key"], ["my-test-KEY"])
        self.assertEqual(timeout, 8)

    def test_error_messages_never_expose_api_key(self):
        key = "super-private-key"
        def opener(request, timeout):
            raise HTTPError(request.full_url, 403, "denied", None, None)
        with self.assertRaises(api.SearchError) as raised:
            api.search_videos("test", key, opener=opener)
        self.assertNotIn(key, str(raised.exception))
        self.assertNotIn("https://", str(raised.exception))

    def test_oversized_body(self):
        def opener(request, timeout):
            return FakeResponse(b"x" * (api.MAX_RESPONSE_BYTES + 1))
        with self.assertRaises(api.SearchError):
            api.search_videos("test", "key", opener=opener)

    def test_missing_key(self):
        with self.assertRaises(api.SearchError):
            api.search_videos("cat", "")

if __name__ == "__main__":
    unittest.main()
