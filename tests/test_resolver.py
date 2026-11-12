"""Pure host tests for optional yt-dlp resolver. No network, receiver or yt-dlp needed."""
import importlib.util
import subprocess
from pathlib import Path
import unittest

MODULE = (
    Path(__file__).resolve().parents[1]
    / "plugin/Plugins/Extensions/WarderYouTube/resolver.py"
)
spec = importlib.util.spec_from_file_location("warderyoutube_resolver", str(MODULE))
resolver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(resolver)

GOOGLEVIDEO = "https://rr1---sn-test.googlevideo.com/videoplayback?id=123&expire=456"


class FakeCompleted:
    def __init__(self, stdout, returncode=0, stderr=""):
        self.stdout = stdout
        self.returncode = returncode
        self.stderr = stderr


class ResolverTests(unittest.TestCase):
    def test_video_id_validation(self):
        self.assertEqual(
            resolver.video_page_url("abcdefghijk"),
            "https://www.youtube.com/watch?v=abcdefghijk"
        )
        for invalid in ("bad", "-evil", "abcdefghijkl", "a/bcdefghij", None,
                        "abcde fghij", "ABCDEFGHIJK\n"):
            with self.subTest(video=invalid):
                with self.assertRaises(resolver.ResolverError):
                    resolver.video_page_url(invalid)

    def test_command_is_bounded_and_does_not_use_shell(self):
        seen = []
        def runner(args, **kwargs):
            seen.append((args, kwargs))
            return FakeCompleted(GOOGLEVIDEO + "\n")
        url = resolver.resolve_video_url(
            "abcdefghijk", which=lambda name: "/usr/bin/yt-dlp",
            runner=runner
        )
        self.assertEqual(url, GOOGLEVIDEO)
        cmd, kw = seen[0]
        self.assertEqual(cmd[0], "/usr/bin/yt-dlp")
        self.assertEqual(cmd[-2], "--")
        self.assertEqual(cmd[-1], "https://www.youtube.com/watch?v=abcdefghijk")
        self.assertIn("--ignore-config", cmd)
        self.assertIn("--no-playlist", cmd)
        self.assertIn("--no-cache-dir", cmd)
        self.assertIn("--get-url", cmd)
        self.assertIn("-f", cmd)
        self.assertEqual(kw["timeout"], resolver.TIMEOUT_SECONDS)
        self.assertFalse(kw["check"])
        self.assertNotIn("shell", kw)

    def test_no_yt_dlp_fails_cleanly(self):
        self.assertFalse(resolver.is_available(which=lambda n: None))
        with self.assertRaisesRegex(resolver.ResolverError, "not installed"):
            resolver.resolve_video_url(
                "abcdefghijk", which=lambda n: None,
                runner=lambda *a, **kw: self.fail("runner must not run")
            )

    def test_reject_unsafe_or_multiple_urls(self):
        invalid = [
            "http://rr1.googlevideo.com/test",
            "https://googlevideo.com.evil.example/watch",
            "https://localhost/test",
            "https://127.0.0.1/videoplayback",
            "file:///etc/passwd",
            "https://example.com/video.mp4",
            "https://evil:pass@rr1.googlevideo.com/video",
            "https://rr1.googlevideo.com/video\nhttps://bad.example/x",
            ""
        ]
        for url in invalid:
            with self.subTest(url=url):
                with self.assertRaises(resolver.ResolverError):
                    resolver.validate_stream_url(url)
        with self.assertRaises(resolver.ResolverError):
            resolver.resolve_video_url(
                "abcdefghijk", which=lambda n: "/usr/bin/yt-dlp",
                runner=lambda args, **kw: FakeCompleted(GOOGLEVIDEO + "\n" + GOOGLEVIDEO + "\n")
            )

    def test_no_raw_urls_in_failures(self):
        secret = "signed-secret-token"
        def failing(args, **kw):
            return FakeCompleted(
                "", returncode=1, stderr="https://rr.googlevideo.com/?sig=" + secret
            )
        with self.assertRaises(resolver.ResolverError) as e:
            resolver.resolve_video_url(
                "abcdefghijk", which=lambda n: "/usr/bin/yt-dlp", runner=failing
            )
        self.assertNotIn(secret, str(e.exception))
        self.assertNotIn("googlevideo", str(e.exception))

    def test_missing_muxed_mp4_retries_android_public_client(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append((argv, kwargs))
            if len(calls) == 1:
                return FakeCompleted("", returncode=1, stderr="ERROR: Requested format is not available")
            return FakeCompleted(GOOGLEVIDEO + "\n")
        url = resolver.resolve_video_url("abcdefghijk", runner=runner,
            which=lambda n: "/usr/bin/yt-dlp")
        self.assertEqual(url, GOOGLEVIDEO)
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1][0][-2:], ["--", "https://www.youtube.com/watch?v=abcdefghijk"])
        self.assertIn("youtube:player-client=android", calls[1][0])
        self.assertLessEqual(calls[1][1]["timeout"], 18)

    def test_private_video_does_not_retry_or_leak_errors(self):
        calls = []
        def runner(argv, **kwargs):
            calls.append(argv)
            return FakeCompleted("", returncode=1, stderr="Sign in to confirm you're not a bot SECRET")
        with self.assertRaises(resolver.ResolverError) as raised:
            resolver.resolve_video_url("abcdefghijk", runner=runner,
                which=lambda n: "/usr/bin/yt-dlp")
        self.assertEqual(len(calls), 1)
        self.assertNotIn("SECRET", str(raised.exception))

    def test_timeout(self):
        def runner(args, **kwargs):
            raise subprocess.TimeoutExpired(cmd=args, timeout=kwargs["timeout"])
        with self.assertRaisesRegex(resolver.ResolverError, "timed out"):
            resolver.resolve_video_url(
                "abcdefghijk", which=lambda n: "/usr/bin/yt-dlp", runner=runner
            )

    def test_bounded_video_quality(self):
        self.assertEqual(set(resolver.QUALITY_FORMATS), {"360", "720"})
        for quality in ("360", "720"):
            format_string = resolver.QUALITY_FORMATS[quality]
            self.assertIn("height<=" + quality, format_string)
            self.assertNotIn("+", format_string)
        seen = []
        def runner(args, **kwargs):
            seen.append(args)
            return FakeCompleted(GOOGLEVIDEO + "\n")
        result = resolver.resolve_video_url(
            "abcdefghijk", quality="360", runner=runner,
            which=lambda _: "/usr/bin/yt-dlp"
        )
        self.assertEqual(result, GOOGLEVIDEO)
        self.assertIn("height<=360", seen[0][seen[0].index("-f") + 1])
        with self.assertRaisesRegex(resolver.ResolverError, "quality"):
            resolver.resolve_video_url("abcdefghijk", quality="1080",
                runner=lambda *a, **kw: self.fail("must not execute"),
                which=lambda _: "/usr/bin/yt-dlp")

    def test_format_is_muxed_not_dash_separate(self):
        self.assertIn("acodec!=none", resolver.MUXED_MP4_FORMAT)
        self.assertIn("height<=720", resolver.MUXED_MP4_FORMAT)
        self.assertNotIn("+", resolver.MUXED_MP4_FORMAT)


if __name__ == "__main__":
    unittest.main()
