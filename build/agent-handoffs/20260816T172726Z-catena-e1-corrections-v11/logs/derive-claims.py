#!/usr/bin/env python3
"""Derive every claim this package makes that a machine can derive.

WHY THIS EXISTS. The V6 package was mechanically intact and descriptively
untrue. Its manifest matched its directory, its ZIP matched its sidecar, its
privacy scan was clean — and `REVIEW_REQUEST.md` named `83cb63b61` as the exact
head of a package sealed for `4639b139f`, three members said 45 sealer tests
where 46 ran, one said four commits where five exist, one said three changed
files where six exist, and four said sixteen raster pairs where fifteen exist.
Every one of those numbers was available to a program at seal time and was
typed by a human instead, from memory, at a moment when the value had moved.

So this writes `claims.json`, and `claims.json` is the source. A number in the
prose of this package is either quoted FROM here, or it is a judgement a
machine cannot make and is labelled as one. `head-consistency.py` then reads
this file back and refuses to let the prose disagree with it.

Nothing here is specific to one correction round beyond its arguments: the
head, the parent and the package directory are all parameters, and no
filename, digest or count of this correction is written into the logic.

THE V9 CORRECTION: THE INVENTORY IS FROZEN, OR IT IS NOT AN INVENTORY. The V8
pipeline derived the package rows at step 9 of 14, and steps 9-11 then rewrote
five of the members those rows had already sized -- this file's own output
among them -- so the shipped inventory understated the final bytes and the
audit could only report the drift as residue. The governing invariant now:
every claimed (bytes, sha256) is computed strictly AFTER the last write of the
claimed bytes.

  * The rows come from the P3 FREEZE SNAPSHOT (`--freeze`), never from the
    live tree. `--write-freeze` is the P3 step that takes that snapshot.
  * A member written at or after this derivation is NAMED in
    `derived_members`, path plus reason, and is never sized or hashed. Rows
    and derived_members partition the final member set exactly, and the
    derivation refuses to run when they do not.
  * `claims.json` and `DERIVED-CLAIMS.md` are written PRE-NORMALIZED: the
    sanitizer's own substitution table is applied to this file's output before
    it lands, and a result the table would still touch is a hard failure. No
    later pass rewrites what this pass sized.
  * The package-total and final-byte authority is `MANIFEST.sha256` together
    with the ZIP and its sidecar -- not this file. This file sizes only what
    was frozen before it was written.

Usage:
    derive-claims.py --package DIR --write-freeze FILE
    derive-claims.py --repo REPO --parent SHA --head SHA --package DIR
                     --freeze FILE [--out claims.json]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

# This tool imports the sealer that ships beside it (see load_sealer), and an
# import writes bytecode. A `__pycache__` inside the package after the freeze
# is an undeclared member and the P5 audit hard-fails on it -- the dry run
# proved exactly that -- so no import made by this tool may write one.
sys.dont_write_bytecode = True

# THE LANE LABEL, rendered wherever a claim belongs to THIS correction round:
# the head test file replayed at the parent is this lane's file, and the
# classes it adds are this lane's classes. The V9 renderer hardcoded "V8" into
# V9 prose, which is a typed number wearing a derived one's clothes. The
# default is the constant; `--lane` overrides it.
LANE = "V10"


def git(repo: Path, *args: str) -> str:
    """One git invocation, its stdout, and a real error if it fails."""
    done = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)
    if done.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def digest(path: Path) -> str:
    hashed = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hashed.update(block)
    return hashed.hexdigest()


def gz(text: str) -> int:
    """gzip -9, mtime pinned to zero — the repository's own budget measure."""
    return len(gzip.compress(text.encode("utf-8"), 9, mtime=0))


def without_comments(text: str, *, script: bool = False) -> str:
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if script:
        stripped = re.sub(r"^\s*//.*$", "", stripped, flags=re.M)
    return stripped


def commits(repo: Path, parent: str, head: str) -> list[dict]:
    """Every commit of the range, with the files each one touches."""
    out = []
    listed = git(repo, "log", "--format=%H", f"{parent}..{head}").split()
    for sha in reversed(listed):
        subject = git(repo, "log", "-1", "--format=%s", sha).strip()
        when = git(repo, "log", "-1", "--format=%aI", sha).strip()
        files = git(repo, "show", "--name-only", "--format=", sha).split()
        out.append({"sha": sha, "subject": subject, "authored": when,
                    "files": sorted(files)})
    return out


def diffstat(repo: Path, parent: str, head: str) -> dict:
    """`--numstat`, summed — never a `--shortstat` line read by eye."""
    rows = []
    added = removed = 0
    for line in git(repo, "diff", "--numstat", f"{parent}..{head}").splitlines():
        if not line.strip():
            continue
        plus, minus, path = line.split("\t", 2)
        # A binary file reports `-`; none is expected here and one would show.
        rows.append({"path": path,
                     "added": None if plus == "-" else int(plus),
                     "removed": None if minus == "-" else int(minus)})
        if plus != "-":
            added += int(plus)
        if minus != "-":
            removed += int(minus)
    status = {}
    for line in git(repo, "diff", "--name-status", f"{parent}..{head}").splitlines():
        if line.strip():
            state, path = line.split("\t", 1)
            status[path] = state
    return {"files": len(rows), "insertions": added, "deletions": removed,
            "rows": sorted(rows, key=lambda one: one["path"]),
            "status": status}


BUDGETS = {
    "catena.css": {"whole": 8000, "stripped": 2700, "script": False},
    "catena.js": {"whole": 13000, "stripped": 8800, "script": True},
    # No ceiling by design; measured because the relocation's cost is a real
    # number a reader downloads, and V5 and V6 were both asked about it.
    "catena-model.js": {"whole": None, "stripped": None, "script": True},
}


def payload(repo: Path, ref: str) -> dict:
    """The gzip figures for one ref, read out of git rather than the tree.

    Reading the tree would measure whatever is checked out; reading the ref
    measures the commit the claim is about. The two agreed here, and only one
    of them says so by construction.
    """
    out = {}
    for name, budget in BUDGETS.items():
        blob = f"{ref}:src/web/browser/catena/{name}"
        try:
            text = git(repo, "show", blob)
        except SystemExit:
            out[name] = None
            continue
        out[name] = {
            "whole": gz(text),
            "whole_ceiling": budget["whole"],
            "stripped": gz(without_comments(text, script=budget["script"])),
            "stripped_ceiling": budget["stripped"],
            "source_bytes": len(text.encode("utf-8")),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
        # What share of the compressed file is explanation. V5 and V6 were
        # each asked whether the unbudgeted model carries too much of it and
        # neither answered; a question that keeps recurring deserves a number
        # rather than an impression, and a derived one rather than a typed.
        whole = out[name]["whole"]
        out[name]["comment_share"] = (
            round((whole - out[name]["stripped"]) / whole, 3) if whole else None)
    js = out.get("catena.js") or {}
    model = out.get("catena-model.js") or {}
    if js and model:
        page = git(repo, "show", f"{ref}:src/web/browser/catena/catena.js")
        both = git(repo, "show", f"{ref}:src/web/browser/catena/catena-model.js")
        out["_combined"] = {
            # Both measures, because neither alone is the load a reader pays.
            "one_stream": gz(page + both),
            "summed": js["whole"] + model["whole"],
        }
    return out


def battery_log(logs: Path, name: str) -> Path:
    """Resolve a battery log by its slug-and-side name.

    The battery prefixes every log with a monotonic per-battery index
    (`NN-name`) so no two ledger entries can share a path. This resolves the
    bare name back: a direct hit first (for members other tools write
    unprefixed), then the single indexed match. Two indexed matches would
    mean two runs claimed one name, and picking one silently is how a figure
    comes to describe the wrong run -- refusal.
    """
    direct = logs / name
    if direct.is_file():
        return direct
    found = sorted(logs.glob("[0-9][0-9]-" + name))
    if len(found) > 1:
        raise SystemExit(f"ambiguous battery log {name}: "
                         + ", ".join(one.name for one in found))
    return found[0] if found else direct


def suite_counts(log: Path) -> dict | None:
    """`Ran N tests`, the failure/error/skip counts, and the FAIL/ERROR set.

    Parsed from the log the run actually wrote, so a count in the prose can be
    traced to a line in a file rather than to somebody's recollection.
    """
    if not log.is_file():
        return None
    text = log.read_text(encoding="utf-8", errors="replace")
    ran = re.search(r"^Ran (\d+) tests? in ([\d.]+)s", text, re.M)
    outcome = re.search(r"^(OK|FAILED)(?:\s*\((.*)\))?\s*$", text, re.M)
    counts = {"failures": 0, "errors": 0, "skipped": 0,
              "expected failures": 0, "unexpected successes": 0}
    if outcome and outcome.group(2):
        for part in outcome.group(2).split(","):
            name, _, value = part.strip().rpartition("=")
            if name and value.isdigit():
                counts[name.strip()] = int(value)
    identities = sorted({
        line.strip() for line in text.splitlines()
        if line.startswith("FAIL: ") or line.startswith("ERROR: ")})
    return {
        "path": log.name,
        "tests": int(ran.group(1)) if ran else None,
        "seconds": float(ran.group(2)) if ran else None,
        "outcome": outcome.group(1) if outcome else None,
        "failures": counts["failures"],
        "errors": counts["errors"],
        "skipped": counts["skipped"],
        "identities": identities,
        "identity_count": len(identities),
    }


def gate_counts(report: Path) -> dict | None:
    """The browser gate's own JSON, reduced to the numbers the prose quotes."""
    if not report.is_file():
        return None
    data = json.loads(report.read_text(encoding="utf-8"))
    # `counts` is the gate's own tally; everything else here is derived from
    # the report's own lists so a count and its members cannot disagree.
    totals = dict(data.get("counts") or {})
    categories: dict[str, int] = {}
    for one in data.get("failures", []) or []:
        key = one.get("check") or one.get("id") or one.get("name") or "?"
        categories[key] = categories.get(key, 0) + 1
    return {
        "path": report.name,
        "totals": totals,
        "measured": {
            "assertions": len(data.get("assertions") or []),
            "failures": len(data.get("failures") or []),
            "pages": len(data.get("pages") or []),
            "routes": len(data.get("routes") or []),
            "states": len(data.get("states") or []),
        },
        "browser": data.get("chrome") or data.get("browser") or "",
        "failure_categories": dict(sorted(categories.items(),
                                          key=lambda kv: -kv[1])),
    }


TEST_FILES = ("tools/tests/test_catena_wave_1.py", "tools/tests/test_catena.py")


def oracles(repo: Path, parent: str, head: str, marker: str,
            parent_log: Path | None) -> dict:
    """The test delta, counted rather than remembered.

    Every figure the V6 package got wrong about its own tests is derived here:
    how many oracles were corrected and where they sit, which classes are new,
    and — the one the V6 roadmap contradicted its own evidence about — which
    classes actually fail at the parent and which do not. A class that does not
    fail at the parent is a real and reportable thing (a positive control, or
    an oracle over behaviour the parent already had right); asserting that they
    all fail is what made the V6 claim false.
    """
    def classes_in(ref: str) -> dict[str, set[str]]:
        found: dict[str, set[str]] = {}
        for name in TEST_FILES:
            try:
                text = git(repo, "show", f"{ref}:{name}")
            except SystemExit:
                continue
            found[name] = set(re.findall(r"^class (\w+)\(", text, re.M))
        return found

    before, after = classes_in(parent), classes_in(head)
    added: dict[str, list[str]] = {}
    for name in after:
        added[name] = sorted(after[name] - before.get(name, set()))

    corrected = []
    for name in TEST_FILES:
        try:
            text = git(repo, "show", f"{head}:{name}")
        except SystemExit:
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if marker not in line:
                continue
            owner = "?"
            for back in range(index, -1, -1):
                if re.match(r"^class ", lines[back]):
                    owner = lines[back].split("(")[0][len("class "):]
                    break
            # The lane that corrected THIS oracle, read from the marker's own
            # tag: a block V8 corrected stays V8's however many lanes follow.
            tagged = re.search(re.escape(marker) + r" \(([^)]+)\)", line)
            corrected.append({"file": name, "line": index + 1, "class": owner,
                              "lane": tagged.group(1) if tagged else "?"})

    by_lane: dict[str, int] = {}
    for one in corrected:
        by_lane[one["lane"]] = by_lane.get(one["lane"], 0) + 1
    out = {
        "marker": marker,
        "corrected_blocks": len(corrected),
        "corrected_sites": corrected,
        "corrected_classes": sorted({one["class"] for one in corrected}),
        "corrected_by_lane": dict(sorted(by_lane.items())),
        "classes_added": added,
        "classes_added_count": sum(len(one) for one in added.values()),
    }

    if parent_log and parent_log.is_file():
        text = parent_log.read_text(encoding="utf-8", errors="replace")
        identities = sorted({line.strip() for line in text.splitlines()
                             if line.startswith(("FAIL: ", "ERROR: "))})
        # The decomposition, held as its parts: methods run, methods failing
        # (a method with failing subtests counts once), controls passing, and
        # the subtest identities themselves. Collapsing these into one "fails
        # N ways across M classes" figure is what the V9 review refused.
        ran = re.search(r"^Ran (\d+) tests? in", text, re.M)
        methods_run = int(ran.group(1)) if ran else None
        failing_methods: set[str] = set()
        for one in identities:
            found = re.search(r"\(([\w.]+)\)", one)
            if found:
                failing_methods.add(found.group(1))
        failing: dict[str, int] = {}
        for one in identities:
            found = re.search(r"\(test_catena\w*\.(\w+)\.", one)
            if found:
                failing[found.group(1)] = failing.get(found.group(1), 0) + 1
        every_added = {one for names in added.values() for one in names}
        out["against_parent"] = {
            "log": parent_log.name,
            "methods_run": methods_run,
            "failing_methods": sorted(failing_methods),
            "failing_method_count": len(failing_methods),
            "passing_methods": (methods_run - len(failing_methods)
                                if methods_run is not None else None),
            "identities": len(identities),
            "subtest_identities": identities,
            "classes": len(failing),
            "failing_by_class": dict(sorted(failing.items())),
            "new_classes_that_fail": sorted(set(failing) & every_added),
            "pre_existing_classes_that_fail": sorted(set(failing) - every_added),
            # Stated, not rounded away: a new class that passes at the parent
            # is not a defect in the class, and V6's roadmap claim that every
            # one of them fails was contradicted by its own decomposition.
            "new_classes_that_do_not_fail": sorted(every_added - set(failing)),
        }
    return out


# The members this derivation and the phases after it write. NAMED, never
# sized: their bytes do not exist yet (or are still moving) when the rows are
# frozen, and a number for them here would be the V8 defect again. The paths
# and their reasons ship in claims.json, so the audit and the final verifier
# read the SAME declaration this file wrote rather than keeping a list by hand.
DERIVED_MEMBERS: tuple[tuple[str, str], ...] = (
    ("claims.json",
     "written by this derivation; it cannot inventory its own bytes"),
    ("DERIVED-CLAIMS.md",
     "rendered from claims.json in the same pass that writes it"),
    ("logs/derive-claims.log",
     "transcript of this derivation, written as the derivation prints"),
    ("logs/head-consistency.log",
     "transcript of the consistency audit, which runs after this derivation"),
    ("MANIFEST.sha256",
     "written by the manifest phase, after every other member is frozen"),
)


def freeze_rows(package: Path) -> list[dict]:
    """P3: (path, bytes, sha256) for every current member. THE snapshot.

    This is the only inventory input the derivation accepts. It is taken after
    the normalize fixpoint and before anything derived exists, so every row it
    carries describes bytes nothing in the pipeline will touch again.
    """
    rows = []
    for path in sorted(package.rglob("*")):
        if not path.is_file():
            continue
        rows.append({"path": path.relative_to(package).as_posix(),
                     "bytes": path.stat().st_size,
                     "sha256": digest(path)})
    return rows


def partition_problems(present: set[str], frozen: set[str],
                       derived: set[str]) -> list[str]:
    """The partition invariant, as refusals. rows and derived_members must
    split the member set exactly: nothing in both, nothing in neither."""
    problems = []
    for one in sorted(frozen & derived):
        problems.append(f"{one} is both a frozen row and a declared "
                        f"derived member")
    for one in sorted(present - frozen - derived):
        problems.append(f"{one} is in the package but in neither the frozen "
                        f"rows nor derived_members -- a placeholder, or an "
                        f"undeclared late write")
    for one in sorted(frozen - present):
        problems.append(f"{one} is a frozen row but is gone from the package")
    return problems


def package_members(rows: list[dict]) -> dict:
    """The package section: the FROZEN inventory, and the derived names.

    Every figure here sums the P3 snapshot. There is deliberately no package
    total: the authority for what the final package weighs is the manifest,
    the ZIP and its sidecar, which are computed after the last write.
    """
    screenshots = [one for one in rows
                   if one["path"].startswith("screenshots/")
                   and one["path"].endswith(".png")]
    befores = {one["path"].split("/")[-1][len("before--"):] for one in screenshots
               if one["path"].split("/")[-1].startswith("before--")}
    afters = {one["path"].split("/")[-1][len("after--"):] for one in screenshots
              if one["path"].split("/")[-1].startswith("after--")}
    return {
        "authority": "package totals and final bytes are proved by "
                     "MANIFEST.sha256, the ZIP and its .zip.sha256 sidecar; "
                     "this file sizes only members frozen before it was "
                     "written",
        "evidence_members": len(rows),
        "evidence_bytes": sum(one["bytes"] for one in rows),
        "rows": rows,
        "derived_members": [{"path": path, "reason": reason}
                            for path, reason in DERIVED_MEMBERS],
        # Counted, never remembered. Zero is a real answer and is reported as
        # one rather than left for prose to imply.
        "screenshots": {
            "png_count": len(screenshots),
            "raster_pairs": len(befores & afters),
            "unpaired": sorted((befores ^ afters)),
        },
    }


def load_sealer():
    """The sanitizer that ships beside this tool, as a module.

    Loaded so this derivation can apply the SAME substitution table the seal
    applies -- one table, two consumers -- rather than a re-implementation
    that would drift from it.
    """
    import importlib.util
    location = Path(__file__).resolve().with_name("sanitize-and-seal.py")
    spec = importlib.util.spec_from_file_location("sealer_for_derivation",
                                                  location)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load the sealer beside this tool: {location}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_once(text: str, sealer) -> str:
    """One full application of the sanitizer's substitution table."""
    for pattern, replacement in sealer.rules(sealer.identities(),
                                             sealer.repo_root()):
        text = pattern.sub(replacement, text)
    return text


def assert_normalized(text: str, sealer, what: str) -> None:
    """Refuse an output a later sanitizer pass would rewrite or flag.

    This is what PRE-NORMALIZED means: the member this derivation writes is
    already at the substitution table's fixpoint and carries no private token,
    so no pass after the freeze has any reason to touch it -- and if one
    would, that is a hard failure here, at derivation time, not residue for a
    reader to discover by comparing digests.
    """
    if normalized_once(text, sealer) != text:
        raise SystemExit(f"{what}: a sanitizer pass would still rewrite this "
                         f"output; refusing to write it")
    checks = sealer.forbidden(sealer.identities(), sealer.repo_root())
    for number, line in enumerate(text.splitlines(), start=1):
        for label, pattern in checks:
            if pattern.search(line):
                raise SystemExit(f"{what}:{number}: private token [{label}] "
                                 f"in this output; refusing to write it")


def byte_scan(package: Path, repo: Path, changed: list[str]) -> dict:
    """NUL, forbidden control bytes and invalid UTF-8, over both trees."""
    findings = []
    scanned = 0
    ALLOWED = {0x09, 0x0A}

    def look(path: Path, label: str) -> None:
        nonlocal scanned
        raw = path.read_bytes()
        scanned += 1
        if b"\x00" in raw:
            findings.append(f"{label}: NUL byte")
        if b"\r" in raw:
            findings.append(f"{label}: carriage return")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as error:
            findings.append(f"{label}: invalid UTF-8 ({error})")
            return
        for index, char in enumerate(text):
            point = ord(char)
            if (point < 0x20 and point not in ALLOWED) or point == 0x7F:
                findings.append(f"{label}: control U+{point:04X} at {index}")
                return

    for name in changed:
        path = repo / name
        if path.is_file():
            look(path, f"changed:{name}")
    if package.is_dir():
        for path in sorted(package.rglob("*")):
            if path.is_file() and path.suffix.lower() not in {".png", ".zip", ".gz"}:
                look(path, f"package:{path.relative_to(package).as_posix()}")
    return {"scanned": scanned, "findings": findings, "clean": not findings}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--parent")
    parser.add_argument("--head")
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--review", default="")
    parser.add_argument("--freeze", type=Path, default=None,
                        help="the P3 snapshot; the ONLY inventory input")
    parser.add_argument("--write-freeze", type=Path, default=None,
                        help="P3: snapshot the package inventory to FILE "
                             "and exit")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--lane", default=LANE,
                        help="the correction-lane label rendered on claims "
                             "this round owns (default: %(default)s)")
    args = parser.parse_args(argv)

    if args.write_freeze:
        rows = freeze_rows(args.package)
        args.write_freeze.write_text(
            json.dumps({"tool": "derive-claims.py", "rows": rows},
                       indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"freeze written: {args.write_freeze.name} "
              f"({len(rows)} member(s), "
              f"{sum(one['bytes'] for one in rows)} bytes)")
        return 0

    for required in ("repo", "parent", "head"):
        if not getattr(args, required):
            parser.error(f"--{required} is required for a derivation")
    if not args.freeze:
        parser.error("--freeze is required: the inventory is the P3 "
                     "snapshot, never the live tree")

    repo = args.repo.resolve()
    parent = git(repo, "rev-parse", args.parent).strip()
    head = git(repo, "rev-parse", args.head).strip()
    review = git(repo, "rev-parse", args.review).strip() if args.review else ""

    stat = diffstat(repo, parent, head)
    logs = args.package / "logs"

    # THE FREEZE, NOT THE TREE. The rows are read back from the P3 snapshot;
    # walking the live tree here is exactly what made the V8 inventory a
    # mid-pipeline reading. The partition is asserted before anything is
    # written: every live member is either a frozen row or a declared derived
    # member, and a frozen row that is also declared derived -- or a member
    # that is neither -- refuses the derivation.
    frozen_rows = json.loads(
        args.freeze.read_text(encoding="utf-8"))["rows"]
    present = {one.relative_to(args.package).as_posix()
               for one in sorted(args.package.rglob("*")) if one.is_file()}
    derived_paths = {path for path, _reason in DERIVED_MEMBERS}
    broken = partition_problems(present,
                                {one["path"] for one in frozen_rows},
                                derived_paths)
    if broken:
        for one in broken:
            print(f"PARTITION: {one}", file=sys.stderr)
        raise SystemExit("the frozen rows and derived_members do not "
                         "partition the member set; refusing to derive")

    claims = {
        "tool": "derive-claims.py",
        "lane": args.lane,
        "identity": {
            "parent": parent,
            "head": head,
            "review_addressed": review,
            # The exact ancestry claim, asserted rather than described.
            "parent_is_ancestor_of_head": subprocess.run(
                ["git", "-C", str(repo), "merge-base", "--is-ancestor",
                 parent, head]).returncode == 0,
            "worktree_clean_at_head": git(repo, "status", "--porcelain").strip() == "",
            "head_of_branch": git(repo, "rev-parse", "HEAD").strip(),
        },
        "commits": commits(repo, parent, head),
        "diff": stat,
        "payload": {"parent": payload(repo, parent), "head": payload(repo, head)},
        "suites": {
            # Named by the SLUG of the command that wrote them, resolved
            # through the battery's index prefix, so a reference in a
            # document resolves to the file without a mapping nobody
            # maintains.
            "focused_catena_head": suite_counts(
                battery_log(logs, "focused-catena-head.log")),
            "focused_catena_parent": suite_counts(
                battery_log(logs, "focused-catena-parent.log")),
            "full_discovery_head": suite_counts(
                battery_log(logs, "full-discovery-head.log")),
            "full_discovery_parent": suite_counts(
                battery_log(logs, "full-discovery-parent.log")),
            "browser_static_head": suite_counts(
                battery_log(logs, "browser-static-head.log")),
            "head_tests_against_parent": suite_counts(
                battery_log(logs, "head-tests-against-parent.log")),
            "sealer": suite_counts(battery_log(logs, "sealer-tests.log")),
        },
        "gate": {"head": gate_counts(battery_log(logs, "browser-gate-head.json")),
                 "parent": gate_counts(battery_log(logs, "browser-gate-parent.json"))},
        "package": package_members(frozen_rows),
        # The marker is the lane-agnostic prefix: each block's own tag names
        # the lane that corrected it, and the derivation reports them as
        # tagged rather than assuming they all belong to one round.
        "oracles": oracles(repo, parent, head, "CORRECTED ORACLE",
                           battery_log(logs, "head-tests-against-parent.log")),
    }
    claims["commit_count"] = len(claims["commits"])
    claims["byte_scan"] = byte_scan(args.package, repo,
                                    sorted(stat["status"]))

    # The identity SET comparison the baseline turns on: same names, whatever
    # the counts. Derived here so no document has to assert it by eye.
    head_full = claims["suites"]["full_discovery_head"]
    parent_full = claims["suites"]["full_discovery_parent"]
    if head_full and parent_full:
        claims["inherited_identities"] = {
            "identical": head_full["identities"] == parent_full["identities"],
            "count": head_full["identity_count"],
            "only_at_head": sorted(set(head_full["identities"])
                                   - set(parent_full["identities"])),
            "only_at_parent": sorted(set(parent_full["identities"])
                                     - set(head_full["identities"])),
            "mentioning_catena": sorted(
                one for one in head_full["identities"] if "catena" in one.lower()),
        }

    text = json.dumps(claims, indent=1, sort_keys=True, ensure_ascii=False) + "\n"
    if args.out:
        # PRE-NORMALIZED, so no later pass rewrites what this pass sized. The
        # sanitizer's own table is applied here -- the one place a substitution
        # may still land in this output -- and the result is asserted to be at
        # the table's fixpoint and token-free before a byte is written.
        sealer = load_sealer()
        text = normalized_once(text, sealer)
        assert_normalized(text, sealer, "claims.json")
        # The dict is re-read FROM the normalized record, so the rendering
        # below and any later re-render from the shipped claims.json start
        # from identical values -- byte-comparable by the final verifier.
        claims = json.loads(text)
        args.out.write_text(text, encoding="utf-8")
        # NAMED, not pathed. This line lands in a log inside the package, and
        # an absolute path there is a private token the sealer then has to
        # rewrite — which makes the seal's own idempotence claim untestable.
        print(f"claims written: {args.out.name} "
              f"({len(text.encode('utf-8'))} bytes)")
        # The same values, rendered for a reader, FROM THE SAME DICT. A prose
        # table typed beside a JSON file is two records of one fact and this
        # repository has been bitten by that pair disagreeing; emitting both
        # from one pass makes the disagreement unrepresentable. The rendering
        # of already-normalized values must itself already be normalized;
        # anything else would make the shipped page and a re-render disagree.
        body = render(claims)
        assert_normalized(body, sealer, "DERIVED-CLAIMS.md")
        page = args.out.with_name("DERIVED-CLAIMS.md")
        page.write_text(body, encoding="utf-8")
        print(f"rendering written: {page.name} "
              f"({page.stat().st_size} bytes)")
    else:
        sys.stdout.write(text)
    return 0


def render(claims: dict) -> str:
    """`claims.json`, as a reader meets it. Every figure comes from the dict."""
    identity = claims["identity"]
    out = ["# Derived claims",
           "",
           "**Every number in this file was computed by `logs/derive-claims.py`"
           " at seal time and written from the same pass that wrote"
           " `claims.json`.** Nothing here was typed. Where a document in this"
           " package states a figure, this is the source it states it from,"
           " and `logs/head-consistency.py` refuses a package whose prose"
           " names a commit these claims do not entitle it to name.",
           "",
           "## Identity",
           "",
           "| | |", "| --- | --- |",
           f"| parent | `{identity['parent']}` |",
           f"| head | `{identity['head']}` |",
           f"| review addressed | `{identity['review_addressed'] or '—'}` |",
           f"| parent is an ancestor of head |"
           f" {identity['parent_is_ancestor_of_head']} |",
           f"| working tree clean at head |"
           f" {identity['worktree_clean_at_head']} |",
           "",
           f"## Commits — {claims['commit_count']}",
           "",
           "| # | sha | subject | files |", "| --- | --- | --- | --- |"]
    for number, one in enumerate(claims["commits"], start=1):
        out.append(f"| {number} | `{one['sha']}` | {one['subject']} | "
                   + "<br>".join(f"`{f}`" for f in one["files"]) + " |")
    diff = claims["diff"]
    out += ["",
            f"## Diff — {diff['files']} file(s), "
            f"{diff['insertions']} insertion(s), {diff['deletions']} deletion(s)",
            "",
            "| state | path | + | − |", "| --- | --- | --- | --- |"]
    for row in diff["rows"]:
        out.append(f"| {diff['status'].get(row['path'], '?')} | `{row['path']}`"
                   f" | {row['added']} | {row['removed']} |")
    out += ["", "## Payload — gzip -9, mtime 0", "",
            "| file | parent whole | head whole | ceiling |"
            " parent stripped | head stripped | ceiling |"
            " parent comment share | head comment share |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for name in BUDGETS:
        before = (claims["payload"]["parent"] or {}).get(name) or {}
        after = (claims["payload"]["head"] or {}).get(name) or {}
        if not after:
            continue
        out.append(
            f"| `src/web/browser/catena/{name}` |"
            f" {before.get('whole', '—')} | {after['whole']} |"
            f" {after['whole_ceiling'] or 'none'} |"
            f" {before.get('stripped', '—')} | {after['stripped']} |"
            f" {after['stripped_ceiling'] or 'none'} |"
            f" {before.get('comment_share', '—')} | {after['comment_share']} |")
    combined_before = (claims["payload"]["parent"] or {}).get("_combined") or {}
    combined_after = (claims["payload"]["head"] or {}).get("_combined") or {}
    if combined_after:
        out += ["",
                "The page and the model together, because neither measure alone"
                " is the load a reader pays:",
                "",
                "| | parent | head | delta |", "| --- | --- | --- | --- |",
                f"| compressed as one stream | {combined_before.get('one_stream')}"
                f" | {combined_after['one_stream']} |"
                f" {combined_after['one_stream'] - combined_before.get('one_stream', 0):+} |",
                f"| compressed separately and summed |"
                f" {combined_before.get('summed')} | {combined_after['summed']} |"
                f" {combined_after['summed'] - combined_before.get('summed', 0):+} |"]
    oracle = claims.get("oracles") or {}
    lane = claims.get("lane") or "this lane"
    if oracle:
        by_lane = oracle.get("corrected_by_lane") or {}
        out += ["", "## Test delta", "", "| | |", "| --- | --- |",
                f"| `{oracle['marker']}` blocks |"
                f" {oracle['corrected_blocks']} |",
                f"| corrected blocks by marking lane | "
                + (", ".join(f"`{k}` {v}" for k, v in by_lane.items())
                   or "—") + " |",
                f"| classes holding a corrected oracle |"
                f" {len(oracle['corrected_classes'])} |",
                f"| test classes added |"
                f" {oracle['classes_added_count']} |",
                "",
                "Each block's marker tag names the lane that corrected it;"
                " nothing here assumes they all belong to one round.",
                "",
                "Classes holding a corrected oracle: "
                + ", ".join(f"`{one}`" for one in oracle["corrected_classes"])
                + "."]
        parent_run = oracle.get("against_parent")
        if parent_run:
            # SEPARATELY, NEVER COLLAPSED. The V9 page reduced this run to
            # "fails N identities across M classes", which averages a control
            # passing and an oracle failing into one number. Each part of the
            # decomposition is its own row, and the failing subtest
            # identities are listed rather than counted away.
            out += ["",
                    f"### The {lane} test file at the parent",
                    "",
                    f"The head's test file — the {lane} file — replayed"
                    f" against the PARENT's production files: same scenarios,"
                    f" same oracles, other code. The decomposition, reported"
                    f" separately:",
                    "",
                    "| | |", "| --- | --- |",
                    f"| methods run | {parent_run.get('methods_run', '—')} |",
                    f"| control methods passing at the parent |"
                    f" {parent_run.get('passing_methods', '—')} |",
                    f"| methods failing at the parent |"
                    f" {parent_run.get('failing_method_count', '—')} |",
                    f"| failing subtest identities |"
                    f" {parent_run['identities']} |",
                    f"| classes with a failure | {parent_run['classes']}"
                    f" ({len(parent_run['new_classes_that_fail'])} added by"
                    f" {lane},"
                    f" {len(parent_run['pre_existing_classes_that_fail'])}"
                    f" pre-existing with a corrected oracle) |",
                    "",
                    "Failing subtest identities at the parent:",
                    ""]
            for one in parent_run.get("subtest_identities") or []:
                out.append(f"- `{one}`")
            out += ["",
                    f"Classes {lane} adds that do **not** fail at the parent: "
                    + (", ".join(f"`{one}`" for one in
                                 parent_run["new_classes_that_do_not_fail"])
                       or "none")
                    + ". A class that passes at both ends closes a proof gap"
                      " rather than a defect, and saying otherwise is the"
                      " claim the V6 roadmap made against its own evidence."]
    out += ["", "## Suites", "",
            "| suite | tests | failures | errors | skips | outcome |"
            " FAIL/ERROR identities |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for name, one in sorted(claims["suites"].items()):
        if not one:
            out.append(f"| {name} | — | — | — | — | not run | — |")
            continue
        out.append(f"| {name} | {one['tests']} | {one['failures']} |"
                   f" {one['errors']} | {one['skipped']} | {one['outcome']} |"
                   f" {one['identity_count']} |")
    inherited = claims.get("inherited_identities")
    if inherited:
        out += ["",
                f"Full-discovery FAIL/ERROR identity sets at parent and head are"
                f" **{'identical' if inherited['identical'] else 'NOT identical'}**"
                f" — {inherited['count']} entries,"
                f" {len(inherited['only_at_head'])} only at the head,"
                f" {len(inherited['only_at_parent'])} only at the parent,"
                f" {len(inherited['mentioning_catena'])} mentioning catena."]
    gate = claims.get("gate") or {}
    if gate.get("head"):
        out += ["", "## Browser gate", "", "| | parent | head |",
                "| --- | --- | --- |"]
        keys = sorted(set((gate['head']['totals'] or {}))
                      | set((gate.get('parent') or {}).get('totals') or {}))
        out.append(f"| browser | {(gate.get('parent') or {}).get('browser', '—')}"
                   f" | {gate['head'].get('browser', '—')} |")
        for key in keys:
            out.append(f"| {key} |"
                       f" {((gate.get('parent') or {}).get('totals') or {}).get(key, '—')} |"
                       f" {gate['head']['totals'].get(key, '—')} |")
        if gate["head"]["failure_categories"]:
            out += ["", "Failure categories at the head: "
                    + ", ".join(f"`{k}` {v}" for k, v in
                                gate["head"]["failure_categories"].items()) + "."]
    package = claims["package"]
    shots = package["screenshots"]
    out += ["", "## Package", "",
            "The inventory below covers ONLY the members frozen before this"
            " file was written. A member written at or after the derivation is"
            " named under *derived members*, never sized or hashed: its bytes"
            " did not exist when the rows froze, and a number typed for it"
            " here would be the V8 defect this file corrects. The"
            " package-total and final-byte authority is `MANIFEST.sha256`"
            " together with the ZIP and its sidecar.",
            "",
            "| | |", "| --- | --- |",
            f"| evidence members (frozen) | {package['evidence_members']} |",
            f"| evidence bytes (sum of the rows) |"
            f" {package['evidence_bytes']} |",
            f"| derived members (named, unsized) |"
            f" {len(package['derived_members'])} |",
            f"| PNGs | {shots['png_count']} |",
            f"| before/after raster pairs | {shots['raster_pairs']} |",
            f"| unpaired captures | {len(shots['unpaired'])} |",
            "",
            "Derived members:",
            ""]
    for one in package["derived_members"]:
        out.append(f"- `{one['path']}` — {one['reason']}")
    out += ["",
            "## Byte and control scan", "",
            f"{claims['byte_scan']['scanned']} file(s) scanned for NUL,"
            f" carriage returns, forbidden control characters and invalid"
            f" UTF-8: **{'clean' if claims['byte_scan']['clean'] else 'FINDINGS'}**."]
    for one in claims["byte_scan"]["findings"]:
        out.append(f"- {one}")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    raise SystemExit(main())
