#!/usr/bin/env python3
"""A defect goes back to the stage that owns it, and tpt decides which.

A content evaluator can find two unrelated things: that the research under
the guide is wrong, and that the prose over it is. They are not repaired in
the same place, and until now the workflow had one failure path, so the
second kind of defect was the only kind it could express. Findings now name
their repair owner in a validated field, and the engine reads that field —
not prose, not a filename, not a finding-id prefix, and not a controller's
judgment — to choose between re-entering research and revising the leaf.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    ACCEPTED,
    BLOCKED,
    CHANGES_REQUIRED,
    FANOUT,
    HOST_MAX,
    PASS,
    PROGRAM,
    REPAIR_ROUTES,
    REPAIR_TARGET,
    SINGLE,
    WorkflowEngine,
    WorkflowError,
    _repair_route,
)
from test_workflow_adversarial import (  # noqa: E402
    WORKFLOW,
    engine_for,
    make_repo,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    DOC,
    FRAGMENTS,
    LANE_PREFIX,
    RESEARCH_LANES,
    VISUAL_LANES,
    PropersCase,
    workflow_json,
)

RESEARCH = "research"
BRIEF = "brief"
AUTHORING = "authoring"
SYNTHESIS = "research-synthesis"


def blocking(finding_id: str, repair_target: str, problem: str = "a defect"):
    return {
        "id": finding_id, "severity": "blocking", "location": "page 1",
        "problem": problem, "required_result": "fix it",
        "repair_target": repair_target,
    }


def advisory(finding_id: str):
    """Advisory findings carry no repair target; nothing routes on them."""
    return {
        "id": finding_id, "severity": "advisory", "location": "page 2",
        "problem": "a nicety", "required_result": "consider it",
    }


class RoutingCase(PropersCase):
    """Drives the real propers workflow as far as content evaluation."""

    def research_submissions(self, run_id, order=None, **kwargs):
        return self.lane_submissions(run_id, order=order, **kwargs)

    def content_submissions(self, run_id, findings_by_lane=None,
                            order=None) -> list[tuple[str, str]]:
        """One content-evaluation lane result per declared lane."""
        findings_by_lane = findings_by_lane or {}
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {e["lane"]: e for e in packet["lanes"]}
        pairs = []
        for lane in (order if order is not None else CONTENT_LANES):
            findings = findings_by_lane.get(lane, [])
            body = {
                "stage": packet["stage"], "iteration": packet["iteration"],
                "lane": lane, "lane_packet_hash": emitted[lane]["hash"],
                "disposition": CHANGES_REQUIRED if findings else PASS,
                "summary": f"{lane} judged its criteria",
                "findings": findings,
            }
            pairs.append((lane, self.write(f"content-{lane}", body)))
        return pairs

    def drive_to(self, target: str) -> str:
        """Seed and advance until the run is waiting at target."""
        out = self.seed()
        run_id = out["run_id"]
        for _ in range(20):
            state = self.engine.load_state(run_id)
            stage_id = state["current_stage"]
            if stage_id == target:
                return run_id
            if stage_id == RESEARCH:
                self.engine.advance(
                    run_id, lane_results=self.research_submissions(run_id))
            elif stage_id == "content-evaluation":
                self.engine.advance(
                    run_id, lane_results=self.content_submissions(run_id))
            else:
                self.pass_stage(run_id, stage_id)
        self.fail(f"could not reach {target}")

    def route_for(self, findings_by_lane: dict, order=None) -> dict:
        """Submit one content evaluation and report where the run went."""
        run_id = self.drive_to("content-evaluation")
        out = self.engine.advance(
            run_id, lane_results=self.content_submissions(
                run_id, findings_by_lane, order=order))
        state = self.engine.load_state(run_id)
        joined = state["result_hashes"][-1]
        return {
            "run_id": run_id,
            "next": out.get("stage"),
            "disposition": out.get("disposition"),
            "packet_hash": out.get("packet_hash"),
            "packet": (Path(out["packet_abs_path"]).read_text(encoding="utf-8")
                       if out.get("packet_abs_path") else ""),
            "joined_bytes": (ROOT / joined["path"]).read_bytes(),
            "transition": state["transitions"][-1],
        }

    def forwarded(self, packet_text: str) -> list[dict]:
        line = next(l for l in packet_text.splitlines()
                    if l.startswith("PRIOR_FINDINGS: "))
        return json.loads(line[len("PRIOR_FINDINGS: "):])


# ---------------------------------------------------------------------------
# 9-14. Synthesis integrates and does not search
# ---------------------------------------------------------------------------

class PureSynthesisTests(RoutingCase):
    """Test 9-14: every original search left this stage."""

    def test_research_synthesis_is_single_and_owns_the_brief(self):
        """Test 9 and 10."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertEqual(stages[SYNTHESIS]["execution"], {"mode": SINGLE})
        text = (FRAGMENTS / "propers" / f"{SYNTHESIS}.md").read_text(
            encoding="utf-8")
        self.assertRegex(text, re.compile(r"sole writer", re.IGNORECASE))
        self.assertIn("research/scope.md", text)

    def test_the_emitted_packet_forbids_new_evidence_gathering(self):
        """Test 11: on the bytes the worker is handed, not the prose about it."""
        run_id = self.drive_to(SYNTHESIS)
        packet = Path(self.engine.replay(run_id) and
                      ROOT / self.engine.load_state(run_id)
                      ["packet_hashes"][-1]["path"]).read_text(encoding="utf-8")
        for forbidden in ("search the web",
                          "search the repository for precedent",
                          "acquire new sources",
                          "hunt cultural afterlives",
                          "find new witnesses",
                          "fill a gap by doing your own research",
                          "silently supplement incomplete lane output"):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, packet)
        self.assertRegex(packet, re.compile(
            r"no original evidence-gathering", re.IGNORECASE))

    def test_the_two_moved_searches_are_no_longer_synthesis_work(self):
        """Test 12 and 13: the instructions moved, they were not duplicated."""
        text = (FRAGMENTS / "propers" / f"{SYNTHESIS}.md").read_text(
            encoding="utf-8")
        flat = " ".join(text.split())
        for gone in ("Hunt the three to five",
                     "run the targeted precedent search",
                     "the cultural-afterlife hunt behind"):
            with self.subTest(gone=gone):
                self.assertNotIn(gone, flat)
        # It still consumes both lanes' output; it just does not produce it.
        self.assertIn("`cultural-afterlife` lane", flat)
        self.assertIn("`precedent-search` lane", flat)
        self.assertRegex(flat, re.compile(
            r"You select; you do not go looking", re.IGNORECASE))

    def test_the_moved_work_lives_in_the_two_new_lanes(self):
        """Test 3 and 4."""
        cultural = (FRAGMENTS / "propers" / "lanes"
                    / "research-cultural-afterlife.md").read_text("utf-8")
        precedent = (FRAGMENTS / "propers" / "lanes"
                     / "research-precedent-search.md").read_text("utf-8")
        self.assertIn("CUL-", cultural)
        self.assertIn("PRE-", precedent)
        self.assertRegex(precedent, re.compile(
            r"not located in the checked corpus"))
        self.assertRegex(cultural, re.compile(
            r"you do not choose the published\s+gallery", re.IGNORECASE))

        run_id = self.drive_to(RESEARCH)
        lanes = {l["lane"]: l for l in self.emitted_lanes(run_id)}
        for lane in ("cultural-afterlife", "precedent-search"):
            with self.subTest(lane=lane):
                self.assertIn(lane, lanes)
                text = (ROOT / lanes[lane]["path"]).read_text(encoding="utf-8")
                self.assertIn(f"LANE: {lane}", text)
                self.assertIn(f"{LANE_PREFIX[lane]}-", text)
                self.assertIn(
                    f"--- FRAGMENT: propers/lanes/research-{lane}.md ---",
                    text)

    def test_insufficient_research_lets_synthesis_block(self):
        """Test 14."""
        run_id = self.drive_to(SYNTHESIS)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        out = self.engine.advance(run_id, result_path=self.write("thin", {
            "stage": SYNTHESIS, "iteration": packet["iteration"],
            "disposition": BLOCKED, "findings": [],
            "summary": "the appointed witness cannot be obtained under "
                       "current source policy; no further sweep would help",
        }))
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertEqual(self.engine.load_state(run_id)["disposition"],
                         BLOCKED)


# ---------------------------------------------------------------------------
# 15-23. Repair ownership and routing
# ---------------------------------------------------------------------------

class RepairOwnershipTests(RoutingCase):
    """Test 15-23: the field decides, and nothing else gets a vote."""

    def test_a_blocking_finding_must_carry_a_valid_repair_target(self):
        """Test 15."""
        run_id = self.drive_to("content-evaluation")
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {e["lane"]: e for e in packet["lanes"]}

        def submit(finding, disposition=CHANGES_REQUIRED) -> str:
            body = {
                "stage": "content-evaluation",
                "iteration": packet["iteration"],
                "lane": CONTENT_LANES[0],
                "lane_packet_hash": emitted[CONTENT_LANES[0]]["hash"],
                "disposition": disposition,
                "summary": "judged", "findings": [finding],
            }
            pairs = self.content_submissions(run_id)
            pairs[0] = (CONTENT_LANES[0], self.write("bad", body))
            return pairs

        missing = {"id": "CON-001", "severity": "blocking",
                   "location": "p1", "problem": "x", "required_result": "y"}
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submit(missing))
        self.assertIn("blocking and missing required field: repair_target",
                      str(caught.exception))

        wrong = dict(missing, repair_target="typesetting")
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submit(wrong))
        self.assertIn("expected one of: research, brief, authoring",
                      str(caught.exception))

        # Severity is what decides whether the owner is required at all, so
        # it is enumerated too: a mis-cased severity would otherwise read as
        # advisory, and a real research defect would route to authoring.
        miscased = dict(missing, severity="Blocking", repair_target=RESEARCH)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submit(miscased))
        self.assertIn("expected one of: blocking, advisory",
                      str(caught.exception))

        # CHANGES_REQUIRED naming no owner would send a reviser work it
        # cannot see, so a routed stage refuses it.
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submit(advisory("CON-9")))
        self.assertIn("no blocking finding", str(caught.exception))

        # An advisory finding needs no owner: nothing routes on it, and a
        # result that asks for no change is a PASS.
        self.engine.advance(
            run_id, lane_results=submit(advisory("CON-900"), PASS))

    def test_authoring_only_findings_route_to_content_revision(self):
        """Test 16."""
        out = self.route_for({
            "citation-integrity": [blocking("CON-CIT-001", AUTHORING)],
            "profile-conformance": [blocking("CON-PRO-001", AUTHORING)],
        })
        self.assertEqual(out["next"], "content-revision")
        self.assertEqual(out["transition"],
                         {"from": "content-evaluation",
                          "to": "content-revision",
                          "disposition": CHANGES_REQUIRED})
        self.assertEqual(
            sorted(f["id"] for f in self.forwarded(out["packet"])),
            ["CON-CIT-001", "CON-PRO-001"])

    def test_any_research_finding_routes_to_research(self):
        """Test 17."""
        out = self.route_for({
            "reception-sweep": [blocking("CON-REC-001", RESEARCH)],
        })
        self.assertEqual(out["next"], RESEARCH)
        self.assertEqual(out["transition"]["to"], RESEARCH)

    def test_mixed_findings_route_to_research_first(self):
        """Test 18: declaration order is priority order, and research is first."""
        out = self.route_for({
            "evidence-discipline": [blocking("CON-EVI-001", RESEARCH)],
            "citation-integrity": [blocking("CON-CIT-001", AUTHORING)],
            "profile-conformance": [blocking("CON-PRO-001", AUTHORING)],
        })
        self.assertEqual(out["next"], RESEARCH,
                         "one research finding sends the whole run to research")

    def test_a_brief_finding_routes_to_the_briefs_sole_writer(self):
        """The middle owner, and the whole reason it exists.

        The evidence is held and the brief states it wrongly. Nothing has to
        be retrieved, and `research-synthesis` is the only stage that may
        write `research/scope.md`, so the repair goes straight there instead
        of discarding a sound brief and re-running seven lanes to arrive back
        at the same writer.
        """
        out = self.route_for({
            "citation-integrity": [blocking("CON-CIT-011", BRIEF)],
        })
        self.assertEqual(out["next"], SYNTHESIS)
        self.assertEqual(out["transition"],
                         {"from": "content-evaluation", "to": SYNTHESIS,
                          "disposition": CHANGES_REQUIRED})
        forwarded = self.forwarded(out["packet"])
        self.assertEqual([f["id"] for f in forwarded], ["CON-CIT-011"])
        self.assertTrue(all(f[REPAIR_TARGET] == BRIEF for f in forwarded),
                        "only brief-owned findings enter the brief repair")

    def test_a_brief_finding_outranks_an_authoring_one(self):
        """Declaration order again, one place further down the list."""
        out = self.route_for({
            "citation-integrity": [blocking("CON-CIT-011", BRIEF)],
            "profile-conformance": [blocking("CON-PRO-001", AUTHORING)],
        })
        self.assertEqual(out["next"], SYNTHESIS,
                         "the brief is corrected before the prose written "
                         "from it")
        self.assertEqual([f["id"] for f in self.forwarded(out["packet"])],
                         ["CON-CIT-011"],
                         "the authoring finding is not carried across the "
                         "reauthoring its own route would trigger")

    def test_a_research_finding_still_outranks_a_brief_one(self):
        """The new owner did not displace the earliest one."""
        out = self.route_for({
            "evidence-discipline": [blocking("CON-EVI-001", RESEARCH)],
            "citation-integrity": [blocking("CON-CIT-011", BRIEF)],
        })
        self.assertEqual(out["next"], RESEARCH,
                         "evidence that was never gathered is repaired first")
        self.assertEqual([f["id"] for f in self.forwarded(out["packet"])],
                         ["CON-EVI-001"])

    def test_the_three_owners_are_declared_in_priority_order(self):
        """The order is the routing, so it is asserted as an ordered list."""
        stage = {s["id"]: s for s in workflow_json()["stages"]}[
            "content-evaluation"]
        self.assertEqual(
            [route[REPAIR_TARGET] for route in stage[REPAIR_ROUTES]],
            [RESEARCH, BRIEF, AUTHORING],
            "earliest authoritative owner first")
        self.assertEqual(
            [route["transition"] for route in stage[REPAIR_ROUTES]],
            [RESEARCH, SYNTHESIS, "content-revision"])

    def test_only_the_routed_findings_travel_the_route(self):
        """Test 20: a research finding cannot arrive at content-revision."""
        out = self.route_for({
            "evidence-discipline": [blocking("CON-EVI-001", RESEARCH)],
            "citation-integrity": [blocking("CON-CIT-001", AUTHORING)],
        })
        self.assertEqual(out["next"], RESEARCH)
        forwarded = self.forwarded(out["packet"])
        self.assertEqual([f["id"] for f in forwarded], ["CON-EVI-001"])
        self.assertTrue(all(f["repair_target"] == RESEARCH for f in forwarded),
                        "only research-owned findings enter the research loop")

    def test_the_research_stage_receives_the_research_findings(self):
        """Test 21: on every lane packet, deterministically."""
        out = self.route_for({
            "reception-sweep": [blocking("CON-REC-001", RESEARCH,
                                         "the Offertory has no reception row")],
        })
        self.assertEqual(out["next"], RESEARCH)
        state = self.engine.load_state(out["run_id"])
        lanes = state["packet_hashes"][-1]["lanes"]
        self.assertEqual(len(lanes), len(RESEARCH_LANES))
        for lane in lanes:
            with self.subTest(lane=lane["lane"]):
                text = (ROOT / lane["path"]).read_text(encoding="utf-8")
                self.assertIn("the Offertory has no reception row", text)
                self.assertIn("CON-REC-001", text)
        replay = self.engine.replay(out["run_id"])
        self.assertTrue(replay["deterministic"],
                        "the forwarded findings must replay from the record")

    def test_the_route_cannot_depend_on_who_reported_first(self):
        """Test 19: the field decides; submission order is not an input."""
        findings = {
            "evidence-discipline": [blocking("CON-EVI-001", RESEARCH)],
            "citation-integrity": [blocking("CON-CIT-001", AUTHORING)],
        }
        declared = self.route_for(findings)
        self.discard_runs()
        scrambled = self.route_for(findings, order=list(reversed(CONTENT_LANES)))
        self.assertEqual(declared["next"], scrambled["next"])
        self.assertEqual(declared["packet_hash"], scrambled["packet_hash"])
        self.assertEqual(declared["joined_bytes"], scrambled["joined_bytes"])

    def test_the_rule_is_a_function_of_the_result_alone(self):
        """Test 19, at the unit the engine actually branches on."""
        stage = next(s for s in workflow_json()["stages"]
                     if s["id"] == "content-evaluation")
        cases = [
            ([blocking("A", AUTHORING)], "content-revision"),
            ([blocking("A", RESEARCH)], RESEARCH),
            ([blocking("A", AUTHORING), blocking("B", RESEARCH)], RESEARCH),
            ([blocking("B", RESEARCH), blocking("A", AUTHORING)], RESEARCH),
            ([advisory("A")], None),
            ([], None),
        ]
        for findings, expected in cases:
            with self.subTest(findings=[f["id"] for f in findings]):
                route = _repair_route(stage, {"findings": findings})
                self.assertEqual(
                    route["transition"] if route else None, expected)

    def test_the_correction_path_is_exactly_the_declared_loop(self):
        """Test 22 and 23: research, synthesis, authoring, preflight, fresh
        evaluation.

        Version 10 put `content-preflight` between the author and the
        evaluation, so the regenerated leaf is checked mechanically before
        five AI lanes read it. The route the correction takes is otherwise
        the one the workflow has always declared.
        """
        run_id = self.drive_to("content-evaluation")
        out = self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {"evidence-discipline": [blocking("CON-EVI-001", RESEARCH)]}))

        visited = [out["stage"]]
        self.assertEqual(out["stage"], RESEARCH)
        out = self.engine.advance(
            run_id, lane_results=self.research_submissions(run_id))
        visited.append(out["stage"])
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, SYNTHESIS))
        visited.append(out["stage"])
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "author-proper"))
        visited.append(out["stage"])
        out = self.pass_stage(run_id, "content-preflight")
        visited.append(out["stage"])
        self.assertEqual(
            visited, [RESEARCH, SYNTHESIS, "author-proper",
                      "content-preflight", "content-evaluation"],
            "the research correction path is fixed by the workflow")

        # Test 23: the second evaluation starts clean. Nothing carries the
        # first one's findings across, and no controller composed a summary.
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertIn("PRIOR_FINDINGS: []", packet)
        self.assertNotIn("CON-EVI-001", packet)
        state = self.engine.load_state(run_id)
        self.assertEqual(state["stage_iterations"]["content-evaluation"], 2)
        self.assertEqual(state["stage_iterations"][RESEARCH], 2)
        self.assertEqual(state["stage_failures"]["content-evaluation"], 1,
                         "the loop is bounded by the evaluator's own budget")

    def test_the_controller_is_never_asked_to_choose_the_route(self):
        """Test 19, in the guidance the controller is given."""
        run_id = self.drive_to("content-evaluation")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        for stage in workflow["stages"]:
            compiled = self.engine._compile_stage_packets(
                workflow, stage, state, self.engine.run_dir(run_id), [])
            text = self.engine._driver_instructions(
                workflow, stage, state, compiled)
            with self.subTest(stage=stage["id"]):
                lowered = text.lower()
                self.assertTrue(text.startswith("EXECUTION POLICY: "))
                # Nothing hands a decision back. "summarize" is deliberately
                # not banned outright: the fan-out guidance forbids it, and a
                # prohibition is the opposite of a request.
                for phrase in ("decide which", "choose the route",
                               "route the", "if the finding", "as appropriate",
                               "where useful", "if useful",
                               "consider delegating"):
                    self.assertNotIn(phrase, lowered)
                if "--lane-result" in text:
                    self.assertIn("do not summarize, merge, reconcile, "
                                  "reorder, or edit any lane result", lowered)

    def test_the_loop_is_bounded_by_the_evaluators_own_budget(self):
        """Three consecutive research routes exhaust content-evaluation."""
        run_id = self.drive_to("content-evaluation")
        research = {"evidence-discipline": [blocking("CON-EVI-001", RESEARCH)]}
        for expected in (RESEARCH, RESEARCH):
            out = self.engine.advance(
                run_id,
                lane_results=self.content_submissions(run_id, research))
            self.assertEqual(out["stage"], expected)
            self.engine.advance(
                run_id, lane_results=self.research_submissions(run_id))
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, SYNTHESIS))
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, "author-proper"))
            self.pass_stage(run_id, "content-preflight")
        out = self.engine.advance(
            run_id, lane_results=self.content_submissions(run_id, research))
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn("iteration limit exceeded", out["message"])


# ---------------------------------------------------------------------------
# 24-33. What must not have moved
# ---------------------------------------------------------------------------

class PreservedGuaranteeTests(RoutingCase):
    """Test 24-33."""

    def test_author_proper_still_reads_the_brief_and_may_not_write_it(self):
        """Test 24."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertEqual(stages["author-proper"]["execution"],
                         {"mode": SINGLE})
        text = (FRAGMENTS / "propers" / "author-proper.md").read_text("utf-8")
        self.assertRegex(text, re.compile(r"immutable|read-only", re.I))

    def test_the_evaluation_fanouts_are_still_host_max(self):
        """Test 25 and 26."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        for stage_id, lanes in (("content-evaluation", CONTENT_LANES),
                                ("visual-evaluation", VISUAL_LANES)):
            with self.subTest(stage=stage_id):
                execution = stages[stage_id]["execution"]
                self.assertEqual(execution["mode"], FANOUT)
                self.assertEqual(execution["parallelism"], HOST_MAX)
                self.assertEqual([l["id"] for l in execution["lanes"]], lanes)

    def test_visual_evaluation_declares_no_repair_routes(self):
        """A visual defect has one owner, so it needs no classification."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertNotIn("repair_routes", stages["visual-evaluation"])
        self.assertEqual(stages["visual-evaluation"]["result_schema"],
                         "evaluator-result.json")
        self.assertEqual(stages["content-evaluation"]["result_schema"],
                         "content-evaluation-result.json")

    def test_the_gates_are_still_programmatic(self):
        """Test 27 and 28."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        for stage_id in ("scope-gate", "mechanical-gates", "final-acceptance",
                         "publication-gates"):
            with self.subTest(stage=stage_id):
                self.assertEqual(stages[stage_id]["type"], "gate")
                self.assertEqual(stages[stage_id]["execution"],
                                 {"mode": PROGRAM})
        accepting = [s for s in workflow_json()["stages"]
                     if ACCEPTED in (s.get("next"), s.get("pass_transition"))]
        self.assertEqual([s["id"] for s in accepting], ["publication-gates"])

    def test_seed_remains_byte_idempotent(self):
        """Test 29 and 32."""
        args = {"proper": DOC, "provider": "gpt"}
        first = self.engine.seed_bytes("proper", args)
        run_id = json.loads(first)["run_id"]
        run_dir = self.engine.run_dir(run_id)
        before = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                  for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(self.engine.seed_bytes("proper", args), first)
        after = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                 for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(json.loads(first)["workflow_version"],
                         workflow_json()["version"])

        # And still after the run has been through the whole research loop.
        out = {"stage": "seed"}
        while out.get("stage") != "content-evaluation":
            state = self.engine.load_state(run_id)
            stage_id = state["current_stage"]
            if stage_id == RESEARCH:
                out = self.engine.advance(
                    run_id, lane_results=self.research_submissions(run_id))
            else:
                out = self.pass_stage(run_id, stage_id)
        self.engine.advance(run_id, lane_results=self.content_submissions(
            run_id, {"evidence-discipline": [blocking("CON-EVI-001",
                                                      RESEARCH)]}))
        self.assertEqual(self.engine.seed_bytes("proper", args), first)

    def test_a_failed_routing_advance_changes_nothing(self):
        """Test 30."""
        run_id = self.drive_to("content-evaluation")
        submissions = self.content_submissions(
            run_id, {"evidence-discipline": [blocking("CON-EVI-001",
                                                      RESEARCH)]})
        before = self.authoritative(run_id)
        packets = self.runs / run_id / "packets"
        os.chmod(packets, 0o500)
        self.addCleanup(os.chmod, packets, 0o755)
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, lane_results=submissions)
        os.chmod(packets, 0o755)
        self.assertEqual(self.authoritative(run_id), before)
        retried = self.engine.advance(run_id, lane_results=submissions)
        self.assertEqual(retried["stage"], RESEARCH)

    def test_a_rejected_evaluation_stays_non_authoritative(self):
        """Test 31."""
        run_id = self.drive_to("content-evaluation")
        before = self.authoritative(run_id)
        replay_before = self.engine.replay(run_id)
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {e["lane"]: e for e in packet["lanes"]}
        pairs = self.content_submissions(run_id)
        pairs[0] = (CONTENT_LANES[0], self.write("unowned", {
            "stage": "content-evaluation", "iteration": packet["iteration"],
            "lane": CONTENT_LANES[0],
            "lane_packet_hash": emitted[CONTENT_LANES[0]]["hash"],
            "disposition": CHANGES_REQUIRED, "summary": "judged",
            "findings": [{"id": "CON-001", "severity": "blocking",
                          "location": "p1", "problem": "x",
                          "required_result": "y"}],
        }))
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, lane_results=pairs)
        self.assertEqual(self.authoritative(run_id), before)
        self.assertEqual(self.engine.replay(run_id), replay_before)


class DeclarationOrderTests(unittest.TestCase):
    """Priority is the order the workflow declares, not the names it uses.

    On the propers pipeline `research` is both declared first and the owner a
    reader would guess wins, so those two rules are indistinguishable there.
    An implementation that hardcoded the names passed every propers test. This
    pipeline declares `authoring` first, so only the declared order can be
    right.
    """

    ROUTED_SCHEMA = "routed-result.json"

    def make_routed_repo(self, routes: list | None = None,
                         admitted: list | None = None,
                         stage_id: str = "eval-stage") -> Path:
        workflow = copy.deepcopy(WORKFLOW)
        for stage in workflow["stages"]:
            if stage["id"] == stage_id:
                stage["result_schema"] = self.ROUTED_SCHEMA
                stage[REPAIR_ROUTES] = routes if routes is not None else [
                    {REPAIR_TARGET: AUTHORING, "transition": "revise-stage"},
                    {REPAIR_TARGET: RESEARCH, "transition": "stage-a"},
                ]
        repo = make_repo(workflow)
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        values = [AUTHORING, RESEARCH] if admitted is None else admitted
        (repo / "workflows" / "schema" / self.ROUTED_SCHEMA).write_text(
            json.dumps({
                "name": "routed-result",
                "required_fields": ["stage", "iteration", "disposition",
                                    "findings"],
                "valid_dispositions": [PASS, CHANGES_REQUIRED, BLOCKED],
                "finding_fields": ["id", "severity", "location", "problem",
                                   "required_result"],
                "blocking_finding_fields": [REPAIR_TARGET],
                "finding_enums": {
                    "severity": ["blocking", "advisory"],
                    REPAIR_TARGET: values,
                },
            }, sort_keys=True, indent=2), encoding="utf-8")
        return repo

    def drive_to_eval(self, repo: Path):
        engine = engine_for(repo)
        out = engine.seed("adv-wf", {"doc": "d1", "provider": "gpt"})
        run_id = out["run_id"]
        while out["stage"] != "eval-stage":
            packet = engine.load_state(run_id)["packet_hashes"][-1]
            path = repo / f"w-{packet['stage']}.json"
            path.write_text(json.dumps({
                "stage": packet["stage"], "iteration": packet["iteration"],
                "disposition": PASS, "summary": "done"}), encoding="utf-8")
            out = engine.advance(run_id, result_path=str(path))
        return engine, run_id

    def submit(self, engine, repo: Path, run_id: str, findings: list) -> dict:
        packet = engine.load_state(run_id)["packet_hashes"][-1]
        path = repo / "eval.json"
        path.write_text(json.dumps({
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": CHANGES_REQUIRED, "summary": "judged",
            "findings": findings}), encoding="utf-8")
        return engine.advance(run_id, result_path=str(path))

    def test_the_first_declared_route_wins_not_the_first_named(self):
        repo = self.make_routed_repo()
        engine, run_id = self.drive_to_eval(repo)
        out = self.submit(engine, repo, run_id, [
            blocking("R-1", RESEARCH), blocking("A-1", AUTHORING)])
        self.assertEqual(
            out["stage"], "revise-stage",
            "`authoring` is declared first here, so it wins; a rule that "
            "preferred the name `research` would send this to stage-a")

    def test_finding_order_within_a_result_does_not_matter(self):
        for order in ([blocking("A-1", AUTHORING), blocking("R-1", RESEARCH)],
                      [blocking("R-1", RESEARCH), blocking("A-1", AUTHORING)]):
            with self.subTest(first=order[0]["repair_target"]):
                repo = self.make_routed_repo()
                engine, run_id = self.drive_to_eval(repo)
                out = self.submit(engine, repo, run_id, order)
                self.assertEqual(out["stage"], "revise-stage")

    def test_the_lower_priority_route_still_fires_alone(self):
        repo = self.make_routed_repo()
        engine, run_id = self.drive_to_eval(repo)
        out = self.submit(engine, repo, run_id, [blocking("R-1", RESEARCH)])
        self.assertEqual(out["stage"], "stage-a")
        forwarded = json.loads(
            [line for line in Path(out["packet_abs_path"])
             .read_text(encoding="utf-8").splitlines()
             if line.startswith("PRIOR_FINDINGS: ")][0][len("PRIOR_FINDINGS: "):])
        self.assertEqual([f["id"] for f in forwarded], ["R-1"])

    def test_a_malformed_route_declaration_fails_closed(self):
        cases = {
            "not-a-list": ({}, "must be a nonempty list"),
            "empty": ([], "must be a nonempty list"),
            "extra-key": ([{REPAIR_TARGET: AUTHORING,
                            "transition": "revise-stage", "why": "no"}],
                          "declares exactly"),
            "missing-transition": ([{REPAIR_TARGET: AUTHORING}],
                                   "declares exactly"),
            "empty-target": ([{REPAIR_TARGET: "", "transition": "stage-a"},
                              {REPAIR_TARGET: RESEARCH,
                               "transition": "stage-a"}],
                             "must be a nonempty string"),
            "duplicate": ([{REPAIR_TARGET: AUTHORING,
                            "transition": "stage-a"},
                           {REPAIR_TARGET: AUTHORING,
                            "transition": "revise-stage"}],
                          "duplicate repair target"),
            "unknown-stage": ([{REPAIR_TARGET: AUTHORING,
                                "transition": "no-such-stage"},
                               {REPAIR_TARGET: RESEARCH,
                                "transition": "stage-a"}],
                              "points to unknown stage"),
        }
        for name, (routes, message) in cases.items():
            with self.subTest(case=name):
                repo = self.make_routed_repo(routes=routes)
                with self.assertRaises(WorkflowError) as caught:
                    engine_for(repo).load_workflow("adv-wf")
                self.assertIn(message, str(caught.exception))

    def test_only_an_evaluator_may_route_a_repair(self):
        repo = self.make_routed_repo(stage_id="stage-a")
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("only an evaluator stage may declare", str(caught.exception))

    def test_a_route_may_not_name_accepted(self):
        repo = self.make_routed_repo(routes=[
            {REPAIR_TARGET: AUTHORING, "transition": ACCEPTED},
            {REPAIR_TARGET: RESEARCH, "transition": "stage-a"}])
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("only a gate stage may accept a run",
                      str(caught.exception))

    def test_the_schema_and_the_routes_must_name_the_same_owners(self):
        # A value the schema admits with no route would fall through to
        # fail_transition in silence.
        repo = self.make_routed_repo(admitted=[AUTHORING, RESEARCH, "layout"])
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("every value a finding may carry needs a route",
                      str(caught.exception))

        # And a route for a value the schema rejects can never fire.
        repo = self.make_routed_repo(admitted=[AUTHORING])
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("every value a finding may carry needs a route",
                      str(caught.exception))

    def test_a_routed_stage_must_enumerate_its_owners(self):
        workflow = copy.deepcopy(WORKFLOW)
        for stage in workflow["stages"]:
            if stage["id"] == "eval-stage":
                stage[REPAIR_ROUTES] = [
                    {REPAIR_TARGET: AUTHORING, "transition": "revise-stage"},
                    {REPAIR_TARGET: RESEARCH, "transition": "stage-a"}]
        repo = make_repo(workflow)  # keeps the plain evaluator-result schema
        self.addCleanup(shutil.rmtree, repo, ignore_errors=True)
        with self.assertRaises(WorkflowError) as caught:
            engine_for(repo).load_workflow("adv-wf")
        self.assertIn("must enumerate the values of repair_target",
                      str(caught.exception))


class RealWorkflowCoverageTests(unittest.TestCase):
    """The propers workflow's own two lists, held to each other.

    `DeclarationOrderTests` proves the rule on a synthetic workflow. This
    proves it where it is load-bearing: the enum in
    `content-evaluation-result.json` and the routes in `proper.json` are two
    lists in two files that nothing but this rule keeps agreed, and the third
    owner had to be added to both at once.
    """

    OWNERS = [RESEARCH, BRIEF, AUTHORING]

    def schema_path(self, root: Path) -> Path:
        return root / "schema" / "content-evaluation-result.json"

    def pipeline_path(self, root: Path) -> Path:
        return root / "pipelines" / "proper.json"

    def copy_workflows(self) -> Path:
        copied = Path(tempfile.mkdtemp()) / "workflows"
        shutil.copytree(ROOT / "workflows", copied)
        self.addCleanup(shutil.rmtree, copied.parent, ignore_errors=True)
        return copied

    def load(self, root: Path):
        return WorkflowEngine(ROOT, root).load_workflow("proper")

    def test_the_enum_and_the_routes_name_the_same_owners(self):
        schema = json.loads(
            self.schema_path(ROOT / "workflows").read_text(encoding="utf-8"))
        self.assertEqual(schema["finding_enums"][REPAIR_TARGET], self.OWNERS)
        stage = {s["id"]: s for s in workflow_json()["stages"]}[
            "content-evaluation"]
        self.assertEqual([r[REPAIR_TARGET] for r in stage[REPAIR_ROUTES]],
                         self.OWNERS)
        # Loading the real workflow is itself the coverage check running.
        self.load(ROOT / "workflows")

    def test_an_owner_the_schema_admits_with_no_route_refuses_the_workflow(self):
        root = self.copy_workflows()
        path = self.schema_path(root)
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["finding_enums"][REPAIR_TARGET] = self.OWNERS + ["layout"]
        path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        with self.assertRaises(WorkflowError) as caught:
            self.load(root)
        self.assertIn("every value a finding may carry needs a route",
                      str(caught.exception))

    def test_a_route_for_an_owner_the_schema_rejects_refuses_the_workflow(self):
        root = self.copy_workflows()
        path = self.pipeline_path(root)
        workflow = json.loads(path.read_text(encoding="utf-8"))
        for stage in workflow["stages"]:
            if stage["id"] == "content-evaluation":
                stage[REPAIR_ROUTES] = [
                    route for route in stage[REPAIR_ROUTES]
                    if route[REPAIR_TARGET] != BRIEF]
        path.write_text(json.dumps(workflow, indent=2), encoding="utf-8")
        with self.assertRaises(WorkflowError) as caught:
            self.load(root)
        self.assertIn("every value a finding may carry needs a route",
                      str(caught.exception))

    def test_dropping_brief_from_both_files_at_once_still_loads(self):
        """The two lists move together, or not at all.

        Without this the two tests above would pass for a workflow that had
        simply lost the owner, and the rule they hold would read as a
        prohibition on changing the enum rather than on changing one of them.
        """
        root = self.copy_workflows()
        path = self.schema_path(root)
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema["finding_enums"][REPAIR_TARGET] = [RESEARCH, AUTHORING]
        path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        path = self.pipeline_path(root)
        workflow = json.loads(path.read_text(encoding="utf-8"))
        for stage in workflow["stages"]:
            if stage["id"] == "content-evaluation":
                stage[REPAIR_ROUTES] = [
                    route for route in stage[REPAIR_ROUTES]
                    if route[REPAIR_TARGET] != BRIEF]
        path.write_text(json.dumps(workflow, indent=2), encoding="utf-8")
        loaded = {s["id"]: s for s in self.load(root)["stages"]}
        self.assertEqual(
            [r[REPAIR_TARGET]
             for r in loaded["content-evaluation"][REPAIR_ROUTES]],
            [RESEARCH, AUTHORING])


class LauncherTests(unittest.TestCase):
    """Test 33."""

    def tpt(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                              text=True, cwd=ROOT)

    def test_registered_tool_dispatch_is_unchanged(self):
        self.assertEqual(self.tpt("--check").returncode, 0)
        parsed = self.tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)

    def test_the_routes_are_visible_in_the_definition(self):
        shown = self.tpt("workflow", "show", "proper")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        stages = {s["id"]: s for s in json.loads(shown.stdout)["stages"]}
        self.assertEqual(stages["content-evaluation"]["repair_routes"], [
            {"repair_target": RESEARCH, "transition": RESEARCH},
            {"repair_target": BRIEF, "transition": SYNTHESIS},
            {"repair_target": AUTHORING, "transition": "content-revision"},
        ])


if __name__ == "__main__":
    unittest.main()
