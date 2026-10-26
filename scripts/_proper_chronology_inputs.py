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
    r"propers/(temporal|general-calendar)/(pc-[sr][0-9]{2}-.+)"
)


class RegisteredTarget(NamedTuple):
    formula: str
    family: str
    slug: str
    owner: str


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


def registered_target(document: str, root: Path, formula: str | None = None) -> RegisteredTarget:
    """Resolve only the stable PC-S temporal and PC-R replacement namespaces.

    A matching slug is insufficient in the other calendar family. Edition
    adoption is a separate check: in particular the stable registry lists both
    possible All Souls expansions without selecting one for any edition.
    """
    match = DOCUMENT.fullmatch(document)
    if match is None or any(part in {"", ".", ".."} for part in document.split("/")):
        raise ValueError("postconciliar identity requires a registered PC-S temporal "
                         "or PC-R general-calendar leaf")
    registry = _file(root, REGISTRY).read_text(encoding="utf-8")
    stems = dict(re.findall(r"^\| (PC-[SR]\d\d) \| `(pc-[sr][^`]+)` \|", registry, re.M))
    keys = set(re.findall(r"`(PC-[SR]\d\d-(?:ABC|[ABC])(?:-[A-Z0-9]+)*)`", registry))
    if formula is not None and (not isinstance(formula, str) or formula not in keys):
        raise ValueError("appointment formula is not an exact registered PC-S or PC-R key")
    targets = []
    for key in ([formula] if formula is not None else sorted(keys)):
        parts = key.split("-")
        parent = "-".join(parts[:2])
        stem = stems.get(parent)
        if stem is None:
            continue
        family = "temporal" if parent.startswith("PC-S") else "general-calendar"
        suffix = "abc" if parts[2] == "ABC" else f"year-{parts[2].lower()}"
        slug = "-".join([stem, suffix, *(part.lower() for part in parts[3:] if part != "O")])
        if (family, slug) != (match[2], match[3]):
            continue
        number = int(parent[4:])
        if family == "temporal" and "SCRUTINY" in parts:
            owner = "ritual/shared/formularies/celebration-of-the-scrutinies"
        elif family == "temporal" and 28 <= number <= 59:
            owner = f"temporal/shared/ordinary-time/weeks/{number - 26:02}"
        else:
            owner = f"{family}/shared/formularies/{stem}"
        targets.append(RegisteredTarget(key, family, slug, owner + "/propers/verified.md"))
    if len(targets) != 1:
        raise ValueError("postconciliar formula does not identify this exact registered slug and family")
    return targets[0]


def replacement_disposition(root: Path, proper_root: Path, target: RegisteredTarget) -> None:
    """Require one exact edition-adopted PC-R row and its stable source owner.

    Read the named columns, so a key or slug mentioned in another target's
    qualifications cannot adopt it. The existing edition tables distinguish
    adopted or published targets from the unresolved replacement inventory.
    """
    registry_path = _file(root, (proper_root / "registry/formula-dispositions.md")
                          .relative_to(root).as_posix())
    lines = registry_path.read_text(encoding="utf-8").splitlines()

    def cells(line: str) -> list[str]:
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            return []
        return [cell.strip() for cell in stripped[1:-1].split("|")]

    rows = []
    required = ("formula key", "full publication slug", "canonical owner", "disposition")
    for index, line in enumerate(lines[:-1]):
        header = [re.sub(r"[*_`]", "", cell).casefold() for cell in cells(line)]
        if any(header.count(name) != 1 for name in required):
            continue
        separator = cells(lines[index + 1])
        if (len(separator) != len(header) or any(
                re.fullmatch(r":?-{3,}:?", cell) is None for cell in separator)):
            continue
        for row_line in lines[index + 2:]:
            row = cells(row_line)
            if not row:
                break
            if len(row) == len(header):
                rows.append(dict(zip(header, row)))
    matches = [row for row in rows if row["formula key"] == f"`{target.formula}`"
               or row["full publication slug"] == f"`{target.slug}`"]
    if (len(matches) != 1 or matches[0]["formula key"] != f"`{target.formula}`"
            or matches[0]["full publication slug"] != f"`{target.slug}`"
            or re.match(r"(?:Adopted|Published)\b", matches[0]["disposition"]) is None):
        raise ValueError("replacement formula requires one exact adopted edition registry disposition")
    links = re.findall(r"\[[^]]+\]\(([^)]+)\)", matches[0]["canonical owner"])
    if links != [f"../{target.owner}"]:
        raise ValueError("replacement edition disposition names a different canonical shared owner")
    if target.formula.startswith("PC-R08-"):
        # The stable registry offers alternatives, not a union of targets.
        # An edition must adopt one complete expansion before any leaf can
        # consume it; checking only this leaf's row would admit both shapes.
        registry = _file(root, REGISTRY).read_text(encoding="utf-8")
        keys = set(re.findall(r"`(PC-R08-(?:ABC|[ABC])-FORMULARY-[123])`", registry))
        expansions = [{key for key in keys if key.split("-")[2] == "ABC"},
                      {key for key in keys if key.split("-")[2] != "ABC"}]
        adopted = [row for row in rows
                   if (row["formula key"].startswith("`PC-R08-")
                       or row["full publication slug"].startswith("`pc-r08-"))
                   and re.match(r"(?:Adopted|Published)\b", row["disposition"])]
        adopted_keys = [row["formula key"].strip("`") for row in adopted]
        if (len(adopted_keys) != len(set(adopted_keys))
                or set(adopted_keys) not in expansions):
            raise ValueError("PC-R08 edition must adopt exactly one complete registered expansion")
        stem = re.search(r"^\| PC-R08 \| `([^`]+)` \|", registry, re.M).group(1)
        for row, key in zip(adopted, adopted_keys):
            parts = key.split("-")
            suffix = "abc" if parts[2] == "ABC" else f"year-{parts[2].lower()}"
            slug = "-".join([stem, suffix, *(part.lower() for part in parts[3:])])
            if (row["formula key"] != f"`{key}`"
                    or row["full publication slug"] != f"`{slug}`"
                    or re.findall(r"\[[^]]+\]\(([^)]+)\)", row["canonical owner"])
                    != [f"../{target.owner}"]):
                raise ValueError("PC-R08 expansion has a different registered slug or canonical shared owner")
    _file(root, (proper_root / target.owner).relative_to(root).as_posix())


def _canonical_locus(system: str, locus: str, key: str) -> str:
    token, chapter, verse = locus.split(".")
    converted = _chronology.to_canonical(system, token, int(chapter), int(verse))
    if isinstance(converted, _chronology.Unresolved):
        raise ValueError(f"{key}: {converted.status}: {converted.reason}")
    if not 1 <= converted.verse <= _chronology.verse_counts().get((converted.token, converted.chapter), 0):
        raise ValueError(f"{key}: citation outside canonical verse bounds: {converted}")
    return str(converted)


def load(document: str, root: Path, provider: str, loci_of) -> Appointments:
    """Validate a complete owning inventory and return canonical query loci.

    Whole-verse corpus queries conservatively cover fractional citations; exact
    printed bounds remain in refs and the explicit query-boundary note. They
    neither supply missing appointed wording nor claim subverse precision.
    """
    target = registered_target(document, root)
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
    formula = data.get("formula", "")
    if formula != target.formula:
        raise ValueError("appointment formula does not identify this exact registered slug")

    proper_root = leaf.parent.parent
    owner_id = (proper_root / target.owner).relative_to(root).as_posix()
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
    if not any(f"`{formula}`" in line and f"`{target.slug}`" in line
               for line in dispositions.splitlines() if line.startswith("|")):
        raise ValueError("appointment formula has no exact edition registry disposition")
    if target.family == "general-calendar":
        replacement_disposition(root, proper_root, target)
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
            # Expansion can erase an invalid edge of a cross-chapter span:
            # Matthew 20:100-21:2 otherwise becomes only Matthew 21:1-2.
            # Validate the parser's original endpoints before expanding, using
            # the same canonical spelling and concordance as the final query.
            for span in passage["ranges"]:
                for endpoint in (span["begin"], span["end"]):
                    point = {"book": passage["book"],
                             "ranges": [{"begin": endpoint, "end": endpoint}]}
                    for locus in loci_of(point, key):
                        _canonical_locus(system, locus, key)
            loci.extend(_canonical_locus(system, locus, key) for locus in loci_of(passage, key))
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
