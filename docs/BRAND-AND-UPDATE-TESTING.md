# YouTube Warder Evolution — development checkpoint

Approved You/Tube logo icons: 100x60 and 150x90 transparent PNG. Plugin descriptor chooses FHD above 1900 pixels, like PiconHub. Search-crash regression remains guarded by tests/test_search_modal_regression.py. Native update UI now checks the testing channel asynchronously and requires confirmation before a verified install. The testing manifest intentionally contains no release. GitHub Actions IPK packaging is manual-only; CI on push runs source tests without publishing or uploading packages. Draft PR only: no merge, public release, or production update.

## Test3 / OpenATV 7.6 + 8.1 fix

Receiver crash logs (2026-11-12) show `TypeError: 'list' object is not callable` in `Screen.deleteGUIScreen` when closing YouTube plugin screens; it calls `self.items()`. Search and Grid now store video lists as `self.video_items`, retaining the inherited Screen/dict `items()` method. Receiver test package 0.0.8~test3 includes the fix; its playback remains experimental. No merge or stable release.

## Receiver test3 feedback, 12 Nov 2026

On OpenATV 8.1, Search for "adel" succeeds and shows 15 items, but card thumbnails are blank and video playback does not start. EXIT from grid reveals the text-results screen. Development follow-up (not released): normalize yt-dlp flat thumbnails to JPEG; report unavailable thumbnail loads; allow one bounded Android public-client retry when yt-dlp explicitly reports that a pre-merged MP4 format is unavailable; make EXIT from cards return directly to Home without the duplicated list. These are compatibility attempts, not receiver-verified playback or thumbnails.

## Warder Radio proven playback architecture reuse (source only)

The Radio Warder Evolution receiver-confirmed YouTube implementation uses native MoviePlayer, backend 4097 (GStreamer), registered 5002 (Exteplayer3 DASH video+audio), HLS and up to eight candidate streams with safe return to previous service. Source adapted here as an **independent plugin implementation**, bundling the pinned GPL-2.0 extractor/interpreter, preserved COPYING.GPLv2 and NOTICE. Radio plugin itself is unmodified and is not a dependency. Primary resolution is the bounded Radio-derived extractor (360/720 MP4 preference, adaptive HLS fallback); installed yt-dlp remains a fallback when the Radio client fails. Only source is committed in Draft PR; no new IPK or public release and nothing is receiver-verified in YouTube Warder yet.
