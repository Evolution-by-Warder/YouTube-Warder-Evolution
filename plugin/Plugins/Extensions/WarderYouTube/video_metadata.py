# -*- coding: utf-8 -*-
"""YouTube Data API videos.list details; never called on the Enigma2 GUI thread.

One detail request costs much less quota than search. No API key, token,
signed URL or HTTP response body is printed or stored by this module.
"""
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
DURATION = re.compile(r"^P(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?)?$")
MAX_RESPONSE_BYTES = 512 * 1024


class VideoInfoError(Exception):
    """Safe status; never contains the URL or API key."""


def display_duration(duration):
    """ISO 8601 YouTube duration into e.g. 2:03 or 1:02:03."""
    if not isinstance(duration, str) or not duration:
        return "Neznáma"
    match = DURATION.fullmatch(duration)
    if match is None or not any(v is not None for v in match.groups()):
        return "Neznáma"
    days, hours, minutes, seconds = (int(v or "0") for v in match.groups())
    total = days * 86400 + hours * 3600 + minutes * 60 + seconds
    if total >= 3600:
        return "%d:%02d:%02d" % (total // 3600, (total // 60) % 60, total % 60)
    return "%d:%02d" % (total // 60, total % 60)


def parse_video_info(payload, expected_id):
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise VideoInfoError("YouTube returned invalid video metadata.")
    found = next(
        (item for item in payload["items"] if isinstance(item, dict)
         and item.get("id") == expected_id), None
    )
    if found is None:
        raise VideoInfoError("Video details are unavailable.")
    snippet = found.get("snippet") or {}
    content = found.get("contentDetails") or {}
    stats = found.get("statistics") or {}
    if not isinstance(snippet, dict) or not isinstance(content, dict) or not isinstance(stats, dict):
        raise VideoInfoError("YouTube returned invalid video metadata.")
    views = stats.get("viewCount")
    if isinstance(views, str) and views.isdigit():
        view_count = format(int(views), ",").replace(",", " ")
    else:
        view_count = "Neznámy"
    return {
        "video_id": expected_id,
        "title": html.unescape(str(snippet.get("title") or "Video"))[:200],
        "channel": html.unescape(str(snippet.get("channelTitle") or ""))[:120],
        "duration": display_duration(content.get("duration")),
        "views": view_count,
        "description": html.unescape(str(snippet.get("description") or ""))[:500],
        "published_at": str(snippet.get("publishedAt") or "")[:30],
    }


def fetch_video_info(video_id, api_key, opener=urlopen, timeout=8):
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise VideoInfoError("Invalid video ID.")
    if not isinstance(api_key, str) or not api_key.strip():
        raise VideoInfoError("Video details require a personal YouTube API key.")
    url = ENDPOINT + "?" + urlencode({
        "part": "snippet,contentDetails,statistics", "id": video_id, "key": api_key.strip()
    })
    req = Request(url, headers={
        "Accept": "application/json", "User-Agent": "WarderYouTube/0.0.6"
    })
    try:
        response = opener(req, timeout=timeout)
        try:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            response.close()
        if len(raw) > MAX_RESPONSE_BYTES:
            raise VideoInfoError("Video metadata exceeds the size limit.")
        try:
            data = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeError):
            raise VideoInfoError("YouTube returned invalid metadata.")
        return parse_video_info(data, video_id)
    except HTTPError as exc:
        if exc.code in (400, 401, 403):
            raise VideoInfoError("YouTube rejected video details; check API access or quota.")
        raise VideoInfoError("Video metadata request failed (HTTP %d)." % exc.code)
    except (URLError, OSError):
        raise VideoInfoError("Network unavailable while loading video details.")
