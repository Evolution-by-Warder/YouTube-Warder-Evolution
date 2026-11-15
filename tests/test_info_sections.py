"""INFO in Home/History/Favourites: offline Enigma2, explicit-request only.

No live Google/YouTube network traffic, even in the API-key branch.
"""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

from test_library_ui import load as load_library, Session as LibrarySession
from test_home_runtime import load as load_home, ready as ready_home, fake

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


class DetailInfoTests(unittest.TestCase):
    def test_local_history_and_favourites_info_does_not_use_network(self):
        for kind in ("history", "favourites"):
            with self.subTest(kind=kind):
                ui, mocks, videos, jobs, played, recorded = load_library()
                screen_session = LibrarySession()
                screen = ui.WarderYouTubeLibrary(screen_session, kind)
                screen.refresh()
                screen.show_info()
                self.assertEqual(jobs, [])
                self.assertEqual(len(screen_session.opens), 1)
                text = screen_session.opens[0][1][0]
                self.assertIn("Video ID", text)
                self.assertIn("Sign in to YouTube", text)

    def test_library_details_are_async_and_ignore_duplicate_info(self):
        ui, mocks, videos, jobs, played, recorded = load_library()
        screen_session = LibrarySession()
        screen = ui.WarderYouTubeLibrary(screen_session, "history")
        screen.refresh()
        with patch.object(ui, "get_api_key", return_value="user-api-key"):
            screen.show_info()
            screen.show_info()
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0][1], (videos["history"][0]["video_id"], "user-api-key"))
        self.assertEqual(screen_session.opens, [])
        jobs[0][3].success({
            "title": "Online title", "channel": "Channel",
            "duration": "3:24", "views": "12 345",
            "description": "Live YouTube info"
        })
        self.assertEqual(len(screen_session.opens), 1)
        message = screen_session.opens[0][1][0]
        self.assertIn("Duration: 3:24", message)
        self.assertIn("Views: 12 345", message)
        self.assertIn("Live YouTube info", message)

    def test_library_error_preserves_local_details_not_external_error(self):
        ui, mocks, videos, jobs, played, recorded = load_library()
        session = LibrarySession()
        screen = ui.WarderYouTubeLibrary(session, "favourites")
        screen.refresh()
        with patch.object(ui, "get_api_key", return_value="user-api-key"):
            screen.show_info()
        jobs[0][3].failure(Exception("private key or HTTP URL must not appear"))
        self.assertEqual(len(session.opens), 1)
        text = session.opens[0][1][0]
        self.assertIn("Song 2", text)
        self.assertNotIn("private key", text)
        self.assertFalse(screen.busy)

    def test_closing_library_discards_info_worker_response(self):
        ui, mocks, videos, jobs, played, recorded = load_library()
        session = LibrarySession()
        screen = ui.WarderYouTubeLibrary(session, "history")
        screen.refresh()
        with patch.object(ui, "get_api_key", return_value="user-api-key"):
            screen.show_info()
        screen.dispose()
        jobs[0][3].success({"title": "Too late"})
        self.assertEqual(session.opens, [])

    def test_home_tiles_local_info_has_clear_no_key_fallback(self):
        mod, key, storage, jobs = load_home(key="")
        screen, session = ready_home(mod)
        for _ in range(3):
            screen.down()
        screen.right()
        mock_info = fake("_warder_home.info_ui", WarderYouTubeInfo=object)
        with patch.dict("sys.modules", {"_warder_home.info_ui": mock_info}):
            screen.info()
        self.assertEqual(len(session.opens), 1)
        self.assertIn("Video ID", session.opens[0][0][1])
        self.assertIn("Sign in to YouTube", session.opens[0][0][1])
        self.assertEqual(session.opens[0][1]["video"]["video_id"], storage["history"][0]["video_id"])
        self.assertEqual(len(jobs), 2)  # initial Home feed only

    def test_home_tiles_info_fetches_metadata_only_after_info(self):
        mod, key, storage, jobs = load_home(key="user-api-key")
        screen, session = ready_home(mod)
        for _ in range(3):
            screen.down()
        screen.right()
        mock_info = fake("_warder_home.info_ui", WarderYouTubeInfo=object)
        with patch.dict("sys.modules", {"_warder_home.info_ui": mock_info}):
            self.assertEqual(len(jobs), 2)
            screen.info()
            screen.info()
            self.assertEqual(len(jobs), 3)
            self.assertEqual(session.opens, [])
            jobs[2][2].success({
                "title": "Remote video", "channel": "Publisher",
                "duration": "12:30", "views": "999",
                "description": "Fetched explicitly"
            })
        self.assertEqual(len(session.opens), 1)
        self.assertIn("Duration: 12:30", session.opens[0][0][1])
        self.assertIn("Views: 999", session.opens[0][0][1])
        self.assertFalse(screen._busy)

    def test_home_closed_before_info_result_must_not_open_popup(self):
        mod, key, storage, jobs = load_home(key="user-api-key")
        screen, session = ready_home(mod)
        for _ in range(3):
            screen.down()
        screen.right()
        mock_info = fake("_warder_home.info_ui", WarderYouTubeInfo=object)
        with patch.dict("sys.modules", {"_warder_home.info_ui": mock_info}):
            screen.info()
        screen.dispose()
        jobs[2][2].success({"title": "Late response"})
        self.assertEqual(session.opens, [])

    def test_four_language_info_labels(self):
        spec = importlib.util.spec_from_file_location("warder_i18n_test27", ROOT / "i18n.py")
        locale = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(locale)
        for lang, expected in {
            "sk": ("Dĺžka", "Pozretia"),
            "cs": ("Délka", "Zhlédnutí"),
            "de": ("Dauer", "Aufrufe"),
            "en": ("Duration", "Views"),
        }.items():
            with self.subTest(lang=lang):
                strings = locale.MESSAGES.get(lang, {})
                self.assertEqual(strings.get("Duration", "Duration"), expected[0])
                self.assertEqual(strings.get("Views", "Views"), expected[1])


if __name__ == "__main__":
    unittest.main()
