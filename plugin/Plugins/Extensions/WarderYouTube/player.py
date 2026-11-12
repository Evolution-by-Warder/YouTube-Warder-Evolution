# -*- coding: utf-8 -*-
"""Native Enigma2/GStreamer playback adapter; no custom renderer.

Compatible baseline under investigation: service type 4097 and MoviePlayer.
Do not assume a receiver supports all codecs or signed URLs.
"""
from enigma import eServiceReference
from Screens.InfoBar import MoviePlayer

SERVICE_TYPE_GSTREAMER = 4097


def open_player(session, stream_url, video_title, on_close=None):
    """Open native player and restore previous TV service when it is closed.

    The caller MUST validate stream_url in the resolver worker first.
    fromMovieSelection=False avoids changing movie-list settings/history.
    """
    service = eServiceReference(SERVICE_TYPE_GSTREAMER, 0, stream_url)
    service.setName((video_title or "YouTube video")[:200])
    if on_close is None:
        session.open(MoviePlayer, service, fromMovieSelection=False)
    else:
        session.openWithCallback(
            on_close, MoviePlayer, service, fromMovieSelection=False
        )
