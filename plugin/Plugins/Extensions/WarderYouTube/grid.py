# -*- coding: utf-8 -*-
"""Native 3x2 video card page, with a strict thumbnail download/decode budget.

Only six cards are visible, two thumbnail network workers and one ePicLoad
decoder may operate. No custom widget renderer or external image dependency.
"""
from .header_ui import add_header
from enigma import ePicLoad
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .grid_model import move_index, page_number, local_slot, VISIBLE_TILES
from .thumbnails import fetch_thumbnail
from .skin import GRID_SKIN
from .tile_scrollbar import TilePageScrollbar
from .i18n import tr as _

THUMB_WIDTH = 491
THUMB_HEIGHT = 276
MAX_DOWNLOADS = 2
CARD_TITLE_LIMIT = 52


def card_title(value, limit=CARD_TITLE_LIMIT):
    """Bound a card's two-line title without changing its full sidebar title."""
    label = " ".join(str(value or "").split())
    return label if len(label) <= limit else label[:limit - 1].rstrip() + "…"


class WarderYouTubeGrid(Screen):
    skin = GRID_SKIN

    def __init__(self, session, items, query, has_next_page=False, on_play=None, on_info=None, on_favorite=None):
        Screen.__init__(self, session)
        add_header(self)
        self.video_items = list(items[:15])
        self.selected = 0 if self.video_items else -1
        self.query = str(query)[:70]
        self.has_next_page = bool(has_next_page)
        self.on_play = on_play
        self.on_info = on_info
        self.on_favorite = on_favorite
        self._ready = False
        self._closed = False
        self._epoch = 0
        self._pending_downloads = []
        self._active_downloads = 0
        # Track per-page inflight requests without bypassing the global cap.
        self._active_requests = []
        self._pending_decodes = []
        self._decoding = None
        self._picload = None
        self._picload_connection = None
        self._picload_signal = None
        self._picload_generation = 0
        self._picload_callback = None
        self._thumb_failures = 0
        self._thumb_shown = 0
        self._thumb_expected = 0
        self._thumb_network_failures = 0
        self._thumb_decode_failures = 0
        self._pixmap_cache = {}
        self._visible_urls = {}
        # Playback/status messages must not be overwritten by late images.
        self._status_override = False

        self["brand"] = Label("YouTube Warder Evolution")
        self["heading"] = Label(_("Search") + ": " + self.query)
        self["status"] = Label("")
        self["footer"] = Label(
            "Šípky: výber    OK: prehrať    MODRÉ: nové hľadanie    "
            "INFO: " + _("Video details") + "    MENU: " + _("Video actions") + "    EXIT: " + _("Home")
        )
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Next"))
        self["key_yellow"] = Label(_("Previous"))
        self["key_blue"] = Label(_("New search"))
        self["video_scroll_track"] = Label(" ")
        self["video_scroll_thumb"] = Label(" ")
        self.page_scroll = TilePageScrollbar(
            self["video_scroll_track"], self["video_scroll_thumb"],
            1880, 217, 5, 722
        )
        for i in range(7):
            self["side%d" % i] = Label("")
        for i in range(VISIBLE_TILES):
            self["focus%d" % i] = Pixmap()
            self["thumb%d" % i] = Pixmap()
            self["title%d" % i] = Label("")
            self["channel%d" % i] = Label("")

        self["actions"] = ActionMap(
            ["NavigationActions", "OkCancelActions", "ColorActions", "InfoActions", "MenuActions"],
            {
                "left": self.left, "right": self.right,
                "up": self.up, "down": self.down,
                "ok": self.play, "info": self.show_info, "menu": self.show_menu,
                "cancel": self.go_back, "red": self.go_back,
                "blue": self.new_search, "green": self.next_page,
                "yellow": self.previous_page
            }, -1
        )
        self.onLayoutFinish.append(self._layout_ready)
        self.onShown.append(self._restore_thumbnails)
        self.onClose.append(self._mark_closed)

    def _create_decoder(self):
        # Enigma2 ePicLoad may become unusable after fast screen switching.
        # Keep each PictureData callback bound to its decoder generation.
        self._picload_generation += 1
        generation = self._picload_generation
        try:
            decoder = ePicLoad()
            signal = decoder.PictureData
            callback = lambda *args: self._decoded_for_generation(generation, *args)
            self._picload = decoder
            self._picload_callback = callback
            if hasattr(signal, "get"):
                self._picload_signal = signal.get()
                self._picload_signal.append(callback)
            else:
                self._picload_connection = signal.connect(callback)
            self._picload.setPara(self._decode_parameters())
            return True
        except Exception:
            self._release_decoder()
            self._picload = None
            return False

    def _decoded_for_generation(self, generation, *args):
        if generation != self._picload_generation or self._closed:
            return
        self._decode_finished(*args)

    def _restart_decoder(self):
        # Drop abandoned PictureData jobs instead of keeping the whole gallery
        # without thumbnails until the user closes and reopens the plugin.
        self._picload_generation += 1
        self._release_decoder()
        self._picload = None
        self._decoding = None
        if not self._closed:
            self._create_decoder()

    def _layout_ready(self):
        if self._closed:
            return
        self._ready = True
        self._create_decoder()
        self._render_page()

    def _restore_thumbnails(self):
        if not self._ready or self._closed:
            return
        restored = 0
        for slot, url in self._visible_urls.items():
            pixmap = self._pixmap_cache.get(url)
            if pixmap is not None:
                try:
                    self["thumb%d" % slot].setPixmap(pixmap)
                    self["thumb%d" % slot].show()
                    restored += 1
                except (AttributeError, TypeError, ValueError, RuntimeError):
                    self._pixmap_cache.pop(url, None)
        if (not restored and self._decoding is not None and self.video_items):
            # A modal may interrupt PictureData forever on older Enigma2.
            # A fresh decoder can repopulate the current page immediately.
            self._restart_decoder()
            self._render_page()
            return
        if (not restored and not self._pending_downloads
                and not self._active_requests and not self._pending_decodes
                and self._decoding is None and self.video_items):
            self._render_page()

    def _decode_parameters(self):
        """Follow the Enigma2 thumbnail pattern from Taapat YouTube.

        Use the actual scaled Pixmap dimensions and AVSwitch framebuffer
        ratio when present. Keep conservative defaults for older images.
        """
        width, height = THUMB_WIDTH, THUMB_HEIGHT
        try:
            widget = self["thumb0"]
            actual = widget.getSize() if getattr(widget, "instance", None) else None
            if (actual and len(actual) == 2 and 0 < actual[0] <= 4096
                    and 0 < actual[1] <= 2160):
                width, height = int(actual[0]), int(actual[1])
        except (AttributeError, TypeError, ValueError, RuntimeError):
            pass
        # OpenATV ePicLoad sets aspect_ratio=0 when the fourth setPara
        # parameter is 0. This fills the entire target pixmap even for
        # square/4:3 thumbnail sources instead of inserting blue side bars.
        # The approved card remains 16:9 with no video-data crop dependency.
        return (width, height, 0, 0, False, 1, "#00000000")

    def _release_decoder(self):
        """Disconnect on either Enigma2 signal API, including during teardown."""
        connection, self._picload_connection = self._picload_connection, None
        signal, self._picload_signal = self._picload_signal, None
        if connection is not None:
            try:
                connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
        if signal is not None:
            try:
                signal.remove(self._picload_callback)
            except (ValueError, AttributeError, RuntimeError):
                pass
        self._picload_callback = None

    def _mark_closed(self):
        self._closed = True
        self._epoch += 1
        self._pending_downloads = []
        self._pending_decodes = []
        self._pixmap_cache.clear()
        self._visible_urls.clear()
        self._release_decoder()
        self._picload = None
        self._picload_generation += 1
        self._picload_callback = None
        self.on_play = None
        self.on_info = None
        self.on_favorite = None

    def set_status(self, message, override=False):
        if not self._closed:
            if override:
                self._status_override = True
            self["status"].setText(message)

    def _render_page(self):
        if not self._ready or self._closed:
            return
        self._epoch += 1
        epoch = self._epoch
        if self._decoding is not None:
            self._restart_decoder()
        elif self._picload is None:
            self._create_decoder()
        self._pending_downloads = []
        self._pending_decodes = []
        self._thumb_failures = 0
        self._thumb_shown = 0
        self._thumb_expected = 0
        self._thumb_network_failures = 0
        self._thumb_decode_failures = 0
        self._status_override = False
        start = page_number(self.selected) * VISIBLE_TILES
        count = (len(self.video_items) + VISIBLE_TILES - 1) // VISIBLE_TILES
        total_pages = count + (1 if self.has_next_page else 0)
        self.page_scroll.update(
            page_number(self.selected) if self.selected >= 0 else 0,
            total_pages if self.video_items else 1
        )
        self._visible_urls = {}

        for slot in range(VISIBLE_TILES):
            absolute = start + slot
            self["thumb%d" % slot].hide()
            if absolute >= len(self.video_items):
                self["title%d" % slot].setText("")
                self["channel%d" % slot].setText("")
                self["focus%d" % slot].hide()
                continue
            video = self.video_items[absolute]
            self["title%d" % slot].setText(card_title(video.get("title")))
            self["channel%d" % slot].setText(str(video.get("channel") or "")[:55])
            url = video.get("thumbnail_url")
            if url:
                self._visible_urls[slot] = url
                cached = self._pixmap_cache.get(url)
                if cached is not None:
                    try:
                        self["thumb%d" % slot].setPixmap(cached)
                        self["thumb%d" % slot].show()
                        continue
                    except (AttributeError, TypeError, ValueError, RuntimeError):
                        self._pixmap_cache.pop(url, None)
                self._thumb_expected += 1
                self._pending_downloads.append((epoch, slot, url))

        self._update_focus()
        self._pump_downloads()

    def _update_focus(self):
        if not self._ready or self._closed:
            return
        active = local_slot(self.selected) if self.selected >= 0 else -1
        first = page_number(self.selected) * VISIBLE_TILES
        for slot in range(VISIBLE_TILES):
            if slot == active and first + slot < len(self.video_items):
                self["focus%d" % slot].show()
            else:
                self["focus%d" % slot].hide()

        self["side0"].setText(_("Results").upper())
        self["side1"].setText("%d / %d" % (self.selected + 1, len(self.video_items))
                              if self.selected >= 0 else "0")
        self["side2"].setText(_("Video selected").upper())
        self["side4"].setText(_("Video channel").upper())
        self["side6"].setText(_("Menu for selected video"))
        if self.selected < 0:
            self["side3"].setText(_("No video selected"))
            self["side5"].setText("")
            self.set_status(_("Žiadne videá."))
        else:
            video = self.video_items[self.selected]
            self["side3"].setText(str(video.get("title") or "")[:90])
            self["side5"].setText(str(video.get("channel") or "")[:56])
            self.set_status(
                _("Video %d/%d  |  strana %d  |  obrázky iba pre viditeľné videá") %
                (self.selected + 1, len(self.video_items), page_number(self.selected) + 1)
            )

    def _pump_downloads(self):
        while (not self._closed and self._active_downloads < MAX_DOWNLOADS
               and self._pending_downloads):
            request = self._pending_downloads.pop(0)
            self._active_downloads += 1
            self._active_requests.append(request)
            # Worker performs disk/network I/O. It never manipulates Enigma2 widgets.
            deferred = deferToThread(fetch_thumbnail, request[2])
            deferred.addCallbacks(
                lambda path, req=request: self._download_done(req, path),
                lambda failure, req=request: self._download_done(req, None)
            )

    def _download_done(self, request, local_path):
        self._active_downloads = max(0, self._active_downloads - 1)
        try:
            self._active_requests.remove(request)
        except ValueError:
            pass
        epoch, slot, _url = request
        if not self._closed and epoch == self._epoch:
            if self._picload is not None and local_path:
                self._pending_decodes.append((epoch, slot, local_path))
                self._start_decode()
            else:
                self._thumb_failures += 1
                if local_path:
                    self._thumb_decode_failures += 1
                else:
                    self._thumb_network_failures += 1
        self._pump_downloads()
        self._check_thumbnails()

    def _start_decode(self):
        if self._closed or self._picload is None or self._decoding is not None:
            return
        while self._pending_decodes:
            request = self._pending_decodes.pop(0)
            if request[0] != self._epoch:
                continue
            self._decoding = request
            try:
                started = self._picload.startDecode(request[2]) == 0
            except Exception:
                started = False
            if started:
                return
            self._decoding = None
            self._thumb_failures += 1
            self._thumb_decode_failures += 1

    def _decode_finished(self, *args):
        request = self._decoding
        self._decoding = None
        if not request or self._closed or request[0] != self._epoch:
            self._start_decode()
            return
        try:
            pixmap_ptr = self._picload.getData() if self._picload else None
            if pixmap_ptr is None:
                self._thumb_failures += 1
                self._thumb_decode_failures += 1
            else:
                # Pixmap.setPixmap delegates to ePixmap.setPixmap. Keep the
                # original native ePtr<gPixmap>, as Warder Radio does; do not
                # dereference it to an incompatible Python gPixmap object.
                widget = self["thumb%d" % request[1]]
                widget.setPixmap(pixmap_ptr)
                widget.show()
                url = self._visible_urls.get(request[1])
                if url is not None:
                    self._pixmap_cache[url] = pixmap_ptr
                    while len(self._pixmap_cache) > 12:
                        self._pixmap_cache.pop(next(iter(self._pixmap_cache)))
                self._thumb_shown += 1
        except (AttributeError, TypeError, ValueError, RuntimeError):
            # A decode error must not cause a GUI crash.
            self._thumb_failures += 1
            self._thumb_decode_failures += 1
        self._start_decode()
        self._check_thumbnails()

    def _check_thumbnails(self):
        # A late download must not erase player or INFO progress messages.
        if self._closed or not self._ready or self._status_override:
            return
        finished = (self._thumb_expected
                    and self._thumb_shown + self._thumb_failures >= self._thumb_expected
                    and not self._pending_downloads
                    and not any(req[0] == self._epoch for req in self._active_requests)
                    and not self._pending_decodes and self._decoding is None)
        if not finished or not self._thumb_failures:
            return
        info = _("sieť: %d, dekodér: %d") % (
            self._thumb_network_failures, self._thumb_decode_failures)
        if self._thumb_failures >= self._thumb_expected:
            self.set_status(_("Náhľady sa nepodarilo načítať (%s).") % info)
        else:
            self.set_status(_("Náhľady %d/%d (%s).") % (
                self._thumb_shown, self._thumb_expected, info))

    def _move(self, direction):
        if self._closed or not self.video_items:
            return
        next_index = move_index(self.selected, direction, len(self.video_items))
        if next_index == self.selected:
            return
        old_page = page_number(self.selected)
        self.selected = next_index
        if page_number(next_index) != old_page:
            self._render_page()
        else:
            # Moving focus is a deliberate user action, so normal status
            # updates become active again.
            self._status_override = False
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
            self.set_status("Zisťujem dostupnosť videa...", override=True)
            self.on_play(self.video_items[self.selected])

    def show_info(self):
        if self.selected >= 0 and callable(self.on_info):
            self.on_info(self.video_items[self.selected])

    def show_menu(self):
        if self.selected >= 0 and callable(self.on_favorite):
            self.on_favorite(self.video_items[self.selected])

    def save_favourite(self):
        # Keep old external callers safe; MENU now opens an action menu.
        self.show_menu()

    def next_page(self):
        if not self.video_items:
            return
        if self.selected + VISIBLE_TILES < len(self.video_items):
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
        # Skip the hidden text-result dialog and return to YouTube home.
        self.close("home")

    def new_search(self):
        self.close("search")
