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

Nothing here is specific to V7 beyond its arguments: the head, the parent and
the package directory are all parameters, and no filename, digest or count of
this correction is written into the logic.

Usage:
    derive-claims.py --repo REPO --parent SHA --head SHA --package DIR
                     [--out claims.json]
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
            corrected.append({"file": name, "line": index + 1, "class": owner})

    out = {
        "marker": marker,
        "corrected_blocks": len(corrected),
        "corrected_sites": corrected,
        "corrected_classes": sorted({one["class"] for one in corrected}),
        "classes_added": added,
        "classes_added_count": sum(len(one) for one in added.values()),
    }

    if parent_log and parent_log.is_file():
        text = parent_log.read_text(encoding="utf-8", errors="replace")
        identities = sorted({line.strip() for line in text.splitlines()
                             if line.startswith(("FAIL: ", "ERROR: "))})
        failing: dict[str, int] = {}
        for one in identities:
            found = re.search(r"\(test_catena\w*\.(\w+)\.", one)
            if found:
                failing[found.group(1)] = failing.get(found.group(1), 0) + 1
        every_added = {one for names in added.values() for one in names}
        out["against_parent"] = {
            "log": parent_log.name,
            "identities": len(identities),
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


def package_members(package: Path) -> dict:
    """Every member, its size and its digest — the inventory, counted."""
    rows = []
    for path in sorted(package.rglob("*")):
        if not path.is_file():
            continue
        rows.append({"path": path.relative_to(package).as_posix(),
                     "bytes": path.stat().st_size,
                     "sha256": digest(path)})
    screenshots = [one for one in rows
                   if one["path"].startswith("screenshots/")
                   and one["path"].endswith(".png")]
    befores = {one["path"].split("/")[-1][len("before--"):] for one in screenshots
               if one["path"].split("/")[-1].startswith("before--")}
    afters = {one["path"].split("/")[-1][len("after--"):] for one in screenshots
              if one["path"].split("/")[-1].startswith("after--")}
    return {
        "members": len(rows),
        "bytes": sum(one["bytes"] for one in rows),
        "rows": rows,
        # Counted, never remembered. Zero is a real answer and is reported as
        # one rather than left for prose to imply.
        "screenshots": {
            "png_count": len(screenshots),
            "raster_pairs": len(befores & afters),
            "unpaired": sorted((befores ^ afters)),
        },
    }


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
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--parent", required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--review", default="")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv)

    repo = args.repo.resolve()
    parent = git(repo, "rev-parse", args.parent).strip()
    head = git(repo, "rev-parse", args.head).strip()
    review = git(repo, "rev-parse", args.review).strip() if args.review else ""

    stat = diffstat(repo, parent, head)
    logs = args.package / "logs"

    claims = {
        "tool": "derive-claims.py",
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
            # Named by the SLUG of the command that wrote them, so a
            # reference in a document resolves to the file without a mapping
            # nobody maintains.
            "focused_catena_head": suite_counts(logs / "focused-catena-head.log"),
            "focused_catena_parent": suite_counts(logs / "focused-catena-parent.log"),
            "full_discovery_head": suite_counts(logs / "full-discovery-head.log"),
            "full_discovery_parent": suite_counts(logs / "full-discovery-parent.log"),
            "browser_static_head": suite_counts(logs / "browser-static-head.log"),
            "v8_tests_against_parent": suite_counts(
                logs / "v8-tests-against-parent.log"),
            "sealer": suite_counts(logs / "sealer-tests.log"),
        },
        "gate": {"head": gate_counts(logs / "browser-gate-head.json"),
                 "parent": gate_counts(logs / "browser-gate-parent.json")},
        "package": package_members(args.package),
        "oracles": oracles(repo, parent, head, "CORRECTED ORACLE (V8)",
                           logs / "v8-tests-against-parent.log"),
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
        args.out.write_text(text, encoding="utf-8")
        # NAMED, not pathed. This line lands in a log inside the package, and
        # an absolute path there is a private token the sealer then has to
        # rewrite — which makes the seal's own idempotence claim untestable.
        print(f"claims written: {args.out.name} "
              f"({len(text.encode('utf-8'))} bytes)")
        # The same values, rendered for a reader, FROM THE SAME DICT. A prose
        # table typed beside a JSON file is two records of one fact and this
        # repository has been bitten by that pair disagreeing; emitting both
        # from one pass makes the disagreement unrepresentable.
        page = args.out.with_name("DERIVED-CLAIMS.md")
        page.write_text(render(claims), encoding="utf-8")
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
    if oracle:
        out += ["", "## Test delta", "", "| | |", "| --- | --- |",
                f"| `{oracle['marker']}` blocks |"
                f" {oracle['corrected_blocks']} |",
                f"| classes holding a corrected oracle |"
                f" {len(oracle['corrected_classes'])} |",
                f"| test classes added |"
                f" {oracle['classes_added_count']} |",
                "",
                "Classes holding a corrected oracle: "
                + ", ".join(f"`{one}`" for one in oracle["corrected_classes"])
                + "."]
        parent_run = oracle.get("against_parent")
        if parent_run:
            out += ["",
                    f"The V8 test file replayed against the PARENT's production"
                    f" files — same scenarios, same oracles, other code —"
                    f" fails **{parent_run['identities']}** identities across"
                    f" **{parent_run['classes']}** classes:"
                    f" {len(parent_run['new_classes_that_fail'])} of the classes"
                    f" V8 adds, and"
                    f" {len(parent_run['pre_existing_classes_that_fail'])}"
                    f" pre-existing classes whose oracles V8 corrected.",
                    "",
                    "Classes V8 adds that do **not** fail at the parent: "
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
    out += ["", "## Package", "", "| | |", "| --- | --- |",
            f"| members | {package['members']} |",
            f"| bytes | {package['bytes']} |",
            f"| PNGs | {shots['png_count']} |",
            f"| before/after raster pairs | {shots['raster_pairs']} |",
            f"| unpaired captures | {len(shots['unpaired'])} |",
            "",
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
