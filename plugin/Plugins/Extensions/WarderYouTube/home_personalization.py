# -*- coding: utf-8 -*-
"""Render only the real YouTube Home chips returned for the signed-in account.

Never infer topic labels from subscriptions. When YouTube's private Home
interface refuses the request, use a plainly labelled regional popular chart
instead of pretending that fabricated categories are personalized.
"""
import re

VISIBLE_CHIPS = 7
MAX_TOPIC_CHIPS = 48


def build_home_chips(chips=(), authenticated=False, **unused):
    """Honor YouTube's exact live labels and ordering, without translations."""
    result, seen = [], set()
    if authenticated and isinstance(chips, (list, tuple)):
        for raw in chips[:MAX_TOPIC_CHIPS]:
            if not isinstance(raw, dict) or raw.get("kind") != "live":
                continue
            identifier = raw.get("id")
            label = raw.get("label")
            if (not isinstance(identifier, str) or not identifier.startswith("yt:")
                    or not isinstance(label, str) or not label.strip()
                    or identifier in seen or len(label) > 120):
                continue
            command = {}
            for key in ("continuation", "params"):
                value = raw.get(key)
                if isinstance(value, str) and 0 < len(value) <= 8192:
                    command[key] = value
            if not command and not raw.get("selected"):
                continue
            entry = {"id": identifier, "kind": "live", "label": label,
                     "title": label, "selected": raw.get("selected") is True}
            entry.update(command)
            seen.add(identifier)
            result.append(entry)
    if result:
        return result
    # Clearly distinct regional fallback, NOT represented as a YouTube chip.
    return [{"kind": "all", "id": "all", "label": "Populárne SK",
             "title": "Populárne na Slovensku"}]


def dedupe_videos(items, limit=96):
    result, seen = [], set()
    for item in items:
        if not isinstance(item, dict):
            continue
        vid = item.get("video_id")
        if (not isinstance(vid, str)
                or not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid)
                or vid in seen):
            continue
        seen.add(vid)
        result.append(item)
        if len(result) >= limit:
            break
    return result
