"""I/O-free run identity and lexical state-path policy."""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import datetime
from pathlib import Path


RUN_ID_RE = re.compile(r"^[0-9]{8}t[0-9]{6}z-[0-9a-f]{12}$")


def new_run_id(
    *,
    current_time: Callable[[], datetime],
    random_suffix: Callable[[], str],
) -> str:
    """Generate one run ID from explicit clock and entropy providers."""

    stamp = current_time().strftime("%Y%m%dt%H%M%Sz").lower()
    return f"{stamp}-{random_suffix()}"


def repo_lock_path(state_root: Path) -> Path:
    return state_root / "repository.lock"


def run_lock_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.lock"


def manifest_path(state_root: Path, run_id: str) -> Path:
    return state_root / "runs" / f"{run_id}.json"
