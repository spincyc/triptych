#!/usr/bin/env python3
"""Why a run stops, and who is allowed to say so.

Run `90dcdddcb6780e60` -- `proper-finish` v1, the Fourteenth Sunday after
Pentecost, provider `claude` -- converged the whole way and blocked anyway. It
raised seven blocking findings, then eleven, then seven; each iteration cleared
the set before it and reached further into the leaf; one of its five lanes went
clean at the second iteration and stayed clean. It terminated at 3/3 with this
message:

    iteration limit exceeded for content-evaluation: 3/3 failures repeating a
    finding this stage had already raised still unrepaired: CON-CIT-020,
    CON-CIT-021, CON-PRO-001, CON-PRO-002

Every one of those four ids named a different defect in a different file each
iteration. `CON-CIT-020` was a quotation attributed to an 1895 newspaper that
no research record carried, and then the King James reference entry.
`CON-PRO-001` was body/appendix duplication, then seven `\\englishgap` blocks,
then checksums printed in the reader-facing body. The earlier ones were
repaired and gone from the document. `stage_failures` stood at 3 against a
ceiling of 6: the run was stopped at half the allowance its own design granted
it, on a false premise, in the direction that looks like a verdict.

No lane caused it and no lane could have prevented it. A fan-out evaluator's
lane packets carry an empty `PRIOR_FINDINGS` by design and lanes are told not
to read earlier results, so no lane can know which ids an earlier iteration
used. One lane guessed at `010`/`011` to dodge a collision it could not see;
another minted `020`/`021` to dodge ids recorded in the brief and landed
squarely on the previous iteration's. An id is a handle a lane minted for its
own report. It is not an identity for a defect.

So the signal moves to the reviser, which is the only actor that can hold it:
it was given the findings, it attempted them, and it knows which it could not
clear. These tests hold that: repair that worked is progress, repair that was
attempted and failed is what spends the budget, and a finding quietly dropped
is refused rather than scored as success.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    NOT_REPAIRED,
    PASS,
    REPAIRED,
    WorkflowError,
    _document_root,
    _standing_findings,
    _toml_string,
)
from test_workflow_repair_routing import (  # noqa: E402
    AUTHORING,
    RoutingCase,
    blocking,
)
from test_workflow_research_fanout import CONTENT_LANES  # noqa: E402

EVALUATION = "content-evaluation"
REVISION = "content-revision"


class BudgetCase(RoutingCase):
    """Drive the evaluation loop with explicit repair reports."""

    def evaluate(self, run_id: str, ids: list[str]) -> dict:
        return self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {CONTENT_LANES[0]: [blocking(fid, AUTHORING)
                                        for fid in ids]}))

    def revise(self, run_id: str, outcomes: dict[str, str]) -> dict:
        state = self.engine.load_state(run_id)
        packet = state["packet_hashes"][-1]
        path = self.write("revision", {
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": PASS, "summary": "probe", "findings": [],
            "artifact_path": "main.tex",
            "finding_dispositions": [
                {"id": fid, "outcome": outcome, "note": "probe"}
                for fid, outcome in outcomes.items()
            ],
        })
        return self.engine.advance(run_id, result_path=path)

    def round_trip(self, run_id: str, ids: list[str],
                   outcomes: dict[str, str]) -> dict:
        out = self.evaluate(run_id, ids)
        if out.get("stage") == "BLOCKED":
            return out
        self.revise(run_id, outcomes)
        return self.engine.advance(run_id, run_gate=True)


class RepairThatWorkedIsProgressTests(BudgetCase):
    """Fresh findings every round, every repair reported successful."""

    def test_three_rounds_of_new_work_do_not_spend_the_repeat_budget(self):
        run_id = self.drive_to(EVALUATION)
        for round_no in range(3):
            ids = [f"CON-EVI-{round_no}{n}" for n in range(2)]
            self.round_trip(run_id, ids, {fid: REPAIRED for fid in ids})
        state = self.engine.load_state(run_id)
        self.assertIsNone(state["disposition"],
                          "the run is still drivable after three rounds")
        self.assertEqual(state["stage_failures"][EVALUATION], 3)
        self.assertEqual(
            state["stage_repeats"][EVALUATION], 1,
            "only the opening failure; the rest were repairs that worked")

    def test_reusing_an_id_for_a_different_defect_costs_nothing(self):
        """The exact shape that blocked 90dcdddcb6780e60."""
        run_id = self.drive_to(EVALUATION)
        for _ in range(3):
            self.round_trip(run_id, ["CON-CIT-020", "CON-PRO-001"],
                            {"CON-CIT-020": REPAIRED,
                             "CON-PRO-001": REPAIRED})
        state = self.engine.load_state(run_id)
        self.assertIsNone(
            state["disposition"],
            "the same ids three times running, every repair reported "
            "successful: under the id rule this blocked at 3/3")
        self.assertEqual(state["stage_repeats"][EVALUATION], 1)


class RepairThatFailedSpendsTheBudgetTests(BudgetCase):
    """A reviser saying it could not clear something is what stops a stage."""

    def test_a_reported_failure_charges_the_budget(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-PRO-001"],
                        {"CON-PRO-001": NOT_REPAIRED})
        state = self.engine.load_state(run_id)
        self.assertEqual(
            state["stage_repeats"][EVALUATION], 1,
            "the opening failure; the report lands on the next evaluation")
        self.round_trip(run_id, ["CON-PRO-001"],
                        {"CON-PRO-001": NOT_REPAIRED})
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_repeats"][EVALUATION], 2)

    def test_repeated_failures_block_and_the_message_says_what_and_why(self):
        run_id = self.drive_to(EVALUATION)
        out = None
        for _ in range(4):
            out = self.round_trip(run_id, ["CON-PRO-001"],
                                  {"CON-PRO-001": NOT_REPAIRED})
            if out.get("stage") == "BLOCKED":
                break
        self.assertEqual(out.get("stage"), "BLOCKED")
        self.assertIn("did not converge", out["message"])
        self.assertIn("attempted and not repaired", out["message"])
        self.assertIn("CON-PRO-001", out["message"])
        self.assertNotIn("repeating a finding", out["message"])


class EveryFindingIsAccountedForTests(BudgetCase):
    """A dropped finding reads exactly like a repaired one."""

    def test_a_reviser_that_omits_a_finding_is_refused(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, ["CON-EVI-001", "CON-EVI-002"])
        with self.assertRaises(WorkflowError) as caught:
            self.revise(run_id, {"CON-EVI-001": REPAIRED})
        self.assertIn("CON-EVI-002", str(caught.exception))

    def test_a_reviser_reporting_on_what_it_was_not_given_is_refused(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, ["CON-EVI-001"])
        with self.assertRaises(WorkflowError) as caught:
            self.revise(run_id, {"CON-EVI-001": REPAIRED,
                                 "CON-EVI-099": REPAIRED})
        self.assertIn("CON-EVI-099", str(caught.exception))

    def test_a_refused_report_leaves_the_run_where_it_was(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, ["CON-EVI-001", "CON-EVI-002"])
        before = self.engine.load_state(run_id)["current_stage"]
        with self.assertRaises(WorkflowError):
            self.revise(run_id, {"CON-EVI-001": REPAIRED})
        after = self.engine.load_state(run_id)
        self.assertEqual(after["current_stage"], before)
        self.assertIsNone(after["disposition"])


class TheDocumentRootIsStatedTests(unittest.TestCase):
    """`ARGS` decides the path; the engine should not make a worker infer it.

    A `citation-integrity` lane swept `src/gpt/...` to completion against a
    packet whose `ARGS` read `"provider":"claude"`, caught it only from an
    unrelated `git status`, and discarded a finished max-effort sweep.
    """

    def test_a_declared_template_resolves_against_the_arguments(self):
        self.assertEqual(
            _document_root(
                {"document_root": "src/{provider}/{proper}"},
                {"provider": "claude", "proper": "liturgy/x/54-y"},
            ),
            "src/claude/liturgy/x/54-y",
        )

    def test_a_workflow_that_declares_none_gets_none(self):
        self.assertIsNone(_document_root({}, {"provider": "claude"}))

    def test_a_template_naming_an_absent_argument_gets_none(self):
        """A guessed path is worse than no path."""
        self.assertIsNone(
            _document_root({"document_root": "src/{missing}"}, {}))


class StandingFindingsOutliveTheirRunTests(unittest.TestCase):
    """A content evaluation's findings reached nothing tracked at all.

    `build/tpt-runs/` is ignored output that `make clean` and `wt tidy` delete
    without asking. One authoring worker, handed an empty `CARRIED_FINDINGS`
    by a pipeline that begins after research, went and read a dead run's
    result directory to find out what was standing against the leaf it was
    rewriting -- work no replay of that packet could reproduce.
    """

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)

    def test_an_absent_record_is_not_an_error(self):
        self.assertEqual(_standing_findings(self.root, "src/claude/leaf"), [])

    def test_no_document_root_reads_nothing(self):
        self.assertEqual(_standing_findings(self.root, None), [])

    def test_a_recorded_finding_comes_back_whole(self):
        target = self.root / "src/claude/leaf/evaluations"
        target.mkdir(parents=True)
        (target / "blocking-findings-v1.toml").write_text(
            'standing_findings_schema = 1\n\n'
            '[[findings]]\n'
            'id = "CON-PRO-002"\n'
            'lane = "profile-conformance"\n'
            'severity = "blocking"\n'
            'location = "sections/30-commentary.tex"\n'
            'problem = "narrates the sweep"\n'
            'required_result = "state the finding"\n'
            'repair_target = "authoring"\n',
            encoding="utf-8",
        )
        standing = _standing_findings(self.root, "src/claude/leaf")
        self.assertEqual(len(standing), 1)
        self.assertEqual(standing[0]["id"], "CON-PRO-002")
        self.assertEqual(standing[0]["repair_target"], "authoring")

    def test_an_unreadable_record_carries_nothing_rather_than_guessing(self):
        target = self.root / "src/claude/leaf/evaluations"
        target.mkdir(parents=True)
        (target / "blocking-findings-v1.toml").write_text(
            "this is not toml = = =\n", encoding="utf-8")
        self.assertEqual(_standing_findings(self.root, "src/claude/leaf"), [])


class TheRecordSurvivesTheProseItHoldsTests(unittest.TestCase):
    """The record's values are a lane's own finding text, unsanitized.

    A finding quotes the document, so it arrives carrying quotation marks,
    backslashes out of LaTeX and newlines, and it is written to a file another
    run has to parse at seed. The first version of the escaper handled `\"\"\"`
    specially and mangled a value ending in one, which is the failure mode that
    matters: a record that parses as something other than what was written.
    """

    def norm(self, text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        return "".join(
            ch if ch in "\t\n" or (0x20 <= ord(ch) < 0x7F) or (
                0xA0 <= ord(ch) and not 0xD800 <= ord(ch) <= 0xDFFF
            )
            else "\\u%04x" % ord(ch)
            for ch in text
        )

    def round_trip(self, text: str):
        import tomllib
        return tomllib.loads(f"v = {_toml_string(text)}\n")["v"]

    def test_the_awkward_values_survive(self):
        for text in [
            "plain", 'has "quotes"', "back\\slash", "two\nlines",
            'multi\nline with "a quote"', "ends with a backslash \\",
            'triple """ inside', 'multi\nline with triple """ inside',
            "tab\there", 'ends with a quote "', 'multi\nline ending "',
            '"""', "\n", "", 'a\\"b', 'z\taa\nz"""',
            # A cold review found the first of these: U+007F satisfies
            # `>= 0x20` and TOML refuses it anyway, so one stray byte in a
            # quoted source made the record unparseable -- and the reader,
            # catching that, discarded every well-formed finding in it.
            "DEL\x7fhere", "NEL\x85here", "C1\x9fhere",
            "\u2028line separator", "accents \u00e9\u00e8", "\u4e2d\u6587",
        ]:
            with self.subTest(text=text):
                self.assertEqual(self.round_trip(text), self.norm(text))

    def test_a_control_character_does_not_break_the_file(self):
        self.assertEqual(self.round_trip("null\x00byte"), "null\\u0000byte")

    def test_the_characters_toml_refuses_are_escaped_not_passed_through(self):
        """`ord(ch) >= 0x20` is not the test TOML applies."""
        for text, expected in (
            ("DEL\x7fhere", "DEL\\u007fhere"),
            ("NEL\x85here", "NEL\\u0085here"),
            ("C1\x9fhere", "C1\\u009fhere"),
        ):
            with self.subTest(text=text):
                self.assertEqual(self.round_trip(text), expected)

    def test_printable_non_ascii_is_left_alone(self):
        """The escape is for what TOML refuses, not for everything foreign."""
        for text in ("Gu\u00e9ranger", "\u4e2d\u6587", "\u2028"):
            with self.subTest(text=text):
                self.assertEqual(self.round_trip(text), text)

    def test_random_prose_of_the_awkward_alphabet_round_trips(self):
        import random
        rng = random.Random(20260904)
        for _ in range(3000):
            text = "".join(
                rng.choice('"\\\n\ta z\x7f\x00\x85\u00e9')
                for _ in range(rng.randint(0, 14))
            )
            with self.subTest(text=text):
                self.assertEqual(self.round_trip(text), self.norm(text))


class TheRecordIsWrittenWhereItSurvivesTests(BudgetCase):
    """The write side: an evaluation leaves a tracked record of what stands."""

    def record(self):
        found = list(self.standing.rglob("blocking-findings-v1.toml"))
        self.assertEqual(len(found), 1, f"expected one record, got {found}")
        import tomllib
        return tomllib.loads(found[0].read_text(encoding="utf-8"))

    def test_an_evaluation_writes_what_stands_against_the_document(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, ["CON-PRO-002"])
        data = self.record()
        self.assertEqual(data["standing"], 1)
        self.assertEqual(data["run_id"], run_id)
        self.assertEqual(
            [f["id"] for f in data["findings"]], ["CON-PRO-002"])
        self.assertEqual(data["findings"][0]["repair_target"], "authoring")

    def test_the_record_states_what_stands_now_and_not_a_history(self):
        run_id = self.drive_to(EVALUATION)
        self.round_trip(run_id, ["CON-PRO-002"], {"CON-PRO-002": REPAIRED})
        self.evaluate(run_id, ["CON-CIT-021"])
        data = self.record()
        self.assertEqual(
            [f["id"] for f in data["findings"]], ["CON-CIT-021"],
            "rewritten whole: the repaired finding is gone, not appended to")

    def test_a_pass_records_that_nothing_stands(self):
        """Distinct from nobody having looked, and read differently later."""
        run_id = self.drive_to(EVALUATION)
        self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {}))
        data = self.record()
        self.assertEqual(data["standing"], 0)
        self.assertEqual(data["disposition"], PASS)
        self.assertEqual(data.get("findings", []), [])

    def test_the_run_that_blocks_records_what_it_blocked_on(self):
        """The case the record exists for, and the one it first missed.

        A cold review drove this: the write sat only on the transition that
        continues, so a run spending its budget returned before reaching it.
        The file left behind named the previous iteration's findings and stated
        a disposition of CHANGES_REQUIRED, reading as though the run were still
        going -- and the findings it actually blocked on survived nowhere but
        the ignored run directory this record was built to replace.
        """
        run_id = self.drive_to(EVALUATION)
        out = None
        for round_no in range(6):
            out = self.round_trip(run_id, ["CON-PRO-900"],
                                  {"CON-PRO-900": NOT_REPAIRED})
            if out.get("stage") == "BLOCKED":
                break
        self.assertEqual(out.get("stage"), "BLOCKED",
                         "the run has to block for this test to mean anything")
        data = self.record()
        self.assertEqual(
            [f["id"] for f in data["findings"]], ["CON-PRO-900"],
            "the record names what the run blocked on, not the round before")
        self.assertEqual(data["run_id"], run_id)

    def test_the_engine_writes_nothing_when_the_record_is_turned_off(self):
        self.engine.standing_findings_root = None
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, ["CON-PRO-002"])
        self.assertEqual(list(self.standing.rglob("*.toml")), [])


class TheRecordCannotLeaveItsRootTests(unittest.TestCase):
    """`document_root` is a template filled from unvalidated arguments.

    `provider` is free text no validator constrains, so a typo made a whole
    `src/gtp/...` tree appear in the working copy and `..` put one anywhere the
    user could write. This is the engine's only write outside `build/`.
    """

    def setUp(self):
        import tempfile
        sys.path.insert(0, str(ROOT / "scripts"))
        from _workflow import WorkflowEngine
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.engine.standing_findings_root = Path(self.tmp.name)
        self.workflow = {
            "id": "probe", "version": 1,
            "document_root": "src/{provider}/{proper}", "stages": [],
        }
        self.stage = {"id": "content-evaluation", "type": "evaluator",
                      "records_standing_findings": True}
        self.result = {"disposition": "CHANGES_REQUIRED", "iteration": 0,
                       "findings": []}

    def write(self, provider):
        state = {"run_id": "probe", "normalized_args":
                 {"provider": provider, "proper": "leaf"}}
        self.engine._record_standing_findings(
            self.workflow, state, self.stage, self.result)

    def test_a_traversing_argument_is_refused(self):
        with self.assertRaises(WorkflowError) as caught:
            self.write("../../../../tmp/pwned")
        self.assertIn("outside", str(caught.exception))

    def test_an_ordinary_argument_still_writes(self):
        self.write("claude")
        self.assertTrue((Path(self.tmp.name) / "src/claude/leaf"
                         / "evaluations/blocking-findings-v1.toml").is_file())

    def test_a_stage_that_does_not_declare_it_writes_nothing(self):
        stage = dict(self.stage)
        del stage["records_standing_findings"]
        self.engine._record_standing_findings(
            self.workflow,
            {"run_id": "p", "normalized_args":
             {"provider": "claude", "proper": "leaf"}},
            stage, self.result)
        self.assertEqual(list(Path(self.tmp.name).rglob("*.toml")), [])


class ADeclarationThatCouldNotWorkIsRefusedAtLoadTests(unittest.TestCase):
    """A wedged production is a typo one line of validation would have caught.

    `reports_repairs` on a stage whose schema defines no
    `finding_disposition_fields` deadlocks: the engine demands the report once
    findings are forwarded there, and refuses a result that carries it.
    """

    def engine_over(self, mutate):
        import json
        import shutil
        import tempfile
        sys.path.insert(0, str(ROOT / "scripts"))
        from _workflow import WorkflowEngine
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        shutil.copytree(ROOT / "workflows", Path(tmp) / "workflows")
        path = Path(tmp) / "workflows/pipelines/proper.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        mutate(data)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return WorkflowEngine(ROOT, Path(tmp) / "workflows")

    def test_a_stage_whose_schema_cannot_carry_the_report_is_refused(self):
        def mutate(data):
            for stage in data["stages"]:
                if stage["id"] == "research":
                    stage["reports_repairs"] = True
        with self.assertRaises(WorkflowError) as caught:
            self.engine_over(mutate).load_workflow("proper")
        self.assertIn("finding_disposition_fields", str(caught.exception))

    def test_a_flag_that_is_not_a_boolean_is_refused(self):
        def mutate(data):
            for stage in data["stages"]:
                if stage["id"] == "content-revision":
                    stage["reports_repairs"] = "yes"
        with self.assertRaises(WorkflowError) as caught:
            self.engine_over(mutate).load_workflow("proper")
        self.assertIn("true or false", str(caught.exception))

    def test_the_real_pipelines_load(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from _workflow import WorkflowEngine
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        for workflow_id in ("proper", "proper-finish"):
            with self.subTest(workflow=workflow_id):
                self.assertTrue(engine.load_workflow(workflow_id)["stages"])


if __name__ == "__main__":
    unittest.main()
