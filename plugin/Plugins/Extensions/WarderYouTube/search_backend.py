# -*- coding: utf-8 -*-
"""Optional yt-dlp search backend with no Google API key.

This module has no Enigma2 dependencies. search_with_ytdlp blocks:
the caller must run it via deferToThread, never in a GUI callback.
"""
import html
import json
import re
import shutil
import subprocess
from urllib.parse import urlsplit

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
PAGE_SIZE = 15
MAX_RESULTS = 60
TIMEOUT = 25
MAX_OUTPUT = 2 * 1024 * 1024


class SearchBackendError(Exception):
    pass


def select_backend(api_key, have_ytdlp):
    if isinstance(api_key, str) and api_key.strip():
        return "api"
    return "yt-dlp" if have_ytdlp else None


def page_offset(token):
    if not token:
        return 0
    if token not in ("yd:15", "yd:30", "yd:45"):
        raise SearchBackendError("Invalid search page.")
    return int(token[3:])


def image_url(url, video_id):
    if isinstance(url, str) and len(url) < 2048:
        try:
            u = urlsplit(url)
            if (u.scheme == "https"
                    and u.hostname in ("i.ytimg.com", "img.youtube.com")
                    and u.port in (None, 443)
                    and not u.username and not u.password
                    and u.path.startswith(("/vi/", "/vi_webp/"))):
                return url
        except ValueError:
            pass
    return "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id


def parse_flat_results(data, offset=0):
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise SearchBackendError("Invalid YouTube search result.")
    entries = data["entries"]
    if len(entries) > MAX_RESULTS:
        raise SearchBackendError("Too many YouTube results.")
    items = []
    for entry in entries[offset:offset + PAGE_SIZE]:
        if not isinstance(entry, dict):
            continue
        vid = entry.get("id")
        if not isinstance(vid, str) or not VIDEO_ID.fullmatch(vid):
            continue
        thumbnail = entry.get("thumbnail")
        if not thumbnail:
            thumbnails = entry.get("thumbnails") or []
            if isinstance(thumbnails, list):
                for thumb in reversed(thumbnails):
                    if isinstance(thumb, dict) and thumb.get("url"):
                        thumbnail = thumb["url"]
                        break
        date = entry.get("upload_date")
        items.append({
            "video_id": vid,
            "title": html.unescape(str(entry.get("title") or "Untitled video"))[:200],
            "channel": html.unescape(str(entry.get("channel") or entry.get("uploader") or ""))[:120],
            "thumbnail_url": image_url(thumbnail, vid),
            "published_at": date if isinstance(date, str) and len(date) == 8 and date.isdigit() else "",
        })
    next_offset = offset + PAGE_SIZE
    more = len(entries) >= next_offset and next_offset < MAX_RESULTS
    return {"items": items, "next_page_token": ("yd:%d" % next_offset) if more else ""}


def search_with_ytdlp(query, token="", runner=subprocess.run,
                      which=shutil.which, timeout=TIMEOUT):
    """Read one page from ytsearch15/30/45/60; no shell or implicit download."""
    if (not isinstance(query, str) or not query.strip() or len(query.strip()) > 160
            or any(c in query for c in "\r\n\0")):
        raise SearchBackendError("Enter a valid search phrase (max 160 characters).")
    offset = page_offset(token)
    command = which("yt-dlp")
    if not command:
        raise SearchBackendError("yt-dlp is not available on this receiver.")
    argv = [
        command, "--ignore-config", "--no-warnings", "--no-progress",
        "--skip-download", "--flat-playlist", "--dump-single-json",
        "--socket-timeout", "8", "--retries", "1", "--extractor-retries", "1",
        "--", "ytsearch%d:%s" % (offset + PAGE_SIZE, query.strip())
    ]
    try:
        result = runner(
            argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        raise SearchBackendError("YouTube search timed out.")
    except OSError:
        raise SearchBackendError("yt-dlp could not start.")
    if result.returncode:
        raise SearchBackendError("YouTube search failed. yt-dlp may need updating.")
    if not isinstance(result.stdout, str) or len(result.stdout) > MAX_OUTPUT:
        raise SearchBackendError("YouTube search response is too large.")
    try:
        result_data = json.loads(result.stdout)
    except ValueError:
        raise SearchBackendError("Invalid YouTube search data.")
    return parse_flat_results(result_data, offset)
