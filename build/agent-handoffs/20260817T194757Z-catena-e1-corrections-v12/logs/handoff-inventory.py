#!/usr/bin/env python3
"""Refuse a handoff whose `HANDOFF.md` points at its contents instead of stating them.

THE DEFECT THIS ANSWERS. An independent review of the V10 package found that
`HANDOFF.md` carried "eight of ten required contents". The two it did not
carry were #8 known limitations and #9 unresolved decisions, and the reason
they were missing is worth stating precisely: they were not absent. A section
existed. It read, in full,

    `LIMITATIONS.md` in full; `REVIEW_REQUEST.md` carries every question that
    needs external judgment; `UNRESOLVED-BLOCKERS.md` lists every finding left
    open with its owner.

Three filenames and three verbs. No limitation is stated; no decision is left
open on the page a reviewer is told is "the factual entry point". A reader
who checked only that a heading existed would have called the file complete,
and the pipeline had no reader at all: nothing in the repository knew the
enumeration existed, so nothing could have caught it. The same review found
the artifact inventory (#10) short of four artifacts the package actually
shipped with -- `EVIDENCE-INDEX.md`, the ZIP, the ZIP's `.sha256` sidecar and
the post-seal verification transcript.

This is the missing reader. It is the protocol's enumeration, written out as
a table, evaluated against a staged or built package directory.

THE AUTHORITATIVE PROTOCOL. `guidance/external-review-handoffs.md`, under
`## Required core files` / `### HANDOFF.md` (lines 69-81), quoted verbatim:

    This is the factual entry point. It contains:

    1. task and intended outcome;
    2. current branch, or `detached HEAD` when applicable;
    3. current commit SHA and the task's base commit when known;
    4. whether the reviewed state includes uncommitted changes;
    5. focused files changed;
    6. preview URLs or exact startup commands, including required route
       state;
    7. implementation summary;
    8. known limitations;
    9. unresolved decisions; and
    10. artifact inventory, including why any conditional artifact class was
        omitted.

The same document requires the four core files (`HANDOFF.md`,
`REVIEW_REQUEST.md`, `changes.patch`, `checks.txt`); requires
`REVIEW_REQUEST.md` to divide its questions into `Blockers` and
`Optional feedback`; requires `checks.txt` to record a numeric exit status per
check; requires the conditional classes `screenshots/`, `logs/` and
`sources.md` to be either present or omitted with a reason stated in the
inventory (line 167-169); and forbids empty `screenshots/` or `logs/`
directories created "to imply review evidence exists".

WHAT THIS TOOL DECIDES, AND WHAT IT CANNOT. Each required content is reported
PRESENT, LINK-ONLY or ABSENT. LINK-ONLY is the verdict this tool exists for
and it is a HEURISTIC, not a proof -- see the LINK-ONLY RULE block below for
the rule, its threshold, and what it can and cannot catch. A section that
states one real limitation and then delegates the rest passes here; so does
a sentence of substantive-looking prose that happens to say nothing. This
tool raises the floor. It does not replace a reader.

Read-only. Standard library only. No network. Nothing is written except an
explicit `--json` path, which must lie outside the inspected package.

Usage:
    handoff-inventory.py --package DIR [--sibling NAME ...] [--json OUT]
"""

from __future__ import annotations

import argparse
import json
import os
import re
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
#      about the thing, it asserts where the thing is written down. A
#      sentence shaped `<subject> ... (see FILE)` survives, because its
#      residual opens with its own subject.
#
# A section is PRESENT when it has at least one substantive sentence and its
# total residual reaches MIN_SECTION_RESIDUAL. It is LINK-ONLY when it has no
# substantive sentence but does contain at least one reference. It is ABSENT
# when no section of the document is about that required content at all, or
# when the section is empty of both prose and references.
#
# WHAT THE RULE CATCHES: the V10 shape exactly -- a section that is a list of
# filenames with delegating verbs between them. It also catches an empty
# section and a bare `see X`.
#
# WHAT IT CANNOT CATCH, and a reader must still: (a) a section that states one
# trivial limitation and delegates every real one -- one substantive sentence
# is enough to pass; (b) prose that is substantive in shape and vacuous in
# content ("Several limitations apply to this work."), which no lexical rule
# can distinguish from a real statement; (c) a delegating sentence phrased
# without a listed opener ("Everything not proven here is elsewhere: `X`.");
# (d) a genuine statement written subject-last, whose residual happens to
# open with a listed verb. (c) and (d) are the false-negative and
# false-positive edges of the same lexical bet. The openers are listed below
# so the bet is auditable rather than hidden.
# ---------------------------------------------------------------------------

MIN_SENTENCE_RESIDUAL = 25
MIN_SECTION_RESIDUAL = 80

FILE_SUFFIXES = (
    "md|txt|json|patch|py|sh|log|zip|sha256|png|jpg|jpeg|svg|gif|js|mjs|css"
    "|html|toml|yml|yaml|ini|cfg|lock|diff"
)

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
# filename. `make public-site` is a command, not a pointer, and stripping it
# would understate the prose a startup section actually carries.
FILEISH_RE = re.compile(
    r"^[\w][\w.+\-]*(?:/[\w.+\-]*)*(?:\.(?:" + FILE_SUFFIXES + r")|/)$"
)

# Sentence boundaries. Hard-wrapped prose puts the newline inside the
# whitespace run, so `\s+` covers it; a blank line ends a sentence outright.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.;!?])\s+|\n\s*\n")

# The delegating predicates of the LINK-ONLY rule. A residual that OPENS with
# one of these, in a sentence that carried a reference, points rather than
# states.
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
# it is not in a CITATION position. `each named in `EVIDENCE-INDEX.md`` tells
# the reader where the logs are written down; it does not inventory
# `EVIDENCE-INDEX.md` as an artifact of this package, and reading it as one is
# precisely how the V10 inventory looked complete while omitting that file.
# The test is the word immediately before the reference.
CITATION_CUES = {
    "in", "into", "see", "per", "from", "at", "by", "within", "under",
    "named", "describes", "described", "listed", "referenced", "via",
    "inside", "through", "against", "beside", "throughout", "reference",
    "referenced-in", "according",
}

WORD_TRIM = "`*_\"'([{)]}.,;:!?—–-§"

# ---------------------------------------------------------------------------
# THE TEN REQUIRED CONTENTS. The wording is the protocol's own, so this table
# reads as the checklist it enforces.
#
#   kind "fact"        the content is a fact the document either states or
#                      does not; evidence is a pattern over the whole file.
#   kind "enumeration" the content is a list; evidence is that the located
#                      section names things.
#   kind "prose"       the content is an assertion; evidence is the LINK-ONLY
#                      rule above.
#   kind "inventory"   as "enumeration", plus the cross-check against the
#                      package's real members.
#
# `cues` locate the section a content belongs to, matched against heading text
# and against bold lead-in lines, case-insensitively.
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
        "patterns": [r"(?i)detached\s+HEAD",
                     r"(?i)\bbranch\b\s*[:=]\s*\S",
                     r"(?i)\bbranch\b[^\n]{0,40}`[^`\n]+`",
                     r"(?i)\bon\s+branch\b\s+\S"],
    },
    {
        "n": 3,
        "text": "current commit SHA and the task's base commit when known",
        "kind": "fact",
        "cues": [r"\bidentity\b", r"\bcommit\b", r"\bhead\b", r"\bbase\b"],
        # A SHA, a word that makes it the reviewed head, and the base clause:
        # either a base/parent is named or the document says it is unknown.
        "all_patterns": [
            r"\b[0-9a-f]{7,40}\b",
            r"(?i)\b(?:head|current commit|commit sha|reviewed commit)\b",
            r"(?i)\b(?:base|parent|merge-base|unknown base|no known base)\b",
        ],
    },
    {
        "n": 4,
        "text": "whether the reviewed state includes uncommitted changes",
        "kind": "fact",
        "cues": [r"\buncommitted\b", r"\bworking tree\b", r"\bidentity\b",
                 r"\bstate\b"],
        "patterns": [r"(?i)\buncommitted\b",
                     r"(?i)working tree\s+(?:is\s+)?clean",
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
        # A command or a preview URL, AND route state: a route-shaped token, a
        # query or fragment, or the words "route state".
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

# The conditional artifact classes the protocol names, with the keyword that
# identifies a class in an omission sentence.
CONDITIONAL_CLASSES = [
    {"name": "screenshots/", "member": "screenshots", "is_dir": True,
     "keyword": r"(?i)screenshots?"},
    {"name": "logs/", "member": "logs", "is_dir": True,
     "keyword": r"(?i)\blogs?\b"},
    {"name": "sources.md", "member": "sources.md", "is_dir": False,
     "keyword": r"(?i)\bsources?\b"},
]

FAIL_PREFIX = "HANDOFF INVENTORY FAILED"


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
    """Split a document into heading sections and bold lead-in paragraphs.

    A heading's body runs to the next heading of the same or a higher level,
    so a parent section carries its subsections' prose. A bold lead-in
    (`**Known limitations** -- ...`) becomes a section of its own, because a
    document may carry a required content without giving it a heading.
    """
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
    """The sentences of `body` that state something rather than point at it."""
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


def evaluate_fact(text: str, section_list: list[Section],
                  content: dict) -> tuple[str, str]:
    if evaluate_patterns(text, content):
        return "PRESENT", "stated in the document"
    if section_list and any(reference_spans(one.body) for one in section_list):
        return "LINK-ONLY", (f"\"{section_list[0].title}\" points elsewhere "
                             f"instead of stating it")
    return "ABSENT", "the document never states it"


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
# The artifact inventory cross-check
# ---------------------------------------------------------------------------

def inventory_entries(body: str) -> set[str]:
    """Names the inventory ENUMERATES, excluding names it merely cites.

    A reference preceded by a citation cue (`named in X`, `see X`, `per X`)
    tells a reader where something is written down. It is not an inventory
    entry, and counting it as one is how the V10 inventory looked complete
    while omitting `EVIDENCE-INDEX.md`, whose only appearance was
    "each named in `EVIDENCE-INDEX.md`".
    """
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


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def render_table(rows: list[tuple[str, str, str]], headers: tuple[str, str, str]) -> list[str]:
    widths = [max(len(headers[i]), *(len(r[i]) for r in rows)) if rows
              else len(headers[i]) for i in range(3)]
    lines = ["  " + "  ".join(headers[i].ljust(widths[i]) for i in range(3)).rstrip(),
             "  " + "  ".join("-" * widths[i] for i in range(3))]
    for row in rows:
        lines.append("  " + "  ".join(row[i].ljust(widths[i])
                                      for i in range(3)).rstrip())
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True,
                        help="the staged or built handoff directory")
    parser.add_argument("--sibling", action="append", default=[],
                        metavar="NAME",
                        help="an artifact that lives BESIDE the package rather "
                             "than inside it -- the ZIP, its .sha256 sidecar, "
                             "a post-seal transcript. The inventory must name "
                             "it too (repeatable)")
    parser.add_argument("--json", type=Path, default=None, metavar="OUT",
                        help="also write the findings as JSON; the path must "
                             "lie outside the inspected package")
    args = parser.parse_args(argv)

    package = args.package.resolve()
    if not package.is_dir():
        raise SystemExit(f"{FAIL_PREFIX}: --package is not a directory")

    if args.json is not None:
        out = args.json.resolve()
        if out == package or package in out.parents:
            raise SystemExit(
                f"{FAIL_PREFIX}: --json would write into the package; this "
                f"tool is read-only over the package it inspects")

    handoff = package / "HANDOFF.md"
    if not handoff.is_file():
        raise SystemExit(f"{FAIL_PREFIX}: the package has no HANDOFF.md")
    try:
        text = handoff.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise SystemExit(f"{FAIL_PREFIX}: HANDOFF.md is not UTF-8 text")

    section_list = parse_sections(text)
    problems: list[str] = []

    # ---- the ten required contents -------------------------------------
    content_rows: list[tuple[str, str, str]] = []
    content_json: list[dict] = []
    for content in CONTENTS:
        located = locate(section_list, content["cues"])
        if content["kind"] == "prose":
            verdict, why = evaluate_prose(located)
        elif content["kind"] == "fact":
            verdict, why = evaluate_fact(text, located, content)
        else:
            verdict, why = evaluate_enumeration(located)
        content_rows.append((str(content["n"]), content["text"], verdict))
        content_json.append({"n": content["n"], "content": content["text"],
                             "verdict": verdict, "detail": why})
        if verdict != "PRESENT":
            problems.append(
                f"HANDOFF.md content #{content['n']} ({content['text']}): "
                f"{verdict} -- {why}")

    # ---- the four required core files ----------------------------------
    core_rows: list[tuple[str, str, str]] = []
    core_json: list[dict] = []
    for name in CORE_FILES:
        path = package / name
        if not path.is_file():
            state, detail = "ABSENT", "required core file is missing"
        elif path.stat().st_size == 0:
            state, detail = "EMPTY", "required core file is zero bytes"
        else:
            state, detail = "PRESENT", ""
        # The protocol's own requirements on the non-HANDOFF core files.
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

    # ---- the inventory against the package's real members ---------------
    inventory_sections = locate(section_list, CONTENTS[9]["cues"])
    inventory_body = "\n\n".join(one.body for one in inventory_sections)
    entries = inventory_entries(inventory_body)

    member_rows: list[tuple[str, str, str]] = []
    member_json: list[dict] = []
    for member in top_level_members(package):
        listed = named_by(entries, member)
        member_rows.append((member, "in package",
                            "NAMED" if listed else "NOT NAMED"))
        member_json.append({"artifact": member, "where": "in package",
                            "named": listed})
        if not listed:
            problems.append(
                f"artifact inventory never names package member {member}")
    for sibling in args.sibling:
        listed = named_by(entries, sibling)
        member_rows.append((sibling, "beside package",
                            "NAMED" if listed else "NOT NAMED"))
        member_json.append({"artifact": sibling, "where": "beside package",
                            "named": listed})
        if not listed:
            problems.append(
                f"artifact inventory never names sibling artifact {sibling}")

    # ---- the conditional artifact classes -------------------------------
    class_rows: list[tuple[str, str, str]] = []
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

    # ---- output ---------------------------------------------------------
    print("handoff inventory: the ten required contents of HANDOFF.md")
    print()
    for line in render_table(content_rows, ("#", "REQUIRED CONTENT", "VERDICT")):
        print(line)
    print()
    print("required core files")
    for line in render_table(core_rows, ("FILE", "STATE", "NOTE")):
        print(line)
    print()
    print("artifact inventory against the package's real artifacts")
    for line in render_table(member_rows, ("ARTIFACT", "WHERE", "INVENTORY")):
        print(line)
    print()
    print("conditional artifact classes")
    for line in render_table(class_rows, ("CLASS", "STATE", "NOTE")):
        print(line)
    print()
    print(f"problems: {len(problems)}")
    for one in problems:
        print("  " + one)

    if args.json is not None:
        payload = {
            "handoff_contents": content_json,
            "core_files": core_json,
            "artifacts": member_json,
            "conditional_classes": class_json,
            "problems": problems,
            "verdict": "FAILED" if problems else "COMPLETE",
        }
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")

    if problems:
        print(FAIL_PREFIX, file=sys.stderr)
        return 1
    print("handoff inventory: COMPLETE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
