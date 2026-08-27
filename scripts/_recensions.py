"""Validate the Roman recension and expression capability catalog.

The catalog is JSON on purpose.  Calendar discovery owns YAML mass indexes;
keeping this record outside that extension makes an unsupported recension
incapable of becoming a selectable calendar merely because it has a row here.
"""

from __future__ import annotations

import json
import re
import tomllib
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Iterator

import yaml


CATALOG = "recensions.json"
SCHEMA = "triptych-roman-recensions/v1"
CAPABILITIES = ("calendar", "propers", "rubrics", "ordinary")
EXPRESSION_CAPABILITIES = ("propers", "ordinary")
AVAILABILITY = frozenset({"available", "partial", "unavailable"})
PUBLICATION = frozenset({"available", "partial", "unavailable", "unestablished"})
COLLATION = frozenset(
    {"directly-collated", "mixed", "finding-aid", "unestablished"}
)
IDENTITY = frozenset({"identified", "unresolved"})
KINDS = frozenset({"book-state", "interval-gap"})
REQUIREMENT_KINDS = frozenset(
    {
        "identity-resolution",
        "source-acquisition",
        "calendar-collation",
        "proper-collation",
        "rubric-collation",
        "ordinary-collation",
        "language-collation",
        "rights-review",
        "schema-decision",
    }
)
ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
LANGUAGE = re.compile(r"[a-z]{2,3}(?:-[A-Z]{2})?\Z")
CAPABILITY_FIELDS = frozenset(
    {"data_availability", "publication_availability", "collation"}
)
RECENSION_REQUIRED = frozenset(
    {
        "id",
        "kind",
        "label",
        "identity_status",
        "language",
        "evidence_refs",
        "capabilities",
        "language_capabilities",
        "activation_requirements",
    }
)
RECENSION_OPTIONAL = frozenset({"calendar", "year", "period", "coverage_ref"})
EXPRESSION_REQUIRED = frozenset(
    {
        "id",
        "parent",
        "label",
        "identity_status",
        "language",
        "territory",
        "year",
        "evidence_refs",
        "capabilities",
        "activation_requirements",
    }
)
REQUIREMENT_FIELDS = frozenset(
    {"id", "kind", "capabilities", "need", "evidence_refs"}
)
COVERAGE_SCHEMAS = frozenset(
    {
        "triptych-recension-coverage/v1",
        "triptych-roman-1962-finding-aid-coverage/v1",
        "triptych-recension-language-coverage/v1",
        "triptych-proper-latin-provenance/v1",
        # A calendar index is an admissible derivable-coverage source. It is not
        # itself evidence of target collation; the catalog capability says that.
        "triptych-calendar-masses/v1",
    }
)


def load_catalog(root: Path) -> dict:
    """Read the catalog beside the calendar directories."""
    return json.loads((root / CATALOG).read_text(encoding="utf-8"))


def _shape(
    problems: list[str], where: str, value: object, required: frozenset[str],
    optional: frozenset[str] = frozenset(),
) -> dict:
    if not isinstance(value, dict):
        problems.append(f"{where} must be an object")
        return {}
    fields = set(value)
    missing = sorted(required - fields)
    unknown = sorted(fields - required - optional)
    if missing:
        problems.append(f"{where} is missing required fields: {', '.join(missing)}")
    if unknown:
        problems.append(f"{where} has unknown fields: {', '.join(unknown)}")
    return value


def _text(problems: list[str], where: str, value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        problems.append(f"{where} must be a non-empty string")
        return False
    return True


def _walk(value: object) -> Iterator[object]:
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


@lru_cache(maxsize=None)
def _document_at(path: Path, mtime_ns: int, size: int) -> object:
    del mtime_ns, size  # cache keys: reparsing follows any on-disk change
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    if path.suffix == ".toml":
        return tomllib.loads(text)
    if path.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return None


def _document(path: Path) -> object:
    stat = path.stat()
    return _document_at(path, stat.st_mtime_ns, stat.st_size)


def _reference_problem(repository: Path, reference: object, where: str) -> str | None:
    if not _text([], where, reference):
        return f"{where} must be a non-empty repo-relative reference"
    assert isinstance(reference, str)
    raw_path, marker, selector = reference.partition("#")
    path = Path(raw_path)
    if path.is_absolute() or ".." in path.parts:
        return f"{where} must be repo-relative, got {reference!r}"
    source = repository / path
    if not source.is_file():
        return f"{where} names missing source {raw_path!r}"
    if not marker or not selector:
        return None
    try:
        document = _document(source)
    except (
        OSError,
        ValueError,
        json.JSONDecodeError,
        tomllib.TOMLDecodeError,
        yaml.YAMLError,
    ) as error:
        return f"{where} cannot inspect {raw_path!r}: {error}"
    if selector.startswith("id="):
        wanted = selector.removeprefix("id=")
        if not any(isinstance(row, dict) and row.get("id") == wanted for row in _walk(document)):
            return f"{where} names absent record id {wanted!r} in {raw_path}"
        return None
    if selector.startswith("/"):
        current = document
        for token in selector[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict) and token in current:
                current = current[token]
            elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
                current = current[int(token)]
            else:
                return f"{where} names absent JSON pointer #{selector} in {raw_path}"
        return None
    if not isinstance(document, dict) or selector not in document:
        return f"{where} names absent top-level record {selector!r} in {raw_path}"
    return None


def _reference_payload(
    repository: Path, reference: object, where: str
) -> tuple[str | None, object, object]:
    """Resolve a structured reference to both its document and selected record."""
    if problem := _reference_problem(repository, reference, where):
        return problem, None, None
    assert isinstance(reference, str)
    raw_path, marker, selector = reference.partition("#")
    source = repository / raw_path
    try:
        document = _document(source)
    except (OSError, ValueError, json.JSONDecodeError, tomllib.TOMLDecodeError, yaml.YAMLError) as error:
        return f"{where} cannot inspect {raw_path!r}: {error}", None, None
    if document is None:
        return f"{where} must name a structured JSON, TOML, or YAML record", None, None
    if not marker or not selector:
        return None, document, document
    if selector.startswith("id="):
        wanted = selector.removeprefix("id=")
        selected = next(
            (
                row
                for row in _walk(document)
                if isinstance(row, dict) and row.get("id") == wanted
            ),
            None,
        )
        return None, document, selected
    if selector.startswith("/"):
        current = document
        for token in selector[1:].split("/"):
            token = token.replace("~1", "/").replace("~0", "~")
            if isinstance(current, dict):
                current = current[token]
            else:
                current = current[int(token)]
        return None, document, current
    assert isinstance(document, dict)
    return None, document, document[selector]


def _references(
    problems: list[str], repository: Path, where: str, values: object,
    *, required: bool = True,
) -> None:
    if not isinstance(values, list) or (required and not values):
        suffix = "non-empty " if required else ""
        problems.append(f"{where} must be a {suffix}list of repo-relative references")
        return
    if len(values) != len(set(map(str, values))):
        problems.append(f"{where} repeats a reference")
    for index, value in enumerate(values):
        if problem := _reference_problem(repository, value, f"{where}[{index}]"):
            problems.append(problem)


def _capability(problems: list[str], where: str, value: object) -> dict:
    row = _shape(problems, where, value, CAPABILITY_FIELDS)
    if not row:
        return row
    data = row.get("data_availability")
    publication = row.get("publication_availability")
    collation = row.get("collation")
    if data not in AVAILABILITY:
        problems.append(f"{where}.data_availability has unknown value {data!r}")
    if publication not in PUBLICATION:
        problems.append(f"{where}.publication_availability has unknown value {publication!r}")
    if collation not in COLLATION:
        problems.append(f"{where}.collation has unknown value {collation!r}")
    if data == "unavailable" and collation != "unestablished":
        problems.append(f"{where} is unavailable but collation is {collation!r}")
    return row


def _capabilities(
    problems: list[str], where: str, value: object, expected: tuple[str, ...]
) -> dict[str, dict]:
    row = _shape(problems, where, value, frozenset(expected))
    return {
        name: _capability(problems, f"{where}.{name}", row.get(name))
        for name in expected
        if name in row
    }


def _requirements(
    problems: list[str], repository: Path, where: str, value: object,
    capability_names: set[str], unavailable: set[str],
) -> None:
    if not isinstance(value, list):
        problems.append(f"{where} must be a list")
        return
    covered: set[str] = set()
    seen: set[str] = set()
    for index, candidate in enumerate(value):
        row_where = f"{where}[{index}]"
        row = _shape(problems, row_where, candidate, REQUIREMENT_FIELDS)
        if not row:
            continue
        identifier = row.get("id")
        if _text(problems, f"{row_where}.id", identifier) and isinstance(identifier, str):
            if not ID.fullmatch(identifier):
                problems.append(f"{row_where}.id is not kebab-case: {identifier!r}")
            if identifier in seen:
                problems.append(f"{row_where}.id {identifier!r} is repeated")
            seen.add(identifier)
        kind = row.get("kind")
        if kind not in REQUIREMENT_KINDS:
            problems.append(f"{row_where}.kind has unknown value {kind!r}")
        stated = row.get("capabilities")
        if not isinstance(stated, list) or not stated:
            problems.append(f"{row_where}.capabilities must be a non-empty list")
        else:
            unknown = sorted(set(map(str, stated)) - capability_names)
            if unknown:
                problems.append(
                    f"{row_where}.capabilities has unknown values: {', '.join(unknown)}"
                )
            covered.update(str(one) for one in stated)
        _text(problems, f"{row_where}.need", row.get("need"))
        _references(problems, repository, f"{row_where}.evidence_refs", row.get("evidence_refs"))
    missing = sorted(unavailable - covered)
    if missing:
        problems.append(
            f"{where} does not account for unavailable capabilities: {', '.join(missing)}"
        )


def _language_capabilities(
    problems: list[str], where: str, value: object, primary: object
) -> None:
    if not isinstance(value, list) or not value:
        problems.append(f"{where} must be a non-empty list")
        return
    seen: set[str] = set()
    for index, candidate in enumerate(value):
        row_where = f"{where}[{index}]"
        row = _shape(
            problems,
            row_where,
            candidate,
            frozenset({"id"}) | CAPABILITY_FIELDS,
            frozenset({"coverage_ref"}),
        )
        language = row.get("id")
        if not isinstance(language, str) or not LANGUAGE.fullmatch(language):
            problems.append(f"{row_where}.id is not a language tag: {language!r}")
        elif language in seen:
            problems.append(f"{row_where}.id {language!r} is repeated")
        else:
            seen.add(language)
        _capability(
            problems,
            row_where,
            {name: row.get(name) for name in CAPABILITY_FIELDS if name in row},
        )
    if primary not in seen:
        problems.append(f"{where} has no row for primary language {primary!r}")


def _coverage_reference(
    problems: list[str],
    repository: Path,
    where: str,
    row: dict,
    *,
    identifier: object,
    calendar: object = None,
    language: object = None,
    required: bool = False,
) -> None:
    if "coverage_ref" not in row:
        if required:
            problems.append(
                f"{where}.coverage_ref is required when target data is available or partial"
            )
        return
    reference_where = f"{where}.coverage_ref"
    problem, document, target = _reference_payload(
        repository, row.get("coverage_ref"), reference_where
    )
    if problem:
        problems.append(problem)
        return
    if not isinstance(target, dict):
        problems.append(f"{reference_where} must resolve to a coverage mapping")
        return
    schema = target.get("schema")
    if schema not in COVERAGE_SCHEMAS:
        problems.append(
            f"{reference_where} resolves to unsupported coverage schema {schema!r}"
        )
    source = document if isinstance(document, dict) else {}
    target_recension = target.get("recension_id") or source.get("recension_id")
    target_calendar = target.get("calendar") or source.get("calendar")
    target_language = target.get("language") or source.get("language")
    if isinstance(identifier, str) and target_recension not in (None, identifier):
        problems.append(
            f"{reference_where} names recension {target_recension!r}, expected {identifier!r}"
        )
    if isinstance(calendar, str) and target_calendar not in (None, calendar):
        problems.append(
            f"{reference_where} names calendar {target_calendar!r}, expected {calendar!r}"
        )
    if isinstance(language, str):
        if target_language is None:
            problems.append(
                f"{reference_where} does not identify language {language!r}"
            )
        elif target_language != language:
            problems.append(
                f"{reference_where} names language {target_language!r}, "
                f"expected {language!r}"
            )
    has_identity = (
        isinstance(identifier, str) and target_recension == identifier
    ) or (
        isinstance(calendar, str) and target_calendar == calendar
    )
    if not has_identity:
        problems.append(
            f"{reference_where} does not identify recension {identifier!r} or "
            f"calendar {calendar!r}"
        )


def _recension(
    problems: list[str], repository: Path, calendars_root: Path, index: int,
    value: object, ids: set[str], calendars: set[str],
) -> None:
    where = f"{calendars_root / CATALOG}: recensions[{index}]"
    row = _shape(problems, where, value, RECENSION_REQUIRED, RECENSION_OPTIONAL)
    if not row:
        return
    identifier = row.get("id")
    if not isinstance(identifier, str) or not ID.fullmatch(identifier):
        problems.append(f"{where}.id is not kebab-case: {identifier!r}")
    elif identifier in ids:
        problems.append(f"{where}.id {identifier!r} is repeated")
    else:
        ids.add(identifier)
    _text(problems, f"{where}.label", row.get("label"))
    kind = row.get("kind")
    if kind not in KINDS:
        problems.append(f"{where}.kind has unknown value {kind!r}")
    identity = row.get("identity_status")
    if identity not in IDENTITY:
        problems.append(f"{where}.identity_status has unknown value {identity!r}")
    language = row.get("language")
    if not isinstance(language, str) or not LANGUAGE.fullmatch(language):
        problems.append(f"{where}.language is not a language tag: {language!r}")
    if kind == "book-state":
        if identity != "identified":
            problems.append(f"{where}: a book-state must have identified identity")
        if not isinstance(row.get("year"), int):
            problems.append(f"{where}.year must be an integer for a book-state")
        if "period" in row:
            problems.append(f"{where}.period belongs only on an interval-gap")
    if kind == "interval-gap":
        if identity != "unresolved":
            problems.append(f"{where}: an interval-gap must have unresolved identity")
        if "calendar" in row:
            problems.append(f"{where}: an interval-gap must not name a calendar")
        period = _shape(
            problems, f"{where}.period", row.get("period"), frozenset({"from", "through"})
        )
        if period and (
            not isinstance(period.get("from"), int)
            or not isinstance(period.get("through"), int)
            or period["from"] > period["through"]
        ):
            problems.append(f"{where}.period must be an ordered integer range")
        if "year" in row:
            problems.append(f"{where}.year belongs only on a book-state")
    calendar = row.get("calendar")
    if calendar is not None:
        if not isinstance(calendar, str) or not ID.fullmatch(calendar):
            problems.append(f"{where}.calendar is not kebab-case: {calendar!r}")
        elif calendar in calendars:
            problems.append(f"{where}.calendar {calendar!r} is repeated")
        else:
            calendars.add(calendar)
        source = calendars_root / str(calendar) / "propers.yaml"
        if not source.is_file():
            problems.append(f"{where}.calendar {calendar!r} has no propers.yaml")
        else:
            try:
                document = _document(source)
            except (OSError, ValueError, yaml.YAMLError) as error:
                problems.append(f"{source}: unreadable while checking the catalog: {error}")
            else:
                declared = document.get("calendar") if isinstance(document, dict) else None
                if declared != calendar:
                    problems.append(
                        f"{where}.calendar is {calendar!r}, but {source} declares {declared!r}"
                    )
    _references(problems, repository, f"{where}.evidence_refs", row.get("evidence_refs"))
    capabilities = _capabilities(
        problems, f"{where}.capabilities", row.get("capabilities"), CAPABILITIES
    )
    unavailable = {
        name for name, capability in capabilities.items()
        if capability.get("data_availability") == "unavailable"
    }
    _language_capabilities(
        problems, f"{where}.language_capabilities", row.get("language_capabilities"), language
    )
    # Coverage references are validated here, with the actual repository root.
    for lang_index, lang in enumerate(row.get("language_capabilities") or []):
        if isinstance(lang, dict):
            _coverage_reference(
                problems,
                repository,
                f"{where}.language_capabilities[{lang_index}]",
                lang,
                identifier=identifier,
                calendar=calendar,
                language=lang.get("id"),
                required=lang.get("data_availability") in {"available", "partial"},
            )
    _coverage_reference(
        problems,
        repository,
        where,
        row,
        identifier=identifier,
        calendar=calendar,
        required=any(
            capability.get("data_availability") in {"available", "partial"}
            for capability in capabilities.values()
        ),
    )
    _requirements(
        problems,
        repository,
        f"{where}.activation_requirements",
        row.get("activation_requirements"),
        set(CAPABILITIES),
        unavailable,
    )


def _expression(
    problems: list[str], repository: Path, calendars_root: Path, index: int,
    value: object, recension_rows: dict[str, dict], expression_ids: set[str],
) -> None:
    where = f"{calendars_root / CATALOG}: expressions[{index}]"
    row = _shape(problems, where, value, EXPRESSION_REQUIRED, frozenset({"coverage_ref"}))
    if not row:
        return
    identifier = row.get("id")
    if not isinstance(identifier, str) or not ID.fullmatch(identifier):
        problems.append(f"{where}.id is not kebab-case: {identifier!r}")
    elif identifier in expression_ids or identifier in recension_rows:
        problems.append(f"{where}.id {identifier!r} is repeated")
    else:
        expression_ids.add(identifier)
    parent = row.get("parent")
    parent_row = recension_rows.get(parent) if isinstance(parent, str) else None
    if parent_row is None:
        problems.append(f"{where}.parent names unknown recension {parent!r}")
    elif (
        parent_row.get("kind") != "book-state"
        or parent_row.get("identity_status") != "identified"
    ):
        problems.append(f"{where}.parent must name an identified book-state, got {parent!r}")
    _text(problems, f"{where}.label", row.get("label"))
    if row.get("identity_status") != "identified":
        problems.append(f"{where}.identity_status must be 'identified'")
    language = row.get("language")
    if not isinstance(language, str) or not LANGUAGE.fullmatch(language):
        problems.append(f"{where}.language is not a language tag: {language!r}")
    territory = row.get("territory")
    if not isinstance(territory, str) or not re.fullmatch(r"[A-Z]{2}", territory):
        problems.append(f"{where}.territory must be an ISO alpha-2 code: {territory!r}")
    expression_year = row.get("year")
    if not isinstance(expression_year, int):
        problems.append(f"{where}.year must be an integer")
    elif parent_row is not None and isinstance(parent_row.get("year"), int):
        if expression_year < parent_row["year"]:
            problems.append(
                f"{where}.year {expression_year} predates parent {parent!r} year "
                f"{parent_row['year']}"
            )
    _references(problems, repository, f"{where}.evidence_refs", row.get("evidence_refs"))
    capabilities = _capabilities(
        problems,
        f"{where}.capabilities",
        row.get("capabilities"),
        EXPRESSION_CAPABILITIES,
    )
    unavailable = {
        name for name, capability in capabilities.items()
        if capability.get("data_availability") == "unavailable"
    }
    _coverage_reference(
        problems,
        repository,
        where,
        row,
        identifier=identifier,
        required=any(
            capability.get("data_availability") in {"available", "partial"}
            for capability in capabilities.values()
        ),
    )
    _requirements(
        problems,
        repository,
        f"{where}.activation_requirements",
        row.get("activation_requirements"),
        set(EXPRESSION_CAPABILITIES),
        unavailable,
    )


def _chronology_problems(path: Path, recensions: list[object]) -> list[str]:
    """Defend the order and non-overlap of the catalog's existing dated rows."""
    problems: list[str] = []
    spans: list[tuple[int, int, int, str]] = []
    for index, candidate in enumerate(recensions):
        if not isinstance(candidate, dict):
            continue
        identifier = str(candidate.get("id") or f"recensions[{index}]")
        if candidate.get("kind") == "book-state" and isinstance(candidate.get("year"), int):
            start = through = candidate["year"]
        elif candidate.get("kind") == "interval-gap" and isinstance(candidate.get("period"), dict):
            start = candidate["period"].get("from")
            through = candidate["period"].get("through")
            if not isinstance(start, int) or not isinstance(through, int) or start > through:
                continue
        else:
            continue
        spans.append((start, through, index, identifier))
    for previous, current in zip(spans, spans[1:]):
        if current[0] < previous[0]:
            problems.append(
                f"{path}: recensions are not chronological: {current[3]!r} is "
                f"listed after {previous[3]!r} despite starting at {current[0]} "
                f"before {previous[0]}"
            )
    ordered = sorted(spans)
    for previous, current in zip(ordered, ordered[1:]):
        if current[0] <= previous[1]:
            problems.append(
                f"{path}: dated recension rows overlap: {previous[3]!r} "
                f"({previous[0]}-{previous[1]}) and {current[3]!r} "
                f"({current[0]}-{current[1]})"
            )
    return problems


def _calendar_lineage_problems(
    path: Path, calendars_root: Path, recensions: list[object]
) -> list[str]:
    """Join every mechanical ``text_from`` edge to catalogued calendar identity."""
    mapped = {
        row["calendar"]: row["id"]
        for row in recensions
        if isinstance(row, dict)
        and isinstance(row.get("calendar"), str)
        and isinstance(row.get("id"), str)
    }
    graph: dict[str, str] = {}
    problems: list[str] = []
    for calendar, recension_id in sorted(mapped.items()):
        source = calendars_root / calendar / "propers.yaml"
        if not source.is_file():
            continue
        try:
            document = _document(source)
        except (OSError, ValueError, yaml.YAMLError):
            continue
        if not isinstance(document, dict) or "text_from" not in document:
            continue
        base = document.get("text_from")
        where = f"{path}: recension {recension_id!r} calendar {calendar!r}"
        if not isinstance(base, str) or not ID.fullmatch(base):
            problems.append(f"{where} has invalid text_from {base!r}")
            continue
        if base not in mapped:
            problems.append(
                f"{where} text_from names uncatalogued calendar {base!r}"
            )
            continue
        graph[calendar] = base

    reported: set[tuple[str, ...]] = set()
    for start in sorted(graph):
        route: list[str] = []
        positions: dict[str, int] = {}
        current = start
        while current in graph:
            if current in positions:
                cycle = tuple(route[positions[current]:] + [current])
                canonical = min(
                    tuple(cycle[index:-1] + cycle[:index] + (cycle[index],))
                    for index in range(len(cycle) - 1)
                )
                if canonical not in reported:
                    reported.add(canonical)
                    problems.append(
                        f"{path}: catalogued calendar text_from cycle: "
                        + " -> ".join(cycle)
                    )
                break
            positions[current] = len(route)
            route.append(current)
            current = graph[current]
    return problems


def catalog_problems(
    calendars_root: Path,
    *,
    repository: Path | None = None,
    required: bool = False,
) -> list[str]:
    """Return every structural, source-reference, and discovery mismatch."""
    path = calendars_root / CATALOG
    if not path.is_file():
        return [f"{path}: required Roman recension catalog is missing"] if required else []
    problems: list[str] = []
    try:
        document = load_catalog(calendars_root)
    except (OSError, json.JSONDecodeError) as error:
        return [f"{path}: unreadable: {error}"]
    root = repository or path.resolve().parents[3]
    top = _shape(
        problems,
        str(path),
        document,
        frozenset({"schema", "as_of", "rite", "vocabulary", "recensions", "expressions"}),
    )
    if not top:
        return problems
    if top.get("schema") != SCHEMA:
        problems.append(f"{path}: schema must be {SCHEMA!r}, got {top.get('schema')!r}")
    if top.get("rite") != "roman":
        problems.append(f"{path}: rite must be 'roman', got {top.get('rite')!r}")
    as_of = top.get("as_of")
    try:
        parsed_as_of = date.fromisoformat(as_of) if isinstance(as_of, str) else None
    except ValueError:
        parsed_as_of = None
    if parsed_as_of is None or str(parsed_as_of) != as_of:
        problems.append(f"{path}: as_of must be a quoted ISO date")
    vocabulary = _shape(
        problems,
        f"{path}: vocabulary",
        top.get("vocabulary"),
        frozenset({"data_availability", "publication_availability", "collation"}),
    )
    expected_vocabularies = {
        "data_availability": AVAILABILITY,
        "publication_availability": PUBLICATION,
        "collation": COLLATION,
    }
    for name, expected in expected_vocabularies.items():
        values = vocabulary.get(name)
        if not isinstance(values, list) or set(values) != set(expected) or len(values) != len(expected):
            problems.append(f"{path}: vocabulary.{name} must enumerate the validator's closed values")
    recensions = top.get("recensions")
    if not isinstance(recensions, list) or not recensions:
        problems.append(f"{path}: recensions must be a non-empty list")
        recensions = []
    ids: set[str] = set()
    calendars: set[str] = set()
    for index, row in enumerate(recensions):
        _recension(problems, root, calendars_root, index, row, ids, calendars)
    problems.extend(_chronology_problems(path, recensions))
    problems.extend(_calendar_lineage_problems(path, calendars_root, recensions))
    recension_rows = {
        row["id"]: row
        for row in recensions
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    expressions = top.get("expressions")
    if not isinstance(expressions, list):
        problems.append(f"{path}: expressions must be a list")
        expressions = []
    expression_ids: set[str] = set()
    for index, row in enumerate(expressions):
        _expression(
            problems,
            root,
            calendars_root,
            index,
            row,
            recension_rows,
            expression_ids,
        )
    held: set[str] = set()
    for source in calendars_root.glob("*/propers.yaml"):
        try:
            index = _document(source)
        except (OSError, ValueError, yaml.YAMLError):
            continue  # the calendar checker owns the primary parse diagnostic
        if isinstance(index, dict) and isinstance(index.get("calendar"), str):
            held.add(index["calendar"])
    missing = sorted(held - calendars)
    extra = sorted(calendars - held)
    if missing:
        problems.append(f"{path}: unregistered calendar indexes: {', '.join(missing)}")
    if extra:
        problems.append(f"{path}: registered calendars without indexes: {', '.join(extra)}")
    return problems
