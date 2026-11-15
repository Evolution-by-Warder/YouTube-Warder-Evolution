# YouTube – Warder Evolution

## Stable release: 1.0.0 (15 November 2026)

YouTube – Warder Evolution is a native Enigma2 YouTube plugin for OpenATV and OpenPLi.

### Features
- Native Full HD remote-control UI: Home, categories, search and subscriptions.
- YouTube account sign-in, personal subscriptions, history and favourites.
- GStreamer playback fallback and ExtePlayer3 integration.
- Quick category selection, including compatibility fixes for different Enigma2 MenuList APIs.
- Automated IPK installation checks for ServiceApp, ExtePlayer3, Python modules and yt-dlp.
- Telnet installation/upgrade/uninstall messages with clear status and GUI restart instruction.

### Compatibility testing
- OpenATV 7.6: functional testing performed.
- OpenPLi 9.2: functional testing performed.
- OpenPLi Scarthgap (GigaBlue Quad 4K Pro): RC4 user-confirmed functional; RC6 upgrade completed without package-manager error.
- Receiver-side test of the final stable 1.0.0 IPK remains to be confirmed.

### Installer notes
`opkg` installs the ServiceApp and ExtePlayer3 package dependencies.
After `opkg` exits, the dependency helper verifies Python modules and yt-dlp. On applicable OpenPLi images it can install `python3-profile`, `python3-pip`, and `python3-certifi` as necessary, then install a compatible yt-dlp version.
Logs: `/tmp/warder-youtube-deps.log`. An Internet connection and working feeds are required for missing dependencies.

### Release package
`enigma2-plugin-extensions-youtube-warder-evolution_1.0.0_all.ipk`

SHA-256: `cb04ded085350681937a1c59d3af893be13dadc8dcaad77bfa26922f2e2b64cd`

Release notes: [RELEASE_NOTES_1.0.0.md](RELEASE_NOTES_1.0.0.md).

**Repository note:** Parts of this repository still contain the earlier development scaffold. The binary artifact and full current source tree are not yet uploaded to the repository. Do not mistake older development sources here for the exact source tree of the 1.0.0 release package.

### Background
The UI uses a lightweight blue style, native Enigma2 controls, and a 1920×1080 layout. Third-party component licenses and attributions must be preserved.
