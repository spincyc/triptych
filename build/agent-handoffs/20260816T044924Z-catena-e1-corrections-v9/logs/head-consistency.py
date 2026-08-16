#!/usr/bin/env python3
"""Refuse a package whose prose disagrees with its own derived claims.

THE DEFECT THIS ANSWERS. The V6 package's `REVIEW_REQUEST.md` opened with
"Exact head `83cb63b61e366fac07b298fee77f63d1658086f7`" while every other
member, the manifest and the evidence commit named `4639b139f…`. Nothing
checked, because nothing could: the head was prose in one file and prose in
another, and prose does not compare itself.

`claims.json` makes the comparison possible, and this makes it happen. Three
questions, over every text member of the package:

  1. IDENTITY. Every 40-hex string that looks like a full commit SHA must be
     one this package is entitled to name — the head, the parent, the review
     it answers, or a commit of the range between parent and head. A stale
     head from a superseded round is the exact V6 failure and is a finding
     here. Abbreviated SHAs are checked the same way, by prefix.

  2. INVERSION. A member that names the head and the parent must not name them
     the other way about. Any line carrying the word `parent` beside the head
     SHA, or `head` beside the parent SHA, is reported for a reader to judge.

  3. REFERENCE. Every package-relative path a member names must exist, and
     every member must be named by something — the V6 pair audit recorded
     thirty-two paths under a `shots/` directory the package does not have.

Nothing here knows anything about one correction round. The head, the parent
and the review come from `claims.json`; the members come from the directory;
and no filename or digest of this correction appears in the logic.

THE V9 CORRECTION: RESIDUE IS EITHER DECLARED OR IT IS A FAILURE. The V8 run
of this audit found members written after the inventory and members whose
bytes had moved after it, and PRINTED them, informationally, undercounted --
three named where five had moved. That reading was wrong twice over: it let
the pipeline rewrite sized members, and it made a reader responsible for
deciding whether the drift mattered. Under the frozen-inventory protocol the
question has a mechanical answer. `claims.json` sizes only members frozen
before it was written and NAMES everything later in `derived_members`, so:

  * a member OUTSIDE derived_members whose bytes differ from its frozen row
    -- or that carries no row at all -- is a HARD FAILURE, exit nonzero;
  * the residue set (present members without rows) must equal the declared
    derived_members exactly, minus only members named by `--pending`, which
    the pipeline passes for members a LATER phase writes (the manifest);
  * a derived_members entry that carries bytes or a digest is itself a
    failure: naming was the whole point, and sizing it would recreate the
    defect under a new key.

Usage:
    head-consistency.py --package DIR [--claims claims.json]
                        [--pending PATH ...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

FULL_SHA = re.compile(r"\b[0-9a-f]{40}\b")
# An abbreviated SHA must contain at least one hex LETTER. A run of seven or
# more digits is a byte count, a line number or a test total — `1,222,521`
# without its separators is not a commit — and flagging those buries the
# finding that matters under arithmetic.
SHORT_SHA = re.compile(r"\b(?=[0-9a-f]{7,39}\b)[0-9a-f]*[a-f][0-9a-f]*\b")
# A package-relative reference: `logs/x.log`, `screenshots/y.png`, `claims.json`.
# `MANIFEST.sha256` is named explicitly rather than by a `.sha256` alternative,
# which matched `hashlib.sha256` in source.
REFERENCE = re.compile(
    r"(?<![\w/.-])((?:logs|screenshots)/[\w.-]+"
    r"|MANIFEST\.sha256|[\w-]+\.(?:json|txt|patch|md))")

# The reference audit reads DOCUMENTS. A tool's source names its own test
# fixtures — `logs/run.txt`, `logs/before--viewport.png` — and those are
# literals inside a program, not claims about this package's contents. The
# identity and inversion checks still read every text member, because a stale
# head SHA in a shipped script is exactly the V6 defect.
DOCUMENT_SUFFIXES = {".md"}

# The IDENTITY audit reads the CLAIM-BEARING members: the documents, and the
# three git-derived records. It does not read source or patches. A `.patch`
# carries `index <blob>..<blob>` lines that are object ids and not commits, and
# a tool's tests carry digest literals of their own fixtures; neither is a
# claim about which head this package was sealed for, and treating them as one
# buries the finding that matters under dozens that do not.
CLAIM_BEARING = {".md"}
CLAIM_BEARING_NAMES = {"checks.txt", "commits.txt", "changed-files.txt"}

TEXT_SUFFIXES = {".md", ".txt", ".json", ".patch", ".py", ".sh", ".mjs",
                 ".sha256", ".js"}


def members(package: Path) -> list[Path]:
    return sorted(one for one in package.rglob("*") if one.is_file())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--claims", type=Path, default=None)
    parser.add_argument("--pending", action="append", default=[],
                        metavar="PATH",
                        help="a declared derived member a LATER phase writes; "
                             "its absence is expected here (repeatable)")
    args = parser.parse_args(argv)

    package = args.package.resolve()
    claims_path = args.claims or (package / "claims.json")
    claims = json.loads(claims_path.read_text(encoding="utf-8"))

    identity = claims["identity"]
    head = identity["head"]
    parent = identity["parent"]
    review = identity.get("review_addressed") or ""
    # Every SHA this package may name, and the reason it may.
    entitled = {head: "head", parent: "parent"}
    if review:
        entitled[review] = "review addressed"
    for one in claims["commits"]:
        entitled.setdefault(one["sha"], "commit in range")
    # And the commits this package DISCUSSES rather than was produced from,
    # declared one at a time with a reason. The default is refusal: an
    # undeclared SHA in a claim-bearing member is the V6 defect and fails here.
    declared = package / "logs" / "named-commits.json"
    if declared.is_file():
        for sha, why in json.loads(
                declared.read_text(encoding="utf-8"))["commits"].items():
            entitled.setdefault(sha, "declared: " + why)

    # PATHS OF THE REPOSITORY, NOT OF THE PACKAGE. A changed file at the
    # repository ROOT — `PROJECT-WORK.md`, `promised-deliverables.toml` — looks
    # exactly like a package reference and is not one. The package's own
    # changed-file record names precisely that set, by construction, so it is
    # read rather than a list of names being kept here by hand.
    outside: set[str] = set()
    changed = package / "changed-files.txt"
    if changed.is_file():
        for line in changed.read_text(encoding="utf-8").splitlines():
            if re.match(r"^[A-Z]\d*\t", line):
                outside.update(one.strip() for one in line.split("\t")[1:] if one.strip())

    problems: list[str] = []
    present = {one.relative_to(package).as_posix() for one in members(package)}
    referenced: set[str] = set()
    scanned = 0

    # The frozen inventory and the declared residue, read up front: the
    # reference audit below needs to know that a document may name a declared
    # derived member that a later phase writes (`--pending`).
    package_claims = claims["package"]
    inventory = {one["path"]: one for one in package_claims["rows"]}
    derived_rows = package_claims.get("derived_members") or []
    derived = {one["path"] for one in derived_rows}
    pending = set(args.pending)

    for path in members(package):
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(package).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{relative}: not UTF-8 text")
            continue
        scanned += 1
        claiming = (path.suffix.lower() in CLAIM_BEARING
                    or relative in CLAIM_BEARING_NAMES)

        for number, line in enumerate(text.splitlines(), start=1):
            if not claiming:
                continue
            # 1. IDENTITY.
            for found in FULL_SHA.findall(line):
                if found not in entitled:
                    problems.append(
                        f"{relative}:{number}: names {found}, which is not the "
                        f"head, the parent, the review, or a commit of the range")
            for found in SHORT_SHA.findall(line):
                if found in entitled or len(found) < 7:
                    continue
                if not any(one.startswith(found) for one in entitled):
                    problems.append(
                        f"{relative}:{number}: names abbreviated {found}, which "
                        f"prefixes no commit this package may name")

            # 2. INVERSION.
            low = line.lower()
            if "parent" in low and head[:12] in line and parent[:12] not in line:
                problems.append(
                    f"{relative}:{number}: calls the HEAD a parent")
            if re.search(r"\bhead\b", low) and parent[:12] in line and head[:12] not in line:
                problems.append(
                    f"{relative}:{number}: calls the PARENT a head")

            # 3. REFERENCE — documents only; see DOCUMENT_SUFFIXES.
            for found in ([] if path.suffix.lower() not in DOCUMENT_SUFFIXES
                          else REFERENCE.findall(line)):
                if found in outside:
                    continue
                referenced.add(found)
                if (found not in present
                        and not found.endswith(".zip.sha256")
                        and found not in (derived & pending)):
                    problems.append(
                        f"{relative}:{number}: names {found}, which the package "
                        f"does not contain")

    # THE FREEZE AUDIT. V8 printed what follows as informational residue and
    # undercounted it; under the frozen-inventory protocol every line of it is
    # a refusal. The rows sized at P3 and the derived_members named at P4 must
    # partition the member set: a frozen member whose bytes moved, a member in
    # neither set, a member in both, or a declared derived member that never
    # arrived (and is not `--pending` for a later phase) each fails the audit.
    inventoried = set(inventory)
    for one in sorted(pending - derived):
        problems.append(f"--pending names {one}, which derived_members does "
                        f"not declare")
    for one in derived_rows:
        extra = sorted(set(one) - {"path", "reason"})
        if extra:
            problems.append(
                f"derived member {one.get('path', '?')} carries "
                f"{', '.join(extra)}: derived members are named, never sized "
                f"or hashed")
    for one in sorted(inventoried & derived):
        problems.append(f"{one} is both a frozen row and a declared derived "
                        f"member")
    vanished = sorted(inventoried - present)
    for one in vanished:
        problems.append(f"claims.json inventories {one}, which is gone")
    undeclared = sorted(present - inventoried - derived)
    for one in undeclared:
        problems.append(f"{one} was written after the freeze without a "
                        f"derived_members declaration")
    never_arrived = sorted(derived - present - pending)
    for one in never_arrived:
        problems.append(f"derived member {one} is declared but was never "
                        f"written (and is not --pending)")
    drifted = []
    for relative in sorted(inventoried & present):
        path = package / relative
        row = inventory[relative]
        if (path.stat().st_size != row["bytes"]
                or hashlib.sha256(path.read_bytes()).hexdigest()
                != row["sha256"]):
            drifted.append(relative)
    for one in drifted:
        problems.append(f"frozen member {one} drifted after the freeze")
    residue = sorted(present - inventoried)

    unreferenced = sorted(present - referenced - {"MANIFEST.sha256"})
    for one in unreferenced:
        problems.append(f"unreferenced member: {one}")

    print(f"head consistency: {scanned} text member(s) scanned")
    print(f"  entitled SHAs: " + ", ".join(
        f"{sha[:12]} ({why})" for sha, why in sorted(entitled.items(),
                                                     key=lambda kv: kv[1])))
    print(f"  package members: {len(present)}; referenced: "
          f"{len(referenced & present)}; unreferenced: {len(unreferenced)}")
    print(f"  frozen rows in claims.json: {len(inventoried)}; declared "
          f"derived members: {len(derived)}; pending: {len(pending)}")
    print(f"  residue (present without a frozen row): {len(residue)}"
          + (" (" + ", ".join(residue) + ")" if residue else "")
          + " -- every one must be a declared derived member")
    print(f"  frozen members that drifted: {len(drifted)}"
          + (" (" + ", ".join(drifted) + ")" if drifted else ""))
    print(f"  problems: {len(problems)}")
    for one in problems:
        print("    " + one)
    if problems:
        print("HEAD CONSISTENCY FAILED", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
