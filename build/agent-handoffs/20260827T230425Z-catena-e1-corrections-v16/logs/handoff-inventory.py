#!/usr/bin/env python3
"""Refuse a handoff whose `HANDOFF.md` cannot be reconciled with its package.

THE DEFECT THIS ANSWERS. An independent review of the V10 package found that
`HANDOFF.md` carried "eight of ten required contents". The two it did not
carry were #8 known limitations and #9 unresolved decisions, and the reason
they were missing is worth stating precisely: they were not absent. A section
existed. It read, in full,

    `LIMITATIONS.md` in full; `REVIEW_REQUEST.md` carries every question that
    needs external judgment; `UNRESOLVED-BLOCKERS.md` lists every finding left
    open with its owner.

Three filenames and three verbs. No limitation is stated; no decision is left
open on the page a reviewer is told is "the factual entry point".

THE SECOND DEFECT, AND WHY THIS TOOL WAS REWRITTEN. The V12 package scored
`10/10` and `problems: 0` under the previous version of this tool, and an
independent review then returned CHANGES REQUIRED against it for four
SUBSTANTIVE failures the tool was structurally incapable of seeing:

    `HANDOFF.md` says eleven limitations while twelve exist; the closure
    record says the parent fails ten ways across nine methods while derived
    claims say twelve across eleven; the artifact inventory omits the tracked
    `.handoff-inventory.log`; and `checks.txt` claims every command while
    expressly omitting seal, sanitize, derive, and audit commands.

Every one of those is a LEXICALLY PERFECT document disagreeing with the bytes
beside it. The old tool computed all ten verdicts from `HANDOFF.md`'s text
alone: it imported neither `hashlib` nor `subprocess`, never opened
`claims.json`, never counted anything, and -- the structural blindness that
produced the third finding -- never discovered a sibling artifact, so a
sibling nobody passed on the command line could not be missed. Its own output
log was exactly such a sibling.

WHAT THIS TOOL NOW DECIDES. Two layers, and the second is the new one.

  LEXICAL. Each of the ten required contents is reported PRESENT, LINK-ONLY,
  INCOMPLETE or ABSENT. LINK-ONLY is a HEURISTIC -- see the LINK-ONLY RULE
  block below.

  SUBSTANTIVE. FOURTEEN mechanical reconciliations against the package's real
  bytes, each of which can fail while every lexical verdict passes:

    1. REFERENCED FILES. Every package-relative path `HANDOFF.md` names must
       resolve to a real file. (`referenced_file_rows`)
    2. COUNTS. Every count claim adjacent to a countable noun -- or anchored
       on a countable file -- is resolved against ground truth recomputed
       from the package. (`count_claim_rows`)
    3. SIBLINGS. The artifacts beside the package are DISCOVERED, not
       declared; `--sibling` is now an additional assertion rather than the
       only source of truth. This tool's own output log is always required to
       be named. (`sibling_names`)
    4. HASHES AND IDENTITY. Every SHA-256 quoted beside a filename is
       recomputed with `hashlib` and compared; head, parent and branch are
       compared against `claims.json`, or against `git` via `subprocess` when
       `claims.json` is absent. A claim that could not be checked is reported
       UNCHECKED rather than passed. (`hash_rows`, `identity_rows`)
    5. STALE COUNTS. A count that misses this package's ground truth is
       re-resolved against every sibling package directory, so a figure
       carried over from a previous package is named as such.
    6. THE ARTIFACT CROSS-CHECK IS BIDIRECTIONAL -- every real artifact must
       be named, and every named package-relative entry must exist -- AND IT
       FEEDS CONTENT #10's VERDICT, which is what the module docstring always
       claimed and the dispatch never did.
    7. DERIVED FIGURES. Figures the package derives into `claims.json` are
       compared against the prose that repeats them, across every root
       document, because `HANDOFF.md` asserts that every figure in the
       package is repeated from there.
    8. COMMAND COVERAGE. When `checks.txt` claims to record every command,
       every command transcript under `logs/attempt-*/` must have a row.
    9a. EMPTY COMMAND SLOTS. A `command :` slot with no invocation string.
        (`command_rows`)
    9b. ELIDED ROWS. A row the package's own label says is not the string a
        shell was handed. (`elided_rows`)
    9c. NON-EXECUTABLE ROWS, RE-DERIVED. V15 read the shipped `recorded:`
        label and believed it, which is why seven rows labelled
        "the exact string handed to the shell; re-runnable" passed a checker
        whose whole job is to disbelieve the documents. Every row's verdict
        is now RECOMPUTED here from `commands.json`'s exec record through
        `catena_command`, and a shipped label that disagrees with the
        re-derivation is itself a finding. (`prose_rows`, `rederived_rows`)
    9d. EXECUTION CONTRADICTIONS. A tool the execution record calls
        never-executed, beside a recorded command that runs it.
        (`unrun_rows`)
    9e. SET-ASIDE COHORTS. A commit described as a cohort that ran and was
        set aside, with no row in the shipped history. (`cohort_rows`)
    9f. SELF-CONTRADICTING COMPLETENESS. A completeness claim in one member
        contradicted by a disclosure in another. (`claim_rows`)

  V16 ADDS, and the docstring above is counted rather than remembered -- V15
  shipped this block saying "Eight" while the V15 delta had already added the
  six 9a-9f families beneath it:

    10. DIVERGENCE ACCOUNTING. A durable example-divergence figure that is
        not the authoritative log's `diverged` field, and in particular one
        that equals `diverged` plus a disjoint counter. (`divergence_rows`)
    11. FINAL-STATE COMPLETENESS. The verdict is taken at the true final
        state: every authoritative log beside the package, the outer
        sanitize and the outer scan included, must be named.
        (`final_state_rows`)
    12. THE SHIPPED/LOCAL-ONLY BOUNDARY. A claim whose only support is an
        artifact that is not in the package and not independently reachable.
        (`boundary_rows`)

EXIT CODES. 0 complete; 1 problems found; 2 the tool could not run. The third
used to be indistinguishable from the second.

Read-only. Standard library only. No network. Nothing is written except an
explicit `--json` path, which must lie outside the inspected package; the
JSON is written on the error path too.

Usage:
    handoff-inventory.py --package DIR [--sibling NAME ...] [--json OUT]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

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

# THE STATE MODEL IS IMPORTED, NOT RESTATED. `checks.py` owns the two axes --
# how an attempt terminated, and whether a completed attempt's measurements
# remain authoritative -- and a second copy here is a second thing to drift.
# The fallback exists only for a package whose `logs/` this file was lifted
# out of; it is the same set, and it is the only place it is written twice.
try:
    import checks as CHECKS  # noqa: E402

    NEVER_EVIDENCE = CHECKS.NEVER_EVIDENCE
except Exception:  # pragma: no cover - only when checks.py is not beside us
    NEVER_EVIDENCE = frozenset({"failed", "abandoned", "discarded"})

# ---------------------------------------------------------------------------
# THE LINK-ONLY RULE, AND ITS THRESHOLDS
#
# A section is LINK-ONLY when it names files instead of saying anything. The
# rule has two halves, and the second is the one that catches V10.
#
#   1. STRIP THE REFERENCES. From each sentence remove markdown links, inline
#      code spans that look like a path or filename, bare filename tokens
#      (`LIMITATIONS.md`, `logs/seal.log`) and section anchors (`§3`). What
#      is left is the RESIDUAL -- the prose that stands without the pointer.
#
#   2. ASK WHETHER ANY SENTENCE STANDS ALONE. A sentence is SUBSTANTIVE when
#      its residual is at least MIN_SENTENCE_RESIDUAL characters AND, if the
#      sentence contained a reference at all, the residual does not OPEN with
#      a delegating predicate (`lists`, `states`, `carries`, `in full`,
#      `see`, `describes`, ...). That opener test is the whole trick: a
#      sentence shaped `FILE <delegating verb> <the thing>` asserts nothing
#      about the thing, it asserts where the thing is written down.
#
# A section is PRESENT when it has at least one substantive sentence and its
# total residual reaches MIN_SECTION_RESIDUAL. It is LINK-ONLY when it has no
# substantive sentence but does contain at least one reference. It is ABSENT
# when no section of the document is about that required content at all.
#
# WHAT IT CANNOT CATCH, and why the substantive layer below exists: prose
# that is substantive in shape and false in content. "Eleven limitations"
# reads exactly like "twelve limitations". No lexical rule separates them;
# only counting the sections of `LIMITATIONS.md` does.
# ---------------------------------------------------------------------------

MIN_SENTENCE_RESIDUAL = 25
MIN_SECTION_RESIDUAL = 80

FILE_SUFFIXES = (
    # `jsonl` before `json`, and both before the rest: the alternation is
    # ordered, so a shorter prefix listed first would match `.json` inside
    # `.jsonl` and leave a stray `l`. V13: the append-only attempt ledger
    # ships as `<package>.attempts.jsonl`, and with no `jsonl` here the tool
    # could not SEE a document naming it — the artifact cross-check reported
    # the sibling unnamed while the bullet naming it sat in the file. A
    # checker that cannot see a suffix reports its absence, which is the
    # class of blindness this tool exists to end.
    "jsonl|md|txt|json|patch|py|sh|log|zip|sha256|png|jpg|jpeg|svg|gif|js"
    "|mjs|css|html|toml|yml|yaml|ini|cfg|lock|diff"
)

# The suffixes a BARE filename must carry before this tool will insist it be
# a member of the package. A bare `catena-model.js` is a repository path
# quoted in prose; a bare `LIMITATIONS.md` is a claim about this package.
PACKAGE_DOC_SUFFIXES = ("md", "txt", "json", "patch", "sha256", "log", "zip")

# A reference: a markdown link, a code span that reads as a path or filename,
# a bare filename, a bare directory-ish path, or a section anchor.
REFERENCE_RE = re.compile(
    r"(?P<link>\[[^\]\n]*\]\([^)\n]*\))"
    r"|(?P<code>`[^`\n]+`)"
    r"|(?P<bare>(?<![\w/.\-])[\w][\w.+\-]*\.(?:" + FILE_SUFFIXES + r")\b)"
    r"|(?P<dir>(?<![\w/.\-:])[\w][\w.+\-]*/[\w./+\-]*)"
    r"|(?P<anchor>§\s*[\w.\-]+)"
)

# A code span counts as a REFERENCE only when its content reads as a path or a
# filename. `make public-site` is a command, not a pointer.
FILEISH_RE = re.compile(
    r"^[\w][\w.+\-]*(?:/[\w.+\-]*)*(?:\.(?:" + FILE_SUFFIXES + r")|/)$"
)

# Sentence boundaries. Hard-wrapped prose puts the newline inside the
# whitespace run, so `\s+` covers it; a blank line ends a sentence outright.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.;!?])\s+|\n\s*\n")

# The delegating predicates of the LINK-ONLY rule.
DELEGATING_OPENER_RE = re.compile(
    r"^(?:and\s+|also\s+|plus\s+|then\s+)?"
    r"(?:in\s+full|in\s+detail|in\s+its\s+entirety|as\s+recorded|as\s+listed"
    r"|see|per|refer\s+to|listed\s+in|recorded\s+in|stated\s+in"
    r"|lists?|states?|carr(?:y|ies)|records?|describ(?:e|es)|names?"
    r"|documents?|enumerates?|contains?|covers?|explains?|holds?|gives?"
    r"|sets?\s+out|details?|answers?|addresses?|tracks?|captures?|collects?"
    r"|reports?|summari[sz]es?|has|have|is\s+the|are\s+the|is\s+a|are\s+a)\b",
    re.IGNORECASE,
)

# A reference in the artifact inventory counts as an INVENTORY ENTRY only when
# it is not in a CITATION position.
CITATION_CUES = {
    "in", "into", "see", "per", "from", "at", "by", "within", "under",
    "named", "describes", "described", "listed", "referenced", "via",
    "inside", "through", "against", "beside", "throughout", "reference",
    "referenced-in", "according",
}

WORD_TRIM = "`*_\"'([{)]}.,;:!?—–-§"

# ---------------------------------------------------------------------------
# HEX TOKENS.
#
# The old `\b[0-9a-f]{7,40}\b` matched ordinary English: `defaced`, `deface`,
# `facade`, `added`, `beefed`. Two tightenings: a hex token must be at least
# eight characters, and it must contain at least one DIGIT, which no English
# word can. `deadbeef` is rejected; `d312786` is too short to be a claim and
# `d312786dd2b23926aa88e29ea15647dfcc7e7e6e` is not.
# ---------------------------------------------------------------------------

HEX_TOKEN_SRC = (r"(?<![0-9a-zA-Z_])(?![a-f]+(?![0-9a-zA-Z_]))"
                 r"[0-9a-f]{8,40}(?![0-9a-zA-Z_])")
HEX_TOKEN_RE = re.compile(HEX_TOKEN_SRC)
SHA256_RE = re.compile(r"(?<![0-9a-zA-Z_])(?![a-f]+(?![0-9a-zA-Z_]))"
                       r"[0-9a-f]{64}(?![0-9a-zA-Z_])")
FULL_SHA_RE = re.compile(r"(?<![0-9a-zA-Z_])[0-9a-f]{40}(?![0-9a-zA-Z_])")

# ---------------------------------------------------------------------------
# THE TEN REQUIRED CONTENTS. The wording is the protocol's own.
#
#   kind "fact"        evidence is a pattern over the LOCATED SECTION's title
#                      and body -- not, as before, over the whole document,
#                      which let a SHA quoted in §3 satisfy §2.
#   kind "enumeration" evidence is that the located section names things.
#   kind "prose"       evidence is the LINK-ONLY rule above.
#   kind "inventory"   as "enumeration", AND the bidirectional cross-check
#                      against the package's real members and siblings. The
#                      cross-check now DECIDES the verdict; it used to be
#                      printed beside a verdict it could not influence.
# ---------------------------------------------------------------------------

CONTENTS: list[dict] = [
    {
        "n": 1,
        "text": "task and intended outcome",
        "kind": "prose",
        "cues": [r"\btask\b", r"\bintended outcome\b", r"\boutcome\b",
                 r"\bgoal\b", r"\bpurpose\b", r"\bwhat this (?:is|lane)\b"],
    },
    {
        "n": 2,
        "text": "current branch, or `detached HEAD` when applicable",
        "kind": "fact",
        "cues": [r"\bbranch\b", r"\bidentity\b", r"\bstate\b"],
        # An AFFIRMATIVE detached-HEAD statement, a `branch: NAME` binding,
        # or a ref-shaped code span. "Not a detached HEAD" no longer counts
        # as a statement that the state IS a detached HEAD.
        "patterns": [r"(?i)(?:^|\b(?:is|on|at|a|currently)\s+)detached\s+HEAD",
                     r"(?i)\bbranch\b\s*[:=]\s*\S",
                     r"(?i)\bbranch\b[^\n]{0,40}`[^`\n]+`",
                     r"(?i)\bon\s+branch\b\s+\S",
                     r"`[\w][\w.+\-]*/[\w.+\-/]+`"],
    },
    {
        "n": 3,
        "text": "current commit SHA and the task's base commit when known",
        "kind": "fact",
        "cues": [r"\bidentity\b", r"\bcommit\b", r"\bhead\b", r"\bbase\b"],
        # A SHA, a word that makes it the reviewed head, and the base clause.
        # The base clause now requires the base word to sit BESIDE a SHA (or
        # to be an explicit statement that there is none); the bare word
        # "parent" anywhere in the document used to be enough.
        "all_patterns": [
            HEX_TOKEN_SRC,
            r"(?i)\b(?:head|current commit|commit sha|reviewed commit)\b",
            r"(?i)(?:\b(?:base|parent|merge[- ]base)\b[^\n]{0,120}?"
            + HEX_TOKEN_SRC
            + r"|" + HEX_TOKEN_SRC + r"[^\n]{0,120}?"
            r"\b(?:base|parent|merge[- ]base)\b"
            r"|\bno known (?:base|parent)\b|\bbase (?:commit )?is unknown\b)",
        ],
    },
    {
        "n": 4,
        "text": "whether the reviewed state includes uncommitted changes",
        "kind": "fact",
        "cues": [r"\buncommitted\b", r"\bworking tree\b", r"\bidentity\b",
                 r"\bstate\b"],
        "patterns": [r"(?i)\buncommitted\b",
                     r"(?i)working tree\s+(?:\w+\s+){0,2}clean",
                     r"(?i)worktree_clean",
                     r"(?i)porcelain\s*=\s*clean",
                     r"(?i)\bno local modifications\b",
                     r"(?i)\bclean worktree\b"],
    },
    {
        "n": 5,
        "text": "focused files changed",
        "kind": "enumeration",
        "cues": [r"\bfocused files\b", r"\bfiles changed\b",
                 r"\bchanged files\b", r"\bfocused (?:diff|paths)\b",
                 r"\bwhat changed\b"],
    },
    {
        "n": 6,
        "text": ("preview URLs or exact startup commands, including required "
                 "route state"),
        "kind": "fact",
        "cues": [r"\bstartup\b", r"\bpreview\b", r"\broute\b",
                 r"\brun\b", r"\bhow to (?:verify|reproduce|run)\b",
                 r"\breproduc"],
        "all_patterns": [
            r"(?i)(?:https?://\S+"
            r"|`[^`\n]*(?:make |python3? |npm |pnpm |yarn |node |\./|bash |sh )"
            r"[^`\n]*`)",
            r"(?i)(?:`[^`\n]*[/#?][^`\n]*`|\broute state\b|\broute\b)",
        ],
    },
    {
        "n": 7,
        "text": "implementation summary",
        "kind": "prose",
        "cues": [r"\bimplementation\b", r"\bwhat was done\b",
                 r"\bwhat was wrong\b", r"\bsummary\b", r"\bapproach\b",
                 r"\bchanges made\b", r"\bwhat changed\b"],
    },
    {
        "n": 8,
        "text": "known limitations",
        "kind": "prose",
        "cues": [r"\blimitation", r"\bknown limits\b", r"\bcaveat",
                 r"\bdoes not prove\b", r"\bnot proven\b"],
    },
    {
        "n": 9,
        "text": "unresolved decisions",
        "kind": "prose",
        "cues": [r"\bunresolved\b", r"\bopen (?:decision|question|issue)",
                 r"\bdecisions?\b", r"\bopen blockers?\b"],
    },
    {
        "n": 10,
        "text": ("artifact inventory, including why any conditional artifact "
                 "class was omitted"),
        "kind": "inventory",
        "cues": [r"\bartifact inventory\b", r"\binventory\b",
                 r"\bartifacts?\b", r"\bcontents of this package\b"],
    },
]

CORE_FILES = ["HANDOFF.md", "REVIEW_REQUEST.md", "changes.patch", "checks.txt"]

CONDITIONAL_CLASSES = [
    {"name": "screenshots/", "member": "screenshots", "is_dir": True,
     "keyword": r"(?i)screenshots?"},
    {"name": "logs/", "member": "logs", "is_dir": True,
     "keyword": r"(?i)\blogs?\b"},
    {"name": "sources.md", "member": "sources.md", "is_dir": False,
     "keyword": r"(?i)\bsources?\b"},
]

FAIL_PREFIX = "HANDOFF INVENTORY FAILED"
SETUP_PREFIX = "HANDOFF INVENTORY COULD NOT RUN"

# The suffix of this tool's own transcript. A package is assembled by
# redirecting this tool's output into `<package>.handoff-inventory.log`
# beside the package, so the inventory must name it -- and the V12 package
# did not, because nothing looked. It is required whether or not it exists on
# disk at the moment of the check, since the check may be the run that writes
# it.
SELF_LOG_SUFFIX = ".handoff-inventory.log"


class SetupFailure(Exception):
    """The tool cannot run at all. Exit 2, never 1."""


# ---------------------------------------------------------------------------
# Document structure
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
LEAD_IN_RE = re.compile(r"^\s*\*\*(.+?)\*\*\s*[:—–-]?\s*(.*)$")


class Section:
    def __init__(self, title: str, level: int) -> None:
        self.title = title
        self.level = level
        self.lines: list[str] = []

    @property
    def body(self) -> str:
        return "\n".join(self.lines).strip()


def parse_sections(text: str) -> list[Section]:
    """Split a document into heading sections and bold lead-in paragraphs."""
    sections: list[Section] = []
    stack: list[Section] = []
    for raw in text.splitlines():
        heading = HEADING_RE.match(raw)
        if heading:
            level = len(heading.group(1))
            while stack and stack[-1].level >= level:
                stack.pop()
            section = Section(heading.group(2), level)
            sections.append(section)
            for parent in stack:
                parent.lines.append(raw)
            stack.append(section)
            continue
        for parent in stack:
            parent.lines.append(raw)
        lead = LEAD_IN_RE.match(raw)
        if lead and lead.group(1).strip():
            section = Section(lead.group(1).strip(), 99)
            section.lines.append(lead.group(2))
            sections.append(section)
    return sections


def chunks_by_heading(text: str) -> list[tuple[str, str]]:
    """(heading, body) for each heading, bodies NOT nested.

    `parse_sections` gives a parent every child's lines, which is right for
    the LINK-ONLY rule and wrong for counting: a sentence under `## 8` would
    be scanned once for `## 8` and again for any ancestor. These chunks
    partition the document instead, so every sentence is scanned once and
    carries exactly one heading for the problem message.
    """
    out: list[tuple[str, str]] = []
    title = ""
    buf: list[str] = []
    for raw in text.splitlines():
        heading = HEADING_RE.match(raw)
        if heading:
            out.append((title, "\n".join(buf)))
            title, buf = heading.group(2), []
        else:
            buf.append(raw)
    out.append((title, "\n".join(buf)))
    return out


def locate(section_list: list[Section], cues: list[str]) -> list[Section]:
    compiled = [re.compile(one, re.IGNORECASE) for one in cues]
    return [one for one in section_list
            if any(rx.search(one.title) for rx in compiled)]


# ---------------------------------------------------------------------------
# References and residual prose
# ---------------------------------------------------------------------------

def reference_spans(text: str) -> list[tuple[int, int, list[str]]]:
    """Every reference in `text` as (start, end, candidate names)."""
    found: list[tuple[int, int, list[str]]] = []
    for match in REFERENCE_RE.finditer(text):
        kind = match.lastgroup
        raw = match.group(0)
        names: list[str] = []
        if kind == "code":
            inner = raw.strip("`").strip()
            if not FILEISH_RE.match(inner):
                continue
            names = [inner]
        elif kind == "link":
            label = re.sub(r"^\[|\]$", "", raw.split("](")[0]).strip("`").strip()
            target = raw.split("](", 1)[1].rstrip(")").strip()
            names = [one for one in (label, target) if one]
        elif kind == "anchor":
            names = []
        else:
            names = [raw]
        found.append((match.start(), match.end(), names))
    return found


def residual_of(text: str) -> str:
    """`text` with every reference removed and whitespace collapsed."""
    spans = reference_spans(text)
    out: list[str] = []
    cursor = 0
    for start, end, _ in spans:
        if start < cursor:
            continue
        out.append(text[cursor:start])
        cursor = end
    out.append(text[cursor:])
    return re.sub(r"\s+", " ", "".join(out)).strip()


def trim_lead(residual: str) -> str:
    return residual.lstrip(" \t*_-—–:;,.()[]·•")


def sentences_of(body: str) -> list[str]:
    return [one.strip() for one in SENTENCE_SPLIT_RE.split(body) if one.strip()]


def substantive_sentences(body: str) -> list[str]:
    keep: list[str] = []
    for sentence in sentences_of(body):
        had_reference = bool(reference_spans(sentence))
        residual = trim_lead(residual_of(sentence))
        if len(residual) < MIN_SENTENCE_RESIDUAL:
            continue
        if had_reference and DELEGATING_OPENER_RE.match(residual):
            continue
        keep.append(sentence)
    return keep


# ---------------------------------------------------------------------------
# GROUND TRUTH. Every quantity this tool can resolve a count claim against,
# recomputed from the package's bytes on every run. A quantity whose source
# artifact is absent resolves to None, and a claim against it is reported
# UNCHECKED rather than passed.
# ---------------------------------------------------------------------------

IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")
TOOL_SUFFIXES = (".py", ".sh", ".mjs")


# ---- V16: the tables the four new check families read ----------------------

#: The producer's summary line, field by field. Derived from
#: `scripts/replay_examples.py`'s `report()`, which prints these seven
#: integers and no others, in this order.
REPLAY_SUMMARY = re.compile(
    r"^replay-examples: (?P<captured>\d+) captured example\(s\); "
    r"(?P<replayed>\d+) replayed, (?P<diverged>\d+) diverged, "
    r"(?P<stale>\d+) known stale, (?P<never>\d+) never run, "
    r"(?P<unrunnable>\d+) unrunnable here, "
    r"(?P<volatile>\d+) volatile line\(s\) declared\s*$",
    re.M)

#: A durable sentence that states an example-divergence figure. Deliberately
#: narrow: it wants a number adjacent to the words this lane argues about, so
#: a gzip headroom of 28 bytes elsewhere in the same document is not a claim
#: about examples. Both orders occur in the V15 records --
#: "30 example divergences" and "with 30 example divergences at both".
DIVERGENCE_CLAIM = re.compile(
    r"(\d+)\s+(?:example\s+)?diverg(?:ence|ing|ent)\w*"
    r"|diverg\w*\s+examples?\D{0,20}?(\d+)",
    re.I)

#: The outer transcripts that are written AFTER the completeness verdict was
#: historically taken. V15 shipped both unnamed and its COMPLETE went stale.
FINAL_STATE_SIBLING = re.compile(
    r"\.(?:outer-sanitize|outer-scan|handoff-inventory)\.log$")

#: An artifact a document names that is not a package member and not a
#: sibling: a retired ledger, a discard marker, a raw retained transcript.
LOCAL_ONLY_REFERENCE = re.compile(
    r"\b([A-Za-z0-9][\w.-]*"
    r"(?:-retired\.jsonl|\.retired\.jsonl|DISCARDED[\w.-]*\.txt"
    r"|SUPERSEDED[\w.-]*\.txt))\b")

#: The disclosure that makes a local-only reference honest. Any one of these
#: phrases, in the same paragraph, says the reviewer cannot open it.
LOCAL_ONLY_DISCLOSURE = re.compile(
    r"local[- ]only|not shipped|outside (?:this|the) (?:package|archive)"
    r"|retained locally|this package does not ship"
    r"|a reviewer cannot open|digest[- ]only",
    re.I)


def divergence_claims(body: str) -> list[tuple[int, str]]:
    """Every stated example-divergence figure in a durable member."""
    found: list[tuple[int, str]] = []
    for match in DIVERGENCE_CLAIM.finditer(body):
        token = match.group(1) or match.group(2)
        if not token:
            continue
        start = body.rfind("\n", 0, match.start()) + 1
        end = body.find("\n", match.end())
        found.append((int(token), body[start:end if end != -1 else len(body)]))
    return found


#: A `DIFF` detail row in `check-examples` output. The producer prints one per
#: divergent CAPTURE, and two captures can carry the same command string --
#: which is the row-vs-name distinction this whole lane keeps finding.
DIFF_ROW = re.compile(r"(?m)^  DIFF    (.*?)\s*$")

#: THE UNSOUND DECOMPOSITION, AS A SHAPE RATHER THAN AS A NUMBER.
#:
#: V16, correcting the V15 review itself: the review said "the authoritative
#: logs report 28 divergent examples plus 2 separately declared volatile
#: lines, not the durable producer claim of 30 divergences", which reads as
#: 30 = 28 + 2. That decomposition is arithmetically impossible.
#: `volatile` is a STATIC constant -- `sum(len(lines) for lines in
#: VOLATILE.values())` over a module-level table naming two `tools/pdf-review`
#: commands with one declared line each -- and those two captures are MASKED
#: BEFORE comparison, so they were never in the divergent set and cannot be
#: subtracted from it. The figure is 2 at every head in every run.
#:
#: The real cause of 30-versus-28 is build state, not arithmetic: 30 on a
#: cold `build/`, 28 on a warm one, and the whole delta is two captures of
#: `tools/mass-ordinary check --out build/example-ordinary`, which diverges
#: on a cold tree and matches once a later capture in the same target has
#: written the directory it is compared against.
#:
#: So what is refused is the SHAPE. Any sentence that presents the volatile
#: count as a component of the divergence count is wrong whatever numbers it
#: carries, and this pattern is about the claim rather than about 30.
#: The joining words that make one figure a COMPONENT of another. `+` is
#: matched as a bare character, not as a word: `\b\+\b` never matches, which
#: is how the reverse spelling escaped an earlier draft of this pattern.
#: The joining words that make one figure a COMPONENT of another. `and` is
#: DELIBERATELY NOT among them: "28 divergent rows, and separately 2 volatile
#: lines, which are not divergences" is the honest sentence this check exists
#: to leave alone, and it contains `and`. `+` is matched as a bare character,
#: not as a word -- `\b\+\b` never matches, which is how the reverse spelling
#: escaped an earlier draft of this pattern.
_JOINER = (r"(?:\bplus\b|\+|\bcomprising\b|\bmade up of\b|"
           r"\bof which\b|\bconsisting of\b)")
#: The summing tail: `... and 2 volatile lines, comprising 30 in total`.
_TOTAL = r"(?:\bcomprising\b|\bin total\b|\btotalling\b|\bfor a total\b)"
DECOMPOSITION_CLAIM = re.compile(
    r"diverg\w*[^.\n]{0,140}?" + _JOINER + r"[^.\n]{0,80}?volatile"
    r"|volatile[^.\n]{0,80}?" + _JOINER + r"[^.\n]{0,140}?diverg\w*"
    r"|diverg\w*[^.\n]{0,140}?volatile[^.\n]{0,60}?" + _TOTAL,
    re.I)
#: THE ONE SOUND SUM, WHICH THIS CHECK MUST NOT REFUSE.
#:
#: `total_differing_rows` is a SEPARATELY NAMED quantity and it is DEFINED as
#: divergent rows plus volatile rows. Saying so is not the unsound claim; the
#: unsound claim is presenting that sum as a count of DIVERGENCES, which is
#: what conflates a run outcome with a static declaration and is what the V15
#: review did. A sentence that names the total by its own name has already
#: made the distinction this check exists to enforce, and refusing it would
#: leave no way to state a figure the protocol itself defines.
SOUND_TOTAL = re.compile(r"total[_ ]differing[_ ]rows", re.I)


def divergence_figures(body: str) -> dict | None:
    """Every example figure one authoritative transcript supports.

    THREE FIGURES, THREE NAMES, DERIVED SEPARATELY -- the same discipline
    `compare-gate.py` needed one artifact over.

      rows      divergent CAPTURES: the producer's `diverged` field, and the
                `DIFF` detail rows, which must agree
      commands  DISTINCT COMMAND STRINGS among those rows. Two captures of
                one command are two rows and one name, and a durable figure
                quoting either is quoting something real
      volatile  DECLARED LINES in the producer's static table. Never an
                example count and never an addend
    """
    match = REPLAY_SUMMARY.search(body)
    if not match:
        return None
    fields = {k: int(v) for k, v in match.groupdict().items()}
    detail = DIFF_ROW.findall(body)
    fields["line"] = body[:match.start()].count("\n") + 1
    fields["diff_rows"] = len(detail)
    fields["diff_commands"] = len({one.strip() for one in detail})
    fields["has_detail"] = bool(detail)
    return fields


def refuse_unsupported_divergence(fields: dict, claimed: int) -> str | None:
    """Refuse a durable figure the transcript does not support.

    SUPPORTED MEANS ONE OF THE TWO REAL FIGURES. A record may quote the row
    count or the distinct-command count -- both are true of the same run and
    they differ -- and it may quote neither anything else.

    IT DOES NOT ASSERT A CONFLATION. The 30-versus-28 gap is build state: a
    cold `build/` yields 30 rows and a warm one 28, and both are honest
    reports of the run that produced them. What this says is that THIS
    package's own transcript does not support THIS package's own figure, and
    it names the precondition that explains it.
    """
    supported = {fields["diverged"], fields["diff_rows"],
                 fields["diff_commands"]} - {0}
    if claimed in supported:
        return None
    if claimed == fields["diverged"] + fields["volatile"]:
        return (f"{claimed} is neither the divergent-row count "
                f"({fields['diverged']}) nor the distinct-command count "
                f"({fields['diff_commands']}) of the transcript this package "
                f"ships. It is also NOT diverged + volatile, whatever it "
                f"looks like: `volatile` counts DECLARED LINES in a static "
                f"table and those captures are masked before comparison, so "
                f"they were never in the divergent set. The likely cause is "
                f"build state -- `check-examples` reports more divergent rows "
                f"on a cold build/ than on a warm one -- so state which run "
                f"the figure is from, and ship that run's transcript")
    return (f"{claimed} is supported by no figure in the transcript this "
            f"package ships: it reports {fields['diverged']} divergent row(s) "
            f"over {fields['diff_commands']} distinct command(s)"
            + (" (no DIFF detail rows are present, so the summary line is the "
               "only source)" if not fields["has_detail"] else "")
            + ". The figure is build-state sensitive -- a cold build/ yields "
              "more divergent rows than a warm one -- so a durable claim "
              "names the run it came from and ships that run's transcript")


def _files_under(root: Path) -> list[Path]:
    out: list[Path] = []
    if not root.is_dir():
        return out
    for base, _dirs, names in os.walk(root):
        for name in names:
            out.append(Path(base) / name)
    return out


def _read(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def checks_steps(body: str) -> list[tuple[str, dict]]:
    """`checks.txt`, as its `--- <slug>` blocks and their `name : value` slots.

    The file is a flat run of blocks, each opened by a `--- <slug>` line and
    filled with indented slots -- `command`, `recorded`, `exit`, `log`. Read
    as blocks rather than as loose lines, a slot can be reported WITH the
    step and the transcript it belongs to, which matters when two steps share
    a slug: the parent and head browser gates are both `browser-gate`, and a
    finding that names only the slug names them both and identifies neither.

    The FIRST value wins for a repeated slot name (`result` appears once per
    headline line), because the block's identity slots appear once.
    """
    blocks: list[tuple[str, dict]] = []
    slug: str | None = None
    slots: dict = {}
    for line in body.splitlines():
        head = re.match(r"^---\s+(\S.*?)\s*$", line)
        if head:
            if slug is not None:
                blocks.append((slug, slots))
            slug, slots = head.group(1), {}
            continue
        slot = re.match(r"^\s+([A-Za-z][\w-]*)\s*:\s*(.*?)\s*$", line)
        if slot and slug is not None:
            slots.setdefault(slot.group(1), slot.group(2))
    if slug is not None:
        blocks.append((slug, slots))
    return blocks


def _heading_count(path: Path, level: str = "## ") -> int | None:
    body = _read(path)
    if body is None:
        return None
    return sum(1 for line in body.splitlines() if line.startswith(level))


class Truth:
    """The package's real quantities, computed once and reused."""

    def __init__(self, package: Path, siblings: list[str] | None = None):
        self.package = package
        self.siblings = siblings or []
        self._cache: dict[str, tuple[int | None, str]] = {}

    def get(self, name: str) -> tuple[int | None, str]:
        if name not in self._cache:
            self._cache[name] = getattr(self, "_q_" + name)()
        return self._cache[name]

    # -- membership ------------------------------------------------------

    def _q_package_members(self) -> tuple[int | None, str]:
        return (len(_files_under(self.package)),
                "files under the package, recursive")

    def _q_top_level_members(self) -> tuple[int | None, str]:
        if not self.package.is_dir():
            return None, "the package is not a directory"
        return len(os.listdir(self.package)), "entries at the package root"

    def _q_logs(self) -> tuple[int | None, str]:
        root = self.package / "logs"
        if not root.is_dir():
            return None, "the package has no logs/"
        return len(_files_under(root)), "files under logs/, recursive"

    def _q_journals(self) -> tuple[int | None, str]:
        found = [one for one in _files_under(self.package)
                 if "journal" in one.name.lower()
                 and one.suffix not in TOOL_SUFFIXES]
        return len(found), "files under the package named *journal*"

    def _q_screenshots(self) -> tuple[int | None, str]:
        root = self.package / "screenshots"
        if not root.is_dir():
            return None, "the package has no screenshots/"
        found = [one for one in _files_under(root)
                 if one.suffix.lower() in IMAGE_SUFFIXES]
        return len(found), "image files under screenshots/"

    def _q_tools(self) -> tuple[int | None, str]:
        root = self.package / "logs"
        if not root.is_dir():
            return None, "the package has no logs/"
        found = [one for one in sorted(root.iterdir())
                 if one.is_file() and one.suffix in TOOL_SUFFIXES]
        return len(found), "executable tools shipped at logs/"

    # -- the attempt ledger ----------------------------------------------

    def _ledger(self) -> dict | None:
        body = _read(self.package / "logs" / "attempts.json")
        if body is None:
            return None
        try:
            loaded = json.loads(body)
        except json.JSONDecodeError:
            return None
        return loaded if isinstance(loaded, dict) else None

    def _q_attempt_rows(self) -> tuple[int | None, str]:
        ledger = self._ledger()
        if ledger is None:
            return None, "the package has no readable logs/attempts.json"
        return len(ledger.get("rows", [])), "rows in logs/attempts.json"

    def _q_attempts(self) -> tuple[int | None, str]:
        ledger = self._ledger()
        if ledger is None:
            return None, "the package has no readable logs/attempts.json"
        seen = {row.get("attempt") for row in ledger.get("rows", [])
                if isinstance(row, dict)}
        seen.discard(None)
        return len(seen), "distinct attempts in logs/attempts.json"

    def _q_battery_rows(self) -> tuple[int | None, str]:
        ledger = self._ledger()
        if ledger is None:
            return None, "the package has no readable logs/attempts.json"
        rows = [row for row in ledger.get("rows", [])
                if isinstance(row, dict)
                and row.get("side") in ("head", "parent")]
        return len(rows), "battery rows in logs/attempts.json"

    def _q_batteries(self) -> tuple[int | None, str]:
        ledger = self._ledger()
        if ledger is None:
            return None, "the package has no readable logs/attempts.json"
        seen = {row.get("attempt") for row in ledger.get("rows", [])
                if isinstance(row, dict)
                and row.get("side") in ("head", "parent")}
        seen.discard(None)
        return len(seen), "battery attempts in logs/attempts.json"

    # -- derived records --------------------------------------------------

    def _q_manifest_rows(self) -> tuple[int | None, str]:
        body = _read(self.package / "MANIFEST.sha256")
        if body is None:
            return None, "the package has no MANIFEST.sha256"
        rows = [one for one in body.splitlines()
                if re.match(r"^[0-9a-f]{64}\s", one.strip())]
        return len(rows), "digest rows in MANIFEST.sha256"

    def _q_commits(self) -> tuple[int | None, str]:
        body = _read(self.package / "commits.txt")
        if body is None:
            return None, "the package has no commits.txt"
        rows = [one for one in body.splitlines()
                if FULL_SHA_RE.match(one.strip())]
        return len(rows), "commit rows in commits.txt"

    def _q_changed_files(self) -> tuple[int | None, str]:
        body = _read(self.package / "changed-files.txt")
        if body is None:
            return None, "the package has no changed-files.txt"
        rows = [one for one in body.splitlines()
                if re.match(r"^[MADRTCU]\d*\t\S", one)]
        return len(rows), "status rows in changed-files.txt"

    def _q_limitations(self) -> tuple[int | None, str]:
        count = _heading_count(self.package / "LIMITATIONS.md")
        if count is None:
            return None, "the package has no LIMITATIONS.md"
        return count, "`##` sections in LIMITATIONS.md"

    def _q_unresolved(self) -> tuple[int | None, str]:
        count = _heading_count(self.package / "UNRESOLVED-BLOCKERS.md")
        if count is None:
            return None, "the package has no UNRESOLVED-BLOCKERS.md"
        return count, "`##` sections in UNRESOLVED-BLOCKERS.md"

    def _q_siblings(self) -> tuple[int | None, str]:
        return len(self.siblings), "artifacts discovered beside the package"


# The countable nouns, longest first so `attempt rows` beats `attempts`. A
# `section` restriction binds the noun only inside the section located for
# that required content -- "six files" means the changed files under
# "Focused files changed" and would mean something else anywhere else.
COUNT_NOUNS: list[dict] = [
    {"noun": r"ownership journals?", "quantity": "journals"},
    {"noun": r"manifest rows?", "quantity": "manifest_rows"},
    {"noun": r"battery rows?", "quantity": "battery_rows"},
    {"noun": r"attempt rows?", "quantity": "attempt_rows"},
    {"noun": r"known limitations?", "quantity": "limitations"},
    {"noun": r"unresolved (?:decisions?|questions?|blockers?)",
     "quantity": "unresolved"},
    {"noun": r"open (?:decisions?|questions?)", "quantity": "unresolved"},
    {"noun": r"package members?", "quantity": "package_members"},
    {"noun": r"limitations?", "quantity": "limitations"},
    {"noun": r"screenshots?", "quantity": "screenshots"},
    {"noun": r"journals?", "quantity": "journals"},
    {"noun": r"batter(?:y|ies)", "quantity": "batteries"},
    {"noun": r"attempts?", "quantity": "attempts"},
    {"noun": r"log files?", "quantity": "logs"},
    {"noun": r"logs", "quantity": "logs"},
    {"noun": r"commits?", "quantity": "commits"},
    {"noun": r"siblings?", "quantity": "siblings"},
    {"noun": r"tools?", "quantity": "tools"},
    {"noun": r"members?", "quantity": "package_members"},
    {"noun": r"(?:focused |changed )?files", "quantity": "changed_files",
     "section": 5},
]

# A count anchored on a file rather than on a noun: "Stated in full in
# `LIMITATIONS.md`, eleven of them." The number's noun is a pronoun; the
# file is what makes it countable. This is the exact shape of the V12
# miscount, so it is the shape this extractor exists for.
COUNTABLE_FILES = {
    "LIMITATIONS.md": "limitations",
    "UNRESOLVED-BLOCKERS.md": "unresolved",
    "MANIFEST.sha256": "manifest_rows",
    "commits.txt": "commits",
    "changed-files.txt": "changed_files",
    "logs/attempts.json": "attempt_rows",
}

NUMBER_WORDS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
    "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
    "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}
NUMBER_RE = re.compile(
    r"(?<![\w.])(?:\d{1,6}|" + "|".join(sorted(NUMBER_WORDS, key=len,
                                               reverse=True))
    + r")(?![\w.])", re.IGNORECASE)

# A word between a number and its noun that breaks the binding. "one root per
# attempt" is not a claim that there is one attempt.
BINDING_STOPWORDS = {
    "per", "of", "in", "for", "from", "to", "with", "on", "at", "by", "and",
    "or", "than", "as", "that", "which", "into", "under", "over", "across",
    "before", "after", "beside", "within", "against",
}


# A determiner that turns a numeral into something other than a count.
# "every one of them" is not a claim that there is one of them.
NON_COUNTING = {"every", "each", "any", "no", "not", "another", "either",
                "neither"}

# The shape the file-anchored extractor accepts: "eleven of them", "twelve in
# total". Without it, "the index of every one of them, and `logs/attempts.json`
# is the attempt ledger" reads as a claim of one attempt row.
PRONOUN_COUNT_RE = re.compile(
    r"^\S+\s*(?:of\s+(?:them|these|those|which|it)\b|in\s+(?:total|all)\b"
    r"|[,.;:]|$)", re.IGNORECASE)


def preceding_word(text: str, at: int) -> str:
    head = text[:at].rstrip()
    parts = re.findall(r"[A-Za-z][\w\-]*", head)
    return parts[-1].lower() if parts else ""


def strip_emphasis(text: str) -> str:
    """`**two** commits` reads as two commits. Bold is not a word boundary."""
    return text.replace("**", "").replace("__", "")


def number_value(token: str) -> int | None:
    low = token.lower()
    if low.isdigit():
        return int(low)
    return NUMBER_WORDS.get(low)


def bind_number_to_noun(tail: str, section_n: int | None) -> dict | None:
    """The countable noun a number governs, or None.

    The window is DELIBERATELY SHORT -- three words, forty characters, and
    never across a code span. A wide window reads "the two V12 classes alone
    are `python3 -m unittest discover -s tools/tests ...`" as a claim about
    two TOOLS, because `tools/` is a word that appears later in the line.
    """
    tail = tail.split("`", 1)[0][:40]
    for index, match in enumerate(re.finditer(r"[A-Za-z][\w\-]*", tail)):
        if index >= 3:
            return None
        word = match.group(0).lower()
        for entry in COUNT_NOUNS:
            if entry.get("section") not in (None, section_n):
                continue
            if re.match(entry["noun"] + r"\b", tail[match.start():],
                        re.IGNORECASE):
                return entry
        if word in BINDING_STOPWORDS:
            return None
    return None


def count_claims(text: str, section5_titles: set[str]) -> list[dict]:
    """Every (number, quantity) claim `text` makes, with its heading."""
    claims: list[dict] = []
    for title, body in chunks_by_heading(text):
        section_n = 5 if title in section5_titles else None
        for sentence in sentences_of(strip_emphasis(body)):
            bound_here: list[dict] = []
            unbound: list[tuple[str, int, int]] = []
            for match in NUMBER_RE.finditer(sentence):
                value = number_value(match.group(0))
                if value is None:
                    continue
                if preceding_word(sentence, match.start()) in NON_COUNTING:
                    continue
                entry = bind_number_to_noun(sentence[match.end():], section_n)
                if entry is None:
                    unbound.append((match.group(0), value, match.start()))
                    continue
                bound_here.append({
                    "quantity": entry["quantity"],
                    "claimed": value,
                    "said": match.group(0),
                    "section": title or "(preamble)",
                    "sentence": " ".join(sentence.split())[:160],
                })
            claims.extend(bound_here)
            if len(unbound) == 1 and not bound_here:
                names = {name.strip().rstrip("/")
                         for _, _, group in reference_spans(sentence)
                         for name in group}
                anchors = {COUNTABLE_FILES[one] for one in names
                           if one in COUNTABLE_FILES}
                said, value, at = unbound[0]
                if len(anchors) == 1 and PRONOUN_COUNT_RE.match(sentence[at:]):
                    claims.append({
                        "quantity": anchors.pop(),
                        "claimed": value,
                        "said": said,
                        "section": title or "(preamble)",
                        "sentence": " ".join(sentence.split())[:160],
                    })
    return claims


# ---------------------------------------------------------------------------
# DERIVED FIGURES. `HANDOFF.md` opens by asserting that every figure in the
# package is derived into `claims.json` and repeated from `DERIVED-CLAIMS.md`.
# That assertion is checkable: the figure in the prose must equal the figure
# in the JSON. The V12 review's second finding -- "the closure record says the
# parent fails ten ways across nine methods while derived claims say twelve
# across eleven" -- is exactly this check, and no lexical rule reaches it,
# because the sentence is well-formed and the file it contradicts is a
# different file.
#
# Each pattern is anchored on its own verb phrase rather than on a bare noun,
# so "reachable only two ways" and "three ways into the request sink" are not
# read as failure counts.
# ---------------------------------------------------------------------------

NUM_SRC = NUMBER_RE.pattern

DERIVED_FIGURES: list[dict] = [
    {"label": "ways the parent fails",
     "regex": r"(?i)fail(?:s|ed|ing)?\s+(" + NUM_SRC + r")\s+ways?",
     "path": ["oracles", "against_parent", "identities"]},
    {"label": "methods the parent fails across",
     "regex": r"(?i)across\s+(" + NUM_SRC + r")\s+methods?",
     "path": ["oracles", "against_parent", "failing_method_count"]},
    {"label": "methods failing at the parent",
     "regex": r"(?i)(" + NUM_SRC + r")\s+methods?\s+fail",
     "path": ["oracles", "against_parent", "failing_method_count"]},
    {"label": "methods run against the parent",
     "regex": r"(?i)(" + NUM_SRC + r")\s+methods?\s+(?:were\s+)?run\b",
     "path": ["oracles", "against_parent", "methods_run"]},
    {"label": "control methods passing at the parent",
     "regex": r"(?i)(" + NUM_SRC + r")\s+(?:control\s+)?methods?\s+pass",
     "path": ["oracles", "against_parent", "passing_methods"]},
]


def dig(blob, path: list[str]):
    cursor = blob
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            return None
        cursor = cursor[key]
    return cursor


# ---------------------------------------------------------------------------
# The artifact inventory cross-check
# ---------------------------------------------------------------------------

def inventory_entries(body: str) -> set[str]:
    """Names the inventory ENUMERATES, excluding names it merely cites."""
    entries: set[str] = set()
    for start, _, names in reference_spans(body):
        prefix = body[:start].rstrip()
        prefix = prefix.rstrip("`*_\"'([{ \t")
        tail = prefix.split()[-1] if prefix.split() else ""
        word = tail.strip(WORD_TRIM).lower()
        if word in CITATION_CUES:
            continue
        for name in names:
            entries.add(name.strip().rstrip("/"))
            entries.add(name.strip())
    return entries


def named_by(entries: set[str], member: str) -> bool:
    bare = member.rstrip("/")
    if member in entries or bare in entries:
        return True
    return any(one == bare or one.startswith(bare + "/") for one in entries)


def top_level_members(package: Path) -> list[str]:
    out: list[str] = []
    for entry in sorted(os.listdir(package)):
        path = package / entry
        out.append(entry + "/" if path.is_dir() else entry)
    return out


def discover_siblings(package: Path) -> list[str]:
    """The artifacts that live BESIDE the package, found rather than declared.

    `--sibling` was the only way a sibling entered this tool's view, and it
    had no `type=Path` and was never stat'ed, so a sibling nobody passed was
    structurally invisible. That is how the V12 package omitted its own
    `.handoff-inventory.log` from the inventory while scoring 10/10.
    """
    parent = package.parent
    prefix = package.name + "."
    found: list[str] = []
    if parent.is_dir():
        for entry in sorted(os.listdir(parent)):
            if entry.startswith(prefix) and (parent / entry).is_file():
                found.append(entry)
    self_log = package.name + SELF_LOG_SUFFIX
    if self_log not in found:
        found.append(self_log)
    return sorted(found)


def sibling_packages(package: Path) -> list[Path]:
    """Other handoff packages beside this one, for the stale-count check."""
    parent = package.parent
    if not parent.is_dir():
        return []
    out: list[Path] = []
    for entry in sorted(os.listdir(parent)):
        path = parent / entry
        if path.is_dir() and path != package and (path / "HANDOFF.md").is_file():
            out.append(path)
    return out


# ---------------------------------------------------------------------------
# Path resolution: which of the names a document uses are CLAIMS ABOUT THIS
# PACKAGE, and which are repository paths quoted in prose.
#
# A name is package-relative when its first component is a real top-level
# directory of the package (`logs/...`, `screenshots/...`), or when it is a
# bare filename carrying a package-document suffix. `src/web/.../catena.js`
# and `guidance/corpus-browser-roadmap.md` are neither, and are not this
# tool's business. Names inside the "focused files changed" section are
# repository paths by definition and are skipped wholesale.
# ---------------------------------------------------------------------------

def classify_reference(name: str, package: Path, siblings: set[str],
                       top_dirs: set[str]) -> tuple[str, str]:
    """(state, note) where state is CHECKED-OK, MISSING or NOT-PACKAGE."""
    clean = name.strip().strip("`").lstrip("./")
    if not clean or "://" in clean or clean.startswith(("/", "#", "$")):
        return "NOT-PACKAGE", "not a package-relative path"
    trailing_slash = clean.endswith("/")
    clean = clean.rstrip("/")
    if not clean:
        return "NOT-PACKAGE", "not a package-relative path"
    if "/" in clean:
        first = clean.split("/", 1)[0]
        if first not in top_dirs:
            return "NOT-PACKAGE", "a repository path, not a package member"
        target = package / clean
        if target.is_dir() or (trailing_slash and target.exists()):
            return "CHECKED-OK", "directory"
        if target.is_file():
            return "CHECKED-OK", "file"
        return "MISSING", "no such file in the package"
    suffix = clean.rsplit(".", 1)[-1].lower() if "." in clean else ""
    if suffix not in PACKAGE_DOC_SUFFIXES:
        return "NOT-PACKAGE", "not a package-document suffix"
    if (package / clean).exists():
        return "CHECKED-OK", "package root"
    if clean in siblings or (package.parent / clean).is_file():
        return "CHECKED-OK", "beside the package"
    return "MISSING", "neither in the package nor beside it"


def document_references(text: str, skip_titles: set[str]) -> list[tuple[str, str]]:
    """(name, heading) for every reference outside the skipped sections."""
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for title, body in chunks_by_heading(text):
        if title in skip_titles:
            continue
        for _, _, names in reference_spans(body):
            for name in names:
                key = (name.strip(), title)
                if key in seen:
                    continue
                seen.add(key)
                out.append((name.strip(), title or "(preamble)"))
    return out


# ---------------------------------------------------------------------------
# Hashes
# ---------------------------------------------------------------------------

def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def quoted_digests(text: str) -> list[tuple[str, str | None]]:
    """(digest, the filename it sits beside) for every SHA-256 in the text.

    BESIDE MEANS ON THE SAME LINE, or the same table cell. A window that
    spilled across lines paired the V11 package's ZIP digest with
    `claims.json`, which is named two paragraphs later -- a confident,
    invented mismatch, which is worse than the UNCHECKED this now reports.
    """
    out: list[tuple[str, str | None]] = []
    for match in SHA256_RE.finditer(text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        line_end = len(text) if line_end < 0 else line_end
        before = text[line_start:match.start()]
        after = text[match.end():line_end]
        # A markdown table puts one fact per cell; do not cross a `|`.
        if "|" in before:
            before = before.rsplit("|", 1)[1]
        if "|" in after:
            after = after.split("|", 1)[0]
        name = None
        for _, _, names in reversed(reference_spans(before)):
            usable = [one for one in names if "." in one]
            if usable:
                name = usable[-1]
                break
        if name is None:
            for _, _, names in reference_spans(after):
                usable = [one for one in names if "." in one]
                if usable:
                    name = usable[0]
                    break
        out.append((match.group(0), name))
    return out


# ---------------------------------------------------------------------------
# Identity, from `claims.json` when it is there and from `git` when it is not
# ---------------------------------------------------------------------------

def git_say(package: Path, args: list[str]) -> str | None:
    try:
        done = subprocess.run(["git", "-C", str(package)] + args,
                              capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if done.returncode != 0:
        return None
    return done.stdout.strip()


def identity_facts(package: Path) -> tuple[dict, str]:
    """The head/parent/branch this package's own records assert, and whence."""
    body = _read(package / "claims.json")
    if body is not None:
        try:
            blob = json.loads(body)
        except json.JSONDecodeError:
            blob = None
        if isinstance(blob, dict):
            ident = blob.get("identity") if isinstance(
                blob.get("identity"), dict) else {}
            facts = {
                "head": ident.get("head") or blob.get("head"),
                "parent": ident.get("parent") or ident.get("base")
                or blob.get("parent"),
                "branch": ident.get("branch") or ident.get("branch_name")
                or dig(blob, ["lane", "branch"]),
                "worktree_clean": ident.get("worktree_clean_at_head"),
            }
            return facts, "claims.json"
    head = git_say(package, ["rev-parse", "HEAD"])
    if head is None:
        return {}, "no claims.json and no git"
    return ({"head": head,
             "parent": git_say(package, ["rev-parse", "HEAD^"]),
             "branch": git_say(package, ["rev-parse", "--abbrev-ref", "HEAD"]),
             "worktree_clean": (git_say(package, ["status", "--porcelain"])
                                == "")},
            "git in the package's own directory")


# ---------------------------------------------------------------------------
# Per-content evaluation
# ---------------------------------------------------------------------------

def evaluate_prose(section_list: list[Section]) -> tuple[str, str]:
    if not section_list:
        return "ABSENT", "no section of the document is about this"
    best = "ABSENT"
    note = "section is empty"
    for section in section_list:
        body = section.body
        substantive = substantive_sentences(body)
        residual = residual_of(body)
        refs = reference_spans(body)
        if substantive and len(residual) >= MIN_SECTION_RESIDUAL:
            return "PRESENT", (f"{len(substantive)} substantive sentence(s) "
                               f"under \"{section.title}\"")
        if refs:
            verdict = "LINK-ONLY"
            detail = (f"\"{section.title}\" names {len(refs)} reference(s) and "
                      f"states nothing itself")
        else:
            verdict = "ABSENT"
            detail = f"\"{section.title}\" carries no substantive prose"
        if verdict == "LINK-ONLY" and best != "PRESENT":
            best, note = verdict, detail
        elif best == "ABSENT":
            note = detail
    return best, note


def evaluate_patterns(text: str, content: dict) -> bool:
    if "all_patterns" in content:
        return all(re.search(one, text) for one in content["all_patterns"])
    return any(re.search(one, text) for one in content["patterns"])


def evaluate_fact(section_list: list[Section], content: dict) -> tuple[str, str]:
    """The patterns run over the LOCATED SECTION, not the whole document.

    Whole-document matching is how a SHA quoted in the identity table could
    satisfy a pattern belonging to another content, and how the word "parent"
    anywhere at all satisfied the base-commit clause of #3.
    """
    if not section_list:
        return "ABSENT", "no section of the document is about this"
    for section in section_list:
        scoped = section.title + "\n" + section.body
        if evaluate_patterns(scoped, content):
            return "PRESENT", f"stated under \"{section.title}\""
    if any(reference_spans(one.body) for one in section_list):
        return "LINK-ONLY", (f"\"{section_list[0].title}\" points elsewhere "
                             f"instead of stating it")
    return "ABSENT", (f"\"{section_list[0].title}\" never states it")


def evaluate_enumeration(section_list: list[Section]) -> tuple[str, str]:
    if not section_list:
        return "ABSENT", "no section of the document is about this"
    for section in section_list:
        spans = reference_spans(section.body)
        if spans:
            named = sum(1 for _, _, names in spans if names)
            if named:
                return "PRESENT", (f"\"{section.title}\" names {named} "
                                   f"path(s)")
    return "ABSENT", f"\"{section_list[0].title}\" names nothing"


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def render_table(rows: list[tuple], headers: tuple) -> list[str]:
    width = len(headers)
    widths = [max([len(headers[i])] + [len(str(r[i])) for r in rows])
              for i in range(width)]
    lines = ["  " + "  ".join(headers[i].ljust(widths[i])
                              for i in range(width)).rstrip(),
             "  " + "  ".join("-" * widths[i] for i in range(width))]
    if not rows:
        lines.append("  (none)")
    for row in rows:
        lines.append("  " + "  ".join(str(row[i]).ljust(widths[i])
                                      for i in range(width)).rstrip())
    return lines


def emit_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------

def inspect(package: Path, declared_siblings: list[str],
            pending_siblings: list[str] | None = None) -> dict:
    """Everything this tool decides, as data. `main` only prints it."""
    handoff = package / "HANDOFF.md"
    if not handoff.is_file():
        raise SetupFailure("the package has no HANDOFF.md")
    try:
        text = handoff.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise SetupFailure("HANDOFF.md is not UTF-8 text")

    section_list = parse_sections(text)
    problems: list[str] = []

    siblings = discover_siblings(package)
    for one in declared_siblings:
        if one not in siblings:
            siblings.append(one)
    # V16: A PENDING SIBLING IS THE CHECKER ACCOUNTING FOR ITS OWN OUTPUT.
    #
    # This gate now runs LAST, at the true final state, and the one artifact
    # that cannot exist when it runs is its own transcript -- a file cannot be
    # an input to the pass that writes it. `--pending-sibling` names it, so
    # the inventory must still NAME it by exact filename (that check is not
    # relaxed) while its absence on disk at this instant is not a gap.
    #
    # NOT A GENERAL ESCAPE HATCH. A pending sibling that the inventory does
    # not name is still a finding, and a pending sibling that is not this
    # tool's own transcript is refused: an operator could otherwise silence
    # any missing artifact by declaring it pending, which is the shape of the
    # defect this whole tool exists to refuse.
    pending = list(pending_siblings or [])
    for one in pending:
        if not one.endswith(SELF_LOG_SUFFIX):
            problems.append(
                f"--pending-sibling {one} is not this tool's own transcript "
                f"({SELF_LOG_SUFFIX}): the only artifact a completeness "
                f"verdict may legitimately not see is the transcript that "
                f"verdict is being written into")
        if one not in siblings:
            siblings.append(one)
    pending_set = set(pending)
    siblings = sorted(set(siblings))
    truth = Truth(package, siblings)

    top_dirs = {one for one in os.listdir(package)
                if (package / one).is_dir()}
    sibling_set = set(siblings)

    section5 = locate(section_list, CONTENTS[4]["cues"])
    section5_titles = {one.title for one in section5}

    # ---- 1. every package-relative path the document names ---------------
    referenced_rows: list[tuple] = []
    referenced_json: list[dict] = []
    inventory_titles = {one.title for one in
                        locate(section_list, CONTENTS[9]["cues"])}
    inventory_missing = 0
    for name, heading in document_references(text, section5_titles):
        state, note = classify_reference(name, package, sibling_set, top_dirs)
        if state == "NOT-PACKAGE":
            continue
        referenced_rows.append((name, heading[:34], state, note))
        referenced_json.append({"path": name, "section": heading,
                                "state": state, "detail": note})
        if state == "MISSING":
            problems.append(
                f"HANDOFF.md names {name} under \"{heading}\" but "
                f"{note}")
            if heading in inventory_titles:
                inventory_missing += 1

    # ---- 2/5. count claims against ground truth, and against siblings -----
    count_rows: list[tuple] = []
    count_json: list[dict] = []
    others = sibling_packages(package)
    for claim in count_claims(text, section5_titles):
        actual, source = truth.get(claim["quantity"])
        if actual is None:
            verdict, note = "UNCHECKED", source
        elif actual == claim["claimed"]:
            verdict, note = "MATCH", source
        else:
            verdict = "MISMATCH"
            note = f"{source} = {actual}"
            stale = []
            for other in others:
                value, _ = Truth(other).get(claim["quantity"])
                if value == claim["claimed"]:
                    stale.append(other.name)
            if stale:
                note += f"; STALE -- {claim['claimed']} is {stale[0]}'s figure"
                problems.append(
                    f"HANDOFF.md under \"{claim['section']}\" claims "
                    f"\"{claim['said']}\" {claim['quantity']} -- that is a "
                    f"STALE COUNT from {stale[0]}; this package has {actual} "
                    f"({source})")
            else:
                problems.append(
                    f"HANDOFF.md under \"{claim['section']}\" claims "
                    f"\"{claim['said']}\" {claim['quantity']} but this "
                    f"package has {actual} ({source})")
        count_rows.append((claim["said"], claim["quantity"], verdict, note))
        count_json.append({"said": claim["said"],
                           "quantity": claim["quantity"],
                           "claimed": claim["claimed"], "actual": actual,
                           "verdict": verdict, "section": claim["section"],
                           "sentence": claim["sentence"], "detail": note})

    # ---- 4a. quoted SHA-256 digests --------------------------------------
    hash_rows: list[tuple] = []
    hash_json: list[dict] = []
    for digest, name in quoted_digests(text):
        short = digest[:12] + "..."
        if name is None:
            hash_rows.append((short, "(no filename beside it)", "UNCHECKED",
                              "no file is named near this digest"))
            hash_json.append({"digest": digest, "file": None,
                              "verdict": "UNCHECKED"})
            continue
        clean = name.strip().strip("`").lstrip("./")
        target = package / clean
        if not target.is_file():
            target = package.parent / clean
        if not target.is_file():
            hash_rows.append((short, clean, "UNCHECKED",
                              "no such file in or beside the package"))
            hash_json.append({"digest": digest, "file": clean,
                              "verdict": "UNCHECKED"})
            continue
        real = sha256_of(target)
        if real == digest:
            hash_rows.append((short, clean, "MATCH", "recomputed"))
            hash_json.append({"digest": digest, "file": clean,
                              "verdict": "MATCH"})
        else:
            hash_rows.append((short, clean, "MISMATCH",
                              "the file hashes to " + real[:12] + "..."))
            hash_json.append({"digest": digest, "file": clean,
                              "verdict": "MISMATCH", "actual": real})
            problems.append(
                f"HANDOFF.md quotes SHA-256 {digest} for {clean}, which "
                f"hashes to {real}")

    # ---- 4b. head, parent and branch -------------------------------------
    facts, source = identity_facts(package)
    identity_rows: list[tuple] = []
    identity_json: list[dict] = []
    body_hex = {one.group(0) for one in HEX_TOKEN_RE.finditer(text)}
    for key, label in (("head", "head commit"), ("parent", "parent commit")):
        value = facts.get(key)
        if not value:
            identity_rows.append((label, "(unknown)", "UNCHECKED",
                                  f"{source} states no {key}"))
            identity_json.append({"claim": label, "verdict": "UNCHECKED",
                                  "detail": source})
            continue
        # A document may abbreviate a SHA, so a stated prefix counts.
        stated = value in body_hex or any(
            len(one) >= 8 and value.startswith(one) for one in body_hex)
        identity_rows.append((label, value[:12] + "...",
                              "MATCH" if stated else "MISSING", source))
        identity_json.append({"claim": label, "value": value,
                              "verdict": "MATCH" if stated else "MISSING",
                              "detail": source})
        if not stated:
            problems.append(
                f"HANDOFF.md never states the {key} commit {value} that "
                f"{source} records")
    branch = facts.get("branch")
    if not branch:
        identity_rows.append(("branch", "(unknown)", "UNCHECKED",
                              f"{source} carries no branch name"))
        identity_json.append({"claim": "branch", "verdict": "UNCHECKED",
                              "detail": f"{source} carries no branch name"})
    else:
        found = branch in text
        identity_rows.append(("branch", branch[:34],
                              "MATCH" if found else "MISSING", source))
        identity_json.append({"claim": "branch", "value": branch,
                              "verdict": "MATCH" if found else "MISSING",
                              "detail": source})
        if not found:
            problems.append(
                f"HANDOFF.md never names the branch {branch} that {source} "
                f"records")

    # ---- 7. derived figures against claims.json --------------------------
    derived_rows: list[tuple] = []
    derived_json: list[dict] = []
    claims_body = _read(package / "claims.json")
    claims_blob = None
    if claims_body is not None:
        try:
            claims_blob = json.loads(claims_body)
        except json.JSONDecodeError:
            claims_blob = None
    if claims_blob is not None:
        documents = [("HANDOFF.md", text)]
        for entry in sorted(package.glob("*.md")):
            if entry.name == "HANDOFF.md":
                continue
            other = _read(entry)
            if other is not None:
                documents.append((entry.name, other))
        for figure in DERIVED_FIGURES:
            expected = dig(claims_blob, figure["path"])
            if not isinstance(expected, int):
                continue
            for doc_name, doc_text in documents:
                for match in re.finditer(figure["regex"],
                                         strip_emphasis(doc_text)):
                    said = match.group(1)
                    value = number_value(said)
                    if value is None:
                        continue
                    verdict = "MATCH" if value == expected else "MISMATCH"
                    derived_rows.append((doc_name, figure["label"], said,
                                         str(expected), verdict))
                    derived_json.append({"document": doc_name,
                                         "figure": figure["label"],
                                         "said": said, "claimed": value,
                                         "derived": expected,
                                         "verdict": verdict})
                    if verdict == "MISMATCH":
                        problems.append(
                            f"{doc_name} says \"{said}\" for "
                            f"{figure['label']} but claims.json derives "
                            f"{expected} at "
                            f"{'.'.join(figure['path'])}")

    # ---- the ten required contents (contents #10 decided below) ----------
    verdicts: dict[int, tuple[str, str]] = {}
    for content in CONTENTS:
        located = locate(section_list, content["cues"])
        if content["kind"] == "prose":
            verdicts[content["n"]] = evaluate_prose(located)
        elif content["kind"] == "fact":
            verdicts[content["n"]] = evaluate_fact(located, content)
        else:
            verdicts[content["n"]] = evaluate_enumeration(located)

    # ---- 3/6. the bidirectional artifact cross-check ----------------------
    inventory_sections = locate(section_list, CONTENTS[9]["cues"])
    inventory_body = "\n\n".join(one.body for one in inventory_sections)
    entries = inventory_entries(inventory_body)

    member_rows: list[tuple] = []
    member_json: list[dict] = []
    inventory_gaps = inventory_missing
    for member in top_level_members(package):
        listed = named_by(entries, member)
        member_rows.append((member, "in package",
                            "NAMED" if listed else "NOT NAMED"))
        member_json.append({"artifact": member, "where": "in package",
                            "named": listed})
        if not listed:
            inventory_gaps += 1
            problems.append(
                f"artifact inventory never names package member {member}")
    for sibling in siblings:
        listed = named_by(entries, sibling)
        exists = (package.parent / sibling).is_file()
        where = "beside package" if exists else "beside package (absent)"
        if sibling in declared_siblings and not exists:
            where = "beside package (asserted, absent)"
        if sibling in pending_set and not exists:
            where = "beside package (pending: written by this pass)"
        member_rows.append((sibling, where, "NAMED" if listed else "NOT NAMED"))
        member_json.append({"artifact": sibling, "where": where,
                            "named": listed, "exists": exists})
        if not listed:
            inventory_gaps += 1
            problems.append(
                f"artifact inventory never names sibling artifact {sibling}")
        if not exists and (sibling.endswith(SELF_LOG_SUFFIX)
                           or sibling in pending_set):
            continue
        if not exists:
            problems.append(
                f"sibling artifact {sibling} is named but does not exist "
                f"beside the package")

    if inventory_gaps and verdicts[10][0] == "PRESENT":
        verdicts[10] = ("INCOMPLETE",
                        f"the artifact cross-check found {inventory_gaps} "
                        f"discrepancy(ies) between the inventory and the "
                        f"package's real artifacts")

    content_rows: list[tuple] = []
    content_json: list[dict] = []
    for content in CONTENTS:
        verdict, why = verdicts[content["n"]]
        content_rows.append((str(content["n"]), content["text"], verdict))
        content_json.append({"n": content["n"], "content": content["text"],
                             "verdict": verdict, "detail": why})
        if verdict != "PRESENT":
            problems.append(
                f"HANDOFF.md content #{content['n']} ({content['text']}): "
                f"{verdict} -- {why}")

    # ---- the four required core files -------------------------------------
    core_rows: list[tuple] = []
    core_json: list[dict] = []
    for name in CORE_FILES:
        path = package / name
        if not path.is_file():
            state, detail = "ABSENT", "required core file is missing"
        elif path.stat().st_size == 0:
            state, detail = "EMPTY", "required core file is zero bytes"
        else:
            state, detail = "PRESENT", ""
        if state == "PRESENT" and name == "REVIEW_REQUEST.md":
            body = path.read_text(encoding="utf-8", errors="replace")
            missing = [one for one in ("Blockers", "Optional feedback")
                       if not re.search(r"(?im)^#{1,6}\s*" + re.escape(one),
                                        body)]
            if missing:
                state = "MALFORMED"
                detail = "no " + " and no ".join(
                    f"`{one}` section" for one in missing)
        if state == "PRESENT" and name == "checks.txt":
            body = path.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"(?im)\bexit\b[^\n]{0,20}?\b\d+\b", body):
                state = "MALFORMED"
                detail = "records no numeric exit status"
        core_rows.append((name, state, detail))
        core_json.append({"file": name, "state": state, "detail": detail})
        if state != "PRESENT":
            problems.append(f"core file {name}: {state} -- {detail}")

    # ---- 8. command coverage in checks.txt --------------------------------
    coverage_rows: list[tuple] = []
    coverage_json: list[dict] = []
    checks_body = _read(package / "checks.txt")
    if checks_body is not None:
        recorded = {one.group(1) for one in
                    re.finditer(r"(?im)^\s*log\s*:\s*(\S+)\s*$", checks_body)}
        shipped = sorted(
            str(one.relative_to(package)).replace(os.sep, "/")
            for one in _files_under(package / "logs")
            if one.suffix == ".log" and one.parent.name.startswith("attempt-"))
        claims_every = bool(re.search(r"(?i)every command", checks_body))
        # A DISCLOSED OMISSION IS NOT AN UNDISCLOSED ONE. V13: the V12 finding
        # was `checks.txt` claiming every command while EXPRESSLY OMITTING
        # four and silently dropping seven more. The claim and the silence
        # together are the defect; the claim alone is not. A file composed at
        # P1 cannot contain a step run at P5, and a file that says so, and
        # then NAMES the transcript it does not carry, has told the reader
        # exactly what a reader needs. So a transcript the file itself names
        # is disclosed, and only an unnamed one is missing. What this refuses
        # is still what the review refused: a completeness claim with a hole
        # nobody mentioned.
        disclosed = {one for one in shipped if one in checks_body}
        for one in shipped:
            listed = one in recorded
            state = ("RECORDED" if listed
                     else "DISCLOSED" if one in disclosed else "NO ROW")
            coverage_rows.append((one, state))
            coverage_json.append({"log": one, "recorded": listed,
                                  "disclosed": one in disclosed})
            if not listed and one not in disclosed and claims_every:
                problems.append(
                    f"checks.txt claims to record every command this lane "
                    f"ran but carries no command row for {one}, and does not "
                    f"name it among what it does not carry")
            # THE UNGATED ARM. V15, the V14 review: the arm above only fires
            # when `checks.txt` uses the words "every command", so a package
            # that dropped the claim would drop the check with it and a
            # transcript could go unrecorded and unmentioned in silence. A
            # shipped transcript with no command row is a hole in the
            # evidence whatever the file promises: the package carries a log
            # and says nothing about what produced it.
            #
            # THE ESCAPE HATCH IS KEPT, deliberately and unchanged. A file
            # composed at P1 cannot carry a step run at P5; one that NAMES
            # the transcript it does not carry has told the reader exactly
            # what a reader needs, and `disclosed` is that test. What this
            # refuses is the undisclosed hole -- now whether or not the
            # completeness claim is present to catch it.
            elif not listed and one not in disclosed:
                problems.append(
                    f"checks.txt carries no command row for the shipped "
                    f"transcript {one} and does not name it anywhere in its "
                    f"prose: the package ships a log and says nothing about "
                    f"the command that wrote it")

    # ---- 9. substance, not shape ------------------------------------------
    #
    # V15, THE V14 REVIEW. Everything above this line asks whether the package
    # has the right FILENAMES and the right SECTION HEADINGS, and a package
    # can satisfy every one of them while the evidence underneath is hollow.
    # V14 scored COMPLETE while shipping a command slot a reader cannot re-run,
    # three rows the package itself labels un-re-runnable, four tools recorded
    # as never executed beside their own transcripts, a commit described as a
    # set-aside cohort that appears in no ledger row, and a completeness claim
    # contradicted by a disclosure in another member. These six blocks read
    # the CONTENT.
    #
    # Every list here is declared unconditionally, before any file is read, so
    # the return below cannot raise on a package that is missing an input.
    # A missing input yields an empty table, which reads as "nothing to say",
    # and the surrounding checks are the ones that refuse an absent member.

    # ---- 9a. command slots that record no invocation ----------------------
    command_rows: list[tuple] = []
    command_json: list[dict] = []
    steps = checks_steps(checks_body) if checks_body is not None else []
    for slug, slots in steps:
        if "command" not in slots:
            continue
        said = slots["command"]
        where = slots.get("log") or "(no transcript recorded)"
        state = "RECORDED" if said else "EMPTY"
        command_rows.append((slug[:30], where[:40], state))
        command_json.append({"step": slug, "log": slots.get("log", ""),
                             "state": state, "command": said})
        if not said:
            problems.append(
                f"checks.txt step {slug} ({where}) carries a `command :` "
                f"slot with no invocation string: the row names a step and "
                f"records nothing that can be re-run, and nothing the "
                f"transcript can be checked against")

    # ---- 9b/9c. rows the package itself says cannot be re-run -------------
    #
    # `checks.py`'s `command_fidelity()` writes one of four verdicts into each
    # `recorded:` slot. ELIDED says capitalised tokens stand in for values the
    # lane held; PROSE says the row is a description rather than a string a
    # shell was handed. Either way the package is telling the reader, in its
    # own words, that the row as shipped cannot be re-run -- and a package
    # whose evidence says that about itself is not complete evidence. The
    # token is matched LITERALLY and in isolation so the surrounding
    # explanation, which contains the word "elided" in lower case, cannot
    # trigger it.
    elided_rows: list[tuple] = []
    elided_json: list[dict] = []
    prose_rows: list[tuple] = []
    prose_json: list[dict] = []
    for slug, slots in steps:
        said = slots.get("recorded", "")
        if not said:
            continue
        where = slots.get("log") or "(no transcript recorded)"
        if re.search(r"\bELIDED\b", said):
            elided_rows.append((slug[:30], where[:40], said[:44]))
            elided_json.append({"step": slug, "log": slots.get("log", ""),
                                "recorded": said})
            problems.append(
                f"checks.txt step {slug} ({where}) records its command "
                f"ELIDED: the package says capitalised tokens in it stand in "
                f"for values this lane held, so the string it ships is not "
                f"the string a shell was handed")
        if re.search(r"\bPROSE\b", said):
            prose_rows.append((slug[:30], where[:40], said[:44]))
            prose_json.append({"step": slug, "log": slots.get("log", ""),
                               "recorded": said})
            problems.append(
                f"checks.txt step {slug} ({where}) records its command "
                f"PROSE: the package says of its own row that it is a "
                f"description of what happened and cannot be re-run as "
                f"written")

    # ---- 9d. a tool recorded as never run, beside a command that runs it --
    #
    # The sibling executed-tool record classes every tool the package ships.
    # `shipped-not-executed` is a claim -- "this did not run" -- and
    # `checks.txt` is the file that lists what ran. When the two disagree the
    # record is wrong, not the transcript: V14 classed `gate-summary.py`,
    # `gzip-sizes.py` and `journal-dump.py` as never executed while shipping
    # both the commands that invoke them and the logs those commands wrote.
    unrun_rows: list[tuple] = []
    unrun_json: list[dict] = []
    executed_sibling = package.parent / (package.name + ".executed-tools.json")
    if checks_body is not None and executed_sibling.is_file():
        commanded = "\n".join(
            one.group(1) for one in
            re.finditer(r"(?m)^\s*command\s*:\s*(.*?)\s*$", checks_body))
        try:
            record = json.loads(executed_sibling.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            record = None
        # V16: THE ROSTER MOVED OUT OF `runs`, so read both. A /1 record
        # keeps its not-executed rows inside `runs`; a /2 record keeps them
        # in `shipped_not_executed`, because a tool that did not run has no
        # instant, no phase and no transcript and manufacturing all three is
        # how V15 shipped six invocations that describe nothing.
        rows_in = list((record or {}).get("runs") or [])
        rows_in += list((record or {}).get("shipped_not_executed") or [])
        for one in rows_in if isinstance(rows_in, list) else []:
            if not isinstance(one, dict):
                continue
            if one.get("class") != "shipped-not-executed":
                continue
            tool = str(one.get("tool") or "")
            if not tool:
                continue
            # The BASENAME, because the recorded command names the copy it
            # ran -- `logs/gzip-sizes.py`, `$EVIDENCE/gzip-sizes.py` -- and
            # which copy ran is precisely what the record is supposed to say.
            if not re.search(r"(?:^|[\s/\'\"])" + re.escape(tool) + r"(?:$|[\s\'\"])",
                             commanded):
                continue
            unrun_rows.append((tool, "shipped-not-executed", "NAMED BY A COMMAND"))
            unrun_json.append({"tool": tool, "class": "shipped-not-executed",
                               "named_by_a_recorded_command": True})
            problems.append(
                f"{executed_sibling.name} records {tool} as "
                f"shipped-not-executed, but checks.txt records a command that "
                f"runs it: the execution record and the command list "
                f"contradict each other and one of them is wrong")

    # ---- 9e. a set-aside cohort with no row in the shipped history --------
    #
    # `logs/named-commits.json` is where a package explains a commit it
    # discusses but was not built from. A commit described as a cohort that
    # RAN AND WAS SET ASIDE is a claim about the lane's history, and the
    # sibling `.attempts.jsonl` is that history. V14 described a superseded
    # head whose battery "appears only in the append-only attempt ledger's
    # set-aside row" -- and no row in the shipped ledger names it.
    cohort_rows: list[tuple] = []
    cohort_json: list[dict] = []
    named_commits = _read(package / "logs/named-commits.json")
    ledger_sibling = package.parent / (package.name + ".attempts.jsonl")
    ledger_body = _read(ledger_sibling) or ""
    if named_commits is not None:
        try:
            named = json.loads(named_commits)
        except json.JSONDecodeError:
            named = {}
        entries = named.get("commits") if isinstance(named, dict) else None
        for sha, why in sorted((entries or {}).items()):
            # A COMMIT, not one of the digests this file also carries: the
            # entries explicitly marked "Not a commit" are 64-hex artefact
            # digests and no ledger row would ever name them.
            if not re.fullmatch(r"[0-9a-f]{40}", str(sha)):
                continue
            if not re.search(r"(?i)\bset[- ]aside\b", str(why)):
                continue
            found = bool(ledger_body) and str(sha)[:12] in ledger_body
            state = "IN THE SHIPPED HISTORY" if found else "NO MATCHING ROW"
            cohort_rows.append((str(sha)[:12], "set-aside cohort", state))
            cohort_json.append({"commit": sha, "kind": "set-aside cohort",
                                "in_shipped_history": found,
                                "history": ledger_sibling.name})
            if not found:
                problems.append(
                    f"logs/named-commits.json describes {str(sha)[:12]} as a "
                    f"set-aside cohort, but {ledger_sibling.name} carries no "
                    f"row naming it: the package asserts a piece of history "
                    f"the history it ships does not record")

    # ---- 9g. THE ATTEMPT DISPOSITIONS, ON BOTH AXES -----------------------
    #
    # V16: THE EXECUTION AXIS AND THE EVIDENCE AXIS ARE DIFFERENT QUESTIONS.
    # `logs/attempts.json` carries, per attempt, how the attempt TERMINATED
    # -- `complete`, `failed`, `abandoned`, `sealed`, `discarded` -- and
    # separately whether a completed attempt's measurements remain
    # authoritative -- `authoritative`, `set-aside`, `superseded`,
    # `unevidenced`. Reading one for the other is how a cohort that ran to
    # completion and was later declined comes to be reported as though it
    # never completed, and how an abandoned attempt comes to be folded into a
    # `failed` or `discarded` tally that asserts a decision nothing made.
    #
    # WHAT THIS ACCEPTS, AND WHAT IT REFUSES. An `abandoned` attempt and an
    # evidence-`set-aside` attempt are both RESOLVED TERMINAL HISTORY: they
    # belong in the shipped record, they are counted, and neither is a
    # defect. What is refused is either of them being counted as a SUCCESS or
    # as AUTHORITATIVE EVIDENCE -- an attempt that did not finish measuring,
    # or whose figures were declined, supports no claim in this package.
    disposition_rows: list[tuple] = []
    disposition_json: list[dict] = []
    shipped_ledger = _read(package / "logs/attempts.json")
    if shipped_ledger is not None:
        try:
            shipped = json.loads(shipped_ledger)
        except json.JSONDecodeError:
            shipped = {}
        summary = shipped.get("attempts") if isinstance(shipped, dict) else []
        sides_of: dict[str, str] = {}
        for row in (shipped.get("rows") if isinstance(shipped, dict) else []):
            if not isinstance(row, dict):
                continue
            name = str(row.get("attempt") or "")
            if name and row.get("side") and name not in sides_of:
                sides_of[name] = str(row["side"])
        tally: dict[str, int] = {}
        evidence_tally: dict[str, int] = {}
        for one in (summary or []):
            if not isinstance(one, dict):
                continue
            name = str(one.get("attempt") or "")
            # THE TWO AXES, READ FROM THEIR OWN FIELDS. `status` is the LAST
            # state and answers neither question on its own; it is the
            # fallback only for a member written before the axes were
            # separated, and it is labelled as such when it is used.
            execution = str(one.get("execution_disposition") or "")
            evidence = str(one.get("evidence_disposition") or "")
            derived = ""
            if not execution:
                execution = str(one.get("terminal_status")
                                or one.get("status") or "")
                derived = " (pre-V16 member; read from terminal_status)"
            if not evidence:
                evidence = ("unevidenced" if execution in NEVER_EVIDENCE
                            else "unevidenced")
            tally[execution] = tally.get(execution, 0) + 1
            evidence_tally[evidence] = evidence_tally.get(evidence, 0) + 1
            disposition_rows.append((name[:38], execution + derived, evidence))
            disposition_json.append({
                "attempt": name,
                "side": sides_of.get(name, ""),
                "execution_disposition": execution,
                "evidence_disposition": evidence,
                "resolved_terminal_history": bool(execution),
                "supports_a_claim": evidence == "authoritative",
            })
            if execution in NEVER_EVIDENCE and evidence != "unevidenced":
                problems.append(
                    f"logs/attempts.json: {name} terminated {execution!r} and "
                    f"the member gives it the evidence disposition "
                    f"{evidence!r}. An attempt that failed, was abandoned or "
                    f"was discarded measured nothing that could be carried or "
                    f"declined; it is unevidenced, and any other word asserts "
                    f"a result its run never reached")
            if not execution:
                problems.append(
                    f"logs/attempts.json: {name} carries no execution "
                    f"disposition; every attempt reaches exactly one, and an "
                    f"attempt the shipped history leaves open is the shape "
                    f"the V15 review refused")
        # ABANDONMENT IS REPORTED BY NAME, NEVER FOLDED. A summary that shows
        # abandoned attempts inside a `failed`, `discarded` or `set-aside`
        # count is asserting a decision nothing made.
        disposition_json.append({
            "counts": {"execution": dict(sorted(tally.items())),
                       "evidence": dict(sorted(evidence_tally.items()))},
            "abandoned": tally.get("abandoned", 0),
            "note": "abandoned attempts are resolved terminal history and are "
                    "counted here under their own name; they are in no "
                    "successful and no authoritative tally",
        })

    # ---- 9f. a completeness claim another member contradicts --------------
    #
    # A package may remove or replace a ledger row -- V14 did, for a good
    # reason, and said so in PROVENANCE.md. What it may not do is say so in
    # one member while another member calls the same history complete or
    # append-only, because a reviewer reads members one at a time.
    #
    # THE REMOVAL PATTERN IS DELIBERATELY NARROW. It requires a LEDGER-ROW
    # noun beside the verb, so PRIVACY-AUDIT.md's honest sentences about the
    # sanitizer -- "a slug with its separators replaced", "a local-offset
    # timestamp is rewritten to its UTC instant rather than deleted", "the
    # identities to remove at run time" -- are not disclosures of a row
    # removal and do not arm this check.
    #
    # AND THE HONEST DOCUMENT IS EXEMPT. The member that makes the claim AND
    # discloses the removal has told the whole truth in one place; only a
    # member that makes the claim while another one carries the disclosure is
    # a problem, which is exactly the reader's situation.
    claim_rows: list[tuple] = []
    claim_json: list[dict] = []
    # THE ADJECTIVE MUST QUALIFY THE NOUN, not merely share a sentence with
    # it. An 80-character window over `complete|whole|full` and
    # `ledger|history|attempt|record` reads `full-discovery; ... attempt
    # parent-...` in LOG-INDEX.md and "wrote its own `complete` row, so one
    # attempt carried two dispositions" in LIMITATIONS.md as completeness
    # claims, which they are not. The qualifier chain below lets
    # "the complete append-only attempt and battery history" through while
    # refusing both of those, and "the incoherent ledger is kept whole in the
    # workspace" -- a true statement about a RETIRED file -- with it.
    HISTORY_NOUN = r"(?:ledgers?|histor(?:y|ies))"
    QUALIFIER = (r"(?:append-only|attempt|battery|lane|sibling|external|"
                 r"shipped|packaged|whole|complete)")
    COMPLETE_CLAIM = re.compile(
        r"(?i)(?:"
        r"\b(?:complete|whole|entire|full)\b"
        r"(?:\s+(?:and\s+)?" + QUALIFIER + r")*\s+" + HISTORY_NOUN + r"\b"
        r"|\b" + HISTORY_NOUN + r"\b[^.\n]{0,40}?\bis\s+(?:the\s+)?"
        r"(?:complete|whole|entire)\b"
        r"|\*\*append-only\*\*"
        r")")
    ROW_REMOVAL = re.compile(
        r"(?i)\b(?:rows?|lines?|entr(?:y|ies))\b[^.\n]{0,60}?\b"
        r"(?:was|were|are|is|been)\s+(?:\w+\s+){0,2}?"
        r"(?:removed|deleted|dropped|replaced|rewritten|excised|purged)\b"
        r"|\b(?:removed|deleted|dropped|replaced|rewritten|excised|purged)"
        r"\b\s+(?:\w+\s+){0,3}?\b(?:rows?|lines?|entr(?:y|ies))\b")
    documents: dict[str, str] = {}
    for one in sorted(_files_under(package)):
        if one.suffix not in (".md", ".txt"):
            continue
        body = _read(one)
        if body is not None:
            documents[str(one.relative_to(package)).replace(os.sep, "/")] = body
    disclosers = sorted(name for name, body in documents.items()
                        if ROW_REMOVAL.search(body))
    for name in sorted(documents):
        if not COMPLETE_CLAIM.search(documents[name]):
            continue
        itself = bool(ROW_REMOVAL.search(documents[name]))
        others_say = [one for one in disclosers if one != name]
        state = ("DISCLOSES IT TOO" if itself
                 else "CONTRADICTED" if others_say else "UNCONTRADICTED")
        claim_rows.append((name[:38], "complete/append-only history", state))
        claim_json.append({"document": name, "claim": "complete history",
                           "discloses_removal_itself": itself,
                           "contradicted_by": others_say if not itself else []})
        if not itself and others_say:
            problems.append(
                f"{name} calls this lane's history complete or append-only, "
                f"but {', '.join(others_say)} discloses that rows were "
                f"removed or replaced; a reader of {name} alone is told the "
                f"history is whole and is never sent to the correction")

    # ---- the conditional artifact classes ---------------------------------
    class_rows: list[tuple] = []
    class_json: list[dict] = []
    for klass in CONDITIONAL_CLASSES:
        path = package / klass["member"]
        exists = path.is_dir() if klass["is_dir"] else path.is_file()
        if exists and klass["is_dir"]:
            if not any(path.iterdir()):
                state = "EMPTY DIRECTORY"
                detail = ("an empty conditional directory implies evidence "
                          "that is not there")
                problems.append(f"conditional class {klass['name']}: {detail}")
            else:
                state, detail = "PRESENT", ""
        elif exists:
            state, detail = "PRESENT", ""
        else:
            reason = next(
                (one for one in sentences_of(inventory_body)
                 if re.search(klass["keyword"], one)
                 and len(trim_lead(residual_of(one)))
                 >= MIN_SENTENCE_RESIDUAL),
                None)
            if reason:
                state, detail = "OMITTED, REASON STATED", ""
            else:
                state = "OMITTED, NO REASON"
                detail = "the inventory states no reason for the omission"
                problems.append(f"conditional class {klass['name']}: {detail}")
        class_rows.append((klass["name"], state, detail))
        class_json.append({"class": klass["name"], "state": state,
                           "detail": detail})

    # ---- 9c. THE VERDICT IS RE-DERIVED, NOT READ ---------------------------
    #
    # V15, THE V15 REVIEW: "the handoff checker trusts the precomputed
    # `LITERAL` label". It did, exactly: 9b/9c above search the shipped
    # `recorded:` slot for the words ELIDED and PROSE and believe whatever
    # else it says. Seven V15 rows said "LITERAL -- the exact string handed
    # to the shell; re-runnable" about strings that quote `$WORKSPACE` inside
    # single quotes, and this checker -- whose entire purpose is to disbelieve
    # the documents and read the bytes -- passed every one of them.
    #
    # THE FIX IS TO RECOMPUTE. `commands.json` carries the exec record for
    # every row; `catena_command.classify` is the same function `checks.py`
    # used to write the label. Running it here turns "the package says so"
    # into "the package says so AND it is so", and a DISAGREEMENT between the
    # shipped label and the re-derivation is itself a finding -- the one V15
    # could not have, because it had nothing to disagree with.
    rederived_rows: list[tuple] = []
    rederived_json: list[dict] = []
    commands_blob = None
    commands_text = _read(package / "commands.json")
    if commands_text is not None:
        try:
            commands_blob = json.loads(commands_text)
        except json.JSONDecodeError:
            problems.append(
                "commands.json is not valid JSON: the machine-readable half "
                "of checks.txt cannot be re-derived, so every command "
                "verdict in this package rests on its own say-so")
    if isinstance(commands_blob, dict):
        try:
            defined = set(CC.check_variables(commands_blob.get("variables")))
        except CC.ExecProblem as problem:
            defined = set()
            problems.append(
                f"commands.json's root table is refused "
                f"[{problem.code}]: {problem.message}")
        rows_in = commands_blob.get("commands")
        for one in rows_in if isinstance(rows_in, list) else []:
            if not isinstance(one, dict):
                continue
            where = f"{one.get('side', '?')}/{one.get('slug', '?')}"
            said = str(one.get("recorded") or "")
            verdict, why = CC.classify(one.get("command"), one.get("exec"),
                                       defined=defined)
            state = "AGREES" if verdict == said else "DISAGREES"
            rederived_rows.append((where[:34], said[:16], verdict[:16]))
            rederived_json.append({"row": where, "shipped": said,
                                   "rederived": verdict, "state": state,
                                   "why": why})
            if verdict == CC.VERDICT_NON_EXECUTABLE:
                problems.append(
                    f"commands.json row {where} does not validate: {why}. "
                    f"The package ships it labelled {said!r}")
            elif state == "DISAGREES":
                problems.append(
                    f"commands.json row {where} ships labelled {said!r} and "
                    f"re-derives as {verdict!r}: the shipped label was not "
                    f"computed from the record beside it, and this checker "
                    f"does not take a label on trust")
    # THE ROWS THEMSELVES, RE-DERIVED FROM `checks.txt` WITH NO RECORD AT
    # ALL. This is the arm that catches V15 as shipped: it has no
    # `commands.json`, its rows are labelled `LITERAL -- the exact string
    # handed to the shell; re-runnable`, and seven of them quote a `$`-anchor
    # inside single quotes. A label that CLAIMS re-runnability about a string
    # the classifier refuses is a false statement about the evidence, and the
    # checker no longer needs the package's cooperation to find it.
    for slug, slots in steps:
        said = str(slots.get("recorded") or "")
        text = str(slots.get("command") or "")
        if not said or not text:
            continue
        claims_runnable = bool(re.search(
            r"\bLITERAL\b|\bEXECUTABLE\b|re-runnable", said))
        if not claims_runnable:
            continue
        verdict, why = CC.classify(text)
        if verdict in (CC.VERDICT_EXECUTABLE, CC.VERDICT_ELIDED):
            continue
        where = slots.get("log") or "(no transcript recorded)"
        rederived_rows.append((slug[:34], "claims re-runnable", verdict[:16]))
        rederived_json.append({"row": slug, "log": slots.get("log", ""),
                               "shipped": said, "rederived": verdict,
                               "state": "DISAGREES", "why": why})
        problems.append(
            f"checks.txt step {slug} ({where}) says of its own command that "
            f"it is re-runnable, and it is not: {why}")

    if commands_blob is None and checks_body is not None and re.search(
            r"\bEXECUTABLE\b", checks_body):
        # A package that CLAIMS executable rows and ships no machine-readable
        # record has made a claim nothing can check. V15's claim was of that
        # kind; the difference is that this now refuses rather than agrees.
        problems.append(
            "checks.txt calls at least one row EXECUTABLE and the package "
            "ships no commands.json: the claim that a row re-runs cannot be "
            "checked against anything, which is the exact shape of the V15 "
            "defect this check exists for")

    # ---- 10. EXAMPLE ACCOUNTING --------------------------------------------
    #
    # V16. The V15 review said "the authoritative logs report 28 divergent
    # examples plus two separately declared volatile lines, not the durable
    # producer claim of 30 divergences". THE REVIEW IS WRONG ON THIS POINT
    # and V16 says so with the experiment attached rather than repeating it.
    #
    # `volatile` is a static constant computed from a module-level table of
    # two `tools/pdf-review` commands with one declared line each; those two
    # captures are MASKED BEFORE COMPARISON, so they were never members of the
    # divergent set and cannot be subtracted from it. 30 = 28 + 2 is not a
    # decomposition, it is a coincidence of two unrelated numbers.
    #
    # The real 30-versus-28 is BUILD STATE. Measured three times at the exact
    # parent in a clean non-/tmp clone: a cold `build/` reports 30 divergent
    # rows and a warm one 28, and the entire delta is two captures of
    # `tools/mass-ordinary check --out build/example-ordinary`, which diverges
    # against a directory a LATER capture in the same target writes. Both
    # figures are honest reports of the run that produced them.
    #
    # So this checks three things, and enforces no constant:
    #   a. the SHAPE `divergences = examples + volatile lines` is refused
    #      whatever numbers it carries, because it is unsound;
    #   b. a durable figure must be one THIS package's own transcript
    #      supports -- the row count or the distinct-command count;
    #   c. rows and distinct commands are reported SEPARATELY, because two
    #      captures of one command are two rows and one name.
    divergence_rows: list[tuple] = []
    divergence_json: list[dict] = []
    logs_dir = package / "logs"
    found_summary = None
    summary_where = ""
    if logs_dir.is_dir():
        for one in sorted(logs_dir.glob("attempt-*/make-check-*.log")):
            body = _read(one)
            if body is None:
                continue
            fields = divergence_figures(body)
            if fields is None:
                continue
            where = f"{one.relative_to(package)}:{fields['line']}"
            divergence_rows.append(
                (where[:38], str(fields["diverged"]),
                 str(fields["diff_commands"]), str(fields["volatile"])))
            divergence_json.append({"log": str(one.relative_to(package)),
                                    **fields})
            if (fields["replayed"] + fields["never"] + fields["unrunnable"]
                    != fields["captured"]):
                problems.append(
                    f"{where}: the replay-examples partition does not close "
                    f"({fields['replayed']} replayed + {fields['never']} "
                    f"never run + {fields['unrunnable']} unrunnable != "
                    f"{fields['captured']} captured); no figure from this "
                    f"line can be cited")
            # THE SUMMARY AND THE DETAIL ROWS MUST AGREE. If the producer
            # says 30 and prints 28 DIFF rows, one of them is describing a
            # different run and neither is quotable.
            if fields["has_detail"] and fields["diff_rows"] != fields["diverged"]:
                problems.append(
                    f"{where}: the summary says {fields['diverged']} diverged "
                    f"and the transcript carries {fields['diff_rows']} DIFF "
                    f"row(s); the line and the detail below it describe "
                    f"different runs")
            if found_summary is None:
                found_summary, summary_where = fields, where
            elif found_summary["diverged"] != fields["diverged"]:
                problems.append(
                    f"two authoritative logs report different divergence "
                    f"counts: {summary_where} says "
                    f"{found_summary['diverged']} and {where} says "
                    f"{fields['diverged']}. `check-examples` is build-state "
                    f"sensitive: run it exactly once per fresh clone")
    for name in ("HANDOFF.md", "LIMITATIONS.md", "DERIVED-CLAIMS.md",
                 "CLAIM-CLOSURE.md", "UNRESOLVED-BLOCKERS.md",
                 "REVIEW_REQUEST.md", "EVIDENCE-INDEX.md", "PROVENANCE.md",
                 "changes.patch"):
        # `changes.patch` IS READ FOR THE FIGURE CHECK AND NOT FOR THE
        # DECOMPOSITION CHECK, and the split is the point. A durable figure
        # this package ships must be supported by the transcript it ships,
        # wherever it is written -- the patch included, which is where a
        # durable record's own figures reach the package. But the decomposition
        # scan asks a different question: does this package ASSERT the unsound
        # shape. The reason is the one
        # `head-consistency.py` already gives for reading only documents. A
        # patch is a record of what changed in a file the package does not
        # ship, not a claim the package makes in its own voice. This lane's
        # patch carries the durable record's own account of CORRECTING the
        # unsound decomposition -- it states the wrong form in order to refuse
        # it, which is what a correction has to do -- and a check that reads a
        # refutation as an assertion would force the record to stop saying
        # what it fixed. The claim-bearing members above are read in full and
        # none of them may state the shape.
        body = _read(package / name)
        if body is None:
            continue
        # (a) THE UNSOUND SHAPE, refused with no reference to any log.
        for match in (() if name == "changes.patch"
                      else DECOMPOSITION_CLAIM.finditer(body)):
            start = body.rfind("\n", 0, match.start()) + 1
            end = body.find("\n", match.end())
            sentence = body[start:end if end != -1 else len(body)]
            # THE EXEMPTION IS SENTENCE-SCOPED, NOT LINE-SCOPED. Prose wraps.
            # A correctly worded sum that named `total_differing_rows` on the
            # NEXT physical line was refused anyway, which pushed an author
            # toward reflowing a true sentence to satisfy a checker rather
            # than toward writing a truer one. The window is the surrounding
            # paragraph: blank-line to blank-line, which is where a wrapped
            # sentence and its own naming of the quantity both live.
            para_start = body.rfind("\n\n", 0, match.start()) + 2
            para_end = body.find("\n\n", match.end())
            paragraph = body[para_start:para_end if para_end != -1 else len(body)]
            if SOUND_TOTAL.search(paragraph):
                continue
            divergence_rows.append((name[:38], "-", "-", "DECOMPOSITION"))
            divergence_json.append({"member": name,
                                    "verdict": "UNSOUND DECOMPOSITION",
                                    "sentence": sentence[:200]})
            problems.append(
                f"{name} presents the volatile-line count as a component of "
                f"the divergence count: {sentence.strip()[:120]!r}. "
                f"`volatile` counts DECLARED LINES in a static table and "
                f"those captures are masked before comparison, so they were "
                f"never in the divergent set; the two figures are never "
                f"addends of one another whatever their values")
        # (b) THE FIGURE ITSELF, against this package's own transcript.
        if found_summary is None:
            continue
        for claimed, sentence in divergence_claims(body):
            bad = refuse_unsupported_divergence(found_summary, claimed)
            divergence_json.append({"member": name, "claimed": claimed,
                                    "verdict": bad or "SUPPORTED",
                                    "sentence": sentence[:200]})
            if bad:
                divergence_rows.append((name[:38], str(claimed), "-",
                                        "UNSUPPORTED"))
                problems.append(f"{name}: {bad} (from {summary_where})")

    # ---- 11. FINAL-STATE COMPLETENESS --------------------------------------
    #
    # V16, THE V15 REVIEW: "the final recorded COMPLETE verdict is stale:
    # rerunning the shipped checker after P11 finds the outer-sanitize and
    # outer-scan siblings unnamed and reports INCOMPLETE."
    #
    # It is stale because the verdict was taken at P10 and P11 then wrote two
    # more authoritative logs beside the package. The pipeline order is fixed
    # in `assemble.sh`; this is the check that makes the fix provable, and it
    # is deliberately UNCONDITIONAL: a package whose siblings include an
    # outer-sanitize or outer-scan transcript must name it, whether or not
    # anyone remembered to pass `--sibling`.
    final_state_rows: list[tuple] = []
    final_state_json: list[dict] = []
    for one in sorted(siblings):
        if not FINAL_STATE_SIBLING.search(one):
            continue
        named = named_by(inventory_entries(inventory_body), one) or any(
            one in (documents.get(name) or "")
            for name in ("HANDOFF.md", "EVIDENCE-INDEX.md", "PROVENANCE.md",
                         "PRIVACY-AUDIT.md"))
        final_state_rows.append((one[:52], "NAMED" if named else "UNNAMED",
                                 "outer authoritative log"))
        final_state_json.append({"sibling": one, "named": named,
                                 "kind": "outer-authoritative-log"})
        if not named:
            problems.append(
                f"{one} sits beside this package and no member names it: it "
                f"is an authoritative log of this attempt, written after the "
                f"completeness verdict was taken, so the verdict describes a "
                f"state this package is no longer in. V15's COMPLETE went "
                f"stale exactly here")

    # ---- 12. THE SHIPPED/LOCAL-ONLY BOUNDARY -------------------------------
    #
    # V16, THE V15 REVIEW: "locally retained discarded markers and raw
    # retained ledgers are outside that scan and preserve builder-local
    # offsets or absolute paths, so no broader all-retained-artifacts privacy
    # claim is accepted."
    #
    # THE RULE, STATED SO IT CAN BE CHECKED. Evidence a reviewer needs is
    # SHIPPED or it is not evidence. A local-only artifact may be REFERENCED
    # by digest -- "this is what we retained, here is its sha256" -- and that
    # is honest; what it may not be is the ONLY support for a claim, because
    # a reviewer holding the archive cannot reach it. So: a member that names
    # a local-only artifact must either ship a sanitized derivative of it or
    # say, in the same breath, that the claim rests on something the reviewer
    # cannot open.
    boundary_rows: list[tuple] = []
    boundary_json: list[dict] = []
    shipped_names = set(top_level_members(package)) | set(siblings)
    for name, body in sorted(documents.items()):
        if body is None:
            continue
        for match in LOCAL_ONLY_REFERENCE.finditer(body):
            named = match.group(1)
            if named in shipped_names or (package / named).exists():
                continue
            if (package.parent / named).exists() and named in siblings:
                continue
            start = body.rfind("\n\n", 0, match.start()) + 2
            end = body.find("\n\n", match.end())
            around = body[start:end if end != -1 else len(body)]
            disclosed = bool(LOCAL_ONLY_DISCLOSURE.search(around))
            state = "DISCLOSED" if disclosed else "UNDISCLOSED"
            boundary_rows.append((name[:24], named[:38], state))
            boundary_json.append({"member": name, "artifact": named,
                                  "state": state,
                                  "shipped": False,
                                  "sentence": around[:200]})
            if not disclosed:
                problems.append(
                    f"{name} rests a claim on {named}, which this package "
                    f"does not ship and which sits beside no sibling a "
                    f"reviewer can open, without saying so: a claim whose "
                    f"only support is a local-only artifact is a claim the "
                    f"reviewer cannot check")

    return {
        "rows": {
            "contents": content_rows, "core": core_rows,
            "referenced": referenced_rows, "counts": count_rows,
            "hashes": hash_rows, "identity": identity_rows,
            "derived": derived_rows, "members": member_rows,
            "coverage": coverage_rows, "classes": class_rows,
            "commands": command_rows, "elided": elided_rows,
            "prose": prose_rows, "unrun": unrun_rows,
            "cohorts": cohort_rows, "claims": claim_rows,
            "dispositions": disposition_rows,
            "rederived": rederived_rows, "divergence": divergence_rows,
            "final_state": final_state_rows, "boundary": boundary_rows,
        },
        "json": {
            "handoff_contents": content_json,
            "core_files": core_json,
            "referenced_files": referenced_json,
            "count_claims": count_json,
            "quoted_digests": hash_json,
            "identity_claims": identity_json,
            "derived_figures": derived_json,
            "artifacts": member_json,
            "command_coverage": coverage_json,
            "conditional_classes": class_json,
            "command_slots": command_json,
            "elided_commands": elided_json,
            "prose_commands": prose_json,
            "unrun_tools_named_by_commands": unrun_json,
            "set_aside_cohorts": cohort_json,
            "attempt_dispositions": disposition_json,
            "history_completeness_claims": claim_json,
            "rederived_command_verdicts": rederived_json,
            "divergence_accounting": divergence_json,
            "final_state_logs": final_state_json,
            "shipped_local_only_boundary": boundary_json,
            "siblings_discovered": siblings,
        },
        "problems": problems,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True,
                        help="the staged or built handoff directory")
    parser.add_argument("--sibling", action="append", default=[],
                        metavar="NAME",
                        help="an artifact that lives BESIDE the package rather "
                             "than inside it. Siblings are now DISCOVERED "
                             "automatically; this asserts an ADDITIONAL one, "
                             "which must then be named and must exist "
                             "(repeatable)")
    parser.add_argument("--pending-sibling", action="append", default=[],
                        metavar="NAME",
                        help="an artifact that HANDOFF.md names and that this "
                             "pass is about to write -- in practice this "
                             "tool's own transcript, which cannot exist when "
                             "it runs. It must still be named by exact "
                             "filename; only its absence on disk is excused, "
                             "and only for this tool's own log (repeatable)")
    parser.add_argument("--json", type=Path, default=None, metavar="OUT",
                        help="also write the findings as JSON, on the error "
                             "path too; the path must lie outside the "
                             "inspected package")
    args = parser.parse_args(argv)

    out = args.json.resolve() if args.json is not None else None
    package = args.package.resolve()

    try:
        if not package.is_dir():
            raise SetupFailure("--package is not a directory")
        if out is not None and (out == package or package in out.parents):
            raise SetupFailure(
                "--json would write into the package; this tool is read-only "
                "over the package it inspects")
        found = inspect(package, list(args.sibling),
                        list(args.pending_sibling))
    except SetupFailure as failure:
        message = f"{SETUP_PREFIX}: {failure}"
        print(message, file=sys.stderr)
        if out is not None and not (out == package or package in out.parents):
            emit_json(out, {"verdict": "SETUP FAILED",
                            "setup_failure": str(failure),
                            "problems": [message]})
        return 2

    rows = found["rows"]
    problems = found["problems"]

    print("handoff inventory: the ten required contents of HANDOFF.md")
    print()
    for line in render_table(rows["contents"],
                             ("#", "REQUIRED CONTENT", "VERDICT")):
        print(line)
    print()
    print("required core files")
    for line in render_table(rows["core"], ("FILE", "STATE", "NOTE")):
        print(line)
    print()
    print("package-relative paths HANDOFF.md names")
    for line in render_table(rows["referenced"],
                             ("PATH", "SECTION", "STATE", "NOTE")):
        print(line)
    print()
    print("count claims against the package's real contents")
    for line in render_table(rows["counts"],
                             ("SAID", "QUANTITY", "VERDICT", "GROUND TRUTH")):
        print(line)
    print()
    print("SHA-256 digests quoted in HANDOFF.md")
    for line in render_table(rows["hashes"],
                             ("DIGEST", "FILE", "VERDICT", "NOTE")):
        print(line)
    print()
    print("identity claims against the package's own records")
    for line in render_table(rows["identity"],
                             ("CLAIM", "VALUE", "VERDICT", "SOURCE")):
        print(line)
    print()
    print("derived figures against claims.json")
    for line in render_table(rows["derived"],
                             ("DOCUMENT", "FIGURE", "SAID", "DERIVED",
                              "VERDICT")):
        print(line)
    print()
    print("artifact inventory against the package's real artifacts")
    for line in render_table(rows["members"],
                             ("ARTIFACT", "WHERE", "INVENTORY")):
        print(line)
    print()
    print("command coverage in checks.txt")
    for line in render_table(rows["coverage"], ("TRANSCRIPT", "IN CHECKS.TXT")):
        print(line)
    print()
    print("conditional artifact classes")
    for line in render_table(rows["classes"], ("CLASS", "STATE", "NOTE")):
        print(line)
    print()
    print("command slots in checks.txt")
    for line in render_table(rows["commands"],
                             ("STEP", "TRANSCRIPT", "STATE")):
        print(line)
    print()
    print("commands checks.txt records ELIDED")
    for line in render_table(rows["elided"],
                             ("STEP", "TRANSCRIPT", "AS RECORDED")):
        print(line)
    print()
    print("commands checks.txt records PROSE")
    for line in render_table(rows["prose"],
                             ("STEP", "TRANSCRIPT", "AS RECORDED")):
        print(line)
    print()
    print("tools recorded as never executed, beside a command that runs them")
    for line in render_table(rows["unrun"],
                             ("TOOL", "RECORDED CLASS", "CHECKS.TXT")):
        print(line)
    print()
    print("set-aside cohorts against the shipped attempt history")
    for line in render_table(rows["cohorts"],
                             ("COMMIT", "DESCRIBED AS", "STATE")):
        print(line)
    print()
    print("attempt dispositions in the shipped history, on BOTH axes -- "
          "abandoned named, never folded")
    for line in render_table(rows["dispositions"],
                             ("ATTEMPT", "EXECUTION", "EVIDENCE")):
        print(line)
    print()
    print("history completeness claims against disclosed row removals")
    for line in render_table(rows["claims"],
                             ("DOCUMENT", "CLAIM", "STATE")):
        print(line)
    print()
    # V16: THE FOUR NEW FAMILIES, EACH WITH ITS OWN TABLE. A finding that
    # reaches only the problem list is a finding a reader cannot see the
    # shape of.
    print("command verdicts RE-DERIVED, not read from the shipped label")
    for line in render_table(rows["rederived"],
                             ("ROW", "SHIPPED", "RE-DERIVED")):
        print(line)
    print()
    print("example accounting: rows, distinct commands and declared "
          "volatile lines, each named separately")
    for line in render_table(rows["divergence"],
                             ("WHERE", "DIVERGENT ROWS", "DISTINCT COMMANDS",
                              "VOLATILE/VERDICT")):
        print(line)
    print()
    print("outer authoritative logs, named or not, at the FINAL state")
    for line in render_table(rows["final_state"],
                             ("SIBLING", "STATE", "KIND")):
        print(line)
    print()
    print("the shipped / local-only evidence boundary")
    for line in render_table(rows["boundary"],
                             ("MEMBER", "ARTIFACT", "STATE")):
        print(line)
    print()
    print(f"problems: {len(problems)}")
    for one in problems:
        print("  " + one)

    verdict = "INCOMPLETE" if problems else "COMPLETE"
    if out is not None:
        payload = dict(found["json"])
        payload["problems"] = problems
        payload["verdict"] = "FAILED" if problems else "COMPLETE"
        emit_json(out, payload)

    print(f"handoff inventory: {verdict}")
    if problems:
        print(FAIL_PREFIX, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
