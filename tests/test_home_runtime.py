"""Mocked native Enigma2 navigation tests for Home live preview."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class Widget:
    def __init__(self, text=""):
        self.text = text
        self.visible = True
        self.image = None

    def setText(self, value):
        self.text = value

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def setPixmap(self, value):
        self.image = value


class FakeScreen(dict):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.onLayoutFinish = []
        self.onShown = []
        self.onClose = []
        self.closed = False

    def close(self, *args):
        self.closed = True
        for action in self.onClose:
            action()


class FakeDeferred:
    def __init__(self):
        self.success = None
        self.failure = None

    def addCallbacks(self, success, failure):
        self.success, self.failure = success, failure


class FakeSession:
    def __init__(self):
        self.opens = []
        self.callbacks = []

    def open(self, *args):
        self.opens.append(args)

    def openWithCallback(self, callback, *args):
        self.callbacks.append((callback, args))


class FakeThumbs:
    def __init__(self, owner):
        self.owner = owner
        self.started = False
        self.pages = []
        self.closed = False

    def start(self):
        self.started = True

    def show(self, items):
        self.pages.append(list(items))

    def close(self):
        self.closed = True


def fake(name, **members):
    result = types.ModuleType(name)
    for key, value in members.items():
        setattr(result, key, value)
    return result


def video(i):
    return {"video_id": "abcdefghij" + str(i), "title": "A very long sample video title " + str(i),
            "channel": "Channel", "thumbnail_url": "https://i.ytimg.com/vi/abcdefghij%d/mqdefault.jpg" % i}


def load(key="", history=None, fav=None):
    pkg = fake("_warder_home")
    pkg.__path__ = [str(ROOT)]
    key_slot = {"value": key}
    storage = {
        "history": list(history if history is not None else [video(0), video(1)]),
        "favourites": list(fav if fav is not None else [video(2)])
    }
    jobs = []

    def worker(*args, **kwargs):
        task = FakeDeferred()
        jobs.append((args, kwargs, task))
        return task

    def list_videos(kind):
        return list(storage[kind])

    def move(index, direction, count):
        if not count:
            return -1
        delta = {"left": -1, "right": 1, "up": -3, "down": 3}[direction]
        return max(0, min(count - 1, index + delta))

    components = fake("Components")
    components.__path__ = []
    screens = fake("Screens")
    screens.__path__ = []
    twisted = fake("twisted")
    twisted.__path__ = []
    internet = fake("twisted.internet")
    internet.__path__ = []
    modules = {
        "_warder_home": pkg,
        "_warder_home.skin": fake("_warder_home.skin", HOME_SKIN="<screen/>"),
        "_warder_home.i18n": fake("_warder_home.i18n", tr=lambda text: text),
        "_warder_home.update_core": fake("_warder_home.update_core", CURRENT_VERSION="0.0.8~test8"),
        "_warder_home.grid_model": fake("_warder_home.grid_model", move_index=move),
        "_warder_home.home_feed": fake("_warder_home.home_feed", popular_videos=lambda key: []),
        "_warder_home.home_thumbs": fake("_warder_home.home_thumbs", HomeThumbs=FakeThumbs),
        "_warder_home.local_library": fake(
            "_warder_home.local_library", LibraryError=ValueError, list_videos=list_videos,
            toggle_favourite=lambda item: True, record_opened=lambda item: None,
            remove_video=lambda kind, item: True, clear_videos=lambda kind: None
        ),
        "_warder_home.settings": fake(
            "_warder_home.settings",
            get_api_key=lambda: key_slot["value"], get_quality=lambda: "720"
        ),
        "_warder_home.resolver": fake(
            "_warder_home.resolver", ResolverError=ValueError,
            resolve_video_streams=lambda *args, **kwargs: [], is_available=lambda: True
        ),
        "_warder_home.api": fake("_warder_home.api", SearchError=ValueError),
        "Components": components,
        "Components.ActionMap": fake("Components.ActionMap", ActionMap=lambda *a, **kw: Widget()),
        "Components.Label": fake("Components.Label", Label=Widget),
        "Components.Pixmap": fake("Components.Pixmap", Pixmap=Widget),
        "Screens": screens,
        "Screens.Screen": fake("Screens.Screen", Screen=FakeScreen),
        "twisted": twisted,
        "twisted.internet": internet,
        "twisted.internet.threads": fake("twisted.internet.threads", deferToThread=worker),
    }
    spec = importlib.util.spec_from_file_location("_warder_home.ui", ROOT / "ui.py")
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(module)
    return module, key_slot, storage, jobs


def ready(module):
    session = FakeSession()
    screen = module.WarderYouTubeHome(session)
    for callback in screen.onLayoutFinish:
        callback()
    return screen, session


class HomeLivePreviewTests(unittest.TestCase):
    def test_screen_items_method_survives_home_navigation_and_close(self):
        # Enigma2 Screen.deleteGUIScreen calls list(self.items()); an instance
        # attribute named "items" crashes GUI teardown after EXIT.
        mod, key, storage, jobs = load()
        screen, session = ready(mod)
        self.assertTrue(callable(screen.items))
        self.assertIn("heading", dict(screen.items()))
        screen.down()
        screen.down()
        screen.down()
        self.assertTrue(callable(screen.items))
        screen.back()
        self.assertTrue(screen.closed)

    def test_selection_changes_right_pane_without_modal(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        self.assertTrue(screen["nav_focus0"].visible)
        self.assertEqual(len(screen.video_items), 2)
        self.assertEqual(screen["heading"].text, "Home")
        screen.down()  # Search
        self.assertEqual(screen["heading"].text, "Search")
        self.assertTrue(screen["preview_message"].visible)
        self.assertEqual(len(screen.video_items), 0)
        screen.down()  # Subscriptions
        self.assertIn("not supported", screen["preview_message"].text)
        screen.down()  # History
        self.assertEqual(screen["heading"].text, "History")
        self.assertEqual(screen["preview_title0"].text, saved["history"][0]["title"])
        self.assertEqual(len(screen.video_items), 2)
        self.assertFalse(screen["nav_focus0"].visible)
        self.assertTrue(screen["nav_focus3"].visible)
        self.assertEqual(session.opens, [])
        self.assertEqual(session.callbacks, [])
        self.assertEqual(jobs, [])

    def test_arrow_right_enters_tiles_and_ok_is_not_automatic(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        screen._play_selected = lambda: session.opens.append(("play",))
        screen.right()
        self.assertEqual(screen.focus_area, "tiles")
        self.assertTrue(screen["preview_focus0"].visible)
        self.assertFalse(screen["nav_focus0"].visible)
        self.assertEqual(session.opens, [])
        screen.right()
        self.assertEqual(screen.tile_index, 1)
        screen.activate()
        self.assertEqual(session.opens, [("play",)])
        screen.left()
        self.assertEqual(screen.tile_index, 0)
        screen.left()
        self.assertEqual(screen.focus_area, "nav")
        self.assertTrue(screen["nav_focus0"].visible)

    def test_history_favourites_and_empty_states_are_real(self):
        mod, key, saved, jobs = load(history=[], fav=[video(2)])
        screen, session = ready(mod)
        self.assertEqual(screen["subtitle"].text, "Favourites (offline)")
        for _ in range(3):
            screen.down()
        self.assertIn("No saved videos", screen["preview_message"].text)
        screen.down()
        screen.down()
        self.assertEqual(screen["heading"].text, "Favourites")
        self.assertEqual(screen.video_items[0]["video_id"], video(2)["video_id"])

    def test_popular_feed_result_is_cached_when_navigating_away(self):
        mod, key, saved, jobs = load(key="test-key")
        screen, session = ready(mod)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0][0][0].__name__, "<lambda>")
        self.assertEqual(jobs[0][0][1], "test-key")
        self.assertIn("Loading", screen["preview_message"].text)
        screen.down()
        jobs[0][2].success([video(3)])
        self.assertEqual(screen["heading"].text, "Search")
        screen.up()
        self.assertEqual(screen.video_items[0]["video_id"], video(3)["video_id"])
        self.assertEqual(screen["subtitle"].text, "Popular in Slovakia")
        self.assertEqual(len(jobs), 1)

    def test_closing_rejects_late_internet_results(self):
        mod, key, saved, jobs = load(key="test-key")
        screen, session = ready(mod)
        screen.close()
        self.assertTrue(screen.thumbs.closed)
        jobs[0][2].success([video(4)])
        self.assertTrue(screen._disposed)
        self.assertEqual(screen.video_items, [])


if __name__ == "__main__":
    unittest.main()
