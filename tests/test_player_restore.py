"""Mock native Radio-derived MoviePlayer navigation and failover."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube/player.py"

class Ref:
    def __init__(self, kind, flags, url):
        self.kind,self.url=kind,url
    def setName(self,title):self.name=title
    def toString(self):return "%s:%s"%(self.kind,self.url)

class Nav:
    def __init__(self):
        self.previous=Ref(1,0,"tv")
        self.current=self.previous
        self.calls=[]
    def getCurrentlyPlayingServiceOrGroup(self):return self.current
    def getCurrentlyPlayingServiceReference(self):return self.current
    def playService(self, ref):
        self.current=ref
        self.calls.append(ref)
        return 0

class MoviePlayer:
    def __init__(self,session,ref,lastservice=None,fromMovieSelection=False):
        self.session=session
        self.lastservice=lastservice
        self.cur_service=ref
        self.onClose=[]
        self.execing=True
        self.session.nav.playService(ref)
    def close(self,*args):
        for fn in self.onClose:fn()
        self.session.nav.playService(self.lastservice)
        if self.session.callback:self.session.callback(*args)

class Session:
    def __init__(self):
        self.nav=Nav()
        self.callback=None
        self.player=None
    def openWithCallback(self, callback, cls,*args):
        self.callback=callback
        self.player=cls(self,*args)
        return self.player

def load():
    enigma=types.ModuleType("enigma")
    enigma.eServiceReference=Ref
    enigma.iPlayableService=types.SimpleNamespace(evTuneFailed=1,evUser=1000)
    enigma.eServiceCenter=types.SimpleNamespace(getInstance=lambda:None)
    tracker=types.ModuleType("Components.ServiceEventTracker")
    tracker.ServiceEventTracker=lambda **kwargs:kwargs
    screens=types.ModuleType("Screens")
    screens.__path__=[]
    info=types.ModuleType("Screens.InfoBar")
    info.MoviePlayer=MoviePlayer
    spec=importlib.util.spec_from_file_location("warder_radio_player_test",PATH)
    mod=importlib.util.module_from_spec(spec)
    with patch.dict(sys.modules,{
        "enigma":enigma,"Components":types.ModuleType("Components"),
        "Components.ServiceEventTracker":tracker,
        "Screens":screens,"Screens.InfoBar":info}):
        spec.loader.exec_module(mod)
    return mod

def item(n,kind=4097):
    return {"url":"https://rr1.googlevideo.com/%s"%n,"service_type":kind}

class RadioPlaybackTests(unittest.TestCase):
    def test_native_exit_restores_tv_once(self):
        m=load();s=Session();done=[]
        m.open_player(s,[item(1)],"Test",on_close=lambda *a:done.append(a))
        self.assertEqual(s.nav.current.kind,4097)
        s.player.leavePlayerOnExit()
        self.assertIs(s.nav.current,s.nav.previous)
        self.assertEqual(done,[()])

    def test_failed_first_stream_tries_next_candidate(self):
        m=load();s=Session()
        m.open_player(s,[item(1),item(2,5002)],"Test")
        s.player.stream_error()
        self.assertEqual(s.nav.current.kind,5002)
        self.assertEqual(s.player.video_index,1)
        s.player.stream_error()
        self.assertTrue(s.player.failed)
        self.assertIs(s.nav.current,s.nav.previous)

    def test_external_channel_change_is_not_undone(self):
        m=load();s=Session()
        m.open_player(s,[item(1)],"Test")
        external=Ref(1,0,"new-station")
        s.nav.playService(external)
        s.player.leavePlayerOnExit()
        self.assertIs(s.nav.current,external)

    def test_reject_unknown_service_type(self):
        m=load();s=Session()
        with self.assertRaises(ValueError):
            m.open_player(s,[item(1,9999)],"Test")
        self.assertIs(s.nav.current,s.nav.previous)

    def test_eof_closes_and_restores_tv(self):
        m=load();s=Session()
        m.open_player(s,[item(1)],"Test")
        s.player.doEofInternal(True)
        self.assertIs(s.nav.current,s.nav.previous)

if __name__=="__main__":
    unittest.main()
