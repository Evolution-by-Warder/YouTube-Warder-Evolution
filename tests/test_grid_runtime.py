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


class FakeConnection:
    def __init__(self, callbacks, callback):
        self.callbacks = callbacks
        self.callback = callback
        self.disconnected = False

    def disconnect(self):
        if not self.disconnected:
            self.disconnected = True
            self.callbacks.remove(self.callback)


class FakeModernSignal:
    def __init__(self, callbacks):
        self.callbacks = callbacks

    def connect(self, callback):
        self.callbacks.append(callback)
        return FakeConnection(self.callbacks, callback)


class FakeDeferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


class TestNativeGrid(unittest.TestCase):
    def load_grid(self, requests, framebuffer=(1, 1), signal_style="get"):
        fake_enigma = types.ModuleType("enigma")
        def decoder_factory():
            decoder = FakePicLoad()
            if signal_style == "connect":
                decoder.PictureData = FakeModernSignal(decoder.callbacks)
            return decoder
        fake_enigma.ePicLoad = decoder_factory

        components = types.ModuleType("Components")
        avswitch = types.ModuleType("Components.AVSwitch")
        avswitch.AVSwitch = lambda: types.SimpleNamespace(getFramebufferScale=lambda: framebuffer)
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
            "Components.AVSwitch": avswitch,
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
        module._test_avswitch = avswitch
        return module

    def video(self, n):
        return {
            "title": "Video %s" % n,
            "channel": "Channel",
            "thumbnail_url": "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg?x=%s" % n,
            "video_id": "abcdefghijk",
        }

    def test_screen_items_method_remains_callable_on_openatv76(self):
        # Screen.deleteGUIScreen relies on the dict.items() method.
        mod = self.load_grid([])
        grid = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        self.assertTrue(callable(grid.items))
        self.assertIn("brand", dict(grid.items()))
        self.assertEqual(len(grid.video_items), 1)
        grid.close()
        self.assertTrue(callable(grid.items))

    def test_thumbnail_decode_uses_framebuffer_scale(self):
        jobs = []
        mod = self.load_grid(jobs, framebuffer=(4, 3))
        g = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        with patch.dict(sys.modules, {"Components.AVSwitch": mod._test_avswitch}):
            g._layout_ready()
        self.assertEqual(g._picload.parameters[:4], (476, 249, 4, 3))
        self.assertTrue(callable(g.items))

    def test_invalid_framebuffer_scale_falls_back_safely(self):
        jobs = []
        mod = self.load_grid(jobs, framebuffer=(0, -1))
        g = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        with patch.dict(sys.modules, {"Components.AVSwitch": mod._test_avswitch}):
            g._layout_ready()
        self.assertEqual(g._picload.parameters[:4], (476, 249, 1, 1))

    def test_modern_signal_connect_and_disconnect(self):
        jobs = []
        mod = self.load_grid(jobs, signal_style="connect")
        grid = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        grid._layout_ready()
        self.assertEqual(len(grid._picload.callbacks), 1)
        self.assertIsNotNone(grid._picload_connection)
        decoder = grid._picload
        jobs[0][1].success("/tmp/modern.jpg")
        decoder.callbacks[0]()
        self.assertEqual(grid["thumb0"].image, "fake native pixmap")
        grid.close()
        self.assertEqual(decoder.callbacks, [])
        self.assertIsNone(grid._picload)

    def test_original_native_pixmap_pointer_is_not_dereferenced(self):
        jobs = []
        mod = self.load_grid(jobs)
        grid = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        grid._layout_ready()
        class NativePointer:
            def __deref__(self):
                raise AssertionError("Native ePtr must not be dereferenced")
        ptr = NativePointer()
        grid._picload.getData = lambda: ptr
        jobs[0][1].success("/tmp/native.jpg")
        grid._decode_finished()
        self.assertIs(grid["thumb0"].image, ptr)

    def test_decoder_read_error_fails_softly(self):
        jobs = []
        mod = self.load_grid(jobs)
        grid = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        grid._layout_ready()
        def bad_data():
            raise RuntimeError("Decoder detached")
        grid._picload.getData = bad_data
        jobs[0][1].success("/tmp/bad.jpg")
        grid._decode_finished()
        self.assertTrue(any(text in grid["status"].text for text in
                            ("Náhľady sa nepodarilo", "Thumbnails could not be loaded")))

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
        self.assertEqual(g.closed_args[0], "home")
        scheduled_at_close = len(jobs)
        jobs[3][1].success("/tmp/later-image.jpg")
        self.assertEqual(len(jobs), scheduled_at_close)

    def test_menu_key_toggles_favourite_callback_without_touching_playback(self):
        jobs = []
        mod = self.load_grid(jobs)
        toggled = []
        g = mod.WarderYouTubeGrid(None, [self.video(0), self.video(1)], "test",
            on_favorite=lambda video: toggled.append(video["title"]))
        g._layout_ready()
        g.save_favourite()
        g.right()
        g.save_favourite()
        self.assertEqual(toggled, ["Video 0", "Video 1"])
        g.close()
        g.save_favourite()
        self.assertEqual(len(toggled), 2)

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

    def test_failed_thumbnails_show_safe_status(self):
        jobs = []
        mod = self.load_grid(jobs)
        grid = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        grid._layout_ready()
        self.assertEqual(len(jobs), 1)
        jobs[0][1].failure(Exception("Network failure with secrets"))
        self.assertIn("Náhľady sa nepodarilo", grid["status"].text)
        self.assertNotIn("secrets", grid["status"].text)

    def test_late_thumbnail_failure_does_not_override_video_status(self):
        jobs = []
        mod = self.load_grid(jobs)
        g = mod.WarderYouTubeGrid(None, [self.video(0)], "test",
            on_play=lambda video: None)
        g._layout_ready()
        g.play()
        self.assertIn("Zisťujem", g["status"].text)
        jobs[0][1].failure(Exception("https://private.example/?sig=secret"))
        self.assertIn("Zisťujem", g["status"].text)
        self.assertNotIn("secret", g["status"].text)

    def test_partial_thumbnail_failures_show_safe_counts(self):
        jobs = []
        mod = self.load_grid(jobs)
        g = mod.WarderYouTubeGrid(None, [self.video(0), self.video(1)], "test")
        g._layout_ready()
        jobs[0][1].failure(Exception("private token"))
        jobs[1][1].success("/tmp/good.jpg")
        g._decode_finished()
        self.assertTrue(any(text in g["status"].text for text in
                            ("Náhľady 1/2", "Thumbnails 1/2")))
        self.assertTrue(any(text in g["status"].text for text in ("sieť: 1", "network: 1")))
        self.assertNotIn("private", g["status"].text)

    def test_download_error_distinguishes_decoder_failure(self):
        jobs = []
        mod = self.load_grid(jobs)
        g = mod.WarderYouTubeGrid(None, [self.video(0)], "test")
        g._layout_ready()
        jobs[0][1].success("/tmp/malformed.jpg")
        g._picload.getData = lambda: None
        g._decode_finished()
        self.assertTrue(any(text in g["status"].text for text in ("dekodér: 1", "decoder: 1")))
        self.assertTrue(any(text in g["status"].text for text in ("sieť: 0", "network: 0")))

    def test_stale_network_worker_does_not_block_new_page_diagnostics(self):
        jobs = []
        mod = self.load_grid(jobs)
        g = mod.WarderYouTubeGrid(None, [self.video(i) for i in range(7)], "test")
        g._layout_ready()
        self.assertEqual(len(jobs), 2)
        g.next_page()
        self.assertEqual(g.selected, 6)
        self.assertEqual(len(jobs), 2)  # Two old workers still running.
        jobs[0][1].failure(Exception("old failure"))
        self.assertEqual(len(jobs), 3)
        jobs[2][1].failure(Exception("new failure"))
        self.assertIn("sieť: 1", g["status"].text)
        self.assertEqual(g._thumb_network_failures, 1)
        self.assertEqual(g._active_downloads, 1)  # Old worker remains counted.
        previous = g["status"].text
        jobs[1][1].failure(Exception("old failure"))
        self.assertEqual(g["status"].text, previous)
        self.assertEqual(g._active_downloads, 0)

    def test_stale_decode_is_discarded_after_page_switch(self):
        jobs = []
        mod = self.load_grid(jobs)
        g = mod.WarderYouTubeGrid(None, [self.video(i) for i in range(7)], "test")
        g._layout_ready()
        jobs[0][1].success("/tmp/old.jpg")
        self.assertIsNotNone(g._decoding)
        g.next_page()
        jobs[1][1].failure(Exception("old page"))
        new_jobs = [job for job in jobs[2:] if job[0][1].endswith("?x=6")]
        self.assertTrue(new_jobs)
        new_jobs[0][1].success("/tmp/new.jpg")
        self.assertFalse(g["thumb0"].visible)
        self.assertEqual(g._decoding[0], 1)  # First page still decoding.
        g._decode_finished()  # Old callback must not display in new page.
        self.assertFalse(g["thumb0"].visible)
        self.assertEqual(g._decoding[0], 2)
        g._decode_finished()
        self.assertTrue(g["thumb0"].visible)
        self.assertEqual(g._thumb_shown, 1)

    def test_grid_next_page_emits_result(self):
        jobs = []
        m = self.load_grid(jobs)
        g = m.WarderYouTubeGrid(None, [self.video(0)], "test", has_next_page=True)
        g._layout_ready()
        g.next_page()
        self.assertEqual(g.closed_args, ("next",))


if __name__ == "__main__":
    unittest.main()
