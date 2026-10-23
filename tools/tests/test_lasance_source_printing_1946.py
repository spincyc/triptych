"""Exact printing identity does not clear a mixed Lasance whole-book scan."""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import tomllib
import unittest

from tools.tests import test_calendar_translation_overlay as base
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _lasance_publication import (
    LASANCE_1945_EDITION,
    LASANCE_1945_PAGE_ARTIFACT,
    LASANCE_1945_RIGHTS_ARTIFACT,
    LASANCE_1946_EDITION,
    LASANCE_1946_PAGE_ARTIFACT,
    LASANCE_1946_WITNESS,
    approved_lasance_printed_page,
    numbered_page_match,
)

OWNER = ROOT / (
    "src/sources/works/francis-xavier-lasance/the-new-roman-missal/"
    "editions/1946-benziger-revised-1945"
)


class Lasance1946PublicationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = base.PublicationBindingTests(
            "test_valid_dual_binding_keeps_remote_page_proof_separate"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.checker = self.fixture.checker
        self.reader = base.load_propers()
        self.records = self.fixture.records
        self.entry = self.fixture.entry
        edition = tomllib.loads((OWNER / "edition.toml").read_text())
        page = tomllib.loads((OWNER / (
            "artifacts/ia-google-facsimile-pdf-4573991d/artifact.toml"
        )).read_text())
        rights = tomllib.loads((ROOT / (
            "src/sources/works/francis-xavier-lasance/the-new-roman-missal/"
            "editions/benziger-revised-1945/artifacts/"
            "new-roman-missal-text-80b34759/artifact.toml"
        )).read_text())
        self.records.pop(self.fixture.edition_id)
        self.records.pop(self.fixture.page_artifact_id)
        self.records[LASANCE_1946_EDITION] = base.record(**edition)
        self.records[LASANCE_1946_PAGE_ARTIFACT] = base.record(**page)
        self.records[LASANCE_1945_RIGHTS_ARTIFACT] = base.record(**rights)
        self.entry.update(
            mass="fixture", form_id="main", proper="Collect", cycle="all",
            occurrence=1, witness=LASANCE_1946_WITNESS,
            artifact_id=LASANCE_1946_PAGE_ARTIFACT,
            ia_leaf=454, ia_leaf_range=[454, 454], printed_page="445",
        )
        self.entry["translations"][0]["source_id"] = LASANCE_1946_EDITION
        for key in (self.fixture.page_passage_id, self.fixture.publication_passage_id,
                    self.fixture.publication_artifact_id):
            self.records[key].data["edition_id"] = LASANCE_1946_EDITION
        self.records[self.fixture.page_passage_id].data.update(
            artifact_id=LASANCE_1946_PAGE_ARTIFACT,
            artifact_sha256=page["sha256"], artifact_page_ranges=[[455, 455]],
            locus="Synthetic fixture Collect", context="Exact body, printed p. 445.",
        )
        self.records[self.fixture.publication_passage_id].data["locus"] = (
            "Synthetic fixture Collect"
        )
        payload = io.StringIO(newline="")
        writer = csv.writer(payload, delimiter="\t", lineterminator="\n")
        writer.writerow(("mass", "form_id", "proper", "cycle", "occurrence", "english_json"))
        writer.writerow(("fixture", "main", "Collect", "all", 1, json.dumps("Exact body.")))
        self.fixture.payload.write_text(payload.getvalue())
        digest = hashlib.sha256(self.fixture.payload.read_bytes()).hexdigest()
        self.entry["publication_artifact_sha256"] = digest
        self.records[self.fixture.publication_artifact_id].data.update(
            sha256=digest, derived_from=LASANCE_1946_PAGE_ARTIFACT,
        )
        self.records[self.fixture.publication_passage_id].data.update(artifact_sha256=digest)
        self.witnesses = {LASANCE_1946_WITNESS: {
            "id": LASANCE_1946_WITNESS, "source_id": LASANCE_1946_EDITION,
            "artifact_id": LASANCE_1945_RIGHTS_ARTIFACT, "rights": "public-domain",
            "rights_jurisdiction": "United States",
            "caution": "Original1937/1945 ordinary English only; whole scan unresolved; inserts excluded.",
        }}
        self.calendar_root = self.fixture.root / "src/sources/calendars"
        self.calendar_root.mkdir(parents=True)
        self.path = self.fixture.root / "inventory.toml"
        self.reader._source_library_records = lambda root: ({
            key: dict(value.data, id=key, record_type=value.record_type)
            for key, value in self.records.items()
        }, [])

    def publication(self, entry=None, witnesses=None):
        return self.checker.overlay_entry_publication_problems(
            "entry", self.entry if entry is None else entry,
            self.witnesses if witnesses is None else witnesses,
        )

    def reader_publication(self, entry=None, witnesses=None):
        return self.reader.validate_translation_publication_binding(
            self.entry if entry is None else entry, self.calendar_root, self.path,
            self.witnesses if witnesses is None else witnesses,
        )

    def assert_rights_rejected(self, entry=None, witnesses=None):
        self.assertIn("registered Lasance1945", "\n".join(self.publication(entry, witnesses)))
        with self.assertRaisesRegex(ValueError, "registered Lasance1945"):
            self.reader_publication(entry, witnesses)

    def test_exact_source_metadata_and_both_consumers_accept_only_transcription(self):
        self.assertEqual(self.publication(), [])
        self.assertIsNone(self.reader_publication())
        self.assertEqual(self.checker.overlay_entry_source_problems(
            "entry", self.entry, self.witnesses), [])
        page = self.records[LASANCE_1946_PAGE_ARTIFACT].data
        self.assertEqual((page["storage"], page["rights_status"], page["indexable"]),
                         ("remote", "unresolved", False))
        self.assertEqual(self.records[LASANCE_1946_EDITION].data["date"], "1946")
        self.assertEqual(self.records[LASANCE_1945_RIGHTS_ARTIFACT].data["edition_id"],
                         LASANCE_1945_EDITION)

    def test_actual_edition_date_language_and_work_cannot_be_relabeled(self):
        edition = self.records[LASANCE_1946_EDITION].data
        for key, value in (("date", "1930"), ("date", "1945"), ("date", "1947"),
                           ("date", "1955"), ("date", "1937"),
                           ("language", "la"), ("work_id", "work.other-missal")):
            with self.subTest(key=key, value=value):
                old = edition[key]
                edition[key] = value
                self.assert_rights_rejected()
                edition[key] = old

    def test_unknown_1946_edition_is_not_a_printing_profile(self):
        publication = self.records[self.fixture.publication_artifact_id].data
        publication["edition_id"] = "edition.other.1946"
        self.records["edition.other.1946"] = base.record("edition", date="1946")
        self.assert_rights_rejected()

    def test_known_1945_identity_cannot_use_a_false_pre1931_date_either(self):
        old_owner = OWNER.parent / "benziger-revised-1945"
        edition = tomllib.loads((old_owner / "edition.toml").read_text())
        page = tomllib.loads((old_owner / (
            "artifacts/internet-archive-facsimile-pdf-6cf3c3d0/artifact.toml"
        )).read_text())
        self.records.pop(LASANCE_1946_EDITION)
        self.records.pop(LASANCE_1946_PAGE_ARTIFACT)
        for record in self.records.values():
            if record.data.get("edition_id") == LASANCE_1946_EDITION:
                record.data["edition_id"] = LASANCE_1945_EDITION
        self.records[LASANCE_1945_EDITION] = base.record(**edition)
        self.records[LASANCE_1945_PAGE_ARTIFACT] = base.record(**page)
        self.entry.update(artifact_id=LASANCE_1945_PAGE_ARTIFACT, witness="lasance-1945")
        self.entry["translations"][0]["source_id"] = LASANCE_1945_EDITION
        self.records[self.fixture.page_passage_id].data.update(
            artifact_id=LASANCE_1945_PAGE_ARTIFACT, artifact_sha256=page["sha256"],
        )
        self.records[self.fixture.publication_artifact_id].data["derived_from"] = (
            LASANCE_1945_PAGE_ARTIFACT
        )
        self.witnesses = {"lasance-1945": {
            "source_id": LASANCE_1945_EDITION,
            "artifact_id": LASANCE_1945_RIGHTS_ARTIFACT, "rights": "public-domain",
            "caution": "Original expression only; later inserts excluded.",
        }}
        self.assertEqual(self.publication(), [])
        self.assertIsNone(self.reader_publication())
        for date in ("1930", "1946", "1955"):
            with self.subTest(date=date):
                self.records[LASANCE_1945_EDITION].data["date"] = date
                self.assert_rights_rejected()

    def test_witness_alias_and_original_rights_owner_are_exact(self):
        for key, value in (("id", "other"), ("source_id", LASANCE_1945_EDITION),
                           ("artifact_id", LASANCE_1946_PAGE_ARTIFACT),
                           ("rights", "permission"), ("rights_jurisdiction", "elsewhere"),
                           ("caution", "")):
            with self.subTest(key=key):
                witnesses = copy.deepcopy(self.witnesses)
                witnesses[LASANCE_1946_WITNESS][key] = value
                self.assert_rights_rejected(witnesses=witnesses)
        self.assert_rights_rejected(witnesses={})
        entry = copy.deepcopy(self.entry)
        entry["witness"] = "lasance-1945"
        self.assert_rights_rejected(entry=entry)

    def test_alias_fallback_must_still_resolve_the_exact_named_source_row(self):
        witnesses = {LASANCE_1946_EDITION: self.witnesses[LASANCE_1946_WITNESS]}
        self.assertEqual(self.publication(witnesses=witnesses), [])
        self.assertIsNone(self.reader_publication(witnesses=witnesses))
        witnesses = copy.deepcopy(witnesses)
        witnesses[LASANCE_1946_EDITION]["id"] = "other"
        self.assert_rights_rejected(witnesses=witnesses)

    def test_rights_anchor_cannot_be_faked_or_moved_to_the_1946_scan(self):
        rights = self.records[LASANCE_1945_RIGHTS_ARTIFACT].data
        for key, value in (("sha256", "0" * 64), ("edition_id", LASANCE_1946_EDITION),
                           ("rights_status", "unresolved"), ("storage", "remote"),
                           ("rights_jurisdiction", "elsewhere")):
            with self.subTest(key=key):
                old = rights[key]
                rights[key] = value
                self.assert_rights_rejected()
                rights[key] = old

    def test_physical_pdf_identity_and_unresolved_disposition_cannot_drift(self):
        page = self.records[LASANCE_1946_PAGE_ARTIFACT].data
        for key, value in (("sha256", "0" * 64), ("byte_size", 135628124),
                           ("page_count", 1885), ("storage", "tracked"),
                           ("rights_status", "public-domain"), ("indexable", True),
                           ("edition_id", LASANCE_1945_EDITION),
                           ("media_type", "text/plain"), ("artifact_type", "ocr")):
            with self.subTest(key=key):
                old = page[key]
                page[key] = value
                self.assert_rights_rejected()
                page[key] = old

    def test_old_expression_ocr_does_not_masquerade_as_a_1946_derivative(self):
        publication = self.records[self.fixture.publication_artifact_id].data
        for parent in (LASANCE_1945_RIGHTS_ARTIFACT, "artifact.unknown", None):
            with self.subTest(parent=parent):
                publication["derived_from"] = parent
                self.assertIn("registered Lasance1945", "\n".join(self.publication()))
                with self.assertRaisesRegex(ValueError, "not derived from the verification artifact"):
                    self.reader_publication()

    def test_1946_ordinary_locus_and_physical_page_bounds_are_required(self):
        for label in ("445a", "1298a", "1298n", "1302a", "1302d", "1298-1299",
                      "1302-1303", "1885a", "0", "446-445", "unknown"):
            with self.subTest(label=label):
                entry = copy.deepcopy(self.entry)
                entry["printed_page"] = label
                self.assert_rights_rejected(entry)
        for leaves in ([-1, 454], [454, 1884], [True, 454], [455, 454], None):
            with self.subTest(leaves=leaves):
                entry = copy.deepcopy(self.entry)
                entry["ia_leaf_range"] = leaves
                self.assert_rights_rejected(entry)

    def test_existing_body_hash_parent_and_same_edition_checks_remain_live(self):
        entry = copy.deepcopy(self.entry)
        entry["translations"][0]["text"] = "Changed body."
        self.assertIn("does not exactly equal", "\n".join(self.publication(entry)))
        with self.assertRaisesRegex(ValueError, "body differs"):
            self.reader_publication(entry)
        entry = copy.deepcopy(self.entry)
        entry["publication_artifact_sha256"] = "0" * 64
        self.assertIn("does not match", "\n".join(self.publication(entry)))
        with self.assertRaisesRegex(ValueError, "artifact hash is stale"):
            self.reader_publication(entry)
        self.records[self.fixture.publication_passage_id].data["edition_id"] = LASANCE_1945_EDITION
        self.assertIn("same edition", "\n".join(self.publication()))
        with self.assertRaisesRegex(ValueError, "different edition"):
            self.reader_publication()


class SharedLasanceRightsAnchorTests(unittest.TestCase):
    def setUp(self):
        self.fixture = base.RuntimePositiveIdentityTests(
            "test_exact_artifact_source_alias_carries_witness_rights_and_label"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.checker = base.load_checker()
        self.checker.OVERLAY_DIR = self.fixture.inventory
        self.checker.act_history = lambda: ({"editio-typica-1920"}, {}, {"date-bound"}, None)
        self.rows = [
            {"id": "lasance-1945", "source_id": LASANCE_1945_EDITION,
             "label": "Original revised1945 expression"},
            {"id": LASANCE_1946_WITNESS, "source_id": LASANCE_1946_EDITION,
             "label": "Separately identified1946 printing"},
        ]
        for row in self.rows:
            row.update(
                artifact_id=LASANCE_1945_RIGHTS_ARTIFACT, rights="public-domain",
                rights_jurisdiction="United States",
                caution="Original1937/1945 English only; whole scan and later inserts excluded.",
                attests="editio-typica-1920", attests_kind="date-bound",
                attests_basis="Synthetic alias fixture; no body is published.",
            )

    def write(self, rows):
        self.fixture.write_entries([])
        path = self.fixture.inventory / "test-proper-translations-v1.toml"
        with path.open("a") as stream:
            for row in rows:
                stream.write("\n[[sources]]\n")
                for key, value in row.items():
                    stream.write(f"{key} = {json.dumps(value)}\n")

    def checker_problems(self):
        return self.checker.overlay_problems([self.fixture.calendar])[0]

    def test_exact_pair_keeps_old_artifact_alias_in_both_source_orders(self):
        for rows in (self.rows, list(reversed(self.rows))):
            with self.subTest(order=[row["id"] for row in rows]):
                self.write(rows)
                _, _, _, aliases = self.fixture.propers.translation_overlay(
                    "test", self.fixture.calendars
                )
                self.assertEqual(aliases[LASANCE_1945_RIGHTS_ARTIFACT]["id"], "lasance-1945")
                self.assertEqual(aliases[LASANCE_1945_EDITION]["id"], "lasance-1945")
                self.assertEqual(aliases[LASANCE_1946_EDITION]["id"], LASANCE_1946_WITNESS)
                self.assertEqual(self.checker_problems(), [])

    def test_unknown_pairs_and_changed_rights_are_still_duplicate_aliases(self):
        for key, value in (("id", "other-printing"), ("source_id", "edition.other"),
                           ("rights", "permission"), ("rights_jurisdiction", "elsewhere"),
                           ("caution", "")):
            with self.subTest(key=key):
                rows = copy.deepcopy(self.rows)
                rows[1][key] = value
                self.write(rows)
                with self.assertRaisesRegex(ValueError, "duplicate translation source alias"):
                    self.fixture.propers.translation_overlay("test", self.fixture.calendars)
                self.assertIn("duplicate translation source alias", "\n".join(self.checker_problems()))

    def test_duplicate_local_ids_and_edition_aliases_do_not_gain_an_exception(self):
        for key, value in (("id", "lasance-1945"), ("source_id", LASANCE_1945_EDITION)):
            with self.subTest(key=key):
                rows = copy.deepcopy(self.rows)
                rows[1][key] = value
                self.write(rows)
                with self.assertRaisesRegex(ValueError, "duplicate translation source"):
                    self.fixture.propers.translation_overlay("test", self.fixture.calendars)
                self.assertIn("duplicate", "\n".join(self.checker_problems()))


class PrintedPageLabelTests(unittest.TestCase):
    def setUp(self):
        self.fixture = base.PublicationBindingTests(
            "test_valid_dual_binding_keeps_remote_page_proof_separate"
        )
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)
        self.checker = self.fixture.checker
        self.witnesses = {"cummiskey-1861": {
            "source_id": self.fixture.edition_id, "rights": "public-domain",
            "artifact_id": self.fixture.page_artifact_id,
            "caution": "Synthetic page-label test; the scan is not distributed.",
        }}

    def source(self, label, context=None):
        entry = copy.deepcopy(self.fixture.entry)
        entry["printed_page"] = label
        match = numbered_page_match(label)
        if context is None and match is not None:
            first, last = match.groups()
            context = f"printed pp. {first}-{last}" if last else f"printed p. {first}"
        self.fixture.records[self.fixture.page_passage_id].data["context"] = context
        return self.checker.overlay_entry_source_problems("entry", entry, self.witnesses)

    def test_actual_lettered_labels_remain_literal_in_the_verified_locus(self):
        for label in ("1168a", "1230-1230a", "1230d", "1230e", "1230e-1230f", "505-506"):
            with self.subTest(label=label):
                self.assertEqual(self.source(label), [])
        self.assertIn("does not record", "\n".join(self.source("1168a", "printed p. 1168")))

    def test_malformed_or_reversed_labels_are_rejected(self):
        for label in ("1168aa", "1230a-f", "1230a-1230", "1230f-1230a", "1230a–1230f",
                      "12/13", "0", "1230a-1231a-1232a", " 1230a", "1230A", None, 1230):
            with self.subTest(label=label):
                self.assertIn("requires printed_page", "\n".join(self.source(label)))

    def test_excluded_lasance_inserts_are_rights_refusals_not_syntax_errors(self):
        for label in ("1298a", "1298n", "1302a", "1302d", "1298-1299", "1301-1303",
                      "1298-1298a", "1298m-1299"):
            with self.subTest(label=label):
                self.assertIsNotNone(numbered_page_match(label))
                self.assertFalse(approved_lasance_printed_page({
                    "witness": "lasance-1945", "printed_page": label,
                }))
        for label in ("1168a", "1230-1230a", "1230e-1230f", "1298", "1302"):
            with self.subTest(label=label):
                self.assertTrue(approved_lasance_printed_page({
                    "witness": "lasance-1945", "printed_page": label,
                }))


if __name__ == "__main__":
    unittest.main()
