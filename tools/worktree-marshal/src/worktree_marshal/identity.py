"""Runtime identity records and read-only authentication policy."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class Repository:
    root: Path
    git_dir: Path
    common_git_dir: Path
    relative_cwd: Path
    linked_worktree: bool
    state_root: Path


@dataclass(frozen=True)
class LinkedWorktreeIdentity:
    worktree: Path
    git_file: Path
    git_dir: Path
    common_git_dir: Path


@dataclass(frozen=True)
class LauncherIdentity:
    """Authenticated identity of the in-process command entry point."""

    path: Path
    device: int
    inode: int


def authenticate_launcher(
    path: Path,
    *,
    os_error_type: Callable[[], type[BaseException]],
    error_type: Callable[[], type[BaseException]],
    regular_file_test: Callable[[], Callable[[int], bool]],
    access_check: Callable[[], Callable[[Path, int], bool]],
    executable_mode: Callable[[], int],
    identity_factory: Callable[
        [],
        Callable[..., LauncherIdentity],
    ],
) -> LauncherIdentity:
    """Authenticate the executable launcher path with lazy dependencies."""

    if not path.is_absolute():
        raise error_type()("the launcher entry point must be an absolute path")
    try:
        resolved = path.resolve(strict=True)
        metadata = resolved.stat()
    except os_error_type() as exc:
        raise error_type()("cannot authenticate the launcher entry point") from exc
    if (
        not regular_file_test()(metadata.st_mode)
        or not access_check()(resolved, executable_mode())
    ):
        raise error_type()("the launcher entry point is not a usable executable")
    return identity_factory()(
        path=resolved,
        device=metadata.st_dev,
        inode=metadata.st_ino,
    )


def exact_single_line(
    path: Path,
    *,
    label: str,
    file_reader: Callable[[], Callable[..., bytes]],
    decode_error_type: Callable[[], type[BaseException]],
    error_type: Callable[[], type[BaseException]],
) -> str:
    """Read and validate one exact Git-administration path line."""

    data = file_reader()(path, label=label)
    if (
        not data.endswith(b"\n")
        or data.count(b"\n") != 1
        or b"\r" in data
    ):
        raise error_type()(f"{label} does not contain one exact line")
    try:
        value = data[:-1].decode("utf-8")
    except decode_error_type() as exc:
        raise error_type()(f"{label} is not valid UTF-8") from exc
    if not value or "\0" in value:
        raise error_type()(f"{label} has an invalid path")
    return value
