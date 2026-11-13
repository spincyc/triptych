"""Resolve one History or Encyclicals product from canonical source records.

The History lookup records which inputs passed the existing native-book gate,
never their text. Catalogue opening checks those identities against the corpus
index; opening a native text still runs its complete publication/extent gate.
The ordinary full producer never uses this interactive lookup.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path, PurePosixPath
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = "src/index/history/native-bindings.json"
INDEX_SCHEMA = "triptych-history-native-bindings/v1"
PREFIX = "structure/act-history/"


def _json(payload, *, indent=None) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=indent,
                       separators=(",", ":") if indent is None else None) + "\n").encode()


def _digest(payload) -> str:
    return hashlib.sha256(_json(payload)).hexdigest()


def _act_tool():
    name = "_reader_history_act_tool"
    if name not in sys.modules:
        loader = importlib.machinery.SourceFileLoader(name, str(ROOT / "tools/act-history"))
        module = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
        sys.modules[name] = module
        loader.exec_module(module)
    return sys.modules[name]


def _tool_paths() -> tuple[str, ...]:
    from _eucharistic_texts import TOOL_INPUT_PATHS
    return tuple(sorted({*TOOL_INPUT_PATHS, "scripts/_reader_history_products.py"}))


def _file_stamp(root: Path, relative: str) -> dict:
    body = (root / relative).read_bytes()
    return {"path": relative, "sha256": hashlib.sha256(body).hexdigest(), "byte_size": len(body)}


def build_index(root: Path = ROOT) -> dict:
    """Run strict native adapters once, retaining only dependency addresses."""
    from _eucharistic_stages import _files, text_binding_ids
    import _eucharistic_texts as texts
    from _eucharistic_history import fingerprint
    root = root.resolve()
    tool_stamps = [_file_stamp(ROOT, path) for path in _tool_paths()]
    stage_paths = _files(root)
    stage_stamps = [_file_stamp(root, path.relative_to(root).as_posix()) for path in stage_paths]
    identifiers = set()
    for path in stage_paths:
        for stage in json.loads(path.read_bytes())["stages"]:
            identifiers.update(text_binding_ids(stage, stage["id"]))
    bindings, inputs = {}, {}
    library = texts._load_library(root)
    with patch.object(texts, "_load_library", lambda selected_root: library):
        for identifier in sorted(identifiers):
            payload = texts.load_adapter(identifier, root)
            stamps = sorted(payload["inputs"], key=lambda row: row["path"])
            bindings[identifier] = {"inputs": [row["path"] for row in stamps], "sha256": _digest(stamps)}
            for stamp in stamps:
                previous = inputs.setdefault(stamp["path"], stamp)
                if previous != stamp:
                    raise ValueError(f"native binding input changed: {stamp['path']}")
    for relative, expected in inputs.items():
        if fingerprint(root, root / relative) != expected:
            raise ValueError(f"native binding input changed during indexing: {relative}")
    if tool_stamps != [_file_stamp(ROOT, path) for path in _tool_paths()]:
        raise ValueError("native binding implementation changed during indexing")
    if stage_stamps != [_file_stamp(root, path.relative_to(root).as_posix()) for path in _files(root)]:
        raise ValueError("native binding stage membership changed during indexing")
    paths = sorted(inputs)
    positions = {path: position for position, path in enumerate(paths)}
    for binding in bindings.values():
        binding["inputs"] = [positions[path] for path in binding["inputs"]]
    return {"schema": INDEX_SCHEMA, "editorial_approval": False, "inputs": paths,
            "bindings": bindings,
            "stages_sha256": _digest(stage_stamps),
            "tools_sha256": _digest(tool_stamps)}


def _identity(root: Path, index, path: Path) -> dict:
    relative = path.relative_to(root).as_posix()
    try:
        digest, size = index.metadata(relative)
    except KeyError:
        from _source_delivery_policy import external_source_identity
        identity = external_source_identity(root, relative)
        if identity is None:
            raise ValueError(f"history input is absent from the corpus index: {relative}")
        return identity
    return {"path": relative, "sha256": digest, "byte_size": size}


class NativeBindings:
    """Metadata sufficient for the stage join; no literal source is copied."""

    def __init__(self, root: Path, index):
        from _eucharistic_stages import DIRECTORY
        self.root, self.index = root, index
        self.data = json.loads(index.read(INDEX_PATH))
        if (self.data.get("schema") != INDEX_SCHEMA
                or self.data.get("editorial_approval") is not False):
            raise ValueError("unsupported History native-binding lookup")
        tools = [_file_stamp(ROOT, path) for path in _tool_paths()]
        if self.data.get("tools_sha256") != _digest(tools):
            raise ValueError("History native-binding lookup is stale; refresh the History index")
        stage_paths = [path for path in index.paths(DIRECTORY + "/", ".json")
                       if PurePosixPath(path).parent.as_posix() == DIRECTORY]
        if self.data.get("stages_sha256") != _digest([_identity(root, index, root / path) for path in stage_paths]):
            raise ValueError("History native-binding stage membership changed; refresh the History index")
        self.stamps = {}
        self.held = {}

    def __call__(self, identifier: str, root: Path) -> dict:
        from _eucharistic_texts import AdapterError, NATIVE_BOOK_DIRECTORY, NATIVE_BOOK_PREFIX
        if identifier in self.held:
            return self.held[identifier]
        try:
            declaration = self.data["bindings"][identifier]
            stamps = []
            for position in declaration["inputs"]:
                relative = self.data["inputs"][position]
                if relative not in self.stamps:
                    self.stamps[relative] = _identity(root, self.index, root / relative)
                stamps.append(self.stamps[relative])
            if _digest(stamps) != declaration["sha256"]:
                raise ValueError("native-book dependencies changed; refresh the History index")
            slug = identifier.removeprefix(NATIVE_BOOK_PREFIX)
            if not identifier.startswith(NATIVE_BOOK_PREFIX) or not slug or "/" in slug:
                raise ValueError("invalid native-book identity")
            relative = f"{NATIVE_BOOK_DIRECTORY}/{slug}.json"
            book = json.loads(self.index.read(relative))
            expected = next(stamp["sha256"] for stamp in stamps if stamp["path"] == relative)
            # The existing stage validator still owns all stage, edition,
            # witness, component and complete-extent joins.
            payload = {"title": book["title"], "inputs": stamps,
                       "book_binding": {"id": slug, "sha256": expected,
                                        **{field: book[field] for field in
                                           ("stage_ids", "catalogue_witness_ids", "components", "witnesses")}},
                       "scope": {"extent_kind": book["extent_kind"], "complete_declared_extent": True,
                                 "whole_book_complete": book["extent_kind"] == "whole-book"}}
        except (KeyError, IndexError, TypeError, StopIteration, ValueError) as error:
            raise AdapterError(f"History native-binding lookup for {identifier}: {error}") from error
        self.held[identifier] = payload
        return payload


@contextmanager
def _sources(root: Path, index):
    """Supply lazy records while preserving the existing source/rights gates.

    The owning reader dispatcher serializes requests. Scoped replacements are
    restored even on errors and never alter a subsequent full producer run.
    """
    import _eucharistic_history as history
    import _eucharistic_texts as texts
    from _indexed_source_library import Library, indexed_records
    library = Library(root, index)
    records = indexed_records(index)
    original = texts._Sources

    class Sources(original):
        def __init__(self, selected_root, selected_library):
            self.root, self.library = selected_root, selected_library
            self.records = records
            self.used, self.inputs = set(), {}

    act = _act_tool()
    with patch.object(texts, "_load_library", lambda selected_root: library), \
            patch.object(texts, "_Sources", Sources), \
            patch.object(act, "source_artifact_records", lambda: records), \
            patch.object(history, "fingerprint", lambda selected_root, path: _identity(selected_root, index, path)):
        yield act, history


def _slices(root: Path, index, act):
    for relative in index.paths("src/sources/inventories/", ".toml"):
        path = PurePosixPath(relative)
        if path.parent.as_posix() != "src/sources/inventories" or not path.name.endswith("-acts-v1.toml"):
            continue
        data = act.load(root / relative)
        yield data


def _catalogue(root, index, act, history):
    return history.catalogue(root / history.DEFAULT_SOURCE, root, act_loader=act.load,
                             binding_loader=NativeBindings(root, index))


def resolve(relative: str, root: Path, index) -> bytes | None:
    """Return exactly one logical browser product, or None for another family."""
    if relative != "encyclicals/index.json" and not relative.startswith(PREFIX):
        return None
    with index.verified_reads():
        return _resolve(relative, root, index)


def _resolve(relative: str, root: Path, index) -> bytes | None:
    root = Path(root).resolve()
    if relative == "encyclicals/index.json":
        import _encyclicals
        return _encyclicals.render(root / _encyclicals.INDEX_RELATIVE,
                                  root / _encyclicals.RELEASE_RELATIVE, root).encode()
    if not relative.startswith(PREFIX):
        return None
    selected = relative.removeprefix(PREFIX)
    parts = PurePosixPath(selected).parts
    if not parts or ".." in parts or not selected.endswith(".json"):
        raise ValueError(f"invalid History product: {relative}")
    with _sources(root, index) as (act, history):
        if selected == "catalogue.json":
            return history.json_bytes(_catalogue(root, index, act, history))
        if len(parts) == 2 and parts[0] == "native-texts":
            identifier = "native-book:" + parts[1].removesuffix(".json")
            # Refuse an unadvertised native selection before loading its text.
            NativeBindings(root, index)(identifier, root)
            return history.json_bytes(history.native_text(identifier, root))
        if len(parts) == 2 and parts[0] == "comparisons":
            catalogue = _catalogue(root, index, act, history)
            return history.json_bytes(history.compare(
                root / history.DEFAULT_SOURCE, root, parts[1].removesuffix(".json"),
                ventilator=act.ventilate, act_loader=act.load, catalogue_context=catalogue))
        if selected == "index.json":
            listed = [{"id": str(data["slice"]), "vocabulary": act.vocabulary_of(data).name,
                       "stations": len(data.get("acts", [])), "lines": len(data.get("lines", []))}
                      for data in _slices(root, index, act)]
            listed.sort(key=lambda row: (row["id"] != act.LANDING_SLICE, row["id"]))
            return _json({"default": act.landing_of(listed), "slices": listed}, indent=1)
        slice_id = parts[0].removesuffix(".json")
        data = next((data for data in _slices(root, index, act) if str(data.get("slice")) == slice_id), None)
        if data is None:
            raise ValueError(f"unknown History slice: {slice_id}")
        act.check(data)
        found = {}
        totals = act.fragments(data, root, slice_id, selected=selected,
                               emit=lambda path, payload: found.update(payload=payload))
        if len(parts) == 1:
            return _json(act.map_payload(data, totals))
        if "payload" not in found:
            raise ValueError(f"unknown History product: {relative}")
        return _json(found["payload"])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("refresh", "check"))
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    wanted = _json(build_index(args.root), indent=1)
    target = args.root / INDEX_PATH
    if args.action == "check":
        if not target.is_file() or target.read_bytes() != wanted:
            parser.error("History native-binding lookup is stale")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(wanted)
    print(f"History native bindings: {args.action} OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
