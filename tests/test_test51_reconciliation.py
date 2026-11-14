"""Receiver-approved test50 regression coverage; no real account/network."""
import ast
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tarfile
import tempfile
import threading
import types
import unittest
from unittest.mock import patch
from urllib.error import URLError

from test_home_runtime import load, ready, video, fake
from test_subscriptions_oauth_api import auth, api, CLIENT, Response
from test_home_tv_auth import load as login_load, Home
from test_ipk_build import m as builder, ar_parts

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'plugin/Plugins/Extensions/WarderYouTube'


class ApprovedSourceTests(unittest.TestCase):
    def test_all_approved_layout_sources_unchanged_from_test50(self):
        manifest=json.loads((ROOT/'tests/fixtures/test50-approved-layout.json').read_text())
        for name, digest in manifest.items():
            with self.subTest(name=name):
                self.assertEqual(hashlib.sha256((SRC/name).read_bytes()).hexdigest(), digest)

    def test_built_package_preserves_all_approved_layout_bytes(self):
        manifest=json.loads((ROOT/'tests/fixtures/test50-approved-layout.json').read_text())
        with tempfile.TemporaryDirectory() as td:
            result=builder.build(Path(td))
            parts=ar_parts(result.read_bytes())
            with tarfile.open(fileobj=io.BytesIO(parts['data.tar.gz']),mode='r:gz') as tar:
                for name,digest in manifest.items():
                    body=tar.extractfile('./'+builder.TARGET_PREFIX+'/'+name).read()
                    self.assertEqual(hashlib.sha256(body).hexdigest(),digest,name)

    def test_no_production_google_credentials_added(self):
        module=ast.parse((SRC/'oauth_app_config.py').read_text())
        assigned={n.targets[0].id:ast.literal_eval(n.value) for n in module.body
                  if isinstance(n,ast.Assign)}
        self.assertEqual(assigned['OAUTH_TV_CLIENT_ID'],'')
        self.assertEqual(assigned['OAUTH_TV_CLIENT_SECRET'],'')

    def test_runtime_and_builder_have_distinct_test51_version(self):
        self.assertEqual(builder.VERSION,'0.0.8~test51')
        self.assertIn('CURRENT_VERSION = "0.0.8~test51"',(SRC/'update_core.py').read_text())


class AccountLifecycleTests(unittest.TestCase):
    def test_invalid_grant_requests_reauthentication_without_deleting_tokens(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json'
            auth.save_tokens({'access_token':'expired','refresh_token':'refresh','expires_at':1},path)
            old=path.read_bytes()
            with self.assertRaises(auth.ReauthorizationRequired):
                auth.access_token(CLIENT,path,lambda *a,**k:Response({'error':'invalid_grant'}))
            self.assertEqual(path.read_bytes(),old)

    def test_temporary_token_error_does_not_request_reauthentication(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json'
            auth.save_tokens({'access_token':'expired','refresh_token':'refresh','expires_at':1},path)
            old=path.read_bytes()
            with self.assertRaises(auth.SubscriptionsAuthError) as err:
                auth.access_token(CLIENT,path,lambda *a,**k:Response({'error':'temporarily_unavailable'}))
            self.assertNotIsInstance(err.exception,auth.ReauthorizationRequired)
            self.assertEqual(path.read_bytes(),old)

    def test_cancelled_pending_login_does_not_write_token_file(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json'; cancelled=threading.Event();cancelled.set()
            self.assertFalse(auth.save_tokens_if_active({'access_token':'private'},cancelled,path))
            self.assertFalse(path.exists())

    def test_active_login_writes_private_file(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json'
            self.assertTrue(auth.save_tokens_if_active({'access_token':'private'},threading.Event(),path))
            self.assertEqual(path.stat().st_mode & 0o777,0o600)

    def test_cancel_while_write_waits_for_lock_does_not_resurrect_account(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json';cancelled=threading.Event();result=[]
            with auth._LOCK:
                worker=threading.Thread(target=lambda:result.append(
                    auth.save_tokens_if_active({'refresh_token':'private'},cancelled,path)))
                worker.start();cancelled.set()
            worker.join(timeout=2)
            self.assertFalse(worker.is_alive())
            self.assertEqual(result,[False]);self.assertFalse(path.exists())

    def test_offline_disconnect_still_removes_only_account_token(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'token.json';other=Path(td)/'favourites.json';other.write_text('keep')
            auth.save_tokens({'refresh_token':'private'},path)
            def offline(*a,**k):raise URLError('private detail must not be printed')
            self.assertFalse(auth.disconnect_account(path,opener=offline))
            self.assertFalse(path.exists());self.assertEqual(other.read_text(),'keep')

    def test_cancelled_login_save_callback_is_ignored(self):
        mod,tasks,timers,modules=login_load();home=Home();login=mod.HomeTVLogin(home)
        login.active=True
        login._poll_ready(0,('connected',{'refresh_token':'secret'}))
        self.assertEqual(len(tasks),1)
        args,deferred=tasks[0]; login.close()
        self.assertTrue(args[2].is_set())
        self.assertFalse(args[0](*args[1:]))
        deferred.success(False)
        self.assertFalse(home.connected)

    def test_auth_error_uses_known_safe_reason_not_raw_details(self):
        mod,tasks,timers,modules=login_load();home=Home();login=mod.HomeTVLogin(home)
        error=mod.SubscriptionsAuthError('YouTube account access was denied.')
        login._poll_failed(0,types.SimpleNamespace(value=error))
        self.assertEqual(home.messages[-1],'YouTube account access was denied.')
        other=mod.HomeTVLogin(home)
        other._poll_failed(0,types.SimpleNamespace(value=RuntimeError('BEARER-SECRET')))
        self.assertEqual(home.messages[-1],'YouTube TV login failed.')
        self.assertFalse(any('BEARER-SECRET' in msg for msg in home.messages))


class SubscriptionRecoveryTests(unittest.TestCase):
    def test_reopening_failed_subscriptions_retries_without_new_login(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        jobs[0][2].success([video(1)])
        screen._personalization_ready({'connected':True,'channels':[], 'load_error':True},screen._personal_epoch)
        old=len(jobs);screen._select_nav(2)
        self.assertEqual(len(jobs),old+1)
        self.assertEqual(jobs[-1][0][0].__name__,'_discover_home_subscriptions')
        self.assertIsNone(screen._inline_tv_login)

    def test_expired_login_requests_new_tv_code_on_ok(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        screen.index=2
        screen._personalization_ready({'connected':True,'channels':[],'reconnect':True},screen._personal_epoch)
        self.assertIn('expired',screen['preview_message'].text)
        calls=[]
        class Login:
            closed=False
            def __init__(self,home):pass
            def start(self):calls.append('start')
        with patch.dict(sys.modules,{'_warder_home.home_tv_auth':fake('_warder_home.home_tv_auth',HomeTVLogin=Login)}):
            screen._open_index(2)
        self.assertEqual(calls,['start'])

    def test_network_outage_does_not_turn_connected_account_into_logged_out(self):
        mod,key,saved,jobs=load(key='api')
        def outage():raise auth.SubscriptionsAuthError('Google authorization service is unavailable.')
        modules={
          '_warder_home.subscriptions_auth':fake('_warder_home.subscriptions_auth',account_connected=lambda:True,
             access_token=outage,ReauthorizationRequired=auth.ReauthorizationRequired),
          '_warder_home.subscriptions_api':fake('_warder_home.subscriptions_api',subscriptions_list=lambda *a,**k:[]),
        }
        with patch.dict(sys.modules,modules):result=mod._discover_home_subscriptions()
        self.assertTrue(result['connected']);self.assertTrue(result['load_error'])
        self.assertFalse(result.get('reconnect',False))

    def test_confirmed_expiry_is_not_reported_as_empty_subscriptions(self):
        mod,key,saved,jobs=load(key='api')
        def expired():raise auth.ReauthorizationRequired('expired')
        modules={
          '_warder_home.subscriptions_auth':fake('_warder_home.subscriptions_auth',account_connected=lambda:True,
             access_token=expired,ReauthorizationRequired=auth.ReauthorizationRequired),
          '_warder_home.subscriptions_api':fake('_warder_home.subscriptions_api',subscriptions_list=lambda *a,**k:[]),
        }
        with patch.dict(sys.modules,modules):result=mod._discover_home_subscriptions()
        self.assertTrue(result['connected']);self.assertTrue(result['reconnect'])

    def test_successful_refresh_discards_stale_channel_video_cache(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        data={'connected':True,'channels':[{'channel_id':'UC'+'a'*22,'title':'Channel'}]}
        screen._personalization_ready(data,screen._personal_epoch)
        screen._subscription_video_cache['channel:'+'UC'+'a'*22]=[video(1)]
        screen._personalization_ready(data,screen._personal_epoch)
        self.assertEqual(screen._subscription_video_cache,{})

    def test_outage_retains_channel_list_for_later_retry(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        channels=[{'channel_id':'UC'+'a'*22,'title':'Channel'}]
        screen._personalization_ready({'connected':True,'channels':channels},screen._personal_epoch)
        screen._personalization_ready({'connected':True,'channels':[],'load_error':True},screen._personal_epoch)
        self.assertEqual(screen._home_channels,channels)

    def test_logout_invalidates_late_account_result_and_preserves_local_library(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        screen.index=2;old_epoch=screen._personal_epoch
        with patch.dict(sys.modules,{'_warder_home.subscriptions_auth':fake('_warder_home.subscriptions_auth',disconnect_account=lambda:True)}):
            screen._disconnect_confirmed(True)
        screen._personalization_ready({'connected':True,'channels':[{'channel_id':'UC'+'a'*22,'title':'stale'}]},old_epoch)
        jobs[-1][2].success(True)
        self.assertFalse(screen._subscriptions_connected)
        self.assertEqual(screen._subscription_chips,[])
        self.assertEqual(saved['favourites'],[video(2)])

    def test_home_revisit_rotates_without_resetting_approved_layout(self):
        mod,key,saved,jobs=load(key='api');screen,session=ready(mod)
        jobs[0][2].success([video(i) for i in range(50)])
        first=[v['video_id'] for v in screen.video_items]
        screen._select_nav(3);screen._select_nav(0)
        second=[v['video_id'] for v in screen.video_items]
        self.assertNotEqual(first,second)
        self.assertEqual(screen._home_chips[0]['category_id'],'0')
        self.assertFalse(screen['status'].visible)
