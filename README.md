# YouTube – Warder Evolution

**Status: 0.0.2-dev.** Lightweight blue YouTube-oriented plugin for Enigma2, currently in development.

## What works in source

- Native Enigma2 menu, settings and video search screens; no web browser.
- Enigma2 virtual keyboard for search.
- **Real YouTube search** through official YouTube Data API v3 with **user-supplied API key**.
- Fifteen results per page, video title and channel, next page navigation.
- Network searches in Twisted worker thread, bounded responses and friendly error states.

**Not working yet:** actual playback, thumbnails/video grid, sign-in, subscriptions, history or playlists. This code has **not been tested on a receiver**, and there is **no IPK release**.

## Approved design

- Hybrid familiarity of desktop YouTube and TV remote control, with flat blue colors.
- Background #08182D, panel #142C47, selected focus #087EC7, accent #36B9FF.
- Full HD reference design, no special C++ renderers, overlay animation or heavy raster decorations.
- Target images: OpenATV 7.6/8.0.x/8.1 and OpenPLi 9.2, to be verified.

## Setup

Configure your own YouTube Data API key in **Settings**, then select **Search**. Read [search guide](docs/SEARCH.md) for details and the local-storage privacy note. Do not publish keys or account tokens in Git.

## Development

- Sources: `plugin/Plugins/Extensions/WarderYouTube`
- API documentation: [docs/SEARCH.md](docs/SEARCH.md)
- [Architecture](docs/ARCHITECTURE.md) | [Assimilation](docs/ASSIMILATION.md) | [Roadmap](docs/ROADMAP.md)
- Test without Enigma2: `python3 -m unittest discover -s tests -v`

Research references: [Taapat](https://github.com/Taapat/enigma2-plugin-youtube), [Fairbird](https://github.com/fairbird/Youtube-Opensource-DreamOS), YouTubeMod (to verify), [yt-dlp](https://github.com/yt-dlp/yt-dlp). Reuse practical ideas, preserve code provenance and attribution when incorporating upstream source.

**No build artifact or production updater feed has been created.**
