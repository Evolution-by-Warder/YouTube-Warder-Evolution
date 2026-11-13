#!/usr/bin/env python3
"""Regenerate ONE clean Warder-family static banner for the YouTube plugin.

Owner-approved complete original 384x429 Warder skull. Fresh metallic title and
handwritten-family-style signature are rendered directly into ONE RGB PNG.
NO old traced title masks, cut-out layers, background patches, runtime fonts,
additional GUI title overlays, or generated/painted parts of the skull.
This tool is build-maintenance only; Pillow and fonts never ship in the IPK.
"""
from pathlib import Path
import argparse
import hashlib
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SKULL = ROOT / "plugin/Plugins/Extensions/WarderYouTube/images/warder_skull.png"
OUT = ROOT / "plugin/Plugins/Extensions/WarderYouTube/images/warder_header.png"
ORIGINAL_SHA256 = "1cb97ce23564d4bfa226433ce59abdb1c42ac09e2dc2a40c809ee6c5065296e5"
TITLE_FONT = "/usr/share/fonts/truetype/lato/Lato-Heavy.ttf"
SIGNATURE_FONT = "/usr/share/fonts/opentype/urw-base35/Z003-MediumItalic.otf"
WIDTH, HEIGHT = 1920, 152


def glow(image, mask, radius, dx, dy, strength, rgb):
    blurred = mask.filter(ImageFilter.GaussianBlur(radius)).point(
        lambda a: a*strength//255
    )
    if dx or dy:
        blurred = ImageChops.offset(blurred, dx, dy)
    image.paste(Image.new("RGB", (WIDTH, HEIGHT), rgb), (0, 0), blurred)


def render(output=OUT):
    if hashlib.sha256(SKULL.read_bytes()).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("The full, exact original Warder skull is required")
    for font in (TITLE_FONT, SIGNATURE_FONT):
        if not Path(font).is_file():
            raise ValueError("Missing build-only Warder-family font: " + font)
    w, h = WIDTH, HEIGHT
    pixels = bytearray(w*h*3)
    for y in range(h):
        for x in range(w):
            left = math.exp(-((x-100)/290)**2 - ((y-52)/94)**2)
            middle = math.exp(-((x-580)/470)**2 - ((y-40)/94)**2)
            far = math.exp(-((x-1620)/660)**2 - ((y-128)/62)**2)
            p = 3*(y*w+x)
            pixels[p:p+3] = bytes((
                int(2+6*left+3*middle+4*far),
                int(7+20*left+9*middle+17*far),
                int(22+49*left+30*middle+48*far)
            ))
    image = Image.frombytes("RGB",(w,h),bytes(pixels)).convert("RGBA")
    mesh = Image.new("RGBA",(w,h),(0,0,0,0))
    draw = ImageDraw.Draw(mesh)
    rng = random.Random(43201)
    nodes = [(rng.randint(0,1000),rng.randint(0,145)) for _ in range(100)]
    for i,(x,y) in enumerate(nodes):
        near = sorted((pt for pt in nodes if pt != (x,y)),
                      key=lambda pt:(pt[0]-x)**2+(pt[1]-y)**2)[:3]
        for xx,yy in near:
            if abs(xx-x)+abs(yy-y) < 130:
                alpha = rng.randint(14,62) if x<220 else rng.randint(5,25)
                draw.line(((x,y),(xx,yy)), fill=(12,112,215,alpha), width=1)
        if i%3==0:
            draw.ellipse((x,y,x+2,y+2),fill=(14,152,244,rng.randint(22,110)))
    image = Image.alpha_composite(image,mesh.filter(ImageFilter.GaussianBlur(2)))
    image = Image.alpha_composite(image,mesh)

    stars = Image.new("RGBA",(w,h),(0,0,0,0))
    d = ImageDraw.Draw(stars)
    rand = random.Random(16611)
    for _ in range(270):
        x,y=rand.randrange(w),rand.randrange(138)
        if 170<x<1100 and y>30 and rand.random()<.77:
            continue
        a=rand.randint(18,110)
        size=1 if rand.random()<.84 else 2
        d.ellipse((x,y,x+size,y+size),
                  fill=(65+rand.randrange(40),135+rand.randrange(80),252,a))
    image=Image.alpha_composite(image,stars)

    # Fresh continuous orbital/atmospheric sweep, not a background patch.
    horizon=Image.new("RGBA",(w,h),(0,0,0,0))
    draw=ImageDraw.Draw(horizon)
    for x in range(1110,w):
        edge=108+.00017*(x-1650)**2
        for yy in range(max(0,int(edge)),h):
            fade=max(0,1-(yy-edge)/56)
            if fade>0:
                draw.point((x,yy),fill=(3,95+int(85*fade),244,int(90*fade)))
    image=Image.alpha_composite(image,horizon.filter(ImageFilter.GaussianBlur(15)))
    image=Image.alpha_composite(image,horizon)
    strokes=Image.new("RGBA",(w,h),(0,0,0,0))
    d=ImageDraw.Draw(strokes)
    points=[(x,108+.00017*(x-1650)**2) for x in range(1080,w)
            if 100 <= 108+.00017*(x-1650)**2 <= h]
    for width,color in ((7,(10,117,245,110)),
                        (3,(24,219,255,190)),
                        (1,(155,253,255,230))):
        d.line(points,fill=color,width=width,joint="curve")
    image=Image.alpha_composite(image,strokes.filter(ImageFilter.GaussianBlur(5)))
    image=Image.alpha_composite(image,strokes)

    # Entire untouched original, intact jaw and ring, fits above y=147.
    skull=Image.open(SKULL).convert("RGBA")
    if skull.size != (384,429):
        raise ValueError("Original skull dimensions changed")
    image.alpha_composite(skull.resize((124,139),Image.Resampling.LANCZOS),(24,3))

    # CLEAN brand lettering. No legacy one-bit title/signature masks.
    font=ImageFont.truetype(TITLE_FONT,74)
    x,y=187,14
    silver_text,cyan_text="YouTube Warder ","Evolution"
    x_blue=x+round(font.getlength(silver_text))
    if x_blue+round(font.getlength(cyan_text))>=1090:
        raise ValueError("Brand title overlaps date/time region")
    masks=[]
    for xx,text in ((x,silver_text),(x_blue,cyan_text)):
        mask=Image.new("L",(w,h),0)
        ImageDraw.Draw(mask).text((xx,y),text,font=font,fill=255)
        masks.append(mask)
        glow(image,mask,7,1,2,160,(0,92,180))
        glow(image,mask,2,2,4,200,(0,3,16))
    silver=Image.new("RGB",(w,h))
    blue=Image.new("RGB",(w,h))
    silver_px=silver.load()
    blue_px=blue.load()
    for yy in range(h):
        if yy<=32:
            c=(230,247,255)
        elif yy<=48:
            c=(247,252,255)
        elif yy<=63:
            c=(181,199,215)
        elif yy<=75:
            c=(100,139,184)
        else:
            c=(86,122,160)
        if yy<40:
            cb=(180,254,255)
        elif yy<52:
            cb=(33,225,253)
        elif yy<67:
            cb=(12,156,248)
        else:
            cb=(5,94,191)
        for xx in range(w):
            silver_px[xx,yy]=c
            blue_px[xx,yy]=cb
    image.paste(silver,(0,0),masks[0])
    image.paste(blue,(0,0),masks[1])

    # GSU-family handwritten signature from CLEAN SCRIPT FONT, not a
    # contaminated RGB pixel mask copied from a previous banner.
    signature=Image.new("L",(w,h),0)
    signature_font=ImageFont.truetype(SIGNATURE_FONT,54)
    ImageDraw.Draw(signature).text((477,81),"by Warder",
                                   font=signature_font,fill=255)
    glow(image,signature,6,0,0,130,(1,123,205))
    image.paste(Image.new("RGB",(w,h),(80,237,255)),(0,0),signature)

    lines=Image.new("RGBA",(w,h),(0,0,0,0))
    d=ImageDraw.Draw(lines)
    for points in (((189,114),(225,118),(274,115),(315,120),(373,117),(405,121),(448,119)),
                   ((673,126),(709,124),(751,128),(795,128),(839,129),(891,128))):
        d.line(points,fill=(3,155,230,190),width=3,joint="curve")
        d.line(points,fill=(77,231,255,240),width=1,joint="curve")
    d.line(((480,134),(555,135),(619,134),(691,133)),
           fill=(16,205,239,190),width=2)
    image=Image.alpha_composite(image,lines.filter(ImageFilter.GaussianBlur(3)))
    image=Image.alpha_composite(image,lines)
    divider=ImageDraw.Draw(image)
    divider.rectangle((0,147,w-1,149),fill=(9,178,217,255))
    divider.line((0,148,w-1,148),fill=(110,246,255,255),width=1)
    path=Path(output)
    path.parent.mkdir(parents=True,exist_ok=True)
    image.convert("RGB").save(path,optimize=True,compress_level=9)
    raw=path.read_bytes()
    assert raw.startswith(bytes((137,80,78,71,13,10,26,10)))
    assert (int.from_bytes(raw[16:20],"big"),
            int.from_bytes(raw[20:24],"big")) == (1920,152)
    print("Warder original: full jaw; single complete banner:",path,
          "bytes:",len(raw),"sha256:",hashlib.sha256(raw).hexdigest())
    return raw


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=OUT)
    args=parser.parse_args()
    render(args.output)
