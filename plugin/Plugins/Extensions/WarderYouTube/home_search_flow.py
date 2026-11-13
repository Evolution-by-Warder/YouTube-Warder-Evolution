# -*- coding: utf-8 -*-
"""A search flow hosted by Home, with no intermediary Enigma2 Screen.

The genuine system keyboard stays in Home's right pane while network search
runs in a worker. Only after the response arrives do we open the existing
native video grid directly. Closing its BLUE 'New search' action resumes Home's
embedded firmware keyboard, never the legacy standalone editor.

The old WarderYouTubeSearch screen remains available for legacy callers, but
is not part of the main Home -> Grid route.
"""
from twisted.internet.threads import deferToThread

from .api import SearchError, search_videos
from .search_backend import SearchBackendError, search_with_ytdlp, select_backend
from .settings import get_api_key
from .resolver import is_available
from .i18n import tr as _


class HomeSearchFlow:
    def __init__(self, home):
        self.home = home
        self.query = ""
        self.backend = None
        self.next_page_token = ""
        self.request = 0
        self.info_request = 0
        self.loading = False
        self.grid_open = False
        self.grid = None
        self.context_open = False
        self.disposed = False

    def dispose(self):
        self.disposed = True
        self.cancel_pending()
        self.info_request += 1
        self.grid = None

    def cancel_pending(self):
        self.request += 1
        self.loading = False

    def _status(self, message, override=False):
        if self.disposed or self.home._disposed:
            return
        grid = self.grid
        if self.grid_open and grid is not None and hasattr(grid, "set_status"):
            grid.set_status(message, override=override)
        elif self.home.index == 1:
            self.home["kb_feedback"].setText(_(message))

    def start(self, query, page_token=""):
        """Fetch from Home while its two panes remain on screen."""
        if (self.disposed or self.home._disposed or self.loading
                or self.grid_open or self.home._playback_active):
            return
        query = str(query or "").strip()
        if not query:
            self._status("Enter your YouTube search")
            return
        key = get_api_key()
        backend = select_backend(key, is_available())
        if not backend:
            self._status("No search backend: set an API key or install yt-dlp.")
            return
        if not page_token:
            self.next_page_token = ""
        self.query = query
        self.backend = backend
        self.loading = True
        self.request += 1
        token = self.request
        self._status("Vyhľadávanie na YouTube...")
        try:
            if backend == "api":
                work = deferToThread(search_videos, query, key, page_token)
            elif backend == "yt-dlp":
                work = deferToThread(search_with_ytdlp, query, page_token)
            else:
                raise ValueError("Unknown YouTube search backend")
            work.addCallbacks(
                lambda response: self._found(token, response),
                lambda failure: self._failed(token, failure)
            )
        except Exception:
            self._failed(token, None)

    def _found(self, token, response):
        if (self.disposed or self.home._disposed or token != self.request
                or self.home.index != 1):
            return
        self.loading = False
        try:
            items = response["items"]
            next_token = response.get("next_page_token") or ""
            if not isinstance(items, list):
                raise ValueError("Invalid YouTube results")
            self.next_page_token = str(next_token)
        except (KeyError, TypeError, AttributeError, ValueError):
            self._status("Unexpected response. Try another search.")
            return
        if not items:
            self._status("No videos found. Try another search.")
            return
        self._open_grid(items)

    def _failed(self, token, failure):
        if (self.disposed or self.home._disposed or token != self.request
                or self.home.index != 1):
            return
        self.loading = False
        error = getattr(failure, "value", None)
        # Never print upstream repr (it can include an API key).
        if isinstance(error, (SearchError, SearchBackendError)):
            message = str(error)
        else:
            message = "Unexpected search error. Please try again."
        self._status(message)

    def _open_grid(self, items):
        if self.disposed or self.grid_open:
            return
        from .grid import WarderYouTubeGrid
        self.grid_open = True
        try:
            self.grid = self.home.session.openWithCallback(
                self.grid_closed, WarderYouTubeGrid,
                items, self.query, bool(self.next_page_token),
                self.play_video, self.info_video, self.context_video
            )
        except Exception:
            self.grid = None
            self.grid_open = False
            self._status("Unable to open video results on this Enigma2 image.")

    def grid_closed(self, action=None):
        """Enigma2 invokes this after the results Screen is actually closed."""
        self.grid_open = False
        self.grid = None
        self.info_request += 1
        if self.disposed or self.home._disposed:
            return
        if action == "next":
            if self.query and self.next_page_token:
                self.start(self.query, self.next_page_token)
            return
        if action == "search":
            home = self.home
            home.index = 1
            home.focus_area = "nav"
            home.page_index = 0
            home._update_preview()
            if home.inline_keyboard is not None:
                home.inline_keyboard.reset()
            home._enter_keyboard_focus()
            return
        if action == "home":
            self.home.index = 0
            self.home.focus_area = "nav"
            self.home.page_index = 0
            self.home._update_preview()

    def play_video(self, video):
        if not self.disposed:
            self.home._play_selected(video)

    def info_video(self, video):
        if self.disposed or self.home._disposed or not self.grid_open:
            return
        from .info_ui import WarderYouTubeInfo
        key = get_api_key()
        if not key:
            self.home.session.open(
                WarderYouTubeInfo,
                "Názov: %s\nKanál: %s\n\n"
                "Podrobné údaje vyžadujú vlastný YouTube Data API kľúč." %
                (video.get("title") or "", video.get("channel") or "")
            )
            return
        from .video_metadata import fetch_video_info, VideoInfoError
        self.info_request += 1
        token = self.info_request
        self._status("Načítavam podrobnosti videa...", override=True)
        try:
            work = deferToThread(fetch_video_info, video["video_id"], key)
            work.addCallbacks(
                lambda info: self._info_ready(token, info),
                lambda error: self._info_failed(token, error)
            )
        except Exception:
            self._info_failed(token, None)

    def _info_ready(self, token, details):
        if (self.disposed or self.home._disposed or not self.grid_open
                or token != self.info_request):
            return
        from .info_ui import WarderYouTubeInfo
        message = (
            "%s\n\nKanál: %s\nDĺžka: %s\nPozretia: %s\n\n%s" %
            (details.get("title") or "", details.get("channel") or "",
             details.get("duration") or "", details.get("views") or "",
             (details.get("description") or "").replace("\r", "").strip()[:420])
        )
        self.home.session.open(WarderYouTubeInfo, message)

    def _info_failed(self, token, failure):
        if (self.disposed or self.home._disposed or not self.grid_open
                or token != self.info_request):
            return
        self._status("Nepodarilo sa načítať podrobnosti videa.", override=True)

    def context_video(self, video):
        if (self.disposed or self.home._disposed or self.context_open
                or not self.grid_open or self.home._playback_active):
            return
        from .context_menu import WarderYouTubeContext
        from .local_library import list_videos, LibraryError
        try:
            saved = any(v.get("video_id") == video.get("video_id")
                        for v in list_videos("favourites"))
            self.context_open = True
            self.home.session.openWithCallback(
                lambda action: self._context_done(action, video),
                WarderYouTubeContext, video, saved, "search"
            )
        except (LibraryError, RuntimeError, ValueError, TypeError):
            self.context_open = False
            self._status("Video actions unavailable.")

    def _context_done(self, action, video):
        self.context_open = False
        if self.disposed or self.home._disposed or not self.grid_open:
            return
        if action == "play":
            self.play_video(video)
        elif action == "info":
            self.info_video(video)
        elif action == "favorite":
            from .local_library import toggle_favourite, LibraryError
            try:
                saved = toggle_favourite(video)
                self._status("Add to favourites ✓" if saved
                             else "Remove from favourites ✓", override=True)
            except LibraryError as error:
                self._status(str(error), override=True)
        elif action == "search" and self.grid is not None:
            # The grid's close callback returns directly to Home's two panes.
            self.grid.close("search")
