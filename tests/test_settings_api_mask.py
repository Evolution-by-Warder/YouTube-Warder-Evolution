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
def environment(configured="", file_key="", advanced=True):
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
        if advanced:
            screen.toggle_advanced()
        yield mod, screen, session, api_key, cfgfile, fake_confirm, fake_system_keyboard


class MaskedKeyTests(unittest.TestCase):
    OLD = "AIza" + "x" * 35
    NEW = "AIza" + "y" * 35

    def test_key_delete_is_explicitly_about_saved_api_key(self):
        with environment(configured=self.OLD) as (mod, screen, session, key, cfgfile, confirm, keyboard):
            self.assertEqual(screen["key_yellow"].text, "Delete API key")
            self.assertIn("delete API key", screen["footer"].text if "footer" in screen else screen["status"].text)
            screen.confirm_clear()
            self.assertEqual(len(session.dialogs), 1)
            self.assertIs(session.dialogs[-1][1], confirm)
            self.assertEqual(session.dialogs[-1][2][0], "Delete saved API key?")
            session.answer(False)
            self.assertEqual(key.value, self.OLD)

    def test_saved_key_stays_masked_and_requires_explicit_change(self):
        with environment(configured=self.OLD) as (mod, screen, session, key, cfgfile, confirm, keyboard):
            self.assertIn("********", screen["key_state"].text)
            self.assertEqual(screen["key_green"].text, "Change API key")
            self.assertNotIn(self.OLD, screen["key_state"].text)
            screen.prompt_key()
            self.assertEqual(len(session.dialogs), 1)
            self.assertIs(session.dialogs[-1][1], confirm)
            self.assertIn("********", session.dialogs[-1][2][0])
            self.assertNotIn(self.OLD, session.dialogs[-1][2][0])
            screen.prompt_key()
            self.assertEqual(len(session.dialogs), 1)
            session.answer(False)
            self.assertEqual(key.value, self.OLD)
            self.assertEqual(cfgfile.saves, 0)
            screen.prompt_key()
            session.answer(True)
            self.assertIs(session.dialogs[-1][1], keyboard)
            self.assertEqual(session.dialogs[-1][3]["value"], "")
            self.assertFalse(session.dialogs[-1][3]["secret"])
            session.answer(None)
            self.assertEqual(key.value, self.OLD)
            self.assertEqual(cfgfile.saves, 0)

    def test_edited_key_saves_only_on_confirmation_and_is_masked_after(self):
        with environment(configured=self.OLD) as (mod, screen, session, key, cfgfile, confirm, keyboard):
            screen.prompt_key()
            session.answer(True)
            self.assertEqual(key.value, self.OLD)
            session.answer(self.NEW)
            self.assertEqual(key.value, self.NEW)
            self.assertEqual(key.saves, 1)
            self.assertEqual(cfgfile.saves, 1)
            self.assertIn("********", screen["key_state"].text)
            self.assertEqual(screen["key_green"].text, "Change API key")
            self.assertNotIn(self.NEW, screen["key_state"].text)
            self.assertNotIn(self.OLD, screen["key_state"].text)

    def test_new_key_is_visible_only_during_first_edit(self):
        with environment() as (mod, screen, session, key, cfgfile, confirm, keyboard):
            self.assertEqual(screen["key_green"].text, "API key")
            screen.prompt_key()
            self.assertEqual(len(session.dialogs), 1)
            self.assertIs(session.dialogs[-1][1], keyboard)
            self.assertEqual(session.dialogs[-1][3]["value"], "")
            self.assertFalse(session.dialogs[-1][3]["secret"])
            session.answer(self.NEW)
            self.assertEqual(key.value, self.NEW)
            self.assertIn("********", screen["key_state"].text)

    def test_manually_supplied_file_is_masked_and_cancel_keeps_it(self):
        with environment(file_key=self.OLD) as (mod, screen, session, key, cfgfile, confirm, keyboard):
            self.assertEqual(mod.get_api_key(), self.OLD)
            self.assertIn("********", screen["key_state"].text)
            self.assertNotIn(self.OLD, screen["key_state"].text)
            screen.prompt_key()
            self.assertIs(session.dialogs[-1][1], confirm)
            session.answer(False)
            self.assertEqual(key.value, "")
            self.assertEqual(mod.get_api_key(), self.OLD)
            self.assertEqual(cfgfile.saves, 0)
            screen.prompt_key()
            session.answer(True)
            session.answer(self.NEW)
            self.assertEqual(mod.get_api_key(), self.NEW)

    def test_invalid_replacement_does_not_overwrite_old_key(self):
        with environment(configured=self.OLD) as (mod, screen, session, key, cfgfile, confirm, keyboard):
            screen.prompt_key()
            session.answer(True)
            session.answer("too short")
            self.assertEqual(key.value, self.OLD)
            self.assertEqual(cfgfile.saves, 0)
            self.assertIn("Invalid", screen["status"].text)
            self.assertNotIn(self.OLD, screen["status"].text)


if __name__ == "__main__":
    unittest.main()
