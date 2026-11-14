"""Mocked private Home browse protocol: no live credentials or network."""
import importlib.util
import json
from pathlib import Path
import re
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load():
    pkg = types.ModuleType("_warder_live")
    pkg.__path__ = [str(ROOT)]
    api = types.ModuleType("_warder_live.api")
    api.SearchError = type("SearchError", (Exception,), {})
    api.VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
    with patch.dict(sys.modules, {"_warder_live": pkg, "_warder_live.api": api}):
        spec = importlib.util.spec_from_file_location(
            "_warder_live.home_live_chips", ROOT / "home_live_chips.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    return mod


def response(logged_out=False):
    return {
        "responseContext": {
            "mainAppWebResponseContext": {"loggedOut": logged_out}
        },
        "contents": {"twoColumnBrowseResultsRenderer": {"tabs": [
            {"tabRenderer": {"content": {"richGridRenderer": {
                "header": {"feedFilterChipBarRenderer": {"contents": [
                    {"chipCloudChipRenderer": {
                        "text": {"simpleText": "Všetko"}, "isSelected": True}},
                    {"chipCloudChipRenderer": {
                        "text": {"runs": [{"text": "Hudba"}]},
                        "navigationEndpoint": {
                            "continuationCommand": {"token": "SERVER_MUSIC"}}}},
                    {"chipCloudChipRenderer": {
                        "text": {"simpleText": "Mixy"},
                        "navigationEndpoint": {
                            "continuationCommand": {"token": "SERVER_MIXES"}}}},
                    {"chipCloudChipRenderer": {
                        "text": {"simpleText": "Domáci majstri"},
                        "navigationEndpoint": {"browseEndpoint": {
                            "browseId": "FEwhat_to_watch",
                            "params": "SERVER_DIY"}}}},
                ]}},
                "contents": [{"richItemRenderer": {"content": {"videoRenderer": {
                    "videoId": "abcdefghijk",
                    "title": {"runs": [{"text": "Real &amp; Personal"}]},
                    "ownerText": {"simpleText": "Creator"},
                }}}}],
            }}}}
        ]}},
    }


class FakeResponse:
    def __init__(self, data):
        self.body = json.dumps(data).encode("utf-8")
    def read(self, size):
        return self.body[:size]
    def close(self):
        pass


class LiveYouTubeHomeTests(unittest.TestCase):
    def test_server_order_exact_text_and_videos(self):
        mod = load()
        result = mod.parse_live_home(response())
        self.assertEqual([chip["label"] for chip in result["chips"]],
                         ["Všetko", "Hudba", "Mixy", "Domáci majstri"])
        self.assertEqual(result["chips"][1]["continuation"], "SERVER_MUSIC")
        self.assertEqual(result["chips"][3]["params"], "SERVER_DIY")
        self.assertEqual(result["videos"][0]["title"], "Real & Personal")

    def test_unauthenticated_public_home_never_claimed_personal(self):
        mod = load()
        for data in (response(True), {"responseContext": {}, "contents": {}}):
            with self.assertRaises(mod.SearchError):
                mod.parse_live_home(data)

    def test_read_only_bearer_header_and_exact_server_filter(self):
        mod = load()
        seen = []
        def opener(request, timeout):
            seen.append((request, json.loads(request.data)))
            return FakeResponse(response())
        mod.live_home("test-access-token-123456", opener=opener)
        self.assertEqual(seen[0][1]["browseId"], "FEwhat_to_watch")
        self.assertTrue(seen[0][0].get_header("Authorization").startswith("Bearer "))
        self.assertNotIn("test-access-token", seen[0][0].full_url)
        chip = {"kind": "live", "continuation": "SERVER_MUSIC"}
        rows = mod.live_category_videos(chip, "test-access-token-123456",
                                        opener=opener)
        self.assertEqual(rows[0]["video_id"], "abcdefghijk")
        self.assertEqual(seen[1][1]["continuation"], "SERVER_MUSIC")
        self.assertNotIn("browseId", seen[1][1])

    def test_no_available_server_chip_fails_instead_of_inventing_topics(self):
        mod = load()
        payload = response()
        payload["contents"] = {"videoRenderer": {
            "videoId": "abcdefghijk", "title": {"simpleText": "Video"}}}
        with self.assertRaises(mod.SearchError):
            mod.parse_live_home(payload)

    def test_filter_result_need_not_repeat_chip_bar(self):
        mod = load()
        result = {"onResponseReceivedActions": [
            {"appendContinuationItemsAction": {"continuationItems": [
                {"videoRenderer": {
                    "videoId": "abcdefghijk",
                    "title": {"simpleText": "Filtered video"}}}]}}]}
        self.assertEqual(mod.parse_live_videos(result)[0]["title"],
                         "Filtered video")


if __name__ == "__main__":
    unittest.main()
