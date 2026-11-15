# Assimilation register

Source | Best concepts to evaluate | Research decision
--- | --- | ---
Taapat/enigma2-plugin-youtube | Enigma2 navigation, API, account, video URL code | Verified native MoviePlayer + eServiceReference playback; don't duplicate large UI
fairbird/Youtube-Opensource-DreamOS | DreamOS improvements, API/search/resolver, packaging | Verified same native player pattern; extraction is based on older youtube-dl logic
YouTubeMod | DASH, audio, subtitles, player behavior | Identify canonical sources and test on hardware before importing
yt-dlp | Maintained stream extraction and format metadata | Optional external backend prototype; no bundled copy; CPU/RAM/flash implications must be measured

## Decisions

- Use a thin **original** Enigma2 MoviePlayer adapter with GStreamer service type 4097 and `fromMovieSelection=False` first.
- Resolve URLs only off the UI thread, with strict video-ID checks and fail-closed, limited HTTPS media-host validation.
- Experimental yt-dlp adapter uses a single muxed MP4, ideally H.264 with audio at <=720p, to maximize first-pass receiver compatibility.
- Do not claim guaranteed YouTube playback or ship a large extractor until receiver compatibility, JavaScript-runtime requirements and footprint are known.
- Continue evaluating Taapat, Fairbird and YouTubeMod alternatives for a lightweight fall-back.
- For any actual imported code, document its origin, revision, author and redistribution obligations. No upstream plugin source has been copied into our original 0.0.3-dev scaffold.

Project links:
https://github.com/Taapat/enigma2-plugin-youtube
https://github.com/fairbird/Youtube-Opensource-DreamOS
https://github.com/yt-dlp/yt-dlp
