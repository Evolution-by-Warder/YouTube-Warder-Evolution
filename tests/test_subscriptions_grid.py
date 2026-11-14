"""Offline native subscription gallery: identical thumbnail budget to Home.

No Google account credentials, network or real receiver required.
"""
import importlib.util
from pathlib import Path
from unittest.mock import patch
import sys
import types
import unittest
import xml.etree.ElementTree as ET


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

    def setPixmap(self, image):
        self.image = image


class MenuList(Widget):
    def __init__(self, values):
        super().__init__()
        self.values = values
        self.index = 0
        self.instance = None

    def setList(self, values):
        self.values = list(values)
        self.index = 0

    def getCurrentIndex(self):
        return self.index

    def down(self):
        self.index = min(len(self.values) - 1, self.index + 1)

    def up(self):
        self.index = max(0, self.index - 1)


class Screen(dict):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.onShown = []
        self.onLayoutFinish = []
        self.onClose = []

    def close(self, *args):
        for cb in self.onClose:
            cb()


class Actions:
    def __init__(self, contexts, mapping, *args):
        self.contexts = contexts
        self.mapping = mapping


class Session:
    def __init__(self):
        self.opens = []

    def open(self, klass, *args, **kwargs):
        self.opens.append((klass, args, kwargs))

    def openWithCallback(self, cb, klass, *args, **kwargs):
        self.opens.append((klass, args, kwargs, cb))


class Deferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


class Thumbs:
    def __init__(self, screen):
        self.screen = screen
        self.started = False
        self.closed = False
        self.shown = []
        self.image_cache = {}

    def start(self):
        self.started = True

    def show(self, items):
        self.shown.append(list(items))
        for i in range(6):
            self.screen["preview_thumb%d" % i].hide()

    def close(self):
        self.closed = True


def module(name, **attrs):
    obj = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(obj, key, value)
    return obj


def video(i):
    return {
        "video_id": "abcdefghij" + str(i),
        "title": "Real video %d" % i,
        "channel": "Artist",
        "thumbnail_url": "https://i.ytimg.com/vi/abcdefghij%d/mqdefault.jpg" % i,
    }


def channel(i):
    return {"channel_id": "UC" + str(i).zfill(22), "title": "Channel %d" % i}


def load():
    pkg = module("_subs_grid")
    pkg.__path__ = [str(ROOT)]
    components = module("Components")
    components.__path__ = []
    screens = module("Screens")
    screens.__path__ = []
    twisted = module("twisted")
    twisted.__path__ = []
    internet = module("twisted.internet")
    internet.__path__ = []
    jobs = []

    def worker(fn):
        d = Deferred()
        jobs.append((fn, d))
        return d

    # Reuse actual blue Library XML, so the gallery must be valid native XML.
    import ast
    tree = ast.parse((ROOT / "skin.py").read_text(encoding="utf-8"))
    base = next(
        ast.literal_eval(stmt.value)
        for stmt in tree.body
        if isinstance(stmt, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "LIBRARY_SKIN"
                for t in stmt.targets)
    )
    home = next(
        ast.literal_eval(stmt.value)
        for stmt in tree.body
        if isinstance(stmt, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "HOME_SKIN"
                for t in stmt.targets)
    )
    fake = {
        "_subs_grid": pkg,
        "_subs_grid.header_ui": module("_subs_grid.header_ui", add_header=lambda scr: scr.__setitem__("hdr_version", Widget())),
        "_subs_grid.i18n": module("_subs_grid.i18n", tr=lambda message: message),
        "_subs_grid.skin": module("_subs_grid.skin", LIBRARY_SKIN=base, HOME_SKIN=home),
        "_subs_grid.home_thumbs": module("_subs_grid.home_thumbs", HomeThumbs=Thumbs),
        "_subs_grid.subscriptions_auth": module(
            "_subs_grid.subscriptions_auth", SubscriptionsAuthError=ValueError,
            account_connected=lambda: True, read_client=lambda: {},
            request_device_code=lambda c: {}, poll_device_code=lambda c,d: ("pending", None),
            save_tokens=lambda t: None, clear_tokens=lambda: None, access_token=lambda: "fake"
        ),
        "_subs_grid.subscriptions_api": module(
            "_subs_grid.subscriptions_api", SubscriptionsApiError=ValueError,
            subscriptions_list=lambda token: [],
            recent_subscription_videos=lambda token: ([], []),
            uploads_playlists=lambda ids, token: {},
            playlist_videos=lambda *args, **kwargs: []
        ),
        "_subs_grid.local_library": module(
            "_subs_grid.local_library", LibraryError=ValueError, record_opened=lambda v: None
        ),
        "_subs_grid.settings": module(
            "_subs_grid.settings", get_quality=lambda: "720"
        ),
        "_subs_grid.resolver": module(
            "_subs_grid.resolver", ResolverError=ValueError,
            resolve_video_streams=lambda *args, **kwargs: []
        ),
        "Components": components,
        "Components.ActionMap": module("Components.ActionMap", ActionMap=Actions),
        "Components.Label": module("Components.Label", Label=Widget),
        "Components.MenuList": module("Components.MenuList", MenuList=MenuList),
        "Components.Pixmap": module("Components.Pixmap", Pixmap=Widget),
        "Screens": screens,
        "Screens.Screen": module("Screens.Screen", Screen=Screen),
        "twisted": twisted,
        "twisted.internet": internet,
        "twisted.internet.threads": module("twisted.internet.threads", deferToThread=worker),
    }
    spec = importlib.util.spec_from_file_location("_subs_grid.subscriptions_ui", ROOT / "subscriptions_ui.py")
    mod = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(mod)
    return mod, fake, jobs


class SubscriptionGalleryTests(unittest.TestCase):
    def test_native_approved_container_and_six_cards(self):
        mod, fake, jobs = load()
        root = ET.fromstring(mod.WarderYouTubeSubscriptions.skin)
        self.assertEqual(root.attrib["size"], "1920,1080")
        self.assertEqual(root.attrib["backgroundColor"], "#08182D")
        nodes = {n.attrib["name"]: n.attrib for n in root.findall("widget")}
        self.assertIn("hdr_version", nodes)
        self.assertIn("results", nodes)
        self.assertEqual(
            len([name for name in nodes if name.startswith("preview_thumb")]), 6
        )
        self.assertEqual(
            len([name for name in nodes if name.startswith("tile_focus")]), 6
        )
        self.assertIn("/video_focus.png", nodes["tile_focus0"]["pixmap"])
        self.assertEqual(nodes["preview_thumb0"]["size"], "473,248")
        self.assertEqual(nodes["tile_title0"]["size"], "457,60")
        self.assertEqual(nodes["tile_channel0"]["size"], "457,24")
        self.assertEqual(nodes["tile_focus0"]["size"], "477,350")
        self.assertEqual(nodes["tile_panel0"]["size"], "473,346")
        self.assertEqual(nodes["video_scroll_track"]["position"], "1781,231")
        self.assertEqual(nodes["video_scroll_thumb"]["position"], "1783,231")
        self.assertNotIn("render=", mod.WarderYouTubeSubscriptions.skin)

    def test_recent_videos_are_3x2_pages_with_real_selection(self):
        mod, fake, jobs = load()
        screen = mod.WarderYouTubeSubscriptions(Session())
        self.assertTrue(callable(screen.items))  # Enigma2 Screen teardown
        screen._start_thumbs()
        self.assertTrue(screen.thumbs.started)
        with patch.dict(sys.modules, fake):
            screen.latest = lambda: None
            screen.connected = True
            screen.mode = "recent"
            screen._rows([video(i) for i in range(13)])
        self.assertFalse(screen["results"].visible)
        self.assertEqual(len(screen.thumbs.shown[-1]), 6)
        self.assertEqual(screen.thumbs.shown[-1][0]["video_id"], video(0)["video_id"])
        self.assertEqual(screen["page_info"].text, "1 / 3  •  13")
        self.assertTrue(screen["video_scroll_thumb"].visible)
        self.assertEqual(screen.page_scroll.pages, 3)
        self.assertTrue(screen["tile_focus0"].visible)
        self.assertFalse(screen["tile_focus1"].visible)
        screen.navigate("down")
        self.assertEqual(screen.tile_index, 3)
        screen.navigate("down")
        self.assertEqual(screen.page_index, 1)
        self.assertEqual(screen._selected()["video_id"], video(6)["video_id"])
        self.assertEqual(screen.thumbs.shown[-1][0]["video_id"], video(6)["video_id"])
        screen.navigate("down")
        screen.navigate("down")
        self.assertEqual(screen.page_index, 2)
        self.assertEqual(screen._selected()["video_id"], video(12)["video_id"])
        screen.navigate("up")
        self.assertEqual(screen.page_index, 1)
        screen.close()
        self.assertTrue(screen.thumbs.closed)

    def test_all_channels_uses_tiles_with_channel_avatars_and_page_scrollbar(self):
        mod, fake, jobs = load()
        screen = mod.WarderYouTubeSubscriptions(Session())
        screen._start_thumbs()
        screen.connected = True
        screen.mode = "recent"
        screen._rows([video(i) for i in range(9)])
        screen.mode = "channels"
        avatars = [
            dict(channel(i), thumbnail_url="https://yt3.ggpht.com/example-avatar-%d" % i)
            for i in range(13)
        ]
        screen._rows(avatars)
        self.assertFalse(screen["results"].visible)
        self.assertEqual(len(screen.thumbs.shown[-1]), 6)
        self.assertEqual(len(screen.mode_items), 13)
        self.assertEqual(screen["page_info"].text, "1 / 3  •  13")
        self.assertEqual(screen["tile_title0"].text, "Channel 0")
        self.assertEqual(screen["tile_channel0"].text, "Channel")
        self.assertTrue(screen["video_scroll_track"].visible)
        self.assertTrue(screen["video_scroll_thumb"].visible)
        screen.navigate("right")
        self.assertEqual(screen._selected()["title"], "Channel 1")
        screen.navigate("down")
        screen.navigate("down")
        self.assertEqual(screen.page_index, 1)
        self.assertEqual(screen._selected()["title"], "Channel 7")
        screen.navigate("down")
        screen.navigate("down")
        self.assertEqual(screen.page_index, 2)
        self.assertEqual(screen._selected()["title"], "Channel 12")
        self.assertEqual(screen.page_scroll.page, 2)
        self.assertEqual(screen.page_scroll.pages, 3)
        self.assertEqual(len(screen.thumbs.shown[-1]), 1)
        screen.close()
        self.assertTrue(screen.thumbs.closed)

    def test_logged_out_tv_authorization_keeps_readable_text_list(self):
        mod, fake, jobs = load()
        screen = mod.WarderYouTubeSubscriptions(Session())
        screen._start_thumbs()
        screen.connected = False
        screen._code_ready(({"client_id":"fake"},{
            "device_code": "fake-device-code",
            "user_code": "ABCD-EFGH",
            "verification_url": "https://www.google.com/device",
            "expires_in": 600, "interval": 5
        }))
        self.assertEqual(screen.mode, "login")
        self.assertTrue(screen["results"].visible)
        self.assertIn("ABCD-EFGH", screen["results"].values[1])
        self.assertEqual(screen.thumbs.shown[-1], [])
        self.assertFalse(screen["tile_focus0"].visible)


if __name__ == "__main__":
    unittest.main()
