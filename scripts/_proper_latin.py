"""Per-text Latin provenance and publication decisions for Mass propers.

The calendar index is a transcription and not, by itself, a publication
permission record.  This module joins each text-bearing owner to a sidecar by
an exact hash and keeps two questions separate:

* provenance: which witness, locator, and comparison establish these words;
* publication: which basis permits these words on which output surfaces.

No record, a stale hash, or an incomplete permission is an unresolved decision
and therefore emits no wording.  In particular, identifying a Vatican edition
as the witness never implies permission to reproduce it.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from typing import Iterable, Iterator, Mapping
import copy
import json
import os
import sys
import tomllib

import _calendars
from _tooling import tree_fingerprint


SCHEMA = "triptych-proper-latin-provenance/v1"
SIDECAR_SUFFIX = "-proper-latin-provenance-v1.toml"
POLICY = "guidance/liturgical-text-publication-policy.md"
TRUSTED_REPOSITORY = Path(__file__).resolve().parents[1]

PROVENANCE_STATES = frozenset({"unresolved", "identified", "collated"})
PUBLICATION_STATES = frozenset({"unresolved", "withheld", "permitted"})
PUBLICATION_BASES = frozenset(
    {
        "unresolved",
        "public-domain",
        "project-created",
        "permission",
        "licensed",
        "restricted",
        "non-exact-historical-witness",
    }
)
AFFIRMATIVE_PUBLICATION_BASES = frozenset(
    {"public-domain", "project-created", "permission", "licensed"}
)
SURFACES = frozenset(
    {"web", "download", "print", "cli", "corpus-data", "public-git"}
)
STRUCTURE_SURFACES = frozenset({"web", "download", "print"})
CLI_SURFACES = frozenset({"cli"})
TRACKED_SURFACES = frozenset({"corpus-data", "public-git"})
EXACT_WITNESS_TYPES = frozenset({"artifact", "segment", "passage"})

KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
DEFAULT_FIELDS = frozenset(
    {"provenance_status", "publication_status", "publication_basis", "surfaces"}
)
ENTRY_FIELDS = frozenset(
    {
        *KEY_FIELDS,
        "text_sha256",
        "body_status",
        "provenance_status",
        "source_id",
        "source_date",
        "locator",
        "relationship",
        "verification_source_id",
        "verification_locator",
        "transformations",
        "provenance_evidence",
        "provenance_authority",
        "provenance_confidence",
        "publication_status",
        "publication_basis",
        "surfaces",
        "publication_source_ids",
        "publication_locator",
        "publication_authority",
        "publication_evidence",
        "publication_retrieved",
        "notice",
        "note",
    }
)
REMOVED_BODY_STATUS = "removed"
REMOVED_TEXT_STATUS = {
    "state": "unavailable",
    "scope": "proper-body",
}


@dataclass(frozen=True, order=True)
class LatinKey:
    """The node that owns one text value, including cycle variants."""

    mass: str
    form: str
    proper: str
    course: str = ""
    cycle: str = ""
    # One-based source order among otherwise identical keys. Repeated slot
    # names are legitimate (Palm Sunday has six Procession Antiphons), so the
    # name alone is not an identity.
    occurrence: int = 0

    @classmethod
    def from_mapping(cls, row: Mapping[str, object]) -> "LatinKey":
        return cls(
            *(str(row.get(field) or "") for field in KEY_FIELDS[:-1]),
            int(row.get("occurrence") or 0),
        )

    def as_dict(self) -> dict[str, object]:
        return {field: getattr(self, field) for field in KEY_FIELDS}

    def label(self) -> str:
        suffix = f"/{self.course}:{self.cycle}" if self.course else ""
        form = f"/{self.form}" if self.form else ""
        occurrence = f"#{self.occurrence}" if self.occurrence else ""
        return f"{self.mass}{form}/{self.proper}{suffix}{occurrence}"


@dataclass(frozen=True)
class LatinDecision:
    """A provenance statement and a distinct, surface-specific permission."""

    key: LatinKey
    text_sha256: str
    provenance_status: str
    publication_status: str
    publication_basis: str
    surfaces: frozenset[str]
    source_id: str = ""
    source_date: str = ""
    locator: str = ""
    relationship: str = ""
    verification_source_id: str = ""
    verification_locator: str = ""
    transformations: tuple[str, ...] = ()
    provenance_evidence: str = ""
    provenance_authority: str = ""
    provenance_confidence: str = ""
    authority: str = ""
    evidence: str = ""
    publication_source_ids: tuple[str, ...] = ()
    publication_locator: str = ""
    publication_retrieved: str = ""
    notice: str = ""
    note: str = ""
    reason: str = ""

    def permits(self, wanted: Iterable[str]) -> bool:
        return (
            not self.reason
            and self.publication_status == "permitted"
            and self.publication_basis in AFFIRMATIVE_PUBLICATION_BASES
            and set(wanted).issubset(self.surfaces)
        )

    def projection(self, wanted: Iterable[str]) -> dict[str, object]:
        required = frozenset(wanted)
        permitted = self.permits(required)
        reason = self.reason
        if not reason and not permitted:
            missing = sorted(required - self.surfaces)
            if self.publication_status != "permitted":
                reason = f"publication status is {self.publication_status}"
            elif self.publication_basis not in AFFIRMATIVE_PUBLICATION_BASES:
                reason = f"publication basis is {self.publication_basis}"
            elif missing:
                reason = "permission does not cover " + ", ".join(missing)
        provenance = {"status": self.provenance_status}
        for field in (
            "source_id",
            "source_date",
            "locator",
            "relationship",
            "verification_source_id",
            "verification_locator",
            "provenance_evidence",
            "provenance_authority",
            "provenance_confidence",
        ):
            if value := getattr(self, field):
                provenance[field] = value
        provenance["transformations"] = list(self.transformations)
        publication: dict[str, object] = {
            "status": self.publication_status,
            "basis": self.publication_basis,
            "surfaces": sorted(self.surfaces),
        }
        for field, value in (
            ("source_ids", list(self.publication_source_ids)),
            ("locator", self.publication_locator),
            ("authority", self.authority),
            ("evidence", self.evidence),
            ("retrieved", self.publication_retrieved),
            ("notice", self.notice),
        ):
            if value:
                publication[field] = value
        return {
            "text_sha256": self.text_sha256,
            "provenance": provenance,
            "publication": publication,
            "withheld": not permitted,
            "reason": reason or None,
            **({"note": self.note} if self.note else {}),
        }


def text_sha256(text: str) -> str:
    """Hash the exact Unicode text obtained from the calendar YAML."""
    return sha256(text.encode("utf-8")).hexdigest()


def _is_removed_body_owner(proper: Mapping[str, object]) -> bool:
    """Whether a text-free proper is an explicit rights quarantine.

    This is deliberately narrower than a generic unavailable status.  A
    witness gap has no former body for the provenance ledger to retain, while
    a rights-withheld proper does.  The ledger records the former exact hash;
    it never reconstructs the removed wording.
    """
    status = proper.get("text_status")
    if not isinstance(status, dict) or any(
        status.get(field) != value for field, value in REMOVED_TEXT_STATUS.items()
    ):
        return False
    reasons = status.get("reasons")
    return isinstance(reasons, list) and any(
        isinstance(reason, dict) and reason.get("kind") == "rights-withheld"
        for reason in reasons
    )


def body_owners(
    document: Mapping[str, object],
) -> Iterator[tuple[LatinKey, str | None, str]]:
    """Every present or explicitly removed direct Latin body owner.

    Occurrence is assigned across both states, so deleting one of several
    same-named bodies cannot renumber or collapse the retained sidecar rows.
    """
    sections = document.get("sections")
    if not isinstance(sections, dict):
        return
    occurrences: dict[tuple[str, str, str, str, str], int] = {}

    def identified(base: LatinKey) -> LatinKey:
        bare = (base.mass, base.form, base.proper, base.course, base.cycle)
        occurrences[bare] = occurrences.get(bare, 0) + 1
        return LatinKey(*bare, occurrences[bare])

    for section in sections.values():
        if not isinstance(section, dict):
            continue
        for mass in section.get("masses") or []:
            if not isinstance(mass, dict):
                continue
            groups: list[tuple[str, object]] = [("", mass.get("propers"))]
            groups.extend(
                (str(form.get("name") or ""), form.get("propers"))
                for form in mass.get("forms") or []
                if isinstance(form, dict)
            )
            for form, propers in groups:
                for proper in propers or []:
                    if not isinstance(proper, dict):
                        continue
                    base = LatinKey(
                        str(mass.get("key") or ""),
                        form,
                        str(proper.get("name") or ""),
                    )
                    if isinstance(proper.get("text"), str):
                        yield identified(base), proper["text"], "present"
                    elif _is_removed_body_owner(proper):
                        yield identified(base), None, REMOVED_BODY_STATUS
                    for course in ("cycles", "weekday_cycles"):
                        branches = proper.get(course)
                        if not isinstance(branches, dict):
                            # Calendar schema validation owns this shape.  The
                            # Latin sidecar join must preserve that actionable
                            # error instead of replacing it with AttributeError.
                            continue
                        for cycle, owner in branches.items():
                            if not isinstance(owner, dict):
                                continue
                            if isinstance(owner.get("text"), str):
                                yield (
                                    identified(
                                        LatinKey(
                                            base.mass,
                                            base.form,
                                            base.proper,
                                            course,
                                            str(cycle),
                                        )
                                    ),
                                    owner["text"],
                                    "present",
                                )
                            elif _is_removed_body_owner(owner):
                                yield (
                                    identified(
                                        LatinKey(
                                            base.mass,
                                            base.form,
                                            base.proper,
                                            course,
                                            str(cycle),
                                        )
                                    ),
                                    None,
                                    REMOVED_BODY_STATUS,
                                )


def text_owners(document: Mapping[str, object]) -> Iterator[tuple[LatinKey, str]]:
    """Every present direct text node, without resolving references."""
    for key, text, status in body_owners(document):
        if status == "present" and isinstance(text, str):
            yield key, text


def _unresolved(key: LatinKey, text: str, reason: str) -> LatinDecision:
    return LatinDecision(
        key=key,
        text_sha256=text_sha256(text),
        provenance_status="unresolved",
        publication_status="unresolved",
        publication_basis="unresolved",
        surfaces=frozenset(),
        reason=reason,
    )


def _decision(
    key: LatinKey,
    text: str,
    row: Mapping[str, object] | None,
) -> LatinDecision:
    if row is None:
        return _unresolved(key, text, "no per-text Latin provenance record")
    actual = text_sha256(text)
    recorded = str(row.get("text_sha256") or "")
    if recorded != actual:
        return _unresolved(key, text, "Latin provenance record has a stale text hash")
    surfaces = row.get("surfaces")
    return LatinDecision(
        key=key,
        text_sha256=actual,
        provenance_status=str(row.get("provenance_status") or "unresolved"),
        publication_status=str(row.get("publication_status") or "unresolved"),
        publication_basis=str(row.get("publication_basis") or "unresolved"),
        surfaces=(
            frozenset(str(one) for one in surfaces)
            if isinstance(surfaces, list)
            else frozenset()
        ),
        source_id=str(row.get("source_id") or ""),
        source_date=str(row.get("source_date") or ""),
        locator=str(row.get("locator") or ""),
        relationship=str(row.get("relationship") or ""),
        verification_source_id=str(row.get("verification_source_id") or ""),
        verification_locator=str(row.get("verification_locator") or ""),
        transformations=tuple(
            str(one) for one in (row.get("transformations") or [])
        ),
        provenance_evidence=str(row.get("provenance_evidence") or ""),
        provenance_authority=str(row.get("provenance_authority") or ""),
        provenance_confidence=str(row.get("provenance_confidence") or ""),
        authority=str(row.get("publication_authority") or ""),
        evidence=str(row.get("publication_evidence") or ""),
        publication_source_ids=tuple(
            str(one) for one in (row.get("publication_source_ids") or [])
        ),
        publication_locator=str(row.get("publication_locator") or ""),
        publication_retrieved=str(row.get("publication_retrieved") or ""),
        notice=str(row.get("notice") or ""),
        note=str(row.get("note") or ""),
    )


def decision_for(
    key: LatinKey,
    text: str,
    records: Mapping[LatinKey, Mapping[str, object]],
) -> LatinDecision:
    """Find exactly one occurrence whose recorded hash answers this owner.

    Direct-source projections pass an occurrence. Resolved/taken-from propers
    currently carry only the terminal mass/form/name, so their occurrence is
    recovered by exact hash. More than one matching occurrence is not guessed:
    two locators may carry the same wording under different permissions.
    """
    if key.occurrence:
        return _decision(key, text, records.get(key))
    candidates = [
        (candidate, row)
        for candidate, row in records.items()
        if (
            candidate.mass,
            candidate.form,
            candidate.proper,
            candidate.course,
            candidate.cycle,
        )
        == (key.mass, key.form, key.proper, key.course, key.cycle)
    ]
    matching = [
        (candidate, row)
        for candidate, row in candidates
        if row.get("text_sha256") == text_sha256(text)
    ]
    if len(matching) == 1:
        return _decision(matching[0][0], text, matching[0][1])
    if len(matching) > 1:
        return _unresolved(key, text, "Latin provenance occurrence is ambiguous")
    if candidates:
        return _unresolved(key, text, "Latin provenance record has a stale text hash")
    return _unresolved(key, text, "no per-text Latin provenance record")


def _row_problems(where: str, row: Mapping[str, object]) -> list[str]:
    problems: list[str] = []
    unknown = sorted(set(row) - ENTRY_FIELDS)
    if unknown:
        problems.append(f"{where}: unknown fields: {', '.join(unknown)}")
    for field in KEY_FIELDS[:-1]:
        if field not in row or not isinstance(row.get(field), str):
            problems.append(f"{where}: {field} must be a string")
    occurrence = row.get("occurrence")
    if not isinstance(occurrence, int) or isinstance(occurrence, bool) or occurrence < 1:
        problems.append(f"{where}: occurrence must be a positive integer")
    digest = row.get("text_sha256")
    if (
        not isinstance(digest, str)
        or len(digest) != 64
        or any(c not in "0123456789abcdef" for c in digest)
    ):
        problems.append(f"{where}: text_sha256 must be 64 lowercase hexadecimal characters")
    body_status = row.get("body_status")
    if body_status is not None and body_status != REMOVED_BODY_STATUS:
        problems.append(
            f"{where}: body_status, when present, must be {REMOVED_BODY_STATUS!r}"
        )
    provenance = row.get("provenance_status")
    publication = row.get("publication_status")
    basis = row.get("publication_basis")
    surfaces = row.get("surfaces")
    if provenance not in PROVENANCE_STATES:
        problems.append(f"{where}: unknown provenance_status {provenance!r}")
    if publication not in PUBLICATION_STATES:
        problems.append(f"{where}: unknown publication_status {publication!r}")
    if basis not in PUBLICATION_BASES:
        problems.append(f"{where}: unknown publication_basis {basis!r}")
    if not isinstance(surfaces, list) or any(one not in SURFACES for one in surfaces):
        problems.append(f"{where}: surfaces must contain only {sorted(SURFACES)}")
        surfaces = []
    elif len(surfaces) != len(set(surfaces)):
        problems.append(f"{where}: surfaces repeats a value")
    publication_source_ids = row.get("publication_source_ids")
    if publication_source_ids is not None and (
        not isinstance(publication_source_ids, list)
        or not publication_source_ids
        or any(
            not isinstance(one, str) or not one.strip()
            for one in publication_source_ids
        )
    ):
        problems.append(
            f"{where}: publication_source_ids must be a nonempty list of source IDs"
        )
        publication_source_ids = []
    elif isinstance(publication_source_ids, list) and len(publication_source_ids) != len(
        set(publication_source_ids)
    ):
        problems.append(f"{where}: publication_source_ids repeats a value")

    source_id = row.get("source_id")
    source_date = row.get("source_date")
    locator = row.get("locator")
    relationship = row.get("relationship")
    if provenance in {"identified", "collated"}:
        if basis != "project-created":
            for field, value in (
                ("source_id", source_id),
                ("source_date", source_date),
                ("locator", locator),
                ("relationship", relationship),
                ("provenance_evidence", row.get("provenance_evidence")),
                ("provenance_authority", row.get("provenance_authority")),
                ("provenance_confidence", row.get("provenance_confidence")),
            ):
                if not isinstance(value, str) or not value.strip():
                    problems.append(f"{where}: {provenance} provenance requires {field}")
    elif any(
        row.get(field)
        for field in (
            "source_id",
            "source_date",
            "locator",
            "relationship",
            "verification_source_id",
            "verification_locator",
            "transformations",
            "provenance_evidence",
            "provenance_authority",
            "provenance_confidence",
        )
    ):
        problems.append(
            f"{where}: unresolved provenance must not carry witness, review, "
            "transformation, or confidence claims"
        )
    transformations = row.get("transformations")
    if provenance in {"identified", "collated"}:
        if not isinstance(transformations, list) or any(
            not isinstance(one, str) or not one.strip() for one in transformations
        ):
            problems.append(f"{where}: identified provenance requires a transformations list")
        if not isinstance(row.get("provenance_evidence"), str) or not str(
            row.get("provenance_evidence")
        ).strip():
            problems.append(f"{where}: identified provenance requires provenance_evidence")
        confidence = row.get("provenance_confidence")
        if confidence not in {"low", "medium", "high"}:
            problems.append(f"{where}: provenance_confidence must be low, medium, or high")
    if provenance == "collated" and basis != "project-created":
        for field in ("verification_source_id", "verification_locator"):
            if not isinstance(row.get(field), str) or not str(row.get(field)).strip():
                problems.append(f"{where}: collated provenance requires {field}")

    if publication == "permitted":
        if provenance not in {"identified", "collated"}:
            problems.append(f"{where}: permitted publication requires identified provenance")
        if basis not in AFFIRMATIVE_PUBLICATION_BASES:
            problems.append(
                f"{where}: permitted publication needs an affirmative basis; "
                f"{basis!r} is intrinsically nonpublishable"
            )
        if not surfaces:
            problems.append(f"{where}: permitted publication must name its output surfaces")
        elif not TRACKED_SURFACES.issubset(surfaces):
            problems.append(
                f"{where}: permitted publication must cover corpus-data and public-git "
                "while the text remains in the tracked public calendar corpus"
            )
        if not isinstance(row.get("publication_evidence"), str) or not str(
            row.get("publication_evidence")
        ).strip():
            problems.append(f"{where}: permitted publication requires evidence")
        if basis != "project-created":
            if not publication_source_ids:
                problems.append(
                    f"{where}: {basis} publication requires independent "
                    "publication_source_ids"
                )
            if not isinstance(row.get("publication_locator"), str) or not str(
                row.get("publication_locator")
            ).strip():
                problems.append(
                    f"{where}: {basis} publication requires a rights-evidence locator"
                )
        if basis == "public-domain":
            if provenance != "collated":
                problems.append(f"{where}: public-domain publication requires per-text collation")
            if relationship not in {
                "exact-transcription",
                "collated-exact",
                "editorial-projection-exact-to-target",
            }:
                problems.append(
                    f"{where}: public-domain publication requires an exact witness relationship"
                )
        elif basis == "project-created":
            if provenance not in {"identified", "collated"}:
                problems.append(
                    f"{where}: project-created publication requires identified authorship"
                )
            if relationship != "project-authored":
                problems.append(
                    f"{where}: project-created publication requires project-authored relationship"
                )
        elif basis in {"permission", "licensed"}:
            if not isinstance(row.get("publication_authority"), str) or not str(
                row.get("publication_authority")
            ).strip():
                problems.append(f"{where}: {basis} publication requires a named authority")
            if not isinstance(row.get("notice"), str) or not str(row.get("notice")).strip():
                problems.append(f"{where}: {basis} publication requires its conditioned notice")
            retrieved = row.get("publication_retrieved")
            try:
                parsed_retrieved = date.fromisoformat(str(retrieved))
            except ValueError:
                parsed_retrieved = None
            if (
                not isinstance(retrieved, str)
                or parsed_retrieved is None
                or parsed_retrieved.isoformat() != retrieved
            ):
                problems.append(f"{where}: {basis} publication requires an ISO retrieval date")
    else:
        if surfaces:
            problems.append(f"{where}: only permitted publication may name output surfaces")
        if publication_source_ids:
            problems.append(
                f"{where}: only permitted publication may name publication_source_ids"
            )
        if publication == "unresolved" and basis != "unresolved":
            problems.append(f"{where}: unresolved publication must keep its basis unresolved")
        if publication == "withheld" and basis not in {
            "restricted",
            "unresolved",
            "non-exact-historical-witness",
        }:
            problems.append(f"{where}: withheld publication has incompatible basis {basis!r}")
    if body_status == REMOVED_BODY_STATUS:
        # Quarantine must never manufacture evidence.  The former exact hash
        # remains useful even when the transcription's witness is unresolved;
        # removal changes residence/publication, not provenance confidence.
        if publication == "permitted":
            problems.append(f"{where}: a removed body cannot be permitted for publication")
        if surfaces:
            problems.append(f"{where}: a removed body must have no publication surfaces")
    return problems


def read_sidecar(path: Path) -> tuple[dict[LatinKey, dict], list[str]]:
    """Read one sidecar. Invalid rows remain unusable and therefore fail closed."""
    try:
        document = _calendars.read_toml(path)
    except (OSError, tomllib.TOMLDecodeError) as error:
        return {}, [f"{path}: unreadable: {error}"]
    problems: list[str] = []
    if document.get("schema") != SCHEMA:
        problems.append(f"{path}: schema must be {SCHEMA!r}")
    if document.get("language") != "la":
        problems.append(f"{path}: language must be 'la'")
    expected_calendar = path.name.removesuffix(SIDECAR_SUFFIX)
    if document.get("calendar") != expected_calendar:
        problems.append(
            f"{path}: calendar must be {expected_calendar!r}, got {document.get('calendar')!r}"
        )
    if document.get("policy") != POLICY:
        problems.append(f"{path}: policy must be {POLICY!r}")
    defaults = document.get("defaults")
    if not isinstance(defaults, dict):
        problems.append(f"{path}: defaults must be a table")
        defaults = {}
    unknown = sorted(set(defaults) - DEFAULT_FIELDS)
    if unknown:
        problems.append(f"{path}: defaults has unknown fields: {', '.join(unknown)}")
    expected_defaults = {
        "provenance_status": "unresolved",
        "publication_status": "unresolved",
        "publication_basis": "unresolved",
        "surfaces": [],
    }
    for field, expected in expected_defaults.items():
        if defaults.get(field) != expected:
            problems.append(
                f"{path}: defaults.{field} must be {expected!r}; publication is decided per text"
            )

    records: dict[LatinKey, dict] = {}
    entries = document.get("entries")
    if not isinstance(entries, list):
        return {}, [*problems, f"{path}: entries must be an array of tables"]
    for index, candidate in enumerate(entries):
        where = f"{path}: entries[{index}]"
        if not isinstance(candidate, dict):
            problems.append(f"{where}: entry must be a table")
            continue
        row = {**defaults, **candidate}
        found = _row_problems(where, row)
        problems.extend(found)
        key = LatinKey.from_mapping(row)
        if key in records:
            problems.append(f"{where}: duplicate key {key.label()}")
            continue
        if not found:
            records[key] = row
    return records, problems


def sidecar_path(inventory_root: Path, calendar: str) -> Path:
    return inventory_root / f"{calendar}{SIDECAR_SUFFIX}"


_SOURCE_LIBRARY_CACHE: dict[
    Path, tuple[dict[str, dict[str, object]], tuple[str, ...]]
] = {}


SOURCE_LIBRARY_CACHE_DIR = TRUSTED_REPOSITORY / "build" / "source-library-cache"
# A sandbox fixture is a handful of files; the real library is ~19,000. Below
# this the load is already cheap and an entry would never be read twice, so the
# suite's thousands of throwaway trees leave nothing behind.
SOURCE_LIBRARY_CACHE_FLOOR = 1000


def _prune_source_library_cache(directory: Path, keep: int) -> None:
    """Keep the newest *keep* entries; each is ~25MB and keyed by the tree."""
    try:
        entries = sorted(
            (path for path in directory.glob("*.json") if path.is_file()),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
    except OSError:
        return
    for stale in entries[keep:]:
        try:
            stale.unlink()
        except OSError:
            pass


def _source_library_cache_entry(root: Path) -> Path | None:
    """Where this tree's parsed record projection is kept, or None.

    The key must cover every tree the projection is derived from, and that is
    all three roots `load_library` reads --- `src/sources` for the records and
    `src/gpt`/`src/claude` for the publication bindings --- not the sources
    alone. Keyed on the sources only, a binding added under a publication root
    left this serving the registry from before it, and a ledger row naming the
    new artifact was reported as "not registered": a stale answer that looked
    exactly like a real finding. It is the failure mode a cache has, and the
    reason a key is written as the inputs rather than as the interesting input.
    """
    if os.environ.get("TRIPTYCH_SOURCE_LIBRARY_CACHE") == "0":
        return None
    sources = root / "src" / "sources"
    if not sources.is_dir():
        return None
    roots = [sources, root / "src" / "gpt", root / "src" / "claude"]
    fingerprint, counted = tree_fingerprint([r for r in roots if r.is_dir()])
    if counted < SOURCE_LIBRARY_CACHE_FLOOR:
        return None
    return SOURCE_LIBRARY_CACHE_DIR / f"{fingerprint}.json"


def _source_library_records(
    calendar_root: Path,
) -> tuple[dict[str, dict[str, object]], list[str]]:
    """Load the registered source graph for a publication path.

    `mass-propers` is itself a publication path, so this loader cannot rely on
    `check-calendar-masses` having run earlier in another process. The source
    tool owns record parsing and graph validation; this module retains only the
    small metadata projection needed to decide whether a per-text witness is
    exact and whether its backing artifact has the claimed rights state.
    """
    root = calendar_root.resolve().parents[2]
    cached = _SOURCE_LIBRARY_CACHE.get(root)
    if cached is not None:
        records, problems = cached
        return records, list(problems)

    # The in-process cache above answers a second call in one process. It never
    # answers the first, and the first is what the suite pays: `tests/tools`
    # starts hundreds of cold tools, and each of them loaded and validated the
    # whole 19,000-file library from scratch to answer one question. So the
    # projection is also kept on disk, keyed by the tree's own fingerprint.
    entry = _source_library_cache_entry(root)
    if entry is not None:
        try:
            held = json.loads(entry.read_text(encoding="utf-8"))
            records = held["records"]
            problems = tuple(held["problems"])
            _SOURCE_LIBRARY_CACHE[root] = (records, problems)
            return records, list(problems)
        except (OSError, ValueError, KeyError, TypeError):
            pass

    try:
        # ``calendar_root`` is a data location selected by ``mass-propers
        # --root``.  It must never become an executable-code search path: an
        # otherwise ordinary fixture shaped like ``<root>/src/sources/calendars``
        # could place arbitrary Python at ``<root>/tools/source-library``.
        # Execute the source-library implementation from this module's own
        # checkout and pass the selected root only as data to ``load_library``.
        tool = (TRUSTED_REPOSITORY / "tools/source-library").resolve()
        if not tool.is_relative_to(TRUSTED_REPOSITORY) or not tool.is_file():
            raise ValueError("trusted source-library tool is unavailable")
        module_name = (
            "_proper_latin_source_library_"
            + sha256(str(tool).encode("utf-8")).hexdigest()[:12]
        )
        loader = SourceFileLoader(module_name, str(tool))
        spec = spec_from_loader(loader.name, loader)
        if spec is None:  # pragma: no cover - a broken checkout
            raise ValueError(f"cannot load {tool}")
        module = module_from_spec(spec)
        sys.modules[spec.name] = module
        loader.exec_module(module)
        library = module.load_library(root, check_binding_fingerprints=False)
        problems = tuple(
            f"source library prevents Latin publication: {problem}"
            for problem in library.errors
        )
        records = {
            record_id: {
                **dict(record.data),
                "record_type": record.record_type,
                "id": record.record_id,
            }
            for record_id, record in library.records.items()
        }
    except Exception as error:  # the source tool is a sibling script, not an API
        records = {}
        problems = (f"cannot validate Latin provenance source records: {error}",)
    if entry is not None:
        # Written only when JSON carries it back unchanged, and compared rather
        # than assumed: TOML has native dates and JSON has not, and a record
        # that came back as a string where a date went in would be a source
        # verdict that resolved successfully and wrongly.
        try:
            held = {"records": records, "problems": list(problems)}
            encoded = json.dumps(held)
            if json.loads(encoded) == held:
                entry.parent.mkdir(parents=True, exist_ok=True)
                aside = entry.with_suffix(f".{os.getpid()}.tmp")
                aside.write_text(encoded, encoding="utf-8")
                os.replace(aside, entry)
                _prune_source_library_cache(entry.parent, keep=2)
        except (OSError, TypeError, ValueError, RecursionError):
            pass

    _SOURCE_LIBRARY_CACHE[root] = (records, problems)
    return records, list(problems)


def _backing_artifact(
    source_id: str,
    sources: Mapping[str, Mapping[str, object]],
) -> Mapping[str, object] | None:
    """Return the physical artifact behind an exact witness record."""
    record = sources.get(source_id)
    if record is None:
        return None
    record_type = record.get("record_type")
    if record_type == "artifact":
        return record
    artifact_id = record.get("artifact_id")
    if record_type == "passage" and not artifact_id:
        segment = sources.get(str(record.get("segment_id") or ""))
        if segment is not None and segment.get("record_type") == "segment":
            artifact_id = segment.get("artifact_id")
    artifact = sources.get(str(artifact_id or ""))
    return artifact if artifact is not None and artifact.get("record_type") == "artifact" else None


def _source_record_problems(
    where: str,
    row: Mapping[str, object],
    sources: Mapping[str, Mapping[str, object]],
) -> list[str]:
    """Validate witness identity and rights against source-library metadata."""
    problems: list[str] = []
    for field in ("source_id", "verification_source_id"):
        source_id = str(row.get(field) or "")
        if not source_id:
            continue
        record = sources.get(source_id)
        if record is None:
            problems.append(f"{where}: {field} {source_id!r} is not registered")
        elif record.get("record_type") not in EXACT_WITNESS_TYPES:
            problems.append(
                f"{where}: {field} {source_id!r} must name an exact artifact, "
                "segment, or passage witness"
            )
        elif _backing_artifact(source_id, sources) is None:
            problems.append(
                f"{where}: {field} {source_id!r} has no validated backing artifact"
            )
    rights_source_ids = row.get("publication_source_ids") or []
    for source_id in rights_source_ids:
        if source_id not in sources:
            problems.append(
                f"{where}: publication_source_id {source_id!r} is not registered"
            )

    if row.get("publication_status") != "permitted":
        return problems
    basis = row.get("publication_basis")
    rights = {
        str(artifact.get("rights_status") or "")
        for source_id in rights_source_ids
        if (artifact := _backing_artifact(str(source_id), sources)) is not None
    }
    if basis == "public-domain" and "public-domain" not in rights:
        problems.append(
            f"{where}: public-domain publication requires an independent registered "
            "public-domain artifact in publication_source_ids"
        )
    elif basis in {"permission", "licensed"} and basis not in rights:
        problems.append(
            f"{where}: {basis} publication requires a publication_source_ids artifact "
            f"with rights_status {basis!r}"
        )
    return problems


def publication_records(
    calendar_root: Path,
    calendar: str,
    inventory_root: Path | None = None,
    *,
    registered_sources: Mapping[str, Mapping[str, object]] | None = None,
) -> tuple[dict[LatinKey, dict], list[str]]:
    """Validated records effective for a calendar, its recension base first."""
    inventory_root = inventory_root or calendar_root.parent / "inventories"
    records: dict[LatinKey, dict] = {}
    problems: list[str] = []
    seen: set[str] = set()

    def add(name: str) -> None:
        if name in seen:
            problems.append(f"Latin provenance recension cycle at {name!r}")
            return
        seen.add(name)
        try:
            document = _calendars.load_document(calendar_root, name, effective=False)
        except Exception as error:
            problems.append(f"{name}: cannot resolve Latin provenance base: {error}")
            return
        base = document.get(_calendars.RECENSION_BASE)
        if isinstance(base, str) and base and base != name:
            add(base)
            # `text_from` establishes repository residence, not that the target
            # recension printed the same words. Keep the base witness as
            # provenance, but remove its permission until THIS recension has a
            # per-text attestation/decision of its own. Otherwise a future
            # public-domain 1962 collation would silently publish under a
            # pre-1955 heading whose coverage file says inherited-uncollated.
            for key, inherited in list(records.items()):
                records[key] = {
                    **inherited,
                    "publication_status": "unresolved",
                    "publication_basis": "unresolved",
                    "surfaces": [],
                    "note": (
                        f"Provenance inherited from {base}; target-recension "
                        f"attestation for {name} is not established."
                    ),
                }
        path = sidecar_path(inventory_root, name)
        if not path.is_file():
            problems.append(f"{path}: missing Latin provenance sidecar")
            return
        found, trouble = read_sidecar(path)
        problems.extend(trouble)
        if trouble:
            # One malformed row or a false file identity taints the ledger as a
            # whole.  A projection must never publish the remaining rows on the
            # assumption that the error was unrelated to them.
            records.clear()
        else:
            records.update(found)

    add(calendar)
    if registered_sources is None:
        registered_sources, source_problems = _source_library_records(calendar_root)
        problems.extend(source_problems)
    if not problems:
        for key, row in records.items():
            problems.extend(_source_record_problems(key.label(), row, registered_sources))
    if problems:
        # Callers deliberately need not inspect the diagnostics to remain safe:
        # an invalid or unavailable source graph publishes no Latin wording.
        records.clear()
    return records, problems


def sidecar_problems(
    calendar_paths: Iterable[Path],
    *,
    inventory_root: Path,
    required: bool,
    registered_source_ids: set[str] | None = None,
) -> list[str]:
    """Validate exact, bidirectional coverage of direct calendar text owners."""
    problems: list[str] = []
    for calendar_path in calendar_paths:
        calendar = calendar_path.parent.name
        path = sidecar_path(inventory_root, calendar)
        if not path.is_file():
            if required:
                problems.append(f"{path}: missing Latin provenance sidecar")
            continue
        records, trouble = read_sidecar(path)
        problems.extend(trouble)
        if registered_source_ids is not None:
            for key, row in records.items():
                for field in ("source_id", "verification_source_id"):
                    source_id = row.get(field)
                    if source_id and source_id not in registered_source_ids:
                        problems.append(
                            f"{path}: {key.label()} {field} {source_id!r} is not "
                            "registered in the source library"
                        )
        try:
            document = _calendars.read_yaml(calendar_path) or {}
        except Exception as error:
            problems.append(f"{calendar_path}: cannot check Latin provenance: {error}")
            continue
        expected = {
            key: (text, status) for key, text, status in body_owners(document)
        }
        for key, (text, status) in expected.items():
            row = records.get(key)
            if row is None:
                problems.append(f"{path}: missing entry for {key.label()}")
            elif status == REMOVED_BODY_STATUS and row.get("body_status") != status:
                problems.append(
                    f"{path}: {key.label()} is a removed proper body but its "
                    "sidecar row is not marked body_status='removed'"
                )
            elif status == "present" and row.get("body_status") == REMOVED_BODY_STATUS:
                problems.append(
                    f"{path}: {key.label()} retains text but its sidecar row says "
                    "body_status='removed'"
                )
            elif isinstance(text, str) and row.get("text_sha256") != text_sha256(text):
                problems.append(f"{path}: stale text hash for {key.label()}")
        for key in sorted(set(records) - set(expected)):
            problems.append(f"{path}: orphan entry for {key.label()}")
    return problems


def sanitize_proper(
    proper: Mapping[str, object],
    base_key: LatinKey,
    records: Mapping[LatinKey, Mapping[str, object]],
    surfaces: Iterable[str],
) -> dict:
    """Copy one resolved proper with unpermitted Latin wording removed."""
    copied = copy.deepcopy(dict(proper))

    def sanitize(owner: dict, key: LatinKey) -> None:
        if _is_removed_body_owner(owner):
            # No retained hash, witness, reason source, or wording crosses the
            # public boundary.  `withheld` records only the public-safe cause
            # of this typed absence, allowing readers to distinguish it from a
            # corpus gap without learning private audit detail.
            owner["latin"] = {
                "target": str(copied.get("name") or "Proper"),
                "state": "unavailable",
                "held": False,
                "available": False,
                "withheld": True,
            }
            return
        text = owner.get("text")
        if not isinstance(text, str):
            return
        decision = decision_for(key, text, records)
        owner["latin"] = decision.projection(surfaces)
        if not decision.permits(surfaces):
            owner["text"] = None

    sanitize(copied, base_key)
    for course in ("cycles", "weekday_cycles"):
        branches = copied.get(course)
        if not isinstance(branches, dict):
            continue
        for cycle, owner in branches.items():
            if isinstance(owner, dict):
                sanitize(
                    owner,
                    LatinKey(base_key.mass, base_key.form, base_key.proper, course, str(cycle)),
                )
    return copied


def sanitize_mass(
    mass: Mapping[str, object],
    records: Mapping[LatinKey, Mapping[str, object]],
    surfaces: Iterable[str],
) -> dict:
    """Copy a source mass so JSON/YAML output cannot retain an unredacted twin."""
    copied = copy.deepcopy(dict(mass))
    mass_key = str(copied.get("key") or "")
    groups: list[tuple[str, object]] = [("", copied.get("propers"))]
    groups.extend(
        (str(form.get("name") or ""), form.get("propers"))
        for form in copied.get("forms") or []
        if isinstance(form, dict)
    )
    occurrences: dict[tuple[str, str, str], int] = {}
    for form, propers in groups:
        if not isinstance(propers, list):
            continue
        for index, proper in enumerate(propers):
            if not isinstance(proper, dict):
                continue
            bare = (mass_key, form, str(proper.get("name") or ""))
            if isinstance(proper.get("text"), str) or _is_removed_body_owner(proper):
                occurrences[bare] = occurrences.get(bare, 0) + 1
            propers[index] = sanitize_proper(
                proper,
                LatinKey(*bare, occurrence=occurrences.get(bare, 0)),
                records,
                surfaces,
            )
    return copied


def render_unresolved_sidecar(calendar: str, document: Mapping[str, object]) -> str:
    """Render a conservative initial ledger; placeholders are project status notes."""
    removed = [key.label() for key, _, status in body_owners(document) if status == REMOVED_BODY_STATUS]
    if removed:
        raise ValueError(
            "cannot reconstruct removed Latin body hashes while rendering a sidecar: "
            + ", ".join(removed)
        )
    def quoted(value: str) -> str:
        return json.dumps(value, ensure_ascii=False)

    lines = [
        f"schema = {quoted(SCHEMA)}",
        f"calendar = {quoted(calendar)}",
        'language = "la"',
        f"policy = {quoted(POLICY)}",
        'scope = "Each direct text node is hash-bound here. Defaults are '
        'deliberately unresolved; witness identity never supplies publication permission."',
        "",
        "[defaults]",
        'provenance_status = "unresolved"',
        'publication_status = "unresolved"',
        'publication_basis = "unresolved"',
        "surfaces = []",
    ]
    for key, text in sorted(text_owners(document)):
        lines.extend(["", "[[entries]]"])
        for field, value in key.as_dict().items():
            lines.append(
                f"{field} = {value}"
                if field == "occurrence"
                else f"{field} = {quoted(str(value))}"
            )
        lines.append(f'text_sha256 = "{text_sha256(text)}"')
        if key.proper == "Placeholder" or text.lstrip().startswith(
            "This entry is a placeholder"
        ):
            lines.extend(
                [
                    'provenance_status = "identified"',
                    'relationship = "project-authored"',
                    'transformations = []',
                    "provenance_evidence = "
                    + quoted(
                        str(Path("src/sources/calendars") / calendar / "propers.yaml")
                    ),
                    'provenance_authority = "Triptych repository status record"',
                    'provenance_confidence = "high"',
                    'publication_status = "permitted"',
                    'publication_basis = "project-created"',
                    'surfaces = ["web", "download", "print", "cli", "corpus-data", "public-git"]',
                    "publication_evidence = "
                    + quoted(
                        str(Path("src/sources/calendars") / calendar / "propers.yaml")
                    ),
                    'note = "Repository status notice, not a Latin liturgical text."',
                ]
            )
    return "\n".join(lines) + "\n"
