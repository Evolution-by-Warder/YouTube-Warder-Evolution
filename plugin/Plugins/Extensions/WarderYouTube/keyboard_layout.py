# -*- coding: utf-8 -*-
"""Single locale-aware Warder keyboard matrix shared by full and inline editors.

Only the view changes between them. Character rows and remote navigation
semantics remain identical; no third-party renderer or system keyboard patch.
"""
from .i18n import language_code

COLUMNS = 10
KEYBOARDS = {
    "sk": ("1234567890", "qwertyuiop", "asdfghjkl-", "zxcvbnm.,?", "áčďéíľňšťž"),
    "cs": ("1234567890", "qwertyuiop", "asdfghjkl-", "zxcvbnm.,?", "áčďéěíňřšť"),
    "de": ("1234567890", "qwertzuiop", "asdfghjkl-", "yxcvbnm.,?", "äöüßéèàâêî"),
    "en": ("1234567890", "qwertyuiop", "asdfghjkl-", "zxcvbnm.,?", "@#:/_()+*?"),
}
ROWS = KEYBOARDS["sk"]


def keyboard_rows(locale=None):
    """Select the same 5x10 character layout in both Warder keyboards."""
    selected = (locale or language_code()).split("_")[0].split("-")[0].lower()
    return KEYBOARDS.get(selected, KEYBOARDS["en"])
