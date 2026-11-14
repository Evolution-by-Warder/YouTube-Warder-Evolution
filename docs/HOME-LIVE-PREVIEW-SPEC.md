# YouTube Warder Evolution — Home live-preview blueprint

Status: **design specification only** (13 November 2026). No code or IPK release authorized by this document. Target: GigaBlue Quad 4K Pro, OpenATV 8.1, 1920 × 1080 Enigma2 native widgets. Preserve current playback, thumbnails, updater verification, and unaffected Warder skin/radio plugins.

## Product direction

The launcher becomes a two-pane **YouTube-style browser**, not a static dashboard. Remove the redundant **RÝCHLY PRÍSTUP** heading and the permanent three large feature cards. The left pane contains the eight existing menu entries. The right pane immediately previews the highlighted section on Up/Down without pressing OK. OK/Right enters the content/action and Left returns focus to the menu. Moving the focus *never* launches the keyboard, a remote request, an update, a login, or a destructive operation by itself.

### Frame geometry (Full HD coordinates)

| Region | x,y | width,height | Content |
| --- | --- | --- | --- |
| Header | 0,0 | 1920,110 | Brand at left; installed runtime version at right (check current installed opkg version; no stale hardcoded test5) |
| Navigation pane | 24,135 | 345,835 | Eight items beginning ~170; no heading; rows ~77 px, clear solid-blue active focus, legible white text |
| Main area | 392,135 | 1490,830 | Active section title, optional section-specific filters, and an inline preview |
| Main grid (where applicable) | ~413,248 | ~1450,670 | 3 columns × 2 rows; each tile has genuine 16:9 thumbnail, two-line bounded title, creator and optional metadata |
| Footer | 0,993 | 1920,87 | Four coloured buttons with *actual* context-sensitive labels, including the native keyboard |

Positions are a **wireframe**, not pixel-perfect production skin. Allow safe scaling in Enigma2. Maintain unobstructed footer and margins for overscan.

### Section navigation and right pane

| Left selection | Right pane, immediately on focus | OK / Right |
| --- | --- | --- |
| Domov | Genuine 3×2 video thumbnails (default tab **Populárne · SK** only if backend can fetch real regional popular videos); optionally **Naposledy prehrané** from local history | Move to video tiles; OK on a tile plays |
| Hľadať | Search row, last query, optionally saved recent queries / cached results, otherwise clear instructions | OK opens Enigma2 system keyboard in blue Warder local screen; no keyboard on hover |
| Odbery | If a supported subscriptions backend exists, preview channels/videos; otherwise clear *not yet supported* state, never fictional content | OK opens only a working supported action, else explanatory view |
| História | Locally stored recently played videos, thumbnails if available, 3×2 | OK/Right selects entries; MENU exposes Play/Details/Delete |
| Playlisty | Local playlists once implemented; until then show honest unimplemented state | No fake active action |
| Obľúbené | Locally saved favourite videos, 3×2; real empty state if no entries | OK/Right selects entries; MENU exposes Play/Remove/Details |
| Nastavenia | Read-only summary: API key configured/not configured (never show key), preferred quality, yt-dlp status, system language | OK enters full settings screen |
| Aktualizácie | Installed opkg version, active update channel, last-known result or *not checked*, no automatic polling on focus | OK enters update screen; only explicit user action checks/installs |

**Home source:** YouTube Data API `videos.list(chart=mostPopular, regionCode=SK, part=snippet,contentDetails)` when configured, and/or a verified compatible backend. It is a **regional popularity list, not personalized YouTube recommendations**. Do not infer "latest worldwide" from search results or claim algorithmic personalization. Without API, show a truthful offline/local fallback (recently played or favourites) and an actionable API setup option; never populate fabricated thumbnails.

## Remote behavior

- Up/Down while left pane focused: **immediate** right-pane switch, same screen, no OK needed and no modal popup.
- Right / OK from a supported list/gallery: shift focus into the content on the right. Left returns to left navigation. OK on a focused video tile plays. Up/Down/Left/Right inside the grid navigate tiles.
- Back/Red: return focus / close as appropriate. MENU on a **selected video** opens populated context actions. A disabled/empty section must not open a blank action menu.
- Coloured footer labels are section/focus-sensitive and must map to functioning remote keys; no text-free bars. The actual system VirtualKeyBoard uses StaticText *sources*, which require correct native widget/renderer binding; verify on OpenATV before release.
- Focus visible as consistent solid bright blue with high-contrast white text (avoid transparent overlays that reveal live TV pixels or produce black translucent highlights).
- Section preview updates synchronously for cached/local data; if fresh data needs network, preserve UI responsiveness, show non-blocking loading/empty/error state and protect against stale asynchronous replies when selection changes. Use a short debounce/cache so quickly scrolling eight menu items doesn't issue eight requests.

## Design and performance guardrails

- Native Enigma2 Label, Pixmap, MenuList and eLabel controls; no browser UI, animation, external renderer, custom C++ or global skin changes.
- Keep **maximum six visible thumbnail requests**, **max two download workers** and **one ePicLoad decoder**, reusing existing cache logic. Do not decode hidden pages or preload every category on cursor movement.
- Use UTF-8/SK labels with SK/CZ/DE/EN based on Enigma2 language. Wrap/cut long titles in two lines without covering channel or bottom bars; long titles remain available in detail/sidebar.
- Search opens on explicit action; retain masked API-key input; no key in logs or query metadata.
- Source-only iterative changes in `feature/native-search-v002`; no stable release or merge to `main` without owner approval; owner's standing test-IPK permission still subject to successful checks and verification on receiver.

## Acceptance criteria

1. Moving among all eight menu rows changes the right pane immediately, **without OK**.
2. "RÝCHLY PRÍSTUP" and permanent three large cards disappear. Home shows a genuine usable tiled feed or honest fallback.
3. Nav focus is a solid legible highlight with no distracting picture/TV transparency; active section and optional grid focus are visually distinct.
4. History/Favourites can be previewed from locally persisted videos; empty states make sense; unsupported sections don't pretend to work.
5. Native Search keyboard stays inside Warder-blue skin, its keys and color legends render correctly; API key remains masked.
6. Header shows actual currently installed plugin version after GUI restart, not stale `0.0.8~test5`.
7. No playback regressions, unwanted opkg changes, background-TV interruption, or excess thumbnail decoding.

This file captures the **target behavior only**. UI mockups shown in chat are schematic and not proof of actual data or finished code.
