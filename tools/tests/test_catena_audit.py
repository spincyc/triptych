"""Completeness means every manifest; verse coverage means only declared edges."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _catena
import _catena_audit as audit
from _commentary import chapter_loci, key_extents, overlapping_keys


class ReferenceExtentTests(unittest.TestCase):
    def test_intermediate_chapters_are_discovered(self):
        self.assertEqual(chapter_loci("Genesis 1:20-4:3"),
                         ["Genesis 1", "Genesis 2", "Genesis 3", "Genesis 4"])

    def test_same_chapter_range_does_not_duplicate_lead(self):
        self.assertEqual(chapter_loci("John 3:1-3:16"), ["John 3"])

    def test_reversed_range_does_not_fabricate_a_first_verse(self):
        self.assertEqual(key_extents("John 3:16-2"), [])
        self.assertEqual(overlapping_keys(["John 3:16-2", "John 3:16"]), [])


class HeldCorpusAuditTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/retrieval"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def manifest(self, name, kind, body=""):
        path = self.root / "src/sources/works/test/work" / f"{name}.toml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'id = "{name}"\nrecord_type = "{kind}"\n{body}')
        return path

    def test_inventory_keeps_malformed_and_duplicate_manifests(self):
        self.manifest("w", "work")
        duplicate = self.manifest("dup", "work")
        duplicate.write_text('id = "w"\nrecord_type = "work"\n')
        broken = self.manifest("broken", "passage")
        broken.write_text('id = "unfinished')
        rows, records, errors = audit.inventory(self.root)
        self.assertEqual(len(rows), 3)
        self.assertEqual(len(records), 1)
        self.assertEqual(len(errors), 2)
        self.assertEqual({row["path"] for row in rows}, {
            path.relative_to(self.root).as_posix()
            for path in self.root.rglob("*.toml")})
        self.assertTrue(all(len(row["sha256"]) == 64 for row in rows))

    def test_stale_or_unknown_review_fails_without_promoting_it(self):
        path = self.root / audit.REVIEW_PATH
        path.parent.mkdir(parents=True)
        path.write_text(f'schema: {audit.REVIEW_SCHEMA}\nreviews:\n'
                        '  - passage_id: p\n    passage_sha256: stale\n'
                        '    disposition: no-scripture-commentary\n    basis: Checked text.\n')
        errors = []
        audit._reviews(self.root, {"p": {"record_type": "passage", "sha256": "fresh"}}, errors)
        self.assertEqual(len(errors), 1)
        self.assertIn("stale passage review", errors[0])

    def test_malformed_review_fields_are_diagnostics_not_exceptions(self):
        path = self.root / audit.REVIEW_PATH
        path.parent.mkdir(parents=True)
        for body in ("reviews: 1", "reviews: [", "reviews:\n  - passage_id: p\n    disposition: []\n    basis: [invented]\n    passage_sha256: abc"):
            with self.subTest(body=body):
                path.write_text(f"schema: {audit.REVIEW_SCHEMA}\n{body}\n")
                errors = []
                audit._reviews(self.root, {}, errors)
                self.assertTrue(errors)

    def test_all_passages_accounted_without_inferred_anchors(self):
        self.manifest("w", "work", 'title = "Work"\nresponsible = "Author"\n')
        self.manifest("e", "edition", 'work_id = "w"\nlanguage = "en"\n')
        self.manifest("a", "artifact", 'edition_id = "e"\nrights_status = "public-domain"\nstorage = "tracked"\n')
        for identifier in ("mapped", "unmapped", "parallel"):
            self.manifest(identifier, "passage", 'edition_id = "e"\nartifact_id = "a"\ntext = "Source words"\nstates = ["verified"]\n')
        extent = {"token": "Gen", "first_chapter": 1, "first_verse": 8,
                  "last_chapter": 3, "last_verse": 2}
        edges = {"fragments": [{"passage_id": "mapped", "work_id": "w", "extent": extent}],
                 "parallels": [{"hung": "mapped", "passage_ids": ["mapped", "parallel"]}]}
        for chapter in range(1, 4):
            path = self.root / _catena.BIBLES_RELATIVE / _catena.CANONICAL_BIBLE / "chapters/Gen" / f"{chapter}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps({"verses": {str(v): "words" for v in range(1, 11)}}))
        decision = {"status": "eligible", "eligible": True}
        scope = SimpleNamespace(errors=[], work_decision=lambda _: decision,
                                author_decision=lambda _: decision, lead_decision=lambda _: decision)
        with patch.object(audit._catena_scope, "Scope", return_value=scope), \
             patch.object(_catena, "load_edges", return_value=edges), \
             patch.object(_catena, "validate", return_value=[]), \
             patch.object(_catena, "controlling_artifact", side_effect=lambda s, p: s.artifacts["a"]), \
             patch.object(_catena, "_commentary_index", return_value={}), \
             patch.object(_catena, "canon", return_value=[{"token": "Gen", "name": "Genesis", "last_chapter": 3}]):
            first = audit.report(self.root)
            self.assertEqual(first, audit.report(self.root))
            with patch.object(audit, "_reviews", return_value={
                    "unmapped": {"disposition": "direct-commentary"},
                    "parallel": {"disposition": "direct-commentary"}}):
                lost = audit.report(self.root)
                self.assertTrue(any("reviewed direct commentary has no canonical fragment edge" in error for error in lost["errors"]))
                self.assertFalse(any(error.startswith("parallel:") for error in lost["errors"]))
            edges["fragments"].append({"broken": "edge"})
            broken = audit.report(self.root)
            self.assertEqual(broken["totals"]["passages"], 3)
            self.assertTrue(any("malformed fragments list" in error for error in broken["errors"]))
        self.assertEqual(first["status"], "invalid")
        self.assertTrue(any("neither a fragment edge nor a reviewed" in error for error in first["errors"]))
        self.assertEqual(first["totals"]["passages"], 3)
        self.assertEqual(first["totals"]["passages_by_index_state"],
                         {"indexed": 1, "parallel": 1, "unindexed": 1})
        self.assertEqual(first["totals"]["verses_with_fragments"], 15)
        chapters = first["books"][0]["chapters"]
        self.assertEqual([row["verses_with_fragments"] for row in chapters], [3, 10, 2])
        unmapped = next(row for row in first["passages"] if row["passage_id"] == "unmapped")
        self.assertEqual(unmapped["scripture_applicability"], "unestablished")
        self.assertNotIn("extent", unmapped)
        self.assertIn("no-canonical-scripture-edge", unmapped["gates"])


if __name__ == "__main__":
    unittest.main()
