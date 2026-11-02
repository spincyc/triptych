"""Native page extraction separates exact-byte custody, rights and review."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_page_witness as witness
from _papal_sources import write_record


def fixture_pdf(overlay=False) -> bytes:
    """Independent project-created vector/text/image PDF, not a source facsimile."""
    objects = [b"", b"<< /Type /Catalog /Pages 2 0 R >>", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for text, pixels in [(b"MODERN WRAPPER", b"\x00\x00"), (b"SOURCE TWO", b"\x0f\xf0"), (b"SOURCE THREE", b"\xaa\x55")]:
        page, content, image = len(objects), len(objects)+1, len(objects)+2
        kids.append(f"{page} 0 R")
        objects.append((f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 140] /Resources << /Font << /F1 3 0 R >> /XObject << /Im0 {image} 0 R >> >> /Contents {content} 0 R >>").encode())
        stream = b"BT /F1 12 Tf 10 100 Td ("+text+b") Tj ET\nq 80 0 0 20 10 40 cm /Im0 Do Q\n"
        if overlay:
            stream += b"q 0 g 0 0 200 140 re f Q\n"
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode()+stream+b"endstream")
        objects.append(b"<< /Type /XObject /Subtype /Image /Width 8 /Height 2 /ColorSpace /DeviceGray /BitsPerComponent 1 /Decode [1 0] /Length 2 >>\nstream\n"+pixels+b"\nendstream")
    objects[2] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count 3 >>".encode()
    data, offsets = bytearray(b"%PDF-1.4\n"), [0]
    for n, obj in enumerate(objects[1:], 1):
        offsets.append(len(data));data += f"{n} 0 obj\n".encode()+obj+b"\nendobj\n"
    xref = len(data);data += f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode()
    for offset in offsets[1:]:data += f"{offset:010} 00000 n \n".encode()
    return bytes(data)+f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()


@unittest.skipUnless(all(shutil.which(t) for t in ["pdfinfo", "pdfimages", "pdfseparate", "pdfunite", "pdftotext"]), "Poppler commands required")
class WitnessTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/acta_reconstruction/page-witness/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.scratch = self.root / ".scratch/run"
        self.scratch.mkdir(parents=True)
        self.pdf = self.scratch / "whole.pdf"
        payload = fixture_pdf();self.pdf.write_bytes(payload)
        self.edition = self.root / "src/sources/works/test/native/editions/1900"
        write_record(self.edition/"edition.toml", {"schema": 1, "record_type": "edition", "id": "edition.test.native.1900", "work_id": "work.test.native", "title": "Test parent", "language": "la"})
        self.parent_path = self.edition / "artifacts/whole/artifact.toml"
        self.parent = {"schema": 1, "record_type": "artifact", "id": "artifact.test.native.1900.whole", "edition_id": "edition.test.native.1900", "media_type": "application/pdf", "storage": "restricted", "rights_status": "unresolved", "rights_basis": "Whole wrapper not cleared.", "sha256": witness.digest(payload), "byte_size": len(payload), "page_count": 3}
        write_record(self.parent_path, self.parent)
        self.recipe = {"schema": witness.SCHEMA, "revision": "2026-10-26T00:00:00Z", "slug": "selected-history", "title": "Synthetic historical pages", "parent_artifact_id": self.parent["id"], "parent_artifact_path": str(self.parent_path.relative_to(self.root)), "parent_sha256": self.parent["sha256"], "parent_byte_size": len(payload), "edition_id": "edition.test.native.1900", "pages": [2, 3], "rights_status": "licensed", "rights_basis": "Project-authored synthetic fixture; caller licenses only selected test pages.", "rights_jurisdiction": "United States", "extent_note": "Select only synthetic source pages 2 and 3; retain the uncleared whole wrapper separately."}

    def tearDown(self):
        self.temp.cleanup()

    def extract(self, recipe=None):
        return witness.extract_witness(self.root, recipe or self.recipe, self.pdf, self.scratch)

    def register(self, recipe=None):
        return witness.register_witness(self.root, recipe or self.recipe, self.pdf, self.scratch)

    def test_whole_parent_hash_and_size_checked_before_output(self):
        self.pdf.write_bytes(self.pdf.read_bytes()+b"changed")
        with self.assertRaisesRegex(ValueError, "whole cached PDF"):
            self.extract()
        self.assertFalse((self.scratch/self.recipe["slug"]).exists())
        bad = dict(self.recipe, parent_sha256="a"*64)
        with self.assertRaisesRegex(ValueError, "complete canonical parent"):
            self.extract(bad)

    def test_no_rights_or_boundary_inference(self):
        for update in [{"rights_status": "unresolved"}, {"rights_basis": ""}, {"pages": [True]}, {"pages": [3, 2]}, {"pages": [2, 2]}, {"pages": [0]}, {"pages": [4]}, {"edition_id": "edition.test.other"}]:
            with self.subTest(update=update), self.assertRaises(ValueError):
                self.extract(dict(self.recipe, **update))
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 1)

    def test_native_page_text_geometry_and_images_survive_noncontiguous_selection(self):
        result = self.extract(dict(self.recipe, pages=[1, 3]))
        output = result["stage"]/"witness.pdf"
        text = witness.run(["pdftotext", str(output), "-"])
        self.assertIn(b"MODERN WRAPPER", text)
        self.assertIn(b"SOURCE THREE", text)
        self.assertNotIn(b"SOURCE TWO", text)
        self.assertEqual(witness.pdf_information(output)["pages"], 2)
        self.assertEqual([x["source_page"] for x in result["receipt"]["checks"]], [1, 3])
        self.assertTrue(all(len(x["native_images"]["images"]) == 1 for x in result["receipt"]["checks"]))
        self.assertNotIn("verified", result["receipt"])
        self.assertEqual(result["receipt"]["visual_review"], "not performed; use pdf-review separately")

    def test_caller_selected_historical_pages_exclude_wrapper_without_clearing_parent(self):
        result = self.extract()
        text = witness.run(["pdftotext", str(result["stage"]/"witness.pdf"), "-"])
        self.assertNotIn(b"MODERN WRAPPER", text)
        self.assertIn(b"SOURCE TWO", text)
        self.assertEqual(tomllib.loads(self.parent_path.read_text())["storage"], "restricted")

    def test_bilevel_backend_retains_native_bits_and_requires_exact_selector(self):
        selector = {"page": 2, "ordinal": 0, "width": 8, "height": 2, "dpi": 72, "pixel_sha256": witness.digest(b"\x0f\xf0")}
        recipe = dict(self.recipe, pages=[2], method="native-bilevel-images", image_selectors=[selector])
        result = self.extract(recipe)
        self.assertEqual(result["receipt"]["checks"][0]["native_pixel_parity"], "pass")
        self.assertEqual(witness.pdf_information(result["stage"]/"witness.pdf")["pages"], 1)
        bad = copy.deepcopy(recipe);bad["slug"] = "wrong-pixels";bad["image_selectors"][0]["pixel_sha256"] = "a"*64
        with self.assertRaisesRegex(ValueError, "pixel hash"):
            self.extract(bad)

    def test_identical_pdf_under_another_slug_does_not_gain_a_second_owner(self):
        selector = {"page": 2, "ordinal": 0, "width": 8, "height": 2, "dpi": 72, "pixel_sha256": witness.digest(b"\x0f\xf0")}
        recipe = dict(self.recipe, pages=[2], method="native-bilevel-images", image_selectors=[selector])
        self.register(recipe)
        with self.assertRaisesRegex(ValueError, "already has canonical owner"):
            self.register(dict(recipe, slug="duplicate-owner"))
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 4)

    def test_registration_creates_three_same_edition_immutable_artifacts_and_no_passage(self):
        first = self.register()
        self.assertEqual(first["status"], "registered")
        self.assertEqual(len(first["artifact_ids"]), 3)
        self.assertFalse(list(self.root.rglob("passage*.toml")))
        pdf_record = tomllib.loads((self.edition/"artifacts/selected-history/artifact.toml").read_text())
        self.assertEqual(pdf_record["derived_from"], self.parent["id"])
        self.assertEqual(pdf_record["rights_basis"], self.recipe["rights_basis"])
        second = self.register()
        self.assertEqual(second["status"], "reused")
        self.assertEqual(first["receipt"]["output_sha256"], second["receipt"]["output_sha256"])
        with self.assertRaisesRegex(ValueError, "recipe collision"):
            self.register(dict(self.recipe, rights_basis="Different caller assessment; requires a distinct immutable recipe."))

    def test_registered_corruption_is_refused_without_repair_or_overwrite(self):
        self.register()
        path = self.edition/"artifacts/selected-history/witness.pdf"
        damaged = path.read_bytes()+b"damaged";path.write_bytes(damaged)
        with self.assertRaisesRegex(ValueError, "receipt output"):
            self.register()
        self.assertEqual(path.read_bytes(), damaged)

    def test_staged_recipe_change_cannot_relabel_an_old_output(self):
        result = self.extract()
        changed = dict(self.recipe, pages=[1])
        (result["stage"]/"recipe.json").write_bytes(witness.json_bytes(changed))
        before = (result["stage"]/"witness.pdf").read_bytes()
        with self.assertRaisesRegex(ValueError, "receipt does not bind"):
            self.register(changed)
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 1)
        self.assertEqual((result["stage"]/"witness.pdf").read_bytes(), before)

    def test_staged_output_and_self_declared_hash_cannot_import_excluded_wrapper(self):
        good = self.extract()
        other = self.extract(dict(self.recipe, slug="different-selection", pages=[1, 2]))
        wrong = (other["stage"]/"witness.pdf").read_bytes()
        (good["stage"]/"witness.pdf").write_bytes(wrong)
        receipt_path = good["stage"]/"receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt.update(output_sha256=witness.digest(wrong), output_byte_size=len(wrong))
        receipt_path.write_bytes(witness.json_bytes(receipt))
        with self.assertRaisesRegex(ValueError, "parity failed against pinned parent"):
            self.register()
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 1)
        self.assertEqual((good["stage"]/"witness.pdf").read_bytes(), wrong)

    def test_new_registration_never_promotes_a_staged_vector_overlay(self):
        good = self.extract()
        forged_parent = self.scratch/"vector-overlay-parent.pdf"
        forged_parent.write_bytes(fixture_pdf(overlay=True))
        parts = []
        for page in self.recipe["pages"]:
            part = self.scratch/f"overlay-{page}.pdf"
            witness.run(["pdfseparate", "-f", str(page), "-l", str(page), str(forged_parent), str(part)])
            parts.append(part)
        wrong_path = self.scratch/"overlay.pdf"
        witness.run(["pdfunite", *map(str, parts), str(wrong_path)])
        wrong = wrong_path.read_bytes()
        self.assertIn(b"0 0 200 140 re f", wrong)
        (good["stage"]/"witness.pdf").write_bytes(wrong)
        receipt_path = good["stage"]/"receipt.json"
        receipt = json.loads(receipt_path.read_text())
        receipt.update(output_sha256=witness.digest(wrong), output_byte_size=len(wrong))
        receipt_path.write_bytes(witness.json_bytes(receipt))
        registered = self.register()
        final = (self.edition/"artifacts/selected-history/witness.pdf").read_bytes()
        self.assertNotIn(b"0 0 200 140 re f", final)
        self.assertNotEqual(final, wrong)
        self.assertEqual(registered["registration_source"], "fresh-pinned-parent-extraction")
        self.assertEqual(registered["staged_output_sha256"], witness.digest(wrong))
        self.assertEqual((good["stage"]/"witness.pdf").read_bytes(), wrong)

    def test_registered_full_record_contract_is_immutable(self):
        self.register()
        path = self.edition/"artifacts/selected-history/artifact.toml"
        original = path.read_bytes()
        for field, value in [("page_count", 99), ("artifact_type", "different"), ("indexable", True),
                             ("media_type", "text/plain"), ("storage", "restricted")]:
            with self.subTest(field=field):
                record = tomllib.loads(original.decode());record[field] = value
                write_record(path, record)
                changed = path.read_bytes()
                with self.assertRaisesRegex(ValueError, "record contract mismatch"):
                    self.register()
                self.assertEqual(path.read_bytes(), changed)
                path.write_bytes(original)

    def test_failed_parity_does_not_register_or_keep_a_final_staged_witness(self):
        with patch.object(witness, "image_snapshot", side_effect=[{"bad": 1}, {"bad": 2}]), self.assertRaisesRegex(ValueError, "parity failed"):
            self.register()
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 1)
        self.assertFalse((self.scratch/self.recipe["slug"]).exists())

    def test_witness_cli_stages_and_registers_without_papal_index_catalog(self):
        recipe = self.scratch/"input-recipe.json"
        recipe.write_bytes(witness.json_bytes(self.recipe))
        args = [str(ROOT/"tools/papal-sources"), "witness", "--root", str(self.root),
                "--recipe", str(recipe), "--cached-pdf", str(self.pdf), "--scratch", str(self.scratch), "--json"]
        staged = subprocess.run(args, capture_output=True, text=True, check=False)
        self.assertEqual(staged.returncode, 0, staged.stderr)
        self.assertEqual(json.loads(staged.stdout)["status"], "staged")
        self.assertEqual(len(list(self.edition.glob("artifacts/*"))), 1)
        registered = subprocess.run(args+["--register"], capture_output=True, text=True, check=False)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        self.assertEqual(len(json.loads(registered.stdout)["artifact_ids"]), 3)
        self.assertFalse((self.root/"src/sources/papal-documents/catalog.json").exists())


if __name__ == "__main__":
    unittest.main()
