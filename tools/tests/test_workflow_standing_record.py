#!/usr/bin/env python3
"""The leaf's standing record holds every stage that spoke, not the last one.

`content-evaluation` and `synthesis-evaluation` both declare
`records_standing_findings`, in both propers pipelines, and a synthesis
evaluation runs only after the content evaluation has passed. The record was
rewritten whole from the one result being recorded, so every run that reached
`derive-synthesis` -- that is, every run that succeeds -- deleted the content
evaluation's observations, accepted findings and advisories from the tracked
record and replaced them with the synthesis evaluation's. Only escalations
survived, and only because they are written from the run's whole ledger rather
than from a result.

It cost a real one. The `proper-finish` run over
`55-fifteenth-after-pentecost` recorded advisory CON-EVI-002, a defect in
`research/scope.md` that was correctly left unrepaired because no
`proper-finish` stage may write that file. The synthesis evaluation then
rewrote the record, and that advisory now stands nowhere in the tree, while
the leaves whose last recorded stage is `content-evaluation` still carry their
content-lane entries.

`OPERATOR.md` records the same failure at v25: every evaluator used to write
this path, and a `web-evaluation` asking for changes replaced the leaf's
content findings with findings about generated HTML. The answer then was to
declare the write per stage, and v26 and v28 recreated the loss by giving a
second stage the declaration.

These tests hold the answer that does not depend on how many stages declare
it. The record is merged per stage: an entry names the stage that raised it, a
write replaces only the recording stage's own entries, and `[[stages]]` says
what each stage last said about this leaf.
"""
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    ACCEPTED_SEVERITY,
    CHANGES_REQUIRED,
    PASS,
    STANDING_FINDINGS_PATH,
    WorkflowEngine,
    _standing_findings,
)

CONTENT = "content-evaluation"
SYNTHESIS = "synthesis-evaluation"
PROVIDER = "claude"
LEAF = "liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost"
DOCUMENT_ROOT = f"src/{PROVIDER}/{LEAF}"

# The schema this file is about. 4 is the merged record; 1, 2 and 3 were each
# rewritten whole by one stage, and leaves in the tree carry all three.
SCHEMA = 4


def finding(finding_id: str, severity: str, **extra) -> dict:
    """One finding of any severity, with the fields its severity carries."""
    entry = {
        "id": finding_id,
        "lane": "evidence-discipline",
        "severity": severity,
        "location": f"sections/30-commentary.tex, the {finding_id} locus",
        "problem": f"{finding_id} states more than its sources support",
        "required_result": f"{finding_id} is repaired or withdrawn",
    }
    entry.update(extra)
    return entry


def blocking(finding_id: str, **extra) -> dict:
    return finding(finding_id, "blocking", repair_target="authoring",
                   **extra)


def accepted(finding_id: str, **extra) -> dict:
    return finding(finding_id, ACCEPTED_SEVERITY,
                   accepted_because="costs more than the defect", **extra)


def advisory(finding_id: str, **extra) -> dict:
    return finding(finding_id, "advisory", **extra)


def observation(note: str, location: str = "research/scope.md l. 17") -> dict:
    return {"lane": "evidence-discipline", "location": location, "note": note}


class StandingRecordCase(unittest.TestCase):
    """Records against one leaf, through the engine's own write path.

    The write is exercised directly rather than by driving a pipeline, for the
    same reason `TheRecordCannotLeaveItsRootTests` does: what is under test is
    the record, and a run that reaches two evaluators costs two dozen advances
    and binds the test to routing it is not about. The stage ids are the real
    ones, so the shape the test holds is the shape the pipelines produce.
    """

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.engine.standing_findings_root = self.root
        self.workflow = {
            "id": "proper-finish", "version": 6,
            "document_root": "src/{provider}/{proper}", "stages": [],
        }
        self.path = self.root / DOCUMENT_ROOT / STANDING_FINDINGS_PATH

    def record(
        self, stage_id: str, findings=(), observations=(),
        disposition: str = CHANGES_REQUIRED, iteration: int = 0,
        escalations=(), run_id: str = "05f2d2fd7c2cf8b3",
    ) -> None:
        """One evaluation result of `stage_id`, recorded as a run would."""
        self.engine._record_standing_findings(
            self.workflow,
            {
                "run_id": run_id,
                "normalized_args": {"provider": PROVIDER, "proper": LEAF},
                "escalations": list(escalations),
            },
            {"id": stage_id, "type": "evaluator",
             "records_standing_findings": True},
            {"disposition": disposition, "iteration": iteration,
             "findings": list(findings), "observations": list(observations)},
        )

    def read(self) -> dict:
        self.assertTrue(self.path.is_file(), f"no record at {self.path}")
        return tomllib.loads(self.path.read_text(encoding="utf-8"))

    def seed(self, text: str) -> None:
        """A record an older schema left in the tree."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(text, encoding="utf-8")

    def ids(self, data: dict, table: str, stage_id: str) -> list[str]:
        return [entry["id"] for entry in data.get(table, [])
                if entry.get("stage") == stage_id]

    def notes(self, data: dict, stage_id: str) -> list[str]:
        return [entry["note"] for entry in data.get("observations", [])
                if entry.get("stage") == stage_id]

    def headers(self, data: dict) -> dict:
        return {entry["stage"]: entry for entry in data.get("stages", [])}

    def the_content_evaluation_speaks(self) -> None:
        """The shape of the run that lost CON-EVI-002."""
        self.record(CONTENT, findings=[
            blocking("CON-CIT-003"),
            accepted("CON-PRO-011"),
            advisory("CON-EVI-002",
                     location="research/scope.md ll. 88-90"),
        ], observations=[observation("the colophon's own arithmetic")])


class TheSecondEvaluatorDoesNotEraseTheFirstTests(StandingRecordCase):
    """The regression this file exists for."""

    def test_a_synthesis_evaluation_keeps_what_content_recorded(self):
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[
            advisory("SYN-FID-004"), accepted("SYN-CON-009"),
        ], observations=[observation("unit 1 inverts its referent",
                                     "sections/synthesis/20-integrated.tex")],
            disposition=PASS, iteration=3)
        data = self.read()
        self.assertEqual(self.ids(data, "advisories", CONTENT),
                         ["CON-EVI-002"],
                         "the advisory the synthesis evaluation deleted")
        self.assertEqual(self.ids(data, "accepted", CONTENT),
                         ["CON-PRO-011"])
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-003"])
        self.assertEqual(self.notes(data, CONTENT),
                         ["the colophon's own arithmetic"])
        self.assertEqual(self.ids(data, "advisories", SYNTHESIS),
                         ["SYN-FID-004"])
        self.assertEqual(self.ids(data, "accepted", SYNTHESIS),
                         ["SYN-CON-009"])

    def test_every_entry_names_the_stage_that_raised_it(self):
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[blocking("SYN-FID-004")],
                    observations=[observation("a note")], disposition=PASS)
        data = self.read()
        for table in ("findings", "accepted", "advisories", "observations"):
            for entry in data.get(table, []):
                with self.subTest(table=table, entry=entry.get("id")):
                    self.assertIn(entry.get("stage"), (CONTENT, SYNTHESIS),
                                  "an entry nobody owns cannot be replaced "
                                  "or believed")

    def test_the_stage_headers_say_what_each_stage_last_said(self):
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[], disposition=PASS, iteration=3)
        headers = self.headers(self.read())
        self.assertEqual(sorted(headers), [CONTENT, SYNTHESIS])
        self.assertEqual(headers[CONTENT]["disposition"], CHANGES_REQUIRED)
        self.assertEqual(headers[CONTENT]["iteration"], 0)
        self.assertEqual(headers[CONTENT]["standing"], 1)
        self.assertEqual(headers[CONTENT]["advisory_count"], 1)
        self.assertEqual(headers[CONTENT]["accepted_count"], 1)
        self.assertEqual(headers[CONTENT]["observation_count"], 1)
        self.assertEqual(headers[SYNTHESIS]["disposition"], PASS)
        self.assertEqual(headers[SYNTHESIS]["iteration"], 3)
        self.assertEqual(headers[SYNTHESIS]["standing"], 0)

    def test_the_record_still_states_what_it_is_and_which_schema(self):
        self.the_content_evaluation_speaks()
        data = self.read()
        self.assertEqual(data["standing_findings_schema"], SCHEMA)
        self.assertEqual(data["record_type"], "standing-blocking-findings")
        self.assertEqual(data["document"], LEAF)
        self.assertEqual(data["provider"], PROVIDER)
        self.assertTrue(
            self.path.read_text(encoding="utf-8").startswith("#"),
            "the file opens by saying what it is, for the person reading it")

    def test_the_totals_count_every_stage(self):
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[blocking("SYN-FID-004"),
                                        advisory("SYN-FID-005")])
        data = self.read()
        self.assertEqual(data["standing"], 2)
        self.assertEqual(data["advisory_count"], 2)
        self.assertEqual(data["accepted_count"], 1)


class AStageReplacesItsOwnEntriesAndNoOthersTests(StandingRecordCase):
    """Merging must not turn the record into a history of everything."""

    def test_a_re_evaluation_supersedes_that_stage_s_earlier_entries(self):
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[advisory("SYN-FID-004")])
        self.record(CONTENT, findings=[blocking("CON-CIT-021")], iteration=1)
        data = self.read()
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-021"],
                         "the repaired finding is gone, not appended to")
        self.assertEqual(self.ids(data, "advisories", CONTENT), [],
                         "and so are the advisories it no longer raises")
        self.assertEqual(self.notes(data, CONTENT), [])
        self.assertEqual(self.ids(data, "advisories", SYNTHESIS),
                         ["SYN-FID-004"],
                         "the other stage's word is not this stage's to spend")

    def test_a_pass_records_an_empty_list_for_its_own_stage_alone(self):
        """"Evaluated, nothing stands" and "nobody has looked", per stage."""
        self.the_content_evaluation_speaks()
        self.record(SYNTHESIS, findings=[], observations=[],
                    disposition=PASS, iteration=2)
        data = self.read()
        headers = self.headers(data)
        self.assertIn(SYNTHESIS, headers,
                      "a stage that looked and found nothing says so")
        self.assertEqual(headers[SYNTHESIS]["standing"], 0)
        self.assertEqual(self.ids(data, "findings", SYNTHESIS), [])
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-003"],
                         "a pass by one stage is not a pass by another")

    def test_the_same_finding_twice_from_one_stage_is_one_entry(self):
        self.record(CONTENT, findings=[blocking("CON-CIT-003"),
                                       blocking("CON-CIT-003")])
        self.assertEqual(self.ids(self.read(), "findings", CONTENT),
                         ["CON-CIT-003"])

    def test_two_stages_may_hold_the_same_finding_id(self):
        """The key is `(stage, id)`: lanes cannot coordinate their ids."""
        self.record(CONTENT, findings=[blocking("EVAL-001")])
        self.record(SYNTHESIS, findings=[blocking("EVAL-001")])
        data = self.read()
        self.assertEqual(self.ids(data, "findings", CONTENT), ["EVAL-001"])
        self.assertEqual(self.ids(data, "findings", SYNTHESIS), ["EVAL-001"])

    def test_an_observation_is_held_by_stage_location_and_note(self):
        same = observation("the same sighting",
                           "generation-metadata.tex l. 22")
        self.record(CONTENT, observations=[same, same,
                                           observation("another", "l. 24")])
        self.record(SYNTHESIS, observations=[same])
        data = self.read()
        self.assertEqual(self.notes(data, CONTENT),
                         ["the same sighting", "another"])
        self.assertEqual(self.notes(data, SYNTHESIS), ["the same sighting"])

    def test_recording_the_same_result_twice_writes_the_same_bytes(self):
        self.the_content_evaluation_speaks()
        first = self.path.read_bytes()
        self.the_content_evaluation_speaks()
        self.assertEqual(self.path.read_bytes(), first)


class AnOlderRecordIsUpgradedRatherThanDroppedTests(StandingRecordCase):
    """Leaves in the tree carry schema 1, 2 and 3 right now.

    Each was rewritten whole by one stage and names it in a top-level `stage`,
    so every entry in it belongs to that stage and is kept under it. The one
    thing that is not kept is a file that does not parse: a record this engine
    cannot read is one it must not guess at, which is the rule
    `_standing_findings` already follows.
    """

    SCHEMA_ONE = (
        "# Blocking findings standing against this publication.\n"
        "standing_findings_schema = 1\n"
        'record_type = "standing-blocking-findings"\n'
        f'document = "{LEAF}"\n'
        f'provider = "{PROVIDER}"\n'
        'run_id = "45f0ddc21d634d9a"\n'
        'workflow = "proper-finish"\n'
        "workflow_version = 4\n"
        f'stage = "{CONTENT}"\n'
        "iteration = 3\n"
        'disposition = "CHANGES_REQUIRED"\n'
        "standing = 1\n"
        "\n"
        "[[findings]]\n"
        'id = "CON-CIT-107"\n'
        'lane = "citation-integrity"\n'
        'severity = "blocking"\n'
        'location = "sections/99-references.tex l. 47"\n'
        'problem = "nine sentences locate material the edition lacks"\n'
        'required_result = "every locator is true of both editions"\n'
        'repair_target = "authoring"\n'
        "\n"
        "[[observations]]\n"
        'lane = "profile-conformance"\n'
        'location = "research/scope.md l. 17"\n'
        'note = "the profile states its macro-order twice"\n'
    )

    def test_a_schema_one_record_is_kept_under_the_stage_it_names(self):
        self.seed(self.SCHEMA_ONE)
        self.record(SYNTHESIS, findings=[advisory("SYN-FID-004")],
                    disposition=PASS)
        data = self.read()
        self.assertEqual(data["standing_findings_schema"], SCHEMA)
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-107"],
                         "the older file's own stage keeps its findings")
        self.assertEqual(self.notes(data, CONTENT),
                         ["the profile states its macro-order twice"])
        self.assertEqual(self.ids(data, "advisories", SYNTHESIS),
                         ["SYN-FID-004"])
        headers = self.headers(data)
        self.assertEqual(headers[CONTENT]["iteration"], 3,
                         "the older header is carried into the array")
        self.assertEqual(headers[CONTENT]["disposition"], "CHANGES_REQUIRED")
        self.assertEqual(headers[CONTENT]["run_id"], "45f0ddc21d634d9a")

    def test_the_stage_that_wrote_the_older_file_still_supersedes_it(self):
        self.seed(self.SCHEMA_ONE)
        self.record(CONTENT, findings=[blocking("CON-CIT-021")], iteration=4)
        data = self.read()
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-021"])
        self.assertEqual(self.notes(data, CONTENT), [])

    def test_a_schema_three_record_keeps_its_verdicts_and_escalations(self):
        self.seed(
            "standing_findings_schema = 3\n"
            f'stage = "{CONTENT}"\n'
            "iteration = 2\n"
            'disposition = "PASS"\n'
            "\n"
            "[[accepted]]\n"
            'id = "CON-PRO-011"\n'
            'severity = "accepted"\n'
            'accepted_because = "settled terminal apparatus"\n'
            "\n"
            "[[advisories]]\n"
            'id = "CON-EVI-002"\n'
            'severity = "advisory"\n'
            'location = "research/scope.md ll. 88-90"\n'
            "\n"
            "[[escalations]]\n"
            f'stage = "{CONTENT}"\n'
            "iteration = 2\n"
            'id = "CON-PRO-004"\n'
            'escalated_to = "guidance/liturgy/roman-1962-propers.md"\n'
        )
        self.record(SYNTHESIS, findings=[], disposition=PASS)
        data = self.read()
        self.assertEqual(self.ids(data, "accepted", CONTENT),
                         ["CON-PRO-011"])
        self.assertEqual(data["accepted"][0]["accepted_because"],
                         "settled terminal apparatus")
        self.assertEqual(self.ids(data, "advisories", CONTENT),
                         ["CON-EVI-002"],
                         "the advisory this whole file is about")

    def test_an_entry_in_a_file_that_names_no_stage_is_still_kept(self):
        self.seed(
            "standing_findings_schema = 1\n"
            "\n[[findings]]\n"
            'id = "CON-CIT-107"\n'
            'severity = "blocking"\n'
        )
        self.record(SYNTHESIS, findings=[], disposition=PASS)
        data = self.read()
        orphans = [entry for entry in data["findings"]
                   if entry["stage"] not in (CONTENT, SYNTHESIS)]
        self.assertEqual([entry["id"] for entry in orphans], ["CON-CIT-107"])
        self.assertIn(orphans[0]["stage"], self.headers(data),
                      "whatever it is attributed to, the array declares it")

    def test_a_record_that_does_not_parse_is_replaced_not_guessed_at(self):
        self.seed("this is not toml = = =\n")
        self.record(CONTENT, findings=[blocking("CON-CIT-003")])
        data = self.read()
        self.assertEqual(self.ids(data, "findings", CONTENT),
                         ["CON-CIT-003"])


class TheMergedRecordStaysAFileTests(StandingRecordCase):
    """A merge reads its own output back, so the escaper is load-bearing."""

    AWKWARD = (
        'the lane quoted """three quotes""" and a \\latin{backslash},\n'
        'then a second line ending in "'
    )

    def test_prose_survives_being_read_back_and_written_again(self):
        self.record(CONTENT, findings=[advisory("CON-EVI-002",
                                                problem=self.AWKWARD)],
                    observations=[observation(self.AWKWARD)])
        self.record(SYNTHESIS, findings=[blocking("SYN-FID-004")],
                    disposition=PASS)
        data = self.read()
        self.assertEqual(data["advisories"][0]["problem"], self.AWKWARD)
        self.assertEqual(self.notes(data, CONTENT), [self.AWKWARD])

    def test_the_escalation_ledger_still_reaches_the_tree_whole(self):
        ledger = [{
            "stage": CONTENT, "iteration": 1,
            "escalated_to": "guidance/liturgy/roman-1962-propers.md",
            "finding": {"id": "CON-PRO-004", "lane": "profile-conformance",
                        "severity": "escalation",
                        "location": "the profile",
                        "problem": "states its macro-order twice",
                        "required_result": "the maintainer reconciles them",
                        "escalated_to":
                            "guidance/liturgy/roman-1962-propers.md"},
        }]
        self.record(CONTENT, findings=[blocking("CON-CIT-003")],
                    escalations=ledger)
        self.record(SYNTHESIS, findings=[], disposition=PASS,
                    escalations=ledger)
        data = self.read()
        self.assertEqual([e["id"] for e in data["escalations"]],
                         ["CON-PRO-004"])
        self.assertEqual(data["escalations"][0]["stage"], CONTENT)

    def test_the_engine_s_reader_sees_every_stage_s_findings(self):
        """`status` reports what stands, and it is not one stage's worth."""
        self.record(CONTENT, findings=[blocking("CON-CIT-003")])
        self.record(SYNTHESIS, findings=[blocking("SYN-FID-004")])
        standing = _standing_findings(self.root, DOCUMENT_ROOT)
        self.assertEqual(sorted(f["id"] for f in standing),
                         ["CON-CIT-003", "SYN-FID-004"])
        self.assertEqual(standing[0]["repair_target"], "authoring")


if __name__ == "__main__":
    unittest.main()
