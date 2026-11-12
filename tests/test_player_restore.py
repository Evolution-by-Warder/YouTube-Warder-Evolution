"""Mock Enigma2 runtime: verify previous-channel restoration on all exits."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

PLAYER = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/player.py"


class ServiceRef:
    def __init__(self, service_type, flags, url):
        self.service_type = service_type
        self.flags = flags
        self.url = url
        self.title = None

    def setName(self, value):
        self.title = value


class Nav:
    def __init__(self, previous="previous TV reference"):
        self.previous = previous
        self.played = []

    def getCurrentlyPlayingServiceOrGroup(self):
        return self.previous

    def playService(self, ref):
        self.played.append(ref)


class Session:
    def __init__(self, fail=False):
        self.nav = Nav()
        self.callback = None
        self.opts = None
        self.fail = fail

    def openWithCallback(self, callback, player, ref, **kwargs):
        self.callback = callback
        self.opts = (player, ref, kwargs)
        self.nav.playService(ref)
        if self.fail:
            raise RuntimeError("simulate failed Enigma2 player")
        return "dialog"


def import_player():
    enigma = types.ModuleType("enigma")
    enigma.eServiceReference = ServiceRef
    screens = types.ModuleType("Screens")
    screens.__path__ = []
    infobar = types.ModuleType("Screens.InfoBar")
    infobar.MoviePlayer = type("MoviePlayer", (), {})
    spec = importlib.util.spec_from_file_location("warder_player_test", str(PLAYER))
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, {"enigma": enigma, "Screens": screens, "Screens.InfoBar": infobar}):
        spec.loader.exec_module(module)
    return module


class PlayerTests(unittest.TestCase):
    def test_restores_previous_service_after_exit(self):
        module = import_player()
        s = Session()
        events = []
        dialog = module.open_player(s, "https://media.googlevideo.com/abc", "A title",
                                    on_close=lambda *a: events.append(a))
        self.assertEqual(dialog, "dialog")
        screen, ref, options = s.opts
        self.assertEqual(ref.service_type, 4097)
        self.assertEqual(ref.title, "A title")
        self.assertFalse(options["fromMovieSelection"])
        self.assertEqual(len(s.nav.played), 1)
        self.assertIs(s.nav.played[0], ref)
        s.callback("closed")
        self.assertEqual(s.nav.played[-1], "previous TV reference")
        self.assertEqual(events, [("closed",)])

    def test_restore_when_no_explicit_callback(self):
        module = import_player()
        s = Session()
        module.open_player(s, "https://media.googlevideo.com/abc", "Video")
        s.callback()
        self.assertEqual(s.nav.played[-1], "previous TV reference")

    def test_restore_if_player_start_fails(self):
        module = import_player()
        s = Session(fail=True)
        with self.assertRaises(RuntimeError):
            module.open_player(s, "https://media.googlevideo.com/abc", "Video")
        self.assertEqual(s.nav.played[-1], "previous TV reference")


if __name__ == "__main__":
    unittest.main()
