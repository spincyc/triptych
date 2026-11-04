"""Deterministic gates for the three-document proper-study workflow."""

from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.machinery
import importlib.util
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path

from _proper_components import (include_graph, lane_source_paths, validate_liturgical_family,
                                presentation_contract, format_contract, authority_contract,
                                pagination_aux_files, load_manifest)
from _corpus import active_tex, REVISION_RE, CONTRIBUTION_RE, PRODUCTION_RE, INHERITANCE_RE

ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"research": "", "synthesis": "-synthesis", "homily": "-homily"}
RECEIPT = "research/artifacts.json"
# Schema 2 (2026-09-23) stopped digesting the TeX .log; see artifact_state().
RECEIPT_SCHEMA = 2
WEB_RECEIPT = "research/web-artifact.json"
RESEARCH_REVIEW_CONTRACT = "proper-study-v3"
# v4 (selected from proper-study version 8) also seals what v3 names only by
# its code: every file the leaf's chronology computation opens outside the
# leaf, every repository module it compiles, and the source records, ancestry
# and available payloads of every source its answer cites. v3 stays as it was,
# so a review sealed under it verifies as it always did.
CHRONOLOGY_READS_CONTRACT = "proper-study-v4"
# v5 (proper-study version 15) adds the reusable-source handoff. Older seals
# retain their exact shape; neither historical bindings nor verdicts migrate.
SOURCE_DISPOSITIONS_CONTRACT = "proper-study-v5"
RESEARCH_REVIEW_CONTRACTS = (RESEARCH_REVIEW_CONTRACT, CHRONOLOGY_READS_CONTRACT,
                           SOURCE_DISPOSITIONS_CONTRACT)
SOURCE_DISPOSITIONS = "research/source-dispositions.toml"
SOURCE_DISPOSITIONS_SCHEMA = "proper-study-source-dispositions-v1"
SOURCE_ADMISSION_INPUTS = (
    "scripts/_proper_study.py", "scripts/_catena.py", "scripts/_canon.py",
    "scripts/_loci.py", "scripts/_projection.py", "scripts/_psalms.py",
    "tools/source-library", "requirements-tools.txt",
)
# Within the leaf the research seal's own rule decides what is evidence: these
# three directories, which it seals whole. The component manifest is opened by
# the postconciliar adapter only to refuse a disagreement; it is authored after
# research, and its bytes are not an input to the answer.
LEAF_EVIDENCE = ("research", "propers", "instance")
LEAF_AGREEMENT_ONLY = ("proper-components.toml",)
# Computation is a separate seal dimension from the source owners declared by
# research. The workflow digest covers recipes/fragments/schemas, not the code
# those commands execute. Keep this bounded adapter/query dependency list here.
CHRONOLOGY_COMPUTATION_INPUTS = (
    "scripts/_proper_chronology.py", "scripts/_proper_chronology_comparisons.py",
    "scripts/_chronology.py", "scripts/_canon.py",
    "scripts/_loci.py", "scripts/_calendars.py", "scripts/_tooling.py",
    "scripts/_psalms.py", "scripts/_deuterocanon.py", "scripts/_projection.py",
    "scripts/_psalter.py", "scripts/_bible_artifacts.py", "scripts/_bible_editions.py",
    "tools/proper-chronology", "requirements-tools.txt",
)
POSTCONCILIAR_CHRONOLOGY_INPUTS = (
    "scripts/_proper_chronology_inputs.py", "tools/citations",
    "guidance/liturgy/postconciliar-propers-registry.md",
)
REFERENCE_ONLY_RECORDS = (
    "research/context.md", "research/scope.md", "propers/retrieved.txt", "propers/verified.md",
)
REFERENCE_ONLY_DECLARATION = 'appointed_text_completeness = "reference-only"'


def run(root: Path, *arguments: str) -> None:
    result = subprocess.run(arguments, cwd=root, capture_output=True, text=True,
                            check=False, timeout=240)
    if result.returncode:
        raise ValueError((result.stdout + result.stderr).strip() or
                         f"command failed: {' '.join(arguments)}")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity(root: Path, document: str) -> str:
    if any(part in {".", "..", ""} for part in document.split("/")):
        raise ValueError("document must be a canonical relative leaf id")
    if document.startswith("liturgy/roman-rite/1962/propers/"):
        run(root, sys.executable, str(root / "tools/check-proper-identity"),
            "--document", document)
        return "library/traditional-latin-mass.md"
    from _proper_chronology_inputs import registered_target

    registered_target(document, root)
    return "library/novus-ordo-liturgy.md"


def leaf_path(root: Path, provider: str, document: str) -> Path:
    if provider not in {"gpt", "claude"}:
        raise ValueError("provider must be gpt or claude")
    leaf = root / "src" / provider / document
    if not leaf.resolve().is_relative_to(root / "src" / provider):
        raise ValueError("document resolves outside its provider")
    return leaf


def scope(root: Path, provider: str, document: str) -> str:
    catalog = identity(root, document)
    leaf_path(root, provider, document)
    plan = (root / "guidance/liturgy/propers-production-plan.md").read_text()
    needle = f"provider `{provider}`, identity `{document}`."
    if not any(line.startswith("- Authorized ")
               and not line.startswith("- Authorized reference-only ") and needle in line
               for line in plan.splitlines()):
        raise ValueError("production plan has no authorization for this exact provider and identity")
    if "/postconciliar/" in document:
        registry = root / "src" / provider / document.split("/propers/")[0] / "propers/registry"
        if not registry.is_dir():
            raise ValueError("postconciliar edition-locale has no owning registry")
    return catalog


def manifest(leaf: Path) -> dict:
    data = load_manifest(leaf / "proper-components.toml")
    if data.get("schema") != 2:
        raise ValueError("proper-study requires component schema 2; use legacy proper for schema 1")
    return data


def reference_only_contract(root: Path, provider: str, document: str, *,
                            require_manifest: bool) -> None:
    """Bind an explicitly authorized locator-only production to its audit records."""
    leaf = leaf_path(root, provider, document)
    plan = root / "guidance/liturgy/propers-production-plan.md"
    authorization = re.compile(
        r"- Authorized reference-only \d{4}-\d{2}-\d{2}: provider `"
        + re.escape(provider) + r"`, identity `" + re.escape(document) + r"`\.")
    authorized = plan.is_file() and any(
        authorization.fullmatch(line) for line in plan.read_text().splitlines())
    records = {name: (leaf / name).read_text().splitlines() if (leaf / name).is_file() else []
               for name in REFERENCE_ONLY_RECORDS}
    path = leaf / "proper-components.toml"
    data = tomllib.loads(path.read_text()) if path.is_file() else {}
    requested = data.get("appointed_text_completeness") == "reference-only" or any(
        lines and lines[0] == REFERENCE_ONLY_DECLARATION for lines in records.values())
    if not authorized and not requested:
        return
    if not authorized:
        raise ValueError("reference-only requires production-plan authorization for this exact provider and identity")
    if not document.startswith("liturgy/roman-rite/1962/propers/"):
        raise ValueError("reference-only production requires the 1962 proper profile")
    declaration = re.compile(r"appointed_text_completeness\s*=")
    for name, lines in records.items():
        declarations = [line for line in lines if declaration.match(line)]
        if (not lines or lines[0] != REFERENCE_ONLY_DECLARATION
                or declarations != [REFERENCE_ONLY_DECLARATION]):
            raise ValueError(f"reference-only requires one literal first-line declaration in {name}")
    if require_manifest or path.is_file():
        if data.get("schema") != 2 or data.get("appointed_text_completeness") != "reference-only":
            raise ValueError("reference-only requires a matching schema-2 component manifest")


def components(root: Path, provider: str, document: str, phase: str,
               edition: str | None = None) -> None:
    arguments = [sys.executable, str(root / "tools/check-proper-components"),
                 "--root", str(root), "--provider", provider,
                 "--document", document, "--phase", phase]
    if edition:
        arguments.extend(["--edition", edition])
    run(root, *arguments)


def render_inputs(root: Path, provider: str, document: str) -> dict[str, str]:
    paths: set[Path] = set()
    leaf = leaf_path(root, provider, document)
    paths.update(path for path in leaf.rglob("*") if path.suffix in {".tex", ".sty", ".cls", ".bib"})
    paths.add(leaf / "proper-components.toml")
    formatted = format_contract(manifest(leaf))
    for mode, suffix in EDITIONS.items():
        recorder = root / "build" / provider / f"{document}{suffix}.fls"
        if not recorder.is_file():
            raise ValueError(f"missing build recorder: {recorder.relative_to(root)}")
        cwd = root / "src" / provider
        recorded: set[Path] = set()
        for line in recorder.read_text().splitlines():
            if line.startswith("PWD "):
                cwd = Path(line[4:])
            elif line.startswith("INPUT "):
                path = Path(line[6:])
                path = (cwd / path).resolve() if not path.is_absolute() else path.resolve()
                if path.is_relative_to(root / "src") and path.is_file():
                    paths.add(path)
                    recorded.add(path)
        if formatted:
            entry = leaf / ("main.tex" if mode == "research" else mode + ".tex")
            semantic = include_graph(entry, leaf, root / "src" / provider)
            unexpected = sorted(
                path.relative_to(root).as_posix() for path in recorded - semantic
                if path.suffix in {".tex", ".sty", ".cls", ".bib"}
            )
            missing = sorted(path.relative_to(root).as_posix() for path in semantic - recorded)
            if unexpected or missing:
                details = []
                if unexpected:
                    details.append("recorder-only: " + ", ".join(unexpected))
                if missing:
                    details.append("semantic-only: " + ", ".join(missing))
                raise ValueError(f"{mode} recorder disagrees with the semantic source graph ("
                                 + "; ".join(details) + ")")
    for path in paths:
        validate_liturgical_family(leaf, root / "src" / provider, path)
    return {str(path.relative_to(root)): digest(path)
            for path in sorted(paths) if path.is_file()}


def artifact_state(root: Path, provider: str, document: str) -> dict:
    """The build receipt: what snapshot records and the visual seal binds.

    Under the presentation contract, `pagination_evidence` binds the study's
    and the concise edition's .aux graphs. Their zref labels carry the
    physical-page markers that the component gate checks, so the gate judges
    the same marker evidence that accompanied the reviewed PDFs. The .aux holds
    no path or clock, so identical builds give identical bytes in any checkout.

    The TeX .log is still read by the gate, which refuses unsettled references,
    but it is not digested. Schema 1 digested it. That tied a receipt to one
    pdfTeX run in one checkout: the log records the start minute, the TeX
    version, and absolute build and texmf paths wrapped at 79 columns, and its
    memory statistics count characters of those paths. Normalizing the root
    would not remove these. The only part of the log that bears on pagination is
    the settledness check, and that has one value whenever the gate passes, so a
    digest of it would prove nothing.
    """
    files = {}
    for mode, suffix in EDITIONS.items():
        path = root / "build" / provider / f"{document}{suffix}.pdf"
        if not path.is_file():
            raise ValueError(f"missing {mode} PDF: {path.relative_to(root)}")
        files[str(path.relative_to(root))] = digest(path)
    result = {"schema": RECEIPT_SCHEMA, "provider": provider, "document": document,
              "pdfs": files, "render_inputs": render_inputs(root, provider, document)}
    if presentation_contract(manifest(leaf_path(root, provider, document))):
        evidence = set()
        for mode in ("research", "synthesis"):
            base = root / "build" / provider / f"{document}{EDITIONS[mode]}"
            evidence.update(pagination_aux_files(base.with_suffix(".aux")))
        result["pagination_evidence"] = {
            str(path.relative_to(root)): digest(path) for path in sorted(evidence)}
    return result




def bound_evidence(root: Path, bindings: Path, *, metadata_only: bool = False) -> set[Path]:
    """Follow the source library's exact ancestry, including available payloads."""
    ids = [item["source_id"] for item in tomllib.loads(bindings.read_text()).get("bindings", [])]
    return source_evidence(root, ids, metadata_only=metadata_only)


def _source_library(root: Path, *, metadata_only: bool = False):
    loader = importlib.machinery.SourceFileLoader("proper_study_sources", str(ROOT / "tools/source-library"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    library_tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = library_tool
    spec.loader.exec_module(library_tool)
    if metadata_only:
        library = library_tool.Library(root, root / "src/sources", [])
        library_tool._load_source_records(library)
    else:
        library = library_tool.load_library(root, check_binding_fingerprints=False)
    return library_tool, library


def source_evidence(root: Path, ids, role: str = "bound evidence", *,
                    metadata_only: bool = False) -> set[Path]:
    """Source ancestry, with available payloads only for historical print seals."""
    ids = list(ids)
    if not ids:
        return set()
    if metadata_only:
        from _document_schema import evidence_metadata
        return evidence_metadata(root, [], source_ids=ids)
    library_tool, library = _source_library(root, metadata_only=metadata_only)
    paths, visited = set(), set()
    while ids:
        source_id = ids.pop()
        if source_id in visited:
            continue
        visited.add(source_id)
        if source_id not in library.records:
            raise ValueError(f"unregistered {role}: {source_id}")
        record = library.records[source_id]
        paths.add(record.path)
        ids.extend(library_tool._dependency_ids(record))
        payload = record.data.get("path")
        if payload and not metadata_only:
            path = (root / payload).resolve()
            if not path.is_relative_to(root):
                raise ValueError("source payload escapes repository")
            if path.is_file():
                paths.add(path)
            elif record.data.get("storage") == "tracked":
                raise ValueError(f"missing tracked source payload: {payload}")
    return paths


def binding_digest(binding: dict) -> str:
    """Pin the local use as well as the source: role, loci, states and context."""
    if not isinstance(binding, dict):
        raise ValueError("source-bindings.toml requires binding tables")
    try:
        canonical = json.dumps(binding, sort_keys=True, separators=(",", ":"))
    except TypeError as error:
        raise ValueError("source binding values must follow the source-library schema") from error
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def source_admission_computation_inputs(root: Path) -> dict[str, str]:
    return {name: digest(root / name) for name in SOURCE_ADMISSION_INPUTS}


def source_dispositions(root: Path, provider: str, document: str, *,
                        metadata_only: bool = False) -> set[Path]:
    """Reconcile research bindings with reusable holdings and fragment admission.

    This is a workflow contract, not an extension of the frozen source schemas.
    An inspected artifact is L2 evidence; only the Catena owner's validated
    passage/Scripture edge establishes L3. Deferred rows are the durable queue,
    with stable keys, exact witness pins and the concrete criteria still missing.
    """
    leaf = leaf_path(root, provider, document)
    path = leaf / SOURCE_DISPOSITIONS
    if not path.is_file():
        raise ValueError(f"missing reusable-source handoff: {SOURCE_DISPOSITIONS}")
    data = tomllib.loads(path.read_text())
    if (set(data) != {"schema", "contract", "document", "numbering", "sources"}
            or type(data.get("schema")) is not int or data["schema"] != 1
            or data.get("contract") != SOURCE_DISPOSITIONS_SCHEMA
            or data.get("document") != document or data.get("numbering") != "vulgate"
            or not isinstance(data.get("sources"), list)):
        raise ValueError(f"{SOURCE_DISPOSITIONS} requires schema 1, contract "
                         f"{SOURCE_DISPOSITIONS_SCHEMA}, this document, vulgate numbering and sources[]")
    binding_path = leaf / "research/source-bindings.toml"
    bindings = tomllib.loads(binding_path.read_text()).get("bindings", [])
    if not isinstance(bindings, list):
        raise ValueError("source-bindings.toml requires bindings[]")
    library_tool, library = _source_library(root, metadata_only=metadata_only)
    covered, keys, admitted, paths = set(), set(), set(), set()
    ceilings = None
    evidence_ids = set()
    required = {"id", "binding_index", "binding_sha256", "source_id", "locus", "relationship", "disposition", "reason"}
    allowed = required | {"source_fingerprint", "passage_ids", "scripture_extents", "missing_criteria"}
    commentary = {"direct-exegesis", "analogue", "doctrinal-illumination", "liturgical-commentary"}

    def strings(value) -> bool:
        return isinstance(value, list) and all(isinstance(one, str) and one.strip() for one in value)

    def ancestry(identifier: str) -> set[str]:
        pending, found = [identifier], set()
        while pending:
            current = pending.pop()
            if current not in found:
                if current not in library.records:
                    raise ValueError(f"unregistered reusable-source evidence: {current}")
                found.add(current)
                pending.extend(library_tool._dependency_ids(library.records[current]))
        return found

    def canonical_evidence(extent) -> None:
        # These exact canonical bytes bound candidate and admitted Scripture
        # endpoints, including analogues outside this leaf's appointments.
        paths.update(path for path in (root / "src/sources/works").glob(
            "*/*/editions/*/artifacts/book-index-*/book-index.tsv")
                     if "vulgata-clementina" in path.as_posix())
        for chapter in (extent.first_chapter, extent.last_chapter):
            path = root / _catena.BIBLES_RELATIVE / _catena.CANONICAL_BIBLE / "chapters" / extent.token / f"{chapter}.json"
            if path.is_file():
                paths.add(path)

    for ordinal, item in enumerate(data["sources"], 1):
        label = f"{SOURCE_DISPOSITIONS}: sources[{ordinal}]"
        if not isinstance(item, dict) or not required <= set(item) or set(item) - allowed:
            raise ValueError(f"{label} has missing or unknown fields")
        if any(not isinstance(item[name], str) or not item[name].strip()
               for name in required - {"binding_index"}):
            raise ValueError(f"{label} requires nonempty string identity, locus, relationship, disposition and reason")
        key = item["id"]
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) or key in keys:
            raise ValueError(f"{label} requires a unique stable kebab-case id")
        keys.add(key)
        index = item["binding_index"]
        if type(index) is not int or not 1 <= index <= len(bindings):
            raise ValueError(f"{label} binding_index must name an existing one-based binding")
        binding = bindings[index - 1]
        if item["binding_sha256"] != binding_digest(binding):
            raise ValueError(f"{label} binding_sha256 disagrees with bindings[{index}]; "
                             "reconcile the changed role, loci, states and context")
        source_id = item["source_id"]
        if source_id != binding.get("source_id"):
            raise ValueError(f"{label} source_id disagrees with bindings[{index}]")
        covered.add(index)
        relationship, disposition = item["relationship"], item["disposition"]
        if relationship not in commentary | {"not-commentary", "lead"}:
            raise ValueError(f"{label} has an unknown Scripture relationship")
        if disposition not in {"admitted", "deferred", "rejected", "not-commentary", "lead"}:
            raise ValueError(f"{label} has an unknown admission disposition")
        if not strings(binding.get("states", [])):
            raise ValueError(f"{label} binding states must be a string list")
        states = set(binding.get("states", []))
        record = library.records.get(source_id)
        if record is None:
            raise ValueError(f"{label} names an unregistered source: {source_id}")
        passages, extents, missing = (item.get(name, []) for name in
                                      ("passage_ids", "scripture_extents", "missing_criteria"))
        if not strings(passages) or not strings(missing) or not isinstance(extents, list):
            raise ValueError(f"{label} passage_ids/missing_criteria must be string lists and scripture_extents an array")
        if disposition == "lead":
            if (relationship != "lead" or binding.get("role") != "lead"
                    or states - {"cataloged"} or item.get("source_fingerprint") is not None
                    or passages or extents or missing):
                raise ValueError(f"{label} lead requires an explicitly uninspected, catalog-only lead binding")
            continue
        if relationship == "lead" or binding.get("role") == "lead":
            raise ValueError(f"{label} cannot turn an uninspected lead into used evidence")
        exact = library_tool._exact_artifacts(library, record)
        if (record.record_type not in {"artifact", "segment", "passage", "corpus"}
                or not exact or any(not re.fullmatch(r"[0-9a-f]{64}", str(one.data.get("sha256", "")))
                                    for one in exact)):
            raise ValueError(f"{label} used evidence requires an exact hashed artifact, segment, passage or corpus; "
                             "catalog-only bibliography is a lead")
        if not states & {"acquired", "searched", "inspected", "verified"}:
            raise ValueError(f"{label} used evidence cannot remain catalog-only")
        if (binding.get("role") in {"direct-witness", "reception"} or relationship in commentary) and not states & {"inspected", "verified"}:
            raise ValueError(f"{label} claim-carrying witness requires actual inspection")
        fingerprint = library_tool.source_fingerprint(library, source_id)
        if binding.get("source_fingerprint") != fingerprint or item.get("source_fingerprint") != fingerprint:
            raise ValueError(f"{label} requires the current reviewed binding source_fingerprint; reread changed evidence")
        evidence_ids.add(source_id)
        if disposition == "not-commentary":
            if relationship != "not-commentary" or passages or extents or missing:
                raise ValueError(f"{label} not-commentary requires that relationship and no fragment claims")
            continue
        if relationship not in commentary:
            raise ValueError(f"{label} commentary admission requires its actual Scripture relationship")
        import _catena
        if disposition in {"deferred", "rejected"}:
            if not missing or passages or not extents and "scripture-extent" not in missing:
                raise ValueError(f"{label} deferred/rejected commentary requires concrete missing_criteria and "
                                 "canonical scripture_extents (or scripture-extent explicitly unresolved)")
            if extents and ceilings is None:
                ceilings = _catena._chapter_ceiling(root)
            for value in extents:
                extent = _catena._extent(value)
                if (extent is None or not isinstance(value["token"], str)
                        or any(type(value[name]) is not int for name in _catena.EXTENT_FIELDS - {"token"})):
                    raise ValueError(f"{label} has a malformed canonical Scripture extent")
                errors = _catena._extent_errors(root, label, extent, ceilings)
                if errors:
                    raise ValueError("\n".join(errors))
                canonical_evidence(extent)
            continue
        if not passages or extents or missing:
            raise ValueError(f"{label} admitted requires passage_ids; Scripture extents derive only from the canonical edge")
        parent_ids = {one.record_id for one in exact} if record.record_type == "corpus" else {source_id}
        for passage_id in passages:
            passage = library.records.get(passage_id)
            if passage is None or passage.record_type != "passage":
                raise ValueError(f"{label} admission requires an existing passage: {passage_id}")
            if not parent_ids & ancestry(passage_id):
                raise ValueError(f"{label} admitted passage is not controlled by its bound witness: {passage_id}")
            if "verified" not in passage.data.get("states", []):
                raise ValueError(f"{label} admitted passage has not been verified: {passage_id}")
            admitted.add(passage_id)
    omitted = sorted(set(range(1, len(bindings) + 1)) - covered)
    if omitted:
        raise ValueError(f"{SOURCE_DISPOSITIONS} omits source bindings: {omitted}")
    paths.update(source_evidence(root, evidence_ids | admitted, "reusable-source evidence",
                                 metadata_only=metadata_only))
    if admitted:
        import _catena
        edges = _catena.load_edges(root)
        mapped = {item.get("passage_id") for item in edges.get("fragments", []) if isinstance(item, dict)}
        if admitted - mapped:
            raise ValueError("admitted passages lack a canonical Scripture edge: " + ", ".join(sorted(admitted - mapped)))
        errors = _catena.validate(root)
        if errors:
            raise ValueError("Catena admission failed:\n" + "\n".join(errors))
        selected = [item for item in edges["fragments"] if item["passage_id"] in admitted]
        # Anthology passages can name a constituent work outside their source
        # controller's ancestry. Its attribution, language and date also count.
        paths.update(source_evidence(root, {item["work_id"] for item in selected}, "admitted commentary work",
                                     metadata_only=metadata_only))
        for item in selected:
            canonical_evidence(_catena._extent(item["extent"]))
        paths.update(root / name for name in (_catena.EDGES_RELATIVE, _catena.ALIASES_RELATIVE,
                                             _catena.ABSENCES_RELATIVE) if (root / name).is_file())
    relevant = {str(one.relative_to(root)) + ": " for one in paths | {binding_path}}
    errors = [error for error in library.errors if any(error.startswith(prefix) for prefix in relevant)]
    if errors:
        raise ValueError("invalid reusable-source evidence:\n" + "\n".join(errors))
    return paths


def research_dependencies(root: Path, provider: str, document: str, *,
                          metadata_only: bool = False) -> set[Path]:
    leaf = leaf_path(root, provider, document)
    record = leaf / "research/review-dependencies.toml"
    declared = tomllib.loads(record.read_text()).get("paths")
    if not isinstance(declared, list) or any(not isinstance(item, str) for item in declared):
        raise ValueError("research/review-dependencies.toml requires paths = [repository-relative evidence paths]")
    canonical_owner = (postconciliar_shared_owner(root, provider, document)
                       if "/postconciliar/" in document else None)
    paths, shared_owner = set(), False
    for name in declared:
        path = root / name
        if Path(name).is_absolute() or ".." in Path(name).parts or (not metadata_only and not path.exists()):
            raise ValueError(f"unsafe or missing evidence dependency: {name}")
        validate_liturgical_family(leaf, root / "src" / provider, path)
        if not path.resolve().is_relative_to(root / "src"):
            raise ValueError("evidence dependencies must name tracked source owners under src/")
        resolved = path.resolve()
        if canonical_owner is not None and (resolved == canonical_owner
                                             or resolved.is_relative_to(canonical_owner)):
            shared_owner = True
        if metadata_only:
            from _document_schema import evidence_metadata
            selected = evidence_metadata(root, [path])
        else:
            selected = [path] if path.is_file() else [item for item in path.rglob("*") if item.is_file()]
        if not selected:
            raise ValueError(f"empty evidence dependency: {name}")
        for item in selected:
            validate_liturgical_family(leaf, root / "src" / provider, item)
        paths.update(selected)
    if "/postconciliar/" in document and not shared_owner:
        raise ValueError("postconciliar research must bind its edition's canonical shared Missal formulary owner")
    return paths


def postconciliar_shared_owner(root: Path, provider: str, document: str) -> Path:
    """Resolve one exact edition owner from the target's edition registry row."""
    parts = Path(document).parts
    if (len(parts) != 7 or parts[:3] != ("liturgy", "roman-rite", "postconciliar")
            or parts[4] != "propers" or parts[5] not in {"temporal", "general-calendar"}):
        raise ValueError("postconciliar document must identify one edition and formulary family")
    edition_root = root / "src" / provider / Path(*parts[:5])
    registry = edition_root / "registry/formula-dispositions.md"
    if not registry.is_file():
        raise ValueError("postconciliar edition has no formula-dispositions registry")
    slug = parts[6]
    lines = registry.read_text().splitlines()

    def cells(line: str) -> list[str]:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            return []
        return [cell.strip() for cell in stripped[1:-1].split("|")]

    rows = []
    for index, line in enumerate(lines[:-1]):
        header = cells(line)
        normalized = [re.sub(r"[*_`]", "", cell).strip().casefold()
                      for cell in header]
        if normalized.count("full publication slug") != 1:
            continue
        separator = cells(lines[index + 1])
        if (len(separator) != len(header)
                or any(re.fullmatch(r":?-{3,}:?", cell) is None for cell in separator)):
            continue
        slug_column = normalized.index("full publication slug")
        for row_line in lines[index + 2:]:
            row = cells(row_line)
            if not row:
                break
            if len(row) == len(header) and row[slug_column] == f"`{slug}`":
                rows.append(row_line)
    if len(rows) != 1:
        raise ValueError(
            "postconciliar formula-dispositions registry must contain one exact target slug row")
    candidates = set()
    for row in rows:
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", row):
            resolved = (registry.parent / target).resolve()
            if "/shared/" in resolved.as_posix() and resolved.name == "verified.md":
                candidates.add(resolved)
    if len(candidates) != 1:
        raise ValueError(
            "postconciliar formula-dispositions registry must name one exact canonical shared owner")
    record = candidates.pop()
    if record.parent.name != "propers":
        raise ValueError("canonical shared owner must end in propers/verified.md")
    owner = record.parent.parent
    family_root = (edition_root / parts[5] / "shared").resolve()
    if not owner.is_relative_to(family_root):
        raise ValueError("canonical shared owner is outside the target formulary family")
    relative = owner.relative_to(family_root).parts
    if parts[5] == "general-calendar":
        valid = len(relative) == 2 and relative[0] == "formularies"
    else:
        valid = ((len(relative) == 2 and relative[0] == "formularies")
                 or (len(relative) == 3 and relative[:2] == ("ordinary-time", "weeks")
                     and re.fullmatch(r"\d{2}", relative[2]) is not None))
    if not valid:
        raise ValueError("canonical shared owner has no registry-authorized layout")
    if not record.is_file():
        raise ValueError(f"missing canonical shared owner: {record.relative_to(root)}")
    return owner


def chronology_computation_inputs(root: Path, provider: str, document: str) -> dict[str, str]:
    """Computation inputs for explicitly requested v3 research review.

    The corpus, concordance data, appointment witnesses and rights records are
    still research evidence and must be declared by their source owners. This
    catches changed query/adapter logic and the stable PC identity registry even
    when regeneration happens to produce the same numerical dates.
    """
    leaf_path(root, provider, document)
    names = CHRONOLOGY_COMPUTATION_INPUTS
    if "/postconciliar/" in document:
        names += POSTCONCILIAR_CHRONOLOGY_INPUTS
    return {name: digest(root / name) for name in sorted(names)}


def chronology_reads(root: Path, provider: str, document: str) -> tuple[set[Path], dict[str, str], list[str]]:
    """What the leaf's chronology computation reads, compiles and cites, for a v4 seal.

    The files are read off the computation itself by
    `_proper_chronology.computation_reads`, never listed here. A file it opens
    inside the leaf is left to the leaf's own seal rule, and one outside that
    rule's directories is refused rather than silently sealed or dropped.
    """
    import _proper_chronology

    leaf = leaf_path(root, provider, document).resolve()
    traced = _proper_chronology.computation_reads(document, root, provider)
    paths = {root / name for name in traced["source_files"]}
    for name in traced["reads"]:
        path = root / name
        if path.resolve().is_relative_to(leaf):
            parts = path.resolve().relative_to(leaf).parts
            if parts[:1] and parts[0] in LEAF_EVIDENCE or parts == LEAF_AGREEMENT_ONLY:
                continue
            raise ValueError("the chronology computation reads a leaf file the research seal "
                             f"does not cover: {name}")
        paths.add(path)
    modules = {name: digest(root / name) for name in traced["modules"]}
    return paths, modules, traced["sources"]


def review_inputs(root: Path, provider: str, document: str, review: str, *,
                  review_contract: str | None = None, mode: str = "print") -> dict:
    """Stable evidence scope for each independent review, sealed by the engine.

    Later editions are absent from earlier content scopes. Final metadata and
    the complete publication closure are bound by source-mode web review;
    historical print mode keeps its exact visual seal. Research is sealed first.
    """
    leaf = leaf_path(root, provider, document)
    if mode not in {"source", "print"}:
        raise ValueError("publication mode must be source or print")
    metadata_only = mode == "source"
    if review_contract is not None and (review_contract not in RESEARCH_REVIEW_CONTRACTS
                                        or review != "research"):
        raise ValueError(f"review-contract {review_contract} applies only to research review")
    paths: set[Path] = set()
    value = {"schema": 1, "provider": provider, "document": document, "review": review}
    if review == "research":
        ignored = {"production-review.md", "artifacts.json", "web-artifact.json",
                   "standing-findings.json"}
        paths.update(path for path in (leaf / "research").rglob("*")
                     if path.is_file() and path.name not in ignored)
        for name in ("context.md", "scope.md", "interpretations.md", "source-bindings.toml"):
            if not (leaf / "research" / name).is_file():
                raise ValueError(f"missing research review input: {name}")
        for directory in ("propers", "instance"):
            paths.update(path for path in (leaf / directory).rglob("*") if path.is_file())
        paths.update(research_dependencies(root, provider, document, metadata_only=metadata_only))
        paths.update(bound_evidence(root, leaf / "research/source-bindings.toml", metadata_only=metadata_only))
        if review_contract in RESEARCH_REVIEW_CONTRACTS:
            for name in ("research/chronology.toml", "research/chronology-annotations.tex"):
                path = leaf / name
                if not path.is_file() or not path.read_text().strip():
                    raise ValueError(f"{review_contract} research review requires canonical "
                                     f"chronology input: {name}")
            value["review_contract"] = review_contract
            computation = chronology_computation_inputs(root, provider, document)
            if review_contract in {CHRONOLOGY_READS_CONTRACT, SOURCE_DISPOSITIONS_CONTRACT}:
                reads, modules, cited = chronology_reads(root, provider, document)
                # The named list stays; anything else the computation compiled joins it.
                computation.update(modules)
                paths.update(reads)
                paths.update(source_evidence(root, cited, "chronology source", metadata_only=metadata_only))
                value["chronology_cited_sources"] = cited
            value["chronology_computation_inputs"] = computation
            if review_contract == SOURCE_DISPOSITIONS_CONTRACT:
                paths.update(source_dispositions(root, provider, document, metadata_only=metadata_only))
                value["source_admission_computation_inputs"] = source_admission_computation_inputs(root)
        if metadata_only:
            from _document_schema import evidence_metadata
            paths = evidence_metadata(root, paths)
            value["publication_mode"] = "source"
    elif review in {"study", "synthesis", "homily"}:
        data = manifest(leaf)
        mode = "research" if review == "study" else review
        entry = leaf / ("main.tex" if mode == "research" else mode + ".tex")
        paths.update(include_graph(entry, leaf, root / "src" / provider))
        selected = [item for item in data["components"] if mode in item["modes"]]
        value["component_contract"] = {
            key: data[key] for key in ("schema", "document", "calendar", "element_keys", "lanes")}
        if presentation_contract(data):
            value["component_contract"]["presentation_contract"] = data["presentation_contract"]
            value["component_contract"]["presentation"] = data["presentation"]
        value["component_contract"]["components"] = [
            {key: item[key] for key in sorted(item) if key != "modes"} for item in selected]
        # References can be declared separately from the literal input graph.
        for item in selected:
            paths.add(leaf / item["path"])
            paths.update(leaf / name for name in item.get("references", []))
        # Lane evidence is research-owned, but a study acceptance also binds the
        # exact evidence map it reviewed.
        if mode == "research":
            paths.update(lane_source_paths(data, leaf))
        # References can own further literal TeX dependencies. Use the same
        # parser as the component gate and web converter for their closure.
        for path in list(paths):
            if path.suffix == ".tex":
                paths.update(include_graph(path, leaf, root / "src" / provider))
        for path in list(paths):
            if path.name != "generation-metadata.tex":
                continue
            text = active_tex(path.read_text())
            residue = text
            for pattern in (REVISION_RE, CONTRIBUTION_RE, PRODUCTION_RE, INHERITANCE_RE):
                residue = pattern.sub("", residue)
            if residue.strip():
                raise ValueError("generation-metadata.tex contains meaning-bearing material outside pure generation declarations")
            value.setdefault("generation_provenance", {})[str(path.relative_to(root))] = {
                "production": PRODUCTION_RE.findall(text), "inheritance": INHERITANCE_RE.findall(text)}
            paths.remove(path)
    elif review == "visual":
        if metadata_only:
            raise ValueError("visual review requires an explicit print export, not source mode")
        value["artifacts"] = artifact_state(root, provider, document)
    elif review == "web":
        path = root / "build/web" / provider / f"{document}.md"
        value["web"] = {str(path.relative_to(root)): digest(path)}
        if mode == "source":
            value["source_publication"] = source_state(root, provider, document, run_gates=False)
    else:
        raise ValueError("unknown review scope")
    for path in paths:
        validate_liturgical_family(leaf, root / "src" / provider, path)
    value["files"] = {str(path.relative_to(root)): digest(path) for path in sorted(paths)}
    return value


def snapshot(root: Path, provider: str, document: str, *, web: bool = False) -> None:
    leaf = leaf_path(root, provider, document)
    if web:
        path = root / "build/web" / provider / f"{document}.md"
        data = {"schema": 1, "provider": provider, "document": document,
                "web": str(path.relative_to(root)), "sha256": digest(path)}
        target = leaf / WEB_RECEIPT
    else:
        data, target = artifact_state(root, provider, document), leaf / RECEIPT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def artifacts(root: Path, provider: str, document: str) -> None:
    leaf = leaf_path(root, provider, document)
    components(root, provider, document, "artifacts")
    recorded = json.loads((leaf / RECEIPT).read_text())
    schema = recorded.get("schema") if isinstance(recorded, dict) else None
    if schema != RECEIPT_SCHEMA:
        reason = ("schema 1 digested the TeX .log, which carries the build's time and "
                  "absolute checkout paths, so it verifies only where it was built"
                  if schema == 1 else f"schema {RECEIPT_SCHEMA} is required")
        raise ValueError(
            f"{RECEIPT} is receipt schema {schema!r}: {reason}. Rebuild all three PDFs, then "
            f"re-snapshot with `python3 scripts/_proper_study.py snapshot --provider {provider} "
            f"--document {document}`. A new receipt records bytes; it does not renew a review")
    current = artifact_state(root, provider, document)
    if recorded != current:
        differing = sorted(key for key in recorded.keys() | current.keys()
                           if recorded.get(key) != current.get(key))
        raise ValueError("built PDFs or render inputs differ from the snapshot prepared for "
                         "visual review (" + ", ".join(differing) + ")")
    for suffix in EDITIONS.values():
        output = f"{document}{suffix}"
        run(root, sys.executable, str(root / "tools/check-generation-metadata"),
            "--provider", provider, "--pdf", output,
            str(root / "build" / provider / f"{output}.pdf"))


def source_state(root: Path, provider: str, document: str, *, run_gates: bool = True) -> dict:
    """Validate declared source outputs without opening a print artifact.

    This identity is sealed by the independent web review after all three
    source reviews. It records inputs, never an editorial or print approval.
    """
    import _document_schema

    leaf = leaf_path(root, provider, document)
    record = _document_schema.load_manifest(root, leaf / "publication.toml")
    report = _document_schema.validate(root, record, phase="content", run_gates=run_gates)
    if not report["ok"]:
        raise ValueError("publication source contract failed: " + "; ".join(report["errors"]))
    expected = [("canonical" if mode == "research" else mode, f"{provider}/{document}{suffix}")
                for mode, suffix in EDITIONS.items()]
    if [(item["role"], item["id"]) for item in record["outputs"]] != expected:
        raise ValueError("publication must declare the ordered canonical, synthesis and homily source outputs")
    return {"schema": 1, "publication_mode": "source", "provider": provider,
            "document": document, "identities": _document_schema.identities(root, record)}


PROVIDER_LABELS = {"gpt": "GPT", "claude": "Claude"}
PROVIDER_COLUMNS = {"ChatGPT": "gpt", "Claude": "claude"}
CATALOG_LINK = re.compile(r"\[([^\]]*)\]\(\.\./(?:pdf|web)/([a-z]+)/[^)]*\)")


def catalog_cell_providers(text: str, row: str, row_links: list[str], primary: str | None) -> None:
    """Each catalog link must be recognizably its provider's.

    A cell in a named provider column links that provider's editions only.
    A cell whose column names no provider must say whose each link is: the
    postconciliar calendar's cycle columns hold every provider's edition in
    one cell. A bare label there reads as the primary provider's, so once a
    second provider's links enter the cell, or a non-primary provider's links
    stand alone in it, every label names its provider. On 2026-09-19 the Claude
    Twenty-fifth Sunday links followed the ChatGPT edition's bare ones and read
    as the same edition's.
    """
    lines = text.splitlines()
    index = lines.index(row)
    header = None
    for above in range(index - 1, 0, -1):
        if not lines[above].startswith("|"):
            break
        if re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", lines[above].strip()):
            header = [part.strip() for part in lines[above - 1].strip().strip("|").split("|")]
            break
    cells = [part.strip() for part in row.strip().strip("|").split(" | ")]
    for number, value in enumerate(cells):
        if not any(link in value for link in row_links):
            continue
        column = header[number] if header and number < len(header) else None
        links = CATALOG_LINK.findall(value)
        if column in PROVIDER_COLUMNS:
            for label, owner in links:
                if owner != PROVIDER_COLUMNS[column]:
                    raise ValueError(f"catalog column {column} links '{label}', "
                                     f"another provider's edition")
            return
        providers = {owner for _, owner in links}
        if providers <= {primary}:
            return
        for label, owner in links:
            name = PROVIDER_LABELS.get(owner, owner)
            if not re.search(rf"\b{re.escape(name)}\b", label):
                raise ValueError(
                    f"catalog cell under a cycle column links '{label}' without naming "
                    f"{name}; qualify every label in the cell by its provider, as "
                    "guidance/repository.md requires")
        return


def publication(root: Path, provider: str, document: str, *, mode: str = "print") -> None:
    catalog = scope(root, provider, document)
    if mode == "source":
        source_state(root, provider, document)
    elif mode == "print":
        artifacts(root, provider, document)
    else:
        raise ValueError("publication mode must be source or print")
    leaf = leaf_path(root, provider, document)
    data = manifest(leaf)
    text = (root / catalog).read_text()
    release = json.loads((root / "release/public-alpha.json").read_text())
    row_links = []
    for output_mode, suffix in EDITIONS.items():
        output = document + suffix
        if data["outputs"].get(output_mode) != output:
            raise ValueError(f"incorrect {output_mode} output id")
        if mode == "print":
            installed = root / "pdf" / provider / f"{output}.pdf"
            if digest(installed) != digest(root / "build" / provider / f"{output}.pdf"):
                raise ValueError(f"installed {output_mode} differs from reviewed build")
        from _document_schema import release_record
        record = release_record(root, root / "release/publications" / provider / f"{output}.json")
        if (record.get("schema_version"), record.get("id"), record.get("catalog"),
            record.get("status")) != (1, output, catalog, "alpha") or record.get("authorization") not in release.get("authorizations", {}):
            raise ValueError(f"release record does not authorize {output_mode} for this catalog")
        if mode == "print":
            row_links.append(f"](../pdf/{provider}/{output}.pdf)")
    row_links.append(f"](../web/{provider}/{document}.html)")
    rows = [line for line in text.splitlines() if all(link in line for link in row_links)]
    if len(rows) != 1:
        raise ValueError("one catalog row must link " + (
            "all three PDFs and canonical web edition" if mode == "print" else "the canonical web edition"))
    if mode == "source" and any(
            f"](../pdf/{provider}/{document}{suffix}.pdf)" in rows[0]
            for suffix in EDITIONS.values()):
        raise ValueError("source publication catalog must not link absent site PDFs")
    catalog_cell_providers(text, rows[0], row_links, release.get("provider"))
    publication_id = document if release.get("provider") == provider else f"{provider}:{document}"
    marker = f"<!-- triptych-publication-id: {publication_id} -->"
    if text.splitlines().count(marker) != 1:
        raise ValueError("catalog must carry exactly one canonical publication marker")
    # No copy of a web edition is tracked: the site converts it from the TeX
    # when it is built (guidance/web-editions.md). The reviewed conversion is
    # current only while a fresh conversion of today's sources is the same
    # bytes, and every reader output of the leaf, companions included, must
    # convert with its fidelity audits.
    receipt = json.loads((leaf / WEB_RECEIPT).read_text())
    generated = root / "build/web" / provider / f"{document}.md"
    if receipt != {"schema": 1, "provider": provider, "document": document,
                   "web": str(generated.relative_to(root)), "sha256": digest(generated)}:
        raise ValueError("web edition differs from the snapshot prepared for web review")
    fresh_root = root / ".scratch/proper-study-web" / provider
    fresh = fresh_root / provider / f"{document}.md"
    fresh.unlink(missing_ok=True)
    run(root, sys.executable, str(root / "tools/web-edition"), "--provider", provider,
        "--output", str(fresh_root), document)
    if digest(fresh) != digest(generated):
        raise ValueError("the reviewed web conversion is not what current sources convert to")
    run(root, sys.executable, str(root / "tools/web-edition"), "check",
        "--leaf", f"{provider}/{document}")
    run(root, sys.executable, str(root / "tools/check-web-edition"),
        "--provider", provider, "--document", document)


def check(root: Path, provider: str, document: str, phase: str,
          edition: str | None, *, require_presentation: bool = False,
          require_format: bool = False, require_authority: bool = False,
          require_orientation: bool = False, require_orientation_v2: bool = False,
          require_orientation_v3: bool = False,
          require_source_dispositions: bool = False, mode: str = "print") -> None:
    if mode not in {"source", "print"}:
        raise ValueError("publication mode must be source or print")
    scope(root, provider, document)
    leaf = leaf_path(root, provider, document)
    if phase == "scope":
        return
    reference_only_contract(root, provider, document, require_manifest=phase != "research")
    if phase == "research":
        for name in ("research/context.md", "research/scope.md", "research/interpretations.md",
                     "research/source-bindings.toml"):
            if not (leaf / name).is_file() or not (leaf / name).read_text().strip():
                raise ValueError(f"missing nonempty research artifact: {name}")
        run(root, sys.executable, str(root / "tools/check-content-preflight"),
            "--root", str(root), "--provider", provider, "--document", document,
            "--check", "bindings-valid")
        if require_source_dispositions:
            if mode == "source":
                source_dispositions(root, provider, document, metadata_only=True)
            else:
                source_dispositions(root, provider, document)
        review_inputs(root, provider, document, "research", mode=mode)
        return
    presentation_contract(manifest(leaf), required=require_presentation)
    format_contract(manifest(leaf), required=require_format)
    # Declaration only: the component checker below tests each lane's carrying
    # authors wherever the manifest declares the contract.
    authority_contract(manifest(leaf), required=require_authority)
    from _proper_chronology import presentation_contract as chronology_presentation
    declared = chronology_presentation(leaf, required=require_orientation or require_orientation_v2,
                                       current=require_orientation_v3)
    if require_orientation_v2 and declared == "orientation-v1":
        raise ValueError("orientation-v2 or later is required")
    if phase == "content":
        components(root, provider, document, "content", edition)
    elif phase == "artifacts":
        if mode == "source":
            source_state(root, provider, document)
        else:
            artifacts(root, provider, document)
    elif phase == "publication":
        publication(root, provider, document, mode=mode)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("identity", "check", "snapshot", "snapshot-web", "seal",
                                          "source-dispositions", "binding-digests"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--provider", choices=("gpt", "claude"), default="gpt")
    parser.add_argument("--document", required=True)
    parser.add_argument("--phase", choices=("scope", "research", "content", "artifacts", "publication"))
    parser.add_argument("--edition", choices=tuple(EDITIONS))
    parser.add_argument("--mode", choices=("source", "print"), default="print",
                        help="source validates source/HTML publication; print preserves historical exact-PDF gates")
    parser.add_argument("--require-presentation", action="store_true",
                        help="require the current physical pagination contract (proper-study v3)")
    parser.add_argument("--require-format", action="store_true",
                        help="require the shared proper typography contract (proper-study v6)")
    parser.add_argument("--require-authority", action="store_true",
                        help="require the author-standing contract (proper-study v7)")
    parser.add_argument("--require-orientation", action="store_true",
                        help="require generated passage/subject/date rows (proper-study v10)")
    parser.add_argument("--require-orientation-v2", action="store_true",
                        help="require orientation-v2 or later (historical proper-study v12 gate)")
    parser.add_argument("--require-orientation-v3", action="store_true",
                        help="require the complete provider-neutral chronology table")
    parser.add_argument("--require-source-dispositions", action="store_true",
                        help="require exact source registration and explicit fragment admission dispositions (proper-study v15)")
    parser.add_argument("--date", default="undated")
    parser.add_argument("--review", choices=("research", "study", "synthesis", "homily", "visual", "web"))
    parser.add_argument("--review-contract", choices=RESEARCH_REVIEW_CONTRACTS,
                        help="explicit versioned research seal; omitted for historical review receipts")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.date != "undated":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
                raise ValueError("date must be YYYY-MM-DD or undated")
            datetime.date.fromisoformat(args.date)
        if args.action == "seal":
            print(json.dumps(review_inputs(root, args.provider, args.document, args.review,
                                           review_contract=args.review_contract, mode=args.mode),
                             sort_keys=True, separators=(",", ":")))
            return 0
        if args.action == "binding-digests":
            path = leaf_path(root, args.provider, args.document) / "research/source-bindings.toml"
            bindings = tomllib.loads(path.read_text()).get("bindings", [])
            print(json.dumps({"bindings": [{"binding_index": index, "source_id": binding["source_id"],
                                           "binding_sha256": binding_digest(binding)}
                                          for index, binding in enumerate(bindings, 1)]}, sort_keys=True))
            return 0
        if args.action == "identity":
            identity(root, args.document)
        elif args.action == "source-dispositions":
            if args.mode == "source":
                source_dispositions(root, args.provider, args.document, metadata_only=True)
            else:
                source_dispositions(root, args.provider, args.document)
        elif args.action.startswith("snapshot"):
            if args.mode == "source" and args.action == "snapshot":
                raise ValueError("source publication uses document-schema identities, not a print snapshot")
            snapshot(root, args.provider, args.document, web=args.action == "snapshot-web")
        elif not args.phase:
            raise ValueError("check requires --phase")
        else:
            check(root, args.provider, args.document, args.phase, args.edition,
                  require_presentation=args.require_presentation, require_format=args.require_format,
                  require_authority=args.require_authority,
                  require_orientation=args.require_orientation,
                  require_orientation_v2=args.require_orientation_v2,
                  require_orientation_v3=args.require_orientation_v3,
                  require_source_dispositions=args.require_source_dispositions, mode=args.mode)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"proper-study: {error}", file=sys.stderr)
        return 1
    print(f"proper-study {args.action} {args.phase or ''}: {args.document}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
