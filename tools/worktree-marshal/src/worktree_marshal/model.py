"""Durable lifecycle vocabulary, transition graph, and transaction transforms.

`RUN_TRANSITIONS` is the declarative lifecycle graph.  Each record names one
durable state writer in `engine.py`, the exact family of states it may be
entered from, and the exact family of states it may record.  The source
families are the same objects the engine uses for its admission guards, so the
table is the single place the whole lifecycle is visible.

The source families are derived from the *state* guards the engine actually
enforces.  A member of a source family may still be refused at run time by a
field, audit, lock, worktree, or ref condition that is not part of the durable
state vocabulary; the graph bounds the durable states, not the whole
precondition.  `restore_integration_transaction` deliberately restores any
recorded string, so `RESTORED_PREVIOUS_STATES` describes only the values
`integrate_run` captures and manifest loading accepts.
"""

from __future__ import annotations

from typing import (
    Collection,
    Iterable,
    Literal,
    Mapping,
    MutableMapping,
    NamedTuple,
    TypeAlias,
    TypeGuard,
)


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

INITIAL_RUN_STATE: RunState = "allocating"

ACTIVE_RUN_STATES: frozenset[RunState] = frozenset(
    {
        "allocating",
        "ready",
        "running",
    }
)

CLEANED_STATES: frozenset[RunState] = frozenset(
    {
        "cleaned",
        "cleaned-branch-retained",
        "cleaned-ref-retained",
    }
)

RETAINED_REF_CLEANUP_STATES: frozenset[RunState] = frozenset(
    {
        "cleaned-branch-retained",
        "cleaned-ref-retained",
    }
)

RESOLVABLE_CONFLICT_STATES: frozenset[RunState] = frozenset(
    {
        "integration-conflict",
        "integration-continue-pending",
    }
)

RESTORATION_CHECKPOINT_STATES: frozenset[RunState] = frozenset(
    {
        "integration-abort-pending",
        "integration-rebase-rollback-pending",
    }
)

REBASE_TRANSACTION_STATES: frozenset[RunState] = frozenset(
    {
        "integration-rebase-pending",
        "integration-rebase-rollback-pending",
        "integration-rebase-recovery-failed",
        "integration-rebase-rollback-failed",
    }
)

LANDING_CHECKPOINT_STATES: frozenset[RunState] = frozenset(
    {
        "integration-merge-pending",
        "integration-manual-landing-pending",
        "integration-verification-pending",
        "integration-verification-failed",
    }
)

CANDIDATE_ABORT_STATES: frozenset[RunState] = frozenset(
    {
        "integration-review-pending",
        "integration-merge-pending",
    }
)

ABORTABLE_INTEGRATION_STATES: frozenset[RunState] = frozenset(
    {
        "integration-conflict",
        "integration-continue-pending",
        "integration-review-pending",
        "integration-merge-pending",
        "integration-abort-pending",
        "integration-rebase-pending",
        "integration-rebase-recovery-failed",
    }
)

CONDITIONAL_ABORT_STATES: frozenset[RunState] = frozenset(
    {
        "integration-verification-failed",
    }
)

INTEGRATED_CLEANUP_STATES: frozenset[RunState] = frozenset(
    {
        "integrated-pending-cleanup",
        "integration-cleanup-pending",
        "integration-cleanup-failed",
    }
)

INTERRUPTED_CLEANUP_STATES: frozenset[RunState] = frozenset(
    {
        "integration-cleanup-pending",
        "integration-cleanup-failed",
    }
)

REOPENABLE_STATES: frozenset[RunState] = (
    frozenset(RUN_STATES)
    - CLEANED_STATES
    - frozenset(RETIREMENT_PENDING_STATES)
    - RESOLVABLE_CONFLICT_STATES
)

INTEGRATION_ENTRY_STATES: frozenset[RunState] = (
    frozenset(RUN_STATES)
    - CLEANED_STATES
    - frozenset(RETIREMENT_PENDING_STATES)
    - frozenset(MANAGED_CONFLICT_STATES)
    - REBASE_TRANSACTION_STATES
)

CLEANABLE_STATES: frozenset[RunState] = (
    frozenset(RUN_STATES)
    - CLEANED_STATES
    - frozenset(RETIREMENT_PENDING_STATES)
    - frozenset(MANAGED_CONFLICT_STATES)
    - frozenset({"quarantined"})
)

UNREACHABLE_RUN_STATES: frozenset[RunState] = frozenset(
    {
        "integration-merge-failed",
    }
)

RESTORED_PREVIOUS_STATES: frozenset[RunState] = (
    INTEGRATION_ENTRY_STATES - UNREACHABLE_RUN_STATES
)


class RunTransition(NamedTuple):
    """One durable state writer and the exact edges it is able to perform."""

    sources: frozenset[RunState]
    targets: frozenset[RunState]
    operations: tuple[str, ...]


RUN_TRANSITIONS: tuple[RunTransition, ...] = (
    RunTransition(frozenset(), frozenset({"allocating"}), ("allocate_run",)),
    RunTransition(
        frozenset({"allocating"}),
        frozenset({"ready"}),
        ("allocate_run",),
    ),
    RunTransition(
        frozenset({"allocating", "ready"}),
        frozenset({"allocation-failed"}),
        ("allocate_run",),
    ),
    RunTransition(REOPENABLE_STATES, frozenset({"running"}), ("launch_child",)),
    RunTransition(
        frozenset({"running"}),
        frozenset({"preserved", "failed-preserved", "quarantined"}),
        ("preserve_run",),
    ),
    RunTransition(
        frozenset({"running"}),
        frozenset({"quarantined"}),
        ("quarantine_rewritten_run",),
    ),
    RunTransition(
        ACTIVE_RUN_STATES,
        frozenset({"interrupted", "quarantined"}),
        ("reconcile_stale_run",),
    ),
    RunTransition(
        CLEANABLE_STATES,
        frozenset({"integration-cleanup-pending"}),
        ("safe_cleanup",),
    ),
    RunTransition(
        frozenset({"integration-cleanup-pending"}),
        RETAINED_REF_CLEANUP_STATES,
        ("safe_cleanup",),
    ),
    RunTransition(
        frozenset({"cleaned-branch-retained"}),
        frozenset({"cleaned-branch-retained"}),
        ("safe_cleanup", "retry_retained_ref_cleanup"),
    ),
    RunTransition(
        frozenset({"cleaned-ref-retained"}),
        frozenset({"cleaned-ref-retained"}),
        ("safe_cleanup", "retry_retained_ref_cleanup"),
    ),
    RunTransition(
        RETAINED_REF_CLEANUP_STATES,
        frozenset({"cleaned"}),
        ("retry_retained_ref_cleanup",),
    ),
    RunTransition(
        INTEGRATED_CLEANUP_STATES,
        RETAINED_REF_CLEANUP_STATES,
        ("recover_removed_worktree_cleanup",),
    ),
    RunTransition(
        frozenset({"integrated-pending-cleanup", "integration-cleanup-pending"}),
        frozenset({"integration-cleanup-failed"}),
        ("launch_child", "integrate_run"),
    ),
    RunTransition(
        frozenset({"integration-rebase-pending", "integration-continue-pending"}),
        frozenset({"integration-conflict"}),
        ("record_managed_conflict",),
    ),
    RunTransition(
        RESOLVABLE_CONFLICT_STATES,
        frozenset({"integration-conflict"}),
        ("resolve_conflict_run", "continue_conflict_run", "launch_resolver"),
    ),
    RunTransition(
        frozenset({"integration-conflict"}),
        frozenset({"integration-continue-pending"}),
        ("continue_conflict_run",),
    ),
    RunTransition(
        frozenset({"integration-continue-pending"}),
        frozenset({"integration-review-pending"}),
        ("record_review_pending_candidate",),
    ),
    RunTransition(
        frozenset({"integration-rebase-pending"}),
        frozenset({"integration-merge-pending"}),
        ("record_initial_rebase_candidate", "integrate_run"),
    ),
    RunTransition(
        INTEGRATION_ENTRY_STATES,
        frozenset({"integration-rebase-pending"}),
        ("integrate_run",),
    ),
    RunTransition(
        frozenset({"integration-rebase-pending"}),
        frozenset({"integration-rebase-rollback-pending"}),
        ("abort_failed_integration_rebase",),
    ),
    RunTransition(
        INTEGRATION_ENTRY_STATES | frozenset({"integration-rebase-rollback-pending"}),
        frozenset(
            {
                "integration-rebase-rollback-pending",
                "integration-rebase-rollback-failed",
            }
        ),
        (
            "rollback_completed_integration_rebase",
            "record_integration_recovery_failure",
        ),
    ),
    RunTransition(
        ABORTABLE_INTEGRATION_STATES | INTEGRATION_ENTRY_STATES,
        frozenset({"integration-rebase-recovery-failed"}),
        ("record_integration_recovery_failure",),
    ),
    RunTransition(
        ABORTABLE_INTEGRATION_STATES | CONDITIONAL_ABORT_STATES,
        frozenset({"integration-abort-pending"}),
        ("abort_conflict_run",),
    ),
    RunTransition(
        frozenset({"integration-abort-pending"}),
        frozenset({"integration-abort-recovery-failed"}),
        ("abort_conflict_run", "record_integration_recovery_failure"),
    ),
    RunTransition(
        RESTORATION_CHECKPOINT_STATES,
        RESTORED_PREVIOUS_STATES,
        ("finish_restored_integration",),
    ),
    RunTransition(
        INTEGRATION_ENTRY_STATES,
        frozenset(
            {
                "integration-merge-pending",
                "integration-manual-landing-pending",
            }
        ),
        ("land_candidate_with_cas", "integrate_run"),
    ),
    RunTransition(
        frozenset(
            {
                "integration-merge-pending",
                "integration-manual-landing-pending",
            }
        ),
        frozenset({"integration-verification-pending"}),
        ("land_candidate_with_cas",),
    ),
    RunTransition(
        LANDING_CHECKPOINT_STATES,
        frozenset({"integration-verification-failed"}),
        ("land_candidate_with_cas",),
    ),
    RunTransition(
        frozenset({"integration-verification-pending"}),
        frozenset({"integrated-pending-cleanup"}),
        ("land_candidate_with_cas",),
    ),
    RunTransition(
        INTEGRATION_ENTRY_STATES,
        frozenset(
            {
                "integration-verification-pending",
                "integration-verification-failed",
                "integrated-pending-cleanup",
            }
        ),
        ("integrate_run",),
    ),
    RunTransition(
        CLEANABLE_STATES,
        frozenset(
            {
                "integration-verification-failed",
                "integrated-pending-cleanup",
            }
        ),
        ("clean_run",),
    ),
    RunTransition(
        frozenset({"quarantined"}),
        frozenset({"retirement-pending"}),
        ("checkpoint_rewritten_quarantine_retirement",),
    ),
    RunTransition(
        frozenset({"retirement-pending"}),
        frozenset({"retirement-ref-cleanup-pending"}),
        ("mark_retirement_worktree_removed",),
    ),
    RunTransition(
        frozenset({"retirement-ref-cleanup-pending"}),
        frozenset({"cleaned"}),
        ("finalize_retirement",),
    ),
)

RUN_TRANSITION_EDGES: frozenset[tuple[RunState, RunState]] = frozenset(
    (source, target)
    for transition in RUN_TRANSITIONS
    for source in transition.sources
    for target in transition.targets
)

RUN_TRANSITION_TARGETS: Mapping[RunState, frozenset[RunState]] = {
    state: frozenset(
        target for source, target in RUN_TRANSITION_EDGES if source == state
    )
    for state in RUN_STATES
}

RUN_TRANSITION_OPERATIONS: tuple[str, ...] = tuple(
    sorted(
        {
            operation
            for transition in RUN_TRANSITIONS
            for operation in transition.operations
        }
    )
)


def run_transition_targets(
    source: str,
    *,
    targets: Mapping[str, Collection[str]] = RUN_TRANSITION_TARGETS,
) -> frozenset[str]:
    """Return the exact durable states one recorded state may become."""

    return frozenset(targets.get(source, frozenset()))


def is_run_transition(
    source: object,
    target: object,
    *,
    edges: Collection[tuple[str, str]] = RUN_TRANSITION_EDGES,
) -> bool:
    """Return whether the engine may durably replace one exact state with another."""

    return (source, target) in edges


def validate_run_transition(
    source: object,
    target: object,
    *,
    error_type: type[Exception],
    edges: Collection[tuple[str, str]] = RUN_TRANSITION_EDGES,
) -> None:
    """Reject a durable state replacement the lifecycle graph does not contain."""

    if not is_run_transition(source, target, edges=edges):
        raise error_type("run manifest has an invalid lifecycle transition")


MANUAL_LANDING_CHECKPOINT_FIELDS = (
    "integration_manual_landing_started_at",
    "integration_landing_expected_head",
    "integration_landing_candidate_head",
    "integration_landing_started_at",
)

INTEGRATION_TRANSACTION_FIELDS = (
    "integration_source_head",
    "integration_target_head",
    "integration_candidate_head",
    "integration_conflict_head",
    "integration_conflict_commit",
    "integration_precommit_commit",
    "integration_precommit_index_tree",
    "integration_conflict_paths",
    "integration_unmerged_paths",
    "integration_allowed_staged_paths",
    "integration_protected_index_paths",
    "integration_protected_index_hash",
    "integration_rebase_metadata_hash",
    "integration_conflicted_at",
    "integration_conflict_error",
    "integration_resolution_staged_at",
    "integration_resolver_scope_error",
    "integration_continue_started_at",
    "integration_manual_resolution",
    *MANUAL_LANDING_CHECKPOINT_FIELDS,
    "integration_abort_mode",
    "integration_abort_started_at",
    "integration_rollback_started_at",
    "integration_target_mismatch_head",
    "integration_target_mismatch_at",
    "integration_target_verification_error",
    "integration_started_at",
    "integration_source_anchor_created",
    "integration_rebased_at",
    "integration_previous_state",
)

ABORTED_INTEGRATION_ARCHIVE_FIELDS = (
    ("integration_source_head", "last_integration_source_head"),
    ("integration_target_head", "last_integration_target_head"),
    ("integration_candidate_head", "last_integration_candidate_head"),
    ("integration_conflict_paths", "last_integration_conflict_paths"),
)


def is_run_state(
    value: object,
    *,
    run_states: Collection[str] = RUN_STATES,
) -> TypeGuard[str]:
    """Return whether a value is one exact durable lifecycle state."""

    return isinstance(value, str) and value in run_states


def restore_integration_transaction(
    manifest: MutableMapping[str, object],
    *,
    transaction_fields: Iterable[str],
    archive_fields: Iterable[tuple[str, str]],
) -> None:
    """Remove one in-memory transaction and restore its recorded prior state."""

    previous_state = manifest.get("integration_previous_state")
    for current, archived in archive_fields:
        value = manifest.get(current)
        if value is not None:
            manifest[archived] = value
    for field in transaction_fields:
        manifest.pop(field, None)
    manifest["state"] = (
        previous_state if isinstance(previous_state, str) else "preserved"
    )
