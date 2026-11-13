# YouTube Warder Evolution — development checkpoint

Approved You/Tube logo icons: 100x60 and 150x90 transparent PNG. Plugin descriptor chooses FHD above 1900 pixels, like PiconHub. Search-crash regression remains guarded by tests/test_search_modal_regression.py. Native update UI now checks the testing channel asynchronously and requires confirmation before a verified install. The testing manifest intentionally contains no release. GitHub Actions IPK packaging is manual-only; CI on push runs source tests without publishing or uploading packages. Draft PR only: no merge, public release, or production update.

## Test3 / OpenATV 7.6 + 8.1 fix

Receiver crash logs (2026-11-12) show `TypeError: 'list' object is not callable` in `Screen.deleteGUIScreen` when closing YouTube plugin screens; it calls `self.items()`. Search and Grid now store video lists as `self.video_items`, retaining the inherited Screen/dict `items()` method. Receiver test package 0.0.8~test3 includes the fix; its playback remains experimental. No merge or stable release.

## Receiver test3 feedback, 12 Nov 2026

On OpenATV 8.1, Search for "adel" succeeds and shows 15 items, but card thumbnails are blank and video playback does not start. EXIT from grid reveals the text-results screen. Development follow-up (not released): normalize yt-dlp flat thumbnails to JPEG; report unavailable thumbnail loads; allow one bounded Android public-client retry when yt-dlp explicitly reports that a pre-merged MP4 format is unavailable; make EXIT from cards return directly to Home without the duplicated list. These are compatibility attempts, not receiver-verified playback or thumbnails.

## Warder Radio proven playback architecture reuse (source only)

The Radio Warder Evolution receiver-confirmed YouTube implementation uses native MoviePlayer, backend 4097 (GStreamer), registered 5002 (Exteplayer3 DASH video+audio), HLS and up to eight candidate streams with safe return to previous service. Source adapted here as an **independent plugin implementation**, bundling the pinned GPL-2.0 extractor/interpreter, preserved COPYING.GPLv2 and NOTICE. Radio plugin itself is unmodified and is not a dependency. Primary resolution is the bounded Radio-derived extractor (360/720 MP4 preference, adaptive HLS fallback); installed yt-dlp remains a fallback when the Radio client fails. Only source is committed in Draft PR; no new IPK or public release and nothing is receiver-verified in YouTube Warder yet.

## Third-party YouTube git1296 IPK audit (2026-11-12)

User-supplied archive `enigma2-plugin-extensions-youtube_git1296_cortexa15hf-neon-vfpv4(1).ip` inspected offline only, never installed. Debian package `enigma2-plugin-extensions-youtube`, version `git1296+15a7fba0+15a7fba89b-r0`, architecture `cortexa15hf-neon-vfpv4`, declared license GPL-2.0-or-later. Its `data.tar.zst` bundles compiled Python modules (`YouTubeVideoUrl.pyc`, `YouTubeUi.pyc`, `YouTubeSearch.pyc`, etc.), PNG/SVG assets, 19 localization catalogues and `/etc/enigma2/YouTube.key` (not copied or disclosed).

Source provenance matches pinned upstream `Taapat/enigma2-plugin-youtube` commit `15a7fba89b63476177ac083b032ee499262f64fb`, already used as source attribution by our Warder Radio YouTube engine. **Do not copy the compiled .pyc binaries**. Keep the Radio-derived GPL-2.0 source and notices already bundled in the development branch.

Useful new Enigma2 detail: upstream `YouTubeUi.py` uses `AVSwitch().getFramebufferScale()` and the actual thumbnail Pixmap dimensions when invoking `ePicLoad.setPara`. Our video grid now follows that approach with bounded, safe defaults; JPEG thumbnail normalization is already in place. Screen source also documents localization, native playback controls, and backend selection; those require separate feature work and real-receiver validation.

Exclude the package's `YouTube.key`, OAuth flows, upstream resume-position `eval`, download tasks, or incompatible configuration/skin overrides. No external dependencies installed, no production merge, and no new IPK. This is an offline source-review and development improvement, not a receiver playback/thumbnail PASS.

## Next source-only playback hardening (2026-11-12)

- **Concurrent quality safety:** serialize the Radio-derived extractor while it temporarily changes plugin-local shared quality settings and its global format table. Restore the previous resolution even when resolution fails. Added paired worker regression tests for 360/720 and exception recovery; workers do not touch Enigma2 widgets.
- **Actual playback feedback:** native MoviePlayer final failure now reports that all candidate streams failed, instead of falsely showing a normal exit. Successful close and failure differ in the on-screen state. Video status now correctly mentions MP4/HLS/DASH rather than only MP4.
- **Media URL guard:** reject nonstandard HTTPS ports from the yt-dlp fallback.
- Source-only changes in Draft PR. Receiver testing remains required, no test IPK or stable release issued.

## Thumbnail native pointer / signal compatibility fix (source-only)

Both OpenATV's legacy ePicLoad PictureData.get().append and newer PictureData.connect callback patterns are now supported with proper disconnect on screen close. The receiver-proven Warder Radio pattern passes the native ePtr returned by ePicLoad.getData() unchanged to Pixmap.setPixmap rather than calling __deref__() on it. This may resolve GigaBlue 8.1 blank tiles; it remains to be tested on physical hardware. Decoder read errors fail softly without crashes, custom renderers, or extra dependencies. New host tests cover modern signal binding, pointer identity, error handling and disconnect.

## Thumbnail failure diagnostics / playback status protection (source-only)

A page may contain 0–6 thumbnails. The native grid now reports download failures separately from ePicLoad decoder failures, including partial success counts (for example `Náhľady 1/2 (sieť: 1, dekodér: 0)`). No URLs, signatures, exception reprs or API keys are exposed. A late thumbnail failure cannot overwrite an active video-resolution/playback/INFO message. User navigation resets the temporary override. Worker limits and native ePicLoad policy are unchanged. Added three mocked regression tests; receiver hardware remains unverified. No new IPK was generated.

## Page-switch thumbnail consistency / API JPEG normalization — 12 Nov 2026

Per-page thumbnail status now checks only active downloads belonging to the currently visible page. Old workers still count toward the global two-worker network limit but cannot suppress current-page completion/error diagnostics. Stale decodes from a previous page are discarded and only the single ePicLoad decoder is used. Official YouTube Data API search results now normalize thumbnails to `https://i.ytimg.com/vi/<validated-id>/mqdefault.jpg`, as the yt-dlp backend already does; this avoids untrusted/unsupported WebP sources and empty tiles when the snippet lacks a thumbnail URL. Added mock tests for rapid page switching, stale network/decode callbacks and canonical JPEG URL handling. No new IPK, release or merge.

## Native MoviePlayer lifetime guard — 12 Nov 2026 (source only)

Search now tracks `playback_active` independently from worker `busy`. While the MoviePlayer dialog is active, a second play/INFO request is rejected, preventing duplicate playback/dialog races. On native callback (normal EXIT, EOF or final stream failure), the flag is cleared; dialog creation exceptions also clear it while hiding signed stream URLs. Host regressions cover duplicate calls, failed opens and a callback after the parent screen has been disposed. No new IPK, release or merge.

## In-plugin testing feed download fix

GitHub Releases silently replaces `~` with `.` in uploaded release asset names. The installed 0.0.8~test3 updater expects `~`, so it cannot retrieve test4 from a prerelease even though the manifest and digest are correct. An update to 0.0.8~test5 uses the normalized dotted URL, while preserving the `~test5` version in the signed IPK control metadata and `opkg` version comparisons. This requires a one-time manual bridge install from test3 to test5; subsequent GitHub Releases-based opt-in testing updates will be recognized. The stable feed, skin and radio plugin are unchanged. Do not publish until package/CI verifications pass.

## GigaBlue Quad 4K Pro / OpenATV 8.1 — receiver screenshots after test5 (2026-11-12)

User supplied three receiver screenshots after being given the 0.0.8~test5 receiver package. The screenshots do not display the installed package version, so test5 is inferred from sequence, not independently read from device.

**Confirmed visually:**
- YouTube Search results for Adele rendered a 3x2 page of six actual JPEG thumbnails, correctly associated with titled video cards and working selection highlight. This resolves the previously observed empty preview cards in 0.0.8~test3.
- Native Enigma2 MoviePlayer displayed the actual opening video image for "Adele - Someone Like You (Official Music Video)" and the skin's own playback InfoBar.
- Native InfoBar reported 1920x1080 video, 16:9, a total duration of 4:44, and an AC3 indicator. A screenshot cannot independently confirm audible sound, continuous playback, seeking, or absence of buffering.
- The video grid is also visible on the third screenshot. The sequence is consistent with returning to the results, but the precise key pressed, restoration of live TV service, and EXIT behavior are not independently proven by still images.

**Remaining receiver checks:** audio actually plays; several different Adele videos play through to at least a few seconds; EXIT from MoviePlayer returns to the grid with the previous selection retained; EXIT from the grid returns to Home instead of the old text list; original DVB service restores when leaving the plugin; INFO and navigation remain responsive; Settings > Updates checks the testing manifest but does not auto-install without on-screen permission. Note the small lone '>' glyph at upper left in the player screenshot for later cosmetic assessment; do not alter native skin until reproduced.

**Do not claim** full functional PASS or stable-release readiness solely from these images. These are valuable hardware evidence of thumbnails and successful video-frame rendering, not complete audio/exit/updater verification. No further IPK, merge or stable release authorized.

### Owner follow-up — audio and playback confirmed (2026-11-12)

After the GigaBlue Quad 4K Pro / OpenATV 8.1 receiver screenshots, the owner explicitly confirmed that Adele's YouTube video **plays with sound and without issues so far**. Thus native video frame, audio output, and initial playback responsiveness are user-confirmed on real hardware; no objective long-duration stability, seek, multiple-video, network load, EXIT, DVB restore, or in-plugin updater tests have been reported. Retain Draft PR; do not infer production readiness, merge or release permission from this test feedback.

### Owner follow-up — EXIT navigation (2026-11-12)

The owner explicitly reports that returning after EXIT is **working so far** on the GigaBlue Quad 4K Pro / OpenATV 8.1. This is a positive real-device navigation observation in addition to confirmed Adele video, sound and preview thumbnails. The exact EXIT sequence/destination and restoration of the original live DVB service were not specified, so mark those finer details as **not independently confirmed**. Keep prolonged stability and in-plugin update check pending. No new IPK or stable release authorized.

### Owner follow-up — live TV service during plugin browsing (2026-11-12)

On GigaBlue Quad 4K Pro / OpenATV 8.1, the owner reports: when opening YouTube Warder Evolution, the previously tuned **TV channel continues playing in the background and its audio remains audible while browsing the plugin**. When the plugin is closed, **that channel's video picture reappears**. This is real-device confirmation that closing the plugin returns to the existing live TV picture without requiring a retune. The background TV audio is an observed UX behavior, not evidence that video playback inside the plugin is broken, and not a requested behavior change.

Do not mute/stop the TV service automatically without a separate product decision. In particular, avoid changing native MoviePlayer previous-service ownership/restoration. Video sound, thumbnails and EXIT had been reported working; longer-duration playback, multi-video transitions and the opt-in updater on a receiver remain pending. Keep Draft PR unmerged; no new IPK or stable release.

### Owner decision — keep background TV audio (2026-11-12)

After confirming that the tuned TV channel's audio continues while browsing YouTube Warder Evolution, the owner explicitly decided: **keep the TV audio playing in the background** ("kľudne ho nechaj"). This behavior is intentional and accepted. Do not add automatic mute, pause, stopService, or audio-routing changes on opening the YouTube menu. Preserve the currently working video playback and service restoration. This is a UI behavior decision, not authorization for a new IPK or stable release.

## Update menu consistency and offline test feed regressions — 12 November 2026

Home and Settings no longer claim playback depends on yt-dlp: search uses yt-dlp or an API key, while the bundled Warder Radio resolver handles video, with yt-dlp only as an optional fallback. Concise Slovak screen labels describe 360/720p quality, API key privacy, and that updates are opt-in. The in-plugin updater explicitly says the testing channel is up to date when CURRENT_VERSION equals the published testing feed. Offline tests verify the published test5 manifest points to GitHub's actual dotted asset name, future test6 offers a safe upgrade, the testing feed is selected, modified/unsigned manifests are rejected, content SHA256 is checked before download acceptance, and the exact opkg status name is matched. No new IPK or stable release.

## Offline end-to-end updater safety tests (2026-11-12)

Added mocked Enigma2 updater UI regression coverage, with no network or receiver required. The Update Check screen starts one background check (not twice on repeated onShown), displays the currently installed test version without installing, and only opens the installer after an explicit YES confirmation. Closing screens discards late worker callbacks. Progress updates use the GUI dispatch path; only a completed, verified installation schedules a GUI-only restart. Failures (including signed/private URL exceptions) show safe messages and never restart the receiver.

Expanded core tests to build a real test5 IPK in an isolated temporary directory and simulate its complete verified download/validation/opkg-install/status-check pipeline. A corrupt IPK must never invoke opkg, and an opkg failure must not be reported as installed. All installation subprocesses are mocked; no actual opkg, network, YouTube video or hardware changes are made. No IPK release or merge requested.

## Functional local favourites and watch-open history (source-only)

New user-facing features, not just mocks: the native Home menu now opens **Favourites** and **History** screens instead of "planned" placeholders. Existing search results and visual video cards support **MENU to add/remove a favourite**. Favourites and most-recently-opened History persist in a private 0600 JSON file under /etc/enigma2, with atomic writes, deduplicated valid YouTube IDs and bounded sizes (200/100). No API key, signed stream URL, thumbnail bytes, or third-party credentials are written. Both libraries can play saved videos via the existing native resolver and MoviePlayer without needing a search API key. The library supports OK playback, INFO metadata, MENU save/remove favourite, YELLOW remove selected, BLUE clear all with explicit yes/no. Browser-only operations do not interrupt live DVB audio; existing TV restoration behavior remains.

History is recorded only after the native MoviePlayer window is successfully opened (not merely when search result is selected); it is labelled "Naposledy otvorené" rather than asserting playback completion. Backend exceptions never display private stream URLs. New screens use only Enigma2's native MenuList, Labels and ActionMap with the same blue 1920×1080 palette and no custom renderer or GPU dependency. Receiver hardware has not yet tested these additions. Do not create a new IPK, alter stable channel or merge.

## Double-confirm guard for opt-in updater (source only)

Updated the existing Updates confirmation flow to ignore repeated OK/GREEN presses while a yes/no modal is open and prevent a second install progress dialog until the prior one closes. The selected release is installed only following one fresh positive confirmation. A negative confirmation or error unlocks the button, and failed modal creation yields a safe status. Mock tests cover duplicate actions, cancellation, progress close/retry, and failure-safe error handling. Search integration tests also verify favourite MENU and recording History only after MoviePlayer opens. No automatic install, IPK release or merge.

## Release to in-plugin Testing updater — 13 Nov 2026

Owner explicitly approved a test IPK release into the YouTube plugin's existing updater. Published **0.0.8~test6** as GitHub prerelease `youtube-warder-v0.0.8-test6` from `feature/native-search-v002`; the branch `update/testing.json` now points to the exact GitHub Releases-normalized asset file `enigma2-plugin-extensions-youtube-warder-evolution_0.0.8.test6_all.ipk`.

- Actual IPK control version: `0.0.8~test6`, Architecture `all`; release asset name uses `.test6` because GitHub normalizes `~` in uploaded asset names
- Size: **66,304 bytes**
- SHA256: `7adcfc9afca8f57762d861321b996e25040ac0e6748b900613bfec8527ab6242`
- CI packaging: https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/actions/runs/43375853885 (success)
- Host regressions: https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/actions/runs/43375853818 and https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/actions/runs/43375859943 (both success; 118 source tests)
- Post-release verification: feed URL exactly matched the published asset download URL, feed SHA matched the asset digest, and feed size matched the published asset size; downloaded Actions artifact IPK SHA256 and `opkg` control version were independently verified.
- After the single owner-approved release, restored the packaging workflow to `workflow_dispatch` only and read-only GitHub token permissions. **No automatic future releases**, no stable feed change, no main merge.

Receiver installation flow: **YouTube Warder Evolution → Updates → OK/GREEN → approve installation**, then GUI-only restart after success. The user's previous receiver tests of test5 (Adele FullHD, audio, thumbnails, EXIT, live TV restoration) must not be conflated with untested test6 Favourites/History and the live updater transition.

## UI redesign requested after test6 receiver screenshots — 13 November 2026

Owner supplied screenshots documenting poor Home and Settings styling, missing color-coded action legends, nonfunctional sidebar rectangles, black native Enigma2 keyboard over live-TV video, and MENU incorrectly directly toggling favourites. These are accepted UX defects rather than playback regressions. The source-only redesign is implemented with new screens and actions described in `docs/UI-REDESIGN.md`; screenshots of redesigned UI have **not** yet been taken from a real receiver. Previous test6 remains the only published testing updater release. No unapproved new IPK, stable publishing or merge.
