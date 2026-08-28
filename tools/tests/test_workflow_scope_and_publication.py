#!/usr/bin/env python3
"""An authorized target is one target, and a published run is a wired one.

Version 9 put two phases around the production phase the workflow already
had. In front of it, `authorize-target` records a maintainer's decision and
`scope-gate` refuses a run whose target was never decided on — a permanent
identity in the registry says a proper *could* be written, never that this
one *may* be. Behind it, the artifacts are published, converted, judged
again, installed, and only then accepted.

These tests hold the two properties that phase pair exists for: that an
authorization opens exactly one provider and one identity and nothing
adjacent to either, and that acceptance now means the publication is wired,
not that two PDFs built.

The gate checks are exercised as the engine runs them — the command string
read out of the pipeline, its placeholders shell-quoted, run through a shell
and judged by exit code — against fixture files in a temporary directory.
`guidance/liturgy/propers-production-plan.md` records real decisions about a
closed collection, so no test writes to the real one.
"""

from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _workflow import (  # noqa: E402
    ACCEPTED,
    BLOCKED,
    FANOUT,
    HOST_MAX,
    PROGRAM,
    SINGLE,
    STRICT_UNION,
    WorkflowEngine,
    _substitute_args,
)
from test_workflow_research_fanout import (  # noqa: E402
    CONTENT_LANES,
    DOC,
    FRAGMENTS,
    RESEARCH_LANES,
    STAGE_ORDER,
    VISUAL_LANES,
    workflow_json,
)

PLAN = "guidance/liturgy/propers-production-plan.md"

# A different identity in the same band as the probe document. It is only ever
# used as a string: what is being tested is that authorizing one identity says
# nothing about its neighbour, and that holds whether or not the neighbour has
# a leaf on disk.
NEIGHBOUR = re.sub(r"/(\d+)-", lambda m: f"/{int(m.group(1)) + 1:02d}-", DOC)
UNREGISTERED = "liturgy/roman-rite/1962/propers/temporal/99-invented-sunday"

# The standing text of the plan file, near enough for a fixture: the section
# the entries live in, and nothing derived from anywhere else.
PLAN_FIXTURE = """# Propers Production Plan

## Scope boundary

The propers collections are **bounded at the set already published**. The
maintainer closed them on 2026-07-25.

### Authorized targets

Each line below records one maintainer decision to open the boundary for one
provider and one permanent identity.

"""

ENTRY_LINE = re.compile(
    r"^[ \t]*(- Authorized <YYYY-MM-DD>: provider `\{provider\}`, "
    r"identity `\{proper\}`\.)[ \t]*$",
    re.MULTILINE,
)


def stages() -> dict[str, dict]:
    return {stage["id"]: stage for stage in workflow_json()["stages"]}


def gate_check(gate_id: str, check_id: str) -> str:
    """The command template the pipeline declares for one gate check."""
    for check in stages()[gate_id]["checks"]:
        if check["id"] == check_id:
            return check["command"]
    raise AssertionError(f"{gate_id} declares no check {check_id}")


def run_check(command: str, proper: str, provider: str,
              cwd: Path) -> subprocess.CompletedProcess:
    """Run a gate check exactly as `_run_gate` would, in a chosen directory."""
    for key, value in (("proper", proper), ("provider", provider)):
        command = command.replace("{" + key + "}", shlex.quote(value))
    return subprocess.run(command, shell=True, capture_output=True, text=True,
                          cwd=cwd, timeout=300)


def entry_for(proper: str, provider: str, date: str = "2026-08-26") -> str:
    """One authorization entry, in the form the fragment specifies.

    Read out of the fragment rather than written down here, so the line this
    test appends and the line the gate greps for cannot drift apart from the
    line the worker is told to write.
    """
    fragment = (FRAGMENTS / "propers" / "authorize-target.md").read_text(
        encoding="utf-8")
    matches = ENTRY_LINE.findall(fragment)
    assert len(matches) == 1, (
        "authorize-target.md must state the entry line verbatim, exactly "
        f"once; found {len(matches)}")
    line = matches[0]
    return (line.replace("<YYYY-MM-DD>", date)
                .replace("{provider}", provider)
                .replace("{proper}", proper))


class PlanFixture(unittest.TestCase):
    """A throwaway tree holding nothing but a plan file to grep."""

    def setUp(self):
        self.tree = Path(tempfile.mkdtemp(prefix="tpt-scope-"))
        self.addCleanup(shutil.rmtree, self.tree, ignore_errors=True)
        self.plan = self.tree / PLAN
        self.plan.parent.mkdir(parents=True, exist_ok=True)
        self.plan.write_text(PLAN_FIXTURE, encoding="utf-8")

    def authorize(self, proper: str, provider: str,
                  date: str = "2026-08-26") -> None:
        """The idempotent append `authorize-target.md` instructs.

        Look for an entry for exactly this provider and this identity; write
        nothing if it is already there, and otherwise append exactly one.
        """
        entry = entry_for(proper, provider, date)
        text = self.plan.read_text(encoding="utf-8")
        pattern = f"provider `{provider}`, identity `{proper}`"
        if pattern in text:
            return
        self.plan.write_text(text + entry + "\n", encoding="utf-8")

    def authorized(self, proper: str, provider: str) -> bool:
        done = run_check(gate_check("scope-gate", "authorized-scope"),
                         proper, provider, self.tree)
        return done.returncode == 0

    def entry_count(self, proper: str, provider: str) -> int:
        needle = f"provider `{provider}`, identity `{proper}`"
        return sum(needle in line
                   for line in self.plan.read_text(encoding="utf-8").split("\n"))


# ---------------------------------------------------------------------------
# Authorization opens one target
# ---------------------------------------------------------------------------

class AuthorizationScopeTests(PlanFixture):
    """One entry authorizes one provider and one identity, and no more."""

    def test_the_boundary_is_closed_before_anything_is_authorized(self):
        self.assertFalse(self.authorized(DOC, "gpt"))
        self.assertFalse(self.authorized(DOC, "claude"))

    def test_authorizing_a_target_authorizes_that_target(self):
        self.authorize(DOC, "gpt")
        self.assertTrue(self.authorized(DOC, "gpt"))

    def test_authorizing_one_provider_does_not_authorize_the_other(self):
        self.authorize(DOC, "gpt")
        self.assertFalse(
            self.authorized(DOC, "claude"),
            "each provider is a separate maintainer decision")

    def test_authorizing_one_identity_does_not_open_its_neighbour(self):
        self.authorize(DOC, "gpt")
        self.assertFalse(
            self.authorized(NEIGHBOUR, "gpt"),
            "an adjacent identity in the same band stays closed")
        self.assertFalse(self.authorized(NEIGHBOUR, "claude"))

    def test_an_identity_is_not_matched_by_a_prefix_of_itself(self):
        """The closing backtick is what stops `5` standing for `51`."""
        self.authorize(DOC, "gpt")
        stem = DOC.rsplit("-", 1)[0]
        self.assertNotEqual(stem, DOC)
        self.assertFalse(self.authorized(stem, "gpt"))

    def test_authorizing_changes_only_the_requested_pair(self):
        self.authorize(NEIGHBOUR, "claude")
        before = self.plan.read_text(encoding="utf-8").split("\n")
        self.authorize(DOC, "gpt")
        after = self.plan.read_text(encoding="utf-8").split("\n")

        added = [line for line in after if line and line not in before]
        self.assertEqual(len(added), 1, added)
        self.assertIn(f"provider `gpt`, identity `{DOC}`", added[0])
        self.assertEqual([line for line in before if line],
                         [line for line in after if line][:len(
                             [line for line in before if line])],
                         "an entry is appended; nothing earlier is rewritten")
        self.assertTrue(self.authorized(NEIGHBOUR, "claude"))
        self.assertTrue(self.authorized(DOC, "gpt"))
        self.assertFalse(self.authorized(NEIGHBOUR, "gpt"))
        self.assertFalse(self.authorized(DOC, "claude"))

    def test_reauthorizing_writes_nothing(self):
        self.authorize(DOC, "gpt")
        once = self.plan.read_bytes()
        self.authorize(DOC, "gpt")
        self.authorize(DOC, "gpt", date="2026-09-01")
        self.assertEqual(self.plan.read_bytes(), once,
                         "reauthorizing an authorized target is a no-op, "
                         "down to the date already recorded")
        self.assertEqual(self.entry_count(DOC, "gpt"), 1)

    def test_both_providers_get_their_own_entry(self):
        self.authorize(DOC, "gpt")
        self.authorize(DOC, "claude")
        self.assertEqual(self.entry_count(DOC, "gpt"), 1)
        self.assertEqual(self.entry_count(DOC, "claude"), 1)
        entries = [line for line in self.plan.read_text(encoding="utf-8")
                   .split("\n") if line.startswith("- Authorized ")]
        self.assertEqual(len(entries), 2)
        for entry in entries:
            with self.subTest(entry=entry):
                self.assertEqual(
                    len(re.findall(r"provider `", entry)), 1,
                    "an entry never covers two providers at once")

    def test_the_fragment_tells_the_worker_what_the_gate_greps_for(self):
        """The written form and the checked form are one string.

        If they were two, an entry could satisfy the fragment and fail the
        gate, and the boundary would refuse targets the maintainer opened.
        """
        command = gate_check("scope-gate", "authorized-scope")
        needle = ('index($0, "provider `" p "`, identity `" d "`.") > 0')
        # The gate matches an authorization LINE, not a mention anywhere in
        # the file, so prose about a target -- or a line revoking one --
        # cannot read as an authorization.
        self.assertIn('index($0, "- Authorized ") == 1', command)
        self.assertIn(needle, command)
        fragment = (FRAGMENTS / "propers" / "authorize-target.md").read_text(
            encoding="utf-8")
        self.assertIn(needle, fragment)
        self.assertIn(PLAN, command)


# ---------------------------------------------------------------------------
# The scope gate
# ---------------------------------------------------------------------------

class ScopeGateTests(PlanFixture):
    """Three questions, all of which must be answered yes."""

    def test_the_gate_asks_for_identity_provider_and_authorization(self):
        gate = stages()["scope-gate"]
        self.assertEqual(gate["type"], "gate")
        self.assertEqual(gate["execution"], {"mode": PROGRAM})
        self.assertEqual([check["id"] for check in gate["checks"]],
                         ["registered-identity", "known-provider",
                          "authorized-scope"])
        self.assertEqual(gate["pass_transition"], "resolve-context")
        self.assertEqual(gate["fail_transition"], BLOCKED,
                         "an unauthorized target has nothing to revise")
        self.assertNotIn("fragments", gate,
                         "a gate gives no instructions to any agent")

    def test_the_gate_stands_between_the_seed_and_any_work(self):
        wiring = stages()
        self.assertEqual(wiring["seed"]["next"], "authorize-target")
        self.assertEqual(wiring["authorize-target"]["next"], "scope-gate")
        self.assertEqual(STAGE_ORDER.index("scope-gate"),
                         STAGE_ORDER.index("resolve-context") - 1)

    def test_a_registered_identity_passes_and_an_invented_one_does_not(self):
        command = gate_check("scope-gate", "registered-identity")
        tool = ROOT / "tools" / "check-proper-identity"
        if not tool.is_file():
            self.skipTest(f"{tool} is not present in this tree")
        self.assertEqual(run_check(command, DOC, "gpt", ROOT).returncode, 0)
        self.assertEqual(
            run_check(command, UNREGISTERED, "gpt", ROOT).returncode, 1,
            "an identity no mass entry registers names no proper to produce")

    def test_only_a_provider_this_repository_publishes_for_passes(self):
        command = gate_check("scope-gate", "known-provider")
        for provider in ("gpt", "claude"):
            with self.subTest(provider=provider):
                self.assertEqual(
                    run_check(command, DOC, provider, ROOT).returncode, 0)
        for provider in ("", "openai", "gpt ", "../gpt", "gpt;true"):
            with self.subTest(provider=provider):
                self.assertNotEqual(
                    run_check(command, DOC, provider, ROOT).returncode, 0)

    def test_the_gate_refuses_without_authorization_and_passes_with_it(self):
        command = gate_check("scope-gate", "authorized-scope")
        self.assertEqual(run_check(command, DOC, "gpt", self.tree).returncode,
                         1, "the boundary is closed until it is opened")
        self.authorize(DOC, "gpt")
        self.assertEqual(run_check(command, DOC, "gpt", self.tree).returncode,
                         0)

    def test_a_registered_identity_is_not_itself_authorization(self):
        """The two questions are independent, and both are asked.

        This is the whole point of the phase: the registry keeps every
        permanent identity, and an identity with no guide is the normal state
        of a closed collection.
        """
        tool = ROOT / "tools" / "check-proper-identity"
        if not tool.is_file():
            self.skipTest(f"{tool} is not present in this tree")
        registered = run_check(
            gate_check("scope-gate", "registered-identity"), DOC, "gpt", ROOT)
        self.assertEqual(registered.returncode, 0)
        self.assertFalse(self.authorized(DOC, "gpt"))


# ---------------------------------------------------------------------------
# Publication acceptance
# ---------------------------------------------------------------------------

class PublicationAcceptanceTests(unittest.TestCase):
    """Only a wired publication is an accepted run."""

    def setUp(self):
        self.stages = stages()

    def test_the_terminal_gate_is_the_only_stage_that_accepts(self):
        accepting = [stage["id"] for stage in workflow_json()["stages"]
                     if ACCEPTED in (stage.get("next"),
                                     stage.get("pass_transition"))]
        self.assertEqual(accepting, ["publication-gates"])
        gate = self.stages["publication-gates"]
        self.assertEqual(gate["type"], "gate")
        self.assertEqual(gate["execution"], {"mode": PROGRAM})
        self.assertEqual(
            STAGE_ORDER.index("publication-gates"),
            max(STAGE_ORDER.index(stage["id"])
                for stage in workflow_json()["stages"]
                if stage["type"] in ("gate", "evaluator")),
            "the accepting gate must be the last evaluator or gate, because "
            "the acceptance audit requires every other one to have passed")

    def test_artifact_acceptance_does_not_end_the_run(self):
        final = self.stages["final-acceptance"]
        self.assertEqual(final["pass_transition"], "publish-artifacts")
        self.assertNotEqual(final["pass_transition"], ACCEPTED)
        self.assertEqual(
            sorted(check["id"] for check in final["checks"]),
            ["canonical-pdf", "generation-metadata", "proper-components",
             "synthesis-pdf"],
            "artifact acceptance keeps every check it had")

    def test_the_publication_gate_checks_the_whole_publication(self):
        checks = {check["id"]: check["command"]
                  for check in self.stages["publication-gates"]["checks"]}
        self.assertEqual(sorted(checks), [
            "authorized-scope", "canonical-pdf-installed",
            "canonical-release-record", "catalog-links", "generation-metadata",
            "no-synthesis-web-edition", "proper-components",
            "synthesis-pdf-installed", "synthesis-release-record",
            "web-edition-declared", "web-edition-tracked", "web-edition-valid",
        ])
        self.assertIn(PLAN, checks["authorized-scope"])
        self.assertIn("pdf/{provider}/{proper}.pdf",
                      checks["canonical-pdf-installed"])
        self.assertIn("pdf/{provider}/{proper}-synthesis.pdf",
                      checks["synthesis-pdf-installed"])
        self.assertIn("--aux", checks["proper-components"])
        self.assertIn("pdf/{provider}/{proper}.pdf",
                      checks["generation-metadata"])
        self.assertIn("check-web-edition", checks["web-edition-valid"])
        self.assertIn("web/{provider}/{proper}.md", checks["web-edition-tracked"])
        self.assertIn("git ls-files", checks["web-edition-tracked"])
        self.assertIn("web/{provider}/{proper}-synthesis.md",
                      checks["no-synthesis-web-edition"])
        self.assertIn("release/publications/{provider}/{proper}.json",
                      checks["canonical-release-record"])
        self.assertIn(
            "release/publications/{provider}/{proper}-synthesis.json",
            checks["synthesis-release-record"])
        for artifact in ('"](../pdf/" p "/" d ".pdf)"',
                         '"](../pdf/" p "/" d "-synthesis.pdf)"',
                         '"](../web/" p "/" d ".html)"'):
            self.assertIn(artifact, checks["catalog-links"])

    def test_a_hostile_identity_cannot_escape_a_gate_command(self):
        """A document id is data. It is never a place to continue the command.

        `_substitute_args` shell-quotes every value, but a template that wraps
        its own placeholder in quotes cancels that: the value's opening quote
        closes the template's literal and the rest of the id is read as shell.
        That is not hypothetical. Before this test, `authorized-scope` read

            grep -qF -- 'provider `{provider}`, identity `{proper}`' PLAN

        and an id ending in a backticked command ran it, as the maintainer of
        this repository confirmed by execution. Assert the property rather than
        any one template: whatever a check is written as, a hostile id must
        survive substitution as inert data.
        """
        payloads = (
            "x`touch /tmp/triptych-gate-escape`",
            "x$(touch /tmp/triptych-gate-escape)",
            "x; touch /tmp/triptych-gate-escape",
            "x' ; touch /tmp/triptych-gate-escape ; '",
        )
        gates = [stage for stage in workflow_json()["stages"]
                 if stage["type"] == "gate"]
        self.assertTrue(gates)
        for stage in gates:
            for check in stage.get("checks", []):
                if "{proper}" not in check["command"]:
                    continue
                for payload in payloads:
                    with self.subTest(gate=stage["id"], check=check["id"],
                                      payload=payload):
                        rendered = _substitute_args(
                            check["command"],
                            {"proper": payload, "provider": "claude"},
                            quote=True)
                        tokens = shlex.split(rendered)
                        self.assertTrue(
                            any(payload in token for token in tokens),
                            f"{stage['id']}/{check['id']}: the id did not "
                            f"survive substitution as inert data")
                        self.assertNotIn(
                            "touch", tokens,
                            f"{stage['id']}/{check['id']}: the payload split "
                            f"apart, so part of the id became a shell word")

    def test_the_installed_artifacts_are_checked_not_the_built_ones(self):
        """A build-tree check would accept a publication nobody installed."""
        checks = {check["id"]: check["command"]
                  for check in self.stages["publication-gates"]["checks"]}
        for check_id in ("canonical-pdf-installed", "synthesis-pdf-installed",
                         "generation-metadata"):
            with self.subTest(check=check_id):
                self.assertNotIn("build/{provider}/{proper}.pdf",
                                 checks[check_id])

    def test_the_publication_checks_are_shell_commands_judged_by_exit_code(self):
        for gate_id in ("scope-gate", "publication-gates"):
            for check in self.stages[gate_id]["checks"]:
                with self.subTest(gate=gate_id, check=check["id"]):
                    self.assertIsInstance(check["command"], str)
                    self.assertNotIn("\n", check["command"])
                    self.assertTrue(check["required_result"].strip())

    def test_every_acceptance_path_runs_the_gates_that_matter(self):
        """Remove one gate's pass edge and ACCEPTED becomes unreachable.

        A stage list says what exists; this says what a run must go through.
        Each of these is on every path from the seed to acceptance, so no
        run reaches ACCEPTED with its scope unchecked, its artifacts
        unaccepted, or its web edition unjudged.
        """
        workflow = workflow_json()
        first = workflow["stages"][0]["id"]

        def reachable(without: tuple[str, str] | None) -> set[str]:
            edges: dict[str, list[str]] = {}
            for stage in workflow["stages"]:
                targets = []
                for key in ("next", "pass_transition", "fail_transition"):
                    if key in stage and (stage["id"], key) != without:
                        targets.append(stage[key])
                for route in stage.get("repair_routes", []) or []:
                    targets.append(route["transition"])
                edges[stage["id"]] = targets
            seen, queue = set(), [first]
            while queue:
                node = queue.pop()
                if node in seen:
                    continue
                seen.add(node)
                queue.extend(edges.get(node, []))
            return seen

        self.assertIn(ACCEPTED, reachable(None))
        for stage_id in ("scope-gate", "final-acceptance", "web-evaluation",
                         "publication-gates"):
            with self.subTest(stage=stage_id):
                self.assertNotIn(
                    ACCEPTED, reachable((stage_id, "pass_transition")),
                    f"a run can reach ACCEPTED without {stage_id} passing")

    def test_a_web_fidelity_failure_routes_to_regeneration_only(self):
        web = self.stages["web-evaluation"]
        self.assertEqual(web["type"], "evaluator")
        self.assertEqual(web["execution"], {"mode": SINGLE})
        self.assertEqual(web["result_schema"], "evaluator-result.json")
        self.assertEqual(web["pass_transition"], "install-publication")
        self.assertEqual(web["fail_transition"], "web-revision")
        self.assertNotIn("repair_routes", web,
                         "a fidelity defect has one owner, so it needs no "
                         "classification")
        revision = self.stages["web-revision"]
        self.assertEqual(revision["type"], "bounded-revision")
        self.assertEqual(revision["revision_target"], "generate-web")
        self.assertEqual(revision["next"], "web-evaluation")
        self.assertIn("max_iterations", web)

    def test_a_publication_defect_is_repaired_where_it_was_installed(self):
        gate = self.stages["publication-gates"]
        self.assertEqual(gate["fail_transition"], "publication-revision")
        revision = self.stages["publication-revision"]
        self.assertEqual(revision["type"], "bounded-revision")
        self.assertEqual(revision["revision_target"], "install-publication")
        self.assertEqual(revision["next"], "publication-gates")
        for stage_id in ("publication-revision", "web-revision"):
            with self.subTest(stage=stage_id):
                self.assertNotIn(
                    self.stages[stage_id]["next"],
                    ("research", "author-proper", "content-evaluation"),
                    "a wiring defect never goes back through authoring")

    def test_the_web_evaluator_names_its_own_finding_space(self):
        text = (FRAGMENTS / "propers" / "web-evaluation.md").read_text(
            encoding="utf-8")
        self.assertIn("`WEB-` prefix", text)
        for foreign in ("VIS-", "CON-", "SCR-", "PAT-"):
            self.assertNotIn(foreign, text,
                             f"web evaluation names {foreign}, another "
                             f"stage's finding space")


# ---------------------------------------------------------------------------
# What version 9 did not change
# ---------------------------------------------------------------------------

class PreservedGuaranteeTests(unittest.TestCase):
    """The production phase is exactly as it was."""

    def setUp(self):
        self.stages = stages()

    def test_the_host_max_lane_rosters_are_unchanged(self):
        for stage_id, lanes in (("research", RESEARCH_LANES),
                                ("content-evaluation", CONTENT_LANES),
                                ("visual-evaluation", VISUAL_LANES)):
            with self.subTest(stage=stage_id):
                execution = self.stages[stage_id]["execution"]
                self.assertEqual(execution["mode"], FANOUT)
                self.assertEqual(execution["parallelism"], HOST_MAX)
                self.assertEqual(execution["join"], STRICT_UNION)
                self.assertEqual([lane["id"] for lane in execution["lanes"]],
                                 lanes)
        fanouts = {stage["id"] for stage in workflow_json()["stages"]
                   if stage["execution"]["mode"] == FANOUT}
        self.assertEqual(fanouts, {"research", "content-evaluation",
                                   "visual-evaluation"},
                         "the publication phase added no fan-out")

    def test_content_evaluation_is_still_the_only_routed_stage(self):
        """The publication phase added no route; version 10 added one owner.

        `brief` was inserted between the two owners this test was written
        for, and it routes to the brief's sole writer. Everything else the
        guarantee covers is unchanged: the order, the two outer owners, and
        the fact that exactly one stage routes at all.
        """
        self.assertEqual(self.stages["content-evaluation"]["repair_routes"], [
            {"repair_target": "research", "transition": "research"},
            {"repair_target": "brief", "transition": "research-synthesis"},
            {"repair_target": "authoring", "transition": "content-revision"},
        ])
        routed = [stage["id"] for stage in workflow_json()["stages"]
                  if stage.get("repair_routes")]
        self.assertEqual(routed, ["content-evaluation"])

    def test_research_synthesis_is_still_the_sole_writer_of_the_brief(self):
        self.assertEqual(self.stages["research-synthesis"]["execution"],
                         {"mode": SINGLE})
        owners = []
        for stage in workflow_json()["stages"]:
            for fragment in stage.get("fragments", []):
                text = (FRAGMENTS / fragment).read_text(encoding="utf-8")
                if "research/scope.md" in text and stage["id"] not in owners:
                    owners.append(stage["id"])
        self.assertNotIn("authorize-target", owners)
        for stage_id in ("publish-artifacts", "generate-web",
                         "install-publication", "web-revision",
                         "publication-revision"):
            with self.subTest(stage=stage_id):
                self.assertNotIn(
                    stage_id, owners,
                    "no publication stage may reach into the research brief")

    def test_the_scope_entry_has_exactly_one_writer(self):
        writers = [stage["id"] for stage in workflow_json()["stages"]
                   for fragment in stage.get("fragments", [])
                   if PLAN in (FRAGMENTS / fragment).read_text(
                       encoding="utf-8")]
        self.assertEqual(writers, ["authorize-target"],
                         "the production plan is a maintainer record with one "
                         "owning stage")

    def test_the_seed_is_still_byte_idempotent_at_the_current_version(self):
        """Version-agnostic on purpose.

        Which version is current is pinned once, by
        `test_the_workflow_version_matches_the_operator_manual` against
        OPERATOR.md. Pinning it a second time here only meant that every bump
        edited a test about byte idempotency, which is not what this is about.
        """
        name = self.id().rsplit(".", 1)[-1]
        runs = ROOT / "build" / f"tpt-runs-scope-{os.getpid()}-{name}"
        shutil.rmtree(runs, ignore_errors=True)
        runs.mkdir(parents=True, exist_ok=True)
        self.addCleanup(shutil.rmtree, runs, ignore_errors=True)
        engine = WorkflowEngine(ROOT, ROOT / "workflows")
        engine.runs_dir = runs

        args = {"proper": DOC, "provider": "gpt"}
        first = engine.seed_bytes("proper", args)
        run_dir = engine.run_dir(json.loads(first)["run_id"])
        before = {path.relative_to(run_dir).as_posix(): path.read_bytes()
                  for path in sorted(run_dir.rglob("*")) if path.is_file()}
        self.assertEqual(engine.seed_bytes("proper", args), first)
        after = {path.relative_to(run_dir).as_posix(): path.read_bytes()
                 for path in sorted(run_dir.rglob("*")) if path.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(json.loads(first)["workflow_version"],
                         workflow_json()["version"])
        self.assertEqual(json.loads(first)["stage"], "seed")

    def test_every_new_fragment_exists_and_is_declared(self):
        declared = {fragment for stage in workflow_json()["stages"]
                    for fragment in stage.get("fragments", [])}
        for name in ("authorize-target", "publish-artifacts", "generate-web",
                     "web-evaluation", "web-revision", "install-publication",
                     "publication-revision"):
            with self.subTest(fragment=name):
                path = FRAGMENTS / "propers" / f"{name}.md"
                self.assertTrue(path.is_file(), f"{name}.md is missing")
                self.assertTrue(path.read_text(encoding="utf-8").strip())
                self.assertIn(f"propers/{name}.md", declared)


if __name__ == "__main__":
    unittest.main()
