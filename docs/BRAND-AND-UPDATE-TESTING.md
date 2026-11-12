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
