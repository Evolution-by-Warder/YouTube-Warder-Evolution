"""Access the single READY-MADE Warder-family header (build verification only).

The canonical complete image is committed at images/warder_header.png.
No runtime text/font layers, no traced bitmap masks or cut-and-paste
signature. The separate render_full_header.py creates the complete art only
when a designer intentionally updates the ONE visual asset.
"""
from pathlib import Path
import hashlib

WIDTH, HEIGHT = 1920, 152
FULL_WARDER_SIZE = (384, 429)
FULL_WARDER_SOURCE_SHA256 = "1cb97ce23564d4bfa226433ce59abdb1c42ac09e2dc2a40c809ee6c5065296e5"
FINAL_BANNER_SHA256 = "023588797d292b985b2d1e4d686ba114757becd49ed374e2beefd95f78a34e31"
ART_DIR = (Path(__file__).resolve().parents[1] /
           "plugin/Plugins/Extensions/WarderYouTube/images")


def _check_png(data, expected_dimensions, color_type):
    signature = bytes((137, 80, 78, 71, 13, 10, 26, 10))
    if not data.startswith(signature) or data[12:16] != b"IHDR":
        raise ValueError("Invalid Warder original or full banner PNG")
    size = (int.from_bytes(data[16:20], "big"),
            int.from_bytes(data[20:24], "big"))
    if size != expected_dimensions or data[24:26] != bytes((8, color_type)):
        raise ValueError("Warder PNG format or dimensions changed")


def render_header():
    """Return one immutable authored RGB PNG, not generated text overlays."""
    source = (ART_DIR / "warder_skull.png").read_bytes()
    _check_png(source, FULL_WARDER_SIZE, 6)
    if hashlib.sha256(source).hexdigest() != FULL_WARDER_SOURCE_SHA256:
        raise ValueError("Complete original Warder skull changed")
    png = (ART_DIR / "warder_header.png").read_bytes()
    _check_png(png, (WIDTH, HEIGHT), 2)
    if hashlib.sha256(png).hexdigest() != FINAL_BANNER_SHA256:
        raise ValueError("Clean finished Warder-family banner changed")
    return png
