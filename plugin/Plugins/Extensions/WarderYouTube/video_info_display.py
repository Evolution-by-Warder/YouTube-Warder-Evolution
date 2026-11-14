# -*- coding: utf-8 -*-
"""Format honest local/remote VIDEO INFO for native Warder screens.

Pure formatter: no GUI, network, API key, video URL or persistent state.
"""


def format_video_info(video, details=None, translate=None, note=None):
    tr = translate or (lambda text: text)
    source = details if isinstance(details, dict) else video
    title = str(source.get("title") or video.get("title") or "YouTube video").strip()[:200]
    channel = str(source.get("channel") or video.get("channel") or "").strip()[:120]
    video_id = str(video.get("video_id") or "")[:11]
    lines = [title, "", "%s: %s" % (tr("Channel"), channel),
             "%s: %s" % (tr("Video ID"), video_id)]
    if isinstance(details, dict):
        duration = str(details.get("duration") or "")
        views = str(details.get("views") or "")
        if duration in ("Neznáma", "Neznámy", "Unknown", ""):
            duration = tr("Unknown")
        if views in ("Neznáma", "Neznámy", "Unknown", ""):
            views = tr("Unknown")
        lines += ["%s: %s" % (tr("Duration"), duration[:40]),
                  "%s: %s" % (tr("Views"), views[:40])]
        description = str(details.get("description") or "").replace("\r", "").strip()[:420]
        if description:
            lines += ["", description]
    elif note:
        lines += ["", tr(note)]
    return "\n".join(lines)[:2200]
