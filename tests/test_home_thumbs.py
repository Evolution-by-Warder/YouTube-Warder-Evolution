"""Native Home image preview: two downloads, one decoder and stale guards."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class Widget:
    def __init__(self):
        self.visible = False
        self.image = None
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False
    def setPixmap(self, ptr):
        self.image = ptr


class FakePicload:
    def __init__(self):
        self.callbacks = []
        self.PictureData = types.SimpleNamespace(get=lambda: self.callbacks)
        self.decode_paths = []
        self.para = None
    def setPara(self, para):
        self.para = para
    def startDecode(self, path):
        self.decode_paths.append(path)
        return 0
    def getData(self):
        return "native ePixmap pointer"


class FakeDeferred:
    def addCallbacks(self, success, failure):
        self.success, self.failure = success, failure


def load():
    package = types.ModuleType("_home_thumbs_test")
    package.__path__ = [str(ROOT)]
    requests = []
    decoder = FakePicload()
    def worker(*args):
        d = FakeDeferred()
        requests.append((args, d))
        return d
    fake_modules = {
        "_home_thumbs_test": package,
        "_home_thumbs_test.thumbnails": types.SimpleNamespace(
            fetch_thumbnail=lambda url: url, cleanup_cache=lambda: None),
        "enigma": types.SimpleNamespace(ePicLoad=lambda: decoder),
        "twisted": types.ModuleType("twisted"),
        "twisted.internet": types.ModuleType("twisted.internet"),
        "twisted.internet.threads": types.SimpleNamespace(deferToThread=worker),
    }
    fake_modules["twisted"].__path__ = []
    fake_modules["twisted.internet"].__path__ = []
    spec = importlib.util.spec_from_file_location(
        "_home_thumbs_test.home_thumbs", ROOT / "home_thumbs.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake_modules):
        spec.loader.exec_module(module)
    screen = {"preview_thumb%d" % i: Widget() for i in range(6)}
    return module.HomeThumbs(screen), screen, requests, decoder


def items(count=6):
    return [{"thumbnail_url": "https://i.ytimg.com/vi/abcdefghij%d/mqdefault.jpg" % i}
            for i in range(count)]


class PreviewThumbTests(unittest.TestCase):
    def test_native_decoder_fills_owner_approved_tile(self):
        """Square/4:3 inputs must not produce bars beside video artwork."""
        thumbs, screen, jobs, decoder = load()
        self.assertEqual(thumbs.decode_parameters()[:4], (473, 248, 0, 0))
        thumbs.start()
        self.assertEqual(decoder.para[:4], (473, 248, 0, 0))
        self.assertEqual(decoder.para[4], False)
        thumbs.show(items(1))
        self.assertEqual(len(jobs), 1)

    def test_no_more_than_two_downloads_for_six_visible_tiles(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        thumbs.show(items(6))
        self.assertEqual(len(jobs), 2)
        self.assertEqual(len(thumbs.queue), 4)
        self.assertEqual(thumbs.active, 2)
        jobs[0][1].success("/tmp/img0.jpg")
        self.assertEqual(len(jobs), 3)
        self.assertEqual(decoder.decode_paths, ["/tmp/img0.jpg"])
        for callback in decoder.callbacks[:]:
            callback()
        self.assertTrue(screen["preview_thumb0"].visible)

    def test_return_from_context_menu_restores_cached_native_pixmap(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        selection = items(1)
        thumbs.show(selection)
        jobs[0][1].success("/tmp/img.jpg")
        for callback in decoder.callbacks[:]:
            callback()
        self.assertTrue(screen["preview_thumb0"].visible)
        self.assertEqual(len(thumbs.image_cache), 1)
        thumbs.show([])  # Another Warder screen is temporarily on top.
        self.assertFalse(screen["preview_thumb0"].visible)
        thumbs.show(selection)
        self.assertTrue(screen["preview_thumb0"].visible)
        self.assertEqual(screen["preview_thumb0"].image, "native ePixmap pointer")
        self.assertEqual(len(jobs), 1)  # No duplicate network request.

    def test_stale_image_never_reappears_after_switching_section(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        thumbs.show(items(3))
        self.assertEqual(len(jobs), 2)
        thumbs.show([])
        jobs[0][1].success("/tmp/old.jpg")
        self.assertFalse(screen["preview_thumb0"].visible)
        self.assertEqual(decoder.decode_paths, [])
        self.assertEqual(thumbs.queue, [])

    def test_abandoned_decode_recovers_on_page_change_without_reopening(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        thumbs.show(items(2))
        jobs[0][1].success("/tmp/first.jpg")
        self.assertIsNotNone(thumbs.decoding)
        old_callback = decoder.callbacks[0]
        thumbs.show(items(1))  # next page while first ePicLoad never finishes
        self.assertTrue(thumbs.ready)
        self.assertIsNone(thumbs.decoding)
        self.assertEqual(len(decoder.callbacks), 1)
        self.assertIsNot(old_callback, decoder.callbacks[0])
        # Old queued PictureData does not eat the new frame.
        jobs[2][1].success("/tmp/new.jpg")
        self.assertIsNotNone(thumbs.decoding)
        old_callback()
        self.assertIsNotNone(thumbs.decoding)
        decoder.callbacks[0]()
        self.assertTrue(screen["preview_thumb0"].visible)

    def test_early_decoder_failure_can_be_retried_without_plugin_restart(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        thumbs.decoder = None
        thumbs.ready = False
        thumbs.show(items(1))
        self.assertTrue(thumbs.ready)
        self.assertIsNotNone(thumbs.decoder)
        self.assertEqual(len(jobs), 1)

    def test_close_disconnects_decoder_and_ignores_callbacks(self):
        thumbs, screen, jobs, decoder = load()
        thumbs.start()
        thumbs.show(items(1))
        self.assertEqual(len(decoder.callbacks), 1)
        thumbs.close()
        self.assertEqual(decoder.callbacks, [])
        jobs[0][1].success("/tmp/old.jpg")
        self.assertFalse(screen["preview_thumb0"].visible)


if __name__ == "__main__":
    unittest.main()
