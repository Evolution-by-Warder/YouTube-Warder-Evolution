# -*- coding: utf-8 -*-
"""Native Warder Odbery: Google TV login, newest uploads, all followed channels.

A read-only account connection is optional and explicit. No Google password,
third-party OAuth credentials or access tokens are displayed. All disk/network
operations run in workers; remote actions do not block the Enigma2 GUI.
"""
import time

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.MenuList import MenuList
from Screens.Screen import Screen
from twisted.internet.threads import deferToThread

from .header_ui import add_header
from .i18n import tr as _
from .skin import LIBRARY_SKIN
from .home_thumbs import HomeThumbs


VISIBLE_TILES = 6


def _short_title(value, limit=48):
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def _subscriptions_skin():
    """Reuse the already-approved blue container and native Home focus art.

    The base native list is still used for channel names and TV login.
    Six video cards are displayed only for latest/channel-upload pages.
    These are plain Enigma2 Label/Pixmap widgets; no extra renderer.
    """
    skin = LIBRARY_SKIN.replace(
        'name="WarderYouTubeLibrary"', 'name="WarderYouTubeSubscriptions"', 1
    )
    widgets = [
        '<widget name="page_info" position="1540,175" size="290,38" '
        'font="Regular;24" foregroundColor="#63D9FA" transparent="1" '
        'halign="right" zPosition="6"/>',
    ]
    for slot in range(VISIBLE_TILES):
        col, row = slot % 3, slot // 3
        x = 62 + 589 * col
        y = 239 + 321 * row
        thumb_x, thumb_y = x + 13, y + 12
        widgets.extend([
            '<widget name="tile_panel%d" position="%d,%d" size="568,310" '
            'font="Regular;1" backgroundColor="#142C47" '
            'foregroundColor="#142C47" transparent="0" zPosition="3"/>' % (slot, x, y),
            '<widget name="tile_focus%d" position="%d,%d" size="568,310" '
            'pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" '
            'alphatest="on" zPosition="8"/>' % (slot, x, y),
            '<widget name="preview_thumb%d" position="%d,%d" size="540,196" '
            'zPosition="4"/>' % (slot, thumb_x, thumb_y),
            '<widget name="tile_title%d" position="%d,%d" size="540,62" '
            'font="Regular;25" foregroundColor="#FFFFFF" transparent="1" '
            'zPosition="5"/>' % (slot, thumb_x, y + 208),
            '<widget name="tile_channel%d" position="%d,%d" size="540,29" '
            'font="Regular;21" foregroundColor="#B9D9F5" transparent="1" '
            'zPosition="5"/>' % (slot, thumb_x, y + 272),
        ])
    return skin.replace("</screen>", "\n  ".join(widgets) + "\n</screen>", 1)


from .subscriptions_auth import (
    SubscriptionsAuthError, account_connected, read_client,
    request_device_code, poll_device_code, save_tokens, clear_tokens, access_token,
)
from .subscriptions_api import (
    SubscriptionsApiError, subscriptions_list, recent_subscription_videos,
    uploads_playlists, playlist_videos,
)
from .local_library import record_opened, LibraryError
from .settings import get_quality
from .resolver import resolve_video_streams, ResolverError


def _device_start():
    client = read_client()
    return client, request_device_code(client)


def _fetch_recent():
    return recent_subscription_videos(access_token())


def _fetch_channels():
    return subscriptions_list(access_token())


def _fetch_channel(channel_id):
    token = access_token()
    playlist = uploads_playlists([channel_id], token).get(channel_id)
    return playlist_videos(playlist, token, limit=30) if playlist else []


class WarderYouTubeSubscriptions(Screen):
    # Native screen with the owner's approved colors, header and key bar.
    skin = _subscriptions_skin()

    def __init__(self, session):
        Screen.__init__(self, session)
        add_header(self)
        self.mode = "recent"
        # Do not shadow Screen.items(): Enigma2 calls it on window teardown.
        self.mode_items = []
        self.page_index = 0
        self.tile_index = 0
        self.channels = []
        self.busy = False
        self.disposed = False
        self.connected = False
        self.playing = False
        self.login = None
        self.client = None
        self.deadline = 0
        self.poll_interval = 5
        self.polling_timer = None
        self.poll_signal = None
        self.poll_connection = None
        self.request_id = 0
        self.disconnect_prompt_open = False
        self["title"] = Label("")
        self["subtitle"] = Label(_("Subscriptions"))
        self["results"] = MenuList([])
        self["page_info"] = Label("")
        for i in range(VISIBLE_TILES):
            self["tile_panel%d" % i] = Label(" ")
            self["tile_focus%d" % i] = Pixmap()
            self["preview_thumb%d" % i] = Pixmap()
            self["tile_title%d" % i] = Label("")
            self["tile_channel%d" % i] = Label("")
        self.thumbs = HomeThumbs(self)
        self["status"] = Label("")
        self["footer"] = Label(_("OK: open video or channel · MENU: disconnect account"))
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Open"))
        self["key_yellow"] = Label(_("Latest videos"))
        self["key_blue"] = Label(_("All subscriptions"))
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "MenuActions", "InfoActions",
             "DirectionActions", "NavigationActions"],
            {"ok": self.choose, "green": self.choose,
             "red": self.close, "cancel": self.close,
             "yellow": self.latest, "blue": self.all_channels,
             "menu": self.disconnect_confirm, "info": self.show_info,
             "up": lambda: self.navigate("up"),
             "down": lambda: self.navigate("down"),
             "left": lambda: self.navigate("left"),
             "right": lambda: self.navigate("right")},
            -1
        )
        self.onLayoutFinish.append(self._start_thumbs)
        self.onLayoutFinish.append(self._start_timer)
        self.onShown.append(self.on_show)
        self.onClose.append(self.dispose)

    def _start_thumbs(self):
        if not self.disposed:
            self.thumbs.start()
            self._render_items()

    def _video_mode(self):
        return self.mode in ("recent", "channel_videos")

    def _hide_tiles(self):
        self.thumbs.show([])
        for i in range(VISIBLE_TILES):
            for prefix in ("tile_panel", "tile_focus", "preview_thumb",
                           "tile_title", "tile_channel"):
                self["%s%d" % (prefix, i)].hide()
        self["page_info"].setText("")

    def _render_items(self):
        self._hide_tiles()
        if not self._video_mode():
            self["results"].setList([
                (item.get("title") or _("Untitled"))[:115]
                for item in self.mode_items
            ])
            self["results"].show()
            return
        self["results"].hide()
        total = len(self.mode_items)
        pages = max(1, (total + VISIBLE_TILES - 1) // VISIBLE_TILES)
        self.page_index = min(max(self.page_index, 0), pages - 1)
        current = self.mode_items[self.page_index * VISIBLE_TILES:
                                  (self.page_index + 1) * VISIBLE_TILES]
        self.tile_index = min(max(self.tile_index, 0), max(0, len(current) - 1))
        self["page_info"].setText("%d / %d  •  %d" % (self.page_index + 1, pages, total)
                                   if total else "")
        for i, video in enumerate(current):
            self["tile_panel%d" % i].show()
            self["tile_title%d" % i].setText(_short_title(video.get("title")))
            self["tile_title%d" % i].show()
            self["tile_channel%d" % i].setText(
                _short_title(video.get("channel"), 41))
            self["tile_channel%d" % i].show()
        self._update_focus()
        self.thumbs.show(current)

    def _update_focus(self):
        count = min(VISIBLE_TILES, max(0, len(self.mode_items) -
                         self.page_index * VISIBLE_TILES))
        for i in range(VISIBLE_TILES):
            widget = self["tile_focus%d" % i]
            if self._video_mode() and i == self.tile_index and i < count:
                widget.show()
            else:
                widget.hide()

    def navigate(self, direction):
        if self.disposed or self.busy or self.playing or not self.mode_items:
            return
        if self._video_mode():
            old = self.page_index * VISIBLE_TILES + self.tile_index
            delta = {"up": -3, "down": 3, "left": -1, "right": 1}.get(direction, 0)
            updated = max(0, min(len(self.mode_items) - 1, old + delta))
            next_page = updated // VISIBLE_TILES
            self.tile_index = updated % VISIBLE_TILES
            if next_page != self.page_index:
                self.page_index = next_page
                self._render_items()
            else:
                self._update_focus()
            return
        # Real Enigma2 MenuList owns the selection in channel/login mode.
        widget = self["results"]
        instance = getattr(widget, "instance", None)
        if instance is not None:
            move = {"up": "moveUp", "down": "moveDown",
                    "left": "pageUp", "right": "pageDown"}.get(direction)
            if move and hasattr(instance, move):
                instance.moveSelection(getattr(instance, move))
        else:
            method = getattr(widget, direction, None)
            if callable(method):
                method()

    def _start_timer(self):
        try:
            from enigma import eTimer
            self.polling_timer = eTimer()
            signal = self.polling_timer.timeout
            if hasattr(signal, "get"):
                self.poll_signal = signal.get()
                self.poll_signal.append(self._poll)
            else:
                self.poll_connection = signal.connect(self._poll)
        except (ImportError, AttributeError, RuntimeError, TypeError):
            self.polling_timer = None

    def _schedule(self):
        if self.disposed or self.polling_timer is None or not self.login:
            return
        if time.time() >= self.deadline:
            self.login = None
            self["status"].setText(_("YouTube login code expired. Try connecting again."))
            self["key_green"].setText(_("Connect YouTube account"))
            return
        try:
            self.polling_timer.start(int(self.poll_interval) * 1000, True)
        except (RuntimeError, AttributeError, TypeError):
            self["status"].setText(_("This receiver cannot run YouTube TV login polling."))

    def _working(self, worker, success, failure=None):
        if self.disposed or self.busy:
            return False
        self.busy = True
        self.request_id += 1
        ident = self.request_id
        try:
            task = deferToThread(worker)
            task.addCallbacks(
                lambda result: self._finish(ident, success, result),
                lambda error: self._error(ident, failure)
            )
            return True
        except Exception:
            self._error(ident, failure)
            return False

    def _finish(self, ident, handler, value):
        if self.disposed or ident != self.request_id:
            return
        self.busy = False
        handler(value)

    def _error(self, ident, handler=None):
        if self.disposed or ident != self.request_id:
            return
        self.busy = False
        if handler is not None:
            handler()
        else:
            self["status"].setText(_("YouTube subscriptions are unavailable."))

    def _rows(self, rows):
        self.mode_items = list(rows)
        self.page_index = 0
        self.tile_index = 0
        self._render_items()

    def _selected(self):
        index = (self.page_index * VISIBLE_TILES + self.tile_index
                 if self._video_mode() else self["results"].getCurrentIndex())
        return (self.mode_items[index]
                if 0 <= index < len(self.mode_items) else None)

    def on_show(self):
        if self.disposed or self.busy or self.connected or self.login is not None:
            return
        self["status"].setText(_("Checking YouTube account connection…"))
        self._working(account_connected, self._account_ready)

    def _account_ready(self, connected):
        self.connected = bool(connected)
        if connected:
            self.latest()
        else:
            self["subtitle"].setText(_("Subscriptions · YouTube account"))
            self["status"].setText(_("Press GREEN to connect your YouTube account using a TV code."))
            self["key_green"].setText(_("Connect YouTube account"))
            self._rows([])

    def start_login(self):
        if self.disposed or self.login or self.connected:
            return
        self["status"].setText(_("Requesting a secure Google TV login code…"))
        self._working(_device_start, self._code_ready, self._login_failed)

    def _login_failed(self):
        self["status"].setText(_(
            "Google TV OAuth client not configured or login unavailable. "
            "Configure /etc/enigma2/warderyoutube-oauth-client.json (mode 0600)."
        ))

    def _code_ready(self, result):
        if self.disposed:
            return
        self.client, self.login = result
        self.deadline = time.time() + self.login["expires_in"]
        self.poll_interval = self.login["interval"]
        self.mode = "login"
        self["subtitle"].setText(_("Connect YouTube account"))
        self._rows([
            {"title": _("Open on your phone or PC:") + "  " + self.login["verification_url"]},
            {"title": _("Enter this code exactly:") + "  " + self.login["user_code"]},
            {"title": _("Then confirm read-only YouTube access in Google.")},
        ])
        self["status"].setText(_("Waiting for Google account authorization…"))
        self["key_green"].setText(_("Waiting for login"))
        self._schedule()

    def _poll(self):
        if self.busy or self.disposed or not self.login:
            return
        if time.time() >= self.deadline:
            self.login = None
            self["status"].setText(_("YouTube login code expired. Try connecting again."))
            self["key_green"].setText(_("Connect YouTube account"))
            return
        client = dict(self.client)
        code = self.login["device_code"]
        self._working(lambda: poll_device_code(client, code), self._poll_result,
                      self._poll_failed)

    def _poll_failed(self):
        self.login = None
        self["status"].setText(_("YouTube login failed or access was denied."))

    def _poll_result(self, response):
        state, token = response
        if state == "slow_down":
            self.poll_interval = min(self.poll_interval + 5, 60)
            self._schedule()
        elif state == "authorization_pending":
            self._schedule()
        elif state == "connected":
            self._working(lambda: save_tokens(token), self._login_saved,
                          self._poll_failed)
        else:
            self._poll_failed()

    def _login_saved(self, result):
        self.login = None
        self.client = None
        self.connected = True
        self["key_green"].setText(_("Open"))
        self["status"].setText(_("YouTube account connected."))
        self.latest()

    def latest(self):
        if not self.connected or self.disposed or self.busy:
            return
        self.mode = "recent"
        self["subtitle"].setText(_("Latest videos from subscriptions (limited sample)"))
        self["status"].setText(_("Loading recent videos from followed channels…"))
        self._working(_fetch_recent, self._recent_ready)

    def _recent_ready(self, result):
        videos, channels = result
        self.channels = channels
        self._rows(videos)
        self["status"].setText(
            _("Showing a limited sample of recent uploads. BLUE: all channels.")
            if videos else _("No recent videos found in the sampled subscriptions.")
        )

    def all_channels(self):
        if not self.connected or self.disposed or self.busy:
            return
        self.mode = "channels"
        self["subtitle"].setText(_("All subscriptions"))
        self["status"].setText(_("Loading your subscribed channels…"))
        self._working(_fetch_channels, self._channels_ready)

    def _channels_ready(self, channels):
        self.channels = channels
        self._rows(channels)
        self["status"].setText(
            _("%d subscribed channels shown. OK: channel videos.") % len(channels)
            if channels else _("No subscribed channels found.")
        )

    def _channel_ready(self, videos):
        self.mode = "channel_videos"
        self._rows(videos)
        self["status"].setText(_("OK: play video · YELLOW: latest · BLUE: all channels")
                               if videos else _("No public videos in this channel."))

    def choose(self):
        if self.disposed or self.busy or self.playing:
            return
        if not self.connected:
            self.start_login()
            return
        item = self._selected()
        if item is None:
            return
        if self.mode == "channels":
            channel_id = item["channel_id"]
            self["subtitle"].setText(item["title"][:90])
            self["status"].setText(_("Loading videos from channel…"))
            self._working(lambda: _fetch_channel(channel_id), self._channel_ready)
        elif self.mode in ("recent", "channel_videos"):
            self._play_video(item)

    def _play_video(self, item):
        self["status"].setText(_("Looking for a compatible video stream…"))
        try:
            from .player import dash_available
            self._working(lambda: resolve_video_streams(
                item["video_id"], quality=get_quality(), dash=dash_available()),
                lambda streams: self._play_ready(item, streams))
        except Exception:
            self["status"].setText(_("Could not open the video player."))

    def _play_ready(self, item, streams):
        try:
            from .player import open_player
            self.playing = True
            open_player(self.session, streams, item["title"], on_close=self._player_closed)
            try:
                record_opened(item)
            except LibraryError:
                pass
        except Exception:
            self.playing = False
            self["status"].setText(_("Could not open the video player."))

    def _player_closed(self, *args):
        self.playing = False

    def show_info(self):
        item = self._selected()
        if self.disposed or self.busy or item is None or "video_id" not in item:
            return
        from .info_ui import WarderYouTubeInfo
        from .video_info_display import format_video_info
        self.session.open(WarderYouTubeInfo, format_video_info(item, translate=_),
                          video=item,
                          thumbnail_pixmap=self.thumbs.image_cache.get(item.get("thumbnail_url")))

    def disconnect_confirm(self):
        if not self.connected or self.disposed or self.busy or self.disconnect_prompt_open:
            return
        from .confirm_ui import WarderYouTubeConfirm
        self.disconnect_prompt_open = True
        self.session.openWithCallback(self._disconnect_answer,
            WarderYouTubeConfirm, _("Disconnect the YouTube account from this receiver?"))

    def _disconnect_answer(self, approved):
        self.disconnect_prompt_open = False
        if not approved or self.disposed or self.busy:
            return
        self._working(clear_tokens, self._disconnected)

    def _disconnected(self, unused):
        self.connected = False
        self.channels = []
        self.login = None
        self.mode = "recent"
        self._account_ready(False)

    def dispose(self):
        self.disposed = True
        self.thumbs.close()
        self.request_id += 1
        self.login = None
        if self.polling_timer is not None:
            try:
                self.polling_timer.stop()
            except (AttributeError, RuntimeError):
                pass
        if self.poll_connection is not None:
            try:
                self.poll_connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
        if self.poll_signal is not None:
            try:
                self.poll_signal.remove(self._poll)
            except (ValueError, AttributeError, RuntimeError):
                pass
