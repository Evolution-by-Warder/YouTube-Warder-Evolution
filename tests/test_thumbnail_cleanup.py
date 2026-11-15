"""Regression coverage for continuous /tmp thumbnail housekeeping."""
import importlib.util
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

SOURCE = (Path(__file__).resolve().parents[1] /
          "plugin/Plugins/Extensions/WarderYouTube/thumbnails.py")
spec = importlib.util.spec_from_file_location("_warder_thumbnail_cleanup", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ThumbnailCleanupTests(unittest.TestCase):
    def test_prunes_expired_and_abandoned_but_preserves_fresh(self):
        with tempfile.TemporaryDirectory() as temp:
            fresh = Path(temp) / ("a" * 64 + ".jpg")
            expired = Path(temp) / ("b" * 64 + ".jpg")
            partial = Path(temp) / "tmpabandoned.partial"
            unrelated = Path(temp) / "other-app.log"
            for f in (fresh, expired, partial, unrelated):
                f.write_bytes(b"data")
            now = time.time()
            os.utime(expired, (now-4000, now-4000))
            os.utime(partial, (now-4000, now-4000))
            mod._prune(temp)
            self.assertTrue(fresh.exists())
            self.assertFalse(expired.exists())
            self.assertFalse(partial.exists())
            self.assertTrue(unrelated.exists())

    def test_enforces_count_on_active_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            for n in range(mod.MAX_CACHE_FILES + 5):
                (Path(temp) / ("%064x.jpg" % n)).write_bytes(b"small")
            mod._prune(temp)
            self.assertEqual(len(list(Path(temp).glob("*.jpg"))), mod.MAX_CACHE_FILES)

    def test_final_cleanup_does_not_remove_unowned_items(self):
        with tempfile.TemporaryDirectory() as temp:
            owned = Path(temp) / ("f" * 64 + ".png")
            unrelated = Path(temp) / "not-a-warder-file"
            owned.write_bytes(b"image")
            unrelated.write_bytes(b"preserve")
            mod.cleanup_cache(temp)
            self.assertFalse(owned.exists())
            self.assertTrue(unrelated.exists())

    def test_follows_no_directory_symlink(self):
        with tempfile.TemporaryDirectory() as outer:
            real = Path(outer) / "real"
            real.mkdir()
            img = real / ("a" * 64 + ".jpg")
            img.write_bytes(b"other data")
            link = Path(outer) / "alias"
            link.symlink_to(real, target_is_directory=True)
            mod.cleanup_cache(str(link))
            mod._prune(str(link))
            self.assertTrue(img.exists())

    def test_accessing_cached_image_also_triggers_prune(self):
        class NoNetwork:
            def __call__(self, *args, **kwargs):
                raise AssertionError("Cached image must avoid re-download")
        url = "https://i.ytimg.com/vi/abcdef12345/mqdefault.jpg"
        import hashlib
        name = hashlib.sha256(url.encode("utf-8")).hexdigest()
        with tempfile.TemporaryDirectory() as temp:
            image = Path(temp) / (name + ".jpg")
            image.write_bytes(b"image")
            expired = Path(temp) / ("b" * 64 + ".jpg")
            expired.write_bytes(b"stale")
            now = time.time()
            os.utime(expired, (now-4000, now-4000))
            result = mod.fetch_thumbnail(url, opener=NoNetwork(), cache_dir=temp)
            self.assertEqual(result, str(image))
            self.assertFalse(expired.exists())


if __name__ == "__main__":
    unittest.main()
