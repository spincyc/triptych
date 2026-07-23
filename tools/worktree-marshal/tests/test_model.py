#!/usr/bin/env python3
"""Direct parity tests for the extracted durable state vocabulary."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
import unittest
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


class StateName(str):
    """A string subclass used to preserve the legacy isinstance contract."""


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
            for field in self.engine.INTEGRATION_TRANSACTION_FIELDS
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

    def test_transaction_clear_restores_every_valid_previous_state(self) -> None:
        for state in EXPECTED_RUN_STATES:
            with self.subTest(previous_state=state):
                manifest = self.transaction_manifest(state)

                self.engine.clear_integration_transaction(manifest)

                self.assertEqual(manifest["state"], state)
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertTrue(
                    set(self.engine.INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )

        for previous_state in (..., None, 1, [], {}):
            with self.subTest(fallback=previous_state):
                manifest = self.transaction_manifest(previous_state)

                self.engine.clear_integration_transaction(manifest)

                self.assertEqual(manifest["state"], "preserved")
                self.assertEqual(manifest["unrelated"], "preserved")
                self.assertTrue(
                    set(self.engine.INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )

    def test_transaction_archive_restores_and_preserves_audit_fields(self) -> None:
        archived_fields = {
            "integration_source_head": "last_integration_source_head",
            "integration_target_head": "last_integration_target_head",
            "integration_candidate_head": "last_integration_candidate_head",
            "integration_conflict_paths": "last_integration_conflict_paths",
        }
        timestamp = "2000-01-01T00:00:00+00:00"

        for state in EXPECTED_RUN_STATES:
            with self.subTest(previous_state=state):
                manifest = self.transaction_manifest(state)
                expected = {
                    archived: manifest[current]
                    for current, archived in archived_fields.items()
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
                        for archived in archived_fields.values()
                    },
                    expected,
                )
                self.assertTrue(
                    set(self.engine.INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
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
                    set(self.engine.INTEGRATION_TRANSACTION_FIELDS).isdisjoint(
                        manifest
                    )
                )


if __name__ == "__main__":
    unittest.main()
