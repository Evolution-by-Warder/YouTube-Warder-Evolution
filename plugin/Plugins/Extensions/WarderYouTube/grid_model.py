# -*- coding: utf-8 -*-
"""Pure 3-column remote navigation. No Enigma2 imports."""
COLUMNS = 3
VISIBLE_TILES = 6


def page_number(index):
    return max(0, index) // VISIBLE_TILES


def local_slot(index):
    return max(0, index) % VISIBLE_TILES


def move_index(index, direction, count):
    if count <= 0:
        return -1
    index = max(0, min(index, count - 1))
    changes = {"left": -1, "right": 1, "up": -COLUMNS, "down": COLUMNS}
    return max(0, min(count - 1, index + changes.get(direction, 0)))


def visible_slice(items, index):
    start = page_number(index) * VISIBLE_TILES
    return items[start:start + VISIBLE_TILES]
