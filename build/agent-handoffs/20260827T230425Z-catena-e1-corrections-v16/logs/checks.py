#!/usr/bin/env python3
"""Compose `checks.txt`, the log index and the packaged attempt ledger.

V6 wrote `checks.txt` by hand — every command, its exit and its result typed
out — and its review found five counts wrong across the package. This file is
the answer for that member specifically: the commands come from the ledgers
the batteries wrote as they ran, the exits come from the same lines, and the
headline result of each log is parsed out of the log rather than remembered.

The battery ledger also carries provenance emitted at run time — the exact
commit, the attempt identity, the `git status --porcelain` result, the cwd as
the `$REPO` token, and each entry's unique log path — and every block below
renders those fields FROM the ledger, so the transcript that claims a run's
commit is the transcript that recorded it.

THE V11 CORRECTION, ONE: TREE STATE IS PER COMMAND. V10 read the porcelain
result once, at preflight, and this file stamped that one answer onto every
row — `clean : clean` on the parent's `head-tests-against-parent` step, which
overwrites a TRACKED file, and on the step after it. The battery now records
`TREE-BEFORE:` and `TREE-AFTER:` on each entry and this renders THOSE. The
preflight and postflight readings are still rendered, once, at battery scope,
where they are true.

THE V11 CORRECTION, TWO: THE INDEX IS DERIVED. `logs/LOG-INDEX.md` is written
here, from the ledgers and from the logs directory itself: every log, the
attempt that produced it, its slug, its order and its exit. It is a document
so that the consistency audit reads it, which is also what makes every log
this package ships a NAMED member rather than an unreferenced one.

THE V11 CORRECTION, THREE: THE ATTEMPT LEDGER SHIPS. The batteries and the
assembly append machine-readable rows to an append-only ledger OUTSIDE the
package, so it can span attempts. The rows belonging to the attempts this
package was built from are copied in as `logs/attempts.json` -- by
`--seal-ledger` at P5, see below, not by the P1 pass that composes checks.txt.
A step row states what a step did; the terminal row of its attempt carries its
one disposition and its one reason, and this resolves the two so no row can be
read as both.

A LOGS DIRECTORY CARRYING A DISCARD MARKER IS REFUSED. A discarded battery
drops one into its own logs directory; a package composed from it would be a
package whose figures came from a run its own record calls non-evidence.

THE V12 CORRECTION, ONE: THE ATTEMPT-LOG AUDIT (`--audit-logs`). V11 gave the
battery logs an attempt ordinal and gave the package-phase transcripts none, so
`logs/gate-comparison.log` was claimed by six attempts in the reviewed package
and `logs/sealer-tests.log` by five, and nothing anywhere compared the ledger's
`log=` values against the transcripts on disk. Every transcript now lives under
`logs/attempt-NN/`, and this audits both directions of that: a row whose log
escapes its own attempt's root, two rows claiming one path, a zero-byte
transcript nobody explained, and a transcript on disk that no row claims are
each a refusal. It writes nothing, so `assemble.sh` can run it after the freeze.

THE V12 CORRECTION, TWO: THE AUTHORITY AUDIT AND THE LATE LEDGER WRITE
(`--seal-ledger`). The reviewed package shipped `logs/attempts.json` marking
THREE attempts `authoritative` -- both batteries and a superseded package
attempt -- while the package it shipped inside carried "unresolved: the ledger
carries no terminal row for this attempt". Two causes, both answered here:

  * ONE WORD FOR TWO FACTS. A battery terminates `complete` or `failed`;
    `sealed` is a package attempt's word and at most one package attempt may
    hold it. (V13 narrowed the package word further -- see the vocabulary
    block below: what V12 called `authoritative` in package bytes is `sealed`,
    and `authoritative` moved to the external post-P8 record.) The state
    machine is written out once, in `assemble.sh`'s header;
    `audit_authority()` below is its executable copy and there is no third
    statement of it.
  * THE MEMBER WAS WRITTEN BEFORE THE FACT IT REPORTED. `logs/attempts.json` is
    no longer written by the P1 pass at all. It is a DECLARED DERIVED MEMBER,
    written by `--seal-ledger` after the consistency audit and immediately
    before the manifest, from a ledger that by then carries the sealing
    attempt's own terminal row. It is pre-normalized on the way out, exactly as
    `claims.json` is, because nothing normalizes the tree after the freeze.

The one thing it does not do is judge. A `check-only` line here says what the
command printed; whether the result is acceptable is argued in the documents,
which is where a judgement belongs.

THE V13 CORRECTION: THE LEDGER IS A LANE'S, ORDINALS ARE SPENT ONCE, AND EVERY
ATTEMPT ENDS OUT LOUD. V12's `next_attempt_no()` computed `max(attempt_no) + 1`
over whatever file it was pointed at. The operator started a fresh ledger
partway through the lane, so ordinals 03/04/05/06 were reissued as 03/04/05
while `PROVENANCE.md` claimed "an ordinal is allocated once for the whole
lane"; four discarded package attempts and four set-aside battery cohorts are
in no surviving ledger, and three shipped members assert they are. Four
answers, all here:

  * A LEDGER NAMES ITS LANE, on a `record=lane` row and again on every row.
    `--allocate-ordinal` refuses to append on another lane's behalf and
    refuses `--fresh` over an existing file, so starting over is loud.
  * AN ORDINAL IS SPENT BY ANY ROW THAT EVER CARRIED IT, however that attempt
    ended. `--allocate-ordinal` is the only allocator and `battery.sh` calls
    it rather than recomputing a maximum.
  * EVERY ATTEMPT REACHES EXACTLY ONE TERMINAL DISPOSITION, and every state
    that is not `complete`, `sealed` or `authoritative` carries a NON-EMPTY
    reason -- on its row and in the shipped summary, V12 shipped it blank.
    `set-aside` is the new word for a battery that completed and whose figures
    were not used; without it those cohorts had no honest state and were
    deleted instead.
  * CHRONOLOGY IS CHECKABLE. Rows of an attempt are in time order, no row ends
    after the instant `logs/attempts.json` is frozen at -- a real timestamp
    now, not a sentence -- and an attempt id's embedded minting instant must
    agree with the attempt's own first row.

Usage:
    checks.py --package DIR --head SHA --parent SHA --attempt-no NN
              [--measured SHA] [--attempts LEDGER.jsonl] [--attempt ID]
    checks.py --audit-logs --package DIR --attempts LEDGER.jsonl
              --attempt ID --attempt-no NN
    checks.py --seal-ledger --package DIR --attempts LEDGER.jsonl
              --attempt ID --attempt-no NN --package-name NAME --head SHA
              [--lane LANE]
    checks.py --allocate-ordinal --attempts LEDGER.jsonl --lane LANE
              [--propose NN] [--fresh]
    checks.py --verify-ledger (--attempts LEDGER.jsonl | --package DIR)
              [--lane LANE] [--frozen-at INSTANT]
    checks.py --history-table --attempts-list A.jsonl [--attempts-list B.jsonl]
              [--lane LANE] [--json OUT] [--assert-invariants]
              [--claim-append-only]
    checks.py --set-aside-attempt ID --attempts LEDGER.jsonl --lane LANE
              --reason WHY
    checks.py --authoritative-evidence ID --attempts LEDGER.jsonl --lane LANE
              --reason WHY
    checks.py --abandon-attempt ID --attempts LEDGER.jsonl --lane LANE
              --reason WHY

TWO AXES, NEVER ONE. `--set-aside-attempt` and `--authoritative-evidence` are
the two answers to ONE question -- what became of a completed attempt's
measurements -- and neither touches the terminal row that says how the attempt
ended. `--abandon-attempt` is on the other axis entirely: it is a terminal
EXECUTION disposition for a run something outside it stopped.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

# THE COMMAND SCHEMA AND ITS CLASSIFIER, IMPORTED RATHER THAN RESTATED.
# `checks.py` composes the rows, `handoff-inventory.py` re-derives their
# verdicts and `replay-command.py` executes them; all three read this one
# module, so a row cannot be called executable by one and refused by another.
# NO BYTECODE, EVER, AND THIS IS NOT HOUSEKEEPING.
#
# `assemble.sh` runs `$PKG/logs/checks.py` at P5 -- AFTER the P3 freeze and
# BEFORE the P6 manifest -- and the import below would write
# `$PKG/logs/__pycache__/catena_command.cpython-3NN.pyc` into the tree that is
# about to be sealed. The manifest would then cover a binary member, and the
# archive's strict-UTF-8 check would refuse the package it just produced.
# Nothing imported across files in this anchor before V16, so this hazard did
# not exist and there was nothing guarding against it.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import catena_command as CC  # noqa: E402

# `--seal-ledger` loads the sealer that ships beside this tool, and an import
# writes bytecode. A `__pycache__` inside the package after the freeze is an
# undeclared member and the P5 audit hard-fails on it.
sys.dont_write_bytecode = True

# The line each suite or check reports itself by. First match wins, and a log
# that matches none is reported as such rather than summarised into silence.
HEADLINES = (
    re.compile(r"^Ran \d+ tests? in [\d.]+s$", re.M),
    re.compile(r"^(?:OK|FAILED)(?: \(.*\))?$", re.M),
    re.compile(r"^Promised-deliverable ledger .*$", re.M),
    re.compile(r"^catena (?:valid|invalid).*$", re.M),
    # `stale:` only where staleness is what the command reports. Full
    # discovery's own log carries such a line from a test that exercises the
    # binding checker, and a row headed by it reads as though the suite had
    # reported binding staleness.
    ("release-bindings", re.compile(r"^stale: .*$", re.M)),
    re.compile(r"^catena\.\w+ whole \d+ stripped \d+$", re.M),
    re.compile(r"^replay-examples: .*$", re.M),
    re.compile(r"^catena\.\w+ whole \d+ stripped \d+$", re.M),
)

# The members a LATER pipeline phase writes. They are named in the index as
# declarations, exactly as `assemble.sh` declares them deferred, because the
# index is composed at P1 and these do not exist yet. `{log_root}` is the
# ASSEMBLY attempt's own root -- the transcripts below belong to one attempt,
# and V11 wrote all five to fixed paths under `logs/` that every rerun opened.
DEFERRED_LOGS: tuple[tuple[str, str], ...] = (
    ("{log_root}/sealer-tests.log", "P1: the sealer's own test suite"),
    ("{log_root}/seal.log", "P2: every normalization pass, appended"),
    ("{log_root}/seal-check.log",
     "P2: the check-only pass that closed the fixpoint"),
    ("{log_root}/derive-claims.log", "P4: the derivation, as it printed"),
    ("{log_root}/head-consistency.log", "P5: the consistency audit"),
    ("logs/attempts.json",
     "P5: the attempt rows this package was built from, composed after the "
     "consistency audit so it carries the sealing attempt's own terminal row"),
)

# A log ROOT and one transcript inside it. Exactly one level: a transcript
# nested deeper is not addressed by any rule here and would slip both
# directions of the audit.
ATTEMPT_LOG = re.compile(r"^logs/attempt-(\d{2})/[^/]+$")
ATTEMPT_ROOT_NAME = re.compile(r"^attempt-\d{2}$")

# AN ATTEMPT ID CARRIES ITS OWN MINTING INSTANT, and V12 proved that is not a
# decoration: the final attempt's id embedded a timestamp 2m25s LATER than its
# own last row and 54s later than the evidence commit, which is only possible
# if the id and the rows came from different runs or the id was typed. The id
# is minted at process start, BEFORE the preflight, so it must not postdate the
# attempt's first row by more than the clock resolution, and it must not
# predate it by more than the preflight can plausibly take.
ATTEMPT_ID = re.compile(
    r"^(head|parent|package)-(\d{8}T\d{6}Z)-(\d{2})([a-z0-9]{6})$")
# THE TOLERANCES, AND WHY THESE NUMBERS.
#
#   LAG (id later than the first row) -- 5s. The id is minted before anything
#   is recorded, so in a sound run this difference is NEGATIVE. Five seconds is
#   the allowance for a coarse clock and for a `date` call landing either side
#   of a second boundary; it is not an allowance for work. V12's 145-second
#   forward skew is refused by an order of magnitude.
#
#   LEAD (id earlier than the first row) -- 600s. Between minting and the first
#   recorded row a battery runs `git rev-parse` and two `git status --porcelain`
#   readings, and an assembly stages a package tree. Ten minutes is roughly two
#   orders of magnitude more than any preflight observed in this lane, so it
#   refuses an id transplanted from an EARLIER run without ever refusing a slow
#   preflight.
ID_LAG_MAX_SECONDS = 5
ID_LEAD_MAX_SECONDS = 600

# Records that live at the TOP of `logs/` by design, and why each one does.
# Everything else under `logs/` that is a transcript belongs to exactly one
# attempt and therefore to exactly one root.
SCOPE_RECORDS: tuple[tuple[str, str], ...] = (
    ("logs/order-head.txt", "the head battery's ordering ledger"),
    ("logs/order-parent.txt", "the parent battery's ordering ledger"),
    ("logs/attempts.json", "the packaged attempt rows, which span attempts"),
)
DISCARD_MARKER = re.compile(r"^logs/DISCARDED-[^/]+\.txt$")

# THE ATTEMPT STATE MACHINE, as transitions. `assemble.sh`'s header states it
# in prose, once; this is the executable copy and the toolchain keeps no third.
# A missing predecessor is the empty string: the ledger is append-only and a
# reader may be handed a slice of it, so entering at any state is allowed and
# what is refused is a transition that goes backwards or sideways.
#
# THE V16 CORRECTION: TWO AXES, NEVER ONE. Until V16 this table carried
# `"complete": ("set-aside",)`, which said that setting a cohort aside is a
# TRANSITION OF THE EXECUTION MACHINE -- `complete -> set-aside`. It is not.
# How an attempt terminated and whether a completed attempt's measurements
# remain authoritative are two different facts about two different things, and
# a single table over both is the same "one word for two facts" defect that
# made V11's authoritative count uncountable, one level down. Read through the
# collapsed table, `--history-table` and `--verify-ledger` printed `set-aside`
# for an attempt whose execution disposition is `complete`, so the record could
# not say that the battery ran to completion and that its figures were declined
# at the same time -- which is exactly what happened.
#
#   EXECUTION DISPOSITION -- how the attempt itself terminated. Terminal,
#   irreversible, EXACTLY ONE per attempt, carried by the one `record=attempt`
#   row: `complete`, `failed`, `abandoned` for a battery; `sealed`,
#   `discarded` for a package attempt.
#
#   EVIDENCE DISPOSITION -- whether a COMPLETED attempt's measurements remain
#   authoritative. Only meaningful for an attempt that terminated `complete`
#   (battery) or `sealed` (package); carried by a later `record=state` row:
#   `authoritative`, `set-aside`, `superseded`, and `unevidenced` for the
#   attempt that has none.
#
# THE ON-DISK SHAPE IS UNCHANGED. An evidence disposition is still one
# `record=state status=<word>` row with its one NON-EMPTY reason, appended
# after the terminal row and leaving it exactly where it is. This is a
# REINTERPRETATION of rows already written, not a rewrite of them: every ledger
# that validated before V16 validates now.
#
# `failed` and `abandoned` attempts are `unevidenced`, always, and no verb will
# set an evidence disposition on one -- there is no measurement to decline or
# to carry, and applying the softer word would cover what the disposition says.
#
# `abandoned` is a first-class TERMINAL EXECUTION disposition, and it is NOT
# `failed`. A battery fails when a step it ran returns non-zero, or when one of
# its own guards refuses: in both cases the run reached a decision and the
# record can name the step that made it. A battery is ABANDONED when something
# outside it stopped it -- a killed process, a lost handle, an operator
# interrupt -- and no step failed at all. V15 had one such attempt, three green
# steps and no disposition, and it is unresolved to this day, because the
# vocabulary could express the absence of a row but not the fact the absence
# stood for. Collapsing it into `failed` would assert a decision nothing made;
# leaving it out is what the review refused.
BATTERY_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "complete", "failed", "abandoned"),
    "started": ("complete", "failed", "abandoned"),
    "complete": (),
    "failed": (),
    "abandoned": (),
}
# THE V13 CORRECTION, PACKAGE SIDE: `sealed`, NOT `authoritative`. NO SEALED
# PACKAGE BYTES MAY CLAIM FINAL AUTHORITY BEFORE P8. Every row that reaches
# `logs/attempts.json` is written at or before P5, and the member is frozen
# there because P6 hashes it -- so a row inside the package asserting
# `authoritative` is asserting the outcome of three phases that had not run
# when it was written. V12 did exactly that, and its own package then carried a
# P8 verdict nobody had. The most a package attempt may claim ABOUT ITSELF, in
# bytes it ships, is that it is `sealed`: the directory is complete, normalized
# and about to be manifested. That claim is true when it is made.
#
# `authoritative` survives, in one place only: the EXTERNAL complete ledger,
# where it is appended AFTER P8 passes, as a post-terminal `record=state` row,
# alongside the `<package>.authority.json` sidecar bound to the final ZIP. It
# is therefore never a terminal disposition on either side, and never a state
# an in-package record may carry.
# `abandoned` IS A PACKAGE STATE TOO, for the reason it is a battery state. An
# assembly stopped from outside -- a killed process, a lost handle, an operator
# interrupt -- reached no decision of its own: no phase refused it and no gate
# failed. `discarded` asserts the pipeline decided, which is exactly the
# distinction the battery axis was given `abandoned` to preserve, and the
# argument does not change because the attempt builds a package rather than
# measuring an endpoint. V16 found this the way it found the battery case:
# an assembly of this lane was stopped during P2 and the only terminal word
# available would have claimed a refusal that never happened.
PACKAGE_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "sealing", "sealed", "discarded", "abandoned"),
    "started": ("sealing", "sealed", "discarded", "abandoned"),
    "sealing": ("sealed", "discarded", "abandoned"),
    "sealed": (),
    "discarded": (),
    "abandoned": (),
}
# Retained under its old name so no caller has to learn a second one, and
# equal to the table above because THE EXECUTION MACHINE IS THE SAME IN BOTH
# SCOPES. What used to distinguish it -- `sealed -> authoritative` -- was never
# an execution transition at all; it is the package's EVIDENCE axis, below.
EXTERNAL_PACKAGE_STATES: dict[str, tuple[str, ...]] = dict(PACKAGE_STATES)

# THE EVIDENCE AXIS, PER SIDE, AS ITS OWN MACHINE. The empty string is "no
# evidence disposition recorded", which reads `unevidenced`.
#
# A BATTERY'S EVIDENCE AXIS HAS THE SAME ONE SUCCESSION THE PACKAGE AXIS HAS,
# and for the same reason. A cohort's figures are carried or they are declined,
# once; `set-aside` is terminal, `authoritative` cannot follow it, and no
# second row of either kind is admitted. What a cohort that WAS authoritative
# may become is SUPERSEDED, when a later cohort measures the same endpoint and
# the package carries that one instead.
#
# V16 found the case in its own run, and found it the hard way. Cohorts 04 and
# 07 were recorded authoritative as soon as they completed -- before any
# package had been sealed from them. P8 then refused the archive because those
# cohorts had executed `battery.sh` at one digest while the package shipped
# another: what ran was not what shipped. The endpoints had to be measured
# again, and the ledger correctly refused to reopen an evidence disposition,
# leaving no way to say what had plainly happened.
#
# Refusing the succession would leave deleting the predecessor's row as the
# only remedy, which is the V12 defect this protocol exists to refuse rather
# than the cure for it. `superseded` says the true thing: those cohorts were
# authoritative, they were replaced, and the record shows both. The lesson the
# package states beside it is that `authoritative` belongs AFTER a seal proves
# the cohort's tools are the shipped ones, not at the moment a battery ends.
BATTERY_EVIDENCE_STATES: dict[str, tuple[str, ...]] = {
    "": ("authoritative", "set-aside"),
    "authoritative": ("superseded",),
    "set-aside": (),
    "superseded": (),
}
# A PACKAGE ATTEMPT'S EVIDENCE AXIS HAS EXACTLY ONE SUCCESSION, and it is the
# one V12 tried to solve by deletion: a package that really did pass P8, really
# was authoritative, and was then replaced is SUPERSEDED. Refusing that
# succession would leave deleting the predecessor's history as the only
# remedy, which is the defect, not the cure. Nothing else moves.
PACKAGE_EVIDENCE_STATES: dict[str, tuple[str, ...]] = {
    "": ("authoritative", "superseded"),
    "authoritative": ("superseded",),
    "superseded": (),
}
# The execution disposition an evidence disposition may be recorded against,
# per side. `failed`, `abandoned` and `discarded` are absent by construction:
# they measured nothing that could be carried or declined.
EVIDENCE_FOLLOWS: dict[str, str] = {"battery": "complete",
                                    "package": "sealed"}
# The word for an attempt with no evidence row. It is never written to a row --
# the absence IS the state -- and it is what `failed` and `abandoned` attempts
# read as, permanently.
EVIDENCE_UNSET = "unevidenced"
EVIDENCE_DISPOSITIONS = frozenset({"authoritative", "set-aside", "superseded",
                                   EVIDENCE_UNSET})
# The one disposition an attempt is allowed, and the row kind that carries it.
# No evidence word is here: an evidence disposition arrives after the attempt
# already terminated, so it can never be the terminal row, in either scope.
TERMINAL_STATES = frozenset({"complete", "failed", "sealed", "discarded",
                             "abandoned"})
# The evidence words that are actually WRITTEN to a row. Kept under the old
# name because the reason rule below and three other modules read it: they are
# post-terminal in the sense that matters to those readers -- they arrive after
# the terminal row and are carried by `record=state`, never by `record=attempt`
# -- and `unevidenced` is excluded because no row ever states it.
POST_TERMINAL_STATES = frozenset({"superseded", "set-aside", "authoritative"})
# NOT A STATE, IN EITHER AXIS. §10: attempts 01-02 of lane V16 were described
# in passing as "refused", and their execution disposition is `failed` with
# "guard refusal" as the CAUSE, recorded in the reason. A guard refusal is a
# cause, never a disposition; there is no `refused` state and this names the
# words that would introduce one so the audit can say so in those terms.
NOT_A_DISPOSITION: dict[str, str] = {
    "refused": "failed",
    "refusal": "failed",
    "refusing": "failed",
}
# The states that mean "this went as intended". Everything else that an attempt
# can END on -- terminal or post-terminal -- must say why, in words, on the row
# that states it AND in the summary the package ships. V12 shipped all five
# `attempts[]` reasons empty, two of them supersessions, with the reasons
# living only on separate state rows nobody joined.
SUCCESSFUL_STATES = frozenset({"complete", "sealed", "authoritative"})
# RESOLVED, AND NEVER EVIDENCE. `abandoned` is terminal -- it closes an
# attempt's history and the audit counts it resolved -- and it is never a
# result. Nothing an abandoned attempt measured may support a claim, because
# the run did not finish measuring; the reason row says what stopped it and
# the figures, if any were written before it stopped, belong to no total.
# Kept as its own name rather than folded into `failed`, `discarded` or
# `set-aside`, each of which asserts something this does not.
UNEVIDENCED_STATES = frozenset({"abandoned"})
# EVERY EXECUTION DISPOSITION THAT CAN NEVER CARRY EVIDENCE. `abandoned` above
# is the one the audit narrates; this is the whole set, and it is what the
# evidence axis reads to answer `unevidenced` permanently rather than
# provisionally. An attempt here is RESOLVED -- its history is closed and the
# audit counts it -- and it is never successful and never authoritative.
NEVER_EVIDENCE = frozenset({"failed", "abandoned", "discarded"})
REASONED_STATES = (TERMINAL_STATES | POST_TERMINAL_STATES) - SUCCESSFUL_STATES
BATTERY_SIDES = frozenset({"head", "parent"})

# THE TWO SCOPES A LEDGER CAN BE READ IN, and the only difference between them.
# `in-package` is the record that ships frozen at P5; `external` is the
# append-only complete ledger that outlives every package and is the only place
# a post-P8 verdict may be written.
IN_PACKAGE, EXTERNAL = "in-package", "external"

# THE LANE IDENTITY ROW. The first row of a lane ledger declares the lane, and
# every row after it repeats it. V12's operator started a fresh ledger file
# partway through the lane, so ordinals 03/04/05/06 were reissued as 03/04/05
# while `PROVENANCE.md` claimed "an ordinal is allocated once for the whole
# lane"; four discarded package attempts and four set-aside battery cohorts are
# in no surviving ledger at all. A ledger that names its lane, and tools that
# refuse to append to a ledger of a DIFFERENT lane or to open a fresh one over
# an existing one, make starting over something an operator must do out loud.
LANE_RECORD = "lane"

# The terminal row a ledger FILE carries about itself when it is retired. It is
# defined here, beside the lane row, because the two are the same KIND of row:
# both are statements about the file rather than about an attempt in it.
RETIRED_RECORD = "retired"

# THE ROWS THAT ARE ABOUT THE FILE, NOT ABOUT AN ATTEMPT.
#
# V16, THE COMMAND-REPLAY LANE, IN PASSING: `--verify-ledger` reported `a row
# names no attempt` on every retired ledger this toolchain has ever produced,
# because §5 of the audit buckets rows by attempt id and faulted the empty
# bucket. The `record=retired` row `--retire-ledger` appends has no attempt id
# and must not: it says the FILE stops here, carrying the file's digest, byte
# count, row count and spent ordinals. Demanding an attempt id of it is
# demanding that a statement about a file name an attempt it is not about, and
# the audit faulted a row its own retirement verb wrote one line earlier.
#
# A row of any OTHER kind with no attempt is still a fault, and that is the
# fault §5 exists for: a `step` or a `state` row must say which attempt it
# belongs to or the ledger cannot be read.
FILE_SCOPED_RECORDS = frozenset({LANE_RECORD, RETIRED_RECORD})

# The phases that run AFTER `logs/attempts.json` is frozen and therefore cannot
# be in it. V12 shipped a member that stopped at P5 and said nothing about it,
# so a reader could not tell "no P6 row exists" from "P6 never ran". Declared,
# now, by name.
PHASES_AFTER_FREEZE: tuple[tuple[str, str], ...] = (
    ("P6", "the manifest pass; it runs after this member is frozen, because "
           "this member is one of the files it hashes"),
    ("P7", "the archive; it runs on the sealed directory and its identity is "
           "in the out-of-package sidecar, not in a member it contains"),
    ("P8", "the final verification; its verdict is in the out-of-package "
           "verification transcript, for the same reason"),
)

# Files under `logs/` that are not logs at all, described so the index can
# account for every member of the directory without calling a tool a
# transcript.
ROLES: tuple[tuple[str, str], ...] = (
    (".py", "the pipeline tool itself, shipped so the package is replayable"),
    (".sh", "the pipeline script itself, shipped so the package is replayable"),
    (".mjs", "a harness shipped with the package"),
)


def ledger(path: Path) -> tuple[dict, list[dict]]:
    """One ledger, as the provenance and the rows it recorded.

    A COMMAND MAY BE MORE THAN ONE LINE, and one of them is: the gzip
    measurement is a `python3 -c "…"` with a real program inside it. Recording
    it on one line would mean recording something other than what ran, so the
    ledger keeps it exact and this reads from `CMD:` to the `exit=` sentinel.
    Rewriting the command to suit the reader would be the reader deciding what
    the record says.

    The provenance comes from the PREFLIGHT/POSTFLIGHT sections the battery
    emits as it runs: the commit, the attempt, the porcelain result, the cwd
    token, and the drift verdict. The PER-COMMAND tree readings come from the
    rows, where the battery took them. Nothing here re-derives anything; the
    ledger is the record.
    """
    meta: dict = {}
    if not path.is_file():
        return meta, []
    rows: list[dict] = []
    stamp = ""
    section = ""
    collecting = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if collecting:
            # `CMDJSON:` CLOSES THE COMMAND AS SURELY AS `exit=` DOES. It is
            # written by `battery.sh` on the line after `CMD:`, and folding it
            # into a multi-line command would put the machine-readable record
            # inside the human-readable one.
            if line.startswith("CMDJSON: "):
                collecting = False
                if rows:
                    rows[-1]["exec_raw"] = line[len("CMDJSON: "):]
            elif line.startswith("exit="):
                collecting = False
                if rows:
                    rows[-1]["exit"] = line[5:]
            elif rows:
                rows[-1]["command"] += "\n" + raw
            continue
        if re.match(r"^\d{4}-\d\d-\d\dT", line):
            stamp = line
        elif line.startswith("PREFLIGHT "):
            section = "pre"
        elif line.startswith("POSTFLIGHT "):
            section = "post"
        elif line.startswith("sha="):
            meta["end_sha" if section == "post" else "sha"] = line[4:]
        elif line.startswith("porcelain="):
            # SECTION-AWARE. The preflight reading and the postflight reading
            # are two different facts about two different instants, and the
            # V10 defect began with storing them in one field.
            meta["end_porcelain" if section == "post" else "porcelain"] = \
                line[len("porcelain="):]
        elif line.startswith("attempt-no="):
            meta["attempt_no"] = line[len("attempt-no="):]
        elif line.startswith("expect-sha="):
            # THE COMMIT THE CALLER SAID THIS BATTERY MEASURES. Rendered beside
            # the commit the checkout actually held, because V12 recorded only
            # the second and compared it to nothing.
            meta["expect"] = line[len("expect-sha="):]
        elif line.startswith("lane="):
            meta["lane"] = line[len("lane="):]
        elif line.startswith("attempt="):
            meta["attempt"] = line[len("attempt="):]
        elif line.startswith("log-prefix="):
            meta["prefix"] = line[len("log-prefix="):]
        elif line.startswith("log-root="):
            meta["root"] = line[len("log-root="):]
        elif line.startswith("log-naming="):
            meta["naming"] = line[len("log-naming="):]
        elif line.startswith("cwd="):
            meta["cwd"] = line[len("cwd="):]
        elif line.startswith("build-state="):
            # V16: THE COLD/WARM READING THE BATTERY TOOK. `check-examples`
            # reports more divergent rows on a cold `build/` than on a warm
            # one, so the divergence figure an attempt records is a property
            # of the tree it ran against as well as of the head. The battery
            # reads it; this renders it, where a reader meets the figure.
            meta["build_state"] = line[len("build-state="):]
        elif line.startswith("build-state-note="):
            meta["build_state_note"] = line[len("build-state-note="):]
        elif line.startswith("root="):
            # THE ROOT VARIABLE DEFINITIONS, ONE PER LINE, AS THE BATTERY
            # EXPORTED THEM. V15's rows named `$WORKSPACE` and `$REPO` and no
            # member of the package said what either was; worse, `$REPO` meant
            # the parent checkout on one line of a row and the candidate
            # checkout on the next. These lines are the definitions, they are
            # written at run time, and `commands.json` carries them.
            name, _, meaning = line[len("root="):].partition(" ")
            meta.setdefault("roots", {})[name] = meaning
        elif line.startswith("sha-drift="):
            meta["drift"] = line[len("sha-drift="):]
        elif line.startswith("REFUSED "):
            meta.setdefault("refused", []).append(line[len("REFUSED "):])
        elif line.startswith("DISCARDED "):
            meta["discarded"] = line[len("DISCARDED "):]
        elif line.startswith("discard-reason="):
            meta["discard_reason"] = line[len("discard-reason="):]
        elif line.startswith("START "):
            rows.append({"slug": line[6:], "start": stamp})
        elif line.startswith("ORDER: ") and rows:
            rows[-1]["order"] = line[len("ORDER: "):]
        elif line.startswith("LOG: ") and rows:
            rows[-1]["log"] = line[5:]
        elif line.startswith("TREE-BEFORE: ") and rows:
            rows[-1]["tree_before"] = line[len("TREE-BEFORE: "):]
        elif line.startswith("TREE-AFTER: ") and rows:
            rows[-1]["tree_after"] = line[len("TREE-AFTER: "):]
        elif line.startswith("CMD: ") and rows:
            rows[-1]["command"] = line[5:]
            collecting = True
        elif line.startswith("CMDJSON: ") and rows:
            rows[-1]["exec_raw"] = line[len("CMDJSON: "):]
        elif line.startswith("exit=") and rows:
            rows[-1]["exit"] = line[5:]
        elif line.startswith("END ") and rows:
            rows[-1]["end"] = stamp
    return meta, rows


def headline(log: Path, slug: str = "") -> list[str]:
    if not log.is_file():
        return ["(no log)"]
    text = log.read_text(encoding="utf-8", errors="replace")
    # A REPORT IS READ AS A REPORT. The browser gate's stdout is its whole JSON
    # report, and scraping it for lines that look like counts returns every
    # per-check tally in it — twenty-six numbers where the reader wants the
    # seven the tool itself calls the totals.
    if log.suffix == ".json":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as error:
            return [f"(not valid JSON: {error})"]
        counts = data.get("counts") or data.get("totals") or {}
        if counts:
            return [", ".join(f"{k} {v}" for k, v in sorted(counts.items()))]
        return ["(a JSON report stating no counts)"]
    said = []
    for pattern in HEADLINES:
        if isinstance(pattern, tuple):
            owner, pattern = pattern
            if slug != owner:
                continue
        for found in pattern.findall(text):
            line = found.strip().strip(",")
            if line and line not in said:
                said.append(line)
    return said or ["(no headline line matched; read the log)"]


# THE PLACEHOLDER AND HEAD TABLES MOVED TO `catena_command.py`.
#
# They were here, and being here is how they came to be applied to a question
# they do not answer. `PLACEHOLDER` decides whether a row is ELIDED, which is
# a true and useful thing to say about `assemble.sh`'s PKG/ZIP/TOOLS rows.
# `COMMAND_HEADS` decided whether a row was "the exact string handed to the
# shell; re-runnable", which it never could: a first token proves nothing
# about a working directory, an environment, or a quote three tokens later.
# Both now live beside the validator that reads them, alongside the
# expandability, prose, argv and root-definition tests V15 had none of. See
# `catena_command.PLACEHOLDER` and `catena_command.COMMAND_HEADS`.
PLACEHOLDER = CC.PLACEHOLDER
COMMAND_HEADS = CC.COMMAND_HEADS


def command_fidelity(text, record=None, defined=None) -> tuple[str, str]:
    """The verdict for one recorded command. Delegated, not restated.

    V15 OWNED THIS TEST HERE AND IT WAS WRONG HERE. The whole of the judgement
    was `first.startswith(COMMAND_HEADS)`, which accepts `format`,
    `installing` and `zipcode` as commands and accepts `python3 would be run
    here to check the tree` as "the exact string handed to the shell;
    re-runnable". Seven rows shipped under that label carrying single-quoted
    `$WORKSPACE` and `$REPO` anchors that no shell expands.

    The test now lives in `catena_command.py`, which is also what
    `handoff-inventory.py` and `replay-command.py` read, so a row cannot be
    called executable by the composer and non-executable by the checker. This
    wrapper exists so the two call sites below read the same as they did.

    DETERMINISM IS UNCHANGED. `catena_command` probes nothing: its head table
    is a literal tuple and its membership test is exact, so `checks.txt`
    re-composes byte-identically off-host exactly as V15 required.
    """
    return CC.classify(text, record, defined=defined)


def exec_of(row: dict):
    """The exec record a ledger row carries, or None.

    A row written by a pre-V16 battery has no `CMDJSON:` line and gets None,
    which classifies as ELIDED or PROSE -- honest about not being replayable
    -- rather than as EXECUTABLE. A malformed one is surfaced as a record that
    fails validation, never silently dropped: a record nobody can parse is a
    fault to report, not an absence.
    """
    # `exec_raw` is the battery ledger's `CMDJSON:` line; `exec_record` is
    # the attempt-ledger field `assemble.sh` writes for a pipeline row. One
    # reader for both, so a pipeline row and a battery row are held to the
    # same standard.
    raw = row.get("exec_raw") or row.get("exec_record")
    if not raw:
        return None
    try:
        record = CC.parse_record(raw)
    except CC.ExecProblem:
        return {"schema": "(unparsable)", "raw": raw}
    # `uses` IS DERIVED HERE TOO, FROM THE RECORD, NOT CARRIED FROM THE LINE.
    #
    # Every row in the shipped ledgers was written before `make_record`
    # derived it, so all 23 carry `uses: []` while using two and three roots
    # apiece. The field is a function of the record's own cwd, argv or shell
    # and env, so this pass recomputes it rather than shipping the ledger's
    # empty one -- the same principle as every other figure in this member:
    # derived where it is rendered, never restated.
    #
    # A record that fails validation keeps whatever it carried, and the
    # classifier below refuses it by name. In particular a record that
    # DECLARES a `uses` disagreeing with its own command raises
    # `misdeclared-uses` here, the assignment is skipped, and the row ships
    # NON-EXECUTABLE with the disagreement stated -- rather than being quietly
    # corrected into agreement by this line.
    try:
        record["uses"] = CC.validate(record, defined=set(CC.ROOT_VARS))
    except CC.ExecProblem:
        pass
    return record


def command_line(row: dict, record) -> tuple[str, str]:
    """The `command :` line for one row, and the disagreement if there is one.

    V16, THE COMMAND-REPLAY LANE, F3. Two comments in this file said the
    `command :` line was rendered from the exec record by
    `catena_command.render_shell` and therefore "cannot disagree" with it.
    `render_shell` had NO CALL SITE HERE: the line was emitted verbatim from
    the ledger's `CMD:` string, and the two did disagree, on both
    `browser-gate` rows, which ship the string without the
    `TRIPTYCH_CHROME=...` assignment the record's `env` carries. On this host
    the gate falls back to the same binary and nothing broke; on a host whose
    browser is elsewhere the shipped line fails where the record works. That
    is the defect class this whole file exists to correct -- a fact asserted
    in prose that a tool could derive, with no gate comparing the two.

    So it is derived now, and the ledger's own string is CHECKED against the
    derivation rather than discarded. Two renderings are legitimate, because
    two writers produce them:

      * `render_shell(record)` -- what `run_argv` hands to `run()` and what
        `assemble.sh` composes for a package-phase row;
      * `render_shell(record, env=False)` -- what `run()` logs for a
        shell-form step, whose `CMD:` line is the shell text without the
        environment prefix.

    A `CMD:` line equal to neither is a ledger whose human half and machine
    half describe different commands, and the caller refuses it. What ships is
    always the full rendering, environment included, so the line a reader
    copies is the line the replay runs.
    """
    recorded = str(row.get("command", "") or "")
    if record is None or record.get("schema") != CC.SCHEMA:
        return recorded, ""
    try:
        shown = CC.render_shell(record)
        bare = CC.render_shell(record, env=False)
    except Exception:  # a record too malformed to render says so elsewhere
        return recorded, ""
    if recorded and recorded not in (shown, bare):
        return shown, (
            f"the ledger's recorded command string and the exec record beside "
            f"it describe different commands.\n"
            f"    logged  : {recorded}\n"
            f"    record  : {shown}\n"
            f"  The string is what a reader copies and the record is what a "
            f"replay runs; a row on which they differ tells two stories and "
            f"neither can be checked against the other")
    return shown, ""


def exec_lines(record, defined=None) -> list[str]:
    """The exec record, rendered for `checks.txt`.

    THREE FIELDS ON THREE LINES, never one string. `cwd`, the executable form,
    and the environment. A reader who wants to run the row reads these; a
    reader who wants to look at it reads the `command :` line above, which
    `command_line()` above DERIVES from these by `render_shell` and refuses to
    render where the ledger's own string disagrees with it.
    """
    if record is None:
        return []
    if record.get("schema") != CC.SCHEMA:
        return ["    exec    : (unparsable exec record; see the ledger)"]
    out = [f"    exec-cwd: {record.get('cwd', '(none)')}"]
    if record.get("argv") is not None:
        out.append("    exec-argv: " + json.dumps(record["argv"]))
    else:
        out.append("    exec-shell: " + str(record.get("shell", "")))
    out.append("    exec-env: " + json.dumps(record.get("env") or {},
                                             sort_keys=True))
    # THE ROOTS THIS ROW ACTUALLY BINDS, so a reviewer knows which `--root`
    # arguments the replay needs without reading the argv for `$` tokens.
    # Derived from the record by `catena_command.validate`, which is the same
    # walk that decides whether the row is executable at all.
    out.append("    exec-uses: "
               + (", ".join("$" + one for one in record.get("uses") or [])
                  or "(no root; the record does not validate)"))
    return out


def resolve_log(logs: Path, row: dict, end: str) -> Path:
    """THE LOG THE LEDGER NAMES, DIRECTORY AND ALL.

    Every entry records its own unique path inside its attempt's root. V11 kept
    only the BASENAME of the recorded value here, which was lossless while all
    logs sat at one level and silently discarded the attempt the moment they
    did not. The constructed names survive only as fallbacks for a ledger
    written before the paths were recorded, and the glob is the V12 shape: the
    attempt's root, then the slug, so a step is named the same thing on both
    sides.
    """
    recorded = str(row.get("log", ""))
    if recorded:
        relative = (recorded[len("logs/"):] if recorded.startswith("logs/")
                    else recorded)
        return logs / relative
    found = sorted(logs.glob("attempt-[0-9][0-9]/" + row["slug"] + end + ".log"))
    if len(found) == 1:
        return found[0]
    log = logs / (row["slug"] + end + ".log")
    if not log.is_file():
        log = logs / (row["slug"] + ".log")
    return log


def read_attempts(path: Path) -> list[dict]:
    """The append-only attempt ledger, as rows. A line that will not parse is
    kept as a problem row rather than skipped: a record with a hole in it says
    so."""
    rows: list[dict] = []
    if not path or not path.is_file():
        return rows
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(),
                                  start=1):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            rows.append({"attempt": f"(unparsable line {number})",
                         "record": "problem", "reason": str(error)})
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def resolve_dispositions(rows: list[dict]) -> dict[str, dict]:
    """attempt id -> its RESOLVED state, from that attempt's own state rows.

    A step row never carries a state, so nothing can be described as
    authoritative and discarded at once; the terminal `record=attempt` row
    carries the disposition once, with its single reason. An attempt with no
    terminal row is reported as unresolved rather than assumed to have
    succeeded.

    THE RESOLVED STATE IS THE LAST ONE, not the terminal one. A package attempt
    that was authoritative and has since been SUPERSEDED is no longer the
    package to review, and a battery that completed and was then SET ASIDE is
    not the cohort whose figures were used; reading only the terminal row is
    how a ledger comes to name three authoritative attempts and four
    indistinguishable `complete` batteries. The terminal disposition and its
    reason are kept beside the resolved one, because a post-terminal state does
    not overwrite the verdict it follows.

    THE REASON TRAVELS WITH THE RESOLVED STATE. V12 shipped five summary
    reasons, every one of them empty, two of them supersessions whose reasons
    existed only on a separate state row that nothing joined. `reason` here is
    the reason belonging to the state this attempt actually resolves to;
    `terminal_status` and `terminal_reason` keep the verdict underneath it.

    V16: THE TWO AXES ARE REPORTED SEPARATELY AND ARE NEVER COLLAPSED.
    `status` above is kept, unchanged, as "the last state recorded" -- three
    other modules read it and one of them ships it -- but it is no longer the
    whole answer and no reader has to take it for one. Every entry also
    carries, on its own key:

      execution_disposition  how the attempt TERMINATED: `complete`, `failed`,
                             `abandoned`, `sealed`, `discarded`, or "" for an
                             attempt with no terminal row.
      evidence_disposition   whether a completed attempt's measurements remain
                             authoritative: `authoritative`, `set-aside`,
                             `superseded`, or `unevidenced`.

    An attempt that terminated `failed`, `abandoned` or `discarded` reads
    `unevidenced` permanently: it measured nothing that could be carried or
    declined, and no verb will record an evidence disposition on it. An
    attempt that terminated `complete` (or `sealed`) with no evidence row is
    `unevidenced` UNTIL one is recorded.
    """
    out: dict[str, dict] = {}
    for row in rows:
        if row.get("record") == LANE_RECORD:
            continue
        attempt = str(row.get("attempt", ""))
        if not attempt:
            continue
        # `evidence` is stated on every summary object, so a reader of the
        # shipped history never has to infer from a disposition name whether
        # an attempt's figures may be used. An abandoned attempt is resolved
        # and carries none.
        seen = out.setdefault(attempt, {"status": "unresolved: the ledger "
                                                  "carries no terminal row "
                                                  "for this attempt",
                                        "reason": "",
                                        "terminal_status": "",
                                        "terminal_reason": "",
                                        "execution_disposition": "",
                                        "execution_reason": "",
                                        "evidence_disposition": EVIDENCE_UNSET,
                                        "evidence_reason": ""})
        if row.get("record") == "attempt":
            if seen.get("_terminal"):
                seen["status"] = ("INCOHERENT: more than one terminal row "
                                  "for one attempt id")
                seen["_incoherent"] = True
                continue
            seen["_terminal"] = True
            seen["terminal_status"] = str(row.get("status", "(not stated)"))
            seen["evidence"] = (
                "none -- this attempt did not finish measuring and no figure "
                "of its is carried into any claim"
                if seen["terminal_status"] in UNEVIDENCED_STATES else "carried")
            seen["terminal_reason"] = str(row.get("reason", ""))
            # THE EXECUTION AXIS, WHICH IS THE TERMINAL ROW AND NOTHING ELSE.
            # No later row moves it, which is what makes `complete` survive a
            # set-aside instead of being replaced by it.
            seen["execution_disposition"] = seen["terminal_status"]
            seen["execution_reason"] = seen["terminal_reason"]
            if not seen.get("_incoherent"):
                if not seen.get("_post_terminal"):
                    seen["status"] = str(row.get("status", "(not stated)"))
                    seen["reason"] = str(row.get("reason", ""))
        elif (row.get("record") == "state"
              and str(row.get("status", "")) in POST_TERMINAL_STATES
              and not seen.get("_incoherent")):
            seen["status"] = str(row.get("status", ""))
            seen["reason"] = str(row.get("reason", ""))
            seen["_post_terminal"] = True
            # THE EVIDENCE AXIS. The LAST evidence row wins, because the one
            # succession the package side allows -- authoritative, then
            # superseded -- is a real change of what the bytes are. The
            # battery side records one and only one, and `audit_authority`
            # refuses a second; this resolver does not silently hide one.
            seen["evidence_disposition"] = str(row.get("status", ""))
            seen["evidence_reason"] = str(row.get("reason", ""))
    for value in out.values():
        # AN ATTEMPT THAT MEASURED NOTHING IS UNEVIDENCED, PERMANENTLY. Said
        # here as well as refused at the verbs, so a ledger that acquired such
        # a row by hand still READS correctly while the audit names it.
        if value["execution_disposition"] in NEVER_EVIDENCE:
            value["evidence_disposition"] = EVIDENCE_UNSET
            value["evidence_reason"] = ""
        value.pop("_terminal", None)
        value.pop("_incoherent", None)
        value.pop("_post_terminal", None)
    return out


def two_axis_line(attempt: str, value: dict) -> str:
    """One attempt, both axes, EACH REASON BESIDE THE AXIS IT BELONGS TO.

    Before V16 this line carried one disposition and one reason, so a cohort
    that COMPLETED and was later declined printed `set-aside` and the reason
    for declining it -- and the fact that the battery ran to completion was
    not on the line at all. Both facts are true, both are on the line, and
    neither reason can be read as belonging to the other axis.
    """
    execution = value.get("execution_disposition") or ""
    if not execution:
        execution = str(value.get("status") or "")
    told = str(value.get("execution_reason") or "")
    if not told and execution == str(value.get("status") or ""):
        told = str(value.get("reason") or "")
    said = str(value.get("evidence_reason") or "")
    return (f"{attempt}: {execution}"
            + (f" -- {told}" if told else "")
            + f" | evidence {value.get('evidence_disposition', EVIDENCE_UNSET)}"
            + (f" -- {said}" if said else ""))


def resolution_counts(resolved: dict[str, dict]) -> str:
    """One line naming both axes, with every disposition counted separately.

    ABANDONMENT IS RESOLVED AND IS NEVER EVIDENCE. It is counted in
    `resolved`, exactly as `complete` and `failed` are -- its history is
    closed -- and it appears in no successful and no authoritative tally.
    Nothing here folds one disposition into a neighbouring one: V15's prose
    put nine attempts under two words, and a count that hides a disposition
    inside another is the same defect at a smaller scale.
    """
    execution: dict[str, int] = {}
    evidence: dict[str, int] = {}
    open_attempts = 0
    for value in resolved.values():
        word = value["execution_disposition"]
        if not word or str(value["status"]).startswith(("unresolved",
                                                        "INCOHERENT")):
            open_attempts += 1
            if not word:
                continue
        execution[word] = execution.get(word, 0) + 1
        evidence[value["evidence_disposition"]] = (
            evidence.get(value["evidence_disposition"], 0) + 1)
    said = ", ".join(f"{key} {execution[key]}" for key in sorted(execution))
    told = ", ".join(f"{key} {evidence[key]}" for key in sorted(evidence))
    return (f"attempts {len(resolved)}; execution ({said or 'none'}); "
            f"evidence ({told or 'none'}); with no terminal row "
            f"{open_attempts}")


def state_rows(rows: list[dict]) -> dict[str, list[dict]]:
    """attempt id -> its state-bearing rows, in ledger order."""
    out: dict[str, list[dict]] = {}
    for row in rows:
        attempt = str(row.get("attempt", ""))
        if not attempt or not str(row.get("status", "")):
            continue
        out.setdefault(attempt, []).append(row)
    return out


def instant(text) -> datetime.datetime | None:
    """One recorded timestamp, as an aware instant, or None if it is not one.

    Two shapes reach here: `date -Is`, which carries a numeric UTC offset, and
    the compact `%Y%m%dT%H%M%SZ` an attempt id embeds. A value with no offset
    is read as UTC rather than refused, because these checks are about ORDER
    and a missing offset is a hole in the record, not a different instant --
    and `--verify-ledger` reports the hole separately when it matters.
    """
    text = str(text or "").strip()
    if not text:
        return None
    if re.fullmatch(r"\d{8}T\d{6}Z", text):
        try:
            return datetime.datetime.strptime(
                text, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            return None
    try:
        found = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if found.tzinfo is None:
        found = found.replace(tzinfo=datetime.timezone.utc)
    return found


def declared_lane(rows: list[dict]) -> tuple[str, list[str]]:
    """The lane a ledger declares, and what is wrong with the declaration."""
    problems: list[str] = []
    declarations = [row for row in rows if row.get("record") == LANE_RECORD]
    named = sorted({str(row.get("lane", "")) for row in declarations
                    if str(row.get("lane", ""))})
    if not declarations:
        problems.append(
            "the ledger carries no record=lane row; a ledger that does not "
            "name its lane cannot refuse a row from another lane, and cannot "
            "tell a reader that the ordinals in it belong to one allocation")
    elif len(named) > 1:
        problems.append("the ledger declares more than one lane ("
                        + ", ".join(named) + "); one ledger, one lane")
    elif len(declarations) > 1:
        problems.append(
            f"the ledger carries {len(declarations)} record=lane rows; a lane "
            f"is declared once, on the first row, and never reopened")
    return (named[0] if len(named) == 1 else ""), problems


def ordinal_owners(rows: list[dict]) -> tuple[dict[str, set[str]], list[str]]:
    """ordinal -> the attempt ids that have ever carried it, and the malformed.

    EVERY row counts, including a discarded attempt's and a superseded one's.
    That is the whole rule: V12 recomputed `max(attempt_no) + 1` over a ledger
    file the operator had just started fresh, so 03/04/05/06 were reissued as
    03/04/05 and two different attempts answer to one ordinal in the surviving
    record.
    """
    owners: dict[str, set[str]] = {}
    problems: list[str] = []
    for row in rows:
        if row.get("record") == LANE_RECORD:
            continue
        attempt = str(row.get("attempt", ""))
        raw = str(row.get("attempt_no", "")).strip()
        if not attempt or not raw:
            continue
        try:
            key = f"{int(raw):02d}"
        except ValueError:
            problems.append(f"{attempt}: attempt_no {raw!r} is not a number")
            continue
        owners.setdefault(key, set()).add(attempt)
    return owners, problems


def audit_ledger(rows: list[dict], lane: str = "",
                 frozen_at: datetime.datetime | None = None) -> list[str]:
    """THE ATTEMPT LEDGER'S OWN INTEGRITY, separate from the state machine.

    `audit_authority()` below asks whether the TRANSITIONS are legal. This asks
    the four questions V12 could not answer about the ledger as a record:

      1. IS IT ONE LANE'S? Every row names its lane and the ledger opens by
         declaring it. A ledger of another lane is refused rather than
         appended to, and a fresh ledger is refused over an existing one, so
         "the operator started over" is impossible to do quietly.
      2. IS EVERY ORDINAL ALLOCATED ONCE? An ordinal any row has ever carried
         is spent, however that attempt ended.
      3. DOES EVERY ATTEMPT END, ONCE, WITH A REASON? Exactly one terminal
         row per attempt, and every state that is not `complete`, `sealed`
         or `authoritative` -- terminal or post-terminal -- carries a
         non-empty reason on the row that states it.
      4. IS IT IN TIME ORDER? Rows of one attempt are appended as they happen;
         a row may not end before it starts, may not start before the row
         appended ahead of it, and may not end after the instant the packaged
         member claims to have been frozen at. An attempt id embeds its own
         minting instant, and that must agree with the attempt's first row.
    """
    problems: list[str] = []
    body = [row for row in rows if row.get("record") != LANE_RECORD]

    # -- 1. ONE LANE, DECLARED AND THEN REPEATED ON EVERY ROW ---------------
    ledger_lane, said = declared_lane(rows)
    problems += said
    if lane and ledger_lane and lane != ledger_lane:
        problems.append(
            f"this ledger belongs to lane {ledger_lane!r}, not {lane!r}; "
            f"refusing to read a lane-{ledger_lane} ledger as lane {lane}'s. "
            f"One lane, one ledger, one allocation of ordinals")
    expected = ledger_lane or lane
    missing = [row for row in body if not str(row.get("lane", ""))]
    if missing:
        problems.append(
            f"{len(missing)} row(s) carry no lane, the first being "
            f"{missing[0].get('attempt', '(no attempt)')!r}; every row names "
            f"its lane so two lanes' ledgers cannot be concatenated in silence")
    foreign = sorted({str(row.get("lane", "")) for row in body
                      if str(row.get("lane", ""))
                      and expected and str(row.get("lane", "")) != expected})
    if foreign:
        problems.append(
            "rows of another lane are present in this one (" + ", ".join(foreign)
            + f"); this is a lane-{expected} ledger")

    # -- 2. AN ORDINAL IS ALLOCATED ONCE FOR THE WHOLE LANE -----------------
    owners, said = ordinal_owners(body)
    problems += said
    for key in sorted(owners):
        if len(owners[key]) > 1:
            problems.append(
                f"attempt ordinal {key} is carried by {len(owners[key])} "
                f"attempts (" + ", ".join(sorted(owners[key]))
                + "); an ordinal is allocated once for the whole lane and is "
                  "never reissued, not to replace a discarded attempt and not "
                  "because a ledger file was started again")
    for key, holders in sorted(owners.items()):
        for one in sorted(holders):
            found = ATTEMPT_ID.match(one)
            if found and found.group(3) != key:
                problems.append(
                    f"{one}: its id embeds ordinal {found.group(3)} while its "
                    f"rows carry attempt_no {key}")

    # -- 3. ONE TERMINAL DISPOSITION EACH, AND A REASON WHERE ONE IS OWED ---
    resolved = resolve_dispositions(body)
    for one, value in sorted(resolved.items()):
        status = str(value.get("status", ""))
        if status.startswith("unresolved"):
            problems.append(
                f"{one}: no terminal row; every attempt reaches exactly one "
                f"terminal disposition, and an attempt that was abandoned is "
                f"abandoned in the record too, with its reason")
        elif status.startswith("INCOHERENT"):
            problems.append(f"{one}: {status}")
        elif status in REASONED_STATES and not str(value["reason"]).strip():
            problems.append(
                f"{one}: resolves to {status!r} and carries no reason, so the "
                f"shipped summary would carry none either")
    for number, row in enumerate(body, start=1):
        status = str(row.get("status", ""))
        if status in REASONED_STATES and not str(row.get("reason", "")).strip():
            problems.append(
                f"{row.get('attempt', '?')}: row {number} states {status!r} "
                f"with an empty reason; every state that is not "
                + " or ".join(sorted(SUCCESSFUL_STATES))
                + " says why, in words, on the row that states it")

    # -- 4. CHRONOLOGY, WITHIN AN ATTEMPT AND AGAINST THE FREEZE ------------
    carried: dict[str, list[tuple[int, dict]]] = {}
    for number, row in enumerate(body, start=1):
        carried.setdefault(str(row.get("attempt", "")), []).append((number, row))
    # ORDERED ON `end`, NOT ON `start`, and that is the only ordering the
    # schema admits: a battery's terminal row opens at BATTERY_START, the same
    # instant its first row opens at, because the row describes the whole
    # attempt. What is strictly increasing is the instant each row CLOSES at,
    # which is the instant it was appended.
    for one in sorted(carried):
        previous: datetime.datetime | None = None
        previous_number = 0
        for number, row in carried[one]:
            start = instant(row.get("start", ""))
            end = instant(row.get("end", ""))
            if start and end and end < start:
                problems.append(
                    f"{one}: row {number} ends {row.get('end')} before it "
                    f"starts {row.get('start')}")
            if end and previous and end < previous:
                problems.append(
                    f"{one}: row {number} ends {row.get('end')}, earlier than "
                    f"row {previous_number} appended ahead of it; the rows of "
                    f"one attempt are appended as they close")
            if end:
                previous, previous_number = end, number
            if frozen_at and end and end > frozen_at:
                problems.append(
                    f"{one}: row {number} ends {row.get('end')}, AFTER the "
                    f"instant this ledger member is frozen at "
                    f"({frozen_at.isoformat()}); a frozen record cannot "
                    f"contain an event later than its own freeze")

    # -- 5. THE ID'S OWN TIMESTAMP AGAINST THE ATTEMPT'S FIRST ROW ----------
    for one in sorted(carried):
        if not one:
            # A ROW ABOUT THE FILE IS NOT A ROW MISSING AN ATTEMPT.
            #
            # `--retire-ledger` appends `record=retired`, which states that
            # this FILE stops here and carries its digest, byte count, row
            # count and spent ordinals. It has no attempt id because it is not
            # about an attempt, and this audit faulted every retired ledger
            # the toolchain has ever written -- a row its own retirement verb
            # had appended one line earlier. The fault is real for every other
            # kind of row, and stays: a `step` or a `state` row that names no
            # attempt cannot be read at all, and those are named here.
            stray = sorted({str(row.get("record") or "(none)")
                            for _number, row in carried[one]
                            if str(row.get("record") or "")
                            not in FILE_SCOPED_RECORDS})
            if stray:
                problems.append(
                    "a row names no attempt: " + ", ".join(
                        f"record={name!r}" for name in stray)
                    + ". Only a row ABOUT THE FILE -- "
                    + ", ".join(sorted(FILE_SCOPED_RECORDS))
                    + " -- may omit the attempt it belongs to")
            continue
        found = ATTEMPT_ID.match(one)
        if not found:
            problems.append(
                f"{one!r}: not a well-formed attempt id "
                f"(<side>-<YYYYMMDDTHHMMSSZ>-<ordinal><nonce>), so nothing can "
                f"check the instant it claims to have been minted at")
            continue
        minted = instant(found.group(2))
        first = None
        for _number, row in carried[one]:
            first = instant(row.get("start", ""))
            if first:
                break
        if not minted or not first:
            continue
        drift = (minted - first).total_seconds()
        if drift > ID_LAG_MAX_SECONDS:
            problems.append(
                f"{one}: its id embeds {found.group(2)}, {drift:.0f}s LATER "
                f"than its own first row ({carried[one][0][1].get('start')}). "
                f"An id is minted before anything is recorded, so a later one "
                f"means the id and the rows come from different runs "
                f"(tolerance {ID_LAG_MAX_SECONDS}s, the clock's, not work's)")
        elif -drift > ID_LEAD_MAX_SECONDS:
            problems.append(
                f"{one}: its id embeds {found.group(2)}, {-drift:.0f}s EARLIER "
                f"than its own first row ({carried[one][0][1].get('start')}); "
                f"only a preflight separates minting from the first row and "
                f"{ID_LEAD_MAX_SECONDS}s is far longer than one takes")
    return problems


def audit_authority(rows: list[dict], scope: str = EXTERNAL) -> list[str]:
    """THE STATE MACHINE, ENFORCED. See `assemble.sh`'s header for the table.

    The incident: a lane's ledger marked THREE attempts `authoritative` -- the
    head battery, the parent battery and a package attempt that had already
    been superseded -- because `battery.sh` and `assemble.sh` wrote the same
    word for two different facts. "This battery ran to completion" and "this is
    the package attempt to review" are separate axes, and with one word for
    both the authoritative count can never be one. So:

      * a battery attempt may only ever be `started`, `complete`, `failed` or
        the post-terminal `set-aside`; `sealing`, `sealed`, `superseded` and
        `authoritative` are package words;
      * every transition an attempt makes must be one the table allows, which
        is what refuses `discarded` followed by `sealed`;
      * exactly one `record=attempt` row per attempt carries the disposition,
        so an attempt cannot be handed two;
      * at most one package attempt in the ledger may RESOLVE to the winning
        word of its scope, superseding being what makes room for the next.

    THE SCOPE IS THE WHOLE OF THE V13 PACKAGE-SIDE CHANGE. Read `in-package`,
    the winning word is `sealed` and `authoritative` is refused by name: those
    bytes are frozen at P5 and P8 has not run, so the claim would be a verdict
    nobody had. Read `external`, `authoritative` is legal as a POST-terminal
    `record=state` row appended after P8 passed, beside the sidecar bound to
    the final ZIP, and it is the winning word there.
    """
    problems: list[str] = []
    sides: dict[str, str] = {}
    external = scope == EXTERNAL
    winning = "authoritative" if external else "sealed"
    for attempt, carried in state_rows(rows).items():
        side = ""
        for row in carried:
            side = str(row.get("side", "")) or side
        sides[attempt] = side
        if side in BATTERY_SIDES:
            table, kind = BATTERY_STATES, "battery"
            evidence_table = BATTERY_EVIDENCE_STATES
        elif side == "package":
            # ONE TABLE FOR BOTH SCOPES, AND THE SCOPE ENFORCED BY THE TWO
            # RULES THAT ACTUALLY STATE IT. V13: a predecessor that really
            # did pass P8, really was authoritative and was then superseded
            # has a history containing the word, and a package sealed
            # afterwards ships that history — deleting it is the V12 defect,
            # not the cure for it. So the transition table is the same in
            # both scopes, and what `in-package` forbids is said exactly
            # twice below: `authoritative` may not be an attempt's
            # DISPOSITION, and nobody may still RESOLVE to it in bytes this
            # pipeline froze before P8.
            table = EXTERNAL_PACKAGE_STATES
            kind = "package"
            evidence_table = PACKAGE_EVIDENCE_STATES
        else:
            problems.append(f"{attempt}: carries state rows but names no "
                            f"known side ({side or '(none)'}); the state "
                            f"machine is defined per side")
            continue
        terminal: list[str] = []
        previous = ""
        # THE SECOND AXIS, WALKED BESIDE THE FIRST AND NEVER MIXED INTO IT.
        # `previous` is the execution machine's state; `evidence` is the
        # evidence machine's. A row belongs to exactly one of them, decided by
        # its status word, and an evidence row therefore never appears as an
        # execution transition -- which is the whole of the V16 correction.
        evidence = ""
        for row in carried:
            status = str(row.get("status", ""))
            record = str(row.get("record", ""))
            # §10: `refused` IS NOT A STATE, IN EITHER AXIS. A guard refusal is
            # a CAUSE and it belongs in the reason; the disposition it causes
            # is `failed`. Named here so a ledger that reaches for the word is
            # told which disposition it meant rather than merely told the word
            # is unknown.
            if status.lower() in NOT_A_DISPOSITION:
                problems.append(
                    f"{attempt}: {status!r} is not a disposition, in either "
                    f"axis. A guard refusal is a CAUSE, recorded in the "
                    f"reason; the execution disposition it causes is "
                    f"{NOT_A_DISPOSITION[status.lower()]!r}")
                continue
            # BY NAME, BECAUSE THE GENERIC MESSAGE WOULD NOT SAY WHY. This is
            # the review's finding, not a vocabulary preference: the row is
            # written at or before P5 and frozen there, so `authoritative`
            # asserts the outcome of P6, P7 and P8 before any of them ran.
            if (status == "authoritative" and not external
                    and record == "attempt" and side == "package"):
                problems.append(
                    f"{attempt}: claims 'authoritative' in a record that is "
                    f"frozen at P5, BEFORE P6, P7 and P8 have run. No sealed "
                    f"package bytes may claim final authority before P8: a "
                    f"package attempt may claim at most 'sealed' about "
                    f"itself, and 'authoritative' is established afterwards, "
                    f"in the external complete ledger and the "
                    f"<package>.authority.json sidecar bound to the final ZIP")
                continue
            # -- the evidence axis ------------------------------------------
            if status in evidence_table and status:
                if record == "attempt":
                    # BOTH FACTS IN ONE SENTENCE, because both are true and a
                    # reader needs both: the word is not this side's execution
                    # vocabulary, AND it is not a disposition at all.
                    problems.append(
                        f"{attempt}: a {kind} attempt is never {status!r}; "
                        f"{status} is not a disposition and must not be "
                        f"carried by a record=attempt row. It is an EVIDENCE "
                        f"disposition, recorded on a record=state row after "
                        f"the attempt has already terminated")
                    continue
                wanted = EVIDENCE_FOLLOWS[kind]
                if not terminal:
                    problems.append(
                        f"{attempt}: illegal transition (start) -> {status}; "
                        f"an evidence disposition says what became of a "
                        f"terminated attempt's measurements, and this attempt "
                        f"has not terminated. Only a {kind} attempt that "
                        f"reached {wanted!r} has measurements to carry or to "
                        f"decline")
                elif terminal[0] != wanted:
                    problems.append(
                        f"{attempt}: illegal transition {terminal[0]} -> "
                        f"{status}; an evidence disposition is only "
                        f"meaningful for a {kind} attempt whose EXECUTION "
                        f"disposition is {wanted!r}. This one terminated "
                        f"{terminal[0]!r}, which is {EVIDENCE_UNSET} and stays "
                        f"so: applying an evidence word to it would cover "
                        f"what that disposition says")
                elif status not in evidence_table[evidence]:
                    problems.append(
                        f"{attempt}: illegal transition "
                        f"{evidence or '(no evidence disposition)'} -> "
                        f"{status}; an attempt reaches at most one evidence "
                        f"disposition and nothing reopens it")
                evidence = status
                previous = previous  # the execution machine does not move
                continue
            # -- the execution axis -----------------------------------------
            if status not in table:
                problems.append(
                    f"{attempt}: a {kind} attempt is never {status!r}; the "
                    f"{kind} states are "
                    + ", ".join(sorted(one for one in table if one))
                    + ", and its evidence dispositions are "
                    + ", ".join(sorted(one for one in evidence_table if one)))
                continue
            if status not in table[previous]:
                problems.append(
                    f"{attempt}: illegal transition "
                    f"{previous or '(start)'} -> {status}")
            if status in TERMINAL_STATES:
                terminal.append(status)
                if record != "attempt":
                    problems.append(
                        f"{attempt}: {status} is a disposition and must be "
                        f"carried by a record=attempt row, not record="
                        f"{record or '(none)'}")
            elif record == "attempt":
                problems.append(
                    f"{attempt}: {status} is not a disposition and must not be "
                    f"carried by a record=attempt row")
            previous = status
        if len(terminal) > 1:
            problems.append(
                f"{attempt}: {len(terminal)} terminal rows ("
                + ", ".join(terminal)
                + "); one attempt gets one disposition and one reason")
    resolved = resolve_dispositions(rows)
    # THE WINNER IS AN EVIDENCE FACT, NOT AN EXECUTION ONE, and it is a
    # PACKAGE's. A battery cohort whose figures a package carries is
    # `authoritative` too -- on its own axis, and as many cohorts as a package
    # ships may be -- so counting winners over the collapsed status is how one
    # tally came to answer two questions.
    def holds(value: dict) -> bool:
        if external:
            return value["evidence_disposition"] == "authoritative"
        # In package bytes the winning word is `sealed`, an EXECUTION fact --
        # and a package already superseded no longer holds it, which is what
        # makes room for the replacement being sealed now.
        return (value["execution_disposition"] == "sealed"
                and value["evidence_disposition"] != "superseded")

    winners = sorted(one for one, value in resolved.items()
                     if holds(value) and sides.get(one) == "package")
    # Nothing more is needed to keep the winning word a package's: `sealed` is
    # refused on a battery by the execution vocabulary above, and
    # `authoritative` on a battery is a legal EVIDENCE disposition -- a cohort
    # whose figures a package carries -- which is a different claim from being
    # the package to review, and is exactly the conflation this separates.
    if len(winners) > 1:
        # THE REMEDY IS NAMED, because the pipeline deliberately does not
        # apply it. Demoting a package that is already out for review is a
        # judgement about which package a reader should be holding, and an
        # assembly script is not entitled to make it silently -- the operator
        # appends the supersession, with its reason, and it is a ledger row
        # like any other.
        problems.append(
            f"{len(winners)} attempts resolve to {winning} ("
            + ", ".join(winners)
            + "); a ledger names at most one package to review. Append one "
              "record=state status=superseded row, with its one reason, for "
              "the attempt being replaced, and seal again")
    # AND IN A RECORD THAT SHIPS, NOBODY HOLDS THE POST-P8 WORD AT ALL. A
    # predecessor that really did pass P8 and really was authoritative must
    # already have been SUPERSEDED before a replacement can be sealed -- that
    # is the rule above -- so it resolves to `superseded` and its historical
    # `authoritative` row ships as the honest history it is. What is refused
    # here is a package shipping bytes in which some attempt STILL HOLDS
    # final authority that this pipeline cannot have established.
    #
    # A PACKAGE ATTEMPT'S, AND ONLY A PACKAGE ATTEMPT'S. A battery cohort's
    # evidence disposition says which measurements this package reports, which
    # is a fact the pipeline HAS at P5 -- it is shipping them -- and not the
    # verdict of a verification that has not run.
    if not external:
        holding = sorted(one for one, value in resolved.items()
                         if value["evidence_disposition"] == "authoritative"
                         and sides.get(one) == "package")
        if holding:
            problems.append(
                "attempts resolving to 'authoritative' in a record frozen at "
                "P5 (" + ", ".join(holding) + "); final authority is "
                "established after P8, in the external complete ledger and "
                "the sidecar bound to the final ZIP, never in package bytes. "
                "Supersede the previous winner, with its one reason, before "
                "sealing a replacement")
    return problems


def audit_attempt_logs(package: Path, rows: list[dict],
                       audited: set[str]) -> list[str]:
    """EVERY TRANSCRIPT UNDER THE ATTEMPT THAT WROTE IT, BOTH DIRECTIONS.

    The incident: `logs/gate-comparison.log` in the reviewed package was
    claimed by six different attempts and `logs/sealer-tests.log` by five,
    because the package-phase transcripts carried no attempt ordinal and every
    rerun opened the same paths. A failed attempt's logs did not stay with that
    attempt; the next attempt overwrote them, and nothing in the pipeline
    compared the ledger's `log=` values against the files on disk.

    `rows` is the whole ledger; `audited` is the set of attempt ids this
    package was built from -- the two staged battery attempts and the assembly.
    Rows of other attempts describe other package directories and are not this
    package's to account for. Four refusals, on top of the containment rule:

      1. a row whose log is under `logs/` but not under `logs/attempt-NN/` for
         that row's OWN ordinal;
      2. one log path claimed by more than one row;
      3. a claimed log of zero bytes with no `log_empty_reason` on any row that
         claims it -- an empty transcript is indistinguishable from a
         transcript that was never written, and the difference is the whole
         question;
      4. a `.log` under an attempt root that no row claims, or any member of a
         root no row writes into.

    A log OUTSIDE `logs/` is not audited: `MANIFEST.sha256`, the invocation log
    and the final-verification transcript live beside the archive by design,
    because a file created after the seal is not in the manifest that seal
    produced. The battery ordering ledgers and the packaged attempt rows sit at
    the top of `logs/` for the reason named in SCOPE_RECORDS, and a discard
    marker sits there because `checks.py` has always refused that glob.
    """
    problems: list[str] = []
    scope = {name for name, _why in SCOPE_RECORDS}
    claims: dict[str, list[dict]] = {}
    roots: set[str] = set()

    # -- 0. NO ROW NAMES A LOG ROOT THE PACKAGE DOES NOT HAVE ---------------
    # V12: ten rows in the shipped `logs/attempts.json` referenced
    # `logs/attempt-03/` and `logs/attempt-04/`, and the package contained
    # neither. The per-file check below never reached them because it only
    # walks the audited attempts, while `write_attempts()` ships EVERY
    # `side=package` row -- so the dangling roots arrived by the one route
    # nothing audited. The scope here is therefore the scope of what SHIPS.
    #
    # A discarded predecessor whose transcripts were never staged is a real
    # case and it has a real answer: the row says so, in words, in
    # `log_root_elsewhere`. What is refused is the silent dangling reference.
    shipped = set(audited) | {str(row.get("attempt", "")) for row in rows
                              if str(row.get("side", "")) == "package"}
    # AN APPEND-ONLY LEDGER CORRECTS ITSELF BY APPENDING. V13: the exemption
    # was read off the row that named the root, so an attempt whose
    # transcripts went away AFTER its rows were written could never be
    # explained — the rows may not be rewritten, and there was nowhere else to
    # say it. A later row for the same attempt carrying `log_root_elsewhere`
    # is that channel: the explanation arrives after the fact, as it must, and
    # it is still IN the ledger rather than in prose beside it.
    explained = {str(row.get("attempt", "")) for row in rows
                 if str(row.get("log_root_elsewhere", "")).strip()}
    dangling: dict[str, set[str]] = {}
    for row in rows:
        if str(row.get("attempt", "")) not in shipped:
            continue
        if str(row.get("attempt", "")) in explained:
            continue
        if str(row.get("log_root_elsewhere", "")).strip():
            continue
        found = ATTEMPT_LOG.match(str(row.get("log", "")))
        if not found:
            continue
        root = f"logs/attempt-{found.group(1)}"
        if not (package / root).is_dir():
            dangling.setdefault(root, set()).add(
                str(row.get("attempt", "(no attempt)")))
    for root in sorted(dangling):
        problems.append(
            f"{root}: named by rows this package ships ("
            + ", ".join(sorted(dangling[root]))
            + ") but the package contains no such log root. Either stage the "
              "root or say on the row, in log_root_elsewhere, where that "
              "attempt's transcripts are and why they are not here")

    for row in rows:
        attempt = str(row.get("attempt", ""))
        if attempt not in audited:
            continue
        value = str(row.get("log", ""))
        if not value or value.startswith("("):
            continue
        if not value.startswith("logs/"):
            continue
        if value in scope or DISCARD_MARKER.match(value):
            continue
        found = ATTEMPT_LOG.match(value)
        if not found:
            problems.append(
                f"{attempt}: names {value}, which is not one transcript inside "
                f"one attempt log root; that shape is the pre-V12 convention "
                f"every attempt could open")
            continue
        try:
            ordinal = f"{int(row.get('attempt_no', -1)):02d}"
        except (TypeError, ValueError):
            ordinal = ""
        if found.group(1) != ordinal:
            problems.append(
                f"{attempt}: names {value}, which lies in attempt root "
                f"{found.group(1)} while the row belongs to attempt ordinal "
                f"{ordinal or '(not stated)'}")
            continue
        roots.add(f"logs/attempt-{ordinal}")
        claims.setdefault(value, []).append(row)
    for value in sorted(claims):
        claiming = claims[value]
        if len(claiming) > 1:
            problems.append(
                f"{value}: claimed by {len(claiming)} ledger rows ("
                + ", ".join(sorted({str(one.get('attempt', '?'))
                                    for one in claiming}))
                + "); one transcript answers to one row")
        path = package / value
        if not path.is_file():
            problems.append(f"{value}: claimed by "
                            f"{claiming[0].get('attempt', '?')} but the "
                            f"package does not contain it")
        elif path.stat().st_size == 0 and not any(
                str(one.get("log_empty_reason", "")) for one in claiming):
            problems.append(
                f"{value}: claimed but zero bytes, and no row explains it "
                f"(set log_empty_reason on the row when a step really does "
                f"print nothing)")
    logs = package / "logs"
    if not logs.is_dir():
        return problems
    for root in sorted(logs.glob("attempt-*")):
        if not root.is_dir():
            continue
        relative_root = "logs/" + root.name
        if not ATTEMPT_ROOT_NAME.match(root.name):
            problems.append(f"{relative_root}: not a two-digit attempt root")
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(package).as_posix()
            if not ATTEMPT_LOG.match(relative):
                problems.append(
                    f"{relative}: nested below its attempt root; no rule "
                    f"addresses a transcript at that depth")
                continue
            if path.suffix == ".log":
                if relative not in claims:
                    problems.append(
                        f"{relative}: no ledger row of any attempt this "
                        f"package was built from claims it")
            elif relative_root not in roots:
                problems.append(
                    f"{relative}: a report in {relative_root}, which no "
                    f"audited row writes a transcript into")
    # AND NOT AT THE TOP OF `logs/`. A transcript there is exactly the shape
    # six attempts could all open, so it is refused by name rather than left
    # to the roster check above, which only walks the roots.
    for path in sorted(logs.glob("*.log")):
        if path.is_file():
            problems.append(
                f"logs/{path.name}: a transcript at the top of logs/ belongs "
                f"to no attempt; every transcript lives under the root of the "
                f"attempt that wrote it")
    return problems


def write_attempts(logs: Path, rows: list[dict], wanted: set[str],
                   package_attempt: str,
                   frozen_at: datetime.datetime | None = None,
                   lane: str = "") -> Path | None:
    """The rows this package was built from, copied in before the freeze.

    Copied, not summarised, and filtered only by attempt identity: the ledger
    outside spans every attempt ever made, and this member carries the ones
    the two staged battery ledgers name, this assembly's own, AND EVERY OTHER
    ASSEMBLY ATTEMPT.

    The last of those is a correction. Filtering to "the attempts this package
    was built from" dropped the assembly attempts that FAILED, so a package
    whose prose named its discarded predecessors shipped a machine-readable
    ledger that named none of them — prose and ledger disagreeing about
    exactly the thing the ledger exists to settle, which is the defect class
    this pipeline is meant to close rather than reproduce. A discarded
    assembly is relevant evidence precisely because it was discarded: it is
    how a reader sees that a refusal fired, that a stamp was never reused, and
    that this package is the attempt that survived. Every `side=package` row
    therefore ships, with its own terminal disposition and its one reason.
    """
    dispositions = resolve_dispositions(rows)
    package_attempts = {str(row.get("attempt", "")) for row in rows
                        if str(row.get("side", "")) == "package"}
    keep = [row for row in rows
            if row.get("record") == LANE_RECORD
            or str(row.get("attempt", "")) in wanted
            or str(row.get("side", "")) == "package"
            or (package_attempt and str(row.get("attempt", "")) == package_attempt)]
    for row in keep:
        if row.get("record") == LANE_RECORD:
            continue
        row["resolved_status"] = dispositions.get(
            str(row.get("attempt", "")), {}).get("status", "unresolved")
    if frozen_at is None:
        frozen_at = datetime.datetime.now(datetime.timezone.utc)
    out = {
        "note": "Rows copied from the append-only attempt ledger that lives "
                "outside this package, filtered to the attempts this package "
                "was built from. A row with record=step states what one step "
                "did; the record=attempt row of the same attempt carries its "
                "one disposition and its one reason, and a record=state row "
                "carries a non-terminal state or a later supersession. "
                "resolved_status on each row is that attempt's LAST state, "
                "joined here mechanically: a battery is complete or failed "
                "and may later be set-aside; a package attempt is sealed or "
                "discarded, and may later be superseded. SEALED IS THE MOST "
                "ANY ROW IN THIS MEMBER MAY CLAIM ABOUT THIS PACKAGE: these "
                "bytes are frozen at P5, before the manifest, the archive and "
                "the final verification, so final authority is not "
                "established here. It is recorded after P8 passes, in the "
                "append-only ledger outside this package and in the authority "
                "sidecar bound to the final ZIP. An authoritative row that "
                "does appear below belongs to an EARLIER package that passed "
                "its own P8 and has since been superseded; it is history, not "
                "a claim about this one.",
        "copied_at_phase": "P5, after the consistency audit and immediately "
                           "before the manifest -- as late as the freeze line "
                           "allows, and late enough to carry the sealing "
                           "attempt's own terminal row, which V11 wrote at P8 "
                           "into a member composed at P1. Rows the pipeline "
                           "appends after this instant, P6 through P8, are in "
                           "the ledger outside the package, not here",
        # THE FREEZE INSTANT, AS AN INSTANT. `copied_at_phase` above is prose,
        # and V12 proved prose is not checkable: attempt 04's supersession is
        # stamped 19:46:00Z inside a file whose phase note says it was frozen
        # at 19:45:30Z, and no tool could compare the two because one of them
        # was a sentence. This field is a timestamp, `--verify-ledger` reads
        # it, and `--seal-ledger` refuses to write a member carrying a row
        # that ends after it.
        "frozen_at": frozen_at.isoformat(),
        "lane": lane or declared_lane(rows)[0],
        # WHAT THIS MEMBER DOES NOT CARRY, DECLARED RATHER THAN TRUNCATED.
        # V12's member stopped at P5 and said nothing about it, so a reader
        # could not tell "P6 left no row" from "P6 never ran". The phases
        # below run after this file is frozen -- necessarily, since the first
        # of them hashes it -- and their rows are in the ledger outside the
        # package and in the out-of-package sidecar.
        "phases_not_recorded": [
            {"phase": phase, "why": why} for phase, why in PHASES_AFTER_FREEZE],
        "attempts": [{"attempt": attempt,
                      # THE REASON BELONGING TO THE STATE THIS RESOLVES TO,
                      # not an empty string. V12 shipped five of these and
                      # every one was empty, two of them supersessions whose
                      # reasons sat on state rows nothing joined to the
                      # summary. The verdict underneath a post-terminal state
                      # is kept beside it rather than replaced by it.
                      "status": value["status"],
                      "reason": value["reason"],
                      "terminal_status": value.get("terminal_status", ""),
                      "terminal_reason": value.get("terminal_reason", ""),
                      # V16: THE TWO AXES, SHIPPED SEPARATELY. `status` above
                      # is the LAST state and it answers one question badly
                      # when the answer is two facts. These two say, on their
                      # own keys, how the attempt terminated and what became
                      # of its measurements -- and `evidence` keeps the
                      # sentence a reader gets instead of having to infer it
                      # from a disposition name.
                      "execution_disposition":
                          value.get("execution_disposition", ""),
                      "execution_reason": value.get("execution_reason", ""),
                      "evidence_disposition":
                          value.get("evidence_disposition", EVIDENCE_UNSET),
                      "evidence_reason": value.get("evidence_reason", ""),
                      "evidence": value.get("evidence", "")}
                     for attempt, value in sorted(dispositions.items())
                     if attempt in wanted or attempt == package_attempt
                     or attempt in package_attempts],
        "rows": keep,
    }
    text = json.dumps(out, indent=2, sort_keys=True) + "\n"
    # PRE-NORMALIZED, because nothing normalizes the tree after the freeze.
    # This member is written at P5, past the P2 fixpoint, so the substitution
    # table is applied here exactly as `derive-claims.py` applies it to
    # claims.json -- the ledger's own `date -Is` stamps carry a local UTC
    # offset and would otherwise reach the seal untouched.
    sealer = load_sealer()
    for pattern, replacement in sealer.rules(sealer.identities(),
                                             sealer.repo_root()):
        text = pattern.sub(replacement, text)
    for label, pattern in sealer.forbidden(sealer.identities(),
                                           sealer.repo_root()):
        for number, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                raise SystemExit(f"logs/attempts.json:{number}: private token "
                                 f"[{label}] survived normalization; refusing "
                                 f"to write it")
    path = logs / "attempts.json"
    path.write_text(text, encoding="utf-8")
    return path


def load_sealer():
    """The sanitizer that ships beside this tool, as a module.

    One substitution table, three consumers: the seal, the derivation and this.
    A re-implementation here would drift from the table the seal enforces, and
    the member this writes lands after the last normalize pass.
    """
    import importlib.util
    location = Path(__file__).resolve().with_name("sanitize-and-seal.py")
    spec = importlib.util.spec_from_file_location("sealer_for_checks", location)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load the sealer beside this tool: {location}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# THE SECOND VOCABULARY, AND WHY THE PACKAGE HAS TO SAY SO ITSELF.
#
# Two disjoint sets of `$NAME` tokens reach a sealed package, from two
# subsystems that never meet:
#
#   REPLAY ROOTS       written by `battery.sh` and `assemble.sh` INTO command
#                      records. They are BINDINGS: `replay-command.py --root
#                      NAME=/path` supplies one and the recorded command runs.
#                      Their names and meanings are declared at run time on
#                      `root=` lines in the ordering ledgers, and the legend
#                      below is built from those lines.
#
#   SANITIZATION TOKENS  written by `sanitize-and-seal.py` INTO transcript
#                      prose at P2. They are SUBSTITUTIONS: a private path was
#                      removed and this token stands where it was. Nothing
#                      binds them and no recorded command may use one --
#                      `catena_command.RESERVED_VARIABLES` refuses exactly
#                      these names in a record for that reason.
#
# So the same directory can be named two ways in one package: the candidate
# checkout is `$CANDIDATE_REPO` in `commands.json` and `$REPO` in a
# transcript. That is not V15's defect -- V15's was ONE token meaning TWO
# directories inside a single row, which is genuinely ambiguous -- but it is
# what the V15 review landed on when `verify-final.log` said `$WORKSPACE/...`
# and `executed-tools.json` said `$EVIDENCE` for one anchor. The package
# answers it in its own bytes rather than leaving a reviewer to work it out.
#
# THE MEANINGS ARE STATED HERE AND THE VOCABULARY IS DERIVED. `sanitization_
# tokens()` reads the sealer's own tables; a token it finds with no entry
# below is a REFUSAL, exactly as an undefined replay root is. The second
# element is the replay root the token names the SAME directory as, or "" when
# it names no replay root at all.
SANITIZATION_MEANINGS: dict[str, tuple[str, str]] = {
    "$REPO": (
        "the checkout `sanitize-and-seal.py --repo` was pointed at, which "
        "this pipeline binds to the implementation clone",
        "CANDIDATE_REPO"),
    "$WORKSPACE": (
        "the workspace root that CONTAINS the checkouts and the anchor. It "
        "is a PREFIX of the replay roots and equal to none of them",
        ""),
    "$EVIDENCE": (
        "the lane's agent evidence directory, the `.agents/<lane>` segment. "
        "It is NOT the tools anchor: the sealer's rule matches that directory "
        "segment and nothing else",
        ""),
    "$SCRATCH": (
        "a builder-local temporary root; nothing under it is shipped and no "
        "authoritative claim rests on it",
        ""),
    "$HOME": (
        "the builder's home directory; nothing under it is shipped and no "
        "authoritative claim rests on it",
        ""),
}
# The meaning of a replay root that the ledgers do not define themselves,
# because the phase that uses it writes no `root=` line: `assemble.sh` binds
# `$PACKAGE_ROOT` in its package-phase records and there is no battery ledger
# to declare it.
REPLAY_ROOT_FALLBACKS: dict[str, str] = {
    "PACKAGE_ROOT": "the package directory itself, which the package-phase "
                    "commands ran inside",
}
_DOLLAR_TOKEN = re.compile(r"\$([A-Z][A-Z0-9_]*)")


def sanitization_tokens() -> list[str]:
    """The path-shaped tokens the SEALER can emit, derived from its own tables.

    Three independent readings of the same module, unioned, so a token added
    to any one of them appears here without this function being edited:

      * every string replacement in `rules()` -- the substitutions themselves;
      * every `PLACEHOLDER_*` constant whose value is path-shaped;
      * the `EXTERNAL_REFERENCE` pattern, which is the sealer's own list of
        the placeholders a reference check must not mistake for a member.

    `rules()` also carries CALLABLE replacements -- `_scratch` is one -- whose
    output cannot be read from the table. That is precisely why the other two
    readings are unioned in: `$SCRATCH` is named by both of them.
    """
    sealer = load_sealer()
    found: set[str] = set()
    for _pattern, replacement in sealer.rules(sealer.identities(),
                                              sealer.repo_root()):
        if isinstance(replacement, str):
            found |= {f"${one}" for one in _DOLLAR_TOKEN.findall(replacement)}
    for name in dir(sealer):
        if not name.startswith("PLACEHOLDER_"):
            continue
        value = getattr(sealer, name)
        if isinstance(value, str) and value.startswith("$"):
            found |= {f"${one}" for one in _DOLLAR_TOKEN.findall(value)}
    pattern = getattr(sealer, "EXTERNAL_REFERENCE", None)
    if pattern is not None:
        found |= {f"${one}"
                  for one in _DOLLAR_TOKEN.findall(
                      getattr(pattern, "pattern", "").replace("\\$", "$"))}
    return sorted(found)


def token_legend(defined_roots: dict[str, str],
                 used: set[str]) -> tuple[list[str], list[str]]:
    """BOTH VOCABULARIES, DERIVED, WITH THE MAPPING STATED. And the refusals.

    `defined_roots` is what the ordering ledgers declared; `used` is every
    `$NAME` a rendered command record actually referenced, so a root a
    package-phase record binds appears even though no battery declared it.

    Three refusals, and each is a real defect rather than a tidiness rule:
      1. a replay root used or declared with no meaning available anywhere --
         the legend would be incomplete and a reader could not bind it;
      2. a sanitization token the sealer can emit with no legend entry -- the
         package would ship a token it does not explain;
      3. a name that is BOTH a replay root and a sanitization token -- ONE
         NAME MEANING TWO DIRECTORIES, which is V15's defect exactly.
    """
    problems: list[str] = []
    roots = dict(defined_roots)
    for name in sorted(used - set(roots)):
        if name in REPLAY_ROOT_FALLBACKS:
            roots[name] = REPLAY_ROOT_FALLBACKS[name]
        else:
            problems.append(
                f"a recorded command references ${name} and no ledger `root=` "
                f"line defines it; every replay root is defined once, in "
                f"words, or a reader cannot bind it")
    tokens = sanitization_tokens()
    unexplained = [one for one in tokens if one not in SANITIZATION_MEANINGS]
    for one in unexplained:
        problems.append(
            f"the sanitizer can emit {one} and this legend has no entry for "
            f"it; a package that ships a token it does not explain is a "
            f"package whose reader has to guess what a path means")
    both = sorted({f"${one}" for one in roots} & set(tokens))
    for one in both:
        problems.append(
            f"{one} is BOTH a replay root and a sanitization token; one name "
            f"means one directory, and a name that is a binding in a command "
            f"record and a substitution in a transcript is the V15 $REPO "
            f"defect under a new spelling")

    out = [
        "REPLAY ROOTS -- BIND THESE TO RUN A RECORDED COMMAND. Every path in",
        "every row above is written against one of these and never as an",
        "absolute path. V15 overloaded one name, $REPO, for both the parent",
        "checkout and the candidate checkout inside a single row; these names",
        "are disjoint and the composer refuses a second, different definition",
        "of any of them.",
        "",
    ]
    for name in sorted(roots):
        out.append(f"  ${name} -- {roots[name]}")
    if not roots:
        out.append("  (no root definitions were recorded by either battery)")
    out += [
        "",
        "SANITIZATION TOKENS -- THESE APPEAR IN TRANSCRIPT PROSE, NEVER IN A",
        "COMMAND RECORD. They are privacy SUBSTITUTIONS, not bindings: a",
        "private path was removed at P2 and the token stands where it was.",
        "Nothing binds them and `replay-command.py` takes no --root for one.",
        "The list below is derived from the sealer's own substitution table,",
        "so a token it can emit and this legend does not explain is refused",
        "rather than shipped.",
        "",
    ]
    for one in sorted(tokens):
        said, same = SANITIZATION_MEANINGS.get(one, ("(no legend entry)", ""))
        if same and same in roots:
            out.append(f"  {one} == ${same} -- {said}")
        else:
            out.append(f"  {one} -- {said}")
    if not tokens:
        out.append("  (the sealer declares no path-shaped substitutions)")
    reserved = sorted(one for one in tokens
                      if one.lstrip("$") in CC.RESERVED_VARIABLES)
    unreserved = sorted(one for one in tokens
                        if one.lstrip("$") not in CC.RESERVED_VARIABLES)
    out += [
        "",
        "  THE TWO VOCABULARIES ARE DISJOINT BY DESIGN, AND THE DESIGN IS",
        "  ENFORCED IN BOTH DIRECTIONS. Of the substitution tokens above,",
        "  " + (", ".join(reserved) or "(none)"),
        "  are names `catena_command.py` REFUSES a command record to define,",
        "  so a name that stands for a removed path in a transcript can never",
        "  also be a binding in a record; "
        + (", ".join(unreserved) or "(none)"),
        "  are shell-standard roots no record binds either. The scopes never",
        "  meet, and no name in this package means two directories. Where a",
        "  token and a replay root do name the SAME directory it is written",
        "  `==` above -- that correspondence is stated, not left to a reader",
        "  to infer from two members that use two spellings.",
    ]
    return out, problems


def write_log_index(logs: Path, batteries: list[tuple[str, dict, list[dict]]],
                    log_root: str, shipped_attempts: bool) -> Path:
    """`logs/LOG-INDEX.md`, derived from the ledgers and from the directory.

    NO COMMAND TEXT LIVES HERE, deliberately. The consistency audit reads
    every package-relative path a DOCUMENT names and requires it to exist; a
    recorded command contains bare artifact names that are arguments, not
    members — the browser gate's own note names `browser-gate-head.json`
    without its directory — and a document that repeated them would be
    audited as though the package had promised them. The exact command string
    is in `checks.txt`, verbatim, on the row for the same log, and in
    `logs/attempts.json` as data.
    """
    # EVERY PATH IN THIS DOCUMENT IS BACKTICKED, and that is load-bearing
    # twice over: the sealer's reference audit reads backticked artifact
    # names and requires them to exist, and the consistency audit's path
    # pattern would otherwise swallow a trailing full stop into the name.
    out: list[str] = [
        "# Log index",
        "",
        "DERIVED, NOT TYPED. `logs/checks.py` writes this file from the two",
        "battery ordering ledgers and from this directory, in the same pass",
        "that composes `checks.txt`. Every log the package ships is listed",
        "here with the attempt that produced it. This index is",
        "`logs/LOG-INDEX.md`.",
        "",
        "NAMING. Every attempt writes into a root of its own under `logs/`,",
        "named attempt- followed by the two-digit ATTEMPT ORDINAL, and a",
        "battery transcript inside it is <slug>-<side>.log. The ordinal names",
        "THE ATTEMPT, not the position of the step: it is allocated from the",
        "append-only attempt ledger that lives outside the package, so a rerun",
        "-- including a rerun against a fresh logs directory -- receives a new",
        "root and cannot reuse a path. Within one attempt a transcript is",
        "keyed by its slug, so a step means the same thing on both sides; the",
        "two sides are two attempts and therefore carry two ordinals, which is",
        "why the roots differ between them.",
        "",
        "WHY THE ORDINAL IS THE DIRECTORY. V11 put it in the battery filename",
        "and left the package-phase transcripts -- the gate comparison, the",
        "sealer tests, the seal passes, the derivation, the consistency audit",
        "-- with no ordinal at all. In the reviewed package the",
        "gate-comparison transcript was claimed by six different attempts and",
        "the sealer-tests transcript by five: a failed attempt's logs did not",
        "stay with that attempt, the next attempt opened the same path and",
        "overwrote them. The root carries the ordinal now, so battery and",
        "package phases are carried by one rule instead of one and none, and",
        "`logs/checks.py --audit-logs` refuses a package in which any",
        "transcript is claimed by other than exactly one attempt.",
        "",
        "WHERE THE COMMANDS ARE. The exact command string of every row below",
        "is recorded verbatim in `checks.txt`, on the row for the same log.",
    ]
    if shipped_attempts:
        out += [
            "It is also carried as data in `logs/attempts.json`, together",
            "with the disposition of every attempt this package was built",
            "from. Commands are NOT repeated in this document: a recorded",
            "command contains bare artifact names that are its arguments and",
            "not members of this package, and the audits that read documents",
            "would read them as promises the package had made.",
        ]
    out.append("")

    accounted: set[str] = set()
    for label, meta, rows in batteries:
        out += [f"## {label} battery", ""]
        if not rows:
            out += ["(the ledger for this battery is not present)", ""]
            continue
        out += [
            f"- ledger: `logs/order-{label.lower()}.txt`",
            f"- attempt: {meta.get('attempt', '(not recorded)')}",
            # THE ROOT'S NAME, NOT ITS PATH. `logs/attempt-NN` is a DIRECTORY,
            # and the consistency audit resolves every package-relative path a
            # document names against the FILES the package contains -- so
            # writing the path here reported the attempt's own root as a
            # member the package does not have, once per battery.
            f"- log root: {Path(meta.get('root', '')).name or '(not recorded)'}"
            f" (under logs/)",
            f"- tree at preflight: {meta.get('porcelain', '(not recorded)')}",
            f"- tree at postflight: "
            f"{meta.get('end_porcelain', '(not recorded)')}",
            "",
        ]
        if meta.get("discarded"):
            out += [
                "- THIS ATTEMPT IS DISCARDED: "
                + meta.get("discard_reason", "(no reason recorded)"),
                "",
            ]
        for row in rows:
            end = "-parent" if label == "PARENT" else "-head"
            log = resolve_log(logs, row, end)
            relative = log.relative_to(logs).as_posix()
            accounted.add(relative)
            out.append(
                f"- `logs/{relative}`"
                + ("" if log.is_file() else "   (NOT SHIPPED)"))
            out.append(
                f"    - slug {row['slug']}; order {row.get('order', '?')};"
                f" exit {row.get('exit', '?')};"
                f" attempt {meta.get('attempt', '(not recorded)')}")
            out.append(
                f"    - tree before {row.get('tree_before', '(not recorded)')};"
                f" after {row.get('tree_after', '(not recorded)')}")
        out.append("")

    out += ["## Everything else this directory carries", "",
            "- `logs/LOG-INDEX.md` -- this index, written after the roster "
            "below was taken",
            ]
    for path in sorted(logs.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(logs).as_posix()
        if relative in accounted or "__pycache__" in path.parts:
            continue
        role = ""
        for suffix, said in ROLES:
            if path.suffix == suffix:
                role = said
                break
        if not role:
            if path.name.startswith("browser-gate-"):
                role = ("the gate's own JSON report, written by the recorded "
                        "command; the log beside it is the short transcript")
            elif path.name.startswith("order-"):
                role = "the ordering ledger one battery wrote as it ran"
            elif path.name == "attempts.json":
                role = ("the attempt ledger rows this package was built from, "
                        "composed after the consistency audit")
            elif path.name == "LOG-INDEX.md":
                role = "this index"
            elif path.name == "gate-comparison.log":
                role = ("P1: the two gate reports compared object for object, "
                        "as a recorded pipeline step")
            elif path.name == "named-commits.json":
                role = "the commits this package discusses, each with a reason"
            else:
                role = "(no role declared for this member)"
        out.append(f"- `logs/{relative}` -- {role}")
    out.append("")
    out += [
        "## Declared, and written after this index",
        "",
        "These members do not exist when this index is composed at P1. They",
        "are named here as declarations, exactly as `logs/assemble.sh`",
        "declares them deferred, and the phase that writes each is stated:",
        "",
    ]
    for relative, said in DEFERRED_LOGS:
        out.append(f"- `{relative.format(log_root=log_root)}` -- {said}")
    out.append("")
    path = logs / "LOG-INDEX.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def battery_attempts(logs: Path) -> set[str]:
    """The attempt ids the two staged battery ledgers name."""
    found: set[str] = set()
    for name in ("order-parent.txt", "order-head.txt"):
        meta, _rows = ledger(logs / name)
        if meta.get("attempt"):
            found.add(str(meta["attempt"]))
    return found


def log_root_for(attempt_no: str) -> str:
    """`logs/attempt-NN` for the ordinal the ledger allocated."""
    if not str(attempt_no).isdigit():
        raise SystemExit("--attempt-no is required: every transcript this "
                         "attempt writes lives under its own log root, and "
                         "the ordinal is what names it")
    return f"logs/attempt-{int(attempt_no):02d}"


def audit_logs_mode(args) -> int:
    rows = read_attempts(args.attempts) if args.attempts else []
    logs = args.package / "logs"
    audited = battery_attempts(logs)
    if args.attempt:
        audited.add(str(args.attempt))
    problems = audit_attempt_logs(args.package, rows, audited)
    print(f"attempt-log audit: {len(audited)} attempt(s) accounted for "
          + ", ".join(sorted(audited)))
    print(f"  problems: {len(problems)}")
    for one in problems:
        print("    " + one)
    if problems:
        print("ATTEMPT-LOG AUDIT FAILED", file=sys.stderr)
        return 1
    return 0


def open_lane_row(lane: str) -> dict:
    """The row a lane ledger opens with, and never carries twice."""
    return {
        "record": LANE_RECORD,
        "lane": lane,
        "opened": datetime.datetime.now(
            datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "note": "This ledger belongs to one lane. Every row below repeats the "
                "lane, an attempt ordinal is allocated once for this lane and "
                "is never reissued -- not to replace a discarded attempt and "
                "not because a ledger file was started again -- and every "
                "attempt in it reaches exactly one terminal disposition, with "
                "a non-empty reason wherever that disposition is not "
                "'complete', 'sealed' or 'authoritative'. logs/checks.py "
                "refuses to "
                "append to this file on behalf of another lane, and refuses "
                "to open a fresh one over it.",
    }



def ledger_facts(path: Path) -> dict:
    """The bytes, the rows and the digest of one ledger file.

    A RETIRED LEDGER IS RETAINED, HASHED AND COUNTED, or it is not retired --
    it is lost. V15 set two ledgers aside and the only surviving statement of
    what was in them is the successor package's PROSE; nothing anywhere ties
    the file on disk to the figures the prose quotes.
    """
    data = path.read_bytes()
    rows = read_attempts(path)
    owners, _malformed = ordinal_owners(rows)
    lane, _said = declared_lane(rows)
    return {
        "path": path.name,
        "bytes": len(data),
        "rows": len(rows),
        "sha256": hashlib.sha256(data).hexdigest(),
        "lane": lane,
        "ordinals_spent": sorted(int(one) for one in owners),
        "attempts": sorted({str(one.get("attempt") or "") for one in rows
                            if one.get("attempt")}),
    }


def append_only_problems(older: list[dict], newer: list[dict]) -> list[str]:
    """Is `newer` an APPEND to `older`, or a replacement of it?

    V16, THE V15 REVIEW: a lane whose ledger was started over three times
    shipped a package calling its history "complete" and "append-only". It was
    neither: no earlier ledger is a prefix of a later one, no attempt id is
    shared between any pair, and ordinals 1 through 6 were reissued.

    APPEND-ONLY IS A PREFIX PROPERTY AND NOTHING ELSE. If the first N rows of
    the successor are not byte-identical to the N rows of the predecessor, a
    row was replaced, and no amount of prose makes the pair append-only. This
    refuses that -- and it refuses it as a FALSE CLAIM rather than as a
    forbidden act, because setting a ledger aside is legitimate. What is not
    legitimate is calling the result one append-only record.
    """
    said: list[str] = []
    if len(newer) < len(older):
        said.append(
            f"the successor carries {len(newer)} row(s) and the predecessor "
            f"{len(older)}: rows were removed, and a record that loses rows "
            f"is not append-only")
    for index, (was, now) in enumerate(zip(older, newer)):
        if was != now:
            said.append(
                f"row {index + 1} differs between the two ledgers: a row was "
                f"REPLACED, not appended to. An append-only record's earlier "
                f"rows are byte-identical in the later file, and this pair is "
                f"not one record")
            break
    if not said and len(newer) == len(older):
        said.append(
            "the two ledgers carry the same rows; the successor appends "
            "nothing and is a copy rather than a continuation")
    return said


def retire_ledger_mode(args) -> int:
    """RETIRE ONE LEDGER INTO ANOTHER, RETAINING AND BINDING WHAT IT SPENT.

    V16, THE V15 REVIEW: "Across three V15 ledgers there are nine package
    attempts ... Ordinals are reused; one retired battery never gets a
    terminal row; completed retired batteries are not classified set-aside."

    All three follow from one thing: a ledger was moved aside by hand and the
    allocator, which can only refuse an ordinal recorded in the file it is
    handed, started again at 1. Ordinal 1 was spent three times in lane V15.

    THIS IS THE VERB THAT MAKES SETTING A LEDGER ASIDE A RECORDED ACT.

      1. The old ledger is AUDITED first. A ledger that does not pass its own
         rules is not retired quietly; the operator is told what is wrong.
      2. Every attempt in it with no terminal row is named. V15 had one -- a
         parent battery with three green steps and no disposition -- and it
         is unresolved to this day.
      3. Every battery that terminated `complete` and whose figures are not
         carried forward is classified `set-aside`, with the reason the
         operator supplies. The word has existed since V13 and V15 used it
         zero times while having two cohorts that needed it.
      4. A terminal `retired` row is appended to the OLD file, so the old
         file says out loud that it stopped.
      5. The NEW ledger opens with a lane row that CARRIES THE OLD ONE'S
         digest, byte count, row count, reason and SPENT ORDINALS -- and the
         allocator unions those forward, so an ordinal spent in a retired
         ledger can never be issued again.
    """
    old_path, new_path = args.retire_ledger, args.to
    if not old_path.is_file():
        print(f"REFUSING: no ledger at {old_path}", file=sys.stderr)
        return 1
    if new_path.exists():
        print(f"REFUSING: {new_path} already exists; a retirement opens a "
              f"FRESH successor, and writing into an existing one is how two "
              f"lanes' records come to share a file", file=sys.stderr)
        return 1
    if not args.reason or not args.reason.strip():
        print("REFUSING: --reason is required. A ledger that stops without "
              "saying why leaves its successor unable to explain the gap, "
              "which is exactly the position V15's prose was in.",
              file=sys.stderr)
        return 1

    rows = read_attempts(old_path)
    lane, said = declared_lane(rows)
    for one in said:
        print(f"REFUSING: {one}", file=sys.stderr)
    if said:
        return 1
    if args.lane and lane and lane != args.lane:
        print(f"REFUSING: {old_path} belongs to lane {lane!r}, not "
              f"{args.lane!r}", file=sys.stderr)
        return 1

    problems = audit_ledger(rows, lane or args.lane, None)
    for one in problems:
        print(f"  retiring ledger reports: {one}")
    resolved = resolve_dispositions(rows)
    unresolved = [name for name, value in sorted(resolved.items())
                  if not value.get("status")
                  or value["status"] not in TERMINAL_STATES
                  | POST_TERMINAL_STATES]
    for name in unresolved:
        print(f"  UNRESOLVED at retirement: {name} reaches no terminal "
              f"disposition; it is retired unresolved and the successor's "
              f"lane row records that")

    # THE SET-ASIDE PASS. A battery that ran green and whose figures are not
    # carried forward has a word for it, and the record uses it.
    set_aside: list[str] = []
    # THE SIDE COMES FROM THE ROWS. `resolve_dispositions` answers how an
    # attempt ended and does not carry the side; reading it from the rows is
    # what makes this pass find the cohorts at all. V15 had exactly two --
    # a parent and a head battery, both `complete`, both declined -- and
    # classified neither, while its PROVENANCE.md said "This lane set no
    # cohort aside" about a lane that had set two aside.
    sides: dict[str, str] = {}
    for row in rows:
        name = str(row.get("attempt") or "")
        if name and row.get("side") and name not in sides:
            sides[name] = str(row["side"])
    for name, value in sorted(resolved.items()):
        side = str(value.get("side") or sides.get(name) or "")
        if not side and "-" in name:
            side = name.split("-", 1)[0]
        if side not in BATTERY_SIDES:
            continue
        if value.get("status") != "complete":
            continue
        set_aside.append(name)

    facts = ledger_facts(old_path)
    facts["unresolved_attempts"] = unresolved
    facts["reason"] = args.reason.strip()
    facts["audit_problems"] = problems

    stamp = datetime.datetime.now(
        datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    with old_path.open("a", encoding="utf-8") as handle:
        for name in set_aside:
            handle.write(json.dumps({
                "record": "state", "lane": lane or args.lane,
                "attempt": name,
                "side": (resolved[name].get("side")
                         or sides.get(name)
                         or (name.split("-", 1)[0] if "-" in name else "")),
                "status": "set-aside", "start": stamp, "end": stamp,
                "reason": (f"this ledger was retired ({facts['reason']}) and "
                           f"no figure in any package derives from this "
                           f"cohort; it ran to completion and its figures "
                           f"were not used"),
            }, sort_keys=True) + "\n")
        handle.write(json.dumps({
            "record": RETIRED_RECORD, "lane": lane or args.lane,
            "retired_at": stamp, "reason": facts["reason"],
            "rows_at_retirement": facts["rows"],
            "bytes_at_retirement": facts["bytes"],
            "ordinals_spent": facts["ordinals_spent"],
            "unresolved_attempts": unresolved,
            "set_aside": set_aside,
            "successor": new_path.name,
            "note": "This ledger stops here. Its successor's opening lane row "
                    "carries this file's digest, byte count, row count and "
                    "spent ordinals, so no ordinal it spent can ever be "
                    "issued again and no reader has to take its contents on "
                    "trust.",
        }, sort_keys=True) + "\n")

    # The digest is taken AFTER the terminal rows are appended, so it
    # describes the file as retired rather than the file as it was a moment
    # before -- the successor binds the artifact a reader will actually open.
    final = ledger_facts(old_path)
    final["reason"] = facts["reason"]
    final["unresolved_attempts"] = unresolved
    final["set_aside"] = set_aside

    opening = open_lane_row(lane or args.lane)
    opening["retired_predecessors"] = [final]
    opening["ordinals_already_spent"] = final["ordinals_spent"]
    opening["note"] += (
        " THIS LEDGER HAS A PREDECESSOR. `retired_predecessors` carries its "
        "digest, byte count, row count, reason and spent ordinals; those "
        "ordinals stay spent and the allocator refuses them here too. The "
        "two files together are the lane's history and neither alone is.")
    new_path.parent.mkdir(parents=True, exist_ok=True)
    new_path.write_text(json.dumps(opening, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"retired {old_path.name} -> {new_path.name}")
    print(f"  bytes {final['bytes']}, rows {final['rows']}, "
          f"sha256 {final['sha256']}")
    print(f"  ordinals carried forward as spent: "
          + (", ".join(f"{one:02d}" for one in final["ordinals_spent"])
             or "(none)"))
    print(f"  set aside: " + (", ".join(set_aside) or "(none)"))
    print(f"  unresolved: " + (", ".join(unresolved) or "(none)"))
    return 0


# THE NINE, IN THE ORDER THEY ARE PRINTED AND SHIPPED. A tuple rather than a
# dict literal's insertion order, because this order is a contract: the
# package quotes these names and a reader compares them line by line.
COUNT_ORDER: tuple[str, ...] = (
    "attempt_count",
    "terminal_execution_disposition_count",
    "unresolved_count",
    "reused_ordinal_count",
    "failed_count",
    "abandoned_count",
    "complete_count",
    "authoritative_evidence_count",
    "set_aside_count",
)


def derive_counts(every: list[dict], reused_ordinals: int) -> dict[str, int]:
    """The nine, derived from the attempts themselves. Nothing here is a
    constant, and nothing folds one disposition into another.

    `every` is one dict per attempt, carrying `execution` and `evidence` as
    `history_table_mode` resolves them: the execution disposition is the
    terminal row and the evidence disposition is what became of the figures.
    An attempt with no terminal row reads `NONE (no terminal row)` and is
    counted `unresolved`, never assumed to have succeeded.
    """
    open_rows = [one for one in every
                 if one["execution"].startswith(("NONE", "INCOHERENT"))]
    terminal_rows = [one for one in every if one not in open_rows]

    def execution(word: str) -> int:
        return sum(1 for one in every if one["execution"] == word)

    def evidence(word: str) -> int:
        return sum(1 for one in every if one["evidence"] == word)

    return {
        "attempt_count": len(every),
        "terminal_execution_disposition_count": len(terminal_rows),
        "unresolved_count": len(open_rows),
        "reused_ordinal_count": reused_ordinals,
        "failed_count": execution("failed"),
        "abandoned_count": execution("abandoned"),
        "complete_count": execution("complete"),
        "authoritative_evidence_count": evidence("authoritative"),
        "set_aside_count": evidence("set-aside"),
    }


def invariant_verdicts(counts: dict[str, int]) -> dict[str, tuple[bool, str]]:
    """The three assertions, each judged MECHANICALLY against the counts.

    They are stated as comparisons between derived figures rather than
    against literals, so a lane that grows an attempt does not need any of
    them rewritten -- which is what makes them assertions about the record
    rather than a second transcription of it.
    """
    return {
        "every attempt reaches exactly one terminal execution disposition": (
            counts["attempt_count"]
            == counts["terminal_execution_disposition_count"],
            f"attempt_count {counts['attempt_count']} == "
            f"terminal_execution_disposition_count "
            f"{counts['terminal_execution_disposition_count']}"),
        "no attempt is left open": (
            counts["unresolved_count"] == 0,
            f"unresolved_count {counts['unresolved_count']} == 0"),
        "no ordinal is carried by two attempts": (
            counts["reused_ordinal_count"] == 0,
            f"reused_ordinal_count {counts['reused_ordinal_count']} == 0"),
    }


def history_table_mode(args) -> int:
    """THE COMPLETE CROSS-LEDGER HISTORY, AS ONE TABLE.

    V16, THE V15 REVIEW: "The advertised five refusals followed by the
    authoritative sixth attempt are only one slice. Across three V15 ledgers
    there are nine package attempts."

    Every earlier auditor in this file reads ONE file, because that is what
    `--seal-ledger` is handed. This reads as many as it is given, in the order
    given, and reports every attempt in all of them under one numbering -- so
    a lane that started its ledger over cannot present the last file's slice
    as the whole history.

    It also states, per adjacent pair, whether the later file is an APPEND to
    the earlier one or a REPLACEMENT of it, and refuses a `--claim-append-only`
    assertion over a pair that is not.
    """
    files = list(args.attempts_list or [])
    if not files:
        print("REFUSING: --history-table wants one or more --attempts paths",
              file=sys.stderr)
        return 1

    loaded: list[tuple[Path, list[dict], dict]] = []
    for one in files:
        if not one.is_file():
            print(f"REFUSING: no ledger at {one}", file=sys.stderr)
            return 1
        loaded.append((one, read_attempts(one), ledger_facts(one)))

    print("LEDGERS, IN THE ORDER GIVEN")
    for path, rows, facts in loaded:
        print(f"  {facts['path']}: {facts['bytes']} bytes, {facts['rows']} "
              f"row(s), lane {facts['lane'] or '(none)'}, sha256 "
              f"{facts['sha256']}")
        print(f"    ordinals spent: "
              + (", ".join(f"{one:02d}" for one in facts["ordinals_spent"])
                 or "(none)"))
    print()

    # APPEND OR REPLACEMENT, per adjacent pair.
    print("BETWEEN EACH PAIR")
    replacements = 0
    for (path_a, rows_a, facts_a), (path_b, rows_b, facts_b) in zip(
            loaded, loaded[1:]):
        said = append_only_problems(rows_a, rows_b)
        if said:
            replacements += 1
            print(f"  {facts_a['path']} -> {facts_b['path']}: REPLACEMENT")
            for one in said:
                print(f"    {one}")
            shared = set(facts_a["attempts"]) & set(facts_b["attempts"])
            print(f"    attempt ids in common: "
                  + (", ".join(sorted(shared)) or "NONE"))
        else:
            print(f"  {facts_a['path']} -> {facts_b['path']}: APPEND "
                  f"(+{len(rows_b) - len(rows_a)} row(s))")
    if not loaded[1:]:
        print("  (one ledger; nothing to compare)")
    print()

    # THE TABLE. One numbering across every file.
    every: list[dict] = []
    for path, rows, facts in loaded:
        resolved = resolve_dispositions(rows)
        firsts: dict[str, str] = {}
        for row in rows:
            name = str(row.get("attempt") or "")
            if name and name not in firsts:
                firsts[name] = str(row.get("start") or row.get("end") or "")
        # THE SIDE AND THE ORDINAL COME FROM THE ROWS, not from the
        # resolution: `resolve_dispositions` answers "how did it end", which
        # is a different question and does not carry either field. Reading
        # them here is what lets the summary say `package_attempts` rather
        # than a single undifferentiated total -- and the V15 prose's whole
        # error was reporting one slice of one kind as the history.
        sides: dict[str, str] = {}
        ordinals: dict[str, str] = {}
        for row in rows:
            name = str(row.get("attempt") or "")
            if not name:
                continue
            if row.get("side") and name not in sides:
                sides[name] = str(row["side"])
            if row.get("attempt_no") and name not in ordinals:
                ordinals[name] = str(row["attempt_no"])
        for name, value in resolved.items():
            status = str(value.get("status") or "")
            # `resolve_dispositions` reports an attempt with no terminal row
            # as a sentence rather than a state; it is normalised here so the
            # summary can count it.
            if not status or status.startswith("unresolved"):
                disposition = "NONE (no terminal row)"
            else:
                disposition = status
            # THE EXECUTION COLUMN IS THE TERMINAL ROW AND NOTHING ELSE.
            # Before V16 this table printed the collapsed last state, so an
            # attempt that COMPLETED and was later set aside appeared in the
            # history as `set-aside` and its execution disposition appeared
            # nowhere at all.
            execution = str(value.get("execution_disposition") or "")
            if not execution:
                execution = ("INCOHERENT" if status.startswith("INCOHERENT")
                             else "NONE (no terminal row)")
            evidence = str(value.get("evidence_disposition")
                           or EVIDENCE_UNSET)
            side = str(value.get("side") or sides.get(name) or "")
            if not side:
                # LAST RESORT, AND SAID OUT LOUD: the id's own prefix. Every
                # attempt id in this lane is `<side>-<stamp>-<ordinal><nonce>`
                # and a row that lost its `side` field still carries it there.
                side = name.split("-", 1)[0] if "-" in name else ""
            every.append({
                "attempt": name,
                "ordinal": str(value.get("attempt_no")
                               or ordinals.get(name, "")),
                "ledger": facts["path"],
                "side": side,
                "start": firsts.get(name, ""),
                "disposition": disposition,
                "execution": execution,
                "evidence": evidence,
                "execution_reason": str(value.get("execution_reason") or ""),
                "evidence_reason": str(value.get("evidence_reason") or ""),
                "reason": str(value.get("reason") or ""),
            })
    every.sort(key=lambda one: (one["start"], one["ledger"], one["attempt"]))

    print("EVERY ATTEMPT, ACROSS EVERY LEDGER, IN START ORDER")
    # TWO DISPOSITION COLUMNS, NEVER ONE. `EXECUTION` is how the attempt
    # terminated; `EVIDENCE` is what became of its measurements. They are
    # different facts about different things and one column could only ever
    # print one of them.
    header = ("#", "ATTEMPT", "ORD", "LEDGER", "SIDE", "START",
              "EXECUTION", "EVIDENCE", "REASON")
    table = [header]
    for index, one in enumerate(every, start=1):
        table.append((str(index), one["attempt"], one["ordinal"],
                      one["ledger"], one["side"], one["start"],
                      one["execution"], one["evidence"], one["reason"][:60]))
    widths = [max(len(row[col]) for row in table)
              for col in range(len(header))]
    for number, row in enumerate(table):
        print("  " + "  ".join(one.ljust(widths[col])
                               for col, one in enumerate(row)).rstrip())
        if number == 0:
            print("  " + "  ".join("-" * one for one in widths))
    print()

    # THE FIGURES, SEPARATELY NAMED. V15's prose said "five refusals then a
    # sixth authoritative attempt" about a nine-attempt history.
    package_attempts = [one for one in every if one["side"] == "package"]
    battery_attempts = [one for one in every
                        if one["side"] in BATTERY_SIDES]
    authoritative = [one for one in package_attempts
                     if one["evidence"] == "authoritative"]
    no_terminal = [one for one in every
                   if one["execution"].startswith(("NONE", "INCOHERENT"))]
    # ABANDONMENT IS NAMED, NEVER FOLDED. V15's prose put nine attempts under
    # two words; a count that hides a disposition inside a neighbouring one is
    # the same defect at a smaller scale.
    abandoned = [one for one in every if one["execution"] == "abandoned"]
    print(f"attempts_total          : {len(every)}")
    print(f"package_attempts        : {len(package_attempts)}")
    print(f"battery_attempts        : {len(battery_attempts)}")
    print(f"attempts_abandoned      : {len(abandoned)}"
          + (" -- " + ", ".join(one["attempt"] for one in abandoned)
             + "; resolved history, and no figure of theirs supports any claim"
             if abandoned else ""))
    print(f"package_authoritative   : {len(authoritative)}")
    print(f"package_non_authoritative: {len(package_attempts) - len(authoritative)}")
    print(f"attempts_with_no_terminal_row: {len(no_terminal)}"
          + (" -- " + ", ".join(one["attempt"] for one in no_terminal)
             if no_terminal else ""))
    print(f"ledger_replacements     : {replacements}")

    # REUSED ORDINALS, ACROSS FILES. Within one file the allocator prevents
    # this; across files nothing did, which is the whole defect.
    by_ordinal: dict[str, set[str]] = {}
    for one in every:
        if one["ordinal"]:
            by_ordinal.setdefault(one["ordinal"], set()).add(one["attempt"])
    reused = {key: value for key, value in by_ordinal.items()
              if len(value) > 1}
    print(f"reused_ordinals         : {len(reused)}")
    for key in sorted(reused, key=lambda one: int(one) if one.isdigit() else 0):
        print(f"  ordinal {key}: " + ", ".join(sorted(reused[key])))
    print()

    # ---- THE NINE COUNTS, EACH SEPARATELY NAMED AND EACH DERIVED ----------
    #
    # NOT ONE OF THESE IS A CONSTANT. Every figure below is computed from the
    # rows the ledgers actually carry, so adding an attempt to the lane
    # changes them without anything being edited -- which is the difference
    # between a package that CARRIES its derivation and a package that ships
    # a transcription of one. V15's own prose is what a transcription looks
    # like when the history moves underneath it.
    #
    # The two axes are counted apart. `complete_count` counts attempts whose
    # EXECUTION disposition is `complete`, whatever became of their figures;
    # `set_aside_count` and `authoritative_evidence_count` count EVIDENCE
    # dispositions, and a `complete` attempt appears in one of the first and
    # at most one of the second. Nothing is folded: an abandoned attempt is
    # in `abandoned_count`, in `terminal_execution_disposition_count`, and in
    # no evidence tally at all.
    counts = derive_counts(every, len(reused))
    for key in COUNT_ORDER:
        print(f"{key:<38}: {counts[key]}")
    print()
    print("INVARIANTS")
    verdicts = invariant_verdicts(counts)
    for name, (ok, said) in verdicts.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {said}")
    failed = [name for name, (ok, _said) in verdicts.items() if not ok]
    print(f"  invariants: {len(verdicts) - len(failed)} of {len(verdicts)} "
          f"PASS" + (" -- FAILING: " + ", ".join(failed) if failed else ""))

    if args.json is not None:
        # THE MACHINE-READABLE FORM, so the package can carry the DERIVATION
        # rather than a sentence about it. Same numbers, same names, from the
        # same pass -- there is no second computation to drift.
        payload = {
            "schema": "catena/attempt-history/2",
            "lane": args.lane or "",
            "ledgers": [{"path": facts["path"], "sha256": facts["sha256"],
                         "bytes": facts["bytes"], "rows": facts["rows"],
                         "lane": facts["lane"],
                         "ordinals_spent": facts["ordinals_spent"]}
                        for _path, _rows, facts in loaded],
            "ledger_replacements": replacements,
            "reused_ordinals": {key: sorted(value)
                                for key, value in sorted(reused.items())},
            "attempts": [{"attempt": one["attempt"],
                          "ordinal": one["ordinal"],
                          "ledger": one["ledger"],
                          "side": one["side"],
                          "start": one["start"],
                          "execution_disposition": one["execution"],
                          "execution_reason": one["execution_reason"],
                          "evidence_disposition": one["evidence"],
                          "evidence_reason": one["evidence_reason"]}
                         for one in every],
            "counts": {key: counts[key] for key in COUNT_ORDER},
            "invariants": {name: {"pass": ok, "statement": said}
                           for name, (ok, said) in verdicts.items()},
            "verdict": "PASS" if not failed else "FAIL",
        }
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2, sort_keys=True)
                             + "\n", encoding="utf-8")
        print(f"derivation written to {args.json}")

    if args.assert_invariants and failed:
        print("REFUSING: the derived history breaks "
              f"{len(failed)} invariant(s): " + ", ".join(failed)
              + ". Every attempt reaches exactly one terminal execution "
                "disposition, none is left open, and no ordinal is carried "
                "by two attempts.", file=sys.stderr)
        return 1
    if args.claim_append_only and (replacements or reused):
        print("REFUSING: --claim-append-only was asserted over a history "
              "that is not one append-only record: "
              f"{replacements} replacement(s), {len(reused)} reused "
              f"ordinal(s). Setting a ledger aside is legitimate; calling "
              f"the result one append-only history is not.", file=sys.stderr)
        return 1
    return 0


def allocate_ordinal_mode(args) -> int:
    """ALLOCATE THE NEXT ORDINAL FOR THIS LANE, OR REFUSE. Prints the number.

    This is the one place an ordinal is allocated, and `battery.sh` calls it
    rather than recomputing `max(attempt_no) + 1` over whatever file it was
    pointed at -- which is exactly what V12 did, over a ledger the operator had
    just started fresh, reissuing 03/04/05/06 as 03/04/05.

    Three refusals: a ledger of another lane, a fresh ledger requested over an
    existing one, and a proposed ordinal any row has ever carried. Nothing here
    is advisory: the caller gets a number on stdout or a nonzero exit.
    """
    path = args.attempts
    if path is None:
        print("REFUSING: --attempts is required to allocate an ordinal",
              file=sys.stderr)
        return 1
    if not args.lane:
        print("REFUSING: --lane is required; an ordinal is allocated for a "
              "lane, and a ledger that does not name its lane cannot say "
              "whose allocation it carries", file=sys.stderr)
        return 1
    rows = read_attempts(path)
    if path.is_file() and rows and args.fresh:
        print(f"REFUSING: {path} already exists and carries {len(rows)} "
              f"row(s); --fresh asks for a new lane ledger and this would "
              f"discard one. Starting a lane's record over is not something "
              f"this pipeline does silently: move the old file aside "
              f"deliberately, under a name that says what it is, and note the "
              f"ordinals it spent -- they stay spent.", file=sys.stderr)
        return 1
    if not path.is_file() or not rows:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(open_lane_row(args.lane),
                                    sort_keys=True) + "\n")
        print(f"opened lane ledger {path} for lane {args.lane}",
              file=sys.stderr)
        rows = read_attempts(path)
    ledger_lane, said = declared_lane(rows)
    if said:
        for one in said:
            print(f"REFUSING: {one}", file=sys.stderr)
        return 1
    if ledger_lane != args.lane:
        print(f"REFUSING: {path} belongs to lane {ledger_lane!r}, not "
              f"{args.lane!r}. A lane appends to its own ledger and to no "
              f"other; pointing two lanes at one file is how one lane's "
              f"ordinals come to describe another's attempts.",
              file=sys.stderr)
        return 1
    owners, malformed = ordinal_owners(rows)
    for one in malformed:
        print(f"REFUSING: {one}", file=sys.stderr)
    if malformed:
        return 1
    spent = {int(key) for key in owners}
    # V16: AN ORDINAL SPENT IN A RETIRED PREDECESSOR STAYS SPENT.
    #
    # This is the whole of V15's ordinal defect. `spent` was derived from the
    # file this allocator was handed, so moving a ledger aside emptied it and
    # `max(spent) + 1` started again at 1. Ordinal 1 was issued three times in
    # lane V15, ordinals 2 through 6 twice each, and the identity row of every
    # one of the three files says an ordinal "is never reissued". The
    # retirement verb writes the predecessor's spent ordinals into the
    # successor's opening lane row, and they are unioned in here.
    carried: set[int] = set()
    for row in rows:
        if row.get("record") != LANE_RECORD:
            continue
        for one in row.get("ordinals_already_spent") or []:
            try:
                carried.add(int(one))
            except (TypeError, ValueError):
                continue
        for old_ledger in row.get("retired_predecessors") or []:
            if not isinstance(old_ledger, dict):
                continue
            for one in old_ledger.get("ordinals_spent") or []:
                try:
                    carried.add(int(one))
                except (TypeError, ValueError):
                    continue
    for one in sorted(carried - spent):
        owners.setdefault(f"{one:02d}", set()).add(
            "a retired predecessor ledger of this lane")
    spent |= carried
    if args.propose:
        try:
            wanted = int(args.propose)
        except ValueError:
            print(f"REFUSING: proposed ordinal {args.propose!r} is not a "
                  f"number", file=sys.stderr)
            return 1
        if wanted in spent:
            print(f"REFUSING: attempt ordinal {wanted:02d} has already been "
                  f"carried by " + ", ".join(sorted(owners[f"{wanted:02d}"]))
                  + ". An ordinal is allocated once for lane "
                  f"{args.lane} and is never reissued, however that attempt "
                  f"ended; reusing one makes two attempts answer to one name "
                  f"and one log root.", file=sys.stderr)
            return 1
    else:
        wanted = (max(spent) + 1) if spent else 1
    if wanted > 99:
        print(f"REFUSING: attempt ordinal {wanted} exceeds the two-digit "
              f"prefix the log roots carry", file=sys.stderr)
        return 1
    print(wanted)
    return 0


def verify_ledger_mode(args) -> int:
    """THE LEDGER, AUDITED AS A RECORD AND AS A STATE MACHINE, writing nothing.

    Runs standalone so an operator -- or a test -- can put a ledger, or a
    package's shipped `logs/attempts.json`, in front of the same rules
    `--seal-ledger` enforces, without a package being sealed around it.

    THE SCOPE IS INFERRED AND OVERRIDABLE. Reading a package's own
    `logs/attempts.json` is by definition reading package bytes, so that is
    `in-package` and `authoritative` is refused there; reading a bare ledger
    file is reading the external complete ledger, where the post-P8 row
    belongs. `--in-package` forces the strict reading either way.
    """
    rows: list[dict] = []
    scope = EXTERNAL
    frozen_at = instant(args.frozen_at) if args.frozen_at else None
    if args.attempts and args.attempts.is_file():
        rows = read_attempts(args.attempts)
    elif args.package and (args.package / "logs" / "attempts.json").is_file():
        member = json.loads((args.package / "logs" / "attempts.json")
                            .read_text(encoding="utf-8"))
        rows = list(member.get("rows", []))
        scope = IN_PACKAGE
        if frozen_at is None:
            frozen_at = instant(member.get("frozen_at", ""))
    else:
        print(f"REFUSING: no attempt ledger at {args.attempts} and no "
              f"logs/attempts.json in {args.package}", file=sys.stderr)
        return 1
    if args.in_package:
        scope = IN_PACKAGE
    problems = audit_ledger(rows, args.lane, frozen_at)
    problems += audit_authority(rows, scope)
    lane_name, _said = declared_lane(rows)
    print(f"ledger audit: lane {lane_name or '(none declared)'}, "
          f"{len(rows)} row(s), scope {scope}, frozen_at "
          f"{frozen_at.isoformat() if frozen_at else '(not stated)'}")
    # BOTH AXES, ALWAYS, AND NEVER ONE COLLAPSED INTO THE OTHER. Before V16
    # this printed the LAST state, so an attempt that ran to completion and
    # whose figures were later declined printed `set-aside` and the fact that
    # it completed was not on the line at all.
    resolved = resolve_dispositions(rows)
    for attempt, value in sorted(resolved.items()):
        print("  " + two_axis_line(attempt, value))
    print("  " + resolution_counts(resolved))
    print(f"  problems: {len(problems)}")
    for one in problems:
        print("    " + one)
    if problems:
        print("LEDGER AUDIT FAILED", file=sys.stderr)
        return 1
    return 0


def seal_ledger_mode(args) -> int:
    """The authority audit, then the shipped ledger. In that order, always.

    Refusing AFTER writing the member would ship the member the audit refused,
    which is how the reviewed package came to carry three authoritative
    attempts and describe itself as unresolved.

    V13: the record audit runs here too, and the freeze instant is REAL. The
    member is stamped with the instant it is written at, and a row that ends
    after that instant is refused rather than shipped -- V12 stamped attempt
    04's supersession 30 seconds after the freeze its own member described.

    V13, PACKAGE SIDE: this reads the ledger in `in-package` scope, because
    what it is about to write is package bytes. The sealing attempt must
    resolve to `sealed`, not `authoritative`: P6, P7 and P8 have not run, and
    a member frozen here cannot carry their verdict.
    """
    if not args.attempts or not args.attempts.is_file():
        print(f"REFUSING: no attempt ledger at {args.attempts}",
              file=sys.stderr)
        return 1
    rows = read_attempts(args.attempts)
    frozen_at = datetime.datetime.now(datetime.timezone.utc)
    problems = audit_ledger(rows, args.lane, frozen_at)
    problems += audit_authority(rows, IN_PACKAGE)
    dispositions = resolve_dispositions(rows)
    mine = dispositions.get(args.attempt, {})
    if str(mine.get("status", "")) == "authoritative":
        # NAMED SEPARATELY FROM THE GENERIC MISMATCH BELOW, because this is
        # the one an operator is most likely to reach for out of habit and the
        # one the review is actually about.
        problems.append(
            f"{args.attempt}: this is the SEALING attempt and it claims "
            f"'authoritative'. P6, P7 and P8 have not run -- this member is "
            f"frozen before the manifest, the archive and the verification -- "
            f"so the claim is a verdict nobody has yet. Write status=sealed "
            f"here; append the post-P8 authoritative row to the external "
            f"ledger, with the <package>.authority.json sidecar, once P8 "
            f"has actually passed")
    elif mine.get("status") != "sealed":
        problems.append(
            f"{args.attempt}: this is the sealing attempt and it resolves to "
            f"{mine.get('status', '(no rows at all)')!r}, not 'sealed'; the "
            f"terminal row is appended before this member is composed, not "
            f"after P8")
    terminal = [row for row in rows
                if str(row.get("attempt", "")) == args.attempt
                and row.get("record") == "attempt"]
    for row in terminal:
        if str(row.get("package", "")) != args.package_name:
            problems.append(
                f"{args.attempt}: its terminal row names package "
                f"{row.get('package', '(none)')!r}, not {args.package_name!r}")
        if str(row.get("head", "")) != args.head:
            problems.append(
                f"{args.attempt}: its terminal row names head "
                f"{row.get('head', '(none)')!r}, not {args.head!r}")
    print(f"authority audit: {len(dispositions)} attempt(s) in the ledger")
    for attempt, value in sorted(dispositions.items()):
        print(f"  {attempt}: {value['execution_disposition'] or value['status']}"
              f" | evidence {value['evidence_disposition']}")
    print("  " + resolution_counts(dispositions))
    print(f"  problems: {len(problems)}")
    for one in problems:
        print("    " + one)
    if problems:
        print("AUTHORITY AUDIT FAILED", file=sys.stderr)
        return 1
    logs = args.package / "logs"
    wanted = battery_attempts(logs)
    path = write_attempts(logs, rows, wanted, args.attempt, frozen_at,
                          args.lane or declared_lane(rows)[0])
    print(f"logs/{path.name} composed from the ledger outside the package, "
          f"pre-normalized, carrying this attempt's own terminal row")
    print(f"  frozen_at {frozen_at.isoformat()}; the phases that run after "
          f"this instant are declared in it by name ("
          + ", ".join(phase for phase, _why in PHASES_AFTER_FREEZE)
          + "), not silently omitted")
    return 0


def abandon_attempt_mode(args) -> int:
    """GIVE AN INTERRUPTED ATTEMPT ITS TERMINAL ROW, WITH ITS REASON.

    V16, THE V15 REVIEW: "one retired battery never gets a terminal row".
    `--retire-ledger` can REPORT such an attempt, and does; it cannot fix one,
    because retiring a whole ledger to close a single interrupted run is not a
    proportionate act and leaves the attempt unresolved in the retired file
    anyway. Until this verb existed the tooling could express abandonment only
    as the absence of a row, which is the very shape the review refused: a
    reader cannot tell an abandoned attempt from a lost one, and the audit can
    only say `unresolved`.

    An attempt is abandoned when something outside the battery stopped it -- a
    killed process, a lost handle, an operator interrupt. That is a real
    disposition and it is recorded as one, in words, on a row of its own. It is
    NOT `discarded`, which the battery writes about its own refusals and which
    asserts the run reached a decision; abandonment asserts only that the run
    stopped and that nothing derives from it.
    """
    path, attempt = args.attempts, args.abandon_attempt
    if not path or not path.is_file():
        print(f"REFUSING: no ledger at {path}", file=sys.stderr)
        return 1
    reason = " ".join((args.reason or "").split())
    if len(reason) < 40 or len(reason.split()) < 8:
        print("REFUSING: --abandon-attempt wants --reason, and a substantive "
              "one -- at least forty characters over at least eight words. An "
              "attempt abandoned without a stated reason is the defect this "
              "verb exists to close, and a token reason is a shorter way to "
              "write the same silence", file=sys.stderr)
        return 1
    rows = read_attempts(path)
    stated = [r.get("lane") for r in rows if r.get("record") == "lane"]
    lane = args.lane or (stated[0] if stated else None)
    if not lane:
        print("REFUSING: --abandon-attempt wants --lane, and the "
              "ledger states none", file=sys.stderr)
        return 1
    mine = [r for r in rows if r.get("attempt") == attempt]
    if not mine:
        print(f"REFUSING: {path} carries no attempt {attempt}", file=sys.stderr)
        return 1
    wrong = sorted({r.get("lane") for r in mine} - {lane, None})
    if wrong:
        print(f"REFUSING: {attempt} belongs to lane {wrong[0]}, not {lane}",
              file=sys.stderr)
        return 1
    # NOTHING FAILED, OR THIS IS NOT AN ABANDONMENT. A battery FAILS when a
    # step it ran returned non-zero or one of its own guards refused: the run
    # reached a decision and the record can name the step that made it. It is
    # ABANDONED only when something outside it stopped it and no step failed at
    # all. Offering abandonment for a run that refused something would let the
    # softer word cover a real refusal, which is the opposite of the closure.
    #
    # A NON-ZERO STEP EXIT IS NOT A FAILED STEP, and reading it as one would
    # make this verb unusable and its refusal a false statement. This battery
    # runs every step and records the exit each returned; four gates in this
    # repository are inherited-red by design and return 2, 2, 1 and 2 at BOTH
    # endpoints, and an attempt that ran them all and finished is `complete`.
    # What says a run reached a decision is a DISPOSITION -- a row carrying
    # `failed` or `discarded`, or a result the battery wrote as a refusal --
    # which is what the battery writes when one of its own guards refuses, and
    # what attempt 01 of this lane carries. That is the thing this guard reads.
    hurt = []
    for r in mine:
        if str(r.get("status", "")) in {"failed", "discarded"}:
            hurt.append(f"{r.get('phase', '?')} recorded "
                        f"{r.get('status')!r}")
        result = str(r.get("result", "")).strip()
        if result.upper().startswith(("REFUSED", "FAILED")):
            hurt.append(f"{r.get('phase', '?')} recorded {result[:40]!r}")
    if hurt:
        print(f"REFUSING: {attempt} carries a step that did not pass "
              f"({'; '.join(hurt)}); an attempt whose own run reached a "
              f"decision is failed or discarded, not abandoned, and the "
              f"disposition that names the decision is the truthful one",
              file=sys.stderr)
        return 1
    already = [r for r in mine if r.get("record") == "attempt"]
    if already:
        print(f"REFUSING: {attempt} already reaches a terminal disposition "
              f"({already[0].get('status')}); every attempt reaches exactly "
              f"one, and rewriting that is what an append-only ledger forbids",
              file=sys.stderr)
        return 1
    seed = mine[0]
    row = {
        "lane": lane,
        "record": "attempt",
        "attempt": attempt,
        "status": "abandoned",
        "phase": "battery" if seed.get("side") in BATTERY_SIDES else "package",
        "reason": reason,
        "steps_recorded": str(sum(1 for r in mine
                                  if r.get("record") == "step")),
    }
    for key in ("attempt_no", "side", "sha", "cwd"):
        if seed.get(key):
            row[key] = seed[key]
    # AND WHERE ITS TRANSCRIPTS ARE, in the same write. Ending an attempt
    # leaves a log root the next package cannot stage, and the record owes the
    # same sentence whichever path ended it -- the assembler's three write it,
    # and this verb ending one by hand is the fourth. It was the fourth to be
    # noticed, after an assembly was refused for a root this verb had left
    # unexplained.
    note = {
        "lane": lane, "record": "note", "attempt": attempt,
        "phase": "attempt-log audit",
        "log_root_elsewhere":
            "this attempt was stopped before it finished and was abandoned; "
            "whatever it had written is kept where it lies, outside any "
            "package, it was never staged, and none of its bytes is evidence "
            "for any claim",
    }
    for key in ("attempt_no", "side"):
        if seed.get(key):
            note[key] = seed[key]
    already_said = any(str(r.get("log_root_elsewhere", "")).strip()
                       for r in mine)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        if not already_said:
            handle.write(json.dumps(note, sort_keys=True) + "\n")
    print(f"abandoned {attempt} in {path.name}")
    print(f"  steps recorded before it stopped: {row['steps_recorded']}")
    print(f"  reason: {reason}")
    return 0


def set_aside_attempt_mode(args) -> int:
    """SAY THAT A COMPLETED COHORT'S FIGURES WERE DECLINED, ON A ROW.

    V16, THE V15 REVIEW: "completed retired batteries are not classified
    set-aside". The word has existed since V13; V15 used it zero times while
    holding two cohorts that needed it, and its record said in prose that it
    had set none aside. `--retire-ledger` can apply the word to a whole
    ledger's cohorts, which is the right act when a ledger stops -- and it is
    the WRONG act when one battery of a live ledger is declined, because
    retiring a ledger to classify one attempt rewrites a record to make it
    tidy. This is the verb for that case, and it appends.

    `set-aside` is POST-TERMINAL. The battery did complete, the terminal row
    still says so, and this row records what became of its figures. That
    distinction is why the two are separate rows rather than one amended one:
    whether a cohort's figures are carried is not known while it runs.
    """
    path, attempt = args.attempts, args.set_aside_attempt
    if not path or not path.is_file():
        print(f"REFUSING: no ledger at {path}", file=sys.stderr)
        return 1
    reason = " ".join((args.reason or "").split())
    if len(reason) < 40 or len(reason.split()) < 8:
        print("REFUSING: --set-aside-attempt wants --reason, and a substantive "
              "one -- at least forty characters over at least eight words. A "
              "cohort set aside without a stated reason is a figure withdrawn "
              "with no account of why", file=sys.stderr)
        return 1
    rows = read_attempts(path)
    stated = [r.get("lane") for r in rows if r.get("record") == "lane"]
    lane = args.lane or (stated[0] if stated else None)
    if not lane:
        print("REFUSING: --set-aside-attempt wants --lane, and the ledger "
              "states none", file=sys.stderr)
        return 1
    mine = [r for r in rows if r.get("attempt") == attempt]
    if not mine:
        print(f"REFUSING: {path} carries no attempt {attempt}", file=sys.stderr)
        return 1
    wrong = sorted({r.get("lane") for r in mine} - {lane, None})
    if wrong:
        print(f"REFUSING: {attempt} belongs to lane {wrong[0]}, not {lane}",
              file=sys.stderr)
        return 1
    seed = mine[0]
    if seed.get("side") not in BATTERY_SIDES:
        print(f"REFUSING: {attempt} is a {seed.get('side')} attempt; "
              f"`set-aside` is battery vocabulary and a package attempt is "
              f"superseded instead", file=sys.stderr)
        return 1
    terminal = [r for r in mine if r.get("record") == "attempt"]
    if not terminal:
        print(f"REFUSING: {attempt} reaches no terminal disposition yet; a "
              f"cohort is set aside AFTER it completes, and an attempt still "
              f"open is not one", file=sys.stderr)
        return 1
    if str(terminal[0].get("status")) != "complete":
        print(f"REFUSING: {attempt} terminated "
              f"{terminal[0].get('status')!r}; only a battery that COMPLETED "
              f"has figures to decline, and applying the softer word to any "
              f"other disposition would cover what that disposition says",
              file=sys.stderr)
        return 1
    already = [r for r in mine if str(r.get("status")) == "set-aside"]
    if already:
        print(f"REFUSING: {attempt} is already set aside", file=sys.stderr)
        return 1
    # AND NO SECOND EVIDENCE DISPOSITION OF ANY KIND. The evidence axis is
    # irreversible exactly as the execution axis is: a cohort whose figures
    # were recorded authoritative is not later declined, and the record does
    # not carry two answers to one question.
    other = [r for r in mine if r.get("record") == "state"
             and str(r.get("status")) in POST_TERMINAL_STATES]
    if other:
        print(f"REFUSING: {attempt} already carries the evidence disposition "
              f"{str(other[0].get('status'))!r}; an attempt reaches at most "
              f"one, and nothing reopens it", file=sys.stderr)
        return 1
    row = {"lane": lane, "record": "state", "attempt": attempt,
           "status": "set-aside", "phase": "battery", "reason": reason}
    for key in ("attempt_no", "side", "sha", "cwd"):
        if seed.get(key):
            row[key] = seed[key]
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"set aside {attempt} in {path.name}")
    print(f"  execution disposition: complete (unchanged; this row does not "
          f"replace it)")
    print(f"  evidence disposition : set-aside")
    print(f"  reason: {reason}")
    return 0


def authoritative_evidence_mode(args) -> int:
    """SAY THAT A COMPLETED COHORT'S FIGURES ARE THE ONES A PACKAGE SHIPS.

    THE MATCHED POSITIVE OF `--set-aside-attempt`, and the half of the
    evidence axis that had no verb at all. Until V16 a cohort could only ever
    be DECLINED out loud: `set-aside` had a verb, and "these are the figures
    this package reports" had none, so an attempt whose measurements the
    package actually carries was indistinguishable in the record from one
    nobody had got round to classifying. Both read `complete`, and the
    difference between them lived in prose.

    It is an EVIDENCE disposition, on its own axis. The battery terminated
    `complete` and that row is not touched, amended or replaced: this appends
    one `record=state status=authoritative` row with its one reason, exactly
    as setting aside appends one, and the two are the two answers to the same
    question. Which is why the guards are the same shape:

      * COMPLETE ONLY. A `failed` or `abandoned` attempt is `unevidenced`,
        permanently -- it measured nothing that could be carried -- and
        calling one authoritative would be asserting a result the run never
        reached. `sealed` is the package side's word for the same position;
        a package attempt establishes its authority through P8 and the
        sidecar, not through this verb.
      * ONE EVIDENCE DISPOSITION, EVER. Refused over any evidence row already
        recorded, including this one.
      * SAME LANE, and a SUBSTANTIVE reason: which package carries these
        figures, and why these and not another cohort's.
    """
    path, attempt = args.attempts, args.authoritative_evidence
    if not path or not path.is_file():
        print(f"REFUSING: no ledger at {path}", file=sys.stderr)
        return 1
    reason = " ".join((args.reason or "").split())
    if len(reason) < 40 or len(reason.split()) < 8:
        print("REFUSING: --authoritative-evidence wants --reason, and a "
              "substantive one -- at least forty characters over at least "
              "eight words. A cohort whose figures a package reports without "
              "an account of which package and why is a figure a reader "
              "cannot trace", file=sys.stderr)
        return 1
    rows = read_attempts(path)
    stated = [r.get("lane") for r in rows if r.get("record") == "lane"]
    lane = args.lane or (stated[0] if stated else None)
    if not lane:
        print("REFUSING: --authoritative-evidence wants --lane, and the "
              "ledger states none", file=sys.stderr)
        return 1
    mine = [r for r in rows if r.get("attempt") == attempt]
    if not mine:
        print(f"REFUSING: {path} carries no attempt {attempt}", file=sys.stderr)
        return 1
    wrong = sorted({r.get("lane") for r in mine} - {lane, None})
    if wrong:
        print(f"REFUSING: {attempt} belongs to lane {wrong[0]}, not {lane}",
              file=sys.stderr)
        return 1
    seed = mine[0]
    if seed.get("side") not in BATTERY_SIDES:
        print(f"REFUSING: {attempt} is a {seed.get('side')} attempt; this "
              f"verb records a BATTERY cohort's evidence disposition. A "
              f"package attempt's authority is established after P8, in the "
              f"external ledger and the <package>.authority.json sidecar "
              f"bound to the final ZIP, and never by hand", file=sys.stderr)
        return 1
    terminal = [r for r in mine if r.get("record") == "attempt"]
    if not terminal:
        print(f"REFUSING: {attempt} reaches no terminal disposition yet; an "
              f"evidence disposition says what became of a TERMINATED "
              f"attempt's measurements, and an attempt still open is not one",
              file=sys.stderr)
        return 1
    if str(terminal[0].get("status")) != "complete":
        print(f"REFUSING: {attempt} terminated "
              f"{terminal[0].get('status')!r}; only a battery that COMPLETED "
              f"has measurements to carry. An attempt that failed or was "
              f"abandoned is {EVIDENCE_UNSET} and stays so, and calling one "
              f"authoritative would assert a result its run never reached",
              file=sys.stderr)
        return 1
    already = [r for r in mine if r.get("record") == "state"
               and str(r.get("status")) in POST_TERMINAL_STATES]
    if already:
        print(f"REFUSING: {attempt} already carries the evidence disposition "
              f"{str(already[0].get('status'))!r}; an attempt reaches at most "
              f"one, and nothing reopens it", file=sys.stderr)
        return 1
    row = {"lane": lane, "record": "state", "attempt": attempt,
           "status": "authoritative", "phase": "battery", "reason": reason}
    for key in ("attempt_no", "side", "sha", "cwd"):
        if seed.get(key):
            row[key] = seed[key]
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"recorded authoritative evidence for {attempt} in {path.name}")
    print(f"  execution disposition: complete (unchanged; this row does not "
          f"replace it)")
    print(f"  evidence disposition : authoritative")
    print(f"  reason: {reason}")
    return 0


def log_root_elsewhere_mode(args) -> int:
    """SAY WHERE A NAMED ATTEMPT'S TRANSCRIPTS ARE, WHEN THEY ARE NOT HERE.

    V16. The attempt-log audit refuses a package whose shipped rows name a log
    root the package does not contain -- the V15 defect where a discarded
    predecessor's root was named and never staged, which refused two of that
    lane's four discarded assemblies. The audit already accepts the honest
    answer: a row carrying `log_root_elsewhere` says, in words, where the
    transcripts went and why they are not here.

    Until now nothing could write that row. An append-only ledger corrects
    itself by APPENDING -- the rows already written may not be rewritten, and
    an attempt whose transcripts were never staged is knowable only after the
    fact -- so this appends a later row for the same attempt rather than
    touching the ones that named the root.

    It is not an exemption from staging. It is the statement that the root is
    somewhere else, which a reviewer can follow; a package that simply omitted
    the root would still be refused.
    """
    path, attempt = args.attempts, args.log_root_elsewhere
    if not path or not path.is_file():
        print(f"REFUSING: no ledger at {path}", file=sys.stderr)
        return 1
    where = " ".join((args.reason or "").split())
    if len(where) < 40 or len(where.split()) < 8:
        print("REFUSING: --log-root-elsewhere wants --reason, and a "
              "substantive one -- at least forty characters over at least "
              "eight words. A root said to be elsewhere with no account of "
              "where is the dangling reference this audit refuses, written "
              "one level down", file=sys.stderr)
        return 1
    rows = read_attempts(path)
    stated = [r.get("lane") for r in rows if r.get("record") == "lane"]
    lane = args.lane or (stated[0] if stated else None)
    if not lane:
        print("REFUSING: --log-root-elsewhere wants --lane, and the ledger "
              "states none", file=sys.stderr)
        return 1
    mine = [r for r in rows if r.get("attempt") == attempt]
    if not mine:
        print(f"REFUSING: {path} carries no attempt {attempt}", file=sys.stderr)
        return 1
    wrong = sorted({r.get("lane") for r in mine} - {lane, None})
    if wrong:
        print(f"REFUSING: {attempt} belongs to lane {wrong[0]}, not {lane}",
              file=sys.stderr)
        return 1
    if any(str(r.get("log_root_elsewhere", "")).strip() for r in mine):
        print(f"REFUSING: {attempt} already says where its log root is",
              file=sys.stderr)
        return 1
    seed = mine[0]
    # NO `status`. This row is not a transition of either axis -- it states a
    # FACT ABOUT WHERE BYTES ARE, and the attempt's execution and evidence
    # dispositions are whatever they already were. Giving it a status would
    # invent a state the machine does not have, which the machine correctly
    # refuses; `record=note` says what it is.
    row = {"lane": lane, "record": "note", "attempt": attempt,
           "phase": "attempt-log audit", "log_root_elsewhere": where}
    for key in ("attempt_no", "side"):
        if seed.get(key):
            row[key] = seed[key]
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"recorded where {attempt} keeps its transcripts")
    print(f"  {where}")
    return 0


def supersede_evidence_mode(args) -> int:
    """A COHORT THAT WAS AUTHORITATIVE AND WAS REPLACED IS SUPERSEDED.

    The one succession either evidence axis admits. It is not a reopening:
    `superseded` is terminal, nothing follows it, and the `authoritative` row
    it follows is left exactly as written, because that attempt really did
    hold that disposition for the time it held it.
    """
    path, attempt = args.attempts, args.supersede_evidence
    if not path or not path.is_file():
        print(f"REFUSING: no ledger at {path}", file=sys.stderr)
        return 1
    reason = " ".join((args.reason or "").split())
    if len(reason) < 40 or len(reason.split()) < 8:
        print("REFUSING: --supersede-evidence wants --reason, and a "
              "substantive one -- at least forty characters over at least "
              "eight words; a figure withdrawn with no account of what "
              "replaced it is the defect, not the record of it",
              file=sys.stderr)
        return 1
    rows = read_attempts(path)
    stated = [r.get("lane") for r in rows if r.get("record") == "lane"]
    lane = args.lane or (stated[0] if stated else None)
    mine = [r for r in rows if r.get("attempt") == attempt]
    if not mine:
        print(f"REFUSING: {path} carries no attempt {attempt}", file=sys.stderr)
        return 1
    wrong = sorted({r.get("lane") for r in mine} - {lane, None})
    if wrong:
        print(f"REFUSING: {attempt} belongs to lane {wrong[0]}, not {lane}",
              file=sys.stderr)
        return 1
    holds = [str(r.get("status")) for r in mine
             if str(r.get("status")) in EVIDENCE_DISPOSITIONS]
    if "superseded" in holds:
        print(f"REFUSING: {attempt} is already superseded", file=sys.stderr)
        return 1
    if "authoritative" not in holds:
        print(f"REFUSING: {attempt} carries no authoritative evidence to "
              f"supersede; its evidence disposition is "
              f"{holds[0] if holds else EVIDENCE_UNSET!r}, and superseding "
              f"anything else would assert it had once been carried",
              file=sys.stderr)
        return 1
    seed = mine[0]
    row = {"lane": lane, "record": "state", "attempt": attempt,
           "status": "superseded", "phase": "evidence", "reason": reason}
    for key in ("attempt_no", "side"):
        if seed.get(key):
            row[key] = seed[key]
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"superseded the evidence of {attempt}")
    print(f"  the authoritative row it follows is unchanged; that attempt did "
          f"hold that disposition")
    print(f"  reason: {reason}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # NOT `required` ANY MORE. `--allocate-ordinal` runs before a package
    # exists -- it is what `battery.sh` calls at preflight -- and
    # `--verify-ledger` can be pointed at a bare ledger file. Every mode that
    # does need one says so below, by name.
    parser.add_argument("--package", type=Path, default=None)
    parser.add_argument("--head", default="")
    parser.add_argument("--parent", default="")
    parser.add_argument("--measured", default="")
    parser.add_argument("--attempts", type=Path, default=None,
                        help="the append-only attempt ledger outside the "
                             "package; its relevant rows are copied in")
    parser.add_argument("--attempt", default="",
                        help="the assembly's own attempt id, so its rows are "
                             "copied in beside the batteries'")
    parser.add_argument("--attempt-no", default="",
                        help="the assembly attempt's ordinal; the transcripts "
                             "the pipeline writes live under logs/attempt-NN")
    parser.add_argument("--package-name", default="",
                        help="--seal-ledger: the package the sealing attempt's "
                             "terminal row must name")
    parser.add_argument("--audit-logs", action="store_true",
                        help="refuse a package whose transcripts are not "
                             "accounted for by exactly one attempt each; "
                             "writes nothing")
    parser.add_argument("--seal-ledger", action="store_true",
                        help="audit the attempt state machine, then write "
                             "logs/attempts.json; the P5 write, not the P1 one")
    parser.add_argument("--lane", default="",
                        help="the lane this ledger belongs to; a tool refuses "
                             "to append to, or read as its own, a ledger that "
                             "declares a different one")
    parser.add_argument("--allocate-ordinal", action="store_true",
                        help="print the next attempt ordinal for --lane, "
                             "opening the ledger if it does not exist; refuses "
                             "an ordinal any row has ever carried")
    parser.add_argument("--propose", default="",
                        help="--allocate-ordinal: the ordinal the caller wants; "
                             "refused if it has ever been used")
    parser.add_argument("--fresh", action="store_true",
                        help="--allocate-ordinal: assert the lane ledger does "
                             "not exist yet; refuses over an existing one")
    parser.add_argument("--supersede-evidence", default=None, metavar="ID",
                        help="record, with --reason, that an authoritative "
                             "cohort was replaced by a later one")
    parser.add_argument("--log-root-elsewhere", default=None, metavar="ID",
                        help="record, with --reason, where an attempt keeps "
                             "its transcripts when the package does not "
                             "contain the log root its rows name")
    parser.add_argument("--set-aside-attempt", default=None,
                        metavar="ID",
                        help="record that a COMPLETED battery cohort's "
                             "figures are not carried, with --reason; the "
                             "post-terminal word V15 held two cohorts for "
                             "and used zero times")
    parser.add_argument("--authoritative-evidence", default=None,
                        metavar="ID",
                        help="record that a COMPLETED battery cohort's "
                             "measurements are the ones a package reports, "
                             "with --reason; the matched positive of "
                             "--set-aside-attempt, on the EVIDENCE axis. The "
                             "attempt's `complete` terminal row is not "
                             "touched, and an attempt that failed or was "
                             "abandoned is refused")
    parser.add_argument("--abandon-attempt", default=None,
                        metavar="ID",
                        help="give an attempt that was interrupted from "
                             "outside its terminal row, with --reason; an "
                             "attempt with no terminal row is the defect "
                             "the V15 review found and this is how the "
                             "record says what happened to it")
    parser.add_argument("--retire-ledger", type=Path, default=None,
                        metavar="OLD",
                        help="stop OLD out loud and open --to as its "
                             "successor: audit it, classify its completed "
                             "and unused batteries set-aside, append a "
                             "terminal `retired` row, and carry its digest, "
                             "bytes, rows and SPENT ORDINALS into the "
                             "successor's opening lane row")
    parser.add_argument("--to", type=Path, default=None, metavar="NEW",
                        help="--retire-ledger: the successor ledger to open")
    parser.add_argument("--reason", default="", metavar="WHY",
                        help="--retire-ledger: why this ledger stopped; "
                             "required, because a ledger that stops without "
                             "saying why leaves its successor unable to "
                             "explain the gap")
    parser.add_argument("--history-table", action="store_true",
                        help="reconstruct the COMPLETE history across every "
                             "--attempts ledger given, as one table under one "
                             "numbering, with the reused ordinals and the "
                             "append-or-replacement verdict for each "
                             "adjacent pair")
    parser.add_argument("--attempts-list", type=Path, action="append",
                        default=[], metavar="LEDGER",
                        help="--history-table: one ledger, repeatable, in "
                             "chronological order")
    parser.add_argument("--claim-append-only", action="store_true",
                        help="--history-table: assert the ledgers given are "
                             "ONE append-only record. Refused over a pair "
                             "that is not, or over a reused ordinal")
    parser.add_argument("--json", type=Path, default=None, metavar="OUT",
                        help="--history-table: write the whole derivation -- "
                             "every attempt on both axes, the nine counts and "
                             "the invariant verdicts -- to OUT as JSON, so a "
                             "package carries the derivation rather than a "
                             "transcription of it")
    parser.add_argument("--assert-invariants", action="store_true",
                        help="--history-table: exit non-zero if any of the "
                             "three invariants fails. They are reported "
                             "either way; this makes the report a gate")
    parser.add_argument("--verify-ledger", action="store_true",
                        help="audit a ledger, or a package's shipped "
                             "logs/attempts.json, as a record and as a state "
                             "machine; writes nothing")
    parser.add_argument("--frozen-at", default="",
                        help="--verify-ledger: the instant the record claims "
                             "to be frozen at; a row ending later is refused")
    parser.add_argument("--in-package", action="store_true",
                        help="--verify-ledger: read the rows as package bytes "
                             "frozen at P5, where the winning word is 'sealed' "
                             "and 'authoritative' is refused; inferred "
                             "automatically when reading a package's own "
                             "logs/attempts.json")
    args = parser.parse_args(argv)

    # THE TWO MODES THAT PRECEDE A PACKAGE. An ordinal is allocated at a
    # battery's preflight, when there is no package and may never be one.
    if args.supersede_evidence:
        return supersede_evidence_mode(args)
    if args.log_root_elsewhere:
        return log_root_elsewhere_mode(args)
    if args.set_aside_attempt:
        return set_aside_attempt_mode(args)
    if args.authoritative_evidence:
        return authoritative_evidence_mode(args)
    if args.abandon_attempt:
        return abandon_attempt_mode(args)
    if args.retire_ledger:
        if args.to is None:
            print("REFUSING: --retire-ledger wants --to NEW", file=sys.stderr)
            return 1
        return retire_ledger_mode(args)
    if args.history_table:
        return history_table_mode(args)
    if args.allocate_ordinal:
        return allocate_ordinal_mode(args)
    if args.verify_ledger:
        return verify_ledger_mode(args)
    if args.package is None:
        parser.error("--package is required in every mode but "
                     "--allocate-ordinal and --verify-ledger")

    logs = args.package / "logs"

    # A DISCARDED RUN'S LOGS ARE NOT EVIDENCE. The battery that abandoned them
    # said so in this directory; composing a package from them would be
    # composing figures from a record that calls itself non-evidence. The root
    # marker is read too: `assemble.sh` writes one there on every failure path,
    # and a half-built package staged into a later one is the same defect
    # wearing a different filename.
    markers = sorted(one.name for one in logs.glob("DISCARDED-*.txt"))
    if (args.package / "DISCARDED.txt").is_file():
        markers.append("DISCARDED.txt (at the package root)")
    if markers:
        print("REFUSING: the staged tree carries a discard marker: "
              + ", ".join(markers), file=sys.stderr)
        print("A discarded attempt's logs are a record of an attempt, not "
              "evidence of a result. Stage a run that completed.",
              file=sys.stderr)
        return 1

    if args.audit_logs:
        return audit_logs_mode(args)
    if args.seal_ledger:
        return seal_ledger_mode(args)
    for required in ("head", "parent"):
        if not getattr(args, required):
            parser.error(f"--{required} is required to compose checks.txt")
    log_root = log_root_for(args.attempt_no)

    out: list[str] = [
        "Every command this lane ran UP TO THE INSTANT THIS FILE IS COMPOSED,",
        "with its numeric exit, the log it wrote, the commit it ran at, and",
        "the state of the working tree read immediately before and immediately",
        "after it.",
        "",
        "WHAT `recorded:` MEANS, ON EVERY ROW. V12 opened by claiming \"Every",
        "command this lane ran, its exact invocation\" and then rendered three",
        "different kinds of thing identically: real invocations from the",
        "battery ledgers, package-phase strings with this lane's values elided",
        "to bare capitals, and prose. Its own epilogue admitted omitting four",
        "commands and dropped seven more without saying so. Each row now",
        "states which kind its command string is:",
        "",
        "  EXECUTABLE   a VALIDATED EXEC RECORD is recorded beside the",
        "               prose: a cwd naming one of the root variables below,",
        "               an argv list or an expandable shell form, and the",
        "               environment the command needed. Re-runnable, and",
        "               `logs/replay-command.py` re-runs it.",
        "  ELIDED       capitalised tokens stand in for this lane's values,",
        "               or a plausible command string carries no exec record.",
        "               Either way not re-runnable as shipped",
        "  PROSE        a description, not an invocation; not re-runnable",
        "  NON-EXECUTABLE  a command was recorded and FAILED validation. The",
        "               reason names the fault by code: quoted-variable,",
        "               prose-prefix, no-command-head, malformed-argv,",
        "               undefined-variable, undefined-cwd",
        "  NOT RECORDED no command string was recorded for this step",
        "",
        "WHAT IS NOT IN THIS FILE is listed at the end, by phase and by name,",
        "rather than left for a reader to notice missing.",
        "",
        "COMPOSED, NOT TYPED. `logs/checks.py` reads the ordering ledgers the",
        "two batteries wrote as they ran and the logs those ledgers name. V6",
        "wrote this member by hand and its review found five counts wrong",
        "across the package; the answer for this one is that nobody writes it.",
        "",
        "THE TREE STATE ON A ROW IS THAT ROW'S. V10 read the porcelain result",
        "once, at preflight, and stamped it on every row -- including the two",
        "parent rows that run after a tracked file has been overwritten, both",
        "of which printed `clean`. Each row below carries the reading the",
        "battery took either side of that row's own command.",
        "",
        f"parent  {args.parent}",
        f"head    {args.head}",
    ]
    if args.measured and args.measured != args.head:
        out += [
            f"measured at {args.measured}",
            "",
            "THIS SHOULD NOT APPEAR. Every figure this package reports is meant",
            "to come from one battery run at the sealed head. If a commit is",
            "named here, some measurement below was taken at a different one,",
            "and which figures that affects is a question for the reader —",
            "which is exactly the position this package exists not to be in.",
        ]
    out.append("")

    batteries: list[tuple[str, dict, list[dict]]] = []
    # HOW MANY OF EACH KIND, COUNTED AS THEY ARE RENDERED and reported in the
    # epilogue, so the opening claim and the content are checkable against
    # each other by a reader who does not read every row.
    fidelity: dict[str, int] = {}
    # THE MACHINE-READABLE COMMAND RECORD, accumulated as the rows render and
    # written out as `commands.json` beside this file. V15 shipped only the
    # prose rows, so the only way to test whether a row re-ran was to read it
    # and believe the label; `replay-command.py --check` reads this.
    command_records: list[dict] = []
    # A ROW WHOSE LOGGED STRING AND WHOSE RECORD DESCRIBE DIFFERENT COMMANDS.
    # `command_line()` derives the shipped line from the record and reports
    # any ledger string that is neither of the two renderings a battery or the
    # assembler can legitimately have written. Collected rather than raised so
    # a reader is told about every such row at once.
    command_conflicts: list[str] = []
    # THE ROOT DEFINITIONS, MERGED FROM THE TWO BATTERY LEDGERS. Each battery
    # writes the same four `root=` lines at run time; a root defined twice
    # with two DIFFERENT meanings is exactly V15's `$REPO` defect and is
    # refused here rather than rendered.
    defined_roots: dict[str, str] = {}
    root_conflicts: list[str] = []
    for _name in ("order-parent.txt", "order-head.txt"):
        _meta, _ = ledger(logs / _name)
        for _root, _meaning in (_meta.get("roots") or {}).items():
            if _root in defined_roots and defined_roots[_root] != _meaning:
                root_conflicts.append(
                    f"{_root} is defined as {defined_roots[_root]!r} by one "
                    f"battery and as {_meaning!r} by the other; one root "
                    f"variable means one directory, and V15's $REPO meaning "
                    f"two is the defect this refuses")
            defined_roots[_root] = _meaning
    # AND THE ROOT NO BATTERY CAN DECLARE, BECAUSE IT DOES NOT EXIST YET WHEN
    # A BATTERY RUNS.
    #
    # `battery.sh` writes four `root=` lines and `$PACKAGE_ROOT` is not among
    # them: a battery has no knowledge of the package directory, which this
    # pipeline creates afterwards. But `assemble.sh`'s package-phase records
    # bind `cwd: "$PACKAGE_ROOT"` -- the P1 gate comparison is one -- so with
    # the ledgers' four names alone that row classifies NON-EXECUTABLE
    # `[undefined-variable]`, is collected into `refused` below, and this
    # tool returns 1 at P5. The assembly stops, on a row that is correct.
    #
    # `REPLAY_ROOT_FALLBACKS` already carried the name and its meaning and was
    # read only by `token_legend()`, so the legend explained a root the root
    # TABLE did not define and the classifier did not accept. It reaches both
    # now, from one place. `setdefault`, not assignment: a `root=` line
    # written at run time outranks a fallback, and the conflict check above
    # still refuses two batteries that disagree.
    for _root, _meaning in REPLAY_ROOT_FALLBACKS.items():
        defined_roots.setdefault(_root, _meaning)
    if root_conflicts:
        for one in sorted(set(root_conflicts)):
            print(f"REFUSING: {one}", file=sys.stderr)
        return 1
    # THE UNDEFINED-VARIABLE TEST IS NOT WEAKENED BY THE LINE ABOVE. A root
    # this set does not carry is still refused: `EVIDENCE_ROOT` in a package
    # whose batteries never declared it fails exactly as before.
    defined_roots_set = set(defined_roots)
    for label, name in (("PARENT", "order-parent.txt"), ("HEAD", "order-head.txt")):
        meta, rows = ledger(logs / name)
        batteries.append((label, meta, rows))
        out += ["=" * 70, f"{label} battery — {logs.name}/{name}", "=" * 70, ""]
        if not rows:
            out += ["(the ledger for this battery is not present)", ""]
            continue
        # The battery-level provenance, once, as the ledger recorded it, and
        # labelled with the instant it describes.
        out += [
            f"attempt    : {meta.get('attempt', '(not recorded)')}"
            f"  (ordinal {meta.get('prefix', '?')}; its transcripts are under "
            f"{meta.get('root', '(not recorded)')}/)",
            f"lane       : {meta.get('lane', '(not recorded)')}",
            # THE CLAIM AND THE CHECKOUT, SIDE BY SIDE. `expected` is what the
            # caller said this battery measures; `sha` is what the checkout
            # actually held. V12 recorded only the second and compared it to
            # nothing, so a clean checkout at the wrong commit was labelled by
            # its third argument.
            f"expected   : {meta.get('expect', '(not recorded; pre-V13 run)')}",
            f"preflight  : sha={meta.get('sha', '?')}"
            f"  porcelain={meta.get('porcelain', '?')}"
            f"  cwd={meta.get('cwd', '?')}",
            f"postflight : sha={meta.get('end_sha', '?')}"
            f"  porcelain={meta.get('end_porcelain', '?')}"
            f"  drift={meta.get('drift', '?')}",
        ]
        if meta.get("build_state"):
            out.append(f"build-state: {meta['build_state']}")
        if meta.get("build_state_note"):
            out.append(f"build-note : {meta['build_state_note']}")
        if meta.get("naming"):
            out.append(f"naming     : {meta['naming']}")
        for refused in meta.get("refused", []):
            out.append(f"refused    : {refused}")
        if meta.get("discarded"):
            out += [
                f"DISCARDED  : {meta['discarded']}",
                f"reason     : {meta.get('discard_reason', '(none recorded)')}",
            ]
        out.append("")
        for row in rows:
            end = "-parent" if label == "PARENT" else "-head"
            log = resolve_log(logs, row, end)
            # THE REPORT, WHERE THE TOOL WRITES ONE. The browser gate's stdout
            # duplicated its JSON report, so the log is a short transcript and
            # the numbers a reader wants are in the `.json`; the headline is
            # taken from the report, and both members are named on the row.
            # ...IN THE SAME ATTEMPT ROOT AS THE LOG. Looked for beside the
            # transcript rather than at the top of `logs/`, because that is
            # where the battery writes it and because two batteries' reports
            # would otherwise be one path.
            report = log.with_name(row["slug"] + end + ".json")
            record = exec_of(row)
            shown, disagreement = command_line(row, record)
            if disagreement:
                command_conflicts.append(f"{row['slug']}: {disagreement}")
            kind, why = command_fidelity(shown, record,
                                         defined=defined_roots_set)
            fidelity[kind] = fidelity.get(kind, 0) + 1
            command_records.append({
                "side": "parent" if label == "PARENT" else "head",
                "slug": row["slug"], "order": row.get("order"),
                "exit": int(row["exit"]) if str(row.get("exit", "")).lstrip("-").isdigit() else None,
                "log": row.get("log"), "attempt": meta.get("attempt"),
                "command": shown, "recorded": kind,
                "why": why, "exec": record})
            out += [
                f"--- {row['slug']}",
                "    command : " + (shown or "(not recorded)")
                .replace("\n", "\n              "),
                f"    recorded: {kind} -- {why}",
                *exec_lines(record, defined_roots),
                f"    exit    : {row.get('exit', '?')}",
                f"    order   : {row.get('order', '?')}",
                f"    started : {row.get('start', '?')}",
                f"    ended   : {row.get('end', '?')}",
                f"    sha     : {meta.get('sha', '(not recorded)')}",
                # CONTEMPORANEOUS, PER COMMAND. Not the preflight's answer.
                f"    clean   : before {row.get('tree_before', '(not recorded)')}"
                f"; after {row.get('tree_after', '(not recorded)')}",
                f"    cwd     : {meta.get('cwd', '(not recorded)')}",
                f"    attempt : {meta.get('attempt', '(not recorded)')}",
                f"    log     : logs/{log.relative_to(logs).as_posix()}"
                + ("" if log.is_file() else "   (not shipped)"),
            ]
            if report.is_file():
                out.append(
                    f"    report  : logs/{report.relative_to(logs).as_posix()}")
            for said in headline(report if report.is_file() else log,
                                 row["slug"]):
                out.append(f"    result  : {said}")
            out.append("")

    # THE PIPELINE'S OWN RECORDED STEPS. A step the assembly runs -- the gate
    # comparison is one -- is a recorded step with a row and a log, not an
    # unlogged aside. V10 shipped a gate comparison nothing in the pipeline
    # invoked, so the comparison had no ledger row at all.
    attempt_rows = read_attempts(args.attempts) if args.attempts else []
    dispositions = resolve_dispositions(attempt_rows)
    pipeline = [row for row in attempt_rows
                if args.attempt and str(row.get("attempt", "")) == args.attempt
                and row.get("record") == "step"]
    if pipeline:
        out += ["=" * 70,
                "PIPELINE steps — assemble.sh's own recorded commands",
                "=" * 70, "",
                f"attempt    : {args.attempt}",
                # THE STATE IT ACTUALLY HOLDS AT THIS INSTANT, WHICH IS NOT
                # "unresolved". V12, the V11 review: this member resolved the
                # sealing attempt's disposition the way a reader of the
                # finished package would, found no terminal row -- because at
                # P1 there cannot be one -- and printed "unresolved" beside
                # the id of the attempt that went on to become authoritative.
                # The review counted that as part of the contradiction, and
                # the explanatory paragraph under it did not repair it: a
                # reader scanning statuses sees the word, not the paragraph.
                #
                # `sealing` is a real state of the package state machine and
                # it is the one this attempt is in while this member is
                # written. Saying so is neither a forward claim nor a
                # contradiction, and the terminal disposition stays where it
                # belongs.
                "status     : sealing",
                "",
                "This member is composed at P1, so it carries the steps run",
                "up to that point, and the attempt is still sealing when it",
                "is written. The attempt's terminal disposition, and every",
                "row appended after this instant, are in logs/attempts.json,",
                "which is composed at P5 for exactly that reason.",
                ""]
        for row in sorted(pipeline, key=lambda one: str(one.get("order", ""))):
            record = exec_of(row)
            shown, disagreement = command_line(row, record)
            if disagreement:
                command_conflicts.append(f"{row.get('phase', '?')}: "
                                         f"{disagreement}")
            kind, why = command_fidelity(shown, record,
                                         defined=defined_roots_set)
            fidelity[kind] = fidelity.get(kind, 0) + 1
            command_records.append({
                "side": "package", "slug": row.get("phase"),
                "order": row.get("order"),
                "exit": int(row["exit"]) if str(row.get("exit", "")).lstrip("-").isdigit() else None,
                "log": row.get("log"), "attempt": row.get("attempt"),
                "command": shown, "recorded": kind,
                "why": why, "exec": record})
            out += [
                f"--- {row.get('phase', '?')}",
                "    command : " + (shown or "(not recorded)")
                .replace("\n", "\n              "),
                f"    recorded: {kind} -- {why}",
                *exec_lines(record, defined_roots),
                f"    exit    : {row.get('exit', '?')}",
                f"    order   : {row.get('order', '?')}",
                f"    started : {row.get('start', '?')}",
                f"    ended   : {row.get('end', '?')}",
                f"    result  : {row.get('result', '?')}",
                # V16, THE V15 REVIEW: THE PACKAGE-COMPARISON ROW HAD NO CWD.
                # `compare-gate.py logs/... logs/...` is three relative paths
                # with nothing anywhere saying what they are relative to, and
                # the row's `attempt :` slot was absent while the ledger
                # carried one. Both are rendered now, from the ledger row.
                #
                # THERE IS NO `--check-commands`, and this comment used to say
                # one refuses a row missing either. No such mode exists in this
                # file or in any tool beside it. What is true is what the two
                # lines below do: a row that recorded no cwd or no attempt
                # prints `(NOT RECORDED)` in that slot, in capitals, where a
                # reader meets it -- and a row whose exec record binds a cwd
                # carries it on `exec-cwd:` as well, validated. Naming a gate
                # that does not exist is the same fault as calling a string
                # re-runnable without running it.
                f"    cwd     : {row.get('cwd', '(NOT RECORDED)')}",
                f"    attempt : {row.get('attempt', '(NOT RECORDED)')}",
                f"    log     : {row.get('log', '(none)')}",
                "",
            ]

    # AND NOTHING IS WRITTEN IF A ROW SAYS TWO THINGS ABOUT ONE COMMAND.
    # Refused here, before any member is composed, because the disagreement is
    # between two halves of the EVIDENCE and cannot be repaired by rendering
    # one of them: whichever half is wrong, the row is not a record of what
    # ran, and shipping the other half would be choosing which to believe.
    if command_conflicts:
        for one in command_conflicts:
            print(f"REFUSING: {one}", file=sys.stderr)
        return 1

    # THE LEDGER MEMBER IS NOT WRITTEN HERE. `--seal-ledger` writes it at P5,
    # after the consistency audit, because an attempt's disposition is not
    # known at P1 and the member that claimed to carry it shipped saying
    # "unresolved" about the very package it shipped inside. The ledger is
    # still READ here, for the pipeline-step block above.
    shipped_attempts = False
    if args.attempts:
        if not args.attempts.is_file():
            print(f"REFUSING: no attempt ledger at {args.attempts}",
                  file=sys.stderr)
            return 1
        shipped_attempts = True

    index = write_log_index(logs, batteries, log_root, shipped_attempts)

    out += [
        "=" * 70,
        "Not recorded in this file, by name",
        "=" * 70,
        "",
        "THE CLAIM AND THE CONTENT AGREE HERE OR NOT AT ALL. V12's epilogue",
        "named four omitted commands while in fact omitting eleven, and the",
        "opening line claimed all of them exactly. What follows is the whole",
        "list, and the reason each one is not above.",
        "",
        "ONE. Everything the pipeline runs AFTER this file is composed. This",
        "member is written at P1. Nothing later can be in it, because it does",
        "not exist yet when this is written:",
        "",
    ]
    for relative, said in DEFERRED_LOGS:
        out.append(f"  - {relative.format(log_root=log_root)} -- {said}")
    for phase, why in PHASES_AFTER_FREEZE:
        out.append(f"  - {phase} -- {why}")
    out += [
        "",
        "  Their ledger rows ARE recorded, in machine-readable form, in the",
        "  append-only attempt ledger that lives outside this package, and",
        "  the rows that exist by P5 are copied into logs/attempts.json. That",
        "  member declares, in `phases_not_recorded`, the phases that run",
        "  after its own freeze, so a reader can tell a phase that left no",
        "  row from a phase that never ran.",
        "",
        "TWO. The transcripts themselves are not summarised here. The sealing",
        f"and sanitization passes are {log_root}/seal-check.log and",
        f"{log_root}/seal.log; the derivation and the audit are",
        f"{log_root}/derive-claims.log and {log_root}/head-consistency.log.",
        "A summary of a transcript is the thing this file exists to stop being",
        "written; the transcripts ship whole.",
        "",
        "THREE. How exact the commands above are, counted:",
        "",
    ]
    for kind in sorted(fidelity):
        out.append(f"  - {kind}: {fidelity[kind]}")
    if not fidelity:
        out.append("  - (no command rows were rendered)")
    # AND WHAT THAT COUNT COVERS, PER SIDE, COUNTED RATHER THAN CLAIMED.
    #
    # V16, THE COMMAND-REPLAY LANE, F5. The battery cohorts carry an exec
    # record on every row; `assemble.sh` sets `STEP_EXEC` on exactly one of
    # its ~20 package-phase steps. Every other package row classifies ELIDED
    # or PROSE -- honest, one row at a time, about not being re-runnable --
    # but a reader meeting one headline figure could take "V16 records
    # executable commands" for a claim about the whole pipeline. It is not
    # one, and the package says so in its own bytes, with the figures counted
    # off the rows above rather than written down beside them.
    coverage: dict[str, dict[str, int]] = {}
    for _one in command_records:
        _at = coverage.setdefault(str(_one.get("side") or "?"),
                                  {"rows": 0, "with_record": 0,
                                   "executable": 0})
        _at["rows"] += 1
        if _one.get("exec"):
            _at["with_record"] += 1
        if _one["recorded"] == CC.VERDICT_EXECUTABLE:
            _at["executable"] += 1
    if coverage:
        out += [
            "",
            "  Which of them carry a command record at all, by side:",
            "",
        ]
        for _side in sorted(coverage):
            _at = coverage[_side]
            out.append(
                f"  - {_side}: {_at['rows']} row(s), {_at['with_record']} "
                f"with an exec record, {_at['executable']} EXECUTABLE")
    _pkg = coverage.get("package")
    if _pkg and _pkg["with_record"] < _pkg["rows"]:
        out += [
            "",
            f"  MOST OF THIS PIPELINE'S OWN STEPS CARRY NO EXEC RECORD. "
            f"{_pkg['with_record']} of the {_pkg['rows']} package-phase rows",
            f"  above carry one; {_pkg['rows'] - _pkg['with_record']} do not, "
            f"and those are ELIDED or PROSE, which is",
            "  honest about not being re-runnable but is not the same thing",
            "  as being recorded. An EXECUTABLE count taken across every row",
            "  in this file is therefore a statement about the two battery",
            "  cohorts and about the package-phase rows named above, and not",
            "  about the assembly as a whole. Extending exec records to the",
            "  remaining package steps is work this member does not claim to",
            "  have done, and the figures on these lines are counted from the",
            "  rows rather than typed, so they cannot drift from them.",
        ]
    out += [
        "",
        "  Only an EXECUTABLE row is re-runnable, and it is re-runnable",
        "  because it carries a validated exec record -- a cwd, an argv or a",
        "  shell form, and an environment -- not because its first word looks",
        "  like a command. An ELIDED row is a real invocation with this",
        "  lane's values replaced by capitalised tokens, or a string with no",
        "  exec record beside it; a PROSE row is a description and was never",
        "  a string a shell was handed; a NON-EXECUTABLE row has a recorded",
        "  command that FAILED validation, and its reason carries the code.",
        "",
        "  V15 called all twenty-four of its rows LITERAL, \"the exact string",
        "  handed to the shell; re-runnable\", while seven of them quoted",
        "  $WORKSPACE or $REPO inside SINGLE quotes, where no shell expands",
        "  them, with no assignments supplied anywhere in the package. The",
        "  label is now earned by a structure and checked by running it.",
        "",
    ]
    # BOTH VOCABULARIES, DERIVED, IN ONE LEGEND. The replay roots come from
    # the ledgers' own `root=` lines unioned with the roots the rendered
    # records actually reference; the substitution tokens come from the
    # sealer's own tables. A token either side can emit and this legend
    # cannot explain is a refusal, not a footnote.
    referenced: set[str] = set()
    for _record in command_records:
        referenced |= set(_DOLLAR_TOKEN.findall(
            json.dumps(_record, sort_keys=True)))
    legend, legend_problems = token_legend(defined_roots, referenced)
    if legend_problems:
        for one in legend_problems:
            print(f"REFUSING: {one}", file=sys.stderr)
        return 1
    out += legend
    out += [
        "",
        "  Replay a row with:",
        "",
        "    python3 logs/replay-command.py --commands commands.json \\",
        "        --check",
        "    python3 logs/replay-command.py --commands commands.json \\",
        "        --side head --replay gzip-sizes \\",
        "        --root CANDIDATE_REPO=/path/to/candidate \\",
        "        --root TOOLS_ANCHOR=/path/to/handoff-tools \\",
        "        --witness 'catena-model.js whole'",
        "",
        "  AN EXIT STATUS ALONE DOES NOT PROVE A ROW RE-RAN, so pass",
        "  `--witness` and be told rather than assuming. Bind both roots of",
        "  `head-tests-against-parent` to an empty directory and its `cp`",
        "  fails, `&&` short-circuits, the suite never starts, the shell",
        "  exits 1 -- and the recorded exit is 1, because the recorded run",
        "  was a suite with 288 failures. `--witness TEXT` requires TEXT in",
        "  the replayed output and reports VACUOUS when the status matched",
        "  and the run did not. The text to use is on the row itself: each",
        "  row's `result :` slot above is the headline of its own recorded",
        "  transcript.",
        "",
    ]
    # AND THE ORDER, BECAUSE A ROW IS NOT NECESSARILY REPLAYABLE ALONE.
    #
    # V16, THE COMMAND-REPLAY LANE, F2. Following the single-row invocation
    # above verbatim on `browser-gate` gives exit 3, not the recorded 1:
    # `corpus_browser_gate: no built artifact at <clone>/build/public-alpha/
    # site`. The row consumes what `public-site` builds, and nothing in the
    # record or in these instructions said so, so a reviewer doing exactly
    # what the package told them would reasonably read V16's replayability
    # claim as failing. With `public-site` replayed first it reproduces
    # byte-identically.
    #
    # The sequence below is DERIVED from the rows above -- their own recorded
    # `ORDER`, per side -- rather than typed, and the specific warning is
    # emitted only for a side whose rows actually carry the pair, so it cannot
    # outlive the rows it describes.
    ordered: dict[str, list[tuple[int, str]]] = {}
    for _one in command_records:
        if _one.get("side") == "package":
            continue
        try:
            _at = int(str(_one.get("order") or ""))
        except ValueError:
            continue
        ordered.setdefault(str(_one.get("side")), []).append(
            (_at, str(_one.get("slug") or "")))
    if ordered:
        out += [
            "  REPLAY A SIDE IN ITS RECORDED ORDER, NOT A ROW ON ITS OWN. A",
            "  step may consume what an earlier step of the same battery",
            "  built, in the same checkout; the invocation above replays one",
            "  row and cannot supply what a row before it produced. Replay",
            "  from ORDER 1, or at least replay every row ahead of the one",
            "  you want, into the same checkout. The orders are these:",
            "",
        ]
        for _side in sorted(ordered):
            out.append(f"  {_side}:")
            for _at, _slug in sorted(ordered[_side]):
                out.append(f"    {_at:>2}  {_slug}")
            _rows = {_slug: _at for _at, _slug in ordered[_side]}
            if ("browser-gate" in _rows and "public-site" in _rows
                    and _rows["public-site"] < _rows["browser-gate"]):
                out += [
                    f"      -- {_side}/browser-gate reads the site",
                    f"         {_side}/public-site builds under",
                    "         build/public-alpha/site. Replayed on a checkout",
                    "         where public-site has not run it exits 3, not",
                    "         its recorded exit, and says so on its own",
                    "         output. That is the prerequisite failing, not",
                    "         the evidence.",
                ]
        out.append("")
    out += [
        "  The machine-readable form of every row above, with its exec",
        "  record and this root table, is `commands.json` beside this file.",
        "",
        "The roster of every log, and the attempt each belongs to, is",
        f"logs/{index.name}, derived in the same pass as this file.",
    ]
    if shipped_attempts:
        out += [
            "The attempt rows themselves — including the ones belonging to",
            "attempts that were discarded — are machine-readable in",
            "logs/attempts.json, which is composed at P5 rather than here:",
            "this file is written before the pipeline knows how the attempt",
            "ends, and that member is written after the pipeline does.",
        ]
    out += [
        "",
        "No judgement is recorded here either. What a result MEANS is argued",
        "in HANDOFF.md, LIMITATIONS.md and UNRESOLVED-BLOCKERS.md.",
        "",
    ]
    (args.package / "checks.txt").write_text("\n".join(out), encoding="utf-8")
    # ---- commands.json, the machine-readable half -------------------------
    #
    # DERIVED IN THE SAME PASS, FROM THE SAME ROWS. It is not a second
    # statement of the commands, it is the SAME statement in the form a
    # program can execute: `checks.txt`'s `command :` lines and the `command`
    # field below are both `catena_command.render_shell(record)` for every row
    # that has a record, produced by one call in `command_line()`, so the two
    # members cannot say different things about one row. That sentence used to
    # stand here while `render_shell` had no call site in this file at all,
    # and the two DID differ on both `browser-gate` rows.
    commands_blob = {
        "schema": "catena-commands/1",
        "variables": CC.make_variables(**defined_roots) if defined_roots
        else {"schema": CC.VARIABLES_SCHEMA, "roots": {}},
        # THE SAME FIGURES A READER MEETS IN `checks.txt`, PER SIDE, so a
        # program can ask what the executable count covers without parsing
        # prose. One `coverage` dict, built once, rendered twice.
        "coverage": coverage,
        "counts": {
            # FIVE NAMES, NEVER ONE NUMBER. V15's epilogue said "LITERAL: 24"
            # about a set in which seven rows were not re-runnable.
            "rows": len(command_records),
            "with_exec_record": sum(1 for one in command_records
                                    if one.get("exec")),
            "executable": sum(1 for one in command_records
                              if one["recorded"] == CC.VERDICT_EXECUTABLE),
            "non_executable": sum(1 for one in command_records
                                  if one["recorded"] == CC.VERDICT_NON_EXECUTABLE),
            "not_replayable_and_says_so": sum(
                1 for one in command_records
                if one["recorded"] in (CC.VERDICT_ELIDED, CC.VERDICT_PROSE,
                                       CC.VERDICT_NOT_RECORDED)),
        },
        "commands": command_records,
    }
    (args.package / "commands.json").write_text(
        json.dumps(commands_blob, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print("commands.json composed: "
          + ", ".join(f"{k} {v}" for k, v in
                      sorted(commands_blob["counts"].items())))
    refused = [one for one in command_records
               if one["recorded"] == CC.VERDICT_NON_EXECUTABLE]
    for one in refused:
        print(f"REFUSING: {one['side']}/{one['slug']}: {one['why']}",
              file=sys.stderr)
    if refused:
        return 1
    print(f"checks.txt composed: {len(out)} lines")
    print(f"logs/{index.name} derived from the ledgers and the directory")
    if shipped_attempts:
        print("logs/attempts.json is declared here and written at P5, by "
              "--seal-ledger, once this attempt has a disposition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
