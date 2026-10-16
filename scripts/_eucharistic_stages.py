"""Validate source-described book states for the owning act-history catalogue.

This evidence projection never supplies act parents or text-carry permissions.
An inspected source declaration is reviewable evidence, not automated collation.
"""
from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

SCHEMA = "triptych-eucharistic-stages/v1"
DIRECTORY = "src/sources/inventories/eucharistic-stages"
TABLES = ("traditions", "sources", "stages", "transitions", "gaps")
COMPONENTS = {"ordinary", "anaphoras", "propers", "rubrics", "calendar", "lectionary", "chant"}
KINDS = {"primary-book", "primary-act", "official-retrospective", "critical-edition",
         "scholarship", "institutional-catalogue"}
PRIMARY_KINDS = {"primary-book", "primary-act", "official-retrospective", "critical-edition"}
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._:-]*\Z")
FIELDS = {
    "traditions": "id label family scope coverage_note",
    "sources": "id title url kind inspection checked_on status limitations",
    "stages": "id tradition_id label date_label start_year end_year date_kind status scope components witness_ids witness_label summary text_coverage evidence limitations reception",
    "transitions": "id from_stage to_stage kind status evidence_level summary components changes evidence limitations comparison_ids historical_parentage",
    "gaps": "id tradition_id period missing next_source consequence",
}


class StageError(ValueError):
    """The declared book-stage evidence is incomplete or inconsistent."""


def string(row: dict, key: str, context: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise StageError(f"{context}: {key} must be a nonempty string")
    return value


def choice(row: dict, key: str, allowed: set[str], context: str) -> str:
    value = string(row, key, context)
    if value not in allowed:
        raise StageError(f"{context}: unsupported {key} {value!r}")
    return value


def strings(row: dict, key: str, context: str, *, nonempty: bool = False) -> list[str]:
    values = row.get(key)
    if (not isinstance(values, list) or (nonempty and not values)
            or any(not isinstance(value, str) or not value.strip() for value in values)
            or len(values) != len(set(values))):
        raise StageError(f"{context}: {key} must be a distinct string array")
    return values


def fields(row: dict, required: str, context: str, optional: str = "") -> None:
    needed = set(required.split())
    allowed = needed | set(optional.split())
    if not isinstance(row, dict) or needed - row.keys() or row.keys() - allowed:
        raise StageError(f"{context}: missing or unsupported fields")


def evidence(row: dict, sources: dict, context: str, *, inspected: bool) -> list[dict]:
    values = row.get("evidence")
    if not isinstance(values, list) or not values:
        raise StageError(f"{context}: requires evidence")
    seen = set()
    for item in values:
        fields(item, "source_id locus claim", context + " evidence")
        key = string(item, "source_id", context)
        locus = string(item, "locus", context)
        string(item, "claim", context)
        if key not in sources:
            raise StageError(f"{context}: unresolved evidence source {key}")
        identity = (key, locus, item["claim"])
        if identity in seen:
            raise StageError(f"{context}: duplicate evidence")
        seen.add(identity)
        if inspected and sources[key]["status"] != "inspected":
            raise StageError(f"{context}: documented evidence requires inspected sources")
    return values


def component_list(row: dict, context: str) -> list[str]:
    result = strings(row, "components", context, nonempty=True)
    if set(result) - COMPONENTS:
        raise StageError(f"{context}: unsupported component")
    return result


def _object(pairs: list[tuple]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise StageError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _constant(value: str):
    raise StageError(f"invalid JSON number {value}")


def _files(root: Path) -> list[Path]:
    directory = root / DIRECTORY
    if directory.is_symlink():
        raise StageError("stage dossier owner must be a real directory")
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise StageError("stage dossier owner must be a real directory")
    paths = sorted(directory.glob("*.json"))
    for path in paths:
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root):
            raise StageError("stage dossiers must be regular repository files")
    return paths


def verify_inputs(root: Path, inputs: list[dict], *, fingerprint) -> None:
    """Check both auto-discovered membership and every retained byte hash."""
    root = root.resolve()
    paths = [path.relative_to(root).as_posix() for path in _files(root)]
    if paths != [stamp["path"] for stamp in inputs]:
        raise StageError("stage dossier membership changed during projection")
    for stamp in inputs:
        if fingerprint(root, root / stamp["path"]) != stamp:
            raise StageError(f"stage input changed: {stamp['path']}")


def load(root: Path, *, catalogue_ids: set[str], comparisons: dict[str, dict], fingerprint,
         default_tradition_id: str | None = None) -> dict:
    """Read the canonical dossier directory; preserve authored order within files.

    The owning engine supplies its shared fingerprint function. Missing dossiers
    mean unresearched coverage, never an empty historical tradition.
    """
    root = root.resolve()
    paths = _files(root)
    rows = {table: [] for table in TABLES}
    dictionaries = {table: {} for table in TABLES}
    dossiers, inputs, seen_ids, dossier_ids = [], [], set(), set()
    for path in paths:
        stamp = fingerprint(root, path)
        try:
            document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object,
                                  parse_constant=_constant)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise StageError(f"cannot read stage dossier {stamp['path']}: {error}") from error
        # Hash before and after parsing so a changed file cannot acquire an old
        # fingerprint while contributing newer assertions.
        if fingerprint(root, path) != stamp:
            raise StageError(f"stage input changed: {stamp['path']}")
        fields(document, "schema_version record_type dossier_id title traditions sources stages transitions gaps",
               stamp["path"], "acquisition_handoffs catalogue_proposals")
        if type(document["schema_version"]) is not int or document["schema_version"] != 1 or document["record_type"] != "eucharistic-book-stages":
            raise StageError(f"{stamp['path']}: expected eucharistic-book-stages schema 1")
        owner = string(document, "dossier_id", stamp["path"])
        if not IDENTIFIER.fullmatch(owner) or owner in dossier_ids:
            raise StageError(f"duplicate or invalid dossier id {owner!r}")
        dossier_ids.add(owner)
        title = string(document, "title", owner)
        for optional in ("acquisition_handoffs", "catalogue_proposals"):
            if optional in document and not isinstance(document[optional], list):
                raise StageError(f"{owner}: {optional} must be an array")
        dossiers.append({"id": owner, "title": title, "inventory": stamp["path"]})
        inputs.append(stamp)
        for table in TABLES:
            values = document[table]
            if not isinstance(values, list):
                raise StageError(f"{owner}: {table} must be an array")
            for row in values:
                fields(row, FIELDS[table], f"{owner} {table}",
                       "git_ancestry text_inheritance" if table == "transitions" else "")
                key = string(row, "id", owner)
                if not IDENTIFIER.fullmatch(key) or key in seen_ids:
                    raise StageError(f"duplicate or invalid stage-history id {key!r}")
                if table in ("sources", "stages", "transitions") and not any(key.startswith(owner + delimiter) for delimiter in ("-", ".", ":")):
                    raise StageError(f"{key}: id must be prefixed with dossier_id")
                seen_ids.add(key)
                projected = {**row, "origin": {"inventory": stamp["path"], "table": table, "id": key}}
                rows[table].append(projected)
                dictionaries[table][key] = projected

    sources, stages = dictionaries["sources"], dictionaries["stages"]
    traditions = dictionaries["traditions"]
    for row in rows["traditions"]:
        for field in ("label", "family", "scope", "coverage_note"):
            string(row, field, row["id"])
    for row in rows["sources"]:
        context = row["id"]
        for field in ("title", "inspection", "limitations"):
            string(row, field, context)
        choice(row, "kind", KINDS, context)
        choice(row, "status", {"inspected", "lead"}, context)
        try:
            url = urlsplit(string(row, "url", context))
        except ValueError as error:
            raise StageError(f"{context}: malformed source URL") from error
        if url.scheme not in ("http", "https") or not url.netloc or url.username or url.password:
            raise StageError(f"{context}: source URL must be public HTTP(S)")
        value = string(row, "checked_on", context)
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                raise ValueError()
            date.fromisoformat(value)
        except ValueError as error:
            raise StageError(f"{context}: checked_on must be an ISO date") from error
    for row in rows["stages"]:
        context = row["id"]
        for field in ("label", "date_label", "scope", "witness_label", "summary", "limitations", "reception"):
            string(row, field, context)
        if string(row, "tradition_id", context) not in traditions:
            raise StageError(f"{context}: unresolved tradition_id")
        start, end = row["start_year"], row["end_year"]
        if not (start is None and end is None):
            if type(start) is not int or type(end) is not int or not 1 <= start <= end <= 9999:
                raise StageError(f"{context}: date bounds must be null together or ordered integer years")
        choice(row, "date_kind", {"attestation", "publication", "approval", "effective", "reconstruction"}, context)
        status = choice(row, "status", {"documented", "provisional"}, context)
        choice(row, "text_coverage", {"not-transcribed", "partial", "complete"}, context)
        if row["text_coverage"] == "complete":
            raise StageError(f"{context}: complete coverage requires a coordinated full-text binding and scope denominator")
        component_list(row, context)
        for identifier in strings(row, "witness_ids", context):
            if identifier not in catalogue_ids:
                raise StageError(f"{context}: unresolved witness_id {identifier}")
        evidence(row, sources, context, inspected=status == "documented")
    for row in rows["transitions"]:
        context = row["id"]
        for field in ("summary", "limitations"):
            string(row, field, context)
        kind = choice(row, "kind", {"revision", "recension-branch", "reception", "witness-succession"}, context)
        status = choice(row, "status", {"documented", "provisional"}, context)
        level = choice(row, "evidence_level", {"text-collated", "primary-description", "scholarly-description", "bibliographic-only"}, context)
        choice(row, "historical_parentage", {"established", "attributed", "unestablished"}, context)
        components = component_list(row, context)
        for field in ("from_stage", "to_stage"):
            identifier = string(row, field, context)
            if identifier not in stages:
                raise StageError(f"{context}: unresolved {field}")
            if status == "documented" and stages[identifier]["status"] != "documented":
                raise StageError(f"{context}: documented transition requires documented endpoints")
        if row["from_stage"] == row["to_stage"]:
            raise StageError(f"{context}: transition cannot point to itself")
        for flag in ("git_ancestry", "text_inheritance"):
            if flag in row and row[flag] is not False:
                raise StageError(f"{context}: historical stages cannot grant {flag}")
            row[flag] = False
        cited = evidence(row, sources, context, inspected=status == "documented" or level == "text-collated")
        if level == "primary-description" and not any(sources[item["source_id"]]["kind"] in PRIMARY_KINDS for item in cited):
            raise StageError(f"{context}: primary-description requires primary source evidence")
        for identifier in strings(row, "comparison_ids", context):
            if identifier not in comparisons:
                raise StageError(f"{context}: unresolved comparison_id {identifier}")
            comparison = comparisons[identifier]
            left = comparison.get("left", {}).get("record_id")
            right = comparison.get("right", {}).get("record_id")
            earlier = stages[row["from_stage"]]["witness_ids"]
            later = stages[row["to_stage"]]["witness_ids"]
            if not ((left in earlier and right in later) or (right in earlier and left in later)):
                raise StageError(f"{context}: comparison endpoints must match the exact stage witnesses")
        changes = row["changes"]
        if not isinstance(changes, list):
            raise StageError(f"{context}: changes must be an array")
        if (level == "text-collated" or (status == "documented" and kind in ("revision", "recension-branch"))) and not changes:
            raise StageError(f"{context}: requires bounded changes")
        if status == "documented" and kind in ("revision", "recension-branch") and level == "bibliographic-only":
            raise StageError(f"{context}: bibliography alone cannot document substantive revision")
        for change in changes:
            fields(change, "component before after locus_before locus_after evidence", context + " change")
            if choice(change, "component", COMPONENTS, context) not in components:
                raise StageError(f"{context}: change component outside declared scope")
            if status == "documented":
                for endpoint in ("from_stage", "to_stage"):
                    if change["component"] not in stages[row[endpoint]]["components"]:
                        raise StageError(f"{context}: documented {change['component']} change outside {endpoint} component scope")
            for field in ("before", "after", "locus_before", "locus_after"):
                string(change, field, context)
            cited = evidence(change, sources, context, inspected=status == "documented" or level == "text-collated")
            if level == "primary-description" and not any(sources[item["source_id"]]["kind"] in PRIMARY_KINDS for item in cited):
                raise StageError(f"{context}: primary-description change requires primary source evidence")
            if level == "text-collated" and not any(sources[item["source_id"]]["kind"] in ("primary-book", "critical-edition") for item in cited):
                raise StageError(f"{context}: text-collated change requires inspected book or critical-edition evidence")
    for row in rows["gaps"]:
        context = row["id"]
        if string(row, "tradition_id", context) not in traditions:
            raise StageError(f"{context}: unresolved tradition_id")
        for field in ("period", "missing", "next_source", "consequence"):
            string(row, field, context)

    verify_inputs(root, inputs, fingerprint=fingerprint)
    counts = {"dossiers": len(dossiers), **{table: len(rows[table]) for table in TABLES}}
    for table in ("stages", "transitions"):
        for status in ("documented", "provisional"):
            counts[status + "_" + table] = sum(row["status"] == status for row in rows[table])
    for kind, label in (("revision", "revisions"), ("recension-branch", "recension_branches"),
                        ("reception", "receptions"), ("witness-succession", "witness_successions")):
        counts["documented_" + label] = sum(row["status"] == "documented" and row["kind"] == kind
                                          for row in rows["transitions"])
    if default_tradition_id is not None:
        if not isinstance(default_tradition_id, str) or default_tradition_id not in traditions:
            raise StageError("default tradition must resolve an exact tradition id")
    else:
        documented = {row["tradition_id"] for row in rows["stages"] if row["status"] == "documented"}
        default_tradition_id = next((row["id"] for row in rows["traditions"] if row["id"] in documented),
                                    rows["traditions"][0]["id"] if rows["traditions"] else None)
    return {"schema": SCHEMA, "dossiers": dossiers, **rows, "counts": counts, "inputs": inputs,
            "default_tradition_id": default_tradition_id,
            "limitations": ["Stage date bounds describe attestation, publication or the declared event, not continuous validity.",
                            "Documented states are identifiable scoped attestations, not a count of wholly transcribed substantive versions.",
                            "Source descriptions and declared page-level collation retain distinct evidence levels; this checker does not perform historical collation.",
                            "Historical parentage and stage transitions grant no Git ancestry, text inheritance or Catholic reception.",
                            "Missing dossiers, stages or links represent research gaps, not historical absence."]}
