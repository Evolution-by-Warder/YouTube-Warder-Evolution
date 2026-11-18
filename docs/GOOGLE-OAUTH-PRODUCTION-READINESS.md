# Google OAuth production readiness — YouTube Warder Evolution

Prepared 18 November 2026. This is a readiness guide, **not** a claim of Google's approval.

## Project identity
- Enigma2 plugin: **YouTube Warder Evolution** (stable source: `1.0.2`).
- Google authentication: OAuth 2.0 TV / limited-input device flow; existing client must be retained.
- Requested scope: `https://www.googleapis.com/auth/youtube.readonly` only.
- Purpose: read subscriptions and related account metadata for the signed-in user, never modify a Google/YouTube account.
- Optional: public browsing/player and locally saved favourites/history do not require Google account sign-in.
- Official public web (once DNS, GitHub Pages and TLS are operational): `https://warder-evolution.eu/youtube.html`.
- Privacy: `https://warder-evolution.eu/privacy.html`.
- Terms: `https://warder-evolution.eu/terms.html`.
- Authorized domain: `warder-evolution.eu`.
- Contact/support: https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/issues

## Steps that depend on the external provider
1. Restore working DNS delegation and HTTPS before submitting URLs to Google verification. This is currently blocked by DNS SERVFAIL/REFUSED for this newly registered domain.
2. In Google Search Console, verify the DNS **domain property** `warder-evolution.eu` with the Google-provided TXT record. Never invent the record or delete existing GitHub Pages A/CNAME entries.
3. In Google Cloud Console / Google Auth Platform / Branding, enter the exact homepage, privacy and terms URLs above and authorized domain. Preserve the **same** original OAuth client ID; no credential rotation without planning a migration.
4. In Data Access, check that no broader scopes were added. Only `youtube.readonly` is needed by current code.
5. In Audience, confirm External / In production after Google prerequisites, then complete any Branding and Data Access verification in Verification Center. Publishing alone does not guarantee sensitive-scope approval.
6. Provide a short video demonstration when Google requests it: launch Enigma2 plugin, use public browsing without login, open TV-device login, authorize with **test account only**, display real subscriptions, disconnect account. Obscure account emails, device codes, tokens and private information.
7. Confirm user-facing Google account login end to end on a receiver after Google approves. Never publish Google user tokens.

## Technical scope justification (for verification form)
`youtube.readonly` is required to display the user's personal YouTube subscriptions and associated channel/video metadata inside the native Enigma2 TV interface. The request is initiated only when the user chooses to connect their Google account with the official Google TV-device OAuth flow. The plugin does not write to YouTube accounts and the read-only scope is the narrowest authorization that supports personal subscriptions. OAuth access and refresh tokens remain on the user's own receiver; the project does not operate a remote account-token collection service.

## Google references
- https://support.google.com/cloud/answer/15549049
- https://support.google.com/cloud/answer/13464321
- https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification
- https://developers.google.com/youtube/data/guides/authentication

Do **not** build/release a new IPK solely for the website or OAuth consent configuration.
