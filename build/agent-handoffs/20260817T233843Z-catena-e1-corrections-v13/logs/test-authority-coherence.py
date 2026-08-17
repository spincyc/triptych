#!/usr/bin/env python3
"""THE COHERENCE GATE, DRIVEN AT EVERY WAY A PACKAGE CAN LIE ABOUT ITSELF.

A gate that has only ever been run against a package that passes is a gate
nobody has seen refuse. Each test here builds a package that is wrong in
exactly one way and asserts that the gate names that way -- and one builds the
package that is right and asserts that the gate is silent, so the refusals are
not simply a tool that always fails.

V13. The V12 suite's positive control PASSED WITHOUT A ZIP, without a P8
transcript and without any record of final authority, because the gate it
drove read two files. That is why its seventeen refusals were all
ledger-shaped: a suite can only refuse what its fixtures can build. The
control below now materialises the whole shipped set -- the package, the outer
log, the archive, the `.zip.sha256` sidecar, the P8 transcript, the
final-authority record and the external append-only ledger -- and every new
fixture breaks exactly one of them.

The two shapes the V12 review found in the shipped V12 package, and which no
fixture here could previously express:

  * `logs/attempts.json` carrying MORE THAN ONE row that reads
    `record=attempt status=authoritative`, demoted to one only by a
    last-state-wins resolver;
  * a sibling `<package>.SUPERSEDED.txt` sitting in the directory beside the
    package, which the gate never opened.

The last test is the one that matters most: the reviewed V11 package, if it is
present, must be REFUSED by this gate, reproducing the independent review's
own finding without being told what it was.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "authority-coherence.py"

HEAD = "1111111111111111111111111111111111111111"
OTHER_HEAD = "2222222222222222222222222222222222222222"
NAME = "20260817T000000Z-catena-e1-corrections-v13"
OTHER_NAME = "20260101T000000Z-something-else"
WINNER = "package-20260817T000000Z-03abcdef"
BATTERY = "head-20260817T000000Z-01ghjkmn"
PARENT_BATTERY = "parent-20260817T000000Z-02pqrstv"
DISCARDED = "package-20260817T000000Z-04wxyz23"
# A package attempt that sealed and simply was not the one P8 blessed. It
# ends `sealed`, which is a success, and so owes no reason.
SEALED_SIBLING = "package-20260817T000000Z-06stuvwx"
# The predecessor that really was authoritative once: it sealed, passed P8,
# was established by its own sidecar, and was then superseded.
PREDECESSOR = "package-20260817T000000Z-07y43xyz"
ESTABLISHED = "2026-08-17T00:05:00Z"

#: Passed for a fixture file that must NOT be written at all.
OMIT = object()


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
    last one -- EVERY state row moves it, which is the V12 defect this suite
    now drives at directly.
    """
    return {"attempt": one, "record": "state", "side": side,
            "status": status, "reason": reason, "order": "2"}


def sound_ledger():
    """A ledger that says one thing, and says it in both places.

    V13: the winning package attempt resolves to `sealed`, not
    `authoritative`. Every row in here was written before the manifest was
    taken, and so before P7 built the archive and before P8 judged it. Final
    authority is established outside, afterwards, by the sidecar.
    """
    rows = [
        attempt_row(BATTERY, "head", "complete"),
        attempt_row(PARENT_BATTERY, "parent", "complete"),
        attempt_row(DISCARDED, "package", "discarded",
                    reason="the sealer's own tests failed with exit 1"),
        attempt_row(WINNER, "package", "sealed",
                    package=NAME, head=HEAD, result=f"sealed {NAME}"),
    ]
    return {
        "attempts": [{"attempt": row["attempt"], "status": row["status"],
                      "reason": row["reason"]} for row in rows],
        "rows": rows,
    }


def sound_external():
    """The external, complete, append-only ledger the package projects from.

    Every attempt the package mentions ends here, and every terminal state
    that is not a SUCCESS says why.

    THE SUCCESSES CARRY NO REASON, deliberately. An earlier draft of this
    fixture gave every row a reason, including the `complete` batteries and
    the `sealed` package attempt, and that masked a contract bug in the gate:
    it demanded a reason from every state that was not `authoritative`, which
    would have refused every well-formed package ever built. A fixture that is
    tidier than reality tests the gate against a world that does not exist.
    """
    return [
        {"attempt": BATTERY, "record": "attempt", "side": "head",
         "status": "complete", "reason": ""},
        {"attempt": PARENT_BATTERY, "record": "attempt", "side": "parent",
         "status": "complete", "reason": ""},
        {"attempt": DISCARDED, "record": "attempt", "side": "package",
         "status": "discarded",
         "reason": "the sealer's own tests failed with exit 1"},
        {"attempt": WINNER, "record": "attempt", "side": "package",
         "status": "sealed", "reason": ""},
        {"attempt": WINNER, "record": "state", "side": "package",
         "status": "authoritative", "reason": ""},
    ]


def sound_outer():
    return (f"== attempt {WINNER} (invocation log: {NAME}.assemble.log)\n"
            f"== head {HEAD}\n"
            f"== sealed: attempt {WINNER} is the sealed attempt for {NAME}\n"
            f"== P8 PASS; attempt {WINNER} is the authoritative package "
            f"attempt for {NAME}\n")


def sound_prose():
    return (f"The authoritative attempt is `{WINNER}`, established after P8 "
            f"for `{NAME}`.\n")


def sound_sidecar(digest, size):
    """`sha256sum -c` compatible on line 1; the byte size on line 2."""
    return f"{digest}  {NAME}.zip\n{size} bytes  {NAME}.zip\n"


def sound_verify(digest, size, verdict="PASS", rehash="UNCHANGED",
                 post_digest=None, post_size=None):
    """The P8 transcript, in verify-final-package.py's own shape."""
    post_digest = digest if post_digest is None else post_digest
    post_size = size if post_size is None else post_size
    return (
        "--- check 1 header\n"
        "[1 header] ok\n"
        "--- post-verification rehash of the archive bytes\n"
        "    checks performed : 1 header, 2 layout, 3 manifest\n"
        f"    pre-check bytes  : {size}\n"
        f"    pre-check sha256 : {digest}\n"
        f"    post-check bytes : {post_size}\n"
        f"    post-check sha256: {post_digest}\n"
        f"    result           : {rehash} -- the archive named in the header\n"
        f"P8 verification: {verdict} (0 problem(s))\n")


def sound_authority(digest, size):
    """THE CONTRACT. The one record that establishes final authority.

    It is written AFTER P8, beside the package and never inside it, and it
    quotes what P8 proved: the archive's exact basename, byte size and
    SHA-256, the P8 verdict and the post-verification rehash. The binding runs
    one way -- this names the archive's digest; the archive does not name
    this one's.
    """
    return {
        "schema": "catena-final-authority/1",
        "attempt": WINNER,
        "package": NAME,
        "head": HEAD,
        "zip_name": f"{NAME}.zip",
        "zip_bytes": size,
        "zip_sha256": digest,
        "p8_log": f"{NAME}.verify-final.log",
        "p8_result": "PASS",
        "rehash_result": "UNCHANGED",
        "rehash_bytes": size,
        "rehash_sha256": digest,
        "status": "authoritative",
        "established": ESTABLISHED,
    }


class Gate(unittest.TestCase):

    def build(self, ledger=None, outer=None, prose=None, marker=None,
              sibling=None, archive=True, extra_member=None, sidecar=None,
              verify=None, authority=None, external=None):
        """The whole shipped set on disk, wrong in whatever way the test asked.

        `None` means "the sound default". `OMIT` means "do not write this file
        at all". Anything else is used verbatim, except `authority`, which is
        a dict of overrides merged into the sound record -- a key whose value
        is `OMIT` is deleted from it.
        """
        root = Path(tempfile.mkdtemp(prefix="coherence-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        package = root / NAME
        (package / "logs").mkdir(parents=True)
        (package / "logs" / "attempts.json").write_text(
            json.dumps(ledger if ledger is not None else sound_ledger(),
                       indent=2, sort_keys=True), encoding="utf-8")
        (package / "PROVENANCE.md").write_text(
            sound_prose() if prose is None else prose, encoding="utf-8")
        if marker:
            (package / marker).write_text("discarded\n", encoding="utf-8")
        if extra_member:
            (package / extra_member).write_text("{}\n", encoding="utf-8")

        if outer is not OMIT:
            (root / f"{NAME}.assemble.log").write_text(
                sound_outer() if outer is None else outer, encoding="utf-8")
        if sibling:
            (root / sibling).write_text("superseded\n", encoding="utf-8")

        # -- P7: the archive, and the digest everything downstream quotes --
        digest, size = "0" * 64, 0
        if archive:
            path = root / f"{NAME}.zip"
            with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as handle:
                for member in sorted(package.rglob("*")):
                    if member.is_file():
                        handle.writestr(
                            member.relative_to(package).as_posix(),
                            member.read_bytes())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            size = path.stat().st_size
        if sidecar is not OMIT:
            (root / f"{NAME}.zip.sha256").write_text(
                sound_sidecar(digest, size) if sidecar is None else sidecar,
                encoding="utf-8")

        # -- P8: the transcript, then the record that quotes it ------------
        if verify is not OMIT:
            (root / f"{NAME}.verify-final.log").write_text(
                sound_verify(digest, size) if verify is None else verify,
                encoding="utf-8")
        if authority is not OMIT:
            record = sound_authority(digest, size)
            if authority:
                record.update(authority)
                record = {key: value for key, value in record.items()
                          if value is not OMIT}
            (root / f"{NAME}.authority.json").write_text(
                json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")

        if external is not OMIT:
            wanted = sound_external() if external is None else external
            (root / f"{NAME}.attempts.jsonl").write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n"
                        for row in wanted), encoding="utf-8")
        return package

    def run_gate(self, package, *extra):
        done = subprocess.run(
            [sys.executable, str(GATE), "--package", str(package),
             "--head", HEAD, *extra],
            capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    # -- the control ---------------------------------------------------

    def test_a_coherent_package_passes(self):
        # WITHOUT THIS EVERY REFUSAL BELOW IS VACUOUS. And it now requires a
        # real ZIP, a real digest sidecar, a real P8 transcript and a real
        # final-authority record: the V12 control passed without any of them.
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
        # No record establishes final authority, so there is no winner.
        code, said = self.run_gate(self.build(authority=OMIT))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative attempts: 0, not 1", said)
        self.assertIn("the final-authority record is missing", said)

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
                row["package"] = OTHER_NAME
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative for", said)

    def test_an_authoritative_attempt_at_another_head_is_refused(self):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["head"] = OTHER_HEAD
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
        self.assertIn("this package's own attempt is superseded", said)

    def test_a_second_terminal_row_for_one_attempt_is_refused(self):
        ledger = sound_ledger()
        ledger["rows"].append(
            attempt_row(WINNER, "package", "discarded", reason="a second"))
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("more than one terminal row", said)

    def test_a_superseded_sealed_attempt_is_named_as_such(self):
        # The summary still says `sealed` while a later state row supersedes
        # it. The rows win, and they disagree.
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

    # -- a battery whose figures were not used says so, and says why ----
    # `complete` could not distinguish a battery whose figures the package
    # cites from one whose figures it silently dropped, so both shipped as
    # `complete` with an empty reason. `set-aside` is the word for the second,
    # and the word is worthless without the reason.

    def _set_aside(self, reason):
        ledger = sound_ledger()
        ledger["rows"].append(
            state_row(PARENT_BATTERY, "parent", "set-aside", reason=reason))
        for one in ledger["attempts"]:
            if one["attempt"] == PARENT_BATTERY:
                one["status"] = "set-aside"
                one["reason"] = reason
        external = sound_external() + [
            {"attempt": PARENT_BATTERY, "record": "state", "side": "parent",
             "status": "set-aside", "reason": reason}]
        return self.build(ledger, external=external)

    def test_a_battery_set_aside_with_a_reason_passes(self):
        code, said = self.run_gate(self._set_aside(
            "the parent battery ran green, but its figures are not cited: the "
            "comparison this package makes is head-only"))
        self.assertEqual(code, 0, said)
        self.assertIn("PASS (0 problems)", said)

    def test_a_battery_set_aside_with_no_reason_is_refused(self):
        code, said = self.run_gate(self._set_aside(""))
        self.assertEqual(code, 1, said)
        self.assertIn("set-aside with no reason", said)

    def test_a_package_attempt_set_aside_is_refused(self):
        # `set-aside` belongs to the battery vocabulary only. A package
        # attempt's bytes are the deliverable, not a figure to cite; it is
        # discarded or superseded, never set aside.
        ledger = sound_ledger()
        ledger["rows"].append(
            state_row(DISCARDED, "package", "set-aside",
                      reason="its figures were not used"))
        for one in ledger["attempts"]:
            if one["attempt"] == DISCARDED:
                one["status"] = "set-aside"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("a package attempt may not be 'set-aside'", said)

    # -- NO SEALED BYTE HOLDS FINAL AUTHORITY ---------------------------
    # The V12 review's substantive finding: authority was written at P5,
    # inside the package, before the archive existed and before P8 judged it.
    # But the refusal is on the HELD CLAIM, never on the presence of the word
    # -- a predecessor's honest history must stay expressible, because the
    # only other way to satisfy the gate is to delete it.

    def test_an_authoritative_disposition_row_is_refused(self):
        # Rule (a): `authoritative` on a `record=attempt` row. A terminal row
        # is written before P8 and cannot carry P8's verdict.
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["status"] = "authoritative"
        for one in ledger["attempts"]:
            if one["attempt"] == WINNER:
                one["status"] = "authoritative"
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("carries 'authoritative' as a DISPOSITION, on a "
                      "record=attempt row", said)
        self.assertIn("The most a terminal row may say is 'sealed'", said)

    def test_a_state_row_claiming_authoritative_is_refused(self):
        # Rule (b): a `record=state status=authoritative` row with nothing
        # superseding it leaves the attempt HOLDING the claim inside shipped
        # bytes. (V12's resolver updated the resolved state only for
        # `superseded`, so it dropped this row entirely and the count never
        # saw the second claimant.)
        ledger = sound_ledger()
        ledger["rows"].append(state_row(DISCARDED, "package", "authoritative"))
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("still RESOLVES to 'authoritative' inside the package",
                      said)
        self.assertIn("authoritative attempts: 2, not 1", said)

    # -- but a predecessor's honest history is not a claim ---------------

    def _with_predecessor(self, superseded=True):
        """`sealed -> authoritative -> superseded`, the real eleven-attempt shape.

        Attempt 07 sealed, passed P8, was legitimately established
        authoritative by its own post-P8 sidecar, and was superseded at P10
        with its one reason. Attempt 11 then sealed cleanly. Both facts are
        true, and both must stay in the record.
        """
        reason = "superseded by a later package attempt at P10"
        ledger = sound_ledger()
        ledger["rows"].append(
            attempt_row(PREDECESSOR, "package", "sealed",
                        package=NAME, head=HEAD, result=f"sealed {NAME}"))
        ledger["rows"].append(
            state_row(PREDECESSOR, "package", "authoritative"))
        external = sound_external() + [
            {"attempt": PREDECESSOR, "record": "attempt", "side": "package",
             "status": "sealed", "reason": ""}]
        if superseded:
            ledger["rows"].append(
                state_row(PREDECESSOR, "package", "superseded", reason=reason))
            external.append(
                {"attempt": PREDECESSOR, "record": "state", "side": "package",
                 "status": "superseded", "reason": reason})
        ledger["attempts"].append({
            "attempt": PREDECESSOR,
            "status": "superseded" if superseded else "authoritative",
            "reason": reason if superseded else ""})
        return self.build(ledger, external=external)

    def test_a_superseded_predecessor_that_was_once_authoritative_passes(self):
        # THE POSITIVE CONTROL FOR THE HISTORY RULE. Without it the refusal
        # below is just the old over-broad rule wearing a new message, and the
        # live-fire deadlock comes straight back.
        code, said = self.run_gate(self._with_predecessor(superseded=True))
        self.assertEqual(code, 0, said)
        self.assertIn("PASS (0 problems)", said)
        self.assertIn("one authoritative attempt", said)

    def test_a_predecessor_still_holding_authority_is_refused(self):
        # The same history with the supersession MISSING: the predecessor
        # still resolves to `authoritative`, so two attempts claim it.
        code, said = self.run_gate(self._with_predecessor(superseded=False))
        self.assertEqual(code, 1, said)
        self.assertIn("still RESOLVES to 'authoritative' inside the package",
                      said)
        self.assertIn("a predecessor must already be superseded before a "
                      "replacement seals".lower(), said.lower())
        self.assertIn("authoritative attempts: 2, not 1", said)

    def test_an_external_authoritative_disposition_row_is_refused(self):
        # Rule (a) holds in the external scope too. The winner MUST resolve
        # to `authoritative` there, but on a state row, never as the attempt's
        # own disposition.
        rows = [row for row in sound_external()
                if not (row["attempt"] == WINNER and row["record"] == "state")]
        for row in rows:
            if row["attempt"] == WINNER:
                row["status"] = "authoritative"
        code, said = self.run_gate(self.build(external=rows))
        self.assertEqual(code, 1, said)
        self.assertIn("carries 'authoritative' as a DISPOSITION, on a "
                      "record=attempt row", said)

    def test_an_authoritative_winner_later_discarded_is_refused(self):
        # Same `elif`: V12 looked only for a later `superseded`, so a later
        # `discarded` left the winner still winning.
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["status"] = "authoritative"
        for one in ledger["attempts"]:
            if one["attempt"] == WINNER:
                one["status"] = "authoritative"
        ledger["rows"].append(
            state_row(WINNER, "package", "discarded",
                      reason="P8 refused the archive"))
        code, said = self.run_gate(self.build(ledger))
        self.assertEqual(code, 1, said)
        self.assertIn("this package's own attempt is discarded", said)

    # -- the final-authority record binds the final ZIP -----------------

    def test_a_record_claiming_a_digest_the_zip_does_not_have_is_refused(self):
        code, said = self.run_gate(self.build(
            authority={"zip_sha256": "a" * 64, "rehash_sha256": "a" * 64}))
        self.assertEqual(code, 1, said)
        self.assertIn("but the archive's own bytes hash to", said)

    def test_a_record_naming_the_wrong_zip_basename_is_refused(self):
        code, said = self.run_gate(self.build(
            authority={"zip_name": f"{OTHER_NAME}.zip"}))
        self.assertEqual(code, 1, said)
        self.assertIn("names archive", said)

    def test_a_record_claiming_the_wrong_zip_size_is_refused(self):
        code, said = self.run_gate(self.build(
            authority={"zip_bytes": 1, "rehash_bytes": 1}))
        self.assertEqual(code, 1, said)
        self.assertIn("but the archive is", said)

    def test_a_record_at_another_implementation_head_is_refused(self):
        code, said = self.run_gate(self.build(authority={"head": OTHER_HEAD}))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative at head", said)

    def test_a_record_omitting_the_zip_size_is_refused(self):
        code, said = self.run_gate(self.build(authority={"zip_bytes": OMIT}))
        self.assertEqual(code, 1, said)
        self.assertIn("no 'zip_bytes'", said)

    def test_a_record_omitting_the_zip_digest_is_refused(self):
        code, said = self.run_gate(self.build(authority={"zip_sha256": OMIT}))
        self.assertEqual(code, 1, said)
        self.assertIn("no 'zip_sha256'", said)

    def test_a_record_naming_no_attempt_is_refused(self):
        code, said = self.run_gate(self.build(authority={"attempt": ""}))
        self.assertEqual(code, 1, said)
        self.assertIn("names no attempt", said)
        self.assertIn("authoritative attempts: 0, not 1", said)

    def test_a_record_that_is_not_yet_authoritative_is_refused(self):
        code, said = self.run_gate(self.build(authority={"status": "sealed"}))
        self.assertEqual(code, 1, said)
        self.assertIn("exists only to say 'authoritative'", said)

    def test_a_record_with_an_unknown_key_is_refused(self):
        code, said = self.run_gate(self.build(
            authority={"authority_sha256": "b" * 64}))
        self.assertEqual(code, 1, said)
        self.assertIn("unknown key 'authority_sha256'", said)

    def test_a_record_with_a_non_integer_size_is_refused(self):
        code, said = self.run_gate(self.build(authority={"zip_bytes": "912"}))
        self.assertEqual(code, 1, said)
        self.assertIn("'zip_bytes' must be an integer", said)

    def test_a_missing_final_authority_record_is_refused(self):
        code, said = self.run_gate(self.build(authority=OMIT))
        self.assertEqual(code, 1, said)
        self.assertIn("nothing else may establish final authority", said)

    def test_an_authority_record_inside_the_archive_is_refused(self):
        # The binding runs ONE WAY. A record the archive vouched for is a
        # record the archive could have been sealed around.
        code, said = self.run_gate(self.build(
            extra_member=f"{NAME}.authority.json"))
        self.assertEqual(code, 1, said)
        self.assertIn("may not live inside the archive it binds", said)

    # -- and only after P8 ----------------------------------------------

    def test_a_p8_transcript_recording_fail_is_refused(self):
        package = self.build()
        digest, size = self._archive_identity(package)
        (package.parent / f"{NAME}.verify-final.log").write_text(
            sound_verify(digest, size, verdict="FAIL"), encoding="utf-8")
        code, said = self.run_gate(package)
        self.assertEqual(code, 1, said)
        self.assertIn("P8 verification is FAIL, not PASS", said)
        self.assertIn("the attempt remains non-authoritative", said)

    def test_a_post_p8_rehash_mismatch_is_refused(self):
        package = self.build()
        digest, size = self._archive_identity(package)
        (package.parent / f"{NAME}.verify-final.log").write_text(
            sound_verify(digest, size, rehash="CHANGED",
                         post_digest="c" * 64), encoding="utf-8")
        code, said = self.run_gate(package)
        self.assertEqual(code, 1, said)
        self.assertIn("the post-P8 rehash is CHANGED, not UNCHANGED", said)

    def test_a_missing_p8_transcript_is_refused(self):
        code, said = self.run_gate(self.build(verify=OMIT))
        self.assertEqual(code, 1, said)
        self.assertIn("the P8 transcript is missing", said)

    def test_a_missing_archive_is_refused(self):
        code, said = self.run_gate(self.build(archive=False))
        self.assertEqual(code, 1, said)
        self.assertIn("the shipped archive is missing", said)

    def test_a_sidecar_disagreeing_with_the_archive_is_refused(self):
        code, said = self.run_gate(self.build(
            sidecar=f"{'d' * 64}  {NAME}.zip\n17 bytes  {NAME}.zip\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("says the archive is", said)

    def test_a_missing_digest_sidecar_is_refused(self):
        code, said = self.run_gate(self.build(sidecar=OMIT))
        self.assertEqual(code, 1, said)
        self.assertIn("the archive digest sidecar is missing", said)

    # -- the external complete ledger resolves every attempt ------------

    def test_an_external_ledger_missing_an_attempt_is_refused(self):
        code, said = self.run_gate(self.build(
            external=[row for row in sound_external()
                      if row["attempt"] != DISCARDED]))
        self.assertEqual(code, 1, said)
        self.assertIn("carries no row for it", said)

    def test_an_external_ledger_that_leaves_success_unexplained_passes(self):
        # THE NORMAL SHAPE, AND A POSITIVE CONTROL. A battery that ran green
        # and a package attempt that sealed are successes; they owe no account
        # of themselves, and a gate that demands one refuses every
        # well-formed package ever built. `sound_external()` is already this
        # shape, so this fixture adds the case it cannot carry: a MENTIONED
        # package attempt whose last external row is `sealed`, since the
        # winner's own last row must be `authoritative`.
        ledger = sound_ledger()
        ledger["rows"].append(
            attempt_row(SEALED_SIBLING, "package", "sealed",
                        package=NAME, head=HEAD, result=f"sealed {NAME}"))
        ledger["attempts"].append(
            {"attempt": SEALED_SIBLING, "status": "sealed", "reason": ""})
        external = sound_external() + [
            {"attempt": SEALED_SIBLING, "record": "attempt", "side": "package",
             "status": "sealed", "reason": ""}]
        code, said = self.run_gate(self.build(ledger, external=external))
        self.assertEqual(code, 0, said)
        self.assertIn("PASS (0 problems)", said)

    def test_an_external_discarded_state_with_no_reason_is_refused(self):
        rows = sound_external()
        for row in rows:
            if row["attempt"] == DISCARDED:
                row["reason"] = ""
        code, said = self.run_gate(self.build(external=rows))
        self.assertEqual(code, 1, said)
        self.assertIn("ends it 'discarded' with no reason", said)
        self.assertIn("a terminal state that is not a success says why", said)

    def test_an_external_failed_battery_with_no_reason_is_refused(self):
        rows = sound_external()
        for row in rows:
            if row["attempt"] == BATTERY:
                row["status"] = "failed"
        code, said = self.run_gate(self.build(external=rows))
        self.assertEqual(code, 1, said)
        self.assertIn("ends it 'failed' with no reason", said)

    def test_an_external_ledger_that_ends_the_winner_otherwise_is_refused(self):
        rows = [row for row in sound_external()
                if not (row["attempt"] == WINNER and row["record"] == "state")]
        rows.append({"attempt": WINNER, "record": "state", "side": "package",
                     "status": "superseded", "reason": "a later package"})
        code, said = self.run_gate(self.build(external=rows))
        self.assertEqual(code, 1, said)
        self.assertIn("ends it 'superseded'", said)

    def test_a_missing_external_ledger_is_refused(self):
        code, said = self.run_gate(self.build(external=OMIT))
        self.assertEqual(code, 1, said)
        self.assertIn("no external attempt ledger was found", said)

    # -- and every other record agrees ----------------------------------

    def test_an_outer_log_naming_another_attempt_authoritative_is_refused(self):
        code, said = self.run_gate(self.build(
            outer=f"== head {HEAD}\n== {NAME}\n== sealed: attempt {DISCARDED} "
                  f"is the authoritative one for {NAME}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative, but the final-authority record names",
                      said)

    def test_an_outer_log_disagreeing_with_the_structured_record_is_refused(self):
        # The structured record names WINNER; the outer log names nobody but
        # the attempt that lost.
        code, said = self.run_gate(self.build(
            outer=f"== attempt {DISCARDED}\n== head {HEAD}\n"
                  f"== sealed: {DISCARDED} is the authoritative one for "
                  f"{NAME}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn(f"never names the authoritative attempt {WINNER}", said)

    def test_the_wrong_package_on_the_authoritative_outer_line_is_refused(self):
        # V12 checked only that the package name appeared SOMEWHERE in the
        # file, never that the line claiming authority named the right one.
        code, said = self.run_gate(self.build(
            outer=f"== attempt {WINNER}\n== head {HEAD}\n== {NAME}\n"
                  f"== sealed: attempt {WINNER} is the authoritative one for "
                  f"{OTHER_NAME}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("the line claiming authority names package", said)

    def test_an_uppercase_attempt_id_claiming_authority_is_refused(self):
        # V12 tested `if "authoritative" not in line` on the UN-lowercased
        # line, so an outer log shouting AUTHORITATIVE was skipped outright,
        # and its id regex was lowercase-only besides.
        code, said = self.run_gate(self.build(
            outer=sound_outer()
            + f"== NOTE: {DISCARDED.upper()} IS THE AUTHORITATIVE PACKAGE "
              f"ATTEMPT FOR {NAME}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("a case variant of", said)
        self.assertIn("authoritative, but the final-authority record names",
                      said)

    def test_a_missing_outer_log_is_refused(self):
        code, said = self.run_gate(self.build(outer=OMIT))
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
        # THE SHAPE V11 ACTUALLY SHIPPED, in its own `checks.txt`: the attempt
        # on one line and its status on the next. A same-line test reads this
        # stanza as clean, which is how the contradiction survived to be found
        # by a human instead.
        code, said = self.run_gate(self.build(
            prose=f"--- seal\n    attempt : {WINNER}\n"
                  f"    status  : unresolved: the ledger carries no terminal "
                  f"row for this attempt\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("describes the authoritative attempt as unresolved",
                      said)

    def test_multiline_prose_naming_another_winner_is_refused(self):
        # The claim on one line, the id on the NEXT. V12 iterated only the ids
        # found on the same line, so this stanza produced zero faults.
        code, said = self.run_gate(self.build(
            prose=f"The authoritative attempt is:\n    {DISCARDED}\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("authoritative, but the final-authority record names",
                      said)

    def test_an_unresolved_attempt_described_as_final_is_refused(self):
        code, said = self.run_gate(self.build(
            prose=f"--- final authority\n    attempt : {WINNER}\n"
                  f"    status  : unresolved: P8 has not been read back\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("describes the authoritative attempt as unresolved",
                      said)

    def test_prose_that_never_names_the_winner_is_refused(self):
        # V12 faulted only prose naming a DIFFERENT attempt; prose that simply
        # never settled the question passed.
        code, said = self.run_gate(self.build(
            prose="This package is the one to review. It was built carefully "
                  "and every check ran green.\n"))
        self.assertEqual(code, 1, said)
        self.assertIn("no prose member names", said)

    # -- and nothing here, or beside here, was abandoned ----------------

    def test_a_package_carrying_a_discard_marker_is_refused(self):
        code, said = self.run_gate(self.build(marker="DISCARDED.txt"))
        self.assertEqual(code, 1, said)
        self.assertIn("discard marker", said)

    def test_a_sibling_zip_discard_marker_for_the_winner_is_refused(self):
        # V12 globbed INSIDE the package only, so `<name>.zip.DISCARDED.txt`
        # -- which the pipeline writes BESIDE it -- was invisible.
        code, said = self.run_gate(self.build(
            sibling=f"{NAME}.zip.DISCARDED.txt"))
        self.assertEqual(code, 1, said)
        self.assertIn("sibling discard/supersession marker", said)
        self.assertIn(f"{NAME}.zip.DISCARDED.txt", said)

    def test_a_sibling_supersession_marker_for_the_winner_is_refused(self):
        # The exact file the shipped V12 package carried beside it.
        code, said = self.run_gate(self.build(sibling=f"{NAME}.SUPERSEDED.txt"))
        self.assertEqual(code, 1, said)
        self.assertIn("sibling discard/supersession marker", said)

    def test_a_missing_ledger_is_refused(self):
        package = self.build()
        (package / "logs" / "attempts.json").unlink()
        code, said = self.run_gate(package)
        self.assertEqual(code, 1, said)
        self.assertIn("the ledger is not optional", said)

    # -- before P8, nobody is authoritative -----------------------------

    def _pre_p8_package(self, **extra):
        ledger = sound_ledger()
        for row in ledger["rows"]:
            if row["attempt"] == WINNER:
                row["status"] = "sealing"
        for one in ledger["attempts"]:
            if one["attempt"] == WINNER:
                one["status"] = "sealing"
        settings = dict(
            ledger=ledger, archive=False, sidecar=OMIT, verify=OMIT,
            authority=OMIT, external=OMIT,
            outer=f"== attempt {WINNER}\n== head {HEAD}\n== sealing {NAME}\n",
            prose=f"`{WINNER}` sealed `{NAME}`; P8 has not run.\n")
        settings.update(extra)
        return self.build(**settings)

    def test_a_pre_p8_attempt_claiming_nothing_passes(self):
        code, said = self.run_gate(self._pre_p8_package(), "--pre-p8")
        self.assertEqual(code, 0, said)
        self.assertIn("no attempt claims final authority", said)

    def test_a_pre_p8_attempt_with_an_authority_record_is_refused(self):
        code, said = self.run_gate(self.build(), "--pre-p8")
        self.assertEqual(code, 1, said)
        self.assertIn("the attempt has reached P8 or is claiming to", said)

    def test_a_pre_p8_attempt_whose_prose_claims_authority_is_refused(self):
        code, said = self.run_gate(
            self._pre_p8_package(prose=sound_prose()), "--pre-p8")
        self.assertEqual(code, 1, said)
        self.assertIn("claims final authority before P8", said)

    # -- helpers ---------------------------------------------------------

    def _archive_identity(self, package):
        path = package.parent / f"{NAME}.zip"
        return hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_size

    # -- the reproduction ------------------------------------------------

    def test_it_reproduces_the_v11_finding_unaided(self):
        # Point V11_PACKAGE at an extracted copy of the reviewed V11 package
        # to run this. The reviewed package is not shipped inside this one --
        # it is immutable on its own evidence branch and copying it here would
        # be a second copy of an artifact that already has a home -- so the
        # transcript of this run is shipped instead, at
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
