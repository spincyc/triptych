#!/usr/bin/env python3
"""One stage owns the research brief, and it is not the one that authors.

`research-synthesis` wrote `research/scope.md` and then `author-proper` was
told to extend it, so the brief had two writers in sequence and no single
stage could be held to its contents. These tests hold the correction where it
has to hold: in the deterministic bytes the workers are actually given, not
in the prose about them. The rule they apply is checked against the defect it
was written for, so it cannot pass by being vacuous.
"""
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    ACCEPTED,
    BLOCKED,
    FANOUT,
    HOST_MAX,
    PASS,
    PROGRAM,
    SINGLE,
    STRICT_UNION,
    WorkflowError,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    DOC,
    FRAGMENTS,
    RESEARCH_LANES,
    VISUAL_LANES,
    PropersCase,
    assert_lane_owns_its_findings,
    workflow_json,
)

BRIEF = "research/scope.md"
OWNER = "research-synthesis"

# The step `author-proper.md` carried before this correction: the second
# write that left the brief with no single owner. It is quoted here rather
# than fetched from history so the rule can be held to it in any checkout.
DUAL_WRITER_STEP = (
    "8. Extend `research/scope.md` with the audit records authoring\n"
    "   adds, preserving the research brief already recorded there.\n"
)

# Giving the brief one writer changed the fragments a run is bound to, so it
# needed a version bump; the workflow was at 4 before it and 5 after.
BRIEF_OWNERSHIP_VERSION = 5

MUTATION = re.compile(
    r"\b(creat\w*|updat\w*|extend\w*|append\w*|rewrit\w*|regenerat\w*"
    r"|overwrit\w*|writ\w*|edit\w*|modif\w*|amend\w*|improv\w*|suppl\w*"
    # No `record\w*`: "the source records ... exist" is a noun in a
    # read-only check, and matching it would fail a lane that only inspects.
    r"|adds?|adding|revis\w*|maintain\w*|place\w*|put)\b",
    re.IGNORECASE,
)
# Only forms that actually forbid. An earlier version accepted `owns?|owned|
# owner`, `without`, and a bare `not` anywhere in the sentence; "own" is
# scoping language that appears throughout the lane fragments, so adding the
# word "owns" to a write directive was enough to walk past the whole check.
NEGATION = re.compile(
    r"(\bdo(es)? not\b|\bmust not\b|\bmay not\b|\bcannot\b|\bnever\b"
    # Deliberately no `leave`/`unchanged`: "extend it and leave the brief
    # intact" would then exempt itself. The prohibitions in the tree carry a
    # real negation without them.
    r"|\bno\b|\bnor\b|\bimmutable\b|\bread-only\b|\bforbidden\b)",
    re.IGNORECASE,
)
# The brief is named several ways in the fragments, and a rule that only knew
# one of them would be evaded by writing another.
NAMES_BRIEF = re.compile(
    r"(research/scope\.md|\bscope\.md\b|\bresearch brief\b)",
    re.IGNORECASE,
)


def sentences(text: str) -> list[str]:
    """Reconstruct wrapped Markdown into sentences.

    The fragments are hard-wrapped at 78 columns, so a directive routinely
    spans two or three lines. A line-based check would miss the verb or miss
    the negation that qualifies it.
    """
    flat = " ".join(text.split())
    return [part for part in re.split(r"(?<=[.:;?])\s+", flat) if part]


def offending_sentences(text: str) -> list[str]:
    """Sentences telling a worker to change the brief.

    A sentence offends when it names the brief and carries a mutation verb
    that no negation qualifies. Prohibitions name the brief and its verbs on
    purpose, and are not offences.

    Adjacent sentences are checked as a pair as well as alone, because the
    natural way to write the directive this rule exists to catch is to name
    the file in one sentence and mutate it in the next.
    """
    parts = sentences(text)
    found = []
    for index, sentence in enumerate(parts):
        windows = [sentence]
        if index + 1 < len(parts):
            windows.append(sentence + " " + parts[index + 1])
        for window in windows:
            if not NAMES_BRIEF.search(window):
                continue
            if MUTATION.search(window) and not NEGATION.search(window):
                found.append(sentence)
                break
    return found


def propers_fragments() -> dict[str, str]:
    """Every fragment the propers workflow can put in front of a worker."""
    workflow = workflow_json()
    names: list[str] = []
    for stage in workflow["stages"]:
        names.extend(stage.get("fragments", []))
        for lane in stage.get("execution", {}).get("lanes", []):
            names.extend(lane.get("fragments", []))
    return {
        name: (FRAGMENTS / name).read_text(encoding="utf-8")
        for name in sorted(set(names))
    }


class BriefOwnershipTests(unittest.TestCase):
    """Enforcement 1-4: exactly one stage is told to write the brief."""

    def test_the_rule_catches_the_defect_it_was_written_for(self):
        """The check has teeth: it rejects the text this change removed."""
        offences = offending_sentences(DUAL_WRITER_STEP)
        self.assertTrue(
            offences,
            "the rule must fail the dual-writer text it was written against")
        self.assertTrue(
            any("Extend" in sentence for sentence in offences),
            f"expected the 'Extend {BRIEF}' step to be the offence, got "
            f"{offences}")

    def test_the_rule_catches_rewordings_of_the_defect(self):
        """Negative controls, each of which defeated an earlier version.

        A rule of this shape is only worth its runtime if it survives someone
        rephrasing the instruction it forbids. Each string below is a real
        way to say "second writer"; the first eight walked past the rule as
        first written.
        """
        evasions = [
            "Extend `research/scope.md` with the audit records this stage "
            "owns.",
            "Extend `research/scope.md` with the audit records authoring "
            "adds, and do this after `main.tex` is complete, not before.",
            "Extend `research/scope.md` with the audit records authoring "
            "adds, without disturbing the brief.",
            "The research brief is at `research/scope.md`. Append your audit "
            "records to the end of it.",
            "Extend the research brief with the audit records authoring adds.",
            "Extend `scope.md` under `research/` with the audit records "
            "authoring adds.",
            "Update `research/scope.md`, whose owner has already written the "
            "brief, with the audit records.",
            "Supplement `research/scope.md` with the audit records authoring "
            "adds.",
            "Run `cat >> research/scope.md` to place the audit records.",
            DUAL_WRITER_STEP,
        ]
        for text in evasions:
            with self.subTest(evasion=text[:60]):
                self.assertTrue(
                    offending_sentences(text),
                    f"the rule lets this through: {text!r}")

    def test_the_rule_permits_the_prohibitions_it_must_permit(self):
        """Positive controls: a rule that flags every mention is useless."""
        allowed = [
            "`research/scope.md` is immutable input owned by "
            "`research-synthesis`.",
            "Read it; do not edit, overwrite, append to, or regenerate it.",
            "Leave `research/scope.md` exactly as you found it.",
            "Authoring adds no audit record to it.",
            "It does not touch `propers/verified.md`, "
            "`propers/retrieved.txt`, `research/scope.md`, or any shared "
            "source inventory.",
            "Read the reception matrix in `research/scope.md` against the "
            "appointed passages.",
            "Do the source records — `propers/verified.md`, "
            "`propers/retrieved.txt`, and `research/scope.md` — exist and "
            "follow the profile's format?",
        ]
        for text in allowed:
            with self.subTest(allowed=text[:60]):
                self.assertEqual(
                    offending_sentences(text), [],
                    f"the rule wrongly flags a read or a prohibition: "
                    f"{text!r}")

    def test_only_research_synthesis_is_told_to_write_the_brief(self):
        """Enforcement 1, 2 and 4, over every fragment in the workflow."""
        owners = []
        for name, text in propers_fragments().items():
            offences = offending_sentences(text)
            if offences:
                owners.append(name)
            with self.subTest(fragment=name):
                if name != f"propers/{OWNER}.md":
                    self.assertEqual(
                        offences, [],
                        f"{name} is told to change {BRIEF}, which only "
                        f"{OWNER} may do")
        self.assertEqual(owners, [f"propers/{OWNER}.md"],
                         f"exactly one fragment writes {BRIEF}")

    def test_research_synthesis_claims_sole_ownership(self):
        """Enforcement 1."""
        text = (FRAGMENTS / "propers" / f"{OWNER}.md").read_text(
            encoding="utf-8")
        self.assertIn(BRIEF, text)
        self.assertRegex(text, re.compile(
            r"sole (writer|owner)|only stage", re.IGNORECASE),
            f"{OWNER} must state that it alone writes {BRIEF}")
        claim = next(s for s in sentences(text)
                     if re.search(r"sole (writer|owner)|only stage", s, re.I))
        self.assertIn(BRIEF, claim,
                      "the ownership claim must name the file it is about")

    def test_author_proper_marks_the_brief_immutable(self):
        """Enforcement 2 and 3."""
        text = (FRAGMENTS / "propers" / "author-proper.md").read_text(
            encoding="utf-8")
        self.assertIn(BRIEF, text, "the author still reads the brief")
        self.assertRegex(text, re.compile(
            r"immutable|read-only", re.IGNORECASE),
            f"author-proper must mark {BRIEF} as immutable input")
        self.assertRegex(text, re.compile(
            r"do not (edit|change|overwrite|append|regenerate|rewrite)",
            re.IGNORECASE))
        self.assertEqual(offending_sentences(text), [])
        self.assertIn(OWNER, text,
                      "the author is told which stage owns the brief")

    def test_the_owner_is_told_to_leave_the_brief_complete(self):
        text = (FRAGMENTS / "propers" / f"{OWNER}.md").read_text(
            encoding="utf-8")
        self.assertRegex(text, re.compile(
            r"complete|sufficient|nothing later|no later", re.IGNORECASE),
            f"{OWNER} must leave {BRIEF} fit for authoring, since no stage "
            f"after it may add to the file")


class EmittedPacketTests(PropersCase):
    """Enforcement 4, on the bytes a worker is actually handed."""

    def compiled_packets(self) -> dict[str, str]:
        run_id, _ = self.advance_to("research")
        workflow = self.engine.load_workflow("proper")
        state = self.engine.load_state(run_id)
        packets = {}
        for stage in workflow["stages"]:
            compiled = self.engine._compile_stage_packets(
                workflow, stage, state, self.engine.run_dir(run_id), [])
            packets[stage["id"]] = compiled["bytes"].decode("utf-8")
            for lane in compiled.get("lanes", []):
                packets[f"{stage['id']}/{lane['lane']}"] = \
                    lane["bytes"].decode("utf-8")
        return packets

    def test_no_emitted_packet_but_the_owners_directs_a_write(self):
        for stage, text in self.compiled_packets().items():
            with self.subTest(stage=stage):
                offences = offending_sentences(text)
                if stage == OWNER:
                    self.assertTrue(
                        offences,
                        f"the {OWNER} packet must be the one that writes "
                        f"{BRIEF}")
                else:
                    self.assertEqual(
                        offences, [],
                        f"the {stage} packet directs a change to {BRIEF}")

    def test_the_author_packet_still_receives_the_brief(self):
        packets = self.compiled_packets()
        author = packets["author-proper"]
        self.assertIn(BRIEF, author,
                      "the author must still be pointed at the brief")
        self.assertRegex(author, re.compile(r"immutable|read-only", re.I))


class BlockedAuthoringTests(PropersCase):
    """Enforcement 5-6: a deficient brief goes back through tpt, not around it."""

    def drive_to_author(self) -> tuple[str, dict]:
        run_id, out = self.advance_to("research")
        out = self.engine.advance(
            run_id, lane_results=self.lane_submissions(run_id))
        self.assertEqual(out["stage"], OWNER)
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, OWNER))
        self.assertEqual(out["stage"], "author-proper")
        return run_id, out

    def test_author_proper_is_told_to_block_on_a_deficient_brief(self):
        """Enforcement 5, in the guidance the author is given."""
        run_id, out = self.drive_to_author()
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        self.assertIn(BLOCKED, packet,
                      "the author must be told the disposition to return")
        text = (FRAGMENTS / "propers" / "author-proper.md").read_text(
            encoding="utf-8")
        self.assertIn(BLOCKED, text)
        self.assertRegex(text, re.compile(
            r"insufficient|deficien\w+|contradictory|unsuitable|cannot",
            re.IGNORECASE),
            "the author must be told when to block rather than repair")

    def test_a_blocked_authoring_result_is_terminal_and_authoritative(self):
        """Enforcement 6: tpt owns the outcome; nothing routes around it."""
        run_id, _ = self.drive_to_author()
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        submitted = {
            "stage": "author-proper", "iteration": packet["iteration"],
            "disposition": BLOCKED,
            "summary": "the research brief is missing required evidence",
        }
        path = self.write("author-blocked", submitted)
        out = self.engine.advance(run_id, result_path=path)
        self.assertEqual(out["disposition"], BLOCKED)

        state = self.engine.load_state(run_id)
        self.assertEqual(state["disposition"], BLOCKED)
        self.assertEqual(state["current_stage"], BLOCKED)
        self.assertEqual(state["transitions"][-1],
                         {"from": "author-proper", "to": BLOCKED,
                          "disposition": BLOCKED})
        recorded = state["result_hashes"][-1]
        self.assertEqual(
            json.loads((ROOT / recorded["path"]).read_text(encoding="utf-8")),
            submitted, "the block is recorded exactly as the worker sent it")

        # A blocked run is over: it emits no successor and accepts nothing.
        self.assertEqual(len(state["packet_hashes"]),
                         len(state["transitions"]),
                         "a blocked run was given no successor packet")
        for attempt in (dict(run_gate=True), dict(result_path=path)):
            with self.assertRaises(WorkflowError) as caught:
                self.engine.advance(run_id, **attempt)
            self.assertIn(BLOCKED, str(caught.exception))

    def test_blocking_does_not_touch_the_brief(self):
        """The engine writes nothing outside its own run directory.

        A fixed list of paths rather than a tree walk: the tree under
        `workflows/` is edited by people while a suite runs, and a spurious
        failure here would say nothing about the engine.
        """
        watched = [
            FRAGMENTS / "propers" / "author-proper.md",
            FRAGMENTS / "propers" / f"{OWNER}.md",
            ROOT / "workflows" / "pipelines" / "proper.json",
            ROOT / "src" / "gpt" / DOC / "research" / "scope.md",
        ]

        def snapshot() -> dict[str, bytes | None]:
            return {
                path.as_posix(): (path.read_bytes() if path.is_file() else None)
                for path in watched
            }

        run_id, _ = self.drive_to_author()
        before = snapshot()
        packet = self.engine.load_state(run_id)["packet_hashes"][-1]
        self.engine.advance(run_id, result_path=self.write("blocked", {
            "stage": "author-proper", "iteration": packet["iteration"],
            "disposition": BLOCKED, "summary": "insufficient research",
        }))
        self.assertEqual(snapshot(), before,
                         "a blocked authoring result changes no workflow "
                         "source, and the engine never writes the brief")


class PreservedArchitectureTests(unittest.TestCase):
    """Regression 5-7 and 11: the accepted topology is untouched."""

    @classmethod
    def setUpClass(cls):
        cls.workflow = workflow_json()
        cls.stages = {s["id"]: s for s in cls.workflow["stages"]}

    def test_the_research_fanout_is_unchanged(self):
        research = self.stages["research"]
        self.assertEqual(research["type"], "linear")
        self.assertEqual(research["execution"]["mode"], FANOUT)
        self.assertEqual(research["execution"]["parallelism"], HOST_MAX)
        self.assertEqual(research["execution"]["join"], STRICT_UNION)
        self.assertEqual(
            [lane["id"] for lane in research["execution"]["lanes"]],
            RESEARCH_LANES)
        self.assertEqual(research["next"], OWNER)
        self.assertEqual(self.stages["source-audit"]["next"], "research")

    def test_the_evaluation_fanouts_are_unchanged(self):
        for stage_id, lanes in (("content-evaluation", CONTENT_LANES),
                                ("visual-evaluation", VISUAL_LANES)):
            with self.subTest(stage=stage_id):
                execution = self.stages[stage_id]["execution"]
                self.assertEqual(execution["mode"], FANOUT)
                self.assertEqual(execution["parallelism"], HOST_MAX)
                self.assertEqual(execution["join"], STRICT_UNION)
                self.assertEqual([lane["id"] for lane in execution["lanes"]],
                                 lanes)

    def test_the_single_owner_stages_are_unchanged(self):
        for stage_id in (OWNER, "author-proper", "source-audit",
                         "content-revision", "artifact-revision",
                         "visual-revision", "build-artifacts"):
            with self.subTest(stage=stage_id):
                self.assertEqual(self.stages[stage_id]["execution"],
                                 {"mode": SINGLE})

    def test_final_acceptance_remains_a_program_gate(self):
        accepting = [s for s in self.workflow["stages"]
                     if ACCEPTED in (s.get("next"), s.get("pass_transition"))]
        self.assertEqual([s["id"] for s in accepting], ["final-acceptance"])
        self.assertEqual(accepting[0]["type"], "gate")
        self.assertEqual(accepting[0]["execution"], {"mode": PROGRAM})

    def test_both_evaluation_fanouts_keep_their_lanes_disjoint(self):
        for lane in CONTENT_LANES + VISUAL_LANES:
            family = "content" if lane in CONTENT_LANES else "visual"
            with self.subTest(lane=lane):
                assert_lane_owns_its_findings(self, f"{family}-{lane}")

    def test_the_integrating_lane_states_no_lane_count(self):
        """A lane fragment that counts the lanes goes stale when one is added.

        `theological-synthesis` told its worker the integrator "integrates
        all five lanes", and two later lanes made that false without anyone
        touching the fragment. It states the relationship instead.
        """
        text = (FRAGMENTS / "propers" / "lanes"
                / "research-theological-synthesis.md").read_text(
                    encoding="utf-8")
        flat = " ".join(text.split())
        self.assertIn("integrates every lane", flat,
                      "the lane must still say who integrates what it "
                      "returns, so its worker knows it is not the authority")
        self.assertNotRegex(
            flat, re.compile(
                r"\b(two|three|four|five|six|seven|eight|nine|ten|\d+) "
                r"lanes\b", re.IGNORECASE),
            "a hardcoded lane count here is false the next time the fan-out "
            "grows, and nothing would fail")

    def test_the_research_fanout_keeps_its_lanes_disjoint(self):
        for lane in RESEARCH_LANES:
            with self.subTest(lane=lane):
                assert_lane_owns_its_findings(self, f"research-{lane}")

    def test_the_workflow_version_is_past_the_ownership_bump(self):
        """Changed guidance bytes must stop a run bound to the old ones."""
        version = self.workflow["version"]
        self.assertIsInstance(version, int)
        self.assertGreaterEqual(
            version, BRIEF_OWNERSHIP_VERSION,
            "these fragments changed, so the bound source digest changed; a "
            "run seeded before that must be told to seed again, which the "
            "pipeline can only do by never going back below the bump")


class PreservedGuaranteeTests(PropersCase):
    """Regression 5, 8-10: determinism, seed, and refusal are untouched."""

    def test_research_fanout_remains_deterministic(self):
        def drive(order):
            run_id, _ = self.advance_to("research")
            out = self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id, order))
            joined = self.engine.load_state(run_id)["result_hashes"][-1]
            return (out["packet_hash"], joined["hash"],
                    [lane["lane"] for lane in joined["lanes"]])

        first = drive(RESEARCH_LANES)
        self.discard_runs()
        second = drive(list(reversed(RESEARCH_LANES)))
        self.assertEqual(first, second)
        self.assertEqual(first[2], RESEARCH_LANES)

    def test_seed_remains_byte_idempotent(self):
        args = {"proper": DOC, "provider": "gpt"}
        first = self.engine.seed_bytes("proper", args)
        run_dir = self.engine.run_dir(json.loads(first)["run_id"])
        before = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                  for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(self.engine.seed_bytes("proper", args), first)
        after = {p.relative_to(run_dir).as_posix(): p.read_bytes()
                 for p in sorted(run_dir.rglob("*")) if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(json.loads(first)["workflow_version"],
                         workflow_json()["version"])

    def test_a_refused_authoring_result_stays_non_authoritative(self):
        run_id, _ = self.advance_to("research")
        self.engine.advance(run_id,
                            lane_results=self.lane_submissions(run_id))
        self.engine.advance(run_id,
                            result_path=self.worker_pass(run_id, OWNER))
        before = self.authoritative(run_id)
        # A result naming the stage the author was never given.
        path = self.write("forged", {
            "stage": OWNER, "iteration": 0, "disposition": PASS,
            "summary": "answering a packet the run has moved past",
        })
        with self.assertRaises(WorkflowError):
            self.engine.advance(run_id, result_path=path)
        self.assertEqual(self.authoritative(run_id), before)

    def test_a_failed_authoring_advance_changes_nothing(self):
        run_id, _ = self.advance_to("research")
        self.engine.advance(run_id,
                            lane_results=self.lane_submissions(run_id))
        before = self.authoritative(run_id)
        packets = self.runs / run_id / "packets"
        os.chmod(packets, 0o500)
        self.addCleanup(os.chmod, packets, 0o755)
        with self.assertRaises(WorkflowError):
            self.engine.advance(
                run_id, result_path=self.worker_pass(run_id, OWNER))
        os.chmod(packets, 0o755)
        self.assertEqual(self.authoritative(run_id), before)


class LauncherTests(unittest.TestCase):
    """Regression 12."""

    def tpt(self, *argv: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), *argv], capture_output=True,
                              text=True, cwd=ROOT)

    def test_registered_tool_dispatch_is_unchanged(self):
        self.assertEqual(self.tpt("--check").returncode, 0)
        parsed = self.tpt("citations", "parse", "Psalm 24:1-3", "--json")
        self.assertEqual(parsed.returncode, 0, parsed.stderr)
        shown = self.tpt("workflow", "show", "proper")
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertEqual(json.loads(shown.stdout)["version"],
                         workflow_json()["version"])


if __name__ == "__main__":
    unittest.main()
