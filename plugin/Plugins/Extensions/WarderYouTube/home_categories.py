# -*- coding: utf-8 -*-
"""Supported YouTube mostPopular categories, not personalized web Mix feeds.

Google videos.list supports videoCategoryId for chart=mostPopular. The user
chooses a category with remote arrows and confirms with OK.
"""

HOME_CATEGORIES = (
    ("0", "All"),
    ("10", "Music"),
    ("20", "Gaming"),
    ("17", "Sports"),
    ("24", "Entertainment"),
    ("25", "News"),
    ("28", "Technology"),
)
CATEGORY_IDS = frozenset(item[0] for item in HOME_CATEGORIES)
