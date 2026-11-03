"""Exact public transport for admitted native TeX editions and their runtime.

This layer does not compile a PDF or acquire a dependency.  The source bundle
producer owns the original TeX graph; the runtime registry owns every engine,
package and font byte.  The publisher joins those two inventories to its
current public admission set and re-derives the join during verification.
"""
from __future__ import annotations

import hashlib
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
    "src/common/native-tex-runtime.json",
)
_SHA = re.compile(r"[0-9a-f]{64}\Z")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")


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


def build_catalog(root: Path, *, documents: dict, revision: str,
                  source_catalog: dict, runtime_manifest: dict,
                  runtime_paths: dict) -> dict:
    """Validate a complete join.  Arguments expose the seam for focused tests."""
    root = Path(root).resolve()
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
    from _native_print import admitted_documents, source_revision
    from _native_print_bundles import prepare_catalog
    from _native_tex_assets import public_manifest, payload_paths

    root = Path(root).resolve()
    documents = admitted_documents(root) if documents is None else documents
    revision = source_revision(root) if revision is None else revision
    sources = prepare_catalog(root, scratch_root=scratch_root,
                              documents=documents, revision=revision)
    return build_catalog(root, documents=documents, revision=revision,
                         source_catalog=sources, runtime_manifest=public_manifest(root),
                         runtime_paths=payload_paths(root))
