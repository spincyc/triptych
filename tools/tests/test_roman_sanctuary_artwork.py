#!/usr/bin/env python3

from __future__ import annotations

import importlib.machinery
import importlib.util
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "tools/lib/check-roman-sanctuary-artwork"


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

    def test_publication_mode_keeps_legacy_opaque_grayscale(self) -> None:
        self.assertTrue(
            ARTWORK_CHECKER.publication_mode_allowed("grayscale", None)
        )
        self.assertTrue(
            ARTWORK_CHECKER.publication_mode_allowed("grayscale", "page-ground")
        )

    def test_publication_mode_allows_alpha_only_for_transparent_boundary(self) -> None:
        self.assertTrue(
            ARTWORK_CHECKER.publication_mode_allowed(
                "grayscale-alpha", "transparent"
            )
        )
        self.assertFalse(
            ARTWORK_CHECKER.publication_mode_allowed("grayscale", "transparent")
        )
        for treatment in (None, "page-ground", "intentional-frame", "full-bleed"):
            with self.subTest(treatment=treatment):
                self.assertFalse(
                    ARTWORK_CHECKER.publication_mode_allowed(
                        "grayscale-alpha", treatment
                    )
                )

    def test_publication_mode_rejects_other_png_modes(self) -> None:
        for mode in ("rgb", "rgba", "indexed"):
            with self.subTest(mode=mode):
                self.assertFalse(
                    ARTWORK_CHECKER.publication_mode_allowed(
                        mode, "transparent"
                    )
                )

    def test_canonical_asset_path_normalizes_repository_prefixed_links(self) -> None:
        relative = "shared/artwork/pencil/example.png"
        self.assertEqual(
            ARTWORK_CHECKER.canonical_asset_path(
                "src/gpt/liturgy/roman-rite/1962/reference/"
                "roman-sanctuary-dictionary/" + relative
            ),
            relative,
        )

    def test_rijks_composition_is_bounded_to_the_comprehensive_edition(self) -> None:
        root = (
            REPO
            / "src/gpt/liturgy/roman-rite/1962/reference/"
            "roman-sanctuary-dictionary"
        )
        with (root / "research/artwork-manifest.toml").open("rb") as handle:
            manifest = tomllib.load(handle)
        artwork = next(
            item for item in manifest["artworks"]
            if item["id"] == "art-sanctuary-ecce-homo-rijks-graphite"
        )
        self.assertEqual(artwork["consumer_edition_ids"], ["ed-comprehensive"])
        self.assertEqual(
            artwork["consumer_plate_ids"],
            ["plt-sanctuary-ecce-homo-rijks-witness"],
        )
        self.assertIn("atypical", artwork["purpose"])
        self.assertIn(
            "src-rijks-ecce-homo-chapel-photo",
            artwork["reference_ids"],
        )

        asset = next(
            item for item in manifest["asset_files"]
            if item["id"] == "file-rpd-sanctuary-ecce-homo-rijks-graphite"
        )
        self.assertEqual(asset["boundary_treatment"], "page-ground")
        self.assertEqual(asset["state"], "canonical-alpha-eligible")

    def test_asset_local_staging_requires_exact_adjacent_hash(self) -> None:
        temporary, root = self.owner()
        self.addCleanup(temporary.cleanup)
        asset = root / "shared/artwork/candidate.png"
        asset.parent.mkdir(parents=True)
        asset.write_bytes(b"candidate")
        digest = __import__("hashlib").sha256(b"candidate").hexdigest()
        asset.with_suffix(".toml").write_text(
            'artwork_id = "art-candidate"\n'
            'review_state = "rejected"\n'
            f'sha256 = "{digest}"\n',
            encoding="utf-8",
        )
        problems = ARTWORK_CHECKER.Problems()
        self.assertTrue(ARTWORK_CHECKER.asset_local_staging_path(asset, problems))
        self.assertEqual(problems.items, [])

    def test_accepted_pontifical_assets_are_canonical_and_rejected_buskin_is_not(self) -> None:
        root = (
            REPO
            / "src/gpt/liturgy/roman-rite/1962/reference/"
            "roman-sanctuary-dictionary"
        )
        with (root / "research/artwork-manifest.toml").open("rb") as handle:
            manifest = tomllib.load(handle)
        files = {item["id"]: item for item in manifest["asset_files"]}
        required = {
            "file-pont-crosier-canonical",
            "file-pont-gremial-isolated-canonical",
            "file-pont-gremial-handling-canonical",
            "file-pont-mitre-forms-canonical",
            "file-pont-mitre-veil-v2-canonical",
            "file-pont-pectoral-cross-canonical",
            "file-pont-bugia-canonical",
            "file-pont-throne-canonical",
            "file-pont-faldstool-canonical",
            "file-pont-vimpa-pair-canonical",
            "file-pont-vimpa-mitre-canonical",
            "file-pont-vimpa-crosier-canonical",
            "file-pont-gloves-canonical",
            "file-pont-ring-canonical",
            "file-pont-ring-glove-canonical",
            "file-pont-sandal-canonical",
            "file-pont-footwear-layered-canonical",
            "file-pont-layering-cutaway-canonical",
        }
        self.assertTrue(required <= files.keys())
        for file_id in required:
            with self.subTest(file_id=file_id):
                self.assertEqual(files[file_id]["state"], "canonical-alpha-eligible")
                self.assertEqual(files[file_id]["boundary_treatment"], "transparent")
        canonical_paths = {item["path"] for item in files.values()}
        self.assertNotIn(
            "shared/artwork/pencil/pontifical-vesture/"
            "RPD-FIG-pontifical-vesture-0001-buskin-alpha.png",
            canonical_paths,
        )


if __name__ == "__main__":
    unittest.main()
