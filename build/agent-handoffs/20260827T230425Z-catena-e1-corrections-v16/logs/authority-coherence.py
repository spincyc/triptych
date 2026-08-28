#!/usr/bin/env python3
"""IS THERE EXACTLY ONE PACKAGE, DOES EVERY RECORD SAY SO, AND DID P8 SAY IT?

V13, the V12 independent review. V12 answered "which attempt is authoritative"
with a ledger and a gate over it, and the gate passed a package whose own
shipped `logs/attempts.json` carried MORE THAN ONE row reading
`record=attempt status=authoritative` -- only a last-state-wins resolver
demoted the extras -- while a sibling `<package>.SUPERSEDED.txt` sat in the
directory the gate never opened. The gate read two files. The package ships
seven records, and the four it did not read were the ones that disagreed.

The deeper defect is not coverage, it is ORDER. V12 wrote the authoritative
row at P5, BEFORE the manifest, before the ZIP existed, and before P7 and P8
had verified anything. Sealed bytes claimed final authority ahead of the proof
that they were sound, and the claim was kept honest only by a convention that
a later failure would go back and supersede the row. A record that must be
repaired later has not settled anything, which is the same defect as V11's,
one phase earlier.

THE REQUIRED PROGRESSION, and this gate enforces it:

    attempt started -> package sealed -> P7/P8 verification
                    -> post-P8 ZIP size/hash confirmed
                    -> FINAL AUTHORITY ESTABLISHED

If P8 fails, the attempt remains non-authoritative. No sealed package bytes
may claim final authority before P8. Therefore:

  * final authority is established by exactly one record, the FINAL-AUTHORITY
    SIDECAR beside the package, written after P8 and naming what P8 proved.

THE WORD IS NOT THE CLAIM. An earlier draft of this gate refused the word
`authoritative` wherever it appeared in P5-frozen bytes, and that was wrong in
a way the lane hit on its eleventh attempt: attempt 07 sealed, passed P8, was
legitimately established authoritative by its own sidecar, and was then
superseded at P10 with its one reason. Attempt 11 sealed cleanly, passed P8,
and was refused -- because its predecessor's HONEST HISTORY was still in the
record. The only way to satisfy that gate was to delete the predecessor's
authoritative row, which is precisely the V12 defect this lane exists to close
(V12 deleted four discarded attempts and four set-aside battery cohorts from
its record). A gate whose only remedy is falsifying history is a worse gate
than none.

So the refusal is on the HELD CLAIM, never on the presence of the word, and it
is exactly two rules:

  (a) IN EITHER SCOPE, `authoritative` may not be a DISPOSITION -- it may not
      sit on a `record=attempt` row. A terminal row is written before the
      manifest is taken, and so before P7 built the archive and before P8
      judged it; a row that cannot know P8's verdict cannot carry it. The most
      a terminal row may say is `sealed`.

  (b) IN THE IN-PACKAGE SCOPE, no attempt may still RESOLVE to
      `authoritative`. Final authority is held by the sidecar, outside; a
      predecessor must already be superseded before a replacement seals.

`authoritative` on a post-terminal `record=state` row that a later
`superseded` row demotes is therefore HISTORY, and passes. The in-package
transition `sealed -> authoritative -> superseded` is expressible on purpose:
both scopes share one package vocabulary, and the two rules above carry the
scope distinction. Externally the winner MUST resolve to `authoritative` --
that is where the claim belongs.

WHY A SIDECAR, AND WHY THE BINDING RUNS ONE WAY. Nothing may be written inside
the package after its manifest is taken, so the record cannot live in the ZIP.
It therefore lives beside it and is bound to it cryptographically: the record
names the ZIP's SHA-256, its exact byte size and its exact basename, and this
gate RECOMPUTES all three from the archive itself rather than believing the
record or the `.zip.sha256` sidecar. The binding is deliberately NOT
self-referential -- the record names the ZIP's digest; the ZIP does not name
the record's. A mutual binding is unconstructible (each would have to be
hashed after the other), and a record the archive vouched for would be a
record the archive could have been sealed around.

The same one-way binding is what proves the ORDER without trusting a clock:
the record must quote the P8 verdict and the POST-verification rehash digest,
neither of which exists until P8 has run to completion over those exact bytes.
A record carrying them cannot have been written first.

THE FINAL-AUTHORITY SIDECAR SCHEMA. JSON object, at
`<package>.authority.json` beside the package (never inside it). Every key is
required; every value is a string unless marked. Unknown keys are a fault, so
that a field this gate does not check cannot be smuggled in beside one it
does.

    {
      "schema":         "catena-final-authority/2",   # exact literal
      "attempt":        "package-YYYYMMDDTHHMMSSZ-NNxxxxxx",
      "package":        "<package basename>",         # == --name
      "head":           "<40 lowercase hex>",         # == --head
      "zip_name":       "<package basename>.zip",     # basename only
      "zip_bytes":      123456,                       # INTEGER, exact size
      "zip_sha256":     "<64 lowercase hex>",         # of the ZIP's bytes
      "p8_log":         "<package basename>.verify-final.log",  # basename
      "p8_result":      "PASS",                       # PASS | FAIL
      "rehash_result":  "UNCHANGED",                  # UNCHANGED | CHANGED
      "rehash_bytes":   123456,                       # INTEGER, post-P8 size
      "rehash_sha256":  "<64 lowercase hex>",         # post-P8 digest
      "status":         "authoritative",              # exact literal
      "established":    "2026-08-17T19:42:59Z",       # ISO-8601, UTC

      # /2: THE DIRECT BINDINGS. V15 bound its parent and its predecessor
      # review TRANSITIVELY, through the archive and the evidence commit.
      "lane":           "V16",
      "parent":         "<40 lowercase hex>",         # the exact parent head
      "review_commit":  "<40 lowercase hex>",         # the review answered
      "ledger_name":    "<package basename>.attempts.jsonl",
      "ledger_sha256":  "<64 lowercase hex>",         # of that slice's bytes

      # /2: FILLED BY --bind-final, AFTER P11 AND P12. Empty at P9, because
      # neither verdict exists then, and a record carrying one that did not
      # exist yet is the fault the V13 phase order was built to end.
      "outer_scan_result":   "CLEAN",                 # from P11's transcript
      "completeness_result": "COMPLETE",              # from P12's verdict
      "completeness_log":    "<package basename>.handoff-inventory.log",

      # /2: THE ONE THAT CANNOT BE BOUND DIRECTLY AT ALL.
      "evidence_commit":      "",                     # always empty; see note
      "evidence_commit_note": "<why, in words>",
      "deferred_bindings":    {}                      # empty when finished
    }

    Required to pass: `status` is `authoritative`; `p8_result` is `PASS` and
    matches the transcript's own verdict line; `rehash_result` is `UNCHANGED`
    and matches the transcript's rehash block; `zip_bytes`/`zip_sha256` and
    `rehash_bytes`/`rehash_sha256` all equal the values this gate recomputes
    from the ZIP on disk; `zip_name` is the ZIP's real basename; `package`
    and `head` are this package and this head; and `attempt` resolves to
    `sealed` -- never to `authoritative` -- in the package's own ledger.

    A `FAIL` p8_result, or a `CHANGED` rehash, is not a way to be
    authoritative with an excuse. It is a refusal: the attempt is not
    authoritative and no record may say it is.

WHAT ELSE THIS READS, and why each one. It is a READER-side gate: it
re-derives the answer from the shipped bytes and compares, rather than
trusting the pipeline that wrote them. It writes nothing.

  --package    the built handoff directory; its `logs/attempts.json` is the
               attempt record and `logs/attempts.json`'s `attempts` array is
               a projection of it that must agree
  --outer      `<package>.assemble.log`, the outer invocation log
  --zip        the shipped archive; hashed and sized HERE, from the bytes
  --sidecar    `<package>.zip.sha256`, which must agree with that recompute
  --verify-log `<package>.verify-final.log`, the P8 transcript
  --authority  `<package>.authority.json`, the final-authority record above
  --ledger     the external, complete, append-only `*.jsonl` attempt ledger,
               which must carry a terminal disposition for every attempt the
               package mentions, and a reason for every disposition that is
               not a SUCCESS. A success explains nothing: a battery that ran
               green, or a package attempt that sealed, is the normal outcome
               and owes no account of itself
  and the sibling markers `<name>.zip.DISCARDED.txt`, `<name>.DISCARDED.txt`,
  `<name>.SUPERSEDED.txt`, which V12 wrote beside the package and never read.

`--pre-p8` is the only way to run without the post-P8 inputs, and it is not a
relaxation: it asserts the opposite claim, that NO record anywhere calls any
attempt authoritative yet.

STRUCTURED DATA FIRST. The authority source is the sidecar and the ledgers.
The prose scan over `PROVENANCE.md` and its siblings is a BACKSTOP that
catches a record disagreeing with them; it never establishes authority. It
reads across lines because V11 wrote the attempt on one line and its status on
the next, and it folds case because an id in a case variant is a second
spelling of an identity that must have exactly one.

WHY SOME RULES LOOK LIKE TWO COPIES AND ARE NOT. `checks.py` refuses to WRITE
a ledger whose vocabulary, transitions or terminal rows are wrong, and it is
right to. It never sees the artifacts a reader actually has. So this
re-derives the resolved state of every attempt from the shipped bytes rather
than trusting the summary written beside them.

The rules genuinely owned elsewhere and not restated here: that a log target
is never overwritten, that a rerun cannot reproduce a previous attempt's
filenames, that a claimed log exists, is claimed once, is non-empty or
explained, and lies under its own attempt's root. Those are
`checks.py --audit-logs`. That the ZIP's members match the manifest, and that
the trust anchor holds, is `verify-final-package.py` -- this gate reads its
VERDICT, and does not re-run it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
import zipfile
from pathlib import Path

# ---------------------------------------------------------------- vocabulary

# V12: a completed validation battery and a sealed package attempt are
# different facts, and V11 wrote one word for both -- which is why its
# authoritative count could never be one. The two sides have two vocabularies.
#
# V13 adds `set-aside`: a battery that RAN GREEN and whose figures were then
# not used. The old vocabulary had no word for it, so such a battery stayed
# `complete` with an empty reason and was indistinguishable from one whose
# figures were used. It is post-terminal and shaped exactly like `superseded`
# -- appended as a later `record=state` row, leaving the `complete` terminal
# row where it is -- and, like every non-authoritative terminal state, it
# REQUIRES a reason: the whole point of the word is to say why.
# V16: TWO AXES, AND THIS SET IS THE UNION OF BOTH. A battery attempt's
# EXECUTION disposition is `complete`, `failed` or `abandoned`; its EVIDENCE
# disposition -- whether the measurements a completed cohort took are the ones
# a package reports -- is `authoritative` or `set-aside`, carried by a later
# `record=state` row that leaves the terminal row where it is.
#
# `abandoned` was missing here entirely, and it is a terminal battery
# disposition `checks.py` has written since V16: a run something OUTSIDE the
# battery stopped, with no step having failed. Without it this gate refused a
# package for shipping the honest record of one.
#
# `authoritative` was missing for the opposite reason -- the assumption that
# the word could only ever mean "the package to review". It means that on the
# PACKAGE side. On the battery side it means "these are the figures this
# package reports", which is a different claim, is knowable at P5 because the
# package is shipping them, and is what `--authoritative-evidence` records.
# The two are kept apart by the two rules below rather than by one vocabulary.
BATTERY_STATES = {"started", "complete", "failed", "abandoned",
                  "authoritative", "set-aside"}

# The execution disposition a battery's EVIDENCE row may follow. Setting aside
# or carrying the figures of a battery that never completed is a different
# fact, and `failed` and `abandoned` already have words: an attempt that
# measured nothing has nothing to carry or to decline.
SET_ASIDE_FROM = "complete"
BATTERY_EVIDENCE = {"authoritative", "set-aside"}

# ONE package vocabulary, shared by both scopes, matching `checks.py`'s
# EXTERNAL_PACKAGE_STATES. `authoritative` is in it so that the honest history
# `sealed -> authoritative -> superseded` is EXPRESSIBLE in shipped bytes; the
# scope distinction is carried by the two rules in the module docstring, not by
# two vocabularies. A vocabulary that cannot spell a true fact forces the
# pipeline to delete it, and deleting it is the defect.
#
# `set-aside` is deliberately NOT here: a package attempt is discarded or
# superseded, never set aside -- its bytes are the deliverable, not a figure
# to cite.
# `abandoned` joins them for the reason the comment above already gives: a
# vocabulary that cannot spell a true fact forces the pipeline to delete it.
# An assembly stopped from outside reached no decision of its own -- no phase
# refused it and no gate failed -- and `discarded` would assert one. This gate
# held its own copy of the package vocabulary, so teaching `checks.py` the word
# left this file still refusing it; that is the second time a stale copy of a
# vocabulary in THIS file has refused a true record, and both times the fix was
# the word, not the record.
PACKAGE_STATES = {"started", "sealing", "sealed", "authoritative",
                  "discarded", "superseded", "abandoned"}

# EVERY TERMINAL STATE IS EXACTLY ONE OF THESE TWO, and which one decides
# whether it owes a reason. Getting this partition wrong in either direction
# is a contract bug, not a strictness dial: demanding a reason from a success
# refuses every well-formed package, and excusing one from a failure is the
# V12 defect ("set aside" with an empty reason) all over again.
#
# `SUCCESSFUL_STATES` is `checks.py`'s settled set, restated here because this
# gate reads bytes that tool never sees. It is pinned against the per-side
# vocabularies below, so the two cannot drift apart silently.
SUCCESSFUL_STATES = {"complete", "sealed", "authoritative"}

# A terminal state that is NOT a success has to say why it is not. A success
# explains nothing: a battery that ran green and whose figures were used is
# the normal outcome, and so is a package attempt that sealed.
REASON_REQUIRED = {"discarded", "failed", "superseded", "set-aside",
                   "abandoned"}

# The dispositions that end an attempt in the external complete ledger.
TERMINAL_STATES = SUCCESSFUL_STATES | REASON_REQUIRED

assert not (SUCCESSFUL_STATES & REASON_REQUIRED), \
    "a terminal state either owes a reason or does not; never both"
assert TERMINAL_STATES == ((BATTERY_STATES - {"started"})
                           | (PACKAGE_STATES - {"started", "sealing"})), \
    "a side's vocabulary grew a terminal state the reason rule does not cover"

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

# Case-folded on purpose: `PACKAGE-...-03ABCDEF` is not a different attempt,
# it is a second spelling of one, and a gate that cannot see it is a gate a
# contradiction walks past.
ATTEMPT_ID = re.compile(
    r"\b(?:head|parent|package)-\d{8}T\d{6}Z-\d{2}[a-z0-9]{6}\b",
    re.IGNORECASE)

# A package basename: the stamp, then words. The lookbehind keeps it from
# matching the tail of an attempt id (`package-20260817T000000Z-03abcdef`).
PACKAGE_TOKEN = re.compile(
    r"(?<![\w-])(\d{8}T\d{6}Z-[A-Za-z][A-Za-z0-9]*(?:-[A-Za-z0-9]+)*)")

# The words that make a line a claim of final authority.
AUTHORITY_WORDS = ("authoritative", "final authority")
#: A line that DENIES authority is not a claim to it. A record must be able to
#: say an attempt is not authoritative -- the assembler's own history summary
#: does exactly that, naming the abandoned attempts and stating they are "in no
#: successful and no authoritative tally" -- and a scan that reads the word
#: without its negation refuses the sentence for saying the true thing. Matched
#: against the whole line, because the denial and the ids share it.
#: A TALLY IS NOT A CLAIM. `evidence : authoritative 2, superseded 9` counts
#: how many attempts hold each disposition; it says nothing about WHICH, and
#: the ids on the next line belong to a different sentence. Read as a claim, it
#: made the following line's ids resolve against it -- so the assembler's own
#: summary of its history refused the package it was summarising.
AUTHORITY_TALLY = re.compile(
    r"(?:authoritative|final authority)\s*[:=]?\s*\d", re.I)
AUTHORITY_DENIED = re.compile(
    r"\b(?:no|not|never|neither|nor|non-|un)\s*"
    r"(?:\w+\s+){0,3}?(?:authoritative|final authority)"
    r"|\bin no (?:\w+\s+){0,3}?tally"
    r"|\bnot the (?:\w+\s+){0,3}?authority", re.I)

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"(?:Z|[+-]\d{2}:?\d{2})$")

# The final-authority record's schema, as (key, python type).
AUTHORITY_SCHEMA = {
    "schema": str,
    "attempt": str,
    "package": str,
    "head": str,
    "zip_name": str,
    "zip_bytes": int,
    "zip_sha256": str,
    "p8_log": str,
    "p8_result": str,
    "rehash_result": str,
    "rehash_bytes": int,
    "rehash_sha256": str,
    "status": str,
    "established": str,
    # ---- /2: THE DIRECT BINDINGS ------------------------------------------
    #
    # V16, THE V15 REVIEW: the parent and the V14 review were "bound
    # transitively through the archive and the final evidence commit". A
    # transitive binding is a chain, and a chain is only as good as the reader
    # willing to follow it. Every one of these names the thing itself.
    "lane": str,
    "parent": str,
    "review_commit": str,
    "ledger_name": str,
    "ledger_sha256": str,
    # ---- /2: THE THREE THAT CANNOT EXIST AT P9 ----------------------------
    #
    # P9 is where authority is established, and it runs BEFORE the outer scan
    # (P11) and before the final completeness verdict (P12). A record written
    # at P9 carrying either value would be carrying a verdict that did not
    # exist yet -- which is precisely the fault V13's reordering was built to
    # end. They are declared empty at P9 and FILLED by the one protocol-
    # permitted post-verdict step, which `--bind-final` performs and which
    # this gate accounts for by requiring them to be non-empty and to match
    # the transcripts they name.
    "outer_scan_result": str,
    "completeness_result": str,
    "completeness_log": str,
    # THE ONE THAT CAN NEVER BE BOUND DIRECTLY, AND THE REASON IS STRUCTURAL.
    # This record is committed; the commit that carries it cannot be named
    # inside it, because naming it would change the bytes and therefore the
    # commit. What IS bound directly is everything the commit contains: the
    # archive's digest, the package basename, the head, the parent, the
    # review commit and the ledger's digest. A reader resolves the evidence
    # commit by finding the commit whose tree carries this record; the record
    # says so, in `evidence_commit_note`, rather than leaving the gap silent.
    "evidence_commit": str,
    "evidence_commit_note": str,
    # field name -> why it is not filled yet. Empty on a finished record.
    "deferred_bindings": dict,
}
AUTHORITY_SCHEMA_ID = "catena-final-authority/2"
AUTHORITY_SCHEMA_ID_V1 = "catena-final-authority/1"

#: The fields P9 cannot fill and `--bind-final` must. A record still carrying
#: any of them as deferred is a record whose authority is not yet complete.
DEFERRABLE = ("outer_scan_result", "completeness_result", "completeness_log",
              "ledger_sha256")

#: What each deferred field must say once bound.
BOUND_VALUES = {
    "outer_scan_result": ("CLEAN",),
    "completeness_result": ("COMPLETE",),
}


def superseded_authorities(rows: list[dict]) -> frozenset[str]:
    """Attempts the LEDGER shows held authority and then lost it.

    Derived, not declared. An attempt that really did reach final authority
    and was really superseded is a fact this lane's own history records, and a
    record that names it is telling the truth about its own past. Requiring it
    to be declared as a foreign mention would mean maintaining a list that
    grows with every superseded assembly, which is the kind of hand-kept
    inventory this protocol replaces everywhere else.
    """
    held, lost = set(), set()
    for row in rows:
        attempt, status = str(row.get("attempt", "")), str(row.get("status", ""))
        if status == "authoritative":
            held.add(attempt)
        elif status == "superseded":
            lost.add(attempt)
    return frozenset(held & lost)


def declared_attempts(package: pathlib.Path) -> frozenset[str]:
    """Attempt ids this package declares it discusses without being them."""
    named = package / "logs" / "named-attempts.json"
    if not named.is_file():
        return frozenset()
    try:
        stated = json.loads(named.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return frozenset()
    listed = stated.get("attempts")
    return frozenset(listed) if isinstance(listed, dict) else frozenset()

def deferred_names(record: dict) -> set[str]:
    """The fields this record itself declares it has not bound yet."""
    stated = record.get("deferred_bindings")
    return set(stated) if isinstance(stated, dict) else set()


class Refusal(Exception):
    """One reason the package may not be published, found before the rest."""


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise Refusal(f"{path} is missing; the ledger is not optional")
    except json.JSONDecodeError as error:
        raise Refusal(f"{path} is not readable JSON: {error}")


def canonical(one: str) -> str:
    """The one spelling of an attempt id: lowercase, but for the stamp's T/Z."""
    return re.sub(r"(\d{8})t(\d{6})z",
                  lambda m: f"{m.group(1)}T{m.group(2)}Z", one.lower())


def digest_and_size(path: Path) -> tuple[str, int]:
    """The archive's SHA-256 and byte size, FROM THE ARCHIVE."""
    hashed = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hashed.update(block)
    return hashed.hexdigest(), path.stat().st_size


def terminal_rows(ledger: dict) -> tuple[dict, dict]:
    """Each attempt's terminal row and its RESOLVED state, from the rows.

    The `rows` array is the record; the `attempts` summary is a projection of
    it. Deriving from `rows` and comparing against `attempts` is the whole
    point -- V11's two disagreed and nothing compared them.

    THE RESOLVED STATE IS THE LAST ONE, not the terminal one. A package
    attempt that was sealed and has since been superseded is no longer the
    package to review, and reading only its terminal row is how a ledger comes
    to name three authoritative attempts. Superseding does not overwrite the
    verdict it supersedes, so the terminal row is kept beside it.

    V13: EVERY state row moves the resolved state, not only `superseded`.
    V12's `elif` updated the state only for `superseded`, so a
    `record=state status=authoritative` row was silently dropped -- a second
    claim of authority that the "exactly one" count could not see -- and a
    `discarded` state after a winning row left the winner still winning.
    """
    found: dict[str, dict] = {}
    resolved: dict[str, str] = {}
    for row in ledger.get("rows", []):
        one = canonical(str(row.get("attempt", "")))
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
    return found, resolved


# ------------------------------------------------------------ the P8 record

def read_verify_log(path: Path) -> dict:
    """The P8 transcript's verdict and its post-verification rehash block."""
    said = path.read_text(encoding="utf-8", errors="replace")
    out: dict = {"verdict": "", "rehash": "", "bytes": None, "sha256": ""}
    verdict = re.search(r"^P8 verification:\s*(PASS|FAIL)\b", said,
                        re.MULTILINE)
    if verdict:
        out["verdict"] = verdict.group(1)
    lines = said.splitlines()
    start = 0
    for number, line in enumerate(lines):
        if "post-verification rehash" in line.lower():
            start = number
            break
    for line in lines[start:]:
        got = re.search(r"post-check bytes\s*:\s*(\d+)", line)
        if got:
            out["bytes"] = int(got.group(1))
        got = re.search(r"post-check sha256\s*:\s*([0-9a-fA-F]{64})", line)
        if got:
            out["sha256"] = got.group(1).lower()
        got = re.search(r"^\s*result\s*:\s*(UNCHANGED|CHANGED)\b", line)
        if got:
            out["rehash"] = got.group(1)
    return out


def read_sidecar(path: Path) -> dict:
    """The `.zip.sha256` sidecar: the digest line, then the byte-size line."""
    said = path.read_text(encoding="utf-8", errors="replace")
    out: dict = {"sha256": "", "name": "", "bytes": None, "bytes_name": ""}
    for line in said.splitlines():
        got = re.match(r"^([0-9a-fA-F]{64})\s+\*?(\S+)\s*$", line)
        if got and not out["sha256"]:
            out["sha256"] = got.group(1).lower()
            out["name"] = got.group(2)
            continue
        got = re.match(r"^(\d+)\s+bytes\s+\*?(\S+)\s*$", line)
        if got and out["bytes"] is None:
            out["bytes"] = int(got.group(1))
            out["bytes_name"] = got.group(2)
    return out


def read_external_ledger(path: Path) -> tuple[dict, list[dict], list[str]]:
    """The external append-only ledger, folded to a last-row-wins disposition.

    Returns the fold, the rows IN ORDER, and any unreadable lines. The ordered
    rows are needed because rule (a) -- `authoritative` may never be a
    disposition -- is about the shape of an individual row, which a fold
    cannot see.
    """
    seen: dict[str, dict] = {}
    ordered: list[dict] = []
    broken: list[str] = []
    for number, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as error:
            broken.append(f"{path.name}:{number}: not readable JSON: {error}")
            continue
        if not isinstance(row, dict):
            broken.append(f"{path.name}:{number}: not a JSON object")
            continue
        one = canonical(str(row.get("attempt", "")))
        if not one:
            continue
        status = str(row.get("status", ""))
        if not status:
            continue
        ordered.append(row)
        seen[one] = row
    return seen, ordered, broken


# ---------------------------------------------------------- the prose scan

# A battery attempt id: the side, then the stamp. A package attempt id says
# `package-`, and only those can claim to have sealed anything.
BATTERY_ATTEMPT = re.compile(r"^(?:parent|head)-\d{8}T\d{6}Z-")


def scan_prose(text: str, winner: str, label: str, fault,
               package_name: str | None = None,
               foreign: frozenset[str] = frozenset()) -> int:
    """The BACKSTOP scan of one prose member or log. Returns winner mentions.

    Never a source of authority: it can only contradict the structured record.
    Three things V12 could not see, and this does:

      * a claim on one line and the id on the NEXT. V11 shipped exactly that
        shape, so a same-line test read the contradicting stanza as clean;
      * an id in a case variant, which is a second spelling of one identity;
      * an authority line that names the WRONG PACKAGE. V12 only checked that
        the package name appeared somewhere in the file.
    """
    lines = text.splitlines()
    subject = ""
    pending = 0        # line number of a claim whose id has not arrived yet
    mentions = 0

    def check_package(numbers: list[int], number: int) -> None:
        if not package_name:
            return
        tokens: list[str] = []
        for one in numbers:
            tokens += PACKAGE_TOKEN.findall(lines[one - 1])
        tokens = [one for one in tokens
                  if not ATTEMPT_ID.fullmatch(one)]
        if tokens and package_name not in tokens:
            fault(f"{label}:{number}: the line claiming authority names "
                  f"package {tokens[0]!r}, not {package_name!r}")

    def resolve(targets: list[str], numbers: list[int], number: int) -> None:
        nonlocal mentions
        for one in targets:
            # TWO AXES, ONE WORD. V16: `authoritative` is the evidence
            # disposition a completed BATTERY cohort carries when the package
            # derives its figures from that cohort's transcripts, and it is
            # separately the name for the one PACKAGE attempt that reached
            # final authority. Both readings are correct and they are about
            # different things: a battery cohort never seals an archive, and a
            # package attempt never measures an endpoint.
            #
            # This scan exists to catch a package naming the WRONG SEALING
            # ATTEMPT, which is a package-side claim. Reading a battery
            # cohort's evidence disposition as such a claim made the gate
            # refuse eleven true sentences -- every one of which correctly
            # named a cohort whose figures the package carries -- and would
            # have forced the prose to stop saying which cohorts its numbers
            # came from in order to pass. A gate that can only be satisfied by
            # removing true statements is measuring the wrong thing.
            if BATTERY_ATTEMPT.match(one):
                continue
            # AND AN ATTEMPT OF ANOTHER LANE, DECLARED. This scan is right to
            # refuse a package naming the wrong sealing attempt; it is wrong
            # to refuse a package RECORDING A PREDECESSOR'S HISTORY, and this
            # lane's record names two V15 package attempts -- the one that
            # sealed the archive V16 supersedes, and the one that held
            # authority for a second before its own gate refused it. Omitting
            # the second would be the defect this lane corrects. The ids are
            # declared in `logs/named-attempts.json` with a reason each, in
            # the same shape as the entitled-SHA record, and an id not
            # declared there is still refused.
            if one in foreign:
                continue
            if one != winner:
                fault(f"{label}:{number}: calls {one} authoritative, but the "
                      f"final-authority record names {winner}")
            else:
                mentions += 1
                check_package(numbers, number)

    for number, line in enumerate(lines, 1):
        low = line.lower()
        raw = ATTEMPT_ID.findall(line)
        ids = [canonical(one) for one in raw]
        for one in raw:
            if one != canonical(one):
                fault(f"{label}:{number}: spells the attempt {one!r}, a case "
                      f"variant of {canonical(one)!r}")
        if ids:
            subject = ids[-1]
        elif not line.strip():
            subject = ""
            pending = 0

        claims = (any(word in low for word in AUTHORITY_WORDS)
                  and not AUTHORITY_DENIED.search(line)
                  and not AUTHORITY_TALLY.search(line))
        if claims:
            targets = ids or ([subject] if subject else [])
            if targets:
                resolve(targets, [number], number)
                pending = 0
            else:
                # The claim is made; the id may be on a following line.
                pending = number
        elif pending and ids:
            resolve(ids, [pending, number], number)
            pending = 0

        if "unresolved" in low and subject == winner:
            fault(f"{label}:{number}: describes the authoritative attempt as "
                  f"unresolved")
        if "survived" in low or "survivor" in low:
            for one in ids or ([subject] if subject else []):
                if one != winner:
                    fault(f"{label}:{number}: names {one} the survivor, but "
                          f"the final-authority record names {winner}")
    return mentions


def scan_for_any_authority(text: str, label: str, fault) -> None:
    """--pre-p8: assert the opposite claim, that NOBODY says authoritative."""
    for number, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if (any(word in low for word in AUTHORITY_WORDS)
                and not AUTHORITY_DENIED.search(line)
                and not AUTHORITY_TALLY.search(line)):
            fault(f"{label}:{number}: claims final authority before P8 -- "
                  f"{line.strip()!r}")


# ------------------------------------------------------------------- markers

def sibling_markers(package: Path, name: str) -> list[str]:
    """The markers V12 wrote BESIDE the package and then never opened."""
    beside = package.parent
    found = []
    for candidate in (f"{name}.zip.DISCARDED.txt", f"{name}.DISCARDED.txt",
                      f"{name}.SUPERSEDED.txt", f"{name}.zip.SUPERSEDED.txt"):
        if (beside / candidate).exists():
            found.append(candidate)
    for path in sorted(beside.glob(f"{name}*.txt")):
        if ("DISCARDED" in path.name or "SUPERSEDED" in path.name) \
                and path.name not in found:
            found.append(path.name)
    return found


# --------------------------------------------------------------- the gate

def check(args) -> list[str]:
    problems: list[str] = []

    def fault(text: str) -> None:
        problems.append(text)

    package: Path = args.package
    name: str = args.name
    head: str = args.head

    ledger = load(package / "logs" / "attempts.json")
    rows, resolved = terminal_rows(ledger)
    summary = {canonical(str(one.get("attempt", ""))): one
               for one in ledger.get("attempts", [])}

    # -- 1. every attempt the ledger mentions is resolved, one way --------
    mentioned = {canonical(str(row.get("attempt", "")))
                 for row in ledger.get("rows", [])}
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
            # ON THE EXECUTION AXIS, NOT THE EVIDENCE ONE. What a battery may
            # never be is authoritative AS ITS DISPOSITION -- that is V11's
            # root defect, one word for "this ran to completion" and "this is
            # the package to review". A later `record=state` row saying the
            # package reports this cohort's figures is the EVIDENCE axis and
            # is a different claim; check 4b below keeps the package-side
            # meaning of the word where it belongs.
            if str(row.get("status", "")) == "authoritative":
                fault(f"{one}: a validation battery is not an authoritative "
                      f"package")
        elif side == "package":
            if written not in PACKAGE_STATES:
                fault(f"{one}: a package attempt may not be {written!r}")
        else:
            fault(f"{one}: unknown side {side!r}")

    # -- 4. THE WORD MAY BE HISTORY; THE CLAIM MAY NOT BE HELD ------------
    # Rule (a). Every row in `logs/attempts.json` was written before the
    # manifest was taken, and so before P7 produced the ZIP and before P8
    # judged it. A TERMINAL row claiming `authoritative` is carrying a verdict
    # that did not exist when it was written. `sealed` is the most it may say.
    # This holds in either scope: a disposition is a disposition.
    for row in ledger.get("rows", []):
        if row.get("record") == "attempt" \
                and str(row.get("status", "")) == "authoritative":
            one = canonical(str(row.get("attempt", "")))
            fault(f"{one}: carries 'authoritative' as a DISPOSITION, on a "
                  f"record=attempt row; P8 had not run when that terminal row "
                  f"was written, so it cannot hold P8's verdict. The most a "
                  f"terminal row may say is 'sealed'")

    # Rule (b). The claim itself is held OUTSIDE, by the post-P8 sidecar. An
    # attempt that still RESOLVES to `authoritative` in shipped bytes is
    # holding it inside. Note what this does NOT refuse: `authoritative` on a
    # post-terminal state row that a later `superseded` row demotes resolves
    # to `superseded`, and is honest history of a predecessor that really was
    # authoritative once. Refusing that would leave deletion as the only
    # remedy, which is the defect this lane exists to close.
    # A PACKAGE ATTEMPT'S, AND ONLY A PACKAGE ATTEMPT'S. A battery cohort
    # resolving to `authoritative` is saying which measurements this package
    # reports -- a fact the pipeline HAS at P5, because it is shipping them --
    # and not the verdict of a verification that has not run.
    held: list[str] = []
    for one, said in sorted(resolved.items()):
        if said == "authoritative" and str(
                rows.get(one, {}).get("side", "")) == "package":
            fault(f"{one}: still RESOLVES to 'authoritative' inside the "
                  f"package; these bytes were frozen before P8 ran, so final "
                  f"authority is held outside by the post-P8 sidecar. A "
                  f"predecessor must already be superseded before a "
                  f"replacement seals")
            held.append(one)

    # -- 5. the final-authority sidecar -----------------------------------
    record: dict = {}
    winner = ""
    zip_sha = ""
    zip_bytes: int | None = None
    verdict: dict = {}

    if args.pre_p8:
        for label, path in (("the final-authority record", args.authority),
                            ("the ZIP", args.zip),
                            ("the P8 transcript", args.verify_log)):
            if path.exists():
                fault(f"--pre-p8 was given, but {label} {path.name} already "
                      f"exists; the attempt has reached P8 or is claiming to")
        if held:
            fault(f"--pre-p8 was given, but the package ledger already holds "
                  f"{', '.join(sorted(held))} authoritative")
    else:
        # -- 5a. the archive, hashed HERE, from its own bytes -------------
        if not args.zip.exists():
            fault(f"{args.zip.name}: the shipped archive is missing; final "
                  f"authority names an archive, so there is nothing to name")
        else:
            zip_sha, zip_bytes = digest_and_size(args.zip)
            try:
                with zipfile.ZipFile(args.zip) as archive:
                    members = archive.namelist()
            except (zipfile.BadZipFile, OSError) as error:
                fault(f"{args.zip.name}: unreadable as a ZIP: {error}")
                members = []
            # The binding runs ONE WAY. A record the archive vouched for is a
            # record the archive could have been sealed around.
            for member in members:
                base = member.rsplit("/", 1)[-1]
                if base.endswith(".authority.json") or base == args.authority.name:
                    fault(f"{args.zip.name}: carries {member!r}; the final "
                          f"authority record may not live inside the archive "
                          f"it binds")

        # -- 5b. the `.zip.sha256` sidecar agrees with that recompute -----
        if not args.sidecar.exists():
            fault(f"{args.sidecar.name}: the archive digest sidecar is missing")
        elif zip_sha:
            side = read_sidecar(args.sidecar)
            if not side["sha256"]:
                fault(f"{args.sidecar.name}: carries no sha256 line")
            elif side["sha256"] != zip_sha:
                fault(f"{args.sidecar.name}: says the archive is {side['sha256']}, "
                      f"the archive's bytes are {zip_sha}")
            if side["bytes"] is None:
                fault(f"{args.sidecar.name}: carries no byte-size line")
            elif side["bytes"] != zip_bytes:
                fault(f"{args.sidecar.name}: says {side['bytes']} bytes, the "
                      f"archive is {zip_bytes} bytes")
            for got in (side["name"], side["bytes_name"]):
                if got and got != args.zip.name:
                    fault(f"{args.sidecar.name}: names {got!r}, not "
                          f"{args.zip.name!r}")

        # -- 5c. the P8 transcript ----------------------------------------
        if not args.verify_log.exists():
            fault(f"{args.verify_log.name}: the P8 transcript is missing; "
                  f"without it nothing proves the archive was verified")
        else:
            verdict = read_verify_log(args.verify_log)
            if verdict["verdict"] != "PASS":
                fault(f"{args.verify_log.name}: P8 verification is "
                      f"{verdict['verdict'] or 'unstated'}, not PASS; if P8 "
                      f"fails the attempt remains non-authoritative")
            if verdict["rehash"] != "UNCHANGED":
                fault(f"{args.verify_log.name}: the post-P8 rehash is "
                      f"{verdict['rehash'] or 'unstated'}, not UNCHANGED")
            if zip_sha:
                if verdict["sha256"] and verdict["sha256"] != zip_sha:
                    fault(f"{args.verify_log.name}: the post-P8 rehash is "
                          f"{verdict['sha256']}, the archive's bytes are "
                          f"{zip_sha}")
                elif not verdict["sha256"]:
                    fault(f"{args.verify_log.name}: records no post-P8 rehash "
                          f"digest")
                if verdict["bytes"] is not None and verdict["bytes"] != zip_bytes:
                    fault(f"{args.verify_log.name}: the post-P8 rehash is over "
                          f"{verdict['bytes']} bytes, the archive is "
                          f"{zip_bytes} bytes")

        # -- 5d. the record itself ----------------------------------------
        if not args.authority.exists():
            fault(f"{args.authority.name}: the final-authority record is "
                  f"missing; nothing else may establish final authority")
        else:
            try:
                record = json.loads(args.authority.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                fault(f"{args.authority.name}: not readable JSON: {error}")
                record = {}
            if record and not isinstance(record, dict):
                fault(f"{args.authority.name}: is not a JSON object")
                record = {}

        try:
            args.authority.resolve().relative_to(package)
        except ValueError:
            pass
        else:
            fault(f"{args.authority.name}: lies inside the package; the "
                  f"record is written after the manifest and cannot be in it")

        if record:
            for key in sorted(AUTHORITY_SCHEMA):
                want = AUTHORITY_SCHEMA[key]
                if key not in record:
                    fault(f"{args.authority.name}: no {key!r}; the final "
                          f"authority record is incomplete")
                elif want is int and (isinstance(record[key], bool)
                                      or not isinstance(record[key], int)):
                    fault(f"{args.authority.name}: {key!r} must be an integer, "
                          f"not {type(record[key]).__name__}")
                elif want is str and not isinstance(record[key], str):
                    fault(f"{args.authority.name}: {key!r} must be a string, "
                          f"not {type(record[key]).__name__}")
            for key in sorted(set(record) - set(AUTHORITY_SCHEMA)):
                fault(f"{args.authority.name}: unknown key {key!r}")

            if str(record.get("schema", "")) != AUTHORITY_SCHEMA_ID:
                fault(f"{args.authority.name}: schema is "
                      f"{record.get('schema')!r}, not {AUTHORITY_SCHEMA_ID!r}"
                      + (". /1 bound the parent and the predecessor review "
                         "only transitively, through the archive and the "
                         "evidence commit, and carried neither the final "
                         "completeness verdict nor the outer-scan verdict"
                         if str(record.get("schema", ""))
                         == AUTHORITY_SCHEMA_ID_V1 else ""))

            # ---- /2: THE DIRECT BINDINGS ---------------------------------
            #
            # Each of these names a thing rather than a route to it. V15's
            # review found its parent and its predecessor review "bound
            # transitively through the archive and the final evidence
            # commit"; a reader had to reconstruct a chain to learn what the
            # package was a correction OF.
            if str(record.get("lane", "")) != (args.lane or
                                               str(record.get("lane", ""))):
                fault(f"{args.authority.name}: lane "
                      f"{record.get('lane')!r} is not {args.lane!r}")
            if not str(record.get("lane", "")).strip():
                fault(f"{args.authority.name}: names no lane")
            claimed_parent = str(record.get("parent", ""))
            if not HEX40.fullmatch(claimed_parent):
                fault(f"{args.authority.name}: parent {claimed_parent!r} is "
                      f"not a 40-character lowercase hex sha; the exact "
                      f"parent is bound HERE, not left to be recovered from "
                      f"the archive")
            elif args.parent and claimed_parent != args.parent:
                fault(f"{args.authority.name}: authoritative against parent "
                      f"{claimed_parent!r}, not {args.parent!r}")
            claimed_review = str(record.get("review_commit", ""))
            if not HEX40.fullmatch(claimed_review):
                fault(f"{args.authority.name}: review_commit "
                      f"{claimed_review!r} is not a 40-character lowercase "
                      f"hex sha; the review this package answers is bound "
                      f"HERE and not transitively")
            elif args.review and claimed_review != args.review:
                fault(f"{args.authority.name}: answers review "
                      f"{claimed_review!r}, not {args.review!r}")

            # THE AUTHORITATIVE ATTEMPT/LEDGER IDENTITY, BY DIGEST. V15 named
            # the ledger and never its bytes, so a reader holding two slices
            # could not tell which one the record meant.
            ledger_name = str(record.get("ledger_name", ""))
            if args.ledger and ledger_name != args.ledger.name:
                fault(f"{args.authority.name}: names ledger "
                      f"{ledger_name!r}, not {args.ledger.name!r}")
            # THE SLICE'S DIGEST IS DEFERRED, and it has to be. P9 derives the
            # slice AFTER writing this record, and P10 and P11 each append
            # their own row to it, so its bytes do not settle until the last
            # of them has run. A digest written at P9 would name a file that
            # did not exist and would be wrong about the one that eventually
            # does. It is declared in `deferred_bindings` like the two
            # verdicts and bound by `--bind-final` at P12; an empty value with
            # no declaration is still refused, so nothing is hidden by this.
            claimed_ledger_sha = str(record.get("ledger_sha256", ""))
            if not claimed_ledger_sha and "ledger_sha256" in deferred_names(record):
                pass
            elif not HEX64.fullmatch(claimed_ledger_sha):
                fault(f"{args.authority.name}: ledger_sha256 "
                      f"{claimed_ledger_sha!r} is not a 64-character "
                      f"lowercase hex digest")
            elif args.ledger and args.ledger.is_file():
                real = hashlib.sha256(args.ledger.read_bytes()).hexdigest()
                if real != claimed_ledger_sha:
                    fault(f"{args.authority.name}: ledger_sha256 says "
                          f"{claimed_ledger_sha}, and {args.ledger.name} "
                          f"hashes to {real}")

            # ---- /2: THE DEFERRED BINDINGS, WHICH MUST BE BOUND BY NOW ---
            #
            # P9 cannot fill these: the outer scan is P11 and the final
            # completeness verdict is P12, and a record written at P9 with
            # either value would carry a verdict that did not exist. They are
            # declared empty there, filled by `--bind-final` after both
            # verdicts, and REQUIRED here -- because by the time this gate
            # runs over a finished package they exist.
            deferred = record.get("deferred_bindings")
            if not isinstance(deferred, dict):
                fault(f"{args.authority.name}: deferred_bindings must be an "
                      f"object mapping an unfilled field to the reason it is "
                      f"unfilled")
                deferred = {}
            # `--bindings-pending` is for the P10 run, which happens
            # BEFORE P11 and P12 and therefore before either verdict exists.
            # It accepts a DECLARED deferral and nothing else: an empty field
            # with no entry in `deferred_bindings` is still refused, so the
            # flag cannot hide a missing binding, only an unwritten one.
            # `--bindings-pending` is for the P10 run, which happens
            # BEFORE P11 and P12 and therefore before either verdict exists.
            # It accepts a DECLARED deferral and nothing else: an empty field
            # with no entry in `deferred_bindings` is still refused, so the
            # flag cannot hide a missing binding, only an unwritten one.
            if not args.pre_p8:
                for key in DEFERRABLE:
                    value = str(record.get(key, ""))
                    if key in deferred:
                        if not args.bindings_pending:
                            fault(f"{args.authority.name}: {key!r} is still "
                                  f"deferred ({deferred[key]!r}); a finished "
                                  f"authority record binds every verdict it "
                                  f"declared it would")
                    elif not value:
                        fault(f"{args.authority.name}: {key!r} is empty and "
                              f"is not declared deferred; a binding is "
                              f"either present or explained, never absent "
                              f"and silent")
                    elif (key in BOUND_VALUES
                          and value not in BOUND_VALUES[key]):
                        # CHECKED WHETHER OR NOT THE BINDINGS ARE PENDING. A
                        # value that IS written must be a legal one; only its
                        # ABSENCE is what pending excuses.
                        fault(f"{args.authority.name}: {key} is {value!r}; "
                              f"an authoritative package's value is one of "
                              f"{', '.join(BOUND_VALUES[key])}. A record does "
                              f"not get to be authoritative with an excuse")

            # THE ONE THAT CANNOT BE BOUND, AND MUST SAY SO. Naming the
            # commit inside the record would change the bytes and therefore
            # the commit; the note is what stops the gap being silent.
            if str(record.get("evidence_commit", "")).strip():
                fault(f"{args.authority.name}: evidence_commit is "
                      f"{record.get('evidence_commit')!r}; it is always "
                      f"empty, because naming the commit that carries this "
                      f"record inside the record changes the bytes and "
                      f"therefore the commit")
            if len(str(record.get("evidence_commit_note", "")).strip()) < 40:
                fault(f"{args.authority.name}: evidence_commit_note is empty "
                      f"or too short to state why the evidence commit cannot "
                      f"be bound directly and what is bound in its place")
            if str(record.get("status", "")) != "authoritative":
                fault(f"{args.authority.name}: status is "
                      f"{record.get('status')!r}; the final-authority record "
                      f"exists only to say 'authoritative'")
            winner = canonical(str(record.get("attempt", "")))
            if not winner:
                fault(f"{args.authority.name}: names no attempt, so no "
                      f"winner identity is established")
            elif not ATTEMPT_ID.fullmatch(winner):
                fault(f"{args.authority.name}: attempt {winner!r} is not an "
                      f"attempt id")
            elif not winner.startswith("package-"):
                fault(f"{args.authority.name}: attempt {winner} is not a "
                      f"package attempt")
            if str(record.get("package", "")) != name:
                fault(f"{args.authority.name}: authoritative for package "
                      f"{record.get('package')!r}, not {name!r}")
            claimed_head = str(record.get("head", ""))
            if not HEX40.fullmatch(claimed_head):
                fault(f"{args.authority.name}: head {claimed_head!r} is not a "
                      f"40-character lowercase hex sha")
            if claimed_head != head:
                fault(f"{args.authority.name}: authoritative at head "
                      f"{claimed_head!r}, not {head!r}")
            if str(record.get("zip_name", "")) != args.zip.name:
                fault(f"{args.authority.name}: names archive "
                      f"{record.get('zip_name')!r}, not {args.zip.name!r}")
            if str(record.get("p8_log", "")) != args.verify_log.name:
                fault(f"{args.authority.name}: names P8 transcript "
                      f"{record.get('p8_log')!r}, not {args.verify_log.name!r}")
            for key in ("zip_sha256", "rehash_sha256"):
                got = str(record.get(key, ""))
                if not HEX64.fullmatch(got):
                    fault(f"{args.authority.name}: {key} {got!r} is not a "
                          f"64-character lowercase hex digest")
                elif zip_sha and got != zip_sha:
                    fault(f"{args.authority.name}: {key} is {got}, but the "
                          f"archive's own bytes hash to {zip_sha}")
            for key in ("zip_bytes", "rehash_bytes"):
                got = record.get(key)
                if isinstance(got, int) and not isinstance(got, bool) \
                        and zip_bytes is not None and got != zip_bytes:
                    fault(f"{args.authority.name}: {key} is {got}, but the "
                          f"archive is {zip_bytes} bytes")
            if str(record.get("p8_result", "")) != "PASS":
                fault(f"{args.authority.name}: p8_result is "
                      f"{record.get('p8_result')!r}; final authority is "
                      f"established only when P8 passed")
            elif verdict and verdict["verdict"] and \
                    verdict["verdict"] != record.get("p8_result"):
                fault(f"{args.authority.name}: p8_result is "
                      f"{record.get('p8_result')!r}, but "
                      f"{args.verify_log.name} records "
                      f"{verdict['verdict']!r}")
            if str(record.get("rehash_result", "")) != "UNCHANGED":
                fault(f"{args.authority.name}: rehash_result is "
                      f"{record.get('rehash_result')!r}; the post-P8 rehash "
                      f"must prove the archive did not move")
            elif verdict and verdict["rehash"] and \
                    verdict["rehash"] != record.get("rehash_result"):
                fault(f"{args.authority.name}: rehash_result is "
                      f"{record.get('rehash_result')!r}, but "
                      f"{args.verify_log.name} records {verdict['rehash']!r}")
            if not TIMESTAMP.fullmatch(str(record.get("established", ""))):
                fault(f"{args.authority.name}: established "
                      f"{record.get('established')!r} is not an ISO-8601 "
                      f"instant")
            # Written after P8, and the filesystem should agree with the
            # content-binding above.
            if args.authority.exists() and args.verify_log.exists():
                if args.authority.stat().st_mtime + 2 < \
                        args.verify_log.stat().st_mtime:
                    fault(f"{args.authority.name}: is older than "
                          f"{args.verify_log.name}; final authority may not "
                          f"predate the P8 verdict it quotes")

    # -- 6. EXACTLY ONE AUTHORITATIVE PACKAGE ATTEMPT ---------------------
    # COUNTED FROM RESOLVED STATUS, never from row presence. A predecessor
    # that was authoritative and has since been superseded resolves to
    # `superseded` and is not a second claimant; counting its history row made
    # this refuse a well-formed package for its own honest past.
    claims = sorted(set(held) | ({winner} if winner else set()))
    if args.pre_p8:
        if claims:
            fault(f"authoritative attempts before P8: {len(claims)}, must be "
                  f"0 ({', '.join(claims)})")
    elif len(claims) != 1:
        fault(f"authoritative attempts: {len(claims)}, not 1 "
              f"({', '.join(claims) or 'none'})")

    # -- 7. and it is THIS package, at THIS head, and it SEALED -----------
    if winner:
        if winner not in rows:
            fault(f"{winner}: the final-authority record names it, but the "
                  f"package ledger carries no terminal row for it")
        else:
            row = rows[winner]
            if canonical(str(row.get("package", ""))) != canonical(name):
                fault(f"{winner}: authoritative for {row.get('package')!r}, "
                      f"not {name!r}")
            if str(row.get("head", "")) != head:
                fault(f"{winner}: authoritative at head {row.get('head')!r}, "
                      f"not {head!r}")
            if not str(row.get("result", "")).startswith("sealed"):
                fault(f"{winner}: result is {row.get('result')!r}, not sealed")
            if str(row.get("reason", "")):
                fault(f"{winner}: authoritative attempts carry no discard "
                      f"reason, and this one carries {row['reason']!r}")
        said = resolved.get(winner, "")
        # `authoritative` is tolerated here ONLY so this does not double-fault
        # what rule (b) in check 4 already refuses by name.
        if said and said not in ("sealed", "authoritative"):
            fault(f"{winner}: the final-authority record names it, but the "
                  f"package ledger resolves it to {said!r}")

    # -- 8. every terminal state that is not authority says why -----------
    # V13: over STATE rows as well as terminal ones. `superseded` and
    # `set-aside` are post-terminal and ride their own row, so a check that
    # read only the terminal row could not see their reason -- and a battery
    # set aside with an empty reason is exactly the shape the review found:
    # indistinguishable from a battery whose figures were used.
    for row in ledger.get("rows", []):
        if row.get("record") not in ("attempt", "state"):
            continue
        status = str(row.get("status", ""))
        if status in REASON_REQUIRED and not str(row.get("reason", "")).strip():
            one = canonical(str(row.get("attempt", "")))
            fault(f"{one}: {status} with no reason")

    # `set-aside` says a battery ran green and its figures were then not
    # used, so it may only follow `complete`. Anything else is a different
    # fact wearing the word.
    for row in ledger.get("rows", []):
        if row.get("record") != "state":
            continue
        status = str(row.get("status", ""))
        if status not in BATTERY_EVIDENCE:
            continue
        one = canonical(str(row.get("attempt", "")))
        if str(rows.get(one, {}).get("side", "")) not in ("head", "parent"):
            continue
        was = str(rows.get(one, {}).get("status", ""))
        if was != SET_ASIDE_FROM:
            if status == "set-aside":
                fault(f"{one}: set aside from {was or 'no terminal row'!r}, "
                      f"but only a {SET_ASIDE_FROM!r} battery may be set "
                      f"aside")
            else:
                fault(f"{one}: recorded {status!r} from "
                      f"{was or 'no terminal row'!r}, but only a "
                      f"{SET_ASIDE_FROM!r} battery has measurements to "
                      f"carry; an attempt that failed or was abandoned is "
                      f"unevidenced and stays so")

    # -- 9. nothing later took the winner's authority away ----------------
    if winner:
        for row in ledger.get("rows", []):
            if canonical(str(row.get("attempt", ""))) == winner \
                    and row.get("record") == "state" \
                    and str(row.get("status", "")) in ("superseded",
                                                       "discarded"):
                fault(f"{winner}: this package's own attempt is "
                      f"{row.get('status')}")

    # -- 10. the external complete ledger resolves every attempt ----------
    if args.ledger is None:
        if not args.pre_p8:
            fault("no external attempt ledger was found beside the package; "
                  "pass --ledger. The in-package ledger is a projection of it, "
                  "not a substitute")
    elif not args.ledger.exists():
        fault(f"{args.ledger.name}: the external attempt ledger is missing")
    else:
        external, ordered, broken = read_external_ledger(args.ledger)
        for one in broken:
            fault(one)
        # Rule (a) again, in the other scope. Externally the winner MUST
        # resolve to `authoritative` -- that is where the claim belongs -- but
        # it still arrives on a post-terminal state row, never as the
        # disposition of the attempt itself.
        for row in ordered:
            if row.get("record") == "attempt" \
                    and str(row.get("status", "")) == "authoritative":
                one = canonical(str(row.get("attempt", "")))
                fault(f"{one}: {args.ledger.name} carries 'authoritative' as "
                      f"a DISPOSITION, on a record=attempt row; a terminal "
                      f"row is written before P8, so it cannot hold P8's "
                      f"verdict. The most a terminal row may say is 'sealed'")
        for one in sorted(mentioned | ({winner} if winner else set())):
            row = external.get(one)
            if row is None:
                fault(f"{one}: the package mentions it, and "
                      f"{args.ledger.name} carries no row for it")
                continue
            status = str(row.get("status", ""))
            if status not in TERMINAL_STATES:
                fault(f"{one}: {args.ledger.name} leaves it at {status!r}, "
                      f"which is not a terminal disposition")
            elif status in REASON_REQUIRED and \
                    not str(row.get("reason", "")).strip():
                fault(f"{one}: {args.ledger.name} ends it {status!r} with no "
                      f"reason; a terminal state that is not a success says "
                      f"why")
        if winner:
            status = str(external.get(winner, {}).get("status", ""))
            if status and status != "authoritative":
                fault(f"{winner}: the final-authority record names it, but "
                      f"{args.ledger.name} ends it {status!r}")

    # -- 11. the outer invocation log agrees ------------------------------
    if not args.outer.exists():
        fault(f"{args.outer.name}: the outer invocation log is missing")
    else:
        said = args.outer.read_text(encoding="utf-8", errors="replace")
        if args.pre_p8:
            scan_for_any_authority(said, args.outer.name, fault)
        elif winner:
            if winner not in canonical(said):
                fault(f"{args.outer.name}: never names the authoritative "
                      f"attempt {winner}")
            if name not in said:
                fault(f"{args.outer.name}: never names the package {name}")
            if head not in said:
                fault(f"{args.outer.name}: never names the head {head}")
            mentions = scan_prose(said, winner, args.outer.name, fault,
                                  package_name=name)
            if not mentions:
                fault(f"{args.outer.name}: never names {winner} on a line "
                      f"that claims authority")

    # -- 12. the package's own prose agrees -------------------------------
    present = [member for member in PROSE_MEMBERS
               if (package / member).is_file()]
    if args.pre_p8:
        for member in present:
            scan_for_any_authority(
                (package / member).read_text(encoding="utf-8",
                                             errors="replace"),
                member, fault)
    elif winner:
        mentions = 0
        # DECLARED foreign ids, PLUS the ones this lane's own ledger shows
        # held authority and lost it. Both are legitimate mentions; only the
        # first needs a human to say so.
        foreign = declared_attempts(package)
        if args.ledger and args.ledger.is_file():
            rows = []
            for line in args.ledger.read_text(
                    encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if isinstance(row, dict):
                    rows.append(row)
            foreign = foreign | superseded_authorities(rows)
        for member in present:
            mentions += scan_prose(
                (package / member).read_text(encoding="utf-8",
                                             errors="replace"),
                winner, member, fault, foreign=foreign)
        if not mentions:
            fault(f"no prose member names {winner} as the authoritative "
                  f"attempt; a reviewer reads these first, and they are "
                  f"silent on the one question the package must settle")

    # -- 13. nothing here, or beside here, was abandoned mid-flight -------
    marker = sorted(one.name for one in package.glob("DISCARDED*.txt"))
    marker += sorted(one.name for one in (package / "logs").glob("DISCARDED*.txt"))
    if marker:
        fault("the package carries a discard marker: " + ", ".join(marker))
    beside = sibling_markers(package, name)
    if beside:
        fault("the winner carries a sibling discard/supersession marker: "
              + ", ".join(beside))

    return problems


# ------------------------------------------------------------------- driver

def find_ledger(beside: Path, name: str) -> Path | None:
    preferred = beside / f"{name}.attempts.jsonl"
    if preferred.exists():
        return preferred
    found = sorted(beside.glob("*.jsonl"))
    if len(found) == 1:
        return found[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--package", required=True, type=Path,
                        help="the built handoff directory")
    parser.add_argument("--head", required=True,
                        help="the exact implementation head this package is for")
    # ---- /2: THE DIRECT BINDINGS THIS GATE COMPARES AGAINST --------------
    #
    # Each is OPTIONAL on the command line and REQUIRED in the record. The
    # record must carry a well-formed value either way; passing the expected
    # value here additionally proves it is the RIGHT one. V15 bound its
    # parent and its predecessor review only through the archive and the
    # evidence commit, so there was nothing for a gate to compare.
    parser.add_argument("--bindings-pending", dest="bindings_pending",
                        action="store_true",
                        help="this run happens BEFORE the outer scan and the "
                             "final completeness verdict exist, so a DECLARED "
                             "deferral of those bindings is accepted. An "
                             "undeclared empty binding is refused either way")
    parser.add_argument("--lane", default=None,
                        help="the lane identity the record must name")
    parser.add_argument("--parent", default=None,
                        help="the exact parent head the record must bind")
    parser.add_argument("--review", default=None,
                        help="the exact review commit the record must bind")
    parser.add_argument("--name", default=None,
                        help="the package basename; defaults to the "
                             "directory's own name")
    parser.add_argument("--outer", type=Path,
                        help="the outer invocation log; defaults to "
                             "<package>.assemble.log beside the package")
    parser.add_argument("--zip", dest="zip", type=Path,
                        help="the shipped archive; defaults to <package>.zip "
                             "beside the package")
    parser.add_argument("--sidecar", type=Path,
                        help="the archive digest sidecar; defaults to "
                             "<package>.zip.sha256 beside the package")
    parser.add_argument("--verify-log", dest="verify_log", type=Path,
                        help="the P8 transcript; defaults to "
                             "<package>.verify-final.log beside the package")
    parser.add_argument("--authority", type=Path,
                        help="the final-authority record; defaults to "
                             "<package>.authority.json beside the package")
    parser.add_argument("--ledger", type=Path,
                        help="the external complete append-only attempt "
                             "ledger (*.jsonl); defaults to "
                             "<package>.attempts.jsonl, or the only *.jsonl "
                             "beside the package")
    parser.add_argument("--pre-p8", dest="pre_p8", action="store_true",
                        help="the attempt has not reached P8. The post-P8 "
                             "inputs are not required, and NO record anywhere "
                             "may claim final authority; the gate asserts "
                             "exactly that")
    args = parser.parse_args()

    package = args.package.resolve()
    beside = package.parent
    name = args.name or package.name

    args.package = package
    args.name = name
    args.outer = args.outer or beside / f"{name}.assemble.log"
    args.zip = args.zip or beside / f"{name}.zip"
    args.sidecar = args.sidecar or beside / f"{name}.zip.sha256"
    args.verify_log = args.verify_log or beside / f"{name}.verify-final.log"
    args.authority = args.authority or beside / f"{name}.authority.json"
    if args.ledger is None:
        args.ledger = find_ledger(beside, name)

    print("--- authority coherence")
    print(f"    package   : {name}")
    print(f"    head      : {args.head}")
    print(f"    outer     : {args.outer.name}")
    print(f"    zip       : {args.zip.name}")
    print(f"    sidecar   : {args.sidecar.name}")
    print(f"    verify-log: {args.verify_log.name}")
    print(f"    authority : {args.authority.name}")
    print(f"    ledger    : {args.ledger.name if args.ledger else '(none found)'}")
    if args.pre_p8:
        print("    mode      : pre-P8 -- no record may claim final authority")
    try:
        problems = check(args)
    except Refusal as error:
        print(f"    REFUSED : {error}")
        print("authority coherence: FAIL (1 problem)")
        return 1

    for one in problems:
        print(f"    problem : {one}")
    if problems:
        print(f"authority coherence: FAIL ({len(problems)} problem(s))")
        return 1
    if args.pre_p8:
        print("    result  : no attempt claims final authority, and P8 has "
              "not run")
    else:
        print("    result  : one authoritative attempt, established after P8, "
              "bound to the archive's own bytes, and every record names it")
    print("authority coherence: PASS (0 problems)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
