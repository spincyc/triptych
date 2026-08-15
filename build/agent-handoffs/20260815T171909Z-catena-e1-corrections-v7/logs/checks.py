#!/usr/bin/env python3
"""Compose `checks.txt` from the two ordering ledgers and the logs they name.

V6 wrote `checks.txt` by hand — every command, its exit and its result typed
out — and its review found five counts wrong across the package. This file is
the answer for that member specifically: the commands come from the ledgers
the batteries wrote as they ran, the exits come from the same lines, and the
headline result of each log is parsed out of the log rather than remembered.

The one thing it does not do is judge. A `check-only` line here says what the
command printed; whether the result is acceptable is argued in the documents,
which is where a judgement belongs.

Usage:
    checks.py --package DIR --head SHA --parent SHA [--measured SHA]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

# The line each suite or check reports itself by. First match wins, and a log
# that matches none is reported as such rather than summarised into silence.
HEADLINES = (
    re.compile(r"^Ran \d+ tests? in [\d.]+s$", re.M),
    re.compile(r"^(?:OK|FAILED)(?: \(.*\))?$", re.M),
    re.compile(r"^Promised-deliverable ledger .*$", re.M),
    re.compile(r"^catena (?:valid|invalid).*$", re.M),
    re.compile(r"^stale: .*$", re.M),
    re.compile(r"^\s*\"assertions\": \d+,$", re.M),
    re.compile(r"^replay-examples: .*$", re.M),
    re.compile(r"^catena\.\w+ whole \d+ stripped \d+$", re.M),
)


def ledger(path: Path) -> list[dict]:
    """One ledger, as the rows it recorded."""
    if not path.is_file():
        return []
    rows: list[dict] = []
    stamp = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if re.match(r"^\d{4}-\d\d-\d\dT", line):
            stamp = line
        elif line.startswith("START "):
            rows.append({"slug": line[6:], "start": stamp})
        elif line.startswith("CMD: ") and rows:
            rows[-1]["command"] = line[5:]
        elif line.startswith("exit=") and rows:
            rows[-1]["exit"] = line[5:]
        elif line.startswith("END ") and rows:
            rows[-1]["end"] = stamp
    return rows


def headline(log: Path) -> list[str]:
    if not log.is_file():
        return ["(no log)"]
    text = log.read_text(encoding="utf-8", errors="replace")
    said = []
    for pattern in HEADLINES:
        for found in pattern.findall(text):
            line = found.strip().strip(",")
            if line and line not in said:
                said.append(line)
    return said or ["(no headline line matched; read the log)"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--measured", default="")
    args = parser.parse_args(argv)

    logs = args.package / "logs"
    out: list[str] = [
        "Every command this lane ran, its exact invocation, its numeric exit,",
        "the log it wrote, and the commit it ran at.",
        "",
        "COMPOSED, NOT TYPED. `logs/checks.py` reads the ordering ledgers the",
        "two batteries wrote as they ran and the logs those ledgers name. V6",
        "wrote this member by hand and its review found five counts wrong",
        "across the package; the answer for this one is that nobody writes it.",
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

    for label, name in (("PARENT", "order-parent.txt"), ("HEAD", "order-head.txt")):
        rows = ledger(logs / name)
        out += ["=" * 70, f"{label} battery — {logs.name}/{name}", "=" * 70, ""]
        if not rows:
            out += ["(the ledger for this battery is not present)", ""]
            continue
        for row in rows:
            log = logs / (row["slug"] + ("-parent.log" if label == "PARENT"
                                         else "-head.log"))
            if not log.is_file():
                log = logs / (row["slug"] + ".log")
            out += [
                f"--- {row['slug']}",
                f"    command : {row.get('command', '(not recorded)')}",
                f"    exit    : {row.get('exit', '?')}",
                f"    started : {row.get('start', '?')}",
                f"    ended   : {row.get('end', '?')}",
                f"    log     : logs/{log.name}"
                + ("" if log.is_file() else "   (not shipped)"),
            ]
            for said in headline(log):
                out.append(f"    result  : {said}")
            out.append("")

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
        "No judgement is recorded here either. What a result MEANS is argued",
        "in HANDOFF.md, LIMITATIONS.md and UNRESOLVED-BLOCKERS.md.",
        "",
    ]
    (args.package / "checks.txt").write_text("\n".join(out), encoding="utf-8")
    print(f"checks.txt composed: {len(out)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
