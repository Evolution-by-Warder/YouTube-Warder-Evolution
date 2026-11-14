# YouTube Warder Evolution — test15 focused video borders (receiver test)

This test candidate retains the verified test14 changes and applies the owner's latest GigaBlue visual feedback.

## Actual implementation
- **Home, History, Favourites:** inactive video-card outline reduced from a thick bright turquoise 5 px band to a **2 px dark blue (#0D5273)** band. The inner native panel expands from 467×314 to 473×320 within the unchanged 477×324 card frame.
- **Search results grid:** all six native cards use **1 px dark blue (#0D536F)** inactive outlines instead of always-bright 2 px cyan. The previously filled blue selection box becomes a **491×364 transparent-centre PNG focus frame** shown only around the actually selected video.
- **Selected card (all four video views):** native high-layer PNG border uses a bright icy-cyan 2 px perimeter, 3 px strong turquoise line and restrained glow. Image and metadata stay unobstructed; only the selected tile uses the accent. No custom Enigma renderer, CSS, C++ or runtime graphics.
- **Runtime behaviour unchanged:** two thumbnail download workers, one ePicLoad decoder, existing native remote key navigation and bounded in-memory thumbnails. The added `grid_focus.png` is built once using standard-library Python and included in the IPK.
- **Scope:** Home panel also serves History/Favourites; separate Grid panel serves search results.

## Receiver visual acceptance
1. Look at six Home tiles: nonselected cards should recede visually.
2. Press RIGHT to enter tiles, then arrows: one clear icy/turquoise frame follows selection and never appears on another card.
3. Repeat in History and Favourites, including cards without thumbnails.
4. Search for a video and navigate the results grid; the bright frame must follow selection, while the video and title remain fully legible.
5. Test leaving a context menu and coming back, ensuring thumbnail restoration from test14 still works.
6. Confirm thin colored bottom shortcut lines and labels on all 12 screens remain intact.

No change to main or stable. CI builds cannot substitute for GigaBlue/OpenATV receiver visual acceptance.
