# -*- coding: utf-8 -*-
"""Native YouTube search and optional experimental playback.

Background jobs use Twisted workers; callbacks update Enigma2 only on reactor
thread. yt-dlp is optional and is never installed by the plugin.
"""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

from twisted.internet.threads import deferToThread

from .api import SearchError, search_videos
from .search_backend import SearchBackendError, search_with_ytdlp, select_backend
from .resolver import ResolverError, is_available, resolve_video_streams
from .settings import WarderYouTubeSettings, get_api_key, get_quality
from .video_metadata import VideoInfoError, fetch_video_info
from .skin import SEARCH_SKIN
from .local_library import toggle_favourite, record_opened, list_videos, LibraryError
from .i18n import tr as _
from .keyboard import WarderYouTubeKeyboard
from .context_menu import WarderYouTubeContext
from .info_ui import WarderYouTubeInfo


class WarderYouTubeSearch(Screen):
    skin = SEARCH_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.query = ""
        self.video_items = []
        self.page_token = ""
        self.next_page_token = ""
        self.busy = False
        # A native MoviePlayer dialog remains active after stream resolution.
        # Keep this independent of background worker busy state.
        self.playback_active = False
        self.closed = False
        self.request_version = 0
        self.active_grid = None
        self.search_backend = None
        self._did_initial_prompt = False
        self.context_open = False

        self["title"] = Label("YouTube Warder Evolution  /  " + _("Search"))
        self["query"] = Label(_("Search videos"))
        self["results"] = MenuList([])
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Next"))
        self["key_yellow"] = Label(_("Settings"))
        self["key_blue"] = Label(_("New search"))
        self["details"] = Label("")
        self["status"] = Label("BLUE: search     YELLOW: settings")
        self["footer"] = Label(
            "UP/DOWN: select    OK: play    BLUE: search    "
            "GREEN: next page    YELLOW: settings    EXIT: back"
        )
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "InfoActions", "MenuActions"],
            {"ok": self.open_selected, "info": self.info_selected,
             "menu": self.favorite_selected,
             "cancel": self.close,
             "red": self.close, "blue": self.open_keyboard,
             "green": self.next_page, "yellow": self.open_settings},
            -1
        )
        self["results"].onSelectionChanged.append(self.selection_changed)
        # onLayoutFinish runs during applySkin, before Session.in_exec is True.
        # Modal VirtualKeyboard must open only after the screen enters exec.
        self.onShown.append(self.first_open)
        self.onClose.append(self.mark_closed)

    def first_open(self):
        # onShown fires again when returning from VirtualKeyboard or MoviePlayer.
        # Only the first activation may open the initial keyboard.
        if self.closed or self._did_initial_prompt:
            return
        self._did_initial_prompt = True
        if select_backend(get_api_key(), is_available()):
            self.open_keyboard()
        else:
            self["status"].setText(
                _("Search needs your API key or an installed yt-dlp. "
                  "Press YELLOW to configure Settings.")
            )

    def mark_closed(self):
        self.closed = True
        self.request_version += 1

    def open_settings(self):
        if not self.busy:
            self.session.open(WarderYouTubeSettings)

    def open_keyboard(self):
        if self.busy or self.closed:
            return
        if not select_backend(get_api_key(), is_available()):
            self["status"].setText(
                _("No search backend: set an API key or install yt-dlp.")
            )
            return
        self.session.openWithCallback(
            self.search_submitted, WarderYouTubeKeyboard,
            value=self.query, title=_("Enter your YouTube search")
        )

    def search_submitted(self, query):
        if query is None or not query.strip():
            return
        self.query = query.strip()
        self.search_backend = select_backend(get_api_key(), is_available())
        self.page_token = ""
        self.next_page_token = ""
        self.video_items = []
        self["results"].setList([])
        self["details"].setText("")
        self._load_page("")

    def next_page(self):
        if not self.busy and self.query and self.next_page_token:
            self._load_page(self.next_page_token)

    def _load_page(self, page_token):
        if self.busy:
            return
        self.busy = True
        self.request_version += 1
        version = self.request_version
        self["query"].setText(_("Search") + ": " + self.query[:60])
        self["status"].setText(_("Internet search") + "...")
        # Both backends run in workers. Never block the Enigma2 GUI thread.
        if self.search_backend == "api":
            deferred = deferToThread(
                search_videos, self.query, get_api_key(), page_token
            )
        elif self.search_backend == "yt-dlp":
            deferred = deferToThread(
                search_with_ytdlp, self.query, page_token
            )
        else:
            self.busy = False
            self["status"].setText("No search backend is configured.")
            return
        deferred.addCallbacks(
            lambda response: self.receive_results(version, page_token, response),
            lambda error: self.receive_error(version, error)
        )

    def receive_results(self, version, page_token, response):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        self.page_token = page_token
        self.next_page_token = response["next_page_token"]
        self.video_items = response["items"]
        self["results"].setList([
            item["title"][:80] +
            ("  |  " + item["channel"][:35] if item["channel"] else "")
            for item in self.video_items
        ])
        self.selection_changed()
        if not self.video_items:
            self["status"].setText(_("No videos found. Press BLUE to search again."))
        else:
            suffix = "  |  GREEN: next page" if self.next_page_token else ""
            self["status"].setText(
                _("%d video(s) found%s") % (len(self.video_items), suffix)
            )
            self.open_grid()

    def receive_error(self, version, failure):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        error = getattr(failure, "value", None)
        if isinstance(error, (SearchError, SearchBackendError)):
            message = str(error)
        else:
            message = "Unexpected error. Please try another search."
        # Do NOT log exception repr: urllib may embed an API key.
        self["status"].setText(message)

    def selection_changed(self):
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.video_items):
            item = self.video_items[index]
            self["details"].setText(
                "%s   |   %s" % (item["channel"], item["published_at"])
            )
        else:
            self["details"].setText("")

    def open_grid(self):
        if self.closed or not self.video_items or self.active_grid is not None:
            return
        # Imports stay lazy: graphics stay optional on older Enigma2 images.
        try:
            from .grid import WarderYouTubeGrid
            self.active_grid = self.session.openWithCallback(
                self.grid_closed, WarderYouTubeGrid,
                self.video_items, self.query, bool(self.next_page_token),
                self.play_video, self.info_video, self.show_context
            )
        except Exception:
            self.active_grid = None
            self["status"].setText(
                "Thumbnail grid not supported here; text results remain usable."
            )

    def grid_closed(self, action=None):
        self.active_grid = None
        # Invalidate video resolution if the card screen was dismissed.
        if self.busy:
            self.request_version += 1
            self.busy = False
        if not self.closed and action == "search":
            self.open_keyboard()
        elif not self.closed and action == "next":
            self.next_page()
        elif not self.closed and action == "home":
            # EXIT from the visual cards skips the redundant underlying list.
            self.close()

    def show_play_status(self, message):
        self["status"].setText(message)
        if self.active_grid is not None and not self.active_grid._closed:
            self.active_grid.set_status(message, override=True)

    def open_selected(self):
        if self.busy:
            return
        index = self["results"].getCurrentIndex()
        if not (0 <= index < len(self.video_items)):
            self.open_keyboard()
            return
        self.play_video(self.video_items[index])

    def favorite_selected(self):
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.video_items):
            self.show_context(self.video_items[index])

    def show_context(self, video):
        if self.busy or self.closed or self.playback_active or self.context_open:
            return
        try:
            saved = any(x["video_id"] == video.get("video_id")
                        for x in list_videos("favourites"))
            self.context_open = True
            self.session.openWithCallback(
                lambda action: self.context_selected(action, video),
                WarderYouTubeContext, video, saved)
        except LibraryError as error:
            self.context_open = False
            self.show_play_status(str(error))
        except Exception:
            self.context_open = False
            self.show_play_status(_("Video actions") + ": " + _("Cancel"))

    def context_selected(self, action, video):
        self.context_open = False
        if self.closed or action is None:
            return
        if action == "play":
            self.play_video(video)
        elif action == "favorite":
            self.toggle_favourite(video)
        elif action == "info":
            self.info_video(video)
        elif action == "search":
            self.open_keyboard()

    def toggle_favourite(self, video):
        if self.busy or self.closed or self.playback_active:
            return
        try:
            saved = toggle_favourite(video)
        except LibraryError as error:
            self.show_play_status(str(error))
            return
        self.show_play_status(
            _("Add to favourites") + " ✓" if saved
            else _("Remove from favourites") + " ✓")

    def info_selected(self):
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.video_items):
            self.info_video(self.video_items[index])

    def info_video(self, video):
        if self.busy or self.closed or self.playback_active:
            return
        api_key = get_api_key()
        if not api_key:
            self.session.open(
                WarderYouTubeInfo,
                "Názov: %s\nKanál: %s\n\n"
                "Podrobné údaje vyžadujú vlastný YouTube Data API kľúč." %
                (video.get("title") or "", video.get("channel") or "")
            )
            return
        self.busy = True
        self.request_version += 1
        version = self.request_version
        self.show_play_status("Načítavam podrobnosti videa...")
        deferred = deferToThread(fetch_video_info, video["video_id"], api_key)
        deferred.addCallbacks(
            lambda details: self.info_ready(version, details),
            lambda failure: self.info_failed(version, failure)
        )

    def info_ready(self, version, details):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        description = (details.get("description") or "").replace("\r", "").strip()
        message = (
            "%s\n\nKanál: %s\nDĺžka: %s\nPozretia: %s\n\n%s" %
            (details["title"], details["channel"], details["duration"],
             details["views"], description[:420])
        )
        self.show_play_status("Podrobnosti videa načítané.")
        self.session.open(WarderYouTubeInfo, message)

    def info_failed(self, version, failure):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        error = getattr(failure, "value", None)
        if isinstance(error, VideoInfoError):
            self.show_play_status(str(error))
        else:
            self.show_play_status("Nepodarilo sa načítať podrobnosti videa.")

    def play_video(self, video):
        if self.busy or self.closed or self.playback_active:
            return
        # The bundled Warder Radio resolver also works without yt-dlp.
        self.busy = True
        self.request_version += 1
        version = self.request_version
        self.show_play_status("Hľadám video stream (MP4 / HLS / DASH)...")
        from .player import dash_available
        deferred = deferToThread(
            resolve_video_streams, video["video_id"],
            quality=get_quality(), dash=dash_available()
        )
        deferred.addCallbacks(
            lambda streams: self.play_resolved(version, video, streams),
            lambda failure: self.play_failed(version, failure)
        )

    def play_resolved(self, version, video, streams):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        if self.playback_active:
            return
        self.playback_active = True
        self.show_play_status(
            "Otváram prehrávač Enigma2. EXIT: návrat k videám."
        )
        try:
            # Do not import MoviePlayer until a stream was actually resolved.
            from .player import open_player
            open_player(
                self.session, streams, video["title"],
                on_close=self.playback_finished
            )
            # Only a successfully opened player is added to recent videos.
            try:
                record_opened(video)
            except LibraryError:
                # History write failure must never interrupt video playback.
                pass
        except Exception:
            self.playback_active = False
            # Do not leak URLs or upstream errors into GUI messages or logs.
            self.show_play_status(
                "Enigma2 could not open the player on this image."
            )

    def play_failed(self, version, failure):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        error = getattr(failure, "value", None)
        if isinstance(error, ResolverError):
            self.show_play_status(str(error))
        else:
            self.show_play_status(
                "Unexpected stream resolution error. Try another video."
            )

    def playback_finished(self, failed=False, *args):
        self.playback_active = False
        if self.closed:
            return
        if failed is True:
            self.show_play_status(
                "Video sa nepodarilo prehrať ani záložnými streamami. "
                "Skúste iné video alebo kvalitu 360p."
            )
        else:
            self.show_play_status(
                "Prehrávanie ukončené. OK: ďalšie video."
            )
