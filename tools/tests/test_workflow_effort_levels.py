#!/usr/bin/env python3
"""How hard the model thinks is workflow data, not a console choice.

Every other dispatch decision this engine makes is declared and hashed: which
stage runs, by one agent or by five lanes, on which fragments, against which
schema. The reasoning effort the dispatched agent runs at was the one input
left to whoever happened to be driving. Two hosts could answer the same packet
bytes at two levels and the run recorded neither, which is the same defect as
an instruction added to a lane brief at the console: an input that changed the
answer and that nothing preserved.

So `effort` is declared in the pipeline, resolved most-specific-first (lane,
then stage, then the workflow default), carried in the packet header where the
packet hash covers it, and printed in the driver instructions beside the lane
it belongs to.

The levels the `proper` pipeline declares, and why:

- `xhigh` is the working default, and the level the long-horizon stages run
  at — seed through the brief, the authoring, the revisions.
- `max` is paid for twice, at the judgment the repository actually fails:
  deciding what it does not hold. `source-audit` collates the appointed text
  against the controlling witness, the `source-citation-coverage` lane decides
  what is attested and what is only a lead, and `content-evaluation` is the
  pass that gates publication on the scholarship. The 54-fourteenth leaf spent
  three revision rounds stripping claims resting on witnesses this repository
  does not hold.
- `high` covers the mechanical stretch: the build, the artifact repair, the
  page-by-page visual review, the web conversion and its evaluation, and the
  install.
- `low` is declared by no stage. It is for a narrow lookup — one locus, one
  hash — and no stage of this workflow is one.

A gate declares no effort at all: tpt runs it, no agent does.
"""
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    EFFORT_LEVELS,
    WorkflowError,
    _stage_effort,
    _validate_workflow,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    PropersCase,
    workflow_json,
)

MAX_STAGES = {"source-audit", "content-evaluation"}
MAX_LANES = {("research", "source-citation-coverage")}
HIGH_STAGES = {
    "build-artifacts", "artifact-revision", "visual-evaluation",
    "visual-revision", "generate-web", "web-evaluation", "web-revision",
    "publish-artifacts", "install-publication",
}
DEFAULT = "xhigh"


def stages() -> dict:
    return {s["id"]: s for s in workflow_json()["stages"]}


class DeclarationTests(unittest.TestCase):
    """What the pipeline declares, held against why each level was chosen."""

    def setUp(self):
        self.workflow = workflow_json()
        self.stages = {s["id"]: s for s in self.workflow["stages"]}

    def test_the_workflow_declares_a_default(self):
        self.assertEqual(self.workflow.get("default_effort"), DEFAULT,
                         "without a default, a stage that declares nothing "
                         "runs at whatever the host picked")

    def test_every_agent_stage_resolves_to_a_declared_level(self):
        for sid, stage in self.stages.items():
            if stage["type"] == "gate":
                continue
            with self.subTest(stage=sid):
                self.assertIn(_stage_effort(self.workflow, stage),
                              EFFORT_LEVELS)

    def test_no_gate_declares_an_effort(self):
        """A gate is run by tpt; an effort on one would name a phantom agent."""
        for sid, stage in self.stages.items():
            if stage["type"] != "gate":
                continue
            with self.subTest(stage=sid):
                self.assertNotIn("effort", stage)
                self.assertIsNone(_stage_effort(self.workflow, stage))

    def test_max_is_declared_where_the_repository_actually_fails(self):
        for sid in MAX_STAGES:
            with self.subTest(stage=sid):
                self.assertEqual(
                    _stage_effort(self.workflow, self.stages[sid]), "max")
        for sid, lane_id in MAX_LANES:
            stage = self.stages[sid]
            lane = next(l for l in stage["execution"]["lanes"]
                        if l["id"] == lane_id)
            with self.subTest(lane=f"{sid}/{lane_id}"):
                self.assertEqual(_stage_effort(self.workflow, stage, lane),
                                 "max")

    def test_max_is_declared_nowhere_else(self):
        """The level is paid for per token; a third max is a cost decision."""
        found = set()
        for sid, stage in self.stages.items():
            if stage["type"] == "gate":
                continue
            lanes = stage["execution"].get("lanes", [])
            if not lanes:
                if _stage_effort(self.workflow, stage) == "max":
                    found.add(sid)
                continue
            for lane in lanes:
                if _stage_effort(self.workflow, stage, lane) == "max":
                    found.add((sid, lane["id"]))
        expected = ({"source-audit"} | MAX_LANES
                    | {("content-evaluation", lane) for lane in CONTENT_LANES})
        self.assertEqual(
            found, expected,
            "max spread beyond the two judgments it was chosen for")

    def test_the_mechanical_stretch_is_high(self):
        for sid in HIGH_STAGES:
            with self.subTest(stage=sid):
                self.assertEqual(
                    _stage_effort(self.workflow, self.stages[sid]), "high")

    def test_the_long_horizon_stages_keep_the_default(self):
        for sid in ("seed", "resolve-context", "research-synthesis",
                    "author-proper", "content-revision"):
            with self.subTest(stage=sid):
                self.assertEqual(
                    _stage_effort(self.workflow, self.stages[sid]), DEFAULT)
                self.assertNotIn(
                    "effort", self.stages[sid],
                    "a stage at the default states it by not restating it; a "
                    "copy here is a second place to keep in step")

    def test_no_stage_is_declared_low(self):
        """`low` is for a one-locus lookup, and no stage of this is one."""
        for sid, stage in self.stages.items():
            if stage["type"] == "gate":
                continue
            lanes = stage["execution"].get("lanes", []) or [None]
            for lane in lanes:
                with self.subTest(stage=sid, lane=lane and lane["id"]):
                    self.assertNotEqual(
                        _stage_effort(self.workflow, stage, lane), "low")

    def test_a_lane_overrides_its_stage_and_a_stage_the_default(self):
        research = self.stages["research"]
        lanes = {l["id"]: l for l in research["execution"]["lanes"]}
        self.assertEqual(
            _stage_effort(self.workflow, research,
                          lanes["source-citation-coverage"]), "max")
        self.assertEqual(
            _stage_effort(self.workflow, research,
                          lanes["cultural-afterlife"]), DEFAULT,
            "one lane's raise must not lift its siblings")


class ValidationTests(unittest.TestCase):
    """A level the engine does not know must not reach a host."""

    def base(self) -> dict:
        return json.loads(json.dumps(workflow_json()))

    def assert_refused(self, data: dict, fragment: str):
        with self.assertRaises(WorkflowError) as caught:
            _validate_workflow(data, Path("proper.json"))
        self.assertIn(fragment, str(caught.exception))

    def test_the_shipped_pipeline_validates(self):
        _validate_workflow(self.base(), Path("proper.json"))

    def test_an_unknown_default_is_refused(self):
        data = self.base()
        data["default_effort"] = "maximum"
        self.assert_refused(data, "default_effort must be one of")

    def test_an_unknown_stage_effort_is_refused(self):
        data = self.base()
        for stage in data["stages"]:
            if stage["id"] == "author-proper":
                stage["effort"] = "ultra"
        self.assert_refused(data, "effort must be one of")

    def test_an_unknown_lane_effort_is_refused(self):
        data = self.base()
        for stage in data["stages"]:
            if stage["id"] == "research":
                stage["execution"]["lanes"][0]["effort"] = "hard"
        self.assert_refused(data, "effort must be one of")

    def test_a_gate_may_not_declare_an_effort(self):
        data = self.base()
        for stage in data["stages"]:
            if stage["id"] == "scope-gate":
                stage["effort"] = "max"
        self.assert_refused(data, "a gate runs no agent")

    def test_a_non_string_effort_is_refused(self):
        data = self.base()
        data["default_effort"] = 3
        self.assert_refused(data, "default_effort must be one of")


class PacketAndDriverTests(PropersCase):
    """The level in the bytes that are hashed, and in the order to dispatch."""

    def compiled(self, stage_id: str):
        run_id, _ = self.advance_to("research")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        stage = next(s for s in workflow["stages"] if s["id"] == stage_id)
        packet = self.engine._compile_stage_packets(
            workflow, stage, state, self.engine.run_dir(run_id), [])
        return workflow, stage, state, packet

    def test_a_single_stage_packet_header_carries_its_effort(self):
        _, _, _, packet = self.compiled("author-proper")
        self.assertIn("\nEFFORT: xhigh\n", packet["bytes"].decode("utf-8"))

    def test_a_gate_packet_carries_no_effort_line(self):
        _, _, _, packet = self.compiled("content-preflight")
        self.assertNotIn("EFFORT:", packet["bytes"].decode("utf-8"))

    def test_each_lane_packet_carries_its_own_level(self):
        _, _, _, packet = self.compiled("research")
        got = {}
        for lane in packet["lanes"]:
            text = lane["bytes"].decode("utf-8")
            got[lane["lane"]] = re.search(r"^EFFORT: (\S+)$", text,
                                          re.MULTILINE).group(1)
        self.assertEqual(got["source-citation-coverage"], "max")
        self.assertEqual(got["cultural-afterlife"], "xhigh")

    def test_every_content_lane_packet_is_max(self):
        _, _, _, packet = self.compiled("content-evaluation")
        for lane in packet["lanes"]:
            with self.subTest(lane=lane["lane"]):
                self.assertIn("\nEFFORT: max\n",
                              lane["bytes"].decode("utf-8"))
        self.assertEqual(
            sorted(l["lane"] for l in packet["lanes"]), sorted(CONTENT_LANES))

    def test_the_effort_is_inside_the_hashed_packet_material(self):
        """Changing the level must move the hash, or nothing recorded it."""
        workflow, stage, state, packet = self.compiled("author-proper")
        before = packet["hash"]
        stage["effort"] = "max"
        after = self.engine._compile_stage_packets(
            workflow, stage, state,
            self.engine.run_dir(state["run_id"]), [])["hash"]
        self.assertNotEqual(before, after)

    def test_the_single_driver_instruction_names_the_level(self):
        workflow, stage, state, packet = self.compiled("author-proper")
        text = self.engine._driver_instructions(workflow, stage, state, packet)
        self.assertIn("EXECUTION POLICY: SINGLE", text)
        self.assertRegex(text, r"reasoning effort xhigh")
        self.assertRegex(
            text, r"not a host choice",
            "the driver must be told the level is not its to pick; that is "
            "the whole reason it is declared")

    def test_the_fanout_roster_names_a_level_per_lane(self):
        workflow, stage, state, packet = self.compiled("research")
        text = self.engine._driver_instructions(workflow, stage, state, packet)
        self.assertIn("EXECUTION POLICY: FANOUT / HOST-MAX", text)
        block = re.search(
            r"^  \d+\. source-citation-coverage\n     effort: max$",
            text, re.MULTILINE)
        self.assertIsNotNone(
            block, "the raised lane's level must sit in its own roster entry, "
                   "where a driver reading the roster cannot miss it")
        self.assertRegex(text, r"do not level the lanes to one effort")

    def test_a_gate_instruction_names_no_level(self):
        workflow, stage, state, packet = self.compiled("content-preflight")
        text = self.engine._driver_instructions(workflow, stage, state, packet)
        self.assertIn("PROGRAM GATE", text)
        self.assertNotIn("reasoning effort", text)


if __name__ == "__main__":
    unittest.main()
