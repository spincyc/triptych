"""Exact public transport for admitted native TeX editions and their runtime.

This layer does not compile a PDF or acquire a dependency.  The source bundle
producer owns the original TeX graph; the runtime registry owns every engine,
package and font byte.  The publisher joins those two inventories to its
current public admission set and re-derives the join during verification.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import urlsplit

SCHEMA = "triptych-native-tex-publication/v1"
RUNTIME_ROUTE = "native-tex/runtime.json"
INPUT_PATHS = (
    "scripts/_native_tex_publication.py",
    "scripts/_native_print_bundles.py",
    "scripts/_native_tex_assets.py",
    "scripts/_native_print.py",
    "scripts/_native_print_artwork.py",
    "src/common/native-tex-runtime.json",
)
_SHA = re.compile(r"[0-9a-f]{64}\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")
_TEX_PACK_BYTES = 8 * 1024 * 1024
_MAX_RUNTIME_RESOURCE = 256 * 1024 * 1024
_COMPRESS_MIN_BYTES = 256 * 1024
_COMPRESS_MIN_SAVING = 32 * 1024


class NativeTeXPublicationError(ValueError):
    pass


def _need(value, message):
    if not value:
        raise NativeTeXPublicationError(message)


def _json(value) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def _digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def _route(value: str) -> str:
    _need(isinstance(value, str) and value.startswith("native-tex/")
          and "\\" not in value and not any(char in value for char in "\0?#%")
          and not any(ord(char) < 33 for char in value)
          and all(part not in {"", ".", "..", ".git", ".scratch", "__pycache__"}
                  for part in value.split("/"))
          and not PurePosixPath(value).is_absolute()
          and PurePosixPath(value).suffix.lower() not in
              {".pdf", ".ps", ".zip", ".tar", ".tex", ".sty", ".aux", ".log"}
          and (not value.lower().endswith(".gz") or value.endswith(".fmt.gz")),
          "unsafe native TeX publication route: " + repr(value))
    return value


def _input_path(root: Path, value: str) -> str:
    _need(isinstance(value, str) and value and "\\" not in value
          and not PurePosixPath(value).is_absolute()
          and all(part not in {"", ".", "..", ".git", ".scratch", "build", "__pycache__"}
                  for part in value.split("/")),
          "unsafe canonical native TeX publication input")
    path = root / value
    current = root
    for part in value.split("/"):
        current /= part
        _need(not current.is_symlink(), "redirected canonical native TeX publication input: " + value)
    _need(path.is_file()
          and path.resolve().is_relative_to(root.resolve()),
          "missing or redirected canonical native TeX publication input: " + value)
    return value


def _asset(body: bytes, *, kind: str) -> dict:
    _need(type(body) is bytes and body, "native TeX publication needs nonempty immutable bytes")
    return {"body": body, "sha256": _digest(body), "bytes": len(body), "kind": kind}


def _runtime_records(value, found=None):
    """The source offer is external; every executable/runtime byte is local."""
    found = {} if found is None else found
    if isinstance(value, list):
        for item in value:
            _runtime_records(item, found)
    elif isinstance(value, dict):
        _need("transport" not in value, "native TeX transports must be derived by the publisher")
        if "url" in value:
            route = _route(value["url"])
            _need(isinstance(value.get("sha256"), str) and _SHA.fullmatch(value["sha256"])
                  and type(value.get("bytes")) is int and value["bytes"] > 0,
                  "runtime payload has no exact byte identity: " + route)
            identity = {"sha256": value["sha256"], "bytes": value["bytes"]}
            _need(route not in found or found[route] == identity,
                  "runtime payload has conflicting identities: " + route)
            found[route] = identity
        for key, item in value.items():
            if key != "correspondingSource":
                _runtime_records(item, found)
    return found


def _gzip_runtime_payloads(group: list, runtime_assets: dict) -> tuple[dict, list, int]:
    files, expanded_bytes = [], 0
    buffer = io.BytesIO()
    # GzipFile fixes both the timestamp and the platform-dependent header.
    with gzip.GzipFile(fileobj=buffer, filename="", mode="wb", mtime=0, compresslevel=6) as packed:
        for (sha256, byte_count), route in group:
            path = Path(runtime_assets[route]["path"])
            _need(path.is_file() and not path.is_symlink(),
                  "native runtime payload is redirected or missing")
            digest, received = hashlib.sha256(), 0
            with path.open("rb") as source:
                while chunk := source.read(1024 * 1024):
                    received += len(chunk)
                    _need(received <= byte_count, "native runtime payload changed while packing: " + route)
                    digest.update(chunk)
                    packed.write(chunk)
            _need(received == byte_count and digest.hexdigest() == sha256,
                  "native runtime payload changed while packing: " + route)
            files.append({"sha256": sha256, "bytes": byte_count, "offset": expanded_bytes})
            expanded_bytes += byte_count
    asset = _asset(buffer.getvalue(), kind="runtime")
    return asset, files, expanded_bytes


def _pack_tex_files(tex_files: list, runtime_assets: dict) -> tuple[list, dict]:
    """Package exact runtime payloads once; lookup aliases keep their own registry rows."""
    _need(isinstance(tex_files, list) and len(tex_files) <= 50000,
          "invalid native TeX package inventory")
    payloads = {}
    deferred = {}
    font_groups = {}
    for row in tex_files:
        _need(isinstance(row, dict), "invalid native TeX package record")
        route = _route(row.get("url"))
        asset = runtime_assets.get(route)
        _need(asset is not None and asset.get("kind") == "runtime" and "path" in asset
              and all(row.get(field) == asset[field] for field in ("sha256", "bytes"))
              and type(row.get("bytes")) is int and 0 < row["bytes"] <= _MAX_RUNTIME_RESOURCE,
              "native TeX package is not an exact admitted runtime payload: " + route)
        key = row["sha256"], row["bytes"]
        payloads[key] = min(route, payloads.get(key, route))
        # This changes transport scheduling only. The browser mounts every
        # lookup and must restart with verified bytes if it probes an omitted
        # font; these suffixes are never an admission or dependency allowlist.
        heavy_font = row.get("format") in {32, 36, 47} or PurePosixPath(row.get("name", "")).suffix.lower() in {
            ".pfb", ".otf", ".ttf", ".ttc",
        }
        deferred[key] = deferred.get(key, True) and heavy_font
        if heavy_font:
            suffix = PurePosixPath(row.get("name", "")).suffix.lower()
            suffix = suffix if suffix in {".pfb", ".otf", ".ttf", ".ttc"} else {
                32: ".pfb", 36: ".ttf", 47: ".otf",
            }[row["format"]]
            name = row.get("name", "")
            # Native metric/map discovery supplies exact Type1 face hints.
            # Keep each body separate so one requested Latin Modern face
            # cannot bring every unrelated roman, sans and mono face along.
            group = suffix, (name if suffix == ".pfb" else name[:2]).casefold()
            font_groups[key] = min(group, font_groups.get(key, group))

    groups, current, size = [], [], 0
    for identity, route in sorted(payloads.items()):
        if deferred[identity]:
            continue
        if current and size + identity[1] > _TEX_PACK_BYTES:
            groups.append((current, False))
            current, size = [], 0
        current.append((identity, route))
        size += identity[1]
    if current:
        groups.append((current, False))
    # A native failure can stop at the first needed face. Unicode fonts retain
    # coarse filename-prefix groups; Type1 faces arrive individually from
    # native accesses and metric/map hints. The same bound applies to every group.
    for family in sorted({font_groups[key] for key in payloads if deferred[key]}):
        current, size = [], 0
        for identity, route in sorted(payloads.items()):
            if not deferred[identity] or font_groups[identity] != family:
                continue
            if current and size + identity[1] > _TEX_PACK_BYTES:
                groups.append((current, _digest(_json(family))))
                current, size = [], 0
            current.append((identity, route))
            size += identity[1]
        if current:
            groups.append((current, _digest(_json(family))))

    packs, assets = [], {}
    for group, on_demand in groups:
        asset, files, expanded_bytes = _gzip_runtime_payloads(group, runtime_assets)
        _need(asset["bytes"] <= _MAX_RUNTIME_RESOURCE,
              "compressed native TeX package exceeds its browser resource limit")
        route = "native-tex/packs/" + asset["sha256"] + ".bin"
        _need(route not in runtime_assets and route not in assets, "native TeX package route collision")
        assets[route] = asset
        pack = {"url": route, "sha256": asset["sha256"], "bytes": asset["bytes"],
                "compression": "gzip", "expanded_bytes": expanded_bytes, "files": files}
        if on_demand:
            pack["deferred"] = True
            pack["font_group"] = on_demand
        packs.append(pack)
    return packs, assets


def _engine_transports(engines: dict, runtime_assets: dict) -> tuple[dict, dict]:
    """Compress large raw engines while retaining their original identity and fallback."""
    _need(isinstance(engines, dict), "invalid native TeX engine inventory")
    result, assets, prepared = {}, {}, {}
    for engine, resources in engines.items():
        _need(isinstance(resources, dict), "invalid native TeX engine descriptor")
        result[engine] = dict(resources)
        for role in ("wasm", "icu", "format"):
            if role not in resources:
                continue
            pin = resources[role]
            _need(isinstance(pin, dict), "invalid native TeX engine resource")
            route = _route(pin.get("url"))
            asset = runtime_assets.get(route)
            _need(asset is not None and asset.get("kind") == "runtime" and "path" in asset
                  and all(pin.get(field) == asset[field] for field in ("sha256", "bytes"))
                  and type(pin.get("bytes")) is int and 0 < pin["bytes"] <= _MAX_RUNTIME_RESOURCE,
                  "native TeX engine is not an exact admitted runtime payload: " + route)
            if pin["bytes"] < _COMPRESS_MIN_BYTES or route.endswith(".gz") or pin.get("compression"):
                continue
            # pdfTeX's .fmt has no .gz suffix, but its controller already inflates it.
            with Path(asset["path"]).open("rb") as stream:
                if stream.read(2) == b"\x1f\x8b":
                    continue
            identity = pin["sha256"], pin["bytes"]
            if identity not in prepared:
                packed, _, _ = _gzip_runtime_payloads([(identity, route)], runtime_assets)
                saving = pin["bytes"] - packed["bytes"]
                if saving < _COMPRESS_MIN_SAVING or saving * 10 < pin["bytes"]:
                    prepared[identity] = None
                else:
                    target = "native-tex/transports/" + packed["sha256"] + ".bin"
                    _need(target not in runtime_assets and target not in assets,
                          "native TeX transport route collision")
                    assets[target] = packed
                    prepared[identity] = {"url": target, "sha256": packed["sha256"],
                                          "bytes": packed["bytes"], "compression": "gzip"}
            if prepared[identity] is not None:
                result[engine][role] = {**pin, "transport": dict(prepared[identity])}
    return result, assets


def _source_pack_assets(bundle: dict, source_assets: dict) -> dict:
    """Admit only bounded, lossless transports of this bundle's exact text."""
    if "sourcePacks" not in bundle and "render_sha256" not in bundle:
        return {}
    from _native_print_bundles import BundleError, validate_bundle
    try:
        validate_bundle(bundle)
    except (BundleError, KeyError, TypeError) as error:
        raise NativeTeXPublicationError("invalid native source transport: " + str(error)) from error
    result = {}
    for pack in bundle.get("sourcePacks", []):
        route = _route("native-tex/" + pack["href"][3:])
        asset = _asset(source_assets.get(route), kind="source-pack")
        _need(all(pack[field] == asset[field] for field in ("sha256", "bytes")),
              "native source pack differs from its exact byte identity")
        try:
            with gzip.GzipFile(fileobj=io.BytesIO(asset["body"])) as stream:
                expanded = stream.read(pack["expanded_bytes"] + 1)
        except (OSError, EOFError, ValueError) as error:
            raise NativeTeXPublicationError("invalid compressed native source pack") from error
        _need(len(expanded) == pack["expanded_bytes"], "native source pack expanded size differs")
        for member in pack["files"]:
            payload = expanded[member["offset"]:member["offset"] + member["bytes"]]
            _need(_digest(payload) == member["sha256"], "native source pack member differs from its source identity")
        result[route] = asset
    return result


def build_catalog(root: Path, *, documents: dict, revision: str,
                  source_catalog: dict, runtime_manifest: dict,
                  runtime_paths: dict) -> dict:
    """Validate a complete join.  Arguments expose the seam for focused tests."""
    root = Path(root).resolve()
    _need("texPacks" not in runtime_manifest, "native TeX packs must be derived by the publisher")
    # Registry URLs are relative to the site root, not this JSON's directory.
    # A relative base preserves both custom-domain and /project/ deployments.
    runtime_manifest = {**runtime_manifest, "asset_base": "../"}
    _need(isinstance(documents, dict) and documents and isinstance(revision, str)
          and _REVISION.fullmatch(revision),
          "native TeX publication needs admitted editions and an exact source revision")
    _need(source_catalog.get("schema") == "triptych-native-print-source-catalog/v1"
          and source_catalog.get("source_revision") == revision
          and set(source_catalog.get("bundles", {})) == set(documents),
          "native TeX source bundles differ from current public admissions or revision")
    assets, selections = {}, {}
    declared_source_assets = set()
    for identity, descriptor in sorted(source_catalog["bundles"].items()):
        route = _route(descriptor.get("route"))
        _need(route.startswith("native-tex/sources/") and route.endswith(".json"),
              "native source bundle is outside its transport namespace")
        body = source_catalog.get("assets", {}).get(route)
        asset = _asset(body, kind="source-bundle")
        _need(all(descriptor.get(field) == asset[field] for field in ("sha256", "bytes")),
              "native source bundle differs from its exact byte identity: " + identity)
        try:
            bundle = json.loads(body)
        except (UnicodeError, ValueError) as error:
            raise NativeTeXPublicationError("invalid native source bundle: " + identity) from error
        admitted = documents[identity]
        _need(bundle.get("schema") == "triptych-native-print-source-bundle/v1"
              and bundle.get("output_id") == identity
              and bundle.get("source_revision") == revision
              and bundle.get("document") == admitted["document"]
              and bundle.get("edition") == admitted["edition"],
              "native source bundle substitutes another edition: " + identity)
        _need(route not in assets or assets[route] == asset,
              "native source bundle route collision")
        declared_source_assets.add(route)
        assets[route] = asset
        for source_file in bundle.get("files", []):
            if source_file.get("encoding") != "url":
                continue
            href = source_file.get("href")
            _need(isinstance(href, str) and href and "\\" not in href
                  and not any(char in href for char in "\0?#%")
                  and not href.startswith("/") and not urlsplit(href).scheme
                  and not urlsplit(href).netloc,
                  "native artwork has an unsafe transport link")
            target = _route(posixpath.normpath(posixpath.join(posixpath.dirname(route), href)))
            _need(target.startswith("native-tex/assets/"),
                  "native artwork escapes its public transport namespace")
            kind = ("source-text" if PurePosixPath(source_file.get("path", "")).suffix.lower()
                    in {".tex", ".sty", ".cls", ".bib", ".bst"} else "source-artwork")
            artwork = _asset(source_catalog["assets"].get(target), kind=kind)
            _need(all(source_file.get(field) == artwork[field] for field in ("sha256", "bytes")),
                  "native artwork differs from its source identity: " + target)
            _need(target not in assets or assets[target] == artwork,
                  "native artwork transport collision")
            declared_source_assets.add(target)
            assets[target] = artwork
        for target, packed in _source_pack_assets(bundle, source_catalog["assets"]).items():
            _need(target not in assets or assets[target] == packed, "native source pack transport collision")
            declared_source_assets.add(target)
            assets[target] = packed
        selections[identity] = {"bundle_href": route,
                                "bundle_sha256": asset["sha256"],
                                "bundle_bytes": asset["bytes"]}
    _need(set(source_catalog.get("assets", {})) == declared_source_assets,
          "unowned native source bundle would reach publication")

    expected_runtime = _runtime_records(runtime_manifest)
    _need(expected_runtime and set(expected_runtime) == set(runtime_paths),
          "native runtime payload inventory is incomplete or includes an unowned file")
    for route, identity in sorted(expected_runtime.items()):
        _need(route not in assets and route != RUNTIME_ROUTE,
              "native runtime payload route collision")
        path = Path(runtime_paths[route])
        _need(path.is_file() and not path.is_symlink(), "native runtime payload is redirected or missing")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        _need(path.stat().st_size == identity["bytes"] and digest.hexdigest() == identity["sha256"],
              "native runtime payload differs from its pinned bytes: " + route)
        assets[route] = {"path": path, **identity, "kind": "runtime"}

    packs, packed_assets = _pack_tex_files(runtime_manifest.get("texFiles", []), assets)
    if packs:
        runtime_manifest["texPacks"] = packs
        assets.update(packed_assets)
    runtime_manifest["engines"], compressed_assets = _engine_transports(runtime_manifest.get("engines"), assets)
    assets.update(compressed_assets)
    runtime_asset = _asset(_json(runtime_manifest), kind="runtime-manifest")
    assets[RUNTIME_ROUTE] = runtime_asset
    source_paths = source_catalog.get("source_paths")
    _need(isinstance(source_paths, (list, tuple)), "native source catalog lacks canonical inputs")
    source_paths = sorted({_input_path(root, path) for path in [*source_paths, *INPUT_PATHS]})
    return {"schema": SCHEMA, "source_revision": revision, "documents": documents,
            "selections": selections,
            "runtime": {"href": RUNTIME_ROUTE, "sha256": runtime_asset["sha256"],
                        "bytes": runtime_asset["bytes"]},
            "assets": dict(sorted(assets.items())), "source_paths": source_paths}


def catalog(root: Path, *, documents=None, revision=None, scratch_root=None) -> dict:
    """Derive offline.  Callers may hold it only within one source snapshot."""
    from _native_print import admission_inputs, admitted_documents, source_revision
    from _native_print_bundles import prepare_catalog
    from _native_tex_assets import public_manifest, payload_paths

    root = Path(root).resolve()
    documents = admitted_documents(root) if documents is None else documents
    revision = source_revision(root) if revision is None else revision
    sources = prepare_catalog(root, scratch_root=scratch_root,
                              documents=documents, revision=revision)
    # The release dispositions and web declarations decide the admitted universe.
    sources["source_paths"] = sorted({*sources["source_paths"], *admission_inputs(root)})
    return build_catalog(root, documents=documents, revision=revision,
                         source_catalog=sources, runtime_manifest=public_manifest(root),
                         runtime_paths=payload_paths(root))
