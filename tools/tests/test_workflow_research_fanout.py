#!/usr/bin/env python3
"""Independent discovery fans out; synthesis and mutation keep one owner.

The propers workflow used to ask one worker to sweep the whole reception
field and then distil it, so the broadest independent work in the pipeline
ran at a concurrency of one. The sweep is now a `research` stage of five
read-only lanes at host maximum, and the distillation that follows is still a
single owner. These tests hold both halves of that: that the discovery really
does fan out over exactly the lanes the workflow declares, and that nothing
which writes the document ever does.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))

from _workflow import (  # noqa: E402
    ACCEPTED,
    BLOCKED,
    FANOUT,
    HOST_MAX,
    PASS,
    PROGRAM,
    SINGLE,
    STRICT_UNION,
    WorkflowEngine,
    WorkflowError,
)

def _probe_document() -> str:
    """A real proper to drive runs against.

    Taken from the workflow's own discovery rather than written down: the
    corpus renumbers — every Sunday after Pentecost shifted by three when the
    Sacred Triduum was numbered inline — and a literal id here would pin the
    suite to whichever numbering happened to be current when it was written.
    """
    engine = WorkflowEngine(ROOT, ROOT / "workflows")
    documents = engine.list_documents(engine.load_workflow("proper"))
    for document in documents:
        if document.endswith("-ninth-after-pentecost"):
            return document
    return documents[0]


DOC = _probe_document()

RESEARCH_LANES = [
    "scripture-context",
    "patristic-reception",
    "liturgical-history",
    "theological-synthesis",
    "source-citation-coverage",
    "cultural-afterlife",
    "precedent-search",
]
LANE_PREFIX = {
    "scripture-context": "SCR",
    "patristic-reception": "PAT",
    "liturgical-history": "LIT",
    "theological-synthesis": "THE",
    "source-citation-coverage": "COV",
    "cultural-afterlife": "CUL",
    "precedent-search": "PRE",
}

# The two evaluation fan-outs, which the research stage must not disturb.
CONTENT_LANES = [
    "evidence-discipline", "reception-sweep", "synthesis-argument",
    "citation-integrity", "profile-conformance",
]
VISUAL_LANES = [
    "density-and-hierarchy", "page-rhythm", "fixed-pagination",
    "clipping-and-apparatus",
]

# `research` was added at version 4, and a run bound to an earlier version
# has no such stage; it must be told to seed again rather than continue.
RESEARCH_STAGE_VERSION = 4

SINGLE_OWNER = {
    "seed", "resolve-context", "source-audit", "research-synthesis",
    "author-proper", "content-revision", "build-artifacts",
    "artifact-revision", "visual-revision",
}
PROGRAM_STAGES = {"mechanical-gates", "final-acceptance"}

# Files a research lane may never be told to touch: the canonical leaf's own
# sources, the built apparatus, and the synthesis brief that the single-owner
# integration stage writes.
FORBIDDEN_IN_LANE_FRAGMENTS = (
    "main.tex", "synthesis.tex", "proper-components.toml",
    "web-edition.toml", "generation-metadata", "research/scope.md",
)

FRAGMENTS = ROOT / "workflows" / "fragments"

# Every lane's finding-id prefix, keyed by the fragment that declares it. Two
# lanes reaching for the same prefix would claim the same finding space, and
# the join would have no way to say whose finding a collision was.
FRAGMENT_PREFIX = {
    **{f"research-{lane}": f"{LANE_PREFIX[lane]}-" for lane in RESEARCH_LANES},
    "content-evidence-discipline": "CON-EVI-",
    "content-reception-sweep": "CON-REC-",
    "content-synthesis-argument": "CON-SYN-",
    "content-citation-integrity": "CON-CIT-",
    "content-profile-conformance": "CON-PRO-",
    "visual-density-and-hierarchy": "VIS-DEN-",
    "visual-page-rhythm": "VIS-RHY-",
    "visual-fixed-pagination": "VIS-FIX-",
    "visual-clipping-and-apparatus": "VIS-APP-",
}


def assert_lane_owns_its_findings(case: unittest.TestCase,
                                  fragment: str) -> None:
    """A lane fragment claims one finding space and one slice of the work.

    What keeps two lanes from reporting the same defect twice, or from
    leaving a criterion to each other, was never their exact bytes: it is
    that each declares the finding-id prefix it alone uses, names no other
    lane's, and tells its worker in as many words that the rest belongs to
    someone else.
    """
    path = FRAGMENTS / "propers" / "lanes" / f"{fragment}.md"
    case.assertTrue(path.is_file(), f"{fragment}.md is missing")
    text = path.read_text(encoding="utf-8")
    case.assertTrue(text.strip(), f"{fragment}.md is empty")

    prefix = FRAGMENT_PREFIX[fragment]
    case.assertIn(f"`{prefix}` prefix", text,
                  f"{fragment} must declare the finding-id prefix it owns")
    for foreign in sorted(set(FRAGMENT_PREFIX.values()) - {prefix}):
        case.assertNotIn(
            foreign, text,
            f"{fragment} names {foreign}, the finding space of another lane")

    # The fragments are hard-wrapped, so the claim routinely spans lines.
    flat = " ".join(text.split())
    case.assertRegex(flat, r"You own .+?, and nothing else\.",
                     f"{fragment} must name the scope it owns, and stop")
    case.assertRegex(flat, r"Another lane owns .+?; do not report on",
                     f"{fragment} must say another lane owns the rest")


def workflow_json() -> dict:
    return json.loads(
        (ROOT / "workflows" / "pipelines" / "proper.json")
        .read_text(encoding="utf-8"))


class PropersCase(unittest.TestCase):
    """Drives the real propers workflow inside a private run directory."""

    def setUp(self):
        name = self.id().rsplit(".", 1)[-1]
        self.runs = ROOT / "build" / f"tpt-runs-research-{os.getpid()}-{name}"
        shutil.rmtree(self.runs, ignore_errors=True)
        self.runs.mkdir(parents=True, exist_ok=True)
        self.addCleanup(shutil.rmtree, self.runs, ignore_errors=True)
        self.engine = WorkflowEngine(ROOT, ROOT / "workflows")
        self.engine.runs_dir = self.runs
        self.answers = self.runs / "answers"
        self.answers.mkdir(parents=True, exist_ok=True)

    # --- helpers ---

    def seed(self) -> dict:
        return self.engine.seed("proper", {"proper": DOC, "provider": "gpt"})

    def discard_runs(self) -> None:
        """Drop the run tree so the same deterministic run can be seeded again."""
        for path in self.runs.iterdir():
            if path != self.answers:
                shutil.rmtree(path, ignore_errors=True)

    def write(self, name: str, body: dict) -> str:
        path = self.answers / f"{name}.json"
        path.write_text(json.dumps(body), encoding="utf-8")
        return str(path)

    def worker_pass(self, run_id: str, name: str) -> str:
        """A passing single-agent result for whatever stage is waiting.

        `findings` is always present: a worker schema ignores it, and an
        evaluator schema requires it. `research-synthesis` is an evaluator
        that also writes an artifact, so one shape answers both.
        """
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        return self.write(name, {
            "stage": packet["stage"], "iteration": packet["iteration"],
            "disposition": PASS, "summary": "probe", "findings": [],
            "artifact_path": "research/scope.md",
        })

    def advance_to(self, target: str) -> tuple[str, dict]:
        """Seed and drive single stages until the run reaches target."""
        out = self.seed()
        run_id = out["run_id"]
        for _ in range(12):
            if out["stage"] == target:
                return run_id, out
            out = self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, out["stage"]))
        self.fail(f"could not reach {target}")

    def emitted_lanes(self, run_id: str) -> list[dict]:
        return self.engine.load_state(run_id)["packet_hashes"][-1]["lanes"]

    def lane_body(self, run_id: str, lane: str, disposition: str = PASS,
                  findings: list | None = None, **overrides) -> dict:
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        emitted = {entry["lane"]: entry for entry in packet.get("lanes", [])}
        prefix = LANE_PREFIX.get(lane, "XXX")
        body = {
            "stage": packet["stage"],
            "iteration": packet["iteration"],
            "lane": lane,
            "lane_packet_hash": emitted.get(lane, {}).get("hash", "0" * 64),
            "disposition": disposition,
            "summary": f"{lane} swept its field",
            "findings": findings if findings is not None else [{
                "id": f"{prefix}-001",
                "claim": f"a claim from {lane}",
                "evidence": [f"a source {lane} checked"],
                "notes": f"what {lane} is unsure of",
            }],
        }
        body.update(overrides)
        return body

    def lane_submissions(self, run_id: str, order: list[str] | None = None,
                         **kwargs) -> list[tuple[str, str]]:
        return [
            (lane, self.write(f"lane-{lane}",
                              self.lane_body(run_id, lane, **kwargs)))
            for lane in (order if order is not None else RESEARCH_LANES)
        ]

    def authoritative(self, run_id: str) -> dict:
        state = self.engine.load_state(run_id)
        results = self.runs / run_id / "results"
        return {
            "current_stage": state["current_stage"],
            "disposition": state["disposition"],
            "packet_hashes": state["packet_hashes"],
            "result_hashes": state["result_hashes"],
            "transitions": state["transitions"],
            "recorded": sorted(p.name for p in results.iterdir())
            if results.is_dir() else [],
        }

    def refuse(self, run_id: str, submissions: list[tuple[str, str]],
               message: str) -> None:
        before = self.authoritative(run_id)
        replay_before = self.engine.replay(run_id)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submissions)
        self.assertIn(message, str(caught.exception))
        self.assertEqual(self.authoritative(run_id), before,
                         "a refused research submission leaves no trace")
        self.assertEqual(self.engine.replay(run_id), replay_before)


# ---------------------------------------------------------------------------
# 1-6, 24-25. Workflow topology
# ---------------------------------------------------------------------------

class TopologyTests(unittest.TestCase):
    """Test 1-6 and 24-25: who runs what, and what must not have moved."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = workflow_json()
        cls.stages = {s["id"]: s for s in cls.workflow["stages"]}

    def test_research_is_fanout_host_max(self):
        """Test 1."""
        research = self.stages["research"]
        self.assertEqual(research["type"], "linear")
        self.assertEqual(research["execution"]["mode"], FANOUT)
        self.assertEqual(research["execution"]["parallelism"], HOST_MAX)
        self.assertEqual(research["execution"]["join"], STRICT_UNION)

    def test_exactly_the_declared_research_lanes(self):
        """Test 2."""
        lanes = self.stages["research"]["execution"]["lanes"]
        self.assertEqual([lane["id"] for lane in lanes], RESEARCH_LANES)
        self.assertEqual(len(lanes), 7)
        for lane in lanes:
            with self.subTest(lane=lane["id"]):
                self.assertEqual(
                    lane["fragments"],
                    [f"propers/lanes/research-{lane['id']}.md"])
                self.assertTrue(
                    (FRAGMENTS / lane["fragments"][0]).is_file())

    def test_research_synthesis_is_single(self):
        """Test 3."""
        self.assertEqual(
            self.stages["research-synthesis"]["execution"], {"mode": SINGLE})

    def test_author_proper_is_single(self):
        """Test 4."""
        self.assertEqual(
            self.stages["author-proper"]["execution"], {"mode": SINGLE})

    def test_source_audit_is_single(self):
        """Test 5."""
        self.assertEqual(
            self.stages["source-audit"]["execution"], {"mode": SINGLE})

    def test_program_gates_remain_program(self):
        """Test 6."""
        for stage_id in PROGRAM_STAGES:
            with self.subTest(stage=stage_id):
                stage = self.stages[stage_id]
                self.assertEqual(stage["type"], "gate")
                self.assertEqual(stage["execution"], {"mode": PROGRAM})

    def test_every_single_owner_stage_is_still_single(self):
        for stage_id in SINGLE_OWNER:
            with self.subTest(stage=stage_id):
                self.assertEqual(self.stages[stage_id]["execution"],
                                 {"mode": SINGLE})

    def test_the_research_chain_is_wired_in_order(self):
        self.assertEqual(self.stages["source-audit"]["next"], "research")
        self.assertEqual(self.stages["research"]["next"], "research-synthesis")
        # research-synthesis is an evaluator now: passing goes on to
        # authoring, asking for more goes back to research.
        self.assertEqual(self.stages["research-synthesis"]["pass_transition"],
                         "author-proper")
        self.assertEqual(self.stages["research-synthesis"]["fail_transition"],
                         "research")
        self.assertEqual(self.stages["author-proper"]["next"],
                         "content-evaluation")

    def test_research_uses_the_research_result_schema(self):
        self.assertEqual(self.stages["research"]["result_schema"],
                         "research-result.json")
        schema = json.loads(
            (ROOT / "workflows" / "schema" / "research-result.json")
            .read_text(encoding="utf-8"))
        self.assertEqual(schema["valid_dispositions"], [PASS, BLOCKED],
                         "a research lane either swept or could not")
        self.assertEqual(schema["finding_fields"],
                         ["id", "claim", "evidence", "notes"])

    def test_the_workflow_version_matches_the_operator_manual(self):
        """A run is bound to a version, so the manual must state the real one.

        Adding `research` required a bump, and that is the floor asserted
        here rather than whatever number is current; what this really guards
        is that a later bump cannot land while the manual still names the
        version before it, since the manual is what an operator reads to
        decide whether a run in hand must be seeded again.
        """
        version = self.workflow["version"]
        self.assertIsInstance(version, int)
        self.assertGreaterEqual(
            version, RESEARCH_STAGE_VERSION,
            "a run bound to a version before `research` existed must fail "
            "closed, so the pipeline may never go back below that bump")
        stated = re.search(
            r"The `proper` workflow is at version (\d+)\.",
            (ROOT / "workflows" / "OPERATOR.md").read_text(encoding="utf-8"))
        self.assertIsNotNone(stated,
                             "OPERATOR.md must state the workflow version")
        self.assertEqual(int(stated.group(1)), version,
                         "OPERATOR.md states a version the pipeline does not")

    def test_content_evaluation_fanout_is_unchanged(self):
        """Test 24."""
        execution = self.stages["content-evaluation"]["execution"]
        self.assertEqual(execution["mode"], FANOUT)
        self.assertEqual(execution["parallelism"], HOST_MAX)
        self.assertEqual(execution["join"], STRICT_UNION)
        self.assertEqual([lane["id"] for lane in execution["lanes"]],
                         CONTENT_LANES)
        self.assertEqual(self.stages["content-evaluation"]["type"],
                         "evaluator")

    def test_visual_evaluation_fanout_is_unchanged(self):
        """Test 25."""
        execution = self.stages["visual-evaluation"]["execution"]
        self.assertEqual(execution["mode"], FANOUT)
        self.assertEqual(execution["parallelism"], HOST_MAX)
        self.assertEqual(execution["join"], STRICT_UNION)
        self.assertEqual([lane["id"] for lane in execution["lanes"]],
                         VISUAL_LANES)
        self.assertEqual(self.stages["visual-evaluation"]["type"], "evaluator")

    def test_only_the_research_stage_was_added(self):
        self.assertEqual(
            [stage["id"] for stage in self.workflow["stages"]],
            ["seed", "resolve-context", "source-audit", "research",
             "research-synthesis", "author-proper", "content-evaluation",
             "content-revision", "build-artifacts", "mechanical-gates",
             "artifact-revision", "visual-evaluation", "visual-revision",
             "final-acceptance"])


# ---------------------------------------------------------------------------
# 7-14. Lane determinism and fail-closed binding
# ---------------------------------------------------------------------------

class ResearchLaneTests(PropersCase):
    """Test 7-14: lane identity is state, and the join is all or nothing."""

    def test_lane_ids_and_order_are_deterministic(self):
        """Test 7."""
        run_id, _ = self.advance_to("research")
        first = self.emitted_lanes(run_id)
        self.discard_runs()
        run_id, _ = self.advance_to("research")
        second = self.emitted_lanes(run_id)
        self.assertEqual([lane["lane"] for lane in first], RESEARCH_LANES)
        self.assertEqual([lane["index"] for lane in first],
                         list(range(len(RESEARCH_LANES))))
        self.assertEqual(first, second)

    def test_identical_state_produces_byte_identical_lane_packets(self):
        """Test 8."""
        run_id, _ = self.advance_to("research")
        first = {lane["lane"]: (ROOT / lane["path"]).read_bytes()
                 for lane in self.emitted_lanes(run_id)}
        for lane in self.emitted_lanes(run_id):
            self.assertEqual(
                hashlib.sha256((ROOT / lane["path"]).read_bytes()).hexdigest(),
                lane["hash"])
        self.discard_runs()
        run_id, _ = self.advance_to("research")
        second = {lane["lane"]: (ROOT / lane["path"]).read_bytes()
                  for lane in self.emitted_lanes(run_id)}
        self.assertEqual(first, second)

    def test_each_lane_packet_carries_only_its_own_lane_guidance(self):
        run_id, _ = self.advance_to("research")
        for lane in self.emitted_lanes(run_id):
            text = (ROOT / lane["path"]).read_text(encoding="utf-8")
            header = text.split("\n\n", 1)[0].splitlines()
            self.assertIn(f"EXECUTION: {FANOUT}/{HOST_MAX}", header)
            self.assertIn(f"LANE: {lane['lane']}", header)
            self.assertIn(f"LANE_INDEX: {lane['index']}", header)
            self.assertIn(
                f"--- FRAGMENT: propers/lanes/research-{lane['lane']}.md ---",
                text)
            for other in RESEARCH_LANES:
                if other != lane["lane"]:
                    self.assertNotIn(
                        f"--- FRAGMENT: propers/lanes/research-{other}.md ---",
                        text,
                        "a lane packet exposes no other lane's instructions")

    def test_completion_order_does_not_change_the_joined_research(self):
        """Test 9 and 10."""
        def drive(order: list[str]) -> dict:
            run_id, _ = self.advance_to("research")
            out = self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id, order))
            state = self.engine.load_state(run_id)
            joined = state["result_hashes"][-1]
            return {
                "next_stage": out["stage"],
                "successor_packet_hash": out["packet_hash"],
                "joined_result_hash": joined["hash"],
                "joined_bytes": (ROOT / joined["path"]).read_bytes(),
                "lane_order": [lane["lane"] for lane in joined["lanes"]],
            }

        declared = drive(RESEARCH_LANES)
        self.discard_runs()
        # No lane finishes where the workflow declared it.
        scrambled = drive([
            "precedent-search", "liturgical-history",
            "source-citation-coverage", "cultural-afterlife",
            "scripture-context", "theological-synthesis",
            "patristic-reception",
        ])
        self.assertEqual(sorted(scrambled["lane_order"]),
                         sorted(RESEARCH_LANES))

        self.assertEqual(declared["next_stage"], "research-synthesis")
        self.assertEqual(declared, scrambled,
                         "neither the joined research nor the successor "
                         "packet may depend on completion order")
        self.assertEqual(declared["lane_order"], RESEARCH_LANES)

        body = json.loads(declared["joined_bytes"].decode("utf-8"))
        self.assertEqual(body["disposition"], PASS)
        self.assertEqual([finding["lane"] for finding in body["findings"]],
                         RESEARCH_LANES)
        self.assertEqual([finding["id"] for finding in body["findings"]],
                         [f"{LANE_PREFIX[lane]}-001"
                          for lane in RESEARCH_LANES])

    def test_lane_findings_are_preserved_verbatim(self):
        run_id, _ = self.advance_to("research")
        finding = {
            "id": "PAT-042", "claim": "a claim worth keeping",
            "evidence": ["Ambrose, Expositio in Ps. 118 (CSEL 62)"],
            "notes": "the attribution is contested",
        }
        submissions = self.lane_submissions(run_id)
        submissions[RESEARCH_LANES.index("patristic-reception")] = (
            "patristic-reception",
            self.write("verbatim", self.lane_body(
                run_id, "patristic-reception", findings=[finding])))
        self.engine.advance(run_id, lane_results=submissions)
        joined = self.engine.load_state(run_id)["result_hashes"][-1]
        body = json.loads((ROOT / joined["path"]).read_text(encoding="utf-8"))
        kept = next(f for f in body["findings"] if f["id"] == "PAT-042")
        tagged = dict(kept)
        self.assertEqual(tagged.pop("lane"), "patristic-reception")
        self.assertEqual(tagged, finding)

    def test_an_undeclared_lane_is_rejected(self):
        """Test 11."""
        run_id, _ = self.advance_to("research")
        extra = self.lane_submissions(run_id) + [
            ("rubrical-forensics", self.write("extra", self.lane_body(
                run_id, "rubrical-forensics")))]
        self.refuse(run_id, extra, "declares no lane 'rubrical-forensics'")

    def test_a_duplicate_lane_is_rejected(self):
        """Test 12."""
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        submissions.append(submissions[2])
        self.refuse(run_id, submissions, "was submitted more than once")

    def test_a_stale_lane_packet_hash_is_rejected(self):
        """Test 13."""
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        index = RESEARCH_LANES.index("liturgical-history")
        submissions[index] = ("liturgical-history", self.write(
            "stale", self.lane_body(run_id, "liturgical-history",
                                    lane_packet_hash="c" * 64)))
        self.refuse(run_id, submissions, "declares packet hash")

    def test_a_result_bound_to_the_wrong_lane_is_rejected(self):
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        index = RESEARCH_LANES.index("scripture-context")
        body = self.lane_body(run_id, "scripture-context")
        body["lane"] = "theological-synthesis"
        submissions[index] = ("scripture-context",
                              self.write("mislabelled", body))
        self.refuse(run_id, submissions,
                    "declares lane 'theological-synthesis'")

    def test_a_missing_lane_prevents_the_join(self):
        """Test 14."""
        for missing in RESEARCH_LANES:
            with self.subTest(missing=missing):
                self.discard_runs()
                run_id, _ = self.advance_to("research")
                partial = [pair for pair in self.lane_submissions(run_id)
                           if pair[0] != missing]
                self.refuse(run_id, partial,
                            f"no result for lane(s) {missing}")

    def test_a_research_lane_cannot_ask_for_revision(self):
        """The schema admits PASS and BLOCKED only; anything else fails."""
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        submissions[0] = (RESEARCH_LANES[0], self.write(
            "changes", self.lane_body(run_id, RESEARCH_LANES[0],
                                      disposition="CHANGES_REQUIRED")))
        self.refuse(run_id, submissions, "invalid disposition")

    def test_one_blocked_lane_blocks_the_stage(self):
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        index = RESEARCH_LANES.index("source-citation-coverage")
        submissions[index] = ("source-citation-coverage", self.write(
            "blocked", self.lane_body(run_id, "source-citation-coverage",
                                      disposition=BLOCKED)))
        out = self.engine.advance(run_id, lane_results=submissions)
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertEqual(self.engine.load_state(run_id)["disposition"],
                         BLOCKED)


# ---------------------------------------------------------------------------
# 15-19, 23. What the controller is told
# ---------------------------------------------------------------------------

class ResearchGuidanceTests(PropersCase):
    """Test 15-19 and 23: five fresh subagents, host maximum, no summarising."""

    def setUp(self):
        super().setUp()
        self.run_id, self.out = self.advance_to("research")
        self.instructions = self.out["instructions"]

    def test_guidance_declares_fanout_host_max(self):
        """Test 15."""
        self.assertTrue(self.instructions.startswith(
            "EXECUTION POLICY: FANOUT / HOST-MAX"))

    def test_guidance_demands_maximum_host_concurrency(self):
        """Test 16."""
        self.assertIn(
            "Use the maximum concurrent subagent capacity supported by this "
            "host.", self.instructions)
        self.assertIn(f"up to all {len(RESEARCH_LANES)} simultaneously",
                      self.instructions)

    def test_guidance_names_exactly_the_declared_lanes(self):
        """Test 17."""
        count = len(RESEARCH_LANES)
        self.assertIn(f"Start exactly {count} fresh subagents, one per lane "
                      f"listed above and none besides.", self.instructions)
        self.assertIn(f"LANES ({count}, in canonical order):",
                      self.instructions)
        for index, lane in enumerate(RESEARCH_LANES):
            self.assertIn(f"  {index}. {lane}", self.instructions)
            self.assertIn(f"--lane-result {lane}=<path>", self.instructions)
        self.assertEqual(self.instructions.count("--lane-result"),
                         len(RESEARCH_LANES))
        for emitted in self.emitted_lanes(self.run_id):
            self.assertIn(f"lane_packet_hash: {emitted['hash']}",
                          self.instructions)

    def test_guidance_forbids_reshaping_the_lane_set(self):
        """Test 18."""
        self.assertIn("Do not invent, omit, combine, or subdivide lanes.",
                      self.instructions)
        self.assertIn("Associate every result with its declared lane id.",
                      self.instructions)

    def test_guidance_specifies_deterministic_batching(self):
        """Test 19."""
        self.assertIn(
            "If all lanes cannot run simultaneously, execute them in "
            "deterministic batches.", self.instructions)
        self.assertIn(
            "If this host supports fewer concurrent subagents than there are "
            "lanes, take the lanes in the canonical order above, run one "
            "batch at the host maximum, then the next batch, until every lane "
            "has completed.", self.instructions)
        self.assertIn("Batching changes no lane id, no lane order, and no "
                      "lane packet byte.", self.instructions)

    def test_the_controller_is_never_asked_to_summarize(self):
        """Test 23."""
        self.assertIn("tpt performs the join itself", self.instructions)
        self.assertIn("Do not summarize, merge, reconcile, reorder, or edit "
                      "any lane result", self.instructions)
        self.assertIn("do not supplement a lane's work yourself",
                      self.instructions)
        self.assertIn("Completion order must not affect result ordering or "
                      "successor guidance.", self.instructions)

    def test_no_stage_guidance_returns_discretion_to_the_host(self):
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(self.run_id)
        for stage in workflow["stages"]:
            with self.subTest(stage=stage["id"]):
                compiled = self.engine._compile_stage_packets(
                    workflow, stage, state,
                    self.engine.run_dir(self.run_id), [])
                text = self.engine._driver_instructions(
                    workflow, stage, state, compiled)
                self.assertTrue(text.startswith("EXECUTION POLICY: "))
                for phrase in ("parallelize as appropriate", "if useful",
                               "as appropriate", "where useful",
                               "consider delegating"):
                    self.assertNotIn(phrase, text.lower())


# ---------------------------------------------------------------------------
# 20-22. The synthesis boundary
# ---------------------------------------------------------------------------

class SynthesisBoundaryTests(PropersCase):
    """Test 20-22: lanes discover, one owner integrates, one owner writes."""

    def test_research_lane_guidance_never_edits_the_document(self):
        """Test 20."""
        shared = (FRAGMENTS / "propers" / "research.md").read_text(
            encoding="utf-8")
        lowered = shared.lower()
        self.assertIn("read-only", lowered,
                      "the shared research fragment states the rule")
        for named in ("verified.md", "retrieved.txt", "research/scope.md"):
            self.assertIn(named, shared,
                          "the shared fragment names what a lane must not "
                          "write")
        for lane in RESEARCH_LANES:
            text = (FRAGMENTS / "propers" / "lanes"
                    / f"research-{lane}.md").read_text(encoding="utf-8")
            for token in FORBIDDEN_IN_LANE_FRAGMENTS:
                with self.subTest(lane=lane, token=token):
                    self.assertNotIn(
                        token, text,
                        f"the {lane} lane names {token}, which only a "
                        f"single-owner stage may touch")

    def test_the_joined_research_reaches_research_synthesis(self):
        """Test 21."""
        run_id, _ = self.advance_to("research")
        out = self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.assertEqual(out["stage"], "research-synthesis")
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        line = next(l for l in packet.splitlines()
                    if l.startswith("PRIOR_FINDINGS: "))
        forwarded = json.loads(line[len("PRIOR_FINDINGS: "):])
        self.assertEqual([finding["lane"] for finding in forwarded],
                         RESEARCH_LANES,
                         "the integration worker receives every lane, in "
                         "canonical order, in its own packet")
        for finding in forwarded:
            self.assertEqual(
                sorted(finding), ["claim", "evidence", "id", "lane", "notes"])
        replay = self.engine.replay(run_id)
        self.assertTrue(replay["deterministic"],
                        "a forwarded join must replay from the record alone")
        self.assertEqual(replay["recompiled_hash"], out["packet_hash"])

    def test_author_proper_works_from_the_synthesized_brief(self):
        """Test 22."""
        run_id, _ = self.advance_to("research")
        out = self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "research-synthesis"))
        self.assertEqual(out["stage"], "author-proper")
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertIn("PRIOR_FINDINGS: []", packet,
                      "the author is not handed the raw lane findings; the "
                      "single-owner synthesis stage consumed them")
        fragment = (FRAGMENTS / "propers" / "author-proper.md").read_text(
            encoding="utf-8")
        self.assertIn("research/scope.md", fragment)
        self.assertIn("research-synthesis", fragment,
                      "the author is pointed at the brief that stage wrote")
        self.assertIn("research/scope.md", packet)

    def test_research_synthesis_owns_the_brief_and_does_not_author(self):
        fragment = (FRAGMENTS / "propers" / "research-synthesis.md").read_text(
            encoding="utf-8")
        self.assertIn("research/scope.md", fragment)
        self.assertIn("PRIOR_FINDINGS", fragment)
        self.assertRegex(fragment, re.compile(
            r"does not author the proper", re.IGNORECASE))


# ---------------------------------------------------------------------------
# 26-30. Guarantees inherited from a04a27f3a
# ---------------------------------------------------------------------------

class PreservedGuaranteeTests(PropersCase):
    """Test 26-29: nothing the previous heads established may loosen."""

    def test_seed_remains_byte_idempotent(self):
        """Test 26."""
        args = {"proper": DOC, "provider": "gpt"}
        first = self.engine.seed_bytes("proper", args)
        run_dir = self.engine.run_dir(json.loads(first)["run_id"])
        before = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                  for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(self.engine.seed_bytes("proper", args), first)
        after = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                 for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(set(json.loads(first)), {
            "bootstrap_version", "instructions", "iteration",
            "normalized_args", "packet_hash", "packet_path", "repo_commit",
            "run_id", "stage", "workflow_digest", "workflow_id",
            "workflow_version",
        })
        self.assertEqual(json.loads(first)["workflow_version"],
                         workflow_json()["version"])

    def test_seed_replays_after_the_research_stage_has_been_joined(self):
        args = {"proper": DOC, "provider": "gpt"}
        first = self.engine.seed_bytes("proper", args)
        run_id = json.loads(first)["run_id"]
        out = {"stage": "seed"}
        while out["stage"] != "research":
            out = self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, out["stage"]))
        self.engine.advance(run_id,
                            lane_results=self.lane_submissions(run_id))
        self.assertEqual(self.engine.seed_bytes("proper", args), first)

    def test_a_failed_research_advance_changes_nothing(self):
        """Test 27 and 28."""
        run_id, _ = self.advance_to("research")
        submissions = self.lane_submissions(run_id)
        before = self.authoritative(run_id)
        packets = self.runs / run_id / "packets"
        os.chmod(packets, 0o500)
        self.addCleanup(os.chmod, packets, 0o755)
        with self.assertRaises(WorkflowError) as caught:
            self.engine.advance(run_id, lane_results=submissions)
        self.assertIn("cannot write", str(caught.exception))
        os.chmod(packets, 0o755)
        self.assertEqual(self.authoritative(run_id), before)
        results = self.runs / run_id / "results"
        self.assertEqual([p.name for p in results.iterdir()
                          if p.name.startswith("research-0")], [])
        retried = self.engine.advance(run_id, lane_results=submissions)
        self.assertEqual(retried["stage"], "research-synthesis")

    def test_final_acceptance_is_still_a_program_gate(self):
        """Test 29."""
        workflow = workflow_json()
        accepting = [s for s in workflow["stages"]
                     if ACCEPTED in (s.get("next"), s.get("pass_transition"))]
        self.assertEqual([s["id"] for s in accepting], ["final-acceptance"])
        self.assertEqual(accepting[0]["type"], "gate")
        self.assertEqual(accepting[0]["execution"], {"mode": PROGRAM})
        self.assertNotIn("fragments", accepting[0])

    def test_content_and_visual_lanes_own_disjoint_finding_spaces(self):
        """Test 24-25, at the fragment level.

        The shared `content-evaluation.md` is deliberately not checked here:
        it carries the repair-ownership rule that routes a defect to its
        owner, which is a wiring rule every lane needs and none of them owns.
        """
        for lane in CONTENT_LANES + VISUAL_LANES:
            family = "content" if lane in CONTENT_LANES else "visual"
            with self.subTest(lane=lane):
                assert_lane_owns_its_findings(self, f"{family}-{lane}")


class LauncherTests(unittest.TestCase):
    """Test 30: the registered-tool surface is untouched."""

    def tpt(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                              text=True, cwd=ROOT)

    def test_registered_tool_dispatch_is_unchanged(self):
        self.assertEqual(self.tpt("--check").returncode, 0)
        listed = self.tpt("--list", "--json")
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertGreater(len(json.loads(listed.stdout)), 10)
        parsed = self.tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)

    def test_the_pipeline_still_loads_over_the_cli(self):
        shown = self.tpt("workflow", "show", "proper")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        workflow = json.loads(shown.stdout)
        self.assertEqual(workflow["version"], workflow_json()["version"])
        fanout = {
            stage["id"]: [lane["id"] for lane in stage["execution"]["lanes"]]
            for stage in workflow["stages"]
            if stage["execution"]["mode"] == FANOUT
        }
        self.assertEqual(fanout, {
            "research": RESEARCH_LANES,
            "content-evaluation": CONTENT_LANES,
            "visual-evaluation": VISUAL_LANES,
        })


if __name__ == "__main__":
    unittest.main()
