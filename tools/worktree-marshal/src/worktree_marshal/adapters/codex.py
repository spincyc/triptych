"""Codex executable candidate selection.

This module owns read-only selection and pre-launch validation for the Codex
adapter. Argument normalization, environment construction, sandbox policy,
process creation, and lifecycle decisions remain in the lifecycle engine until
their own parity seams are protected.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Protocol


class CodexProfile(Protocol):
    real_codex_environment: str


class LauncherSnapshot(Protocol):
    device: int
    inode: int


def select_codex_executable(
    launcher: LauncherSnapshot,
    *,
    profile: CodexProfile,
    environment: Callable[[], Mapping[str, str]],
    path_factory: Callable[[], Callable[[str], Path]],
    executable_path: Callable[[], Callable[[], list[str]]],
    current_directory: Callable[[], str],
    os_error_type: Callable[[], type[BaseException]],
    regular_file_test: Callable[[], Callable[[int], bool]],
    access_check: Callable[[], Callable[[Path, int], bool]],
    executable_mode: Callable[[], int],
    error_type: Callable[[], type[BaseException]],
) -> Path:
    """Select one usable non-launcher executable candidate for Codex."""

    override = environment().get(profile.real_codex_environment)
    if override:
        candidate = path_factory()(override)
        if not candidate.is_absolute():
            raise error_type()(
                f"{profile.real_codex_environment} must be an absolute path"
            )
        candidates = [candidate]
    else:
        candidates = [
            path_factory()(entry or current_directory()) / "codex"
            for entry in executable_path()()
        ]

    for candidate in candidates:
        try:
            metadata = candidate.stat()
        except os_error_type():
            continue
        if (
            not regular_file_test()(metadata.st_mode)
            or not access_check()(candidate, executable_mode())
        ):
            continue
        if (metadata.st_dev, metadata.st_ino) == (
            launcher.device,
            launcher.inode,
        ):
            continue
        return candidate.absolute()

    if override:
        raise error_type()(
            f"{profile.real_codex_environment} does not name a usable "
            "non-launcher executable"
        )
    raise error_type()(
        "cannot find the real Codex executable; set "
        f"{profile.real_codex_environment}"
    )
