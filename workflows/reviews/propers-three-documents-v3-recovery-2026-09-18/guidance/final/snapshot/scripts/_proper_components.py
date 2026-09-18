"""Schema-two proper editions: structural checks, never semantic approval.

Schema one remains owned by check-proper-components. These helpers also give
publication discovery one definition of a companion and its canonical owner.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

MANIFEST = "proper-components.toml"
MODES = ("research", "synthesis", "homily")
ENTRYPOINTS = {"research": "main.tex", "synthesis": "synthesis.tex", "homily": "homily.tex"}
SENSES = {"literal", "allegorical", "moral", "anagogical"}
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
KINDS = {"front-matter", "appointed-text", "proper-treatment", "interpretive-lane",
         "integrated-commentary", "homily", "terminal-apparatus"}
PRESENTATION_CONTRACT = "interpretive-pagination-v1"
PRESENTATION_ROLES = ("inventory", "overview", "chronology", "themes", "commentary")
PAGE_RANGES = {"research": (20, 50), "synthesis": (10, 12)}
MARKER_PREFIX = "triptych:concise:"
MARKERS = {
    "inventory": {"inventory:start": 1, "inventory:end": 1},
    "overview": {"overview:start": 1, "sense:literal": 1, "sense:allegorical": 1,
                 "sense:moral": 1, "sense:anagogical": 1, "overview:end": 1},
    "chronology": {"chronology:start": 2, "chronology:end": 2},
    "themes": {"themes:start": 3, "themes:end": 4},
    "commentary": {"commentary:start": 5},
}


def presentation_contract(data: dict, *, required: bool = False) -> bool:
    """Opt in explicitly; historical schema-two publications keep their contract."""
    value = data.get("presentation_contract")
    if value is None and not required:
        if "presentation" in data:
            raise ValueError("presentation requires an explicit presentation_contract")
        return False
    if data.get("schema") != 2 or value != PRESENTATION_CONTRACT:
        raise ValueError(f"presentation_contract must be {PRESENTATION_CONTRACT!r}")
    return True


def presentation_sources(data: dict, leaf: Path, provider_root: Path,
                         records: dict, *, check_files: bool) -> None:
    """Check declared membership and source-owned markers, not prose quality."""
    mapping = data.get("presentation")
    if not isinstance(mapping, dict) or set(mapping) != set(PRESENTATION_ROLES):
        raise ValueError("presentation must map inventory, overview, chronology, themes, commentary")
    if any(not isinstance(key, str) or key not in records for key in mapping.values()):
        raise ValueError("presentation roles must name declared component keys")
    if len(set(mapping.values())) != len(PRESENTATION_ROLES):
        raise ValueError("presentation roles require distinct component owners")
    for role, key in mapping.items():
        item = records[key]
        if "synthesis" not in item["modes"]:
            raise ValueError(f"presentation {role} must belong to synthesis")
        expected_kind = "integrated-commentary" if role == "commentary" else "front-matter"
        if item["kind"] != expected_kind:
            raise ValueError(f"presentation {role} must be {expected_kind}")
        if role == "inventory" and set(item.get("element_keys", [])) != set(data["element_keys"]):
            raise ValueError("presentation inventory must cover every appointed element key")
    chronology = records[mapping["chronology"]]
    annotations = "research/chronology-annotations.tex"
    if annotations not in chronology.get("references", []):
        raise ValueError("presentation chronology must declare canonical chronology annotations")
    if not check_files:
        return
    entry = leaf / "synthesis.tex"
    reached = include_graph(entry, leaf, provider_root)
    label_pattern = re.compile(r"\\zlabel\s*\{(" + re.escape(MARKER_PREFIX) + r"[^{}]+)\}")
    expected = [MARKER_PREFIX + name for role in PRESENTATION_ROLES for name in MARKERS[role]]
    owners = {MARKER_PREFIX + name: (leaf / records[mapping[role]]["path"]).resolve()
              for role in PRESENTATION_ROLES for name in MARKERS[role]}
    found = []
    for path in reached:
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
        if (path.resolve() != (leaf / chronology["path"]).resolve()
                and re.search(r"\\chronodate\s*\{", text)):
            raise ValueError("synthesis chronology cells must have the sole page-two source owner")
        labels = label_pattern.findall(text)
        for label in labels:
            if owners.get(label) != path.resolve():
                raise ValueError(f"presentation marker {label!r} has the wrong source owner")
        found.extend(labels)
        owned = [label for label in expected if owners[label] == path.resolve()]
        if labels != owned:
            raise ValueError(f"presentation markers missing, duplicated, or unordered in {path.name}")
    if sorted(found) != sorted(expected):
        raise ValueError("presentation requires every physical-page marker exactly once")

    # Follow actual include order, including repeated imports, rather than set order.
    annotation_imports = []
    def ordered(path: Path) -> list[str]:
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
        result = []
        for match in re.finditer(r"\\(zlabel|input|include)\s*\{([^{}]+)\}", text):
            command, value = match.groups()
            if command == "zlabel":
                if value.startswith(MARKER_PREFIX):
                    result.append(value)
                continue
            for base in (provider_root, provider_root.parent):
                target = (base / (value if Path(value).suffix else value + ".tex")).resolve()
                if target in reached:
                    if target == (leaf / annotations).resolve():
                        annotation_imports.append(target)
                    result.extend(ordered(target))
                    break
        return result
    if ordered(entry) != expected:
        raise ValueError("synthesis include order must follow the presentation roles exactly once")
    if len(annotation_imports) != 1:
        raise ValueError("synthesis must import canonical chronology annotations exactly once")
    owner = (leaf / chronology["path"]).resolve()
    if (leaf / annotations).resolve() not in include_graph(owner, leaf, provider_root):
        raise ValueError("presentation chronology must import canonical chronology annotations")
    text = re.sub(r"(?<!\\)%[^\n]*", "", owner.read_text())
    if not re.search(r"\\chronodate\s*\{", text) or not re.search(r"\\chronologyannotation\s*\{", text):
        raise ValueError("presentation chronology must use generated annotations in chronology cells")
    markers = list(label_pattern.finditer(text))
    if any(not markers[0].end() <= match.start() < markers[-1].start()
           for match in re.finditer(r"\\chronodate\s*\{", text)):
        raise ValueError("chronology cells must lie between their physical start/end markers")


def pagination_aux_files(aux: Path) -> list[Path]:
    """Read LaTeX's child aux graph beneath the output directory, once each."""
    root = aux.parent.resolve()
    found = []
    visited = set()

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError("pagination aux include escapes its output directory")
        if resolved in visited:
            raise ValueError("pagination aux includes a duplicate or cycle")
        visited.add(resolved)
        found.append(path)
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text())
        for token in re.finditer(r"\\@input\b", text):
            argument = re.match(r"\s*\{([^{}]+)\}", text[token.end():])
            if not argument:
                raise ValueError("pagination aux include must name a literal relative aux file")
            name = argument[1]
            relative = Path(name)
            if (relative.is_absolute() or ".." in relative.parts or relative.suffix != ".aux"
                    or any(character in name for character in "\\#\x00")):
                raise ValueError("pagination aux include must name a safe relative aux file")
            visit(root / relative)

    visit(aux)
    return found


def presentation_artifacts(data: dict, destination: Path, modes: tuple) -> None:
    """Physical PDF extent plus settled absolute-page evidence; never a review."""
    for mode in modes:
        if mode not in PAGE_RANGES:
            continue
        base = destination / data["outputs"][mode]
        result = subprocess.run(["pdfinfo", str(base.with_suffix(".pdf"))],
                                capture_output=True, text=True, timeout=30, check=False)
        match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.M)
        if result.returncode or not match:
            raise ValueError(f"cannot determine {mode} physical PDF page count")
        pages = int(match[1])
        lower, upper = PAGE_RANGES[mode]
        if not lower <= pages <= upper:
            raise ValueError(f"{mode} requires {lower}–{upper} physical pages; PDF has {pages}")
        log = base.with_suffix(".log").read_text(errors="replace")
        if re.search(r"undefined references|multiply[- ]defined labels|[Rr]erun to|"
                     r"Label\(s\) may have changed|Reference .* undefined", log):
            raise ValueError(f"{mode} pagination requires settled references and markers")
        if mode != "synthesis":
            continue
        aux = "\n".join(path.read_text() for path in pagination_aux_files(base.with_suffix(".aux")))
        labels = re.findall(r"\\zref@newlabel\{(" + re.escape(MARKER_PREFIX)
                            + r"[^{}]+)\}\{([^\n]*)\}", aux)
        expected = {MARKER_PREFIX + name: page for group in MARKERS.values()
                    for name, page in group.items()}
        if sorted(label for label, _ in labels) != sorted(expected):
            raise ValueError("aux requires every physical-page marker exactly once")
        for label, properties in labels:
            absolute = re.findall(r"\\abspage\{([0-9]+)\}", properties)
            if len(absolute) != 1 or int(absolute[0]) != expected[label]:
                raise ValueError(f"{label} must resolve to physical page {expected[label]}")


def liturgical_family(document: str) -> str | None:
    parts = Path(document).parts
    if parts[:3] == ("liturgy", "roman-rite", "1962"):
        return "roman-1962"
    if parts[:3] == ("liturgy", "roman-rite", "postconciliar"):
        return "postconciliar"
    return None


def validate_liturgical_family(leaf: Path, provider_root: Path, target: Path) -> None:
    """Keep calendar and edition content owners separate, including recorder inputs."""
    document = leaf.resolve().relative_to(provider_root.resolve()).as_posix()
    family = liturgical_family(document)
    target = target.resolve()
    if not target.is_relative_to(provider_root.resolve()):
        # Generic format and provider-neutral research sources may be shared;
        # liturgical content from another provider is never an authored input.
        src = provider_root.resolve().parent
        if target.is_relative_to(src):
            parts = target.relative_to(src).parts
            if len(parts) > 2 and parts[:2] == ("sources", "calendars"):
                target_family = "postconciliar" if parts[2] == "postconciliar" else parts[2]
                if family and target_family != family:
                    raise ValueError("include crosses the calendar source-owner boundary")
            if len(parts) > 1 and liturgical_family(str(Path(*parts[1:]))):
                raise ValueError("include crosses a provider's liturgical content boundary")
        return
    target_id = target.relative_to(provider_root.resolve()).as_posix()
    target_family = liturgical_family(target_id)
    if family and target_family and target_family != family:
        raise ValueError(f"include crosses the {family} calendar/proper boundary")
    if family == target_family == "postconciliar" and Path(document).parts[3] != Path(target_id).parts[3]:
        raise ValueError("include crosses the postconciliar edition/locale boundary")


def relative_id(value: object, field: str) -> str:
    if (not isinstance(value, str) or not value
            or any(not KEY.fullmatch(part) for part in value.split("/"))):
        raise ValueError(f"{field} must be a safe lowercase provider-relative id")
    return value


def strings(value: object, field: str, *, required: bool = True) -> list[str]:
    if (not isinstance(value, list)
            or any(not isinstance(item, str) or not item.strip() for item in value)
            or (required and not value) or len(value) != len(set(value))):
        raise ValueError(f"{field} must be a {'nonempty ' if required else ''}list of unique nonempty strings")
    return value


def owned_path(leaf: Path, value: object, field: str, *, exists: bool = True) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must name a relative file")
    path = Path(value)
    target = (leaf / path).resolve()
    if path.is_absolute() or ".." in path.parts or not target.is_relative_to(leaf.resolve()):
        raise ValueError(f"{field} must remain inside the canonical leaf")
    if exists and (not target.is_file() or target.stat().st_size == 0):
        raise ValueError(f"{field} names a missing or empty file: {value}")
    return target


def outputs(data: dict) -> dict[str, str]:
    """Validate identities before any consumer joins them onto a filesystem root."""
    if data.get("schema") not in {1, 2} or data.get("record_type") != "proper-components":
        raise ValueError("manifest requires schema = 1 or 2 and record_type = 'proper-components'")
    document = relative_id(data.get("document"), "document")
    if document.endswith(("-synthesis", "-homily")):
        raise ValueError("document must name the canonical research edition")
    result = data.get("outputs")
    if not isinstance(result, dict):
        raise ValueError("[outputs] is required")
    modes = MODES if data.get("schema") == 2 else MODES[:2]
    for mode in (*modes, "web"):
        expected = document if mode in {"research", "web"} else f"{document}-{mode}"
        if result.get(mode) != expected:
            raise ValueError(f"outputs.{mode} must equal {expected!r}")
    completeness = data.get("appointed_text_completeness")
    if completeness not in {"complete", "rights-limited"}:
        raise ValueError("appointed_text_completeness must be 'complete' or 'rights-limited'")
    labels = {"canonical_label": "Full PDF" if completeness == "complete" else "Research PDF",
              "synthesis_label": "Synthesis PDF"}
    if data.get("schema") == 2:
        labels["homily_label"] = "Homily PDF"
    for key, label in labels.items():
        if result.get(key) != label:
            raise ValueError(f"outputs.{key} must be {label!r}")
    if set(result) != set(modes) | {"web"} | set(labels):
        raise ValueError("outputs contains an undeclared output or label")
    return result


def companion_owner(source_root: Path, document: str) -> tuple[Path, Path] | None:
    """Resolve declared companions only; a real canonical leaf always wins."""
    relative_id(document, "document")
    direct = source_root / document
    if (direct / "main.tex").is_file():
        return None
    for mode in ("synthesis", "homily"):
        suffix = f"-{mode}"
        if not document.endswith(suffix):
            continue
        leaf = source_root / document.removesuffix(suffix)
        manifest = leaf / MANIFEST
        if not manifest.is_file():
            return None
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        if data.get("schema") not in {1, 2} or data.get("record_type") != "proper-components":
            raise ValueError(f"invalid proper manifest {manifest}")
        declared = outputs(data)
        if data["document"] != leaf.relative_to(source_root).as_posix():
            raise ValueError("manifest document does not match its owner")
        if declared.get(mode) == document:
            entry = owned_path(leaf, data.get(f"{mode}_entrypoint"), f"{mode}_entrypoint")
            return leaf, entry
    return None


def include_graph(entry: Path, leaf: Path, provider_root: Path) -> set[Path]:
    """Walk static, unconditional local includes; refuse unsupported ambiguity.

    The build resolves TeX inputs from the provider directory and src/. Local
    content must use that same spelling. Shared inputs are checked for existence
    and retained ownership; their own TeX macros are outside this graph.
    """
    visited: set[Path] = set()
    stack: set[Path] = set()
    token = re.compile(r"\\(?:input|include)\b|\\(?:if[a-zA-Z@]*|else|fi)\b")

    def walk(path: Path) -> None:
        if path in stack:
            raise ValueError(f"include cycle at {path.name}")
        if path in visited:
            return
        visited.add(path)
        stack.add(path)
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
        depth = 0
        for match in token.finditer(text):
            command = match.group()
            if command.startswith("\\if"):
                depth += 1
                continue
            if command == "\\fi":
                depth = max(0, depth - 1)
                continue
            if command == "\\else":
                continue
            argument = re.match(r"\s*\{([^{}]+)\}", text[match.end():])
            prefix = re.sub(r"\\[{}]", "", text[:match.start()])
            grouped = prefix.count("{") != prefix.count("}")
            if not argument or depth or grouped:
                raise ValueError(f"{path.name}: schema 2 requires literal unconditional includes")
            value = argument.group(1)
            relative = Path(value)
            if relative.is_absolute() or ".." in relative.parts or "\\" in value:
                raise ValueError(f"{path.name}: unsafe or dynamic include {value!r}")
            candidates = [base / (value if relative.suffix else f"{value}.tex")
                          for base in (provider_root, provider_root.parent)]
            target = next((candidate.resolve() for candidate in candidates if candidate.is_file()), None)
            if target is None:
                raise ValueError(f"{path.name}: missing include {value!r}")
            if not target.is_relative_to(provider_root.resolve()) and not target.is_relative_to((provider_root.parent / "common").resolve()):
                raise ValueError(f"{path.name}: include escapes its provider/common source owners")
            validate_liturgical_family(leaf, provider_root, target)
            if target.is_relative_to(leaf.resolve()):
                walk(target)
        stack.remove(path)

    walk(entry)
    return visited


def audit_v2(data: dict, path: Path, provider_root: Path, *, phase: str = "content",
             edition: str | None = None, build_root: Path | None = None) -> None:
    if data.get("schema") != 2:
        raise ValueError("three-edition validation requires schema = 2")
    if phase not in {"scope", "content", "artifacts"} or (edition is not None and edition not in MODES):
        raise ValueError("unknown validation phase or edition")
    leaf = path.parent
    declared = outputs(data)
    if data["document"] != leaf.relative_to(provider_root).as_posix():
        raise ValueError("document must match its canonical leaf id")
    family = liturgical_family(data["document"])
    if data.get("calendar") not in {"roman-1962", "postconciliar"} or (family and data["calendar"] != family):
        raise ValueError("calendar must identify and match the document's separate liturgical family")
    modes = (edition,) if edition else MODES
    check_files = phase != "scope"
    entries = {}
    for mode, name in ENTRYPOINTS.items():
        field = "entrypoint" if mode == "research" else f"{mode}_entrypoint"
        if data.get(field) != name:
            raise ValueError(f"{field} must be {name!r}")
        entries[mode] = owned_path(leaf, name, field, exists=check_files and mode in modes)
        if (provider_root / f"{data['document']}-{mode}").exists() and mode != "research":
            raise ValueError(f"{mode} must not have a second editable leaf")
    elements = strings(data.get("element_keys"), "element_keys")
    if any(not KEY.fullmatch(key) for key in elements):
        raise ValueError("element_keys must use stable lowercase kebab-case")
    components = data.get("components")
    if not isinstance(components, list) or not components:
        raise ValueError("[[components]] is required")
    records: dict[str, dict] = {}
    component_paths: dict[str, Path] = {}
    for item in components:
        if not isinstance(item, dict):
            raise ValueError("components must be tables")
        key = item.get("key")
        if not isinstance(key, str) or not KEY.fullmatch(key) or key in records:
            raise ValueError("component keys must be unique lowercase kebab-case")
        records[key] = item
        if item.get("kind") not in KINDS:
            raise ValueError(f"component {key}: invalid schema 2 kind")
        selected = strings(item.get("modes"), f"component {key} modes")
        if set(selected) - set(MODES):
            raise ValueError(f"component {key}: invalid mode")
        needed = check_files and bool(set(selected) & set(modes))
        component_paths[key] = owned_path(leaf, item.get("path"), f"component {key} path", exists=needed)
        if component_paths[key] in entries.values():
            raise ValueError("schema 2 components must be fragments, not entrypoints")
        bound = strings(item.get("element_keys", []), f"component {key} element_keys", required=False)
        if set(bound) - set(elements):
            raise ValueError(f"component {key}: undeclared element key")
        strings(item.get("depends_on", []), f"component {key} depends_on", required=False)
        for reference in strings(item.get("references", []), f"component {key} references", required=False):
            owned_path(leaf, reference, f"component {key} reference", exists=needed)
    if len(set(component_paths.values())) != len(component_paths):
        raise ValueError("schema 2 component paths must have one authoritative key")
    for key, item in records.items():
        for dependency in item.get("depends_on", []):
            if dependency not in records or not set(item["modes"]) <= set(records[dependency]["modes"]):
                raise ValueError(f"component {key}: unknown or omitted dependency {dependency!r}")
    def visit(key: str, trail: set[str]) -> None:
        if key in trail:
            raise ValueError("component dependency cycle")
        for dependency in records[key].get("depends_on", []):
            visit(dependency, trail | {key})
    for key in records:
        visit(key, set())
    for kind, mode in (("appointed-text", "research"), ("proper-treatment", "research"),
                       ("integrated-commentary", "synthesis"), ("homily", "homily")):
        matches = [item for item in components if item["kind"] == kind]
        if len(matches) != 1 or matches[0]["modes"] != [mode]:
            raise ValueError(f"exactly one {kind} component in {mode} mode is required")
        if set(matches[0].get("element_keys", [])) != set(elements):
            raise ValueError(f"{kind} must declare coverage of every element key")
    for mode in MODES:
        if not any(item["kind"] == "terminal-apparatus" and mode in item["modes"] for item in components):
            raise ValueError(f"{mode} requires terminal-apparatus")
    lanes = data.get("lanes")
    if not isinstance(lanes, list) or not 2 <= len(lanes) <= 5:
        raise ValueError("schema 2 requires 2–5 interpretive lanes")
    lane_keys: set[str] = set()
    bound_components: set[str] = set()
    for lane in lanes:
        if not isinstance(lane, dict):
            raise ValueError("lanes must be tables")
        key = lane.get("key")
        if not isinstance(key, str) or not KEY.fullmatch(key) or key in lane_keys:
            raise ValueError("lane keys must be unique lowercase kebab-case")
        lane_keys.add(key)
        authors = strings(lane.get("authors"), f"lane {key} authors")
        if len({author.strip().casefold() for author in authors}) < 2:
            raise ValueError(f"lane {key} requires at least two distinct authors")
        for source in strings(lane.get("sources"), f"lane {key} sources"):
            owned_path(leaf, source, f"lane {key} source", exists=check_files)
        if set(strings(lane.get("senses"), f"lane {key} senses")) != SENSES:
            raise ValueError(f"lane {key} requires all four senses")
        if set(strings(lane.get("element_keys"), f"lane {key} element_keys")) != set(elements):
            raise ValueError(f"lane {key} must cover every element key")
        for reference in strings(lane.get("component_keys"), f"lane {key} component_keys"):
            component = records.get(reference)
            if (component is None or component["kind"] != "interpretive-lane"
                    or component["modes"] != ["research"] or reference in bound_components):
                raise ValueError(f"lane {key} must own distinct research interpretive-lane components")
            bound_components.add(reference)
        coverage = set().union(*(set(records[ref].get("element_keys", [])) for ref in lane["component_keys"]))
        if coverage != set(elements):
            raise ValueError(f"lane {key} component coverage must include every element key")
    if bound_components != {key for key, item in records.items() if item["kind"] == "interpretive-lane"}:
        raise ValueError("every interpretive-lane component must belong to one declared lane")
    paginated = presentation_contract(data)
    if paginated:
        presentation_sources(data, leaf, provider_root, records,
                             check_files=check_files and "synthesis" in modes)
    if check_files:
        for mode in modes:
            reached = include_graph(entries[mode], leaf, provider_root)
            allowed = {entries[mode], (leaf / "generation-metadata.tex").resolve()}
            allowed.update(component_paths.values())
            for component in components:
                if mode in component["modes"]:
                    allowed.update((leaf / ref).resolve() for ref in component.get("references", []))
            if reached - allowed:
                unknown = sorted(str(item.relative_to(leaf.resolve())) for item in reached - allowed)
                raise ValueError(f"{mode} includes undeclared local fragments: {', '.join(unknown)}")
            for key, component in records.items():
                included = component_paths[key] in reached
                if (mode in component["modes"]) != included:
                    raise ValueError(f"{mode} include graph disagrees with component {key!r}")
    if phase == "artifacts":
        destination = build_root or provider_root.parents[1] / "build" / provider_root.name
        for mode in modes:
            pdf = owned_path(destination, declared[mode] + ".pdf", f"{mode} output")
            if not pdf.read_bytes().startswith(b"%PDF-"):
                raise ValueError(f"{mode} output is not a PDF")
        if paginated:
            presentation_artifacts(data, destination, modes)
