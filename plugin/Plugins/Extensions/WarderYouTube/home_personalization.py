"""Dynamic topical Home chips from real YouTube subscription interests.

Subscriptions, individual channel links, History and Favourites already have
separate main-menu entries and MUST NOT appear in the Home filter row.
Only truthful topic labels inferred from actual subscribed channel names
are exposed. No unsupported web Mixes or fake recommendations.
"""

import re
import unicodedata

VISIBLE_CHIPS = 7
MAX_TOPIC_CHIPS = 8

TOPICS = (
    ("build", "Stavba", ("drevostav", "stavba", "stavebn", "construction",
                         "carpenter", "stolar", "woodwork", "tesar")),
    ("cars", "Autá", ("auto", "automobil", "garaz", "mechanic", "motor",
                      "car repair", "moto", "vehicle", "maranello")),
    ("workshop", "Dielňa", ("oprav", "dielna", "repair", "workshop",
                            "naradie", "tools", "kutil", "diy")),
    ("music", "Hudba", ("hudba", "music", "muzik", "radio", "pesne", "songs", "records", "dj")),
    ("gaming", "Hry", ("gaming", "games", "gameplay", "minecraft", "fortnite", "hranie")),
    ("audio", "Audioknihy", ("audioknih", "audiobook", "poviedky", "spoken word")),
    ("nature", "Príroda", ("priroda", "nature", "wildlife", "animals", "zvierata")),
    ("sport", "Šport", ("sport", "futbal", "football", "hokej", "hockey", "fitness")),
    ("travel", "Cestovanie", ("cestov", "travel", "trip", "dovolen", "exploring")),
    ("tech", "Technika", ("technolog", "science", "hardware", "tech", "linux", "pc build")),
    ("news", "Správy", ("spravy", "news", "aktuality", "report", "televizia")),
)


def _normal(text):
    value = unicodedata.normalize("NFKD", str(text or ""))
    return "".join(ch for ch in value if not unicodedata.combining(ch)).lower()


def build_home_chips(channels=(), authenticated=False):
    """Create Home filter chips only for topics backed by real subscriptions.

    No duplicates of main-menu Odbery, Obľúbené, História and no individual
    channel titles. There is always a useful Všetko entry. A disconnected
    user has no account-derived filters; nothing is invented.
    """
    chips = [{"kind": "all", "id": "all", "label": "Všetko",
              "title": "Populárne na Slovensku"}]
    if not authenticated:
        return chips
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
    for topic_id, label, words in TOPICS:
        matches = [cid for cid, name in safe
                   if any(word in _normal(name) for word in words)]
        if matches:
            chips.append({"kind": "topic", "id": "topic:" + topic_id,
                          "label": label, "title": label,
                          "channels": tuple(matches[:8])})
            if len(chips) > MAX_TOPIC_CHIPS:
                break
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
