# -*- coding: utf-8 -*-
"""Six bounded Home preview thumbnails using native Enigma2 ePicLoad.

The same 2-network-worker / 1-decoder ceiling as the existing video grid.
Never load thumbnails for hidden pages or stale menu selections.
"""
from enigma import ePicLoad
from twisted.internet.threads import deferToThread

from .thumbnails import fetch_thumbnail

VISIBLE = 6
MAX_DOWNLOADS = 2


class HomeThumbs:
    def __init__(self, screen):
        self.screen = screen
        self.ready = False
        self.closed = False
        self.epoch = 0
        self.active = 0
        self.queue = []
        self.decodes = []
        self.decoding = None
        self.decoder = None
        self.signal = None
        self.connection = None
        self._decoder_generation = 0
        self._decode_callback = None
        # The on-screen ePixmap may lose its buffer while a dialog is open.
        # Retain at most 12 native ePtr frames for safe restoration.
        self.image_cache = {}

    def start(self):
        if self.closed or (self.ready and self.decoder is not None):
            return
        # A missing ePicLoad may recover after an Enigma2 GUI transition.
        self._decoder_generation += 1
        generation = self._decoder_generation
        try:
            decoder = ePicLoad()
            signal = decoder.PictureData
            callback = lambda *args: self._decoded_if_current(generation, *args)
            self.decoder = decoder
            self._decode_callback = callback
            if hasattr(signal, "get"):
                self.signal = signal.get()
                self.signal.append(callback)
            else:
                self.connection = signal.connect(callback)
            self.decoder.setPara(self.decode_parameters())
            self.ready = True
        except Exception:
            self.ready = False
            self._release()
            self.decoder = None

    def _decoded_if_current(self, generation, *args):
        # A late callback from a released decoder must never consume the
        # new decoder's in-flight image or leave its queue permanently stuck.
        if generation != self._decoder_generation:
            return
        self._decoded(*args)

    def _restart_decoder(self):
        """Break an abandoned ePicLoad job after rapid page/menu changes.

        ePicLoad sometimes never emits PictureData for an abandoned decode
        on embedded receivers. Releasing it makes new visible frames progress
        without requiring a full plugin restart.
        """
        self._decoder_generation += 1
        self._release()
        self.decoder = None
        self.decoding = None
        self.ready = False
        if not self.closed:
            self.start()

    def decode_parameters(self):
        width, height = 461, 259
        try:
            widget = self.screen["preview_thumb0"]
            actual = widget.getSize() if getattr(widget, "instance", None) else None
            if (actual and len(actual) == 2 and
                    0 < actual[0] <= 4096 and 0 < actual[1] <= 2160):
                width, height = int(actual[0]), int(actual[1])
        except (AttributeError, TypeError, ValueError, RuntimeError):
            pass
        x, y = 1, 1
        try:
            from Components.AVSwitch import AVSwitch
            value = AVSwitch().getFramebufferScale()
            if (isinstance(value, (tuple, list)) and len(value) == 2
                    and all(type(i) is int and 0 < i <= 16 for i in value)):
                x, y = value
        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError):
            pass
        return (width, height, x, y, False, 1, "#00000000")

    def show(self, items):
        self.epoch += 1
        self.queue = []
        self.decodes = []
        # Never keep a stale decoder lock when another page is selected.
        if self.decoding is not None:
            self._restart_decoder()
        elif self.decoder is None:
            self.start()
        for slot in range(VISIBLE):
            self.screen["preview_thumb%d" % slot].hide()
        if self.closed or not self.ready or self.decoder is None:
            return
        for slot, item in enumerate(items[:VISIBLE]):
            url = item.get("thumbnail_url") if isinstance(item, dict) else None
            if not url:
                continue
            cached = self.image_cache.get(url)
            if cached is not None:
                try:
                    widget = self.screen["preview_thumb%d" % slot]
                    widget.setPixmap(cached)
                    widget.show()
                    continue
                except (AttributeError, TypeError, ValueError, RuntimeError):
                    self.image_cache.pop(url, None)
            self.queue.append((self.epoch, slot, url))
        self._pump()

    def _pump(self):
        if self.closed or not self.ready:
            return
        while self.queue and self.active < MAX_DOWNLOADS:
            req = self.queue.pop(0)
            self.active += 1
            try:
                work = deferToThread(fetch_thumbnail, req[2])
                work.addCallbacks(
                    lambda path, req=req: self._downloaded(req, path),
                    lambda error, req=req: self._downloaded(req, None)
                )
            except Exception:
                self.active = max(0, self.active - 1)

    def _downloaded(self, req, path):
        self.active = max(0, self.active - 1)
        if not self.closed and path and req[0] == self.epoch:
            self.decodes.append((req[0], req[1], path, req[2]))
            self._start_decode()
        self._pump()

    def _start_decode(self):
        if self.closed or self.decoder is None or self.decoding is not None:
            return
        while self.decodes:
            req = self.decodes.pop(0)
            if req[0] != self.epoch:
                continue
            self.decoding = req
            try:
                if self.decoder.startDecode(req[2]) == 0:
                    return
            except Exception:
                pass
            self.decoding = None
            # startDecode failures can leave this particular ePicLoad broken.
            # Retry the next visible frame using a fresh decoder.
            if not self.closed:
                self._restart_decoder()
                return

    def _decoded(self, *args):
        req, self.decoding = self.decoding, None
        if (req is not None and not self.closed and req[0] == self.epoch
                and self.decoder is not None):
            try:
                pixmap = self.decoder.getData()
                if pixmap is not None:
                    widget = self.screen["preview_thumb%d" % req[1]]
                    widget.setPixmap(pixmap)
                    widget.show()
                    self.image_cache[req[3]] = pixmap
                    while len(self.image_cache) > 12:
                        self.image_cache.pop(next(iter(self.image_cache)))
            except (AttributeError, TypeError, ValueError, RuntimeError):
                pass
        self._start_decode()

    def _release(self):
        if self.connection is not None:
            try:
                self.connection.disconnect()
            except (AttributeError, RuntimeError):
                pass
            self.connection = None
        if self.signal is not None:
            try:
                self.signal.remove(self._decode_callback)
            except (ValueError, AttributeError, RuntimeError):
                pass
            self.signal = None
        self._decode_callback = None

    def close(self):
        self.closed = True
        self.epoch += 1
        self._decoder_generation += 1
        self.queue = []
        self.decodes = []
        self.image_cache.clear()
        self._release()
        self.decoder = None
