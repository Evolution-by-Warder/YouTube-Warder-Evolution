"""Offline YouTube subscriptions tests; NO real Google credentials or network."""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load(module):
    spec = importlib.util.spec_from_file_location("_warder_subs_test_" + module, ROOT / (module + ".py"))
    item = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(item)
    return item


auth = load("subscriptions_auth")
api = load("subscriptions_api")
CLIENT = {"client_id": "12345678-abcdefghijklmnopqrstuvwx.apps.googleusercontent.com",
          "client_secret": "not-real-test-value"}
UC_A = "UC" + "a"*22
UC_B = "UC" + "b"*22


class Response(io.BytesIO):
    def __init__(self, data):
        super().__init__(json.dumps(data).encode("utf-8"))
    def close(self):
        super().close()


class AuthTests(unittest.TestCase):
    def test_no_real_secrets_are_bundled(self):
        self.assertFalse((ROOT / "warderyoutube-oauth-client.json").exists())
        self.assertEqual(auth.SCOPE, "https://www.googleapis.com/auth/youtube.readonly")
        self.assertIn("oauth2.googleapis.com", auth.DEVICE_URL)

    def test_private_tv_client_file(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "oauth.json"
            path.write_text(json.dumps(CLIENT), encoding="utf8")
            os.chmod(path, 0o600)
            self.assertEqual(auth.read_client(path), CLIENT)
            os.chmod(path, 0o644)
            with self.assertRaises(auth.SubscriptionsAuthError):
                auth.read_client(path)

    def test_google_device_code_is_validated_without_printing_tokens(self):
        seen = []
        def opener(req, timeout):
            seen.append(req)
            return Response({"device_code": "device-code-example",
                             "user_code": "ABCD-EFGH",
                             "verification_url": "https://www.google.com/device",
                             "expires_in": 900, "interval": 7})
        data = auth.request_device_code(CLIENT, opener)
        self.assertEqual(data["user_code"], "ABCD-EFGH")
        self.assertEqual(data["interval"], 7)
        self.assertIn(b"youtube.readonly", seen[0].data)
        self.assertNotIn(CLIENT["client_secret"].encode(), seen[0].data)

    def test_invalid_verification_domain_is_rejected(self):
        def evil(req, timeout):
            return Response({"device_code": "device-code-example",
                             "user_code": "ABCD",
                             "verification_uri": "https://not-google.example/device",
                             "expires_in": 900})
        with self.assertRaises(auth.SubscriptionsAuthError):
            auth.request_device_code(CLIENT, evil)

    def test_pending_and_slow_down(self):
        for expected in ("authorization_pending", "slow_down"):
            with self.subTest(expected=expected):
                status, token = auth.poll_device_code(
                    CLIENT, "device-example", opener=lambda r, timeout: Response({"error": expected}))
                self.assertEqual(status, expected)
                self.assertIsNone(token)

    def test_refresh_tokens_never_need_google_password(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "token.json"
            auth.save_tokens({"access_token": "expired", "refresh_token": "refresh",
                              "expires_at": 1}, path)
            requests = []
            def opener(req, timeout):
                requests.append(req)
                return Response({"access_token": "renewed", "expires_in": 3600, "scope": auth.SCOPE})
            result = auth.access_token(CLIENT, path, opener)
            self.assertEqual(result, "renewed")
            self.assertEqual(auth.access_token(CLIENT, path, opener), "renewed")
            self.assertEqual(len(requests), 1)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertTrue(auth.account_connected(path))
            auth.clear_tokens(path)
            self.assertFalse(auth.account_connected(path))


class ApiTests(unittest.TestCase):
    def test_all_channels_are_real_and_deduplicated(self):
        requested = []
        def opener(req, timeout):
            requested.append(req)
            query = parse_qs(urlsplit(req.full_url).query)
            self.assertEqual(query.get("mine"), ["true"])
            if len(requested) == 1:
                return Response({"items": [
                    {"snippet": {"title": "Channel A", "resourceId": {"channelId": UC_A}}},
                    {"snippet": {"title": "Channel A duplicate", "resourceId": {"channelId": UC_A}}},
                ], "nextPageToken": "next"})
            return Response({"items": [
                {"snippet": {"title": "Channel B", "resourceId": {"channelId": UC_B}}}
            ]})
        items = api.subscriptions_list("test-token", opener=opener)
        self.assertEqual([x["channel_id"] for x in items], [UC_A, UC_B])
        self.assertEqual(len(requested), 2)
        self.assertTrue(all("Authorization" in x.headers for x in requested))
        self.assertFalse(any("test-token" in x.full_url for x in requested))

    def test_recent_videos_use_real_uploads_playlists(self):
        requests = []
        def opener(req, timeout):
            requests.append(req)
            path = urlsplit(req.full_url).path
            if path.endswith("/subscriptions"):
                return Response({"items":[{"snippet":{
                    "title":"Artist A", "resourceId":{"channelId":UC_A}}}]})
            if path.endswith("/channels"):
                return Response({"items":[{"id":UC_A, "contentDetails":{
                    "relatedPlaylists":{"uploads": "UU" + "a"*22}}}]})
            if path.endswith("/playlistItems"):
                return Response({"items":[{"snippet":{
                    "title":"Latest song", "videoOwnerChannelTitle":"Artist A"},
                    "contentDetails":{"videoId":"abcdefghijk",
                    "videoPublishedAt":"2026-11-14T09:00:00Z"}}]})
            raise AssertionError("Unexpected Google endpoint")
        videos, channels = api.recent_subscription_videos("token", opener=opener)
        self.assertEqual(len(channels), 1)
        self.assertEqual(videos[0]["video_id"], "abcdefghijk")
        self.assertEqual(videos[0]["channel"], "Artist A")
        self.assertEqual(videos[0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")
        self.assertEqual(len(requests), 3)

    def test_channel_avatar_uses_only_youtube_image_cdn(self):
        sample = {"items":[{"snippet":{
            "title": "Music Channel",
            "resourceId": {"channelId": UC_A},
            "thumbnails": {"medium": {
                "url": "https://yt3.ggpht.com/channel-avatar-example"
            }}
        }}]}
        items = api.parse_subscriptions(sample)
        self.assertEqual(items[0]["thumbnail_url"],
                         "https://yt3.ggpht.com/channel-avatar-example")
        sample["items"][0]["snippet"]["thumbnails"]["medium"]["url"] = (
            "https://attacker.invalid/private-token"
        )
        self.assertEqual(api.parse_subscriptions(sample)[0]["thumbnail_url"], "")

    def test_channel_image_cache_allows_only_youtube_image_domains(self):
        spec = importlib.util.spec_from_file_location(
            "_warder_thumbnail_security_unit", ROOT / "thumbnails.py"
        )
        thumb = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(thumb)
        self.assertEqual(
            thumb.validate_thumbnail_url(
                "https://yt3.ggpht.com/abc_channel_avatar_123"
            ), "https://yt3.ggpht.com/abc_channel_avatar_123"
        )
        for url in (
            "http://yt3.ggpht.com/abc_channel_avatar_123",
            "https://yt3.ggpht.com.attacker.invalid/abc",
            "https://attacker.invalid/channel-avatar",
            "https://yt3.ggpht.com:666/abcd",
        ):
            with self.subTest(url=url):
                with self.assertRaises(thumb.ThumbnailError):
                    thumb.validate_thumbnail_url(url)

    def test_unauthorized_token_does_not_expose_request(self):
        with self.assertRaises(api.SubscriptionsApiError):
            api.subscriptions_list("", opener=lambda *a, **k: None)


if __name__ == "__main__":
    unittest.main()
