"""Physical witness delivery must preserve the reviewed source evidence graph."""
from __future__ import annotations

import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_source_library as fixtures
import _eucharistic_history as history
import _eucharistic_texts as texts


SOURCES = fixtures.SOURCE_LIBRARY
STORE = SOURCES._artifact_store
SCAN_ID = "artifact.augustine.de-civitate-dei.npnf-dods.scan"
SCAN_PASSAGE_ID = "passage.augustine.de-civitate-dei.npnf-dods.scan-10-6"
ARTIFACT_DIR = (
    "src/sources/works/augustine/de-civitate-dei/editions/npnf-dods/artifacts/scan"
)
SCAN_PATH = f"{ARTIFACT_DIR}/source.pdf"
SCAN_BYTES = b"%PDF-1.7\nExact facsimile witness.\n%%EOF\n"


class SourceDeliveryTests(unittest.TestCase):
    write = fixtures.SourceLibraryTests.write

    def setUp(self) -> None:
        scratch = fixtures.ROOT / ".scratch/source-resolver"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary_directory = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary_directory.name)
        (self.root / "src/sources").mkdir(parents=True)
        (self.root / "src/gpt").mkdir(parents=True)
        fixtures.SourceLibraryTests.add_valid_vertical_fixture(self)
        self.write(SCAN_PATH, SCAN_BYTES)
        digest = hashlib.sha256(SCAN_BYTES).hexdigest()
        self.write(
            f"{ARTIFACT_DIR}/artifact.toml",
            f'''
            schema = 2
            record_type = "artifact"
            id = "{SCAN_ID}"
            edition_id = "{fixtures.EDITION_ID}"
            artifact_type = "facsimile"
            media_type = "application/pdf"
            storage = "tracked"
            rights_status = "public-domain"
            rights_basis = "Public-domain printing."
            rights_jurisdiction = "United States"
            source_url = "https://example.org/scan.pdf"
            retrieved = "2026-07-22"
            sha256 = "{digest}"
            byte_size = {len(SCAN_BYTES)}
            path = "{SCAN_PATH}"
            page_count = 3
            ''',
        )
        self.write(
            "src/sources/works/augustine/de-civitate-dei/editions/npnf-dods/passages/scan-10-6.toml",
            f'''
            schema = 2
            record_type = "passage"
            id = "{SCAN_PASSAGE_ID}"
            edition_id = "{fixtures.EDITION_ID}"
            artifact_id = "{SCAN_ID}"
            artifact_sha256 = "{digest}"
            locus = "{fixtures.LOCUS}"
            states = ["inspected", "verified"]
            context = "The image witness was inspected."
            artifact_page_ranges = [[1, 2]]
            verified_on = "2026-07-22"
            ''',
        )
        library = SOURCES.load_library(self.root)
        self.assertEqual([], library.errors)
        pin = SOURCES.source_fingerprint(library, SCAN_PASSAGE_ID)
        self.write("src/gpt/history/scan-demo/main.tex", "Scan witness demo\n")
        self.write(
            "src/gpt/history/scan-demo/research/source-bindings.toml",
            f'''
            schema = 2
            record_type = "bindings"
            document = "history/scan-demo"
            [[bindings]]
            source_id = "{SCAN_PASSAGE_ID}"
            role = "direct-witness"
            states = ["inspected", "verified"]
            context = "The facsimile controls the passage."
            source_fingerprint = "{pin}"
            verified_on = "2026-07-22"
            ''',
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def delivery(self, path: str = SCAN_PATH, payload: bytes = SCAN_BYTES,
                 media_type: str = "application/pdf") -> dict:
        archive_buffer = io.BytesIO()
        with tarfile.open(fileobj=archive_buffer, mode="w", format=tarfile.USTAR_FORMAT) as archive:
            member = tarfile.TarInfo(path)
            member.size = len(payload)
            archive.addfile(member, io.BytesIO(payload))
        self.archive_bytes = archive_buffer.getvalue()
        archive_hash = hashlib.sha256(self.archive_bytes).hexdigest()
        index = {
            "schema": STORE.SCHEMA,
            "archives": [{
                "id": archive_hash, "name": "evidence.tar", "sha256": archive_hash,
                "bytes": len(self.archive_bytes), "urls": ["https://example.org/evidence.tar"],
            }],
            "artifacts": [{
                "path": path, "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload), "kind": "source-evidence", "media_type": media_type,
                "archive": archive_hash, "member": path,
            }],
        }
        self.save_index(index)
        return index

    def save_index(self, index: dict) -> None:
        self.write(STORE.INDEX_PATH, json.dumps(index))

    def errors(self, **kwargs) -> str:
        return "\n".join(SOURCES.load_library(self.root, **kwargs).errors)

    def test_externalization_preserves_all_fingerprints_search_and_reverse_uses(self) -> None:
        before = SOURCES.load_library(self.root)
        pins = {key: SOURCES.source_fingerprint(before, key) for key in before.records}
        uses = SOURCES.binding_rows(before, SCAN_ID)
        impact = SOURCES.impact_rows(before, SCAN_ID)
        search = SOURCES.search_rows(before, fixtures.CORPUS_ID, "sacrifice")
        self.delivery()
        (self.root / SCAN_PATH).unlink()
        with patch.object(STORE, "resolve", side_effect=AssertionError("unexpected hydration")), \
                patch.object(STORE, "urlopen", side_effect=AssertionError("unexpected network")):
            after = SOURCES.load_library(self.root)
            self.assertEqual([], after.errors)
            self.assertEqual(pins, {key: SOURCES.source_fingerprint(after, key) for key in after.records})
            self.assertEqual(uses, SOURCES.binding_rows(after, SCAN_ID))
            self.assertEqual(impact, SOURCES.impact_rows(after, SCAN_ID))
            self.assertEqual(search, SOURCES.search_rows(after, fixtures.CORPUS_ID, "sacrifice"))
        self.assertEqual(after, SOURCES._library_from_json(json.loads(json.dumps(SOURCES._library_as_json(after)))))

    def test_metadata_validation_does_not_read_even_present_external_witness(self) -> None:
        self.delivery()
        original_hash = SOURCES._hash_and_size

        def text_only_hash(path):
            self.assertNotEqual(path, self.root / SCAN_PATH)
            return original_hash(path)

        with patch.object(SOURCES, "_hash_and_size", side_effect=text_only_hash), \
                patch.object(STORE, "resolve", side_effect=AssertionError("unexpected resolution")):
            self.assertEqual("", self.errors())
        (self.root / SCAN_PATH).write_bytes(b"tampered witness")
        self.assertEqual("", self.errors())
        self.assertIn("mismatch", self.errors(check_external_bytes=True))

    def test_missing_undeclared_binary_still_fails(self) -> None:
        (self.root / SCAN_PATH).unlink()
        self.assertIn("tracked artifact file does not exist", self.errors())

    def test_external_identity_must_match_hash_size_and_media(self) -> None:
        for field, value in (("sha256", "0" * 64), ("bytes", 1), ("media_type", "image/png")):
            with self.subTest(field=field):
                index = self.delivery()
                index["artifacts"][0][field] = value
                self.save_index(index)
                self.assertIn(f"does not match artifact {field}", self.errors())

    def test_unknown_source_owner_and_malformed_index_fail(self) -> None:
        index = self.delivery()
        entry = index["artifacts"][0]
        entry["path"] = entry["member"] = f"{ARTIFACT_DIR}/unowned.pdf"
        self.save_index(index)
        self.assertIn("external source payload has no artifact owner", self.errors())
        for malformed in ({"schema": "wrong"}, {**index, "typo": True}):
            self.save_index(malformed)
            self.assertIn(STORE.INDEX_PATH, self.errors())

    def test_retained_text_cannot_be_externalized_or_go_missing(self) -> None:
        library = SOURCES.load_library(self.root)
        text_record = library.records[fixtures.ARTIFACT_ID]
        path = text_record.data["path"]
        payload = (self.root / path).read_bytes()
        self.delivery(path, payload, "text/plain")
        (self.root / path).unlink()
        errors = self.errors()
        self.assertIn("searchable text payload must remain in the checkout", errors)
        self.assertIn("tracked artifact file does not exist", errors)

    def test_default_resolver_requires_hydration_and_explicit_fetch_checks_bytes(self) -> None:
        self.delivery()
        (self.root / SCAN_PATH).unlink()
        library = SOURCES.load_library(self.root)
        with patch.object(STORE, "urlopen", side_effect=AssertionError("unexpected network")):
            with self.assertRaisesRegex(SOURCES.SourceLibraryQueryError, "not hydrated"):
                SOURCES.artifact_path(library, SCAN_ID)
            self.assertIn("not hydrated", self.errors(check_external_bytes=True))
        with patch.object(STORE, "urlopen", return_value=io.BytesIO(self.archive_bytes)) as request:
            hydrated = SOURCES.artifact_path(library, SCAN_ID, fetch=True)
            self.assertEqual(SCAN_BYTES, hydrated.read_bytes())
            request.assert_called_once()
        self.assertNotEqual(self.root / SCAN_PATH, hydrated)
        self.assertFalse((self.root / SCAN_PATH).exists())
        self.assertEqual("", self.errors(check_external_bytes=True))
        hydrated.chmod(0o644)
        hydrated.write_bytes(b"tampered cache")
        self.assertEqual("", self.errors())
        self.assertIn("mismatch", self.errors(check_external_bytes=True))

    def test_full_evidence_fetch_batches_archive_hydration(self) -> None:
        self.delivery()
        (self.root / SCAN_PATH).unlink()
        with patch.object(STORE, "urlopen", return_value=io.BytesIO(self.archive_bytes)), \
                patch.object(STORE, "hydrate", wraps=STORE.hydrate) as hydrate:
            self.assertEqual("", self.errors(check_external_bytes=True, fetch=True))
            hydrate.assert_called_once_with(self.root, [SCAN_PATH], fetch=True)

    def test_external_delivery_does_not_bypass_distribution_rights(self) -> None:
        self.delivery()
        manifest = self.root / ARTIFACT_DIR / "artifact.toml"
        manifest.write_text(manifest.read_text().replace(
            'rights_status = "public-domain"', 'rights_status = "restricted"'
        ))
        library = SOURCES.load_library(self.root)
        self.assertIn("affirmative distribution", "\n".join(library.errors))
        with self.assertRaisesRegex(SOURCES.SourceLibraryQueryError, "distribution rights"):
            SOURCES.artifact_path(library, SCAN_ID, fetch=True)
        with patch.object(STORE, "hydrate", side_effect=AssertionError("invalid rights must not fetch")):
            self.assertIn("affirmative distribution", self.errors(check_external_bytes=True, fetch=True))

    def test_full_evidence_also_checks_external_parent_embedded_references(self) -> None:
        self.delivery()
        manifest = self.root / ARTIFACT_DIR / "artifact.toml"
        with manifest.open("a") as output:
            output.write(
                '\nsupport_artifacts = [{ artifact_id = "' + fixtures.ARTIFACT_ID
                + '", embedded_reference = "city-of-god.txt" }]\n'
            )
        self.assertEqual("", self.errors(check_binding_fingerprints=False))
        self.assertIn("does not occur in the exact parent artifact", self.errors(
            check_binding_fingerprints=False, check_external_bytes=True
        ))

    def test_fetch_is_only_accepted_for_explicit_evidence_audit(self) -> None:
        with self.assertRaisesRegex(ValueError, "check_external_bytes"):
            SOURCES.load_library(self.root, fetch=True)
        result = fixtures.SourceLibraryTests.run_cli(self, "validate", "--fetch")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("--fetch requires --full-evidence", result.stderr)

    def test_retired_projection_receipts_have_no_owner(self) -> None:
        # The browser-product descriptor is the one freshness proof for these
        # projections; a reintroduced receipt is unowned source-tree data.
        for name in ("source-reader", "act-history"):
            with self.subTest(name=name):
                path = f"src/sources/inventories/{name}-projection-receipt-v1.json"
                self.write(path, "{}")
                self.assertIn("outside the source-library schema", self.errors())
                (self.root / path).unlink()

    def test_receipt_name_is_not_a_general_json_exemption(self) -> None:
        self.write("src/sources/inventories/unowned-receipt.json", "{}")
        self.assertIn("outside the source-library schema", self.errors())

    def text_derived_from_scan(self) -> None:
        manifest = self.root / SOURCES.load_library(self.root).records[fixtures.ARTIFACT_ID].path
        with manifest.open("a") as output:
            output.write(f'\nderived_from = "{SCAN_ID}"\ntransformation = "Synthetic transcription fixture."\n')

    def test_text_projection_uses_absent_binary_parent_identity_without_reading_it(self) -> None:
        self.text_derived_from_scan()
        self.delivery()
        (self.root / SCAN_PATH).unlink()
        with patch.object(STORE, "resolve", side_effect=AssertionError("ancestor bytes not needed")), \
                patch.object(STORE, "urlopen", side_effect=AssertionError("no network")):
            sources = texts._Sources(self.root, texts._load_library(self.root))
            passage = sources.use(fixtures.PASSAGE_ID)
            sources.verify_projection(passage, "The City offers Sacrifice.")
            self.assertEqual({
                "path": SCAN_PATH, "sha256": hashlib.sha256(SCAN_BYTES).hexdigest(),
                "byte_size": len(SCAN_BYTES),
            }, sources.inputs[SCAN_PATH])
            self.assertIn(STORE.INDEX_PATH, sources.inputs)
            payload = {
                "inputs": list(sources.inputs.values()),
                "units": [{
                    "unit_id": "unit.fixture.text", "text": "The City offers Sacrifice.",
                    "text_sha256": hashlib.sha256(b"The City offers Sacrifice.").hexdigest(),
                    "publication": {"status": "permitted", "surfaces": ["public-git"]},
                }],
            }
            history.verify_adapter(payload, self.root)
        with self.assertRaisesRegex(texts.AdapterError, "not cached"):
            sources.payload(sources.records[SCAN_ID])
        with patch.object(STORE, "urlopen", return_value=io.BytesIO(self.archive_bytes)):
            self.assertEqual(SCAN_BYTES, sources.payload(sources.records[SCAN_ID], fetch=True))
        self.assertNotIn(".scratch", "\n".join(sources.inputs))

    def test_text_projection_still_requires_matching_parent_delivery_and_retained_text(self) -> None:
        self.text_derived_from_scan()
        (self.root / SCAN_PATH).unlink()
        with self.assertRaisesRegex(texts.AdapterError, "tracked artifact file does not exist"):
            texts._load_library(self.root)
        index = self.delivery()
        index["artifacts"][0]["sha256"] = "0" * 64
        self.save_index(index)
        with self.assertRaisesRegex(texts.AdapterError, "does not match artifact sha256"):
            texts._load_library(self.root)
        with self.assertRaisesRegex(history.HistoryError, "does not match artifact sha256"):
            history.fingerprint(self.root, self.root / SCAN_PATH)
        self.delivery()
        text = SOURCES.load_library(self.root, check_binding_fingerprints=False).records[fixtures.ARTIFACT_ID]
        (self.root / text.data["path"]).unlink()
        with self.assertRaisesRegex(texts.AdapterError, "tracked artifact file does not exist"):
            texts._load_library(self.root)


if __name__ == "__main__":
    unittest.main()
