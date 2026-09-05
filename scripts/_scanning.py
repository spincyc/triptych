#!/usr/bin/env python3
"""Look for many literal needles in a lot of text, without asking each one.

Several gates here answer the same shape of question: does any of a large set
of protected identities appear anywhere in this corpus. Asked directly it is
one substring search per identity per document --- 1,146 identities against
every published file --- and it was the most expensive thing in two of the
suite's slowest tests.

The saving is a pre-filter that can only ever say "impossible", never "absent":

- Every identity shares one of a handful of leading fragments, because ids in
  this repository are `artifact.`/`edition.` prefixed. A document containing
  none of those fragments contains no identity, so the whole set can be skipped
  after two C-level searches.
- The fragments are DERIVED from the needles on every call, never written down.
  That is the entire safety of it: an identity in some new shape extends the
  marker set by itself, where a hardcoded pair would silently stop matching it
  and the gate would pass what it could not see.

Nothing here decides that a needle IS present --- that is still an exact
substring test against the real text. The pre-filter only decides where no
exact test is worth running, and a wrong pre-filter would be the reference that
resolves successfully and wrongly, which `guidance/the-shape.md` names as the
one defect this repository exists to refuse.
"""

from __future__ import annotations

import re
from typing import Iterable, Sequence

# Short enough that every id has one, long enough to be rare in running prose.
MARKER_LENGTH = 8


def markers_for(needles: Iterable[str]) -> tuple[str, ...]:
    """The distinct leading fragments of *needles*, as a sound pre-filter.

    If a text contains needle `n`, it contains `n[:MARKER_LENGTH]`. So a text
    containing no marker contains no needle. A needle shorter than the marker
    length contributes itself, which keeps the implication true.
    """
    return tuple(sorted({needle[:MARKER_LENGTH] for needle in needles if needle}))


# The characters a repository id is made of. Used to cut a document into the
# runs an id could possibly lie inside; anything else is a boundary.
_TOKEN = re.compile(r"[A-Za-z0-9._:@+-]+")
_SEPARATOR = "\x00"


def present(
    haystack: str,
    needles: Sequence[str],
    markers: tuple[str, ...] | None = None,
) -> list[str]:
    """Every needle that actually occurs in *haystack*, in the given order.

    The answer is exactly `[n for n in needles if n in haystack]`, reached two
    cheaper ways first.

    The markers skip the whole set when none of them occurs. That is the common
    case, and on its own it was not enough: the files that do carry an
    `artifact.`/`edition.` id are the three multi-megabyte propers projections,
    and 1,146 searches across 28 MB is most of a second per file.

    So the haystack is reduced to the distinct runs of id-legal characters in
    it, joined by a separator that is not id-legal. An id is a contiguous run
    of those characters, so it can only lie inside one such run, and the runs
    of a 13 MB projection are a few thousand distinct tokens rather than
    millions of repeated ones. Both directions hold exactly: a needle in the
    document lies inside some run and so inside the join, and a needle in the
    join cannot straddle the separator because it contains no such character.

    That argument depends on every needle being made only of id-legal
    characters. Where one is not --- which no id here is, but nothing stops a
    caller --- the reduction is skipped and the direct scan answers instead,
    rather than a faster wrong answer.
    """
    if not needles:
        return []
    if markers is None:
        markers = markers_for(needles)
    if markers and not any(marker in haystack for marker in markers):
        return []
    if all(_TOKEN.fullmatch(needle) for needle in needles):
        haystack = _SEPARATOR.join(set(_TOKEN.findall(haystack)))
    return [needle for needle in needles if needle in haystack]
