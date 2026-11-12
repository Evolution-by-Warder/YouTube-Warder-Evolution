# YouTube – Warder Evolution

**Status: 0.0.1-dev (native Enigma2 UI prototype, not a working YouTube player).**

Our goal: a familiar YouTube desktop/Smart TV hybrid with a lightweight blue interface for OpenATV and OpenPLi. No heavy web browser, complex overlays, unnecessary renderers, or animated decoration.

- Background #08182D, panels #142C47, focus #087EC7, accent #36B9FF.
- Native Enigma2 controls, 1920×1080 reference layout, remote-control-first navigation.
- Independent UI, metadata/search, video resolver and playback modules.
- Efficient thumbnails, bounded cache and zero blocking network calls on the GUI thread.
- No stream extraction, login, video search, playback or IPK release yet.

Development layout: plugin/ (native source), docs/ (architecture, assimilation and roadmap), tests/ and GitHub Actions (source checks only).

Reference projects to assimilate where appropriate:
- https://github.com/Taapat/enigma2-plugin-youtube
- https://github.com/fairbird/Youtube-Opensource-DreamOS
- YouTubeMod (canonical source to verify)
- https://github.com/yt-dlp/yt-dlp

Use their strongest proven ideas and practical features while preserving source attributions and any applicable code-reuse conditions. For now, our scaffold is independent original code.

Run developer checks: python3 -m unittest discover -s tests -v

Host tests do not establish receiver compatibility. No published package or feed is present.
