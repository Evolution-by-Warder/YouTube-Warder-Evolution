# -*- coding: utf-8 -*-
"""Independent adaptation of the proven Warder Radio YouTube resolver.

The included GPL-2.0 YouTube extraction sources and attribution are preserved
under youtube_engine/. Called only from a worker, never from the GUI thread.
"""
import json
import ssl
import time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from .youtube_engine.settings import config

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36"
MAX_RESPONSE_BYTES = 3 * 1024 * 1024
LIMIT = 8


def allowed_origin(url, media=False):
    if not isinstance(url, str) or not url or len(url) > 8192:
        raise ValueError("Unsupported YouTube address")
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
        allowed = (host == "googlevideo.com" or host.endswith(".googlevideo.com")) if media else (
            host == "youtube.com" or host.endswith(".youtube.com")
            or host == "googlevideo.com" or host.endswith(".googlevideo.com"))
        if (parts.scheme != "https" or not allowed or parts.username is not None
                or parts.password is not None or parts.port not in (None, 443)
                or any(char in url for char in "\r\n\0")):
            raise ValueError("Unsupported YouTube address")
    except ValueError:
        raise ValueError("Unsupported YouTube address") from None
    return url


class Transport:
    """Verified HTTPS/URL allowlist with a single bounded request deadline."""
    def __init__(self, opener=None, clock=time.monotonic):
        self.clock = clock
        self.deadline = clock() + 30
        self.opener = opener or (lambda request, timeout: urlopen(
            request, timeout=timeout, context=ssl.create_default_context()))

    def page(self, url, data=None, headers=None):
        allowed_origin(url)
        remaining = self.deadline - self.clock()
        if remaining <= 0:
            raise TimeoutError("YouTube lookup deadline exceeded")
        body = json.dumps(data).encode("utf-8") if data is not None else None
        request_headers = {"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"}
        request_headers.update(headers or {})
        if body is not None:
            request_headers["Content-Type"] = "application/json"
        req = Request(url, data=body, headers=request_headers)
        chunks, count = [], 0
        with self.opener(req, timeout=min(5, remaining)) as response:
            target = (getattr(response, "url", None)
                      or (response.geturl() if hasattr(response, "geturl") else url))
            allowed_origin(target)
            while True:
                if self.clock() >= self.deadline:
                    raise TimeoutError("YouTube lookup deadline exceeded")
                chunk = response.read(min(65536, MAX_RESPONSE_BYTES + 1 - count))
                if not chunk:
                    break
                count += len(chunk)
                if count > MAX_RESPONSE_BYTES:
                    raise ValueError("YouTube response exceeded size limit")
                chunks.append(chunk)
        return b"".join(chunks).decode("utf-8", "replace")


def extract_candidates(video_id, quality="720", dash=False,
                       resolver_factory=None, transport_factory=Transport):
    """Return up to eight validated playable sources, with native backends.

    360/720 set the MP4 format ceiling. HLS is adaptive and may dynamically
    choose another resolution; kept as a fallback rather than forced quality.
    """
    from .resolver import video_page_url
    video_page_url(video_id)
    if quality not in ("360", "720"):
        raise ValueError("Invalid quality")
    if resolver_factory is None:
        from .youtube_engine.extractor import YouTubeVideoUrl
        resolver_factory = YouTubeVideoUrl
    previous_quality = config.plugins.YouTube.maxResolution.value
    config.plugins.YouTube.maxResolution.value = "18" if quality == "360" else "22"
    try:
        resolver = resolver_factory()
        resolver.enable_dash = bool(dash)
        resolver._download_webpage = transport_factory().page
        first = resolver.extract(video_id)
        candidates = [first] + list(getattr(resolver, "playback_urls", []))
    finally:
        config.plugins.YouTube.maxResolution.value = previous_quality
    result, seen = [], set()
    for url in candidates:
        if not isinstance(url, str) or url in seen:
            continue
        parts = url.split("&suburi=")
        try:
            if len(parts) == 1:
                allowed_origin(parts[0], media=True)
                kind = 4097
            elif len(parts) == 2 and dash:
                allowed_origin(parts[0], media=True)
                allowed_origin(parts[1], media=True)
                kind = 5002
            else:
                continue
        except ValueError:
            continue
        seen.add(url)
        result.append({"url": url, "service_type": kind})
        if len(result) == LIMIT:
            break
    if not result:
        raise ValueError("No safe playable YouTube stream was found")
    return result
