"""Exhaustive manifest and passage accounting, without inventing Scripture edges.

The report is reproducible metadata, never a source admission or an `indexed`
evidence state. Every source manifest is counted, including broken records.
Only existing typed fragment edges contribute to biblical coverage; an absent
edge establishes neither a commentary gap nor absence of biblical relevance.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import tomllib
from typing import Any
import yaml

import _catena
import _catena_scope

SCHEMA = "triptych-catena-held-corpus-audit/v1"
REVIEW_PATH = Path("src/sources/commentary/held-passage-review.yaml")
REVIEW_SCHEMA = "triptych-catena-held-passage-review/v1"
DISPOSITIONS = {
    "direct-commentary", "no-scripture-commentary", "incidental-citation",
    "needs-admission", "deferred-multiple-loci",
    "redundant-container", "needs-boundary-review",
}
KINDS = ("work", "edition", "artifact", "segment", "passage")


def inventory(root: Path) -> tuple[list[dict], dict[str, dict], list[str]]:
    """Retain one row per physical manifest even when its identity is unusable."""
    rows, records, errors = [], {}, []
    for path in sorted((root / "src/sources/works").rglob("*.toml")):
        relative = path.relative_to(root).as_posix()
        row: dict[str, Any] = {"path": relative}
        rows.append(row)
        try:
            raw = path.read_bytes()
            row["sha256"] = hashlib.sha256(raw).hexdigest()
            data = tomllib.loads(raw.decode("utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
            row["error"] = f"unreadable manifest: {type(error).__name__}"
            errors.append(f"{relative}: {row['error']}")
            continue
        identifier, kind = data.get("id"), data.get("record_type")
        row.update(id=identifier, record_type=kind)
        if not isinstance(identifier, str) or not identifier or not isinstance(kind, str) or kind not in KINDS:
            row["error"] = "missing identity or unsupported record type"
        elif identifier in records:
            row["error"] = f"duplicate identity {identifier}"
        elif any(key in data and not isinstance(data[key], str) for key in (
            "work_id", "edition_id", "artifact_id", "segment_id", "text", "language",
            "responsible", "title", "work_type", "rights_status", "rights_basis", "license")):
            row["error"] = "record has a nontextual identity, text or descriptive field"
        elif "states" in data and (not isinstance(data["states"], list)
                                     or any(not isinstance(value, str) for value in data["states"])):
            row["error"] = "states must be a list of strings"
        if "error" not in row:
            records[identifier] = data
        if "error" in row:
            errors.append(f"{relative}: {row['error']}")
        for key in ("work_id", "edition_id", "artifact_id", "segment_id", "language",
                    "storage", "media_type", "rights_status"):
            if key in data:
                row[key] = data[key]
    if not rows:
        errors.append("source manifest inventory is empty")
    return rows, records, errors


def _reviews(root: Path, manifests: dict, errors: list[str]) -> dict[str, dict]:
    path = root / REVIEW_PATH
    if not path.is_file():
        return {}
    try:
        document = _catena._load_yaml(path)
    except (OSError, ValueError, yaml.YAMLError, _catena.CatenaError) as error:
        errors.append(f"{REVIEW_PATH}: cannot read reviews: {error}")
        return {}
    if not isinstance(document, dict) or document.get("schema") != REVIEW_SCHEMA:
        errors.append(f"{REVIEW_PATH}: invalid review schema")
        return {}
    reviews: dict[str, dict] = {}
    rows = document.get("reviews")
    if not isinstance(rows, list):
        errors.append(f"{REVIEW_PATH}: reviews must be a list")
        return {}
    for ordinal, row in enumerate(rows, 1):
        label = f"{REVIEW_PATH}: reviews[{ordinal}]"
        prior_errors = len(errors)
        if not isinstance(row, dict):
            errors.append(f"{label}: expected mapping")
            continue
        if set(row) != {"passage_id", "passage_sha256", "disposition", "basis"}:
            errors.append(f"{label}: needs exactly passage_id, passage_sha256, disposition, basis")
        identifier = row.get("passage_id")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{label}: passage_id must be a nonempty string")
            continue
        manifest = manifests.get(identifier) or {}
        if identifier in reviews:
            errors.append(f"{label}: duplicate passage {identifier}")
        if manifest.get("record_type") != "passage":
            errors.append(f"{label}: unknown passage {identifier}")
        if row.get("passage_sha256") != manifest.get("sha256"):
            errors.append(f"{label}: stale passage review {identifier}")
        if (not isinstance(row.get("disposition"), str) or row["disposition"] not in DISPOSITIONS
                or not isinstance(row.get("basis"), str) or not row["basis"].strip()):
            errors.append(f"{label}: unsupported disposition or empty basis")
        if isinstance(identifier, str) and len(errors) == prior_errors:
            reviews[identifier] = row
    return reviews


def report(root: Path = _catena.ROOT) -> dict[str, Any]:
    root = root.resolve()
    manifests, records, errors = inventory(root)
    by_id = {row["id"]: row for row in manifests if "id" in row and "error" not in row}
    kinds = {kind: {key: data for key, data in records.items()
                    if data.get("record_type") == kind} for kind in KINDS}
    sources = _catena.Sources(*(kinds[kind] for kind in KINDS))
    scope = _catena_scope.Scope(root, works=kinds["work"])
    errors.extend(scope.errors)
    reviews = _reviews(root, by_id, errors)
    try:
        edges = _catena.load_edges(root)
    except (OSError, ValueError, yaml.YAMLError, _catena.CatenaError) as error:
        errors.append(f"{_catena.EDGES_RELATIVE}: {error}")
        edges = {}
    # Preserve full manifest accounting even when the authored edge cannot be
    # traversed. Such a report is invalid, never a clean zero-fragment result.
    for field in ("fragments", "blocked", "parallels"):
        rows = edges.get(field) or []
        def usable(row):
            if not isinstance(row, dict):
                return False
            if field == "parallels":
                return (isinstance(row.get("hung"), str)
                        and isinstance(row.get("passage_ids"), list)
                        and all(isinstance(value, str) for value in row["passage_ids"]))
            if not isinstance(row.get("passage_id"), str):
                return False
            return field != "fragments" or (isinstance(row.get("work_id"), str)
                                             and _catena._extent(row.get("extent")) is not None)
        if not isinstance(rows, list) or any(not usable(row) for row in rows):
            errors.append(f"{_catena.EDGES_RELATIVE}: malformed {field} list")
            edges[field] = []
    fragments = edges.get("fragments") or []
    mapped = {row["passage_id"]: row for row in fragments}
    blocked = {row["passage_id"]: row for row in edges.get("blocked") or []}
    parallels = {identifier: row["hung"] for row in edges.get("parallels") or []
                 for identifier in row["passage_ids"] if identifier != row["hung"]}
    # The ordinary gate, rather than a weaker local reconstruction, owns edge
    # admission. Report all errors and preserve the inventory on failure.
    try:
        errors.extend(_catena.validate(root))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, yaml.YAMLError, _catena.CatenaError) as error:
        errors.append(f"fragment validation could not complete: {type(error).__name__}: {error}")
    for row in manifests:
        if row.get("record_type") == "work" and "error" not in row:
            row["commentator_scope"] = scope.work_decision(row["id"])

    passages = []
    for identifier, passage in sorted(kinds["passage"].items()):
        edge = mapped.get(identifier)
        edition_id = passage.get("edition_id")
        if passage.get("segment_id"):
            edition_id = (kinds["segment"].get(passage["segment_id"]) or {}).get("edition_id", edition_id)
        edition = kinds["edition"].get(edition_id) or {}
        owner_id = edition.get("work_id", "")
        work_id = edge["work_id"] if edge else owner_id
        work = kinds["work"].get(work_id) or {}
        controller = _catena.controlling_artifact(sources, passage) or {}
        decision = scope.work_decision(work_id)
        state = "indexed" if edge else "blocked" if identifier in blocked else (
            "parallel" if identifier in parallels else "unindexed")
        if edge and not decision["eligible"]:
            state = "excluded" if decision["status"] == "excluded" else "scope-unreviewed"
        review = reviews.get(identifier)
        if (review and review.get("disposition") == "direct-commentary"
                and decision["eligible"] and not edge and state != "parallel"):
            errors.append(f"{identifier}: reviewed direct commentary has no canonical fragment edge; restore the edge or record its specific unresolved admission gates")
        if (state == "unindexed" and decision["eligible"] and not review
                and str(passage.get("text") or "").strip()
                and any(stage in (passage.get("states") or []) for stage in ("inspected", "verified"))):
            errors.append(f"{identifier}: eligible inspected text has neither a fragment edge nor a reviewed Scripture applicability disposition")
        gates = []
        if not edge and state == "unindexed":
            gates.append("no-canonical-scripture-edge")
        if not str(passage.get("text") or "").strip():
            gates.append("no-explicit-text")
        if not any(stage in (passage.get("states") or []) for stage in ("inspected", "verified")):
            gates.append("inspection-not-recorded")
        if not controller:
            gates.append("no-resolved-controller")
        elif not (controller.get("rights_status") in _catena.PUBLISHABLE_RIGHTS or (
            controller.get("rights_status") == "licensed" and
            controller.get("license") in _catena.REDISTRIBUTABLE_LICENSES)):
            gates.append("publication-rights-not-established")
        if not decision["eligible"]:
            gates.append("commentator-" + decision["status"])
        row = {
            "passage_id": identifier, "path": by_id[identifier]["path"],
            "sha256": by_id[identifier]["sha256"], "edition_id": edition_id,
            "owning_work_id": owner_id, "commentator_work_id": work_id if edge else None,
            "author": work.get("responsible", ""), "work": work.get("title", ""),
            "language": edition.get("language", ""), "index_state": state,
            "scripture_applicability": "direct-commentary" if edge else (
                review["disposition"] if review else "unestablished"),
            "commentator_scope": decision,
            "owner_is_container": any(word in str(work.get("work_type", ""))
                                      for word in ("anthology", "collection")),
            "recorded_states": passage.get("states") or [],
            "explicit_text_characters": len(str(passage.get("text") or "")),
            "controller_id": controller.get("id"), "storage": controller.get("storage"),
            "rights_status": controller.get("rights_status"),
            "gates": gates,
        }
        if edge:
            row["extent"] = edge["extent"]
        if review:
            row["review"] = review
        if identifier in parallels:
            row["parallel_hung"] = parallels[identifier]
        passages.append(row)

    # A union of canonical verse addresses, not a count of fragment lengths.
    # Read actual printed verse keys: a maximum verse number is not a census.
    books = []
    active = [row for row in passages if row["index_state"] == "indexed"]
    for book in _catena.canon(root):
        token = book["token"]
        selected = [row for row in active if row["extent"]["token"] == token]
        chapter_rows = []
        for chapter in range(1, book["last_chapter"] + 1):
            path = root / _catena.BIBLES_RELATIVE / _catena.CANONICAL_BIBLE / "chapters" / token / f"{chapter}.json"
            try:
                verses = sorted(int(key) for key in json.loads(path.read_text())["verses"])
            except (OSError, ValueError, KeyError) as error:
                errors.append(f"{path.relative_to(root)}: cannot enumerate verses ({type(error).__name__})")
                verses = []
            touched = [row for row in selected if row["extent"]["first_chapter"] <= chapter <= row["extent"]["last_chapter"]]
            covered = [verse for verse in verses if any(
                (r["extent"]["first_chapter"], r["extent"]["first_verse"]) <= (chapter, verse) <=
                (r["extent"]["last_chapter"], r["extent"]["last_verse"]) for r in touched)]
            chapter_rows.append({"chapter": chapter, "verses": len(verses),
                                 "verses_with_fragments": len(covered), "fragments": len(touched)})
        books.append({"token": token, "name": book["name"], "fragments": len(selected),
                      "languages": dict(sorted(Counter(row["language"] for row in selected).items())),
                      "chapters": chapter_rows})
    totals = {
        "manifests": len(manifests),
        "records_by_type": dict(sorted(Counter(row.get("record_type") if isinstance(row.get("record_type"), str)
                                               else "unreadable-or-malformed" for row in manifests).items())),
        "invalid_manifests": sum("error" in row for row in manifests),
        "passages": len(passages),
        "passages_by_index_state": dict(sorted(Counter(row["index_state"] for row in passages).items())),
        "passages_by_language": dict(sorted(Counter(row["language"] for row in passages).items())),
        "passages_by_applicability": dict(sorted(Counter(row["scripture_applicability"] for row in passages).items())),
        "books_with_fragments": sum(bool(book["fragments"]) for book in books),
        "chapters_with_fragments": sum(bool(chapter["fragments"]) for book in books for chapter in book["chapters"]),
        "verses_with_fragments": sum(chapter["verses_with_fragments"] for book in books for chapter in book["chapters"]),
    }
    lead_counts: Counter = Counter()
    for entry in _catena._commentary_index(root).get("passages") or []:
        for lead in entry.get("works") or []:
            lead_counts[scope.lead_decision(lead)["status"]] += 1
    totals["chapter_leads_by_scope"] = dict(sorted(lead_counts.items()))
    inputs = [_catena.EDGES_RELATIVE, _catena.ALIASES_RELATIVE, _catena.INDEX_RELATIVE,
              _catena.ABSENCES_RELATIVE, REVIEW_PATH,
              *(Path(path) for path in _catena_scope.INPUTS)]
    return {
        "schema": SCHEMA, "status": "invalid" if errors else "ok", "numbering": _catena._projection.CANONICAL,
        "basis": {
            "manifest_universe": "all *.toml recursively under src/sources/works",
            "edges": _catena.EDGES_RELATIVE.as_posix(),
            "scope": "All registrations and languages; biblical coverage counts only eligible typed fragments.",
            "unindexed_means": "No canonical fragment edge; biblical applicability is unestablished unless separately reviewed. This is not proof of a missing commentary or of no Scripture relevance.",
            "gates_mean": "Recorded impediments, not a complete admission checklist or a new verification event.",
            "container_scope": "For unmapped anthology passages, scope describes the owning registration, not an inferred constituent author.",
        },
        "inputs": [{"path": path.as_posix(), "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest()}
                   for path in inputs if (root / path).is_file()],
        "totals": totals, "errors": sorted(set(errors)), "manifests": manifests,
        "passages": passages, "books": books,
    }
