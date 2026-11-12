"""Static source tests: playback remains separate from networking and GUI."""
import ast
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "plugin/Plugins/Extensions/WarderYouTube"


class PlaybackSourceTests(unittest.TestCase):
    def test_all_sources_syntax(self):
        for path in PKG.glob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_native_movieplayer_restoration(self):
        source = (PKG / "player.py").read_text(encoding="utf-8")
        self.assertIn("fromMovieSelection=False", source)
        self.assertIn("eServiceReference", source)
        self.assertIn("SERVICE_TYPE_GSTREAMER = 4097", source)
        self.assertNotIn("subprocess", source)
        self.assertNotIn("urlopen", source)

    def test_background_ytdlp_and_lifecycle(self):
        source = (PKG / "search.py").read_text(encoding="utf-8")
        self.assertIn("deferToThread(resolve_video_url", source)
        self.assertIn("self.request_version", source)
        self.assertIn("self.closed", source)
        self.assertIn("on_close=self.playback_finished", source)

    def test_no_bundled_extractor_or_credentials(self):
        source = (PKG / "resolver.py").read_text(encoding="utf-8")
        self.assertIn("--ignore-config", source)
        self.assertIn("subprocess.run", source)
        self.assertNotIn("os.system(", source)
        self.assertNotIn("shell=True", source)


if __name__ == "__main__":
    unittest.main()
