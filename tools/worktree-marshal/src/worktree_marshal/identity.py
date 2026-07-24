"""Immutable runtime identity records shared by launcher workflows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


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
