#!/usr/bin/env python3
"""Direct parity tests for immutable repository and launcher identities."""

from __future__ import annotations

import importlib
import inspect
import os
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
