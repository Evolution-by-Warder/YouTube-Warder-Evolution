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


# The anonymous YouTube home feed does not require an owner's Data API key.
# It is not a stable public API; failures must fall back to the local library.
import re

PUBLIC_HOME_URL = "https://www.youtube.com/?gl=SK&hl=sk"
PUBLIC_MAX_HTML = 4 * 1024 * 1024
INITIAL_DATA = re.compile(r"(?:var\s+)?ytInitialData\s*=\s*")


def _rendered_text(node):
    if isinstance(node, str):
        return html.unescape(node)
    if isinstance(node, dict):
        if isinstance(node.get("simpleText"), str):
            return html.unescape(node["simpleText"])
        if isinstance(node.get("content"), str):
            return html.unescape(node["content"])
        runs = node.get("runs")
        if isinstance(runs, list):
            return html.unescape("".join(str(r.get("text") or "")
                                         for r in runs if isinstance(r, dict)))
    return ""


def parse_public_home(html_text):
    """Extract only actual public videos from YouTube's anonymous home page.

    Missing initial data, login/consent pages and changed layouts are expected
    possibilities; they are never treated as successful empty recommendations.
    """
    if not isinstance(html_text, str) or len(html_text) > PUBLIC_MAX_HTML:
        raise SearchError("Public YouTube home response is invalid.")
    match = INITIAL_DATA.search(html_text)
    if match is None:
        raise SearchError("Public YouTube home list is unavailable.")
    try:
        data, unused = json.JSONDecoder().raw_decode(
            html_text[match.end():].lstrip()
        )
    except (ValueError, TypeError):
        raise SearchError("Public YouTube home list is unavailable.")
    if not isinstance(data, dict):
        raise SearchError("Public YouTube home list is invalid.")

    results, used, stack, visited = [], set(), [data], 0
    while stack and len(results) < MAX_RESULTS and visited < 14000:
        node = stack.pop()
        visited += 1
        if isinstance(node, dict):
            renderer = (node.get("videoRenderer")
                        or node.get("gridVideoRenderer")
                        or node.get("compactVideoRenderer"))
            if isinstance(renderer, dict):
                video_id = renderer.get("videoId")
                title = _rendered_text(renderer.get("title"))
                channel = (_rendered_text(renderer.get("ownerText"))
                           or _rendered_text(renderer.get("longBylineText"))
                           or _rendered_text(renderer.get("shortBylineText")))
            elif isinstance(node.get("lockupViewModel"), dict):
                model = node["lockupViewModel"]
                video_id = model.get("contentId")
                meta = model.get("metadata") or {}
                metadata = meta.get("lockupMetadataViewModel") or {}
                title = _rendered_text(metadata.get("title"))
                byline = metadata.get("metadata") or {}
                channel = _rendered_text(byline.get("contentMetadataViewModel"))
            else:
                video_id = None
            if (isinstance(video_id, str) and VIDEO_ID.fullmatch(video_id)
                    and title and video_id not in used):
                used.add(video_id)
                results.append({
                    "video_id": video_id,
                    "title": title[:200],
                    "channel": channel[:120],
                    "published_at": "",
                    "thumbnail_url": ("https://i.ytimg.com/vi/%s/mqdefault.jpg"
                                      % video_id),
                })
            for child in reversed(list(node.values())):
                if isinstance(child, (dict, list)):
                    stack.append(child)
        elif isinstance(node, list):
            for child in reversed(node):
                if isinstance(child, (dict, list)):
                    stack.append(child)
    if not results:
        raise SearchError("Public YouTube home did not return usable videos.")
    return results


def public_home_videos(opener=urlopen, timeout=8):
    """Anonymous public browsing, never personalized and never signed in."""
    request = Request(
        PUBLIC_HOME_URL,
        headers={
            "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                           "AppleWebKit/537.36 Chrome/130.0 Safari/537.36"),
            "Accept-Language": "sk-SK,sk;q=0.9,en;q=0.5",
            "Accept": "text/html",
        }
    )
    try:
        response = opener(request, timeout=timeout)
        try:
            final_url = response.geturl() if hasattr(response, "geturl") else PUBLIC_HOME_URL
            if not isinstance(final_url, str) or not final_url.startswith(
                ("https://www.youtube.com/", "https://youtube.com/")
            ):
                raise SearchError("Public YouTube home redirected elsewhere.")
            body = response.read(PUBLIC_MAX_HTML + 1)
        finally:
            response.close()
        if len(body) > PUBLIC_MAX_HTML:
            raise SearchError("Public YouTube home response is too large.")
        return parse_public_home(body.decode("utf-8", "replace"))
    except (HTTPError, URLError, OSError):
        raise SearchError("Public YouTube home is temporarily unavailable.")
