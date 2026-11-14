"""Manual smoke: verify Google accepts the Warder TV OAuth client ID.

Never log, persist, artifact-upload, or expose an OAuth secret, device code
or verification URL. No account login/consent is attempted in CI: actual
subscriptions are tested only after the owner authorizes on the receiver.
"""
import os
import sys
from pathlib import Path

MODULES = Path(__file__).resolve().parents[1] / "plugin/Plugins/Extensions"
sys.path.insert(0, str(MODULES))
from WarderYouTube.subscriptions_auth import (
    CLIENT_ID, SubscriptionsAuthError, request_device_code,
)


def main():
    client_id = os.environ.get("WARDER_TEST_OAUTH_CLIENT_ID", "")
    secret = os.environ.get("WARDER_TEST_OAUTH_CLIENT_SECRET", "")
    if not client_id or not secret:
        print("BLOCKED: OAuth ID and secret must be configured as encrypted repository Actions Secrets.")
        return 2
    if not CLIENT_ID.fullmatch(client_id) or len(secret) > 256:
        print("FAIL: OAuth TV client configuration format is invalid.")
        return 2
    try:
        response = request_device_code({"client_id": client_id, "client_secret": secret})
    except SubscriptionsAuthError as error:
        print("FAIL: Google TV authorization endpoint rejected the device-code request:", str(error))
        return 1
    # Do not print either the Google device code or its verification URL.
    if response.get("device_code") and response.get("user_code"):
        print("PASS: Google TV device-code request accepted. Interactive receiver consent not tested.")
        return 0
    print("FAIL: Google did not return the expected device-code fields.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
