"""Bounded browser projections for the canonical-corpus terminal reader.

Discovery is tracked metadata; reading bodies remain in their canonical files.
The existing producers own every transformation and publication decision. This
router selects their smallest supported unit and never invokes a family build.
"""
from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager, nullcontext
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys

from _indexed_source_library import indexed_records
from _proper_latin import reading_records
from _calendars import verified_parse_cache
from _corpus_index import session_derivations

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = "src/index/reader-manifests.json"
_TOOLS = {}
_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"


def _tool(name):
    if name not in _TOOLS:
        loader = SourceFileLoader("_reader_product_" + name.replace("-", "_"), str(ROOT / "tools" / name))
        spec = spec_from_loader(loader.name, loader)
        module = module_from_spec(spec)
        sys.modules[loader.name] = module
        loader.exec_module(module)
        _TOOLS[name] = module
    return _TOOLS[name]


def _json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _route(relative):
    if (not isinstance(relative, str) or not relative or "\\" in relative or "\0" in relative
            or PurePosixPath(relative).is_absolute()
            or any(part in {"", ".", ".."} for part in relative.split("/"))):
        raise ValueError("unsafe reader product path")
    return relative


@contextmanager
def _reading(index, *, reuse=False):
    # The older parser cache uses timestamps. The reader's exact-content owner
    # must see canonical reads, including equal-size edits with restored mtimes.
    previous = os.environ.get("TRIPTYCH_YAML_CACHE")
    os.environ["TRIPTYCH_YAML_CACHE"] = "0"
    if not hasattr(index, "_reader_parse_cache"):
        index._reader_parse_cache = {}
    if not hasattr(index, "_reader_derivations"):
        index._reader_derivations = {}
    # Only selected reading reuses calendar-wide derivations between records;
    # maintenance derives discovery from scratch.
    derivations = session_derivations(index._reader_derivations) if reuse else nullcontext()
    try:
        with (index.verified_reads(), reading_records(indexed_records(index)),
              verified_parse_cache(index._reader_parse_cache), derivations):
            yield
    finally:
        if previous is None:
            os.environ.pop("TRIPTYCH_YAML_CACHE", None)
        else:
            os.environ["TRIPTYCH_YAML_CACHE"] = previous


class _Artifacts(Mapping):
    def __init__(self, root, index):
        self.root, self.index = Path(root), index

    def __getitem__(self, identifier):
        if self.index.record_kind(identifier) != "artifact":
            raise KeyError(identifier)
        return dict(self.index.record(identifier),
                    _path=self.root / self.index.record_path(identifier),
                    _source_root=self.root / "src/sources")

    def __iter__(self):
        return iter(self.index.records("artifact"))

    def __len__(self):
        return len(self.index.records("artifact"))


def _skeleton(structure):
    """Keep discovery and qualifications, never Proper bodies or renderings."""
    return _tool("mass-propers").reader_structure(structure)


def build_reader_indexes(root: Path, index=None) -> dict[str, bytes]:
    """Maintenance operation: derive thin discovery from canonical producers.

    Return files for the index owner to validate and write. Normal reading
    never calls this function, and these files contain no reading payloads.
    """
    root = Path(root)
    with _reading(index) if index is not None else nullcontext():
        propers = _tool("mass-propers")
        days, rubrics, ordinary = (_tool(name) for name in ("calendar-days", "calendar-rubrics", "mass-ordinary"))
        calendars = root / "src/sources/calendars"
        names = propers.calendars(calendars)
        tokens = propers.book_tokens()
        files, offers = {}, []
        for name in names:
            structure = propers.calendar_structure(calendars, name, tokens)
            files[f"src/index/propers/{name}.json"] = _json(_skeleton(structure))
            files[f"src/index/propers/search/{name}.json"] = _json(propers.search_structure(structure))
            offers.append({"id": name, "edition": structure["edition"],
                           "edition_short": structure.get("edition_short"),
                           "reader_index": True,
                           "reader_file": f"structure/propers/reader/{name}.json",
                           "read_payload": {"catalog": f"structure/propers/catalog/{name}.json",
                                            "mass_prefix": f"structure/propers/mass/{name}/"}})
        offers.sort(key=lambda row: (row["id"] != propers.LANDING_MISSAL, row["id"]))
        indexes = {name: days.load_calendar(calendars, name) for name in names}
        built_rubrics, problems, _ = rubrics.build(calendars, None)
        if problems:
            raise ValueError("; ".join(problems))
        library = (_Artifacts(root, index) if index is not None
                   else ordinary.artifact_records(root / "src/sources"))
        built_ordinary = [ordinary.calendar_structure(root / "src/sources", path, library)
                          for path in ordinary.inventories(root / "src/sources", None)]
        bible = _tool("index-bible")
        servable = ({name.split("/")[3] for name in index.paths("src/sources/bibles/") if "/chapters/" in name}
                    if index is not None else {name for name in bible.EDITIONS
                                               if (root / "src/sources/bibles" / name / "chapters").is_dir()})
        manifests = {
            "bibles.json": bible.manifest_document(servable),
            "structure/propers/index.json": {"default": propers.LANDING_MISSAL, "missals": offers},
            "structure/calendar/index.json": days.index_document(indexes, 2020, 2120),
            "structure/rubrics/index.json": rubrics.index_document(built_rubrics),
            "structure/ordinary/index.json": ordinary.index_file(built_ordinary),
        }
        files[MANIFESTS] = _json(manifests)
        return files


def _header(index, calendar):
    body = index.read(f"src/index/propers/{calendar}.json")
    value = json.loads(body)
    if (value.get("schema") != "triptych-propers-structure/v1"
            or value.get("calendar") != calendar or value.get("reader_index") is not True):
        raise ValueError(f"invalid reader discovery for {calendar}")
    value["generation"] = hashlib.sha256(body).hexdigest()
    return value


def resolve(relative: str, root: Path, index) -> bytes | None:
    """Resolve a logical browser route; unsupported routes return None.

    A known but missing canonical dependency raises visibly. It is never an
    empty library or permission to regenerate all browser-product families.
    """
    relative, root = _route(relative), Path(root)
    if relative == "bibles.json" or relative in {
            "structure/propers/index.json", "structure/calendar/index.json",
            "structure/rubrics/index.json", "structure/ordinary/index.json"}:
        return _json(json.loads(index.read(MANIFESTS))[relative])
    chapter = re.fullmatch(rf"({_SLUG})/chapters/([A-Za-z0-9]+)/([1-9][0-9]*)\.json", relative)
    if chapter:
        offered = json.loads(index.read(MANIFESTS))["bibles.json"]["bibles"]
        if chapter[1] not in {row["id"] for row in offered}:
            raise ValueError("Bible edition is not offered by the corpus index")
        return index.read("src/sources/bibles/" + relative)
    skeleton = re.fullmatch(rf"structure/propers/(?:reader/)?({_SLUG})\.json", relative)
    if skeleton:
        return _json(_header(index, skeleton[1]))
    search = re.fullmatch(rf"structure/propers/search/({_SLUG})\.json", relative)
    if search:
        return index.read(f"src/index/propers/search/{search[1]}.json")
    catalog = re.fullmatch(rf"structure/propers/catalog/({_SLUG})\.json", relative)
    if catalog:
        header = _header(index, catalog[1])
        return _json({"schema": "triptych-propers-read-catalog/v1", "calendar": catalog[1],
                      "generation": header["generation"], "masses": header["masses"],
                      "structure": {key: value for key, value in header.items() if key != "masses"}})
    mass = re.fullmatch(rf"structure/propers/mass/({_SLUG})/({_SLUG})\.json", relative)
    year = re.fullmatch(rf"structure/calendar/({_SLUG})/([0-9]{{4}})\.json", relative)
    rubric = re.fullmatch(rf"structure/rubrics/({_SLUG})\.json", relative)
    ordinary = re.fullmatch(rf"structure/ordinary/({_SLUG})\.json", relative)
    if not any((mass, year, rubric, ordinary)):
        if relative.startswith("structure/sources/"):
            from _reader_source_products import resolve as family
        elif relative.startswith(("structure/catena/", "structure/readings/", "structure/paragraphs/")):
            from _reader_commentary_products import resolve as family
        elif relative == "encyclicals/index.json" or relative.startswith("structure/act-history/"):
            from _reader_history_products import resolve as family
        elif relative.startswith(("structure/documents/", "web-editions/")):
            from _reader_publication_products import resolve as family
        else:
            return None
        return family(relative, root, index)
    with _reading(index, reuse=True):
        calendars = root / "src/sources/calendars"
        if mass:
            from _reader_bibles import bible_context
            owner = _tool("mass-propers")
            header = _header(index, mass[1])
            if mass[2] not in {row["key"] for row in header["masses"]}:
                raise ValueError(f"Mass is not in the reader index: {mass[1]}/{mass[2]}")
            with bible_context(root, index):
                selected = owner.calendar_structure(calendars, mass[1], owner.book_tokens(),
                                                    mass_keys={mass[2]}, translation_order=header["translations"])
            return _json({"schema": owner.READ_MASS_SCHEMA, "calendar": mass[1],
                          "generation": header["generation"], "mass": selected["masses"][0]})
        if year:
            owner, civil_year = _tool("calendar-days"), int(year[2])
            span = json.loads(index.read(MANIFESTS))["structure/calendar/index.json"]["span"]
            if not span["first"] <= civil_year <= span["last"]:
                raise ValueError("civil year is outside the indexed calendar span")
            payloads, _ = owner.structure_projection({year[1]: owner.load_calendar(calendars, year[1])},
                                                     civil_year, civil_year)
            return owner.serialise_year(payloads[Path(year[1]) / f"{civil_year}.json"]).encode()
        if rubric:
            owner = _tool("calendar-rubrics")
            payloads, problems, _ = owner.build(calendars, rubric[1])
            if problems:
                raise ValueError("; ".join(problems))
            return owner.serialise_json(payloads[0], indent=None).encode()
        owner = _tool("mass-ordinary")
        sources = root / "src/sources"
        path = sources / "inventories" / (ordinary[1] + owner.INVENTORY_SUFFIX)
        payload = owner.calendar_structure(sources, path, _Artifacts(root, index))
        return owner.serialise(payload).encode()
