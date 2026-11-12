# -*- coding: utf-8 -*-
"""Native Enigma2/GStreamer playback adapter, without a custom renderer.

OpenATV 7.6 MoviePlayer restores the previous channel automatically ONLY
when fromMovieSelection=True. We intentionally use False to avoid manipulating
the movie list, so this adapter must explicitly restore the previous service.
"""
from enigma import eServiceReference
from Screens.InfoBar import MoviePlayer

SERVICE_TYPE_GSTREAMER = 4097


def open_player(session, stream_url, video_title, on_close=None):
    """Use the built-in MoviePlayer and restore live TV when it closes.

    The caller must validate the resolved HTTPS stream URL first. No signed
    stream URL is written to logs, local history or configuration.
    """
    previous_service = session.nav.getCurrentlyPlayingServiceOrGroup()
    service = eServiceReference(SERVICE_TYPE_GSTREAMER, 0, stream_url)
    service.setName((video_title or "YouTube video")[:200])

    def finish(*args):
        try:
            if previous_service is not None:
                session.nav.playService(previous_service)
        finally:
            if on_close is not None:
                on_close(*args)

    try:
        return session.openWithCallback(
            finish, MoviePlayer, service, fromMovieSelection=False
        )
    except Exception:
        # A failed dialog creation may have already started the video stream.
        if previous_service is not None:
            session.nav.playService(previous_service)
        raise
