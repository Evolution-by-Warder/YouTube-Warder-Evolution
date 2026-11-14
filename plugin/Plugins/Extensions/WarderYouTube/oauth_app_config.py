# -*- coding: utf-8 -*-
"""Developer-maintained public TV OAuth application identity.

Once the Warder project's Google TV/limited-input OAuth client is approved,
its ID and client secret can be supplied when building the receiver package.
TV-installed clients cannot protect a shared client secret: it is NOT a
password, refresh token, or Google user credential. Do not ship a dummy ID.

Before then, login remains explicitly unavailable; public videos still work.
The optional private /etc/enigma2/warderyoutube-oauth-client.json file remains
supported for advanced installation/testing and overrides these values.
"""
OAUTH_TV_CLIENT_ID = ""
OAUTH_TV_CLIENT_SECRET = ""
