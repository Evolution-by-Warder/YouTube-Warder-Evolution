# -*- coding: utf-8 -*-
"""Real signed-in YouTube Home filters, never inferred from subscriptions.

YouTube Data API has no endpoint for the personalized Home chip rail. This
read-only, best-effort Innertube browse request uses the user's existing OAuth
token, runs only in a background worker and fails closed if signed-in data
cannot be verified. YouTube may change this undocumented format at any time.
"""
import hashlib
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .api import SearchError, VIDEO_ID

BROWSE_URL = "https://www.youtube.com/youtubei/v1/browse?prettyPrint=false"
CLIENT_VERSION = "2.20260114.08.00"
MAX_BYTES = 4 * 1024 * 1024
MAX_CHIPS = 48
MAX_VIDEOS = 96


def _text(node):
    if isinstance(node, str):
        return html.unescape(node)
    if not isinstance(node, dict):
        return ""
    if isinstance(node.get("simpleText"), str):
        return html.unescape(node["simpleText"])
    if isinstance(node.get("content"), str):
        return html.unescape(node["content"])
    if isinstance(node.get("runs"), list):
        return html.unescape("".join(
            str(run.get("text") or "") for run in node["runs"]
            if isinstance(run, dict)))
    if isinstance(node.get("text"), (dict, str)):
        return _text(node["text"])
    return ""


def _walk(root, max_nodes=16000):
    stack, visited = [root], 0
    while stack and visited < max_nodes:
        node = stack.pop()
        visited += 1
        if isinstance(node, dict):
            yield node
            stack.extend(reversed([
                v for v in node.values() if isinstance(v, (list, dict))
            ]))
        elif isinstance(node, list):
            stack.extend(reversed([
                v for v in node if isinstance(v, (list, dict))
            ]))


def _authenticated(payload):
    context = payload.get("responseContext") or {}
    if not isinstance(context, dict):
        return False
    main = context.get("mainAppWebResponseContext") or {}
    if isinstance(main, dict) and main.get("loggedOut") is False:
        return True
    for group in context.get("serviceTrackingParams") or []:
        if not isinstance(group, dict):
            continue
        for item in group.get("params") or []:
            if (isinstance(item, dict) and item.get("key") == "logged_in"
                    and item.get("value") in ("1", "true")):
                return True
    return False


def _command(node):
    """Use only server-provided navigation commands, never guessed searches."""
    if not isinstance(node, dict):
        return None
    for key in ("navigationEndpoint", "serviceEndpoint", "tapCommand", "onTap"):
        if isinstance(node.get(key), dict):
            found = _command(node[key])
            if found:
                return found
    for key in ("innertubeCommand", "command", "commandExecutorCommand"):
        if isinstance(node.get(key), dict):
            found = _command(node[key])
            if found:
                return found
    for value in node.get("commands") or []:
        if isinstance(value, dict):
            found = _command(value)
            if found:
                return found
    direct = node.get("continuationCommand") or {}
    if isinstance(direct, dict):
        token = direct.get("token")
        if isinstance(token, str) and 0 < len(token) <= 8192:
            return {"continuation": token}
    browse = node.get("browseEndpoint") or {}
    if isinstance(browse, dict):
        params = browse.get("params")
        browse_id = browse.get("browseId")
        if (isinstance(params, str) and 0 < len(params) <= 8192
                and browse_id in ("FEwhat_to_watch", None)):
            return {"params": params}
    return None


def _filter_rows(payload):
    """Find actual chip bar, ignoring chips nested elsewhere on the page."""
    for node in _walk(payload):
        for key in ("feedFilterChipBarRenderer", "chipCloudRenderer",
                    "feedFilterChipBarViewModel"):
            bar = node.get(key)
            if isinstance(bar, dict):
                items = bar.get("contents") or bar.get("chips") or []
                if isinstance(items, list) and items:
                    yield items


def parse_live_home(payload):
    """Return exact, ordered Home chips with their actual YouTube commands."""
    if not isinstance(payload, dict) or not _authenticated(payload):
        raise SearchError("Could not verify signed-in YouTube Home filters.")
    chips = []
    for entries in _filter_rows(payload):
        for entry in entries[:MAX_CHIPS]:
            if not isinstance(entry, dict):
                continue
            raw = (entry.get("chipCloudChipRenderer")
                   or entry.get("chipViewModel") or entry.get("chipView")
                   or entry)
            if not isinstance(raw, dict):
                continue
            label = " ".join(_text(raw.get("text") or raw.get("title") or "").split())
            if not label or len(label) > 120:
                continue
            selected = raw.get("isSelected") is True or raw.get("selected") is True
            command = _command(raw)
            if not selected and not command:
                continue
            marker = label + "\0" + json.dumps(command, sort_keys=True)
            chip = {
                "id": "yt:" + hashlib.sha256(marker.encode("utf-8")).hexdigest()[:24],
                "kind": "live", "label": label, "title": label,
                "selected": selected,
            }
            if command:
                chip.update(command)
            if chip["id"] not in {c["id"] for c in chips}:
                chips.append(chip)
        if chips:
            break
    if not chips:
        raise SearchError("YouTube did not provide usable Home category chips.")
    return {"chips": chips, "videos": parse_live_videos(payload)}


def parse_live_videos(payload):
    """Read only concrete video entries from a YouTube browse response."""
    if not isinstance(payload, dict) or payload.get("error"):
        raise SearchError("YouTube category response is invalid.")
    videos = []
    seen = set()
    for node in _walk(payload):
        data = (node.get("videoRenderer") or node.get("gridVideoRenderer")
                or node.get("compactVideoRenderer"))
        if isinstance(data, dict):
            video_id = data.get("videoId")
            title = _text(data.get("title"))
            channel = (_text(data.get("ownerText"))
                       or _text(data.get("longBylineText"))
                       or _text(data.get("shortBylineText")))
        else:
            model = node.get("lockupViewModel")
            if not isinstance(model, dict):
                continue
            video_id = model.get("contentId")
            meta = model.get("metadata") or {}
            meta = meta.get("lockupMetadataViewModel") or {}
            title = _text(meta.get("title"))
            channel = ""
        if (isinstance(video_id, str) and VIDEO_ID.fullmatch(video_id)
                and title and video_id not in seen):
            seen.add(video_id)
            videos.append({
                "video_id": video_id, "title": title[:200],
                "channel": channel[:120], "published_at": "",
                "thumbnail_url": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id,
            })
        if len(videos) >= MAX_VIDEOS:
            break
    return videos


def _browse(access_token, command=None, opener=urlopen, timeout=10):
    if not isinstance(access_token, str) or not 8 <= len(access_token) <= 8192:
        raise SearchError("Connect your YouTube account to load real categories.")
    client = {
        "clientName": "WEB", "clientVersion": CLIENT_VERSION,
        "hl": "sk", "gl": "SK",
    }
    body = {"context": {"client": client}, "browseId": "FEwhat_to_watch"}
    if command:
        if not isinstance(command, dict):
            raise SearchError("Invalid Home category command.")
        continuation = command.get("continuation")
        params = command.get("params")
        if isinstance(continuation, str) and 0 < len(continuation) <= 8192:
            body.pop("browseId")
            body["continuation"] = continuation
        elif isinstance(params, str) and 0 < len(params) <= 8192:
            body["params"] = params
        else:
            raise SearchError("YouTube category has no valid navigation command.")
    request = Request(
        BROWSE_URL,
        data=json.dumps(body, separators=(",", ":")).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-YouTube-Client-Name": "1",
            "X-YouTube-Client-Version": CLIENT_VERSION,
            "Origin": "https://www.youtube.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36",
        },
        method="POST",
    )
    try:
        response = opener(request, timeout=timeout)
        try:
            raw = response.read(MAX_BYTES + 1)
        finally:
            response.close()
        if len(raw) > MAX_BYTES:
            raise SearchError("YouTube category response is too large.")
        parsed = json.loads(raw.decode("utf-8"))
        if not isinstance(parsed, dict) or parsed.get("error"):
            raise SearchError("YouTube categories are unavailable.")
        return parsed
    except (HTTPError, URLError, OSError, UnicodeError, ValueError):
        # Never leak the Bearer token or response headers in error messages.
        raise SearchError("Could not load signed-in YouTube Home categories.")


def live_home(access_token, opener=urlopen):
    return parse_live_home(_browse(access_token, opener=opener))


def live_category_videos(chip, access_token, opener=urlopen):
    if not isinstance(chip, dict) or chip.get("kind") != "live":
        raise SearchError("Invalid live YouTube category.")
    command = {key: chip[key] for key in ("continuation", "params") if key in chip}
    if not command:
        raise SearchError("The YouTube category cannot be opened.")
    return parse_live_videos(_browse(access_token, command, opener=opener))
