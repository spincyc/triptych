"""Act reconstruction preserves exact witnesses and admits only bounded texts."""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_acta as acta
import _papal_sources as sources
import _typeset_papal as typeset

LOADER = importlib.machinery.SourceFileLoader("acta_test_source_library", str(ROOT / "tools/source-library"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
SOURCE_LIBRARY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SOURCE_LIBRARY
SPEC.loader.exec_module(SOURCE_LIBRARY)

REVISION = "2026-10-26T00:00:00Z"
WRAPPER = b"MODERN WRAPPER: synthetic wording excluded before retention.\n"
TEXT = (
    b"ACTA SYNTHETICA\r\n" + WRAPPER
    + b"SYNTHETIC INCIPIT\n"
    + b"Prima pars.\fSecunda pars in eadem linea physica.\n"
    + b"Datum Romae. TEST PP.\n"
)
RETAINED = TEXT.replace(WRAPPER, b"")


class ActaFixture(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/acta-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        (self.root / "src/gpt").mkdir(parents=True)
        self.environment = {**os.environ, "TRIPTYCH_LIBRARY_CACHE": "0", "PYTHONDONTWRITEBYTECODE": "1"}
        self.pdf = b"%PDF-1.4\n% Synthetic project-owned fixture, not a renderable scan.\n%%EOF\n"
        self.write(".scratch/witness.pdf", self.pdf)
        self.write(".scratch/witness.txt", TEXT)
        self.volume = {
            "archive_id": "archive.ass.001",
            "pdf_path": ".scratch/witness.pdf",
            "text_path": ".scratch/witness.txt",
            "source_url": "https://www.vatican.va/archive/ass/documents/ASS-01-fixture.pdf",
            "pdf_sha256": hashlib.sha256(self.pdf).hexdigest(),
            "text_sha256": hashlib.sha256(TEXT).hexdigest(),
            "pdf_bytes": len(self.pdf),
            "text_bytes": len(TEXT),
            "page_count": 2,
            "publication_year": 1900,
            "historical_printing_basis": "Synthetic project-owned fixture labelled as a 1900 printing; no external source wording.",
            "extraction_command": ["pdftotext", "-layout", "-enc", "UTF-8", ".scratch/witness.pdf", ".scratch/witness.txt"],
            "historical_text_line_ranges": [[1, 1], [3, 5]],
            "excluded_wrapper_ranges": [[2, 2]],
            "acts": [self.act()],
            "gaps": [],
        }
    def act(self, **updates):
        return {
            "local_id": "ass-001-synthetic-act",
            "title": "Synthetic incipit",
            "pope": "Test Pope",
            "date": "1900-01-01",
            "document_type": "apostolic-letter",
            "language": "la",
            "physical_line_ranges": [[3, 5]],
            "artifact_page_ranges": [[1, 2]],
            "printed_pages": "1-2",
            "identity_evidence": "Synthetic issuer, incipit and dating clause identify the fixture act.",
            "boundary_evidence": "Synthetic opening through final dating clause; no omitted body or unresolved boundary.",
            "source_note": "Project-owned synthetic fixture, not a historical transcription.",
            "completeness": "complete",
            "canonical_work_id": None,
            "canonical_join_evidence": None,
            **updates,
        }

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def write_json(self, relative, data):
        return self.write(relative, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    def recipe(self, volumes=None, relative=".scratch/recipes.json"):
        return self.write_json(relative, {"schema": "triptych-acta-recipes/v1", "volumes": volumes or [self.volume]})

    def catalog(self, *, register=True, volumes=None):
        return acta.catalog(self.root, volumes or [self.volume], REVISION, register=register)

    def records(self, name):
        return [(path, tomllib.loads(path.read_text(encoding="utf-8")))
                for path in sorted((self.root / "src/sources/works").rglob(name))]

    def cli(self, *arguments):
        return subprocess.run([str(ROOT / "tools/papal-acta"), *arguments, "--root", str(self.root), "--json"],
                              cwd=ROOT, env=self.environment, text=True, capture_output=True, check=False)


class PhysicalExtentTests(ActaFixture):
    def test_physical_lines_use_only_lf_and_preserve_form_feed(self):
        lines = acta.physical_lines(TEXT)
        self.assertEqual(len(lines), 5)
        self.assertIn(b"\f", lines[3])
        self.assertEqual(len(acta.physical_lines(b"first\rsecond\fthird\nlast")), 2)
        self.assertEqual(acta.physical_lines(b""), [])

    def test_ranges_are_positive_inclusive_ordered_and_nonoverlapping(self):
        acta.bounds([[1, 1], [3, 5]], 5)
        for ranges in ([[0, 1]], [[1, 6]], [[2, 1]], [[1, 3], [3, 4]],
                       [[3, 4], [1, 2]], [[True, 2]], [[1.0, 2]], [[1]], "1-2"):
            with self.subTest(ranges=ranges), self.assertRaises(ValueError):
                acta.bounds(ranges, 5)

    def test_wrapper_exclusion_preserves_every_other_byte_and_remaps_ranges(self):
        retained, mapping, transformation = acta.retain_derivative(self.root, self.volume, self.volume)
        self.assertEqual(retained, RETAINED)
        self.assertNotIn(WRAPPER, retained)
        self.assertEqual(acta.remap([[3, 5]], mapping), [[2, 4]])
        self.assertTrue(transformation)
        for ranges in ([[2, 2]], [[1, 3]], [[6, 6]], [[4, 5], [3, 3]], [[3, 4], [4, 5]]):
            with self.subTest(ranges=ranges), self.assertRaises(ValueError):
                acta.remap(ranges, mapping)

    def test_retention_requires_exact_hash_and_byte_extent(self):
        for field, wrong in (("text_sha256", "0" * 64), ("text_bytes", len(TEXT) + 1),
                             ("pdf_sha256", "0" * 64), ("pdf_bytes", len(self.pdf) + 1)):
            volume = {**self.volume, field: wrong}
            with self.subTest(field=field), self.assertRaises(ValueError):
                acta.read_recipes(self.root, [self.recipe([volume])])

    def test_historical_and_excluded_ranges_cannot_overlap(self):
        for updates in ({"historical_text_line_ranges": [[1, 5]]},
                        {"excluded_wrapper_ranges": [[2, 3]]}):
            volume = {**self.volume, **updates}
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                acta.retain_derivative(self.root, volume, volume)

    def test_ordered_derivative_requires_exact_parent_hash_extent_and_reproduction(self):
        raw = b"Datum Romae.\nPars prima.\nINCIPIT.\n"
        ordered = b"INCIPIT.\nPars prima.\nDatum Romae.\n"
        self.write(".scratch/source-parent.txt", raw)
        self.write(".scratch/ordered.txt", ordered)
        derivative = {
            "text_path": ".scratch/ordered.txt", "text_sha256": hashlib.sha256(ordered).hexdigest(),
            "text_bytes": len(ordered), "extraction_command": "Synthetic exact source line reordering.",
            "source_parent_text_path": ".scratch/source-parent.txt", "source_parent_text_sha256": hashlib.sha256(raw).hexdigest(),
            "source_parent_text_bytes": len(raw), "ordered_source_line_ranges": [[3, 3], [2, 2], [1, 1]],
        }
        self.volume["additional_derivatives"] = [derivative]
        acta.read_recipes(self.root, [self.recipe()])
        for updates in ({"source_parent_text_sha256": "0" * 64}, {"source_parent_text_bytes": len(raw) + 1},
                        {"ordered_source_line_ranges": [[1, 3]]}, {"ordered_source_line_ranges": [[4, 4]]}):
            self.volume["additional_derivatives"] = [{**derivative, **updates}]
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                acta.read_recipes(self.root, [self.recipe()])
        self.volume["additional_derivatives"] = [derivative]
        data = self.catalog()
        restricted = {record["sha256"]: record for _, record in self.records("artifact.toml") if record["storage"] == "restricted"}
        parent = restricted[hashlib.sha256(raw).hexdigest()]
        child = restricted[hashlib.sha256(ordered).hexdigest()]
        self.assertEqual(parent["derived_from"], data["volumes"][0]["pdf_artifact_id"])
        self.assertEqual(child["derived_from"], parent["id"])
        self.assertNotIn("path", parent)
        self.assertNotIn("path", child)
        with patch.dict(os.environ, {"TRIPTYCH_LIBRARY_CACHE": "0"}):
            library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [], "\n".join(library.errors))

    def test_raw_source_paths_must_stay_in_repository_scratch(self):
        for field, path in (("pdf_path", "../outside.pdf"), ("text_path", "src/sources/witness.txt")):
            volume = {**self.volume, field: path}
            with self.subTest(field=field), self.assertRaises(ValueError):
                acta.read_recipes(self.root, [self.recipe([volume])])

    def test_unicode_source_column_slices_replay_exact_characters(self):
        parent = "αbody HEADER\nleft right\n".encode("utf-8")
        selected = "αbody\nleft\nright\n".encode("utf-8")
        self.write(".scratch/columns.txt", parent)
        self.write(".scratch/selected.txt", selected)
        derivative = {
            "text_path": ".scratch/selected.txt", "text_sha256": acta.sha(selected),
            "text_bytes": len(selected), "source_parent_text_path": ".scratch/columns.txt",
            "source_parent_text_sha256": acta.sha(parent), "source_parent_text_bytes": len(parent),
            "ordered_source_line_slices": [
                {"physical_line_range": [1, 1], "unicode_columns": [0, 5]},
                {"physical_line_range": [2, 2], "unicode_columns": [0, 4]},
                {"physical_line_range": [2, 2], "unicode_columns": [5, None]},
            ],
        }
        self.assertEqual(acta.source_parent(self.root, derivative), (parent, acta.sha(parent)))
        for bad in ([{"physical_line_range": [1, 1], "unicode_columns": [-1, 5]}],
                    [{"physical_line_range": [1, 1], "unicode_columns": [True, 5]}],
                    [{"physical_line_range": [1, 1], "unicode_columns": [0, 4]}]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                acta.source_parent(self.root, {**derivative, "ordered_source_line_slices": bad})
        with self.assertRaises(ValueError):
            acta.source_parent(self.root, {**derivative, "ordered_source_line_ranges": [[1, 2]]})

    def test_header_fragments_keep_the_original_lf_row_boundary(self):
        parent = "body HEADER continues\nnext row\n".encode()
        output = "body  continues\nnext row\n".encode()
        self.write(".scratch/fragment-parent.txt", parent)
        self.write(".scratch/fragment-output.txt", output)
        derivative = {"text_path": ".scratch/fragment-output.txt", "source_parent_text_path": ".scratch/fragment-parent.txt",
                      "source_parent_text_sha256": acta.sha(parent), "ordered_source_line_slices": [
                          {"physical_line_range": [1, 1], "unicode_columns": [0, 5]},
                          {"physical_line_range": [1, 1], "unicode_columns": [11, None], "join_previous": True},
                          {"physical_line_range": [2, 2], "unicode_columns": None},
                      ]}
        self.assertEqual(acta.source_parent(self.root, derivative), (parent, acta.sha(parent)))
        bad = copy.deepcopy(derivative)
        bad["ordered_source_line_slices"][1]["physical_line_range"] = [2, 2]
        with self.assertRaises(ValueError):
            acta.source_parent(self.root, bad)


class RegistrationTests(ActaFixture):
    def test_registration_keeps_one_container_payload_and_truthful_cross_work_segments(self):
        data = self.catalog()
        self.assertEqual(acta.validate_catalog(self.root, data)["retained_act_witnesses"], 1)
        row = data["documents"][0]
        self.assertTrue(row["text_available"])
        self.assertEqual(row["physical_line_ranges"], [[2, 4]])
        self.assertEqual(row["source_physical_line_ranges"], [[3, 5]])
        self.assertEqual((self.root / row["text_path"]).read_bytes(), RETAINED)
        artifacts = self.records("artifact.toml")
        retained = [record for _, record in artifacts if record["storage"] == "tracked"]
        self.assertEqual(len(retained), 1)
        controller = retained[0]
        self.assertEqual(controller["id"], row["artifact_id"])
        self.assertEqual(controller["sha256"], hashlib.sha256(RETAINED).hexdigest())
        self.assertEqual(controller["byte_size"], len(RETAINED))
        self.assertNotEqual(controller["edition_id"], row["edition_id"])
        for _, record in artifacts:
            if record["storage"] != "tracked":
                self.assertNotIn("path", record)
        segments = self.records("historical-text.toml")
        self.assertEqual(len(segments), 1)
        segment = segments[0][1]
        self.assertEqual(segment["schema"], 2)
        self.assertEqual(segment["edition_id"], row["edition_id"])
        self.assertEqual(segment["artifact_id"], controller["id"])
        self.assertEqual(segment["artifact_sha256"], controller["sha256"])
        self.assertNotIn("rights_status", segment)
        self.assertNotIn("path", segment)
        pdf_segments = self.records("archival-pdf.toml")
        self.assertEqual(pdf_segments[0][1]["artifact_page_ranges"], [[1, 2]])
        self.assertEqual(pdf_segments[0][1]["artifact_sha256"], self.volume["pdf_sha256"])
        for path in (self.root / "src/sources/works").rglob("*"):
            if path.is_file():
                self.assertNotIn(WRAPPER.rstrip(), path.read_bytes(), str(path))

    def test_registered_graph_passes_the_source_library_validator(self):
        self.catalog()
        with patch.dict(os.environ, {"TRIPTYCH_LIBRARY_CACHE": "0"}):
            library = SOURCE_LIBRARY.load_library(self.root)
        self.assertEqual(library.errors, [], "\n".join(library.errors))

    def test_index_is_read_only_and_does_not_admit_unregistered_bodies(self):
        data = self.catalog(register=False)
        self.assertEqual(data["coverage"]["source_act_records"], 1)
        self.assertFalse(data["documents"][0]["text_available"])
        self.assertFalse((self.root / "src/sources/works").exists())
        self.assertEqual(acta.make_manifest(data, REVISION)["documents"], [])

    def test_complete_later_or_mixed_language_body_is_rejected_before_mutation(self):
        for updates in ({"publication_year": 1931}, {"metadata_only": True}):
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                self.catalog(volumes=[{**self.volume, **updates}])
        self.volume["acts"][0]["language"] = "mul"
        with self.assertRaises(ValueError):
            self.catalog()
        self.assertFalse((self.root / "src/sources/works").exists())

    def test_historical_act_date_does_not_clear_a_later_printing(self):
        self.volume["historical_printing_year"] = 1968
        with self.assertRaises(ValueError):
            self.catalog()
        self.assertFalse((self.root / "src/sources/works").exists())

    def test_unknown_act_date_remains_unknown_despite_known_printing_year(self):
        self.volume["acts"][0]["date"] = None
        data = self.catalog()
        self.assertIsNone(data["documents"][0]["date"])
        self.assertIsNone(acta.make_manifest(data, REVISION)["documents"][0]["date"])
        for _, record in self.records("work.toml"):
            self.assertNotIn("composed", record)

    def test_unresolved_boundaries_are_cataloged_without_an_admitted_act(self):
        self.volume["acts"][0].update({"completeness": "unresolved", "boundary_evidence": "Closing boundary not established."})
        data = self.catalog()
        self.assertEqual(data["coverage"]["unresolved"], 1)
        self.assertFalse(data["documents"][0]["text_available"])
        self.assertEqual(acta.make_manifest(data, REVISION)["documents"], [])
        self.assertFalse(self.records("historical-text.toml"))

    def test_complete_act_requires_identity_and_boundary_evidence_and_valid_ranges(self):
        for updates in ({"boundary_evidence": ""}, {"identity_evidence": ""},
                        {"physical_line_ranges": []}, {"physical_line_ranges": [[2, 5]]},
                        {"artifact_page_ranges": [[1, 3]]}):
            volume = copy.deepcopy(self.volume)
            volume["acts"][0].update(updates)
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                self.catalog(volumes=[volume])
        self.assertFalse((self.root / "src/sources/works").exists())

    def test_metadata_only_later_volume_retains_no_protected_payload(self):
        self.volume.update({"publication_year": 2026, "metadata_only": True})
        self.volume.pop("historical_printing_basis")
        self.volume["acts"][0].update({"date": "2026-01-01", "completeness": "metadata-only"})
        data = self.catalog()
        self.assertEqual(data["coverage"]["metadata_only"], 1)
        self.assertEqual(acta.make_manifest(data, REVISION)["documents"], [])
        self.assertFalse(list((self.root / "src/sources/works").rglob("*.txt")))
        self.assertFalse(list((self.root / "src/sources/works").rglob("*.pdf")))
        self.assertFalse(self.records("historical-text.toml"))
        for _, record in self.records("artifact.toml"):
            self.assertEqual(record["storage"], "restricted")
            self.assertNotIn("path", record)

    def test_duplicate_volume_and_local_act_ids_are_rejected(self):
        first = self.recipe()
        second = self.recipe(relative=".scratch/duplicate.json")
        with self.assertRaises(ValueError):
            acta.read_recipes(self.root, [first, second])
        self.volume["acts"].append(copy.deepcopy(self.volume["acts"][0]))
        with self.assertRaises(ValueError):
            acta.read_recipes(self.root, [self.recipe()])

    def test_join_requires_evidence_and_an_existing_canonical_work(self):
        row = self.volume["acts"][0]
        row["canonical_work_id"] = "work.fixture.existing"
        with self.assertRaises(ValueError):
            self.catalog()
        row["canonical_join_evidence"] = "Synthetic same issuer/date/incipit comparison."
        with self.assertRaises(ValueError):
            self.catalog()
        self.assertFalse((self.root / "src/sources/works").exists())

    def existing_work(self):
        directory = self.root / "src/sources/works/fixture/existing"
        work = directory / "work.toml"
        edition = directory / "editions/1890-existing/edition.toml"
        sources.write_record(work, {"schema": 1, "record_type": "work", "id": "work.fixture.existing",
                                   "title": "Original canonical title", "responsible": "Test Pope", "work_type": "apostolic-letter"})
        sources.write_record(edition, {"schema": 1, "record_type": "edition", "id": "edition.fixture.existing.1890",
                                      "work_id": "work.fixture.existing", "title": "Existing edition", "language": "la", "date": "1890"})
        return work, edition

    def test_reviewed_join_reuses_work_without_rewriting_it_or_old_edition(self):
        work, edition = self.existing_work()
        before = {path: path.read_bytes() for path in (work, edition)}
        self.volume["acts"][0].update({"canonical_work_id": "work.fixture.existing",
                                       "canonical_join_evidence": "Synthetic issuer/date/incipit comparison identifies the same work."})
        data = self.catalog()
        self.assertEqual(data["documents"][0]["work_id"], "work.fixture.existing")
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        works = self.records("work.toml")
        self.assertEqual(sum(record["id"] == "work.fixture.existing" for _, record in works), 1)
        self.assertEqual(len(works), 2)

    def test_manifest_selects_one_witness_for_each_work_and_language(self):
        self.existing_work()
        first = self.volume["acts"][0]
        first.update({"canonical_work_id": "work.fixture.existing", "canonical_join_evidence": "Synthetic identity comparison."})
        second = {**first, "local_id": "ass-001-second-witness"}
        third = {**first, "local_id": "ass-001-english-witness", "language": "en"}
        self.volume["acts"] = [first, second, third]
        data = self.catalog()
        self.assertEqual(len(data["documents"]), 3)
        manifest = acta.make_manifest(data, REVISION)
        self.assertEqual(len(manifest["documents"]), 2)
        self.assertEqual({row["language"] for row in manifest["documents"]}, {"la", "en"})

    def test_reviewed_language_witnesses_share_one_new_work(self):
        first = self.volume["acts"][0]
        first.update({"work_local_id": "same-act", "work_identity_evidence": "Synthetic issuer/date/incipit comparison."})
        self.volume["acts"].append({**first, "local_id": "ass-001-english", "language": "en", "title": "English fixture title"})
        data = self.catalog()
        self.assertEqual(len({row["work_id"] for row in data["documents"]}), 1)
        works = [record for _, record in self.records("work.toml") if record.get("work_type") == "apostolic-letter"]
        self.assertEqual(len(works), 1)
        self.assertEqual(set(works[0]["languages"]), {"la", "en"})
        self.assertEqual(len(acta.make_manifest(data, REVISION)["documents"]), 2)

    def test_language_group_requires_evidence_and_consistent_issuer_and_date(self):
        for updates in ({"work_identity_evidence": ""}, {"pope": "Different Pope"}, {"date": "1900-01-02"}):
            volume = copy.deepcopy(self.volume)
            first = volume["acts"][0]
            first.update({"work_local_id": "same-act", "work_identity_evidence": "Synthetic identity comparison."})
            volume["acts"].append({**first, "local_id": "ass-001-english", "language": "en", **updates})
            with self.subTest(updates=updates), self.assertRaises(ValueError):
                self.catalog(volumes=[volume])
        self.assertFalse((self.root / "src/sources/works").exists())

    def test_source_explicit_translation_date_conflict_is_preserved(self):
        first = self.volume["acts"][0]
        first.update({"work_local_id": "same-act", "work_identity_evidence": "Source explicitly labels the next version as a translation.",
                      "work_date_discrepancy": "Synthetic versions give different dates; neither date is resolved."})
        self.volume["acts"].append({**first, "local_id": "ass-001-english", "language": "en", "date": "1900-01-02"})
        data = self.catalog()
        self.assertEqual(len({row["work_id"] for row in data["documents"]}), 1)
        self.assertEqual({row["date"] for row in data["documents"]}, {"1900-01-01", "1900-01-02"})
        work = next(record for _, record in self.records("work.toml") if record.get("work_type") == "apostolic-letter")
        self.assertNotIn("composed", work)

    def test_repeated_registration_is_byte_identical(self):
        first = self.catalog()
        before = {path: path.read_bytes() for path in (self.root / "src/sources/works").rglob("*") if path.is_file()}
        second = self.catalog()
        self.assertEqual(first, second)
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_same_pdf_subsets_reuse_one_container_and_retained_payload(self):
        second = copy.deepcopy(self.volume)
        second["archive_id"] = "archive.ass.001.subset"
        second["parent_archive_id"] = self.volume["archive_id"]
        second["acts"][0]["local_id"] = "second-source-witness"
        data = self.catalog(volumes=[self.volume, second])
        self.assertEqual(len({v["pdf_artifact_id"] for v in data["volumes"]}), 1)
        self.assertEqual(len({a["artifact_id"] for a in data["documents"]}), 1)
        self.assertEqual(data["coverage"]["unique_pdf_witnesses"], 1)
        self.assertEqual(data["coverage"]["numbered_volumes_by_series"], {"ASS": 1})
        self.assertEqual(sum(r["storage"] == "tracked" for _, r in self.records("artifact.toml")), 1)

    def test_existing_ass_journal_identity_is_reused(self):
        owner = self.root / "src/sources/works/holy-see/acta-sanctae-sedis"
        sources.write_record(owner / "work.toml", {"schema": 1, "record_type": "work", "id": "work.holy-see.acta-sanctae-sedis",
            "title": "Acta Sanctae Sedis", "responsible": "Historical editors", "work_type": "periodical"})
        data = self.catalog()
        self.assertEqual(data["volumes"][0]["container_work_id"], "work.holy-see.acta-sanctae-sedis")
        self.assertFalse((self.root / acta.SOURCE_ROOT / "acta-sanctae-sedis").exists())

    def test_exact_existing_pdf_ancestor_url_controls_the_reader_link(self):
        owner = self.root / "src/sources/works/holy-see/acta-sanctae-sedis"
        sources.write_record(owner / "work.toml", {"schema": 1, "record_type": "work", "id": "work.holy-see.acta-sanctae-sedis",
            "title": "Acta Sanctae Sedis", "responsible": "Historical editors", "work_type": "periodical"})
        edition = owner / "editions/1900-fixture"
        eid = "edition.holy-see.acta-sanctae-sedis.fixture"
        sources.write_record(edition / "edition.toml", {"schema": 1, "record_type": "edition", "id": eid,
            "work_id": "work.holy-see.acta-sanctae-sedis", "title": "Synthetic printing", "language": "la", "date": "1900"})
        actual = "https://archive.org/download/synthetic-fixture/synthetic-fixture.pdf"
        sources.write_record(edition / "artifacts/raw-pdf/artifact.toml", {"schema": 2, "record_type": "artifact",
            "id": "artifact.holy-see.acta-sanctae-sedis.fixture.raw-pdf", "edition_id": eid, "artifact_type": "scan-pdf",
            "media_type": "application/pdf", "storage": "restricted", "rights_status": "unresolved",
            "rights_basis": "Synthetic fixture; raw parent is not retained.", "sha256": acta.sha(self.pdf), "byte_size": len(self.pdf),
            "page_count": 2, "source_url": actual})
        data = self.catalog()
        self.assertEqual(data["documents"][0]["source_url"], actual)
        self.assertEqual(data["documents"][0]["discovery_source_url"], self.volume["source_url"])
        self.assertEqual(acta.make_manifest(data, REVISION)["documents"][0]["source_url"], actual)

    def test_machine_issuer_id_has_a_truthful_human_display_name(self):
        self.volume["acts"][0]["pope"] = "pius-x"
        data = self.catalog()
        self.assertEqual(data["documents"][0]["pope"], "Pius X")
        self.assertEqual(data["documents"][0]["pope_id"], "pius-x")
        work = next(r for _, r in self.records("work.toml") if r.get("work_type") == "apostolic-letter")
        self.assertEqual(work["responsible"], "Pius X")

    def test_retained_fragment_does_not_enter_the_complete_act_manifest(self):
        data = self.catalog()
        data["documents"][0]["completeness"] = "unresolved"
        data["documents"][0]["retained_fragment_available"] = True
        self.assertEqual(acta.make_manifest(data, REVISION)["documents"], [])

    def test_catalog_rejects_duplicate_act_ids_and_falsified_coverage(self):
        data = self.catalog()
        duplicate = copy.deepcopy(data)
        duplicate["documents"].append(copy.deepcopy(data["documents"][0]))
        with self.assertRaises(ValueError):
            acta.validate_catalog(self.root, duplicate)
        data["coverage"]["retained_act_witnesses"] += 1
        with self.assertRaises(ValueError):
            acta.validate_catalog(self.root, data)

    def test_catalog_detects_mutated_controller_hash_size_and_segment(self):
        data = self.catalog()
        row = data["documents"][0]
        payload_path = self.root / row["text_path"]
        payload = payload_path.read_bytes()
        payload_path.write_bytes(payload + b"tampered\n")
        with self.assertRaises(ValueError):
            acta.validate_catalog(self.root, data)
        payload_path.write_bytes(payload)
        segment_path = self.root / row["segment_path"]
        segment = tomllib.loads(segment_path.read_text())
        segment["artifact_sha256"] = "0" * 64
        sources.write_record(segment_path, segment)
        with self.assertRaises(ValueError):
            acta.validate_catalog(self.root, data)

    def test_manifest_round_trip_resolves_only_the_act_and_handles_page_form_feed(self):
        data = self.catalog()
        path = self.write_json(".scratch/manifest.json", acta.make_manifest(data, REVISION))
        _, documents = typeset.read_manifest(path, self.root)
        self.assertEqual(len(documents), 1)
        text = documents[0]["text"]
        self.assertNotIn("ACTA SYNTHETICA", text)
        self.assertNotIn("MODERN WRAPPER", text)
        self.assertEqual(text.split(), b"\n".join(TEXT.split(b"\n")[2:]).decode().split())


class CommandLineTests(ActaFixture):
    def test_index_and_series_listing_preserve_metadata_without_source_mutation(self):
        result = self.cli("index", "--recipes", str(self.recipe()), "--revision", REVISION, "--out", ".scratch/index.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertFalse((self.root / "src/sources/works").exists())
        for series, count in (("ASS", 1), ("AAS", 0)):
            result = self.cli("list", "--catalog", ".scratch/index.json", "--series", series)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data["count"], count)
            for row in data["documents"]:
                self.assertFalse(row["text_available"])

    def test_register_check_and_manifest_round_trip(self):
        recipe = self.recipe()
        result = self.cli("register", "--recipes", str(recipe), "--revision", REVISION,
                          "--out", ".scratch/catalog.json", "--manifest", ".scratch/manifest.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["v"], 1)
        self.assertTrue((self.root / ".scratch/manifest.json").exists())
        result = self.cli("check", "--catalog", ".scratch/catalog.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["retained_act_witnesses"], 1)
        result = self.cli("manifest", "--catalog", ".scratch/catalog.json", "--revision", REVISION,
                          "--out", ".scratch/second-manifest.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.root / ".scratch/manifest.json").read_bytes(),
                         (self.root / ".scratch/second-manifest.json").read_bytes())

    def test_invalid_recipe_fails_without_writing_catalog_or_source_records(self):
        self.volume["pdf_sha256"] = "0" * 64
        result = self.cli("register", "--recipes", str(self.recipe()), "--revision", REVISION,
                          "--out", ".scratch/catalog.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertEqual(json.loads(result.stderr)["status"], "error")
        self.assertFalse((self.root / ".scratch/catalog.json").exists())
        self.assertFalse((self.root / "src/sources/works").exists())


if __name__ == "__main__":
    unittest.main()
