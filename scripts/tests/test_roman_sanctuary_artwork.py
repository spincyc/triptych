#!/usr/bin/env python3

from __future__ import annotations

import importlib.machinery
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts/check-roman-sanctuary-artwork"


def load_checker():
    loader = importlib.machinery.SourceFileLoader("artwork_checker", str(CHECKER))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


ARTWORK_CHECKER = load_checker()


EMPTY_MANIFEST = """\
schema_version = 1
manifest_id = "roman-sanctuary-dictionary-artwork"
owner = "liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
asset_root = "shared/artwork"
status = "held-no-assets"
asset_files = []
artwork_links = []
artworks = []

[coverage]
object_record_glob = "shared/objects/**/*.toml"
exclude_paths = ["shared/schema/object.example.toml"]
publication_ready_workflow_state = "publication-ready"
required_artwork_workflow_state = "consumer-review-passed"
require_bidirectional_links = true
require_variant_coverage = true
"""


class ArtworkManifestTests(unittest.TestCase):
    def owner(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "research").mkdir()
        (root / "shared/objects").mkdir(parents=True)
        (root / "research/artwork-manifest.toml").write_text(
            EMPTY_MANIFEST, encoding="utf-8"
        )
        return temporary, root

    def run_checker(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(CHECKER), "--root", str(root)],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_empty_held_manifest_is_valid(self) -> None:
        temporary, root = self.owner()
        self.addCleanup(temporary.cleanup)
        result = self.run_checker(root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_publication_ready_object_requires_artwork(self) -> None:
        temporary, root = self.owner()
        self.addCleanup(temporary.cleanup)
        (root / "shared/objects/chalice.toml").write_text(
            """\
id = "obj-chalice"
workflow_state = "publication-ready"
artwork = []
variants = []
""",
            encoding="utf-8",
        )
        result = self.run_checker(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("publication-ready object has no artwork", result.stderr)

    def test_nonready_object_link_is_reported_as_held_notice(self) -> None:
        temporary, root = self.owner()
        self.addCleanup(temporary.cleanup)
        (root / "shared/objects/chalice.toml").write_text(
            """\
id = "obj-chalice"
workflow_state = "identified"
variants = []

[[artwork]]
id = "art-chalice-front"
""",
            encoding="utf-8",
        )
        result = self.run_checker(root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NOTICE:", result.stderr)
        self.assertIn("absent from canonical manifest", result.stderr)

    def boundary_problems(self, **fields: str) -> list[str]:
        problems = ARTWORK_CHECKER.Problems()
        ARTWORK_CHECKER.validate_boundary_treatment(
            fields, "art-test", problems
        )
        return problems.items

    def test_boundary_treatment_is_optional_for_existing_records(self) -> None:
        self.assertEqual(self.boundary_problems(), [])

    def test_boundary_treatment_accepts_unframed_forms_without_rationale(self) -> None:
        for treatment in ("transparent", "page-ground"):
            with self.subTest(treatment=treatment):
                self.assertEqual(
                    self.boundary_problems(boundary_treatment=treatment), []
                )

    def test_boundary_treatment_requires_rationale_for_deliberate_edges(self) -> None:
        for treatment in ("intentional-frame", "full-bleed"):
            with self.subTest(treatment=treatment):
                problems = self.boundary_problems(boundary_treatment=treatment)
                self.assertTrue(
                    any("must be nonempty" in problem for problem in problems)
                )
                self.assertEqual(
                    self.boundary_problems(
                        boundary_treatment=treatment,
                        boundary_treatment_rationale="The visible edge is intentional.",
                    ),
                    [],
                )

    def test_boundary_treatment_rejects_inconsistent_rationale(self) -> None:
        problems = self.boundary_problems(
            boundary_treatment="transparent",
            boundary_treatment_rationale="Unneeded explanation.",
        )
        self.assertTrue(any("is not allowed" in problem for problem in problems))
        orphan = self.boundary_problems(
            boundary_treatment_rationale="Missing treatment."
        )
        self.assertTrue(any("requires boundary_treatment" in problem for problem in orphan))

    def test_boundary_treatment_rejects_unknown_value(self) -> None:
        problems = self.boundary_problems(boundary_treatment="feathered")
        self.assertTrue(any("has invalid state" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
