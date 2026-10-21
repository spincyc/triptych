"""Mechanical packet checks use synthetic words and IHDR-only byte streams."""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/chant-page-proof"
loader = SourceFileLoader("chant_page_proof_under_test", str(TOOL))
spec = spec_from_loader(loader.name, loader)
checker = module_from_spec(spec)
loader.exec_module(checker)


def sha(value):
    return hashlib.sha256(value.encode("utf-8") if isinstance(value, str) else value).hexdigest()


class ChantPageProofTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch, prefix="chant-page-proof-test-")
        self.addCleanup(self.temporary.cleanup)
        self.packet = Path(self.temporary.name) / "packet"
        (self.packet / "images").mkdir(parents=True)

    def fixture(self, flat=False):
        # A header stream, not a scan or generated raster. Only the documented
        # PNG signature/IHDR dimension promise is exercised by these bytes.
        image = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR" + struct.pack(">II", 3, 5) + b"\x08\x02\0\0\0" + b"\0\0\0\0"
        (self.packet / "images/cue.png").write_bytes(image)
        body = "Synthetic Ω café cue."
        if flat:
            row = {key: body for key in ("source_body", "target_control_body", "target_proposal")}
            row.update({key + "_sha256": sha(body) for key in list(row)})
            record = {"role": "synthetic", "artifact_page_one_based": 1, "dpi": 200, "crop": None,
                      "command": ["pdftoppm", "-f", "1", "-l", "1", "-r", "200", "-png", "-singlefile", "never-read.pdf", "images/cue"],
                      "exit": 0, "stderr": "", "path": "images/cue.png"}
            self.receipts = [copy.deepcopy(record)]
            entry = {**record, "bytes": len(image), "sha256": sha(image), "width": 3, "height": 5, "actually_viewed": False}
            self.proof = {"schema": "triptych.scratch.checked-chant-word-proof/v1", "rows": [row], "images": [entry]}
        else:
            row = {key: {"checked_text": body, "checked_text_sha256": sha(body)} for key in ("source", "target")}
            row.update(normalized_target_proposal=body, normalized_target_proposal_sha256=sha(body))
            self.proof = {"packet_type": "bounded-source-proof-only", "rows": [row], "images": [
                {"path": "images/cue.png", "sha256": sha(image), "size_bytes": len(image),
                 "dimensions_pixels": [3, 5], "actually_viewed": False}]}
            self.receipts = None
        self.save()

    def save(self):
        files = ["source-proof.json"]
        (self.packet / files[0]).write_text(json.dumps(self.proof, ensure_ascii=False), encoding="utf-8")
        if self.receipts is not None:
            (self.packet / "render.json").write_text(json.dumps(self.receipts), encoding="utf-8")
            files.append("render.json")
        entries = [{"path": name, "size_bytes": (self.packet / name).stat().st_size,
                    "sha256": sha((self.packet / name).read_bytes())} for name in files]
        (self.packet / "MANIFEST.json").write_text(json.dumps({"files": entries}), encoding="utf-8")
        (self.packet / "SHA256SUMS").write_text("".join(e["sha256"] + "  " + e["path"] + "\n" for e in entries), encoding="utf-8")

    def check(self, **kwargs):
        return checker.check_packet(self.packet, **({"manifest": "MANIFEST.json"} | kwargs))

    def reject(self, pattern, **kwargs):
        result = self.check(**kwargs)
        self.assertEqual(result["status"], "fail", result)
        self.assertRegex("; ".join(result["problems"]), pattern)

    def test_nested_packet_reuses_owner_hashes_and_does_not_mutate_files(self):
        self.fixture()
        before = {p: p.read_bytes() for p in self.packet.rglob("*") if p.is_file()}
        with mock.patch.object(checker, "hash_and_size", wraps=checker.hash_and_size) as files, mock.patch.object(checker, "text_sha256", wraps=checker.text_sha256) as bodies:
            result = self.check()
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(result["counts"], {"files": 1, "body_hash_pairs": 3, "images": 1,
                                          "embedded_render_records": 0, "external_render_receipts": 0})
        files.assert_any_call(self.packet / "images/cue.png")
        bodies.assert_any_call("Synthetic Ω café cue.")
        self.assertEqual({p: p.read_bytes() for p in self.packet.rglob("*") if p.is_file()}, before)
        self.assertEqual(result["scope"], "mechanical-only")
        self.assertIn("actually_viewed or other review attestations", result["not_certified"])

    def test_flat_sha_inventory_and_explicit_render_receipt(self):
        self.fixture(flat=True)
        result = self.check(manifest=None, sha256sums="SHA256SUMS", receipts=["render.json"])
        self.assertEqual(result["status"], "pass", result)
        self.assertEqual(result["counts"]["embedded_render_records"], 1)
        self.assertEqual(result["counts"]["external_render_receipts"], 1)
        self.assertFalse((self.packet / "never-read.pdf").exists())

    def test_wrong_file_hash_size_and_empty_inventory_reject(self):
        for field, value, message in [("sha256", "0" * 64, "byte SHA256 mismatch"),
                                       ("size_bytes", 1, "byte size mismatch"),
                                       ("size_bytes", None, "invalid manifest byte size")]:
            with self.subTest(field=field, value=value):
                self.fixture(); path = self.packet / "MANIFEST.json"
                document = json.loads(path.read_text()); document["files"][0][field] = value
                path.write_text(json.dumps(document)); self.reject(message)
        (self.packet / "MANIFEST.json").write_text('{"files": []}')
        self.reject("nonempty files list")

    def test_exact_body_hash_rejects_added_lf_and_unicode_recomposition(self):
        for changed in ["Synthetic Ω café cue.\n", "Synthetic Ω cafe\u0301 cue."]:
            with self.subTest(body=changed):
                self.fixture(); self.proof["rows"][0]["source"]["checked_text"] = changed
                self.save(); self.reject("exact Unicode body SHA256 mismatch")

    def test_image_bytes_sizes_dimensions_and_non_png_reject(self):
        for field, value, message in [("sha256", "0" * 64, "byte SHA256 mismatch"),
                                       ("size_bytes", 1, "byte size mismatch"),
                                       ("dimensions_pixels", [5, 3], "IHDR dimensions mismatch")]:
            with self.subTest(field=field):
                self.fixture(); self.proof["images"][0][field] = value
                self.save(); self.reject(message)
        self.fixture(); image = b"this is not a PNG header"; (self.packet / "images/cue.png").write_bytes(image)
        self.proof["images"][0].update(size_bytes=len(image), sha256=sha(image))
        self.save(); self.reject("missing PNG IHDR")

    def test_failed_render_command_or_inconsistent_receipts_reject_without_execution(self):
        self.fixture(flat=True); self.receipts[0]["exit"] = 1
        self.save(); self.reject("records failure", receipts=["render.json"])
        for change, message in [
            (lambda r: r.update(exit=1), "records failure"),
            (lambda r: r.update(dpi=400), "page/DPI disagrees"),
            (lambda r: r.update(command=["never-execute", "input", "output"]), "unsupported render command"),
            (lambda r: r.update(crop={"x": 0, "y": 0, "width": 3, "height": 5}), "crop disagrees")]:
            with self.subTest(message=message):
                self.fixture(flat=True); change(self.proof["images"][0]); self.save(); self.reject(message)
        self.fixture(flat=True); self.receipts[0]["role"] = "different-owner"
        self.save(); self.reject("disagrees with image record: role", receipts=["render.json"])
        self.fixture(flat=True); self.receipts.append(copy.deepcopy(self.receipts[0]))
        self.save(); self.reject("unknown or duplicated", receipts=["render.json"])

    def test_path_escape_duplicate_and_uninventoried_proof_reject(self):
        for name in ["../source-proof.json", str(self.packet / "source-proof.json")]:
            with self.subTest(path=name):
                self.fixture(); self.reject("relative without parent traversal", proof=name)
        self.fixture(); outside = self.packet.parent / "outside.png"; outside.write_bytes(b"outside")
        (self.packet / "images/escape.png").symlink_to(outside)
        self.proof["images"][0]["path"] = "images/escape.png"; self.save(); self.reject("escapes the packet")
        self.fixture(); self.proof["images"].append(copy.deepcopy(self.proof["images"][0]))
        self.save(); self.reject("duplicate proof image")
        self.fixture(); (self.packet / "MANIFEST.json").write_text(json.dumps({"files": [{"path": "images/cue.png", "size_bytes": 33, "sha256": sha((self.packet / "images/cue.png").read_bytes())}]}))
        self.reject("proof must be covered")

    def test_unknown_layout_and_review_claims_do_not_become_source_certificates(self):
        self.fixture(); self.proof["packet_type"] = "unknown-layout"
        self.save(); self.reject("unsupported source-proof layout")
        self.fixture(); self.proof["rows"][0]["target"] = {"checked_text": "Different synthetic words.", "checked_text_sha256": sha("Different synthetic words.")}
        self.proof["rights"] = "unverified"; self.save()
        self.assertEqual(self.check()["status"], "pass")
        self.assertIn("normalization or lexical equivalence", self.check()["not_certified"])

    def test_cli_json_failure_and_help(self):
        self.fixture()
        good = subprocess.run([sys.executable, "-B", str(TOOL), str(self.packet), "--manifest", "MANIFEST.json", "--json"], capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)["scope"], "mechanical-only")
        bad = subprocess.run([sys.executable, "-B", str(TOOL), str(self.packet), "--manifest", "absent.json", "--json"], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertEqual(json.loads(bad.stdout)["status"], "fail")
        self.assertNotIn("Traceback", bad.stderr)
        helped = subprocess.run([sys.executable, "-B", str(TOOL), "--help"], capture_output=True, text=True)
        self.assertEqual(helped.returncode, 0)
        self.assertIn("No receipt command is executed", helped.stdout)


if __name__ == "__main__":
    unittest.main()
