# -*- coding: utf-8 -*-
"""Warder Evolution: strict opt-in, hash-verified YouTube plugin updates.

Inspired by the approved Warder Radio/PiconHub updater architecture.
The small Python 3 backend has no Enigma2 imports. All I/O is blocking:
ALWAYS run check_update/install_update in a Twisted worker thread.
"""
import hashlib
import io
import json
import re
import ssl
import subprocess
import tarfile
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO = "Evolution-by-Warder/YouTube-Warder-Evolution"
PACKAGE = "enigma2-plugin-extensions-youtube-warder-evolution"
PRODUCT = "YouTube Warder Evolution"
CURRENT_VERSION = "0.0.8~test35"
FEED_TESTING = ("https://raw.githubusercontent.com/" + REPO +
                "/feature/native-search-v002/update/testing.json")
FEED_STABLE = ("https://raw.githubusercontent.com/" + REPO +
               "/main/update/stable.json")
MAX_MANIFEST = 32 * 1024
MAX_IPK = 4 * 1024 * 1024
PREFIX = "usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/"
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)(?:[~-](test|beta|rc)(\d+))?$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class UpdateError(Exception):
    """Safe text: do not include network URLs, tokens or raw opkg logs."""


def version_key(version):
    if not isinstance(version, str):
        raise UpdateError("Neplatné číslo verzie.")
    m = VERSION_PATTERN.fullmatch(version)
    if m is None:
        raise UpdateError("Neplatné číslo verzie.")
    major, minor, patch, stage, num = m.groups()
    rank = {"test": 0, "beta": 1, "rc": 2, None: 3}
    return (int(major), int(minor), int(patch), rank[stage], int(num or 0))


def channel_for_version(version):
    version_key(version)
    return "testing" if VERSION_PATTERN.fullmatch(version).group(4) else "stable"


def expected_url(version):
    tag = "youtube-warder-v" + version.replace("~", "-")
    filename = PACKAGE + "_" + version.replace("~", ".") + "_all.ipk"
    return "https://github.com/" + REPO + "/releases/download/" + tag + "/" + filename


def parse_manifest(raw, current_version):
    try:
        doc = json.loads(raw)
    except (ValueError, TypeError, UnicodeError):
        raise UpdateError("Nesprávny aktualizačný manifest.")
    channel = channel_for_version(current_version)
    if (not isinstance(doc, dict) or type(doc.get("schema")) is not int
            or doc["schema"] != 1 or doc.get("product") != PRODUCT
            or doc.get("channel") != channel):
        raise UpdateError("Aktualizačný kanál alebo produkt nesúhlasí.")
    release = doc.get("release")
    if release is None:
        return None
    if not isinstance(release, dict):
        raise UpdateError("Nesprávny záznam aktualizácie.")
    version = release.get("version")
    version_key(version)
    if channel == "testing" and "~test" not in version:
        raise UpdateError("Nesprávna testovacia verzia.")
    if channel == "stable" and VERSION_PATTERN.fullmatch(version).group(4):
        raise UpdateError("Vývojová verzia v stabilnom kanáli.")
    if release.get("tag") != "youtube-warder-v" + version.replace("~", "-"):
        raise UpdateError("Nesprávne označenie vydania.")
    if release.get("url") != expected_url(version):
        raise UpdateError("Aktualizačný balík nie je z oficiálneho zdroja.")
    digest, size = release.get("sha256"), release.get("bytes")
    if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
        raise UpdateError("Chýba kontrolný súčet balíka.")
    if type(size) is not int or not 0 < size <= MAX_IPK:
        raise UpdateError("Neplatná veľkosť aktualizácie.")
    notes = release.get("notes", "")
    if not isinstance(notes, str) or len(notes) > 1000:
        raise UpdateError("Neplatný popis aktualizácie.")
    if version_key(version) <= version_key(current_version):
        return None
    return {"version": version, "sha256": digest, "bytes": size,
            "url": expected_url(version), "notes": notes}


def _open(url, timeout=8):
    request = Request(url, headers={"User-Agent": "WarderYouTubeUpdater/0.0.8",
                                   "Cache-Control": "no-cache"})
    return urlopen(request, timeout=timeout, context=ssl.create_default_context())


def check_update(current_version, opener=_open):
    channel = channel_for_version(current_version)
    target = FEED_TESTING if channel == "testing" else FEED_STABLE
    try:
        with opener(target, timeout=8) as response:
            raw = response.read(MAX_MANIFEST + 1)
    except (HTTPError, URLError, OSError):
        raise UpdateError("Nedá sa načítať aktualizačný manifest.")
    if len(raw) > MAX_MANIFEST:
        raise UpdateError("Aktualizačný manifest je príliš veľký.")
    return parse_manifest(raw, current_version)


def download_update(release, destination, opener=_open, progress=None):
    """Stream to a unique temporary file, reject partial/corrupted IPK."""
    path = Path(destination)
    sha = hashlib.sha256()
    total = 0
    try:
        with path.open("xb") as local:
            with opener(release["url"], timeout=15) as remote:
                while True:
                    chunk = remote.read(32768)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > release["bytes"] or total > MAX_IPK:
                        raise UpdateError("Balík je väčší než potvrdená veľkosť.")
                    sha.update(chunk)
                    local.write(chunk)
                    if progress:
                        progress("download", total, release["bytes"])
        if total != release["bytes"] or sha.hexdigest() != release["sha256"]:
            raise UpdateError("Kontrolný súčet alebo veľkosť balíka nesúhlasí.")
        return path
    except (HTTPError, URLError, OSError) as exc:
        path.unlink(missing_ok=True)
        raise UpdateError("Aktualizáciu sa nepodarilo stiahnuť.") from None
    except Exception:
        path.unlink(missing_ok=True)
        raise


def _ar_entries(data):
    if not data.startswith(b"!<arch>\n"):
        raise UpdateError("Balík nemá formát IPK.")
    i = 8
    entries = {}
    while i < len(data):
        if i + 60 > len(data):
            raise UpdateError("Nekompletný archív IPK.")
        h = data[i:i+60]
        if h[58:60] != b"\x60\n":
            raise UpdateError("Chybná hlavička IPK.")
        try:
            name = h[:16].decode("ascii").strip().rstrip("/")
            length = int(h[48:58].decode("ascii").strip())
        except (ValueError, UnicodeError):
            raise UpdateError("Neplatná hlavička IPK.")
        i += 60
        if name in entries or length < 0 or i + length > len(data):
            raise UpdateError("Neplatný obsah archívu IPK.")
        entries[name] = data[i:i+length]
        i += length + length % 2
    return entries


def validate_ipk(path, release):
    """Validate the exact package/architecture/version and all payload paths."""
    data = Path(path).read_bytes()
    if len(data) != release["bytes"] or hashlib.sha256(data).hexdigest() != release["sha256"]:
        raise UpdateError("Kontrolný súčet aktualizácie nesúhlasí.")
    entries = _ar_entries(data)
    if set(entries) != {"debian-binary", "control.tar.gz", "data.tar.gz"}:
        raise UpdateError("Balík IPK obsahuje nečakané archívy.")
    if entries["debian-binary"] != b"2.0\n":
        raise UpdateError("Neplatná verzia formátu IPK.")
    try:
        with tarfile.open(fileobj=io.BytesIO(entries["control.tar.gz"]), mode="r:gz") as control:
            ctrl = next((f for f in control if f.name.lstrip("./") == "control"), None)
            if ctrl is None or not ctrl.isfile() or ctrl.size > 8192:
                raise UpdateError("Chýbajú údaje balíka.")
            fields = {}
            for line in control.extractfile(ctrl).read().decode("utf-8").splitlines():
                if line and not line[0].isspace() and ":" in line:
                    key, val = line.split(":", 1)
                    if key in fields:
                        raise UpdateError("Duplicitný údaj balíka.")
                    fields[key] = val.strip()
        if (fields.get("Package") != PACKAGE or
                fields.get("Architecture") != "all" or
                fields.get("Version") != release["version"]):
            raise UpdateError("Balík nemá správny názov alebo verziu.")
        with tarfile.open(fileobj=io.BytesIO(entries["data.tar.gz"]), mode="r:gz") as content:
            members = content.getmembers()
            names = []
            for entry in members:
                name = entry.name
                if name.startswith("./"):
                    name = name[2:]
                if (not entry.isfile() or name.startswith("/") or
                        ".." in Path(name).parts or not name.startswith(PREFIX)
                        or not (name.endswith((".py", ".png"))
                                or name in (PREFIX + "youtube_engine/NOTICE",
                                            PREFIX + "youtube_engine/COPYING.GPLv2"))):
                    raise UpdateError("Balík obsahuje súbory mimo pluginu.")
                names.append(name)
            if len(names) != len(set(names)) or len(names) < 12:
                raise UpdateError("Balík je nekompletný.")
            for required in ("plugin.py", "update_core.py", "update_ui.py",
                             "images/plugin.png", "images/plugin_fhd.png",
                             "radio_streams.py", "youtube_engine/extractor.py",
                             "youtube_engine/jsinterp.py", "youtube_engine/NOTICE",
                             "youtube_engine/COPYING.GPLv2"):
                if PREFIX + required not in names:
                    raise UpdateError("Aktualizácia neobsahuje všetky súbory.")
    except (tarfile.TarError, UnicodeError, OSError):
        raise UpdateError("Poškodený archív IPK.")
    return True


def _installed_version(command_output):
    for paragraph in command_output.split("\n\n"):
        fields = {}
        for line in paragraph.splitlines():
            if ": " in line and not line[:1].isspace():
                key, value = line.split(": ", 1)
                fields[key] = value
        if fields.get("Package") == PACKAGE:
            return fields.get("Version"), fields.get("Status")
    return None, None


def install_update(release, opener=_open, runner=subprocess.run, progress=None):
    """Called only after confirmation, from a worker, never in a GUI callback."""
    with tempfile.TemporaryDirectory(prefix="warder-youtube-update-") as tmp:
        path = Path(tmp) / (PACKAGE + "_" + release["version"] + "_all.ipk")
        download_update(release, path, opener=opener, progress=progress)
        if progress:
            progress("verify", 0, 0)
        validate_ipk(path, release)
        if progress:
            progress("install", 0, 0)
        try:
            result = runner(
                ["opkg", "install", str(path)],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, timeout=180, check=False
            )
            if result.returncode:
                if result.returncode == 255:
                    # OpenATV opkg may refuse an already-installed IPK with
                    # code 255. A stale GUI module can still offer that same
                    # release after the package was upgraded. Check the
                    # installed package/version, never infer success from 255.
                    existing = runner(
                        ["opkg", "status", PACKAGE],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                        text=True, timeout=12, check=False
                    )
                    version, state = _installed_version(existing.stdout or "")
                    if (existing.returncode == 0 and version == release["version"]
                            and state is not None and
                            state.startswith("install ok installed")):
                        if progress:
                            progress("complete", release["bytes"], release["bytes"])
                        return version
                raise UpdateError("Inštalácia opkg skončila chybou (%d)." % result.returncode)
            status = runner(["opkg", "status", PACKAGE],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, timeout=12, check=False)
        except (OSError, subprocess.TimeoutExpired):
            raise UpdateError("Aktualizácia sa nemohla dokončiť.")
        if status.returncode:
            raise UpdateError("Nedá sa overiť nainštalovaná verzia.")
        version, state = _installed_version(status.stdout or "")
        if version != release["version"] or state is None or not state.startswith("install ok installed"):
            raise UpdateError("Aktualizácia sa nainštalovala neúplne.")
        if progress:
            progress("complete", release["bytes"], release["bytes"])
    return release["version"]
