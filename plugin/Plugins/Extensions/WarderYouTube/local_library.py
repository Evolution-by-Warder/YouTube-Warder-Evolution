# -*- coding: utf-8 -*-
"""Bounded, local-only video favourites and recently opened video list.

Keeps no signed playback URLs, API keys, credentials or video files. Storage
is independent from the Enigma2 global settings and survives plugin updates.
"""
import json
import os
import re
import tempfile
from pathlib import Path
from threading import Lock

LIBRARY_PATH = Path("/etc/enigma2/warderyoutube-library.json")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
MAX_FILE_BYTES = 160 * 1024
LIMITS = {"favourites": 200, "history": 100}
_LOCK = Lock()


class LibraryError(Exception):
    """UI-safe local storage error."""


def _video(video):
    if not isinstance(video, dict):
        raise LibraryError("Neplatné údaje videa.")
    video_id = video.get("video_id")
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise LibraryError("Neplatný identifikátor videa.")
    title = video.get("title")
    channel = video.get("channel")
    published = video.get("published_at")
    return {
        "video_id": video_id,
        "title": (title if isinstance(title, str) else "YouTube video").strip()[:200],
        "channel": (channel if isinstance(channel, str) else "").strip()[:120],
        "published_at": (published if isinstance(published, str) else "")[:30],
        # Recreate from the validated ID. Never persist untrusted thumbnail URLs.
        "thumbnail_url": "https://i.ytimg.com/vi/%s/mqdefault.jpg" % video_id,
    }


def _read(path):
    if not path.exists():
        return {"schema": 1, "favourites": [], "history": []}
    try:
        with path.open("rb") as handle:
            raw = handle.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            raise LibraryError("Uložený zoznam videí je príliš veľký.")
        saved = json.loads(raw.decode("utf-8"))
        if (not isinstance(saved, dict) or type(saved.get("schema")) is not int
                or saved["schema"] != 1):
            raise LibraryError("Neplatný formát uložených videí.")
        result = {"schema": 1}
        for kind, limit in LIMITS.items():
            items = saved.get(kind)
            if not isinstance(items, list) or len(items) > limit:
                raise LibraryError("Neplatný obsah uložených videí.")
            seen = set()
            clean = []
            for item in items:
                normalized = _video(item)
                video_id = normalized["video_id"]
                if video_id in seen:
                    raise LibraryError("Duplicitné uložené video.")
                seen.add(video_id)
                clean.append(normalized)
            result[kind] = clean
        return result
    except LibraryError:
        raise
    except (ValueError, UnicodeError, OSError, TypeError):
        # Never silently overwrite a broken file with an empty library.
        raise LibraryError("Uložené videá sa nepodarilo načítať.") from None


def _write(path, data):
    payload = (json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    if len(payload) > MAX_FILE_BYTES:
        raise LibraryError("Zoznam videí je príliš veľký.")
    temp = None
    try:
        # Same-filesystem write + atomic replace; avoid torn JSON on power loss.
        with tempfile.NamedTemporaryFile(
                prefix=".warder-youtube-", suffix=".tmp",
                dir=str(path.parent), delete=False) as handle:
            temp = Path(handle.name)
            os.chmod(handle.name, 0o600)
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(str(temp), str(path))
    except OSError:
        raise LibraryError("Videá sa nepodarilo bezpečne uložiť.") from None
    finally:
        if temp is not None:
            try:
                temp.unlink()
            except OSError:
                pass


def list_videos(kind, path=LIBRARY_PATH):
    if kind not in LIMITS:
        raise LibraryError("Neznámy zoznam videí.")
    with _LOCK:
        return list(_read(Path(path))[kind])


def toggle_favourite(video, path=LIBRARY_PATH):
    """Return True when saved, False when removed."""
    item = _video(video)
    with _LOCK:
        path = Path(path)
        saved = _read(path)
        records = saved["favourites"]
        old_count = len(records)
        records[:] = [x for x in records if x["video_id"] != item["video_id"]]
        added = len(records) == old_count
        if added:
            records.insert(0, item)
            del records[LIMITS["favourites"]:]
        _write(path, saved)
        return added


def record_opened(video, path=LIBRARY_PATH):
    """Record only after the native player was opened, not on failed resolve."""
    item = _video(video)
    with _LOCK:
        path = Path(path)
        saved = _read(path)
        items = saved["history"]
        items[:] = [x for x in items if x["video_id"] != item["video_id"]]
        items.insert(0, item)
        del items[LIMITS["history"]:]
        _write(path, saved)


def remove_video(kind, video_id, path=LIBRARY_PATH):
    if kind not in LIMITS or not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise LibraryError("Neplatná položka videa.")
    with _LOCK:
        path = Path(path)
        saved = _read(path)
        items = saved[kind]
        old_count = len(items)
        items[:] = [x for x in items if x["video_id"] != video_id]
        if len(items) != old_count:
            _write(path, saved)
            return True
        return False


def clear_videos(kind, path=LIBRARY_PATH):
    if kind not in LIMITS:
        raise LibraryError("Neznámy zoznam videí.")
    with _LOCK:
        path = Path(path)
        saved = _read(path)
        saved[kind] = []
        _write(path, saved)
