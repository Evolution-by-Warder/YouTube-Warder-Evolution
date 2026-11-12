"""Tests for the self-contained Warder Radio YouTube candidate adapter."""
from pathlib import Path
import sys
import types
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

    def test_reject_url_and_quality(self):
        for u in ("http://rr1.googlevideo.com/video",
                  "https://rr1.googlevideo.com.attacker.example/",
                  "file:///etc/passwd",
                  "https://localhost/video",
                  "https://user:pass@rr1.googlevideo.com/"):
            with self.assertRaises(ValueError):
                radio_streams.allowed_origin(u,media=True)
        with self.assertRaises(ValueError):
            radio_streams.extract_candidates("abcdefghijk",quality="1080",
                       resolver_factory=FakeResolver,transport_factory=FakeNetwork)
        with self.assertRaises(Exception):
            radio_streams.extract_candidates("bad-id",quality="720",
                       resolver_factory=FakeResolver,transport_factory=FakeNetwork)

if __name__ == "__main__":
    unittest.main()
