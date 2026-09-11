#!/usr/bin/env python3
"""A program reads the companion before two AI lanes are spent on it.

`content-preflight` is reachable from `author-proper` and `content-revision`,
and both are forbidden to write the synthesis companion. The stages that do
write it -- `derive-synthesis` and `synthesis-revision` -- run after
`content-evaluation` has passed, and the only gate between them and
publication was `mechanical-gates`, whose three checks are the component
manifest and two `make doc` builds. So every companion-owned byte a run wrote
reached `synthesis-evaluation`'s two lanes with no program having read it.

One production paid for that in the shape the house-voice class is recorded in:
a References entry describing what a cited edition supplied in terms of
apparatus the companion does not print took three consecutive evaluation
rounds, one site at a time, all in one file -- two sites, then three, then one.
`synthesis-preflight` is the answer `OPERATOR.md` records for `house-voice`,
applied where the companion is written: a gate loop drains a mechanical class
at no evaluator cost.

The gate cannot simply re-run the thirteen. Its failures go to
`synthesis-revision`, which may write the companion and the seam and nothing
else, so a check that named a canonical-only file would name a file its
reviser is forbidden to touch -- and a gate keeps the finding-id comparison
whatever a reviser reports, so three such refusals would block the run
outright. What makes the seven it does run safe is the edition scope: under
`--edition synthesis` every file read is a file the companion typesets, and
every guard is resolved to the branch the companion prints.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import shlex
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPELINES = ROOT / "workflows" / "pipelines"
TOOL = "check-content-preflight"
PREFLIGHT = ROOT / "tools" / TOOL
ERROR = f"{TOOL} error: "
STAGE = "synthesis-preflight"
PIPELINE_NAMES = ("proper.json", "proper-finish.json")

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _parallel import gather  # noqa: E402
from _workflow import PROGRAM, _substitute_args  # noqa: E402

# The seven the gate runs, in the order it declares them, and the six it does
# not. The reason is one rule applied thirteen times: a check belongs here if
# `--edition synthesis` narrows it to bytes the companion prints, because that
# is what makes its refusal repairable by the companion's own reviser.
#
#   references-used             the companion prints its own References
#                               apparatus and drops the sweep that used some
#                               of it; an entry used only there is unused here
#   identifiers-resolve         an identifier the companion's own prose prints
#   restricted-not-reproduced   what the companion prints, against the rights
#                               in src/sources; the companion is published as
#                               its own artifact under its own release record
#   unquoted-not-quoted         the companion's own References against the
#                               companion's own printed passages
#   structural-meta-labels      a structural surface of a section written for
#                               this edition alone
#   house-voice                 the class that names the gate
#   proposal-fields             the exploratory synthesis the companion keeps,
#                               shortened by the derivation
#
# And the six left out, each for the same rule read the other way:
#
#   bindings-valid              research/source-bindings.toml is one record for
#                               the leaf, written by author-proper; the edition
#                               flag is inert and synthesis-revision may not
#                               write research/
#   relation-coverage           two tables of one proper-components.toml; the
#                               flag is inert, and a manifest defect is neither
#                               a derivation nor a seam repair
#   provenance-matches-run      one \AIGenerationProvenance record for the
#                               leaf, in a file every prose list excludes; it
#                               would hold the companion's reviser to a fact
#                               about the canonical edition
#   chronology-record-current   a generated record under research/, rewritten
#   chronology-annotations-     from the corpus by a stage that ran long before
#     current                   the companion existed
#   chronology-claims-supported the flag does narrow it, but it is one of three
#                               that form one contract and the other two are
#                               edition-blind; half a contract in a gate is
#                               worse than none, and its remedy is a generated
#                               file no companion reviser owns
GATE_CHECKS = (
    "references-used",
    "identifiers-resolve",
    "restricted-not-reproduced",
    "unquoted-not-quoted",
    "structural-meta-labels",
    "house-voice",
    "proposal-fields",
)
NOT_IN_THE_GATE = (
    "bindings-valid",
    "relation-coverage",
    "provenance-matches-run",
    "chronology-record-current",
    "chronology-annotations-current",
    "chronology-claims-supported",
)

LOADER = importlib.machinery.SourceFileLoader(
    "triptych_synthesis_preflight_tool", str(PREFLIGHT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {PREFLIGHT}")
TOOL_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = TOOL_MODULE
SPEC.loader.exec_module(TOOL_MODULE)


def pipeline(name: str) -> dict:
    return json.loads((PIPELINES / name).read_text(encoding="utf-8"))


def stages(name: str) -> dict:
    return {stage["id"]: stage for stage in pipeline(name)["stages"]}


def order(name: str) -> list[str]:
    return [stage["id"] for stage in pipeline(name)["stages"]]


def manifest_leaves() -> list[tuple[str, str]]:
    """Every 1962 propers leaf the manifest era produced, both providers."""
    return [
        (provider, found.parent.relative_to(ROOT / "src" / provider).as_posix())
        for provider in ("claude", "gpt")
        for found in sorted(
            (ROOT / "src" / provider / "liturgy/roman-rite/1962/propers")
            .glob("*/*/proper-components.toml"))
    ]


def run_check(provider: str, document: str, check: str,
              edition: str | None = None) -> subprocess.CompletedProcess:
    command = [str(PREFLIGHT), "--provider", provider,
               "--document", document, "--check", check]
    if edition is not None:
        command += ["--edition", edition]
    return subprocess.run(command, capture_output=True, text=True, cwd=ROOT)


def short(provider: str, document: str) -> str:
    return f"{provider}/{document.rsplit('/', 1)[-1]}"


class TopologyTests(unittest.TestCase):
    """Where the gate stands, in both pipelines, and where a failure may go."""

    def test_it_sits_between_the_companion_s_writer_and_its_evaluation(self):
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                listed = order(name)
                self.assertIn(STAGE, listed)
                self.assertEqual(
                    listed[listed.index("derive-synthesis") + 1], STAGE,
                    "the gate reads what derive-synthesis has just written")
                self.assertEqual(
                    listed[listed.index(STAGE) + 1], "synthesis-evaluation")

    def test_both_of_the_companion_s_writers_re_enter_the_gate(self):
        """The reviser goes back to the program, not to the two lanes.

        `synthesis-revision` re-entering `synthesis-evaluation` would spend
        two max-effort lanes on a companion whose mechanical defect may still
        stand, which is exactly what `content-revision` does not do.
        """
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                declared = stages(name)
                self.assertEqual(declared["derive-synthesis"]["next"], STAGE)
                self.assertEqual(declared["synthesis-revision"]["next"], STAGE)

    def test_it_is_a_program_gate_with_a_bounded_loop(self):
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                declared = stages(name)[STAGE]
                self.assertEqual(declared["type"], "gate")
                self.assertEqual(declared["execution"], {"mode": PROGRAM})
                self.assertEqual(declared["pass_transition"],
                                 "synthesis-evaluation")
                self.assertEqual(declared["fail_transition"],
                                 "synthesis-revision")
                self.assertEqual(declared["max_iterations"], 3)
                self.assertNotIn("effort", declared,
                                 "tpt runs a gate and no agent does, so a "
                                 "gate that declared a reasoning effort would "
                                 "be refused at load")
                self.assertNotIn("fragments", declared,
                                 "a program gate asks no agent anything")
                self.assertNotIn("repair_routes", declared,
                                 "a mechanical defect in the companion has "
                                 "one owner, so it needs no classification")

    def test_a_failure_reaches_a_reviser_that_may_repair_it(self):
        """The whole reason the checks are edition-scoped.

        `synthesis-revision` owns `derivation` and `seam` and nothing else.
        Every file the gate can name is one the companion typesets, so what it
        refuses is either the companion's own bytes or shared prose whose form
        the companion makes visible -- and both of those are on that list.
        """
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                declared = stages(name)
                reviser = declared[declared[STAGE]["fail_transition"]]
                self.assertEqual(reviser["type"], "bounded-revision")
                self.assertEqual(reviser["revision_target"],
                                 "derive-synthesis")
                self.assertEqual(sorted(reviser["repairs"]),
                                 ["derivation", "seam"])
                for key in ("next", "pass_transition", "fail_transition"):
                    self.assertNotEqual(reviser.get(key), "content-revision")
                    self.assertNotEqual(reviser.get(key), "research")

    def test_the_canonical_gate_is_left_where_it_was(self):
        """This change adds a gate; it moves none.

        `content-preflight` still runs the whole thirteen at leaf scope
        between the author and the evaluation, and a run that reaches the new
        gate has already passed it.
        """
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                listed = order(name)
                declared = stages(name)
                self.assertEqual(
                    listed[listed.index("author-proper") + 1],
                    "content-preflight")
                self.assertEqual(
                    declared["content-preflight"]["pass_transition"],
                    "content-evaluation")
                self.assertEqual(
                    declared["content-preflight"]["fail_transition"],
                    "content-revision")
                for check in declared["content-preflight"]["checks"]:
                    self.assertNotIn(
                        "--edition", check["command"],
                        "the canonical gate reads the leaf, which is the "
                        "default and every hand invocation's scope too")


class CheckListTests(unittest.TestCase):
    """Which of the thirteen the gate runs, and how each is written."""

    def commands(self, name: str) -> dict[str, str]:
        return {check["id"]: check["command"]
                for check in stages(name)[STAGE]["checks"]}

    def test_the_gate_runs_exactly_the_seven_that_are_true_of_a_companion(self):
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                self.assertEqual(list(self.commands(name)), list(GATE_CHECKS))

    def test_the_two_pipelines_declare_the_same_gate(self):
        """One contract, so a run cannot pass it in one pipeline and not the
        other for a reason nobody chose."""
        first, second = (stages(name)[STAGE] for name in PIPELINE_NAMES)
        self.assertEqual(first, second)

    def test_every_check_the_gate_runs_is_one_the_tool_implements(self):
        """The tool is the authority on what checks there are.

        Read from `--list` rather than from the tuple above, because a gate
        naming a check the tool does not implement fails at the shell with a
        message about an argument, which reads nothing like the defect it is.
        """
        listed = subprocess.run(
            [str(PREFLIGHT), "--list"],
            capture_output=True, text=True, cwd=ROOT).stdout.split()
        self.assertEqual(sorted(listed),
                         sorted(GATE_CHECKS + NOT_IN_THE_GATE),
                         "the tool's own listing and this file disagree "
                         "about which checks exist")
        for name in PIPELINE_NAMES:
            with self.subTest(pipeline=name):
                for check_id in self.commands(name):
                    self.assertIn(check_id, listed)

    def test_the_gate_names_no_check_the_edition_flag_cannot_narrow(self):
        """The six left out, named so that leaving one out is a decision.

        Each was excluded for a reason written beside `NOT_IN_THE_GATE`
        above. What is asserted here is only that none of them is in the gate:
        a check whose subject is one record for the whole leaf cannot be
        narrowed to the companion, so its refusal would reach a reviser who
        may not repair it, and three refusals block the run.
        """
        for name in PIPELINE_NAMES:
            for check_id in NOT_IN_THE_GATE:
                with self.subTest(pipeline=name, check=check_id):
                    self.assertNotIn(check_id, self.commands(name))

    def test_every_check_reads_the_synthesis_edition(self):
        for name in PIPELINE_NAMES:
            for check_id, command in self.commands(name).items():
                with self.subTest(pipeline=name, check=check_id):
                    self.assertIn("--edition synthesis", command)
                    self.assertNotIn("--edition canonical", command)
                    self.assertNotIn("--edition leaf", command)

    def test_every_check_is_one_command_over_the_run_s_own_arguments(self):
        registry = json.loads(
            (ROOT / "tmt.json").read_text(encoding="utf-8"))["tools"]
        for name in PIPELINE_NAMES:
            for check_id, command in self.commands(name).items():
                with self.subTest(pipeline=name, check=check_id):
                    self.assertIn(f"tools/tpt {TOOL} ", command)
                    self.assertIn(TOOL, registry,
                                  "a gate may only run a registered tool")
                    self.assertIn(f"--check {check_id}", command)
                    residue = command.replace("{proper}", "").replace(
                        "{provider}", "")
                    self.assertNotRegex(
                        residue, r"\{[A-Za-z_][A-Za-z0-9_.]*\}",
                        "the gate takes a name the run supplies nothing for")
                    for shell in ("&&", "||", ";", "|"):
                        self.assertNotIn(
                            shell, command,
                            "each check is one command, judged by its own "
                            "exit code")

    def test_every_check_states_what_it_requires(self):
        for name in PIPELINE_NAMES:
            for check in stages(name)[STAGE]["checks"]:
                with self.subTest(pipeline=name, check=check["id"]):
                    self.assertGreater(
                        len(check.get("required_result", "")), 80,
                        "a refusal is read by a reviser, and a check that "
                        "says only its own name says nothing about what to "
                        "produce")

    PAYLOADS = (
        "x`touch /tmp/triptych-synthesis-preflight-escape`",
        "x$(touch /tmp/triptych-synthesis-preflight-escape)",
        "x; touch /tmp/triptych-synthesis-preflight-escape",
        "x' ; touch /tmp/triptych-synthesis-preflight-escape ; '",
    )

    def test_a_hostile_identity_survives_as_data(self):
        """The property fab7db40b established, held for the new gate too."""
        for name in PIPELINE_NAMES:
            for check_id, command in self.commands(name).items():
                for payload in self.PAYLOADS:
                    with self.subTest(pipeline=name, check=check_id,
                                      payload=payload):
                        rendered = _substitute_args(
                            command, {"proper": payload,
                                      "provider": "claude"}, quote=True)
                        tokens = shlex.split(rendered)
                        self.assertTrue(
                            any(payload in token for token in tokens),
                            "the id did not survive substitution as inert "
                            "data")
                        self.assertNotIn("touch", tokens,
                                         "part of the id became a shell word")


class EditionResolverTests(unittest.TestCase):
    """`\\ifdefined\\TriptychSynthesisEdition`, resolved for one edition."""

    maxDiff = None

    BLOCK = (
        "Before.\n"
        "\\ifdefined\\TriptychSynthesisEdition\n"
        "Only the companion prints this.\n"
        "\\else\n"
        "Only the canonical edition prints this.\n"
        "\\fi\n"
        "After.\n"
    )
    # The other form in the tree, and the reason the dropped branch is blanked
    # rather than cut: the sentence runs through the guard, so what the reader
    # is given is one sentence and not two fragments.
    INLINE = (
        "and so answers the missal in number alone. "
        "\\ifdefined\\TriptychSynthesisEdition\n"
        "The companion says it shortly,\n"
        "\\else\n"
        "The canonical edition says it at length,\n"
        "\\fi{} and the Communion's two readings follow.\n"
    )

    def resolve(self, text: str, defined: bool) -> str:
        return TOOL_MODULE.resolve_edition(text, defined)

    def words(self, text: str) -> str:
        return " ".join(text.split())

    def test_the_leaf_scope_is_the_bytes_unchanged(self):
        """The default resolves nothing, which is what keeps every hand
        invocation and every content-preflight command what it was."""
        for text in (self.BLOCK, self.INLINE):
            self.assertEqual(self.resolve(text, None), text)

    def test_a_block_guard_resolves_both_ways(self):
        self.assertIn("Only the companion prints this.",
                      self.resolve(self.BLOCK, True))
        self.assertNotIn("Only the canonical edition prints this.",
                         self.resolve(self.BLOCK, True))
        self.assertIn("Only the canonical edition prints this.",
                      self.resolve(self.BLOCK, False))
        self.assertNotIn("Only the companion prints this.",
                         self.resolve(self.BLOCK, False))
        for defined in (True, False):
            with self.subTest(defined=defined):
                resolved = self.resolve(self.BLOCK, defined)
                self.assertNotIn("\\ifdefined", resolved)
                self.assertNotIn("\\else", resolved)
                self.assertNotIn("\\fi", resolved)
                self.assertIn("Before.", resolved)
                self.assertIn("After.", resolved)

    def test_an_inline_guard_leaves_one_sentence(self):
        self.assertEqual(
            self.words(self.resolve(self.INLINE, True)),
            "and so answers the missal in number alone. The companion says "
            "it shortly, {} and the Communion's two readings follow.")
        self.assertEqual(
            self.words(self.resolve(self.INLINE, False)),
            "and so answers the missal in number alone. The canonical "
            "edition says it at length, {} and the Communion's two readings "
            "follow.")

    def test_every_offset_and_line_number_is_still_the_file_s_own(self):
        """A refusal names the line an editor shows, or a worker guesses.

        The dropped branch becomes spaces and keeps its newlines, so the
        resolved text is the same length as the file and breaks in the same
        places.
        """
        for text in (self.BLOCK, self.INLINE):
            for defined in (True, False):
                with self.subTest(defined=defined):
                    resolved = self.resolve(text, defined)
                    self.assertEqual(len(resolved), len(text))
                    self.assertEqual(
                        [index for index, char in enumerate(resolved)
                         if char == "\n"],
                        [index for index, char in enumerate(text)
                         if char == "\n"])
                    for was, now in zip(text, resolved):
                        self.assertIn(now, (was, " "))

    def test_a_commented_guard_token_closes_nothing(self):
        """A `%` makes a line a comment and not TeX.

        A walk that counted a commented `\\fi` would end the branch early and
        publish the other edition's sentence.
        """
        text = ("\\ifdefined\\TriptychSynthesisEdition\n"
                "% \\fi is not a \\fi here\n"
                "The companion sentence.\n"
                "\\else\n"
                "The canonical sentence.\n"
                "\\fi\n")
        self.assertIn("The companion sentence.", self.resolve(text, True))
        self.assertNotIn("The canonical sentence.", self.resolve(text, True))
        self.assertIn("The canonical sentence.", self.resolve(text, False))
        self.assertNotIn("The companion sentence.", self.resolve(text, False))

    def test_another_flag_s_conditional_is_stepped_over_whole(self):
        """`\\ifdefined\\TriptychPrintEdition` is in this corpus too.

        Its `\\fi` is not the guard's, and taking it for one would resolve two
        conditionals into each other.
        """
        text = ("\\ifdefined\\TriptychSynthesisEdition\n"
                "\\ifdefined\\TriptychPrintEdition\n"
                "companion, print\n"
                "\\else\n"
                "companion, screen\n"
                "\\fi\n"
                "\\else\n"
                "canonical only\n"
                "\\fi\n")
        companion = self.resolve(text, True)
        self.assertIn("companion, print", companion)
        self.assertIn("companion, screen", companion)
        self.assertIn("\\ifdefined\\TriptychPrintEdition", companion)
        self.assertNotIn("canonical only", companion)
        canonical = self.resolve(text, False)
        self.assertIn("canonical only", canonical)
        self.assertNotIn("companion, print", canonical)
        self.assertNotIn("\\ifdefined\\TriptychPrintEdition", canonical)

    def test_a_guard_with_no_else_prints_in_one_edition_only(self):
        text = ("\\ifdefined\\TriptychSynthesisEdition\n"
                "Companion only.\n"
                "\\fi\n")
        self.assertIn("Companion only.", self.resolve(text, True))
        self.assertNotIn("Companion only.", self.resolve(text, False))

    def test_an_unclosed_guard_is_an_error_and_not_a_guess(self):
        with self.assertRaises(ValueError) as caught:
            self.resolve("\\ifdefined\\TriptychSynthesisEdition\nnothing\n",
                         True)
        self.assertIn("never closed", str(caught.exception))

    def test_fi_is_not_read_out_of_a_macro_name(self):
        """One leaf's `format.tex` defines `\\finishfulltextelement`."""
        text = ("\\ifdefined\\TriptychSynthesisEdition\n"
                "\\finishfulltextelement\n"
                "companion\n"
                "\\else\n"
                "canonical\n"
                "\\fi\n")
        self.assertIn("companion", self.resolve(text, True))
        self.assertNotIn("canonical", self.resolve(text, True))

    def test_the_flag_is_read_off_the_entry_file_and_never_assumed(self):
        """Two shapes of `synthesis.tex` are current, and both are right.

        Most companions define `\\TriptychSynthesisEdition` and input
        `main.tex`, which branches on it. Three carry a standalone preamble
        that defines nothing and inputs a section list of its own, so a guard
        in a file such a companion shares with `main.tex` takes the canonical
        branch there. Assuming the flag from the edition's name would publish
        the wrong branch in three leaves.
        """
        shapes = {}
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            if not (leaf / "synthesis.tex").is_file():
                continue
            shapes.setdefault(
                TOOL_MODULE.flag_defined(leaf, "synthesis"), []).append(
                short(provider, document))
        self.assertEqual(sorted(shapes), [False, True],
                         f"both shapes are in the corpus: {shapes}")
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            with self.subTest(leaf=short(provider, document)):
                self.assertIs(TOOL_MODULE.flag_defined(leaf, "canonical"),
                              False)
                self.assertIsNone(TOOL_MODULE.flag_defined(leaf, "leaf"))

    def test_every_tex_file_in_the_corpus_resolves(self):
        """No leaf in the tree defeats the walk.

        A guard the walk cannot read is a guard it would resolve wrongly and
        silently, so the whole corpus is parsed here rather than one fixture.
        """
        guarded = 0
        for path in sorted((ROOT / "src").rglob("*.tex")):
            text = path.read_text(encoding="utf-8")
            if TOOL_MODULE.GUARD.search(TOOL_MODULE.uncommented(text)):
                guarded += 1
            for defined in (True, False):
                resolved = self.resolve(text, defined)
                self.assertEqual(len(resolved), len(text), path)
                self.assertFalse(
                    TOOL_MODULE.GUARD.search(
                        TOOL_MODULE.uncommented(resolved)),
                    f"{path}: a guard survived its own resolution")
        self.assertGreater(guarded, 0, "no guard was exercised at all")


class EditionScopeTests(unittest.TestCase):
    """What each edition reads, over the corpus rather than over a fixture."""

    def test_the_leaf_scope_reads_what_both_editions_read(self):
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            with self.subTest(leaf=short(provider, document)):
                whole = set(TOOL_MODULE.leaf_tex(leaf))
                for edition in ("canonical", "synthesis"):
                    self.assertLessEqual(
                        set(TOOL_MODULE.leaf_tex(leaf, edition)), whole,
                        "an edition reads a file the leaf scope does not")

    def test_the_synthesis_scope_drops_the_sections_it_does_not_print(self):
        """The companion omits the appointed texts and the reception sweep.

        Stated as a difference rather than by filename: `sections/synthesis/`
        is not a reliable name for a companion-only file, and one leaf's
        canonical edition inputs a section from that very directory.
        """
        narrowed = 0
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            if not (leaf / "synthesis.tex").is_file():
                continue
            companion = set(TOOL_MODULE.leaf_tex(leaf, "synthesis"))
            canonical = set(TOOL_MODULE.leaf_tex(leaf, "canonical"))
            with self.subTest(leaf=short(provider, document)):
                self.assertTrue(canonical - companion,
                                "the canonical edition prints something the "
                                "companion does not")
                self.assertTrue(companion - canonical,
                                "the companion prints something the "
                                "canonical edition does not")
            narrowed += 1
        self.assertGreater(narrowed, 0)

    def test_a_canonical_only_defect_is_not_the_companion_s_to_repair(self):
        """The thirteenth Sunday, where the difference is seventeen findings.

        At canonical scope `house-voice` refuses that leaf on sentences in
        `sections/05-appointed-text.tex` and `sections/30-commentary.tex` --
        neither of which the companion prints. At synthesis scope it names
        the companion's own integrated commentary and one shared file, which
        are `derivation` and `seam`, the two things its reviser may repair.
        """
        document = ("liturgy/roman-rite/1962/propers/temporal/"
                    "53-thirteenth-after-pentecost")
        leaf = ROOT / "src" / "claude" / document
        if not leaf.is_dir():
            self.skipTest("the specimen leaf is not in the tree")
        canonical = run_check("claude", document, "house-voice", "canonical")
        companion = run_check("claude", document, "house-voice", "synthesis")
        self.assertEqual(canonical.returncode, 1)
        self.assertEqual(companion.returncode, 1)
        self.assertIn("sections/05-appointed-text.tex", canonical.stderr)
        self.assertNotIn("sections/05-appointed-text.tex", companion.stderr)
        self.assertNotIn("sections/30-commentary.tex", companion.stderr)
        self.assertIn("sections/synthesis/20-integrated-commentary.tex",
                      companion.stderr)

    def test_a_refusal_names_only_files_the_companion_prints(self):
        """Held over every leaf the gate refuses, not over one.

        A reviser handed a file its edition does not typeset has been handed
        a repair it may not make, and reporting it unrepaired three times
        blocks the run.
        """
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            printed = {path.relative_to(leaf).as_posix()
                       for path in TOOL_MODULE.leaf_tex(leaf, "synthesis")}
            results = gather(
                lambda check: run_check(provider, document, check,
                                        "synthesis"),
                GATE_CHECKS)
            for check, result in zip(GATE_CHECKS, results):
                for line in result.stderr.splitlines():
                    if not line.startswith(ERROR):
                        continue
                    said = line.split(": ", 2)[-1]
                    for named in printed:
                        if said.startswith(named):
                            break
                    else:
                        continue
                    with self.subTest(leaf=short(provider, document),
                                      check=check):
                        self.assertIn(said.split(":", 1)[0], printed)

    def test_the_edition_is_named_in_what_the_tool_prints(self):
        """A gate log says which document it judged.

        The same check id over the canonical edition and over the companion
        are two different measurements, and a line that read the same for
        both would leave the run's own record ambiguous about which reviser
        owes the repair.
        """
        provider, document = manifest_leaves()[0]
        plain = run_check(provider, document, "references-used")
        scoped = run_check(provider, document, "references-used", "synthesis")
        self.assertIn("references-used: ", plain.stdout + plain.stderr)
        self.assertIn("references-used (synthesis edition): ",
                      scoped.stdout + scoped.stderr)


class CorpusTests(unittest.TestCase):
    """What the gate would do to the corpus today, recorded rather than
    assumed.

    A gate that refused most of the corpus would not be a gate, it would be a
    stop; and a gate that refused a leaf its own canonical preflight accepts
    would be a new bar raised on work already published under the old one.
    Both are measured here, over every leaf the manifest era produced.
    """

    maxDiff = None

    # Every check content-preflight runs at leaf scope except the one that
    # needs a run's identity, which no published leaf can satisfy outside the
    # run that wrote its provenance record.
    CONTENT_PREFLIGHT_CHECKS = tuple(
        check for check in GATE_CHECKS + NOT_IN_THE_GATE
        if check != "provenance-matches-run")

    def refused(self, checks, edition):
        leaves = manifest_leaves()
        jobs = [(provider, document, check)
                for check in checks for provider, document in leaves]
        results = gather(
            lambda job: run_check(job[0], job[1], job[2], edition), jobs)
        return sorted({short(job[0], job[1])
                       for job, result in zip(jobs, results)
                       if result.returncode})

    def test_the_gate_refuses_six_of_the_fifteen_manifest_leaves(self):
        """Which, recorded, so that a change in the number is a decision.

        Every one of the six is a leaf `content-preflight` refuses as well,
        and five of the six are refused for `house-voice` in prose written
        before either screen existed.
        """
        self.assertEqual(len(manifest_leaves()), 15)
        self.assertEqual(
            self.refused(GATE_CHECKS, "synthesis"),
            ["claude/49-ninth-after-pentecost",
             "claude/51-eleventh-after-pentecost",
             "claude/52-twelfth-after-pentecost",
             "claude/53-thirteenth-after-pentecost",
             "gpt/49-ninth-after-pentecost",
             "gpt/52-twelfth-after-pentecost"])

    def test_the_gate_refuses_no_leaf_the_canonical_gate_accepts(self):
        """The bar this adds is not a new bar.

        A leaf that passes `content-preflight` today passes this gate today,
        so nothing in the corpus is refused for the first time by putting a
        program where the companion is written.
        """
        gate = set(self.refused(GATE_CHECKS, "synthesis"))
        canonical_gate = set(
            self.refused(self.CONTENT_PREFLIGHT_CHECKS, None))
        self.assertTrue(
            gate <= canonical_gate,
            f"refused by the new gate alone: {sorted(gate - canonical_gate)}")

    def test_the_companion_only_prose_the_gate_was_built_for(self):
        """The three leaves whose companion-owned files carry the class.

        Measured over the files only the companion prints, and taken from the
        `\\input` graph rather than from a directory name. That is the whole
        difference between nine sites and five: the eleventh Sunday's
        integrated commentary is `sections/32-integrated-commentary.tex`, so
        a sweep of `sections/synthesis/` misses four of these and the leaf
        they are in, while the thirteenth Sunday in the other provider inputs
        a file from `sections/synthesis/` into its *canonical* edition. The
        remaining twelve leaves' companion files carry none of the class,
        which is why it belongs in a gate loop and not in the evaluation
        behind it.
        """
        sites = {}
        for provider, document in manifest_leaves():
            leaf = ROOT / "src" / provider / document
            if not (leaf / "synthesis.tex").is_file():
                continue
            only = {path.relative_to(leaf).as_posix()
                    for path in set(TOOL_MODULE.leaf_tex(leaf, "synthesis"))
                    - set(TOOL_MODULE.leaf_tex(leaf, "canonical"))}
            result = run_check(provider, document, "house-voice", "synthesis")
            found = sum(
                1 for line in result.stderr.splitlines()
                if line.startswith(f"{ERROR}house-voice (synthesis edition): ")
                and "not screened:" not in line
                and line.split(": ", 2)[-1].split(":", 1)[0] in only)
            if found:
                sites[short(provider, document)] = found
        self.assertEqual(sites, {"claude/51-eleventh-after-pentecost": 4,
                                 "claude/52-twelfth-after-pentecost": 3,
                                 "claude/53-thirteenth-after-pentecost": 2})


if __name__ == "__main__":
    unittest.main()
