# -*- coding: utf-8 -*-
"""Dynamic Home chips from actual subscribed YouTube channels.

No imitation of YouTube's private web recommendations or Mixes, and no
duplicate History/Favourites chips: these already live in the left menu.
Only matching real channels produce topical chips. Network I/O is handled
by the caller in a Twisted worker, not in the Enigma2 GUI.
"""
import re
import unicodedata

VISIBLE_CHIPS = 7
MAX_CHANNEL_CHIPS = 12
MAX_TOPIC_CHIPS = 5

TOPICS = (
    ("music", "Hudba", ("hudba", "music", "muzik", "radio", "pesne", "songs", "records", "dj")),
    ("gaming", "Hry", ("gaming", "games", "gameplay", "minecraft", "fortnite", "hranie")),
    ("audio", "Audioknihy", ("audioknih", "audiobook", "poviedky", "spoken word")),
    ("nature", "Príroda", ("priroda", "nature", "wildlife", "animals", "zvierata")),
    ("sport", "Šport", ("sport", "futbal", "football", "hokej", "hockey", "fitness")),
    ("tech", "Technika", ("technolog", "science", "hardware", "tech", "linux", "pc build")),
    ("news", "Správy", ("spravy", "news", "aktuality", "report", "televizia")),
)


def _normal(text):
    value = unicodedata.normalize("NFKD", str(text or ""))
    return "".join(ch for ch in value if not unicodedata.combining(ch)).lower()


def _short(text, limit=13):
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[:limit - 1].rstrip() + "…"


def build_home_chips(channels=(), authenticated=False):
    """Return stable IDs/labels backed only by available account resources.

    The list can be longer than seven; the Home UI exposes a sliding window
    of seven chip widgets. All records refer only to genuine channel IDs.
    """
    chips = [{"kind": "all", "id": "all", "label": "Všetko",
              "title": "Populárne na Slovensku"}]
    safe, seen = [], set()
    for raw in channels:
        if not isinstance(raw, dict):
            continue
        cid = raw.get("channel_id")
        title = " ".join(str(raw.get("title") or "").split())[:160]
        if (not isinstance(cid, str)
                or not re.fullmatch(r"UC[A-Za-z0-9_-]{22}", cid)
                or not title or cid in seen):
            continue
        safe.append((cid, title))
        seen.add(cid)
    if authenticated and safe:
        chips.append({"kind": "recent", "id": "recent",
                      "label": "Nové odbery", "title": "Nové videá z odberov"})

    topic_count = 0
    for topic_id, label, words in TOPICS:
        matches = [cid for cid, name in safe if any(w in _normal(name) for w in words)]
        if matches:
            chips.append({"kind": "topic", "id": "topic:" + topic_id,
                          "label": label, "title": label,
                          "channels": tuple(matches[:8])})
            topic_count += 1
            if topic_count >= MAX_TOPIC_CHIPS:
                break
    # Expose a bounded set of actual channels, not guessed personalized feeds.
    for cid, title in safe[:MAX_CHANNEL_CHIPS]:
        chips.append({"kind": "channel", "id": "channel:" + cid,
                      "label": _short(title), "title": title,
                      "channels": (cid,)})
    return chips


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
