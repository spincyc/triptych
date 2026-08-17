#!/usr/bin/env python3
"""THE COHERENCE GATE, DRIVEN AT EVERY WAY A PACKAGE CAN LIE ABOUT ITSELF.

A gate that has only ever been run against a package that passes is a gate
nobody has seen refuse. Each test here builds a package that is wrong in
exactly one way and asserts that the gate names that way — and one builds the
package that is right and asserts that the gate is silent, so the refusals
are not simply a tool that always fails.

The last test is the one that matters most: the reviewed V11 package, if it
is present, must be REFUSED by this gate, reproducing the independent
review's own finding without being told what it was.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "authority-coherence.py"

HEAD = "1111111111111111111111111111111111111111"
NAME = "20260817T000000Z-catena-e1-corrections-v12"
WINNER = "package-20260817T000000Z-03abcdef"
BATTERY = "head-20260817T000000Z-01ghjkmn"
PARENT_BATTERY = "parent-20260817T000000Z-02pqrstv"
DISCARDED = "package-20260817T000000Z-04wxyz23"


def attempt_row(one, side, status, **extra):
    """A terminal row: the disposition, carried once, with its one reason."""
    row = {"attempt": one, "record": "attempt", "side": side,
           "status": status, "reason": "", "order": "1",
           "log": "logs/attempt-01/battery.log"}
    row.update(extra)
    return row


def state_row(one, side, status, reason=""):
    """A non-terminal state, or the post-terminal `superseded`.

    Superseding does not overwrite the verdict it supersedes, so it rides its
    own row and the terminal row stays where it is. The RESOLVED state is the
    last one.
    """
    return {"attempt": one, "record": "state", "side": side,
            "status": status, "reason": reason, "order": "2"}


def sound_ledger():
    """A ledger that says one thing, and says it in both places."""
    rows = [
        attempt_row(BATTERY, "head", "complete"),
        attempt_row(PARENT_BATTERY, "parent", "complete"),
        attempt_row(DISCARDED, "package", "discarded",
                    reason="the sealer's own tests failed with exit 1"),
        attempt_row(WINNER, "package", "authoritative",
                    package=NAME, head=HEAD, result=f"sealed {NAME}"),
    ]
    return {
        "attempts": [{"attempt": row["attempt"], "status": row["status"],
                      "reason": row["reason"]} for row in rows],
        "rows": rows,
    }


class Gate(unittest.TestCase):

    def build(self, ledger=None, outer=None, prose=None, marker=None):
        """One package on disk, wrong in whatever way the test asked for."""
        root = Path(tempfile.mkdtemp(prefix="coherence-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        package = root / NAME
        (package / "logs").mkdir(parents=True)
        (package / "logs" / "attempts.json").write_text(
            json.dumps(ledger if ledger is not None else sound_ledger(),
                       indent=2, sort_keys=True), encoding="utf-8")
        if outer is None:
            outer = (f"== attempt {WINNER} (invocation log: {NAME}.assemble.log)\n"
                     f"== head {HEAD}\n"
                     f"== sealed: attempt {WINNER} is the authoritative one "
                     f"for {NAME}\n")
        (root / f"{NAME}.assemble.log").write_text(outer, encoding="utf-8")
        (package / "PROVENANCE.md").write_text(
            prose if prose is not None
            else f"The authoritative attempt is `{WINNER}`.\n",
            encoding="utf-8")
        if marker:
            (package / marker).write_text("discarded\n", encoding="utf-8")
        return package

    def run_gate(self, package):
        done = subprocess.run(
            [sys.executable, str(GATE), "--package", str(package),
             "--head", HEAD],
            capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    # -- the control ---------------------------------------------------

    def test_a_coherent_package_passes(self):
        # WITHOUT THIS EVERY REFUSAL BELOW IS VACUOUS.
        code, said = self.run_gate(self.build())
        self.assertEqual(code, 0, said)
        self.assertIn("PASS (0 problems)", said)

    # -- one authoritative attempt, and only one ------------------------

    def test_two_authoritative_package_attempts_are_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == DISCARDED:
                row["status"] = "authoritative"
                row["reason"] = ""
                row["package"] = NAME
                row["head"] = HEAD
                row["result"] = f"sealed {NAME}"
        for one in ledger["attempts"]:
            if one["attempt"] == DISCARDED:
                one["status"] = "authoritative"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative attempts: 2, not 1", said)

    def test_no_authoritative_attempt_at_all_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["status"] = "sealing"
        for one in ledger["attempts"]:
            if one["attempt"] == WINNER:
                one["status"] = "sealing"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative attempts: 0, not 1", said)

    def test_a_battery_written_authoritative_is_refused(self):
        # THE V11 DEFECT'S ROOT. One word for two facts made the count
        # uncountable.
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == BATTERY:
                row["status"] = "authoritative"
        for one in ledger["attempts"]:
            if one["attempt"] == BATTERY:
                one["status"] = "authoritative"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("a validation battery is not an authoritative package",
                      said)

    # -- and it is THIS package, at THIS head ---------------------------

    def test_an_authoritative_attempt_for_another_package_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["package"] = "20260101T000000Z-something-else"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative for", said)

    def test_an_authoritative_attempt_at_another_head_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["head"] = "2222222222222222222222222222222222222222"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative at head", said)

    def test_an_authoritative_attempt_that_did_not_seal_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["result"] = "in progress"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("not sealed", said)

    # -- nothing is two things at once ----------------------------------

    def test_an_attempt_both_authoritative_and_superseded_is_refused(self):
        ledger = sound_ledger()
        ledger["rows"].append(
            state_row(WINNER, "package", "superseded",
                      reason="a later package supersedes this one"))
        for one in ledger["attempts"]:
            if one["attempt"] == WINNER:
                one["status"] = "superseded"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        # It resolves to `superseded`, so it is not counted authoritative --
        # and the package is left with none, which is the refusal.
        self.assertIn("authoritative attempts: 0, not 1", said)

    def test_a_second_terminal_row_for_one_attempt_is_refused(self):
        ledger = sound_ledger()
        ledger["rows"].append(
            attempt_row(WINNER, "package", "discarded", reason="a second"))
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("more than one terminal row", said)

    def test_a_superseded_authoritative_attempt_is_named_as_such(self):
        # The other direction: the summary still says authoritative while a
        # later state row supersedes it. The rows win, and they disagree.
        ledger = sound_ledger()
        ledger["rows"].append(
            state_row(WINNER, "package", "superseded", reason="replaced"))
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("the rows resolve to 'superseded'", said)

    def test_an_unresolved_attempt_is_refused(self):
        # V11 SHIPPED EXACTLY THIS STRING for the attempt it was built from.
        ledger = sound_ledger()
        ledger["attempts"].append({
            "attempt": "package-20260817T000000Z-05mnpqrs",
            "status": "unresolved: the ledger carries no terminal row for "
                      "this attempt",
            "reason": ""})
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("unresolved in the shipped ledger", said)
        self.assertIn("no terminal row", said)

    def test_a_discarded_attempt_with_no_reason_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == DISCARDED:
                row["reason"] = ""
        for one in ledger["attempts"]:
            if one["attempt"] == DISCARDED:
                one["reason"] = ""
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("discarded with no reason", said)

    def test_a_summary_that_contradicts_its_own_rows_is_refused(self):
        ledger = sound_ledger()
        for one in ledger["attempts"]:
            if one["attempt"] == DISCARDED:
                one["status"] = "sealing"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("the summary says", said)

    # -- and every other record agrees ----------------------------------

    def test_an_outer_log_naming_another_attempt_authoritative_is_refused(self):
        code, said = self.run_gate(self.build(
            outer=f"== head {HEAD}\n== sealed: attempt {DISCARDED} is the "
                  f"authoritative one for {NAME}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative, but the ledger names", said)

    def test_a_missing_outer_log_is_refused(self):
        package = self.build()
        (package.parent / f"{NAME}.assemble.log").unlink()
        code, said = self.run_gate(package)
        self.assertEqual(code, 1, said)
        self.assertIn("outer invocation log is missing", said)

    def test_prose_naming_another_attempt_the_survivor_is_refused(self):
        # V11's PROVENANCE.md called the SUPERSEDED attempt the survivor.
        code, said = self.run_gate(self.build(
            prose=f"`{DISCARDED}` is the attempt that survived, and it is the "
                  f"one this package was built from.\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("the survivor", said)

    def test_prose_calling_the_authoritative_attempt_unresolved_is_refused(self):
        # THE SHAPE V11 ACTUALLY SHIPPED, in its own `checks.txt`: the
        # attempt on one line and its status on the next. A same-line test
        # reads this stanza as clean, which is how the contradiction
        # survived to be found by a human instead.
        code, said = self.run_gate(self.build(
            prose=f"--- seal\n    attempt : {WINNER}\n"
                  f"    status  : unresolved: the ledger carries no terminal "
                  f"row for this attempt\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("describes the authoritative attempt as unresolved",
                      said)

    # -- and nothing here was abandoned ---------------------------------

    def test_a_package_carrying_a_discard_marker_is_refused(self):
        code, said = self.run_gate(self.build(marker="DISCARDED.txt"))
        self.assertEqual(code, 1, said)
        self.assertIn("discard marker", said)

    def test_a_missing_ledger_is_refused(self):
        package = self.build()
        (package / "logs" / "attempts.json").unlink()
        code, said = self.run_gate(package)
        self.assertEqual(code, 1, said)
        self.assertIn("the ledger is not optional", said)

    # -- the reproduction ------------------------------------------------

    def test_it_reproduces_the_v11_finding_unaided(self):
        # Point V11_PACKAGE at an extracted copy of the reviewed V11 package
        # to run this. The reviewed package is not shipped inside this one --
        # it is immutable on its own evidence branch and copying it here
        # would be a second copy of an artifact that already has a home --
        # so the transcript of this run is shipped instead, at
        # `logs/v11-authority-reproduction.txt`.
        import os
        named = os.environ.get("V11_PACKAGE")
        reviewed = (Path(named) if named
                    else HERE / "v11pkg"
                    / "20260816T172726Z-catena-e1-corrections-v11")
        if not reviewed.is_dir():
            self.skipTest("set V11_PACKAGE to an extracted copy of the "
                          "reviewed V11 package to run this")
        done = subprocess.run(
            [sys.executable, str(GATE), "--package", str(reviewed),
             "--head", "0255b84996e1dc24da3ce75ac318c4f774b7957c"],
            capture_output=True, text=True)
        said = done.stdout + done.stderr
        self.assertEqual(done.returncode, 1, said)
        # The three the review named, each found without being told.
        self.assertIn("authoritative attempts: 3, not 1", said)
        self.assertIn("package-20260816T172726Z-08vvjhkw: unresolved", said)
        self.assertIn("a validation battery is not an authoritative package",
                      said)
        # And the attempt it DOES call authoritative is the superseded one.
        self.assertIn("package-20260816T172114Z-07835xnr", said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
