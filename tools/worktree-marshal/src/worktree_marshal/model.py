"""Pure durable run-state vocabulary for Worktree Marshal."""

from __future__ import annotations

from typing import Collection, Literal, TypeAlias, TypeGuard


RunState: TypeAlias = Literal[
    "allocating",
    "allocation-failed",
    "ready",
    "running",
    "preserved",
    "failed-preserved",
    "interrupted",
    "quarantined",
    "retirement-pending",
    "retirement-ref-cleanup-pending",
    "cleaned",
    "cleaned-branch-retained",
    "integration-conflict",
    "integration-continue-pending",
    "integration-review-pending",
    "integration-manual-landing-pending",
    "integration-abort-pending",
    "integration-abort-recovery-failed",
    "integration-rebase-pending",
    "integration-rebase-recovery-failed",
    "integration-rebase-rollback-pending",
    "integration-rebase-rollback-failed",
    "integration-merge-pending",
    "integration-merge-failed",
    "integration-verification-pending",
    "integration-verification-failed",
    "integrated-pending-cleanup",
    "integration-cleanup-pending",
    "integration-cleanup-failed",
    "cleaned-ref-retained",
]

RETIREMENT_PENDING_STATES: set[RunState] = {
    "retirement-pending",
    "retirement-ref-cleanup-pending",
}

MANAGED_CONFLICT_STATES: set[RunState] = {
    "integration-conflict",
    "integration-continue-pending",
    "integration-abort-pending",
}

RUN_STATES: set[RunState] = {
    "allocating",
    "allocation-failed",
    "ready",
    "running",
    "preserved",
    "failed-preserved",
    "interrupted",
    "quarantined",
    *RETIREMENT_PENDING_STATES,
    "cleaned",
    "cleaned-branch-retained",
    "integration-conflict",
    "integration-continue-pending",
    "integration-review-pending",
    "integration-manual-landing-pending",
    "integration-abort-pending",
    "integration-abort-recovery-failed",
    "integration-rebase-pending",
    "integration-rebase-recovery-failed",
    "integration-rebase-rollback-pending",
    "integration-rebase-rollback-failed",
    "integration-merge-pending",
    "integration-merge-failed",
    "integration-verification-pending",
    "integration-verification-failed",
    "integrated-pending-cleanup",
    "integration-cleanup-pending",
    "integration-cleanup-failed",
    "cleaned-ref-retained",
}


def is_run_state(
    value: object,
    *,
    run_states: Collection[str] = RUN_STATES,
) -> TypeGuard[str]:
    """Return whether a value is one exact durable lifecycle state."""

    return isinstance(value, str) and value in run_states
