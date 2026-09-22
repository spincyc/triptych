#!/usr/bin/env python3
"""Who an author is, as the Church has judged him: one row per person, with its basis.

THE GAP THIS CLOSES. The proper-study rule asks for "at least two distinct
Fathers or saints" per reading, and nothing recorded who is one. The component
checker counts any two author strings; the harvest's `role` is a model's lead
data and tags Rupert of Deutz `saintly` on some rows and `ecclesiastical-writer`
on others. Standing is a fact about a person, established by an act of the
Church or by the patrological convention that defines a Father, and it has one
home: `src/sources/inventories/author-standing-v1.toml`. Locus rows, harvest
tags and study records point here; none of them restates it.

WHAT IS CHECKED. The file's own shape: closed fields, a standing from the closed
set, a basis that cites its sources, persons and names unique, namespaces that
exist in the library, censures that say who censured what and when. Coverage --
whether every liturgical commentary's author and every published lane author
has a row -- is REPORTED, never failed: a registration or a proper study adding
a new author must not turn `make check-sources` red for want of a row the
maintainer has not yet been asked to judge.

What the standing values MEAN for a study is not decided here. That rule belongs
to the proper-study guidance and the opt-in component contract, which read this
registry; this module only keeps the registry true.
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-author-standing/v1"
RECORD_TYPE = "author-standing"
REPORT_SCHEMA = "triptych-author-standing-report/v1"
REGISTRY_RELATIVE = Path("src/sources/inventories/author-standing-v1.toml")
WORKS_RELATIVE = Path("src/sources/works")

# The closed set, in the order the registry file explains them. A person carries
# the first that is true of him: Augustine is a Father before he is a Doctor.
STANDINGS = (
    "father",
    "doctor",
    "saint",
    "blessed",
    "venerable",
    "servant-of-god",
    "ecclesiastical-writer",
    "historian",
    "non-catholic",
)

TOP_FIELDS = {"schema", "record_type", "audited_on", "persons"}
PERSON_FIELDS = {
    "id",
    "namespaces",
    "name",
    "names",
    "died",
    "standing",
    "standing_basis",
    "basis_sources",
    "censures",
    "confession",
    "notes",
}
CENSURE_FIELDS = {"body", "year", "point", "source"}
REQUIRED = ("id", "name", "names", "died", "standing", "standing_basis", "basis_sources", "confession")

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RECORD_ID = re.compile(r"^(?:work|edition|artifact|passage|segment)\.[a-z0-9.-]+$")
URL = re.compile(r"^https://[^\s]+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class StandingError(RuntimeError):
    """The registry cannot be read at all."""


def fold(text: Any) -> str:
    """How a name is compared: case and spacing never make two people one or one two."""
    return " ".join(str(text or "").split()).casefold()


def load(root: Path = ROOT) -> dict[str, Any]:
    path = Path(root) / REGISTRY_RELATIVE
    if not path.is_file():
        raise StandingError(f"{REGISTRY_RELATIVE.as_posix()}: not found")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise StandingError(f"{REGISTRY_RELATIVE.as_posix()}: {error}") from error
    if data.get("schema") != SCHEMA:
        raise StandingError(
            f"{REGISTRY_RELATIVE.as_posix()}: declares schema {data.get('schema')!r}, expected {SCHEMA!r}"
        )
    return data


def persons(data: dict[str, Any]) -> list[dict[str, Any]]:
    value = data.get("persons") or []
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def namespaces_of(person: dict[str, Any]) -> list[str]:
    value = person.get("namespaces")
    return [str(item) for item in value] if isinstance(value, list) else []


def _record_exists(root: Path, record_id: str) -> bool:
    """Whether a cited `work.`/`edition.`/`artifact.`... id is a library record."""
    kind, _, rest = record_id.partition(".")
    parts = rest.split(".")
    base = Path(root) / WORKS_RELATIVE
    if len(parts) < 2:
        return False
    work = base / parts[0] / parts[1]
    if kind == "work":
        return len(parts) == 2 and (work / "work.toml").is_file()
    if len(parts) < 3:
        return False
    edition = work / "editions" / parts[2]
    if kind == "edition":
        return len(parts) == 3 and (edition / "edition.toml").is_file()
    tail = ".".join(parts[3:])
    if kind == "artifact":
        return (edition / "artifacts" / tail / "artifact.toml").is_file()
    if kind == "passage":
        return (edition / "passages" / f"{tail}.toml").is_file()
    if kind == "segment":
        return (edition / "segments" / f"{tail}.toml").is_file()
    return False


def validate(root: Path = ROOT) -> list[str]:
    """Every reason the registry cannot be trusted, sorted and deduplicated."""
    root = Path(root)
    where = REGISTRY_RELATIVE.as_posix()
    try:
        data = load(root)
    except StandingError as error:
        return [str(error)]
    errors: list[str] = []
    unknown = sorted(set(data) - TOP_FIELDS)
    if unknown:
        errors.append(f"{where}: unknown top-level fields: {', '.join(unknown)}")
    if data.get("record_type") != RECORD_TYPE:
        errors.append(f"{where}: record_type must be {RECORD_TYPE!r}")
    if not DATE.match(str(data.get("audited_on") or "")):
        errors.append(f"{where}: audited_on must be an ISO date")
    rows = persons(data)
    if not rows:
        errors.append(f"{where}: persons must be a nonempty array of tables")
    seen_ids: dict[str, str] = {}
    seen_names: dict[str, str] = {}
    seen_namespaces: dict[str, str] = {}
    works = Path(root) / WORKS_RELATIVE
    for ordinal, person in enumerate(rows, start=1):
        pid = str(person.get("id") or "")
        label = f"{where}: persons[{ordinal}] {pid}".rstrip()
        unknown = sorted(set(person) - PERSON_FIELDS)
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        for field in REQUIRED:
            value = person.get(field)
            if value is None or (isinstance(value, (str, list)) and not value):
                errors.append(f"{label} states no {field}")
        if pid and not KEBAB.match(pid):
            errors.append(f"{label} id must be lowercase kebab-case, the person's work-id namespace")
        if pid in seen_ids:
            errors.append(f"{label} repeats the person at {seen_ids[pid]}")
        elif pid:
            seen_ids[pid] = label
        standing = person.get("standing")
        if standing is not None and standing not in STANDINGS:
            errors.append(f"{label} standing is {standing!r}; it must be one of {', '.join(STANDINGS)}")
        for field in ("name", "died", "standing_basis", "confession", "notes"):
            if field in person and not isinstance(person[field], str):
                errors.append(f"{label} {field} must be a string")
        names = person.get("names")
        if not isinstance(names, list) or any(not isinstance(n, str) or not n.strip() for n in names):
            errors.append(f"{label} names must be a list of the forms the person is cited by")
            names = []
        if isinstance(person.get("name"), str) and fold(person["name"]) not in {fold(n) for n in names}:
            errors.append(f"{label} names must include its own name {person['name']!r}")
        for name in names:
            key = fold(name)
            if key in seen_names and seen_names[key] != pid:
                errors.append(f"{label} name {name!r} already names {seen_names[key]}; one name, one person")
            seen_names[key] = pid
        spaces = person.get("namespaces", [])
        if not isinstance(spaces, list) or any(not isinstance(s, str) for s in spaces):
            errors.append(f"{label} namespaces must be a list of work-id namespaces")
            spaces = []
        for space in spaces:
            if not (works / space).is_dir():
                errors.append(f"{label} namespace {space!r} is not a directory of {WORKS_RELATIVE.as_posix()}")
            if space in seen_namespaces and seen_namespaces[space] != pid:
                errors.append(f"{label} namespace {space!r} already belongs to {seen_namespaces[space]}")
            seen_namespaces[space] = pid
        sources = person.get("basis_sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{label} basis_sources must cite at least one source")
            sources = []
        for source in sources:
            text = str(source)
            if URL.match(text):
                continue
            if RECORD_ID.match(text):
                if not _record_exists(root, text):
                    errors.append(f"{label} cites {text!r}, which is not a record in the library")
                continue
            errors.append(f"{label} source {text!r} is neither an https URL nor a library record id")
        censures = person.get("censures", [])
        if not isinstance(censures, list):
            errors.append(f"{label} censures must be an array of tables")
            censures = []
        for number, censure in enumerate(censures, start=1):
            clabel = f"{label} censures[{number}]"
            if not isinstance(censure, dict):
                errors.append(f"{clabel} must be a table")
                continue
            unknown = sorted(set(censure) - CENSURE_FIELDS)
            if unknown:
                errors.append(f"{clabel} has unknown fields: {', '.join(unknown)}")
            for field in ("body", "year", "point", "source"):
                if not str(censure.get(field) or "").strip():
                    errors.append(f"{clabel} states no {field}")
            source = str(censure.get("source") or "")
            if source and not (URL.match(source) or (RECORD_ID.match(source) and _record_exists(root, source))):
                errors.append(f"{clabel} source {source!r} is neither an https URL nor a library record id")
    return sorted(set(errors))


class Registry:
    """Lookups over a validated registry: by person id, work namespace, or cited name."""

    def __init__(self, root: Path = ROOT) -> None:
        self.root = Path(root)
        try:
            self.data = load(self.root)
        except StandingError:
            self.data = {}
        self.rows = persons(self.data)
        self.by_id = {str(row.get("id")): row for row in self.rows}
        self.by_namespace: dict[str, dict[str, Any]] = {}
        self.by_name: dict[str, dict[str, Any]] = {}
        for row in self.rows:
            for space in namespaces_of(row):
                self.by_namespace.setdefault(space, row)
            for name in row.get("names") or []:
                self.by_name.setdefault(fold(name), row)

    def for_work(self, work_id: str) -> dict[str, Any] | None:
        """The person whose namespace a `work.<namespace>.<work>` id sits under."""
        parts = str(work_id).split(".")
        return self.by_namespace.get(parts[1]) if len(parts) >= 3 else None

    def for_name(self, name: str) -> dict[str, Any] | None:
        return self.by_name.get(fold(name))


def _liturgical_commentary_namespaces(root: Path) -> dict[str, str]:
    """Namespace -> work id, for every work registered as a liturgical commentary."""
    found: dict[str, str] = {}
    for path in sorted((Path(root) / WORKS_RELATIVE).glob("*/*/work.toml")):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        if data.get("work_type") == "liturgical-commentary" and isinstance(data.get("id"), str):
            found.setdefault(path.parent.parent.name, data["id"])
    return found


def _lane_authors(root: Path) -> dict[str, list[str]]:
    """Every lane author a proper-components manifest names, with the leaves naming him."""
    found: dict[str, list[str]] = {}
    for path in sorted(Path(root).glob("src/*/liturgy/**/proper-components.toml")):
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        leaf = path.parent.relative_to(Path(root) / "src").as_posix()
        for lane in data.get("lanes") or []:
            for author in (lane or {}).get("authors") or []:
                leaves = found.setdefault(str(author), [])
                if leaf not in leaves:
                    leaves.append(leaf)
    return found


def report(root: Path = ROOT) -> dict[str, Any]:
    """The registry, validated, with the two coverage questions answered but not enforced."""
    root = Path(root)
    errors = validate(root)
    registry = Registry(root)
    counts = {standing: 0 for standing in STANDINGS}
    for row in registry.rows:
        if row.get("standing") in counts:
            counts[row["standing"]] += 1
    commentaries = _liturgical_commentary_namespaces(root)
    missing_commentary = sorted(
        work_id for space, work_id in commentaries.items() if space not in registry.by_namespace
    )
    lanes = _lane_authors(root)
    missing_lane = sorted(name for name in lanes if registry.for_name(name) is None)
    return {
        "schema": REPORT_SCHEMA,
        "status": "invalid" if errors else "ok",
        "errors": errors,
        "registry": REGISTRY_RELATIVE.as_posix(),
        "audited_on": registry.data.get("audited_on"),
        "totals": {
            "persons": len(registry.rows),
            "by_standing": {k: v for k, v in counts.items() if v},
            "liturgical_commentaries": len(commentaries),
            "liturgical_commentaries_without_row": len(missing_commentary),
            "lane_authors": len(lanes),
            "lane_authors_without_row": len(missing_lane),
        },
        "uncovered": {
            "liturgical_commentaries": missing_commentary,
            "lane_authors": missing_lane,
        },
        "persons": [
            {
                "id": row.get("id"),
                "name": row.get("name"),
                "died": row.get("died"),
                "standing": row.get("standing"),
                "censures": len(row.get("censures") or []),
            }
            for row in registry.rows
        ],
    }
