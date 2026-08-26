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

Zero or more TYPED TEMPORAL ASSERTIONS, never a scalar date. Eight relations,
and the distinctions between them are the point:

    composition             when the text was written
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

A locus with no assertion is not missing from this corpus; it has a status.
`research-pending` is the honest default and the corpus says so rather than
reporting coverage it does not have. `gaps.yaml` records the statuses that are
KNOWN to be something else — a tradition that dates nothing, a text that cannot
be aligned. `guidance/the-shape.md` §4: absence is data and must have somewhere
to live, or it will be filled.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, NamedTuple

ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = ROOT / "src" / "sources" / "chronology"

# The system chronology is authored in. Not a constant for its own sake: it is
# `_projection.CANONICAL`, named here so that the two cannot drift apart, and
# checked against it at load time.
CANONICAL_SYSTEM = "vulgate"

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
    "narrated-event",
    "utterance",
    "historical-setting",
    "superscription-setting",
    "retrospective-event",
    "prophecy-given",
    "prophetic-referent",
)

# The order a query returns assertions in, so a consumer's output is stable and
# a diff of two queries is a diff of the answers rather than of the sorting.
# Composition first because it is the one assertion nearly every locus has.
RELATION_ORDER = {relation: index for index, relation in enumerate(RELATIONS)}

DISPOSITIONS = ("preferred", "alternate", "disputed")

# How a date's endpoints are to be read. Separate from `basis` on purpose:
# "approximate" says the date is approximate, not that its source is weak.
PRECISIONS = (
    "day",              # from == to, both carrying month and day
    "month-day",        # month and day known, year not
    "year",             # from == to, exact
    "approximate-year", # from == to, the source's own "about"
    "range",            # the subject spans from..to
    "interval",         # the subject falls somewhere within from..to
    "relative",         # no absolute endpoints; a stated interval from another event
)

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

# Every status a locus can carry. `dated` and `inherited` are earned by
# assertions; the rest are authored in gaps.yaml, except `research-pending`,
# which is what a locus has when nothing else applies.
STATUSES = (
    "dated",              # at least one direct, substantive assertion
    "inherited",          # covered only by an inherited composition assertion
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

    @property
    def derived(self) -> bool:
        return self.derivation is not None

    def __str__(self) -> str:
        if self.precision == "relative" and self.relative:
            return str(self.relative.get("statement") or self.relative)
        if self.begin is None:
            return "?"
        if self.begin == self.end or self.end is None:
            head = str(self.begin)
            return f"about {head}" if self.precision == "approximate-year" else head
        joiner = "-" if self.precision == "range" else " to "
        return f"{self.begin}{joiner}{self.end}"


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
        "precision", "from", "to", "relative", "label", "derivation",
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
    """A textual unit with its own composition chronology, and its extent."""

    id: str
    title: str
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


class Answer(NamedTuple):
    """A resolved locus and everything the corpus says about it."""

    locus: Locus
    assertions: tuple[Assertion, ...]
    status: str
    note: str

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


def _document(name: str, root: Path) -> dict[str, Any]:
    path = root / f"{name}.yaml"
    if not path.exists():
        raise ChronologyError(f"{path}: the chronology corpus is missing {name}.yaml")
    data = _yaml().safe_load(path.read_text(encoding="utf-8"))
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


def _claims(raw: dict[str, Any], where: str, profiles: set[str]) -> tuple[Claim, ...]:
    listed = raw.get("dates")
    if not isinstance(listed, list) or not listed:
        raise ChronologyError(f"{where}: needs a non-empty 'dates' list")
    claims: list[Claim] = []
    for index, entry in enumerate(listed, start=1):
        spot = f"{where} date {index}"
        if not isinstance(entry, dict):
            raise ChronologyError(f"{spot}: expected a mapping")
        _keys(
            entry,
            {"profile", "disposition", "date", "basis", "sources", "note"},
            spot,
        )
        profile = entry.get("profile")
        if profile not in profiles:
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
        claims.append(
            Claim(
                profile=profile,
                disposition=disposition,
                date=date,
                basis=_text(entry, "basis", spot, required=True),
                sources=_sources(entry, spot, required=not date.derived),
                note=_text(entry, "note", spot),
            )
        )
    # The conflict policy, enforced rather than described: one preferred claim
    # per profile, and none at all while any claim on the subject is disputed.
    for profile in profiles:
        mine = [claim for claim in claims if claim.profile == profile]
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
        system = entry.get("system", CANONICAL_SYSTEM)
        if system != CANONICAL_SYSTEM:
            raise ChronologyError(
                f"{spot}: chronology is authored in {CANONICAL_SYSTEM!r}; a "
                f"locus in {system!r} reaches it through the concordance, not "
                f"by being authored twice"
            )
        token = entry.get("book")
        if token not in books:
            raise ChronologyError(
                f"{spot}: {token!r} is not a book of the canon; see scripts/_canon.py"
            )
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


class Corpus(NamedTuple):
    """Everything authored, validated, and keyed the way a query asks for it."""

    profiles: dict[str, dict[str, Any]]
    events: dict[str, Event]
    units: dict[str, Unit]
    bindings: tuple[Binding, ...]
    gaps: tuple[Gap, ...]
    books: dict[str, int]


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


def _load_profiles(root: Path) -> dict[str, dict[str, Any]]:
    document = _document("profiles", root)
    listed = document.get("profiles")
    if not isinstance(listed, list) or not listed:
        raise ChronologyError(f"{root}/profiles.yaml: needs a non-empty 'profiles' list")
    profiles: dict[str, dict[str, Any]] = {}
    for entry in listed:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/profiles.yaml: a profile must be a mapping")
        identifier = check_id(entry.get("id"), "profile", f"{root}/profiles.yaml")
        if identifier in profiles:
            raise ChronologyError(f"{root}/profiles.yaml: duplicate profile {identifier}")
        for required in ("title", "intent", "authority", "conflict", "non_goals"):
            if not entry.get(required):
                raise ChronologyError(
                    f"{root}/profiles.yaml: profile {identifier} states no {required}; "
                    f"a profile that does not say what wins is not a policy"
                )
        profiles[identifier] = entry
    return profiles


def _load_events(root: Path, profiles: set[str]) -> dict[str, Event]:
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
            claims=_claims(entry, where, profiles),
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


def _load_units(root: Path, profiles: set[str], books: dict[str, int]) -> dict[str, Unit]:
    document = _document("composition", root)
    units: dict[str, Unit] = {}
    for entry in document.get("units") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/composition.yaml: a unit must be a mapping")
        where = f"{root}/composition.yaml unit {entry.get('id')!r}"
        _keys(entry, {"id", "title", "scope", "dates", "note"}, where)
        identifier = check_id(entry.get("id"), "composition unit", where)
        if identifier in units:
            raise ChronologyError(f"{where}: duplicate unit id")
        units[identifier] = Unit(
            id=identifier,
            title=_text(entry, "title", where, required=True),
            scope=_scope(entry.get("scope"), where, books),
            claims=_claims(entry, where, profiles),
            note=_text(entry, "note", where),
        )
    _refuse_ambiguous_inheritance(units, root)
    return units


def _refuse_ambiguous_inheritance(units: dict[str, Unit], root: Path) -> None:
    """Two units of equal width over one verse is an error, not a tie.

    Nothing here may pick between them: choosing the first, the narrowest by
    accident of authoring order, or the more recently edited would all be a
    date resolving successfully and wrongly. So the corpus refuses to load and
    the author says which unit owns the text.
    """
    by_width: dict[int, dict[tuple[str, int, int], str]] = {}
    for unit in units.values():
        width = unit.width()
        seen = by_width.setdefault(width, {})
        for span in unit.scope:
            for key in _span_keys(span, unit.scope):
                if key in seen and seen[key] != unit.id:
                    raise ChronologyError(
                        f"{root}/composition.yaml: units {seen[key]} and "
                        f"{unit.id} both claim {key[0]}.{key[1]}.{key[2]} at the "
                        f"same width; narrow one of them"
                    )
                seen[key] = unit.id


def _span_keys(span: Span, _scope_all: tuple[Span, ...]) -> Iterable[tuple[str, int, int]]:
    """The overlap key a span occupies. Chapter-level, so it needs no verse counts."""
    if span.chapter is None:
        yield (span.token, 0, 0)
        return
    if span.first is None and span.last is None:
        yield (span.token, span.chapter, 0)
        return
    yield (span.token, span.chapter, span.first or 1)


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
        if relation == "composition":
            raise ChronologyError(
                f"{where}: composition is not an event binding; it is a textual "
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


def _load_gaps(root: Path, books: dict[str, int]) -> tuple[Gap, ...]:
    document = _document("gaps", root)
    gaps: list[Gap] = []
    authored = set(STATUSES) - {"dated", "inherited", "research-pending"}
    for entry in document.get("gaps") or []:
        if not isinstance(entry, dict):
            raise ChronologyError(f"{root}/gaps.yaml: a gap must be a mapping")
        where = f"{root}/gaps.yaml gap {entry.get('status')!r}"
        _keys(entry, {"status", "scope", "reason", "sources"}, where)
        status = entry.get("status")
        if status not in authored:
            raise ChronologyError(
                f"{where}: status {status!r} is not one an author may assert; "
                f"choose from {sorted(authored)}. 'dated' and 'inherited' are "
                f"earned by assertions and 'research-pending' is the default"
            )
        gaps.append(
            Gap(
                status=status,
                scope=_scope(entry.get("scope"), where, books),
                reason=_text(entry, "reason", where, required=True),
                sources=_sources(entry, where, required=False),
            )
        )
    return tuple(gaps)


@lru_cache(maxsize=4)
def load(root: Path | None = None) -> Corpus:
    """Read and validate the whole corpus, or refuse with the reason."""
    where = Path(root) if root is not None else CORPUS_ROOT
    books = _canon_books()
    profiles = _load_profiles(where)
    events = _load_events(where, set(profiles))
    units = _load_units(where, set(profiles), books)
    bindings = _load_bindings(where, events, books)
    gaps = _load_gaps(where, books)
    return Corpus(profiles, events, units, bindings, gaps, books)


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
        try:
            moved, reason = _deuterocanon.convert_verse(
                token, chapter, verse, system, CANONICAL_SYSTEM
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
            index[token][0].append(unit)
    for binding in corpus.bindings:
        for token in {span.token for span in binding.scope}:
            index[token][1].append(binding)
    for gap in corpus.gaps:
        for token in {span.token for span in gap.scope}:
            index[token][2].append(gap)
    return {
        token: (tuple(units), tuple(bindings), tuple(gaps))
        for token, (units, bindings, gaps) in index.items()
    }


def chronology(
    locus: Locus | str,
    *,
    profile: str | None = None,
    root: Path | None = None,
) -> Answer | Unresolved:
    """Everything the corpus says about one verse, in a stable order.

    Returns EVERY applicable assertion. It never picks one when alternatives
    exist: `guidance/the-shape.md` §5 is that a tool which always answers lies
    when it does not know, and choosing silently between two traditional dates
    is the same lie with better manners.
    """
    corpus = load(root)
    if isinstance(locus, str):
        locus = parse_locus(locus)
    if locus.system != CANONICAL_SYSTEM:
        converted = to_canonical(locus.system, locus.token, locus.chapter, locus.verse)
        if isinstance(converted, Unresolved):
            return converted._replace(locus=str(locus))
        locus = converted
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

    units, bindings, gaps = _by_book(root)[locus.token]
    assertions: list[Assertion] = []

    # Composition, by inheritance: the narrowest unit covering the verse wins,
    # and equal widths were refused at load time rather than broken here.
    best: Unit | None = None
    best_span: Span | None = None
    for unit in units:
        span = _scope_covers(unit.scope, locus.token, locus.chapter, locus.verse)
        if span is None:
            continue
        if best is None or unit.width() > best.width():
            best, best_span = unit, span
    if best is not None and best_span is not None:
        for claim in best.claims:
            if profile and claim.profile != profile:
                continue
            assertions.append(
                Assertion(
                    relation="composition",
                    subject=best.id,
                    title=best.title,
                    claim=claim,
                    inherited=best_span.first is None or best_span.chapter is None,
                    scope=_scope_text(best.scope),
                )
            )

    # Events, by binding. One event, dated once, reached from every locus bound
    # to it under whichever relation that locus stands in to it.
    for binding in bindings:
        span = _scope_covers(binding.scope, locus.token, locus.chapter, locus.verse)
        if span is None:
            continue
        event = corpus.events[binding.event]
        for claim in event.claims:
            if profile and claim.profile != profile:
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

    assertions.sort(key=lambda item: item.sort_key())

    if assertions:
        direct = any(not item.inherited for item in assertions)
        others = any(item.relation != "composition" for item in assertions)
        status = "dated" if direct or others else "inherited"
        return Answer(locus, tuple(assertions), status, "")

    for gap in gaps:
        if _scope_covers(gap.scope, locus.token, locus.chapter, locus.verse):
            return Answer(locus, (), gap.status, gap.reason)
    return Answer(
        locus,
        (),
        "research-pending",
        "no ranked source has been inspected for this locus yet",
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


def coverage(root: Path | None = None, profile: str | None = None) -> dict[str, Any]:
    """The counts a headline may be built from, never a headline on its own.

    Every category is reported. A single percentage is forbidden by
    `guidance/scripture-chronology.md` for the reason it is forbidden
    everywhere in this repository: "100% covered" is true of a corpus that has
    researched nothing, if the thing being counted is keys in a file.
    """
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
        if run.relations and set(run.relations) != {"composition"}:
            substantive += run.verses
    accounted = sum(by_status.values())
    if accounted != total:
        raise ChronologyError(
            f"coverage accounts for {accounted} verses of {total}; every locus "
            f"must reach exactly one status"
        )
    alternates = _alternate_verses(table, root, profile)
    return {
        "status": "ok",
        "total_verses": total,
        "runs": len(table),
        "by_status": dict(sorted(by_status.items())),
        "by_relation": dict(sorted(by_relation.items())),
        "verses_with_multiple_relations": multiple,
        "verses_with_substantive_event_assertions": substantive,
        "verses_with_alternative_traditional_claims": alternates,
    }


def _alternate_verses(table: list[Run], root: Path | None, profile: str | None) -> int:
    """Verses whose answer preserves more than one traditional claim."""
    corpus = load(root)
    contested = {
        subject
        for holder in (*corpus.events.values(), *corpus.units.values())
        for subject in ((holder.id,) if len(holder.claims) > 1 else ())
    }
    return sum(
        run.verses for run in table if contested.intersection(run.subjects)
    )


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
    for kind, identifier, claims in holders:
        for claim in claims:
            for source in claim.sources:
                if source in known:
                    continue
                if source.startswith("bible:"):
                    # `bible:<edition>:<locus>` — Scripture cited as its own
                    # rank-1 witness, at a stated locus in a tracked edition.
                    parts = source.split(":", 2)
                    if len(parts) == 3 and f"bible.{parts[1]}" in known:
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
                    Locus(CANONICAL_SYSTEM, span.token, span.chapter, verse), root=root
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
