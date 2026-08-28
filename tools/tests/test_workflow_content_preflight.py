#!/usr/bin/env python3
"""A shell decides what a shell can decide, before five AI lanes are spent.

Two rounds of a production run spent a five-lane content evaluation
discovering References entries the body never cites, a cited source
identifier that resolved to nothing, a manifest relation the brief restated
with the wrong element keys, and a witness quoted in a guide that says four
times it does not quote him. None of those is a judgment. `content-preflight`
runs between `author-proper` and `content-evaluation` and settles them by exit
code, so the evaluation behind it spends its budget on what only judgment can
settle.

Its failures go to `content-revision` and never to research. A mechanical
defect in the leaf is repaired in the leaf; nothing about it says the evidence
under the leaf is wrong, and routing it to `research` would re-run seven lanes
over a defect grep found.
"""
import json
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
    BLOCKED,
    FAIL,
    PASS,
    PROGRAM,
    _current_packet,
    _substitute_args,
)
from test_workflow_research_fanout import (  # noqa: E402
    DOC,
    STAGE_ORDER,
    workflow_json,
)
from test_workflow_repair_routing import (  # noqa: E402
    RESEARCH,
    RoutingCase,
    blocking,
)

STAGE = "content-preflight"
TOOL = "check-content-preflight"
CHECKS = ("references-used", "identifiers-resolve",
          "restricted-not-reproduced", "relation-coverage",
          "unquoted-not-quoted")
# A leaf the whole evaluation loop has already accepted, in the provider the
# rest of the workflow suite drives runs against.
PUBLISHED = ("gpt", DOC)


def stage() -> dict:
    return {s["id"]: s for s in workflow_json()["stages"]}[STAGE]


def check_commands() -> dict[str, str]:
    return {check["id"]: check["command"] for check in stage()["checks"]}


class TopologyTests(unittest.TestCase):
    """Where the gate sits, and where a failure of it may go."""

    def test_the_gate_sits_between_the_author_and_the_evaluation(self):
        order = [s["id"] for s in workflow_json()["stages"]]
        self.assertEqual(order, STAGE_ORDER)
        self.assertEqual(order[order.index("author-proper") + 1], STAGE)
        self.assertEqual(order[order.index(STAGE) + 1], "content-evaluation")
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        self.assertEqual(stages["author-proper"]["next"], STAGE)

    def test_it_is_a_program_gate_with_a_bounded_loop(self):
        declared = stage()
        self.assertEqual(declared["type"], "gate")
        self.assertEqual(declared["execution"], {"mode": PROGRAM})
        self.assertEqual(declared["pass_transition"], "content-evaluation")
        self.assertEqual(declared["fail_transition"], "content-revision")
        self.assertEqual(declared["max_iterations"], 3)
        self.assertNotIn("fragments", declared,
                         "a program gate asks no agent anything")
        self.assertNotIn("repair_routes", declared,
                         "a mechanical defect has one owner, so it needs no "
                         "classification")

    def test_a_preflight_failure_never_reaches_research(self):
        """The repair is in the leaf, so it is made in the leaf.

        Reachability, not just the declared transition: whatever
        `content-revision` does next must not be a research stage either, or
        the gate would be a slow road back to the seven lanes.
        """
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        failure = stages[STAGE]["fail_transition"]
        self.assertEqual(failure, "content-revision")
        revision = stages[failure]
        self.assertEqual(revision["type"], "bounded-revision")
        self.assertEqual(revision["revision_target"], "author-proper")
        # The reviser re-enters the gate, not the evaluation behind it, so a
        # mechanical defect's repair is checked mechanically. Sending it
        # straight to `content-evaluation` would spend five AI lanes on a
        # document whose preflight failure may still stand.
        self.assertEqual(revision["next"], STAGE)
        for key in ("next", "pass_transition", "fail_transition"):
            self.assertNotEqual(revision.get(key), "research")
            self.assertNotEqual(revision.get(key), "research-synthesis")

    def test_every_check_is_one_command_over_the_run_s_own_arguments(self):
        commands = check_commands()
        self.assertEqual(list(commands), list(CHECKS),
                         "the five checks the design names, in order")
        registry = json.loads(
            (ROOT / "tmt.json").read_text(encoding="utf-8"))["tools"]
        for check_id, command in commands.items():
            with self.subTest(check=check_id):
                self.assertIn(f"tools/tpt {TOOL} ", command)
                self.assertIn(TOOL, registry,
                              "a gate may only run a registered tool")
                self.assertIn(f"--check {check_id}", command)
                residue = command.replace("{proper}", "").replace(
                    "{provider}", "")
                self.assertNotRegex(
                    residue, r"\{[A-Za-z_][A-Za-z0-9_]*\}",
                    "the gate takes an argument the run has not normalized")
                for shell in ("&&", "||", ";", "|"):
                    self.assertNotIn(
                        shell, command,
                        "each check is one command, judged by its own exit "
                        "code")

    def test_a_hostile_identity_survives_as_data(self):
        """The property fab7db40b established, held for the new checks too.

        A template that wraps its own placeholder in quotes cancels the
        shell-quoting `_substitute_args` applies, and the rest of the id is
        read as shell. The suite asserts this over every gate; it is asserted
        here as well because these four commands are the newest place it
        could be got wrong.
        """
        payloads = (
            "x`touch /tmp/triptych-preflight-escape`",
            "x$(touch /tmp/triptych-preflight-escape)",
            "x; touch /tmp/triptych-preflight-escape",
            "x' ; touch /tmp/triptych-preflight-escape ; '",
        )
        for check_id, command in check_commands().items():
            for payload in payloads:
                with self.subTest(check=check_id, payload=payload):
                    rendered = _substitute_args(
                        command, {"proper": payload, "provider": "claude"},
                        quote=True)
                    tokens = shlex.split(rendered)
                    self.assertTrue(
                        any(payload in token for token in tokens),
                        "the id did not survive substitution as inert data")
                    self.assertNotIn("touch", tokens,
                                     "part of the id became a shell word")


class CheckBehaviourTests(unittest.TestCase):
    """Each check, over a leaf that satisfies it and one that does not.

    The passing case is a real published leaf every time. A check that only
    ever ran against a fixture would be free to be wrong about the corpus.
    """

    maxDiff = None

    def setUp(self):
        self.tree = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tree, ignore_errors=True)
        self.leaf = self.tree / "src" / "claude" / "probe"
        self.leaf.mkdir(parents=True)
        library = self.tree / "src" / "sources" / "works" / "probe"
        library.mkdir(parents=True)
        (library / "work.toml").write_text(
            'id = "work.catholic-church.missale-romanum"\n', encoding="utf-8")
        self.write_library()
        self.write_leaf()
        self.write_manifest(['"introit"', '"collect"'])
        self.write_bindings()

    # One public-domain witness and one restricted one, each reached the way
    # a real binding reaches it: the public-domain artifact directly, the
    # restricted one through the passage record that names its artifact.
    PUBLIC_ARTIFACT = ("artifact.english-college-of-douay.douay-rheims-bible."
                       "challoner-1749.verse-text")
    RESTRICTED_PASSAGE = (
        "passage.united-states-conference-of-catholic-bishops."
        "new-american-bible-revised-edition.usccb-web-2026-08-21.galatians")
    RESTRICTED_ARTIFACT = (
        "artifact.united-states-conference-of-catholic-bishops."
        "new-american-bible-revised-edition.usccb-web-2026-08-21.galatians")

    def write_library(self):
        library = self.tree / "src" / "sources" / "works" / "probe"
        (library / "douay.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.PUBLIC_ARTIFACT}"\n'
            'storage = "tracked"\n'
            'rights_status = "public-domain"\n', encoding="utf-8")
        (library / "nabre-artifact.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.RESTRICTED_ARTIFACT}"\n'
            'storage = "restricted"\n'
            'rights_status = "restricted"\n', encoding="utf-8")
        (library / "nabre-passage.toml").write_text(
            'record_type = "passage"\n'
            f'id = "{self.RESTRICTED_PASSAGE}"\n'
            f'artifact_id = "{self.RESTRICTED_ARTIFACT}"\n', encoding="utf-8")

    def write_bindings(self, restricted_role="context"):
        research = self.leaf / "research"
        research.mkdir(exist_ok=True)
        (research / "source-bindings.toml").write_text(
            'schema = 1\nrecord_type = "bindings"\n\n'
            '[[bindings]]\n'
            f'source_id = "{self.PUBLIC_ARTIFACT}"\n'
            'role = "translation-control"\n\n'
            '[[bindings]]\n'
            f'source_id = "{self.RESTRICTED_PASSAGE}"\n'
            f'role = "{restricted_role}"\n', encoding="utf-8")

    GOOD_TRANSLATION = "English: Douay--Rheims (Challoner), Ps. 8:2"
    GOOD_ID = "work.catholic-church.missale-romanum"

    def write_leaf(self, translation=None, identifier=None, extra=""):
        (self.leaf / "main.tex").write_text(f"""\\section*{{Commentary}}
Augustine, \\work{{Enarrationes in Psalmos}} 8, is read at the Introit.
Guéranger is summarised for the devotional reception only.

\\begin{{namedtranslation}}{{{translation or self.GOOD_TRANSLATION}}}
O Lord our Lord, how admirable is thy name.
\\end{{namedtranslation}}

\\section*{{References}}
\\begin{{itemize}}
\\item Augustine, \\work{{Enarrationes in Psalmos}} 8. Registered in the
repository's source library as \\texttt{{{identifier or self.GOOD_ID}}}.
\\item Prosper Guéranger, \\work{{The Liturgical Year}}, vol.~II.
\\textit{{Cited only as a witness to devotional reception; it supplies no
English printed in this guide.}}
{extra}\\end{{itemize}}
""", encoding="utf-8")

    def write_manifest(self, relation_keys):
        (self.leaf / "proper-components.toml").write_text(f"""schema = 1
record_type = "proper-components"
element_keys = ["introit", "collect", "gospel"]

[[components]]
key = "source-grounded-synthesis"
kind = "source-grounded-synthesis"
path = "main.tex"
element_keys = ["introit", "collect"]

[[relations]]
key = "probe-relation"
element_keys = [{", ".join(relation_keys)}]
evidence = ["source-grounded-synthesis"]
""", encoding="utf-8")

    def probe(self, check):
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--root", str(self.tree),
             "--provider", "claude", "--document", "probe", "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    def published(self, check):
        provider, document = PUBLISHED
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--provider", provider,
             "--document", document, "--check", check],
            capture_output=True, text=True, cwd=ROOT)

    def test_every_check_passes_on_a_published_leaf(self):
        for check in CHECKS:
            with self.subTest(check=check):
                result = self.published(check)
                self.assertEqual(
                    result.returncode, 0,
                    f"{check} refused src/{PUBLISHED[0]}/{PUBLISHED[1]}, a "
                    f"leaf the whole loop has accepted: {result.stderr}")
                self.assertTrue(result.stdout.startswith(f"{check}: "),
                                "a passing check says what it counted")

    def test_the_whole_preflight_passes_on_every_leaf_with_a_manifest(self):
        """Not one leaf: every published one the manifest era produced."""
        checked = 0
        for provider in ("claude", "gpt"):
            root = ROOT / "src" / provider / "liturgy/roman-rite/1962/propers"
            for manifest in sorted(root.glob("*/*/proper-components.toml")):
                document = manifest.parent.relative_to(
                    ROOT / "src" / provider).as_posix()
                with self.subTest(leaf=f"{provider}/{document}"):
                    result = subprocess.run(
                        [str(ROOT / "tools" / TOOL), "--provider", provider,
                         "--document", document],
                        capture_output=True, text=True, cwd=ROOT)
                    self.assertEqual(result.returncode, 0, result.stderr)
                checked += 1
        self.assertGreater(checked, 0, "no published leaf was checked")

    def test_the_probe_leaf_passes_before_anything_is_broken(self):
        for check in CHECKS:
            with self.subTest(check=check):
                self.assertEqual(self.probe(check).returncode, 0,
                                 self.probe(check).stderr)

    def test_references_used_refuses_an_entry_the_body_never_names(self):
        self.write_leaf(extra=(
            "\\item Francis Blomefield, \\work{An Essay towards a "
            "Topographical History of the County of Norfolk}, vol.~4.\n"))
        result = self.probe("references-used")
        self.assertEqual(result.returncode, 1)
        self.assertIn("cited nowhere in the body", result.stderr)
        self.assertIn("Blomefield", result.stderr,
                      "the refusal names the entry it refused")
        for other in ("identifiers-resolve", "relation-coverage",
                      "unquoted-not-quoted"):
            with self.subTest(check=other):
                self.assertEqual(self.probe(other).returncode, 0,
                                 "one defect refused one check")

    # --- restricted-not-reproduced --------------------------------------

    def test_restricted_refuses_a_restricted_translation_control(self):
        """The leaf declares the reproduction, in its own binding record.

        `translation-control` is the role that says the published English is
        this witness's words. Against an artifact registered `restricted` it
        is a contradiction between two files, and neither file shows it.
        """
        self.write_bindings(restricted_role="translation-control")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1)
        self.assertIn("bound as translation-control", result.stderr)
        self.assertIn("registered restricted", result.stderr)
        self.assertIn(self.RESTRICTED_PASSAGE, result.stderr,
                      "the refusal names the source it refused")

    def test_restricted_refuses_a_set_passage_credited_to_restricted_bytes(self):
        """The leaf prints it, whatever role the binding claims.

        The binding still says `context` — summarised, not reproduced — and
        the leaf prints a passage over the witness's name anyway. This is the
        shape the earlier production's rights violation actually had.
        """
        self.write_leaf(translation="New American Bible, Revised Edition, "
                                    "Gal. 5:16--24")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1)
        self.assertIn("a set passage is attributed to", result.stderr)
        self.assertIn("may not be reproduced", result.stderr)

    def test_restricted_reads_the_rights_through_the_passage_record(self):
        """The rights are on the artifact; the leaf never names the artifact.

        The binding names a passage, and only the passage's `artifact_id`
        reaches the record that carries `storage`. A check that stopped at the
        bound id would find no rights at all and pass everything.
        """
        library = self.tree / "src" / "sources" / "works" / "probe"
        (library / "nabre-artifact.toml").write_text(
            'record_type = "artifact"\n'
            f'id = "{self.RESTRICTED_ARTIFACT}"\n'
            'storage = "tracked"\n'
            'rights_status = "public-domain"\n', encoding="utf-8")
        self.write_bindings(restricted_role="translation-control")
        self.assertEqual(
            self.probe("restricted-not-reproduced").returncode, 0,
            "with the artifact unrestricted the same binding is lawful")

    def test_restricted_passes_a_public_domain_translation_control(self):
        """The Douay is bound as the translation control and printed. Fine."""
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2 bound sources, 1 of them restricted, none reproduced",
                      result.stdout)

    def test_restricted_ignores_a_word_two_bound_sources_share(self):
        """An attribution that cannot say which source it means says nothing.

        Both bound sources become "bible" here. A word that does not
        discriminate between the leaf's own bindings cannot be evidence that
        the restricted one was the one reproduced.
        """
        self.write_leaf(translation="Bible, Ps. 8:2")
        self.assertEqual(
            self.probe("restricted-not-reproduced").returncode, 0,
            "a shared word must not convict either source")

    def test_a_leaf_local_alias_of_a_printed_passage_is_still_read(self):
        """`format.tex` renames the environment; the passage is still printed.

        Six of the twenty published propers wrap `sourcecard` in a name of
        their own, `54-fourteenth-after-pentecost` — the leaf both production
        runs were producing — among them. A check matching only the base names
        saw zero printed passages in those six. It was not passing them; it
        was not reading them.
        """
        (self.leaf / "format.tex").write_text(
            "\\newenvironment{fulltextenglish}[1]"
            "{\\begin{sourcecard}{#1}\\small}{\\end{sourcecard}}\n",
            encoding="utf-8")
        (self.leaf / "main.tex").write_text(
            (self.leaf / "main.tex").read_text(encoding="utf-8")
            .replace("namedtranslation", "fulltextenglish")
            .replace(self.GOOD_TRANSLATION,
                     "New American Bible, Revised Edition, Gal. 5:16--24"),
            encoding="utf-8")
        result = self.probe("restricted-not-reproduced")
        self.assertEqual(result.returncode, 1,
                         "the alias must not hide the printed passage")
        self.assertIn("a set passage is attributed to", result.stderr)

    def test_identifiers_resolve_refuses_an_unregistered_identifier(self):
        self.write_leaf(identifier="edition.no-such-house.no-such-book.1861")
        result = self.probe("identifiers-resolve")
        self.assertEqual(result.returncode, 1)
        self.assertIn("registered nowhere in src/sources", result.stderr)
        self.assertIn("edition.no-such-house.no-such-book.1861",
                      result.stderr)
        self.assertEqual(self.probe("references-used").returncode, 0)

    def test_an_identifier_broken_for_the_typesetter_is_still_one_id(self):
        """`\\allowbreak` and a line end split the id, not the source.

        A line-at-a-time reader sees `edition.eugene-cummiskey` and calls a
        registered source unregistered. Four published leaves print an id
        this way.
        """
        self.write_leaf(
            identifier="work.catholic-church.\\allowbreak\nmissale-romanum")
        result = self.probe("identifiers-resolve")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 source identifiers", result.stdout)

    def test_relation_coverage_refuses_an_element_the_unit_does_not_claim(self):
        self.write_manifest(['"introit"', '"collect"', '"gospel"'])
        result = self.probe("relation-coverage")
        self.assertEqual(result.returncode, 1)
        self.assertIn("probe-relation", result.stderr)
        self.assertIn("'gospel'", result.stderr,
                      "the refusal names the element that is unclaimed")
        self.assertEqual(self.probe("unquoted-not-quoted").returncode, 0)

    def test_unquoted_not_quoted_refuses_a_contradicted_attribution(self):
        self.write_leaf(translation=(
            "English: Guéranger, \\work{The Liturgical Year}, p.~224"))
        result = self.probe("unquoted-not-quoted")
        self.assertEqual(result.returncode, 1)
        self.assertIn("References declare unquoted", result.stderr)
        self.assertIn("gueranger", result.stderr)
        self.assertEqual(self.probe("references-used").returncode, 0)

    def test_a_missing_manifest_is_a_refusal_and_not_a_vacuous_pass(self):
        (self.leaf / "proper-components.toml").unlink()
        result = self.probe("relation-coverage")
        self.assertEqual(result.returncode, 1)
        self.assertIn("no proper-components.toml", result.stderr)


class DrivenRunTests(RoutingCase):
    """The gate as a run actually meets it."""

    def drive_to_preflight(self, run_id: str | None = None) -> str:
        """Seed if needed, then advance until the run is waiting at the gate."""
        if run_id is None:
            run_id, _ = self.advance_to("research")
            out = self.engine.advance(
                run_id, lane_results=self.lane_submissions(run_id))
            self.assertEqual(out["stage"], "research-synthesis")
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "research-synthesis"))
        self.assertEqual(out["stage"], "author-proper")
        out = self.engine.advance(
            run_id, result_path=self.worker_pass(run_id, "author-proper"))
        self.assertEqual(out["stage"], STAGE,
                         "the author hands the leaf to the preflight")
        return run_id

    def stub_failure(self, check: str, finding_id: str):
        """Answer only this gate with FAIL, leaving every other gate real."""
        real = self.engine._run_gate

        def run_gate(workflow, declared, state, rid):
            if declared["id"] != STAGE:
                return real(workflow, declared, state, rid)
            return {
                "disposition": FAIL, "stage": STAGE,
                "iteration": _current_packet(state, STAGE)["iteration"],
                "findings": [{
                    "id": finding_id, "severity": "blocking", "check": check,
                    "problem": "command exited 1",
                    "required_result": f"{check} must pass",
                }],
            }

        self.engine._run_gate = run_gate

    def test_the_gate_runs_for_real_and_passes_the_published_leaf(self):
        run_id = self.drive_to_preflight()
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "content-evaluation")
        state = self.engine.load_state(run_id)
        self.assertEqual(state["transitions"][-1],
                         {"from": STAGE, "to": "content-evaluation",
                          "disposition": PASS})
        logs = sorted(
            path.name for path in
            (self.engine.run_dir(run_id) / "gate-logs").glob(f"{STAGE}-*"))
        self.assertEqual(
            [name.split("-", 3)[-1] for name in logs],
            sorted(f"{check}.log" for check in CHECKS),
            "every declared check ran and left its untouched log")
        for name in logs:
            text = (self.engine.run_dir(run_id) / "gate-logs" / name
                    ).read_text(encoding="utf-8")
            self.assertIn("exit 0", text)
            self.assertIn(f"tools/tpt {TOOL}", text)

    def test_a_failing_gate_sends_the_run_to_content_revision(self):
        """The wiring, with the checks themselves stubbed out.

        What the checks decide is held above, against real leaves. What is
        held here is where a decision of FAIL takes the run, which no leaf in
        the tree currently produces.
        """
        run_id = self.drive_to_preflight()
        self.stub_failure("references-used", "GATE-REFERENCES-USED")
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["stage"], "content-revision")
        self.assertNotEqual(out["stage"], RESEARCH)
        state = self.engine.load_state(run_id)
        self.assertEqual(state["transitions"][-1],
                         {"from": STAGE, "to": "content-revision",
                          "disposition": FAIL})
        packet = Path(out["packet_abs_path"]).read_text(encoding="utf-8")
        forwarded = json.loads(next(
            line for line in packet.splitlines()
            if line.startswith("PRIOR_FINDINGS: "))[len("PRIOR_FINDINGS: "):])
        self.assertEqual([f["id"] for f in forwarded],
                         ["GATE-REFERENCES-USED"],
                         "the reviser is handed the check's own output")

    def test_three_consecutive_refusals_block_the_run(self):
        """The cheap loop is cheap, and bounded like every other.

        The reviser returns to the gate directly, so a refusal costs one
        worker and one gate run. Nothing upstream is disturbed: no evaluation
        lane, no research lane, no synthesis. Three consecutive refusals end
        the run.
        """
        run_id = self.drive_to_preflight()
        self.stub_failure("relation-coverage", "GATE-RELATION-COVERAGE")
        for _ in range(2):
            out = self.engine.advance(run_id, run_gate=True)
            self.assertEqual(out["stage"], "content-revision")
            out = self.engine.advance(
                run_id,
                result_path=self.worker_pass(run_id, "content-revision"))
            self.assertEqual(
                out["stage"], STAGE,
                "the reviser goes back to the gate that refused it")
        out = self.engine.advance(run_id, run_gate=True)
        self.assertEqual(out["disposition"], BLOCKED)
        self.assertIn("iteration limit exceeded", out["message"])
        self.assertIn(STAGE, out["message"])


if __name__ == "__main__":
    unittest.main()
