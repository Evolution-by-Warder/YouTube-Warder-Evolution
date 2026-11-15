# YouTube Warder Evolution test10: API key and video-quality behavior

Status: development/test candidate (13 November 2026), **not yet verified on receiver**. This is an isolated YouTube Warder Evolution change; FullHDGlass and Radio Warder Evolution are unchanged.

## Existing API key and manual file

The standard Enigma2 configuration is saved under `/etc/enigma2/settings` as `config.plugins.warderyoutube.api_key`. The owner can also put one ASCII key on a single line into `/etc/enigma2/warderyoutube_api.key`, owned by the receiver user and protected with **mode 0600**. The plugin reads the file **on demand** when the Enigma2-configured key is empty, including after a GUI restart. It rejects symlinks, group/world readable files, multiline entries and invalid lengths/characters. It does not print the key or store it in the plugin's GitHub files.

Recommended manual installation through a trusted local SSH/Telnet session (do not put the actual key in command arguments or chat):

```sh
umask 077
cat > /etc/enigma2/warderyoutube_api.key
# Paste the key on ONE line, press Enter, then Ctrl-D
chmod 600 /etc/enigma2/warderyoutube_api.key
```

The manual file is optional. The configured Enigma2 key takes precedence if set. Removing the Enigma2 key through the plugin does not delete a separately owner-managed key file; Settings explicitly warns if that file remains active. To disable the manual key entirely, remove the file yourself.

## How the on-screen editor behaves

- If **no key** is configured: GREEN/OK opens a blank editor. New characters are **visible while typing** for verification and correction.
- If a **key is already configured** (including via the manual file): Settings shows **`API key: ********`**, with a fixed number of stars regardless of actual length. GREEN/OK says **Change API key** and first opens a Worder-styled yes/no confirmation showing only the fixed mask.
- If change is confirmed: opens a fresh blank keyboard. The old secret is **never preloaded or rendered**. New characters remain readable until GREEN/Confirm saves them. The previous value stays active until that final save.
- If cancel or invalid input: original key persists unchanged. After save, Settings returns to **`********`** and credentials never enter GUI Label text, status messages or debug logs.
- Stored Enigma2 config and the manual file are **not encrypted**. Use trusted access and correct file permissions. Masking protects from casual on-screen exposure, not from a receiver administrator/root user.

## Quality

Menu chooses maximum preference **360p / 480p / 720p / 1080p / 1440p / 2160p**. At 2160p, select the best *available compatible* quality at or below that ceiling (e.g. 1080p if 4K isn't offered). Actual 4K playback requires compatible source stream, codec and Enigma2 playback backend. Single-track MP4 and DASH selection fall back to compatible lower formats; HLS can be adaptive and may not enforce an exact ceiling.

## Home without an API key

The Home preview can attempt a public/anonymous YouTube website request, parse real video identifiers and use standard JPEG thumbnails. It does **not** pretend to supply personalized recommendations or official API regional popularity. Since Google's unauthenticated web structure can change, network/consent failures return a clear fallback to locally saved History or Favourites, without blocking Enigma2 GUI or inventing videos.

## Release constraints

Manual test10 IPK requires hardware validation before testing-feed publication. Do not merge to `main`, release stable, or auto-install; preserve security and SHA256 checks.
