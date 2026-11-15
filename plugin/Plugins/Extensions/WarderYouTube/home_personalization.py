# -*- coding: utf-8 -*-
"""General YouTube Home categories, without guessed account interests.

One fixed Všetko + six rotating official categories. All Home chip labels are
standard YouTube categories, never claimed to match the personalized web site.
"""
import re
from .home_categories import rotating_categories

VISIBLE_CHIPS = 7


def build_home_chips(day=None, **unused):
    result = []
    for category_id, label in rotating_categories(day):
        is_all = category_id == "0"
        result.append({
            "kind": "all" if is_all else "general",
            "id": "category:" + category_id,
            "category_id": category_id,
            "label": label,
            "title": "Popular in Slovakia" if is_all else label,
        })
    return result


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
