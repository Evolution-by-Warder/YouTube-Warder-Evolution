# Owner-approved YouTube by Warder header · test24
The **sole canonical static art** is `plugin/Plugins/Extensions/WarderYouTube/images/warder_header.png`.
Approved by the owner on the GigaBlue Quad 4K Pro with OpenATV 8.1 in test24
(13 November 2026). Keep the EXACT graphics: `YouTube` title,
`by Warder` script and strokes, full Warder skull, cosmic/planet background.
No white margins, no overlays, no recomposition, no title patch.

* Dimensions: **1920 × 152**; PNG 8-bit RGB (color type 2).
* Exact length: **435475 bytes**.
* SHA-256: `93b509055bfe63e1126ccca27f324829d8a2e0c6bbdd3d10976b30d7cf70935c`.
* Git blob object: `5cc0a9b3827c803ca8cc736148e924c259de9bf0`.
* Compared byte-for-byte with the test24 receiver IPK and owner-approved source.
* Used across all 12 screens, native date/clock/version remain separate.
* `tools/warder_header_art.py` verifies both original skull and exact approved
  image, and `tools/build_test_ipk.py` packages the binary unchanged.
* `tools/render_full_header.py` was intentionally deleted: it generated the
  superseded test17 artwork, **not** the owner-approved header.

Release gate: never publish a package if its embedded PNG digest differs,
even if 207 host tests are green. Test on receiver first before stable merge.
