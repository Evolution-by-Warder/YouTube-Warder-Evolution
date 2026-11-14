# -*- coding: utf-8 -*-
"""One-line, content-width YouTube Home category chips.

The visible count is automatically reduced for longer localized channel names.
No pixel-based clipping or two-line text; native Enigma2 widgets are moved and
resized on layout, preserving the blue skin and remote navigation.
"""
import unicodedata

CHIP_LEFT = 427
CHIP_RIGHT = 1495  # Page count starts at 1560; arrow is at 1507.
CHIP_GAP = 7
MAX_VISIBLE = 7


def chip_width(label):
    """Conservative Regular;22 estimate with breathing room for any locale."""
    label = str(label or "").strip()
    visual = 0
    for ch in label:
        east = unicodedata.east_asian_width(ch)
        if east in ("W", "F"):
            visual += 22
        elif ch in "ilíI.,'!;| ":
            visual += 8
        elif ch in "MW@ŽŠŘ":
            visual += 18
        elif ch.isupper():
            visual += 16
        else:
            visual += 13
    return max(86, min(286, visual + 34))


def layout_chips(labels, selected, previous_offset=0):
    """Return (offset, [(index, x, width), ...], has_previous, has_next).

    Keep the selected chip in view and fit as many as possible without
    shrinking or wrapping its label. Handles 1..N account-specific chips.
    """
    if not labels:
        return 0, [], False, False
    selected = max(0, min(int(selected), len(labels) - 1))
    start = max(0, min(int(previous_offset), len(labels) - 1))
    if selected < start:
        start = selected

    def visible_from(offset):
        out, x = [], CHIP_LEFT
        for i in range(offset, min(len(labels), offset + MAX_VISIBLE)):
            width = chip_width(labels[i])
            if x + width > CHIP_RIGHT:
                break
            out.append((i, x, width))
            x += width + CHIP_GAP
        return out

    slots = visible_from(start)
    while (not slots or selected > slots[-1][0]) and start < selected:
        start += 1
        slots = visible_from(start)
    if not slots:
        start = selected
        slots = visible_from(start)
    end = slots[-1][0] if slots else start - 1
    return start, slots, start > 0, end < len(labels) - 1
