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

    def test_wheel_contains_importable_code_resource_and_license(self) -> None:
        with zipfile.ZipFile(self.wheel) as archive:
            names = set(archive.namelist())

        self.assertIn("worktree_marshal/__init__.py", names)
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
            "src/worktree_marshal/__init__.py",
            "src/worktree_marshal/triptych_compat.py",
            "src/worktree_marshal/resources/__init__.py",
            "src/worktree_marshal/resources/worktree-marshal.mk",
            "tests/test_distribution.py",
            "tests/test_make_fragment.py",
            "tests/test_package.py",
        }
        missing = {
            relative for relative in expected if f"{root}/{relative}" not in names
        }
        self.assertEqual(missing, set())


if __name__ == "__main__":
    unittest.main()
