"""The brief has a writer in `proper-finish`, and an escalation reaches the tree.

`proper-finish` begins after research, so until version 5 nothing in it could
write `research/scope.md`: a `brief` finding found there had no owner, and a
later authoring pass reading the uncorrected brief regenerated the defect the
previous evaluation had spent a finding removing. `brief-revision` is that
writer. It takes the `brief` findings, corrects the sentence in place, and hands
the run to `content-revision`, where the same evaluation's `authoring` findings
arrive under `CARRIED_FINDINGS`.

The same version writes the run's escalation ledger into the tracked standing
findings record, because seven escalations of one production survived only in
a handoff a driver wrote by hand.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools" / "tests"))

from _workflow import (  # noqa: E402
    CHANGES_REQUIRED,
    ESCALATION,
    PASS,
    REPAIRED,
    WorkflowEngine,
    _current_packet,
)
from test_workflow_research_fanout import CONTENT_LANES  # noqa: E402

WORKFLOW = "proper-finish"
DOC = "liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost"
PROVIDER = "gpt"
EVALUATION = "content-evaluation"
BRIEF_REVISION = "brief-revision"
REVISION = "content-revision"
PREFLIGHT = "content-preflight"
FRAGMENTS = ROOT / "workflows" / "fragments"


def blocking(finding_id: str, target: str) -> dict:
    return {
        "id": finding_id, "severity": "blocking",
        "location": "sections/30-commentary.tex 12",
        "problem": f"{finding_id} is wrong",
        "required_result": f"make {finding_id} right",
        "repair_target": target,
    }


def escalation(finding_id: str) -> dict:
    return {
        "id": finding_id, "severity": ESCALATION,
        "location": "src/sources/inventories/x.toml 5881",
        "problem": "two records contradict each other",
        "required_result": "the maintainer decides which governs",
        "escalated_to": "src/sources/inventories/x.toml",
    }


def header(packet_text: str, field: str) -> list:
    prefix = f"{field}: "
    line = next(l for l in packet_text.splitlines() if l.startswith(prefix))
    return json.loads(line[len(prefix):])


class FinishCase(unittest.TestCase):
    """Drives the real finish workflow in a private run directory."""

    def setUp(self):
        name = self.id().rsplit(".", 1)[-1]
        self.runs = ROOT / "build" / f"tpt-runs-finish-{os.getpid()}-{name}"
        shutil.rmtree(self.runs, ignore_errors=True)
        self.runs.mkdir(parents=True, exist_ok=True)
        self.addCleanup(shutil.rmtree, self.runs, ignore_errors=True)
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.engine.runs_dir = self.runs
        self.standing = self.runs / "standing"
        self.engine.standing_findings_root = self.standing
        self.answers = self.runs / "answers"
        self.answers.mkdir(parents=True, exist_ok=True)
        # As in PropersCase: no author writes the provenance record in a
        # driven run, and the house-voice screen is held elsewhere.
        unsatisfiable = {"provenance-matches-run", "house-voice"}
        real_run_gate = self.engine._run_gate

        def run_gate(workflow, stage, state, run_id):
            stage = {**stage, "checks": [
                check for check in stage.get("checks", [])
                if check["id"] not in unsatisfiable]}
            return real_run_gate(workflow, stage, state, run_id)

        self.engine._run_gate = run_gate
        self.workflow = self.engine.load_workflow(WORKFLOW)
        self.stages = {s["id"]: s for s in self.workflow["stages"]}

    def write(self, name: str, body: dict) -> str:
        path = self.answers / f"{name}.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return str(path)

    def worker_pass(self, run_id: str) -> str:
        state = self.engine.load_state(run_id)
        packet = state["packet_hashes"][-1]
        body = {
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": PASS, "summary": "probe", "findings": [],
            "artifact_path": "research/scope.md",
        }
        owed = state.get("findings_forwarded_ids", {}).get(packet["stage"], [])
        if owed and self.stages[packet["stage"]].get("reports_repairs"):
            body["finding_dispositions"] = [
                {"id": fid, "outcome": REPAIRED} for fid in owed]
        return self.write(f"{packet['stage']}-{packet['iteration']}", body)

    def pass_stage(self, run_id: str, stage_id: str) -> dict:
        if self.stages[stage_id]["type"] == "gate":
            return self.engine.advance(run_id, run_gate=True)
        return self.engine.advance(run_id, result_path=self.worker_pass(run_id))

    def drive_to(self, target: str) -> str:
        out = self.engine.seed(WORKFLOW, {"proper": DOC, "provider": PROVIDER})
        run_id = out["run_id"]
        for _ in range(8):
            if out["stage"] == target:
                return run_id
            out = self.pass_stage(run_id, out["stage"])
        self.fail(f"could not reach {target}: at {out['stage']}")

    def evaluate(self, run_id: str, by_lane: dict) -> dict:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {e["lane"]: e for e in packet["lanes"]}
        pairs = []
        for lane in CONTENT_LANES:
            findings = list(by_lane.get(lane, []))
            pairs.append((lane, self.write(f"lane-{lane}-{packet['iteration']}", {
                "stage": packet["stage"], "iteration": packet["iteration"],
                "lane": lane, "lane_packet_hash": emitted[lane]["hash"],
                "disposition": (CHANGES_REQUIRED if any(
                    f["severity"] == "blocking" for f in findings) else PASS),
                "summary": f"{lane} judged its criteria",
                "findings": findings,
            })))
        return self.engine.advance(run_id, lane_results=pairs)

    def packet_text(self, run_id: str) -> str:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        return (ROOT / packet["path"]).read_text(encoding="utf-8")


class BriefRouteTests(FinishCase):
    """A `brief` finding has an owner in the finish pipeline."""

    MIXED = {
        CONTENT_LANES[2]: [blocking("CON-SYN-001", "brief")],
        CONTENT_LANES[0]: [blocking("CON-EVI-001", "authoring"),
                           blocking("CON-EVI-002", "authoring")],
    }

    def test_the_brief_owner_is_declared_and_writes_nothing_else(self):
        stage = self.stages[BRIEF_REVISION]
        self.assertEqual(stage["type"], "bounded-revision")
        self.assertEqual(stage["execution"], {"mode": "single"})
        self.assertEqual(stage["repairs"], ["brief"])
        self.assertTrue(stage["reports_repairs"])
        self.assertEqual(stage["next"], REVISION)
        text = (FRAGMENTS / "propers" / "brief-revision.md").read_text(
            encoding="utf-8")
        self.assertIn("research/scope.md", text)
        self.assertIn("may not edit the canonical leaf", text)
        self.assertNotIn(BRIEF_REVISION, {
            s["id"] for s in self.engine.load_workflow("proper")["stages"]},
            "in proper the brief's writer is research-synthesis")

    def test_a_brief_finding_goes_to_the_brief_and_the_leafs_findings_follow(self):
        run_id = self.drive_to(EVALUATION)
        out = self.evaluate(run_id, self.MIXED)
        self.assertEqual(out["stage"], BRIEF_REVISION,
                         "brief outranks authoring, as in proper")
        text = self.packet_text(run_id)
        self.assertEqual([f["id"] for f in header(text, "PRIOR_FINDINGS")],
                         ["CON-SYN-001"],
                         "only the findings that chose the route travel it")
        self.assertEqual(header(text, "CARRIED_FINDINGS"), [])
        self.assertNotIn("REPAIR_TARGETS:", text,
                         "a worker-shaped stage routes nothing and its packet "
                         "names no owners")

        out = self.pass_stage(run_id, BRIEF_REVISION)
        self.assertEqual(out["stage"], REVISION,
                         "the brief is corrected in place and the leaf's own "
                         "reviser runs next, not a re-authoring")
        text = self.packet_text(run_id)
        self.assertEqual(header(text, "PRIOR_FINDINGS"), [],
                         "nothing was forwarded by an evaluator")
        self.assertEqual(
            sorted(f["id"] for f in header(text, "CARRIED_FINDINGS")),
            ["CON-EVI-001", "CON-EVI-002"],
            "the authoring findings the route passed over are carried to "
            "the owner that runs next")
        state = self.engine.load_state(run_id)
        self.assertEqual(state["findings_forwarded_ids"].get(REVISION, []), [])

        out = self.pass_stage(run_id, REVISION)
        self.assertEqual(out["stage"], PREFLIGHT,
                         "a reviser handed nothing forwarded owes no report "
                         "and the loop re-enters the gate")

    def test_a_brief_finding_not_repaired_charges_the_evaluators_budget(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, {CONTENT_LANES[2]: [blocking("CON-SYN-001", "brief")]})
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        out = self.engine.advance(run_id, result_path=self.write("brief-fail", {
            "stage": BRIEF_REVISION, "iteration": packet["iteration"],
            "disposition": PASS, "summary": "could not", "findings": [],
            "artifact_path": "research/scope.md",
            "finding_dispositions": [
                {"id": "CON-SYN-001", "outcome": "not-repaired",
                 "note": "needs evidence the brief does not hold"}],
        }))
        self.assertEqual(out["stage"], REVISION)
        state = self.engine.load_state(run_id)
        self.assertEqual(state["unrepaired_for"].get(EVALUATION), ["CON-SYN-001"],
                         "the report is charged to the stage whose finding it was")

    def test_a_research_owner_is_refused_at_the_join(self):
        run_id = self.drive_to(EVALUATION)
        with self.assertRaises(Exception) as caught:
            self.evaluate(run_id, {
                CONTENT_LANES[3]: [blocking("CON-CIT-001", "research")]})
        self.assertIn("expected one of: brief, authoring", str(caught.exception))


class EscalationRecordTests(FinishCase):
    """The ledger reaches the tree beside the findings."""

    def record(self) -> dict:
        path = (self.standing / "src" / PROVIDER / DOC / "evaluations"
                / "blocking-findings-v1.toml")
        self.assertTrue(path.is_file(), f"no standing record at {path}")
        return tomllib.loads(path.read_text(encoding="utf-8"))

    def test_an_escalation_is_written_beside_the_standing_findings(self):
        run_id = self.drive_to(EVALUATION)
        out = self.evaluate(run_id, {
            CONTENT_LANES[4]: [escalation("CON-PRO-004"),
                               blocking("CON-PRO-001", "authoring")]})
        self.assertEqual(out["stage"], REVISION)
        record = self.record()
        self.assertEqual(record["standing_findings_schema"], 2)
        self.assertEqual([f["id"] for f in record["findings"]], ["CON-PRO-001"])
        self.assertEqual(len(record["escalations"]), 1)
        entry = record["escalations"][0]
        self.assertEqual(entry["id"], "CON-PRO-004")
        self.assertEqual(entry["stage"], EVALUATION)
        self.assertEqual(entry["iteration"], 0)
        self.assertEqual(entry["lane"], CONTENT_LANES[4])
        self.assertEqual(entry["escalated_to"], "src/sources/inventories/x.toml")
        self.assertEqual(entry["required_result"],
                         "the maintainer decides which governs")

    def test_the_ledger_persists_into_a_later_passing_record(self):
        run_id = self.drive_to(EVALUATION)
        self.evaluate(run_id, {
            CONTENT_LANES[4]: [escalation("CON-PRO-004"),
                               blocking("CON-PRO-001", "authoring")]})
        self.pass_stage(run_id, REVISION)
        self.pass_stage(run_id, PREFLIGHT)
        out = self.evaluate(run_id, {})
        self.assertEqual(out["stage"], "derive-synthesis")
        record = self.record()
        self.assertEqual(record["disposition"], PASS)
        self.assertEqual(record.get("findings", []), [])
        self.assertEqual([e["id"] for e in record["escalations"]],
                         ["CON-PRO-004"],
                         "a pass clears the findings and keeps the decision "
                         "the maintainer still owes")


class CriteriaOwnershipTests(unittest.TestCase):
    """The two new criteria exist and each has exactly one lane."""

    def fragment(self, name: str) -> str:
        return (FRAGMENTS / "propers" / name).read_text(encoding="utf-8")

    def test_the_shared_fragment_states_both_criteria(self):
        shared = self.fragment("content-evaluation.md")
        self.assertIn("13. **Fidelity to the appointed texts**", shared)
        self.assertIn("14. **Fidelity to the guide itself**", shared)
        self.assertIn("one fullest\n   home", shared)
        self.assertIn("discovery section and not a recap", shared)

    def test_each_new_criterion_has_one_owning_lane(self):
        owners = {}
        for lane in ("content-evidence-discipline", "content-reception-sweep",
                     "content-synthesis-argument", "content-citation-integrity",
                     "content-profile-conformance"):
            text = self.fragment(f"lanes/{lane}.md")
            for criterion in ("13 (Fidelity to the appointed texts)",
                              "14 (Fidelity to the guide itself)"):
                if f"**{criterion}**" in text:
                    owners.setdefault(criterion, []).append(lane)
        self.assertEqual(owners, {
            "13 (Fidelity to the appointed texts)": ["content-evidence-discipline"],
            "14 (Fidelity to the guide itself)": ["content-profile-conformance"],
        })


if __name__ == "__main__":
    unittest.main()
