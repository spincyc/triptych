#!/usr/bin/env python3
"""Which library records hold other works inside them, and what is held of a lead.

THE HOLE THIS CLOSES. `commentary-work-index discover` names the works that
comment on a passage, and a researcher then asks the source library whether
each is held. Many are held only INSIDE another record: a Migne volume, a
collected-works tome, an NPNF anthology, a whole-volume optical layer filed
under whichever constituent a lane happened to be reading. Nothing linked the
container to what it contains, so a sweep that checked each lead by its own work
record reported held witnesses as absent -- three review rounds running in one
proper study. The library said so itself, in prose nobody could query: the
Venice tomus of Aquinas "holding Aquinas's lectures on Matthew and on John",
whose two commentaries "are not yet registered as such".

WHY A SEPARATE INVENTORY AND NOT A FIELD. `source-library`'s
`source_fingerprint()` hashes a record's whole data and its ancestors', and
reviewed bindings pin those fingerprints. A field added to a work or artifact
record would move every fingerprint under it and hand a review obligation to
every pinned binding -- `guidance/catena.md` §7 records the policy and
`fragment-loci.yaml` already obeys it. So the edge lives in
`src/sources/inventories/source-containment-v1.toml`, beside the records, and
the records are not touched.

WHAT IS STORED AND WHAT IS DERIVED. Stored: which records are containers, what
each contains, how far each constituent reaches inside it, and the evidence for
it. Derived, every run: which records are container-shaped (the inventory's
declared shapes, plus every record another work's segment or catena fragment
already points into), whether each has an entry, whether each entry still
describes the bytes it was reviewed against, and every join between the
commentary index's identities and the library's. `validate` refuses the
inventory the moment any of those disagree, so a container cannot be added to
the library silently.

A HOLDING IS A CLAIM OF THE SAME SHAPE AS AN ABSENCE. "No registered holding"
is bounded by the joins this module makes and says so wherever it is printed:
a work held under a name none of them reaches is still reported absent, and the
remedy is an `identities` row, never a looser match.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
import tomllib
from pathlib import Path
from typing import Any, Iterable, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _calendars  # noqa: E402
import _canon  # noqa: E402
import _catena  # noqa: E402
from _tooling import cached_json, code_fingerprint, tree_fingerprint  # noqa: E402

ROOT = _catena.ROOT
SCHEMA = "triptych-source-containment/v1"
RECORD_TYPE = "source-containment"
REPORT_SCHEMA = "triptych-source-containment-report/v1"
INVENTORY_RELATIVE = Path("src/sources/inventories/source-containment-v1.toml")
WORKS_RELATIVE = Path("src/sources/works")
CATALOG_CACHE = Path("build/sources/containment-catalog")
# A sandbox library is a handful of files; caching it would leave an entry that
# nothing reads again. The real library is thousands.
CATALOG_CACHE_FLOOR = 500

RESOLVED = "resolved"
PARTIAL = "partial"
UNRESOLVED = "unresolved"
STATUSES = (RESOLVED, PARTIAL, UNRESOLVED)

TOP_FIELDS = {
    "schema",
    "record_type",
    "audited_on",
    "numbering",
    "shapes",
    "identities",
    "not_containers",
    "containers",
}
SHAPE_FIELDS = {"work_types", "description_patterns", "artifact_patterns"}
CONTAINER_FIELDS = {"id", "manifest_sha256", "status", "basis", "unresolved", "constituents"}
CONSTITUENT_FIELDS = {
    "author",
    "title",
    "work_id",
    "scripture",
    "whole",
    "locator",
    "extent_unresolved",
    "basis",
}
NOT_CONTAINER_FIELDS = {"id", "manifest_sha256", "reason"}
IDENTITY_FIELDS = {"author", "title", "work_id", "reason"}

# How a lead reaches a library record. Ordered strongest first: an id a record
# carries beats a reviewed row, which beats a name that happens to agree.
JOINS = ("index-work-id", "identity", "constituent", "fragment-edge", "title")

# What a container says about the passage asked for.
INSIDE = "inside"
PARTIALLY = "partial"
OUTSIDE = "outside"
WHOLE_WORK = "whole-work"
NOT_STATED = "not-stated"

HELD = "held"
HELD_IN_CONTAINER = "held-in-container"
CATALOGED = "cataloged-only"
NONE = "none"

NONE_NOTE = (
    "no library record, fragment edge, identity row or containment entry joins "
    "this work; that is an absence from those joins, not proof that no copy exists"
)


class ContainmentError(RuntimeError):
    """The inventory cannot be read at all."""


# ---------------------------------------------------------------------------
# The library, read once
# ---------------------------------------------------------------------------


def _toml(path: Path) -> dict[str, Any] | None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _build_catalog(root: Path) -> dict[str, Any]:
    """The fields this module reads from every work, edition, artifact and segment."""
    base = root / WORKS_RELATIVE
    works: dict[str, Any] = {}
    editions: dict[str, Any] = {}
    artifacts: dict[str, Any] = {}
    segments: dict[str, Any] = {}
    for path in sorted(base.glob("*/*/work.toml")):
        data = _toml(path)
        if not data or not isinstance(data.get("id"), str):
            continue
        works[data["id"]] = {
            "title": str(data.get("title") or ""),
            "responsible": str(data.get("responsible") or ""),
            "work_type": str(data.get("work_type") or ""),
            "alternate_titles": [str(t) for t in data.get("alternate_titles") or []],
            "description": str(data.get("description") or ""),
            "path": _relative(root, path),
        }
    for path in sorted(base.glob("*/*/editions/*/edition.toml")):
        data = _toml(path)
        if not data or not isinstance(data.get("id"), str):
            continue
        editions[data["id"]] = {
            "work_id": str(data.get("work_id") or ""),
            "language": str(data.get("language") or ""),
            "title": str(data.get("title") or ""),
            "path": _relative(root, path),
            # Counted, not parsed: a passage's presence is what a holding
            # report needs, and there are five thousand of them.
            "passages": len(list(path.parent.glob("passages/*.toml"))),
        }
    for path in sorted(base.glob("*/*/editions/*/artifacts/*/artifact.toml")):
        data = _toml(path)
        if not data or not isinstance(data.get("id"), str):
            continue
        artifacts[data["id"]] = {
            "edition_id": str(data.get("edition_id") or ""),
            "storage": str(data.get("storage") or ""),
            "artifact_type": str(data.get("artifact_type") or ""),
            "media_type": str(data.get("media_type") or ""),
            "notes": str(data.get("notes") or ""),
            "provenance": str(data.get("provenance") or ""),
            "path": _relative(root, path),
        }
    for path in sorted(base.glob("*/*/editions/*/segments/*.toml")):
        data = _toml(path)
        if not data or not isinstance(data.get("id"), str):
            continue
        segments[data["id"]] = {
            "edition_id": str(data.get("edition_id") or ""),
            "artifact_id": str(data.get("artifact_id") or ""),
            "path": _relative(root, path),
        }
    return {
        "works": works,
        "editions": editions,
        "artifacts": artifacts,
        "segments": segments,
    }


_CATALOGS: dict[Path, dict[str, Any]] = {}


def catalog(root: Path = ROOT) -> dict[str, Any]:
    """The library's records, keyed by the tree they were read from."""
    root = Path(root)
    if root in _CATALOGS:
        return _CATALOGS[root]
    base = root / WORKS_RELATIVE
    value: dict[str, Any]
    if os.environ.get("TRIPTYCH_CONTAINMENT_CACHE") == "0" or not base.is_dir():
        value = _build_catalog(root)
    else:
        fingerprint, counted = tree_fingerprint([base])
        if counted < CATALOG_CACHE_FLOOR:
            value = _build_catalog(root)
        else:
            value = cached_json(
                root / CATALOG_CACHE,
                f"{fingerprint}-{code_fingerprint(__file__)}",
                lambda: _build_catalog(root),
            )
    _CATALOGS[root] = value
    return value


def owner_of_artifact(library: dict[str, Any], artifact_id: str) -> str:
    artifact = library["artifacts"].get(artifact_id) or {}
    edition = library["editions"].get(artifact.get("edition_id", "")) or {}
    return str(edition.get("work_id") or "")


def artifacts_of_work(library: dict[str, Any], work_id: str) -> list[str]:
    editions = {
        edition_id
        for edition_id, edition in library["editions"].items()
        if edition["work_id"] == work_id
    }
    return sorted(
        artifact_id
        for artifact_id, artifact in library["artifacts"].items()
        if artifact["edition_id"] in editions
    )


def storage_counts(library: dict[str, Any], artifact_ids: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for artifact_id in artifact_ids:
        storage = library["artifacts"].get(artifact_id, {}).get("storage") or "unknown"
        counts[storage] = counts.get(storage, 0) + 1
    return dict(sorted(counts.items()))


# ---------------------------------------------------------------------------
# The inventory
# ---------------------------------------------------------------------------


def load_inventory(root: Path = ROOT) -> dict[str, Any]:
    path = Path(root) / INVENTORY_RELATIVE
    if not path.is_file():
        raise ContainmentError(f"{INVENTORY_RELATIVE.as_posix()}: not found")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        raise ContainmentError(f"{INVENTORY_RELATIVE.as_posix()}: {error}") from error
    if data.get("schema") != SCHEMA:
        raise ContainmentError(
            f"{INVENTORY_RELATIVE.as_posix()}: declares schema {data.get('schema')!r}, "
            f"expected {SCHEMA!r}"
        )
    return data


def manifest_sha256(root: Path, library: dict[str, Any], record_id: str) -> str | None:
    """The bytes a container entry was reviewed against: its own manifest."""
    record = library["works"].get(record_id) or library["artifacts"].get(record_id)
    if record is None:
        return None
    try:
        return hashlib.sha256((Path(root) / record["path"]).read_bytes()).hexdigest()
    except OSError:
        return None


def _entries(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key) or []
    return [entry for entry in value if isinstance(entry, dict)] if isinstance(value, list) else []


# ---------------------------------------------------------------------------
# Scripture extents
# ---------------------------------------------------------------------------


class Point(NamedTuple):
    chapter: int
    verse: int


class Span(NamedTuple):
    book: str
    begin: Point
    end: Point


_RANGE = re.compile(
    r"^(?P<c1>[1-9][0-9]*)(?::(?P<v1>[1-9][0-9]*))?"
    r"(?:-(?P<c2>[1-9][0-9]*)(?::(?P<v2>[1-9][0-9]*))?)?$"
)
_UNBOUNDED = 10_000


class Canon:
    """The canonical book names and their bounds, read once per root."""

    def __init__(self, root: Path) -> None:
        self.root = Path(root)
        self.books = {book["name"]: book for book in _canon.books(self.root)}
        self._verses: dict[tuple[str, int], int | None] = {}

    def last_verse(self, book: str, chapter: int) -> int | None:
        token = self.books[book]["token"]
        key = (token, chapter)
        if key not in self._verses:
            self._verses[key] = _catena._verse_ceiling(self.root, token, chapter)
        return self._verses[key]

    def parse(self, text: Any) -> tuple[Span | None, str | None]:
        """One `Book C[:V][-C[:V]]` extent, or the reason it is malformed.

        A verse on one end requires a verse on the other, so `Psalms 80-150` is
        chapters and `Matthew 13:36-28:20` is a point-to-point run; nothing
        reads as the index's `Matthew 9:1-9:8` differently from how it wrote.
        """
        if not isinstance(text, str) or not text.strip():
            return None, f"extent {text!r} is not a nonempty string"
        text = text.strip()
        book = next(
            (
                name
                for name in sorted(self.books, key=len, reverse=True)
                if text == name or text.startswith(name + " ")
            ),
            None,
        )
        if book is None:
            return None, f"extent {text!r} names no book of the canon"
        rest = text[len(book):].strip()
        last_chapter = int(self.books[book]["last_chapter"])
        if not rest:
            return Span(book, Point(1, 1), Point(last_chapter, _UNBOUNDED)), None
        match = _RANGE.match(rest)
        if not match:
            return None, f"extent {text!r} is not of the form 'Book C[:V][-C[:V]]'"
        c1 = int(match["c1"])
        c2 = int(match["c2"]) if match["c2"] else c1
        if bool(match["v1"]) != bool(match["v2"]) and match["c2"]:
            return None, (
                f"extent {text!r} gives a verse on one end only; write both ends "
                "as chapter:verse or neither"
            )
        v1 = int(match["v1"]) if match["v1"] else 1
        if match["v2"]:
            v2 = int(match["v2"])
        elif match["v1"] and not match["c2"]:
            v2 = v1
        else:
            v2 = _UNBOUNDED
        for chapter in (c1, c2):
            if chapter > last_chapter:
                return None, (
                    f"extent {text!r} names {book} {chapter}, past its last "
                    f"chapter {last_chapter}"
                )
        for chapter, verse in ((c1, v1), (c2, v2)):
            ceiling = self.last_verse(book, chapter)
            if verse != _UNBOUNDED and ceiling is not None and verse > ceiling:
                return None, (
                    f"extent {text!r} names {book} {chapter}:{verse}, past its "
                    f"last verse {ceiling}"
                )
        if (c1, v1) > (c2, v2):
            return None, f"extent {text!r} ends before it begins"
        return Span(book, Point(c1, v1), Point(c2, v2)), None

    def normalize(self, span: Span) -> Span:
        """Close an open verse bound at the chapter's real last verse."""
        end = span.end
        if end.verse == _UNBOUNDED:
            ceiling = self.last_verse(span.book, end.chapter)
            end = Point(end.chapter, ceiling if ceiling is not None else _UNBOUNDED)
        return Span(span.book, span.begin, end)

    def _next(self, point: Point, book: str) -> Point:
        ceiling = self.last_verse(book, point.chapter)
        if ceiling is not None and point.verse >= ceiling:
            return Point(point.chapter + 1, 1)
        return Point(point.chapter, point.verse + 1)

    def merge(self, spans: list[Span]) -> list[Span]:
        """Adjacent and overlapping spans of one book as one run."""
        merged: list[Span] = []
        for span in sorted(self.normalize(s) for s in spans):
            if merged and merged[-1].book == span.book and span.begin <= self._next(
                merged[-1].end, span.book
            ):
                last = merged[-1]
                merged[-1] = Span(last.book, last.begin, max(last.end, span.end))
            else:
                merged.append(span)
        return merged

    def passage_spans(self, record: dict[str, Any]) -> list[Span]:
        """The canonical passage record `discover` asked about, as spans."""
        book = str(record.get("book") or "")
        if book not in self.books:
            return []
        spans: list[Span] = []
        for entry in record.get("ranges") or []:
            begin = (entry or {}).get("begin") or {}
            end = (entry or {}).get("end") or begin
            try:
                c1 = int(begin["chapter"])
                c2 = int(end.get("chapter", c1))
            except (KeyError, TypeError, ValueError):
                continue
            v1 = begin.get("verse") if isinstance(begin.get("verse"), int) else 1
            v2 = end.get("verse") if isinstance(end.get("verse"), int) else _UNBOUNDED
            spans.append(self.normalize(Span(book, Point(c1, v1), Point(c2, v2))))
        return spans

    def coverage(self, extent: list[Span], asked: list[Span]) -> str:
        """Whether a constituent's extent covers the passage asked about."""
        if not asked:
            return NOT_STATED
        runs = self.merge(extent)
        inside = all(
            any(run.book == span.book and run.begin <= span.begin and span.end <= run.end
                for run in runs)
            for span in asked
        )
        if inside:
            return INSIDE
        touches = any(
            run.book == span.book and run.begin <= span.end and span.begin <= run.end
            for run in runs
            for span in asked
        )
        return PARTIALLY if touches else OUTSIDE


# ---------------------------------------------------------------------------
# The commentary index's identities
# ---------------------------------------------------------------------------


def _fold(text: Any) -> str:
    return " ".join(str(text or "").split()).casefold()


class Identities(NamedTuple):
    index_works: set[tuple[str, str]]
    group_titles: dict[tuple[str, str], set[str]]
    title_to_group: dict[tuple[str, str], tuple[str, str]]
    fragment_works: dict[tuple[str, str], set[str]]
    author_aliases: dict[str, str]


def _yaml(path: Path) -> Any:
    if not path.is_file():
        return {}
    data = _calendars.read_yaml(path)
    return data if isinstance(data, dict) else {}


_IDENTITIES: dict[Path, Identities] = {}


def identities(root: Path = ROOT) -> Identities:
    """The index's (author, title) works, their alias titles, and the fragment joins."""
    root = Path(root)
    if root in _IDENTITIES:
        return _IDENTITIES[root]
    index = _yaml(root / _catena.INDEX_RELATIVE)
    index_works: set[tuple[str, str]] = set()
    for entry in index.get("passages") or []:
        for work in (entry or {}).get("works") or []:
            if isinstance(work, dict):
                index_works.add((str(work.get("author") or ""), str(work.get("title") or "")))
    aliases = _yaml(root / _catena.ALIASES_RELATIVE)
    group_titles: dict[tuple[str, str], set[str]] = {}
    title_to_group: dict[tuple[str, str], tuple[str, str]] = {}
    for group in aliases.get("groups") or []:
        if not isinstance(group, dict):
            continue
        key = (str(group.get("author") or ""), str(group.get("work") or ""))
        titles = {_fold(title) for title in group.get("titles") or []} | {_fold(key[1])}
        group_titles[key] = titles
        for title in titles:
            title_to_group.setdefault((key[0], title), key)
    edges = _yaml(root / _catena.EDGES_RELATIVE)
    fragment_works: dict[tuple[str, str], set[str]] = {}
    for fragment in edges.get("fragments") or []:
        alias = (fragment or {}).get("work_alias")
        if isinstance(alias, dict) and fragment.get("work_id"):
            key = (str(alias.get("author") or ""), str(alias.get("work") or ""))
            fragment_works.setdefault(key, set()).add(str(fragment["work_id"]))
    author_aliases = {
        str(row.get("source_library")): str(row.get("harvest"))
        for row in edges.get("author_aliases") or []
        if isinstance(row, dict)
    }
    value = Identities(index_works, group_titles, title_to_group, fragment_works, author_aliases)
    _IDENTITIES[root] = value
    return value


def _author_forms(responsible: str, aliases: dict[str, str]) -> set[str]:
    """The names a library `responsible` answers to in the harvest's naming.

    The whole string, the part before its first comma -- "Athanasius of
    Alexandria, under whose name the expositions are printed" is Athanasius --
    and any equivalence `fragment-loci.yaml` declares with a reason. Nothing
    looser: two people become one by resemblance.
    """
    forms = {responsible.strip(), responsible.split(",")[0].strip()}
    forms |= {aliases[form] for form in list(forms) if form in aliases}
    return {form for form in forms if form}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def _compiled(patterns: Any, label: str, errors: list[str]) -> list[re.Pattern[str]]:
    compiled: list[re.Pattern[str]] = []
    if not isinstance(patterns, list):
        errors.append(f"{label} must be a list")
        return compiled
    for pattern in patterns:
        try:
            compiled.append(re.compile(str(pattern), re.IGNORECASE))
        except re.error as error:
            errors.append(f"{label}: {pattern!r} does not compile: {error}")
    return compiled


def container_shaped(
    library: dict[str, Any], shapes: dict[str, Any], errors: list[str] | None = None
) -> dict[str, list[str]]:
    """Every record that must carry an entry, with why.

    Declared: a work of a container type, a work whose own description calls
    it a container, an artifact whose own notes call it a whole volume or say
    it carries other works. Derived: a work whose bytes another work's segment
    already points into, or which a catena fragment names as its container.
    The derived half needs no declaring and cannot be forgotten -- the evidence
    that a record holds another work is already in the library.
    """
    errors = errors if errors is not None else []
    work_types = set(shapes.get("work_types") or [])
    described = _compiled(shapes.get("description_patterns") or [], "shapes.description_patterns", errors)
    volumes = _compiled(shapes.get("artifact_patterns") or [], "shapes.artifact_patterns", errors)
    shaped: dict[str, list[str]] = {}
    for work_id, work in library["works"].items():
        if work["work_type"] in work_types:
            shaped.setdefault(work_id, []).append(f"work_type {work['work_type']}")
        for pattern in described:
            if pattern.search(work["description"]):
                shaped.setdefault(work_id, []).append(f"description matches {pattern.pattern!r}")
                break
    for segment_id, segment in library["segments"].items():
        owner = owner_of_artifact(library, segment["artifact_id"])
        constituent = (library["editions"].get(segment["edition_id"]) or {}).get("work_id", "")
        if owner and constituent and owner != constituent:
            shaped.setdefault(owner, []).append(f"segment {segment_id}")
    for artifact_id, artifact in library["artifacts"].items():
        owner = owner_of_artifact(library, artifact_id)
        if owner in shaped:
            continue
        text = f"{artifact['notes']} {artifact['provenance']}"
        for pattern in volumes:
            if pattern.search(text):
                shaped.setdefault(artifact_id, []).append(f"artifact notes match {pattern.pattern!r}")
                break
    return shaped


def _fragment_containers(root: Path, library: dict[str, Any]) -> list[tuple[str, str, str]]:
    """(container work, constituent work, passage) for every fragment's `constituent_of`."""
    edges = _yaml(Path(root) / _catena.EDGES_RELATIVE)
    rows: list[tuple[str, str, str]] = []
    for fragment in edges.get("fragments") or []:
        container = str((fragment or {}).get("constituent_of") or "")
        if not container:
            continue
        owner = (library["editions"].get(container) or {}).get("work_id", "")
        rows.append((owner or container, str(fragment.get("work_id") or ""), str(fragment.get("passage_id") or "")))
    return rows


def validate(root: Path = ROOT) -> list[str]:
    """Every reason the inventory cannot be trusted, deterministically ordered.

    Three refusals carry the weight: a container-shaped record with no entry,
    an entry naming a record the library does not have, and an extent that
    does not parse against the canon. The rest keep an entry honest about the
    bytes it describes: a manifest changed since review, a segment or fragment
    showing a constituent the entry does not list, a constituent named by
    other than the index's own title.
    """
    root = Path(root)
    where = INVENTORY_RELATIVE.as_posix()
    errors: list[str] = []
    try:
        data = load_inventory(root)
    except ContainmentError as error:
        return [str(error)]
    library = catalog(root)
    names = identities(root)
    books = Canon(root)

    unknown = sorted(set(data) - TOP_FIELDS)
    if unknown:
        errors.append(f"{where}: unknown top-level fields: {', '.join(unknown)}")
    if data.get("record_type") != RECORD_TYPE:
        errors.append(f"{where}: record_type must be {RECORD_TYPE!r}")
    if data.get("numbering") != _catena._projection.CANONICAL:
        errors.append(
            f"{where}: numbering is {data.get('numbering')!r}; a scripture extent is "
            f"a canonical address and {_catena._projection.CANONICAL!r} is the only one"
        )
    shapes = data.get("shapes") if isinstance(data.get("shapes"), dict) else {}
    if not shapes:
        errors.append(f"{where}: shapes must be a table declaring what a container looks like")
    unknown = sorted(set(shapes) - SHAPE_FIELDS)
    if unknown:
        errors.append(f"{where}: shapes has unknown fields: {', '.join(unknown)}")
    shaped = container_shaped(library, shapes, errors)

    listed: dict[str, str] = {}
    dispositioned: set[str] = set()

    def claim(record_id: str, label: str) -> None:
        if record_id in listed:
            errors.append(f"{label}: {record_id} is already entered at {listed[record_id]}")
        else:
            listed[record_id] = label

    def pinned(record_id: str, recorded: Any, label: str) -> None:
        actual = manifest_sha256(root, library, record_id)
        if actual is None:
            errors.append(f"{label}: names {record_id}, which is not a work or artifact record in the library")
            return
        if recorded != actual:
            errors.append(
                f"{label}: {record_id} manifest_sha256 is {recorded!r} but its manifest now "
                f"hashes {actual}; the record changed since this entry was reviewed, so "
                f"re-read it and re-pin"
            )

    for ordinal, row in enumerate(_entries(data, "identities"), start=1):
        label = f"{where}: identities[{ordinal}]"
        unknown = sorted(set(row) - IDENTITY_FIELDS)
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        key = (str(row.get("author") or ""), str(row.get("title") or ""))
        if key not in names.index_works:
            errors.append(f"{label} names {key[0]} | {key[1]}, which the commentary index does not list")
        if str(row.get("work_id") or "") not in library["works"]:
            errors.append(f"{label} names {row.get('work_id')!r}, which is not a work record in the library")
        if not str(row.get("reason") or "").strip():
            errors.append(f"{label} states no reason")

    for ordinal, row in enumerate(_entries(data, "not_containers"), start=1):
        label = f"{where}: not_containers[{ordinal}]"
        unknown = sorted(set(row) - NOT_CONTAINER_FIELDS)
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        record_id = str(row.get("id") or "")
        claim(record_id, label)
        dispositioned.add(record_id)
        pinned(record_id, row.get("manifest_sha256"), label)
        if not str(row.get("reason") or "").strip():
            errors.append(f"{label} states no reason")

    constituents_of: dict[str, set[str]] = {}
    for ordinal, row in enumerate(_entries(data, "containers"), start=1):
        record_id = str(row.get("id") or "")
        label = f"{where}: containers[{ordinal}] {record_id}"
        unknown = sorted(set(row) - CONTAINER_FIELDS)
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        claim(record_id, label)
        pinned(record_id, row.get("manifest_sha256"), label)
        status = row.get("status")
        if status not in STATUSES:
            errors.append(f"{label} status is {status!r}; it must be one of {', '.join(STATUSES)}")
        if not str(row.get("basis") or "").strip():
            errors.append(f"{label} states no basis")
        note = str(row.get("unresolved") or "").strip()
        if status in (PARTIAL, UNRESOLVED) and not note:
            errors.append(f"{label} is {status} and must say what is not established, in `unresolved`")
        if status == RESOLVED and note:
            errors.append(f"{label} is resolved and carries an `unresolved` note; one of the two is wrong")
        constituents = row.get("constituents") or []
        if not isinstance(constituents, list):
            errors.append(f"{label} constituents must be a list")
            constituents = []
        if status in (RESOLVED, PARTIAL) and not constituents:
            errors.append(f"{label} is {status} and lists no constituent")
        held = constituents_of.setdefault(record_id, set())
        for number, part in enumerate(constituents, start=1):
            part_label = f"{label} constituents[{number}]"
            if not isinstance(part, dict):
                errors.append(f"{part_label} must be a table")
                continue
            errors.extend(_constituent_errors(part, part_label, library, names, books))
            if part.get("work_id"):
                held.add(str(part["work_id"]))

    for record_id, reasons in sorted(shaped.items()):
        if record_id not in listed:
            errors.append(
                f"{where}: {record_id} is container-shaped ({reasons[0]}) and has no "
                f"containment entry; add it to `containers`, or to `not_containers` "
                f"with the reason it holds no other work"
            )

    evidence = [
        (owner_of_artifact(library, s["artifact_id"]),
         (library["editions"].get(s["edition_id"]) or {}).get("work_id", ""),
         f"segment {segment_id}", s["artifact_id"])
        for segment_id, s in sorted(library["segments"].items())
    ] + [
        (owner, work_id, f"fragment {passage_id} (constituent_of)", "")
        for owner, work_id, passage_id in _fragment_containers(root, library)
    ]
    for owner, constituent, source, artifact_id in evidence:
        if not owner or not constituent or owner == constituent:
            continue
        entered = constituents_of.get(owner, set()) | constituents_of.get(artifact_id, set())
        if owner in dispositioned:
            errors.append(f"{where}: {source} shows {owner} holds {constituent}, but {owner} is entered as not a container")
        elif constituent not in entered:
            errors.append(
                f"{where}: {source} shows {owner} holds {constituent}, and its containment "
                f"entry does not list that work as a constituent"
            )
    return sorted(set(errors))


def _constituent_errors(
    part: dict[str, Any],
    label: str,
    library: dict[str, Any],
    names: Identities,
    books: Canon,
) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(part) - CONSTITUENT_FIELDS)
    if unknown:
        errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
    author = str(part.get("author") or "").strip()
    title = str(part.get("title") or "").strip()
    if not author or not title:
        errors.append(f"{label} needs an author and a title")
    work_id = part.get("work_id")
    if work_id is not None and str(work_id) not in library["works"]:
        errors.append(f"{label} names {work_id!r}, which is not a work record in the library")
    if not str(part.get("basis") or "").strip():
        errors.append(f"{label} states no basis for its identity and extent")
    # A constituent the index lists must be called what the index calls it, or
    # discover cannot join it and the holding goes unreported.
    if (author, title) not in names.index_works:
        group = names.title_to_group.get((author, _fold(title)))
        if group is not None and group[1] != title and group in names.index_works:
            errors.append(
                f"{label} names {author} | {title}; the commentary index calls that "
                f"work {group[1]!r}, and only that title joins it"
            )
    extent_fields = [key for key in ("scripture", "whole", "locator", "extent_unresolved") if key in part]
    if not extent_fields:
        errors.append(
            f"{label} states no extent: give scripture, whole, locator, or "
            f"extent_unresolved with the reason it cannot be established"
        )
    if "whole" in part and not isinstance(part["whole"], bool):
        errors.append(f"{label} whole must be true or false")
    for key in ("locator", "extent_unresolved"):
        if key in part and not str(part[key] or "").strip():
            errors.append(f"{label} {key} is empty")
    if "scripture" in part:
        spans = part["scripture"]
        if not isinstance(spans, list) or not spans:
            errors.append(f"{label} scripture must be a nonempty list of extents")
        else:
            for text in spans:
                _, problem = books.parse(text)
                if problem:
                    errors.append(f"{label} has a malformed extent: {problem}")
    return errors


# ---------------------------------------------------------------------------
# Holdings, for discover
# ---------------------------------------------------------------------------


class Holdings:
    """What the library holds of each lead `discover` returns.

    Built once per run: the catalog, the inventory, and the identity joins are
    the same for every work on every passage asked about.
    """

    def __init__(self, root: Path = ROOT) -> None:
        self.root = Path(root)
        self.library = catalog(self.root)
        self.names = identities(self.root)
        self.books = Canon(self.root)
        try:
            self.inventory = load_inventory(self.root)
        except ContainmentError:
            self.inventory = {}
        self.containers = _entries(self.inventory, "containers")
        self.identity_rows = _entries(self.inventory, "identities")
        self._by_author: dict[str, list[str]] = {}
        for work_id, work in self.library["works"].items():
            for form in _author_forms(work["responsible"], self.names.author_aliases):
                self._by_author.setdefault(form, []).append(work_id)
        self._segments_by_edition: dict[str, list[str]] = {}
        for segment_id, segment in self.library["segments"].items():
            self._segments_by_edition.setdefault(segment["edition_id"], []).append(segment_id)
        self._artifacts_by_edition: dict[str, list[str]] = {}
        for artifact_id, artifact in self.library["artifacts"].items():
            self._artifacts_by_edition.setdefault(artifact["edition_id"], []).append(artifact_id)

    # -- joins ---------------------------------------------------------------

    def library_works(self, author: str, title: str, work_id: str | None) -> dict[str, list[str]]:
        """Library work ids for one index lead, each with how it was reached."""
        found: dict[str, list[str]] = {}

        def add(identifier: str, how: str) -> None:
            if identifier in self.library["works"] and how not in found.setdefault(identifier, []):
                found[identifier].append(how)

        if work_id:
            add(work_id, "index-work-id")
        for row in self.identity_rows:
            if (str(row.get("author") or ""), str(row.get("title") or "")) == (author, title):
                add(str(row.get("work_id") or ""), "identity")
        for container in self.containers:
            for part in container.get("constituents") or []:
                if (
                    isinstance(part, dict)
                    and part.get("work_id")
                    and (str(part.get("author") or ""), str(part.get("title") or "")) == (author, title)
                ):
                    add(str(part["work_id"]), "constituent")
        for identifier in sorted(self.names.fragment_works.get((author, title), ())):
            add(identifier, "fragment-edge")
        titles = self.names.group_titles.get((author, title), set()) | {_fold(title)}
        for identifier in self._by_author.get(author, []):
            work = self.library["works"][identifier]
            own = {_fold(work["title"])} | {_fold(t) for t in work["alternate_titles"]}
            if own & titles:
                add(identifier, "title")
        return {key: sorted(value, key=JOINS.index) for key, value in sorted(found.items())}

    # -- reports -------------------------------------------------------------

    def _edition_report(self, edition_id: str) -> dict[str, Any]:
        edition = self.library["editions"][edition_id]
        artifacts = sorted(self._artifacts_by_edition.get(edition_id, []))
        segments = []
        for segment_id in sorted(self._segments_by_edition.get(edition_id, [])):
            segment = self.library["segments"][segment_id]
            segments.append(
                {
                    "segment_id": segment_id,
                    "artifact_id": segment["artifact_id"],
                    "container_work_id": owner_of_artifact(self.library, segment["artifact_id"]),
                    "storage": self.library["artifacts"].get(segment["artifact_id"], {}).get("storage", ""),
                }
            )
        return {
            "edition_id": edition_id,
            "title": edition["title"],
            "language": edition["language"],
            "artifacts": [
                {
                    "artifact_id": artifact_id,
                    "storage": self.library["artifacts"][artifact_id]["storage"],
                    "artifact_type": self.library["artifacts"][artifact_id]["artifact_type"],
                }
                for artifact_id in artifacts
            ],
            "segments": segments,
            "passages": edition["passages"],
        }

    def _direct_report(self, work_id: str, joined_by: list[str]) -> dict[str, Any]:
        work = self.library["works"][work_id]
        editions = sorted(
            edition_id
            for edition_id, edition in self.library["editions"].items()
            if edition["work_id"] == work_id
        )
        reports = [self._edition_report(edition_id) for edition_id in editions]
        artifact_ids = [a["artifact_id"] for r in reports for a in r["artifacts"]]
        return {
            "work_id": work_id,
            "title": work["title"],
            "responsible": work["responsible"],
            "joined_by": joined_by,
            "languages": sorted({r["language"] for r in reports if r["language"]}),
            "artifact_storage": storage_counts(self.library, artifact_ids),
            "segment_count": sum(len(r["segments"]) for r in reports),
            "passage_count": sum(r["passages"] for r in reports),
            "editions": reports,
        }

    def _container_title(self, record_id: str) -> tuple[str, str]:
        if record_id in self.library["works"]:
            return "work", self.library["works"][record_id]["title"]
        artifact = self.library["artifacts"].get(record_id) or {}
        edition = self.library["editions"].get(artifact.get("edition_id", "")) or {}
        return "artifact", f"{edition.get('title', '')} [{artifact.get('artifact_type', '')}]"

    def _container_artifacts(self, record_id: str) -> list[str]:
        if record_id in self.library["works"]:
            return artifacts_of_work(self.library, record_id)
        return [record_id] if record_id in self.library["artifacts"] else []

    def for_work(
        self,
        author: str,
        title: str,
        work_id: str | None,
        asked: list[Span],
    ) -> dict[str, Any]:
        """Every registered holding of one lead, and whether each reaches the passage."""
        joined = self.library_works(author, title, work_id)
        direct = [self._direct_report(identifier, how) for identifier, how in joined.items()]
        containers: list[dict[str, Any]] = []
        for container in self.containers:
            record_id = str(container.get("id") or "")
            if record_id not in self.library["works"] and record_id not in self.library["artifacts"]:
                continue
            parts = [part for part in container.get("constituents") or [] if isinstance(part, dict)]
            named = [
                part
                for part in parts
                if (str(part.get("author") or ""), str(part.get("title") or "")) == (author, title)
            ]
            # A constituent named as the lead is the answer. One reached only
            # through a library record the lead joins is a PART of the lead --
            # Theodoret's Galatians inside his whole Pauline commentary -- and
            # is reported only where nothing in the container names the lead
            # itself, so a part never stands in for a whole the container has.
            matched = named or [
                part
                for part in parts
                if part.get("work_id") and str(part["work_id"]) in joined
            ]
            for part in matched:
                kind, container_title = self._container_title(record_id)
                containers.append(
                    {
                        "container_id": record_id,
                        "container_kind": kind,
                        "container_title": container_title,
                        "container_status": container.get("status"),
                        "artifact_storage": storage_counts(
                            self.library, self._container_artifacts(record_id)
                        ),
                        "constituent": {
                            key: part[key]
                            for key in (
                                "author",
                                "title",
                                "work_id",
                                "scripture",
                                "whole",
                                "locator",
                                "extent_unresolved",
                            )
                            if key in part
                        },
                        "passage": self._coverage(part, asked),
                    }
                )
        containers.sort(key=lambda row: (row["container_id"], row["constituent"].get("title", "")))
        return {
            "status": self._status(direct, containers),
            "direct": direct,
            "containers": containers,
        }

    def _coverage(self, part: dict[str, Any], asked: list[Span]) -> str:
        if isinstance(part.get("scripture"), list) and part["scripture"]:
            spans = [span for span, _ in (self.books.parse(t) for t in part["scripture"]) if span]
            if spans:
                return self.books.coverage(spans, asked)
        if part.get("whole") is True:
            return WHOLE_WORK
        return NOT_STATED

    @staticmethod
    def _status(direct: list[dict[str, Any]], containers: list[dict[str, Any]]) -> str:
        if any(d["artifact_storage"] or d["segment_count"] for d in direct):
            return HELD
        if any(c["artifact_storage"] for c in containers):
            return HELD_IN_CONTAINER
        if direct or containers:
            return CATALOGED
        return NONE


# ---------------------------------------------------------------------------
# The report the check verb prints
# ---------------------------------------------------------------------------


def report(root: Path = ROOT) -> dict[str, Any]:
    """The inventory, summarized, with every container's resolution state."""
    root = Path(root)
    errors = validate(root)
    try:
        data = load_inventory(root)
    except ContainmentError:
        data = {}
    names = identities(root)
    library = catalog(root)
    containers = []
    for row in _entries(data, "containers"):
        parts = [p for p in row.get("constituents") or [] if isinstance(p, dict)]
        record_id = str(row.get("id") or "")
        kind = "work" if record_id in library["works"] else "artifact"
        containers.append(
            {
                "id": record_id,
                "kind": kind,
                "status": row.get("status"),
                "unresolved": row.get("unresolved", ""),
                "constituents": [
                    {
                        **{key: part[key] for key in sorted(part) if key != "basis"},
                        "in_index": (str(part.get("author") or ""), str(part.get("title") or ""))
                        in names.index_works,
                    }
                    for part in parts
                ],
            }
        )
    by_status = {status: 0 for status in STATUSES}
    for row in containers:
        if row["status"] in by_status:
            by_status[row["status"]] += 1
    constituents = [part for row in containers for part in row["constituents"]]
    return {
        "schema": REPORT_SCHEMA,
        "status": "invalid" if errors else "ok",
        "errors": errors,
        "inventory": INVENTORY_RELATIVE.as_posix(),
        "audited_on": data.get("audited_on"),
        "totals": {
            "containers": len(containers),
            "work_containers": len([row for row in containers if row["kind"] == "work"]),
            "artifact_containers": len([row for row in containers if row["kind"] == "artifact"]),
            "by_status": by_status,
            "constituents": len(constituents),
            "constituents_in_index": len([part for part in constituents if part["in_index"]]),
            "not_containers": len(_entries(data, "not_containers")),
            "identities": len(_entries(data, "identities")),
        },
        "containers": containers,
    }
