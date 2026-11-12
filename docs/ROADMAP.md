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
- [ ] Explore optional alternatives to user-provided API key without claiming reliability

## Phase 2 — graphics and usability
- [ ] 2–3 column video preview grid with bounded scaled thumbnails
- [ ] Cache and cancellation for thumbnail downloads
- [ ] Performance measurement on SF8008 and GigaBlue Quad 4K Pro

## Phase 3 — real video playback
- [ ] Compare Taapat, Fairbird, YouTubeMod, yt-dlp extractors
- [ ] Modular resolver and Enigma2 player integration
- [ ] Codec, DASH/HLS, quality, remote player controls and expiry recovery

## Phase 4 — user features
- [ ] Local watch history, favourites, playlists
- [ ] Optional authenticated features after security review
- [ ] Multilingual translations

## Phase 5 — delivery
- [ ] Owner-approved test IPK and install/upgrade/remove checks
- [ ] Receiver test matrix and regression suite
- [ ] No stable release without explicit approval
