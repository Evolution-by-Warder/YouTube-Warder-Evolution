# -*- coding: utf-8 -*-
"""Read actual installed opkg package version without blocking the GUI."""
import subprocess

from .update_core import PACKAGE, CURRENT_VERSION, _installed_version, version_key, UpdateError


def read_installed_version(run=subprocess.run):
    """Return installed YouTube plugin version, never a version of another IPK."""
    try:
        process = run(
            ["opkg", "status", PACKAGE],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            universal_newlines=True, timeout=3, check=False
        )
        if process.returncode != 0:
            return CURRENT_VERSION
        version, state = _installed_version(process.stdout or "")
        if not version or not state or "installed" not in state.split():
            return CURRENT_VERSION
        version_key(version)
        return version
    except (OSError, subprocess.TimeoutExpired, ValueError, TypeError, UpdateError):
        return CURRENT_VERSION
