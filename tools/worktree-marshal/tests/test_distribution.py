#!/usr/bin/env python3
"""Build and inspect the extraction-stage wheel and source distribution."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SETUPTOOLS_AVAILABLE = importlib.util.find_spec("setuptools") is not None


@unittest.skipUnless(SETUPTOOLS_AVAILABLE, "setuptools build backend is unavailable")
class DistributionArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary_directory = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temporary_directory.cleanup)
        temporary_root = Path(cls.temporary_directory.name)
        source = temporary_root / "source"
        artifacts = temporary_root / "artifacts"
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
        artifacts.mkdir()
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        build = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import pathlib, sys; "
                    "from setuptools.build_meta import build_sdist, build_wheel; "
                    "output = pathlib.Path(sys.argv[1]); "
                    "build_sdist(str(output)); "
                    "build_wheel(str(output))"
                ),
                str(artifacts),
            ],
            cwd=source,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if build.returncode:
            raise AssertionError(
                "distribution build failed\n"
                f"stdout:\n{build.stdout}\n"
                f"stderr:\n{build.stderr}"
            )
        wheels = sorted(artifacts.glob("*.whl"))
        source_distributions = sorted(artifacts.glob("*.tar.gz"))
        if len(wheels) != 1 or len(source_distributions) != 1:
            raise AssertionError(
                "expected one wheel and one source distribution; "
                f"found wheels={wheels!r}, source distributions={source_distributions!r}"
            )
        cls.wheel = wheels[0]
        cls.source_distribution = source_distributions[0]

        extracted = temporary_root / "extracted-sdist"
        extracted.mkdir()
        with tarfile.open(cls.source_distribution, mode="r:gz") as archive:
            archive.extractall(extracted)
        extracted_roots = [path for path in extracted.iterdir() if path.is_dir()]
        if len(extracted_roots) != 1:
            raise AssertionError(
                "expected one extracted source-distribution root; "
                f"found {extracted_roots!r}"
            )

        rebuilt_artifacts = temporary_root / "rebuilt-artifacts"
        rebuilt_artifacts.mkdir()
        rebuilt = subprocess.run(
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
            env=environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if rebuilt.returncode:
            raise AssertionError(
                "wheel build from source distribution failed\n"
                f"stdout:\n{rebuilt.stdout}\n"
                f"stderr:\n{rebuilt.stderr}"
            )
        rebuilt_wheels = sorted(rebuilt_artifacts.glob("*.whl"))
        if len(rebuilt_wheels) != 1:
            raise AssertionError(
                "expected one wheel rebuilt from the source distribution; "
                f"found {rebuilt_wheels!r}"
            )
        cls.sdist_wheel = rebuilt_wheels[0]

        cls.venv = temporary_root / "venv"
        create_venv = subprocess.run(
            [sys.executable, "-m", "venv", str(cls.venv)],
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if create_venv.returncode:
            raise AssertionError(
                "test virtual environment creation failed\n"
                f"stdout:\n{create_venv.stdout}\n"
                f"stderr:\n{create_venv.stderr}"
            )
        cls.venv_bin = cls.venv / "bin"
        cls.venv_python = cls.venv_bin / "python"
        cls.installed_command = cls.venv_bin / "worktree-marshal"
        install = subprocess.run(
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
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if install.returncode:
            raise AssertionError(
                "wheel installation failed\n"
                f"stdout:\n{install.stdout}\n"
                f"stderr:\n{install.stderr}"
            )
        if not cls.installed_command.is_file():
            raise AssertionError("wheel did not install the worktree-marshal command")

        cls.outside = temporary_root / "outside-source-tree"
        cls.home = cls.outside / "home"
        cls.home.mkdir(parents=True)
        cls.state_home = cls.outside / "state"
        cls.installed_environment = os.environ.copy()
        cls.installed_environment.pop("PYTHONHOME", None)
        cls.installed_environment.pop("PYTHONPATH", None)
        cls.installed_environment.update(
            {
                "HOME": str(cls.home),
                "PATH": str(cls.venv_bin),
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1",
                "XDG_STATE_HOME": str(cls.state_home),
            }
        )

    def run_installed(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.installed_command), *arguments],
            cwd=self.outside,
            env=self.installed_environment,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def test_wheel_contains_importable_code_resource_and_license(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            names = set(archive.namelist())

        self.assertIn("worktree_marshal/__init__.py", names)
        self.assertIn("worktree_marshal/cli.py", names)
        self.assertIn("worktree_marshal/engine.py", names)
        self.assertIn("worktree_marshal/profiles.py", names)
        self.assertIn("worktree_marshal/triptych_compat.py", names)
        self.assertIn("worktree_marshal/resources/__init__.py", names)
        self.assertIn(
            "worktree_marshal/resources/worktree-marshal.mk",
            names,
        )
        self.assertTrue(
            any(name.endswith(".dist-info/licenses/LICENSE") for name in names),
            names,
        )

    def test_wheel_publishes_only_the_generic_console_script(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            entry_point_names = [
                name
                for name in archive.namelist()
                if name.endswith(".dist-info/entry_points.txt")
            ]
            self.assertEqual(len(entry_point_names), 1, entry_point_names)
            entry_points = archive.read(entry_point_names[0]).decode("utf-8")

        self.assertEqual(
            entry_points.strip().splitlines(),
            [
                "[console_scripts]",
                "worktree-marshal = worktree_marshal.cli:main",
            ],
        )
        self.assertNotIn("triptych-codex", entry_points)

    def test_wheel_metadata_records_no_runtime_dependency(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            metadata_names = [
                name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
            ]
            self.assertEqual(len(metadata_names), 1, metadata_names)
            metadata = archive.read(metadata_names[0]).decode("utf-8")

        self.assertIn("Name: worktree-marshal\n", metadata)
        self.assertIn("Version: 0.0.0\n", metadata)
        self.assertIn("Requires-Python: >=3.10\n", metadata)
        self.assertNotIn("Requires-Dist:", metadata)

    def test_source_distribution_contains_build_review_and_test_inputs(self) -> None:
        with tarfile.open(self.source_distribution, mode="r:gz") as archive:
            names = set(archive.getnames())

        roots = {name.split("/", 1)[0] for name in names if name}
        self.assertEqual(len(roots), 1, roots)
        root = roots.pop()
        expected = {
            "LICENSE",
            "MANIFEST.in",
            "README.md",
            "pyproject.toml",
            "docs/compatibility-contract.md",
            "docs/design.md",
            "docs/generic-v1.md",
            "src/worktree_marshal/__init__.py",
            "src/worktree_marshal/cli.py",
            "src/worktree_marshal/engine.py",
            "src/worktree_marshal/profiles.py",
            "src/worktree_marshal/triptych_compat.py",
            "src/worktree_marshal/resources/__init__.py",
            "src/worktree_marshal/resources/worktree-marshal.mk",
            "tests/test_distribution.py",
            "tests/test_cli.py",
            "tests/test_make_fragment.py",
            "tests/test_package.py",
            "tests/test_profile_isolation.py",
        }
        missing = {
            relative for relative in expected if f"{root}/{relative}" not in names
        }
        self.assertEqual(missing, set())

    def test_wheel_rebuilt_from_sdist_has_the_command_and_cli_module(self) -> None:
        with zipfile.ZipFile(self.sdist_wheel) as archive:
            names = set(archive.namelist())
            entry_point_names = [
                name for name in names if name.endswith(".dist-info/entry_points.txt")
            ]
            self.assertEqual(len(entry_point_names), 1, entry_point_names)
            entry_points = archive.read(entry_point_names[0]).decode("utf-8")

        self.assertIn("worktree_marshal/cli.py", names)
        self.assertIn(
            "worktree-marshal = worktree_marshal.cli:main",
            entry_points,
        )

    def test_installed_command_metadata_is_pure_outside_source_tree(self) -> None:
        version = self.run_installed("--version")
        help_result = self.run_installed("--help")

        self.assertEqual(version.returncode, 0, version.stderr)
        self.assertEqual(version.stdout, "worktree-marshal 0.0.0\n")
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("usage: worktree-marshal", help_result.stdout)
        self.assertIn("--profile", help_result.stdout)
        self.assertIn("generic-v1", help_result.stdout)
        self.assertIn("triptych", help_result.stdout)
        self.assertFalse(
            self.state_home.exists(),
            "metadata commands must not discover Git or create launcher state",
        )

    def test_installed_stateful_command_requires_profile_before_git(self) -> None:
        missing = self.run_installed("status")
        unknown = self.run_installed("--profile", "unknown", "status")

        self.assertEqual(missing.returncode, 2, missing)
        self.assertIn("--profile", missing.stderr)
        self.assertEqual(unknown.returncode, 2, unknown)
        self.assertIn("unknown", unknown.stderr)
        self.assertFalse(
            self.state_home.exists(),
            "invalid profile selection must fail before launcher state discovery",
        )


if __name__ == "__main__":
    unittest.main()
