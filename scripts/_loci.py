"""Turn a converted verse range into the loci a reading page fetches.

A range is not always inside one chapter. `Exodus 14:15-15:1` is the Easter
Vigil's third lesson and `1 Corinthians 10:31-11:1` is an epistle as the missal
prints it, and a locus that keeps only the opening chapter turns both into a
verse span that runs backwards — 15 to 1 — which renders as nothing at all.
That is why this is one function and not a line inlined in each caller.

An open end means "to the end of the chapter" and an open beginning means "from
its first verse", so a span across chapters needs no verse counts to describe:
the middle chapters are simply open at both ends.

The second half places a citation's loci in each edition the site offers, where
that edition's own printing departs from the numbering it is addressed in. It
is shared by the two generators of browser structure -- `mass-propers` and
`reading-plan` -- so the propers and the plan cannot read one edition two ways.
"""

from __future__ import annotations

import functools
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]


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


class EditionReader(NamedTuple):
    """One edition the site offers, as a structure file must address it.

    `addressing` is the loci key the edition reads (`_psalms.addressing`).
    `carried` is the edition's own verse-alias table -- where it prints a
    cited locus, `None` where it records not carrying it -- with each row's
    note; `chapters` are the chapters that table touches.
    """

    id: str
    addressing: str
    carried: dict
    chapters: frozenset


@functools.lru_cache(maxsize=1)
def edition_readers() -> tuple[EditionReader, ...]:
    """Every publishable edition held in the repository, with its departure table.

    The structure's loci are per addressing, not per edition, and that is right
    as far as numbering goes. It is not the whole of what an edition prints: the
    Clementine opens Vulgate Psalm 115 at verse 1 where the numbering opens it
    at 10, carries Psalm 15:11 inside 15:10, and divides Psalm 42:5 between two
    verses of its own; the King James prints Vulgate Daniel 13 as Susanna and
    records no correspondence for Ecclesiasticus. Each edition's own
    `verse-aliases.tsv` says so, `index-bible` resolves through it, and the
    browser, reading the addressing's loci alone, served the Clementine's
    *in atriis domus Domini* for Lent 2's *Credidi, propter quod locutus sum*.
    The editions are `index-bible`'s register, read rather than restated, and
    each table is read through `_projection`, the one parser of it.
    """
    from _projection import alias_rows, point  # noqa: PLC0415
    from _psalms import addressing  # noqa: PLC0415

    loader = SourceFileLoader("_index_bible_register", str(ROOT / "tools" / "index-bible"))
    spec = spec_from_loader(loader.name, loader)
    register = module_from_spec(spec)
    loader.exec_module(register)
    readers: list[EditionReader] = []
    for name, edition in sorted(register.EDITIONS.items()):
        artifacts = register.SOURCE_ROOT / str(edition["artifacts"])
        if not edition["publishable"] or not artifacts.is_dir():
            continue
        carried: dict = {}
        for row in alias_rows(artifacts.parent):
            cited = point(row.cited_locus, name)
            target = point(row.resolves_to, name) if row.resolves_to else None
            carried[tuple(cited)] = (None if target is None else tuple(target), row.note)
        readers.append(
            EditionReader(
                id=name,
                addressing=addressing(str(edition["numbering"]), str(edition["psalm_titles"])),
                carried=carried,
                chapters=frozenset((token, chapter) for token, chapter, _ in carried),
            )
        )
    return tuple(readers)


def placed(reader: EditionReader, token: str, loci: list[dict]) -> tuple[list[dict], str]:
    """`loci` as this edition prints them, or the reason it cannot.

    The edition's alias table is consulted first and its answer is final, as in
    `index-bible`'s `Bible.carrier`: a renumbered verse moves, a merged one
    lands on the verse carrying it (printed once), and a recorded refusal
    refuses the citation for this edition with the table's own reason. A
    bound left open stays open -- it means the chapter's first or last verse as
    this edition prints it, which is why a whole psalm is never renumbered into
    its own numbering. Each locus keeps its own place in the citation, so a
    citation cited in pieces is still cited in pieces; loci in chapters the
    table does not touch pass through untouched.
    """
    moved: list[dict] = []
    for locus in loci:
        book = locus.get("book") or token
        chapter, first, last = locus["chapter"], locus.get("first"), locus.get("last")
        if (book, chapter) not in reader.chapters or (first is None and last is None):
            moved.append(dict(locus))
            continue

        def carrier(verse: int) -> tuple:
            return reader.carried.get((book, chapter, verse), ((book, chapter, verse), ""))

        if first is None or last is None:
            verse = int(first if first is not None else last)
            target, note = carrier(verse)
            if target is None:
                return [], f"{book} {chapter}:{verse} is recorded as not carried by this edition: {note}"
            if target[:2] != (book, chapter):
                return [], (
                    f"{book} {chapter}:{verse} stands at {target[0]} {target[1]}:{target[2]} "
                    f"in this edition, and the range's open end cannot be placed there"
                )
            moved.append({
                **locus,
                "first": None if first is None else target[2],
                "last": None if last is None else target[2],
            })
            continue
        carriers: list[tuple] = []
        for verse in range(int(first), int(last) + 1):
            target, note = carrier(verse)
            if target is None:
                return [], f"{book} {chapter}:{verse} is recorded as not carried by this edition: {note}"
            if not carriers or carriers[-1] != target:
                carriers.append(target)
        runs: list[list] = []
        for held, at, verse in carriers:
            if runs and runs[-1][:2] == [held, at] and runs[-1][3] + 1 == verse:
                runs[-1][3] = verse
            else:
                runs.append([held, at, verse, verse])
        for held, at, low, high in runs:
            row = {"chapter": at, "first": low, "last": high}
            moved.append(row if held == token else {"book": held, **row})
    return moved, ""


def edition_departures(
    token: str, loci: dict[str, list[dict]], refused: dict[str, str]
) -> tuple[dict[str, list[dict]], dict[str, str]]:
    """Each offered edition's own loci where its printing departs, and its refusals.

    `loci` is a citation's loci by addressing and `refused` the reasons any
    addressing could not take it. Returned: the loci of every edition whose
    verse-alias table moves them (`edition_loci`), and `refused` extended with
    every edition that table refuses. An edition whose addressing is already
    refused is left to that reason; one whose table moves nothing writes nothing.
    """
    departures: dict[str, list[dict]] = {}
    refused = dict(refused)
    for reader in edition_readers():
        base = loci.get(reader.addressing)
        if base is None:
            continue
        moved, problem = placed(reader, token, base)
        if problem:
            refused[reader.id] = problem
        elif moved != base:
            departures[reader.id] = moved
    return departures, refused
