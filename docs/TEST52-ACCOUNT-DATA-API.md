# test52 — account-first YouTube Data API and Settings

## Implemented

The existing receiver-local Google TV OAuth session is now preferred for the
Home mostPopular chart, all general category requests and continuation pages,
search and search continuation, and on-demand video details in Home, search,
History and Favourites. A separate personal API key is not required when the
user is signed in. The API remains the official YouTube Data API: the Home
feed is still regional/category popular videos, not personalized web Home.

`data_auth.py` owns the credential choice. A locally saved signed-in session
is selected before any optional API key. Token refresh happens inside existing
Twisted network workers; GUI availability checks never refresh tokens. Bearer
tokens go in the Authorization header only, never in URL parameters, logs,
thumbnail requests or the playback resolver. Live Bearer requests do not follow
redirects. Transient token failures do not silently switch to another key.

Settings now starts with **YouTube account**, the stored sign-in state, and
clear TV-code instructions. Green/OK opens account management in the existing
Home right-hand Subscriptions pane. Yellow/MENU opens **Advanced**, retaining
optional API-key editing, masking, deletion confirmation and the private file
fallback. Red/MENU returns from Advanced. Existing keys and tokens are neither
removed nor overwritten by this upgrade. Quality controls are unchanged.

Without a saved account, an existing optional API key still works. With neither
credential, public browsing/yt-dlp fallbacks remain where supported, and Data
API-only features ask the user to sign in rather than implying a key is mandatory.

## Validation

- 325 offline unit/runtime/package tests pass, including 21 new account-first
  tests: blank key, category/search pagination, metadata, actual mocked refresh
  of an expired token, failed/revoked credentials, no credential redirects, key
  fallback, main/advanced Settings and account navigation.
- IPK version: `0.0.8~test52`, 595958 bytes.
- IPK SHA256: `af2f1918e1c9aaebd8cbf480431c4b91953e91b322d30fb223b0bcb06154eeef`.
- All six approved layout source/PNG assets are byte-identical to the test50
  manifest (and test51): no cell/frame, gap or thumbnail geometry changes.
- 48 top-level Python modules; no bytecode/cache, account credentials or tokens
  bundled. Runtime/control versions checked against the built IPK.

The owner reported successful sign-out and sign-in on test51. The test52
account-only Data API calls and revised Settings still require receiver testing.
No live user tokens or private Google configuration are available in the build
environment. Shared app OAuth config remains unchanged and empty; a receiver's
existing private client override continues to work. No new OAuth scopes needed.

## Receiver check

Keep the existing sign-in. In Settings, verify account status and the statement
that no personal key is needed. Open Home categories, change a category, request
more results, search and open INFO. Signed-in requests ignore a saved API key,
so deleting a working backup key is not necessary for adoption. Advanced keeps
it available for signed-out use. Confirm login/logout and retry after offline
operation. Private/age-restricted playback is outside this change.

## Official basis

- https://developers.google.com/youtube/registering_an_application
  (API key required only when the request does not provide an OAuth token)
- https://developers.google.com/identity/protocols/oauth2/limited-input-device
  (TV authorization, youtube.readonly, token refresh and Bearer headers)

Development candidate only; main, stable releases and updater manifests unchanged.
