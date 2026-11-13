"""Mock native Enigma2 Favorites/History UI; zero live network or opkg."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

PATH = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube/library_ui.py")


class Widget:
    def __init__(self, text=""):
        self.text = text
        self.values = []
        self.onSelectionChanged = []

    def setText(self, value):
        self.text = value

    def setList(self, values):
        self.values = values

    def getCurrentIndex(self):
        return 0


class Screen(dict):
    def __init__(self, session):
        self.session = session
        self.onShown = []
        self.onClose = []
        self.closed = False

    def close(self):
        self.closed = True
        for fn in self.onClose:
            fn()


class Deferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


class Session:
    def __init__(self):
        self.opens = []
        self.confirmations = []

    def open(self, klass, *args, **kwargs):
        self.opens.append((klass, args, kwargs))

    def openWithCallback(self, callback, klass, *args, **kwargs):
        self.confirmations.append((callback, klass, args, kwargs))


def mkmod(name, **attrs):
    value = types.ModuleType(name)
    for key, item in attrs.items():
        setattr(value, key, item)
    return value


def sample(n):
    return {
        "video_id": ("%011d" % n), "title": "Song " + str(n),
        "channel": "Official Artist", "published_at": "",
        "thumbnail_url": "https://i.ytimg.com/vi/00000000001/mqdefault.jpg"
    }


def load():
    videos = {"history": [sample(1)], "favourites": [sample(2)]}
    jobs = []
    played = []
    recorded = []
    def list_videos(kind):
        return list(videos[kind])
    def remove_video(kind, video_id):
        old = len(videos[kind])
        videos[kind] = [v for v in videos[kind] if v["video_id"] != video_id]
        return old != len(videos[kind])
    def clear_videos(kind):
        videos[kind] = []
    def toggle_favourite(video):
        collection = videos["favourites"]
        if any(item["video_id"] == video["video_id"] for item in collection):
            remove_video("favourites", video["video_id"])
            return False
        collection.insert(0, video)
        return True
    def record_opened(video):
        recorded.append(video["video_id"])
    def defer(function, *args, **kwargs):
        d = Deferred()
        jobs.append((function, args, kwargs, d))
        return d
    def play(session, streams, title, on_close):
        played.append((streams, title, on_close))
    keyboard = type("FakeMessageBox", (), {"TYPE_YESNO": 1, "TYPE_INFO": 2})
    package = mkmod("_test_warder_library")
    package.__path__ = [str(PATH.parent)]
    components = mkmod("Components")
    components.__path__ = []
    screens = mkmod("Screens")
    screens.__path__ = []
    twisted = mkmod("twisted")
    twisted.__path__ = []
    internet = mkmod("twisted.internet")
    internet.__path__ = []
    fake = {
        "_test_warder_library": package,
        "_test_warder_library.i18n": mkmod(
            "_test_warder_library.i18n", tr=lambda value: value
        ),
        "_test_warder_library.confirm_ui": mkmod(
            "_test_warder_library.confirm_ui", WarderYouTubeConfirm=object
        ),
        "_test_warder_library.skin": mkmod(
            "_test_warder_library.skin", LIBRARY_SKIN="<screen/>"
        ),
        "_test_warder_library.local_library": mkmod(
            "_test_warder_library.local_library",
            LibraryError=ValueError, list_videos=list_videos,
            remove_video=remove_video, clear_videos=clear_videos,
            toggle_favourite=toggle_favourite, record_opened=record_opened
        ),
        "_test_warder_library.resolver": mkmod(
            "_test_warder_library.resolver",
            ResolverError=ValueError, resolve_video_streams=lambda *a, **k: []
        ),
        "_test_warder_library.settings": mkmod(
            "_test_warder_library.settings", get_quality=lambda: "720"
        ),
        "_test_warder_library.player": mkmod(
            "_test_warder_library.player",
            dash_available=lambda: False, open_player=play
        ),
        "Components": components,
        "Components.ActionMap": mkmod(
            "Components.ActionMap", ActionMap=lambda *a, **k: object()
        ),
        "Components.Label": mkmod("Components.Label", Label=Widget),
        "Components.MenuList": mkmod("Components.MenuList", MenuList=Widget),
        "Screens": screens,
        "Screens.Screen": mkmod("Screens.Screen", Screen=Screen),
        "Screens.MessageBox": mkmod("Screens.MessageBox", MessageBox=keyboard),
        "twisted": twisted, "twisted.internet": internet,
        "twisted.internet.threads": mkmod(
            "twisted.internet.threads", deferToThread=defer
        ),
    }
    spec = importlib.util.spec_from_file_location(
        "_test_warder_library.library_ui", str(PATH))
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(module)
    return module, fake, videos, jobs, played, recorded


class LibraryUiTests(unittest.TestCase):
    def test_favourites_and_history_open_without_api_key(self):
        ui, fake, videos, jobs, played, recorded = load()
        for kind, expected in (("history", "Song 1"), ("favourites", "Song 2")):
            screen = ui.WarderYouTubeLibrary(Session(), kind)
            with patch.dict(sys.modules, fake):
                for show in screen.onShown:
                    show()
            self.assertIn(expected, screen["results"].values[0])
            self.assertEqual(len(screen.video_items), 1)
        self.assertEqual(jobs, [])

    def test_menu_from_history_saves_favourite_and_yellow_removes(self):
        ui, fake, videos, jobs, played, recorded = load()
        screen = ui.WarderYouTubeLibrary(Session(), "history")
        screen.refresh()
        screen.save_favourite()
        self.assertEqual(len(videos["favourites"]), 2)
        screen.remove_selected()
        self.assertEqual(videos["history"], [])
        self.assertEqual(len(videos["favourites"]), 2)

    def test_clear_requires_yes_and_deduplicates_confirmations(self):
        ui, fake, videos, jobs, played, recorded = load()
        session = Session()
        screen = ui.WarderYouTubeLibrary(session, "history")
        screen.refresh()
        screen.confirm_clear()
        screen.confirm_clear()
        self.assertEqual(len(session.confirmations), 1)
        session.confirmations[0][0](False)
        self.assertEqual(len(videos["history"]), 1)
        screen.confirm_clear()
        self.assertEqual(len(session.confirmations), 2)
        session.confirmations[-1][0](True)
        self.assertEqual(videos["history"], [])
        self.assertEqual(len(videos["favourites"]), 1)

    def test_play_uses_background_resolver_and_records_after_player_opens(self):
        ui, fake, videos, jobs, played, recorded = load()
        session = Session()
        screen = ui.WarderYouTubeLibrary(session, "favourites")
        screen.refresh()
        with patch.dict(sys.modules, fake):
            screen.play_selected()
            screen.play_selected()  # no parallel resolution
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0][1], (sample(2)["video_id"],))
            self.assertEqual(jobs[0][2], {"quality": "720", "dash": False})
            self.assertEqual(recorded, [])
            streams = [{"url": "https://rr1.googlevideo.com/stream", "service_type": 4097}]
            jobs[0][3].success(streams)
            self.assertEqual(len(played), 1)
            self.assertEqual(recorded, [sample(2)["video_id"]])
            self.assertTrue(screen.playback_active)
            screen.play_selected()
            self.assertEqual(len(jobs), 1)
            played[0][2](False)
            self.assertFalse(screen.playback_active)
            self.assertIn("Prehrávanie ukončené", screen["status"].text)

    def test_failed_player_creation_never_records_history_or_signed_url(self):
        ui, fake, videos, jobs, played, recorded = load()
        screen = ui.WarderYouTubeLibrary(Session(), "favourites")
        screen.refresh()
        def failure(*args, **kwargs):
            raise RuntimeError("https://rr1.googlevideo.com/?sig=SECRET")
        fake["_test_warder_library.player"].open_player = failure
        with patch.dict(sys.modules, fake):
            screen.play_selected()
            jobs[0][3].success([{"url": "https://rr1.googlevideo.com/stream",
                                 "service_type": 4097}])
        self.assertFalse(screen.playback_active)
        self.assertEqual(recorded, [])
        self.assertNotIn("SECRET", screen["status"].text)

    def test_closed_screen_discards_late_resolution(self):
        ui, fake, videos, jobs, played, recorded = load()
        screen = ui.WarderYouTubeLibrary(Session(), "history")
        screen.refresh()
        with patch.dict(sys.modules, fake):
            screen.play_selected()
            screen.close()
            jobs[0][3].success([{"url": "https://rr1.googlevideo.com/stream",
                                 "service_type": 4097}])
        self.assertEqual(played, [])
        self.assertEqual(recorded, [])

    def test_info_is_local_and_read_only(self):
        ui, fake, videos, jobs, played, recorded = load()
        session = Session()
        screen = ui.WarderYouTubeLibrary(session, "favourites")
        screen.refresh()
        screen.show_info()
        self.assertEqual(len(session.opens), 1)
        self.assertIn("Song 2", session.opens[0][1][0])
        self.assertEqual(jobs, [])


if __name__ == "__main__":
    unittest.main()
