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
VERSION = "0.0.8~test11"
FILENAME = "%s_%s_all.ipk" % (PACKAGE, VERSION)
SENSITIVE = re.compile(rb"AIza[0-9A-Za-z_-]{20,}")


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
    path = output_dir / FILENAME
    path.write_bytes(ipk)
    digest = hashlib.sha256(ipk).hexdigest()
    (output_dir / (FILENAME + ".sha256")).write_text(
        digest + "  " + FILENAME + "\n", encoding="ascii"
    )
    print("PASS: test IPK built (%d Python files + 2 PNG icons, %d bytes)." %
          (len(data_files), len(ipk)))
    print("PASS: package SHA256:", digest)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    options = parser.parse_args()
    build(options.output)
