# Stable update feed

`stable.json` is the manifest read by the **Aktualizácie** screen in the installed YouTube Warder Evolution 1.0.0.

Current stable release: 1.0.0. `release: null` is deliberate: the currently distributed 1.0.0 plugin should show **up to date**, and no newer binary has been published on the required GitHub Release asset URL.

## Publishing the next stable update

1. Publish the tested IPK as an asset under a GitHub Release tagged `youtube-warder-vX.Y.Z`.
2. Asset filename must be `enigma2-plugin-extensions-youtube-warder-evolution_X.Y.Z_all.ipk`.
3. Set `release` in `stable.json` to an object containing: `version`, `tag`, `url`, `sha256`, `bytes`, `notes`. SHA256 and bytes must match the GitHub asset exactly.
4. Keep `schema: 1`, `product: "YouTube Warder Evolution"`, `channel: "stable"`.
5. Do not publish the manifest until the IPK is reachable. Users check manually via **Aktualizácie**.

Example for a *future* version (replace placeholder values with real hashes/sizes):

```json
{
  "schema": 1,
  "product": "YouTube Warder Evolution",
  "channel": "stable",
  "release": {
    "version": "1.0.1",
    "tag": "youtube-warder-v1.0.1",
    "url": "https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/releases/download/youtube-warder-v1.0.1/enigma2-plugin-extensions-youtube-warder-evolution_1.0.1_all.ipk",
    "sha256": "<64 lowercase hex digits>",
    "bytes": 0,
    "notes": "Release notes"
  }
}
```

The updater validates the entire manifest, SHA256, byte length and IPK payload before calling `opkg`. The manifest alone cannot host the update binary. Existing `1.0.0` clients use `https://raw.githubusercontent.com/Evolution-by-Warder/YouTube-Warder-Evolution/main/update/stable.json`.
