"""Source-preservation and refusal cases for explicit note-block replay."""
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_source_notes as notes


class SourceNotesTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get("PAPAL_SOURCE_NOTES_TEST_TMPDIR", ROOT / ".scratch/papal-source-notes-tests"))
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.raw = b"wrapper\nBody begins It\n 1 Source note.\ncontinues here.\nnext wrapper\nClosing.\n"
        (self.root / "source.txt").write_bytes(self.raw)
        self.spec = {"schema": notes.SCHEMA, "source_artifact_id": "artifact.example.source",
                     "source_path": "source.txt", "source_sha256": notes.sha(self.raw),
                     "physical_line_ranges": [[2, 4], [6, 6]], "note_line_ranges": [[3, 3]]}

    def test_source_words_order_and_note_boundaries(self):
        result, report = notes.derive(self.spec, self.root)
        self.assertEqual(result, b"Body begins It\n\n 1 Source note.\n\ncontinues here.\n\nClosing.\n")
        self.assertTrue(report["selected_non_lf_bytes_preserved"])
        self.assertTrue(report["source_order_preserved"])
        self.assertEqual(report["source_note_groups"], 1)

    def test_wrong_source_hash_is_refused(self):
        self.spec["source_sha256"] = "0" * 64
        with self.assertRaisesRegex(notes.SourceNotesError, "source SHA"):
            notes.derive(self.spec, self.root)

    def test_ranges_must_be_exact_and_ordered(self):
        for ranges in ([[2, 4], [4, 6]], [[6, 6], [2, 4]], [[2, 7]], [[True, 4]]):
            with self.subTest(ranges=ranges):
                spec = {**self.spec, "physical_line_ranges": ranges}
                with self.assertRaises(notes.SourceNotesError):
                    notes.derive(spec, self.root)

    def test_note_cannot_cross_a_selection_gap(self):
        self.spec["note_line_ranges"] = [[3, 6]]
        with self.assertRaisesRegex(notes.SourceNotesError, "crosses a gap"):
            notes.derive(self.spec, self.root)

    def test_extra_fields_and_traversal_are_refused(self):
        for spec in ({**self.spec, "repair_words": True}, {**self.spec, "source_path": "../source.txt"}):
            with self.assertRaises(notes.SourceNotesError):
                notes.derive(spec, self.root)

    def test_expected_output_pin_is_checked(self):
        self.spec["expected_sha256"] = "0" * 64
        with self.assertRaisesRegex(notes.SourceNotesError, "derived output"):
            notes.derive(self.spec, self.root)

    def test_present_expected_pin_requires_a_valid_digest(self):
        for expected in (None, "", False, 0, "A" * 64, "0" * 63, [], {}):
            with self.subTest(expected=expected), self.assertRaisesRegex(notes.SourceNotesError, "expected_sha256"):
                notes.derive({**self.spec, "expected_sha256": expected}, self.root)

    def inline_spec(self):
        raw = "wrapper\nBody é. 21 Note α. 22 Note β.\nClosing.\n".encode("utf-8")
        (self.root / "source.txt").write_bytes(raw)
        line = raw.split(b"\n")[1]
        boundaries = []
        for text in (b"21 Note", b"22 Note"):
            offset = line.index(text)
            boundaries.append({"physical_line": 2, "source_line_sha256": notes.sha(line),
                               "byte_offset": offset,
                               "before_utf8": line[:offset].decode("utf-8")[-4:],
                               "after_utf8": line[offset:].decode("utf-8")[:7]})
        return {**self.spec, "source_sha256": notes.sha(raw), "physical_line_ranges": [[2, 3]],
                "note_line_ranges": [], "inline_note_boundaries": boundaries}

    def test_inline_boundaries_preserve_exact_source_bytes_and_order(self):
        spec = self.inline_spec()
        source = (self.root / "source.txt").read_bytes()
        payload, report = notes.derive(spec, self.root)
        self.assertEqual(payload, "Body é. \n\n21 Note α. \n\n22 Note β.\nClosing.\n".encode("utf-8"))
        self.assertEqual((self.root / "source.txt").read_bytes(), source)
        self.assertEqual(report["inline_boundary_count"], 2)
        self.assertEqual(report["source_note_groups"], 2)
        selected = b"\n".join(source.split(b"\n")[1:3]) + b"\n"
        self.assertEqual(payload.replace(b"\n", b""), selected.replace(b"\n", b""))
        self.assertEqual(len(payload), len(selected) + 4)
        spec["expected_sha256"] = notes.sha(payload)
        self.assertEqual(notes.derive(spec, self.root)[0], payload)

    def test_inline_and_whole_line_boundaries_can_be_combined(self):
        spec = self.inline_spec()
        spec["note_line_ranges"] = [[3, 3]]
        payload, report = notes.derive(spec, self.root)
        self.assertTrue(payload.endswith(b"22 Note \xce\xb2.\n\nClosing.\n\n"))
        self.assertEqual(report["source_note_groups"], 3)

    def test_inline_schema_offsets_hashes_and_anchors_are_exact(self):
        original = self.inline_spec()
        line = (self.root / "source.txt").read_bytes().split(b"\n")[1]
        changes = (
            {"physical_line": True}, {"physical_line": 1}, {"physical_line": 99},
            {"byte_offset": True}, {"byte_offset": -1}, {"byte_offset": 0},
            {"byte_offset": len(line)}, {"byte_offset": line.index("é".encode()) + 1},
            {"source_line_sha256": None}, {"source_line_sha256": "0" * 64},
            {"before_utf8": ""}, {"after_utf8": " "}, {"after_utf8": "21\nNote"},
            {"before_utf8": "wrong"}, {"after_utf8": "wrong"}, {"extra": True},
        )
        for change in changes:
            spec = copy.deepcopy(original)
            spec["inline_note_boundaries"][0].update(change)
            with self.subTest(change=change), self.assertRaises(notes.SourceNotesError):
                notes.derive(spec, self.root)
        for value in (None, [], {}, [None], [{}], original["inline_note_boundaries"][::-1],
                      [original["inline_note_boundaries"][0]] * 2):
            spec = {**original, "inline_note_boundaries": value}
            with self.subTest(value=value), self.assertRaises(notes.SourceNotesError):
                notes.derive(spec, self.root)

    def test_inline_rejects_empty_notes_unselected_lines_and_empty_partitions(self):
        spec = self.inline_spec()
        with self.assertRaises(notes.SourceNotesError):
            notes.derive({**spec, "inline_note_boundaries": []}, self.root)
        with self.assertRaises(notes.SourceNotesError):
            notes.derive({**self.spec, "note_line_ranges": []}, self.root)
        with self.assertRaisesRegex(notes.SourceNotesError, "selected extent"):
            notes.derive({**spec, "physical_line_ranges": [[1, 1], [3, 3]]}, self.root)
        raw = b"A   B\n"
        (self.root / "source.txt").write_bytes(raw)
        boundaries = [{"physical_line": 1, "source_line_sha256": notes.sha(raw[:-1]),
                       "byte_offset": offset, "before_utf8": before, "after_utf8": after}
                      for offset, before, after in ((1, "A", "   B"), (4, "A   ", "B"))]
        with self.assertRaisesRegex(notes.SourceNotesError, "whitespace-only partition"):
            notes.derive({**spec, "source_sha256": notes.sha(raw), "physical_line_ranges": [[1, 1]],
                          "inline_note_boundaries": boundaries}, self.root)

    def cli(self, verb, spec=None, target=None, spec_path=None):
        spec_path = spec_path or self.root / "spec.json"
        spec_path.parent.mkdir(parents=True, exist_ok=True)
        spec_path.write_text(json.dumps(spec or self.spec))
        target = target or self.root / ".scratch/out.txt"
        with contextlib.redirect_stdout(io.StringIO()) as output, contextlib.redirect_stderr(io.StringIO()) as error:
            code = notes.main([verb, "--spec", str(spec_path), "--out", str(target),
                               "--root", str(self.root), "--json"])
        return code, output.getvalue(), error.getvalue()

    def test_input_and_spec_aliases_are_refused_in_scratch(self):
        source = self.root / ".scratch/source.txt"
        source.parent.mkdir()
        source.write_bytes(self.raw)
        spec = {**self.spec, "source_path": ".scratch/source.txt"}
        spec_path = self.root / ".scratch/spec.json"
        aliases = [source, spec_path]
        for kind in ("symlink", "hardlink"):
            for name, original in (("source", source), ("spec", spec_path)):
                if not original.exists():
                    original.write_text(json.dumps(spec))
                alias = source.parent / f"{name}-{kind}"
                if kind == "symlink":
                    alias.symlink_to(original)
                else:
                    os.link(original, alias)
                aliases.append(alias)
        for verb in ("derive", "check"):
            for alias in aliases:
                with self.subTest(verb=verb, alias=alias.name):
                    code, out, error = self.cli(verb, spec, alias, spec_path)
                    self.assertEqual(code, 64)
                    self.assertEqual(out, "")
                    self.assertIn("alias", json.loads(error)["error"])
                    self.assertEqual(source.read_bytes(), self.raw)
                    self.assertEqual(json.loads(spec_path.read_text()), spec)

    def test_existing_output_is_immutable_and_exact_replay_is_idempotent(self):
        target = self.root / ".scratch/out.txt"
        self.assertEqual(self.cli("derive", target=target)[0], 0)
        stamp = target.stat().st_mtime_ns
        self.assertEqual(self.cli("derive", target=target)[0], 0)
        self.assertEqual(target.stat().st_mtime_ns, stamp)
        target.write_bytes(b"retained differing bytes")
        for verb, expected in (("derive", 64), ("check", 1)):
            self.assertEqual(self.cli(verb, target=target)[0], expected)
            self.assertEqual(target.read_bytes(), b"retained differing bytes")

    def test_duplicate_json_keys_and_missing_check_never_write(self):
        spec_path = self.root / "spec.json"
        duplicate = json.dumps(self.spec).replace('"schema":', '"schema":"other","schema":', 1)
        spec_path.write_text(duplicate)
        target = self.root / ".scratch/missing/out.txt"
        with contextlib.redirect_stderr(io.StringIO()) as error:
            code = notes.main(["derive", "--spec", str(spec_path), "--out", str(target),
                               "--root", str(self.root), "--json"])
        self.assertEqual(code, 64)
        self.assertIn("duplicate JSON key", json.loads(error.getvalue())["error"])
        self.assertFalse(target.parent.exists())
        code, output, error = self.cli("check", target=target)
        self.assertEqual(code, 1)
        self.assertEqual(error, "")
        self.assertEqual(json.loads(output)["status"], "mismatch")
        self.assertFalse(target.parent.exists())

    def test_derive_check_and_tampered_check(self):
        spec_path = self.root / "spec.json"
        spec_path.write_text(json.dumps(self.spec))
        target = self.root / ".scratch/out.txt"
        args = ["--spec", str(spec_path), "--out", str(target), "--root", str(self.root), "--json"]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(notes.main(["derive", *args]), 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "derived")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(notes.main(["check", *args]), 0)
        target.write_bytes(target.read_bytes().replace(b"Closing", b"Changed"))
        tampered = target.read_bytes()
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(notes.main(["check", *args]), 1)
        self.assertEqual(target.read_bytes(), tampered)

    def test_derive_cannot_overwrite_the_source(self):
        spec_path = self.root / "spec.json"
        spec_path.write_text(json.dumps(self.spec))
        with contextlib.redirect_stderr(io.StringIO()):
            code = notes.main(["derive", "--spec", str(spec_path), "--out", str(self.root / "source.txt"), "--root", str(self.root)])
        self.assertEqual(code, 64)
        self.assertEqual((self.root / "source.txt").read_bytes(), self.raw)


if __name__ == "__main__":
    unittest.main()
