"""Reconcile real, isolated source graphs without accepting or rewriting drift."""
from __future__ import annotations

import copy
from contextlib import redirect_stdout
import io
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/missal-coverage-reconciliation"
LOADER = importlib.machinery.SourceFileLoader("missal_reconciliation_test", str(TOOL))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
REPORT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(REPORT)

WORK = "work.fixture.constituent"
EDITION = "edition.fixture.constituent.1900"
CONTAINER_EDITION = "edition.fixture.container.1900"
ARTIFACT = "artifact.fixture.container.1900.text"
SEGMENT = "segment.fixture.constituent.1900.text"


class CommandHelpTests(unittest.TestCase):
    def test_help_shows_both_real_commands_and_notes_without_audit_or_transcripts(self):
        output = io.StringIO()
        with mock.patch.object(REPORT, "run", side_effect=AssertionError("help ran the audit")), \
                redirect_stdout(output), self.assertRaises(SystemExit) as stopped:
            REPORT.main(["--help"])
        self.assertEqual(0, stopped.exception.code)
        help_text = output.getvalue()
        self.assertIn("examples (real invocations; `make check-examples` replays each one):", help_text)
        examples = REPORT.EXAMPLES[""]
        self.assertEqual([example.command for example in examples],
                         ["tools/missal-coverage-reconciliation", "tools/missal-coverage-reconciliation --json"])
        for example in examples:
            self.assertIn("$ " + example.command, help_text)
            self.assertIn(example.note, help_text)
            self.assertTrue(example.output, "each command must have an actual captured transcript")
            for line in example.output:
                self.assertNotIn(line, help_text)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        scratch = Path(os.environ.get("TMPDIR", ROOT / ".scratch"))
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="missal-reconciliation-", dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        (self.root / "src/gpt").mkdir(parents=True)
        for name in ("container", "constituent"):
            base = f"src/sources/works/fixture/{name}"
            self.toml(base + "/work.toml", {
                "schema": 1, "record_type": "work", "id": f"work.fixture.{name}",
                "title": name, "responsible": "Constructed test fixture",
                "work_type": "test-fixture", "languages": ["en"], "locus_pattern": "line-[0-9]+",
            })
            self.toml(base + "/editions/1900/edition.toml", {
                "schema": 1, "record_type": "edition", "id": f"edition.fixture.{name}.1900",
                "work_id": f"work.fixture.{name}", "title": name, "language": "en",
                "publication": "Constructed fixture", "date": "1900",
            })
        self.artifact_base = "src/sources/works/fixture/container/editions/1900/artifacts/text/"
        body = b"Container introduction.\nConstituent text.\nContainer appendix.\n"
        self.write(self.artifact_base + "text.txt", body)
        self.digest = hashlib.sha256(body).hexdigest()
        self.artifact = {
            "schema": 2, "record_type": "artifact", "id": ARTIFACT,
            "edition_id": CONTAINER_EDITION, "artifact_type": "plain-text", "media_type": "text/plain",
            "storage": "tracked", "rights_status": "public-domain", "rights_basis": "Original test fixture",
            "rights_jurisdiction": "United States", "source_url": "https://example.org/fixture",
            "retrieved": "2026-01-01", "sha256": self.digest, "byte_size": len(body),
            "path": self.artifact_base + "text.txt", "indexable": True, "encoding": "utf-8", "page_count": 3,
        }
        self.toml(self.artifact_base + "artifact.toml", self.artifact)
        self.segment_path = "src/sources/works/fixture/constituent/editions/1900/segments/text.toml"
        self.segment = {
            "schema": 2, "record_type": "segment", "id": SEGMENT, "edition_id": EDITION,
            "artifact_id": ARTIFACT, "artifact_sha256": self.digest, "segment_type": "constituent-work",
            "states": ["cataloged", "acquired"], "context": "Constructed bounded constituent.",
            "physical_line_ranges": [[2, 2]], "artifact_page_ranges": [[2, 2]],
        }
        self.toml(self.segment_path, self.segment)
        self.candidate = {
            "id": "candidate", "source_library_work_id": WORK, "source_library_edition_id": EDITION,
            "source_artifact_ids": [ARTIFACT], "source_segment_ids": [SEGMENT], "source_ids": ["catalogue"],
        }
        self.write(REPORT.history.DEFAULT_SOURCE,
                   'schema_version = 1\nrecord_type = "catholic-eucharistic-history"\nscope_ref = "fixture"\n')
        self.write_inventory()
        self.write(REPORT.INVENTORIES["western"][0], "candidates = []\ncoverage = []\nsources = []\n")
        self.coverage = {
            "schema_version": 1, "record_type": "eucharistic-book-stage-coverage-audit",
            "audit_id": "fixture", "title": "Constructed coverage fixture",
            "inputs": [], "count_semantics": {
                "eastern_census_slots": 1, "western_coverage_trajectories": 0,
                "eastern_candidates": 1, "western_candidates": 0, "presentation_groups": 0,
                "eastern_empty_candidate_slots_at_input": [], "western_empty_candidate_slots_at_input": 0,
            },
            "dossier_snapshot": [], "canonical_traditions": [], "proposed_traditions": [],
            "sources": [], "western_trajectory_coverage": [],
            "eastern_church_coverage": [{
                "id": "church", "candidate_ids": ["candidate"],
                "dossier_coverage": {"status": "unmapped", "text_coverage_counts": {}},
            }],
            "validation": {"coverage_status_counts": {"unmapped": 1}},
        }
        self.refresh_fixture_snapshot()

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())

    def toml(self, relative, fields):
        self.write(relative, self.toml_fields(fields))

    @staticmethod
    def toml_fields(fields):
        return "".join(f"{key} = {json.dumps(value)}\n" for key, value in fields.items())

    def write_inventory(self):
        self.write(REPORT.INVENTORIES["eastern"][0],
                   '[[sources]]\nid = "catalogue"\n[[records]]\n' + self.toml_fields(self.candidate)
                   + '[[church_coverage]]\nid = "church"\ncandidate_ids = ["candidate"]\n')

    def refresh_fixture_snapshot(self):
        # Only fixture setup updates pins. The tool is never allowed to do so.
        self.coverage["inputs"] = [REPORT.history.fingerprint(self.root, self.root / path)
                                   for path in [REPORT.history.DEFAULT_SOURCE,
                                                *(spec[0] for spec in REPORT.INVENTORIES.values())]]
        self.write_coverage()

    def write_coverage(self):
        self.write(REPORT.COVERAGE, json.dumps(self.coverage))

    def codes(self, payload):
        return {row["code"] for row in payload["findings"]}

    def cli(self):
        return subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.root), "--json"],
                              capture_output=True, text=True, check=False,
                              env={**os.environ, "TRIPTYCH_LIBRARY_CACHE": "1"})

    def filesystem_state(self):
        return {path.relative_to(self.root).as_posix():
                (path.stat().st_mtime_ns, path.read_bytes() if path.is_file() else None)
                for path in self.root.rglob("*")}

    def test_cross_work_segment_is_valid_and_unresolved_research_is_not_failure(self):
        result = self.cli()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual("ok", payload["status"])
        self.assertEqual([], payload["findings"])
        self.assertEqual(["church"], payload["research_limits"]["coverage_rows_without_stages"])

    def test_container_requires_an_explicit_matching_segment_on_this_row(self):
        del self.candidate["source_segment_ids"]
        self.write_inventory()
        self.refresh_fixture_snapshot()
        payload = REPORT.run(self.root)
        self.assertEqual({"edition-member-mismatch"}, self.codes(payload))

    def test_same_edition_artifact_needs_no_segment(self):
        self.candidate.update(source_library_work_id="work.fixture.container",
                              source_library_edition_id=CONTAINER_EDITION, source_segment_ids=[])
        self.write_inventory()
        self.refresh_fixture_snapshot()
        self.assertEqual([], REPORT.run(self.root)["findings"])

    def test_segment_for_another_edition_cannot_excuse_wrong_artifact(self):
        self.candidate["source_library_edition_id"] = CONTAINER_EDITION
        self.write_inventory()
        self.refresh_fixture_snapshot()
        payload = REPORT.run(self.root)
        self.assertIn("edition-work-mismatch", self.codes(payload))
        self.assertTrue(any(row["code"] == "edition-member-mismatch"
                            and row["location"].endswith(".source_segment_ids") for row in payload["findings"]))
        # The candidate's edition must match the segment, even when the artifact
        # is a valid container for another constituent elsewhere in the graph.
        self.candidate["source_library_edition_id"] = "edition.fixture.container.other"
        self.toml("src/sources/works/fixture/container/editions/other/edition.toml", {
            "schema": 1, "record_type": "edition", "id": self.candidate["source_library_edition_id"],
            "work_id": "work.fixture.container", "title": "Other edition", "language": "en",
            "publication": "Constructed fixture", "date": "1901",
        })
        self.candidate["source_library_work_id"] = "work.fixture.container"
        self.write_inventory()
        self.refresh_fixture_snapshot()
        payload = REPORT.run(self.root)
        self.assertTrue(any(row["code"] == "edition-member-mismatch"
                            and row["location"].endswith(".source_artifact_ids") for row in payload["findings"]))

    def test_segment_does_not_cover_sibling_or_derivative_artifact(self):
        sibling = copy.deepcopy(self.artifact)
        sibling.update(id="artifact.fixture.container.1900.sibling", storage="remote",
                       source_url="https://example.org/sibling", indexable=False,
                       derived_from=ARTIFACT, transformation="Constructed derivative fixture")
        for key in ("path", "encoding"):
            sibling.pop(key)
        self.toml("src/sources/works/fixture/container/editions/1900/artifacts/sibling/artifact.toml", sibling)
        self.candidate["source_artifact_ids"].append(sibling["id"])
        self.write_inventory()
        self.refresh_fixture_snapshot()
        payload = REPORT.run(self.root)
        self.assertEqual({"edition-member-mismatch"}, self.codes(payload))
        self.assertIn(sibling["id"], payload["findings"][0]["message"])

    def test_owner_rejects_stale_hash_or_out_of_bounds_segment(self):
        for field, value in (("artifact_sha256", "0" * 64), ("artifact_page_ranges", [[2, 4]]),
                             ("physical_line_ranges", [[2, 4]])):
            with self.subTest(field=field):
                changed = {**self.segment, field: value}
                self.toml(self.segment_path, changed)
                payload = REPORT.run(self.root)
                self.assertIn("source-owner-validation", self.codes(payload), payload)
        self.toml(self.segment_path, self.segment)

    def test_container_exception_does_not_reassign_passage_ownership(self):
        passage = "passage.fixture.container.1900.line-2"
        self.toml("src/sources/works/fixture/container/editions/1900/passages/line-2.toml", {
            "schema": 2, "record_type": "passage", "id": passage,
            "edition_id": CONTAINER_EDITION, "artifact_id": ARTIFACT,
            "artifact_sha256": self.digest, "locus": "line-2", "states": ["acquired"],
            "context": "A passage attributed to the container edition.", "physical_line_ranges": [[2, 2]],
        })
        self.candidate["source_library_passage_ids"] = [passage]
        self.write_inventory()
        self.refresh_fixture_snapshot()
        payload = REPORT.run(self.root)
        self.assertEqual({"edition-member-mismatch"}, self.codes(payload))
        self.assertTrue(payload["findings"][0]["location"].endswith(".source_library_passage_ids"))

    def test_unknown_and_wrong_type_canonical_records_remain_invalid(self):
        for segment, expected in (("segment.fixture.missing", "unknown-canonical-record"),
                                  (ARTIFACT, "canonical-type")):
            with self.subTest(segment=segment):
                self.candidate["source_segment_ids"] = [segment]
                self.write_inventory()
                self.refresh_fixture_snapshot()
                payload = REPORT.run(self.root)
                self.assertIn(expected, self.codes(payload))
                self.assertIn("edition-member-mismatch", self.codes(payload))

    def test_stale_coverage_and_unknown_references_fail_without_repair(self):
        self.coverage["count_semantics"]["eastern_candidates"] = 99
        self.coverage["inputs"][0]["sha256"] = "0" * 64
        self.coverage["eastern_church_coverage"][0]["candidate_ids"] = ["missing"]
        self.coverage["eastern_church_coverage"][0]["next_sources"] = {"inventory_source_ids": ["missing"]}
        self.write_coverage()
        before = self.filesystem_state()
        result = self.cli()
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertTrue({"stale-count", "stale-fingerprint", "stale-membership", "unknown-candidate", "unknown-source"}
                        <= self.codes(json.loads(result.stdout)))
        self.assertEqual(before, self.filesystem_state())

    def test_read_only_deterministic_cli_even_when_cache_is_enabled(self):
        before = self.filesystem_state()
        first, second = self.cli(), self.cli()
        self.assertEqual(0, first.returncode, first.stdout + first.stderr)
        self.assertEqual((first.returncode, first.stdout, first.stderr),
                         (second.returncode, second.stdout, second.stderr))
        self.assertEqual(before, self.filesystem_state())
        self.assertFalse((self.root / "build").exists())


if __name__ == "__main__":
    unittest.main()
