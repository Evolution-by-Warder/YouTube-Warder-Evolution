# -*- coding: utf-8 -*-
"""Native MoviePlayer failover adapted from our proven Warder Radio player.

Only the image's existing 4097 / registered 5002 services are used. Nothing
is installed or modified outside this plugin.
"""
import shutil
import enigma
from enigma import eServiceReference, iPlayableService
from Components.ServiceEventTracker import ServiceEventTracker
from Screens.InfoBar import MoviePlayer


def dash_available():
    """Use DASH only when both Exteplayer3 and service 5002 are available."""
    if not shutil.which("exteplayer3"):
        return False
    try:
        center = enigma.eServiceCenter.getInstance()
        return center.info(eServiceReference(5002, 0, "https://www.youtube.com/")) is not None
    except (AttributeError, RuntimeError, TypeError):
        return False


class WarderYouTubePlayer(MoviePlayer):
    ENABLE_RESUME_SUPPORT = False

    def __init__(self, session, streams, title, previous_service):
        streams = list(streams)[:8]
        if not streams or any(not isinstance(s, dict)
                              or s.get("service_type") not in (4097, 5002)
                              or not isinstance(s.get("url"), str)
                              for s in streams):
            raise ValueError("Unsupported YouTube stream candidates")
        self.streams = streams
        self.title = (title or "YouTube video")[:200]
        self.previous_service = previous_service
        self.video_index = 0
        self.finished = False
        self.failed = False
        first = self.make_reference(streams[0])
        self.video_reference_keys = {first.toString()}
        kwargs = {"lastservice": previous_service}
        # Keep the image's own close handler, avoiding a duplicate TV restart.
        code = getattr(MoviePlayer.__init__, "__code__", None)
        if code is not None and "fromMovieSelection" in code.co_varnames[:code.co_argcount]:
            kwargs["fromMovieSelection"] = False
        MoviePlayer.__init__(self, session, first, **kwargs)
        self.skinName = ["MoviePlayer"]
        self.onClose.insert(0, self.prepare_return)
        event_map = {iPlayableService.evTuneFailed: self.stream_error}
        if hasattr(iPlayableService, "evUser"):
            event_map[iPlayableService.evUser + 12] = self.stream_error
        self.video_events = ServiceEventTracker(screen=self, eventmap=event_map)

    def make_reference(self, stream):
        ref = eServiceReference(stream["service_type"], 0, stream["url"])
        ref.setName(self.title)
        return ref

    def owns(self):
        current = self.session.nav.getCurrentlyPlayingServiceReference()
        return current is not None and current.toString() in self.video_reference_keys

    def prepare_return(self):
        if self.finished:
            return
        self.finished = True
        current = self.session.nav.getCurrentlyPlayingServiceReference()
        if self.owns() or current is None:
            self.lastservice = self.previous_service
        else:
            # An external channel change must not be reversed on EXIT.
            self.lastservice = current

    def leavePlayer(self):
        self.close()

    def leavePlayerOnExit(self):
        self.close()

    def handleLeave(self, how):
        self.close()

    def doEofInternal(self, playing):
        if self.execing and playing and not self.finished:
            self.close()

    def stream_error(self):
        if self.finished:
            return
        current = self.session.nav.getCurrentlyPlayingServiceReference()
        if current is not None and not self.owns():
            self.close()
            return
        while self.video_index + 1 < len(self.streams):
            self.video_index += 1
            next_ref = self.make_reference(self.streams[self.video_index])
            self.cur_service = next_ref
            self.video_reference_keys.add(next_ref.toString())
            try:
                if self.session.nav.playService(next_ref) in (None, 0):
                    return
            except Exception:
                pass
        self.failed = True
        self.close(True)


def open_player(session, streams, video_title, on_close=None):
    """Open native MoviePlayer; only restore manually if dialog creation fails."""
    previous = session.nav.getCurrentlyPlayingServiceOrGroup()
    try:
        return session.openWithCallback(
            on_close or (lambda *args: None),
            WarderYouTubePlayer, streams, video_title, previous
        )
    except Exception:
        if previous is not None:
            session.nav.playService(previous)
        raise
