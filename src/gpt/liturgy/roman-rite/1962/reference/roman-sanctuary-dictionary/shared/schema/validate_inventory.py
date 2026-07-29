#!/usr/bin/env python3
"""Validate Roman Sanctuary Dictionary object records and derived selections."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
DEFAULT_SCHEMA = HERE / "inventory-schema.toml"
DEFAULT_EDITIONS = HERE / "edition-selections.toml"


@dataclass(frozen=True)
class Problem:
    path: Path
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.field}: {self.message}"


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        return tomllib.load(stream)


def dotted_get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def discover(paths: Iterable[Path]) -> list[Path]:
    found: list[Path] = []
    for path in paths:
        if path.is_dir():
            found.extend(sorted(path.rglob("*.toml")))
        else:
            found.append(path)
    excluded = {DEFAULT_SCHEMA.resolve(), DEFAULT_EDITIONS.resolve()}
    return sorted({p.resolve() for p in found if p.resolve() not in excluded})


class Validator:
    def __init__(self, schema: dict[str, Any], editions: dict[str, Any]) -> None:
        self.schema = schema
        self.editions = editions
        self.problems: list[Problem] = []
        self.records: dict[str, tuple[Path, dict[str, Any]]] = {}
        self.variants: dict[str, str] = {}
        self.artwork: dict[str, dict[str, Any]] = {}
        self.claims: dict[str, str] = {}
        self.gaps: dict[str, str] = {}
        self.prompts: dict[str, str] = {}
        self.id_pattern = re.compile(schema["id_pattern"])

    def error(self, path: Path, field: str, message: str) -> None:
        self.problems.append(Problem(path, field, message))

    def require_keys(
        self, path: Path, data: dict[str, Any], prefix: str, required: Iterable[str]
    ) -> None:
        for key in required:
            if key not in data:
                self.error(path, f"{prefix}{key}", "required field is missing")

    def enum(
        self, path: Path, field: str, value: Any, values: Iterable[str]
    ) -> None:
        allowed = set(values)
        if not isinstance(value, str) or value not in allowed:
            self.error(path, field, f"expected one of {sorted(allowed)}, got {value!r}")

    def enum_array(
        self, path: Path, field: str, value: Any, values: Iterable[str], minimum: int = 0
    ) -> None:
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            self.error(path, field, "expected an array of strings")
            return
        if len(value) < minimum:
            self.error(path, field, f"expected at least {minimum} item(s)")
        if len(value) != len(set(value)):
            self.error(path, field, "contains duplicate values")
        allowed = set(values)
        for item in value:
            if item not in allowed:
                self.error(path, field, f"unknown value {item!r}")

    def id_value(self, path: Path, field: str, value: Any, prefix: str) -> None:
        if (
            not isinstance(value, str)
            or not value.startswith(prefix)
            or self.id_pattern.fullmatch(value) is None
        ):
            self.error(path, field, f"expected a valid {prefix} identifier")

    def string_array(
        self, path: Path, field: str, value: Any, minimum: int = 0
    ) -> None:
        if not isinstance(value, list) or any(
            not isinstance(v, str) or not v.strip() for v in value
        ):
            self.error(path, field, "expected an array of nonempty strings")
            return
        if len(value) < minimum:
            self.error(path, field, f"expected at least {minimum} item(s)")
        if len(value) != len(set(value)):
            self.error(path, field, "contains duplicate values")

    def register_unique(
        self, registry: dict[str, str], path: Path, field: str, value: Any, owner: str
    ) -> None:
        if not isinstance(value, str):
            return
        if value in registry:
            self.error(path, field, f"duplicate ID; already owned by {registry[value]}")
        else:
            registry[value] = owner

    def validate_record(self, path: Path, data: dict[str, Any]) -> None:
        allowed = set(self.schema["record"]["required"] + self.schema["record"]["optional"])
        for key in sorted(set(data) - allowed):
            self.error(path, key, "unknown top-level field")
        self.require_keys(path, data, "", self.schema["record"]["required"])

        if data.get("schema_version") != self.schema["fields"]["schema_version"]["constant"]:
            self.error(path, "schema_version", "unsupported schema version")
        object_id = data.get("id")
        self.id_value(path, "id", object_id, "obj-")
        if isinstance(object_id, str):
            if object_id in self.records:
                self.error(path, "id", f"duplicate object ID; first seen in {self.records[object_id][0]}")
            else:
                self.records[object_id] = (path, data)

        for field in ("preferred_english_name", "latin_headword"):
            if not isinstance(data.get(field), str) or not data[field].strip():
                self.error(path, field, "expected a nonempty string")
        for field in ("alternate_english_names", "alternate_latin_names"):
            if field in data:
                self.string_array(path, field, data[field])

        for field in ("workflow_state", "presentation_mode"):
            if field in data:
                self.enum(path, field, data[field], self.schema["fields"][field]["values"])
        for field in ("categories", "periods", "statuses", "ceremonies"):
            if field in data:
                self.enum_array(
                    path,
                    field,
                    data[field],
                    self.schema["fields"][field]["values"],
                    minimum=1,
                )

        self.validate_id_array(path, data, "component_objects", "obj-")
        self.validate_id_array(path, data, "confusable_with", "obj-")
        self.validate_id_array(path, data, "related_objects", "obj-")
        if "parent_object" in data:
            self.id_value(path, "parent_object", data["parent_object"], "obj-")

        self.validate_presence(path, data.get("presence"))
        self.validate_handling(path, data.get("handling"))
        self.validate_relevance(path, data.get("audience_relevance"))
        self.validate_claims(path, object_id, data.get("claims"))
        self.validate_sources(path, object_id, data.get("sources"))
        self.validate_variants(path, object_id, data.get("variants", []))
        self.validate_artwork(
            path, object_id, data.get("artwork"), data.get("workflow_state")
        )
        if data.get("presentation_mode") == "text-only" and data.get("artwork"):
            self.error(
                path,
                "artwork",
                "text-only object must not register publication artwork",
            )
        self.validate_audience_notes(path, data)
        self.validate_unresolved_gaps(path, object_id, data)

    def validate_id_array(
        self, path: Path, data: dict[str, Any], field: str, prefix: str
    ) -> None:
        if field not in data:
            return
        value = data[field]
        if not isinstance(value, list):
            self.error(path, field, "expected an array")
            return
        if len(value) != len(set(v for v in value if isinstance(v, str))):
            self.error(path, field, "contains duplicate IDs")
        for index, item in enumerate(value):
            self.id_value(path, f"{field}[{index}]", item, prefix)

    def validate_presence(self, path: Path, value: Any) -> None:
        if not isinstance(value, dict):
            self.error(path, "presence", "expected a table")
            return
        self.require_keys(path, value, "presence.", self.schema["presence"]["required"])
        allowed = set(self.schema["presence"]["required"] + self.schema["presence"]["optional"])
        for key in set(value) - allowed:
            self.error(path, f"presence.{key}", "unknown field")
        for field in ("locations", "contexts"):
            if field in value:
                self.string_array(path, f"presence.{field}", value[field], minimum=1)
        if "composition_ids" in value:
            if not isinstance(value["composition_ids"], list):
                self.error(path, "presence.composition_ids", "expected an array")
            else:
                for index, item in enumerate(value["composition_ids"]):
                    self.id_value(path, f"presence.composition_ids[{index}]", item, "plt-")
        if "local_variability" in value:
            self.enum(
                path,
                "presence.local_variability",
                value["local_variability"],
                self.schema["presence"]["local_variability"]["values"],
            )

    def validate_handling(self, path: Path, value: Any) -> None:
        if not isinstance(value, dict):
            self.error(path, "handling", "expected a table")
            return
        self.require_keys(path, value, "handling.", self.schema["handling"]["required"])
        allowed = set(self.schema["handling"]["required"] + self.schema["handling"]["optional"])
        for key in set(value) - allowed:
            self.error(path, f"handling.{key}", "unknown field")
        handlers = self.schema["handling"]["ordinary_handlers"]["values"]
        if "ordinary_handlers" in value:
            self.enum_array(path, "handling.ordinary_handlers", value["ordinary_handlers"], handlers, 1)
        if "server_relation" in value:
            self.enum(
                path,
                "handling.server_relation",
                value["server_relation"],
                self.schema["handling"]["server_relation"]["values"],
            )
        for field in ("prepares", "presents", "receives", "stores"):
            if field in value:
                self.enum_array(path, f"handling.{field}", value[field], handlers)
        if "warnings" in value:
            self.string_array(path, "handling.warnings", value["warnings"])

    def validate_relevance(self, path: Path, value: Any) -> None:
        if not isinstance(value, dict):
            self.error(path, "audience_relevance", "expected a table")
            return
        required = self.schema["audience_relevance"]["required"]
        self.require_keys(path, value, "audience_relevance.", required)
        for key in set(value) - set(required):
            self.error(path, f"audience_relevance.{key}", "unknown field")
        for key in required:
            if key in value:
                self.enum(
                    path,
                    f"audience_relevance.{key}",
                    value[key],
                    self.schema["audience_relevance"][key]["values"],
                )

    def validate_claims(self, path: Path, owner: Any, value: Any) -> None:
        if not isinstance(value, list) or not value:
            self.error(path, "claims", "expected a nonempty array of tables")
            return
        spec = self.schema["claim"]
        allowed = set(spec["required"] + spec["optional"])
        for index, claim in enumerate(value):
            field = f"claims[{index}]"
            if not isinstance(claim, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, claim, field + ".", spec["required"])
            for key in set(claim) - allowed:
                self.error(path, f"{field}.{key}", "unknown field")
            claim_id = claim.get("id")
            self.id_value(path, f"{field}.id", claim_id, "clm-")
            self.register_unique(self.claims, path, f"{field}.id", claim_id, str(owner))
            if "kind" in claim:
                self.enum(path, f"{field}.kind", claim["kind"], self.schema["claim"]["kind"]["values"])
            if "evidence_state" in claim:
                self.enum(
                    path,
                    f"{field}.evidence_state",
                    claim["evidence_state"],
                    self.schema["claim"]["evidence_state"]["values"],
                )
            if not isinstance(claim.get("text"), str) or not claim["text"].strip():
                self.error(path, f"{field}.text", "expected a nonempty string")
            self.validate_local_id_list(path, field + ".source_ids", claim.get("source_ids"), "src-")
            self.validate_local_id_list(
                path, field + ".applies_to_variants", claim.get("applies_to_variants", []), "var-"
            )
            if claim.get("evidence_state") != "editorial-proposal" and not claim.get("source_ids"):
                self.error(path, f"{field}.source_ids", "non-editorial claims require a source")
            if "as_of" in claim and not isinstance(claim["as_of"], dt.date):
                self.error(path, f"{field}.as_of", "expected an unquoted TOML local date")

    def validate_sources(self, path: Path, owner: Any, value: Any) -> None:
        if not isinstance(value, list) or not value:
            self.error(path, "sources", "expected a nonempty array of tables")
            return
        spec = self.schema["source"]
        allowed = set(spec["required"] + spec["optional"])
        local: set[str] = set()
        for index, source in enumerate(value):
            field = f"sources[{index}]"
            if not isinstance(source, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, source, field + ".", spec["required"])
            for key in set(source) - allowed:
                self.error(path, f"{field}.{key}", "unknown field")
            source_id = source.get("id")
            self.id_value(path, f"{field}.id", source_id, "src-")
            if source_id in local:
                self.error(path, f"{field}.id", "duplicate source ID within object")
            elif isinstance(source_id, str):
                local.add(source_id)
            for key in ("binding", "locus"):
                if not isinstance(source.get(key), str) or not source[key].strip():
                    self.error(path, f"{field}.{key}", "expected a nonempty string")
            if isinstance(source.get("binding"), str) and re.match(
                r"^[a-z][a-z0-9+.-]*://", source["binding"], re.IGNORECASE
            ):
                self.error(path, f"{field}.binding", "expected a canonical binding ID, not a bare URL")
            if "role" in source:
                self.enum(path, f"{field}.role", source["role"], self.schema["source"]["role"]["values"])
            if "verification_state" in source:
                self.enum(
                    path,
                    f"{field}.verification_state",
                    source["verification_state"],
                    self.schema["source"]["verification_state"]["values"],
                )
            if "checked_on" in source and not isinstance(source["checked_on"], dt.date):
                self.error(path, f"{field}.checked_on", "expected an unquoted TOML local date")
        if isinstance(owner, str):
            record = self.records.get(owner, (path, {}))[1]
            for index, claim in enumerate(record.get("claims", [])):
                if not isinstance(claim, dict):
                    continue
                for source_id in claim.get("source_ids", []):
                    if source_id not in local:
                        self.error(path, f"claims[{index}].source_ids", f"unknown local source {source_id}")

    def validate_variants(self, path: Path, owner: Any, value: Any) -> None:
        if not isinstance(value, list):
            self.error(path, "variants", "expected an array of tables")
            return
        spec = self.schema["variant"]
        allowed = set(spec["required"] + spec["optional"])
        for index, variant in enumerate(value):
            field = f"variants[{index}]"
            if not isinstance(variant, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, variant, field + ".", spec["required"])
            for key in set(variant) - allowed:
                self.error(path, f"{field}.{key}", "unknown field")
            variant_id = variant.get("id")
            self.id_value(path, f"{field}.id", variant_id, "var-")
            self.register_unique(self.variants, path, f"{field}.id", variant_id, str(owner))
            for key in ("preferred_name", "distinguishing_features"):
                if not isinstance(variant.get(key), str) or not variant[key].strip():
                    self.error(path, f"{field}.{key}", "expected a nonempty string")
            if "status" in variant:
                self.enum(
                    path,
                    f"{field}.status",
                    variant["status"],
                    self.schema["fields"]["statuses"]["values"],
                )
            if "periods" in variant:
                self.enum_array(
                    path,
                    f"{field}.periods",
                    variant["periods"],
                    self.schema["fields"]["periods"]["values"],
                    1,
                )
            if "ceremonies" in variant:
                self.enum_array(
                    path,
                    f"{field}.ceremonies",
                    variant["ceremonies"],
                    self.schema["fields"]["ceremonies"]["values"],
                    1,
                )
            for key in ("regions", "communities"):
                if key in variant:
                    self.string_array(path, f"{field}.{key}", variant[key], 1)
            self.validate_local_id_list(path, f"{field}.source_ids", variant.get("source_ids"), "src-")
            self.validate_local_id_list(path, f"{field}.artwork_ids", variant.get("artwork_ids"), "art-")

    def validate_artwork(
        self, path: Path, owner: Any, value: Any, workflow_state: Any
    ) -> None:
        if not isinstance(value, list):
            self.error(path, "artwork", "expected an array of tables")
            return
        if not value and workflow_state == "publication-ready":
            self.error(
                path,
                "artwork",
                "publication-ready object requires at least one artwork record",
            )
        spec = self.schema["artwork"]
        allowed = set(spec["required"] + spec["optional"])
        for index, art in enumerate(value):
            field = f"artwork[{index}]"
            if not isinstance(art, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, art, field + ".", spec["required"])
            for key in set(art) - allowed:
                self.error(path, f"{field}.{key}", "unknown field")
            art_id = art.get("id")
            self.id_value(path, f"{field}.id", art_id, "art-")
            if isinstance(art_id, str):
                canonical_fields = (
                    "view",
                    "asset",
                    "review_state",
                    "depicts",
                    "variant_id",
                    "scale_mode",
                    "context_object_ids",
                    "render_owner",
                )
                identity = {key: art.get(key) for key in canonical_fields}
                existing = self.artwork.get(art_id)
                if existing is None:
                    self.artwork[art_id] = {
                        "identity": identity,
                        "owners": {str(owner)},
                        "path": path,
                    }
                else:
                    if identity != existing["identity"]:
                        self.error(
                            path,
                            f"{field}.id",
                            f"shared artwork definition conflicts with {existing['path']}",
                        )
                    existing["owners"].add(str(owner))
            for key in ("view", "review_state", "scale_mode"):
                if key in art:
                    self.enum(path, f"{field}.{key}", art[key], self.schema["artwork"][key]["values"])
            if not isinstance(art.get("asset"), str) or not art["asset"].strip():
                self.error(path, f"{field}.asset", "expected a nonempty repository-relative path")
            elif Path(art["asset"]).is_absolute() or ".." in Path(art["asset"]).parts:
                self.error(path, f"{field}.asset", "must be a safe repository-relative path")
            self.validate_local_id_list(path, f"{field}.depicts", art.get("depicts"), "obj-", minimum=1)
            if isinstance(owner, str) and owner not in art.get("depicts", []):
                self.error(
                    path,
                    f"{field}.depicts",
                    f"shared artwork must depict its owning record {owner}",
                )
            if "render_owner" in art:
                self.id_value(
                    path, f"{field}.render_owner", art["render_owner"], "obj-"
                )
                if art["render_owner"] not in art.get("depicts", []):
                    self.error(
                        path,
                        f"{field}.render_owner",
                        "render owner must appear in depicts",
                    )
            if "variant_id" in art:
                self.id_value(path, f"{field}.variant_id", art["variant_id"], "var-")
            if "context_object_ids" in art:
                self.validate_local_id_list(
                    path, f"{field}.context_object_ids", art["context_object_ids"], "obj-"
                )

    def validate_audience_notes(self, path: Path, data: dict[str, Any]) -> None:
        notes = data.get("audience_note", [])
        if not isinstance(notes, list):
            self.error(path, "audience_note", "expected an array of tables")
            return
        for index, note in enumerate(notes):
            field = f"audience_note[{index}]"
            if not isinstance(note, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, note, field + ".", self.schema["audience_note"]["required"])
            for key in set(note) - set(self.schema["audience_note"]["required"]):
                self.error(path, f"{field}.{key}", "unknown field")
            if "audience" in note:
                self.enum(
                    path,
                    f"{field}.audience",
                    note["audience"],
                    self.schema["audience_note"]["audience"]["values"],
                )
            self.validate_local_id_list(path, f"{field}.claim_ids", note.get("claim_ids"), "clm-", 1)

    def validate_unresolved_gaps(
        self, path: Path, owner: Any, data: dict[str, Any]
    ) -> None:
        value = data.get("unresolved_gaps")
        if value is None:
            return
        if not isinstance(value, dict):
            self.error(path, "unresolved_gaps", "expected a table")
            return
        required = self.schema["unresolved_gaps"]["required"]
        self.require_keys(path, value, "unresolved_gaps.", required)
        for key in set(value) - set(required):
            self.error(path, f"unresolved_gaps.{key}", "unknown field")
        if not isinstance(value.get("qualification"), str) or not value[
            "qualification"
        ].strip():
            self.error(
                path, "unresolved_gaps.qualification", "expected a nonempty string"
            )

        gaps = value.get("gaps")
        if not isinstance(gaps, list) or not gaps:
            self.error(
                path,
                "unresolved_gaps.gaps",
                "expected a nonempty array of tables",
            )
            gaps = []
        allowed_gap_targets = ("obj-", "clm-", "src-", "art-", "var-")
        gap_spec = self.schema["unresolved_gaps"]["gap"]
        for index, gap in enumerate(gaps):
            field = f"unresolved_gaps.gaps[{index}]"
            if not isinstance(gap, dict):
                self.error(path, field, "expected a table")
                continue
            self.require_keys(path, gap, field + ".", gap_spec["required"])
            for key in set(gap) - set(gap_spec["required"]):
                self.error(path, f"{field}.{key}", "unknown field")
            gap_id = gap.get("id")
            self.id_value(path, f"{field}.id", gap_id, "gap-")
            self.register_unique(self.gaps, path, f"{field}.id", gap_id, str(owner))
            if "kind" in gap:
                self.enum(
                    path,
                    f"{field}.kind",
                    gap["kind"],
                    self.schema["unresolved_gaps"]["gap"]["kind"][
                        "values"
                    ],
                )
            if not isinstance(gap.get("summary"), str) or not gap["summary"].strip():
                self.error(path, f"{field}.summary", "expected a nonempty string")
            self.validate_mixed_id_list(
                path,
                f"{field}.target_ids",
                gap.get("target_ids"),
                allowed_gap_targets,
                minimum=1,
            )

    def validate_mixed_id_list(
        self,
        path: Path,
        field: str,
        value: Any,
        prefixes: tuple[str, ...],
        minimum: int = 0,
    ) -> None:
        if not isinstance(value, list):
            self.error(path, field, "expected an array")
            return
        if len(value) < minimum:
            self.error(path, field, f"expected at least {minimum} item(s)")
        if len(value) != len(set(v for v in value if isinstance(v, str))):
            self.error(path, field, "contains duplicate IDs")
        for index, item in enumerate(value):
            if (
                not isinstance(item, str)
                or not item.startswith(prefixes)
                or self.id_pattern.fullmatch(item) is None
            ):
                self.error(
                    path,
                    f"{field}[{index}]",
                    f"expected an ID beginning with one of {prefixes}",
                )

    def validate_local_id_list(
        self, path: Path, field: str, value: Any, prefix: str, minimum: int = 0
    ) -> None:
        if not isinstance(value, list):
            self.error(path, field, "expected an array")
            return
        if len(value) < minimum:
            self.error(path, field, f"expected at least {minimum} item(s)")
        if len(value) != len(set(v for v in value if isinstance(v, str))):
            self.error(path, field, "contains duplicate IDs")
        for index, item in enumerate(value):
            self.id_value(path, f"{field}[{index}]", item, prefix)

    def validate_cross_references(self) -> None:
        object_ids = set(self.records)
        artwork_ids = set(self.artwork)
        for object_id, (path, data) in self.records.items():
            for field in ("component_objects", "confusable_with", "related_objects"):
                for target in data.get(field, []):
                    if target not in object_ids:
                        self.error(path, field, f"unknown object {target}")
                    if target == object_id:
                        self.error(path, field, "self-reference is not permitted")
            parent = data.get("parent_object")
            if parent is not None and parent not in object_ids:
                self.error(path, "parent_object", f"unknown object {parent}")
            local_sources = {
                s.get("id") for s in data.get("sources", []) if isinstance(s, dict)
            }
            local_claims = {
                c.get("id") for c in data.get("claims", []) if isinstance(c, dict)
            }
            for index, claim in enumerate(data.get("claims", [])):
                if not isinstance(claim, dict):
                    continue
                for variant in claim.get("applies_to_variants", []):
                    if self.variants.get(variant) != object_id:
                        self.error(path, f"claims[{index}].applies_to_variants", f"variant {variant} is not owned by this object")
            for index, variant in enumerate(data.get("variants", [])):
                if not isinstance(variant, dict):
                    continue
                for source in variant.get("source_ids", []):
                    if source not in local_sources:
                        self.error(path, f"variants[{index}].source_ids", f"unknown local source {source}")
                for art in variant.get("artwork_ids", []):
                    entry = self.artwork.get(art)
                    if art not in artwork_ids or not entry or object_id not in entry["owners"]:
                        self.error(path, f"variants[{index}].artwork_ids", f"artwork {art} is not linked from this object")
            for index, art in enumerate(data.get("artwork", [])):
                if not isinstance(art, dict):
                    continue
                for depicted in art.get("depicts", []):
                    if depicted not in object_ids:
                        self.error(path, f"artwork[{index}].depicts", f"unknown object {depicted}")
                for context in art.get("context_object_ids", []):
                    if context not in object_ids:
                        self.error(path, f"artwork[{index}].context_object_ids", f"unknown object {context}")
                variant = art.get("variant_id")
                if variant is not None and variant not in self.variants:
                    self.error(path, f"artwork[{index}].variant_id", f"unknown variant {variant}")
            for index, note in enumerate(data.get("audience_note", [])):
                if not isinstance(note, dict):
                    continue
                for claim in note.get("claim_ids", []):
                    if claim not in local_claims:
                        self.error(path, f"audience_note[{index}].claim_ids", f"unknown local claim {claim}")
            local_variants = {
                variant.get("id")
                for variant in data.get("variants", [])
                if isinstance(variant, dict)
            }
            local_artwork = {
                art.get("id")
                for art in data.get("artwork", [])
                if isinstance(art, dict)
            }
            for index, gap in enumerate(
                (
                    data.get("unresolved_gaps", {}).get("gaps", [])
                    if isinstance(data.get("unresolved_gaps"), dict)
                    else []
                )
            ):
                if not isinstance(gap, dict):
                    continue
                for target in gap.get("target_ids", []):
                    known = (
                        target == object_id
                        or target in local_claims
                        or target in local_sources
                        or target in local_variants
                        or target in local_artwork
                    )
                    if not known:
                        self.error(
                            path,
                            f"unresolved_gaps.gaps[{index}].target_ids",
                            f"unknown or nonlocal target {target}",
                        )

    def validate_publication_gate(self) -> None:
        gate = self.schema["publication_gate"]
        for object_id, (path, data) in self.records.items():
            if data.get("workflow_state") not in gate["selectable_workflow_states"]:
                continue
            claims = [claim for claim in data.get("claims", []) if isinstance(claim, dict)]
            artworks = [art for art in data.get("artwork", []) if isinstance(art, dict)]
            sources_list = [
                source for source in data.get("sources", []) if isinstance(source, dict)
            ]
            kinds = {claim.get("kind") for claim in claims}
            for required in gate["required_claim_kinds"]:
                if required not in kinds:
                    self.error(path, "claims", f"publication-ready object lacks required {required!r} claim")
            sources = {source.get("id"): source for source in sources_list}
            for index, claim in enumerate(claims):
                if claim.get("evidence_state") not in gate["allowed_claim_states"]:
                    self.error(path, f"claims[{index}].evidence_state", "not allowed for publication-ready object")
                if claim.get("kind") == "symbolism" and not claim.get("source_ids"):
                    self.error(path, f"claims[{index}].source_ids", "symbolism requires a source")
                for source_id in claim.get("source_ids", []):
                    source = sources.get(source_id)
                    if source and source.get("verification_state") != "claim-verified":
                        self.error(
                            path,
                            f"claims[{index}].source_ids",
                            f"publication claim cites source {source_id} that is not claim-verified",
                        )
            if "historical-discontinued-before-1962" in data.get("statuses", []):
                if "chronology" not in kinds:
                    self.error(path, "claims", "historical object requires a chronology claim")
            for index, art in enumerate(artworks):
                if art.get("review_state") not in gate["allowed_artwork_states"]:
                    self.error(path, f"artwork[{index}].review_state", "not allowed for publication-ready object")
            source_states = {s.get("verification_state") for s in sources_list}
            if "claim-verified" not in source_states:
                self.error(path, "sources", "publication-ready object has no claim-verified source")

    def selected(self, edition: dict[str, Any]) -> list[str]:
        selected: list[str] = []
        for object_id, (_, data) in self.records.items():
            if data.get("workflow_state") not in edition.get("include_workflow_states", []):
                continue
            if set(data.get("statuses", [])) & set(edition.get("exclude_statuses", [])):
                continue
            if object_id in edition.get("explicit_exclusions", []):
                continue
            relevance_field = edition.get("relevance_field")
            if relevance_field:
                relevance_match = dotted_get(data, relevance_field) in edition.get("include_relevance", [])
                category_match = bool(
                    set(data.get("categories", [])) & set(edition.get("include_categories", []))
                )
                if not relevance_match and not category_match:
                    continue
            else:
                if not set(data.get("statuses", [])) & set(edition.get("include_statuses", [])):
                    continue
                if not set(data.get("periods", [])) & set(edition.get("include_periods", [])):
                    continue
            selected.append(object_id)
        return sorted(selected, key=lambda item: self.records[item][1].get("sort_name", self.records[item][1].get("preferred_english_name", item)))

    def validate(self, paths: list[Path]) -> None:
        for path in paths:
            try:
                data = load_toml(path)
            except (OSError, tomllib.TOMLDecodeError) as exc:
                self.error(path, "<file>", f"cannot parse TOML: {exc}")
                continue
            self.validate_record(path, data)
        self.validate_cross_references()
        self.validate_publication_gate()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("inventory", nargs="+", type=Path, help="object TOML file(s) or directories")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--editions", type=Path, default=DEFAULT_EDITIONS)
    parser.add_argument("--list-edition", metavar="EDITION_ID")
    args = parser.parse_args(argv)

    try:
        schema = load_toml(args.schema)
        editions = load_toml(args.editions)
    except (OSError, tomllib.TOMLDecodeError, KeyError) as exc:
        print(f"schema error: {exc}", file=sys.stderr)
        return 2

    validator = Validator(schema, editions)
    paths = discover(args.inventory)
    if not paths:
        print("inventory error: no object TOML files found", file=sys.stderr)
        return 2
    validator.validate(paths)
    for problem in sorted(validator.problems, key=lambda p: (str(p.path), p.field, p.message)):
        print(problem, file=sys.stderr)
    if validator.problems:
        print(f"{len(validator.problems)} problem(s)", file=sys.stderr)
        return 1

    if args.list_edition:
        edition = next(
            (entry for entry in editions.get("editions", []) if entry.get("id") == args.list_edition),
            None,
        )
        if edition is None:
            print(f"unknown edition: {args.list_edition}", file=sys.stderr)
            return 2
        for object_id in validator.selected(edition):
            print(object_id)
    else:
        print(f"validated {len(validator.records)} object record(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
