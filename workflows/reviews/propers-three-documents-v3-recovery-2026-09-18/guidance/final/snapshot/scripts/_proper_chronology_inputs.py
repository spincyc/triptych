"""Reviewed, family-owned appointment inputs for postconciliar chronology.

This reads no chronology data and assigns no dates.  Local research owns the
citations; the canonical citation parser and chronology concordance own their
encoding and conversion.  The generic calendar index is not an edition-specific
appointment authority.  In particular its known Psalm 118 lead must not override
the reviewed Hebrew Psalm 119 appointment in the Week 25 owner.
"""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import re
import tomllib
from functools import lru_cache
from pathlib import Path
from typing import NamedTuple

import _chronology

ROOT = Path(__file__).resolve().parents[1]
INPUT = "research/chronology-inputs.toml"
REGISTRY = "guidance/liturgy/postconciliar-propers-registry.md"
DOCUMENT = re.compile(
    r"liturgy/roman-rite/postconciliar/([a-z0-9]+(?:-[a-z0-9]+)*)/"
    r"propers/temporal/(pc-s[0-9]{2}-.+)"
)


class Appointments(NamedTuple):
    formula: str
    elements: tuple
    dependencies: tuple[tuple[str, str], ...]
    notes: tuple[str, ...]


@lru_cache(maxsize=1)
def _citations():
    loader = importlib.machinery.SourceFileLoader(
        "_proper_chronology_citations", str(ROOT / "tools/citations")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def _file(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or any(
        part in {"", ".", ".."} for part in value.split("/")
    ):
        raise ValueError(f"noncanonical appointment dependency: {value!r}")
    path = root / value
    if path.is_absolute() and not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"appointment dependency leaves repository: {value!r}")
    if path.resolve() != root.resolve() / value:
        raise ValueError(f"appointment dependency aliases a different owner: {value!r}")
    if not path.is_file():
        raise ValueError(f"missing appointment dependency: {value}")
    return path


def _fields(record: dict, allowed: set[str], where: str) -> None:
    if not isinstance(record, dict) or set(record) - allowed:
        raise ValueError(f"{where}: invalid or unknown appointment fields")


def load(document: str, root: Path, provider: str, loci_of) -> Appointments:
    """Validate a complete owning inventory and return canonical query loci.

    Whole-verse corpus queries conservatively cover fractional citations; exact
    printed bounds remain in refs and the explicit query-boundary note. They
    neither supply missing appointed wording nor claim subverse precision.
    """
    match = DOCUMENT.fullmatch(document)
    if match is None or any(part in {"", ".", ".."} for part in document.split("/")):
        raise ValueError("postconciliar chronology requires a registered PC-S temporal leaf")
    if provider not in {"gpt", "claude"}:
        raise ValueError("postconciliar chronology provider must be gpt or claude")
    leaf_id = f"src/{provider}/{document}"
    leaf = root / leaf_id
    source = _file(root, f"{leaf_id}/{INPUT}")
    data = tomllib.loads(source.read_text(encoding="utf-8"))
    _fields(data, {"schema", "record_type", "document", "calendar", "formula",
                   "shared_owner", "elements"}, INPUT)
    if (data.get("schema"), data.get("record_type"), data.get("document"),
            data.get("calendar")) != (1, "proper-chronology-inputs", document, "postconciliar"):
        raise ValueError("appointment input schema, document or calendar does not match its leaf")

    registry_path = _file(root, REGISTRY)
    registry = registry_path.read_text(encoding="utf-8")
    stems = dict(re.findall(r"^\| (PC-S\d\d) \| `(pc-s[^`]+)` \|", registry, re.M))
    formula = data.get("formula", "")
    if not isinstance(formula, str) or not re.fullmatch(
        r"PC-S\d\d-(?:ABC|[ABC])(?:-[A-Z0-9]+)*", formula
    ) or f"`{formula}`" not in registry:
        raise ValueError("appointment formula is not an exact registered PC-S key")
    parts = formula.split("-")
    parent = "-".join(parts[:2])
    stem = stems.get(parent)
    suffix = "abc" if parts[2] == "ABC" else f"year-{parts[2].lower()}"
    slug = "-".join([stem or "", suffix, *(part.lower() for part in parts[3:] if part != "O")])
    if slug != match[2]:
        raise ValueError("appointment formula does not identify this exact registered slug")

    proper_root = leaf.parent.parent
    number = int(parent[4:])
    if "SCRUTINY" in parts:
        owner = proper_root / "ritual/shared/formularies/celebration-of-the-scrutinies"
    elif 28 <= number <= 59:
        owner = proper_root / f"temporal/shared/ordinary-time/weeks/{number - 26:02}"
    else:
        owner = proper_root / f"temporal/shared/formularies/{stem}"
    owner_id = (owner / "propers/verified.md").relative_to(root).as_posix()
    if data.get("shared_owner") != owner_id:
        raise ValueError("appointment shared owner is not this formula's same-edition canonical owner")
    local_owner = f"{leaf_id}/propers/verified.md"
    dependencies = {source, registry_path, _file(root, owner_id), _file(root, local_owner)}
    # Research establishes appointments before authoring creates presentation
    # components. A later manifest must agree, but neither its presence nor
    # unrelated layout bytes are inputs to a chronology answer.
    component_path = leaf / "proper-components.toml"
    instance_path = _file(root, f"{leaf_id}/instance/manifest.md")
    dependencies.add(instance_path)
    for filename in ("README.md", "formula-dispositions.md"):
        dependencies.add(_file(root, (proper_root / "registry" / filename).relative_to(root).as_posix()))
    dispositions = (proper_root / "registry/formula-dispositions.md").read_text(encoding="utf-8")
    if not any(f"`{formula}`" in line and f"`{slug}`" in line
               for line in dispositions.splitlines() if line.startswith("|")):
        raise ValueError("appointment formula has no exact edition registry disposition")
    elements = data.get("elements")
    if not isinstance(elements, list) or not elements:
        raise ValueError("appointment input requires a complete element inventory")
    keys = [element.get("key") for element in elements if isinstance(element, dict)]
    if (len(keys) != len(elements) or any(not isinstance(key, str) or
            not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) for key in keys)
            or len(set(keys)) != len(keys)):
        raise ValueError("appointment elements require distinct canonical element keys")
    instance = instance_path.read_text(encoding="utf-8")
    rows = [line.split("|")[2].strip().strip("`") for line in instance.splitlines()
            if re.match(r"^\|\s*\d+[a-z]?\s*\|", line)]
    if rows != keys:
        raise ValueError("appointment elements disagree with the ordered instance inventory")
    if component_path.exists() or component_path.is_symlink():
        component_path = _file(root, f"{leaf_id}/proper-components.toml")
        components = tomllib.loads(component_path.read_text(encoding="utf-8"))
        if components.get("document") != document or components.get("calendar") != "postconciliar":
            raise ValueError("component manifest has a different appointment identity or family")
        if components.get("element_keys") != keys:
            raise ValueError("appointment elements must exactly partition the ordered component element_keys")

    output, notes = [], []
    for element in elements:
        _fields(element, {"key", "name", "owner", "citations", "non_scriptural_reason"}, INPUT)
        key, name = element["key"], element.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{key}: missing element name")
        if element.get("owner") not in {owner_id, local_owner}:
            raise ValueError(f"{key}: citation owner is not this leaf or its canonical shared owner")
        citations = element.get("citations")
        if not isinstance(citations, list):
            raise ValueError(f"{key}: citations must be an explicit list")
        if not citations:
            reason = element.get("non_scriptural_reason")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{key}: non-scriptural element requires an explicit reason")
            notes.append(f"{key}: {reason}")
        elif "non_scriptural_reason" in element:
            raise ValueError(f"{key}: scriptural and non-scriptural dispositions conflict")
        refs, loci = [], []
        for citation in citations:
            _fields(citation, {"ref", "citation", "system", "kind"}, key)
            ref, text = citation.get("ref"), citation.get("citation")
            kind, system = citation.get("kind"), citation.get("system")
            if kind not in {"appointed", "adaptation", "identified-basis", "response"}:
                raise ValueError(f"{key}: unknown citation relationship")
            if not isinstance(text, str) or not isinstance(ref, str) or ref not in {text, f"Cf. {text}"}:
                raise ValueError(f"{key}: printed ref must preserve the exact citation, optionally Cf.")
            if ref.startswith("Cf.") and kind != "adaptation":
                raise ValueError(f"{key}: Cf. citation must retain its adaptation relationship")
            passage = _citations().parse_citation(text)
            if system not in {"vulgate", "hebrew"} or (system == "hebrew" and passage["book"] != "Psalms"):
                raise ValueError(f"{key}: unsupported citation numbering system for this book")
            # Nonpreferred open ranges cannot borrow preferred-system bounds.
            if system != "vulgate" and any(
                span["begin"].get("chapter") != span["end"].get("chapter")
                or span["begin"].get("verse") is None or span["end"].get("verse") is None
                for span in passage["ranges"]
            ):
                raise ValueError(f"{key}: Hebrew psalm queries require closed single-chapter ranges")
            for locus in loci_of(passage, key):
                token, chapter, verse = locus.split(".")
                converted = _chronology.to_canonical(system, token, int(chapter), int(verse))
                if isinstance(converted, _chronology.Unresolved):
                    raise ValueError(f"{key}: {converted.status}: {converted.reason}")
                if not 1 <= converted.verse <= _chronology.verse_counts().get((converted.token, converted.chapter), 0):
                    raise ValueError(f"{key}: citation outside canonical verse bounds: {converted}")
                loci.append(str(converted))
            partial = any(endpoint.get("part") for span in passage["ranges"] for endpoint in span.values())
            notes.append(f"{key}: {ref}; {kind}; {system} numbering; " +
                         ("whole-verse query envelope, not subverse chronology or appointed wording."
                          if partial else "canonical verse queries, not appointed wording."))
            refs.append(ref)
        output.append((key, name, tuple(refs), tuple(dict.fromkeys(loci))))
    fingerprints = tuple(sorted((path.relative_to(root).as_posix(),
                                  hashlib.sha256(path.read_bytes()).hexdigest())
                                 for path in dependencies))
    return Appointments(formula, tuple(output), fingerprints, tuple(notes))
