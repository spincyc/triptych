"""The one designator of every coherent missal the corpus identifies.

`src/sources/inventories/missal-designators-v1.toml` owns the display name of
each coherent missal: a promulgated typical edition, an officially issued
emended reprint, a use's or rite's own edition issued by its competent
authority, or an approved translation or adaptation. A printing, lay missal,
facsimile, critical edition or partial book is a witness and keeps its
bibliographic identity in the source library instead of receiving one.

Editions the records name without establishing them are kept in the
registry's `leads` table, never given a designator, so that they stay visible.

A designator names what the book IS. Limits, cut-off dates, witnesses and
inherited material belong in `qualification`, never in the designator, and the
lexical check below refuses the relative words that once stood in for a name.
The short form a control may show is derived here, never stored: it is the
designator's final comma-separated segment.

Reader calendars keep their opaque directory keys (`roman-pre-1955` among
them). A registry row's `calendar` joins the key to the book; every consumer
reads the name through `_calendars.index_header`, `_calendars.load_document`
or `calendar_identity`, and a calendar index restating it is refused.
"""

from __future__ import annotations

import re
import tomllib
from datetime import date
from functools import lru_cache
from pathlib import Path

REGISTRY = Path("src/sources/inventories/missal-designators-v1.toml")
SCHEMA = "triptych-missal-designators/v1"
KINDS = frozenset(
    {
        "typical-edition",
        "emended-reprint",
        "use-edition",
        "approved-translation",
        "approved-adaptation",
    }
)
REQUIRED = frozenset({"key", "designator", "kind", "rite", "language", "year", "sources"})
OPTIONAL = frozenset({"act", "recension", "calendar", "qualification", "witnesses"})
# A book whose authority rests on its own printed statement or on a decree
# recorded elsewhere, and not on a row of the act histories, says so.
NO_ACT = "No separate act row is recorded."
# Editions the records name but whose identity or authority is not yet
# established: kept visible, never given a designator.
LEAD_FIELDS = frozenset({"key", "subject", "status", "reason", "sources"})
LEAD_STATUSES = frozenset(
    {
        "reported-unverified",
        "authority-locus-unconfirmed",
        "copy-not-registered",
        "unestablished",
    }
)
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LANGUAGE = re.compile(r"[a-z]{2,3}(?:-[A-Z]{2})?\Z")
EDITION_ID = re.compile(r"edition\.([a-z0-9-]+)\.([a-z0-9-]+)\.([a-z0-9-]+)\Z")
# Words and shapes that describe a book by its relation to something else or
# by the state of this project's evidence, rather than naming it.
RELATIVE = re.compile(
    r"\b(?:pre|post|before|after|prior|until|circa|approx\w*|base|addition\w*|"
    r"with|witness\w*|study|projection|nominal|transition\w*|unresolved|"
    r"partial|reader|view|\w*conciliar|recension)\b"
    r"|\d{4}\s*[-–]\s*\d{4}|\bc\.\s*\d",
    re.IGNORECASE,
)
ACT_SOURCES = (
    Path("src/sources/inventories/missal-acquisition-audit-v1.toml"),
    Path("src/sources/inventories/latin-missal-acts-v1.toml"),
)
CATALOG = Path("src/sources/calendars/recensions.json")


def short_form(designator: str) -> str:
    """The name a one-line control shows: the designator's final segment."""
    return designator.rsplit(", ", 1)[-1]


@lru_cache(maxsize=None)
def _parsed(path: Path, mtime_ns: int, size: int) -> dict:
    del mtime_ns, size  # cache keys: reparsing follows any on-disk change
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load(repository: Path) -> dict | None:
    """The registry of `repository`, or None where it holds none."""
    path = Path(repository) / REGISTRY
    try:
        stat = path.stat()
    except OSError:
        return None
    return _parsed(path, stat.st_mtime_ns, stat.st_size)


def rows(repository: Path) -> list[dict]:
    document = load(repository) or {}
    return [row for row in document.get("missals") or [] if isinstance(row, dict)]


def calendar_identity(repository: Path, calendar: str) -> dict | None:
    """The display identity a reader calendar takes from the registry.

    None where the repository holds no registry (a synthetic fixture) or no
    row names this calendar; the calendar check refuses the latter in the
    production tree.
    """
    for row in rows(repository):
        if row.get("calendar") == calendar and isinstance(row.get("designator"), str):
            return {
                "edition": row["designator"],
                "edition_short": short_form(row["designator"]),
                "edition_qualification": str(row.get("qualification") or ""),
            }
    return None


def _act_ids(repository: Path) -> set[str]:
    found: set[str] = set()
    for relative in ACT_SOURCES:
        path = repository / relative
        try:
            with path.open("rb") as handle:
                document = tomllib.load(handle)
        except (OSError, tomllib.TOMLDecodeError):
            continue
        for act in document.get("acts") or []:
            if isinstance(act, dict) and isinstance(act.get("id"), str):
                found.add(act["id"])
    return found


def _edition_exists(repository: Path, identifier: object) -> bool:
    """Whether a source-library edition record carries this id.

    The id's last segment usually names the edition directory; where it does
    not, the work's edition records are read for the id itself.
    """
    found = EDITION_ID.fullmatch(identifier) if isinstance(identifier, str) else None
    if not found:
        return False
    work = repository / "src/sources/works" / found.group(1) / found.group(2) / "editions"
    if (work / found.group(3) / "edition.toml").is_file():
        return True
    for record in work.glob("*/edition.toml"):
        try:
            with record.open("rb") as handle:
                if tomllib.load(handle).get("id") == identifier:
                    return True
        except (OSError, tomllib.TOMLDecodeError):
            continue
    return False


@lru_cache(maxsize=None)
def _record_ids(path: Path, mtime_ns: int, size: int) -> frozenset[str]:
    """Every record id a TOML or JSON evidence file holds, gathered once."""
    del mtime_ns, size  # cache keys: reparsing follows any on-disk change
    from _recensions import _document, _walk  # late: _recensions imports _calendars

    return frozenset(
        row["id"] for row in _walk(_document(path))
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    )


def _reference(repository: Path, reference: object, where: str) -> str | None:
    """`_recensions`' reference check, with `#id=` lookups served from an index.

    The timeline inventory holds some fifteen hundred records; walking it
    once per reference made the registry check the slowest part of the
    calendar gate.
    """
    from _recensions import _reference_problem

    if isinstance(reference, str) and "#id=" in reference:
        raw, _, wanted = reference.partition("#id=")
        source = repository / raw
        if source.is_file() and not source.is_symlink():
            stat = source.stat()
            if wanted in _record_ids(source, stat.st_mtime_ns, stat.st_size):
                return None
    return _reference_problem(repository, reference, where)


def _catalog_rows(repository: Path) -> dict[str, dict]:
    import json

    try:
        document = json.loads((repository / CATALOG).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out: dict[str, dict] = {}
    for group in ("recensions", "expressions"):
        for row in document.get(group) or []:
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                out[row["id"]] = dict(row, _group=group)
    return out


def problems(repository: Path, *, required: bool = False) -> list[str]:
    """Every way the registry fails to give each coherent missal one name."""
    repository = Path(repository)
    path = repository / REGISTRY
    document = load(repository)
    if document is None:
        return [f"{path}: the missal designator registry is missing"] if required else []
    out: list[str] = []
    top_fields = {"schema", "as_of", "missals", "leads"}
    if not {"schema", "as_of", "missals"} <= set(document) <= top_fields:
        out.append(f"{path}: top level must hold schema, as_of, missals and optional leads")
    if document.get("schema") != SCHEMA:
        out.append(f"{path}: schema must be {SCHEMA!r}, got {document.get('schema')!r}")
    as_of = document.get("as_of")
    try:
        parsed = date.fromisoformat(as_of) if isinstance(as_of, str) else None
    except ValueError:
        parsed = None
    if parsed is None:
        out.append(f"{path}: as_of must be a quoted ISO date")
    missals = document.get("missals")
    if not isinstance(missals, list) or not missals:
        return out + [f"{path}: missals must be a non-empty list"]

    acts = _act_ids(repository)
    catalog = _catalog_rows(repository)
    keys: set[str] = set()
    names: dict[str, str] = {}
    shorts: dict[str, str] = {}
    calendars: dict[str, str] = {}
    recensions: dict[str, str] = {}
    for index, row in enumerate(missals):
        where = f"{path}: missals[{index}]"
        if not isinstance(row, dict):
            out.append(f"{where} must be a table")
            continue
        missing = sorted(REQUIRED - set(row))
        unknown = sorted(set(row) - REQUIRED - OPTIONAL)
        if missing:
            out.append(f"{where} is missing required fields: {', '.join(missing)}")
        if unknown:
            out.append(f"{where} has unknown fields: {', '.join(unknown)}")
        key = row.get("key")
        if not isinstance(key, str) or not KEY.fullmatch(key):
            out.append(f"{where}.key is not kebab-case: {key!r}")
        elif key in keys:
            out.append(f"{where}.key {key!r} is repeated")
        else:
            keys.add(key)
            where = f"{path}: missal {key!r}"
        designator = row.get("designator")
        year = row.get("year")
        if not isinstance(year, int):
            out.append(f"{where}.year must be an integer")
        if not isinstance(designator, str) or ", " not in designator:
            out.append(
                f"{where}.designator must read '<book>, <edition state>', got {designator!r}"
            )
        else:
            if designator != designator.strip() or "  " in designator:
                out.append(f"{where}.designator carries stray whitespace")
            relative = RELATIVE.search(designator)
            if relative:
                out.append(
                    f"{where}.designator {designator!r} describes the book by "
                    f"{relative.group(0)!r} rather than naming it; put limits in "
                    "qualification"
                )
            final = short_form(designator)
            if isinstance(year, int) and not final.startswith(f"{year} "):
                out.append(
                    f"{where}.designator must end with the segment for its own "
                    f"year {year}, got {final!r}"
                )
            if designator in names:
                out.append(f"{where}.designator repeats {names[designator]!r}")
            names[designator] = str(key)
        kind = row.get("kind")
        if kind not in KINDS:
            out.append(f"{where}.kind has unknown value {kind!r}")
        for field in ("rite", "qualification"):
            value = row.get(field)
            if field in row and (not isinstance(value, str) or not value.strip()):
                out.append(f"{where}.{field} must be a non-empty string")
        language = row.get("language")
        if not isinstance(language, str) or not LANGUAGE.fullmatch(language):
            out.append(f"{where}.language is not a language tag: {language!r}")
        act = row.get("act")
        if act is not None and act not in acts:
            out.append(f"{where}.act names no recorded act: {act!r}")
        if act is None and NO_ACT not in str(row.get("qualification") or ""):
            out.append(f"{where}: a missal with no act row must say {NO_ACT!r} in its qualification")
        sources = row.get("sources")
        if not isinstance(sources, list) or not sources:
            out.append(f"{where}.sources must be a non-empty list")
        else:
            for position, reference in enumerate(sources):
                problem = _reference(repository, reference, f"{where}.sources[{position}]")
                if problem:
                    out.append(problem)
        witnesses = row.get("witnesses", [])
        if not isinstance(witnesses, list):
            out.append(f"{where}.witnesses must be a list")
            witnesses = []
        for witness in witnesses:
            if not _edition_exists(repository, witness):
                out.append(f"{where}.witnesses names no source-library edition: {witness!r}")
        recension = row.get("recension")
        if recension is not None:
            target = catalog.get(recension)
            if target is None:
                out.append(f"{where}.recension names no catalog row: {recension!r}")
            elif target.get("kind", "book-state") != "book-state":
                out.append(f"{where}.recension must name a book state, not {recension!r}")
            else:
                if recension in recensions:
                    out.append(f"{where}.recension {recension!r} is already designated by {recensions[recension]!r}")
                recensions[recension] = str(key)
                if target.get("calendar") != row.get("calendar"):
                    out.append(
                        f"{where}.calendar {row.get('calendar')!r} disagrees with catalog "
                        f"row {recension!r} calendar {target.get('calendar')!r}"
                    )
        calendar = row.get("calendar")
        if calendar is not None:
            if not isinstance(calendar, str) or not KEY.fullmatch(calendar):
                out.append(f"{where}.calendar is not kebab-case: {calendar!r}")
            elif calendar in calendars:
                out.append(f"{where}.calendar {calendar!r} is already designated by {calendars[calendar]!r}")
            else:
                calendars[calendar] = str(key)
                if not (repository / "src/sources/calendars" / calendar / "propers.yaml").is_file():
                    out.append(f"{where}.calendar {calendar!r} has no propers.yaml")
            if not isinstance(row.get("qualification"), str):
                out.append(f"{where}: a reader calendar's designator needs its qualification")
            if isinstance(designator, str):
                short = short_form(designator)
                if short in shorts:
                    out.append(f"{where}: short form {short!r} repeats {shorts[short]!r}")
                shorts[short] = str(key)

    leads = document.get("leads", [])
    if not isinstance(leads, list):
        out.append(f"{path}: leads must be a list")
        leads = []
    for index, row in enumerate(leads):
        where = f"{path}: leads[{index}]"
        if not isinstance(row, dict) or set(row) != LEAD_FIELDS:
            out.append(f"{where} must hold exactly {sorted(LEAD_FIELDS)}")
            continue
        key = row["key"]
        if not isinstance(key, str) or not KEY.fullmatch(key) or key in keys:
            out.append(f"{where}.key is not a fresh kebab-case key: {key!r}")
        else:
            keys.add(key)
        if row["status"] not in LEAD_STATUSES:
            out.append(f"{where}.status has unknown value {row['status']!r}")
        for field in ("subject", "reason"):
            if not isinstance(row[field], str) or not row[field].strip():
                out.append(f"{where}.{field} must be a non-empty string")
        if not isinstance(row["sources"], list) or not row["sources"]:
            out.append(f"{where}.sources must be a non-empty list")
        else:
            for position, reference in enumerate(row["sources"]):
                problem = _reference(repository, reference, f"{where}.sources[{position}]")
                if problem:
                    out.append(problem)

    for identifier, target in sorted(catalog.items()):
        if target.get("kind", "book-state") == "book-state" and identifier not in recensions:
            out.append(f"{path}: catalog book state {identifier!r} has no designator")
    held = sorted(
        candidate.parent.name
        for candidate in (repository / "src/sources/calendars").glob("*/propers.yaml")
    )
    for calendar in held:
        if calendar not in calendars:
            out.append(f"{path}: reader calendar {calendar!r} has no designator")
    return out
