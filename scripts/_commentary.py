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
"""

from __future__ import annotations

import re

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
