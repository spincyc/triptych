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

from _psalms import PSALMS

# How a refusal reads when it is the edition's own verse-alias table speaking
# rather than a gap. The distinction is load-bearing: a recorded refusal is
# settled data about the edition, and nothing downstream should read it as a
# correction that has gone stale.
NOT_CARRIED = "is recorded as not carried by this edition"


DIVERGENCES = "citation_divergences"

# The numbering every recorded resolution is written in. Each one was derived by
# reading the cited words out of a Vulgate-numbered edition, so it says where a
# Vulgate-numbered edition carries them and nothing more.
RESOLVED_IN = "vulgate"


# What a divergent locus says about an edition in some other numbering. The
# three are not interchangeable and the difference is the whole point: a book
# the Lectionary and a Greek-numbered New Testament divide alike wants the
# citation left exactly as it stands, and "correcting" it onto the Vulgate is
# the same silent mis-resolution in the other direction.
RESOLVED = "resolved"  # divides the book as the Vulgate does; use the resolution
AS_CITED = "as-cited"  # divides the book as the calendar cites it; leave it alone
UNRECORDED = "unrecorded"  # neither is established; refuse rather than guess
STANCES = (RESOLVED, AS_CITED, UNRECORDED)
STANCE = "numbering"


def chapters_touched(entry: dict) -> set[int]:
    """Every chapter a citation's ranges reach into, boundary-crossers included."""
    chapters: set[int] = set()
    for span in entry.get("ranges") or []:
        if not isinstance(span, dict):
            continue
        begin = span.get("begin") or {}
        end = span.get("end") or begin
        first = begin.get("chapter")
        if first is None:
            continue
        last = end.get("chapter")
        chapters.update(range(int(first), int(first if last is None else last) + 1))
    return chapters


class Divergences:
    """One calendar's declared numbering divergences, validated as they load.

    A declaration is worth only as much as its upkeep, so each one is checked
    against the citations the calendar actually makes. A resolution for a
    reference no longer cited, a resolution landing in another book, and a
    declared chapter nothing cites are all errors: dead entries that still read
    as coverage are how a table stops matching the thing it describes.

    What is deliberately *not* an error is a citation inside a declared locus
    with no resolution recorded. That one refuses, and the citation goes
    unindexed. Returning whatever verse the edition happens to print at those
    numbers is the defect this machinery exists to stop, and a refusal is the
    only answer that cannot be mistaken for the text.

    `numbering` is the numbering of the edition being indexed. The recorded
    resolutions are written in `RESOLVED_IN`; every other numbering an indexed
    edition may be in must be ruled on per locus under `STANCE`, because a book
    two systems divide alike wants no correction at all.
    """

    def __init__(
        self,
        calendar: str,
        document: dict,
        entries: list[dict],
        canon,
        numbering: str = RESOLVED_IN,
        *,
        numberings: tuple[str, ...],
    ) -> None:
        self.calendar = calendar
        self.canon = canon
        self.numbering = numbering
        self.numberings = numberings
        self.loci: list[tuple[str, frozenset[int], str, dict[str, str]]] = []
        self.resolved: dict[str, tuple[str, str, list]] = {}
        # Absent and empty both mean the calendar claims no divergence; a value
        # of any other shape is a mistake, and reading it as "none" would drop
        # the declaration silently, which is the failure mode being fixed here.
        declared = document.get(DIVERGENCES)
        declared = [] if declared is None else declared
        if not isinstance(declared, list):
            raise ValueError(f"{calendar}: {DIVERGENCES} must be a list of divergent loci")
        self.cited: dict[str, tuple[str, set[int]]] = {}
        for entry in entries:
            ref = str(entry["ref"])
            if ref not in self.cited:
                self.cited[ref] = (str(entry.get("book") or ""), chapters_touched(entry))
        for locus in declared:
            self._declare(locus)

    def _declare(self, locus: object) -> None:
        where = f"{self.calendar}: {DIVERGENCES}"
        if not isinstance(locus, dict):
            raise ValueError(f"{where}: each divergent locus must be a mapping")
        book = locus.get("book")
        if not isinstance(book, str) or not book:
            raise ValueError(f"{where}: a divergent locus must name a book")
        if book == PSALMS:
            # The psalter has a tracked verse-level concordance and converts
            # through it; a second mechanism here could only contradict it.
            raise ValueError(f"{where}: {book} numbering is owned by the psalm concordance")
        reason = locus.get("divergence")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{where}: {book} must say how the numbering diverges")
        chapters = self._chapters(where, book, locus.get("chapters"))
        stances = self._stances(where, book, locus.get(STANCE))
        resolutions = locus.get("citations")
        if not isinstance(resolutions, dict) or not resolutions:
            raise ValueError(f"{where}: {book} declares no citations; remove the locus instead")
        covered: set[int] = set()
        for ref, target in sorted(resolutions.items()):
            covered |= self._resolve(where, book, chapters, str(ref), target)
        stale = sorted(chapters - covered) if chapters else []
        if stale:
            raise ValueError(
                f"{where}: {book} declares chapters {stale} that no listed citation reaches"
            )
        self.loci.append((book, chapters, reason.strip(), stances))

    def _stances(self, where: str, book: str, declared: object) -> dict[str, str]:
        """Where each other numbering stands on this book, ruled on one by one.

        A default would be the wrong shape for this question: the two answers
        are opposites, one correcting a citation and the other leaving it
        untouched, and whichever were the default would be applied silently to
        the books nobody had thought about yet.
        """
        wanted = self.numberings
        if not isinstance(declared, dict):
            raise ValueError(
                f"{where}: {book} must say under {STANCE} where each of "
                f"{list(wanted)} stands, one of {list(STANCES)}"
            )
        for numbering in wanted:
            stance = declared.get(numbering)
            if stance not in STANCES:
                raise ValueError(
                    f"{where}: {book} {STANCE} for {numbering!r} is {stance!r}; "
                    f"it must be one of {list(STANCES)}"
                )
        extra = sorted(set(declared) - set(wanted))
        if extra:
            raise ValueError(
                f"{where}: {book} {STANCE} rules on {extra}, which no indexed edition "
                f"is in ({RESOLVED_IN} always takes the resolution and is not listed)"
            )
        return {numbering: str(declared[numbering]) for numbering in wanted}

    def _chapters(self, where: str, book: str, declared: object) -> frozenset[int]:
        """The chapters this book diverges in; empty means the whole book."""
        if declared is None:
            return frozenset()
        if not isinstance(declared, list) or not declared:
            raise ValueError(f"{where}: {book} chapters must be a non-empty list")
        for chapter in declared:
            if not isinstance(chapter, int) or isinstance(chapter, bool) or chapter < 1:
                raise ValueError(f"{where}: {book} chapter {chapter!r} is not a chapter number")
        return frozenset(declared)

    def _resolve(
        self, where: str, book: str, chapters: frozenset[int], ref: str, target: object
    ) -> set[int]:
        """Validate one recorded resolution and keep it. Returns what it covers."""
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"{where}: {book} resolution for {ref!r} must be a reference string")
        if ref in self.resolved:
            raise ValueError(f"{where}: {ref!r} is resolved twice")
        found = self.cited.get(ref)
        if found is None:
            raise ValueError(f"{where}: {ref!r} is resolved but no longer cited by this calendar")
        home, touched = found
        if home != book:
            raise ValueError(f"{where}: {ref!r} is cited under {home!r}, not {book!r}")
        if chapters and not touched & chapters:
            raise ValueError(f"{where}: {ref!r} reaches no divergent chapter of {book}")
        try:
            passage = self.canon.parse_citation(target.strip())
        except self.canon.CitationError as error:
            raise ValueError(
                f"{where}: {ref!r} resolves to an unreadable reference: {error}"
            ) from error
        if passage["book"] != book:
            # An override may correct the numbering, never the book: a citation
            # that resolves into another book is a different citation.
            raise ValueError(
                f"{where}: {ref!r} resolves into {passage['book']}, outside {book}"
            )
        self.resolved[ref] = (book, target.strip(), passage["ranges"])
        return touched & chapters if chapters else touched

    def locus_of(self, book: str, touched: set[int]) -> tuple[str, dict[str, str]] | None:
        """The declared locus this citation falls in: how it diverges, and stances."""
        for declared, chapters, reason, stances in self.loci:
            if declared == book and (not chapters or touched & chapters):
                return reason, stances
        return None

    def stance(self, stances: dict[str, str]) -> str:
        """What this locus says about the edition being indexed."""
        if self.numbering == RESOLVED_IN:
            return RESOLVED
        return stances.get(self.numbering, UNRECORDED)

    def apply(self, entry: dict, ranges: list) -> tuple[list, str]:
        """The ranges that select this citation's text here, or why it refuses."""
        book = str(entry.get("book") or "")
        found = self.locus_of(book, chapters_touched(entry))
        if found is None:
            return ranges, ""
        reason, stances = found
        stance = self.stance(stances)
        if stance == AS_CITED:
            # This edition divides the book the way the calendar cites it, so
            # the citation already names the verses it means.
            return ranges, ""
        if stance == UNRECORDED:
            return [], (
                f"{self.calendar} numbers {book} divergently ({reason}); this edition is "
                f"in {self.numbering} numbering and the locus records no ruling for it "
                f"beyond {UNRECORDED!r}"
            )
        recorded = self.resolved.get(str(entry["ref"]))
        if recorded is not None:
            return recorded[2], ""
        return [], (
            f"{self.calendar} numbers {book} divergently ({reason}) and records no "
            f"resolution for this citation; add one under {DIVERGENCES}"
        )

    def confirm(self, bible: "Bible") -> None:
        """Every resolution must reach real text in an edition holding its book.

        A citation the edition cannot address is ordinary — a calendar may cite
        a book this edition never printed. A hand-written resolution that
        cannot be addressed is not: it is a correction that has stopped
        correcting, and it fails the build rather than joining the unresolved
        tally where a reader would read it as the calendar's problem.

        An edition the resolutions do not apply to is not asked to address
        them: it never uses one, and failing its build over a correction meant
        for another numbering would report the wrong edition's problem. Neither
        is an edition that has recorded, in its own verse aliases, that it does
        not carry the locus. That refusal is the edition speaking about itself,
        and it belongs in the unresolved tally rather than stopping the build.
        """
        for ref, (book, target, ranges) in sorted(self.resolved.items()):
            token = bible.token(book)
            if token is None:
                continue
            found = self.locus_of(book, self.cited[ref][1])
            if found is None or self.stance(found[1]) != RESOLVED:
                continue
            _, problem = bible.passage(token, ranges)
            if problem and not problem.endswith(NOT_CARRIED):
                raise ValueError(
                    f"{self.calendar}: {DIVERGENCES} resolves {ref!r} to {target!r}, "
                    f"which this edition cannot address: {problem}"
                )




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
