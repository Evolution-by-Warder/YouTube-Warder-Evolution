"""Owner-managed Enigma2 API key file must never be disclosed or auto-created."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "plugin/Plugins/Extensions/WarderYouTube/api_key_file.py"
spec = importlib.util.spec_from_file_location("warder_manual_api", MOD)
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class ManualKeyFileTests(unittest.TestCase):
    def test_absent_or_invalid_file_falls_back_safely(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "warderyoutube_api.key"
            self.assertEqual(api.read_manual_key(str(file)), "")
            file.write_text("invalid key with spaces\n", encoding="utf-8")
            file.chmod(0o600)
            self.assertEqual(api.read_manual_key(str(file)), "")
            file.write_text("A" * 300, encoding="ascii")
            self.assertEqual(api.read_manual_key(str(file)), "")

    def test_manual_0600_key_is_loaded_on_every_access(self):
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / "warderyoutube_api.key"
            one = "AIza" + "a" * 35
            two = "AIza" + "b" * 35
            file.write_text(one + "\n", encoding="ascii")
            file.chmod(0o600)
            self.assertEqual(api.read_manual_key(str(file)), one)
            file.write_text(two + "\n", encoding="ascii")
            self.assertEqual(api.read_manual_key(str(file)), two)

    def test_public_read_and_symlinks_are_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            actual = Path(d) / "real.key"
            actual.write_text("AIza" + "Z" * 35 + "\n", encoding="ascii")
            actual.chmod(0o644)
            self.assertEqual(api.read_manual_key(str(actual)), "")
            actual.chmod(0o600)
            link = Path(d) / "link.key"
            link.symlink_to(actual)
            self.assertEqual(api.read_manual_key(str(link)), "")
            self.assertEqual(api.read_manual_key(str(actual)), actual.read_text().strip())


if __name__ == "__main__":
    unittest.main()
