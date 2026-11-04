"""An engine that may seed the retired `proper` and `proper-finish` workflows.

Both definitions were retired on 2026-11-04 in favour of `proper-study`, and the
engine refuses to seed them. They remain this suite's richest fixture for
engine behaviour that every workflow shares: fan-out lanes, repair routing,
convergence budgets, standing findings. The modules that drive those
definitions import `WorkflowEngine` from here, so the opt-in is visible at
the import and nowhere outside the suite can reach it.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

import _workflow  # noqa: E402


class WorkflowEngine(_workflow.WorkflowEngine):
    """The engine, admitting seeds of the frozen legacy definitions."""

    admit_retired_seeds = True
