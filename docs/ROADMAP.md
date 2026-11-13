# Roadmap

## Phase 0 — foundation
- [x] GitHub project and architecture
- [x] Lightweight blue native navigation scaffold
- [x] Source-level automated checks
- [x] GigaBlue Quad 4K Pro / OpenATV 8.1 smoke test: thumbnails, Adele Full HD video, audio, EXIT

## Phase 1 — real video search
- [x] Enigma2 virtual keyboard and Search screen
- [x] Modular official YouTube Data API v3 search adapter (own API key required)
- [x] Non-blocking network worker, bounded JSON response, safe errors
- [x] Real result titles/channels and explicit next-page control
- [x] API key entry/clear in settings
- [x] OpenATV 8.1 on GigaBlue visually and audibly confirmed
- [ ] Validate on OpenATV 7.6/8.0.x and OpenPLi 9.2
- [ ] Internationalize user-visible text via locale catalogues
- [x] Implement optional yt-dlp public search without a Google API key
- [x] On-demand INFO button: metadata from videos.list, async worker and native MessageBox
- [x] Live search/thumbnail test with repository Actions secret
- [ ] Receiver test for INFO and video metadata
- [ ] Validate no-key search with an installed yt-dlp on supported receivers

## Phase 2 — graphics and usability
- [x] Native 3 × 2 thumbnail grid with blue remote focus — six cards confirmed on GigaBlue
- [x] Two worker downloads, single ePicLoad decoder, stale-result guards and bounded 4 MiB /tmp cache
- [ ] Performance measurement on SF8008 and GigaBlue Quad 4K Pro

## Phase 3 — experimental playback
- [x] Compare native player integration in Taapat and Fairbird
- [x] Thin 4097/GStreamer MoviePlayer bridge (host-tested source only)
- [x] Optional yt-dlp single-muxed-MP4 resolver; isolated worker, bounded timeout, no auto-install
- [x] Tests for subprocess args, video IDs, URL validation and safe failures
- [x] Real yt-dlp extraction attempted from GitHub Actions: inconclusive (anti-bot restriction on one public video), not a pass
- [x] Native 360p/720p maximum quality setting with safe, muxed MP4 formats
- [x] Actual live playback on GigaBlue/OpenATV 8.1: Adele Full HD video, sound, EXIT confirmed
- [ ] Extended playback, seeking, multiple video/audio formats and fallback stream failure recovery
- [ ] Optional other stream backends or installation plan after footprint measurements
- [ ] Codec, DASH/HLS, quality, remote player controls, expiry recovery

## Phase 4 — user features
- [x] Local favourites and recently opened History — source implementation and host tests
- [ ] Receiver test of favourites/history (test6 prerelease published 13 Nov 2026; pending owner test)
- [ ] Playlists and other account-independent features
- [ ] Optional authenticated features after security review
- [ ] Multilingual translations

## Phase 5 — delivery
- [x] Owner-approved test IPK 0.0.8~test5 installed, basic video/audio/EXIT confirmed
- [x] Source-level IPK and opt-in updater tests with mocked opkg
- [ ] Live updater test from test5 to published test6 (owner-approved prerelease; pending real receiver confirmation)
- [ ] Real install/upgrade/remove matrix on other image versions
- [ ] Receiver test matrix and regression suite
- [ ] No stable release without explicit approval
