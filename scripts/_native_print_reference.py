"""Exchange source-prepared native catalogs between jobs of the same Pages run.

An expected manifest digest comes from the caller's authenticated artifact.
Each bundle binds its dependency fingerprints, mounted files and all derived
transports. Shards can omit raw assets whose exact bytes are in the checkout.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import stat
import tempfile

import _native_print_bundles as bundles
from _native_print_compile import partition
from _native_tex_publication import _source_pack_assets

SCHEMA = "triptych-native-print-reference/v1"
PUBLICATION_SCHEMA = "triptych-native-print-reference/v2"
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_NUMBER = re.compile(r"[1-9][0-9]*\Z")
_SOURCE = re.compile(r"native-tex/sources/[0-9a-f]{64}\.json\Z")
_ASSET = re.compile(r"native-tex/assets/[0-9a-f]{64}\.(?:bin|tex|sty|cls|bib|bst|png|jpg|jpeg|eps)\Z")
_PACK = re.compile(r"native-tex/source-packs/[0-9a-f]{64}\.bin\Z")


def _need(value, explanation):
    if not value:
        raise ValueError("native print reference: " + explanation)


def _origin(revision, run_id, run_attempt):
    _need(isinstance(revision, str) and bundles._REVISION.fullmatch(revision)
          and isinstance(run_id, str) and _NUMBER.fullmatch(run_id)
          and isinstance(run_attempt, str) and _NUMBER.fullmatch(run_attempt),
          "invalid revision, run id or attempt")


def _directory(path):
    path = Path(path).absolute()
    _need(not any(member.is_symlink() for member in (path, *path.parents)),
          "redirected reference directory")
    return path


def _regular(path):
    _need(stat.S_ISREG(path.lstat().st_mode), "missing or redirected reference file: " + str(path))
    return path


def write_reference_catalog(directory: Path, catalog: dict, *, run_id: str, run_attempt: str,
                            shard: tuple[int, int] | None = None, publication_parts: dict | None = None) -> str:
    """Atomically export a canonical catalog produced by this trusted operation."""
    revision = catalog["source_revision"]
    _origin(revision, run_id, run_attempt)
    _need(catalog["schema"] == bundles.CATALOG_SCHEMA and catalog["bundles"], "empty or invalid catalog")
    directory = _directory(directory)
    _need(not directory.exists() or directory.is_dir() and not any(directory.iterdir()),
          "refusing to replace a non-empty reference destination")
    directory.parent.mkdir(parents=True, exist_ok=True)
    checkout_assets = {}
    if shard is not None:
        _need(len(shard) == 2 and 1 <= shard[0] <= shard[1], "invalid shard number")
        source_by_hash = {}
        for descriptor in catalog["bundles"].values():
            bundle = json.loads(catalog["assets"][descriptor["route"]])
            for row in bundle["source_inputs"]:
                source_by_hash.setdefault(row["sha256"], row["path"])
        for route in catalog["assets"]:
            if _ASSET.fullmatch(route) and (path := source_by_hash.get(Path(route).stem)) is not None:
                checkout_assets[route] = path
    manifest = {"schema": SCHEMA, "source_revision": revision, "run_id": run_id,
                "run_attempt": run_attempt, "shard": list(shard) if shard else None,
                "bundles": catalog["bundles"], "checkout_assets": checkout_assets}
    if publication_parts is not None:
        manifest.update(schema=PUBLICATION_SCHEMA, publication_parts=publication_parts)
    manifest_bytes = bundles.canonical(manifest) + b"\n"
    with tempfile.TemporaryDirectory(dir=directory.parent) as temporary:
        stage = Path(temporary) / "reference"
        stage.mkdir()
        for route, body in catalog["assets"].items():
            _need(_SOURCE.fullmatch(route) or _ASSET.fullmatch(route) or _PACK.fullmatch(route),
                  "unexpected native export route: " + route)
            if route not in checkout_assets:
                target = stage / route
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body)
        (stage / "catalog.json").write_bytes(manifest_bytes)
        os.replace(stage, directory)
    return bundles._sha(manifest_bytes)


def _inventory(directory):
    """Inventory ordinary routes before reading any artifact-selected path."""
    paths = {}
    _need(set(path.name for path in directory.iterdir()) == {"catalog.json", "native-tex"},
          "unexpected files in reference directory")
    native = directory / "native-tex"
    _need(native.is_dir() and not native.is_symlink(), "missing native transport directory")
    formats = {"sources": _SOURCE, "assets": _ASSET, "source-packs": _PACK}
    for group in native.iterdir():
        _need(group.name in formats and not group.is_symlink() and group.is_dir(), "invalid transport directory")
        for path in group.iterdir():
            route = path.relative_to(directory).as_posix()
            _need(formats[group.name].fullmatch(route), "invalid reference route: " + route)
            paths[route] = _regular(path)
    return paths


def _manifest(directory, revision, run_id, run_attempt, expected_sha256, shard):
    directory = _directory(directory)
    _need(isinstance(expected_sha256, str) and _DIGEST.fullmatch(expected_sha256),
          "invalid independent manifest digest")
    body = _regular(directory / "catalog.json").read_bytes()
    _need(bundles._sha(body) == expected_sha256, "manifest digest differs from its authenticated artifact")
    manifest = json.loads(body)
    fields = {"schema", "source_revision", "run_id", "run_attempt", "shard", "bundles", "checkout_assets"}
    if isinstance(manifest, dict) and manifest.get("schema") == PUBLICATION_SCHEMA:
        fields.add("publication_parts")
    _need(isinstance(manifest, dict) and set(manifest) == fields
        and manifest["schema"] in {SCHEMA, PUBLICATION_SCHEMA} and manifest["source_revision"] == revision
        and manifest["run_id"] == run_id, "wrong reference schema, revision or workflow run")
    attempt = manifest["run_attempt"]
    _need(isinstance(attempt, str) and _NUMBER.fullmatch(attempt) and
          (int(attempt) <= int(run_attempt) if shard else attempt == run_attempt),
          "wrong reference run attempt")
    _need(manifest["shard"] == (list(shard) if shard else None), "wrong shard assignment")
    return manifest


def publication_parts(directory, *, revision, run_id, run_attempt, expected_sha256):
    """Read the publication portions of this consumer's separately authenticated merged catalog."""
    _origin(revision, run_id, run_attempt)
    manifest = _manifest(directory, revision, run_id, run_attempt, expected_sha256, None)
    _need(manifest["schema"] == PUBLICATION_SCHEMA, "missing authenticated publication source expectations")
    return manifest["publication_parts"]


def _read_reference(directory, *, root, documents, revision, run_id, run_attempt, expected_sha256,
                    shard, source_inputs, collect_publications=None):
    """Read one sealed artifact. For shards, restore the pre-sharing representation."""
    directory = _directory(directory)
    manifest = _manifest(directory, revision, run_id, run_attempt, expected_sha256, shard)
    if collect_publications is not None:
        number = str(shard[0])
        about = manifest.get("publication_parts")
        _need(isinstance(about, dict) and set(about) == {number}, "missing or unexpected publication partition")
        part = about[number]
        _need(isinstance(part, dict) and part.get("attempt") == manifest["run_attempt"],
              "publication producer differs from native producer")
        collect_publications[number] = part
    routes, omitted = manifest["bundles"], manifest["checkout_assets"]
    _need(isinstance(routes, dict) and routes and set(routes) == set(documents),
          "reference editions differ from the current admissions or partition")
    paths = _inventory(directory)
    _need(isinstance(omitted, dict) and all(_ASSET.fullmatch(route) for route in omitted)
          and set(omitted).isdisjoint(paths), "invalid checkout asset inventory")
    # A route can be referenced by many editions. Hash each actual body once.
    assets, identities, seen, prepared, artwork = {}, {}, set(), {}, {}

    def read(route, row):
        size, digest = row["bytes"], row["sha256"]
        _need(type(size) is int and size > 0 and isinstance(digest, str) and _DIGEST.fullmatch(digest),
              "invalid reference asset descriptor")
        if route not in assets:
            if route in omitted:
                path = bundles._source(root, omitted[route])
            else:
                _need(route in paths, "missing reference asset: " + route)
                path = paths[route]
            _need(path.stat().st_size == size, "changed reference asset size: " + route)
            payload = path.read_bytes()
            _need(len(payload) == size and bundles._sha(payload) == digest, "changed reference asset: " + route)
            assets[route], identities[route] = payload, (size, digest)
        _need(identities[route] == (size, digest), "conflicting reference asset descriptors")
        seen.add(route)
        return assets[route]

    for identity, descriptor in routes.items():
        route = descriptor["route"]
        _need(set(descriptor) == {"route", "bytes", "sha256"} and _SOURCE.fullmatch(route) and route not in seen,
              "invalid or duplicate source bundle route")
        bundle = json.loads(read(route, descriptor))
        _need(bundle["output_id"] == identity and bundle["source_revision"] == revision
              and route == f"{bundles.SOURCE_ROUTE}/{bundle['content_sha256']}.json"
              and all(bundle[key] == documents[identity][key] for key in ("document", "edition", "title"))
              and bundle.get("render_sha256"), "source bundle differs from its admitted edition")
        for pack in bundle.get("sourcePacks", ()):
            target = "native-tex/" + pack["href"].removeprefix("../")
            _need(_PACK.fullmatch(target), "invalid source pack route")
            read(target, pack)
        _source_pack_assets(bundle, assets)  # Checks content, render, inline bytes and every expanded pack member.
        inputs = bundle["source_inputs"]
        _need(isinstance(inputs, list) and inputs, "missing canonical source fingerprints")
        previous = ""
        for row in inputs:
            path = row["path"]
            _need(isinstance(path, str) and path > previous and set(row) == {"path", "bytes", "sha256"}
                  and row == source_inputs.setdefault(path, row), "conflicting or unordered source fingerprints")
            previous = path
        for index, row in enumerate(bundle["files"]):
            if row["encoding"] != "url":
                continue
            target = "native-tex/" + row["href"][3:]  # validate_bundle checked the exact href.
            payload = read(target, row)
            if shard and target.endswith(".bin"):
                bundle["files"][index] = {"path": row["path"], "bytes": row["bytes"], "sha256": row["sha256"],
                                          "encoding": "utf8", "content": payload.decode("utf-8")}
            elif shard:
                artwork[target] = payload
        if shard:
            bundle.pop("sourcePacks", None)
            del bundle["content_sha256"]
            prepared[identity] = bundle
    _need(seen == paths.keys() | omitted.keys(), "unowned or missing reference asset")
    for route, path in omitted.items():
        _need(path in source_inputs and identities[route] == (source_inputs[path]["bytes"], source_inputs[path]["sha256"]),
              "omitted asset must match an exact declared checkout input")
    return (prepared, artwork) if shard else (routes, assets)


def _verify_sources(root, source_inputs):
    snapshot = bundles._CatalogInputs(root)
    rows = snapshot.fingerprints(source_inputs)
    _need(all(row == source_inputs[row["path"]] for row in rows), "canonical source fingerprint differs")
    snapshot.verify()


def load_reference_catalog(directory: Path, *, root: Path, documents: dict, revision: str, run_id: str,
                           run_attempt: str, expected_sha256: str) -> dict:
    """Validate the entire merged source catalog against its independent digest and checkout."""
    _origin(revision, run_id, run_attempt)
    root = Path(root).resolve()
    inputs = {}
    routes, assets = _read_reference(directory, root=root, documents=documents, revision=revision,
                                     run_id=run_id, run_attempt=run_attempt, expected_sha256=expected_sha256,
                                     shard=None, source_inputs=inputs)
    _verify_sources(root, inputs)
    return {"schema": bundles.CATALOG_SCHEMA, "source_revision": revision, "bundles": routes,
            "assets": assets, "source_paths": sorted(inputs)}


def merge_reference_catalogs(directory: Path, *, root: Path, documents: dict, revision: str, run_id: str,
                             run_attempt: str, shards: int, expected_keys: dict, publication_parts=None) -> dict:
    """Require every source-built partition and apply the full catalog's sharing policy once."""
    _origin(revision, run_id, run_attempt)
    directory, root = _directory(directory), Path(root).resolve()
    expected = {str(i) for i in range(1, shards + 1)}
    _need(shards > 0 and expected == {child.name for child in directory.iterdir()}
          and isinstance(expected_keys, dict) and expected == expected_keys.keys(), "incomplete shard set")
    prepared, artwork, inputs = {}, {}, {}
    for number in range(1, shards + 1):
        selection = {key: documents[key] for key in partition(documents, number, shards)}
        editions, assets = _read_reference(directory / str(number), root=root, documents=selection,
                                           revision=revision, run_id=run_id, run_attempt=run_attempt,
                                           expected_sha256=expected_keys[str(number)], shard=(number, shards),
                                           source_inputs=inputs, collect_publications=publication_parts)
        prepared.update(editions)
        for route, body in assets.items():
            _need(artwork.setdefault(route, body) == body, "conflicting native artwork across shards")
    catalog = bundles.package_catalog(prepared, artwork, revision)
    _verify_sources(root, inputs)
    return catalog
