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
    `authoritative` is a package attempt's word and at most one package attempt
    may hold it. The state machine is written out once, in `assemble.sh`'s
    header; `audit_authority()` below is its executable copy and there is no
    third statement of it.
  * THE MEMBER WAS WRITTEN BEFORE THE FACT IT REPORTED. `logs/attempts.json` is
    no longer written by the P1 pass at all. It is a DECLARED DERIVED MEMBER,
    written by `--seal-ledger` after the consistency audit and immediately
    before the manifest, from a ledger that by then carries the sealing
    attempt's own terminal row. It is pre-normalized on the way out, exactly as
    `claims.json` is, because nothing normalizes the tree after the freeze.

The one thing it does not do is judge. A `check-only` line here says what the
command printed; whether the result is acceptable is argued in the documents,
which is where a judgement belongs.

Usage:
    checks.py --package DIR --head SHA --parent SHA --attempt-no NN
              [--measured SHA] [--attempts LEDGER.jsonl] [--attempt ID]
    checks.py --audit-logs --package DIR --attempts LEDGER.jsonl
              --attempt ID --attempt-no NN
    checks.py --seal-ledger --package DIR --attempts LEDGER.jsonl
              --attempt ID --attempt-no NN --package-name NAME --head SHA
"""

from __future__ import annotations

import argparse
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
BATTERY_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "complete", "failed"),
    "started": ("complete", "failed"),
    "complete": (),
    "failed": (),
}
PACKAGE_STATES: dict[str, tuple[str, ...]] = {
    "": ("started", "sealing", "authoritative", "discarded"),
    "started": ("sealing", "authoritative", "discarded"),
    "sealing": ("authoritative", "discarded"),
    "authoritative": ("superseded",),
    "discarded": (),
    "superseded": (),
}
# The one disposition an attempt is allowed, and the row kind that carries it.
TERMINAL_STATES = frozenset(
    {"complete", "failed", "authoritative", "discarded"})
BATTERY_SIDES = frozenset({"head", "parent"})

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
    package to review, and reading only its terminal row is how a ledger comes
    to name three authoritative attempts. The disposition and its reason still
    come from the terminal row, because superseding does not overwrite the
    verdict it supersedes.
    """
    out: dict[str, dict] = {}
    for row in rows:
        attempt = str(row.get("attempt", ""))
        if not attempt:
            continue
        seen = out.setdefault(attempt, {"status": "unresolved: the ledger "
                                                  "carries no terminal row "
                                                  "for this attempt",
                                        "reason": ""})
        if row.get("record") == "attempt":
            if seen.get("_terminal"):
                seen["status"] = ("INCOHERENT: more than one terminal row "
                                  "for one attempt id")
                seen["_incoherent"] = True
                continue
            seen["_terminal"] = True
            if not seen.get("_incoherent"):
                seen["status"] = str(row.get("status", "(not stated)"))
            seen["reason"] = str(row.get("reason", ""))
        elif (row.get("record") == "state"
              and str(row.get("status", "")) == "superseded"
              and not seen.get("_incoherent")):
            seen["status"] = "superseded"
            seen["superseded_reason"] = str(row.get("reason", ""))
    for value in out.values():
        value.pop("_terminal", None)
        value.pop("_incoherent", None)
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


def audit_authority(rows: list[dict]) -> list[str]:
    """THE STATE MACHINE, ENFORCED. See `assemble.sh`'s header for the table.

    The incident: a lane's ledger marked THREE attempts `authoritative` -- the
    head battery, the parent battery and a package attempt that had already
    been superseded -- because `battery.sh` and `assemble.sh` wrote the same
    word for two different facts. "This battery ran to completion" and "this is
    the package attempt to review" are separate axes, and with one word for
    both the authoritative count can never be one. So:

      * a battery attempt may only ever be `started`, `complete` or `failed`;
        `authoritative`, `sealing` and `superseded` are package words;
      * every transition an attempt makes must be one the table allows, which
        is what refuses `discarded` followed by `authoritative`;
      * exactly one `record=attempt` row per attempt carries the disposition,
        so an attempt cannot be handed two;
      * at most one package attempt in the ledger may RESOLVE to
        `authoritative`, superseding being what makes room for the next.
    """
    problems: list[str] = []
    sides: dict[str, str] = {}
    for attempt, carried in state_rows(rows).items():
        side = ""
        for row in carried:
            side = str(row.get("side", "")) or side
        sides[attempt] = side
        if side in BATTERY_SIDES:
            table, kind = BATTERY_STATES, "battery"
        elif side == "package":
            table, kind = PACKAGE_STATES, "package"
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
    authoritative = sorted(one for one, value in resolved.items()
                           if value["status"] == "authoritative")
    for one in authoritative:
        if sides.get(one) != "package":
            problems.append(
                f"{one}: only a package attempt may be authoritative; this "
                f"one is side={sides.get(one) or '(none)'}")
    if len(authoritative) > 1:
        # THE REMEDY IS NAMED, because the pipeline deliberately does not
        # apply it. Demoting a package that is already out for review is a
        # judgement about which package a reader should be holding, and an
        # assembly script is not entitled to make it silently -- the operator
        # appends the supersession, with its reason, and it is a ledger row
        # like any other.
        problems.append(
            f"{len(authoritative)} attempts resolve to authoritative ("
            + ", ".join(authoritative)
            + "); a ledger names at most one package to review. Append one "
              "record=state status=superseded row, with its one reason, for "
              "the attempt being replaced, and seal again")
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
                   package_attempt: str) -> Path | None:
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
            if str(row.get("attempt", "")) in wanted
            or str(row.get("side", "")) == "package"
            or (package_attempt and str(row.get("attempt", "")) == package_attempt)]
    for row in keep:
        row["resolved_status"] = dispositions.get(
            str(row.get("attempt", "")), {}).get("status", "unresolved")
    out = {
        "note": "Rows copied from the append-only attempt ledger that lives "
                "outside this package, filtered to the attempts this package "
                "was built from. A row with record=step states what one step "
                "did; the record=attempt row of the same attempt carries its "
                "one disposition and its one reason, and a record=state row "
                "carries a non-terminal state or a later supersession. "
                "resolved_status on each row is that attempt's LAST state, "
                "joined here mechanically: a battery is complete or failed, "
                "and authoritative is a package attempt's word, held by at "
                "most one attempt in this ledger.",
        "copied_at_phase": "P5, after the consistency audit and immediately "
                           "before the manifest -- as late as the freeze line "
                           "allows, and late enough to carry the sealing "
                           "attempt's own terminal row, which V11 wrote at P8 "
                           "into a member composed at P1. Rows the pipeline "
                           "appends after this instant, P6 through P8, are in "
                           "the ledger outside the package, not here",
        "attempts": [{"attempt": attempt,
                      "status": value["status"],
                      "reason": value["reason"]}
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


def seal_ledger_mode(args) -> int:
    """The authority audit, then the shipped ledger. In that order, always.

    Refusing AFTER writing the member would ship the member the audit refused,
    which is how the reviewed package came to carry three authoritative
    attempts and describe itself as unresolved.
    """
    if not args.attempts or not args.attempts.is_file():
        print(f"REFUSING: no attempt ledger at {args.attempts}",
              file=sys.stderr)
        return 1
    rows = read_attempts(args.attempts)
    problems = audit_authority(rows)
    dispositions = resolve_dispositions(rows)
    mine = dispositions.get(args.attempt, {})
    if mine.get("status") != "authoritative":
        problems.append(
            f"{args.attempt}: this is the sealing attempt and it resolves to "
            f"{mine.get('status', '(no rows at all)')!r}; the terminal row is "
            f"appended before this member is composed, not after P8")
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
    path = write_attempts(logs, rows, wanted, args.attempt)
    print(f"logs/{path.name} composed from the ledger outside the package, "
          f"pre-normalized, carrying this attempt's own terminal row")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True)
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
    args = parser.parse_args(argv)

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
        "Every command this lane ran, its exact invocation, its numeric exit,",
        "the log it wrote, the commit it ran at, and the state of the working",
        "tree read immediately before and immediately after it.",
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
            out += [
                f"--- {row['slug']}",
                "    command : " + str(row.get("command", "(not recorded)"))
                .replace("\n", "\n              "),
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
            out += [
                f"--- {row.get('phase', '?')}",
                "    command : " + str(row.get("command", "(not recorded)"))
                .replace("\n", "\n              "),
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
        "Not recorded in this file",
        "=" * 70,
        "",
        "The sealing and sanitization passes are their own transcripts —",
        f"{log_root}/seal-check.log and {log_root}/seal.log — and the",
        f"derivation and audit are {log_root}/derive-claims.log and",
        f"{log_root}/head-consistency.log. They are not summarised here,",
        "because a summary of a transcript is the thing this file exists to",
        "stop being written.",
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
