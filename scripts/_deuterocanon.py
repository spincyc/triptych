"""Numbering of Esther, Ecclesiasticus and Daniel across the arrangements.

The three deuterocanonical books that the Latin and Greek traditions arrange
differently, and the only three the tracked calendars cite where the difference
changes what a reference selects. The psalter has had a verse-level concordance
since the same defect was found there; these three had none, and a citation of
`Daniel 14:27` or `Ecclesiasticus 36:18` resolved against a Greek-numbered
edition returned real text under a correct-looking reference and reported
nothing.

An *arrangement* here is a way of dividing and addressing these books, named for
what it is rather than for one edition that prints it:

    vulgate                 Esther in sixteen chapters with the Greek additions
                            appended as 10:4-16:24; Daniel in fourteen chapters
                            with the Canticle inside 3:24-90; Ecclesiasticus in
                            the long Latin form. Witnessed by the Douay-Rheims
                            and, in Latin, by the Clementine.

    greek                   Esther in ten chapters with the additions in a book
                            of their own; Daniel in twelve, with the Song of the
                            Three, Susanna and Bel as separate books;
                            Ecclesiasticus in the corrected Greek form.
                            Witnessed by the Revised Version and the King James
                            Apocrypha.

    world-english-catholic  The Greek divisions, addressed as the Greek Daniel
                            and Esther address them: the Canticle inside Daniel
                            3, Susanna as Daniel 13, Bel as Daniel 14, and the
                            Esther additions merged into the chapters they
                            belong to. Witnessed by the World English Bible,
                            Catholic Edition, and by nothing else here.

The third is a distinct arrangement and not a departure from the second, which
is why it is named: its Daniel 14 runs one verse ahead of the Vulgate's from
beginning to end, and no edition-level departure table would say so.

The concordance is a table of correspondences between two arrangements, one row
per run of verses. Both sides of every row name their arrangement, so no column
means anything by position and no reader has to infer which system a number is
in. That is the failure the psalm concordance still carries: its `hebrew` column
records the Vulgate's division of a psalm under Hebrew numbers, which is a third
thing and is named for neither.

Six relations are expressible, and three of them the psalm table cannot say:

    one-to-one     equal-length runs, verse for verse
    split-right    one verse on the left becomes several on the right
    merged-right   several verses on the left become one on the right
    absent-right   text one arrangement carries and the other does not
    absent-left    the same in the other direction
    not-recorded   known to diverge here, with no correspondence established

The psalm table requires each row's two runs to be the same length and each
psalter continuous per chapter, so it can say only `one-to-one`. Esther 15 needs
three of the six in one chapter: the Vulgate's 15:1-3 is absent from the Greek,
its 15:13-14 is the Greek's single 15:10, and its 15:15 is the Greek's 15:11-12.

`not-recorded` is a positive statement, not a gap. It is the difference between
"nobody has looked" and "someone looked and found no clean correspondence", and
it is what Ecclesiasticus gets: the Vulgate and the Greek divide that book
differently in all fifty-one chapters, so no offset, per chapter or per book,
carries it.

Nothing here is trusted on its word. `_concordance` reads the tracked verse text
of each arrangement's witness edition and refuses to load a table whose rows do
not tile every book's printed extent exactly once, or whose recorded opening
words are not the words the witness prints at that locus. A hand-typed ceiling
cannot rot unnoticed here, because no ceiling is typed.
"""

from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parents[1]
WORKS = ROOT / "src" / "sources" / "works"

# The concordance, tracked as an artifact of the edition it was compiled from
# and against. It is a Triptych-created reference table of numbering alone and
# carries no scripture text beyond the opening words each row is checked by.
CONCORDANCE_ROOT = (
    WORKS / "english-college-of-douay" / "douay-rheims-bible"
    / "editions" / "challoner-gutenberg-1581" / "artifacts"
)
CONCORDANCE_GLOB = "deuterocanon-numbering-*/deuterocanon-numbering.tsv"

# The edition whose tracked verse text stands for each arrangement, and the
# artifact directory it is read from. The witness is what the table is validated
# against; where a second tracked edition is in the same arrangement it is a
# control and is named in the artifact record, not here.
WITNESSES: dict[str, str] = {
    "vulgate": "english-college-of-douay/douay-rheims-bible/editions"
    "/challoner-gutenberg-1581/artifacts",
    "greek": "convocation-of-canterbury/revised-version/editions/ebible-eng-rv/artifacts",
    "world-english-catholic": "ebible-org/world-english-bible/editions"
    "/catholic-eng-web-c/artifacts",
}

# The books this concordance rules on. A citation of anything else is not its
# business, and saying so is not a refusal.
BOOKS = ("Esth", "EsthGr", "Ecclus", "Dan", "SgThree", "Sus", "Bel")

ONE_TO_ONE = "one-to-one"
SPLIT_RIGHT = "split-right"
MERGED_RIGHT = "merged-right"
ABSENT_RIGHT = "absent-right"
ABSENT_LEFT = "absent-left"
NOT_RECORDED = "not-recorded"
RELATIONS = (
    ONE_TO_ONE, SPLIT_RIGHT, MERGED_RIGHT, ABSENT_RIGHT, ABSENT_LEFT, NOT_RECORDED
)

# How many opening words a row records. Enough to identify the verse in any
# translation of it; few enough that the table stays a numbering table.
OPENING_WORDS = 7

_NOT_LETTERS = re.compile(r"[^a-z0-9 ]+")


class NumberingError(ValueError):
    """A reference cannot be converted between two arrangements."""


class ConcordanceUnavailable(RuntimeError):
    """The concordance is missing or self-contradictory, so nothing converts."""


class Locus(NamedTuple):
    """One run of verses inside one chapter of one book of one arrangement."""

    arrangement: str
    book: str
    chapter: int
    first: int
    last: int

    def __str__(self) -> str:
        span = str(self.first) if self.first == self.last else f"{self.first}-{self.last}"
        return f"{self.arrangement} {self.book} {self.chapter}:{span}"

    @property
    def length(self) -> int:
        return self.last - self.first + 1


class Correspondence(NamedTuple):
    """One row: what the left run is in the right arrangement, and how exactly.

    Both arrangements are always named, so a row still says which pair it
    belongs to when one side has no verses at all — which is how an addition
    absent from the other tradition is recorded rather than merely omitted.
    """

    pair: tuple[str, str]
    left: Locus | None
    right: Locus | None
    relation: str
    note: str

    def flipped(self) -> "Correspondence":
        """The same statement read from the other side."""
        mirror = {
            SPLIT_RIGHT: MERGED_RIGHT,
            MERGED_RIGHT: SPLIT_RIGHT,
            ABSENT_RIGHT: ABSENT_LEFT,
            ABSENT_LEFT: ABSENT_RIGHT,
        }
        return Correspondence(
            (self.pair[1], self.pair[0]),
            self.right,
            self.left,
            mirror.get(self.relation, self.relation),
            self.note,
        )


def normalize(text: str) -> str:
    """Verse text reduced to the letters and digits an opening is compared on."""
    return " ".join(_NOT_LETTERS.sub(" ", text.casefold()).split())


@lru_cache(maxsize=None)
def _printed(arrangement: str) -> dict[tuple[str, int, int], str]:
    """Every verse the witness edition prints, for the books in scope."""
    where = WITNESSES.get(arrangement)
    if where is None:
        raise ConcordanceUnavailable(f"no witness edition is declared for {arrangement!r}")
    artifacts = WORKS / where
    verses: dict[tuple[str, int, int], str] = {}
    for path in sorted(artifacts.glob("verse-text-*/*.tsv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for line in csv.DictReader(handle, delimiter="\t"):
                if line["book"] in BOOKS:
                    verses[(line["book"], int(line["chapter"]), int(line["verse"]))] = (
                        line["text"]
                    )
    if not verses:
        raise ConcordanceUnavailable(
            f"the witness for {arrangement} carries none of {list(BOOKS)}: {artifacts}"
        )
    return verses


def _extents(arrangement: str) -> dict[tuple[str, int], tuple[int, int]]:
    """The first and last verse number the witness prints in each chapter.

    Read from the text, never declared. The psalm concordance's hand-typed
    ceilings were wrong for two psalms and nothing noticed; a ceiling that is
    derived cannot be wrong without the text being wrong.
    """
    bounds: dict[tuple[str, int], tuple[int, int]] = {}
    for book, chapter, verse in _printed(arrangement):
        low, high = bounds.get((book, chapter), (verse, verse))
        bounds[(book, chapter)] = (min(low, verse), max(high, verse))
    return bounds


def _span(field: str) -> tuple[int, int] | None:
    text = field.strip()
    if not text:
        return None
    low, _, high = text.partition("-")
    return int(low), int(high or low)


def _arrangement(row: dict[str, str], side: str, where: str) -> str:
    named = row[f"{side}_arrangement"].strip()
    if named not in WITNESSES:
        raise ConcordanceUnavailable(
            f"{where}: the {side} arrangement is {named!r}; the declared ones are "
            f"{sorted(WITNESSES)}"
        )
    return named


def _side(row: dict[str, str], side: str, arrangement: str, where: str) -> Locus | None:
    book = row[f"{side}_book"].strip()
    if not book:
        if row[f"{side}_chapter"].strip() or row[f"{side}_verses"].strip():
            raise ConcordanceUnavailable(f"{where}: a {side} locus with no book")
        return None
    if book not in BOOKS:
        raise ConcordanceUnavailable(f"{where}: {arrangement} names book {book!r}")
    span = _span(row[f"{side}_verses"])
    if span is None:
        raise ConcordanceUnavailable(f"{where}: {arrangement} {book} names no verses")
    first, last = span
    if last < first:
        raise ConcordanceUnavailable(f"{where}: {arrangement} {book} runs {first}-{last}")
    return Locus(arrangement, book, int(row[f"{side}_chapter"]), first, last)


def _check_shape(entry: Correspondence, where: str) -> None:
    left, right, relation = entry.left, entry.right, entry.relation
    if relation not in RELATIONS:
        raise ConcordanceUnavailable(f"{where}: unknown relation {relation!r}")
    if left is None and right is None:
        raise ConcordanceUnavailable(f"{where}: a row naming no verses at all")
    if relation == ABSENT_RIGHT and (left is None or right is not None):
        raise ConcordanceUnavailable(
            f"{where}: {ABSENT_RIGHT} means the left run has no counterpart, so it "
            f"needs a left run and no right one"
        )
    if relation == ABSENT_LEFT and (right is None or left is not None):
        raise ConcordanceUnavailable(
            f"{where}: {ABSENT_LEFT} means the right run has no counterpart, so it "
            f"needs a right run and no left one"
        )
    if relation not in (ABSENT_RIGHT, ABSENT_LEFT, NOT_RECORDED) and (
        left is None or right is None
    ):
        raise ConcordanceUnavailable(f"{where}: {relation} needs a run on both sides")
    if left is None or right is None:
        return
    if relation == ONE_TO_ONE and left.length != right.length:
        raise ConcordanceUnavailable(
            f"{where}: {left} is {left.length} verses and {right} is {right.length}; "
            f"{ONE_TO_ONE} needs runs of equal length"
        )
    if relation == SPLIT_RIGHT and not (left.length == 1 and right.length > 1):
        raise ConcordanceUnavailable(
            f"{where}: {SPLIT_RIGHT} means one verse becoming several, and this is "
            f"{left.length} becoming {right.length}"
        )
    if relation == MERGED_RIGHT and not (left.length > 1 and right.length == 1):
        raise ConcordanceUnavailable(
            f"{where}: {MERGED_RIGHT} means several verses becoming one, and this is "
            f"{left.length} becoming {right.length}"
        )


def _check_opening(locus: Locus | None, recorded: str, where: str, side: str) -> None:
    """The recorded opening must be what the witness prints at the locus.

    A row whose openings still match cannot have drifted away from the text; a
    row whose openings no longer match is a table that has stopped describing
    the library, and loading it would convert references by a rule nothing
    supports any longer.
    """
    recorded = recorded.strip()
    if locus is None:
        if recorded:
            raise ConcordanceUnavailable(f"{where}: a {side} opening with no {side} run")
        return
    printed = _printed(locus.arrangement).get((locus.book, locus.chapter, locus.first))
    if printed is None:
        # A number inside a chapter's extent that the witness does not print;
        # the extent check owns that, and there is nothing to compare here.
        if recorded:
            raise ConcordanceUnavailable(
                f"{where}: the {locus.arrangement} witness prints no "
                f"{locus.book} {locus.chapter}:{locus.first}, but an opening is recorded"
            )
        return
    if not recorded:
        raise ConcordanceUnavailable(f"{where}: {locus} records no opening words")
    if not normalize(printed).startswith(recorded):
        raise ConcordanceUnavailable(
            f"{where}: {locus} is recorded as opening {recorded!r}, but the witness "
            f"prints {' '.join(normalize(printed).split()[:OPENING_WORDS])!r}"
        )


def _check_coverage(path: Path, entries: list[Correspondence]) -> None:
    """Within each pair, each side must account for every verse its witness prints.

    Both ends of every chapter come from the tracked text rather than from a
    column, so a row that overruns a chapter or stops short of it is caught
    without any ceiling having been declared. Accounting is not the same as
    mapping: a `not-recorded` or `absent` row accounts for its verses by saying
    what is known about them, which is exactly the difference between a
    reviewed refusal and a hole.
    """
    claimed: dict[tuple[tuple[str, str], str, str, int], dict[int, str]] = {}
    for entry in entries:
        for locus in (entry.left, entry.right):
            if locus is None:
                continue
            key = (entry.pair, locus.arrangement, locus.book, locus.chapter)
            seen = claimed.setdefault(key, {})
            for verse in range(locus.first, locus.last + 1):
                if verse in seen:
                    raise ConcordanceUnavailable(
                        f"{path}: {locus.arrangement} {locus.book} "
                        f"{locus.chapter}:{verse} is claimed twice between "
                        f"{entry.pair[0]} and {entry.pair[1]}"
                    )
                seen[verse] = entry.relation
    for (pair, arrangement, book, chapter), verses in sorted(claimed.items()):
        printed = _printed(arrangement)
        here = sorted(v for (b, c, v) in printed if b == book and c == chapter)
        if not here:
            raise ConcordanceUnavailable(
                f"{path}: the {arrangement} witness has no {book} {chapter}"
            )
        missing = [verse for verse in here if verse not in verses]
        if missing:
            raise ConcordanceUnavailable(
                f"{path}: between {pair[0]} and {pair[1]}, {arrangement} {book} "
                f"{chapter} leaves verses {missing[0]}-{missing[-1]} unaccounted for"
            )
        beyond = sorted(verse for verse in verses if not here[0] <= verse <= here[-1])
        if beyond:
            raise ConcordanceUnavailable(
                f"{path}: between {pair[0]} and {pair[1]}, {arrangement} {book} "
                f"{chapter} claims verse {beyond[0]}, but the witness prints only "
                f"{here[0]}-{here[-1]}"
            )
    # Every chapter of every book a pair rules on must be ruled on. A book half
    # covered would refuse half its citations for no recorded reason, which is
    # the silent gap `not-recorded` exists to replace.
    for pair in sorted({key[0] for key in claimed}):
        ruled = {key[1:] for key in claimed if key[0] == pair}
        books = {(arrangement, book) for arrangement, book, _ in ruled}
        for arrangement, book in sorted(books):
            for (there, chapter) in sorted(_extents(arrangement)):
                if there == book and (arrangement, book, chapter) not in ruled:
                    raise ConcordanceUnavailable(
                        f"{path}: {arrangement} {book} {chapter} is in the witness and "
                        f"in no {pair[0]}/{pair[1]} row; rule on it, with "
                        f"{NOT_RECORDED} if nothing is established"
                    )


@lru_cache(maxsize=1)
def _rows() -> tuple[Correspondence, ...]:
    found = sorted(CONCORDANCE_ROOT.glob(CONCORDANCE_GLOB))
    if len(found) != 1:
        raise ConcordanceUnavailable(
            f"expected one deuterocanon concordance under {CONCORDANCE_ROOT}, "
            f"found {len(found)}"
        )
    path = found[0]
    entries: list[Correspondence] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for line, row in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            where = f"{path}:{line}"
            pair = (_arrangement(row, "left", where), _arrangement(row, "right", where))
            if pair[0] == pair[1]:
                raise ConcordanceUnavailable(f"{where}: a row from {pair[0]} to itself")
            entry = Correspondence(
                pair,
                _side(row, "left", pair[0], where),
                _side(row, "right", pair[1], where),
                row["relation"].strip(),
                row["note"].strip(),
            )
            _check_shape(entry, where)
            if entry.relation == NOT_RECORDED and not entry.note:
                raise ConcordanceUnavailable(
                    f"{where}: {NOT_RECORDED} must say what was looked at and not found"
                )
            _check_opening(entry.left, row["left_opening"], where, "left")
            _check_opening(
                None if entry.relation == NOT_RECORDED else entry.right,
                row["right_opening"], where, "right",
            )
            entries.append(entry)
    _check_coverage(path, entries)
    return tuple(entries)


@lru_cache(maxsize=None)
def _index(source: str, target: str) -> dict[tuple[str, int, int], Correspondence]:
    """Every verse of `source` the concordance rules on against `target`.

    Rows are read in whichever direction is asked for. A row says the same thing
    from either side once its relation is mirrored, so recording it twice would
    only give the two copies a chance to disagree.
    """
    table: dict[tuple[str, int, int], Correspondence] = {}
    for entry in _rows():
        if entry.pair == (target, source):
            entry = entry.flipped()
        if entry.pair != (source, target) or entry.left is None:
            continue
        for verse in range(entry.left.first, entry.left.last + 1):
            table[(entry.left.book, entry.left.chapter, verse)] = entry
    return table


def convert_verse(
    book: str, chapter: int, verse: int, source: str, target: str
) -> tuple[Locus | None, str]:
    """Where one verse of `source` stands in `target`, or why it does not.

    Returns the locus and an empty problem, or `None` and the reason. The reason
    is the point: an addition one arrangement does not carry, a verse the other
    divides, and a book nothing has been established for want three different
    repairs and must not read alike.
    """
    if source == target:
        return Locus(target, book, chapter, verse, verse), ""
    if source not in WITNESSES or target not in WITNESSES:
        raise NumberingError(f"no arrangement named {source!r} or {target!r}")
    entry = _index(source, target).get((book, chapter, verse))
    if entry is None:
        return None, (
            f"no correspondence is recorded between {source} and {target} for "
            f"{book} {chapter}:{verse}"
        )
    if entry.relation == NOT_RECORDED:
        return None, f"{entry.left} is not mapped onto {target}: {entry.note}"
    if entry.relation == ABSENT_RIGHT:
        return None, f"{entry.left} has no counterpart in {target}: {entry.note}"
    if entry.relation == ABSENT_LEFT:
        return None, (
            f"{book} {chapter}:{verse} is a verse {target} carries and {source} does "
            f"not: {entry.note}"
        )
    right = entry.right
    assert right is not None  # every other relation has one, by _check_shape
    if entry.relation == SPLIT_RIGHT:
        return None, (
            f"{entry.left} is {right} in {target}, which is more than one verse, and a "
            f"reference to one verse cannot select it without cutting it"
        )
    if entry.relation == MERGED_RIGHT:
        return right, (
            f"{book} {chapter}:{verse} is part of {right}, which carries the whole of "
            f"{entry.left}; the text returned is a superset of the verse cited"
        )
    return Locus(
        target, right.book, right.chapter,
        right.first + (verse - entry.left.first),
        right.first + (verse - entry.left.first),
    ), ""


def convert_through(
    book: str, chapter: int, verse: int, hops: tuple[str, ...]
) -> tuple[Locus | None, str]:
    """Convert along a chain of arrangements, refusing at the first inexact hop.

    Composition is only safe where every hop is one-to-one across the verse in
    question, so a merged or split hop stops the chain rather than being carried
    through it. The World English Catholic Edition is two hops from the Vulgate
    and this is the only way to reach it without a second table saying the same
    thing twice.
    """
    where: Locus | None = Locus(hops[0], book, chapter, verse, verse)
    problem = ""
    for source, target in zip(hops, hops[1:]):
        assert where is not None
        found, problem = convert_verse(where.book, where.chapter, where.first, source, target)
        if found is None:
            return None, problem
        if problem:
            # A merged hop gives a containing verse, not the verse; converting
            # onward from it would claim a precision the row denies.
            return (found, problem) if target == hops[-1] else (None, problem)
        where = found
    return where, problem


# Which arrangement each indexed edition prints these three books in, and where
# its verse-alias table lives. Only the editions that are not in the Vulgate
# arrangement are here: an edition that prints the numbers a citation uses needs
# no aliases, and listing it would invite a table of empty rows.
#
# The Catholic Public Domain Version is deliberately absent. It declares Vulgate
# numbering and keeps it everywhere except Esther, which it prints in the
# Septuagint's narrative order and in fifteen chapters of its own division: its
# 1:1 is the Vulgate's 11:2, its 3:1 is the Vulgate's 1:1, and its chapter 5
# holds thirteen verses where the Vulgate's chapter 3 holds fifteen. That is a
# re-chaptering of the book and not a renumbering of it, one edition witnesses
# it, and no calendar cites it; its Esther stays refused wholesale by the rows
# its own artifact already carries.
ALIASED: dict[str, tuple[str, str]] = {
    "king-james-version": (
        "greek", "church-of-england/king-james-version/editions/ebible-engkjv/artifacts"
    ),
    "revised-version-1895": (
        "greek", "convocation-of-canterbury/revised-version/editions/ebible-eng-rv/artifacts"
    ),
    "world-english-bible-catholic": (
        "world-english-catholic",
        "ebible-org/world-english-bible/editions/catholic-eng-web-c/artifacts",
    ),
}

# The books a citation reaches these three through, in the arrangement the
# calendars cite. Alias rows are derived for every verse of them.
CITED_IN = "vulgate"
CITED_BOOKS = ("Esth", "Ecclus", "Dan")

# The vocabulary the editions' verse-alias tables already use. `renumbered` is a
# locus this edition carries elsewhere; `merged-verse` is a locus whose text it
# carries inside a longer verse, so the text returned is a superset;
# `not-in-this-edition` is a locus it does not carry at all; and
# `numbering-not-recorded` is a locus whose counterpart is not established, or
# is established but is more than one verse and so cannot be addressed.
RENUMBERED = "renumbered"
MERGED_VERSE = "merged-verse"
NOT_CARRIED = "not-in-this-edition"
UNRECORDED = "numbering-not-recorded"

ALIAS_COLUMNS = ("cited_locus", "resolves_to", "kind", "note")

# Loci where a tracked edition prints something other than what its arrangement's
# witness prints at the same number. These are textual defects, not numbering
# ones, and they are here because a derived alias would otherwise send a citation
# to a number the edition fills with the wrong words — the same silent
# mis-resolution the concordance exists to stop, arrived at from the other side.
#
# Each is declared with both openings and both are checked against the tracked
# text on load, so a departure cannot be asserted and cannot survive the defect
# being corrected.
TEXT_DEPARTURES: dict[str, tuple[tuple[str, int, int, str, str, str], ...]] = {
    "king-james-version": (
        (
            "SgThree", 1, 55, "o sea and rivers", "o ye mountains",
            "the King James Apocrypha repeats the mountains of verse 53 here, where the "
            "Revised Version and the Latin both have the seas and rivers, so its 55 and "
            "56 are one line out of step with the rest of the Greek witness",
        ),
        (
            "SgThree", 1, 56, "o ye fountains", "o ye seas and rivers",
            "see verse 55: this edition's fountains are unprinted and its 56 carries the "
            "seas and rivers instead",
        ),
    ),
}


def _hops(arrangement: str) -> tuple[str, ...]:
    """The chain from the numbering a citation uses to this arrangement."""
    if arrangement == "greek":
        return (CITED_IN, "greek")
    return (CITED_IN, "greek", arrangement)


@lru_cache(maxsize=None)
def _edition_text(edition: str) -> dict[tuple[str, int, int], str]:
    """Every verse one indexed edition prints, for the books in scope."""
    _, where = ALIASED[edition]
    verses: dict[tuple[str, int, int], str] = {}
    for path in sorted((WORKS / where).glob("verse-text-*/*.tsv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for line in csv.DictReader(handle, delimiter="\t"):
                if line["book"] in BOOKS:
                    verses[(line["book"], int(line["chapter"]), int(line["verse"]))] = (
                        line["text"]
                    )
    return verses


@lru_cache(maxsize=None)
def _departures(edition: str) -> dict[tuple[str, int, int], str]:
    """The declared textual departures, checked against the tracked text."""
    arrangement, _ = ALIASED[edition]
    printed = _edition_text(edition)
    witness = _printed(arrangement)
    found: dict[tuple[str, int, int], str] = {}
    for book, chapter, verse, expected, actual, reason in TEXT_DEPARTURES.get(edition, ()):
        here = (book, chapter, verse)
        for label, text, opening in (
            ("the witness", witness.get(here), expected),
            (edition, printed.get(here), actual),
        ):
            if text is None or not normalize(text).startswith(opening):
                raise ConcordanceUnavailable(
                    f"{edition} declares a departure at {book} {chapter}:{verse} where "
                    f"{label} is said to open {opening!r}; the tracked text does not"
                )
        if expected == actual:
            raise ConcordanceUnavailable(
                f"{edition} declares a departure at {book} {chapter}:{verse} that is "
                f"not one: both sides open {expected!r}"
            )
        found[here] = reason
    return found


def derive_aliases(edition: str) -> list[dict[str, str]]:
    """The verse-alias rows this edition's numbering of these books requires.

    Derived from the concordance and from the verses the Vulgate witness prints,
    so the ceilings and the correspondences have one source. A locus this
    edition prints at the number cited gets no row at all: a table that restated
    the identity would be a second copy of the concordance, free to drift.
    """
    arrangement, _ = ALIASED[edition]
    hops = _hops(arrangement)
    printed = _edition_text(edition)
    departures = _departures(edition)
    rows: list[dict[str, str]] = []
    for book, chapter, verse in sorted(
        locus for locus in _printed(CITED_IN) if locus[0] in CITED_BOOKS
    ):
        found, problem = convert_through(book, chapter, verse, hops)
        here = None if found is None else (found.book, found.chapter, found.first)
        if here is not None and here in departures:
            kind, target, problem = UNRECORDED, None, departures[here]
        elif here is not None and here not in printed:
            kind, target = NOT_CARRIED, None
            problem = (
                f"{CITED_IN} {book} {chapter}:{verse} is {found}, which this edition "
                f"does not print"
            )
        elif found is not None and not problem:
            if here == (book, chapter, verse):
                continue
            kind, target = RENUMBERED, found
        elif found is not None:
            kind, target = MERGED_VERSE, found
        elif "has no counterpart" in problem:
            kind, target = NOT_CARRIED, None
        else:
            kind, target = UNRECORDED, None
        rows.append(
            {
                "cited_locus": f"{book}.{chapter}.{verse}",
                "resolves_to": ""
                if target is None
                else f"{target.book}.{target.chapter}.{target.first}",
                "kind": kind,
                "note": problem or _renumbering_note(book, chapter, verse, target),
            }
        )
    return rows


def _renumbering_note(book: str, chapter: int, verse: int, target: Locus | None) -> str:
    return (
        f"{CITED_IN} {book} {chapter}:{verse} stands in this edition at "
        f"{target.book} {target.chapter}:{target.first}"
    )


def _main(argv: list[str]) -> int:
    import sys as _sys

    if len(argv) != 1 or argv[0] not in ALIASED:
        print(f"usage: _deuterocanon.py {{{','.join(sorted(ALIASED))}}}", file=_sys.stderr)
        return 2
    print("\t".join(ALIAS_COLUMNS))
    for row in derive_aliases(argv[0]):
        print("\t".join(row[column] for column in ALIAS_COLUMNS))
    return 0


if __name__ == "__main__":
    import sys as _sys

    raise SystemExit(_main(_sys.argv[1:]))
