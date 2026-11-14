# -*- coding: utf-8 -*-
"""Native Warder information dialog with reliable manual text navigation.

Uses the original working Enigma2 Label, not the ScrollLabel widget which
rendered a blank body on the GigaBlue/OpenATV receiver. All content is retained
in memory and exposed line-by-line; no timers, custom renderer or animation.
"""
import textwrap
from .header_ui import add_header
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from .i18n import tr as _
from .skin import INFO_SKIN


# Match the enlarged INFO text area (1660 x 580, Regular 30).
# Display two more lines without crossing the existing blue frame.
LINE_WIDTH = 65
VISIBLE_LINES = 14

# Track and thumb stay entirely inside the existing INFO frame.
SCROLL_X = 1798
SCROLL_Y = 313
SCROLL_HEIGHT = 580
SCROLL_WIDTH = 8
MIN_THUMB_HEIGHT = 38

# Use exactly the same 410x230 picture dimensions as the Home video tiles.
VIDEO_THUMB_WIDTH = 410
VIDEO_THUMB_HEIGHT = 230


def wrap_info_lines(message, width=LINE_WIDTH):
    lines = []
    for paragraph in str(message or "").replace("\r", "").split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(
            paragraph, width=width, expand_tabs=True,
            replace_whitespace=True, drop_whitespace=True,
            break_long_words=True, break_on_hyphens=False,
        ) or [""])
    return lines or [""]


class WarderYouTubeInfo(Screen):
    skin = INFO_SKIN

    def __init__(self, session, message, title=None, video=None, thumbnail_pixmap=None):
        Screen.__init__(self, session)
        add_header(self)
        self._info_lines = wrap_info_lines(str(message)[:2500])
        self._top_line = 0
        # Selected item's image is optional; keep INFO readable without a thumbnail.
        self._video = video if isinstance(video, dict) else None
        self._cached_thumbnail = thumbnail_pixmap
        self._thumbnail_decoder = None
        self._thumbnail_signal = None
        self._thumbnail_connection = None
        self._thumbnail_disposed = False
        self["brand"] = Label("YouTube Warder Evolution")
        self["title"] = Label(title or _("Video details"))
        self["body"] = Label(self._visible_text())
        self["video_thumbnail"] = Pixmap()
        self["video_thumbnail"].hide()
        self.onLayoutFinish.append(self._show_video_thumbnail)
        self.onClose.append(self._close_video_thumbnail)
        # Keep the proven plain Label text: the firmware ScrollLabel was blank.
        self["scroll_track"] = Label(" ")
        self["scroll_thumb"] = Label(" ")
        self.onLayoutFinish.append(self._refresh_scrollbar)
        self["key_red"] = Label(_("Back"))
        self["key_green"] = Label(_("Close"))
        self["key_yellow"] = Label(_("Scroll up"))
        self["key_blue"] = Label(_("Scroll down"))
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions", "DirectionActions", "NavigationActions"],
            {
                "ok": self.close, "cancel": self.close,
                "red": self.close, "green": self.close,
                "up": self.scroll_up, "down": self.scroll_down,
                "pageUp": self.page_up, "pageDown": self.page_down,
                "yellow": self.page_up, "blue": self.page_down,
            }, -1)

    def _max_top_line(self):
        return max(0, len(self._info_lines) - VISIBLE_LINES)

    def _visible_text(self):
        return "\n".join(self._info_lines[
            self._top_line:self._top_line + VISIBLE_LINES
        ])

    def _refresh_scrollbar(self):
        """Display a proportional vertical thumb for the current text position.

        Only native eLabel widgets are used. Position and size are updated
        after screen layout and on remote-key navigation. Short texts do not
        show a misleading scrollbar.
        """
        maximum = self._max_top_line()
        if maximum <= 0:
            self["scroll_track"].hide()
            self["scroll_thumb"].hide()
            return

        self["scroll_track"].show()
        self["scroll_thumb"].show()
        visible = min(VISIBLE_LINES, len(self._info_lines))
        height = max(MIN_THUMB_HEIGHT, int(
            SCROLL_HEIGHT * float(visible) / len(self._info_lines)
        ))
        height = min(SCROLL_HEIGHT, height)
        travel = SCROLL_HEIGHT - height
        top = SCROLL_Y + (travel * self._top_line // maximum)
        self._scroll_thumb_top = top
        self._scroll_thumb_height = height
        instance = getattr(self["scroll_thumb"], "instance", None)
        if instance is not None:
            try:
                from enigma import ePoint, eSize
                instance.resize(eSize(SCROLL_WIDTH, height))
                instance.move(ePoint(SCROLL_X, top))
            except (ImportError, RuntimeError, TypeError, AttributeError):
                # Native static skin position remains as a safe fallback.
                pass

    def _move(self, amount):
        new_top = max(0, min(self._max_top_line(), self._top_line + amount))
        if new_top != self._top_line:
            self._top_line = new_top
            self["body"].setText(self._visible_text())
            self._refresh_scrollbar()

    def scroll_up(self):
        self._move(-1)

    def scroll_down(self):
        self._move(1)

    def page_up(self):
        self._move(-VISIBLE_LINES)

    def page_down(self):
        self._move(VISIBLE_LINES)

    def _show_video_thumbnail(self):
        """Reuse the precise Home tile picture or decode its temporary JPEG.

        No new requests are made while browsing or scrolling, only when INFO
        is opened. Network I/O runs outside the GUI thread.
        """
        if self._thumbnail_disposed or self._video is None:
            return
        if self._cached_thumbnail is not None:
            try:
                self["video_thumbnail"].setPixmap(self._cached_thumbnail)
                self["video_thumbnail"].show()
                return
            except (AttributeError, TypeError, ValueError, RuntimeError):
                self._cached_thumbnail = None
        video_id = self._video.get("video_id")
        if not isinstance(video_id, str):
            return
        import re
        if re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id) is None:
            return
        url = self._video.get("thumbnail_url")
        # The saved ID is trustworthy only after strict YouTube ID validation.
        if not isinstance(url, str) or not url:
            url = "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id
        try:
            from .thumbnails import validate_thumbnail_url, fetch_thumbnail
            from twisted.internet.threads import deferToThread
            from enigma import ePicLoad
            validate_thumbnail_url(url)
            decoder = ePicLoad()
            signal = decoder.PictureData
            if hasattr(signal, "get"):
                self._thumbnail_signal = signal.get()
                self._thumbnail_signal.append(self._thumbnail_decoded)
            else:
                self._thumbnail_connection = signal.connect(self._thumbnail_decoded)
            self._thumbnail_decoder = decoder
            decoder.setPara(self._thumbnail_decode_settings())
            worker = deferToThread(fetch_thumbnail, url)
            worker.addCallbacks(self._thumbnail_downloaded,
                                lambda failure: None)
        except Exception:
            # If the image decoder or network is unavailable, text and
            # scrolling are unaffected (no placeholder covering the text).
            self._release_thumbnail_decoder()

    def _thumbnail_decode_settings(self):
        scale_x, scale_y = 1, 1
        try:
            from Components.AVSwitch import AVSwitch
            scale = AVSwitch().getFramebufferScale()
            if (isinstance(scale, (list, tuple)) and len(scale) == 2 and
                    all(type(n) is int and 0 < n <= 16 for n in scale)):
                scale_x, scale_y = scale
        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError):
            pass
        return (VIDEO_THUMB_WIDTH, VIDEO_THUMB_HEIGHT,
                scale_x, scale_y, False, 1, "#00000000")

    def _thumbnail_downloaded(self, path):
        if (self._thumbnail_disposed or not path or
                self._thumbnail_decoder is None):
            return
        try:
            if self._thumbnail_decoder.startDecode(path) != 0:
                return
        except Exception:
            pass

    def _thumbnail_decoded(self, *args):
        if self._thumbnail_disposed or self._thumbnail_decoder is None:
            return
        try:
            pixmap = self._thumbnail_decoder.getData()
            if pixmap is not None:
                self._cached_thumbnail = pixmap
                self["video_thumbnail"].setPixmap(pixmap)
                self["video_thumbnail"].show()
        except (AttributeError, TypeError, ValueError, RuntimeError):
            pass

    def _release_thumbnail_decoder(self):
        if self._thumbnail_connection is not None:
            try:
                self._thumbnail_connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
            self._thumbnail_connection = None
        if self._thumbnail_signal is not None:
            try:
                self._thumbnail_signal.remove(self._thumbnail_decoded)
            except (AttributeError, ValueError, RuntimeError):
                pass
            self._thumbnail_signal = None
        self._thumbnail_decoder = None

    def _close_video_thumbnail(self):
        self._thumbnail_disposed = True
        self._release_thumbnail_decoder()
        self._cached_thumbnail = None
