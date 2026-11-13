"""Mocked Enigma2 updater lifecycle tests: no receiver, network or opkg side effects."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

UI = (Path(__file__).resolve().parents[1] /
      "plugin/Plugins/Extensions/WarderYouTube/update_ui.py")


class Widget:
    def __init__(self, text=""):
        self.text = text
        self.value = 0

    def setText(self, value):
        self.text = value

    def setValue(self, value):
        self.value = value


class Screen(dict):
    def __init__(self, session):
        self.session = session
        self.onShown = []
        self.onClose = []
        self.closed = False

    def close(self):
        self.closed = True
        for callback in self.onClose:
            callback()


class Timer:
    def __init__(self):
        self.callback = []
        self.started = None
        self.stopped = False

    def start(self, milliseconds, single_shot):
        self.started = (milliseconds, single_shot)

    def stop(self):
        self.stopped = True


class Deferred:
    def addCallbacks(self, success, failure):
        self.success = success
        self.failure = failure
        return self


class Session:
    def __init__(self):
        self.modal_calls = []
        self.opens = []

    def openWithCallback(self, callback, cls, *args, **kwargs):
        self.modal_calls.append((callback, cls, args, kwargs))

    def open(self, cls, *args, **kwargs):
        self.opens.append((cls, args, kwargs))


class SafeUpdateError(Exception):
    pass


def make_module(name, **attrs):
    m = types.ModuleType(name)
    for key, value in attrs.items():
        setattr(m, key, value)
    return m


def load_updater():
    background = []
    def submit(function, *args, **kwargs):
        deferred = Deferred()
        background.append((function, args, kwargs, deferred))
        return deferred

    parent = make_module("_mock_warder_updates")
    parent.__path__ = [str(UI.parent)]
    label = Widget
    progress = Widget
    shutdown = type("TryQuitMainloop", (), {})
    fake = {
        "_mock_warder_updates.header_ui": make_module("_mock_warder_updates.header_ui", add_header=lambda sc: sc.__setitem__("hdr_version", Widget())),
        "enigma": make_module("enigma", eTimer=Timer),
        "Components": make_module("Components"),
        "Components.ActionMap": make_module(
            "Components.ActionMap", ActionMap=lambda *a, **k: object()
        ),
        "Components.Label": make_module("Components.Label", Label=label),
        "Components.ProgressBar": make_module("Components.ProgressBar", ProgressBar=progress),
        "Screens": make_module("Screens"),
        "Screens.Screen": make_module("Screens.Screen", Screen=Screen),
        "Screens.MessageBox": make_module(
            "Screens.MessageBox", MessageBox=type(
                "MessageBox", (), {"TYPE_YESNO": 0}
            )
        ),
        "Screens.Standby": make_module("Screens.Standby", TryQuitMainloop=shutdown),
        "twisted": make_module("twisted"),
        "twisted.internet": make_module("twisted.internet", reactor=types.SimpleNamespace(
            callFromThread=lambda fn, *a: fn(*a)
        )),
        "twisted.internet.threads": make_module(
            "twisted.internet.threads", deferToThread=submit
        ),
        "_mock_warder_updates": parent,
        "_mock_warder_updates.skin": make_module(
            "_mock_warder_updates.skin", UPDATE_SKIN="<screen/>",
            UPDATE_CHECK_SKIN="<screen/>"
        ),
        "_mock_warder_updates.i18n": make_module(
            "_mock_warder_updates.i18n", tr=lambda value: value
        ),
        "_mock_warder_updates.confirm_ui": make_module(
            "_mock_warder_updates.confirm_ui", WarderYouTubeConfirm=object
        ),
        "_mock_warder_updates.update_core": make_module(
            "_mock_warder_updates.update_core",
            install_update=lambda *args, **kwargs: "0.0.8~test6",
            check_update=lambda *args, **kwargs: None,
            CURRENT_VERSION="0.0.8~test5",
            UpdateError=SafeUpdateError,
        ),
    }
    fake["Components"].__path__ = []
    fake["Screens"].__path__ = []
    fake["twisted"].__path__ = []
    fake["twisted.internet"].__path__ = []
    spec = importlib.util.spec_from_file_location(
        "_mock_warder_updates.update_ui", str(UI)
    )
    obj = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, fake):
        spec.loader.exec_module(obj)
    return obj, background, shutdown


def sample_release():
    return {
        "version": "0.0.8~test6",
        "url": ("https://github.com/Evolution-by-Warder/"
                "YouTube-Warder-Evolution/releases/download/"
                "youtube-warder-v0.0.8-test6/"
                "enigma2-plugin-extensions-youtube-warder-evolution_0.0.8.test6_all.ipk"),
        "notes": "Test6 for owner testing",
    }


class UpdateUiTests(unittest.TestCase):
    def test_check_runs_only_once_and_current_version_does_not_install(self):
        ui, jobs, shutdown = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateCheck(session)
        for callback in screen.onShown + screen.onShown:
            callback()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0][1], ())
        self.assertIs(jobs[0][0], ui.check_actual_installed_version)
        self.assertEqual(session.opens, [])
        jobs[0][3].success(("0.0.8~test13", None))
        self.assertEqual(screen["hdr_version"].text, "0.0.8~test13")
        self.assertIn("test13", screen["detail"].text)
        self.assertIn("najnovšiu", screen["status"].text)
        screen.ask_install()
        self.assertEqual(session.modal_calls, [])

    def test_explicit_confirmation_required_before_install_screen(self):
        ui, jobs, _ = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateCheck(session)
        screen.found(sample_release())
        screen.ask_install()
        screen.ask_install()  # double OK/green cannot open another confirmation
        self.assertEqual(len(session.modal_calls), 1)
        callback = session.modal_calls[0][0]
        callback(False)
        self.assertEqual(session.opens, [])
        callback(True)  # stale duplicate confirmation cannot install
        self.assertEqual(len(session.modal_calls), 1)
        screen.ask_install()
        self.assertEqual(len(session.modal_calls), 2)
        session.modal_calls[-1][0](True)
        self.assertEqual(len(session.modal_calls), 3)
        self.assertIs(session.modal_calls[-1][1], ui.WarderYouTubeUpdateProgress)
        self.assertEqual(session.modal_calls[-1][2][0]["version"], "0.0.8~test6")
        screen.ask_install()  # progress dialog already open; no second install
        screen.install_confirmed(True)
        self.assertEqual(len(session.modal_calls), 3)
        session.modal_calls[-1][0]()  # progress window closed
        self.assertFalse(screen.install_started)
        screen.ask_install()  # now a future retry can ask again
        self.assertEqual(len(session.modal_calls), 4)

    def test_updater_confirmation_open_error_fails_without_install(self):
        ui, jobs, _ = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateCheck(session)
        screen.found(sample_release())
        session.openWithCallback = lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("Secret URL"))
        screen.ask_install()
        self.assertFalse(screen.confirmation_open)
        self.assertFalse(screen.install_started)
        self.assertNotIn("Secret", screen["status"].text)

    def test_closed_check_rejects_late_worker_and_confirmation(self):
        ui, jobs, _ = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateCheck(session)
        screen.begin_once()
        screen.close()
        jobs[0][3].success(sample_release())
        self.assertIsNone(screen.release)
        screen.install_confirmed(True)
        self.assertEqual(session.opens, [])

    def test_progress_never_restarts_until_success(self):
        ui, jobs, shutdown = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateProgress(session, sample_release())
        for callback in screen.onShown + screen.onShown:
            callback()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(session.opens, [])
        progress = jobs[0][2]["progress"]
        progress("download", 25, 100)
        self.assertEqual(screen["progress"].value, 25)
        self.assertEqual(screen["percentage"].text, "25%")
        progress("verify")
        progress("install")
        self.assertEqual(session.opens, [])
        jobs[0][3].success("0.0.8~test6")
        self.assertEqual(screen.restart_timer.started, (3000, True))
        self.assertEqual(screen["progress"].value, 100)
        screen.restart_gui()
        self.assertEqual(session.opens, [(shutdown, (3,), {})])

    def test_failed_install_never_restarts_and_allows_exit(self):
        ui, jobs, _ = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateProgress(session, sample_release())
        screen.begin_once()
        secret = "https://rr1.googlevideo.com/?sig=private"
        jobs[0][3].failure(types.SimpleNamespace(value=RuntimeError(secret)))
        self.assertTrue(screen.failed)
        self.assertEqual(session.opens, [])
        self.assertNotIn("private", screen["detail"].text)
        screen.restart_gui()
        self.assertEqual(session.opens, [])
        screen.exit_failed()
        self.assertTrue(screen.closed)
        self.assertTrue(screen.restart_timer.stopped)

    def test_disposed_progress_rejects_late_success_or_download(self):
        ui, jobs, _ = load_updater()
        session = Session()
        screen = ui.WarderYouTubeUpdateProgress(session, sample_release())
        screen.begin_once()
        screen.close()
        jobs[0][2]["progress"]("download", 100, 100)
        jobs[0][3].success("0.0.8~test6")
        self.assertIsNone(screen.restart_timer.started)
        self.assertEqual(session.opens, [])


if __name__ == "__main__":
    unittest.main()
