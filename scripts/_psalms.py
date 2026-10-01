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
concordance the source library carries for the Douay-Rheims, which maps the
2528 verses that printing numbers one to one between the two systems, and from
the same printing's verse-alias table, which records the two verses it prints
inside the verse before them — Vulgate 28:11 and 150:6 — so that the numbering
holds all 2530. Deriving from tracked tables rather than restating them is the
point — the restated copies disagreed, and gave Hebrew 10 and 115 the last
verse of the Vulgate psalm hosting them rather than their own.

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

# The concordance's witness records, in its own verse-alias table, the verses it
# prints inside the verse before them. Two are psalm verses, and both belong to
# the numbering the concordance describes; see `witness_merges`.
WITNESS_ALIASES_GLOB = "verse-aliases-*/verse-aliases.tsv"
PSALMS_TOKEN = "Ps"
MERGED_VERSE = "merged-verse"


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
    convert a reference into a plausible wrong verse silently. The verses the
    witness prints inside the verse before them are restored to both systems
    first (`witness_merges`), so the bounds and conversions describe the
    numbering rather than one printing's divisions of it.

    The equal-length rule is also a limit on what the table can say, and it is
    worth stating because it is invisible from the file. A row is a
    correspondence between two runs of verses, so one verse of one system
    answering to two of the other has no representation here at all: there is no
    row shape that holds it, and the check below refuses any attempt to write
    one. That is a property of the format rather than an oversight, but it means
    the concordance cannot record a division inside a psalm — only that there is
    one. Where such a division exists the psalm carries
    `english_offset_uniform: no` and `english_verse` refuses it, rather than
    applying an offset that holds only at the head of the psalm. A psalm so
    flagged is therefore saying two things at once: the body divides
    differently, and this table cannot say how. Anything that needs to know how
    must read the two editions' printed verses, which is what the Hebrew 13
    correction of 2026-07-30 did.
    """
    found = sorted(CONCORDANCE_ROOT.glob(CONCORDANCE_GLOB))
    if len(found) != 1:
        raise PsalterUnavailable(
            f"expected one psalm concordance under {CONCORDANCE_ROOT}, found {len(found)}"
        )
    runs: list[list[int]] = []
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
            runs.append([int(row["vulgate_psalm"]), *vulgate, int(row["hebrew_psalm"]), *hebrew])
    _restore_witness_merges(found[0], runs)
    rows: dict[str, list[Segment]] = {system: [] for system in SYSTEMS}
    for vulgate_psalm, vulgate_first, vulgate_last, hebrew_psalm, hebrew_first, hebrew_last in runs:
        rows["vulgate"].append(
            Segment(vulgate_psalm, vulgate_first, vulgate_last, hebrew_psalm, hebrew_first)
        )
        rows["hebrew"].append(
            Segment(hebrew_psalm, hebrew_first, hebrew_last, vulgate_psalm, vulgate_first)
        )
    return {system: _by_chapter(found[0], system, rows[system]) for system in SYSTEMS}


@lru_cache(maxsize=1)
def witness_merges() -> tuple[tuple[int, int], ...]:
    """The Vulgate psalm verses the concordance's witness prints inside the verse before.

    The concordance cannot be the whole statement of the psalm numbering by
    itself, and the reason is how it was compiled rather than an oversight: its
    rows are runs of the Challoner Douay's printed verses, and that printing
    joins Vulgate 28:10-11 and 150:5-6, so read alone the table ends both psalms
    a verse early — in both systems, since each row's Hebrew run matches its
    Vulgate run verse for verse. Both verses are cited (christ-the-king's
    *Sedebit Dominus Rex in aeternum* is `Psalm 28:10-11`, two responsorial
    psalms end at `Psalm 150:6`), both are printed as verses of their own by
    every other tracked witness of either numbering, and the witness's own alias
    table already records where it carries each. So the numbering is stated by
    the two tracked artifacts together, and this reads the second. Nothing is
    typed here: the loci come out of the witness's `verse-aliases.tsv`.

    Only a verse merged into the one before it can say this, and only at the end
    of its psalm; anything else in the table refuses the load rather than being
    read as something it does not say.
    """
    found = sorted(CONCORDANCE_ROOT.glob(WITNESS_ALIASES_GLOB))
    if len(found) != 1:
        raise PsalterUnavailable(
            f"expected one verse-alias table under {CONCORDANCE_ROOT}, found {len(found)}"
        )
    merges: list[tuple[int, int]] = []
    with found[0].open(encoding="utf-8", newline="") as handle:
        for line, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            cited = (row.get("cited_locus") or "").strip().split(".")
            if len(cited) != 3 or cited[0] != PSALMS_TOKEN:
                continue
            chapter, verse = int(cited[1]), int(cited[2])
            carrier = (row.get("resolves_to") or "").strip()
            kind = (row.get("kind") or "").strip()
            if kind != MERGED_VERSE or carrier != f"{PSALMS_TOKEN}.{chapter}.{verse - 1}":
                raise PsalterUnavailable(
                    f"{found[0]}:{line}: the witness records Psalm {chapter}:{verse} as "
                    f"{kind!r} into {carrier!r}; only a verse printed inside the one "
                    f"before it says anything about the psalm numbering"
                )
            merges.append((chapter, verse))
    return tuple(sorted(merges))


def _restore_witness_merges(path: Path, runs: list[list[int]]) -> None:
    """Give back to each system the verse the witness prints inside the one before.

    The merged verse closes its Vulgate psalm, and the Hebrew run that answers
    to the witness's last printed verse must close its Hebrew psalm too: then
    the verse it merged is the next verse of both, and extending the two runs by
    one keeps the row equal-length on both sides. A merge anywhere else would
    need a correspondence this rule does not supply, so it refuses instead.
    """
    for chapter, verse in witness_merges():
        here = [run for run in runs if run[0] == chapter]
        if not here:
            raise PsalterUnavailable(
                f"{path}: the witness merges into Vulgate Psalm {chapter}, "
                f"which the concordance lacks"
            )
        last = max(here, key=lambda run: run[2])
        if last[2] != verse - 1:
            raise PsalterUnavailable(
                f"{path}: the witness prints Vulgate {chapter}:{verse} inside {chapter}:{verse - 1}, "
                f"but the concordance ends Vulgate Psalm {chapter} at verse {last[2]}; a merged "
                f"verse completes the numbering only at the end of its psalm"
            )
        hebrew_last = max(run[5] for run in runs if run[3] == last[3])
        if last[5] != hebrew_last:
            raise PsalterUnavailable(
                f"{path}: Vulgate {chapter}:{verse - 1} answers to Hebrew {last[3]}:{last[5]}, "
                f"which does not end Hebrew Psalm {last[3]}; the merged verse has no "
                f"next Hebrew verse to answer to"
            )
        last[2] += 1
        last[5] += 1


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


def verse_runs(verses: list[int]) -> str:
    """`verse 11`, `verses 11-12`, or `verses 1-9 and 20`, for a reason."""
    runs: list[list[int]] = []
    for verse in verses:
        if runs and verse == runs[-1][1] + 1:
            runs[-1][1] = verse
        else:
            runs.append([verse, verse])
    named = [str(low) if low == high else f"{low}-{high}" for low, high in runs]
    noun = "verse" if len(verses) == 1 else "verses"
    return f"{noun} {' and '.join(named)}"


def closed_at_bounds(
    book: str, begin: dict, end: dict | None, system: str
) -> tuple[dict, dict]:
    """One psalm range with any open end closed at its psalm's bound in `system`.

    An open end means "from the psalm's first verse" or "to its last", and the
    first is not always 1: the concordance runs Vulgate 147 from 12 to 20.
    `convert_range` does not close it. Given an open end it moves the chapter
    number alone and returns what it knows as a caveat, so Vulgate `Psalm 147`,
    which is Hebrew 147:12-20, came back as Hebrew 147 whole -- Vulgate 146's
    eleven verses included -- and the caveat was dropped. Closed first, the
    range converts verse for verse like any other and `dropped_verses` can
    count it. A range across psalms, or outside the psalter, is returned as it
    came, for `convert_range` to refuse.
    """
    end = end or begin
    chapter = begin.get("chapter")
    if book != PSALMS or chapter is None or end.get("chapter", chapter) != chapter:
        return begin, end
    extent = psalm_extent(int(chapter), system)
    if extent is None:
        return begin, end
    low, high = extent
    if begin.get("verse") is None:
        begin = {**begin, "verse": low}
    if end.get("verse") is None:
        end = {**end, "chapter": chapter, "verse": high}
    return begin, end


def dropped_verses(
    book: str, begin: dict, end: dict | None, source: str, target: str, pieces: list[dict]
) -> str:
    """Why converting one range to `target` would lose a verse it cites, or ''.

    `convert_range` keeps only the verses the concordance numbers, so a range
    running past a psalm's bound there comes back shorter rather than refused:
    real verses, short, with nothing to say so. A range that cannot be
    converted whole is not converted; the reason names the bound it ran into.
    The worked case is Hebrew `Psalm 56:13-14`: every tracked Vulgate witness
    prints Psalm 55 with thirteen verses, the two systems divide the psalm's
    body differently, and Hebrew 56:14 has no Vulgate verse of its own.

    An open end is counted as the verses it stands for: each side is closed at
    its psalm's bound (`closed_at_bounds`) before the two are compared, so a
    whole psalm moved by its chapter number alone does not pass for converted.

    The check sits beside `convert_range` rather than inside it, so that
    function's own callers are unchanged; `convert_range_whole` is the
    conversion that applies it.
    """
    if book != PSALMS or source == target:
        return ""
    begin, end = closed_at_bounds(book, begin, end, source)
    chapter, first, last = begin.get("chapter"), begin.get("verse"), end.get("verse")
    if chapter is None or first is None or last is None:
        return ""  # outside the psalter; convert_range refuses it itself
    if end.get("chapter", chapter) != chapter:
        return ""  # convert_range refuses a range across psalms itself
    chapter, first, last = int(chapter), int(first), int(last)
    cited = last - first + 1
    served = 0
    for piece in pieces:
        opens, closes = closed_at_bounds(book, piece["begin"], piece["end"], target)
        served += int(closes["verse"]) - int(opens["verse"]) + 1
    if served == cited:
        return ""
    reference = f"{source} Psalm {chapter}:{first}-{last}"
    if served > cited:
        return f"{reference} would convert to {served} verses in {target}, not its {cited}"
    extent = psalm_extent(chapter, source)
    if extent is None:
        return f"{reference} would convert to {served} of its {cited} verses in {target}"
    low, high = extent
    lost = [verse for verse in range(first, last + 1) if not low <= verse <= high]
    bounds = []
    if first < low:
        bounds.append(f"begins before verse {low}, where the tracked psalm concordance "
                      f"begins {source} Psalm {chapter}")
    if last > high:
        bounds.append(f"runs past verse {high}, where the tracked psalm concordance "
                      f"ends {source} Psalm {chapter}")
    if not bounds or not lost:
        return f"{reference} would convert to {served} of its {cited} verses in {target}"
    return (
        f"{reference} {' and '.join(bounds)}, so converting it to {target} "
        f"would drop {verse_runs(lost)}"
    )


def _reopened(piece: dict, system: str, opens: bool, closes: bool) -> dict:
    """A converted piece with each end the citation runs past its psalm's bound left open.

    `opens` and `closes` say whether the cited passage runs on past this
    piece's begin or end: because the citation left that end open, or because
    the range continues into a neighbouring psalm there. Where it does and the
    piece stops at its psalm's bound in `system`, that end means "the psalm's
    first verse" or "its last", and is served as one rather than as the number
    the concordance gives it -- editions of one system number the same psalm
    differently. The Clementine, the 1899 Douay and the CPDV print Vulgate 147
    as verses 1-9, not 12-20, and the Clementine prints a tenth verse of
    Vulgate 19 that the concordance's witness joins to its ninth. Closed at the
    concordance's verses, a converted citation would lose exactly those. An end
    carrying a verse part is the citation's own and is never reopened.
    """
    begin, end = dict(piece.get("begin") or {}), dict(piece.get("end") or {})
    chapter = begin.get("chapter")
    if chapter is None or end.get("chapter") != chapter:
        return piece
    extent = psalm_extent(int(chapter), system)
    if extent is None:
        return piece
    low, high = extent
    if opens and begin.get("verse") == low and not begin.get("part"):
        begin.pop("verse")
    if closes and end.get("verse") == high and not end.get("part"):
        end.pop("verse")
    return {"begin": begin, "end": end}


def convert_range_whole(
    book: str, begin: dict, end: dict | None, source: str, target: str
) -> list[dict]:
    """Convert one range verse for verse, refusing rather than losing a verse.

    `convert_range` with the three rules every caller resolving a citation
    needs, held here once rather than reimplemented per tool:

    - An open end is closed at its psalm's bound before converting
      (`closed_at_bounds`), so Vulgate `Psalm 147` converts to Hebrew 147:12-20
      and not to Hebrew 147 whole.
    - A range that would come back short raises `NumberingError` naming the
      bound (`dropped_verses`) instead of returning the verses that survived.
    - An end the cited passage runs past is served open again wherever the
      converted piece reaches its psalm's bound (`_reopened`): a whole psalm is
      served whole, and a half-open range such as Vulgate 28:3- stays
      "to the end of the psalm" rather than ending at the concordance's verse.

    A range in another book, or read in the numbering it is written in, is
    returned as it came: a citation is never converted into its own numbering,
    because editions of one system number the same psalm differently.
    """
    end = end or begin
    if book != PSALMS or source == target:
        return [{"begin": dict(begin), "end": dict(end)}]
    open_begin = begin.get("verse") is None
    open_end = end.get("verse") is None
    if open_begin or open_end:
        begin, end = closed_at_bounds(book, begin, end, source)
    pieces, _ = convert_range(book, begin, end, source, target)
    lost = dropped_verses(book, begin, end, source, target, pieces)
    if lost:
        raise NumberingError(lost)
    if not (open_begin or open_end):
        return pieces
    last = len(pieces) - 1
    return [
        _reopened(piece, target, open_begin or index > 0, open_end or index < last)
        for index, piece in enumerate(pieces)
    ]


# The English convention is not a third numbering system: it numbers the psalms
# exactly as the Hebrew does and differs only in printing the inscription
# unnumbered, so an English Bible's verse numbers run one or two lower than the
# Hebrew ones through the body of most psalms. The concordance records that
# offset in its own columns, and records where it does not hold, so the
# correspondence is read from there rather than assumed to be uniform.
ENGLISH_UNIFORM = "yes"


@lru_cache(maxsize=1)
def _english() -> tuple[dict[tuple[int, int], int | None], frozenset[int]]:
    """The English verse each Hebrew run opens at, and the psalms that refuse.

    Keyed by the Hebrew chapter and the first verse of a run, so the runs
    themselves stay owned by the validated Hebrew segmentation and this table
    adds only the English column to it. A `None` marks a run English Bibles
    leave unnumbered — the inscription. A psalm the concordance flags as not
    uniformly offset is collected separately and is not converted at all: the
    two conventions divide the body of those psalms differently, and an offset
    taken from the head of the psalm would be wrong further down.
    """
    found = sorted(CONCORDANCE_ROOT.glob(CONCORDANCE_GLOB))
    if len(found) != 1:
        raise PsalterUnavailable(
            f"expected one psalm concordance under {CONCORDANCE_ROOT}, found {len(found)}"
        )
    opens: dict[tuple[int, int], int | None] = {}
    divided: set[int] = set()
    with found[0].open(encoding="utf-8", newline="") as handle:
        for line, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            chapter = int(row["hebrew_psalm"])
            hebrew = _bounds(row["hebrew_verses"])
            if hebrew is None:
                raise PsalterUnavailable(f"{found[0]}:{line}: a psalm row without a Hebrew range")
            english = _bounds(row["english_verses"])
            if english is not None and english[1] - english[0] != hebrew[1] - hebrew[0]:
                raise PsalterUnavailable(
                    f"{found[0]}:{line}: the Hebrew and English runs are different lengths"
                )
            if row["english_offset_uniform"].strip() != ENGLISH_UNIFORM:
                divided.add(chapter)
            opens[(chapter, hebrew[0])] = None if english is None else english[0]
    return opens, frozenset(divided)


def english_verse(chapter: int, verse: int) -> tuple[int | None, str]:
    """The verse an English Bible prints for a Hebrew-numbered psalm verse.

    Returns the verse and an empty problem, or `None` and the reason no verse
    can be named. Refusing is the point: an edition that leaves the inscription
    unnumbered has no verse at all for the Hebrew numbering's first verse, and
    the sixteen psalms the concordance flags as not uniformly offset divide
    their bodies differently as well. Returning whatever number the head of the
    psalm suggests would land on real text that is not the text cited.
    """
    opens, divided = _english()
    if chapter in divided:
        return None, (
            f"English Bibles divide Psalm {chapter} differently from the Hebrew "
            "numbering, and no verse-for-verse correspondence is recorded for it"
        )
    for segment in _segments(chapter, "hebrew"):
        if segment.first <= verse <= segment.last:
            start = opens.get((chapter, segment.first))
            if start is None:
                return None, (
                    f"Hebrew Psalm {chapter}:{verse} is the inscription, which English "
                    "Bibles print unnumbered"
                )
            return start + (verse - segment.first), ""
    raise NumberingError(f"hebrew Psalm {chapter}:{verse} is outside the psalm")


def unnumber_titles(ranges: list) -> tuple[list, str]:
    """Move Hebrew-numbered psalm ranges onto an edition that numbers no title.

    Every calendar tracked here numbers a psalm's inscription, and the King
    James Version does not, so its Psalm 51:1 is the *Miserere* that a
    Hebrew-numbered calendar cites as 51:3. The shift is a property of the
    edition rather than of the reference, and it is applied to the ranges only.
    An end left open stays open: it means the psalm's first or last verse
    whatever number the edition gives it.

    A range this correspondence cannot carry is refused rather than moved by
    the offset at the head of the psalm. Two cases refuse. An endpoint on the
    inscription has no verse to move to, because the edition prints those words
    without a number. And where the two conventions divide a psalm's body
    differently the concordance records no verse-for-verse correspondence at
    all, so an offset taken from the first verse would land on real text some
    way from the words cited.

    Held here, beside `english_verse`, because two tools need it: the Bible
    indexes (`tools/index-bible`) and the browser structure (`tools/mass-propers`),
    which until 2026-10-01 applied no shift at all, so every page reading an
    edition that leaves titles unnumbered was one or two verses off wherever a
    psalm has a numbered heading.
    """
    moved: list = []
    for span in ranges:
        piece: dict = {}
        for side in ("begin", "end"):
            end = span.get(side)
            if not isinstance(end, dict):
                continue
            chapter, verse = end.get("chapter"), end.get("verse")
            if chapter is None or verse is None:
                piece[side] = dict(end)
                continue
            found, problem = english_verse(int(chapter), int(verse))
            if found is None:
                return [], problem
            piece[side] = {**end, "verse": found}
        moved.append(piece)
    return moved, ""


# How a structure file addresses a citation: one set of loci per numbering
# system and psalm-title convention an edition can be printed in. The title
# convention is not a third numbering system -- chapters and bodies agree with
# the Hebrew -- but an edition that leaves the inscription unnumbered prints
# most psalms' verses one or two lower, so it cannot be read with the Hebrew
# loci. The key is what `index-bible manifest` writes as an edition's `loci`,
# so a page takes the loci already computed for its edition and holds no
# numbering logic of its own.
TITLES_NUMBERED = "numbered"
TITLES_UNNUMBERED = "unnumbered"
ADDRESSINGS: dict[str, tuple[str, str]] = {
    "vulgate": ("vulgate", TITLES_NUMBERED),
    "hebrew": ("hebrew", TITLES_NUMBERED),
    "hebrew-unnumbered-titles": ("hebrew", TITLES_UNNUMBERED),
}


def addressed(book: str, converted: dict[str, list]) -> tuple[dict[str, list], dict[str, str]]:
    """One citation's ranges for every addressing, and why any addressing refuses.

    `converted` holds the citation's ranges already converted into each numbering
    system in `SYSTEMS`; each caller converts by its own rule. An addressing that
    leaves psalm titles unnumbered takes the Hebrew ranges shifted by
    `unnumber_titles`, and where that refuses -- an endpoint on the inscription,
    or one of the psalms whose body the two conventions divide differently -- the
    addressing gets no ranges and its reason instead, while the others still
    serve the citation. Only the psalter shifts; every other book reads the same
    ranges under every addressing.
    """
    ranges: dict[str, list] = {}
    refused: dict[str, str] = {}
    for key, (numbering, titles) in ADDRESSINGS.items():
        pieces = converted[numbering]
        if titles == TITLES_UNNUMBERED and book == PSALMS:
            try:
                pieces, problem = unnumber_titles(pieces)
            except NumberingError as error:
                problem = str(error)
            if problem:
                refused[key] = problem
                continue
        ranges[key] = pieces
    return ranges, refused


def addressing(numbering: str, titles: str) -> str:
    """The structure-loci key an edition in `numbering` with these psalm titles reads."""
    for key, declared in ADDRESSINGS.items():
        if declared == (numbering, titles):
            return key
    raise NumberingError(
        f"no structure loci are computed for {numbering!r} numbering with psalm titles "
        f"{titles!r}; known: {', '.join(f'{n}/{t}' for n, t in ADDRESSINGS.values())}"
    )


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
