#!/usr/bin/env python3
"""The Scripture chronology corpus: what this project believes about when.

A PROJECT-GLOBAL FACT, HELD ONCE, for the same reason `_canon` holds the canon.
When a biblical text was written, when the event it narrates happened, when the
words it quotes were spoken, and what later event tradition reads it as
prophesying are four different questions, and every consumer that has ever
wanted one of them has wanted the others too. Held anywhere downstream — in a
proper, in a study, in a page template — each consumer researches its own
answer, and the answers drift. `guidance/scripture-chronology.md` owns the
contract; this is the derivation.

## Where this sits

    citation  ->  versification / projection  ->  CANONICAL LOCUS  ->  here

Chronology attaches to a locus in a NAMED ADDRESSING SYSTEM, spelled exactly as
`_projection` spells one: `Ps.50.3`, `Matt.27.35`. The system is `vulgate`, the
same `_projection.CANONICAL` every tracked projection projects into, because
that is the system this repository's calendars cite in and its canonical edition
witnesses. Nothing here invents a universal verse space, and nothing here
reverses a projection: a caller resolves its citation the way it already does
and asks about the canonical locus it arrives at.

A locus in another system reaches the corpus only through a concordance that
already exists and already refuses when it must — `_psalms` for the psalter's
vulgate/hebrew numbering, `_deuterocanon` for the arrangements of Esther,
Sirach and Daniel. A refusal there is returned as a refusal here. That is the
whole reason `guidance/versification.md` §4 says there is no universal verse
space: for Sirach there are two texts, not two numberings, and a chronology key
that resolved anyway would be the defect of `guidance/the-shape.md` §1 wearing
one more costume.

## What a locus resolves to

Zero or more TYPED TEMPORAL ASSERTIONS, never a scalar date. Ten relations,
and the distinctions between them are the point:

    composition             when the text was written
    final-formation         when a composite text reached its final form
    textual-attestation     when this text is witnessed in a dated edition
    narrated-event          when the event the passage narrates happened
    utterance               when the words the passage quotes were spoken
    historical-setting      the occasion tradition associates with the text
    superscription-setting  the setting the biblical title itself asserts
    retrospective-event     an earlier event the passage explicitly recalls
    prophecy-given          when the oracle was uttered
    prophetic-referent      the later event tradition reads it as prophesying

`prophetic-referent` is not `narrated-event`: Psalm 21 is not a report of the
Passion, and a corpus that could not say so would date David narrating Calvary.
`superscription-setting` is not `composition`: a title is evidence about a
setting and is not proof of a year. `composition` is not `historical-setting`.
And `textual-attestation` is not either one: a dated witness proves that this
text existed by then, never that it was written then.

## What is authored, and what is derived

Authored, under `src/sources/chronology/`:

    profiles.yaml      whose testimony wins, and what this profile refuses
    events.yaml        reusable temporal subjects, dated once
    composition.yaml   composition chronology by textual unit
    bindings.yaml      locus ranges -> event, under a relation
    gaps.yaml          typed status where the corpus knowingly says nothing

Derived, by `tools/scripture-chronology`: the coverage view, run-compressed.
An event is dated ONCE and bound from every locus that needs it, so the four
Gospels cannot acquire four Crucifixion dates — the failure `the-shape.md` §2
predicts of every restatement, and the reason bindings carry no dates at all.

Inheritance runs the same way: a composition unit scoped to a book reaches
every verse in it without a row per verse, and a narrower unit wins over a
wider one. Two units of the same width covering one locus is an error, not a
tie to break, because nothing here may pick.

## Absence

A locus with no assertion still has a status. `research-pending` is the honest
default and the corpus says so rather than reporting coverage it does not have.
`gaps.yaml` records statuses known to be something else — for example, that a
tradition assigns no date. A comprehensive profile may fall through such a gap
to a source-backed claim in another leaf, with textual attestation as the last
resort. `guidance/the-shape.md` §4 still governs the authored evidence: absence
is data, and a gap never becomes a fabricated year merely to close coverage.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = ROOT / "src" / "sources" / "chronology"

# The PREFERRED SHARED SYSTEM, which is not the same as the only one.
#
# `vulgate` is preferred because it is what `_projection.CANONICAL` projects
# into, what both tracked calendars cite in, and what the canonical edition
# witnesses. A fact about a text that CAN be stated here is stated here once,
# and every edition reaches it through machinery that already exists.
#
# But `guidance/versification.md` §4 settles that some traditions carry a
# DIFFERENT TEXT rather than a different numbering, and for those the
# concordance rightly refuses. A refusal there answers one question — may this
# locus be asserted equivalent to that one — and the corpus used to read it as
# an answer to another: may this locus carry chronology at all. It may. The
# Greek Ecclesiasticus is the standing case: 1 355 of its 1 356 loci refuse the
# Vulgate, and the Catholic Encyclopedia dates the Greek translation and the
# Latin version separately and explicitly.
PREFERRED_SYSTEM = "vulgate"

# Kept as the old name so nothing outside this module breaks on the rename.
CANONICAL_SYSTEM = PREFERRED_SYSTEM


def _scripture_systems() -> dict[str, frozenset[str] | None]:
    """Every system a scope may name, and the books each one can address.

    Read from the modules that OWN the names rather than restated here, because
    a fifth list beside theirs is how they stop agreeing — and they already do:
    `_commentary.NUMBERING_SYSTEMS` names `septuagint`, `nova-vulgata` and `nab`,
    for which no concordance exists, and omits `world-english-catholic`, for
    which one does. This function admits only names with machinery behind them.

    A value of None means "every book of the canon". A frozenset means the
    system can address those books and no others, which is the check the
    abandoned scratch patch lacked: it would have accepted `{system: hebrew,
    book: Matt}`, since it tested the system name against a flat set and never
    asked whether that system numbers Matthew at all. `hebrew` is a psalter
    numbering; outside the psalter it names nothing this repository can resolve.
    """
    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import _deuterocanon  # noqa: PLC0415
    import _psalms  # noqa: PLC0415
    import _projection  # noqa: PLC0415

    systems: dict[str, frozenset[str] | None] = {_projection.CANONICAL: None}
    for name in _psalms.SYSTEMS:
        if name != _projection.CANONICAL:
            systems[name] = frozenset({"Ps"})
    for name in _deuterocanon.WITNESSES:
        if name == _projection.CANONICAL:
            continue
        systems[name] = frozenset(_deuterocanon.BOOKS)
    return systems


@lru_cache(maxsize=1)
def scripture_systems() -> dict[str, frozenset[str] | None]:
    return _scripture_systems()

# The documents that carry Scripture loci and must therefore declare the system
# those loci are numbered in. Profiles and events name no verse.
LOCUS_BEARING = ("composition", "bindings", "gaps")

SCHEMAS = {
    "profiles": "triptych-chronology-profiles/v1",
    "events": "triptych-chronology-events/v1",
    "composition": "triptych-chronology-composition/v1",
    "bindings": "triptych-chronology-bindings/v1",
    "gaps": "triptych-chronology-gaps/v1",
}

# --- Vocabulary -------------------------------------------------------------

RELATIONS = (
    "composition",
    "final-formation",
    "textual-attestation",
    "narrated-event",
    "utterance",
    "historical-setting",
    "superscription-setting",
    "retrospective-event",
    "prophecy-given",
    "prophetic-referent",
)

# Textual history is temporal, but it is not an event narrated by the text.
# `composition-only` is the established public status name, so final formation
# joins composition on this side of the status boundary rather than making a
# psalter whose final form is dated look as though every event it mentions had
# been dated.
TEXTUAL_RELATIONS = frozenset(
    {"composition", "final-formation", "textual-attestation"}
)

# A cascade is deliberately one rule, not an open vocabulary a caller may
# interpret. It chooses independently per relation so a traditional
# composition claim cannot suppress a critical narrated-event or
# final-formation claim.
CASCADE_SELECTION = "first-with-answerable-assertion-per-relation"

# The order a query returns assertions in, so a consumer's output is stable and
# a diff of two queries is a diff of the answers rather than of the sorting.
# Composition first because it is the one assertion nearly every locus has.
RELATION_ORDER = {relation: index for index, relation in enumerate(RELATIONS)}

DISPOSITIONS = ("preferred", "alternate", "disputed")

# ANSWERABILITY, which is neither a disposition nor a rank.
#
# A disposition is a position WITHIN the candidate set: `alternate` and
# `disputed` both leave a claim answerable, which is why neither could ever be
# the way to exclude one. Answerability says whether the claim is in that set at
# all. The corpus holds evidence it must not answer with — a figure the citing
# source rejects, a figure printed only for comparison, a source's refusal to
# assign a date — and until this axis existed the only place to put such a
# figure was beside the answers with a note asking not to be believed. Every
# default consumer read the answer, and none read the note.
#
# The two states are closed vocabulary. WHICH state a claim may hold is decided
# by its profile, from the basis of that particular value; see `Policy` and the
# `admissibility` block of `profiles.yaml`.
ANSWERABILITY = ("answerable", "preserved")

# How a date's endpoints are to be read. Separate from `basis` on purpose:
# "approximate" says the date is approximate, not that its source is weak.
#
# `relative` and `duration` are the two that are easy to confuse and must not be.
# `relative` is an OFFSET: B happened N units after A, and naming A is the whole
# of what makes it meaningful. `duration` is a LENGTH: B lasted N units, and it
# is measured from nothing at all. "He judged Israel eighteen years" states no
# point in time and no anchor; reading it as an offset would put the judgeship
# eighteen years after whatever the anchor happened to be. One value that meant
# both would be a date that resolves successfully and wrongly, which is the
# failure `guidance/the-shape.md` §1 names.
PRECISIONS = (
    "day",              # from == to, both carrying month and day
    "month-day",        # month and day known, year not
    "year",             # from == to, exact
    "approximate-year", # from == to, the source's own "about"
    "range",            # the subject spans from..to
    "interval",         # the subject falls somewhere within from..to
    "relative",         # no absolute endpoints; a stated interval FROM another event
    "duration",         # how long the subject itself lasted; measured from nothing
    "boundary",         # one-sided before/after limit, by endpoint or named anchor
)

BOUNDARY_DIRECTIONS = (
    "before", "after", "no-later-than", "no-earlier-than",
)

# A positive chronology guarantee needs a POSITION, not merely any temporal
# fact. A duration says how long something lasted but not when; a month-day
# recurs every year and therefore does not locate it on a chronology. Relative
# and boundary values qualify because their named anchor or one-sided endpoint
# deliberately preserves the source's open horizon rather than inventing a
# closed interval.
POSITIONAL_PRECISIONS = frozenset(
    {"day", "year", "approximate-year", "range", "interval", "relative", "boundary"}
)

# The units a duration may be stated in, largest first, which is also the order
# they render in. No unit smaller than a day, because no inspected source states
# one, and none larger than a year, because a source that says "two centuries"
# says it in years or says something vaguer than a duration.
DURATION_UNITS = ("years", "months", "days")

# `basis` in this repository means the prose that says what GROUNDS a claim,
# and it is required beside every stated date. `tools/source-library` enforces
# the same pairing on a work record — "composed requires composed_basis: say
# what dates the writing, and never the printing" — and
# `src/sources/commentary/work-extents.yaml` states the standard it is held to:
# "A basis that merely restates this repository's own prose is not a basis."
# It is not an enum and it is not a confidence. Whether a claim is derived is
# said by its carrying a `derivation`, not by a second word.

# B.C./A.D. share one axis and are comparable. Anno Mundi is the era traditional
# sources actually print, and it is NOT converted here: an epoch would have to
# be chosen, no ranked source in this repository has been inspected asserting
# one, and a conversion would be a date that resolves successfully and wrongly.
ERAS = ("bc", "ad", "am")
CHRISTIAN_ERAS = ("bc", "ad")

# Every status a locus can carry. The first three are earned from assertions
# that APPLY to a locus, at whatever scope they were authored; the rest are
# authored in gaps.yaml, except `research-pending`, which is what a locus has
# when nothing else applies.
STATUSES = (
    "dated",              # a substantive assertion applies, direct or inherited
    "composition-only",   # only composition/final-formation assertions apply
    "attestation-only",   # only a dated textual witness reaches the locus
    "research-pending",   # not yet researched. The default, and honest.
    "undated-in-tradition",  # ranked sources inspected; tradition dates nothing
    "not-alignable",      # the locus cannot be safely addressed from the asking system
    "textually-distinct", # another tradition carries a different text, not a renumbering
)

# Deliberately NOT reused from `_projection.OVERRIDES` (`absent`, `unrecorded`,
# `displaced`, ...). Those words mean things about where TEXT is. A verse can be
# present, aligned and perfectly addressable and still have no date, and a word
# that meant both would hide one of them.

STATUS_ORDER = {status: index for index, status in enumerate(STATUSES)}

# The statuses an AUTHOR may assert, which is every status that is neither
# earned from an assertion nor the default. Named here rather than recomputed
# at the one place that enforces it, because the coverage guard in
# `tools/tests/test_chronology.py` asks the same question and two spellings of
# one set is how they stop agreeing.
EARNED_STATUSES = ("dated", "composition-only", "attestation-only")

AUTHORED_STATUSES = tuple(
    status
    for status in STATUSES
    if status not in EARNED_STATUSES and status != "research-pending"
)

# --- Errors -----------------------------------------------------------------


class ChronologyError(ValueError):
    """Authored chronology that cannot be loaded, with the reason and the file."""


class Unresolved(NamedTuple):
    """A refusal. Returned, never raised, so a caller can print the reason."""

    status: str
    reason: str
    locus: str = ""

    @property
    def resolved(self) -> bool:
        return False


# --- Identity ---------------------------------------------------------------

# Lowercase, dotted, machine-readable, independent of any path or title, per
# `guidance/sources.md`. `life-of-christ.crucifixion` rather than a number, so
# that a binding names what it means and a reviewer reads it.
ID = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*(?:\.[a-z0-9]+(?:-[a-z0-9]+)*)*\Z")


def check_id(value: object, what: str, where: str) -> str:
    if not isinstance(value, str) or not ID.match(value):
        raise ChronologyError(
            f"{where}: {value!r} is not a {what} id; ids are lowercase words "
            f"joined by hyphens, in dotted namespaces"
        )
    return value


class Locus(NamedTuple):
    """One verse, in a named system. `_projection.Locus` plus its system."""

    system: str
    token: str
    chapter: int
    verse: int

    def __str__(self) -> str:
        return f"{self.token}.{self.chapter}.{self.verse}"


class Span(NamedTuple):
    """A contiguous run inside one chapter. `last` None means to its end."""

    system: str
    token: str
    chapter: int
    first: int | None
    last: int | None

    def __str__(self) -> str:
        # A whole-book scope has no chapter, and printing one anyway produced
        # the literal "Ezech.None" — which then travelled out to consumers as
        # the authored scope of every whole-book binding. That string is the
        # provenance channel now that scope and directness have stopped
        # deciding status, so it has to name something real.
        if self.chapter is None:
            return self.token
        if self.first is None and self.last is None:
            return f"{self.token}.{self.chapter}"
        if self.first == self.last:
            return f"{self.token}.{self.chapter}.{self.first}"
        return f"{self.token}.{self.chapter}.{self.first or 1}-{self.last if self.last is not None else ''}"


def parse_locus(value: str, where: str = "locus", system: str = CANONICAL_SYSTEM) -> Locus:
    """`Ps.50.3` as `_projection.point` reads one, carrying its system."""
    try:
        token, chapter, verse = value.rsplit(".", 2)
        return Locus(system, token, int(chapter), int(verse))
    except ValueError as exc:
        raise ChronologyError(
            f"{where}: {value!r} is not a book.chapter.verse locus"
        ) from exc


# --- Dates ------------------------------------------------------------------

MONTH_LENGTH = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


class Endpoint(NamedTuple):
    """One end of a date. Absent fields are unknown, never defaulted."""

    year: int | None
    era: str | None
    month: int | None
    day: int | None
    calendar: str | None

    def key(self) -> tuple[int, int]:
        """Sortable within one era axis. B.C. counts down, so it negates."""
        if self.year is None or self.era is None:
            return (0, 0)
        if self.era == "bc":
            return (0, -self.year)
        if self.era == "ad":
            return (0, self.year)
        return (1, self.year)  # anno mundi: its own axis, never mixed with the first

    def __str__(self) -> str:
        if self.year is None:
            if self.month is None:
                return "?"
            return f"{self.month:02d}-{self.day:02d}" if self.day else f"month {self.month}"
        era = {"bc": "B.C.", "ad": "A.D.", "am": "A.M."}[self.era or "ad"]
        if self.month and self.day:
            return f"{self.year} {era}, {self.month:02d}-{self.day:02d}"
        return f"{self.year} {era}"


class Date(NamedTuple):
    """A structured temporal claim. `label` is the source's words, never truth."""

    precision: str
    begin: Endpoint | None
    end: Endpoint | None
    relative: dict[str, Any] | None
    label: str
    derivation: dict[str, Any] | None
    duration: dict[str, Any] | None = None
    boundary: dict[str, Any] | None = None

    @property
    def derived(self) -> bool:
        return self.derivation is not None

    @property
    def anchor(self) -> str | None:
        """The event this date is measured FROM, and only that.

        A duration's `within` is not an anchor and is deliberately not returned
        here: it says where the span sits, not what it is counted from.
        """
        if self.relative:
            return self.relative.get("of")
        return self.boundary.get("anchor") if self.boundary else None

    def __str__(self) -> str:
        if self.precision == "boundary" and self.boundary:
            if self.boundary.get("statement"):
                return str(self.boundary["statement"])
            direction = {
                "before": "before",
                "after": "after",
                "no-later-than": "no later than",
                "no-earlier-than": "no earlier than",
            }[self.boundary["direction"]]
            return f"{direction} {self.boundary['endpoint']}"
        if self.precision == "duration" and self.duration:
            return str(self.duration.get("statement") or _duration_text(self.duration))
        if self.precision == "relative" and self.relative:
            return str(self.relative.get("statement") or self.relative)
        if self.begin is None:
            return "?"
        if self.begin == self.end or self.end is None:
            head = str(self.begin)
            return f"about {head}" if self.precision == "approximate-year" else head
        joiner = "-" if self.precision == "range" else " to "
        return f"{self.begin}{joiner}{self.end}"


def is_positional_date(date: Date) -> bool:
    """Whether a date locates or bounds its subject in time.

    `day` is structurally allowed to omit a year, so it qualifies only when it
    carries one. `month-day` and `duration` never qualify: both may remain as
    useful assertions beside a last-resort dated witness, but neither can make
    the comprehensive coverage promise true by itself.
    """
    if date.precision not in POSITIONAL_PRECISIONS:
        return False
    if date.precision == "day":
        return bool(date.begin and date.begin.year is not None)
    return True


def _duration_text(duration: dict[str, Any]) -> str:
    """`{years: 18}` as "18 years"; the fallback when a source gave no words."""
    parts = [
        f"{duration[unit]} {unit[:-1] if duration[unit] == 1 else unit}"
        for unit in DURATION_UNITS
        if duration.get(unit)
    ]
    return " ".join(parts) or "?"


def _duration(raw: object, where: str) -> dict[str, Any]:
    """Read a stated length. It is measured from nothing, and says so."""
    if not isinstance(raw, dict):
        raise ChronologyError(f"{where}: a duration must be a mapping")
    unknown = set(raw) - {*DURATION_UNITS, "statement", "within"}
    if unknown:
        raise ChronologyError(f"{where}: unknown duration key(s) {sorted(unknown)}")
    stated = {unit: raw[unit] for unit in DURATION_UNITS if unit in raw}
    if not stated:
        raise ChronologyError(
            f"{where}: a duration must state a length in one of "
            f"{list(DURATION_UNITS)}"
        )
    for unit, value in stated.items():
        if not isinstance(value, int) or isinstance(value, bool):
            raise ChronologyError(f"{where}: duration {unit} must be a whole number")
        if value < 0:
            raise ChronologyError(
                f"{where}: duration {unit} is {value}; a span cannot run backwards"
            )
        if value == 0:
            # Not pedantry. A zero-length span is how "the source says nothing
            # about how long" would look if it were written down, and it must
            # not be writable: absence has `undated-in-tradition` and a gap row.
            raise ChronologyError(
                f"{where}: duration {unit} is zero; a span of no length is not a "
                f"span, and a source that states none is silence, not a duration"
            )
    within = raw.get("within")
    if within is not None and not isinstance(within, str):
        raise ChronologyError(f"{where}: duration 'within' must name one event")
    return {**stated, **({"statement": raw["statement"]} if "statement" in raw else {}),
            **({"within": within} if within else {})}


def _endpoint(raw: object, where: str) -> Endpoint:
    if not isinstance(raw, dict):
        raise ChronologyError(f"{where}: a date endpoint must be a mapping, not {raw!r}")
    unknown = set(raw) - {"year", "era", "month", "day", "calendar"}
    if unknown:
        # An unrecognised key is a hard failure everywhere in this repository:
        # a validator that ignores what it does not know cannot tell a typo
        # from a fact, and `guidance/the-shape.md` §1 is a register of what
        # that costs. `et ego in vobis: null` got in exactly this way.
        raise ChronologyError(f"{where}: unknown endpoint key(s) {sorted(unknown)}")
    year, era = raw.get("year"), raw.get("era")
    month, day, calendar = raw.get("month"), raw.get("day"), raw.get("calendar")
    if year is not None:
        if not isinstance(year, int) or isinstance(year, bool):
            raise ChronologyError(f"{where}: year {year!r} is not a whole number")
        if year == 0:
            # There is no year zero in either Christian era, and a corpus that
            # accepted one would be off by one for every interval crossing it.
            raise ChronologyError(f"{where}: there is no year zero")
        if year < 0:
            raise ChronologyError(
                f"{where}: year {year} is negative; B.C. is an era, not a sign"
            )
        if era not in ERAS:
            raise ChronologyError(f"{where}: era {era!r} is not one of {list(ERAS)}")
    elif era is not None:
        raise ChronologyError(f"{where}: era {era!r} given with no year")
    if month is not None:
        if not isinstance(month, int) or not 1 <= month <= 12:
            raise ChronologyError(f"{where}: month {month!r} is not 1-12")
    if day is not None:
        if month is None:
            raise ChronologyError(f"{where}: day {day!r} given with no month")
        if not isinstance(day, int) or not 1 <= day <= MONTH_LENGTH[month - 1]:
            raise ChronologyError(
                f"{where}: day {day!r} is not a day of month {month}"
            )
    if calendar is not None and calendar not in ("julian", "gregorian", "hebrew"):
        raise ChronologyError(f"{where}: calendar {calendar!r} is not recognised")
    return Endpoint(year, era, month, day, calendar)


def parse_date(raw: object, where: str) -> Date:
    """Read one date, refusing every shape that could be read two ways."""
    if not isinstance(raw, dict):
        raise ChronologyError(f"{where}: a date must be a mapping, not {raw!r}")
    unknown = set(raw) - {
        "precision", "from", "to", "relative", "duration", "boundary", "label",
        "derivation",
    }
    if unknown:
        raise ChronologyError(f"{where}: unknown date key(s) {sorted(unknown)}")
    precision = raw.get("precision")
    if precision not in PRECISIONS:
        raise ChronologyError(
            f"{where}: precision {precision!r} is not one of {list(PRECISIONS)}"
        )
    label = raw.get("label") or ""
    if not isinstance(label, str):
        raise ChronologyError(f"{where}: label must be text")
    derivation = raw.get("derivation")
    if derivation is not None:
        # A derivation is what makes a date derived; there is no second word
        # saying so, because two ways of saying it is one way of disagreeing.
        if not isinstance(derivation, dict) or not derivation.get("rule"):
            raise ChronologyError(
                f"{where}: a derivation must name the rule it applied"
            )
        if not derivation.get("inputs"):
            raise ChronologyError(
                f"{where}: a derivation must name the input claims it used, so "
                f"the result can be recomputed rather than trusted"
            )
        unknown_derivation = set(derivation) - {"rule", "inputs", "note"}
        if unknown_derivation:
            raise ChronologyError(
                f"{where} derivation: unknown key(s) {sorted(unknown_derivation)}"
            )

    relative = raw.get("relative")
    duration = raw.get("duration")
    boundary = raw.get("boundary")

    if precision == "boundary":
        if relative is not None or duration is not None:
            raise ChronologyError(
                f"{where}: a boundary carries its endpoint or anchor inside "
                f"'boundary', not relative or duration"
            )
        if raw.get("from") or raw.get("to"):
            raise ChronologyError(
                f"{where}: a boundary carries one endpoint, not a from/to range"
            )
        if not isinstance(boundary, dict):
            raise ChronologyError(f"{where}: precision 'boundary' needs a mapping")
        unknown_boundary = set(boundary) - {
            "direction", "endpoint", "anchor", "statement",
        }
        if unknown_boundary:
            raise ChronologyError(
                f"{where} boundary: unknown key(s) {sorted(unknown_boundary)}"
            )
        direction = boundary.get("direction")
        if direction not in BOUNDARY_DIRECTIONS:
            raise ChronologyError(
                f"{where}: boundary direction {direction!r} is not one of "
                f"{list(BOUNDARY_DIRECTIONS)}"
            )
        endpoint = boundary.get("endpoint")
        anchor = boundary.get("anchor")
        if (endpoint is None) == (anchor is None):
            raise ChronologyError(
                f"{where}: a boundary needs exactly one of endpoint or anchor"
            )
        if endpoint is not None:
            parsed_endpoint = _endpoint(endpoint, f"{where} boundary endpoint")
            if parsed_endpoint.year is None:
                raise ChronologyError(
                    f"{where}: a boundary endpoint needs a year"
                )
            if boundary.get("statement") is not None and not isinstance(
                boundary.get("statement"), str
            ):
                raise ChronologyError(
                    f"{where}: boundary statement must be text"
                )
            normalized = {
                "direction": direction,
                "endpoint": parsed_endpoint,
                **(
                    {"statement": boundary["statement"]}
                    if boundary.get("statement") else {}
                ),
            }
            return Date(
                precision, parsed_endpoint, parsed_endpoint, None, label,
                derivation, None, normalized,
            )
        if not isinstance(anchor, str) or not anchor.strip():
            raise ChronologyError(f"{where}: boundary anchor must name one subject")
        statement = boundary.get("statement")
        if not isinstance(statement, str) or not statement.strip():
            raise ChronologyError(
                f"{where}: an anchor boundary needs the source's statement"
            )
        return Date(
            precision, None, None, None, label, derivation, None,
            {"direction": direction, "anchor": anchor, "statement": statement},
        )
    if boundary is not None:
        raise ChronologyError(f"{where}: only precision 'boundary' carries 'boundary'")

    # The two are kept apart structurally, not by convention, because the whole
    # point of the distinction is that a consumer must never read one as the
    # other. A duration that could name an offset anchor would be exactly the
    # overloaded value this precision was split out to abolish.
    if precision == "duration":
        if relative is not None:
            raise ChronologyError(
                f"{where}: a duration is measured from nothing and carries no "
                f"'relative' anchor. If the source says how long AND where it "
                f"is measured from, those are two claims; if it says how long "
                f"and merely where it sits, that is duration.within"
            )
        if raw.get("from") or raw.get("to"):
            raise ChronologyError(
                f"{where}: a duration carries no absolute endpoints; give it "
                f"precision 'range' or 'interval' if the source states them"
            )
        return Date(
            precision, None, None, None, label, derivation, _duration(duration, where)
        )
    if duration is not None:
        raise ChronologyError(
            f"{where}: only a duration carries 'duration'; precision "
            f"{precision!r} states a position in time, not a length"
        )

    if precision == "relative":
        if not isinstance(relative, dict) or not relative.get("of"):
            raise ChronologyError(
                f"{where}: a relative date must name the event it is relative to"
            )
        if raw.get("from") or raw.get("to"):
            raise ChronologyError(
                f"{where}: a relative date carries no absolute endpoints; "
                f"give it precision 'interval' if it has them"
            )
        return Date(precision, None, None, relative, label, derivation)
    if relative is not None:
        raise ChronologyError(f"{where}: only a relative date carries 'relative'")

    if "from" not in raw:
        raise ChronologyError(f"{where}: precision {precision!r} needs a 'from' endpoint")
    begin = _endpoint(raw["from"], f"{where} from")
    end = _endpoint(raw["to"], f"{where} to") if "to" in raw else begin

    single = precision in ("day", "month-day", "year", "approximate-year")
    if single and begin != end:
        raise ChronologyError(
            f"{where}: precision {precision!r} names one point, but 'from' and "
            f"'to' differ; use 'range' or 'interval'"
        )
    if precision == "day" and (begin.month is None or begin.day is None):
        raise ChronologyError(f"{where}: precision 'day' needs a month and a day")
    if precision == "month-day":
        if begin.month is None or begin.day is None:
            raise ChronologyError(f"{where}: precision 'month-day' needs a month and a day")
        if begin.year is not None:
            raise ChronologyError(
                f"{where}: precision 'month-day' means the year is unknown, but a "
                f"year is given; use 'day'"
            )
    if precision in ("year", "approximate-year", "range", "interval"):
        if begin.year is None or (end and end.year is None):
            raise ChronologyError(f"{where}: precision {precision!r} needs a year")
    if not single and end is not None:
        # Mixing Anno Mundi with a Christian era inside one range would put two
        # different epochs on one axis and produce an ordering nobody asserted.
        if (begin.era == "am") != (end.era == "am"):
            raise ChronologyError(
                f"{where}: a range may not run between Anno Mundi and the "
                f"Christian era; they are different reckonings"
            )
        if end.key() < begin.key():
            raise ChronologyError(
                f"{where}: the range ends at {end} but begins at {begin}"
            )
    return Date(precision, begin, end, None, label, derivation)


# --- Assertions -------------------------------------------------------------


class Claim(NamedTuple):
    """One dated statement about one temporal subject, with its provenance.

    `sources` names source-library records — a passage, artifact, edition or
    work id under `src/sources/works` — or a tracked bible edition. It is never
    empty for a sourced claim: `guidance/the-shape.md` §6 is that provenance
    travels with the artifact, and a date with nothing behind it is exactly the
    fluent wrong answer this apparatus exists to catch.
    """

    profile: str
    disposition: str
    date: Date
    basis: str
    sources: tuple[str, ...]
    note: str
    # RESOLVED AT LOAD, from what the claim states and what its profile says an
    # unstated one means. Both are recorded rather than one derived flag,
    # because a reviewer asking why a figure is not answered needs the class
    # that excluded it, not the fact of exclusion.
    answerability: str = "answerable"
    basis_class: str = "unreviewed"
    reporting_exception: str | None = None

    @property
    def derived(self) -> bool:
        return self.date.derived


class Event(NamedTuple):
    """A reusable temporal subject. Dated once, bound from wherever it happened."""

    id: str
    title: str
    parent: str | None
    claims: tuple[Claim, ...]
    note: str


class Unit(NamedTuple):
    """A textual unit with its own textual-history chronology and extent."""

    id: str
    title: str
    relation: str
    scope: tuple[Span, ...]
    claims: tuple[Claim, ...]
    note: str

    def width(self) -> int:
        """How specific this unit is. A narrower unit wins over a wider one."""
        if any(span.chapter is None for span in self.scope):
            return 0  # whole book
        if any(span.first is None and span.last is None for span in self.scope):
            return 1  # whole chapters
        return 2      # a verse range


class Binding(NamedTuple):
    """A locus range, an event, and the relation that joins them.

    Carries NO date. The date is the event's, held once, which is what stops
    four Gospels acquiring four Crucifixion dates.
    """

    relation: str
    event: str
    scope: tuple[Span, ...]
    note: str
    sources: tuple[str, ...]


class Gap(NamedTuple):
    """A locus range the corpus knowingly says nothing dated about, and why."""

    status: str
    scope: tuple[Span, ...]
    reason: str
    sources: tuple[str, ...]
    profile: str


class Assertion(NamedTuple):
    """What a query returns: a relation, a claim, and where the claim came from.

    `inherited` says the assertion reached this locus through a unit or binding
    scoped wider than the verse asked about, so a consumer can tell a statement
    about this verse from a statement about its book.
    """

    relation: str
    subject: str        # the event or composition-unit id the claim belongs to
    title: str
    claim: Claim
    inherited: bool
    scope: str          # the authored extent it reached this locus from

    def sort_key(self) -> tuple:
        return (
            RELATION_ORDER[self.relation],
            DISPOSITIONS.index(self.claim.disposition),
            self.subject,
            str(self.claim.date),
        )


class Mapping(NamedTuple):
    """Whether the asked locus reached the preferred shared system, and how.

    A SEPARATE AXIS from chronology status, which is the whole of Correction A.
    `status` here answers "may this locus be asserted equivalent to a Vulgate
    one", and its refusals are `_deuterocanon`'s and `_psalms`' own words. It
    never answers "does this locus have chronology", and a consumer that reads
    it as though it did will conclude that the Greek Ecclesiasticus is undated
    because the Latin numbers its chapters differently.
    """

    system: str
    status: str          # shared | native | textually-distinct | not-alignable
    reached: str | None  # the preferred-system locus, where one was reached
    note: str = ""


class Answer(NamedTuple):
    """A resolved locus and everything the corpus says about it."""

    locus: Locus
    assertions: tuple[Assertion, ...]
    status: str
    note: str
    mapping: Mapping | None = None
    asked: str | None = None
    # The requested profile may be a cascade; every assertion still carries
    # the leaf profile that owns the claim. This map makes the selection
    # decision explicit without rewriting provenance onto the claim.
    requested_profile: str | None = None
    resolved_profiles: tuple[tuple[str, str], ...] = ()

    @property
    def resolved(self) -> bool:
        return True


# --- Loading ----------------------------------------------------------------


def _yaml():
    try:
        import yaml  # noqa: PLC0415
    except ModuleNotFoundError as exc:  # pragma: no cover - environment
        raise ChronologyError(
            "PyYAML is required to read the chronology corpus "
            "(requirements-tools.txt)"
        ) from exc
    return yaml


@lru_cache(maxsize=1)
def _strict_loader():
    """A SAFE loader that also records every key stated twice in one mapping.

    PyYAML resolves a repeated key by keeping the last one, silently. A corpus
    that is invalid under YAML 1.2 therefore loads clean, and every gate
    standing behind the loader reports it healthy. That is not hypothetical
    here: edits applied by string replacement left a second `sources:` inside
    one claim of `events.yaml` and a second `label:` inside two `date:`
    mappings of `composition.yaml`, and `validate` reported the corpus valid,
    `check` reported the coverage table current, and the whole test suite
    passed over it. Every duplicated pair happened to be identical, so no
    answer moved -- which is exactly why nothing could see it, and exactly the
    machine-valid-but-wrong shape this apparatus exists to catch.

    The check rides the parse rather than adding a second scan of the bytes,
    and `construct_mapping` is called for every mapping node the document has,
    at every depth, so a key doubled four levels down inside a list of claims
    is seen as readily as one at the top of the file. It is built lazily
    because PyYAML is an optional dependency this module imports on use.
    """
    yaml = _yaml()

    class StrictMappingLoader(yaml.SafeLoader):
        """SafeLoader in every construction; it only refuses to stay quiet."""

        def __init__(self, stream):
            super().__init__(stream)
            self.repeated: list[tuple[Any, int, int]] = []

        def construct_mapping(self, node, deep=False):
            first: dict[Any, int] = {}
            for key_node, _ in node.value:
                key = self.construct_object(key_node, deep=True)
                line = key_node.start_mark.line + 1
                try:
                    seen = first.get(key)
                except TypeError:
                    # An unhashable key. Not our refusal to make: the base
                    # constructor states it, and states it better.
                    continue
                if seen is None:
                    first[key] = line
                else:
                    self.repeated.append((key, seen, line))
            return super().construct_mapping(node, deep=deep)

    return StrictMappingLoader


def _read_document(path: Path) -> Any:
    """Parse one corpus file, refusing a repeated key before anything reads it.

    Every problem in the file is collected before the refusal, because an
    author fixing authored data wants the list -- the same reason `validate`
    collects. The refusal is raised rather than accumulated because a mapping
    with a key stated twice has no defined meaning, and interpreting one is the
    move this gate exists to prevent.
    """
    loader = _strict_loader()(path.read_text(encoding="utf-8"))
    try:
        data = loader.get_single_data()
        repeated = list(loader.repeated)
    finally:
        loader.dispose()
    if repeated:
        listed = "; ".join(
            f"{path}:{line}: key {key!r} is stated twice in one mapping "
            f"(first at line {first})"
            for key, first, line in repeated
        )
        raise ChronologyError(
            f"{listed}. A repeated key is invalid YAML: PyYAML keeps the last "
            f"one silently, so the file means whatever its reader assumed. "
            f"Delete the later occurrence."
        )
    return data


def _document(name: str, root: Path) -> dict[str, Any]:
    path = root / f"{name}.yaml"
    if not path.exists():
        raise ChronologyError(f"{path}: the chronology corpus is missing {name}.yaml")
    # BEFORE the schema check and before any value here is read as a fact: a
    # repeated key makes the whole file's meaning undefined, so it is not a
    # thing to interpret and then complain about.
    data = _read_document(path)
    if not isinstance(data, dict):
        raise ChronologyError(f"{path}: expected a mapping at the top level")
    declared = data.get("schema")
    if declared != SCHEMAS[name]:
        raise ChronologyError(
            f"{path}: declares schema {declared!r}; this loader reads "
            f"{SCHEMAS[name]!r}"
        )
    if name in LOCUS_BEARING:
        # A locus without its declared system is the exact defect
        # `guidance/bibles-for-agents.md` opens with, and the neighbouring
        # datasets all declare it at the top of the file for that reason:
        # `src/sources/commentary/fragment-loci.yaml` and
        # `src/sources/reading-plans/narrative-spine.yaml` both do.
        numbering = data.get("numbering")
        if numbering != CANONICAL_SYSTEM:
            raise ChronologyError(
                f"{path}: declares numbering {numbering!r}; chronology is "
                f"authored in {CANONICAL_SYSTEM!r} and a file that does not say "
                f"so is a file whose loci mean whatever the reader assumed"
            )
    return data


def _keys(raw: dict[str, Any], allowed: set[str], where: str) -> None:
    """Refuse an unrecognised key rather than ignoring it.

    A validator that skips what it does not recognise cannot tell a typo from a
    fact. `guidance/sources.md` names the absence of this check on propers as a
    known gap; it is not going to be a gap here.
    """
    unknown = set(raw) - allowed
    if unknown:
        raise ChronologyError(f"{where}: unknown key(s) {sorted(unknown)}")


def _text(raw: dict[str, Any], key: str, where: str, required: bool = False) -> str:
    value = raw.get(key, "")
    if value in (None, ""):
        if required:
            raise ChronologyError(f"{where}: {key} is required")
        return ""
    if not isinstance(value, str):
        raise ChronologyError(f"{where}: {key} must be text, not {value!r}")
    return value.strip()


def _sources(raw: dict[str, Any], where: str, required: bool) -> tuple[str, ...]:
    value = raw.get("sources") or []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ChronologyError(f"{where}: sources must be a list of record ids")
    if required and not value:
        raise ChronologyError(
            f"{where}: a sourced claim must name at least one source record; "
            f"a date with no provenance cannot be checked and is not admitted"
        )
    return tuple(value)


def _answerability(
    entry: dict[str, Any], spot: str, policy: Policy | None
) -> tuple[str, str, str | None]:
    """The state, the basis class and the exception one claim actually carries.

    THE CONTRADICTIONS ARE REFUSED HERE, at the only moment both the claim and
    its profile are in hand. A claim that says it is answerable on a basis its
    profile excludes is not a claim with a bad note; it is two statements that
    cannot both be true, and admitting it would put the whole contract back
    where it was — in prose, beside a value the query returned anyway.
    """
    state = entry.get("answerability")
    if state is None:
        state = policy.unstated_answerability if policy else "answerable"
    if state not in ANSWERABILITY:
        raise ChronologyError(
            f"{spot}: answerability {state!r} is not one of {list(ANSWERABILITY)}"
        )
    basis_class = entry.get("basis_class")
    if basis_class is None:
        basis_class = policy.unstated_basis if policy else "unreviewed"
    elif policy and basis_class not in policy.classes:
        raise ChronologyError(
            f"{spot}: basis_class {basis_class!r} is not a basis class "
            f"{policy.profile} declares; it declares {sorted(policy.classes)}"
        )
    lift = entry.get("reporting_exception")
    if lift is not None and not isinstance(lift, str):
        raise ChronologyError(f"{spot}: reporting_exception must name one exception")
    if lift and policy:
        declared = policy.exceptions.get(lift)
        if declared is None:
            raise ChronologyError(
                f"{spot}: reporting_exception {lift!r} is not declared by "
                f"{policy.profile}; the exceptions it declares are "
                f"{sorted(policy.exceptions)}"
            )
        if declared.get("basis") != basis_class:
            # THE EXCEPTION DOES NOT GENERALISE, and this is where that is true
            # rather than merely written down. Ussher's exception lifts
            # `reported-excluded` and nothing else; a claim reaching for it from
            # `modern-critical` is refused by name.
            raise ChronologyError(
                f"{spot}: reporting_exception {lift!r} lifts basis class "
                f"{declared.get('basis')!r}, and this claim's basis class is "
                f"{basis_class!r}; a named exception admits one excluded basis "
                f"and does not extend by analogy to another"
            )
        if state != "answerable":
            raise ChronologyError(
                f"{spot}: reporting_exception {lift!r} is named on a "
                f"{state!r} claim; an exception exists to make a value "
                f"answerable and says nothing about preserved evidence"
            )
    if policy and state == "answerable" and basis_class not in policy.admissible:
        if not (lift and policy.exceptions.get(lift, {}).get("basis") == basis_class):
            raise ChronologyError(
                f"{spot}: basis_class {basis_class!r} is not admissible under "
                f"{policy.profile}, so this claim may not be 'answerable'. A "
                f"chronology value is a candidate answer only when both the "
                f"source AND the basis for that value are admissible; preserve "
                f"it with answerability: preserved instead"
            )
    if state == "preserved" and entry.get("disposition", "preferred") == "preferred":
        raise ChronologyError(
            f"{spot}: a 'preserved' claim may not be 'preferred'; preferred "
            f"means the claim this profile displays first, and preserved "
            f"evidence is never displayed as an answer"
        )
    return state, str(basis_class), (lift or None)


def _claims(
    raw: dict[str, Any],
    where: str,
    policies: dict[str, Policy],
    required: bool = True,
) -> tuple[Claim, ...]:
    listed = raw.get("dates")
    if listed is None and not required:
        # A SUBJECT WITH NO CLAIM IS STILL A SUBJECT. An event exists to be
        # named — by a binding, or as the anchor another claim is measured
        # from — and naming one is not the same act as dating it. Requiring a
        # date of every event meant that withdrawing the only claim on a
        # subject was impossible without deleting the subject, and where other
        # claims anchor on it that cannot be done either. The corpus met this
        # at `israel.monarchy.saul-accession`, whose single claim was a modern
        # reconstruction §4.3 excludes and on whose identity other claims and
        # bindings depend. An event with no `dates` asserts nothing,
        # returns nothing, and leaves the loci bound to it to whatever else
        # reaches them — which is the honest answer when no ranked source has
        # dated it. A composition unit still requires one: a unit exists only
        # to carry a composition date, so a dateless one would be a scope
        # asserting nothing about the text it names.
        return ()
    if not isinstance(listed, list) or not listed:
        raise ChronologyError(f"{where}: needs a non-empty 'dates' list")
    claims: list[Claim] = []
    for index, entry in enumerate(listed, start=1):
        spot = f"{where} date {index}"
        if not isinstance(entry, dict):
            raise ChronologyError(f"{spot}: expected a mapping")
        _keys(
            entry,
            {
                "profile", "disposition", "date", "basis", "sources", "note",
                "answerability", "basis_class", "reporting_exception",
            },
            spot,
        )
        profile = entry.get("profile")
        if profile not in policies:
            raise ChronologyError(
                f"{spot}: profile {profile!r} is not declared in profiles.yaml"
            )
        disposition = entry.get("disposition", "preferred")
        if disposition not in DISPOSITIONS:
            raise ChronologyError(
                f"{spot}: disposition {disposition!r} is not one of "
                f"{list(DISPOSITIONS)}"
            )
        date = parse_date(entry.get("date"), spot)
        state, basis_class, lift = _answerability(entry, spot, policies.get(profile))
        claims.append(
            Claim(
                profile=profile,
                disposition=disposition,
                date=date,
                basis=_text(entry, "basis", spot, required=True),
                sources=_sources(entry, spot, required=not date.derived),
                note=_text(entry, "note", spot),
                answerability=state,
                basis_class=basis_class,
                reporting_exception=lift,
            )
        )
    # The conflict policy, enforced rather than described: one preferred claim
    # per profile, and none at all while any claim on the subject is disputed.
    #
    # OVER THE CANDIDATE SET ONLY. `preferred`, `alternate` and `disputed` say
    # which admissible claim this profile displays first; preserved evidence is
    # displayed as no answer at all, so counting it here would make withdrawing
    # a figure from the answers into a conflict-policy error, and would leave a
    # subject whose every answerable claim was withdrawn asserting that one of
    # its preserved figures is preferred.
    for profile in policies:
        mine = [
            claim for claim in claims
            if claim.profile == profile and claim.answerability == "answerable"
        ]
        preferred = [claim for claim in mine if claim.disposition == "preferred"]
        disputed = [claim for claim in mine if claim.disposition == "disputed"]
        if len(preferred) > 1:
            raise ChronologyError(
                f"{where}: {len(preferred)} claims are 'preferred' under "
                f"{profile}; exactly one may be"
            )
        if preferred and disputed:
            raise ChronologyError(
                f"{where}: a claim is 'preferred' under {profile} while another "
                f"is 'disputed'; an unsettled disagreement has no preferred side"
            )
        if len(mine) > 1 and not preferred and not disputed:
            raise ChronologyError(
                f"{where}: {len(mine)} claims under {profile} and none is "
                f"preferred or disputed; say which"
            )
    return tuple(claims)


def _scope(raw: object, where: str, books: dict[str, int]) -> tuple[Span, ...]:
    """Read an authored extent into spans, one per chapter it touches."""
    entries = raw if isinstance(raw, list) else [raw]
    spans: list[Span] = []
    for index, entry in enumerate(entries, start=1):
        spot = f"{where} scope {index}" if len(entries) > 1 else f"{where} scope"
        if not isinstance(entry, dict):
            raise ChronologyError(f"{spot}: expected a mapping")
        _keys(entry, {"system", "book", "chapter", "through", "first", "last"}, spot)
        system = entry.get("system", PREFERRED_SYSTEM)
        systems = scripture_systems()
        if system not in systems:
            raise ChronologyError(
                f"{spot}: {system!r} is not a Scripture system this repository "
                f"has machinery for; the systems are {sorted(systems)}"
            )
        token = entry.get("book")
        addressable = systems[system]
        if addressable is not None and token not in addressable:
            # The check the flat-set version could not make. `hebrew` is a
            # psalter numbering and names nothing outside it; `greek` addresses
            # the seven books `_deuterocanon` holds a witness for and no others.
            raise ChronologyError(
                f"{spot}: {system!r} does not number {token!r}; it addresses "
                f"{sorted(addressable)}"
            )
        if system == PREFERRED_SYSTEM and token not in books:
            raise ChronologyError(
                f"{spot}: {token!r} is not a book of the canon; see scripts/_canon.py"
            )
        # A NATIVE SCOPE IS BOUNDED BY ITS OWN WITNESS, not by the canon. The
        # canon check refused every scope naming `EsthGr`, which the Greek
        # witness prints and `scripture_systems()` admits but `_canon` has no
        # book row for — so a native locus in it could not be given a gap row,
        # and the ten loci the cold audit found carrying a mapping word where a
        # chronology status belongs had no route to an authored one. A system's
        # extent is read from the text that prints it, the same rule
        # `_system_loci` obeys.
        limits = books
        if system != PREFERRED_SYSTEM:
            printed = _system_loci(system) or []
            native_chapters: dict[str, int] = {}
            for there, chapter_number, _verse in printed:
                native_chapters[there] = max(
                    native_chapters.get(there, 0), chapter_number
                )
            if token not in native_chapters:
                raise ChronologyError(
                    f"{spot}: {system!r} prints no {token!r}; it prints "
                    f"{sorted(native_chapters)}"
                )
            limits = native_chapters
        books = limits
        chapter = entry.get("chapter")
        through = entry.get("through", chapter)
        first, last = entry.get("first"), entry.get("last")
        if chapter is None:
            if first is not None or last is not None or through is not None:
                raise ChronologyError(
                    f"{spot}: a whole-book scope names no chapter or verse"
                )
            spans.append(Span(system, token, None, None, None))
            continue
        if not isinstance(chapter, int) or not 1 <= chapter <= books[token]:
            raise ChronologyError(
                f"{spot}: {token} has {books[token]} chapters; {chapter!r} is not one"
            )
        if not isinstance(through, int) or not chapter <= through <= books[token]:
            raise ChronologyError(
                f"{spot}: 'through' {through!r} is not a chapter of {token} at or "
                f"after {chapter}"
            )
        if through != chapter:
            # A run across chapters: open at the join, exactly as `_loci` does,
            # so no verse count is needed to describe it.
            spans.append(Span(system, token, chapter, first, None))
            for middle in range(chapter + 1, through):
                spans.append(Span(system, token, middle, None, None))
            spans.append(Span(system, token, through, None, last))
            continue
        if first is not None and last is not None and last < first:
            raise ChronologyError(
                f"{spot}: the range ends at verse {last} but begins at {first}"
            )
        spans.append(Span(system, token, chapter, first, last))
    if not spans:
        raise ChronologyError(f"{where}: a scope names no text")
    return tuple(spans)


class Policy(NamedTuple):
    """One profile's admissibility contract, normalised out of its YAML.

    THE GOVERNING RULE, in the smallest machine form that can enforce it: a
    chronology value is a candidate answer under a profile only when BOTH the
    source AND the basis for that particular value are admissible under it.

    The source half is `authority`/`non_authorities` and is reviewed when a
    claim is authored. `audit()` mechanically proves that named provenance is a
    real repository record (and, for Scripture, a real edition locus); it does
    not infer that source's authority rank from its id. The basis half is this:
    every claim carries the class of the method its value came from, and the
    profile says which classes it answers with. Neither half can be satisfied
    by the other, which is the whole point. A Catholic author's own voice
    satisfies the first and settles nothing about the second.

    `admissible` is deliberately a set of class names and NOT a rank threshold.
    Rank orders admissible evidence; there is no rank at which an excluded
    method becomes admissible, so admissibility cannot be expressed as a
    position in the hierarchy and must not be stored as one.
    """

    profile: str
    admissible: frozenset[str]      # basis classes this profile answers with
    classes: frozenset[str]         # every class it declares; others are typos
    unstated_basis: str             # the class a claim that names none carries
    unstated_answerability: str     # the state a claim that names none carries
    exceptions: dict[str, dict[str, Any]]  # narrow, named reporting lifts

    def answers_with(self, claim: "Claim") -> bool:
        """Is this claim in the default candidate set? The one place it is asked.

        Admissibility of the BASIS is decided here and nowhere else, and it is
        decided before rank: nothing in this function consults the authority
        hierarchy, the disposition, or the order assertions are returned in.
        Human review uses rank to author a disposition. Sorting reproduces that
        disposition; this function neither computes nor infers source rank.
        """
        if claim.answerability != "answerable":
            return False
        if claim.basis_class in self.admissible:
            return True
        lifted = self.exceptions.get(claim.reporting_exception or "")
        return bool(lifted and lifted.get("basis") == claim.basis_class)


class Cascade(NamedTuple):
    """An ordered composition of leaf evidence profiles.

    A cascade owns no claims and makes no new chronology assertion. For each
    relation independently, it selects the first leaf with at least one
    answerable candidate and returns that leaf's complete candidate set.
    """

    profile: str
    fallback_profiles: tuple[str, ...]
    selection: str


class Corpus(NamedTuple):
    """Everything authored, validated, and keyed the way a query asks for it."""

    profiles: dict[str, dict[str, Any]]
    events: dict[str, Event]
    units: dict[str, Unit]
    bindings: tuple[Binding, ...]
    gaps: tuple[Gap, ...]
    books: dict[str, int]
    policies: dict[str, Policy]
    cascades: dict[str, Cascade]
    default_profile: str

    def answers_with(self, claim: Claim) -> bool:
        """Whether the profile the claim was authored under answers with it.

        A claim whose profile declares no policy is answerable, and that is not
        a loophole: `_load_profiles` refuses a profile with no `admissibility`
        block, so a corpus that reaches here without one has none because it was
        built by hand in a test.
        """
        policy = self.policies.get(claim.profile)
        return policy.answers_with(claim) if policy else True


def _canon_books() -> dict[str, int]:
    """The canon's book tokens and chapter counts, read from `_canon`.

    Not restated here. `_canon` reads the canonical edition's own book index,
    and a second list beside it would be the hand-written table that
    `guidance/the-shape.md` §2 says has already disagreed with the derived one.
    """
    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import _canon  # noqa: PLC0415

    return {book["token"]: int(book["chapters"]) for book in _canon.books()}


def _policy(entry: dict[str, Any], where: str) -> Policy:
    """Read one profile's admissibility contract, refusing anything ambiguous.

    Every refusal here is a state that would otherwise have to be caught by a
    reader noticing prose. An unrecognised basis class, a profile whose unstated
    default names nothing, a reporting exception that lifts a class already
    admissible: each of them means the policy says something other than what it
    looks like it says, and a policy nobody can read is not a control.
    """
    raw = entry.get("admissibility")
    if not isinstance(raw, dict):
        raise ChronologyError(
            f"{where}: admissibility must be a mapping stating this profile's "
            f"basis classes; a profile that does not say which METHODS it "
            f"answers with cannot tell a traditional figure from a modern one "
            f"reprinted in a traditional book"
        )
    for required in ("rule", "own_voice", "before_rank", "preservation", "bases"):
        if not raw.get(required):
            raise ChronologyError(f"{where}: admissibility states no {required}")
    listed = raw.get("bases")
    if not isinstance(listed, list) or not listed:
        raise ChronologyError(f"{where}: admissibility needs a non-empty 'bases' list")
    classes: dict[str, bool] = {}
    for index, base in enumerate(listed, start=1):
        spot = f"{where} basis {index}"
        if not isinstance(base, dict):
            raise ChronologyError(f"{spot}: a basis class must be a mapping")
        _keys(base, {"id", "admissible", "what"}, spot)
        identifier = check_id(base.get("id"), "basis class", spot)
        if identifier in classes:
            raise ChronologyError(f"{spot}: duplicate basis class {identifier!r}")
        admissible = base.get("admissible")
        if not isinstance(admissible, bool):
            raise ChronologyError(
                f"{spot}: basis class {identifier!r} must say admissible: true "
                f"or false; a class that does not say is a class a reader will "
                f"assume about"
            )
        if not _text(base, "what", spot, required=True):
            raise ChronologyError(f"{spot}: basis class {identifier!r} states no 'what'")
        classes[identifier] = admissible
    unstated = raw.get("unstated")
    if unstated not in classes:
        raise ChronologyError(
            f"{where}: admissibility 'unstated' is {unstated!r}, which is not "
            f"one of this profile's basis classes {sorted(classes)}; a claim "
            f"that names no basis class has to land somewhere stated"
        )
    exceptions: dict[str, dict[str, Any]] = {}
    for index, lift in enumerate(raw.get("reporting_exceptions") or [], start=1):
        spot = f"{where} reporting exception {index}"
        if not isinstance(lift, dict):
            raise ChronologyError(f"{spot}: a reporting exception must be a mapping")
        _keys(
            lift,
            {"id", "named", "basis", "requires", "display", "does_not_generalise"},
            spot,
        )
        identifier = check_id(lift.get("id"), "reporting exception", spot)
        if identifier in exceptions:
            raise ChronologyError(f"{spot}: duplicate reporting exception {identifier!r}")
        for required in ("named", "requires", "display", "does_not_generalise"):
            if not _text(lift, required, spot):
                raise ChronologyError(
                    f"{spot}: reporting exception {identifier!r} states no "
                    f"{required}; an exception whose scope is not written down "
                    f"is the general licence it was written not to be"
                )
        basis = lift.get("basis")
        if basis not in classes:
            raise ChronologyError(
                f"{spot}: reporting exception {identifier!r} lifts basis class "
                f"{basis!r}, which this profile does not declare"
            )
        if classes[basis]:
            # NARROWNESS, ENFORCED. An exception over an admissible class lifts
            # nothing and reads as though it lifted everything, which is exactly
            # how a named exception becomes a general licence.
            raise ChronologyError(
                f"{spot}: reporting exception {identifier!r} lifts basis class "
                f"{basis!r}, which is already admissible; an exception exists to "
                f"admit one excluded basis and nothing else"
            )
        exceptions[identifier] = dict(lift)
    states = entry.get("answerability")
    if not isinstance(states, dict):
        raise ChronologyError(
            f"{where}: answerability must be a mapping saying what this profile "
            f"answers with and what it merely preserves"
        )
    for required in ("states", "query", "refusal", "dispositions"):
        if not states.get(required):
            raise ChronologyError(f"{where}: answerability states no {required}")
    declared = states.get("states")
    if not isinstance(declared, dict) or set(declared) != set(ANSWERABILITY):
        raise ChronologyError(
            f"{where}: answerability must define exactly {list(ANSWERABILITY)}"
        )
    default_state = states.get("unstated")
    if default_state not in ANSWERABILITY:
        raise ChronologyError(
            f"{where}: answerability 'unstated' is {default_state!r}, not one of "
            f"{list(ANSWERABILITY)}"
        )
    return Policy(
        profile=str(entry.get("id")),
        admissible=frozenset(name for name, ok in classes.items() if ok),
        classes=frozenset(classes),
        unstated_basis=str(unstated),
        unstated_answerability=str(default_state),
        exceptions=exceptions,
    )


def _load_profile_contract(
    root: Path,
) -> tuple[
    dict[str, dict[str, Any]], dict[str, Policy], dict[str, Cascade], str
]:
    document = _document("profiles", root)
    listed = document.get("profiles")
    if not isinstance(listed, list) or not listed:
        raise ChronologyError(f"{root}/profiles.yaml: needs a non-empty 'profiles' list")
    profiles: dict[str, dict[str, Any]] = {}
    policies: dict[str, Policy] = {}
    cascades: dict[str, Cascade] = {}
    for entry in listed:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/profiles.yaml: a profile must be a mapping")
        identifier = check_id(entry.get("id"), "profile", f"{root}/profiles.yaml")
        if identifier in profiles:
            raise ChronologyError(f"{root}/profiles.yaml: duplicate profile {identifier}")
        profiles[identifier] = entry

    for identifier, entry in profiles.items():
        kind = entry.get("kind", "evidence")
        if kind == "cascade":
            _keys(
                entry,
                {
                    "id", "kind", "title", "intent", "fallback_profiles",
                    "selection", "non_goals", "versioning",
                },
                f"{root}/profiles.yaml cascade {identifier!r}",
            )
            for required in (
                "title", "intent", "fallback_profiles", "selection",
                "non_goals", "versioning",
            ):
                if not entry.get(required):
                    raise ChronologyError(
                        f"{root}/profiles.yaml: cascade {identifier} states no "
                        f"{required}"
                    )
            fallback = entry.get("fallback_profiles")
            if (
                not isinstance(fallback, list)
                or not fallback
                or not all(isinstance(item, str) for item in fallback)
            ):
                raise ChronologyError(
                    f"{root}/profiles.yaml: cascade {identifier} needs a "
                    f"non-empty fallback_profiles list"
                )
            if len(fallback) != len(set(fallback)):
                raise ChronologyError(
                    f"{root}/profiles.yaml: cascade {identifier} repeats a "
                    f"fallback profile"
                )
            selection = entry.get("selection")
            if selection != CASCADE_SELECTION:
                raise ChronologyError(
                    f"{root}/profiles.yaml: cascade {identifier} selection "
                    f"{selection!r} is not {CASCADE_SELECTION!r}"
                )
            cascades[identifier] = Cascade(
                identifier, tuple(fallback), str(selection)
            )
            continue
        if kind != "evidence":
            raise ChronologyError(
                f"{root}/profiles.yaml: profile {identifier} kind {kind!r} is "
                f"neither 'evidence' nor 'cascade'"
            )
        for required in (
            "title", "intent", "authority", "admissibility", "answerability",
            "conflict", "non_goals",
        ):
            if not entry.get(required):
                raise ChronologyError(
                    f"{root}/profiles.yaml: profile {identifier} states no {required}; "
                    f"a profile that does not say what wins is not a policy"
                )
        policies[identifier] = _policy(
            entry, f"{root}/profiles.yaml profile {identifier!r}"
        )

    for identifier, cascade in cascades.items():
        for fallback in cascade.fallback_profiles:
            if fallback not in policies:
                kind = "cascade" if fallback in cascades else "undeclared"
                raise ChronologyError(
                    f"{root}/profiles.yaml: cascade {identifier} fallback "
                    f"{fallback!r} is {kind}; fallbacks must name declared leaf "
                    f"evidence profiles"
                )

    default = document.get("default_profile")
    if default is None:
        if len(profiles) != 1:
            raise ChronologyError(
                f"{root}/profiles.yaml: multiple profiles require one explicit "
                f"top-level default_profile; omitting --profile must never union "
                f"claims silently"
            )
        default = next(iter(profiles))
    if default not in profiles:
        raise ChronologyError(
            f"{root}/profiles.yaml: default_profile {default!r} is not declared"
        )
    return profiles, policies, cascades, str(default)


def _load_profiles(root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, Policy]]:
    """Compatibility surface for callers inspecting leaf profile policy."""
    profiles, policies, _cascades, _default = _load_profile_contract(root)
    return profiles, policies


def _load_events(root: Path, policies: dict[str, Policy]) -> dict[str, Event]:
    document = _document("events", root)
    events: dict[str, Event] = {}
    for entry in document.get("events") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/events.yaml: an event must be a mapping")
        where = f"{root}/events.yaml event {entry.get('id')!r}"
        _keys(entry, {"id", "title", "parent", "dates", "note"}, where)
        identifier = check_id(entry.get("id"), "event", where)
        if identifier in events:
            raise ChronologyError(f"{where}: duplicate event id")
        events[identifier] = Event(
            id=identifier,
            title=_text(entry, "title", where, required=True),
            parent=check_id(entry["parent"], "event", where) if entry.get("parent") else None,
            claims=_claims(entry, where, policies, required=False),
            note=_text(entry, "note", where),
        )
    for event in events.values():
        if event.parent and event.parent not in events:
            raise ChronologyError(
                f"{root}/events.yaml: event {event.id} names parent "
                f"{event.parent}, which no event declares"
            )
    # A cycle in the parent chain would make any walk of it non-terminating,
    # and an event that is its own ancestor is not a fact about time.
    for event in events.values():
        seen, walk = {event.id}, event.parent
        while walk:
            if walk in seen:
                raise ChronologyError(
                    f"{root}/events.yaml: event {event.id}'s parent chain is a cycle"
                )
            seen.add(walk)
            walk = events[walk].parent
    return events


def _load_units(
    root: Path, policies: dict[str, Policy], books: dict[str, int]
) -> dict[str, Unit]:
    document = _document("composition", root)
    units: dict[str, Unit] = {}
    for entry in document.get("units") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/composition.yaml: a unit must be a mapping")
        where = f"{root}/composition.yaml unit {entry.get('id')!r}"
        _keys(entry, {"id", "title", "relation", "scope", "dates", "note"}, where)
        identifier = check_id(entry.get("id"), "composition unit", where)
        if identifier in units:
            raise ChronologyError(f"{where}: duplicate unit id")
        relation = entry.get("relation", "composition")
        if relation not in TEXTUAL_RELATIONS:
            raise ChronologyError(
                f"{where}: textual-unit relation {relation!r} is not one of "
                f"{sorted(TEXTUAL_RELATIONS)}"
            )
        units[identifier] = Unit(
            id=identifier,
            title=_text(entry, "title", where, required=True),
            relation=relation,
            scope=_scope(entry.get("scope"), where, books),
            claims=_claims(entry, where, policies),
            note=_text(entry, "note", where),
        )
    _refuse_ambiguous_inheritance(units, root)
    return units


def _refuse_ambiguous_inheritance(units: dict[str, Unit], root: Path) -> None:
    """Two units of equal width over one verse and profile are an error.

    Narrowing is evaluated independently inside each evidence profile. Units
    owned by disjoint profiles are not alternatives for one query and may
    therefore overlap; units that share a profile still leave that profile a
    tie nothing may break. The relation is independent for the same reason:
    composition and final formation may describe the same textual extent.
    """
    by_width: dict[
        tuple[str, str, int], dict[tuple[str, str, int, int], str]
    ] = {}
    for unit in units.values():
        width = unit.width()
        for profile in {claim.profile for claim in unit.claims}:
            seen = by_width.setdefault((unit.relation, profile, width), {})
            for span in unit.scope:
                for key in _span_keys(span, unit.scope):
                    if key in seen and seen[key] != unit.id:
                        raise ChronologyError(
                            f"{root}/composition.yaml: units {seen[key]} and "
                            f"{unit.id} both claim {key[0]} "
                            f"{key[1]}.{key[2]}.{key[3]} under {profile} at "
                            f"the same width; narrow one of them"
                        )
                    seen[key] = unit.id


def _span_keys(
    span: Span, _scope_all: tuple[Span, ...]
) -> Iterable[tuple[str, str, int, int]]:
    """The overlap key a span occupies. Chapter-level, so it needs no verse counts.

    Keyed by SYSTEM first. Two whole-book units over `Ecclus` are ambiguous
    only if they are talking about the same text; the Vulgate's
    Ecclesiasticus and the Greek one are two texts, which is the whole reason
    the second may be authored natively at all, and a unit over each is not a
    tie for anything to break.
    """
    if span.chapter is None:
        yield (span.system, span.token, 0, 0)
        return
    if span.first is None and span.last is None:
        yield (span.system, span.token, span.chapter, 0)
        return
    yield (span.system, span.token, span.chapter, span.first or 1)


def _load_bindings(root: Path, events: dict[str, Event], books: dict[str, int]) -> tuple[Binding, ...]:
    document = _document("bindings", root)
    bindings: list[Binding] = []
    for entry in document.get("bindings") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/bindings.yaml: a binding must be a mapping")
        where = (
            f"{root}/bindings.yaml binding {entry.get('relation')!r} -> "
            f"{entry.get('event')!r}"
        )
        if "date" in entry or "dates" in entry:
            # Checked before the key sweep so the message is the reason rather
            # than "unknown key". This is the one door through which parallel
            # passages acquire parallel dates.
            raise ChronologyError(
                f"{where}: a binding carries no date. The event holds it once, "
                f"which is what stops parallel passages acquiring parallel dates"
            )
        _keys(entry, {"relation", "event", "scope", "note", "sources"}, where)
        relation = entry.get("relation")
        if relation not in RELATIONS:
            raise ChronologyError(
                f"{where}: relation {relation!r} is not one of {list(RELATIONS)}"
            )
        if relation in TEXTUAL_RELATIONS:
            raise ChronologyError(
                f"{where}: {relation} is not an event binding; it is a textual "
                f"unit in composition.yaml, because it inherits and an event "
                f"does not"
            )
        event = entry.get("event")
        if event not in events:
            raise ChronologyError(
                f"{where}: event {event!r} is not declared in events.yaml"
            )
        bindings.append(
            Binding(
                relation=relation,
                event=event,
                scope=_scope(entry.get("scope"), where, books),
                note=_text(entry, "note", where),
                sources=_sources(entry, where, required=False),
            )
        )
    return tuple(bindings)


def _load_gaps(
    root: Path, books: dict[str, int], policies: dict[str, Policy]
) -> tuple[Gap, ...]:
    document = _document("gaps", root)
    gaps: list[Gap] = []
    authored = set(AUTHORED_STATUSES)
    default_profile = document.get("profile")
    if default_profile is None:
        # Compatibility for the established corpus and test fixtures. The
        # status itself is explicitly traditional; once another evidence
        # profile needs gaps, the document or row must name it.
        if "catholic-traditional-v1" in policies:
            default_profile = "catholic-traditional-v1"
        elif len(policies) == 1:
            default_profile = next(iter(policies))
    for entry in document.get("gaps") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/gaps.yaml: a gap must be a mapping")
        where = f"{root}/gaps.yaml gap {entry.get('status')!r}"
        _keys(entry, {"profile", "status", "scope", "reason", "sources"}, where)
        status = entry.get("status")
        if status not in authored:
            raise ChronologyError(
                f"{where}: status {status!r} is not one an author may assert; "
                f"choose from {sorted(authored)}. {list(EARNED_STATUSES)} are "
                f"earned from the assertions that apply, and 'research-pending' "
                f"is the default"
            )
        profile = entry.get("profile", default_profile)
        if profile not in policies:
            raise ChronologyError(
                f"{where}: profile {profile!r} is not a declared leaf evidence "
                f"profile"
            )
        gaps.append(
            Gap(
                status=status,
                scope=_scope(entry.get("scope"), where, books),
                reason=_text(entry, "reason", where, required=True),
                sources=_sources(entry, where, required=False),
                profile=str(profile),
            )
        )
    return tuple(gaps)


@lru_cache(maxsize=4)
def load(root: Path | None = None) -> Corpus:
    """Read and validate the whole corpus, or refuse with the reason."""
    where = Path(root) if root is not None else CORPUS_ROOT
    books = _canon_books()
    profiles, policies, cascades, default_profile = _load_profile_contract(where)
    events = _load_events(where, policies)
    units = _load_units(where, policies, books)
    bindings = _load_bindings(where, events, books)
    gaps = _load_gaps(where, books, policies)
    _refuse_dangling_anchors(events, units, where)
    _refuse_duplicated_native_scopes(units, bindings, gaps, where)
    return Corpus(
        profiles, events, units, bindings, gaps, books, policies, cascades,
        default_profile,
    )


def _refuse_duplicated_native_scopes(
    units: dict[str, Unit],
    bindings: tuple[Binding, ...],
    gaps: tuple[Gap, ...],
    where: Path,
) -> None:
    """Native authoring is allowed only where it does not restate a shared fact.

    This is what keeps "one fact, one place" a GATE rather than a convention.
    Admitting native non-Vulgate loci creates exactly one new way to duplicate:
    author a fact at `{system: greek, book: Ecclus}` that the Vulgate already
    holds and that the concordance can safely carry between them.

    TWO THINGS WERE WRONG WITH THE FIRST VERSION OF THIS GATE, and the cold
    audit of `2330d63a5` found both.

    It probed **one locus** — `span.first or 1`, and verse 1 of chapter 1 for a
    whole-book scope — so a span whose opening refused was admitted entire,
    however its interior behaved. A gate that checks the first locus proves
    something about the first locus.

    And it asked the wrong question of the locus it did check. Mappability was
    standing in for duplication, and the two come apart at exactly one place in
    this repository: the concordance carries greek Ecclus 36:16 safely to
    vulgate Ecclus 36:18, but the fact authored natively there is the date of
    the GREEK TRANSLATION, which the Vulgate unit does not hold and could not —
    it dates the Hebrew original and the Latin version. Refusing that scope, or
    splitting it to exclude the one locus, would have deleted the only
    assertion true of that verse. Safe correspondence means the two loci carry
    corresponding text. It does not mean every fact about one is a fact about
    the other.

    So the gate now walks **every locus the witness prints** inside the span,
    and refuses a locus that maps safely only when the native subject would
    restate a claim the preferred locus already holds under the same relation.
    That is `guidance/the-shape.md` §2 stated as a test — two copies of a fact —
    rather than a proxy for it.
    """
    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import _psalms  # noqa: PLC0415

    # WHICH KIND OF OTHER SYSTEM THIS IS, asked of the module that owns it.
    # A psalter numbering is a numbering: hebrew Psalm 51 IS vulgate Psalm 50,
    # §8 says "one psalm with one chronology", and any fact about one is a fact
    # about the other. A deuterocanon witness is a WITNESS: §3.2 settles that
    # for Sirach "there are two texts, not two numberings", so a fact about the
    # Greek translation is not thereby a fact about the Latin, even at a verse
    # where the two correspond. The gate must not treat these alike, and asking
    # the owning module is how the answer stays where the machinery is.
    renumberings = {name for name in _psalms.SYSTEMS if name != PREFERRED_SYSTEM}

    preferred_units = [
        unit for unit in units.values()
        if any(span.system == PREFERRED_SYSTEM for span in unit.scope)
    ]
    preferred_bindings = [
        binding for binding in bindings
        if any(span.system == PREFERRED_SYSTEM for span in binding.scope)
    ]

    def already_held(reached: Locus, relation: str) -> set[str]:
        """Rendered claims of `relation` the preferred locus already carries."""
        held: set[str] = set()
        for unit in preferred_units:
            if unit.relation != relation:
                continue
            if _scope_covers(
                [s for s in unit.scope if s.system == PREFERRED_SYSTEM],
                reached.token, reached.chapter, reached.verse,
            ):
                held.update(str(claim.date) for claim in unit.claims)
        for binding in preferred_bindings:
            if binding.relation != relation:
                continue
            if _scope_covers(
                [s for s in binding.scope if s.system == PREFERRED_SYSTEM],
                reached.token, reached.chapter, reached.verse,
            ):
                held.add(binding.event)
        return held

    scoped: list[tuple[str, str, str, tuple[Span, ...], tuple[str, ...]]] = [
        *(
            ("composition unit", unit.id, unit.relation, unit.scope,
             tuple(str(claim.date) for claim in unit.claims))
            for unit in units.values()
        ),
        *(
            ("binding", f"{binding.relation} -> {binding.event}",
             binding.relation, binding.scope, (binding.event,))
            for binding in bindings
        ),
        *(("gap", f"{gap.status}", "", gap.scope, ()) for gap in gaps),
    ]
    for kind, identifier, relation, scope, mine in scoped:
        for span in scope:
            if span.system == PREFERRED_SYSTEM:
                continue
            shared: list[tuple[str, str]] = []
            duplicated: list[tuple[str, str, str]] = []
            for token, chapter, verse in _span_loci(span):
                reached = to_canonical(span.system, token, chapter, verse)
                if isinstance(reached, Unresolved):
                    continue
                shared.append((f"{token} {chapter}:{verse}", str(reached)))
                if span.system in renumberings:
                    # Same text under another number. Nothing further to ask.
                    duplicated.append(
                        (f"{token} {chapter}:{verse}", str(reached),
                         "the same text under another number")
                    )
                    continue
                if not relation:
                    # A gap row restates nothing; any safe correspondence means
                    # the status belongs at the preferred locus.
                    duplicated.append((f"{token} {chapter}:{verse}", str(reached), ""))
                    continue
                overlap = already_held(reached, relation) & set(mine)
                for item in sorted(overlap):
                    duplicated.append(
                        (f"{token} {chapter}:{verse}", str(reached), item)
                    )
            if not duplicated:
                continue
            here, there, what = duplicated[0]
            spread = (
                f" {len(shared)} of this scope's loci correspond safely and "
                f"{len(duplicated)} of those would duplicate; if that is a "
                f"property of part of the span only, split the span."
                if len(shared) > 1 else ""
            )
            raise ChronologyError(
                f"{where}: {kind} {identifier} authors chronology natively at "
                f"{span.system} {here}, the concordance carries that locus "
                f"safely to {there}, and the preferred locus already holds "
                f"{what!r} under {relation!r}. A fact true of both texts is "
                f"authored once, at the preferred {PREFERRED_SYSTEM} locus, and "
                f"reached from here through the concordance.{spread}"
            )


def _span_loci(span: Span) -> list[tuple[str, int, int]]:
    """Every locus a native span covers, read from the witness that prints it.

    A span is validated over its whole extent or it is not validated. Returning
    the printed loci rather than an integer range is the same rule `_system_loci`
    obeys, and for the same reason: a verse number no witness prints is not a
    locus, and probing one proves nothing about the text.
    """
    printed = _system_loci(span.system)
    if printed is None:
        return []
    out = []
    for token, chapter, verse in printed:
        if token != span.token:
            continue
        if span.chapter is not None and chapter != span.chapter:
            continue
        if span.first is not None and verse < span.first:
            continue
        if span.last is not None and verse > span.last:
            continue
        out.append((token, chapter, verse))
    return out


def _refuse_dangling_anchors(
    events: dict[str, Event], units: dict[str, Unit], where: Path
) -> None:
    """Every named date anchor must be a chronology subject this corpus holds.

    This applies both to relative offsets and to anchor-backed one-sided
    boundaries. Where a relative claim and its anchor's refused date come out
    of one source record, the anchor must additionally be something this
    profile actually answers with.

    Found by an author, not by a test: a claim reading "forty years after
    <event>" loaded cleanly and audited cleanly while naming an event that did
    not exist, so the date said nothing and said it in well-formed YAML. That
    is `guidance/the-shape.md` §1 inside the apparatus built to catch it, and
    it is checked here rather than in the audit because a dangling anchor is a
    structural defect and not a question about the rest of the repository.

    THE SECOND REFUSAL is the same defect one level up, and the corpus met it at
    `israel.patriarchs.abram-contact-with-egypt-and-elam`. One sentence of the
    Catholic Encyclopedia said that Abram "appears to have reached Chanaan about
    2300 B.C., when he came into passing contact with Egypt (Genesis 12) and
    Elam (Genesis 14)". The corpus refused the year, on Sayce's Babylonian
    synchronism, and preserved it on the arrival. It then went on ANSWERING with
    the rest of that same sentence, as a relative claim measured to the arrival
    it had just refused to date — and the interval it stated was the event
    restated, so thirty-five verses of Genesis reported status `dated` on a
    tautology whose only chronological content was the excluded number.

    So the refusal is narrow and says exactly that: an ANSWERABLE relative claim
    whose anchor holds claims, none of them answerable, and which cites a source
    record one of those refused claims also cites. That is the corpus answering
    with one half of a source statement whose other half it refused, where the
    half it answers with is only a position measured to the half it refused.

    WHAT IT DELIBERATELY DOES NOT REFUSE, because refusing it would be wrong:
    a relative claim anchored on a subject the corpus openly does not date at
    all. `israel.monarchy.saul-accession` holds no answerable claim and three
    claims are measured from it — the private anointing, the deliverance of
    Jabes Galaad, and the writing of Judges — and two of those three are rank-1
    Scriptural relations, which this profile's authority list puts FIRST:
    "Scripture's own chronological and RELATIONAL statements". "About a month
    after this" is chronology, and it is chronology whether or not anyone can
    say which year the month fell in. A rule refusing those would refuse the
    thing the profile ranks highest in order to catch a tautology, so it does
    not; what makes the Abram case different is not that the anchor is undated
    but that the claim and the anchor's refused figure are one source statement.
    """
    known = {**events, **units}
    for kind, holder in (
        *(("event", event) for event in events.values()),
        *(("composition unit", unit) for unit in units.values()),
    ):
        for claim in holder.claims:
            # A duration names no anchor, but it may say what it sits inside,
            # and a containment that names nothing is as empty as an offset
            # that does. Checked here for the same reason: it is structural.
            containing = (claim.date.duration or {}).get("within")
            if containing is not None and containing not in known:
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} states a duration within "
                    f"{containing!r}, which is neither an event nor a "
                    f"composition unit this corpus holds; a span contained by "
                    f"nothing is not contained"
                )
            boundary_anchor = (claim.date.boundary or {}).get("anchor")
            if boundary_anchor is not None and boundary_anchor not in known:
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} is bounded relative to "
                    f"{boundary_anchor!r}, which is neither an event nor a "
                    f"composition unit this corpus holds; a one-sided "
                    f"position bounded by nothing states nothing"
                )
            relative = claim.date.relative
            if not relative:
                continue
            anchor = relative.get("of")
            if anchor not in known:
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} is dated relative to "
                    f"{anchor!r}, which is neither an event nor a composition "
                    f"unit this corpus holds; a date measured from nothing "
                    f"states nothing"
                )
            unknown = set(relative) - {"of", "statement", "note"}
            if unknown:
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} relative date: unknown "
                    f"key(s) {sorted(unknown)}"
                )
            if not relative.get("statement"):
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} is dated relative to "
                    f"{anchor} without saying what the interval is"
                )
            if claim.answerability != "answerable":
                continue
            anchored = known[anchor]
            if not anchored.claims:
                continue
            if any(other.answerability == "answerable" for other in anchored.claims):
                continue
            shared = sorted(
                set(claim.sources).intersection(
                    source for other in anchored.claims for source in other.sources
                )
            )
            if shared:
                raise ChronologyError(
                    f"{where}: {kind} {holder.id} answers with a date relative "
                    f"to {anchor}, whose every claim this profile refuses, on "
                    f"the same source record(s) {shared}; the corpus would be "
                    f"answering with one half of a source statement whose other "
                    f"half it withdrew, and the half it answers with is only a "
                    f"position measured to the half it withdrew. Preserve it "
                    f"too, or ground it on a source that dates it independently"
                )


# --- Reaching the corpus from another system --------------------------------


def to_canonical(system: str, token: str, chapter: int, verse: int) -> Locus | Unresolved:
    """Convert an asking system's locus into the one chronology is authored in.

    Only through a concordance that already exists and already refuses. There
    is deliberately no general reverse projection here: `_projection` runs
    canonical -> edition, and inventing the inverse would produce a plausible
    locus wherever the real answer is that two traditions carry different text.
    """
    if system == CANONICAL_SYSTEM:
        return Locus(CANONICAL_SYSTEM, token, chapter, verse)

    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)

    if token == "Ps":
        import _psalms  # noqa: PLC0415

        if system not in _psalms.SYSTEMS:
            return Unresolved(
                "not-alignable",
                f"{system!r} is not a psalm numbering this repository records",
            )
        try:
            moved_chapter, moved_verse, note = _psalms.convert_point(
                chapter, verse, system, CANONICAL_SYSTEM
            )
        except _psalms.NumberingError as error:
            return Unresolved("not-alignable", str(error))
        if moved_chapter is None or moved_verse is None:
            return Unresolved("not-alignable", note or "no correspondence recorded")
        return Locus(CANONICAL_SYSTEM, token, moved_chapter, moved_verse)

    import _deuterocanon  # noqa: PLC0415

    if token in _deuterocanon.BOOKS:
        # Not a blanket refusal. The concordance knows where a correspondence
        # was established and where one was looked for and not found, and those
        # are different answers: Ecclesiasticus is `not-recorded` for the whole
        # book because the Latin and the Greek are independent translations out
        # of two languages, while Daniel and Esther have real rows in places.
        # Refusing everything would hide which of the two a caller had hit.
        # ROUTE MATTERS. `convert_verse` asks for a direct row, and the direct
        # World-English-Catholic-to-Vulgate index is empty: that edition is two
        # hops from the Vulgate, through the Greek, and `_deuterocanon`'s own
        # docstring says `convert_through` "is the only way to reach it without
        # a second table saying the same thing twice". Asking the wrong way
        # returned `textually-distinct` for every one of its loci — a refusal
        # asserted by taking the wrong road, which under the corrected coverage
        # rules would have counted them all as new Scripture. (The count then
        # given was 2 131, the densified figure; the witness prints 2 094.)
        hops = (
            (system, "greek", PREFERRED_SYSTEM)
            if system == "world-english-catholic"
            else (system, PREFERRED_SYSTEM)
        )
        try:
            moved, reason = _deuterocanon.convert_through(
                token, chapter, verse, hops
            )
        except _deuterocanon.NumberingError as error:
            return Unresolved("not-alignable", str(error))
        if moved is None:
            return Unresolved("textually-distinct", reason)
        if moved.first != moved.last:
            # A run, not a point. Returning its first verse would answer about
            # one verse of several without saying so.
            return Unresolved(
                "textually-distinct",
                f"{token} {chapter}:{verse} in {system} is "
                f"{moved.book} {moved.chapter}:{moved.first}-{moved.last} in "
                f"{CANONICAL_SYSTEM}, which is more than one verse: {reason}",
            )
        return Locus(CANONICAL_SYSTEM, moved.book, moved.chapter, moved.first)
    return Unresolved(
        "not-alignable",
        f"no concordance between {system!r} and {CANONICAL_SYSTEM!r} is "
        f"recorded for {token}",
    )


# --- Query ------------------------------------------------------------------


def _covers(span: Span, token: str, chapter: int, verse: int) -> bool:
    if span.token != token:
        return False
    if span.chapter is None:
        return True
    if span.chapter != chapter:
        return False
    if span.first is not None and verse < span.first:
        return False
    if span.last is not None and verse > span.last:
        return False
    return True


def _scope_covers(scope: tuple[Span, ...], token: str, chapter: int, verse: int) -> Span | None:
    for span in scope:
        if _covers(span, token, chapter, verse):
            return span
    return None


def _scope_text(scope: tuple[Span, ...]) -> str:
    return " ".join(str(span) for span in scope)


@lru_cache(maxsize=4)
def _by_book(root: Path | None) -> dict[str, tuple[tuple, tuple, tuple]]:
    """Units, bindings and gaps grouped by book token.

    Coverage asks every one of the canonical edition's 35 809 verses, and a
    linear scan of the whole corpus per verse is the difference between a check
    that runs in a gate and one nobody runs.
    """
    corpus = load(root)
    index: dict[str, list[list]] = {}
    for token in corpus.books:
        index[token] = [[], [], []]
    for unit in corpus.units.values():
        for token in {span.token for span in unit.scope}:
            # This index serves the preferred canonical walk only. A native
            # witness may have arrangement-only book tokens such as Greek
            # `Sus` and `Bel`; those units are gathered by
            # `_native_assertions()` before conversion and have no entry in
            # the canonical book dictionary.
            if token in index:
                index[token][0].append(unit)
    for binding in corpus.bindings:
        for token in {span.token for span in binding.scope}:
            if token in index:
                index[token][1].append(binding)
    for gap in corpus.gaps:
        for token in {span.token for span in gap.scope}:
            if token in index:
                index[token][2].append(gap)
    return {
        token: (tuple(units), tuple(bindings), tuple(gaps))
        for token, (units, bindings, gaps) in index.items()
    }


def _status_of(assertions: Iterable[Assertion]) -> str:
    """APPLICABILITY, NOT DIRECTNESS — the one place that decides it.

    Whether a substantive assertion reaches this verse is one question; whether
    it was authored at this verse or at a scope containing it is another, and
    the second rides on each returned assertion as `inherited`. The old rule
    asked the second and answered the first with it, which said two wrong
    things at once: a whole-book `prophecy-given` over Ezechiel left 271 verses
    looking undated though the oracle applies to every one of them, and a
    directly authored composition unit alone would have made a verse "dated"
    though nothing had dated an event it tells of.

    Textual attestation is separated once more inside textual history: it
    proves only that a dated witness contains the text. Calling that
    `composition-only` would imply precisely the writing claim its relation was
    introduced not to make.
    """
    relations = {item.relation for item in assertions}
    if any(relation not in TEXTUAL_RELATIONS for relation in relations):
        return "dated"
    if relations == {"textual-attestation"}:
        return "attestation-only"
    return "composition-only"


def _profile_order(corpus: Corpus, requested: str) -> tuple[str, ...]:
    """The leaf evidence profiles a request may consult, in order."""
    if requested in corpus.policies:
        return (requested,)
    cascade = corpus.cascades.get(requested)
    if cascade is not None:
        return cascade.fallback_profiles
    raise ChronologyError(
        f"profile {requested!r} is not declared; choose from "
        f"{sorted(corpus.profiles)}"
    )


def _select_assertions(
    corpus: Corpus,
    assertions: Iterable[Assertion],
    requested: str,
    evidence: bool,
) -> tuple[tuple[Assertion, ...], tuple[tuple[str, str], ...]]:
    """Apply one evidence profile or a relation-wise ordered cascade.

    Only answerable candidates decide which cascade leaf wins. Preserved
    evidence cannot block fallback. Once a leaf wins a relation, evidence mode
    may show that leaf's preserved claims beside its answers, exactly as it
    does for an explicit leaf-profile query; suppressed fallback profiles stay
    available by querying them explicitly.
    """
    gathered = tuple(assertions)
    order = _profile_order(corpus, requested)

    def without_redundant_attestation(
        selected: Iterable[Assertion], resolved: Iterable[tuple[str, str]]
    ) -> tuple[tuple[Assertion, ...], tuple[tuple[str, str], ...]]:
        selected_tuple = tuple(selected)
        resolved_tuple = tuple(resolved)
        if any(
            item.relation != "textual-attestation"
            and corpus.answers_with(item.claim)
            and is_positional_date(item.claim.date)
            for item in selected_tuple
        ):
            selected_tuple = tuple(
                item for item in selected_tuple
                if item.relation != "textual-attestation"
            )
            resolved_tuple = tuple(
                item for item in resolved_tuple
                if item[0] != "textual-attestation"
            )
        return (
            tuple(sorted(selected_tuple, key=lambda item: item.sort_key())),
            resolved_tuple,
        )

    if requested in corpus.policies:
        answerable = tuple(
            item for item in gathered
            if item.claim.profile == requested and corpus.answers_with(item.claim)
        )
        selected = tuple(
            item for item in gathered
            if item.claim.profile == requested
            and (evidence or corpus.answers_with(item.claim))
        )
        resolved = tuple(
            (relation, requested)
            for relation in RELATIONS
            if any(item.relation == relation for item in answerable)
        )
        return without_redundant_attestation(selected, resolved)

    selected: list[Assertion] = []
    resolved: list[tuple[str, str]] = []
    for relation in RELATIONS:
        for leaf in order:
            answerable = [
                item for item in gathered
                if item.relation == relation
                and item.claim.profile == leaf
                and corpus.answers_with(item.claim)
            ]
            if not answerable:
                continue
            resolved.append((relation, leaf))
            if evidence:
                selected.extend(
                    item for item in gathered
                    if item.relation == relation and item.claim.profile == leaf
                )
            else:
                selected.extend(answerable)
            break
    if evidence:
        # Evidence is an audit request, not a fallback vote. Preserved claims
        # from an earlier leaf must remain inspectable even though they cannot
        # stop the cascade from choosing a later answerable profile.
        held = {
            (item.relation, item.subject, item.claim.profile, str(item.claim.date))
            for item in selected
        }
        selected.extend(
            item for item in gathered
            if item.claim.profile in order
            and not corpus.answers_with(item.claim)
            and (
                item.relation, item.subject, item.claim.profile,
                str(item.claim.date),
            ) not in held
        )
    return without_redundant_attestation(selected, resolved)


def _gap_for(
    corpus: Corpus, locus: Locus, requested: str
) -> Gap | None:
    """The first leaf-profile gap after every cascade candidate was empty."""
    for leaf in _profile_order(corpus, requested):
        for gap in corpus.gaps:
            if gap.profile != leaf:
                continue
            if _scope_covers(
                [span for span in gap.scope if span.system == locus.system],
                locus.token, locus.chapter, locus.verse,
            ):
                return gap
    return None


def _candidates(
    corpus: Corpus,
    claims: Iterable[Claim],
    profile: str | None,
    evidence: bool,
) -> Iterable[Claim]:
    """The claims a query may return, gated BEFORE anything is ordered.

    THE STRUCTURAL EXCLUSION. `guidance/scripture-chronology.md` §4.5: a
    chronology value is a candidate answer only where both the source and the
    basis of that value are admissible under the profile, and the profile
    decides it — here, in code, at the one point where a stored claim becomes a
    returned assertion. Every gathering loop in this module goes through this
    function, so there is no second path by which a preserved figure reaches a
    default consumer.

    It runs BEFORE RANK. Nothing above has consulted the authority hierarchy or
    the disposition yet; `sort_key` orders what comes out of here, and ordering
    is the only thing rank does. An inadmissible basis therefore cannot be
    rescued by the rank of the work that printed it, at any rank.

    `evidence` opens the provenance/audit surface, which is a DIFFERENT
    QUESTION from what the corpus answers with: what did this source print, and
    what did this corpus decide about it. A caller has to ask for it, which is
    the difference between preserved evidence and a note asking not to be
    believed.
    """
    for claim in claims:
        if profile and claim.profile != profile:
            continue
        if not evidence and not corpus.answers_with(claim):
            continue
        yield claim


def _native_assertions(
    corpus: Corpus, locus: Locus, profiles: tuple[str, ...]
) -> tuple[Assertion, ...]:
    """What was authored in the asked locus's OWN system, at its own locus.

    Only scopes that name this system are consulted. A Vulgate scope is not
    silently reused here: if the two texts corresponded safely the load-time
    gate would have refused the native scope, so anything reached from here is
    a fact about this text and about no other.
    """
    found: list[Assertion] = []
    best: dict[tuple[str, str], tuple[Unit, Span]] = {}
    requested_profiles = frozenset(profiles)
    for unit in corpus.units.values():
        span = _scope_covers(
            [s for s in unit.scope if s.system == locus.system],
            locus.token,
            locus.chapter,
            locus.verse,
        )
        if span is None:
            continue
        for profile in (
            {claim.profile for claim in unit.claims} & requested_profiles
        ):
            key = (unit.relation, profile)
            held = best.get(key)
            if held is None or unit.width() > held[0].width():
                best[key] = (unit, span)
    for (_relation, profile), (unit, span) in best.items():
        for claim in unit.claims:
            if claim.profile != profile:
                continue
            found.append(
                Assertion(
                    relation=unit.relation,
                    subject=unit.id,
                    title=unit.title,
                    claim=claim,
                    inherited=span.first is None or span.chapter is None,
                    scope=_scope_text(unit.scope),
                )
            )
    for binding in corpus.bindings:
        span = _scope_covers(
            [s for s in binding.scope if s.system == locus.system],
            locus.token,
            locus.chapter,
            locus.verse,
        )
        if span is None:
            continue
        event = corpus.events[binding.event]
        for claim in event.claims:
            if claim.profile not in profiles:
                continue
            found.append(
                Assertion(
                    relation=binding.relation,
                    subject=event.id,
                    title=event.title,
                    claim=claim,
                    inherited=span.first is None and span.last is None,
                    scope=_scope_text(binding.scope),
                )
            )
    found.sort(key=lambda item: item.sort_key())
    return tuple(found)


def _broad_preferred_assertions(
    corpus: Corpus, locus: Locus, profiles: tuple[str, ...], root: Path | None
) -> tuple[Assertion, ...]:
    """Claims safe at a Psalm whose exact preferred verse segmentation fails.

    `_psalms` establishes the Psalm identity, but its point mapping was built
    against Douay verse extents and a few targets are not verse addresses the
    preferred latVUC witness prints. A whole-book or whole-chapter assertion is
    still true of that Psalm; a verse-scoped assertion is not safe without an
    exact text correspondence and is deliberately excluded here.
    """
    units, bindings, _gaps = _by_book(root)[locus.token]
    requested_profiles = frozenset(profiles)
    best: dict[tuple[str, str], tuple[Unit, Span]] = {}

    def broad_span(scope: tuple[Span, ...]) -> Span | None:
        for span in scope:
            if span.system != PREFERRED_SYSTEM or span.token != locus.token:
                continue
            if span.chapter is None:
                return span
            if (
                span.chapter == locus.chapter
                and span.first is None
                and span.last is None
            ):
                return span
        return None

    for unit in units:
        span = broad_span(unit.scope)
        if span is None:
            continue
        for leaf in {claim.profile for claim in unit.claims} & requested_profiles:
            key = (unit.relation, leaf)
            held = best.get(key)
            if held is None or unit.width() > held[0].width():
                best[key] = (unit, span)

    found: list[Assertion] = []
    for (_relation, leaf), (unit, _span) in best.items():
        for claim in unit.claims:
            if claim.profile != leaf:
                continue
            found.append(
                Assertion(
                    unit.relation, unit.id, unit.title, claim,
                    inherited=True, scope=_scope_text(unit.scope),
                )
            )
    for binding in bindings:
        if broad_span(binding.scope) is None:
            continue
        event = corpus.events[binding.event]
        for claim in event.claims:
            if claim.profile not in requested_profiles:
                continue
            found.append(
                Assertion(
                    binding.relation, event.id, event.title, claim,
                    inherited=True, scope=_scope_text(binding.scope),
                )
            )
    return tuple(sorted(found, key=lambda item: item.sort_key()))


def chronology(
    locus: Locus | str,
    *,
    profile: str | None = None,
    root: Path | None = None,
    evidence: bool = False,
) -> Answer | Unresolved:
    """Everything the corpus ANSWERS WITH about one verse, in a stable order.

    Returns EVERY applicable candidate assertion. It never picks one when
    alternatives exist: `guidance/the-shape.md` §5 is that a tool which always
    answers lies when it does not know, and choosing silently between two
    traditional dates is the same lie with better manners.

    "Every applicable" is not "everything stored". A claim reaches this set only
    where the profile it was authored under answers with it -- both the source
    and the basis of that particular value admissible under the profile -- and
    `_candidates` is the single gate. `evidence=True` opens the provenance and
    audit surface and returns preserved evidence beside the answers, which is
    the only way to see it and is never what a default consumer gets.
    """
    corpus = load(root)
    if isinstance(locus, str):
        locus = parse_locus(locus)
    asked_locus = locus

    requested_profile = profile or corpus.default_profile
    profile_order = _profile_order(corpus, requested_profile)

    asked = str(locus)
    mapping: Mapping | None = None
    native: tuple[Assertion, ...] = ()
    native_loci: list[Locus] = [locus]
    if locus.system != PREFERRED_SYSTEM:
        systems = scripture_systems()
        if locus.system not in systems:
            return Unresolved(
                "not-alignable",
                f"{locus.system!r} is not a Scripture system this repository "
                f"has machinery for; the systems are {sorted(systems)}",
                asked,
            )
        addressable = systems[locus.system]
        if addressable is not None and locus.token not in addressable:
            return Unresolved(
                "not-alignable",
                f"{locus.system!r} does not number {locus.token!r}; it "
                f"addresses {sorted(addressable)}",
                asked,
            )
        printed = _system_locus_membership(locus.system)
        if printed is None:
            return Unresolved(
                "not-alignable",
                f"{locus.system!r} has no tracked witness or concordance that "
                f"enumerates its loci",
                asked,
            )
        if (locus.token, locus.chapter, locus.verse) not in printed:
            return Unresolved(
                "not-alignable",
                f"{asked} is not a locus printed by the tracked "
                f"{locus.system!r} witness",
                asked,
            )

        # NATIVE FIRST, and this ordering is the correction. What the corpus
        # authored AT this locus is true of this locus whatever the concordance
        # can or cannot carry, so it is gathered before the mapping is even
        # attempted. The old code asked the concordance first and returned its
        # refusal, which threw away chronology that was sitting right there.
        # A WEC deuterocanonical locus may be the same text as a Greek locus
        # even where that Greek locus cannot be carried onward to the Vulgate.
        # Gather chronology at every exact hop reached, not only at the final
        # preferred-system destination. Coverage already deduplicates those
        # loci as one text; query must not call the address unresearched while
        # the chronology is sitting at its safe intermediate counterpart.
        if locus.system == "world-english-catholic":
            import _deuterocanon  # noqa: PLC0415

            if locus.token in _deuterocanon.BOOKS:
                try:
                    intermediate, intermediate_problem = _deuterocanon.convert_verse(
                        locus.token, locus.chapter, locus.verse,
                        "world-english-catholic", "greek",
                    )
                except _deuterocanon.NumberingError:
                    intermediate = None
                    intermediate_problem = ""
                if (
                    intermediate is not None
                    and not intermediate_problem
                    and intermediate.first == intermediate.last
                ):
                    native_loci.append(
                        Locus(
                            "greek", intermediate.book, intermediate.chapter,
                            intermediate.first,
                        )
                    )
        native = tuple(
            item
            for native_locus in native_loci
            for item in _native_assertions(corpus, native_locus, profile_order)
        )

        converted = to_canonical(locus.system, locus.token, locus.chapter, locus.verse)
        if isinstance(converted, Unresolved):
            mapping = Mapping(locus.system, converted.status, None, converted.reason)
            selected, resolved_profiles = _select_assertions(
                corpus, native, requested_profile, evidence
            )
            answerable_selected = tuple(
                item for item in selected if corpus.answers_with(item.claim)
            )
            if answerable_selected:
                # Both true at once: this text has chronology, and it may not
                # be asserted equivalent to the Vulgate's. The status is
                # computed by the same rule the shared path uses, so a native
                # locus carrying composition is composition-only and one
                # carrying only a dated witness is attestation-only here
                # exactly as either would be on the shared path.
                return Answer(
                    locus, selected, _status_of(answerable_selected), "", mapping, asked,
                    requested_profile, resolved_profiles,
                )
            # A MAPPING WORD IS NOT A CHRONOLOGY STATUS, and returning the
            # refusal here made it one. §3.0.1 separated the two axes for the
            # locus that HAS chronology and left the locus that has none still
            # answering `textually-distinct` to the question "is this dated?".
            # The cold audit found ten loci in that position with no route to
            # anything else. The mapping refusal keeps its own axis, and the
            # chronology axis answers the way every other unresolved locus in
            # the corpus does — from an authored gap row if one reaches it, and
            # otherwise from the honest default, which §9 says is not authored.
            for native_locus in native_loci:
                gap = _gap_for(corpus, native_locus, requested_profile)
                if gap is not None:
                    return Answer(
                        locus, selected, gap.status, gap.reason, mapping, asked,
                        requested_profile, resolved_profiles,
                    )
            return Answer(
                locus,
                selected,
                "research-pending",
                "no ranked source has been inspected for this locus yet",
                mapping,
                asked,
                requested_profile,
                resolved_profiles,
            )
        mapping = Mapping(locus.system, "shared", str(converted), "")
        locus = converted
        # A SAFE CORRESPONDENCE IS NOT AN ERASURE. Where the asked locus also
        # carries chronology authored in its own system, that fact is true of
        # this text whether or not the concordance can carry the locus, and it
        # is carried forward to be merged with the shared answer below. The
        # previous code computed `native` here and then dropped it, so at the
        # one locus where the Greek Ecclesiasticus corresponds safely to the
        # Vulgate the Greek translation's own date became unreachable — the
        # same shape as the refusal-swallows-chronology defect §3.0.1 was
        # written to end, arriving from the other side.
    if locus.token not in corpus.books:
        return Unresolved(
            "not-alignable",
            f"{locus.token!r} is not a book of the canon",
            str(locus),
        )
    if not 1 <= locus.chapter <= corpus.books[locus.token]:
        return Unresolved(
            "not-alignable",
            f"{locus.token} has {corpus.books[locus.token]} chapters; "
            f"{locus.chapter} is not one",
            str(locus),
        )
    ceiling = verse_counts()[(locus.token, locus.chapter)]
    if not 1 <= locus.verse <= ceiling:
        if asked_locus.system != PREFERRED_SYSTEM:
            # The Psalm concordance establishes which Psalm this is, but its
            # point rows were derived from Douay verse extents. At the handful
            # of places where the tracked Clementine witness segments that
            # Psalm differently, the converted number is not an address in
            # the preferred witness. Keep the original address as the answer's
            # identity and the failed target on the mapping axis. Whole-Psalm
            # chronology remains safe; verse-scoped chronology does not.
            mapping = Mapping(
                asked_locus.system,
                "not-alignable",
                None,
                f"{asked} converts to preferred {locus}, but "
                f"{locus.token}.{locus.chapter} prints verses 1-{ceiling} in "
                f"the tracked preferred witness; only whole-Psalm chronology "
                f"is retained and no verse-scoped assertion is transferred",
            )
            broad = (
                _broad_preferred_assertions(corpus, locus, profile_order, root)
                if asked_locus.token == "Ps"
                else ()
            )
            gathered = list(broad)
            held = {
                (item.relation, item.subject, item.claim.profile, str(item.claim.date))
                for item in gathered
            }
            gathered.extend(
                item for item in native
                if (
                    item.relation, item.subject, item.claim.profile,
                    str(item.claim.date),
                ) not in held
            )
            selected, resolved_profiles = _select_assertions(
                corpus, gathered, requested_profile, evidence
            )
            answerable_selected = tuple(
                item for item in selected if corpus.answers_with(item.claim)
            )
            if answerable_selected:
                return Answer(
                    asked_locus,
                    selected,
                    _status_of(answerable_selected),
                    "",
                    mapping,
                    asked,
                    requested_profile,
                    resolved_profiles,
                )
            for candidate in (asked_locus, locus):
                gap = _gap_for(corpus, candidate, requested_profile)
                if gap is not None:
                    return Answer(
                        asked_locus,
                        selected,
                        gap.status,
                        gap.reason,
                        mapping,
                        asked,
                        requested_profile,
                        resolved_profiles,
                    )
            return Answer(
                asked_locus,
                selected,
                "research-pending",
                "no ranked source has been inspected for this locus yet",
                mapping,
                asked,
                requested_profile,
                resolved_profiles,
            )
        return Unresolved(
            "not-alignable",
            f"{locus.token}.{locus.chapter} has verses 1-{ceiling} in the "
            f"tracked preferred witness; {locus.verse} is not one",
            asked,
        )

    units, bindings, gaps = _by_book(root)[locus.token]
    assertions: list[Assertion] = []

    # Composition, by inheritance: the narrowest unit covering the verse wins,
    # and equal widths were refused at load time rather than broken here.
    #
    # THE SCOPE RULE IS NOT THE ANSWERABILITY RULE, and it is applied first on
    # purpose. A narrower unit exists because that text has its own composition
    # history, so if its claims are all preserved the verse gets no composition
    # date rather than the containing book's: falling back would assert the
    # book's date over a text the corpus has said is not dated by it, which is a
    # date resolving successfully and wrongly. An author withdrawing a unit's
    # last answerable claim is saying the unit's own chronology is unsettled,
    # and `research-pending` is the honest answer to that.
    best: dict[tuple[str, str], tuple[Unit, Span]] = {}
    requested_profiles = frozenset(profile_order)
    for unit in units:
        # Only scopes in the system being asked about. A native Greek scope is
        # a fact about the Greek text; letting it answer a Vulgate query would
        # be the duplication the load-time gate exists to prevent, arriving
        # through the back door.
        span = _scope_covers(
            [s for s in unit.scope if s.system == locus.system],
            locus.token,
            locus.chapter,
            locus.verse,
        )
        if span is None:
            continue
        # Specificity is meaningful only within one leaf evidence profile.
        # A narrower traditional unit says nothing about whether a broader
        # critical unit applies, and must not erase it before the cascade gets
        # the chance to choose between those profiles.
        for profile in (
            {claim.profile for claim in unit.claims} & requested_profiles
        ):
            key = (unit.relation, profile)
            held = best.get(key)
            if held is None or unit.width() > held[0].width():
                best[key] = (unit, span)
    for (_relation, profile), (unit, best_span) in best.items():
        for claim in unit.claims:
            if claim.profile != profile:
                continue
            assertions.append(
                Assertion(
                    relation=unit.relation,
                    subject=unit.id,
                    title=unit.title,
                    claim=claim,
                    inherited=best_span.first is None or best_span.chapter is None,
                    scope=_scope_text(unit.scope),
                )
            )

    # Events, by binding. One event, dated once, reached from every locus bound
    # to it under whichever relation that locus stands in to it.
    for binding in bindings:
        span = _scope_covers(
            [s for s in binding.scope if s.system == locus.system],
            locus.token,
            locus.chapter,
            locus.verse,
        )
        if span is None:
            continue
        event = corpus.events[binding.event]
        for claim in event.claims:
            if claim.profile not in profile_order:
                continue
            assertions.append(
                Assertion(
                    relation=binding.relation,
                    subject=event.id,
                    title=event.title,
                    claim=claim,
                    inherited=span.first is None and span.last is None,
                    scope=_scope_text(binding.scope),
                )
            )

    if native:
        held = {
            (item.relation, item.subject, item.claim.profile, str(item.claim.date))
            for item in assertions
        }
        assertions.extend(
            item for item in native
            if (
                item.relation, item.subject, item.claim.profile,
                str(item.claim.date),
            ) not in held
        )
    selected, resolved_profiles = _select_assertions(
        corpus, assertions, requested_profile, evidence
    )
    answerable_selected = tuple(
        item for item in selected if corpus.answers_with(item.claim)
    )

    if answerable_selected:
        # APPLICABILITY, NOT DIRECTNESS. Whether a substantive assertion reaches
        # this verse is one question; whether it was authored at this verse or
        # at a scope containing it is another, and the second is provenance that
        # rides on each returned assertion. The old rule asked the second and
        # answered the first with it, which said two wrong things at once: a
        # whole-book `prophecy-given` over Ezechiel left eight and a half
        # chapters looking undated though the oracle applies to every verse in
        # its scope, and a directly authored composition unit alone made a verse
        # "dated" though nothing had dated an event it tells of.
        return Answer(
            locus, selected, _status_of(answerable_selected), "", mapping, asked,
            requested_profile, resolved_profiles,
        )

    gap = _gap_for(corpus, locus, requested_profile)
    if gap is not None:
        return Answer(
            locus, selected, gap.status, gap.reason, mapping, asked,
            requested_profile, resolved_profiles,
        )
    return Answer(
        locus,
        selected,
        "research-pending",
        "no ranked source has been inspected for this locus yet",
        mapping,
        asked,
        requested_profile,
        resolved_profiles,
    )


# --- Coverage ---------------------------------------------------------------


@lru_cache(maxsize=2)
def verse_counts(root: Path | None = None) -> dict[tuple[str, int], int]:
    """How many verses each canonical chapter carries, read from the edition.

    The coverage universe is the canonical edition's own text and nothing else.
    A count typed beside it would be the second source of truth that
    `guidance/the-shape.md` §2 predicts will disagree, and the disagreement
    here would be a coverage percentage nobody could check.
    """
    import json as _json  # noqa: PLC0415
    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import _canon  # noqa: PLC0415

    base = Path(root) if root is not None else _canon.ROOT
    chapters = base / _canon.BIBLES_RELATIVE / _canon.CANONICAL_BIBLE / "chapters"
    counts: dict[tuple[str, int], int] = {}
    for book in _canon.books(base):
        token = book["token"]
        for chapter in range(1, int(book["chapters"]) + 1):
            path = chapters / token / f"{chapter}.json"
            if not path.exists():
                raise ChronologyError(
                    f"{path}: the canonical edition carries no such chapter, but "
                    f"its own book index counts it"
                )
            counts[(token, chapter)] = len(
                _json.loads(path.read_text(encoding="utf-8"))["verses"]
            )
    return counts


class Run(NamedTuple):
    """A maximal run of consecutive verses the corpus answers identically.

    Runs, not verses, for the reason `guidance/versification.md` §4 gives for
    the psalm concordance: a segment is the unit a reviewer can actually read,
    and enumerating verses would be an order of magnitude more rows carrying
    the same information while hiding the structure.
    """

    token: str
    chapter: int
    first: int
    last: int
    status: str
    relations: tuple[str, ...]
    subjects: tuple[str, ...]

    @property
    def verses(self) -> int:
        return self.last - self.first + 1


def _signature(answer: Answer | Unresolved) -> tuple:
    if isinstance(answer, Unresolved):
        return (answer.status, (), ())
    return (
        answer.status,
        tuple(sorted({item.relation for item in answer.assertions})),
        tuple(sorted({item.subject for item in answer.assertions})),
    )


def runs(root: Path | None = None, profile: str | None = None) -> list[Run]:
    """Every canonical verse, compressed into runs that answer alike."""
    counts = verse_counts()
    corpus = load(root)
    out: list[Run] = []
    for token in corpus.books:
        for chapter in range(1, corpus.books[token] + 1):
            open_run: list[Any] | None = None
            for verse in range(1, counts[(token, chapter)] + 1):
                answer = chronology(
                    Locus(CANONICAL_SYSTEM, token, chapter, verse),
                    profile=profile,
                    root=root,
                )
                signature = _signature(answer)
                if open_run is not None and open_run[0] == signature:
                    open_run[2] = verse
                    continue
                if open_run is not None:
                    out.append(
                        Run(token, chapter, open_run[1], open_run[2], *open_run[0])
                    )
                open_run = [signature, verse, verse]
            if open_run is not None:
                out.append(Run(token, chapter, open_run[1], open_run[2], *open_run[0]))
    return out


def _system_loci(system: str) -> list[tuple[str, int, int]] | None:
    """Every locus a named system prints, or None if it cannot be enumerated.

    None is a real answer and is reported as one. A system this repository can
    name but not enumerate cannot be honestly accounted for, and a coverage
    report that quietly omitted it would be claiming completeness over a
    universe it had not measured.
    """
    import sys as _sys  # noqa: PLC0415

    scripts = str(Path(__file__).resolve().parent)
    if scripts not in _sys.path:
        _sys.path.insert(0, scripts)
    import _deuterocanon  # noqa: PLC0415
    import _psalms  # noqa: PLC0415

    if system in _psalms.SYSTEMS and system != PREFERRED_SYSTEM:
        out = []
        for chapter in range(1, _psalms.LAST_PSALM + 1):
            low, high = _psalms._extent(chapter, system)
            out.extend(("Ps", chapter, verse) for verse in range(low, high + 1))
        return out
    if system in _deuterocanon.WITNESSES:
        try:
            printed = _deuterocanon._printed(system)
        except Exception:  # noqa: BLE001 - an unmeasurable system is a finding
            return None
        # THE VERSES THE WITNESS PRINTS, not the range they span. This used to
        # fill each chapter from `_extents`, which keeps only the first and last
        # number, so every verse number the witness SKIPS was invented back:
        # 38 in `greek`, 37 in `world-english-catholic`. The 35 invented Greek
        # Ecclesiasticus loci were exactly the Latin pluses the cited article
        # calls "foreign not only to the Greek, but also to the Hebrew text",
        # so the count turned Latin expansions into Greek Scripture and then
        # reported a date as applying to them. A universe is what a witness
        # holds, and only reading the witness can say what that is.
        return sorted(printed)
    return None


@lru_cache(maxsize=None)
def _system_locus_membership(
    system: str,
) -> frozenset[tuple[str, int, int]] | None:
    """Exact printed addresses for query validation, cached for verse walks."""
    loci = _system_loci(system)
    return frozenset(loci) if loci is not None else None


@lru_cache(maxsize=4)
def native_coverage(
    root: Path | None = None, profile: str | None = None
) -> dict[str, Any]:
    """Each named system beside the preferred one, counted without double-counting.

    A locus that the concordance carries safely to the Vulgate is NOT new
    Scripture — it is the same text under another number, and its chronology is
    held once at the preferred locus. Only loci the concordance refuses are
    additional content, and only those are counted here.
    """
    import _deuterocanon  # noqa: PLC0415

    out: dict[str, Any] = {}
    counted: list[str] = []

    # NAMED BUT UNENUMERABLE, reported rather than omitted. §9.3: "A system this
    # repository can name but cannot enumerate is reported as `enumerable:
    # false` and is a reason the coverage requirement stays open, not a thing to
    # leave out quietly." `_commentary` declares numbering systems a commentary
    # row may legally cite, three of which chronology has no concordance for.
    # Iterating only the systems with machinery left the report implying that
    # four names were all there were, and made the `enumerable: false` branch
    # below unreachable for the names it was written for.
    import _commentary  # noqa: PLC0415

    for system in sorted(getattr(_commentary, "NUMBERING_SYSTEMS", ())):
        if system == PREFERRED_SYSTEM or system in scripture_systems():
            continue
        out[system] = {
            "enumerable": False,
            "note": "this repository holds no concordance that enumerates this "
                    "system's loci, so its native universe cannot be honestly "
                    "accounted for; chronology may not be authored in it",
        }

    for system in sorted(scripture_systems()):
        if system == PREFERRED_SYSTEM:
            continue
        loci = _system_loci(system)
        if loci is None:
            out[system] = {
                "enumerable": False,
                "note": "this repository holds no witness that enumerates this "
                        "system's loci, so its native universe cannot be "
                        "honestly accounted for",
            }
            continue
        shared = 0
        already = 0
        additional = 0
        by_status: dict[str, int] = {}
        for token, chapter, verse in loci:
            reached = to_canonical(system, token, chapter, verse)
            if not isinstance(reached, Unresolved):
                shared += 1
                continue
            # It refuses the preferred system — but that does not make it new
            # text. The World English Catholic edition re-divides the GREEK,
            # and 2 088 of the 2 094 loci it prints reach it; counting those
            # again would be counting one text twice because two editions
            # number it differently, which is exactly what §9.2 forbids.
            elsewhere = False
            for prior in counted:
                if token not in (scripture_systems().get(prior) or ()):
                    continue
                try:
                    moved, _ = _deuterocanon.convert_through(
                        token, chapter, verse, (system, prior)
                    )
                except Exception:  # noqa: BLE001
                    moved = None
                if moved is not None:
                    elsewhere = True
                    break
            if elsewhere:
                already += 1
                continue
            additional += 1
            answer = chronology(
                Locus(system, token, chapter, verse), profile=profile, root=root
            )
            status = answer.status if isinstance(answer, Answer) else reached.status
            by_status[status] = by_status.get(status, 0) + 1
        out[system] = {
            "enumerable": True,
            "printed_loci": len(loci),
            "safely_shared_with_preferred": shared,
            "same_text_as_a_system_already_counted": already,
            "additional_loci": additional,
            "by_status": dict(sorted(by_status.items())),
        }
        counted.append(system)
    return out


def _coverage_loci(universe: str, root: Path | None = None) -> list[Locus]:
    """The actual loci counted by a requested coverage universe.

    Both universes are necessarily limited to systems this repository can
    enumerate from a tracked witness or concordance. `distinct-content` counts
    each such text once: the preferred universe plus only native loci that
    cannot be safely shared with it or a native system already counted.
    `addresses` counts every printed address the resolver supports, including
    alternate numberings and translations of the same text. The latter is the
    stronger consumer guarantee inside that enumerable boundary: an address
    must not return empty merely because coverage correctly deduplicates its
    content.
    """
    if universe not in ("primary", "distinct-content", "addresses"):
        raise ChronologyError(
            f"coverage universe {universe!r} is not 'distinct-content' or "
            f"'addresses'"
        )
    counts = verse_counts()
    corpus = load(root)
    loci = [
        Locus(PREFERRED_SYSTEM, token, chapter, verse)
        for token, chapters in corpus.books.items()
        for chapter in range(1, chapters + 1)
        for verse in range(1, counts[(token, chapter)] + 1)
    ]
    if universe == "primary":
        return loci

    import _deuterocanon  # noqa: PLC0415

    counted: list[str] = []
    for system in sorted(scripture_systems()):
        if system == PREFERRED_SYSTEM:
            continue
        printed = _system_loci(system)
        if printed is None:
            continue
        for token, chapter, verse in printed:
            if universe == "addresses":
                loci.append(Locus(system, token, chapter, verse))
                continue
            reached = to_canonical(system, token, chapter, verse)
            if not isinstance(reached, Unresolved):
                continue
            elsewhere = False
            for prior in counted:
                if token not in (scripture_systems().get(prior) or ()):
                    continue
                try:
                    moved, _ = _deuterocanon.convert_through(
                        token, chapter, verse, (system, prior)
                    )
                except Exception:  # noqa: BLE001 - a refusal is a finding
                    moved = None
                if moved is not None:
                    elsewhere = True
                    break
            if not elsewhere:
                loci.append(Locus(system, token, chapter, verse))
        counted.append(system)
    return loci


def _expanded_coverage(
    root: Path | None, profile: str | None, universe: str, require_date: bool
) -> dict[str, Any]:
    requested_profile = profile or load(root).default_profile
    loci = _coverage_loci(universe, root)
    native = native_coverage(root, profile)
    unenumerable = {
        system: str(detail.get("note", ""))
        for system, detail in sorted(native.items())
        if not detail.get("enumerable")
    }
    by_status: dict[str, int] = {status: 0 for status in STATUSES}
    by_relation: dict[str, int] = {relation: 0 for relation in RELATIONS}
    by_system: dict[str, int] = {}
    missing: list[str] = []
    multiple = substantive = alternates = 0
    direct = inherited = both = 0
    run_count = 0
    previous: tuple[str, str, int, int, tuple] | None = None
    for locus in loci:
        answer = chronology(locus, profile=profile, root=root)
        by_system[locus.system] = by_system.get(locus.system, 0) + 1
        if isinstance(answer, Unresolved):
            status, assertions = answer.status, ()
        else:
            status, assertions = answer.status, answer.assertions
        by_status[status] = by_status.get(status, 0) + 1
        relations = {item.relation for item in assertions}
        for relation in relations:
            by_relation[relation] += 1
        if len(relations) > 1:
            multiple += 1
        if relations - TEXTUAL_RELATIONS:
            substantive += 1
        if any(item.claim.disposition in ("alternate", "disputed") for item in assertions):
            alternates += 1
        substantive_items = [
            item for item in assertions if item.relation not in TEXTUAL_RELATIONS
        ]
        if substantive_items:
            has_direct = any(not item.inherited for item in substantive_items)
            has_inherited = any(item.inherited for item in substantive_items)
            if has_direct and has_inherited:
                both += 1
            elif has_direct:
                direct += 1
            else:
                inherited += 1
        if not any(is_positional_date(item.claim.date) for item in assertions):
            missing.append(str(locus))
        signature = _signature(answer)
        marker = (locus.system, locus.token, locus.chapter, locus.verse, signature)
        if (
            previous is None
            or previous[:3] != marker[:3]
            or marker[3] != previous[3] + 1
            or marker[4] != previous[4]
        ):
            run_count += 1
        previous = marker
    if require_date and missing:
        sample = ", ".join(missing[:20])
        more = f"; {len(missing) - 20} more" if len(missing) > 20 else ""
        raise ChronologyError(
            f"coverage --require-date found {len(missing)} valid {universe} "
            f"loci with no answerable positional Date: {sample}{more}"
        )
    return {
        "status": "ok",
        "profile": requested_profile,
        "universe": (
            "distinct-scripture-content"
            if universe == "distinct-content"
            else "supported-scripture-addresses"
        ),
        "total_verses": len(loci),
        "runs": run_count,
        "by_status": dict(sorted(by_status.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "by_system": dict(sorted(by_system.items())),
        "verses_with_multiple_relations": multiple,
        "verses_with_substantive_event_assertions": substantive,
        "verses_with_alternative_traditional_claims": alternates,
        "substantive_by_provenance": {
            "direct_only": direct, "inherited_only": inherited, "both": both,
        },
        "missing_dates": len(missing),
        "require_date": require_date,
        # A ZERO INSIDE A NAMED DENOMINATOR, never a claim about systems the
        # repository cannot enumerate. Keep both the stable machine category
        # and each excluded system's native-coverage reason in the payload so
        # a caller cannot turn `missing_dates: 0` into "all numbering systems".
        "universe_limitations": {
            "date_completeness_scope": "enumerated-loci-only",
            "note": (
                "missing_dates and --require-date apply only to loci enumerated "
                "by tracked witnesses and concordances"
            ),
        },
        "unenumerable_systems": unenumerable,
    }


def coverage(
    root: Path | None = None,
    profile: str | None = None,
    universe: str = "primary",
    require_date: bool = False,
) -> dict[str, Any]:
    """The counts a headline may be built from, never a headline on its own.

    Every category is reported. A single percentage is forbidden by
    `guidance/scripture-chronology.md` for the reason it is forbidden
    everywhere in this repository: "100% covered" is true of a corpus that has
    researched nothing, if the thing being counted is keys in a file.
    """
    if universe != "primary":
        return _expanded_coverage(root, profile, universe, require_date)

    requested_profile = profile or load(root).default_profile
    table = runs(root, profile)
    counts = verse_counts()
    total = sum(counts.values())
    by_status: dict[str, int] = {status: 0 for status in STATUSES}
    by_relation: dict[str, int] = {relation: 0 for relation in RELATIONS}
    multiple = 0
    substantive = 0
    for run in table:
        by_status[run.status] = by_status.get(run.status, 0) + run.verses
        for relation in run.relations:
            by_relation[relation] += run.verses
        if len(run.relations) > 1:
            multiple += run.verses
        if any(relation not in TEXTUAL_RELATIONS for relation in run.relations):
            substantive += run.verses
    accounted = sum(by_status.values())
    if accounted != total:
        raise ChronologyError(
            f"coverage accounts for {accounted} verses of {total}; every locus "
            f"must reach exactly one status"
        )
    alternates = _alternate_verses(table, root, profile)
    provenance = _provenance_verses(table, root, profile)
    missing: list[Run] = []
    for run in table:
        answer = chronology(
            Locus(PREFERRED_SYSTEM, run.token, run.chapter, run.first),
            profile=profile,
            root=root,
        )
        assertions = answer.assertions if isinstance(answer, Answer) else ()
        if not any(is_positional_date(item.claim.date) for item in assertions):
            missing.append(run)
    payload = {
        "status": "ok",
        "profile": requested_profile,
        "universe": "vulgate-clementine-primary",
        "total_verses": total,
        "runs": len(table),
        "by_status": dict(sorted(by_status.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "verses_with_multiple_relations": multiple,
        "verses_with_substantive_event_assertions": substantive,
        "verses_with_alternative_traditional_claims": alternates,
        "substantive_by_provenance": provenance,
        "native_systems": native_coverage(root, profile),
        "missing_dates": sum(run.verses for run in missing),
        "require_date": require_date,
    }
    if require_date and missing:
        sample = [f"{run.token}.{run.chapter}.{run.first}" for run in missing[:20]]
        if sample:
            raise ChronologyError(
                f"coverage --require-date found valid primary loci with no "
                f"answerable positional Date: {', '.join(sample)}"
            )
    return payload


def _provenance_verses(
    table: list[Run], root: Path | None, profile: str | None
) -> dict[str, int]:
    """How the substantive assertions reached the verses they apply to.

    Reported beside the statuses and never inside them. Directness is what the
    corrected status rule deliberately stopped asking (§9), so it has to be
    visible somewhere or the question "was any of this authored at this verse?"
    becomes unanswerable. Counted over verses whose status is `dated`, since
    that is the only status directness could be mistaken for evidence about.
    """
    direct = inherited = both = 0
    for run in table:
        if run.status != "dated":
            continue
        answer = chronology(
            Locus(CANONICAL_SYSTEM, run.token, run.chapter, run.first),
            profile=profile,
            root=root,
        )
        if not isinstance(answer, Answer):
            continue
        substantive = [
            item for item in answer.assertions
            if item.relation not in TEXTUAL_RELATIONS
        ]
        if not substantive:
            continue
        has_direct = any(not item.inherited for item in substantive)
        has_inherited = any(item.inherited for item in substantive)
        if has_direct and has_inherited:
            both += run.verses
        elif has_direct:
            direct += run.verses
        else:
            inherited += run.verses
    return {
        "direct_only": direct,
        "inherited_only": inherited,
        "both": both,
    }


def _alternate_verses(table: list[Run], root: Path | None, profile: str | None) -> int:
    """Verses whose selected answer preserves alternatives for one subject.

    Count the query result, not claims stored on the holder. This is both the
    semantic boundary and what makes an omitted profile observationally equal
    to its declared default: a cascade id is not a leaf claim.profile, while
    every selected assertion still carries the leaf that actually answered.
    Group by relation and subject so two bindings of one event do not turn one
    claim into a disagreement, and count claim identity so overlapping bindings
    cannot duplicate the same claim into an apparent alternative.
    """
    total = 0
    for run in table:
        answer = chronology(
            Locus(PREFERRED_SYSTEM, run.token, run.chapter, run.first),
            profile=profile,
            root=root,
        )
        if not isinstance(answer, Answer):
            continue
        groups: dict[tuple[str, str], set[int]] = {}
        for item in answer.assertions:
            groups.setdefault((item.relation, item.subject), set()).add(
                id(item.claim)
            )
        if any(len(claims) > 1 for claims in groups.values()):
            total += run.verses
    return total


def answerability(root: Path | None = None) -> dict[str, Any]:
    """What the corpus answers with, what it preserves, and on what basis.

    Reported rather than asserted. A profile change moves claims between these
    counts WITHOUT any claim file changing, which is the whole reason profile
    policy is production semantic state: the numbers here are the observable
    surface of a policy edit, and the review diff enumerates which claims moved.

    `by_basis` is also the standing debt. Every claim still standing on the
    profile's unstated basis class is one nobody has yet classified under the
    contract, and a corpus that reported only "answerable: N" would be reporting
    that as a finding.
    """
    corpus = load(root)
    counts = {state: 0 for state in ANSWERABILITY}
    by_basis: dict[str, int] = {}
    answered = 0
    for holder in (*corpus.events.values(), *corpus.units.values()):
        for claim in holder.claims:
            counts[claim.answerability] = counts.get(claim.answerability, 0) + 1
            by_basis[claim.basis_class] = by_basis.get(claim.basis_class, 0) + 1
            if corpus.answers_with(claim):
                answered += 1
    return {
        "claims": sum(counts.values()),
        "candidate_claims": answered,
        "by_state": dict(sorted(counts.items())),
        "by_basis": dict(sorted(by_basis.items())),
        "unstated_basis": {
            name: policy.unstated_basis for name, policy in sorted(corpus.policies.items())
        },
    }


# --- Audit ------------------------------------------------------------------


def _known_source_ids(repo: Path | None = None) -> set[str]:
    """Every source-library record id, read from the library's own tree.

    Read rather than restated. A list of acceptable ids beside the library
    would be the second source of truth this repository has already been bitten
    by, and it would go stale the first time a record was added.
    """
    import re as _re  # noqa: PLC0415

    base = Path(repo) if repo is not None else ROOT
    works = base / "src" / "sources" / "works"
    found: set[str] = set()
    pattern = _re.compile(r'^id = "([^"]+)"', _re.MULTILINE)
    for record in works.rglob("*.toml"):
        match = pattern.search(record.read_text(encoding="utf-8"))
        if match:
            found.add(match.group(1))
    return found


def _bible_source_ids(repo: Path | None = None) -> set[str]:
    """The tracked bible editions, addressable as sources for a rank-1 claim."""
    base = Path(repo) if repo is not None else ROOT
    bibles = base / "src" / "sources" / "bibles"
    if not bibles.is_dir():
        return set()
    return {
        f"bible.{edition.name}"
        for edition in bibles.iterdir()
        if (edition / "index.yaml").exists()
    }


def _bible_source_locus_problem(source: str, repo: Path | None = None) -> str | None:
    """Why a `bible:<edition>:<locus>` source is not in that exact witness."""
    import json as _json  # noqa: PLC0415

    parts = source.split(":", 2)
    if len(parts) != 3 or not parts[1] or not parts[2]:
        return "is not a bible:<edition>:<book.chapter.verse> source"
    edition, raw_locus = parts[1], parts[2]
    try:
        locus = parse_locus(raw_locus, f"source {source!r}")
    except ChronologyError:
        return "does not name a book.chapter.verse locus"
    base = Path(repo) if repo is not None else ROOT
    chapter = (
        base / "src" / "sources" / "bibles" / edition / "chapters"
        / locus.token / f"{locus.chapter}.json"
    )
    if not chapter.is_file():
        return (
            f"names {raw_locus}, but the tracked {edition!r} witness prints no "
            f"{locus.token}.{locus.chapter} chapter"
        )
    try:
        verses = _json.loads(chapter.read_text(encoding="utf-8")).get("verses")
    except (OSError, ValueError, AttributeError) as error:
        return f"cannot read the tracked {edition!r} chapter: {error}"
    if not isinstance(verses, dict) or str(locus.verse) not in verses:
        return (
            f"names {raw_locus}, but the tracked {edition!r} witness does not "
            f"print that verse"
        )
    return None


def audit(root: Path | None = None, repo: Path | None = None) -> list[str]:
    """Every problem load-time validation cannot see, collected not raised.

    Load refuses malformed data. This asks the questions that need the rest of
    the repository to answer: does that source record exist, does that verse
    exist, and does a gap contradict an assertion standing over the same verse.
    """
    corpus = load(root)
    problems: list[str] = []

    known = _known_source_ids(repo) | _bible_source_ids(repo)
    holders: list[tuple[str, str, tuple[Claim, ...]]] = [
        *(("event", event.id, event.claims) for event in corpus.events.values()),
        *(("unit", unit.id, unit.claims) for unit in corpus.units.values()),
    ]
    source_holders: list[tuple[str, str, tuple[str, ...]]] = [
        *(
            (kind, identifier, claim.sources)
            for kind, identifier, claims in holders
            for claim in claims
        ),
        *(
            ("binding", f"{binding.relation} -> {binding.event}", binding.sources)
            for binding in corpus.bindings
        ),
        *(
            ("gap", f"{gap.status} {_scope_text(gap.scope)}", gap.sources)
            for gap in corpus.gaps
        ),
    ]
    for kind, identifier, sources in source_holders:
        for source in sources:
            if source in known:
                continue
            if source.startswith("bible:"):
                # `bible:<edition>:<locus>` — Scripture cited as its own
                # rank-1 witness, at a stated locus in a tracked edition.
                # The edition directory alone is not evidence that the cited
                # verse exists in it: validate the exact chapter record before
                # admitting the source.
                parts = source.split(":", 2)
                if len(parts) == 3 and f"bible.{parts[1]}" in known:
                    problem = _bible_source_locus_problem(source, repo)
                    if problem:
                        problems.append(
                            f"{kind} {identifier}: source {source!r} {problem}"
                        )
                    continue
            problems.append(
                f"{kind} {identifier}: source {source!r} is not a record "
                f"this repository holds"
            )
    for derivation_holder in holders:
        kind, identifier, claims = derivation_holder
        for claim in claims:
            if not claim.derived:
                continue
            for used in claim.date.derivation.get("inputs", []):
                if used not in corpus.events and used not in corpus.units:
                    problems.append(
                        f"{kind} {identifier}: derivation input {used!r} is "
                        f"neither an event nor a composition unit"
                    )

    counts = verse_counts()
    for kind, identifier, scope in (
        *(("unit", unit.id, unit.scope) for unit in corpus.units.values()),
        *(
            ("binding", f"{binding.relation} -> {binding.event}", binding.scope)
            for binding in corpus.bindings
        ),
        *(("gap", f"{gap.status} {_scope_text(gap.scope)}", gap.scope) for gap in corpus.gaps),
    ):
        for span in scope:
            if span.chapter is None:
                continue
            ceiling = counts.get((span.token, span.chapter))
            if ceiling is None:
                problems.append(
                    f"{kind} {identifier}: {span.token} has no chapter {span.chapter}"
                )
                continue
            for edge, verse in (("first", span.first), ("last", span.last)):
                if verse is None:
                    continue
                if verse < 1 or verse > ceiling:
                    # Never clamp. guidance/versification.md §8.5 rule 1: a
                    # range naming a verse past the chapter's end is an error,
                    # and the message names the ceiling and the edition.
                    problems.append(
                        f"{kind} {identifier}: {span.token}.{span.chapter} ends "
                        f"at verse {ceiling} in the canonical edition, but the "
                        f"scope's {edge} verse is {verse}"
                    )

    for gap in corpus.gaps:
        for span in gap.scope:
            if span.chapter is None:
                continue
            ceiling = counts.get((span.token, span.chapter))
            if ceiling is None:
                continue
            for verse in range(span.first or 1, (span.last or ceiling) + 1):
                answer = chronology(
                    Locus(span.system, span.token, span.chapter, verse),
                    profile=gap.profile,
                    root=root,
                )
                if isinstance(answer, Answer) and answer.assertions:
                    problems.append(
                        f"gap {gap.status} covers {span.token}.{span.chapter}."
                        f"{verse}, which carries "
                        f"{len(answer.assertions)} assertion(s); a gap says the "
                        f"corpus has nothing, and it has something"
                    )
                    break
    return sorted(set(problems))
