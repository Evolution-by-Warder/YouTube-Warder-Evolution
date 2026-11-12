# -*- coding: utf-8 -*-
"""Native 3x2 video card page, with a strict thumbnail download/decode budget.

Only six cards are visible, two thumbnail network workers and one ePicLoad
decoder may operate. No custom widget renderer or external image dependency.
"""
from enigma import ePicLoad
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .grid_model import move_index, page_number, local_slot, VISIBLE_TILES
from .thumbnails import fetch_thumbnail
from .skin import GRID_SKIN

THUMB_WIDTH = 476
THUMB_HEIGHT = 249
MAX_DOWNLOADS = 2
SIDEBAR = ("Domov", "Hľadať", "Odbery", "História", "Playlisty", "Obľúbené", "Nastavenia")


class WarderYouTubeGrid(Screen):
    skin = GRID_SKIN

    def __init__(self, session, items, query, has_next_page=False, on_play=None):
        Screen.__init__(self, session)
        self.items = list(items[:15])
        self.selected = 0 if self.items else -1
        self.query = str(query)[:70]
        self.has_next_page = bool(has_next_page)
        self.on_play = on_play
        self._ready = False
        self._closed = False
        self._epoch = 0
        self._pending_downloads = []
        self._active_downloads = 0
        self._pending_decodes = []
        self._decoding = None
        self._picload = None

        self["brand"] = Label("YouTube - Warder Evolution")
        self["heading"] = Label("Hľadanie: " + self.query)
        self["status"] = Label("")
        self["footer"] = Label(
            "Šípky: výber    OK: prehrať    MODRÉ: nové hľadanie    "
            "ZELENÉ: ďalšie    ŽLTÉ: späť    EXIT: zoznam"
        )
        for i, name in enumerate(SIDEBAR):
            self["side%d" % i] = Label(name)
        for i in range(VISIBLE_TILES):
            self["focus%d" % i] = Label("")
            self["thumb%d" % i] = Pixmap()
            self["title%d" % i] = Label("")
            self["channel%d" % i] = Label("")

        self["actions"] = ActionMap(
            ["NavigationActions", "OkCancelActions", "ColorActions"],
            {
                "left": self.left, "right": self.right,
                "up": self.up, "down": self.down,
                "ok": self.play, "cancel": self.go_back, "red": self.go_back,
                "blue": self.new_search, "green": self.next_page,
                "yellow": self.previous_page
            }, -1
        )
        self.onLayoutFinish.append(self._layout_ready)
        self.onClose.append(self._mark_closed)

    def _layout_ready(self):
        if self._closed:
            return
        self._ready = True
        self._picload = ePicLoad()
        self._picload.PictureData.get().append(self._decode_finished)
        self._picload.setPara((THUMB_WIDTH, THUMB_HEIGHT, 1, 1, False, 1, "#00000000"))
        self._render_page()

    def _mark_closed(self):
        self._closed = True
        self._epoch += 1
        self._pending_downloads = []
        self._pending_decodes = []
        self.on_play = None

    def set_status(self, message):
        if not self._closed:
            self["status"].setText(message)

    def _render_page(self):
        if not self._ready or self._closed:
            return
        self._epoch += 1
        epoch = self._epoch
        self._pending_downloads = []
        self._pending_decodes = []
        start = page_number(self.selected) * VISIBLE_TILES

        for slot in range(VISIBLE_TILES):
            absolute = start + slot
            self["thumb%d" % slot].hide()
            if absolute >= len(self.items):
                self["title%d" % slot].setText("")
                self["channel%d" % slot].setText("")
                self["focus%d" % slot].hide()
                continue
            video = self.items[absolute]
            self["title%d" % slot].setText(str(video.get("title") or "")[:88])
            self["channel%d" % slot].setText(str(video.get("channel") or "")[:55])
            url = video.get("thumbnail_url")
            if url:
                self._pending_downloads.append((epoch, slot, url))

        self._update_focus()
        self._pump_downloads()

    def _update_focus(self):
        if not self._ready or self._closed:
            return
        active = local_slot(self.selected) if self.selected >= 0 else -1
        first = page_number(self.selected) * VISIBLE_TILES
        for slot in range(VISIBLE_TILES):
            if slot == active and first + slot < len(self.items):
                self["focus%d" % slot].show()
            else:
                self["focus%d" % slot].hide()

        if self.selected < 0:
            self.set_status("Žiadne videá.")
        else:
            self.set_status(
                "Video %d/%d  |  strana %d  |  obrázky iba pre viditeľné videá" %
                (self.selected + 1, len(self.items), page_number(self.selected) + 1)
            )

    def _pump_downloads(self):
        while (not self._closed and self._active_downloads < MAX_DOWNLOADS
               and self._pending_downloads):
            request = self._pending_downloads.pop(0)
            self._active_downloads += 1
            # Worker performs disk/network I/O. It never manipulates Enigma2 widgets.
            deferred = deferToThread(fetch_thumbnail, request[2])
            deferred.addCallbacks(
                lambda path, req=request: self._download_done(req, path),
                lambda failure, req=request: self._download_done(req, None)
            )

    def _download_done(self, request, local_path):
        self._active_downloads = max(0, self._active_downloads - 1)
        epoch, slot, _url = request
        if not self._closed and epoch == self._epoch and local_path:
            self._pending_decodes.append((epoch, slot, local_path))
            self._start_decode()
        self._pump_downloads()

    def _start_decode(self):
        if self._closed or self._picload is None or self._decoding is not None:
            return
        while self._pending_decodes:
            request = self._pending_decodes.pop(0)
            if request[0] != self._epoch:
                continue
            self._decoding = request
            if self._picload.startDecode(request[2]) == 0:
                return
            self._decoding = None

    def _decode_finished(self, *args):
        request = self._decoding
        self._decoding = None
        pixmap_ptr = self._picload.getData() if self._picload else None
        if (request and not self._closed and request[0] == self._epoch
                and pixmap_ptr is not None):
            slot = request[1]
            pixmap = (pixmap_ptr.__deref__()
                      if hasattr(pixmap_ptr, "__deref__") else pixmap_ptr)
            self["thumb%d" % slot].setPixmap(pixmap)
            self["thumb%d" % slot].show()
        self._start_decode()

    def _move(self, direction):
        if self._closed or not self.items:
            return
        next_index = move_index(self.selected, direction, len(self.items))
        if next_index == self.selected:
            return
        old_page = page_number(self.selected)
        self.selected = next_index
        if page_number(next_index) != old_page:
            self._render_page()
        else:
            self._update_focus()

    def left(self):
        self._move("left")

    def right(self):
        self._move("right")

    def up(self):
        self._move("up")

    def down(self):
        self._move("down")

    def play(self):
        if self.selected >= 0 and callable(self.on_play):
            self.set_status("Zisťujem dostupnosť videa...")
            self.on_play(self.items[self.selected])

    def next_page(self):
        if not self.items:
            return
        if self.selected + VISIBLE_TILES < len(self.items):
            self.selected += VISIBLE_TILES
            self._render_page()
        elif self.has_next_page:
            self.close("next")
        else:
            self.set_status("Ďalšie videá už nie sú k dispozícii.")

    def previous_page(self):
        if self.selected >= VISIBLE_TILES:
            self.selected -= VISIBLE_TILES
            self._render_page()
        else:
            self.set_status("Toto je prvá stránka.")

    def go_back(self):
        self.close(None)

    def new_search(self):
        self.close("search")
