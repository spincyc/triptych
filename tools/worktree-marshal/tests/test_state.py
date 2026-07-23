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

    def test_state_location_kernel_and_engine_wrapper_signatures(self) -> None:
        state_base_parameters = inspect.signature(
            self.state_policy.state_base
        ).parameters
        self.assertEqual(
            tuple(state_base_parameters),
            (
                "profile",
                "environment",
                "path_factory",
                "home",
                "error_type",
            ),
        )
        for parameter in state_base_parameters.values():
            self.assertIs(parameter.kind, inspect.Parameter.KEYWORD_ONLY)
            self.assertIs(parameter.default, inspect.Parameter.empty)

        repository_slug_parameters = inspect.signature(
            self.state_policy.repository_slug
        ).parameters
        self.assertEqual(
            tuple(repository_slug_parameters),
            ("root", "substitute"),
        )
        self.assertIs(
            repository_slug_parameters["root"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        self.assertIs(
            repository_slug_parameters["substitute"].kind,
            inspect.Parameter.KEYWORD_ONLY,
        )
        for parameter in repository_slug_parameters.values():
            self.assertIs(parameter.default, inspect.Parameter.empty)

        expected_engine_parameters = {
            "state_base": (),
            "repository_slug": ("root",),
        }
        for helper_name, expected in expected_engine_parameters.items():
            with self.subTest(engine_wrapper=helper_name):
                self.assertIsNot(
                    getattr(self.engine, helper_name),
                    getattr(self.state_policy, helper_name),
                )
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

    def test_state_base_override_precedes_xdg_and_preserves_order(self) -> None:
        events: list[tuple[str, object]] = []
        result = object()

        class Profile:
            @property
            def state_environment(profile_self) -> str:
                events.append(("profile-state-environment", None))
                return "CUSTOM_STATE"

            @property
            def override_state_suffix(profile_self) -> tuple[str, ...]:
                events.append(("profile-override-suffix", None))
                return ("profiles", "selected")

            @property
            def default_state_parts(profile_self) -> tuple[str, ...]:
                raise AssertionError("read the default suffix after an override")

        class Environment:
            @property
            def get(environment_self) -> object:
                events.append(("resolve-get", None))

                def lookup(name: str) -> str:
                    events.append(("get", name))
                    values = {
                        "CUSTOM_STATE": "/override",
                        "XDG_STATE_HOME": "/xdg",
                    }
                    return values[name]

                return lookup

        class Candidate:
            def is_absolute(candidate_self) -> bool:
                events.append(("is-absolute", None))
                return True

            @property
            def joinpath(candidate_self) -> object:
                events.append(("bind-joinpath", None))

                def join(*parts: str) -> object:
                    events.append(("joinpath", parts))
                    return result

                return join

        def environment() -> object:
            events.append(("environment", None))
            return Environment()

        def path_factory(value: str) -> object:
            events.append(("path-factory", value))
            return Candidate()

        home = mock.Mock(side_effect=AssertionError("used home after override"))
        error_type = mock.Mock(
            side_effect=AssertionError("resolved error type for absolute path")
        )
        observed = self.state_policy.state_base(
            profile=Profile(),
            environment=environment,
            path_factory=path_factory,
            home=home,
            error_type=error_type,
        )

        self.assertIs(observed, result)
        self.assertEqual(
            events,
            [
                ("environment", None),
                ("resolve-get", None),
                ("profile-state-environment", None),
                ("get", "CUSTOM_STATE"),
                ("path-factory", "/override"),
                ("is-absolute", None),
                ("bind-joinpath", None),
                ("profile-override-suffix", None),
                ("joinpath", ("profiles", "selected")),
            ],
        )
        home.assert_not_called()
        error_type.assert_not_called()

    def test_state_base_reacquires_environment_for_xdg_branch(self) -> None:
        events: list[tuple[str, object]] = []
        result = object()

        class Profile:
            @property
            def state_environment(profile_self) -> str:
                events.append(("profile-state-environment", None))
                return "CUSTOM_STATE"

            @property
            def override_state_suffix(profile_self) -> tuple[str, ...]:
                raise AssertionError("read override suffix without an override")

            @property
            def default_state_parts(profile_self) -> tuple[str, ...]:
                events.append(("profile-default-parts", None))
                return ("marshal", "profile")

        class Environment:
            def __init__(
                environment_self,
                label: str,
                values: dict[str, str],
            ) -> None:
                environment_self.label = label
                environment_self.values = values

            def get(environment_self, name: str) -> str | None:
                events.append(
                    ("get", (environment_self.label, name))
                )
                return environment_self.values.get(name)

        environments = iter(
            (
                Environment("first", {"CUSTOM_STATE": ""}),
                Environment("second", {"XDG_STATE_HOME": "/xdg"}),
            )
        )

        def environment() -> object:
            events.append(("environment", None))
            return next(environments)

        class Candidate:
            def is_absolute(candidate_self) -> bool:
                events.append(("is-absolute", None))
                return True

            @property
            def joinpath(candidate_self) -> object:
                events.append(("bind-joinpath", None))

                def join(*parts: str) -> object:
                    events.append(("joinpath", parts))
                    return result

                return join

        def path_factory(value: str) -> object:
            events.append(("path-factory", value))
            return Candidate()

        home = mock.Mock(side_effect=AssertionError("used home after XDG"))
        error_type = mock.Mock(
            side_effect=AssertionError("resolved error type for absolute path")
        )
        observed = self.state_policy.state_base(
            profile=Profile(),
            environment=environment,
            path_factory=path_factory,
            home=home,
            error_type=error_type,
        )

        self.assertIs(observed, result)
        self.assertEqual(
            events,
            [
                ("environment", None),
                ("profile-state-environment", None),
                ("get", ("first", "CUSTOM_STATE")),
                ("environment", None),
                ("get", ("second", "XDG_STATE_HOME")),
                ("path-factory", "/xdg"),
                ("is-absolute", None),
                ("bind-joinpath", None),
                ("profile-default-parts", None),
                ("joinpath", ("marshal", "profile")),
            ],
        )
        home.assert_not_called()
        error_type.assert_not_called()

    def test_state_base_home_fallback_preserves_lexical_join_order(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []
        result = object()

        class Profile:
            @property
            def state_environment(profile_self) -> str:
                events.append(("profile-state-environment", None))
                return "CUSTOM_STATE"

            @property
            def override_state_suffix(profile_self) -> tuple[str, ...]:
                raise AssertionError("read override suffix on home fallback")

            @property
            def default_state_parts(profile_self) -> tuple[str, ...]:
                events.append(("profile-default-parts", None))
                return ("marshal", "profile")

        class Environment:
            def get(environment_self, name: str) -> None:
                events.append(("get", name))
                return None

        def environment() -> object:
            events.append(("environment", None))
            return Environment()

        class TracingPath:
            def __init__(path_self, label: str) -> None:
                path_self.label = label

            def __truediv__(path_self, component: str) -> object:
                events.append(("divide", (path_self.label, component)))
                labels = {
                    ("home", ".local"): "local",
                    ("local", "state"): "state",
                }
                return TracingPath(labels[(path_self.label, component)])

            @property
            def joinpath(path_self) -> object:
                events.append(("bind-joinpath", path_self.label))

                def join(*parts: str) -> object:
                    events.append(
                        ("joinpath", (path_self.label, parts))
                    )
                    return result

                return join

        def home() -> object:
            events.append(("home", None))
            return TracingPath("home")

        path_factory = mock.Mock(
            side_effect=AssertionError("constructed an empty environment value")
        )
        error_type = mock.Mock(
            side_effect=AssertionError("resolved error type on home fallback")
        )
        observed = self.state_policy.state_base(
            profile=Profile(),
            environment=environment,
            path_factory=path_factory,
            home=home,
            error_type=error_type,
        )

        self.assertIs(observed, result)
        self.assertEqual(
            events,
            [
                ("environment", None),
                ("profile-state-environment", None),
                ("get", "CUSTOM_STATE"),
                ("environment", None),
                ("get", "XDG_STATE_HOME"),
                ("home", None),
                ("divide", ("home", ".local")),
                ("divide", ("local", "state")),
                ("bind-joinpath", "state"),
                ("profile-default-parts", None),
                ("joinpath", ("state", ("marshal", "profile"))),
            ],
        )
        path_factory.assert_not_called()
        error_type.assert_not_called()

    def test_state_base_relative_diagnostics_are_exact_and_lazy(self) -> None:
        class RelativeStateError(RuntimeError):
            pass

        cases = (
            (
                "override",
                {
                    "CUSTOM_STATE": "relative/override",
                    "XDG_STATE_HOME": "/unused",
                },
                "CUSTOM_STATE must be an absolute path",
            ),
            (
                "xdg",
                {
                    "CUSTOM_STATE": "",
                    "XDG_STATE_HOME": "relative/xdg",
                },
                "XDG_STATE_HOME must be an absolute path",
            ),
        )
        for name, values, expected_message in cases:
            with self.subTest(branch=name):
                events: list[tuple[str, object]] = []

                class Profile:
                    @property
                    def state_environment(profile_self) -> str:
                        events.append(
                            ("profile-state-environment", None)
                        )
                        return "CUSTOM_STATE"

                    @property
                    def override_state_suffix(
                        profile_self,
                    ) -> tuple[str, ...]:
                        raise AssertionError("read suffix for a relative path")

                    @property
                    def default_state_parts(
                        profile_self,
                    ) -> tuple[str, ...]:
                        raise AssertionError("read suffix for a relative path")

                class Candidate:
                    def is_absolute(candidate_self) -> bool:
                        events.append(("is-absolute", None))
                        return False

                    def joinpath(
                        candidate_self,
                        *parts: str,
                    ) -> object:
                        raise AssertionError("joined a relative state path")

                def environment() -> object:
                    events.append(("environment", None))
                    return values

                def path_factory(value: str) -> object:
                    events.append(("path-factory", value))
                    return Candidate()

                def error_type() -> type[Exception]:
                    events.append(("error-type", None))
                    return RelativeStateError

                home = mock.Mock(
                    side_effect=AssertionError(
                        "used home after a relative configured path"
                    )
                )
                with self.assertRaisesRegex(
                    RelativeStateError,
                    f"^{re.escape(expected_message)}$",
                ):
                    self.state_policy.state_base(
                        profile=Profile(),
                        environment=environment,
                        path_factory=path_factory,
                        home=home,
                        error_type=error_type,
                    )

                expected_environment_calls = 1 if name == "override" else 2
                self.assertEqual(
                    sum(
                        event == ("environment", None)
                        for event in events
                    ),
                    expected_environment_calls,
                )
                expected_profile_reads = 2 if name == "override" else 1
                self.assertEqual(
                    sum(
                        event == ("profile-state-environment", None)
                        for event in events
                    ),
                    expected_profile_reads,
                )
                expected_tail = [
                    ("is-absolute", None),
                    ("error-type", None),
                ]
                if name == "override":
                    expected_tail.append(
                        ("profile-state-environment", None)
                    )
                self.assertEqual(
                    events[-len(expected_tail) :],
                    expected_tail,
                )
                home.assert_not_called()

    def test_state_base_failures_short_circuit_later_providers(self) -> None:
        class ProviderFailure(RuntimeError):
            pass

        profile = SimpleNamespace(
            state_environment="CUSTOM_STATE",
            override_state_suffix=("override",),
            default_state_parts=("default",),
        )
        unused_path_factory = mock.Mock(
            side_effect=AssertionError("called path factory after failure")
        )
        unused_home = mock.Mock(
            side_effect=AssertionError("called home after failure")
        )
        unused_error_type = mock.Mock(
            side_effect=AssertionError("called error type after failure")
        )

        with self.assertRaisesRegex(
            ProviderFailure,
            "^environment failed$",
        ):
            self.state_policy.state_base(
                profile=profile,
                environment=mock.Mock(
                    side_effect=ProviderFailure("environment failed")
                ),
                path_factory=unused_path_factory,
                home=unused_home,
                error_type=unused_error_type,
            )
        unused_path_factory.assert_not_called()
        unused_home.assert_not_called()
        unused_error_type.assert_not_called()

        path_failure = mock.Mock(
            side_effect=ProviderFailure("path construction failed")
        )
        with self.assertRaisesRegex(
            ProviderFailure,
            "^path construction failed$",
        ):
            self.state_policy.state_base(
                profile=profile,
                environment=lambda: {"CUSTOM_STATE": "/override"},
                path_factory=path_failure,
                home=unused_home,
                error_type=unused_error_type,
            )
        path_failure.assert_called_once_with("/override")
        unused_home.assert_not_called()
        unused_error_type.assert_not_called()

        class AbsoluteFailure:
            def is_absolute(candidate_self) -> bool:
                raise ProviderFailure("absolute check failed")

        with self.assertRaisesRegex(
            ProviderFailure,
            "^absolute check failed$",
        ):
            self.state_policy.state_base(
                profile=profile,
                environment=lambda: {"CUSTOM_STATE": "/override"},
                path_factory=lambda value: AbsoluteFailure(),
                home=unused_home,
                error_type=unused_error_type,
            )
        unused_home.assert_not_called()
        unused_error_type.assert_not_called()

        environment_calls = 0

        def changing_environment() -> dict[str, str]:
            nonlocal environment_calls
            environment_calls += 1
            if environment_calls == 1:
                return {"CUSTOM_STATE": ""}
            raise ProviderFailure("second environment failed")

        with self.assertRaisesRegex(
            ProviderFailure,
            "^second environment failed$",
        ):
            self.state_policy.state_base(
                profile=profile,
                environment=changing_environment,
                path_factory=unused_path_factory,
                home=unused_home,
                error_type=unused_error_type,
            )
        self.assertEqual(environment_calls, 2)
        unused_home.assert_not_called()

        default_reads = 0

        class FallbackProfile:
            state_environment = "CUSTOM_STATE"

            @property
            def default_state_parts(
                profile_self,
            ) -> tuple[str, ...]:
                nonlocal default_reads
                default_reads += 1
                return ("default",)

        with self.assertRaisesRegex(ProviderFailure, "^home failed$"):
            self.state_policy.state_base(
                profile=FallbackProfile(),
                environment=lambda: {},
                path_factory=unused_path_factory,
                home=mock.Mock(
                    side_effect=ProviderFailure("home failed")
                ),
                error_type=unused_error_type,
            )
        self.assertEqual(default_reads, 0)

    def test_engine_state_base_defers_mutable_runtime_providers(self) -> None:
        events: list[tuple[str, object]] = []
        profile = object()
        result = object()

        class EnvironmentApi:
            def __init__(api_self, label: str) -> None:
                api_self.label = label

            @property
            def environ(api_self) -> object:
                events.append(("environment", api_self.label))
                return ("environment", api_self.label)

        class PathApi:
            def __init__(api_self, label: str) -> None:
                api_self.label = label

            def __call__(api_self, value: str) -> object:
                events.append(("path-factory", (api_self.label, value)))
                return ("path", api_self.label, value)

            def home(api_self) -> object:
                events.append(("home", api_self.label))
                return ("home", api_self.label)

        class InitialError(RuntimeError):
            pass

        class ReboundError(RuntimeError):
            pass

        initial_os = EnvironmentApi("initial")
        rebound_os = EnvironmentApi("rebound")
        initial_path = PathApi("initial")
        rebound_path = PathApi("rebound")

        def active_profile() -> object:
            events.append(("active-profile", None))
            self.engine.os = rebound_os
            self.engine.Path = rebound_path
            self.engine.LauncherError = ReboundError
            return profile

        def state_base_kernel(**providers: object) -> object:
            events.append(("kernel", tuple(providers)))
            self.assertIs(providers["profile"], profile)
            self.assertEqual(
                providers["environment"](),
                ("environment", "rebound"),
            )
            self.assertEqual(
                providers["path_factory"]("configured"),
                ("path", "rebound", "configured"),
            )
            self.assertEqual(
                providers["home"](),
                ("home", "rebound"),
            )
            self.assertIs(providers["error_type"](), ReboundError)
            return result

        with (
            mock.patch.object(self.engine, "os", initial_os),
            mock.patch.object(self.engine, "Path", initial_path),
            mock.patch.object(self.engine, "LauncherError", InitialError),
            mock.patch.object(
                self.engine,
                "active_profile",
                side_effect=active_profile,
            ),
            mock.patch.object(
                self.engine,
                "_state_base",
                side_effect=state_base_kernel,
            ),
        ):
            observed = self.engine.state_base()

        self.assertIs(observed, result)
        self.assertEqual(
            events,
            [
                ("active-profile", None),
                (
                    "kernel",
                    (
                        "profile",
                        "environment",
                        "path_factory",
                        "home",
                        "error_type",
                    ),
                ),
                ("environment", "rebound"),
                ("path-factory", ("rebound", "configured")),
                ("home", "rebound"),
            ],
        )

    def test_engine_state_base_real_kernel_resolves_providers_at_use(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []

        class InitialError(RuntimeError):
            pass

        class ReboundError(RuntimeError):
            pass

        class Profile:
            @property
            def state_environment(profile_self) -> str:
                events.append(("profile-state-environment", None))
                return "CUSTOM_STATE"

            @property
            def override_state_suffix(
                profile_self,
            ) -> tuple[str, ...]:
                raise AssertionError("read override suffix for a falsey value")

            @property
            def default_state_parts(
                profile_self,
            ) -> tuple[str, ...]:
                raise AssertionError("read default suffix for a relative path")

        class ReboundEnvironment:
            def get(environment_self, name: str) -> object:
                events.append(("rebound-get", name))
                if name != "XDG_STATE_HOME":
                    raise AssertionError(f"unexpected rebound lookup: {name}")
                return xdg_value

        class ReboundOs:
            @property
            def environ(api_self) -> object:
                events.append(("rebound-environment", None))
                return ReboundEnvironment()

        class FalseyOverride:
            def __bool__(value_self) -> bool:
                events.append(("override-truthiness", None))
                self.engine.os = ReboundOs()
                return False

        class InitialEnvironment:
            def get(environment_self, name: str) -> object:
                events.append(("initial-get", name))
                if name != "CUSTOM_STATE":
                    raise AssertionError(f"reused initial environment: {name}")
                return FalseyOverride()

        class InitialOs:
            @property
            def environ(api_self) -> object:
                events.append(("initial-environment", None))
                return InitialEnvironment()

        class Candidate:
            def is_absolute(candidate_self) -> bool:
                events.append(("is-absolute", None))
                self.engine.LauncherError = ReboundError
                return False

        class ReboundPath:
            def __call__(path_self, value: object) -> object:
                events.append(("rebound-path", value))
                self.assertIs(value, xdg_value)
                return Candidate()

            def home(path_self) -> object:
                raise AssertionError("used home after a truthy XDG value")

        class InitialPath:
            def __call__(path_self, value: object) -> object:
                raise AssertionError("captured Path before XDG truthiness")

            def home(path_self) -> object:
                raise AssertionError("used home after a truthy XDG value")

        class TruthyXdg:
            def __bool__(value_self) -> bool:
                events.append(("xdg-truthiness", None))
                self.engine.Path = ReboundPath()
                return True

        xdg_value = TruthyXdg()

        def active_profile() -> object:
            events.append(("active-profile", None))
            return Profile()

        with (
            mock.patch.object(
                self.engine,
                "active_profile",
                side_effect=active_profile,
            ),
            mock.patch.object(self.engine, "os", InitialOs()),
            mock.patch.object(self.engine, "Path", InitialPath()),
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialError,
            ),
        ):
            with self.assertRaisesRegex(
                ReboundError,
                "^XDG_STATE_HOME must be an absolute path$",
            ):
                self.engine.state_base()

        self.assertEqual(
            events,
            [
                ("active-profile", None),
                ("initial-environment", None),
                ("profile-state-environment", None),
                ("initial-get", "CUSTOM_STATE"),
                ("override-truthiness", None),
                ("rebound-environment", None),
                ("rebound-get", "XDG_STATE_HOME"),
                ("xdg-truthiness", None),
                ("rebound-path", xdg_value),
                ("is-absolute", None),
            ],
        )

    def test_engine_override_error_is_captured_before_diagnostic_name(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []

        class ExpectedError(RuntimeError):
            pass

        class TooLateError(RuntimeError):
            pass

        class Profile:
            reads = 0

            @property
            def state_environment(profile_self) -> str:
                profile_self.reads += 1
                events.append(
                    ("profile-state-environment", profile_self.reads)
                )
                if profile_self.reads == 2:
                    self.engine.LauncherError = TooLateError
                return "CUSTOM_STATE"

            @property
            def override_state_suffix(
                profile_self,
            ) -> tuple[str, ...]:
                raise AssertionError("read suffix for a relative override")

        class Candidate:
            def is_absolute(candidate_self) -> bool:
                events.append(("is-absolute", None))
                return False

        class PathApi:
            def __call__(path_self, value: str) -> object:
                events.append(("path", value))
                return Candidate()

        with (
            mock.patch.object(
                self.engine,
                "active_profile",
                return_value=Profile(),
            ),
            mock.patch.object(
                self.engine,
                "os",
                SimpleNamespace(
                    environ={"CUSTOM_STATE": "relative/path"}
                ),
            ),
            mock.patch.object(self.engine, "Path", PathApi()),
            mock.patch.object(
                self.engine,
                "LauncherError",
                ExpectedError,
            ),
        ):
            with self.assertRaisesRegex(
                ExpectedError,
                "^CUSTOM_STATE must be an absolute path$",
            ):
                self.engine.state_base()

        self.assertEqual(
            events,
            [
                ("profile-state-environment", 1),
                ("path", "relative/path"),
                ("is-absolute", None),
                ("profile-state-environment", 2),
            ],
        )

    def test_repository_slug_normalization_is_exactly_ascii(self) -> None:
        cases = (
            ("Triptych", "triptych"),
            ("Hello_World.git", "hello-world-git"),
            ("a..B__C", "a-b-c"),
            ("123 Project 456", "123-project-456"),
            ("Église Café", "glise-caf"),
            ("Straße", "stra-e"),
            ("Καλημέρα", "repository"),
            ("ＦＯＯ", "repository"),
            ("---", "repository"),
            ("", "repository"),
        )
        for name, expected in cases:
            with self.subTest(name=name):
                observed = self.state_policy.repository_slug(
                    SimpleNamespace(name=name),
                    substitute=re.sub,
                )
                self.assertEqual(observed, expected)

    def test_repository_slug_kernel_preserves_operation_order(self) -> None:
        events: list[tuple[str, object]] = []
        truthy_result = object()

        class Slug:
            def strip(slug_self, characters: str) -> object:
                events.append(("strip", characters))
                return truthy_result

        class LoweredName:
            def __format__(
                name_self,
                specification: str,
            ) -> str:
                raise AssertionError("formatted repository name")

        class Name:
            def lower(name_self) -> object:
                events.append(("lower", None))
                return LoweredName()

        class Root:
            @property
            def name(root_self) -> object:
                events.append(("root-name", None))
                return Name()

        def substitute(
            pattern: str,
            replacement: str,
            value: object,
        ) -> object:
            events.append(
                ("substitute", (pattern, replacement, value.__class__))
            )
            return Slug()

        observed = self.state_policy.repository_slug(
            Root(),
            substitute=substitute,
        )

        self.assertIs(observed, truthy_result)
        self.assertEqual(
            events,
            [
                ("root-name", None),
                ("lower", None),
                (
                    "substitute",
                    (r"[^a-z0-9]+", "-", LoweredName),
                ),
                ("strip", "-"),
            ],
        )

        self.assertEqual(
            self.state_policy.repository_slug(
                SimpleNamespace(name="---"),
                substitute=re.sub,
            ),
            "repository",
        )

    def test_repository_slug_failures_propagate_without_fallback(self) -> None:
        class SlugFailure(RuntimeError):
            pass

        class BrokenRoot:
            @property
            def name(root_self) -> str:
                raise SlugFailure("name failed")

        substitute = mock.Mock(
            side_effect=AssertionError("substituted after name failure")
        )
        with self.assertRaisesRegex(SlugFailure, "^name failed$"):
            self.state_policy.repository_slug(
                BrokenRoot(),
                substitute=substitute,
            )
        substitute.assert_not_called()

        class BrokenName:
            def lower(name_self) -> str:
                raise SlugFailure("lower failed")

        substitute.reset_mock()
        with self.assertRaisesRegex(SlugFailure, "^lower failed$"):
            self.state_policy.repository_slug(
                SimpleNamespace(name=BrokenName()),
                substitute=substitute,
            )
        substitute.assert_not_called()

        with self.assertRaisesRegex(SlugFailure, "^substitute failed$"):
            self.state_policy.repository_slug(
                SimpleNamespace(name="repository"),
                substitute=mock.Mock(
                    side_effect=SlugFailure("substitute failed")
                ),
            )

        class BrokenSlug:
            def strip(slug_self, characters: str) -> str:
                raise SlugFailure("strip failed")

        with self.assertRaisesRegex(SlugFailure, "^strip failed$"):
            self.state_policy.repository_slug(
                SimpleNamespace(name="repository"),
                substitute=lambda pattern, replacement, value: BrokenSlug(),
            )

    def test_engine_repository_slug_captures_substitute_before_root_name(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []

        def initial_substitute(
            pattern: str,
            replacement: str,
            value: str,
        ) -> str:
            events.append(
                ("initial-substitute", (pattern, replacement, value))
            )
            return re.sub(pattern, replacement, value)

        class InitialRegexApi:
            @property
            def sub(api_self) -> object:
                events.append(("capture-substitute", None))
                return initial_substitute

        class ReboundRegexApi:
            @property
            def sub(api_self) -> object:
                raise AssertionError(
                    "resolved substitute after reading the repository name"
                )

        class Root:
            @property
            def name(root_self) -> str:
                events.append(("root-name", None))
                self.engine.re = ReboundRegexApi()
                return "Project Name"

        with mock.patch.object(self.engine, "re", InitialRegexApi()):
            observed = self.engine.repository_slug(Root())

        self.assertEqual(observed, "project-name")
        self.assertEqual(
            events,
            [
                ("capture-substitute", None),
                ("root-name", None),
                (
                    "initial-substitute",
                    (r"[^a-z0-9]+", "-", "project name"),
                ),
            ],
        )

    def test_discover_repository_keeps_state_outside_security_boundary(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []
        start = Path("/repository/subdirectory")
        root = Path("/repository")
        git_dir = Path("/repository/.git")
        common_git_dir = Path("/repository/.git")

        def git(
            cwd: Path,
            *arguments: str,
            check: bool = True,
        ) -> object:
            events.append(("git", (cwd, arguments, check)))
            outputs = {
                ("rev-parse", "--is-inside-work-tree"): "true\n",
                ("rev-parse", "--show-toplevel"): f"{root}\n",
            }
            return SimpleNamespace(
                returncode=0,
                stdout=outputs[arguments],
            )

        def absolute_git_path(cwd: Path, selector: str) -> Path:
            events.append(("absolute-git-path", (cwd, selector)))
            paths = {
                "--git-dir": git_dir,
                "--git-common-dir": common_git_dir,
            }
            return paths[selector]

        class OperatingSystemApi:
            def fsencode(api_self, value: object) -> bytes:
                events.append(("fsencode", value))
                return b"common-git-directory"

        class Digest:
            def hexdigest(digest_self) -> str:
                events.append(("hexdigest", None))
                return "0123456789abcdef"

        class HashApi:
            def sha256(api_self, value: bytes) -> object:
                events.append(("sha256", value))
                return Digest()

        class Profile:
            @property
            def state_environment(profile_self) -> str:
                events.append(("profile-state-environment", None))
                return "CUSTOM_STATE"

        def state_base() -> Path:
            events.append(("state-base", None))
            return root / ".marshal-state"

        def repository_slug(discovered_root: Path) -> str:
            events.append(("repository-slug", discovered_root))
            return "project"

        def active_profile() -> object:
            events.append(("active-profile", None))
            return Profile()

        with (
            mock.patch.object(self.engine, "git", side_effect=git),
            mock.patch.object(
                self.engine,
                "absolute_git_path",
                side_effect=absolute_git_path,
            ),
            mock.patch.object(self.engine, "os", OperatingSystemApi()),
            mock.patch.object(self.engine, "hashlib", HashApi()),
            mock.patch.object(
                self.engine,
                "state_base",
                side_effect=state_base,
            ),
            mock.patch.object(
                self.engine,
                "repository_slug",
                side_effect=repository_slug,
            ),
            mock.patch.object(
                self.engine,
                "active_profile",
                side_effect=active_profile,
            ),
            mock.patch.object(
                self.engine,
                "Repository",
                side_effect=AssertionError(
                    "constructed a repository with state inside its worktree"
                ),
            ) as repository_type,
        ):
            with self.assertRaisesRegex(
                self.engine.LauncherError,
                "^CUSTOM_STATE must keep launcher state outside the worktree$",
            ):
                self.engine.discover_repository(start)

        repository_type.assert_not_called()
        self.assertEqual(
            events,
            [
                (
                    "git",
                    (
                        start,
                        ("rev-parse", "--is-inside-work-tree"),
                        False,
                    ),
                ),
                (
                    "git",
                    (
                        start,
                        ("rev-parse", "--show-toplevel"),
                        True,
                    ),
                ),
                ("absolute-git-path", (root, "--git-dir")),
                ("absolute-git-path", (root, "--git-common-dir")),
                ("fsencode", common_git_dir),
                ("sha256", b"common-git-directory"),
                ("hexdigest", None),
                ("state-base", None),
                ("repository-slug", root),
                ("active-profile", None),
                ("profile-state-environment", None),
            ],
        )

    def test_discover_repository_rejects_outside_cwd_before_state_policy(
        self,
    ) -> None:
        start = Path("/outside")
        root = Path("/repository")
        git_outputs = iter(
            (
                SimpleNamespace(returncode=0, stdout="true\n"),
                SimpleNamespace(returncode=0, stdout=f"{root}\n"),
            )
        )
        state_base = mock.Mock(
            side_effect=AssertionError(
                "selected state before authenticating the discovered root"
            )
        )
        repository_slug = mock.Mock(
            side_effect=AssertionError(
                "slugged a root before checking the current directory"
            )
        )
        with (
            mock.patch.object(
                self.engine,
                "git",
                side_effect=lambda *args, **kwargs: next(git_outputs),
            ),
            mock.patch.object(
                self.engine,
                "absolute_git_path",
                side_effect=(
                    Path("/repository/.git"),
                    Path("/repository/.git"),
                ),
            ),
            mock.patch.object(self.engine, "state_base", state_base),
            mock.patch.object(
                self.engine,
                "repository_slug",
                repository_slug,
            ),
            mock.patch.object(
                self.engine.hashlib,
                "sha256",
                side_effect=AssertionError(
                    "hashed state identity before relative-cwd validation"
                ),
            ),
        ):
            with self.assertRaisesRegex(
                self.engine.LauncherError,
                "^the current directory is outside the discovered worktree$",
            ):
                self.engine.discover_repository(start)

        state_base.assert_not_called()
        repository_slug.assert_not_called()

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
