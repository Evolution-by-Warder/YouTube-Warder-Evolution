"""Inline update regression tests: right pane, no separate update dialog."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

PATH = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube/inline_update.py")


class Label:
    def __init__(self):
        self.value = ""
    def setText(self, value):
        self.value = value


class Home:
    def __init__(self):
        self.index = 6
        self.installed_version = "0.0.8~test59"
        self._busy = False
        self.details = []
        self.items = {k: Label() for k in ("key_green", "key_yellow",
                                          "key_blue", "key_red", "version")}
        self.session = Session()
    def __getitem__(self, key):
        return self.items[key]
    def _show_details(self, rows):
        self.details = rows


class Session:
    def __init__(self):
        self.dialogs = []
        self.opens = []
    def openWithCallback(self, fn, cls, *args):
        self.dialogs.append((fn, cls, args))
    def open(self, cls, *args):
        self.opens.append((cls, args))


class Deferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure


class Timer:
    def __init__(self):
        self.callback = []
        self.started = None
        self.stopped = False
    def start(self, delay, single_shot):
        self.started = (delay, single_shot)
    def stop(self):
        self.stopped = True


def load():
    parent = types.ModuleType("_inline_test")
    parent.__path__ = [str(PATH.parent)]
    runs = []
    def worker(fn, *args, **kwargs):
        d = Deferred()
        runs.append((fn, args, kwargs, d))
        return d
    fake = {
        "_inline_test": parent,
        "_inline_test.i18n": types.SimpleNamespace(tr=lambda value: value),
        "_inline_test.update_core": types.SimpleNamespace(
            check_update=lambda version: None, install_update=lambda *a, **k: None,
            UpdateError=ValueError),
        "_inline_test.installed_version": types.SimpleNamespace(
            read_installed_version=lambda: "0.0.8~test59"),
        "_inline_test.confirm_ui": types.SimpleNamespace(
            WarderYouTubeConfirm=object),
        "twisted": types.ModuleType("twisted"),
        "twisted.internet": types.ModuleType("twisted.internet"),
        "twisted.internet.threads": types.SimpleNamespace(deferToThread=worker),
        "enigma": types.SimpleNamespace(eTimer=Timer),
        "Screens": types.ModuleType("Screens"),
        "Screens.Standby": types.SimpleNamespace(TryQuitMainloop=object),
    }
    fake["twisted"].__path__ = []
    fake["twisted.internet"].__path__ = []
    fake["twisted.internet"].reactor = types.SimpleNamespace(
        callFromThread=lambda fn, *args: fn(*args))
    fake["Screens"].__path__ = []
    spec = importlib.util.spec_from_file_location("_inline_test.inline_update", PATH)
    module = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(module)
    # Imports inside confirm(), _installed() and _restart_gui() are lazy.
    # Keep test-only module names accessible for those callback invocations.
    for name in ("_inline_test", "_inline_test.confirm_ui", "enigma",
                 "Screens", "Screens.Standby"):
        sys.modules[name] = fake[name]
    return module, runs, fake


def release():
    return {"version": "0.0.8~test60", "notes": "New updater in right pane"}


class InlineUpdateTests(unittest.TestCase):
    def test_check_rendered_in_right_pane_and_no_install_without_confirmation(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.show()
        self.assertIn("test59", home.details[0])
        controller.activate()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(home.session.dialogs, [])
        self.assertEqual(home.session.opens, [])
        jobs[0][3].success(("0.0.8~test59", release()))
        self.assertIn("test60", home.details[1])
        self.assertEqual(home["key_green"].value, "Install")
        controller.activate()
        self.assertEqual(len(home.session.dialogs), 1)
        home.session.dialogs[-1][0](False)
        self.assertEqual(len(jobs), 1)
        self.assertFalse(home._busy)

    def test_install_updates_in_place_then_gui_only_restart(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.release = release()
        controller.confirm()
        home.session.dialogs[-1][0](True)
        self.assertTrue(controller.installing)
        self.assertTrue(home._busy)
        self.assertEqual(len(jobs), 1)
        progress = jobs[0][2]["progress"]
        progress("download", 250, 1000)
        self.assertIn("25%", home.details)
        progress("verify")
        self.assertIn("SHA256", home.details[2])
        progress("install")
        self.assertIn("opkg", home.details[2])
        self.assertEqual(home.session.opens, [])
        jobs[0][3].success("0.0.8~test60")
        self.assertTrue(controller.completed)
        self.assertEqual(controller._restart_timer.started, (3000, True))
        self.assertEqual(home.session.opens, [])
        with patch.dict(sys.modules, {"Screens": fakes["Screens"],
                                       "Screens.Standby": fakes["Screens.Standby"]}):
            controller._restart_timer.callback[0]()
        self.assertEqual(home.session.opens, [(object, (3,))])

    def test_install_failure_unlocks_controls_without_gui_restart(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.release = release()
        controller.confirm()
        home.session.dialogs[-1][0](True)
        jobs[0][3].failure(types.SimpleNamespace(value=RuntimeError("SENSITIVE")))
        self.assertFalse(controller.installing)
        self.assertFalse(home._busy)
        self.assertEqual(home.session.opens, [])
        self.assertNotIn("SENSITIVE", " ".join(home.details))
        controller._restart_gui()
        self.assertEqual(home.session.opens, [])

    def test_ignored_old_check_after_navigating_away(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.check()
        controller.leave()
        home.index = 0
        jobs[0][3].success(("0.0.8~test59", release()))
        self.assertIsNone(controller.release)
        self.assertFalse(controller.checking)

    def test_dispose_never_restarts_or_opens_dialog(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.check()
        controller.close()
        jobs[0][3].success(("0.0.8~test59", release()))
        self.assertEqual(home.session.opens, [])
        self.assertEqual(home.session.dialogs, [])


if __name__ == "__main__":
    unittest.main()
