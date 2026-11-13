# -*- coding: utf-8 -*-
"""Official regional popular videos for the Warder Home feed.

Never personalize or invent recommendations. Blocking requests run exclusively
through a Twisted worker; never expose credential-bearing URLs in errors.
"""
import html
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .api import SearchError, MAX_RESPONSE_BYTES, VIDEO_ID

POPULAR_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
REGION = "SK"
MAX_RESULTS = 12


def parse_popular_response(payload):
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise SearchError("YouTube returned invalid popular video data.")
    if "error" in payload:
        raise SearchError("YouTube did not provide popular videos.")
    items = []
    for entry in payload["items"][:MAX_RESULTS]:
        if not isinstance(entry, dict):
            continue
        video_id = entry.get("id")
        snippet = entry.get("snippet")
        if (not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id)
                or not isinstance(snippet, dict)):
            continue
        items.append({
            "video_id": video_id,
            "title": html.unescape(str(snippet.get("title") or "YouTube video"))[:200],
            "channel": html.unescape(str(snippet.get("channelTitle") or ""))[:120],
            "published_at": str(snippet.get("publishedAt") or "")[:30],
            "thumbnail_url": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id,
        })
    return items


def popular_videos(api_key, opener=urlopen, timeout=8):
    if not isinstance(api_key, str) or not api_key.strip():
        raise SearchError("YouTube API key is required for popular videos.")
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": REGION,
        "maxResults": MAX_RESULTS,
        "key": api_key.strip(),
    }
    request = Request(
        POPULAR_ENDPOINT + "?" + urlencode(params),
        headers={"Accept": "application/json", "User-Agent": "WarderYouTube/0.0.8"}
    )
    try:
        response = opener(request, timeout=timeout)
        try:
            body = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            response.close()
        if len(body) > MAX_RESPONSE_BYTES:
            raise SearchError("YouTube returned an oversized response.")
        try:
            result = json.loads(body.decode("utf-8"))
        except (UnicodeError, ValueError):
            raise SearchError("YouTube returned invalid popular video data.")
        return parse_popular_response(result)
    except HTTPError as error:
        if error.code in (400, 401, 403):
            raise SearchError("YouTube API key or quota could not load popular videos.")
        raise SearchError("YouTube popular video request failed.")
    except (URLError, OSError):
        raise SearchError("Popular videos are temporarily unavailable.")
