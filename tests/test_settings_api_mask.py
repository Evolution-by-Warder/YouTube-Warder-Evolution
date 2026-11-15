"""Visible draft / masked saved YouTube API key behavior on mocked Enigma2."""
import importlib.util
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType, SimpleNamespace
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class Widget:
    def __init__(self, text=""):
        self.text = text
    def setText(self, text):
        self.text = text


class ConfigValue:
    def __init__(self, value=""):
        self.value = value
        self.saves = 0
    def save(self):
        self.saves += 1


class ConfigFile:
    def __init__(self):
        self.saves = 0
    def save(self):
        self.saves += 1


class FakeScreen(dict):
    def __init__(self, session):
        super().__init__()
        self.session = session
    def close(self, *args):
        pass


class FakeSession:
    def __init__(self):
        self.dialogs = []
    def openWithCallback(self, callback, klass, *args, **kwargs):
        self.dialogs.append((callback, klass, args, kwargs))
    def answer(self, value):
        self.dialogs[-1][0](value)


def make_module(name, **items):
    result = ModuleType(name)
    for key, val in items.items():
        setattr(result, key, val)
    return result


@contextmanager
def environment(configured="", file_key="", advanced=False):
    api_key = ConfigValue(configured)
    quality = ConfigValue("720")
    cfg = SimpleNamespace(plugins=SimpleNamespace(warderyoutube=SimpleNamespace(
        api_key=api_key, max_quality=quality)))
    cfgfile = ConfigFile()
    fake_confirm = type("FakeConfirm", (), {})
    fake_system_keyboard = type("FakeSystemKeyboard", (), {})
    fake_fallback_keyboard = type("FakeWarderKeyboard", (), {})
    package = make_module("_warder_settings_test")
    package.__path__ = [str(ROOT)]
    components = make_module("Components")
    components.__path__ = []
    screens = make_module("Screens")
    screens.__path__ = []
    modules = {
        "_warder_settings_test.header_ui": make_module("_warder_settings_test.header_ui", add_header=lambda sc: sc.__setitem__("hdr_version", Widget())),
        "_warder_settings_test": package,
        "_warder_settings_test.skin": make_module(
            "_warder_settings_test.skin", SETTINGS_SKIN="<screen/>"),
        "_warder_settings_test.resolver": make_module(
            "_warder_settings_test.resolver", is_available=lambda: True),
        "_warder_settings_test.i18n": make_module(
            "_warder_settings_test.i18n", tr=lambda t: t),
        "_warder_settings_test.confirm_ui": make_module(
            "_warder_settings_test.confirm_ui", WarderYouTubeConfirm=fake_confirm),
        "_warder_settings_test.api_key_file": make_module(
            "_warder_settings_test.api_key_file",
            read_manual_key=lambda: file_key,
            VALID_KEY=__import__("re").compile(r"^[A-Za-z0-9_-]{20,160}$")),
        "_warder_settings_test.keyboard": make_module(
            "_warder_settings_test.keyboard",
            WarderYouTubeKeyboard=fake_fallback_keyboard),
        "_warder_settings_test.native_keyboard": make_module(
            "_warder_settings_test.native_keyboard",
            WarderNativeSearchKeyboard=fake_system_keyboard),
        "Components": components,
        "Components.ActionMap": make_module(
            "Components.ActionMap", ActionMap=lambda *args, **kwargs: Widget()),
        "Components.Label": make_module("Components.Label", Label=Widget),
        "Components.config": make_module(
            "Components.config", ConfigSelection=lambda **kw: ConfigValue(kw["default"]),
            ConfigSubsection=lambda: SimpleNamespace(), ConfigText=lambda **kw: ConfigValue(),
            config=cfg, configfile=cfgfile),
        "Screens": screens,
        "Screens.MessageBox": make_module("Screens.MessageBox", MessageBox=type("M", (), {})),
        "Screens.Screen": make_module("Screens.Screen", Screen=FakeScreen),
    }
    spec = importlib.util.spec_from_file_location(
        "_warder_settings_test.settings", ROOT / "settings.py")
    mod = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(mod)
        session = FakeSession()
        screen = mod.WarderYouTubeSettings(session)
        yield mod, screen, session, api_key, cfgfile, fake_confirm, fake_system_keyboard


class PlayerModeSettingsTests(unittest.TestCase):
    def test_yellow_cycles_available_players_and_persists(self):
        with environment(advanced=False) as (mod, screen, session, key, cfgfile, *_):
            self.assertEqual(mod.get_player_mode(), "auto")
            with patch.object(mod, "available_player_modes", return_value=("auto", "gst", "exte")):
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "gst")
                self.assertIn("gstplayer", screen["resolver_state"].text)
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "exte")
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "auto")
            self.assertEqual(cfgfile.saves, 3)
            self.assertFalse(hasattr(screen, '_advanced'))

    def test_missing_serviceapp_allows_preference_with_explicit_auto_fallback(self):
        with environment(advanced=False) as (mod, screen, session, key, cfgfile, *_):
            with patch.object(mod, "available_player_modes", return_value=("auto",)):
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "gst")
                self.assertIn("gstplayer", screen["resolver_state"].text)
                self.assertIn("Unavailable; using Automatic", screen["resolver_state"].text)
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "exte")
                self.assertIn("exteplayer3", screen["resolver_state"].text)
                screen.toggle_player()
                self.assertEqual(mod.get_player_mode(), "auto")
                self.assertNotIn("Unavailable; using Automatic", screen["resolver_state"].text)
            self.assertEqual(cfgfile.saves, 3)

class HiddenLegacyKeyTests(unittest.TestCase):
    OLD = "AIza" + "x" * 35

    def test_existing_key_kept_without_visible_editor(self):
        with environment(configured=self.OLD) as (mod, screen, session, key, cfgfile, *_):
            self.assertEqual(mod.get_api_key(), self.OLD)
            self.assertNotIn(self.OLD, " ".join(w.text for w in screen.values() if hasattr(w, "text")))
            self.assertFalse(any("API key" in w.text for w in screen.values() if hasattr(w, "text")))
            self.assertNotIn("menu", screen["actions"].mapping if hasattr(screen["actions"], "mapping") else {})
            self.assertFalse(hasattr(screen, "prompt_key"))
            self.assertFalse(hasattr(screen, "toggle_advanced"))
            self.assertEqual(cfgfile.saves, 0)

    def test_old_manual_file_still_works_as_fallback(self):
        with environment(file_key=self.OLD) as (mod, screen, session, key, cfgfile, *_):
            self.assertEqual(mod.get_api_key(), self.OLD)
            self.assertEqual(key.value, "")
            self.assertFalse(hasattr(screen, "clear_key"))


if __name__ == "__main__":
    unittest.main()
