# YouTube – Warder Evolution

Lightweight native Enigma2 YouTube plugin with a blue Full HD interface. The priorities are remote usability, small flash footprint and compatibility with OpenATV receivers — no browser, GLES dependency or custom graphical renderer.

## Current status — 12 November 2026

- **Last owner-installed receiver build:** **0.0.8~test5** ([test-only GitHub prerelease](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/releases/tag/youtube-warder-v0.0.8-test5)).
- **Physical receiver evidence:** GigaBlue Quad 4K Pro / OpenATV 8.1. The owner confirmed YouTube Adele search results with all six thumbnails, real Full HD video, **working sound**, and successful **EXIT navigation**. When the plugin closes the TV picture returns. Original live TV audio stays audible while browsing the menu **by owner choice**.
- **New development since test5:** native **Favourites** and **History**, selectable/replayable from Home, and safe persistence. These changes exist in source on the Draft PR branch **but are not in the installed test5 IPK yet**.
- **Still unverified:** additional video formats and extended playback, INFO on receiver, new saved-video screens on hardware, SF8008/OpenATV 7.6/OpenPLi 9.2 compatibility, and a live in-plugin update to a newer prerelease.
- **No stable release, no main-branch merge.** A test IPK is prepared or published only with the owner's explicit approval.

## Functional components

- **Search:** YouTube Data API v3 with your own key, or optional preinstalled yt-dlp for public search without a key. Remote VirtualKeyboard and real results/pagination.
- **Video grid:** native 3×2 cards with six JPEG thumbnails, blue selection, and bounded network/decoder work (two workers + one native ePicLoad). MENU toggles local favourites on the development branch.
- **Video playback:** independent bundled Warder Radio-derived YouTube resolver (GPL-2.0 material with attribution), native Enigma2 MoviePlayer and bounded MP4/HLS options; DASH candidates only when registered Exteplayer3 is available. Optional yt-dlp is a **fallback**, not required for playback. EXIT restores normal navigation and the existing TV service.
- **INFO:** optional detailed title/channel/duration/views/description lookup from the official API, only if an API key is configured.
- **Settings:** API key, 360p/720p preferred limit (adaptive HLS may choose another resolution). API keys reside unencrypted in the receiver's Enigma2 settings and must not be shared.
- **Favourites / History (development source only):** save a searched video using MENU, open either list from Home, play the selected item using OK, remove with YELLOW, clear with BLUE after confirmation, and show INFO locally. History means **recently opened in MoviePlayer**, not a claim that every video was watched to completion.
- **Local privacy:** saved video titles, channel names and canonical thumbnail URLs only; no signed media URLs, credentials or video files. Up to 200 favourites and 100 recently opened items, private atomic JSON file under /etc/enigma2, retained through plugin updates.
- **Updates:** separate opt-in testing feed, strict official release URL/size/SHA256/IPK structure/version checks. No unattended install. Existing test5 is current; the new update flow and repeated-confirmation guards are host-tested but await a newer owner-approved receiver release.

## Design and validation

- Native Enigma2 Labels, MenuList, Pixmap, ActionMap and ePicLoad only; no custom renderer.
- Full HD 1920×1080 reference layout; target OpenATV 7.6, 8.0.x, 8.1 and OpenPLi 9.2. Only the GigaBlue / OpenATV 8.1 combination has the above hardware confirmations.
- Offline tests: python3 -m unittest discover -s tests -v
- Docs: [Search](docs/SEARCH.md), [Video metadata](docs/VIDEO_INFO.md), [Thumbnails](docs/THUMBNAILS.md), [Playback](docs/PLAYBACK.md), [Architecture](docs/ARCHITECTURE.md), [Roadmap](docs/ROADMAP.md), [Receiver checkpoints](docs/BRAND-AND-UPDATE-TESTING.md).
- Referenced projects: [Taapat](https://github.com/Taapat/enigma2-plugin-youtube), [Fairbird](https://github.com/fairbird/Youtube-Opensource-DreamOS), yt-dlp and our own Warder Radio Evolution. Applicable upstream attribution and licenses are retained.

**Development remains under owner review in [Draft PR #1](https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/pull/1).** The installed test5 build does not automatically gain later source edits.
