## Current development checkpoint: 0.0.8~test51 (14 November 2026)

Source reconciled from the exact receiver-tested test50 IPK. The owner accepted
Home video rotation in test50 and the test47+ shared 477×350 tile/focus geometry,
473×248 artwork and 24 px row gap. Those layout files and PNGs are SHA256-pinned;
new packages must retain them byte-for-byte. Playlists stay removed.

Test51 improves retry after subscription-service outages, distinguishes explicit
OAuth expiry from temporary errors, clears stale upload caches on refresh, and
prevents queued token saves after login cancellation. It does not claim private
video playback or personal web-Home recommendations. The app TV OAuth identity
is intentionally empty; real-account login remains pending legitimate developer
configuration and receiver verification. No stable release or main merge.

See `docs/TEST51-RECONCILIATION.md` for exact scope and validation.

---

# YouTube – Warder Evolution

Native Enigma2 YouTube plugin with Warder blue Full HD interface. No browser,
GLES dependency or custom C++ renderer. Real search and playback, an optional
API key or preinstalled yt-dlp, native remote control and a small IPK footprint.

## Current test release — 13 November 2026

- **Latest owner-confirmed GigaBlue build:** **0.0.8~test24** on GigaBlue Quad 4K Pro / OpenATV 8.1.
  The owner confirmed the two-panel Home, genuine **Enigma2 system keyboard**
  inside the right-hand Search panel, direct search→video results without
  the old blank intermediary screen, BLUE **New search** returning to the
  same two-panel keyboard and clearing the previous search phrase.
- **Official opt-in TESTING prerelease:** [v0.0.8~test24](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/releases/tag/youtube-warder-v0.0.8-test24).
  The GitHub build contains **all 54 installable data members and all opkg
  maintainer scripts byte-for-byte identical** to the owner-accepted test24
  receiver package. The outer IPK archive can have a different hash due to
  repackaging; the installed files are unchanged.
- **Approved Warder header:** single original 1920×152 PNG, SHA-256
  `93b509055bfe63e1126ccca27f324829d8a2e0c6bbdd3d10976b30d7cf70935c`,
  committed as the actual source asset — **no title mask, redrawn artwork,
  overlay, or image regeneration**. All 12 screens reuse the same header;
  weekday/date/time/version remain live Enigma2 widgets.
- **Published IPK:** 552512 bytes, SHA-256
  `b7692b1ecd681b60e653f894d062c06a5bbf08ab5363594ecf2a353d6e79f459`.
  The testing updater pins the exact official release URL, size and checksum.
- **Validation:** 207 host unit/regression tests PASS; source and scaffold
  CI checks green. Receiver appearance, embedded keyboard and search
  transitions have owner acceptance on GigaBlue/OpenATV 8.1.
- **No stable release, no `main` branch merge.** Work continues in
  `feature/native-search-v002` and [Draft PR #1](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/1).

### What still needs device testing

Complete end-to-end favourites/history workflows, multi-video playback and
EXIT/TV restoration across more sources, optional detailed INFO, update/
reinstall/remove operations, and compatibility on SF8008 / OpenATV 7.6 /
OpenPLi 9.2 are **not** claimed as accepted from the GigaBlue test24 screenshots.
The owner's earlier test5 confirmed actual Adele videos with Full HD picture,
sound and working EXIT restoration on GigaBlue; broader testing is pending.

## Features in test24

- **Search:** original firmware VirtualKeyBoard displayed inside Home's
  right panel on highlighting Hľadať. Arrows select keys, OK inserts, Shift
  and locale follow the receiver, green searches using YouTube Data API v3
  (with a configured key) or optional yt-dlp (if already installed).
- **Video results:** real paginated YouTube results, 3×2 native video grid,
  JPEG thumbnails, remote focus, blue new-search action and bounded
  thumbnail loading (two workers + one native ePicLoad).
- **Playback:** bundled Warder Radio-derived GPL-2.0 YouTube resolver, native
  Enigma2 player, bounded MP4/HLS candidates and DASH only with a registered
  compatible external player. Optional yt-dlp is not a required dependency.
- **Local favourites and history:** explicit saving/removal/clearing via native
  UI; history records successfully **opened** video sessions, not completed
  watches. Up to 200 favourites and 100 recent items. JSON under
  `/etc/enigma2` retains titles/channels/thumbnail URLs, not signed media
  URLs, API keys or video files.
- **INFO:** detailed metadata requires your API key; otherwise local video
  title/channel are available. Configurable quality preference.
- **Settings:** an API key can be configured locally; it is kept **unencrypted**
  in receiver settings and should not be shared. Avoid screenshots/logs
  containing it.
- **Updates:** opt-in testing feed only, strict URL/version/size/SHA256,
  opkg control/member validation, explicit user confirmation, no unattended
  upgrades. Accepted test24 is published in the testing channel.

## Installation and verification

Download the **test-only** IPK from the release above, copy it to `/tmp`,
and install it with:

```sh
opkg install '/tmp/enigma2-plugin-extensions-youtube-warder-evolution_0.0.8.test24_all.ipk'
```

Then restart the Enigma2 GUI. The GitHub asset file name uses `.test24`
(normalized by GitHub); the installed opkg control version is `0.0.8~test24`.
Do not treat testing releases as stable receiver updates.

Host validation from the GitHub branch:

```sh
python3 -m unittest discover -s tests -v
python3 tools/build_test_ipk.py --output dist
cd dist && sha256sum -c *.sha256
```

The build checks the **exact approved image digest**, not an approximate
re-render. See [approved header provenance](docs/APPROVED_YOUTUBE_HEADER.md),
[playback](docs/PLAYBACK.md), [architecture](docs/ARCHITECTURE.md),
[roadmap](docs/ROADMAP.md) and [receiver checkpoints](docs/BRAND-AND-UPDATE-TESTING.md).

Upstream references and required GPL-2.0 attributions for Taapat, Fairbird,
Warder Radio-derived components and yt-dlp integrations are retained.
