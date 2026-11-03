"""Neutral source schemas retain existing vocabularies and semantic owners."""
from __future__ import annotations

import csv
from contextlib import contextmanager, ExitStack
import hashlib
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
        scratch = ROOT / ".scratch/next-source-schema"
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
        import _browser_products as products
        with patch.object(Path, "open", no_pdf_open), patch.object(Path, "read_bytes", no_pdf_read), \
                patch.object(products, "_generate", side_effect=AssertionError("schema checks must not generate products")):
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


class ChronologySourceSchemaTests(unittest.TestCase):
    """Exercise the real neutral checker with current chronology source files.

    Only unrelated Bible/plan/papal semantics are fixture values. This sparse
    fixture declares no browser-product contract; production still uses its
    normal verified-product gate and never bypasses its freshness checks.
    """

    def setUp(self):
        scratch = ROOT / ".scratch/source-edition-schema-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        families = [family for family in schemas.source_types(ROOT)
                    if family["id"] in {"bible-edition", "scripture-chronology-source"}]
        lines = ['schema_version = 1', 'record_type = "source-document-family-registry"']
        for family in families:
            lines.append("[[families]]")
            lines.extend(key + " = " + json.dumps(value) for key, value in family.items())
            owner = self.root / family["owner"]
            owner.parent.mkdir(parents=True, exist_ok=True)
            owner.write_text("# Fixture owner; semantic execution is not claimed.\n")
        registry = self.root / schemas.REGISTRY
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text("\n".join(lines) + "\n")
        destination = self.root / "src/sources/chronology"
        destination.mkdir(parents=True)
        for source in (ROOT / "src/sources/chronology").glob("*.yaml"):
            (destination / source.name).write_bytes(source.read_bytes())
        self.orientation = destination / "orientation.yaml"

    def report(self):
        with patch.object(schemas, "_bibles", return_value=[{"id": "fixture"}]), \
                patch.object(schemas, "_plans", return_value=([], [])), \
                patch.object(schemas, "_papal_manifests", return_value=(0, 0)), \
                patch.object(schemas._print_catalog, "_papal_pages", return_value={}):
            return schemas.check_source_editions(self.root)

    def test_orientation_is_admitted_with_its_existing_semantic_owner(self):
        report = self.report()
        self.assertTrue(report["ok"], report["errors"])
        chronology = next(row for row in report["families"]
                          if row["id"] == "scripture-chronology-source")
        self.assertEqual(chronology["members"], 6)
        self.assertIn("triptych-chronology-orientation/v1", chronology["schema_ids"])
        self.assertEqual(chronology["semantic_checks"], "owning-gate")
        self.assertEqual(report["external_gates"], [{
            "id": "scripture-chronology-source",
            "command": ["tools/scripture-chronology", "validate"], "status": "not-run"}])

    def test_unregistered_orientation_version_is_still_refused(self):
        self.orientation.write_text(self.orientation.read_text().replace(
            "triptych-chronology-orientation/v1", "triptych-chronology-orientation/v999"))
        report = self.report()
        self.assertFalse(report["ok"])
        self.assertIn("orientation.yaml: unexpected canonical schema", report["errors"][0])

    def test_current_chronology_family_requires_all_six_source_members(self):
        self.orientation.unlink()
        report = self.report()
        self.assertFalse(report["ok"])
        self.assertIn("scripture-chronology-source: fewer members", report["errors"][0])


class VerifiedProductSourceTests(unittest.TestCase):
    """Cold protocol fixtures; product-store cryptography has its own tests.

    The fixture supplies the store's promised private verified snapshot. The
    schema consumer must hold it throughout the check and must never generate,
    fall back to stale logical files, or declare cache paths canonical.
    """

    def setUp(self):
        import _browser_products as products
        self.products = products
        scratch = ROOT / ".scratch/next-source-schema"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.seed = self.root / ".scratch/product-seed"
        self.seed.mkdir(parents=True)
        self.active = False
        self.holds = []
        self.papal_calls = []
        self.write("scripts/_browser_products.py", "# Declared product-store contract fixture.\n")
        self.write("scripts/fixture-schema-owner.py", "# Existing schema owner fixture.\n")
        self.write("src/sources/bibles/fixture/chapters/Gen/1.json", '{"schema":"fixture-canonical"}\n')
        self.write("src/web/data/structure/sources/index.json", '{"schema":"stale-unverified-trap"}\n')
        families = []
        for name in ("bible-edition", "reading-plan", "reading-plan-volume", "papal-selection", "papal-reader"):
            families.append({"id": name, "paths": ["src/web/data/encyclicals/index.json"]
                if name == "papal-reader" else ["src/sources/fixture/*.toml"], "schema_ids": ["fixture"],
                "required_fields": ["id"], "minimum_members": 1})
        families += [{"id": "source-reader-projection", "paths": ["src/web/data/structure/sources/index.json"],
                      "schema_ids": ["triptych-source-reader/v1"], "required_fields": ["schema", "counted", "works"], "minimum_members": 1},
                     {"id": "canonical-bible-fragment", "paths": ["src/sources/bibles/*/chapters/*/*.json"],
                      "schema_ids": ["fixture-canonical"], "required_fields": ["schema"], "minimum_members": 1}]
        lines = ['schema_version = 1', 'record_type = "source-document-family-registry"']
        for family in families:
            lines += ["[[families]]", 'owner = "scripts/fixture-schema-owner.py"', 'validator = ["never-run"]']
            lines += [key + " = " + json.dumps(value) for key, value in family.items()]
        self.write(schemas.REGISTRY, "\n".join(lines) + "\n")
        self.payloads = {
            "encyclicals/index.json": {"counts": {"readers": 1}, "encyclicals": [{"readers": [{"release_id": "fixture", "language": "en"}]}]},
            "structure/sources/index.json": {"schema": "triptych-source-reader/v1", "counted": {"works": 1}, "works": [{"id": "fixture"}]},
        }
        self.descriptor = {"schema": "cold-product-protocol-fixture/v1", "files": {}}
        for name, payload in self.payloads.items():
            body = (json.dumps(payload) + "\n").encode()
            target = self.seed / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            self.descriptor["files"][name] = {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
        self.save_descriptor()
        stack = self.enterContext(ExitStack())
        self.store = stack.enter_context(patch.object(products, "verified_products", side_effect=self.verified))
        self.generate = stack.enter_context(patch.object(products, "_generate", side_effect=AssertionError("no generation")))
        stack.enter_context(patch.object(schemas, "_bibles", side_effect=self.bibles))
        stack.enter_context(patch.object(schemas, "_plans", return_value=([{"id": "fixture-plan"}], [{"id": "fixture-volume"}])))
        stack.enter_context(patch.object(schemas, "_papal_manifests", return_value=(1, 1)))
        stack.enter_context(patch.object(schemas._print_catalog, "_papal_pages", side_effect=self.papal))

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    def save_descriptor(self):
        self.write(schemas.BROWSER_DESCRIPTOR, json.dumps(self.descriptor) + "\n")

    @contextmanager
    def verified(self, root):
        self.assertEqual(root, self.root)
        descriptor = json.loads((root / schemas.BROWSER_DESCRIPTOR).read_text())
        with tempfile.TemporaryDirectory(dir=self.seed.parent) as temporary:
            data = Path(temporary) / "data"
            data.mkdir()
            files = {}
            for name, identity in descriptor["files"].items():
                try:
                    body = (self.seed / name).read_bytes()
                except OSError as error:
                    raise self.products.ProductError(f"browser product bytes/membership differ: missing {name}") from error
                if {"sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)} != identity:
                    raise self.products.ProductError(f"browser product bytes/membership differ: changed {name}")
                path = data / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(body)
                files[name] = path
            held = SimpleNamespace(data_root=data, files=files,
                source_paths={schemas.BROWSER_DESCRIPTOR, "scripts/_browser_products.py"},
                products_identity=hashlib.sha256((root / schemas.BROWSER_DESCRIPTOR).read_bytes()).hexdigest())
            self.holds.append(held)
            self.active = True
            try:
                yield held
            finally:
                self.active = False

    def bibles(self, root, family):
        self.assertTrue(self.active)
        return [{"id": "canonical-fixture-edition"}]

    def papal(self, root, *, data_root, data_source_paths):
        self.assertTrue(self.active)
        self.assertEqual(set(data_source_paths), {schemas.BROWSER_DESCRIPTOR, "scripts/_browser_products.py"})
        self.assertNotIn("src/web/data/encyclicals/index.json", data_source_paths)
        self.papal_calls.append((data_root, data_source_paths))
        data = json.loads((data_root / "encyclicals/index.json").read_text())
        self.assertEqual(data["counts"]["readers"], 1)
        return {"papal-documents/fixture.html": {"title": "Fixture"}}

    def test_cold_products_are_held_and_only_logical_browser_patterns_move(self):
        report = schemas.check_source_editions(self.root)
        self.assertTrue(report["ok"], report["errors"])
        families = {family["id"]: family for family in report["families"]}
        self.assertEqual(families["source-reader-projection"]["members"], 1)
        self.assertEqual(families["canonical-bible-fragment"]["members"], 1)
        self.assertEqual(families["papal-reader"]["members"], 1)
        self.assertEqual(report["browser_products_identity"], self.holds[0].products_identity)
        self.assertFalse(self.holds[0].data_root.exists())
        self.assertNotIn(str(self.seed), json.dumps(report))
        self.assertNotIn(str(self.holds[0].data_root), json.dumps(report))
        self.generate.assert_not_called()

    def test_missing_descriptor_cannot_fall_back_to_existing_logical_files(self):
        (self.root / schemas.BROWSER_DESCRIPTOR).unlink()
        report = schemas.check_source_editions(self.root)
        self.assertFalse(report["ok"])
        self.assertIn(schemas.BROWSER_DESCRIPTOR, report["errors"][0])
        self.store.assert_not_called()
        self.assertFalse(self.papal_calls)

    def test_missing_product_module_and_corrupt_descriptor_fail_closed(self):
        module = self.root / "scripts/_browser_products.py"
        original = module.read_bytes()
        module.unlink()
        report = schemas.check_source_editions(self.root)
        self.assertFalse(report["ok"])
        self.assertIn("scripts/_browser_products.py", report["errors"][0])
        self.store.assert_not_called()
        module.write_bytes(original)
        (self.root / schemas.BROWSER_DESCRIPTOR).write_text("{broken descriptor")
        report = schemas.check_source_editions(self.root)
        self.assertFalse(report["ok"])
        self.assertFalse(self.papal_calls)
        self.generate.assert_not_called()

    def test_sparse_legacy_fixture_without_product_contract_keeps_logical_paths(self):
        (self.root / "scripts/_browser_products.py").unlink()
        (self.root / schemas.BROWSER_DESCRIPTOR).unlink()
        with schemas._held_browser_products(self.root) as held:
            self.assertIsNone(held)
            paths = schemas._family_paths(self.root, ["src/web/data/structure/sources/index.json"], held)
        self.assertEqual(paths, [("src/web/data/structure/sources/index.json",
                                 self.root / "src/web/data/structure/sources/index.json")])
        self.store.assert_not_called()

    def test_missing_or_corrupt_cached_bytes_fail_without_generation(self):
        path = self.seed / "structure/sources/index.json"
        original = path.read_bytes()
        for mode in ("missing", "corrupt"):
            with self.subTest(mode=mode):
                if mode == "missing":
                    path.unlink()
                else:
                    path.write_bytes(b"corrupt product bytes")
                report = schemas.check_source_editions(self.root)
                self.assertFalse(report["ok"])
                self.assertIn("bytes/membership differ", report["errors"][0])
                self.assertFalse(self.papal_calls)
                path.write_bytes(original)
        self.generate.assert_not_called()

    def test_missing_verified_family_does_not_silently_count_zero(self):
        del self.descriptor["files"]["structure/sources/index.json"]
        self.save_descriptor()
        report = schemas.check_source_editions(self.root)
        self.assertFalse(report["ok"])
        self.assertIn("source-reader-projection", report["errors"][0])
        self.assertIn("src/web/data/structure/sources/index.json", report["errors"][0])

    def test_product_schema_errors_name_logical_paths_not_cache_paths(self):
        path = self.seed / "structure/sources/index.json"
        path.write_text('{"schema":"wrong"}\n')
        body = path.read_bytes()
        self.descriptor["files"]["structure/sources/index.json"] = {
            "sha256": hashlib.sha256(body).hexdigest(), "bytes": len(body)}
        self.save_descriptor()
        report = schemas.check_source_editions(self.root)
        self.assertFalse(report["ok"])
        self.assertIn("src/web/data/structure/sources/index.json", report["errors"][0])
        self.assertNotIn(str(self.seed), report["errors"][0])
        self.assertNotIn(str(self.holds[0].data_root), report["errors"][0])


if __name__ == "__main__":
    unittest.main()
