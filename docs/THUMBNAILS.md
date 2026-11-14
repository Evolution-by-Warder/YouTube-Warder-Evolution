# Video thumbnail grid — 0.0.4-dev

A familiar desktop-YouTube style grid, optimized for Enigma2 and a TV remote.

## Rendering
- 6 fixed native Pixmap widgets (3 columns × 2 rows), text labels, and blue focus.
- The layout is Full HD 1920×1080 reference; the platform may scale it.
- Arrow keys move between cards; OK uses the existing experimental player.
- GREEN moves through the six-card pages, then requests more API results.
- BLUE opens a new search; YELLOW moves to previous six-card page.
- EXIT returns to the text-list fallback. The sidebar is decorative for now;
  sections not yet implemented must not appear actionable.

## Resource constraints
- Only visible cards cause thumbnail downloads; zero background prefetch.
- At most 2 active network fetches, 1 native ePicLoad decoder.
- Each compressed JPG/PNG is <= 240 KiB; images are decoded to 476×249.
- Disk cache only in /tmp/warder-youtube-thumbs, <= 4 MiB and 36 images.
- No persistent flash writes; eviction removes oldest cached images.
- The image worker rejects non-YouTube thumbnail hosts and invalid content.
- Page switches discard stale callbacks and hide old-page Pixmap widgets.
- Closed screens reject new GUI updates, even if a worker finishes later.

## Important limitations
The host-side tests cover source, layout rules and mocked downloads, not live
Enigma2 ePicLoad rendering. Confirm the decoder signals, focus selection,
memory budget, frame timings and close behavior on SF8008/OpenATV 7.6 and
OpenPLi before release. If it proves slow on a receiver, provide a list-only
fallback instead of adding custom C++ renderers.

Video playback remains experimental and needs a separately available yt-dlp,
a configured YouTube Data API key, and a receiver supporting the selected codec.
