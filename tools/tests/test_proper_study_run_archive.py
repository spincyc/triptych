"""A terminal run's archive is the engine's bytes, verified, and nothing else.

Drivers of `tpt proper-study` copied each accepted run's results, packets,
seed and interventions into the leaf by hand, with a scratch script re-derived
three times. The archive is evidence a reader is asked to trust, so the tests
here come in three kinds.

Most build a small repository in a temporary directory -- a run directory, a
leaf, and a stand-in launcher that answers `status` and `replay` -- and ask
the tool's own functions what they make of it: what record.md says, and every
refusal. Each refusal also asserts that nothing was written, because the
failure that motivated building the archive aside was a half archive left in
the leaf that the next attempt then refused to overwrite.

The last kind is the one that would catch a real regression. Where this
checkout still holds the run directory of an already-archived run, the tool
archives it again into a scratch directory and the result must equal the
committed archive byte for byte. `build/tpt-runs/` is ignored output, so those
tests skip in a checkout that never ran the workflow, and say so.
"""

from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "proper-study-run-archive"
LOADER = importlib.machinery.SourceFileLoader("triptych_run_archive", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {TOOL}")
ARCHIVER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ARCHIVER
SPEC.loader.exec_module(ARCHIVER)

RUN = "0123456789abcdef"
PROPER = "liturgy/roman-rite/1962/propers/temporal/99-fixture-sunday"
LEAF = f"src/claude/{PROPER}"
CYCLES = "workflows/reviews/fixture/CYCLES.md"

# Committed archives whose run directories a working checkout may still hold.
REPRODUCIBLE = (
    (
        "9c1136f1f8d1241c",
        "src/claude/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost",
        "workflows/reviews/claude-1962-60-production-2026-10-07/CYCLES.md",
    ),
    (
        "a27462e34ec9c09a",
        "src/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost",
        "workflows/reviews/claude-1962-59-production-2026-09-30/CYCLES.md",
    ),
    (
        "0b0f756d95e3ee20",
        "src/claude/liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/"
        "propers/temporal/pc-s54-twenty-eighth-sunday-in-ordinary-time-year-a",
        "workflows/reviews/claude-pc-s54-production-2026-10-08/CYCLES.md",
    ),
)

# The launcher stand-in prints <root>/engine/<verb>.json and exits with the
# status in <root>/engine/<verb>.rc, so a test can make the engine disagree.
STUB = """#!/usr/bin/env python3
import sys
from pathlib import Path
engine = Path(__file__).resolve().parents[1] / "engine"
verb = sys.argv[3]
sys.stdout.write((engine / f"{verb}.json").read_text())
rc = engine / f"{verb}.rc"
raise SystemExit(int(rc.read_text()) if rc.exists() else 0)
"""


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree(directory: Path) -> dict[str, bytes]:
    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


class Fixture(unittest.TestCase):
    """A repository with one terminal run of three stages and its leaf."""

    stages = (("scope-gate", 0, "PASS"), ("research-review", 0, "CHANGES_REQUIRED"),
              ("research-review", 1, "PASS"))
    interventions = 1
    disposition = "ACCEPTED"

    def setUp(self) -> None:
        scratch = ROOT / ".scratch/pc-r-workflow-support/archive/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.scratch = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.scratch.name)
        self.run_dir = self.root / "build" / "tpt-runs" / RUN
        (self.root / LEAF).mkdir(parents=True)
        launcher = self.root / "tools" / "tpt"
        launcher.parent.mkdir(parents=True)
        launcher.write_text(STUB, encoding="utf-8")
        launcher.chmod(0o755)
        self.build()

    def tearDown(self) -> None:
        self.scratch.cleanup()

    def build(self) -> None:
        for sub in ("results", "packets", "interventions"):
            (self.run_dir / sub).mkdir(parents=True, exist_ok=True)
        packets, results = [], []
        for stage, iteration, disposition in self.stages:
            stem = f"{stage}-{iteration:04d}"
            packet = f"PACKET {stem}\n".encode()
            result = json.dumps({"disposition": disposition, "stage": stage}).encode()
            (self.run_dir / "packets" / f"{stem}.txt").write_bytes(packet)
            (self.run_dir / "results" / f"{stem}.json").write_bytes(result)
            packets.append({"stage": stage, "iteration": iteration, "hash": sha(packet),
                            "path": f"build/tpt-runs/{RUN}/packets/{stem}.txt"})
            results.append({"stage": stage, "iteration": iteration, "hash": sha(result),
                            "disposition": disposition,
                            "path": f"build/tpt-runs/{RUN}/results/{stem}.json"})
        for index in range(self.interventions):
            (self.run_dir / "interventions" / f"{index:04d}.json").write_text(
                json.dumps({"text": f"intervention {index}"}), encoding="utf-8")
        bootstrap = b'{"bootstrap": true}\n'
        (self.run_dir / "bootstrap.json").write_bytes(bootstrap)
        self.manifest = {
            "bootstrap": {"path": "bootstrap.json", "sha256": sha(bootstrap), "version": 1},
            "normalized_args": {"proper": PROPER, "provider": "claude"},
            "repo_commit": "f" * 40,
            "run_id": RUN,
            "workflow_digest": "d" * 64,
            "workflow_id": "proper-study",
            "workflow_version": 11,
        }
        self.write_json("manifest.json", self.manifest)
        self.state = {
            "run_id": RUN,
            "disposition": self.disposition,
            "current_stage": self.disposition,
            "document_root": LEAF,
            "packet_hashes": packets,
            "result_hashes": results,
        }
        self.write_json("state.json", self.state)
        engine = self.root / "engine"
        engine.mkdir(exist_ok=True)
        (engine / "status.json").write_text(json.dumps(
            {"run_id": RUN, "disposition": self.disposition}, indent=2) + "\n")
        (engine / "replay.json").write_text(json.dumps(
            {"run_id": RUN, "disposition": self.disposition, "deterministic": None,
             "recorded_file_intact": True}, indent=2) + "\n")

    def write_json(self, name: str, value: dict) -> None:
        (self.run_dir / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    @property
    def leaf_archive(self) -> Path:
        return self.root / LEAF / "evaluations" / "proper-study-results" / RUN

    def archived(self, output: Path | None = None, **options) -> Path:
        dest, _ = ARCHIVER.archive_run(self.root, RUN, CYCLES,
                                       str(output) if output else None, **options)
        return dest

    def refusal(self, *, output: Path | None = None, run: str = RUN,
                cycles: str = CYCLES, **options) -> str:
        before = tree(self.root)
        with self.assertRaises(ARCHIVER.ArchiveError) as raised:
            ARCHIVER.archive_run(self.root, run, cycles, str(output) if output else None, **options)
        self.assertEqual(tree(self.root), before, "a refusal wrote something")
        self.assertEqual(list(self.root.rglob(".*.partial-*")), [])
        return str(raised.exception)

    def retained_result(self, **fields) -> tuple[Path, dict]:
        path = self.run_dir / "results/research-review-0001.json"
        result = json.loads(path.read_text())
        result.update(fields)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        self.state["result_hashes"][-1]["hash"] = sha(path.read_bytes())
        self.write_json("state.json", self.state)
        return path, result


class ArchiveContentTests(Fixture):
    def test_the_leaf_archive_holds_the_engine_bytes_exactly(self) -> None:
        dest = self.archived()
        self.assertEqual(dest, self.leaf_archive)
        held = tree(dest)
        for sub in ("results", "packets", "interventions"):
            for path in (self.run_dir / sub).iterdir():
                name = path.name if sub == "results" else f"{sub}/{path.name}"
                self.assertEqual(held.pop(name), path.read_bytes(), name)
        self.assertEqual(held.pop("seed-bootstrap.json"),
                         (self.run_dir / "bootstrap.json").read_bytes())
        self.assertEqual(held.pop("seed-manifest.json"),
                         (self.run_dir / "manifest.json").read_bytes())
        self.assertEqual(held.pop("terminal-status.json"),
                         (self.root / "engine" / "status.json").read_bytes())
        self.assertEqual(held.pop("terminal-replay.json"),
                         (self.root / "engine" / "replay.json").read_bytes())
        self.assertEqual(sorted(held), ["record.md"], "the archive holds something extra")

    def test_the_record_tabulates_every_result_against_its_packet(self) -> None:
        record = (self.archived() / "record.md").read_text(encoding="utf-8")
        for packet, result in zip(self.state["packet_hashes"], self.state["result_hashes"]):
            row = (f"| {result['stage']} | {result['iteration']} | "
                   f"{result['disposition']} | `{packet['hash']}` | `{result['hash']}` |")
            self.assertIn(row, record)
        self.assertIn(f"account of every cycle is in `{CYCLES}`.", record)
        self.assertIn("Workflow `proper-study`, version 11, digest `" + "d" * 64 + "`.", record)
        self.assertIn(f"Run `{RUN}`; seed commit `{'f' * 40}`. Terminal disposition "
                      "**ACCEPTED**.", record)
        self.assertIn("The run recorded 3 results over 3 packets, all of which are "
                      "preserved verbatim under `packets/`.", record)
        self.assertTrue(record.endswith("which it confirms.\n"))

    def test_one_intervention_is_spoken_of_in_the_singular(self) -> None:
        record = (self.archived() / "record.md").read_text(encoding="utf-8")
        self.assertIn("`interventions/` holds the 1 manual intervention this run "
                      "recorded. It is unencoded workflow debt, not an acceptance.", record)
        self.assertNotIn("interventions this run", record)

    def test_an_output_directory_receives_the_same_archive(self) -> None:
        elsewhere = self.root / "elsewhere"
        dest = self.archived(output=elsewhere)
        self.assertEqual(dest, elsewhere)
        self.assertFalse(self.leaf_archive.exists(), "--output also wrote the leaf")
        self.assertEqual(tree(elsewhere), tree(self.archived()))

    def test_an_empty_output_directory_is_not_an_overwrite(self) -> None:
        empty = self.root / "empty"
        empty.mkdir()
        self.assertIn("record.md", tree(self.archived(output=empty)))


class PublicDerivativeTests(Fixture):
    def test_stale_staging_contents_are_neither_published_nor_removed(self) -> None:
        output = self.root / "public-archive"
        stale = output.parent / f".{output.name}.partial-{os.getpid()}"
        stale.mkdir()
        (stale / "unreviewed.txt").write_text(f"Unreviewed: {self.root.parent}/external/evidence.json\n")
        expected = tree(stale)
        dest = self.archived(output=output, redact_repository_paths=True)
        self.assertEqual(tree(stale), expected)
        self.assertNotIn("unreviewed.txt", tree(dest))
        receipt = json.loads((dest / ARCHIVER.REDACTION_RECEIPT).read_text())
        self.assertEqual(set(tree(dest)), {item["path"] for item in receipt["files"]}
                         | {ARCHIVER.REDACTION_RECEIPT, ARCHIVER.RECORD})

    def test_foreign_staging_symlink_is_neither_followed_nor_removed(self) -> None:
        output = self.root / "public-archive"
        foreign = self.root / "foreign"
        foreign.mkdir()
        (foreign / "keep.txt").write_text("Foreign contents.\n")
        stale = output.parent / f".{output.name}.partial-{os.getpid()}"
        stale.symlink_to(foreign, target_is_directory=True)
        expected = tree(foreign)
        dest = self.archived(output=output, redact_repository_paths=True)
        self.assertTrue(stale.is_symlink())
        self.assertEqual(stale.resolve(), foreign)
        self.assertEqual(tree(foreign), expected)
        self.assertNotIn("keep.txt", tree(dest))

    def test_copy_failure_cleans_only_its_new_staging_and_preserves_empty_destination(self) -> None:
        output = self.root / "public-archive"
        output.mkdir()
        stale = output.parent / f".{output.name}.partial-{os.getpid()}"
        stale.mkdir()
        (stale / "keep.txt").write_text("Foreign contents.\n")
        before, directories = tree(self.root), set(self.root.iterdir())
        with mock.patch.object(Path, "write_bytes", side_effect=OSError("injected copy failure")):
            with self.assertRaisesRegex(OSError, "injected copy failure"):
                self.archived(output=output, redact_repository_paths=True)
        self.assertEqual(tree(self.root), before)
        self.assertEqual(set(self.root.iterdir()), directories)
        self.assertTrue(output.is_dir())
        self.assertEqual(list(output.iterdir()), [])

    def test_only_notes_change_with_complete_hash_receipt_and_immutable_native_run(self) -> None:
        notes = (f"Read {self.root}/.scratch/evidence.json and {self.root}/research/audit.md; "
                 "Revelation 7:2-4, 9-14; https://example.test/source/home/reading.pdf.")
        path, original = self.retained_result(
            notes=notes, summary="The bounded evidence supports the finding.",
            review_inputs={"schema": 5, "sha256": "b" * 64, "paths": ["src/sources/work.toml"]},
            artifact_path="research/evidence.md", findings=[{"id": "F1", "severity": "accepted"}])
        native = tree(self.run_dir)
        original_bytes = path.read_bytes()
        dest = self.archived(redact_repository_paths=True)
        result = json.loads((dest / path.name).read_text())
        self.assertEqual(result, {**original, "notes": notes.replace(str(self.root) + "/", "")})
        self.assertEqual(tree(self.run_dir), native)
        receipt = json.loads((dest / ARCHIVER.REDACTION_RECEIPT).read_text())
        self.assertEqual((receipt["schema"], receipt["policy"], receipt["run_id"]),
                         (1, ARCHIVER.REDACTION_POLICY, RUN))
        row = next(item for item in receipt["files"] if item["path"] == path.name)
        self.assertEqual(row, {"path": path.name, "native_sha256": sha(original_bytes),
                               "archived_sha256": sha((dest / path.name).read_bytes()),
                               "changes": [{"json_pointer": "/notes", "replacements": 2}]})
        original_archive = ARCHIVER.collect(self.root, RUN).files
        for item in receipt["files"]:
            self.assertEqual(item["archived_sha256"], sha((dest / item["path"]).read_bytes()))
            if item["path"] != path.name:
                self.assertEqual(item["native_sha256"], item["archived_sha256"])
                self.assertEqual(item["changes"], [])
                if item["path"] in original_archive:
                    self.assertEqual((dest / item["path"]).read_bytes(), original_archive[item["path"]])
        record = (dest / "record.md").read_text()
        self.assertIn("explicitly declared public derivatives", record)
        self.assertIn(row["native_sha256"], record)
        self.assertIn(row["archived_sha256"], record)
        self.assertIn("Archived result SHA-256", record)
        self.assertFalse(any(str(self.root).encode() in data for data in tree(dest).values()))

    def test_list_notes_record_every_changed_string_pointer_and_preserve_other_entries(self) -> None:
        notes = [f"Read {self.root}/.scratch/first.json.",
                 f"Keep {self.root}/research/second.md and {self.root}/research/third.md.",
                 "Already relative: research/fourth.md; John 1:1/3."]
        path, original = self.retained_result(notes=notes)
        dest = self.archived(redact_repository_paths=True)
        self.assertEqual(json.loads((dest / path.name).read_text()),
                         {**original, "notes": [text.replace(str(self.root) + "/", "") for text in notes]})
        receipt = json.loads((dest / ARCHIVER.REDACTION_RECEIPT).read_text())
        row = next(item for item in receipt["files"] if item["path"] == path.name)
        self.assertEqual(row["changes"], [{"json_pointer": "/notes/0", "replacements": 1},
                                          {"json_pointer": "/notes/1", "replacements": 2}])

    def test_already_relative_notes_and_http_citations_retain_exact_bytes(self) -> None:
        for notes in ("Read research/audit.md; https://example.test/home/source.pdf.",
                      [".scratch/evidence.json", "John 1:1-3; http://example.test/Users/source.pdf"]):
            with self.subTest(notes=notes):
                path, _ = self.retained_result(notes=notes)
                expected = path.read_bytes()
                dest = self.archived(output=self.root / f"relative-{isinstance(notes, list)}",
                                     redact_repository_paths=True)
                self.assertEqual((dest / path.name).read_bytes(), expected)
                receipt = json.loads((dest / ARCHIVER.REDACTION_RECEIPT).read_text())
                self.assertTrue(all(item["native_sha256"] == item["archived_sha256"]
                                    and item["changes"] == [] for item in receipt["files"]))

    def test_derivative_reproduction_is_deterministic_and_leaves_native_state_exact(self) -> None:
        self.retained_result(notes=f"Checked {self.root}/.scratch/evidence.json.")
        before = tree(self.run_dir)
        first = self.archived(output=self.root / "first", redact_repository_paths=True)
        second = self.archived(output=self.root / "second", redact_repository_paths=True)
        self.assertEqual(tree(first), tree(second))
        self.assertEqual(tree(self.run_dir), before)

    def test_packet_placeholder_root_is_a_template_and_its_exact_bytes_are_preserved(self) -> None:
        packet = self.run_dir / "packets/scope-gate-0000.txt"
        expected = b"Write `<document_root>/evaluations/blocking-findings-v1.toml`.\n"
        packet.write_bytes(expected)
        self.state["packet_hashes"][0]["hash"] = sha(expected)
        self.write_json("state.json", self.state)
        dest = self.archived(redact_repository_paths=True)
        self.assertEqual((dest / "packets/scope-gate-0000.txt").read_bytes(), expected)

    def test_default_refuses_private_notes_without_copying_or_rewriting_them(self) -> None:
        self.retained_result(notes=f"Checked {self.root}/.scratch/evidence.json.")
        self.assertIn("private absolute filesystem path", self.refusal())

    def test_unsupported_decision_seal_artifact_and_nested_note_fields_are_never_redacted(self) -> None:
        original = (self.run_dir / "results/research-review-0001.json").read_bytes()
        for field, value in (
            ("summary", f"Checked {self.root}/.scratch/evidence.json"),
            ("artifact_path", f"{self.root}/research/evidence.md"),
            ("review_inputs", {"paths": [f"{self.root}/src/sources/work.toml"]}),
            ("findings", [{"problem": f"Inspect {self.root}/research/evidence.md"}]),
            ("notes", [{"text": f"Inspect {self.root}/research/evidence.md"}]),
        ):
            with self.subTest(field=field):
                (self.run_dir / "results/research-review-0001.json").write_bytes(original)
                self.retained_result(**{field: value})
                self.assertIn("private absolute filesystem path",
                              self.refusal(redact_repository_paths=True))

    def test_other_absolute_paths_and_noncanonical_descendants_refuse(self) -> None:
        for path in (str(self.root.parent / "external/evidence.json"),
                     str(self.root) + "/../external/evidence.json",
                     str(self.root) + "/research//evidence.md", str(self.root)):
            with self.subTest(path=path):
                self.retained_result(notes=f"Inspect {path}")
                self.refusal(redact_repository_paths=True)

    def test_repeated_leading_posix_and_unc_separators_cannot_hide_absolute_paths(self) -> None:
        external = str(self.root.parent / "external/evidence.json").lstrip("/")
        paths = ["/" * count + external for count in (2, 3, 4, 8)]
        paths += ["/" * count + "synthetic-private" for count in (2, 3, 4, 8)]
        paths += ["\\" * count + "fixture-host\\evidence.txt" for count in (2, 3, 4, 8)]
        paths += ["\\" * count + "fixture-host" for count in (2, 3, 4, 8)]
        for path in paths:
            for redact in (False, True):
                with self.subTest(path=path, redact=redact):
                    self.retained_result(notes=f"Inspect {path}")
                    self.assertIn("private absolute filesystem path",
                                  self.refusal(redact_repository_paths=redact))

    def test_source_url_and_template_repeated_separators_remain_exact(self) -> None:
        notes = ("https://example.test///source.pdf and "
                 "<document_root>///evaluations/result.json are source and template references.")
        path, _ = self.retained_result(notes=notes)
        expected = path.read_bytes()
        dest = self.archived(redact_repository_paths=True)
        self.assertEqual((dest / path.name).read_bytes(), expected)

    def test_a_source_url_containing_current_machine_root_is_refused_without_changing_the_citation(self) -> None:
        self.retained_result(notes=f"https://example.test/source?path={self.root}/research/evidence.md")
        self.assertIn("private absolute filesystem path", self.refusal(redact_repository_paths=True))

    def test_packets_interventions_and_terminal_reports_remain_exact_or_refuse(self) -> None:
        packet = self.run_dir / "packets/scope-gate-0000.txt"
        packet.write_text(f"Inspect {self.root}/research/evidence.md\n")
        self.state["packet_hashes"][0]["hash"] = sha(packet.read_bytes())
        self.write_json("state.json", self.state)
        self.assertIn("private absolute filesystem path", self.refusal(redact_repository_paths=True))
        self.build()
        intervention = self.run_dir / "interventions/0000.json"
        intervention.write_text(json.dumps({"text": f"Inspect {self.root}/research/evidence.md"}))
        self.assertIn("private absolute filesystem path", self.refusal(redact_repository_paths=True))
        self.build()
        report = self.root / "engine/status.json"
        data = json.loads(report.read_text())
        data["notes"] = f"Inspect {self.root}/research/evidence.md"
        report.write_text(json.dumps(data))
        self.assertIn("private absolute filesystem path", self.refusal(redact_repository_paths=True))

    def test_derivative_still_verifies_original_hash_before_any_replacement(self) -> None:
        path, _ = self.retained_result(notes=f"Inspect {self.root}/research/evidence.md")
        path.write_bytes(path.read_bytes() + b"\n")
        self.assertIn("result hash mismatch", self.refusal(redact_repository_paths=True))

    def test_privacy_refusal_preserves_an_empty_destination_and_leaves_no_partial_archive(self) -> None:
        self.retained_result(notes=str(self.root.parent / "external/evidence.json"))
        empty = self.root / "empty"
        empty.mkdir()
        self.refusal(output=empty, redact_repository_paths=True)
        self.assertTrue(empty.is_dir())
        self.assertEqual(list(empty.iterdir()), [])


class PluralTests(Fixture):
    interventions = 2

    def test_several_interventions_are_spoken_of_in_the_plural(self) -> None:
        record = (self.archived() / "record.md").read_text(encoding="utf-8")
        self.assertIn("`interventions/` holds the 2 manual interventions this run "
                      "recorded. They are unencoded workflow debt, not acceptances.", record)


class NoInterventionTests(Fixture):
    interventions = 0
    stages = (("scope-gate", 0, "BLOCKED"),)
    disposition = "BLOCKED"

    def test_a_blocked_run_with_no_intervention_says_so(self) -> None:
        dest = self.archived()
        record = (dest / "record.md").read_text(encoding="utf-8")
        self.assertIn("Terminal disposition **BLOCKED**.", record)
        self.assertIn("The run recorded 1 result over 1 packet, which is preserved", record)
        self.assertIn("The run recorded no manual intervention", record)
        self.assertFalse((dest / "interventions").exists())


class RefusalTests(Fixture):
    def test_a_run_that_is_not_terminal_is_refused(self) -> None:
        self.state.update(disposition=None, current_stage="research-review")
        self.write_json("state.json", self.state)
        message = self.refusal()
        self.assertIn("is not terminal", message)
        self.assertIn("'research-review'", message)

    def test_an_existing_archive_is_never_overwritten(self) -> None:
        self.archived()
        self.assertIn("refusing to overwrite", self.refusal())
        occupied = self.root / "occupied"
        occupied.mkdir()
        (occupied / "keep.txt").write_text("mine")
        self.assertIn("refusing to overwrite", self.refusal(output=occupied))

    def test_a_result_that_no_longer_hashes_to_its_record_is_refused(self) -> None:
        (self.run_dir / "results" / "research-review-0001.json").write_text("{}")
        self.assertIn("result hash mismatch", self.refusal())

    def test_a_packet_that_no_longer_hashes_to_its_record_is_refused(self) -> None:
        (self.run_dir / "packets" / "scope-gate-0000.txt").write_text("edited\n")
        self.assertIn("packet hash mismatch", self.refusal())

    def test_a_recorded_path_outside_the_run_is_not_followed(self) -> None:
        self.state["result_hashes"][0]["path"] = "src/elsewhere.json"
        self.write_json("state.json", self.state)
        self.assertIn("recorded outside", self.refusal())

    def test_a_packet_without_a_result_is_refused(self) -> None:
        self.state["result_hashes"].pop()
        self.write_json("state.json", self.state)
        self.assertIn("3 packets but 2 results", self.refusal())

    def test_lane_evidence_is_refused_rather_than_dropped(self) -> None:
        self.state["result_hashes"][0]["lanes"] = [{"lane": "a", "path": "x", "hash": "y"}]
        self.write_json("state.json", self.state)
        self.assertIn("lane evidence", self.refusal())

    def test_a_replay_that_does_not_confirm_integrity_is_refused(self) -> None:
        (self.root / "engine" / "replay.json").write_text(json.dumps(
            {"run_id": RUN, "disposition": "ACCEPTED", "recorded_file_intact": False}))
        self.assertIn("does not confirm", self.refusal())

    def test_an_engine_that_fails_is_refused(self) -> None:
        (self.root / "engine" / "status.rc").write_text("2")
        self.assertIn("exited 2", self.refusal())

    def test_another_workflows_run_is_refused(self) -> None:
        self.manifest["workflow_id"] = "proper"
        self.write_json("manifest.json", self.manifest)
        self.assertIn("proper-study runs only", self.refusal())

    def test_a_missing_leaf_is_not_created(self) -> None:
        (self.root / LEAF).rmdir()
        self.assertIn("does not exist; write the archive elsewhere", self.refusal())

    def test_an_unknown_or_malformed_run_is_refused(self) -> None:
        self.assertIn("no run 0000000000000000", self.refusal(run="0000000000000000"))
        self.assertIn("is not a run id", self.refusal(run=RUN[:8]))
        self.assertIn("is not a run id", self.refusal(run="../../etc"))

    def test_a_machine_path_for_the_cycles_record_is_refused(self) -> None:
        self.assertIn("repository-relative", self.refusal(cycles="/tmp/CYCLES.md"))
        self.assertIn("repository-relative", self.refusal(cycles="../CYCLES.md"))


class ExitStatusTests(Fixture):
    """A driver reads the exit status; the process must give the right one."""

    def run_tool(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(TOOL), "--root", str(self.root), *argv],
            capture_output=True, text=True, cwd=ROOT,
        )

    def test_an_archive_exits_zero_and_names_what_it_wrote(self) -> None:
        result = self.run_tool(RUN, "--cycles", CYCLES)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout,
            f"archived ACCEPTED run {RUN}: 3 results, 3 packets, 1 intervention -> "
            f"{LEAF}/evaluations/proper-study-results/{RUN}\n",
        )

    def test_a_refusal_exits_one_with_the_error_on_stderr(self) -> None:
        self.run_tool(RUN, "--cycles", CYCLES)
        result = self.run_tool(RUN, "--cycles", CYCLES)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr.startswith(ARCHIVER.ERROR), result.stderr)

    def test_the_cycles_record_is_required(self) -> None:
        self.assertEqual(self.run_tool(RUN).returncode, 2)

    def test_explicit_derivative_flag_records_a_public_archive(self) -> None:
        self.retained_result(notes=f"Inspect {self.root}/research/evidence.md")
        result = self.run_tool(RUN, "--cycles", CYCLES, "--redact-repository-paths")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.leaf_archive / ARCHIVER.REDACTION_RECEIPT).is_file())


class ReproductionTests(unittest.TestCase):
    """Archiving an archived run again reproduces the committed archive exactly."""

    def test_every_available_run_reproduces_its_committed_archive(self) -> None:
        reproduced = 0
        for run, leaf, cycles in REPRODUCIBLE:
            committed = ROOT / leaf / "evaluations" / "proper-study-results" / run
            if not (ROOT / "build" / "tpt-runs" / run).is_dir() or not committed.is_dir():
                continue
            with self.subTest(run=run), tempfile.TemporaryDirectory() as scratch:
                dest, _ = ARCHIVER.archive_run(ROOT, run, cycles, str(Path(scratch) / run))
                self.assertEqual(tree(dest), tree(committed))
                reproduced += 1
        if not reproduced:
            self.skipTest("no archived run's directory is held under build/tpt-runs/")


if __name__ == "__main__":
    unittest.main()
