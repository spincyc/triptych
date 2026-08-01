"""Where a tracked edition's printed psalter departs from the numbering it declares.

An edition declares a numbering; the psalter it prints is a witness of that
numbering and not the numbering itself. The two are not the same thing, and
`guidance/versification.md` §1.1 names the confusion between them as the root of
everything in that document. This module holds the difference for the psalter:
per edition, where its printed verse numbers stop describing the system it cites
in, and what a citation written in that system therefore resolves to here.

The failure it exists to stop is the one the library is built around. The
tracked Clementine prints Psalm 115 as verses 1-10 where the numbering it
declares runs 10-19, so `Bible.verse('Ps', 115, 10)` returned *in atriis domus
Domini* — the last verse of the psalm under the first verse's number, real Latin
at a correct-looking reference, with nothing counting it a failure. Its verse
alias table was a two-column header and nothing else, and nothing distinguished
"this edition has no departures" from "nobody recorded any".

**Which numbering is the departing one is a per-psalm question, and it is not
always this edition's.** The concordance `_psalms` reads is a verse-level
alignment of the Vulgate against the Hebrew, and its equal-length rule means its
Vulgate column can only be the printing that aligns one to one with the Hebrew —
which is the Challoner Douay-Rheims it was compiled from. Measured against
Copenhagen's published `vul` scheme on 2026-07-31, the tracked Clementine's
psalter departs from the Vulgate at exactly two psalms, 115 and 147, and the
concordance's column is the departing witness at the other seven:

    psalm   concordance   Clementine   published vul
    15      1-11          1-10         10
    19      1-9           1-10         10
    28      1-10          1-11         11
    42      1-6           1-5           5
    115     10-19         1-10         19
    125     1-7           1-6           6
    135     1-27          1-26         26
    147     12-20         1-9          20
    150     1-5           1-6           6

Both traditions are cited. The 1962 Missal's communion *Notas mihi fecisti vias
vitae* is cited `Psalm 15:11`, a number only the eleven-verse division has; the
postconciliar communion *Sedebit Dominus Rex in aeternum* is cited
`Psalm 28:10-11`, a number only the eleven-verse division of *that* psalm has.
So a table keyed on the citation is the only thing that can serve both, which is
what this is.

That asymmetry decides what each declaration derives, and the rule is: **write a
row where the edition would otherwise answer with the wrong text; leave
resolution alone, and record the divergence, where it answers with the head of
the right text.** A refusal at Psalm 28:10 or Psalm 150:5 would take away text
these editions carry at the numbers the citing books actually print, and the
published scheme sides with these editions at every one of those loci. A
refusal at the Catholic Public Domain Version's Psalm 92:1 gives back a citation
that today returns the psalm's Latin title.

Six relations are declared, and both ends of every one are read from tracked
text rather than typed. `identity` and `renumbered` are equal-length runs at the
same or different numbers; `merged` is a printed verse carrying the whole of a
cited run and possibly more; `split` is one cited verse printed as several;
`displaced` is a cited verse no single printed verse carries whole; `unnumbered`
is a printed verse the cited numbering does not number at all.

Nothing here is trusted on its word. The rows of a declared psalm must tile the
concordance's extent and the edition's printed extent exactly once each, every
declaration records the opening words of both sides and they are checked against
the two texts on load, and `obligations` derives the psalms that must be
declared from the two extents. A psalm that diverges and is not declared fails;
a psalm that is declared and does not diverge fails too, so the record cleans
itself when a text is corrected.
"""

from __future__ import annotations

import csv
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import _psalms
from _deuterocanon import (
    ALIAS_COLUMNS,
    MERGED_VERSE,
    OPENING_WORDS,
    RENUMBERED,
    UNRECORDED,
    normalize,
)

ROOT = Path(__file__).resolve().parents[1]
WORKS = ROOT / "src" / "sources" / "works"

PSALMS_TOKEN = "Ps"

# The edition the concordance was compiled from and against. A cited locus is a
# locus of this printing, so a declaration's cited opening is checked here.
WITNESS = (
    "english-college-of-douay/douay-rheims-bible/editions"
    "/challoner-gutenberg-1581/artifacts"
)
WITNESS_EDITION = "douay-rheims"

# Every indexed edition whose printed psalter this module rules on: the
# numbering it declares, and the tracked artifact directory its verse text and
# alias table live in. An edition is here whether or not it departs, because the
# check derives the obligation from the text — listing one that turns out to
# agree costs an empty tuple and buys the assurance that somebody looked.
#
# `tools/index-bible` remains the register of record for what an edition
# declares. The numbering is restated here so that this module can be run and
# tested on its own, and every entry point compares the two rather than trusting
# either: a disagreement fails loudly instead of deriving the wrong table.
EDITIONS: dict[str, tuple[str, str]] = {
    "douay-rheims": ("vulgate", WITNESS),
    "douay-rheims-american-1899": (
        "vulgate",
        "english-college-of-douay/douay-rheims-bible/editions"
        "/american-1899-ebible/artifacts",
    ),
    "clementine-vulgate": (
        "vulgate",
        "catholic-church/vulgata-clementina/editions/ebible-latvuc/artifacts",
    ),
    "catholic-public-domain-version": (
        "vulgate",
        "ronald-conte/catholic-public-domain-version/editions"
        "/sacredbible-original-web-2026-07-31/artifacts",
    ),
    "world-english-bible-catholic": (
        "hebrew",
        "ebible-org/world-english-bible/editions/catholic-eng-web-c/artifacts",
    ),
    "king-james-version": (
        "hebrew",
        "church-of-england/king-james-version/editions/ebible-engkjv/artifacts",
    ),
    "revised-version-1895": (
        "hebrew",
        "convocation-of-canterbury/revised-version/editions/ebible-eng-rv/artifacts",
    ),
}

IDENTITY = "identity"
RENUMBER = "renumbered"
MERGED = "merged"
SPLIT = "split"
DISPLACED = "displaced"
UNNUMBERED = "unnumbered"
RELATIONS = (IDENTITY, RENUMBER, MERGED, SPLIT, DISPLACED, UNNUMBERED)

# The relations that say nothing new when they are all a psalm carries. A psalm
# declared with these alone would be asserting a departure it does not have.
AGREEING = (IDENTITY,)


class PsalterError(RuntimeError):
    """A declared departure does not describe the tracked text, or one is missing."""


class Departure(NamedTuple):
    """One run of a psalm, as the citation numbers it and as this edition prints it.

    `cited` is a verse range in the numbering the edition declares, read through
    the tracked concordance; `printed` is a verse range of this edition's own
    text. Either may be absent, and which one may be absent is what the relation
    says. The two openings are the first seven words of the first verse of each
    side, normalized, and both are checked against the text they describe — the
    cited one against the concordance's witness edition, the printed one against
    this edition. They are the reason a declaration cannot outlive the text.
    """

    psalm: int
    relation: str
    cited: tuple[int, int] | None
    printed: tuple[int, int] | None
    cited_opening: str
    printed_opening: str
    note: str


# The declared departures, per edition. Nothing is derived from a count here:
# each run was established by reading the two texts side by side, and the
# openings are what make that reading checkable afterwards.
DEPARTURES: dict[str, tuple[Departure, ...]] = {
    # The edition the concordance is compiled from. It cannot depart from itself,
    # and the check proves the concordance still describes it.
    "douay-rheims": (),
    "douay-rheims-american-1899": (
        Departure(
            115, RENUMBER, (10, 19), (1, 10),
            "i have believed therefore have i spoken",
            "i have believed therefore have i spoken",
            "the Vulgate keeps the numbering Psalm 115 had before the Hebrew split "
            "and opens it at verse 10; this edition restarts it at 1, so every "
            "verse of the psalm answers to a different number here",
        ),
        Departure(
            147, RENUMBER, (12, 20), (1, 9),
            "alleluia praise the lord o jerusalem praise",
            "praise the lord o jerusalem praise thy",
            "as at Psalm 115: the Vulgate opens Psalm 147 at verse 12 and this "
            "edition restarts it at 1",
        ),
    ),
    "clementine-vulgate": (
        Departure(
            15, IDENTITY, (1, 9), (1, 9),
            "the inscription of a title to david",
            "tituli inscriptio ipsi david conserva me domine", "",
        ),
        Departure(
            15, MERGED, (10, 11), (10, 10),
            "because thou wilt not leave my soul",
            "quoniam non derelinques animam meam in inferno",
            "the Vulgate carries *notas mihi fecisti vias vitae* at the end of "
            "verse 10 where the concordance's witness gives it a verse 11 of its "
            "own; the 1962 Missal cites that communion as Psalm 15:11, so the "
            "number is cited and has to resolve somewhere",
        ),
        Departure(
            19, IDENTITY, (1, 8), (1, 8),
            "unto the end a psalm for david",
            "in finem psalmus david", "",
        ),
        Departure(
            19, SPLIT, (9, 9), (9, 10),
            "they are bound and have fallen but",
            "ipsi obligati sunt et ceciderunt nos autem",
            "this edition gives *Domine salvum fac regem* a verse of its own, as "
            "the published Vulgate scheme does and the concordance's witness does "
            "not",
        ),
        Departure(
            42, IDENTITY, (1, 3), (1, 3),
            "a psalm for david judge me o",
            "psalmus david judica me deus et discerne", "",
        ),
        Departure(
            42, MERGED, (4, 4), (4, 4),
            "and i will go in to the",
            "et introibo ad altare dei ad deum",
            "the verse boundary moves inside this psalm: this edition's verse 4 "
            "carries *confitebor tibi in cithara* as well, which the concordance's "
            "witness numbers 5",
        ),
        Departure(
            42, DISPLACED, (5, 5), None,
            "to thee o god my god i", "",
            "the cited verse is divided between this edition's 4 and 5 and no "
            "printed verse carries it whole, so there is no number here to send a "
            "citation of it to",
        ),
        Departure(
            42, MERGED, (6, 6), (5, 5),
            "hope in god for i will still",
            "quare tristis es anima mea et quare",
            "this edition's verse 5 opens with the *quare tristis* the "
            "concordance's witness numbers 5 and closes with the whole of its 6",
        ),
        Departure(
            115, RENUMBER, (10, 19), (1, 10),
            "i have believed therefore have i spoken",
            "alleluja credidi propter quod locutus sum ego",
            "the Vulgate keeps the numbering Psalm 115 had before the Hebrew split "
            "and opens it at verse 10; this edition restarts it at 1, so every "
            "verse of the psalm answers to a different number here",
        ),
        Departure(
            125, IDENTITY, (1, 5), (1, 5),
            "when the lord brought back the captivity",
            "canticum graduum in convertendo dominus captivitatem sion", "",
        ),
        Departure(
            125, MERGED, (6, 7), (6, 6),
            "going they went and wept casting their",
            "euntes ibant et flebant mittentes semina sua",
            "the sowing and the sheaves are one verse here and two in the "
            "concordance's witness",
        ),
        Departure(
            135, IDENTITY, (1, 25), (1, 25),
            "alleluia praise the lord for he is",
            "alleluja confitemini domino quoniam bonus quoniam in", "",
        ),
        Departure(
            135, MERGED, (26, 27), (26, 26),
            "give glory to the god of heaven",
            "confitemini deo caeli quoniam in aeternum misericordia",
            "the last two *confitemini* are one verse here and two in the "
            "concordance's witness",
        ),
        Departure(
            147, RENUMBER, (12, 20), (1, 9),
            "alleluia praise the lord o jerusalem praise",
            "alleluja lauda jerusalem dominum lauda deum tuum",
            "as at Psalm 115: the Vulgate opens Psalm 147 at verse 12 and this "
            "edition restarts it at 1",
        ),
    ),
    "catholic-public-domain-version": (
        Departure(
            13, IDENTITY, (1, 2), (1, 2),
            "unto the end a psalm for david",
            "unto the end a psalm of david", "",
        ),
        Departure(
            13, SPLIT, (3, 3), (3, 6),
            "they are all gone aside they are",
            "they have all gone astray together they",
            "the Old Latin plus that Romans 3 quotes stands inside one verse in "
            "the concordance's witness and is four verses here",
        ),
        Departure(
            13, RENUMBER, (4, 7), (7, 10),
            "shall not all they know that work",
            "will they never learn all those who",
            "the four verses after the plus stand three numbers later here",
        ),
        Departure(
            19, IDENTITY, (1, 8), (1, 8),
            "unto the end a psalm for david",
            "unto the end a psalm of david", "",
        ),
        Departure(
            19, SPLIT, (9, 9), (9, 10),
            "they are bound and have fallen but",
            "they have been bound and they have",
            "this edition gives *O Lord, save the king* a verse of its own, as the "
            "published Vulgate scheme does and the concordance's witness does not",
        ),
        Departure(
            42, IDENTITY, (1, 3), (1, 3),
            "a psalm for david judge me o",
            "a psalm of david judge me o", "",
        ),
        Departure(
            42, MERGED, (4, 4), (4, 4),
            "and i will go in to the",
            "and i will enter up to the",
            "the verse boundary moves inside this psalm: this edition's verse 4 "
            "carries the confession on the stringed instrument as well, which the "
            "concordance's witness numbers 5",
        ),
        Departure(
            42, DISPLACED, (5, 5), None,
            "to thee o god my god i", "",
            "the cited verse is divided between this edition's 4 and 5 and no "
            "printed verse carries it whole, so there is no number here to send a "
            "citation of it to",
        ),
        Departure(
            42, MERGED, (6, 6), (5, 5),
            "hope in god for i will still",
            "why are you sad my soul and",
            "this edition's verse 5 opens with the *why are you sad* the "
            "concordance's witness numbers 5 and closes with the whole of its 6",
        ),
        Departure(
            92, UNNUMBERED, None, (1, 1),
            "", "the praise of a canticle of david",
            "this edition numbers the psalm's Latin title as a verse of its own; "
            "the concordance's witness prints no title here at all, so the "
            "citation numbering has no number for it",
        ),
        Departure(
            92, SPLIT, (1, 1), (2, 3),
            "the lord hath reigned he is clothed",
            "the lord has reigned he has been",
            "the reigning, the strength and the founding of the world are one "
            "verse in the concordance's witness and two here — and because the "
            "title took verse 1, a citation of 92:1 lands on the title rather "
            "than on the head of the verse it means",
        ),
        Departure(
            92, RENUMBER, (2, 5), (4, 7),
            "my throne is prepared from of old",
            "my throne is prepared from of old",
            "the rest of the psalm stands two numbers later here",
        ),
        Departure(
            115, RENUMBER, (10, 19), (1, 10),
            "i have believed therefore have i spoken",
            "alleluia i had confidence because of what",
            "the Vulgate keeps the numbering Psalm 115 had before the Hebrew split "
            "and opens it at verse 10; this edition restarts it at 1, so every "
            "verse of the psalm answers to a different number here",
        ),
        Departure(
            147, RENUMBER, (12, 20), (1, 9),
            "alleluia praise the lord o jerusalem praise",
            "alleluia praise the lord o jerusalem praise",
            "as at Psalm 115: the Vulgate opens Psalm 147 at verse 12 and this "
            "edition restarts it at 1",
        ),
    ),
    # The three Hebrew-numbered editions leave a psalm's inscription unnumbered
    # and are otherwise in the numbering they declare; the check derives that
    # rather than taking it on trust.
    "world-english-bible-catholic": (),
    "king-james-version": (),
    "revised-version-1895": (),
}


@lru_cache(maxsize=None)
def printed(artifacts: str) -> dict[int, dict[int, str]]:
    """Every psalm verse one edition prints, keyed by psalm and verse."""
    verses: dict[int, dict[int, str]] = {}
    for path in sorted((WORKS / artifacts).glob("verse-text-*/*.tsv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                if row["book"] != PSALMS_TOKEN:
                    continue
                verses.setdefault(int(row["chapter"]), {})[int(row["verse"])] = row["text"]
    if not verses:
        raise PsalterError(f"{artifacts}: the tracked verse text carries no psalter")
    return verses


def printed_extent(artifacts: str, psalm: int) -> tuple[int, int] | None:
    """The first and last verse number this edition prints in one psalm."""
    verses = printed(artifacts).get(psalm)
    if not verses:
        return None
    return min(verses), max(verses)


def system_extent(psalm: int) -> tuple[int, int]:
    """The verse numbers the Vulgate psalm numbering has, from both tracked statements."""
    low, high = _psalms.psalm_extent(psalm, "vulgate")
    recorded = _witness_aliases().get(psalm, set())
    if recorded:
        low, high = min(low, *recorded), max(high, *recorded)
    return low, high


@lru_cache(maxsize=1)
def _witness_aliases() -> dict[int, set[int]]:
    """The psalm verse numbers the witness edition records without printing them.

    The concordance cannot be the whole statement of the Vulgate psalm numbering,
    and the reason is structural rather than an oversight. Its rows must be runs
    of equal length in both systems, so its Vulgate column can only be the
    printing that aligns one to one with the Hebrew — and where the Vulgate
    divides a verse the Hebrew joins, that column has to follow the Hebrew and
    the number goes unrecorded. Psalm 28:11 and Psalm 150:6 are exactly those
    numbers: both are cited, both are in the published Vulgate scheme, and the
    witness edition's own alias table already records where it carries each.

    So the numbering is stated by two tracked artifacts together, and this reads
    the second. Nothing here is typed: the loci come out of the witness's
    `verse-aliases.tsv`, which the projection validates like any other.
    """
    found: dict[int, set[int]] = {}
    tables = sorted((WORKS / WITNESS).glob("verse-aliases-*/verse-aliases.tsv"))
    if len(tables) != 1:
        raise PsalterError(
            f"expected one verse-alias table under {WORKS / WITNESS}, found {len(tables)}"
        )
    with tables[0].open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            parts = (row.get("cited_locus") or "").split(".")
            if len(parts) == 3 and parts[0] == PSALMS_TOKEN:
                found.setdefault(int(parts[1]), set()).add(int(parts[2]))
    return found


def declared_extent(psalm: int, numbering: str) -> tuple[tuple[int, int], ...]:
    """The extents a psalm may print under a declared numbering, in order.

    A Vulgate-numbered edition has exactly one answer, read from the concordance
    and widened by whatever the witness edition's alias table records beyond it.
    A Hebrew-numbered one has two, because whether the inscription takes a verse
    number of its own is a convention of the printing rather than of the system,
    and this module is not told which the edition follows. Both are returned and
    either satisfies the check; a psalm the concordance flags as dividing its
    body differently returns nothing, because no English extent is derivable for
    it and `_psalms.english_verse` refuses it for the same reason.
    """
    if numbering == "vulgate":
        return (system_extent(psalm),)
    if numbering != "hebrew":
        raise PsalterError(
            f"no psalter extent for numbering {numbering!r}; the concordance "
            f"carries vulgate and hebrew"
        )
    hebrew = _psalms.psalm_extent(psalm, "hebrew")
    last, _ = _psalms.english_verse(psalm, hebrew[1])
    if last is None:
        # One of the sixteen the concordance flags: the two conventions divide
        # the body of the psalm differently and it records no verse-for-verse
        # correspondence, so no English extent is derivable and this check has
        # nothing to say. `undecided` reports these rather than passing over
        # them, because an unchecked psalm and a checked one must not read alike.
        return ()
    for verse in range(hebrew[0], hebrew[1] + 1):
        # The head of the psalm may be the inscription, which an English-
        # convention printing leaves unnumbered; the first numbered verse is
        # whichever comes after it.
        found, _ = _psalms.english_verse(psalm, verse)
        if found is not None:
            return (hebrew, (found, last))
    return (hebrew,)


def obligations(artifacts: str, numbering: str) -> dict[int, tuple]:
    """The psalms whose printed extent contradicts the numbering this edition declares.

    This is the check that was missing. An edition may print a psalter that
    disagrees with its declared numbering — that is an ordinary fact about a
    printing — but it may not do so silently, because a citation resolved against
    such a psalm returns real text under a correct-looking reference. Derived
    from the concordance and the tracked verse text, so neither end is a number
    anyone typed.
    """
    found: dict[int, tuple] = {}
    for psalm in range(1, _psalms.LAST_PSALM + 1):
        here = printed_extent(artifacts, psalm)
        if here is None:
            found[psalm] = (None, declared_extent(psalm, numbering))
            continue
        allowed = declared_extent(psalm, numbering)
        if allowed and here not in allowed:
            found[psalm] = (here, allowed)
    return found


def undecided(numbering: str) -> list[int]:
    """Psalms no extent can be derived for, so the check cannot rule on them.

    Only Hebrew-numbered editions have any: the sixteen the concordance flags as
    dividing their body differently from the English convention. They are
    reported rather than passed over silently, because an unchecked psalm and a
    checked one must not read alike.
    """
    if numbering != "hebrew":
        return []
    return [
        psalm
        for psalm in range(1, _psalms.LAST_PSALM + 1)
        if not declared_extent(psalm, numbering)
    ]


def _check_run(where: str, run: tuple[int, int] | None, side: str) -> None:
    if run is not None and run[1] < run[0]:
        raise PsalterError(f"{where}: the {side} run {run[0]}-{run[1]} ends before it begins")


def _check_opening(
    where: str, verses: dict[int, str], run: tuple[int, int] | None, opening: str, side: str
) -> None:
    """The recorded opening must be what the text prints at the head of the run."""
    opening = opening.strip()
    if run is None:
        if opening:
            raise PsalterError(f"{where}: a {side} opening with no {side} run")
        return
    if not opening:
        raise PsalterError(f"{where}: the {side} run {run[0]}-{run[1]} records no opening words")
    text = verses.get(run[0])
    if text is None:
        raise PsalterError(f"{where}: nothing is printed at the {side} verse {run[0]}")
    if not normalize(text).startswith(opening):
        raise PsalterError(
            f"{where}: the {side} run is recorded as opening {opening!r}, but the text "
            f"prints {' '.join(normalize(text).split()[:OPENING_WORDS])!r}"
        )


def _check_shape(where: str, entry: Departure) -> None:
    if entry.relation not in RELATIONS:
        raise PsalterError(f"{where}: unknown relation {entry.relation!r}")
    if entry.relation == DISPLACED and (entry.cited is None or entry.printed is not None):
        raise PsalterError(
            f"{where}: {DISPLACED} means no printed verse carries the cited one whole, "
            f"so it needs a cited run and no printed one"
        )
    if entry.relation == UNNUMBERED and (entry.printed is None or entry.cited is not None):
        raise PsalterError(
            f"{where}: {UNNUMBERED} means the citation numbering has no number for a "
            f"printed verse, so it needs a printed run and no cited one"
        )
    if entry.relation not in (DISPLACED, UNNUMBERED) and (
        entry.cited is None or entry.printed is None
    ):
        raise PsalterError(f"{where}: {entry.relation} needs a run on both sides")
    if entry.cited is None or entry.printed is None:
        return
    cited = entry.cited[1] - entry.cited[0]
    written = entry.printed[1] - entry.printed[0]
    if entry.relation in (IDENTITY, RENUMBER) and cited != written:
        raise PsalterError(
            f"{where}: {entry.relation} needs runs of equal length, and this is "
            f"{cited + 1} against {written + 1}"
        )
    if entry.relation == IDENTITY and entry.cited != entry.printed:
        raise PsalterError(
            f"{where}: {IDENTITY} means the same numbers, and this is "
            f"{entry.cited} against {entry.printed}"
        )
    if entry.relation == RENUMBER and entry.cited == entry.printed:
        raise PsalterError(f"{where}: {RENUMBER} at the same numbers is {IDENTITY}")
    if entry.relation == MERGED and written != 0:
        raise PsalterError(
            f"{where}: {MERGED} means one printed verse carrying the cited run, and "
            f"this names {written + 1}"
        )
    if entry.relation == SPLIT and not (cited == 0 and written > 0):
        raise PsalterError(
            f"{where}: {SPLIT} means one cited verse printed as several, and this is "
            f"{cited + 1} against {written + 1}"
        )


def _check_coverage(where: str, psalm: int, artifacts: str, entries: list[Departure]) -> None:
    """The rows of a psalm must tile both extents exactly once.

    Neither extent is declared: the cited one comes from the concordance and the
    printed one from this edition's tracked verses, so a run that overruns a
    psalm or stops short of it is caught without any ceiling having been typed.
    The psalm concordance's own hand-typed ceilings were wrong for two psalms and
    nothing noticed.
    """
    for side, extent in (
        ("cited", system_extent(psalm)),
        ("printed", printed_extent(artifacts, psalm)),
    ):
        if extent is None:
            raise PsalterError(f"{where}: this edition prints no Psalm {psalm}")
        seen: dict[int, str] = {}
        for entry in entries:
            run = entry.cited if side == "cited" else entry.printed
            if run is None:
                continue
            for verse in range(run[0], run[1] + 1):
                if verse in seen:
                    raise PsalterError(
                        f"{where}: the {side} verse {verse} of Psalm {psalm} is claimed twice"
                    )
                seen[verse] = entry.relation
        wanted = set(range(extent[0], extent[1] + 1))
        missing = sorted(wanted - set(seen))
        if missing:
            raise PsalterError(
                f"{where}: Psalm {psalm} leaves the {side} verses {missing} unaccounted "
                f"for; rule on every verse of a psalm that is declared at all"
            )
        beyond = sorted(set(seen) - wanted)
        if beyond:
            raise PsalterError(
                f"{where}: Psalm {psalm} claims the {side} verse {beyond[0]}, but the "
                f"{side} extent is {extent[0]}-{extent[1]}"
            )


@lru_cache(maxsize=None)
def departures(edition: str, numbering: str) -> tuple[Departure, ...]:
    """This edition's declared departures, validated against the two texts.

    Validation is the whole value of the table. Every declaration is checked for
    shape, for openings against both texts, and for tiling both extents; and the
    obligations derived from the texts are checked against the declarations in
    both directions, so a divergence nobody declared fails and a declaration that
    has stopped being true fails too.
    """
    if edition not in EDITIONS:
        raise PsalterError(f"no psalter departures are declared for {edition!r}")
    declared, artifacts = EDITIONS[edition]
    if numbering != declared:
        raise PsalterError(
            f"{edition} is being projected from {numbering!r} and is declared here as "
            f"{declared!r}; one of the two registers is wrong and neither may be guessed"
        )
    entries = DEPARTURES[edition]
    if edition == WITNESS_EDITION:
        # The witness cannot be checked against itself: its printed psalter and
        # its alias table are the two artifacts that together state the numbering
        # every other edition is measured against. What holds it honest is
        # `_psalms._concordance`, which refuses to load a table that has stopped
        # tiling the psalter, and the alias table's own load-time validation.
        if entries:
            raise PsalterError(
                f"{edition} is the edition the numbering is read from and cannot depart "
                f"from it; its own alias table is where it records what it does not print"
            )
        return entries
    witness = printed(WITNESS)
    here = printed(artifacts)
    by_psalm: dict[int, list[Departure]] = {}
    for index, entry in enumerate(entries):
        where = f"{edition} Psalm {entry.psalm} (declaration {index + 1})"
        _check_shape(where, entry)
        _check_run(where, entry.cited, "cited")
        _check_run(where, entry.printed, "printed")
        _check_opening(where, witness.get(entry.psalm, {}), entry.cited, entry.cited_opening, "cited")
        _check_opening(
            where, here.get(entry.psalm, {}), entry.printed, entry.printed_opening, "printed"
        )
        if entry.relation not in AGREEING and not entry.note.strip():
            raise PsalterError(f"{where}: a {entry.relation} run must say what it found")
        by_psalm.setdefault(entry.psalm, []).append(entry)
    for psalm, rows in sorted(by_psalm.items()):
        _check_coverage(f"{edition}", psalm, artifacts, rows)
        if all(row.relation in AGREEING for row in rows):
            raise PsalterError(
                f"{edition}: Psalm {psalm} is declared and every run agrees; remove the "
                f"declaration rather than leaving one that asserts nothing"
            )
    owed = obligations(artifacts, numbering)
    for psalm in sorted(owed):
        if psalm not in by_psalm:
            here_extent, allowed = owed[psalm]
            wanted = " or ".join(f"{low}-{high}" for low, high in allowed) or "nothing"
            printed_as = "nothing" if here_extent is None else f"{here_extent[0]}-{here_extent[1]}"
            raise PsalterError(
                f"{edition}: Psalm {psalm} prints verses {printed_as} where the {numbering} "
                f"numbering it declares has {wanted}, and no departure is declared for it. "
                f"An edition may print a psalter that departs from the numbering it cites "
                f"in; it may not do so silently, because a citation resolved against such "
                f"a psalm returns real text under a correct-looking reference. Declare it "
                f"in scripts/_psalter.py"
            )
    for psalm in sorted(by_psalm):
        if psalm not in owed:
            raise PsalterError(
                f"{edition}: Psalm {psalm} is declared as departing, and its printed "
                f"extent agrees with the {numbering} numbering; remove the declaration"
            )
    return entries


def derive_aliases(edition: str, numbering: str) -> list[dict[str, str]]:
    """The verse-alias rows this edition's psalter requires, derived not typed.

    One rule decides which declarations produce a row: write one where the
    edition would otherwise answer a citation with the wrong text, and leave
    resolution alone where it answers with the head of the right text.

    A `renumbered` run moves every cited verse, so each gets a row. A `merged`
    run has the printed verse carrying the whole cited run and possibly more, so
    each cited verse resolves there and the note declares the superset — that is
    §8.5's rule that a superset is returned with a note and never as an exact
    match. A `displaced` cited verse has no printed verse carrying it whole and
    refuses. A `split` writes a row only when the printed run does not open at
    the cited verse's own number: then the number addresses something else
    entirely and must refuse, where otherwise it still addresses the head of the
    text cited and taking that away would remove text the edition carries at the
    number the citing books print.
    """
    rows: list[dict[str, str]] = []
    for entry in departures(edition, numbering):
        if entry.relation in (IDENTITY, UNNUMBERED):
            continue
        assert entry.cited is not None  # every other relation has one, by _check_shape
        first, last = entry.cited
        for verse in range(first, last + 1):
            cited_locus = f"{PSALMS_TOKEN}.{entry.psalm}.{verse}"
            if entry.relation == RENUMBER:
                assert entry.printed is not None
                target = entry.printed[0] + (verse - first)
                rows.append({
                    "cited_locus": cited_locus,
                    "resolves_to": f"{PSALMS_TOKEN}.{entry.psalm}.{target}",
                    "kind": RENUMBERED,
                    "note": entry.note,
                })
            elif entry.relation == MERGED:
                assert entry.printed is not None
                rows.append({
                    "cited_locus": cited_locus,
                    "resolves_to": f"{PSALMS_TOKEN}.{entry.psalm}.{entry.printed[0]}",
                    "kind": MERGED_VERSE,
                    "note": entry.note,
                })
            elif entry.relation == DISPLACED:
                rows.append({
                    "cited_locus": cited_locus, "resolves_to": "",
                    "kind": UNRECORDED, "note": entry.note,
                })
            elif entry.relation == SPLIT:
                assert entry.printed is not None
                if entry.printed[0] == verse:
                    continue
                rows.append({
                    "cited_locus": cited_locus, "resolves_to": "",
                    "kind": UNRECORDED, "note": entry.note,
                })
    rows.sort(key=lambda row: tuple(int(part) for part in row["cited_locus"].split(".")[1:]))
    return rows


def split_loci(edition: str, numbering: str) -> list[tuple[str, str]]:
    """The cited loci this edition prints as more than one verse, and why.

    These carry no alias row where the printed run opens at the cited number, so
    without this they would be the one kind of divergence nothing counted — which
    is how the psalter got here. A projection row keeps them listed.
    """
    return [
        (f"{PSALMS_TOKEN}.{entry.psalm}.{entry.cited[0]}", entry.note)
        for entry in departures(edition, numbering)
        if entry.relation == SPLIT and entry.cited is not None
    ]


def edition_of(artifacts_root: Path) -> str | None:
    """The edition whose artifact directory this is, or None if it is not indexed."""
    resolved = artifacts_root.resolve()
    for edition, (_, where) in EDITIONS.items():
        if (WORKS / where).resolve() == resolved:
            return edition
    return None


def _main(argv: list[str]) -> int:
    import sys as _sys

    if len(argv) != 1 or argv[0] not in EDITIONS:
        print(f"usage: _psalter.py {{{','.join(sorted(EDITIONS))}}}", file=_sys.stderr)
        return 2
    print("\t".join(ALIAS_COLUMNS))
    for row in derive_aliases(argv[0], EDITIONS[argv[0]][0]):
        print("\t".join(row[column] for column in ALIAS_COLUMNS))
    return 0


if __name__ == "__main__":
    import sys as _sys

    raise SystemExit(_main(_sys.argv[1:]))
