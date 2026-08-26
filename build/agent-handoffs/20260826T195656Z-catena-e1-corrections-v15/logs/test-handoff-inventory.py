#!/usr/bin/env python3
"""THE HANDOFF INVENTORY, DRIVEN AT EVERY WAY A HANDOFF CAN BE LEXICALLY
PERFECT AND SUBSTANTIVELY FALSE.

The previous version of this checker scored the V12 package `10/10` and
`problems: 0`, and an independent review then refused that package for four
substantive failures. Every one of them was a well-formed English sentence
disagreeing with the bytes beside it, and a checker that reads only
`HANDOFF.md` cannot see any of them. Each test below builds a package that is
wrong in exactly one such way and asserts that the tool names it — and the
first builds the package that is right and asserts the tool is silent, so the
refusals are not simply a tool that always fails.

The last test is the reproduction: the reviewed V12 package, if it is present
on this machine, must be REFUSED, and must be refused for the four findings
the review actually made, without being told what they were.
"""

from __future__ import annotations

import json
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "handoff-inventory.py"

NAME = "20260101T000000Z-handoff-inventory-selftest"
HEAD = "d312786dd2b23926aa88e29ea15647dfcc7e7e6e"
PARENT = "b0255b84996e1dc24da3ce75ac318c4f774b7957"
BRANCH = "impl/handoff-inventory-selftest"

SIBLING_SUFFIXES = (".zip", ".zip.sha256", ".assemble.log",
                    ".verify-final.log", ".authority-coherence.log",
                    ".handoff-inventory.log")

ROOT_FILES = ("HANDOFF.md", "REVIEW_REQUEST.md", "CLAIM-CLOSURE.md",
              "PROVENANCE.md", "EVIDENCE-INDEX.md", "DERIVED-CLAIMS.md",
              "PRIVACY-AUDIT.md", "LIMITATIONS.md", "UNRESOLVED-BLOCKERS.md",
              "claims.json", "checks.txt", "commits.txt", "changed-files.txt",
              "changes.patch", "MANIFEST.sha256")


# The spelled numeral the inventory's count claims are written with. The
# fixtures below change how many logs and siblings a package really has, and
# HANDOFF.md has to say the new number in words or the count check -- which is
# doing its job -- refuses the fixture before the check under test is reached.
COUNT_WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
              6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}

# THE HONEST PROSE THE 9f PATTERNS MUST NOT READ AS A ROW REMOVAL. Both
# sentences are shaped like the ones that forced the patterns to be tightened:
# PRIVACY-AUDIT.md describes the SANITIZER removing and replacing identities,
# and LIMITATIONS.md uses the words "complete" and "attempt" in one sentence
# about something else entirely. Neither is a disclosure that a ledger row was
# removed, and neither is a claim that the history is whole.
SANITIZER_PROSE = (
    "The sanitizer derives the identities to remove at run time rather than "
    "from a list. A slug with its separators replaced is the same identity "
    "and is caught in that flattened form. A local-offset timestamp is "
    "rewritten to its UTC instant rather than deleted, so ordering and "
    "elapsed time survive while the offset does not.\n")
TWO_DISPOSITIONS_PROSE = (
    "One attempt was closed out by hand as failed and then wrote its own "
    "complete row, so one attempt carried two dispositions and the ledger "
    "audit refused it within the minute.\n")


def numbered(count: int, stem: str) -> str:
    """A document with `count` `##` sections, so a count claim has a truth."""
    out = [f"# {stem}\n"]
    for one in range(1, count + 1):
        out.append(f"## {one}. The {stem.lower()} numbered {one}.\n")
        out.append("This one is stated rather than pointed at, at a length "
                   "no residual test mistakes for a filename.\n")
    return "\n".join(out)


def handoff(members: int, limitations_word: str = "twelve",
            sibling_names: tuple[str, ...] = SIBLING_SUFFIXES,
            zip_digest: str = "", extra_entry: str = "",
            logs_extra: tuple[str, ...] = (), logs_word: str = "five",
            siblings_word: str = "six") -> str:
    siblings = "".join(
        f"{NAME}{one}, an artifact of the sealing pipeline;\n"
        for one in sibling_names)
    extra_logs = "".join(f", `{one}`" for one in logs_extra)
    return f"""# Selftest handoff

Every figure in this file is derived into `claims.json` and rendered in
`DERIVED-CLAIMS.md`.

## 1. Task and intended outcome

This lane exists to give the handoff inventory a package it can agree with,
so that every refusal the suite asserts is a refusal of one named defect and
not the noise of a tool that fails on everything it is shown.

The intended outcome is a package whose prose and whose bytes say the same
thing, member by member and figure by figure.

## 2. Branch

`{BRANCH}`

Not merged, and archived nowhere else.

## 3. Current commit and base commit

| | |
| --- | --- |
| head | `{HEAD}` |
| parent, the commit this lane starts from | `{PARENT}` |

The parent is an ancestor of the head and the range is two commits, derived
in `commits.txt` rather than asserted here.

## 4. Uncommitted changes

None. The working tree was clean at the head when this package was
assembled, and `claims.json` carries the derived reading.

## 5. Focused files changed

Three files.

| file | what it is |
| --- | --- |
| `src/one.js` | the production change |
| `tools/tests/test_one.py` | the regressions |
| `NOTES.md` | the durable record |

## 6. Startup commands and route state

Run `python3 -m unittest discover -s tools/tests` from the checkout root.
Then open the route with its required state: `/selftest/#book=Gen`.

## 7. Implementation summary

The correction is one function, which takes the record once and answers every
downstream question from that single reading rather than asking the raw
record again at each sink.

Nothing downstream reads the raw record, so no two readings can disagree.

## 8. Known limitations

Stated in full in `LIMITATIONS.md`, {limitations_word} of them. The one a
reviewer should read first is that the read-once contract is a claim about
one projection and not about one whole render, which is a narrower guarantee
than a reader might assume from the phrase.

## 9. Unresolved decisions

This lane leaves three unresolved decisions open, and each is put to the
reviewer as a question in `REVIEW_REQUEST.md` rather than settled here.

Whether one read per projection is the contract the review meant is the
first of them, and this lane does not presume the answer.

## 10. Artifact inventory

Every member of this package, and every artifact that lives beside it.

**Documents at the package root** — `HANDOFF.md` (this file),
`REVIEW_REQUEST.md`, `CLAIM-CLOSURE.md`, `PROVENANCE.md`,
`EVIDENCE-INDEX.md`, `DERIVED-CLAIMS.md`, `PRIVACY-AUDIT.md`,
`LIMITATIONS.md`, `UNRESOLVED-BLOCKERS.md`.

**Derived records at the package root** — `claims.json`, `checks.txt`,
`commits.txt`, `changed-files.txt`, `changes.patch`, `MANIFEST.sha256`.
There are four manifest rows.{extra_entry}

**`logs/`** — `logs/LOG-INDEX.md`, `logs/attempts.json`,
`logs/attempt-01/focused.log`, `logs/attempt-01/request-journals.log`{extra_logs} and
`logs/assemble.sh`. That is {logs_word} logs, one tool, and one ownership journal,
written by two attempts of which two battery rows survive.

**`screenshots/`** — `screenshots/INDEX.md` and two screenshots.

**Siblings, which live beside this directory and not inside it** —
{siblings}
The transport copy `{NAME}.zip` carries SHA-256 `{zip_digest}`.

This package holds {members} package members and {siblings_word} siblings.

**Conditional artifact classes, and why any is omitted.** Screenshots are
required for this lane and are present. A sources record is **omitted**,
because this lane adds no external source, edition or passage record of any
kind.
"""


CLAIM_CLOSURE = """# Claim closure

Against the uncorrected parent, the same file fails {ways} ways across
{methods} methods, each of them planted at a production sink rather than
inferred from an absence nobody forbade.
"""


class Inventory(unittest.TestCase):

    # -- the package under test -----------------------------------------

    def build(self, limitations=12, limitations_word="twelve",
              sibling_names=SIBLING_SUFFIXES, name_all_siblings=True,
              extra_entry="", extra_member=None, bad_zip_digest=False,
              ways="three", methods="two", checks_complete=True,
              stale_package_limitations=None,
              # -- the V15 substance checks, 9a through 9f -----------------
              checks_header=None, checks_epilogue="", empty_command=False,
              command_strings=None, recorded_verdict=None,
              extra_siblings=None, named_commits=None, document_prose=None):
        """One package on disk, wrong in whatever way the test asked for."""
        root = Path(tempfile.mkdtemp(prefix="handoff-inventory-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        package = root / NAME
        (package / "logs" / "attempt-01").mkdir(parents=True)
        (package / "screenshots").mkdir(parents=True)

        write = lambda rel, body: (package / rel).write_text(  # noqa: E731
            body, encoding="utf-8")

        write("REVIEW_REQUEST.md",
              "# Review request\n\n## Blockers\n\n1. Is one read per "
              "projection the contract?\n\n## Optional feedback\n\n"
              "1. Anything else worth naming.\n")
        write("CLAIM-CLOSURE.md",
              CLAIM_CLOSURE.format(ways=ways, methods=methods))
        write("PROVENANCE.md", "# Provenance\n\nOne attempt sealed this.\n")
        write("EVIDENCE-INDEX.md", "# Evidence index\n\nEvery log, once.\n")
        write("DERIVED-CLAIMS.md", "# Derived claims\n\nRendered figures.\n")
        write("PRIVACY-AUDIT.md", "# Privacy audit\n\nNo secret shipped.\n")
        write("LIMITATIONS.md", numbered(limitations, "Limitation"))
        write("UNRESOLVED-BLOCKERS.md", numbered(3, "Open blocker"))
        write("commits.txt", f"{HEAD}\n  a subject line\n"
                             f"{PARENT}\n  another subject line\n")
        write("changed-files.txt",
              "M\tsrc/one.js\nM\ttools/tests/test_one.py\nM\tNOTES.md\n")
        write("changes.patch", "--- a/src/one.js\n+++ b/src/one.js\n")
        write("MANIFEST.sha256", "".join(
            f"{'0' * 63}{one}  member-{one}.txt\n" for one in range(4)))
        write("claims.json", json.dumps({
            "identity": {"head": HEAD, "parent": PARENT, "branch": BRANCH,
                         "worktree_clean_at_head": True},
            "oracles": {"against_parent": {"identities": 3,
                                           "failing_method_count": 2,
                                           "methods_run": 400,
                                           "passing_methods": 398}},
        }, indent=2))

        logs = package / "logs"
        (logs / "LOG-INDEX.md").write_text("# Log index\n", encoding="utf-8")
        (logs / "assemble.sh").write_text("#!/bin/sh\n", encoding="utf-8")
        (logs / "attempts.json").write_text(json.dumps({"rows": [
            {"attempt": "head-01", "side": "head", "record": "attempt",
             "status": "complete"},
            {"attempt": "parent-02", "side": "parent", "record": "attempt",
             "status": "complete"},
        ]}, indent=2), encoding="utf-8")
        (logs / "attempt-01" / "focused.log").write_text(
            "ran\n", encoding="utf-8")
        (logs / "attempt-01" / "request-journals.log").write_text(
            "journal\n", encoding="utf-8")

        recorded = ["logs/attempt-01/focused.log"]
        if checks_complete:
            recorded.append("logs/attempt-01/request-journals.log")
        said = list(command_strings or ["python3 -c pass"] * len(recorded))
        rows = ""
        for index, one in enumerate(recorded):
            # 9a: a slot that names a step and records nothing to re-run.
            invocation = "" if (empty_command and index == 0) else said[index]
            rows += f"--- step {index}\n    command : {invocation}\n"
            # 9b/9c: the verdict `checks.py` writes about its own row.
            if recorded_verdict is not None:
                rows += f"    recorded: {recorded_verdict}\n"
            rows += f"    exit    : 0\n    log     : {one}\n\n"
        header = (checks_header if checks_header is not None else
                  "Every command this lane ran, its exact invocation and its "
                  "numeric exit.")
        write("checks.txt", header + "\n\n" + rows + checks_epilogue)

        # 9e: the commits this package discusses but was not produced from.
        if named_commits is not None:
            (logs / "named-commits.json").write_text(
                json.dumps(named_commits, indent=2), encoding="utf-8")

        # 9f: prose appended to a named member, so a claim in one document
        # and a disclosure in another are two documents, as a reader meets
        # them. Only HANDOFF.md is read for counts and references, so text
        # added here cannot disturb any other check.
        for rel, extra in (document_prose or {}).items():
            (package / rel).write_text(
                (package / rel).read_text(encoding="utf-8") + "\n" + extra,
                encoding="utf-8")

        shots = package / "screenshots"
        (shots / "INDEX.md").write_text("# Screenshots\n", encoding="utf-8")
        for one in ("before", "after"):
            (shots / f"{one}.png").write_bytes(b"\x89PNG\r\n\x1a\n")

        if extra_member:
            (package / extra_member).write_text("stray\n", encoding="utf-8")

        for suffix in SIBLING_SUFFIXES:
            (root / f"{NAME}{suffix}").write_text(
                f"a sibling artifact{suffix}\n", encoding="utf-8")
        # 9d/9e read siblings by name: `.executed-tools.json` and
        # `.attempts.jsonl`. A sibling that exists and is not named in the
        # inventory is a finding of its own, so these join `sibling_names`
        # and the spelled sibling count moves with them.
        for suffix, body in sorted((extra_siblings or {}).items()):
            (root / f"{NAME}{suffix}").write_text(body, encoding="utf-8")
        sibling_names = tuple(sibling_names) + tuple(
            sorted(extra_siblings or {}))
        digest = hashlib.sha256((root / f"{NAME}.zip").read_bytes()).hexdigest()
        if bad_zip_digest:
            digest = "0" * 63 + "1"

        if stale_package_limitations is not None:
            other = root / "20251201T000000Z-a-previous-package"
            other.mkdir()
            (other / "HANDOFF.md").write_text("# Previous\n", encoding="utf-8")
            (other / "LIMITATIONS.md").write_text(
                numbered(stale_package_limitations, "Limitation"),
                encoding="utf-8")

        members = sum(len(names) for _, _, names in os.walk(package)) + 1
        logs_extra = (("logs/named-commits.json",)
                      if named_commits is not None else ())
        write("HANDOFF.md", handoff(
            members=members, limitations_word=limitations_word,
            sibling_names=sibling_names if name_all_siblings
            else tuple(one for one in sibling_names
                       if one != ".handoff-inventory.log"),
            zip_digest=digest, extra_entry=extra_entry,
            logs_extra=logs_extra,
            logs_word=COUNT_WORD[5 + len(logs_extra)],
            siblings_word=COUNT_WORD[len(sibling_names)]))
        return package

    def run_tool(self, package, *extra):
        done = subprocess.run(
            [sys.executable, str(TOOL), "--package", str(package)]
            + list(extra), capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    # -- the control -----------------------------------------------------

    def test_a_complete_package_passes(self):
        # WITHOUT THIS EVERY REFUSAL BELOW IS VACUOUS.
        code, said = self.run_tool(self.build())
        self.assertEqual(code, 0, said)
        self.assertIn("problems: 0", said)
        self.assertIn("handoff inventory: COMPLETE", said)
        self.assertNotIn("NOT NAMED", said)
        self.assertNotIn("MISMATCH", said)

    def test_the_control_really_counts_rather_than_skipping(self):
        # A count check that resolves nothing would pass everything.
        _code, said = self.run_tool(self.build())
        for quantity in ("limitations", "commits", "changed_files",
                         "screenshots", "logs", "tools", "journals",
                         "attempts", "battery_rows", "manifest_rows",
                         "package_members", "siblings", "unresolved"):
            self.assertIn(quantity, said,
                          f"no count claim resolved against {quantity}")

    # -- 2. counts against the package's real contents --------------------

    def test_a_miscounted_limitation_count_fails(self):
        # THE REVIEW'S FIRST FINDING, EXACTLY: "eleven limitations while
        # twelve exist". Lexically perfect; substantively false.
        code, said = self.run_tool(self.build(limitations_word="eleven"))
        self.assertEqual(code, 1, said)
        self.assertIn("claims \"eleven\" limitations", said)
        self.assertIn("this package has 12", said)
        self.assertIn("`##` sections in LIMITATIONS.md", said)

    def test_a_stale_count_from_a_prior_package_is_named_as_stale(self):
        code, said = self.run_tool(self.build(
            limitations_word="eleven", stale_package_limitations=11))
        self.assertEqual(code, 1, said)
        self.assertIn("STALE COUNT from 20251201T000000Z-a-previous-package",
                      said)
        self.assertIn("this package has 12", said)

    def test_a_miscounted_member_total_fails(self):
        # An extra member nobody counted and nobody named.
        code, said = self.run_tool(self.build(extra_member="STRAY-NOTE.md"))
        self.assertEqual(code, 1, said)
        self.assertIn("package_members", said)
        self.assertIn("files under the package, recursive", said)

    # -- 3. siblings, discovered rather than declared ----------------------

    def test_an_undiscovered_sibling_fails(self):
        # THE REVIEW'S THIRD FINDING. Nobody passes `--sibling` for the
        # tool's own transcript, so the old tool could not miss it.
        code, said = self.run_tool(self.build(name_all_siblings=False))
        self.assertEqual(code, 1, said)
        self.assertIn(f"never names sibling artifact {NAME}"
                      f".handoff-inventory.log", said)

    def test_the_tools_own_log_is_required_even_before_it_exists(self):
        package = self.build(name_all_siblings=False)
        (package.parent / f"{NAME}.handoff-inventory.log").unlink()
        code, said = self.run_tool(package)
        self.assertEqual(code, 1, said)
        self.assertIn(".handoff-inventory.log", said)
        self.assertIn("never names sibling artifact", said)

    def test_an_explicitly_asserted_sibling_that_does_not_exist_fails(self):
        code, said = self.run_tool(self.build(),
                                   "--sibling", f"{NAME}.nonexistent.log")
        self.assertEqual(code, 1, said)
        self.assertIn(f"{NAME}.nonexistent.log", said)

    # -- 1/6. referenced files, and the bidirectional cross-check ----------

    def test_a_handoff_that_names_a_nonexistent_file_fails(self):
        code, said = self.run_tool(self.build(
            extra_entry=" The roster is `logs/no-such-transcript.log`."))
        self.assertEqual(code, 1, said)
        self.assertIn("HANDOFF.md names logs/no-such-transcript.log", said)
        self.assertIn("no such file in the package", said)

    def test_the_artifact_cross_check_drives_content_ten(self):
        # THE DOCSTRING'S CONTRACT, WHICH THE DISPATCH NEVER HONOURED: the
        # contents table used to print `10 ... PRESENT` while the artifact
        # table printed NOT NAMED rows.
        code, said = self.run_tool(self.build(extra_member="STRAY-NOTE.md"))
        self.assertEqual(code, 1, said)
        self.assertIn("never names package member STRAY-NOTE.md", said)
        self.assertIn("content #10", said)
        self.assertIn("INCOMPLETE -- the artifact cross-check", said)
        # And the row itself is no longer PRESENT.
        row = next(one for one in said.splitlines()
                   if one.strip().startswith("10  artifact inventory"))
        self.assertNotIn("PRESENT", row)
        self.assertIn("INCOMPLETE", row)

    # -- 4. hashes and identity -------------------------------------------

    def test_a_quoted_sha256_that_does_not_match_the_file_fails(self):
        code, said = self.run_tool(self.build(bad_zip_digest=True))
        self.assertEqual(code, 1, said)
        self.assertIn("quotes SHA-256", said)
        self.assertIn(f"for {NAME}.zip", said)
        self.assertIn("which hashes to", said)

    def test_a_head_the_handoff_never_states_fails(self):
        package = self.build()
        body = (package / "HANDOFF.md").read_text(encoding="utf-8")
        (package / "HANDOFF.md").write_text(
            body.replace(HEAD, "c" * 8 + "0" * 32), encoding="utf-8")
        code, said = self.run_tool(package)
        self.assertEqual(code, 1, said)
        self.assertIn(f"never states the head commit {HEAD}", said)
        self.assertIn("claims.json", said)

    def test_a_branch_the_handoff_never_names_fails(self):
        package = self.build()
        body = (package / "HANDOFF.md").read_text(encoding="utf-8")
        (package / "HANDOFF.md").write_text(
            body.replace(BRANCH, "impl/something-else"), encoding="utf-8")
        code, said = self.run_tool(package)
        self.assertEqual(code, 1, said)
        self.assertIn(f"never names the branch {BRANCH}", said)

    def test_an_unverifiable_claim_is_reported_unchecked_not_passed(self):
        package = self.build()
        (package / "claims.json").unlink()
        code, said = self.run_tool(package)
        self.assertIn("UNCHECKED", said)
        self.assertIn("no claims.json", said)

    # -- 7. derived figures against claims.json ----------------------------

    def test_a_closure_figure_that_contradicts_claims_json_fails(self):
        # THE REVIEW'S SECOND FINDING: "the closure record says the parent
        # fails ten ways across nine methods while derived claims say twelve
        # across eleven".
        code, said = self.run_tool(self.build(ways="ten", methods="nine"))
        self.assertEqual(code, 1, said)
        self.assertIn("CLAIM-CLOSURE.md says \"ten\" for ways the parent "
                      "fails", said)
        self.assertIn("claims.json derives 3", said)
        self.assertIn("methods the parent fails across", said)

    # -- 8. command coverage in checks.txt ---------------------------------

    def test_a_checks_file_that_omits_a_command_it_claims_to_carry_fails(self):
        # THE REVIEW'S FOURTH FINDING: "checks.txt claims every command while
        # expressly omitting seal, sanitize, derive, and audit commands".
        code, said = self.run_tool(self.build(checks_complete=False))
        self.assertEqual(code, 1, said)
        self.assertIn("checks.txt claims to record every command", said)
        self.assertIn("logs/attempt-01/request-journals.log", said)

    # -- 9. substance, not shape: the V15 checks ---------------------------
    #
    # Each of the six reads the CONTENT of the evidence rather than its
    # filenames, so each gets a fixture that trips exactly it, and a negative
    # fixture proving it stays silent on honest evidence. Without the second
    # half a check that always fires would pass its own test.

    # -- 9a. a command slot that records nothing to re-run -----------------

    def test_a_command_slot_with_no_invocation_fails(self):
        code, said = self.run_tool(self.build(empty_command=True))
        self.assertEqual(code, 1, said)
        self.assertIn("carries a `command :` slot with no invocation string",
                      said)
        self.assertIn("logs/attempt-01/focused.log", said)
        self.assertIn("handoff inventory: INCOMPLETE", said)

    def test_a_command_slot_that_records_an_invocation_is_silent(self):
        # The control for 9a: the same table, every slot filled.
        code, said = self.run_tool(self.build())
        self.assertEqual(code, 0, said)
        self.assertNotIn("no invocation string", said)

    # -- 9a (second arm). a transcript with no command row -----------------

    def test_a_transcript_with_no_command_row_fails_without_the_claim(self):
        # THE UNGATED ARM. The old check only fired when checks.txt used the
        # words "every command", so dropping the claim dropped the check.
        # A shipped log nothing accounts for is a hole either way.
        code, said = self.run_tool(self.build(
            checks_complete=False,
            checks_header="This file records the commands this lane ran."))
        self.assertEqual(code, 1, said)
        self.assertIn("carries no command row for the shipped transcript "
                      "logs/attempt-01/request-journals.log", said)
        self.assertIn("says nothing about the command that wrote it", said)
        # and NOT via the older arm, which this header does not arm
        self.assertNotIn("claims to record every command", said)

    def test_a_transcript_disclosed_in_prose_is_not_a_hole(self):
        # THE ESCAPE HATCH, KEPT. A file composed at P1 cannot carry a step
        # run at P5; one that NAMES the transcript it does not carry has told
        # the reader exactly what a reader needs.
        code, said = self.run_tool(self.build(
            checks_complete=False,
            checks_header="This file records the commands this lane ran.",
            checks_epilogue=(
                "Not carried here, and named rather than omitted in "
                "silence: logs/attempt-01/request-journals.log was written "
                "after this file was composed.\n")))
        self.assertEqual(code, 0, said)
        self.assertIn("DISCLOSED", said)
        self.assertNotIn("no command row", said)

    # -- 9b. a row the package itself marks ELIDED -------------------------

    def test_a_command_recorded_elided_fails(self):
        code, said = self.run_tool(self.build(
            recorded_verdict="ELIDED -- the capitalised token(s) PKG stand "
                             "in for values this lane held"))
        self.assertEqual(code, 1, said)
        self.assertIn("records its command ELIDED", said)
        self.assertIn("stand in for values this lane held", said)
        self.assertIn("logs/attempt-01/focused.log", said)
        self.assertIn("logs/attempt-01/request-journals.log", said)

    def test_a_command_recorded_literal_is_silent(self):
        code, said = self.run_tool(self.build(
            recorded_verdict="LITERAL -- the exact string handed to the "
                             "shell"))
        self.assertEqual(code, 0, said)
        self.assertNotIn("records its command ELIDED", said)
        self.assertNotIn("records its command PROSE", said)

    # -- 9c. a row the package itself marks PROSE --------------------------

    def test_a_command_recorded_prose_fails(self):
        code, said = self.run_tool(self.build(
            recorded_verdict="PROSE -- a description of what happened, not "
                             "a string a shell was handed"))
        self.assertEqual(code, 1, said)
        self.assertIn("records its command PROSE", said)
        self.assertIn("cannot be re-run as written", said)

    def test_the_word_elided_in_lower_case_prose_is_not_a_verdict(self):
        # The token is matched LITERALLY and in isolation, so the sentence
        # that EXPLAINS elision cannot be mistaken for a row that admits it.
        code, said = self.run_tool(self.build(
            recorded_verdict="LITERAL -- the exact string handed to the "
                             "shell; nothing in it was elided or described"))
        self.assertEqual(code, 0, said)
        self.assertNotIn("records its command ELIDED", said)

    # -- 9d. a tool recorded as never run, beside a command that runs it ---

    EXECUTED_SIBLING = ".executed-tools.json"

    def executed_record(self, tool: str, klass: str) -> dict:
        return {".executed-tools.json": json.dumps({
            "schema": "catena-executed-tools/1",
            "attempt": "package-20260101T000000Z-01",
            "anchor": "$EVIDENCE",
            "runs": [{"tool": tool, "path": f"logs/{tool}",
                      "attempt": "package-20260101T000000Z-01",
                      "sha256": "", "at": "2026-01-01T00:00:00Z",
                      "phase": "P8 final verification", "log": "",
                      "class": klass}],
        }, indent=2)}

    def test_a_tool_recorded_unrun_beside_a_command_that_runs_it_fails(self):
        code, said = self.run_tool(self.build(
            extra_siblings=self.executed_record("assemble.sh",
                                                "shipped-not-executed"),
            command_strings=["python3 logs/assemble.sh --package PKG",
                             "python3 -c pass"]))
        self.assertEqual(code, 1, said)
        self.assertIn("records assemble.sh as shipped-not-executed", said)
        self.assertIn("checks.txt records a command that runs it", said)

    def test_a_tool_no_command_names_may_be_recorded_unrun(self):
        # THE HALF THAT MATTERS. `shipped-not-executed` is the honest class
        # for a reviewer-facing helper the build never calls, and saying so
        # must not be a finding.
        code, said = self.run_tool(self.build(
            extra_siblings=self.executed_record("verify-final-package.py",
                                                "shipped-not-executed")))
        self.assertEqual(code, 0, said)
        self.assertNotIn("shipped-not-executed, but checks.txt", said)

    # -- 9e. a set-aside cohort with no row in the shipped history ---------

    SET_ASIDE = "cfa1b5fa5e415ed0cf9574cb4a8e5a03cd2629bf"

    def cohort_package(self, ledger_names_it: bool):
        rows = [{"attempt": "head-01", "record": "attempt",
                 "status": "complete"}]
        if ledger_names_it:
            rows.append({"attempt": "head-00", "record": "attempt",
                         "status": "set-aside", "head": self.SET_ASIDE,
                         "reason": "a green battery kept rather than "
                                   "deleted"})
        return self.build(
            named_commits={
                "_why": "Commits this package discusses but was not "
                        "produced from.",
                "commits": {
                    self.SET_ASIDE:
                        "A superseded head of this same lane. A head battery "
                        "ran green against it and was SET ASIDE rather than "
                        "deleted when the comparison moved the head.",
                },
            },
            extra_siblings={".attempts.jsonl": "".join(
                json.dumps(one, sort_keys=True) + "\n" for one in rows)})

    def test_a_set_aside_cohort_with_no_ledger_row_fails(self):
        code, said = self.run_tool(self.cohort_package(False))
        self.assertEqual(code, 1, said)
        self.assertIn("describes cfa1b5fa5e41 as a set-aside cohort", said)
        self.assertIn("carries no row naming it", said)

    def test_a_set_aside_cohort_the_ledger_names_is_silent(self):
        code, said = self.run_tool(self.cohort_package(True))
        self.assertEqual(code, 0, said)
        self.assertIn("IN THE SHIPPED HISTORY", said)
        self.assertNotIn("carries no row naming it", said)

    # -- 9f. a completeness claim another member contradicts ---------------

    CLAIM_PROSE = ("The complete append-only ledger is a sibling beside this "
                   "package, and the authority gate reads that one.\n")
    REMOVAL_PROSE = ("Two rows were removed from the fresh ledger, and that "
                     "is disclosed here rather than left for a reviewer to "
                     "find by counting. They recorded no event and nothing "
                     "had read them, so exactly those two lines were removed "
                     "and replaced with step notes carrying no disposition "
                     "at all.\n")

    def test_a_completeness_claim_another_member_contradicts_fails(self):
        code, said = self.run_tool(self.build(document_prose={
            "EVIDENCE-INDEX.md": self.CLAIM_PROSE,
            # The honest member: it claims AND discloses, in one place.
            "PROVENANCE.md": self.CLAIM_PROSE + self.REMOVAL_PROSE,
        }))
        self.assertEqual(code, 1, said)
        self.assertIn("EVIDENCE-INDEX.md calls this lane's history complete "
                      "or append-only", said)
        self.assertIn("PROVENANCE.md discloses that rows were removed", said)
        self.assertIn("DISCLOSES IT TOO", said)
        # THE EXEMPTION. The member that tells the whole truth in one place
        # is not the reader's problem and must not be reported as one.
        self.assertNotIn("PROVENANCE.md calls this lane's history", said)

    def test_honest_sanitizer_prose_is_not_a_disclosed_row_removal(self):
        # THE TWO FALSE-POSITIVE CLASSES, BOTH ARMED AT ONCE. A completeness
        # claim is present, so the check is live; what is absent is any
        # disclosure that a LEDGER ROW was removed. PRIVACY-AUDIT.md's
        # sentences are about the sanitizer removing and replacing
        # IDENTITIES, and LIMITATIONS.md's uses "complete" and "attempt" in
        # one sentence about two dispositions. Neither may arm this check.
        code, said = self.run_tool(self.build(document_prose={
            "EVIDENCE-INDEX.md": self.CLAIM_PROSE,
            "PRIVACY-AUDIT.md": SANITIZER_PROSE,
            "LIMITATIONS.md": TWO_DISPOSITIONS_PROSE,
        }))
        self.assertEqual(code, 0, said)
        self.assertIn("UNCONTRADICTED", said)
        self.assertNotIn("calls this lane's history complete", said)

    # -- 7 (patterns). the fact patterns are scoped and tightened ----------

    def test_an_english_word_no_longer_satisfies_a_sha_claim(self):
        # `\\b[0-9a-f]{7,40}\\b` matched `defaced`, and a bare `parent`
        # satisfied the base-commit clause, so a §3 with no SHA in it passed.
        package = self.build()
        body = (package / "HANDOFF.md").read_text(encoding="utf-8")
        body = body.replace(
            f"| head | `{HEAD}` |\n"
            f"| parent, the commit this lane starts from | `{PARENT}` |",
            "| head | the defaced facade of a parent commit |")
        (package / "HANDOFF.md").write_text(body, encoding="utf-8")
        code, said = self.run_tool(package)
        self.assertEqual(code, 1, said)
        self.assertIn("content #3", said)

    def test_a_fact_stated_only_in_another_section_no_longer_counts(self):
        # `evaluate_fact` used to search the WHOLE document, so §6's route
        # words could satisfy §6 from anywhere at all.
        package = self.build()
        body = (package / "HANDOFF.md").read_text(encoding="utf-8")
        body = body.replace(
            "Run `python3 -m unittest discover -s tools/tests` from the "
            "checkout root.\nThen open the route with its required state: "
            "`/selftest/#book=Gen`.",
            "There is nothing to run here.")
        (package / "HANDOFF.md").write_text(body, encoding="utf-8")
        code, said = self.run_tool(package)
        self.assertEqual(code, 1, said)
        self.assertIn("content #6", said)

    # -- 8 (exit codes). could-not-run is not found-problems ---------------

    def test_a_missing_package_exits_two_not_one(self):
        code, said = self.run_tool(Path("/nonexistent/package/directory"))
        self.assertEqual(code, 2, said)
        self.assertIn("HANDOFF INVENTORY COULD NOT RUN", said)
        self.assertIn("--package is not a directory", said)

    def test_a_package_without_a_handoff_exits_two(self):
        package = self.build()
        (package / "HANDOFF.md").unlink()
        code, said = self.run_tool(package)
        self.assertEqual(code, 2, said)
        self.assertIn("the package has no HANDOFF.md", said)

    def test_a_json_path_inside_the_package_is_still_refused(self):
        package = self.build()
        code, said = self.run_tool(package, "--json",
                                   str(package / "findings.json"))
        self.assertEqual(code, 2, said)
        self.assertIn("read-only over the package it inspects", said)
        self.assertFalse((package / "findings.json").exists())

    def test_the_error_path_still_writes_json(self):
        package = self.build()
        (package / "HANDOFF.md").unlink()
        out = package.parent / "findings.json"
        code, said = self.run_tool(package, "--json", str(out))
        self.assertEqual(code, 2, said)
        self.assertTrue(out.is_file(), said)
        payload = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(payload["verdict"], "SETUP FAILED")

    def test_the_success_path_writes_json_with_the_discovered_siblings(self):
        package = self.build()
        out = package.parent / "findings.json"
        code, said = self.run_tool(package, "--json", str(out))
        self.assertEqual(code, 0, said)
        payload = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(payload["verdict"], "COMPLETE")
        self.assertIn(f"{NAME}.handoff-inventory.log",
                      payload["siblings_discovered"])
        self.assertTrue(payload["count_claims"])

    # -- the reproduction ---------------------------------------------------

    def test_it_reproduces_the_v12_review_findings_unaided(self):
        # NO DEFAULT PATH. This module SHIPS INSIDE the package it helps
        # build, so a machine path written here would be a machine path in
        # the archive — the exact class of leak the lane exists to close, and
        # one the sealer would rewrite, breaking the executed-to-shipped
        # digest equality the review requires. The reviewed package is named
        # by the operator or the reproduction does not run.
        named = os.environ.get("V12_PACKAGE")
        if not named:
            self.skipTest("set V12_PACKAGE to the reviewed V12 package")
        reviewed = Path(named)
        if not reviewed.is_dir():
            self.skipTest("V12_PACKAGE is not a directory")
        code, said = self.run_tool(reviewed)
        self.assertEqual(code, 1, said)
        # 1. eleven limitations against twelve.
        self.assertIn("claims \"eleven\" limitations but this package has 12",
                      said)
        # 2. ten ways across nine methods against twelve across eleven.
        self.assertIn("CLAIM-CLOSURE.md says \"ten\" for ways the parent "
                      "fails but claims.json derives 12", said)
        self.assertIn("says \"nine\" for methods the parent fails across but "
                      "claims.json derives 11", said)
        # 3. the inventory omits the tool's own tracked transcript.
        self.assertIn("never names sibling artifact 20260817T194757Z-catena-"
                      "e1-corrections-v12.handoff-inventory.log", said)
        # 4. checks.txt claims every command and omits seal, sanitize,
        #    derive and audit.
        for one in ("seal.log", "seal-check.log", "derive-claims.log",
                    "head-consistency.log"):
            self.assertIn(f"no command row for logs/attempt-05/{one}", said)
        # And the cross-check now reaches the contents table.
        self.assertIn("content #10", said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
