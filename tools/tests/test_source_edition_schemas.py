"""Neutral source schemas retain existing vocabularies and semantic owners."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from document_schema_checks import source_editions as schemas


class SourceSchemaTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/source-html/schema-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.schema = json.loads((ROOT / "src/common/document-schemas/bible-book-index.schema.json").read_text())

    def book_index(self, rows):
        path = self.root / "book-index.tsv"
        fields = list(self.schema["required"])
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
        return path

    def row(self, **changes):
        return {"ordinal": "1", "token": "Gen", "file": "01-genesis.tsv", "testament": "old",
                "douay_title": "Genesis", "modern_name": "Genesis", "missal_latin_abbreviation": "Gen.",
                "alternate_names": "Gen", **changes}

    def test_existing_optional_columns_and_blank_douay_title_are_allowed(self):
        # KJV-only books truthfully have no Douay title; no title is fabricated.
        path = self.book_index([self.row(douay_title="")])
        self.assertEqual(len(schemas.check_book_index(path, self.schema)), 1)

    def test_duplicate_book_identity_and_unsafe_file_fail(self):
        for rows in ([self.row(), self.row(ordinal="2", file="02-genesis.tsv")],
                     [self.row(file="../genesis.tsv")]):
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                schemas.check_book_index(self.book_index(rows), self.schema)

    def test_printed_verse_gaps_are_preserved_but_duplicates_fail(self):
        book = SimpleNamespace(token="Acts", verses=[(8, 36, "First"), (8, 38, "After omitted verse")])
        schemas.check_verse_addresses(book)
        book.verses.append((8, 38, "Duplicated address"))
        with self.assertRaisesRegex(ValueError, "duplicate or unordered"):
            schemas.check_verse_addresses(book)

    def test_plan_overlap_and_adjacent_ranges(self):
        checker = schemas._print_catalog._bible_typesetter().sibling("reading-plan")
        def reading(order, start, end):
            return {"order": order, "tier": "landmarks", "book": "Genesis", "title": "Fixture",
                    "ranges": [{"begin": {"chapter": 1, "verse": start},
                                "end": {"chapter": 1, "verse": end}}]}
        document = {"schema": checker.SCHEMA, "title": "Fixture", "canon": "catholic-73", "numbering": "vulgate",
                    "tiers": {"landmarks": {"readings": 2}}, "omissions": "Fixture", "precedents": [],
                    "periods": [{"key": "a", "readings": [reading(1, 1, 3), reading(2, 4, 5)]}]}
        bounds = {("Gen", 1): (1, 5)}
        self.assertEqual(checker.check_plan(Path("fixture.yaml"), document, {"Genesis": "Gen"}, bounds), [])
        document["periods"][0]["readings"][1] = reading(2, 3, 5)
        errors = checker.check_plan(Path("fixture.yaml"), document, {"Genesis": "Gen"}, bounds)
        self.assertTrue(any("overlaps reading 1 at Genesis 1:3" in error for error in errors))

    def test_overlap_inside_one_discontiguous_reading_is_not_silently_deduplicated(self):
        checker = schemas._print_catalog._bible_typesetter().sibling("reading-plan")
        span = {"begin": {"chapter": 1, "verse": 1}, "end": {"chapter": 1, "verse": 2}}
        document = {"schema": checker.SCHEMA, "title": "Fixture", "canon": "catholic-73", "numbering": "vulgate",
                    "tiers": {"landmarks": {}}, "omissions": "Fixture", "precedents": [],
                    "periods": [{"readings": [{"order": 1, "tier": "landmarks", "book": "Genesis",
                                              "ranges": [span, span]}]}]}
        errors = checker.check_plan(Path("fixture.yaml"), document, {"Genesis": "Gen"}, {("Gen", 1): (1, 3)})
        self.assertTrue(any("overlaps reading 1" in error for error in errors))

    def test_all_current_families_have_source_schema_coverage_without_pdf_or_external_gates(self):
        original_open, original_read = Path.open, Path.read_bytes
        def no_pdf_open(path, *args, **kwargs):
            self.assertNotEqual(path.suffix.lower(), ".pdf")
            return original_open(path, *args, **kwargs)
        def no_pdf_read(path, *args, **kwargs):
            self.assertNotEqual(path.suffix.lower(), ".pdf")
            return original_read(path, *args, **kwargs)
        with patch.object(Path, "open", no_pdf_open), patch.object(Path, "read_bytes", no_pdf_read), \
                patch("subprocess.run", side_effect=AssertionError("owning gates must not run implicitly")):
            report = schemas.check_source_editions(ROOT)
        self.assertTrue(report["ok"], report["errors"])
        families = {row["id"]: row for row in report["families"]}
        self.assertEqual(families["bible-edition"]["members"], 7)
        self.assertEqual(families["reading-plan"]["members"], 1)
        self.assertEqual(families["reading-plan-volume"]["members"], 6)
        self.assertEqual(families["papal-reader"]["members"], 350)
        self.assertGreater(families["papal-selection"]["records"][0]["selections"], 4831)
        self.assertEqual(len(families), 13)
        self.assertTrue(report["external_gates"])
        self.assertTrue(all(gate["status"] == "not-run" for gate in report["external_gates"]))


if __name__ == "__main__":
    unittest.main()
