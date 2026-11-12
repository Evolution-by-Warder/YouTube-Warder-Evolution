# -*- coding: utf-8 -*-
"""Native results screen with non-blocking YouTube Data API lookup.

No video player here yet. The Twisted Deferred resumes on the reactor thread,
while urllib only runs in the worker pool.
"""
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.MenuList import MenuList
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

try:
    from Screens.VirtualKeyBoard import VirtualKeyboard
except ImportError:
    from Screens.VirtualKeyBoard import VirtualKeyBoard as VirtualKeyboard

from twisted.internet.threads import deferToThread

from .api import SearchError, search_videos
from .settings import WarderYouTubeSettings, get_api_key
from .skin import SEARCH_SKIN


class WarderYouTubeSearch(Screen):
    skin = SEARCH_SKIN

    def __init__(self, session):
        Screen.__init__(self, session)
        self.query = ""
        self.items = []
        self.page_token = ""
        self.next_page_token = ""
        self.busy = False
        self.closed = False
        self.request_version = 0

        self["title"] = Label("YouTube - Warder Evolution / Search")
        self["query"] = Label("Search videos")
        self["results"] = MenuList([])
        self["details"] = Label("")
        self["status"] = Label("BLUE: search     YELLOW: settings")
        self["footer"] = Label(
            "UP/DOWN: select     OK: details     BLUE: search     "
            "GREEN: next page     YELLOW: settings     EXIT: back"
        )
        self["actions"] = ActionMap(
            ["OkCancelActions", "ColorActions"],
            {"ok": self.open_selected, "cancel": self.close,
             "red": self.close, "blue": self.open_keyboard,
             "green": self.next_page, "yellow": self.open_settings},
            -1
        )
        self["results"].onSelectionChanged.append(self.selection_changed)
        self.onLayoutFinish.append(self.first_open)
        self.onClose.append(self.mark_closed)

    def first_open(self):
        if get_api_key():
            self.open_keyboard()
        else:
            self["status"].setText("Set your API key via YELLOW / Settings before searching.")

    def mark_closed(self):
        self.closed = True
        self.request_version += 1

    def open_settings(self):
        if not self.busy:
            self.session.open(WarderYouTubeSettings)

    def open_keyboard(self):
        if self.busy:
            return
        if not get_api_key():
            self["status"].setText("Missing API key. Press YELLOW to open Settings.")
            return
        self.session.openWithCallback(
            self.search_submitted, VirtualKeyboard,
            title="Search YouTube videos", text=self.query
        )

    def search_submitted(self, query):
        if query is None or not query.strip():
            return
        self.query = query.strip()
        self.page_token = ""
        self.next_page_token = ""
        self.items = []
        self["results"].setList([])
        self["details"].setText("")
        self._load_page("")

    def next_page(self):
        if not self.busy and self.query and self.next_page_token:
            self._load_page(self.next_page_token)

    def _load_page(self, page_token):
        if self.busy:
            return
        self.busy = True
        self.request_version += 1
        version = self.request_version
        self["query"].setText("Search: " + self.query[:60])
        self["status"].setText("Loading real YouTube results...")
        # No network activity or JSON decoding on the GUI thread.
        deferred = deferToThread(search_videos, self.query, get_api_key(), page_token)
        deferred.addCallbacks(
            lambda response: self.receive_results(version, page_token, response),
            lambda error: self.receive_error(version, error)
        )

    def receive_results(self, version, page_token, response):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        self.page_token = page_token
        self.next_page_token = response["next_page_token"]
        self.items = response["items"]
        self["results"].setList([
            item["title"][:80] + ("  |  " + item["channel"][:35] if item["channel"] else "")
            for item in self.items
        ])
        self.selection_changed()
        if not self.items:
            self["status"].setText("No videos found. Press BLUE to search again.")
        else:
            suffix = "  |  GREEN: next page" if self.next_page_token else ""
            self["status"].setText("%d video(s) found%s" % (len(self.items), suffix))

    def receive_error(self, version, failure):
        if self.closed or version != self.request_version:
            return
        self.busy = False
        error = getattr(failure, "value", None)
        if isinstance(error, SearchError):
            message = str(error)
        else:
            message = "Unexpected error. Please try another search."
        # Do NOT log exception repr: urllib exceptions may include key in URL.
        self["status"].setText(message)

    def selection_changed(self):
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.items):
            item = self.items[index]
            self["details"].setText("%s   |   %s" % (item["channel"], item["published_at"]))
        else:
            self["details"].setText("")

    def open_selected(self):
        if not self.items:
            self.open_keyboard()
            return
        index = self["results"].getCurrentIndex()
        if 0 <= index < len(self.items):
            video = self.items[index]
            self.session.open(
                MessageBox,
                "Video: %s\nChannel: %s\n\nPlayback will be implemented after "
                "the separate stream resolver and receiver tests." %
                (video["title"], video["channel"]),
                type=MessageBox.TYPE_INFO
            )
