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
                self.assertTrue(all(x.name.endswith((".py", ".png", "/NOTICE", "/COPYING.GPLv2")) for x in members))
                self.assertTrue(any(x.name.endswith("/youtube_engine/extractor.py") for x in members))
                self.assertTrue(any(x.name.endswith("/youtube_engine/COPYING.GPLv2") for x in members))
                self.assertEqual(len({x.name for x in members}), len(members))
                self.assertTrue(any(x.name.endswith("/plugin.py") for x in members))
                for icon, dimensions in (("plugin.png", (100, 60)), ("plugin_fhd.png", (150, 90))):
                    raw = tar.extractfile("./" + m.TARGET_PREFIX + "/images/" + icon).read()
                    self.assertTrue(raw.startswith(b"\x89PNG\r\n\x1a\n"))
                    self.assertEqual(tuple(int.from_bytes(raw[i:i + 4], "big") for i in (16, 20)), dimensions)

                # Native PNG menu symbols and transparent selection frames
                # are real IPK members, not just concept artwork.
                accent_names = [("nav_%d.png" % i, (64, 64)) for i in range(8)]
                accent_names += [("nav_focus.png", (328, 72)),
                                 ("video_focus.png", (477, 324)),
                                 ("grid_focus.png", (491, 364))]
                for icon, dimensions in accent_names:
                    raw = tar.extractfile("./" + m.TARGET_PREFIX + "/images/" + icon).read()
                    self.assertEqual(raw[:8], b"\x89PNG\r\n\x1a\n")
                    self.assertEqual(tuple(int.from_bytes(raw[i:i+4], "big")
                                           for i in (16, 20)), dimensions)
                    self.assertEqual(raw[25], 6)  # RGBA, alpha transparency

    def test_video_focus_frames_are_transparent_inside_and_bright_on_edge(self):
        import zlib
        # The selected border must pop against dark, one/two-pixel static
        # borders, without covering actual YouTube thumbnails.
        from importlib.util import spec_from_file_location, module_from_spec
        art_path = P.parent / "warder_nav_art.py"
        spec = spec_from_file_location("_focus_art_test", art_path)
        art = module_from_spec(spec)
        spec.loader.exec_module(art)
        for render, dims in (
            (art.render_video_focus, (477, 324)),
            (art.render_grid_focus, (491, 364))
        ):
            raw = render()
            self.assertEqual(raw[25], 6)
            self.assertEqual((int.from_bytes(raw[16:20], "big"),
                              int.from_bytes(raw[20:24], "big")), dims)
            offset = 8
            compressed = bytearray()
            while offset < len(raw):
                length = int.from_bytes(raw[offset:offset+4], "big")
                chunk = raw[offset+4:offset+8]
                if chunk == b"IDAT":
                    compressed.extend(raw[offset+8:offset+8+length])
                offset += length+12
                if chunk == b"IEND":
                    break
            pixels = zlib.decompress(bytes(compressed))
            row_size = dims[0]*4+1
            self.assertTrue(all(pixels[i*row_size] == 0 for i in range(dims[1])))
            def at(x, y):
                base = y*row_size+1+x*4
                return pixels[base:base+4]
            border = at(0, dims[1]//2)
            inside = at(dims[0]//2, dims[1]//2)
            self.assertGreater(border[0], 140)
            self.assertGreater(border[1], 220)
            self.assertEqual(border[3], 255)
            self.assertEqual(inside[3], 0)

    def test_displayed_version_matches_control_package(self):
        """Prevent the Home header and opkg control version from drifting."""
        from ast import parse, Assign, Name, Constant
        core_path = (P.parent.parent /
                     "plugin/Plugins/Extensions/WarderYouTube/update_core.py")
        tree = parse(core_path.read_text(encoding="utf-8"))
        values = [
            node.value.value for node in tree.body
            if isinstance(node, Assign)
            and isinstance(node.value, Constant)
            and any(isinstance(target, Name) and target.id == "CURRENT_VERSION"
                    for target in node.targets)
        ]
        self.assertEqual(values, [m.VERSION])

    def test_hooks_are_non_destructive(self):
        for name, script in m.control_scripts().items():
            self.assertTrue(script.startswith("#!/bin/sh"), name)
            self.assertIn("exit 0", script, name)
            for forbidden in ("opkg install", "opkg remove", "rm -rf", "init 4", "killall", "reboot"):
                self.assertNotIn(forbidden, script, name)


if __name__ == "__main__":
    unittest.main()
