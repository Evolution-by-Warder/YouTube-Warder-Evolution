# YouTube – Warder Evolution 1.0.0

First stable IPK package, finalized from the tested RC6 build on 15 November 2026.

## Highlights
- Home with categories, search and video grids
- YouTube account sign-in, subscriptions, history and favourites
- GStreamer and ExtePlayer3 playback paths
- MenuList compatibility fix across OpenPLi and OpenATV
- Automatic ServiceApp / ExtePlayer3 package dependencies, Python module checks, yt-dlp bootstrapping
- Detailed Telnet installation, upgrade and removal messages
- Corrected IPK archive layout; obsolete-root-entry warning eliminated during RC4-to-RC6 upgrade

## Tested
- OpenATV 7.6; OpenPLi 9.2: user functional tests
- OpenPLi Scarthgap: user tests of RC4, clean automated yt-dlp installation, and RC6 upgrade
- Stable 1.0.0 still requires final in-device smoke testing

## Installation
```sh
opkg install /tmp/enigma2-plugin-extensions-youtube-warder-evolution_1.0.0_all.ipk
```
Restart Enigma2 GUI after installation. Dependency provisioning runs after the opkg transaction finishes. Check `/tmp/warder-youtube-deps.log` if needed.

SHA-256 of local release package: `cb04ded085350681937a1c59d3af893be13dadc8dcaad77bfa26922f2e2b64cd`.

**Publication status:** This document records the local 1.0.0 package; attaching the IPK to a GitHub Release and synchronizing the full latest source code are separate pending steps.
