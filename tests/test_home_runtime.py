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
        "_warder_home.header_ui": fake("_warder_home.header_ui", add_header=lambda sc: sc.__setitem__("hdr_version", Widget())),
        "_warder_home": pkg,
        "_warder_home.skin": fake("_warder_home.skin", HOME_SKIN="<screen/>"),
        "_warder_home.i18n": fake("_warder_home.i18n", tr=lambda text: text,
                                    language_code=lambda: "sk"),
        "_warder_home.update_core": fake("_warder_home.update_core", CURRENT_VERSION="0.0.8~test8"),
        "_warder_home.grid_model": fake("_warder_home.grid_model", move_index=move),
        "_warder_home.home_feed": fake("_warder_home.home_feed", popular_videos=lambda key: [], public_home_videos=lambda: []),
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
        # Initial Home requests the public anonymous feed once, but merely
        # moving between sections never opens modal dialogs or issues more.
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0][0], (mod.public_home_videos,))

    def test_public_home_without_api_replaces_local_fallback(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        self.assertEqual(len(jobs), 1)
        self.assertIs(jobs[0][0][0], mod.public_home_videos)
        self.assertEqual(screen["subtitle"].text, "Recently played (offline)")
        jobs[0][2].success([video(4)])
        self.assertEqual(screen["subtitle"].text,
                         "Public YouTube selection (no API key)")
        self.assertEqual(screen.video_items[0]["video_id"], video(4)["video_id"])
        screen.down()
        screen.up()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(len(screen.video_items), 1)

    def test_public_feed_failure_keeps_local_videos(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        jobs[0][2].failure(RuntimeError("site changed"))
        self.assertEqual(screen["subtitle"].text, "Recently played (offline)")
        self.assertEqual(len(screen.video_items), len(saved["history"]))
        self.assertEqual(len(jobs), 1)

    def test_left_menu_wraps_endlessly_in_both_directions(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        self.assertEqual(screen.index, 0)

        screen.up()  # Domov -> Aktualizacie
        self.assertEqual(screen.index, 7)
        self.assertEqual(screen["heading"].text, "Updates")
        self.assertTrue(screen["nav_focus7"].visible)
        self.assertFalse(screen["nav_focus0"].visible)

        screen.down()  # Aktualizacie -> Domov
        self.assertEqual(screen.index, 0)
        self.assertEqual(screen["heading"].text, "Home")
        self.assertTrue(screen["nav_focus0"].visible)
        self.assertFalse(screen["nav_focus7"].visible)

        for _ in range(len(screen.sections) * 3):
            screen.down()
        self.assertEqual(screen.index, 0)
        for _ in range(len(screen.sections) * 2):
            screen.up()
        self.assertEqual(screen.index, 0)
        self.assertEqual(screen.focus_area, "nav")
        self.assertEqual(session.opens, [])
        self.assertEqual(session.callbacks, [])
        # Scrolling around never starts new network requests after initial Home.
        self.assertEqual(len(jobs), 1)

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

    def test_navigation_hint_removed_and_focus_follows_home_and_history(self):
        mod, key, saved, jobs = load()
        screen, session = ready(mod)
        # The remote help used to be rendered on every menu preview, directly
        # on top of the bottom frame. The status area is now reserved for
        # actual errors, loading and the focused video name.
        self.assertNotIn("Up/Down: sections", screen["status"].text)
        self.assertTrue(screen["nav_focus0"].visible)
        screen.right()
        self.assertTrue(screen["preview_focus0"].visible)
        self.assertFalse(screen["preview_focus1"].visible)
        screen.right()
        self.assertFalse(screen["preview_focus0"].visible)
        self.assertTrue(screen["preview_focus1"].visible)
        screen.left()
        screen.left()
        self.assertEqual(screen.focus_area, "nav")
        self.assertEqual(screen["status"].text, "")
        # Home and History use the same genuine video focus rather than
        # having an unmarked selected thumbnail in History.
        for _ in range(3):
            screen.down()
        self.assertEqual(screen[ "heading" ].text, "History")
        self.assertTrue(screen["nav_focus3"].visible)
        self.assertEqual(screen["status"].text, "")
        screen.right()
        self.assertTrue(screen["preview_focus0"].visible)
        screen.right()
        self.assertTrue(screen["preview_focus1"].visible)
        self.assertFalse(screen["preview_focus0"].visible)

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

    def test_live_home_pages_through_all_youtube_results_not_fixed_six(self):
        mod, key, saved, jobs = load(key="configured-api-key")
        screen, session = ready(mod)
        jobs[0][2].success([video(i) for i in range(14)])
        self.assertEqual(len(screen.video_items), 6)
        self.assertEqual(screen.video_items[0]["video_id"], video(0)["video_id"])
        self.assertIn("1 / 3", screen["page_info"].text)
        screen.right()
        screen.down()    # tile 0 -> tile 3
        screen.down()    # beyond bottom row -> next real batch
        self.assertEqual(screen.page_index, 1)
        self.assertEqual(screen.video_items[0]["video_id"], video(6)["video_id"])
        screen.down()
        screen.down()
        self.assertEqual(screen.page_index, 2)
        self.assertEqual([v["video_id"] for v in screen.video_items],
                         [video(12)["video_id"], video(13)["video_id"]])
        screen.up()
        self.assertEqual(screen.page_index, 1)
        self.assertEqual(len(jobs), 1)  # Paging uses real buffered videos.

    def test_live_feed_revalidates_after_ttl_without_erasing_current_cards(self):
        mod, key, saved, jobs = load(key="configured-api-key")
        screen, session = ready(mod)
        jobs[0][2].success([video(i) for i in range(7)])
        screen._version_checked = True
        screen._popular_fetched_at = 0
        with patch.object(mod, "monotonic", return_value=1000):
            screen._on_shown()
        self.assertEqual(len(jobs), 2)
        self.assertEqual(screen.video_items[0]["video_id"], video(0)["video_id"])
        jobs[1][2].success([video(7), video(8)])
        self.assertEqual(screen.video_items[0]["video_id"], video(7)["video_id"])
        self.assertEqual(screen["page_info"].text, "")
        self.assertEqual(len(session.opens), 0)

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
