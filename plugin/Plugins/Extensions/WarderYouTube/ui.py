# -*- coding: utf-8 -*-
"""Native two-pane Warder Home: immediate focus preview and genuine video tiles.

Navigation never opens modal dialogs, starts playback or installs updates
without an explicit remote action. No global Enigma2 skin or custom renderer.
"""
from .header_ui import add_header
from time import monotonic
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .skin import HOME_SKIN
from .i18n import tr as _
from .update_core import CURRENT_VERSION
from .grid_model import move_index
from .system_keyboard_pane import SystemKeyboardPane
from .home_feed import popular_videos_page, public_home_videos
from .home_personalization import VISIBLE_CHIPS, build_home_chips, dedupe_videos
from .home_thumbs import HomeThumbs
from .tile_scrollbar import TilePageScrollbar
from .local_library import (
    LibraryError, list_videos, toggle_favourite, record_opened,
    remove_video, clear_videos,
)
from .settings import get_api_key, get_quality
from .resolver import ResolverError, resolve_video_streams, is_available
from .api import SearchError
from .video_metadata import fetch_video_info
from .video_info_display import format_video_info

SECTIONS = (
    ("Home", "Personal YouTube selection"),
    ("Search", "Enter your YouTube search"),
    ("Subscriptions", "Your YouTube subscriptions"),
    ("History", "Recently played videos"),
    ("Playlists", "Playlists are not supported yet."),
    ("Favourites", "Saved videos"),
    ("Settings", "Current configuration"),
    ("Updates", "Update status (check only on request)"),
)
VISIBLE_TILES = 6
POPULAR_REFRESH_SECONDS = 600


def preview_title(text, limit=49):
    result = " ".join(str(text or "").split())
    return result if len(result) <= limit else result[:limit - 1].rstrip() + "…"


def _discover_home_subscriptions():
    """Read-only authenticated subscriptions in a Twisted worker, not GUI."""
    try:
        from .subscriptions_auth import account_connected, access_token
        from .subscriptions_api import subscriptions_list
        if account_connected():
            channels = subscriptions_list(access_token())
            return {"connected": True, "channels": channels}
    except Exception:
        return {"connected": False, "channels": []}
    return {"connected": False, "channels": []}


def _load_personal_channel_videos(chip):
    """Retrieve actual channel uploads lazily; never fake YouTube web Mixes."""
    from .subscriptions_auth import access_token
    from .subscriptions_api import (recent_subscription_videos, uploads_playlists,
                                    playlist_videos, SubscriptionsApiError)
    token = access_token()
    if chip.get("kind") == "recent":
        videos, channels = recent_subscription_videos(token)
        return dedupe_videos(videos)
    identifiers = list(chip.get("channels") or ())[:8]
    if not identifiers:
        return []
    playlists = uploads_playlists(identifiers, token)
    videos = []
    for channel_id in identifiers:
        playlist = playlists.get(channel_id)
        if not playlist:
            continue
        try:
            items = playlist_videos(
                playlist, token, limit=50 if chip.get("kind") == "channel" else 10)
            videos.extend(items)
        except SubscriptionsApiError:
            continue
    videos.sort(key=lambda v: (v.get("published_at") or "",
                              v.get("video_id") or ""), reverse=True)
    return dedupe_videos(videos)


class WarderYouTubeHome(Screen):
    skin = HOME_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        add_header(self)
        self.sections = [(_(name), _(description)) for name, description in SECTIONS]
        self.index = 0
        self.focus_area = "nav"
        self.tile_index = 0
        # The inline search panel uses Enigma2's ORIGINAL VirtualKeyBoard
        # list + Input. No homemade letter matrix, UI-renderer or modal Screen.
        self.kb_shown = False
        self.inline_keyboard = None
        self.kb_unavailable_reason = ""
        self._home_search_flow = None
        self.video_items = []
        self.page_index = 0
        self._section_items = []
        self._section_subtitle = ""
        self._popular_fetched_at = 0
        self._mounted = False
        self._disposed = False
        self._popular_requested = False
        self._popular_loading = False
        self._popular_cache = None
        self._popular_error = False
        self._popular_source = "api"
        self._popular_request_epoch = 0
        self._popular_next_page_token = ""
        self._popular_total_results = None
        self._popular_more_loading = False
        self._category_index = 0
        self._category_cursor = 0
        self._category_offset = 0
        self._home_chips = build_home_chips()
        self._personal_requested = False
        self._personal_fetched_at = 0
        self._personal_epoch = 0
        self._personal_video_epoch = 0
        self._personal_video_cache = {}
        self._auth_maybe_changed = False
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
            self["nav_focus%d" % i] = Pixmap()
        self["heading"] = Label("")
        self["subtitle"] = Label("")
        self["page_info"] = Label("")
        for i in range(VISIBLE_CHIPS):
            self["category_panel%d" % i] = Label(" ")
            self["category_focus%d" % i] = Label(" ")
            self["category%d" % i] = Label("")
        self["category_more"] = Label("")
        self["kb_hint"] = Label("")
        self["kb_feedback"] = Label("")
        try:
            self.inline_keyboard = SystemKeyboardPane(
                session, self._keyboard_native_submit, self._leave_keyboard_focus
            )
            # Attach precisely the firmware's Components.Input/MenuList to
            # Home so Enigma2 can create their native GUI widgets here.
            self["kb_system_input"] = self.inline_keyboard.input
            self["kb_system_list"] = self.inline_keyboard.list
        except (ImportError, AttributeError, ValueError, RuntimeError, TypeError) as error:
            self.kb_unavailable_reason = type(error).__name__
            # Graceful incompatible-image diagnostic instead of a fake keypad.
            self.inline_keyboard = None
            self["kb_system_input"] = Label("")
            self["kb_system_list"] = Label("")
        self["preview_message"] = Label("")
        self["status"] = Label("")
        for i in range(VISIBLE_TILES):
            self["preview_focus%d" % i] = Pixmap()
            self["preview_panel%d" % i] = Label(" ")
            self["preview_border%d" % i] = Label(" ")
            self["preview_thumb%d" % i] = Pixmap()
            self["preview_title%d" % i] = Label("")
            self["preview_channel%d" % i] = Label("")
            self["detail%d" % i] = Label("")
        self["key_red"] = Label(_("Close"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("History"))
        self["key_blue"] = Label(_("Search"))
        self.thumbs = HomeThumbs(self)
        self["video_scroll_track"] = Label(" ")
        self["video_scroll_thumb"] = Label(" ")
        self.page_scroll = TilePageScrollbar(
            self["video_scroll_track"], self["video_scroll_thumb"],
            1874, 252, 5, 667
        )

        self["actions"] = ActionMap(
            ["NavigationActions", "OkCancelActions", "ColorActions",
             "MenuActions", "InfoActions"],
            {
                "up": self.up, "down": self.down, "left": self.left,
                "right": self.right, "ok": self.activate,
                "green": self.green, "yellow": self.yellow,
                "blue": self.blue, "menu": self.menu,
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
        if self.inline_keyboard is not None:
            try:
                self.inline_keyboard.layout_finished()
            except (ImportError, AttributeError, ValueError, RuntimeError, TypeError) as error:
                self.kb_unavailable_reason = type(error).__name__
                self.inline_keyboard = None
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
        # Discover authenticated subscriptions away from the GUI thread.
        # Returning from Odbery after login or logout refreshes chip sources.
        if self._mounted and not self._disposed:
            self._request_personalization(force=self._auth_maybe_changed)
            self._auth_maybe_changed = False
        # Returning from player/library refreshes local data, but does not
        # automatically poll the update server or repeat the popular feed.
        if self._mounted and not self._disposed and not self._playback_active:
            if self.index in (0, 1, 3, 5, 6, 7):
                self._update_preview()
            if (self.index == 0 and self._popular_cache
                    and not self._popular_loading
                    and monotonic() - self._popular_fetched_at > POPULAR_REFRESH_SECONDS):
                # Recheck real YouTube only after the bounded freshness window;
                # keep the previous visible tiles while the worker runs.
                self._popular_requested = False
                self._request_popular(refresh=True)

    def _version_ready(self, version):
        if self._disposed or not isinstance(version, str):
            return
        self.installed_version = version
        self["version"].setText(version + "  •  Enigma2")
        self["hdr_version"].setText(version)
        if self._mounted and self.index == 7:
            self._update_preview()

    def _version_failed(self, failure):
        # Keep the current built-in version if opkg is not available.
        return

    def dispose(self):
        self._disposed = True
        self._play_request += 1
        if self._home_search_flow is not None:
            self._home_search_flow.dispose()
        if self.inline_keyboard is not None:
            self.inline_keyboard.cleanup()
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

    def _selected_home_chip(self):
        if 0 <= self._category_index < len(self._home_chips):
            return self._home_chips[self._category_index]
        return self._home_chips[0]

    def _render_categories(self):
        visible = self.index == 0
        if visible:
            self["subtitle"].hide()
        else:
            self["subtitle"].show()
        selection = (self._category_cursor if self.focus_area == "categories"
                     else self._category_index)
        if selection < self._category_offset:
            self._category_offset = selection
        if selection >= self._category_offset + VISIBLE_CHIPS:
            self._category_offset = selection - VISIBLE_CHIPS + 1
        self._category_offset = max(0, min(
            self._category_offset, max(0, len(self._home_chips) - VISIBLE_CHIPS)))
        for slot in range(VISIBLE_CHIPS):
            absolute = self._category_offset + slot
            display = visible and absolute < len(self._home_chips)
            for prefix in ("category_panel", "category"):
                widget = self["%s%d" % (prefix, slot)]
                if display:
                    widget.show()
                else:
                    widget.hide()
            if display:
                self["category%d" % slot].setText(
                    _(self._home_chips[absolute]["label"]))
            focus = self["category_focus%d" % slot]
            if display and absolute == selection:
                focus.show()
            else:
                focus.hide()
        if visible and len(self._home_chips) > VISIBLE_CHIPS:
            self["category_more"].setText(
                "›" if self._category_offset + VISIBLE_CHIPS < len(self._home_chips)
                else "‹")
            self["category_more"].show()
        else:
            self["category_more"].hide()

    def _enter_categories(self):
        if self.index != 0 or self._disposed:
            return
        self.focus_area = "categories"
        self._category_cursor = self._category_index
        self["status"].setText(_("Choose a category and press OK"))
        self._update_nav()
        self._update_tile_focus()
        self._render_categories()
        self._update_keys()

    def _choose_category(self):
        if self.index != 0 or self._disposed or self._busy or self._playback_active:
            return
        if self._category_cursor == self._category_index and self.video_items:
            self.focus_area = "tiles"
            self.tile_index = 0
            self._update_tile_focus()
            self._render_categories()
            self._update_keys()
            return
        self._category_index = self._category_cursor
        self._personal_video_epoch += 1  # ignore callbacks for older chips
        self.page_index = 0
        self._show_selected_home_chip()
        self._render_categories()
        self._update_keys()

    def _request_personalization(self, force=False):
        if self._disposed or self._personal_requested:
            return
        if (not force and self._personal_fetched_at
                and monotonic() - self._personal_fetched_at < 300):
            return
        self._personal_requested = True
        self._personal_epoch += 1
        epoch = self._personal_epoch
        try:
            task = deferToThread(_discover_home_subscriptions)
            task.addCallbacks(
                lambda data: self._personalization_ready(data, epoch),
                lambda err: self._personalization_failed(epoch))
        except Exception:
            self._personalization_failed(epoch)

    def _personalization_ready(self, data, epoch):
        if self._disposed or epoch != self._personal_epoch:
            return
        self._personal_requested = False
        self._personal_fetched_at = monotonic()
        if not isinstance(data, dict):
            return
        old_id = self._selected_home_chip()["id"]
        cursor_id = (self._home_chips[self._category_cursor]["id"]
                     if 0 <= self._category_cursor < len(self._home_chips)
                     else old_id)
        updated = build_home_chips(
            channels=data.get("channels") or (),
            authenticated=bool(data.get("connected")))
        lookup = {chip["id"]: i for i, chip in enumerate(updated)}
        if [item["id"] for item in updated] != [
                item["id"] for item in self._home_chips]:
            self._personal_video_cache.clear()
            self._personal_video_epoch += 1
        self._home_chips = updated
        self._category_index = lookup.get(old_id, 0)
        self._category_cursor = lookup.get(cursor_id, self._category_index)
        if old_id not in lookup and self.index == 0:
            self.page_index = 0
            self._show_selected_home_chip()
        self._render_categories()

    def _personalization_failed(self, epoch):
        if not self._disposed and epoch == self._personal_epoch:
            self._personal_requested = False

    def _show_selected_home_chip(self):
        chip = self._selected_home_chip()
        if chip["kind"] == "all":
            if self._popular_cache:
                self._show_tiles(
                    self._popular_cache,
                    "Popular in Slovakia" if self._popular_source == "api"
                    else "Public YouTube selection (no API key)")
            elif self._popular_loading:
                if self._popular_source == "public":
                    self._fallback_home()
                else:
                    self._show_message("Loading popular videos for Slovakia…")
            elif self._popular_error:
                self._fallback_home()
            else:
                self._request_popular()
            return
        cache = self._personal_video_cache.get(chip["id"])
        if cache is not None:
            self._show_tiles(cache, chip["title"])
            return
        self._request_personal_videos(chip)

    def _request_personal_videos(self, chip):
        self._personal_video_epoch += 1
        epoch = self._personal_video_epoch
        selected = chip["id"]
        self._show_message("Loading subscribed channels…")
        self._render_categories()
        try:
            task = deferToThread(_load_personal_channel_videos, dict(chip))
            task.addCallbacks(
                lambda videos: self._personal_videos_ready(selected, videos, epoch),
                lambda err: self._personal_videos_failed(selected, epoch))
        except Exception:
            self._personal_videos_failed(selected, epoch)

    def _personal_videos_ready(self, chip_id, videos, epoch):
        if self._disposed or epoch != self._personal_video_epoch:
            return
        rows = dedupe_videos(videos if isinstance(videos, list) else [])
        self._personal_video_cache[chip_id] = rows
        if self.index == 0 and self._selected_home_chip()["id"] == chip_id:
            self._show_tiles(rows, self._selected_home_chip()["title"])
            self._render_categories()
            if self._selected_home_chip()["kind"] == "recent":
                self["status"].setText(_("Recent subscriptions: limited channel sample."))
            elif self._selected_home_chip()["kind"] == "topic":
                self["status"].setText(_("Topic: videos from matching subscribed channels."))

    def _personal_videos_failed(self, chip_id, epoch):
        if self._disposed or epoch != self._personal_video_epoch:
            return
        if self.index == 0 and self._selected_home_chip()["id"] == chip_id:
            self._show_message("YouTube subscriptions are temporarily unavailable.")
            self._render_categories()

    def _clear_preview(self):
        self.thumbs.show([])
        for i in range(VISIBLE_TILES):
            for prefix in ("preview_focus", "preview_panel", "preview_border", "preview_thumb",
                           "preview_title", "preview_channel", "detail"):
                self["%s%d" % (prefix, i)].hide()
        self["preview_message"].hide()
        self.video_items = []
        self.tile_index = 0
        self["page_info"].setText("")
        self.page_scroll.update(0, 1)

    def _show_message(self, message, details=None):
        self._clear_preview()
        self._section_items = []
        self.page_index = 0
        self["preview_message"].setText(_(message))
        self["preview_message"].show()
        if details:
            self["status"].setText(_(details))

    def _show_details(self, rows):
        self._clear_preview()
        self._section_items = []
        self.page_index = 0
        for i, text in enumerate(rows[:VISIBLE_TILES]):
            widget = self["detail%d" % i]
            widget.setText(_(text))
            widget.show()

    def _show_tiles(self, items, subtitle):
        all_videos = list(items)
        self._clear_preview()
        self._section_items = all_videos
        self._section_subtitle = subtitle
        pages = max(1, (len(all_videos) + VISIBLE_TILES - 1) // VISIBLE_TILES)
        if self.page_index >= pages:
            self.page_index = 0
        first = self.page_index * VISIBLE_TILES
        self.video_items = all_videos[first:first + VISIBLE_TILES]
        self["subtitle"].setText(_(subtitle))
        if (self.index == 0 and self._selected_home_chip()["kind"] == "all"
                and self._popular_source == "api"):
            reported = self._popular_total_results
            actual_pages = max(pages, (reported + VISIBLE_TILES - 1) // VISIBLE_TILES) if reported else (
                pages + (1 if self._popular_next_page_token else 0))
            shown_count = reported if reported else len(all_videos)
            # The displayed total is the YouTube chart count, never a claim
            # about all videos on the platform or a user's channel.
            self["page_info"].setText(
                "%d / %d  •  %d" % (self.page_index + 1, actual_pages, shown_count)
                if actual_pages > 1 else "")
        else:
            actual_pages = pages
            self["page_info"].setText(
                "%d / %d  •  %d" % (self.page_index + 1, pages, len(all_videos))
                if len(all_videos) > VISIBLE_TILES else "")
        self.page_scroll.update(self.page_index, actual_pages)
        if not self.video_items:
            self["preview_message"].setText(_("No saved videos in this section."))
            self["preview_message"].show()
            return
        for i, video in enumerate(self.video_items):
            self["preview_panel%d" % i].show()
            self["preview_border%d" % i].show()
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
            "Public YouTube videos are unavailable. "
            "Recently played and saved videos will appear here."
        )

    def _request_popular(self, refresh=False):
        if self._popular_requested or self._disposed:
            return
        key = get_api_key()
        category_id = "0"
        self._popular_source = "api" if key else "public"
        if not key and category_id != "0":
            self._popular_error = True
            self._show_message("Choose an API key to browse video categories.")
            self._render_categories()
            return
        self._popular_requested = True
        self._popular_loading = True
        self._popular_more_loading = False
        self._popular_request_epoch += 1
        request_epoch = self._popular_request_epoch
        if key and not refresh:
            self._show_message("Loading popular videos for Slovakia…")
            self._render_categories()
        elif refresh:
            self["status"].setText(_("Refreshing real YouTube videos…"))
        else:
            self._fallback_home()
            self["status"].setText(_("Loading public YouTube videos…"))
            self._render_categories()
        try:
            work = (deferToThread(popular_videos_page, key,
                                  category_id=category_id)
                    if key else deferToThread(public_home_videos))
            work.addCallbacks(
                lambda payload: self._popular_loaded(payload, request_epoch),
                lambda failure: self._popular_failed(failure, request_epoch))
        except Exception:
            self._popular_failed(None, request_epoch)

    def _popular_loaded(self, payload, request_epoch=None):
        if (self._disposed or (request_epoch is not None
                and request_epoch != self._popular_request_epoch)):
            return
        self._popular_loading = False
        if isinstance(payload, dict):
            videos = payload.get("items") or []
            token = payload.get("next_page_token") or ""
            total = payload.get("total_results")
        else:
            videos, token, total = payload, "", None
        self._popular_cache = videos[:24] if isinstance(videos, list) else []
        self._popular_next_page_token = token if isinstance(token, str) else ""
        self._popular_total_results = total if type(total) is int and total > 0 else None
        self._popular_fetched_at = monotonic()
        self._popular_error = False
        if self.index == 0 and self._selected_home_chip()["kind"] == "all":
            if self._popular_cache:
                self._show_tiles(
                    self._popular_cache,
                    "Popular in Slovakia" if self._popular_source == "api"
                    else "Public YouTube selection (no API key)")
            else:
                self._show_message("No videos in selected category.")
            self._render_categories()

    def _popular_failed(self, failure, request_epoch=None):
        if (self._disposed or (request_epoch is not None
                and request_epoch != self._popular_request_epoch)):
            return
        self._popular_loading = False
        self._popular_error = True
        self._popular_fetched_at = monotonic()
        if (self.index == 0 and self._selected_home_chip()["kind"] == "all"
                and self._popular_cache):
            self["status"].setText(_("Live YouTube refresh unavailable; previous data shown."))
            return
        if self.index == 0 and self._selected_home_chip()["kind"] == "all":
            self._fallback_home()
            self["status"].setText(
                _("Popular videos are temporarily unavailable.") if self._popular_source == "api"
                else _("Public YouTube list unavailable; showing local videos.")
            )
            self._render_categories()

    def _request_more_popular(self):
        if (self.index != 0 or self._disposed or self._popular_more_loading
                or self._selected_home_chip()["kind"] != "all"
                or not self._popular_next_page_token or not get_api_key()):
            return False
        token = self._popular_next_page_token
        category_id = "0"
        request_epoch = self._popular_request_epoch
        next_page = self.page_index + 1
        self._popular_more_loading = True
        self["status"].setText(_("Loading more videos…"))
        try:
            job = deferToThread(popular_videos_page, get_api_key(),
                                category_id=category_id, page_token=token)
            job.addCallbacks(
                lambda response: self._more_popular_ready(response, request_epoch, next_page),
                lambda failure: self._more_popular_failed(request_epoch))
        except Exception:
            self._more_popular_failed(request_epoch)
        return True

    def _more_popular_ready(self, response, request_epoch, next_page):
        if self._disposed or request_epoch != self._popular_request_epoch:
            return
        self._popular_more_loading = False
        if not isinstance(response, dict):
            self._more_popular_failed(request_epoch)
            return
        old_ids = {video.get("video_id") for video in self._popular_cache}
        new_items = [
            v for v in response.get("items", []) if isinstance(v, dict)
            and v.get("video_id") not in old_ids
        ]
        self._popular_cache.extend(new_items[:24])
        next_token = response.get("next_page_token") or ""
        # Avoid a server accidentally returning a token that loops forever.
        old_token = self._popular_next_page_token
        self._popular_next_page_token = (
            next_token if isinstance(next_token, str) and next_token != old_token
            else ""
        )
        new_total = response.get("total_results")
        if type(new_total) is int and new_total > 0:
            self._popular_total_results = new_total
        if (self.index == 0 and self._selected_home_chip()["kind"] == "all"
                and self._popular_cache):
            if next_page * VISIBLE_TILES < len(self._popular_cache):
                self.page_index = next_page
            self._show_tiles(self._popular_cache, "Popular in Slovakia")
            self._render_categories()
        self["status"].setText(_("More videos loaded.") if new_items
                              else _("No more videos in this category."))

    def _more_popular_failed(self, request_epoch):
        if self._disposed or request_epoch != self._popular_request_epoch:
            return
        self._popular_more_loading = False
        self["status"].setText(_("More videos could not be loaded. Try again."))

    def _update_preview(self):
        if self._disposed or not self._mounted:
            return
        self._hide_inline_keyboard()
        self._clear_preview()
        self["heading"].setText(self.sections[self.index][0])
        self["subtitle"].setText(self.sections[self.index][1])
        self["status"].setText("")
        if self.index == 0:
            self._show_selected_home_chip()
        elif self.index == 1:
            self._show_inline_keyboard()
        elif self.index == 2:
            self._show_message("Press OK to open YouTube subscriptions and TV account login.")
        elif self.index == 3:
            self._show_tiles(self._local_items("history"), "Recently played videos")
        elif self.index == 4:
            self._show_message("Playlists are not supported yet.")
        elif self.index == 5:
            self._show_tiles(self._local_items("favourites"), "Saved videos")
        elif self.index == 6:
            self._show_details([
                _("API key") + ": " + (_("Configured") if get_api_key() else _("Not configured")),
                _("Maximum video quality") + ": %sp" % get_quality(),
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
        self._render_categories()
        self._update_keys()

    def _hide_inline_keyboard(self):
        self.kb_shown = False
        for name in ("kb_system_input", "kb_system_list",
                     "kb_hint", "kb_feedback"):
            self[name].hide()

    def _show_inline_keyboard(self):
        """Show REAL system keyboard components in Home's right panel."""
        self.kb_shown = True
        self["kb_hint"].show()
        self["kb_feedback"].show()
        if self.inline_keyboard is None or not self.inline_keyboard.ready:
            self["kb_hint"].setText(
                _("The system keyboard cannot be embedded on this Enigma2 image.")
            )
            self["kb_feedback"].setText(self.kb_unavailable_reason)
            return
        self.inline_keyboard.show()
        self["kb_hint"].setText(
            _("Arrows: choose · OK: type · GREEN: search · YELLOW: delete character · BLUE: space · MENU: Shift")
        )
        self["kb_feedback"].setText("")

    def _enter_keyboard_focus(self):
        if (self.index != 1 or not self.kb_shown
                or self.inline_keyboard is None or not self.inline_keyboard.ready
                or self._disposed):
            return
        self.focus_area = "keyboard"
        self._update_nav()
        self._update_keys()

    def _leave_keyboard_focus(self):
        if self._disposed:
            return
        self.focus_area = "nav"
        self._update_nav()
        self._update_keys()

    def _keyboard_move(self, direction):
        if self.focus_area == "keyboard" and self.inline_keyboard is not None:
            self.inline_keyboard.navigate(direction)

    def _keyboard_append(self, character):
        if self.focus_area != "keyboard" or self.inline_keyboard is None:
            return
        if len(self.inline_keyboard.value()) >= 160:
            self["kb_feedback"].setText(_("Search phrase is too long."))
            return
        if character == " ":
            self.inline_keyboard.space()
        self["kb_feedback"].setText("")

    def _keyboard_press(self):
        if self.focus_area == "keyboard" and self.inline_keyboard is not None:
            if len(self.inline_keyboard.value()) < 160:
                # Firmware keymap handles letters, locale, SHIFT and special
                # Enter/Cancel keys; no Warder character table is involved.
                self.inline_keyboard.press()
            else:
                self["kb_feedback"].setText(_("Search phrase is too long."))

    def _keyboard_delete(self):
        if self.focus_area == "keyboard" and self.inline_keyboard is not None:
            self.inline_keyboard.delete()

    def _keyboard_case(self):
        if self.focus_area == "keyboard" and self.inline_keyboard is not None:
            self.inline_keyboard.shift()

    def _keyboard_native_submit(self, query):
        self._keyboard_submit(query)

    def _keyboard_submit(self, query=None):
        if self.focus_area != "keyboard" or self.inline_keyboard is None:
            return
        query = (self.inline_keyboard.value() if query is None else query).strip()
        if not query:
            self["kb_feedback"].setText(_("Enter your YouTube search"))
            return
        if len(query) > 160:
            self["kb_feedback"].setText(_("Search phrase is too long."))
            return
        # Dispatch from the current Home Screen while its two-pane keyboard
        # remains visible. Open Grid only when real results arrive; never
        # create the redundant Search Screen that visibly flashed before.
        if self._home_search_flow is None:
            from .home_search_flow import HomeSearchFlow
            self._home_search_flow = HomeSearchFlow(self)
        self._home_search_flow.start(query)

    def _update_keys(self):
        if self.focus_area == "categories":
            self["key_red"].setText(_("Back"))
            self["key_green"].setText(_("Choose category"))
            self["key_yellow"].setText(_("History"))
            self["key_blue"].setText(_("Search"))
            return
        if self.focus_area == "keyboard":
            self["key_red"].setText(_("Back"))
            self["key_green"].setText(_("Search"))
            self["key_yellow"].setText(_("Delete character"))
            self["key_blue"].setText(_("Space"))
            return
        self["key_red"].setText(_("Back") if self.focus_area == "tiles" else _("Close"))
        self["key_green"].setText(
            _("Play video") if self.focus_area == "tiles" and self.video_items
            else _("Search") if self.index == 1 else _("Open")
        )
        self["key_yellow"].setText(_("History"))
        self["key_blue"].setText(_("Search"))

    def _select_nav(self, index):
        if self._disposed or self._busy or self._playback_active or self._context_open:
            return
        # Circular main-menu navigation: Up from Home -> Updates,
        # Down from Updates -> Home. Only the left menu wraps; the
        # right-hand video grid keeps its existing navigation semantics.
        index = index % len(self.sections)
        if (self.index == 1 and index != 1
                and self._home_search_flow is not None):
            # Discard late worker results when navigating away from Search.
            self._home_search_flow.cancel_pending()
        if self.index == index and self.focus_area == "nav":
            return
        self.index = index
        self.page_index = 0
        self.focus_area = "nav"
        self._update_preview()

    def up(self):
        if self.focus_area == "categories":
            return
        if self.focus_area == "keyboard":
            self._keyboard_move("up")
        elif self.focus_area == "nav":
            self._select_nav(self.index - 1)
        elif (self.focus_area == "tiles" and self.index == 0
                and self.page_index == 0 and self.tile_index < 3):
            self._enter_categories()
        else:
            self._move_tile("up")

    def down(self):
        if self.focus_area == "categories":
            if self.video_items:
                self.focus_area = "tiles"
                self.tile_index = 0
                self._update_tile_focus()
                self._render_categories()
                self._update_keys()
            return
        if self.focus_area == "keyboard":
            self._keyboard_move("down")
        elif self.focus_area == "nav":
            self._select_nav(self.index + 1)
        else:
            self._move_tile("down")

    def left(self):
        if self.focus_area == "categories":
            self._category_cursor = (self._category_cursor - 1) % len(self._home_chips)
            self._render_categories()
            return
        if self.focus_area == "keyboard":
            if self.inline_keyboard is not None and self.inline_keyboard.is_left_edge():
                self._leave_keyboard_focus()
            else:
                self._keyboard_move("left")
            return
        if self.focus_area == "tiles":
            if self.tile_index % 3 == 0:
                self.focus_area = "nav"
                # Do not leave the old video title under the menu when
                # keyboard focus returns from the right-hand preview.
                self["status"].setText("")
                self._update_nav()
                self._update_tile_focus()
                self._update_keys()
            else:
                self._move_tile("left")

    def right(self):
        if self.focus_area == "categories":
            self._category_cursor = (self._category_cursor + 1) % len(self._home_chips)
            self._render_categories()
            return
        if self.focus_area == "keyboard":
            self._keyboard_move("right")
            return
        if self.focus_area == "nav" and self.index == 1:
            self._enter_keyboard_focus()
        elif self.focus_area == "nav":
            self._enter_tiles()
        else:
            self._move_tile("right")

    def _move_tile(self, direction):
        if not self.video_items or self._busy or self._playback_active or self._context_open:
            return
        # Six visible native tiles are a PAGE, not a fixed list of videos.
        # Navigate through all actual items returned by YouTube/local library.
        if ((direction == "down" and self.tile_index + 3 >= len(self.video_items))
                or (direction == "right" and self.tile_index == len(self.video_items) - 1)):
            if self._switch_page(1):
                return
        if direction == "up" and self.tile_index < 3:
            if self._switch_page(-1):
                return
        next_index = move_index(self.tile_index, direction, len(self.video_items))
        if next_index != self.tile_index:
            self.tile_index = next_index
            self._update_tile_focus()

    def _switch_page(self, delta):
        max_page = (len(self._section_items) - 1) // VISIBLE_TILES
        new_page = self.page_index + delta
        if new_page < 0 or new_page > max_page:
            if delta > 0 and self._request_more_popular():
                return True
            return False
        self.page_index = new_page
        self._show_tiles(self._section_items, self._section_subtitle)
        self._update_tile_focus()
        return True

    def _enter_tiles(self):
        if (self.index == 0 and not self.video_items
                and self.focus_area == "nav"):
            self._enter_categories()
            return
        if self.video_items and self.focus_area == "nav":
            self.focus_area = "tiles"
            self.tile_index = 0
            self._update_nav()
            self._update_tile_focus()
            self._update_keys()

    def back(self):
        if self.focus_area == "categories":
            self.focus_area = "nav"
            self["status"].setText("")
            self._update_nav()
            self._render_categories()
            self._update_tile_focus()
            self._update_keys()
            return
        if self.focus_area == "keyboard":
            self._leave_keyboard_focus()
            return
        if self.focus_area == "tiles":
            self.focus_area = "nav"
            self["status"].setText("")
            self._update_nav()
            self._update_tile_focus()
            self._update_keys()
        else:
            self.close()

    def green(self):
        if self.focus_area == "keyboard":
            self._keyboard_submit()
        else:
            self.activate()

    def yellow(self):
        if self.focus_area == "keyboard":
            self._keyboard_delete()
            return
        if self.focus_area == "tiles":
            self.context()
        else:
            self._select_nav(3)

    def blue(self):
        if self.focus_area == "keyboard":
            self._keyboard_append(" ")
            return
        self._select_nav(1)
        self._enter_keyboard_focus()

    def menu(self):
        if self.focus_area == "keyboard":
            self._keyboard_case()
        else:
            self.context()

    def activate(self):
        if self._disposed or self._busy or self._playback_active or self._context_open:
            return
        if self.focus_area == "keyboard":
            self._keyboard_press()
        elif self.focus_area == "tiles":
            self._play_selected()
        elif self.focus_area == "categories":
            self._choose_category()
        elif self.index == 1:
            self._enter_keyboard_focus()
        elif self.index in (0, 3, 5) and self.video_items:
            self._enter_tiles()
        else:
            self._open_index(self.index)

    def _open_index(self, index):
        if self._disposed or self._busy or self._context_open or self._playback_active:
            return
        if index == 1:
            self._select_nav(1)
            self._enter_keyboard_focus()
        elif index == 2:
            self._auth_maybe_changed = True
            from .subscriptions_ui import WarderYouTubeSubscriptions
            self.session.open(WarderYouTubeSubscriptions)
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

    def _info_cached_thumbnail(self, item):
        """Reuse the Home tile's exact already-decoded image when available."""
        if isinstance(item, dict):
            url = item.get("thumbnail_url")
            cache = getattr(self.thumbs, "image_cache", None)
            if isinstance(url, str) and isinstance(cache, dict):
                return cache.get(url)
        return None

    def info(self):
        item = self.selected_video()
        if (item is None or self._busy or self._playback_active or
                self._disposed or self._context_open or self._confirm_open):
            return
        from .info_ui import WarderYouTubeInfo
        key = get_api_key()
        if not key:
            self.session.open(
                WarderYouTubeInfo,
                format_video_info(
                    item, translate=_,
                    note="Detailed information requires a YouTube API key."
                ), video=item, thumbnail_pixmap=self._info_cached_thumbnail(item)
            )
            return
        self._busy = True
        self._play_request += 1
        token = self._play_request
        self["status"].setText(_("Loading video details…"))
        try:
            worker = deferToThread(fetch_video_info, item["video_id"], key)
            worker.addCallbacks(
                lambda details: self._info_ready(token, item, details),
                lambda failure: self._info_failed(token, item, failure)
            )
        except Exception:
            self._info_failed(token, item, None)

    def _info_ready(self, token, item, details):
        if self._disposed or token != self._play_request:
            return
        from .info_ui import WarderYouTubeInfo
        self._busy = False
        self["status"].setText(_("Video details loaded."))
        self.session.open(
            WarderYouTubeInfo,
            format_video_info(item, details, translate=_),
            video=item, thumbnail_pixmap=self._info_cached_thumbnail(item)
        )

    def _info_failed(self, token, item, failure):
        if self._disposed or token != self._play_request:
            return
        from .info_ui import WarderYouTubeInfo
        self._busy = False
        self["status"].setText(_("Details unavailable; showing saved video information."))
        self.session.open(
            WarderYouTubeInfo,
            format_video_info(
                item, translate=_,
                note="Details unavailable; showing saved video information."
            ), video=item, thumbnail_pixmap=self._info_cached_thumbnail(item)
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
                (_("Clear all favourite videos") if self.index == 5
                 else _("Clear entire history")) + "?"
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

    def _play_selected(self, video=None):
        # Video Grid invokes this with the actual selected video, while Home
        # tiles continue to call it without an argument.
        if video is None:
            video = self.selected_video()
        if (video is None or self._disposed or self._busy or
                self._playback_active or self._context_open):
            return
        self._busy = True
        self._play_request += 1
        token = self._play_request
        self["status"].setText(_("Looking for a compatible video stream…"))
        if (self._home_search_flow is not None
                and self._home_search_flow.grid_open):
            self._home_search_flow._status(
                _("Looking for a compatible video stream…"), override=True
            )
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
            if (self._home_search_flow is not None
                    and self._home_search_flow.grid_open):
                self._home_search_flow._status(
                    _("Unable to open Enigma2 player."), override=True
                )
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
        message = (str(error) if isinstance(error, ResolverError)
                   else _("Unable to obtain a video stream."))
        self["status"].setText(message)
        if (self._home_search_flow is not None
                and self._home_search_flow.grid_open):
            self._home_search_flow._status(message, override=True)

    def _player_closed(self, failed=False, *args):
        self._playback_active = False
        if self._disposed:
            return
        if (self._home_search_flow is not None
                and self._home_search_flow.grid_open):
            self._home_search_flow._status(
                _("Playback failed.") if failed else
                _("Playback ended. OK: play another video."), override=True
            )
        else:
            self._update_preview()
