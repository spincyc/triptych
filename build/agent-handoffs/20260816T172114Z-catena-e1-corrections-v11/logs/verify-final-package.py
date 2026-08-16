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

READ-ONLY, AND NOW THAT IS TRUE OF THE CODE AS WELL AS THE BYTES. The V10
verifier called itself read-only while doing three things a reviewer would
not accept from an archive under review: it `exec_module`d the archive's own
`logs/derive-claims.py` in this process, and it ran the archive's own
`logs/head-consistency.py` and `logs/sanitize-and-seal.py` as subprocesses.
An archive that wants to pass could simply ship a renderer that returns the
page it shipped and an auditor that exits 0 — the verification would have
been performed BY the thing under verification. Nothing from inside the
reviewed ZIP is imported or executed here any more. The ZIP is opened as
data; members are read, hashed and compared.

WHERE THE SHARED LOGIC COMES FROM INSTEAD. Checks 6 and 7 genuinely need the
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

THE TRANSCRIPT IS BOUND TO THE ARCHIVE IT PROVES. Before the first check it
prints the ZIP's exact basename, byte size and sha256 — computed from the
archive bytes themselves, not read from the sidecar — the expected package
root, a UTC timestamp, THIS VERIFIER's own path and sha256 (it is outside the
archive, so it can hash itself), the trusted tool directory and each trusted
tool's digest, and the package's own identity (`identity.head`,
`identity.parent`, lane, declared member counts) read as JSON DATA out of the
ZIP — never by executing anything. The V9 transcript carried none of this, so
it would have read identically for any other archive whose sidecar happened
to agree with it. Seven checks, in order:

  1. SIDECAR.    The ZIP's sha256 AND its byte size against the recorded
                 sidecar values. Size too: a truncated download that happens
                 to collide on nothing is still not the artifact.
  2. LAYOUT.     Exactly one top-level root, equal to the package name; no
                 duplicate entries, no absolute paths, no `..` segments.
                 Problems are typed (`Problem.kind`), and only the
                 `unsafe-path` class stops the run — a substring test over
                 English prose used to decide that, and fired on any
                 duplicate entry whose filename merely contained "path".
  3. MANIFEST.   The extracted set minus `MANIFEST.sha256` equals the
                 manifest rows, and every digest matches. A path listed twice
                 in the manifest is a named failure — independent of the
                 duplicate-archive-entry check in 2, because a duplicate row
                 collapses silently into a dict and then proves half of what
                 it appears to.
  4. ROWS.       Every `claims.json` row matches the extracted member's bytes
                 and sha256, `evidence_bytes` is their sum and
                 `evidence_members` their count. A path frozen twice is a
                 named failure here for the same reason as in 3. A row that
                 fails otherwise is the V8 defect: a size claimed before the
                 last write.
  5. PARTITION.  rows ∪ derived_members is exactly the member set, the
                 intersection is empty, and no derived member carries a size
                 or digest — named, never sized, is the contract.
  6. RENDERING.  `DERIVED-CLAIMS.md` re-rendered from the extracted
                 `claims.json` by the TRUSTED renderer, byte-compared; and
                 the archive's renderer byte-compared against the trusted one.
  7. AUDITS.     The TRUSTED `head-consistency.py` and the TRUSTED
                 sanitizer's `--check-only`, re-run over the extraction, both
                 clean; and both archive copies byte-compared against the
                 trusted ones.

Between checks 5 and 6 the transcript prints the final-byte arithmetic,
derived from the extraction alone: the final member count, each derived
member's final byte size and their sum, the frozen-rows byte total, and the
total uncompressed bytes — so the transcript itself carries the figures the
V9 verifier left for a reader to compute.

AND THEN IT READS THE ARCHIVE AGAIN. After every check has run, the ZIP's
byte size and sha256 are recomputed from the file on disk and compared with
the values captured before the first check. Both pairs are printed under
explicit `pre-check` / `post-check` labels together with the list of checks
that ran between them, and a difference is a hard failure. A verifier that
hashes once at the top has proved something about the bytes it read at the
top; this proves the run as a whole examined one unchanging artifact.

Every check runs even after an earlier one fails, so one transcript names
every problem rather than the first. Nothing here writes anywhere except a
temporary extraction directory that is removed on exit; running it twice on
the same ZIP is the same run twice, which a reviewer can and should confirm
(the header's timestamp is the one line that moves).

Usage:
    verify-final-package.py --zip PACKAGE.zip [--sidecar PACKAGE.zip.sha256]
                            [--name PACKAGE_NAME] [--tools TRUSTED_DIR]
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

# This process imports the TRUSTED renderer (check 6) from the tools
# directory, and an import that writes bytecode would leave a `__pycache__`
# beside a tool this run is supposed to leave untouched. The subprocesses of
# check 7 do not inherit this flag, so they are launched with `-B` and
# `PYTHONDONTWRITEBYTECODE=1` explicitly.
sys.dont_write_bytecode = True

MANIFEST_NAME = "MANIFEST.sha256"

# The shared logic checks 6 and 7 need, by filename. Each is resolved in the
# TRUSTED tools directory and compared against `logs/<name>` in the archive.
RENDERER = "derive-claims.py"
AUDITORS = ("head-consistency.py", "sanitize-and-seal.py")

# A `claims.json` read straight out of the ZIP is untrusted input read as
# data; a cap keeps a hostile member from being decompressed into memory.
PEEK_LIMIT = 1 << 24


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


def check_manifest(root: Path) -> list[str]:
    """Check 3: extracted set minus the manifest == the manifest, digest by
    digest. This is what `--verify` already proved of the TREE; here it is
    proved of what the ZIP actually delivered."""
    problems: list[str] = []
    target = root / MANIFEST_NAME
    if not target.is_file():
        return [f"the archive carries no {MANIFEST_NAME}"]
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
    for one in sorted(set(listed) - present):
        problems.append(f"manifest lists {one}, which the archive omits")
    for one in sorted(present - set(listed) - {MANIFEST_NAME}):
        problems.append(f"archive carries {one}, which the manifest does "
                        f"not list")
    for one in sorted(set(listed) & present):
        if digest(root / one) != listed[one]:
            problems.append(f"digest mismatch against the manifest: {one}")
    return problems


def check_claims_rows(claims: dict, root: Path) -> list[str]:
    """Check 4: every frozen row against the delivered bytes. A failing row is
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
    """Check 5: rows ∪ derived_members is the member set, exactly, and a
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
    """Check 6: the renderer, over the shipped claims, must reproduce the
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
    print("--- check 6 trust anchor")
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
    """Check 7: the package's own auditors, replayed over the extraction —
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
    print("--- check 7 trust anchors")
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


def trusted_provenance(tools: Path, expected_root: str) -> list[tuple[str, str]]:
    """Where the trusted copies came from, said plainly.

    A path and a digest per tool are printed by `binding_report` at the
    checks themselves; this is the directory-level statement, plus the git
    commit of the checkout that holds it when there is one, plus the one
    caveat that matters: `assemble.sh` runs this verifier out of the package
    STAGING tree's `logs/`, so by default the anchor is the tree the ZIP was
    built from. That is still outside the reviewed archive and it is still
    not executed archive bytes, but it is not an independent checkout, and a
    reviewer who wants one passes `--tools`.
    """
    binding = [("tools", str(tools))]
    try:
        done = subprocess.run(
            ["git", "-C", str(tools), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10)
        commit = done.stdout.strip() if done.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        commit = ""
    binding.append(("tools at", commit or "(not a git checkout)"))
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
    return binding


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
    args = parser.parse_args(argv)

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
    binding += trusted_provenance(tools, expected_root)
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

    def outcome(label: str, problems: list[str]) -> None:
        performed.append(label)
        print(f"[{label}] {'ok' if not problems else 'FAILED'}"
              + (f" -- {len(problems)} problem(s)" if problems else ""))
        for one in problems:
            print(f"    {one}")
        failed.extend(problems)

    refused = False
    outcome("1 sidecar", check_sidecar(archive, sidecar, pre_digest))

    try:
        with zipfile.ZipFile(archive) as handle:
            names = [one.filename for one in handle.infolist()
                     if not one.is_dir()]
            layout = check_layout(names, expected_root)
            outcome("2 layout", layout)
            if unsafe_layout(layout):
                # A path that could escape the extraction directory is the one
                # problem that makes extracting unsafe; everything below needs
                # the extraction, so this is the single early exit. It is
                # decided on the problem's CLASS, not on its wording.
                print("REFUSING to extract an archive with escaping paths.",
                      file=sys.stderr)
                refused = True
            else:
                with tempfile.TemporaryDirectory() as scratch:
                    handle.extractall(scratch)
                    root = Path(scratch) / expected_root
                    if not root.is_dir():
                        outcome("3 manifest",
                                [f"no {expected_root}/ directory in the "
                                 f"archive"])
                    else:
                        outcome("3 manifest", check_manifest(root))
                        claims_path = root / "claims.json"
                        if not claims_path.is_file():
                            outcome("4 claims rows",
                                    ["the archive carries no claims.json"])
                        else:
                            claims = json.loads(
                                claims_path.read_text(encoding="utf-8"))
                            outcome("4 claims rows",
                                    check_claims_rows(claims, root))
                            outcome("5 partition",
                                    check_partition(claims, root))
                            for line in final_bytes(claims, root):
                                print(line)
                        outcome("6 rendering", check_rendering(root, tools))
                        outcome("7 shipped audits",
                                check_shipped_audits(root, tools))
    except zipfile.BadZipFile as error:
        outcome("2 layout", [f"archive unreadable: {error}"])

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
