# -*- coding: utf-8 -*-
"""Native Enigma2 Favourites / History browser; no external renderers.

The receiver's TV service stays running while browsing, as requested by the
owner. Only playback activates the existing native Warder MoviePlayer.
"""
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .skin import LIBRARY_SKIN
from .local_library import (
    LibraryError, list_videos, remove_video, clear_videos,
    toggle_favourite, record_opened
)
from .resolver import ResolverError, resolve_video_streams
from .settings import get_quality
from .i18n import tr as _
from .confirm_ui import WarderYouTubeConfirm
from .info_ui import WarderYouTubeInfo


class WarderYouTubeLibrary(Screen):
    skin = LIBRARY_SKIN

    def __init__(self, session, kind):
        if kind not in ("favourites", "history"):
            raise ValueError("Unknown video library")
        Screen.__init__(self, session)
        add_header(self)
        self.kind = kind
        self.video_items = []
        self.busy = False
        self.playback_active = False
        self.disposed = False
        self.confirmation_open = False
        self.request_version = 0

        title = _("Favourites") if kind == "favourites" else _("History")
        self["title"] = Label("YouTube Warder Evolution / " + title)
        self["subtitle"] = Label("")
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Play video"))
        self["key_yellow"] = Label(
            _("Remove video from favourites") if kind == "favourites"
            else _("Delete video from history")
        )
        self["key_blue"] = Label(
            _("Clear all favourite videos") if kind == "favourites"
            else _("Clear entire history")
        )
        self["results"] = MenuList([])
        self["status"] = Label("")
        self["footer"] = Label(
            _("OK: play · INFO: details · MENU: actions · YELLOW: remove favourite · BLUE: clear favourites · EXIT: home")
            if kind == "favourites" else
            _("OK: play · INFO: details · MENU: actions · YELLOW: delete from history · BLUE: clear history · EXIT: home")
        )
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "InfoActions", "MenuActions"],
            {
                "ok": self.play_selected, "info": self.show_info,
                "menu": self.open_actions, "green": self.play_selected,
                "yellow": self.remove_selected,
                "blue": self.confirm_clear, "cancel": self.close,
                "red": self.close
            }, -1
        )
        self["results"].onSelectionChanged.append(self.selection_changed)
        self.onShown.append(self.refresh)
        self.onClose.append(self.dispose)

    def dispose(self):
        self.disposed = True
        self.request_version += 1

    def refresh(self):
        if self.disposed or self.busy or self.playback_active:
            return
        try:
            items = list_videos(self.kind)
        except LibraryError as error:
            self.video_items = []
            self["results"].setList([])
            self["status"].setText(str(error))
            return
        self.video_items = items
        self["results"].setList([
            "%s   |   %s" % ((item["title"] or "YouTube video")[:93],
                             item["channel"][:50])
            for item in items
        ])
        self["subtitle"].setText("%s: %d videí" % (
            _("Favourites") if self.kind == "favourites" else _("Recently opened"), len(items)))
        self["status"].setText(
            _("Zoznam je prázdny. V hľadaní stlač MENU na uloženie videa.")
            if not items and self.kind == "favourites" else
            _("História je prázdna. Otvor video z výsledkov hľadania.")
            if not items else _("Vyber video a stlač OK. Prehrávanie nepotrebuje API kľúč.")
        )

    def _selected(self):
        if self.disposed:
            return None
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.video_items):
            return self.video_items[index]
        return None

    def selection_changed(self):
        # No network requests when browsing locally stored video names.
        return

    def show_info(self):
        if self.busy or self.playback_active:
            return
        item = self._selected()
        if item is not None:
            self.session.open(
                WarderYouTubeInfo,
                "Názov: %s\nKanál: %s\nID videa: %s" %
                (item["title"], item["channel"], item["video_id"])
            )

    def open_actions(self):
        item = self._selected()
        if item is None or self.busy or self.playback_active:
            return
        from .context_menu import WarderYouTubeContext
        self.session.openWithCallback(
            self.action_selected, WarderYouTubeContext, item,
            self.kind == "favourites", self.kind)

    def action_selected(self, action):
        if self.disposed:
            return
        if action == "play":
            self.play_selected()
        elif action == "favorite":
            self.save_favourite()
        elif action == "info":
            self.show_info()
        elif action == "remove":
            self.remove_selected()
        elif action == "clear":
            self.confirm_clear()

    def save_favourite(self):
        if self.busy or self.playback_active:
            return
        item = self._selected()
        if item is None:
            return
        try:
            added = toggle_favourite(item)
            if self.kind == "favourites":
                self.refresh()
            self["status"].setText(
                "Video pridané do obľúbených." if added
                else "Video odstránené z obľúbených."
            )
        except LibraryError as error:
            self["status"].setText(str(error))

    def remove_selected(self):
        if self.busy or self.playback_active:
            return
        item = self._selected()
        if item is None:
            return
        try:
            removed = remove_video(self.kind, item["video_id"])
            self.refresh()
            if removed:
                self["status"].setText(
                    _("Video removed from favourites.") if self.kind == "favourites"
                    else _("Video removed from history.")
                )
        except LibraryError as error:
            self["status"].setText(str(error))

    def confirm_clear(self):
        if (self.disposed or self.busy or self.playback_active
                or self.confirmation_open or not self.video_items):
            return
        self.confirmation_open = True
        try:
            self.session.openWithCallback(
                self.clear_confirmed, WarderYouTubeConfirm,
                (_("Clear all favourite videos") if self.kind == "favourites"
                 else _("Clear entire history")) + "?"
            )
        except Exception:
            self.confirmation_open = False
            self["status"].setText("Potvrdenie nebolo možné zobraziť.")

    def clear_confirmed(self, confirmed):
        self.confirmation_open = False
        if self.disposed or not confirmed:
            return
        try:
            clear_videos(self.kind)
            self.refresh()
            self["status"].setText(
                _("All favourite videos removed.") if self.kind == "favourites"
                else _("Entire history cleared.")
            )
        except LibraryError as error:
            self["status"].setText(str(error))

    def play_selected(self):
        if self.busy or self.playback_active or self.disposed or self.confirmation_open:
            return
        item = self._selected()
        if item is None:
            return
        self.busy = True
        self.request_version += 1
        version = self.request_version
        self["status"].setText("Hľadám kompatibilný YouTube stream...")
        try:
            from .player import dash_available
            deferred = deferToThread(
                resolve_video_streams, item["video_id"],
                quality=get_quality(), dash=dash_available()
            )
            deferred.addCallbacks(
                lambda streams: self.play_ready(version, item, streams),
                lambda error: self.play_error(version, error)
            )
        except Exception:
            self.busy = False
            self["status"].setText("Prehrávanie sa nepodarilo spustiť.")

    def play_ready(self, version, item, streams):
        if self.disposed or version != self.request_version:
            return
        self.busy = False
        if self.playback_active:
            return
        self.playback_active = True
        self["status"].setText("Otváram prehrávač Enigma2...")
        try:
            from .player import open_player
            open_player(self.session, streams, item["title"],
                        on_close=self.player_closed)
        except Exception:
            self.playback_active = False
            self["status"].setText("Prehrávač Enigma2 sa nepodarilo otvoriť.")
            return
        try:
            record_opened(item)
        except LibraryError:
            # Saving history never takes precedence over playback.
            pass

    def play_error(self, version, failure):
        if self.disposed or version != self.request_version:
            return
        self.busy = False
        error = getattr(failure, "value", None)
        self["status"].setText(
            str(error) if isinstance(error, ResolverError)
            else "Kompatibilný stream sa nepodarilo získať."
        )

    def player_closed(self, failed=False, *args):
        self.playback_active = False
        if self.disposed:
            return
        self.refresh()
        self["status"].setText(
            "Video sa nepodarilo prehrať. Skús iné video alebo kvalitu 360p."
            if failed is True else "Prehrávanie ukončené. OK: ďalšie video."
        )
