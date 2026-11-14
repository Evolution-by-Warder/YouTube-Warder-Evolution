"""Account-only Data API requests and UI dispatch; no real credentials/network."""
import importlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1] / 'plugin/Plugins/Extensions/WarderYouTube'
PKG = '_account_data52'
pkg = types.ModuleType(PKG)
pkg.__path__ = [str(ROOT)]
sys.modules[PKG] = pkg
policy = importlib.import_module(PKG + '.data_auth')
api = importlib.import_module(PKG + '.api')
feed = importlib.import_module(PKG + '.home_feed')
metadata = importlib.import_module(PKG + '.video_metadata')
backend = importlib.import_module(PKG + '.search_backend')


class Reply:
    def __init__(self, payload):
        self.body = io.BytesIO(json.dumps(payload).encode('utf-8'))
    def read(self, n):
        return self.body.read(n)
    def close(self):
        pass


def payload(search=False):
    return {'items': [{'id': {'videoId': 'abcdefghijk'} if search else 'abcdefghijk',
                      'snippet': {'title': 'Real video', 'channelTitle': 'Creator'},
                      'contentDetails': {'duration': 'PT2M'},
                      'statistics': {'viewCount': '42'}}],
            'nextPageToken': 'next-b', 'pageInfo': {'totalResults': 60}}


class AccountDataTests(unittest.TestCase):
    TOKEN = 'test-access-token-no-real-user-52'

    def setUp(self):
        self.real_access_token = policy.auth.access_token
        self.connected = patch.object(policy.auth, 'account_connected', return_value=True)
        self.token = patch.object(policy.auth, 'access_token', return_value=self.TOKEN)
        self.connected.start()
        self.get_token = self.token.start()
        self.addCleanup(self.connected.stop)
        self.addCleanup(self.token.stop)

    def capture(self, result):
        self.requests = []
        def opener(req, timeout):
            self.requests.append(req)
            return Reply(result)
        return opener

    def assert_oauth_only(self):
        req = self.requests[-1]
        query = parse_qs(urlsplit(req.full_url).query)
        self.assertEqual(urlsplit(req.full_url).netloc, 'www.googleapis.com')
        self.assertEqual(req.get_header('Authorization'), 'Bearer ' + self.TOKEN)
        self.assertNotIn('key', query)
        self.assertNotIn('access_token', query)
        self.assertNotIn(self.TOKEN, req.full_url)
        self.assertIsNone(req.data)
        return query

    def test_home_account_only_and_category_paging(self):
        page = feed.popular_videos_page('', category_id='10', page_token='page-a',
                                        opener=self.capture(payload()))
        self.assertEqual(page['next_page_token'], 'next-b')
        q = self.assert_oauth_only()
        self.assertEqual(q['videoCategoryId'], ['10'])
        self.assertEqual(q['pageToken'], ['page-a'])
        self.assertEqual(q['maxResults'], ['50'])

    def test_search_account_only_and_paging(self):
        api.search_videos('Hudba & videá', '', 'search-page',
                          opener=self.capture(payload(True)))
        q = self.assert_oauth_only()
        self.assertEqual(q['q'], ['Hudba & videá'])
        self.assertEqual(q['pageToken'], ['search-page'])

    def test_video_details_account_only(self):
        got = metadata.fetch_video_info('abcdefghijk', '', opener=self.capture(payload()))
        self.assertEqual(got['duration'], '2:00')
        self.assertEqual(self.assert_oauth_only()['id'], ['abcdefghijk'])

    def test_account_takes_precedence_over_existing_key_everywhere(self):
        for fn in (lambda op: api.search_videos('music', 'OLD-BACKUP-KEY', opener=op),
                   lambda op: feed.popular_videos_page('OLD-BACKUP-KEY', opener=op),
                   lambda op: metadata.fetch_video_info('abcdefghijk', 'OLD-BACKUP-KEY', opener=op)):
            fn(self.capture(payload(True) if fn is None else payload()))
            self.assert_oauth_only()
            self.assertNotIn('OLD-BACKUP-KEY', self.requests[-1].full_url)

    def test_availability_check_never_refreshes_on_gui_thread(self):
        self.assertTrue(policy.can_use_data_api(''))
        self.assertEqual(backend.select_backend('', False), 'api')
        self.get_token.assert_not_called()

    def test_expired_token_is_refreshed_by_existing_token_worker(self):
        api.search_videos('music', '', opener=self.capture(payload(True)))
        self.get_token.assert_called_once_with()

    def test_network_token_failure_does_not_fall_back_to_a_different_key(self):
        self.get_token.side_effect = policy.auth.SubscriptionsAuthError('raw PRIVATE-CREDENTIAL')
        with self.assertRaises(api.SearchError) as exc:
            api.search_videos('music', 'BACKUP', opener=self.capture(payload(True)))
        self.assertEqual(self.requests, [])
        self.assertIn('refresh YouTube sign-in', str(exc.exception))
        self.assertNotIn('PRIVATE', str(exc.exception))
        self.assertNotIn('BACKUP', str(exc.exception))

    def test_revoked_session_requires_reconnection_without_deleting_state(self):
        self.get_token.side_effect = policy.auth.ReauthorizationRequired('raw TOKEN')
        with patch.object(policy.auth, 'clear_tokens') as clear:
            with self.assertRaises(feed.SearchError) as exc:
                feed.popular_videos_page('', opener=self.capture(payload()))
            clear.assert_not_called()
        self.assertIn('Connect the account again', str(exc.exception))
        self.assertEqual(self.requests, [])

    def test_invalid_token_cannot_inject_headers(self):
        for token in ('', 'bad\r\nHeader: leak', 'has space', 'é', 'x'*8193):
            self.get_token.return_value = token
            with self.subTest(token_length=len(token)), self.assertRaises(policy.DataAuthorizationError):
                policy.authorize_request({}, {}, '')

    def test_bearer_request_cannot_follow_a_redirect(self):
        req = Request('https://www.googleapis.com/youtube/v3/videos',
                      headers={'Authorization': 'Bearer ' + self.TOKEN})
        with patch.object(policy, 'build_opener') as build:
            policy.open_authorized(req, policy.urlopen, 8)
            build.return_value.open.assert_called_once_with(req, timeout=8)
            handler = build.call_args[0][0]
            self.assertIsNone(handler.redirect_request(req, None, 302, '', {},
                                                        'https://other.invalid/'))

    def test_real_expired_token_refresh_is_used_for_keyless_chart(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'tokens.json'
            policy.auth.save_tokens({'access_token': 'expired',
                'refresh_token': 'refresh-test', 'expires_at': 1}, path)
            def refresh():
                return self.real_access_token(
                    {'client_id': 'test-client', 'client_secret': 'test-secret'}, path,
                    opener=lambda *a, **k: Reply({'access_token': self.TOKEN,
                                                 'expires_in': 3600}))
            self.get_token.side_effect = refresh
            feed.popular_videos_page('', opener=self.capture(payload()))
            self.assert_oauth_only()
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads(path.read_text())['access_token'], self.TOKEN)

    def test_signed_out_optional_key_still_works(self):
        with patch.object(policy.auth, 'account_connected', return_value=False):
            feed.popular_videos_page('optional-KEY', opener=self.capture(payload()))
            req = self.requests[0]
            self.assertIsNone(req.get_header('Authorization'))
            self.assertEqual(parse_qs(urlsplit(req.full_url).query)['key'], ['optional-KEY'])
            self.assertEqual(backend.select_backend('', True), 'yt-dlp')
            self.assertIsNone(backend.select_backend('', False))
            self.get_token.assert_not_called()

    def test_signed_out_without_key_has_an_explicit_signin_message(self):
        with patch.object(policy.auth, 'account_connected', return_value=False):
            with self.assertRaises(feed.SearchError) as exc:
                feed.popular_videos_page('', opener=self.capture(payload()))
            self.assertIn('Sign in to YouTube', str(exc.exception))
            self.assertEqual(self.requests, [])

    def test_http_auth_failure_never_exposes_token_or_key(self):
        def reject(req, timeout):
            raise HTTPError(req.full_url, 401, self.TOKEN, None, None)
        for call, error in ((lambda: api.search_videos('x', '', opener=reject), api.SearchError),
                            (lambda: feed.popular_videos_page('', opener=reject), api.SearchError),
                            (lambda: metadata.fetch_video_info('abcdefghijk', '', opener=reject), metadata.VideoInfoError)):
            with self.assertRaises(error) as exc:
                call()
            self.assertIn('Connect the account again', str(exc.exception))
            self.assertNotIn(self.TOKEN, str(exc.exception))


class AccountUiTests(unittest.TestCase):
    def test_home_without_api_key_uses_official_chart_and_more_pages(self):
        from test_home_runtime import load, ready, video
        ui, key, storage, jobs = load(key='')
        with patch.object(ui, 'can_use_data_api', return_value=True):
            home, session = ready(ui)
            self.assertIs(jobs[0][0][0], ui.popular_videos_page)
            self.assertEqual(jobs[0][0][1], '')
            jobs[0][2].success({'items': [video(i) for i in range(24)],
                                'next_page_token': 'p2', 'total_results': 60})
            self.assertTrue(home._request_more_popular())
            self.assertEqual(jobs[-1][1]['page_token'], 'p2')
            self.assertEqual(jobs[-1][0][1], '')
            home._category_cursor = 1
            home._choose_category()
            self.assertIs(jobs[-1][0][0], ui.popular_videos_page)
            self.assertEqual(jobs[-1][1]['category_id'], home._home_chips[1]['category_id'])

    def test_home_info_without_key_dispatches_metadata_worker(self):
        from test_home_runtime import load, ready, fake
        ui, key, storage, jobs = load(key='')
        home, session = ready(ui)
        home.right()
        before = len(jobs)
        with patch.object(ui, 'can_use_data_api', return_value=True), patch.dict(sys.modules, {
            '_warder_home.info_ui': fake('_warder_home.info_ui', WarderYouTubeInfo=object)
        }):
            home.info()
        self.assertEqual(len(jobs), before + 1)
        self.assertIs(jobs[-1][0][0], ui.fetch_video_info)
        self.assertEqual(jobs[-1][0][2], '')

    def test_history_and_favourites_details_without_key(self):
        from test_library_ui import load, Session
        for kind in ('history', 'favourites'):
            ui, mocks, videos, jobs, played, recorded = load()
            screen = ui.WarderYouTubeLibrary(Session(), kind)
            screen.refresh()
            with patch.object(ui, 'can_use_data_api', return_value=True):
                screen.show_info()
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0][1][1], '')

    def test_main_settings_explains_account_without_showing_key(self):
        from test_settings_api_mask import environment
        with environment(configured='stored-backup-key', advanced=False) as env:
            ui, screen, session, key = env[:4]
            with patch.object(ui, 'account_available', return_value=True):
                screen.refresh()
            self.assertEqual(screen['section_search'].text, 'YOUTUBE ACCOUNT')
            self.assertIn('No personal API key is needed', screen['key_state'].text)
            self.assertEqual(screen['key_green'].text, 'Manage account')
            self.assertEqual(screen['key_yellow'].text, 'Advanced')
            self.assertNotIn('stored-backup-key', ' '.join(v.text for v in screen.values() if hasattr(v, 'text')))
            self.assertNotIn('********', screen['key_state'].text)
            self.assertEqual(key.value, 'stored-backup-key')

    def test_advanced_backup_remains_masked_and_back_returns_to_account(self):
        from test_settings_api_mask import environment
        with environment(configured='stored-backup-key', advanced=False) as env:
            ui, screen, session, key = env[:4]
            screen.secondary_action()
            self.assertTrue(screen._advanced)
            self.assertIn('********', screen['key_state'].text)
            self.assertEqual(screen['key_yellow'].text, 'Delete API key')
            screen.back()
            self.assertFalse(screen._advanced)
            self.assertEqual(screen['key_yellow'].text, 'Advanced')
            self.assertEqual(key.value, 'stored-backup-key')

    def test_settings_signin_routes_to_existing_right_hand_subscriptions(self):
        from test_home_runtime import load, ready
        ui, key, storage, jobs = load()
        home, session = ready(ui)
        home.index = 5
        with patch.object(ui, 'account_available', return_value=False), \
                patch.object(home, '_open_subscription_login') as start:
            home._settings_closed('account')
            self.assertEqual(home.index, 2)
            self.assertEqual(session.opens, [])
            home._personalization_ready({'connected': False, 'channels': []}, home._personal_epoch)
            start.assert_called_once()

    def test_search_and_details_flow_with_blank_key(self):
        from test_home_direct_search import native_search, module
        with native_search() as (flow, home, jobs, api_fn):
            globals_ = flow.start.__globals__
            with patch.dict(globals_, {'get_api_key': lambda: '',
                                      'select_backend': lambda key, available: 'api'}):
                flow.start('music')
            self.assertEqual(jobs[-1][0], (api_fn, 'music', '', ''))
            jobs[-1][1].success({'items': [{'video_id': 'abcdefghijk', 'title': 'Music'}],
                                 'next_page_token': 'p2'})
            def metadata_fn(*args):
                return {}
            with patch.dict(sys.modules, {
                '_home_direct_test.info_ui': module('i', WarderYouTubeInfo=object),
                '_home_direct_test.video_metadata': module('m', fetch_video_info=metadata_fn, VideoInfoError=ValueError)
            }), patch.dict(globals_, {'get_api_key': lambda: '', 'can_use_data_api': lambda key: True}):
                flow.info_video({'video_id': 'abcdefghijk'})
            self.assertEqual(jobs[-1][0], (metadata_fn, 'abcdefghijk', ''))


if __name__ == '__main__':
    unittest.main()
