"""Versioned publication manifests over canonical, losslessly retained sources.

Discovery never drops a source because its manifest is missing or invalid.
Adapters describe existing ownership, not an inferred interpretation of TeX.
Schema checks, owning genre gates, and rendered review remain separate facts.
"""
from __future__ import annotations

import fnmatch
import hashlib
import importlib
import importlib.machinery
import importlib.util
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path, PurePosixPath
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("src/common/document-schemas/registry.toml")
MANIFEST = "publication.toml"
PROVIDERS = ("claude", "gpt")
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
MANIFEST_FIELDS = {
    "schema_version", "id", "kind", "profile", "source_format", "entrypoint",
    "outputs", "structure", "content_inputs", "evidence_inputs", "render_inputs",
    "contracts", "canonical_owner", "document",
}
OUTPUT_FIELDS = {"id", "role", "entrypoint", "derivation"}
STRUCTURE_FIELDS = {"role", "source", "data", "key", "outputs", "depends_on"}
CONTRACT_FIELDS = {
    "component_schema", "presentation_contract", "format_contract",
    "authority_contract", "chronology_presentation", "appointed_text_completeness",
}
DERIVED_FIELDS = {
    "provider", "leaf", "source_dir", "manifest_path", "manifest_origin",
    "discovery_error", "profile_definition",
}
OUTPUT_ROLES = ("canonical", "synthesis", "homily")
TEXT_SUFFIXES = {".tex", ".sty", ".cls", ".md", ".toml", ".yaml", ".yml",
                 ".json", ".txt", ".tsv", ".csv", ".bib", ".html", ".css", ".js"}
AUDIT_DIRS = {"research", "evaluations", "evaluation", "instance", "propers"}
OPERATIONAL_RECORDS = {
    "production-review.md", "production-manifest.md", "web-edition-review.md",
    "web-edition-artifacts.toml", "web-review.md", "pdf-review.md", "render-review.md",
    "installation.md", "source-review.json", "source-review.toml",
    "artifacts.json", "web-artifact.json", "standing-findings.json",
}
_SOURCE_INDEX: dict[Path, dict[str, Path]] = {}
_SOURCE_MODULE = None
_FILE_HASHES: dict[Path, tuple[tuple, bytes]] = {}
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
INHERIT_RE = re.compile(r"\\AIInheritedGenerationMetadata\{([^{}]+)\}")

# Paths name actual record owners. A role declaration cannot substitute main.tex
# for a missing audit record. Content roles outside this map stay declarations
# until their owning validator or reviewer examines them.
ROLE_PATHS = {
    "scope": ["research/scope.md"],
    "source-audit": ["research/source-audit.md"],
    "chronology": ["research/chronology.md"],
    "tradition-audit": ["research/tradition-audit.md"],
    "evidence-map": ["research/evidence-map.md"],
    "pastor-succession": ["sections/*historical-pastors*.tex", "research/pastor-succession.md"],
    "derivation": ["research/derivation.md"],
    "prayer-inventory": ["research/prayer-inventory.md"],
    "daily-prayers": ["prayers/day-*.tex"],
    "edition-manifest": ["research/edition-manifest.md"],
    "instance-manifest": ["instance/manifest.md"],
    "appointed-source": ["propers/verified.md"],
    "retrieved-source": ["propers/retrieved.txt"],
    "chronology-record": ["research/chronology.toml"],
    "chronology-projection": ["research/chronology-annotations.tex"],
    "interpretations": ["research/interpretations.md"],
    "proper-components": ["proper-components.toml"],
    "sequence-inventory": ["research/sequence-inventory.md"],
    "rubric-index": ["research/rubric-index.md"],
    "worked-cases": ["research/worked-cases.md"],
    "calendar-inventory": ["research/calendar-inventory.md"],
    "module-map": ["research/module-map.md"],
    "module-selection": ["module-data.tex"],
    "companion-map": ["research/companion-map.md", "research/module-map.md"],
    "curriculum-map": ["research/curriculum-map.md"],
    "passage-inventory": ["research/passage-inventory.md"],
    "vocabulary-map": ["research/vocabulary-map.md"],
    "answer-key-audit": ["research/answer-key-audit.md"],
    "guide-map": ["research/guide-map.md"],
    "response-inventory": ["research/response-inventory.md"],
    "ceremonial-inventory": ["research/ceremonial-inventory.md"],
    "pronunciation-audit": ["research/pronunciation-audit.md"],
    "flash-card-manifest": ["research/flash-card-manifest.md"],
    "dictionary-schema": ["shared/schema/inventory-schema.toml"],
    "dictionary-selections": ["shared/schema/edition-selections.toml"],
    "object-records": ["shared/objects/**/*.toml"],
    "artwork-manifest": ["research/artwork-manifest.toml", "research/artwork-manifest.md"],
    "plate-manifest": ["research/plate-manifest.md", "research/plate-manifest.toml"],
    "sacrament-matrix": ["fragments/full-matrix.tex"],
    "sacrament-lexicon": ["fragments/lexicon.tex"],
    "sacrament-summaries": ["summaries/*.tex"],
    "initiation-table": ["sections/14-churches-initiation.tex"],
    "virtue-inventory": ["research/virtue-inventory.md"],
    "terminology-audit": ["research/terminology-audit.md"],
    "question-inventory": ["research/question-inventory.md"],
    "order-inventory": ["research/order-inventory.md"],
    "corpus-inventory": ["research/corpus-inventory.md"],
    "timeline-audit": ["research/timeline-audit.md"],
    "prayer-text-audit": ["research/prayer-text-audit.md"],
    "corpus-status": ["research/corpus-status.md"],
}


class SchemaError(ValueError):
    """An unsafe, unknown or inconsistent publication declaration."""


def _strict(data: dict, fields: set[str], label: str) -> None:
    if not isinstance(data, dict):
        raise SchemaError(f"{label} must be a table")
    unknown = set(data) - fields
    if unknown:
        raise SchemaError(f"{label}: unknown fields: {', '.join(sorted(unknown))}")


def _string(value, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise SchemaError(f"{label} must be a nonempty trimmed string")
    return value


def _strings(value, label: str) -> list[str]:
    if not isinstance(value, list):
        raise SchemaError(f"{label} must be an array")
    result = [_string(v, label) for v in value]
    if len(result) != len(set(result)):
        raise SchemaError(f"{label} contains duplicates")
    return result


def _relative(value: str, label: str, *, glob: bool = False) -> str:
    value = _string(value, label)
    parts = PurePosixPath(value).parts
    if ("\\" in value or value.startswith("/") or ":" in value or
            any(p in {".", ".."} for p in value.split("/")) or
            not parts or str(PurePosixPath(value)) != value):
        raise SchemaError(f"{label}: unsafe or noncanonical relative path {value!r}")
    if not glob and any(c in value for c in "*?["):
        raise SchemaError(f"{label}: globs are not allowed here")
    return value


def _id(value: str) -> tuple[str, str]:
    value = _relative(value, "id")
    provider, separator, leaf = value.partition("/")
    if provider not in PROVIDERS or not separator or not leaf:
        raise SchemaError("id must be provider-qualified: gpt/<leaf> or claude/<leaf>")
    if any(not KEY.fullmatch(p) for p in leaf.split("/")):
        raise SchemaError(f"id contains a non-kebab-case component: {value}")
    return provider, leaf


def _within(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise SchemaError(f"path escapes repository: {path}")
    return resolved


def _provider_input(root: Path, path: Path, provider: str) -> None:
    resolved = _within(root, path)
    for other in PROVIDERS:
        if other != provider and resolved.is_relative_to((root / "src" / other).resolve()):
            raise SchemaError("publication input imports another provider's authored substance")


def _inheritance_cycle(root: Path, publication_id: str) -> None:
    seen = set()
    current = publication_id
    while current:
        if current in seen:
            raise SchemaError(f"canonical generation inheritance cycle at {current}")
        seen.add(current)
        provider, _ = _id(current)
        metadata = root / "src" / current / "generation-metadata.tex"
        if not metadata.is_file():
            return
        match = INHERIT_RE.search(metadata.read_text(encoding="utf-8"))
        current = f"{provider}/{match.group(1)}" if match else None


def _paths(root: Path, pattern: str, *, must_exist: bool = True) -> list[Path]:
    _relative(pattern, "input path", glob=True)
    matches = sorted(root.glob(pattern)) if any(c in pattern for c in "*?[") else [root / pattern]
    result = []
    for path in matches:
        _within(root, path)
        if path.is_file():
            result.append(path)
        elif path.exists() and not any(c in pattern for c in "*?["):
            raise SchemaError(f"input must name a file, not a directory: {pattern}")
    if must_exist and not result:
        raise SchemaError(f"input has no existing file: {pattern}")
    return result


def _metadata_path(path: Path, root: Path) -> bool:
    relative = path.relative_to(root)
    if relative.parts[:3] != ("src", "sources", "works"):
        return path.suffix in TEXT_SUFFIXES
    # Artifact directories hold metadata next to external or retained payloads.
    # Only their canonical manifest is a metadata input, even for .txt/.toml blobs.
    if "artifacts" in relative.parts:
        return path.name == "artifact.toml"
    return path.suffix == ".toml"


def registry(root: Path = ROOT) -> dict:
    path = Path(root) / REGISTRY
    if not path.is_file():
        path = ROOT / REGISTRY
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    _strict(data, {"schema_version", "record_type", "manifest_name", "description", "types"}, "registry")
    if data.get("schema_version") != 1 or data.get("record_type") != "document-schema-registry":
        raise SchemaError("unsupported document schema registry")
    seen = set()
    for item in data.get("types", []):
        _strict(item, {"kind", "patterns", "profile", "required_roles", "requirements", "gates"}, "type")
        if not KEY.fullmatch(_string(item.get("kind"), "kind")) or item["kind"] in seen:
            raise SchemaError("duplicate or invalid registry kind")
        seen.add(item["kind"])
        for key in ("patterns", "required_roles", "requirements"):
            _strings(item.get(key), key)
        _relative(item["profile"], "profile")
    return data


def _identity(root: Path, leaf_dir: Path) -> tuple[str, str]:
    path = _within(root, leaf_dir)
    try:
        relative = path.relative_to((root / "src").resolve()).as_posix()
    except ValueError as exc:
        raise SchemaError("publication owner must be under src/<provider>/") from exc
    return _id(relative)


def classify(root: Path, leaf_dir: Path) -> str:
    root = Path(root).resolve()
    _, leaf = _identity(root, Path(leaf_dir))
    for item in registry(root)["types"]:
        if any(fnmatch.fnmatchcase(leaf, pattern) for pattern in item["patterns"]):
            return item["kind"]
    raise SchemaError(f"no registered document genre for {leaf}")


def _definition(root: Path, kind: str) -> dict:
    for item in registry(root)["types"]:
        if item["kind"] == kind:
            return item
    raise SchemaError(f"unknown publication kind {kind!r}")


def _owner(root: Path, provider: str, leaf: str) -> Path:
    base = root / "src" / provider
    for boundary in ("curriculums/ecclesiastical-latin", "/altar-server-guides", "/roman-sanctuary-dictionary"):
        position = leaf.find(boundary)
        if position >= 0:
            return base / leaf[:position + len(boundary)]
    if leaf == "theology/sacraments-at-a-glance":
        return base / "theology/sacraments"
    if leaf.startswith("devotions/novenas/") and leaf.endswith("-daily-prayer"):
        return base / leaf.removesuffix("-daily-prayer")
    return base / leaf


def _component_data(leaf_dir: Path) -> dict:
    path = leaf_dir / "proper-components.toml"
    if not path.is_file():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SchemaError(f"cannot read {path.name}: {exc}") from exc
    if data.get("schema") not in (1, 2):
        raise SchemaError("proper-components.toml has an unsupported schema")
    return data


def _expected_outputs(root: Path, provider: str, leaf: str) -> list[dict]:
    leaf_dir = root / "src" / provider / leaf
    components = _component_data(leaf_dir)
    metadata = leaf_dir / "generation-metadata.tex"
    inherited = bool(metadata.is_file() and INHERIT_RE.search(metadata.read_text(encoding="utf-8")))
    result = [{"id": f"{provider}/{leaf}", "role": "canonical", "entrypoint": "main.tex",
               "derivation": "projection" if inherited else "authored"}]
    if components:
        result.append({"id": f"{provider}/{leaf}-synthesis", "role": "synthesis",
                       "entrypoint": components.get("synthesis_entrypoint", "synthesis.tex"),
                       "derivation": "authored" if components["schema"] == 2 else "projection"})
        if components["schema"] == 2:
            result.append({"id": f"{provider}/{leaf}-homily", "role": "homily",
                           "entrypoint": components.get("homily_entrypoint", "homily.tex"),
                           "derivation": "authored"})
    return result


def _find_role(root: Path, leaf_dir: Path, owner: Path, role: str) -> list[dict]:
    for base in dict.fromkeys((leaf_dir, owner)):
        for candidate in ROLE_PATHS.get(role, []):
            pattern = (base.relative_to(root) / candidate).as_posix()
            if _paths(root, pattern, must_exist=False):
                if base == leaf_dir:
                    return [{"role": role, "source": candidate}]
                return [{"role": role, "data": pattern}]
    return []


def adapter_manifest(root: Path, leaf_dir: Path) -> dict:
    """Propose declarations of existing files; never fabricate missing research."""
    root = Path(root).resolve()
    leaf_dir = Path(leaf_dir)
    if not leaf_dir.is_absolute():
        leaf_dir = root / leaf_dir
    provider, leaf = _identity(root, leaf_dir)
    kind = classify(root, leaf_dir)
    definition = _definition(root, kind)
    owner = _owner(root, provider, leaf)
    data = {"schema_version": 1, "id": f"{provider}/{leaf}", "kind": kind,
            "profile": definition["profile"],
            "source_format": "structured" if kind == "pictorial-dictionary" else "latex",
            "entrypoint": "main.tex", "outputs": _expected_outputs(root, provider, leaf),
            "structure": [{"role": "body", "source": "main.tex", "outputs": ["canonical"]}]}
    for role, name in (("generation", "generation-metadata.tex"), ("web-declaration", "web-edition.toml")):
        if (leaf_dir / name).is_file():
            data["structure"].append({"role": role, "source": name})
    roles = list(dict.fromkeys(definition["required_roles"] + ["proper-components", "chronology-record", "chronology-projection", "interpretations"]))
    for role in roles:
        data["structure"].extend(_find_role(root, leaf_dir, owner, role))
    metadata = leaf_dir / "generation-metadata.tex"
    inherited = INHERIT_RE.search(metadata.read_text(encoding="utf-8")) if metadata.is_file() else None
    if inherited:
        data["canonical_owner"] = f"{provider}/{inherited.group(1)}"
    component_data = _component_data(leaf_dir)
    if component_data:
        data["contracts"] = {"component_schema": component_data["schema"]}
        for key in CONTRACT_FIELDS - {"component_schema"}:
            if key in component_data:
                data["contracts"][key] = component_data[key]
    return data


def _structure_paths(root: Path, record: dict, item: dict) -> list[Path]:
    if "source" in item:
        pattern = f"{record['source_dir']}/{item['source']}"
    else:
        pattern = item["data"]
    paths = _paths(root, pattern)
    leaf_dir = (root / record["source_dir"]).resolve()
    other = {p for p in PROVIDERS if p != record["provider"]}
    for path in paths:
        resolved = _within(root, path)
        if "source" in item and not resolved.is_relative_to(leaf_dir):
            raise SchemaError("structure source escapes its owning leaf through a symlink")
        for provider in other:
            if resolved.is_relative_to((root / "src" / provider).resolve()):
                raise SchemaError("structure cannot import another provider through a symlink")
    return paths


def _normalise(root: Path, data: dict, manifest_path: Path | None) -> dict:
    _strict(data, MANIFEST_FIELDS, "publication")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise SchemaError("schema_version must be 1")
    provider, leaf = _id(data.get("id"))
    leaf_dir = root / "src" / provider / leaf
    if manifest_path is not None and manifest_path.resolve().parent != leaf_dir.resolve():
        raise SchemaError("manifest id must match its canonical owning directory")
    kind = _string(data.get("kind"), "kind")
    definition = _definition(root, kind)
    if classify(root, leaf_dir) != kind:
        raise SchemaError("kind disagrees with the registered genre of its owning path")
    if data.get("profile") != definition["profile"]:
        raise SchemaError("profile must be the registered owning profile")
    source_format = data.get("source_format")
    if source_format not in {"latex", "structured", "markdown"}:
        raise SchemaError("source_format must be latex, structured or markdown")
    entrypoint = _relative(data.get("entrypoint"), "entrypoint")
    if source_format == "markdown" and not entrypoint.endswith(".md"):
        raise SchemaError("markdown entrypoint must have .md extension")
    if source_format == "latex" and not entrypoint.endswith(".tex"):
        raise SchemaError("latex entrypoint must have .tex extension")
    result = dict(data, provider=provider, leaf=leaf, source_dir=f"src/{provider}/{leaf}",
                  manifest_path=manifest_path.relative_to(root).as_posix() if manifest_path else None,
                  manifest_origin="declared" if manifest_path else "adapter",
                  profile_definition=definition)
    if "document" in data:
        # A [document] table opts the leaf into a document type; its own
        # module owns the declaration's rules (guidance/document-schemas.md).
        import _document_types  # noqa: PLC0415

        try:
            _document_types.declaration(root, leaf_dir)
        except _document_types.DocumentTypeError as exc:
            raise SchemaError(f"document type: {exc}") from exc
    if not isinstance(data.get("outputs"), list) or not data["outputs"]:
        raise SchemaError("outputs must be a nonempty array of tables")
    result["outputs"] = []
    roles = set()
    ids = set()
    for output in data["outputs"]:
        _strict(output, OUTPUT_FIELDS, "output")
        _id(output.get("id"))
        role = output.get("role")
        if role not in OUTPUT_ROLES or role in roles or output["id"] in ids:
            raise SchemaError("output roles and ids must be known and unique")
        roles.add(role)
        ids.add(output["id"])
        expected_id = data["id"] + ("" if role == "canonical" else f"-{role}")
        if output["id"] != expected_id:
            raise SchemaError(f"{role} output id must be {expected_id}")
        path = _relative(output.get("entrypoint"), "output entrypoint")
        if output.get("derivation") not in {"authored", "projection"}:
            raise SchemaError("output derivation must be authored or projection")
        result["outputs"].append(dict(output, source_path=f"{result['source_dir']}/{path}"))
    canonical = next((o for o in result["outputs"] if o["role"] == "canonical"), None)
    if canonical is None or canonical["entrypoint"] != entrypoint:
        raise SchemaError("exactly one canonical output must use the declared entrypoint")
    if source_format in {"latex", "structured"}:
        expected = _expected_outputs(root, provider, leaf)
        if [{k: o[k] for k in OUTPUT_FIELDS} for o in result["outputs"]] != expected:
            raise SchemaError("outputs or authored/projection distinctions disagree with the canonical source contracts")
    structure = data.get("structure")
    if not isinstance(structure, list) or not structure:
        raise SchemaError("structure must be a nonempty array of tables")
    body = [item for item in structure if isinstance(item, dict) and item.get("role") == "body"]
    if len(body) != 1 or body[0].get("source") != entrypoint:
        raise SchemaError("structure must declare one canonical body at its exact entrypoint")
    nodes = {}
    for index, item in enumerate(structure):
        _strict(item, STRUCTURE_FIELDS, "structure")
        role = _string(item.get("role"), "structure role")
        if not KEY.fullmatch(role):
            raise SchemaError("structure role must be lowercase kebab-case")
        if ("source" in item) == ("data" in item):
            raise SchemaError("structure requires exactly one source or data path")
        if "source" in item:
            _relative(item["source"], "structure source", glob=True)
        if "data" in item:
            _relative(item["data"], "structure data", glob=True)
            if not item["data"].startswith("src/"):
                raise SchemaError("structure data must belong beneath src/")
            if item["data"].startswith(tuple(f"src/{p}/" for p in PROVIDERS if p != provider)):
                raise SchemaError("structure cannot import another provider's authored substance")
        key = item.get("key", f"{role}-{index + 1}")
        if not KEY.fullmatch(_string(key, "structure key")) or key in nodes:
            raise SchemaError("structure keys must be kebab-case and unique")
        selected = _strings(item.get("outputs", list(roles)), "structure outputs")
        if not selected or set(selected) - roles:
            raise SchemaError("structure outputs must name existing output roles")
        nodes[key] = _strings(item.get("depends_on", []), "structure depends_on")
        _structure_paths(root, result, item)
    _acyclic(nodes, "structure")
    for field in ("content_inputs", "evidence_inputs", "render_inputs"):
        for pattern in _strings(data.get(field, []), field):
            _relative(pattern, field, glob=True)
            if pattern.split("/", 1)[0] in {".git", ".scratch", "build", "pdf", "web"}:
                raise SchemaError(f"{field} must name canonical repository inputs")
            for path in _paths(root, pattern):
                if field != "evidence_inputs":
                    _provider_input(root, path, provider)
                if field == "evidence_inputs" and not _metadata_path(path, root):
                    raise SchemaError("evidence_inputs name metadata, never external witness payloads")
    contracts = data.get("contracts", {})
    _strict(contracts, CONTRACT_FIELDS, "contracts")
    components = _component_data(leaf_dir)
    for key, value in contracts.items():
        if key == "component_schema":
            if type(value) is not int or value not in (1, 2):
                raise SchemaError("component_schema must be integer 1 or 2")
        else:
            _string(value, f"contract {key}")
        actual = components.get("schema" if key == "component_schema" else key)
        if actual != value:
            raise SchemaError(f"contract {key} disagrees with proper-components.toml")
    if components and contracts.get("component_schema") != components["schema"]:
        raise SchemaError("contracts must preserve the existing component schema")
    if components:
        for key in CONTRACT_FIELDS - {"component_schema"}:
            if key in components and contracts.get(key) != components[key]:
                raise SchemaError(f"contracts must preserve the existing {key}")
    if "canonical_owner" in data:
        owner_provider, _ = _id(data["canonical_owner"])
        if owner_provider != provider or data["canonical_owner"] == data["id"]:
            raise SchemaError("canonical_owner must name another same-provider publication")
        _paths(root, f"src/{data['canonical_owner']}/main.tex")
    metadata = leaf_dir / "generation-metadata.tex"
    inherited = INHERIT_RE.search(metadata.read_text(encoding="utf-8")) if metadata.is_file() else None
    expected_owner = f"{provider}/{inherited.group(1)}" if inherited else None
    if data.get("canonical_owner") != expected_owner:
        raise SchemaError("canonical_owner must preserve the exact existing generation inheritance")
    _inheritance_cycle(root, data["id"])
    for output in result["outputs"]:
        for path in _paths(root, output["source_path"]):
            if not path.resolve().is_relative_to(leaf_dir.resolve()):
                raise SchemaError("output entrypoint escapes its owning leaf through a symlink")
    return result


def _acyclic(nodes: dict[str, list[str]], label: str) -> None:
    visited, active = set(), set()

    def visit(key):
        if key not in nodes:
            raise SchemaError(f"{label} dependency names unknown key {key}")
        if key in active:
            raise SchemaError(f"{label} dependency cycle at {key}")
        if key in visited:
            return
        active.add(key)
        for dependency in nodes[key]:
            visit(dependency)
        active.remove(key)
        visited.add(key)
    for key in nodes:
        visit(key)


def load_manifest(root: Path, path: Path) -> dict:
    root = Path(root).resolve()
    path = Path(path)
    if not path.is_absolute():
        path = root / path
    _within(root, path)
    if path.name != MANIFEST:
        raise SchemaError(f"publication manifest must be named {MANIFEST}")
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SchemaError(f"cannot read {path.relative_to(root)}: {exc}") from exc
    return _normalise(root, data, path)


def discover(root: Path = ROOT) -> list[dict]:
    """All main.tex leaves, including invalid/missing declarations as records."""
    root = Path(root).resolve()
    records = []
    for provider in PROVIDERS:
        for main in sorted((root / "src" / provider).rglob("main.tex")):
            manifest = main.parent / MANIFEST
            try:
                record = load_manifest(root, manifest) if manifest.is_file() else _normalise(
                    root, adapter_manifest(root, main.parent), None)
            except (SchemaError, OSError, UnicodeError) as exc:
                leaf = main.parent.relative_to(root / "src" / provider).as_posix()
                record = {"id": f"{provider}/{leaf}", "provider": provider, "leaf": leaf,
                          "source_dir": main.parent.relative_to(root).as_posix(),
                          "manifest_path": manifest.relative_to(root).as_posix() if manifest.exists() else None,
                          "manifest_origin": "declared" if manifest.exists() else "adapter",
                          "outputs": [], "discovery_error": str(exc)}
            records.append(record)
    # Orphan manifests are findings, never an excuse to change the source census.
    known = {r["manifest_path"] for r in records}
    for provider in PROVIDERS:
        for manifest in sorted((root / "src" / provider).rglob(MANIFEST)):
            relative = manifest.relative_to(root).as_posix()
            if relative not in known:
                leaf = manifest.parent.relative_to(root / "src" / provider).as_posix()
                try:
                    future = load_manifest(root, manifest)
                    if future["source_format"] != "markdown":
                        raise SchemaError("orphan manifest has no canonical main.tex source")
                    records.append(future)
                except (SchemaError, OSError, UnicodeError) as exc:
                    records.append({"id": f"{provider}/{leaf}", "provider": provider, "leaf": leaf,
                                    "source_dir": manifest.parent.relative_to(root).as_posix(),
                                    "manifest_path": relative, "manifest_origin": "declared", "outputs": [],
                                    "discovery_error": f"orphan or invalid manifest: {exc}"})
    return sorted(records, key=lambda r: r["id"])


def _raw_manifest(data: dict) -> dict:
    raw = {k: v for k, v in data.items() if k not in DERIVED_FIELDS}
    if isinstance(raw.get("outputs"), list):
        raw["outputs"] = [{k: v for k, v in item.items() if k != "source_path"}
                          if isinstance(item, dict) else item for item in raw["outputs"]]
    return raw


def dumps_manifest(data: dict) -> str:
    """Serialize only canonical manifest fields, with deterministic ordering."""
    raw = _raw_manifest(data)
    _strict(raw, MANIFEST_FIELDS, "publication")
    lines = []
    scalar_keys = ("schema_version", "id", "kind", "profile", "source_format", "entrypoint", "canonical_owner")
    for key in scalar_keys + ("content_inputs", "evidence_inputs", "render_inputs"):
        if key in raw:
            lines.append(f"{key} = {json.dumps(raw[key], ensure_ascii=False)}")
    if raw.get("contracts"):
        lines += ["", "[contracts]"]
        lines += [f"{k} = {json.dumps(v, ensure_ascii=False)}" for k, v in sorted(raw["contracts"].items())]
    for table, fields in (("outputs", OUTPUT_FIELDS), ("structure", STRUCTURE_FIELDS)):
        for item in raw.get(table, []):
            _strict(item, fields, table)
            lines += ["", f"[[{table}]]"]
            for key, value in item.items():
                if key in fields:
                    lines.append(f"{key} = {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


def _source_files(root: Path, base: Path, *, evidence: bool) -> set[Path]:
    result = set()
    if not base.exists():
        return result
    for path in base.rglob("*"):
        if not path.is_file() or any(p in {".scratch", "__pycache__"} for p in path.relative_to(base).parts):
            continue
        parts = set(path.relative_to(base).parts[:-1])
        if parts & {"evaluations", "evaluation"}:
            continue  # Historical run archives do not define the current work.
        if evidence and path.name in OPERATIONAL_RECORDS:
            continue  # Acceptance/install bookkeeping cannot change its own seal.
        audit = bool(parts & AUDIT_DIRS)
        if audit != evidence:
            continue
        if evidence and (path.suffix not in TEXT_SUFFIXES or "artifacts" in path.parts):
            continue
        _within(root, path)
        if path.name != MANIFEST:
            result.add(path)
    return result


def _literal_closure(root: Path, record: dict) -> tuple[set[Path], list[str]]:
    """Conservative literal edges only; computed TeX is explicitly unproven."""
    files, pending, graph, unresolved = set(), [], {}, []
    for output in record["outputs"]:
        pending.append(root / output["source_path"])
    bases = (root / "src" / record["provider"], root / "src")
    while pending:
        path = pending.pop()
        if path in files:
            continue
        _within(root, path)
        _provider_input(root, path, record["provider"])
        files.add(path)
        graph[path.as_posix()] = []
        if path.suffix not in {".tex", ".sty", ".cls"}:
            continue
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
        for argument in INPUT_RE.findall(text):
            if "\\" in argument or "#" in argument:
                unresolved.append(f"{path.relative_to(root)}: computed input {argument}")
                continue
            _relative(argument.strip(), "literal TeX input")
            target = None
            for base in (path.parent,) + bases:
                for candidate in (base / argument, base / f"{argument}.tex"):
                    if candidate.is_file():
                        target = _within(root, candidate)
                        break
                if target:
                    break
            if target:
                graph[path.as_posix()].append(target.as_posix())
                pending.append(target)
            else:
                raise SchemaError(f"{path.relative_to(root)}: unresolved literal input {argument}")
    _acyclic(graph, "literal TeX source")
    return files, sorted(set(unresolved))


def _file_hash(path: Path) -> bytes:
    # One publication operation may consume the same artwork or preamble in
    # hundreds of outputs. Reuse only while the file's identity/stats agree;
    # a concurrent write invalidates the cache and cannot create a mixed seal.
    for _ in range(3):
        before = path.stat()
        signature = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
        held = _FILE_HASHES.get(path)
        if held and held[0] == signature:
            return held[1]
        digest = hashlib.sha256(path.read_bytes()).digest()
        after = path.stat()
        if signature == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            _FILE_HASHES[path] = (signature, digest)
            return digest
    raise SchemaError(f"source changed while its identity was being read: {path.name}")


def _digest(root: Path, paths: set[Path], declaration=None) -> dict:
    digest = hashlib.sha256()
    if declaration is not None:
        digest.update(json.dumps(declaration, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\0")
    names = []
    for path in sorted(paths, key=lambda p: p.relative_to(root).as_posix()):
        name = path.relative_to(root).as_posix()
        names.append(name)
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(_file_hash(path))
    return {"sha256": digest.hexdigest(), "inputs": names}


def _source_module():
    global _SOURCE_MODULE
    if _SOURCE_MODULE is None:
        loader = importlib.machinery.SourceFileLoader("_document_schema_source_library", str(ROOT / "tools/source-library"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[loader.name] = module
        loader.exec_module(module)
        _SOURCE_MODULE = module
    return _SOURCE_MODULE


def _source_index(root: Path, *, refresh: bool = False) -> dict[str, Path]:
    if root not in _SOURCE_INDEX or refresh:
        module = _source_module()
        library = module.Library(root, root / "src/sources", [])
        # This reads source manifests only. load_library's retained-text checks,
        # artifact resolution, disk caches and hydration are deliberately unused.
        module._load_source_records(library)
        if any("duplicate id" in error for error in library.errors):
            raise SchemaError("source metadata has duplicate identities")
        _SOURCE_INDEX[root] = {key: value.path for key, value in library.records.items()}
    return _SOURCE_INDEX[root]


def _evidence_ancestry(root: Path, evidence: set[Path], *, source_ids=()) -> set[Path]:
    """Follow declared owners and source-library ancestry, without payload IO."""
    evidence = {p for p in evidence if p.name not in OPERATIONAL_RECORDS}
    result = set(evidence)
    source_ids = set(source_ids)
    pending = list(evidence)
    seen = set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        if path.suffix != ".toml":
            continue
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        if path.name == "source-bindings.toml":
            for binding in data.get("bindings", []):
                if isinstance(binding, dict) and isinstance(binding.get("source_id"), str):
                    source_ids.add(binding["source_id"])
        if path.name == "review-dependencies.toml":
            for pattern in _strings(data.get("paths", []), "review dependencies paths"):
                if not pattern.startswith("src/"):
                    raise SchemaError("review dependencies must remain beneath src/")
                for dependency in _review_dependency_paths(root, pattern):
                    if dependency.name in OPERATIONAL_RECORDS:
                        continue
                    result.add(dependency)
                    pending.append(dependency)
    if not source_ids:
        return result
    module = _source_module()
    index = _source_index(root)
    visited = set()
    active = set()

    def visit(source_id):
        nonlocal index
        if source_id in active:
            raise SchemaError(f"source metadata dependency cycle: {source_id}")
        if source_id in visited:
            return
        if source_id not in index:
            index = _source_index(root, refresh=True)
        if source_id not in index:
            raise SchemaError(f"bound source has no canonical metadata record: {source_id}")
        path = index[source_id]
        _within(root, path)
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        if data.get("id") != source_id:
            raise SchemaError(f"bound source metadata identity changed: {source_id}")
        active.add(source_id)
        result.add(path)
        record = SimpleNamespace(record_type=data.get("record_type"), data=data)
        for dependency in module._dependency_ids(record):
            visit(dependency)
        active.remove(source_id)
        visited.add(source_id)
    for source_id in sorted(source_ids):
        visit(source_id)
    return result


def _review_dependency_paths(root: Path, pattern: str) -> set[Path]:
    """Directory declarations expand to metadata; payload declarations to owners."""
    _relative(pattern, "review dependency", glob=True)
    matches = list(root.glob(pattern)) if any(c in pattern for c in "*?[") else [root / pattern]
    result = set()

    def artifact_owner(path):
        return next((parent / "artifact.toml" for parent in path.parents
                     if parent.is_relative_to(root) and (parent / "artifact.toml").is_file()), None)

    for match in matches:
        _within(root, match)
        if not match.exists():
            owner = artifact_owner(match)
            if owner is not None and match.name not in {"artifact.toml", "edition.toml", "work.toml"}:
                result.add(owner)
                continue
            raise SchemaError(f"review dependency does not exist: {pattern}")
        paths = match.rglob("*") if match.is_dir() else [match]
        for path in paths:
            _within(root, path)
            if not path.is_file():
                continue
            if _metadata_path(path, root):
                result.add(path)
            else:
                # A legacy seal may name an exact lawful text or scan.  Its
                # owner's artifact.toml carries hash/rights identity here;
                # exhaustive byte verification still belongs to its gate.
                owner = artifact_owner(path)
                if owner is not None:
                    result.add(owner)
                elif not match.is_dir():
                    raise SchemaError(f"review payload has no controlling metadata owner: {pattern}")
    if not result:
        raise SchemaError(f"review dependency has no metadata files: {pattern}")
    return result


def evidence_metadata(root: Path, paths, *, source_ids=()) -> set[Path]:
    """Public metadata-only evidence closure, usable before a manifest exists.

    File/directory paths may be repository-relative or absolute beneath root.
    Current source/binding metadata is included; operational review/install
    receipts and external witness payloads are not read or added.
    """
    root = Path(root).resolve()
    initial = set()
    for value in paths:
        path = Path(value)
        relative = _within(root, path if path.is_absolute() else root / path).relative_to(root).as_posix()
        initial.update(p for p in _review_dependency_paths(root, relative)
                       if p.name not in OPERATIONAL_RECORDS and "evaluations" not in p.parts)
    return _evidence_ancestry(root, initial, source_ids=source_ids)


def identities(root: Path, record: dict, *, output: str | None = None) -> dict:
    """Source identities, not a rendered-artifact or witness-byte approval."""
    root = Path(root).resolve()
    if record.get("discovery_error"):
        raise SchemaError(record["discovery_error"])
    leaf_dir = root / record["source_dir"]
    owner = _owner(root, record["provider"], record["leaf"])
    content = _source_files(root, leaf_dir, evidence=False)
    evidence = _source_files(root, leaf_dir, evidence=True)
    profile = root / record["profile"]
    if profile.is_file():
        evidence.add(profile)
    for base in (owner / "shared", owner / "research"):
        if base.name == "research":
            evidence.update(p for p in base.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
                            and p.name not in OPERATIONAL_RECORDS and "evaluations" not in p.parts)
        else:
            content.update(_source_files(root, base, evidence=False))
            evidence.update(_source_files(root, base, evidence=True))
    closure, unresolved = _literal_closure(root, record)
    content.update(closure)
    for item in record["structure"]:
        paths = _structure_paths(root, record, item)
        if item["role"] in ROLE_PATHS and item["role"] not in {"daily-prayers", "sacrament-matrix", "sacrament-lexicon", "sacrament-summaries", "initiation-table", "object-records", "dictionary-selections", "module-selection", "chronology-projection"}:
            evidence.update(paths)
        else:
            content.update(paths)
    render = set(content)
    render_patterns = ["src/common/*.tex", "src/common/*.sty", "scripts/*.py",
                       "scripts/document_schema_checks/*.py",
                       "tools/web-edition", str(REGISTRY), "Makefile"]
    if record["kind"] == "pictorial-dictionary":
        render_patterns.append("tools/render-sanctuary-dictionary")
    for pattern in render_patterns:
        render.update(_paths(root, pattern, must_exist=False))
    for field, target in (("content_inputs", content), ("evidence_inputs", evidence), ("render_inputs", render)):
        for pattern in record.get(field, []):
            target.update(_paths(root, pattern))
    # Metadata asserts witness hashes; identity never hydrates or reads external
    # witness blobs. Exhaustive source-byte validation remains an owning gate.
    evidence = _evidence_ancestry(root, {p for p in evidence if _metadata_path(p, root)})
    declaration = _raw_manifest(record)
    result = {"content": _digest(root, content, declaration),
              "evidence": _digest(root, evidence), "render": _digest(root, render),
              "outputs": {}, "limitations": [
                  "Source identity does not establish semantic or rendered review acceptance.",
                  "Evidence identity covers audit/binding metadata and controlling source-record ancestry, not external witness payload verification.",
              ] + unresolved}
    for item in record["outputs"]:
        if output is not None and item["role"] != output and item["id"] != output:
            continue
        result["outputs"][item["role"]] = _digest(root, set(), {
            "output": {k: v for k, v in item.items() if k in OUTPUT_FIELDS},
            "content": result["content"]["sha256"], "evidence": result["evidence"]["sha256"],
            "render": result["render"]["sha256"],
        })
        result["outputs"][item["role"]]["inputs"] = sorted(set(
            result["content"]["inputs"] + result["evidence"]["inputs"] + result["render"]["inputs"]))
    if output is not None and not result["outputs"]:
        raise SchemaError(f"unknown output {output}")
    return result


def _nonempty(path: Path) -> bool:
    if path.suffix not in TEXT_SUFFIXES:
        return path.stat().st_size > 0
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".tex", ".sty", ".cls"}:
        text = re.sub(r"(?<!\\)%[^\n]*", "", text)
    else:
        text = re.sub(r"(?m)^\s*#.*$", "", text)
    return bool(text.strip())


def _content_checks(root: Path, record: dict) -> list[str]:
    errors = []
    roles = {}
    owner = _owner(root, record["provider"], record["leaf"])
    for item in record["structure"]:
        paths = _structure_paths(root, record, item)
        roles.setdefault(item["role"], set()).update(paths)
        if any(not _nonempty(p) for p in paths):
            errors.append(f"empty content for role {item['role']}")
        if item["role"] in ROLE_PATHS:
            allowed = set()
            for base in dict.fromkeys((root / record["source_dir"], owner)):
                for pattern in ROLE_PATHS[item["role"]]:
                    allowed.update(_paths(root, (base.relative_to(root) / pattern).as_posix(), must_exist=False))
            if not set(paths) <= allowed:
                errors.append(f"role {item['role']} does not reference its actual bounded canonical record")
    required = list(record["profile_definition"]["required_roles"])
    if record.get("contracts", {}).get("component_schema") == 2:
        required += ["proper-components", "interpretations"]
        if record.get("contracts", {}).get("chronology_presentation"):
            required += ["chronology-record", "chronology-projection"]
    counts = {role: sum(item["role"] == role for item in record["structure"]) for role in required}
    for role in required:
        if role not in roles:
            errors.append(f"missing required role: {role}")
        elif counts[role] != 1:
            errors.append(f"required role must have one canonical declaration: {role}")
    if record["kind"] == "novena" and len(roles.get("daily-prayers", set())) != 9:
        errors.append("novena requires exactly nine distinct nonempty canonical day sources")
    if record["kind"] in {"sacraments", "sacraments-summary"}:
        expected = {"baptism", "confirmation", "eucharist", "penance", "anointing", "orders", "matrimony"}
        actual = {p.stem for p in roles.get("sacrament-summaries", set())}
        if actual != expected:
            errors.append("sacramental summaries must name exactly the seven canonical sacraments")
    if record["kind"] == "curriculum-packet":
        paths = roles.get("module-selection", set())
        if paths:
            text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
            match = re.search(r"\\newcommand\{\\ModuleWorksheetVariants\}\{([^{}]+)\}", text)
            if not match or {v.strip() for v in match.group(1).split(",")} != {"A", "B", "C", "D"}:
                errors.append("trunk packet must select all four canonical worksheet variants A,B,C,D")
    kind = record["kind"]
    if kind.startswith("curriculum-"):
        module_name = "curriculum"
    elif kind.startswith(("proper-", "mass-", "server-")) or kind in {"assembly-reference", "calendar-reference", "pictorial-dictionary"}:
        module_name = "liturgy"
    elif kind.startswith("marian-") or kind in {"sacraments", "sacraments-summary", "virtues", "angelology", "heresies"}:
        module_name = "reference"
    else:
        module_name = "prose"
    try:
        checker = importlib.import_module(f"document_schema_checks.{module_name}")
        errors.extend(checker.check(root, record))
    except ModuleNotFoundError as exc:
        errors.append(f"owning source-structure validator is unavailable: {module_name}: {exc}")
    return errors


def gates(root: Path, record: dict, phase: str) -> list[dict]:
    provider, leaf = record["provider"], record["leaf"]
    if phase == "render":
        selected = [(f"generation-{output['role']}", ["tools/check-generation-metadata", "--provider", provider,
                     "--pdf", output["id"].split("/", 1)[1], f"pdf/{output['id']}.pdf"])
                    for output in record["outputs"]]
    else:
        selected = [("generation", ["tools/check-generation-metadata", "--provider", provider, "--document", leaf])]
    if phase != "source":
        for gate in record["profile_definition"].get("gates", []):
            commands = {
                "proper-components": ["tools/check-proper-components", "--root", str(root), "--provider", provider, "--document", leaf, "--phase", "artifacts" if phase == "render" else "content"],
                "proper-content": ["tools/check-content-preflight", "--provider", provider, "--document", leaf],
                "curriculum": ["tools/check-curriculum-structure", "--curriculum-root", f"src/{provider}/curriculums/ecclesiastical-latin", "--sources-only"],
                "dictionary-artwork": ["tools/check-roman-sanctuary-artwork"],
            }
            if gate == "curriculum" and phase == "render":
                stem = f"build/{provider}/{leaf}"
                commands[gate] = ["tools/check-curriculum-structure", "--curriculum-root",
                                  f"src/{provider}/curriculums/ecclesiastical-latin", "--document", leaf,
                                  "--toc", stem + ".toc", "--out", stem + ".out", "--pdf", f"pdf/{provider}/{leaf}.pdf"]
            selected.append((gate, commands[gate]))
    return [{"id": key, "phase": phase, "command": command, "status": "not-run"} for key, command in selected]


def validate(root: Path, record: dict, *, phase: str = "source", run_gates: bool = False,
             require_manifest: bool = True) -> dict:
    root = Path(root).resolve()
    report = {"id": record.get("id"), "phase": phase, "ok": False, "errors": [], "warnings": [], "external_gates": []}
    if phase not in {"source", "content", "render"}:
        raise SchemaError("phase must be source, content or render")
    try:
        if record.get("discovery_error"):
            raise SchemaError(record["discovery_error"])
        raw = _raw_manifest(record)
        path = root / record["manifest_path"] if record.get("manifest_path") else None
        checked = _normalise(root, raw, path)
        if require_manifest and checked["manifest_origin"] != "declared":
            report["errors"].append("missing publication.toml; adapter discovery is not a manifest")
        _literal_closure(root, checked)
        if phase in {"content", "render"}:
            report["errors"].extend(_content_checks(root, checked))
        report["external_gates"] = gates(root, checked, phase)
        if run_gates:
            for gate in report["external_gates"]:
                command = [str(root / gate["command"][0]), *gate["command"][1:]]
                try:
                    completed = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
                    gate.update(status="pass" if completed.returncode == 0 else "fail", exit_code=completed.returncode,
                                output=(completed.stdout + completed.stderr)[-8000:])
                except OSError as exc:
                    gate.update(status="unavailable", output=str(exc))
                if gate["status"] != "pass":
                    report["errors"].append(f"owning gate did not pass: {gate['id']}")
        report["warnings"] += ["Declared semantic roles and machine source checks do not establish source fidelity or specialist/visual acceptance."]
        if any(g["status"] == "not-run" for g in report["external_gates"]):
            report["warnings"].append("Existing owning gates were not run; their acceptance is not implied.")
        report["requirements"] = checked["profile_definition"]["requirements"]
    except (ValueError, OSError, UnicodeError) as exc:
        report["errors"].append(str(exc))
    report["ok"] = not report["errors"]
    return report
