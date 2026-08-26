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
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

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
# THE V13 CORRECTION: `set-aside`. V12's vocabulary admitted only `started`,
# `complete` and `failed` for a battery, so a cohort that ran to completion and
# whose figures were then NOT used was forced to `complete` with an empty
# reason -- indistinguishable, in the record, from the cohort whose figures the
# package reports. Four such cohorts are missing from every surviving V12
# ledger for exactly that reason: there was no word for them, so they were
# deleted instead of recorded. `set-aside` is that word.
#
# It is POST-TERMINAL, exactly as `superseded` is on the package side, and for
# the same reason: whether a completed battery's figures were used is not known
# while it is running, so it cannot be its terminal disposition. The battery
# terminates `complete`, and the operator later appends one `record=state`
# row -- `status=set-aside`, with its one NON-EMPTY reason -- which becomes the
# attempt's resolved state. Superseding does not overwrite the verdict it
# supersedes and neither does this: the battery did complete, and the terminal
# row still says so.
BATTERY_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "complete", "failed"),
    "started": ("complete", "failed"),
    "complete": ("set-aside",),
    "failed": (),
    "set-aside": (),
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
PACKAGE_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "sealing", "sealed", "discarded"),
    "started": ("sealing", "sealed", "discarded"),
    "sealing": ("sealed", "discarded"),
    "sealed": ("superseded",),
    "discarded": (),
    "superseded": (),
}
# The same machine, plus the one transition only the external ledger may
# record: a sealed package that has PASSED P8 becomes the authoritative one.
EXTERNAL_PACKAGE_STATES: dict[str, tuple[str, ...]] = {
    **PACKAGE_STATES,
    "sealed": ("authoritative", "superseded"),
    "authoritative": ("superseded",),
}
# The one disposition an attempt is allowed, and the row kind that carries it.
# `authoritative` is NOT here: it arrives after the attempt already terminated
# `sealed`, so it cannot be the terminal row, in either scope.
TERMINAL_STATES = frozenset({"complete", "failed", "sealed", "discarded"})
# States that arrive AFTER the terminal row and become the resolved state.
# Carried by `record=state`, never by `record=attempt`.
POST_TERMINAL_STATES = frozenset({"superseded", "set-aside", "authoritative"})
# The states that mean "this went as intended". Everything else that an attempt
# can END on -- terminal or post-terminal -- must say why, in words, on the row
# that states it AND in the summary the package ships. V12 shipped all five
# `attempts[]` reasons empty, two of them supersessions, with the reasons
# living only on separate state rows nobody joined.
SUCCESSFUL_STATES = frozenset({"complete", "sealed", "authoritative"})
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
            if line.startswith("exit="):
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


# A STANDALONE CAPITALISED TOKEN IS A PLACEHOLDER UNTIL PROVED OTHERWISE.
# `assemble.sh` records its package-phase commands with `PKG`, `FREEZE`, `ZIP`,
# `TOOLS`, `LEDGER` and `ATTEMPT` standing in for the values it held, so those
# rows are not re-runnable strings; the batteries record real ones. V12
# presented both under one heading that claimed "its exact invocation".
# Excluded by the lookarounds: anything with a dot, slash or hyphen glued to it
# (`MANIFEST.sha256` is a filename), and anything after a `$` (a shell
# variable is a recorded expansion, not an elision).
#
# V15: AND AN ASSIGNMENT'S LEFT-HAND SIDE, which the `=` in the lookahead
# excludes. `TRIPTYCH_CHROME='/usr/bin/chromium' node tools/tests/...` is the
# OPPOSITE of an elision: the environment the command needs, spelled into the
# recorded string so a reviewer handed that string alone can reproduce the
# row, instead of being left inherited and invisible. A token glued to an `=`
# is a variable NAME being set, not a stand-in for a value the lane held --
# the value is right there after the `=`. Checked against V14: no recorded
# command in that package carries a capitalised token followed by `=`, so
# nothing previously marked ELIDED changes verdict because of this.
PLACEHOLDER = re.compile(r"(?<![\w./$-])([A-Z][A-Z0-9_]{2,})(?![\w./=-])")
# The first token of a string a shell was actually handed.
#
# THIS TUPLE IS THE WHOLE TEST, AND IT IS DELIBERATELY A FIXED LIST. It is
# tempting to replace it with `shutil.which(first)` and let the host's PATH
# decide, but `checks.txt` is a shipped, byte-stable member: a reviewer
# re-composing it off-host, on a machine with a different PATH, would get
# different verdicts and a different file. A literal tuple classifies the
# same way everywhere and forever, so the composed member is reproducible.
# The cost is that the list has to be extended by hand when a battery starts
# invoking a head it never invoked before -- which is what V15 did below.
COMMAND_HEADS = ("python3", "python", "bash", "sh", "make", "git", "node",
                 "npm", "cd", "env", "printf", "echo", "set", "(", "./",
                 "tools/", "logs/", "scripts/",
                 # V15: the coreutils and shell builtins a battery really
                 # invokes. `cp` was the one that mattered -- the V14
                 # parent-replay row began `cp '$REPO/tools/tests/...'` and
                 # was reported PROSE, i.e. "cannot be re-run as written",
                 # about a string the shell had in fact been handed.
                 "cp", "mv", "rm", "mkdir", "install", "test", "[",
                 "for", "if", "while", "true", "false", "zip", "unzip")


def command_fidelity(text) -> tuple[str, str]:
    """Is this recorded command a string a shell was handed, or a stand-in?

    `checks.txt` opened by claiming "Every command this lane ran, its exact
    invocation" and then rendered, identically, three kinds of thing: real
    invocations from the battery ledgers, package-phase strings with the
    lane's values elided to bare capitals, and outright prose. The claim and
    the content now agree because every row says which it is.

    The ELIDED verdict is deliberately conservative: a capitalised token that
    really was literal -- `git rev-parse HEAD` would be one -- is labelled
    elided too, because nothing here can tell them apart, and over-marking is
    the safe direction for a claim of exactness.

    V15: PROSE IS NOW ONLY EVER SAID ABOUT PROSE. The verdict turns on the
    first token being in `COMMAND_HEADS`, and that tuple listed only the
    interpreters and version-control tools. A battery step really does begin
    with a coreutils command -- V14's parent replay was

        cp '$REPO/tools/tests/test_catena_wave_1.py' tools/tests/... && \\
            python3 -m unittest discover ...

    -- and the missing `cp` made the package say of it "a description of what
    happened, not a string a shell was handed; it cannot be re-run as
    written", of a string a shell was handed and which re-runs verbatim.
    That is a false statement about the evidence, and worse than the elision
    it was guarding against, because it invites a reviewer to skip the row.
    `COMMAND_HEADS` therefore now also carries the coreutils and shell
    builtins a battery composes with: cp, mv, rm, mkdir, install, test, [,
    for, if, while, true, false, zip, unzip.

    The test stays a fixed tuple rather than a `shutil.which()` PATH probe on
    purpose; see the note above the tuple. The verdict has to be identical
    off-host, because `checks.txt` is a byte-stable shipped member and a
    reviewer must be able to re-compose it and get the same bytes.
    """
    text = str(text or "")
    if not text.strip():
        return "NOT RECORDED", ("no command string was recorded for this step; "
                                "there is nothing to re-run and nothing to "
                                "check it against")
    first = text.strip().split()[0]
    if not (first.startswith(COMMAND_HEADS) or "/" in first or "=" in first):
        return "PROSE", ("a description of what happened, not a string a shell "
                         "was handed; it cannot be re-run as written")
    found = sorted(set(PLACEHOLDER.findall(text)))
    if found:
        return "ELIDED", ("the capitalised token(s) " + ", ".join(found)
                          + " stand in for values this lane held; substitute "
                            "them to re-run. Marked conservatively: a token "
                            "that really was literal is marked the same way")
    return "LITERAL", "the exact string handed to the shell"


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
    """
    out: dict[str, dict] = {}
    for row in rows:
        if row.get("record") == LANE_RECORD:
            continue
        attempt = str(row.get("attempt", ""))
        if not attempt:
            continue
        seen = out.setdefault(attempt, {"status": "unresolved: the ledger "
                                                  "carries no terminal row "
                                                  "for this attempt",
                                        "reason": "",
                                        "terminal_status": "",
                                        "terminal_reason": ""})
        if row.get("record") == "attempt":
            if seen.get("_terminal"):
                seen["status"] = ("INCOHERENT: more than one terminal row "
                                  "for one attempt id")
                seen["_incoherent"] = True
                continue
            seen["_terminal"] = True
            seen["terminal_status"] = str(row.get("status", "(not stated)"))
            seen["terminal_reason"] = str(row.get("reason", ""))
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
    for value in out.values():
        value.pop("_terminal", None)
        value.pop("_incoherent", None)
        value.pop("_post_terminal", None)
    return out


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
            problems.append("a row names no attempt")
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
        else:
            problems.append(f"{attempt}: carries state rows but names no "
                            f"known side ({side or '(none)'}); the state "
                            f"machine is defined per side")
            continue
        terminal: list[str] = []
        previous = ""
        for row in carried:
            status = str(row.get("status", ""))
            record = str(row.get("record", ""))
            # BY NAME, BECAUSE THE GENERIC MESSAGE WOULD NOT SAY WHY. This is
            # the review's finding, not a vocabulary preference: the row is
            # written at or before P5 and frozen there, so `authoritative`
            # asserts the outcome of P6, P7 and P8 before any of them ran.
            if (status == "authoritative" and not external
                    and record == "attempt"):
                problems.append(
                    f"{attempt}: claims 'authoritative' in a record that is "
                    f"frozen at P5, BEFORE P6, P7 and P8 have run. No sealed "
                    f"package bytes may claim final authority before P8: a "
                    f"package attempt may claim at most 'sealed' about "
                    f"itself, and 'authoritative' is established afterwards, "
                    f"in the external complete ledger and the "
                    f"<package>.authority.json sidecar bound to the final ZIP")
                continue
            if status not in table:
                problems.append(
                    f"{attempt}: a {kind} attempt is never {status!r}; the "
                    f"{kind} states are "
                    + ", ".join(sorted(one for one in table if one)))
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
    winners = sorted(one for one, value in resolved.items()
                     if value["status"] == winning)
    for one in winners:
        if sides.get(one) != "package":
            problems.append(
                f"{one}: only a package attempt may be {winning}; this "
                f"one is side={sides.get(one) or '(none)'}")
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
    if not external:
        holding = sorted(one for one, value in resolved.items()
                         if value["status"] == "authoritative")
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
                      "terminal_reason": value.get("terminal_reason", "")}
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
    for attempt, value in sorted(resolve_dispositions(rows).items()):
        note = f" -- {value['reason']}" if str(value.get("reason", "")) else ""
        print(f"  {attempt}: {value['status']}{note}")
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
        print(f"  {attempt}: {value['status']}")
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
        "  LITERAL      the exact string handed to the shell; re-runnable",
        "  ELIDED       capitalised tokens stand in for this lane's values;",
        "               substitute them to re-run. Marked conservatively",
        "  PROSE        a description, not an invocation; not re-runnable",
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
            kind, why = command_fidelity(row.get("command", ""))
            fidelity[kind] = fidelity.get(kind, 0) + 1
            out += [
                f"--- {row['slug']}",
                "    command : " + str(row.get("command", "(not recorded)"))
                .replace("\n", "\n              "),
                f"    recorded: {kind} -- {why}",
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
            kind, why = command_fidelity(row.get("command", ""))
            fidelity[kind] = fidelity.get(kind, 0) + 1
            out += [
                f"--- {row.get('phase', '?')}",
                "    command : " + str(row.get("command", "(not recorded)"))
                .replace("\n", "\n              "),
                f"    recorded: {kind} -- {why}",
                f"    exit    : {row.get('exit', '?')}",
                f"    order   : {row.get('order', '?')}",
                f"    started : {row.get('start', '?')}",
                f"    ended   : {row.get('end', '?')}",
                f"    result  : {row.get('result', '?')}",
                f"    log     : {row.get('log', '(none)')}",
                "",
            ]

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
    out += [
        "",
        "  Only the LITERAL rows are re-runnable as written. An ELIDED row is",
        "  a real invocation with this lane's values replaced by capitalised",
        "  tokens; a PROSE row is a description and was never a string a",
        "  shell was handed.",
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
    print(f"checks.txt composed: {len(out)} lines")
    print(f"logs/{index.name} derived from the ledgers and the directory")
    if shipped_attempts:
        print("logs/attempts.json is declared here and written at P5, by "
              "--seal-ledger, once this attempt has a disposition")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
