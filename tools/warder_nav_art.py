"""Load SHA-pinned receiver-approved test50 artwork, without redraw/rescaling."""
from pathlib import Path
import hashlib

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "plugin/Plugins/Extensions/WarderYouTube/images"
ICON_COUNT = 8
ICON_SIZE = 64
NAV_FOCUS_SIZE = (328, 72)
VIDEO_FOCUS_SIZE = GRID_FOCUS_SIZE = (477, 350)
APPROVED = {'nav_4.png': 'c7cf0519873365ba51126ae05ae169c76515113eccd5b47e5976c999d6c839c6', 'nav_0.png': 'ba623bc3e7fcee307052f1eeb91f7ccf325a146c5511c3db6568d854078c6f65', 'nav_3.png': '30077fc351524540890999cbe28b61203a710ed9dc5cc40fa8b2feef73b1f4b5', 'grid_focus.png': 'c44f7116f2c7af2089103b3890ec581da6c0e258583a055331b1be081108c6c4', 'nav_6.png': '0295cf6f61fa00878e483747980cc737d13c33af036d6f7a7da58e9464770ede', 'nav_7.png': '8b6e400026d61db74195ce79aa9ab4e46ebe55f6c43a55bdbe68e1cf887912c9', 'nav_5.png': 'b74812d4827cba8844b61402799c2a7be923753351b0d310291531fbd9f02d68', 'nav_2.png': '4a9c342c35d7221971c240ea3146f0a99c3e55411cafa4f5ef236dc810d6f211', 'nav_1.png': '872dde7d1b04d41b9ee74a9ed74c0be443b68ea24431fa195939b37d7517a20c', 'nav_focus.png': 'e7c5e3800572277ecac31b97efecabe787557c11437809cd10c5715200569867', 'video_focus.png': 'c44f7116f2c7af2089103b3890ec581da6c0e258583a055331b1be081108c6c4'}


def _load(name):
    raw = (IMAGES / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != APPROVED[name]:
        raise ValueError("Approved Warder artwork changed: " + name)
    return raw


def render_icon(index):
    if type(index) is not int or not 0 <= index < ICON_COUNT:
        raise ValueError("Invalid menu icon")
    return _load("nav_%d.png" % index)


def render_nav_focus():
    return _load("nav_focus.png")


def render_video_focus():
    return _load("video_focus.png")


def render_grid_focus():
    return _load("grid_focus.png")
