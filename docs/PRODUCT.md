# Approved product vision

A familiar YouTube-like experience with desktop sidebar/search/grid and Smart TV focus-based remote navigation.

## Blue native Enigma2
Background #08182D. Panels #142C47. Selected item #087EC7. Accent #36B9FF.
Full HD 1920×1080 layout, legible text, no visual overload.

## Constraints
- Use existing Screen, Label, MenuList, Pixmap and ActionMap primitives.
- Avoid layered translucent windows, gradients, live animated effects, custom GLES-only renderers, and heavy image decoding.
- Remote arrows move selection; OK activates; EXIT returns; color keys are practical shortcuts.
- Keep design uniform across skins and images, and make it performant on SF8008.
- Present actual videos only when a real and validated backend is available.

Planned: Home, Search, Subscriptions, History, Playlists, Favourites, Settings; video grid, thumbnail and metadata, playback controls. Most are not yet implemented.
