"""Conversion between Vulgate and Hebrew psalm numbering.

The two systems diverge across most of the psalter because the Septuagint and
Vulgate join and split psalms differently from the Masoretic text. A reference
carried in one system and resolved in the other returns a different psalm, so
every tool that resolves a psalm reference converts through here rather than
assuming its inputs agree.

Chapter correspondence, Vulgate to Hebrew:

    1-8      identical
    9        Hebrew 9 (vv. 1-21) and Hebrew 10 (vv. 22-39)
    10-112   Hebrew chapter + 1
    113      Hebrew 114 (vv. 1-8) and Hebrew 115 (vv. 9-26)
    114      Hebrew 116 (vv. 1-9)
    115      Hebrew 116 (vv. 10-19)
    116-145  Hebrew chapter + 1
    146      Hebrew 147 (vv. 1-11)
    147      Hebrew 147 (vv. 12-20)
    148-150  identical

Verse numbering diverges too: the Vulgate commonly counts a psalm's title as
its first verse, so a verse number may shift by one within a corresponding
chapter. That offset is edition-dependent, so this module converts chapters and
reports the verse relationship rather than silently renumbering verses.
"""

from __future__ import annotations

SYSTEMS = ("vulgate", "hebrew")
PSALMS = "Psalms"

# Vulgate chapters that correspond to part of a Hebrew chapter, and vice versa.
# Each entry maps a Vulgate chapter to (hebrew chapter, first verse, last verse)
# of the Vulgate range it covers; None bounds mean the whole chapter.
_VULGATE_SPLITS = {
    9: ((9, 1, 21), (10, 22, 39)),
    113: ((114, 1, 8), (115, 9, 26)),
}
_VULGATE_PARTIALS = {
    114: (116, 1, 9),
    115: (116, 10, 19),
    146: (147, 1, 11),
    147: (147, 12, 20),
}


class NumberingError(ValueError):
    """A psalm reference cannot be converted without more information."""


def _check(system: str) -> str:
    if system not in SYSTEMS:
        raise NumberingError(f"unknown psalm numbering {system!r}; expected one of {SYSTEMS}")
    return system


def vulgate_to_hebrew(chapter: int, verse: int | None = None) -> tuple[int, str]:
    """Return the Hebrew chapter for a Vulgate one, plus any caveat."""
    if chapter in _VULGATE_SPLITS:
        for hebrew, low, high in _VULGATE_SPLITS[chapter]:
            if verse is not None and low <= verse <= high:
                return hebrew, f"Vulgate {chapter}:{verse} falls in Hebrew {hebrew}"
        options = ", ".join(str(h) for h, _, _ in _VULGATE_SPLITS[chapter])
        raise NumberingError(
            f"Vulgate Psalm {chapter} splits into Hebrew {options}; a verse is needed to choose"
        )
    if chapter in _VULGATE_PARTIALS:
        hebrew, low, high = _VULGATE_PARTIALS[chapter]
        return hebrew, f"Vulgate {chapter} is Hebrew {hebrew}:{low}-{high}"
    if 10 <= chapter <= 112 or 116 <= chapter <= 145:
        return chapter + 1, ""
    if 1 <= chapter <= 8 or 148 <= chapter <= 150:
        return chapter, ""
    raise NumberingError(f"Psalm {chapter} is outside the psalter")


def hebrew_to_vulgate(chapter: int, verse: int | None = None) -> tuple[int, str]:
    """Return the Vulgate chapter for a Hebrew one, plus any caveat."""
    if chapter in (9, 10):
        return 9, f"Hebrew {chapter} is part of Vulgate 9"
    if chapter in (114, 115):
        return 113, f"Hebrew {chapter} is part of Vulgate 113"
    if chapter == 116:
        if verse is None:
            raise NumberingError(
                "Hebrew Psalm 116 splits into Vulgate 114 and 115; a verse is needed to choose"
            )
        return (114, "Hebrew 116:1-9 is Vulgate 114") if verse <= 9 else (
            115,
            "Hebrew 116:10-19 is Vulgate 115",
        )
    if chapter == 147:
        if verse is None:
            raise NumberingError(
                "Hebrew Psalm 147 splits into Vulgate 146 and 147; a verse is needed to choose"
            )
        return (146, "Hebrew 147:1-11 is Vulgate 146") if verse <= 11 else (
            147,
            "Hebrew 147:12-20 is Vulgate 147",
        )
    if 11 <= chapter <= 113 or 117 <= chapter <= 146:
        return chapter - 1, ""
    if 1 <= chapter <= 8 or 148 <= chapter <= 150:
        return chapter, ""
    raise NumberingError(f"Psalm {chapter} is outside the psalter")


def convert_chapter(chapter: int, source: str, target: str, verse: int | None = None):
    """Convert one psalm chapter between systems. Returns (chapter, caveat)."""
    _check(source)
    _check(target)
    if source == target:
        return chapter, ""
    if source == "vulgate":
        return vulgate_to_hebrew(chapter, verse)
    return hebrew_to_vulgate(chapter, verse)


def convert_reference(book: str, chapter: int, source: str, target: str, verse=None):
    """Convert a reference; only the psalter is renumbered between systems."""
    if book != PSALMS:
        return chapter, ""
    return convert_chapter(chapter, source, target, verse)
