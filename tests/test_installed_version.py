"""Only the installed YouTube package can identify the live UI version."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions/WarderYouTube"


def load():
    package = types.ModuleType("_installed_test")
    package.__path__ = [str(ROOT)]
    with patch.dict(sys.modules, {"_installed_test": package}):
        spec = importlib.util.spec_from_file_location(
            "_installed_test.installed_version", ROOT / "installed_version.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module


class Process:
    def __init__(self, content, code=0):
        self.stdout = content
        self.returncode = code


class InstalledVersionTests(unittest.TestCase):
    def test_installed_version_comes_from_exact_package(self):
        m = load()
        def run(args, **kwargs):
            self.assertEqual(args, ["opkg", "status", m.PACKAGE])
            self.assertEqual(kwargs["timeout"], 3)
            return Process(
                "Package: another-plugin\nVersion: 99.0\nStatus: install ok installed\n\n"
                "Package: %s\nVersion: 0.0.8~test9\nStatus: install ok installed\n" %
                m.PACKAGE
            )
        self.assertEqual(m.read_installed_version(run=run), "0.0.8~test9")

    def test_missing_broken_or_other_package_never_changes_runtime_version(self):
        m = load()
        for output in (
            "Package: unrelated\nVersion: 99.0\nStatus: install ok installed\n",
            "Package: %s\nVersion: invalid\nStatus: install ok installed\n" % m.PACKAGE,
            "Package: %s\nVersion: 0.0.8~test9\nStatus: deinstall ok config-files\n" % m.PACKAGE,
        ):
            self.assertEqual(m.read_installed_version(run=lambda *a, **kw: Process(output)),
                             m.CURRENT_VERSION)
        self.assertEqual(
            m.read_installed_version(run=lambda *a, **kw: Process("", 1)),
            m.CURRENT_VERSION
        )

    def test_opkg_error_is_nonfatal(self):
        m = load()
        def fail(*args, **kwargs):
            raise OSError("not installed")
        self.assertEqual(m.read_installed_version(run=fail), m.CURRENT_VERSION)


if __name__ == "__main__":
    unittest.main()
