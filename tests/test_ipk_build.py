"""Test test-only .ipk packaging and uninstall/install hook integrity."""
import importlib.util
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

P = Path(__file__).resolve().parents[1] / "tools/build_test_ipk.py"
spec = importlib.util.spec_from_file_location("warder_ipk_build", str(P))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def ar_parts(data):
    assert data.startswith(b"!<arch>\n")
    offset, parts = 8, {}
    while offset < len(data):
        header = data[offset:offset+60]
        name = header[:16].decode("ascii").strip().rstrip("/")
        size = int(header[48:58].decode("ascii").strip())
        if header[58:60] != b"\x60\n":
            raise ValueError("invalid ar header")
        offset += 60
        parts[name] = data[offset:offset+size]
        offset += size + size % 2
    return parts


class PackagingTests(unittest.TestCase):
    def test_ipk_contains_native_python_icons_and_hook_modes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = m.build(Path(temp))
            contents = path.read_bytes()
            self.assertTrue(m.SENSITIVE.search(contents) is None)
            parts = ar_parts(contents)
            self.assertEqual(set(parts), {"debian-binary", "control.tar.gz", "data.tar.gz"})
            self.assertEqual(parts["debian-binary"], b"2.0\n")
            with tarfile.open(fileobj=io.BytesIO(parts["control.tar.gz"]), mode="r:gz") as tar:
                names = {f.name: f for f in tar.getmembers()}
                self.assertTrue({"./control", "./preinst", "./postinst", "./prerm", "./postrm"}.issubset(names))
                self.assertEqual(names["./preinst"].mode, 0o755)
                self.assertEqual(names["./postrm"].mode, 0o755)
                control = tar.extractfile("./control").read().decode("utf-8")
                self.assertIn("Version: " + m.VERSION, control)
            with tarfile.open(fileobj=io.BytesIO(parts["data.tar.gz"]), mode="r:gz") as tar:
                members = tar.getmembers()
                self.assertGreaterEqual(len(members), 10)
                self.assertTrue(all(x.name.startswith("./" + m.TARGET_PREFIX + "/") for x in members))
                self.assertTrue(all(x.name.endswith((".py", ".png")) for x in members))
                self.assertEqual(len({x.name for x in members}), len(members))
                self.assertTrue(any(x.name.endswith("/plugin.py") for x in members))
                for icon, dimensions in (("plugin.png", (100, 60)), ("plugin_fhd.png", (150, 90))):
                    raw = tar.extractfile("./" + m.TARGET_PREFIX + "/images/" + icon).read()
                    self.assertTrue(raw.startswith(b"\x89PNG\r\n\x1a\n"))
                    self.assertEqual(tuple(int.from_bytes(raw[i:i + 4], "big") for i in (16, 20)), dimensions)

    def test_hooks_are_non_destructive(self):
        for name, script in m.control_scripts().items():
            self.assertTrue(script.startswith("#!/bin/sh"), name)
            self.assertIn("exit 0", script, name)
            for forbidden in ("opkg install", "opkg remove", "rm -rf", "init 4", "killall", "reboot"):
                self.assertNotIn(forbidden, script, name)


if __name__ == "__main__":
    unittest.main()
