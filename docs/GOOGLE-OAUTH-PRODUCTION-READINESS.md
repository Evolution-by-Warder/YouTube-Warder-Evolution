# Google OAuth verification — YouTube Warder Evolution

Updated 21 November 2026 for project **warder-438910** (project number **1063944298730**).

This document records what the published source demonstrates and what must still be checked outside the repository. It is not Google's approval, proof of live website availability, or evidence that the demo video already meets Google's requirements. No change to OAuth credentials or production packages is required by this document.

## 1. Application and OAuth scope — verified from source

- Product: **YouTube Warder Evolution**, independent Enigma2 plugin for OpenATV/OpenPLi TV receivers.
- Authentication: voluntary Google OAuth 2.0 **TV / Limited Input Device** flow initiated inside the plugin.
- Exactly one scope is requested by the device-code request in `plugin/Plugins/Extensions/WarderYouTube/subscriptions_auth.py`:
  `https://www.googleapis.com/auth/youtube.readonly`.
- This scope is used by the user-facing **Subscriptions** feature to retrieve the signed-in user's followed channels and associated channel/upload metadata using the official YouTube Data API. Public browsing and locally maintained favourites/history do not require YouTube account sign-in.
- Why a narrower scope is not sufficient: unauthenticated requests and public API-key access cannot retrieve *the currently signed-in user's private subscription list*. There is no less-privileged YouTube scope exposing those account-specific subscriptions for this feature. The plugin does **not** request scopes that permit uploads, subscription changes, likes, comments, or deletion.
- Authorized YouTube API requests are made with a Bearer token over HTTPS. Access and refresh tokens are stored locally under `/etc/enigma2/warderyoutube-oauth-token.json` with `0600` file permissions. The application does not operate a Warder Evolution server for collecting Google account tokens.
- Disconnecting a linked account attempts token revocation and removes the local token file. Uninstalling may intentionally preserve user data; this is disclosed in the privacy policy.

Sources: `subscriptions_auth.py`, `subscriptions_api.py`, `home_tv_auth.py`, `data_auth.py`, `docs/privacy.html`.

## 2. Public website and policies — source prepared, live checks separate

The repository contains these website pages and `docs/CNAME` targets the project domain:

- Homepage/product: https://warder-evolution.eu/youtube.html
- Privacy policy: https://warder-evolution.eu/privacy.html
- Terms: https://warder-evolution.eu/terms.html
- Support: https://github.com/Evolution-by-Warder/YouTube-Warder-Evolution/issues

**To verify in a real browser / Google Cloud Console:** all pages load over HTTPS; the homepage and Cloud Console point to the **same** privacy policy URL; the domain is owned/verified in Google Search Console by an account that qualifies for the Cloud project; the application name and branding are consistent; and the actual current privacy disclosure matches the released app.

A previously documented transient DNS support ticket is historical and should not be treated as a present failure. This document makes no claim that any DNS or HTTPS issue persists.

## 3. Google Cloud Console — requires account-owner inspection

Open Google Cloud Console, select project `warder-438910`, and inspect Google Auth Platform:

1. **Branding:** application name, support email, verified domain, homepage URL and privacy-policy URL.
2. **Audience:** External and correct publishing status; if an already-public application is in production, do not move it to Testing merely to record a demo.
3. **Clients:** confirm the existing **TVs and Limited Input devices** OAuth client ID used by the installed plugin belongs to this exact project. Keep existing user credentials/configuration; do not rotate the OAuth client without a migration plan.
4. **Data Access:** confirm the declared/requested scope **exactly matches** `https://www.googleapis.com/auth/youtube.readonly`. Remove unnecessary scopes from the verification request, but do not remove anything until its absence from production clients is confirmed.
5. **Verification Center:** review any *specific* reviewer findings or additional questions and the status of the existing submission.
6. **YouTube Data API v3:** confirm it is enabled in the selected project.

**Unknown from the repository:** the live values of these account-only Console settings, current Search Console verification, and approval state. Do not claim these checks have passed without viewing them.

## 4. Demonstration video — reviewer-ready recording sequence

The verification video must correspond to the same installed app and OAuth client in the submitted project. Record the following full flow, ideally with clear English labels or narration:

1. Show the TV receiver opening **YouTube Warder Evolution**; show its identity/branding.
2. Demonstrate public content without a Google login; then navigate to the **YouTube account** action to deliberately initiate sign-in.
3. Display the TV's Google device authorization instructions.
4. On a second browser/device using a **dedicated test Google account**, open Google's provided authorization flow; show the complete **consent screen in English**. Expand **Show all services** where applicable, so the requested YouTube read-only permission is clearly legible.
5. Complete the user's affirmative authorization; return to the TV plugin and show that it is signed in.
6. Open **Subscriptions** and demonstrate that real followed channels and their videos appear. This proves the user-facing operation of the sole requested scope.
7. Show disconnect in the plugin and, if useful, Google Account connection settings. Do not falsely claim a YouTube-account deletion or write operation — the permission is read-only.

Record the user's actual consent workflow; do not splice in an unrelated Google app's consent screen. Avoid disclosing passwords, refresh/access tokens and unrelated personal data. Ensure the video is **Public or Unlisted**, not Private.

**Owner-confirmed existing tutorial link:** https://youtu.be/-pAWMgy9leU (the first character of the video ID is a hyphen). The owner supplied the MP4 source `Warder_Evolution_OAuth_Step_by_Step_FINAL(1).mp4` for review on 21 November 2026. This file was inspected: 116 seconds, 1600×900, 24 fps, silent, with **11 illustrated slides/steps**, rather than an uninterrupted live screen capture.

**Review outcome — useful tutorial but not sufficient as sole compliance evidence:**
- Intro explicitly describes the presentation as an *illustrated step-by-step sign-in flow*.
- Slides 1–7 explain the Enigma2 and Google device-code path; slide 8 illustrates a Google OAuth consent screen containing the read-only YouTube account permission.
- The consent slide shows **“See access details”** collapsed; there is no expanded service/scope detail in the movie.
- Slides 9–11 show a success example, a subscription gallery and signed-in settings, but as static example screens, not independently observable execution of the OAuth flow and YouTube API response.
- Real-time functioning, a fresh user consent interaction, exact configured scope and OAuth client identity are **not proven by the video**. The YouTube hosting visibility (Public/Unlisted) was not checked from the local file.

**Updated upload (owner-provided on 21 November 2026):** https://youtu.be/JFUfU9jQW9k — "YouTube Warder Evolution – Google OAuth Verification Demo". This supersedes the prior tutorial as the **intended link for the pending verification application**. It was prepared from current receiver screenshots showing launch from Plugin Browser, Home, account connection by Google device code, Google's English consent screen, opened "See access details" (including a readable enlargement), successful connection, a genuine subscribed-channel feed, and the signed-in settings state. It retains the original branded introduction and ending and masks the user's account email/name in OAuth screenshots. The owner selected **Unlisted** on YouTube Studio; publication/accessibility after saving cannot be independently confirmed through the available YouTube fetch.

**Evidence caveat / remaining action:** The newly uploaded MP4 is still an edited sequence of real screenshots, **not a continuous live screen recording**. Thus it documents the screens but does not by itself conclusively prove live interaction through the entire authorization flow. Google's [demo guidance](https://support.google.com/cloud/answer/13804565) asks for an end-to-end demonstration. If the reviewers require continuous evidence, capture a live TV/device sign-in and actual subscriptions, and submit that recording instead. Keep the former tutorial https://youtu.be/-pAWMgy9leU as an older reference. Do not claim final approval or complete video compliance yet.

Official requirement: https://support.google.com/cloud/answer/13804565

Google guidance:
- https://support.google.com/cloud/answer/13804565
- https://support.google.com/cloud/answer/13464321
- https://developers.google.com/identity/protocols/oauth2/limited-input-device

## 5. Privacy disclosure review

The existing privacy page describes optional read-only access, local token storage, account connection/disconnection, third-party services, retention, and contact information. Before confirming full compliance, check these details against the **currently installed** app:

- Disclose all actual raw account data read and any locally derived/aggregated data, including retention and deletion.
- Describe use, recipient categories/transfers, protection, and prohibition on selling, targeted advertising and unauthorized reuse.
- Confirm a **prominent in-app privacy notice** is visible on the receiver and users can discover the full published privacy policy. The source currently shows a brief local-data notice in Settings; whether a prominent full-policy link is provided in the released UI requires separate inspection.
- This application does not require a Gmail/Drive/Photos/Workspace AI-training disclosure unless it actually requests one of those APIs/scopes.

## 6. Reply to Google — after the remaining checks

Reply in the existing thread headed **[Action Needed] Your Google APIs Verification Request**. Include project identity, the sole read-only scope, a detailed necessity explanation, verified website/policy links, an accessible compliant demo video, and clear test navigation. State explicitly which checks are complete. Avoid claiming approval or successful checks that have not been observed. Do not send user passwords, access tokens or OAuth client secrets.

**Release constraints:** no IPK release, no OAuth credential rotation, and no production merge solely to prepare this verification checklist.
