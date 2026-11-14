# -*- coding: utf-8 -*-
"""Bounded, ephemeral thumbnail cache. This module runs in a worker thread.

Two downloads at most are scheduled by the UI. Images stay in /tmp (no
persistent flash cache), never exceed 240 KiB per image, 4 MiB total/36 files.
"""
import hashlib
import os
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

CACHE_DIR = "/tmp/warder-youtube-thumbs"
MAX_BYTES_PER_IMAGE = 240 * 1024
MAX_CACHE_BYTES = 4 * 1024 * 1024
MAX_CACHE_FILES = 36
REQUEST_TIMEOUT = 6
ALLOWED_HOSTS = ("i.ytimg.com", "img.youtube.com")
CHANNEL_IMAGE_HOSTS = ("yt3.ggpht.com", "yt3.googleusercontent.com")


class ThumbnailError(Exception):
    pass


def validate_thumbnail_url(url):
    if not isinstance(url, str) or not url or len(url) > 2048:
        raise ThumbnailError("Invalid thumbnail URL.")
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower()
        port = parts.port
    except ValueError:
        raise ThumbnailError("Invalid thumbnail URL.")
    video_image = (host in ALLOWED_HOSTS and
                   parts.path.startswith(("/vi/", "/vi_webp/")))
    channel_image = (host in CHANNEL_IMAGE_HOSTS and
                     parts.path.startswith("/") and len(parts.path) >= 5)
    if (parts.scheme != "https" or not (video_image or channel_image)
            or port not in (None, 443) or parts.username or parts.password
            or parts.fragment):
        raise ThumbnailError("Unsupported thumbnail URL.")
    return url


def _prune(cache_dir):
    entries = []
    total = 0
    for name in os.listdir(cache_dir):
        if not name.endswith((".jpg", ".png")):
            continue
        path = os.path.join(cache_dir, name)
        if os.path.islink(path) or not os.path.isfile(path):
            continue
        try:
            st = os.stat(path)
        except OSError:
            continue
        total += st.st_size
        entries.append((st.st_mtime, path, st.st_size))
    entries.sort()
    while entries and (len(entries) > MAX_CACHE_FILES or total > MAX_CACHE_BYTES):
        _, path, size = entries.pop(0)
        try:
            os.unlink(path)
        except OSError:
            pass
        total -= size


def fetch_thumbnail(url, opener=urlopen, cache_dir=CACHE_DIR):
    """Network I/O only from worker; never expose URL contents as GUI error."""
    validate_thumbnail_url(url)
    name = hashlib.sha256(url.encode("utf-8")).hexdigest()
    try:
        os.makedirs(cache_dir, mode=0o700, exist_ok=True)
        for ext in (".jpg", ".png"):
            cached = os.path.join(cache_dir, name + ext)
            if os.path.isfile(cached) and 0 < os.path.getsize(cached) <= MAX_BYTES_PER_IMAGE:
                os.utime(cached, None)
                return cached
    except OSError:
        raise ThumbnailError("Thumbnail cache is unavailable.")

    try:
        response = opener(Request(
            url, headers={"Accept": "image/jpeg,image/png", "User-Agent": "WarderYouTube/0.0.4"}
        ), timeout=REQUEST_TIMEOUT)
        try:
            validate_thumbnail_url(response.geturl() if hasattr(response, "geturl") else url)
            image = response.read(MAX_BYTES_PER_IMAGE + 1)
        finally:
            response.close()
    except (HTTPError, URLError, OSError):
        raise ThumbnailError("Could not download this thumbnail.")
    if not isinstance(image, bytes) or len(image) > MAX_BYTES_PER_IMAGE:
        raise ThumbnailError("Thumbnail exceeds the size limit.")
    if image.startswith(b"\xff\xd8\xff"):
        ext = ".jpg"
    elif image.startswith(b"\x89PNG\r\n\x1a\n"):
        ext = ".png"
    else:
        raise ThumbnailError("Corrupt or unsupported image data.")

    target = os.path.join(cache_dir, name + ext)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".partial", dir=cache_dir, delete=False) as f:
            temporary = f.name
            f.write(image)
        os.replace(temporary, target)
        _prune(cache_dir)
        return target
    except OSError:
        raise ThumbnailError("Thumbnail cache is unavailable.")
    finally:
        if temporary and os.path.exists(temporary):
            try:
                os.unlink(temporary)
            except OSError:
                pass
