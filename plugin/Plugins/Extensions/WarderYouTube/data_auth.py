# -*- coding: utf-8 -*-
"""One credential policy for the official YouTube Data API.

Account checks inspect local state only. Token refresh in authorize_request
must run in the caller's network worker. Never send tokens to the resolver,
thumbnail hosts, logs, or URL parameters. A failed signed-in session is NOT
silently replaced with a different API-key identity.
"""
from urllib.request import HTTPRedirectHandler, build_opener, urlopen

from . import subscriptions_auth as auth


class DataAuthorizationError(Exception):
    """Fixed, safe UI text only; no credentials or raw upstream exceptions."""


def account_available():
    return auth.account_connected()


def can_use_data_api(api_key=""):
    return account_available() or bool(isinstance(api_key, str) and api_key.strip())


def authorize_request(params, headers, api_key=""):
    """Copy parameters and attach OAuth first, optional key only when signed out."""
    params, headers = dict(params), dict(headers)
    params.pop("key", None)
    params.pop("access_token", None)
    headers.pop("Authorization", None)
    if account_available():
        try:
            token = auth.access_token()
        except auth.ReauthorizationRequired:
            raise DataAuthorizationError(
                "YouTube authorization expired. Connect the account again.") from None
        except auth.SubscriptionsAuthError:
            raise DataAuthorizationError(
                "Could not refresh YouTube sign-in. Check the connection and retry.") from None
        if (not isinstance(token, str) or not 1 <= len(token) <= 8192
                or not token.isascii() or any(ord(c) < 33 or ord(c) == 127 for c in token)):
            raise DataAuthorizationError("YouTube sign-in data is invalid. Sign in again.")
        headers["Authorization"] = "Bearer " + token
    elif isinstance(api_key, str) and api_key.strip():
        params["key"] = api_key.strip()
    else:
        raise DataAuthorizationError(
            "Sign in to YouTube to use this feature. A personal API key is optional.")
    return params, headers


def authorization_error(status):
    if status == 401:
        return "YouTube authorization expired. Connect the account again."
    return "YouTube denied API access or its quota was exceeded. Try again later."


class _NoCredentialRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward a Bearer token to a different endpoint or host.
        return None


def open_authorized(request, opener, timeout):
    """Use the injected test opener, but never redirect a live Bearer request."""
    if request.get_header("Authorization") and opener is urlopen:
        return build_opener(_NoCredentialRedirect()).open(request, timeout=timeout)
    return opener(request, timeout=timeout)
