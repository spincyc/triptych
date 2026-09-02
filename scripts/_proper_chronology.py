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
RECORD_SCHEMA = 1
RECORD_TYPE = "proper-chronology"
GENERATOR = "tools/tpt proper-chronology record"

# The numbering the calendar must declare for a locus to cross into the corpus
# unconverted. Both sides spell it the same word; neither is trusted to.
REQUIRED_NUMBERING = _chronology.PREFERRED_SYSTEM


class ChronologyWiringError(ValueError):
    """A proper whose appointed loci cannot be resolved, with the reason."""


class Claim(NamedTuple):
    """One assertion the corpus makes, reduced to what a leaf may print.

    `label` is the source's own words and is the only field a guide displays;
    `date` is the normalized form and is carried for sorting and comparison,
    never for the page. The ids — `subject`, `relation`, `profile` — are what
    §14 requires a consumer to carry, so that the prose above can be
    regenerated from the corpus rather than re-researched.

    `basis` and `note` are deliberately absent. They run to thousands of
    characters of provenance prose, they are the corpus's to state, and a copy
    of them here would be a second place they could be edited. A reader who
    wants them runs `tools/tpt scripture-chronology query <locus> --evidence`.
    """

    locus: str
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
    inherited: bool
    scope: str
    sources: tuple[str, ...]

    def sort_key(self) -> tuple:
        return (self.relation, self.subject, self.date, self.label, self.locus)


class Element(NamedTuple):
    """One appointed element of the formulary, with its loci and their dates."""

    key: str
    name: str
    refs: tuple[str, ...]
    loci: tuple[str, ...]
    status: str
    reason: str
    claims: tuple[Claim, ...]


class Dossier(NamedTuple):
    """Everything the corpus answers about one proper's appointed Scripture."""

    document: str
    calendar: str
    mass: str
    system: str
    profile: str
    elements: tuple[Element, ...]

    def element(self, key: str) -> Element | None:
        for item in self.elements:
            if item.key == key:
                return item
        return None


# --- From a leaf id to its mass --------------------------------------------

# The identity prefix a leaf id carries. `tools/check-proper-identity` owns the
# grammar and the scope gate has already refused an unregistered one by the
# time anything here runs; this only needs the prefix in order to look the mass
# up, so it matches the prefix and nothing else about the slug.
PREFIX = re.compile(r"\A([0-9]{2}|[fm][0-9]{2})-")


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
            f"Scripture; `tools/tpt check-proper-identity` is the check that "
            f"refuses this at the scope gate"
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
            locus=str(answer.locus),
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
            inherited=item.inherited,
            scope=item.scope,
            sources=tuple(item.claim.sources),
        )
        for item in answer.assertions
    ]
    return answer.status, answer.note, claims


def _joined_status(statuses: list[str]) -> str:
    """The most substantive status any of an element's loci carries.

    An element cited across several verses can be dated at one and undated at
    another, and the element's own status is the strongest of them — which is
    `STATUS_ORDER`'s own ordering, not a second ranking written here.
    """
    if not statuses:
        return ""
    return min(statuses, key=lambda status: _chronology.STATUS_ORDER.get(status, 99))


def dossier(
    document: str,
    root: Path = ROOT,
    profile: str | None = None,
    corpus_root: Path | None = None,
) -> Dossier:
    """Everything the corpus answers about a proper's appointed Scripture."""
    mass_key, _mass = mass_of(document, root)
    elements = []
    for key, name, refs, loci in appointed(document, root):
        statuses: list[str] = []
        reasons: list[str] = []
        claims: dict[tuple, Claim] = {}
        for locus in loci:
            status, reason, found = _claims_at(locus, profile, corpus_root)
            statuses.append(status)
            if reason and reason not in reasons:
                reasons.append(reason)
            for claim in found:
                # One assertion reaching six appointed verses is one fact, and
                # the locus it is filed under is the first verse it reached, so
                # that the record does not print a book-wide composition date
                # once per verse of a ten-verse pericope.
                claims.setdefault(claim.sort_key()[:4], claim)
        elements.append(
            Element(
                key=key,
                name=name,
                refs=refs,
                loci=loci,
                status=_joined_status(statuses),
                reason=reasons[0] if reasons else "",
                claims=tuple(sorted(claims.values(), key=Claim.sort_key)),
            )
        )
    return Dossier(
        document=document,
        calendar=CALENDAR,
        mass=mass_key,
        system=REQUIRED_NUMBERING,
        profile=profile or "",
        elements=tuple(elements),
    )


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
# `label` is the source's own words and the only field a guide may display.
# `date` is the normalized form, for comparison and never for the page. An
# element with no `status` cites no Scripture; an element whose status is
# `undated-in-tradition` or `research-pending` has no date to print, and the
# guide states that absence rather than filling it.
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
        for claim in element.claims:
            lines.append("")
            lines.append("[[elements.claims]]")
            for name in Claim._fields:
                lines.append(_field(name, getattr(claim, name)))
    return "\n".join(lines) + "\n"


def record_path(leaf: Path) -> Path:
    return leaf / RECORD
