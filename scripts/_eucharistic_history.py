"""Coverage and evidence-bound text snapshots owned by tools/act-history.

Research discovery cannot create normative stations or text ancestry. Text
adapters remain responsible for exact source identity and publication decisions.
"""
from __future__ import annotations

from collections import Counter
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib
from urllib.parse import quote, urlsplit

SCHEMA = "triptych-eucharistic-history/v1"
CORPUS_SCHEMA = "triptych-eucharistic-corpus/v1"
COMPARISON_SCHEMA = "triptych-eucharistic-witness-comparison/v1"
NATIVE_TEXT_SCHEMA = "triptych-eucharistic-native-text/v1"
COMPARISON_KINDS = {"same-prayer-witness-comparison": "same-prayer-witnesses",
                    "parallel-liturgical-unit-comparison": "parallel-function-not-same-composition"}
RELATIONSHIP_SCHEMA = "eucharistic-history-relationships"
RELATIONSHIP_KINDS = {"borrowing": True, "reception": True, "shared-text": False,
                      "common-ancestry": False, "edition-succession": True}
MARKER = ".triptych-act-history-corpus.json"
DEFAULT_SOURCE = "src/sources/inventories/catholic-eucharistic-history-v1.toml"
SLUG = re.compile(r"[a-z0-9][a-z0-9-]*\Z")
TOOL_ROOT = Path(__file__).resolve().parents[1]
TEXT_SERIALIZATION = {"id": "act-history-ventilate/v1", "owner": "tools/act-history:ventilate",
                      "encoding": "UTF-8", "line_ending": "LF", "final_newline": True,
                      "source_hash_field": "text_sha256", "output_hash_field": "serialized_text_sha256"}


class HistoryError(ValueError):
    """An input or output boundary prevents a truthful projection."""


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, default=str) + "\n").encode()


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def inside(root: Path, value: str | Path) -> Path:
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise HistoryError(f"source path is outside repository: {value}")
    return path


def fingerprint(root: Path, path: Path) -> dict:
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise HistoryError(f"cannot read {path.relative_to(root)}: {error.strerror}") from error
    return {"path": path.relative_to(root).as_posix(), "sha256": digest(payload), "byte_size": len(payload)}


def read_toml(root: Path, path: Path, inputs: dict) -> dict:
    try:
        body = path.read_bytes()
    except OSError as error:
        raise HistoryError(f"cannot read {path.relative_to(root)}: {error.strerror}") from error
    record = {"path": path.relative_to(root).as_posix(), "sha256": digest(body), "byte_size": len(body)}
    inputs[record["path"]] = record
    try:
        return tomllib.loads(body.decode("utf-8"))
    except (UnicodeError, tomllib.TOMLDecodeError) as error:
        raise HistoryError(f"cannot parse {record['path']}: {error}") from error


def route(source: Path, root: Path) -> tuple[dict, dict]:
    root = root.resolve()
    inputs: dict[str, dict] = {}
    data = read_toml(root, inside(root, source), inputs)
    if data.get("schema_version") != 1 or data.get("record_type") != "catholic-eucharistic-history":
        raise HistoryError("expected schema_version=1, record_type=catholic-eucharistic-history")
    if not isinstance(data.get("scope_ref"), str) or not data["scope_ref"]:
        raise HistoryError("history routing requires scope_ref")
    for table in ("catalogues", "act_slices", "text_sets", "comparisons", "relationship_sets", "presentation_groups", "text_versions"):
        rows = data.get(table, [])
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise HistoryError(f"{table} must be an array of tables")
        identifiers = [row.get("id") for row in rows]
        if any(not isinstance(key, str) or not SLUG.fullmatch(key) for key in identifiers):
            raise HistoryError(f"{table} requires stable slug ids")
        if len(identifiers) != len(set(identifiers)):
            raise HistoryError(f"duplicate id in {table}")
        fields = {"text_sets": ("adapter",), "catalogues": ("path", "table"),
                  "act_slices": ("path",), "comparisons": ("kind",), "relationship_sets": ("path",),
                  "presentation_groups": ("label",), "text_versions": ("text_set",)}[table]
        for row in rows:
            for field in fields:
                if not isinstance(row.get(field), str) or not row[field]:
                    raise HistoryError(f"{table} {row['id']}: missing {field}")
    return data, inputs


def required_string(row: dict, key: str, context: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise HistoryError(f"{context}: {key} must be a nonempty string")
    return value


def comparison_identity(row: dict) -> str:
    kind = row.get("kind")
    if not isinstance(kind, str) or kind not in COMPARISON_KINDS:
        raise HistoryError("unsupported comparison kind")
    return COMPARISON_KINDS[kind]


def relationship_evidence(row: dict, sources: dict, identifier: str, *, inspected: bool) -> list[dict]:
    evidence = row.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        raise HistoryError(f"{identifier}: evidence must name sources and loci")
    result, seen = [], set()
    for citation in evidence:
        if not isinstance(citation, dict) or set(citation) != {"source_id", "locus"}:
            raise HistoryError(f"{identifier}: evidence requires source_id and locus only")
        source_id = required_string(citation, "source_id", identifier)
        locus = required_string(citation, "locus", identifier)
        if source_id not in sources:
            raise HistoryError(f"{identifier}: unresolved evidence source {source_id}")
        if (source_id, locus) in seen:
            raise HistoryError(f"{identifier}: duplicate evidence source and locus")
        seen.add((source_id, locus))
        if inspected and sources[source_id]["inspection_status"] != "inspected":
            raise HistoryError(f"{identifier}: sourced relationship or entity requires inspected evidence")
        result.append({**citation, "source": sources[source_id]})
    return result


def relationships(data: dict, root: Path, entries: dict, comparisons: dict, inputs: dict) -> tuple[list[dict], list[dict]]:
    """Evidence links are never passed to act parents or corpus inheritance."""
    result, entities, held = [], {}, []
    allowed = {"id", "kind", "label", "from", "to", "certainty", "scope", "basis", "limitations",
               "evidence", "comparison_ids", "date_label", "chronology", "ancestor_ref",
               "git_ancestry", "text_inheritance"}
    for owner in data.get("relationship_sets", []):
        path = inside(root, owner["path"])
        inventory = read_toml(root, path, inputs)
        if inventory.get("schema_version") != 1 or inventory.get("record_type") != RELATIONSHIP_SCHEMA:
            raise HistoryError(f"{owner['id']}: expected schema_version=1, record_type={RELATIONSHIP_SCHEMA}")
        sources = {}
        source_rows = inventory.get("sources", [])
        if not isinstance(source_rows, list):
            raise HistoryError(f"{owner['id']}: sources must be an array of tables")
        for source in source_rows:
            if not isinstance(source, dict):
                raise HistoryError(f"{owner['id']}: source must be a table")
            key = required_string(source, "id", owner["id"])
            if key in sources:
                raise HistoryError(f"{owner['id']}: duplicate relationship source {key}")
            for field in ("title", "inspection"):
                required_string(source, field, key)
            if source.get("inspection_status") not in ("inspected", "not-inspected"):
                raise HistoryError(f"{key}: source requires explicit inspection_status")
            if "url" in source and safe_url(source["url"]) is None:
                raise HistoryError(f"{key}: source URL must be an HTTP(S) source route")
            sources[key] = {**source, "url": source.get("url")}
        entity_rows = inventory.get("entities", [])
        if not isinstance(entity_rows, list) or any(not isinstance(row, dict) for row in entity_rows):
            raise HistoryError(f"{owner['id']}: entities must be an array of tables")
        for row in entity_rows:
            key = required_string(row, "id", owner["id"])
            identifier = owner["id"] + ":entity:" + key
            if not SLUG.fullmatch(key) or identifier in entities or identifier in entries:
                raise HistoryError(f"{owner['id']}: duplicate or unsafe entity id {key}")
            fields = {"id", "label", "kind", "family", "scope", "basis", "limitations", "evidence"}
            if set(row) - fields or row.get("kind") != "textual-tradition":
                raise HistoryError(f"{identifier}: entity is an undated textual-tradition, not an edition or act")
            for field in ("label", "family", "scope", "basis", "limitations"):
                required_string(row, field, identifier)
            entities[identifier] = {**row, "id": identifier, "chronology": None, "relationship_ids": [],
                                    "evidence": relationship_evidence(row, sources, identifier, inspected=True),
                                    "origin": {"inventory": path.relative_to(root).as_posix(), "table": "entities", "id": key}}
        held.append((owner, path, inventory, sources))
    endpoints = entries.keys() | entities.keys()
    for owner, path, inventory, sources in held:
        rows = inventory.get("relationships")
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise HistoryError(f"{owner['id']}: relationships must be an array of tables")
        seen = set()
        for row in rows:
            key = required_string(row, "id", owner["id"])
            if not SLUG.fullmatch(key) or key in seen:
                raise HistoryError(f"{owner['id']}: duplicate or unsafe relationship id {key}")
            seen.add(key)
            identifier = owner["id"] + ":" + key
            if set(row) - allowed:
                raise HistoryError(f"{identifier}: unsupported relationship fields: {', '.join(sorted(set(row) - allowed))}")
            for field in ("git_ancestry", "text_inheritance"):
                if field in row and row[field] is not False:
                    raise HistoryError(f"{identifier}: relationships cannot grant {field}")
            kind = row.get("kind")
            if not isinstance(kind, str) or kind not in RELATIONSHIP_KINDS:
                raise HistoryError(f"{identifier}: unsupported relationship kind")
            for field in ("from", "to"):
                endpoint = required_string(row, field, identifier)
                if endpoint not in endpoints:
                    raise HistoryError(f"{identifier}: unresolved {field} endpoint {endpoint}")
            if row["from"] == row["to"]:
                raise HistoryError(f"{identifier}: relationship endpoints must be distinct")
            if row.get("certainty") not in ("sourced", "attributed", "disputed", "unresolved"):
                raise HistoryError(f"{identifier}: unsupported relationship certainty")
            for field in ("scope", "basis", "limitations"):
                required_string(row, field, identifier)
            for field in ("label", "date_label"):
                if field in row:
                    required_string(row, field, identifier)
            ancestor = row.get("ancestor_ref")
            if ancestor is not None and (kind != "common-ancestry" or not isinstance(ancestor, str)
                                         or ancestor not in endpoints or ancestor in (row["from"], row["to"])):
                raise HistoryError(f"{identifier}: ancestor_ref must identify a separate recorded common ancestor")
            projected_evidence = relationship_evidence(row, sources, identifier, inspected=row["certainty"] == "sourced")
            comparison_ids = row.get("comparison_ids", [])
            if (not isinstance(comparison_ids, list) or any(not isinstance(item, str) for item in comparison_ids)
                    or len(comparison_ids) != len(set(comparison_ids))):
                raise HistoryError(f"{identifier}: comparison_ids must be distinct comparison IDs")
            comparison_links = []
            for comparison_id in comparison_ids:
                if comparison_id not in comparisons:
                    raise HistoryError(f"{identifier}: unresolved comparison {comparison_id}")
                comparison = comparisons[comparison_id]
                linked = {comparison.get(side, {}).get("record_id") for side in ("left", "right")}
                if linked != {row["from"], row["to"]}:
                    raise HistoryError(f"{identifier}: comparison record_id endpoints do not match relationship")
                comparison_links.append({"id": comparison_id, "projection_path": comparison["projection_path"]})
            result.append({**row, "id": identifier, "label": row.get("label", kind),
                           "directed": RELATIONSHIP_KINDS[kind], "date_label": row.get("date_label"),
                           "chronology": chronology(row), "ancestor_ref": ancestor,
                           "evidence": projected_evidence, "comparison_ids": comparison_ids,
                           "comparison_links": comparison_links,
                           "origin": {"inventory": path.relative_to(root).as_posix(), "table": "relationships", "id": key},
                           "git_ancestry": False, "text_inheritance": False})
    return sorted(result, key=lambda row: row["id"]), sorted(entities.values(), key=lambda row: row["id"])


def presentation_groups(data: dict, entries: list[dict], entities: list[dict]) -> list[dict]:
    """Source-owned labels group aliases without changing historical identity."""
    aliases, groups = {}, {}
    for row in data.get("presentation_groups", []):
        identifier = row["id"]
        label = required_string(row, "label", identifier)
        if "note" in row:
            required_string(row, "note", identifier)
        families = row.get("families")
        if (not isinstance(families, list) or not families
                or any(not isinstance(key, str) or not key.strip() for key in families)
                or len(families) != len(set(families))):
            raise HistoryError(f"{identifier}: families must be distinct nonempty aliases")
        for family in families:
            if family in aliases:
                raise HistoryError(f"{identifier}: family alias {family!r} belongs to two presentation groups")
            aliases[family] = identifier
        groups[identifier] = {"id": identifier, "label": label, "status": "declared",
                              "families": families, "note": row.get("note"), "count": 0, "entity_count": 0}
    for entry in [*entries, *entities]:
        family = entry["family"]
        if not isinstance(family, str) or not family.strip():
            raise HistoryError(f"{entry['id']}: family must be a nonempty string")
        identifier = aliases.get(family, "unmapped:" + family)
        if identifier not in groups:
            groups[identifier] = {"id": identifier, "label": family + " (unmapped)", "status": "unmapped",
                                  "families": [family], "note": "No presentation group has been declared for this source family.",
                                  "count": 0, "entity_count": 0}
        group = groups[identifier]
        group["entity_count" if entry.get("kind") == "textual-tradition" else "count"] += 1
        entry["presentation_group"] = {key: group[key] for key in ("id", "label", "status")}
    return sorted(groups.values(), key=lambda row: row["id"])


def safe_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    return value if parsed.scheme in ("https", "http") and parsed.netloc else None


def evidence_sources(row: dict, source_rows: dict) -> list[dict]:
    named = row.get("source_ids", row.get("sources", []))
    if not isinstance(named, list):
        named = []
    result = []
    for key in named:
        if not isinstance(key, str) or key not in source_rows:
            raise HistoryError(f"{row.get('id')}: unresolved source reference {key!r}")
        source = source_rows[key]
        result.append({"id": key, "url": safe_url(source.get("url")),
                       "label": source.get("label", source.get("title", key)),
                       "inspection": source.get("inspection", "not stated")})
    return result


def chronology(row: dict) -> dict | None:
    """Only an explicit structured bound can position a research record."""
    value = row.get("chronology")
    bound_fields = ("start", "end", "kind", "certainty")
    if value is None and any("chronology_" + key in row for key in bound_fields):
        value = {key: row["chronology_" + key] for key in bound_fields if "chronology_" + key in row}
    if value is None:
        return None
    if not isinstance(value, dict) or not {"start", "end", "kind", "certainty"} <= value.keys():
        raise HistoryError(f"{row.get('id')}: chronology requires start, end, kind, certainty")
    if (not isinstance(value["start"], int) or isinstance(value["start"], bool)
            or not isinstance(value["end"], int) or isinstance(value["end"], bool)
            or value["start"] > value["end"]):
        raise HistoryError(f"{row.get('id')}: chronology bounds must be ordered integer years")
    for key in ("kind", "certainty"):
        required_string(value, key, str(row.get("id")))
    return {key: value[key] for key in ("start", "end", "kind", "certainty")}


def record_links(row: dict, sources: list[dict]) -> list[dict]:
    links = []
    for key in ("route", "book_route", "url"):
        url = safe_url(row.get(key))
        if url:
            links.append({"kind": "source-route", "label": "Book or source route", "url": url})
    for url in row.get("source_urls", []):
        if safe_url(url):
            links.append({"kind": "source-route", "label": "Source route", "url": url})
    for source in sources:
        if source["url"]:
            links.append({"kind": "evidence", "label": source["label"], "url": source["url"]})
    return list({link["url"]: link for link in links}.values())


def source_library_links(entries: list[dict], root: Path, inputs: dict) -> None:
    """Only an exact canonical edition can supply this same-site route."""
    library = None
    for entry in entries:
        row = entry["source_record"]
        if "source_library_edition_id" not in row:
            continue
        identifier = row["source_library_edition_id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"edition\.[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", identifier):
            raise HistoryError(f"{entry['id']}: invalid source-library edition id")
        if library is None:
            from _eucharistic_texts import _load_library, AdapterError
            try:
                library = _load_library(root)
            except AdapterError as error:
                raise HistoryError(f"source-library edition link: {error}") from error
        record = library.records.get(identifier)
        if record is None or record.record_type != "edition":
            raise HistoryError(f"{entry['id']}: unresolved source-library edition {identifier}")
        stamp = fingerprint(root, inside(root, record.path))
        inputs[stamp["path"]] = stamp
        entry["links"].append({"kind": "source-library-edition", "edition_id": identifier,
                               "label": "Open edition in the Source Library",
                               "url": "../sources/#edition=" + quote(identifier, safe="")})


def catalogue(source: Path, root: Path, *, act_loader) -> dict:
    root = root.resolve()
    data, inputs = route(source, root)
    entries = []
    for owner in data.get("catalogues", []):
        path = inside(root, owner["path"])
        research = read_toml(root, path, inputs)
        table = owner.get("table")
        rows = research.get(table)
        if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
            raise HistoryError(f"{owner['id']}: missing record table {table!r}")
        source_rows = {row["id"]: row for row in research.get("sources", [])}
        seen = set()
        for row in rows:
            key = row.get("id")
            if not isinstance(key, str) or not key or key in seen:
                raise HistoryError(f"{owner['id']}: missing or duplicate record id {key!r}")
            seen.add(key)
            sources = evidence_sources(row, source_rows)
            entries.append({
                "id": owner["id"] + ":" + key,
                "origin": {"inventory": path.relative_to(root).as_posix(), "table": table, "id": key},
                "family": row.get("family", owner.get("family", "unclassified")),
                "title": row.get("title", row.get("book_label", key)),
                "date_label": str(row.get("date", "unknown")), "chronology": chronology(row),
                "record_kind": row.get("kind", "research-record"),
                "evidence_status": "candidate", "text_status": row.get("transcription_status", row.get("text_acquisition", "not-acquired")),
                "acquisition_status": row.get("acquisition_status", "unestablished"),
                "collation_status": row.get("collation_status", "unestablished"),
                "substantive_status": "unestablished", "sources": sources,
                "source_record": row, "links": record_links(row, sources), "act_ref": None,
            })
    for owner in data.get("act_slices", []):
        path = inside(root, owner["path"])
        acts = act_loader(path)
        for input_path in acts.get("source_files", [str(path)]):
            held = inside(root, input_path)
            record = fingerprint(root, held)
            inputs[record["path"]] = record
        for row in acts.get("acts", []):
            # The historical act date already has a checked precision. It is
            # not extracted from a research title or a free-form date label.
            date = str(row.get("date", "unknown"))
            year = int(date[:4]) if re.fullmatch(r"[0-9]{4}(?:-[0-9]{2}){0,2}", date) else None
            printed = row.get("station_kind") == "printed"
            entries.append({
                "id": owner["id"] + ":" + row["id"],
                "origin": {"inventory": path.relative_to(root).as_posix(), "table": "acts", "id": row["id"]},
                "family": row.get("line", "unclassified"), "title": row["title"],
                "date_label": date,
                "chronology": {"start": year, "end": year, "kind": "recorded-event", "certainty": row.get("date_precision", "recorded")} if year is not None else None,
                "record_kind": "printed-witness" if printed else "normative-act",
                "evidence_status": "recorded-station", "text_status": "unassessed-for-catalogue",
                "acquisition_status": "unassessed-for-catalogue", "collation_status": "unassessed-for-catalogue",
                "substantive_status": "unestablished", "sources": [],
                "source_record": row, "links": [],
                "act_ref": {"slice": owner["id"], "station_id": row["id"]},
            })
    source_library_links(entries, root, inputs)
    classifications = data.get("classifications", [])
    by_id = {entry["id"]: entry for entry in entries}
    if len(by_id) != len(entries):
        raise HistoryError("catalogue namespaces produce duplicate record identities")
    for classification in classifications:
        key = classification.get("id")
        if key not in by_id or not classification.get("basis") or not classification.get("source_ref"):
            raise HistoryError("classification requires a known id, source_ref and evidence basis")
        status = classification.get("substantive_status")
        if status not in ("substantive-established", "same-state-witness", "unestablished"):
            raise HistoryError(f"{key}: unknown substantive classification")
        by_id[key]["substantive_status"] = status
        by_id[key]["classification"] = classification
    holdings = None
    if data.get("holdings_inventory"):
        path = inside(root, data["holdings_inventory"])
        held = read_toml(root, path, inputs)
        holdings = {"inventory": path.relative_to(root).as_posix(), "checked_on": held.get("checked_on"),
                    "artifacts": held.get("artifacts", []),
                    "status": "recorded-acquisition-audit-not-reverified"}
    text_sets = [{**row, "status": "configured-not-generated"} for row in data.get("text_sets", [])]
    comparisons = [{**row, "status": "configured-not-generated", "historical_ancestry_claimed": False,
                    "identity_claim": comparison_identity(row),
                    "projection_path": f"comparisons/{row['id']}.json", "relationship_ids": []}
                   for row in data.get("comparisons", [])]
    for comparison in comparisons:
        for side in ("left", "right"):
            declaration = comparison.get(side, {})
            if not isinstance(declaration, dict):
                raise HistoryError(f"{comparison['id']}: {side} must be a table")
            if "record_id" in declaration and (not isinstance(declaration["record_id"], str)
                                                or declaration["record_id"] not in by_id):
                raise HistoryError(f"{comparison['id']}: unresolved {side} record_id")
    comparisons_by_id = {row["id"]: row for row in comparisons}
    relations, entities = relationships(data, root, by_id, comparisons_by_id, inputs)
    endpoints = {**by_id, **{row["id"]: row for row in entities}}
    for entry in entries:
        entry["relationship_ids"] = []
    for relation in relations:
        for endpoint in (relation["from"], relation["to"]):
            endpoints[endpoint]["relationship_ids"].append(relation["id"])
        for comparison_id in relation["comparison_ids"]:
            comparisons_by_id[comparison_id]["relationship_ids"].append(relation["id"])
    groups = presentation_groups(data, entries, entities)
    from _eucharistic_stages import load as load_stages, StageError
    try:
        stage_history = load_stages(root, catalogue_ids=set(by_id), catalogue_records=by_id, comparisons=comparisons_by_id,
                                    fingerprint=fingerprint,
                                    default_tradition_id=data.get("stage_history_default_tradition"))
    except StageError as error:
        raise HistoryError(f"stage history: {error}") from error
    for stamp in stage_history["inputs"]:
        inputs[stamp["path"]] = stamp
    native_texts = {}
    for stage in stage_history["stages"]:
        if "text_bindings" in stage:
            for projected in stage["text_projections"]:
                identifier = projected["text_binding"].removeprefix("native-book:")
                native_texts[identifier] = {"id": identifier, "adapter_id": projected["text_binding"],
                                          "projection_path": projected["text_projection_path"],
                                          "binding_sha256": projected["text_binding_sha256"]}
            continue
        if "text_binding" not in stage:
            continue
        # The stage loader has checked the binding, extent, rights and exact
        # catalogue witnesses. One constituent is stored once across stages.
        identifier = stage["text_binding"].removeprefix("native-book:")
        projection_path = f"native-texts/{identifier}.json"
        binding_hash = inputs[f"src/sources/inventories/eucharistic-books/{identifier}.json"]["sha256"]
        stage["text_projection_path"] = projection_path
        stage["text_binding_sha256"] = binding_hash
        native_texts[identifier] = {"id": identifier, "adapter_id": stage["text_binding"],
                                    "projection_path": projection_path, "binding_sha256": binding_hash}
    entries.sort(key=lambda row: row["id"])
    return {"schema": SCHEMA, "scope_ref": data["scope_ref"], "entries": entries,
            "counts": {"entries": len(entries), "substantive_established": sum(e["substantive_status"] == "substantive-established" for e in entries),
                       "witnesses": sum(e["record_kind"] in ("printed-witness", "manuscript-witness") for e in entries),
                       "candidates": sum(e["evidence_status"] == "candidate" for e in entries), "text_sets": len(text_sets),
                       "relationships": len(relations), "relationship_entities": len(entities), "presentation_groups": len(groups),
                       "unmapped_families": sum(group["status"] == "unmapped" for group in groups)},
            "text_sets": text_sets,
            "native_texts": [native_texts[key] for key in sorted(native_texts)],
            "comparisons": comparisons, "relationships": relations, "relationship_entities": entities, "presentation_groups": groups,
            "stage_history": stage_history,
            "holdings": holdings, "inputs": sorted(inputs.values(), key=lambda row: row["path"]),
            "limitations": ["Research records are candidates, not accepted normative stations or text ancestry.",
                            "Recorded printings and acts are not a census of proven substantive liturgical versions.",
                            "Unknown acquisition or unrecorded text is not historical absence.",
                            "Relationship types and their uncertainty do not grant Git ancestry or textual inheritance.",
                            "A missing research relationship is not evidence that traditions were historically unrelated.",
                            "Presentation groups label source-family aliases; their count is not a census of rites or Churches.",
                            "No complete-book claim or all-tradition completeness claim is made.",
                            "Legacy promulgated act chains retain recorded-unit inheritance; departure-effect status is not a text-continuity audit."]}


def native_text(adapter_id: str, root: Path) -> dict:
    """Project accepted native wording and its public citation, never raw OCR."""
    from _eucharistic_texts import load_adapter, AdapterError, NATIVE_BOOK_PREFIX
    identifier = adapter_id.removeprefix(NATIVE_BOOK_PREFIX)
    if not adapter_id.startswith(NATIVE_BOOK_PREFIX) or not SLUG.fullmatch(identifier):
        raise HistoryError("native text projection requires an exact native-book binding")
    try:
        payload = load_adapter(adapter_id, root)
    except AdapterError as error:
        raise HistoryError(f"native text projection: {error}") from error
    binding = payload["book_binding"]
    sources = {row["id"]: row for row in payload["sources"]}
    # This is a reading projection, not the source-library manifests. Only
    # public citation and normalization fields cross this boundary.
    source_fields = ("id", "record_type", "edition_id", "artifact_id", "title", "publication", "date", "authority",
                     "language", "source_url", "rights_status", "rights_basis",
                     "rights_jurisdiction", "transformation")
    cited = set()
    units = []
    for unit in payload["units"]:
        cited.update((unit["source_id"], unit["source_artifact_id"], unit["text_edition_id"]))
        language = unit["language"]
        units.append({key: unit[key] for key in
                      ("unit_id", "source_order", "native_path", "component", "kind", "language",
                       "text", "text_sha256", "witness_id", "witness_pages", "source_id",
                       "source_artifact_id", "text_edition_id", "publication")})
        units[-1].update(direction="rtl" if language.split("-")[0] in ("ar", "he", "syr", "arc") else "ltr",
                         source_locator=unit["provenance"]["source_locator"])
    for witness in binding["witnesses"]:
        cited.update((witness["edition_id"], witness["artifact_id"]))
    return {"schema": NATIVE_TEXT_SCHEMA, "id": identifier, "adapter_id": adapter_id,
            "title": payload["title"], "stage_ids": binding["stage_ids"],
            "catalogue_witness_ids": binding["catalogue_witness_ids"],
            "binding_sha256": binding["sha256"], "scope": payload["scope"], "counts": payload["counts"],
            "witnesses": [{key: witness[key] for key in ("id", "edition_id", "artifact_id", "scope_pages")}
                          for witness in binding["witnesses"]],
            "sources": [{key: sources[identifier][key] for key in source_fields if key in sources[identifier]}
                        for identifier in sorted(cited)],
            "units": units}


def write_catalogue(payload: dict, out: Path, *, check: bool = False) -> dict:
    wanted = json_bytes(payload)
    if check:
        if not out.is_file() or out.is_symlink() or out.read_bytes() != wanted:
            raise HistoryError(f"catalogue projection differs or is missing: {out}")
    else:
        if out.is_symlink():
            raise HistoryError("refusing a symlink catalogue output")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(wanted)
    return {"schema": SCHEMA, "counts": payload["counts"], "current" if check else "written": str(out)}


def verify_adapter(payload: dict, root: Path) -> None:
    """Defense in depth: an adapter result cannot bypass exact public-git checks."""
    units = payload.get("units")
    if not isinstance(units, list) or not units:
        raise HistoryError("adapter produced no accepted text units")
    if payload.get("book_binding") or payload.get("scope", {}).get("whole_book_complete"):
        from _eucharistic_texts import load_adapter, NATIVE_BOOK_PREFIX, AdapterError
        adapter = payload.get("adapter_id", "")
        if not adapter.startswith(NATIVE_BOOK_PREFIX):
            raise HistoryError("complete extent requires a validated native book adapter")
        try:
            canonical = load_adapter(adapter, root)
        except AdapterError as error:
            raise HistoryError(f"native book validation: {error}") from error
        if any(payload.get(key) != canonical.get(key) for key in ("units", "scope", "book_binding", "historical_date", "inputs")):
            raise HistoryError("native book adapter result differs from its checked source binding")
    seen = set()
    for unit in units:
        key = unit.get("unit_id")
        if (not isinstance(key, str) or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._-]*", key)
                or key in seen):
            raise HistoryError(f"duplicate or unsafe stable unit id: {key!r}")
        seen.add(key)
        text = unit.get("text")
        if not isinstance(text, str) or not text or digest(text.encode()) != unit.get("text_sha256"):
            raise HistoryError(f"{key}: missing text or exact text hash mismatch")
        permission = unit.get("publication", {})
        if (unit.get("withheld") or unit.get("reason") or permission.get("status") != "permitted"
                or "public-git" not in permission.get("surfaces", [])):
            raise HistoryError(f"{key}: publication to public-git is not permitted")
    if not payload.get("inputs"):
        raise HistoryError("adapter did not identify its source inputs")
    for expected in payload["inputs"]:
        found = fingerprint(root, inside(root, expected["path"]))
        if found["sha256"] != expected.get("sha256"):
            raise HistoryError(f"source hash mismatch: {expected['path']}")
    for expected in payload.get("tool_inputs", []):
        found = fingerprint(TOOL_ROOT, inside(TOOL_ROOT, expected["path"]))
        if found["sha256"] != expected.get("sha256"):
            raise HistoryError(f"trusted tool input hash mismatch: {expected['path']}")


def text_path(unit: dict) -> str:
    """Readable liturgical identities, not content hashes or source line numbers."""
    # '@' is escaped in actual values, so the empty marker cannot collide
    # with a genuine form/course/cycle named "default" or "@none".
    def component(value):
        if value in (None, ""):
            return "@none"
        encoded = quote(str(value), safe="-._")
        # URL quoting always leaves dots unescaped, but Git rejects these
        # complete path segments. Literal percent signs were already escaped,
        # so this representation cannot collide with a source value "%2E".
        if encoded in (".", "..") or encoded.lower() == ".git":
            encoded = encoded.replace(".", "%2E")
        return encoded
    identity = unit.get("identity", {})
    if unit.get("native_path"):
        from _eucharistic_texts import native_text_path
        return native_text_path(unit["native_path"])
    if {"mass", "form", "course", "cycle", "proper", "occurrence"} <= identity.keys():
        return (f"text/propers/{component(identity['mass'])}/form-{component(identity['form'])}/"
                f"course-{component(identity['course'])}/cycle-{component(identity['cycle'])}/"
                f"{component(identity['proper'])}--{component(identity['occurrence'])}.txt")
    if unit.get("division") and unit.get("element_key"):
        return f"text/ordinary/{component(unit['division'])}/{component(unit['element_key'])}.txt"
    raise HistoryError(f"{unit.get('unit_id')}: no supported semantic liturgical identity")


def serialized_text(text: str, identifier: str, *, ventilator) -> bytes:
    """Use the command's owning serializer; refuse any editorial alteration."""
    clauses = ventilator(text)
    if (not isinstance(clauses, list) or not clauses
            or any(not isinstance(clause, str) or not clause for clause in clauses)):
        raise HistoryError(f"{identifier}: clause serializer produced no valid text")
    serialized = "\n".join(clauses) + "\n"
    if serialized.split() != text.split():
        raise HistoryError(f"{identifier}: clause serializer changed non-whitespace content")
    return serialized.encode("utf-8")


def reconstruction_tree(payload: dict, identifier: str, inputs: dict, *, ventilator) -> dict[str, bytes]:
    units = payload["units"]
    complete = payload.get("scope", {}).get("whole_book_complete") is True
    if complete and not payload.get("book_binding"):
        raise HistoryError("complete book requires a validated native book binding")
    metadata = {key: value for key, value in payload.items() if key not in ("units", "inputs", "sources")}
    metadata.update({"schema": CORPUS_SCHEMA, "record_kind": "reconstruction", "id": identifier,
                     "text_ancestry": "isolated-root", "historical_act_claimed": False,
                     "text_serialization": TEXT_SERIALIZATION,
                     "git_timestamp": "fixed synthetic 2000-01-01T00:00:00Z; not a historical or review date"})
    implementation = {row["path"]: row for row in payload.get("tool_inputs", [])}
    for relative in ("scripts/_eucharistic_history.py", "tools/act-history"):
        implementation[relative] = fingerprint(TOOL_ROOT, TOOL_ROOT / relative)
    metadata["tool_inputs"] = sorted(implementation.values(), key=lambda row: row["path"])
    files = {"reconstruction.json": json_bytes(metadata), "inputs.json": json_bytes(sorted(inputs.values(), key=lambda row: row["path"])),
             "sources.json": json_bytes(payload.get("sources", [])),
             "coverage.json": json_bytes({"scope": payload.get("scope"), "counts": payload.get("counts"),
                                           "unknown_is_absence": False, "complete_book": complete,
                                           "omitted_body_owners": payload.get("omitted_body_owners", [])}),
             "order.json": json_bytes([{"unit_id": unit["unit_id"], "path": text_path(unit), "source_order": unit.get("source_order"),
                                         "division": unit.get("division"), "division_order": unit.get("division_order")}
                                        for unit in units])}
    for unit in units:
        path = text_path(unit)
        if path in files:
            raise HistoryError(f"duplicate semantic text path: {path}")
        files[path] = serialized_text(unit["text"], unit["unit_id"], ventilator=ventilator)
        provenance = {k: v for k, v in unit.items() if k != "text"}
        provenance.update({"serialized_text_sha256": digest(files[path]), "text_serialization": TEXT_SERIALIZATION})
        files["provenance/" + path.removeprefix("text/").removesuffix(".txt") + ".json"] = json_bytes(provenance)
    introduction = ("This is an independently collated complete native book within its explicit witness extent.\n"
                    "It is not a promulgation or a claim that all complementary service books are held.\n"
                    if complete else
                    "This is an isolated, bounded reconstruction from registered source owners.\n"
                    "It is not a promulgation, a complete missal, or an asserted historical revision.\n")
    files["README.md"] = (f"# {payload.get('title', identifier)}\n\n" + introduction +
        "The Git timestamp is a fixed synthetic value, not the target or extraction date.\n"
        f"Target date: {payload.get('target_date') or 'not established'}.\n"
        f"Witness date: {payload.get('witness_date') or 'not a single dated witness'}.\n"
        f"Whole reconstruction review date: {payload.get('reviewed_on') or 'not established; see per-source evidence'}.\n\n"
        "Read reconstruction.json, coverage.json, sources.json and each provenance record\n"
        "before interpreting the clause-line text files. Serialization reuses the act\n"
        "history's mechanical ventilate function and changes only whitespace. Provenance\n"
        "retains the exact source-body hash separately from the serialized text hash.\n"
        "Unknown acquisition or omitted coverage\n"
        "does not mean a prayer was historically absent. These branches claim no text\n"
        "inheritance from one another or from the separate normative act graph.\n").encode()
    for name in files:
        parts = name.split("/")
        if any("/".join(parts[:length]) in files for length in range(1, len(parts))):
            raise HistoryError(f"semantic file/directory collision: {name}")
    return files


def git(repo: Path, *args: str, input: bytes | None = None) -> bytes:
    env = {**{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "LC_ALL": "C", "TZ": "UTC"}
    done = subprocess.run(["git", "-C", str(repo), *args], input=input, capture_output=True, env=env)
    if done.returncode:
        raise HistoryError("git " + args[0] + ": " + done.stderr.decode(errors="replace").strip())
    return done.stdout


def _owned_output(out: Path) -> None:
    if out.is_symlink():
        raise HistoryError("refusing symlink corpus output")
    if not out.exists():
        return
    try:
        marker = out / MARKER
        held = json.loads(marker.read_text()) if not marker.is_symlink() else {}
    except (OSError, ValueError):
        held = {}
    if held.get("schema") != CORPUS_SCHEMA or held.get("owner") != "tools/act-history corpus":
        raise HistoryError("refusing to replace an output without this tool's corpus ownership marker")
    if (out / "config").is_symlink() or not (out / "HEAD").is_file():
        raise HistoryError("owned corpus output is not the expected bare repository")
    if git(out, "remote").strip():
        raise HistoryError("refusing to replace a corpus repository configured with a remote")


def _text_versions(data: dict, accepted: list, root: Path) -> list:
    """Resolve only explicitly authorized historical parents, never text inheritance."""
    from _eucharistic_texts import native_parentage, AdapterError
    from _eucharistic_stages import verify_progression, StageError
    progression_input = fingerprint(TOOL_ROOT, TOOL_ROOT / "scripts/_eucharistic_stages.py")
    by_set = {row["id"]: (payload, files) for row, payload, files in accepted}
    versions, transitions, stages = {}, [], {}
    for row in data.get("text_versions", []):
        if row["text_set"] not in by_set:
            raise HistoryError(f"{row['id']}: unknown version text_set")
        payload, files = by_set[row["text_set"]]
        if not payload.get("book_binding") or payload.get("scope", {}).get("complete_declared_extent") is not True:
            raise HistoryError(f"{row['id']}: temporal snapshot requires an independently verified complete declared extent")
        parents = row.get("parents")
        if not isinstance(parents, list) or any(not isinstance(parent, dict) for parent in parents):
            raise HistoryError("text version requires explicit parents array (empty for an isolated root)")
        parent_ids = [parent.get("version_id") for parent in parents]
        if (any(not isinstance(key, str) or not SLUG.fullmatch(key) for key in parent_ids)
                or len(set(parent_ids)) != len(parent_ids)):
            raise HistoryError("text version parents must be distinct version ids")
        event = payload["historical_date"]
        stages[row["id"]] = {"date_kind": event["kind"], "start_year": event["start_year"], "end_year": event["end_year"]}
        versions[row["id"]] = (row, payload, dict(files), [])
    for key, (row, payload, files, receipts) in versions.items():
        for parent in row["parents"]:
            if parent["version_id"] not in versions:
                raise HistoryError(f"{key}: unknown parent version {parent['version_id']}")
            try:
                receipt = native_parentage(root, required_string(parent, "evidence_path", key),
                                          versions[parent["version_id"]][1], payload)
            except (AdapterError, OSError) as error:
                raise HistoryError(f"{key}: historical parentage: {error}") from error
            receipts.append({"version_id": parent["version_id"], **receipt})
            transitions.append({"id": parent["version_id"] + "--" + key, "from_stage": parent["version_id"],
                                "to_stage": key, "status": "documented"})
        metadata = json.loads(files["reconstruction.json"])
        implementation = {stamp["path"]: stamp for stamp in metadata["tool_inputs"]}
        implementation[progression_input["path"]] = progression_input
        metadata["tool_inputs"] = sorted(implementation.values(), key=lambda stamp: stamp["path"])
        metadata.update({"record_kind": "text-version", "id": key,
                         "text_ancestry": "explicit-evidence-authorized" if receipts else "explicit-isolated-root",
                         "historical_parentage_claimed": bool(receipts), "text_inheritance": False,
                         "parents": receipts})
        files["reconstruction.json"] = json_bytes(metadata)
        inputs = {row["path"]: row for row in json.loads(files["inputs.json"])}
        for receipt in receipts:
            for stamp in receipt["inputs"]:
                if stamp["path"] in inputs and inputs[stamp["path"]] != stamp:
                    raise HistoryError("version parentage source changed during validation")
                inputs[stamp["path"]] = stamp
        files["inputs.json"] = json_bytes(sorted(inputs.values(), key=lambda row: row["path"]))
        files["README.md"] = (f"# {payload.get('title', key)}\n\n"
            "This is a complete snapshot within its explicitly reviewed native extent.\n"
            "See coverage.json for whole-book versus constituent coverage and exclusions.\n"
            "Git parents exist only where the exact binding has an evidence authorization receipt.\n"
            "Every snapshot materializes its own verified literal text; no parent text is inherited.\n"
            "The Git timestamp is synthetic 2000-01-01, never the historical event date.\n"
            "Historical date bounds and their event role remain in reconstruction.json.\n").encode()
    try:
        verify_progression(stages, transitions)
    except StageError as error:
        raise HistoryError(f"text version progression: {error}") from error
    ordered, pending = [], set(versions)
    while pending:
        ready = sorted(key for key in pending if all(parent["version_id"] not in pending for parent in versions[key][0]["parents"]))
        if not ready:
            raise HistoryError("text version parent cycle")
        for key in ready:
            ordered.append(versions[key])
            pending.remove(key)
    if fingerprint(TOOL_ROOT, TOOL_ROOT / progression_input["path"]) != progression_input:
        raise HistoryError("version progression implementation changed during validation")
    return ordered


def corpus(source: Path, root: Path, out: Path, *, ventilator, adapter_loader=None, supported_adapters=None) -> dict:
    root = root.resolve()
    if adapter_loader is None:
        from _eucharistic_texts import load_adapter, adapter_ids
        adapter_loader, supported_adapters = load_adapter, adapter_ids(root)
    data, routing_inputs = route(source, root)
    rows = data.get("text_sets", [])
    if not rows:
        raise HistoryError("no text_sets configured")
    _owned_output(out)
    accepted = []
    for row in sorted(rows, key=lambda row: row["id"]):
        adapter = row.get("adapter")
        if adapter not in supported_adapters:
            raise HistoryError(f"unknown text adapter: {adapter!r}")
        payload = adapter_loader(adapter, root)
        verify_adapter(payload, root)
        inputs = {**routing_inputs, **{item["path"]: item for item in payload["inputs"]}}
        accepted.append((row, payload, reconstruction_tree(payload, row["id"], inputs, ventilator=ventilator)))
    versions = _text_versions(data, accepted, root)
    # All source/permission checks happen before touching a previous artifact.
    for expected in routing_inputs.values():
        if fingerprint(root, inside(root, expected["path"]))["sha256"] != expected["sha256"]:
            raise HistoryError(f"routing input changed during reconstruction: {expected['path']}")
    for _, payload, _ in accepted:
        verify_adapter(payload, root)
    for _, _, files, _ in versions:
        for expected in json.loads(files["inputs.json"]):
            if fingerprint(root, inside(root, expected["path"])) != expected:
                raise HistoryError(f"version input changed during reconstruction: {expected['path']}")
    out.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".act-history-corpus-", dir=out.parent))
    backup = None
    try:
        git(stage, "init", "--bare", "--template=", "--object-format=sha1", "--initial-branch=corpus")
        stream = bytearray()
        for row, payload, files in accepted:
            identifier = row["id"]
            message = (f"Reconstruct bounded text: {identifier}\n\nRecord-kind: reconstruction\n"
                       f"Target-date: {payload.get('target_date') or 'unestablished'}\n"
                       f"Witness-date: {payload.get('witness_date') or 'not-a-single-witness'}\n"
                       f"Reconstruction-review-date: {payload.get('reviewed_on') or 'unestablished'}\n"
                       "Timestamp-policy: synthetic-fixed-epoch-v1\nGit-date-role: synthetic-serialization\nHistorical-act-claimed: no\n").encode()
            stream.extend(f"commit refs/heads/reconstruction/{identifier}\nauthor Triptych reconstruction <reconstruction@triptych.invalid> 946684800 +0000\ncommitter Triptych reconstruction <reconstruction@triptych.invalid> 946684800 +0000\ndata {len(message)}\n".encode())
            stream.extend(message + b"\ndeleteall\n")
            for name, body in sorted(files.items()):
                stream.extend(f"M 100644 inline {name}\ndata {len(body)}\n".encode())
                stream.extend(body + b"\n")
            stream.extend(b"\n")
        marks = {row["id"]: index for index, (row, _, _, _) in enumerate(versions, 1)}
        for row, payload, files, receipts in versions:
            identifier, event = row["id"], payload["historical_date"]
            message = (f"Native text snapshot: {identifier}\n\nRecord-kind: text-version\n"
                       f"Historical-date-role: {event['kind']}\nHistorical-date-start: {event['start_year']}\n"
                       f"Historical-date-end: {event['end_year']}\nHistorical-date-label: {event['label']}\n"
                       "Timestamp-policy: synthetic-fixed-epoch-v1\nGit-date-role: synthetic-serialization\n"
                       "Historical-act-claimed: no\nText-inheritance: no\n").encode()
            stream.extend(f"commit refs/heads/version/{identifier}\nmark :{marks[identifier]}\nauthor Triptych reconstruction <reconstruction@triptych.invalid> 946684800 +0000\ncommitter Triptych reconstruction <reconstruction@triptych.invalid> 946684800 +0000\ndata {len(message)}\n".encode())
            stream.extend(message + b"\n")
            for index, parent in enumerate(row["parents"]):
                stream.extend(f"{'from' if index == 0 else 'merge'} :{marks[parent['version_id']]}\n".encode())
            stream.extend(b"deleteall\n")
            for name, body in sorted(files.items()):
                stream.extend(f"M 100644 inline {name}\ndata {len(body)}\n".encode())
                stream.extend(body + b"\n")
            stream.extend(b"\n")
        stream.extend(b"done\n")
        git(stage, "fast-import", "--quiet", "--date-format=raw", input=bytes(stream))
        git(stage, "symbolic-ref", "HEAD", "refs/heads/reconstruction/" + accepted[0][0]["id"])
        git(stage, "fsck", "--strict")
        expected_trees = [("refs/heads/reconstruction/" + row["id"], files) for row, _, files in accepted]
        expected_trees += [("refs/heads/version/" + row["id"], files) for row, _, files, _ in versions]
        for ref, files in expected_trees:
            paths = {name.decode("utf-8") for name in git(stage, "ls-tree", "-rz", "--name-only", ref).split(b"\0") if name}
            if paths != set(files):
                raise HistoryError(f"serialized Git tree differs from the complete snapshot: {ref}")
        branches = {row["id"]: git(stage, "rev-parse", "refs/heads/reconstruction/" + row["id"]).decode().strip()
                    for row, _, _ in accepted}
        version_branches = {row["id"]: git(stage, "rev-parse", "refs/heads/version/" + row["id"]).decode().strip()
                            for row, _, _, _ in versions}
        marker = {"schema": CORPUS_SCHEMA, "owner": "tools/act-history corpus", "branches": branches}
        if versions:
            marker["version_branches"] = version_branches
        (stage / MARKER).write_bytes(json_bytes(marker))
        _owned_output(out)
        if out.exists():
            backup = Path(tempfile.mkdtemp(prefix=".act-history-corpus-old-", dir=out.parent))
            backup.rmdir()
            out.rename(backup)
        try:
            stage.rename(out)
        except OSError:
            if backup is not None:
                backup.rename(out)
                backup = None
            raise
        if backup is not None:
            shutil.rmtree(backup)
        return {"schema": CORPUS_SCHEMA, "out": str(out), "commits": len(accepted) + len(versions), "branches": branches,
                "units": sum(len(payload["units"]) for _, payload, _ in accepted),
                "text_sets": [{"id": row["id"], "adapter": row["adapter"], "counts": payload["counts"],
                               "scope": payload["scope"], "ref": "refs/heads/reconstruction/" + row["id"]}
                              for row, payload, _ in accepted],
                "historical_ancestry_claimed": any(receipts for _, _, _, receipts in versions),
                **({"version_commits": len(versions), "version_branches": version_branches} if versions else {})}
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def _member_container(unit: dict) -> tuple | None:
    if unit.get("native_path"):
        return ("native", *unit["native_path"][:-1])
    if unit.get("division"):
        return ("ordinary", unit["division"])
    identity = unit.get("identity", {})
    fields = ("mass", "form", "course", "cycle")
    if all(field in identity for field in fields):
        return ("proper", *(identity[field] for field in fields))
    return None


def _comparison_record_binding(record: dict | None, members: list[dict]) -> dict:
    """Check declared canonical identities, never infer a manuscript mapping."""
    if record is None:
        return {"status": "no-catalogue-record", "checked_fields": []}
    declared = record["source_record"]
    checked = {}
    edition = declared.get("source_library_edition_id")
    if "source_library_edition_id" in declared:
        if not isinstance(edition, str) or not edition.strip():
            raise HistoryError(f"{record['id']}: invalid canonical edition binding")
        if any(unit.get("text_edition_id") != edition for unit in members):
            raise HistoryError(f"{record['id']}: comparison member text edition does not match catalogue binding")
        checked["source_library_edition_id"] = edition
    # A critical edition can contain several different liturgies. Its edition
    # identity alone cannot substitute for an explicitly bounded passage owner.
    for field, unit_field in (("source_library_passage_ids", "source_id"),
                              ("source_library_checked_text_artifact_ids", "source_artifact_id")):
        if field not in declared:
            continue
        allowed = declared[field]
        if (not isinstance(allowed, list) or not allowed
                or any(not isinstance(value, str) or not value.strip() for value in allowed)
                or len(allowed) != len(set(allowed))):
            raise HistoryError(f"{record['id']}: invalid canonical {field} binding")
        if any(unit.get(unit_field) not in allowed for unit in members):
            raise HistoryError(f"{record['id']}: comparison member {unit_field} does not match catalogue binding")
        checked[field] = list(allowed)
    return {"status": "checked-declared-identities" if checked else "unestablished-no-canonical-binding",
            "checked_fields": list(checked), "declarations": checked,
            "limitation": "Only explicit source-owner identities are checked; no manuscript identity, historical date or ancestry is inferred."}


def compare(source: Path, root: Path, identifier: str, *, ventilator,
            adapter_loader=None, supported_adapters=None, act_loader=None) -> dict:
    """Compare explicit witness membership without creating textual ancestry."""
    root = root.resolve()
    data, inputs = route(source, root)
    declarations = {row["id"]: row for row in data.get("comparisons", [])}
    if identifier not in declarations:
        raise HistoryError(f"unknown comparison: {identifier!r}")
    declaration = declarations[identifier]
    identity_claim = comparison_identity(declaration)
    if declaration.get("membership_status") != "established":
        raise HistoryError("comparison membership must be explicitly established")
    for field in ("basis", "apparatus_caveat"):
        if not isinstance(declaration.get(field), str) or not declaration[field].strip():
            raise HistoryError(f"comparison requires {field}")
    references = declaration.get("source_refs")
    if (not isinstance(references, list) or not references
            or any(not isinstance(key, str) or not key for key in references)
            or len(references) != len(set(references))):
        raise HistoryError("comparison requires distinct explicit source_refs")
    if adapter_loader is None:
        from _eucharistic_texts import load_adapter, adapter_ids
        adapter_loader, supported_adapters = load_adapter, adapter_ids(root)
    text_sets = {row["id"]: row for row in data.get("text_sets", [])}
    loaded, sides, source_records, tool_inputs = {}, {}, {}, {}

    def collect(rows: list[dict], target: dict, key: str) -> None:
        for row in rows:
            name = row[key]
            if name in target and json_bytes(target[name]) != json_bytes(row):
                raise HistoryError(f"comparison inputs disagree for {name}")
            target[name] = row

    related = []
    records = {}
    stage_inputs = None
    for side in ("left", "right"):
        if not isinstance(declaration.get(side), dict):
            raise HistoryError(f"comparison {side} must name a configured text_set")
    if data.get("relationship_sets") or any("record_id" in declaration.get(side, {}) for side in ("left", "right")):
        if data.get("act_slices") and act_loader is None:
            raise HistoryError("linked comparison requires the owning act loader to validate catalogue records")
        context = catalogue(source, root, act_loader=act_loader)
        records = {row["id"]: row for row in context["entries"]}
        related = [row for row in context["relationships"] if identifier in row["comparison_ids"]]
        collect(context["inputs"], inputs, "path")
        stage_inputs = context["stage_history"]["inputs"]

    for side in ("left", "right"):
        selected = declaration.get(side)
        if not isinstance(selected, dict) or selected.get("text_set") not in text_sets:
            raise HistoryError(f"comparison {side} must name a configured text_set")
        ids = selected.get("unit_ids")
        if (not isinstance(ids, list) or not ids
                or any(not isinstance(key, str) or not key for key in ids)
                or len(ids) != len(set(ids))):
            raise HistoryError(f"comparison {side} requires distinct ordered unit_ids")
        owner = text_sets[selected["text_set"]]
        adapter = owner["adapter"]
        if adapter not in supported_adapters:
            raise HistoryError(f"unknown text adapter: {adapter!r}")
        if adapter not in loaded:
            payload = adapter_loader(adapter, root)
            verify_adapter(payload, root)
            loaded[adapter] = payload
        payload = loaded[adapter]
        units = {unit["unit_id"]: unit for unit in payload["units"]}
        missing = [key for key in ids if key not in units]
        if missing:
            raise HistoryError(f"comparison {side} names missing unit IDs: {', '.join(missing)}")
        members = [units[key] for key in ids]
        record_binding = _comparison_record_binding(records.get(selected.get("record_id")), members)
        if len(members) > 1:
            containers = [_member_container(unit) for unit in members]
            order = [unit.get("source_order") for unit in members]
            if (containers[0] is None or any(value != containers[0] for value in containers)
                    or any(not isinstance(value, int) or isinstance(value, bool) for value in order)
                    or any(a >= b for a, b in zip(order, order[1:]))):
                raise HistoryError(f"comparison {side} membership has uncertain source order or container")
        output_members = []
        for position, unit in enumerate(members, 1):
            body = serialized_text(unit["text"], unit["unit_id"], ventilator=ventilator)
            output_members.append({**{key: value for key, value in unit.items() if key != "text"},
                                   "comparison_order": position, "text_path": text_path(unit),
                                   "source_text": unit["text"], "serialized_text": body.decode("utf-8"),
                                   "serialized_text_sha256": digest(body)})
        joined = " ".join(unit["text"] for unit in members)
        body = serialized_text(joined, identifier + ":" + side, ventilator=ventilator)
        sides[side] = {"text_set": owner["id"], "adapter": adapter, "title": payload.get("title"),
                       "record_id": selected.get("record_id"), "record_binding": record_binding,
                       "target_date": payload.get("target_date"), "witness_date": payload.get("witness_date"),
                       "reviewed_on": payload.get("reviewed_on"), "scope": payload.get("scope"),
                       "members": output_members, "join_rule": "insert-one-space-between-exact-source-bodies",
                       "joined_source_text": joined, "joined_source_text_sha256": digest(joined.encode("utf-8")),
                       "serialized_text": body.decode("utf-8"), "serialized_text_sha256": digest(body)}
        collect(payload["inputs"], inputs, "path")
        collect(payload.get("tool_inputs", []), tool_inputs, "path")
        collect(payload.get("sources", []), source_records, "id")
    unresolved = [key for key in references if key not in source_records]
    if unresolved:
        raise HistoryError("comparison source_refs are not in its checked source owners: " + ", ".join(unresolved))
    # Revalidate after both sides are loaded; no result may mix changing inputs.
    for payload in loaded.values():
        verify_adapter(payload, root)
    for expected in inputs.values():
        if fingerprint(root, inside(root, expected["path"]))["sha256"] != expected["sha256"]:
            raise HistoryError(f"comparison input changed: {expected['path']}")
    if stage_inputs is not None:
        from _eucharistic_stages import verify_inputs as verify_stage_inputs, StageError
        try:
            verify_stage_inputs(root, stage_inputs, fingerprint=fingerprint)
        except StageError as error:
            raise HistoryError(f"stage history: {error}") from error
    for relative in ("scripts/_eucharistic_history.py", "scripts/_eucharistic_stages.py", "tools/act-history"):
        tool_inputs[relative] = fingerprint(TOOL_ROOT, TOOL_ROOT / relative)
    unified = "".join(difflib.unified_diff(
        sides["left"]["serialized_text"].splitlines(keepends=True),
        sides["right"]["serialized_text"].splitlines(keepends=True),
        fromfile="left/" + sides["left"]["text_set"], tofile="right/" + sides["right"]["text_set"],
    ))
    return {"schema": COMPARISON_SCHEMA, "id": identifier, "kind": declaration["kind"], "identity_claim": identity_claim,
            "membership_status": declaration["membership_status"], "basis": declaration["basis"],
            "apparatus_caveat": declaration["apparatus_caveat"], "source_refs": references,
            "historical_ancestry_claimed": False, "historical_act_claimed": False,
            "introduction_date_inferred": False, "text_serialization": TEXT_SERIALIZATION,
            "relationship_ids": [row["id"] for row in related], "relationships": related,
            **sides, "unified_diff": unified, "identical_serialized_text": not unified,
            "inputs": sorted(inputs.values(), key=lambda row: row["path"]),
            "tool_inputs": sorted(tool_inputs.values(), key=lambda row: row["path"]),
            "sources": sorted(source_records.values(), key=lambda row: row["id"]),
            "limitations": ["This is an explicitly aligned witness comparison, not an asserted historical revision or parent relationship.",
                            "Orthography, spacing, capitalization and punctuation remain visible; a textual diff does not classify their historical significance.",
                            "The apparatus caveat must accompany any historical interpretation of this bounded passage."]}


def write_comparison(payload: dict, out: Path) -> dict:
    if out.is_symlink():
        raise HistoryError("refusing a symlink comparison output")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(json_bytes(payload))
    return {"schema": COMPARISON_SCHEMA, "id": payload["id"], "written": str(out),
            "left_units": len(payload["left"]["members"]), "right_units": len(payload["right"]["members"]),
            "identical_serialized_text": payload["identical_serialized_text"], "historical_ancestry_claimed": False}
