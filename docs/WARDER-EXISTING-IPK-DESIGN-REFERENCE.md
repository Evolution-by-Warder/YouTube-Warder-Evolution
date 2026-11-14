# YouTube Warder Evolution — proven Warder visual system from owner IPKs

Source artifacts supplied by owner (13 Nov 2026):
- `enigma2-plugin-skins-fullhdglass_1.0.80_all.ipk`
- `enigma2-plugin-extensions-radio-warder-evolution_0.1.9.4_all.ipk`
- `enigma2-plugin-extensions-piconhub_0.1.41_all.ipk`
- `enigma2-plugin-extensions-gsu_13.41-r4_all.ipk`

All four Debian/opkg archives were inspected offline, including `data.tar.gz` contents, and the actual PNG assets and native Enigma2 XML. **No other installed plugin is modified** by this reference.

## Source findings

| Existing product | Real background or header reference in its IPK | Geometry / behavior |
|---|---|---|
| Glass System Utility | `usr/lib/enigma2/python/Plugins/Extensions/GlassSysUtil/images/warder-main.png` | 1671 × 941 RGB background with skull, branded banner and planet; runtime text in `GSU_skins_FHD.py` |
| Radio Warder Evolution | `usr/lib/enigma2/python/Plugins/Extensions/WarderRadio/artwork/background.png` | 1672 × 941 RGB complete designed background with pre-rendered Warder Radio title; `skin.py` draws **native opaque 2 px cyan borders** around three panels and positions live header labels |
| Warder PiconHub | `usr/lib/enigma2/python/Plugins/Extensions/WarderPiconHub/images/warder-background.png` | 1672 × 941 RGB complete branded background; `warder_layout.py` uses **native `global.CurrentTime`** and normal Label/Converter widgets for weekday, date, hour/minute, seconds |
| FullHDGlass Warder Evolution | `usr/lib/enigma2/python/Plugins/Extensions/setupGlass17/images/warder-settings-background.png` | 1671 × 941 RGB; a custom `WarderSettingsHeader` renderer exists for its own skin, **must not be imported into YouTube** |

### Important design requirements

1. Use **one approved Warder family style**, not a new painted skull, new font pack or alternate blue theme. Derive visual proportions from the real owner assets; do not bundle another plugin or reference another plugin's live installed directories.
2. Top left: skull emblem and the correct **YouTube Warder Evolution** product name; the other products' baked-in labels (PiconHub, Glass System Utility, Warder Radio) are **not suitable to copy unchanged**.
3. Top right: **localized weekday, localized date, live clock with seconds and version**. Dynamic native text, not baked into a PNG. Prefer native `global.CurrentTime` and built-in `Label`/standard converters where compatible; if a bounded timer is required, attach it once per visible screen and stop on hide/close.
4. Top horizontal cyan edge; content frame borders **2 px** in cyan, rendered by plain `eLabel` strips as done in Radio rather than new renderers. Highlight/focus should remain visible in solid blue, without TV transparency.
5. Home, History, Playlists, Favorites, Search results all use the same frame treatment. Individual 3×2 video tiles have thin **static** borders with brighter selected focus, and thumbnail/title/channel boundaries stay readable.
6. Keep the dynamic area in native Enigma2 widgets; image assets are decoded once and reused. No animated background, new C++, shader, continuous redrawing, per-tile canvas, or external renderers.
7. The packaged artwork is 1671/1672×941, whereas current YouTube skin uses 1920×1080: **scale consciously**, not blindly using `pixmap` at mismatched coordinates. The original top band is ~134 px high in the 941px source (155 px in 1080 after uniform scale).
8. Keep YouTube's own plugin icon, playback engine, API secret storage and controls isolated.

### Implementation staging

- Stage 1 — Extract/prepare a *small product-specific* header from the approved Warder-family source motif: skull at left, cyan/planet at right, no baked-in clock/version or *other product* title; avoid needless full-screen 1.5 MB background when a pre-rendered banner is sufficient.
- Stage 2 — Wire one shared layout fragment into **all 12 screens**, with real version and native time labels; remove conflicting legacy top text elements. Keep content below the actual 155 px FHD header and prevent overlap.
- Stage 3 — Apply thin native edges on each primary panel and video tile, including History, Playlists and Favourites. Check under GLES on/off where possible.
- Stage 4 — Confirm with owner on GigaBlue OpenATV 8.1, including the currently unresolved native keyboard text insertion issue, *before* any stable release or main merge.

**Do not claim this documentation means the graphical release is already finished or receiver-verified.**
