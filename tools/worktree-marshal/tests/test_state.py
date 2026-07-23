#!/usr/bin/env python3
"""Direct parity tests for run identity and lexical state paths."""

from __future__ import annotations

import importlib
import inspect
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE_ROOT / "src"


class StatePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))
        cls.state_policy = importlib.import_module("worktree_marshal.state")
        cls.engine = importlib.import_module("worktree_marshal.engine")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def test_state_import_is_engine_free_and_environment_neutral(self) -> None:
        script = (
            "import os, sys; "
            "before = dict(os.environ); "
            f"sys.path.insert(0, {str(SOURCE_ROOT)!r}); "
            "import worktree_marshal.state; "
            "raise SystemExit("
            "'worktree_marshal.engine' in sys.modules "
            "or dict(os.environ) != before"
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

    def test_engine_preserves_run_identity_and_path_surfaces(self) -> None:
        self.assertIs(self.engine.RUN_ID_RE, self.state_policy.RUN_ID_RE)
        for helper_name in (
            "new_run_id",
            "repo_lock_path",
            "run_lock_path",
            "manifest_path",
        ):
            with self.subTest(helper=helper_name):
                self.assertIsNot(
                    getattr(self.engine, helper_name),
                    getattr(self.state_policy, helper_name),
                )

        expected_parameters = {
            "new_run_id": (),
            "repo_lock_path": ("repository",),
            "run_lock_path": ("repository", "run_id"),
            "manifest_path": ("repository", "run_id"),
            "validate_run_id": ("run_id",),
        }
        for helper_name, expected in expected_parameters.items():
            with self.subTest(signature=helper_name):
                parameters = inspect.signature(
                    getattr(self.engine, helper_name)
                ).parameters
                self.assertEqual(tuple(parameters), expected)
                for parameter in parameters.values():
                    self.assertIs(
                        parameter.kind,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                    self.assertIs(parameter.default, inspect.Parameter.empty)

    def test_run_id_grammar_is_exact_and_syntactic(self) -> None:
        self.assertEqual(
            self.state_policy.RUN_ID_RE.pattern,
            r"^[0-9]{8}t[0-9]{6}z-[0-9a-f]{12}$",
        )
        self.assertEqual(self.state_policy.RUN_ID_RE.flags, re.UNICODE)

        valid = (
            "20260723t010203z-000000000000",
            "19991231t235959z-abcdef012345",
            "00000000t000000z-ffffffffffff",
            "99999999t999999z-deadbeefcafe",
        )
        invalid = (
            "",
            "20260723T010203z-000000000000",
            "20260723t010203Z-000000000000",
            "20260723t010203z-ABCDEF012345",
            "2026072t010203z-000000000000",
            "202607230t010203z-000000000000",
            "20260723t01020z-000000000000",
            "20260723t0102030z-000000000000",
            "20260723t010203z-00000000000",
            "20260723t010203z-0000000000000",
            "20260723-010203z-000000000000",
            "20260723t010203-000000000000",
            "20260723t010203z_000000000000",
            "x20260723t010203z-000000000000",
            "20260723t010203z-000000000000x",
            "20260723t010203z-000000000000\n",
            " 20260723t010203z-000000000000",
            "２０２６０７２３t010203z-000000000000",
            "../20260723t010203z-000000000000",
        )
        for run_id in valid:
            with self.subTest(valid=run_id):
                self.assertIsNotNone(
                    self.state_policy.RUN_ID_RE.fullmatch(run_id)
                )
        for run_id in invalid:
            with self.subTest(invalid=run_id):
                self.assertIsNone(
                    self.state_policy.RUN_ID_RE.fullmatch(run_id)
                )

        for value in (None, 17, b"20260723t010203z-000000000000"):
            with self.subTest(non_string=value):
                with self.assertRaises(TypeError):
                    self.state_policy.RUN_ID_RE.fullmatch(value)

    def test_validate_run_id_keeps_engine_regex_and_lazy_diagnostic(
        self,
    ) -> None:
        valid = "20260723t010203z-000000000000"
        with mock.patch.object(
            self.engine,
            "active_profile",
            side_effect=AssertionError("profile acquired for a valid run ID"),
        ) as active_profile:
            self.engine.validate_run_id(valid)
        active_profile.assert_not_called()

        events: list[tuple[str, object]] = []

        class InitialError(RuntimeError):
            pass

        class ExpectedError(RuntimeError):
            pass

        class TooLateError(RuntimeError):
            pass

        def rebound_profile() -> object:
            events.append(("profile", None))
            self.engine.LauncherError = TooLateError
            return SimpleNamespace(display_name="Rebound Marshal")

        class RebindingPattern:
            def fullmatch(pattern_self, run_id: str) -> None:
                events.append(("fullmatch", run_id))
                self.engine.LauncherError = ExpectedError
                self.engine.active_profile = rebound_profile
                return None

        with (
            mock.patch.object(
                self.engine,
                "RUN_ID_RE",
                RebindingPattern(),
            ),
            mock.patch.object(self.engine, "LauncherError", InitialError),
            mock.patch.object(
                self.engine,
                "active_profile",
                side_effect=AssertionError("captured the old profile resolver"),
            ),
        ):
            with self.assertRaisesRegex(
                ExpectedError,
                "^invalid Rebound Marshal run ID$",
            ):
                self.engine.validate_run_id("invalid")

        self.assertEqual(
            events,
            [
                ("fullmatch", "invalid"),
                ("profile", None),
            ],
        )

        for value in (None, 17, b"invalid"):
            with self.subTest(non_string=value):
                with mock.patch.object(
                    self.engine,
                    "active_profile",
                    side_effect=AssertionError(
                        "profile acquired after regex type failure"
                    ),
                ) as active_profile:
                    with self.assertRaises(TypeError):
                        self.engine.validate_run_id(value)
                active_profile.assert_not_called()

    def test_new_run_id_kernel_preserves_exact_operation_order(self) -> None:
        events: list[tuple[str, object]] = []

        class LoweredStamp:
            def __format__(stamp_self, specification: str) -> str:
                events.append(("format-stamp", specification))
                return "20260723t010203z"

        class FormattedStamp:
            def lower(stamp_self) -> object:
                events.append(("lower", None))
                return LoweredStamp()

        class Timestamp:
            def strftime(timestamp_self, format_string: str) -> object:
                events.append(("strftime", format_string))
                return FormattedStamp()

        class RandomSuffix:
            def __format__(suffix_self, specification: str) -> str:
                events.append(("format-suffix", specification))
                return "AbCdEf012345"

        def current_time() -> object:
            events.append(("current-time", None))
            return Timestamp()

        def random_suffix() -> object:
            events.append(("random-suffix", None))
            return RandomSuffix()

        observed = self.state_policy.new_run_id(
            current_time=current_time,
            random_suffix=random_suffix,
        )

        self.assertEqual(observed, "20260723t010203z-AbCdEf012345")
        self.assertEqual(
            events,
            [
                ("current-time", None),
                ("strftime", "%Y%m%dt%H%M%Sz"),
                ("lower", None),
                ("format-stamp", ""),
                ("random-suffix", None),
                ("format-suffix", ""),
            ],
        )

    def test_new_run_id_does_not_consume_entropy_after_stamp_failures(
        self,
    ) -> None:
        class ClockFailure(RuntimeError):
            pass

        class FormatFailure(RuntimeError):
            pass

        class LowerFailure(RuntimeError):
            pass

        class StampRenderFailure(RuntimeError):
            pass

        class BrokenTimestamp:
            def strftime(timestamp_self, format_string: str) -> object:
                raise FormatFailure("format failed")

        class BrokenFormattedStamp:
            def lower(stamp_self) -> object:
                raise LowerFailure("lower failed")

        class LoweringTimestamp:
            def strftime(timestamp_self, format_string: str) -> object:
                return BrokenFormattedStamp()

        class BrokenRenderedStamp:
            def __format__(stamp_self, specification: str) -> str:
                raise StampRenderFailure("stamp rendering failed")

        class RenderingFormattedStamp:
            def lower(stamp_self) -> object:
                return BrokenRenderedStamp()

        class RenderingTimestamp:
            def strftime(timestamp_self, format_string: str) -> object:
                return RenderingFormattedStamp()

        cases = (
            (
                "clock",
                mock.Mock(side_effect=ClockFailure("clock failed")),
                ClockFailure,
                "clock failed",
            ),
            (
                "strftime",
                mock.Mock(return_value=BrokenTimestamp()),
                FormatFailure,
                "format failed",
            ),
            (
                "lower",
                mock.Mock(return_value=LoweringTimestamp()),
                LowerFailure,
                "lower failed",
            ),
            (
                "stamp-render",
                mock.Mock(return_value=RenderingTimestamp()),
                StampRenderFailure,
                "stamp rendering failed",
            ),
        )
        for name, current_time, error_type, message in cases:
            with self.subTest(case=name):
                random_suffix = mock.Mock(
                    side_effect=AssertionError("consumed entropy")
                )
                with self.assertRaisesRegex(error_type, f"^{message}$"):
                    self.state_policy.new_run_id(
                        current_time=current_time,
                        random_suffix=random_suffix,
                    )
                random_suffix.assert_not_called()

    def test_new_run_id_propagates_suffix_failures_without_normalizing(
        self,
    ) -> None:
        class SuffixFailure(RuntimeError):
            pass

        class RenderFailure(RuntimeError):
            pass

        timestamp = SimpleNamespace(
            strftime=lambda format_string: "20260723T010203Z"
        )
        with self.assertRaisesRegex(SuffixFailure, "^suffix failed$"):
            self.state_policy.new_run_id(
                current_time=lambda: timestamp,
                random_suffix=lambda: (_ for _ in ()).throw(
                    SuffixFailure("suffix failed")
                ),
            )

        class BrokenSuffix:
            def __format__(suffix_self, specification: str) -> str:
                raise RenderFailure("suffix rendering failed")

        with self.assertRaisesRegex(
            RenderFailure,
            "^suffix rendering failed$",
        ):
            self.state_policy.new_run_id(
                current_time=lambda: timestamp,
                random_suffix=lambda: BrokenSuffix(),
            )

        observed = self.state_policy.new_run_id(
            current_time=lambda: timestamp,
            random_suffix=lambda: "UPPER/slashed suffix",
        )
        self.assertEqual(
            observed,
            "20260723t010203z-UPPER/slashed suffix",
        )

    def test_engine_new_run_id_resolves_clock_and_entropy_lazily(self) -> None:
        events: list[tuple[str, object]] = []

        class ReboundTimezone:
            @property
            def utc(timezone_self) -> str:
                events.append(("timezone.utc", None))
                return "rebound-utc"

        class InitialTimezone:
            @property
            def utc(timezone_self) -> str:
                raise AssertionError("captured timezone before datetime.now")

        class FormattedStamp:
            def lower(stamp_self) -> str:
                events.append(("lower", None))
                self.engine.secrets = rebound_secrets
                return "20260723t010203z"

        class Timestamp:
            def strftime(timestamp_self, format_string: str) -> object:
                events.append(("strftime", format_string))
                return FormattedStamp()

        def now(utc: object) -> object:
            events.append(("now", utc))
            return Timestamp()

        class DatetimeApi:
            @property
            def now(datetime_self) -> object:
                events.append(("datetime.now", None))
                self.engine.timezone = ReboundTimezone()
                return now

        class InitialSecrets:
            def token_hex(secrets_self, size: int) -> str:
                raise AssertionError("captured secrets before stamp formatting")

        class ReboundSecrets:
            def token_hex(secrets_self, size: int) -> str:
                events.append(("token-hex", size))
                return "ABCDEF012345"

        rebound_secrets = ReboundSecrets()
        with (
            mock.patch.object(self.engine, "datetime", DatetimeApi()),
            mock.patch.object(self.engine, "timezone", InitialTimezone()),
            mock.patch.object(self.engine, "secrets", InitialSecrets()),
        ):
            observed = self.engine.new_run_id()

        self.assertEqual(observed, "20260723t010203z-ABCDEF012345")
        self.assertEqual(
            events,
            [
                ("datetime.now", None),
                ("timezone.utc", None),
                ("now", "rebound-utc"),
                ("strftime", "%Y%m%dt%H%M%Sz"),
                ("lower", None),
                ("token-hex", 6),
            ],
        )

    def test_lexical_path_kernels_preserve_exact_opaque_joins(self) -> None:
        roots = (Path("/state/root"), Path("relative/state"))
        for state_root in roots:
            with self.subTest(root=state_root):
                self.assertEqual(
                    self.state_policy.repo_lock_path(state_root),
                    state_root / "repository.lock",
                )
                self.assertEqual(
                    self.state_policy.run_lock_path(state_root, "run.id"),
                    state_root / "runs" / "run.id.lock",
                )
                self.assertEqual(
                    self.state_policy.manifest_path(state_root, "run.id"),
                    state_root / "runs" / "run.id.json",
                )

        cases = (
            ("", Path("/state/runs/.lock"), Path("/state/runs/.json")),
            (
                "../escape",
                Path("/state/runs/../escape.lock"),
                Path("/state/runs/../escape.json"),
            ),
            (
                "nested/run",
                Path("/state/runs/nested/run.lock"),
                Path("/state/runs/nested/run.json"),
            ),
            (
                "/outside/run",
                Path("/outside/run.lock"),
                Path("/outside/run.json"),
            ),
            (
                " whitespace ",
                Path("/state/runs/ whitespace .lock"),
                Path("/state/runs/ whitespace .json"),
            ),
        )
        for run_id, lock_path, manifest_path in cases:
            with self.subTest(run_id=run_id):
                self.assertEqual(
                    self.state_policy.run_lock_path(Path("/state"), run_id),
                    lock_path,
                )
                self.assertEqual(
                    self.state_policy.manifest_path(
                        Path("/state"),
                        run_id,
                    ),
                    manifest_path,
                )

    def test_path_wrappers_preserve_get_format_and_division_order(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []

        class TracingPath:
            def __init__(path_self, label: str) -> None:
                path_self.label = label

            def __truediv__(
                path_self,
                component: object,
            ) -> object:
                events.append(("divide", (path_self.label, component)))
                if component == "runs":
                    return TracingPath("runs")
                return ("result", path_self.label, component)

        class TracingRunId:
            def __format__(
                run_self,
                specification: str,
            ) -> str:
                events.append(("format-run-id", specification))
                return "opaque.id"

        class RepositoryStub:
            @property
            def state_root(repository_self) -> object:
                events.append(("get-state-root", None))
                return TracingPath("root")

        repository = RepositoryStub()
        run_id = TracingRunId()
        self.assertEqual(
            self.engine.run_lock_path(repository, run_id),
            ("result", "runs", "opaque.id.lock"),
        )
        self.assertEqual(
            events,
            [
                ("get-state-root", None),
                ("divide", ("root", "runs")),
                ("format-run-id", ""),
                ("divide", ("runs", "opaque.id.lock")),
            ],
        )

        events.clear()
        self.assertEqual(
            self.engine.manifest_path(repository, run_id),
            ("result", "runs", "opaque.id.json"),
        )
        self.assertEqual(
            events,
            [
                ("get-state-root", None),
                ("divide", ("root", "runs")),
                ("format-run-id", ""),
                ("divide", ("runs", "opaque.id.json")),
            ],
        )

        events.clear()
        self.assertEqual(
            self.engine.repo_lock_path(repository),
            ("result", "root", "repository.lock"),
        )
        self.assertEqual(
            events,
            [
                ("get-state-root", None),
                ("divide", ("root", "repository.lock")),
            ],
        )

    def test_path_kernel_failures_short_circuit_later_operations(self) -> None:
        class FirstDivisionFailure(RuntimeError):
            pass

        class FormatFailure(RuntimeError):
            pass

        class FinalDivisionFailure(RuntimeError):
            pass

        format_events: list[str] = []

        class UnexpectedFormat:
            def __format__(
                run_self,
                specification: str,
            ) -> str:
                format_events.append(specification)
                raise AssertionError("formatted after first division failed")

        class BrokenRoot:
            def __truediv__(root_self, component: object) -> object:
                raise FirstDivisionFailure("first division failed")

        with self.assertRaisesRegex(
            FirstDivisionFailure,
            "^first division failed$",
        ):
            self.state_policy.run_lock_path(BrokenRoot(), UnexpectedFormat())
        self.assertEqual(format_events, [])

        events: list[str] = []

        class Intermediate:
            def __truediv__(
                intermediate_self,
                component: object,
            ) -> object:
                events.append("final-division")
                raise FinalDivisionFailure("final division failed")

        class Root:
            def __truediv__(root_self, component: object) -> object:
                events.append("first-division")
                return Intermediate()

        class BrokenRunId:
            def __format__(
                run_self,
                specification: str,
            ) -> str:
                events.append("format")
                raise FormatFailure("format failed")

        with self.assertRaisesRegex(FormatFailure, "^format failed$"):
            self.state_policy.manifest_path(Root(), BrokenRunId())
        self.assertEqual(events, ["first-division", "format"])

        events.clear()
        with self.assertRaisesRegex(
            FinalDivisionFailure,
            "^final division failed$",
        ):
            self.state_policy.manifest_path(Root(), "run")
        self.assertEqual(events, ["first-division", "final-division"])

    def test_manifest_selection_retains_validation_boundaries(self) -> None:
        repository = SimpleNamespace(state_root=Path("/state"))
        with (
            mock.patch.object(
                self.engine,
                "active_profile",
                return_value=SimpleNamespace(display_name="Worktree Marshal"),
            ),
            mock.patch.object(
                self.engine,
                "manifest_path",
                side_effect=AssertionError("addressed an invalid run ID"),
            ) as manifest_path,
        ):
            with self.assertRaisesRegex(
                self.engine.LauncherError,
                "^invalid Worktree Marshal run ID$",
            ):
                self.engine.load_manifest(repository, "../escape")
        manifest_path.assert_not_called()

        with tempfile.TemporaryDirectory() as directory:
            state_root = Path(directory)
            runs = state_root / "runs"
            runs.mkdir()
            (runs / "first.json").touch()
            (runs / "second.json").touch()
            events: list[tuple[str, str]] = []

            class FirstPattern:
                def fullmatch(pattern_self, run_id: str) -> bool:
                    events.append(("first", run_id))
                    self.engine.RUN_ID_RE = SecondPattern()
                    return False

            class SecondPattern:
                def fullmatch(pattern_self, run_id: str) -> bool:
                    events.append(("second", run_id))
                    return run_id == "second"

            retained = {
                "run_id": "second",
                "state": "preserved",
            }
            status_repository = SimpleNamespace(
                linked_worktree=False,
                state_root=state_root,
            )
            with (
                mock.patch.object(self.engine, "RUN_ID_RE", FirstPattern()),
                mock.patch.object(self.engine, "initialize_state"),
                mock.patch.object(
                    self.engine,
                    "file_lock",
                    side_effect=lambda path: nullcontext(),
                ),
                mock.patch.object(
                    self.engine,
                    "load_manifest",
                    return_value=retained,
                ) as load_manifest,
                mock.patch.object(self.engine, "reconcile_stale_run"),
                mock.patch.object(
                    self.engine,
                    "run_is_active",
                    return_value=False,
                ),
                mock.patch("builtins.print"),
            ):
                observed = self.engine.show_status(
                    status_repository,
                    None,
                )

            self.assertEqual(observed, 0)
            self.assertEqual(
                events,
                [
                    ("first", "first"),
                    ("second", "second"),
                ],
            )
            load_manifest.assert_called_once_with(
                status_repository,
                "second",
            )


if __name__ == "__main__":
    unittest.main()
