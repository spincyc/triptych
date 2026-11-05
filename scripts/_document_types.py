#!/usr/bin/env python3
"""Document types: one shared skeleton per kind of publication edition.

A document type is a directory ``src/common/document-types/<type>/`` holding a
``type.toml`` manifest and one TeX template per edition. A publication leaf
opts in with a ``[document]`` table in its ``publication.toml`` that names the
type and supplies only what is the leaf's own: metadata fields (title, PDF
subject, ...), ordered region lists of its authored section files, and option
choices. Doc-local macros stay in the leaf's conventional ``format.tex``.

Every opted-in edition entrypoint (``main.tex``, ``synthesis.tex``,
``homily.tex``) is then a *generated projection*: this module instantiates the
type's template with the leaf's declaration and writes ordinary, literal TeX.
The entrypoint is never edited by hand. ``Assembly`` derives the current
entrypoints and projection files when web, print, or source validation reads
them; tracked snapshots do not determine their contents. ``refresh`` remains
an explicit snapshot-maintenance operation, while the CLI's ``--check``
validates live assembly without requiring those snapshots to be rewritten.

Why generated literal entrypoints rather than a TeX-level ``\\input`` of a
shared shell with macro paths: every downstream reader of this corpus -- Make's
dependency graph, the recorder check, native print bundles, ``web-edition``,
the schema closure (which treats a computed ``\\input`` as unproven), the
generation-metadata and proper-component checks -- follows literal ``\\input``
paths. A generated entrypoint keeps all of them working for every type without
type-specific code, and keeps one implementation of the expansion instead of a
TeX one and a Python emulation that could drift apart.

Deterministic content is placed in named *slots*. A slot names an output of a
*projection*: a module in ``scripts/document_projections/`` discovered by file
name. Refreshing a leaf runs every projection its templates slot, writes the
projection's files, and writes the entrypoints, so adding a deterministic page
to every leaf of a type takes a projection module, one slot line in the
template, and one ``refresh --all``.

Template language (line oriented; everything else is copied verbatim):

``%@ region NAME``      the leaf's declared region list for this edition
``%@ slot PROJ/OUTPUT`` ``\\input`` of that projection output in this leaf
``%@ input PATH``       ``\\input`` of a required leaf file (``PATH.tex``)
``%@ input? PATH``      the same, omitted when the leaf has no such file
``%@ option NAME``      the fragment ``<type>/<NAME>/<value>.tex`` chosen by the
                        leaf (or the type's default), expanded recursively
``%@ if FIELD``         keep the lines up to the matching ``%@ end`` only when
                        the field resolves non-empty (blocks nest; they close
                        in the file that opens them)
``%% ...``              a template comment, never copied
``@{field}``            the resolved value of a declared metadata field, of
                        a declared option (its chosen value), or of the
                        built-in ``document`` (the leaf's TeX-root path, for a
                        path that must sit inside a macro body, such as
                        ``\\input{@{document}/generation-metadata}%``)

A region entry that looks like a leaf-relative path (no backslash, braces or
whitespace) becomes ``\\input{<document>/<entry>}``; any other string is raw TeX
copied as written, which is how a leaf keeps its own spacing between sections.
Two table entries name a section with more to say about it:

``{ source = PATH, roles = [ROLE, ...] }``  a section with the semantic roles
                        it fulfils (``publication.toml`` structure roles)
``{ component = KEY }`` a proper's component, whose path, kind, modes and
                        dependencies its ``proper-components.toml`` owns

The regions are the leaf's one ordered section list. A type may name a
default role for a region's plain path entries (``section_roles``); the schema
loader derives every section's structure role from the regions, and the
proper component checker reads each component's path from its manifest, so no
other record lists the sections again (guidance/document-schemas.md).
"""

from __future__ import annotations

import importlib
import pkgutil
import re
import tomllib
from dataclasses import dataclass, field, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES_DIR = Path("src/common/document-types")
TYPE_MANIFEST = "type.toml"
TYPE_SCHEMA = 1
TYPE_RECORD = "document-type"
DECLARATION = "document"
PUBLICATION = "publication.toml"
PROVIDERS = ("claude", "gpt")
GENERATED_BY = "tools/tpt document-types refresh"
GENERATED_DIR = "generated"
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FIELD_REFERENCE = re.compile(r"@\{([a-z0-9]+(?:-[a-z0-9]+)*)\}")
DIRECTIVE = re.compile(r"%@\s*(region|slot|input\??|option|if)\s+(\S+)\s*\Z")
END = re.compile(r"%@\s*end\s*\Z")
PATH_ENTRY = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\Z")
OUTPUT_ROLES = ("canonical", "synthesis", "homily")
# A reference every template may make without declaring it.
BUILTIN_FIELDS = ("document",)
RESERVED_TEMPLATE_NAMES = frozenset({"main.tex", "synthesis.tex", "homily.tex"})


class DocumentTypeError(ValueError):
    """A type, declaration or template that cannot produce a sound entrypoint."""


# --- Types --------------------------------------------------------------------


@dataclass(frozen=True)
class Edition:
    name: str
    role: str
    template: Path
    entrypoint: str
    fields: dict[str, str | None]  # name -> default; None is required
    regions: dict[str, bool]  # name -> required
    options: dict[str, str | None]  # name -> default value; None is required
    # region -> the structure role of its plain path entries
    section_roles: dict[str, str] = field(default_factory=dict)

    def names(self) -> set[str]:
        return set(self.fields) | set(self.regions) | set(self.options)


@dataclass(frozen=True)
class DocumentType:
    id: str
    path: Path
    description: str
    kinds: tuple[str, ...]
    editions: dict[str, Edition]

    def option_values(self, option: str) -> tuple[str, ...]:
        directory = self.path / option
        if not directory.is_dir():
            return ()
        return tuple(sorted(path.stem for path in directory.glob("*.tex")))


def _string_map(value, where: str) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str) for key, item in value.items()
    ):
        raise DocumentTypeError(f"{where} must be a table of strings")
    return dict(value)


def _string_list(value, where: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise DocumentTypeError(f"{where} must be a list of strings")
    return list(value)


def load_type(path: Path) -> DocumentType:
    """Read and validate one ``type.toml`` and the templates it names."""
    manifest = path / TYPE_MANIFEST
    where = manifest.as_posix()
    try:
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise DocumentTypeError(f"{where}: {exc}") from exc
    allowed = {"schema", "record_type", "id", "description", "kinds", "editions"}
    unknown = set(data) - allowed
    if unknown:
        raise DocumentTypeError(f"{where}: unknown keys {sorted(unknown)}")
    if data.get("schema") != TYPE_SCHEMA or data.get("record_type") != TYPE_RECORD:
        raise DocumentTypeError(f"{where}: needs schema = {TYPE_SCHEMA} and record_type = {TYPE_RECORD!r}")
    identifier = data.get("id")
    if identifier != path.name or not isinstance(identifier, str) or not NAME.match(identifier):
        raise DocumentTypeError(f"{where}: id must equal its directory name, in lower-case words")
    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        raise DocumentTypeError(f"{where}: description is required")
    kinds = tuple(_string_list(data.get("kinds", []), f"{where} kinds"))
    if not kinds:
        raise DocumentTypeError(f"{where}: kinds must name the publication kinds that may opt in")
    raw_editions = data.get("editions")
    if not isinstance(raw_editions, dict) or not raw_editions:
        raise DocumentTypeError(f"{where}: at least one [editions.<name>] table is required")
    editions: dict[str, Edition] = {}
    roles: set[str] = set()
    for name, raw in raw_editions.items():
        at = f"{where} editions.{name}"
        if not NAME.match(name) or not isinstance(raw, dict):
            raise DocumentTypeError(f"{at}: edition names are lower-case words naming a table")
        extra = set(raw) - {"role", "template", "entrypoint", "fields", "optional_fields",
                            "regions", "optional_regions", "options", "section_roles"}
        if extra:
            raise DocumentTypeError(f"{at}: unknown keys {sorted(extra)}")
        role = raw.get("role")
        if role not in OUTPUT_ROLES or role in roles:
            raise DocumentTypeError(f"{at}: role must be one unused of {OUTPUT_ROLES}")
        roles.add(role)
        template = path / str(raw.get("template", ""))
        if not raw.get("template") or not template.is_file() or template.parent != path:
            raise DocumentTypeError(f"{at}: template must name a file in the type directory")
        # A template named like an entrypoint would be discovered as a
        # publication (Make finds every main.tex under src/).
        if template.name in RESERVED_TEMPLATE_NAMES:
            raise DocumentTypeError(f"{at}: name the template <edition>.template.tex, not {template.name}")
        entrypoint = raw.get("entrypoint")
        if not isinstance(entrypoint, str) or "/" in entrypoint or not entrypoint.endswith(".tex"):
            raise DocumentTypeError(f"{at}: entrypoint must be a leaf-level .tex file name")
        fields: dict[str, str | None] = {
            item: None for item in _string_list(raw.get("fields", []), f"{at} fields")}
        for item, default in _string_map(raw.get("optional_fields", {}), f"{at} optional_fields").items():
            fields[item] = default
        regions = {item: True for item in _string_list(raw.get("regions", []), f"{at} regions")}
        regions.update({item: False for item in
                        _string_list(raw.get("optional_regions", []), f"{at} optional_regions")})
        options: dict[str, str | None] = dict(_string_map(raw.get("options", {}), f"{at} options"))
        declared = [*fields, *regions, *options]
        if len(declared) != len(set(declared)) or not all(NAME.match(item) for item in declared):
            raise DocumentTypeError(f"{at}: field, region and option names must be distinct lower-case words")
        if set(declared) & set(BUILTIN_FIELDS):
            raise DocumentTypeError(f"{at}: {sorted(set(declared) & set(BUILTIN_FIELDS))} is a built-in reference")
        section_roles = _string_map(raw.get("section_roles", {}), f"{at} section_roles")
        for region, section_role in section_roles.items():
            if region not in regions or not NAME.match(section_role):
                raise DocumentTypeError(
                    f"{at}: section_roles maps a declared region to a lower-case role, not {region!r}")
        editions[name] = Edition(name, role, template, entrypoint, fields, regions, options,
                                 section_roles)
    found = DocumentType(identifier, path, description.strip(), kinds, editions)
    for edition in editions.values():
        for option, default in edition.options.items():
            values = found.option_values(option)
            if not values:
                raise DocumentTypeError(f"{where}: option {option!r} has no {option}/<value>.tex fragments")
            if default is not None and default not in values:
                raise DocumentTypeError(f"{where}: option {option!r} default {default!r} is not one of {values}")
    return found


def discover_types(root: Path = ROOT) -> dict[str, DocumentType]:
    """Every type, found by directory convention: no shared registry to edit."""
    base = root / TYPES_DIR
    if not base.is_dir():
        return {}
    return {path.name: load_type(path)
            for path in sorted(base.iterdir())
            if (path / TYPE_MANIFEST).is_file()}


# --- Projections --------------------------------------------------------------


@dataclass(frozen=True)
class LeafContext:
    """What a projection may read about the leaf it renders."""

    root: Path
    provider: str
    document: str
    leaf: Path
    kind: str
    type_id: str
    editions: tuple[str, ...]
    # The output keys of this projection that the leaf's templates slot. A
    # projection renders these (and its support files) and need not render
    # outputs no template of this leaf places.
    outputs: tuple[str, ...] = ()


def discover_projections() -> dict[str, object]:
    """Projection modules in ``scripts/document_projections``, keyed by NAME."""
    import document_projections  # noqa: PLC0415

    found: dict[str, object] = {}
    for info in sorted(pkgutil.iter_modules(document_projections.__path__), key=lambda item: item.name):
        if info.name.startswith("_"):
            continue
        module = importlib.import_module(f"document_projections.{info.name}")
        name = getattr(module, "NAME", None)
        outputs = getattr(module, "OUTPUTS", None)
        if not isinstance(name, str) or not NAME.match(name) or name in found:
            raise DocumentTypeError(f"projection module {info.name}: NAME must be a unique lower-case name")
        if name.replace("-", "_") != info.name:
            raise DocumentTypeError(f"projection module {info.name}: file name must spell NAME {name!r}")
        if not isinstance(outputs, dict) or not outputs or not callable(getattr(module, "render", None)):
            raise DocumentTypeError(f"projection {name}: needs OUTPUTS and render(context)")
        found[name] = module
    return found


def template_slots(found: DocumentType, edition: Edition) -> list[str]:
    """Every slot an edition's template can fill, under any option value."""
    slots: list[str] = []
    pending = [edition.template]
    for option in edition.options:
        pending.extend(found.path / option / f"{value}.tex" for value in found.option_values(option))
    for template in pending:
        for line in template.read_text(encoding="utf-8").splitlines():
            match = DIRECTIVE.match(line.strip())
            if match and match.group(1) == "slot" and match.group(2) not in slots:
                slots.append(match.group(2))
    return slots


def slot_path(slot: str, projections: dict[str, object]) -> str:
    name, _, output = slot.partition("/")
    module = projections.get(name)
    if module is None:
        raise DocumentTypeError(f"slot {slot!r} names no projection in scripts/document_projections")
    path = module.OUTPUTS.get(output)  # type: ignore[attr-defined]
    if path is None:
        raise DocumentTypeError(f"slot {slot!r}: projection {name!r} has no output {output!r}")
    return path


# --- Leaf declarations ----------------------------------------------------------


@dataclass(frozen=True)
class Declaration:
    provider: str
    document: str
    leaf: Path
    kind: str
    type: DocumentType
    shared: dict[str, str]
    editions: dict[str, dict]
    outputs: dict[str, str] = field(default_factory=dict)  # role -> entrypoint
    # key -> leaf-relative path of each component in proper-components.toml
    components: dict[str, str] = field(default_factory=dict)

    def context(self, root: Path) -> LeafContext:
        return LeafContext(root, self.provider, self.document, self.leaf, self.kind,
                           self.type.id, tuple(self.editions))


def leaf_identity(root: Path, leaf: Path) -> tuple[str, str]:
    relative = leaf.resolve().relative_to((root / "src").resolve())
    provider, *rest = relative.parts
    if provider not in PROVIDERS or not rest:
        raise DocumentTypeError(f"{leaf}: not a provider publication leaf")
    return provider, Path(*rest).as_posix()


def declaration(root: Path, leaf: Path, types: dict[str, DocumentType] | None = None) -> Declaration | None:
    """The leaf's ``[document]`` opt-in, validated against its type, or None."""
    manifest = leaf / PUBLICATION
    if not manifest.is_file():
        return None
    data = tomllib.loads(manifest.read_text(encoding="utf-8"))
    raw = data.get(DECLARATION)
    if raw is None:
        return None
    where = f"{manifest.relative_to(root).as_posix()} [{DECLARATION}]"
    if not isinstance(raw, dict):
        raise DocumentTypeError(f"{where} must be a table")
    types = discover_types(root) if types is None else types
    identifier = raw.get("type")
    if identifier not in types:
        raise DocumentTypeError(f"{where}: type {identifier!r} is not a directory under {TYPES_DIR}")
    found_type = types[identifier]
    # kind and outputs are derived from the leaf's path and records; the schema
    # loader owns that derivation (and refuses an explicit contradiction).
    import _document_schema  # noqa: PLC0415

    try:
        kind, declared_outputs = _document_schema.derived_kind_and_outputs(root, leaf, data)
    except _document_schema.SchemaError as exc:
        raise DocumentTypeError(f"{where}: {exc}") from exc
    if kind not in found_type.kinds:
        raise DocumentTypeError(f"{where}: type {identifier!r} does not admit publication kind {kind!r}")
    shared: dict[str, str] = {}
    editions: dict[str, dict] = {}
    for key, value in raw.items():
        if key == "type":
            continue
        if isinstance(value, dict):
            if key not in found_type.editions:
                raise DocumentTypeError(f"{where}: {identifier!r} has no edition {key!r}")
            editions[key] = value
        elif isinstance(value, str):
            shared[key] = value
        else:
            raise DocumentTypeError(f"{where}: {key!r} must be a string field or an edition table")
    if not editions:
        raise DocumentTypeError(f"{where}: declare at least one [{DECLARATION}.<edition>] table")
    usable = set().union(*(found_type.editions[name].fields for name in editions),
                         *(found_type.editions[name].options for name in editions))
    for key in shared:
        if key not in usable:
            raise DocumentTypeError(f"{where}: shared {key!r} is no field or option of a declared edition")
    outputs = {item.get("role"): item.get("entrypoint")
               for item in declared_outputs if isinstance(item, dict)}
    components = _component_paths(leaf)
    for name in editions:
        edition = found_type.editions[name]
        if outputs.get(edition.role) != edition.entrypoint:
            raise DocumentTypeError(
                f"{where}: edition {name!r} needs a [[outputs]] role {edition.role!r} "
                f"with entrypoint {edition.entrypoint!r}")
        for key, value in editions[name].items():
            if key not in edition.names():
                raise DocumentTypeError(f"{where}: {name}.{key} is not declared by {identifier!r}")
            if key in edition.regions:
                if not isinstance(value, list):
                    raise DocumentTypeError(f"{where}: region {name}.{key} must be a list")
                for item in value:
                    _region_entry(item, components, f"{where}: region {name}.{key}")
            elif not isinstance(value, str):
                raise DocumentTypeError(f"{where}: {name}.{key} must be a string")
    # A companion declared among the outputs but not written yet may gain its
    # edition table later; an entrypoint that exists must be generated.
    for role, entry in outputs.items():
        claimed = [name for name in editions if found_type.editions[name].role == role]
        if isinstance(entry, str) and not claimed and (leaf / entry).is_file():
            raise DocumentTypeError(
                f"{where}: output {role!r} has an entrypoint ({entry}) but no "
                f"[{DECLARATION}.<edition>] table, so it would stay hand-written")
    provider, document = leaf_identity(root, leaf)
    return Declaration(provider, document, leaf, kind, found_type, shared, editions,
                       {key: value for key, value in outputs.items() if isinstance(key, str)},
                       components)


COMPONENTS = "proper-components.toml"


def _component_paths(leaf: Path) -> dict[str, str]:
    """Each proper component's path, keyed as a region's ``component`` names it."""
    path = leaf / COMPONENTS
    if not path.is_file():
        return {}
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return {item["key"]: item["path"] for item in data.get("components", [])
            if isinstance(item, dict) and isinstance(item.get("key"), str)
            and isinstance(item.get("path"), str)}


def _region_entry(item, components: dict[str, str], where: str) -> None:
    if isinstance(item, str):
        path = item if item.endswith(".tex") else item + ".tex"
        named = {value: key for key, value in components.items()}
        if PATH_ENTRY.match(item) and path in named:
            # The component's manifest owns its path; a region names it by key.
            raise DocumentTypeError(f"{where}: place component {named[path]!r} as "
                                    f"{{ component = {named[path]!r} }}, not by its path")
        return
    if not isinstance(item, dict):
        raise DocumentTypeError(f"{where}: an entry is a string or a table")
    if set(item) == {"component"}:
        key = item["component"]
        if key not in components:
            raise DocumentTypeError(f"{where}: no component {key!r} in {COMPONENTS}")
        if not components[key].endswith(".tex") or components[key].startswith(GENERATED_DIR + "/"):
            raise DocumentTypeError(
                f"{where}: component {key!r} is not an authored .tex section a region can place")
        return
    if set(item) - {"source", "roles"} or "source" not in item:
        raise DocumentTypeError(
            f"{where}: a table entry is {{ source = PATH, roles = [...] }} or {{ component = KEY }}")
    source = item["source"]
    roles = item.get("roles", [])
    if not isinstance(source, str) or not PATH_ENTRY.match(source):
        raise DocumentTypeError(f"{where}: source {source!r} must be a leaf-relative path")
    _region_entry(source, components, where)
    if (not isinstance(roles, list) or not all(isinstance(role, str) and NAME.match(role) for role in roles)
            or len(roles) != len(set(roles))):
        raise DocumentTypeError(f"{where}: roles of {source!r} must be distinct lower-case words")


def _entry_path(decl: Declaration, item) -> str | None:
    """The leaf-relative section path a region entry places, or None for raw TeX."""
    if isinstance(item, dict):
        if "component" in item:
            return decl.components[item["component"]].removesuffix(".tex")
        return item["source"].removesuffix(".tex")
    return item.removesuffix(".tex") if PATH_ENTRY.match(item) else None


@dataclass(frozen=True)
class Section:
    """One section a leaf's regions place, as the schema and gates read it."""

    source: str  # leaf-relative, with .tex
    roles: tuple[str, ...]
    outputs: tuple[str, ...]  # output roles of the editions that place it
    component: str | None = None


def sections(decl: Declaration) -> list[Section]:
    """The leaf's one section list: every region entry naming a file, in order.

    A plain path entry takes its region's default role (``section_roles``), a
    ``{ source, roles }`` entry its own roles, and a component entry none: its
    meaning is its proper-components kind. A section placed by more than one
    edition is listed once, with every edition's output role.
    """
    found: dict[str, Section] = {}
    for name, local in decl.editions.items():
        edition = decl.type.editions[name]
        for region in edition.regions:
            for item in local.get(region, []) if isinstance(local.get(region), list) else []:
                path = _entry_path(decl, item)
                if path is None:
                    continue
                if isinstance(item, dict) and "component" in item:
                    roles: tuple[str, ...] = ()
                    component = item["component"]
                elif isinstance(item, dict):
                    roles, component = tuple(item.get("roles", [])), None
                else:
                    default = edition.section_roles.get(region)
                    roles, component = ((default,) if default else ()), None
                source = path + ".tex"
                held = found.get(source)
                if held is None:
                    found[source] = Section(source, roles, (edition.role,), component)
                    continue
                if held.roles != roles or held.component != component:
                    raise DocumentTypeError(
                        f"{decl.document}: {source} is placed with different roles in different regions")
                if edition.role not in held.outputs:
                    found[source] = replace(held, outputs=held.outputs + (edition.role,))
    return list(found.values())


def opted_in_leaves(root: Path = ROOT) -> list[Path]:
    """Every provider leaf whose publication.toml declares a document type."""
    leaves = []
    for provider in PROVIDERS:
        base = root / "src" / provider
        if not base.is_dir():
            continue
        for manifest in sorted(base.rglob(PUBLICATION)):
            text = manifest.read_text(encoding="utf-8")
            if re.search(rf"^\[{DECLARATION}\]\s*$", text, re.M):
                leaves.append(manifest.parent)
    return leaves


# --- Rendering ----------------------------------------------------------------


def _resolved(decl: Declaration, edition: Edition, name: str, kind: str):
    local = decl.editions[edition.name]
    if name in local:
        return local[name]
    if kind != "region" and name in decl.shared:
        return decl.shared[name]
    default = {"field": edition.fields, "option": edition.options}.get(kind, {}).get(name)
    if kind == "region":
        if edition.regions.get(name):
            raise DocumentTypeError(f"{decl.document}: edition {edition.name!r} requires region {name!r}")
        return []
    if default is None:
        raise DocumentTypeError(f"{decl.document}: edition {edition.name!r} requires {kind} {name!r}")
    return default


def _leaf_file(decl: Declaration, entry: str) -> Path:
    path = decl.leaf / (entry if entry.endswith(".tex") else entry + ".tex")
    if ".." in Path(entry).parts or not path.is_file():
        raise DocumentTypeError(f"{decl.document}: no leaf file {entry!r}")
    return path


def _input(decl: Declaration, entry: str) -> str:
    _leaf_file(decl, entry)
    return "\\input{" + decl.document + "/" + entry.removesuffix(".tex") + "}"


def _expand(decl: Declaration, edition: Edition, template: Path, projections: dict,
            slots: list[str], depth: int = 0) -> list[str]:
    if depth > 8:
        raise DocumentTypeError(f"{template}: option fragments nest too deeply")
    lines: list[str] = []
    kept: list[bool] = []  # one entry per open ``%@ if`` block
    for line in template.read_text(encoding="utf-8").splitlines():
        if line.startswith("%%"):
            continue
        if END.match(line.strip()):
            if not kept:
                raise DocumentTypeError(f"{template}: %@ end without %@ if")
            kept.pop()
            continue
        match = DIRECTIVE.match(line.strip())
        if line.lstrip().startswith("%@") and match is None:
            raise DocumentTypeError(f"{template}: malformed directive {line.strip()!r}")
        if match is not None and match.group(1) == "if":
            kept.append(bool(str(_field(decl, edition, match.group(2))).strip()))
            continue
        if not all(kept):
            continue
        if match is None:
            lines.append(FIELD_REFERENCE.sub(
                lambda found: str(_field(decl, edition, found.group(1))), line))
            continue
        verb, argument = match.groups()
        if verb == "region":
            if argument not in edition.regions:
                raise DocumentTypeError(f"{template}: region {argument!r} is not declared by its edition")
            for entry in _resolved(decl, edition, argument, "region"):
                path = _entry_path(decl, entry)
                lines.append(_input(decl, path) if path is not None else entry)
        elif verb == "slot":
            slots.append(argument)
            path = slot_path(argument, projections)
            lines.append("\\input{" + decl.document + "/" + path.removesuffix(".tex") + "}")
        elif verb == "input":
            lines.append(_input(decl, argument))
        elif verb == "input?":
            if (decl.leaf / (argument + ".tex")).is_file():
                lines.append(_input(decl, argument))
        else:
            if argument not in edition.options:
                raise DocumentTypeError(f"{template}: option {argument!r} is not declared by its edition")
            value = _resolved(decl, edition, argument, "option")
            if value not in decl.type.option_values(argument):
                raise DocumentTypeError(
                    f"{decl.document}: option {argument}={value!r} is not one of "
                    f"{decl.type.option_values(argument)}")
            lines.extend(_expand(decl, edition, decl.type.path / argument / f"{value}.tex",
                                 projections, slots, depth + 1))
    if kept:
        raise DocumentTypeError(f"{template}: %@ if without %@ end")
    return lines


def _field(decl: Declaration, edition: Edition, name: str) -> str:
    if name == "document":
        return decl.document
    if name in edition.options:
        # The chosen value, already one of the type's own fragment names, so a
        # template may build a path from it (``shared/@{form}-ceremony``).
        return _resolved(decl, edition, name, "option")
    if name not in edition.fields:
        raise DocumentTypeError(f"{edition.template}: field {name!r} is not declared by its edition")
    return _resolved(decl, edition, name, "field")


def header(decl: Declaration, edition: Edition) -> str:
    return (f"% Generated by {GENERATED_BY} from "
            f"{TYPES_DIR.as_posix()}/{decl.type.id}/{edition.template.name}\n"
            f"% and this leaf's publication.toml [{DECLARATION}] table. Do not edit.\n")


def render_edition(decl: Declaration, edition_name: str, projections: dict | None = None) -> tuple[str, list[str]]:
    """The entrypoint text for one edition, and the slots it filled."""
    projections = discover_projections() if projections is None else projections
    edition = decl.type.editions[edition_name]
    slots: list[str] = []
    body = _expand(decl, edition, edition.template, projections, slots)
    return header(decl, edition) + "\n".join(body) + "\n", slots


def render_leaf(root: Path, decl: Declaration, projections: dict | None = None) -> dict[str, str]:
    """Every generated file of one opted-in leaf, keyed leaf-relative.

    Entrypoints for every declared edition, then each projection slotted by
    any of them. A projection runs once per leaf and returns whole files.
    """
    projections = discover_projections() if projections is None else projections
    files: dict[str, str] = {}
    slotted: dict[str, dict[str, None]] = {}
    for name in decl.editions:
        text, slots = render_edition(decl, name, projections)
        files[decl.type.editions[name].entrypoint] = text
        for slot in slots:
            projection, _, output = slot.partition("/")
            slotted.setdefault(projection, {})[output] = None
    for name, outputs in slotted.items():
        module = projections[name]
        context = replace(decl.context(root), outputs=tuple(outputs))
        produced = module.render(context)  # type: ignore[attr-defined]
        missing = {module.OUTPUTS[output] for output in outputs} - set(produced)  # type: ignore[attr-defined]
        if missing:
            raise DocumentTypeError(f"projection {name} did not produce {sorted(missing)}")
        for path, text in produced.items():
            if path in files and files[path] != text:
                raise DocumentTypeError(f"{decl.document}: two generators disagree about {path}")
            if Path(path).is_absolute() or ".." in Path(path).parts:
                raise DocumentTypeError(f"projection {name} wrote outside its leaf: {path}")
            files[path] = text
    return files


@dataclass(frozen=True)
class Refresh:
    leaf: str
    changed: tuple[str, ...]
    current: tuple[str, ...]
    # Authored files a slotted projection owns the subject of: an authored
    # copy of a generated page. A projection reports them through an optional
    # ``authored_conflicts(context, generated)`` hook.
    conflicts: tuple[str, ...] = ()
    # Files under the leaf's generated/ that nothing generates any more, such
    # as a page whose slot left the leaf's type. ``refresh`` deletes them;
    # ``--check`` reports them.
    orphans: tuple[str, ...] = ()


def refresh(root: Path, leaves: list[Path], *, check: bool,
            projections: dict | None = None) -> list[Refresh]:
    """Write (or, with ``check``, compare) every generated file of each leaf."""
    types = discover_types(root)
    projections = discover_projections() if projections is None else projections
    results = []
    for leaf in leaves:
        decl = declaration(root, leaf, types)
        if decl is None:
            raise DocumentTypeError(f"{leaf.relative_to(root)}: declares no [{DECLARATION}] type")
        files = render_leaf(root, decl, projections)
        conflicts = []
        for name in sorted({slot.partition("/")[0] for edition in decl.editions
                            for slot in render_edition(decl, edition, projections)[1]}):
            hook = getattr(projections[name], "authored_conflicts", None)
            if hook is not None:
                conflicts.extend(hook(decl.context(root), frozenset(files)))
        generated = leaf / GENERATED_DIR
        orphans = sorted(path.relative_to(leaf).as_posix() for path in generated.rglob("*")
                         if path.is_file() and path.relative_to(leaf).as_posix() not in files) \
            if generated.is_dir() else []
        if not check:
            for relative in orphans:
                (leaf / relative).unlink()
        changed, current = [], []
        for relative, text in sorted(files.items()):
            path = leaf / relative
            held = path.read_text(encoding="utf-8") if path.is_file() else None
            if held == text:
                current.append(relative)
                continue
            changed.append(relative)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
        results.append(Refresh(f"{decl.provider}/{decl.document}", tuple(changed), tuple(current),
                               tuple(conflicts), tuple(orphans)))
    return results


def generated_files(root: Path, leaf: Path) -> list[str]:
    """Leaf-relative paths the leaf's declaration generates (for gates)."""
    decl = declaration(root, leaf)
    if decl is None:
        return []
    return sorted(render_leaf(root, decl))


class Assembly:
    """One operation's current document templates and deterministic content.

    Carried generated bytes are snapshots, never rendering inputs. Entrypoint
    files remain discovery placeholders for the existing publication tools.
    Authored files retain their exact bytes. The operation owns this cache;
    a new build creates a new Assembly rather than retaining it globally.
    """

    def __init__(self, root: Path = ROOT, *, projections: dict | None = None):
        self.root = Path(root).resolve()
        self.projections = projections
        self._files: dict[Path, dict[Path, str]] = {}
        self._owners: dict[Path, Path | None] = {}
        self._dependencies: dict[Path, set[Path]] = {}
        self._prepared: set[str] = set()

    def owner(self, path: Path) -> Path | None:
        path = Path(path).absolute()
        if path in self._owners:
            return self._owners[path]
        try:
            relative = path.relative_to(self.root / "src")
        except ValueError:
            return None
        if not relative.parts or relative.parts[0] not in PROVIDERS:
            return None
        boundary = self.root / "src" / relative.parts[0]
        leaf = next((parent for parent in path.parents
                     if parent != boundary and boundary in parent.parents
                     and (parent / PUBLICATION).is_file()), None)
        self._owners[path] = leaf
        return leaf

    def files(self, leaf: Path) -> dict[Path, str]:
        """Absolute virtual paths, with structural/authorship defects refused."""
        leaf = Path(leaf).resolve()
        if leaf not in self._files:
            decl = declaration(self.root, leaf)
            if decl is None:
                self._files[leaf] = {}
            else:
                projections = self.projections
                if projections is None:
                    projections = discover_projections()
                for name in {slot.partition("/")[0] for edition in decl.editions
                             for slot in render_edition(decl, edition, projections)[1]}:
                    prepare = getattr(projections[name], "prepare", None)
                    if prepare is not None and name not in self._prepared:
                        prepare(self.root)
                        self._prepared.add(name)
                generated = render_leaf(self.root, decl, projections)
                for name in {slot.partition("/")[0] for edition in decl.editions
                             for slot in render_edition(decl, edition, projections)[1]}:
                    hook = getattr(projections[name], "authored_conflicts", None)
                    conflicts = hook(decl.context(self.root), frozenset(generated)) if hook else []
                    if conflicts:
                        raise DocumentTypeError(f"{decl.document}: authored generated content: {conflicts}")
                directory = leaf / GENERATED_DIR
                orphans = [path.relative_to(leaf).as_posix() for path in directory.rglob("*")
                           if path.is_file() and path.relative_to(leaf).as_posix() not in generated]
                if orphans:
                    raise DocumentTypeError(f"{decl.document}: orphaned generated files: {sorted(orphans)}")
                self._files[leaf] = {leaf / name: text for name, text in generated.items()}
        return self._files[leaf]

    def generated(self, path: Path) -> str | None:
        path = Path(path).absolute()
        leaf = self.owner(path)
        return self.files(leaf).get(path) if leaf is not None else None

    def is_file(self, path: Path) -> bool:
        return self.generated(path) is not None or Path(path).is_file()

    def read_text(self, path: Path) -> str:
        text = self.generated(path)
        return text if text is not None else Path(path).read_text(encoding="utf-8")

    def read_bytes(self, path: Path) -> bytes:
        text = self.generated(path)
        return text.encode("utf-8") if text is not None else Path(path).read_bytes()

    def dependencies(self, leaf: Path) -> set[Path]:
        """Canonical template/projection inputs, separate from virtual bytes."""
        leaf = Path(leaf).resolve()
        if leaf in self._dependencies:
            return self._dependencies[leaf]
        decl = declaration(self.root, leaf)
        if decl is None:
            return set()
        paths = {leaf / PUBLICATION, *decl.type.path.rglob("*.tex"),
                 decl.type.path / TYPE_MANIFEST}
        software = self.root / "scripts/_document_types.py"
        if software.is_file():
            paths.add(software)
        if (leaf / COMPONENTS).is_file():
            paths.add(leaf / COMPONENTS)
        projections = self.projections if self.projections is not None else discover_projections()
        for name in {slot.partition("/")[0] for edition in decl.editions
                     for slot in render_edition(decl, edition, projections)[1]}:
            hook = getattr(projections[name], "dependencies", None)
            if hook is not None:
                paths.update(hook(decl.context(self.root)))
        paths.difference_update(self.files(leaf))
        self._dependencies[leaf] = paths
        return paths

    def content_dependencies(self, path: Path) -> set[Path]:
        """Projection inputs only when this generated content is actually read.

        A generated entrypoint is a skeleton; its templates are render inputs.
        A homily reaching no deterministic page consequently gains no biblical
        chronology content dependency merely by sharing that page's leaf.
        """
        leaf = self.owner(path)
        if leaf is None or Path(path).absolute() not in self.files(leaf):
            return set()
        decl = declaration(self.root, leaf)
        if decl is None or Path(path).name in {
                decl.type.editions[name].entrypoint for name in decl.editions}:
            return set()
        return {dependency for dependency in self.dependencies(leaf)
                if not dependency.is_relative_to(decl.type.path)
                and dependency not in {leaf / PUBLICATION, leaf / COMPONENTS,
                                       self.root / "scripts/_document_types.py"}
                and dependency.relative_to(self.root).parts[0] in {"src", "scripts"}}


def stage(root: Path, provider: str, entrypoint: str, destination: Path) -> Path:
    """Materialize only generated bytes for native Make, outside tracked src/."""
    import hashlib
    import json
    import os

    root, destination = root.resolve(), Path(os.path.abspath(destination))
    if provider not in PROVIDERS or Path(entrypoint).is_absolute() or ".." in Path(entrypoint).parts:
        raise DocumentTypeError("stage needs a provider-relative entrypoint")
    if (destination == root or root.is_relative_to(destination)
            or destination.is_relative_to(root / "src")
            or destination.is_relative_to(root / ".git")):
        raise DocumentTypeError("assembly output must not contain the repository or canonical sources")

    def no_links(path: Path) -> None:
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise DocumentTypeError("assembly output must not traverse a symlink")

    no_links(destination)
    owner = {"schema": 1, "provider": provider, "entrypoint": entrypoint}
    owner_path = destination / "owner.json"
    previous = []
    if destination.exists():
        if not destination.is_dir():
            raise DocumentTypeError("assembly output is not a directory")
        if any(destination.iterdir()):
            no_links(owner_path)
            try:
                held = json.loads(owner_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise DocumentTypeError("refusing an unowned nonempty assembly output") from exc
            if held != owner:
                raise DocumentTypeError("assembly output belongs to a different edition")
            manifest_path = destination / "manifest.json"
            no_links(manifest_path)
            try:
                previous = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise DocumentTypeError("assembly output has no valid owned manifest") from exc
    if not isinstance(previous, list):
        raise DocumentTypeError("assembly output manifest is not a file list")
    previous_paths = set()
    prefix = f"src/{provider}/{Path(entrypoint).parent.as_posix()}/"
    for row in previous:
        name = row.get("path") if isinstance(row, dict) else None
        digest = row.get("sha256") if isinstance(row, dict) else None
        if (not isinstance(name, str) or not name.startswith(prefix)
                or Path(name).is_absolute() or any(part in {"", ".", ".."} for part in name.split("/"))
                or name in previous_paths or not isinstance(digest, str)
                or not re.fullmatch(r"[0-9a-f]{64}", digest)):
            raise DocumentTypeError("assembly output manifest has an invalid owned path")
        previous_paths.add(name)
        target = destination / name
        no_links(target)
        if target.exists() and (not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest):
            raise DocumentTypeError("refusing to overwrite modified staged content")
    entry = root / "src" / provider / entrypoint
    assembly = Assembly(root)
    leaf = assembly.owner(entry)
    files = assembly.files(leaf) if leaf else {}
    for path in files:
        name = path.relative_to(root).as_posix()
        target = destination / name
        no_links(target)
        if target.exists() and name not in previous_paths:
            raise DocumentTypeError("refusing to overwrite an unowned assembly file")
    for name in ("owner.json", "manifest.json", "entrypoint", "files"):
        no_links(destination / name)
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for path, text in sorted(files.items()):
        relative = path.relative_to(root)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = text.encode("utf-8")
        if not target.is_file() or target.read_bytes() != payload:
            target.write_bytes(payload)
        manifest.append({"path": relative.as_posix(), "sha256": hashlib.sha256(payload).hexdigest()})
    for name in previous_paths - {path.relative_to(root).as_posix() for path in files}:
        target = destination / name
        if target.is_file():
            target.unlink()
    selected = destination / entry.relative_to(root) if entry in files else entry
    values = {
        "owner.json": json.dumps(owner, sort_keys=True, separators=(",", ":")) + "\n",
        "manifest.json": json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        "entrypoint": str(selected) + "\n",
        "files": "".join(str(destination / path.relative_to(root)) + "\n" for path in sorted(files)),
    }
    for name, text in values.items():
        path = destination / name
        if not path.is_file() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
    return selected


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stage current document assembly for native Make.")
    parser.add_argument("stage", choices=("stage",))
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--provider", required=True, choices=PROVIDERS)
    parser.add_argument("--entrypoint", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    stage(args.root, args.provider, args.entrypoint, args.out)
