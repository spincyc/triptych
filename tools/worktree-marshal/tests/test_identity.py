#!/usr/bin/env python3
"""Direct parity tests for runtime identities and launcher authentication."""

from __future__ import annotations

import importlib
import inspect
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from dataclasses import MISSING, FrozenInstanceError, fields, is_dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import get_type_hints
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE_ROOT / "src"


class OpaqueValue:
    """Stable test value that exposes accidental conversion in repr or identity."""

    def __init__(self, label: str) -> None:
        self.label = label

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, OpaqueValue)
            and self.label == other.label
        )

    def __hash__(self) -> int:
        return hash((OpaqueValue, self.label))

    def __repr__(self) -> str:
        return f"<opaque:{self.label}>"


class IdentityModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))
        cls.identity = importlib.import_module("worktree_marshal.identity")
        cls.engine = importlib.import_module("worktree_marshal.engine")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def schemas(
        self,
    ) -> tuple[
        tuple[type, tuple[tuple[str, type], ...]],
        ...,
    ]:
        return (
            (
                self.identity.Repository,
                (
                    ("root", Path),
                    ("git_dir", Path),
                    ("common_git_dir", Path),
                    ("relative_cwd", Path),
                    ("linked_worktree", bool),
                    ("state_root", Path),
                ),
            ),
            (
                self.identity.LinkedWorktreeIdentity,
                (
                    ("worktree", Path),
                    ("git_file", Path),
                    ("git_dir", Path),
                    ("common_git_dir", Path),
                ),
            ),
            (
                self.identity.LauncherIdentity,
                (
                    ("path", Path),
                    ("device", int),
                    ("inode", int),
                ),
            ),
        )

    def test_identity_import_is_cycle_free_and_environment_neutral(
        self,
    ) -> None:
        sibling_modules = (
            "engine",
            "git",
            "locks",
            "model",
            "process",
            "profiles",
            "state",
        )
        script = (
            "import os, sys; "
            "before = dict(os.environ); "
            "before_cwd = os.getcwd(); "
            f"sys.path.insert(0, {str(SOURCE_ROOT)!r}); "
            "import worktree_marshal.identity; "
            f"siblings = {sibling_modules!r}; "
            "raise SystemExit("
            "dict(os.environ) != before or "
            "os.getcwd() != before_cwd or "
            "any(f'worktree_marshal.{name}' in sys.modules for name in siblings)"
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

    def test_engine_reexports_the_exact_identity_classes(self) -> None:
        for class_name in (
            "Repository",
            "LinkedWorktreeIdentity",
            "LauncherIdentity",
        ):
            with self.subTest(identity=class_name):
                identity_type = getattr(self.identity, class_name)
                self.assertIs(
                    getattr(self.engine, class_name),
                    identity_type,
                )
                self.assertEqual(
                    identity_type.__module__,
                    "worktree_marshal.identity",
                )
        self.assertFalse(hasattr(self.identity, "Audit"))
        self.assertFalse(hasattr(self.identity, "PrimaryCheckoutState"))
        self.assertEqual(
            self.engine.Audit.__module__,
            "worktree_marshal.engine",
        )
        self.assertEqual(
            self.engine.PrimaryCheckoutState.__module__,
            "worktree_marshal.engine",
        )
        self.assertEqual(
            self.identity.LauncherIdentity.__doc__,
            "Authenticated identity of the in-process command entry point.",
        )

    def test_launcher_authentication_kernel_and_wrapper_signatures(
        self,
    ) -> None:
        parameters = inspect.signature(
            self.identity.authenticate_launcher
        ).parameters
        self.assertEqual(
            tuple(parameters),
            (
                "path",
                "os_error_type",
                "error_type",
                "regular_file_test",
                "access_check",
                "executable_mode",
                "identity_factory",
            ),
        )
        self.assertIs(
            parameters["path"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        for name in tuple(parameters)[1:]:
            self.assertIs(
                parameters[name].kind,
                inspect.Parameter.KEYWORD_ONLY,
            )
        for parameter in parameters.values():
            self.assertIs(parameter.default, inspect.Parameter.empty)

        self.assertIsNot(
            self.engine.authenticate_launcher,
            self.identity.authenticate_launcher,
        )
        wrapper_parameters = inspect.signature(
            self.engine.authenticate_launcher
        ).parameters
        self.assertEqual(tuple(wrapper_parameters), ("path",))
        self.assertIs(
            wrapper_parameters["path"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        self.assertIs(
            wrapper_parameters["path"].default,
            inspect.Parameter.empty,
        )

    def test_exact_single_line_kernel_and_wrapper_signatures(self) -> None:
        self.assertIs(
            self.engine._exact_single_line,
            self.identity.exact_single_line,
        )
        parameters = inspect.signature(
            self.identity.exact_single_line
        ).parameters
        self.assertEqual(
            tuple(parameters),
            (
                "path",
                "label",
                "file_reader",
                "decode_error_type",
                "error_type",
            ),
        )
        self.assertIs(
            parameters["path"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        for name in tuple(parameters)[1:]:
            self.assertIs(
                parameters[name].kind,
                inspect.Parameter.KEYWORD_ONLY,
            )
        for parameter in parameters.values():
            self.assertIs(parameter.default, inspect.Parameter.empty)

        self.assertIsNot(
            self.engine.exact_single_line,
            self.identity.exact_single_line,
        )
        wrapper_parameters = inspect.signature(
            self.engine.exact_single_line
        ).parameters
        self.assertEqual(tuple(wrapper_parameters), ("path", "label"))
        self.assertIs(
            wrapper_parameters["path"].kind,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
        self.assertIs(
            wrapper_parameters["label"].kind,
            inspect.Parameter.KEYWORD_ONLY,
        )
        for parameter in wrapper_parameters.values():
            self.assertIs(parameter.default, inspect.Parameter.empty)

    def test_exact_single_line_kernel_preserves_success_order_and_values(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []
        path = object()

        class TruthValue:
            def __bool__(truth_self) -> bool:
                events.append(("endswith-truth", None))
                return True

        class CountValue:
            def __ne__(count_self, other: object) -> bool:
                events.append(("count-compare", other))
                return False

        class DecodedValue:
            def __bool__(value_self) -> bool:
                events.append(("value-truth", None))
                return True

            def __contains__(value_self, needle: object) -> bool:
                events.append(("value-contains", needle))
                return False

        decoded = DecodedValue()

        class EncodedValue:
            def decode(encoded_self, encoding: str) -> object:
                events.append(("decode", encoding))
                return decoded

        class Data:
            def endswith(data_self, suffix: object) -> object:
                events.append(("endswith", suffix))
                return TruthValue()

            def count(data_self, needle: object) -> object:
                events.append(("count", needle))
                return CountValue()

            def __contains__(data_self, needle: object) -> bool:
                events.append(("data-contains", needle))
                return False

            def __getitem__(data_self, key: object) -> object:
                events.append(("slice", key))
                return EncodedValue()

        data = Data()

        def file_reader() -> object:
            events.append(("reader-provider", None))

            def read(observed_path: object, *, label: str) -> object:
                events.append(
                    ("reader-call", (observed_path, label))
                )
                return data

            return read

        decode_error_type = mock.Mock(
            side_effect=AssertionError(
                "resolved the decode error type on success"
            )
        )
        error_type = mock.Mock(
            side_effect=AssertionError(
                "resolved the launcher error on success"
            )
        )

        observed = self.identity.exact_single_line(
            path,
            label="the admin file",
            file_reader=file_reader,
            decode_error_type=decode_error_type,
            error_type=error_type,
        )

        self.assertIs(observed, decoded)
        self.assertEqual(
            events,
            [
                ("reader-provider", None),
                ("reader-call", (path, "the admin file")),
                ("endswith", b"\n"),
                ("endswith-truth", None),
                ("count", b"\n"),
                ("count-compare", 1),
                ("data-contains", b"\r"),
                ("slice", slice(None, -1, None)),
                ("decode", "utf-8"),
                ("value-truth", None),
                ("value-contains", "\0"),
            ],
        )
        decode_error_type.assert_not_called()
        error_type.assert_not_called()

    def test_exact_single_line_kernel_accepts_the_legacy_byte_domain(
        self,
    ) -> None:
        cases = (
            (b"path\n", "path"),
            ("café/δ\n".encode(), "café/δ"),
            (b"../relative path\n", "../relative path"),
            (b" \t \n", " \t "),
            (b"\x01\n", "\x01"),
            ("\u2028\n".encode(), "\u2028"),
        )

        for data, expected in cases:
            with self.subTest(data=data):
                reader = mock.Mock(return_value=data)
                decode_error_type = mock.Mock(
                    side_effect=AssertionError(
                        "resolved decode error for valid UTF-8"
                    )
                )
                error_type = mock.Mock(
                    side_effect=AssertionError(
                        "resolved launcher error for valid input"
                    )
                )

                observed = self.identity.exact_single_line(
                    Path("/admin/file"),
                    label="the admin file",
                    file_reader=lambda: reader,
                    decode_error_type=decode_error_type,
                    error_type=error_type,
                )

                self.assertEqual(observed, expected)
                reader.assert_called_once_with(
                    Path("/admin/file"),
                    label="the admin file",
                )
                decode_error_type.assert_not_called()
                error_type.assert_not_called()

    def test_exact_single_line_shape_checks_short_circuit_in_order(
        self,
    ) -> None:
        class LineError(RuntimeError):
            pass

        expected_events = {
            "terminal-newline": ["endswith"],
            "newline-count": ["endswith", "count"],
            "carriage-return": ["endswith", "count", "contains"],
        }

        for rejection, expected in expected_events.items():
            with self.subTest(rejection=rejection):
                events: list[str] = []

                class Data:
                    def endswith(data_self, suffix: bytes) -> bool:
                        self.assertEqual(suffix, b"\n")
                        events.append("endswith")
                        return rejection != "terminal-newline"

                    def count(data_self, needle: bytes) -> int:
                        self.assertEqual(needle, b"\n")
                        events.append("count")
                        return 2 if rejection == "newline-count" else 1

                    def __contains__(data_self, needle: bytes) -> bool:
                        self.assertEqual(needle, b"\r")
                        events.append("contains")
                        return rejection == "carriage-return"

                    def __getitem__(data_self, key: object) -> object:
                        raise AssertionError("decoded a malformed line")

                def error_type() -> type[BaseException]:
                    events.append("error-provider")
                    return LineError

                decode_error_type = mock.Mock(
                    side_effect=AssertionError(
                        "resolved decode error for a malformed line"
                    )
                )
                with self.assertRaises(LineError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: Data()
                        ),
                        decode_error_type=decode_error_type,
                        error_type=error_type,
                    )

                self.assertEqual(
                    str(caught.exception),
                    "the admin file does not contain one exact line",
                )
                self.assertIsNone(caught.exception.__cause__)
                self.assertEqual(events, expected + ["error-provider"])
                decode_error_type.assert_not_called()

    def test_exact_single_line_shape_rejection_precedes_decoding(
        self,
    ) -> None:
        class LineError(RuntimeError):
            pass

        cases = (
            b"",
            b"path",
            b"path\nextra",
            b"path\nextra\n",
            b"\n\n",
            b"path\r\n",
            b"pa\rth\n",
            b"\xff",
            b"\xff\r\n",
            b"\xff\n\n",
        )

        for data in cases:
            with self.subTest(data=data):
                decode_error_type = mock.Mock(
                    side_effect=AssertionError(
                        "decoded before validating exact line shape"
                    )
                )
                with self.assertRaises(LineError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: data
                        ),
                        decode_error_type=decode_error_type,
                        error_type=lambda: LineError,
                    )

                self.assertEqual(
                    str(caught.exception),
                    "the admin file does not contain one exact line",
                )
                self.assertIsNone(caught.exception.__cause__)
                decode_error_type.assert_not_called()

    def test_exact_single_line_chains_decode_errors_from_the_narrow_block(
        self,
    ) -> None:
        class SelectedDecodeError(RuntimeError):
            pass

        class LineError(RuntimeError):
            pass

        for stage in ("slice", "decode-attribute", "decode-call"):
            with self.subTest(wrapped_stage=stage):
                original = SelectedDecodeError(stage)
                events: list[str] = []

                class EncodedValue:
                    @property
                    def decode(encoded_self) -> object:
                        events.append("decode-attribute")
                        if stage == "decode-attribute":
                            raise original

                        def decode(encoding: str) -> None:
                            self.assertEqual(encoding, "utf-8")
                            events.append("decode-call")
                            if stage == "decode-call":
                                raise original
                            raise AssertionError(
                                "decode unexpectedly succeeded"
                            )

                        return decode

                class Data:
                    def endswith(data_self, suffix: bytes) -> bool:
                        return True

                    def count(data_self, needle: bytes) -> int:
                        return 1

                    def __contains__(data_self, needle: bytes) -> bool:
                        return False

                    def __getitem__(data_self, key: object) -> EncodedValue:
                        events.append("slice")
                        if stage == "slice":
                            raise original
                        return EncodedValue()

                decode_error_type = mock.Mock(
                    return_value=SelectedDecodeError
                )
                error_type = mock.Mock(return_value=LineError)
                with self.assertRaises(LineError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: Data()
                        ),
                        decode_error_type=decode_error_type,
                        error_type=error_type,
                    )

                self.assertEqual(
                    str(caught.exception),
                    "the admin file is not valid UTF-8",
                )
                self.assertIs(caught.exception.__cause__, original)
                self.assertIs(caught.exception.__context__, original)
                decode_error_type.assert_called_once_with()
                error_type.assert_called_once_with()
                self.assertEqual(
                    events,
                    {
                        "slice": ["slice"],
                        "decode-attribute": [
                            "slice",
                            "decode-attribute",
                        ],
                        "decode-call": [
                            "slice",
                            "decode-attribute",
                            "decode-call",
                        ],
                    }[stage],
                )

    def test_exact_single_line_rejects_actual_invalid_utf8_with_exact_cause(
        self,
    ) -> None:
        class LineError(RuntimeError):
            pass

        with self.assertRaises(LineError) as caught:
            self.identity.exact_single_line(
                Path("/admin/file"),
                label="the admin file",
                file_reader=lambda: (
                    lambda path, *, label: b"\xff\n"
                ),
                decode_error_type=lambda: UnicodeDecodeError,
                error_type=lambda: LineError,
            )

        self.assertEqual(
            str(caught.exception),
            "the admin file is not valid UTF-8",
        )
        self.assertIsInstance(
            caught.exception.__cause__,
            UnicodeDecodeError,
        )
        self.assertIs(
            caught.exception.__context__,
            caught.exception.__cause__,
        )

    def test_exact_single_line_does_not_translate_nonmatching_decode_errors(
        self,
    ) -> None:
        class SelectedDecodeError(RuntimeError):
            pass

        for stage in ("slice", "decode-attribute", "decode-call"):
            with self.subTest(unwrapped_stage=stage):
                original = LookupError(stage)

                class EncodedValue:
                    @property
                    def decode(encoded_self) -> object:
                        if stage == "decode-attribute":
                            raise original

                        def decode(encoding: str) -> None:
                            if stage == "decode-call":
                                raise original
                            raise AssertionError(
                                "decode unexpectedly succeeded"
                            )

                        return decode

                class Data:
                    def endswith(data_self, suffix: bytes) -> bool:
                        return True

                    def count(data_self, needle: bytes) -> int:
                        return 1

                    def __contains__(data_self, needle: bytes) -> bool:
                        return False

                    def __getitem__(data_self, key: object) -> EncodedValue:
                        if stage == "slice":
                            raise original
                        return EncodedValue()

                decode_error_type = mock.Mock(
                    return_value=SelectedDecodeError
                )
                error_type = mock.Mock(
                    side_effect=AssertionError(
                        "translated a nonmatching decode error"
                    )
                )
                with self.assertRaises(LookupError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: Data()
                        ),
                        decode_error_type=decode_error_type,
                        error_type=error_type,
                    )

                self.assertIs(caught.exception, original)
                decode_error_type.assert_called_once_with()
                error_type.assert_not_called()

        original = SelectedDecodeError("decode failed")
        matcher_failure = RuntimeError("decode matcher failed")

        class FailingData:
            def endswith(data_self, suffix: bytes) -> bool:
                return True

            def count(data_self, needle: bytes) -> int:
                return 1

            def __contains__(data_self, needle: bytes) -> bool:
                return False

            def __getitem__(data_self, key: object) -> object:
                raise original

        def broken_decode_error_type() -> type[BaseException]:
            raise matcher_failure

        blocked_error_type = mock.Mock(
            side_effect=AssertionError(
                "translated after decode matcher failure"
            )
        )
        with self.assertRaises(RuntimeError) as matcher_caught:
            self.identity.exact_single_line(
                Path("/admin/file"),
                label="the admin file",
                file_reader=lambda: (
                    lambda path, *, label: FailingData()
                ),
                decode_error_type=broken_decode_error_type,
                error_type=blocked_error_type,
            )

        self.assertIs(matcher_caught.exception, matcher_failure)
        self.assertIs(matcher_caught.exception.__context__, original)
        blocked_error_type.assert_not_called()

    def test_exact_single_line_keeps_all_other_failures_outside_decode_catch(
        self,
    ) -> None:
        class SelectedDecodeError(RuntimeError):
            pass

        stages = (
            "reader-provider",
            "reader-call",
            "endswith",
            "count",
            "carriage-contains",
            "value-truth",
            "value-contains",
        )

        for stage in stages:
            with self.subTest(unwrapped_stage=stage):
                original = SelectedDecodeError(stage)

                def fail_at(observed: str) -> None:
                    if stage == observed:
                        raise original

                class DecodedValue:
                    def __bool__(value_self) -> bool:
                        fail_at("value-truth")
                        return True

                    def __contains__(
                        value_self,
                        needle: object,
                    ) -> bool:
                        self.assertEqual(needle, "\0")
                        fail_at("value-contains")
                        return False

                class EncodedValue:
                    def decode(
                        encoded_self,
                        encoding: str,
                    ) -> DecodedValue:
                        self.assertEqual(encoding, "utf-8")
                        return DecodedValue()

                class Data:
                    def endswith(data_self, suffix: bytes) -> bool:
                        self.assertEqual(suffix, b"\n")
                        fail_at("endswith")
                        return True

                    def count(data_self, needle: bytes) -> int:
                        self.assertEqual(needle, b"\n")
                        fail_at("count")
                        return 1

                    def __contains__(
                        data_self,
                        needle: bytes,
                    ) -> bool:
                        self.assertEqual(needle, b"\r")
                        fail_at("carriage-contains")
                        return False

                    def __getitem__(
                        data_self,
                        key: object,
                    ) -> EncodedValue:
                        return EncodedValue()

                def file_reader() -> object:
                    fail_at("reader-provider")

                    def read(path: object, *, label: str) -> Data:
                        fail_at("reader-call")
                        return Data()

                    return read

                decode_error_type = mock.Mock(
                    return_value=SelectedDecodeError
                )
                error_type = mock.Mock(
                    side_effect=AssertionError(
                        "translated a failure outside decoding"
                    )
                )
                with self.assertRaises(SelectedDecodeError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=file_reader,
                        decode_error_type=decode_error_type,
                        error_type=error_type,
                    )

                self.assertIs(caught.exception, original)
                decode_error_type.assert_not_called()
                error_type.assert_not_called()

    def test_exact_single_line_invalid_path_checks_short_circuit_in_order(
        self,
    ) -> None:
        class LineError(RuntimeError):
            pass

        for rejection in ("empty", "nul"):
            with self.subTest(rejection=rejection):
                events: list[str] = []

                class DecodedValue:
                    def __bool__(value_self) -> bool:
                        events.append("value-truth")
                        return rejection != "empty"

                    def __contains__(
                        value_self,
                        needle: object,
                    ) -> bool:
                        self.assertEqual(needle, "\0")
                        events.append("value-contains")
                        return rejection == "nul"

                class EncodedValue:
                    def decode(
                        encoded_self,
                        encoding: str,
                    ) -> DecodedValue:
                        return DecodedValue()

                class Data:
                    def endswith(data_self, suffix: bytes) -> bool:
                        return True

                    def count(data_self, needle: bytes) -> int:
                        return 1

                    def __contains__(
                        data_self,
                        needle: bytes,
                    ) -> bool:
                        return False

                    def __getitem__(
                        data_self,
                        key: object,
                    ) -> EncodedValue:
                        return EncodedValue()

                def error_type() -> type[BaseException]:
                    events.append("error-provider")
                    return LineError

                decode_error_type = mock.Mock(
                    side_effect=AssertionError(
                        "resolved decode error after successful decode"
                    )
                )
                with self.assertRaises(LineError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: Data()
                        ),
                        decode_error_type=decode_error_type,
                        error_type=error_type,
                    )

                self.assertEqual(
                    str(caught.exception),
                    "the admin file has an invalid path",
                )
                self.assertIsNone(caught.exception.__cause__)
                self.assertEqual(
                    events,
                    (
                        ["value-truth", "error-provider"]
                        if rejection == "empty"
                        else [
                            "value-truth",
                            "value-contains",
                            "error-provider",
                        ]
                    ),
                )
                decode_error_type.assert_not_called()

        for data in (b"\n", b"a\0b\n"):
            with self.subTest(actual_bytes=data):
                with self.assertRaises(LineError) as caught:
                    self.identity.exact_single_line(
                        Path("/admin/file"),
                        label="the admin file",
                        file_reader=lambda: (
                            lambda path, *, label: data
                        ),
                        decode_error_type=lambda: UnicodeDecodeError,
                        error_type=lambda: LineError,
                    )
                self.assertEqual(
                    str(caught.exception),
                    "the admin file has an invalid path",
                )
                self.assertIsNone(caught.exception.__cause__)

    def test_exact_single_line_resolves_error_before_formatting_label(
        self,
    ) -> None:
        events: list[str] = []

        class CapturedError(RuntimeError):
            pass

        class ReboundError(RuntimeError):
            pass

        class Label:
            def __format__(
                label_self,
                format_specification: str,
            ) -> str:
                self.assertEqual(format_specification, "")
                events.append("format-label")
                error_types[0] = ReboundError
                return "the admin file"

        error_types: list[type[BaseException]] = [CapturedError]

        def error_type() -> type[BaseException]:
            events.append("error-provider")
            return error_types[0]

        with self.assertRaises(CapturedError) as caught:
            self.identity.exact_single_line(
                Path("/admin/file"),
                label=Label(),
                file_reader=lambda: (
                    lambda path, *, label: b"missing-newline"
                ),
                decode_error_type=mock.Mock(
                    side_effect=AssertionError("decoded malformed input")
                ),
                error_type=error_type,
            )

        self.assertEqual(
            str(caught.exception),
            "the admin file does not contain one exact line",
        )
        self.assertEqual(events, ["error-provider", "format-label"])
        self.assertIs(error_types[0], ReboundError)

    def test_engine_exact_single_line_wrapper_forwards_lazy_globals(
        self,
    ) -> None:
        class InitialDecodeError(RuntimeError):
            pass

        class ReboundDecodeError(RuntimeError):
            pass

        class InitialLineError(RuntimeError):
            pass

        class ReboundLineError(RuntimeError):
            pass

        path = Path("/admin/file")
        initial_reader = mock.Mock(name="initial-reader")
        rebound_reader = mock.Mock(name="rebound-reader")
        sentinel = object()

        def exact_single_line(
            observed_path: object,
            **dependencies: object,
        ) -> object:
            self.assertIs(observed_path, path)
            self.assertEqual(
                tuple(dependencies),
                (
                    "label",
                    "file_reader",
                    "decode_error_type",
                    "error_type",
                ),
            )
            self.assertEqual(dependencies["label"], "the admin file")
            self.engine.safe_regular_file_bytes = rebound_reader
            self.assertIs(
                dependencies["file_reader"](),
                rebound_reader,
            )
            self.engine.UnicodeDecodeError = ReboundDecodeError
            self.assertIs(
                dependencies["decode_error_type"](),
                ReboundDecodeError,
            )
            self.engine.LauncherError = ReboundLineError
            self.assertIs(
                dependencies["error_type"](),
                ReboundLineError,
            )
            return sentinel

        with (
            mock.patch.object(
                self.engine,
                "_exact_single_line",
                side_effect=exact_single_line,
            ) as kernel,
            mock.patch.object(
                self.engine,
                "safe_regular_file_bytes",
                initial_reader,
            ),
            mock.patch.object(
                self.engine,
                "UnicodeDecodeError",
                InitialDecodeError,
                create=True,
            ),
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialLineError,
            ),
        ):
            observed = self.engine.exact_single_line(
                path,
                label="the admin file",
            )

        self.assertIs(observed, sentinel)
        kernel.assert_called_once()
        initial_reader.assert_not_called()
        rebound_reader.assert_not_called()

    def test_engine_real_exact_single_line_kernel_observes_rebound_errors(
        self,
    ) -> None:
        class InitialDecodeError(RuntimeError):
            pass

        class ReboundDecodeError(RuntimeError):
            pass

        class InitialLineError(RuntimeError):
            pass

        class ReboundLineError(RuntimeError):
            pass

        decode_failure = ReboundDecodeError("invalid encoding")
        path = Path("/admin/file")
        reader = mock.Mock()

        class EncodedValue:
            def decode(encoded_self, encoding: str) -> None:
                self.assertEqual(encoding, "utf-8")
                raise decode_failure

        class Data:
            def endswith(data_self, suffix: bytes) -> bool:
                return True

            def count(data_self, needle: bytes) -> int:
                return 1

            def __contains__(data_self, needle: bytes) -> bool:
                return False

            def __getitem__(data_self, key: object) -> EncodedValue:
                return EncodedValue()

        def read(observed_path: object, *, label: str) -> Data:
            self.assertIs(observed_path, path)
            self.assertEqual(label, "the admin file")
            self.engine.UnicodeDecodeError = ReboundDecodeError
            self.engine.LauncherError = ReboundLineError
            return Data()

        reader.side_effect = read
        with (
            mock.patch.object(
                self.engine,
                "_exact_single_line",
                self.identity.exact_single_line,
            ),
            mock.patch.object(
                self.engine,
                "safe_regular_file_bytes",
                reader,
            ),
            mock.patch.object(
                self.engine,
                "UnicodeDecodeError",
                InitialDecodeError,
                create=True,
            ),
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialLineError,
            ),
        ):
            with self.assertRaises(ReboundLineError) as caught:
                self.engine.exact_single_line(
                    path,
                    label="the admin file",
                )

        self.assertEqual(
            str(caught.exception),
            "the admin file is not valid UTF-8",
        )
        self.assertIs(caught.exception.__cause__, decode_failure)
        reader.assert_called_once_with(path, label="the admin file")

    def test_engine_exact_single_line_matches_real_file_behavior(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "commondir"
            path.write_bytes("../..\n".encode())
            self.assertEqual(
                self.engine.exact_single_line(
                    path,
                    label="the retained worktree commondir file",
                ),
                "../..",
            )

            cases = (
                (
                    b"missing-newline",
                    "the retained worktree commondir file "
                    "does not contain one exact line",
                ),
                (
                    b"\xff\n",
                    "the retained worktree commondir file "
                    "is not valid UTF-8",
                ),
                (
                    b"\n",
                    "the retained worktree commondir file "
                    "has an invalid path",
                ),
            )
            for data, message in cases:
                with self.subTest(data=data):
                    path.write_bytes(data)
                    with self.assertRaisesRegex(
                        self.engine.LauncherError,
                        f"^{message}$",
                    ):
                        self.engine.exact_single_line(
                            path,
                            label=(
                                "the retained worktree commondir file"
                            ),
                        )

    def test_dataclass_schemas_and_constructor_surfaces_are_exact(
        self,
    ) -> None:
        for identity_type, expected_schema in self.schemas():
            with self.subTest(identity=identity_type.__name__):
                self.assertTrue(is_dataclass(identity_type))
                parameters = inspect.signature(identity_type).parameters
                signature = inspect.signature(identity_type)
                self.assertEqual(
                    tuple(parameters),
                    tuple(name for name, annotation in expected_schema),
                )
                self.assertIs(signature.return_annotation, None)
                self.assertEqual(
                    identity_type.__annotations__,
                    {
                        name: annotation.__name__
                        for name, annotation in expected_schema
                    },
                )
                resolved_types = get_type_hints(identity_type)
                self.assertEqual(
                    resolved_types,
                    dict(expected_schema),
                )
                model_fields = fields(identity_type)
                self.assertEqual(
                    tuple(field.name for field in model_fields),
                    tuple(name for name, annotation in expected_schema),
                )
                self.assertEqual(
                    tuple(resolved_types[field.name] for field in model_fields),
                    tuple(annotation for name, annotation in expected_schema),
                )
                self.assertEqual(
                    tuple(field.type for field in model_fields),
                    tuple(
                        annotation.__name__
                        for name, annotation in expected_schema
                    ),
                )
                self.assertEqual(
                    identity_type.__match_args__,
                    tuple(name for name, annotation in expected_schema),
                )

                for parameter in parameters.values():
                    self.assertIs(
                        parameter.kind,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                    self.assertIs(parameter.default, inspect.Parameter.empty)
                for field in model_fields:
                    self.assertIs(field.default, MISSING)
                    self.assertIs(field.default_factory, MISSING)
                    self.assertTrue(field.init)
                    self.assertTrue(field.repr)
                    self.assertTrue(field.compare)
                    self.assertIsNone(field.hash)
                    self.assertFalse(field.kw_only)
                    self.assertEqual(dict(field.metadata), {})

                settings = identity_type.__dataclass_params__
                self.assertTrue(settings.init)
                self.assertTrue(settings.repr)
                self.assertTrue(settings.eq)
                self.assertFalse(settings.order)
                self.assertFalse(settings.unsafe_hash)
                self.assertTrue(settings.frozen)
                self.assertFalse(hasattr(identity_type, "__slots__"))

                with self.assertRaises(TypeError):
                    identity_type()
                with self.assertRaises(TypeError):
                    identity_type(
                        *(object() for field in expected_schema),
                        object(),
                    )
                with self.assertRaises(TypeError):
                    identity_type(
                        **{
                            **{
                                name: object()
                                for name, annotation in expected_schema
                            },
                            "unexpected": object(),
                        }
                    )

    def test_construction_preserves_every_opaque_value_by_identity(
        self,
    ) -> None:
        for identity_type, expected_schema in self.schemas():
            with self.subTest(identity=identity_type.__name__):
                values = tuple(
                    OpaqueValue(name)
                    for name, annotation in expected_schema
                )
                positional = identity_type(*values)
                keyword = identity_type(
                    **{
                        name: value
                        for (name, annotation), value in zip(
                            expected_schema,
                            values,
                            strict=True,
                        )
                    }
                )

                for (name, annotation), value in zip(
                    expected_schema,
                    values,
                    strict=True,
                ):
                    self.assertIs(getattr(positional, name), value)
                    self.assertIs(getattr(keyword, name), value)
                self.assertEqual(positional, keyword)

                first_name = expected_schema[0][0]
                with self.assertRaises(FrozenInstanceError):
                    setattr(positional, first_name, object())
                with self.assertRaises(FrozenInstanceError):
                    delattr(positional, first_name)
                with self.assertRaises(FrozenInstanceError):
                    positional.unexpected = object()

        class HostileValue:
            def __fspath__(value_self) -> str:
                raise AssertionError("coerced a path field")

            def __bool__(value_self) -> bool:
                raise AssertionError("coerced a boolean field")

            def __int__(value_self) -> int:
                raise AssertionError("coerced an integer field")

            def __index__(value_self) -> int:
                raise AssertionError("indexed an integer field")

        for identity_type, expected_schema in self.schemas():
            with self.subTest(hostile_identity=identity_type.__name__):
                values = tuple(
                    HostileValue()
                    for name, annotation in expected_schema
                )
                observed = identity_type(*values)
                for (name, annotation), value in zip(
                    expected_schema,
                    values,
                    strict=True,
                ):
                    self.assertIs(getattr(observed, name), value)

    def test_value_semantics_hash_repr_and_positional_shape_are_exact(
        self,
    ) -> None:
        for identity_type, expected_schema in self.schemas():
            with self.subTest(identity=identity_type.__name__):
                first_values = tuple(
                    OpaqueValue(name)
                    for name, annotation in expected_schema
                )
                equal_values = tuple(
                    OpaqueValue(name)
                    for name, annotation in expected_schema
                )
                changed_values = (
                    *equal_values[:-1],
                    OpaqueValue("changed"),
                )
                first = identity_type(*first_values)
                equal = identity_type(*equal_values)
                changed = identity_type(*changed_values)

                self.assertIsNot(first, equal)
                self.assertEqual(first, equal)
                self.assertEqual(hash(first), hash(equal))
                self.assertEqual(hash(first), hash(first_values))
                self.assertNotEqual(first, changed)
                self.assertNotEqual(first, tuple(first_values))
                with self.assertRaises(TypeError):
                    first < equal

                expected_repr = (
                    f"{identity_type.__name__}("
                    + ", ".join(
                        f"{name}=<opaque:{name}>"
                        for name, annotation in expected_schema
                    )
                    + ")"
                )
                self.assertEqual(repr(first), expected_repr)
                self.assertEqual(
                    tuple(
                        getattr(first, name)
                        for name in identity_type.__match_args__
                    ),
                    first_values,
                )

                subclass = type(
                    f"Derived{identity_type.__name__}",
                    (identity_type,),
                    {},
                )
                self.assertNotEqual(first, subclass(*equal_values))

                unhashable_values = (*first_values[:-1], [])
                unhashable = identity_type(*unhashable_values)
                with self.assertRaises(TypeError):
                    hash(unhashable)

    def test_launcher_authentication_kernel_preserves_exact_success_order(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []
        sentinel = object()

        class TruthValue:
            def __init__(truth_self, label: str) -> None:
                truth_self.label = label

            def __bool__(truth_self) -> bool:
                events.append(("truth", truth_self.label))
                return True

        class Metadata:
            @property
            def st_mode(metadata_self) -> object:
                events.append(("st-mode", None))
                return "opaque-mode"

            @property
            def st_dev(metadata_self) -> object:
                events.append(("st-dev", None))
                return "opaque-device"

            @property
            def st_ino(metadata_self) -> object:
                events.append(("st-ino", None))
                return "opaque-inode"

        class ResolvedPath:
            def stat(resolved_self) -> object:
                events.append(("stat", None))
                return Metadata()

        resolved = ResolvedPath()

        class InputPath:
            def is_absolute(path_self) -> object:
                events.append(("is-absolute", None))
                return TruthValue("absolute")

            def resolve(path_self, *, strict: bool) -> object:
                events.append(("resolve", strict))
                return resolved

        path = InputPath()

        def os_error_type() -> type[OSError]:
            raise AssertionError("resolved OS error type without an exception")

        def error_type() -> type[Exception]:
            raise AssertionError("resolved launcher error on success")

        def regular_file_test() -> object:
            events.append(("regular-resolver", None))

            def test(mode: object) -> object:
                events.append(("regular-test", mode))
                return TruthValue("regular")

            return test

        def access_check() -> object:
            events.append(("access-resolver", None))

            def check(candidate: object, mode: object) -> object:
                events.append(("access-check", (candidate, mode)))
                return TruthValue("executable")

            return check

        def executable_mode() -> object:
            events.append(("mode-resolver", None))
            return "opaque-executable-mode"

        def identity_factory() -> object:
            events.append(("identity-resolver", None))

            def construct(**values: object) -> object:
                events.append(("identity-constructor", values))
                return sentinel

            return construct

        observed = self.identity.authenticate_launcher(
            path,
            os_error_type=os_error_type,
            error_type=error_type,
            regular_file_test=regular_file_test,
            access_check=access_check,
            executable_mode=executable_mode,
            identity_factory=identity_factory,
        )

        self.assertIs(observed, sentinel)
        self.assertEqual(
            events,
            [
                ("is-absolute", None),
                ("truth", "absolute"),
                ("resolve", True),
                ("stat", None),
                ("regular-resolver", None),
                ("st-mode", None),
                ("regular-test", "opaque-mode"),
                ("truth", "regular"),
                ("access-resolver", None),
                ("mode-resolver", None),
                (
                    "access-check",
                    (resolved, "opaque-executable-mode"),
                ),
                ("truth", "executable"),
                ("identity-resolver", None),
                ("st-dev", None),
                ("st-ino", None),
                (
                    "identity-constructor",
                    {
                        "path": resolved,
                        "device": "opaque-device",
                        "inode": "opaque-inode",
                    },
                ),
            ],
        )

    def test_launcher_authentication_kernel_short_circuits_rejections(
        self,
    ) -> None:
        class AuthenticationError(RuntimeError):
            pass

        dependencies = {
            "os_error_type": mock.Mock(
                side_effect=AssertionError("resolved OS error type")
            ),
            "regular_file_test": mock.Mock(
                side_effect=AssertionError("resolved regular-file test")
            ),
            "access_check": mock.Mock(
                side_effect=AssertionError("resolved access check")
            ),
            "executable_mode": mock.Mock(
                side_effect=AssertionError("resolved executable mode")
            ),
            "identity_factory": mock.Mock(
                side_effect=AssertionError("resolved identity factory")
            ),
        }
        relative = mock.Mock()
        relative.is_absolute.return_value = False
        with self.assertRaisesRegex(
            AuthenticationError,
            "^the launcher entry point must be an absolute path$",
        ):
            self.identity.authenticate_launcher(
                relative,
                error_type=lambda: AuthenticationError,
                **dependencies,
            )
        relative.resolve.assert_not_called()
        for provider in dependencies.values():
            provider.assert_not_called()

        metadata = SimpleNamespace(st_mode="mode", st_dev=1, st_ino=2)
        resolved = mock.Mock()
        resolved.stat.return_value = metadata
        absolute = mock.Mock()
        absolute.is_absolute.return_value = True
        absolute.resolve.return_value = resolved
        os_error_type = mock.Mock(return_value=OSError)
        regular_predicate = mock.Mock(return_value=False)
        regular_file_test = mock.Mock(return_value=regular_predicate)
        access_check = mock.Mock(
            side_effect=AssertionError("checked access for a non-file")
        )
        executable_mode = mock.Mock(
            side_effect=AssertionError("resolved mode for a non-file")
        )
        identity_factory = mock.Mock(
            side_effect=AssertionError("constructed rejected identity")
        )
        with self.assertRaisesRegex(
            AuthenticationError,
            "^the launcher entry point is not a usable executable$",
        ):
            self.identity.authenticate_launcher(
                absolute,
                os_error_type=os_error_type,
                error_type=lambda: AuthenticationError,
                regular_file_test=regular_file_test,
                access_check=access_check,
                executable_mode=executable_mode,
                identity_factory=identity_factory,
            )
        regular_file_test.assert_called_once_with()
        regular_predicate.assert_called_once_with("mode")
        access_check.assert_not_called()
        executable_mode.assert_not_called()
        identity_factory.assert_not_called()
        os_error_type.assert_not_called()

        access_predicate = mock.Mock(return_value=False)
        access_check = mock.Mock(return_value=access_predicate)
        executable_mode = mock.Mock(return_value="execute")
        identity_factory = mock.Mock(
            side_effect=AssertionError("constructed nonexecutable identity")
        )
        with self.assertRaisesRegex(
            AuthenticationError,
            "^the launcher entry point is not a usable executable$",
        ):
            self.identity.authenticate_launcher(
                absolute,
                os_error_type=os_error_type,
                error_type=lambda: AuthenticationError,
                regular_file_test=lambda: (
                    lambda mode: True
                ),
                access_check=access_check,
                executable_mode=executable_mode,
                identity_factory=identity_factory,
            )
        access_check.assert_called_once_with()
        executable_mode.assert_called_once_with()
        access_predicate.assert_called_once_with(resolved, "execute")
        identity_factory.assert_not_called()
        os_error_type.assert_not_called()

    def test_launcher_authentication_kernel_chains_only_lookup_os_errors(
        self,
    ) -> None:
        class ExpectedOsError(OSError):
            pass

        class AuthenticationError(RuntimeError):
            pass

        for stage in (
            "resolve-attribute",
            "resolve-call",
            "stat-attribute",
            "stat-call",
        ):
            with self.subTest(wrapped_stage=stage):
                original = ExpectedOsError(f"{stage} failed")
                events: list[str] = []

                class Resolved:
                    @property
                    def stat(resolved_self) -> object:
                        events.append("stat-attribute")
                        if stage == "stat-attribute":
                            raise original

                        def inspect() -> object:
                            events.append("stat-call")
                            if stage == "stat-call":
                                raise original
                            raise AssertionError(
                                "continued after expected lookup failure"
                            )

                        return inspect

                class InputPath:
                    def is_absolute(path_self) -> bool:
                        return True

                    @property
                    def resolve(path_self) -> object:
                        events.append("resolve-attribute")
                        if stage == "resolve-attribute":
                            raise original

                        def canonicalize(*, strict: bool) -> object:
                            events.append("resolve-call")
                            self.assertTrue(strict)
                            if stage == "resolve-call":
                                raise original
                            return Resolved()

                        return canonicalize

                os_error_type = mock.Mock(
                    return_value=ExpectedOsError
                )
                error_type = mock.Mock(
                    return_value=AuthenticationError
                )
                regular_file_test = mock.Mock(
                    side_effect=AssertionError(
                        "validated after path lookup failed"
                    )
                )
                identity_factory = mock.Mock(
                    side_effect=AssertionError(
                        "constructed after path lookup failed"
                    )
                )

                with self.assertRaises(AuthenticationError) as raised:
                    self.identity.authenticate_launcher(
                        InputPath(),
                        os_error_type=os_error_type,
                        error_type=error_type,
                        regular_file_test=regular_file_test,
                        access_check=mock.Mock(),
                        executable_mode=mock.Mock(),
                        identity_factory=identity_factory,
                    )

                self.assertEqual(
                    str(raised.exception),
                    "cannot authenticate the launcher entry point",
                )
                self.assertIs(raised.exception.__cause__, original)
                self.assertIs(raised.exception.__context__, original)
                self.assertTrue(
                    raised.exception.__suppress_context__
                )
                os_error_type.assert_called_once_with()
                error_type.assert_called_once_with()
                regular_file_test.assert_not_called()
                identity_factory.assert_not_called()
                expected_events = {
                    "resolve-attribute": ["resolve-attribute"],
                    "resolve-call": [
                        "resolve-attribute",
                        "resolve-call",
                    ],
                    "stat-attribute": [
                        "resolve-attribute",
                        "resolve-call",
                        "stat-attribute",
                    ],
                    "stat-call": [
                        "resolve-attribute",
                        "resolve-call",
                        "stat-attribute",
                        "stat-call",
                    ],
                }
                self.assertEqual(events, expected_events[stage])

        class UnexpectedFailure(RuntimeError):
            pass

        for stage in ("resolve", "stat"):
            with self.subTest(unmatched_stage=stage):
                original = UnexpectedFailure(f"{stage} failed")
                path = mock.Mock()
                path.is_absolute.return_value = True
                resolved = mock.Mock()
                if stage == "resolve":
                    path.resolve.side_effect = original
                else:
                    path.resolve.return_value = resolved
                    resolved.stat.side_effect = original
                os_error_type = mock.Mock(return_value=ExpectedOsError)
                error_type = mock.Mock(
                    side_effect=AssertionError(
                        "wrapped a non-OS lookup failure"
                    )
                )

                with self.assertRaises(UnexpectedFailure) as raised:
                    self.identity.authenticate_launcher(
                        path,
                        os_error_type=os_error_type,
                        error_type=error_type,
                        regular_file_test=mock.Mock(),
                        access_check=mock.Mock(),
                        executable_mode=mock.Mock(),
                        identity_factory=mock.Mock(),
                    )

                self.assertIs(raised.exception, original)
                os_error_type.assert_called_once_with()
                error_type.assert_not_called()

    def test_launcher_authentication_kernel_keeps_other_failures_outside_catch(
        self,
    ) -> None:
        stages = (
            "is-absolute",
            "absolute-truth",
            "st-mode",
            "regular-resolver",
            "regular-call",
            "regular-truth",
            "access-resolver",
            "mode-resolver",
            "access-call",
            "access-truth",
            "identity-resolver",
            "st-dev",
            "st-ino",
            "identity-call",
        )
        for stage in stages:
            with self.subTest(stage=stage):
                failure = OSError(f"{stage} failed")

                class ExplodingTruth:
                    def __bool__(truth_self) -> bool:
                        raise failure

                class Metadata:
                    @property
                    def st_mode(metadata_self) -> object:
                        if stage == "st-mode":
                            raise failure
                        return "mode"

                    @property
                    def st_dev(metadata_self) -> object:
                        if stage == "st-dev":
                            raise failure
                        return "device"

                    @property
                    def st_ino(metadata_self) -> object:
                        if stage == "st-ino":
                            raise failure
                        return "inode"

                class Resolved:
                    def stat(resolved_self) -> object:
                        return Metadata()

                class InputPath:
                    def is_absolute(path_self) -> object:
                        if stage == "is-absolute":
                            raise failure
                        if stage == "absolute-truth":
                            return ExplodingTruth()
                        return True

                    def resolve(
                        path_self,
                        *,
                        strict: bool,
                    ) -> object:
                        return Resolved()

                def regular_file_test() -> object:
                    if stage == "regular-resolver":
                        raise failure

                    def test(mode: object) -> object:
                        if stage == "regular-call":
                            raise failure
                        if stage == "regular-truth":
                            return ExplodingTruth()
                        return True

                    return test

                def access_check() -> object:
                    if stage == "access-resolver":
                        raise failure

                    def check(
                        path: object,
                        mode: object,
                    ) -> object:
                        if stage == "access-call":
                            raise failure
                        if stage == "access-truth":
                            return ExplodingTruth()
                        return True

                    return check

                def executable_mode() -> object:
                    if stage == "mode-resolver":
                        raise failure
                    return "execute"

                def identity_factory() -> object:
                    if stage == "identity-resolver":
                        raise failure

                    def construct(**values: object) -> object:
                        if stage == "identity-call":
                            raise failure
                        return values

                    return construct

                os_error_type = mock.Mock(
                    side_effect=AssertionError(
                        "caught an error outside path lookup"
                    )
                )
                error_type = mock.Mock(
                    side_effect=AssertionError(
                        "translated an error outside path lookup"
                    )
                )
                with self.assertRaises(OSError) as raised:
                    self.identity.authenticate_launcher(
                        InputPath(),
                        os_error_type=os_error_type,
                        error_type=error_type,
                        regular_file_test=regular_file_test,
                        access_check=access_check,
                        executable_mode=executable_mode,
                        identity_factory=identity_factory,
                    )

                self.assertIs(raised.exception, failure)
                os_error_type.assert_not_called()
                error_type.assert_not_called()

    def test_engine_launcher_wrapper_resolves_every_global_lazily(
        self,
    ) -> None:
        path = object()
        sentinel = object()
        events: list[tuple[str, object]] = []

        class InitialOsError(OSError):
            pass

        class ReboundOsError(OSError):
            pass

        class InitialLauncherError(RuntimeError):
            pass

        class ReboundLauncherError(RuntimeError):
            pass

        initial_identity = object()
        rebound_identity = object()

        class InitialStatApi:
            @property
            def S_ISREG(api_self) -> object:
                raise AssertionError("resolved regular test eagerly")

        class ReboundStatApi:
            @property
            def S_ISREG(api_self) -> object:
                events.append(("regular-test", None))
                return "rebound-regular-test"

        class InitialOsApi:
            @property
            def access(api_self) -> object:
                raise AssertionError("resolved access eagerly")

            @property
            def X_OK(api_self) -> object:
                raise AssertionError("resolved executable mode eagerly")

        class ModeOsApi:
            @property
            def X_OK(api_self) -> object:
                events.append(("executable-mode", None))
                return "rebound-executable-mode"

        class AccessOsApi:
            @property
            def access(api_self) -> object:
                events.append(("access-check", None))
                self.engine.os = ModeOsApi()
                return "rebound-access-check"

        def kernel(observed_path: object, **providers: object) -> object:
            events.append(("kernel", tuple(providers)))
            self.assertIs(observed_path, path)

            self.engine.OSError = ReboundOsError
            self.assertIs(providers["os_error_type"](), ReboundOsError)
            events.append(("os-error-type", None))

            self.engine.LauncherError = ReboundLauncherError
            self.assertIs(
                providers["error_type"](),
                ReboundLauncherError,
            )
            events.append(("launcher-error-type", None))

            self.engine.stat = ReboundStatApi()
            self.assertEqual(
                providers["regular_file_test"](),
                "rebound-regular-test",
            )

            self.engine.os = AccessOsApi()
            self.assertEqual(
                providers["access_check"](),
                "rebound-access-check",
            )
            self.assertEqual(
                providers["executable_mode"](),
                "rebound-executable-mode",
            )

            self.engine.LauncherIdentity = rebound_identity
            self.assertIs(
                providers["identity_factory"](),
                rebound_identity,
            )
            events.append(("identity-factory", None))
            return sentinel

        with (
            mock.patch.object(
                self.engine,
                "_authenticate_launcher",
                side_effect=kernel,
                create=True,
            ),
            mock.patch.object(
                self.engine,
                "OSError",
                InitialOsError,
                create=True,
            ),
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialLauncherError,
            ),
            mock.patch.object(
                self.engine,
                "stat",
                InitialStatApi(),
            ),
            mock.patch.object(
                self.engine,
                "os",
                InitialOsApi(),
            ),
            mock.patch.object(
                self.engine,
                "LauncherIdentity",
                initial_identity,
            ),
        ):
            observed = self.engine.authenticate_launcher(path)

        self.assertIs(observed, sentinel)
        self.assertEqual(
            events,
            [
                (
                    "kernel",
                    (
                        "os_error_type",
                        "error_type",
                        "regular_file_test",
                        "access_check",
                        "executable_mode",
                        "identity_factory",
                    ),
                ),
                ("os-error-type", None),
                ("launcher-error-type", None),
                ("regular-test", None),
                ("access-check", None),
                ("executable-mode", None),
                ("identity-factory", None),
            ],
        )

    def test_engine_and_real_kernel_rebind_error_types_at_failure(
        self,
    ) -> None:
        events: list[str] = []

        class InitialOsError(OSError):
            pass

        class ReboundOsError(OSError):
            pass

        class InitialLauncherError(RuntimeError):
            pass

        class ReboundLauncherError(RuntimeError):
            pass

        failure = ReboundOsError("lookup failed")

        class InputPath:
            def is_absolute(path_self) -> bool:
                events.append("is-absolute")
                return True

            def resolve(path_self, *, strict: bool) -> object:
                events.append("resolve")
                self.assertTrue(strict)
                self.engine.OSError = ReboundOsError
                self.engine.LauncherError = ReboundLauncherError
                raise failure

        with (
            mock.patch.object(
                self.engine,
                "OSError",
                InitialOsError,
                create=True,
            ),
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialLauncherError,
            ),
        ):
            with self.assertRaises(ReboundLauncherError) as raised:
                self.engine.authenticate_launcher(InputPath())

        self.assertEqual(events, ["is-absolute", "resolve"])
        self.assertEqual(
            str(raised.exception),
            "cannot authenticate the launcher entry point",
        )
        self.assertIs(raised.exception.__cause__, failure)
        self.assertIs(raised.exception.__context__, failure)

    def test_engine_and_real_kernel_rebind_validation_globals_in_order(
        self,
    ) -> None:
        events: list[tuple[str, object]] = []

        class InitialLauncherError(RuntimeError):
            pass

        class ReboundLauncherError(RuntimeError):
            def __init__(
                error_self,
                message: str,
            ) -> None:
                events.append(("launcher-error", message))
                super().__init__(message)

        class InitialStatApi:
            @property
            def S_ISREG(api_self) -> object:
                raise AssertionError("captured regular-file test eagerly")

        class InitialOsApi:
            @property
            def access(api_self) -> object:
                raise AssertionError("captured access check eagerly")

            @property
            def X_OK(api_self) -> object:
                raise AssertionError("captured executable mode eagerly")

        class ModeOsApi:
            @property
            def X_OK(api_self) -> object:
                events.append(("mode-lookup", None))
                return "current-executable-mode"

        class AccessOsApi:
            @property
            def access(api_self) -> object:
                events.append(("access-lookup", None))
                self.engine.os = ModeOsApi()

                def access(
                    candidate: object,
                    mode: object,
                ) -> bool:
                    events.append(("access-call", (candidate, mode)))
                    self.engine.LauncherError = ReboundLauncherError
                    return False

                return access

        class ReboundStatApi:
            @property
            def S_ISREG(api_self) -> object:
                events.append(("regular-lookup", None))

                def is_regular(mode: object) -> bool:
                    events.append(("regular-call", mode))
                    self.engine.os = AccessOsApi()
                    return True

                return is_regular

        class Metadata:
            @property
            def st_mode(metadata_self) -> object:
                events.append(("st-mode", None))
                return "current-mode"

        class Resolved:
            def stat(resolved_self) -> object:
                events.append(("stat", None))
                self.engine.stat = ReboundStatApi()
                return Metadata()

        resolved = Resolved()

        class InputPath:
            def is_absolute(path_self) -> bool:
                events.append(("is-absolute", None))
                return True

            def resolve(path_self, *, strict: bool) -> object:
                events.append(("resolve", strict))
                return resolved

        with (
            mock.patch.object(
                self.engine,
                "LauncherError",
                InitialLauncherError,
            ),
            mock.patch.object(
                self.engine,
                "stat",
                InitialStatApi(),
            ),
            mock.patch.object(
                self.engine,
                "os",
                InitialOsApi(),
            ),
        ):
            with self.assertRaises(ReboundLauncherError) as raised:
                self.engine.authenticate_launcher(InputPath())

        self.assertEqual(
            str(raised.exception),
            "the launcher entry point is not a usable executable",
        )
        self.assertEqual(
            events,
            [
                ("is-absolute", None),
                ("resolve", True),
                ("stat", None),
                ("regular-lookup", None),
                ("st-mode", None),
                ("regular-call", "current-mode"),
                ("access-lookup", None),
                ("mode-lookup", None),
                (
                    "access-call",
                    (resolved, "current-executable-mode"),
                ),
                (
                    "launcher-error",
                    "the launcher entry point is not a usable executable",
                ),
            ],
        )

    def test_authenticate_launcher_resolves_rebound_constructor_last(
        self,
    ) -> None:
        sentinel = object()
        rebound_factory = mock.Mock(return_value=sentinel)
        initial_factory = mock.Mock(
            side_effect=AssertionError("captured launcher identity too early")
        )
        real_access = os.access

        with tempfile.TemporaryDirectory() as directory:
            launcher = Path(directory) / "launcher"
            launcher.touch(mode=0o700)
            launcher.chmod(0o700)
            resolved = launcher.resolve(strict=True)
            metadata = resolved.stat()
            access_events: list[tuple[Path, int]] = []

            def validating_access(path: Path, mode: int) -> bool:
                access_events.append((path, mode))
                self.assertTrue(real_access(path, mode))
                self.engine.LauncherIdentity = rebound_factory
                return True

            with (
                mock.patch.object(
                    self.engine,
                    "LauncherIdentity",
                    initial_factory,
                ),
                mock.patch.object(
                    self.engine.os,
                    "access",
                    side_effect=validating_access,
                ),
            ):
                observed = self.engine.authenticate_launcher(launcher)

        self.assertIs(observed, sentinel)
        self.assertEqual(access_events, [(resolved, os.X_OK)])
        initial_factory.assert_not_called()
        rebound_factory.assert_called_once_with(
            path=resolved,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )

    def test_launcher_authentication_matches_real_filesystem_behavior(
        self,
    ) -> None:
        class AuthenticationError(RuntimeError):
            pass

        def authenticate(path: Path) -> object:
            return self.identity.authenticate_launcher(
                path,
                os_error_type=lambda: OSError,
                error_type=lambda: AuthenticationError,
                regular_file_test=lambda: stat.S_ISREG,
                access_check=lambda: os.access,
                executable_mode=lambda: os.X_OK,
                identity_factory=lambda: (
                    self.identity.LauncherIdentity
                ),
            )

        executable = Path(sys.executable).resolve(strict=True)
        metadata = executable.stat()
        expected = self.identity.LauncherIdentity(
            path=executable,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )
        self.assertEqual(authenticate(executable), expected)
        self.assertEqual(
            self.engine.authenticate_launcher(executable),
            expected,
        )

        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory).resolve(strict=True)
            with self.assertRaisesRegex(
                AuthenticationError,
                "^the launcher entry point is not a usable executable$",
            ):
                authenticate(temporary)

            missing = temporary / "missing-launcher"
            with self.assertRaises(AuthenticationError) as raised:
                authenticate(missing)
            self.assertEqual(
                str(raised.exception),
                "cannot authenticate the launcher entry point",
            )
            self.assertIsInstance(
                raised.exception.__cause__,
                FileNotFoundError,
            )

            nonexecutable = temporary / "nonexecutable"
            nonexecutable.write_text("#!/bin/sh\n", encoding="utf-8")
            nonexecutable.chmod(stat.S_IRUSR | stat.S_IWUSR)
            if not os.access(nonexecutable, os.X_OK):
                with self.assertRaisesRegex(
                    AuthenticationError,
                    "^the launcher entry point is not a usable executable$",
                ):
                    authenticate(nonexecutable)

            link = temporary / "launcher-link"
            try:
                link.symlink_to(executable)
            except (NotImplementedError, OSError):
                pass
            else:
                self.assertEqual(authenticate(link), expected)

        relative = Path("relative-launcher")
        with self.assertRaises(AuthenticationError) as raised:
            authenticate(relative)
        self.assertEqual(
            str(raised.exception),
            "the launcher entry point must be an absolute path",
        )
        self.assertIsNone(raised.exception.__cause__)

    def test_linked_worktree_authentication_resolves_rebound_constructor_last(
        self,
    ) -> None:
        canonical_worktree = Path("/state/worktrees/run")
        git_file = canonical_worktree / ".git"
        common_git_dir = Path("/repository/.git")
        worktrees_admin = common_git_dir / "worktrees"
        git_dir = worktrees_admin / "run"
        sentinel = object()
        events: list[tuple[str, object]] = []
        rebound_factory = mock.Mock(return_value=sentinel)
        initial_factory = mock.Mock(
            side_effect=AssertionError(
                "captured linked-worktree identity too early"
            )
        )

        class RebindingBacklink:
            def __ne__(backlink_self, other: object) -> bool:
                events.append(("validate-backlink", other))
                self.engine.LinkedWorktreeIdentity = rebound_factory
                return False

        backlink = RebindingBacklink()
        real_directory_values = {
            "the retained worktree": canonical_worktree,
            "the retained worktree Git admin directory": git_dir,
            "the retained worktree common Git directory": common_git_dir,
            "the recorded common Git directory": common_git_dir,
            "the common linked-worktree administration directory": (
                worktrees_admin
            ),
        }

        def exact_real_directory(path: Path, *, label: str) -> Path:
            events.append(("real-directory", (path, label)))
            return real_directory_values[label]

        line_values = {
            git_file: f"gitdir: {git_dir}",
            git_dir / "commondir": str(common_git_dir),
            git_dir / "gitdir": str(git_file),
        }

        def exact_single_line(path: Path, *, label: str) -> str:
            events.append(("single-line", (path, label)))
            return line_values[path]

        pointer_values = iter((git_dir, common_git_dir, backlink))

        def exact_pointer_path(
            raw_value: str,
            *,
            relative_to: Path,
            label: str,
        ) -> object:
            events.append(
                ("pointer", (raw_value, relative_to, label))
            )
            return next(pointer_values)

        identity_registry: dict[Path, object] = {}
        owner_registry: dict[Path, Path] = {}
        with (
            mock.patch.object(
                self.engine,
                "LinkedWorktreeIdentity",
                initial_factory,
            ),
            mock.patch.object(
                self.engine,
                "exact_real_directory",
                side_effect=exact_real_directory,
            ),
            mock.patch.object(
                self.engine,
                "exact_single_line",
                side_effect=exact_single_line,
            ),
            mock.patch.object(
                self.engine,
                "exact_pointer_path",
                side_effect=exact_pointer_path,
            ),
            mock.patch.object(
                self.engine,
                "_LINKED_WORKTREE_IDENTITIES",
                identity_registry,
            ),
            mock.patch.object(
                self.engine,
                "_LINKED_ADMIN_OWNERS",
                owner_registry,
            ),
        ):
            observed = self.engine.authenticate_linked_worktree_path(
                canonical_worktree,
                expected_common_git_dir=common_git_dir,
            )

        self.assertIs(observed, sentinel)
        initial_factory.assert_not_called()
        rebound_factory.assert_called_once_with(
            worktree=canonical_worktree,
            git_file=git_file,
            git_dir=git_dir,
            common_git_dir=common_git_dir,
        )
        self.assertIs(identity_registry[canonical_worktree], sentinel)
        self.assertEqual(owner_registry[git_dir], canonical_worktree)
        self.assertEqual(
            events[-1],
            ("validate-backlink", git_file),
        )
        self.assertEqual(
            tuple(
                event[1][1]
                for event in events
                if event[0] == "real-directory"
            ),
            (
                "the retained worktree",
                "the retained worktree Git admin directory",
                "the retained worktree common Git directory",
                "the recorded common Git directory",
                "the common linked-worktree administration directory",
            ),
        )
        self.assertEqual(
            sum(event[0] == "single-line" for event in events),
            3,
        )
        self.assertEqual(
            [
                event[1]
                for event in events
                if event[0] == "single-line"
            ],
            [
                (
                    git_file,
                    "the retained worktree .git file",
                ),
                (
                    git_dir / "commondir",
                    "the retained worktree commondir file",
                ),
                (
                    git_dir / "gitdir",
                    "the retained worktree gitdir backlink",
                ),
            ],
        )
        self.assertEqual(
            sum(event[0] == "pointer" for event in events),
            3,
        )

    def test_discover_repository_resolves_rebound_constructor_after_boundary(
        self,
    ) -> None:
        start = Path("/repository/subdirectory")
        root = Path("/repository")
        git_dir = Path("/repository/.git")
        common_git_dir = Path("/repository/.git")
        sentinel = object()
        events: list[tuple[str, object]] = []
        initial_factory = mock.Mock(
            side_effect=AssertionError("captured repository type too early")
        )

        def rebound_factory(**values: object) -> object:
            events.append(("repository-factory", values))
            return sentinel

        class ResolvedState:
            def __eq__(state_self, other: object) -> bool:
                events.append(("state-equality", other))
                return False

            @property
            def parents(state_self) -> tuple[Path, ...]:
                events.append(("state-parents", None))
                self.engine.Repository = rebound_factory
                return (Path("/marshal-state"), Path("/"))

        resolved_state = ResolvedState()

        class StateCandidate:
            def resolve(candidate_self) -> object:
                events.append(("state-resolve", None))
                return resolved_state

        class StateBase:
            def __truediv__(base_self, component: str) -> object:
                events.append(("state-component", component))
                return StateCandidate()

        git_results = iter(
            (
                SimpleNamespace(returncode=0, stdout="true\n"),
                SimpleNamespace(returncode=0, stdout=f"{root}\n"),
            )
        )
        with (
            mock.patch.object(
                self.engine,
                "Repository",
                initial_factory,
            ),
            mock.patch.object(
                self.engine,
                "git",
                side_effect=lambda *args, **kwargs: next(git_results),
            ),
            mock.patch.object(
                self.engine,
                "absolute_git_path",
                side_effect=(git_dir, common_git_dir),
            ),
            mock.patch.object(
                self.engine,
                "state_base",
                return_value=StateBase(),
            ),
            mock.patch.object(
                self.engine,
                "repository_slug",
                return_value="project",
            ),
        ):
            observed = self.engine.discover_repository(start)

        self.assertIs(observed, sentinel)
        initial_factory.assert_not_called()
        factory_events = [
            event for event in events if event[0] == "repository-factory"
        ]
        self.assertEqual(
            factory_events,
            [
                (
                    "repository-factory",
                    {
                        "root": root,
                        "git_dir": git_dir,
                        "common_git_dir": common_git_dir,
                        "relative_cwd": Path("subdirectory"),
                        "linked_worktree": False,
                        "state_root": resolved_state,
                    },
                )
            ],
        )
        self.assertEqual(
            tuple(event[0] for event in events[-4:]),
            (
                "state-resolve",
                "state-equality",
                "state-parents",
                "repository-factory",
            ),
        )


if __name__ == "__main__":
    unittest.main()
