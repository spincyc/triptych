#!/usr/bin/env python3
"""Direct parity tests for the extracted durable lifecycle model seam."""

from __future__ import annotations

import ast
import importlib
import os
import subprocess
import sys
import unittest
from collections.abc import Iterator, MutableMapping
from pathlib import Path
from typing import get_args
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE_ROOT / "src"
EXPECTED_RUN_STATES = frozenset(
    {
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
    }
)
EXPECTED_RETIREMENT_PENDING_STATES = frozenset(
    {
        "retirement-pending",
        "retirement-ref-cleanup-pending",
    }
)
EXPECTED_MANAGED_CONFLICT_STATES = frozenset(
    {
        "integration-conflict",
        "integration-continue-pending",
        "integration-abort-pending",
    }
)
EXPECTED_MANUAL_LANDING_CHECKPOINT_FIELDS = (
    "integration_manual_landing_started_at",
    "integration_landing_expected_head",
    "integration_landing_candidate_head",
    "integration_landing_started_at",
)
EXPECTED_INTEGRATION_TRANSACTION_FIELDS = (
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
    *EXPECTED_MANUAL_LANDING_CHECKPOINT_FIELDS,
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
EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS = (
    ("integration_source_head", "last_integration_source_head"),
    ("integration_target_head", "last_integration_target_head"),
    ("integration_candidate_head", "last_integration_candidate_head"),
    ("integration_conflict_paths", "last_integration_conflict_paths"),
)
EXPECTED_TRANSITION_FAMILIES = {
    "ACTIVE_RUN_STATES": frozenset(
        {
            "allocating",
            "ready",
            "running",
        }
    ),
    "CLEANED_STATES": frozenset(
        {
            "cleaned",
            "cleaned-branch-retained",
            "cleaned-ref-retained",
        }
    ),
    "RETAINED_REF_CLEANUP_STATES": frozenset(
        {
            "cleaned-branch-retained",
            "cleaned-ref-retained",
        }
    ),
    "RESOLVABLE_CONFLICT_STATES": frozenset(
        {
            "integration-conflict",
            "integration-continue-pending",
        }
    ),
    "RESTORATION_CHECKPOINT_STATES": frozenset(
        {
            "integration-abort-pending",
            "integration-rebase-rollback-pending",
        }
    ),
    "REBASE_TRANSACTION_STATES": frozenset(
        {
            "integration-rebase-pending",
            "integration-rebase-rollback-pending",
            "integration-rebase-recovery-failed",
            "integration-rebase-rollback-failed",
        }
    ),
    "LANDING_CHECKPOINT_STATES": frozenset(
        {
            "integration-merge-pending",
            "integration-manual-landing-pending",
            "integration-verification-pending",
            "integration-verification-failed",
        }
    ),
    "CANDIDATE_ABORT_STATES": frozenset(
        {
            "integration-review-pending",
            "integration-merge-pending",
        }
    ),
    "ABORTABLE_INTEGRATION_STATES": frozenset(
        {
            "integration-conflict",
            "integration-continue-pending",
            "integration-review-pending",
            "integration-merge-pending",
            "integration-abort-pending",
            "integration-rebase-pending",
            "integration-rebase-recovery-failed",
        }
    ),
    "CONDITIONAL_ABORT_STATES": frozenset({"integration-verification-failed"}),
    "INTEGRATED_CLEANUP_STATES": frozenset(
        {
            "integrated-pending-cleanup",
            "integration-cleanup-pending",
            "integration-cleanup-failed",
        }
    ),
    "INTERRUPTED_CLEANUP_STATES": frozenset(
        {
            "integration-cleanup-pending",
            "integration-cleanup-failed",
        }
    ),
    "UNREACHABLE_RUN_STATES": frozenset({"integration-merge-failed"}),
    "REOPENABLE_STATES": EXPECTED_RUN_STATES
    - {
        "cleaned",
        "cleaned-branch-retained",
        "cleaned-ref-retained",
        "retirement-pending",
        "retirement-ref-cleanup-pending",
        "integration-conflict",
        "integration-continue-pending",
    },
    "INTEGRATION_ENTRY_STATES": EXPECTED_RUN_STATES
    - {
        "cleaned",
        "cleaned-branch-retained",
        "cleaned-ref-retained",
        "retirement-pending",
        "retirement-ref-cleanup-pending",
        "integration-conflict",
        "integration-continue-pending",
        "integration-abort-pending",
        "integration-rebase-pending",
        "integration-rebase-rollback-pending",
        "integration-rebase-recovery-failed",
        "integration-rebase-rollback-failed",
    },
    "CLEANABLE_STATES": EXPECTED_RUN_STATES
    - {
        "cleaned",
        "cleaned-branch-retained",
        "cleaned-ref-retained",
        "retirement-pending",
        "retirement-ref-cleanup-pending",
        "integration-conflict",
        "integration-continue-pending",
        "integration-abort-pending",
        "quarantined",
    },
}
EXPECTED_TRANSITION_FAMILIES["RESTORED_PREVIOUS_STATES"] = (
    EXPECTED_TRANSITION_FAMILIES["INTEGRATION_ENTRY_STATES"]
    - EXPECTED_TRANSITION_FAMILIES["UNREACHABLE_RUN_STATES"]
)
EXPECTED_TRANSITION_OPERATIONS = (
    "abort_conflict_run",
    "abort_failed_integration_rebase",
    "allocate_run",
    "checkpoint_rewritten_quarantine_retirement",
    "clean_run",
    "continue_conflict_run",
    "finalize_retirement",
    "finish_restored_integration",
    "integrate_run",
    "land_candidate_with_cas",
    "launch_child",
    "launch_resolver",
    "mark_retirement_worktree_removed",
    "preserve_run",
    "quarantine_rewritten_run",
    "reconcile_stale_run",
    "record_initial_rebase_candidate",
    "record_integration_recovery_failure",
    "record_managed_conflict",
    "record_review_pending_candidate",
    "recover_removed_worktree_cleanup",
    "resolve_conflict_run",
    "retry_retained_ref_cleanup",
    "rollback_completed_integration_rebase",
    "safe_cleanup",
)
ENGINE_TRANSITION_FAMILY_ALIASES = (
    "ABORTABLE_INTEGRATION_STATES",
    "ACTIVE_RUN_STATES",
    "CANDIDATE_ABORT_STATES",
    "CLEANED_STATES",
    "CONDITIONAL_ABORT_STATES",
    "INTEGRATED_CLEANUP_STATES",
    "INTERRUPTED_CLEANUP_STATES",
    "LANDING_CHECKPOINT_STATES",
    "REBASE_TRANSACTION_STATES",
    "RESOLVABLE_CONFLICT_STATES",
    "RESTORATION_CHECKPOINT_STATES",
    "RETAINED_REF_CLEANUP_STATES",
)
ILLEGAL_RUN_TRANSITIONS = (
    ("cleaned", "running"),
    ("cleaned", "ready"),
    ("cleaned", "integration-rebase-pending"),
    ("cleaned", "retirement-pending"),
    ("preserved", "cleaned"),
    ("ready", "integration-conflict"),
    ("running", "cleaned"),
    ("quarantined", "cleaned"),
    ("integration-review-pending", "integration-continue-pending"),
    ("interrupted", "retirement-pending"),
    ("integration-conflict", "integrated-pending-cleanup"),
    ("integration-conflict", "cleaned"),
    ("retirement-ref-cleanup-pending", "retirement-pending"),
    ("retirement-pending", "cleaned"),
    ("allocating", "preserved"),
    ("allocation-failed", "ready"),
    ("cleaned-branch-retained", "cleaned-ref-retained"),
    ("cleaned-ref-retained", "cleaned-branch-retained"),
    ("preserved", "integration-merge-failed"),
    ("running", "integration-conflict"),
)


class StateName(str):
    """A string subclass used to preserve the legacy isinstance contract."""


class MappingFailure(RuntimeError):
    """An injected mutable-manifest operation failure."""


class RecordingManifest(MutableMapping[str, object]):
    """A mutable manifest that records and can fail before named operations."""

    def __init__(
        self,
        values: dict[str, object],
        *,
        fail_at: tuple[str, str] | None = None,
    ) -> None:
        self.values = values.copy()
        self.events: list[tuple[str, str]] = []
        self.fail_at = fail_at

    def _record(self, operation: str, field: str) -> None:
        event = (operation, field)
        self.events.append(event)
        if event == self.fail_at:
            raise MappingFailure(f"{operation} failed for {field}")

    def __getitem__(self, field: str) -> object:
        return self.values[field]

    def __setitem__(self, field: str, value: object) -> None:
        self._record("set", field)
        self.values[field] = value

    def __delitem__(self, field: str) -> None:
        del self.values[field]

    def __iter__(self) -> Iterator[str]:
        return iter(self.values)

    def __len__(self) -> int:
        return len(self.values)

    def get(self, field: str, default: object = None) -> object:
        self._record("get", field)
        return self.values.get(field, default)

    def pop(self, field: str, default: object = None) -> object:
        self._record("pop", field)
        return self.values.pop(field, default)


class ModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))
        cls.model = importlib.import_module("worktree_marshal.model")
        cls.engine = importlib.import_module("worktree_marshal.engine")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def transaction_manifest(self, previous_state: object = ...) -> dict:
        manifest = {
            field: f"value:{field}"
            for field in EXPECTED_INTEGRATION_TRANSACTION_FIELDS
            if field != "integration_previous_state"
        }
        manifest.update(
            {
                "state": "integration-abort-pending",
                "unrelated": "preserved",
            }
        )
        if previous_state is not ...:
            manifest["integration_previous_state"] = previous_state
        return manifest

    def test_model_import_does_not_load_the_lifecycle_engine(self) -> None:
        script = (
            "import os, sys; "
            "before = dict(os.environ); "
            f"sys.path.insert(0, {str(SOURCE_ROOT)!r}); "
            "import worktree_marshal.model; "
            "raise SystemExit("
            "'worktree_marshal.engine' in sys.modules or dict(os.environ) != before"
            ")"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            cwd=PACKAGE_ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_run_state_vocabulary_and_type_alias_are_exact(self) -> None:
        self.assertIs(type(self.model.RUN_STATES), set)
        self.assertEqual(self.model.RUN_STATES, EXPECTED_RUN_STATES)
        self.assertEqual(set(get_args(self.model.RunState)), EXPECTED_RUN_STATES)

    def test_state_families_are_exact_sets_and_subsets(self) -> None:
        self.assertIs(type(self.model.RETIREMENT_PENDING_STATES), set)
        self.assertIs(type(self.model.MANAGED_CONFLICT_STATES), set)
        self.assertEqual(
            self.model.RETIREMENT_PENDING_STATES,
            EXPECTED_RETIREMENT_PENDING_STATES,
        )
        self.assertEqual(
            self.model.MANAGED_CONFLICT_STATES,
            EXPECTED_MANAGED_CONFLICT_STATES,
        )
        self.assertLessEqual(
            self.model.RETIREMENT_PENDING_STATES,
            self.model.RUN_STATES,
        )
        self.assertLessEqual(
            self.model.MANAGED_CONFLICT_STATES,
            self.model.RUN_STATES,
        )
        self.assertTrue(
            self.model.RETIREMENT_PENDING_STATES.isdisjoint(
                self.model.MANAGED_CONFLICT_STATES
            )
        )

    def test_integration_field_vocabularies_are_exact_ordered_tuples(self) -> None:
        expected = (
            (
                self.model.MANUAL_LANDING_CHECKPOINT_FIELDS,
                EXPECTED_MANUAL_LANDING_CHECKPOINT_FIELDS,
            ),
            (
                self.model.INTEGRATION_TRANSACTION_FIELDS,
                EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
            ),
            (
                self.model.ABORTED_INTEGRATION_ARCHIVE_FIELDS,
                EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
            ),
        )
        for observed, oracle in expected:
            with self.subTest(first=oracle[0]):
                self.assertIs(type(observed), tuple)
                self.assertEqual(observed, oracle)
                self.assertEqual(len(observed), len(set(observed)))

        self.assertIs(
            self.engine.MANUAL_LANDING_CHECKPOINT_FIELDS,
            self.model.MANUAL_LANDING_CHECKPOINT_FIELDS,
        )
        self.assertIs(
            self.engine.INTEGRATION_TRANSACTION_FIELDS,
            self.model.INTEGRATION_TRANSACTION_FIELDS,
        )
        archive_sources = {
            current
            for current, _ in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        }
        archive_destinations = {
            archived
            for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        }
        self.assertLessEqual(
            archive_sources,
            set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS),
        )
        self.assertEqual(
            len(archive_destinations),
            len(EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS),
        )
        self.assertTrue(
            archive_destinations.isdisjoint(
                EXPECTED_INTEGRATION_TRANSACTION_FIELDS
            )
        )

    def test_classifier_preserves_exact_string_semantics(self) -> None:
        for state in EXPECTED_RUN_STATES:
            with self.subTest(valid=state):
                self.assertTrue(self.model.is_run_state(state))
        self.assertTrue(self.model.is_run_state(StateName("preserved")))

        invalid = (
            "",
            "Preserved",
            "preserved ",
            "preserved\n",
            "integration-merge",
            None,
            1,
            b"preserved",
            [],
            {},
        )
        for value in invalid:
            with self.subTest(invalid=value):
                self.assertFalse(self.model.is_run_state(value))

        self.assertTrue(
            self.model.is_run_state(
                "injected-test-state",
                run_states={"injected-test-state"},
            )
        )

    def test_engine_preserves_state_set_aliases_and_rebinding(self) -> None:
        self.assertIs(self.engine.RUN_STATES, self.model.RUN_STATES)
        self.assertIs(
            self.engine.RETIREMENT_PENDING_STATES,
            self.model.RETIREMENT_PENDING_STATES,
        )
        self.assertIs(
            self.engine.MANAGED_CONFLICT_STATES,
            self.model.MANAGED_CONFLICT_STATES,
        )
        self.assertIs(self.engine.is_run_state, self.model.is_run_state)

        with mock.patch.object(self.engine, "RUN_STATES", set()):
            with self.assertRaisesRegex(
                self.engine.LauncherError,
                "^run manifest has an invalid lifecycle state$",
            ):
                self.engine.validate_manifest_paths(
                    object(),
                    {"state": "preserved"},
                )

    def test_manifest_state_diagnostics_remain_exact_and_opaque(self) -> None:
        invalid = "not-a-state"
        with self.assertRaisesRegex(
            self.engine.LauncherError,
            "^run manifest has an invalid lifecycle state$",
        ) as current:
            self.engine.validate_manifest_paths(
                object(),
                {"state": invalid},
            )
        self.assertNotIn(invalid, str(current.exception))

        with self.assertRaisesRegex(
            self.engine.LauncherError,
            "^run manifest has an invalid previous lifecycle state$",
        ) as previous:
            self.engine.validate_manifest_paths(
                object(),
                {
                    "state": "preserved",
                    "integration_previous_state": invalid,
                },
            )
        self.assertNotIn(invalid, str(previous.exception))

    def test_pure_transaction_restore_preserves_exact_string_semantics(self) -> None:
        string_states = (
            *EXPECTED_RUN_STATES,
            "invalid-but-still-a-string",
            StateName("preserved"),
        )
        for previous_state in string_states:
            with self.subTest(previous_state=previous_state):
                manifest = self.transaction_manifest(previous_state)
                extension = object()
                manifest["extension"] = extension

                result = self.model.restore_integration_transaction(
                    manifest,
                    transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
                    archive_fields=(),
                )

                self.assertIsNone(result)
                self.assertIs(manifest["state"], previous_state)
                self.assertIs(manifest["extension"], extension)
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )
                self.assertTrue(
                    {
                        archived
                        for _, archived in (
                            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                        )
                    }.isdisjoint(manifest)
                )

        for previous_state in (..., None, 0, True, b"preserved", [], {}):
            with self.subTest(fallback=previous_state):
                manifest = self.transaction_manifest(previous_state)

                self.model.restore_integration_transaction(
                    manifest,
                    transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
                    archive_fields=(),
                )

                self.assertEqual(manifest["state"], "preserved")
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )
                self.assertTrue(
                    {
                        archived
                        for _, archived in (
                            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                        )
                    }.isdisjoint(manifest)
                )

    def test_pure_transaction_archive_distinguishes_none_and_falsey_values(
        self,
    ) -> None:
        manifest = self.transaction_manifest("preserved")
        extension = object()
        manifest["extension"] = extension
        falsey_values = ("", 0, False, [])
        for (current, archived), value in zip(
            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
            falsey_values,
            strict=True,
        ):
            manifest[current] = value
            manifest[archived] = f"old:{archived}"

        self.model.restore_integration_transaction(
            manifest,
            transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
            archive_fields=EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
        )

        self.assertEqual(
            tuple(
                manifest[archived]
                for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
            ),
            falsey_values,
        )
        self.assertIs(manifest["extension"], extension)
        self.assertTrue(
            set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(manifest)
        )

        manifest = self.transaction_manifest("preserved")
        retained = {
            archived: object()
            for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        }
        manifest.update(retained)
        none_source, missing_source, populated_source, second_none_source = (
            current for current, _ in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        )
        manifest[none_source] = None
        manifest.pop(missing_source)
        manifest[populated_source] = "new-value"
        manifest[second_none_source] = None

        self.model.restore_integration_transaction(
            manifest,
            transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
            archive_fields=EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
        )

        for current, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS:
            with self.subTest(current=current):
                if current == populated_source:
                    self.assertEqual(manifest[archived], "new-value")
                else:
                    self.assertIs(manifest[archived], retained[archived])
        self.assertTrue(
            set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(manifest)
        )

    def test_transaction_transform_preserves_operation_and_failure_order(
        self,
    ) -> None:
        supplied = self.transaction_manifest("preserved")
        manifest = RecordingManifest(supplied)

        self.model.restore_integration_transaction(
            manifest,
            transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
            archive_fields=EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
        )

        expected_archive_events: list[tuple[str, str]] = [
            ("get", "integration_previous_state"),
        ]
        for current, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS:
            expected_archive_events.extend(
                (("get", current), ("set", archived))
            )
        expected_events = [
            *expected_archive_events,
            *(
                ("pop", field)
                for field in EXPECTED_INTEGRATION_TRANSACTION_FIELDS
            ),
            ("set", "state"),
        ]
        self.assertEqual(manifest.events, expected_events)
        self.assertEqual(manifest["state"], "preserved")

        failing_field = EXPECTED_INTEGRATION_TRANSACTION_FIELDS[2]
        manifest = RecordingManifest(
            supplied,
            fail_at=("pop", failing_field),
        )
        with self.assertRaisesRegex(
            MappingFailure,
            "^pop failed for integration_candidate_head$",
        ):
            self.model.restore_integration_transaction(
                manifest,
                transaction_fields=EXPECTED_INTEGRATION_TRANSACTION_FIELDS,
                archive_fields=EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS,
            )

        fields_before_failure = EXPECTED_INTEGRATION_TRANSACTION_FIELDS[:2]
        self.assertEqual(
            manifest.events,
            [
                *expected_archive_events,
                *(("pop", field) for field in fields_before_failure),
                ("pop", failing_field),
            ],
        )
        expected_values = supplied.copy()
        for current, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS:
            expected_values[archived] = supplied[current]
        for field in fields_before_failure:
            expected_values.pop(field)
        self.assertEqual(manifest.values, expected_values)
        self.assertEqual(manifest["state"], "integration-abort-pending")

    def test_transaction_clear_restores_every_valid_previous_state(self) -> None:
        for state in EXPECTED_RUN_STATES:
            with self.subTest(previous_state=state):
                manifest = self.transaction_manifest(state)

                self.engine.clear_integration_transaction(manifest)

                self.assertEqual(manifest["state"], state)
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )
                self.assertTrue(
                    {
                        archived
                        for _, archived in (
                            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                        )
                    }.isdisjoint(manifest)
                )

        for previous_state in (..., None, 1, [], {}):
            with self.subTest(fallback=previous_state):
                manifest = self.transaction_manifest(previous_state)

                self.engine.clear_integration_transaction(manifest)

                self.assertEqual(manifest["state"], "preserved")
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )
                self.assertTrue(
                    {
                        archived
                        for _, archived in (
                            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                        )
                    }.isdisjoint(manifest)
                )

    def test_engine_wrappers_forward_rebound_field_inventories(self) -> None:
        rebound_transaction_fields = (
            "custom_transaction",
            "integration_previous_state",
        )

        manifest = {
            "state": "integration-abort-pending",
            "integration_previous_state": "invalid-but-still-a-string",
            "custom_transaction": "remove",
            "integration_source_head": "preserve",
        }
        with (
            mock.patch.object(
                self.engine,
                "INTEGRATION_TRANSACTION_FIELDS",
                rebound_transaction_fields,
            ),
            mock.patch.object(self.engine, "utc_now") as clock,
        ):
            result = self.engine.clear_integration_transaction(manifest)

        self.assertIsNone(result)
        self.assertEqual(manifest["state"], "invalid-but-still-a-string")
        self.assertNotIn("custom_transaction", manifest)
        self.assertNotIn("integration_previous_state", manifest)
        self.assertEqual(manifest["integration_source_head"], "preserve")
        self.assertNotIn("last_integration_source_head", manifest)
        self.assertNotIn("last_custom_transaction", manifest)
        clock.assert_not_called()

        archived_value: list[object] = []
        previous_state = StateName("preserved")
        manifest = {
            "state": "integration-abort-pending",
            "integration_previous_state": previous_state,
            "custom_transaction": archived_value,
            "integration_source_head": "preserve",
        }
        with (
            mock.patch.object(
                self.engine,
                "INTEGRATION_TRANSACTION_FIELDS",
                rebound_transaction_fields,
            ),
            mock.patch.object(
                self.engine,
                "utc_now",
                return_value="2000-01-01T00:00:00+00:00",
            ),
        ):
            self.engine.archive_aborted_integration(manifest)

        self.assertIs(manifest["state"], previous_state)
        self.assertNotIn("custom_transaction", manifest)
        self.assertNotIn("integration_previous_state", manifest)
        self.assertNotIn("last_custom_transaction", manifest)
        self.assertEqual(manifest["integration_source_head"], "preserve")
        self.assertEqual(manifest["last_integration_source_head"], "preserve")
        self.assertEqual(
            manifest["last_integration_aborted_at"],
            "2000-01-01T00:00:00+00:00",
        )

    def test_archive_clock_runs_after_transform_and_failure_stays_observable(
        self,
    ) -> None:
        timestamp = "2000-01-01T00:00:00+00:00"
        manifest = self.transaction_manifest("preserved")
        expected_archive = {
            archived: manifest[current]
            for current, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        }

        def observe_transformed_manifest() -> str:
            self.assertEqual(manifest["state"], "preserved")
            self.assertTrue(
                set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                    manifest
                )
            )
            self.assertEqual(
                {
                    archived: manifest[archived]
                    for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                },
                expected_archive,
            )
            self.assertNotIn("last_integration_aborted_at", manifest)
            return timestamp

        with mock.patch.object(
            self.engine,
            "utc_now",
            side_effect=observe_transformed_manifest,
        ) as clock:
            self.engine.archive_aborted_integration(manifest)

        clock.assert_called_once_with()
        self.assertEqual(manifest["last_integration_aborted_at"], timestamp)

        manifest = self.transaction_manifest("preserved")
        old_timestamp = "1999-01-01T00:00:00+00:00"
        manifest["last_integration_aborted_at"] = old_timestamp
        expected_failure_archive = {
            archived: manifest[current]
            for current, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
        }

        class ClockFailure(RuntimeError):
            pass

        def fail_after_observing_transform() -> str:
            self.assertEqual(manifest["state"], "preserved")
            self.assertTrue(
                set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                    manifest
                )
            )
            self.assertEqual(
                {
                    archived: manifest[archived]
                    for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                },
                expected_failure_archive,
            )
            self.assertEqual(
                manifest["last_integration_aborted_at"],
                old_timestamp,
            )
            raise ClockFailure("clock unavailable")

        with (
            mock.patch.object(
                self.engine,
                "utc_now",
                side_effect=fail_after_observing_transform,
            ),
            self.assertRaisesRegex(ClockFailure, "^clock unavailable$"),
        ):
            self.engine.archive_aborted_integration(manifest)

        self.assertEqual(manifest["state"], "preserved")
        self.assertTrue(
            set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(manifest)
        )
        self.assertEqual(
            {
                archived: manifest[archived]
                for _, archived in EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
            },
            expected_failure_archive,
        )
        self.assertEqual(
            manifest["last_integration_aborted_at"],
            old_timestamp,
        )

    def test_transaction_archive_restores_and_preserves_audit_fields(self) -> None:
        timestamp = "2000-01-01T00:00:00+00:00"

        for state in EXPECTED_RUN_STATES:
            with self.subTest(previous_state=state):
                manifest = self.transaction_manifest(state)
                expected = {
                    archived: manifest[current]
                    for current, archived in (
                        EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                    )
                }

                with mock.patch.object(
                    self.engine,
                    "utc_now",
                    return_value=timestamp,
                ):
                    self.engine.archive_aborted_integration(manifest)

                self.assertEqual(manifest["state"], state)
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertEqual(manifest["last_integration_aborted_at"], timestamp)
                self.assertEqual(
                    {
                        archived: manifest[archived]
                        for _, archived in (
                            EXPECTED_ABORTED_INTEGRATION_ARCHIVE_FIELDS
                        )
                    },
                    expected,
                )
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )

        for previous_state in (..., None, 1, [], {}):
            with self.subTest(fallback=previous_state):
                manifest = self.transaction_manifest(previous_state)

                with mock.patch.object(
                    self.engine,
                    "utc_now",
                    return_value=timestamp,
                ):
                    self.engine.archive_aborted_integration(manifest)

                self.assertEqual(manifest["state"], "preserved")
                self.assertEqual(manifest["last_integration_aborted_at"], timestamp)
                self.assertTrue(
                    set(EXPECTED_INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )


class RunTransitionTests(unittest.TestCase):
    """Direct enforcement tests for the declarative lifecycle transition graph."""

    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))
        cls.model = importlib.import_module("worktree_marshal.model")
        cls.engine = importlib.import_module("worktree_marshal.engine")
        cls.engine_source = (
            SOURCE_ROOT / "worktree_marshal" / "engine.py"
        ).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def engine_recorded_states(self) -> set[str]:
        """Return every durable state literal the engine writes to a manifest."""

        tree = ast.parse(self.engine_source)
        recorded: set[str] = set()
        indirect: list[str] = []

        def harvest(value: ast.expr) -> None:
            found = {
                node.value
                for node in ast.walk(value)
                if isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value in self.model.RUN_STATES
            }
            if found:
                recorded.update(found)
            else:
                indirect.append(ast.unparse(value))

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target, ast.Subscript)
                        and isinstance(target.slice, ast.Constant)
                        and target.slice.value == "state"
                    ):
                        harvest(node.value)
            if isinstance(node, ast.Dict):
                for key, value in zip(node.keys, node.values):
                    if isinstance(key, ast.Constant) and key.value == "state":
                        harvest(value)
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "state":
                        harvest(keyword.value)

        self.assertEqual(
            sorted(set(indirect)),
            ["retained_state", "state"],
            "an unrecognized indirect durable state writer appeared in the engine",
        )
        return recorded

    def test_transition_families_are_exact_immutable_state_subsets(self) -> None:
        self.assertEqual(
            set(EXPECTED_TRANSITION_FAMILIES),
            {
                name
                for name in vars(self.model)
                if name.endswith("_STATES") and name not in {"RUN_STATES"}
            }
            - {"RETIREMENT_PENDING_STATES", "MANAGED_CONFLICT_STATES"},
        )
        for name, expected in EXPECTED_TRANSITION_FAMILIES.items():
            with self.subTest(family=name):
                family = getattr(self.model, name)
                self.assertIs(type(family), frozenset)
                self.assertEqual(family, expected)
                self.assertLessEqual(family, self.model.RUN_STATES)
        self.assertEqual(self.model.INITIAL_RUN_STATE, "allocating")
        self.assertIn(self.model.INITIAL_RUN_STATE, self.model.RUN_STATES)

    def test_engine_guards_reuse_the_shared_transition_families(self) -> None:
        for name in ENGINE_TRANSITION_FAMILY_ALIASES:
            with self.subTest(family=name):
                self.assertIs(
                    getattr(self.engine, name),
                    getattr(self.model, name),
                )
        self.assertIs(self.engine.RUN_TRANSITIONS, self.model.RUN_TRANSITIONS)
        self.assertIs(self.engine.is_run_transition, self.model.is_run_transition)
        self.assertIs(
            self.engine.run_transition_targets,
            self.model.run_transition_targets,
        )
        self.assertIs(
            self.engine.validate_run_transition,
            self.model.validate_run_transition,
        )

    def test_engine_admission_guards_have_no_remaining_literal_state_sets(self) -> None:
        tree = ast.parse(self.engine_source)
        literal_sets = [
            ast.unparse(node)
            for node in ast.walk(tree)
            if isinstance(node, ast.Set)
            and node.elts
            and all(
                isinstance(element, ast.Constant)
                and isinstance(element.value, str)
                and element.value in self.model.RUN_STATES
                for element in node.elts
            )
        ]

        self.assertEqual(literal_sets, ["{'quarantined'}"])

    def test_transition_records_are_well_formed_and_attributable(self) -> None:
        self.assertIs(type(self.model.RUN_TRANSITIONS), tuple)
        self.assertEqual(
            self.model.RUN_TRANSITION_OPERATIONS,
            EXPECTED_TRANSITION_OPERATIONS,
        )
        creations = []
        for transition in self.model.RUN_TRANSITIONS:
            with self.subTest(transition=transition.operations):
                self.assertIs(type(transition.sources), frozenset)
                self.assertIs(type(transition.targets), frozenset)
                self.assertIs(type(transition.operations), tuple)
                self.assertTrue(transition.operations)
                self.assertTrue(transition.targets)
                self.assertLessEqual(transition.sources, self.model.RUN_STATES)
                self.assertLessEqual(transition.targets, self.model.RUN_STATES)
                for operation in transition.operations:
                    self.assertTrue(callable(getattr(self.engine, operation)))
                if not transition.sources:
                    creations.append(transition)

        self.assertEqual(len(creations), 1)
        self.assertEqual(
            creations[0].targets,
            frozenset({self.model.INITIAL_RUN_STATE}),
        )
        self.assertEqual(creations[0].operations, ("allocate_run",))

    def test_every_engine_state_write_is_a_declared_transition_target(self) -> None:
        recorded = self.engine_recorded_states()
        declared = {target for _, target in self.model.RUN_TRANSITION_EDGES}

        self.assertEqual(recorded, declared)
        self.assertEqual(
            self.model.RUN_STATES - declared,
            self.model.UNREACHABLE_RUN_STATES,
        )

    def test_every_declared_transition_is_reachable_from_allocation(self) -> None:
        reachable = {self.model.INITIAL_RUN_STATE}
        frontier = [self.model.INITIAL_RUN_STATE]
        while frontier:
            for target in self.model.run_transition_targets(frontier.pop()):
                if target not in reachable:
                    reachable.add(target)
                    frontier.append(target)

        self.assertEqual(
            self.model.RUN_STATES - reachable,
            self.model.UNREACHABLE_RUN_STATES,
        )
        admitted = reachable | self.model.UNREACHABLE_RUN_STATES
        for source, target in sorted(self.model.RUN_TRANSITION_EDGES):
            with self.subTest(edge=(source, target)):
                self.assertIn(source, admitted)
                self.assertIn(target, reachable)
        for state in self.model.UNREACHABLE_RUN_STATES:
            with self.subTest(unreachable=state):
                self.assertNotIn(
                    state,
                    {target for _, target in self.model.RUN_TRANSITION_EDGES},
                )
        self.assertEqual(
            {
                state
                for state in self.model.RUN_STATES
                if not self.model.run_transition_targets(state)
            },
            frozenset({"cleaned"}),
        )

    def test_transition_targets_are_the_exact_declared_edges(self) -> None:
        self.assertIs(type(self.model.RUN_TRANSITION_EDGES), frozenset)
        for state in self.model.RUN_STATES:
            with self.subTest(state=state):
                targets = self.model.run_transition_targets(state)
                self.assertIs(type(targets), frozenset)
                self.assertEqual(
                    targets,
                    {
                        target
                        for source, target in self.model.RUN_TRANSITION_EDGES
                        if source == state
                    },
                )
        self.assertEqual(self.model.run_transition_targets("cleaned"), frozenset())
        self.assertEqual(self.model.run_transition_targets("not-a-state"), frozenset())
        self.assertEqual(
            self.model.run_transition_targets(
                "injected",
                targets={"injected": ["ready"]},
            ),
            frozenset({"ready"}),
        )

    def test_illegal_transitions_are_rejected(self) -> None:
        for source, target in ILLEGAL_RUN_TRANSITIONS:
            with self.subTest(illegal=(source, target)):
                self.assertIn(source, self.model.RUN_STATES)
                self.assertIn(target, self.model.RUN_STATES)
                self.assertFalse(self.model.is_run_transition(source, target))
                with self.assertRaisesRegex(
                    self.engine.LauncherError,
                    "^run manifest has an invalid lifecycle transition$",
                ) as rejected:
                    self.model.validate_run_transition(
                        source,
                        target,
                        error_type=self.engine.LauncherError,
                    )
                self.assertNotIn(source, str(rejected.exception))
                self.assertNotIn(target, str(rejected.exception))

        for source, target in sorted(self.model.RUN_TRANSITION_EDGES):
            with self.subTest(legal=(source, target)):
                self.assertTrue(self.model.is_run_transition(source, target))
                self.assertIsNone(
                    self.model.validate_run_transition(
                        source,
                        target,
                        error_type=self.engine.LauncherError,
                    )
                )

        self.assertFalse(self.model.is_run_transition(None, "ready"))
        self.assertFalse(self.model.is_run_transition("ready", None))
        self.assertFalse(self.model.is_run_transition(StateName("cleaned"), "running"))
        self.assertTrue(
            self.model.is_run_transition(
                "injected",
                "state",
                edges={("injected", "state")},
            )
        )

    def test_declared_admission_families_match_their_recorded_edges(self) -> None:
        self.assertEqual(
            self.model.run_transition_targets("integration-conflict"),
            frozenset({"integration-conflict", "integration-continue-pending"})
            | frozenset({"integration-abort-pending"})
            | frozenset({"integration-rebase-recovery-failed"}),
        )
        for state in self.model.ABORTABLE_INTEGRATION_STATES | (
            self.model.CONDITIONAL_ABORT_STATES
        ):
            with self.subTest(abortable=state):
                self.assertIn(
                    "integration-abort-pending",
                    self.model.run_transition_targets(state),
                )
        for state in self.model.RETAINED_REF_CLEANUP_STATES:
            with self.subTest(retained=state):
                self.assertIn("cleaned", self.model.run_transition_targets(state))
        for state in self.model.RESTORATION_CHECKPOINT_STATES:
            with self.subTest(restoration=state):
                self.assertEqual(
                    self.model.RESTORED_PREVIOUS_STATES
                    - self.model.run_transition_targets(state),
                    frozenset(),
                )
        self.assertEqual(
            self.model.run_transition_targets("quarantined")
            & frozenset(self.model.RETIREMENT_PENDING_STATES),
            frozenset({"retirement-pending"}),
        )
        self.assertEqual(
            self.model.run_transition_targets("retirement-pending"),
            frozenset({"retirement-ref-cleanup-pending"}),
        )
        self.assertEqual(
            self.model.run_transition_targets("retirement-ref-cleanup-pending"),
            frozenset({"cleaned"}),
        )


if __name__ == "__main__":
    unittest.main()
