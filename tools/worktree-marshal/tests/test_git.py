#!/usr/bin/env python3
"""Direct parity tests for the extracted Git policy seam."""

from __future__ import annotations

import importlib
import inspect
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE_ROOT / "src"
EXPECTED_UNSAFE_GIT_ENV = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_ASKPASS",
        "GIT_ATTR_GLOBAL",
        "GIT_ATTR_SOURCE",
        "GIT_ATTR_SYSTEM",
        "GIT_CEILING_DIRECTORIES",
        "GIT_COMMON_DIR",
        "GIT_CONFIG",
        "GIT_CONFIG_COUNT",
        "GIT_CONFIG_GLOBAL",
        "GIT_CONFIG_NOSYSTEM",
        "GIT_CONFIG_PARAMETERS",
        "GIT_CONFIG_SYSTEM",
        "GIT_DIFF_OPTS",
        "GIT_DIR",
        "GIT_DISCOVERY_ACROSS_FILESYSTEM",
        "GIT_EDITOR",
        "GIT_EXEC_PATH",
        "GIT_EXTERNAL_DIFF",
        "GIT_EXTERNAL_DIFF_TRUST_EXIT_CODE",
        "GIT_GLOB_PATHSPECS",
        "GIT_GRAFT_FILE",
        "GIT_ICASE_PATHSPECS",
        "GIT_IMPLICIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_LITERAL_PATHSPECS",
        "GIT_MERGE_AUTOEDIT",
        "GIT_NAMESPACE",
        "GIT_NOGLOB_PATHSPECS",
        "GIT_NO_REPLACE_OBJECTS",
        "GIT_OBJECT_DIRECTORY",
        "GIT_OPTIONAL_LOCKS",
        "GIT_PREFIX",
        "GIT_PROXY_COMMAND",
        "GIT_QUARANTINE_PATH",
        "GIT_REDIRECT_STDERR",
        "GIT_REDIRECT_STDIN",
        "GIT_REDIRECT_STDOUT",
        "GIT_REPLACE_REF_BASE",
        "GIT_SEQUENCE_EDITOR",
        "GIT_SHALLOW_FILE",
        "GIT_SHELL_PATH",
        "GIT_SSH",
        "GIT_SSH_COMMAND",
        "GIT_SSH_VARIANT",
        "GIT_TEMPLATE_DIR",
        "GIT_WORK_TREE",
    }
)


class GitPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))
        cls.policy = importlib.import_module("worktree_marshal.git")
        cls.engine = importlib.import_module("worktree_marshal.engine")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def validate_output(
        self,
        output: bytes,
        *,
        boolean_values: set[str] | None = None,
        command_config_pattern: re.Pattern[str] | None = None,
    ) -> None:
        class PolicyError(RuntimeError):
            pass

        self.policy.validate_effective_git_configuration(
            output,
            error_type=lambda: PolicyError,
            boolean_values=lambda: (
                self.policy.GIT_BOOLEAN_VALUES
                if boolean_values is None
                else boolean_values
            ),
            command_config_pattern=lambda: (
                self.policy.GIT_COMMAND_CONFIG_RE
                if command_config_pattern is None
                else command_config_pattern
            ),
        )

    def test_policy_import_does_not_load_the_lifecycle_engine(self) -> None:
        script = (
            "import os, sys; "
            "before = dict(os.environ); "
            f"sys.path.insert(0, {str(SOURCE_ROOT)!r}); "
            "import worktree_marshal.git; "
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

    def test_engine_preserves_the_existing_policy_surface(self) -> None:
        self.assertIs(
            self.engine.hardened_git_arguments,
            self.policy.hardened_git_arguments,
        )
        self.assertIs(self.engine.GIT_BASE_ARGUMENTS, self.policy.GIT_BASE_ARGUMENTS)
        self.assertIs(
            self.engine.GIT_BOOLEAN_VALUES,
            self.policy.GIT_BOOLEAN_VALUES,
        )
        self.assertIs(
            self.engine.GIT_COMMAND_CONFIG_RE,
            self.policy.GIT_COMMAND_CONFIG_RE,
        )
        self.assertIs(
            self.engine.GIT_INDEXED_CONFIG_ENV_RE,
            self.policy.GIT_INDEXED_CONFIG_ENV_RE,
        )
        self.assertIs(self.engine.GIT_UNSAFE_ENV, self.policy.GIT_UNSAFE_ENV)
        self.assertIsNot(
            self.engine.validate_effective_git_configuration,
            self.policy.validate_effective_git_configuration,
        )
        parameters = inspect.signature(
            self.engine.validate_effective_git_configuration
        ).parameters
        self.assertEqual(tuple(parameters), ("cwd",))
        self.assertIs(
            parameters["cwd"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        self.assertIs(parameters["cwd"].default, inspect.Parameter.empty)
        source = {"KEEP": "yes", "GIT_DIR": "/hostile"}
        self.assertEqual(
            self.engine.sanitized_git_environment(source),
            self.policy.sanitized_git_environment(source),
        )

    def test_engine_wrapper_preserves_rebound_policy_globals(self) -> None:
        source = {
            "CUSTOM_UNSAFE": "remove",
            "CUSTOM_INDEXED": "remove",
            "GIT_CONFIG_KEY_0": "preserve",
            "GIT_DIR": "preserve",
        }
        with (
            mock.patch.object(
                self.engine,
                "GIT_UNSAFE_ENV",
                {"CUSTOM_UNSAFE"},
            ),
            mock.patch.object(
                self.engine,
                "GIT_INDEXED_CONFIG_ENV_RE",
                re.compile(r"^CUSTOM_INDEXED$"),
            ),
        ):
            observed = self.engine.sanitized_git_environment(source)

        self.assertNotIn("CUSTOM_UNSAFE", observed)
        self.assertNotIn("CUSTOM_INDEXED", observed)
        self.assertEqual(observed["GIT_CONFIG_KEY_0"], "preserve")
        self.assertEqual(observed["GIT_DIR"], "preserve")

    def test_sanitized_environment_is_a_repeatable_copy(self) -> None:
        forced = {
            "EDITOR": ":",
            "GIT_ATTR_GLOBAL": os.devnull,
            "GIT_ATTR_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_EDITOR": ":",
            "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_OPTIONAL_LOCKS": "1",
            "GIT_PAGER": "",
            "GIT_SEQUENCE_EDITOR": ":",
            "GIT_TERMINAL_PROMPT": "0",
            "VISUAL": ":",
        }
        self.assertIs(type(self.policy.GIT_UNSAFE_ENV), set)
        self.assertEqual(self.policy.GIT_UNSAFE_ENV, EXPECTED_UNSAFE_GIT_ENV)
        source = {name: "hostile" for name in EXPECTED_UNSAFE_GIT_ENV}
        source.update(
            {
                "CDPATH": "/hostile",
                "GIT_CONFIG_KEY_0": "core.fsmonitor",
                "GIT_CONFIG_VALUE_0": "/hostile",
                "GIT_CONFIG_KEY_27": "filter.hostile.process",
                "GIT_CONFIG_VALUE_27": "/hostile",
                "GIT_TEST_FAKE": "1",
                "GIT_TRACE": "1",
                "GIT_TRACE2_EVENT": "/hostile",
                "SSH_ASKPASS": "/hostile",
                "KEEP": "yes",
                "GIT_CONFIG_KEY_x": "preserved-near-miss",
                "GIT_TEST": "preserved-near-miss",
                "GIT_TRAC": "preserved-near-miss",
            }
        )
        original = source.copy()

        first = self.policy.sanitized_git_environment(source)
        second = self.policy.sanitized_git_environment(source)

        self.assertEqual(source, original)
        self.assertIsNot(first, source)
        self.assertEqual(first, second)
        self.assertEqual({name: first[name] for name in forced}, forced)
        self.assertEqual(first["KEEP"], "yes")
        self.assertEqual(first["GIT_CONFIG_KEY_x"], "preserved-near-miss")
        self.assertEqual(first["GIT_TEST"], "preserved-near-miss")
        self.assertEqual(first["GIT_TRAC"], "preserved-near-miss")
        removed = (
            (EXPECTED_UNSAFE_GIT_ENV - forced.keys())
            | {
                "CDPATH",
                "GIT_CONFIG_KEY_0",
                "GIT_CONFIG_VALUE_0",
                "GIT_CONFIG_KEY_27",
                "GIT_CONFIG_VALUE_27",
                "GIT_TEST_FAKE",
                "GIT_TRACE",
                "GIT_TRACE2_EVENT",
                "SSH_ASKPASS",
            }
        )
        self.assertTrue(removed.isdisjoint(first), removed.intersection(first))

    def test_engine_wrapper_preserves_default_environment_acquisition(self) -> None:
        source = {
            "KEEP": "yes",
            "GIT_DIR": "/hostile",
        }
        with mock.patch.dict(os.environ, source, clear=True):
            observed = self.engine.sanitized_git_environment()

        self.assertEqual(observed["KEEP"], "yes")
        self.assertNotIn("GIT_DIR", observed)
        self.assertEqual(observed["GIT_TERMINAL_PROMPT"], "0")

    def test_base_arguments_are_frozen(self) -> None:
        self.assertEqual(
            self.policy.GIT_BASE_ARGUMENTS,
            (
                "--no-replace-objects",
                "-c",
                "core.hooksPath=/dev/null",
                "-c",
                "commit.gpgSign=false",
                "-c",
                "tag.gpgSign=false",
                "-c",
                "core.editor=:",
                "-c",
                "sequence.editor=:",
            ),
        )

    def test_effective_configuration_policy_is_frozen(self) -> None:
        dangerous = (
            "filter.example.clean",
            "filter.example.smudge",
            "filter.example.process",
            "merge.example.driver",
            "diff.external",
            "diff.example.command",
            "diff.example.textconv",
            "FILTER.EXAMPLE.PROCESS",
        )
        benign = (
            "core.editor",
            "filter.example.required",
            "merge.example.name",
            "diff.example.binary",
        )

        for name in dangerous:
            with self.subTest(dangerous=name):
                self.assertIsNotNone(self.policy.GIT_COMMAND_CONFIG_RE.fullmatch(name))
        for name in benign:
            with self.subTest(benign=name):
                self.assertIsNone(self.policy.GIT_COMMAND_CONFIG_RE.fullmatch(name))
        self.assertEqual(
            self.policy.GIT_BOOLEAN_VALUES,
            {"", "0", "1", "false", "no", "off", "on", "true", "yes"},
        )

    def test_effective_configuration_accepts_boolean_and_benign_values(
        self,
    ) -> None:
        accepted = (
            "",
            " ",
            "0",
            "1",
            "false",
            "no",
            "off",
            "on",
            "true",
            "yes",
            " TRUE ",
            "\tNo\n",
        )
        for value in accepted:
            with self.subTest(fsmonitor=value):
                output = (
                    b"core.editor\nvim\0"
                    b"filter.example.required\ntrue\0"
                    b"filter.example.process\n \t\0"
                    b"core.fsmonitor\n"
                    + value.encode()
                    + b"\0"
                )
                self.validate_output(output)

        self.validate_output(b"\0\0")
        self.validate_output(b"benign.key\nfirst\nsecond\0")
        self.validate_output(b"benign.key\nvalue-without-trailing-nul")

    def test_effective_configuration_rejects_malformed_records(self) -> None:
        malformed = (
            b"missing-separator",
            b"\nmissing-key",
            b"valid.key\nvalue\0missing-separator",
        )
        for output in malformed:
            with self.subTest(output=output):
                with self.assertRaisesRegex(
                    RuntimeError,
                    "^Git returned malformed effective configuration$",
                ):
                    self.validate_output(output)

    def test_effective_configuration_rejects_command_bearing_values(
        self,
    ) -> None:
        cases = (
            (
                b"core.fsmonitor\n/bin/command\0",
                "unsafe command-bearing Git configuration 'core.fsmonitor'",
            ),
            (
                b"FILTER.EXAMPLE.CLEAN\n/bin/command\0",
                "unsafe command-bearing Git configuration 'filter.example.clean'",
            ),
            (
                b"filter.example.smudge\n/bin/command\0",
                "unsafe command-bearing Git configuration 'filter.example.smudge'",
            ),
            (
                b"filter.example.process\n/bin/command\0",
                "unsafe command-bearing Git configuration 'filter.example.process'",
            ),
            (
                b"merge.example.driver\n/bin/command\0",
                "unsafe command-bearing Git configuration 'merge.example.driver'",
            ),
            (
                b"diff.external\n/bin/command\0",
                "unsafe command-bearing Git configuration 'diff.external'",
            ),
            (
                b"diff.example.command\n/bin/command\0",
                "unsafe command-bearing Git configuration 'diff.example.command'",
            ),
            (
                b"diff.example.textconv\n/bin/command",
                "unsafe command-bearing Git configuration 'diff.example.textconv'",
            ),
        )
        for output, message in cases:
            with self.subTest(output=output):
                with self.assertRaisesRegex(RuntimeError, f"^{message}$"):
                    self.validate_output(output)

    def test_effective_configuration_uses_last_duplicate_and_surrogates(
        self,
    ) -> None:
        self.validate_output(
            b"core.fsmonitor\n/bin/command\0CORE.FSMONITOR\ntrue\0"
        )
        self.validate_output(
            b"filter.example.process\n/bin/command\0"
            b"FILTER.EXAMPLE.PROCESS\n \0"
        )
        self.validate_output(b"custom.\xff\nvalue-\xfe\0")

        with self.assertRaisesRegex(
            RuntimeError,
            "^unsafe command-bearing Git configuration 'core.fsmonitor'$",
        ):
            self.validate_output(
                b"core.fsmonitor\ntrue\0CORE.FSMONITOR\n/bin/command\0"
            )
        with self.assertRaisesRegex(
            RuntimeError,
            "^unsafe command-bearing Git configuration "
            "'filter.example.process'$",
        ):
            self.validate_output(
                b"filter.example.process\n \0"
                b"FILTER.EXAMPLE.PROCESS\n/bin/command\0"
            )

    def test_effective_configuration_preserves_validation_precedence(
        self,
    ) -> None:
        with self.assertRaisesRegex(
            RuntimeError,
            "^Git returned malformed effective configuration$",
        ):
            self.validate_output(
                b"core.fsmonitor\n/bin/command\0missing-separator"
            )

        class PolicyError(RuntimeError):
            pass

        pattern = mock.Mock(
            side_effect=AssertionError("matched patterns before fsmonitor")
        )
        with self.assertRaisesRegex(
            PolicyError,
            "^unsafe command-bearing Git configuration 'core.fsmonitor'$",
        ):
            self.policy.validate_effective_git_configuration(
                b"diff.external\n/bin/command\0"
                b"core.fsmonitor\n/bin/command",
                error_type=lambda: PolicyError,
                boolean_values=lambda: self.policy.GIT_BOOLEAN_VALUES,
                command_config_pattern=pattern,
            )
        pattern.assert_not_called()

        boolean_values = mock.Mock(
            side_effect=AssertionError("resolved booleans without fsmonitor")
        )
        self.policy.validate_effective_git_configuration(
            b"benign.key\nvalue",
            error_type=lambda: PolicyError,
            boolean_values=boolean_values,
            command_config_pattern=lambda: re.compile(r"(?!)"),
        )
        boolean_values.assert_not_called()

    def test_engine_effective_configuration_probe_is_exact_and_bounded(
        self,
    ) -> None:
        cwd = Path("/repository")
        successful = SimpleNamespace(
            returncode=0,
            stdout=b"core.fsmonitor\ntrue\0",
        )
        with mock.patch.object(
            self.engine,
            "raw_git",
            return_value=successful,
        ) as raw_git:
            self.engine.validate_effective_git_configuration(cwd)

        raw_git.assert_called_once_with(
            cwd,
            "config",
            "--null",
            "--list",
            text=False,
            check=False,
        )

        class ProbeError(RuntimeError):
            pass

        class FailedProbe:
            returncode = 17

            @property
            def stdout(self) -> bytes:
                raise AssertionError("read stdout after a failed probe")

        with (
            mock.patch.object(
                self.engine,
                "raw_git",
                return_value=FailedProbe(),
            ),
            mock.patch.object(self.engine, "LauncherError", ProbeError),
        ):
            with self.assertRaisesRegex(
                ProbeError,
                "^cannot inspect the repository's effective Git configuration$",
            ):
                self.engine.validate_effective_git_configuration(cwd)

    def test_engine_effective_configuration_resolves_policy_lazily(
        self,
    ) -> None:
        events: list[tuple[str, str]] = []

        class InitialError(RuntimeError):
            pass

        class ReboundError(RuntimeError):
            pass

        class FirstPattern:
            def fullmatch(pattern_self, key: str) -> None:
                events.append(("first-pattern", key))
                self.engine.GIT_COMMAND_CONFIG_RE = SecondPattern()
                return None

        class SecondPattern:
            def fullmatch(pattern_self, key: str) -> object | None:
                events.append(("second-pattern", key))
                if key == "danger.key":
                    self.engine.LauncherError = ReboundError
                    return object()
                return None

        result = SimpleNamespace(
            returncode=0,
            stdout=b"safe.key\nvalue\0danger.key\ncommand\0",
        )
        with (
            mock.patch.object(self.engine, "raw_git", return_value=result),
            mock.patch.object(
                self.engine,
                "GIT_COMMAND_CONFIG_RE",
                FirstPattern(),
            ),
            mock.patch.object(self.engine, "LauncherError", InitialError),
        ):
            with self.assertRaisesRegex(
                ReboundError,
                "^unsafe command-bearing Git configuration 'danger.key'$",
            ):
                self.engine.validate_effective_git_configuration(
                    Path("/repository")
                )

        self.assertEqual(
            events,
            [
                ("first-pattern", "safe.key"),
                ("second-pattern", "danger.key"),
            ],
        )

        class RebindingOutput:
            def split(output_self, separator: bytes) -> list[bytes]:
                self.assertEqual(separator, b"\0")
                self.engine.GIT_BOOLEAN_VALUES = {"custom"}
                return [b"core.fsmonitor\ncustom"]

        rebound_result = SimpleNamespace(
            returncode=0,
            stdout=RebindingOutput(),
        )
        with (
            mock.patch.object(
                self.engine,
                "raw_git",
                return_value=rebound_result,
            ),
            mock.patch.object(
                self.engine,
                "GIT_BOOLEAN_VALUES",
                {"initial"},
            ),
        ):
            self.engine.validate_effective_git_configuration(
                Path("/repository")
            )

    def test_git_resolves_the_effective_configuration_wrapper(self) -> None:
        cwd = Path("/repository")
        expected = SimpleNamespace(returncode=0)
        events: list[str] = []

        def authenticate_cwd(observed: Path) -> None:
            self.assertEqual(observed, cwd)
            events.append("authenticate")

        def validate_configuration(observed: Path) -> None:
            self.assertEqual(observed, cwd)
            events.append("validate")

        def run_git(*args: object, **kwargs: object) -> object:
            events.append("raw-git")
            return expected

        with (
            mock.patch.object(
                self.engine,
                "authenticate_git_cwd",
                side_effect=authenticate_cwd,
            ) as authenticate,
            mock.patch.object(
                self.engine,
                "validate_effective_git_configuration",
                side_effect=validate_configuration,
            ) as validate,
            mock.patch.object(
                self.engine,
                "raw_git",
                side_effect=run_git,
            ) as raw_git,
        ):
            observed = self.engine.git(cwd, "status", "--short")

        self.assertIs(observed, expected)
        self.assertEqual(events, ["authenticate", "validate", "raw-git"])
        authenticate.assert_called_once_with(cwd)
        validate.assert_called_once_with(cwd)
        raw_git.assert_called_once_with(
            cwd,
            "status",
            "--short",
            check=True,
            text=True,
            environment=None,
            input_data=None,
        )

        class ValidationError(RuntimeError):
            pass

        blocked_command = mock.Mock(
            side_effect=AssertionError("ran Git after validation failure")
        )
        with (
            mock.patch.object(self.engine, "authenticate_git_cwd"),
            mock.patch.object(
                self.engine,
                "validate_effective_git_configuration",
                side_effect=ValidationError("unsafe configuration"),
            ),
            mock.patch.object(self.engine, "raw_git", blocked_command),
        ):
            with self.assertRaisesRegex(
                ValidationError,
                "^unsafe configuration$",
            ):
                self.engine.git(cwd, "status", "--short")

        blocked_command.assert_not_called()

    def test_rebase_hardening_preserves_the_existing_argument_matrix(self) -> None:
        cases = (
            (("status", "--short"), ["status", "--short"]),
            (
                ("-C", "/repository", "rebase", "target"),
                ["-C", "/repository", "rebase", "--no-gpg-sign", "target"],
            ),
            (("rebase", "--abort"), ["rebase", "--abort"]),
            (("rebase", "--continue"), ["rebase", "--continue"]),
            (("rebase", "--edit-todo"), ["rebase", "--edit-todo"]),
            (("rebase", "--quit"), ["rebase", "--quit"]),
            (("rebase", "--skip"), ["rebase", "--skip"]),
            (
                ("rebase", "--no-gpg-sign", "target"),
                ["rebase", "--no-gpg-sign", "target"],
            ),
            (
                ("rebase", "--gpg-sign", "target"),
                ["rebase", "--gpg-sign", "target"],
            ),
            (
                ("rebase", "--gpg-sign=ABC123", "target"),
                ["rebase", "--gpg-sign=ABC123", "target"],
            ),
        )

        for supplied, expected in cases:
            with self.subTest(supplied=supplied):
                mutable = list(supplied)
                observed = self.policy.hardened_git_arguments(mutable)
                self.assertEqual(observed, expected)
                self.assertEqual(mutable, list(supplied))
                self.assertIsNot(observed, mutable)


if __name__ == "__main__":
    unittest.main()
