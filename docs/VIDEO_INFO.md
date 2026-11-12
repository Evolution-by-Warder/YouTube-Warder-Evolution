# On-demand video details — 0.0.6-dev

Press INFO on a selected video in the native 3×2 grid or the text-results
fallback. If a personal YouTube Data API key is configured on the receiver,
the plugin fetches one record via \`videos.list\`: title, channel, duration,
view count and short description.

- No extra calls when moving focus with arrow keys.
- JSON/HTTP are processed in a worker, not on the Enigma2 GUI thread.
- A missing API key shows existing title/channel locally and explains how to
  enable richer details. No API key is injected into a public IPK.
- Video info uses about 1 Data API quota unit per call; the search API
  typically costs 100 units per request.
- The live CI smoke test uses the repository Actions secret for one search,
  one video-details request and one official thumbnail, without logging
  credentials, actual video URLs or signed stream URLs.
- Validated on GitHub CI but **not yet verified on an Enigma2 receiver**.

The optional yt-dlp search backend does not automatically enable detailed
YouTube Data API information; it can still provide titles and channel names.
