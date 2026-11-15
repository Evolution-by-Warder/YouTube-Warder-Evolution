"""Prevent shipping empty TV OAuth settings in a public stable IPK."""
import importlib.util
from pathlib import Path
import re
import unittest

SRC = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"
CLIENT_ID = re.compile(r"^[0-9A-Za-z._-]{8,200}\.apps\.googleusercontent\.com$")

class OAuthStableReleaseTests(unittest.TestCase):
    def test_tv_client_is_configured_but_user_tokens_are_not_bundled(self):
        source = (SRC / "oauth_app_config.py").read_text(encoding="utf-8")
        spec = importlib.util.spec_from_file_location("warder_oauth_release", SRC / "oauth_app_config.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(CLIENT_ID.fullmatch(module.OAUTH_TV_CLIENT_ID))
        self.assertIsInstance(module.OAUTH_TV_CLIENT_SECRET, str)
        self.assertTrue(module.OAUTH_TV_CLIENT_SECRET)
        self.assertNotIn("access_token", source)
        self.assertNotIn("refresh_token", source)
        self.assertNotIn("warderyoutube-oauth-token", source)

if __name__ == "__main__":
    unittest.main()
