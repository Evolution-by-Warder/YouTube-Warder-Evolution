# -*- coding: utf-8 -*-
"""Optional, replaceable yt-dlp backend for individual public video URLs.

This module does NOT import Enigma2.  resolve_video_url() is blocking and MUST
be called through deferToThread by the UI.  The yt-dlp executable is not
bundled, downloaded or installed by this project.

Stage 0: prefer a single muxed MP4 with both audio and video; separate DASH
tracks and DRM formats are out of scope until tested on real hardware.
"""
import re
import shutil
import subprocess
from urllib.parse import urlsplit

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
MAX_STDOUT_CHARS = 16384
TIMEOUT_SECONDS = 28
# A single media stream is important for the first Enigma2/GStreamer test.
# Prefer AVC/H.264 with audio and <= 720p; fall back to a different muxed MP4.
MUXED_MP4_FORMAT = (
    "b[ext=mp4][vcodec^=avc1][acodec!=none][height<=720]/"
    "b[ext=mp4][acodec!=none][height<=720]"
)
QUALITY_FORMATS = {
    "360": (
        "b[ext=mp4][vcodec^=avc1][acodec!=none][height<=360]/"
        "b[ext=mp4][acodec!=none][height<=360]"
    ),
    "720": MUXED_MP4_FORMAT,
}


class ResolverError(Exception):
    """Safe, user-readable failure; never contains a signed stream URL."""


def is_available(which=shutil.which):
    return bool(which("yt-dlp"))


def video_page_url(video_id):
    """Reject malformed IDs; subprocess never receives user-controlled options."""
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise ResolverError("The selected video has an invalid YouTube ID.")
    return "https://www.youtube.com/watch?v=" + video_id


def validate_stream_url(url):
    """Allow only HTTPS direct media hosts, not local/private or arbitrary URLs."""
    if not isinstance(url, str):
        raise ResolverError("The resolver returned an invalid media URL.")
    url = url.strip()
    if not url or any(c in url for c in "\r\n\0"):
        raise ResolverError("The resolver returned an invalid media URL.")
    try:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower()
        if (parsed.scheme.lower() != "https"
                or not (host == "googlevideo.com" or host.endswith(".googlevideo.com"))
                or parsed.username is not None or parsed.password is not None):
            raise ResolverError("The resolver did not return a supported HTTPS video stream.")
    except ValueError:
        raise ResolverError("The resolver returned an invalid media URL.")
    if len(url) > 8192:
        raise ResolverError("The stream URL is unexpectedly long.")
    return url


def resolve_video_url(video_id, runner=subprocess.run, which=shutil.which,
                      timeout=TIMEOUT_SECONDS, quality="720"):
    """Resolve once using optional yt-dlp; call only off the UI thread.

    No shell, no credentials or log output; no auto-download or plugin update.
    The subprocess is bounded by timeout; failures never expose signed URLs.
    """
    watch_url = video_page_url(video_id)
    if quality not in QUALITY_FORMATS:
        raise ResolverError("Unsupported playback quality setting.")
    executable = which("yt-dlp")
    if not executable:
        raise ResolverError(
            "yt-dlp is not installed. Playback needs an available resolver backend."
        )
    argv = [
        executable, "--ignore-config", "--no-playlist", "--no-warnings",
        "--no-progress", "--no-cache-dir", "--socket-timeout", "8",
        "--retries", "1", "--extractor-retries", "1",
        "-f", QUALITY_FORMATS[quality], "--get-url", "--", watch_url
    ]
    try:
        output = runner(
            argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, timeout=timeout, check=False
        )
    except subprocess.TimeoutExpired:
        raise ResolverError("YouTube stream lookup timed out.")
    except OSError:
        raise ResolverError("The yt-dlp executable could not be started.")

    if output.returncode:
        diagnostic = (output.stderr or "").lower()
        # In 2026 yt-dlp often cannot see YouTube's pre-merged MP4 (itag 18).
        # Retry with a different public player client only for that exact
        # failure; do not retry age/private/geo restrictions or auth failures.
        if "requested format is not available" in diagnostic:
            retry_argv = argv[:-2] + [
                "--extractor-args", "youtube:player-client=android",
                "--", watch_url
            ]
            try:
                output = runner(
                    retry_argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, timeout=min(timeout, 18), check=False
                )
            except subprocess.TimeoutExpired:
                raise ResolverError("Záložné získanie MP4 prekročilo časový limit.")
            except OSError:
                raise ResolverError("Záložný prehrávací klient sa nepodarilo spustiť.")
            if output.returncode:
                raise ResolverError(
                    "YouTube neponúka kompatibilný spoločný MP4 stream. "
                    "Skúste kvalitu 360p alebo iné video."
                )
        elif "sign in to confirm" in diagnostic or "not a bot" in diagnostic:
            raise ResolverError(
                "YouTube požaduje overenie prehrávania. Bez prihlásenia nie je dostupné."
            )
        elif "private video" in diagnostic or "video unavailable" in diagnostic:
            raise ResolverError("Vybrané video je nedostupné alebo súkromné.")
        else:
            raise ResolverError(
                "Získanie videa zlyhalo. Skúste iné video alebo kvalitu 360p."
            )
    stdout = output.stdout
    if not isinstance(stdout, str) or len(stdout) > MAX_STDOUT_CHARS:
        raise ResolverError("Unexpected response from the resolver.")
    lines = [x.strip() for x in stdout.splitlines() if x.strip()]
    if len(lines) != 1:
        raise ResolverError("The resolver did not return exactly one media stream.")
    return validate_stream_url(lines[0])


def resolve_video_streams(video_id, quality="720", dash=False):
    """Reuse our Radio resolver's bounded multiple-stream playback policy.

    The standalone yt-dlp muxed MP4 path remains a fallback; neither backend
    installs dependencies or needs an account/API key. No signed URL is logged.
    """
    video_page_url(video_id)
    if quality not in QUALITY_FORMATS:
        raise ResolverError("Unsupported playback quality setting.")
    try:
        from .radio_streams import extract_candidates
        return extract_candidates(video_id, quality=quality, dash=bool(dash))
    except Exception:
        # Radio's public client may be unavailable on a particular YouTube
        # rollout. Try the already-installed yt-dlp, without exposing upstream
        # URLs, cookies, signed tokens or raw exception text in the UI.
        try:
            url = resolve_video_url(video_id, quality=quality)
            return [{"url": url, "service_type": 4097}]
        except ResolverError as exc:
            raise ResolverError(
                "Video nemá dostupný kompatibilný stream (HLS/MP4/DASH). "
                "Skúste iné video alebo kvalitu 360p."
            ) from None
