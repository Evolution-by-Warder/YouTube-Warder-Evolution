# -*- coding: utf-8 -*-
"""Small, replaceable YouTube Data API search adapter.

Network I/O is blocking: call this module from a worker, NEVER from the
Enigma2 GUI thread. Nothing from Enigma2 is imported here.
"""
import html
import json
import re

from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SEARCH_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
MAX_RESPONSE_BYTES = 1024 * 1024
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


class SearchError(Exception):
    """Error safe to display to users: never includes tokens or request URLs."""


def parse_search_response(payload):
    """Return a small, GUI-independent dict from the official search response."""
    if not isinstance(payload, dict):
        raise SearchError("Invalid YouTube response.")
    if "error" in payload:
        raise SearchError("YouTube rejected the request. Check your API key and quota.")
    if not isinstance(payload.get("items"), list):
        raise SearchError("Invalid YouTube response: missing video list.")

    items = []
    for item in payload["items"]:
        if not isinstance(item, dict):
            continue
        video_id = item.get("id", {})
        if not isinstance(video_id, dict):
            continue
        video_id = video_id.get("videoId")
        if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
            continue
        snippet = item.get("snippet")
        if not isinstance(snippet, dict):
            continue
        # Use a canonical JPEG on the official YouTube image host. Some API
        # snippets return missing, redirected or WebP thumbnails which the
        # receiver's native ePicLoad cannot reliably decode. A validated ID
        # fixes the origin and avoids passing untrusted URLs to the downloader.
        thumb_url = "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id
        title = html.unescape(str(snippet.get("title") or "Untitled video"))[:200]
        channel = html.unescape(str(snippet.get("channelTitle") or ""))[:120]
        items.append({
            "video_id": video_id,
            "title": title,
            "channel": channel,
            "thumbnail_url": thumb_url,
            "published_at": str(snippet.get("publishedAt") or "")[:30],
        })
    token = payload.get("nextPageToken") or ""
    if not isinstance(token, str) or len(token) > 512:
        token = ""
    return {"items": items, "next_page_token": token}


def search_videos(query, api_key, page_token="", opener=urlopen, timeout=8):
    """Perform one API search; designed for Twisted deferToThread.

    Does not expose the key, URL, or upstream response body in error messages.
    """
    if not isinstance(api_key, str) or not api_key.strip():
        raise SearchError("Set your YouTube Data API key in Settings first.")
    if not isinstance(query, str) or not query.strip():
        raise SearchError("Enter a search phrase.")
    query = query.strip()
    if len(query) > 160:
        raise SearchError("Search phrase is too long (160 characters maximum).")
    if page_token and (not isinstance(page_token, str) or len(page_token) > 512):
        raise SearchError("Invalid search page token.")

    params = {
        "part": "snippet", "type": "video", "maxResults": 15,
        "q": query, "key": api_key.strip(), "safeSearch": "moderate",
    }
    if page_token:
        params["pageToken"] = page_token
    url = SEARCH_ENDPOINT + "?" + urlencode(params)
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "WarderYouTube/0.0.2"})
    try:
        response = opener(request, timeout=timeout)
        try:
            content = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            response.close()
        if len(content) > MAX_RESPONSE_BYTES:
            raise SearchError("YouTube returned an unexpectedly large response.")
        try:
            payload = json.loads(content.decode("utf-8"))
        except (UnicodeError, ValueError):
            raise SearchError("YouTube returned invalid data.")
        return parse_search_response(payload)
    except HTTPError as error:
        if error.code in (400, 401, 403):
            raise SearchError("YouTube rejected the request (HTTP %s). Check your API key or quota." % error.code)
        raise SearchError("YouTube request failed (HTTP %s)." % error.code)
    except (URLError, OSError):
        raise SearchError("Network unavailable or YouTube did not respond.")
