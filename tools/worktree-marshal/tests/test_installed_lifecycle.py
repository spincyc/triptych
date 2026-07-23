#!/usr/bin/env python3
"""Bounded stateful lifecycle coverage for the sdist-rebuilt wheel."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import unittest
from pathlib import Path

if __package__:
    from ._artifact_fixture import (
        SETUPTOOLS_AVAILABLE,
        get_built_artifacts,
    )
else:
    from _artifact_fixture import (  # type: ignore[import-not-found]
        SETUPTOOLS_AVAILABLE,
        get_built_artifacts,
    )


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COMMAND_TIMEOUT_SECONDS = 60


FAKE_CODEX_SOURCE = """\
#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def git(cwd: Path, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )


arguments = sys.argv[1:]
workdir_index = arguments.index("-C")
workdir = Path(arguments[workdir_index + 1]).resolve()
root = Path(git(workdir, "rev-parse", "--show-toplevel").stdout.strip()).resolve()

action = os.environ.get("FAKE_CODEX_ACTION")
if action == "commit":
    (root / "agent-result.txt").write_text(
        os.environ.get("FAKE_CODEX_CONTENT", "installed result\\n"),
        encoding="utf-8",
    )
    git(root, "add", "agent-result.txt")
    git(root, "commit", "-m", "Installed agent result")
elif action == "stage-conflict":
    conflict = root / os.environ.get(
        "FAKE_CODEX_CONFLICT_PATH",
        "agent-result.txt",
    )
    conflict.write_text(
        os.environ.get("FAKE_CODEX_CONTENT", "installed resolved result\\n"),
        encoding="utf-8",
    )
    git(root, "add", str(conflict.relative_to(root)))

raise SystemExit(int(os.environ.get("FAKE_CODEX_EXIT", "0")))
"""


class InstalledLifecycleTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def checked(
        cls,
        arguments: list[str],
        *,
        cwd: Path,
        environment: dict[str, str],
        purpose: str,
        timeout: int = COMMAND_TIMEOUT_SECONDS,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            arguments,
            cwd=cwd,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        if result.returncode:
            raise AssertionError(
                f"{purpose} failed with status {result.returncode}\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )
        return result

    @classmethod
    def setUpClass(cls) -> None:
        if not SETUPTOOLS_AVAILABLE:
            raise AssertionError("setuptools build backend is unavailable")
        git = shutil.which("git")
        if git is None:
            raise AssertionError("Git is unavailable")
        cls.git_executable = Path(git).resolve()
        make = shutil.which("make")
        if make is None:
            raise AssertionError("GNU Make is unavailable")
        make_version = subprocess.run(
            [make, "--version"],
            text=True,
            capture_output=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
        if make_version.returncode or "GNU Make" not in make_version.stdout:
            raise AssertionError("GNU Make is unavailable")
        cls.make_executable = Path(make).resolve()

        artifacts = get_built_artifacts(PACKAGE_ROOT)
        cls.artifacts = artifacts
        cls.root = artifacts.root
        cls.copied_build_source = artifacts.copied_source
        cls.extracted_sdist = artifacts.extracted_sdist
        cls.venv = artifacts.venv
        cls.venv_bin = artifacts.venv_bin
        cls.venv_python = artifacts.venv_python
        cls.console = artifacts.installed_command

    def setUp(self) -> None:
        self.case = self.artifacts.new_case(
            prefix="outside-checkout-",
        )
        self.addCleanup(self.case.cleanup)
        self.lifecycle_root = Path(self.case.name)
        self.control = self.lifecycle_root / "control"
        self.consumer = self.lifecycle_root / "consumer"
        self.home = self.lifecycle_root / "home"
        self.bin = self.lifecycle_root / "bin"
        self.consumer_fragment = self.consumer / "worktree-marshal.mk"
        self.consumer_makefile = self.consumer / "Makefile"
        self.consumer_console = self.consumer / "worktree-marshal"
        self.control.mkdir(parents=True)
        self.consumer.mkdir()
        self.home.mkdir()
        self.bin.mkdir()
        self.fake_codex = self.bin / "codex"
        self.fake_codex.write_text(FAKE_CODEX_SOURCE, encoding="utf-8")
        self.fake_codex.chmod(0o755)
        self.compatibility = self.bin / "triptych-compat-installed"
        self.compatibility.write_text(
            (
                f"#!{self.venv_python}\n"
                "from pathlib import Path\n"
                "from worktree_marshal import triptych_compat\n\n"
                "raise SystemExit(\n"
                "    triptych_compat.main(invocation_path=Path(__file__).resolve())\n"
                ")\n"
            ),
            encoding="utf-8",
        )
        self.compatibility.chmod(0o755)
        self.generic_state = self.lifecycle_root / "generic-state"
        self.triptych_state = self.lifecycle_root / "triptych-state"

        self.git("init", "-b", "main")
        self.git("config", "user.name", "Worktree Marshal Installed Test")
        self.git("config", "user.email", "marshal-installed@example.invalid")
        self.git("config", "commit.gpgSign", "false")
        (self.control / "baseline.txt").write_text("baseline\n", encoding="utf-8")
        self.git("add", "baseline.txt")
        self.git("commit", "-m", "Synthetic installed baseline")
        self.installed_origins = self.prepare_installed_consumer()

    @property
    def generic_profile_state(self) -> Path:
        return self.generic_state / "profiles" / "generic-v1"

    def environment(self, additions: dict[str, str] | None = None) -> dict[str, str]:
        environment = os.environ.copy()
        for name in list(environment):
            if (
                name.startswith("WORKTREE_MARSHAL_")
                or name.startswith("TRIPTYCH_CODEX_")
                or name
                in {
                    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                    "GIT_COMMON_DIR",
                    "GIT_DIR",
                    "GIT_INDEX_FILE",
                    "GIT_OBJECT_DIRECTORY",
                    "GIT_PREFIX",
                    "GIT_WORK_TREE",
                    "GNUMAKEFLAGS",
                    "MAKEFILES",
                    "MAKEFLAGS",
                    "MAKELEVEL",
                    "MAKEOVERRIDES",
                    "MFLAGS",
                    "PYTHONHOME",
                    "PYTHONPATH",
                    "RUN",
                }
            ):
                environment.pop(name, None)
        search_path = [
            str(self.venv_bin),
            str(self.git_executable.parent),
            *os.defpath.split(os.pathsep),
        ]
        environment.update(
            {
                "HOME": str(self.home),
                "PATH": os.pathsep.join(dict.fromkeys(search_path)),
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_NOSYSTEM": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1",
                "XDG_STATE_HOME": str(self.lifecycle_root / "xdg-state"),
                "WORKTREE_MARSHAL_REAL_CODEX": str(self.fake_codex),
                "WORKTREE_MARSHAL_STATE_DIR": str(self.generic_state),
                "TRIPTYCH_CODEX_REAL": str(self.fake_codex),
                "TRIPTYCH_CODEX_STATE_DIR": str(self.triptych_state),
            }
        )
        if additions:
            environment.update(additions)
        return environment

    def git(
        self,
        *arguments: str,
        check: bool = True,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.git_executable), *arguments],
            cwd=cwd or self.control,
            env=self.environment(),
            text=True,
            capture_output=True,
            check=check,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    def run_console(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.console), *arguments],
            cwd=self.control,
            env=self.environment(environment),
            text=True,
            capture_output=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    def run_compatibility(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.compatibility), *arguments],
            cwd=self.control,
            env=self.environment(environment),
            text=True,
            capture_output=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    def run_make(
        self,
        *arguments: str,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(self.make_executable),
                "--no-print-directory",
                "-f",
                str(self.consumer_makefile),
                *arguments,
            ],
            cwd=self.control,
            env=self.environment(environment),
            text=True,
            capture_output=True,
            check=False,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

    @staticmethod
    def manifests(state_root: Path) -> set[Path]:
        return set(state_root.glob("*/runs/*.json"))

    @staticmethod
    def manifest_snapshot(path: Path) -> tuple[bytes, int, int]:
        metadata = path.stat()
        return path.read_bytes(), metadata.st_mode, metadata.st_mtime_ns

    def prepare_installed_consumer(self) -> dict[str, Path]:
        provenance = self.checked(
            [
                str(self.venv_python),
                "-c",
                "\n".join(
                    (
                        "import json",
                        "from importlib.resources import files",
                        "import worktree_marshal",
                        "import worktree_marshal.resources as resources",
                        (
                            "from worktree_marshal import "
                            "cli, engine, profiles, triptych_compat"
                        ),
                        (
                            "fragment = files('worktree_marshal.resources')"
                            ".joinpath('worktree-marshal.mk')"
                        ),
                        "print(json.dumps({",
                        "    'package': worktree_marshal.__file__,",
                        "    'cli': cli.__file__,",
                        "    'engine': engine.__file__,",
                        "    'profiles': profiles.__file__,",
                        "    'triptych_compat': triptych_compat.__file__,",
                        "    'resources': resources.__file__,",
                        "    'make_fragment': str(fragment),",
                        "}, sort_keys=True))",
                    )
                ),
            ],
            cwd=self.control,
            environment=self.environment(),
            purpose="installed-package provenance check",
        )
        origins = {
            name: Path(value).resolve()
            for name, value in json.loads(provenance.stdout).items()
        }
        for name, origin in origins.items():
            with self.subTest(installed_origin=name):
                self.assertTrue(origin.is_relative_to(self.venv), origin)
                self.assertFalse(origin.is_relative_to(PACKAGE_ROOT), origin)
                self.assertTrue(origin.is_file(), origin)

        installed_fragment = origins["make_fragment"]
        shutil.copy2(installed_fragment, self.consumer_fragment)
        self.consumer_console.symlink_to(self.console)
        self.consumer_makefile.write_text(
            (
                "override WORKTREE_MARSHAL := ../consumer/worktree-marshal\n"
                "include ../consumer/worktree-marshal.mk\n"
            ),
            encoding="utf-8",
        )
        self.assertEqual(
            self.consumer_fragment.read_bytes(),
            installed_fragment.read_bytes(),
        )
        self.assertFalse(
            self.consumer_makefile.resolve().is_relative_to(self.control.resolve())
        )
        self.assertFalse(
            self.consumer_fragment.resolve().is_relative_to(self.control.resolve())
        )
        self.assertEqual(self.consumer_console.resolve(), self.console.resolve())
        self.assertEqual(self.git("status", "--porcelain").stdout, "")
        return origins

    def active_rebase_paths(self, worker: Path) -> list[Path]:
        paths: list[Path] = []
        for name in ("rebase-merge", "rebase-apply"):
            path = Path(
                self.git(
                    "rev-parse",
                    "--git-path",
                    name,
                    cwd=worker,
                ).stdout.strip()
            )
            if not path.is_absolute():
                path = worker / path
            if path.exists():
                paths.append(path)
        return paths

    def worktree_paths(self) -> list[Path]:
        return [
            Path(line.removeprefix("worktree ")).resolve()
            for line in self.git("worktree", "list", "--porcelain").stdout.splitlines()
            if line.startswith("worktree ")
        ]

    def ref_oid(self, ref: str) -> str | None:
        result = self.git("rev-parse", "--verify", ref, check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    def launch_and_read_manifest(
        self,
        state_root: Path,
        *arguments: str,
        expected_status: int,
        environment: dict[str, str] | None = None,
        compatibility: bool = False,
    ) -> tuple[Path, dict]:
        before = self.manifests(state_root)
        runner = self.run_compatibility if compatibility else self.run_console
        launched = runner(*arguments, environment=environment)
        self.assertEqual(launched.returncode, expected_status, launched.stderr)
        created = self.manifests(state_root) - before
        self.assertEqual(len(created), 1, created)
        path = created.pop()
        return path, json.loads(path.read_text(encoding="utf-8"))

    def test_sdist_rebuilt_wheel_runs_generic_and_triptych_lifecycles(self) -> None:
        self.assertFalse(self.control.resolve().is_relative_to(PACKAGE_ROOT))
        self.assertFalse(self.copied_build_source.exists())
        self.assertFalse(self.extracted_sdist.exists())
        self.assertNotIn("PYTHONPATH", self.environment())
        self.assertNotIn("PYTHONHOME", self.environment())
        self.assertTrue(self.compatibility.resolve().is_relative_to(self.lifecycle_root))
        self.assertTrue(self.venv_python.is_relative_to(self.venv))
        self.assertEqual(
            self.compatibility.read_text(encoding="utf-8").splitlines()[0],
            f"#!{self.venv_python}",
        )

        hardlink = self.bin / "worktree-marshal-hardlink"
        symlink = self.bin / "worktree-marshal-symlink"
        os.link(self.console, hardlink)
        symlink.symlink_to(self.console)
        for candidate in (self.console, hardlink, symlink):
            with self.subTest(real_agent=candidate.name):
                rejected = self.run_console(
                    "--profile",
                    "generic-v1",
                    "run",
                    "--agent",
                    "codex",
                    environment={"WORKTREE_MARSHAL_REAL_CODEX": str(candidate)},
                )
                self.assertEqual(rejected.returncode, 2, rejected.stderr)
                self.assertIn("non-launcher executable", rejected.stderr)
        self.assertEqual(self.manifests(self.generic_profile_state), set())
        self.assertEqual(self.manifests(self.triptych_state), set())
        worktrees = self.git("worktree", "list", "--porcelain").stdout
        self.assertEqual(worktrees.count("worktree "), 1)

        before_committed = self.manifests(self.generic_profile_state)
        committed_launch = self.run_make(
            "codex",
            environment={"FAKE_CODEX_ACTION": "commit"},
        )
        self.assertEqual(
            committed_launch.returncode,
            0,
            committed_launch.stderr,
        )
        created_committed = (
            self.manifests(self.generic_profile_state) - before_committed
        )
        self.assertEqual(len(created_committed), 1, created_committed)
        committed_path = created_committed.pop()
        committed = json.loads(committed_path.read_text(encoding="utf-8"))
        committed_id = committed["run_id"]
        committed_head = committed["final_head"]
        self.assertEqual(committed["state"], "preserved")
        self.assertFalse(committed["dirty"])
        self.assertEqual(committed["profile_id"], "generic-v1")
        self.assertEqual(committed["agent"], "codex")

        generic_before_cross_profile = self.manifest_snapshot(committed_path)
        cross_profile = self.run_console(
            "--profile", "triptych", "status", committed_id
        )
        self.assertEqual(cross_profile.returncode, 2, cross_profile.stderr)
        self.assertIn(
            f"unknown Triptych Codex run {committed_id}",
            cross_profile.stderr,
        )
        self.assertEqual(
            self.manifest_snapshot(committed_path),
            generic_before_cross_profile,
        )
        self.assertFalse(
            any(path.stem == committed_id for path in self.manifests(self.triptych_state))
        )
        self.assertTrue(Path(committed["worktree"]).is_dir())

        status = self.run_make("status", f"RUN={committed_id}")
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertIn(committed_id, status.stdout)
        self.assertIn("preserved", status.stdout)

        integrated = self.run_make("integrate", f"RUN={committed_id}")
        self.assertEqual(integrated.returncode, 0, integrated.stderr)
        committed_cleaned = json.loads(committed_path.read_text(encoding="utf-8"))
        self.assertEqual(committed_cleaned["state"], "cleaned")
        self.assertEqual(committed_cleaned["integrated_head"], committed_head)
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            committed_head,
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "installed result\n",
        )
        self.assertEqual(self.git("status", "--porcelain").stdout, "")
        self.assertFalse(Path(committed["worktree"]).exists())
        self.assertFalse(Path(committed["tmpdir"]).exists())

        clean_path, clean_run = self.launch_and_read_manifest(
            self.generic_profile_state,
            "--profile",
            "generic-v1",
            "run",
            "--agent",
            "codex",
            expected_status=3,
            environment={"FAKE_CODEX_EXIT": "3"},
        )
        self.assertEqual(clean_run["state"], "failed-preserved")
        self.assertFalse(clean_run["dirty"])
        cleaned = self.run_make("clean-run", f"RUN={clean_run['run_id']}")
        self.assertEqual(cleaned.returncode, 0, cleaned.stderr)
        self.assertEqual(
            json.loads(clean_path.read_text(encoding="utf-8"))["state"],
            "cleaned",
        )
        self.assertFalse(Path(clean_run["worktree"]).exists())
        self.assertFalse(Path(clean_run["tmpdir"]).exists())

        compatibility_path, compatibility_run = self.launch_and_read_manifest(
            self.triptych_state,
            "installed compatibility run",
            expected_status=3,
            environment={"FAKE_CODEX_EXIT": "3"},
            compatibility=True,
        )
        compatibility_id = compatibility_run["run_id"]
        self.assertEqual(compatibility_run["state"], "failed-preserved")
        self.assertNotIn("profile_id", compatibility_run)
        self.assertNotIn("agent", compatibility_run)

        compatibility_before_cross_profile = self.manifest_snapshot(
            compatibility_path
        )
        generic_cross_profile = self.run_console(
            "--profile", "generic-v1", "status", compatibility_id
        )
        self.assertEqual(
            generic_cross_profile.returncode,
            2,
            generic_cross_profile.stderr,
        )
        self.assertIn(
            f"unknown Worktree Marshal run {compatibility_id}",
            generic_cross_profile.stderr,
        )
        self.assertEqual(
            self.manifest_snapshot(compatibility_path),
            compatibility_before_cross_profile,
        )
        self.assertFalse(
            any(
                path.stem == compatibility_id
                for path in self.manifests(self.generic_profile_state)
            )
        )
        self.assertTrue(Path(compatibility_run["worktree"]).is_dir())

        compatibility_status = self.run_console(
            "--profile", "triptych", "status", compatibility_id
        )
        self.assertEqual(
            compatibility_status.returncode,
            0,
            compatibility_status.stderr,
        )
        self.assertIn(compatibility_id, compatibility_status.stdout)
        self.assertIn("failed-preserved", compatibility_status.stdout)
        compatibility_cleaned = self.run_console(
            "--profile", "triptych", "clean", compatibility_id
        )
        self.assertEqual(
            compatibility_cleaned.returncode,
            0,
            compatibility_cleaned.stderr,
        )
        self.assertEqual(
            json.loads(compatibility_path.read_text(encoding="utf-8"))["state"],
            "cleaned",
        )
        self.assertFalse(Path(compatibility_run["worktree"]).exists())

        triptych_path, triptych = self.launch_and_read_manifest(
            self.triptych_state,
            "--profile",
            "triptych",
            "run",
            "--agent",
            "codex",
            expected_status=3,
            environment={"FAKE_CODEX_EXIT": "3"},
        )
        triptych_id = triptych["run_id"]
        self.assertEqual(triptych["state"], "failed-preserved")
        self.assertNotIn("profile_id", triptych)
        self.assertNotIn("agent", triptych)
        triptych_status = self.run_compatibility(
            "--triptych-status", triptych_id
        )
        self.assertEqual(triptych_status.returncode, 0, triptych_status.stderr)
        self.assertIn(triptych_id, triptych_status.stdout)
        self.assertIn("failed-preserved", triptych_status.stdout)
        triptych_cleaned = self.run_compatibility(
            "--triptych-clean", triptych_id
        )
        self.assertEqual(triptych_cleaned.returncode, 0, triptych_cleaned.stderr)
        self.assertEqual(
            json.loads(triptych_path.read_text(encoding="utf-8"))["state"],
            "cleaned",
        )
        self.assertFalse(Path(triptych["worktree"]).exists())
        self.assertEqual(
            self.manifests(self.triptych_state),
            {compatibility_path, triptych_path},
        )

    def test_installed_generic_managed_conflict_lifecycle(self) -> None:
        before = self.manifests(self.generic_profile_state)
        launched = self.run_make(
            "codex",
            environment={
                "FAKE_CODEX_ACTION": "commit",
                "FAKE_CODEX_CONTENT": "installed worker result\n",
            },
        )
        self.assertEqual(launched.returncode, 0, launched.stderr)
        created = self.manifests(self.generic_profile_state) - before
        self.assertEqual(len(created), 1, created)
        manifest_path = created.pop()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        run_id = manifest["run_id"]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]
        source_anchor = (
            f"refs/worktree-marshal/generic-v1/runs/{run_id}/"
            "integration-source"
        )
        self.assertEqual(manifest["state"], "preserved")
        self.assertFalse(manifest["dirty"])
        self.assertEqual(manifest["format_id"], "worktree-marshal-run")
        self.assertEqual(manifest["profile_id"], "generic-v1")
        self.assertEqual(manifest["agent"], "codex")

        (self.control / "agent-result.txt").write_text(
            "installed conflicting target\n",
            encoding="utf-8",
        )
        self.git("add", "agent-result.txt")
        self.git("commit", "-m", "Add installed conflicting target")
        target_head = self.git("rev-parse", "HEAD").stdout.strip()

        conflicted_result = self.run_make("integrate", f"RUN={run_id}")
        self.assertEqual(
            conflicted_result.returncode,
            2,
            conflicted_result.stderr,
        )
        self.assertIn("conflict", conflicted_result.stderr.lower())
        self.assertNotIn(str(worker), conflicted_result.stderr)
        conflicted = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(conflicted["state"], "integration-conflict")
        self.assertEqual(conflicted["final_head"], source_head)
        self.assertEqual(conflicted["integration_source_head"], source_head)
        self.assertEqual(conflicted["integration_target_head"], target_head)
        self.assertEqual(
            conflicted["integration_conflict_paths"],
            ["agent-result.txt"],
        )
        self.assertNotIn("integration_candidate_head", conflicted)
        self.assertNotIn("integrated_head", conflicted)
        self.assertEqual(self.ref_oid(source_anchor), source_head)
        self.assertTrue(self.active_rebase_paths(worker))
        self.assertEqual(
            self.git(
                "diff",
                "--name-only",
                "--diff-filter=U",
                cwd=worker,
            ).stdout.splitlines(),
            ["agent-result.txt"],
        )
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            target_head,
        )

        resolved = self.run_make(
            "resolve",
            f"RUN={run_id}",
            environment={
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_CONTENT": "installed resolved result\n",
            },
        )
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        staged = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(staged["state"], "integration-conflict")
        self.assertNotIn("integration_candidate_head", staged)
        self.assertEqual(
            self.git(
                "diff",
                "--name-only",
                "--diff-filter=U",
                cwd=worker,
            ).stdout,
            "",
        )
        self.assertEqual(
            self.git(
                "diff",
                "--cached",
                "--name-only",
                cwd=worker,
            ).stdout.splitlines(),
            ["agent-result.txt"],
        )

        continued = self.run_make("continue", f"RUN={run_id}")
        self.assertEqual(continued.returncode, 0, continued.stderr)
        self.assertIn("review", continued.stderr.lower())
        pending = json.loads(manifest_path.read_text(encoding="utf-8"))
        candidate_head = pending["integration_candidate_head"]
        self.assertEqual(pending["state"], "integration-review-pending")
        self.assertTrue(pending["integration_manual_resolution"])
        self.assertEqual(pending["integration_unmerged_paths"], [])
        self.assertEqual(pending["integration_source_head"], source_head)
        self.assertEqual(pending["integration_target_head"], target_head)
        self.assertNotEqual(candidate_head, source_head)
        self.assertEqual(
            self.git("rev-parse", "HEAD", cwd=worker).stdout.strip(),
            candidate_head,
        )
        self.assertEqual(
            self.git("rev-parse", "HEAD^", cwd=worker).stdout.strip(),
            target_head,
        )
        self.assertEqual(
            self.git("status", "--porcelain=v1", cwd=worker).stdout,
            "",
        )
        self.assertEqual(
            self.git(
                "symbolic-ref",
                "--short",
                "HEAD",
                cwd=worker,
            ).stdout.strip(),
            manifest["branch"],
        )
        self.assertEqual(self.active_rebase_paths(worker), [])
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            target_head,
        )

        manifest_before_diff = self.manifest_snapshot(manifest_path)
        worker_status_before_diff = self.git(
            "status",
            "--porcelain=v1",
            cwd=worker,
        ).stdout
        control_status_before_diff = self.git(
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ).stdout
        reviewed = self.run_make("final-diff", f"RUN={run_id}")
        self.assertEqual(reviewed.returncode, 0, reviewed.stderr)
        self.assertIn("installed conflicting target", reviewed.stdout)
        self.assertIn("installed resolved result", reviewed.stdout)
        for private_path in (
            str(self.control),
            str(worker),
            manifest["tmpdir"],
            str(self.generic_state),
        ):
            self.assertNotIn(private_path, reviewed.stdout)
            self.assertNotIn(private_path, reviewed.stderr)
        self.assertEqual(
            self.manifest_snapshot(manifest_path),
            manifest_before_diff,
        )
        self.assertEqual(
            self.git("rev-parse", "HEAD", cwd=worker).stdout.strip(),
            candidate_head,
        )
        self.assertEqual(
            self.git("status", "--porcelain=v1", cwd=worker).stdout,
            worker_status_before_diff,
        )
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            target_head,
        )
        self.assertEqual(
            self.git(
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
            ).stdout,
            control_status_before_diff,
        )

        landed = self.run_make("integrate", f"RUN={run_id}")
        self.assertEqual(landed.returncode, 0, landed.stderr)
        cleaned = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(cleaned["state"], "cleaned")
        self.assertEqual(cleaned["integration_candidate_head"], candidate_head)
        self.assertEqual(cleaned["integrated_head"], candidate_head)
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            candidate_head,
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "installed resolved result\n",
        )
        self.assertEqual(self.git("status", "--porcelain=v1").stdout, "")
        self.assertEqual(self.worktree_paths(), [self.control.resolve()])
        self.assertFalse(worker.exists())
        self.assertFalse(Path(manifest["tmpdir"]).exists())
        self.assertIsNone(self.ref_oid(f"refs/heads/{manifest['branch']}"))
        self.assertIsNone(self.ref_oid(source_anchor))

    def test_installed_triptych_conflict_abort_restores_audited_source(
        self,
    ) -> None:
        manifest_path, manifest = self.launch_and_read_manifest(
            self.triptych_state,
            "installed Triptych conflict run",
            expected_status=0,
            environment={
                "FAKE_CODEX_ACTION": "commit",
                "FAKE_CODEX_CONTENT": "installed Triptych worker result\n",
            },
            compatibility=True,
        )
        run_id = manifest["run_id"]
        worker = Path(manifest["worktree"])
        source_head = manifest["final_head"]
        source_anchor = (
            f"refs/triptych-codex/runs/{run_id}/integration-source"
        )
        self.assertEqual(manifest["state"], "preserved")
        self.assertNotIn("format_id", manifest)
        self.assertNotIn("profile_id", manifest)
        self.assertNotIn("agent", manifest)

        (self.control / "agent-result.txt").write_text(
            "installed Triptych conflicting target\n",
            encoding="utf-8",
        )
        self.git("add", "agent-result.txt")
        self.git("commit", "-m", "Add installed Triptych conflicting target")
        target_head = self.git("rev-parse", "HEAD").stdout.strip()

        conflicted_result = self.run_console(
            "--profile",
            "triptych",
            "integrate",
            run_id,
        )
        self.assertEqual(
            conflicted_result.returncode,
            2,
            conflicted_result.stderr,
        )
        conflicted = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(conflicted["state"], "integration-conflict")
        self.assertEqual(conflicted["integration_source_head"], source_head)
        self.assertEqual(conflicted["integration_target_head"], target_head)
        self.assertEqual(
            conflicted["integration_conflict_paths"],
            ["agent-result.txt"],
        )
        self.assertEqual(self.ref_oid(source_anchor), source_head)
        self.assertTrue(self.active_rebase_paths(worker))

        resolved = self.run_console(
            "--profile",
            "triptych",
            "resolve",
            run_id,
            environment={
                "FAKE_CODEX_ACTION": "stage-conflict",
                "FAKE_CODEX_CONTENT": "discarded Triptych resolution\n",
            },
        )
        self.assertEqual(resolved.returncode, 0, resolved.stderr)
        self.assertEqual(
            self.git(
                "diff",
                "--name-only",
                "--diff-filter=U",
                cwd=worker,
            ).stdout,
            "",
        )
        self.assertEqual(
            self.git(
                "diff",
                "--cached",
                "--name-only",
                cwd=worker,
            ).stdout.splitlines(),
            ["agent-result.txt"],
        )
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "discarded Triptych resolution\n",
        )

        aborted = self.run_console(
            "--profile",
            "triptych",
            "abort",
            run_id,
        )
        self.assertEqual(aborted.returncode, 0, aborted.stderr)
        self.assertIn("restored", aborted.stderr.lower())
        self.assertEqual(
            self.git("rev-parse", "refs/heads/main").stdout.strip(),
            target_head,
        )
        self.assertEqual(
            (self.control / "agent-result.txt").read_text(encoding="utf-8"),
            "installed Triptych conflicting target\n",
        )
        self.assertEqual(
            self.git("rev-parse", "HEAD", cwd=worker).stdout.strip(),
            source_head,
        )
        self.assertEqual(
            self.git("status", "--porcelain=v1", cwd=worker).stdout,
            "",
        )
        self.assertEqual(
            self.git(
                "symbolic-ref",
                "--short",
                "HEAD",
                cwd=worker,
            ).stdout.strip(),
            manifest["branch"],
        )
        self.assertEqual(self.active_rebase_paths(worker), [])
        self.assertEqual(
            (worker / "agent-result.txt").read_text(encoding="utf-8"),
            "installed Triptych worker result\n",
        )

        restored = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(restored["state"], "preserved")
        self.assertEqual(restored["final_head"], source_head)
        self.assertNotIn("format_id", restored)
        self.assertNotIn("profile_id", restored)
        self.assertNotIn("agent", restored)
        self.assertEqual(
            restored["last_integration_source_head"],
            source_head,
        )
        self.assertEqual(
            restored["last_integration_target_head"],
            target_head,
        )
        self.assertEqual(
            restored["last_integration_conflict_paths"],
            ["agent-result.txt"],
        )
        self.assertIn("last_integration_aborted_at", restored)
        self.assertEqual(
            [key for key in restored if key.startswith("integration_")],
            [],
        )
        self.assertIsNone(self.ref_oid(source_anchor))
        self.assertTrue(worker.is_dir())
        self.assertTrue(Path(manifest["tmpdir"]).is_dir())
        self.assertEqual(
            self.ref_oid(f"refs/heads/{manifest['branch']}"),
            source_head,
        )
        self.assertEqual(
            set(self.worktree_paths()),
            {self.control.resolve(), worker.resolve()},
        )
        self.assertEqual(self.manifests(self.generic_profile_state), set())


if __name__ == "__main__":
    unittest.main()
