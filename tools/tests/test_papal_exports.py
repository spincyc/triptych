"""Catalog exports keep edition identity and never distribute cached text."""
from __future__ import annotations

import copy
import csv
import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from _papal_exports import citation_key, export_catalog, tex_escape


def fixture():
    return {"documents": [
        {"id": "papal.pius-ix.quanta-cura-1864", "pope_id": "pius-ix", "pope": "Pius IX",
         "title": "Quanta cura", "date": "1864-12-08", "document_type": "encyclical",
         "languages": {"en": "https://example.org/en/quanta.html", "la": "https://example.org/la/quanta.html"},
         "text": "PRIVATE CACHED BODY"},
        {"id": "papal.benedictus-xiv.quanta-cura-1741", "pope_id": "benedictus-xiv", "pope": "Benedict XIV",
         "title": "Quanta cura", "date": "1741-06-30", "document_type": "encyclical",
         "languages": {"it": "https://example.org/it/quanta.html"}},
    ], "cache_path": "/private/cache"}


class PapalExportTests(unittest.TestCase):
    def test_citation_keys_separate_repeated_titles_and_languages(self):
        entries = json.loads(export_catalog(fixture(), "json"))["editions"]
        self.assertEqual(3, len({row["citation_key"] for row in entries}))
        changed = copy.deepcopy(fixture())
        changed["documents"][0]["title"] = "Corrected title"
        changed["documents"][0]["date"] = "1864-12-09"
        self.assertEqual(citation_key(fixture()["documents"][0]["id"], "en"),
                         json.loads(export_catalog(changed, "json"))["editions"][1]["citation_key"])

    def test_identity_hash_separates_lossy_slug_collisions(self):
        self.assertNotEqual(citation_key("papal.a.b", "la"), citation_key("papal.a-b", "la"))

    def test_identical_display_fields_do_not_merge_distinct_documents(self):
        catalog = fixture()
        second = copy.deepcopy(catalog["documents"][0])
        second["id"] += "-distinct-document"
        catalog["documents"] = [catalog["documents"][0], second]
        rows = json.loads(export_catalog(catalog, "json"))["editions"]
        self.assertEqual(4, len(rows))
        self.assertEqual(4, len({row["citation_key"] for row in rows}))

    def test_exports_are_metadata_only(self):
        for format in ("json", "csv", "biblatex", "beamer"):
            output = export_catalog(fixture(), format)
            self.assertNotIn("PRIVATE CACHED BODY", output)
            self.assertNotIn("/private/cache", output)

    def test_related_regulation_uses_actual_issuer_without_changing_pope_context(self):
        catalog = fixture()
        catalog["documents"][0].update(source_responsible="Cardinal Merry del Val",
                                      source_work_type="curial-regulation", record_role="constituent")
        rows = list(csv.DictReader(io.StringIO(export_catalog(catalog, "csv"))))
        row = next(row for row in rows if row["language"] == "en")
        self.assertEqual("Pius IX", row["pope"])
        self.assertEqual("Cardinal Merry del Val", row["responsible"])
        self.assertEqual("curial-regulation", row["document_type"])
        self.assertEqual("encyclical", row["source_document_type"])
        self.assertIn("author = {{Cardinal Merry del Val}}", export_catalog(catalog, "biblatex"))

    def test_reviewed_roles_dates_and_overlapping_forms_survive_exports(self):
        catalog = fixture()
        item = catalog["documents"][0]
        item.update(document_types=["encyclical", "apostolic-letter"],
                    record_role="composite", constituents=[{"title": "Second act"}],
                    issues=["Index date conflicts with the signature"],
                    resolved_date="1864-12-09", date_resolution={"basis": "Printed signature"})
        exported = json.loads(export_catalog(catalog, "json"))["documents"][-1]
        for field in ("document_types", "record_role", "constituents", "issues",
                      "resolved_date", "date_resolution"):
            self.assertEqual(item[field], exported[field])
        csv_rows = list(csv.DictReader(io.StringIO(export_catalog(catalog, "csv"))))
        row = next(row for row in csv_rows if row["id"] == item["id"])
        self.assertEqual("encyclical; apostolic-letter", row["document_types"])
        self.assertEqual("composite", row["record_role"])
        self.assertEqual("1864-12-08", row["date"])
        self.assertEqual("1864-12-09", row["resolved_date"])

    def test_json_keeps_unfiltered_coverage_and_scope_without_cache_paths(self):
        catalog = fixture()
        catalog["scope"] = {"categories": ["encyclicals", "bulls"]}
        catalog["coverage"] = [
            {"url": "https://example.org/index.html", "rows": 4, "status": "ok",
             "cache_path": "/private/cache"},
            {"url": "https://example.org/missing.html", "rows": 0, "status": "not-found"},
        ]
        catalog["documents"] = catalog["documents"][:1]
        exported = json.loads(export_catalog(catalog, "json"))
        self.assertEqual(catalog["scope"], exported["scope"])
        self.assertEqual(2, len(exported["coverage"]))
        self.assertNotIn("cache_path", exported["coverage"][0])

    def test_csv_roundtrip_preserves_quoted_title_and_language(self):
        catalog = fixture()
        catalog["documents"][0]["title"] = 'A title, "with quotes"'
        rows = list(csv.DictReader(io.StringIO(export_catalog(catalog, "csv"))))
        self.assertEqual(3, len(rows))
        self.assertEqual('A title, "with quotes"', rows[1]["title"])
        self.assertEqual("en", rows[1]["language"])

    def test_duplicate_ids_are_refused(self):
        catalog = fixture()
        catalog["documents"].append(catalog["documents"][0])
        with self.assertRaisesRegex(ValueError, "unique"):
            export_catalog(catalog, "biblatex")

    def test_tex_metacharacters_are_escaped(self):
        catalog = fixture()
        catalog["documents"][0]["title"] = r"A {title} & 50% \input{other}"
        for format in ("biblatex", "beamer"):
            output = export_catalog(catalog, format)
            self.assertIn(tex_escape(catalog["documents"][0]["title"]), output)
            self.assertNotIn(r"\input{other}", output)

    def test_source_url_cannot_break_out_of_tex_argument(self):
        for url in (r"https://example.org/}\input{other}", "javascript:alert(1)",
                    "https://user:secret@example.org/source"):
            catalog = fixture()
            catalog["documents"][0]["languages"]["en"] = url
            with self.assertRaisesRegex(ValueError, "source URL"):
                export_catalog(catalog, "beamer")

    def test_beamer_fallback_names_the_actual_language(self):
        output = export_catalog(fixture(), "beamer", language="en")
        self.assertIn("Read the Italian source", output)
        self.assertIn("Read the English source", output)
        self.assertEqual(2, output.count(r"\begin{frame}"))

    def test_compound_source_card_names_reviewed_constituents(self):
        catalog = fixture()
        catalog["documents"][0].update(title="Misleading original index label", record_role="composite",
                                      constituents=[{"subject": "First act"}, {"title": "Second act"}])
        output = export_catalog(catalog, "beamer")
        self.assertIn(r"\frametitle{\small Compound source delivery}", output)
        self.assertIn("First act; Second act", output)
        self.assertNotIn("Misleading original index label", output)
        self.assertIn("Compound source delivery containing multiple documents", export_catalog(catalog, "biblatex"))

    def test_reviewed_date_is_validated_and_controls_chronological_order(self):
        catalog = fixture()
        catalog["documents"][0]["resolved_date"] = "1700-01-01"
        exported = json.loads(export_catalog(catalog, "json"))
        self.assertEqual(catalog["documents"][0]["id"], exported["documents"][0]["id"])
        catalog["documents"][0]["resolved_date"] = "1700-13-01"
        with self.assertRaises(ValueError):
            export_catalog(catalog, "csv")

    def test_unlinked_work_remains_visible_without_inventing_an_edition(self):
        catalog = fixture()
        catalog["documents"][0]["languages"] = {}
        exported = json.loads(export_catalog(catalog, "json"))
        self.assertEqual(2, len(exported["documents"]))
        self.assertEqual(1, len(exported["editions"]))
        rows = list(csv.DictReader(io.StringIO(export_catalog(catalog, "csv"))))
        self.assertEqual("work", rows[1]["record_kind"])
        self.assertEqual("", rows[1]["language"])
        self.assertEqual("", rows[1]["source_url"])
        self.assertIn("@misc{", export_catalog(catalog, "biblatex"))
        self.assertIn("Source link unavailable", export_catalog(catalog, "beamer"))

    def test_invalid_dates_are_not_exported_as_certain(self):
        catalog = fixture()
        catalog["documents"][0]["date"] = "1864-13-08"
        with self.assertRaises(ValueError):
            export_catalog(catalog, "csv")


if __name__ == "__main__":
    unittest.main()
