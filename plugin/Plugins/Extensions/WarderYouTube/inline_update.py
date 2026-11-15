# -*- coding: utf-8 -*-
"""Warder updater embedded in Home's existing right pane.

Network/opkg operations always run off the GUI thread; a short Warder-styled
yes/no confirmation is the only dialog. No separate update Screen is opened.
"""
from twisted.internet import reactor
from twisted.internet.threads import deferToThread

from .i18n import tr as _
from .update_core import check_update, install_update, UpdateError
from .installed_version import read_installed_version


def _check_installed():
    version = read_installed_version()
    return version, check_update(version)


class InlineUpdater:
    def __init__(self, home):
        self.home = home
        self.generation = 0
        self.checking = False
        self.checked = False
        self.installing = False
        self.confirming = False
        self.confirm_yes = False
        self.release = None
        self.installed = ""
        self.phase = ""
        self.percent = 0
        self.error = ""
        self.completed = False
        self.details = False
        self._restart_timer = None

    def is_busy(self):
        return self.installing or self.confirming

    def close(self):
        self.generation += 1
        self.confirming = False
        # Do not interrupt an ongoing opkg install. GUI callbacks become inert.
        self.home = None
        if self._restart_timer is not None:
            try:
                self._restart_timer.stop()
            except (AttributeError, RuntimeError):
                pass
        self._restart_timer = None

    def leave(self):
        """Invalidate asynchronous checks if the user navigates away."""
        if not self.installing:
            self.generation += 1
            self.checking = False

    def show(self):
        h = self.home
        if h is None or h.index != 6:
            return
        h._show_details([
            _("Installed") + ": " + (self.installed or h.installed_version),
            _("Updates") + ": " + (self.release["version"] if self.release else _("Check on demand")),
            self._state_text(),
            (_("Confirm update") + ": " + self.release["version"]) if self.confirming else "",
            (("%d%%" % self.percent) if self.phase in ("", "download") else
             _("Download finished: 100%") if self.phase in ("verify", "install", "complete") else "")
            if self.installing or self.completed else "",
            self._note()
        ])
        if hasattr(h, "_hide_update_widgets"):
            h._hide_update_widgets()
        if self.confirming:
            h["update_no"].setText(_("No"))
            h["update_yes"].setText(_("Yes"))
            # Only the selected word changes colour, never a filled rectangle.
            h["update_no_focus"].setText(_("No"))
            h["update_yes_focus"].setText(_("Yes"))
            h["update_no" if self.confirm_yes else "update_yes"].show()
            h["update_yes_focus" if self.confirm_yes else "update_no_focus"].show()
        elif self.installing or self.completed:
            h["update_progress"].setValue(self.percent)
            h["update_progress"].show()
        h["key_green"].setText(
            _("Confirm") if self.confirming else
            _("Install") if self.release and not self.is_busy() else
            _("Checking updates") if self.checking else
            _("Check for updates"))
        h["key_yellow"].setText(
            _("No") if self.confirming else _("Details") if self.release else "")
        h["key_blue"].setText("" if self.confirming or self.installing else _("Refresh"))
        h["key_red"].setText(_("Cancel") if self.confirming else
                             _("Back") if self.installing else _("Close"))

    def _state_text(self):
        if self.error:
            return _("Update failed") + ": " + self.error
        if self.completed:
            return _("Installation completed.")
        if self.installing:
            return {
                "download": _("Sťahovanie overeného IPK..."),
                "verify": _("Kontrola SHA256 a obsahu IPK..."),
                "install": _("Inštalácia cez opkg..."),
                "complete": _("Kontrola nainštalovanej verzie dokončená.")
            }.get(self.phase, _("Príprava overenej aktualizácie..."))
        if self.checking:
            return _("Checking updates")
        if self.release:
            return _("Update found")
        if self.checked:
            return _("You are up to date.")
        return _("Press OK to check updates.")

    def _note(self):
        if self.confirming:
            return _("Arrows: select · OK: confirm · EXIT: cancel")
        if self.error:
            return _("Stlačte OK alebo EXIT na návrat. Žiadny reštart.")
        if self.installing:
            return _("Aktualizáciu neprerušujte. Po úspechu sa obnoví GUI Enigma2.")
        if self.completed:
            return _("Grafické rozhranie Enigma2 sa obnoví.")
        if self.release:
            return (self.release.get("notes", "") if self.details else
                    _("OK / ZELENÉ: aktualizovať    EXIT: späť"))
        return _("Updates are checked only on request.")

    def activate(self):
        if self.home is None or self.is_busy() or self.checking:
            return
        if self.release is not None:
            self.confirm()
        else:
            self.check()

    def check(self):
        if self.home is None or self.is_busy() or self.checking:
            return
        self.generation += 1
        token = self.generation
        self.error = ""
        self.release = None
        self.details = False
        self.checked = False
        self.checking = True
        self.show()
        try:
            task = deferToThread(_check_installed)
            task.addCallbacks(lambda data: self._checked(token, data),
                              lambda err: self._check_failed(token, err))
        except Exception:
            self._check_failed(token, None)

    def _checked(self, token, data):
        if self.home is None or token != self.generation:
            return
        self.checking = False
        self.checked = True
        self.installed, self.release = data
        self.home.installed_version = self.installed
        self.home["version"].setText(self.installed + "  •  Enigma2")
        self.show()

    def _check_failed(self, token, err):
        if self.home is None or token != self.generation:
            return
        self.checking = False
        self.checked = False
        self.error = _("Kontrola aktualizácie zlyhala.")
        self.show()

    def details_toggle(self):
        if self.release is None or self.is_busy():
            return
        self.details = not self.details
        self.show()

    def confirm(self):
        if self.home is None or self.checking or self.is_busy() or self.release is None:
            return
        self.confirming = True
        self.confirm_yes = False
        self.show()

    def select(self, yes):
        if self.home is None or not self.confirming:
            return
        self.confirm_yes = bool(yes)
        self.show()

    def answer(self, approved):
        if self.confirming:
            self._confirmed(self.generation, approved)

    def _confirmed(self, token, approved):
        if self.home is None or token != self.generation or not self.confirming:
            return
        self.confirming = False
        self.confirm_yes = False
        if not approved or self.release is None:
            self.show()
            return
        self.installing = True
        self.error = ""
        self.phase = ""
        self.percent = 0
        self.completed = False
        self.home._busy = True
        self.show()
        try:
            task = deferToThread(install_update, self.release, progress=self._worker_progress)
            task.addCallbacks(lambda version: self._installed(token, version),
                              lambda err: self._install_failed(token, err))
        except Exception:
            self._install_failed(token, None)

    def _worker_progress(self, phase, current=0, total=0):
        # Receiver's widgets may only be touched in the Enigma2 GUI thread.
        reactor.callFromThread(self._progress, phase, current, total)

    def _progress(self, phase, current, total):
        if self.home is None or not self.installing:
            return
        self.phase = phase
        if phase == "download" and total:
            self.percent = max(0, min(100, 100 * current // total))
        if phase == "complete":
            self.percent = 100
        self.show()

    def _installed(self, token, version):
        if self.home is None or token != self.generation:
            return
        self.installing = False
        self.completed = True
        self.percent = 100
        self.phase = "complete"
        self.installed = version
        self.home._busy = True  # protect successful install until GUI restarts
        self.show()
        try:
            from enigma import eTimer
            self._restart_timer = eTimer()
            self._restart_timer.callback.append(self._restart_gui)
            self._restart_timer.start(3000, True)
        except Exception:
            self.error = _("Grafické rozhranie Enigma2 sa obnoví.")
            self.home._busy = False
            self.show()

    def _restart_gui(self):
        if self.home is None or not self.completed or self.error:
            return
        from Screens.Standby import TryQuitMainloop
        self.home.session.open(TryQuitMainloop, 3)

    def _install_failed(self, token, err):
        if self.home is None or token != self.generation:
            return
        self.installing = False
        self.home._busy = False
        safe = getattr(err, "value", None)
        self.error = str(safe) if isinstance(safe, UpdateError) else _(
            "Nepodarilo sa dokončiť aktualizáciu.")
        self.show()
