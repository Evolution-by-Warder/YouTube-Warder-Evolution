"""Regression tests: never flash the legacy search screen before video results.

Home owns the network search. The native Grid opens only after results arrive;
its BLUE/SEARCH callback returns directly to the right-pane system keyboard.
"""
from contextlib import contextmanager
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

SOURCE = (Path(__file__).resolve().parents[1] /
          "plugin/Plugins/Extensions/WarderYouTube/home_search_flow.py")


def module(name, **attrs):
    obj = types.ModuleType(name)
    for name_, value in attrs.items():
        setattr(obj, name_, value)
    return obj


class Label:
    def __init__(self):
        self.text = ""

    def setText(self, text):
        self.text = text


class FakeInlineKeyboard:
    def __init__(self):
        self.value_text = "aladin"
        self.reset_calls = 0

    def reset(self):
        self.reset_calls += 1
        self.value_text = ""


class Grid:
    def __init__(self, callback, args):
        self.callback = callback
        self.args = args
        self.statuses = []
        self._closed = False

    def close(self, action):
        self._closed = True
        self.callback(action)

    def set_status(self, message, override=False):
        self.statuses.append((message, override))


class Session:
    def __init__(self):
        self.grids = []
        self.other_dialogs = []

    def openWithCallback(self, callback, screen, *args):
        if screen is not FakeVideoGrid:
            self.other_dialogs.append(("context", callback, screen, args))
            return None
        grid = Grid(callback, args)
        self.grids.append(grid)
        return grid

    def open(self, screen, *args, **kwargs):
        self.other_dialogs.append(("open", screen, args, kwargs))


class FakeVideoGrid:
    pass


class FakeHome(dict):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.index = 1
        self.focus_area = "keyboard"
        self._disposed = False
        self._playback_active = False
        self.page_index = 0
        self.inline_keyboard = FakeInlineKeyboard()
        self["kb_feedback"] = Label()
        self.preview_count = 0
        self.play_requests = []

    def _update_preview(self):
        self.preview_count += 1

    def _enter_keyboard_focus(self):
        self.focus_area = "keyboard"

    def _play_selected(self, video):
        self.play_requests.append(video)


class Deferred:
    def __init__(self):
        self.success = None
        self.failure = None

    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


@contextmanager
def native_search():
    jobs = []

    def worker(*args):
        d = Deferred()
        jobs.append((args, d))
        return d

    def search_api(*args):
        return []

    def search_ytdlp(*args):
        return []

    root = module("_home_direct_test")
    root.__path__ = [str(SOURCE.parent)]
    twisted = module("twisted")
    twisted.__path__ = []
    internet = module("twisted.internet")
    internet.__path__ = []
    classes = {
        "_home_direct_test": root,
        "_home_direct_test.api": module(
            "_home_direct_test.api", SearchError=ValueError, search_videos=search_api),
        "_home_direct_test.search_backend": module(
            "_home_direct_test.search_backend",
            SearchBackendError=RuntimeError, search_with_ytdlp=search_ytdlp,
            select_backend=lambda key, available: "api" if key else "yt-dlp" if available else None),
        "_home_direct_test.settings": module(
            "_home_direct_test.settings", get_api_key=lambda: "TEST_KEY"),
        "_home_direct_test.resolver": module(
            "_home_direct_test.resolver", is_available=lambda: True),
        "_home_direct_test.i18n": module(
            "_home_direct_test.i18n", tr=lambda text: text),
        "_home_direct_test.grid": module(
            "_home_direct_test.grid", WarderYouTubeGrid=FakeVideoGrid),
        "twisted": twisted,
        "twisted.internet": internet,
        "twisted.internet.threads": module(
            "twisted.internet.threads", deferToThread=worker)
    }
    spec = importlib.util.spec_from_file_location(
        "_home_direct_test.home_search_flow", SOURCE
    )
    flow_mod = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, classes):
        spec.loader.exec_module(flow_mod)
        home = FakeHome()
        yield flow_mod.HomeSearchFlow(home), home, jobs, search_api


class DirectSearchFlowTests(unittest.TestCase):
    def video(self):
        return {"video_id": "abcdefghijk", "title": "Aladin", "channel": "Disney"}

    def test_results_open_directly_from_home_without_transient_search_screen(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            self.assertEqual(home.session.grids, [])
            self.assertEqual(home.session.other_dialogs, [])
            self.assertTrue(flow.loading)
            self.assertEqual(jobs[0][0], (api, "aladin", "TEST_KEY", ""))
            jobs[0][1].success({"items": [self.video()], "next_page_token": "page2"})
            self.assertFalse(flow.loading)
            self.assertEqual(len(home.session.grids), 1)
            grid = home.session.grids[0]
            self.assertEqual(grid.args[0], [self.video()])
            self.assertEqual(grid.args[1:3], ("aladin", True))
            self.assertEqual(home.session.other_dialogs, [])
            self.assertEqual(flow.query, "aladin")

    def test_blue_new_search_returns_to_two_panels_and_resets_system_input(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            jobs[0][1].success({"items": [self.video()], "next_page_token": ""})
            grid = home.session.grids[-1]
            grid.close("search")
            self.assertTrue(grid._closed)
            self.assertEqual(home.index, 1)
            self.assertEqual(home.focus_area, "keyboard")
            self.assertEqual(home.preview_count, 1)
            self.assertEqual(home.inline_keyboard.reset_calls, 1)
            self.assertEqual(home.inline_keyboard.value_text, "")
            self.assertEqual(len(home.session.grids), 1)
            self.assertEqual(home.session.other_dialogs, [])

    def test_next_page_keeps_home_as_loading_screen_and_opens_grid_only_on_data(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            jobs[0][1].success({"items": [self.video()], "next_page_token": "PT2"})
            home.session.grids[-1].close("next")
            self.assertEqual(len(jobs), 2)
            self.assertEqual(jobs[1][0], (api, "aladin", "TEST_KEY", "PT2"))
            self.assertEqual(len(home.session.grids), 1)
            jobs[1][1].success({"items": [self.video()], "next_page_token": ""})
            self.assertEqual(len(home.session.grids), 2)
            self.assertEqual(home.session.other_dialogs, [])

    def test_back_goes_to_home_with_no_search_screen_underneath(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            jobs[0][1].success({"items": [self.video()], "next_page_token": ""})
            home.session.grids[-1].close("home")
            self.assertEqual(home.index, 0)
            self.assertEqual(home.focus_area, "nav")
            self.assertEqual(home.preview_count, 1)
            self.assertEqual(home.session.other_dialogs, [])

    def test_grid_playback_delegates_existing_home_player(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            jobs[0][1].success({"items": [self.video()], "next_page_token": ""})
            grid = home.session.grids[-1]
            on_play = grid.args[3]
            on_play(self.video())
            self.assertEqual(home.play_requests, [self.video()])
            self.assertEqual(home.session.other_dialogs, [])

    def test_late_worker_result_cannot_reopen_closed_or_other_section(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            flow.cancel_pending()
            jobs[0][1].success({"items": [self.video()], "next_page_token": ""})
            self.assertEqual(home.session.grids, [])
            flow.start("new")
            home.index = 3
            jobs[1][1].success({"items": [self.video()], "next_page_token": ""})
            self.assertEqual(home.session.grids, [])
            home.index = 1
            flow.dispose()
            jobs[1][1].failure(RuntimeError("wrong"))
            self.assertEqual(home.session.grids, [])

    def test_failed_or_empty_search_keeps_real_inline_keyboard_visible(self):
        with native_search() as (flow, home, jobs, api):
            flow.start("aladin")
            jobs[0][1].failure(types.SimpleNamespace(value=RuntimeError("Test backend unavailable")))
            self.assertIn("Test backend unavailable", home["kb_feedback"].text)
            self.assertEqual(home.session.grids, [])
            flow.start("aladin")
            jobs[1][1].success({"items": [], "next_page_token": ""})
            self.assertIn("No videos found", home["kb_feedback"].text)
            self.assertEqual(home.session.grids, [])


if __name__ == "__main__":
    unittest.main()
