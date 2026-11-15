"""Anonymous YouTube website feed parsing without credentials or receiver."""
import importlib.util
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load():
    pkg = types.ModuleType("_warder_public")
    pkg.__path__ = [str(ROOT)]
    api = types.ModuleType("_warder_public.api")
    api.SearchError = type("SearchError", (Exception,), {})
    api.VIDEO_ID = __import__("re").compile(r"^[a-zA-Z0-9_-]{11}$")
    api.MAX_RESPONSE_BYTES = 1_000_000
    with patch.dict(sys.modules, {"_warder_public": pkg, "_warder_public.api": api}):
        spec = importlib.util.spec_from_file_location(
            "_warder_public.home_feed", str(ROOT / "home_feed.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod


class FakeResponse:
    def __init__(self, body):
        self.body = body
        self.closed = False

    def read(self, count):
        return self.body[:count]

    def geturl(self):
        return "https://www.youtube.com/"

    def close(self):
        self.closed = True


class PublicFeedTests(unittest.TestCase):
    def test_nested_home_video_cards_deduped_and_bounded(self):
        mod = load()
        payload = {
            "contents": [{"videoRenderer": {
                "videoId": "abcdefghijk",
                "title": {"runs": [{"text": "Public &amp; Popular"}]},
                "ownerText": {"runs": [{"text": "SK Creator"}]}
            }}, {"videoRenderer": {"videoId": "abcdefghijk", "title": {"simpleText": "Duplicate"}}},
                {"gridVideoRenderer": {
                    "videoId": "01234567890", "title": {"simpleText": "Another real video"}}},
                {"videoRenderer": {"videoId": "bad", "title": {"simpleText": "Invalid"}}}]
        }
        html = "<html><script>var ytInitialData = " + json.dumps(payload) + ";</script></html>"
        videos = mod.parse_public_home(html)
        self.assertEqual(len(videos), 2)
        self.assertEqual(videos[0]["title"], "Public & Popular")
        self.assertEqual(videos[0]["channel"], "SK Creator")
        self.assertEqual(videos[0]["thumbnail_url"],
                         "https://i.ytimg.com/vi/abcdefghijk/mqdefault.jpg")

    def test_missing_data_fails_cleanly(self):
        mod = load()
        for text in ("<html></html>", "ytInitialData = {broken", "ytInitialData = {}"):
            with self.subTest(text=text):
                with self.assertRaises(mod.SearchError):
                    mod.parse_public_home(text)

    def test_real_public_request_uses_no_key_or_account(self):
        mod = load()
        payload = {"contents": [{"videoRenderer": {
            "videoId": "abcdefghijk", "title": {"simpleText": "Real card"},
            "ownerText": {"simpleText": "Channel"}
        }}]}
        web = ("ytInitialData = " + json.dumps(payload) + ";").encode()
        captured = []
        def opener(req, timeout):
            captured.append((req.full_url, timeout, req.headers))
            return FakeResponse(web)
        videos = mod.public_home_videos(opener=opener)
        self.assertEqual(len(videos), 1)
        self.assertEqual(len(captured), 1)
        self.assertIn("youtube.com", captured[0][0])
        self.assertNotIn("key=", captured[0][0].lower())
        self.assertNotIn("Authorization", captured[0][2])


    def test_anonymous_home_without_recommendations_falls_back_to_search(self):
        mod = load()
        calls = []
        valid = {"contents": [{"videoRenderer": {
            "videoId": "01234567890", "title": {"simpleText": "Real search result"},
            "ownerText": {"simpleText": "SK channel"}
        }}]}
        class Response(FakeResponse):
            def __init__(self, body, url):
                super().__init__(body)
                self.url = url
            def geturl(self):
                return self.url
        def opener(req, timeout):
            calls.append(req)
            if len(calls) == 1:
                return Response(b"<html>ytInitialData = {}</html>", req.full_url)
            return Response(("ytInitialData = " + json.dumps(valid) + ";").encode(),
                            req.full_url)
        items = mod.public_home_videos(opener=opener)
        self.assertEqual([x["video_id"] for x in items], ["01234567890"])
        self.assertEqual(len(calls), 2)
        self.assertIn("search_query=", calls[1].full_url)
        for request in calls:
            self.assertNotIn("Authorization", request.headers)
            self.assertNotIn("key=", request.full_url)

    def test_anonymous_categories_use_real_public_search_without_account(self):
        mod = load()
        urls = []
        data = {"contents": [{"videoRenderer": {
            "videoId": "abcdefghijk", "title": {"simpleText": "Music video"}
        }}]}
        def opener(req, timeout):
            urls.append(req.full_url)
            return FakeResponse(("ytInitialData = " + json.dumps(data) + ";").encode())
        items = mod.public_category_videos("10", opener=opener)
        self.assertEqual(items[0]["title"], "Music video")
        self.assertEqual(len(urls), 1)
        self.assertIn("search_query=", urls[0])
        self.assertIn("youtube.com/results", urls[0])
        with self.assertRaises(mod.SearchError):
            mod.public_category_videos("999", opener=opener)
        self.assertEqual(len(urls), 1)


    def test_public_continuation_loads_actual_next_page_without_account(self):
        mod = load()
        key = "A" * 39
        initial = {"contents": [
            {"videoRenderer": {"videoId": "abcdefghijk", "title": {"simpleText": "First"}}},
            {"continuationItemRenderer": {"continuationEndpoint": {
                "continuationCommand": {"token": "first-page-cursor"}}}}
        ]}
        html = ('<script>ytcfg.set({"INNERTUBE_API_KEY":"' + key +
                '","INNERTUBE_CLIENT_VERSION":"2.20261115.00.00"});</script>' +
                '<script>var ytInitialData = ' + json.dumps(initial) + ';</script>')
        next_payload = {"onResponseReceivedCommands": [{
            "appendContinuationItemsAction": {"continuationItems": [
                {"videoRenderer": {"videoId": "01234567890",
                                   "title": {"simpleText": "Second"}}},
                {"continuationItemRenderer": {"continuationEndpoint": {
                    "continuationCommand": {"token": "second-page-cursor"}}}}
            ]}}]}
        class Response(FakeResponse):
            def __init__(self, body, url):
                super().__init__(body)
                self.url = url
            def geturl(self):
                return self.url
        requests = []
        def opener(req, timeout):
            requests.append(req)
            if len(requests) == 1:
                return Response(html.encode(), req.full_url)
            return Response(json.dumps(next_payload).encode(), req.full_url)
        first = mod.public_category_page("25", opener=opener)
        self.assertEqual([x["title"] for x in first["items"]], ["First"])
        self.assertTrue(first["next_page_token"])
        second = mod.public_category_page("25", page_token=first["next_page_token"],
                                          opener=opener)
        self.assertEqual([x["title"] for x in second["items"]], ["Second"])
        self.assertTrue(second["next_page_token"])
        body = json.loads(requests[1].data.decode())
        self.assertEqual(body["continuation"], "first-page-cursor")
        self.assertEqual(body["context"]["client"]["clientName"], "WEB")
        self.assertIn("/youtubei/v1/search", requests[1].full_url)
        self.assertNotIn("Authorization", requests[1].headers)

    def test_every_home_category_can_load_first_and_next_anonymous_page(self):
        """All 14 category identifiers, including All, use the same cursor."""
        mod = load()
        category_ids = {"0", "1", "10", "15", "17", "19", "20",
                        "22", "23", "24", "25", "26", "27", "28"}
        self.assertEqual(set(mod.PUBLIC_QUERIES), category_ids)
        self.assertEqual(len(category_ids), 14)
        key = "B" * 39
        for category_id in sorted(category_ids):
            with self.subTest(category=category_id):
                html = ('ytcfg.set({"INNERTUBE_API_KEY":"' + key +
                        '","INNERTUBE_CLIENT_VERSION":"2.20261115.00.00"});' +
                        'var ytInitialData = ' + json.dumps({"contents": [
                            {"videoRenderer": {
                                "videoId": "abcdefghijk",
                                "title": {"simpleText": "First video"}}},
                            {"continuationItemRenderer": {"continuationEndpoint": {
                                "continuationCommand": {"token": "NEXTTOKEN"}}}}
                        ]}) + ';')
                follow = {"onResponseReceivedCommands": [{
                    "appendContinuationItemsAction": {"continuationItems": [
                        {"videoRenderer": {
                            "videoId": "01234567890",
                            "title": {"simpleText": "Second video"}}}
                    ]}}]}
                class Response(FakeResponse):
                    def __init__(self, data, url):
                        super().__init__(data)
                        self.url = url
                    def geturl(self):
                        return self.url
                calls = []
                def opener(request, timeout):
                    calls.append(request)
                    if category_id == "0" and len(calls) == 1:
                        # Anonymous Home can be empty; fallback to public search.
                        return Response(b"ytInitialData = {};", request.full_url)
                    if request.data is None:
                        return Response(html.encode(), request.full_url)
                    return Response(json.dumps(follow).encode(), request.full_url)
                first = mod.public_category_page(category_id, opener=opener)
                self.assertEqual(first["pagination_state"], "ready")
                self.assertTrue(first["next_page_token"])
                nxt = mod.public_category_page(
                    category_id, page_token=first["next_page_token"],
                    opener=opener)
                self.assertEqual(nxt["items"][0]["video_id"], "01234567890")
                self.assertEqual(json.loads(calls[-1].data)["continuation"],
                                 "NEXTTOKEN")
                self.assertTrue(all(
                    "Authorization" not in call.headers for call in calls))

    def test_all_home_recommendations_use_browse_continuation(self):
        mod = load()
        data = {"contents": [
            {"videoRenderer": {"videoId": "abcdefghijk",
                               "title": {"simpleText": "From Home"}}},
            {"continuationItemRenderer": {"continuationEndpoint": {
                "continuationCommand": {"token": "HOME_NEXT"}}}}
        ]}
        html = ('ytcfg.set({"INNERTUBE_API_KEY":"' + "A" * 39 +
                '","INNERTUBE_CLIENT_VERSION":"2.20261115.00.00"});' +
                'var ytInitialData = ' + json.dumps(data) + ';')
        requests = []
        class Response(FakeResponse):
            def __init__(self, raw, target):
                super().__init__(raw)
                self.target = target
            def geturl(self):
                return self.target
        def opener(req, timeout):
            requests.append(req)
            if len(requests) == 1:
                return Response(html.encode(), req.full_url)
            return Response(json.dumps({"contents": [
                {"videoRenderer": {"videoId": "01234567890",
                                   "title": {"simpleText": "Further Home"}}}
            ]}).encode(), req.full_url)
        first = mod.public_category_page("0", opener=opener)
        self.assertEqual(first["pagination_state"], "ready")
        second = mod.public_category_page("0", page_token=first["next_page_token"],
                                          opener=opener)
        self.assertIn("/youtubei/v1/browse", requests[-1].full_url)
        self.assertEqual(second["items"][0]["title"], "Further Home")

    def test_missing_pagination_metadata_is_reported_not_claimed_as_end(self):
        mod = load()
        initial = {"contents": [
            {"videoRenderer": {"videoId": "abcdefghijk",
                               "title": {"simpleText": "First"}}},
            {"continuationItemRenderer": {"continuationEndpoint": {
                "continuationCommand": {"token": "MORE"}}}}
        ]}
        page = ("ytInitialData = " + json.dumps(initial) + ";").encode()
        first = mod.public_category_page(
            "25", opener=lambda req, timeout: FakeResponse(page))
        self.assertEqual(len(first["items"]), 1)
        self.assertEqual(first["next_page_token"], "")
        self.assertEqual(first["pagination_state"], "missing_web_client")

    def test_all_categories_continue_when_youtube_omits_web_cursor(self):
        mod = load()
        self.assertEqual(len(mod.PUBLIC_QUERIES), 14)
        for category in sorted(mod.PUBLIC_QUERIES):
            with self.subTest(category=category):
                requests = []
                class Response(FakeResponse):
                    def __init__(self, data, target):
                        super().__init__(data)
                        self.target = target
                    def geturl(self):
                        return self.target
                def opener(req, timeout):
                    requests.append(req)
                    # First anonymous Home response is empty; search is real.
                    if category == "0" and len(requests) == 1:
                        return Response(b"ytInitialData = {};", req.full_url)
                    video = ("abcdefghijk" if len(requests) <=
                             (2 if category == "0" else 1) else "01234567890")
                    data = {"contents": [{"videoRenderer": {
                        "videoId": video,
                        "title": {"simpleText": "Real public video"}}}]}
                    body = ("ytInitialData = " + json.dumps(data) + ";").encode()
                    return Response(body, req.full_url)
                first = mod.public_category_page(category, opener=opener)
                self.assertEqual(len(first["items"]), 1)
                self.assertTrue(first["next_page_token"])
                self.assertIn(first["pagination_state"],
                              ("missing_continuation", "missing_web_client"))
                second = mod.public_category_page(
                    category, page_token=first["next_page_token"], opener=opener)
                self.assertEqual(len(second["items"]), 1)
                self.assertEqual(second["items"][0]["video_id"], "01234567890")
                self.assertIn("search_query=", requests[-1].full_url)
                self.assertTrue(all("Authorization" not in req.headers
                                    for req in requests))

    def test_discovery_cursor_stays_in_its_original_category(self):
        mod = load()
        token = mod._discovery_cursor("25", 1)
        with self.assertRaises(mod.SearchError):
            mod.public_category_page("10", page_token=token,
                                     opener=lambda *args: self.fail("no network"))

    def test_unsafe_public_page_cursor_rejected_without_network(self):
        mod = load()
        def forbidden(*args, **kwargs):
            self.fail("Invalid page cursor must not call the network")
        for token in ("bad", "{}", '{"continuation":"x","key":"x","version":"x"}'):
            with self.subTest(token=token):
                with self.assertRaises(mod.SearchError):
                    mod.public_category_page("25", page_token=token, opener=forbidden)


if __name__ == "__main__":
    unittest.main()
