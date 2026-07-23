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
