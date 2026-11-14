# test51 — exact test50 source reconciliation and account recovery

Date: 2026-11-14. Development branch only; no stable release, tag, main merge
or updater-feed modification. This note records work actually present here.

## Baseline

GitHub checkpoint before reconciliation: `098de73b4e6c05cb0baae3de37229f57ec13624c`
(the preceding runtime was test43).

Exact uploaded receiver package test50 SHA256:
`80fe4b17e112cecccbfaf1720b95a8907d82eb58998bbed6b5c714bbffd92dc8`.
All runtime sources/assets were extracted from that package, then only the
explicit changes below were made. Foreign plugins and receiver settings are not
modified. Credentials/token files are not part of the source or IPK.

## Preserved, not redesigned

- Common 477×350 focus/tile geometry, 473×248 thumbnails, 24 px row gap.
- Exact skin.py, grid.py, home_thumbs.py, tile_dimensions.py and both focus PNGs.
- No duplicate title footer during grid browsing; Playlists remains removed.
- General official Home categories, All first, daily rotation, MENU quick select.
- Home real-video rotation on revisit, up to 50 API results and manual refresh.
- Test49 subscription paging and local-account disconnect.

`tests/fixtures/test50-approved-layout.json` pins these source and asset bytes.
The previous package builder generated outdated focus geometry. It now loads
and verifies the accepted PNG files instead of redrawing them.

## New runtime changes

- Reopening Odbery after an API/network failure actually retries; temporary
  errors do not falsely sign the user out or report an empty account.
- Only explicit OAuth `invalid_grant` is classified as needing authorization
  again. The user can request a new TV code with OK. Temporary refresh errors
  keep the existing local credentials for later retry.
- Successful subscription refresh clears stale per-channel video caches even
  when the channel IDs have not changed. Failed refresh keeps existing channel
  names for retry, without presenting them as freshly retrieved results.
- Queued login saves check a cancellation Event under the token-storage lock;
  closing the login before that save runs does not recreate the token file.
- Denied and expired TV-code errors use fixed translated messages; raw network
  errors and tokens are never echoed to the UI.

## Validation and limits

The full repository offline suite is run, including migrated tests for the
owner's changed category/layout requirements and new account-recovery tests.
It checks the built IPK, not only the source XML. These are mocks/offline tests,
NOT evidence of successful Google consent or playback on a real receiver.
The app-level OAuth client ID and client secret remain empty on purpose.
No user password or invented developer credentials are added.

Google's documented device flow still requires a legitimate TV/limited-input
OAuth client and user consent, on a browser-capable phone or computer:
https://developers.google.com/identity/protocols/oauth2/limited-input-device
Official subscription paging:
https://developers.google.com/youtube/v3/docs/subscriptions/list

## Remaining external prerequisite

Configure the developer-owned Google TV OAuth identity, then test sign-in,
account expiry, token refresh, loading and disconnect on GigaBlue/OpenATV.
OAuth authorization does not guarantee private-video playback. Test51 is a
receiver test candidate; do not describe it as a stable or fully authenticated
release until those live checks actually pass.
