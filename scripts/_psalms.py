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


# Where one system's psalm is part of another's, the part restarts its own
# verse numbering: Hebrew 116:10 is Vulgate 115:1, so the verse shifts by the
# length of the preceding part. Keyed by (source, target, source chapter) to
# (target chapter, verse delta), applied when the source verse is in range.
_POINT_MAP = {
    ("vulgate", "hebrew"): {
        9: (((1, 21), 9, 0), ((22, None), 10, -21)),
        113: (((1, 8), 114, 0), ((9, None), 115, -8)),
        114: (((1, None), 116, 0),),
        115: (((1, None), 116, +9),),
        146: (((1, None), 147, 0),),
        147: (((1, None), 147, +11),),
    },
    ("hebrew", "vulgate"): {
        9: (((1, None), 9, 0),),
        10: (((1, None), 9, +21),),
        114: (((1, None), 113, 0),),
        115: (((1, None), 113, +8),),
        116: (((1, 9), 114, 0), ((10, None), 115, -9)),
        147: (((1, 11), 146, 0), ((12, None), 147, -11)),
    },
}


def convert_point(chapter: int, verse: int | None, source: str, target: str):
    """Convert one chapter:verse point. Returns (chapter, verse, caveat)."""
    _check(source)
    _check(target)
    if source == target:
        return chapter, verse, ""
    table = _POINT_MAP[(source, target)].get(chapter)
    if table is None:
        converted, note = convert_chapter(chapter, source, target, verse)
        return converted, verse, note
    for (low, high), target_chapter, delta in table:
        if verse is None:
            if len(table) > 1:
                raise NumberingError(
                    f"{source} Psalm {chapter} divides in {target}; a verse is needed to choose"
                )
            return target_chapter, None, f"{source} {chapter} is part of {target} {target_chapter}"
        if verse >= low and (high is None or verse <= high):
            shifted = verse + delta
            note = ""
            if delta or len(table) > 1:
                note = f"{source} {chapter}:{verse} is {target} {target_chapter}:{shifted}"
            return target_chapter, shifted, note
    raise NumberingError(f"{source} Psalm {chapter}:{verse} is outside the psalm")


def _first_part_bound(chapter: int, system: str) -> int | None:
    """Last verse of the first part where a psalm divides in the other system."""
    if system == "vulgate":
        return {9: 21, 113: 8}.get(chapter)
    return {116: 9, 147: 11}.get(chapter)


def convert_range(
    book: str, begin: dict, end: dict | None, source: str, target: str
) -> tuple[list[dict], list[str]]:
    """Convert one passage range, splitting it where the psalter divides.

    A range is the unit the calendar data actually stores, and it is the unit
    that can cross a boundary: Hebrew 116:8-12 is Vulgate 114:8-9 plus
    115:1-3. Returning ranges rather than a bare chapter keeps that expressible
    and stops every caller reassembling it differently.

    Verse numbers are carried through unchanged. The Vulgate commonly counts a
    psalm's title as its first verse, so a verse may sit one off within the
    corresponding chapter; that offset is edition-dependent and is reported as
    a caveat rather than guessed.
    """
    _check(source)
    _check(target)
    end = end or dict(begin)
    if book != PSALMS or source == target:
        return [{"begin": dict(begin), "end": dict(end)}], []

    start_chapter, start_verse = begin.get("chapter"), begin.get("verse")
    stop_chapter, stop_verse = end.get("chapter", start_chapter), end.get("verse")
    if start_chapter != stop_chapter:
        raise NumberingError(
            f"psalm range spans chapters {start_chapter}-{stop_chapter}; "
            "convert each chapter separately"
        )

    caveats: list[str] = []
    bound = _first_part_bound(start_chapter, source)
    if bound is not None and start_verse is not None and stop_verse is not None:
        if start_verse <= bound < stop_verse:
            # The range crosses where this psalm divides, so it becomes two,
            # each carrying the verse numbering of its own target chapter.
            lo_c, lo_v, lo_note = convert_point(start_chapter, start_verse, source, target)
            _, lo_end, _ = convert_point(start_chapter, bound, source, target)
            hi_c, hi_v, hi_note = convert_point(start_chapter, bound + 1, source, target)
            _, hi_end, _ = convert_point(start_chapter, stop_verse, source, target)
            caveats = [n for n in (lo_note, hi_note) if n]
            caveats.append(
                f"{source} {start_chapter}:{start_verse}-{stop_verse} divides across "
                f"{target} {lo_c} and {hi_c}"
            )
            return (
                [
                    {"begin": {"chapter": lo_c, "verse": lo_v},
                     "end": {"chapter": lo_c, "verse": lo_end}},
                    {"begin": {"chapter": hi_c, "verse": hi_v},
                     "end": {"chapter": hi_c, "verse": hi_end}},
                ],
                caveats,
            )

    begin_chapter, begin_verse, begin_note = convert_point(
        start_chapter, start_verse, source, target
    )
    end_chapter, end_verse, _ = convert_point(start_chapter, stop_verse, source, target)
    if begin_note:
        caveats.append(begin_note)
    return (
        [
            {**{"begin": {**begin, "chapter": begin_chapter, "verse": begin_verse}},
             "end": {**end, "chapter": end_chapter, "verse": end_verse}}
        ],
        caveats,
    )
