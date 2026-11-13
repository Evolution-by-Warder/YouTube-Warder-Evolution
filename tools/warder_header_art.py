"""Static Warder-blue shared header asset. Pure Python, build-time only.

No Pillow, Internet access, fonts or executable code on the receiver.
"""
import math
import random
import struct
import zlib

WIDTH, HEIGHT = 1920, 134


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
            left = math.exp(-((x-100)/300)**2-((y-60)/69)**2)
            mid = math.exp(-((x-700)/500)**2-((y-10)/95)**2)
            right = math.exp(-((x-1535)/550)**2-((y-133)/40)**2)
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
    beam = ((162,104),(215,109),(272,106),(320,112),(370,105),
            (428,112),(489,107),(549,115),(609,110),(662,115),(714,112),(820,109))
    for (x1,y1),(x2,y2) in zip(beam,beam[1:]):
        line(x1,y1,x2,y2,(0,108,189),.5,3)
        line(x1,y1,x2,y2,(11,217,250),.75)
    for x in range(1090,w):
        center = 117+36*((x-1535)/565)**2
        if center >= h:
            continue
        for y in range(max(0,int(center)-7),min(h,int(center)+8)):
            d=abs(y-center)
            blend(x,y,(25,157,247),max(0,(1-d/8)*.5))
            if d < 1.5:
                blend(x,y,(118,241,255),.87)

    # Embed the exact owner-supplied Warder family logo ONCE, rather than
    # drawing or layering an invented skull. PNG is indexed RGBA with a
    # small palette. The source file remains separately versioned in the repo.
    from pathlib import Path
    skull_path = (Path(__file__).resolve().parents[1] /
                  "plugin/Plugins/Extensions/WarderYouTube/images/warder_skull.png")
    png = skull_path.read_bytes()
    if not png.startswith(bytes((137,80,78,71,13,10,26,10))):
        raise ValueError("Invalid original Warder skull asset")
    offset, palette, alphas, pixels = 8, b"", b"", bytearray()
    chunks = bytearray()
    sw = sh = 0
    while offset + 12 <= len(png):
        length = int.from_bytes(png[offset:offset+4], "big")
        tag = png[offset+4:offset+8]
        payload = png[offset+8:offset+8+length]
        if tag == b"IHDR":
            sw = int.from_bytes(payload[:4], "big")
            sh = int.from_bytes(payload[4:8], "big")
            if payload[8:] != bytes((8,3,0,0,0)) or (sw,sh)!=(104,100):
                raise ValueError("Unsupported original Warder skull format")
        elif tag == b"PLTE":
            palette = payload
        elif tag == b"tRNS":
            alphas = payload
        elif tag == b"IDAT":
            chunks.extend(payload)
        offset += 12 + length
        if tag == b"IEND":
            break
    if not palette or not chunks:
        raise ValueError("Incomplete original Warder skull")
    scanlines = zlib.decompress(bytes(chunks))
    if len(scanlines) != sh*(sw+1):
        raise ValueError("Unexpected Warder skull scanlines")
    # The original indexed PNG deliberately uses filter=0 on every row.
    if any(scanlines[row*(sw+1)] != 0 for row in range(sh)):
        raise ValueError("Unsupported Warder skull PNG filter")
    # One static compositing pass at build time. The receiver only decodes
    # the finalized shared 1920x134 PNG; no runtime scaling or rendering.
    target_w, target_h, origin_x, origin_y = 135, 129, 24, 2
    for iy in range(target_h):
        sy = iy * sh // target_h
        for ix in range(target_w):
            sx = ix * sw // target_w
            color_index = scanlines[sy*(sw+1)+1+sx]
            a = (alphas[color_index] / 255.0
                 if color_index < len(alphas) else 1.0)
            pi = color_index*3
            rgb = tuple(palette[pi:pi+3])
            blend(origin_x+ix, origin_y+iy, rgb, a)

    for x in (1392,1664):
        for y in range(20,112):
            blend(x,y,(47,224,244),.85)
    for y in range(129,134):
        for x in range(w):
            blend(x,y,((50,235,250) if y==132 else
                       (1,160,231) if y==133 else (2,60+25*(y-129),110+24*(y-129))))
    # Quantize to a lightweight indexed PNG (RGB332 palette). The static
    # image is decoded by Enigma2 only once; no runtime drawing or PIL.
    palette = bytearray()
    for index in range(256):
        r = ((index >> 5) & 7) * 255 // 7
        g = ((index >> 2) & 7) * 255 // 7
        b = (index & 3) * 255 // 3
        palette.extend((r, g, b))
    indexed = bytearray(w * h)
    for pixel in range(w * h):
        base = pixel * 3
        red, green, blue = image[base:base+3]
        indexed[pixel] = (red & 0xe0) | ((green & 0xe0) >> 3) | (blue >> 6)
    data = b"".join(b"\x00" + indexed[y*w:(y+1)*w] for y in range(h))

    def chunk(tag, body):
        full = tag + body
        return (struct.pack(">I", len(body)) + full +
                struct.pack(">I", zlib.crc32(full) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 3, 0, 0, 0)) +
            chunk(b"PLTE", bytes(palette)) +
            chunk(b"IDAT", zlib.compress(data, 9)) + chunk(b"IEND", b""))
