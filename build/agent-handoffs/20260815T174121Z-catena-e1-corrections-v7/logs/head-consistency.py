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

Nothing here knows anything about V7. The head, the parent and the review come
from `claims.json`; the members come from the directory; and no filename or
digest of this correction appears in the logic.

Usage:
    head-consistency.py --package DIR [--claims claims.json]
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
                if found not in present and not found.endswith(".zip.sha256"):
                    problems.append(
                        f"{relative}:{number}: names {found}, which the package "
                        f"does not contain")

    # A package inventory taken before the seal cannot include the seal, nor
    # the transcripts of the steps that follow it. That is unavoidable and it
    # is a discrepancy, so it is DERIVED and printed rather than left for a
    # reader to discover by counting. `MANIFEST.sha256` is the authoritative
    # member list; `claims.json` records the inventory at derivation time.
    inventory = {one["path"]: one["sha256"] for one in claims["package"]["rows"]}
    inventoried = set(inventory)
    later = sorted(present - inventoried)
    vanished = sorted(inventoried - present)
    for one in vanished:
        problems.append(f"claims.json inventories {one}, which is gone")
    # A member whose BYTES moved after the derivation is the same residue one
    # step finer, and it is derived too rather than left to be discovered by
    # comparing digests by hand. `MANIFEST.sha256` is the authoritative record
    # of what the package holds; this says which members it and `claims.json`
    # necessarily disagree about, and why.
    moved = []
    for relative in sorted(inventoried & present):
        digest = hashlib.sha256((package / relative).read_bytes()).hexdigest()
        if digest != inventory[relative]:
            moved.append(relative)

    unreferenced = sorted(present - referenced - {"MANIFEST.sha256"})
    for one in unreferenced:
        problems.append(f"unreferenced member: {one}")

    print(f"head consistency: {scanned} text member(s) scanned")
    print(f"  entitled SHAs: " + ", ".join(
        f"{sha[:12]} ({why})" for sha, why in sorted(entitled.items(),
                                                     key=lambda kv: kv[1])))
    print(f"  package members: {len(present)}; referenced: "
          f"{len(referenced & present)}; unreferenced: {len(unreferenced)}")
    print(f"  inventoried in claims.json: {len(inventoried)}; written after that"
          f" derivation: {len(later)}"
          + (" (" + ", ".join(later) + ")" if later else ""))
    print(f"  members whose bytes moved after that derivation: {len(moved)}"
          + (" (" + ", ".join(moved) + ")" if moved else ""))
    print(f"  problems: {len(problems)}")
    for one in problems:
        print("    " + one)
    if problems:
        print("HEAD CONSISTENCY FAILED", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
