"""A proper's appointed loci, and what the chronology corpus says about them.

This is the propers' one route to biblical chronology, and it exists because
`guidance/scripture-chronology.md` §14 forbids the other one. A proper that
wants to print when a psalm was composed or when the episode behind an
Offertory happened MUST read `src/sources/chronology/`; it may not infer,
research, harmonize, or recall a replacement date, and where the corpus
returns an unresolved state the proper preserves that state or omits the date.

Three seams meet here and none of them is re-implemented:

- **The citation.** `_calendars.resolve_propers` is how every other consumer
  reaches a proper's appointed verses, and it is how this one does. Nothing
  here parses a citation string; the calendar's machine encoding
  (`book`, `ranges`) is primary, `tools/citations` owns it, and `_loci`
  turns a range into the chapters it touches.
- **The book name.** `_canon.books()` maps the calendar's modern book name
  ("1 Kings", "Psalms") onto the token the rest of the repository addresses a
  book by ("3Kings", "Ps"), which is the spelling the chronology corpus uses
  because `_chronology._canon_books` reads the same index. A hand-written
  table beside it is the second source of truth `guidance/the-shape.md` §2
  predicts will disagree.
- **The chronology.** `_chronology.chronology()` is the whole seam onto the
  corpus, per that guidance's §2. Nothing here reads the corpus YAML.

The calendar declares `psalm_numbering: vulgate` and the chronology corpus's
preferred system is `vulgate`, so a locus crosses this boundary unconverted.
That agreement is asserted rather than assumed: `element_loci` refuses when
the calendar declares any other numbering, because a psalm locus quietly read
in the wrong system would name a different psalm and still look right.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import _calendars
import _canon
import _chronology
from _loci import range_to_loci

ROOT = Path(__file__).resolve().parents[1]
CALENDARS = "src/sources/calendars"
CALENDAR = "roman-1962"

# The record this module renders, and where a leaf carries it. It lives in
# `research/` because that is the leaf's audit payload, which is where §14 says
# the stable ids belong: "event id, unit id, profile, relation ... so prose can
# be regenerated without re-researching the fact".
RECORD = "research/chronology.toml"
RECORD_SCHEMA = 2
RECORD_TYPE = "proper-chronology"
GENERATOR = "tools/tpt proper-chronology record"

# The publication-facing projection of the record.  It deliberately lives
# beside, rather than inside, chronology.toml: the record carries the corpus's
# source words for audit, while this generated TeX carries a compact and
# deterministic display of the same assertions.  Neither file is an authoring
# surface.
ANNOTATIONS_RECORD = "research/chronology-annotations.tex"
ANNOTATIONS_SCHEMA = 2
ANNOTATIONS_TYPE = "proper-chronology-annotations"
ANNOTATIONS_GENERATOR = "tools/tpt proper-chronology annotations"

# The numbering the calendar must declare for a locus to cross into the corpus
# unconverted. Both sides spell it the same word; neither is trusted to.
REQUIRED_NUMBERING = _chronology.PREFERRED_SYSTEM


class ChronologyWiringError(ValueError):
    """A proper whose appointed loci cannot be resolved, with the reason."""


class Reach(NamedTuple):
    """How one corpus assertion reaches one appointed locus."""

    locus: str
    inherited: bool
    scope: str

    def sort_key(self) -> tuple:
        return (self.locus, self.scope, self.inherited)


class Claim(NamedTuple):
    """One assertion the corpus makes, with every appointed-locus reach.

    `label` is the source's own words and is the only field a manually authored
    guide may display; `date` is the normalized form and is carried for sorting
    and comparison, never for a manual page. The sole permitted display
    exception is this module's deterministic generated annotation projection:
    it derives a concise `display_label` from the structured corpus date while
    retaining the raw `label` and claim `profile`, so the projection is
    lossless and reviewable rather than a second authored chronology. The ids
    — `subject`, `relation`, `profile` — are what §14 requires a consumer to
    carry, so that the prose above can be regenerated from the corpus rather
    than re-researched.

    `basis` and `note` are deliberately absent. They run to thousands of
    characters of provenance prose, they are the corpus's to state, and a copy
    of them here would be a second place they could be edited. A reader who
    wants them runs `tools/tpt scripture-chronology query <locus> --evidence`.
    """

    relation: str
    subject: str
    title: str
    label: str
    date: str
    precision: str
    disposition: str
    answerability: str
    basis_class: str
    profile: str
    sources: tuple[str, ...]
    reaches: tuple[Reach, ...]

    def sort_key(self) -> tuple:
        return (
            self.relation,
            self.subject,
            self.date,
            self.label,
            tuple(reach.sort_key() for reach in self.reaches),
        )

    def identity_key(self) -> tuple:
        """The assertion identity shared by every locus it applies to.

        A reach says which address was asked and how the assertion reached it;
        it does not change the underlying claim. Every corpus-owned field that
        can change the claim's meaning or provenance does participate,
        including profile: moving an otherwise identical date between evidence
        profiles must move generated bytes.
        """
        return (
            self.relation,
            self.subject,
            self.title,
            self.label,
            self.date,
            self.precision,
            self.disposition,
            self.answerability,
            self.basis_class,
            self.profile,
            self.sources,
        )


class Element(NamedTuple):
    """One element's full audit answer and safe publication intersection."""

    key: str
    name: str
    refs: tuple[str, ...]
    loci: tuple[str, ...]
    status: str
    reason: str
    claims: tuple[Claim, ...]
    publication_status: str
    publication_reason: str
    publication_claims: tuple[Claim, ...]


class Dossier(NamedTuple):
    """Everything the corpus answers about one proper's appointed Scripture.

    `state` says whether the calendar appoints this identity a formulary at
    all, so that "no dates" and "no formulary to date" are two answers rather
    than one silence, and `reason` carries the corpus-facing explanation of a
    negative state in the same way an element's `reason` carries the corpus's.
    """

    document: str
    calendar: str
    mass: str
    system: str
    profile: str
    state: str
    reason: str
    elements: tuple[Element, ...]

    def element(self, key: str) -> Element | None:
        for item in self.elements:
            if item.key == key:
                return item
        return None


class AnnotationClaim(NamedTuple):
    """One corpus assertion in its audit and publication forms.

    ``label`` remains the source's exact wording.  ``display_label`` is a
    deterministic projection of the structured date, never a replacement
    claim and never written back to the corpus.  Keeping both in the generated
    artifact makes abbreviation visible and mechanically reviewable.
    """

    subject: str
    title: str
    relation: str
    label: str
    display_label: str
    date: str
    precision: str
    disposition: str
    profile: str
    sources: tuple[str, ...]
    reaches: tuple[Reach, ...]


class AnnotationGroup(NamedTuple):
    """All candidates for one relation, or one explicit relation gap."""

    relation: str
    status: str
    reason: str
    claims: tuple[AnnotationClaim, ...]


class AnnotationElement(NamedTuple):
    """The annotation for one appointed scriptural proper element."""

    key: str
    name: str
    refs: tuple[str, ...]
    status: str
    groups: tuple[AnnotationGroup, ...]


class AnnotationProjection(NamedTuple):
    """A stable publication projection of a proper chronology dossier."""

    document: str
    calendar: str
    mass: str
    system: str
    profile: str
    state: str
    reason: str
    elements: tuple[AnnotationElement, ...]


# --- From a leaf id to its mass --------------------------------------------

# The identity prefix a leaf id carries. `tools/check-proper-identity` owns the
# grammar and the scope gate has already refused an unregistered one by the
# time anything here runs; this only needs the prefix in order to look the mass
# up, so it matches the prefix and nothing else about the slug.
PREFIX = re.compile(r"\A([0-9]{2}|[fm][0-9]{2})-")

# A ritual identity, which the calendar transcribed here appoints no mass entry
# for. See `formulary_state`.
RITUAL = re.compile(r"\Am[0-9]{2}\Z")

# The two answers to "does the calendar appoint this identity a formulary".
APPOINTED = "appointed"
NO_CALENDAR_FORMULARY = "no-calendar-formulary"


def formulary_state(document: str) -> tuple[str, str]:
    """`(state, reason)`: does the calendar appoint this identity a formulary?

    A ritual identity — `m01`, in `ritual/m01-nuptial-mass` — is appointed by
    a rite and not by a day, and the 1962 calendar transcribed in
    `src/sources/calendars` carries the book's temporal and sanctoral cycles.
    No mass entry there holds an `M` registry value, so there is no formulary
    for this wiring to resolve. `tools/check-proper-identity` meets the same
    gap from the other side and accepts an `m` prefix on its grammar alone;
    the comment "Why ritual identities stop at the grammar" in that tool is
    the full statement of why, and this is the same fact answered in this
    module's own terms.

    It is an ANSWER and not an error, because the two are not the same fact.
    An unregistered numeric identity is a leaf claiming to be a day the
    calendar does not have, and is refused. A ritual leaf is a real published
    document whose Scripture this repository's calendar sources do not
    encode: the honest record says exactly that, so a bound run can carry one
    instead of having no compliant path at all. What the record must not do
    is imply the rite appoints no Scripture — it appoints a great deal — so
    the reason travels with the state wherever the state is printed.
    """
    prefix = identity_prefix(document)
    if RITUAL.match(prefix):
        return NO_CALENDAR_FORMULARY, (
            f"identity {prefix!r} is a ritual Mass, appointed by a rite and "
            f"not by a day, and no mass entry in the {CALENDAR} calendar "
            f"carries an M registry value; this wiring reaches Scripture "
            f"through the calendar, so it can resolve no appointed loci here. "
            f"That is a limit of the calendar sources, not a statement that "
            f"the rite appoints no Scripture, and no date may be supplied "
            f"from anywhere else to fill it"
        )
    return APPOINTED, ""


def identity_prefix(document: str) -> str:
    """The catalog identity a leaf id claims, e.g. `54`."""
    slug = document.rstrip("/").rpartition("/")[2]
    matched = PREFIX.match(slug)
    if matched is None:
        raise ChronologyWiringError(
            f"{document!r} does not name a 1962 proper leaf: its slug must "
            f"begin with a two-digit, f- or m-prefixed catalog identity"
        )
    return matched.group(1)


@lru_cache(maxsize=4)
def _calendar_document(root: Path) -> dict:
    return _calendars.load_document(root / CALENDARS, CALENDAR)


def mass_of(document: str, root: Path = ROOT) -> tuple[str, dict]:
    """The calendar mass entry whose registry value is this leaf's identity."""
    prefix = identity_prefix(document)
    calendar = _calendar_document(root)
    found = [
        (key, mass)
        for key, mass in _calendars.mass_index(calendar).items()
        if str(mass.get("registry") or "").lower() == prefix
    ]
    if not found:
        raise ChronologyWiringError(
            f"identity {prefix!r} is registered by no mass entry in the "
            f"{CALENDAR} calendar, so nothing here can name its appointed "
            f"Scripture"
        )
    if len(found) > 1:
        raise ChronologyWiringError(
            f"identity {prefix!r} is registered by {len(found)} mass entries "
            f"({', '.join(key for key, _ in found)}); one identity names one "
            f"formulary, and this one names more than one"
        )
    return found[0]


# --- From a mass to its loci ------------------------------------------------

SLUG = re.compile(r"[^a-z0-9]+")


def element_key(name: str) -> str:
    """The manifest's element key for a proper's printed name.

    `proper-components.toml` keys an element `introit`; the calendar prints it
    `Introit`. One rule, here, so the manifest and this record cannot come to
    spell the same element two ways.
    """
    return SLUG.sub("-", name.strip().lower()).strip("-")


@lru_cache(maxsize=1)
def _tokens() -> dict[str, str]:
    """Modern book name to the token every locus in this repository uses."""
    return {book["name"]: book["token"] for book in _canon.books()}


@lru_cache(maxsize=1)
def _verse_counts() -> dict[tuple[str, int], int]:
    """Only read when a citation leaves a range open at one end."""
    return _chronology.verse_counts()


def _loci_of(entry: dict, where: str) -> list[str]:
    """One citation's verses, as loci in the corpus's own spelling."""
    book = str(entry.get("book") or "")
    token = _tokens().get(book)
    if token is None:
        raise ChronologyWiringError(
            f"{where}: the calendar cites book {book!r}, which the canonical "
            f"book index does not name; a locus cannot be built from it"
        )
    out: list[str] = []
    for span in entry.get("ranges") or []:
        if not isinstance(span, dict):
            continue
        try:
            pieces = range_to_loci(span.get("begin") or {}, span.get("end"))
        except ValueError as exc:
            raise ChronologyWiringError(f"{where}: {exc}") from exc
        for piece in pieces:
            chapter = int(piece["chapter"])
            first = piece.get("first")
            last = piece.get("last")
            if first is None:
                first = 1
            if last is None:
                last = _verse_counts().get((token, chapter))
                if last is None:
                    raise ChronologyWiringError(
                        f"{where}: the canonical edition counts no verses at "
                        f"{token} {chapter}, so an open citation cannot be "
                        f"closed"
                    )
            out.extend(
                f"{token}.{chapter}.{verse}"
                for verse in range(int(first), int(last) + 1)
            )
    return out


def appointed(document: str, root: Path = ROOT) -> list[tuple[str, str, tuple[str, ...], tuple[str, ...]]]:
    """Each appointed element as `(key, name, refs, loci)`, in missal order.

    Elements the missal composes rather than quotes — Collect, Secret,
    Postcommunion — carry no Scripture and appear with no loci. They are kept
    in the list rather than dropped, because a record that showed only the
    scriptural elements would leave a reader unable to tell an element with no
    Scripture from one this pass forgot.
    """
    if formulary_state(document)[0] != APPOINTED:
        return []
    calendar = _calendar_document(root)
    numbering = str(calendar.get("psalm_numbering") or "")
    if numbering != REQUIRED_NUMBERING:
        raise ChronologyWiringError(
            f"the {CALENDAR} calendar declares psalm numbering {numbering!r} "
            f"and the chronology corpus answers in {REQUIRED_NUMBERING!r}; a "
            f"psalm locus may not cross that boundary unconverted, and this "
            f"wiring converts nothing"
        )
    key, mass = mass_of(document, root)
    entries, problems = _calendars.resolve_propers(calendar, mass)
    if problems:
        raise ChronologyWiringError(
            f"mass {key}: the calendar cannot resolve this formulary: "
            f"{'; '.join(problems)}"
        )
    out = []
    for _label, proper, _provenance in entries:
        name = str(proper.get("name") or "")
        where = f"mass {key} proper {name!r}"
        refs: list[str] = []
        loci: list[str] = []
        for entry in proper.get("verses") or []:
            if not isinstance(entry, dict):
                continue
            refs.append(str(entry.get("ref") or ""))
            loci.extend(_loci_of(entry, where))
        seen: dict[str, None] = {}
        for locus in loci:
            seen.setdefault(locus, None)
        out.append((element_key(name), name, tuple(refs), tuple(seen)))
    return out


# --- From loci to the corpus's answer ---------------------------------------


def _claims_at(locus: str, profile: str | None, corpus_root: Path | None) -> tuple[str, str, list[Claim]]:
    """`chronology()` for one locus, reduced to what this record carries."""
    answer = _chronology.chronology(locus, profile=profile, root=corpus_root)
    if not answer.resolved:
        return answer.status, answer.reason, []
    claims = [
        Claim(
            relation=item.relation,
            subject=item.subject,
            title=item.title,
            label=item.claim.date.label,
            date=str(item.claim.date),
            precision=item.claim.date.precision,
            disposition=item.claim.disposition,
            answerability=item.claim.answerability,
            basis_class=item.claim.basis_class,
            profile=item.claim.profile,
            sources=tuple(item.claim.sources),
            reaches=(
                Reach(
                    locus=str(answer.locus),
                    inherited=item.inherited,
                    scope=item.scope,
                ),
            ),
        )
        for item in answer.assertions
    ]
    return answer.status, answer.note, claims


NONUNIFORM = "nonuniform"


def _claim_maps(
    answers: list[tuple[str, str, str, list[Claim]]],
) -> list[dict[tuple, tuple[Claim, ...]]]:
    """Assertion identities at each locus, without losing reach routes."""
    out: list[dict[tuple, tuple[Claim, ...]]] = []
    for _locus, _status, _reason, claims in answers:
        grouped: dict[tuple, list[Claim]] = {}
        for claim in claims:
            grouped.setdefault(claim.identity_key(), []).append(claim)
        out.append(
            {
                identity: tuple(candidates)
                for identity, candidates in grouped.items()
            }
        )
    return out


def _aggregate_claims(
    by_locus: list[dict[tuple, tuple[Claim, ...]]], identities: set[tuple]
) -> tuple[Claim, ...]:
    """Claims with every distinct locus-to-scope route retained."""
    aggregated: list[Claim] = []
    for identity in identities:
        first: Claim | None = None
        reaches: dict[tuple, Reach] = {}
        for claims in by_locus:
            candidates = claims.get(identity)
            if candidates is None:
                continue
            for claim in candidates:
                if first is None:
                    first = claim
                for reach in claim.reaches:
                    reaches.setdefault(reach.sort_key(), reach)
        if first is not None:
            aggregated.append(
                first._replace(
                    reaches=tuple(
                        reaches[key] for key in sorted(reaches)
                    )
                )
            )
    return tuple(sorted(aggregated, key=Claim.sort_key))


def _all_claims(
    answers: list[tuple[str, str, str, list[Claim]]],
) -> tuple[Claim, ...]:
    """Every resolved assertion, including locus-specific ones."""
    by_locus = _claim_maps(answers)
    identities = set().union(*(set(claims) for claims in by_locus))
    return _aggregate_claims(by_locus, identities)


def _common_claims(
    answers: list[tuple[str, str, str, list[Claim]]],
) -> tuple[tuple[Claim, ...], str, str]:
    """Claims safe for one element-wide cell, plus its truthful status.

    A Date cell is labelled with the whole appointed element, not one verse of
    it. An assertion therefore survives only when every appointed locus
    supports the same assertion identity. Unioning the per-locus answers made
    a claim about one constituent look true of the entire cell.
    """
    if not answers:
        return (), "", ""

    by_locus = _claim_maps(answers)
    common = set(by_locus[0])
    for claims in by_locus[1:]:
        common.intersection_update(claims)
    held = _aggregate_claims(by_locus, common)

    union = set().union(*(set(claims) for claims in by_locus))
    omitted = union - common
    statuses = [status for _locus, status, _reason, _claims in answers]
    reasons = [
        reason
        for _locus, _status, reason, _claims in answers
        if reason
    ]

    if held:
        # The corpus owns this distinction too: a dated textual witness alone
        # is ``attestation-only`` and must not be relabelled as a composition
        # claim merely because both relations are part of textual history.
        status = _chronology._status_of(held)
        if omitted:
            detail = ", ".join(
                f"{locus}={locus_status}"
                for locus, locus_status, _reason, _claims in answers
            )
            return (
                held,
                status,
                "Only assertions supported at every appointed locus are "
                f"carried; locus-specific assertions were omitted ({detail}).",
            )
        return held, status, reasons[0] if reasons else ""

    if not union and len(set(statuses)) == 1:
        return (), statuses[0], reasons[0] if reasons else ""

    detail = ", ".join(
        f"{locus}={status}" for locus, status, _reason, _claims in answers
    )
    return (
        (),
        NONUNIFORM,
        "No single chronology assertion applies across every appointed "
        f"locus ({detail}); the element-wide Date cell must not print a "
        "locus-specific claim.",
    )


def _audit_status(
    answers: list[tuple[str, str, str, list[Claim]]],
) -> tuple[str, str]:
    """The strongest per-locus corpus answer, without publication inference."""
    if not answers:
        return "", ""
    statuses = [status for _locus, status, _reason, _claims in answers]
    status = min(
        statuses,
        key=lambda item: _chronology.STATUS_ORDER.get(item, 99),
    )
    reason = next(
        (
            reason
            for _locus, _status, reason, _claims in answers
            if reason
        ),
        "",
    )
    return status, reason


def dossier(
    document: str,
    root: Path = ROOT,
    profile: str | None = None,
    corpus_root: Path | None = None,
) -> Dossier:
    """Everything the corpus answers about a proper's appointed Scripture."""
    # `_chronology.chronology` resolves an omitted profile to the corpus's
    # declared default. Resolve it once here as well, before any query or early
    # return, so the audit record names the policy that actually produced it
    # instead of recording the empty spelling by which the caller requested
    # that policy. `load` is cached, and every locus query reaches the same
    # cached corpus through the chronology seam below.
    effective_profile = profile or _chronology.load(corpus_root).default_profile
    state, reason = formulary_state(document)
    if state != APPOINTED:
        # Empty, and valid: the record exists, says which identity it is for,
        # and says in the corpus's absence why it lists nothing. A gate can
        # regenerate and compare it like any other, and a leaf carrying it
        # still may not print a chronology claim, because there is no element
        # for one to be true of.
        return Dossier(
            document=document,
            calendar=CALENDAR,
            mass="",
            system=REQUIRED_NUMBERING,
            profile=effective_profile,
            state=state,
            reason=reason,
            elements=(),
        )
    mass_key, _mass = mass_of(document, root)
    elements = []
    for key, name, refs, loci in appointed(document, root):
        answers: list[tuple[str, str, str, list[Claim]]] = []
        for locus in loci:
            status, reason, found = _claims_at(
                locus, effective_profile, corpus_root
            )
            answers.append((locus, status, reason, found))
        claims = _all_claims(answers)
        status, reason = _audit_status(answers)
        publication_claims, publication_status, publication_reason = (
            _common_claims(answers)
        )
        elements.append(
            Element(
                key=key,
                name=name,
                refs=refs,
                loci=loci,
                status=status,
                reason=reason,
                claims=claims,
                publication_status=publication_status,
                publication_reason=publication_reason,
                publication_claims=publication_claims,
            )
        )
    return Dossier(
        document=document,
        calendar=CALENDAR,
        mass=mass_key,
        system=REQUIRED_NUMBERING,
        profile=effective_profile,
        state=state,
        reason=reason,
        elements=tuple(elements),
    )


# --- From the audit record to publication annotations ----------------------

ABSOLUTE_POINT = re.compile(
    r"\A(?P<about>about )?(?P<year>[0-9]+) "
    r"(?P<era>A\.D\.|B\.C\.|A\.M\.)\Z"
)
ABSOLUTE_SPAN = re.compile(
    r"\A(?P<first>[0-9]+) (?P<era>A\.D\.|B\.C\.|A\.M\.)(?:-| to )"
    r"(?P<last>[0-9]+) (?P=era)\Z"
)


def _is_century_notation(span: re.Match[str]) -> bool:
    """Whether interval endpoints only notate one or more whole centuries.

    The corpus profile's ``display.century_notation`` contract says these
    endpoints are storage normalization and neither endpoint is asserted. The
    A B.C. envelope starts on a hundred and ends on a year ending in 01; an
    A.D. or A.M. envelope runs in the other direction. Multi-century envelopes
    such as Job's retain the same signature.
    """
    first = int(span.group("first"))
    last = int(span.group("last"))
    if span.group("era") == "B.C.":
        return first % 100 == 0 and last % 100 == 1
    return first % 100 == 1 and last % 100 == 0


RELATION_LABELS = {
    "composition": "Composition",
    "final-formation": "Final formation",
    "textual-attestation": "Textual attestation",
    "narrated-event": "Event",
    "utterance": "Utterance",
    "historical-setting": "Historical setting",
    "superscription-setting": "Superscription setting",
    "retrospective-event": "Retrospective event",
    "prophecy-given": "Prophecy given",
    "prophetic-referent": "Prophetic referent",
}

GAP_DISPLAY = {
    "undated-in-tradition": "Undated in the traditional chronology corpus",
    "research-pending": "Chronology research pending",
    "not-alignable": "Chronology not alignable",
    "textually-distinct": "Textually distinct chronology",
    NONUNIFORM: "No single date applies across every cited locus",
}


def concise_display_label(claim: Claim) -> str:
    """A compact, deterministic display of one structured corpus date.

    Absolute endpoints are merely respelled; no endpoint or precision is
    changed. A relative claim cannot safely be shortened by clipping the
    source sentence, because a second clause can hold a second bound. Its
    projection therefore retains the full source wording, changing only the
    initial capitalization and terminal punctuation.
    """
    point = ABSOLUTE_POINT.match(claim.date)
    if point:
        prefix = "c. " if point.group("about") else ""
        return f"{prefix}{point.group('era')} {point.group('year')}"
    span = ABSOLUTE_SPAN.match(claim.date)
    if span:
        if _is_century_notation(span):
            label = claim.label.strip()
            return label[:1].upper() + label[1:]
        approximate = bool(
            re.search(r"\b(?:about|approx(?:imately)?\.?)\b", claim.label, re.I)
        )
        prefix = "c. " if approximate else ""
        return (
            f"{prefix}{span.group('era')} {span.group('first')}\N{EN DASH}"
            f"{span.group('last')}"
        )
    if claim.precision == "relative":
        label = claim.label.strip().rstrip(".")
        return label[:1].upper() + label[1:]
    if claim.precision == "boundary":
        label = claim.date.strip()
        return label[:1].upper() + label[1:]
    if claim.precision == "duration":
        return f"Duration: {claim.date}"
    return claim.date


def _annotation_claim(claim: Claim) -> AnnotationClaim:
    return AnnotationClaim(
        subject=claim.subject,
        title=claim.title,
        relation=claim.relation,
        label=claim.label,
        display_label=concise_display_label(claim),
        date=claim.date,
        precision=claim.precision,
        disposition=claim.disposition,
        profile=claim.profile,
        sources=claim.sources,
        reaches=claim.reaches,
    )


def _group_status(claims: tuple[AnnotationClaim, ...]) -> str:
    """The most cautious disposition represented by a relation group."""
    dispositions = {claim.disposition for claim in claims}
    if "disputed" in dispositions:
        return "disputed"
    if "preferred" in dispositions:
        return "preferred"
    return "alternate"


def _gap_group(relation: str, status: str, reason: str) -> AnnotationGroup:
    return AnnotationGroup(
        relation=relation,
        status=status or "research-pending",
        reason=reason,
        claims=(),
    )


def annotations(found: Dossier) -> AnnotationProjection:
    """Project a dossier into complete, grouped publication annotations.

    Only elements with appointed Scripture need a Date cell. Every candidate
    in the element-wide publication intersection occurs exactly once in its
    relation group; locus-specific audit claims remain in ``Element.claims``
    and are never promoted to the whole Date cell. A Gospel also always carries
    a narrated-event group. When the corpus supplies only composition
    chronology, that empty group makes the missing event chronology explicit
    instead of letting the book's composition date masquerade as the episode's
    date.
    """
    projected: list[AnnotationElement] = []
    for element in found.elements:
        if not element.loci:
            continue

        by_relation: dict[str, list[AnnotationClaim]] = {}
        for claim in element.publication_claims:
            by_relation.setdefault(claim.relation, []).append(
                _annotation_claim(claim)
            )

        groups: list[AnnotationGroup] = []
        for relation, claims in by_relation.items():
            held = tuple(
                sorted(
                    claims,
                    key=lambda claim: (
                        _chronology.DISPOSITIONS.index(claim.disposition),
                        claim.date,
                        claim.label,
                        claim.subject,
                    ),
                )
            )
            groups.append(
                AnnotationGroup(
                    relation=relation,
                    status=_group_status(held),
                    reason="",
                    claims=held,
                )
            )

        # A scriptural element with no assertions still needs a visible answer
        # in its Date cell.  Composition is the date of the text itself, and is
        # the only relation a bare corpus gap can honestly stand for here.
        if not groups:
            groups.append(
                _gap_group(
                    "composition",
                    element.publication_status,
                    element.publication_reason,
                )
            )

        # Gospel dossiers promise both the episode and the text's composition.
        # `composition-only` otherwise makes the first one disappear silently.
        if element.key == "gospel" and "narrated-event" not in by_relation:
            has_locus_specific_event = any(
                claim.relation == "narrated-event"
                for claim in element.claims
            )
            if has_locus_specific_event:
                groups.append(
                    _gap_group(
                        "narrated-event",
                        NONUNIFORM,
                        "No single narrated-event assertion applies across "
                        "every cited locus; the audit record retains the "
                        "locus-specific event answers.",
                    )
                )
            else:
                groups.append(
                    _gap_group(
                        "narrated-event",
                        "research-pending",
                        "No narrated-event assertion applies to the appointed "
                        "Gospel loci; the corpus supplies no event date here.",
                    )
                )

        groups.sort(
            key=lambda group: (
                _chronology.RELATION_ORDER.get(group.relation, 999),
                group.relation,
            )
        )
        projected.append(
            AnnotationElement(
                key=element.key,
                name=element.name,
                refs=element.refs,
                status=element.publication_status,
                groups=tuple(groups),
            )
        )

    return AnnotationProjection(
        document=found.document,
        calendar=found.calendar,
        mass=found.mass,
        system=found.system,
        profile=found.profile,
        state=found.state,
        reason=found.reason,
        elements=tuple(projected),
    )


def annotation_payload(found: AnnotationProjection) -> dict[str, object]:
    """The JSON-ready annotation contract, with source and display labels."""
    return {
        "status": "ok",
        "schema": ANNOTATIONS_SCHEMA,
        "projection_type": ANNOTATIONS_TYPE,
        "document": found.document,
        "calendar": found.calendar,
        "mass": found.mass,
        "system": found.system,
        "profile": found.profile,
        "formulary": found.state,
        "formulary_reason": found.reason,
        "generated_by": ANNOTATIONS_GENERATOR,
        "elements": [
            {
                "key": element.key,
                "name": element.name,
                "refs": list(element.refs),
                "status": element.status,
                "groups": [
                    {
                        "relation": group.relation,
                        "status": group.status,
                        "reason": group.reason,
                        "claims": [
                            {
                                "subject": claim.subject,
                                "title": claim.title,
                                "relation": claim.relation,
                                # The corpus/source's exact words.  The
                                # display label below is only a projection.
                                "label": claim.label,
                                "display_label": claim.display_label,
                                "date": claim.date,
                                "precision": claim.precision,
                                "disposition": claim.disposition,
                                "profile": claim.profile,
                                "sources": list(claim.sources),
                                "reaches": [
                                    {
                                        "locus": reach.locus,
                                        "inherited": reach.inherited,
                                        "scope": reach.scope,
                                    }
                                    for reach in claim.reaches
                                ],
                            }
                            for claim in group.claims
                        ],
                    }
                    for group in element.groups
                ],
            }
            for element in found.elements
        ],
    }


def _relation_label(relation: str) -> str:
    return RELATION_LABELS.get(relation, relation.replace("-", " ").title())


def _gap_display(group: AnnotationGroup) -> str:
    if group.relation == "narrated-event" and group.status == "research-pending":
        return "No narrated-event date in the chronology corpus"
    if group.relation == "narrated-event" and group.status == NONUNIFORM:
        return "No single narrated-event assertion applies across every cited locus"
    return GAP_DISPLAY.get(group.status, group.status.replace("-", " ").capitalize())


def _group_display(group: AnnotationGroup) -> str:
    relation = _relation_label(group.relation)
    if not group.claims:
        return f"{relation} -- {_gap_display(group)}."
    values = _candidate_display(group, lambda claim: claim.display_label)
    qualifier = f" -- {group.status}" if group.status != "preferred" else ""
    sentence = f"{relation}{qualifier}: {values}"
    return sentence if sentence.endswith((".", "?", "!", "\N{HORIZONTAL ELLIPSIS}")) else sentence + "."


def render_annotations_text(found: AnnotationProjection) -> str:
    """A compact human-readable view of the annotation projection."""
    if not found.elements:
        return (found.reason or "No scriptural element resolved for this formulary") + "\n"
    lines: list[str] = []
    for element in found.elements:
        lines.append(element.key)
        lines.extend(f"  {_group_display(group)}" for group in element.groups)
    return "\n".join(lines) + "\n"


TEX_ESCAPE = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "_": r"\_",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
    "\N{EN DASH}": "--",
    "\N{EM DASH}": "---",
    "\N{HORIZONTAL ELLIPSIS}": "...",
}


def tex_escape(value: str) -> str:
    """Plain corpus text made safe inside one generated TeX argument."""
    return "".join(TEX_ESCAPE.get(char, char) for char in value)


def _tex_claim(claim: AnnotationClaim) -> str:
    arguments = (
        claim.subject,
        claim.relation,
        claim.profile,
        claim.disposition,
        claim.label,
        claim.display_label,
    )
    reach_provenance = "".join(
        "\\chronologyannotationreach"
        f"{{{tex_escape(reach.locus)}}}"
        f"{{{tex_escape(reach.scope)}}}"
        f"{{{'true' if reach.inherited else 'false'}}}"
        for reach in claim.reaches
    )
    return reach_provenance + "\\chronologyannotationclaim" + "".join(
        "{" + tex_escape(value) + "}" for value in arguments
    )


def _candidate_display(group: AnnotationGroup, render_claim) -> str:
    """All candidates, compactly labelled when dispositions differ."""
    buckets = {
        disposition: [
            render_claim(claim)
            for claim in group.claims
            if claim.disposition == disposition
        ]
        for disposition in _chronology.DISPOSITIONS
    }
    nonempty = [name for name, values in buckets.items() if values]
    if len(nonempty) == 1:
        return "; ".join(buckets[nonempty[0]])

    segments: list[str] = []
    labels = {
        "preferred": "Preferred",
        "alternate": "alternatives",
        "disputed": "disputed",
    }
    for disposition in _chronology.DISPOSITIONS:
        values = buckets[disposition]
        if values:
            segments.append(f"{labels[disposition]} {', '.join(values)}")
    return "; ".join(segments)


def _tex_group(group: AnnotationGroup) -> str:
    relation = _relation_label(group.relation)
    if not group.claims:
        visible = f"{relation} -- {_gap_display(group)}."
    else:
        values = _candidate_display(group, _tex_claim)
        plain_values = _candidate_display(group, lambda claim: claim.display_label)
        qualifier = f" -- {group.status}" if group.status != "preferred" else ""
        visible = f"{relation}{qualifier}: {values}"
        if not plain_values.endswith((".", "?", "!", "\N{HORIZONTAL ELLIPSIS}")):
            visible += "."
    return (
        "\\chronologyannotationgroup"
        f"{{{tex_escape(group.relation)}}}"
        f"{{{tex_escape(group.status)}}}"
        f"{{{visible}}}"
    )


def render_annotations_tex(found: AnnotationProjection) -> str:
    """Canonical generated TeX definitions for a proper's Date cells."""
    lines = [
        "% Generated. Do not edit.",
        "% Deterministic projection of research/chronology.toml.",
        f"% schema: {ANNOTATIONS_SCHEMA}",
        f"% document: {found.document}",
        f"% generated-by: {ANNOTATIONS_GENERATOR}",
        # These are intentionally `newcommand`, not `providecommand`. This
        # generated artifact owns the public annotation seam and is input once;
        # a prior definition must make TeX fail rather than silently replace
        # the checked display with unchecked content.
        r"\newcommand{\chronologyannotationclaim}[6]{#6}",
        r"\newcommand{\chronologyannotationreach}[3]{}",
        r"\newcommand{\chronologyannotationgroup}[3]{#3}",
        r"\newcommand{\chronologyannotation}[1]{%",
        r"  \ifcsname triptychchronologyannotation@#1\endcsname",
        r"    \csname triptychchronologyannotation@#1\endcsname",
        r"  \else",
        r"    \PackageError{triptych}{No chronology annotation for #1}{}%",
        r"  \fi}",
    ]
    for element in found.elements:
        lines.extend(
            (
                f"% {element.key}: {tex_escape(element.name)}",
                "\\expandafter\\def\\csname "
                f"triptychchronologyannotation@{tex_escape(element.key)}"
                r"\endcsname{%",
            )
        )
        for index, group in enumerate(element.groups):
            spacer = r"\space " if index else ""
            lines.append(f"  {spacer}{_tex_group(group)}%")
        lines.append("}")
    return "\n".join(lines) + "\n"


def annotations_path(leaf: Path) -> Path:
    return leaf / ANNOTATIONS_RECORD


# --- Rendering the record ---------------------------------------------------

HEADER = """\
# Generated. Do not edit.
#
# What the Scripture chronology corpus answers about this proper's appointed
# loci, written by `{generator}` and held
# against the corpus by `check-content-preflight`. Every field
# here is the corpus's, carried so that the guide's prose can be regenerated
# without re-researching the fact: `guidance/scripture-chronology.md` §14.
#
# `formulary` is `appointed` when the calendar appoints this identity a Mass
# formulary, and `no-calendar-formulary` when it does not — a ritual Mass,
# appointed by a rite rather than by a day, which the calendar sources here do
# not encode. In that state the record lists no element, `formulary_reason`
# says why, and no date may be supplied from anywhere else to fill the gap.
#
# `label` is the source's own words and the only value a manually authored
# guide may display. `date` is the normalized form, for comparison and never
# for a manual page. The sole permitted display exception is the deterministic
# `tools/tpt proper-chronology annotations` projection: it may render its
# concise `display_label` because the same generated contract retains the raw
# `label` and claim `profile`. No manual consumer may mint or edit one. An
# element's `claims` are the full audit union of assertions resolved at any of
# its appointed loci; each claim's nested `reaches` records every locus, corpus
# scope, and inheritance route by which it was returned. `publication_claims`
# is the exact across-all-loci intersection that the generated one-cell
# annotation may display. `status` and `reason` summarize the audit answer;
# `publication_status` and `publication_reason` describe that safe
# intersection. An element with no `status` cites no Scripture; one whose
# publication status is
# `undated-in-tradition` or `research-pending` has no date to print, and the
# guide states that absence rather than filling it. `nonuniform` means its loci
# have chronology but share no one assertion an element-wide Date cell could
# truthfully print.
"""


def _string(value: str) -> str:
    """A TOML basic string. Every escape TOML requires, and no others."""
    out = []
    for char in value:
        if char == "\\":
            out.append("\\\\")
        elif char == '"':
            out.append('\\"')
        elif char == "\n":
            out.append("\\n")
        elif char == "\r":
            out.append("\\r")
        elif char == "\t":
            out.append("\\t")
        elif ord(char) < 0x20 or ord(char) == 0x7F:
            out.append(f"\\u{ord(char):04X}")
        else:
            out.append(char)
    return '"' + "".join(out) + '"'


def _array(values) -> str:
    return "[" + ", ".join(_string(str(value)) for value in values) + "]"


def _field(name: str, value) -> str:
    if isinstance(value, bool):
        return f"{name} = {'true' if value else 'false'}"
    if isinstance(value, (tuple, list)):
        return f"{name} = {_array(value)}"
    if isinstance(value, int):
        return f"{name} = {value}"
    return f"{name} = {_string(str(value))}"


def _render_claim(lines: list[str], table: str, claim: Claim) -> None:
    """Append one claim and its complete reach provenance as TOML tables."""
    lines.append("")
    lines.append(f"[[{table}]]")
    for name in Claim._fields:
        if name != "reaches":
            lines.append(_field(name, getattr(claim, name)))
    for reach in claim.reaches:
        lines.append("")
        lines.append(f"[[{table}.reaches]]")
        for name in Reach._fields:
            lines.append(_field(name, getattr(reach, name)))


def render(found: Dossier) -> str:
    """The record's canonical bytes. One dossier renders one way, always."""
    lines = [HEADER.format(generator=GENERATOR), ""]
    lines.append(_field("schema", RECORD_SCHEMA))
    lines.append(_field("record_type", RECORD_TYPE))
    lines.append(_field("document", found.document))
    lines.append(_field("calendar", found.calendar))
    lines.append(_field("mass", found.mass))
    lines.append(_field("system", found.system))
    lines.append(_field("profile", found.profile))
    lines.append(_field("formulary", found.state))
    lines.append(_field("formulary_reason", found.reason))
    lines.append(_field("generated_by", GENERATOR))
    for element in found.elements:
        lines.append("")
        lines.append("[[elements]]")
        lines.append(_field("key", element.key))
        lines.append(_field("name", element.name))
        lines.append(_field("refs", element.refs))
        lines.append(_field("loci", element.loci))
        lines.append(_field("status", element.status))
        lines.append(_field("reason", element.reason))
        lines.append(_field("publication_status", element.publication_status))
        lines.append(_field("publication_reason", element.publication_reason))
        for claim in element.claims:
            _render_claim(lines, "elements.claims", claim)
        for claim in element.publication_claims:
            _render_claim(lines, "elements.publication_claims", claim)
    return "\n".join(lines) + "\n"


def record_path(leaf: Path) -> Path:
    return leaf / RECORD
