# -*- coding: utf-8 -*-
"""One reusable, native Enigma2 Warder header for every YouTube screen.

A single static PNG provides the visual identity; date, clock and version
remain native Label components. No converters, global skin changes, animation
or external renderers. The 1 Hz timer only runs while a screen is visible.
"""
from datetime import datetime

from Components.Label import Label

# All YouTube screens share one non-blocking installed-package lookup.
# The GUI may keep an older imported module around after an IPK upgrade;
# opkg is the authoritative source, not a hard-coded test build value.
_version_cache = None
_version_pending = []
_version_busy = False


def _version_ready(actual):
    global _version_cache, _version_busy
    from .update_core import CURRENT_VERSION
    _version_cache = actual if isinstance(actual, str) and actual else CURRENT_VERSION
    _version_busy = False
    subscribers = list(_version_pending)
    _version_pending[:] = []
    for controller in subscribers:
        controller.set_installed_version(_version_cache)
    return actual


def _version_failed(_error):
    return _version_ready(None)


def _request_installed_version(controller):
    global _version_busy
    if controller.closed:
        return
    if _version_cache is not None:
        controller.set_installed_version(_version_cache)
        return
    if controller not in _version_pending:
        _version_pending.append(controller)
    if _version_busy:
        return
    _version_busy = True
    try:
        from .installed_version import read_installed_version
        from twisted.internet.threads import deferToThread
        deferred = deferToThread(read_installed_version)
        deferred.addCallbacks(_version_ready, _version_failed)
    except (ImportError, AttributeError, RuntimeError, TypeError):
        # Never stall or crash the UI for a status label.
        _version_failed(None)



DAY_NAMES = {
    "sk": ("Pondelok", "Utorok", "Streda", "Štvrtok", "Piatok", "Sobota", "Nedeľa"),
    "cs": ("Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek", "Sobota", "Neděle"),
    "de": ("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"),
    "en": ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"),
}
MONTH_NAMES = {
    "sk": ("januára", "februára", "marca", "apríla", "mája", "júna", "júla",
           "augusta", "septembra", "októbra", "novembra", "decembra"),
    "cs": ("ledna", "února", "března", "dubna", "května", "června", "července",
           "srpna", "září", "října", "listopadu", "prosince"),
    "de": ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
           "August", "September", "Oktober", "November", "Dezember"),
    "en": ("January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"),
}
VERSION_WORDS = {"sk": "Verzia:", "cs": "Verze:", "de": "Version:", "en": "Version:"}


def receiver_language():
    try:
        from .i18n import language_code
        code = language_code()
        return str(code).split("_")[0].split("-")[0].lower()
    except (ImportError, AttributeError, TypeError, ValueError):
        return "en"


def header_strings(moment=None, locale="sk"):
    moment = moment or datetime.now()
    language = locale if locale in DAY_NAMES else "en"
    day = DAY_NAMES[language][moment.weekday()]
    month = MONTH_NAMES[language][moment.month-1]
    if language == "en":
        date = "%s %d, %d" % (month, moment.day, moment.year)
    elif language == "de":
        date = "%d. %s %d" % (moment.day, month, moment.year)
    else:
        date = "%d. %s %d" % (moment.day, month, moment.year)
    return day, date, moment.strftime("%H:%M:%S"), VERSION_WORDS[language]


class HeaderController:
    def __init__(self, screen):
        self.screen = screen
        self.timer = None
        self.connection = None
        self.timeout_callbacks = None
        self.closed = False
        # Product name and by-Warder signature are baked into the single
        # approved static banner. Only live values need native widgets.
        screen["hdr_day"] = Label("")
        screen["hdr_date"] = Label("")
        screen["hdr_clock"] = Label("")
        screen["hdr_seconds"] = Label("")
        screen["hdr_version_label"] = Label("")
        from .update_core import CURRENT_VERSION
        screen["hdr_version"] = Label(CURRENT_VERSION)
        self.update()
        for hook in ("onShown", "onShow"):
            callbacks = getattr(screen, hook, None)
            if callbacks is not None:
                callbacks.append(self.start)
        for hook, action in (("onHide", self.stop), ("onClose", self.close)):
            callbacks = getattr(screen, hook, None)
            if callbacks is not None:
                callbacks.append(action)

    def set_installed_version(self, version):
        if not self.closed and isinstance(version, str) and version:
            self.screen["hdr_version"].setText(version)

    def update(self):
        if self.closed:
            return
        day, date, clock, version_label = header_strings(
            datetime.now(), receiver_language())
        self.screen["hdr_day"].setText(day)
        self.screen["hdr_date"].setText(date)
        # Standard Warder/PiconHub treatment: large HH:MM, smaller :SS.
        hours_minutes, seconds = clock.rsplit(":", 1)
        self.screen["hdr_clock"].setText(hours_minutes)
        self.screen["hdr_seconds"].setText(":" + seconds)
        self.screen["hdr_version_label"].setText(version_label)

    def start(self):
        if self.closed:
            return
        self.update()
        _request_installed_version(self)
        if self.timer is None:
            try:
                from enigma import eTimer
                self.timer = eTimer()
                timeout = self.timer.timeout
                if hasattr(timeout, "get"):
                    self.timeout_callbacks = timeout.get()
                    self.timeout_callbacks.append(self.update)
                else:
                    self.connection = timeout.connect(self.update)
            except (ImportError, AttributeError, RuntimeError, TypeError):
                self.timer = None
                return
        try:
            self.timer.start(1000, False)
        except (AttributeError, RuntimeError, TypeError):
            pass

    def stop(self):
        if self.timer is not None:
            try:
                self.timer.stop()
            except (AttributeError, RuntimeError, TypeError):
                pass

    def close(self):
        if self.closed:
            return
        self.closed = True
        if self in _version_pending:
            _version_pending.remove(self)
        self.stop()
        if self.connection is not None:
            try:
                self.connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
            self.connection = None
        if self.timeout_callbacks is not None:
            try:
                self.timeout_callbacks.remove(self.update)
            except (ValueError, AttributeError, RuntimeError):
                pass
            self.timeout_callbacks = None
        self.timer = None


def add_header(screen):
    controller = HeaderController(screen)
    # Keep the controller alive for the lifetime of this screen.
    screen._warder_header = controller
    return controller
