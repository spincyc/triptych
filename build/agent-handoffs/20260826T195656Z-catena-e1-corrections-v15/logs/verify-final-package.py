#!/usr/bin/env python3
"""Prove the shipped ZIP against every claim the package makes about itself.

WHY THIS EXISTS. The V8 pipeline's last word was `sanitize-and-seal.py
--verify`, which proved the ZIP against the manifest and the manifest against
the tree — and never opened `claims.json`. So an inventory captured at step 9
of a 14-step pipeline shipped with five rows describing bytes that steps 9-11
had already rewritten, 1,822 bytes short of the truth, and every mechanical
check still passed. The verification and the claims never met.

THIS IS P8, AND IT IS THE MEETING. It runs from the final ZIP alone — the
artifact a reviewer actually receives, not the tree it was built from — and
its transcript is written OUTSIDE the package, because a file created after
the seal is not in the manifest that seal produced.

READ-ONLY, AND THAT IS TRUE OF THE CODE AS WELL AS THE BYTES. The V10
verifier called itself read-only while doing three things a reviewer would
not accept from an archive under review: it `exec_module`d the archive's own
`logs/derive-claims.py` in this process, and it ran the archive's own
`logs/head-consistency.py` and `logs/sanitize-and-seal.py` as subprocesses.
An archive that wants to pass could simply ship a renderer that returns the
page it shipped and an auditor that exits 0 — the verification would have
been performed BY the thing under verification. Nothing from inside the
reviewed ZIP is imported or executed here. The ZIP is opened as data; members
are read, hashed and compared. The only bytes this process writes are a
temporary extraction directory that is removed on exit, and — only when
`--table-out PATH` explicitly asks for it — the machine-readable tool table.

WHERE THE SHARED LOGIC COMES FROM INSTEAD. Checks 9 and 10 genuinely need the
renderer and the auditors, so they run the TRUSTED copies that sit beside
this file (`--tools DIR`, default `Path(__file__).parent`), and the
transcript records each one's absolute path and sha256. Coverage is not
weakened by the move, because each trusted copy's sha256 is also compared
against the archive's copy of the same tool and any divergence is a named
failure: trusted bytes == shipped bytes plus "the trusted renderer reproduces
the page" is exactly the proposition "the shipped renderer reproduces the
page", reached without running shipped code. When a comparison cannot be made
— the archive omits the tool, or the trusted copy is absent — the transcript
says so in those words and the check FAILS rather than passing quietly.

THE TRUST ANCHOR MUST ITSELF BE ANCHORED. `--tools DIR` is the only thing in
this run that is executed, so a mutable, unversioned directory of scripts is
not a trust anchor, it is a second unverified artifact. The V12 verifier
printed `(not a git checkout)` as a NOTE and passed. Here an unversioned
anchor — not a git checkout, or a checkout in which the tool directory is
untracked, or one whose tool directory has uncommitted modifications — is a
PROBLEM, named `unversioned trust anchor`, unless `--accept-unversioned-tools`
is passed, in which case the transcript says in those words that the operator
accepted it.

THE TRANSCRIPT IS BOUND TO THE ARCHIVE IT PROVES. Before the first check it
prints the ZIP's exact basename, byte size and sha256 — computed from the
archive bytes themselves, not read from the sidecar — the expected package
root, a UTC timestamp, THIS VERIFIER's own path and sha256 (it is outside the
archive, so it can hash itself), the trusted tool directory with its git
provenance, and the package's own identity (`identity.head`,
`identity.parent`, lane, declared member counts) read as JSON DATA out of the
ZIP — never by executing anything. Eleven checks, in order:

  0. TRUST ANCHOR. The `--tools` directory is a versioned, clean checkout, or
                 the operator accepted an unversioned one in writing.
  1. SIDECAR.    The ZIP's sha256 AND its byte size against the recorded
                 sidecar values. Size too: a truncated download that happens
                 to collide on nothing is still not the artifact.
  2. LAYOUT.     Exactly one top-level root, equal to the package name; no
                 duplicate entries, no absolute paths, no `..` segments.
                 Problems are typed (`Problem.kind`), and only the
                 `unsafe-path` class stops the run — a substring test over
                 English prose used to decide that, and fired on any
                 duplicate entry whose filename merely contained "path".
  3. STRUCTURE.  THE ARITHMETIC OF THE CONTAINER ITSELF, which no earlier
                 verifier performed. The End of Central Directory record is
                 parsed by hand; its claimed entry count, central-directory
                 size and central-directory offset are checked against the
                 directory that is actually there; every member's LOCAL file
                 header is compared field by field against its CENTRAL
                 directory entry (name, compression method, CRC-32,
                 compressed size, uncompressed size); and every byte of the
                 file is accounted for from offset 0 to the end of the EOCD
                 record, so a prepended prefix or a trailing tail — both of
                 which Python's `zipfile` silently tolerates — is named. A
                 ZIP that carries a second archive stapled to its front is
                 not the artifact that was sealed.
  4. CRC-32.     Every member decompressed and its CRC-32 recomputed and
                 compared against the value in the central directory, with
                 its own outcome line. The V12 verifier never called
                 `testzip()`, never read `ZipInfo.CRC` and never imported
                 `zlib`: CRC was validated only as a side effect of
                 `extractall`, and the `BadZipFile` that raised was caught by
                 a handler that appended `2 layout` to the performed list a
                 SECOND time, reporting a decompression failure as a layout
                 failure and dropping checks 3 through 7 with no accounting.
  5. EXTRACTION. Its own step, with its own outcome, precisely so that a
                 decompression failure is reported as a decompression
                 failure; when it fails the checks that need the extraction
                 are listed as SKIPPED with the reason, never dropped.
  6. MANIFEST.   The ZIP's own member list — `infolist()`, not the
                 extraction — minus `MANIFEST.sha256` equals the manifest
                 rows, and every digest matches. Reading the extraction
                 instead is how the V12 verifier could miss a duplicate entry
                 (two members with one name collapse into one file on
                 extraction and the survivor proves the manifest) and an
                 empty directory entry (it leaves no file at all). Duplicate
                 entry names are REFUSED here, independently of check 2, and
                 each member's declared uncompressed size is compared against
                 the bytes extraction actually produced.
  7. ROWS.       Every `claims.json` row matches the extracted member's bytes
                 and sha256, `evidence_bytes` is their sum and
                 `evidence_members` their count. A path frozen twice is a
                 named failure. A row that fails otherwise is the V8 defect:
                 a size claimed before the last write.
  8. PARTITION.  rows ∪ derived_members is exactly the member set, the
                 intersection is empty, and no derived member carries a size
                 or digest — named, never sized, is the contract.
  9. RENDERING.  `DERIVED-CLAIMS.md` re-rendered from the extracted
                 `claims.json` by the TRUSTED renderer, byte-compared; and
                 the archive's renderer byte-compared against the trusted one.
 10. AUDITS.     The TRUSTED `head-consistency.py` and the TRUSTED
                 sanitizer's `--check-only`, re-run over the extraction, both
                 clean; and both archive copies byte-compared against the
                 trusted ones.
 11. TOOL BYTES. EVERY tool the package ships under `logs/`, not three of
                 them. The V12 verifier's byte proof was hard-coded to
                 `derive-claims.py`, `head-consistency.py` and
                 `sanitize-and-seal.py`; eleven other shipped tools —
                 including `assemble.sh` and `checks.py`, the two that WRITE
                 the records under review — were never compared to anything
                 at all. Here every `logs/*.py` and `logs/*.sh` member gets a
                 row, a class, and a THREE-WAY digest comparison: the digest
                 captured contemporaneously AT EXECUTION (`--executed`), the
                 digest of the trusted copy, and the digest of the shipped
                 copy. Any inequality is a problem; a shipped tool with no
                 execution record and no declared class is a problem; a tool
                 in `--executed` that the package does not ship is a problem.

Between checks 8 and 9 the transcript prints the final-byte arithmetic,
derived from the extraction alone: the final member count, each derived
member's final byte size and their sum, the frozen-rows byte total, and the
total uncompressed bytes.

AND THEN IT READS THE ARCHIVE AGAIN. After every check has run, the ZIP's
byte size and sha256 are recomputed from the file on disk and compared with
the values captured before the first check. Both pairs are printed under
explicit `pre-check` / `post-check` labels together with the list of checks
that ran between them AND the list of checks that were skipped, and a
difference is a hard failure.

Every check runs even after an earlier one fails, so one transcript names
every problem rather than the first. Running it twice on the same ZIP is the
same run twice, which a reviewer can and should confirm (the header's
timestamp is the one line that moves).

-----------------------------------------------------------------------------
THE `--executed` INPUT: A CONTRACT THE ASSEMBLER MUST SATISFY
-----------------------------------------------------------------------------

A shipped copy of a tool proves nothing about the tool that RAN unless the
bytes that ran were hashed AT THE MOMENT THEY RAN. This verifier cannot go
back in time and do that; the assembler must, and hand the record here.

The assembler writes ONE such file per package attempt, BESIDE the package
and never inside it, named `<package-basename>.executed-tools.json`.
`--executed PATH` names that UTF-8 JSON file. The top level is an OBJECT with
exactly these four keys, all REQUIRED:

  {
    "schema":  "catena-executed-tools/1",       string, exactly this value.
    "attempt": "package-20260817T194757Z-03ab", string. The package attempt
                                                this record belongs to.
    "anchor":  "$EVIDENCE",                     string. The SANITIZED,
                                                SYMBOLIC tool-anchor identity
                                                -- the placeholder the sealer
                                                rewrites absolute paths to.
                                                NEVER an absolute path: this
                                                file ships, and a value that
                                                is absolute or contains a home
                                                directory is a FAULT here.
    "runs":    [ ... ]                          array (may be []).
  }

Each element of `runs` is an OBJECT with EXACTLY these eight keys, all
REQUIRED, all strings. An unknown key is a FAULT — a record whose shape
drifts is a record nobody can rely on:

  {
    "tool":    "checks.py",                     The tool ID: the BASENAME as
                                                shipped under `logs/`; for an
                                                external system tool, the
                                                command name ("git").
    "path":    "logs/checks.py",                The package-relative path of
                                                the shipped copy, or "" for an
                                                external system tool. A `path`
                                                naming something the package
                                                does not ship is a problem.
    "attempt": "package-20260817T194757Z-03ab", The run/attempt ID this
                                                invocation belongs to.
    "sha256":  "<64 lowercase hex>",            The SHA-256 of the EXACT
                                                BYTES, taken IMMEDIATELY
                                                BEFORE the invocation. May be
                                                "" for the three non-executed
                                                classes.
    "at":      "2026-08-17T19:45:20Z",          An ISO-8601 instant with an
                                                explicit offset or `Z`.
    "phase":   "P1 checks.txt and the log index",
                                                What the invocation was for.
                                                Recorded, never parsed.
    "log":     "logs/attempt-05/seal.log",      The evidence log this
                                                invocation wrote, package-
                                                relative. "" means none, and
                                                is reported as such.
    "class":   "shipped-executed",              EXACTLY one of the four
                                                values below.
  }

`runs` may carry SEVERAL rows for one tool — a tool invoked at three phases
gets three rows. EVERY row for one tool must carry the SAME `sha256`, and a
disagreement is a FAULT: that is precisely the "the bytes changed mid-run"
detection this record exists to make possible.

The four classes, which are the four ways a tool can relate to the package:

  "shipped-executed"      The package ships it AND it ran while the package
                          was built. Its `sha256` MUST equal both the trusted
                          copy's and the shipped copy's. This is the class
                          the three-way comparison exists for.
  "shipped-not-executed"  The package ships it and it did NOT run on this
                          build. `sha256` may be ""; the shipped copy is
                          still compared against the trusted one.
  "external-system-tool"  A system tool that ran but is not ours to ship
                          (git, tar, python3). `path` must be ""; `sha256`
                          may be ""; it is REPORTED, not compared.
  "reviewer-only-helper"  Shipped for the REVIEWER to run, not run by the
                          build (a test suite, this verifier). `sha256` may
                          be ""; the shipped copy is still compared against
                          the trusted one.

EVERY tool the package ships under `logs/` must appear in `runs` with some
class. One that does not is a problem — `shipped, unclassified` — because
otherwise "deliberately not run" and "we forgot to record it" are the same
silence, and the whole point of this input is to make that distinction
impossible to fudge.

WITHOUT `--executed`, this verifier degrades to the V12 behaviour — a TWO-WAY
shipped-vs-trusted comparison — and says so: the transcript prints
`EXECUTED-BYTE CLAIM: UNPROVEN` and every row's `executed` column reads `no
record`. It does not pass the executed-byte claim; it declines to make it.

-----------------------------------------------------------------------------
THE `--table-out` OUTPUT
-----------------------------------------------------------------------------

`--table-out PATH` writes the machine-readable tool table as UTF-8 JSON
(2-space indent, sorted keys, trailing newline). The top level is an OBJECT:

  {
    "schema":          "catena-tool-byte-table/1",   string, exactly.
    "generated":       "2026-08-17T19:47:57Z",       string, UTC.
    "archive":   {"name": string, "bytes": integer, "sha256": string},
    "package":         "<package root name>",        string.
    "trusted_tools":   "<absolute path>",            string.
    "executed_input":  "<absolute path>" | null,     the --executed file.
    "executed_attempt": "package-..." | null,        its `attempt`.
    "executed_anchor":  "$EVIDENCE" | null,          its `anchor`.
    "executed_proof":  "proved" | "unproven",        string.
    "problem_count":   integer,                      problems in `rows`.
    "counts":          { ... },                      object; see below.
    "rows":            [ ... ]                       array, sorted by tool_id.
  }

`counts` names the two tallies SEPARATELY, and nothing here or in the
transcript ever prints them combined. A tool invoked eight times is ONE tool
and EIGHT invocations; V14 printed `classes : shipped-executed 4,
shipped-not-executed 14` (tools) three lines below the assembler's
`executed-tools: 16 shipped-executed, 11 shipped-not-executed`
(invocations), and a reader had two tallies of one word and no way to tell
them apart.

  {
    "unique_tools":          18,      integer. One per `rows` element.
    "invocations":           27,      integer. Run rows across all tools.
    "executed_tools":         6,      integer. Tools whose class says ran.
    "executed_invocations":  20,      integer. Their run rows.
    "tools_by_class":        {...},   object, class -> tool count.
    "invocations_by_class":  {...},   object, class -> run-row count.
  }

Each element of `rows` is an OBJECT, one per tool, carrying the eight columns
the review asked for plus the trusted leg and the per-invocation detail:

  {
    "tool_id":          "assemble.sh",           string.
    "logical_path":     "logs/assemble.sh",      string.
    "class":            "shipped-executed",      string, one of the four
                                                 classes, or "unclassified".
    "attempt":          "package-...-03ab"|null, string|null. The run/attempt
                                                 ID; the single one when all
                                                 invocations agree, else null
                                                 (see `attempts`).
    "attempts":         ["...", "..."],          array of string.
    "executed":         true | false,            boolean. Did it run?
    "executed_recorded": true | false,           boolean. Was a
                                                 contemporaneous record
                                                 supplied at all?
    "executed_sha256":  "<64 hex>" | null,       string|null.
    "shipped_sha256":   "<64 hex>" | null,       string|null.
    "trusted_sha256":   "<64 hex>" | null,       string|null.
    "equal":            true | false | null,     boolean|null. null when
                                                 fewer than two digests exist
                                                 to compare.
    "evidence_log":     "logs/..." | null,       string|null. The single log
                                                 when all invocations agree,
                                                 else null.
    "evidence_logs":    ["logs/...", ...],       array of string.
    "invocations":      [ ... ],                 array. The `runs` rows for
                                                 this tool, verbatim: each an
                                                 object with the eight keys
                                                 `tool`, `path`, `attempt`,
                                                 `sha256`, `at`, `phase`,
                                                 `log`, `class`.
    "problems":         ["...", ...]             array of string.
  }

Usage:
    verify-final-package.py --zip PACKAGE.zip [--sidecar PACKAGE.zip.sha256]
                            [--name PACKAGE_NAME] [--tools TRUSTED_DIR]
                            [--executed EXECUTED.json] [--table-out TABLE.json]
                            [--accept-unversioned-tools]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib
from datetime import datetime, timezone
from pathlib import Path

# This process imports the TRUSTED renderer (check 9) from the tools
# directory, and an import that writes bytecode would leave a `__pycache__`
# beside a tool this run is supposed to leave untouched. The subprocesses of
# check 10 do not inherit this flag, so they are launched with `-B` and
# `PYTHONDONTWRITEBYTECODE=1` explicitly.
sys.dont_write_bytecode = True

MANIFEST_NAME = "MANIFEST.sha256"

# The shared logic checks 9 and 10 need, by filename. Each is resolved in the
# TRUSTED tools directory and compared against `logs/<name>` in the archive.
# NOTE: these three are the tools this verifier RUNS. They are no longer the
# only three it COMPARES -- check 11 covers every tool shipped under `logs/`.
RENDERER = "derive-claims.py"
AUDITORS = ("head-consistency.py", "sanitize-and-seal.py")

# What counts as a shipped tool for check 11: an executable-source member
# sitting directly in `logs/`, not in an attempt subdirectory.
TOOL_SUFFIXES = (".py", ".sh")

# A `claims.json` read straight out of the ZIP is untrusted input read as
# data; a cap keeps a hostile member from being decompressed into memory.
PEEK_LIMIT = 1 << 24

# The two schema identifiers, which are contracts with the assembler.
EXECUTED_SCHEMA = "catena-executed-tools/1"
TABLE_SCHEMA = "catena-tool-byte-table/1"

CLASS_SHIPPED_EXECUTED = "shipped-executed"
CLASS_SHIPPED_NOT_EXECUTED = "shipped-not-executed"
CLASS_EXTERNAL = "external-system-tool"
CLASS_REVIEWER_HELPER = "reviewer-only-helper"
CLASS_UNCLASSIFIED = "unclassified"
TOOL_CLASSES = (CLASS_SHIPPED_EXECUTED, CLASS_SHIPPED_NOT_EXECUTED,
                CLASS_EXTERNAL, CLASS_REVIEWER_HELPER)

# The eight keys every `runs` row carries, and only those eight.
RUN_KEYS = ("tool", "path", "attempt", "sha256", "at", "phase", "log", "class")
EXECUTED_KEYS = ("schema", "attempt", "anchor", "runs")
# An `at` instant: ISO-8601 with an explicit offset or `Z`.
AT_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"(?:Z|[+-]\d{2}:?\d{2})$")

# The raw signatures the structure check reads by hand. `zipfile` hides all
# of this, which is exactly why nothing in V12 could see a prepended prefix.
LFH_SIG = b"PK\x03\x04"      # local file header
CD_SIG = b"PK\x01\x02"       # central directory file header
EOCD_SIG = b"PK\x05\x06"     # end of central directory
Z64_EOCD_SIG = b"PK\x06\x06"  # zip64 end of central directory
Z64_LOC_SIG = b"PK\x06\x07"  # zip64 end of central directory locator

EOCD_STRUCT = "<IHHHHIIH"    # 22 bytes
LFH_STRUCT = "<IHHHHHIIIHH"  # 30 bytes

FLAG_DATA_DESCRIPTOR = 0x08
FLAG_UTF8_NAME = 0x800


class Problem(str):
    """A problem message that also carries a machine-readable class.

    It IS a `str`, so every consumer that prints one, joins one or asks
    `"duplicate" in one` keeps working unchanged; `kind` is the structured
    signal the control flow reads instead of guessing at English. The V10
    early exit was `if any("path" in one for one in layout)`, which fired on
    `duplicate archive entry: logs/pathological.txt` and would have stopped
    firing the day someone rewrote "parent-escaping archive path" as
    "archive entry escapes the extraction directory".
    """

    kind: str

    def __new__(cls, message: str, kind: str = "") -> "Problem":
        one = super().__new__(cls, message)
        one.kind = kind
        return one


# The layout problem classes. Only UNSAFE_PATH is fatal-before-extraction.
KIND_DUPLICATE_ENTRY = "duplicate-entry"
KIND_WRONG_ROOT = "wrong-root"
KIND_UNSAFE_PATH = "unsafe-path"
# The classes the new checks raise.
KIND_STRUCTURE = "structure"
KIND_CRC = "crc"
KIND_EXTRACTION = "extraction"
KIND_TOOL = "tool-bytes"
KIND_EXECUTED_INPUT = "executed-input"
KIND_ANCHOR = "unversioned-anchor"


class ToolBinding:
    """One piece of shared logic, and the two copies of it that must agree.

    `trusted` is the copy this verifier will actually run — outside the
    reviewed archive, identified by absolute path and digest in the
    transcript. `shipped_digest` is the digest of the archive's copy, read as
    bytes and never executed. Equal digests are what lets a check performed
    with the trusted copy be reported as a fact about the shipped one.

    Hand-written rather than a `@dataclass` on purpose: this module is loaded
    by `importlib.util.spec_from_file_location` + `exec_module` without being
    registered in `sys.modules` (the test suite does exactly that), and
    `dataclasses` resolves annotations through `sys.modules[cls.__module__]`,
    which is `None` under that load. A decorator that makes the file
    unimportable by its own test harness is not worth five lines.
    """

    def __init__(self, name: str, trusted: Path, trusted_digest: str | None,
                 shipped: str, shipped_digest: str | None) -> None:
        self.name = name
        self.trusted = trusted
        self.trusted_digest = trusted_digest
        self.shipped = shipped
        self.shipped_digest = shipped_digest


def digest(path: Path) -> str:
    hashed = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hashed.update(block)
    return hashed.hexdigest()


def member_digest(handle: zipfile.ZipFile,
                  info: zipfile.ZipInfo) -> str | None:
    """The sha256 of ONE member's decompressed bytes, read out of the ZIP.

    Read from the archive, not from an extraction: a duplicate entry name
    leaves one file on disk and two members in the container, and the whole
    point of check 11 is to hash the bytes the container actually carries.
    Returns None when the member does not decompress -- check 4 reports that
    as what it is.
    """
    hashed = hashlib.sha256()
    try:
        with handle.open(info) as stream:
            for block in iter(lambda: stream.read(1 << 20), b""):
                hashed.update(block)
    except (zipfile.BadZipFile, zlib.error, OSError, EOFError, RuntimeError,
            ValueError, NotImplementedError):
        return None
    return hashed.hexdigest()


def bind_tool(root: Path, tools: Path, name: str) -> ToolBinding:
    """Locate both copies of one tool and hash each. Reads bytes only."""
    trusted = (tools / name).resolve()
    shipped = root / "logs" / name
    return ToolBinding(
        name=name,
        trusted=trusted,
        trusted_digest=digest(trusted) if trusted.is_file() else None,
        shipped=f"logs/{name}",
        shipped_digest=digest(shipped) if shipped.is_file() else None,
    )


def binding_report(binding: ToolBinding) -> tuple[list[str], list[Problem]]:
    """The transcript lines for one binding, and the problems it raises.

    A divergence is REPORTED, never absorbed: if the archive ships a renderer
    whose bytes differ from the one this verifier ran, then what ran is not
    what shipped, and the check that used it proves nothing about the
    package. Same for a missing copy at either end.
    """
    lines = [f"    tool {binding.name}",
             f"      trusted : {binding.trusted}",
             f"      trusted sha256: {binding.trusted_digest or '(absent)'}",
             f"      shipped : {binding.shipped} (read as bytes, never run)",
             f"      shipped sha256: {binding.shipped_digest or '(absent)'}"]
    problems: list[Problem] = []
    if binding.trusted_digest is None:
        problems.append(Problem(
            f"no trusted copy of {binding.name} at {binding.trusted}: this "
            f"check cannot be performed without executing archive code, and "
            f"is NOT proved", "missing-trusted-tool"))
    if binding.shipped_digest is None:
        problems.append(Problem(
            f"the archive carries no {binding.shipped}: nothing to compare "
            f"the trusted {binding.name} against, so what this check proves "
            f"is NOT a fact about a shipped tool", "missing-shipped-tool"))
    if (binding.trusted_digest and binding.shipped_digest
            and binding.trusted_digest != binding.shipped_digest):
        problems.append(Problem(
            f"{binding.shipped} differs from the trusted "
            f"{binding.trusted.name}: shipped {binding.shipped_digest}, "
            f"trusted {binding.trusted_digest} -- the trusted copy was used, "
            f"so this check is NOT a fact about the shipped tool",
            "tool-divergence"))
    if not problems:
        lines.append("      agreement: identical bytes -- running the "
                     "trusted copy is running the shipped one")
    return lines, problems


def load_trusted(binding: ToolBinding, alias: str):
    """A TRUSTED tool, as a module.

    The V10 version of this function was `load_tool(root, ...)` and imported
    the copy out of the extracted archive, on the reasoning that importing
    from anywhere else "would verify a renderer nobody received". The
    reasoning was right about the risk and wrong about the remedy: the
    identity of the received renderer is established by comparing DIGESTS,
    which needs no execution at all, and executing it needs a trust anchor
    the archive cannot move.
    """
    location = binding.trusted
    spec = importlib.util.spec_from_file_location(alias, location)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load the trusted tool: {location}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# The checks. Each returns problems; none stops the others. They are module-
# level functions on purpose: the test suite drives each one against a crafted
# failure so that "the verifier would catch it" is a pinned fact, not a hope.
# ---------------------------------------------------------------------------


def identity_header(archive: Path, expected_root: str, hashed: str,
                    binding: list[tuple[str, str]] | None = None) -> list[str]:
    """The binding. Every `ok` below is about THESE bytes: the basename, the
    exact size, the sha256 computed from the archive itself, the root the
    layout check will demand, and when the run happened. A transcript without
    this header proves an archive; it just cannot say which one.

    `binding` carries the rest of the identity the V11 review asked for — the
    verifier's own path and digest, the trusted tool directory, the package's
    head SHA and declared counts — as ordered (label, value) pairs so that
    every line of it reads the same way.
    """
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "== P8 final verification, bound to the exact archive",
        f"   archive : {archive.name}",
        f"   bytes   : {archive.stat().st_size}",
        f"   sha256  : {hashed}",
        f"   root    : {expected_root}",
        f"   verified: {stamp} (UTC)",
    ]
    for label, value in binding or []:
        lines.append(f"   {label:<16}: {value}" if label else f"   {value}")
    return lines


def peek_identity(archive: Path, expected_root: str) -> tuple[dict, str]:
    """`claims.json`, read out of the ZIP AS DATA, before anything is
    extracted or run. `json.loads` of bytes handed back by `zipfile` executes
    nothing; this is the whole point. Returns (identity fields, note)."""
    member = f"{expected_root}/claims.json"
    try:
        with zipfile.ZipFile(archive) as handle:
            info = handle.getinfo(member)
            if info.file_size > PEEK_LIMIT:
                return {}, f"{member} is {info.file_size} bytes; not read"
            claims = json.loads(handle.read(member).decode("utf-8"))
    except KeyError:
        return {}, f"the archive carries no {member}"
    except (zipfile.BadZipFile, OSError, UnicodeDecodeError,
            json.JSONDecodeError) as error:
        return {}, f"{member} is unreadable as JSON: {error}"
    identity = claims.get("identity") or {}
    package = claims.get("package") or {}
    return {
        "head": identity.get("head") or "(absent)",
        "parent": identity.get("parent") or "(absent)",
        "review": identity.get("review_addressed") or "(none)",
        "lane": claims.get("lane") or "(absent)",
        "tool": claims.get("tool") or "(absent)",
        "members": package.get("evidence_members"),
        "bytes": package.get("evidence_bytes"),
        "derived": len(package.get("derived_members") or []),
    }, ""


def parse_sidecar(text: str) -> tuple[str, int | None]:
    """The recorded digest and byte size. The first line stays `sha256sum`
    format so `sha256sum -c` keeps working; the size is its own line."""
    found = re.search(r"\b([0-9a-fA-F]{64})\b", text)
    recorded = found.group(1).lower() if found else ""
    sized = re.search(r"^(\d+) bytes\b", text, re.M)
    return recorded, int(sized.group(1)) if sized else None


def check_sidecar(archive: Path, sidecar: Path,
                  actual_digest: str | None = None) -> list[str]:
    """Check 1: the bytes a reviewer holds are the bytes that were sealed.
    The digest is computed once, in the header, and handed in; recomputing it
    here would let the header and the check describe different reads. (The
    post-check rehash at the end is a DIFFERENT read on purpose: its whole
    job is to notice a change between the two.)"""
    problems: list[str] = []
    if not sidecar.is_file():
        return [f"no sidecar: {sidecar.name}"]
    recorded, size = parse_sidecar(sidecar.read_text(encoding="utf-8"))
    if not recorded:
        problems.append(f"{sidecar.name} records no sha256")
    elif recorded != (actual_digest or digest(archive)):
        problems.append(f"archive sha256 does not match {sidecar.name}")
    actual = archive.stat().st_size
    if size is None:
        problems.append(f"{sidecar.name} records no byte size")
    elif size != actual:
        problems.append(f"archive is {actual} bytes; {sidecar.name} "
                        f"records {size}")
    return problems


def check_layout(names: list[str], expected_root: str) -> list[Problem]:
    """Check 2: one root, no duplicates, no path that escapes extraction.

    Every problem is typed. `unsafe_layout()` below reads the type, so the
    decision "is it safe to extract this" is made on a class and not on
    whether an English sentence happens to contain the letters `path`."""
    problems: list[Problem] = []
    if len(names) != len(set(names)):
        seen: set[str] = set()
        for one in names:
            if one in seen:
                problems.append(Problem(f"duplicate archive entry: {one}",
                                        KIND_DUPLICATE_ENTRY))
            seen.add(one)
    roots = {one.split("/", 1)[0] for one in names}
    if roots != {expected_root}:
        problems.append(Problem(
            f"top-level entries {sorted(roots)}; expected exactly "
            f"['{expected_root}']", KIND_WRONG_ROOT))
    for one in names:
        if one.startswith("/") or re.match(r"^[A-Za-z]:", one):
            problems.append(Problem(f"absolute archive path: {one}",
                                    KIND_UNSAFE_PATH))
        if ".." in one.split("/"):
            problems.append(Problem(f"parent-escaping archive path: {one}",
                                    KIND_UNSAFE_PATH))
    return problems


def unsafe_layout(problems: list[Problem]) -> list[Problem]:
    """The layout problems that make extraction itself unsafe."""
    return [one for one in problems
            if getattr(one, "kind", "") == KIND_UNSAFE_PATH]


# ---------------------------------------------------------------------------
# Check 3: the container's own arithmetic.
# ---------------------------------------------------------------------------


def zip64_local_sizes(extra: bytes, usize: int, csize: int) -> tuple[int, int]:
    """The real sizes when a local header parks them in a zip64 extra field.

    Only consulted when the 32-bit field reads 0xFFFFFFFF. The extra field is
    a sequence of (id: u16, size: u16, payload) records; 0x0001 is zip64 and
    its payload begins with the uncompressed then the compressed size as
    u64s. Anything malformed is left alone -- the caller then compares the
    sentinel against the central value and reports the disagreement, which is
    the correct outcome for a header nobody can parse.
    """
    at = 0
    while at + 4 <= len(extra):
        which, size = struct.unpack_from("<HH", extra, at)
        payload = extra[at + 4:at + 4 + size]
        at += 4 + size
        if which != 0x0001:
            continue
        if len(payload) >= 8:
            usize = struct.unpack_from("<Q", payload, 0)[0]
        if len(payload) >= 16:
            csize = struct.unpack_from("<Q", payload, 8)[0]
        break
    return usize, csize


def check_structure(archive: Path,
                    infos: list[zipfile.ZipInfo]
                    ) -> tuple[list[str], list[Problem]]:
    """Check 3: EOCD arithmetic, local-vs-central headers, and every byte of
    the file accounted for.

    `zipfile` is deliberately forgiving: it locates the central directory by
    scanning backwards, silently computes an offset correction when the
    archive has a prefix stapled to it, and never looks at a local file
    header except to check the name. So an archive with a megabyte of
    unrelated bytes in front of it, or a tail appended after the EOCD, or a
    local header that disagrees with the central directory about a member's
    size, opens cleanly and lists correctly. None of those is the artifact
    that was sealed. This function reads the raw bytes and says so.
    """
    lines: list[str] = ["--- archive byte span accounting"]
    problems: list[Problem] = []
    size = archive.stat().st_size

    with archive.open("rb") as raw:
        tail_len = min(size, 22 + 0xFFFF)
        raw.seek(size - tail_len)
        tail = raw.read(tail_len)
        at = tail.rfind(EOCD_SIG)
        if at < 0 or tail_len - at < 22:
            lines.append("    (no end-of-central-directory record; the "
                         "arithmetic cannot be performed)")
            problems.append(Problem(
                "no end-of-central-directory record in the last 64 KiB of "
                "the file: this is not a well-formed ZIP container",
                KIND_STRUCTURE))
            return lines, problems
        eocd_at = size - tail_len + at
        (_sig, disk, cd_disk, here_entries, total_entries, cd_size, cd_offset,
         comment_len) = struct.unpack(EOCD_STRUCT, tail[at:at + 22])

        zip64 = 0xFFFF in (disk, cd_disk, here_entries, total_entries) \
            or 0xFFFFFFFF in (cd_size, cd_offset)
        cd_terminus = eocd_at
        if zip64:
            locator_at = eocd_at - 20
            found = False
            if locator_at >= 0:
                raw.seek(locator_at)
                locator = raw.read(20)
                if locator[:4] == Z64_LOC_SIG:
                    z64_at = struct.unpack_from("<Q", locator, 8)[0]
                    if 0 <= z64_at <= size - 56:
                        raw.seek(z64_at)
                        record = raw.read(56)
                        if record[:4] == Z64_EOCD_SIG:
                            disk, cd_disk = struct.unpack_from("<II", record,
                                                               16)
                            (here_entries, total_entries, cd_size,
                             cd_offset) = struct.unpack_from("<QQQQ", record,
                                                             24)
                            cd_terminus = z64_at
                            found = True
            lines.append("    zip64            : yes")
            if not found:
                problems.append(Problem(
                    "the EOCD record uses zip64 sentinel values but no "
                    "readable zip64 end-of-central-directory record was "
                    "found before it", KIND_STRUCTURE))
                return lines, problems

        eocd_end = eocd_at + 22 + comment_len
        trailing = size - eocd_end
        actual_cd_at = cd_terminus - cd_size
        first_local = min((one.header_offset for one in infos), default=0)

        # -- the raw walk of the central directory ------------------------
        walk_count = 0
        walk_size = 0
        if 0 <= actual_cd_at <= size:
            raw.seek(actual_cd_at)
            blob = raw.read(max(cd_size, 0))
            cursor = 0
            while cursor + 46 <= len(blob) and blob[cursor:cursor + 4] == CD_SIG:
                namelen, extralen, commentlen = struct.unpack_from(
                    "<HHH", blob, cursor + 28)
                cursor += 46 + namelen + extralen + commentlen
                walk_count += 1
            walk_size = cursor
        else:
            problems.append(Problem(
                f"the end-of-central-directory record places the central "
                f"directory at offset {actual_cd_at}, which is outside the "
                f"{size}-byte file", KIND_STRUCTURE))

        lines += [
            f"    file size          : {size} bytes",
            f"    first local header : offset {first_local}",
            f"    central directory  : offset {actual_cd_at}, {walk_size} "
            f"byte(s), {walk_count} entry(ies) walked",
            f"    EOCD record        : offset {eocd_at}, comment "
            f"{comment_len} byte(s), ends at {eocd_end}",
            f"    EOCD claims        : central directory at offset "
            f"{cd_offset}, {cd_size} byte(s), {total_entries} entry(ies)",
            f"    zipfile decoded    : {len(infos)} entry(ies)",
            f"    span               : bytes 0..{eocd_end} of {size}; "
            f"prefix {first_local}, trailing {trailing}",
        ]

        # -- prefix and tail ----------------------------------------------
        if first_local != 0:
            problems.append(Problem(
                f"{first_local} byte(s) precede the first local file header: "
                f"the archive carries a prepended prefix and is not the "
                f"sealed artifact", KIND_STRUCTURE))
        if actual_cd_at != cd_offset:
            problems.append(Problem(
                f"the end-of-central-directory record places the central "
                f"directory at offset {cd_offset}; it actually begins at "
                f"{actual_cd_at} (a {actual_cd_at - cd_offset}-byte shift)",
                KIND_STRUCTURE))
        if trailing > 0:
            problems.append(Problem(
                f"{trailing} trailing byte(s) after the end-of-central-"
                f"directory record: the archive's bytes are not exactly "
                f"accounted for", KIND_STRUCTURE))
        elif trailing < 0:
            problems.append(Problem(
                f"the end-of-central-directory comment claims {comment_len} "
                f"byte(s), which overruns the end of the {size}-byte file",
                KIND_STRUCTURE))

        # -- the counts and the sizes -------------------------------------
        if disk != 0 or cd_disk != 0:
            problems.append(Problem(
                f"the archive claims to be a multi-disk set (disk {disk}, "
                f"central directory on disk {cd_disk}); a sealed evidence "
                f"package is one file", KIND_STRUCTURE))
        if here_entries != total_entries:
            problems.append(Problem(
                f"the end-of-central-directory record claims {here_entries} "
                f"entry(ies) on this disk but {total_entries} in total",
                KIND_STRUCTURE))
        if total_entries != len(infos):
            problems.append(Problem(
                f"the end-of-central-directory record claims {total_entries} "
                f"entry(ies); the central directory holds {len(infos)}",
                KIND_STRUCTURE))
        if walk_count != len(infos):
            problems.append(Problem(
                f"a raw walk of the central directory found {walk_count} "
                f"entry(ies); zipfile decoded {len(infos)}", KIND_STRUCTURE))
        if walk_size != cd_size:
            problems.append(Problem(
                f"the end-of-central-directory record records a "
                f"{cd_size}-byte central directory; it walks to {walk_size} "
                f"byte(s)", KIND_STRUCTURE))

        # -- every local header against its central entry ------------------
        descriptors = 0
        spans: list[tuple[int, int, str]] = []
        for info in sorted(infos, key=lambda one: one.header_offset):
            raw.seek(info.header_offset)
            head = raw.read(30)
            if len(head) < 30 or head[:4] != LFH_SIG:
                problems.append(Problem(
                    f"{info.filename}: no local file header at the offset "
                    f"{info.header_offset} its central directory entry "
                    f"records", KIND_STRUCTURE))
                continue
            (_s, _v, flags, method, _t, _d, crc, csize, usize, namelen,
             extralen) = struct.unpack(LFH_STRUCT, head)
            name_bytes = raw.read(namelen)
            extra = raw.read(extralen)
            if usize == 0xFFFFFFFF or csize == 0xFFFFFFFF:
                usize, csize = zip64_local_sizes(extra, usize, csize)
            try:
                local_name = name_bytes.decode(
                    "utf-8" if flags & FLAG_UTF8_NAME else "cp437")
            except UnicodeDecodeError:
                local_name = repr(name_bytes)
            if local_name != info.filename:
                problems.append(Problem(
                    f"local header name {local_name!r} disagrees with the "
                    f"central directory entry {info.filename!r}",
                    KIND_STRUCTURE))
            if method != info.compress_type:
                problems.append(Problem(
                    f"{info.filename}: local header compression method "
                    f"{method} disagrees with the central directory's "
                    f"{info.compress_type}", KIND_STRUCTURE))
            if flags & FLAG_DATA_DESCRIPTOR:
                descriptors += 1
            else:
                if crc != info.CRC:
                    problems.append(Problem(
                        f"{info.filename}: local header CRC-32 {crc:08x} "
                        f"disagrees with the central directory's "
                        f"{info.CRC:08x}", KIND_STRUCTURE))
                if csize != info.compress_size:
                    problems.append(Problem(
                        f"{info.filename}: local header compressed size "
                        f"{csize} disagrees with the central directory's "
                        f"{info.compress_size}", KIND_STRUCTURE))
                if usize != info.file_size:
                    problems.append(Problem(
                        f"{info.filename}: local header uncompressed size "
                        f"{usize} disagrees with the central directory's "
                        f"{info.file_size}", KIND_STRUCTURE))
            spans.append((info.header_offset,
                          info.header_offset + 30 + namelen + extralen
                          + info.compress_size,
                          info.filename))

        # -- the member data region, byte by byte --------------------------
        if descriptors:
            lines.append(
                f"    data descriptors   : {descriptors} member(s) stream "
                f"their sizes into a trailing data descriptor; their local "
                f"CRC/size fields are empty by design and the member-region "
                f"accounting below is not performed")
        else:
            cursor = first_local
            for start, end, name in sorted(spans):
                if start != cursor:
                    problems.append(Problem(
                        f"{start - cursor} unaccounted byte(s) between the "
                        f"previous member and the local header of {name}",
                        KIND_STRUCTURE))
                cursor = max(cursor, end)
            if infos and cursor != actual_cd_at:
                problems.append(Problem(
                    f"{actual_cd_at - cursor} unaccounted byte(s) between "
                    f"the last member's data and the central directory",
                    KIND_STRUCTURE))
            elif not problems:
                lines.append("    accounted          : every byte from 0 to "
                             "the end of the EOCD record belongs to a member, "
                             "the central directory, or the EOCD itself")
    return lines, problems


def check_crc(handle: zipfile.ZipFile,
              infos: list[zipfile.ZipInfo]) -> list[Problem]:
    """Check 4: every member's CRC-32, recomputed and compared.

    The V12 verifier never checked a CRC explicitly. It relied on
    `extractall` raising, and its handler reported the raising as a LAYOUT
    problem while quietly dropping five later checks. A CRC failure is a
    statement about a member's bytes and it deserves its own outcome, its own
    wording, and its own place in the performed/skipped accounting.

    `zipfile` verifies the CRC itself at end-of-stream and raises
    `BadZipFile("Bad CRC-32 for file ...")`; the running CRC computed here is
    complete by that point, so the message names both values rather than
    forwarding an exception string.
    """
    problems: list[Problem] = []
    for info in infos:
        if info.is_dir():
            if info.file_size or info.CRC:
                problems.append(Problem(
                    f"directory entry {info.filename} declares "
                    f"{info.file_size} byte(s) and CRC {info.CRC:08x}; a "
                    f"directory entry carries neither", KIND_CRC))
            continue
        running = 0
        total = 0
        failure = None
        try:
            with handle.open(info) as stream:
                for block in iter(lambda: stream.read(1 << 20), b""):
                    running = zlib.crc32(block, running)
                    total += len(block)
        except (zipfile.BadZipFile, zlib.error, OSError, EOFError,
                RuntimeError, ValueError, NotImplementedError) as error:
            failure = error
        actual = running & 0xFFFFFFFF
        expected = info.CRC & 0xFFFFFFFF
        if failure is not None and "CRC" not in str(failure):
            problems.append(Problem(
                f"member {info.filename} does not decompress: {failure}",
                KIND_CRC))
            continue
        if actual != expected:
            problems.append(Problem(
                f"CRC-32 mismatch for {info.filename}: the central directory "
                f"records {expected:08x}, the decompressed bytes hash to "
                f"{actual:08x}", KIND_CRC))
        elif failure is not None:
            problems.append(Problem(
                f"member {info.filename} does not decompress: {failure}",
                KIND_CRC))
        if total != info.file_size and failure is None:
            problems.append(Problem(
                f"member {info.filename} decompresses to {total} byte(s); "
                f"the central directory declares {info.file_size}", KIND_CRC))
    return problems


def check_manifest(root: Path, infos: list[zipfile.ZipInfo],
                   expected_root: str) -> list[str]:
    """Check 6: the manifest, cross-proved against the ZIP'S OWN MEMBER LIST.

    The V12 version of this function built its `present` set from
    `root.rglob("*")` over the extraction, so the container's truth reached it
    only after extraction had already flattened it: two members named the same
    thing became one file and the survivor proved the manifest; an empty
    directory entry left nothing on disk at all and was invisible; and no
    entry's declared size was ever compared against anything. The member set
    now comes from `infolist()`, duplicates are REFUSED here independently of
    check 2, directory entries are named, and each member's declared
    uncompressed size is compared against the bytes extraction produced. The
    digests still come from the extracted files, which is where the bytes are.
    """
    problems: list[str] = []
    prefix = f"{expected_root}/"
    shipped: dict[str, zipfile.ZipInfo] = {}
    directories: list[str] = []
    seen: set[str] = set()
    for info in infos:
        name = info.filename
        if not name.startswith(prefix):
            problems.append(f"archive entry {name} is outside {prefix}")
            continue
        relative = name[len(prefix):]
        if info.is_dir():
            directories.append(relative.rstrip("/"))
            continue
        if not relative:
            continue
        if name in seen:
            problems.append(f"duplicate ZIP entry name: {relative} -- the "
                            f"manifest cross-check refuses duplicate entries, "
                            f"because on extraction they collapse into one "
                            f"file and the survivor proves the manifest for "
                            f"both")
        seen.add(name)
        shipped[relative] = info
    for one in sorted(directories):
        if not any(member.startswith(one + "/") for member in shipped):
            problems.append(f"empty directory entry {one}/: it leaves nothing "
                            f"on extraction, so no manifest row can cover it")

    target = root / MANIFEST_NAME
    if not target.is_file():
        return problems + [f"the archive carries no {MANIFEST_NAME}"]
    listed: dict[str, str] = {}
    for number, line in enumerate(
            target.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        found = re.match(r"^([0-9a-fA-F]{64})\s\s?(.+)$", line)
        if not found:
            problems.append(f"malformed manifest line {number}: {line!r}")
            continue
        # A path listed twice collapses into one dict key below and the rest
        # of the check then proves half of what the manifest appears to say.
        if found.group(2) in listed:
            problems.append(f"duplicate manifest row: {found.group(2)}")
        listed[found.group(2)] = found.group(1).lower()

    present = {one.relative_to(root).as_posix()
               for one in sorted(root.rglob("*")) if one.is_file()}
    for one in sorted(set(shipped) - present):
        problems.append(f"the ZIP declares {one}, which the extraction does "
                        f"not produce")
    for one in sorted(present - set(shipped)):
        problems.append(f"the extraction produced {one}, which the ZIP's "
                        f"central directory does not declare")

    for one in sorted(set(listed) - set(shipped)):
        problems.append(f"manifest lists {one}, which the archive omits")
    for one in sorted(set(shipped) - set(listed) - {MANIFEST_NAME}):
        problems.append(f"archive carries {one}, which the manifest does "
                        f"not list")
    for one in sorted(set(listed) & set(shipped)):
        path = root / one
        if not path.is_file():
            continue
        actual = path.stat().st_size
        if actual != shipped[one].file_size:
            problems.append(f"{one}: the central directory declares "
                            f"{shipped[one].file_size} byte(s), the "
                            f"extraction delivers {actual}")
        if digest(path) != listed[one]:
            problems.append(f"digest mismatch against the manifest: {one}")
    return problems


def check_claims_rows(claims: dict, root: Path) -> list[str]:
    """Check 7: every frozen row against the delivered bytes. A failing row is
    THE defect this protocol exists to make impossible: a (bytes, sha256)
    computed before the last write of the bytes it claims."""
    problems: list[str] = []
    package = claims["package"]
    rows = package["rows"]
    # A path frozen twice would double-count in evidence_bytes and let two
    # rows disagree about one member; named here, independently of check 2's
    # duplicate archive entries.
    seen: set[str] = set()
    for one in rows:
        if one["path"] in seen:
            problems.append(f"duplicate claims row: {one['path']}")
        seen.add(one["path"])
    for one in rows:
        path = root / one["path"]
        if not path.is_file():
            problems.append(f"claims row {one['path']}: not in the archive")
            continue
        if path.stat().st_size != one["bytes"]:
            problems.append(f"claims row {one['path']}: claims {one['bytes']} "
                            f"bytes, archive delivers "
                            f"{path.stat().st_size} -- a stale row")
        elif digest(path) != one["sha256"]:
            problems.append(f"claims row {one['path']}: sha256 does not match "
                            f"the delivered bytes -- a stale row")
    total = sum(one["bytes"] for one in rows)
    if package.get("evidence_bytes") != total:
        problems.append(f"evidence_bytes says {package.get('evidence_bytes')}; "
                        f"the rows sum to {total}")
    if package.get("evidence_members") != len(rows):
        problems.append(f"evidence_members says "
                        f"{package.get('evidence_members')}; there are "
                        f"{len(rows)} rows")
    return problems


def check_partition(claims: dict, root: Path) -> list[str]:
    """Check 8: rows ∪ derived_members is the member set, exactly, and a
    derived member is a name and a reason -- never a size, never a hash."""
    problems: list[str] = []
    package = claims["package"]
    frozen = {one["path"] for one in package["rows"]}
    derived_rows = package.get("derived_members") or []
    derived = {one["path"] for one in derived_rows}
    for one in derived_rows:
        extra = sorted(set(one) - {"path", "reason"})
        if extra:
            problems.append(f"derived member {one.get('path', '?')} carries "
                            f"{', '.join(extra)}: named, never sized")
    present = {one.relative_to(root).as_posix()
               for one in sorted(root.rglob("*")) if one.is_file()}
    for one in sorted(frozen & derived):
        problems.append(f"{one} is both a frozen row and a derived member")
    for one in sorted(present - frozen - derived):
        problems.append(f"{one} is in the archive but in neither rows nor "
                        f"derived_members")
    for one in sorted((frozen | derived) - present):
        problems.append(f"{one} is claimed (row or derived) but not in the "
                        f"archive")
    return problems


def final_bytes(claims: dict, root: Path) -> list[str]:
    """The final-byte arithmetic, derived from the extraction alone. The
    frozen rows carry their own total by construction; the derived members
    are named-never-sized in claims.json, so their FINAL sizes exist nowhere
    until somebody measures the delivered bytes — this is where. Reporting,
    not a check: any disagreement is already a partition or rows failure."""
    package = claims["package"]
    rows = package.get("rows") or []
    frozen_total = sum(one["bytes"] for one in rows)
    present = sorted(one for one in root.rglob("*") if one.is_file())
    total = sum(one.stat().st_size for one in present)
    lines = [
        "--- final bytes, derived from the archive alone",
        f"    members            : {len(present)}",
        f"    frozen rows        : {len(rows)} row(s), {frozen_total} bytes",
    ]
    derived_rows = package.get("derived_members") or []
    derived_total = 0
    for one in derived_rows:
        path = root / one["path"]
        if path.is_file():
            derived_total += path.stat().st_size
            lines.append(f"    derived {one['path']}: "
                         f"{path.stat().st_size} bytes")
        else:
            lines.append(f"    derived {one['path']}: (absent)")
    lines.append(f"    derived members    : {len(derived_rows)} member(s), "
                 f"{derived_total} bytes")
    summed = frozen_total + derived_total
    closing = (f"    total uncompressed : {total} bytes across "
               f"{len(present)} member(s)")
    if summed == total:
        closing += f" (= frozen {frozen_total} + derived {derived_total})"
    else:
        closing += (f"; frozen {frozen_total} + derived {derived_total} = "
                    f"{summed}, which does not add up -- see the partition "
                    f"check")
    lines.append(closing)
    return lines


def check_rendering(root: Path, tools: Path) -> list[str]:
    """Check 9: the renderer, over the shipped claims, must reproduce the
    shipped page byte for byte. Two records of one fact, proved one.

    The renderer that RUNS is the trusted copy beside this verifier; the
    renderer that SHIPPED is hashed and compared, never imported. When the
    two digests agree, "the trusted renderer reproduces the page" and "the
    shipped renderer reproduces the page" are the same sentence, and the
    second one has been reached without giving the archive a way to answer
    the question about itself. When they disagree, `binding_report` says so
    and this check fails.
    """
    binding = bind_tool(root, tools, RENDERER)
    lines, problems = binding_report(binding)
    print("--- check 9 trust anchor")
    for line in lines:
        print(line)
    if binding.trusted_digest is None:
        return problems
    try:
        deriver = load_trusted(binding, "trusted_deriver")
    except (SystemExit, Exception) as error:  # noqa: BLE001 -- report, don't die
        return problems + [f"cannot load the trusted renderer: {error}"]
    claims_path = root / "claims.json"
    page = root / "DERIVED-CLAIMS.md"
    for one in (claims_path, page):
        if not one.is_file():
            return problems + [f"the archive carries no {one.name}; the "
                               f"re-render comparison is NOT proved"]
    try:
        claims = json.loads(claims_path.read_text(encoding="utf-8"))
        rendered = deriver.render(claims)
    except Exception as error:  # noqa: BLE001 -- a crash is a finding
        return problems + [f"the trusted renderer could not render the "
                           f"shipped claims.json: {error!r}"]
    shipped = page.read_text(encoding="utf-8")
    if rendered != shipped:
        problems.append("DERIVED-CLAIMS.md does not re-render byte-identically "
                        "from the shipped claims.json")
    return problems


def check_shipped_audits(root: Path, tools: Path) -> list[str]:
    """Check 10: the package's own auditors, replayed over the extraction —
    from the TRUSTED copies, with the shipped copies hashed and compared.

    Run with the extraction as the working directory so the sanitizer's
    repo-root rule keys on nothing: what is being asked is whether the
    DELIVERED bytes are clean and consistent, on any machine. Because the
    scripts now live outside the extraction, `sys.path[0]` in the child is
    the trusted tools directory rather than the archive's `logs/` — so an
    archive cannot even shadow a stdlib module the auditor imports.

    `-B` and `PYTHONDONTWRITEBYTECODE=1` are passed explicitly: this
    process's `sys.dont_write_bytecode` is not inherited, and the V10 run
    left `__pycache__` directories beside whatever it executed.
    """
    problems: list[str] = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    arguments = {
        "head-consistency.py": ["--package", str(root)],
        "sanitize-and-seal.py": [str(root), "--check-only"],
    }
    print("--- check 10 trust anchors")
    bindings = []
    for name in AUDITORS:
        binding = bind_tool(root, tools, name)
        bindings.append(binding)
        lines, found = binding_report(binding)
        for line in lines:
            print(line)
        problems.extend(found)
    for binding in bindings:
        if binding.trusted_digest is None:
            print(f"--- {binding.name} over the extraction: NOT RUN "
                  f"(no trusted copy)")
            continue
        command = [sys.executable, "-B", str(binding.trusted)]
        command += arguments[binding.name]
        done = subprocess.run(command, capture_output=True, text=True,
                              cwd=root, env=env)
        print(f"--- {binding.name} (trusted copy) over the extraction "
              f"(exit {done.returncode})")
        sys.stdout.write(done.stdout)
        sys.stderr.write(done.stderr)
        if done.returncode != 0:
            problems.append(f"{binding.name} fails over the extracted archive")
    return problems


# ---------------------------------------------------------------------------
# Check 11: every shipped tool, three ways.
# ---------------------------------------------------------------------------


def shipped_tool_digests(handle: zipfile.ZipFile,
                         expected_root: str) -> dict[str, str | None]:
    """The digest of every tool the package ships directly under `logs/`.

    Read out of the ZIP as bytes, never executed, never extracted first. A
    member that will not decompress maps to None and is reported as such;
    check 4 has already named the underlying failure.
    """
    prefix = f"{expected_root}/logs/"
    found: dict[str, str | None] = {}
    for info in handle.infolist():
        if info.is_dir():
            continue
        name = info.filename
        if not name.startswith(prefix):
            continue
        rest = name[len(prefix):]
        if "/" in rest or not rest.endswith(TOOL_SUFFIXES):
            continue
        found[rest] = member_digest(handle, info)
    return found


def load_executed(path: Path) -> tuple[dict, list[Problem]]:
    """The contemporaneous execution record, validated against the contract.

    A digest handed in by the assembler is the ONLY evidence anyone will ever
    have about the bytes that actually ran, so a malformed record is a
    finding, not something to work around. Every field named in the module
    docstring is checked for presence and type here; the message says which
    element and which key, because the assembler is the audience.
    """
    problems: list[Problem] = []
    empty: dict = {"runs": [], "attempt": None, "anchor": None}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError) as error:
        return empty, [Problem(f"--executed {path} is unreadable as JSON: "
                               f"{error}", KIND_EXECUTED_INPUT)]
    if not isinstance(raw, dict):
        return empty, [Problem(f"--executed {path}: the top level must be a "
                               f"JSON object, not a "
                               f"{type(raw).__name__}", KIND_EXECUTED_INPUT)]
    if raw.get("schema") != EXECUTED_SCHEMA:
        problems.append(Problem(
            f"--executed {path}: schema is {raw.get('schema')!r}; this "
            f"verifier implements {EXECUTED_SCHEMA!r}", KIND_EXECUTED_INPUT))
    for key in EXECUTED_KEYS:
        if key not in raw:
            problems.append(Problem(
                f"--executed {path}: the top level has no {key!r}",
                KIND_EXECUTED_INPUT))
    for key in sorted(set(raw) - set(EXECUTED_KEYS)):
        problems.append(Problem(
            f"--executed {path}: unknown top-level key {key!r}; the schema "
            f"is exactly {', '.join(EXECUTED_KEYS)}", KIND_EXECUTED_INPUT))

    attempt = raw.get("attempt")
    if not isinstance(attempt, str) or not attempt:
        problems.append(Problem(
            f"--executed {path}: 'attempt' must be a non-empty string",
            KIND_EXECUTED_INPUT))
        attempt = None

    # THE ANCHOR IS SHIPPED, SO IT MUST BE SYMBOLIC. An absolute path in a
    # record that travels inside a reviewed package is a leak of the
    # assembling machine, which is the very thing the sealer rewrites.
    anchor = raw.get("anchor")
    if not isinstance(anchor, str) or not anchor:
        problems.append(Problem(
            f"--executed {path}: 'anchor' must be a non-empty string",
            KIND_EXECUTED_INPUT))
        anchor = None
    elif (anchor.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", anchor)
          or re.search(r"/home\b", anchor) or anchor.startswith("~")):
        problems.append(Problem(
            f"--executed {path}: 'anchor' is {anchor!r}, which is an absolute "
            f"or home-directory path; it must be the SANITIZED symbolic "
            f"anchor identity, because this record ships",
            KIND_EXECUTED_INPUT))

    runs: list[dict] = []
    given = raw.get("runs")
    if not isinstance(given, list):
        if "runs" in raw:
            problems.append(Problem(
                f"--executed {path}: 'runs' must be an array",
                KIND_EXECUTED_INPUT))
        given = []
    for number, one in enumerate(given, start=1):
        if not isinstance(one, dict):
            problems.append(Problem(
                f"--executed {path}: runs[{number}] is not an object",
                KIND_EXECUTED_INPUT))
            continue
        broken = False
        for key in RUN_KEYS:
            if not isinstance(one.get(key), str):
                problems.append(Problem(
                    f"--executed {path}: runs[{number}] has no string "
                    f"{key!r}", KIND_EXECUTED_INPUT))
                broken = True
        for key in sorted(set(one) - set(RUN_KEYS)):
            problems.append(Problem(
                f"--executed {path}: runs[{number}] carries the unknown key "
                f"{key!r}; a run row is exactly {', '.join(RUN_KEYS)}",
                KIND_EXECUTED_INPUT))
            broken = True
        if broken:
            continue
        if not one["tool"]:
            problems.append(Problem(
                f"--executed {path}: runs[{number}] names no tool",
                KIND_EXECUTED_INPUT))
            continue
        if one["class"] not in TOOL_CLASSES:
            problems.append(Problem(
                f"--executed {path}: runs[{number}] ({one['tool']}) has class "
                f"{one['class']!r}; it must be one of "
                f"{', '.join(TOOL_CLASSES)}", KIND_EXECUTED_INPUT))
            continue
        if one["sha256"] and not re.fullmatch(r"[0-9a-f]{64}", one["sha256"]):
            problems.append(Problem(
                f"--executed {path}: runs[{number}] ({one['tool']}) records "
                f"sha256 {one['sha256']!r}, which is neither empty nor 64 "
                f"lowercase hex characters", KIND_EXECUTED_INPUT))
            continue
        if one["class"] == CLASS_SHIPPED_EXECUTED and not one["sha256"]:
            problems.append(Problem(
                f"--executed {path}: runs[{number}] ({one['tool']}) is "
                f"{CLASS_SHIPPED_EXECUTED} with an empty sha256; the whole "
                f"point of this record is the digest taken immediately "
                f"before the invocation", KIND_EXECUTED_INPUT))
        if not AT_PATTERN.match(one["at"]):
            problems.append(Problem(
                f"--executed {path}: runs[{number}] ({one['tool']}) records "
                f"at {one['at']!r}, which is not an ISO-8601 instant with an "
                f"explicit offset or Z", KIND_EXECUTED_INPUT))
        if one["class"] == CLASS_EXTERNAL and one["path"]:
            problems.append(Problem(
                f"--executed {path}: runs[{number}] ({one['tool']}) is "
                f"{CLASS_EXTERNAL} but carries path {one['path']!r}; an "
                f"external system tool ships nothing, so its path is \"\"",
                KIND_EXECUTED_INPUT))
        runs.append({key: one[key] for key in RUN_KEYS})
    return {"runs": runs, "attempt": attempt, "anchor": anchor}, problems


def tool_table(shipped: dict[str, str | None], tools: Path,
               executed: dict | None
               ) -> tuple[list[dict], list[str], list[Problem], dict]:
    """Check 11: every shipped tool, classified, and compared THREE ways.

    The V12 mechanism was right and its coverage was three tools out of
    fifteen. The three legs are the digest captured AT EXECUTION by the
    assembler, the digest of the TRUSTED copy this verifier would run, and
    the digest of the copy the package SHIPPED. All present legs must be
    equal. Fewer than two legs is not a pass, it is an unprovable claim, and
    it is reported as a problem.

    Returns (rows for `--table-out`, transcript lines, problems).
    """
    have = executed is not None
    runs = (executed or {}).get("runs") or []

    by_tool: dict[str, list[dict]] = {}
    for one in runs:
        by_tool.setdefault(one["tool"], []).append(one)
    shipped_paths = {f"logs/{one}" for one in shipped}

    lines: list[str] = ["--- check 11 tool bytes, three ways "
                        "(executed / trusted / shipped)"]
    if have:
        lines.append(f"    execution record : attempt "
                     f"{(executed or {}).get('attempt') or '(unnamed)'}, "
                     f"anchor {(executed or {}).get('anchor') or '(unnamed)'}, "
                     f"{len(runs)} run row(s) over {len(by_tool)} tool(s)")
        lines.append("    EXECUTED-BYTE CLAIM: PROVED where an executed "
                     "digest is present and equal to the trusted and shipped "
                     "bytes")
    else:
        lines.append("    execution record : none supplied")
        lines.append("    EXECUTED-BYTE CLAIM: UNPROVEN -- no --executed "
                     "record was supplied, so this is a two-way shipped-vs-"
                     "trusted comparison and the bytes that RAN are not "
                     "proved to be the bytes that shipped")

    rows: list[dict] = []
    problems: list[Problem] = []
    for tool_id in sorted(set(shipped) | set(by_tool)):
        mine = by_tool.get(tool_id, [])
        shipped_digest = shipped.get(tool_id)
        is_shipped = tool_id in shipped
        trusted_path = tools / tool_id
        trusted_digest = digest(trusted_path) if trusted_path.is_file() else None
        row_problems: list[str] = []

        # THE MID-RUN BYTE CHANGE. Several rows for one tool are normal -- a
        # tool invoked at three phases gets three rows -- but they must all
        # name the same bytes, or the tool changed underneath the run and no
        # single digest describes what executed.
        recorded = {one["sha256"] for one in mine if one["sha256"]}
        executed_digest = next(iter(recorded)) if len(recorded) == 1 else None
        if len(recorded) > 1:
            row_problems.append(
                f"{tool_id} was executed as {len(recorded)} different byte "
                f"sequences across {len(mine)} run row(s) -- the bytes "
                f"changed mid-run: {', '.join(sorted(recorded))}")

        classes = {one["class"] for one in mine}
        if len(classes) > 1:
            row_problems.append(
                f"{tool_id} is recorded under {len(classes)} different "
                f"classes: {', '.join(sorted(classes))}")
            klass = CLASS_UNCLASSIFIED
        elif classes:
            klass = next(iter(classes))
        else:
            klass = CLASS_UNCLASSIFIED

        attempts = [one["attempt"] for one in mine]
        logs = [one["log"] for one in mine if one["log"]]
        declared_path = next((one["path"] for one in mine if one["path"]), "")
        logical = declared_path or (f"logs/{tool_id}" if is_shipped
                                    else "(external system tool)")
        # `executed` is a property of the CLASS, not of the row count: a
        # shipped-not-executed tool still gets a row, saying it did not run.
        ran = klass in (CLASS_SHIPPED_EXECUTED, CLASS_EXTERNAL)

        if have:
            if is_shipped and not mine:
                row_problems.append(
                    f"{tool_id} is shipped as logs/{tool_id} but --executed "
                    f"carries no run row for it: shipped, unclassified -- "
                    f"'deliberately not run' and 'we forgot to record it' "
                    f"must not be the same silence")
            for one in mine:
                if one["path"] and one["path"] not in shipped_paths:
                    row_problems.append(
                        f"{tool_id}: the run row at {one['at']} names path "
                        f"{one['path']}, which the package does not ship")
            if klass == CLASS_EXTERNAL and is_shipped:
                row_problems.append(
                    f"{tool_id} is recorded {CLASS_EXTERNAL} but the package "
                    f"ships logs/{tool_id}")
            if (klass in (CLASS_SHIPPED_EXECUTED, CLASS_SHIPPED_NOT_EXECUTED,
                          CLASS_REVIEWER_HELPER) and not is_shipped):
                row_problems.append(
                    f"{tool_id} is recorded {klass} but the package ships no "
                    f"logs/{tool_id}")

        if is_shipped and shipped_digest is None:
            row_problems.append(
                f"logs/{tool_id} does not decompress, so its shipped bytes "
                f"cannot be hashed or compared")

        # -- the comparison -----------------------------------------------
        # Only a `shipped-executed` row carries an executed digest that MUST
        # equal the other two. The other three classes are reported: their
        # digests, when present, are shown but never made a verdict.
        compare_executed = (klass == CLASS_SHIPPED_EXECUTED
                            and executed_digest is not None)
        present = {label: value for label, value in (
            ("executed", executed_digest if compare_executed else None),
            ("trusted", trusted_digest),
            ("shipped", shipped_digest)) if value}
        equal: bool | None
        if klass == CLASS_EXTERNAL or len(present) < 2:
            equal = None
        else:
            equal = len(set(present.values())) == 1
        if equal is False:
            row_problems.append(
                f"{tool_id}: the copies disagree -- "
                + "; ".join(f"{label} {value}"
                            for label, value in sorted(present.items())))
        if compare_executed and shipped_digest:
            for one in mine:
                if one["sha256"] and one["sha256"] != shipped_digest:
                    row_problems.append(
                        f"{tool_id}: the bytes executed in attempt "
                        f"{one['attempt'] or '(unnamed)'} at {one['at']} "
                        f"({one['phase'] or 'no phase'}) hash to "
                        f"{one['sha256']}, the shipped logs/{tool_id} hashes "
                        f"to {shipped_digest} -- what ran is not what shipped"
                        + (f" (evidence log {one['log']})" if one["log"]
                           else ""))
        if klass != CLASS_EXTERNAL and is_shipped and len(present) < 2:
            row_problems.append(
                f"{tool_id}: only {len(present)} copy is available "
                f"({', '.join(sorted(present)) or 'none'}), so no byte "
                f"comparison can be made and the claim is unproved")

        rows.append({
            "tool_id": tool_id,
            "logical_path": logical,
            "class": klass,
            "attempt": attempts[0] if len(set(attempts)) == 1 else None,
            "attempts": attempts,
            "executed": ran,
            "executed_recorded": have,
            "executed_sha256": executed_digest,
            "shipped_sha256": shipped_digest,
            "trusted_sha256": trusted_digest,
            "equal": equal,
            "evidence_log": logs[0] if len(set(logs)) == 1 else None,
            "evidence_logs": logs,
            "invocations": [dict(one) for one in mine],
            "problems": row_problems,
        })
        problems.extend(Problem(one, KIND_TOOL) for one in row_problems)

    width = max([len(one["tool_id"]) for one in rows] + [len("tool")])
    lines.append(f"    {'tool'.ljust(width)}  {'class':<20}  {'ran':<9}  "
                 f"{'equal':<7}  executed/trusted/shipped")
    for row in rows:
        ran = ("yes" if row["executed"]
               else ("no" if row["executed_recorded"] else "no record"))
        equal = ("yes" if row["equal"] is True
                 else ("NO" if row["equal"] is False else "n/a"))
        trio = "/".join((one or "--------")[:8] for one in (
            row["executed_sha256"], row["trusted_sha256"],
            row["shipped_sha256"]))
        lines.append(f"    {row['tool_id'].ljust(width)}  {row['class']:<20}  "
                     f"{ran:<9}  {equal:<7}  {trio}"
                     + (f"  {row['attempt']}" if row["attempt"] else ""))
    # TWO COUNTS, TWO NAMES, NEVER ONE NUMBER.
    #
    # V15, the V14 review. This block printed one line, `classes :
    # shipped-executed 4, shipped-not-executed 14`, over 18 unique TOOLS,
    # three lines below `assemble.sh`'s own `executed-tools: 16
    # shipped-executed, 11 shipped-not-executed`, which counted INVOCATION
    # ROWS. Both were true and neither said which it was, so a reader had two
    # tallies of the same word that could not both be right and no way to
    # reconcile them. A tool invoked eight times is one tool and eight
    # invocations; the two facts get two names here and in the table JSON,
    # and nothing anywhere prints a combined `N/M` label.
    tools_by_class: dict[str, int] = {}
    invocations_by_class: dict[str, int] = {}
    for row in rows:
        tools_by_class[row["class"]] = tools_by_class.get(row["class"], 0) + 1
        invocations_by_class[row["class"]] = (
            invocations_by_class.get(row["class"], 0) + len(row["invocations"]))
    counts = {
        "unique_tools": len(rows),
        "invocations": sum(len(row["invocations"]) for row in rows),
        "executed_tools": sum(1 for row in rows if row["executed"]),
        "executed_invocations": sum(len(row["invocations"]) for row in rows
                                    if row["executed"]),
        "tools_by_class": tools_by_class,
        "invocations_by_class": invocations_by_class,
    }

    def tally(counted: dict[str, int]) -> str:
        return ", ".join(f"{name} {count}"
                         for name, count in sorted(counted.items())) or "(none)"

    lines.append(f"    unique tools     : {counts['unique_tools']}"
                 f" ({counts['executed_tools']} executed)")
    lines.append(f"    invocations      : {counts['invocations']}"
                 f" ({counts['executed_invocations']} executed)")
    lines.append("    tools by class   : " + tally(tools_by_class))
    lines.append("    invocations/class: " + tally(invocations_by_class))
    return rows, lines, problems, counts


def trusted_provenance(tools: Path, expected_root: str,
                       accept_unversioned: bool = False
                       ) -> tuple[list[tuple[str, str]], list[Problem]]:
    """Where the trusted copies came from, said plainly — and whether that
    origin is anchored to anything at all.

    A path and a digest per tool are printed by `binding_report` at the
    checks themselves; this is the directory-level statement. The V12 version
    printed `(not a git checkout)` as a NOTE and moved on, which meant the
    ONE thing this run executes could be an unversioned, mutable directory of
    scripts and the transcript would still read as a pass. It is a PROBLEM
    now — the directory must be a git checkout, the tools must be TRACKED in
    it, and the tracked tools must be CLEAN — unless the operator passes
    `--accept-unversioned-tools`, which is recorded here in those words.

    `assemble.sh` runs this verifier out of the package STAGING tree's
    `logs/`, so by default the anchor is the tree the ZIP was built from.
    That is still outside the reviewed archive and it is still not executed
    archive bytes, but it is not an independent checkout, and a reviewer who
    wants one passes `--tools`.
    """
    binding = [("tools", str(tools))]
    problems: list[Problem] = []

    def git(*arguments: str) -> tuple[int, str]:
        try:
            done = subprocess.run(["git", "-C", str(tools), *arguments],
                                  capture_output=True, text=True, timeout=10)
        except (OSError, subprocess.SubprocessError):
            return 1, ""
        return done.returncode, done.stdout

    code, out = git("rev-parse", "HEAD")
    commit = out.strip() if code == 0 else ""
    binding.append(("tools at", commit or "(not a git checkout)"))

    reason = ""
    if not commit:
        reason = "not a git checkout"
    else:
        code, out = git("ls-files", "--", ".")
        if code != 0 or not out.strip():
            reason = "a git checkout, but this directory is untracked in it"
        else:
            code, out = git("status", "--porcelain", "--", ".")
            if code != 0:
                reason = "a git checkout whose status could not be read"
            elif out.strip():
                dirty = len([one for one in out.splitlines() if one.strip()])
                reason = (f"a git checkout with {dirty} uncommitted "
                          f"change(s) in this directory")
    if reason:
        binding.append(("anchor", f"UNVERSIONED -- {reason}"))
        if accept_unversioned:
            binding.append(("", "ACCEPTED by --accept-unversioned-tools: the "
                                "operator has accepted that the tools this "
                                "run EXECUTES are not anchored to a commit, "
                                "so the digests below name bytes that can "
                                "change without trace"))
        else:
            problems.append(Problem(
                f"the trusted tool anchor {tools} is unversioned ({reason}): "
                f"the only code this verification executes is not anchored "
                f"to any commit, so its digests name mutable bytes -- pass "
                f"--accept-unversioned-tools to accept this deliberately, or "
                f"point --tools at a clean, tracked checkout", KIND_ANCHOR))
    else:
        binding.append(("anchor", f"versioned and clean at {commit}"))

    staging = (tools.name == "logs"
               and (tools.parent / "claims.json").is_file())
    if staging:
        binding.append(("", f"NOTE: the trusted tools live in a package "
                            f"staging tree ({tools.parent.name}); they are "
                            f"outside the reviewed ZIP but not an "
                            f"independent checkout -- pass --tools DIR for "
                            f"one"))
    elif tools.name == expected_root or expected_root in tools.parts:
        binding.append(("", "NOTE: the trusted tools directory is named "
                            "after the package under review"))
    return binding, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--zip", type=Path, required=True, dest="archive")
    parser.add_argument("--sidecar", type=Path, default=None)
    parser.add_argument("--name", default=None,
                        help="expected package root inside the archive "
                             "(default: the ZIP's own stem)")
    parser.add_argument("--tools", type=Path, default=None,
                        help="the TRUSTED copies of the shared tools this "
                             "verification runs (default: the directory "
                             "holding this verifier). Never the archive.")
    parser.add_argument("--executed", type=Path, default=None,
                        help="JSON recording, per invocation, the sha256 of "
                             "the exact bytes each tool was executed as "
                             "(schema " + EXECUTED_SCHEMA + "; see the module "
                             "docstring). Without it the executed-byte claim "
                             "is reported UNPROVEN rather than passed.")
    parser.add_argument("--table-out", type=Path, default=None,
                        dest="table_out",
                        help="write the machine-readable tool byte table to "
                             "this path as JSON (schema " + TABLE_SCHEMA + ")")
    parser.add_argument("--accept-unversioned-tools", action="store_true",
                        dest="accept_unversioned",
                        help="accept a --tools anchor that is not a clean, "
                             "tracked git checkout. Without this an "
                             "unversioned anchor is a PROBLEM, not a note.")
    args = parser.parse_args(argv)

    # The transcript is read in order, and check 10's subprocesses write
    # straight to fd 2 while this process's `print` is block-buffered the
    # moment the transcript is redirected to a file. Without this, an
    # auditor's refusal appears ABOVE the header that names the archive.
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except (AttributeError, OSError):  # pragma: no cover -- exotic stdout
        pass

    archive = args.archive.resolve()
    if not archive.is_file():
        print(f"no such archive: {archive}", file=sys.stderr)
        return 2
    sidecar = args.sidecar or archive.with_name(archive.name + ".sha256")
    expected_root = args.name or archive.name.removesuffix(".zip")
    here = Path(__file__).resolve()
    tools = (args.tools.resolve() if args.tools else here.parent)

    # THE BINDING, before the first check: the digest is computed here, from
    # the archive bytes themselves, and the sidecar check receives it rather
    # than reading twice. These two values are also the PRE-CHECK pair the
    # rehash at the bottom compares against.
    pre_size = archive.stat().st_size
    pre_digest = digest(archive)
    identity, note = peek_identity(archive, expected_root)
    binding: list[tuple[str, str]] = [
        ("verifier", str(here)),
        ("verifier sha256", digest(here)),
    ]
    provenance, anchor_problems = trusted_provenance(
        tools, expected_root, args.accept_unversioned)
    binding += provenance
    executed: dict | None = None
    executed_problems: list[Problem] = []
    if args.executed is not None:
        executed, executed_problems = load_executed(args.executed.resolve())
        binding.append(("executed", f"{args.executed.resolve()} "
                                    f"({len(executed['runs'])} run row(s), "
                                    f"attempt "
                                    f"{executed['attempt'] or '(unnamed)'}, "
                                    f"anchor "
                                    f"{executed['anchor'] or '(unnamed)'})"))
    else:
        binding.append(("executed", "(none supplied -- the executed-byte "
                                    "claim will be reported UNPROVEN)"))
    if identity:
        binding += [
            ("head", identity["head"]),
            ("parent", identity["parent"]),
            ("review", identity["review"]),
            ("lane", f"{identity['lane']} (claims tool: {identity['tool']})"),
            ("claims", f"{identity['members']} frozen row(s), "
                       f"{identity['bytes']} byte(s), "
                       f"{identity['derived']} derived member(s), as "
                       f"claims.json declares"),
        ]
    else:
        binding.append(("head", f"(unavailable: {note})"))
    # Named again, under the labels the pre/post comparison uses, so the two
    # halves of that comparison read alike and neither can be mistaken for
    # the other.
    binding += [
        ("pre-check bytes", str(pre_size)),
        ("pre-check sha256", pre_digest),
    ]
    for line in identity_header(archive, expected_root, pre_digest, binding):
        print(line)

    failed: list[str] = []
    performed: list[str] = []
    skipped: list[str] = []

    def outcome(label: str, problems: list[str]) -> None:
        performed.append(label)
        print(f"[{label}] {'ok' if not problems else 'FAILED'}"
              + (f" -- {len(problems)} problem(s)" if problems else ""))
        for one in problems:
            print(f"    {one}")
        failed.extend(problems)

    def skip(label: str, reason: str) -> None:
        """A check that did not run says so, by name, with the reason.

        The V12 verifier's `BadZipFile` handler dropped checks 3 through 7
        without a word; the transcript then read as though a five-check
        package had been fully verified.
        """
        skipped.append(label)
        print(f"[{label}] SKIPPED -- {reason}")

    outcome("0 trust anchor",
            list(anchor_problems) + list(executed_problems))
    outcome("1 sidecar", check_sidecar(archive, sidecar, pre_digest))

    refused = False
    later = ["6 manifest", "7 claims rows", "8 partition", "9 rendering",
             "10 shipped audits"]
    try:
        handle = zipfile.ZipFile(archive)
    except (zipfile.BadZipFile, OSError) as error:
        outcome("2 layout", [Problem(f"the archive is not a readable ZIP "
                                     f"container: {error}", KIND_STRUCTURE)])
        for label in ["3 structure", "4 crc", "5 extraction", *later,
                      "11 tool bytes"]:
            skip(label, "the archive could not be opened as a ZIP")
    else:
        with handle:
            infos = handle.infolist()
            names = [one.filename for one in infos if not one.is_dir()]
            layout = check_layout(names, expected_root)
            outcome("2 layout", layout)

            structure_lines, structure_problems = check_structure(archive,
                                                                  infos)
            for line in structure_lines:
                print(line)
            outcome("3 structure", structure_problems)
            outcome("4 crc", check_crc(handle, infos))

            shipped = shipped_tool_digests(handle, expected_root)

            if unsafe_layout(layout):
                # A path that could escape the extraction directory is the one
                # problem that makes extracting unsafe; everything below needs
                # the extraction, so this is the single early exit. It is
                # decided on the problem's CLASS, not on its wording.
                print("REFUSING to extract an archive with escaping paths.",
                      file=sys.stderr)
                refused = True
                for label in ["5 extraction", *later]:
                    skip(label, "extraction was refused: the archive carries "
                                "a path that escapes the extraction directory")
            else:
                with tempfile.TemporaryDirectory() as scratch:
                    broken = None
                    try:
                        handle.extractall(scratch)
                    except (zipfile.BadZipFile, zlib.error, OSError, EOFError,
                            RuntimeError, ValueError,
                            NotImplementedError) as error:
                        broken = error
                    if broken is not None:
                        # NOT a layout problem. The V12 handler said `2 layout`
                        # here, a second time, and then dropped five checks.
                        outcome("5 extraction",
                                [Problem(f"the archive does not extract: "
                                         f"{broken}", KIND_EXTRACTION)])
                        for label in later:
                            skip(label, f"the archive does not extract "
                                        f"({type(broken).__name__})")
                    else:
                        outcome("5 extraction", [])
                        root = Path(scratch) / expected_root
                        if not root.is_dir():
                            outcome("6 manifest",
                                    [f"no {expected_root}/ directory in the "
                                     f"archive"])
                            for label in later[1:]:
                                skip(label, f"there is no {expected_root}/ "
                                            f"directory to check")
                        else:
                            outcome("6 manifest",
                                    check_manifest(root, infos, expected_root))
                            claims_path = root / "claims.json"
                            if not claims_path.is_file():
                                outcome("7 claims rows",
                                        ["the archive carries no claims.json"])
                                skip("8 partition",
                                     "the archive carries no claims.json")
                            else:
                                claims = json.loads(
                                    claims_path.read_text(encoding="utf-8"))
                                outcome("7 claims rows",
                                        check_claims_rows(claims, root))
                                outcome("8 partition",
                                        check_partition(claims, root))
                                for line in final_bytes(claims, root):
                                    print(line)
                            outcome("9 rendering", check_rendering(root, tools))
                            outcome("10 shipped audits",
                                    check_shipped_audits(root, tools))

            rows, table_lines, tool_problems, tool_counts = tool_table(
                shipped, tools, executed)
            for line in table_lines:
                print(line)
            outcome("11 tool bytes", tool_problems)

            if args.table_out is not None:
                table = {
                    "schema": TABLE_SCHEMA,
                    "generated": datetime.now(timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"),
                    "archive": {"name": archive.name, "bytes": pre_size,
                                "sha256": pre_digest},
                    "package": expected_root,
                    "trusted_tools": str(tools),
                    "executed_input": (str(args.executed.resolve())
                                       if args.executed is not None else None),
                    "executed_attempt": (executed or {}).get("attempt"),
                    "executed_anchor": (executed or {}).get("anchor"),
                    "executed_proof": ("proved" if executed is not None
                                       else "unproven"),
                    "problem_count": len(tool_problems),
                    # SEPARATELY NAMED, NEVER COMBINED. `unique_tools` counts
                    # tools; `invocations` counts run rows; the `*_by_class`
                    # maps say the same two things per class. V14 printed one
                    # ambiguous tally and a reader could not tell which.
                    "counts": tool_counts,
                    "rows": rows,
                }
                try:
                    args.table_out.write_text(
                        json.dumps(table, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
                    print(f"--- tool byte table written to "
                          f"{args.table_out} "
                          f"({tool_counts['unique_tools']} unique tool(s), "
                          f"{tool_counts['invocations']} invocation(s), "
                          f"schema {TABLE_SCHEMA})")
                except OSError as error:
                    print(f"--- tool byte table NOT written: {error}")
                    failed.append(f"could not write --table-out "
                                  f"{args.table_out}: {error}")

    # THE POST-CHECK REHASH. Everything above read the archive, extracted it,
    # and ran auditors over the extraction. This re-reads the archive itself
    # and proves the file did not move under the run: without it, the header's
    # digest describes the first read and nothing describes the last one.
    post_size = archive.stat().st_size
    post_digest = digest(archive)
    unchanged = (post_size == pre_size and post_digest == pre_digest)
    print("--- post-verification rehash of the archive bytes")
    print(f"    checks performed : "
          + (", ".join(performed) if performed else "(none)")
          + ("; extraction REFUSED after check 2" if refused else ""))
    print(f"    checks skipped   : "
          + (", ".join(skipped) if skipped else "(none)"))
    print(f"    pre-check bytes  : {pre_size}")
    print(f"    pre-check sha256 : {pre_digest}")
    print(f"    post-check bytes : {post_size}")
    print(f"    post-check sha256: {post_digest}")
    if unchanged:
        print("    result           : UNCHANGED -- every check above read "
              "the archive named in the header")
    else:
        print("    result           : CHANGED -- the archive moved during "
              "this verification")
        failed.append(f"the archive changed during verification: "
                      f"{pre_size} bytes/{pre_digest} before the checks, "
                      f"{post_size} bytes/{post_digest} after")

    print(f"P8 verification: {'PASS' if not failed else 'FAIL'} "
          f"({len(failed)} problem(s))")
    if failed:
        print("P8 VERIFICATION FAILED: the shipped archive does not prove "
              "its own claims.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
