"""Refuse lossy/ambiguous source-unit permutations and preserve body bytes."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _papal_source_order import SourceOrderError, derive


class SourceOrderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="papal-order-test-", dir=ROOT / ".scratch")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = b"  BODY before\nL1  R1\nL2  R2\nBODY after  \n"
        (self.root / "source.txt").write_bytes(self.source)
        self.spec = {
            "schema": "triptych-papal-source-order/v1", "source_artifact_id": "artifact.test.notes",
            "source_path": "source.txt", "source_sha256": hashlib.sha256(self.source).hexdigest(),
            "physical_line_ranges": [[1, 4]],
            "note_groups": [{"id": "notes", "geometry_basis": "Exact two-column native proof.",
                "physical_line_range": [2, 3], "slices": [
                    {"id": "l1", "physical_line": 2, "byte_range": [0, 4]},
                    {"id": "r1", "physical_line": 2, "byte_range": [4, 6]},
                    {"id": "l2", "physical_line": 3, "byte_range": [0, 4]},
                    {"id": "r2", "physical_line": 3, "byte_range": [4, 6]}],
                "order": ["l1", "l2", "r1", "r2"], "block_starts": ["r1"]}]}

    def rejected(self, change):
        spec = copy.deepcopy(self.spec)
        change(spec)
        with self.assertRaises(SourceOrderError):
            derive(spec, self.root)

    def test_exact_slices_and_body_bytes(self):
        output, report = derive(self.spec, self.root)
        self.assertEqual(output, b"  BODY before\n\nL1  \nL2  \n\nR1\nR2\n\nBODY after  \n")
        self.assertEqual(sorted(output.replace(b"\n", b"")), sorted(self.source.replace(b"\n", b"")))
        self.assertEqual(report["note_groups"], 1)
        self.assertEqual((self.root / "source.txt").read_bytes(), self.source)

    def test_gap(self):
        self.rejected(lambda s: s["note_groups"][0]["slices"][0].update(byte_range=[0, 3]))

    def test_overlap(self):
        self.rejected(lambda s: s["note_groups"][0]["slices"][1].update(byte_range=[3, 6]))

    def test_omitted_line(self):
        self.rejected(lambda s: s["note_groups"][0].update(slices=s["note_groups"][0]["slices"][:2], order=["l1", "r1"], block_starts=[]))

    def test_duplicate_slice_or_order(self):
        self.rejected(lambda s: s["note_groups"][0]["slices"][1].update(id="l1"))
        self.rejected(lambda s: s["note_groups"][0].update(order=["l1", "l2", "r1", "r1"]))

    def test_unknown_or_missing_order_units(self):
        self.rejected(lambda s: s["note_groups"][0].update(order=["l1", "l2", "r1"]))
        self.rejected(lambda s: s["note_groups"][0].update(order=["l1", "l2", "r1", "unknown"]))

    def test_utf8_boundary(self):
        raw = self.source.replace(b"L1", "é".encode())
        (self.root / "source.txt").write_bytes(raw)
        self.spec["source_sha256"] = hashlib.sha256(raw).hexdigest()
        self.rejected(lambda s: s["note_groups"][0]["slices"][0].update(byte_range=[0, 1]))

    def test_source_pin_and_expected_output(self):
        self.rejected(lambda s: s.update(source_sha256="0" * 64))
        self.rejected(lambda s: s.update(expected_sha256="0" * 64))

    def test_group_and_selection_coverage(self):
        self.rejected(lambda s: s.update(physical_line_ranges=[[1, 2], [4, 4]]))
        self.rejected(lambda s: s["note_groups"].append(dict(s["note_groups"][0], id="overlap")))
        self.rejected(lambda s: s.update(physical_line_ranges=[[1, 2], [2, 4]]))

    def test_invalid_range_and_fields(self):
        self.rejected(lambda s: s["note_groups"][0]["slices"][0].update(byte_range=[False, 4]))
        self.rejected(lambda s: s["note_groups"][0]["slices"][0].update(byte_range=[0, 999]))
        self.rejected(lambda s: s.update(inferred_columns=True))
        self.rejected(lambda s: s["note_groups"][0].update(geometry_basis=""))

    def test_paths_and_blocks(self):
        self.rejected(lambda s: s.update(source_path="../source.txt"))
        self.rejected(lambda s: s["note_groups"][0].update(block_starts=["missing"]))
        self.rejected(lambda s: s["note_groups"][0].update(block_starts=["r1", "r1"]))

    def call(self, verb, spec, output):
        path = self.root / "spec.json"
        path.write_text(spec if isinstance(spec, str) else json.dumps(spec))
        return subprocess.run([str(ROOT / "tools/papal-source-order"), verb, "--spec", str(path),
            "--out", str(output), "--root", str(self.root), "--json"], capture_output=True, text=True)

    def test_cli_replay_refusal_and_duplicate_keys(self):
        output = self.root / ".scratch/text.txt"
        self.assertEqual(self.call("derive", self.spec, output).returncode, 0)
        self.assertEqual(self.call("check", self.spec, output).returncode, 0)
        retained = self.root / "retained-source.txt"
        retained.write_bytes(output.read_bytes())
        self.assertEqual(self.call("check", self.spec, retained).returncode, 0)
        output.write_text("different")
        self.assertEqual(self.call("derive", self.spec, output).returncode, 1)
        self.assertEqual(output.read_text(), "different")
        self.assertEqual(self.call("derive", self.spec, self.root / "canonical.txt").returncode, 1)
        duplicate = json.dumps(self.spec).replace('"schema":', '"schema":"duplicate","schema":', 1)
        self.assertIn("duplicate JSON key", self.call("derive", duplicate, output).stdout)


if __name__ == "__main__":
    unittest.main()
