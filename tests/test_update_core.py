"""Update channel/version guard regressions; no Enigma2 runtime required."""
import importlib.util
from pathlib import Path
import json
import unittest
SRC = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/update_core.py"
spec = importlib.util.spec_from_file_location("warder_test_update", SRC)
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)
class UpdateCoreTests(unittest.TestCase):
    def test_tilde_versions_and_tag(self):
        self.assertEqual(u.CURRENT_VERSION, "0.0.8~test3")
        self.assertEqual(u.channel_for_version(u.CURRENT_VERSION), "testing")
        self.assertLess(u.version_key("0.0.8~test2"), u.version_key("0.0.8~test3"))
        self.assertLess(u.version_key("0.0.8~test3"), u.version_key("0.0.8"))
        self.assertIn("/youtube-warder-v0.0.8-test3/", u.expected_url("0.0.8~test3"))
        self.assertIn("_0.0.8~test3_all.ipk", u.expected_url("0.0.8~test3"))
    def test_no_release_and_reject_unsigned(self):
        base = {"schema": 1, "product": u.PRODUCT, "channel": "testing", "release": None}
        self.assertIsNone(u.parse_manifest(json.dumps(base).encode(), u.CURRENT_VERSION))
        base["release"] = {"version": "0.0.8~test4"}
        with self.assertRaises(u.UpdateError):
            u.parse_manifest(json.dumps(base).encode(), u.CURRENT_VERSION)
if __name__ == "__main__":
    unittest.main()
