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

SHA-256 of local release package: `a327cb501ae6a16cba0600f695fc0897c07eac91bd5802a2ea9f19e4848cc5e4`.

**Publication status:** The release workflow builds the IPK from the checked-in sources, uploads it to a stable GitHub Release, and publishes the verified update manifest after successful publication.
