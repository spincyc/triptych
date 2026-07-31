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

That table is documentation, not data. The module holds no correspondence of
its own: every conversion, bound and split is read from the verse-level
concordance the source library carries for the Douay-Rheims, which maps all
2528 verses of the psalter one to one between the two systems. Deriving from
one table rather than restating it in several is the point — the restated
copies disagreed, and gave Hebrew 10 and 115 the last verse of the Vulgate
psalm hosting them rather than their own.

Verse numbers are those actually printed. Where the Vulgate keeps a psalm's
pre-split numbering the concordance keeps it too, so Vulgate 115 runs 10-19 and
is Hebrew 116:10-19 verse for verse, exactly as the editions print both. A
converted reference therefore addresses its target edition directly and needs
no realignment afterwards.

The Vulgate commonly counts a psalm's title as its first verse where modern
English versions leave it unnumbered. That offset is a property of the English
convention rather than of either system here, and the concordance records it
separately; it is not applied by these conversions.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

SYSTEMS = ("vulgate", "hebrew")
PSALMS = "Psalms"
LAST_PSALM = 150

# The verse-level concordance, tracked as an artifact of the edition it was
# compiled from and against. It is a Triptych-created reference table of
# numbering alone, carrying no scripture text.
CONCORDANCE_ROOT = (
    Path(__file__).resolve().parents[1]
    / "src" / "sources" / "works" / "english-college-of-douay" / "douay-rheims-bible"
    / "editions" / "challoner-gutenberg-1581" / "artifacts"
)
CONCORDANCE_GLOB = "psalm-numbering-*/psalm-numbering.tsv"


class NumberingError(ValueError):
    """A psalm reference cannot be converted without more information."""


class PsalterUnavailable(RuntimeError):
    """The concordance is missing or malformed, so nothing can be converted."""


class Segment(NamedTuple):
    """One run of verses that both systems number without interruption."""

    chapter: int
    first: int
    last: int
    other_chapter: int
    other_first: int


def _check(system: str) -> str:
    if system not in SYSTEMS:
        raise NumberingError(f"unknown psalm numbering {system!r}; expected one of {SYSTEMS}")
    return system


def _bounds(field: str) -> tuple[int, int] | None:
    """A `12` or `12-20` cell as a verse range; the English-only cells are not."""
    text = field.strip()
    if not text or not text[0].isdigit():
        return None
    low, _, high = text.partition("-")
    return int(low), int(high or low)


@lru_cache(maxsize=1)
def _concordance() -> dict[str, dict[int, tuple[Segment, ...]]]:
    """Every verse of the psalter, keyed by system and chapter.

    The table is validated as it is read rather than trusted: both sides of a
    row must run the same length, and each system must cover all 150 psalms
    without a gap or an overlap. A concordance that failed those tests could
    convert a reference into a plausible wrong verse silently.
    """
    found = sorted(CONCORDANCE_ROOT.glob(CONCORDANCE_GLOB))
    if len(found) != 1:
        raise PsalterUnavailable(
            f"expected one psalm concordance under {CONCORDANCE_ROOT}, found {len(found)}"
        )
    rows: dict[str, list[Segment]] = {system: [] for system in SYSTEMS}
    with found[0].open(encoding="utf-8", newline="") as handle:
        for line, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            vulgate = _bounds(row["vulgate_verses"])
            hebrew = _bounds(row["hebrew_verses"])
            if vulgate is None or hebrew is None:
                raise PsalterUnavailable(f"{found[0]}:{line}: a psalm row without both systems")
            if vulgate[1] - vulgate[0] != hebrew[1] - hebrew[0]:
                raise PsalterUnavailable(
                    f"{found[0]}:{line}: the two systems disagree on how many verses this is"
                )
            here = int(row["vulgate_psalm"]), int(row["hebrew_psalm"])
            rows["vulgate"].append(Segment(here[0], *vulgate, here[1], hebrew[0]))
            rows["hebrew"].append(Segment(here[1], *hebrew, here[0], vulgate[0]))
    return {system: _by_chapter(found[0], system, rows[system]) for system in SYSTEMS}


def _by_chapter(path: Path, system: str, segments: list[Segment]) -> dict[int, tuple[Segment, ...]]:
    table: dict[int, list[Segment]] = {}
    for segment in segments:
        table.setdefault(segment.chapter, []).append(segment)
    missing = [c for c in range(1, LAST_PSALM + 1) if c not in table]
    if missing or len(table) != LAST_PSALM:
        raise PsalterUnavailable(f"{path}: the {system} psalter is missing psalms {missing}")
    for chapter, found in table.items():
        found.sort(key=lambda segment: segment.first)
        for earlier, later in zip(found, found[1:]):
            if later.first != earlier.last + 1:
                raise PsalterUnavailable(
                    f"{path}: {system} Psalm {chapter} is not continuous at verse {later.first}"
                )
    return {chapter: tuple(found) for chapter, found in table.items()}


def _segments(chapter: int, system: str) -> tuple[Segment, ...]:
    found = _concordance()[_check(system)].get(chapter)
    if found is None:
        raise NumberingError(f"Psalm {chapter} is outside the psalter")
    return found


def _targets(chapter: int, system: str) -> tuple[int, ...]:
    """The chapters this one corresponds to in the other system, in order."""
    seen: list[int] = []
    for segment in _segments(chapter, system):
        if segment.other_chapter not in seen:
            seen.append(segment.other_chapter)
    return tuple(seen)


def _extent(chapter: int, system: str) -> tuple[int, int]:
    found = _segments(chapter, system)
    return found[0].first, found[-1].last


def _other(system: str) -> str:
    return "hebrew" if _check(system) == "vulgate" else "vulgate"


def _describe(chapter: int, system: str, target: int) -> str:
    """How much of `target` this chapter accounts for, where it is only part."""
    covered = [s for s in _segments(chapter, system) if s.other_chapter == target]
    low = min(s.other_first for s in covered)
    high = max(s.other_first + (s.last - s.first) for s in covered)
    other = _other(system)
    if _extent(target, other) == (low, high):
        return f"{system} {chapter} is part of {other} {target}"
    return f"{system} {chapter} is {other} {target}:{low}-{high}"


def _convert_chapter(chapter: int, system: str, verse: int | None) -> tuple[int, str]:
    """Convert a chapter, using `verse` only to choose between targets."""
    targets = _targets(chapter, system)
    other = _other(system)
    if len(targets) == 1:
        target = targets[0]
        if len(_targets(target, other)) > 1:
            # This chapter is only part of the one it maps to.
            return target, _describe(chapter, system, target)
        return target, ""
    if verse is None:
        options = ", ".join(str(target) for target in targets)
        raise NumberingError(
            f"{system.capitalize()} Psalm {chapter} splits into {other.capitalize()} "
            f"{options}; a verse is needed to choose"
        )
    for segment in _segments(chapter, system):
        if segment.first <= verse <= segment.last:
            return (
                segment.other_chapter,
                f"{system.capitalize()} {chapter}:{verse} falls in "
                f"{other.capitalize()} {segment.other_chapter}",
            )
    raise NumberingError(f"{system} Psalm {chapter}:{verse} is outside the psalm")


def vulgate_to_hebrew(chapter: int, verse: int | None = None) -> tuple[int, str]:
    """Return the Hebrew chapter for a Vulgate one, plus any caveat."""
    return _convert_chapter(chapter, "vulgate", verse)


def hebrew_to_vulgate(chapter: int, verse: int | None = None) -> tuple[int, str]:
    """Return the Vulgate chapter for a Hebrew one, plus any caveat."""
    return _convert_chapter(chapter, "hebrew", verse)


def convert_chapter(chapter: int, source: str, target: str, verse: int | None = None):
    """Convert one psalm chapter between systems. Returns (chapter, caveat)."""
    _check(source)
    _check(target)
    if source == target:
        return chapter, ""
    return _convert_chapter(chapter, source, verse)


def convert_reference(book: str, chapter: int, source: str, target: str, verse=None):
    """Convert a reference; only the psalter is renumbered between systems."""
    if book != PSALMS:
        return chapter, ""
    return convert_chapter(chapter, source, target, verse)


def convert_point(chapter: int, verse: int | None, source: str, target: str):
    """Convert one chapter:verse point. Returns (chapter, verse, caveat).

    Unlike the chapter functions, a verse given here is converted and so must
    exist: it selects text, and a verse outside its psalm cannot.
    """
    _check(source)
    _check(target)
    if source == target:
        return chapter, verse, ""
    if verse is None:
        converted, note = _convert_chapter(chapter, source, None)
        return converted, None, note
    for segment in _segments(chapter, source):
        if segment.first <= verse <= segment.last:
            moved = segment.other_first + (verse - segment.first)
            note = ""
            if segment.other_chapter != chapter or moved != verse:
                note = (
                    f"{source} {chapter}:{verse} is {target} "
                    f"{segment.other_chapter}:{moved}"
                )
            return segment.other_chapter, moved, note
    raise NumberingError(f"{source} Psalm {chapter}:{verse} is outside the psalm")


def convert_range(
    book: str, begin: dict, end: dict | None, source: str, target: str
) -> tuple[list[dict], list[str]]:
    """Convert one passage range, splitting it where the psalter divides.

    A range is the unit the calendar data actually stores, and it is the unit
    that can cross a boundary: Hebrew 116:8-12 is Vulgate 114:8-9 plus
    115:10-12. Returning ranges rather than a bare chapter keeps that
    expressible and stops every caller reassembling it differently.
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

    if start_verse is None or stop_verse is None:
        # A whole chapter, or an open end: there is no verse to divide on, so
        # the chapter conversion decides and any caveat it raises stands.
        chapter, note = _convert_chapter(start_chapter, source, start_verse or stop_verse)
        moved = {
            "begin": {**begin, "chapter": chapter},
            "end": {**end, "chapter": chapter},
        }
        return [moved], [note] if note else []

    pieces: list[dict] = []
    caveats: list[str] = []
    for segment in _segments(start_chapter, source):
        low = max(start_verse, segment.first)
        high = min(stop_verse, segment.last)
        if low > high:
            continue
        shift = segment.other_first - segment.first
        # Anything the endpoints carry beyond the locus — a verse-part letter,
        # say — belongs to the endpoint it was written on. Where a range
        # divides, the interior ends are new and carry nothing.
        opens = begin if low == start_verse else {}
        closes = end if high == stop_verse else {}
        pieces.append(
            {
                "begin": {**opens, "chapter": segment.other_chapter, "verse": low + shift},
                "end": {**closes, "chapter": segment.other_chapter, "verse": high + shift},
            }
        )
    if not pieces:
        raise NumberingError(
            f"{source} Psalm {start_chapter}:{start_verse}-{stop_verse} is outside the psalm"
        )
    # The concordance segments a psalm wherever the two systems account for it
    # differently — around an inscription, say — and a range crossing such a
    # seam comes back as two pieces that abut. Rejoin those: the seam is an
    # artefact of the table, not a break in the passage. Pieces that land in
    # different chapters, or that leave a gap, are a real division and stay
    # apart, which is what keeps a deliberately disjoint citation disjoint.
    joined = [pieces[0]]
    for piece in pieces[1:]:
        last = joined[-1]
        abuts = (
            piece["begin"]["chapter"] == last["end"]["chapter"]
            and piece["begin"]["verse"] == last["end"]["verse"] + 1
        )
        if abuts:
            joined[-1] = {"begin": last["begin"], "end": piece["end"]}
        else:
            joined.append(piece)
    pieces = joined
    if len(pieces) > 1:
        landed = ", ".join(str(piece["begin"]["chapter"]) for piece in pieces)
        caveats.append(
            f"{source} {start_chapter}:{start_verse}-{stop_verse} divides across "
            f"{target} {landed}"
        )
    else:
        _, _, note = convert_point(start_chapter, start_verse, source, target)
        if note:
            caveats.append(note)
    return pieces, caveats


def psalm_extent(chapter: int, system: str) -> tuple[int, int] | None:
    """The first and last verse Psalm `chapter` has in `system`.

    The first is not always 1: where the Vulgate keeps a pre-split numbering it
    prints Psalm 115 as verses 10-19 and Psalm 147 as 12-20.
    """
    _check(system)
    if not isinstance(chapter, int) or not 1 <= chapter <= LAST_PSALM:
        return None
    return _extent(chapter, system)


def psalm_ceiling(chapter: int, system: str) -> int | None:
    """The last verse Psalm `chapter` has in `system`, or None if unknown."""
    extent = psalm_extent(chapter, system)
    return None if extent is None else extent[1]


def validate_psalm(chapter: int, verse: int | None, system: str) -> str:
    """Return a problem describing an impossible psalm reference, or ''.

    Every psalm is bounded, not only the six that divide, so a reference like
    `Psalm 118:137` in a Hebrew-declared calendar is caught: Hebrew 118 ends at
    29, and only the Vulgate's 118 runs to 176.
    """
    _check(system)
    if not isinstance(chapter, int) or not 1 <= chapter <= LAST_PSALM:
        return f"Psalm {chapter} is outside the psalter (1-{LAST_PSALM})"
    first, last = _extent(chapter, system)
    if verse is not None and verse > last:
        return (
            f"Psalm {chapter}:{verse} exceeds {system} Psalm {chapter}, "
            f"which ends at verse {last}"
        )
    if verse is not None and verse < first:
        return (
            f"Psalm {chapter}:{verse} precedes {system} Psalm {chapter}, "
            f"which begins at verse {first}"
        )
    return ""
