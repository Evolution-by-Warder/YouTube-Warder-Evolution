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
        self.visible = False
    def setText(self, value):
        self.value = value
    def setValue(self, value):
        self.value = value
    def show(self):
        self.visible = True
    def hide(self):
        self.visible = False


class Home:
    def __init__(self):
        self.index = 6
        self.installed_version = "0.0.8~test59"
        self._busy = False
        self.details = []
        self.items = {k: Label() for k in ("key_green", "key_yellow",
                                          "key_blue", "key_red", "version", "status",
                                          "update_progress", "update_no", "update_yes",
                                          "update_no_focus", "update_yes_focus")}
        self.session = Session()
    def __getitem__(self, key):
        return self.items[key]
    def _show_details(self, rows):
        self.details = rows
    def _hide_update_widgets(self):
        for key in ("update_progress", "update_no", "update_yes",
                    "update_no_focus", "update_yes_focus"):
            self.items[key].hide()


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


class InlineConfirmationAppearanceTests(unittest.TestCase):
    def test_selected_word_has_no_filled_selection_bar(self):
        import ast
        import xml.etree.ElementTree as ET
        source = (PATH.parent / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        skin = next(ast.literal_eval(assign.value) for assign in tree.body
                    if isinstance(assign, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "HOME_SKIN"
                            for t in assign.targets))
        widgets = {w.attrib.get("name"): w.attrib
                   for w in ET.fromstring(skin).findall("widget")}
        for name in ("update_no_focus", "update_yes_focus"):
            widget = widgets[name]
            self.assertEqual(widget["transparent"], "1")
            self.assertEqual(widget["font"], "Regular;32")
            self.assertEqual(widget["size"], "555,50")
            self.assertEqual(widget["foregroundColor"], "#32DFFF")
            self.assertNotIn("backgroundColor", widget)

    def test_confirmation_yes_left_no_right_below_prompt_above_footer(self):
        import ast
        import xml.etree.ElementTree as ET
        source = (PATH.parent / "skin.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        skin = next(ast.literal_eval(assign.value) for assign in tree.body
                    if isinstance(assign, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "HOME_SKIN"
                            for t in assign.targets))
        widgets = {w.get("name"): w for w in ET.fromstring(skin).findall("widget")}
        for name in ("update_yes", "update_yes_focus"):
            self.assertEqual(widgets[name].get("position"), "483,665")
        for name in ("update_no", "update_no_focus"):
            self.assertEqual(widgets[name].get("position"), "1088,665")
        prompt_top = int(widgets["detail3"].get("position").split(",")[1])
        options_top = int(widgets["update_yes"].get("position").split(",")[1])
        hint_top = int(widgets["status"].get("position").split(",")[1])
        self.assertLess(prompt_top, options_top)
        self.assertLess(options_top, hint_top)


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
        self.assertEqual(len(home.session.dialogs), 0)
        self.assertTrue(controller.confirming)
        self.assertFalse(controller.confirm_yes)
        self.assertTrue(home["update_no_focus"].visible)
        self.assertIn("Confirm update:", home.details[3])
        self.assertEqual(home.details[5], "")
        self.assertIn("Arrows: select", home["status"].value)
        self.assertFalse(home["update_no"].visible)
        self.assertTrue(home["update_yes"].visible)
        controller.answer(False)
        self.assertEqual(len(jobs), 1)
        self.assertFalse(home._busy)

    def test_actual_enigma_widgets_move_not_just_skin_xml(self):
        mod, jobs, fakes = load()
        home = Home()
        class Native:
            def __init__(self):
                self.point = None
            def move(self, point):
                self.point = (point.x, point.y)
        class Point:
            def __init__(self, x, y):
                self.x, self.y = x, y
        for name in ("detail3", "update_yes", "update_yes_focus",
                     "update_no", "update_no_focus", "status"):
            if name not in home.items:
                home.items[name] = Label()
            home.items[name].instance = Native()
        controller = mod.InlineUpdater(home)
        controller.release = release()
        with patch.object(fakes["enigma"], "ePoint", Point, create=True):
            controller.confirm()
        self.assertEqual(home["detail3"].instance.point, (449, 565))
        self.assertEqual(home["update_yes"].instance.point, (483, 665))
        self.assertEqual(home["update_yes_focus"].instance.point, (483, 665))
        self.assertEqual(home["update_no"].instance.point, (1088, 665))
        self.assertEqual(home["update_no_focus"].instance.point, (1088, 665))
        self.assertEqual(home["status"].instance.point, (427, 939))
        self.assertTrue(home["update_no_focus"].visible)
        self.assertFalse(home["update_yes_focus"].visible)
        controller.select(True)
        self.assertTrue(home["update_yes_focus"].visible)
        self.assertFalse(home["update_no_focus"].visible)

    def test_confirmation_text_order_and_status_clear_when_cancelled(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.release = release()
        controller.confirm()
        self.assertEqual(home.details[2], "New version available")
        self.assertEqual(home.details[3],
                         "Confirm update: 0.0.8~test60")
        self.assertEqual(home.details[5], "")
        self.assertEqual(home["status"].value,
                         "Arrows: select · OK: confirm · EXIT: cancel")
        self.assertTrue(home["update_no_focus"].visible)
        self.assertFalse(home["update_yes_focus"].visible)
        controller.select(True)
        self.assertTrue(home["update_yes_focus"].visible)
        controller.answer(False)
        self.assertEqual(home["status"].value, "")
        self.assertFalse(controller.installing)
        self.assertEqual(jobs, [])

    def test_checked_without_release_reports_up_to_date_and_retry_resets(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.check()
        self.assertTrue(controller.checking)
        self.assertFalse(controller.checked)
        jobs[0][3].success(("0.0.8~test65", None))
        self.assertTrue(controller.checked)
        self.assertFalse(controller.checking)
        self.assertEqual(home.details[2], "You are up to date.")
        self.assertEqual(home.session.dialogs, [])
        controller.check()
        self.assertFalse(controller.checked)
        self.assertTrue(controller.checking)
        jobs[1][3].failure(types.SimpleNamespace(value=RuntimeError("offline")))
        self.assertFalse(controller.checked)
        self.assertIn("failed", home.details[2])
        controller.check()
        jobs[2][3].success(("0.0.8~test65", release()))
        self.assertTrue(controller.checked)
        self.assertIn("New version available", home.details[2])

    def test_install_updates_in_place_then_gui_only_restart(self):
        mod, jobs, fakes = load()
        home = Home()
        controller = mod.InlineUpdater(home)
        controller.release = release()
        controller.confirm()
        self.assertEqual(home.session.dialogs, [])
        self.assertTrue(home["update_no_focus"].visible)
        controller.select(True)
        self.assertTrue(home["update_yes_focus"].visible)
        self.assertFalse(home["update_yes"].visible)
        self.assertTrue(home["update_no"].visible)
        controller.answer(True)
        self.assertTrue(controller.installing)
        self.assertTrue(home._busy)
        self.assertEqual(len(jobs), 1)
        progress = jobs[0][2]["progress"]
        progress("download", 250, 1000)
        self.assertIn("25%", home.details)
        self.assertEqual(home["update_progress"].value, 25)
        self.assertTrue(home["update_progress"].visible)
        progress("verify")
        self.assertIn("SHA256", home.details[2])
        self.assertEqual(home.details[4], "Download finished: 100%")
        progress("install")
        self.assertIn("opkg", home.details[2])
        self.assertEqual(home.session.opens, [])
        self.assertEqual(home["update_progress"].value, 25)
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
        controller.select(True)
        controller.answer(True)
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
