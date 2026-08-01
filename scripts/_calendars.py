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

import re
from pathlib import Path

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
REFERENCE_FIELDS = ("mass", "form", "proper", "citation", "note")
# A proper that takes its text from elsewhere holds no text of its own. Naming
# the slot twice is the restatement this key exists to remove, so the incipit
# comes from the resolved proper and may not be retyped beside the reference.
REFERENCE_EXCLUDES = ("source", "text", "verses", "cycles", "incipit", "translations")

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
#   `stands_before` HISTORICAL. The id, in an acts inventory, of the act this
#                   recension stands before. Nothing mechanical reads it. It is
#                   the claim about descent, and it is kept in the vocabulary of
#                   acts because guidance/the-shape.md section 7 fixes the
#                   station as the act and not the book.
#
# So a file may say "I stand before Maxima Redemptionis" and "my untouched
# entries were read from a 1962 printing" at once, and both are true. That is
# guidance/recensions.md Rule 2a -- attestation is separated from residence --
# and it is what lets a recension be declared before anything is transcribed.
RECENSION_BASE = "text_from"
RECENSION_ACT = "stands_before"

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
    """
    import yaml

    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=loader)


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


def load_document(root: Path, calendar: str, effective: bool = True) -> dict:
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
    document = _read(root / calendar / MASS_INDEX)
    base_name = document.get(RECENSION_BASE)
    if not effective or not isinstance(base_name, str) or not base_name:
        return document
    base = load_document(root, base_name, effective=True)
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
) -> dict:
    """Mark a mass with how the recension reached it, so a page can say so.

    guidance/recensions.md Rule 2a: a text attested by only one printing says so.
    An entry carried through from the base with no departure is exactly that
    case, and it is the overwhelming majority, so the stamp goes on every entry
    rather than only on the interesting ones. A renderer that finds no stamp is
    reading a calendar that is nobody's recension.
    """
    out = dict(mass)
    out["recension"] = {
        "calendar": calendar,
        "kind": kind,
        "stated": stated,
        "text_from": "" if stated else calendar,
        "basis": basis,
        "also": [
            {"kind": str(row.get(DEPARTURE) or ""), "basis": str(row.get(DEPARTURE_BASIS) or "")}
            for row in also
        ],
    }
    return out


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
                kept.append(_stamp(mass, base_name, "", "", stated=False))
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
                kept.append(_stamp(carried, base_name, kind, basis, stated=False, also=also))
                continue
            if kind == "unrecorded":
                # Known to differ, correspondence not established. The base entry
                # is carried so the day still resolves, and the stamp is what
                # stops the page claiming the base's text was checked.
                kept.append(_stamp(mass, base_name, kind, basis, stated=False, also=also))
                continue
            # replaced, reslotted: the recension's own entry wins outright.
            kept.append(_stamp(departure, calendar, kind, basis, stated=True, also=also))
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
    if document.get(RECENSION_ACT) in (None, ""):
        problems.append(
            f"{path}: declares {RECENSION_BASE} without {RECENSION_ACT}. A recension "
            "must say which act it stands before, because `text_from` records where "
            "text was transcribed and is not a claim about which book came first."
        )
    base = load_document(root, base_name, effective=True)
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


def reference_of(node: object) -> dict | None:
    """The `takes_from` mapping a mass or proper carries, if it carries one."""
    if not isinstance(node, dict):
        return None
    found = node.get(TAKES_FROM)
    return found if isinstance(found, dict) else None


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
        base, problems = _resolve_reference(document, mass, reference, chain)
        overrides = [p for p in (mass.get("propers") or []) if isinstance(p, dict)]
        base = _apply_overrides(base, overrides)
    resolved: list[tuple[str, dict, dict | None]] = []
    for label, proper, provenance in base:
        inner = reference_of(proper)
        if inner is None:
            resolved.append((label, proper, provenance))
            continue
        taken, trouble = _resolve_proper(document, key, proper, inner, chain)
        problems.extend(trouble)
        if taken is not None:
            resolved.append((label, taken, _provenance(inner, proper)))
    return resolved, problems


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
) -> list[tuple[str, dict, dict | None]]:
    by_name = {str(p.get("name")): p for p in overrides}
    used: set[str] = set()
    out: list[tuple[str, dict, dict | None]] = []
    for label, proper, provenance in base:
        name = str(proper.get("name"))
        if name in by_name:
            used.add(name)
            out.append((label, by_name[name], None))
        else:
            out.append((label, proper, provenance))
    for proper in overrides:
        if str(proper.get("name")) not in used:
            out.append(("", proper, None))
    return out


def _resolve_reference(
    document: dict,
    mass: dict,
    reference: dict,
    chain: tuple[str, ...],
) -> tuple[list[tuple[str, dict, dict | None]], list[str]]:
    key = str(mass.get("key") or "")
    where = f"mass {key}"
    target_key = reference.get("mass")
    if not isinstance(target_key, str) or not target_key:
        return [], [f"{where}: {TAKES_FROM} needs the key of the mass it takes from"]
    if target_key == key:
        return [], [f"{where}: {TAKES_FROM} points at itself"]
    if target_key in chain:
        route = " -> ".join((*chain, key, target_key))
        return [], [f"{where}: {TAKES_FROM} closes a cycle: {route}"]
    target = mass_index(document).get(target_key)
    if target is None:
        return [], [f"{where}: {TAKES_FROM} names mass {target_key!r}, which this calendar has no entry for"]
    form = str(reference.get("form") or "")
    if form or isinstance(target.get("forms"), list):
        chosen, trouble = _form_propers(target, form)
        if trouble:
            return [], [f"{where}: {TAKES_FROM} {trouble}"]
        provenance = {"mass": target_key, "form": form, "proper": "", "citation": str(reference.get("citation") or "")}
        return [("", p, dict(provenance, proper=str(p.get("name") or ""))) for p in chosen], []
    inherited, problems = resolve_propers(document, target, (*chain, key))
    citation = str(reference.get("citation") or "")
    out = [
        (
            label,
            proper,
            {
                "mass": target_key,
                "form": label,
                "proper": str(proper.get("name") or ""),
                "citation": citation,
            },
        )
        for label, proper, _ in inherited
    ]
    return out, problems


def _resolve_proper(
    document: dict,
    key: str,
    proper: dict,
    reference: dict,
    chain: tuple[str, ...],
) -> tuple[dict | None, list[str]]:
    name = str(proper.get("name") or "")
    where = f"mass {key} proper {name!r}"
    target_key = reference.get("mass")
    if not isinstance(target_key, str) or not target_key:
        return None, [f"{where}: {TAKES_FROM} needs the key of the mass it takes from"]
    if target_key in (*chain, key):
        route = " -> ".join((*chain, key, target_key))
        return None, [f"{where}: {TAKES_FROM} closes a cycle: {route}"]
    target = mass_index(document).get(target_key)
    if target is None:
        return None, [f"{where}: {TAKES_FROM} names mass {target_key!r}, which this calendar has no entry for"]
    wanted = str(reference.get("proper") or name)
    form = str(reference.get("form") or "")
    entries, problems = resolve_propers(document, target, (*chain, key))
    for label, found, _ in entries:
        if str(found.get("name")) == wanted and (not form or label == form):
            return found, problems
    where_form = f" of form {form!r}" if form else ""
    return None, [
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
        return [
            (str(proper["text"]), "", f"no {lang} translation{scope} recorded; showing Latin")
        ]
    return []
