"""The tracked act-history browser projection is exact and orphan-free.

The structure writer used to update one slice in a shared directory.  That
could leave both changed fragments and files whose source row had disappeared,
and no deployment gate compared what the browser served with a fresh
derivation.  These tests exercise the complete projection and, critically, the
three distinct drift shapes against temporary copies so the refusal itself is
proved without touching tracked data.
"""

from __future__ import annotations

import json
import importlib.machinery
import importlib.util
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[2]
TPT = ROOT / "tools" / "tpt"
TRACKED = ROOT / "src" / "web" / "data" / "structure" / "act-history"


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_act_history_structure_tool", str(ROOT / "tools" / "act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/act-history")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(TPT), "act-history", *arguments],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def files(root: pathlib.Path) -> dict[str, bytes]:
    if not root.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


class ActHistoryStructureTests(unittest.TestCase):
    def temporary_projection(self) -> tuple[tempfile.TemporaryDirectory, pathlib.Path]:
        # A clean checkout need not have the ignored build/ directory yet.
        # System temporary space is removed by the context owner and makes the
        # refusal tests independent of invocation order.
        held = tempfile.TemporaryDirectory()
        out = pathlib.Path(held.name)
        shutil.copytree(TRACKED, out / "structure" / "act-history")
        return held, out

    def test_the_tracked_projection_is_a_fresh_complete_derivation(self) -> None:
        checked = run("structure", "--check")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("current: 505 files for 3 slices", checked.stdout)

    def test_check_refuses_changed_missing_and_orphaned_files_without_writing(self) -> None:
        cases = (
            "changed",
            "missing",
            "orphan",
            "symlink",
            "directory-symlink",
            "special",
        )
        for kind in cases:
            with self.subTest(kind=kind):
                held, out = self.temporary_projection()
                self.addCleanup(held.cleanup)
                projection = out / "structure" / "act-history"
                if kind == "changed":
                    name = "index.json"
                    (projection / name).write_text('{"stale":true}\n', encoding="utf-8")
                elif kind == "missing":
                    name = "roman-holy-week/units.json"
                    (projection / name).unlink()
                elif kind == "orphan":
                    name = "latin-missal/unit/retired-prayer.json"
                    orphan = projection / name
                    orphan.parent.mkdir(parents=True, exist_ok=True)
                    orphan.write_text("{}\n", encoding="utf-8")
                elif kind == "symlink":
                    name = "linked-projection.json"
                    (projection / name).symlink_to(projection / "index.json")
                elif kind == "directory-symlink":
                    name = "latin-missal/linked-directory"
                    (projection / name).symlink_to(
                        projection / "roman-holy-week", target_is_directory=True
                    )
                else:
                    name = "latin-missal/unexpected-pipe"
                    os.mkfifo(projection / name)

                before = files(projection)
                checked = run("structure", "--check", "--out", str(out))
                self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
                self.assertIn("has drifted", checked.stderr)
                self.assertIn(name, checked.stderr)
                self.assertEqual(before, files(projection), "read-only check changed output")

    def test_descendant_swap_never_opens_or_reads_external_file(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        projection = out / "structure" / "act-history"
        before = files(projection)

        with tempfile.TemporaryDirectory() as external:
            sentinel = pathlib.Path(external) / "must-not-open.txt"
            sentinel.write_bytes(b"outside sentinel\n")
            sentinel_stat = sentinel.stat()
            original_reader = tool._read_structure_file
            original_open = tool.os.open
            original_read = tool.os.read
            accesses: list[str] = []
            swapped = False

            def is_sentinel(descriptor: int) -> bool:
                found = os.fstat(descriptor)
                return (found.st_dev, found.st_ino) == (
                    sentinel_stat.st_dev,
                    sentinel_stat.st_ino,
                )

            def guarded_open(path, flags, mode=0o777, *, dir_fd=None):
                descriptor = original_open(path, flags, mode, dir_fd=dir_fd)
                if is_sentinel(descriptor):
                    accesses.append("open")
                    os.close(descriptor)
                    raise AssertionError("external sentinel was opened")
                return descriptor

            def guarded_read(descriptor, amount):
                if is_sentinel(descriptor):
                    accesses.append("read")
                    raise AssertionError("external sentinel was read")
                return original_read(descriptor, amount)

            def swap_at_classification(parent_fd, name, expected, label):
                nonlocal swapped
                if not swapped and label == projection / "index.json":
                    swapped = True
                    retained = ".index.json-before-swap"
                    os.rename(
                        name,
                        retained,
                        src_dir_fd=parent_fd,
                        dst_dir_fd=parent_fd,
                    )
                    os.symlink(sentinel, name, dir_fd=parent_fd)
                    try:
                        return original_reader(parent_fd, name, expected, label)
                    finally:
                        os.unlink(name, dir_fd=parent_fd)
                        os.rename(
                            retained,
                            name,
                            src_dir_fd=parent_fd,
                            dst_dir_fd=parent_fd,
                        )
                return original_reader(parent_fd, name, expected, label)

            with mock.patch.object(
                tool, "_read_structure_file", side_effect=swap_at_classification
            ), mock.patch.object(tool.os, "open", side_effect=guarded_open), mock.patch.object(
                tool.os, "read", side_effect=guarded_read
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.structure_all(out, check_only=True)

            self.assertTrue(swapped, "the classification/open boundary was not exercised")
            self.assertEqual([], accesses)
            self.assertIn("changed while opening file", str(failure.exception))
            self.assertEqual(b"outside sentinel\n", sentinel.read_bytes())

        self.assertEqual(before, files(projection))
        checked = tool.structure_all(out, check_only=True)
        self.assertEqual(505, checked["files"])

        (projection / "index.json").write_text('{"stale":true}\n', encoding="utf-8")
        refreshed = tool.structure_all(out, check_only=False)
        self.assertIn("index.json", refreshed["updated"])
        self.assertEqual(files(TRACKED), files(projection))

    def test_descendant_directory_exchange_is_rejected_before_traversal(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        projection = out / "structure" / "act-history"
        original_open_child = tool._open_child_directory
        swapped = False
        retained = projection / ".latin-missal-before-swap"

        def swap_after_classification(parent_fd, parent, name, *, create):
            nonlocal swapped
            if not swapped and parent == projection and name == "latin-missal":
                swapped = True
                os.rename(
                    name,
                    retained.name,
                    src_dir_fd=parent_fd,
                    dst_dir_fd=parent_fd,
                )
                os.mkdir(name, dir_fd=parent_fd)
            return original_open_child(parent_fd, parent, name, create=create)

        try:
            with mock.patch.object(
                tool, "_open_child_directory", side_effect=swap_after_classification
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.structure_all(out, check_only=True)
            self.assertTrue(swapped, "the directory classification/open boundary was not exercised")
            self.assertIn("changed while opening directory", str(failure.exception))
        finally:
            replacement = projection / "latin-missal"
            if replacement.is_dir():
                replacement.rmdir()
            if retained.is_dir():
                retained.rename(replacement)

        checked = tool.structure_all(out, check_only=True)
        self.assertEqual(505, checked["files"])

    def test_projection_root_exchange_is_rejected_before_traversal(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        structure = out / "structure"
        projection = structure / "act-history"
        original_open_child = tool._open_child_directory
        swapped = False
        retained = structure / ".act-history-before-swap"

        def swap_after_classification(parent_fd, parent, name, *, create):
            nonlocal swapped
            if not swapped and parent == structure and name == "act-history":
                swapped = True
                os.rename(
                    name,
                    retained.name,
                    src_dir_fd=parent_fd,
                    dst_dir_fd=parent_fd,
                )
                os.mkdir(name, dir_fd=parent_fd)
            return original_open_child(parent_fd, parent, name, create=create)

        try:
            with mock.patch.object(
                tool, "_open_child_directory", side_effect=swap_after_classification
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.structure_all(out, check_only=True)
            self.assertTrue(swapped, "the projection-root open boundary was not exercised")
            self.assertIn("changed while opening directory", str(failure.exception))
        finally:
            if projection.is_dir():
                projection.rmdir()
            if retained.is_dir():
                retained.rename(projection)

        checked = tool.structure_all(out, check_only=True)
        self.assertEqual(505, checked["files"])

    def test_scoped_manifest_discovery_refuses_a_symlinked_map(self) -> None:
        tool = load_tool()
        with tempfile.TemporaryDirectory() as held, tempfile.TemporaryDirectory() as external:
            root = pathlib.Path(held)
            sentinel = pathlib.Path(external) / "outside.json"
            sentinel.write_text(
                '{"schema":"triptych-act-map/v1","slice":"outside"}\n',
                encoding="utf-8",
            )
            linked = root / "outside.json"
            linked.symlink_to(sentinel)
            with mock.patch.object(
                tool,
                "_read_structure_file",
                side_effect=AssertionError("symlink target reader was reached"),
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.held(root)

            self.assertIn("non-regular act-history map", str(failure.exception))
            self.assertEqual(
                '{"schema":"triptych-act-map/v1","slice":"outside"}\n',
                sentinel.read_text(encoding="utf-8"),
            )

    def test_full_writer_repairs_drift_and_prunes_only_its_owned_directory(self) -> None:
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        projection = out / "structure" / "act-history"
        (projection / "index.json").write_text('{"stale":true}\n', encoding="utf-8")
        (projection / "roman-holy-week/units.json").unlink()
        orphan = projection / "latin-missal/unit/retired-prayer.json"
        orphan.write_text("{}\n", encoding="utf-8")
        sibling = out / "structure" / "not-owned-by-act-history.txt"
        sibling.write_text("keep\n", encoding="utf-8")

        refreshed = run("structure", "--out", str(out), "--json")
        self.assertEqual(refreshed.returncode, 0, refreshed.stdout + refreshed.stderr)
        payload = json.loads(refreshed.stdout)
        self.assertIn("latin-missal/unit/retired-prayer.json", payload["removed"])
        self.assertIn("index.json", payload["updated"])
        self.assertIn("roman-holy-week/units.json", payload["updated"])
        self.assertEqual(files(TRACKED), files(projection))
        self.assertEqual("keep\n", sibling.read_text(encoding="utf-8"))

    def test_scoped_check_is_refused_instead_of_masquerading_as_complete(self) -> None:
        checked = run(
            "structure",
            "--check",
            "--source",
            "src/sources/inventories/roman-holy-week-acts-v1.toml",
        )
        self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
        self.assertIn("complete tracked projection", checked.stderr)

    def test_check_does_not_create_repository_build_or_a_missing_output(self) -> None:
        tool = load_tool()
        with tempfile.TemporaryDirectory() as held:
            sandbox = pathlib.Path(held) / "repository"
            sandbox.mkdir()
            output = sandbox / "data"
            tool.ROOT = sandbox

            with self.assertRaises(tool.Problem):
                tool.structure_all(output, check_only=True)

            self.assertFalse((sandbox / "build").exists())
            self.assertFalse(output.exists())

    def test_writer_and_check_reject_symlinked_and_non_directory_parents(self) -> None:
        with tempfile.TemporaryDirectory() as held, tempfile.TemporaryDirectory() as external:
            root = pathlib.Path(held)
            external_root = pathlib.Path(external)
            sentinel = external_root / "must-survive.txt"
            sentinel.write_text("external\n", encoding="utf-8")
            linked = root / "linked"
            linked.symlink_to(external_root, target_is_directory=True)

            for verb in (("structure", "--out", str(linked)), ("structure", "--check", "--out", str(linked))):
                with self.subTest(arguments=verb):
                    result = run(*verb)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn("symlinked structure output component", result.stderr)
                    self.assertEqual("external\n", sentinel.read_text(encoding="utf-8"))

            regular = root / "regular-file"
            regular.write_text("not a directory\n", encoding="utf-8")
            result = run("structure", "--out", str(regular))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("not a directory", result.stderr)

    def test_cleanup_swap_cannot_redirect_writer_deletion(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        with tempfile.TemporaryDirectory() as external:
            external_root = pathlib.Path(external)
            sentinel = external_root / "must-survive.txt"
            sentinel.write_text("outside\n", encoding="utf-8")
            original_remove = tool._remove_directory_entry

            def swap_before_cleanup(parent_fd: int, name: str) -> None:
                if "-retired-" not in name:
                    original_remove(parent_fd, name)
                    return
                saved = f"{name}.held"
                os.rename(name, saved, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
                os.symlink(
                    external_root,
                    name,
                    target_is_directory=True,
                    dir_fd=parent_fd,
                )
                try:
                    original_remove(parent_fd, name)
                finally:
                    try:
                        os.unlink(name, dir_fd=parent_fd)
                    except FileNotFoundError:
                        pass
                    original_remove(parent_fd, saved)

            with mock.patch.object(
                tool,
                "_remove_directory_entry",
                side_effect=swap_before_cleanup,
            ):
                result = tool.structure_all(out, check_only=False)

            self.assertEqual(505, result["files"])
            self.assertEqual("outside\n", sentinel.read_text(encoding="utf-8"))

    def test_staging_swap_cannot_redirect_writer_writes_or_install_symlink(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        projection = out / "structure" / "act-history"
        with tempfile.TemporaryDirectory() as external:
            external_root = pathlib.Path(external)
            sentinel = external_root / "must-survive.txt"
            sentinel.write_text("outside\n", encoding="utf-8")
            original_copytree = tool._copy_structure_tree
            saved: list[pathlib.Path] = []

            def swap_at_write_boundary(source, staged_fd):
                lexical = tool._descriptor_path(staged_fd).resolve()
                retained = lexical.with_name(lexical.name + ".held")
                lexical.rename(retained)
                lexical.symlink_to(external_root, target_is_directory=True)
                saved.append(retained)
                return original_copytree(source, staged_fd)

            with mock.patch.object(
                tool,
                "_copy_structure_tree",
                side_effect=swap_at_write_boundary,
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.structure_all(out, check_only=False)

            self.assertIn("changed during operation", str(failure.exception))
            self.assertEqual(
                ["must-survive.txt"],
                sorted(path.name for path in external_root.iterdir()),
            )
            self.assertEqual("outside\n", sentinel.read_text(encoding="utf-8"))
            self.assertTrue(projection.is_dir())
            self.assertFalse(projection.is_symlink())
            self.assertTrue(saved and saved[0].is_dir())

    def test_writer_rejects_success_if_held_structure_parent_was_detached(self) -> None:
        tool = load_tool()
        held, out = self.temporary_projection()
        self.addCleanup(held.cleanup)
        original_copy = tool._copy_structure_tree
        moved: list[tuple[pathlib.Path, pathlib.Path]] = []

        def detach_structure_parent(source, staged_fd):
            staged = tool._descriptor_path(staged_fd).resolve()
            parent = staged.parent
            retained = parent.with_name(parent.name + ".held")
            parent.rename(retained)
            parent.mkdir()
            moved.append((parent, retained))
            return original_copy(source, staged_fd)

        try:
            with mock.patch.object(
                tool,
                "_copy_structure_tree",
                side_effect=detach_structure_parent,
            ):
                with self.assertRaises(tool.Problem) as failure:
                    tool.structure_all(out, check_only=False)
            self.assertIn("changed during operation", str(failure.exception))
        finally:
            for parent, retained in moved:
                if parent.is_dir():
                    parent.rmdir()
                if retained.exists():
                    retained.rename(parent)


if __name__ == "__main__":
    unittest.main()
