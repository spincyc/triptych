#!/usr/bin/env python3
"""IS THERE EXACTLY ONE PACKAGE, AND DOES EVERY RECORD SAY SO?

V12, the V11 independent review. The V11 package shipped a machine-readable
attempt ledger that named the SUPERSEDED package attempt `authoritative` and
gave the attempt that actually shipped the status string "unresolved: the
ledger carries no terminal row for this attempt". Its own `checks.txt`
repeated the unresolved line; its outer invocation log called the shipped
attempt authoritative; the sibling supersession marker said not to review the
earlier package; and `PROVENANCE.md` claimed every attempt carried one
terminal disposition and then named the superseded attempt the survivor. Five
records, four different answers to the one question a reviewer must settle
before reading anything else: WHICH PACKAGE IS THIS.

The ledger exists to settle that. A ledger a reader has to repair from prose
has not settled it, and the repair is exactly the step that can be done
wrongly — which is the defect this whole lane exists to refuse, arriving in
the apparatus rather than in the data.

So this runs BEFORE publication and refuses the package outright unless every
record agrees. It is a READER-side gate: it re-derives the answer from the
shipped bytes and compares, rather than trusting the pipeline that wrote them.
It writes nothing.

WHY SOME RULES LOOK LIKE TWO COPIES AND ARE NOT. `checks.py` refuses to
WRITE a ledger whose vocabulary, transitions or terminal rows are wrong, and
it is right to. It never sees the artifacts a reader actually has: the outer
invocation log, the package's prose, a discard marker, or the shipped
`logs/attempts.json` as bytes on disk after every later phase has run. So
this re-derives the resolved state of every attempt from those bytes rather
than trusting the summary written beside them, and requires the answer to be
EXACTLY one — where the writer requires at most one, because at the instant
it writes, the one has not been added yet.

The rules genuinely owned elsewhere and not restated here: that a log target
is never overwritten, that a rerun cannot reproduce a previous attempt's
filenames, that a claimed log exists, is claimed once, is non-empty or
explained, and lies under its own attempt's root. Those are
`checks.py --audit-logs`, and duplicating them here would be a second source
of truth for a rule that already has one.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- vocabulary

# V12: a completed validation battery and a sealed package attempt are
# different facts, and V11 wrote one word for both -- which is why its
# authoritative count could never be one. The two sides now have two
# vocabularies, and only a package attempt may ever be authoritative.
BATTERY_STATES = {"started", "complete", "failed"}
PACKAGE_STATES = {"started", "sealing", "authoritative", "discarded",
                  "superseded"}

# A status that resolves nothing. V11 shipped one of these on the attempt it
# was built from, so the string is matched by shape rather than by equality:
# the pipeline embeds its reason in it.
UNRESOLVED = re.compile(r"^\s*unresolved\b", re.IGNORECASE)
INCOHERENT = re.compile(r"^\s*INCOHERENT\b")

# The prose members a reviewer reads for authority, and the word that would
# make one of them disagree with the ledger.
PROSE_MEMBERS = ("checks.txt", "PROVENANCE.md", "HANDOFF.md",
                 "REVIEW_REQUEST.md", "EVIDENCE-INDEX.md", "LIMITATIONS.md",
                 "CLAIM-CLOSURE.md", "DERIVED-CLAIMS.md")

ATTEMPT_ID = re.compile(r"\b(?:head|parent|package)-\d{8}T\d{6}Z-\d{2}[a-z0-9]{6}\b")


class Refusal(Exception):
    """One reason the package may not be published."""


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise Refusal(f"{path} is missing; the ledger is not optional")
    except json.JSONDecodeError as error:
        raise Refusal(f"{path} is not readable JSON: {error}")


def terminal_rows(ledger: dict) -> tuple[dict, dict]:
    """Each attempt's terminal row and its RESOLVED state, from the rows.

    The `rows` array is the record; the `attempts` summary is a projection of
    it. Deriving from `rows` and comparing against `attempts` is the whole
    point -- V11's two disagreed and nothing compared them.

    THE RESOLVED STATE IS THE LAST ONE, not the terminal one. A package
    attempt that was authoritative and has since been superseded is no longer
    the package to review, and reading only its terminal row is how a ledger
    comes to name three authoritative attempts. Superseding does not overwrite
    the verdict it supersedes, so the terminal row is kept beside it.
    """
    found: dict[str, dict] = {}
    resolved: dict[str, str] = {}
    for row in ledger.get("rows", []):
        one = str(row.get("attempt", ""))
        kind = row.get("record")
        if kind not in ("attempt", "state"):
            continue
        if not one:
            raise Refusal(f"a {kind} row names no attempt")
        if kind == "attempt":
            if one in found:
                raise Refusal(f"{one} carries more than one terminal row")
            found[one] = row
            resolved[one] = str(row.get("status", ""))
        elif str(row.get("status", "")) == "superseded":
            resolved[one] = "superseded"
    return found, resolved


def check(package: Path, outer: Path, head: str, name: str) -> list[str]:
    problems: list[str] = []

    def fault(text: str) -> None:
        problems.append(text)

    ledger = load(package / "logs" / "attempts.json")
    rows, resolved = terminal_rows(ledger)
    summary = {str(one.get("attempt", "")): one
               for one in ledger.get("attempts", [])}

    # -- 1. every attempt the ledger mentions is resolved, one way --------
    mentioned = {str(row.get("attempt", "")) for row in ledger.get("rows", [])}
    mentioned |= set(summary)
    mentioned.discard("")
    for one in sorted(mentioned):
        stated = str(summary.get(one, {}).get("status", ""))
        if not stated:
            fault(f"{one}: the summary states no status")
        elif UNRESOLVED.match(stated):
            fault(f"{one}: unresolved in the shipped ledger -- {stated!r}")
        elif INCOHERENT.match(stated):
            fault(f"{one}: {stated}")
        if one not in rows:
            fault(f"{one}: no terminal row")

    # -- 2. the summary and the rows say the same thing -------------------
    # The summary is a projection. If it has been edited, or written from a
    # different slice of the ledger than the rows beside it, this is where a
    # reader finds out -- and V11's two disagreed with nothing comparing them.
    for one in sorted(set(resolved) | set(summary)):
        stated = str(summary.get(one, {}).get("status", ""))
        derived = resolved.get(one, "")
        if not derived:
            fault(f"{one}: in the summary, but no row resolves it")
        elif stated and stated != derived:
            fault(f"{one}: the rows resolve to {derived!r}, the summary says "
                  f"{stated!r}")

    # -- 3. the vocabularies are kept apart -------------------------------
    for one, row in sorted(rows.items()):
        side = str(row.get("side", ""))
        written = resolved.get(one, "")
        if side in ("head", "parent"):
            if written not in BATTERY_STATES:
                fault(f"{one}: a {side} battery may not be {written!r}")
            if written == "authoritative":
                fault(f"{one}: a validation battery is not an authoritative "
                      f"package")
        elif side == "package":
            if written not in PACKAGE_STATES:
                fault(f"{one}: a package attempt may not be {written!r}")
        else:
            fault(f"{one}: unknown side {side!r}")

    # -- 4. EXACTLY ONE AUTHORITATIVE PACKAGE ATTEMPT ---------------------
    authoritative = sorted(one for one, said in resolved.items()
                           if said == "authoritative")
    if len(authoritative) != 1:
        fault(f"authoritative attempts: {len(authoritative)}, not 1 "
              f"({', '.join(authoritative) or 'none'})")

    # -- 5. and it is THIS package, at THIS head --------------------------
    winner = authoritative[0] if len(authoritative) == 1 else None
    if winner:
        row = rows[winner]
        if str(row.get("package", "")) != name:
            fault(f"{winner}: authoritative for {row.get('package')!r}, not "
                  f"{name!r}")
        if str(row.get("head", "")) != head:
            fault(f"{winner}: authoritative at head {row.get('head')!r}, not "
                  f"{head!r}")
        if not str(row.get("result", "")).startswith("sealed"):
            fault(f"{winner}: result is {row.get('result')!r}, not sealed")
        if str(row.get("reason", "")):
            fault(f"{winner}: authoritative attempts carry no discard reason, "
                  f"and this one carries {row['reason']!r}")

    # -- 6. a discarded attempt says why, exactly once --------------------
    for one, row in sorted(rows.items()):
        if str(row.get("status", "")) in ("discarded", "failed"):
            reason = str(row.get("reason", "")).strip()
            if not reason:
                fault(f"{one}: discarded with no reason")

    # -- 7. the package this one supersedes is named, and is not here -----
    # A superseded attempt resolves to `superseded` and so cannot also be
    # counted authoritative; what is checked here is the other direction --
    # that the attempt THIS package claims has not itself been superseded by
    # something later in the same ledger.
    if winner:
        for row in ledger.get("rows", []):
            if (str(row.get("attempt", "")) == winner
                    and row.get("record") == "state"
                    and str(row.get("status", "")) == "superseded"):
                fault(f"{winner}: this package's own attempt is superseded")

    # -- 8. the outer invocation log agrees -------------------------------
    if not outer.exists():
        fault(f"{outer.name}: the outer invocation log is missing")
    elif winner:
        said = outer.read_text(encoding="utf-8", errors="replace")
        if winner not in said:
            fault(f"{outer.name}: never names the authoritative attempt "
                  f"{winner}")
        if name not in said:
            fault(f"{outer.name}: never names the package {name}")
        if head not in said:
            fault(f"{outer.name}: never names the head {head}")
        # And it names no OTHER attempt as the authoritative one.
        for line in said.splitlines():
            if "authoritative" not in line:
                continue
            for other in ATTEMPT_ID.findall(line):
                if other != winner:
                    fault(f"{outer.name}: calls {other} authoritative, but the "
                          f"ledger names {winner}")

    # -- 9. the package's own prose agrees ---------------------------------
    if winner:
        for member in PROSE_MEMBERS:
            path = package / member
            if not path.is_file():
                continue
            said = path.read_text(encoding="utf-8", errors="replace")
            # V11 wrote the attempt on one line and its status on the next:
            #
            #     attempt : package-20260816T172726Z-08vvjhkw
            #     status  : unresolved: the ledger carries no terminal row
            #
            # so a same-line test finds nothing and the record that actually
            # contradicted the package reads as clean. The subject of a
            # status line is whatever attempt was last named, and it stays
            # the subject until another is named or a blank line ends the
            # stanza.
            subject = ""
            for number, line in enumerate(said.splitlines(), 1):
                low = line.lower()
                named = ATTEMPT_ID.findall(line)
                if named:
                    subject = named[-1]
                elif not line.strip():
                    subject = ""
                if "authoritative" in low:
                    for other in named:
                        if other != winner:
                            fault(f"{member}:{number}: calls {other} "
                                  f"authoritative, but the ledger names "
                                  f"{winner}")
                if "unresolved" in low and subject == winner:
                    fault(f"{member}:{number}: describes the authoritative "
                          f"attempt as unresolved")
                if "survived" in low or "survivor" in low:
                    for other in ATTEMPT_ID.findall(line):
                        if other != winner:
                            fault(f"{member}:{number}: names {other} the "
                                  f"survivor, but the ledger names {winner}")

    # -- 10. nothing here was abandoned mid-flight -------------------------
    marker = sorted(one.name for one in package.glob("DISCARDED*.txt"))
    marker += sorted(one.name for one in (package / "logs").glob("DISCARDED*.txt"))
    if marker:
        fault("the package carries a discard marker: " + ", ".join(marker))

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--package", required=True, type=Path,
                        help="the built handoff directory")
    parser.add_argument("--outer", type=Path,
                        help="the outer invocation log; defaults to "
                             "<package>.assemble.log beside the package")
    parser.add_argument("--head", required=True,
                        help="the exact implementation head this package is for")
    parser.add_argument("--name", default=None,
                        help="the package basename; defaults to the "
                             "directory's own name")
    args = parser.parse_args()

    package = args.package.resolve()
    name = args.name or package.name
    outer = args.outer or package.parent / f"{name}.assemble.log"

    print("--- authority coherence")
    print(f"    package : {name}")
    print(f"    head    : {args.head}")
    print(f"    outer   : {outer.name}")
    try:
        problems = check(package, outer, args.head, name)
    except Refusal as error:
        print(f"    REFUSED : {error}")
        print("authority coherence: FAIL (1 problem)")
        return 1

    for one in problems:
        print(f"    problem : {one}")
    if problems:
        print(f"authority coherence: FAIL ({len(problems)} problem(s))")
        return 1
    print("    result  : one authoritative attempt, and every record names it")
    print("authority coherence: PASS (0 problems)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
