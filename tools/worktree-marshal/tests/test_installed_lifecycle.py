#!/usr/bin/env python3
"""Bounded stateful lifecycle coverage for the sdist-rebuilt wheel."""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SETUPTOOLS_AVAILABLE = importlib.util.find_spec("setuptools") is not None
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

if os.environ.get("FAKE_CODEX_ACTION") == "commit":
    (root / "agent-result.txt").write_text("installed result\\n", encoding="utf-8")
    git(root, "add", "agent-result.txt")
    git(root, "commit", "-m", "Installed agent result")

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

        cls.temporary = tempfile.TemporaryDirectory(
            prefix="worktree-marshal-installed-lifecycle-"
        )
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        source = cls.root / "source"
        sdist_artifacts = cls.root / "sdist-artifacts"
        rebuilt_artifacts = cls.root / "rebuilt-artifacts"
        extracted = cls.root / "extracted-sdist"
        cls.copied_build_source = source
        cls.extracted_sdist = extracted
        shutil.copytree(
            PACKAGE_ROOT,
            source,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                "*.pyo",
                "*.egg-info",
                "build",
                "dist",
            ),
        )
        sdist_artifacts.mkdir()
        rebuilt_artifacts.mkdir()
        extracted.mkdir()

        build_environment = os.environ.copy()
        build_environment.pop("PYTHONHOME", None)
        build_environment.pop("PYTHONPATH", None)
        build_environment["PYTHONDONTWRITEBYTECODE"] = "1"
        cls.checked(
            [
                sys.executable,
                "-c",
                (
                    "import pathlib, sys; "
                    "from setuptools.build_meta import build_sdist; "
                    "build_sdist(str(pathlib.Path(sys.argv[1])))"
                ),
                str(sdist_artifacts),
            ],
            cwd=source,
            environment=build_environment,
            purpose="source-distribution build",
        )
        source_distributions = sorted(sdist_artifacts.glob("*.tar.gz"))
        if len(source_distributions) != 1:
            raise AssertionError(
                "expected one source distribution; "
                f"found {source_distributions!r}"
            )
        cls.source_distribution = source_distributions[0]

        with tarfile.open(cls.source_distribution, mode="r:gz") as archive:
            archive.extractall(extracted)
        extracted_roots = [path for path in extracted.iterdir() if path.is_dir()]
        if len(extracted_roots) != 1:
            raise AssertionError(
                "expected one extracted source-distribution root; "
                f"found {extracted_roots!r}"
            )
        cls.checked(
            [
                sys.executable,
                "-c",
                (
                    "import pathlib, sys; "
                    "from setuptools.build_meta import build_wheel; "
                    "build_wheel(str(pathlib.Path(sys.argv[1])))"
                ),
                str(rebuilt_artifacts),
            ],
            cwd=extracted_roots[0],
            environment=build_environment,
            purpose="wheel rebuild from source distribution",
        )
        wheels = sorted(rebuilt_artifacts.glob("*.whl"))
        if len(wheels) != 1:
            raise AssertionError(
                "expected one wheel rebuilt from the source distribution; "
                f"found {wheels!r}"
            )
        cls.sdist_wheel = wheels[0]

        cls.venv = cls.root / "venv"
        cls.checked(
            [sys.executable, "-m", "venv", str(cls.venv)],
            cwd=cls.root,
            environment=build_environment,
            purpose="virtual-environment creation",
        )
        cls.venv_bin = cls.venv / "bin"
        cls.venv_python = cls.venv_bin / "python"
        cls.console = cls.venv_bin / "worktree-marshal"
        cls.checked(
            [
                str(cls.venv_python),
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "--no-cache-dir",
                "--no-deps",
                "--no-index",
                str(cls.sdist_wheel),
            ],
            cwd=cls.root,
            environment=build_environment,
            purpose="sdist-rebuilt wheel installation",
        )
        if not cls.console.is_file():
            raise AssertionError("the rebuilt wheel did not install its console script")
        for build_tree in (cls.copied_build_source, cls.extracted_sdist):
            if build_tree.parent != cls.root:
                raise AssertionError(f"refusing to remove unexpected path {build_tree}")
            shutil.rmtree(build_tree)
            if build_tree.exists():
                raise AssertionError(f"temporary build tree remains at {build_tree}")

    def setUp(self) -> None:
        self.case = tempfile.TemporaryDirectory(
            dir=self.root,
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
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.git_executable), *arguments],
            cwd=self.control,
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


if __name__ == "__main__":
    unittest.main()
