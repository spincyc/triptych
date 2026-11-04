"""Symlink-free, race-checked file reads, hashes and replacements.

Every path is opened through a chain of directory descriptors with
``O_NOFOLLOW`` and rechecked against the inode it started from, so a symlink,
special file or ancestor exchanged during an operation fails instead of
redirecting it. The browser-product store uses these helpers for its inputs,
cache entries and descriptor. ``_external_identities`` cross-checks exact
binary delivery metadata without hydrating evidence bytes.
"""
from __future__ import annotations

import hashlib
from contextlib import contextmanager
import json
import os
from pathlib import Path, PurePosixPath
import secrets
import stat
import tomllib

import _artifact_store


class SafeFileError(ValueError):
    """A path is missing, unsafe, or changed during the operation."""


def _same_inode(left, right) -> bool:
    return (left.st_dev, left.st_ino) == (right.st_dev, right.st_ino)


def _require_entry(parent: int, name: str, descriptor: int) -> None:
    entry = os.stat(name, dir_fd=parent, follow_symlinks=False)
    if not _same_inode(entry, os.fstat(descriptor)):
        raise SafeFileError(f"input path changed during operation: {name}")


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
                raise SafeFileError(f"input directory changed while opening: {relative}")
        yield descriptors[-1], parts[-1]
    finally:
        try:
            if not _same_inode(os.stat(root, follow_symlinks=False), os.fstat(descriptors[0])):
                raise SafeFileError("repository path changed during operation")
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
                raise SafeFileError(f"input directory changed while opening: {relative}")
            yield directory
        finally:
            try:
                _require_entry(parent, name, directory)
            finally:
                os.close(directory)


def read_file(root: Path, relative: str) -> bytes:
    """Read a regular file through symlink-free directory descriptors."""
    try:
        with _open_parent(root, relative) as (parent, name):
            before = os.stat(name, dir_fd=parent, follow_symlinks=False)
            descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            try:
                opened = os.fstat(descriptor)
                if not stat.S_ISREG(opened.st_mode) or not _same_inode(before, opened):
                    raise SafeFileError(f"input must be an unchanged regular file: {relative}")
                blocks = []
                while block := os.read(descriptor, 1024 * 1024):
                    blocks.append(block)
                after = os.fstat(descriptor)
                _require_entry(parent, name, descriptor)
                if _file_stamp(opened) != _file_stamp(after):
                    raise SafeFileError(f"input changed while reading: {relative}")
                return b"".join(blocks)
            finally:
                os.close(descriptor)
    except OSError as error:
        raise SafeFileError(f"missing or unsafe input: {relative}: {error.strerror}") from error


def atomic_write(root: Path, relative: str, body: bytes, *, scratch: Path) -> None:
    """Replace a regular single-link file; transient bytes stay under ``scratch``."""
    scratch.mkdir(parents=True, exist_ok=True)
    aside = "replace-" + secrets.token_hex(12)
    try:
        with _open_directory(root, scratch.relative_to(root).as_posix()) as scratch_fd:
            try:
                with _open_parent(root, relative) as (parent, name):
                    try:
                        existing = os.stat(name, dir_fd=parent, follow_symlinks=False)
                    except FileNotFoundError:
                        existing = None
                    if existing is not None and (not stat.S_ISREG(existing.st_mode) or existing.st_nlink != 1):
                        raise SafeFileError(f"target must be a regular file with one link: {relative}")
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
        raise SafeFileError(f"cannot safely replace: {relative}: {error.strerror}") from error


def _relative(value: str) -> str:
    if (not isinstance(value, str) or not value or "\\" in value or "\0" in value
            or PurePosixPath(value).is_absolute()
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        raise SafeFileError(f"unsafe relative path: {value!r}")
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
            raise SafeFileError(f"input must be a regular file: {relative}")
        digest = hashlib.sha256()
        while block := os.read(descriptor, 1024 * 1024):
            digest.update(block)
        after = os.fstat(descriptor)
        _require_entry(parent, name, descriptor)
        if _file_stamp(before) != _file_stamp(after):
            raise SafeFileError(f"input changed while hashing: {relative}")
        return digest.hexdigest(), after.st_size
    except OSError as error:
        raise SafeFileError(f"missing or unsafe input: {relative}: {error.strerror}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


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
        raise SafeFileError(f"invalid artifact delivery metadata: {error}") from error
    result = {}
    for entry in entries:
        name = entry["path"]
        if not name.startswith("src/sources/works/"):
            continue
        manifest_name = str(PurePosixPath(name).parent / "artifact.toml")
        # A git-history reference may name a JSON inventory; others are binary.
        binary = PurePosixPath(name).suffix.lower() in _artifact_store.BINARY_SUFFIXES
        if ((not binary and "git_commit" not in entry)
                or entry["kind"] != "source-evidence" or manifest_name not in names):
            raise SafeFileError(f"external source requires its exact binary artifact manifest: {name}")
        try:
            data = tomllib.loads(read_file(root, manifest_name).decode("utf-8"))
        except (OSError, UnicodeError, ValueError) as error:
            raise SafeFileError(f"cannot read external artifact manifest: {manifest_name}") from error
        if (data.get("record_type") != "artifact" or data.get("storage") != "tracked"
                or data.get("indexable") is True
                or str(data.get("media_type", "")).startswith("text/")
                or any(data.get(field) != entry[key] for field, key in (
                    ("path", "path"), ("sha256", "sha256"), ("byte_size", "bytes"),
                    ("media_type", "media_type")))
                or type(data.get("byte_size")) is not int):
            raise SafeFileError(f"external artifact identity differs from delivery metadata: {name}")
        # These identities are themselves bound by both files' content hashes.
        result[name] = {"manifest": manifest_name, "sha256": entry["sha256"], "bytes": entry["bytes"]}
    return result


