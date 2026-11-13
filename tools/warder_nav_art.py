"""Warder YouTube native menu picons and focus accents (build time only).

Pure standard-library PNG generation: no custom renderer or runtime drawing on
the receiver. Artwork consists of small white line symbols with a restrained
Warder-cyan glow, selected-row blue fill, and a transparent video focus frame.
"""
import math
import struct
import zlib

ICON_COUNT = 8
ICON_SIZE = 64
NAV_FOCUS_SIZE = (328, 72)
VIDEO_FOCUS_SIZE = (477, 324)
GRID_FOCUS_SIZE = (491, 364)


def png_rgba(width, height, rgba):
    if len(rgba) != width * height * 4:
        raise ValueError("Invalid RGBA buffer")
    def chunk(kind, body):
        data = kind + body
        return (struct.pack(">I", len(body)) + data +
                struct.pack(">I", zlib.crc32(data) & 0xffffffff))
    scanlines = b"".join(
        b"\x00" + bytes(rgba[y * width * 4:(y + 1) * width * 4])
        for y in range(height)
    )
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height,
                                         8, 6, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(scanlines, 9)) +
            chunk(b"IEND", b""))


def _segments(points, closed=False):
    items = list(zip(points, points[1:]))
    if closed:
        items.append((points[-1], points[0]))
    return items


def _arc(cx, cy, radius, start, stop, samples=40):
    return [(cx + radius * math.cos(start + (stop - start) * i / samples),
             cy + radius * math.sin(start + (stop - start) * i / samples))
            for i in range(samples + 1)]


def _star(cx, cy):
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = 23 if i % 2 == 0 else 10.5
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    return points


def _icon_strokes(index):
    strokes = []
    def path(points, closed=False):
        strokes.extend(_segments(points, closed))
    def arc(cx, cy, radius, start, stop):
        path(_arc(cx, cy, radius, start, stop))
    if index == 0:  # Home
        path([(10, 30), (32, 12), (54, 30)])
        path([(17, 27), (17, 55), (47, 55), (47, 27)])
        path([(28, 55), (28, 42), (37, 42), (37, 55)])
        path([(45, 17), (45, 12), (50, 12), (50, 23)])
    elif index == 1:  # Search
        arc(27, 27, 16, 0, 2 * math.pi)
        path([(39, 39), (55, 55)])
    elif index == 2:  # Subscriptions
        path([(32, 10), (32, 44), (19, 31)])
        path([(32, 44), (45, 31)])
        path([(13, 48), (13, 56), (51, 56), (51, 48)])
    elif index == 3:  # History
        arc(33, 34, 21, -2.35, 3.70)
        path([(8, 16), (8, 31), (22, 31)])
        path([(33, 18), (33, 34), (44, 41)])
    elif index == 4:  # Playlists
        for y in (19, 29, 39):
            path([(12, y), (49 if y != 39 else 33, y)])
        path([(40, 40), (40, 55), (55, 48)], closed=True)
    elif index == 5:  # Favourites
        path(_star(32, 33), closed=True)
    elif index == 6:  # Settings
        arc(32, 33, 17, 0, 2 * math.pi)
        arc(32, 33, 8, 0, 2 * math.pi)
        for i in range(8):
            a = i * math.pi / 4
            path([(32 + 17 * math.cos(a), 33 + 17 * math.sin(a)),
                  (32 + 24 * math.cos(a), 33 + 24 * math.sin(a))])
    elif index == 7:  # Updates
        arc(32, 32, 21, -2.72, 0.30)
        arc(32, 32, 21, 0.42, 3.42)
        path([(52, 22), (55, 39), (39, 36)])
        path([(12, 42), (9, 25), (25, 28)])
    else:
        raise ValueError("Invalid menu icon index")
    return strokes


def render_icon(index):
    strokes = _icon_strokes(index)
    raw = bytearray(ICON_SIZE * ICON_SIZE * 4)
    for y in range(ICON_SIZE):
        for x in range(ICON_SIZE):
            px, py = x + 0.5, y + 0.5
            distance = 999
            for (x1, y1), (x2, y2) in strokes:
                dx, dy = x2 - x1, y2 - y1
                length = dx * dx + dy * dy
                t = 0 if length == 0 else max(0, min(1,
                    ((px - x1) * dx + (py - y1) * dy) / length))
                dist = math.hypot(px - (x1 + t * dx),
                                  py - (y1 + t * dy))
                distance = min(distance, dist)
            core = max(0, min(1, 2.5 - distance))
            glow = max(0, min(1, (7.0 - distance) / 5.0))
            alpha = int(255 * (core + (1 - core) * glow * 0.27))
            if alpha:
                p = (y * ICON_SIZE + x) * 4
                raw[p:p+4] = bytes((
                    int(83 + 172 * core),
                    int(207 + 48 * core),
                    255,
                    alpha
                ))
    return png_rgba(ICON_SIZE, ICON_SIZE, raw)


def render_nav_focus():
    w, h = NAV_FOCUS_SIZE
    raw = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            edge = min(x, w-1-x, y, h-1-y)
            if (x < 6 and y < 6 and (x-5)**2 + (y-5)**2 > 25 or
                x >= w-6 and y < 6 and (x-(w-6))**2 + (y-5)**2 > 25 or
                x < 6 and y >= h-6 and (x-5)**2 + (y-(h-6))**2 > 25 or
                x >= w-6 and y >= h-6 and (x-(w-6))**2 + (y-(h-6))**2 > 25):
                continue
            highlight = 1 - min(1, y / float(h))
            if edge < 2:
                rgb = (29, 221, 255)
            elif edge < 5:
                rgb = (12, 139, 220)
            else:
                rgb = (int(7 + 4 * highlight),
                       int(94 + 31 * highlight),
                       int(171 + 54 * highlight))
            p = (y*w+x)*4
            raw[p:p+4] = bytes((*rgb, 255))
    return png_rgba(w, h, raw)


def _render_selected_video_frame(width, height):
    """Only the focused tile gets a luminous cyan frame.

    The centre is transparent so thumbnails and text are never covered.
    Both Home (477x324) and Search results (491x364) reuse this geometry.
    """
    w, h = width, height
    raw = bytearray(w * h * 4)
    for y in range(h):
        for x in range(w):
            edge = min(x, y, w - 1 - x, h - 1 - y)
            if edge < 2:
                rgb, alpha = (177, 253, 255), 255
            elif edge < 5:
                rgb, alpha = (15, 222, 255), 255
            elif edge < 9:
                rgb, alpha = (8, 129, 206), int(150 * (9 - edge) / 4)
            else:
                continue
            p = (y * w + x) * 4
            raw[p:p+4] = bytes((*rgb, alpha))
    return png_rgba(w, h, raw)


def render_video_focus():
    return _render_selected_video_frame(*VIDEO_FOCUS_SIZE)


def render_grid_focus():
    return _render_selected_video_frame(*GRID_FOCUS_SIZE)
