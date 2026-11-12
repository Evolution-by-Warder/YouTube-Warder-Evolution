# YouTube – Warder Evolution

**Status: 0.0.3-dev.** Lightweight blue YouTube plugin for Enigma2, under active development.

## What is implemented in source

- Native Enigma2 Home, Search, Settings and search results; no web browser or heavy renderer.
- Keyboard-based search through YouTube Data API v3 with the user's own API key.
- 15 real video titles/channels per page; next-page and error handling.
- Asynchronous resolver: **optional external yt-dlp** converts a video ID to a single muxed MP4 stream URL off the GUI thread, when available.
- An experimental native Enigma2 MoviePlayer adapter attempts playback of resolved HTTPS streams and returns to the previous TV service on exit.
- Defensive input checks, bounded subprocess timeout, URL checks and automated mocked tests.

**Not working yet or unverified:** nothing has been tested on a physical receiver; playback is experimental and depends on a compatible yt-dlp executable, Enigma2/GStreamer support and the video format. There is no bundled resolver, no automatic installation, no thumbnail grid, no account login or subscriptions, no IPK release.

## Design

- YouTube desktop navigation + TV remote usability.
- Blue palette: #08182D background, #142C47 panels, #087EC7 selection, #36B9FF accents.
- Full HD reference layout, minimal CPU and flash-space cost, native widgets, no graphic overload.
- Target OpenATV 7.6, 8.0.x, 8.1, and OpenPLi 9.2: **compatibility pending real tests**.

## Setup / developer validation

- Search currently requires your own YouTube Data API key (Settings). Enigma2 stores it **unencrypted**, so do not share settings files.
- Playback additionally requires yt-dlp installed separately and accessible on PATH, plus compatible codecs.
- [Search guide](docs/SEARCH.md) · [Playback guide](docs/PLAYBACK.md) · [Architecture](docs/ARCHITECTURE.md) · [Roadmap](docs/ROADMAP.md)
- Run: python3 -m unittest discover -s tests -v

Ideas to compare and assimilate: [Taapat](https://github.com/Taapat/enigma2-plugin-youtube), [Fairbird](https://github.com/fairbird/Youtube-Opensource-DreamOS), YouTubeMod and [yt-dlp](https://github.com/yt-dlp/yt-dlp). Source attribution and code redistribution requirements are respected.

**Development PR only. No IPK, updater feed or stable release.**
