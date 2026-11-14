# -*- coding: utf-8 -*-
"""Google TV-device login inside the SAME right pane as Home / Odbery.

No passwords, private OAuth client credentials or bearer tokens are shown.
Device verification code is displayed only in memory, never logged or shipped
in the IPK. Blocking OAuth calls and disk writes run in Twisted workers;
eTimer polls only at the interval returned by Google.
"""
from time import monotonic
from twisted.internet.threads import deferToThread

from .i18n import tr as _
from .subscriptions_auth import (read_client, request_device_code,
                                 poll_device_code, save_tokens)


def _device_request():
    client = read_client()
    return client, request_device_code(client)


class HomeTVLogin:
    def __init__(self, home):
        self.home = home
        self.active = False
        self.closed = False
        self.epoch = 0
        self.client = None
        self.device = None
        self.deadline = 0
        self.interval = 5
        self.polling = False
        self.timer = None
        self.connection = None
        self.signal = None

    def start(self):
        if self.closed or self.home._disposed:
            return
        if self.active:
            self.show_details()
            return
        self.active = True
        self.epoch += 1
        epoch = self.epoch
        self.home._show_message("Requesting a secure Google TV login code…")
        try:
            worker = deferToThread(_device_request)
            worker.addCallbacks(
                lambda data: self._code_ready(epoch, data),
                lambda err: self._failed(epoch,
                    "Google TV OAuth client not configured or login unavailable.")
            )
        except Exception:
            self._failed(epoch, "YouTube TV login is unavailable.")

    def _code_ready(self, epoch, data):
        if not self._current(epoch):
            return
        try:
            self.client, self.device = data
            self.interval = max(5, int(self.device["interval"]))
            self.deadline = monotonic() + int(self.device["expires_in"])
        except (TypeError, KeyError, ValueError):
            self._failed(epoch, "Google did not return a usable TV code.")
            return
        self.show_details()
        try:
            from enigma import eTimer
            timer = eTimer()
            signal = timer.timeout
            if hasattr(signal, "get"):
                self.signal = signal.get()
                self.signal.append(self._poll)
            else:
                self.connection = signal.connect(self._poll)
            self.timer = timer
            self._schedule()
        except (ImportError, AttributeError, RuntimeError, TypeError):
            self._failed(epoch, "This receiver cannot poll YouTube TV login.")

    def show_details(self):
        if not self.active or self.closed or self.home._disposed:
            return
        if self.device:
            self.home._show_details([
                "YouTube / Google TV login",
                _("Open on your phone or PC:"),
                str(self.device["verification_url"]),
                _("Enter this code exactly:"),
                str(self.device["user_code"]),
                _("Then confirm read-only YouTube access in Google."),
            ])
            self.home["status"].setText(_("Waiting for Google account authorization…"))
        else:
            self.home._show_message("Requesting a secure Google TV login code…")

    def _current(self, epoch):
        return not self.closed and not self.home._disposed and epoch == self.epoch

    def _schedule(self):
        if not self.active or self.closed or self.device is None or not self.timer:
            return
        if monotonic() >= self.deadline:
            self._failed(self.epoch, "YouTube login code expired. Try connecting again.")
            return
        try:
            self.timer.start(int(self.interval) * 1000, True)
        except (RuntimeError, AttributeError, TypeError):
            self._failed(self.epoch, "YouTube TV login polling unavailable.")

    def _poll(self):
        if not self.active or self.closed or self.polling or self.device is None:
            return
        if monotonic() >= self.deadline:
            self._failed(self.epoch, "YouTube login code expired. Try connecting again.")
            return
        self.polling = True
        epoch = self.epoch
        client = dict(self.client)
        code = self.device["device_code"]
        try:
            task = deferToThread(poll_device_code, client, code)
            task.addCallbacks(lambda result: self._poll_ready(epoch, result),
                              lambda err: self._failed(epoch, "YouTube TV login failed."))
        except Exception:
            self._failed(epoch, "YouTube TV login is unavailable.")

    def _poll_ready(self, epoch, result):
        if not self._current(epoch):
            return
        self.polling = False
        state, tokens = result
        if state == "slow_down":
            self.interval = min(self.interval + 5, 60)
            self._schedule()
        elif state == "authorization_pending":
            self._schedule()
        elif state == "connected" and isinstance(tokens, dict):
            try:
                task = deferToThread(save_tokens, tokens)
                task.addCallbacks(lambda _: self._saved(epoch),
                                  lambda err: self._failed(epoch,
                                      "Could not save private YouTube account tokens."))
            except Exception:
                self._failed(epoch, "Could not save private YouTube account tokens.")
        else:
            self._failed(epoch, "YouTube TV login failed.")

    def _saved(self, epoch):
        if not self._current(epoch):
            return
        self.close()
        self.home["status"].setText(_("YouTube account connected."))
        self.home._subscription_login_ready()

    def _failed(self, epoch, message):
        if not self._current(epoch):
            return
        self.close()
        if self.home.index == 2:
            self.home._show_message(message)
            self.home._render_categories()

    def close(self):
        if self.closed:
            return
        self.closed = True
        self.active = False
        self.epoch += 1
        if self.timer is not None:
            try:
                self.timer.stop()
            except (RuntimeError, AttributeError, TypeError):
                pass
            self.timer = None
        if self.connection is not None:
            try:
                self.connection.disconnect()
            except (RuntimeError, AttributeError, TypeError):
                pass
            self.connection = None
        if self.signal is not None:
            try:
                self.signal.remove(self._poll)
            except (ValueError, AttributeError, RuntimeError):
                pass
            self.signal = None
        self.client = None
        self.device = None
