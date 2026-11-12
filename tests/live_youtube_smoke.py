"""Live smoke with GitHub Actions secret; prints no secrets, URLs or response bodies.

The test costs one YouTube Data API search.list request (~100 quota units).
No external pip dependencies; no keys stored in Git or test artifacts.
"""
import importlib.util
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_DIR = ROOT / "plugin/Plugins/Extensions/WarderYouTube"


def load_module(name):
    path = MODULE_DIR / (name + ".py")
    spec = importlib.util.spec_from_file_location("warder_live_" + name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run():
    key = os.environ.get("WARDER_TEST_API_KEY", "").strip()
    if not key:
        print("FAIL: repository Actions secret WARDER_YOUTUBE_API_KEY is not configured.")
        return 2

    api = load_module("api")
    thumbnails = load_module("thumbnails")
    try:
        # Single 15-result request; avoid spending repeated API quota.
        result = api.search_videos("enigma2 receiver", key)
        videos = result.get("items", [])
        if not videos:
            print("FAIL: live YouTube search returned no videos.")
            return 1
        if len(videos) > 15:
            print("FAIL: live YouTube search returned too many items.")
            return 1
        if not all(isinstance(item.get("video_id"), str) and
                   len(item["video_id"]) == 11 and item.get("title")
                   for item in videos):
            print("FAIL: invalid live result schema.")
            return 1
        print("PASS: real YouTube search returned %d valid videos." % len(videos))

        metadata = load_module("video_metadata")
        details = metadata.fetch_video_info(videos[0]["video_id"], key)
        if (details.get("video_id") != videos[0]["video_id"]
                or not details.get("title") or not details.get("duration")):
            print("FAIL: real YouTube video metadata is incomplete.")
            return 1
        print("PASS: real video details resolved through YouTube videos.list.")

        image_urls = [item["thumbnail_url"] for item in videos if item.get("thumbnail_url")]
        if not image_urls:
            print("FAIL: search results returned no usable thumbnail URLs.")
            return 1
        # Verify one live image, not 15; cache stays only in /tmp on CI.
        image_path = thumbnails.fetch_thumbnail(image_urls[0])
        if os.path.getsize(image_path) > thumbnails.MAX_BYTES_PER_IMAGE:
            print("FAIL: thumbnail file exceeded size budget.")
            return 1
        print("PASS: one official YouTube thumbnail downloaded within size limit.")
    except Exception as error:
        # Never use traceback/str(error): exceptions can contain signed URLs or keys.
        print("FAIL: live API/thumbnail smoke; exception class: %s." %
              type(error).__name__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
