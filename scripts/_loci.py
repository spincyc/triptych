"""Turn a converted verse range into the loci a reading page fetches.

A range is not always inside one chapter. `Exodus 14:15-15:1` is the Easter
Vigil's third lesson and `1 Corinthians 10:31-11:1` is an epistle as the missal
prints it, and a locus that keeps only the opening chapter turns both into a
verse span that runs backwards — 15 to 1 — which renders as nothing at all.
That is why this is one function and not a line inlined in each caller.

An open end means "to the end of the chapter" and an open beginning means "from
its first verse", so a span across chapters needs no verse counts to describe:
the middle chapters are simply open at both ends.
"""

from __future__ import annotations


def range_to_loci(begin: dict, end: dict) -> list[dict]:
    """One locus per chapter the range touches, in reading order."""
    first_chapter = begin.get("chapter")
    if first_chapter is None:
        return []
    last_chapter = end.get("chapter", first_chapter)
    if last_chapter is None:
        last_chapter = first_chapter
    first_chapter, last_chapter = int(first_chapter), int(last_chapter)
    if last_chapter < first_chapter:
        # A descending range is a defect in the citation, not something to
        # render; the caller reports it rather than guessing what was meant.
        raise ValueError(
            f"range ends at chapter {last_chapter} but begins at {first_chapter}"
        )
    if first_chapter == last_chapter:
        first_verse, last_verse = begin.get("verse"), end.get("verse")
        # The same refusal as the chapter one above, for the same reason. It was
        # missing here for as long as the chapter check has existed, and the
        # test named for it never reached this branch because every case it
        # carried crossed a chapter — so `Psalm 24:9-3` returned a locus running
        # from 9 to 3, which renders as nothing at all. That is the very defect
        # this module's docstring was written about, surviving inside it.
        if first_verse is not None and last_verse is not None:
            if int(last_verse) < int(first_verse):
                raise ValueError(
                    f"range ends at {first_chapter}:{last_verse} "
                    f"but begins at {first_chapter}:{first_verse}"
                )
        return [
            {
                "chapter": first_chapter,
                "first": first_verse,
                "last": last_verse,
            }
        ]
    loci = [{"chapter": first_chapter, "first": begin.get("verse"), "last": None}]
    loci.extend(
        {"chapter": chapter, "first": None, "last": None}
        for chapter in range(first_chapter + 1, last_chapter)
    )
    loci.append({"chapter": last_chapter, "first": None, "last": end.get("verse")})
    return loci
