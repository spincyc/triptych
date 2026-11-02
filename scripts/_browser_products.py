"""Offline, content-addressed browser products; never source or approval evidence.

The descriptor records a mechanical two-build proof. Ordinary builds may only
reproduce its committed bytes. Readers hold a private verified snapshot for the
whole operation, so changing a cache pathname cannot change bytes being served.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
import hashlib
import errno
import fcntl
from functools import wraps
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
from typing import Any, Iterator

import _source_projection_receipt as receipt

MANIFEST_RELATIVE = "release/browser-products.json"
SCHEMA = "triptych-browser-products/v1"
INPUT_SCHEMA = "triptych-browser-product-inputs/v1"
POLICY_SCHEMA = "triptych-browser-publication-policy/v1"
PROOF = "two-independent-cold-builds-byte-parity"
INPUT_TREES = ("src", "scripts", "tools", "guidance", "workflows", "web", "release/publications", "release/rights", "release/papal-documents")
INPUT_FILES = ("AGENTS.md", "LICENSE", "THIRD_PARTY.md", "Makefile", "tmt.json", ".gitattributes", ".gitignore", "requirements-tools.txt", "requirements-public-alpha.txt", "requirements-tui.txt", "release/public-alpha.json", "release/papal-documents.json")
EXCLUDED = frozenset({MANIFEST_RELATIVE, *receipt.MECHANICAL_RECEIPTS})
POLICY_FIELDS = {"schema_version", "release_id", "provider", "providers", "authorizations"}
AUTH_FIELDS = {"basis", "authority_role", "authority_scope", "rights_record", "rights_record_sha256", "site_sources", "approved_on", "duration", "effective_at", "expires_at", "timezone", "conditions"}
_HELD: ContextVar[dict] = ContextVar("browser_products_held", default={})
_LOCKS: ContextVar[dict] = ContextVar("browser_product_locks", default={})


class ProductError(ValueError):
    """Missing, stale, corrupt, or unsafe mechanical browser products."""


@dataclass(frozen=True)
class VerifiedProducts:
    data_root: Path
    files: dict[str, Path]
    source_paths: set[str]
    products_identity: str
    projected_source_paths: set[str]


def _json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _sha(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProductError(f"duplicate JSON field: {key}")
        result[key] = value
    return result


def _decode(body: bytes) -> Any:
    try:
        return json.loads(body, object_pairs_hook=_unique, parse_constant=lambda value: (_ for _ in ()).throw(ProductError(f"invalid JSON constant: {value}")))
    except (UnicodeError, ValueError) as error:
        raise ProductError(f"invalid browser product JSON: {error}") from error


def _relative(value: str) -> str:
    if (not isinstance(value, str) or not value or "\\" in value or "\0" in value or PurePosixPath(value).is_absolute()
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise ProductError(f"unsafe browser product path: {value!r}")
    return value


def _keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ProductError(f"unsupported {label} fields; expected {sorted(expected)}")


def _digest(value):
    if not isinstance(value, str) or re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise ProductError("expected a lowercase SHA-256 identity")


def _read(root: Path, name: str) -> bytes:
    try:
        return receipt.read_file(Path("/"), (_absolute(root) / _relative(name)).as_posix().lstrip("/"))
    except (receipt.ReceiptError, OSError) as error:
        raise ProductError(str(error)) from error


def _absolute(path: Path) -> Path:
    """Lexical absolute path: resolving first would hide an unsafe symlink."""
    return Path(os.path.abspath(path))


def _safe_directory(path: Path, *, create=False):
    path = _absolute(path)
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            if create:
                try:
                    os.mkdir(part, dir_fd=descriptor)
                except FileExistsError:
                    pass
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
    except OSError as error:
        raise ProductError(f"missing or unsafe browser product directory: {path}: {error.strerror}") from error
    finally:
        os.close(descriptor)
    return path


def _excluded_namespace(name):
    return (name == "src/web/data" or name.startswith("src/web/data/")
            # Historical originals are optional delivery payloads. Their full
            # delivery, attested record and report metadata remain canonical;
            # snapshot-store independently rejects undeclared original files.
            or name == "release/papal-documents/inputs" or name.startswith("release/papal-documents/inputs/"))


def _regular_bytecode(name):
    # Call only after lstat has proved a regular file. Cache directories and
    # other members remain governed inputs; a .pyc name never excuses a link
    # or special filesystem object.
    path = PurePosixPath(name)
    return (name.startswith(("scripts/", "tools/")) and "__pycache__" in path.parts
            and path.suffix in {".pyc", ".pyo"})


def _paths(root: Path, trees=INPUT_TREES, files=INPUT_FILES, excludes=()) -> set[str]:
    """Physical membership includes ignored/new canonical inputs, without Git HEAD."""
    result = set()

    def walk(directory: int, prefix: str):
        before = os.fstat(directory)
        for entry in sorted(os.scandir(directory), key=lambda value: value.name):
            name = _relative(prefix + entry.name)
            if _excluded_namespace(name) or any(name == path or name.startswith(path + "/") for path in excludes):
                continue
            original = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(original.st_mode):
                child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                try:
                    if not receipt._same_inode(original, os.fstat(child)):
                        raise ProductError(f"canonical directory changed: {name}")
                    walk(child, name + "/")
                    receipt._require_entry(directory, entry.name, child)
                finally:
                    os.close(child)
            elif stat.S_ISREG(original.st_mode):
                if name not in EXCLUDED and not _regular_bytecode(name):
                    result.add(name)
            else:
                raise ProductError(f"canonical input must be a regular file or directory: {name}")
        if receipt._file_stamp(before) != receipt._file_stamp(os.fstat(directory)):
            raise ProductError(f"canonical membership changed: {prefix}")

    try:
        for tree in trees:
            try:
                with receipt._open_directory(root, tree) as directory:
                    walk(directory, tree + "/")
            except FileNotFoundError:
                continue
        for name in files:
            if _excluded_namespace(name) or any(name == path or name.startswith(path + "/") for path in excludes):
                continue
            try:
                with receipt._open_parent(root, name) as (parent, leaf):
                    mode = os.stat(leaf, dir_fd=parent, follow_symlinks=False).st_mode
                    if not stat.S_ISREG(mode):
                        raise ProductError(f"canonical input must be regular: {name}")
                    if name not in EXCLUDED and not _regular_bytecode(name):
                        result.add(name)
            except FileNotFoundError:
                continue
    except (OSError, receipt.ReceiptError) as error:
        raise ProductError(f"unsafe canonical inputs: {error}") from error
    for entry in os.scandir(root):
        if entry.name.startswith("requirements") and entry.name.endswith(".txt") or entry.name.endswith((".lock", "-lock.json")):
            if not stat.S_ISREG(entry.stat(follow_symlinks=False).st_mode):
                raise ProductError(f"dependency lock must be regular: {entry.name}")
            result.add(_relative(entry.name))
    return result


def _policy(body: bytes) -> dict:
    policy = _decode(body)
    _keys(policy, POLICY_FIELDS, "publication policy")
    if (type(policy["schema_version"]) is not int or policy["schema_version"] != 2
            or not isinstance(policy["release_id"], str) or not isinstance(policy["provider"], str)
            or not isinstance(policy["providers"], list) or not all(isinstance(p, str) for p in policy["providers"])
            or not isinstance(policy["authorizations"], dict)):
        raise ProductError("unsupported publication policy types/version")
    authors = {}
    for name, auth in policy["authorizations"].items():
        _keys(auth, AUTH_FIELDS, "publication authorization")
        for key in AUTH_FIELDS - {"authority_scope", "conditions", "site_sources", "expires_at"}:
            if not isinstance(auth[key], str):
                raise ProductError(f"invalid publication authorization field: {key}")
        if auth["expires_at"] is not None and not isinstance(auth["expires_at"], str):
            raise ProductError("invalid publication authorization expiry")
        for key in ("authority_scope", "conditions"):
            if not isinstance(auth[key], list) or not all(isinstance(item, str) for item in auth[key]):
                raise ProductError(f"invalid publication authorization list: {key}")
        if not isinstance(auth["site_sources"], dict):
            raise ProductError("invalid derived site sources")
        _relative(auth["rights_record"])
        authors[name] = {key: value for key, value in auth.items() if key not in {"site_sources", "rights_record_sha256"}}
    return {"schema": POLICY_SCHEMA, **{key: value for key, value in policy.items() if key != "authorizations"}, "authorizations": authors}


def _rights(body: bytes) -> bytes:
    """Omit only generated SHA table rows; preserve headings and policy prose."""
    text = body.decode("utf-8")
    header = "## Exact approved reader-facing site sources"
    if header not in text:
        return body
    pattern = re.compile(r"(^" + re.escape(header) + r"\s*$)([\s\S]*?)(?=^## |\Z)", re.MULTILINE)
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise ProductError("rights record must have exactly one generated site-source section")
    def omit(match):
        lines = []
        for line in match[2].splitlines(keepends=True):
            if re.fullmatch(r"\| `[^`]+` \| `[0-9a-f]{64}` \|\s*", line):
                continue
            lines.append(line)
        return match[1] + "".join(lines)
    return pattern.sub(omit, text).encode("utf-8")


def _component(name: str) -> str:
    if name.startswith(("scripts/", "tools/")) or name == "Makefile":
        return "generator"
    if "requirements" in name or PurePosixPath(name).name.endswith((".lock", "-lock.json")):
        return "lock"
    if name.startswith(("release/", "guidance/")) or name in {"LICENSE", "THIRD_PARTY.md", "AGENTS.md"} or any(token in name.lower() for token in ("rights", "artifact.toml", "web-edition.toml")):
        return "rights"
    return "content"


def _input_spec(recipe=None):
    if recipe is None:
        return INPUT_TREES, INPUT_FILES, ()
    trees = tuple(dict.fromkeys((*recipe["input_trees"], "scripts", "tools", "guidance", "release/publications", "release/rights")))
    files = tuple(dict.fromkeys((*recipe["input_files"], *INPUT_FILES)))
    return trees, files, tuple(recipe["exclude_paths"])


def _identity_batch(root: Path, recipes=None) -> dict:
    """One fresh content-hash pass for overlapping family closures per phase."""
    root = _safe_directory(root)
    recipes = _recipes() if recipes is None else recipes
    specs = {None: _input_spec(), **{recipe["id"]: _input_spec(recipe) for recipe in recipes}}
    trees = sorted({tree for spec in specs.values() for tree in spec[0]})
    trees = tuple(tree for tree in trees if not any(tree.startswith(parent + "/") for parent in trees if parent != tree))
    files = tuple(sorted({name for spec in specs.values() for name in spec[1]}))
    def discover():
        found = _paths(root, trees, files)
        selected = {}
        for key, (scopes, exact, excludes) in specs.items():
            selected[key] = {name for name in found
                             if (name in exact or any(name.startswith(tree + "/") for tree in scopes)
                                 or "/" not in name and (name.startswith("requirements") or name.endswith((".lock", "-lock.json"))))
                             and not any(name == excluded or name.startswith(excluded + "/") for excluded in excludes)}
        selected[None] = set().union(*selected.values())
        return selected
    memberships = discover()
    # The aggregate commits every canonical recipe scope, including paths
    # outside conservative roots, with one filesystem walk per phase.
    names = memberships[None]
    try:
        external = receipt._external_identities(root, names)
    except (receipt.ReceiptError, OSError, ValueError) as error:
        raise ProductError(f"invalid external source identities: {error}") from error
    memberships[None].update(external)
    for key in memberships:
        if key is not None:
            memberships[key].update(name for name, value in external.items() if value["manifest"] in memberships[key] or name in memberships[key])
    values = {}
    for name in sorted(memberships[None]):
        if name in external:
            value = {"path": name, "external": external[name]}
        else:
            body = _read(root, name)
            if name == "release/public-alpha.json":
                body = _json(_policy(body))
            elif name.startswith("release/rights/"):
                try:
                    body = _rights(body)
                except UnicodeError as error:
                    raise ProductError(f"rights record is not UTF-8: {name}") from error
            value = {"path": name, "sha256": _sha(body), "bytes": len(body)}
        values[name] = value
    after = discover()
    after[None].update(external)
    for key in after:
        if key is not None:
            after[key].update(name for name, value in external.items() if value["manifest"] in after[key] or name in after[key])
    if memberships != after:
        raise ProductError("canonical input membership changed while hashing")
    result = {}
    for key, members in memberships.items():
        components = {category: [] for category in ("content", "rights", "generator", "lock")}
        for name in sorted(members):
            components[_component(name)].append(values[name])
        identity = {"schema": INPUT_SCHEMA, **{category: _sha(_json(items)) for category, items in components.items()},
                    "membership": _sha(_json(sorted(members))), "count": len(members), "source_paths": sorted(members)}
        identity["sha256"] = _sha(_json({name: value for name, value in identity.items() if name != "source_paths"}))
        result[key] = identity
    return result


def input_identity(root: Path, product=None) -> dict:
    """Hash current canonical content/rights/code/locks and exact membership.

    Source membership is independently discovered. No output, descriptor,
    mechanical receipt, cache path, Git ref or timestamp supplies source identity.
    """
    key = product["id"] if isinstance(product, dict) else product
    result = _identity_batch(root)
    if key not in result:
        raise ProductError(f"unknown browser product family: {key}")
    return result[key]


def _commitment(identity):
    # Path membership is cryptographically committed once by its sorted-set
    # hash. Repeating tens of thousands of path strings in each family makes a
    # mechanical descriptor approach the size of the disposable products.
    return {name: value for name, value in identity.items() if name != "source_paths"}


def _validate_inputs(value):
    _keys(value, {"schema", "sha256", "content", "rights", "generator", "lock", "membership", "count"}, "input identity")
    if value["schema"] != INPUT_SCHEMA or type(value["count"]) is not int or value["count"] < 0:
        raise ProductError("unsupported browser product input identity")
    for key in ("sha256", "content", "rights", "generator", "lock", "membership"):
        _digest(value[key])
    if value["sha256"] != _sha(_json({key: item for key, item in value.items() if key != "sha256"})):
        raise ProductError("invalid browser product input digest")


def _recipes():
    from _browser_product_recipes import RECIPES
    recipes = json.loads(_json(RECIPES))
    ids = set()
    for recipe in recipes:
        _keys(recipe, {"id", "version", "output_prefixes", "argv", "input_trees", "input_files", "exclude_paths"}, "browser recipe")
        if not isinstance(recipe["id"], str) or recipe["id"] in ids or not isinstance(recipe["version"], (str, int)):
            raise ProductError("invalid browser recipe identity/version")
        ids.add(recipe["id"])
        for field in ("output_prefixes", "input_trees", "input_files", "exclude_paths"):
            if not isinstance(recipe[field], list):
                raise ProductError(f"invalid recipe paths: {field}")
            for name in recipe[field]:
                _relative(name)
        if not isinstance(recipe["argv"], list):
            raise ProductError("recipe argv must be a list")
    return recipes


def _validate_manifest(value):
    _keys(value, {"schema", "inputs", "recipes", "products", "proof", "editorial_approval"}, "browser product descriptor")
    if value["schema"] != SCHEMA or value["proof"] != PROOF or value["editorial_approval"] is not False:
        raise ProductError("unsupported browser product proof/schema")
    _validate_inputs(value["inputs"])
    if not isinstance(value["recipes"], list) or not value["recipes"] or not isinstance(value["products"], list) or not value["products"]:
        raise ProductError("browser product descriptor needs recipes and products")
    if value["recipes"] != _recipes():
        raise ProductError("browser product recipes changed; run `browser-products record` after reviewing the change")
    seen = set()
    ids = set()
    for product in value["products"]:
        _keys(product, {"id", "inputs", "key", "files", "count", "bytes", "path_set_sha256"}, "browser product family")
        if not isinstance(product["id"], str) or product["id"] in ids:
            raise ProductError("invalid or duplicate product family")
        ids.add(product["id"])
        _validate_inputs(product["inputs"])
        if product["key"] != family_identity(product, value["recipes"]):
            raise ProductError("invalid content-addressed browser family key")
        files = product["files"]
        if not isinstance(files, dict) or not files:
            raise ProductError("product family has no outputs")
        recipe = next((item for item in value["recipes"] if item["id"] == product["id"]), None)
        if recipe is None:
            raise ProductError("unknown browser product family")
        for name, identity in files.items():
            _relative(name)
            if not any(name == prefix or name.startswith(prefix + "/") for prefix in recipe["output_prefixes"]):
                raise ProductError(f"browser product path is outside its owning recipe: {name}")
            if not name.endswith(".json") or name in seen:
                raise ProductError(f"unexpected or overlapping browser product: {name}")
            seen.add(name)
            _keys(identity, {"sha256", "bytes"}, "browser output identity")
            _digest(identity["sha256"])
            if type(identity["bytes"]) is not int or identity["bytes"] < 0:
                raise ProductError("invalid browser output byte count")
        if (type(product["count"]) is not int or product["count"] != len(files)
                or type(product["bytes"]) is not int or product["bytes"] != sum(item["bytes"] for item in files.values())
                or product["path_set_sha256"] != _sha(_json(sorted(files)))):
            raise ProductError("browser product output inventory totals differ")
    recipe_ids = {recipe["id"] for recipe in value["recipes"]}
    if ids != recipe_ids:
        raise ProductError("browser product family membership differs from recipes")
    return value


def load_manifest(root: Path) -> dict:
    try:
        return _validate_manifest(_decode(_read(_safe_directory(root), MANIFEST_RELATIVE)))
    except ProductError as error:
        raise ProductError(f"browser product descriptor is missing, invalid, or stale: {error}") from error


def _expected(manifest):
    return {name: value for product in manifest["products"] for name, value in product["files"].items()}


def products_identity(manifest: dict) -> str:
    return _sha(_json(manifest))


def working_data_root(root: Path) -> Path:
    cache = cache_directory(_absolute(root))
    return cache.with_name(cache.name + "-work")


# Historical spelling retained for producer adapters.
working_root = working_data_root


def family_identity(product: dict, recipes: list) -> str:
    recipe = next(item for item in recipes if item["id"] == product["id"])
    return _sha(_json({"schema": SCHEMA, "recipe": recipe, "inputs": product["inputs"], "files": product["files"]}))


def cache_directory(root: Path, cache_root=None) -> Path:
    value = cache_root if cache_root is not None else os.environ.get("TRIPTYCH_BROWSER_DATA_ROOT", "build/browser-data")
    path = Path(value)
    return _absolute(path if path.is_absolute() else root / path)


def _inventory(target: Path) -> dict:
    """Hash exact JSON membership using descriptor-relative, no-follow opens."""
    target = _safe_directory(target)
    files = {}
    def walk(directory, prefix):
        before = os.fstat(directory)
        for entry in sorted(os.scandir(directory), key=lambda value: value.name):
            name = _relative(prefix + entry.name)
            original = entry.stat(follow_symlinks=False)
            if stat.S_ISDIR(original.st_mode):
                child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory)
                try:
                    if not receipt._same_inode(original, os.fstat(child)):
                        raise ProductError(f"product directory changed: {name}")
                    count_before = len(files)
                    walk(child, name + "/")
                    if len(files) == count_before:
                        raise ProductError(f"unexpected empty browser product directory: {name}")
                    receipt._require_entry(directory, entry.name, child)
                finally:
                    os.close(child)
            elif stat.S_ISREG(original.st_mode) and original.st_nlink == 1 and name.endswith(".json"):
                digest, size = receipt._file_hash_at(directory, entry.name, name)
                files[name] = {"sha256": digest, "bytes": size}
            else:
                raise ProductError(f"unexpected or unsafe product output: {name}")
        if receipt._file_stamp(before) != receipt._file_stamp(os.fstat(directory)):
            raise ProductError("product membership changed during verification")
    try:
        with receipt._open_directory(Path("/"), target.as_posix().lstrip("/")) as descriptor:
            walk(descriptor, "")
    except (OSError, receipt.ReceiptError) as error:
        raise ProductError(f"cannot verify product outputs: {error}") from error
    if not files:
        raise ProductError("browser products have no outputs")
    return files


def _compare(actual, expected):
    if actual == expected:
        return
    missing, extra = sorted(expected.keys() - actual.keys()), sorted(actual.keys() - expected.keys())
    changed = sorted(key for key in expected.keys() & actual.keys() if expected[key] != actual[key])
    raise ProductError(f"browser product bytes/membership differ (missing={missing[:4]}, extra={extra[:4]}, changed={changed[:4]}); remove the corrupt exact cache entry and run `browser-products build`, or review inputs and explicitly `browser-products record`")


def _current(root, manifest):
    current = _identity_batch(root)
    if manifest["inputs"] != _commitment(current[None]) or any(product["inputs"] != _commitment(current[product["id"]]) for product in manifest["products"]):
        raise ProductError("browser product inputs changed; review source/rights/code changes and run `browser-products record` explicitly")
    return current


def _cache_data(root, product, cache_root=None):
    parent = cache_directory(root, cache_root)
    target = parent / product["key"]
    _safe_directory(parent)
    with receipt._open_directory(Path("/"), parent.as_posix().lstrip("/")) as cache_fd:
        with os.scandir(cache_fd) as entries:
            for entry in entries:
                mode = entry.stat(follow_symlinks=False).st_mode
                if entry.name == ".browser-products-cache-v1" and stat.S_ISREG(mode):
                    continue
                if re.fullmatch(r"[0-9a-f]{64}", entry.name) is None or not stat.S_ISDIR(mode):
                    raise ProductError(f"unexpected or unsafe browser cache entry: {entry.name}")
    _safe_directory(target)
    with receipt._open_directory(Path("/"), target.as_posix().lstrip("/")) as descriptor:
        if set(os.listdir(descriptor)) != {"data"}:
            raise ProductError("unexpected files in sealed browser product cache entry")
    return _safe_directory(target / "data")


def check(root: Path, *, cache_root=None, product_ids=None) -> dict:
    root = _safe_directory(root)
    before = _read(root, MANIFEST_RELATIVE)
    manifest = _validate_manifest(_decode(before))
    _current(root, manifest)
    for product in _selected(manifest, product_ids):
        target = _cache_data(root, product, cache_root)
        _compare(_inventory(target), product["files"])
    if product_ids is None:
        aggregate = {"key": products_identity(manifest), "files": _expected(manifest)}
        _compare(_inventory(_cache_data(root, aggregate, cache_root)), aggregate["files"])
    _current(root, manifest)
    if before != _read(root, MANIFEST_RELATIVE):
        raise ProductError("browser product descriptor changed during check")
    return manifest


def _selected(manifest, product_ids=None):
    if product_ids is None:
        return manifest["products"]
    wanted = set(product_ids)
    known = {product["id"] for product in manifest["products"]}
    if not wanted or wanted - known:
        raise ProductError(f"unknown browser product families: {sorted(wanted - known)}")
    return [product for product in manifest["products"] if product["id"] in wanted]


def _held_key(root, cache_root, product_ids=None):
    return (str(_absolute(root)), str(cache_directory(_absolute(root), cache_root)), None if product_ids is None else tuple(sorted(set(product_ids))))


def held_products(root: Path, *, cache_root=None, product_ids=None) -> VerifiedProducts | None:
    # A full held context can safely satisfy a selected consumer.
    return _HELD.get().get(_held_key(root, cache_root)) or _HELD.get().get(_held_key(root, cache_root, product_ids))


def require_products(root: Path, *, cache_root=None) -> VerifiedProducts:
    products = held_products(root, cache_root=cache_root)
    if products is None:
        raise ProductError("browser product paths require a held `verified_products` context for the entire operation")
    return products


def _scratch(root):
    return _safe_directory(root / ".scratch/next-product-store", create=True)


@contextmanager
def verified_products(root: Path, *, cache_root=None, product_ids=None) -> Iterator[VerifiedProducts]:
    root = _safe_directory(root)
    existing = held_products(root, cache_root=cache_root, product_ids=product_ids)
    if existing is not None:
        yield existing
        return
    before = _read(root, MANIFEST_RELATIVE)
    manifest = _validate_manifest(_decode(before))
    current = _current(root, manifest)
    selected = _selected(manifest, product_ids)
    expected = {name: value for product in selected for name, value in product["files"].items()}
    with tempfile.TemporaryDirectory(prefix="verified-", dir=_scratch(root)) as temporary:
        snapshot = Path(temporary) / "data"
        snapshot.mkdir()
        for product in selected:
            target = _cache_data(root, product, cache_root)
            for name, identity in product["files"].items():
                body = _read(target, name)
                if {"sha256": _sha(body), "bytes": len(body)} != identity:
                    raise ProductError(f"browser product changed before private snapshot: {name}")
                destination = snapshot / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(body)
            _compare(_inventory(target), product["files"])
        if before != _read(root, MANIFEST_RELATIVE):
            raise ProductError("browser product descriptor changed before private snapshot")
        result = VerifiedProducts(snapshot, {name: snapshot / name for name in expected},
                                  {name for name in current[None]["source_paths"] if _component(name) in {"generator", "lock"}} | {MANIFEST_RELATIVE},
                                  products_identity(manifest),
                                  {name for name in current[None]["source_paths"] if name == "release/public-alpha.json" or name.startswith("release/rights/")})
        key = _held_key(root, cache_root, product_ids)
        token = _HELD.set({**_HELD.get(), key: result})
        try:
            yield result
            _compare(_inventory(snapshot), expected)
            _current(root, manifest)
            if before != _read(root, MANIFEST_RELATIVE):
                raise ProductError("browser product descriptor changed during operation")
        finally:
            _HELD.reset(token)


def _generate(root, out, product_ids=None):
    from _browser_product_recipes import generate
    generate(root, out, product_ids=product_ids)


def _install(root, product, generated, cache_root):
    parent = _safe_directory(cache_directory(root, cache_root), create=True)
    with receipt._open_directory(Path("/"), parent.as_posix().lstrip("/")) as cache_fd:
        marker_fd = os.open(".browser-products-cache-v1", os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o644, dir_fd=cache_fd)
        try:
            if not stat.S_ISREG(os.fstat(marker_fd).st_mode):
                raise ProductError("browser cache marker must be a regular file")
        finally:
            os.close(marker_fd)
    destination = parent / product["key"]
    if destination.exists() or destination.is_symlink():
        _compare(_inventory(_cache_data(root, product, cache_root)), product["files"])
        return
    # Cache entries and private build trees share the conventional repository
    # filesystem. Refuse a cross-device promotion instead of partial copying.
    with tempfile.TemporaryDirectory(prefix="install-", dir=_scratch(root)) as temporary:
        staged = Path(temporary) / "entry"
        staged.mkdir()
        for name, expected in product["files"].items():
            body = _read(generated, name)
            if {"sha256": _sha(body), "bytes": len(body)} != expected:
                raise ProductError(f"generated product changed before install: {name}")
            target = staged / "data" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
        _compare(_inventory(staged / "data"), product["files"])
        try:
            with receipt._open_directory(Path("/"), parent.as_posix().lstrip("/")) as cache_fd:
                with receipt._open_directory(Path("/"), staged.parent.as_posix().lstrip("/")) as staging_fd:
                    os.rename(staged.name, destination.name, src_dir_fd=staging_fd, dst_dir_fd=cache_fd)
        except OSError as error:
            if error.errno in {errno.EEXIST, errno.ENOTEMPTY}:
                _compare(_inventory(_cache_data(root, product, cache_root)), product["files"])
            else:
                raise ProductError(f"cannot atomically install browser products: {error}") from error


def committed_data_root(root: Path, *, cache_root=None) -> Path:
    """Locate the stable aggregate view; callers must run the product gate first.

    This accessor intentionally does not hash inputs or hold an expiring context.
    Reading for publication uses verified_products instead.
    """
    manifest = load_manifest(root)
    return cache_directory(_absolute(root), cache_root) / products_identity(manifest) / "data"


current_data_root = committed_data_root
default_data_root = committed_data_root


def assert_working_output(root: Path, target: Path) -> Path:
    target = _absolute(target if Path(target).is_absolute() else root / target)
    existing = target
    while not existing.exists() and not existing.is_symlink():
        existing = existing.parent
    _safe_directory(existing if existing.is_dir() else existing.parent)
    if existing.is_symlink():
        raise ProductError("ordinary producer output must not follow a symlink")
    known = {cache_directory(_absolute(root)), _absolute(root) / "build/browser-data"}
    known.update(products.data_root for products in _HELD.get().values())
    for ancestor in (target, *target.parents):
        if (ancestor / ".browser-products-cache-v1").exists():
            known.add(ancestor)
    for cache in known:
        if target == cache or target in cache.parents or cache in target.parents:
            raise ProductError("ordinary producer --out must use a working directory outside the sealed browser product cache")
    return target


def _assemble(root, manifest, cache_root):
    combined = {"key": products_identity(manifest), "files": _expected(manifest)}
    entry = cache_directory(root, cache_root) / combined["key"]
    if entry.exists() or entry.is_symlink():
        _compare(_inventory(_cache_data(root, combined, cache_root)), combined["files"])
        return
    with tempfile.TemporaryDirectory(prefix="aggregate-", dir=_scratch(root)) as temporary:
        out = Path(temporary) / "data"
        out.mkdir()
        for product in manifest["products"]:
            target = _cache_data(root, product, cache_root)
            for name, identity in product["files"].items():
                body = _read(target, name)
                if {"sha256": _sha(body), "bytes": len(body)} != identity:
                    raise ProductError(f"family changed while assembling aggregate: {name}")
                destination = out / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(body)
        _install(root, combined, out, cache_root)


def build(root: Path, *, cache_root=None) -> dict:
    root = _safe_directory(root)
    before = _read(root, MANIFEST_RELATIVE)
    manifest = _validate_manifest(_decode(before))
    _current(root, manifest)
    missing = []
    for product in manifest["products"]:
        entry = cache_directory(root, cache_root) / product["key"]
        if entry.exists() or entry.is_symlink():
            _compare(_inventory(_cache_data(root, product, cache_root)), product["files"])
        else:
            missing.append(product)
    if missing:
        with tempfile.TemporaryDirectory(prefix="cold-", dir=_scratch(root)) as temporary:
            out = Path(temporary) / "data"
            _generate(root, out, [product["id"] for product in missing])
            expected = {name: value for product in missing for name, value in product["files"].items()}
            _compare(_inventory(out), expected)
            _current(root, manifest)
            if before != _read(root, MANIFEST_RELATIVE):
                raise ProductError("browser product descriptor changed during cold build")
            for product in missing:
                _install(root, product, out, cache_root)
    _assemble(root, manifest, cache_root)
    return check(root, cache_root=cache_root)


def _family_products(files, recipes, inputs):
    products = []
    assigned = set()
    for recipe in recipes:
        owned = {name: identity for name, identity in files.items() if any(name == prefix or name.startswith(prefix.rstrip("/") + "/") for prefix in recipe["output_prefixes"])}
        if assigned.intersection(owned):
            raise ProductError("recipe output prefixes overlap")
        assigned.update(owned)
        product = {"id": recipe["id"], "inputs": inputs[recipe["id"]], "files": owned, "count": len(owned), "bytes": sum(item["bytes"] for item in owned.values()), "path_set_sha256": _sha(_json(sorted(owned)))}
        product["key"] = family_identity(product, recipes)
        products.append(product)
    if assigned != set(files):
        raise ProductError(f"producer emitted outputs without an owning recipe: {sorted(set(files) - assigned)[:4]}")
    return products


def record(root: Path, *, cache_root=None) -> dict:
    root = _safe_directory(root)
    descriptor_before = _read(root, MANIFEST_RELATIVE) if os.path.lexists(root / MANIFEST_RELATIVE) else None
    recipes = _recipes()
    identities = _identity_batch(root, recipes)
    inputs = _commitment(identities[None])
    family_inputs = {recipe["id"]: _commitment(identities[recipe["id"]]) for recipe in recipes}
    # Reuse only an exact previous two-build proof, current family identity and
    # complete validated cache. A cache miss always receives two new cold builds.
    retained = {}
    try:
        previous = load_manifest(root)
    except ProductError:
        previous = None
    if previous:
        for product in previous["products"]:
            if product["inputs"] == family_inputs.get(product["id"]):
                entry = cache_directory(root, cache_root) / product["key"]
                if entry.exists() or entry.is_symlink():
                    _compare(_inventory(_cache_data(root, product, cache_root)), product["files"])
                    retained[product["id"]] = product
    changed = [recipe for recipe in recipes if recipe["id"] not in retained]
    with tempfile.TemporaryDirectory(prefix="record-", dir=_scratch(root)) as temporary:
        if changed:
            first, second = Path(temporary) / "first", Path(temporary) / "second"
            ids = [recipe["id"] for recipe in changed]
            _generate(root, first, ids)
            outputs = _inventory(first)
            _generate(root, second, ids)
            _compare(_inventory(second), outputs)
            products = _family_products(outputs, changed, family_inputs)
        else:
            products = []
        if identities != _identity_batch(root, recipes) or recipes != _recipes():
            raise ProductError("canonical inputs changed during independent cold builds; descriptor was not written")
        generated = {product["id"]: product for product in products}
        manifest = {"schema": SCHEMA, "inputs": inputs, "recipes": recipes,
                    "products": [retained.get(recipe["id"]) or generated[recipe["id"]] for recipe in recipes],
                    "proof": PROOF, "editorial_approval": False}
        _validate_manifest(manifest)
        for product in products:
            _install(root, product, first, cache_root)
        _assemble(root, manifest, cache_root)
        if inputs != _commitment(input_identity(root)):
            raise ProductError("canonical inputs changed before descriptor write")
        descriptor_after = _read(root, MANIFEST_RELATIVE) if os.path.lexists(root / MANIFEST_RELATIVE) else None
        if descriptor_before != descriptor_after:
            raise ProductError("browser product descriptor changed during recording; no descriptor was written")
        try:
            receipt.atomic_write(root, MANIFEST_RELATIVE, (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8"), scratch=_scratch(root))
        except (OSError, receipt.ReceiptError) as error:
            raise ProductError(f"cannot safely write product descriptor: {error}") from error
    return manifest


def prune(root: Path, *, cache_root=None) -> dict:
    """Remove obsolete disposable keys only after proving the current cache."""
    root = _safe_directory(root)
    manifest = check(root, cache_root=cache_root)
    parent = _safe_directory(cache_directory(root, cache_root))
    keep = {products_identity(manifest), *(product["key"] for product in manifest["products"])}
    try:
        with receipt._open_directory(Path("/"), parent.as_posix().lstrip("/")) as descriptor:
            marker = os.stat(".browser-products-cache-v1", dir_fd=descriptor, follow_symlinks=False)
            if not stat.S_ISREG(marker.st_mode):
                raise ProductError("refusing to prune a cache without its regular ownership marker")
            obsolete = []
            with os.scandir(descriptor) as entries:
                for entry in entries:
                    if entry.name == ".browser-products-cache-v1":
                        continue
                    if re.fullmatch(r"[0-9a-f]{64}", entry.name) is None or not stat.S_ISDIR(entry.stat(follow_symlinks=False).st_mode):
                        raise ProductError(f"refusing to prune an unknown or unsafe cache entry: {entry.name}")
                    if entry.name not in keep:
                        obsolete.append(entry.name)
            if not shutil.rmtree.avoids_symlink_attacks:
                raise ProductError("this platform cannot safely prune cache directories")
            for name in obsolete:
                shutil.rmtree(name, dir_fd=descriptor)
    except (OSError, receipt.ReceiptError) as error:
        raise ProductError(f"cannot safely prune browser cache: {error}") from error
    return manifest


@contextmanager
def _cache_lock(root: Path, cache_root=None, *, exclusive=False):
    root = _safe_directory(root)
    key = str(cache_directory(root, cache_root))
    held = _LOCKS.get()
    if key in held:
        if exclusive and not held[key]:
            raise ProductError("cannot build, record or prune while holding a read-only browser product context")
        yield
        return
    # Advisory coordination is transient, never a cached success stamp or an
    # input identity. It also works before the cache itself has been created.
    lock_path = _scratch(root) / ("cache-" + _sha(key.encode()) + ".lock")
    descriptor = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise ProductError("browser cache lock must be a regular file")
        fcntl.flock(descriptor, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        token = _LOCKS.set({**held, key: exclusive})
        try:
            yield
        finally:
            _LOCKS.reset(token)
            fcntl.flock(descriptor, fcntl.LOCK_UN)
    finally:
        os.close(descriptor)


def _locked(function, *, exclusive):
    @wraps(function)
    def call(root, *, cache_root=None, **kwargs):
        with _cache_lock(root, cache_root, exclusive=exclusive):
            return function(root, cache_root=cache_root, **kwargs)
    return call


check = _locked(check, exclusive=False)
build = _locked(build, exclusive=True)
record = _locked(record, exclusive=True)
prune = _locked(prune, exclusive=True)
_verified_products_unlocked = verified_products


@contextmanager
def verified_products(root: Path, *, cache_root=None, product_ids=None):
    with _cache_lock(root, cache_root):
        with _verified_products_unlocked(root, cache_root=cache_root, product_ids=product_ids) as products:
            yield products


def main(argv=None, *, examples=None):
    parser = argparse.ArgumentParser(description=__doc__)
    if examples is not None:
        from _tooling import examples_live_on_the_verbs, with_examples
        examples_live_on_the_verbs(parser, "browser-products")
    sub = parser.add_subparsers(dest="verb", required=True)
    for verb in ("check", "build", "record", "key", "prune"):
        child = sub.add_parser(verb, help={"check": "Verify current inputs and every exact cached output, offline.", "build": "Reproduce committed products offline on an exact cache miss.", "record": "Explicitly record byte parity from two independent cold builds.", "key": "Print the exact current descriptor/cache identity without generating.", "prune": "Verify current products, then remove obsolete disposable cache keys."}[verb])
        if examples is not None:
            with_examples(child, examples.get(verb, ()))
        child.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        child.add_argument("--cache-root", type=Path)
        child.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.verb == "key":
            manifest = load_manifest(args.root)
            _current(args.root, manifest)
        else:
            manifest = globals()[args.verb](args.root, cache_root=args.cache_root)
        result = {"status": "ok", "products_identity": products_identity(manifest), "family_keys": {product["id"]: product["key"] for product in manifest["products"]}, "products": len(manifest["products"]), "files": len(_expected(manifest)), "bytes": sum(value["bytes"] for value in _expected(manifest).values())}
        print(json.dumps(result, sort_keys=True) if args.json else products_identity(manifest) if args.verb == "key" else f"browser-products: {result['products']} products, {result['files']} files; ok")
        return 0
    except (ProductError, OSError) as error:
        print(json.dumps({"status": "error", "error": str(error)}, sort_keys=True) if args.json else f"browser-products: {error}", file=sys.stdout if args.json else sys.stderr)
        return 1
