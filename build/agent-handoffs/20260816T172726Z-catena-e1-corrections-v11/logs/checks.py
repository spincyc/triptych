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
package was built from are copied in here, as `logs/attempts.json`, before
the freeze. A step row states what a step did; the terminal row of its
attempt states whether the attempt is authoritative or discarded, with its
one reason, and this resolves the two so no row can be read as both.

A LOGS DIRECTORY CARRYING A DISCARD MARKER IS REFUSED. A discarded battery
drops one into its own logs directory; a package composed from it would be a
package whose figures came from a run its own record calls non-evidence.

The one thing it does not do is judge. A `check-only` line here says what the
command printed; whether the result is acceptable is argued in the documents,
which is where a judgement belongs.

Usage:
    checks.py --package DIR --head SHA --parent SHA [--measured SHA]
              [--attempts LEDGER.jsonl] [--attempt ID]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

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

# The transcripts a LATER pipeline phase writes. They are named in the index
# as declarations, exactly as `assemble.sh` declares them deferred, because
# the index is composed at P1 and these do not exist yet.
DEFERRED_LOGS: tuple[tuple[str, str], ...] = (
    ("logs/sealer-tests.log", "P1: the sealer's own test suite"),
    ("logs/seal.log", "P2: every normalization pass, appended"),
    ("logs/seal-check.log", "P2: the check-only pass that closed the fixpoint"),
    ("logs/derive-claims.log", "P4: the derivation, as it printed"),
    ("logs/head-consistency.log", "P5: the consistency audit"),
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
        elif line.startswith("attempt="):
            meta["attempt"] = line[len("attempt="):]
        elif line.startswith("log-prefix="):
            meta["prefix"] = line[len("log-prefix="):]
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
    """THE LOG THE LEDGER NAMES.

    Every entry records its own unique, attempt-prefixed path. The constructed
    names survive only as fallbacks for a ledger written before the paths were
    recorded, and the glob is the V11 shape: a two-digit ATTEMPT ordinal, then
    the slug, so a step is named the same thing on both sides.
    """
    recorded = row.get("log", "")
    if recorded:
        return logs / Path(recorded).name
    found = sorted(logs.glob("[0-9][0-9]-" + row["slug"] + end + ".log"))
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
    """attempt id -> its disposition, taken from that attempt's TERMINAL row.

    A step row never carries a disposition, so nothing can be described as
    authoritative and discarded at once; the terminal row carries it once,
    with its single reason. An attempt with no terminal row is reported as
    unresolved rather than assumed to have succeeded.
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
                continue
            seen["_terminal"] = True
            seen["status"] = str(row.get("status", "(not stated)"))
            seen["reason"] = str(row.get("reason", ""))
    for value in out.values():
        value.pop("_terminal", None)
    return out


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
                "did; the record=attempt row of the same attempt states "
                "whether that attempt is authoritative or discarded, and its "
                "one reason. resolved_status on each row is that terminal "
                "verdict, joined here mechanically.",
        "copied_at_phase": "P1, before the P3 freeze; rows the pipeline "
                           "appends after this instant are in the ledger "
                           "outside the package, not here",
        "attempts": [{"attempt": attempt,
                      "status": value["status"],
                      "reason": value["reason"]}
                     for attempt, value in sorted(dispositions.items())
                     if attempt in wanted or attempt == package_attempt
                     or attempt in package_attempts],
        "rows": keep,
    }
    path = logs / "attempts.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    return path


def write_log_index(logs: Path, batteries: list[tuple[str, dict, list[dict]]],
                    shipped_attempts: bool) -> Path:
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
        "NAMING. A battery log is <attempt ordinal>-<slug>-<side>.log. The",
        "two-digit ordinal names THE ATTEMPT, not the position of the step:",
        "it is allocated from the append-only attempt ledger that lives",
        "outside the package, so a rerun -- including a rerun against a fresh",
        "logs directory -- receives a new ordinal and cannot reuse a",
        "filename. Within one attempt a log is keyed by its slug, so a step",
        "means the same thing on both sides; the two sides are two attempts",
        "and therefore carry two ordinals, which is why the numbers differ",
        "between them.",
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
            f"- log prefix: {meta.get('prefix', '(not recorded)')}",
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
            accounted.add(log.name)
            out.append(
                f"- `logs/{log.name}`"
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
        if path.name in accounted or "__pycache__" in path.parts:
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
                        "copied in before the freeze")
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
        "These transcripts do not exist when this index is composed at P1.",
        "They are named here as declarations, exactly as `logs/assemble.sh`",
        "declares them deferred, and the phase that writes each is stated:",
        "",
    ]
    for relative, said in DEFERRED_LOGS:
        out.append(f"- `{relative}` -- {said}")
    out.append("")
    path = logs / "LOG-INDEX.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--measured", default="")
    parser.add_argument("--attempts", type=Path, default=None,
                        help="the append-only attempt ledger outside the "
                             "package; its relevant rows are copied in")
    parser.add_argument("--attempt", default="",
                        help="the assembly's own attempt id, so its rows are "
                             "copied in beside the batteries'")
    args = parser.parse_args(argv)

    logs = args.package / "logs"

    # A DISCARDED RUN'S LOGS ARE NOT EVIDENCE. The battery that abandoned them
    # said so in this directory; composing a package from them would be
    # composing figures from a record that calls itself non-evidence.
    markers = sorted(one.name for one in logs.glob("DISCARDED-*.txt"))
    if markers:
        print("REFUSING: the staged logs carry a discard marker: "
              + ", ".join(markers), file=sys.stderr)
        print("A discarded attempt's logs are a record of an attempt, not "
              "evidence of a result. Stage an authoritative run.",
              file=sys.stderr)
        return 1

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
    wanted: set[str] = set()
    for label, name in (("PARENT", "order-parent.txt"), ("HEAD", "order-head.txt")):
        meta, rows = ledger(logs / name)
        batteries.append((label, meta, rows))
        if meta.get("attempt"):
            wanted.add(meta["attempt"])
        out += ["=" * 70, f"{label} battery — {logs.name}/{name}", "=" * 70, ""]
        if not rows:
            out += ["(the ledger for this battery is not present)", ""]
            continue
        # The battery-level provenance, once, as the ledger recorded it, and
        # labelled with the instant it describes.
        out += [
            f"attempt    : {meta.get('attempt', '(not recorded)')}"
            f"  (logs of this attempt are prefixed "
            f"{meta.get('prefix', '?')}-)",
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
            report = logs / (row["slug"] + end + ".json")
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
                f"    log     : logs/{log.name}"
                + ("" if log.is_file() else "   (not shipped)"),
            ]
            if report.is_file():
                out.append(f"    report  : logs/{report.name}")
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
                f"status     : "
                f"{dispositions.get(args.attempt, {}).get('status', '?')}",
                "",
                "Rows appended after this member was composed at P1 are in the",
                "attempt ledger outside the package, which spans attempts.",
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

    shipped_attempts = False
    if args.attempts:
        if not args.attempts.is_file():
            print(f"REFUSING: no attempt ledger at {args.attempts}",
                  file=sys.stderr)
            return 1
        write_attempts(logs, attempt_rows, wanted, args.attempt)
        shipped_attempts = True

    index = write_log_index(logs, batteries, shipped_attempts)

    out += [
        "=" * 70,
        "Not recorded in this file",
        "=" * 70,
        "",
        "The sealing and sanitization passes are their own transcripts —",
        "logs/seal-check.log and logs/seal.log — and the derivation and audit",
        "are logs/derive-claims.log and logs/head-consistency.log. They are",
        "not summarised here, because a summary of a transcript is the thing",
        "this file exists to stop being written.",
        "",
        "The roster of every log, and the attempt each belongs to, is",
        f"logs/{index.name}, derived in the same pass as this file.",
    ]
    if shipped_attempts:
        out += [
            "The attempt rows themselves — including the ones belonging to",
            "attempts that were discarded — are machine-readable in",
            "logs/attempts.json, copied in before the freeze from the",
            "append-only ledger outside the package that spans attempts.",
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
        print("logs/attempts.json copied from the attempt ledger outside "
              "the package")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
