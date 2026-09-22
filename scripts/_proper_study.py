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
                                presentation_contract, format_contract, pagination_aux_files)
from _corpus import active_tex, REVISION_RE, CONTRIBUTION_RE, PRODUCTION_RE, INHERITANCE_RE

ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"research": "", "synthesis": "-synthesis", "homily": "-homily"}
RECEIPT = "research/artifacts.json"
WEB_RECEIPT = "research/web-artifact.json"
RESEARCH_REVIEW_CONTRACT = "proper-study-v3"
# Computation is a separate seal dimension from the source owners declared by
# research. The workflow digest covers recipes/fragments/schemas, not the code
# those commands execute. Keep this bounded adapter/query dependency list here.
CHRONOLOGY_COMPUTATION_INPUTS = (
    "scripts/_proper_chronology.py", "scripts/_proper_chronology_comparisons.py",
    "scripts/_chronology.py", "scripts/_canon.py",
    "scripts/_loci.py", "scripts/_calendars.py", "scripts/_tooling.py",
    "scripts/_psalms.py", "scripts/_deuterocanon.py", "scripts/_projection.py",
    "scripts/_psalter.py", "tools/proper-chronology", "requirements-tools.txt",
)
POSTCONCILIAR_CHRONOLOGY_INPUTS = (
    "scripts/_proper_chronology_inputs.py", "tools/citations",
    "guidance/liturgy/postconciliar-propers-registry.md",
)


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
    match = re.fullmatch(
        r"liturgy/roman-rite/postconciliar/([a-z0-9]+(?:-[a-z0-9]+)*)/"
        r"propers/temporal/(pc-s[0-9]{2}-.+)", document)
    if not match:
        raise ValueError("expected a 1962 proper or registered postconciliar "
                         "Proper-of-Time formula; other target families need "
                         "an explicit registry resolver")
    registry = (root / "guidance/liturgy/postconciliar-propers-registry.md").read_text()
    stems = dict(re.findall(r"^\| (PC-S\d\d) \| `(pc-s[^`]+)` \|", registry, re.M))
    keys = set(re.findall(r"`(PC-S\d\d-(?:ABC|[ABC])(?:-[A-Z0-9]+)*)`", registry))
    slugs = set()
    for key in keys:
        parts = key.split("-")
        parent, coverage = "-".join(parts[:2]), parts[2]
        if parent not in stems:
            continue
        suffix = "abc" if coverage == "ABC" else f"year-{coverage.lower()}"
        rest = [part.lower() for part in parts[3:] if part != "O"]
        slugs.add("-".join([stems[parent], suffix, *rest]))
    if match[2] not in slugs:
        raise ValueError("postconciliar slug names no exact formula in the stable registry")
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
    if not any(line.startswith("- Authorized ") and needle in line
               for line in plan.splitlines()):
        raise ValueError("production plan has no authorization for this exact provider and identity")
    if "/postconciliar/" in document:
        registry = root / "src" / provider / document.split("/propers/")[0] / "propers/registry"
        if not registry.is_dir():
            raise ValueError("postconciliar edition-locale has no owning registry")
    return catalog


def manifest(leaf: Path) -> dict:
    data = tomllib.loads((leaf / "proper-components.toml").read_text())
    if data.get("schema") != 2:
        raise ValueError("proper-study requires component schema 2; use legacy proper for schema 1")
    return data


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
    files = {}
    for mode, suffix in EDITIONS.items():
        path = root / "build" / provider / f"{document}{suffix}.pdf"
        if not path.is_file():
            raise ValueError(f"missing {mode} PDF: {path.relative_to(root)}")
        files[str(path.relative_to(root))] = digest(path)
    result = {"schema": 1, "provider": provider, "document": document,
              "pdfs": files, "render_inputs": render_inputs(root, provider, document)}
    if presentation_contract(manifest(leaf_path(root, provider, document))):
        evidence = set()
        for mode in ("research", "synthesis"):
            base = root / "build" / provider / f"{document}{EDITIONS[mode]}"
            evidence.add(base.with_suffix(".log"))
            evidence.update(pagination_aux_files(base.with_suffix(".aux")))
        result["pagination_evidence"] = {
            str(path.relative_to(root)): digest(path) for path in sorted(evidence)}
    return result




def bound_evidence(root: Path, bindings: Path) -> set[Path]:
    """Follow the source library's exact ancestry, including available payloads."""
    ids = [item["source_id"] for item in tomllib.loads(bindings.read_text()).get("bindings", [])]
    if not ids:
        return set()
    loader = importlib.machinery.SourceFileLoader("proper_study_sources", str(ROOT / "tools/source-library"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    library_tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = library_tool
    spec.loader.exec_module(library_tool)
    library = library_tool.load_library(root, check_binding_fingerprints=False)
    paths, visited = set(), set()
    while ids:
        source_id = ids.pop()
        if source_id in visited:
            continue
        visited.add(source_id)
        if source_id not in library.records:
            raise ValueError(f"unregistered bound evidence: {source_id}")
        record = library.records[source_id]
        paths.add(record.path)
        ids.extend(library_tool._dependency_ids(record))
        payload = record.data.get("path")
        if payload:
            path = (root / payload).resolve()
            if not path.is_relative_to(root):
                raise ValueError("source payload escapes repository")
            if path.is_file():
                paths.add(path)
            elif record.data.get("storage") == "tracked":
                raise ValueError(f"missing tracked source payload: {payload}")
    return paths


def research_dependencies(root: Path, provider: str, document: str) -> set[Path]:
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
        if Path(name).is_absolute() or ".." in Path(name).parts or not path.exists():
            raise ValueError(f"unsafe or missing evidence dependency: {name}")
        validate_liturgical_family(leaf, root / "src" / provider, path)
        if not path.resolve().is_relative_to(root / "src"):
            raise ValueError("evidence dependencies must name tracked source owners under src/")
        resolved = path.resolve()
        if canonical_owner is not None and (resolved == canonical_owner
                                             or resolved.is_relative_to(canonical_owner)):
            shared_owner = True
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


def review_inputs(root: Path, provider: str, document: str, review: str, *,
                  review_contract: str | None = None) -> dict:
    """Stable evidence scope for each independent review, sealed by the engine.

    Later editions are deliberately absent from earlier content scopes. Metadata
    evolves with contributors and is finally bound, in full, by visual review.
    Research evidence and source bindings are independently sealed before prose.
    """
    leaf = leaf_path(root, provider, document)
    if review_contract is not None and (review_contract != RESEARCH_REVIEW_CONTRACT or review != "research"):
        raise ValueError("review-contract proper-study-v3 applies only to research review")
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
        paths.update(research_dependencies(root, provider, document))
        paths.update(bound_evidence(root, leaf / "research/source-bindings.toml"))
        if review_contract == RESEARCH_REVIEW_CONTRACT:
            for name in ("research/chronology.toml", "research/chronology-annotations.tex"):
                path = leaf / name
                if not path.is_file() or not path.read_text().strip():
                    raise ValueError(f"v3 research review requires canonical chronology input: {name}")
            value["review_contract"] = review_contract
            value["chronology_computation_inputs"] = chronology_computation_inputs(root, provider, document)
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
        value["artifacts"] = artifact_state(root, provider, document)
    elif review == "web":
        path = root / "build/web" / provider / f"{document}.md"
        value["web"] = {str(path.relative_to(root)): digest(path)}
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
    if recorded != artifact_state(root, provider, document):
        raise ValueError("built PDFs or render inputs differ from the snapshot prepared for visual review")
    for suffix in EDITIONS.values():
        output = f"{document}{suffix}"
        run(root, sys.executable, str(root / "tools/check-generation-metadata"),
            "--provider", provider, "--pdf", output,
            str(root / "build" / provider / f"{output}.pdf"))


def publication(root: Path, provider: str, document: str) -> None:
    catalog = scope(root, provider, document)
    artifacts(root, provider, document)
    leaf = leaf_path(root, provider, document)
    data = manifest(leaf)
    text = (root / catalog).read_text()
    release = json.loads((root / "release/public-alpha.json").read_text())
    row_links = []
    for mode, suffix in EDITIONS.items():
        output = document + suffix
        if data["outputs"].get(mode) != output:
            raise ValueError(f"incorrect {mode} output id")
        installed = root / "pdf" / provider / f"{output}.pdf"
        if digest(installed) != digest(root / "build" / provider / f"{output}.pdf"):
            raise ValueError(f"installed {mode} differs from reviewed build")
        record = json.loads((root / "release/publications" / provider / f"{output}.json").read_text())
        if (record.get("schema_version"), record.get("id"), record.get("catalog"),
            record.get("status")) != (1, output, catalog, "alpha") or record.get("authorization") not in release.get("authorizations", {}):
            raise ValueError(f"release record does not authorize {mode} for this catalog")
        row_links.append(f"](../pdf/{provider}/{output}.pdf)")
    row_links.append(f"](../web/{provider}/{document}.html)")
    rows = [line for line in text.splitlines() if all(link in line for link in row_links)]
    if len(rows) != 1:
        raise ValueError("one catalog row must link all three PDFs and canonical web edition")
    publication_id = document if release.get("provider") == provider else f"{provider}:{document}"
    marker = f"<!-- triptych-publication-id: {publication_id} -->"
    if text.splitlines().count(marker) != 1:
        raise ValueError("catalog must carry exactly one canonical publication marker")
    web = root / "web" / provider / f"{document}.md"
    receipt = json.loads((leaf / WEB_RECEIPT).read_text())
    generated = root / "build/web" / provider / f"{document}.md"
    if receipt != {"schema": 1, "provider": provider, "document": document,
                   "web": str(generated.relative_to(root)), "sha256": digest(generated)}:
        raise ValueError("web edition differs from the snapshot prepared for web review")
    if digest(web) != digest(generated):
        raise ValueError("installed web edition differs from the reviewed conversion")
    run(root, "git", "ls-files", "--error-unmatch", str(web.relative_to(root)))
    for suffix in ("-synthesis", "-homily"):
        if (root / "web" / provider / f"{document}{suffix}.md").exists():
            raise ValueError("derived companions must not create separate web prose authorities")
    run(root, sys.executable, str(root / "tools/check-web-edition"),
        "--provider", provider, "--document", document)


def check(root: Path, provider: str, document: str, phase: str,
          edition: str | None, *, require_presentation: bool = False,
          require_format: bool = False) -> None:
    scope(root, provider, document)
    leaf = leaf_path(root, provider, document)
    if phase == "scope":
        return
    if phase == "research":
        for name in ("research/context.md", "research/scope.md", "research/interpretations.md",
                     "research/source-bindings.toml"):
            if not (leaf / name).is_file() or not (leaf / name).read_text().strip():
                raise ValueError(f"missing nonempty research artifact: {name}")
        run(root, sys.executable, str(root / "tools/check-content-preflight"),
            "--root", str(root), "--provider", provider, "--document", document,
            "--check", "bindings-valid")
        review_inputs(root, provider, document, "research")
        return
    presentation_contract(manifest(leaf), required=require_presentation)
    format_contract(manifest(leaf), required=require_format)
    if phase == "content":
        components(root, provider, document, "content", edition)
    elif phase == "artifacts":
        artifacts(root, provider, document)
    elif phase == "publication":
        publication(root, provider, document)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("identity", "check", "snapshot", "snapshot-web", "seal"))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--provider", choices=("gpt", "claude"), default="gpt")
    parser.add_argument("--document", required=True)
    parser.add_argument("--phase", choices=("scope", "research", "content", "artifacts", "publication"))
    parser.add_argument("--edition", choices=tuple(EDITIONS))
    parser.add_argument("--require-presentation", action="store_true",
                        help="require the current physical pagination contract (proper-study v3)")
    parser.add_argument("--require-format", action="store_true",
                        help="require the shared proper typography contract (proper-study v6)")
    parser.add_argument("--date", default="undated")
    parser.add_argument("--review", choices=("research", "study", "synthesis", "homily", "visual", "web"))
    parser.add_argument("--review-contract", choices=(RESEARCH_REVIEW_CONTRACT,),
                        help="explicit v3 research seal; omitted for historical review receipts")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.date != "undated":
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
                raise ValueError("date must be YYYY-MM-DD or undated")
            datetime.date.fromisoformat(args.date)
        if args.action == "seal":
            print(json.dumps(review_inputs(root, args.provider, args.document, args.review,
                                           review_contract=args.review_contract),
                             sort_keys=True, separators=(",", ":")))
            return 0
        if args.action == "identity":
            identity(root, args.document)
        elif args.action.startswith("snapshot"):
            snapshot(root, args.provider, args.document, web=args.action == "snapshot-web")
        elif not args.phase:
            raise ValueError("check requires --phase")
        else:
            check(root, args.provider, args.document, args.phase, args.edition,
                  require_presentation=args.require_presentation, require_format=args.require_format)
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as error:
        print(f"proper-study: {error}", file=sys.stderr)
        return 1
    print(f"proper-study {args.action} {args.phase or ''}: {args.document}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
