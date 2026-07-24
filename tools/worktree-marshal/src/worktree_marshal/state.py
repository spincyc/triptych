"""I/O-free run identity and state-location policy."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Protocol


class StateProfile(Protocol):
    state_environment: str
    override_state_suffix: Sequence[str]
    default_state_parts: Sequence[str]


RUN_ID_RE = re.compile(r"^[0-9]{8}t[0-9]{6}z-[0-9a-f]{12}$")


def private_directory(
    path: Path,
    *,
    os_error_type: Callable[[], type[BaseException]],
    error_type: Callable[[], type[BaseException]],
    directory_test: Callable[[], Callable[[int], bool]],
    flag_lookup: Callable[[], Callable[[str, int], int]],
    read_only_flag: Callable[[], int],
    file_open: Callable[[], Callable[[Path, int], int]],
    file_stat: Callable[[], Callable[[int], object]],
    same_stat: Callable[[], Callable[[object, object], bool]],
    file_chmod: Callable[[], Callable[[int, int], None]],
    file_close: Callable[[], Callable[[int], None]],
) -> None:
    """Create and descriptor-authenticate one private state directory."""

    try:
        path.mkdir(mode=0o700, parents=True, exist_ok=True)
        metadata = path.lstat()
    except os_error_type() as exc:
        raise error_type()(
            "cannot create or inspect a private launcher directory"
        ) from exc
    if not directory_test()(metadata.st_mode):
        raise error_type()("a private launcher path is not a real directory")
    directory_flag = flag_lookup()("O_DIRECTORY", 0)
    nofollow_flag = flag_lookup()("O_NOFOLLOW", 0)
    if not directory_flag or not nofollow_flag:
        raise error_type()(
            "safe private launcher directory setup is unavailable"
        )
    try:
        descriptor = file_open()(
            path,
            read_only_flag()
            | directory_flag
            | nofollow_flag
            | flag_lookup()("O_CLOEXEC", 0),
        )
    except os_error_type() as exc:
        raise error_type()(
            "cannot open a private launcher directory safely"
        ) from exc
    try:
        opened = file_stat()(descriptor)
        if (
            not directory_test()(opened.st_mode)
            or not same_stat()(metadata, opened)
        ):
            raise error_type()(
                "a private launcher directory changed during setup"
            )
        file_chmod()(descriptor, 0o700)
    except os_error_type() as exc:
        raise error_type()(
            "cannot authenticate a private launcher directory"
        ) from exc
    finally:
        file_close()(descriptor)


def new_run_id(
    *,
    current_time: Callable[[], datetime],
    random_suffix: Callable[[], str],
) -> str:
    """Generate one run ID from explicit clock and entropy providers."""

    stamp = current_time().strftime("%Y%m%dt%H%M%Sz").lower()
    return f"{stamp}-{random_suffix()}"


def state_base(
    *,
    profile: StateProfile,
    environment: Callable[[], Mapping[str, str]],
    path_factory: Callable[[str], Path],
    home: Callable[[], Path],
    error_type: Callable[[], type[Exception]],
) -> Path:
    """Select the state base from explicit profile and environment providers."""

    override = environment().get(profile.state_environment)
    if override:
        candidate = path_factory(override)
        if not candidate.is_absolute():
            raise error_type()(
                f"{profile.state_environment} must be an absolute path"
            )
        return candidate.joinpath(*profile.override_state_suffix)

    xdg_state = environment().get("XDG_STATE_HOME")
    if xdg_state:
        candidate = path_factory(xdg_state)
        if not candidate.is_absolute():
            raise error_type()("XDG_STATE_HOME must be an absolute path")
        return candidate.joinpath(*profile.default_state_parts)
    return (home() / ".local" / "state").joinpath(
        *profile.default_state_parts
    )


def repository_slug(
    root: Path,
    *,
    substitute: Callable[[str, str, str], str],
) -> str:
    """Normalize a repository basename for its state-directory prefix."""

    slug = substitute(r"[^a-z0-9]+", "-", root.name.lower()).strip("-")
    return slug or "repository"


def repo_lock_path(state_root: Path) -> Path:
    return state_root / "repository.lock"


def run_lock_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.lock"


def manifest_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.json"
