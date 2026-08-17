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

  SUBSTANTIVE. Eight mechanical reconciliations against the package's real
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

def inspect(package: Path, declared_siblings: list[str]) -> dict:
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
        member_rows.append((sibling, where, "NAMED" if listed else "NOT NAMED"))
        member_json.append({"artifact": sibling, "where": where,
                            "named": listed, "exists": exists})
        if not listed:
            inventory_gaps += 1
            problems.append(
                f"artifact inventory never names sibling artifact {sibling}")
        if not exists and sibling.endswith(SELF_LOG_SUFFIX):
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

    return {
        "rows": {
            "contents": content_rows, "core": core_rows,
            "referenced": referenced_rows, "counts": count_rows,
            "hashes": hash_rows, "identity": identity_rows,
            "derived": derived_rows, "members": member_rows,
            "coverage": coverage_rows, "classes": class_rows,
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
        found = inspect(package, list(args.sibling))
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
