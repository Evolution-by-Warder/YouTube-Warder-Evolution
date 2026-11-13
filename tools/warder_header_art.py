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

    # Warder metallic cyber skull within the electric circular family emblem.
    cx, cy = 94, 66
    for radius in range(68,47,-1):
        point(cx,cy,radius,(10,112,205),.013)
    for angle in range(0,360,2):
        a=math.radians(angle)
        for radius in (56.5,58,60.5,65):
            x,y=round(cx+radius*math.cos(a)),round(cy+radius*math.sin(a))
            blend(x,y,(50,193,245),.85 if radius in (58,60.5) else .45)
    point(cx,cy,53,(3,10,26),.88)
    for y in range(28,109):
        half = 24+(y-28)*.78 if y<46 else (37 if y<79 else 34-(y-79)*.32)
        for x in range(int(cx-half),int(cx+half)+1):
            f=max(.18,1-abs(x-cx)/half*.62)
            color=100+28*math.cos((x-cx)*.12)+27*math.sin(y*.16)
            blend(x,y,(color*f,(color+23)*f,(color+48)*f),.8)
    for sign in (-1,1):
        line(cx+sign*11,37,cx+sign*33,49,(4,10,29),.92,5)
        line(cx+sign*34,49,cx+sign*36,67,(6,21,35),.9,4)
        point(cx+sign*18,65,13,(2,3,10),.99)
        point(cx+sign*18,65,7,(240,26,13),.98)
        point(cx+sign*18,65,3,(255,210,125),.98)
    for y in range(81,95):
        for x in range(cx-6,cx+7):
            if abs(x-cx)+(95-y)*.34 < 7:
                blend(x,y,(2,6,15),.95)
    line(cx-22,97,cx+22,97,(4,16,35),.93,4)
    for i in range(-4,5):
        line(cx+i*5,97,cx+i*5,106,(18,34,51),.97,2)
    line(cx-21,108,cx+21,108,(100,214,240),.7)
    for angle in (30,65,98,145,200,251,303):
        a=math.radians(angle)
        line(cx+60*math.cos(a),cy+60*math.sin(a),
             cx+69*math.cos(a),cy+69*math.sin(a),(33,191,246),.7,2)

    for x in (1392,1664):
        for y in range(20,112):
            blend(x,y,(47,224,244),.85)
    for y in range(129,134):
        for x in range(w):
            blend(x,y,((50,235,250) if y==132 else
                       (1,160,231) if y==133 else (2,60+25*(y-129),110+24*(y-129))))
    data = b"".join(b"\x00" + image[y*w*3:(y+1)*w*3] for y in range(h))

    def chunk(tag, body):
        full = tag+body
        return (struct.pack(">I",len(body))+full+
                struct.pack(">I",zlib.crc32(full)&0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR",struct.pack(">IIBBBBB",w,h,8,2,0,0,0)) +
            chunk(b"IDAT",zlib.compress(data,9)) + chunk(b"IEND",b""))
