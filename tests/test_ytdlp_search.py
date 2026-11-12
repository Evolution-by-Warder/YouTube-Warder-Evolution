"""Mock yt-dlp public video search without any network access."""
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

FILE = (Path(__file__).resolve().parents[1]
        / "plugin/Plugins/Extensions/WarderYouTube/search_backend.py")
spec = importlib.util.spec_from_file_location("warder_ytdlp_backend", str(FILE))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample(n):
    return {"_type": "playlist", "entries": [
        {"id": "video%06d" % i, "title": "Rock &amp; %d" % i,
         "uploader": "Station", "thumbnail": "https://i.ytimg.com/vi/video%06d/mqdefault.jpg" % i}
        for i in range(n)
    ]}


class Response:
    def __init__(self, text, code=0, stderr=""):
        self.stdout = text
        self.stderr = stderr
        self.returncode = code


class Tests(unittest.TestCase):
    def test_priority(self):
        self.assertEqual(mod.select_backend("key", True), "api")
        self.assertEqual(mod.select_backend(" ", True), "yt-dlp")
        self.assertIsNone(mod.select_backend("", False))

    def test_search_paging_and_argv(self):
        calls = []
        def runner(argv, **kw):
            calls.append((argv, kw))
            n = int(argv[-1].split(":")[0].removeprefix("ytsearch"))
            return Response(json.dumps(sample(n)))
        a = mod.search_with_ytdlp("jazz & soul", runner=runner, which=lambda _: "/usr/bin/yt-dlp")
        b = mod.search_with_ytdlp("jazz & soul", "yd:15", runner=runner, which=lambda _: "/usr/bin/yt-dlp")
        self.assertEqual(len(a["items"]), 15)
        self.assertEqual(a["next_page_token"], "yd:15")
        self.assertEqual(b["items"][0]["title"], "Rock & 15")
        self.assertEqual(b["next_page_token"], "yd:30")
        self.assertEqual(calls[0][0][-2:], ["--", "ytsearch15:jazz & soul"])
        self.assertIn("--flat-playlist", calls[0][0])
        self.assertIn("--dump-single-json", calls[0][0])
        self.assertEqual(calls[0][1]["timeout"], mod.TIMEOUT)
        self.assertNotIn("shell", calls[0][1])

    def test_max_page_and_invalid_values(self):
        c = mod.parse_flat_results(sample(60), 45)
        self.assertEqual(len(c["items"]), 15)
        self.assertEqual(c["next_page_token"], "")
        with self.assertRaises(mod.SearchBackendError):
            mod.parse_flat_results(sample(61))
        for bad in ("15", "yd:0", "yd:60", "yd:030", "yd:-1", "bogus"):
            with self.subTest(token=bad):
                with self.assertRaises(mod.SearchBackendError):
                    mod.page_offset(bad)
        for bad in ("", "x" * 161, "line\nbreak", None):
            with self.subTest(query=bad):
                with self.assertRaises(mod.SearchBackendError):
                    mod.search_with_ytdlp(bad, which=lambda _: "/usr/bin/yt-dlp")

    def test_flat_webp_thumbnail_uses_supported_jpeg(self):
        video = "abcdefghijk"
        webp = "https://i.ytimg.com/vi_webp/%s/hqdefault.webp" % video
        self.assertEqual(mod.image_url(webp, video),
            "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")

    def test_safe_image_and_video_ids(self):
        d = sample(2)
        d["entries"][0]["id"] = "invalid"
        d["entries"][1]["thumbnail"] = "https://i.ytimg.com.evil.com/internal"
        items = mod.parse_flat_results(d)["items"]
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/video000001/mqdefault.jpg")

    def test_timeout_and_error_without_sensitive_stderr(self):
        def timeout(argv, **kw):
            raise subprocess.TimeoutExpired(argv, kw["timeout"])
        with self.assertRaisesRegex(mod.SearchBackendError, "timed out"):
            mod.search_with_ytdlp("test", runner=timeout, which=lambda _: "/usr/bin/yt-dlp")
        with self.assertRaises(mod.SearchBackendError) as raised:
            mod.search_with_ytdlp("test", which=lambda _: "/usr/bin/yt-dlp",
                runner=lambda argv, **kw: Response("", 1, "SIGNED_SECRET"))
        self.assertNotIn("SIGNED_SECRET", str(raised.exception))
        with self.assertRaisesRegex(mod.SearchBackendError, "not available"):
            mod.search_with_ytdlp("test", which=lambda _: None)


if __name__ == "__main__":
    unittest.main()
