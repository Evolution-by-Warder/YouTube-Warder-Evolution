"""Tests for the self-contained Warder Radio YouTube candidate adapter."""
from pathlib import Path
import sys
import types
import threading
import time
import unittest

EXT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions"
sys.path.insert(0, str(EXT))
from WarderYouTube import radio_streams


class FakeNetwork:
    def page(self,*args,**kwargs):
        raise AssertionError("Network I/O must not be used with fake resolver")


class FakeResolver:
    def __init__(self):
        self.playback_urls=[]
    def extract(self,video_id):
        self.playback_urls=[
            "https://manifest.googlevideo.com/master.m3u8",
            "https://rr1.googlevideo.com/uhd&suburi=https://rr2.googlevideo.com/audio",
            "https://rr1.googlevideo.com/hd&suburi=https://attacker.example/audio",
            "https://rr1.googlevideo.com/sd"
        ]
        return self.playback_urls[0]


class RadioEngineIntegrationTests(unittest.TestCase):
    def test_4097_and_registered_5002_candidates(self):
        result=radio_streams.extract_candidates("abcdefghijk",quality="720",dash=True,
                          resolver_factory=FakeResolver,transport_factory=FakeNetwork)
        self.assertEqual([x["service_type"] for x in result],[4097,5002,4097])
        self.assertEqual(len(result),3)
        self.assertFalse(any("attacker" in x["url"] for x in result))

    def test_dash_never_leaks_without_backend(self):
        result=radio_streams.extract_candidates("abcdefghijk",quality="360",dash=False,
                          resolver_factory=FakeResolver,transport_factory=FakeNetwork)
        self.assertEqual(len(result),2)
        self.assertTrue(all(x["service_type"]==4097 for x in result))

    def test_parallel_quality_requests_do_not_mix_settings(self):
        from WarderYouTube.youtube_engine.settings import config
        results = []
        errors = []
        initial = config.plugins.YouTube.maxResolution.value

        def worker(quality, expected):
            class Resolver:
                playback_urls = []
                def extract(self, video_id):
                    before = config.plugins.YouTube.maxResolution.value
                    time.sleep(0.02)
                    after = config.plugins.YouTube.maxResolution.value
                    results.append((expected, before, after))
                    return "https://rr1.googlevideo.com/video"
            try:
                radio_streams.extract_candidates("abcdefghijk", quality=quality,
                    resolver_factory=Resolver, transport_factory=FakeNetwork)
            except Exception as exc:
                errors.append(str(type(exc)))

        one = threading.Thread(target=worker, args=("360", "18"))
        two = threading.Thread(target=worker, args=("720", "22"))
        one.start(); two.start()
        one.join(timeout=2); two.join(timeout=2)
        self.assertFalse(one.is_alive() or two.is_alive())
        self.assertEqual(errors, [])
        self.assertCountEqual([x[0] for x in results], ["18", "22"])
        self.assertTrue(all(expected == before == after for expected, before, after in results))
        self.assertEqual(config.plugins.YouTube.maxResolution.value, initial)

    def test_resolver_exception_restores_original_quality(self):
        from WarderYouTube.youtube_engine.settings import config
        initial = config.plugins.YouTube.maxResolution.value
        class BrokenResolver:
            playback_urls = []
            def extract(self, video_id):
                raise RuntimeError("test-only failure")
        with self.assertRaises(RuntimeError):
            radio_streams.extract_candidates("abcdefghijk", quality="360",
                resolver_factory=BrokenResolver, transport_factory=FakeNetwork)
        self.assertEqual(config.plugins.YouTube.maxResolution.value, initial)

    def test_4k_quality_uses_best_available_lower_dash_height(self):
        from WarderYouTube.youtube_engine.extractor import YouTubeVideoUrl, PRIORITY_VIDEO_FORMAT
        from WarderYouTube.youtube_engine.settings import config
        resolver = YouTubeVideoUrl.__new__(YouTubeVideoUrl)
        resolver.use_dash_mp4 = ()
        initial = config.plugins.YouTube.maxHeight.value
        samples = [
            {"itag": "313", "height": 2160, "mimeType": "video/mp4; codecs=avc1"},
            {"itag": "137", "height": 1080, "mimeType": "video/mp4; codecs=avc1"},
            {"itag": "136", "height": 720, "mimeType": "video/mp4; codecs=avc1"},
        ]
        try:
            config.plugins.YouTube.maxHeight.value = 2160
            available = resolver._sort_formats(PRIORITY_VIDEO_FORMAT, samples)
            self.assertEqual(available[0]["height"], 2160)
            without_4k = resolver._sort_formats(PRIORITY_VIDEO_FORMAT, samples[1:])
            self.assertEqual(without_4k[0]["height"], 1080)
            config.plugins.YouTube.maxHeight.value = 1080
            capped = resolver._sort_formats(PRIORITY_VIDEO_FORMAT, samples)
            self.assertEqual(capped[0]["height"], 1080)
            self.assertTrue(all(entry["height"] <= 1080 for entry in capped))
        finally:
            config.plugins.YouTube.maxHeight.value = initial

    def test_reject_url_and_quality(self):
        for u in ("http://rr1.googlevideo.com/video",
                  "https://rr1.googlevideo.com.attacker.example/",
                  "file:///etc/passwd",
                  "https://localhost/video",
                  "https://user:pass@rr1.googlevideo.com/"):
            with self.assertRaises(ValueError):
                radio_streams.allowed_origin(u,media=True)
        with self.assertRaises(ValueError):
            radio_streams.extract_candidates("abcdefghijk",quality="4320",
                       resolver_factory=FakeResolver,transport_factory=FakeNetwork)
        with self.assertRaises(Exception):
            radio_streams.extract_candidates("bad-id",quality="720",
                       resolver_factory=FakeResolver,transport_factory=FakeNetwork)

if __name__ == "__main__":
    unittest.main()
