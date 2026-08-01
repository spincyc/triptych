"""Loci shared by the commentary harvest and the corpus that consumes it.

The harvest is run by chapter and the corpus is keyed by verse range, so the
two speak different key spaces over the same material. `Psalms 24` and
`Psalms 24:1-24:3` name the same chapter and match as strings not at all: of
1596 corpus references only 13 found a harvested locus, so 184 of 195 masses
came back empty from a corpus that held 7297 attributions.

Both tools therefore derive their chapter loci here rather than each keeping
its own copy. A second implementation of this rule would be a restatement, and
restatements drift: the point of the key space is that both ends agree on it.

The discovery index stores one granularity — the chapter locus — and every
finer view is derived from it. `overlapping_keys` is what holds that line: two
keys covering some of the same text mean the index answers one question two
ways, and both answers look complete. It survived a promotion once because
nothing looked.

A locus also has a third element the key does not write down: the numbering
system it is addressed in. `Psalms 24` is Ad te levavi in the Vulgate and Unto
thee, O Lord in the Hebrew, and both resolve. The index declares that system,
and everything below is what makes the declaration checkable rather than
asserted — the vocabulary it may use, the bounds a key must respect in the
system it claims, and the derivation that finds a key whose citing calendar's
own divergence register puts it somewhere else.
"""

from __future__ import annotations

import re

import _projection
import _psalms

_REFERENCE = re.compile(r"^(.*?)\s+(\d.*)$")
_WHOLE_CHAPTER = re.compile(r"^\d+$")
_ONE_VERSE = re.compile(r"^(\d+):(\d+)$")
_SPAN = re.compile(r"^(\d+):(\d+)\s*-\s*(?:(\d+):)?(\d+)$")

# (book, chapter, first verse, last verse); None at either end means the
# chapter is open there, so a chapter key covers every verse in it.
Extent = tuple[str, int, "int | None", "int | None"]


def chapter_loci(passage: str) -> list[str]:
    """Split a reference into one locus per chapter, never wider.

    A query may cover at most a single chapter: grouping across chapters drops
    works that comment on only one of them. Isaiah 63:16-64:7 is therefore two
    loci, not one, which costs more queries and loses nothing.
    """
    match = _REFERENCE.match(passage.strip())
    if not match:
        return [passage]
    book, tail = match.group(1), match.group(2)
    chapters: list[str] = []
    for chapter in re.findall(r"(\d+):", tail) or re.findall(r"^(\d+)$", tail):
        locus = f"{book} {chapter}"
        if locus not in chapters:
            chapters.append(locus)
    return chapters or [passage]


def book_of(locus: str) -> str:
    """The book a locus names, without its chapter or verses."""
    match = _REFERENCE.match(locus.strip())
    return match.group(1) if match else locus.strip()


def key_extents(key: str) -> list[Extent]:
    """The text one index key covers, chapter by chapter.

    Returns `[]` for anything this cannot parse rather than guessing an
    extent: `overlapping_keys` then compares such a key by its spelling alone,
    which is the safe direction. A guessed extent would report an overlap that
    is not there, or worse, miss one that is.
    """
    match = _REFERENCE.match(key.strip())
    if not match:
        return []
    book, tail = match.group(1), match.group(2).strip()
    if _WHOLE_CHAPTER.match(tail):
        return [(book, int(tail), None, None)]
    verse = _ONE_VERSE.match(tail)
    if verse:
        chapter, number = int(verse.group(1)), int(verse.group(2))
        return [(book, chapter, number, number)]
    span = _SPAN.match(tail)
    if not span:
        return []
    first_chapter, first_verse = int(span.group(1)), int(span.group(2))
    last_chapter = int(span.group(3) or first_chapter)
    last_verse = int(span.group(4))
    if last_chapter < first_chapter:
        return []
    if last_chapter == first_chapter:
        return [(book, first_chapter, first_verse, max(first_verse, last_verse))]
    # A span across chapters is open at the seam: the first chapter runs to its
    # end and the last begins at its start, exactly as `_loci.range_to_loci`
    # splits a reading. Splitting at the boundary is not the same as dropping
    # what lies past it.
    extents: list[Extent] = [(book, first_chapter, first_verse, None)]
    extents += [(book, c, None, None) for c in range(first_chapter + 1, last_chapter)]
    extents.append((book, last_chapter, None, last_verse))
    return extents


def _extents_meet(one: Extent, two: Extent) -> bool:
    book, chapter, first, last = one
    other_book, other_chapter, other_first, other_last = two
    if book != other_book or chapter != other_chapter:
        return False
    if first is not None and other_last is not None and first > other_last:
        return False
    if other_first is not None and last is not None and other_first > last:
        return False
    return True


def overlapping_keys(keys: list[str]) -> list[tuple[str, str]]:
    """Pairs of index keys that cover some of the same text.

    An index answers one question once. Two keys over one stretch of scripture
    give a consumer two different corpora for the same passage — the chapter
    row and the verse row each look complete, and each is missing what the
    other holds.
    """
    parsed = [(key, key_extents(key)) for key in keys]
    # Only keys naming the same book can meet, so the comparison stays within
    # a book rather than running over every pair in the index.
    by_book: dict[str, set[int]] = {}
    for index, (_key, extents) in enumerate(parsed):
        for book, _chapter, _first, _last in extents or [("", 0, None, None)]:
            by_book.setdefault(book, set()).add(index)
    clashes: set[tuple[str, str]] = set()
    for members in by_book.values():
        ordered = sorted(members)
        for position, left in enumerate(ordered):
            for right in ordered[position + 1:]:
                (one, one_extents), (two, two_extents) = parsed[left], parsed[right]
                if one_extents and two_extents:
                    met = any(_extents_meet(a, b) for a in one_extents for b in two_extents)
                else:
                    # Unparseable: the only overlap that can be proved is that
                    # the two keys are spelled the same.
                    met = one == two
                if met:
                    first, second = sorted((one, two))
                    clashes.add((first, second))
    return sorted(clashes)


# --- which numbering the keys are in ----------------------------------------
#
# The system a reference is written in is the element a citation almost never
# writes down, and the one that decides what it means. It is not a two-way
# vulgate-or-hebrew flag: `guidance/versification.md` §3.3 and §7.4 record that
# the Vulgate and the Greek disagree with each other and not merely with the
# Hebrew — TVTMS gives Vulgate Psalm 9:22-39 against Greek 9:21-38 for the same
# words — and the catena's Genesis pilot already holds Basil, whose text is
# Greek, while Brenton's Septuagint is a tracked edition. A vocabulary that
# could not tell those apart would have to call one of them the other.
#
# The Patristic Text Archive writes `LXX:Ps:83:7` and Biblindex writes
# `Vg:Mc:12:8:6-8`: both put the system in first position of every reference.
# This index does not, because its keys are derived by promotion from the
# ledger and a prefix on 524 of them would be 524 restatements of one fact. It
# declares the system once at the file level instead, and writes a row-level
# override only where a key is not in it — the §8.0 projection shape, where
# identity writes nothing.
CANONICAL = _projection.CANONICAL

# What `numbering` may say at the file level. Named narrowly enough to
# distinguish two states of one tradition (§7.4): `greek` is the numbering the
# Revised Version and the King James print for the Greek-divided books, which
# is not `septuagint`, and `nova-vulgata` is not `vulgate`.
NUMBERING_SYSTEMS = (
    "vulgate",
    "hebrew",
    "greek",
    "septuagint",
    "nova-vulgata",
    "nab",
)

# A row-level value only, and the one §8.0 already defines: known to diverge,
# correspondence not established. A key whose every citation means a different
# chapter of the canon is not in the declared system, and the harvest ledger
# records no numbering at all, so which system it *is* in cannot be derived.
# Saying `unrecorded` is the whole of what is known; naming a system would be
# the guess this apparatus exists to refuse.
UNRECORDED = "unrecorded"

PSALMS = _psalms.PSALMS


def declared_numbering(document: dict, where: str) -> str:
    """The system an index's keys are addressed in, or raise saying so.

    An index with no declaration is the defect this exists to stop. Its keys
    resolve either way — Vulgate Psalm 24 and Hebrew Psalm 24 are both real
    psalms — so a consumer reading the wrong one gets real commentary attached
    to the wrong text and nothing counts it as a failure.
    """
    declared = document.get("numbering") if isinstance(document, dict) else None
    if not declared:
        raise ValueError(
            f"{where}: no `numbering` declared; the keys name a chapter and not "
            "the system it is numbered in, and Vulgate Psalm 24 is Hebrew 25 — "
            f"declare one of {list(NUMBERING_SYSTEMS)}"
        )
    if declared not in NUMBERING_SYSTEMS:
        raise ValueError(
            f"{where}: numbering is {declared!r}, which is not one of "
            f"{list(NUMBERING_SYSTEMS)}"
        )
    return str(declared)


def row_numbering(row: dict) -> str:
    """A row's own system, when it overrides the file's, else ''."""
    if not isinstance(row, dict):
        return ""
    return str(row.get("numbering") or "").strip()


def impossible_key(key: str, system: str, chapters: dict[str, int]) -> str:
    """Why `key` cannot exist in `system`, or '' when it can.

    `chapters` maps a book name to the last chapter the canonical witness
    prints, so the ceiling is read from a tracked edition rather than typed
    here. The psalter's bounds come from `_psalms`, which reads the tracked
    concordance and knows both systems' extents: the Vulgate prints Psalm 115
    as verses 10-19 where the Hebrew has none of it, so a verse-bearing key is
    checkable in a way a chapter-bearing one is not.
    """
    extents = key_extents(key)
    if not extents:
        return f"{key!r} is not a locus this key space can parse"
    problems: list[str] = []
    for book, chapter, first, last in extents:
        if book == PSALMS and system in _psalms.SYSTEMS:
            for verse in (first, last):
                problem = _psalms.validate_psalm(chapter, verse, system)
                if problem and problem not in problems:
                    problems.append(problem)
            continue
        ceiling = chapters.get(book)
        if ceiling is None:
            problems.append(f"{book!r} is not a book of the canon")
        elif chapter > ceiling:
            problems.append(
                f"{book} {chapter} is past {system} {book}, which ends at "
                f"chapter {ceiling}"
            )
    return "; ".join(problems)


def moved_citations(document: dict) -> dict[str, str]:
    """A calendar's citations whose own resolution lands in another chapter.

    `citation_divergences` records, per citation, the locus in the Vulgate's
    numbering that the citation actually names. Most of those corrections move
    a verse inside its chapter and leave the chapter key alone. The ones that
    move the chapter are the ones that matter here, because the chapter is what
    the index is keyed on: `Joel 3:1-5` is Vulgate `Joel 2:28-32`, so a key
    derived from it is not Vulgate Joel 3 — and Vulgate Joel 3 exists, is the
    valley of Josaphat, and is not what the mass is reading.
    """
    moved: dict[str, str] = {}
    if not isinstance(document, dict):
        return moved
    for entry in document.get("citation_divergences") or []:
        if not isinstance(entry, dict):
            continue
        for cited, resolved in (entry.get("citations") or {}).items():
            cited, resolved = str(cited), str(resolved)
            if set(chapter_loci(cited)) != set(chapter_loci(resolved)):
                moved[cited] = resolved
    return moved
