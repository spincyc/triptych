#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "scripts/check-roman-sanctuary-artwork"


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


if __name__ == "__main__":
    unittest.main()
