# Architecture and performance

UI Screen -> Controller -> Search/Catalogue / Resolver / Local Storage
Resolver -> Player adapter -> Enigma2/GStreamer

Keep YouTube HTTP/API and URL extraction separate from Enigma2 UI. Platform fixes should not force reworking the visual layout.

## Performance
- No network or subprocess calls in the main UI thread.
- Scale artwork before rendering, limit concurrency, cache size, and only load visible thumbnails.
- Avoid unnecessary redraws and background activity.
- Benchmark key press latency and memory on GigaBlue Quad 4K Pro and Octagon SF8008.

## Intended compatibility: receiver tests pending
OpenATV 7.6, 8.0.x, 8.1 (GLES on/off), OpenPLi 9.2.
No 4K, DRM, DASH, subtitles, authentication or video-playback claims until the actual receiver codec/GStreamer path passes tests.

## Release
Source and unit tests first. Test IPK only after approval. Stable release and feed require owner authorization and receiver verification.
