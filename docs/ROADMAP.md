# Roadmap

## Phase 0 — foundation
- [x] GitHub project and architecture
- [x] Lightweight blue native navigation scaffold
- [x] Source-level automated checks
- [ ] Physical receiver smoke test

## Phase 1 — real video search
- [x] Enigma2 virtual keyboard and Search screen
- [x] Modular official YouTube Data API v3 search adapter (own API key required)
- [x] Non-blocking network worker, bounded JSON response, safe errors
- [x] Real result titles/channels and explicit next-page control
- [x] API key entry/clear in settings
- [ ] Validate on OpenATV 7.6/8.1 and OpenPLi 9.2
- [ ] Internationalize user-visible text via locale catalogues
- [ ] Evaluate lower-friction catalogue backends

## Phase 2 — graphics and usability
- [ ] 2–3 column video preview grid with bounded scaled thumbnails
- [ ] Cache and cancellation for thumbnail downloads
- [ ] Performance measurement on SF8008 and GigaBlue Quad 4K Pro

## Phase 3 — experimental playback
- [x] Compare native player integration in Taapat and Fairbird
- [x] Thin 4097/GStreamer MoviePlayer bridge (host-tested source only)
- [x] Optional yt-dlp single-muxed-MP4 resolver; isolated worker, bounded timeout, no auto-install
- [x] Tests for subprocess args, video IDs, URL validation and safe failures
- [ ] Actual live test on receiver: **not validated**
- [ ] Optional other stream backends or installation plan after footprint measurements
- [ ] Codec, DASH/HLS, quality, remote player controls, expiry recovery

## Phase 4 — user features
- [ ] Local watch history, favourites, playlists
- [ ] Optional authenticated features after security review
- [ ] Multilingual translations

## Phase 5 — delivery
- [ ] Owner-approved test IPK and install/upgrade/remove checks
- [ ] Receiver test matrix and regression suite
- [ ] No stable release without explicit approval
