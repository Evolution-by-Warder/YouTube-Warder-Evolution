# -*- coding: utf-8 -*-
"""MenuList selection compatibility across OpenPLi and OpenATV images.

Enigma2 MenuList exposes getSelectionIndex() on many images; the underlying
native eListboxPythonMultiContent/eListboxContent exposes
getCurrentSelectionIndex().  getCurrentIndex() is not a portable MenuList API.
"""

def selected_index(menu):
    """Return selected zero-based index, or -1 if selection is unavailable."""
    for target, methods in (
        (menu, ("getSelectionIndex", "getCurrentIndex")),
        (getattr(menu, "l", None), ("getCurrentSelectionIndex",)),
        (getattr(menu, "instance", None), ("getCurrentIndex",)),
    ):
        if target is None:
            continue
        for name in methods:
            method = getattr(target, name, None)
            if not callable(method):
                continue
            try:
                result = method()
                if isinstance(result, int) and not isinstance(result, bool):
                    return result
            except (AttributeError, TypeError, RuntimeError):
                continue
    return -1
