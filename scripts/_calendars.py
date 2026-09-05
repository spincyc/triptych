#!/usr/bin/env python3
"""What may live under `src/sources/calendars`, and which tool owns each kind.

A calendar directory used to hold exactly one kind of file, so the tools that
read it discovered their inputs with `rglob("*.yaml")` and treated whatever they
found as a mass index. That was an accident of there being only one kind, not a
decision that there could only ever be one: the moment a second kind of
calendar-scoped source landed beside `propers.yaml`, every one of those globs
read it as a mass index and failed on its missing `sections`.

So discovery is by the declared schema, and it lives here once. A file whose
schema names a kind another tool owns is skipped and *reported as skipped*; a
file whose schema is recognised by nobody is a hard failure. Silently ignoring
an unclassifiable file would be worse than the noisy failure it replaces --- a
mass index with a mistyped schema string would simply stop being checked.

It owns the other half of that seam too: which header fields a companion may
*not* carry. A calendar directory describes one book, and the mass index is the
file that identifies it. A companion that retypes the identity is a second copy
with nothing comparing it to the first, which is what `restated_identity`
refuses.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tomllib
from _tooling import prune_cache
from datetime import date as calendar_date
from pathlib import Path

# `yaml` is imported where it is parsed, not here. Every tool that touches a
# calendar imports this module, and PyYAML costs 6.8ms to import --- for a
# parse that, with the cache warm, usually never happens.

MASS_INDEX_SCHEMA = "triptych-calendar-masses/v1"
MASS_INDEX = "propers.yaml"

# Every other schema that legitimately sits in a calendar directory, with the
# tool that validates it. Adding a kind of calendar source means adding a line
# here and nowhere else.
COMPANION_SCHEMAS = {
    "triptych-calendar-rubrics/v1": "calendar-rubrics",
}

# The identity of the book a calendar's masses are printed in. Both fields
# belong to the mass index, because that is the file that transcribes the book;
# a companion source in the same directory names the same book but is not what
# identifies it, and reads these from the index instead of writing them out
# again. `restated_identity` refuses the second copy.
#
# `edition` identifies the printing bibliographically. `edition_short` is the
# name a reader would say — "1962 Missal" — because a select control has room
# for one of them and a reader has patience for one of them, and it is not the
# sixty-eight characters of "Missale Romanum, editio typica tertia 2008,
# reimpressio emendata 2008".
INDEX_OWNED = ("edition", "edition_short")

# The one way a mass or a proper says "this text is appointed here, and it is
# printed there". The books say it constantly and this schema could not: a
# fourth-class feria takes the preceding Sunday's Mass, a resumed Sunday after
# the Epiphany takes that Sunday's orations under the twenty-third Sunday after
# Pentecost's chants, a third-class saint takes a whole Mass from the Commune
# Sanctorum and supplies only a Collect. With no way to say it, the only way to
# carry such a day was to retype the text beside itself, and the copies drift:
# `resumed-epiphany-5` and `epiphany-5` held one Collect twice and disagreed at
# `caelestis` against `coelestis`, four such pairs disagreeing in five ways.
#
# `mass` names a mass key in the same file, `form` one of that mass's forms,
# and — on a proper only — `proper` the slot to take, defaulting to the
# referring proper's own name. `citation` records the edition's own printed
# pointer ("Missa Statuit, de Communi unius Martyris I loco [4]"), which is the
# evidence that the reference is the book's and not the reader's.
TAKES_FROM = "takes_from"
COMMON_SETS = "common_sets"
REFERENCE_FIELDS = ("mass", "form", "proper", "citation", "note", COMMON_SETS)
# A proper that takes its text from elsewhere holds no text of its own. Naming
# the slot twice is the restatement this key exists to remove, so the incipit
# comes from the resolved proper and may not be retyped beside the reference.
REFERENCE_EXCLUDES = (
    "source", "text", "verses", "cycles", "weekday_cycles", "incipit", "translations",
)

# A source Proper can state why it is not one cumulative member of the normal
# Ordinary frame.  This is row-local because alternatives and exceptional
# before/after-frame material are facts about the exact appointment, including
# a referenced appointment, rather than about a same-named slot everywhere.
ORDINARY_DISPOSITION = "ordinary_disposition"
ORDINARY_DISPOSITION_KINDS = frozenset({"alternative", "unplaced"})
ORDINARY_ALTERNATIVE_FIELDS = frozenset({"kind", "group", "option", "basis"})
ORDINARY_UNPLACED_FIELDS = frozenset({"kind", "group", "region", "basis"})
ORDINARY_UNPLACED_REGIONS = frozenset({"before-frame", "after-frame"})
ORDINARY_DISPOSITION_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

# --------------------------------------------------------------- recensions
#
# A recension is one state of a rite held as its DEPARTURES from another state,
# never as a second copy of it. guidance/recensions.md Rule 2 owns the rule; this
# is the mechanism, and it lives here because `resolve_propers` lives here and
# there must be exactly one way to resolve a day.
#
# Two relations are declared, and they are deliberately not the same field,
# because collapsing them is how a record ends up asserting that the older book
# descends from the newer one:
#
#   `text_from`     MECHANICAL. The calendar that supplies every entry this file
#                   does not state. It is a statement about where text has been
#                   transcribed in THIS REPOSITORY, not about which book came
#                   first. Today it points from the pre-1955 recension at
#                   `roman-1962`, because the 1962 typical edition is the only
#                   printing anyone here has read a proper from.
#
#   `stands_before` HISTORICAL. A non-empty list of ids in the acts inventory,
#                   naming the acts explicitly used to bound this recension.
#                   Nothing mechanical reads it. It is the claim
#                   about descent, and it is kept in the vocabulary of acts
#                   because guidance/the-shape.md section 7 fixes the station as
#                   the act and not the book.
#
# So a file may say "I stand before Maxima Redemptionis" and "my untouched
# entries were read from a 1962 printing" at once, and both are true. That is
# guidance/recensions.md Rule 2a -- attestation is separated from residence --
# and it is what lets a recension be declared before anything is transcribed.
RECENSION = "recension"
RECENSION_BASE = "text_from"
RECENSION_ACT = "stands_before"
RECENSION_ACT_INVENTORY = "latin-missal-acts-v1.toml"
RECENSION_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

# A recension's short departure file is not evidence that the unstated book was
# checked and found equal to its base.  `recension_coverage` makes that boundary
# executable: every domain is accounted for, inherited material says how far it
# was collated, and each evidence or blocker row uses a closed vocabulary.  The
# prose in guidance/recensions.md Rule 4 remains the explanation; this is the
# part a gate can refuse when it drifts.
RECENSION_COVERAGE = "recension_coverage"
RECENSION_COVERAGE_SCHEMA = "triptych-recension-coverage/v1"
RECENSION_COVERAGE_FIELDS = frozenset(
    {"schema", "as_of", "status", "domains", "inheritance", "evidence", "blockers"}
)
RECENSION_COVERAGE_STATUSES = frozenset({"structural-only", "partial", "complete"})
RECENSION_COVERAGE_DOMAINS = (
    "calendar",
    "precedence",
    "propers",
    "commons",
    "ordinary",
    "ceremonies",
)
RECENSION_DOMAIN_FIELDS = frozenset({"state", "basis"})
RECENSION_DOMAIN_STATES = frozenset(
    {
        "unexamined",
        "none",
        "structural-only",
        "partial",
        "complete",
        "inherited-uncollated",
        "blocked-by-model",
        "out-of-scope",
    }
)
RECENSION_INHERITANCE_FIELDS = frozenset({"source_calendar", "status", "basis"})
RECENSION_INHERITANCE_STATUSES = frozenset({"uncollated", "partial", "complete"})
RECENSION_EVIDENCE_FIELDS = frozenset(
    {"id", "domains", "grade", "record", "basis", "witnesses"}
)
RECENSION_EVIDENCE_GRADES = frozenset(
    {"located-only", "ocr-structure-read", "source-read", "page-image-collated"}
)
RECENSION_BLOCKER_FIELDS = frozenset({"id", "kind", "status", "record", "requirement"})
RECENSION_BLOCKER_KINDS = frozenset(
    {
        "missing-witness",
        "unregistered-artifact",
        "page-image-collation",
        "rights-restriction",
        "schema-gap",
        "unmodeled-recension",
        "provenance-gap",
        "data-transcription",
        "scope-exclusion",
    }
)
RECENSION_BLOCKER_STATUSES = frozenset({"open", "blocked"})

# guidance/recensions.md section 3 fixes this vocabulary. It is closed here so a
# misspelt kind fails instead of being read as a departure nobody classified.
DEPARTURE = "departure"
DEPARTURE_KINDS = (
    "absent",  # the base has this mass; this recension does not
    "added",  # this recension has one the base does not
    "replaced",  # both have it and the text differs
    "renamed",  # the same formulary under another name or key
    "moved",  # the same liturgy on another day, or at another hour
    "reslotted",  # the same words in a different slot
    "unrecorded",  # known to differ, correspondence not established
)
# Which kinds require the base to hold the key, and which require it not to.
# `added` is the only one that names something the base has never had; every
# other kind is a statement ABOUT a base entry, so a key the base does not hold
# is a reference that resolves to nothing -- the defect of guidance/the-shape.md
# section 1, in the one file written to prevent it.
DEPARTURE_NEEDS_BASE = tuple(k for k in DEPARTURE_KINDS if k != "added")
# A departure that resolves to the base entry unchanged, with only the scalar
# fields the recension restates overlaid. `renamed` and `moved` say the liturgy
# is the same one; restating its propers beside it would be the second copy
# Rule 2 exists to refuse.
DEPARTURE_OVERLAYS = ("renamed", "moved")
# Scalar fields a `renamed` or `moved` departure may overlay onto the base entry.
# Anything outside this list would be a silent edit of the base's text.
OVERLAY_FIELDS = ("name", "title", "date", "rank", "day", "hour", "key")
# Every departure must say what established it. A departure with no basis is a
# difference someone asserted, which is precisely what this vocabulary exists to
# keep apart from a difference someone read.
DEPARTURE_BASIS = "basis"
# The act-history station or attribution record for one departure claim. It is
# optional: leaving it unset says that no honest station has been established.
# An `unrecorded` difference may name the later station that inventories it;
# consumers must not restate every such station as a causal instrument.
DEPARTURE_ACT = "act"
# One liturgy can depart in several ways at once, and the Triduum is where that
# is the rule rather than the exception: the pre-1955 Holy Saturday service is
# the same liturgy MOVED to another hour, RENAMED, and REPLACED in most of its
# lessons. Forcing one kind per row would make the file choose which of those to
# record and drop the rest, so the primary `departure` is the one the machinery
# acts on and `also` carries the others, each with its own basis. Every kind in
# `also` is checked against the same closed vocabulary, so the secondary claims
# are held to the primary one's standard rather than living in prose.
DEPARTURE_ALSO = "also"

# A YAML top-level key sits at column zero, which is what makes this cheap scan
# equivalent to a parse for the one field it wants.
SCHEMA_LINE = re.compile(r"^schema:[ \t]*(?:['\"])?([^'\"\s#]+)", re.MULTILINE)
_HEADER_LINES: dict[str, re.Pattern[str]] = {}


def _header_line(field: str) -> re.Pattern[str]:
    if field not in _HEADER_LINES:
        _HEADER_LINES[field] = re.compile(
            rf"^{re.escape(field)}:[ \t]*(.+?)[ \t]*$", re.MULTILINE
        )
    return _HEADER_LINES[field]


def declared_schema(path: Path) -> str | None:
    """The `schema` a calendar source declares, or None if it declares none."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = SCHEMA_LINE.search(text)
    return found.group(1) if found else None


def header(path: Path, field: str) -> str | None:
    """A one-line top-level scalar a calendar source declares, or None."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = _header_line(field).search(text)
    return found.group(1).strip("'\"") if found else None


def index_header(root: Path, calendar: str, field: str) -> str | None:
    """A header field read from the calendar's mass index and nowhere else."""
    return header(root / calendar / MASS_INDEX, field)


def partition(root: Path, calendar: str | None = None) -> tuple[list[Path], list[dict], list[str]]:
    """Split a calendar root into mass indexes, companions, and complaints.

    Returns `(indexes, companions, problems)`. `companions` records each file
    another tool owns, so a caller can say what it did not check rather than
    leaving the reader to infer it from a count.
    """
    if not root.is_dir():
        raise ValueError(f"missing calendar root: {root}")

    indexes: list[Path] = []
    companions: list[dict] = []
    problems: list[str] = []

    for path in sorted(root.rglob("*.yaml")):
        if calendar is not None and path.parent.name != calendar:
            continue
        schema = declared_schema(path)
        if schema == MASS_INDEX_SCHEMA:
            indexes.append(path)
        elif schema in COMPANION_SCHEMAS:
            companions.append(
                {
                    "path": path.as_posix(),
                    "schema": schema,
                    "owner": COMPANION_SCHEMAS[schema],
                }
            )
        else:
            problems.append(
                f"{path}: declares schema {schema!r}, which is neither the mass index "
                f"{MASS_INDEX_SCHEMA!r} nor a companion kind "
                f"({', '.join(sorted(COMPANION_SCHEMAS))}). A calendar source must "
                "declare a schema this repository recognises, so that a mistyped one "
                "fails instead of going unchecked."
            )

    return indexes, companions, problems


def restated_identity(root: Path, calendar: str | None = None) -> list[str]:
    """Every companion source that writes out an identity the index owns.

    `edition` sat hand-typed in both files of both calendar directories — four
    copies of two strings, with nothing in the repository comparing them. They
    happened to agree; nothing made them agree. This same repository has held
    one census in three copies that all disagreed, and a README restating four
    totals its own table gave differently, so agreement between hand-typed
    copies is a fact about a moment and not a property of the data.

    So a companion carrying one of these fields fails here whether or not its
    value matches. The disagreement is the symptom; the second copy is the
    defect, and it is the only thing a check can catch before the drift.
    """
    problems: list[str] = []
    _, companions, _ = partition(root, calendar)
    for companion in companions:
        path = Path(companion["path"])
        index = root / path.parent.name / MASS_INDEX
        for field in INDEX_OWNED:
            found = header(path, field)
            if found is None:
                continue
            owned = header(index, field)
            if found == owned:
                problems.append(
                    f"{path}: restates {field} {found!r}, which {index} owns and "
                    f"{companion['owner']} reads from there. Delete the line: a copy "
                    "that agrees today is a disagreement that has not happened yet."
                )
            else:
                problems.append(
                    f"{path}: declares {field} {found!r} while {index} declares "
                    f"{owned!r}. Two files claim a different book for the same "
                    f"calendar; the mass index is the owner, and {companion['owner']} "
                    "reads it from there. Delete the line."
                )
    return problems


_YAML_CACHE = Path(__file__).resolve().parents[1] / "build" / "yaml-cache"
_YAML_CACHE_VERSION = "1"
_YAML_CACHE_FLOOR = 256 * 1024
# Unlike the tree-fingerprinted caches, this one is keyed PER FILE, so every
# eligible file is "current" at once and they do not take turns. There are 38
# over the floor in this checkout; a retention below that number evicts a file
# another tool is about to ask for and the cache thrashes instead of hitting.
# Generous on purpose: an entry is a parsed copy of a file that already exists.
_YAML_CACHE_KEEP = 128


def _cache_entry(path: Path, kind: str = "yaml") -> Path | None:
    """Where this file's parsed form is kept, or None where it is not cached."""
    if os.environ.get("TRIPTYCH_YAML_CACHE") == "0":
        return None
    try:
        stat = path.stat()
    except OSError:
        return None
    if stat.st_size < _YAML_CACHE_FLOOR:
        return None
    key = "\0".join(
        (_YAML_CACHE_VERSION, kind, str(path.resolve()),
         str(stat.st_mtime_ns), str(stat.st_size))
    )
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return _YAML_CACHE / digest[:2] / f"{digest}.json"


def _yaml_error() -> type[BaseException]:
    """PyYAML's error base, resolved only when something has already failed."""
    import yaml  # noqa: PLC0415

    return yaml.YAMLError


def read_yaml(path: Path):
    """Read a YAML file with the fastest SAFE loader this machine has.

    `yaml.safe_load` is the pure-Python scanner, and it was the whole cost of
    answering a single date: 2.1 of the 2.5 seconds `calendar-days day` took
    were spent scanning a megabyte of `propers.yaml` character by character,
    and `mass-propers show --bible` spent as much again on a 1.3 MB bible
    index. libyaml parses the same bytes about eight times faster.

    It is the same derivation over the same input and not a shortcut past one.
    That claim was checked rather than assumed: both loaders were run over
    every `propers.yaml` in this repository and the documents compared equal.
    `CSafeLoader` is the C SAFE loader — it constructs no arbitrary Python
    objects, exactly as `safe_load` does not — and where libyaml is not
    installed this falls back to the pure-Python one and only the speed
    changes.

    Above libyaml sits a parse cache, because the cost was never one parse.
    `tests/tools/*.test` makes 421 tool invocations, each a cold interpreter,
    and the tools compose each other as commands on purpose --- `mass-today`'s
    `invoke` says why --- so a single `mass-today show` is four processes
    re-scanning the same unchanged megabytes. A saving that does not outlive a
    process is no saving here, so the cache is a file: the parsed document as
    JSON under ignored `build/`, which `guidance/repository.md` already names
    as where caches live. Loading it costs 0.010s against libyaml's 0.49s and
    the pure-Python scanner's 2.09s for the 2.2 MB postconciliar propers.

    It caches the derivation rather than adding a second one, and that is
    checked per file every time an entry is written, not assumed once. A
    document reaches the cache only if `json.loads(json.dumps(document))`
    compares equal to it, so a file JSON cannot carry exactly is never cached
    and is parsed as it always was --- two of this repository's 31 YAML files
    today. The gate is that equality rather than a bare `try` because JSON
    coerces silently: a mapping keyed by integers survives `json.dumps` and
    returns keyed by strings, which is the reference that resolves
    successfully and wrongly, and `guidance/the-shape.md` names that as the
    one defect this repository exists to refuse.

    The key is the file's path, mtime and size, so an edited calendar misses
    rather than needing an invalidation anybody has to remember. Files below
    `_YAML_CACHE_FLOOR` are parsed directly: they are already faster than the
    round trip, and the suite writes thousands of small sandbox fixtures whose
    entries would never be read twice. `TRIPTYCH_YAML_CACHE=0` disables it.
    """
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return _cached_parse(
        path, "yaml", lambda text: yaml.load(text, Loader=loader)
    )


def read_toml(path: Path):
    """Read a TOML file, with the same parse cache `read_yaml` uses.

    `tomllib` is the pure-Python parser and there is no C one in the standard
    library, so the repository's ledgers cost what they weigh: 0.196s for the
    5.5 MB staleness inventory, 0.153s for the 4.2 MB Latin provenance. Every
    tool that answers one question about one proper paid both, in a fresh
    process, because the ledger is where the answer lives. Through the cache
    they load in 0.006s and 0.005s.

    The same round-trip gate applies and matters more here than for YAML: TOML
    has native dates and times, and JSON has not. A ledger carrying one is
    simply never cached and is parsed as it always was, rather than coming back
    with a string where a date went in.
    """
    import tomllib

    return _cached_parse(path, "toml", tomllib.loads)


def _cached_parse(path: Path, kind: str, parse):
    """Parse *path* with *parse*, through the JSON cache described above."""
    entry = _cache_entry(path, kind)
    if entry is not None:
        try:
            return json.loads(entry.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass

    document = parse(path.read_text(encoding="utf-8"))

    if entry is not None:
        try:
            encoded = json.dumps(document)
            if json.loads(encoded) == document:
                entry.parent.mkdir(parents=True, exist_ok=True)
                # Written aside and renamed, because these run in parallel and
                # a half-written entry read by a sibling is a wrong answer.
                aside = entry.with_suffix(f".{os.getpid()}.tmp")
                aside.write_text(encoded, encoding="utf-8")
                os.replace(aside, entry)
                prune_cache(_YAML_CACHE, keep=_YAML_CACHE_KEEP, pattern='**/*.json')
        except (OSError, TypeError, ValueError, RecursionError):
            pass

    return document


def _read(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"no calendar index at {path}")
    document = read_yaml(path)
    if not isinstance(document, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return document


def base_of(root: Path, calendar: str) -> str | None:
    """The calendar a recension takes its unstated entries from, or None.

    Read with the cheap header scan rather than a parse, because callers ask
    this of every directory before deciding whether to load anything.
    """
    found = header(root / calendar / MASS_INDEX, RECENSION_BASE)
    return found or None


def departures_of(document: dict) -> list[tuple[str, dict, dict]]:
    """Every departure the document states, as (section, section body, mass)."""
    out: list[tuple[str, dict, dict]] = []
    for section, body in sorted((document.get("sections") or {}).items()):
        if not isinstance(body, dict):
            continue
        for mass in body.get("masses") or []:
            if isinstance(mass, dict):
                out.append((section, body, mass))
    return out


def load_document(
    root: Path,
    calendar: str,
    effective: bool = True,
    _chain: tuple[str, ...] = (),
) -> dict:
    """A calendar's document: for a recension, the base with its departures applied.

    This is the single derivation, and every tool that serves a day reads it
    from here. A calendar that declares no `text_from` is returned exactly as it
    sits on disk, so the two existing calendars are untouched by this path.

    `effective=False` returns the file as written, which is what the census
    counts: the size of a recension is the size of its DIFF, and a census that
    counted the merged document would report the base's mass count under the
    recension's name and call the projection large. guidance/versification.md
    section 8.0 settles the same point for editions -- the default rule writes no
    row, so the projection measures distance rather than volume.
    """
    if calendar in _chain:
        cycle = " -> ".join((*_chain, calendar))
        raise ValueError(f"calendar recension inheritance cycle: {cycle}")
    document = _read(root / calendar / MASS_INDEX)
    base_name = document.get(RECENSION_BASE)
    if not effective or not isinstance(base_name, str) or not base_name:
        return document
    base = load_document(root, base_name, effective=True, _chain=(*_chain, calendar))
    return _apply_departures(document, base, base_name)


def _also(mass: dict) -> list[dict]:
    found = mass.get(DEPARTURE_ALSO)
    return [row for row in found if isinstance(row, dict)] if isinstance(found, list) else []


def _stamp(
    mass: dict,
    calendar: str,
    kind: str,
    basis: str,
    stated: bool,
    also: list[dict] | tuple = (),
    act: str = "",
) -> dict:
    """Mark a mass with how the recension reached it, so a page can say so.

    guidance/recensions.md Rule 2a: a text attested by only one printing says so.
    An entry carried through from the base with no departure is exactly that
    case, and it is the overwhelming majority, so the stamp goes on every entry
    rather than only on the interesting ones. A renderer that finds no stamp is
    reading a calendar that is nobody's recension.
    """
    out = dict(mass)
    stamp = {
        "calendar": calendar,
        "kind": kind,
        "stated": stated,
        "text_from": "" if stated else calendar,
        "basis": basis,
        "also": [],
    }
    if act:
        stamp[DEPARTURE_ACT] = act
    for row in also:
        secondary = {
            "kind": str(row.get(DEPARTURE) or ""),
            "basis": str(row.get(DEPARTURE_BASIS) or ""),
        }
        secondary_act = str(row.get(DEPARTURE_ACT) or "")
        if secondary_act:
            secondary[DEPARTURE_ACT] = secondary_act
        stamp["also"].append(secondary)
    out[RECENSION] = stamp
    return out


def _residence_of(mass: dict, fallback: str) -> str:
    """The calendar where inherited words reside, through any middle states."""
    held = mass.get(RECENSION)
    if not isinstance(held, dict):
        return fallback
    if held.get("stated"):
        return str(held.get("calendar") or fallback)
    return str(held.get("text_from") or held.get("calendar") or fallback)


def _apply_departures(document: dict, base: dict, base_name: str) -> dict:
    calendar = str(document.get("calendar") or "")
    stated: dict[str, dict] = {}
    for _, _, mass in departures_of(document):
        key = str(mass.get("key") or "")
        if key:
            stated[key] = mass

    merged: dict[str, dict] = {}
    for section, body in sorted((base.get("sections") or {}).items()):
        if not isinstance(body, dict):
            continue
        kept: list[dict] = []
        for mass in body.get("masses") or []:
            if not isinstance(mass, dict):
                continue
            key = str(mass.get("key") or "")
            departure = stated.pop(key, None)
            if departure is None:
                # A multi-hop recension must retain the calendar in which the
                # words actually reside. Re-stamping A's text as B merely
                # because C inherits through B creates false provenance.
                kept.append(
                    dict(mass)
                    if isinstance(mass.get(RECENSION), dict)
                    else _stamp(mass, base_name, "", "", stated=False)
                )
                continue
            kind = str(departure.get(DEPARTURE) or "")
            basis = str(departure.get(DEPARTURE_BASIS) or "")
            also = _also(departure)
            if kind == "absent":
                # Dropped outright. The reason lives in the departure row and is
                # reported by `recension_problems` if it is missing, so an
                # absence can never be silent.
                continue
            if kind in DEPARTURE_OVERLAYS:
                carried = dict(mass)
                for field in OVERLAY_FIELDS:
                    if field in departure:
                        carried[field] = departure[field]
                kept.append(
                    _stamp(
                        carried,
                        _residence_of(mass, base_name),
                        kind,
                        basis,
                        stated=False,
                        also=also,
                        act=str(departure.get(DEPARTURE_ACT) or ""),
                    )
                )
                continue
            if kind == "unrecorded":
                # Known to differ, correspondence not established. The base entry
                # is carried so the day still resolves, and the stamp is what
                # stops the page claiming the base's text was checked.
                kept.append(
                    _stamp(
                        mass,
                        _residence_of(mass, base_name),
                        kind,
                        basis,
                        stated=False,
                        also=also,
                        act=str(departure.get(DEPARTURE_ACT) or ""),
                    )
                )
                continue
            # replaced, reslotted: the recension's own entry wins outright.
            kept.append(
                _stamp(
                    departure,
                    calendar,
                    kind,
                    basis,
                    stated=True,
                    also=also,
                    act=str(departure.get(DEPARTURE_ACT) or ""),
                )
            )
        merged[section] = dict(body, masses=kept)

    # `added`, and anything whose key the base does not hold. The latter is a
    # defect `recension_problems` reports; it is still carried here so that one
    # bad row does not silently remove a mass from the served calendar.
    for key, departure in stated.items():
        section = _section_for(document, key) or "seasonal"
        body = merged.setdefault(section, dict((base.get("sections") or {}).get(section) or {}, masses=[]))
        body["masses"] = [
            *body.get("masses", []),
            _stamp(
                departure,
                calendar,
                str(departure.get(DEPARTURE) or "added"),
                str(departure.get(DEPARTURE_BASIS) or ""),
                stated=True,
                also=_also(departure),
                act=str(departure.get(DEPARTURE_ACT) or ""),
            ),
        ]

    out = {k: v for k, v in document.items() if k != "sections"}
    out["sections"] = merged
    return out


def _section_for(document: dict, key: str) -> str | None:
    for section, _, mass in departures_of(document):
        if str(mass.get("key") or "") == key:
            return section
    return None


def _coverage_shape(
    problems: list[str], where: str, node: object, required: frozenset[str]
) -> dict:
    if not isinstance(node, dict):
        problems.append(f"{where} must be a mapping")
        return {}
    fields = set(node)
    missing = sorted(required - fields)
    unknown = sorted(fields - required)
    if missing:
        problems.append(f"{where} is missing required fields: {', '.join(missing)}")
    if unknown:
        problems.append(f"{where} has unknown fields: {', '.join(unknown)}")
    return node


def _coverage_text(problems: list[str], where: str, node: dict, field: str) -> None:
    value = node.get(field)
    if not isinstance(value, str) or not value.strip():
        problems.append(f"{where}.{field} must be a non-empty string")


def _walk(value: object):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _markdown_anchor(text: str, wanted: str) -> bool:
    """Whether a Markdown heading owns the GitHub-style fragment ``wanted``."""
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        label = match.group(1).strip().lower()
        slug = re.sub(r"[^\w\- ]", "", label, flags=re.UNICODE)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        if slug == wanted:
            return True
    return False


def _contained_reference_path(repository: Path, relative: Path) -> Path | None:
    """Resolve a repository reference without following a symlink out of it."""

    try:
        root = repository.resolve()
        source = (root / relative).resolve()
    except (OSError, RuntimeError):
        return None
    return source if source.is_relative_to(root) else None


def _coverage_record_problem(repository: Path, reference: object, where: str) -> str | None:
    """Resolve one coverage evidence/blocker record, including its local locus."""
    if not isinstance(reference, str) or not reference.strip():
        return f"{where} must be a non-empty repo-relative reference"
    raw_path, marker, selector = reference.partition("#")
    relative = Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        return f"{where} must be repo-relative, got {reference!r}"
    source = _contained_reference_path(repository, relative)
    if source is None:
        return f"{where} escapes the repository through a symlink: {reference!r}"
    if not source.is_file():
        return f"{where} names missing record {raw_path!r}"
    if not marker or not selector:
        return None
    if source.suffix == ".md":
        try:
            text = source.read_text(encoding="utf-8")
        except OSError as error:
            return f"{where} cannot inspect {raw_path!r}: {error}"
        if not _markdown_anchor(text, selector):
            return f"{where} names absent heading #{selector} in {raw_path}"
        return None
    try:
        if source.suffix == ".toml":
            held = tomllib.loads(source.read_text(encoding="utf-8"))
        elif source.suffix == ".json":
            held = json.loads(source.read_text(encoding="utf-8"))
        elif source.suffix in {".yaml", ".yml"}:
            held = read_yaml(source)
        else:
            return f"{where} cannot resolve a fragment in {raw_path!r}"
    except (OSError, ValueError, tomllib.TOMLDecodeError, _yaml_error()) as error:
        return f"{where} cannot inspect {raw_path!r}: {error}"
    wanted = selector.removeprefix("id=")
    if isinstance(held, dict) and wanted in held:
        return None
    if any(isinstance(row, dict) and row.get("id") == wanted for row in _walk(held)):
        return None
    return f"{where} names absent record id {wanted!r} in {raw_path}"


def _repository_for_calendar_root(root: Path) -> Path:
    """The repository owning a canonical or synthetic calendar root."""
    if (
        root.name == "calendars"
        and root.parent.name == "sources"
        and root.parent.parent.name == "src"
    ):
        return root.parent.parent.parent
    return root.parent


def _act_ids(
    source: Path,
    chain: tuple[Path, ...] = (),
    boundary: Path | None = None,
) -> set[str]:
    """Act ids from the authoritative inventory and every file it extends."""
    try:
        boundary = boundary or source.parent.resolve()
        source = source.resolve()
    except (OSError, RuntimeError) as error:
        raise ValueError(f"cannot resolve authoritative act inventory {source}: {error}") from error
    if not source.is_relative_to(boundary):
        raise ValueError(f"act inventory escapes its local directory through a symlink: {source}")
    if source in chain:
        route = " -> ".join(str(path) for path in (*chain, source))
        raise ValueError(f"act inventory extends cycle: {route}")
    if not source.is_file():
        raise ValueError(f"no authoritative act inventory at {source}")
    try:
        document = tomllib.loads(source.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValueError(f"cannot read authoritative act inventory {source}: {error}") from error
    if document.get("acts_schema") != 1:
        raise ValueError(f"{source}: acts_schema must be 1")
    found = {
        row["id"]
        for row in document.get("acts") or []
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    extends = document.get("extends")
    if extends is not None:
        if (
            not isinstance(extends, str)
            or not extends.strip()
            or Path(extends).is_absolute()
            or ".." in Path(extends).parts
        ):
            raise ValueError(f"{source}: extends must be a local relative filename")
        found.update(_act_ids(source.parent / extends, (*chain, source), boundary))
    return found


def recension_coverage_problems(
    path: Path,
    document: dict,
    base_name: str,
    *,
    repository: Path | None = None,
) -> list[str]:
    """Validate what a recension independently establishes and merely inherits."""
    problems: list[str] = []
    where = f"{path}: {RECENSION_COVERAGE}"
    coverage = _coverage_shape(
        problems, where, document.get(RECENSION_COVERAGE), RECENSION_COVERAGE_FIELDS
    )
    if not coverage:
        return problems
    if coverage.get("schema") != RECENSION_COVERAGE_SCHEMA:
        problems.append(
            f"{where}.schema must be {RECENSION_COVERAGE_SCHEMA!r}, got "
            f"{coverage.get('schema')!r}"
        )
    as_of = coverage.get("as_of")
    if not isinstance(as_of, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of):
        problems.append(f"{where}.as_of must be a quoted ISO date, got {as_of!r}")
    else:
        try:
            calendar_date.fromisoformat(as_of)
        except ValueError:
            problems.append(f"{where}.as_of is not a calendar date: {as_of!r}")
    status = coverage.get("status")
    if not isinstance(status, str) or status not in RECENSION_COVERAGE_STATUSES:
        problems.append(
            f"{where}.status must be one of "
            f"{', '.join(sorted(RECENSION_COVERAGE_STATUSES))}, got {status!r}"
        )

    domains = coverage.get("domains")
    if not isinstance(domains, dict):
        problems.append(f"{where}.domains must be a mapping")
        domains = {}
    domain_keys = set(domains)
    missing_domains = sorted(set(RECENSION_COVERAGE_DOMAINS) - domain_keys)
    unknown_domains = sorted(domain_keys - set(RECENSION_COVERAGE_DOMAINS))
    if missing_domains:
        problems.append(
            f"{where}.domains is missing required domains: {', '.join(missing_domains)}"
        )
    if unknown_domains:
        problems.append(f"{where}.domains has unknown domains: {', '.join(unknown_domains)}")
    for domain in RECENSION_COVERAGE_DOMAINS:
        if domain not in domains:
            continue
        row_where = f"{where}.domains.{domain}"
        row = _coverage_shape(
            problems, row_where, domains.get(domain), RECENSION_DOMAIN_FIELDS
        )
        if not row:
            continue
        if not isinstance(row.get("state"), str) or row.get("state") not in RECENSION_DOMAIN_STATES:
            problems.append(
                f"{row_where}.state must be one of "
                f"{', '.join(sorted(RECENSION_DOMAIN_STATES))}, got {row.get('state')!r}"
            )
        _coverage_text(problems, row_where, row, "basis")

    inheritance_where = f"{where}.inheritance"
    inheritance = _coverage_shape(
        problems,
        inheritance_where,
        coverage.get("inheritance"),
        RECENSION_INHERITANCE_FIELDS,
    )
    if inheritance:
        if inheritance.get("source_calendar") != base_name:
            problems.append(
                f"{inheritance_where}.source_calendar must equal {RECENSION_BASE} "
                f"{base_name!r}, got {inheritance.get('source_calendar')!r}"
            )
        if (
            not isinstance(inheritance.get("status"), str)
            or inheritance.get("status") not in RECENSION_INHERITANCE_STATUSES
        ):
            problems.append(
                f"{inheritance_where}.status must be one of "
                f"{', '.join(sorted(RECENSION_INHERITANCE_STATUSES))}, got "
                f"{inheritance.get('status')!r}"
            )
        _coverage_text(problems, inheritance_where, inheritance, "basis")

    evidence = coverage.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        problems.append(f"{where}.evidence must be a non-empty list")
        evidence = []
    evidence_ids: set[str] = set()
    for index, candidate in enumerate(evidence):
        row_where = f"{where}.evidence[{index}]"
        row = _coverage_shape(
            problems, row_where, candidate, RECENSION_EVIDENCE_FIELDS
        )
        if not row:
            continue
        _coverage_text(problems, row_where, row, "id")
        identifier = row.get("id")
        if isinstance(identifier, str):
            if not RECENSION_ID.fullmatch(identifier):
                problems.append(f"{row_where}.id is not kebab-case: {identifier!r}")
            if identifier in evidence_ids:
                problems.append(f"{row_where}.id {identifier!r} is repeated")
            evidence_ids.add(identifier)
        stated_domains = row.get("domains")
        if not isinstance(stated_domains, list) or not stated_domains:
            problems.append(f"{row_where}.domains must be a non-empty list")
        else:
            invalid = sorted({
                repr(one)
                for one in stated_domains
                if not isinstance(one, str) or one not in RECENSION_COVERAGE_DOMAINS
            })
            if invalid:
                problems.append(f"{row_where}.domains has unknown domains: {', '.join(invalid)}")
            if len(stated_domains) != len(set(map(str, stated_domains))):
                problems.append(f"{row_where}.domains repeats a domain")
        if (
            not isinstance(row.get("grade"), str)
            or row.get("grade") not in RECENSION_EVIDENCE_GRADES
        ):
            problems.append(
                f"{row_where}.grade must be one of "
                f"{', '.join(sorted(RECENSION_EVIDENCE_GRADES))}, got {row.get('grade')!r}"
            )
        _coverage_text(problems, row_where, row, "record")
        if problem := _coverage_record_problem(
            repository or _repository_for_calendar_root(path.parent.parent),
            row.get("record"),
            f"{row_where}.record",
        ):
            problems.append(problem)
        _coverage_text(problems, row_where, row, "basis")
        witnesses = row.get("witnesses")
        if (
            not isinstance(witnesses, list)
            or not witnesses
            or any(not isinstance(one, str) or not one.strip() for one in witnesses)
        ):
            problems.append(f"{row_where}.witnesses must be a non-empty list of strings")
        elif len(witnesses) != len(set(witnesses)):
            problems.append(f"{row_where}.witnesses repeats a witness")

    blockers = coverage.get("blockers")
    if not isinstance(blockers, list):
        problems.append(f"{where}.blockers must be a list")
        blockers = []
    blocker_ids: set[str] = set()
    blocker_kinds: set[str] = set()
    for index, candidate in enumerate(blockers):
        row_where = f"{where}.blockers[{index}]"
        row = _coverage_shape(
            problems, row_where, candidate, RECENSION_BLOCKER_FIELDS
        )
        if not row:
            continue
        _coverage_text(problems, row_where, row, "id")
        identifier = row.get("id")
        if isinstance(identifier, str):
            if not RECENSION_ID.fullmatch(identifier):
                problems.append(f"{row_where}.id is not kebab-case: {identifier!r}")
            if identifier in blocker_ids:
                problems.append(f"{row_where}.id {identifier!r} is repeated")
            blocker_ids.add(identifier)
        kind = row.get("kind")
        if not isinstance(kind, str) or kind not in RECENSION_BLOCKER_KINDS:
            problems.append(
                f"{row_where}.kind must be one of "
                f"{', '.join(sorted(RECENSION_BLOCKER_KINDS))}, got {kind!r}"
            )
        elif isinstance(kind, str):
            blocker_kinds.add(kind)
        if (
            not isinstance(row.get("status"), str)
            or row.get("status") not in RECENSION_BLOCKER_STATUSES
        ):
            problems.append(
                f"{row_where}.status must be one of "
                f"{', '.join(sorted(RECENSION_BLOCKER_STATUSES))}, got "
                f"{row.get('status')!r}"
            )
        _coverage_text(problems, row_where, row, "record")
        if problem := _coverage_record_problem(
            repository or _repository_for_calendar_root(path.parent.parent),
            row.get("record"),
            f"{row_where}.record",
        ):
            problems.append(problem)
        _coverage_text(problems, row_where, row, "requirement")

    if status == "complete" and blockers:
        problems.append(f"{where}.status is complete but blockers remain")
    if status == "complete":
        incomplete = [
            domain
            for domain in RECENSION_COVERAGE_DOMAINS
            if not isinstance(domains.get(domain), dict)
            or domains[domain].get("state") != "complete"
        ]
        if incomplete:
            problems.append(
                f"{where}.status is complete but these domains are not complete: "
                f"{', '.join(incomplete)}"
            )
        if inheritance.get("status") != "complete":
            problems.append(
                f"{where}.status is complete but inheritance.status is not complete"
            )
    if status != "complete" and not blockers:
        problems.append(f"{where}.status {status!r} requires at least one blocker")
    if status == "structural-only" and not any(
        isinstance(domains.get(domain), dict)
        and domains[domain].get("state") == "structural-only"
        for domain in RECENSION_COVERAGE_DOMAINS
    ):
        problems.append(
            f"{where}.status is structural-only but no domain has state structural-only"
        )
    if any(
        isinstance(domains.get(domain), dict)
        and domains[domain].get("state") == "blocked-by-model"
        for domain in RECENSION_COVERAGE_DOMAINS
    ) and "schema-gap" not in blocker_kinds:
        problems.append(f"{where} has a domain blocked-by-model but no schema-gap blocker")
    return problems


def recension_problems(root: Path, calendar: str) -> list[str]:
    """Every way a recension's departures fail to mean anything.

    guidance/recensions.md section 6 item 2 asks for exactly this check: one that
    fails when a recension's base does not exist, and when a departure names a
    mass the base does not hold. A row pointing at nothing is the same defect as
    a citation that resolves wrongly, and it is worse here, because a departure
    that resolves to nothing removes a Mass from the calendar instead of adding a
    broken link to it.
    """
    problems: list[str] = []
    path = root / calendar / MASS_INDEX
    try:
        document = _read(path)
    except ValueError as error:
        return [str(error)]
    base_name = document.get(RECENSION_BASE)
    if not isinstance(base_name, str) or not base_name:
        return []
    if not (root / base_name / MASS_INDEX).is_file():
        return [
            f"{path}: {RECENSION_BASE} names calendar {base_name!r}, which this "
            f"repository has no {MASS_INDEX} for. A recension whose base does not "
            "exist serves nothing and says nothing."
        ]
    if base_name == calendar:
        return [f"{path}: {RECENSION_BASE} points at itself"]
    historical_acts = document.get(RECENSION_ACT)
    known_acts: set[str] = set()
    if not isinstance(historical_acts, list) or not historical_acts:
        problems.append(
            f"{path}: declares {RECENSION_BASE} without {RECENSION_ACT}. A recension "
            "must give a non-empty list of acts it stands before, because `text_from` records where "
            "text was transcribed and is not a claim about which book came first."
        )
    else:
        invalid_acts = [
            act
            for act in historical_acts
            if not isinstance(act, str) or not RECENSION_ID.fullmatch(act)
        ]
        if invalid_acts:
            problems.append(
                f"{path}: {RECENSION_ACT} entries must be act ids, got {invalid_acts!r}"
            )
        if len(historical_acts) != len(set(map(str, historical_acts))):
            problems.append(f"{path}: {RECENSION_ACT} repeats an act id")
        act_source = root.parent / "inventories" / RECENSION_ACT_INVENTORY
        try:
            known_acts = _act_ids(act_source)
        except ValueError as error:
            problems.append(f"{path}: cannot resolve {RECENSION_ACT}: {error}")
        else:
            for historical_act in historical_acts:
                if isinstance(historical_act, str) and historical_act not in known_acts:
                    problems.append(
                        f"{path}: {RECENSION_ACT} names unknown act {historical_act!r} in "
                        f"{act_source}"
                    )
    problems.extend(
        recension_coverage_problems(
            path,
            document,
            base_name,
            repository=_repository_for_calendar_root(root),
        )
    )
    try:
        base = load_document(root, base_name, effective=True, _chain=(calendar,))
    except (OSError, ValueError) as error:
        problems.append(f"{path}: cannot resolve {RECENSION_BASE}: {error}")
        return problems
    held = mass_index(base)
    seen: set[str] = set()
    for _, _, mass in departures_of(document):
        key = str(mass.get("key") or "")
        where = f"{path}: departure {key or '(no key)'!r}"
        if not key:
            problems.append(f"{where}: every departure needs the key it departs in")
            continue
        if key in seen:
            problems.append(f"{where}: stated twice; a departure has one row")
        seen.add(key)
        kind = mass.get(DEPARTURE)
        if kind not in DEPARTURE_KINDS:
            problems.append(
                f"{where}: {DEPARTURE} must be one of {', '.join(DEPARTURE_KINDS)}, "
                f"got {kind!r}"
            )
            continue
        if not str(mass.get(DEPARTURE_BASIS) or "").strip():
            problems.append(
                f"{where}: {kind} departure states no {DEPARTURE_BASIS}. A difference "
                "with no basis is a difference someone asserted."
            )
        departure_act = mass.get(DEPARTURE_ACT)
        if departure_act is not None:
            if not isinstance(departure_act, str) or not RECENSION_ID.fullmatch(departure_act):
                problems.append(
                    f"{where}: {DEPARTURE_ACT} is not an act id: {departure_act!r}"
                )
            elif departure_act not in known_acts:
                problems.append(
                    f"{where}: {DEPARTURE_ACT} names unknown act {departure_act!r}"
                )
        if kind in DEPARTURE_NEEDS_BASE and key not in held:
            problems.append(
                f"{where}: {kind} names a mass {base_name!r} does not hold. Only "
                "`added` may name a key the base has never had."
            )
        if kind == "added" and key in held:
            problems.append(
                f"{where}: added names a mass {base_name!r} already holds; that is "
                "`replaced`, not `added`."
            )
        found = mass.get(DEPARTURE_ALSO)
        if found is not None and not isinstance(found, list):
            problems.append(f"{where}: {DEPARTURE_ALSO} must be a list of departures")
            continue
        for row in found or []:
            if not isinstance(row, dict):
                problems.append(f"{where}: every {DEPARTURE_ALSO} entry is a mapping")
                continue
            secondary = row.get(DEPARTURE)
            if secondary not in DEPARTURE_KINDS:
                problems.append(
                    f"{where}: {DEPARTURE_ALSO} {DEPARTURE} must be one of "
                    f"{', '.join(DEPARTURE_KINDS)}, got {secondary!r}"
                )
            if secondary == kind:
                problems.append(
                    f"{where}: {DEPARTURE_ALSO} repeats the primary kind {kind!r}; "
                    "a second row saying the same thing is a restatement, not a "
                    "second departure"
                )
            if not str(row.get(DEPARTURE_BASIS) or "").strip():
                problems.append(
                    f"{where}: {DEPARTURE_ALSO} {secondary!r} states no "
                    f"{DEPARTURE_BASIS}; a secondary claim is held to the primary "
                    "one's standard"
                )
            secondary_act = row.get(DEPARTURE_ACT)
            if secondary_act is not None:
                if not isinstance(secondary_act, str) or not RECENSION_ID.fullmatch(secondary_act):
                    problems.append(
                        f"{where}: {DEPARTURE_ALSO} {DEPARTURE_ACT} is not an act id: "
                        f"{secondary_act!r}"
                    )
                elif secondary_act not in known_acts:
                    problems.append(
                        f"{where}: {DEPARTURE_ALSO} {DEPARTURE_ACT} names unknown act "
                        f"{secondary_act!r}"
                    )
    return problems


def mass_index(document: dict) -> dict[str, dict]:
    """Every mass in the file, keyed by its `key`, in section order.

    A reference resolves inside one calendar. Reaching across calendars is
    refused on purpose: the 1962 and postconciliar books print different
    prayers under the same names, and a pointer that crossed would be the
    cycle-letter import `guidance/propers-for-agents.md` already forbids.
    """
    out: dict[str, dict] = {}
    for _, body in sorted((document.get("sections") or {}).items()):
        if not isinstance(body, dict):
            continue
        for mass in body.get("masses") or []:
            if isinstance(mass, dict) and isinstance(mass.get("key"), str):
                out.setdefault(mass["key"], mass)
    return out


# ------------------------------------------------- appointed across a span
#
# The books appoint a text on a RANGE of days as readily as on one: the Sequence
# Victimae paschali laudes is said at every Mass from Easter Sunday to Saturday
# in albis, and Veni Sancte Spiritus at every Mass of the octave of Pentecost.
# `takes_from` already carries such a text without copying it, one proper at a
# time. What no file could say was that the twelve days are ONE appointment: the
# Easter span survived as an English sentence in a `notes` string that nothing
# reads and nothing checks, and the Pentecost span was written nowhere at all.
#
# So the span is stated once, in the calendar's `rubrics.yaml`, and the masses
# reference the text as they reference any other. This is the reader, and it is
# the only one: the gate joins these rows to the masses, and a renderer that
# wants to print "appointed daily within the octave" beside a Sequence reads the
# same rows rather than re-deriving the day list from twelve separate entries.
#
# A span states where the text is PRINTED and which masses it is appointed on;
# it never carries the text. The entries are held to their own closed field list
# for the reason `PROPER_FIELDS` is closed in `check-calendar-masses`: a schema
# silent about unrecognised keys turns a typo into a rule nobody applies.
APPOINTED_ACROSS = "appointed_across"
SPAN_FIELDS = frozenset(
    {"id", "label", "prints", "keys", "before", "stated", "locus", "latin", "note"}
)
# Where the text is written out, once: a mass key in the same file and the name
# of one of its propers. Every mass in `keys` takes that proper by reference.
SPAN_PRINTS = "prints"
SPAN_PRINTS_FIELDS = frozenset({"mass", "proper"})
# `stated` is whether this repository has READ the rubric that appoints the
# span, and `locus` is where it read it. They are two fields rather than one
# because a span whose day list this repository is confident of, and whose
# printed rubric it has never seen, is the ordinary case here and must be able
# to say so: `stated: false` with `locus: null` is that sentence. Inventing a
# plausible citation instead would put a fabricated authority behind a real
# reading, which is worse than the missing one.
SPAN_STATED = "stated"
SPAN_LOCUS = "locus"


def spans_of(document: dict) -> list[dict]:
    """Every span a calendar's rubrics state, as written.

    Raw rows, as `departures_of` returns raw masses: the shape is validated by
    the gate that reports on it, so a malformed row is a complaint and not an
    exception thrown out of a reader.
    """
    found = document.get(APPOINTED_ACROSS)
    if not isinstance(found, list):
        return []
    return [row for row in found if isinstance(row, dict)]


def reference_of(node: object) -> dict | None:
    """The `takes_from` mapping a mass or proper carries, if it carries one."""
    if not isinstance(node, dict):
        return None
    found = node.get(TAKES_FROM)
    return found if isinstance(found, dict) else None


def validate_ordinary_disposition(value: object) -> dict:
    """Return one exact row disposition, or refuse a lossy/ambiguous shape."""

    if not isinstance(value, dict):
        raise ValueError(f"{ORDINARY_DISPOSITION} must be a mapping")
    kind = value.get("kind")
    if kind not in ORDINARY_DISPOSITION_KINDS:
        raise ValueError(
            f"{ORDINARY_DISPOSITION}.kind must be one of "
            f"{sorted(ORDINARY_DISPOSITION_KINDS)}, got {kind!r}"
        )
    fields = (
        ORDINARY_ALTERNATIVE_FIELDS
        if kind == "alternative"
        else ORDINARY_UNPLACED_FIELDS
    )
    unknown = sorted(str(field) for field in set(value) - fields)
    missing = sorted(str(field) for field in fields - set(value))
    if unknown:
        raise ValueError(
            f"{ORDINARY_DISPOSITION} {kind!r} carries unknown field(s) "
            + ", ".join(unknown)
        )
    if missing:
        raise ValueError(
            f"{ORDINARY_DISPOSITION} {kind!r} is missing field(s) "
            + ", ".join(missing)
        )
    for field in ("group", "option") if kind == "alternative" else ("group",):
        held = value.get(field)
        if not isinstance(held, str) or not ORDINARY_DISPOSITION_ID.fullmatch(held):
            raise ValueError(
                f"{ORDINARY_DISPOSITION}.{field} must be a nonempty lowercase "
                f"kebab-case string, got {held!r}"
            )
    basis = value.get("basis")
    if not isinstance(basis, str) or not basis.strip():
        raise ValueError(f"{ORDINARY_DISPOSITION}.basis must be a nonempty string")
    if kind == "unplaced" and value.get("region") not in ORDINARY_UNPLACED_REGIONS:
        raise ValueError(
            f"{ORDINARY_DISPOSITION}.region must be one of "
            f"{sorted(ORDINARY_UNPLACED_REGIONS)}, got {value.get('region')!r}"
        )
    # Do not normalize, enrich, or drop evidence.  Public consumers receive the
    # same closed mapping the source supplied.
    return dict(value)


def ordinary_disposition_group_problems(
    key: str,
    entries: list[tuple[str, dict, dict | None]],
) -> list[str]:
    """Validate alternative groups over each resolved source formulary.

    Validation after reference resolution makes the rule self-cleaning: a
    removed option turns its former group into a singleton and a newly added
    row is not silently swept into a choice by its display name.
    """

    problems: list[str] = []
    alternatives: dict[tuple[str, str], list[dict]] = {}
    unplaced: dict[tuple[str, str], list[dict]] = {}
    for form, proper, _ in entries:
        if ORDINARY_DISPOSITION not in proper:
            continue
        name = str(proper.get("name") or "")
        where = (
            f"mass {key}"
            + (f" form {form!r}" if form else "")
            + f" proper {name!r}: {ORDINARY_DISPOSITION}"
        )
        try:
            disposition = validate_ordinary_disposition(
                proper[ORDINARY_DISPOSITION]
            )
        except ValueError as error:
            problems.append(f"{where}: {error}")
            continue
        identity = (form, disposition["group"])
        if disposition["kind"] == "alternative":
            alternatives.setdefault(identity, []).append(disposition)
        else:
            unplaced.setdefault(identity, []).append(disposition)

    for (form, group), members in alternatives.items():
        where = f"mass {key}" + (f" form {form!r}" if form else "")
        if (form, group) in unplaced:
            problems.append(
                f"{where}: {ORDINARY_DISPOSITION} group {group!r} mixes "
                "alternative and unplaced rows"
            )
        options = {str(member["option"]) for member in members}
        if len(options) < 2:
            problems.append(
                f"{where}: alternative {ORDINARY_DISPOSITION} group {group!r} "
                "must retain at least two distinct options"
            )
        bases = {str(member["basis"]) for member in members}
        if len(bases) != 1:
            problems.append(
                f"{where}: alternative {ORDINARY_DISPOSITION} group {group!r} "
                "must carry one identical basis on every member"
            )
    for (form, group), members in unplaced.items():
        where = f"mass {key}" + (f" form {form!r}" if form else "")
        bases = {str(member["basis"]) for member in members}
        if len(bases) != 1:
            problems.append(
                f"{where}: unplaced {ORDINARY_DISPOSITION} group {group!r} "
                "must carry one identical basis on every member"
            )
        regions = {str(member["region"]) for member in members}
        if len(regions) != 1:
            problems.append(
                f"{where}: unplaced {ORDINARY_DISPOSITION} group {group!r} "
                "must carry one identical region on every member"
            )
    return problems


def ordinary_disposition_source_problems(
    key: str,
    form: str,
    propers: list[dict],
) -> list[str]:
    """Validate source-local group runs and out-of-frame boundaries."""

    entries = [(form, proper, None) for proper in propers]
    problems = ordinary_disposition_group_problems(key, entries)
    groups: dict[tuple[str, str], list[int]] = {}
    options: dict[tuple[str, str], list[int]] = {}
    before: list[int] = []
    after: list[int] = []
    for index, proper in enumerate(propers):
        if ORDINARY_DISPOSITION not in proper:
            continue
        try:
            disposition = validate_ordinary_disposition(
                proper[ORDINARY_DISPOSITION]
            )
        except ValueError:
            # The exact-shape problem is already reported by the shared group
            # walk; boundary checks cannot safely interpret a malformed row.
            continue
        kind = str(disposition["kind"])
        group = str(disposition["group"])
        groups.setdefault((kind, group), []).append(index)
        if kind == "alternative":
            options.setdefault((group, str(disposition["option"])), []).append(index)
        elif disposition["region"] == "before-frame":
            before.append(index)
        else:
            after.append(index)

    where = f"mass {key}" + (f" form {form!r}" if form else "")
    for (kind, group), positions in groups.items():
        if positions != list(range(positions[0], positions[-1] + 1)):
            problems.append(
                f"{where}: {kind} {ORDINARY_DISPOSITION} group {group!r} "
                "must occupy one contiguous source-order run"
            )
    for (group, option), positions in options.items():
        if positions != list(range(positions[0], positions[-1] + 1)):
            problems.append(
                f"{where}: alternative {ORDINARY_DISPOSITION} group {group!r} "
                f"option {option!r} must occupy one contiguous source-order bundle"
            )
    if before and before != list(range(0, before[-1] + 1)):
        problems.append(
            f"{where}: before-frame {ORDINARY_DISPOSITION} rows must be an exact "
            "source-order prefix"
        )
    if after and after != list(range(after[0], len(propers))):
        problems.append(
            f"{where}: after-frame {ORDINARY_DISPOSITION} rows must be an exact "
            "source-order suffix"
        )
    return problems


def _form_propers(mass: dict, form: str) -> tuple[list[dict], str | None]:
    """The propers of one form of a mass, or of the mass itself when `form` is empty."""
    forms = mass.get("forms")
    if isinstance(forms, list) and forms:
        if not form:
            names = ", ".join(str(f.get("name")) for f in forms if isinstance(f, dict))
            return [], f"names a mass printed in forms ({names}) without saying which"
        for body in forms:
            if isinstance(body, dict) and str(body.get("name")) == form:
                return [p for p in (body.get("propers") or []) if isinstance(p, dict)], None
        return [], f"names form {form!r}, which that mass does not print"
    if form:
        return [], f"names form {form!r} of a mass printed in no forms"
    return [p for p in (mass.get("propers") or []) if isinstance(p, dict)], None


def resolve_propers(
    document: dict,
    mass: dict,
    chain: tuple[str, ...] = (),
) -> tuple[list[tuple[str, dict, dict | None]], list[str]]:
    """A mass's propers as appointed, following every `takes_from` to its text.

    Returns `(entries, problems)`; each entry is `(form label, proper,
    provenance)`, and `provenance` is `None` for a proper the mass prints
    itself or `{"mass", "form", "proper", "citation"}` for one it takes from
    elsewhere. Nothing is copied into the file: this is the single derivation,
    and both the validator and the browser's structure read it from here.

    A mass carrying `takes_from` starts from the referenced formulary and then
    applies its own `propers` as replacements matched on `name` — which is how
    a third-class saint says "the Mass of the Common, but this Collect".
    A local proper whose name the referenced formulary does not print is
    appended in the order given, because the Missal does add a slot the Common
    lacks and dropping it silently would be worse than an odd position.
    """
    key = str(mass.get("key") or "")
    problems: list[str] = []
    local_propers = [
        proper
        for proper in (mass.get("propers") or [])
        if isinstance(proper, dict)
    ]
    problems.extend(ordinary_disposition_source_problems(key, "", local_propers))
    for form in mass.get("forms") or []:
        if not isinstance(form, dict):
            continue
        label = str(form.get("name") or "form")
        form_propers = [
            proper
            for proper in (form.get("propers") or [])
            if isinstance(proper, dict)
        ]
        problems.extend(
            ordinary_disposition_source_problems(key, label, form_propers)
        )
    reference = reference_of(mass)
    if reference is None:
        base: list[tuple[str, dict, dict | None]] = [
            ("", proper, None)
            for proper in (mass.get("propers") or [])
            if isinstance(proper, dict)
        ]
        for form in mass.get("forms") or []:
            if not isinstance(form, dict):
                continue
            label = str(form.get("name") or "form")
            base.extend(
                (label, proper, None)
                for proper in (form.get("propers") or [])
                if isinstance(proper, dict)
            )
    else:
        overrides = [p for p in (mass.get("propers") or []) if isinstance(p, dict)]
        local_override_families = {
            proper_family(str(proper.get("name") or "")) for proper in overrides
        }
        base, common_families, problems = _resolve_reference(
            document, mass, reference, chain, local_override_families
        )
        base = _apply_overrides(base, overrides, common_families)
        # A dated Mass may appoint the Common except for an own Collect family
        # whose wording is unavailable. Apply local overrides first, then
        # remove only inherited members of that family: a local non-Collect
        # override keeps both its printed position and its own provenance.
        status = mass.get("text_status")
        if (
            isinstance(status, dict)
            and status.get("state") == "unavailable"
            and status.get("scope") == "proper-collect"
        ):
            base = [
                entry
                for entry in base
                if not (
                    str(entry[1].get("name") or "").split(" (", 1)[0] == "Collect"
                    and entry[2] is not None
                )
            ]
    resolved: list[tuple[str, dict, dict | None]] = []
    for label, proper, provenance in base:
        inner = reference_of(proper)
        if inner is None:
            resolved.append((label, proper, provenance))
            continue
        taken, terminal, trouble = _resolve_proper(
            document, key, proper, inner, chain, source_form=label
        )
        problems.extend(trouble)
        if taken is not None:
            resolved.append((label, taken, terminal or _provenance(inner, proper)))
    problems.extend(ordinary_disposition_group_problems(key, resolved))
    return resolved, problems


def _appoint_resolved_proper(found: dict, wrapper: dict, wanted: str) -> dict:
    """Borrow target wording while retaining appointment-local structure."""

    local_name = str(wrapper.get("name") or "")
    if local_name == wanted and ORDINARY_DISPOSITION not in wrapper:
        return found
    appointed = dict(found)
    if local_name != wanted:
        appointed["name"] = local_name
    if ORDINARY_DISPOSITION in wrapper:
        appointed[ORDINARY_DISPOSITION] = wrapper[ORDINARY_DISPOSITION]
    return appointed


def _provenance(reference: dict, proper: dict) -> dict:
    return {
        "mass": str(reference.get("mass") or ""),
        "form": str(reference.get("form") or ""),
        "proper": str(reference.get("proper") or proper.get("name") or ""),
        "citation": str(reference.get("citation") or ""),
    }


def _apply_overrides(
    base: list[tuple[str, dict, dict | None]],
    overrides: list[dict],
    family_overrides: set[str] | None = None,
) -> list[tuple[str, dict, dict | None]]:
    family_overrides = family_overrides or set()
    by_name = {str(p.get("name")): p for p in overrides}
    by_family = {
        proper_family(str(proper.get("name") or "")): proper
        for proper in overrides
        if proper_family(str(proper.get("name") or "")) in family_overrides
    }
    used: set[str] = set()
    used_families: set[str] = set()
    out: list[tuple[str, dict, dict | None]] = []

    def appointed_replacement(replacement: dict, inherited: dict) -> dict:
        # A local override replaces the target's wording at the same appointed
        # slot. Structural disposition belongs to that appointment and survives
        # unless the local row explicitly supplies its own exact disposition.
        if (
            ORDINARY_DISPOSITION in inherited
            and ORDINARY_DISPOSITION not in replacement
        ):
            return {
                **replacement,
                ORDINARY_DISPOSITION: inherited[ORDINARY_DISPOSITION],
            }
        return replacement

    for label, proper, provenance in base:
        name = str(proper.get("name"))
        family = proper_family(name)
        if family in by_family:
            if family in used_families:
                continue
            replacement = by_family[family]
            replacement_name = str(replacement.get("name") or "")
            used.add(replacement_name)
            used_families.add(family)
            out.append((label, appointed_replacement(replacement, proper), None))
        elif name in by_name:
            used.add(name)
            out.append(
                (label, appointed_replacement(by_name[name], proper), None)
            )
        else:
            out.append((label, proper, provenance))
    for proper in overrides:
        if str(proper.get("name")) not in used:
            out.append(("", proper, None))
    return out


def proper_family(name: str) -> str:
    """The stable Proper slot governed by a qualified Common-set member."""

    return name.split(" (", 1)[0]


def _common_set_propers(
    target: dict,
    reference: dict,
    where: str,
    local_override_families: set[str],
) -> tuple[list[dict], set[str], list[str]]:
    """Filter one Common formulary to its selected, or safely unresolved, sets.

    Common catalog entries remain a flat transcription of every printed
    alternative.  A whole-Mass reference must explicitly select one option or
    declare the choice unresolved.  In the latter case the shared formulary is
    still useful, but no alternative member is emitted as though appointed.
    """

    propers = [p for p in (target.get("propers") or []) if isinstance(p, dict)]
    definitions = target.get(COMMON_SETS)
    selected_by_reference = reference.get(COMMON_SETS)
    if definitions is None:
        if selected_by_reference is not None:
            return (
                propers,
                set(),
                [
                    f"{where}: {TAKES_FROM}.{COMMON_SETS} selects a target that "
                    f"defines no {COMMON_SETS}"
                ],
            )
        return propers, set(), []
    if not isinstance(definitions, dict) or not definitions:
        return [], set(), [f"{where}: target {COMMON_SETS} must be a nonempty mapping"]

    selections = selected_by_reference if isinstance(selected_by_reference, dict) else {}
    problems: list[str] = []
    if not isinstance(selected_by_reference, dict):
        problems.append(
            f"{where}: {TAKES_FROM} must disposition every target {COMMON_SETS} group"
        )
    selected_names: set[str] = set()
    grouped_names: set[str] = set()
    governed_families: set[str] = set()
    for group_id, group in definitions.items():
        group_where = f"{where}: {TAKES_FROM}.{COMMON_SETS}.{group_id}"
        if not isinstance(group, dict):
            problems.append(f"{group_where} targets a malformed group")
            continue
        families = group.get("families")
        if isinstance(families, list):
            governed_families.update(
                family for family in families if isinstance(family, str) and family
            )
        options = group.get("options")
        if not isinstance(options, dict):
            problems.append(f"{group_where} targets malformed options")
            continue
        for members in options.values():
            if isinstance(members, list):
                grouped_names.update(
                    member for member in members if isinstance(member, str) and member
                )
        disposition = selections.get(group_id)
        if not isinstance(disposition, dict):
            problems.append(f"{group_where} is not dispositioned")
            continue
        state = disposition.get("state")
        if state == "selected":
            option_id = disposition.get("option")
            members = options.get(option_id) if isinstance(option_id, str) else None
            if not isinstance(members, list):
                problems.append(f"{group_where} names unknown option {option_id!r}")
                continue
            selected_names.update(
                member for member in members if isinstance(member, str) and member
            )
        elif state == "unresolved":
            candidates = disposition.get("candidates")
            if not isinstance(candidates, list) or not candidates:
                problems.append(f"{group_where} unresolved candidates must be nonempty")
            elif any(
                not isinstance(candidate, str) or candidate not in options
                for candidate in candidates
            ):
                problems.append(f"{group_where} carries an unknown unresolved candidate")
            # A local oration remains appointed even when the inherited choice
            # is unresolved. Retain one source-order seat per locally replaced
            # family; `_apply_overrides` substitutes the local body before any
            # result is exposed, so no candidate Common wording escapes.
            seated: set[str] = set()
            for members in options.values():
                if not isinstance(members, list):
                    continue
                for member in members:
                    if not isinstance(member, str):
                        continue
                    family = proper_family(member)
                    if family in local_override_families and family not in seated:
                        selected_names.add(member)
                        seated.add(family)
        else:
            problems.append(f"{group_where}.state must be selected or unresolved")
    extra = sorted(set(selections) - set(definitions), key=str)
    if extra:
        problems.append(
            f"{where}: {TAKES_FROM}.{COMMON_SETS} carries unknown group(s) "
            + ", ".join(repr(group) for group in extra)
        )
    return (
        [
            proper
            for proper in propers
            if str(proper.get("name") or "") not in grouped_names
            or str(proper.get("name") or "") in selected_names
        ],
        governed_families,
        problems,
    )


def _resolve_reference(
    document: dict,
    mass: dict,
    reference: dict,
    chain: tuple[str, ...],
    local_override_families: set[str],
) -> tuple[list[tuple[str, dict, dict | None]], set[str], list[str]]:
    key = str(mass.get("key") or "")
    where = f"mass {key}"
    target_key = reference.get("mass")
    if not isinstance(target_key, str) or not target_key:
        return [], set(), [f"{where}: {TAKES_FROM} needs the key of the mass it takes from"]
    if target_key == key:
        return [], set(), [f"{where}: {TAKES_FROM} points at itself"]
    if target_key in chain:
        route = " -> ".join((*chain, key, target_key))
        return [], set(), [f"{where}: {TAKES_FROM} closes a cycle: {route}"]
    target = mass_index(document).get(target_key)
    if target is None:
        return [], set(), [f"{where}: {TAKES_FROM} names mass {target_key!r}, which this calendar has no entry for"]
    chosen_propers, common_families, set_problems = _common_set_propers(
        target, reference, where, local_override_families
    )
    form = str(reference.get("form") or "")
    if form or isinstance(target.get("forms"), list):
        if target.get(COMMON_SETS) is not None:
            return (
                [],
                common_families,
                [*set_problems, f"{where}: {TAKES_FROM}.{COMMON_SETS} cannot target forms"],
            )
        chosen, trouble = _form_propers(target, form)
        if trouble:
            return [], common_families, [f"{where}: {TAKES_FROM} {trouble}"]
        provenance = {"mass": target_key, "form": form, "proper": "", "citation": str(reference.get("citation") or "")}
        return [("", p, dict(provenance, proper=str(p.get("name") or ""))) for p in chosen], common_families, set_problems
    filtered_target = dict(target)
    filtered_target["propers"] = chosen_propers
    inherited, problems = resolve_propers(document, filtered_target, (*chain, key))
    problems = [*set_problems, *problems]
    citation = str(reference.get("citation") or "")
    # Where the text is PRINTED, not the first hop toward it.
    #
    # `target` may itself take a proper from a third mass, and this loop used to
    # throw the inner provenance away and name `target` regardless. The text was
    # right and the address was wrong, which is the quiet half of the failure:
    # `overlay_key` files a proper's translation under the mass that prints it,
    # so seven days -- Perpetua and Felicitas, Frances of Rome, Petronilla,
    # Elizabeth -- looked up their English at a Common that carries none, found
    # nothing, and rendered Latin while the terminal Common's English sat in the
    # ledger. Keeping the inner provenance makes the address follow the text.
    out = [
        (
            label,
            proper,
            inner
            or {
                "mass": target_key,
                "form": label,
                "proper": str(proper.get("name") or ""),
                "citation": citation,
            },
        )
        for label, proper, inner in inherited
    ]
    return out, common_families, problems


def _resolve_proper(
    document: dict,
    key: str,
    proper: dict,
    reference: dict,
    chain: tuple[str, ...],
    *,
    source_form: str = "",
) -> tuple[dict | None, dict | None, list[str]]:
    name = str(proper.get("name") or "")
    where = f"mass {key} proper {name!r}"
    target_key = reference.get("mass")
    if not isinstance(target_key, str) or not target_key:
        return None, None, [f"{where}: {TAKES_FROM} needs the key of the mass it takes from"]
    form = str(reference.get("form") or "")
    if target_key == key:
        # A book may print one proper once and direct a later sibling form back
        # to it. The explicit, different form is a complete target, not the
        # self-cycle made by a whole Mass pointing at itself. Keep this exception
        # narrow: only a directly printed target proper may cross the sibling
        # edge; same-form and chained sibling references remain refused.
        if not form or form == source_form:
            route = " -> ".join((*chain, key, target_key))
            return None, None, [f"{where}: {TAKES_FROM} closes a cycle: {route}"]
        target = mass_index(document).get(target_key)
        if target is None:  # Defensive: the referring mass came from this index.
            return None, None, [
                f"{where}: {TAKES_FROM} names mass {target_key!r}, which this calendar has no entry for"
            ]
        candidates, trouble = _form_propers(target, form)
        if trouble:
            return None, None, [f"{where}: {TAKES_FROM} {trouble}"]
        wanted = str(reference.get("proper") or name)
        for found in candidates:
            if str(found.get("name")) != wanted:
                continue
            if reference_of(found) is not None:
                return None, None, [
                    f"{where}: {TAKES_FROM} names a sibling-form proper which itself takes from elsewhere"
                ]
            appointed = _appoint_resolved_proper(found, proper, wanted)
            return appointed, _provenance(reference, proper), []
        return None, None, [
            f"{where}: {TAKES_FROM} names proper {wanted!r} of form {form!r} of mass "
            f"{target_key!r}, which appoints no such proper"
        ]
    if target_key in chain:
        route = " -> ".join((*chain, key, target_key))
        return None, None, [f"{where}: {TAKES_FROM} closes a cycle: {route}"]
    target = mass_index(document).get(target_key)
    if target is None:
        return None, None, [
            f"{where}: {TAKES_FROM} names mass {target_key!r}, which this calendar has no entry for"
        ]
    wanted = str(reference.get("proper") or name)
    entries, problems = resolve_propers(document, target, (*chain, key))
    for label, found, terminal in entries:
        if str(found.get("name")) == wanted and (not form or label == form):
            # The reference names where the text is printed; the wrapper names
            # the slot as it is appointed here. Usually those names agree and
            # the target object can pass through unchanged. A qualified local
            # slot such as ``Collect (Item altera oratio)`` may deliberately
            # name the target's unqualified ``Collect``, however. Keep that
            # local display/slot identity while borrowing every other field
            # from the target. This is shallow on purpose: verses, cycles and
            # translations remain the target's objects rather than restated
            # content free to drift.
            return _appoint_resolved_proper(found, proper, wanted), terminal, problems
    where_form = f" of form {form!r}" if form else ""
    return None, None, [
        *problems,
        f"{where}: {TAKES_FROM} names proper {wanted!r}{where_form} of mass "
        f"{target_key!r}, which appoints no such proper",
    ]


def texts_of(
    proper: dict, lang: str, witness: str | None = None
) -> list[tuple[str, str, str]]:
    """Which of a proper's texts to print, and under whose name.

    Latin is the tracked text; any other language is a carried translation.
    Where a proper holds two translations in the requested language, BOTH are
    returned and each is named. A terminal has no dropdown, and picking one
    silently would hide exactly what the reader asked to see: two witnesses to
    one prayer are worth showing precisely because they differ, and their
    disagreement is what caught 38 wrong orations in this corpus. `witness`
    narrows to one when that is what is wanted.

    Returns `(text, attribution, note)` triples; the attribution is empty
    where there is nothing to choose between. It lives here rather than in
    `mass-propers` because two tools print a proper — that one and
    `mass-today --expanded` — and a second copy of this rule would be a second
    answer to "which text is this Mass said in".
    """
    if lang == "la":
        return [(str(proper.get("text") or ""), "", "")]
    found = [
        translation
        for translation in proper.get("translations") or []
        if isinstance(translation, dict) and translation.get("lang") == lang
        and (witness is None or translation.get("source_id") == witness)
    ]
    if found:
        named = len(found) > 1
        return [
            (
                str(translation.get("text") or ""),
                str(translation.get("source_id") or "this project") if named else "",
                "",
            )
            for translation in found
        ]
    if proper.get("text"):
        scope = f" from {witness}" if witness else ""
        # A proper nobody has reached and one deliberately left without English
        # print the same Latin, and only one of them is work outstanding. The
        # `untranslated` ledger records which is which and the reason; say so
        # rather than let a settled decision read as a gap.
        if proper.get("untranslated") and not witness:
            note = f"no {lang} recorded, deliberately; see the untranslated ledger"
        else:
            note = f"no {lang} translation{scope} recorded; showing Latin"
        return [(str(proper["text"]), "", note)]
    return []


def incipit_only_of(
    proper: dict, lang: str, witness: str | None = None
) -> dict[str, str] | None:
    """Return a cited scripture incipit as apparatus, never selected text.

    A chant's Latin incipit identifies its cited scripture proper and records
    only the opening words.  It is not a translation into the language the
    reader requested, and it is not the full Latin proper.  Keep that
    distinction in shared semantics so a terminal cannot turn an unlabelled
    incipit into an apparent English rendering merely by printing it below an
    English heading.

    This result concerns the proper body selected by :func:`texts_of`.
    Citation-backed scripture is a separate material layer: the Bible may
    resolve the reference while the liturgical identifier remains a Latin
    incipit.  A composed proper without a publishable body does *not* enter
    this path; its typed unavailable or untranslated record owns that absence.
    """
    incipit = str(proper.get("incipit") or "").strip()
    cited_scripture = (
        proper.get("source") == "scripture"
        and any(
            isinstance(verse, dict) and verse.get("ref")
            for verse in proper.get("verses") or []
        )
    )
    if (
        not cited_scripture
        or not incipit
        or any(text for text, _, _ in texts_of(proper, lang, witness))
    ):
        return None

    note = "Latin incipit only"
    if lang != "la":
        scope = f" from {witness}" if witness else ""
        note += f"; no {lang} rendering{scope} recorded"
    material = {
        "text": incipit,
        "language": "la",
        "extent": "incipit",
        "requested_language": lang,
        "note": note,
    }
    if witness:
        material["requested_witness"] = witness
    return material
