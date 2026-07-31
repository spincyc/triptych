"""Loci shared by the commentary harvest and the corpus that consumes it.

The harvest is run by chapter and the corpus is keyed by verse range, so the
two speak different key spaces over the same material. `Psalms 24` and
`Psalms 24:1-24:3` name the same chapter and match as strings not at all: of
1596 corpus references only 13 found a harvested locus, so 184 of 195 masses
came back empty from a corpus that held 7297 attributions.

Both tools therefore derive their chapter loci here rather than each keeping
its own copy. A second implementation of this rule would be a restatement, and
restatements drift: the point of the key space is that both ends agree on it.
"""

from __future__ import annotations

import re


def chapter_loci(passage: str) -> list[str]:
    """Split a reference into one locus per chapter, never wider.

    A query may cover at most a single chapter: grouping across chapters drops
    works that comment on only one of them. Isaiah 63:16-64:7 is therefore two
    loci, not one, which costs more queries and loses nothing.
    """
    match = re.match(r"^(.*?)\s+(\d.*)$", passage.strip())
    if not match:
        return [passage]
    book, tail = match.group(1), match.group(2)
    chapters: list[str] = []
    for chapter in re.findall(r"(\d+):", tail) or re.findall(r"^(\d+)$", tail):
        locus = f"{book} {chapter}"
        if locus not in chapters:
            chapters.append(locus)
    return chapters or [passage]
