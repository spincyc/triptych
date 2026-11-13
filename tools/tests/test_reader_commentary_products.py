"""Indexed reads retain the full producers' exact bytes and refusal semantics."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _catena
from _corpus_index import CorpusIndex
import _reader_bibles
import _reader_commentary_products as reader

_DENSITY_ADAPTER = r"""
const fs = require('fs'), path = require('path');
const root = process.argv[1], input = JSON.parse(fs.readFileSync(0, 'utf8'));
globalThis.CatenaModel = require(path.join(root, 'src/web/browser/catena/catena-model.js'));
const loads = [];
class NotFound extends Error {}
globalThis.Triptych = {
  NotFound, languageName: (code) => code,
  loadBibles: async () => ({ok: true, bibles: input.editions}),
  loadJSON: async (where) => {
    loads.push(where);
    if (where === 'structure/catena/index.json') return input.index;
    if (where === 'structure/paragraphs/index.json') return {};
    if (Object.hasOwn(input.chapters, where)) return input.chapters[where];
    throw new NotFound(where);
  },
};
const adapter = require(path.join(root, 'scripts/lectern/adapters/catena.js'))({
  script() {}, read(where) {
    const token = where.slice('structure/catena/density/'.length, -5);
    return input.density ? input.density[token] : undefined;
  },
});
(async () => {
  const rows = {};
  for (const book of input.index.canon) rows[book.token] = await adapter.density(book.token);
  process.stdout.write(JSON.stringify({rows, loads}));
})().catch((error) => { console.error(error.message); process.exitCode = 1; });
"""


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
            with self.assertRaisesRegex(ValueError, "invalid source record|canonical source is corrupt"):
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

    def density_fixture(self):
        catalog = json.loads(self.index.read(reader.CATALOG_PATH))["catena"]
        catalog["canon"] = [book for book in catalog["canon"] if book["token"] in {"Gen", "Ex", "Ps"}]
        paths = ("structure/catena/01-gen/001.json", "structure/catena/01-gen/002.json",
                 "structure/catena/02-ex/003.json", "structure/catena/21-ps/002.json")
        chapters = {path: json.loads(self.resolve(path)) for path in paths}
        from _reader_products import MANIFESTS
        editions = json.loads(self.index.read(MANIFESTS))["bibles.json"]["bibles"]
        return {"index": catalog, "chapters": chapters, "editions": editions}

    def adapter_density(self, fixture):
        result = subprocess.run(["node", "-e", _DENSITY_ADAPTER, str(ROOT)],
                                input=json.dumps(fixture), text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_density_keeps_model_counts_without_loading_chapters(self):
        fixture = self.density_fixture()
        expected = self.adapter_density(fixture)
        fixture["density"] = reader.density_metadata(ROOT, fixture["index"], fixture["chapters"], fixture["editions"])
        actual = self.adapter_density(fixture)
        self.assertEqual(actual["rows"], expected["rows"])
        self.assertEqual(actual["loads"], ["structure/catena/index.json", "structure/paragraphs/index.json"])
        self.assertGreater(expected["rows"]["Gen"][0]["fragments"], 0)
        self.assertGreater(expected["rows"]["Ex"][2]["leads"], 0)
        self.assertEqual(expected["rows"]["Ex"][2]["fragments"], 0)
        self.assertTrue(any(row["refused"] for row in expected["rows"]["Ps"]))
        self.assertTrue(any(row["unreadable"] for row in expected["rows"]["Gen"]))
        self.assertTrue(any(not row["held"] for row in expected["rows"]["Ex"]))

        catalog = json.loads(self.index.read(reader.CATALOG_PATH))
        catalog["density"] = fixture["density"]
        reads = []
        def only_metadata(relative):
            reads.append(relative)
            if relative != reader.CATALOG_PATH:
                raise AssertionError(f"density read a body: {relative}")
            return reader._json(catalog)

        with patch.object(self.index, "read", side_effect=only_metadata):
            payload = json.loads(self.resolve("structure/catena/density/Gen.json"))
        self.assertEqual(payload["rows"], expected["rows"]["Gen"])
        self.assertEqual(reads, [reader.CATALOG_PATH])

    def test_density_refuses_missing_metadata_and_different_editions(self):
        catalog = json.loads(self.index.read(reader.CATALOG_PATH))
        catalog.pop("density", None)
        with patch.object(reader, "_catalog", return_value=catalog):
            with self.assertRaisesRegex(ValueError, "density index is missing"):
                self.resolve("structure/catena/density/Gen.json")
        fixture = self.density_fixture()
        fixture["density"] = reader.density_metadata(ROOT, fixture["index"], fixture["chapters"], fixture["editions"])
        fixture["density"]["Gen"]["editions"] = []
        result = subprocess.run(["node", "-e", _DENSITY_ADAPTER, str(ROOT)],
                                input=json.dumps(fixture), text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not describe this book and its editions", result.stderr)


if __name__ == "__main__":
    unittest.main()
