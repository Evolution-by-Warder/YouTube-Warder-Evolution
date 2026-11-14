# YouTube Warder Evolution 0.0.8~test14 — receiver QA

Development test candidate only. No stable release and no merge to `main`.

## Changes requested from GigaBlue/OpenATV 8.1 screenshots

1. **Entire plugin:** all 12 native screens now use the Glass System Utility–style bottom shortcuts: four short red/green/yellow/blue lines, matching colored labels on the dark footer, and *no filled colored rectangles*. This includes the native search keyboard.
2. **Header:** original Warder skull fully placed above the divider without the added artificial lower-jaw alpha fade; live clock and date still use native Enigma2 labels.
3. **Home:** six tiles are the *visible page size*, not a hardcoded catalog. Fetches up to 24 genuine current YouTube regional videos per request using the user-supplied Data API key (`videos.list chart=mostPopular regionCode=SK`) or public anonymous YouTube initial data without an API key. Page navigation by right/down/up, real page count, and bounded 10-minute refresh on returning to Home. If live YouTube is unavailable, offline history/favourites are clearly labelled rather than invented as trending.
4. **Thumbnail restoration:** bounded native ePtr caches reapply images after a modal context window, returning from playback, or switching between Home, History, and Favourites. No unbounded image cache or extra background downloader; two workers / one ePicLoad decoder remain.
5. **Opaque selection:** custom native Label focus rows replace transparent Enigma MenuList selection in confirmation and video actions; search/library listbox fallbacks explicitly have a solid Warder blue selected background.
6. **Text clipping/overlap:** title/channel boxes in Home and the search-result grid have usable two-line height; search heading is shorter and update-progress version/phase/progress labels no longer cross the update panel's top border.
7. **Updater:** query the actual `opkg status` version in a worker to avoid offering a version already installed while stale GUI modules are still running. If `opkg install` returns 255, accept it as already installed **only** after a second exact package/version/installed-state check; otherwise still report error safely.

## Receiver manual checks

- Compare header skull's jaw and divider with the supplied Warder reference.
- Verify colored text/three-pixel lines and *absence* of big rectangles on Home, Search, Grid, History, Favourites, Settings, Updates, update confirmation, video context, info and both keyboards.
- Move through menu and video tiles; check active highlight always fully opaque.
- Open/close MENU, INFO and confirmation; thumbnails remain on screen after return.
- Move to the second/third page of live Home recommendations when at least seven items are returned; genuine titles, channels and pictures change per page.
- Open History and Favourites; verify thumbnails and compact selected focus on return.
- Search for a long video title; two lines of text should not overlap channel text.
- Verify update-progress title below the top border and no replay of an already-installed version.
- Check that EXIT/colored remote buttons and current TV audio/playback still function.

Source CI and a successful package build are *not* the same as confirmation on physical hardware.
