# -*- coding: utf-8 -*-
"""Tiny native page indicator shared by Home, Odbery and Search galleries.

The tested INFO scrollbar already uses plain opaque Enigma2 Labels. Use the
same mechanism here: no custom renderer, timer, animations or overlays.
"""


class TilePageScrollbar:
    def __init__(self, track, thumb, x, y, width, height):
        self.track = track
        self.thumb = thumb
        self.x, self.y = int(x), int(y)
        self.width, self.height = int(width), int(height)
        self.page = 0
        self.pages = 1
        self.thumb_top = self.y
        self.thumb_height = self.height
        self.update(0, 1)

    def update(self, page, pages):
        self.pages = max(1, int(pages))
        self.page = max(0, min(int(page), self.pages - 1))
        if self.pages <= 1:
            self.track.hide()
            self.thumb.hide()
            return
        self.track.show()
        self.thumb.show()
        self.thumb_height = min(
            self.height, max(38, self.height // self.pages)
        )
        travel = self.height - self.thumb_height
        self.thumb_top = self.y + (
            travel * self.page // (self.pages - 1)
        )
        widget = getattr(self.thumb, "instance", None)
        if widget is None:
            return
        try:
            from enigma import ePoint, eSize
            widget.resize(eSize(self.width, self.thumb_height))
            widget.move(ePoint(self.x, self.thumb_top))
        except (ImportError, AttributeError, RuntimeError, TypeError):
            # The static skin position remains the fallback on old firmware.
            pass
