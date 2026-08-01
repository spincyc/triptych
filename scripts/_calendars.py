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
