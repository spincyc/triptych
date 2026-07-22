#!/usr/bin/env python3
"""Focused tests for the extraction-stage package metadata and import."""

from __future__ import annotations

import importlib
import re
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PACKAGE_ROOT / "src"
PYPROJECT = PACKAGE_ROOT / "pyproject.toml"


def project_section() -> str:
    text = PYPROJECT.read_text(encoding="utf-8")
    _, section = text.split("[project]\n", 1)
    return section.split("\n[", 1)[0]


def project_string(name: str) -> str:
    match = re.search(
        rf'(?m)^{re.escape(name)}\s*=\s*"([^"]+)"\s*$',
        project_section(),
    )
    if match is None:
        raise AssertionError(f"missing string project metadata: {name}")
    return match.group(1)


class PackageScaffoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sys.path.insert(0, str(SOURCE_ROOT))

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            sys.path.remove(str(SOURCE_ROOT))
        except ValueError:
            pass

    def test_distribution_metadata_matches_imported_package(self) -> None:
        package = importlib.import_module("worktree_marshal")

        self.assertEqual(project_string("name"), "worktree-marshal")
        self.assertEqual(project_string("version"), package.__version__)
        self.assertEqual(package.__version__, "0.0.0")
        self.assertEqual(project_string("license"), "MIT")

    def test_supported_python_and_runtime_dependency_contract(self) -> None:
        section = project_section()

        self.assertEqual(project_string("requires-python"), ">=3.10")
        self.assertRegex(section, r"(?m)^dependencies\s*=\s*\[\]\s*$")

    def test_make_fragment_is_an_importable_package_resource(self) -> None:
        resources = importlib.import_module("worktree_marshal.resources")
        fragment = resources.make_fragment()

        self.assertTrue(fragment.is_file())
        self.assertEqual(fragment.name, "worktree-marshal.mk")
        self.assertIn(
            "Worktree Marshal Make-fragment API 1",
            resources.read_make_fragment(),
        )

    def test_scaffold_has_no_published_command_entry_point(self) -> None:
        metadata = PYPROJECT.read_text(encoding="utf-8")

        self.assertNotIn("[project.scripts]", metadata)
        self.assertNotIn("worktree-marshal =", project_section())


if __name__ == "__main__":
    unittest.main()
