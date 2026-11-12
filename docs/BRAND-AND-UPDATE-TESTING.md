# YouTube Warder Evolution — development checkpoint

Approved You/Tube logo icons: 100x60 and 150x90 transparent PNG. Plugin descriptor chooses FHD above 1900 pixels, like PiconHub. Search-crash regression remains guarded by tests/test_search_modal_regression.py. Native update UI now checks the testing channel asynchronously and requires confirmation before a verified install. The testing manifest intentionally contains no release. GitHub Actions IPK packaging is manual-only; CI on push runs source tests without publishing or uploading packages. Draft PR only: no merge, public release, or production update.

## Test3 / OpenATV 7.6 + 8.1 fix

Receiver crash logs (2026-11-12) show `TypeError: 'list' object is not callable` in `Screen.deleteGUIScreen` when closing YouTube plugin screens; it calls `self.items()`. Search and Grid now store video lists as `self.video_items`, retaining the inherited Screen/dict `items()` method. Receiver test package 0.0.8~test3 includes the fix; its playback remains experimental. No merge or stable release.
