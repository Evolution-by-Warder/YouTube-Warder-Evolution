# Experimental native playback bridge (0.0.3-dev)

## Design

Search (YouTube Data API with a user-supplied key) -> video ID -> optional resolver worker -> a single verified HTTPS media URL -> native Enigma2 MoviePlayer (GStreamer service type 4097).

We inspected Taapat and Fairbird: both open Enigma2 MoviePlayer with an eServiceReference generated from their extracted media URL. For the first experiment we implement our own thin adapter and use **yt-dlp as an optional external resolver**, without copying, bundling, installing or invoking it on the GUI thread.

## Current limits

- **Not tested on any receiver.** Passing desktop CI tests is *not* proof of playback.
- Requires a working `yt-dlp` executable already on PATH. The plugin will not install or update it. Some Enigma2 images may lack a compatible Python/runtime.
- The worker selects a single muxed MP4 with audio (preferring H.264 up to 720p); no separate DASH video/audio tracks are combined.
- Video may be restricted, unavailable, DRM-protected, use newer YouTube extraction requirements or be in an unsupported format. A valid URL does not guarantee GStreamer can decode it.
- Timeouts and extraction errors are nonfatal and do not reveal signed URLs in GUI text.
- Returned media URL must use HTTPS on a googlevideo.com hostname. It is transient and is **not stored in history, sent to logs or copied to Git**.
- On OpenATV 7.6, `MoviePlayer(fromMovieSelection=False)` does **not** restore the previous service automatically. Our `player.py` adapter saves the current service first and explicitly restores it in the movie-player close callback, including error recovery. OpenPLi and other image variations still require physical tests.
- No UI decorations or extra renderers are added. No permanent package or production updater is produced.

## Receiver test checklist

1. Confirm the plugin opens and closes without a traceback.
2. Search with a personally configured Data API key, choose a publicly playable test video.
3. If yt-dlp is missing, the GUI must show a clear message and remain responsive.
4. With yt-dlp installed independently, try a short 360p/720p H.264/AAC video.
5. Verify audio and video, pause/seek/EXIT, and that the previously watched TV service resumes.
6. Exit the search screen while the resolver is busy: no delayed playback/dialog should appear.
7. Compare OpenATV 7.6, 8.1 (GLES on/off), OpenPLi 9.2, SF8008 and GigaBlue Quad 4K Pro.
8. Record startup time, remote key response, memory, CPU and source/installed size.

Never suggest piping remote shell scripts into root as a prerequisite. Do not automatically install dependencies. Do not claim the plugin is production ready until hardware trials pass.
