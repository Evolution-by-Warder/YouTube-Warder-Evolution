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
from .home_categories import CATEGORY_IDS
from .data_auth import (authorize_request, DataAuthorizationError,
                        authorization_error, open_authorized)

POPULAR_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
REGION = "SK"
MAX_RESULTS = 50


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


def popular_videos_page(api_key="", category_id="0", page_token="", region=REGION,
                        opener=urlopen, timeout=8):
    """One bounded YouTube chart page, including the API's real next token.

    A category selection does not claim to reproduce the personalized
    recommendations or "Mixes" from the YouTube website.
    """
    if category_id not in CATEGORY_IDS:
        raise SearchError("Unsupported YouTube video category.")
    if not isinstance(region, str) or len(region) != 2 or not region.isalpha():
        raise SearchError("Invalid YouTube region.")
    if (not isinstance(page_token, str) or len(page_token) > 150
            or (page_token and not all(ch.isascii() and (ch.isalnum() or ch in "-_+=/") for ch in page_token))):
        raise SearchError("Invalid YouTube page token.")
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region.upper(),
        "maxResults": MAX_RESULTS,
    }
    if category_id != "0":
        params["videoCategoryId"] = category_id
    if page_token:
        params["pageToken"] = page_token
    try:
        params, headers = authorize_request(params, {
            "Accept": "application/json", "User-Agent": "WarderYouTube/0.0.8"
        }, api_key)
    except DataAuthorizationError as error:
        raise SearchError(str(error)) from None
    request = Request(POPULAR_ENDPOINT + "?" + urlencode(params), headers=headers)
    try:
        response = open_authorized(request, opener, timeout)
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
        items = parse_popular_response(result)
        token = result.get("nextPageToken") or ""
        if not isinstance(token, str) or len(token) > 150:
            token = ""
        info = result.get("pageInfo") or {}
        total = info.get("totalResults") if isinstance(info, dict) else None
        if type(total) is not int or total <= 0 or total > 100000:
            total = None
        return {"items": items, "next_page_token": token,
                "total_results": total}
    except HTTPError as error:
        if error.code in (400, 401, 403):
            raise SearchError(authorization_error(error.code)) from None
        raise SearchError("YouTube popular video request failed.")
    except (URLError, OSError):
        raise SearchError("Popular videos are temporarily unavailable.")


def popular_videos(api_key, opener=urlopen, timeout=8):
    """Backward-compatible one-page list for existing callers and tests."""
    return popular_videos_page(api_key, opener=opener, timeout=timeout)["items"]


# The anonymous YouTube home feed does not require an owner's Data API key.
# It is not a stable public API; failures must fall back to the local library.
import re

PUBLIC_HOME_URL = "https://www.youtube.com/?gl=SK&hl=sk"
PUBLIC_MAX_HTML = 4 * 1024 * 1024
INITIAL_DATA = re.compile(r"(?:var\s+)?ytInitialData\s*=\s*")


WEB_KEY = re.compile(r'"INNERTUBE_API_KEY"\s*:\s*"([A-Za-z0-9_-]{12,80})"')
WEB_VERSION = re.compile(r'"INNERTUBE_CLIENT_VERSION"\s*:\s*"([A-Za-z0-9._-]{4,80})"')
WEB_VISITOR = re.compile(r'"VISITOR_DATA"\s*:\s*"([A-Za-z0-9_%=-]{1,300})"')
CONTINUATION_URL = "https://www.youtube.com/youtubei/v1/search?"
BROWSE_CONTINUATION_URL = "https://www.youtube.com/youtubei/v1/browse?"
PUBLIC_PAGE_LIMIT = 50
MAX_PAGE_TOKEN = 4096


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


def _initial_data(html_text):
    if not isinstance(html_text, str) or len(html_text) > PUBLIC_MAX_HTML:
        raise SearchError("Public YouTube home response is invalid.")
    match = INITIAL_DATA.search(html_text)
    if match is None:
        raise SearchError("Public YouTube home list is unavailable.")
    try:
        data, unused = json.JSONDecoder().raw_decode(
            html_text[match.end():].lstrip())
    except (ValueError, TypeError):
        raise SearchError("Public YouTube home list is unavailable.") from None
    if not isinstance(data, dict):
        raise SearchError("Public YouTube home list is invalid.")
    return data


def _public_results(data):
    """Walk only a bounded portion of real YouTube renderer data."""
    if not isinstance(data, dict):
        raise SearchError("Public YouTube response is invalid.")
    results, used, stack, visited, continuation = [], set(), [data], 0, ""
    while stack and visited < 18000:
        node = stack.pop()
        visited += 1
        if isinstance(node, dict):
            if not continuation:
                command = (node.get("continuationCommand") or
                           node.get("nextContinuationData"))
                if isinstance(command, dict):
                    candidate = command.get("token") or command.get("continuation")
                    if isinstance(candidate, str) and 0 < len(candidate) <= 3000:
                        continuation = candidate
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
                    and title and video_id not in used
                    and len(results) < PUBLIC_PAGE_LIMIT):
                used.add(video_id)
                results.append({
                    "video_id": video_id, "title": title[:200],
                    "channel": channel[:120], "published_at": "",
                    "thumbnail_url": ("https://i.ytimg.com/vi/%s/mqdefault.jpg"
                                      % video_id)})
            for child in reversed(list(node.values())):
                if isinstance(child, (dict, list)):
                    stack.append(child)
        elif isinstance(node, list):
            for child in reversed(node):
                if isinstance(child, (dict, list)):
                    stack.append(child)
    if not results:
        raise SearchError("Public YouTube page did not return usable videos.")
    return results, continuation


def parse_public_home(html_text):
    """Compatibility: return only real video cards from a public page."""
    return _public_results(_initial_data(html_text))[0]


def _web_config(html_text):
    """Read YouTube's *public webpage* client metadata, never a user's key.

    Some page variants HTML-escape quotes or escape their config inside a
    script. Only accept tightly validated fields from the returned page.
    """
    candidates = (html_text, html.unescape(html_text),
                  html_text.replace('\\\\"', '"'))
    def field(pattern):
        for candidate in candidates:
            match = pattern.search(candidate)
            if match:
                return match.group(1)
        return ""
    return {"key": field(WEB_KEY), "version": field(WEB_VERSION),
            "visitor": field(WEB_VISITOR)}


def _pack_continuation(token, config, endpoint="search", category_id="", discovery_stage=0):
    if (category_id not in PUBLIC_QUERIES or type(discovery_stage) is not int
            or not -1 <= discovery_stage < DISCOVERY_STAGE_LIMIT
            or endpoint not in ("search", "browse") or not token
            or not config.get("key") or not config.get("version")):
        return ""
    packed = json.dumps({"continuation": token, "endpoint": endpoint,
                         "key": config["key"],
                         "version": config["version"],
                         "category": category_id,
                         "stage": discovery_stage,
                         "visitor": config.get("visitor", "")},
                        separators=(",", ":"))
    return packed if len(packed) <= MAX_PAGE_TOKEN else ""


def _unpack_continuation(value):
    if not isinstance(value, str) or not 0 < len(value) <= MAX_PAGE_TOKEN:
        raise SearchError("Invalid public video page.")
    try:
        info = json.loads(value)
    except ValueError:
        raise SearchError("Invalid public video page.") from None
    if not isinstance(info, dict):
        raise SearchError("Invalid public video page.")
    token, key, version = (info.get("continuation"),
                           info.get("key"), info.get("version"))
    visitor = info.get("visitor", "")
    endpoint = info.get("endpoint", "search")
    category_id = info.get("category", "")
    stage = info.get("stage", 0)
    if (category_id not in PUBLIC_QUERIES or type(stage) is not int
            or not -1 <= stage < DISCOVERY_STAGE_LIMIT
            or endpoint not in ("search", "browse")
            or not isinstance(token, str) or not 0 < len(token) <= 3000
            or any(ord(ch) < 33 or ord(ch) > 126 for ch in token)
            or not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_-]{12,80}", key)
            or not isinstance(version, str) or not re.fullmatch(r"[A-Za-z0-9._-]{4,80}", version)
            or not isinstance(visitor, str) or len(visitor) > 300
            or not re.fullmatch(r"[A-Za-z0-9_%=-]*", visitor)):
        raise SearchError("Invalid public video page.")
    return info


def _continuation_page(page_token, opener, timeout):
    info = _unpack_continuation(page_token)
    base = (BROWSE_CONTINUATION_URL if info["endpoint"] == "browse"
            else CONTINUATION_URL)
    url = base + urlencode({"prettyPrint": "false", "key": info["key"]})
    payload = {"context": {"client": {
        "clientName": "WEB", "clientVersion": info["version"],
        "hl": "sk", "gl": "SK"}},
        "continuation": info["continuation"]}
    headers = {"User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                              "AppleWebKit/537.36 Chrome/130.0 Safari/537.36"),
               "Content-Type": "application/json", "Accept": "application/json",
               "Origin": "https://www.youtube.com"}
    if info["visitor"]:
        headers["X-Goog-Visitor-Id"] = info["visitor"]
    req = Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    try:
        response = opener(req, timeout=timeout)
        try:
            final = response.geturl() if hasattr(response, "geturl") else url
            if not isinstance(final, str) or not final.startswith(
                    ("https://www.youtube.com/youtubei/", "https://youtube.com/youtubei/")):
                raise SearchError("Public video page redirected elsewhere.")
            raw = response.read(PUBLIC_MAX_HTML + 1)
        finally:
            response.close()
    except (HTTPError, URLError, OSError):
        raise SearchError("More public YouTube videos are unavailable.") from None
    if len(raw) > PUBLIC_MAX_HTML:
        raise SearchError("Public YouTube response is too large.")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError):
        raise SearchError("Public YouTube returned invalid page data.") from None
    videos, continuation = _public_results(data)
    next_token = _pack_continuation(continuation, info, info["endpoint"],
                                    info["category"], info["stage"])
    if not next_token or continuation == info["continuation"]:
        next_token = _discovery_cursor(info["category"], info["stage"] + 1)
    return {"items": videos, "next_page_token": next_token,
            "total_results": None}


# Search pages normally contain public results even when an unsigned Home page
# has no recommended feed. These are search topics, not a personalized chart.
PUBLIC_QUERIES = {
    "0": "Slovensko videá",
    "1": "film animácia", "10": "hudba music",
    "15": "zvieratá", "17": "šport", "19": "cestovanie",
    "20": "gaming hry", "22": "ľudia vlog", "23": "komédia",
    "24": "zábava", "25": "správy Slovensko", "26": "návody životný štýl",
    "27": "vzdelávanie", "28": "technológie",
}
PUBLIC_SEARCH_URL = "https://www.youtube.com/results?"

# Related public topic searches are a fallback when unsigned YouTube search/Home
# does not expose a continuation. These are real results, not a fabricated page
# token or a personalized recommendation. Use bounded server requests.
PUBLIC_DISCOVERY_TERMS = (
    "", "novinky", "najnovšie", "2026", "slovensky", "zaujímavosti",
    "reportáž", "dokument", "najlepšie", "rozhovor", "prehľad",
    "video", "2025", "2024", "krátke videá", "populárne",
    "slovensko", "vysvetlenie", "ukážky", "top", "inšpirácia",
    "dnes", "zaujímavé", "nové", "trendy", "2023", "archív",
    "výber", "tipy", "príbeh", "témy", "recenzia"
)
DISCOVERY_STAGE_LIMIT = len(PUBLIC_DISCOVERY_TERMS)


def _discovery_cursor(category_id, stage):
    if (category_id not in PUBLIC_QUERIES or not isinstance(stage, int)
            or stage < 0 or stage >= DISCOVERY_STAGE_LIMIT):
        return ""
    return json.dumps({"kind": "public_discovery",
                       "category": category_id, "stage": stage},
                      separators=(",", ":"))


def _discovery_request(category_id, stage, opener, timeout):
    if category_id not in PUBLIC_QUERIES or not 0 <= stage < DISCOVERY_STAGE_LIMIT:
        raise SearchError("No more public discovery searches in this category.")
    base = PUBLIC_QUERIES[category_id]
    suffix = PUBLIC_DISCOVERY_TERMS[stage]
    query = (base + " " + suffix).strip()
    url = PUBLIC_SEARCH_URL + urlencode({"search_query": query,
                                         "hl": "sk", "gl": "SK"})
    page = _read_public_page(url, opener, timeout, as_page=True,
                             endpoint="search", category_id=category_id,
                             discovery_stage=stage)
    return page



def _read_public_page(url, opener, timeout, as_page=False,
                      endpoint="search", category_id="", discovery_stage=0):
    request = Request(url, headers={
        "User-Agent": ("Mozilla/5.0 (X11; Linux x86_64) "
                       "AppleWebKit/537.36 Chrome/130.0 Safari/537.36"),
        "Accept-Language": "sk-SK,sk;q=0.9,en;q=0.5",
        "Accept": "text/html",
    })
    try:
        response = opener(request, timeout=timeout)
        try:
            final_url = response.geturl() if hasattr(response, "geturl") else url
            if not isinstance(final_url, str) or not final_url.startswith(
                ("https://www.youtube.com/", "https://youtube.com/")
            ):
                raise SearchError("Public YouTube page redirected elsewhere.")
            body = response.read(PUBLIC_MAX_HTML + 1)
        finally:
            response.close()
    except (HTTPError, URLError, OSError):
        raise SearchError("Public YouTube page is temporarily unavailable.") from None
    if len(body) > PUBLIC_MAX_HTML:
        raise SearchError("Public YouTube response is too large.")
    content = body.decode("utf-8", "replace")
    if not as_page:
        return parse_public_home(content)
    videos, continuation = _public_results(_initial_data(content))
    config = _web_config(content)
    cursor = _pack_continuation(continuation, config, endpoint,
                                category_id, discovery_stage)
    if not cursor:
        cursor = _discovery_cursor(category_id, discovery_stage + 1)
    return {"items": videos, "next_page_token": cursor,
            "total_results": None,
            "pagination_state": ("ready" if cursor else
                                 "missing_continuation" if not continuation else
                                 "missing_web_client")}



def public_category_videos(category_id="0", opener=urlopen, timeout=8):
    """Real, anonymous YouTube video cards, no account or Data API key.

    For All, attempt the unsigned Home once; its recommendation rail is often
    empty for new/anonymous sessions, so fall back to an actual search page.
    Category chips use public topic searches, NOT the official popularity chart.
    Every request remains size-bounded and runs in the calling worker thread.
    """
    if category_id not in PUBLIC_QUERIES:
        raise SearchError("Unsupported public YouTube category.")
    if category_id == "0":
        try:
            return _read_public_page(PUBLIC_HOME_URL, opener, timeout)
        except SearchError:
            pass
    search = urlencode({"search_query": PUBLIC_QUERIES[category_id],
                        "hl": "sk", "gl": "SK"})
    return _read_public_page(PUBLIC_SEARCH_URL + search, opener, timeout)


def public_category_page(category_id="0", page_token="", opener=urlopen, timeout=8):
    """Fetch an actual public page; continue only with YouTube's real cursor."""
    if category_id not in PUBLIC_QUERIES:
        raise SearchError("Unsupported public YouTube category.")
    if page_token:
        try:
            info = json.loads(page_token)
        except (ValueError, TypeError):
            raise SearchError("Invalid public video page.") from None
        if isinstance(info, dict) and info.get("kind") == "public_discovery":
            if info.get("category") != category_id or type(info.get("stage")) is not int:
                raise SearchError("Invalid public video page.")
            return _discovery_request(category_id, info["stage"], opener, timeout)
        if not isinstance(info, dict) or info.get("category") != category_id:
            raise SearchError("Invalid public video page.")
        # The anonymous YouTube webpage may advertise a continuation but
        # reject it on another request (client/visitor/session mismatch).
        # Fall back only for a structurally valid category-bound token.
        verified = _unpack_continuation(page_token)
        try:
            return _continuation_page(page_token, opener, timeout)
        except SearchError:
            next_stage = verified["stage"] + 1
            if 0 <= next_stage < DISCOVERY_STAGE_LIMIT:
                return _discovery_request(category_id, next_stage, opener, timeout)
            raise
    if category_id == "0":
        try:
            return _read_public_page(PUBLIC_HOME_URL, opener, timeout, as_page=True,
                                     endpoint="browse", category_id=category_id,
                                     discovery_stage=-1)
        except SearchError:
            pass
    search = urlencode({"search_query": PUBLIC_QUERIES[category_id],
                        "hl": "sk", "gl": "SK"})
    return _read_public_page(PUBLIC_SEARCH_URL + search, opener, timeout,
                             as_page=True, category_id=category_id,
                             discovery_stage=0)


def public_home_videos(opener=urlopen, timeout=8):
    """Backward-compatible anonymous Home worker entrypoint."""
    return public_category_videos("0", opener=opener, timeout=timeout)
