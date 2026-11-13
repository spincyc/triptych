"""Selected Catena, reading-plan and paragraph products from canonical data.

The discovery catalog contains addresses and counts only. The existing owners
still decide author eligibility, text admission, translation voice, Scripture
numbering, snippets and printed versus projected paragraphs.
"""
from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager, ExitStack
import csv
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import sys
from unittest.mock import patch

import _canon
import _catena
import _catena_scope
import _loci
import _paragraphs
import _psalms
import _reader_bibles
from _indexed_source_library import indexed_records

CATALOG_PATH = "src/index/commentary/catalog.json"
SCHEMA = "triptych-reader-commentary-addresses/v1"


def _json(value) -> bytes:
    return _catena._serialise(value).encode("utf-8")


def build_catalog(root: Path) -> dict:
    """Extract a thin address table from the full authoritative producers."""
    root = Path(root)
    destination = root / ".scratch/commentary-reader/catalog-derivation"
    _catena._SOURCES_CACHE.pop(root, None)
    _catena._INDEX_CACHE.pop(root, None)
    directory, products, _ = _catena._structure_files(root, destination)
    catalog = json.loads(products[directory / "index.json"])
    catalog.pop("absences")  # The source-owned reason is read when requested.
    chapters = {}
    for path, body in products.items():
        if path.parent == directory or path.parent.name in {"text", "scripture"}:
            continue
        chapter = json.loads(body)
        chapters.setdefault(path.parent.name, {})[str(chapter["chapter"])] = [
            row["id"] for row in chapter["fragments"]]
    paragraph_directory, paragraph_products, _ = _catena._paragraph_files(root, destination)
    absent_works = {work for work, _ in _catena.absences_by_work(root)}
    absence_editions = sorted(identifier for identifier, edition
                              in _catena._sources_cache(root).editions.items()
                              if edition.get("work_id") in absent_works)
    return {"schema": SCHEMA, "catena": catalog, "chapters": chapters,
            "absence_editions": absence_editions,
            "paragraphs": json.loads(paragraph_products[paragraph_directory / "index.json"])}


def refresh_metadata(root: Path) -> list[str]:
    """Explicit maintenance operation, called before the generic index refresh."""
    products = {_reader_bibles.METADATA_PATH: _reader_bibles.build_metadata(root),
                CATALOG_PATH: build_catalog(root)}
    for relative, payload in products.items():
        target = Path(root) / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_json(payload))
    return list(products)


def check_metadata(root: Path) -> list[str]:
    """Full replay; no repair or adoption of changed counts during a read."""
    expected = {_reader_bibles.METADATA_PATH: _reader_bibles.build_metadata(root),
                CATALOG_PATH: build_catalog(root)}
    return [relative for relative, payload in expected.items()
            if not (Path(root) / relative).is_file()
            or (Path(root) / relative).read_bytes() != _json(payload)]


class _Records(Mapping):
    def __init__(self, index, kind, ids=None):
        self.index, self.kind = index, kind
        self.ids = None if ids is None else tuple(ids)
        self.data = indexed_records(index)

    def __getitem__(self, identifier):
        if self.index.record_kind(identifier) != self.kind:
            raise KeyError(identifier)
        return self.data[identifier]

    def __contains__(self, identifier):
        try:
            return self.index.record_kind(identifier) == self.kind
        except KeyError:
            return False

    def __iter__(self):
        return iter(self.index.records(self.kind) if self.ids is None else self.ids)

    def __len__(self):
        return len(self.index.records(self.kind) if self.ids is None else self.ids)


def _sources(index, *, editions=None):
    return _catena.Sources(*[_Records(index, kind, editions if kind == "edition" else None)
                             for kind in ("work", "edition", "artifact", "segment", "passage")])


def _yaml_bytes(body):
    import yaml
    return yaml.load(body, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def _clear_psalms():
    for name in ("_concordance", "witness_merges", "_english"):
        function = getattr(_psalms, name, None)
        if hasattr(function, "cache_clear"):
            function.cache_clear()


@contextmanager
def _context(root, index, catalog):
    """Keep source reads verified, root-scoped and free of prior process caches."""
    original_books = catalog["catena"]["canon"]
    books = [{key: value for key, value in row.items() if key != "path"}
             for row in original_books]
    root = Path(root)
    reference = root / "src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts"
    parsed = {}

    def load_yaml(path):
        relative = Path(path).relative_to(root).as_posix()
        if relative not in parsed:
            parsed[relative] = _yaml_bytes(index.read(relative))
        return parsed[relative]

    with _reader_bibles.READ_LOCK, ExitStack() as stack:
        _clear_psalms()
        stack.enter_context(index.verified_reads())
        stack.enter_context(patch.object(_catena, "_load_yaml", load_yaml))
        stack.enter_context(patch.object(_canon, "books", lambda root=root: books))
        stack.enter_context(patch.object(_paragraphs, "PROJECTION_ROOT", reference))
        stack.enter_context(patch.object(_psalms, "CONCORDANCE_ROOT", reference))
        try:
            yield
        finally:
            _clear_psalms()


def _catalog(index):
    data = json.loads(index.read(CATALOG_PATH))
    if data.get("schema") != SCHEMA:
        raise ValueError(f"{CATALOG_PATH}: unsupported commentary address index")
    return data


def _scope(root, sources):
    scope = _catena_scope.Scope(root, works=sources.works)
    if scope.errors:
        raise _catena.CatenaError("; ".join(scope.errors))
    return scope


def _text(row):
    return {"id": row["id"],
            **{key: row.get(key, "") for key in _catena.CARRIED_WITH_TEXT},
            **{key: row[key] for key in _catena.OPTIONAL_CARRIED_WITH_TEXT if key in row}}


def _metadata(row):
    carried = {*_catena.CARRIED_WITH_TEXT, *_catena.OPTIONAL_CARRIED_WITH_TEXT}
    return {**{key: value for key, value in row.items() if key not in carried},
            "text_words": len(str(row.get("text", "")).split())}


def _validate_selected(root, sources, edges, identifiers):
    """Apply the owning publication gate before materializing selected words."""
    problems = []
    if edges.get("numbering") != _catena._projection.CANONICAL:
        problems.append("Catena edges do not declare canonical Vulgate numbering")
    for fragment in edges.get("fragments", []):
        identifier = fragment.get("passage_id")
        if identifier not in identifiers:
            continue
        if fragment.get("numbering") != _catena._projection.CANONICAL:
            problems.append(f"{identifier}: fragment does not declare canonical numbering")
        problems.extend(_catena._passage_errors(sources, identifier, identifier,
                         fragment["work_id"], fragment, root=root))
    if problems:
        raise _catena.CatenaError("; ".join(problems))


def _catena_product(relative, root, index, catalog):
    suffix = relative.removeprefix("structure/catena/")
    if suffix == "index.json":
        edges = _catena.load_edges(root)
        sources = _sources(index, editions=catalog["absence_editions"])
        _scope(root, sources)
        return _json({**catalog["catena"],
                      "absences": _catena.absent_by_work(root, sources=sources, edges=edges)})
    books = {book["path"]: book for book in catalog["catena"]["canon"]}
    if suffix.startswith("scripture/") and suffix.endswith(".json"):
        book = books.get(suffix[len("scripture/"):-5])
        if book is None:
            return None
        with _reader_bibles.bible_context(root, index) as selected:
            offered = {row["id"] for row in _catena.offered_editions(root)}
            editions = [(reader, selected(reader.id)) for reader in _loci.edition_readers()
                        if reader.id in offered]
            return _json(_catena.scripture_for_book(root, book, editions))
    edges = _catena.load_edges(root)
    sources = _sources(index)
    scope = _scope(root, sources)
    if suffix.startswith("text/") and suffix.endswith(".json"):
        identifier = suffix[len("text/"):-5]
        if not _catena.SAFE_ID.fullmatch(identifier):
            return None
        edge = next((row for row in edges.get("fragments", [])
                     if row.get("passage_id") == identifier), None)
        if edge is None or not scope.allowed_work(edge["work_id"]):
            return None
        _validate_selected(root, sources, edges, {identifier})
        rows = _catena.fragments_for_book(root, edge["extent"]["token"],
            scope=scope, sources=sources, edges=edges, passage_ids={identifier})
        if len(rows) != 1:
            raise ValueError(f"{identifier}: indexed fragment did not resolve uniquely")
        return _json(_text(rows[0]))
    parts = suffix.split("/")
    if len(parts) != 2 or not parts[1].endswith(".json") or not parts[1][:-5].isdigit():
        return None
    folder, leaf = parts
    book = books.get(folder)
    chapter = int(leaf[:-5])
    if book is None or leaf != _canon.chapter_name(chapter, catalog["catena"]["chapter_digits"]):
        return None
    present = catalog["chapters"].get(folder, {})
    if str(chapter) not in present:
        return None
    identifiers = present[str(chapter)]
    _validate_selected(root, sources, edges, set(identifiers))
    rows = _catena.fragments_for_book(root, book["token"], scope=scope,
        sources=sources, edges=edges, passage_ids=set(identifiers))
    if {row["id"] for row in rows} != set(identifiers):
        raise ValueError(f"{relative}: commentary membership index is stale")
    here = [_metadata(row) for row in rows]
    discovery = _catena._load_yaml(root / _catena.INDEX_RELATIVE)
    leads = _catena.leads_for_book(root, book["token"], book["name"], scope=scope, discovery=discovery)
    blocked = _catena.blocked_for_book(root, book["token"], scope=scope, edges=edges)
    standing = _catena.chapters_touched(root,
        [{"id": str(number), "extent": row["extent"]} for number, row in enumerate(blocked)], [chapter])
    refused = {edition: [row for row in entries if row["chapter"] == chapter]
               for edition, entries in _catena.refusals_for_book(root, book["token"]).items()}
    shared, slim = _catena._fold_shared(here)
    return _json({"token": book["token"], "name": book["name"], "chapter": chapter,
        "chapters": book["last_chapter"], "numbering": _catena._projection.CANONICAL,
        "text_prefix": "structure/catena/text/", "sources": shared, "fragments": slim,
        "leads": leads.get(str(chapter)) or [],
        "refusals": {edition: rows for edition, rows in refused.items() if rows},
        "blocked": [blocked[int(number)] for number in standing[chapter]],
        "languages": sorted({row["language"] for row in here if row.get("language")})})


def _reading_plan(root):
    name = "_reader_reading_plan"
    loader = importlib.machinery.SourceFileLoader(name, str(root / "tools/reading-plan"))
    spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


def _reading_product(relative, root, index):
    slug = relative.removeprefix("structure/readings/").removesuffix(".json")
    if not _catena.SAFE_ID.fullmatch(slug):
        return None
    source = f"src/sources/reading-plans/{slug}.yaml"
    if source not in index.paths(prefix="src/sources/reading-plans/", suffix=".yaml"):
        return None
    module = _reading_plan(root)
    document = module.load_plan(root / source)
    book_paths = index.paths(prefix="src/sources/works/english-college-of-douay/douay-rheims-bible/editions/challoner-gutenberg-1581/artifacts/", suffix="/book-index.tsv")
    if len(book_paths) != 1:
        raise ValueError("reading plan requires exactly one Douay book index")
    tokens = {row["modern_name"]: row["token"] for row in
              csv.DictReader(io.StringIO(index.read(book_paths[0]).decode()), delimiter="\t")}
    with _reader_bibles.bible_context(root, index) as selected:
        problems = module.check_plan(root / source, document, tokens,
                                     selected("douay-rheims").chapters)
        if problems:
            raise ValueError("; ".join(problems))
        return _json(module.plan_structure(document, tokens))


def _paragraph_product(relative, root, index, catalog):
    suffix = relative.removeprefix("structure/paragraphs/")
    if suffix == "index.json":
        return _json(catalog["paragraphs"])
    parts = suffix.split("/")
    if len(parts) != 3 or not parts[-1].endswith(".json") or not parts[-1][:-5].isdigit():
        return None
    edition, folder, leaf = parts
    if edition not in catalog["paragraphs"]["editions"]:
        return None
    book = next((row for row in catalog["catena"]["canon"] if row["path"] == folder), None)
    chapter = int(leaf[:-5])
    if book is None or leaf != _canon.chapter_name(chapter, catalog["catena"]["chapter_digits"]):
        return None
    register = _loci._bible_register()
    artifacts = root / "src/sources/works" / register.EDITIONS[edition]["artifacts"]
    selected = _reader_bibles.bible(root, index, edition)
    target = book["token"], chapter
    carrier = selected.carrier

    def scoped_carrier(token, at, verse):
        point = token, at, verse
        native = selected.aliases.get(point, point)
        return carrier(token, at, verse) if native is not None and native[:2] == target else None

    selected.carrier = scoped_carrier
    found = _paragraphs.breaks(artifacts, selected)
    marks = {str(verse): kind for (token, at, verse), kind in found.items()
             if (token, at) == target}
    if not marks:
        return None
    return _json({"edition": edition, "token": book["token"], "chapter": chapter,
                  "breaks": dict(sorted(marks.items(), key=lambda row: int(row[0])))})


def resolve(relative: str, root: Path, index) -> bytes | None:
    """Return one logical product; absence is None, source failure is an error."""
    if not any(relative.startswith(prefix) for prefix in
               ("structure/catena/", "structure/readings/", "structure/paragraphs/")):
        return None
    if not relative.endswith(".json") or any(part in {"", ".", ".."} for part in relative.split("/")):
        return None
    root = Path(root)
    catalog = _catalog(index)
    with _context(root, index, catalog):
        if relative.startswith("structure/catena/"):
            return _catena_product(relative, root, index, catalog)
        if relative.startswith("structure/readings/"):
            return _reading_product(relative, root, index)
        return _paragraph_product(relative, root, index, catalog)
