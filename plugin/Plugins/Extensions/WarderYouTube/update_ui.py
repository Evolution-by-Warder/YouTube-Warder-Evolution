# -*- coding: utf-8 -*-
"""Minimal native Enigma2 updater UI, same opt-in pattern as Warder Radio.

Never manipulate Enigma2 GUI controls from background worker threads.
Do not silently install or restart; user must accept the update first.
"""
from .header_ui import add_header
from enigma import eTimer
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
from twisted.internet import reactor
from twisted.internet.threads import deferToThread

from .skin import UPDATE_SKIN, UPDATE_CHECK_SKIN
from .update_core import install_update, check_update, CURRENT_VERSION, UpdateError
from .i18n import tr as _
from .confirm_ui import WarderYouTubeConfirm



def check_actual_installed_version():
    """Blocking: get installed opkg version before checking the test feed.

    The running GUI may still hold test10 Python modules although opkg has
    already installed test13. Do NOT offer an already-installed build.
    """
    from .installed_version import read_installed_version
    installed = read_installed_version()
    return installed, check_update(installed)


class WarderYouTubeUpdateProgress(Screen):
    skin = UPDATE_SKIN

    def __init__(self, session, release):
        Screen.__init__(self, session)
        add_header(self)
        self.release = release
        self.started = False
        self.disposed = False
        self.finished = False
        self.failed = False
        self["title"] = Label("YouTube Warder Evolution  /  " + _("Updates"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Install"))
        self["key_yellow"] = Label(_("Details"))
        self["key_blue"] = Label(_("Refresh"))
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


class WarderYouTubeUpdateCheck(Screen):
    """Check in a worker; install only following explicit on-screen confirmation."""
    skin = UPDATE_CHECK_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        add_header(self)
        self.started = False
        self.disposed = False
        self.release = None
        self.confirmation_open = False
        self.install_started = False
        self["title"] = Label("YouTube Warder Evolution  /  " + _("Updates"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label("")
        self["key_yellow"] = Label(_("Details"))
        self["key_blue"] = Label(_("Refresh"))
        self._checking = False
        self.details_visible = False
        self["status"] = Label("Kontrola testovacieho aktualizačného kanála...")
        self["detail"] = Label("Aktuálna verzia: " + CURRENT_VERSION)
        self["footer"] = Label("EXIT: späť")
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], {
            "ok": self.ask_install, "green": self.ask_install,
            "cancel": self.close, "red": self.close,
            "yellow": self.toggle_details, "blue": self.refresh_check
        }, -1)
        self.onShown.append(self.begin_once)
        self.onClose.append(self.dispose)

    def begin_once(self):
        if self.started or self.disposed:
            return
        self.started = True
        self._checking = True
        work = deferToThread(check_actual_installed_version)
        work.addCallbacks(self.found, self.failed_check)

    def found(self, release):
        if self.disposed:
            return
        # New worker result includes the real opkg version. Plain release is
        # still accepted for older callback callers and mocked receiver tests.
        if isinstance(release, tuple) and len(release) == 2:
            installed_version, release = release
            self["hdr_version"].setText(installed_version)
            self["detail"].setText("Nainštalovaná verzia: " + installed_version)
        else:
            installed_version = CURRENT_VERSION
        self._checking = False
        self.release = release
        if release is None:
            self["key_green"].setText("")
            self["status"].setText(_("Testovací kanál: používate najnovšiu dostupnú verziu."))
            self["detail"].setText("Nainštalovaná verzia: " + installed_version)
            self["footer"].setText("EXIT: späť")
        else:
            self["key_green"].setText(_("Install"))
            self["status"].setText(_("Update found") + ": " + release["version"])
            self["detail"].setText(release.get("notes") or "Oficiálne overená aktualizácia.")
            self["footer"].setText("OK / ZELENÉ: aktualizovať    EXIT: späť")

    def failed_check(self, failure):
        if self.disposed:
            return
        self._checking = False
        self["key_green"].setText("")
        problem = getattr(failure, "value", None)
        self["status"].setText("Kontrola aktualizácie zlyhala.")
        self["detail"].setText(str(problem) if isinstance(problem, UpdateError)
                               else "Nepodarilo sa kontaktovať aktualizačný server.")
        self["footer"].setText("EXIT: späť")

    def toggle_details(self):
        if self.disposed or self.release is None:
            return
        self.details_visible = not self.details_visible
        self["detail"].setText(
            (self.release.get("notes") or "") if self.details_visible
            else _("Update found") + ": " + self.release["version"])

    def refresh_check(self):
        if self.disposed or self._checking or self.confirmation_open or self.install_started:
            return
        self.started = False
        self.release = None
        self.details_visible = False
        self["key_green"].setText("")
        self["status"].setText(_("Checking updates"))
        self.begin_once()

    def ask_install(self):
        if (self.disposed or self._checking or self.release is None or
                self.confirmation_open or self.install_started):
            return
        self.confirmation_open = True
        try:
            self.session.openWithCallback(
                self.install_confirmed, WarderYouTubeConfirm,
                _("Confirm update") + ": " + self.release["version"] +
                " • GUI Enigma2"
            )
        except Exception:
            self.confirmation_open = False
            self["status"].setText("Potvrdenie aktualizácie sa nepodarilo otvoriť.")

    def install_confirmed(self, confirmed):
        if self.disposed or not self.confirmation_open:
            return
        self.confirmation_open = False
        if not confirmed or self.release is None or self.install_started:
            return
        self.install_started = True
        try:
            # Prevent a second installation while the first progress dialog
            # is still active; unlock only after that dialog actually closes.
            self.session.openWithCallback(
                self.progress_closed, WarderYouTubeUpdateProgress, self.release)
        except Exception:
            self.install_started = False
            self["status"].setText("Inštalátor aktualizácie sa nepodarilo otvoriť.")

    def progress_closed(self, *args):
        self.install_started = False
        if not self.disposed:
            self["status"].setText("Inštalačné okno bolo zatvorené.")

    def dispose(self):
        self.disposed = True
        self.confirmation_open = False
