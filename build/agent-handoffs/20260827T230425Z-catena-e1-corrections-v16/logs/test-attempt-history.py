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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catena_command as CC  # noqa: E402

HERE = Path(__file__).resolve().parent
CHECKS = HERE / "checks.py"
BATTERY = HERE / "battery.sh"

LANE = "V13"
HEAD_ONE = "head-20260817T120000Z-01ghjkmn"
PARENT_ONE = "parent-20260817T121000Z-02pqrstv"
PACKAGE_ONE = "package-20260817T123000Z-03wxyz23"
# V16: a second battery and a second package attempt, for the abandonment
# refusals -- which need an attempt that started and never terminated.
HEAD_TWO = "head-20260817T170000Z-04abcdef"
HEAD_THREE = "head-20260817T190000Z-06cdefgh"
PACKAGE_TWO = "package-20260817T180000Z-05bcdefg"


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
        # V16: BOTH AXES, NEVER COLLAPSED. Before the axes were separated
        # this line read `set-aside` and the fact that the battery COMPLETED
        # was nowhere on it.
        self.assertIn(f"{HEAD_ONE}: complete | evidence set-aside -- the "
                      f"cohort ran at the parent's tree", said)

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
        self.assertIn(f"{PACKAGE_ONE}: sealed | evidence authoritative",
                      said)

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
        self.assertIn(f"{PACKAGE_ONE}: sealed | evidence superseded", said)

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

    def test_checks_txt_marks_executable_elided_and_prose_commands(self):
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
            "cwd=$CANDIDATE_REPO\n"
            "root=CANDIDATE_REPO the implementation checkout under review\n"
            "root=TOOLS_ANCHOR the handoff-tools checkout\n"
            "log-prefix=01\n"
            "log-root=logs/attempt-01\n"
            "2026-08-17T12:00:05Z\n"
            "START focused-catena\n"
            "ORDER: 1\n"
            "LOG: logs/attempt-01/focused-head.log\n"
            "TREE-BEFORE: clean\n"
            "CMD: python3 -m unittest discover -s tools/tests\n"
            'CMDJSON: {"schema": "catena-exec-command/1", "cwd": '
            '"$CANDIDATE_REPO", "env": {}, "shell": null, "argv": '
            '["python3", "-m", "unittest", "discover", "-s", '
            '"tools/tests"], "uses": []}\n'
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
        # V16, THE V15 REVIEW: `LITERAL` IS GONE AND `EXECUTABLE` REPLACES
        # IT, and the difference is not a rename. `LITERAL` was said about a
        # STRING whose first token prefix-matched a table; V15 shipped seven
        # rows under it that quote `$WORKSPACE` inside single quotes and can
        # never run. `EXECUTABLE` is said only about a validated exec record
        # -- the row below carries one, and the two rows without one are
        # honest about not being re-runnable.
        self.assertIn("recorded: EXECUTABLE -- a validated exec record", text)
        self.assertIn("exec-cwd: $CANDIDATE_REPO", text)
        self.assertIn('exec-argv: ["python3", "-m", "unittest"', text)
        self.assertIn("recorded: ELIDED -- the capitalised token(s) PKG", text)
        self.assertIn("recorded: PROSE -- a description of what happened",
                      text)
        # The opening claim and the epilogue agree, and the epilogue counts.
        self.assertIn("EXECUTABLE: 1", text)
        self.assertIn("ELIDED: 1", text)
        self.assertIn("PROSE: 1", text)
        # THE ROOT TABLE IS RENDERED, ONCE, FROM THE LEDGER'S OWN `root=`
        # LINES. V15 named `$WORKSPACE` and `$REPO` in seven rows and defined
        # neither anywhere in the package.
        self.assertIn("$CANDIDATE_REPO -- the implementation checkout under "
                      "review", text)
        self.assertNotIn("\n  $REPO --", text)
        # And the machine-readable half exists and agrees.
        blob = json.loads(
            (package / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(blob["schema"], "catena-commands/1")
        self.assertEqual(blob["counts"]["executable"], 1)
        self.assertEqual(blob["counts"]["non_executable"], 0)
        self.assertEqual(blob["counts"]["not_replayable_and_says_so"], 2)
        self.assertNotIn("REPO", blob["variables"]["roots"])
        self.assertIn("Not recorded in this file, by name", text)
        for phase in ("P6", "P7", "P8"):
            self.assertIn(f"  - {phase} -- ", text)
        # And the battery block states the commit the caller CLAIMED, beside
        # the one the checkout held.
        self.assertIn("expected   : 1111111111111111111111111111111111111111",
                      text)

    def one_row_package(self, slug: str, cmd: str, record) -> Path:
        """A package whose head battery ran exactly one step, as given.

        `cmd` is the ledger's `CMD:` line -- the string a battery LOGS -- and
        `record` is the `CMDJSON:` line beside it. The two are supplied
        separately on purpose: the whole of F3 is what happens when they
        disagree.
        """
        root = self.temp("command-line-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        (logs / "attempt-01").mkdir(parents=True)
        (logs / "attempt-01" / f"{slug}-head.log").write_text(
            "ok\n", encoding="utf-8")
        (logs / "order-head.txt").write_text(
            "PREFLIGHT battery=head\n"
            "2026-08-17T12:00:00Z\n"
            f"attempt={HEAD_ONE}\n"
            "attempt-no=1\n"
            "lane=V13\n"
            "expect-sha=1111111111111111111111111111111111111111\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "cwd=$CANDIDATE_REPO\n"
            "root=CANDIDATE_REPO the implementation checkout under review\n"
            "root=TOOLS_ANCHOR the handoff-tools checkout\n"
            "log-prefix=01\n"
            "log-root=logs/attempt-01\n"
            "2026-08-17T12:00:05Z\n"
            f"START {slug}\n"
            "ORDER: 1\n"
            f"LOG: logs/attempt-01/{slug}-head.log\n"
            "TREE-BEFORE: clean\n"
            f"CMD: {cmd}\n"
            "CMDJSON: " + json.dumps(record, sort_keys=True) + "\n"
            "exit=0\n"
            "TREE-AFTER: clean\n"
            "2026-08-17T12:04:00Z\n"
            f"END {slug}\n"
            "POSTFLIGHT battery=head\n"
            "2026-08-17T12:04:01Z\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "sha-drift=none\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text("", encoding="utf-8")
        return package

    def test_the_command_line_is_rendered_from_the_record(self):
        """V16, THE COMMAND-REPLAY LANE, F3, ON THE ROW IT WAS FOUND ON.

        `battery.sh`'s `run()` logs `CMD: $cmd` for a shell-form step, and
        `$cmd` carries no environment prefix -- the environment lives in the
        record. So both shipped `browser-gate` rows carried a `command :`
        line WITHOUT the `TRIPTYCH_CHROME=...` assignment their own record
        holds, under two comments claiming the line was rendered from the
        record and "cannot disagree" with it. The line is rendered now.
        """
        record = CC.make_record(
            "$CANDIDATE_REPO",
            shell='node tools/tests/gate.mjs; gate=$?; '
                  'python3 "$TOOLS_ANCHOR/gate-summary.py"; exit $gate',
            env={"TRIPTYCH_CHROME": "/usr/bin/chromium"})
        package = self.one_row_package("browser-gate", record["shell"], record)
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3")
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("    command : TRIPTYCH_CHROME=/usr/bin/chromium node "
                      "tools/tests/gate.mjs", text)
        # AND THE MACHINE-READABLE HALF CARRIES THE SAME STRING, because both
        # come from one `render_shell` call rather than from two writers.
        blob = json.loads(
            (package / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(blob["commands"][0]["command"],
                         CC.render_shell(record))

    def test_a_logged_command_that_contradicts_its_record_is_refused(self):
        """THE MATCHED NEGATIVE, and the gate that was missing entirely.

        A ledger whose human half names one tool and whose machine half names
        another is a row that tells two stories. Neither can be checked
        against the other, and rendering one of them would be choosing which
        to believe, so the composition refuses and writes nothing.
        """
        record = CC.make_record(
            "$CANDIDATE_REPO",
            argv=["python3", "$TOOLS_ANCHOR/gzip-sizes.py", "src"])
        package = self.one_row_package(
            "gzip-sizes", "python3 tools/some-other-tool.py src", record)
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3")
        self.assertEqual(code, 1, said)
        self.assertIn("REFUSING: gzip-sizes:", said)
        self.assertIn("describe different commands", said)
        self.assertIn("some-other-tool.py", said)
        self.assertFalse((package / "checks.txt").exists())
        self.assertFalse((package / "commands.json").exists())

    def test_the_roots_a_row_uses_are_derived_not_read_from_the_ledger(self):
        """V16, THE COMMAND-REPLAY LANE, F4, WHERE A REVIEWER MEETS IT.

        The ledger line below says `"uses": []` -- which is what all 23
        recorded rows say -- about a command that references two roots. The
        composed member must state the two, because they are a function of
        the record beside them and this file derives every figure it prints.
        """
        root = self.temp("checks-uses-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        (logs / "attempt-01").mkdir(parents=True)
        (logs / "attempt-01" / "gzip-head.log").write_text("ok\n",
                                                           encoding="utf-8")
        (logs / "order-head.txt").write_text(
            "PREFLIGHT battery=head\n"
            "2026-08-17T12:00:00Z\n"
            f"attempt={HEAD_ONE}\n"
            "attempt-no=1\n"
            "lane=V13\n"
            "expect-sha=1111111111111111111111111111111111111111\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "cwd=$CANDIDATE_REPO\n"
            "root=CANDIDATE_REPO the implementation checkout under review\n"
            "root=TOOLS_ANCHOR the handoff-tools checkout\n"
            "log-prefix=01\n"
            "log-root=logs/attempt-01\n"
            "2026-08-17T12:00:05Z\n"
            "START gzip-sizes\n"
            "ORDER: 1\n"
            "LOG: logs/attempt-01/gzip-head.log\n"
            "TREE-BEFORE: clean\n"
            'CMD: python3 "$TOOLS_ANCHOR/gzip-sizes.py" src\n'
            'CMDJSON: {"schema": "catena-exec-command/1", "cwd": '
            '"$CANDIDATE_REPO", "env": {}, "shell": null, "argv": '
            '["python3", "$TOOLS_ANCHOR/gzip-sizes.py", "src"], '
            '"uses": []}\n'
            "exit=0\n"
            "TREE-AFTER: clean\n"
            "2026-08-17T12:04:00Z\n"
            "END gzip-sizes\n"
            "POSTFLIGHT battery=head\n"
            "2026-08-17T12:04:01Z\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "sha-drift=none\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text("", encoding="utf-8")
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3")
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("exec-uses: $CANDIDATE_REPO, $TOOLS_ANCHOR", text)
        blob = json.loads(
            (package / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(blob["commands"][0]["exec"]["uses"],
                         ["CANDIDATE_REPO", "TOOLS_ANCHOR"])


# ---------------------------------------------------------------------------
# V16, THE COMMAND-REPLAY LANE, F0: THE ROOT NO BATTERY CAN DECLARE.
#
# The lane replayed all 23 recorded battery rows from fresh clones and found
# the package would never assemble: `assemble.sh`'s one exec-bearing
# package-phase row binds `cwd: "$PACKAGE_ROOT"`, `checks.py` built its root
# table only from the two battery ledgers' `root=` lines, and a battery cannot
# name a directory that does not exist while it runs. The row classified
# NON-EXECUTABLE `[undefined-variable]` and `checks.py` returned 1 at P5.
# Never caught because the package had never been assembled end to end.
class PackagePhaseCommands(Fixture):
    """A PACKAGE-PHASE ROW RUNS INSIDE THE PACKAGE, AND SAYS SO."""

    HEAD_LEDGER = (
        "PREFLIGHT battery=head\n"
        "2026-08-17T12:00:00Z\n"
        f"attempt={HEAD_ONE}\n"
        "attempt-no=1\n"
        "lane=V13\n"
        "expect-sha=1111111111111111111111111111111111111111\n"
        "sha=1111111111111111111111111111111111111111\n"
        "porcelain=clean\n"
        "cwd=$CANDIDATE_REPO\n"
        "root=CANDIDATE_REPO the implementation checkout under review\n"
        "root=TOOLS_ANCHOR the handoff-tools checkout\n"
        "log-prefix=01\n"
        "log-root=logs/attempt-01\n"
        "POSTFLIGHT battery=head\n"
        "2026-08-17T12:04:01Z\n"
        "sha=1111111111111111111111111111111111111111\n"
        "porcelain=clean\n"
        "sha-drift=none\n")

    def compose(self, pipeline: list[dict]) -> tuple[int, str, Path]:
        """Compose `checks.txt` over a package whose pipeline rows are given.

        The battery ledger declares CANDIDATE_REPO and TOOLS_ANCHOR and
        nothing else, exactly as `battery.sh` does for the two roots a
        package-phase row never uses -- so PACKAGE_ROOT and EVIDENCE_ROOT are
        both absent from the ledgers and the two tests below differ only in
        which of them the row names.
        """
        root = self.temp("package-phase-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        logs.mkdir(parents=True)
        (logs / "order-head.txt").write_text(self.HEAD_LEDGER,
                                             encoding="utf-8")
        (logs / "order-parent.txt").write_text("", encoding="utf-8")
        ledger = self.ledger([lane_row(), *pipeline], root)
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3", "--attempts", ledger, "--attempt",
            PACKAGE_ONE)
        return code, said, package

    def gate_row(self, record: dict) -> dict:
        return step(
            PACKAGE_ONE, 3, "package", "2026-08-17T12:31:00Z",
            "2026-08-17T12:32:00Z", "logs/attempt-03/gate-comparison.log",
            phase="P1 gate", cwd="$PACKAGE_ROOT",
            command=CC.render_shell(record),
            exec_record=json.dumps(record, sort_keys=True))

    def test_a_package_phase_row_bound_to_the_package_root_is_executable(self):
        """THE ROW THE ASSEMBLY ACTUALLY WRITES, AND IT MUST NOT REFUSE.

        Without the fallback merged into the root table this row classifies
        NON-EXECUTABLE, `checks.py` prints `REFUSING: package/P1 gate` and
        returns 1, and the pipeline stops at P5.
        """
        record = CC.make_record(
            "$PACKAGE_ROOT",
            argv=["python3", "logs/compare-gate.py",
                  "logs/attempt-01/browser-gate-parent.json",
                  "logs/attempt-01/browser-gate-head.json"])
        code, said, package = self.compose([self.gate_row(record)])
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("exec-cwd: $PACKAGE_ROOT", text)
        self.assertIn("recorded: EXECUTABLE -- a validated exec record", text)
        # AND THE ROOT TABLE THE PACKAGE SHIPS DEFINES IT, so a reviewer can
        # bind it and `replay-command.py --check` accepts the row too.
        blob = json.loads(
            (package / "commands.json").read_text(encoding="utf-8"))
        self.assertIn("PACKAGE_ROOT", blob["variables"]["roots"])
        self.assertEqual(blob["counts"]["non_executable"], 0)
        self.assertIn("$PACKAGE_ROOT -- the package directory itself", text)

    def bare_row(self, phase: str, command: str, order: str) -> dict:
        """A package-phase row with NO exec record, as most of them are."""
        return step(PACKAGE_ONE, 3, "package", "2026-08-17T12:35:00Z",
                    "2026-08-17T12:36:00Z", "(none)", phase=phase,
                    order=order, command=command)

    def test_the_package_states_how_much_of_itself_it_records(self):
        """V16, THE COMMAND-REPLAY LANE, F5, DISCLOSED RATHER THAN IMPLIED.

        `assemble.sh` sets `STEP_EXEC` on one of its ~20 package-phase steps.
        Every other package row is ELIDED or PROSE, which is honest one row
        at a time -- but a single EXECUTABLE headline across every row could
        be read as a claim about the whole pipeline, and it is not one. The
        figures below are COUNTED off the rows, so they cannot drift from
        them.
        """
        record = CC.make_record(
            "$PACKAGE_ROOT",
            argv=["python3", "logs/compare-gate.py",
                  "logs/attempt-01/browser-gate-parent.json",
                  "logs/attempt-01/browser-gate-head.json"])
        code, said, package = self.compose([
            self.gate_row(record),
            self.bare_row("P2 seal",
                          "logs/sanitize-and-seal.py PKG --claims claims.json",
                          "2"),
            self.bare_row("P7 archive",
                          "zip the package with constant entry metadata, then "
                          "write the manifest.", "3"),
        ])
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("- package: 3 row(s), 1 with an exec record, "
                      "1 EXECUTABLE", text)
        self.assertIn("MOST OF THIS PIPELINE'S OWN STEPS CARRY NO EXEC "
                      "RECORD. 1 of the 3 package-phase rows", text)
        self.assertIn("2 do not", text)
        # AND MACHINE-READABLY, so the figure can be checked without prose.
        blob = json.loads(
            (package / "commands.json").read_text(encoding="utf-8"))
        self.assertEqual(blob["coverage"]["package"],
                         {"rows": 3, "with_record": 1, "executable": 1})

    def test_a_fully_recorded_pipeline_makes_no_such_disclosure(self):
        """THE MATCHED NEGATIVE. The sentence is earned by the count.

        Give every package row a record and the admission disappears,
        because it is emitted from the figures rather than kept in the file
        against the day it becomes true again.
        """
        record = CC.make_record(
            "$PACKAGE_ROOT", argv=["python3", "logs/compare-gate.py", "a", "b"])
        code, said, package = self.compose([self.gate_row(record)])
        self.assertEqual(code, 0, said)
        text = (package / "checks.txt").read_text(encoding="utf-8")
        self.assertIn("- package: 1 row(s), 1 with an exec record, "
                      "1 EXECUTABLE", text)
        self.assertNotIn("CARRY NO EXEC RECORD", text)

    def test_a_row_using_a_root_nothing_defines_is_still_refused(self):
        """THE MATCHED NEGATIVE, and the reason the fix is a fallback TABLE
        rather than a relaxed test.

        `EVIDENCE_ROOT` is a known root name that this package's batteries
        never declared and no fallback supplies. The row must still be
        refused, or the undefined-variable check has been traded away to buy
        the row above.
        """
        record = CC.make_record(
            "$PACKAGE_ROOT",
            argv=["python3", "logs/compare-gate.py",
                  "$EVIDENCE_ROOT/browser-gate-head.json"])
        code, said, package = self.compose([self.gate_row(record)])
        self.assertEqual(code, 1, said)
        self.assertIn("REFUSING", said)
        self.assertIn("$EVIDENCE_ROOT", said)
        self.assertIn("no ledger `root=` line defines it", said)
        self.assertFalse((package / "checks.txt").exists(),
                         "a refused composition must not write the member")
        # AND THE CLASSIFIER ITSELF, ASKED DIRECTLY with the set this package
        # defines: the undefined-variable test still refuses the row, which is
        # the thing the PACKAGE_ROOT fallback must not have bought.
        verdict, why = CC.classify(
            CC.render_shell(record), record,
            defined={"CANDIDATE_REPO", "TOOLS_ANCHOR", "PACKAGE_ROOT"})
        self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)
        self.assertIn("undefined-variable", why)
        self.assertIn("EVIDENCE_ROOT", why)


# ---------------------------------------------------------------------------
# V16, THE COMMAND-REPLAY LANE, F2: A ROW IS NOT NECESSARILY REPLAYABLE ALONE.
#
# The lane replayed `browser-gate` from a fresh clone exactly as `checks.txt`
# instructed and got exit 3, not the recorded 1: `corpus_browser_gate: no
# built artifact at <clone>/build/public-alpha/site`. The row consumes what
# `public-site` (ORDER 7) builds, and neither the record nor the replay
# instructions said so. With `public-site` replayed first it reproduces
# byte-identically. A reviewer following the instructions must not get exit 3
# and conclude the evidence is broken.
class OrderedReplay(Fixture):
    """THE ORDER IS RENDERED, AND IT IS RENDERED FROM THE ROWS."""

    def package_of(self, steps: list[tuple[int, str]]) -> Path:
        root = self.temp("ordered-replay-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        (logs / "attempt-01").mkdir(parents=True)
        body = ""
        for order, slug in steps:
            (logs / "attempt-01" / f"{slug}-head.log").write_text(
                "ok\n", encoding="utf-8")
            record = CC.make_record("$CANDIDATE_REPO",
                                    argv=["make", slug])
            body += (
                "2026-08-17T12:00:05Z\n"
                f"START {slug}\n"
                f"ORDER: {order}\n"
                f"LOG: logs/attempt-01/{slug}-head.log\n"
                "TREE-BEFORE: clean\n"
                f"CMD: {CC.render_shell(record)}\n"
                "CMDJSON: " + json.dumps(record, sort_keys=True) + "\n"
                "exit=0\n"
                "TREE-AFTER: clean\n"
                "2026-08-17T12:04:00Z\n"
                f"END {slug}\n")
        (logs / "order-head.txt").write_text(
            "PREFLIGHT battery=head\n"
            "2026-08-17T12:00:00Z\n"
            f"attempt={HEAD_ONE}\n"
            "attempt-no=1\n"
            "lane=V13\n"
            "expect-sha=1111111111111111111111111111111111111111\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "cwd=$CANDIDATE_REPO\n"
            "root=CANDIDATE_REPO the implementation checkout under review\n"
            "log-prefix=01\n"
            "log-root=logs/attempt-01\n"
            + body +
            "POSTFLIGHT battery=head\n"
            "2026-08-17T12:04:01Z\n"
            "sha=1111111111111111111111111111111111111111\n"
            "porcelain=clean\n"
            "sha-drift=none\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text("", encoding="utf-8")
        return package

    def compose(self, steps) -> str:
        package = self.package_of(steps)
        code, said = self.run_checks(
            "--package", package, "--head", "1" * 40, "--parent", "2" * 40,
            "--attempt-no", "3")
        self.assertEqual(code, 0, said)
        return (package / "checks.txt").read_text(encoding="utf-8")

    def test_the_recorded_order_is_rendered_and_the_prerequisite_named(self):
        """THE POSITIVE. The sequence, and the pair that needs it."""
        text = self.compose([(7, "public-site"), (8, "browser-gate")])
        self.assertIn("REPLAY A SIDE IN ITS RECORDED ORDER", text)
        self.assertIn("     7  public-site", text)
        self.assertIn("     8  browser-gate", text)
        self.assertIn("-- head/browser-gate reads the site", text)
        self.assertIn("build/public-alpha/site", text)
        # The order comes from the ledger, so the listing is sorted by ORDER
        # rather than by the order the rows happen to appear.
        self.assertLess(text.index("     7  public-site"),
                        text.index("     8  browser-gate"))

    def test_the_prerequisite_note_does_not_outlive_the_rows(self):
        """THE MATCHED NEGATIVE, and it is the one that keeps this derived.

        A battery with no `public-site` row must not carry a sentence about
        one. The warning is emitted from the rows present, not typed beside
        them, which is the difference between a derived member and a member
        that says what it said last time.
        """
        text = self.compose([(1, "catena-check"), (8, "browser-gate")])
        self.assertIn("REPLAY A SIDE IN ITS RECORDED ORDER", text)
        self.assertIn("     8  browser-gate", text)
        self.assertNotIn("public-alpha", text)
        self.assertNotIn("reads the site", text)


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



# ---------------------------------------------------------------------------
# V16, THE V15 REVIEW: THE CLASSIFIER PARSES, IT DOES NOT TRUST.
#
# The review's finding, in its own words: "`checks.txt` calls all 24 command
# rows `LITERAL`, but seven load-bearing rows contain single-quoted
# `'$WORKSPACE/...'` or `'$REPO/...'` paths. Those anchors cannot expand and
# no assignments are supplied. ... prefix matching accepts prose such as
# `format`, `installing` and `zipcode`, and the handoff checker trusts the
# precomputed `LITERAL` label."
#
# ONE POSITIVE AND ONE MATCHED NEGATIVE PER CHECK, which is the V15 pattern.
# Each negative here is a real V15 string or the review's own example, not an
# invented one.
class CommandClassifier(unittest.TestCase):
    """Every refusal `catena_command` can raise, exercised both ways."""

    # ---- quoted anchors: the seven rows V15 shipped -----------------------

    #: The seven V15 rows, verbatim from
    #: db5f651e:build/agent-handoffs/20260826T195656Z-catena-e1-corrections-v15/checks.txt
    #: at lines 153, 168, 183, 198, 341, 371 and 386.
    V15_UNEXPANDABLE = (
        ("parent browser-gate",
         "TRIPTYCH_CHROME='/usr/bin/chromium' node "
         "tools/tests/corpus_browser_gate.mjs --json-out "
         "'$WORKSPACE/spincyc/v15-package-src/logs/attempt-01/"
         "browser-gate-parent.json' > /dev/null; gate=$?; python3 "
         "'$WORKSPACE/spincyc/v15-handoff-tools/gate-summary.py' "
         "'$WORKSPACE/spincyc/v15-package-src/logs/attempt-01/"
         "browser-gate-parent.json'; exit $gate"),
        ("parent gzip-sizes",
         "python3 '$WORKSPACE/spincyc/v15-handoff-tools/gzip-sizes.py' "
         "src/web/browser/catena"),
        ("parent head-tests-against-parent",
         "cp '$REPO/tools/tests/test_catena_wave_1.py' "
         "tools/tests/test_catena_wave_1.py && python3 -m unittest discover "
         "-s tools/tests -p 'test_catena_wave_1.py' -v"),
        ("parent request-journals",
         "python3 '$WORKSPACE/spincyc/v15-handoff-tools/journal-dump.py' "
         "tools/tests/test_catena_wave_1.py"),
        ("head browser-gate",
         "TRIPTYCH_CHROME='/usr/bin/chromium' node "
         "tools/tests/corpus_browser_gate.mjs --json-out "
         "'$WORKSPACE/spincyc/v15-package-src/logs/attempt-02/"
         "browser-gate-head.json' > /dev/null; gate=$?; exit $gate"),
        ("head gzip-sizes",
         "python3 '$WORKSPACE/spincyc/v15-handoff-tools/gzip-sizes.py' "
         "src/web/browser/catena"),
        ("head request-journals",
         "python3 '$WORKSPACE/spincyc/v15-handoff-tools/journal-dump.py' "
         "tools/tests/test_catena_wave_1.py"),
    )

    def test_every_v15_row_that_shipped_literal_is_refused_now(self):
        """THE NEGATIVE, CALIBRATED AGAINST THE REAL V15 PACKAGE.

        V15's classifier answered `LITERAL -- the exact string handed to the
        shell` for every one of these. Each one quotes a `$`-anchor inside
        SINGLE quotes, so the shell passes the dollar sign through and the
        command names a path that cannot exist.
        """
        for name, text in self.V15_UNEXPANDABLE:
            with self.subTest(row=name):
                verdict, why = CC.classify(text)
                self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)
                self.assertIn("quoted-variable", why)
                trapped = CC.unexpandable_variables(text)
                self.assertTrue(trapped, "the anchor is inside single quotes")

    def test_the_repaired_row_is_executable(self):
        """THE MATCHED POSITIVE. Double quotes, and the row runs."""
        record = CC.make_record(
            "$CANDIDATE_REPO",
            argv=["python3", "$TOOLS_ANCHOR/gzip-sizes.py",
                  "src/web/browser/catena"])
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)
        self.assertEqual(
            CC.render_shell(record),
            'python3 "$TOOLS_ANCHOR/gzip-sizes.py" src/web/browser/catena')
        self.assertEqual(
            CC.unexpandable_variables(CC.render_shell(record)), [])

    # ---- $REPO overloading ------------------------------------------------

    def test_the_overloaded_v15_names_are_reserved(self):
        """`$REPO` named two directories in one V15 row; it is refused."""
        for name in ("REPO", "WORKSPACE", "EVIDENCE", "SCRATCH"):
            with self.subTest(name=name):
                with self.assertRaises(CC.ExecProblem) as caught:
                    CC.make_variables(**{name: "anything"})
                self.assertEqual(caught.exception.code, "reserved-variable")
                with self.assertRaises(CC.ExecProblem) as caught:
                    CC.check_variables({"schema": CC.VARIABLES_SCHEMA,
                                        "roots": {name: "anything"}})
                self.assertEqual(caught.exception.code, "reserved-variable")

    def test_the_parent_replay_row_names_two_distinct_roots(self):
        """THE POSITIVE for the row `$REPO` overloading made unrecoverable.

        The cwd is the PARENT checkout; the test file comes from the
        CANDIDATE checkout. Two names, two bindings, and the replay resolves
        each to its own directory.
        """
        record = CC.make_record(
            "$PARENT_REPO",
            shell='cp "$CANDIDATE_REPO/tools/tests/test_catena_wave_1.py" '
                  "tools/tests/test_catena_wave_1.py && python3 -m unittest "
                  "discover -s tools/tests -p 'test_catena_wave_1.py' -v")
        verdict, _ = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE)
        cwd, _env, form = CC.resolve(
            record, {"PARENT_REPO": "/parent", "CANDIDATE_REPO": "/candidate"})
        self.assertEqual(cwd, "/parent")
        self.assertIn("/candidate/tools/tests/test_catena_wave_1.py", form)
        self.assertNotIn("/parent/tools/tests/test_catena_wave_1.py", form)

    def test_a_root_the_record_does_not_define_is_refused(self):
        with self.assertRaises(CC.ExecProblem) as caught:
            CC.validate({"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                         "argv": ["python3", "$PARENT_REPO/x.py"]},
                        defined={"CANDIDATE_REPO"})
        self.assertEqual(caught.exception.code, "undefined-variable")

    # ---- prose prefix -----------------------------------------------------

    def test_prose_that_begins_with_a_command_word_is_prose(self):
        """The review's own two examples, plus the family they belong to."""
        for text in ("python3 would be run here to check the tree",
                     "cp is used to place the head test file",
                     "make will be invoked by the operator",
                     "git was run against the parent checkout",
                     "node has already produced the report"):
            with self.subTest(text=text):
                verdict, why = CC.classify(text)
                self.assertEqual(verdict, CC.VERDICT_PROSE, why)
                record = {"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                          "shell": text}
                verdict, why = CC.classify(None, record,
                                           defined=set(CC.ROOT_VARS))
                self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)
                self.assertIn("prose-prefix", why)

    def test_a_real_invocation_beginning_with_the_same_word_is_not_prose(self):
        """THE MATCHED POSITIVE, so the prose test is not a word blacklist."""
        for text in ("python3 -m unittest discover -s tools/tests",
                     "cp a.py b.py",
                     "make -k check",
                     "git status --porcelain",
                     "node tools/tests/corpus_browser_gate.mjs"):
            with self.subTest(text=text):
                prose, why = CC.looks_like_prose(text)
                self.assertFalse(prose, why)

    # ---- prefix overmatch -------------------------------------------------

    def test_prefix_overmatch_is_closed(self):
        """`format`, `installing`, `zipcode` -- the review's three findings.

        V15 tested `first.startswith(COMMAND_HEADS)`, so each of these was a
        command. The test is exact membership now.
        """
        for token in ("format", "installing", "zipcode", "testify", "iffy",
                      "forward", "envelope", "setting", "catalogue",
                      "nodemon", "printfriendly", "shell", "makefile"):
            with self.subTest(token=token):
                self.assertFalse(CC.is_command_head(token))
        # And the heads themselves, plus the path-shaped ones, still pass.
        for token in ("python3", "cp", "make", "git", "zip", "install", "for",
                      "tools/tpt", "./run.sh", "scripts/_catena.py"):
            with self.subTest(token=token):
                self.assertTrue(CC.is_command_head(token))

    # ---- the remaining refusal codes --------------------------------------

    def test_a_missing_command_head_is_refused(self):
        verdict, why = CC.classify(
            None, {"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                   "argv": ["zipcode", "90210"]},
            defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE)
        self.assertIn("no-command-head", why)

    def test_malformed_argv_is_refused(self):
        for argv in ([], ["python3", ""], ["python3", 3], "python3 x"):
            with self.subTest(argv=argv):
                verdict, why = CC.classify(
                    None, {"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                           "argv": argv}, defined=set(CC.ROOT_VARS))
                self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)

    def test_a_row_with_both_argv_and_shell_is_refused(self):
        verdict, why = CC.classify(
            None, {"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                   "argv": ["python3", "x.py"], "shell": "python3 x.py"},
            defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE)
        self.assertIn("argv-and-shell", why)

    def test_a_row_with_no_cwd_is_refused(self):
        """THE AMBIGUOUS-CWD CASE V15'S TESTS DID NOT EXERCISE.

        `python3 logs/compare-gate.py logs/a.json logs/b.json` is three
        relative paths and nothing saying what they are relative to. V15
        shipped exactly that row with no `cwd :` slot at all.
        """
        for cwd in (None, "", "$REPO", "/absolute/path", "$CANDIDATE_REPO/x"):
            with self.subTest(cwd=cwd):
                verdict, why = CC.classify(
                    None, {"schema": CC.SCHEMA, "cwd": cwd,
                           "argv": ["python3", "logs/compare-gate.py"]},
                    defined=set(CC.ROOT_VARS))
                self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)

    def test_the_package_comparison_row_with_its_cwd_is_executable(self):
        """THE MATCHED POSITIVE for the row above."""
        record = CC.make_record(
            "$PACKAGE_ROOT",
            argv=["python3", "logs/compare-gate.py",
                  "logs/attempt-01/browser-gate-parent.json",
                  "logs/attempt-02/browser-gate-head.json"])
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)

    def test_uppercase_quoted_data_is_not_an_elision(self):
        """THE CASE V15'S TESTS DID NOT EXERCISE, per the review.

        A capital word inside quoted DATA -- an acronym in a note, a pattern
        -- is not a value the lane elided. It is also not a reason to call a
        row executable. Both halves are asserted.
        """
        text = ("node gate.mjs; echo 'report written: the gate prints the "
                "same JSON report to stdout'")
        verdict, why = CC.classify(text)
        self.assertEqual(verdict, CC.VERDICT_ELIDED, why)
        self.assertIn("JSON", why)
        # With a record, the same string is executable, and the acronym in
        # the note changes nothing -- because the verdict no longer turns on
        # scanning the string for capitals.
        record = CC.make_record("$CANDIDATE_REPO", shell=text)
        verdict, why = CC.classify(text, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)

    def test_a_plausible_string_without_a_record_is_never_executable(self):
        """THE STRUCTURAL RULE. A string cannot earn `EXECUTABLE`.

        This is the whole difference from V15: the label describes a
        structure that carries a cwd and an environment, so no amount of
        looking at a string can produce it.
        """
        verdict, why = CC.classify("make -k check")
        self.assertEqual(verdict, CC.VERDICT_ELIDED, why)
        self.assertNotEqual(verdict, CC.VERDICT_EXECUTABLE)

    def test_the_local_shell_variable_is_not_an_undefined_root(self):
        """`gate=$?` then `exit $gate` is a shell local, not a root."""
        record = CC.make_record(
            "$CANDIDATE_REPO",
            shell="node gate.mjs; gate=$?; echo done; exit $gate")
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)

    def test_an_unbound_root_refuses_a_replay_rather_than_running_it(self):
        """THE NON-VACUITY GUARD. An empty substitution runs the wrong thing.

        Substituting nothing for `$CANDIDATE_REPO` would run the command in
        whatever directory the replay started in and report its exit as the
        row's. That is a replay that proves nothing, so it refuses.
        """
        record = CC.make_record("$CANDIDATE_REPO",
                                argv=["python3", "$TOOLS_ANCHOR/x.py"])
        with self.assertRaises(CC.ExecProblem) as caught:
            CC.resolve(record, {"CANDIDATE_REPO": "/candidate"})
        self.assertEqual(caught.exception.code, "unbound-root")
        self.assertIn("TOOLS_ANCHOR", caught.exception.message)
        # THE MATCHED POSITIVE: bound, and it resolves.
        cwd, _env, argv = CC.resolve(
            record, {"CANDIDATE_REPO": "/candidate", "TOOLS_ANCHOR": "/tools"})
        self.assertEqual(cwd, "/candidate")
        self.assertEqual(argv, ["python3", "/tools/x.py"])

    def test_the_slash_and_equals_escape_hatches_are_closed(self):
        """TWO LEAKS THE V15 REVIEW DID NOT NAME.

        V15's whole test was
            `first.startswith(COMMAND_HEADS) or "/" in first or "=" in first`
        so ANY prose whose first token merely contained a slash or an equals
        sign classified as re-runnable. The `=` disjunct was ADDED in V15,
        for `TRIPTYCH_CHROME='...'`, with zero coverage.
        """
        for text in ("a/b was not measured",
                     "src/web/browser was not rebuilt",
                     "x=y was not measured",
                     "NOTES=this is a note about what ran",
                     "half/of the steps were skipped"):
            with self.subTest(text=text):
                verdict, why = CC.classify(text)
                self.assertEqual(verdict, CC.VERDICT_PROSE, why)

    def test_a_real_assignment_prefix_is_still_a_command(self):
        """THE MATCHED POSITIVE. The `=` disjunct existed for a reason and
        the reason survives: an environment assignment in front of a real
        head is a command, and the head test looks past it."""
        self.assertEqual(
            CC.head_of("TRIPTYCH_CHROME=/usr/bin/chromium node gate.mjs"),
            "node")
        record = CC.make_record(
            "$CANDIDATE_REPO", argv=["node", "tools/tests/gate.mjs"],
            env={"TRIPTYCH_CHROME": "/usr/bin/chromium"})
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)
        self.assertEqual(
            CC.render_shell(record),
            "TRIPTYCH_CHROME=/usr/bin/chromium node tools/tests/gate.mjs")

    def test_the_fourth_verdict_is_reachable(self):
        """`NOT RECORDED` had no fixture in V15's one classifier test."""
        for text in (None, "", "   ", "\n\t "):
            with self.subTest(text=repr(text)):
                verdict, why = CC.classify(text)
                self.assertEqual(verdict, CC.VERDICT_NOT_RECORDED, why)
                self.assertIn("nothing to re-run", why)

    def test_the_verdict_is_the_same_off_host(self):
        """THE BYTE-STABILITY PROPERTY V15 ARGUED FOR AND NEVER TESTED.

        `checks.txt` is a shipped member and a reviewer re-composing it on
        another machine must get the same bytes. The classifier therefore
        probes nothing: no PATH, no filesystem, no clock, no environment.
        This asserts that directly -- an empty PATH, an empty environment and
        a different working directory change no verdict.
        """
        samples = [
            "python3 -m unittest discover -s tools/tests",
            "make -k check",
            "cp a.py b.py && python3 -m unittest",
            "python3 '$WORKSPACE/tools/x.py' src",
            "python3 would be run here to check the tree",
            "logs/sanitize-and-seal.py PKG --claims claims.json",
            "",
        ]
        before = [CC.classify(one) for one in samples]
        saved_env = dict(os.environ)
        saved_cwd = os.getcwd()
        try:
            os.environ.clear()
            os.environ["PATH"] = ""
            os.chdir(tempfile.gettempdir())
            after = [CC.classify(one) for one in samples]
        finally:
            os.environ.clear()
            os.environ.update(saved_env)
            os.chdir(saved_cwd)
        self.assertEqual(before, after,
                         "a verdict that moves with the host makes checks.txt "
                         "un-recomposable, which is the property the fixed "
                         "head tuple exists to guarantee")
        # AND THE TABLES THEMSELVES ARE LITERALS, not derived at import.
        self.assertIsInstance(CC.COMMAND_HEADS, tuple)
        self.assertIsInstance(CC.PATH_HEAD_PREFIXES, tuple)
        self.assertNotIn("", CC.COMMAND_HEADS)

    def test_a_compound_command_is_classified_whole(self):
        """Eight of V15's twenty-four rows carry `&&`, `;` or a pipeline and
        none had a fixture."""
        record = CC.make_record(
            "$PARENT_REPO",
            shell='git checkout -- tools/tests/x.py; echo "restored"; '
                  'git status --porcelain; '
                  'echo "entries: $(git status --porcelain | wc -l)"')
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE, why)
        # The same command with one anchor mis-quoted is refused.
        broken = dict(record)
        broken["shell"] = ("cp '$CANDIDATE_REPO/tools/tests/x.py' x.py; "
                           "echo done")
        verdict, why = CC.classify(None, broken, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)
        self.assertIn("quoted-variable", why)

    def test_the_quote_lexer_reads_the_three_states(self):
        """The whole of the V15 defect, as a table."""
        cases = (
            ("'$A'", "single"),
            ('"$A"', "double"),
            ("$A", "bare"),
            ("'a'$A'b'", "bare"),
            ('"a\'$A\'b"', "double"),
            ("\\'$A", "bare"),
        )
        for text, want in cases:
            with self.subTest(text=text):
                found = CC.quote_state_scan(text)
                self.assertEqual([one[2] for one in found], [want], text)

    # ---- `uses`: derived, not empty, and not taken on trust ---------------
    #
    # V16, THE COMMAND-REPLAY LANE, F4: `make_record` threw away
    # `validate()`'s return value -- the sorted list of roots the command
    # references -- so `uses` shipped as `[]` on all 23 recorded rows,
    # including rows that use three roots apiece.

    def test_make_record_derives_the_roots_the_command_uses(self):
        """THE POSITIVE. Three roots referenced, three roots recorded."""
        record = CC.make_record(
            "$CANDIDATE_REPO",
            shell='node tools/tests/gate.mjs --json-out '
                  '"$EVIDENCE_ROOT/gate.json"; gate=$?; '
                  'python3 "$TOOLS_ANCHOR/gate-summary.py"; exit $gate')
        self.assertEqual(record["uses"],
                         ["CANDIDATE_REPO", "EVIDENCE_ROOT", "TOOLS_ANCHOR"])
        # The row's own shell local is NOT a root and is not in the list.
        self.assertNotIn("gate", record["uses"])
        # An argv row, and its cwd counts: it is a root the replay must bind.
        argv = CC.make_record("$PARENT_REPO",
                              argv=["python3", "$TOOLS_ANCHOR/gzip-sizes.py"])
        self.assertEqual(argv["uses"], ["PARENT_REPO", "TOOLS_ANCHOR"])

    def test_a_record_that_misdeclares_what_it_uses_is_refused(self):
        """THE MATCHED NEGATIVE. A claim that disagrees with the record.

        `uses` is derivable from the record, so a stated one is a claim, and
        an unchecked claim about a command is the whole of the V15 defect.
        """
        record = CC.make_record("$PARENT_REPO",
                                argv=["python3", "$TOOLS_ANCHOR/x.py"])
        record["uses"] = ["PARENT_REPO"]
        with self.assertRaises(CC.ExecProblem) as caught:
            CC.validate(record, defined=set(CC.ROOT_VARS))
        self.assertEqual(caught.exception.code, "misdeclared-uses")
        self.assertIn("TOOLS_ANCHOR", caught.exception.message)
        verdict, why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_NON_EXECUTABLE, why)
        self.assertIn("misdeclared-uses", why)

    def test_a_record_that_declares_nothing_is_not_accused_of_lying(self):
        """AND THE RECORDS ALREADY WRITTEN STILL PASS.

        Every row in the shipped ledgers carries `uses: []`, from before the
        field was derived. An absent claim is not a false one, and refusing
        those rows would stop the assembly over a field nothing reads.
        """
        record = CC.make_record("$PARENT_REPO",
                                argv=["python3", "$TOOLS_ANCHOR/x.py"])
        record["uses"] = []
        self.assertEqual(CC.validate(record, defined=set(CC.ROOT_VARS)),
                         ["PARENT_REPO", "TOOLS_ANCHOR"])
        verdict, _why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE)
        record.pop("uses")
        verdict, _why = CC.classify(None, record, defined=set(CC.ROOT_VARS))
        self.assertEqual(verdict, CC.VERDICT_EXECUTABLE)


class CommandReplay(Fixture):
    """V16, DEFECT 13: A REPLAY THAT RUNS, AND ONE THAT REFUSES TO.

    "For representative rows: reconstruct the environment, execute the
    recorded command exactly, verify the intended tool runs, and compare
    exit/result identity. The checker must FAIL when quoting prevents
    expansion."
    """

    def replay_tool(self) -> Path:
        return Path(__file__).resolve().parent / "replay-command.py"

    def commands_file(self, root: Path, rows: list[dict],
                      roots: dict | None = None) -> Path:
        blob = {
            "schema": "catena-commands/1",
            "variables": {"schema": CC.VARIABLES_SCHEMA,
                          "roots": roots if roots is not None
                          else dict(CC.ROOT_VARS)},
            "counts": {}, "commands": rows,
        }
        out = root / "commands.json"
        out.write_text(json.dumps(blob, indent=2, sort_keys=True),
                       encoding="utf-8")
        return out

    def run_replay(self, *args) -> tuple[int, str]:
        done = subprocess.run(
            [sys.executable, str(self.replay_tool()), *[str(one) for one in args]],
            capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr

    def test_a_recorded_row_replays_and_its_exit_matches(self):
        """THE POSITIVE, AND IT IS NOT VACUOUS.

        The recorded command writes a witness file. The replay is checked for
        the witness as well as for the exit, so a replay that "succeeded"
        without starting the intended process fails this test.
        """
        root = self.temp("command-replay-")
        candidate = root / "candidate"
        (candidate / "tools").mkdir(parents=True)
        (candidate / "tools" / "witness.py").write_text(
            "import pathlib, sys\n"
            "pathlib.Path('ran.txt').write_text('the intended tool ran')\n"
            "raise SystemExit(3)\n", encoding="utf-8")
        rows = [{"side": "head", "slug": "witness", "exit": 3,
                 "command": "python3 tools/witness.py",
                 "recorded": CC.VERDICT_EXECUTABLE,
                 "exec": CC.make_record("$CANDIDATE_REPO",
                                        argv=["python3", "tools/witness.py"])}]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay(
            "--commands", commands, "--side", "head", "--replay", "witness",
            "--root", f"CANDIDATE_REPO={candidate}")
        self.assertEqual(code, 0, said)
        self.assertIn("exit : 3 (recorded 3)", said)
        self.assertEqual((candidate / "ran.txt").read_text(encoding="utf-8"),
                         "the intended tool ran",
                         "the replay must actually start the intended tool")

    def test_a_replay_whose_exit_diverges_is_reported(self):
        """THE MATCHED NEGATIVE for the positive above."""
        root = self.temp("command-replay-")
        candidate = root / "candidate"
        (candidate / "tools").mkdir(parents=True)
        (candidate / "tools" / "witness.py").write_text(
            "raise SystemExit(9)\n", encoding="utf-8")
        rows = [{"side": "head", "slug": "witness", "exit": 3,
                 "command": "python3 tools/witness.py",
                 "recorded": CC.VERDICT_EXECUTABLE,
                 "exec": CC.make_record("$CANDIDATE_REPO",
                                        argv=["python3", "tools/witness.py"])}]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay(
            "--commands", commands, "--side", "head", "--replay", "witness",
            "--root", f"CANDIDATE_REPO={candidate}")
        self.assertEqual(code, 1, said)
        self.assertIn("DIVERGED", said)

    def test_the_checker_fails_when_quoting_prevents_expansion(self):
        """DEFECT 13, THE REQUIRED DEMONSTRATION.

        A V15-shaped row -- a `$`-anchor inside single quotes -- is put into
        a command record and `--check` is asked about it. It must refuse, and
        it must refuse for the stated reason.
        """
        root = self.temp("command-replay-")
        rows = [{
            "side": "head", "slug": "gzip-sizes", "exit": 0,
            "command": "python3 '$TOOLS_ANCHOR/gzip-sizes.py' src",
            "recorded": CC.VERDICT_EXECUTABLE,
            "exec": {"schema": CC.SCHEMA, "cwd": "$CANDIDATE_REPO",
                     "env": {}, "argv": None,
                     "shell": "python3 '$TOOLS_ANCHOR/gzip-sizes.py' src"},
        }]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay("--commands", commands, "--check")
        self.assertEqual(code, 1, said)
        self.assertIn("quoted-variable", said)
        self.assertIn("rows refused             : 1", said)
        # AND IT REFUSES TO RUN IT, rather than running something else.
        code, said = self.run_replay(
            "--commands", commands, "--side", "head", "--replay",
            "gzip-sizes", "--root", "CANDIDATE_REPO=/tmp",
            "--root", "TOOLS_ANCHOR=/tmp")
        self.assertEqual(code, 2, said)
        self.assertIn("quoted-variable", said)

    # ---- the exit status is necessary and it is not sufficient ------------
    #
    # V16, THE COMMAND-REPLAY LANE, F1. `--replay` compared exit codes only
    # while its docstring called itself "the non-vacuity proof" that "the head
    # named in the record is the process that ran". The lane demonstrated a
    # false pass on `parent/head-tests-against-parent` -- the row V15 got
    # wrong, and the one row the whole V16 representation was rebuilt to fix.

    def parent_replay_row(self, root: Path) -> tuple[Path, Path]:
        """The lane's own probe: both roots bound to an empty directory.

        `cp` fails, `&&` short-circuits, `python3 -m unittest` never runs, the
        shell exits 1 -- and the record says 1, because the recorded run was a
        wave-1 suite with 288 failures. A failed `cp` and a failing suite are
        the same number.
        """
        parent = root / "parent"
        candidate = root / "candidate"
        parent.mkdir()
        candidate.mkdir()
        record = CC.make_record(
            "$PARENT_REPO",
            shell='cp "$CANDIDATE_REPO/tools/tests/test_catena_wave_1.py" '
                  'tools/tests/test_catena_wave_1.py && python3 -m unittest '
                  "discover -s tools/tests -p 'test_catena_wave_1.py' -v")
        rows = [{"side": "parent", "slug": "head-tests-against-parent",
                 "exit": 1, "command": CC.render_shell(record),
                 "recorded": CC.VERDICT_EXECUTABLE, "exec": record}]
        return self.commands_file(root, rows), parent

    def test_a_row_that_matches_on_exit_alone_says_so(self):
        """THE FALSE PASS ITSELF, kept and labelled rather than hidden.

        Exit-code identity is still reported as a match, because it is one;
        what is new is that the tool states on its own output exactly what it
        compared, so a reader cannot take this run for more than it is.
        """
        root = self.temp("false-pass-")
        commands, parent = self.parent_replay_row(root)
        code, said = self.run_replay(
            "--commands", commands, "--side", "parent",
            "--replay", "head-tests-against-parent",
            "--root", f"PARENT_REPO={parent}",
            "--root", f"CANDIDATE_REPO={root / 'candidate'}")
        self.assertEqual(code, 0, said)
        self.assertIn("exit : 1 (recorded 1)", said)
        self.assertIn("matched on EXIT STATUS ALONE", said)
        # And the suite really did not run, which is the whole point.
        self.assertNotIn("Ran 604 tests", said)

    def test_a_witness_catches_the_run_that_never_happened(self):
        """THE MATCHED NEGATIVE, and the check the docstring used to claim.

        The recorded transcript says `Ran 604 tests` and `FAILED
        (failures=288)`. A run in which `cp` failed and `unittest` never
        started cannot say either, however its exit status came out.
        """
        root = self.temp("false-pass-")
        commands, parent = self.parent_replay_row(root)
        code, said = self.run_replay(
            "--commands", commands, "--side", "parent",
            "--replay", "head-tests-against-parent",
            "--witness", "Ran 604 tests",
            "--witness", "FAILED (failures=288)",
            "--root", f"PARENT_REPO={parent}",
            "--root", f"CANDIDATE_REPO={root / 'candidate'}")
        self.assertEqual(code, 1, said)
        self.assertIn("exit : 1 (recorded 1)", said)
        self.assertIn("VACUOUS", said)
        self.assertIn("witness: MISSING 'Ran 604 tests'", said)
        self.assertNotIn("matched on EXIT STATUS ALONE", said)

    def test_a_witness_the_intended_tool_prints_is_found(self):
        """THE MATCHED POSITIVE. The tool runs, says its line, and passes."""
        root = self.temp("witness-")
        candidate = root / "candidate"
        (candidate / "tools").mkdir(parents=True)
        (candidate / "tools" / "suite.py").write_text(
            "import sys\n"
            "print('Ran 604 tests in 12.0s')\n"
            "print('FAILED (failures=288)', file=sys.stderr)\n"
            "raise SystemExit(1)\n", encoding="utf-8")
        record = CC.make_record("$CANDIDATE_REPO",
                                argv=["python3", "tools/suite.py"])
        rows = [{"side": "head", "slug": "suite", "exit": 1,
                 "command": CC.render_shell(record),
                 "recorded": CC.VERDICT_EXECUTABLE, "exec": record}]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay(
            "--commands", commands, "--side", "head", "--replay", "suite",
            "--witness", "Ran 604 tests",
            # STDERR COUNTS AS OUTPUT, because the recorded transcripts the
            # witnesses come from are themselves `> log 2>&1`.
            "--witness", "FAILED (failures=288)",
            "--root", f"CANDIDATE_REPO={candidate}")
        self.assertEqual(code, 0, said)
        self.assertIn("witness: FOUND   'Ran 604 tests'", said)
        self.assertIn("witness: FOUND   'FAILED (failures=288)'", said)
        self.assertNotIn("VACUOUS", said)
        self.assertNotIn("matched on EXIT STATUS ALONE", said)

    def test_a_witness_does_not_rescue_a_diverged_exit(self):
        """AND THE EXIT CHECK IS NOT TRADED AWAY FOR THE NEW ONE."""
        root = self.temp("witness-")
        candidate = root / "candidate"
        (candidate / "tools").mkdir(parents=True)
        (candidate / "tools" / "suite.py").write_text(
            "print('Ran 604 tests in 12.0s')\n"
            "raise SystemExit(7)\n", encoding="utf-8")
        record = CC.make_record("$CANDIDATE_REPO",
                                argv=["python3", "tools/suite.py"])
        rows = [{"side": "head", "slug": "suite", "exit": 1,
                 "command": CC.render_shell(record),
                 "recorded": CC.VERDICT_EXECUTABLE, "exec": record}]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay(
            "--commands", commands, "--side", "head", "--replay", "suite",
            "--witness", "Ran 604 tests",
            "--root", f"CANDIDATE_REPO={candidate}")
        self.assertEqual(code, 1, said)
        self.assertIn("witness: FOUND", said)
        self.assertIn("DIVERGED", said)

    def test_the_repaired_row_passes_the_same_checker(self):
        """THE MATCHED POSITIVE for the refusal above."""
        root = self.temp("command-replay-")
        rows = [{
            "side": "head", "slug": "gzip-sizes", "exit": 0,
            "command": 'python3 "$TOOLS_ANCHOR/gzip-sizes.py" src',
            "recorded": CC.VERDICT_EXECUTABLE,
            "exec": CC.make_record(
                "$CANDIDATE_REPO",
                argv=["python3", "$TOOLS_ANCHOR/gzip-sizes.py", "src"]),
        }]
        commands = self.commands_file(root, rows)
        code, said = self.run_replay("--commands", commands, "--check")
        self.assertEqual(code, 0, said)
        self.assertIn("rows validated EXECUTABLE: 1", said)
        self.assertIn("rows refused             : 0", said)

# ---------------------------------------------------------------------------
# V16, DEFECT 6: ONE APPEND-ONLY LEDGER, AND A RETIREMENT THAT IS A RECORDED
# ACT RATHER THAN A `mv`.
#
# The review found nine package attempts across three V15 ledgers where the
# prose says "five refusals then a sixth authoritative attempt"; ordinals 1
# through 6 reissued; one retired battery with no terminal row; two completed
# retired batteries never classified set-aside; and a fresh-ledger attempt
# that briefly reached authority before supersession. Every one of those is
# downstream of the same thing: the ordinal allocator can only refuse an
# ordinal recorded IN THE FILE IT IS HANDED, so moving a ledger aside emptied
# it and `max(spent) + 1` started again at 1.
class Retirement(Fixture):

    def two_batteries_and_a_package(self, lane=LANE):
        """A ledger with a green battery whose figures are not carried."""
        return [
            lane_row(lane),
            {"record": "state", "lane": lane, "attempt": "parent-a",
             "attempt_no": "1", "side": "parent", "status": "started",
             "start": "2026-08-17T10:00:00Z", "end": "2026-08-17T10:00:00Z",
             "reason": ""},
            {"record": "attempt", "lane": lane, "attempt": "parent-a",
             "attempt_no": "1", "side": "parent", "status": "complete",
             "start": "2026-08-17T10:00:00Z", "end": "2026-08-17T10:05:00Z",
             "reason": ""},
            {"record": "state", "lane": lane, "attempt": "head-b",
             "attempt_no": "2", "side": "head", "status": "started",
             "start": "2026-08-17T10:06:00Z", "end": "2026-08-17T10:06:00Z",
             "reason": ""},
            {"record": "attempt", "lane": lane, "attempt": "head-b",
             "attempt_no": "2", "side": "head", "status": "complete",
             "start": "2026-08-17T10:06:00Z", "end": "2026-08-17T10:10:00Z",
             "reason": ""},
        ]

    def retire(self, rows, reason="the host changed mid-lane", lane=LANE):
        root = self.temp("retirement-")
        old = root / "old.jsonl"
        old.write_text("".join(json.dumps(one, sort_keys=True) + "\n"
                               for one in rows), encoding="utf-8")
        new = root / "new.jsonl"
        code, said = self.run_checks(
            "--retire-ledger", old, "--to", new, "--lane", lane,
            "--reason", reason)
        return code, said, old, new

    def test_the_retired_ledger_the_verb_writes_passes_its_own_audit(self):
        """V16, THE COMMAND-REPLAY LANE, IN PASSING.

        `--verify-ledger` reported `a row names no attempt` on every retired
        ledger this toolchain has ever produced. The row it faulted is the
        `record=retired` row `--retire-ledger` appends one line earlier: a
        statement about the FILE -- its digest, byte count, row count and
        spent ordinals -- which has no attempt id because it is not about an
        attempt. A verb and an audit in the same tool disagreeing about what
        a legal row looks like is the same defect class as the rest of this
        lane, one file further in.
        """
        code, said, old, _new = self.retire([
            lane_row(),
            state(HEAD_ONE, 1, "head", "started",
                  "2026-08-17T12:00:00Z", "2026-08-17T12:00:00Z"),
            terminal(HEAD_ONE, 1, "head", "complete",
                     "2026-08-17T12:00:00Z", "2026-08-17T12:04:01Z"),
        ])
        self.assertEqual(code, 0, said)
        rows = [json.loads(one) for one
                in old.read_text(encoding="utf-8").splitlines() if one.strip()]
        retired = [one for one in rows if one.get("record") == "retired"]
        self.assertEqual(len(retired), 1, rows)
        self.assertNotIn("attempt", retired[0])
        code, said = self.run_checks("--verify-ledger", "--attempts", old,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn("problems: 0", said)
        self.assertNotIn("names no attempt", said)

    def test_a_row_that_is_not_about_the_file_still_needs_an_attempt(self):
        """THE MATCHED NEGATIVE. The fault is real for every other row.

        A `step` row that names no attempt cannot be read at all: nothing
        says which attempt ran it. Recognising the retirement row must not
        buy that, so the refusal is keyed on the record KIND and names it.
        """
        rows = sound_rows()
        rows.append({"record": "step", "lane": LANE, "attempt_no": "1",
                     "side": "head", "start": "2026-08-17T12:07:00Z",
                     "end": "2026-08-17T12:08:00Z", "exit": "0",
                     "log": "logs/attempt-01/x.log", "command": "make check"})
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("a row names no attempt: record='step'", said)
        self.assertIn("Only a row ABOUT THE FILE", said)

    def test_a_retirement_carries_the_spent_ordinals_forward(self):
        """THE V15 DEFECT, CLOSED.

        Ordinal 1 was spent three times in lane V15 and ordinals 2 through 6
        twice each, while the identity row of all three files says an ordinal
        "is never reissued". The successor's lane row carries the
        predecessor's spent ordinals and the allocator unions them in.
        """
        code, said, old, new = self.retire(self.two_batteries_and_a_package())
        self.assertEqual(code, 0, said)
        opening = json.loads(new.read_text(encoding="utf-8"))
        self.assertEqual(opening["ordinals_already_spent"], [1, 2])
        # THE NEXT ORDINAL IS 3 OVER AN EMPTY-LOOKING FILE.
        code, ordinal, said = self.allocate("--attempts", new, "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertEqual(ordinal, "3")
        # AND A REISSUE IS REFUSED BY NAME.
        code, _ordinal, said = self.allocate(
            "--attempts", new, "--lane", LANE, "--propose", "1")
        self.assertEqual(code, 1, said)
        self.assertIn("a retired predecessor ledger of this lane", said)

    def test_the_predecessor_is_retained_hashed_and_counted(self):
        """A retired ledger whose contents survive only as prose is lost."""
        code, said, old, new = self.retire(self.two_batteries_and_a_package())
        self.assertEqual(code, 0, said)
        opening = json.loads(new.read_text(encoding="utf-8"))
        facts = opening["retired_predecessors"][0]
        for key in ("path", "bytes", "rows", "sha256", "ordinals_spent",
                    "reason"):
            self.assertIn(key, facts)
        import hashlib
        self.assertEqual(facts["sha256"],
                         hashlib.sha256(old.read_bytes()).hexdigest(),
                         "the digest must describe the file as retired")
        self.assertEqual(facts["bytes"], len(old.read_bytes()))
        self.assertIn("the host changed mid-lane", facts["reason"])

    def test_the_old_ledger_says_out_loud_that_it_stopped(self):
        code, said, old, new = self.retire(self.two_batteries_and_a_package())
        self.assertEqual(code, 0, said)
        rows = [json.loads(one) for one in
                old.read_text(encoding="utf-8").splitlines() if one.strip()]
        terminal = [one for one in rows if one.get("record") == "retired"]
        self.assertEqual(len(terminal), 1, rows)
        self.assertEqual(terminal[0]["successor"], "new.jsonl")
        self.assertIn("ordinals_spent", terminal[0])

    def test_completed_unused_batteries_are_classified_set_aside(self):
        """V15 had two and classified neither, while PROVENANCE.md said
        "This lane set no cohort aside"."""
        code, said, old, new = self.retire(self.two_batteries_and_a_package())
        self.assertEqual(code, 0, said)
        self.assertIn("set aside: head-b, parent-a", said)
        rows = [json.loads(one) for one in
                old.read_text(encoding="utf-8").splitlines() if one.strip()]
        aside = {one["attempt"] for one in rows
                 if one.get("status") == "set-aside"}
        self.assertEqual(aside, {"parent-a", "head-b"})
        for one in rows:
            if one.get("status") == "set-aside":
                self.assertTrue(one["reason"].strip(),
                                "a set-aside cohort states why")

    def test_an_attempt_with_no_terminal_row_is_named_at_retirement(self):
        """V15's L1 held one and it is unresolved to this day."""
        rows = self.two_batteries_and_a_package()
        rows = [one for one in rows
                if not (one.get("record") == "attempt"
                        and one.get("attempt") == "parent-a")]
        code, said, old, new = self.retire(rows)
        self.assertEqual(code, 0, said)
        self.assertIn("UNRESOLVED at retirement: parent-a", said)
        opening = json.loads(new.read_text(encoding="utf-8"))
        self.assertIn("parent-a",
                      opening["retired_predecessors"][0]["unresolved_attempts"])

    def test_a_retirement_without_a_reason_is_refused(self):
        code, said, old, new = self.retire(self.two_batteries_and_a_package(),
                                           reason="   ")
        self.assertEqual(code, 1, said)
        self.assertIn("--reason is required", said)

    def test_a_retirement_over_an_existing_successor_is_refused(self):
        root = self.temp("retirement-")
        old = root / "old.jsonl"
        old.write_text("".join(
            json.dumps(one, sort_keys=True) + "\n"
            for one in self.two_batteries_and_a_package()), encoding="utf-8")
        new = root / "new.jsonl"
        new.write_text("{}\n", encoding="utf-8")
        code, said = self.run_checks("--retire-ledger", old, "--to", new,
                                     "--lane", LANE, "--reason", "why")
        self.assertEqual(code, 1, said)
        self.assertIn("already exists", said)



class Abandonment(Fixture):
    """AN ATTEMPT STOPPED FROM OUTSIDE REACHES A TERMINAL ROW, WITH ITS REASON.

    V16, THE V15 REVIEW: "one retired battery never gets a terminal row". The
    vocabulary could express the ABSENCE of a row and not the fact the absence
    stood for, so a reader could not tell an abandoned attempt from a lost one
    and the audit could only say `unresolved`. `--abandon-attempt` is the verb
    that says what happened; these are the refusals that keep it from becoming
    a shorter way to write the same silence.
    """

    REASON = ("the process running this battery was stopped from outside it "
              "after three green steps; no step failed and no figure of this "
              "attempt is carried anywhere")

    def abandon(self, path, attempt, *extra):
        return self.run_checks("--abandon-attempt", attempt, "--attempts",
                               path, "--lane", LANE, *extra)

    def unterminated(self):
        """A ledger whose last attempt started and never reached a verdict."""
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z"),
                 step(HEAD_TWO, 4, "head", "2026-08-17T17:00:01Z",
                      "2026-08-17T17:00:02Z",
                      "logs/attempt-04/focused-catena-head.log")]
        return self.ledger(rows)

    def test_an_attempt_with_no_terminal_row_fails_the_audit_before_this(self):
        path = self.unterminated()
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 1, said)
        self.assertIn("no terminal row", said)

    def test_abandoning_it_gives_it_one_and_the_audit_passes(self):
        path = self.unterminated()
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 0, said)
        self.assertIn("steps recorded before it stopped: 1", said)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn("abandoned -- the process running this battery", said)
        self.assertIn("problems: 0", said)

    def test_abandonment_is_not_failure_and_says_so_in_the_row(self):
        """`failed` asserts a decision. Nothing decided this."""
        path = self.unterminated()
        self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        terminal = [r for r in rows
                    if r.get("attempt") == HEAD_TWO
                    and r.get("record") == "attempt"]
        self.assertEqual(len(terminal), 1)
        self.assertEqual(terminal[0]["status"], "abandoned")
        self.assertEqual(terminal[0]["reason"], self.REASON)

    def test_an_abandonment_with_no_reason_is_refused(self):
        path = self.unterminated()
        code, said = self.abandon(path, HEAD_TWO)
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)

    def test_a_reason_too_short_to_be_one_is_refused(self):
        path = self.unterminated()
        code, said = self.abandon(path, HEAD_TWO, "--reason", "stopped")
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)

    def test_an_attempt_the_ledger_does_not_carry_is_refused(self):
        path = self.unterminated()
        code, said = self.abandon(path, "head-20260817T990000Z-99zzzzzz",
                                  "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no attempt", said)

    def test_an_attempt_that_already_terminated_is_refused(self):
        """One attempt, one terminal disposition. Rewriting one is forbidden."""
        path = self.ledger(sound_rows())
        code, said = self.abandon(path, HEAD_ONE, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("already reaches a terminal disposition", said)

    def test_a_package_assembly_stopped_from_outside_is_abandoned(self):
        """The battery argument, unchanged by what the attempt was building.

        An assembly stopped from outside reached no decision of its own: no
        phase refused it and no gate failed. `discarded` asserts the pipeline
        decided, and saying so would claim a refusal that never happened.
        """
        rows = sound_rows()
        rows += [state(PACKAGE_TWO, 5, "package", "started",
                       "2026-08-17T18:00:00Z", "2026-08-17T18:00:00Z"),
                 step(PACKAGE_TWO, 5, "package", "2026-08-17T18:00:01Z",
                      "2026-08-17T18:00:02Z",
                      "logs/attempt-05/seal.log")]
        path = self.ledger(rows)
        code, said = self.abandon(path, PACKAGE_TWO, "--reason", self.REASON)
        self.assertEqual(code, 0, said)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{PACKAGE_TWO}: abandoned", said)

    def test_an_abandoned_package_attempt_is_still_irreversible(self):
        rows = sound_rows()
        rows += [state(PACKAGE_TWO, 5, "package", "started",
                       "2026-08-17T18:00:00Z", "2026-08-17T18:00:00Z")]
        path = self.ledger(rows)
        self.abandon(path, PACKAGE_TWO, "--reason", self.REASON)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        for later in ("sealed", "discarded"):
            with self.subTest(later=later):
                more = rows + [state(PACKAGE_TWO, 5, "package", later,
                                     "2026-08-17T19:00:00Z",
                                     "2026-08-17T19:00:00Z",
                                     reason="an attempt reopened after it was "
                                            "abandoned")]
                code, said = self.verify(more)
                self.assertEqual(code, 1, said)


    # -- the V16 hardening: what abandonment may and may not cover ----------

    def with_step(self, **over):
        """One started attempt plus one step, shaped by the caller."""
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z"),
                 step(HEAD_TWO, 4, "head", "2026-08-17T17:00:01Z",
                      "2026-08-17T17:00:02Z",
                      "logs/attempt-04/make-check-head.log", **over)]
        return self.ledger(rows)

    def test_an_inherited_red_gate_does_not_block_abandonment(self):
        """A NON-ZERO EXIT IS A RESULT, NOT A FAILED STEP.

        Four gates in the repository under test are inherited-red by design
        and return 2, 2, 1 and 2 at BOTH endpoints. Reading a non-zero exit as
        a failure would make this verb unusable after step five and would
        record a false statement about the attempt.
        """
        path = self.with_step(exit="2", result="exit 2")
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 0, said)

    def test_a_step_that_recorded_a_refusal_blocks_abandonment(self):
        path = self.with_step(exit="1", result="REFUSED: log target exists")
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("carries a step that did not pass", said)
        self.assertIn("failed or discarded, not abandoned", said)

    def test_a_step_that_recorded_failure_blocks_abandonment(self):
        path = self.with_step(exit="1", status="failed", result="failed")
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("carries a step that did not pass", said)

    def test_an_attempt_of_another_lane_is_refused(self):
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z")]
        for row in rows:
            if row.get("attempt") == HEAD_TWO:
                row["lane"] = "V15"
        path = self.ledger(rows)
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane V15", said)

    def test_abandonment_is_irreversible(self):
        """No later row may move an abandoned attempt anywhere at all."""
        path = self.unterminated()
        self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        for later in ("complete", "failed", "set-aside"):
            with self.subTest(later=later):
                more = rows + [state(HEAD_TWO, 4, "head", later,
                                     "2026-08-17T18:00:00Z",
                                     "2026-08-17T18:00:00Z",
                                     reason="an attempt reopened after it was "
                                            "abandoned")]
                code, said = self.verify(more)
                self.assertEqual(code, 1, said)
        # And the verb itself will not write a second disposition either.
        code, said = self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("already reaches a terminal disposition", said)

    def test_replacement_work_takes_a_new_attempt_id(self):
        """The abandoned id is spent; the rerun is its own attempt."""
        path = self.unterminated()
        self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        rows += [state(HEAD_THREE, 6, "head", "started",
                       "2026-08-17T19:00:00Z", "2026-08-17T19:00:00Z"),
                 terminal(HEAD_THREE, 6, "head", "complete",
                         "2026-08-17T19:00:00Z", "2026-08-17T19:10:00Z")]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_TWO}: abandoned", said)
        self.assertIn(f"{HEAD_THREE}: complete", said)

    def test_completeness_sees_it_resolved_but_never_as_evidence(self):
        path = self.unterminated()
        self.abandon(path, HEAD_TWO, "--reason", self.REASON)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn("problems: 0", said)
        self.assertNotIn("unresolved", said)
        self.assertIn(f"{HEAD_TWO}: abandoned", said)


class SetAsideVerb(Fixture):
    """THE POST-TERMINAL WORD, APPENDED RATHER THAN INFERRED.

    V16, THE V15 REVIEW: "completed retired batteries are not classified
    set-aside". V15 held two such cohorts, used the word zero times, and its
    record said in prose that it had set none aside. Retiring a whole ledger to
    classify one attempt of a live one would rewrite a record to make it tidy,
    so this appends instead.
    """

    REASON = ("this cohort measured a head that was superseded before the "
              "package was built and none of its figures is carried into any "
              "claim of this lane")

    def aside(self, path, attempt, *extra):
        return self.run_checks("--set-aside-attempt", attempt, "--attempts",
                               path, "--lane", LANE, *extra)

    def test_a_completed_cohort_is_set_aside_and_the_audit_passes(self):
        path = self.ledger(sound_rows())
        code, said = self.aside(path, HEAD_ONE, "--reason", self.REASON)
        self.assertEqual(code, 0, said)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: complete | evidence set-aside -- this "
                      f"cohort measured", said)

    def test_the_terminal_row_still_says_the_battery_completed(self):
        """Post-terminal, not an amendment: the battery did complete."""
        path = self.ledger(sound_rows())
        self.aside(path, HEAD_ONE, "--reason", self.REASON)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        mine = [r for r in rows if r.get("attempt") == HEAD_ONE]
        terminal = [r for r in mine if r.get("record") == "attempt"]
        self.assertEqual([r["status"] for r in terminal], ["complete"])
        self.assertEqual([r["status"] for r in mine
                          if r.get("record") == "state"
                          and r.get("status") == "set-aside"], ["set-aside"])

    def test_an_attempt_still_open_cannot_be_set_aside(self):
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z")]
        code, said = self.aside(self.ledger(rows), HEAD_TWO,
                                "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("reaches no terminal disposition yet", said)

    def test_a_disposition_other_than_complete_cannot_be_softened(self):
        """`set-aside` may not cover what `failed` or `abandoned` says."""
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z"),
                 terminal(HEAD_TWO, 4, "head", "failed",
                          "2026-08-17T17:00:00Z", "2026-08-17T17:05:00Z",
                          reason="a guard of the battery refused this run")]
        code, said = self.aside(self.ledger(rows), HEAD_TWO,
                                "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("would cover what that disposition says", said)

    def test_a_package_attempt_is_superseded_not_set_aside(self):
        code, said = self.aside(self.ledger(sound_rows()), PACKAGE_ONE,
                                "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("battery vocabulary", said)

    def test_setting_one_aside_twice_is_refused(self):
        path = self.ledger(sound_rows())
        self.aside(path, HEAD_ONE, "--reason", self.REASON)
        code, said = self.aside(path, HEAD_ONE, "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("already set aside", said)

    def test_a_token_reason_is_refused(self):
        code, said = self.aside(self.ledger(sound_rows()), HEAD_ONE,
                                "--reason", "not used")
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)

    def test_an_attempt_of_another_lane_is_refused(self):
        rows = [dict(r) for r in sound_rows()]
        for row in rows:
            if row.get("attempt") == HEAD_ONE:
                row["lane"] = "V15"
        code, said = self.aside(self.ledger(rows), HEAD_ONE,
                                "--reason", self.REASON)
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane V15", said)



class LogRootElsewhere(Fixture):
    """A NAMED ROOT THAT IS NOT HERE IS EXPLAINED, OR IT IS REFUSED."""

    WHERE = ("this assembly was discarded before the freeze; its partially "
             "built tree is kept unaltered beside its discard marker in the "
             "build directory and none of its bytes is evidence")

    def where(self, path, attempt, *extra):
        return self.run_checks("--log-root-elsewhere", attempt, "--attempts",
                               path, "--lane", LANE, *extra)

    def test_the_row_carries_no_status_because_it_is_not_a_transition(self):
        """It states where bytes are; both dispositions stay what they were."""
        path = self.ledger(sound_rows())
        code, said = self.where(path, PACKAGE_ONE, "--reason", self.WHERE)
        self.assertEqual(code, 0, said)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        note = [r for r in rows if r.get("record") == "note"]
        self.assertEqual(len(note), 1)
        self.assertNotIn("status", note[0])
        self.assertEqual(note[0]["log_root_elsewhere"], self.WHERE)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)

    def test_a_fabricated_status_would_have_been_refused(self):
        """The control: the machine has no such state, and says so."""
        rows = sound_rows() + [state(PACKAGE_ONE, 3, "package",
                                     "log-root-elsewhere",
                                     "2026-08-17T16:00:00Z",
                                     "2026-08-17T16:00:00Z",
                                     reason="a state the machine lacks")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("never 'log-root-elsewhere'", said)

    def test_a_token_reason_is_refused(self):
        code, said = self.where(self.ledger(sound_rows()), PACKAGE_ONE,
                                "--reason", "moved")
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)

    def test_an_attempt_the_ledger_does_not_carry_is_refused(self):
        code, said = self.where(self.ledger(sound_rows()),
                                "package-20260817T990000Z-99zzzzzz",
                                "--reason", self.WHERE)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no attempt", said)

    def test_saying_it_twice_is_refused(self):
        path = self.ledger(sound_rows())
        self.where(path, PACKAGE_ONE, "--reason", self.WHERE)
        code, said = self.where(path, PACKAGE_ONE, "--reason", self.WHERE)
        self.assertEqual(code, 1, said)
        self.assertIn("already says where its log root is", said)

    def test_an_attempt_of_another_lane_is_refused(self):
        rows = [dict(r) for r in sound_rows()]
        for row in rows:
            if row.get("attempt") == PACKAGE_ONE:
                row["lane"] = "V15"
        code, said = self.where(self.ledger(rows), PACKAGE_ONE,
                                "--reason", self.WHERE)
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane V15", said)



class SupersededEvidence(Fixture):
    """THE ONE SUCCESSION EITHER EVIDENCE AXIS ADMITS."""

    WHY = ("a later cohort measured the same endpoint with the tools the "
           "package actually ships, and the figures carried are that "
           "cohort's rather than this one's")

    def sup(self, path, attempt, *extra):
        return self.run_checks("--supersede-evidence", attempt, "--attempts",
                               path, "--lane", LANE, *extra)

    def authoritative(self, attempt=HEAD_ONE):
        path = self.ledger(sound_rows())
        self.run_checks("--authoritative-evidence", attempt, "--attempts",
                        path, "--lane", LANE, "--reason",
                        "this cohort measured the endpoint whose figures the "
                        "package carries and its transcripts are shipped")
        return path

    def test_an_authoritative_cohort_may_be_superseded(self):
        path = self.authoritative()
        code, said = self.sup(path, HEAD_ONE, "--reason", self.WHY)
        self.assertEqual(code, 0, said)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn("evidence superseded", said)

    def test_the_authoritative_row_it_follows_is_left_alone(self):
        """That attempt did hold that disposition for the time it held it."""
        path = self.authoritative()
        self.sup(path, HEAD_ONE, "--reason", self.WHY)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        mine = [r for r in rows if r.get("attempt") == HEAD_ONE]
        self.assertEqual(
            [r["status"] for r in mine if r.get("status") == "authoritative"],
            ["authoritative"])
        self.assertEqual(
            [r["status"] for r in mine if r.get("status") == "superseded"],
            ["superseded"])

    def test_superseded_is_terminal(self):
        path = self.authoritative()
        self.sup(path, HEAD_ONE, "--reason", self.WHY)
        code, said = self.sup(path, HEAD_ONE, "--reason", self.WHY)
        self.assertEqual(code, 1, said)
        self.assertIn("already superseded", said)

    def test_a_set_aside_cohort_cannot_be_superseded(self):
        """Superseding it would assert it had once been carried."""
        path = self.ledger(sound_rows())
        self.run_checks("--set-aside-attempt", HEAD_ONE, "--attempts", path,
                        "--lane", LANE, "--reason",
                        "this cohort completed and its figures were declined "
                        "before any package carried them")
        code, said = self.sup(path, HEAD_ONE, "--reason", self.WHY)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no authoritative evidence", said)

    def test_an_unevidenced_cohort_cannot_be_superseded(self):
        code, said = self.sup(self.ledger(sound_rows()), HEAD_ONE,
                              "--reason", self.WHY)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no authoritative evidence", said)

    def test_authoritative_cannot_follow_superseded(self):
        path = self.authoritative()
        self.sup(path, HEAD_ONE, "--reason", self.WHY)
        code, said = self.run_checks(
            "--authoritative-evidence", HEAD_ONE, "--attempts", path,
            "--lane", LANE, "--reason",
            "an attempt whose evidence was superseded must never reclaim it")
        self.assertEqual(code, 1, said)

    def test_a_token_reason_is_refused(self):
        code, said = self.sup(self.authoritative(), HEAD_ONE,
                              "--reason", "replaced")
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)



class CrossLedgerHistory(Fixture):
    """THE HISTORY IS EVERY LEDGER, NOT THE LAST ONE."""

    def ledger_file(self, root, name, rows):
        path = root / name
        path.write_text("".join(json.dumps(one, sort_keys=True) + "\n"
                                for one in rows), encoding="utf-8")
        return path

    def two_files(self):
        root = self.temp("history-")
        first = self.ledger_file(root, "first.jsonl", [
            lane_row(),
            {"record": "attempt", "lane": LANE, "attempt": "package-one",
             "attempt_no": "1", "side": "package", "status": "discarded",
             "start": "2026-08-17T10:00:00Z", "end": "2026-08-17T10:01:00Z",
             "reason": "the normalize pass failed"},
        ])
        second = self.ledger_file(root, "second.jsonl", [
            lane_row(),
            {"record": "attempt", "lane": LANE, "attempt": "package-two",
             "attempt_no": "1", "side": "package", "status": "sealed",
             "start": "2026-08-17T11:00:00Z", "end": "2026-08-17T11:01:00Z",
             "reason": ""},
            {"record": "state", "lane": LANE, "attempt": "package-two",
             "attempt_no": "1", "side": "package", "status": "authoritative",
             "start": "2026-08-17T11:00:00Z", "end": "2026-08-17T11:02:00Z",
             "reason": "", "package": "a-package", "head": "1" * 40},
        ])
        return first, second

    def test_the_table_counts_every_attempt_across_every_ledger(self):
        first, second = self.two_files()
        code, said = self.run_checks(
            "--history-table", "--lane", LANE,
            "--attempts-list", first, "--attempts-list", second)
        self.assertEqual(code, 0, said)
        self.assertIn("attempts_total          : 2", said)
        self.assertIn("package_attempts        : 2", said)
        self.assertIn("package_authoritative   : 1", said)
        self.assertIn("package_non_authoritative: 1", said)
        self.assertIn("package-one", said)
        self.assertIn("package-two", said)

    def test_a_replacement_is_named_as_one(self):
        """No earlier V15 ledger is a prefix of a later one and no attempt id
        is shared between any pair -- three files, three claims to be the
        lane's one append-only record."""
        first, second = self.two_files()
        code, said = self.run_checks(
            "--history-table", "--lane", LANE,
            "--attempts-list", first, "--attempts-list", second)
        self.assertEqual(code, 0, said)
        self.assertIn("REPLACEMENT", said)
        self.assertIn("a row was REPLACED, not appended to", said)
        self.assertIn("attempt ids in common: NONE", said)
        self.assertIn("ledger_replacements     : 1", said)

    def test_reused_ordinals_across_files_are_named(self):
        first, second = self.two_files()
        code, said = self.run_checks(
            "--history-table", "--lane", LANE,
            "--attempts-list", first, "--attempts-list", second)
        self.assertEqual(code, 0, said)
        self.assertIn("reused_ordinals         : 1", said)
        self.assertIn("ordinal 1: package-one, package-two", said)

    def test_append_only_is_refused_over_a_replacement(self):
        """THE REFUSAL THE BRIEF ASKS FOR: the tooling must refuse to call a
        history append-only across a row replacement."""
        first, second = self.two_files()
        code, said = self.run_checks(
            "--history-table", "--lane", LANE, "--claim-append-only",
            "--attempts-list", first, "--attempts-list", second)
        self.assertEqual(code, 1, said)
        self.assertIn("is not one append-only record", said)

    def test_append_only_stands_over_a_real_append(self):
        """THE MATCHED POSITIVE. A genuine continuation passes."""
        root = self.temp("history-")
        base = [
            lane_row(),
            {"record": "attempt", "lane": LANE, "attempt": "package-one",
             "attempt_no": "1", "side": "package", "status": "discarded",
             "start": "2026-08-17T10:00:00Z", "end": "2026-08-17T10:01:00Z",
             "reason": "the normalize pass failed"},
        ]
        more = base + [
            {"record": "attempt", "lane": LANE, "attempt": "package-two",
             "attempt_no": "2", "side": "package", "status": "sealed",
             "start": "2026-08-17T11:00:00Z", "end": "2026-08-17T11:01:00Z",
             "reason": ""},
        ]
        first = self.ledger_file(root, "first.jsonl", base)
        second = self.ledger_file(root, "second.jsonl", more)
        code, said = self.run_checks(
            "--history-table", "--lane", LANE, "--claim-append-only",
            "--attempts-list", first, "--attempts-list", second)
        self.assertEqual(code, 0, said)
        self.assertIn("APPEND (+1 row(s))", said)
        self.assertIn("reused_ordinals         : 0", said)

    def test_an_attempt_with_no_terminal_row_is_counted(self):
        root = self.temp("history-")
        only = self.ledger_file(root, "only.jsonl", [
            lane_row(),
            {"record": "state", "lane": LANE, "attempt": "parent-open",
             "attempt_no": "1", "side": "parent", "status": "started",
             "start": "2026-08-17T10:00:00Z", "end": "2026-08-17T10:00:00Z",
             "reason": ""},
        ])
        code, said = self.run_checks(
            "--history-table", "--lane", LANE, "--attempts-list", only)
        self.assertEqual(code, 0, said)
        self.assertIn("attempts_with_no_terminal_row: 1 -- parent-open", said)
        self.assertIn("NONE (no terminal row)", said)


# ---------------------------------------------------------------------------
# V16: THE TWO AXES
# ---------------------------------------------------------------------------
#
# `checks.py` treated `set-aside` as a post-terminal transition of the
# EXECUTION state machine -- `BATTERY_STATES` carried `"complete":
# ("set-aside",)` -- and the resolver collapsed an attempt to one `status`.
# So `--history-table` and `--verify-ledger` printed `set-aside` for an
# attempt whose execution disposition is `complete`, and the fact that the
# battery ran to completion was on no line anywhere.
#
# Every test below drives ONE of the two axes and carries its matched
# opposite, because a refusal with no positive beside it is a tool that
# always fails and a positive with no refusal beside it is a tool that never
# checks anything.

# The seven-attempt shape of the real lane, as ids the audit accepts.
A01 = "parent-20260827T135733Z-01m83vq7"
A02 = "parent-20260827T141358Z-02sh6373"
A03 = "parent-20260827T141439Z-038xp4y2"
A04 = "parent-20260827T143106Z-04hy5j4v"
A05 = "head-20260827T144631Z-05qmtgwx"
A06 = "head-20260827T150233Z-06zg9rhq"
A07 = "head-20260827T154350Z-079xrp6n"

WHY_SET_ASIDE = ("this cohort measured a head that was superseded before the "
                 "package was built and none of its figures is carried into "
                 "any claim of this lane")
WHY_AUTHORITATIVE = ("this cohort measured the checkout this package reports "
                     "and every figure of that side in the package is derived "
                     "from its transcripts")
WHY_FAILED = "a guard of the battery refused this run before any step ran"
WHY_ABANDONED = ("the process running this battery was stopped from outside "
                 "it after three green steps; no step failed and no figure of "
                 "this attempt is carried anywhere")


def known_mix() -> list[dict]:
    """The real lane's shape: two failed, four complete, one abandoned, with
    two cohorts set aside and two carried.

    Written as a fixture so the nine counts are asserted against a history
    whose composition is known by construction -- and NOT as literals in the
    tool, which is the difference between a derivation and a transcription.
    """
    def life(attempt, no, side, execution, reason="",
             evidence="", evidence_reason=""):
        # THE INSTANTS COME FROM THE ID. An attempt id embeds the instant it
        # was minted at and the audit compares the two, so a fixture that
        # invented its own timestamps would be refused for a reason that has
        # nothing to do with what it is testing.
        minted = attempt.split("-")[1]
        stamp = (f"{minted[0:4]}-{minted[4:6]}-{minted[6:8]}T"
                 f"{minted[9:11]}:{minted[11:13]}:{minted[13:15]}")
        made = [state(attempt, no, side, "started",
                      f"{stamp}Z", f"{stamp}Z"),
                terminal(attempt, no, side, execution,
                         f"{stamp}Z", f"{stamp[:-2]}59Z", reason=reason)]
        if evidence:
            made.append(state(attempt, no, side, evidence,
                              f"{stamp[:-2]}59Z", f"{stamp[:-2]}59Z",
                              reason=evidence_reason))
        return made

    return [
        lane_row(),
        *life(A01, 1, "parent", "failed", WHY_FAILED),
        *life(A02, 2, "parent", "failed", WHY_FAILED),
        *life(A03, 3, "parent", "complete",
              evidence="set-aside", evidence_reason=WHY_SET_ASIDE),
        *life(A04, 4, "parent", "complete",
              evidence="authoritative", evidence_reason=WHY_AUTHORITATIVE),
        *life(A05, 5, "head", "complete",
              evidence="set-aside", evidence_reason=WHY_SET_ASIDE),
        *life(A06, 6, "head", "abandoned", WHY_ABANDONED),
        *life(A07, 7, "head", "complete",
              evidence="authoritative", evidence_reason=WHY_AUTHORITATIVE),
    ]


class TwoAxes(Fixture):
    """EXECUTION AND EVIDENCE ARE REPORTED SEPARATELY, AND NEVER COLLAPSED."""

    def test_both_axes_are_on_the_line_and_neither_replaces_the_other(self):
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                       reason=WHY_SET_ASIDE)]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: complete | evidence set-aside", said)
        # THE MATCHED NEGATIVE, and it is the defect itself: the old line put
        # `set-aside` where the execution disposition belongs.
        self.assertNotIn(f"{HEAD_ONE}: set-aside", said)

    def test_an_attempt_with_no_evidence_row_reads_unevidenced(self):
        code, said = self.verify(sound_rows())
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: complete | evidence unevidenced", said)

    def test_an_evidence_row_is_not_an_execution_transition(self):
        """`complete -> set-aside` is not a transition and is not described as
        one: the execution machine does not move, and the audit is silent."""
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                       reason=WHY_SET_ASIDE)]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertNotIn("complete -> set-aside", said)
        self.assertNotIn("illegal transition", said)

    def test_an_execution_word_on_a_state_row_is_still_refused(self):
        """THE MATCHED NEGATIVE. The axes being separate does not make the
        execution machine permissive: a disposition still rides a
        record=attempt row and nothing else."""
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "failed",
                       "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                       reason="a second disposition, on a state row")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("must be carried by a record=attempt row", said)

    def test_an_evidence_word_on_an_attempt_row_is_refused(self):
        rows = sound_rows()
        rows += [terminal(HEAD_TWO, 4, "head", "set-aside",
                          "2026-08-17T17:00:00Z", "2026-08-17T17:00:10Z",
                          reason=WHY_SET_ASIDE)]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("is not a disposition and must not be carried by a "
                      "record=attempt row", said)

    def test_a_second_execution_disposition_is_refused(self):
        rows = sound_rows()
        rows += [terminal(HEAD_ONE, 1, "head", "failed",
                          "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                          reason="a second disposition for one attempt")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("2 terminal rows", said)

    def test_refused_is_not_a_state_in_either_axis(self):
        """§10. Attempts 01 and 02 of this lane were described in passing as
        "refused"; their execution disposition is `failed` and the guard
        refusal is the CAUSE, recorded in the reason."""
        rows = sound_rows()
        rows += [terminal(HEAD_TWO, 4, "head", "refused",
                          "2026-08-17T17:00:00Z", "2026-08-17T17:00:10Z",
                          reason="a guard of the battery refused this run")]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("'refused' is not a disposition, in either axis", said)
        self.assertIn("the execution disposition it causes is 'failed'", said)

    def test_the_disposition_a_guard_refusal_causes_is_accepted(self):
        """THE MATCHED POSITIVE: the same run, recorded the right way."""
        rows = sound_rows()
        rows += [terminal(HEAD_TWO, 4, "head", "failed",
                          "2026-08-17T17:00:00Z", "2026-08-17T17:00:10Z",
                          reason="guard refusal: logs/order-head.txt already "
                                 "exists, so nothing was run")]
        code, said = self.verify(rows)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_TWO}: failed -- guard refusal", said)
        self.assertIn("| evidence unevidenced", said)


class AuthoritativeEvidence(Fixture):
    """THE OTHER HALF OF THE EVIDENCE AXIS, WHICH HAD NO VERB AT ALL.

    A cohort could be DECLINED out loud -- `--set-aside-attempt` -- and
    "these are the figures this package reports" lived in prose. Both cohorts
    read `complete`, and nothing in the record told them apart.
    """

    def record(self, path, attempt, *extra):
        return self.run_checks("--authoritative-evidence", attempt,
                               "--attempts", path, "--lane", LANE, *extra)

    def failed_and_abandoned(self) -> Path:
        rows = sound_rows()
        rows += [
            state(HEAD_TWO, 4, "head", "started",
                  "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z"),
            terminal(HEAD_TWO, 4, "head", "failed",
                     "2026-08-17T17:00:00Z", "2026-08-17T17:05:00Z",
                     reason="a guard of the battery refused this run"),
            state(HEAD_THREE, 6, "head", "started",
                  "2026-08-17T19:00:00Z", "2026-08-17T19:00:00Z"),
            terminal(HEAD_THREE, 6, "head", "abandoned",
                     "2026-08-17T19:00:00Z", "2026-08-17T19:05:00Z",
                     reason=WHY_ABANDONED),
        ]
        return self.ledger(rows)

    def test_a_completed_cohort_is_recorded_authoritative_and_audits(self):
        path = self.ledger(sound_rows())
        code, said = self.record(path, HEAD_ONE, "--reason",
                                 WHY_AUTHORITATIVE)
        self.assertEqual(code, 0, said)
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: complete | evidence authoritative", said)

    def test_the_terminal_row_still_says_the_battery_completed(self):
        path = self.ledger(sound_rows())
        self.record(path, HEAD_ONE, "--reason", WHY_AUTHORITATIVE)
        rows = [json.loads(one) for one in
                path.read_text(encoding="utf-8").splitlines() if one.strip()]
        mine = [r for r in rows if r.get("attempt") == HEAD_ONE]
        self.assertEqual([r["status"] for r in mine
                          if r.get("record") == "attempt"], ["complete"])
        self.assertEqual([r["status"] for r in mine
                          if r.get("record") == "state"
                          and r["status"] == "authoritative"],
                         ["authoritative"])

    def test_authoritative_is_refused_on_a_failed_attempt(self):
        code, said = self.record(self.failed_and_abandoned(), HEAD_TWO,
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("terminated 'failed'", said)
        self.assertIn("unevidenced and stays so", said)

    def test_authoritative_is_refused_on_an_abandoned_attempt(self):
        code, said = self.record(self.failed_and_abandoned(), HEAD_THREE,
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("terminated 'abandoned'", said)

    def test_set_aside_is_refused_on_an_abandoned_attempt(self):
        """The mirror refusal on the other evidence word."""
        code, said = self.run_checks(
            "--set-aside-attempt", HEAD_THREE, "--attempts",
            self.failed_and_abandoned(), "--lane", LANE,
            "--reason", WHY_SET_ASIDE)
        self.assertEqual(code, 1, said)
        self.assertIn("would cover what that disposition says", said)

    def test_an_attempt_still_open_cannot_be_recorded_authoritative(self):
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z")]
        code, said = self.record(self.ledger(rows), HEAD_TWO,
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("reaches no terminal disposition yet", said)

    def test_a_second_evidence_disposition_is_refused(self):
        """Both orders, because irreversibility is not a preference for one
        word over the other."""
        for first, second in (("--authoritative-evidence",
                               "--set-aside-attempt"),
                              ("--set-aside-attempt",
                               "--authoritative-evidence")):
            with self.subTest(first=first):
                path = self.ledger(sound_rows())
                code, said = self.run_checks(
                    first, HEAD_ONE, "--attempts", path, "--lane", LANE,
                    "--reason", WHY_AUTHORITATIVE)
                self.assertEqual(code, 0, said)
                code, said = self.run_checks(
                    second, HEAD_ONE, "--attempts", path, "--lane", LANE,
                    "--reason", WHY_SET_ASIDE)
                self.assertEqual(code, 1, said)
                self.assertIn("already carries the evidence disposition",
                              said)

    def test_the_audit_refuses_a_second_evidence_row_written_by_hand(self):
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "authoritative",
                       "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                       reason=WHY_AUTHORITATIVE),
                 state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:01:00Z", "2026-08-17T16:01:00Z",
                       reason=WHY_SET_ASIDE)]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("illegal transition authoritative -> set-aside", said)

    def test_an_evidence_row_before_the_terminal_row_is_refused(self):
        rows = sound_rows()
        rows += [state(HEAD_TWO, 4, "head", "started",
                       "2026-08-17T17:00:00Z", "2026-08-17T17:00:00Z"),
                 state(HEAD_TWO, 4, "head", "authoritative",
                       "2026-08-17T17:01:00Z", "2026-08-17T17:01:00Z",
                       reason=WHY_AUTHORITATIVE)]
        code, said = self.verify(rows)
        self.assertEqual(code, 1, said)
        self.assertIn("illegal transition (start) -> authoritative", said)

    def test_a_package_attempt_is_refused_by_this_verb(self):
        code, said = self.record(self.ledger(sound_rows()), PACKAGE_ONE,
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("this verb records a BATTERY cohort's evidence "
                      "disposition", said)

    def test_a_token_reason_is_refused(self):
        code, said = self.record(self.ledger(sound_rows()), HEAD_ONE,
                                 "--reason", "we used it")
        self.assertEqual(code, 1, said)
        self.assertIn("wants --reason", said)

    def test_an_attempt_of_another_lane_is_refused(self):
        rows = [dict(r) for r in sound_rows()]
        for row in rows:
            if row.get("attempt") == HEAD_ONE:
                row["lane"] = "V15"
        code, said = self.record(self.ledger(rows), HEAD_ONE,
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("belongs to lane V15", said)

    def test_an_unknown_attempt_is_refused(self):
        code, said = self.record(self.ledger(sound_rows()),
                                 "head-20260817T990000Z-99zzzzzz",
                                 "--reason", WHY_AUTHORITATIVE)
        self.assertEqual(code, 1, said)
        self.assertIn("carries no attempt", said)


class AbandonmentIsResolvedNotEvidence(Fixture):
    """RESOLVED, COUNTED, AND IN NO AUTHORITATIVE TALLY."""

    def test_an_abandoned_attempt_is_resolved_and_unevidenced(self):
        path = self.ledger(known_mix())
        code, said = self.run_checks("--verify-ledger", "--attempts", path,
                                     "--lane", LANE)
        self.assertEqual(code, 0, said)
        self.assertIn(f"{A06}: abandoned", said)
        self.assertIn("| evidence unevidenced", said)
        self.assertIn("with no terminal row 0", said)

    def test_it_is_counted_under_its_own_name_and_no_other(self):
        path = self.ledger(known_mix())
        code, said = self.run_checks("--history-table", "--lane", LANE,
                                     "--attempts-list", path)
        self.assertEqual(code, 0, said)
        self.assertIn("abandoned_count                       : 1", said)
        # NEVER FOLDED: not a failure, not a completion, not evidence.
        self.assertIn("failed_count                          : 2", said)
        self.assertIn("complete_count                        : 4", said)
        self.assertIn("authoritative_evidence_count          : 2", said)


class NineCounts(Fixture):
    """THE NINE, DERIVED, AND THE INVARIANTS JUDGED MECHANICALLY."""

    EXPECTED = {
        "attempt_count": 7,
        "terminal_execution_disposition_count": 7,
        "unresolved_count": 0,
        "reused_ordinal_count": 0,
        "failed_count": 2,
        "abandoned_count": 1,
        "complete_count": 4,
        "authoritative_evidence_count": 2,
        "set_aside_count": 2,
    }

    def table(self, rows, *extra):
        return self.run_checks("--history-table", "--lane", LANE,
                               "--attempts-list", self.ledger(rows), *extra)

    def test_every_count_is_derived_from_the_history(self):
        code, said = self.table(known_mix())
        self.assertEqual(code, 0, said)
        for name, value in self.EXPECTED.items():
            with self.subTest(count=name):
                self.assertIn(f"{name:<38}: {value}", said)

    def test_the_table_carries_both_axes_in_their_own_columns(self):
        code, said = self.table(known_mix())
        self.assertEqual(code, 0, said)
        self.assertIn("EXECUTION", said)
        self.assertIn("EVIDENCE", said)
        self.assertNotIn("DISPOSITION  REASON", said)
        for line in said.splitlines():
            if A03 in line and "complete" in line:
                self.assertIn("set-aside", line)
                break
        else:  # pragma: no cover - the assertion above is the test
            self.fail(f"no row for {A03} carrying both axes:\n{said}")

    def test_the_counts_move_with_the_history_rather_than_being_pinned(self):
        """NOT A TRANSCRIPTION. One more completed cohort and the figures
        change without anything in the tool being edited."""
        rows = known_mix()
        rows += [state("head-20260827T160000Z-08abcdef", 8, "head", "started",
                       "2026-08-27T16:00:00Z", "2026-08-27T16:00:00Z"),
                 terminal("head-20260827T160000Z-08abcdef", 8, "head",
                          "complete", "2026-08-27T16:00:00Z",
                          "2026-08-27T16:00:30Z")]
        code, said = self.table(rows)
        self.assertEqual(code, 0, said)
        self.assertIn("attempt_count                         : 8", said)
        self.assertIn("complete_count                        : 5", said)
        self.assertIn("terminal_execution_disposition_count  : 8", said)

    def test_the_invariants_pass_on_a_sound_history(self):
        code, said = self.table(known_mix())
        self.assertEqual(code, 0, said)
        self.assertIn("invariants: 3 of 3 PASS", said)
        self.assertIn("PASS  every attempt reaches exactly one terminal "
                      "execution disposition", said)

    def test_an_open_attempt_fails_the_invariant_that_should_fail(self):
        rows = known_mix()
        rows += [state("head-20260827T160000Z-08abcdef", 8, "head", "started",
                       "2026-08-27T16:00:00Z", "2026-08-27T16:00:00Z")]
        code, said = self.table(rows)
        self.assertEqual(code, 0, said)
        self.assertIn("FAIL  no attempt is left open", said)
        self.assertIn("unresolved_count 1 == 0", said)
        self.assertIn("FAIL  every attempt reaches exactly one terminal "
                      "execution disposition", said)
        self.assertIn("FAILING:", said)

    def test_assert_invariants_turns_the_report_into_a_gate(self):
        rows = known_mix()
        rows += [state("head-20260827T160000Z-08abcdef", 8, "head", "started",
                       "2026-08-27T16:00:00Z", "2026-08-27T16:00:00Z")]
        code, said = self.table(rows, "--assert-invariants")
        self.assertEqual(code, 1, said)
        self.assertIn("breaks 2 invariant(s)", said)

    def test_assert_invariants_is_silent_over_a_sound_history(self):
        code, said = self.table(known_mix(), "--assert-invariants")
        self.assertEqual(code, 0, said)
        self.assertIn("invariants: 3 of 3 PASS", said)

    def test_a_reused_ordinal_fails_its_own_invariant(self):
        rows = known_mix()
        rows += [state("head-20260827T160000Z-07abcdef", 7, "head", "started",
                       "2026-08-27T16:00:00Z", "2026-08-27T16:00:00Z"),
                 terminal("head-20260827T160000Z-07abcdef", 7, "head",
                          "complete", "2026-08-27T16:00:00Z",
                          "2026-08-27T16:00:30Z")]
        code, said = self.table(rows)
        self.assertEqual(code, 0, said)
        self.assertIn("FAIL  no ordinal is carried by two attempts", said)
        self.assertIn("reused_ordinal_count 1 == 0", said)

    def test_the_derivation_is_written_machine_readable(self):
        root = self.temp("history-json-")
        path = self.ledger(known_mix(), root)
        out = root / "derived" / "history.json"
        code, said = self.run_checks("--history-table", "--lane", LANE,
                                     "--attempts-list", path, "--json", out)
        self.assertEqual(code, 0, said)
        blob = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(blob["counts"], self.EXPECTED)
        self.assertEqual(blob["verdict"], "PASS")
        self.assertEqual(len(blob["attempts"]), 7)
        found = {one["attempt"]: one for one in blob["attempts"]}
        self.assertEqual(found[A03]["execution_disposition"], "complete")
        self.assertEqual(found[A03]["evidence_disposition"], "set-aside")
        self.assertEqual(found[A06]["execution_disposition"], "abandoned")
        self.assertEqual(found[A06]["evidence_disposition"], "unevidenced")
        self.assertEqual(found[A07]["evidence_disposition"], "authoritative")
        self.assertTrue(all(one["pass"]
                            for one in blob["invariants"].values()),
                        blob["invariants"])

    def test_the_json_records_a_failing_invariant_as_failing(self):
        root = self.temp("history-json-")
        rows = known_mix()
        rows += [state("head-20260827T160000Z-08abcdef", 8, "head", "started",
                       "2026-08-27T16:00:00Z", "2026-08-27T16:00:00Z")]
        path = self.ledger(rows, root)
        out = root / "history.json"
        code, said = self.run_checks("--history-table", "--lane", LANE,
                                     "--attempts-list", path, "--json", out)
        self.assertEqual(code, 0, said)
        blob = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(blob["verdict"], "FAIL")
        self.assertEqual(blob["counts"]["unresolved_count"], 1)


class SealedSummaryCarriesBothAxes(Fixture):
    """THE SHIPPED SUMMARY, ON BOTH AXES, WITH THE EXPLANATION FIELD."""

    def test_the_member_states_execution_and_evidence_separately(self):
        root = self.temp("seal-both-")
        package = root / "20260817T123000Z-catena-e1"
        logs = package / "logs"
        logs.mkdir(parents=True)
        (logs / "order-head.txt").write_text(
            f"PREFLIGHT battery=head\nattempt={HEAD_ONE}\n", encoding="utf-8")
        (logs / "order-parent.txt").write_text(
            f"PREFLIGHT battery=parent\nattempt={PARENT_ONE}\n",
            encoding="utf-8")
        rows = sound_rows()
        rows += [state(HEAD_ONE, 1, "head", "set-aside",
                       "2026-08-17T16:00:00Z", "2026-08-17T16:00:00Z",
                       reason=WHY_SET_ASIDE)]
        ledger = self.ledger(rows, root)
        code, said = self.run_checks(
            "--seal-ledger", "--package", package, "--attempts", ledger,
            "--attempt", PACKAGE_ONE, "--attempt-no", "3", "--lane", LANE,
            "--package-name", "20260817T123000Z-catena-e1",
            "--head", "1" * 40)
        if "cannot load the sealer" in said:
            self.skipTest("sanitize-and-seal.py is not loadable right now")
        self.assertEqual(code, 0, said)
        self.assertIn(f"{HEAD_ONE}: complete | evidence set-aside", said)
        shipped = json.loads(
            (logs / "attempts.json").read_text(encoding="utf-8"))
        mine = [one for one in shipped["attempts"]
                if one["attempt"] == HEAD_ONE][0]
        self.assertEqual(mine["execution_disposition"], "complete")
        self.assertEqual(mine["evidence_disposition"], "set-aside")
        self.assertEqual(mine["execution_reason"], "")
        self.assertIn("none of its figures", mine["evidence_reason"])
        # The explanation field a reader gets instead of inferring from a
        # disposition name is still there, and is still a sentence.
        self.assertIn("evidence", mine)
        self.assertTrue(mine["evidence"], mine)


if __name__ == "__main__":
    unittest.main(verbosity=2)
