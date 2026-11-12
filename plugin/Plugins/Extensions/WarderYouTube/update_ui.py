# -*- coding: utf-8 -*-
"""Minimal native Enigma2 updater UI, same opt-in pattern as Warder Radio.

Never manipulate Enigma2 GUI controls from background worker threads.
Do not silently install or restart; user must accept the update first.
"""
from enigma import eTimer
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from twisted.internet import reactor
from twisted.internet.threads import deferToThread

from .skin import UPDATE_SKIN
from .update_core import install_update


class WarderYouTubeUpdateProgress(Screen):
    skin = UPDATE_SKIN

    def __init__(self, session, release):
        Screen.__init__(self, session)
        self.release = release
        self.started = False
        self.disposed = False
        self.finished = False
        self.failed = False
        self["title"] = Label("YouTube Warder Evolution - aktualizácia")
        self["version"] = Label("Nová verzia: " + release["version"])
        self["phase"] = Label("Príprava overenej aktualizácie...")
        self["detail"] = Label("")
        self["percentage"] = Label("")
        self["footer"] = Label("Aktualizáciu neprerušujte. Po úspechu sa obnoví GUI Enigma2.")
        self["progress"] = ProgressBar()
        self["progress"].setValue(0)
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.exit_failed,
            "cancel": self.exit_failed,
            "red": self.exit_failed
        }, -1)
        self.restart_timer = eTimer()
        self.restart_timer.callback.append(self.restart_gui)
        self.onShown.append(self.begin_once)
        self.onClose.append(self.dispose)

    def begin_once(self):
        if self.started or self.disposed:
            return
        self.started = True
        work = deferToThread(install_update, self.release, progress=self.worker_progress)
        work.addCallbacks(self.success, self.failure)

    def worker_progress(self, phase, count=0, total=0):
        reactor.callFromThread(self.show_progress, phase, count, total)

    def show_progress(self, phase, count, total):
        if self.disposed or self.finished:
            return
        titles = {
            "download": "Sťahovanie overeného IPK...",
            "verify": "Kontrola SHA256 a obsahu IPK...",
            "install": "Inštalácia cez opkg...",
            "complete": "Kontrola nainštalovanej verzie dokončená."
        }
        self["phase"].setText(titles.get(phase, "Aktualizácia..."))
        if phase == "download" and total > 0:
            progress = max(0, min(100, int(100 * count / total)))
            self["progress"].setValue(progress)
            self["percentage"].setText("%d%%" % progress)
            self["detail"].setText("%d / %d kB" % (count // 1024, total // 1024))
        elif phase in ("verify", "install"):
            self["percentage"].setText("")
            self["detail"].setText("Nástroje prijímača pripravujú bezpečný prechod.")
        elif phase == "complete":
            self["progress"].setValue(100)

    def success(self, installed_version):
        if self.disposed:
            return
        self.finished = True
        self["progress"].setValue(100)
        self["phase"].setText("Aktualizácia na %s prebehla úspešne." % installed_version)
        self["percentage"].setText("100%")
        self["detail"].setText("Grafické rozhranie Enigma2 sa obnoví.")
        self["footer"].setText("Inštalácia je hotová.")
        self.restart_timer.start(3000, True)

    def failure(self, failure):
        if self.disposed:
            return
        self.finished = True
        self.failed = True
        # Never display Twisted Failure repr; it could contain a request URL.
        safe_type = getattr(failure, "value", None)
        from .update_core import UpdateError
        detail = str(safe_type) if isinstance(safe_type, UpdateError) else (
            "Nepodarilo sa dokončiť aktualizáciu."
        )
        self["phase"].setText("Aktualizácia zlyhala.")
        self["detail"].setText(detail)
        self["footer"].setText("Stlačte OK alebo EXIT na návrat. Žiadny reštart.")
        self["percentage"].setText("")

    def exit_failed(self):
        if self.failed and self.finished:
            self.close()

    def restart_gui(self):
        if self.disposed or not self.finished or self.failed:
            return
        # Explicitly use Enigma2 GUI-only restart (code 3), not box reboot.
        self.session.open(TryQuitMainloop, 3)

    def dispose(self):
        self.disposed = True
        self.restart_timer.stop()
