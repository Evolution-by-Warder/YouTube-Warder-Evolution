# -*- coding: utf-8 -*-
"""Truthful, account-derived Home chips; never impersonate YouTube web Mixes.

Chips are based on local receiver History/Favourites and the actual channels
returned by the user's read-only YouTube subscriptions. Topic chips appear
only if real subscribed channel names support the topic. Each chip therefore
has a real, resolvable content source. No account tokens are stored here.
"""
import re
import unicodedata

VISIBLE_CHIPS = 7
MAX_CHANNEL_CHIPS = 12
MAX_TOPIC_CHIPS = 5

# Conservative keyword matches, from actual channel names only; none are
# presented as Google's personal recommendations.
TOPICS = (
    ("music", "Hudba", ("music", "muzik", "hudba", "radio", "dj", "records", "songs", "pesn")),
    ("games", "Hry", ("gaming", "gameplay", "games", "minecraft", "fortnite", "hranie", "hrac")),
    ("audio", "Audioknihy", ("audioknih", "audiobook", "spoken word", "poviedky")),
    ("nature", "Príroda", ("priroda", "nature", "wildlife", "zvierat", "animals", "forest")),
    ("sports", "Šport", ("sport", "football", "futbal", "hockey", "hokej", "fitness")),
    ("tech", "Technika", ("tech", "technolog", "ved", "science", "hardware", "pc build", "linux")),
    ("news", "Správy", ("news", "sprav", "aktualit", "report", "televizia")),
)


def _normalized(text):
    value = unicodedata.normalize("NFKD", str(text or ""))
    return "".join(ch for ch in value if not unicodedata.combining(ch)).lower()


def _matches(name, words):
    normalized = _normalized(name)
    return any(word in normalized for word in words)


def _short_name(value):
    value = " ".join(str(value or "").split())
    return value if len(value) <= 17 else value[:16].rstrip() + "…"


def build_home_chips(channels=(), history=(), favourites=(), account=False):
    """Dynamic chips with explicit backing sources, stable IDs and no fakes.

    The largest visible source list comes from actual subscriptions; the
    horizontal viewport displays seven chips at a time and scrolls on arrows.
    """
    result = [{"kind": "all", "id": "all", "label": "Všetko", "title": "Všetko"}]
    safe_channels, seen = [], set()
    for channel in channels:
        if not isinstance(channel, dict):
            continue
        channel_id = channel.get("channel_id")
        title = " ".join(str(channel.get("title") or "").split())
        if (not isinstance(channel_id, str) or not re.fullmatch(
                r"UC[A-Za-z0-9_-]{22}", channel_id)
                or not title or channel_id in seen):
            continue
        seen.add(channel_id)
        safe_channels.append((channel_id, title[:160]))
    if account and safe_channels:
        result.append({"kind": "recent", "id": "recent", "label": "Nové z odberov",
                       "title": "Najnovšie videá z odberov"})
    if history:
        result.append({"kind": "history", "id": "history", "label": "Pozreté",
                       "title": "Naposledy prehrané videá"})
    if favourites:
        result.append({"kind": "favourites", "id": "favourites", "label": "Obľúbené",
                       "title": "Uložené videá"})
    for key, title, words in TOPICS:
        matched = [channel_id for channel_id, channel_name in safe_channels
                   if _matches(channel_name, words)]
        if matched:
            result.append({"kind": "topic", "id": "topic:" + key, "label": title,
                           "title": title, "channels": tuple(matched[:12])})
            if sum(item["kind"] == "topic" for item in result) >= MAX_TOPIC_CHIPS:
                break

    # Watching affinity selects which subscribed channels to expose first.
    watched = {_normalized(item.get("channel")) for item in history
               if isinstance(item, dict) and item.get("channel")}
    ordered = sorted(enumerate(safe_channels),
                     key=lambda item: (0 if _normalized(item[1][1]) in watched else 1,
                                       item[0]))
    for _, (channel_id, title) in ordered[:MAX_CHANNEL_CHIPS]:
        result.append({"kind": "channel", "id": "channel:" + channel_id,
                       "label": _short_name(title), "title": title,
                       "channels": (channel_id,)})
    return result


def dedupe_videos(items, limit=96):
    """Only unique genuine YouTube video records may appear in a tile feed."""
    result, seen = [], set()
    for item in items:
        if not isinstance(item, dict):
            continue
        identifier = item.get("video_id")
        if not isinstance(identifier, str) or not re.fullmatch(
                r"[A-Za-z0-9_-]{11}", identifier) or identifier in seen:
            continue
        seen.add(identifier)
        result.append(item)
        if len(result) >= limit:
            break
    return result
