# -*- coding: utf-8 -*-
"""Real per-user YouTube subscription rail in the Home right pane.

The left Odbery menu owns subscriptions; the Home category rail remains topics
only. This separate rail contains the latest-uploads feed and actual followed
channel names, with no fabricated topics, Mixes, or duplicated video lists.
"""
import re

MAX_CHANNELS = 160
MAX_LABEL_LENGTH = 21
CHANNEL_ID = re.compile(r"^UC[A-Za-z0-9_-]{22}$")


def subscription_chips(channels, connected=False):
    """Make horizontal chips from read-only Google subscriptions.list results."""
    if not connected:
        return []
    chips = [{
        "id": "latest",
        "kind": "recent",
        "label": "Najnovšie",
        "title": "Najnovšie z odberov (výber kanálov)",
    }]
    seen = set()
    for item in channels[:MAX_CHANNELS]:
        if not isinstance(item, dict):
            continue
        identifier = item.get("channel_id")
        title = " ".join(str(item.get("title") or "").split())[:160]
        if (not isinstance(identifier, str)
                or not CHANNEL_ID.fullmatch(identifier)
                or identifier in seen or not title):
            continue
        seen.add(identifier)
        label = (title if len(title) <= MAX_LABEL_LENGTH
                 else title[:MAX_LABEL_LENGTH - 1].rstrip() + "…")
        chips.append({
            "id": "channel:" + identifier,
            "kind": "channel",
            "label": label,
            "title": title,
            "channels": (identifier,),
        })
    return chips
