#!/usr/bin/env python3
"""A source the library has not registered is not evidence the research lacks.

Run `5f2d2447ee8d4445` reached `author-proper` with a brief that carried
everything the profile asks of a gallery entry — both texts, exact loci,
wording checks, rights status, payoff and limit, for five afterlives — and
blocked, correctly under the instructions it had. The brief's coverage table
had turned the `source-citation-coverage` lane's provenance notes into
conditions of publishing: register these witnesses, bind them, omit any
unbound claim. No stage of this workflow may register a source. `src/sources/`
is written outside a run, the research lanes are read-only, and the author may
not retrieve, so the demand could be met by nobody and another pass through
the lanes could not have met it either.

Two rules hold that here, in the bytes the workers are handed:

1. The lane, the brief and the author each distinguish a witness no lane
   reached — missing evidence, which the lanes can be sent back for — from a
   witness a lane checked that the library has no record of, which is a note
   in the audit and a claim the guide may print on its own citation.
2. `research/source-bindings.toml` has exactly one writer. The source system
   requires the file and `content-preflight` reads it for rights, while no
   stage was told to produce it: a leaf built from scratch would have failed
   that gate with no repair target able to fix it.

Every rule is also run against the text it replaced, so a matcher cannot pass
by matching nothing.
"""
import re
import subprocess
import sys
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_workflow_research_fanout import (  # noqa: E402
    FRAGMENTS,
    PropersCase,
    workflow_json,
)

AUTHOR = "author-proper"
SYNTHESIS = "research-synthesis"
REVISER = "content-revision"
COVERAGE_LANE = "source-citation-coverage"
BINDINGS = "research/source-bindings.toml"

# ---------------------------------------------------------------------------
# The text each rule replaced, quoted rather than fetched from history so the
# rules can be held to it in any checkout.
# ---------------------------------------------------------------------------

# The coverage lane's whole survey list before this change. It named the risk
# and never said who could answer it, so "weak, second-hand, or still only a
# lead" and "an unregistered source" arrived in the brief as one kind of thing.
PRE_CHANGE_COVERAGE_SURVEY = """
Survey the appointed texts against `guidance/sources.md` and the
repository's own source library, and collate:

- important claims this proper will rest on that still lack a source
- gaps in the source families — a tradition, corpus, language, or genre
  left unswept
- support that is weak, second-hand, or still only a lead
- primary sources the repository already holds that would replace a
  second-hand or derivative citation
- citation, rights, edition-identity, and provenance risks likely to matter
  during authoring
"""

# research-synthesis.md's step 6 before this change: the whole instruction
# for turning the coverage lane's findings into what constrains authoring.
PRE_CHANGE_SYNTHESIS_STEP = """
6. Name the missing evidence that should block or constrain authoring,
   drawing on the `source-citation-coverage` lane's findings.
"""

# The author's BLOCKED contract before this change. It said needing evidence
# the brief does not carry is an insufficient brief, which is true, and left
# an unregistered source looking exactly like it.
PRE_CHANGE_BLOCKED_CONTRACT = """
Needing evidence the brief does not carry is that insufficiency, and it is
the case most easily misread as something else. It is not a gap for this
stage to fill. Retrieving evidence is out of scope for authoring, whatever
the source and however easy the retrieval looks: no fetch, no download, no
reaching past the brief into a catalog, a library, or an edition the brief
did not put in your hands, and nothing recalled from model memory to stand
in for a date, a place, a genre, a locus, or an attribution. Ease is not
permission. A source one command away is as far out of scope as one nobody
holds, because evidence gathered here is evidence no research lane swept, no
coverage audit saw, and no rights check cleared.
"""

# The author's owned-file list before this change: seven files, and the
# binding record the rights gate reads was not among them.
PRE_CHANGE_OWNED_FILES = """
6. Create or update `web-edition.toml` with web edition eligibility.
7. Create or update `propers/verified.md` and `propers/retrieved.txt`.
8. Leave `research/scope.md` exactly as you found it.
"""


def sentences(text: str) -> list[str]:
    """Reconstruct hard-wrapped Markdown into sentences.

    The fragments wrap at 78 columns, so a rule routinely spans three lines
    and a line-based check would see half of it.
    """
    flat = " ".join(text.split())
    return [part for part in re.split(r"(?<=[.:;?])\s+", flat) if part]


def _hits(text: str, *patterns: re.Pattern) -> list[str]:
    """Sentences in which every pattern fires at once."""
    return [s for s in sentences(text)
            if all(pattern.search(s) for pattern in patterns)]


def _re(pattern: str) -> re.Pattern:
    return re.compile(pattern, re.IGNORECASE)


# Rule 1: an unregistered source is not a claim the guide must withhold.
UNREGISTERED = _re(r"(has |have )?not registered|unregistered"
                   r"|library does not hold|library has yet to hold"
                   r"|no record for it|does not yet carry")
PUBLISHABLE = _re(r"publishable|may print|guide prints|is not that"
                  r"|not that insufficiency|never a (control|condition|bar)"
                  r"|rather than a (defect|bar|condition)|note in the audit"
                  r"|provenance note")

# Rule 2: registering a source is work no stage of the run may do.
REGISTERING = _re(r"regist\w*|`src/sources/`|source library|the library")
NO_OWNER_HERE = _re(r"no stage|nothing (here|in this workflow)"
                    r"|outside (a|the) run|forbidden|may not|never register")

# Rule 3: the binding record has a writer. A prohibition names the file and
# a mutation verb too — "never write it, another stage owns it" — so a
# negation in the same sentence disqualifies the hit, or this rule would
# count the fragment that forbids the write as the fragment that owns it.
BINDING_FILE = _re(r"source-bindings\.toml")
OWNS_IT = _re(r"create or update|\bowns\b|produce\w*|writ\w*")
FORBIDS = _re(r"\bdo(es)? not\b|\bmust not\b|\bmay not\b|\bcannot\b"
              r"|\bnever\b|\bno\b|\bnor\b|\bforbidden\b|\bread-only\b"
              r"|\bimmutable\b|another stage")

# Rule 4: it binds only what the library already registers, and the
# fingerprint comes from the tool. No bare "from it": that fires on almost
# any sentence about a command.
FINGERPRINT_TOOL = _re(r"source-library fingerprint")
NOT_BY_HAND = _re(r"never type|by hand|refuses an id|take the fingerprint")

# Rule 5: and it claims no verification that was not performed.
STATE_FIELDS = _re(r"`states`|verified_on")
NO_FURTHER = _re(r"no further than|no more than|not a verified one"
                 r"|may go no further")

# Control: nothing tells a worker to write the shared library. The library is
# named several ways and a rule that knew one of them would be walked past by
# writing another, which `test_workflow_brief_ownership.py` learned first.
LIBRARY = _re(r"src/sources|source library")
# Whole words, not prefixes: `edit\w*` matches "edition" and `add\w*` matches
# "address", and this lane's own survey line carries both.
# No `registered`: "any further registered source this leaf uses" is an
# adjective about the library's contents, not a direction to write it.
LIBRARY_MUTATION = _re(r"\b(writ\w+|creat\w+|updat\w+|amend\w+|register"
                       r"|registers|registering|adds?|adding|added|edits?"
                       r"|editing|edited)\b")
# No bare `no`: "add the record when no entry exists" carries one and forbids
# nothing. Only forms that actually forbid, and the one scoping phrase that
# does the forbidding here.
LIBRARY_NEGATION = _re(r"\bdo(es)? not\b|\bmust not\b|\bmay not\b"
                       r"|\bcannot\b|\bnever\b|\bnor\b|\bforbidden\b"
                       r"|\bread-only\b|\bnothing\b|\bno stage\b"
                       r"|\bnot yours\b|outside (a|the) run")


def unregistered_is_still_publishable(text: str) -> list[str]:
    return _hits(text, UNREGISTERED, PUBLISHABLE)


def registration_has_no_owner_here(text: str) -> list[str]:
    return _hits(text, REGISTERING, NO_OWNER_HERE)


def owns_the_binding_record(text: str) -> list[str]:
    return [s for s in _hits(text, BINDING_FILE, OWNS_IT)
            if not FORBIDS.search(s)]


def binds_only_what_the_library_registers(text: str) -> list[str]:
    return _hits(text, FINGERPRINT_TOOL, NOT_BY_HAND)


def claims_no_unperformed_verification(text: str) -> list[str]:
    return _hits(text, STATE_FIELDS, NO_FURTHER)


def tells_a_worker_to_write_the_library(text: str) -> list[str]:
    """Sentences directing a worker at the shared library.

    Pairs are checked as well as single sentences: naming the library in one
    sentence and the write in the next is the natural way to write the
    directive this rule exists to catch, and a negation two sentences away
    does not qualify a directive.
    """
    parts = sentences(text)
    found = []
    for index, sentence in enumerate(parts):
        windows = [sentence]
        if index + 1 < len(parts):
            windows.append(sentence + " " + parts[index + 1])
        for window in windows:
            if (LIBRARY.search(window) and LIBRARY_MUTATION.search(window)
                    and not LIBRARY_NEGATION.search(window)):
                found.append(sentence)
                break
    return found


def fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / f"{name}.md").read_text(encoding="utf-8")


def lane_fragment(name: str) -> str:
    return (FRAGMENTS / "propers" / "lanes" / f"research-{name}.md").read_text(
        encoding="utf-8")


def propers_fragments() -> dict[str, str]:
    """Every fragment the propers workflow can put in front of a worker."""
    names: list[str] = []
    for stage in workflow_json()["stages"]:
        names.extend(stage.get("fragments", []))
        for lane in stage.get("execution", {}).get("lanes", []):
            names.extend(lane.get("fragments", []))
    return {name: (FRAGMENTS / name).read_text(encoding="utf-8")
            for name in dict.fromkeys(names)
            if name.startswith("propers/")}


class MatcherTests(unittest.TestCase):
    """Each rule is proved to discriminate before it is used to assert."""

    def test_no_rule_fires_on_nothing(self):
        for label, rule in (
                ("unregistered-still-publishable",
                 unregistered_is_still_publishable),
                ("registration-has-no-owner", registration_has_no_owner_here),
                ("owns-the-binding-record", owns_the_binding_record),
                ("binds-what-is-registered",
                 binds_only_what_the_library_registers),
                ("no-unperformed-verification",
                 claims_no_unperformed_verification),
                ("writes-the-library", tells_a_worker_to_write_the_library)):
            with self.subTest(rule=label):
                self.assertEqual(rule(""), [])
                self.assertEqual(rule("The propers are appointed texts."), [])

    def test_the_rules_reject_the_text_they_replaced(self):
        for label, rule, samples in (
                ("unregistered-still-publishable",
                 unregistered_is_still_publishable,
                 [PRE_CHANGE_COVERAGE_SURVEY, PRE_CHANGE_SYNTHESIS_STEP,
                  PRE_CHANGE_BLOCKED_CONTRACT,
                  # The reading that ended the run.
                  "Register and bind exact witnesses before publishing any "
                  "claim that rests on them."]),
                ("registration-has-no-owner", registration_has_no_owner_here,
                 [PRE_CHANGE_COVERAGE_SURVEY, PRE_CHANGE_SYNTHESIS_STEP]),
                ("owns-the-binding-record", owns_the_binding_record,
                 [PRE_CHANGE_OWNED_FILES])):
            for text in samples:
                with self.subTest(rule=label, text=" ".join(text.split())[:60]):
                    self.assertEqual(
                        rule(text), [],
                        f"{label} fires on text that does not state it")

    def test_the_rules_accept_the_rules_reworded(self):
        for label, rule, samples in (
                ("unregistered-still-publishable",
                 unregistered_is_still_publishable,
                 ["A source the library has not registered is publishable on "
                  "the work, edition and locus a lane checked.",
                  "That the library holds no record for it is a provenance "
                  "note, not a claim the guide must withhold."]),
                ("registration-has-no-owner", registration_has_no_owner_here,
                 ["Registering a source is work no stage of this workflow may "
                  "perform.",
                  "Nothing in this workflow writes `src/sources/`."]),
                ("owns-the-binding-record", owns_the_binding_record,
                 ["Create or update `research/source-bindings.toml`, this "
                  "publication's binding record."]),
                ("binds-what-is-registered",
                 binds_only_what_the_library_registers,
                 ["`tools/source-library fingerprint <source_id>` refuses an "
                  "id no record backs."]),
                ("no-unperformed-verification",
                 claims_no_unperformed_verification,
                 ["Its `states` and verified_on may go no further than the "
                  "audit records support."])):
            for text in samples:
                with self.subTest(rule=label, text=" ".join(text.split())[:60]):
                    self.assertTrue(
                        rule(text), f"{label} misses a real statement of it")

    def test_the_ownership_rule_does_not_count_a_prohibition(self):
        """Naming the file and a write verb is what a prohibition does too."""
        for text in (
                "Never write `research/source-bindings.toml`; another stage "
                "owns it.",
                "This lane does not write `research/source-bindings.toml`.",
                "`research/source-bindings.toml` is read-only input here."):
            with self.subTest(text=text[:50]):
                self.assertEqual(owns_the_binding_record(text), [])

    def test_the_library_control_fires_on_the_thing_it_forbids(self):
        for text in (
                "Add the missing witness to `src/sources/` and bind it.",
                # Unbackticked, and split across two sentences: both are ways
                # of writing the directive that a narrower rule walks past.
                "Create the artifact record under src/sources yourself.",
                "The source library is where a witness becomes citable. "
                "Register the edition there before you bind it."):
            with self.subTest(text=text[:50]):
                self.assertTrue(tells_a_worker_to_write_the_library(text))
        for text in (
                "Never register a source yourself: no stage of this workflow "
                "writes `src/sources/`.",
                "Nothing here writes `src/sources/`.",
                "Survey the appointed texts against the repository's own "
                "source library, and collate every edition-identity risk."):
            with self.subTest(allowed=text[:50]):
                self.assertEqual(tells_a_worker_to_write_the_library(text), [])


class FragmentTests(unittest.TestCase):
    """The rules, in the fragment sources that carry them."""

    def test_the_coverage_lane_separates_the_two_defects(self):
        text = lane_fragment(COVERAGE_LANE)
        self.assertTrue(
            unregistered_is_still_publishable(text),
            "the lane that raises the risk must say that an unregistered "
            "source is still a publishable claim")
        self.assertTrue(
            registration_has_no_owner_here(text),
            "and that registering one is work no stage of this run may do")

    def test_the_brief_carries_the_distinction_to_the_author(self):
        text = fragment(SYNTHESIS)
        self.assertTrue(unregistered_is_still_publishable(text))
        self.assertTrue(registration_has_no_owner_here(text))

    def test_the_author_is_told_an_absent_record_is_not_insufficiency(self):
        text = fragment(AUTHOR)
        self.assertIn("BLOCKED", text)
        self.assertTrue(
            unregistered_is_still_publishable(text),
            "the author must be told that an unregistered source is not the "
            "brief insufficiency it blocks on")

    def test_the_author_owns_the_binding_record(self):
        text = fragment(AUTHOR)
        self.assertIn(BINDINGS, text)
        self.assertTrue(owns_the_binding_record(text))
        self.assertTrue(
            binds_only_what_the_library_registers(text),
            "the binder must take ids and fingerprints from the tool that "
            "resolves them, not from its own memory")
        self.assertTrue(
            claims_no_unperformed_verification(text),
            "a binding states what this publication did with a source; a "
            "verification nobody performed makes every consumer of it wrong")

    def test_exactly_one_fragment_writes_the_binding_record(self):
        owners = [name for name, text in propers_fragments().items()
                  if owns_the_binding_record(text)]
        self.assertEqual(
            owners, [f"propers/{AUTHOR}.md"],
            f"exactly one fragment may write {BINDINGS}")

    def test_no_fragment_tells_a_worker_to_write_the_library(self):
        for name, text in propers_fragments().items():
            with self.subTest(fragment=name):
                self.assertEqual(
                    tells_a_worker_to_write_the_library(text), [],
                    f"{name} directs a worker at `src/sources/`, which no "
                    f"stage of a run may write")

    def test_the_phrasings_that_ended_the_run_are_not_instructions(self):
        """The wording that turned a provenance note into a bar.

        The coverage lane names these to forbid them, so a fragment may
        carry one only in a sentence that forbids it. A future edit that
        reintroduces the instruction reintroduces the block, and every other
        test here would still pass.
        """
        phrasings = ("register and bind before publishing",
                     "publication waits on",
                     "omit any unbound claim",
                     "before the claims resting on them can be published")
        for name, text in propers_fragments().items():
            for sentence in sentences(text):
                for phrasing in phrasings:
                    if phrasing not in sentence.lower():
                        continue
                    with self.subTest(fragment=name, phrasing=phrasing):
                        self.assertTrue(
                            FORBIDS.search(sentence),
                            f"{name} carries {phrasing!r} as an instruction: "
                            f"{sentence}")

    def test_the_gate_that_reads_the_record_still_exists(self):
        """The reason the file needs a writer at all."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        checks = {c["id"] for c in stages["content-preflight"]["checks"]}
        self.assertIn("restricted-not-reproduced", checks)

    def test_the_gate_holds_the_record_the_author_now_writes(self):
        """The file has a writer inside the run, so it has a check there."""
        stages = {s["id"]: s for s in workflow_json()["stages"]}
        checks = {c["id"] for c in stages["content-preflight"]["checks"]}
        self.assertIn("bindings-valid", checks)

    def test_the_verbs_the_author_is_sent_to_exist(self):
        """Exact invocations, checked rather than assumed."""
        for argv, expected in (
                (["fingerprint", "--help"], "source_id"),
                (["validate", "--help"], "validate")):
            with self.subTest(argv=argv):
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "tools" / "source-library"),
                     *argv],
                    capture_output=True, text=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertIn(expected, proc.stdout)

    def test_the_fingerprint_is_the_value_a_binding_must_carry(self):
        """The instruction's whole point, held against a published leaf.

        The author is told to take a binding's fingerprint from the tool. If
        the tool printed anything else the instruction would produce a file
        the validator refuses, and the only place that shows is here.
        """
        leaf = (ROOT / "src/gpt/liturgy/roman-rite/1962/propers/temporal"
                / "53-thirteenth-after-pentecost")
        bindings = tomllib.loads(
            (leaf / "research/source-bindings.toml").read_text(
                encoding="utf-8"))
        bound = next(b for b in bindings["bindings"]
                     if b.get("source_fingerprint"))
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "source-library"),
             "fingerprint", bound["source_id"]],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), bound["source_fingerprint"])


class EmittedPacketTests(PropersCase):
    """The same rules, in the bytes the workers are actually handed."""

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

    def setUp(self):
        super().setUp()
        self.packets = self.compiled_packets()

    def test_the_coverage_lane_packet_carries_the_distinction(self):
        text = self.packets[f"research/{COVERAGE_LANE}"]
        self.assertTrue(unregistered_is_still_publishable(text))
        self.assertTrue(registration_has_no_owner_here(text))

    def test_the_author_packet_carries_both_rules(self):
        text = self.packets[AUTHOR]
        self.assertTrue(unregistered_is_still_publishable(text))
        self.assertTrue(owns_the_binding_record(text))
        self.assertTrue(binds_only_what_the_library_registers(text))

    def test_the_reviser_packet_inherits_them(self):
        """`content-revision` re-authors, so it must bind by the same rules."""
        text = self.packets[REVISER]
        self.assertTrue(unregistered_is_still_publishable(text))
        self.assertTrue(owns_the_binding_record(text))

    def test_the_rules_are_not_in_every_packet(self):
        """A matcher that fires everywhere proves nothing where it matters."""
        for stage in ("build-artifacts", "generate-web", "publish-artifacts"):
            with self.subTest(stage=stage):
                text = self.packets[stage]
                self.assertEqual(owns_the_binding_record(text), [])
                self.assertEqual(unregistered_is_still_publishable(text), [])


if __name__ == "__main__":
    unittest.main()
