# -*- coding: utf-8 -*-
"""Bounded, ephemeral thumbnail cache. This module runs in a worker thread.

Two downloads at most are scheduled by the UI. Images stay in /tmp (no
persistent flash cache), never exceed 240 KiB per image, 4 MiB total/36 files.
"""
import hashlib
import os
import re
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

CACHE_DIR = "/tmp/warder-youtube-thumbs"
MAX_BYTES_PER_IMAGE = 240 * 1024
MAX_CACHE_BYTES = 4 * 1024 * 1024
MAX_CACHE_FILES = 36
MAX_CACHE_AGE = 30 * 60  # stale thumbnails after 30 minutes without reuse
MAX_PARTIAL_AGE = 10 * 60  # only abandoned downloads, not active workers
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
    """Bound temp usage on every access, including existing cached images.

    Remove old thumbnails and abandoned partial writes; keep recently used
    files and retain at most 36 images/4 MiB for responsive page navigation.
    """
    if os.path.islink(cache_dir) or not os.path.isdir(cache_dir):
        return
    now = time.time()
    entries = []
    total = 0
    for name in os.listdir(cache_dir):
        path = os.path.join(cache_dir, name)
        if os.path.islink(path) or not os.path.isfile(path):
            continue
        if not (_CACHE_IMAGE_NAME.fullmatch(name)
                or _CACHE_PARTIAL_NAME.fullmatch(name)):
            continue
        try:
            st = os.stat(path)
        except OSError:
            continue
        age = max(0, now - st.st_mtime)
        if _CACHE_PARTIAL_NAME.fullmatch(name):
            if age >= MAX_PARTIAL_AGE:
                try:
                    os.unlink(path)
                except OSError:
                    pass
            continue
        if age >= MAX_CACHE_AGE or st.st_size <= 0 or st.st_size > MAX_BYTES_PER_IMAGE:
            try:
                os.unlink(path)
            except OSError:
                pass
            continue
        total += st.st_size
        entries.append((st.st_mtime, path, st.st_size))
    entries.sort()
    while entries and (len(entries) > MAX_CACHE_FILES or total > MAX_CACHE_BYTES):
        _, path, size = entries.pop(0)
        try:
            os.unlink(path)
            total -= size
        except OSError:
            pass


# Only files created by this module may be removed. Never clean /tmp itself.
_CACHE_IMAGE_NAME = re.compile(r"^[0-9a-f]{64}\.(?:jpg|png)$")
_CACHE_PARTIAL_NAME = re.compile(r"^tmp[^/]*\.partial$")


def cleanup_cache(cache_dir=CACHE_DIR):
    """Remove owned thumbnail files after the final worker finishes.

    Do not follow symlinks, delete other apps' files or recursively delete
    arbitrary content. A failed cleanup is harmless: /tmp cache is bounded.
    """
    try:
        if os.path.islink(cache_dir) or not os.path.isdir(cache_dir):
            return
        for name in os.listdir(cache_dir):
            if not (_CACHE_IMAGE_NAME.fullmatch(name)
                    or _CACHE_PARTIAL_NAME.fullmatch(name)):
                continue
            path = os.path.join(cache_dir, name)
            if os.path.islink(path) or not os.path.isfile(path):
                continue
            try:
                os.unlink(path)
            except OSError:
                pass
        try:
            os.rmdir(cache_dir)  # only when empty, never recursive
        except OSError:
            pass
    except OSError:
        pass

def fetch_thumbnail(url, opener=urlopen, cache_dir=CACHE_DIR):
    """Network I/O only from worker; never expose URL contents as GUI error."""
    validate_thumbnail_url(url)
    name = hashlib.sha256(url.encode("utf-8")).hexdigest()
    try:
        if os.path.islink(cache_dir):
            raise OSError('Unsafe thumbnail cache path')
        os.makedirs(cache_dir, mode=0o700, exist_ok=True)
        _prune(cache_dir)
        for ext in (".jpg", ".png"):
            cached = os.path.join(cache_dir, name + ext)
            if os.path.isfile(cached) and 0 < os.path.getsize(cached) <= MAX_BYTES_PER_IMAGE:
                os.utime(cached, None)
                _prune(cache_dir)
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
