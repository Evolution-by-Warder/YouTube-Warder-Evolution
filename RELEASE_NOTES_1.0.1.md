# YouTube – Warder Evolution 1.0.1

**Maintenance release — 15 November 2026**

## Fixed
- Restored the working Google TV OAuth application identity that shipped in the tested test85/RC6 packages. The initial public GitHub-built 1.0.0 accidentally inherited an older source file with empty OAuth client fields. On that 1.0.0, **Odbery / Subscriptions** incorrectly displayed that a TV application had not been configured.
- Preserved the existing account-token storage and all other YouTube features; no user access or refresh tokens are included in the release.
- Added release-time validation that the installed TV OAuth identity is configured so this regression cannot silently recur.
- GitHub stable release assets are immutable; subsequent fixes require a new version rather than overwriting an existing IPK.
- Kept **Aktualizácie** pointed at the stable manifest, allowing users with 1.0.0 to install 1.0.1.

## Compatibility
OpenATV 7.6, OpenPLi 9.2, OpenPLi Scarthgap. The base RC6 was tested on real receivers; the 1.0.1 OAuth fix is based on the exact tested test85 configuration. This newly published package still needs a receiver-side smoke test.

## Installation and update
Use **Aktualizácie** in 1.0.0, or install the IPK:

```sh
opkg install /tmp/enigma2-plugin-extensions-youtube-warder-evolution_1.0.1_all.ipk
```

Restart the Enigma2 GUI after installation. Check `/tmp/warder-youtube-deps.log` for automatic dependency installation details.

## Security
The bundled TV app OAuth identity is used to initiate the device login flow; it is not a YouTube password, API token, user access token, or user refresh token. Receiver-local token files and saved settings are preserved.
