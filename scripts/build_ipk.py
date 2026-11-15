#!/usr/bin/env python3
"""Build deterministic IPK from the checked-in plugin and CONTROL files."""
import gzip
import io
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "enigma2-plugin-extensions-youtube-warder-evolution"
SRC = ROOT / "plugin/Plugins/Extensions/WarderYouTube"
CTRL = ROOT / "packaging/CONTROL"
PREFIX = "usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube"

def tar_gz(items):
    plain = io.BytesIO()
    with tarfile.open(fileobj=plain, mode="w", format=tarfile.USTAR_FORMAT) as ar:
        for name, path, directory, executable in items:
            info = tarfile.TarInfo(name)
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ""
            info.mode = 0o755 if directory or executable else 0o644
            if directory:
                info.type = tarfile.DIRTYPE
                ar.addfile(info)
            else:
                content = path.read_bytes()
                info.size = len(content)
                ar.addfile(info, io.BytesIO(content))
    output = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=output, mode="wb", mtime=0, compresslevel=9) as gz:
        gz.write(plain.getvalue())
    return output.getvalue()

def member(archive, name, payload):
    header = (name + "/").ljust(16) + "0".ljust(12) + "0".ljust(6) + "0".ljust(6)
    header += "100644".ljust(8) + str(len(payload)).ljust(10) + "`\n"
    archive.write(header.encode("ascii"))
    archive.write(payload)
    if len(payload) % 2:
        archive.write(b"\n")

def main():
    fields = dict(line.split(": ", 1) for line in (CTRL / "control").read_text().splitlines() if ": " in line)
    assert fields["Package"] == PACKAGE and fields["Architecture"] == "all"
    control = tar_gz([(p.name, p, False, p.name != "control") for p in sorted(CTRL.iterdir()) if p.is_file()])
    base = Path(PREFIX)
    directories = [Path("usr"), Path("usr/lib"), Path("usr/lib/enigma2"), Path("usr/lib/enigma2/python"),
                   Path("usr/lib/enigma2/python/Plugins"), Path("usr/lib/enigma2/python/Plugins/Extensions"), base]
    files = [(p.as_posix(), None, True, False) for p in directories]
    for p in sorted(SRC.rglob("*")):
        rel = p.relative_to(SRC)
        dest = (base / rel).as_posix()
        if p.is_dir():
            files.append((dest, None, True, False))
        elif p.is_file() and "__pycache__" not in rel.parts and p.suffix not in (".pyc", ".pyo"):
            files.append((dest, p, False, p.name == "install_deps.sh"))
    binary = tar_gz(files)
    output = ROOT / (PACKAGE + "_" + fields["Version"] + "_all.ipk")
    archive = io.BytesIO()
    archive.write(b"!<arch>\n")
    for name, content in [("debian-binary", b"2.0\n"), ("control.tar.gz", control), ("data.tar.gz", binary)]:
        member(archive, name, content)
    output.write_bytes(archive.getvalue())
    print(output)

if __name__ == "__main__":
    main()
