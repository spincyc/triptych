"""Preserve exact historical papal release inputs in a separate delivery index.

These are frozen installation and review records, not source-library artifacts.
Metadata checks attest declarations; opening or replaying original JSON requires
hash-verified local bytes. Network access is opt-in through explicit hydration.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
from typing import Any

import _artifact_store as transport

INDEX_PATH = "release/papal-documents/input-delivery.json"
RELEASE_PATH = "release/papal-documents.json"
PREFIX = "release/papal-documents/inputs/"
SCHEMA = "triptych-papal-input-delivery/v1"
KIND = "historical-release-input"
DEFAULT_URL = "https://github.com/spincyc/triptych-artifacts/releases/download/{release}/{archive}"
SnapshotStoreError = transport.ArtifactStoreError


def _owned_path(value: Any) -> str:
    relative = transport._relative(value)
    path = PurePosixPath(relative)
    if str(path.parent) + "/" != PREFIX or path.suffix not in {".json", ".jsonl"}:
        raise SnapshotStoreError(f"not a frozen papal input path: {relative}")
    return relative


def _validate(data: Any) -> None:
    transport.validate_delivery_index(data, schema=SCHEMA, kinds=(KIND,), path_prefix=PREFIX)
    for entry in data["artifacts"]:
        path = PurePosixPath(_owned_path(entry["path"]))
        if path.stem != entry["sha256"]:
            raise SnapshotStoreError(f"frozen input filename must equal its exact SHA-256: {path}")
        media = "application/x-ndjson" if path.suffix == ".jsonl" else "application/json"
        if entry["media_type"] != media or entry["bytes"] <= 0 or "origin_url" in entry:
            raise SnapshotStoreError(f"invalid frozen input media, extent, or origin fields: {path}")


@lru_cache(maxsize=8)
def _load_index(path: Path, mtime: int, ctime: int, size: int) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=transport._unique_keys)
        _validate(data)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        if isinstance(error, SnapshotStoreError):
            raise
        raise SnapshotStoreError(f"invalid {INDEX_PATH}: {error}") from error
    return data


def load_index(root: Path | str) -> dict[str, Any]:
    """Return read-only parsed metadata, cached against filesystem changes."""
    path = transport._path(Path(root), INDEX_PATH)
    if not path.exists():
        return {"schema": SCHEMA, "archives": [], "artifacts": []}
    stat = path.stat()
    return _load_index(path, stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size)


def known_external(root: Path | str, path: str | Path) -> dict[str, Any] | None:
    relative = _owned_path(str(path))
    return next((entry for entry in load_index(root)["artifacts"] if entry["path"] == relative), None)


def cache_path(root: Path | str, entry: dict[str, Any]) -> Path:
    return transport.cache_path(root, entry)


def validate_ref(root: Path | str, ref: dict[str, Any], require_bytes: bool = False) -> dict[str, Any]:
    """Match an unchanged release reference to exact delivery declarations.

    Metadata mode does not assert row inclusion or open a declared snapshot.
    Older/local fixtures without a delivery declaration require verified bytes.
    Extra reference fields such as row_index remain owned by their consumer.
    """
    if not isinstance(ref, dict):
        raise SnapshotStoreError("frozen input reference must be an object")
    relative = _owned_path(ref.get("path"))
    digest, size = ref.get("sha256"), ref.get("bytes")
    if not isinstance(digest, str) or not transport._DIGEST.fullmatch(digest) or type(size) is not int or size <= 0:
        raise SnapshotStoreError(f"invalid frozen input reference pins: {relative}")
    entry = known_external(root, relative)
    if entry is None:
        if transport._path(Path(root), INDEX_PATH).exists():
            raise SnapshotStoreError(f"frozen input reference is not declared: {relative}")
        # A missing declaration never grants metadata-only acceptance to an
        # arbitrary absent path. This also keeps pre-delivery test fixtures.
        transport._verify(transport._path(Path(root), relative), ref)
        return {"path": relative, "sha256": digest, "bytes": size, "kind": KIND,
                "media_type": "application/x-ndjson" if relative.endswith(".jsonl") else "application/json"}
    if entry["sha256"] != digest or entry["bytes"] != size:
        raise SnapshotStoreError(f"frozen input delivery reference hash/size mismatch: {relative}")
    if require_bytes:
        resolve(root, relative)
    return entry


def resolve(root: Path | str, path: str | Path, fetch: bool = False) -> Path:
    """Resolve original/cache bytes, refusing network access unless explicit."""
    root = Path(root)
    relative = _owned_path(str(path))
    original = transport._path(root, relative)
    entry = known_external(root, relative)
    if entry is None and transport._path(root, INDEX_PATH).exists():
        raise SnapshotStoreError(f"frozen input path is not declared: {relative}")
    if original.is_file():
        return transport._verify(original, entry) if entry else original
    if entry is None:
        raise FileNotFoundError(f"no original frozen input or delivery declaration: {relative}")
    cached = cache_path(root, entry)
    if cached.exists():
        return transport._verify(cached, entry)
    if fetch:
        hydrate(root, [relative], fetch=True)
        return transport._verify(cached, entry)
    raise FileNotFoundError(f"frozen input is not cached: {relative}; run tools/snapshot-store hydrate {relative} --archive-dir PACK or explicitly --fetch")


def _release_refs(root: Path) -> list[dict[str, Any]]:
    path = transport._path(root, RELEASE_PATH)
    if not path.exists():
        return []
    try:
        release = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=transport._unique_keys)
    except (OSError, UnicodeError, ValueError) as error:
        raise SnapshotStoreError(f"cannot inspect frozen input references: {error}") from error
    refs: dict[tuple[str, str, int], dict[str, Any]] = {}

    def visit(value):
        if isinstance(value, dict):
            if isinstance(value.get("path"), str) and value["path"].startswith(PREFIX):
                # Validate types before using the values as dictionary keys.
                relative = _owned_path(value["path"])
                if not isinstance(value.get("sha256"), str) or type(value.get("bytes")) is not int:
                    raise SnapshotStoreError(f"invalid release frozen input reference: {relative}")
                refs[(relative, value["sha256"], value["bytes"])] = value
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(release)
    return list(refs.values())


def validate_index(root: Path | str, local_bytes: bool = False) -> list[str]:
    """Check delivery/reference metadata; optionally verify existing local bytes."""
    root = Path(root).resolve()
    try:
        data = load_index(root)
        if transport._path(root, INDEX_PATH).exists():
            folder = transport._path(root, PREFIX.rstrip("/"))
            declared = {entry["path"] for entry in data["artifacts"]}
            if folder.exists():
                if not folder.is_dir():
                    raise SnapshotStoreError("frozen input directory is not a directory")
                for path in folder.iterdir():
                    relative = path.relative_to(root).as_posix()
                    if path.is_symlink() or not path.is_file() or relative not in declared:
                        raise SnapshotStoreError(f"unregistered or nonregular frozen input: {relative}")
        for ref in _release_refs(root):
            validate_ref(root, ref)
        if local_bytes:
            for entry in data["artifacts"]:
                for path in (transport._path(root, entry["path"]), cache_path(root, entry)):
                    if path.exists():
                        transport._verify(path, entry)
        return []
    except (SnapshotStoreError, OSError) as error:
        return [str(error)]


def hydrate(root: Path | str, paths: list[str], *, archive_dir: Path | str | None = None,
            fetch: bool = False) -> list[Path]:
    root = Path(root).resolve()
    data = load_index(root)
    wanted = {_owned_path(path) for path in paths}
    entries = {entry["path"]: entry for entry in data["artifacts"]}
    if wanted - entries.keys():
        raise SnapshotStoreError(f"frozen input paths not declared: {sorted(wanted - entries.keys())[:3]}")
    missing = set()
    for relative in wanted:
        try:
            resolve(root, relative)
        except FileNotFoundError:
            missing.add(relative)
    for archive in data["archives"]:
        members = [entry for entry in data["artifacts"] if entry["archive"] == archive["id"]]
        if missing.intersection(entry["path"] for entry in members):
            local = transport._archive_path(root, archive, Path(archive_dir) if archive_dir else None, fetch)
            transport._read_archive(local, members, root, missing)
    return [resolve(root, relative) for relative in sorted(wanted)]


def _inventory(root: Path) -> list[dict[str, Any]]:
    root = Path(root).resolve()
    previous = {entry["path"]: entry for entry in load_index(root)["artifacts"]}
    paths = set(subprocess.check_output(["git", "ls-files", "-z", "--", PREFIX], cwd=root).decode("utf-8").strip("\0").split("\0")) - {""}
    paths.update(previous)
    # Future inputs are written into this ignored directory after the original
    # tracked snapshots have been retired. Discover those exact files without
    # requiring an otherwise unnecessary force-add to Git.
    folder = transport._path(root, PREFIX.rstrip("/"))
    if folder.exists():
        if not folder.is_dir():
            raise SnapshotStoreError("frozen input directory is not a directory")
        for path in sorted(folder.iterdir()):
            relative = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.is_file():
                raise SnapshotStoreError(f"nonregular frozen input cannot be inventoried: {relative}")
            paths.add(_owned_path(relative))
    result = []
    for relative in sorted(paths):
        _owned_path(relative)
        path = transport._path(root, relative)
        if path.is_file():
            old = previous.get(relative)
            if old is not None:
                transport._verify(path, old)
            digest = transport._digest(path)
            if PurePosixPath(relative).stem != digest:
                raise SnapshotStoreError(f"frozen input filename does not match exact bytes: {relative}")
            entry = {"path": relative, "sha256": digest, "bytes": path.stat().st_size, "kind": KIND,
                     "media_type": "application/x-ndjson" if relative.endswith(".jsonl") else "application/json"}
        elif relative in previous:
            entry = {key: value for key, value in previous[relative].items() if key not in {"archive", "member"}}
        else:
            raise FileNotFoundError(f"tracked frozen input is missing without a delivery declaration: {relative}")
        if entry["bytes"] <= 0:
            raise SnapshotStoreError(f"empty frozen input: {relative}")
        result.append(entry)
    return result


def pack(root: Path | str, out: Path | str, *, release: str, url_template: str = DEFAULT_URL,
         max_archive_bytes: int = transport.MAX_ARCHIVE_BYTES) -> dict[str, Any]:
    root, out = Path(root).resolve(), Path(out).resolve()
    if not transport._SLUG.fullmatch(release) or not 10240 <= max_archive_bytes <= transport.MAX_ARCHIVE_BYTES:
        raise SnapshotStoreError("release must be a safe slug and archive limit between 10240 and 512000000")
    inventory = _inventory(root)
    inventory_by_path = {entry["path"]: entry for entry in inventory}

    def packing_resolver(base, relative):
        original = transport._path(base, relative)
        if original.is_file():
            return transport._verify(original, inventory_by_path[relative])
        return resolve(base, relative)

    archives, entries = transport.pack_delivery_archives(root, out, inventory, resolver=packing_resolver,
        release=release, archive_prefix="triptych-papal-inputs", url_template=url_template,
        max_archive_bytes=max_archive_bytes)
    snapshot = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    data = {"schema": SCHEMA, "snapshot": snapshot, "archives": archives, "artifacts": entries}
    _validate(data)
    indexed = {entry["path"]: entry for entry in entries}
    for ref in _release_refs(root):
        entry = indexed.get(ref["path"])
        if entry is None or entry["sha256"] != ref["sha256"] or entry["bytes"] != ref["bytes"]:
            raise SnapshotStoreError(f"release reference is not preserved by snapshot pack: {ref['path']}")
    transport._json(transport._path(root, INDEX_PATH), data)
    transport._json(out / "input-delivery.json", data)
    for source, name in ((Path(__file__), "snapshot-store.py"), (Path(transport.__file__), "_artifact_store.py")):
        if source.resolve() != (out / name).resolve():
            shutil.copyfile(source, out / name)
    (out / "README.txt").write_text(
        "Triptych frozen papal release input offline pack\n\n"
        "Preserves exact JSON and JSONL bytes, including currently unreferenced snapshots.\n"
        "Keep both Python files and all archives together. Python 3.11+ is required.\n"
        "Use the matching checkout with release/papal-documents/input-delivery.json.\n"
        "Verify the whole pack without network access:\n"
        "  python3 snapshot-store.py check --root /path/to/checkout --archives --archive-dir .\n"
        "Restore missing snapshots into the checkout's ignored content cache:\n"
        "  python3 snapshot-store.py hydrate --root /path/to/checkout --all --archive-dir .\n"
        "Then check --require-local verifies all original bytes. No path is recreated\n"
        "under release/papal-documents/inputs/. Metadata checks attest declarations,\n"
        "not row-inclusion replay. Use the separate full evidence audit for that.\n"
        "No command uploads archives. Only an explicit --fetch permits downloads.\n",
        encoding="utf-8")
    sums = [(archive["name"], archive["sha256"]) for archive in archives]
    sums.extend((name, transport._digest(out / name)) for name in
                ("input-delivery.json", "snapshot-store.py", "_artifact_store.py", "README.txt"))
    (out / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sums), encoding="utf-8")
    return data


def _summary(data: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ok", "snapshots": len(data["artifacts"]),
            "bytes": sum(entry["bytes"] for entry in data["artifacts"]), "archives": len(data["archives"]),
            "archive_bytes": sum(entry["bytes"] for entry in data["archives"])}


def main(argv: list[str] | None = None, *, examples: dict | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    if examples is not None:
        from _tooling import examples_live_on_the_verbs, with_examples
        examples_live_on_the_verbs(parser, "snapshot-store")
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name in ("inventory", "pack", "check", "hydrate"):
        command = verbs.add_parser(name)
        command.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        command.add_argument("--json", action="store_true")
        if examples is not None:
            with_examples(command, examples.get(name, ()))
        if name == "inventory":
            command.add_argument("--declared", action="store_true", help="inspect metadata without opening snapshots")
            command.add_argument("--summary", action="store_true", help="omit individual entries from JSON")
        if name == "pack":
            command.add_argument("--out", type=Path, default=Path(".scratch/next-snapshot-store/packs"))
            command.add_argument("--release", required=True)
            command.add_argument("--url-template", default=DEFAULT_URL)
            command.add_argument("--max-archive-bytes", type=int, default=transport.MAX_ARCHIVE_BYTES)
        if name == "check":
            command.add_argument("--local", action="store_true", help="verify any existing originals/cache bytes")
            command.add_argument("--require-local", action="store_true", help="require every snapshot locally")
            command.add_argument("--archives", action="store_true", help="verify complete archive membership and bytes")
        if name in {"check", "hydrate"}:
            command.add_argument("--archive-dir", type=Path)
        if name == "hydrate":
            command.add_argument("paths", nargs="*")
            command.add_argument("--all", action="store_true")
            command.add_argument("--fetch", action="store_true", help="explicitly allow release downloads")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.verb == "inventory":
            entries = load_index(root)["artifacts"] if args.declared else _inventory(root)
            result = {"status": "ok", "snapshots": len(entries), "bytes": sum(e["bytes"] for e in entries)}
            if not args.summary:
                result["entries"] = entries
        elif args.verb == "pack":
            out = args.out if args.out.is_absolute() else root / args.out
            result = _summary(pack(root, out, release=args.release, url_template=args.url_template,
                                   max_archive_bytes=args.max_archive_bytes))
        else:
            if not transport._path(root, INDEX_PATH).is_file():
                raise SnapshotStoreError(f"missing frozen input delivery index: {INDEX_PATH}")
            data = load_index(root)
            result = _summary(data)
            if args.verb == "check":
                errors = validate_index(root, local_bytes=args.local or args.require_local)
                if errors:
                    raise SnapshotStoreError("; ".join(errors))
                if args.require_local:
                    for entry in data["artifacts"]:
                        resolve(root, entry["path"])
                if args.archives:
                    directory = args.archive_dir or root / ".scratch/next-snapshot-store/packs"
                    for archive in data["archives"]:
                        path = transport._archive_path(root, archive, directory, False)
                        transport._read_archive(path, [e for e in data["artifacts"] if e["archive"] == archive["id"]])
            else:
                if args.all == bool(args.paths):
                    raise SnapshotStoreError("select explicit snapshot paths or --all")
                paths = [e["path"] for e in data["artifacts"]] if args.all else args.paths
                result["resolved"] = len(hydrate(root, paths, archive_dir=args.archive_dir, fetch=args.fetch))
        print(json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else
              f"snapshot-store: {result['snapshots']} snapshots, {result['bytes']} bytes; {result.get('archives', 0)} archives; ok")
        return 0
    except (SnapshotStoreError, OSError, subprocess.CalledProcessError) as error:
        if args.json:
            print(json.dumps({"status": "error", "error": str(error)}, sort_keys=True))
        else:
            print(f"snapshot-store: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
