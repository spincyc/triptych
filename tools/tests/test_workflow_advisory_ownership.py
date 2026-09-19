#!/usr/bin/env python3
"""An advisory belongs to the stage that raised it, and proper-study says so.

Four defects found by driving the first real Claude `proper-study` production
(run `1e02dc05f2df9940`, the 1962 Seventeenth Sunday after Pentecost), each
repaired here and each pinned by a test.

1. `_outstanding_advisories` read back only to the most recent evaluator
   result of *any* stage and stopped there, so another evaluator's PASS ended
   advisories it had never seen. In that run `study-review` filed three
   advisories against the leaf's prose, the route went up to `research`,
   `research-review` passed, and `author-study` — the one stage that edits the
   files those advisories name — was dispatched with an empty advisory header.
   The rule the function states is per raising stage: an advisory is
   outstanding until the stage that raised it speaks again.

2. The six `proper-study` review schemas admitted only `blocking` and
   `advisory`, while `common/result-format.md`, compiled into every one of
   their packets, documents `accepted` and `escalation` and tells a reviewer
   when to use them. The visual reviewer followed its packet, filed one
   finding as `accepted`, and the engine refused the whole submission. The
   engine's own handling of both severities is generic and schema-driven; only
   these schemas withheld them.

3. `proper` and `proper-finish` declare `review_scope` on their evaluators;
   `proper-study` declared it on none of its six review stages, so every
   re-review was a full cold read of an already accepted document. That is the
   documented cause of a review that does not terminate, and the run shows it:
   `study-review` reached three consecutive purely-novel failing rounds
   against a ceiling of four.

4. The Makefile registered every `.toml` beneath a leaf as a render
   prerequisite of the derived PDFs, including the standing-findings record an
   evaluation stage writes mid-run. Installation therefore retypeset documents
   whose sources had not moved, and the retypeset log — sealed as the run's
   pagination evidence — differs in pdfTeX's clock.
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    PASS,
    WorkflowEngine,
)

STUDY_REVIEW = "study-review"
RESEARCH_REVIEW = "research-review"
REVIEW_STAGES = [
    "research-review", "study-review", "synthesis-review",
    "homily-review", "visual-review", "web-review",
]


def advisory(finding_id: str) -> dict:
    return {
        "id": finding_id, "severity": "advisory", "location": "sections/20.tex",
        "problem": "a defect that does not merit blocking",
        "required_result": "what would resolve it if anyone acted on it",
    }


def blocking(finding_id: str, target: str) -> dict:
    return {
        "id": finding_id, "severity": "blocking", "location": "sections/80.tex",
        "problem": "a defect", "required_result": "repair it",
        "repair_target": target,
    }


def pipeline(name: str) -> dict:
    return json.loads(
        (ROOT / "workflows" / "pipelines" / f"{name}.json")
        .read_text(encoding="utf-8"))


class OutstandingAdvisoryTests(unittest.TestCase):
    """Whose PASS ends whose advisories."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="tpt-advisory-"))
        self.addCleanup(self._cleanup)
        self.engine = WorkflowEngine(self.tmp, ROOT / "workflows")
        self.workflow = self.engine.load_workflow("proper-study")

    def _cleanup(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def record(self, stage: str, iteration: int, disposition: str,
               findings: list) -> dict:
        """Write a result where the engine will look for it, as a run does."""
        import hashlib
        body = {
            "stage": stage, "iteration": iteration,
            "disposition": disposition,
            "summary": "recorded for this test", "findings": findings,
        }
        relative = f"results/{stage}-{iteration:04d}.json"
        path = self.tmp / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(body, indent=2).encode("utf-8")
        path.write_bytes(payload)
        return {
            "stage": stage, "iteration": iteration,
            "disposition": disposition, "path": relative,
            "hash": hashlib.sha256(payload).hexdigest(),
        }

    def outstanding(self, results: list, current: str) -> list[str]:
        state = {"result_hashes": results, "current_stage": current}
        return [
            finding["id"] for finding in self.engine._outstanding_advisories(
                "run", self.workflow, state)
        ]

    def test_an_advisory_survives_another_evaluators_pass(self):
        """The shape that lost three of them on a real run."""
        results = [
            self.record(STUDY_REVIEW, 0, CHANGES_REQUIRED, [
                blocking("STU-002", "research"),
                advisory("STU-003"), advisory("STU-004"), advisory("STU-005"),
            ]),
            self.record(RESEARCH_REVIEW, 4, PASS, []),
        ]
        self.assertEqual(
            self.outstanding(results, "author-study"),
            ["STU-003", "STU-004", "STU-005"],
            "the study's advisories are owed to the stage that edits the "
            "files they name, whatever another evaluator has since said")

    def test_a_stages_own_pass_ends_its_own_advisories(self):
        results = [
            self.record(STUDY_REVIEW, 0, CHANGES_REQUIRED, [
                blocking("STU-001", "study"), advisory("STU-003"),
            ]),
            self.record(STUDY_REVIEW, 1, PASS, []),
        ]
        self.assertEqual(self.outstanding(results, "derive-synthesis"), [],
                         "its own later word is what ends an advisory's life")

    def test_two_evaluators_both_outstanding_are_joined_once_each(self):
        results = [
            self.record(RESEARCH_REVIEW, 0, CHANGES_REQUIRED, [
                blocking("RES-001", "research"), advisory("RES-005"),
            ]),
            self.record(STUDY_REVIEW, 0, CHANGES_REQUIRED, [
                blocking("STU-001", "study"), advisory("STU-003"),
            ]),
        ]
        self.assertEqual(self.outstanding(results, "author-study"),
                         ["RES-005", "STU-003"],
                         "joined in workflow stage order, no duplicates")

    def test_nothing_is_outstanding_before_any_evaluation(self):
        self.assertEqual(self.outstanding([], "research"), [])


class ReviewSeveritiesTests(unittest.TestCase):
    """Every severity the packet documents, the schema admits."""

    def schema(self, stage: str) -> dict:
        return json.loads(
            (ROOT / "workflows" / "schema" / f"proper-study-{stage}.json")
            .read_text(encoding="utf-8"))

    def test_the_review_schemas_admit_accepted_and_escalation(self):
        for stage in REVIEW_STAGES:
            with self.subTest(stage=stage):
                schema = self.schema(stage)
                self.assertEqual(
                    schema["finding_enums"]["severity"],
                    ["blocking", "accepted", "escalation", "advisory"])
                self.assertEqual(schema["accepted_finding_fields"],
                                 ["accepted_because"])
                self.assertEqual(schema["escalation_finding_fields"],
                                 ["escalated_to"])

    def test_a_scoped_review_may_say_why_it_is_raising_this_now(self):
        """`out_of_scope_reason` is demanded of a scoped blocking finding."""
        for stage in REVIEW_STAGES:
            with self.subTest(stage=stage):
                self.assertIn("out_of_scope_reason",
                              self.schema(stage)["optional_finding_fields"])

    def test_the_fragment_that_documents_them_reaches_these_stages(self):
        fragment = (ROOT / "workflows" / "fragments" / "common"
                    / "result-format.md").read_text(encoding="utf-8")
        self.assertIn("\"severity\": \"accepted\"", fragment)
        for stage in pipeline("proper-study")["stages"]:
            if stage["id"] in REVIEW_STAGES:
                self.assertIn("common/result-format.md", stage["fragments"])


class ReviewScopeTests(unittest.TestCase):
    """A later review reads what moved, as the older pipelines already do."""

    def test_every_proper_study_review_scopes_its_re_reads(self):
        stages = {s["id"]: s for s in pipeline("proper-study")["stages"]}
        for stage in REVIEW_STAGES:
            with self.subTest(stage=stage):
                self.assertTrue(stages[stage].get("review_scope"))

    def test_the_older_pipelines_are_unchanged(self):
        for name in ("proper", "proper-finish"):
            scoping = {s["id"] for s in pipeline(name)["stages"]
                       if s.get("review_scope")}
            with self.subTest(pipeline=name):
                self.assertEqual(
                    scoping, {"content-evaluation", "synthesis-evaluation"})

    def test_the_definition_moved_version(self):
        """A changed definition is a new version, not the old one edited."""
        self.assertGreaterEqual(pipeline("proper-study")["version"], 4)


class DerivedSourceRegistrationTests(unittest.TestCase):
    """What a run writes into a leaf is not a render input."""

    LEAF = ("src/claude/liturgy/roman-rite/1962/propers/temporal/"
            "57-seventeenth-after-pentecost")
    DERIVED = ("build/claude/liturgy/roman-rite/1962/propers/temporal/"
               "57-seventeenth-after-pentecost-synthesis.pdf")

    def test_the_standing_findings_record_is_not_a_prerequisite(self):
        record = ROOT / self.LEAF / "evaluations" / "blocking-findings-v1.toml"
        if not record.is_file():
            self.skipTest("this leaf carries no standing-findings record")
        database = subprocess.run(
            ["make", "-p", "-n", "PROVIDER=claude", self.DERIVED],
            cwd=ROOT, capture_output=True, text=True,
            env={**os.environ, "LC_ALL": "C"}, timeout=300).stdout
        self.assertIn(self.LEAF, database, "the leaf's sources are registered")
        self.assertNotIn("blocking-findings-v1.toml", database,
                         "an evaluation's own record must not make a derived "
                         "PDF stale: the retypeset is byte-identical in the "
                         "PDF and not in the log the run sealed")


if __name__ == "__main__":
    unittest.main()
