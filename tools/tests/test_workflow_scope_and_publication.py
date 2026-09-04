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
            "canonical-release-record", "catalog-links",
            "catalog-read-link-resolves", "generation-metadata",
            "installed-pdf-matches-accepted", "no-synthesis-web-edition",
            "other-provider-cell-unchanged", "proper-components",
            "publication-marker", "release-record-valid",
            "site-document-catalogue", "site-public-alpha",
            "site-release-bindings", "site-web-editions-current",
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
        checked = 0
        for stage in gates:
            for check in stage.get("checks", []):
                # Every name the command carries, the document id and the
                # run's own identity alike. A gate command may name the run it
                # belongs to -- `{run.workflow_digest}` and its four siblings
                # -- and those values are engine-generated, which is not a
                # reason to substitute them differently. The property is the
                # property: whatever a check is written as, a hostile value in
                # any of its names must survive as inert data.
                names = sorted(set(re.findall(
                    r"\{([A-Za-z_][A-Za-z0-9_.]*)\}", check["command"])))
                if not names:
                    continue
                for name in names:
                    for payload in payloads:
                        with self.subTest(gate=stage["id"],
                                          check=check["id"], name=name,
                                          payload=payload):
                            args = {"proper": DOC, "provider": "claude"}
                            args.update({
                                other: "inert" for other in names
                                if other not in args})
                            args[name] = payload
                            rendered = _substitute_args(
                                check["command"], args, quote=True)
                            tokens = shlex.split(rendered)
                            self.assertTrue(
                                any(payload in token for token in tokens),
                                f"{stage['id']}/{check['id']}: {name} did not "
                                f"survive substitution as inert data")
                            self.assertNotIn(
                                "touch", tokens,
                                f"{stage['id']}/{check['id']}: the payload "
                                f"split apart, so part of {name} became a "
                                f"shell word")
                            checked += 1
        self.assertGreater(checked, 0, "no gate command was substituted")

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
# What the gate proves about the publication it is looking at
# ---------------------------------------------------------------------------

CATALOG = "library/traditional-latin-mass.md"
MANIFEST = "release/public-alpha.json"
RECORDS = "release/publications"


def cell(provider: str, proper: str) -> str:
    """This provider's wired cell, in the form `guidance/repository.md` fixes."""
    return (f"[Full PDF](../pdf/{provider}/{proper}.pdf)"
            f" \u00b7 [Synthesis PDF](../pdf/{provider}/{proper}-synthesis.pdf)"
            f" \u00b7 [Read](../web/{provider}/{proper}.html)")


def marker(provider: str, proper: str, primary: str) -> str:
    """The stable marker: bare for the primary provider, prefixed otherwise."""
    label = proper if provider == primary else f"{provider}:{proper}"
    return f"<!-- triptych-publication-id: {label} -->"


def release_record(proper: str, **overrides) -> str:
    """One publication record, in the bytes `release-bindings` writes."""
    entry = {"schema_version": 1, "id": proper, "catalog": CATALOG,
             "status": "alpha",
             "authorization": "perpetual-public-repository-2026"}
    entry.update(overrides)
    return json.dumps(entry, indent=2) + "\n"


class PublicationTree(unittest.TestCase):
    """A throwaway tree holding only what the check under test reads.

    The real catalog, manifest and release records describe publications a
    maintainer decided on, so no test here writes to them; each check is run
    from a directory that carries a fixture of exactly the files it opens.
    """

    PRIMARY = "gpt"
    PROVIDER = "claude"
    OTHER = "gpt"

    def setUp(self):
        self.tree = Path(tempfile.mkdtemp(prefix="tpt-publication-"))
        self.addCleanup(shutil.rmtree, self.tree, ignore_errors=True)
        self.write(MANIFEST, json.dumps(
            {"schema_version": 1, "release_id": "fixture",
             "provider": self.PRIMARY, "providers": ["gpt", "claude"]},
            indent=2) + "\n")

    def write(self, relative: str, text: str) -> Path:
        path = self.tree / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def write_bytes(self, relative: str, data: bytes) -> Path:
        path = self.tree / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def write_catalog(self, markers, rows) -> None:
        body = ["# Traditional Latin Mass", "", *markers, "",
                "| ID | Sunday | ChatGPT | Claude |",
                "| ---: | --- | --- | --- |"]
        body += [f"| {number} | **{name}** | {gpt} | {claude} |"
                 for number, name, gpt, claude in rows]
        self.write(CATALOG, "\n".join(body) + "\n")

    def wire(self, proper: str = DOC, provider: str | None = None,
             other: str | None = None, times: int = 1) -> None:
        """The catalog as `install-publication` leaves it.

        `times` repeats the whole wiring — marker and row — which is what an
        install that ran twice without reading what it had already written
        would produce.
        """
        provider = provider or self.PROVIDER
        mine = cell(provider, proper)
        other = "Planned" if other is None else other
        gpt, claude = (mine, other) if provider == "gpt" else (other, mine)
        markers, rows = [], []
        for _ in range(times):
            markers.append(marker(provider, proper, self.PRIMARY))
            rows.append(("54", "Fourteenth Sunday after Pentecost",
                         gpt, claude))
        self.write_catalog(markers, rows)

    def check(self, check_id: str, proper: str = DOC,
              provider: str | None = None) -> int:
        return run_check(gate_check("publication-gates", check_id), proper,
                         provider or self.PROVIDER, self.tree).returncode


class InstalledArtifactTests(PublicationTree):
    """Test 18: what is installed is the artifact that was accepted."""

    def install(self, canonical: bytes, synthesis: bytes,
                built: bytes | None = None,
                built_synthesis: bytes | None = None,
                proper: str = DOC) -> None:
        provider = self.PROVIDER
        if built is not None:
            self.write_bytes(f"build/{provider}/{proper}.pdf", built)
        if built_synthesis is not None:
            self.write_bytes(f"build/{provider}/{proper}-synthesis.pdf",
                             built_synthesis)
        self.write_bytes(f"pdf/{provider}/{proper}.pdf", canonical)
        self.write_bytes(f"pdf/{provider}/{proper}-synthesis.pdf", synthesis)

    def test_the_installed_pdfs_are_the_accepted_builds(self):
        self.install(b"%PDF canonical", b"%PDF synthesis",
                     built=b"%PDF canonical", built_synthesis=b"%PDF synthesis")
        self.assertEqual(self.check("installed-pdf-matches-accepted"), 0)

    def test_an_installed_canonical_pdf_that_is_not_the_accepted_one_fails(self):
        self.install(b"%PDF rebuilt after acceptance", b"%PDF synthesis",
                     built=b"%PDF canonical", built_synthesis=b"%PDF synthesis")
        self.assertNotEqual(
            self.check("installed-pdf-matches-accepted"), 0,
            "a file at the publication path is not the accepted artifact")

    def test_an_installed_synthesis_pdf_from_another_build_fails(self):
        self.install(b"%PDF canonical", b"%PDF stale synthesis",
                     built=b"%PDF canonical", built_synthesis=b"%PDF synthesis")
        self.assertNotEqual(self.check("installed-pdf-matches-accepted"), 0)

    def test_an_install_with_no_accepted_build_to_compare_against_fails(self):
        """The comparison is the proof, so it cannot be skipped when absent.

        The gate already reads `build/{provider}/{proper}-synthesis.aux` for
        `proper-components`, so the accepted build tree is present when this
        gate runs; a run that has lost it has lost the evidence, and the
        publication is unproven rather than proven.
        """
        self.install(b"%PDF canonical", b"%PDF synthesis")
        self.assertNotEqual(self.check("installed-pdf-matches-accepted"), 0)

    def test_the_check_compares_the_build_tree_against_the_publication_tree(self):
        command = gate_check("publication-gates",
                             "installed-pdf-matches-accepted")
        self.assertIn("cmp -s build/{provider}/{proper}.pdf "
                      "pdf/{provider}/{proper}.pdf", command)
        self.assertIn("build/{provider}/{proper}-synthesis.pdf", command)


class ReleaseRecordContentTests(PublicationTree):
    """Test 22: the record is validated, not merely counted."""

    def records(self, canonical: str | None = None,
                synthesis: str | None = None, proper: str = DOC) -> None:
        root = f"{RECORDS}/{self.PROVIDER}"
        if canonical is not None:
            self.write(f"{root}/{proper}.json", canonical)
        if synthesis is not None:
            self.write(f"{root}/{proper}-synthesis.json", synthesis)

    def test_a_pair_of_records_describing_this_publication_passes(self):
        self.records(release_record(DOC),
                     release_record(f"{DOC}-synthesis"))
        self.assertEqual(self.check("release-record-valid"), 0)

    def test_a_record_naming_another_leaf_fails(self):
        self.records(release_record(NEIGHBOUR),
                     release_record(f"{DOC}-synthesis"))
        self.assertNotEqual(self.check("release-record-valid"), 0)

    def test_the_synthesis_record_must_name_the_synthesis(self):
        self.records(release_record(DOC), release_record(DOC))
        self.assertNotEqual(
            self.check("release-record-valid"), 0,
            "a companion record naming the canonical leaf is the canonical "
            "record written twice")

    def test_a_record_pointing_at_another_catalog_fails(self):
        self.records(release_record(DOC, catalog="library/liturgy.md"),
                     release_record(f"{DOC}-synthesis"))
        self.assertNotEqual(self.check("release-record-valid"), 0)

    def test_a_held_record_is_not_a_published_one(self):
        self.records(release_record(DOC, status="hold", authorization=None),
                     release_record(f"{DOC}-synthesis"))
        self.assertNotEqual(
            self.check("release-record-valid"), 0,
            "`hold` carries a null authorization and publishes nothing")

    def test_a_record_at_an_unknown_schema_version_fails(self):
        self.records(release_record(DOC, schema_version=2),
                     release_record(f"{DOC}-synthesis"))
        self.assertNotEqual(self.check("release-record-valid"), 0)

    def test_a_missing_companion_record_fails(self):
        self.records(release_record(DOC))
        self.assertNotEqual(self.check("release-record-valid"), 0)


class CatalogWiringTests(PublicationTree):
    """Tests 24 and 26: one cell is wired, and the row says whose it is."""

    def test_a_wired_cell_beside_a_planned_one_passes(self):
        self.wire()
        self.assertEqual(self.check("other-provider-cell-unchanged"), 0)

    def test_a_wired_cell_beside_the_other_provider_own_links_passes(self):
        self.wire(other=cell(self.OTHER, DOC))
        self.assertEqual(
            self.check("other-provider-cell-unchanged"), 0,
            "the other provider publishing the same identity is the normal "
            "state of a row both providers have produced")

    def test_this_provider_links_in_the_other_provider_cell_fail(self):
        """Test 24. Publishing one provider wires one cell."""
        self.wire(other=cell(self.PROVIDER, DOC))
        self.assertNotEqual(
            self.check("other-provider-cell-unchanged"), 0,
            "the same provider cannot own both cells of one row")

    def test_a_blanked_other_provider_cell_fails(self):
        self.wire(other="")
        self.assertNotEqual(
            self.check("other-provider-cell-unchanged"), 0,
            "a cell emptied by this publication is a cell this publication "
            "changed; `Planned` is the closed state, not blank")

    def test_the_other_provider_cell_keeps_its_own_word(self):
        self.wire(other="Coming soon")
        self.assertNotEqual(
            self.check("other-provider-cell-unchanged"), 0,
            "the closed state is the bare word `Planned`")

    def test_the_marker_for_a_secondary_provider_is_prefixed(self):
        """Test 26."""
        self.wire()
        self.assertEqual(self.check("publication-marker"), 0)

    def test_a_bare_marker_does_not_stand_for_a_secondary_provider(self):
        """Test 26. The bare id is the primary provider's publication."""
        self.wire()
        catalog = (self.tree / CATALOG).read_text(encoding="utf-8")
        self.write(CATALOG, catalog.replace(
            marker(self.PROVIDER, DOC, self.PRIMARY),
            marker(self.PRIMARY, DOC, self.PRIMARY)))
        self.assertNotEqual(
            self.check("publication-marker"), 0,
            "a marker naming the primary provider says nothing about this one")

    def test_the_primary_provider_marker_is_bare(self):
        self.wire(provider=self.PRIMARY, other="Planned")
        self.assertEqual(
            self.check("publication-marker", provider=self.PRIMARY), 0)

    def test_a_row_with_no_marker_at_all_fails(self):
        self.wire()
        catalog = (self.tree / CATALOG).read_text(encoding="utf-8")
        self.write(CATALOG, catalog.replace(
            marker(self.PROVIDER, DOC, self.PRIMARY) + "\n", ""))
        self.assertNotEqual(self.check("publication-marker"), 0)

    def test_the_read_link_must_sit_in_this_provider_own_row(self):
        """The catalog half of `catalog-read-link-resolves`.

        `catalog-links` sets its three flags anywhere in the file, so three
        different rows satisfy it. This one requires the `Read` link and the
        PDF link on one line.
        """
        command = gate_check("publication-gates", "catalog-read-link-resolves")
        self.wire()
        catalog = self.tree / CATALOG
        text = catalog.read_text(encoding="utf-8")
        rendered = _substitute_args(command, {"proper": DOC,
                                              "provider": self.PROVIDER},
                                    quote=True)
        awk = rendered.split(" && git ls-files")[0]
        self.assertEqual(subprocess.run(awk, shell=True, cwd=self.tree,
                                        capture_output=True).returncode, 0)
        catalog.write_text(
            text.replace(f" \u00b7 [Read](../web/{self.PROVIDER}/{DOC}.html)", ""),
            encoding="utf-8")
        self.assertNotEqual(
            subprocess.run(awk, shell=True, cwd=self.tree,
                           capture_output=True).returncode, 0)

    def test_the_read_link_is_bound_to_the_tracked_markdown_source(self):
        """The site renders the `.html`; the `.md` is what can be tracked.

        `release/public-alpha.json`'s page map turns
        `web/<provider>/<leaf>.md` into `web/<provider>/<leaf>.html` at site
        build time, and no `.html` under `web/` is tracked. So the check
        proves the source the catalog's link is rendered from, and refuses a
        hand-made `.html` sitting beside it.
        """
        command = gate_check("publication-gates", "catalog-read-link-resolves")
        self.assertIn("git ls-files --error-unmatch web/{provider}/{proper}.md",
                      command)
        self.assertIn("test ! -e web/{provider}/{proper}.html", command)
        self.assertEqual(
            len(list((ROOT / "web").rglob("*.html"))), 0,
            "the tracked web tree holds Markdown; the HTML is the build's")

    def test_the_wired_catalog_passes_every_catalog_check_together(self):
        self.wire()
        for check_id in ("catalog-links", "other-provider-cell-unchanged",
                         "publication-marker"):
            with self.subTest(check=check_id):
                self.assertEqual(self.check(check_id), 0)


class PublicationIdempotencyTests(PublicationTree):
    """Test 27: installing and wiring twice converges on one state."""

    def test_wiring_the_same_publication_twice_writes_the_same_catalog(self):
        self.wire()
        once = (self.tree / CATALOG).read_bytes()
        self.wire()
        self.assertEqual((self.tree / CATALOG).read_bytes(), once)
        for check_id in ("catalog-links", "other-provider-cell-unchanged",
                         "publication-marker"):
            with self.subTest(check=check_id):
                self.assertEqual(self.check(check_id), 0)

    def test_a_duplicated_row_is_refused(self):
        self.wire(times=2)
        self.assertNotEqual(
            self.check("other-provider-cell-unchanged"), 0,
            "an identity owns one catalog row; a second is a wiring step "
            "that ran twice without reading what it had written")

    def test_a_duplicated_marker_is_refused(self):
        self.wire()
        catalog = (self.tree / CATALOG).read_text(encoding="utf-8")
        line = marker(self.PROVIDER, DOC, self.PRIMARY)
        self.write(CATALOG, catalog.replace(line, line + "\n" + line, 1))
        self.assertNotEqual(
            self.check("publication-marker"), 0,
            "one publication, one marker")

    def test_reinstalling_the_same_pdfs_still_matches_the_accepted_build(self):
        provider = self.PROVIDER
        for _ in range(2):
            self.write_bytes(f"build/{provider}/{DOC}.pdf", b"%PDF canonical")
            self.write_bytes(f"build/{provider}/{DOC}-synthesis.pdf",
                             b"%PDF synthesis")
            self.write_bytes(f"pdf/{provider}/{DOC}.pdf", b"%PDF canonical")
            self.write_bytes(f"pdf/{provider}/{DOC}-synthesis.pdf",
                             b"%PDF synthesis")
            self.assertEqual(self.check("installed-pdf-matches-accepted"), 0)


class SiteValidationTests(unittest.TestCase):
    """Part XII's broader site validation, run by the gate and not a worker."""

    SITE_CHECKS = {
        "site-release-bindings": "check-release-bindings",
        "site-public-alpha": "check-public-alpha",
        "site-document-catalogue": "check-document-catalogue",
        "site-web-editions-current": "check-web-editions-current",
    }

    def test_the_gate_runs_the_site_checks_itself(self):
        """The Makefile half is asserted as text, not run.

        These four read the entire tracked corpus — every publication record,
        every catalogue row, every web edition — so there is no fixture tree
        to run them against, and running them here would only restate what
        `make check` already runs. What is asserted is that the gate names a
        target the Makefile really declares, so the gate cannot pass by
        invoking nothing.
        """
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        for check_id, target in self.SITE_CHECKS.items():
            with self.subTest(check=check_id):
                command = gate_check("publication-gates", check_id)
                self.assertTrue(command.startswith(f"make {target} && "),
                                command)
                self.assertRegex(makefile, rf"(?m)^{re.escape(target)}:")

    def test_each_site_check_is_bound_to_this_publication(self):
        """A whole-repository check can pass while knowing nothing of a target.

        `tools/tests/test_workflow_engine.py` requires every gate check to
        name one of the run's arguments, and the reason is this one: a
        constant command passes or fails alike for every target. So each site
        check carries a second clause naming the surface that check validated
        and requiring this publication to be inside it — a recorded site
        source, two validated release records, three catalogued artifacts, one
        compared web edition.
        """
        for check_id in self.SITE_CHECKS:
            with self.subTest(check=check_id):
                command = gate_check("publication-gates", check_id)
                clause = command.split(" && ", 1)[1]
                self.assertTrue(
                    "{proper}" in clause and "{provider}" in clause,
                    f"{check_id}'s second clause names no target")

    def test_the_binding_clauses_name_the_surface_each_check_validated(self):
        checks = {check_id: gate_check("publication-gates", check_id)
                  for check_id in self.SITE_CHECKS}
        self.assertIn("web/{provider}/{proper}.md release/public-alpha.json",
                      checks["site-release-bindings"])
        self.assertIn("release/publications/{provider}/{proper}.json",
                      checks["site-public-alpha"])
        self.assertIn("release/publications/{provider}/{proper}-synthesis.json",
                      checks["site-public-alpha"])
        corpus = "src/web/data/structure/documents/corpus.json"
        self.assertIn(corpus, checks["site-document-catalogue"])
        self.assertTrue((ROOT / corpus).is_file())
        self.assertIn("web/{provider}/{proper}.md",
                      checks["site-web-editions-current"])

    def test_the_corpus_clause_finds_a_published_proper_and_not_an_unwired_one(self):
        """Run the clause the document catalogue check carries, alone.

        The `make` half is the slow, whole-repository one; the clause is what
        binds it to this publication, and it is run here against the real
        tracked corpus for a published identity and for the unpublished
        neighbour of one.
        """
        command = gate_check("publication-gates", "site-document-catalogue")
        clause = command.split(" && ", 1)[1]
        corpus = json.loads(
            (ROOT / "src/web/data/structure/documents/corpus.json").read_text(
                encoding="utf-8"))
        published = None
        for work in corpus.get("works", []):
            leaf = work.get("leaf", "")
            if "/propers/temporal/" not in leaf:
                continue
            for edition in work.get("editions", []):
                web = edition.get("web") or ""
                pdf = edition.get("pdf") or ""
                companions = [also.get("pdf") or ""
                              for also in edition.get("also", [])]
                if (web.endswith(f"{leaf}.html") and pdf.endswith(f"{leaf}.pdf")
                        and any(also.endswith(f"{leaf}-synthesis.pdf")
                                for also in companions)):
                    published = (web.split("/")[1], leaf)
                    break
            if published:
                break
        if published is None:
            self.skipTest("no catalogued proper edition in this tree")
        provider, proper = published
        self.assertEqual(
            run_check(clause, proper, provider, ROOT).returncode, 0)
        self.assertNotEqual(
            run_check(clause, UNREGISTERED, provider, ROOT).returncode, 0,
            "an identity the corpus does not carry is not catalogued")

    def test_the_installer_no_longer_attests_to_them(self):
        """The authority is the gate's, and it is not held in two places."""
        fragment = (FRAGMENTS / "propers" / "install-publication.md").read_text(
            encoding="utf-8")
        for target in self.SITE_CHECKS.values():
            with self.subTest(target=target):
                self.assertNotIn(
                    f"make {target}", fragment,
                    f"{target} is a gate check; the fragment must not ask a "
                    f"worker to run it and report that it passed")
        self.assertIn("make refresh-release-bindings ADOPT=1", fragment,
                      "the one step that writes stays with the installer")
        publish = (FRAGMENTS / "propers" / "publish-artifacts.md").read_text(
            encoding="utf-8")
        self.assertNotIn(
            "cmp build/", publish,
            "the byte comparison is `installed-pdf-matches-accepted`, not "
            "prose a worker confirms")


class IdentityOwnershipTests(unittest.TestCase):
    """Test 4: the workflow keeps no identity list of its own."""

    def test_the_pipeline_carries_no_hand_maintained_list_of_propers(self):
        text = (ROOT / "workflows" / "pipelines" / "proper.json").read_text(
            encoding="utf-8")
        found = re.findall(
            r"liturgy/roman-rite/1962/propers/[a-z]+/[0-9]{2}-[a-z-]+", text)
        self.assertLessEqual(
            len(set(found)), 1,
            f"the pipeline names {sorted(set(found))}; a second identity is "
            f"the beginning of a duplicate registry")

    def test_the_pipeline_names_an_identity_only_as_an_example(self):
        workflow = workflow_json()
        description = workflow["argument_schema"]["proper"]["description"]
        self.assertIn("e.g.", description,
                      "the one id the pipeline states is an example of the "
                      "argument's shape, not a member of a permitted set")
        for stage in workflow["stages"]:
            for check in stage.get("checks", []):
                with self.subTest(check=check["id"]):
                    self.assertNotIn(
                        "propers/temporal/", check["command"],
                        "no gate may decide identity from a literal written "
                        "into the pipeline")

    def test_identity_is_decided_by_the_registry_tool(self):
        command = gate_check("scope-gate", "registered-identity")
        self.assertIn("check-proper-identity", command)
        self.assertIn("{proper}", command)
        self.assertTrue((ROOT / "tools" / "check-proper-identity").is_file())


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
        engine.standing_findings_root = runs / "standing"

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
