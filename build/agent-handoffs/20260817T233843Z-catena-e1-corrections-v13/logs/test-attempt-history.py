#!/usr/bin/env python3
"""THE ATTEMPT HISTORY, DRIVEN AT EVERY WAY V12'S RECORD OF ITSELF WAS WRONG.

The V12 review found that the lane's own history — which attempts ran, which
commit each measured, which ordinals were spent, how each ended and why — was
not recoverable from anything the lane shipped. Ordinals 03/04/05/06 were
reissued as 03/04/05 over a ledger file the operator had started fresh; four
discarded package attempts and four set-aside battery cohorts are in no
surviving ledger while three shipped members assert they are; all five summary
reasons were empty; ten rows named log roots the package did not contain; a
supersession was stamped thirty seconds after the freeze of the file carrying
it; and a battery could be told which commit it measured only by an argument
nothing compared to the checkout.

Each test below builds a history that is wrong in exactly one of those ways and
asserts the tool NAMES that way. Two build the history that is right and assert
the tools are silent, so the refusals are not simply tools that always fail.

`unittest`, stdlib only, run as `python3 test-attempt-history.py`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "checks.py"
BATTERY = HERE / "battery.sh"

LANE = "V13"
HEAD_ONE = "head-20260817T120000Z-01ghjkmn"
PARENT_ONE = "parent-20260817T121000Z-02pqrstv"
PACKAGE_ONE = "package-20260817T123000Z-03wxyz23"


def lane_row(lane: str = LANE) -> dict:
    return {"record": "lane", "lane": lane, "opened": "2026-08-17T11:59:00Z"}


def state(attempt, no, side, status, start, end, reason="", **extra) -> dict:
    row = {"attempt": attempt, "attempt_no": str(no), "lane": LANE,
           "record": "state", "side": side, "status": status,
           "reason": reason, "start": start, "end": end}
    row.update(extra)
    return row


def step(attempt, no, side, start, end, log, **extra) -> dict:
    row = {"attempt": attempt, "attempt_no": str(no), "lane": LANE,
           "record": "step", "side": side, "start": start, "end": end,
           "exit": "0", "log": log, "command": "python3 -m unittest discover"}
    row.update(extra)
    return row


def terminal(attempt, no, side, status, start, end, reason="", **extra) -> dict:
    row = {"attempt": attempt, "attempt_no": str(no), "lane": LANE,
           "record": "attempt", "side": side, "status": status,
           "reason": reason, "start": start, "end": end, "exit": "0",
           "log": f"logs/order-{side}.txt"}
    row.update(extra)
    return row


def sound_rows() -> list[dict]:
    """A lane history that says one thing and says it everywhere.

    Two batteries that completed and one package attempt that SEALED. Ordinals
    01, 02, 03, each carried by exactly one attempt; every attempt terminal
    exactly once; every id's embedded instant agreeing with its own first row;
    every row appended in the order it closed.

    `sealed`, NOT `authoritative`. The package attempt's terminal row is
    written at P5, before the manifest, the archive and the verification, so
    the most it may claim is that the directory is sealed. The post-P8 winner
    is a separate, later `record=state status=authoritative` row and it exists
    only in the external complete ledger -- `external_winner()` below adds it.
    """
    return [
        lane_row(),
        state(HEAD_ONE, 1, "head", "started",
              "2026-08-17T12:00:00Z", "2026-08-17T12:00:00Z"),
        step(HEAD_ONE, 1, "head", "2026-08-17T12:00:05Z",
             "2026-08-17T12:04:00Z", "logs/attempt-01/focused-head.log"),
        terminal(HEAD_ONE, 1, "head", "complete",
                 "2026-08-17T12:00:00Z", "2026-08-17T12:04:01Z"),
        state(PARENT_ONE, 2, "parent", "started",
              "2026-08-17T12:10:00Z", "2026-08-17T12:10:00Z"),
        step(PARENT_ONE, 2, "parent", "2026-08-17T12:10:05Z",
             "2026-08-17T12:14:00Z",
             "logs/attempt-02/focused-parent.log"),
        terminal(PARENT_ONE, 2, "parent", "complete",
                 "2026-08-17T12:10:00Z", "2026-08-17T12:14:01Z"),
        state(PACKAGE_ONE, 3, "package", "started",
              "2026-08-17T12:30:00Z", "2026-08-17T12:30:00Z"),
        terminal(PACKAGE_ONE, 3, "package", "sealed",
                 "2026-08-17T12:30:00Z", "2026-08-17T12:40:00Z",
                 package="20260817T123000Z-catena-e1", head="1" * 40,
                 result="sealed 20260817T123000Z-catena-e1"),
    ]


def external_winner(attempt=PACKAGE_ONE, no=3) -> dict:
    """The post-P8 row, which exists ONLY in the external complete ledger.

    Appended after the archive verified, beside the authority sidecar bound to
    the final ZIP. Post-terminal, exactly like `superseded`: the attempt
    already terminated `sealed` and that verdict is not overwritten.
    """
    return state(attempt, no, "package", "authoritative",
                 "2026-08-17T12:50:00Z", "2026-08-17T12:50:00Z")


class Fixture(unittest.TestCase):
    """A temp directory, a ledger in it, and one way to run the tool."""

    def temp(self, prefix="attempt-history-") -> Path:
        root = Path(tempfile.mkdtemp(prefix=prefix))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        return root

    def ledger(self, rows, root: Path | None = None) -> Path:
        root = root or self.temp()
        path = root / "attempt-ledger.jsonl"
        path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8")
        return path

    def run_checks(self, *args) -> tuple[int, str]:
        done = subprocess.run([sys.executable, str(CHECKS), *[str(one) for one
                                                              in args]],
                              capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def allocate(self, *args) -> tuple[int, str, str]:
        """THE ORDINAL COMES BACK ON STDOUT, ALONE, and that is the contract.

        `battery.sh` captures stdout and nothing else, so a diagnostic that
        leaked onto it would be parsed as an ordinal. The tests read the two
        streams apart for the same reason.
        """
        done = subprocess.run(
            [sys.executable, str(CHECKS), "--allocate-ordinal",
             *[str(one) for one in args]], capture_output=True, text=True)
        return done.returncode, done.stdout.strip(), done.stdout + done.stderr

    def verify(self, rows, *extra) -> tuple[int, str]:
        return self.run_checks("--verify-ledger", "--attempts",
                               self.ledger(rows), "--lane", LANE, *extra)


class Control(Fixture):
    """Without these, every refusal below is vacuous."""

    def test_a_sound_lane_history_passes(self):
        code, said = self.verify(sound_rows())
        self.assertEqual(code, 0, said)
        self.assertIn("problems: 0", said)
        self.assertIn(f"{HEAD_ONE}: complete", said)
        self.assertIn(f"{PACKAGE_ONE}: sealed", said)

    def test_a_fresh_lane_ledger_is_opened_and_allocates_from_one(self):
        path = self.temp() / "ledger.jsonl"
        code, out, said = self.allocate("--attempts", path, "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertEqual(out, "1")
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        self.assertEqual(rows[0]["record"], "lane")
        self.assertEqual(rows[0]["lane"], LANE)


class Ordinals(Fixture):
    """AN ORDINAL IS ALLOCATED ONCE FOR THE LANE, AND NEVER REISSUED."""

    def test_an_ordinal_reused_across_a_ledger_reset_is_refused(self):
        # THE V12 INCIDENT, EXACTLY. The operator started a fresh ledger file
        # partway through the lane; `max(attempt_no) + 1` over the new file
        # returned 03 again, and two different attempts came to answer to one
        # ordinal and therefore to one log root.
        rows = sound_rows()
        rows += [
            state("package-20260817T140000Z-03qrstvw", 3, "package", "started",
                  "2026-08-17T14:00:00Z", "2026-08-17T14:00:00Z"),
            terminal("package-20260817T140000Z-03qrstvw", 3, "package",
                     "discarded", "2026-08-17T14:00:00Z",
                     "2026-08-17T14:05:00Z",
                     reason="the sealer's own tests failed with exit 1"),
        ]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("attempt ordinal 03 is carried by 2 attempts", said)
        self.assertIn("never reissued", said)

    def test_the_allocator_refuses_an_ordinal_the_lane_has_spent(self):
        path = self.ledger(sound_rows())
        code, _out, said = self.allocate("--attempts", path, "--lane", LANE,
                                         "--propose", "2")
        self.assertEqual(code, 1, said)
        self.assertIn("attempt ordinal 02 has already been carried by", said)
        self.assertIn(PARENT_ONE, said)

    def test_a_spent_ordinal_stays_spent_when_its_attempt_was_discarded(self):
        # The point of the rule: a discarded attempt's ordinal is not freed.
        rows = sound_rows()
        rows += [terminal("package-20260817T140000Z-04qrstvw", 4, "package",
                          "discarded", "2026-08-17T14:00:00Z",
                          "2026-08-17T14:05:00Z",
                          reason="the consistency audit failed with exit 1")]
        path = self.ledger(rows)
        code, _out, said = self.allocate("--attempts", path, "--lane", LANE,
                                         "--propose", "4")
        self.assertEqual(code, 1, said)
        self.assertIn("attempt ordinal 04 has already been carried by", said)

    def test_the_allocator_hands_out_the_next_unspent_ordinal(self):
        path = self.ledger(sound_rows())
        code, out, said = self.allocate("--attempts", path, "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertEqual(out, "4")


class LaneIdentity(Fixture):
    """A LEDGER BELONGS TO ONE LANE, AND SAYS SO ON EVERY ROW."""

    def test_appending_to_a_ledger_of_a_different_lane_is_refused(self):
        path = self.ledger(sound_rows())
        code, _out, said = self.allocate("--attempts", path, "--lane", "V12")
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane 'V13', not 'V12'", said)

    def test_opening_a_fresh_ledger_over_an_existing_one_is_refused(self):
        path = self.ledger(sound_rows())
        code, _out, said = self.allocate("--attempts", path, "--lane", LANE,
                                         "--fresh")
        self.assertEqual(code, 1, said)
        self.assertIn("--fresh asks for a new lane ledger", said)
        self.assertIn("they stay spent", said)

    def test_a_ledger_that_names_no_lane_is_refused(self):
        rows = [row for row in sound_rows() if row.get("record") != "lane"]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no record=lane row", said)

    def test_a_row_of_another_lane_inside_this_one_is_refused(self):
        rows = sound_rows()
        for row in rows:
            if row.get("attempt") == PARENT_ONE:
                row["lane"] = "V12"
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("rows of another lane are present in this one", said)


class Dispositions(Fixture):
    """EVERY ATTEMPT ENDS ONCE, AND SAYS WHY WHEN IT DID NOT GO AS INTENDED."""

    def test_a_terminal_state_with_an_empty_reason_is_refused(self):
        rows = sound_rows()
        rows += [terminal("package-20260817T140000Z-04qrstvw", 4, "package",
                          "discarded", "2026-08-17T14:00:00Z",
                          "2026-08-17T14:05:00Z", reason="")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("with an empty reason", said)
        self.assertIn("says why, in words, on the row that states it", said)

    def test_an_attempt_with_no_terminal_row_is_refused(self):
        rows = [row for row in sound_rows()
                if not (row.get("attempt") == HEAD_ONE
                        and row.get("record") == "attempt")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn(f"{HEAD_ONE}: no terminal row", said)

    def test_two_terminal_rows_for_one_attempt_are_refused(self):
        rows = sound_rows()
        rows += [terminal(HEAD_ONE, 1, "head", "failed",
                          "2026-08-17T12:00:00Z",
                          "2026-08-17T12:05:00Z",
                          reason="a second verdict for one attempt")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("more than one terminal row", said)

    def test_a_superseded_attempt_carries_its_reason_to_the_summary(self):
        # V12 shipped five summary reasons and every one was empty, two of
        # them supersessions whose reasons sat on rows nothing joined.
        rows = sound_rows()
        rows += [
            state(PACKAGE_ONE, 3, "package", "superseded",
                  "2026-08-17T13:00:00Z", "2026-08-17T13:00:00Z",
                  reason="P7 failed to archive; replaced by a later attempt"),
            state("package-20260817T150000Z-04qrstvw", 4, "package", "started",
                  "2026-08-17T15:00:00Z", "2026-08-17T15:00:00Z"),
            terminal("package-20260817T150000Z-04qrstvw", 4, "package",
                     "sealed", "2026-08-17T15:00:00Z",
                     "2026-08-17T15:10:00Z",
                     package="20260817T150000Z-catena-e1", head="1" * 40,
                     result="sealed 20260817T150000Z-catena-e1"),
        ]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertIn("superseded -- P7 failed to archive", said)


class SetAside(Fixture):
    """A BATTERY THAT COMPLETED AND WAS NOT USED HAS A WORD FOR IT."""

    def test_a_set_aside_battery_with_a_reason_is_accepted_and_reported(self):
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:00:00Z",
                       "2026-08-17T16:00:00Z",
                       reason="the cohort ran at the parent's tree by "
                              "mistake; its figures were not used")]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: set-aside -- the cohort ran at the "
                      f"parent's tree", said)

    def test_a_set_aside_battery_with_no_reason_is_refused(self):
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:00:00Z",
                       "2026-08-17T16:00:00Z", reason="")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("set-aside", said)
        self.assertIn("empty reason", said)

    def test_set_aside_is_not_a_package_word(self):
        rows = sound_rows()
        rows += [state(PACKAGE_ONE, 3, "package", "set-aside",
                       "2026-08-17T16:00:00Z",
                       "2026-08-17T16:00:00Z",
                       reason="wrong vocabulary for a package attempt")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("a package attempt is never 'set-aside'", said)


class SealedNotAuthoritative(Fixture):
    """NO SEALED PACKAGE BYTES MAY CLAIM FINAL AUTHORITY BEFORE P8.

    Every row that reaches `logs/attempts.json` is written at or before P5 and
    frozen there, because P6 hashes the member. A row inside the package
    claiming `authoritative` therefore asserts the outcome of the manifest, the
    archive and the verification before any of them ran -- which is what V12
    shipped. The most a package attempt may claim about ITSELF, in bytes it
    ships, is `sealed`. `authoritative` is established afterwards, in the
    external complete ledger and the sidecar bound to the final ZIP.
    """

    def package(self, rows) -> tuple[Path, Path]:
        root = self.temp("seal-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        logs.mkdir(parents=True)
        (logs / "order-head.txt").write_text(
            f"PREFLIGHT battery=head\nattempt={HEAD_ONE}\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text(
            f"PREFLIGHT battery=parent\nattempt={PARENT_ONE}\n",
            encoding="utf-8")
        return package, self.ledger(rows, root)

    def seal(self, rows) -> tuple[int, str]:
        package, ledger = self.package(rows)
        return self.run_checks(
            "--seal-ledger", "--package", package, "--attempts", ledger,
            "--attempt", PACKAGE_ONE, "--attempt-no", "3", "--lane", LANE,
            "--package-name", "20260817T123000Z-catena-e1",
            "--head", "1" * 40)

    def test_seal_ledger_accepts_a_sealed_attempt(self):
        # THE CONTROL. Without it the refusal below is vacuous.
        code, said = self.seal(sound_rows())
        if "cannot load the sealer" in said:
            self.skipTest("sanitize-and-seal.py is not loadable right now")
        self.assertEqual(code, 0, said)
        self.assertIn(f"{PACKAGE_ONE}: sealed", said)

    def test_seal_ledger_refuses_an_in_package_authoritative_row(self):
        rows = sound_rows()
        for row in rows:
            if (row.get("attempt") == PACKAGE_ONE
                    and row.get("record") == "attempt"):
                row["status"] = "authoritative"
        code, said = self.seal(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("P6, P7 and P8 have not run", said)
        self.assertIn("Write status=sealed here", said)
        self.assertIn("sidecar", said)
        self.assertIn("AUTHORITY AUDIT FAILED", said)

    def test_seal_ledger_refuses_an_authoritative_predecessor_still_holding(
            self):
        # A previous package that passed its own P8 must be SUPERSEDED before
        # a replacement may be sealed; until then nothing may ship saying some
        # attempt still holds authority these bytes cannot have established.
        rows = sound_rows() + [external_winner()]
        rows += [
            state("package-20260817T150000Z-04qrstvw", 4, "package", "started",
                  "2026-08-17T15:00:00Z", "2026-08-17T15:00:00Z"),
            terminal("package-20260817T150000Z-04qrstvw", 4, "package",
                     "sealed", "2026-08-17T15:00:00Z",
                     "2026-08-17T15:10:00Z",
                     package="20260817T123000Z-catena-e1", head="1" * 40,
                     result="sealed 20260817T123000Z-catena-e1"),
        ]
        package, ledger = self.package(rows)
        code, said = self.run_checks(
            "--seal-ledger", "--package", package, "--attempts", ledger,
            "--attempt", "package-20260817T150000Z-04qrstvw", "--attempt-no",
            "4", "--lane", LANE, "--package-name",
            "20260817T123000Z-catena-e1", "--head", "1" * 40)
        self.assertEqual(code, 1, said)
        self.assertIn("in a record frozen at P5", said)
        self.assertIn("Supersede the previous winner", said)

    def test_the_external_ledger_may_record_the_post_p8_winner(self):
        # The other half of the split: `sealed` -> `authoritative` is exactly
        # the transition the EXTERNAL complete ledger exists to record.
        code, said = self.verify(sound_rows() + [external_winner()])
        self.assertEqual(code, 0, said)
        self.assertIn("scope external", said)
        self.assertIn(f"{PACKAGE_ONE}: authoritative", said)

    def test_in_package_scope_refuses_a_row_that_still_holds_authority(self):
        # The contract, not the sentence: in bytes frozen at P5, NOBODY may
        # still hold the post-P8 word. Which of the two rules says so depends
        # on the shape of the row, and both name P8 as the reason.
        code, said = self.verify(sound_rows() + [external_winner()],
                                 "--in-package")
        self.assertEqual(code, 1, said)
        self.assertIn("scope in-package", said)
        self.assertIn("after P8", said)
        self.assertIn(PACKAGE_ONE, said)

    def test_in_package_scope_ships_a_superseded_predecessors_history(self):
        # V13: the word may appear in shipped bytes as HISTORY. A predecessor
        # that really did pass P8, really was authoritative and was then
        # superseded is exactly the record V12 deleted instead of keeping, and
        # a package sealed afterwards carries it. What is refused is an
        # attempt that STILL HOLDS authority, which the sibling test pins.
        rows = sound_rows() + [external_winner()]
        rows.append(state(PACKAGE_ONE, 3, "package", "superseded",
                          "2026-08-17T12:55:00Z", "2026-08-17T12:55:00Z",
                          reason="replaced by the attempt that sealed after "
                                 "it, for the reason this row carries"))
        code, said = self.verify(rows, "--in-package")
        self.assertEqual(code, 0, said)
        self.assertIn("scope in-package", said)
        self.assertIn(f"{PACKAGE_ONE}: superseded", said)

    def test_authoritative_may_not_be_a_terminal_row_even_externally(self):
        # It arrives after the attempt already terminated `sealed`, so it can
        # never be the disposition; that is true in both scopes.
        rows = sound_rows()
        for row in rows:
            if (row.get("attempt") == PACKAGE_ONE
                    and row.get("record") == "attempt"):
                row["status"] = "authoritative"
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("must not be carried by a record=attempt row", said)

    def test_a_battery_may_not_be_sealed(self):
        rows = sound_rows()
        for row in rows:
            if (row.get("attempt") == HEAD_ONE
                    and row.get("record") == "attempt"):
                row["status"] = "sealed"
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("a battery attempt is never 'sealed'", said)


class LedgerPath(Fixture):
    """EITHER LEDGER PATH WORKS MECHANICALLY. Only one keeps the guarantee."""

    def test_allocate_and_verify_work_against_a_per_package_ledger_path(self):
        # The assembler lane may point $ATTEMPTS at a per-package file beside
        # the package rather than the lane-wide one. Nothing here assumes a
        # filename, and the parent directory is created if it is missing.
        root = self.temp("per-package-")
        path = (root / "build" / "agent-handoffs"
                / "20260817T123000Z-catena-e1.attempts.jsonl")
        code, out, said = self.allocate("--attempts", path, "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertEqual(out, "1")
        self.assertTrue(path.is_file())
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn("lane V13", said)

    def test_a_per_package_ledger_cannot_see_ordinals_another_file_spent(self):
        # THE COST, MADE VISIBLE. Ordinal uniqueness is a property of ONE
        # file. Split the lane across two and 01 is handed out twice, which is
        # the V12 defect wearing a tidier filename. The lane-wide ledger is
        # what the guarantee rests on; this test exists so that is not a
        # sentence in a report but a fact the suite states.
        root = self.temp("split-")
        first, second = root / "one.jsonl", root / "two.jsonl"
        for path in (first, second):
            code, out, said = self.allocate("--attempts", path, "--lane",
                                            LANE)
            self.assertEqual(code, 0, said)
            self.assertEqual(out, "1")


class Chronology(Fixture):
    """A RECORD OF WHEN THINGS HAPPENED IS CHECKABLE, OR IT IS DECORATION."""

    def test_a_row_ending_after_the_freeze_instant_is_refused(self):
        # V12: attempt 04's supersession is stamped 19:46:00Z inside a file
        # whose own phase note says it was frozen at 19:45:30Z.
        rows = sound_rows()
        rows += [state(PACKAGE_ONE, 3, "package", "superseded",
                       "2026-08-17T19:46:00Z",
                       "2026-08-17T19:46:00Z",
                       reason="P8 verification failed")]
        code, said = self.verify(rows, "--frozen-at",
                                 "2026-08-17T19:45:30Z")
        self.assertEqual(code, 1, said)
        self.assertIn("AFTER the instant this ledger member is frozen at",
                      said)

    def test_a_row_that_ends_before_it_starts_is_refused(self):
        rows = sound_rows()
        for row in rows:
            if row.get("attempt") == HEAD_ONE and row.get("record") == "step":
                row["end"] = "2026-08-17T11:00:00Z"
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("before it starts", said)

    def test_rows_appended_out_of_time_order_are_refused(self):
        rows = sound_rows()
        rows.append(step(HEAD_ONE, 1, "head", "2026-08-17T11:30:00Z",
                         "2026-08-17T11:31:00Z",
                         "logs/attempt-01/late-head.log"))
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("appended ahead of it", said)

    def test_an_attempt_id_whose_timestamp_postdates_its_rows_is_refused(self):
        # V12's final attempt: an id embedding an instant 2m25s LATER than the
        # attempt's own last row, and 54s later than the evidence commit.
        late = "head-20260817T120225Z-01ghjkmn"
        rows = [row if row.get("attempt") != HEAD_ONE
                else {**row, "attempt": late} for row in sound_rows()]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("LATER than its own first row", said)
        self.assertIn("tolerance 5s", said)

    def test_an_attempt_id_minted_long_before_its_rows_is_refused(self):
        early = "head-20260817T100000Z-01ghjkmn"
        rows = [row if row.get("attempt") != HEAD_ONE
                else {**row, "attempt": early} for row in sound_rows()]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("EARLIER than its own first row", said)

    def test_a_small_lead_between_minting_and_the_first_row_is_allowed(self):
        # The preflight really does sit between the two, and the tolerance
        # exists so a sound run is not refused for taking a second.
        rows = sound_rows()
        for row in rows:
            if row.get("attempt") == HEAD_ONE and row.get("record") == "state":
                row["start"] = "2026-08-17T12:00:03Z"
                row["end"] = "2026-08-17T12:00:03Z"
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)


class AttemptLogs(Fixture):
    """NO ROW NAMES A LOG ROOT THE PACKAGE DOES NOT HAVE."""

    def package(self, rows, roots=()) -> tuple[Path, Path]:
        root = self.temp("package-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        logs.mkdir(parents=True)
        (logs / "order-head.txt").write_text(
            f"PREFLIGHT battery=head\nattempt={HEAD_ONE}\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text(
            f"PREFLIGHT battery=parent\nattempt={PARENT_ONE}\n",
            encoding="utf-8")
        for name in roots:
            (logs / name).mkdir()
        return package, self.ledger(rows, root)

    def staged(self) -> list[dict]:
        """Rows whose transcripts really are staged, so the audit can pass."""
        rows = [row for row in sound_rows() if row.get("record") != "step"]
        return rows

    def test_a_row_naming_a_missing_log_root_is_refused(self):
        # V12: ten rows referenced logs/attempt-03/ and logs/attempt-04/, and
        # the package contained neither.
        rows = self.staged() + [
            step(PACKAGE_ONE, 3, "package", "2026-08-17T12:31:00Z",
                 "2026-08-17T12:32:00Z",
                 "logs/attempt-03/sealer-tests.log"),
        ]
        package, ledger = self.package(rows)
        code, said = self.run_checks("--audit-logs", "--package", package,
                                     "--attempts", ledger, "--attempt",
                                     PACKAGE_ONE, "--attempt-no", "3")
        self.assertEqual(code, 1, said)
        self.assertIn("logs/attempt-03: named by rows this package ships",
                      said)
        self.assertIn("the package contains no such log root", said)

    def test_a_row_that_says_where_its_root_went_is_allowed(self):
        rows = self.staged() + [
            step(PACKAGE_ONE, 3, "package", "2026-08-17T12:31:00Z",
                 "2026-08-17T12:32:00Z",
                 "logs/attempt-03/sealer-tests.log",
                 log_root_elsewhere="this attempt was discarded before the "
                                    "freeze; its transcripts stayed in the "
                                    "build tree and are named in the sidecar"),
        ]
        package, ledger = self.package(rows)
        code, said = self.run_checks("--audit-logs", "--package", package,
                                     "--attempts", ledger, "--attempt",
                                     PACKAGE_ONE, "--attempt-no", "3")
        self.assertNotIn("named by rows this package ships", said)


class Commands(Fixture):
    """AN ELIDED COMMAND IS NOT PRESENTED AS AN EXACT INVOCATION."""

    def test_checks_txt_marks_literal_elided_and_prose_commands(self):
        root = self.temp("checks-txt-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        (logs / "attempt-01").mkdir(parents=True)
        (logs / "attempt-01" / "focused-head.log").write_text(
            "Ran 3 tests in 0.1s\nOK\n", encoding="utf-8")
        (logs / "order-head.txt").write_text(
            "PREFLIGHT battery=head\n"
            "2026-08-17T12:00:00Z\n"
            f"attempt={HEAD_ONE}\n"
            "attempt-no=1\n"
            "lane=V13\n"
            "expect-sha=1111111111111111111111111111111111111111\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "cwd=$REPO\n"
            "log-prefix=01\n"
            "log-root=logs/attempt-01\n"
            "2026-08-17T12:00:05Z\n"
            "START focused-catena\n"
            "ORDER: 1\n"
            "LOG: logs/attempt-01/focused-head.log\n"
            "TREE-BEFORE: clean\n"
            "CMD: python3 -m unittest discover -s tools/tests\n"
            "exit=0\n"
            "TREE-AFTER: clean\n"
            "2026-08-17T12:04:00Z\n"
            "END focused-catena\n"
            "POSTFLIGHT battery=head\n"
            "2026-08-17T12:04:01Z\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "sha-drift=none\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text("", encoding="utf-8")
        rows = [
            lane_row(),
            step(PACKAGE_ONE, 3, "package", "2026-08-17T12:31:00Z",
                 "2026-08-17T12:32:00Z", "logs/attempt-03/seal.log",
                 phase="P2 seal",
                 command="logs/sanitize-and-seal.py PKG --claims claims.json"),
            step(PACKAGE_ONE, 3, "package", "2026-08-17T12:33:00Z",
                 "2026-08-17T12:34:00Z", "(none)", phase="P1 gate",
                 command="the gate comparison did not run: one or both "
                         "reports are absent"),
        ]
        ledger = self.ledger(rows, root)
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3", "--attempts", ledger, "--attempt",
            PACKAGE_ONE)
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("recorded: LITERAL -- the exact string handed to the "
                      "shell", text)
        self.assertIn("recorded: ELIDED -- the capitalised token(s) PKG", text)
        self.assertIn("recorded: PROSE -- a description of what happened",
                      text)
        # The opening claim and the epilogue agree, and the epilogue counts.
        self.assertIn("LITERAL: 1", text)
        self.assertIn("ELIDED: 1", text)
        self.assertIn("PROSE: 1", text)
        self.assertIn("Not recorded in this file, by name", text)
        for phase in ("P6", "P7", "P8"):
            self.assertIn(f"  - {phase} -- ", text)
        # And the battery block states the commit the caller CLAIMED, beside
        # the one the checkout held.
        self.assertIn("expected   : 1111111111111111111111111111111111111111",
                      text)


class Battery(Fixture):
    """THE BATTERY REFUSES A CHECKOUT THAT IS NOT WHAT IT WAS TOLD IT IS."""

    def repo(self) -> tuple[Path, str]:
        """A throwaway git repository. NEVER a clone in this workspace."""
        root = self.temp("battery-repo-")
        repo = root / "clone"
        (repo / "scripts").mkdir(parents=True)
        (repo / "scripts" / "_catena.py").write_text(
            "import pathlib, sys\n"
            "pathlib.Path('leftover-from-a-step.txt').write_text('x')\n"
            "sys.exit(1)\n", encoding="utf-8")
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                   GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                     ["commit", "-qm", "one"]):
            subprocess.run(["git", "-C", str(repo), *args], check=True,
                           env=env, capture_output=True)
        sha = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                             capture_output=True, text=True,
                             check=True).stdout.strip()
        return repo, sha

    def run_battery(self, repo, logs, side="head", expect="", lane=LANE,
                    attempts=None):
        env = dict(os.environ)
        env.pop("ATTEMPT_NO", None)
        if expect:
            env["EXPECT_SHA"] = expect
        else:
            env.pop("EXPECT_SHA", None)
        if lane:
            env["LANE"] = lane
        else:
            env.pop("LANE", None)
        if attempts:
            env["ATTEMPTS"] = str(attempts)
        done = subprocess.run(
            ["bash", str(BATTERY), str(repo), str(logs), side],
            capture_output=True, text=True, env=env)
        return done.returncode, done.stdout + done.stderr

    def test_a_battery_with_no_expected_sha_is_refused(self):
        repo, _sha = self.repo()
        code, said = self.run_battery(repo, repo.parent / "logs", expect="")
        self.assertEqual(code, 1, said)
        self.assertIn("REFUSING: EXPECT_SHA is required", said)
        self.assertIn("A battery measures a NAMED commit", said)

    def test_a_battery_with_no_lane_is_refused(self):
        repo, sha = self.repo()
        code, said = self.run_battery(repo, repo.parent / "logs", expect=sha,
                                      lane="")
        self.assertEqual(code, 1, said)
        self.assertIn("REFUSING: LANE is required", said)

    def test_a_checkout_at_the_wrong_commit_is_refused_terminally(self):
        # THE V12 HOLE: the commit was read and compared to nothing, so a clean
        # checkout at the wrong commit passed preflight and postflight and was
        # labelled by its third argument.
        repo, sha = self.repo()
        logs = repo.parent / "logs"
        attempts = repo.parent / "attempt-ledger.jsonl"
        wrong = "0" * 40
        code, said = self.run_battery(repo, logs, expect=wrong,
                                      attempts=attempts)
        self.assertEqual(code, 1, said)
        self.assertIn("is not at the commit this battery claims to measure",
                      said)
        self.assertIn(f"expected : {wrong}", said)
        self.assertIn(f"found    : {sha}", said)
        # THROUGH discard(): a marker, and a terminal row with a real reason.
        markers = sorted(logs.glob("DISCARDED-*.txt"))
        self.assertEqual(len(markers), 1, sorted(logs.iterdir()))
        rows = [json.loads(one) for one
                in attempts.read_text(encoding="utf-8").splitlines()
                if one.strip()]
        final = [row for row in rows if row.get("record") == "attempt"]
        self.assertEqual(len(final), 1, rows)
        self.assertEqual(final[0]["status"], "failed")
        self.assertIn("not at the commit this battery was told it measures",
                      final[0]["reason"])
        self.assertEqual(final[0]["lane"], LANE)

    def test_a_dirty_postflight_fails_the_battery(self):
        # `set -u` is on and `-e` is not, so a step that leaves the tree dirty
        # -- a failing restore is the real case -- did not abort, and V12 then
        # keyed the failure branch only on SHA drift and wrote status=complete.
        repo, sha = self.repo()
        logs = repo.parent / "logs"
        attempts = repo.parent / "attempt-ledger.jsonl"
        code, said = self.run_battery(repo, logs, expect=sha,
                                      attempts=attempts)
        self.assertEqual(code, 1, said)
        self.assertIn("dirty at postflight", said)
        self.assertTrue((repo / "leftover-from-a-step.txt").is_file(),
                        "the step that dirties the tree did not run")
        rows = [json.loads(one) for one
                in attempts.read_text(encoding="utf-8").splitlines()
                if one.strip()]
        final = [row for row in rows if row.get("record") == "attempt"]
        self.assertEqual(len(final), 1, [row.get("status") for row in rows])
        self.assertEqual(final[0]["status"], "failed")
        self.assertIn("dirty when the battery finished", final[0]["reason"])
        # AND THE ORDINAL WAS SPENT THE MOMENT IT WAS ALLOCATED.
        started = [row for row in rows if row.get("status") == "started"]
        self.assertEqual(len(started), 1, rows)
        self.assertEqual(started[0]["attempt_no"], "1")

    def test_the_battery_refuses_a_ledger_of_another_lane(self):
        repo, sha = self.repo()
        attempts = repo.parent / "attempt-ledger.jsonl"
        attempts.write_text(json.dumps(lane_row("V12"), sort_keys=True) + "\n",
                            encoding="utf-8")
        code, said = self.run_battery(repo, repo.parent / "logs", expect=sha,
                                      attempts=attempts)
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane 'V12', not 'V13'", said)
        self.assertIn("no attempt ordinal was allocated", said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
