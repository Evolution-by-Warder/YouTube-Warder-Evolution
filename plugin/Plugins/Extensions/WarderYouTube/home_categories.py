# -*- coding: utf-8 -*-
"""Official YouTube video-category IDs for the SK mostPopular video chart.

These are broad Data API categories, NOT the personalized YouTube web Home
chips. "All" is fixed first; the remaining six rotate once per receiver-local
date. The selection never changes while one Home Screen is open.
"""
from datetime import date

# Standard YouTube Data API v3 videoCategory IDs (videos.list chart=mostPopular).
CORE_CATEGORIES = (
    ("10", "Music"),
    ("20", "Gaming"),
    ("17", "Sports"),
    ("24", "Entertainment"),
    ("25", "News"),
    ("28", "Technology"),
)
EXTRA_CATEGORIES = (
    ("26", "Howto & Style"),
    ("15", "Pets & Animals"),
    ("19", "Travel & Events"),
    ("22", "People & Blogs"),
    ("23", "Comedy"),
    ("27", "Education"),
    ("1", "Film & Animation"),
)
HOME_CATEGORIES = (("0", "All"),) + CORE_CATEGORIES + EXTRA_CATEGORIES
CATEGORY_IDS = frozenset(identifier for identifier, unused in HOME_CATEGORIES)


def rotating_categories(day=None):
    """Keep Všetko pinned; rotate four main + two extra topics per day.

    Uses receiver-local calendar date rather than randomness, so navigating
    between sections, paging or reopening the popup cannot reorder the list.
    """
    ordinal = date.today().toordinal() if day is None else int(day)
    base_start = ordinal % len(CORE_CATEGORIES)
    extra_start = ordinal % len(EXTRA_CATEGORIES)
    core = [CORE_CATEGORIES[(base_start + i) % len(CORE_CATEGORIES)]
            for i in range(4)]
    extras = [EXTRA_CATEGORIES[(extra_start + i) % len(EXTRA_CATEGORIES)]
              for i in range(2)]
    return (("0", "All"),) + tuple(core + extras)
