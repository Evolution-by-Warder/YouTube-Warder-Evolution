#!/usr/bin/env python3
"""Create a self-contained, SMALL, receiver-test-only Enigma2 .ipk.

No downloader, yt-dlp, API key, videos, cache or other third-party files.
The package includes the Radio-derived GPL-2.0 YouTube resolver sources and license.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import io
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PKG_DIR = ROOT / "plugin/Plugins/Extensions/WarderYouTube"
TARGET_PREFIX = "usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube"
PACKAGE = "enigma2-plugin-extensions-youtube-warder-evolution"
VERSION = "0.0.8~test39"
FILENAME = "%s_%s_all.ipk" % (PACKAGE, VERSION)
SENSITIVE = re.compile(rb"(?:AIza[0-9A-Za-z_-]{20,}|GOCSPX-[0-9A-Za-z_-]{20,})")


def control_scripts():
    return {
        "preinst": """#!/bin/sh
echo '[Warder YouTube] Priprava instalacie / aktualizacie testovacieho balika...'
exit 0
""",
        "postinst": """#!/bin/sh
echo '[Warder YouTube] Instalacia/aktualizacia dokoncena (testovacia verzia).'
echo '[Warder YouTube] Po instalacii obnovte GUI Enigma2. Prijimac neresetujeme automaticky.'
echo '[Warder YouTube] API kluc sa nastavuje az v nastaveniach pluginu.'
exit 0
""",
        "prerm": """#!/bin/sh
echo '[Warder YouTube] Priprava odinstalovania / aktualizacie pluginu...'
exit 0
""",
        "postrm": """#!/bin/sh
echo '[Warder YouTube] Odinstalovanie/prechod na novu verziu dokonceny.'
echo '[Warder YouTube] Cudzie pluginy, yt-dlp ani ulozene nastavenia Enigma2 sa nemenili.'
exit 0
""",
    }


def tar_gzip(files):
    """Make a deterministic gzip-tar archive of [(path, bytes, executable)]."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode="w", format=tarfile.GNU_FORMAT) as tar:
            for name, content, executable in sorted(files):
                if name.startswith("/") or ".." in Path(name).parts:
                    raise ValueError("Invalid tar member")
                entry = tarfile.TarInfo("./" + name)
                entry.mode = 0o755 if executable else 0o644
                entry.uid = entry.gid = 0
                entry.uname = entry.gname = "root"
                entry.mtime = 0
                entry.size = len(content)
                tar.addfile(entry, io.BytesIO(content))
    return buf.getvalue()


def ar_member(name, data):
    if len(name) > 15:
        raise ValueError("ar file name exceeds 15 bytes: " + name)
    fields = (
        (name + "/").ljust(16)
        + str(0).ljust(12)
        + str(0).ljust(6)
        + str(0).ljust(6)
        + ("100644").ljust(8)
        + str(len(data)).ljust(10)
        + "\x60\n"
    )
    assert len(fields) == 60
    return fields.encode("ascii") + data + (b"\n" if len(data) % 2 else b"")


def build(output_dir):
    if not PKG_DIR.is_dir():
        raise ValueError("Plugin source directory is missing.")
    py_sources = sorted(PKG_DIR.glob("*.py"))
    if len(py_sources) < 10 or not (PKG_DIR / "plugin.py").exists():
        raise ValueError("Incomplete plugin source tree.")
    data_files = []
    for source in py_sources:
        content = source.read_bytes()
        if SENSITIVE.search(content):
            raise ValueError("Possible API key in source: " + source.name)
        data_files.append((TARGET_PREFIX + "/" + source.name, content, False))

    for filename, expected in (("plugin.png", (100, 60)),
                               ("plugin_fhd.png", (150, 90))):
        path = PKG_DIR / "images" / filename
        raw = path.read_bytes()
        if (len(raw) > 100_000 or not raw.startswith(b"\x89PNG\r\n\x1a\n")
                or raw[12:16] != b"IHDR"
                or tuple(int.from_bytes(raw[i:i + 4], "big") for i in (16, 20)) != expected):
            raise ValueError("Invalid Warder plugin icon: " + filename)
        data_files.append((TARGET_PREFIX + "/images/" + filename, raw, False))

    # Pre-render all eight native menu icons and two focus states at build
    # time. Receiver sees only ePixmap/Pixmap PNGs, no Python drawing.
    import importlib.util
    art_file = ROOT / "tools" / "warder_nav_art.py"
    art_spec = importlib.util.spec_from_file_location("_warder_nav_art", str(art_file))
    art = importlib.util.module_from_spec(art_spec)
    art_spec.loader.exec_module(art)
    accents = [("nav_%d.png" % i, art.render_icon(i), (64, 64))
               for i in range(art.ICON_COUNT)]
    accents += [
        ("nav_focus.png", art.render_nav_focus(), art.NAV_FOCUS_SIZE),
        ("video_focus.png", art.render_video_focus(), art.VIDEO_FOCUS_SIZE),
        ("grid_focus.png", art.render_grid_focus(), art.GRID_FOCUS_SIZE)
    ]
    for filename, png, expected in accents:
        if (not png.startswith(b"\x89PNG\r\n\x1a\n") or
                png[12:16] != b"IHDR" or png[25] != 6 or
                tuple(int.from_bytes(png[i:i+4], "big") for i in (16, 20)) != expected or
                not 0 < len(png) < 150_000):
            raise ValueError("Invalid Warder navigation artwork: " + filename)
        data_files.append((TARGET_PREFIX + "/images/" + filename, png, False))

    # Copy ONLY the SHA256-pinned, owner-accepted 1920x152 PNG, unchanged.
    # Import by explicit build-script path: unit tests load this builder via
    # importlib with sys.path that does not contain tools/.
    import importlib.util
    asset_path = ROOT / "tools" / "warder_header_art.py"
    spec = importlib.util.spec_from_file_location("_warder_header_art", str(asset_path))
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    header_png = source.render_header()
    if not (header_png[:8] == bytes((137, 80, 78, 71, 13, 10, 26, 10))
            and int.from_bytes(header_png[16:20], "big") == 1920
            and int.from_bytes(header_png[20:24], "big") == 152
            and len(header_png) < 600_000):
        raise ValueError("Invalid Warder shared header PNG (bytes=%d, signature=%r, size=%d,%d)" % (len(header_png), header_png[:8], int.from_bytes(header_png[16:20], "big"), int.from_bytes(header_png[20:24], "big")))
    data_files.append((TARGET_PREFIX + "/images/warder_header.png",
                       header_png, False))

    # Include our self-contained Radio-derived GPL-2.0 backend and license.
    # No plugin dependency, downloader, credentials or third-party binaries.
    engine = PKG_DIR / "youtube_engine"
    for filename in ("__init__.py", "compat.py", "extractor.py", "jsinterp.py",
                     "settings.py", "NOTICE", "COPYING.GPLv2"):
        path = engine / filename
        data_files.append((TARGET_PREFIX + "/youtube_engine/" + filename,
                           path.read_bytes(), False))

    control_text = (
        "Package: %s\nVersion: %s\nArchitecture: all\n"
        "Section: extra\nPriority: optional\nMaintainer: Evolution by Warder\n"
        "Description: TEST ONLY - native blue Enigma2 YouTube UI and experimental video player\n"
    ) % (PACKAGE, VERSION)
    control_files = [("control", control_text.encode("utf-8"), False)]
    for name, content in control_scripts().items():
        control_files.append((name, content.encode("utf-8"), True))
    control_tar = tar_gzip(control_files)
    data_tar = tar_gzip(data_files)
    ipk = b"!<arch>\n" + b"".join((
        ar_member("debian-binary", b"2.0\n"),
        ar_member("control.tar.gz", control_tar),
        ar_member("data.tar.gz", data_tar),
    ))
    output_dir.mkdir(parents=True, exist_ok=True)
    # Direct visual QA of the exact same static PNG included inside IPK.
    (output_dir / "warder-header-preview.png").write_bytes(header_png)
    path = output_dir / FILENAME
    path.write_bytes(ipk)
    digest = hashlib.sha256(ipk).hexdigest()
    (output_dir / (FILENAME + ".sha256")).write_text(
        digest + "  " + FILENAME + "\n", encoding="ascii"
    )
    total_png = sum(path.endswith(".png") for path, _, _ in data_files)
    print("PASS: test IPK built (%d Python files + %d PNG images, %d bytes)." %
          (len(py_sources), total_png, len(ipk)))
    print("PASS: package SHA256:", digest)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    options = parser.parse_args()
    build(options.output)
