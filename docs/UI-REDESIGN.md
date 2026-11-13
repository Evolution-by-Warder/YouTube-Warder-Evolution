# Warder YouTube — native UI overhaul, 13 November 2026

## Why this source-only revision exists

Owner supplied GigaBlue Quad 4K Pro / OpenATV 8.1 screenshots of the running **0.0.8~test6** and reported that the Search, Home, Settings, Updates and results UI did not meet Warder standards. Actual playback, JPEG thumbnail decoding, TV-audio background behavior and EXIT were already working and must not be disrupted.

## Changes implemented in the development branch

- **Home:** a native, information-rich blue Warder dashboard rather than a mostly empty area, with a defined navigation list, three informative feature cards and a visible four-color remote action bar. No custom renderer or browser, just native Enigma2 widgets/eLabels.
- **Search keyboard:** replaces the default dark/transparent Enigma2 VirtualKeyboard with a full-screen branded on-plugin 50-key layout. Remote arrows move focus, OK inserts a character, numeric keys insert digits, MENU toggles letter case, RED cancels, GREEN accepts, YELLOW backspaces, BLUE inserts a space. When entering the API key the text is masked and the previously stored key is never pre-filled into the editor.
- **Search results grid:** native 3×2 thumbnails and single ePicLoad decoder are preserved; old fake/non-actionable sidebar menu rectangles have been replaced with **selected video title, channel, result count and an explicit MENU hint**. Sidebar labels are raised above panels to address blank text layering in supplied screenshots.
- **MENU:** selecting a video now opens a branded **context menu** with Play, Add/Remove Favourite, Info and New Search. MENU no longer directly changes saved favourites. History and Favourites have contextual actions for removing and clearing entries.
- **Settings:** two compact functional sections for search/API key and playback plus a privacy area, not lines spread across the whole screen. All core action buttons are visible.
- **Updates:** full-width native action legend identifies RED Back, GREEN Install when a verified update exists, YELLOW Details, BLUE Refresh. Prevents duplicate install confirmations; native yes/no panel replaces the unstyled Enigma popup. Upload/download still use the original strict SHA256 verification and actual opkg version check.
- **Info and confirmation:** the plugin now uses its own native full-screen screens instead of standard dark Enigma2 information/confirmation windows for supported YouTube video actions, clearing saved data and the updater.
- **Languages:** the principal menu titles, commands, key legends and many status messages derive from the currently selected Enigma2 language with SK, CZ, DE and EN support and English fallback. Some backend diagnostic messages and release-specific update notes remain provider-supplied and can require further translation; do not claim complete language catalogue coverage.

## Native action map

| Screen | RED | GREEN | YELLOW | BLUE | MENU |
|---|---|---|---|---|---|
| Home | Close | Open selected section | History | Updates | — |
| Search results grid | Home/Back | Next results | Previous results | New Search | Video context actions |
| Search text fallback | Back | Next | Settings | New Search | Video context actions |
| Warder keyboard | Cancel | Submit | Delete character | Insert space | Toggle case |
| Settings | Back | Edit API key | Remove API key (confirm) | Switch 360/720p | — |
| Updates | Back | Install (when available) | Details | Recheck | — |
| Favourites / History | Back | Play | Remove selected | Clear list (confirm) | Context actions |

## Safety and rollout

The current owner-published updater package is **0.0.8~test6** and must remain unchanged until the owner explicitly authorizes another IPK. All UI changes here are **source-only**, in Draft PR #1, and have not been loaded on the actual receiver. The Enigma2/GLES/OpenATV compatibility of the new keyboard and layouts, performance on SF8008, and visual legibility of new 1920×1080 screens still need real-device confirmation. No new custom renderer, external imagery, new web dependencies, restarted live DVB service or stable update feed changes were introduced.

Run offline: python3 -m unittest discover -s tests -v.
