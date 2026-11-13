"""Indexed reads retain the full producers' exact bytes and refusal semantics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _catena
from _corpus_index import CorpusIndex
import _reader_bibles
import _reader_commentary_products as reader


class CommentaryReaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Currency is independently exercised by test_corpus_index. This suite
        # checks selected canonical byte reads while other code may be edited.
        cls.index = CorpusIndex(ROOT, _bind=False)
        descriptor = json.loads((ROOT / "release/browser-products.json").read_bytes())
        cls.expected = {path: record for family in descriptor["products"]
                        if family["id"] in {"catena", "paragraphs", "readings"}
                        for path, record in family["files"].items()}

    def resolve(self, path):
        with patch.object(_catena, "load_sources", side_effect=AssertionError("whole source graph")), \
             patch.object(_catena, "_structure_files", side_effect=AssertionError("whole Catena")), \
             patch.object(_catena, "_paragraph_files", side_effect=AssertionError("all paragraphs")):
            return reader.resolve(path, ROOT, self.index)

    def assert_product(self, path):
        body = self.resolve(path)
        self.assertIsInstance(body, bytes, path)
        self.assertEqual(len(body), self.expected[path]["bytes"], path)
        self.assertEqual(hashlib.sha256(body).hexdigest(), self.expected[path]["sha256"], path)
        return json.loads(body)

    def test_metadata_contains_addresses_and_counts_without_bodies(self):
        catalog = json.loads(self.index.read(reader.CATALOG_PATH))
        self.assertNotIn("absences", catalog["catena"])
        self.assertNotIn('"text"', json.dumps(catalog))
        self.assertNotIn('"basis"', json.dumps(catalog))
        bibles = _reader_bibles.metadata(self.index)
        for books in bibles["editions"].values():
            for chapters in books.values():
                for bounds in chapters.values():
                    self.assertTrue(all(type(value) is int for value in bounds))

    def test_catena_catalog_and_selected_chapters_match_published_bytes(self):
        self.assert_product("structure/catena/index.json")
        for folder, chapter in (("01-gen", 1), ("47-matt", 9), ("48-mark", 10), ("21-ps", 50)):
            path = f"structure/catena/{folder}/{chapter:03}.json"
            with self.subTest(path=path):
                self.assert_product(path)

    def test_selected_text_does_not_load_other_passage_bodies(self):
        path = next(path for path in self.expected
                    if path.startswith("structure/catena/text/") and "origen" in path)
        identifier = Path(path).stem
        selected_path = self.index.record_path(identifier)
        reads = []
        original = self.index.read

        def selected(relative):
            reads.append(relative)
            if "/passages/" in relative and relative != selected_path:
                raise AssertionError(f"unselected passage read: {relative}")
            return original(relative)

        with patch.object(self.index, "read", side_effect=selected):
            payload = self.assert_product(path)
        self.assertIn(selected_path, reads)
        self.assertEqual(payload["id"], identifier)
        self.assertIn("acknowledgement", payload)

    def test_source_failure_is_not_an_empty_text(self):
        path = next(path for path in self.expected if path.startswith("structure/catena/text/"))
        selected_path = self.index.record_path(Path(path).stem)
        original = self.index.read

        def broken(relative):
            if relative == selected_path:
                raise ValueError("selected canonical source is corrupt")
            return original(relative)

        with patch.object(self.index, "read", side_effect=broken):
            with self.assertRaisesRegex(ValueError, "invalid source record"):
                self.resolve(path)

    def test_selected_text_retains_the_owning_rights_gate(self):
        path = next(path for path in self.expected if path.startswith("structure/catena/text/"))
        original = self.index.record

        def restricted(identifier):
            row = original(identifier)
            if self.index.record_kind(identifier) == "artifact":
                return {**row, "rights_status": "restricted", "license": ""}
            return row

        with patch.object(self.index, "record", side_effect=restricted):
            with self.assertRaisesRegex(_catena.CatenaError, "may not be published"):
                self.resolve(path)

    def test_selected_scripture_retains_numbering_and_refusals(self):
        psalms = self.assert_product("structure/catena/scripture/21-ps.json")
        self.assertEqual(psalms["chapters"]["50"]["loci"]["hebrew-unnumbered-titles"][0]["chapter"], 51)
        self.assert_product("structure/catena/scripture/32-dan.json")

    def test_paragraphs_retain_printed_and_projected_distinction(self):
        self.assert_product("structure/paragraphs/index.json")
        kjv = self.assert_product("structure/paragraphs/king-james-version/01-gen/001.json")
        self.assertIn("printed", kjv["breaks"].values())
        self.assertIn("projected", kjv["breaks"].values())
        self.assert_product("structure/paragraphs/clementine-vulgate/01-gen/001.json")

    def test_reading_plan_matches_the_existing_producer(self):
        self.assert_product("structure/readings/narrative-spine.json")

    def test_unowned_and_absent_products_are_absent(self):
        for path in ("structure/catena/text/not-held.json", "structure/catena/01-gen/999.json",
                     "structure/catena/scripture/not-a-book.json",
                     "structure/readings/not-a-plan.json",
                     "structure/paragraphs/not-an-edition/01-gen/001.json",
                     "structure/paragraphs/clementine-vulgate/01-gen/999.json"):
            with self.subTest(path=path):
                self.assertIsNone(self.resolve(path))

    def test_lazy_bible_uses_the_owners_open_bounds(self):
        with self.index.verified_reads(), _reader_bibles.bible_context(ROOT, self.index) as selected:
            bible = selected("clementine-vulgate")
            self.assertEqual(bible.open_bounds[("Ps", 147)], (12, 20))
            text, problem = bible.passage("Ps", [{"begin": {"chapter": 147}, "end": {"chapter": 147}}])
            self.assertFalse(problem)
            self.assertIn("Lauda", text)
            self.assertEqual(set(bible.verses.loaded), {("Ps", 147)})


if __name__ == "__main__":
    unittest.main()
