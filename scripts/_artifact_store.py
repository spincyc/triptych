"""Exact historical binary delivery, without changing source-record identity.

The tracked sidecar describes immutable bytes and bounded release archives.
Validation and resolution never use the network unless ``fetch=True`` is
explicit. Run this module directly to bootstrap a checkout from an offline pack.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
import mimetypes
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from typing import Any
from urllib.parse import urlsplit
from urllib.request import urlopen

INDEX_PATH = "src/sources/artifact-delivery.json"
SCHEMA = "triptych-artifact-delivery/v1"
MAX_ARCHIVE_BYTES = 512_000_000
BINARY_SUFFIXES = frozenset({
    ".pdf", ".djvu", ".zip", ".gz", ".xz", ".epub", ".tar", ".jpg",
    ".jpeg", ".png", ".webp", ".tif", ".tiff", ".jp2", ".iff", ".traineddata",
})
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_SLUG = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._-]*\Z")
_CHUNK = 1024 * 1024


class ArtifactStoreError(ValueError):
    """Delivery metadata or retained bytes failed an integrity check."""


def _relative(value: Any) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ArtifactStoreError(f"unsafe relative artifact path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in {"", ".", ".."} for p in value.split("/")):
        raise ArtifactStoreError(f"unsafe relative artifact path: {value!r}")
    if str(path) != value or ":" in value.split("/")[0]:
        raise ArtifactStoreError(f"noncanonical relative artifact path: {value!r}")
    return value


def _path(root: Path, relative: str) -> Path:
    """Reject traversal and symlinks, including symlinked cache parents."""
    relative = _relative(relative)
    root = root.resolve()
    current = root
    for part in relative.split("/"):
        current = current / part
        if current.is_symlink():
            raise ArtifactStoreError(f"artifact paths may not traverse symlinks: {relative}")
    return current


def _digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(_CHUNK):
            result.update(chunk)
    return result.hexdigest()


def _verify(path: Path, entry: dict[str, Any]) -> Path:
    if path.is_symlink() or not path.is_file():
        raise FileNotFoundError(f"artifact is unavailable locally: {entry.get('path', entry.get('name'))}")
    if path.stat().st_size != entry["bytes"] or _digest(path) != entry["sha256"]:
        raise ArtifactStoreError(f"artifact hash or size mismatch: {entry.get('path', entry.get('name'))}")
    return path


def _validate(data: Any) -> None:
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise ArtifactStoreError(f"expected {SCHEMA}")
    if set(data) - {"schema", "snapshot", "archives", "artifacts"}:
        raise ArtifactStoreError("unknown artifact delivery index fields")
    if not isinstance(data.get("archives"), list) or not isinstance(data.get("artifacts"), list):
        raise ArtifactStoreError("delivery archives and artifacts must be arrays")
    snapshot = data.get("snapshot")
    if snapshot is not None and (not isinstance(snapshot, str) or not re.fullmatch(r"[0-9a-f]{40,64}", snapshot)):
        raise ArtifactStoreError("snapshot must be a full Git object ID")
    archives: dict[str, dict[str, Any]] = {}
    names: set[str] = set()
    for archive in data["archives"]:
        if not isinstance(archive, dict) or set(archive) != {"id", "name", "sha256", "bytes", "urls"}:
            raise ArtifactStoreError("invalid archive fields")
        if not isinstance(archive["sha256"], str) or not _DIGEST.fullmatch(archive["sha256"]):
            raise ArtifactStoreError("invalid archive SHA-256")
        if archive["id"] != archive["sha256"] or archive["id"] in archives:
            raise ArtifactStoreError("archive IDs must be unique exact SHA-256 values")
        name = _relative(archive["name"])
        if "/" in name or not name.endswith(".tar") or name in names:
            raise ArtifactStoreError("archive names must be unique .tar basenames")
        if type(archive["bytes"]) is not int or not 0 < archive["bytes"] <= MAX_ARCHIVE_BYTES:
            raise ArtifactStoreError("archive size must be positive and at most 512000000 bytes")
        if not isinstance(archive["urls"], list) or not archive["urls"]:
            raise ArtifactStoreError("archive requires at least one public delivery URL")
        for url in archive["urls"]:
            parsed = urlsplit(url) if isinstance(url, str) else None
            if parsed is None or parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.fragment:
                raise ArtifactStoreError("archive delivery URLs must be public HTTPS URLs")
        names.add(name)
        archives[archive["id"]] = archive
    paths: set[str] = set()
    members: set[tuple[str, str]] = set()
    referenced: set[str] = set()
    for entry in data["artifacts"]:
        required = {"path", "sha256", "bytes", "kind", "media_type", "archive", "member"}
        if not isinstance(entry, dict) or not required <= entry.keys() or entry.keys() - required - {"origin_url"}:
            raise ArtifactStoreError("invalid artifact delivery entry fields")
        path, member = _relative(entry["path"]), _relative(entry["member"])
        if path in paths or member != path:
            raise ArtifactStoreError("artifact paths must be unique and equal their archive member names")
        if not isinstance(entry["sha256"], str) or not _DIGEST.fullmatch(entry["sha256"]):
            raise ArtifactStoreError(f"invalid artifact SHA-256: {path}")
        if type(entry["bytes"]) is not int or entry["bytes"] < 0:
            raise ArtifactStoreError(f"invalid artifact byte size: {path}")
        if entry["kind"] not in {"source-evidence", "historical-publication", "historical-binary"}:
            raise ArtifactStoreError(f"invalid artifact kind: {path}")
        if not isinstance(entry["media_type"], str) or not re.fullmatch(r"[\w.+-]+/[\w.+-]+", entry["media_type"]):
            raise ArtifactStoreError(f"invalid artifact media type: {path}")
        if entry["archive"] not in archives:
            raise ArtifactStoreError(f"artifact names an unknown archive: {path}")
        if entry["bytes"] > archives[entry["archive"]]["bytes"]:
            raise ArtifactStoreError(f"artifact exceeds its archive: {path}")
        key = (entry["archive"], member)
        if key in members:
            raise ArtifactStoreError(f"duplicate archive member: {path}")
        if "origin_url" in entry:
            origin = entry["origin_url"]
            parsed = urlsplit(origin) if isinstance(origin, str) else None
            if parsed is None or parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username or parsed.password:
                raise ArtifactStoreError(f"invalid public origin URL: {path}")
        paths.add(path)
        members.add(key)
        referenced.add(entry["archive"])
    if referenced != archives.keys():
        raise ArtifactStoreError("delivery index contains an archive without members")


def _unique_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ArtifactStoreError(f"duplicate delivery JSON key: {key}")
        result[key] = value
    return result


@lru_cache(maxsize=8)
def _load_index(path: Path, mtime: int, ctime: int, size: int) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_keys)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ArtifactStoreError(f"cannot read {INDEX_PATH}: {error}") from error
    try:
        _validate(data)
    except (TypeError, KeyError, ValueError) as error:
        if isinstance(error, ArtifactStoreError):
            raise
        raise ArtifactStoreError(f"invalid delivery field type: {error}") from error
    return data


def load_index(root: Path | str) -> dict[str, Any]:
    """Load the strict sidecar; treat its returned records as read-only.

    Parsed data is cached against filesystem change stamps so graph consumers
    do not repeatedly parse thousands of entries. The sidecar is atomically
    replaced by pack, and an edited sidecar is validated again.
    """
    path = _path(Path(root), INDEX_PATH)
    if not path.exists():
        return {"schema": SCHEMA, "archives": [], "artifacts": []}
    stat = path.stat()
    return _load_index(path, stat.st_mtime_ns, stat.st_ctime_ns, stat.st_size)


def delivery_entries(root: Path | str) -> list[dict[str, Any]]:
    return load_index(root)["artifacts"]


def known_external(root: Path | str, repo_relative_path: str | Path) -> dict[str, Any] | None:
    path = _relative(str(repo_relative_path))
    return next((entry for entry in delivery_entries(root) if entry["path"] == path), None)


def cache_path(root: Path | str, entry: dict[str, Any]) -> Path:
    return _path(Path(root), f".scratch/artifact-cache/{entry['sha256']}/{PurePosixPath(entry['path']).name}")


def validate_index(root: Path | str, local_bytes: bool = False) -> list[str]:
    """Return diagnostics; local byte checks never require absent payloads."""
    try:
        data = load_index(root)
        if local_bytes:
            for entry in data["artifacts"]:
                original = _path(Path(root), entry["path"])
                cached = cache_path(root, entry)
                for path in (original, cached):
                    if path.exists():
                        _verify(path, entry)
        return []
    except (ArtifactStoreError, OSError) as error:
        return [str(error)]


def resolve(root: Path | str, repo_relative_path: str | Path, fetch: bool = False) -> Path:
    """Return exact original/cache bytes; explicit fetch enables release access."""
    root = Path(root)
    relative = _relative(str(repo_relative_path))
    original = _path(root, relative)
    entry = known_external(root, relative)
    if original.is_file():
        return _verify(original, entry) if entry else original
    if entry is None:
        raise FileNotFoundError(f"no local artifact or delivery entry: {relative}")
    cached = cache_path(root, entry)
    if cached.exists():
        return _verify(cached, entry)
    if fetch:
        hydrate(root, [relative], fetch=True)
        return _verify(cached, entry)
    raise FileNotFoundError(f"external artifact is not cached: {relative}; run tools/artifact-store hydrate {relative} --fetch, or use an offline --archive-dir")


def _archive_path(root: Path, archive: dict[str, Any], archive_dir: Path | None, fetch: bool) -> Path:
    if archive_dir is not None:
        candidate = archive_dir / archive["name"]
        if candidate.exists() or candidate.is_symlink():
            return _verify(candidate, archive)
    cached = _path(root, f".scratch/artifact-cache/archives/{archive['name']}")
    if cached.exists():
        return _verify(cached, archive)
    if not fetch:
        raise FileNotFoundError(f"archive is unavailable locally: {archive['name']}; supply --archive-dir or --fetch")
    cached.parent.mkdir(parents=True, exist_ok=True)
    errors = []
    for url in archive["urls"]:
        fd, temporary = tempfile.mkstemp(prefix=".download-", dir=cached.parent)
        try:
            with os.fdopen(fd, "wb") as target, urlopen(url, timeout=60) as source:
                remaining = archive["bytes"]
                while chunk := source.read(min(_CHUNK, remaining + 1)):
                    remaining -= len(chunk)
                    if remaining < 0:
                        raise ArtifactStoreError("download exceeds recorded archive size")
                    target.write(chunk)
            _verify(Path(temporary), archive)
            os.replace(temporary, cached)
            return cached
        except (OSError, ValueError) as error:
            errors.append(f"{url}: {error}")
        finally:
            Path(temporary).unlink(missing_ok=True)
    raise ArtifactStoreError("all exact archive delivery routes failed: " + "; ".join(errors))


def _read_archive(path: Path, expected: list[dict[str, Any]], root: Path | None = None,
                  selected: set[str] | None = None) -> int:
    """Read regular, registered members only; never call tarfile.extract()."""
    entries = {entry["member"]: entry for entry in expected}
    seen: set[str] = set()
    hydrated = 0
    try:
        with tarfile.open(path, mode="r:") as archive:
            for member in archive:
                name = _relative(member.name)
                if name not in entries or name in seen or not member.isreg() or member.linkname:
                    raise ArtifactStoreError(f"unregistered, duplicate, or nonregular archive member: {name}")
                entry = entries[name]
                if member.size != entry["bytes"]:
                    raise ArtifactStoreError(f"archive member size mismatch: {name}")
                seen.add(name)
                source = archive.extractfile(member)
                if source is None:
                    raise ArtifactStoreError(f"archive member is unreadable: {name}")
                target = cache_path(root, entry) if root is not None and selected is not None and name in selected else None
                temporary = None
                output = None
                try:
                    if target is not None:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        fd, temporary = tempfile.mkstemp(prefix=".hydrate-", dir=target.parent)
                        output = os.fdopen(fd, "wb")
                    digest = hashlib.sha256()
                    count = 0
                    with source:
                        while chunk := source.read(_CHUNK):
                            digest.update(chunk)
                            count += len(chunk)
                            if output is not None:
                                output.write(chunk)
                    if output is not None:
                        output.close()
                    if count != entry["bytes"] or digest.hexdigest() != entry["sha256"]:
                        raise ArtifactStoreError(f"archive member hash mismatch: {name}")
                    if target is not None:
                        os.chmod(temporary, 0o444)
                        os.replace(temporary, target)
                        hydrated += 1
                finally:
                    if output is not None:
                        output.close()
                    if temporary is not None:
                        Path(temporary).unlink(missing_ok=True)
    except (tarfile.TarError, EOFError) as error:
        raise ArtifactStoreError(f"invalid artifact archive: {path.name}: {error}") from error
    if seen != entries.keys():
        raise ArtifactStoreError(f"archive is missing registered members: {sorted(entries.keys() - seen)[:3]}")
    return hydrated


def hydrate(root: Path | str, paths: list[str], *, archive_dir: Path | str | None = None,
            fetch: bool = False) -> list[Path]:
    root = Path(root).resolve()
    data = load_index(root)
    wanted = {_relative(path) for path in paths}
    entries = {entry["path"]: entry for entry in data["artifacts"]}
    if wanted - entries.keys():
        raise ArtifactStoreError(f"paths not declared in the delivery index: {sorted(wanted - entries.keys())[:3]}")
    missing = set()
    for path in wanted:
        try:
            resolve(root, path)
        except FileNotFoundError:
            missing.add(path)
    for archive in data["archives"]:
        members = [entry for entry in data["artifacts"] if entry["archive"] == archive["id"]]
        if missing.intersection(entry["path"] for entry in members):
            local = _archive_path(root, archive, Path(archive_dir) if archive_dir else None, fetch)
            _read_archive(local, members, root, missing)
    return [resolve(root, path) for path in sorted(wanted)]


def _inventory(root: Path) -> list[dict[str, Any]]:
    result = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True, stdout=subprocess.PIPE)
    previous = {entry["path"]: entry for entry in delivery_entries(root)}
    paths = {p.decode("utf-8") for p in result.stdout.split(b"\0") if p}
    paths.update(previous)
    entries = []
    for relative in sorted(paths):
        suffix = PurePosixPath(relative).suffix.lower()
        source = relative.startswith("src/sources/works/")
        if relative not in previous and suffix != ".pdf" and not (source and suffix in BINARY_SUFFIXES):
            continue
        path = _path(root, relative)
        old = previous.get(relative)
        if not path.is_file() and old is None:
            raise ArtifactStoreError(f"cannot inventory missing tracked binary: {relative}")
        media_type = mimetypes.guess_type(relative)[0] or "application/octet-stream"
        kind = "source-evidence" if source else "historical-publication" if relative.startswith("pdf/") else "historical-binary"
        if path.is_file():
            if old is not None:
                _verify(path, old)
            entry = {"path": relative, "sha256": _digest(path), "bytes": path.stat().st_size,
                     "kind": kind, "media_type": media_type}
        else:
            # An ordinary clone keeps every declaration even before hydration.
            # Repacking later resolves each exact object, never erases entries.
            entry = {key: value for key, value in old.items() if key not in {"archive", "member"}}
        if source:
            manifest = path.parent / "artifact.toml"
            if not manifest.is_file():
                raise ArtifactStoreError(f"source binary has no artifact manifest: {relative}")
            metadata = tomllib.loads(manifest.read_text(encoding="utf-8"))
            if metadata.get("path") != relative or metadata.get("sha256") != entry["sha256"] or metadata.get("byte_size") != entry["bytes"]:
                raise ArtifactStoreError(f"source binary disagrees with its artifact manifest: {relative}")
            entry["media_type"] = metadata["media_type"]
            if metadata.get("source_url"):
                entry["origin_url"] = metadata["source_url"]
        entries.append(entry)
    return entries


def _tar_info(entry: dict[str, Any]) -> tarfile.TarInfo:
    info = tarfile.TarInfo(entry["path"])
    info.size = entry["bytes"]
    info.mode = 0o444
    info.uid = info.gid = info.mtime = 0
    info.uname = info.gname = ""
    return info


def _tar_size(entries: list[dict[str, Any]]) -> int:
    size = sum(len(_tar_info(entry).tobuf(format=tarfile.PAX_FORMAT)) + ((entry["bytes"] + 511) // 512) * 512 for entry in entries)
    return ((size + 1024 + tarfile.RECORDSIZE - 1) // tarfile.RECORDSIZE) * tarfile.RECORDSIZE


def _json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".index-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def pack(root: Path | str, out: Path | str, *, release: str,
         url_template: str = "https://github.com/spincyc/triptych-artifacts/releases/download/{release}/{archive}",
         max_archive_bytes: int = MAX_ARCHIVE_BYTES) -> dict[str, Any]:
    """Preserve tracked binary evidence before publishing the sidecar atomically."""
    root = Path(root).resolve()
    out = Path(out).resolve()
    if not _SLUG.fullmatch(release) or not 10240 <= max_archive_bytes <= MAX_ARCHIVE_BYTES:
        raise ArtifactStoreError("release must be a safe slug and archive limit between 10240 and 512000000")
    entries = _inventory(root)
    groups: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_size = 0
    for entry in entries:
        if _tar_size([entry]) > max_archive_bytes:
            raise ArtifactStoreError(f"artifact cannot fit the requested archive bound: {entry['path']}")
        entry_size = len(_tar_info(entry).tobuf(format=tarfile.PAX_FORMAT)) + ((entry["bytes"] + 511) // 512) * 512
        projected_size = ((current_size + entry_size + 1024 + tarfile.RECORDSIZE - 1) // tarfile.RECORDSIZE) * tarfile.RECORDSIZE
        if current and projected_size > max_archive_bytes:
            groups.append(current)
            current = []
            current_size = 0
        current.append(entry)
        current_size += entry_size
    if current:
        groups.append(current)
    out.mkdir(parents=True, exist_ok=True)
    archives = []
    packed = []
    for ordinal, group in enumerate(groups, 1):
        fd, temporary = tempfile.mkstemp(prefix=".pack-", suffix=".tar", dir=out)
        os.close(fd)
        temporary = Path(temporary)
        try:
            with tarfile.open(temporary, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for entry in group:
                    with resolve(root, entry["path"]).open("rb") as source:
                        archive.addfile(_tar_info(entry), source)
            digest = _digest(temporary)
            name = f"triptych-binaries-{ordinal:04d}-{digest[:16]}.tar"
            metadata = {"id": digest, "name": name, "sha256": digest, "bytes": temporary.stat().st_size,
                        "urls": [url_template.format(release=release, archive=name)]}
            if metadata["bytes"] > max_archive_bytes:
                raise ArtifactStoreError("packed archive exceeded its size bound")
            members = [dict(entry, archive=digest, member=entry["path"]) for entry in group]
            _read_archive(temporary, members)
            os.replace(temporary, out / name)
            archives.append(metadata)
            packed.extend(members)
        finally:
            temporary.unlink(missing_ok=True)
    snapshot = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    data = {"schema": SCHEMA, "snapshot": snapshot, "archives": archives, "artifacts": packed}
    _validate(data)
    _json(_path(root, INDEX_PATH), data)
    _json(out / "artifact-delivery.json", data)
    bootstrap = out / "artifact-store.py"
    if Path(__file__).resolve() != bootstrap:
        shutil.copyfile(__file__, bootstrap)
    (out / "README.txt").write_text(
        "Triptych exact binary evidence offline pack\n\n"
        "Keep this entire directory together with a Triptych checkout. Archives are\n"
        "bounded, deterministic uncompressed tar files; do not extract them manually.\n"
        "The matching tracked index is src/sources/artifact-delivery.json.\n\n"
        "Verify every member (no network):\n"
        "  python3 artifact-store.py check --root /path/to/checkout --archives --archive-dir .\n"
        "Hydrate every missing payload into the checkout's ignored cache (no network):\n"
        "  python3 artifact-store.py hydrate --root /path/to/checkout --all --archive-dir .\n"
        "Then tools/source-library validate --full-evidence checks exact source evidence.\n"
        "Python 3.11 or newer is required. Existing source manifests keep their original\n"
        "paths, hashes, rights, and fingerprints. A hydrated cache is disposable; retain\n"
        "this offline pack separately from the checkout. No archive upload is implied.\n",
        encoding="utf-8")
    sums = [(item["name"], item["sha256"]) for item in archives]
    sums.extend((name, _digest(out / name)) for name in ("artifact-delivery.json", "artifact-store.py", "README.txt"))
    (out / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sums), encoding="utf-8")
    return data


def _summary(data: dict[str, Any]) -> dict[str, Any]:
    return {"status": "ok", "artifacts": len(data["artifacts"]), "bytes": sum(entry["bytes"] for entry in data["artifacts"]),
            "archives": len(data["archives"]), "archive_bytes": sum(entry["bytes"] for entry in data["archives"]),
            "kinds": dict(sorted(Counter(entry["kind"] for entry in data["artifacts"]).items()))}


def main(argv: list[str] | None = None, *, examples: dict | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    if examples is not None:
        from _tooling import examples_live_on_the_verbs, with_examples
        examples_live_on_the_verbs(parser, "artifact-store")
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name in ("inventory", "pack", "check", "hydrate"):
        command = verbs.add_parser(name)
        command.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        command.add_argument("--json", action="store_true", help="print machine-readable summary")
        if examples is not None:
            with_examples(command, examples.get(name, ()))
        if name == "inventory":
            command.add_argument("--declared", action="store_true", help="report indexed declarations without reading payloads")
            command.add_argument("--summary", action="store_true", help="omit individual entries from JSON output")
        if name == "pack":
            command.add_argument("--out", type=Path, default=Path(".scratch/artifact-store"))
            command.add_argument("--release", required=True)
            command.add_argument("--url-template", default="https://github.com/spincyc/triptych-artifacts/releases/download/{release}/{archive}")
            command.add_argument("--max-archive-bytes", type=int, default=MAX_ARCHIVE_BYTES)
        if name == "check":
            command.add_argument("--local", action="store_true", help="verify any existing original/cache bytes")
            command.add_argument("--require-local", action="store_true", help="require every indexed payload locally")
            command.add_argument("--archives", action="store_true", help="verify every archive and member")
        if name in {"check", "hydrate"}:
            command.add_argument("--archive-dir", type=Path, help="offline archive directory (relative to current directory)")
        if name == "hydrate":
            command.add_argument("paths", nargs="*")
            command.add_argument("--all", action="store_true")
            command.add_argument("--fetch", action="store_true", help="explicitly allow public release downloads")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.verb == "inventory":
            entries = delivery_entries(root) if args.declared else _inventory(root)
            result = {"status": "ok", "artifacts": len(entries), "bytes": sum(entry["bytes"] for entry in entries),
                      "kinds": dict(sorted(Counter(entry["kind"] for entry in entries).items())), "entries": entries}
            if args.summary:
                del result["entries"]
        elif args.verb == "pack":
            out = args.out if args.out.is_absolute() else root / args.out
            result = _summary(pack(root, out, release=args.release, url_template=args.url_template, max_archive_bytes=args.max_archive_bytes))
        else:
            if not _path(root, INDEX_PATH).is_file():
                raise ArtifactStoreError(f"missing delivery index: {INDEX_PATH}")
            data = load_index(root)
            result = _summary(data)
            if args.verb == "check":
                errors = validate_index(root, local_bytes=args.local or args.require_local)
                if errors:
                    raise ArtifactStoreError("; ".join(errors))
                if args.require_local:
                    for entry in data["artifacts"]:
                        resolve(root, entry["path"])
                if args.archives:
                    archive_dir = args.archive_dir or root / ".scratch/artifact-store"
                    for archive in data["archives"]:
                        local = _archive_path(root, archive, archive_dir, False)
                        _read_archive(local, [entry for entry in data["artifacts"] if entry["archive"] == archive["id"]])
            else:
                if args.all == bool(args.paths):
                    raise ArtifactStoreError("select explicit paths or --all")
                paths = [entry["path"] for entry in data["artifacts"]] if args.all else args.paths
                result["resolved"] = len(hydrate(root, paths, archive_dir=args.archive_dir, fetch=args.fetch))
        if args.json:
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        else:
            print(f"artifact-store: {result['artifacts']} artifacts, {result['bytes']} bytes; {result.get('archives', 0)} archives; ok")
        return 0
    except (ArtifactStoreError, OSError, subprocess.CalledProcessError) as error:
        if args.json:
            print(json.dumps({"status": "error", "error": str(error)}, sort_keys=True))
        else:
            print(f"artifact-store: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
