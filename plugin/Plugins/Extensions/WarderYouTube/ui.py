# -*- coding: utf-8 -*-
"""Native two-pane Warder Home: immediate focus preview and genuine video tiles.

Navigation never opens modal dialogs, starts playback or installs updates
without an explicit remote action. No global Enigma2 skin or custom renderer.
"""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .skin import HOME_SKIN
from .i18n import tr as _
from .update_core import CURRENT_VERSION
from .grid_model import move_index
from .home_feed import popular_videos
from .home_thumbs import HomeThumbs
from .local_library import (
    LibraryError, list_videos, toggle_favourite, record_opened,
    remove_video, clear_videos,
)
from .settings import get_api_key, get_quality
from .resolver import ResolverError, resolve_video_streams, is_available
from .api import SearchError

SECTIONS = (
    ("Home", "Popular in Slovakia"),
    ("Search", "Enter your YouTube search"),
    ("Subscriptions", "Subscriptions are not supported yet."),
    ("History", "Recently played videos"),
    ("Playlists", "Playlists are not supported yet."),
    ("Favourites", "Saved videos"),
    ("Settings", "Current configuration"),
    ("Updates", "Update status (check only on request)"),
)
VISIBLE_TILES = 6


def preview_title(text, limit=49):
    result = " ".join(str(text or "").split())
    return result if len(result) <= limit else result[:limit - 1].rstrip() + "…"


class WarderYouTubeHome(Screen):
    skin = HOME_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.sections = [(_(name), _(description)) for name, description in SECTIONS]
        self.index = 0
        self.focus_area = "nav"
        self.tile_index = 0
        self.video_items = []
        self._mounted = False
        self._disposed = False
        self._popular_requested = False
        self._popular_loading = False
        self._popular_cache = None
        self._popular_error = False
        self._busy = False
        self._playback_active = False
        self._context_open = False
        self._confirm_open = False
        self._play_request = 0
        self.installed_version = CURRENT_VERSION
        self._version_checked = False

        self["brand"] = Label("YouTube Warder Evolution")
        self["version"] = Label(CURRENT_VERSION + "  •  Enigma2")
        for i, (name, description) in enumerate(self.sections):
            self["nav%d" % i] = Label(name)
            self["nav_focus%d" % i] = Label(" ")
        self["heading"] = Label("")
        self["subtitle"] = Label("")
        self["preview_message"] = Label("")
        self["status"] = Label("")
        for i in range(VISIBLE_TILES):
            self["preview_focus%d" % i] = Label(" ")
            self["preview_panel%d" % i] = Label(" ")
            self["preview_thumb%d" % i] = Pixmap()
            self["preview_title%d" % i] = Label("")
            self["preview_channel%d" % i] = Label("")
            self["detail%d" % i] = Label("")
        self["key_red"] = Label(_("Close"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("History"))
        self["key_blue"] = Label(_("Search"))
        self.thumbs = HomeThumbs(self)

        self["actions"] = ActionMap(
            ["NavigationActions", "OkCancelActions", "ColorActions",
             "MenuActions", "InfoActions"],
            {
                "up": self.up, "down": self.down, "left": self.left,
                "right": self.right, "ok": self.activate,
                "green": self.activate, "yellow": self.yellow,
                "blue": self.blue, "menu": self.context,
                "info": self.info, "red": self.back, "cancel": self.back,
            }, -1
        )
        self.onLayoutFinish.append(self._layout_ready)
        self.onShown.append(self._on_shown)
        self.onClose.append(self.dispose)

    def _layout_ready(self):
        if self._disposed or self._mounted:
            return
        self._mounted = True
        self.thumbs.start()
        self._update_nav()
        self._update_preview()

    def _on_shown(self):
        # An opkg read runs once in a worker; a stale hardcoded version in a
        # previously loaded UI must not be presented as installed truth.
        if not self._version_checked and not self._disposed:
            self._version_checked = True
            try:
                from .installed_version import read_installed_version
                task = deferToThread(read_installed_version)
                task.addCallbacks(self._version_ready, self._version_failed)
            except Exception:
                pass
        # Returning from player/library refreshes local data, but does not
        # automatically poll the update server or repeat the popular feed.
        if self._mounted and not self._disposed and not self._playback_active:
            if self.index in (0, 3, 5, 6, 7):
                self._update_preview()

    def _version_ready(self, version):
        if self._disposed or not isinstance(version, str):
            return
        self.installed_version = version
        self["version"].setText(version + "  •  Enigma2")
        if self._mounted and self.index == 7:
            self._update_preview()

    def _version_failed(self, failure):
        # Keep the current built-in version if opkg is not available.
        return

    def dispose(self):
        self._disposed = True
        self._play_request += 1
        self.thumbs.close()

    def _update_nav(self):
        if not self._mounted or self._disposed:
            return
        for i in range(len(self.sections)):
            focus = self["nav_focus%d" % i]
            if self.focus_area == "nav" and self.index == i:
                focus.show()
            else:
                focus.hide()

    def _clear_preview(self):
        self.thumbs.show([])
        for i in range(VISIBLE_TILES):
            for prefix in ("preview_focus", "preview_panel", "preview_thumb",
                           "preview_title", "preview_channel", "detail"):
                self["%s%d" % (prefix, i)].hide()
        self["preview_message"].hide()
        self.video_items = []
        self.tile_index = 0

    def _show_message(self, message, details=None):
        self._clear_preview()
        self["preview_message"].setText(_(message))
        self["preview_message"].show()
        if details:
            self["status"].setText(_(details))

    def _show_details(self, rows):
        self._clear_preview()
        for i, text in enumerate(rows[:VISIBLE_TILES]):
            widget = self["detail%d" % i]
            widget.setText(_(text))
            widget.show()

    def _show_tiles(self, items, subtitle):
        self._clear_preview()
        self.video_items = list(items[:VISIBLE_TILES])
        self["subtitle"].setText(_(subtitle))
        if not self.video_items:
            self["preview_message"].setText(_("No saved videos in this section."))
            self["preview_message"].show()
            return
        for i, video in enumerate(self.video_items):
            self["preview_panel%d" % i].show()
            title = self["preview_title%d" % i]
            channel = self["preview_channel%d" % i]
            title.setText(preview_title(video.get("title")))
            channel.setText(str(video.get("channel") or "")[:43])
            title.show()
            channel.show()
        self.thumbs.show(self.video_items)
        self._update_tile_focus()

    def _update_tile_focus(self):
        if self._disposed or not self._mounted:
            return
        for i in range(VISIBLE_TILES):
            focus = self["preview_focus%d" % i]
            if self.focus_area == "tiles" and i == self.tile_index and i < len(self.video_items):
                focus.show()
            else:
                focus.hide()
        if self.focus_area == "tiles" and self.video_items:
            self["status"].setText(preview_title(self.video_items[self.tile_index].get("title"), 85))

    def _local_items(self, kind):
        try:
            return list_videos(kind)
        except LibraryError as error:
            self["status"].setText(str(error))
            return []

    def _fallback_home(self):
        recent = self._local_items("history")
        if recent:
            self._show_tiles(recent, "Recently played (offline)")
            return
        saved = self._local_items("favourites")
        if saved:
            self._show_tiles(saved, "Favourites (offline)")
            return
        self._show_message(
            "Set an API key in Settings for popular videos; "
            "your recently played and saved videos will appear here."
        )

    def _request_popular(self):
        if self._popular_requested or self._disposed:
            return
        key = get_api_key()
        if not key:
            self._fallback_home()
            return
        self._popular_requested = True
        self._popular_loading = True
        self._show_message("Loading popular videos for Slovakia…")
        try:
            work = deferToThread(popular_videos, key)
            work.addCallbacks(self._popular_loaded, self._popular_failed)
        except Exception:
            self._popular_failed(None)

    def _popular_loaded(self, videos):
        if self._disposed:
            return
        self._popular_loading = False
        self._popular_cache = videos[:12] if isinstance(videos, list) else []
        if self.index == 0:
            if self._popular_cache:
                self._show_tiles(self._popular_cache, "Popular in Slovakia")
            else:
                self._fallback_home()

    def _popular_failed(self, failure):
        if self._disposed:
            return
        self._popular_loading = False
        self._popular_error = True
        if self.index == 0:
            self._fallback_home()
            self["status"].setText(_("Popular videos are temporarily unavailable."))

    def _update_preview(self):
        if self._disposed or not self._mounted:
            return
        self._clear_preview()
        self["heading"].setText(self.sections[self.index][0])
        self["subtitle"].setText(self.sections[self.index][1])
        self["status"].setText(_("Up/Down: sections • Right: videos • OK: open"))
        if self.index == 0:
            if self._popular_cache:
                self._show_tiles(self._popular_cache, "Popular in Slovakia")
            elif self._popular_loading:
                self._show_message("Loading popular videos for Slovakia…")
            elif self._popular_error or not get_api_key():
                self._fallback_home()
            else:
                self._request_popular()
        elif self.index == 1:
            self._show_message(
                "Press OK to enter a search phrase. "
                "The system keyboard opens inside Warder."
            )
        elif self.index == 2:
            self._show_message("Subscriptions are not supported yet.")
        elif self.index == 3:
            self._show_tiles(self._local_items("history"), "Recently played videos")
        elif self.index == 4:
            self._show_message("Playlists are not supported yet.")
        elif self.index == 5:
            self._show_tiles(self._local_items("favourites"), "Saved videos")
        elif self.index == 6:
            self._show_details([
                _("API key") + ": " + (_("Configured") if get_api_key() else _("Not configured")),
                _("Preferred quality") + ": %sp" % get_quality(),
                "yt-dlp: " + (_("Available") if is_available() else _("Not installed")),
                _("Language from Enigma2"),
                _("API stored unencrypted"),
            ])
        elif self.index == 7:
            self._show_details([
                _("Installed") + ": " + self.installed_version,
                _("Channel") + ": " + _("Testing"),
                _("Updates") + ": " + _("Check on demand"),
            ])
        self._update_nav()
        self._update_tile_focus()
        self._update_keys()

    def _update_keys(self):
        self["key_red"].setText(_("Back") if self.focus_area == "tiles" else _("Close"))
        self["key_green"].setText(
            _("Play video") if self.focus_area == "tiles" and self.video_items else _("Open")
        )
        self["key_yellow"].setText(_("History"))
        self["key_blue"].setText(_("Search"))

    def _select_nav(self, index):
        if self._disposed or self._busy or self._playback_active or self._context_open:
            return
        index = max(0, min(index, len(self.sections) - 1))
        if self.index == index and self.focus_area == "nav":
            return
        self.index = index
        self.focus_area = "nav"
        self._update_preview()

    def up(self):
        if self.focus_area == "nav":
            self._select_nav(self.index - 1)
        else:
            self._move_tile("up")

    def down(self):
        if self.focus_area == "nav":
            self._select_nav(self.index + 1)
        else:
            self._move_tile("down")

    def left(self):
        if self.focus_area == "tiles":
            if self.tile_index % 3 == 0:
                self.focus_area = "nav"
                self._update_nav()
                self._update_tile_focus()
                self._update_keys()
            else:
                self._move_tile("left")

    def right(self):
        if self.focus_area == "nav":
            self._enter_tiles()
        else:
            self._move_tile("right")

    def _move_tile(self, direction):
        if not self.video_items or self._busy or self._playback_active or self._context_open:
            return
        next_index = move_index(self.tile_index, direction, len(self.video_items))
        if next_index != self.tile_index:
            self.tile_index = next_index
            self._update_tile_focus()

    def _enter_tiles(self):
        if self.video_items and self.focus_area == "nav":
            self.focus_area = "tiles"
            self.tile_index = 0
            self._update_nav()
            self._update_tile_focus()
            self._update_keys()

    def back(self):
        if self.focus_area == "tiles":
            self.focus_area = "nav"
            self["status"].setText(_("Up/Down: sections • Right: videos • OK: open"))
            self._update_nav()
            self._update_tile_focus()
            self._update_keys()
        else:
            self.close()

    def yellow(self):
        if self.focus_area == "tiles":
            self.context()
        else:
            self._select_nav(3)

    def blue(self):
        self._open_index(1)

    def activate(self):
        if self._disposed or self._busy or self._playback_active or self._context_open:
            return
        if self.focus_area == "tiles":
            self._play_selected()
        elif self.index in (0, 3, 5) and self.video_items:
            self._enter_tiles()
        else:
            self._open_index(self.index)

    def _open_index(self, index):
        if self._disposed or self._busy or self._context_open or self._playback_active:
            return
        if index == 1:
            from .search import WarderYouTubeSearch
            self.session.open(WarderYouTubeSearch)
        elif index in (3, 5):
            from .library_ui import WarderYouTubeLibrary
            self.session.open(WarderYouTubeLibrary,
                              "history" if index == 3 else "favourites")
        elif index == 6:
            from .settings import WarderYouTubeSettings
            self.session.open(WarderYouTubeSettings)
        elif index == 7:
            from .update_ui import WarderYouTubeUpdateCheck
            self.session.open(WarderYouTubeUpdateCheck)
        elif index == 0:
            if not self.video_items:
                self._open_index(6)
        else:
            self["status"].setText(_("This section is not supported yet."))

    def selected_video(self):
        if (self.focus_area == "tiles" and
                0 <= self.tile_index < len(self.video_items)):
            return self.video_items[self.tile_index]
        return None

    def info(self):
        item = self.selected_video()
        if item is None or self._busy or self._playback_active:
            return
        from .info_ui import WarderYouTubeInfo
        self.session.open(
            WarderYouTubeInfo,
            "%s\n%s\n%s" % (item.get("title", ""), item.get("channel", ""),
                             item.get("video_id", ""))
        )

    def context(self):
        item = self.selected_video()
        if (item is None or self._context_open or self._busy or
                self._playback_active or self._disposed):
            return
        from .context_menu import WarderYouTubeContext
        mode = "history" if self.index == 3 else (
            "favourites" if self.index == 5 else "search"
        )
        saved = any(v["video_id"] == item.get("video_id")
                    for v in self._local_items("favourites"))
        self._context_open = True
        try:
            self.session.openWithCallback(
                lambda action: self._context_done(action, item),
                WarderYouTubeContext, item, saved, mode
            )
        except Exception:
            self._context_open = False
            self["status"].setText(_("Video actions unavailable."))

    def _context_done(self, action, item):
        self._context_open = False
        if self._disposed or action is None:
            return
        if action == "play":
            self._play_selected()
        elif action == "info":
            self.info()
        elif action == "search":
            self._open_index(1)
        elif action == "favorite":
            try:
                toggle_favourite(item)
                self._update_preview()
            except LibraryError as error:
                self["status"].setText(str(error))
        elif action == "remove" and self.index in (3, 5):
            try:
                remove_video("history" if self.index == 3 else "favourites",
                             item["video_id"])
                self.focus_area = "nav"
                self._update_preview()
            except LibraryError as error:
                self["status"].setText(str(error))
        elif action == "clear" and self.index in (3, 5):
            from .confirm_ui import WarderYouTubeConfirm
            self._confirm_open = True
            self.session.openWithCallback(
                self._clear_confirmed, WarderYouTubeConfirm,
                _("Clear") + ": " + self.sections[self.index][0] + "?"
            )

    def _clear_confirmed(self, confirmed):
        self._confirm_open = False
        if not confirmed or self._disposed or self.index not in (3, 5):
            return
        try:
            clear_videos("history" if self.index == 3 else "favourites")
            self.focus_area = "nav"
            self._update_preview()
        except LibraryError as error:
            self["status"].setText(str(error))

    def _play_selected(self):
        video = self.selected_video()
        if (video is None or self._disposed or self._busy or
                self._playback_active or self._context_open):
            return
        self._busy = True
        self._play_request += 1
        token = self._play_request
        self["status"].setText(_("Looking for a compatible video stream…"))
        try:
            from .player import dash_available
            task = deferToThread(
                resolve_video_streams, video["video_id"],
                quality=get_quality(), dash=dash_available()
            )
            task.addCallbacks(
                lambda streams: self._play_ready(token, video, streams),
                lambda failure: self._play_failed(token, failure)
            )
        except Exception:
            self._busy = False
            self["status"].setText(_("Unable to start playback."))

    def _play_ready(self, token, video, streams):
        if self._disposed or token != self._play_request:
            return
        self._busy = False
        if self._playback_active:
            return
        self._playback_active = True
        try:
            from .player import open_player
            open_player(self.session, streams, video["title"],
                        on_close=self._player_closed)
        except Exception:
            self._playback_active = False
            self["status"].setText(_("Unable to open Enigma2 player."))
            return
        try:
            record_opened(video)
        except LibraryError:
            pass

    def _play_failed(self, token, failure):
        if self._disposed or token != self._play_request:
            return
        self._busy = False
        error = getattr(failure, "value", None)
        self["status"].setText(
            str(error) if isinstance(error, ResolverError)
            else _("Unable to obtain a video stream.")
        )

    def _player_closed(self, failed=False, *args):
        self._playback_active = False
        if not self._disposed:
            self._update_preview()
