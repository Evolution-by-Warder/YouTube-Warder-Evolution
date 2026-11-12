"""Regression test for the GigaBlue Quad 4K Pro / OpenATV 8.1 Search crash.

Repro log: 2026-11-12 17:16:28, Search.first_open from onLayoutFinish:
  RuntimeError: Modal open are allowed only from a screen which is modal!

Mock the essential Enigma2 Session lifecycle: layout before in_exec; shown
only after entering modal exec. Returning from keyboard must not reopen it.
No physical Enigma2 receiver is required for this test.
"""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

SEARCH = (
    Path(__file__).resolve().parents[1]
    / "plugin/Plugins/Extensions/WarderYouTube/search.py"
)


class FakeWidget:
    def __init__(self, text=""):
        self.text = text
        self.onSelectionChanged = []

    def setText(self, value):
        self.text = value

    def setList(self, value):
        self.data = value

    def getCurrentIndex(self):
        return 0


class FakeScreen(dict):
    def __init__(self, session):
        self.session = session
        self.onLayoutFinish = []
        self.onShown = []
        self.onClose = []

    def close(self, *args):
        for callback in self.onClose:
            callback()


class FakeSession:
    def __init__(self):
        self.in_exec = False
        self.modal_calls = []
        self.current_dialog = None

    def openWithCallback(self, callback, screen, **kwargs):
        if not self.in_exec:
            raise RuntimeError(
                "[StartEnigma] Error: Modal open are allowed only from a screen which is modal!"
            )
        self.modal_calls.append((callback, screen, kwargs))
        return "virtual-keyboard-dialog"


def module(name, **attrs):
    obj = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(obj, key, value)
    return obj


def load_search(api_key="configured-key", have_ytdlp=False):
    fake_keyboard = type("VirtualKeyboard", (), {})
    fake_settings = type("WarderYouTubeSettings", (), {})
    fake_message_box = type("MessageBox", (), {"TYPE_INFO": 1})
    fake_map = lambda *args, **kwargs: object()

    def selection(key, installed):
        return "api" if key else ("yt-dlp" if installed else None)

    def no_network(*args, **kwargs):
        raise AssertionError("No worker network calls allowed in this test")

    fake_modules = {
        "Components": module("Components"),
        "Components.ActionMap": module("Components.ActionMap", ActionMap=fake_map),
        "Components.Label": module("Components.Label", Label=FakeWidget),
        "Components.MenuList": module("Components.MenuList", MenuList=FakeWidget),
        "Screens": module("Screens"),
        "Screens.MessageBox": module("Screens.MessageBox", MessageBox=fake_message_box),
        "Screens.Screen": module("Screens.Screen", Screen=FakeScreen),
        "Screens.VirtualKeyBoard": module("Screens.VirtualKeyBoard", VirtualKeyboard=fake_keyboard),
        "twisted": module("twisted"),
        "twisted.internet": module("twisted.internet"),
        "twisted.internet.threads": module("twisted.internet.threads", deferToThread=no_network),
        "_warder_modal": module("_warder_modal"),
        "_warder_modal.api": module("_warder_modal.api", SearchError=Exception, search_videos=no_network),
        "_warder_modal.search_backend": module(
            "_warder_modal.search_backend",
            SearchBackendError=Exception, search_with_ytdlp=no_network, select_backend=selection
        ),
        "_warder_modal.resolver": module(
            "_warder_modal.resolver", ResolverError=Exception,
            is_available=lambda: have_ytdlp, resolve_video_streams=no_network
        ),
        "_warder_modal.settings": module(
            "_warder_modal.settings", WarderYouTubeSettings=fake_settings,
            get_api_key=lambda: api_key, get_quality=lambda: "720"
        ),
        "_warder_modal.video_metadata": module(
            "_warder_modal.video_metadata", VideoInfoError=Exception, fetch_video_info=no_network
        ),
        "_warder_modal.skin": module("_warder_modal.skin", SEARCH_SKIN="<screen/>"),
    }
    fake_modules["_warder_modal"].__path__ = [str(SEARCH.parent)]
    fake_modules["Components"].__path__ = []
    fake_modules["Screens"].__path__ = []
    fake_modules["twisted"].__path__ = []
    fake_modules["twisted.internet"].__path__ = []
    spec = importlib.util.spec_from_file_location("_warder_modal.search", str(SEARCH))
    result = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake_modules):
        spec.loader.exec_module(result)
    return result


class SearchModalRegressionTests(unittest.TestCase):
    def test_screen_items_method_remains_callable_on_openatv76(self):
        # OpenATV 7.6 Screen.deleteGUIScreen calls list(self.items()).
        source = load_search(api_key="", have_ytdlp=False)
        screen = source.WarderYouTubeSearch(FakeSession())
        self.assertTrue(callable(screen.items))
        self.assertIn("results", dict(screen.items()))
        self.assertEqual(screen.video_items, [])

    def test_playback_failure_and_normal_exit_have_distinct_status(self):
        source = load_search(api_key="", have_ytdlp=False)
        screen = source.WarderYouTubeSearch(FakeSession())
        screen.playback_finished(True)
        self.assertIn("nepodarilo prehrať", screen["status"].text)
        screen.playback_finished(False)
        self.assertIn("Prehrávanie ukončené", screen["status"].text)
        screen.mark_closed()
        screen.playback_finished(True)
        self.assertIn("Prehrávanie ukončené", screen["status"].text)

    def test_keyboard_is_never_opened_during_layout(self):
        source = load_search()
        session = FakeSession()
        screen = source.WarderYouTubeSearch(session)
        session.current_dialog = screen

        # Enigma2 calls onLayoutFinish from applySkin while session.in_exec=False.
        for callback in screen.onLayoutFinish:
            callback()
        self.assertEqual(session.modal_calls, [])
        self.assertFalse(screen._did_initial_prompt)

        # Session.execBegin sets in_exec=True, then calls onShown.
        session.in_exec = True
        for callback in screen.onShown:
            callback()
        self.assertEqual(len(session.modal_calls), 1)
        self.assertEqual(session.modal_calls[0][2]["title"], "Search YouTube videos")

        # onShown may fire again when returning from VirtualKeyboard/MoviePlayer.
        for callback in screen.onShown:
            callback()
        self.assertEqual(len(session.modal_calls), 1)

        for callback in screen.onClose:
            callback()
        for callback in screen.onShown:
            callback()
        self.assertEqual(len(session.modal_calls), 1)

    def test_no_backend_shows_status_without_modal(self):
        source = load_search(api_key="", have_ytdlp=False)
        session = FakeSession()
        screen = source.WarderYouTubeSearch(session)
        for callback in screen.onLayoutFinish:
            callback()
        self.assertEqual(session.modal_calls, [])

        session.in_exec = True
        for callback in screen.onShown:
            callback()
        self.assertEqual(session.modal_calls, [])
        self.assertIn("Search needs", screen["status"].text)

    def test_installed_ytdlp_without_api_key_still_opens_once(self):
        source = load_search(api_key="", have_ytdlp=True)
        session = FakeSession()
        screen = source.WarderYouTubeSearch(session)
        for callback in screen.onLayoutFinish:
            callback()
        session.in_exec = True
        for callback in screen.onShown:
            callback()
        self.assertEqual(len(session.modal_calls), 1)


if __name__ == "__main__":
    unittest.main()
