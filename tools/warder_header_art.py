"""Static Warder-blue shared header asset. Pure Python, build-time only.

No Pillow, Internet access, fonts or executable code on the receiver.
"""
import base64
import importlib.util
from pathlib import Path
import math
import random
import struct
import zlib

WIDTH, HEIGHT = 1920, 152


FULL_WARDER_SOURCE_SHA256 = "1cb97ce23564d4bfa226433ce59abdb1c42ac09e2dc2a40c809ee6c5065296e5"
FULL_WARDER_SIZE = (384, 429)
# The complete canonical PiconHub/Warder original is the only logo source.
# Do not use the old 104x100 cropped image or generate/paint a replacement.


def decode_original_skull(png):
    """Read the original 8-bit RGBA PNG using only the standard library.

    All five PNG row filters are handled. Work is done once by the IPK builder;
    Enigma2 still receives exactly one ready-made 1920x152 static header.
    """
    import hashlib
    if hashlib.sha256(png).hexdigest() != FULL_WARDER_SOURCE_SHA256:
        raise ValueError("Warder original artwork SHA256 does not match")
    if not png.startswith(bytes((137, 80, 78, 71, 13, 10, 26, 10))):
        raise ValueError("Invalid canonical Warder PNG")
    i, image_data, dimensions = 8, bytearray(), None
    while i + 12 <= len(png):
        size = int.from_bytes(png[i:i+4], "big")
        tag = png[i+4:i+8]
        chunk = png[i+8:i+8+size]
        if len(chunk) != size:
            raise ValueError("Truncated Warder original")
        if tag == b"IHDR":
            dimensions = (int.from_bytes(chunk[0:4], "big"),
                          int.from_bytes(chunk[4:8], "big"))
            if len(chunk) != 13 or dimensions != FULL_WARDER_SIZE or chunk[8:] != bytes((8, 6, 0, 0, 0)):
                raise ValueError("Unsupported original Warder artwork dimensions or PNG format")
        elif tag == b"IDAT":
            image_data.extend(chunk)
        i += size + 12
        if tag == b"IEND":
            break
    if dimensions != FULL_WARDER_SIZE or not image_data:
        raise ValueError("Incomplete Warder original artwork")
    w, h = dimensions
    raw = zlib.decompress(bytes(image_data))
    stride = w * 4
    if len(raw) != h * (stride + 1):
        raise ValueError("Unsupported original Warder scanline length")
    rgba = bytearray(w * h * 4)
    previous = bytearray(stride)
    for y in range(h):
        start = y * (stride + 1)
        filter_type = raw[start]
        if filter_type > 4:
            raise ValueError("Unsupported PNG filter")
        row = bytearray(raw[start+1:start+1+stride])
        for x in range(stride):
            left = row[x-4] if x >= 4 else 0
            up = previous[x]
            upper_left = previous[x-4] if x >= 4 else 0
            if filter_type == 1:
                prediction = left
            elif filter_type == 2:
                prediction = up
            elif filter_type == 3:
                prediction = (left + up) // 2
            elif filter_type == 4:
                p = left + up - upper_left
                a, b, c = abs(p-left), abs(p-up), abs(p-upper_left)
                prediction = left if a <= b and a <= c else up if b <= c else upper_left
            else:
                prediction = 0
            row[x] = (row[x] + prediction) & 255
        rgba[y*stride:(y+1)*stride] = row
        previous = row
    return w, h, rgba


def skull_placement():
    """Keep the full 384x429 symbol, especially the jaw, above the divider."""
    # The Warder divider begins at y=147. The complete source ends at y=142,
    # leaving a five-pixel gap; neither side nor the bottom is ever cut off.
    return 24, 3, 124, 139


def lettering_placement():
    """Warder-family lettering sized alongside the larger complete skull."""
    # The stock title masks are enlarged together, not stretched or redrawn.
    # Text still ends before the native weekday/date area at x=1090.
    return (184, 12, 1.10), (474, 89, 1.15)


def render_header():
    w, h = WIDTH, HEIGHT
    image = bytearray(w * h * 3)

    def blend(x, y, color, opacity=1.0):
        if x < 0 or x >= w or y < 0 or y >= h or opacity <= 0:
            return
        p = (y * w + x) * 3
        for i in range(3):
            image[p + i] = max(0, min(255, int(image[p + i] * (1-opacity) +
                                                color[i] * opacity)))

    def point(cx, cy, radius, color, alpha=1.0):
        rr = radius * radius
        for y in range(max(0, int(cy-radius)), min(h, int(cy+radius+1))):
            for x in range(max(0, int(cx-radius)), min(w, int(cx+radius+1))):
                if (x-cx)*(x-cx)+(y-cy)*(y-cy) <= rr:
                    blend(x, y, color, alpha)

    def line(x1, y1, x2, y2, color, alpha=1.0, width=1):
        steps = max(1, int(max(abs(x2-x1), abs(y2-y1))))
        for i in range(steps+1):
            x, y = round(x1 + (x2-x1)*i/steps), round(y1 + (y2-y1)*i/steps)
            if width == 1:
                blend(x, y, color, alpha)
            else:
                point(x, y, width*.55, color, alpha)

    for y in range(h):
        for x in range(w):
            left = math.exp(-((x-100)/300)**2-((y-70)/80)**2)
            mid = math.exp(-((x-700)/500)**2-((y-10)/95)**2)
            right = math.exp(-((x-1535)/550)**2-((y-151)/46)**2)
            noise = 1.7*math.sin(x/91+y/17)**2
            blend(x, y, (2+11*left+3*mid+3*right+noise,
                         7+26*left+8*mid+36*right+noise,
                         21+58*left+22*mid+79*right+noise))
    random_source = random.Random(314159)
    for i in range(160):
        x, y = random_source.randrange(w), random_source.randrange(h-7)
        a = random_source.random()*(.42 if 170 < x < 1140 else 1.0)
        if x > 1090 and y > 15:
            a *= .32
        point(x, y, 1.4+a, (21, 110, 230), .18+a*.45)
        if i%5 == 0:
            ex = x + random_source.choice((-1,1))*random_source.randrange(12,64)
            ey = y + random_source.randrange(-12,14)
            line(x, y, ex, ey, (10, 87, 188), a*.22)
    beam = ((162,124),(215,129),(272,126),(320,132),(370,125),
            (428,132),(489,127),(549,135),(609,130),(662,135),(714,132),(820,129))
    for (x1,y1),(x2,y2) in zip(beam,beam[1:]):
        line(x1,y1,x2,y2,(0,108,189),.5,3)
        line(x1,y1,x2,y2,(11,217,250),.75)
    for x in range(1090,w):
        center = 135+36*((x-1535)/565)**2
        if center >= h:
            continue
        for y in range(max(0,int(center)-7),min(h,int(center)+8)):
            d=abs(y-center)
            blend(x,y,(25,157,247),max(0,(1-d/8)*.5))
            if d < 1.5:
                blend(x,y,(118,241,255),.87)

    # The complete, exact, original Warder skull is composited once.
    # Four subpixel samples per axis use premultiplied alpha so tiny silver
    # details/glows survive shrinking without edge halos or an invented jaw.
    skull_path = (Path(__file__).resolve().parents[1] /
                  "plugin/Plugins/Extensions/WarderYouTube/images/warder_skull.png")
    sw, sh, source_pixels = decode_original_skull(skull_path.read_bytes())
    origin_x, origin_y, target_w, target_h = skull_placement()
    if not (origin_x >= 0 and origin_y >= 0 and
            origin_x + target_w <= 174 and origin_y + target_h <= 143):
        raise ValueError("Canonical skull placement would overlap its reserved space")
    for iy in range(target_h):
        for ix in range(target_w):
            total_alpha = total_r = total_g = total_b = 0
            for sy_sub in range(4):
                source_y = min(sh-1, int((iy+(sy_sub+0.5)/4)*sh/target_h))
                for sx_sub in range(4):
                    source_x = min(sw-1, int((ix+(sx_sub+0.5)/4)*sw/target_w))
                    p = (source_y*sw+source_x)*4
                    a = source_pixels[p+3]
                    total_alpha += a
                    total_r += source_pixels[p]*a
                    total_g += source_pixels[p+1]*a
                    total_b += source_pixels[p+2]*a
            if total_alpha:
                rgb = (total_r/total_alpha,
                       total_g/total_alpha,
                       total_b/total_alpha)
                blend(origin_x+ix, origin_y+iy, rgb, total_alpha/(16*255))

    # Owner-approved product lettering: the exact existing Warder-title
    # silhouettes, compressed as two tiny one-bit masks. Draw them once into
    # this PNG at build-time. No receiver-side fonts, SVGs or overlays.
    mask_path = Path(__file__).resolve().with_name("warder_title_masks.py")
    spec = importlib.util.spec_from_file_location("_warder_title_masks", str(mask_path))
    shapes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shapes)

    def stamp(encoded, sw, sh, origin_x, origin_y, scale, signature=False):
        raw = zlib.decompress(base64.b64decode(encoded))
        if len(raw) != (sw * sh + 7) // 8:
            raise ValueError("Invalid original Warder lettering mask")
        target_w, target_h = round(sw*scale), round(sh*scale)
        for y in range(target_h):
            src_y = min(sh-1, int(y/scale))
            for x in range(target_w):
                src_x = min(sw-1, int(x/scale))
                i = src_y*sw+src_x
                if not raw[i >> 3] & (0x80 >> (i & 7)):
                    continue
                tx, ty = origin_x+x, origin_y+y
                blend(tx+2, ty+2, (1,17,39), .78)
                if signature:
                    color = (51, min(255, 201 + (target_h-y)//3), 242)
                elif tx < 740:
                    light = max(153, min(245, 178 + 62*(1-abs(y/target_h-.45)*2)))
                    color = (light, min(255, light+12), min(255, light+28))
                else:
                    light = 163 + (target_h-y)*75//target_h
                    color = (20, min(255,light), 255)
                blend(tx,ty,color,1.0)

    (name_x, name_y, name_scale), (by_x, by_y, by_scale) = lettering_placement()
    if name_x + round(shapes.TITLE_WIDTH*name_scale) >= 1090:
        raise ValueError("Warder lettering overlaps the live date area")
    if by_y + round(shapes.BY_HEIGHT*by_scale) >= HEIGHT-5:
        raise ValueError("Warder signature overlaps the bottom divider")
    stamp(shapes.TITLE_MASK_B64, shapes.TITLE_WIDTH, shapes.TITLE_HEIGHT,
          name_x, name_y, name_scale)
    stamp(shapes.BY_MASK_B64, shapes.BY_WIDTH, shapes.BY_HEIGHT,
          by_x, by_y, by_scale, True)

    for x in (1392,1664):
        for y in range(20,138):
            blend(x,y,(47,224,244),.85)
    for y in range(h-5, h):
        for x in range(w):
            offset = y - (h-5)
            blend(x,y,((50,235,250) if offset == 3 else
                       (1,160,231) if offset == 4 else
                       (2,60+25*offset,110+24*offset)))
    # Keep the original deep-navy/metallic shades. RGB332 turned almost
    # every dark blue into pure black and visibly damaged the Warder design.
    # Still ONE static 1920x152 PNG decoded only once on the receiver.
    data = b"".join(b"\x00" + image[y*w*3:(y+1)*w*3] for y in range(h))

    def chunk(tag, body):
        full = tag + body
        return (struct.pack(">I", len(body)) + full +
                struct.pack(">I", zlib.crc32(full) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(data, 9)) + chunk(b"IEND", b""))
