"""Content proofs for projections, without loading the source graph.

The scope is a conservative superset of source-reader inputs, selected from
Git's tracked files and a physical walk independent of local ignore rules.
Both mechanical receipts are excluded
because neither is source authority. Changed membership is part of the proof.
Only an exact artifact manifest plus delivery entry can replace binary bytes;
ordinary missing inputs, unknown payloads and symlinks remain errors.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import stat
import subprocess
import sys
import tomllib
from typing import Any

import _artifact_store

RECEIPT_PATH = "src/sources/inventories/source-reader-projection-receipt-v1.json"
RECEIPT_SCHEMA = "triptych-source-reader-projection-receipt/v1"
MECHANICAL_RECEIPTS = frozenset({
    RECEIPT_PATH,
    "src/sources/inventories/act-history-projection-receipt-v1.json",
})
# Broad scopes deliberately include rights authorities and helper imports that
# are not reached by the generator's ordinary manifest traversal. Provider
# trees also participate in source-library's safety and binding validation.
INPUT_TREES = ("src/sources", "src/gpt", "src/claude", "scripts", "tools", "guidance", "workflows")
INPUT_FILES = (
    "AGENTS.md", "LICENSE", "THIRD_PARTY.md", "Makefile", "tmt.json",
    ".gitattributes", ".gitignore", "requirements-tools.txt", "requirements-public-alpha.txt",
    "src/web/browser/sources/reader-model.js",
)


class ReceiptError(ValueError):
    """A projection's content proof is missing, stale or incomplete."""


def _same_inode(left, right) -> bool:
    return (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino)


def _require_entry(parent: int, name: str, descriptor: int) -> None:
    entry = os.stat(name, dir_fd=parent, follow_symlinks=False)
    if not _same_inode(entry, os.fstat(descriptor)):
        raise ReceiptError(f"input path changed during operation: {name}")


@contextmanager
def _open_parent(root: Path, relative: str):
    parts = _relative(relative).split("/")
    descriptors = [os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)]
    try:
        for part in parts[:-1]:
            before = os.stat(part, dir_fd=descriptors[-1], follow_symlinks=False)
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptors[-1])
            descriptors.append(child)
            if not _same_inode(before, os.fstat(child)):
                raise ReceiptError(f"input directory changed while opening: {relative}")
        yield descriptors[-1], parts[-1]
    finally:
        try:
            if not _same_inode(os.stat(root, follow_symlinks=False), os.fstat(descriptors[0])):
                raise ReceiptError("repository path changed during operation")
            for index in range(len(descriptors) - 1):
                _require_entry(descriptors[index], parts[index], descriptors[index + 1])
        finally:
            for descriptor in reversed(descriptors):
                os.close(descriptor)


@contextmanager
def _open_directory(root: Path, relative: str):
    with _open_parent(root, relative) as (parent, name):
        before = os.stat(name, dir_fd=parent, follow_symlinks=False)
        directory = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
        try:
            if not _same_inode(before, os.fstat(directory)):
                raise ReceiptError(f"input directory changed while opening: {relative}")
            yield directory
        finally:
            try:
                _require_entry(parent, name, directory)
            finally:
                os.close(directory)


def read_file(root: Path, relative: str) -> bytes:
    """Read receipt data through symlink-free directory descriptors."""
    try:
        with _open_parent(root, relative) as (parent, name):
            before = os.stat(name, dir_fd=parent, follow_symlinks=False)
            descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            try:
                opened = os.fstat(descriptor)
                if not stat.S_ISREG(opened.st_mode) or not _same_inode(before, opened):
                    raise ReceiptError(f"input must be an unchanged regular file: {relative}")
                blocks = []
                while block := os.read(descriptor, 1024 * 1024):
                    blocks.append(block)
                after = os.fstat(descriptor)
                _require_entry(parent, name, descriptor)
                if _file_stamp(opened) != _file_stamp(after):
                    raise ReceiptError(f"input changed while reading: {relative}")
                return b"".join(blocks)
            finally:
                os.close(descriptor)
    except OSError as error:
        raise ReceiptError(f"missing or unsafe input: {relative}: {error.strerror}") from error


def atomic_write(root: Path, relative: str, body: bytes, *, scratch: Path | None = None) -> None:
    """Replace proof data safely; transient bytes remain under caller's scratch."""
    scratch = scratch or root / ".scratch/source-projection-receipt"
    scratch.mkdir(parents=True, exist_ok=True)
    aside = "receipt-" + secrets.token_hex(12)
    try:
        with _open_directory(root, scratch.relative_to(root).as_posix()) as scratch_fd:
            try:
                with _open_parent(root, relative) as (parent, name):
                    try:
                        existing = os.stat(name, dir_fd=parent, follow_symlinks=False)
                    except FileNotFoundError:
                        existing = None
                    if existing is not None and (not stat.S_ISREG(existing.st_mode) or existing.st_nlink != 1):
                        raise ReceiptError(f"receipt must be a regular file with one link: {relative}")
                    descriptor = os.open(aside, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                         0o644, dir_fd=scratch_fd)
                    with os.fdopen(descriptor, "wb") as stream:
                        stream.write(body)
                    os.replace(aside, name, src_dir_fd=scratch_fd, dst_dir_fd=parent)
            finally:
                try:
                    os.unlink(aside, dir_fd=scratch_fd)
                except FileNotFoundError:
                    pass
    except OSError as error:
        raise ReceiptError(f"cannot safely write receipt: {relative}: {error.strerror}") from error


def _relative(value: str) -> str:
    if (not isinstance(value, str) or not value or "\\" in value or "\0" in value
            or PurePosixPath(value).is_absolute()
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise ReceiptError(f"unsafe receipt path: {value!r}")
    return value


def _file_stamp(value) -> tuple:
    return value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns, value.st_ctime_ns


def _file_hash_at(parent: int, name: str, relative: str) -> tuple[str, int]:
    descriptor = None
    try:
        entry = os.stat(name, dir_fd=parent, follow_symlinks=False)
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or not _same_inode(entry, before):
            raise ReceiptError(f"input must be a regular file: {relative}")
        digest = hashlib.sha256()
        while block := os.read(descriptor, 1024 * 1024):
            digest.update(block)
        after = os.fstat(descriptor)
        _require_entry(parent, name, descriptor)
        if _file_stamp(before) != _file_stamp(after):
            raise ReceiptError(f"input changed while hashing: {relative}")
        return digest.hexdigest(), after.st_size
    except OSError as error:
        raise ReceiptError(f"missing or unsafe input: {relative}: {error.strerror}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _file_hash(root: Path, relative: str) -> tuple[str, int]:
    try:
        with _open_parent(root, relative) as (parent, name):
            return _file_hash_at(parent, name, relative)
    except OSError as error:
        raise ReceiptError(f"missing or unsafe input: {relative}: {error.strerror}") from error


def _json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _physical_paths(root: Path) -> set[str]:
    """Find present inputs and reject special files that Git silently omits."""
    names: set[str] = set()

    def walk(directory: int, prefix: str) -> None:
        before = os.fstat(directory)
        with os.scandir(directory) as entries:
            for entry in entries:
                name = prefix + entry.name
                original = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(original.st_mode):
                    child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=directory)
                    try:
                        if not _same_inode(original, os.fstat(child)):
                            raise ReceiptError(f"input directory changed while opening: {name}")
                        walk(child, name + "/")
                        _require_entry(directory, entry.name, child)
                    finally:
                        os.close(child)
                elif stat.S_ISREG(original.st_mode):
                    # Read-only hashing permits ordinary hard links: every path
                    # and its bytes are still bound. Receipt writes reject them.
                    names.add(_relative(name))
                else:
                    raise ReceiptError(f"unsafe governing input must be a regular file or directory: {name}")
        if _file_stamp(before) != _file_stamp(os.fstat(directory)):
            raise ReceiptError("governing input membership changed during filesystem preflight")

    try:
        for tree in INPUT_TREES:
            try:
                with _open_directory(root, tree) as directory:
                    walk(directory, tree + "/")
            except FileNotFoundError:
                # Missing tracked members are diagnosed by the subsequent hash
                # pass. Optional input scopes may be absent in a small fixture.
                continue
        for relative in INPUT_FILES:
            try:
                with _open_parent(root, relative) as (parent, name):
                    value = os.stat(name, dir_fd=parent, follow_symlinks=False)
                    if not stat.S_ISREG(value.st_mode):
                        raise ReceiptError(f"unsafe governing input must be a regular file: {relative}")
                    names.add(relative)
            except FileNotFoundError:
                continue
    except OSError as error:
        raise ReceiptError(f"cannot safely inspect governing input paths: {error.strerror}") from error
    return names


def _git_paths(root: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--",
             *INPUT_TREES, *INPUT_FILES],
            cwd=root, capture_output=True, check=True,
        )
        names = (set(result.stdout.decode("utf-8").split("\0")) - {""}) | _physical_paths(root)
    except (OSError, UnicodeError, subprocess.CalledProcessError) as error:
        raise ReceiptError("cannot enumerate the repository's governing inputs with git ls-files") from error
    return {
        _relative(name) for name in names
        if name not in MECHANICAL_RECEIPTS
        # Python's code cache is never a generator input. Do not apply this to
        # sources: an ignored file there still needs its ordinary schema owner.
        and not (name.startswith(("scripts/", "tools/"))
                 and "__pycache__" in PurePosixPath(name).parts
                 and PurePosixPath(name).suffix in {".pyc", ".pyo"})
    }


def _external_identities(root: Path, names: set[str]) -> dict[str, dict]:
    """Cross-check only delivery manifests, never materialize the source graph."""
    try:
        if _artifact_store.INDEX_PATH not in names:
            return {}
        delivery = json.loads(read_file(root, _artifact_store.INDEX_PATH),
                              object_pairs_hook=_artifact_store._unique_keys)
        _artifact_store._validate(delivery)
        entries = delivery["artifacts"]
    except (ValueError, OSError, KeyError, TypeError) as error:
        raise ReceiptError(f"invalid artifact delivery metadata: {error}") from error
    result = {}
    for entry in entries:
        name = entry["path"]
        if not name.startswith("src/sources/works/"):
            continue
        manifest_name = str(PurePosixPath(name).parent / "artifact.toml")
        if (PurePosixPath(name).suffix.lower() not in _artifact_store.BINARY_SUFFIXES
                or entry["kind"] != "source-evidence" or manifest_name not in names):
            raise ReceiptError(f"external source requires its exact binary artifact manifest: {name}")
        try:
            data = tomllib.loads(read_file(root, manifest_name).decode("utf-8"))
        except (OSError, UnicodeError, ValueError) as error:
            raise ReceiptError(f"cannot read external artifact manifest: {manifest_name}") from error
        if (data.get("record_type") != "artifact" or data.get("storage") != "tracked"
                or data.get("indexable") is True
                or str(data.get("media_type", "")).startswith("text/")
                or any(data.get(field) != entry[key] for field, key in (
                    ("path", "path"), ("sha256", "sha256"), ("byte_size", "bytes"),
                    ("media_type", "media_type")))
                or type(data.get("byte_size")) is not int):
            raise ReceiptError(f"external artifact identity differs from delivery metadata: {name}")
        # These identities are themselves bound by both files' content hashes.
        result[name] = {"manifest": manifest_name, "sha256": entry["sha256"], "bytes": entry["bytes"]}
    return result


def input_identity(root: Path) -> dict:
    """Hash complete governing membership and contents, with no graph or hydration."""
    root = root.resolve()
    names = _git_paths(root)
    external = _external_identities(root, names)
    names.update(external)
    digest = hashlib.sha256()
    membership = hashlib.sha256()
    for name in sorted(names):
        membership.update(_json_bytes(name) + b"\n")
        if name in external:
            identity = {"path": name, "external": external[name]}
        else:
            hashed, size = _file_hash(root, name)
            identity = {"path": name, "sha256": hashed, "bytes": size}
        digest.update(_json_bytes(identity) + b"\n")
    if names != _git_paths(root) | set(external):
        raise ReceiptError("governing input membership changed while hashing")
    return {"count": len(names), "path_set_sha256": membership.hexdigest(),
            "sha256": digest.hexdigest(), "external_count": len(external)}


def output_identity(root: Path, target: Path) -> dict:
    """Record every output and reject extra payloads and unsafe filesystem objects."""
    root = root.resolve()
    target = target if target.is_absolute() else root / target
    try:
        relative = target.relative_to(root).as_posix()
    except ValueError as error:
        raise ReceiptError("projection output must be beneath the repository") from error
    files = {}

    def walk(directory: int, prefix: str) -> None:
        before = os.fstat(directory)
        with os.scandir(directory) as entries:
            for entry in entries:
                name = prefix + entry.name
                mode = entry.stat(follow_symlinks=False).st_mode
                if stat.S_ISDIR(mode):
                    child = os.open(entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=directory)
                    try:
                        if not _same_inode(entry.stat(follow_symlinks=False), os.fstat(child)):
                            raise ReceiptError(f"projection directory changed while opening: {name}")
                        walk(child, name + "/")
                        _require_entry(directory, entry.name, child)
                    finally:
                        os.close(child)
                else:
                    if not stat.S_ISREG(mode) or PurePosixPath(name).suffix != ".json":
                        raise ReceiptError(f"unexpected or unsafe projection output: {relative}/{name}")
                    digest, _ = _file_hash_at(directory, entry.name, relative + "/" + name)
                    files[name] = digest
        if _file_stamp(before) != _file_stamp(os.fstat(directory)):
            raise ReceiptError("projection output membership changed while hashing")

    try:
        with _open_directory(root, relative) as directory:
            walk(directory, "")
    except OSError as error:
        raise ReceiptError(f"missing or unsafe projection output: {relative}: {error.strerror}") from error
    if not files:
        raise ReceiptError(f"projection has no outputs: {relative}")
    return {"count": len(files), "sha256": hashlib.sha256(_json_bytes(files)).hexdigest(),
            "files": files}


def check_receipt(root: Path, target: Path, projection_schema: str) -> dict:
    try:
        receipt = json.loads(read_file(root, RECEIPT_PATH), object_pairs_hook=_artifact_store._unique_keys)
    except (OSError, UnicodeError, ValueError) as error:
        raise ReceiptError(f"projection receipt is missing or invalid; run `source-reader structure --record-receipt`: {error}") from error
    if (not isinstance(receipt, dict)
            or set(receipt) != {"schema", "projection_schema", "proof", "editorial_approval", "inputs", "outputs", "counted"}
            or receipt.get("schema") != RECEIPT_SCHEMA
            or receipt.get("projection_schema") != projection_schema
            or receipt.get("proof") != "independent-full-structure-check"
            or receipt.get("editorial_approval") is not False):
        raise ReceiptError("projection receipt has an unsupported proof or schema")
    counted = receipt.get("counted")
    if (not isinstance(counted, dict)
            or set(counted) != {"works", "editions", "artifacts", "passages", "readable"}
            or any(type(value) is not int or value < 0 for value in counted.values())):
        raise ReceiptError("projection receipt has invalid mechanical counts")
    if receipt.get("inputs") != input_identity(root):
        raise ReceiptError("projection receipt inputs changed; run the full `source-reader structure --record-receipt`")
    if receipt.get("outputs") != output_identity(root, target):
        raise ReceiptError("projection receipt outputs changed or have missing/extra files; run the full `source-reader structure --record-receipt`")
    return receipt


def record_receipt(root: Path, target: Path, projection_schema: str) -> dict:
    """Prove tracked output by independent replay before recording any identity."""
    inputs = input_identity(root)
    outputs = output_identity(root, target)
    environment = {**os.environ, "TRIPTYCH_LIBRARY_CACHE": "0", "TRIPTYCH_CORPUS_CACHE": "0"}
    completed = subprocess.run(
        [sys.executable, "-B", "-X",
         "pycache_prefix=" + str(root / ".scratch/source-projection-receipt" / ("python-" + secrets.token_hex(16))),
         str(root / "tools/source-reader"), "structure", "--check", "--strict", "--json", "--out", str(target.parent.parent)],
        cwd=root, env=environment, capture_output=True, text=True, check=False,
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ReceiptError(f"full source projection check failed; receipt was not written: {detail}")
    try:
        replayed = json.loads(completed.stdout)
    except ValueError as error:
        raise ReceiptError("full source projection check returned invalid JSON; receipt was not written") from error
    if replayed.get("status") != "ok" or replayed.get("files") != outputs["count"]:
        raise ReceiptError("full source projection check did not prove the complete output set")
    if inputs != input_identity(root) or outputs != output_identity(root, target):
        raise ReceiptError("projection inputs or outputs changed during replay; receipt was not written")
    counted = {key: replayed[key] for key in ("works", "editions", "artifacts", "passages", "readable")}
    receipt = {"schema": RECEIPT_SCHEMA, "projection_schema": projection_schema,
               "proof": "independent-full-structure-check", "editorial_approval": False,
               "inputs": inputs, "outputs": outputs, "counted": counted}
    atomic_write(root, RECEIPT_PATH,
                 (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode("utf-8"))
    return receipt
