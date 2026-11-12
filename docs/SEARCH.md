# Phase 1: YouTube search

## Current functionality

- Home -> Search opens Enigma2 VirtualKeyboard after an API key is configured.
- Search performs a real `search.list` request via the official YouTube Data API v3, with `type=video`, `part=snippet`, 15 items per page.
- Up/down choose results; OK displays metadata and a clear statement that playback is still unavailable.
- BLUE starts a new search; GREEN requests the next page; YELLOW opens API key settings; EXIT returns.
- HTTP and JSON processing run in Twisted's worker thread; callbacks update the UI on the reactor thread. Stale callbacks are ignored when the screen closes.
- The interface is **text-first** at this stage. Thumbnails/tiles and video playback remain future work.

## Configure

1. Create your own YouTube Data API key in a Google Cloud project where YouTube Data API v3 is enabled.
2. In the plugin open Settings (or YELLOW from Search). Press OK/GREEN to input or replace the key.
3. Use Search from Home, enter a search phrase using Enigma2 keyboard, and select a video result.
4. Search consumes API quota. Avoid unnecessary repeated queries.

**Privacy:** the receiver stores the key using Enigma2's ordinary settings mechanism. This storage is not encrypted; limit access to the receiver, do not share settings files, and avoid showing the keyboard while screen-sharing. We do not bundle a shared key.

The HTTP response parser ignores malformed items and does not include raw YouTube HTTP request URLs (which contain the key) in user-visible error messages. No private token or credential is committed to Git.

## Deliberately not done yet

No working playback, yt-dlp bundle, user login, subscriptions, local playlists, thumbnails or genuine Home recommendations. No IPK build/release and no guarantee of OpenATV/OpenPLi runtime compatibility until receiver testing.

Reference: https://developers.google.com/youtube/data/reference/rest/v3/search/list
