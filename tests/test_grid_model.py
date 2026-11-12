"""Pure navigation and cache tests run without Enigma2."""
import importlib.util
import io
import pathlib
import tempfile
import unittest

PKG = pathlib.Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load(name):
    spec = importlib.util.spec_from_file_location("yt_" + name, str(PKG / (name + ".py")))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


grid = load("grid_model")
thumb = load("thumbnails")
URL = "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg"
JPEG = b"\xff\xd8\xff\xe0sample"


class Response:
    def __init__(self, url, data):
        self.url = url
        self.data = io.BytesIO(data)

    def geturl(self):
        return self.url

    def read(self, count):
        return self.data.read(count)

    def close(self):
        pass


class GridTests(unittest.TestCase):
    def test_focus(self):
        self.assertEqual(grid.VISIBLE_TILES, 6)
        self.assertEqual(grid.move_index(4, "down", 15), 7)
        self.assertEqual(grid.move_index(0, "left", 15), 0)
        self.assertEqual(grid.move_index(14, "right", 15), 14)
        self.assertEqual(grid.move_index(2, "right", 3), 2)
        self.assertEqual(grid.move_index(0, "up", 0), -1)
        self.assertEqual(grid.page_number(8), 1)
        self.assertEqual(grid.local_slot(8), 2)
        self.assertEqual(grid.visible_slice(list(range(15)), 8), list(range(6, 12)))

    def test_block_unsafe_hosts(self):
        self.assertEqual(thumb.validate_thumbnail_url(URL), URL)
        for url in ("http://i.ytimg.com/vi/foo/default.jpg",
                    "https://evil.example/vi/foo/default.jpg",
                    "https://i.ytimg.com.evil.example/vi/foo/default.jpg",
                    "https://i.ytimg.com:8080/vi/foo/default.jpg",
                    "https://secret@i.ytimg.com/vi/foo/default.jpg",
                    "file:///etc/passwd", None):
            with self.subTest(url=url):
                with self.assertRaises(thumb.ThumbnailError):
                    thumb.validate_thumbnail_url(url)

    def test_cache_and_redirect(self):
        calls = []
        def opener(req, timeout):
            calls.append(req.full_url)
            return Response(req.full_url, JPEG)
        with tempfile.TemporaryDirectory() as cache:
            p1 = thumb.fetch_thumbnail(URL, opener=opener, cache_dir=cache)
            p2 = thumb.fetch_thumbnail(URL, opener=opener, cache_dir=cache)
            self.assertEqual(p1, p2)
            self.assertEqual(len(calls), 1)
            self.assertEqual(pathlib.Path(p1).read_bytes(), JPEG)
        with tempfile.TemporaryDirectory() as cache:
            with self.assertRaises(thumb.ThumbnailError):
                thumb.fetch_thumbnail(URL, cache_dir=cache,
                    opener=lambda req, timeout: Response("https://evil.example/file", JPEG))

    def test_invalid_and_oversize_bytes(self):
        for data in (b"<html>not image", b"x" * (thumb.MAX_BYTES_PER_IMAGE + 1)):
            with tempfile.TemporaryDirectory() as cache:
                with self.assertRaises(thumb.ThumbnailError):
                    thumb.fetch_thumbnail(URL, cache_dir=cache,
                        opener=lambda req, timeout: Response(URL, data))


if __name__ == "__main__":
    unittest.main()
