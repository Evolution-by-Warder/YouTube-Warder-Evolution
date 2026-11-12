"""Mocked Enigma2 smoke test: six visible cards and stale network callback guards."""
import importlib.util
import sys
import types
from pathlib import Path
import unittest
from unittest.mock import patch

PKG = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class Widget:
    def __init__(self, text=""):
        self.text = text
        self.visible = True
        self.image = None

    def setText(self, text):
        self.text = text

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def setPixmap(self, image):
        self.image = image


class FakeScreen(dict):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.onLayoutFinish = []
        self.onClose = []
        self.closed_args = None

    def close(self, *args):
        self.closed_args = args
        for callback in self.onClose:
            callback()


class FakePicLoad:
    def __init__(self):
        self.callbacks = []
        self.PictureData = types.SimpleNamespace(get=lambda: self.callbacks)
        self.loaded_path = None

    def setPara(self, args):
        self.parameters = args

    def startDecode(self, path):
        self.loaded_path = path
        return 0

    def getData(self):
        return "fake native pixmap"


class FakeDeferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


class TestNativeGrid(unittest.TestCase):
    def load_grid(self, requests):
        fake_enigma = types.ModuleType("enigma")
        fake_enigma.ePicLoad = FakePicLoad

        components = types.ModuleType("Components")
        components.__path__ = []
        action = types.ModuleType("Components.ActionMap")
        action.ActionMap = lambda *args, **kwargs: Widget()
        label = types.ModuleType("Components.Label")
        label.Label = Widget
        pixmap = types.ModuleType("Components.Pixmap")
        pixmap.Pixmap = Widget

        screens = types.ModuleType("Screens")
        screens.__path__ = []
        screen = types.ModuleType("Screens.Screen")
        screen.Screen = FakeScreen

        twisted = types.ModuleType("twisted")
        twisted.__path__ = []
        internet = types.ModuleType("twisted.internet")
        internet.__path__ = []
        threads = types.ModuleType("twisted.internet.threads")

        def deferred_to_thread(*args):
            d = FakeDeferred()
            requests.append((args, d))
            return d

        threads.deferToThread = deferred_to_thread
        package = types.ModuleType("_warder_mock")
        package.__path__ = [str(PKG)]
        modules = {
            "enigma": fake_enigma,
            "Components": components,
            "Components.ActionMap": action,
            "Components.Label": label,
            "Components.Pixmap": pixmap,
            "Screens": screens,
            "Screens.Screen": screen,
            "twisted": twisted,
            "twisted.internet": internet,
            "twisted.internet.threads": threads,
            "_warder_mock": package,
        }
        spec = importlib.util.spec_from_file_location(
            "_warder_mock.grid", str(PKG / "grid.py")
        )
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(module)
            # Ensure module globals have been imported while mocks are available.
        return module

    def video(self, n):
        return {
            "title": "Video %s" % n,
            "channel": "Channel",
            "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg?x=%s" % n,
            "video_id": "abcdefghijk",
        }

    def test_visible_six_and_stale_callback_discard(self):
        jobs = []
        grid_module = self.load_grid(jobs)
        g = grid_module.WarderYouTubeGrid(None, [self.video(i) for i in range(9)], "test")
        g._layout_ready()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(g._active_downloads, 2)
        self.assertTrue(g["focus0"].visible)
        self.assertFalse(g["focus1"].visible)
        self.assertEqual(g["title0"].text, "Video 0")

        g.right()
        self.assertEqual(g.selected, 1)
        self.assertTrue(g["focus1"].visible)
        g.down()
        self.assertEqual(g.selected, 4)
        g.down()
        self.assertEqual(g.selected, 7)  # next six-card page
        self.assertEqual(g["title0"].text, "Video 6")
        self.assertFalse(g["thumb0"].visible)

        # Old-page responses cannot decode into the new page.
        jobs[0][1].success("/tmp/old-image.jpg")
        self.assertEqual(len(jobs), 3)
        self.assertIsNone(g._decoding)
        self.assertFalse(g["thumb0"].visible)
        jobs[1][1].success("/tmp/other-old-image.jpg")
        self.assertEqual(len(jobs), 4)

        # Current page starts exactly one decoder.
        jobs[2][1].success("/tmp/current-image.jpg")
        self.assertIsNotNone(g._decoding)
        self.assertFalse(g["thumb0"].visible)
        g._decode_finished()
        self.assertTrue(g["thumb0"].visible)
        self.assertEqual(g["thumb0"].image, "fake native pixmap")

        # Closing screen prohibits future image updates.
        g.go_back()
        self.assertTrue(g._closed)
        self.assertIsNone(g.closed_args[0])
        scheduled_at_close = len(jobs)
        jobs[3][1].success("/tmp/later-image.jpg")
        self.assertEqual(len(jobs), scheduled_at_close)

    def test_info_button_for_current_video(self):
        jobs = []
        mod = self.load_grid(jobs)
        selected = []
        grid = mod.WarderYouTubeGrid(
            None, [self.video(0), self.video(1)], "test",
            on_info=lambda video: selected.append(video["title"])
        )
        grid._layout_ready()
        grid.right()
        grid.show_info()
        self.assertEqual(selected, ["Video 1"])
        grid.close()
        grid.show_info()
        self.assertEqual(selected, ["Video 1"])

    def test_grid_next_page_emits_result(self):
        jobs = []
        m = self.load_grid(jobs)
        g = m.WarderYouTubeGrid(None, [self.video(0)], "test", has_next_page=True)
        g._layout_ready()
        g.next_page()
        self.assertEqual(g.closed_args, ("next",))


if __name__ == "__main__":
    unittest.main()
