# -*- coding: utf-8 -*-
"""Optional owner-managed API key file, independent of Enigma2 config saves.

Never print, log, or copy the key into a release package. A symlink, oversized,
multiline or world-readable file is deliberately ignored.
"""
import os
import re
import stat

API_KEY_FILE = "/etc/enigma2/warderyoutube_api.key"
VALID_KEY = re.compile(r"^[A-Za-z0-9_-]{20,160}$")
MAX_FILE_BYTES = 256


def read_manual_key(path=API_KEY_FILE):
    """Read a manually supplied key (mode 0600), or return empty on any issue."""
    try:
        info = os.lstat(path)
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
            return ""
        if info.st_size > MAX_FILE_BYTES:
            return ""
        # Reject symlinks, special devices and replaced large files.
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(path, flags), "rb") as stream:
            raw = stream.read(MAX_FILE_BYTES + 1)
        if len(raw) > MAX_FILE_BYTES:
            return ""
        value = raw.decode("ascii").strip()
        return value if VALID_KEY.fullmatch(value) else ""
    except (OSError, UnicodeError, ValueError):
        return ""
