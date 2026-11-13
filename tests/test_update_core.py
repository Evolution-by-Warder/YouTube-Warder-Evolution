"""Offline regression tests for the opt-in YouTube update feed and IPK installer."""
import importlib.util
import hashlib
import io
import json
from pathlib import Path
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "plugin/Plugins/Extensions/WarderYouTube/update_core.py"
spec = importlib.util.spec_from_file_location("warder_test_update", SRC)
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)


def valid_manifest(version):
    return {
        "schema": 1, "product": u.PRODUCT, "channel": "testing",
        "release": {
            "version": version,
            "tag": "youtube-warder-v" + version.replace("~", "-"),
            "url": u.expected_url(version),
            "sha256": "a" * 64,
            "bytes": 62210,
            "notes": "Safe receiver-test candidate"
        }
    }


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self
    def __exit__(self, *args):
        self.close()


class UpdateCoreTests(unittest.TestCase):
    def test_tilde_versions_and_github_normalized_asset_url(self):
        self.assertEqual(u.CURRENT_VERSION, "0.0.8~test15")
        self.assertEqual(u.channel_for_version(u.CURRENT_VERSION), "testing")
        self.assertLess(u.version_key("0.0.8~test6"), u.version_key("0.0.8~test7"))
        self.assertLess(u.version_key("0.0.8~test7"), u.version_key("0.0.8"))
        self.assertIn("/youtube-warder-v0.0.8-test7/", u.expected_url("0.0.8~test7"))
        self.assertIn("_0.0.8.test7_all.ipk", u.expected_url("0.0.8~test7"))

    def test_no_release_and_reject_unsigned(self):
        base = {"schema": 1, "product": u.PRODUCT, "channel": "testing", "release": None}
        self.assertIsNone(u.parse_manifest(json.dumps(base).encode(), u.CURRENT_VERSION))
        base["release"] = {"version": "0.0.8~test8"}
        with self.assertRaises(u.UpdateError):
            u.parse_manifest(json.dumps(base).encode(), u.CURRENT_VERSION)

    def test_published_testing_manifest_matches_real_github_asset(self):
        feed = json.loads((ROOT / "update/testing.json").read_text(encoding="utf-8"))
        rel = feed["release"]
        # Pinned, independently verified GitHub prerelease in the testing feed.
        # When publishing the next test candidate, update these values only
        # after its actual release asset and SHA256 have been verified.
        self.assertEqual(rel["version"], "0.0.8~test15")
        self.assertEqual(rel["sha256"], "4a5e8386f09de33c9b46cd3fac42d30ad35859ff8d53c7f4d898044fca25d859")
        self.assertEqual(rel["bytes"], 165488)
        self.assertEqual(rel["url"], u.expected_url(rel["version"]))
        self.assertEqual(len(rel["sha256"]), 64)
        self.assertGreater(rel["bytes"], 0)
        self.assertIsNone(u.parse_manifest(json.dumps(feed).encode(), u.CURRENT_VERSION))
        self.assertLessEqual(u.version_key(rel["version"]), u.version_key(u.CURRENT_VERSION))

    def test_installed_test6_is_offered_test7_for_opt_in_update(self):
        candidate = valid_manifest("0.0.8~test7")
        release = u.parse_manifest(json.dumps(candidate).encode(), "0.0.8~test6")
        self.assertEqual(release["version"], "0.0.8~test7")
        self.assertEqual(release["url"], u.expected_url("0.0.8~test7"))
        self.assertTrue(release["url"].endswith("_0.0.8.test7_all.ipk"))

    def test_future_testing_update_is_offered_with_dotted_download_url(self):
        future = valid_manifest("0.0.8~test16")
        release = u.parse_manifest(json.dumps(future).encode(), u.CURRENT_VERSION)
        self.assertEqual(release["version"], "0.0.8~test16")
        self.assertEqual(release["url"], u.expected_url("0.0.8~test16"))
        self.assertTrue(release["url"].endswith("_0.0.8.test16_all.ipk"))

    def test_manifest_rejects_mismatched_tag_url_or_digest(self):
        for change, value in [
            ("tag", "youtube-warder-v0.0.8-test99"),
            ("url", "https://attacker.invalid/plugin.ipk"),
            ("url", u.expected_url("0.0.8~test8").replace(".test8", "~test8")),
            ("sha256", "invalid"),
            ("bytes", 0),
        ]:
            with self.subTest(field=change, value=value):
                bad = valid_manifest("0.0.8~test8")
                bad["release"][change] = value
                with self.assertRaises(u.UpdateError):
                    u.parse_manifest(json.dumps(bad).encode(), u.CURRENT_VERSION)

    def test_check_update_uses_testing_feed_and_no_auto_install(self):
        requested = []
        future = json.dumps(valid_manifest("0.0.8~test16")).encode("utf-8")
        def fake_open(url, timeout):
            requested.append((url, timeout))
            return FakeResponse(future)
        result = u.check_update(u.CURRENT_VERSION, opener=fake_open)
        self.assertEqual(result["version"], "0.0.8~test16")
        self.assertEqual(requested, [(u.FEED_TESTING, 8)])

    def test_verified_download_and_reject_corruption(self):
        payload = b"ipk-bytes-from-test-only-backend"
        info = {
            "url": u.expected_url("0.0.8~test8"),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        }
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "download.ipk"
            progress = []
            result = u.download_update(
                info, dest, opener=lambda url, timeout: FakeResponse(payload),
                progress=lambda *args: progress.append(args)
            )
            self.assertEqual(result.read_bytes(), payload)
            self.assertIn(("download", len(payload), len(payload)), progress)
            dest.unlink()
            bad = dict(info, sha256="0" * 64)
            with self.assertRaises(u.UpdateError):
                u.download_update(bad, dest,
                    opener=lambda url, timeout: FakeResponse(payload))
            self.assertFalse(dest.exists())

    def test_installed_package_status_exact_match(self):
        status = "Package: other-plugin\nVersion: 0.0.8~test8\n\n" + (
            "Package: " + u.PACKAGE + "\n"
            "Version: 0.0.8~test8\nStatus: install ok installed\n")
        self.assertEqual(u._installed_version(status),
                         ("0.0.8~test8", "install ok installed"))
        self.assertEqual(u._installed_version("Package: unrelated\nVersion: 1\n"),
                         (None, None))



    def test_actual_ipk_offline_install_verification_no_real_opkg(self):
        """Dry-run the complete install from the real current test7 package builder."""
        import sys
        from unittest.mock import patch
        import types
        builder_file = ROOT / "tools/build_test_ipk.py"
        builder_spec = importlib.util.spec_from_file_location(
            "warder_ipk_builder_for_update_test", builder_file)
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as tmp:
            package = builder.build(Path(tmp))
            data = package.read_bytes()
            release = {
                "version": builder.VERSION,
                "url": u.expected_url(builder.VERSION),
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": len(data),
            }
            commands = []
            progress = []
            def fake_run(argv, **kwargs):
                commands.append(argv)
                if argv[1] == "install":
                    self.assertTrue(Path(argv[2]).is_file())
                    self.assertIn("warder-youtube-update-", argv[2])
                    return types.SimpleNamespace(returncode=0, stdout="")
                if argv[1] == "status":
                    result = (
                        "Package: " + u.PACKAGE + "\n"
                        "Version: " + builder.VERSION + "\n"
                        "Status: install ok installed\n"
                    )
                    return types.SimpleNamespace(returncode=0, stdout=result)
                self.fail("Unexpected subprocess command")
            installed = u.install_update(
                release, opener=lambda url, timeout: FakeResponse(data),
                runner=fake_run, progress=lambda *args: progress.append(args))
            self.assertEqual(installed, builder.VERSION)
            self.assertEqual([cmd[1] for cmd in commands], ["install", "status"])
            phases = [step[0] for step in progress]
            self.assertGreaterEqual(phases.count("download"), 1)
            self.assertEqual(phases[0], "download")
            self.assertEqual([phase for phase in phases if phase != "download"],
                             ["verify", "install", "complete"])

    def test_opkg_255_only_succeeds_when_exact_package_already_installed(self):
        # OpenATV can reject reinstalling the same test release with code 255.
        import types
        builder_path = ROOT / "tools/build_test_ipk.py"
        spec = importlib.util.spec_from_file_location("build_for_installed", builder_path)
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as tmp:
            data = builder.build(Path(tmp)).read_bytes()
            release = {"version": builder.VERSION,
                       "url": u.expected_url(builder.VERSION),
                       "sha256": hashlib.sha256(data).hexdigest(),
                       "bytes": len(data)}
            calls = []
            def runner(command, **kwargs):
                calls.append(command[1])
                if command[1] == "install":
                    return types.SimpleNamespace(returncode=255, stdout="private error")
                return types.SimpleNamespace(
                    returncode=0,
                    stdout="Package: " + u.PACKAGE + "\nVersion: " + builder.VERSION +
                           "\nStatus: install ok installed\n"
                )
            progress = []
            installed = u.install_update(
                release, opener=lambda url, timeout: FakeResponse(data),
                runner=runner, progress=lambda *args: progress.append(args))
            self.assertEqual(installed, builder.VERSION)
            self.assertEqual(calls, ["install", "status"])
            self.assertEqual(progress[-1][0], "complete")
            # A different package/version must never be accepted just on 255.
            def wrong(command, **kwargs):
                if command[1] == "install":
                    return types.SimpleNamespace(returncode=255, stdout="")
                return types.SimpleNamespace(returncode=0, stdout=(
                    "Package: " + u.PACKAGE + "\nVersion: 0.0.8~test1\n"
                    "Status: install ok installed\\n"))
            with self.assertRaisesRegex(u.UpdateError, "255"):
                u.install_update(release,
                    opener=lambda url, timeout: FakeResponse(data), runner=wrong)

    def test_corrupt_ipk_never_invokes_opkg(self):
        import types
        data = b"not-an-ipk"
        release = {
            "version": "0.0.8~test8",
            "url": u.expected_url("0.0.8~test8"),
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        }
        calls = []
        with self.assertRaises(u.UpdateError):
            u.install_update(release,
                opener=lambda url, timeout: FakeResponse(data),
                runner=lambda *args, **kwargs: calls.append(args))
        self.assertEqual(calls, [])

    def test_opkg_install_failure_stops_before_status_check(self):
        import types
        builder_file = ROOT / "tools/build_test_ipk.py"
        builder_spec = importlib.util.spec_from_file_location(
            "warder_ipk_builder_for_fail_test", builder_file)
        builder = importlib.util.module_from_spec(builder_spec)
        builder_spec.loader.exec_module(builder)
        with tempfile.TemporaryDirectory() as tmp:
            payload = builder.build(Path(tmp)).read_bytes()
            release = {
                "version": builder.VERSION,
                "url": u.expected_url(builder.VERSION),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
            calls = []
            def fake_run(cmd, **kwargs):
                calls.append(cmd[1])
                return types.SimpleNamespace(returncode=1, stdout="private output")
            with self.assertRaisesRegex(u.UpdateError, "opkg.*1"):
                u.install_update(release,
                    opener=lambda url, timeout: FakeResponse(payload),
                    runner=fake_run)
            self.assertEqual(calls, ["install"])


if __name__ == "__main__":
    unittest.main()
