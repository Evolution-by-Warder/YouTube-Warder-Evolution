"""TV device login remains inside the right pane, never opens a modal."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = (Path(__file__).resolve().parents[1] /
        "plugin/Plugins/Extensions/WarderYouTube")


class Deferred:
    def addCallbacks(self, success, failure):
        self.success, self.failure = success, failure


class Timer:
    def __init__(self):
        self.callbacks = []
        self.timeout = types.SimpleNamespace(get=lambda: self.callbacks)
        self.ms = None
        self.stopped = False
    def start(self, ms, once):
        self.ms = ms
    def stop(self):
        self.stopped = True
    def fire(self):
        for callback in list(self.callbacks):
            callback()


class Home(dict):
    def __init__(self):
        self._disposed = False
        self.index = 2
        self.messages = []
        self.details = []
        self.connected = False
        self["status"] = types.SimpleNamespace(setText=lambda text: self.messages.append(text))
    def _show_message(self, value):
        self.messages.append(value)
    def _show_details(self, lines):
        self.details.append(list(lines))
    def _render_categories(self):
        return
    def _subscription_login_ready(self):
        self.connected = True


def load():
    tasks = []
    timers = []
    def worker(*args):
        deferred = Deferred()
        tasks.append((args, deferred))
        return deferred
    def timer_factory():
        timer = Timer()
        timers.append(timer)
        return timer
    def mod(name, **items):
        result = types.ModuleType(name)
        for key, value in items.items():
            setattr(result, key, value)
        return result
    package = mod("_home_tv_test")
    package.__path__ = [str(ROOT)]
    modules = {
        "_home_tv_test": package,
        "_home_tv_test.i18n": mod("_home_tv_test.i18n", tr=lambda text: text),
        "_home_tv_test.subscriptions_auth": mod(
            "_home_tv_test.subscriptions_auth",
            read_client=lambda: {},
            request_device_code=lambda credentials: {},
            poll_device_code=lambda client, code: None,
            save_tokens=lambda tokens: None),
        "twisted": mod("twisted"),
        "twisted.internet": mod("twisted.internet"),
        "twisted.internet.threads": mod("twisted.internet.threads",
                                         deferToThread=worker),
        "enigma": mod("enigma", eTimer=timer_factory),
    }
    modules["twisted"].__path__ = []
    modules["twisted.internet"].__path__ = []
    spec = importlib.util.spec_from_file_location(
        "_home_tv_test.home_tv_auth", ROOT / "home_tv_auth.py")
    target = importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules, modules):
        spec.loader.exec_module(target)
    return target, tasks, timers, modules


class InlineLoginTests(unittest.TestCase):
    def test_login_shows_code_in_right_pane_and_saves_only_in_worker(self):
        code = {
            "device_code": "secret-private-device-code",
            "user_code": "A1-B2-C3", "verification_url": "https://google.com/device",
            "expires_in": 600, "interval": 5
        }
        mod, tasks, timers, modules = load()
        home = Home()
        with patch.dict(sys.modules, {"enigma": modules["enigma"]}):
            login = mod.HomeTVLogin(home)
            login.start()
            self.assertEqual(len(tasks), 1)
            self.assertIn("Google TV", home.messages[-1])
            tasks[0][1].success(({"client_id": "private"}, code))
            self.assertEqual(len(timers), 1)
            self.assertIn("A1-B2-C3", home.details[0])
            self.assertEqual(timers[0].ms, 5000)
            timers[0].fire()
            self.assertEqual(len(tasks), 2)
            self.assertEqual(tasks[1][0][1], {"client_id": "private"})
            tasks[1][1].success(("connected", {"access_token": "private-access",
                                               "refresh_token": "private-refresh"}))
            self.assertEqual(len(tasks), 3)
            self.assertEqual(tasks[2][0][0].__name__, "<lambda>" if False else "save_tokens")
            tasks[2][1].success(None)
            self.assertTrue(home.connected)
            self.assertTrue(login.closed)
            self.assertTrue(timers[0].stopped)
            self.assertEqual(timers[0].callbacks, [])

    def test_aborted_login_does_not_reuse_expired_device_callback(self):
        mod, tasks, timers, modules = load()
        home = Home()
        login = mod.HomeTVLogin(home)
        login.start()
        login.close()
        tasks[0][1].success(({}, {"device_code": "bad"}))
        self.assertEqual(home.details, [])
        self.assertFalse(home.connected)
        self.assertTrue(login.closed)


if __name__ == "__main__":
    unittest.main()
