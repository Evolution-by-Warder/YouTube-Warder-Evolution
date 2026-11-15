"""Real yt-dlp extraction smoke. Does NOT download or print stream URLs.

Public test only. No YouTube API key or account is used. A runner may be rate
limited or challenged by YouTube; such a failure must remain visible.
"""
import importlib.util
from pathlib import Path
import subprocess
import sys

SOURCE = (Path(__file__).resolve().parents[1]
          / "plugin/Plugins/Extensions/WarderYouTube/resolver.py")
spec = importlib.util.spec_from_file_location("warder_live_resolver", str(SOURCE))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Public video IDs. Do not print provider URLs or individual video details.
TEST_VIDEO_IDS = ("jNQXAC9IVRw", "BaW_jenozKc")


def classify_error(stderr):
    """Small finite status categories. Never emit the raw error text."""
    message = (stderr or "").lower()
    if "sign in to confirm" in message or "not a bot" in message:
        return "YouTube anti-bot restriction"
    if "no supported javascript runtime" in message or "javascript runtime" in message:
        return "JavaScript runtime unavailable"
    if "requested format is not available" in message:
        return "muxed H264/AAC MP4 format unavailable"
    if "http error 403" in message or "forbidden" in message:
        return "HTTP 403 access restriction"
    if "http error 429" in message or "too many requests" in message:
        return "HTTP 429 rate limit"
    if "extractor" in message or "signature" in message:
        return "extractor compatibility issue"
    return "unknown YouTube extraction restriction"


def main():
    last_class = "unknown"
    for index, video_id in enumerate(TEST_VIDEO_IDS, start=1):
        errors = []
        def runner(args, **kwargs):
            reply = subprocess.run(args, **kwargs)
            if reply.returncode != 0:
                errors.append(classify_error(reply.stderr))
            return reply

        try:
            media_url = module.resolve_video_url(video_id, runner=runner, timeout=35)
        except module.ResolverError as error:
            last_class = errors[-1] if errors else type(error).__name__
            print("INCONCLUSIVE: public video candidate %d failed: %s." % (index, last_class))
            continue

        # Only a recognized https googlevideo media URL can pass.
        if not media_url.startswith("https://") or not module.validate_stream_url(media_url):
            print("FAIL: extractor returned unsupported media URL.")
            return 1
        print("PASS: real yt-dlp extraction returned a validated HTTPS muxed-media URL.")
        print("PASS: no download performed and URL was not logged.")
        return 0

    print("INCONCLUSIVE: no candidate extracted on GitHub-hosted runner (%s)." % last_class)
    # A hosted runner failure is NOT a receiver playback failure, but also is
    # NOT a success. CI must reflect that honestly.
    return 2


if __name__ == "__main__":
    sys.exit(main())
