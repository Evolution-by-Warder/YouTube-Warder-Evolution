# -*- coding: utf-8 -*-
"""Read-only YouTube subscriptions and recent uploads via official Data API.

No API key or account ID is accepted from user-visible URLs. Bearer tokens
travel only in HTTP headers, never in query strings. Blocking: call in worker.
"""
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

BASE = "https://www.googleapis.com/youtube/v3/"
MAX_RESPONSE_BYTES = 512 * 1024
CHANNEL_ID = re.compile(r"^UC[A-Za-z0-9_-]{22}$")
PLAYLIST_ID = re.compile(r"^[A-Za-z0-9_-]{10,64}$")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
MAX_CHANNEL_PAGES = 4
MAX_RECENT_CHANNELS = 16
MAX_RECENT_VIDEOS = 24


class SubscriptionsApiError(Exception):
    """Safe UI messages only; never include bearer tokens or network URLs."""


def _get(resource, params, token, opener=urlopen):
    if not isinstance(token, str) or not token or len(token) > 8192:
        raise SubscriptionsApiError("Connect your YouTube account first.")
    request = Request(BASE + resource + "?" + urlencode(params), headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
        "User-Agent": "WarderYouTube/0.0.8",
    })
    try:
        response = opener(request, timeout=8)
        try:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        finally:
            response.close()
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise SubscriptionsApiError("YouTube account access expired or is not permitted.")
        raise SubscriptionsApiError("YouTube subscriptions are temporarily unavailable.")
    except (URLError, OSError, TimeoutError):
        raise SubscriptionsApiError("Cannot reach YouTube subscriptions.")
    if len(raw) > MAX_RESPONSE_BYTES:
        raise SubscriptionsApiError("YouTube subscriptions response is too large.")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError):
        raise SubscriptionsApiError("YouTube returned invalid subscription data.")
    if not isinstance(data, dict) or not isinstance(data.get("items"), list):
        raise SubscriptionsApiError("YouTube returned invalid subscription data.")
    return data


def parse_subscriptions(data):
    items = []
    for item in data.get("items", []):
        if not isinstance(item, dict):
            continue
        snippet = item.get("snippet") or {}
        resource = snippet.get("resourceId") or {}
        channel = resource.get("channelId")
        if not isinstance(channel, str) or not CHANNEL_ID.fullmatch(channel):
            continue
        title = html.unescape(str(snippet.get("title") or "YouTube channel")).strip()[:160]
        thumbnails = snippet.get("thumbnails") or {}
        avatar = ""
        if isinstance(thumbnails, dict):
            for size in ("medium", "high", "default"):
                entry = thumbnails.get(size) or {}
                url = entry.get("url") if isinstance(entry, dict) else ""
                if not isinstance(url, str) or len(url) > 2048:
                    continue
                try:
                    parts = urlsplit(url)
                    if (parts.scheme == "https"
                            and parts.hostname in ("yt3.ggpht.com", "yt3.googleusercontent.com")
                            and parts.port in (None, 443)
                            and not parts.username and not parts.password
                            and parts.path.startswith("/") and len(parts.path) >= 5):
                        avatar = url
                        break
                except ValueError:
                    continue
        items.append({"channel_id": channel, "title": title,
                      "thumbnail_url": avatar,
                      "published_at": str(snippet.get("publishedAt") or "")[:32]})
    return items


def subscriptions_list(access_token, opener=urlopen, limit=160):
    """Load up to 4 pages (200 entries), never silently claim all beyond cap."""
    limit = max(1, min(int(limit), 200))
    found, seen = [], set()
    page = ""
    for _ in range(MAX_CHANNEL_PAGES):
        params = {"part": "snippet,contentDetails", "mine": "true",
                  "maxResults": 50, "order": "alphabetical"}
        if page:
            params["pageToken"] = page
        result = _get("subscriptions", params, access_token, opener)
        for subscription in parse_subscriptions(result):
            if subscription["channel_id"] in seen:
                continue
            seen.add(subscription["channel_id"])
            found.append(subscription)
            if len(found) >= limit:
                return found
        page = result.get("nextPageToken") or ""
        if not page or not isinstance(page, str) or len(page) > 150:
            break
    return found


def uploads_playlists(channel_ids, access_token, opener=urlopen):
    playlist_ids = {}
    ids = [c for c in channel_ids if isinstance(c, str) and CHANNEL_ID.fullmatch(c)]
    for start in range(0, len(ids), 50):
        data = _get("channels", {"part": "contentDetails", "id": ",".join(ids[start:start+50]),
                                 "maxResults": 50}, access_token, opener)
        for channel in data["items"]:
            if not isinstance(channel, dict):
                continue
            identifier = channel.get("id")
            upload_id = ((channel.get("contentDetails") or {}).get("relatedPlaylists") or {}).get("uploads")
            if (identifier in ids and isinstance(upload_id, str)
                    and PLAYLIST_ID.fullmatch(upload_id)):
                playlist_ids[identifier] = upload_id
    return playlist_ids


def playlist_videos(playlist_id, access_token, opener=urlopen, limit=12):
    if not isinstance(playlist_id, str) or not PLAYLIST_ID.fullmatch(playlist_id):
        raise SubscriptionsApiError("YouTube channel uploads are unavailable.")
    params = {"part": "snippet,contentDetails", "playlistId": playlist_id,
              "maxResults": max(1, min(int(limit), 50))}
    data = _get("playlistItems", params, access_token, opener)
    result = []
    for item in data["items"]:
        if not isinstance(item, dict):
            continue
        snippet = item.get("snippet") or {}
        details = item.get("contentDetails") or {}
        resource = snippet.get("resourceId") or {}
        video_id = details.get("videoId") or resource.get("videoId")
        if (not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id)
                or snippet.get("title") in ("Private video", "Deleted video")):
            continue
        result.append({
            "video_id": video_id,
            "title": html.unescape(str(snippet.get("title") or "YouTube video"))[:200],
            "channel": html.unescape(str(snippet.get("videoOwnerChannelTitle")
                                         or snippet.get("channelTitle") or ""))[:120],
            "published_at": str(details.get("videoPublishedAt")
                                or snippet.get("publishedAt") or "")[:32],
            "thumbnail_url": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id,
        })
    return result


def recent_subscription_videos(access_token, opener=urlopen,
                               channel_limit=MAX_RECENT_CHANNELS):
    """Bounded sample of the user's channels, not a claim of all YouTube uploads.

    This cap avoids issuing hundreds of YouTube Data API requests on receivers.
    The UI must label the partial scope, and expose 'All subscriptions' separately.
    """
    channels = subscriptions_list(access_token, opener=opener, limit=160)
    if not channels:
        return [], channels
    limit = max(1, min(int(channel_limit), MAX_RECENT_CHANNELS))
    sample = channels[:limit]
    mappings = uploads_playlists([c["channel_id"] for c in sample],
                                 access_token, opener=opener)
    videos, seen = [], set()
    for channel in sample:
        playlist_id = mappings.get(channel["channel_id"])
        if not playlist_id:
            continue
        try:
            latest = playlist_videos(playlist_id, access_token, opener=opener, limit=3)
        except SubscriptionsApiError:
            continue
        for video in latest:
            if video["video_id"] in seen:
                continue
            seen.add(video["video_id"])
            if not video["channel"]:
                video["channel"] = channel["title"]
            videos.append(video)
    videos.sort(key=lambda item: (item["published_at"], item["video_id"]), reverse=True)
    return videos[:MAX_RECENT_VIDEOS], channels
