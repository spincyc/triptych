#!/usr/bin/env python3
"""Build the profile-contract cold-review surface for the correction lane.

Two artifacts, both derived and neither hand-picked:

  src/sources/chronology/profile-contract-rereview-manifest.tsv
  src/sources/chronology/profile-contract-corrections.tsv

The manifest is the surface a genuinely cold reviewer works from. §26 of the
lane brief fixes what has to be in it, and every clause of that list is a
QUERY OVER THE DATA rather than a judgement of this lane's:

  - every factual claim changed in this lane      -> the claim diff
  - every binding/scope changed                   -> the binding diff
  - every claim whose answerability moved         -> the answerability diff
  - all Howlett claims, all Sloet claims          -> by cited source record
  - the Ussher-exception claims                   -> by reporting_exception
  - the five named blockers                       -> by id, asserted present
  - profile-policy and semantic-diff gate cases   -> the profile diff and the
                                                     gates that watch it

so that a row cannot be forgotten by being unmemorable. Deduplicated on
case_type + ':' + case_id, which is what lets one claim appear once though four
clauses of §26 reach it, while the `why_in_review` column keeps every reason
that reached it.

The base side is a committed revision, loaded by ITS OWN loader through
chronology_review_diff. The head side is the WORKING TREE, loaded by the
loader in it: this lane leaves its work uncommitted for a coordinator to
review, and a manifest that could only be built after the commit would be
built too late to inform it.

  python3 scripts/build_profile_contract_manifest.py [--base REV]
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import chronology_review_diff as review  # noqa: E402

CHRONOLOGY = "src/sources/chronology"
HOWLETT = "artifact.catholic-encyclopedia.volume-3.new-york-1908.newadvent-03731a-f5f96f04"
SLOET = "artifact.catholic-encyclopedia.volume-8.new-york-1910.newadvent-08654a-645bba6c"

# The five blockers, by the id the final cold acceptance review named them
# under. Asserted present at the end: a manifest that silently lost one of
# these is worse than no manifest, because it reads as a clean bill.
BLOCKERS = {
    "claim:event:israel.divided-kingdom.fall-of-samaria#0": (
        "MF-1", "FA-140",
        "BLOCKER 1 -- fall of Samaria: the rank-1 Scriptural relation of "
        "4 Kings 18:10, suppressed until 2026-09-01 by Sloet's critical "
        "judgement that the Ezechias-Osee synchronism is unhistorical",
    ),
    "claim:event:israel.primeval.creation#1": (
        "MF-2", "-",
        "BLOCKER 2 -- creation#1: Howlett's refusal to date, authored as a "
        "date and displayed by query Gen.1.1 though its own note said it "
        "must never be",
    ),
    "claim:event:israel.exile.third-captivity#4": (
        "FA-140", "RR-090-LEAD",
        "BLOCKER 3 -- the 536 case: a figure the corpus itself calls the look "
        "of a printing error, returned as a live alternate beside 586, 587 "
        "and 588",
    ),
    "binding:narrated-event -> life-of-christ.crucifixion": (
        "MF-4", "FA-005",
        "BLOCKER 4 -- Matt 27:53: a verse whose own words date its action "
        "after the Resurrection, answered with seven Crucifixion dates, every "
        "one marked direct",
    ),
    "family:sloet-own-table": (
        "MF-3", "FA-019",
        "BLOCKER 5 -- the Sloet family: six claims resting on a table whose "
        "author declares its method to be the one the profile excludes",
    ),
}

# Historical review ids, carried forward so a cold reviewer can trace a case
# back through every lane that touched it rather than meeting it fresh.
HISTORY = {
    "claim:event:israel.divided-kingdom.fall-of-samaria#0": "MF-1",
    "claim:event:israel.divided-kingdom.fall-of-samaria#4": "MF-3;FA-019",
    "claim:event:israel.primeval.creation#1": "MF-2",
    "claim:event:israel.primeval.creation#0": "MF-2",
    "claim:event:israel.exile.third-captivity#4": "FA-140;RR-090-LEAD",
    "claim:event:israel.exile.third-captivity#0": "FA-030;E2-008;LEAD-001;P-012;RR-014",
    "claim:event:israel.monarchy.david-accession#1": "MF-3;FA-043",
    "claim:event:israel.monarchy.solomon-accession#1": "MF-3;FA-048",
    "claim:event:israel.monarchy.temple-begun#3": "MF-3;FA-050;RR-030;RR-090",
    "claim:event:israel.divided-kingdom.division#2": "MF-3;FA-019",
    "claim:event:israel.divided-kingdom.ezechias-accession#1": "MF-3",
    "claim:event:israel.monarchy.temple-begun#2": "FA-049;P-004;E2-001;G-006;S1-001;RR-029",
    "claim:event:israel.exodus.the-exodus#0": "FA-032;E1-008;E1-010;LEAD-014;G-006;RR-016",
    "claim:event:israel.divided-kingdom.division#0": "FA-018;RR-090-LEAD",
    "claim:event:israel.monarchy.birth-of-david#0": "FA-042;P-025;RR-026",
    "binding:narrated-event -> life-of-christ.crucifixion": "FA-005;FA-133;LEAD-016",
    "contract:src/sources/chronology/profiles.yaml": "MF-7;FA-094",
    "contract:scripts/chronology_review_diff.py": "MF-6;FA-089",
}


def working_tree(repo: Path) -> dict:
    """The corpus in the WORKING TREE, through the same projection worker."""
    with tempfile.TemporaryDirectory(prefix="chronology-worktree-") as tmp:
        # The worker resolves the loader relative to ITSELF, so it has to sit
        # at the root of a tree that has a `scripts` beside the corpus. Symlink
        # one rather than copy: the point is to read the working tree as it is.
        tree = Path(tmp)
        (tree / "scripts").symlink_to(repo / "scripts")
        for shared in (*review.SHARED, CHRONOLOGY):
            link = tree / shared
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(repo / shared)
        worker = tree / "_review_projection.py"
        worker.write_text(review.WORKER)
        done = subprocess.run(
            [sys.executable, str(worker), str(tree / CHRONOLOGY)],
            capture_output=True, text=True, cwd=str(tree),
        )
        if done.returncode:
            raise SystemExit("the working tree would not load:\n" + done.stderr.strip())
        return json.loads(done.stdout)


class Surface:
    """Rows keyed by case, so one case reached four ways is still one row."""

    def __init__(self) -> None:
        self.rows: dict[str, dict] = {}

    def add(self, case_type: str, case_id: str, **fields) -> dict:
        key = f"{case_type}:{case_id}"
        row = self.rows.get(key)
        if row is None:
            row = self.rows[key] = {
                "case_type": case_type, "case_id": case_id,
                "changed_in_lane": "no", "change": "-", "answerability_change": "-",
                "basis_class": "-", "answerability": "-", "disposition": "-",
                "source_record": "-", "prior_review_ids": HISTORY.get(key, "-"),
                "why_in_review": [],
            }
        for name, value in fields.items():
            if name == "why_in_review":
                if value not in row["why_in_review"]:
                    row["why_in_review"].append(value)
            elif value not in ("-", "", None):
                row[name] = value
        return row


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--base", default="HEAD")
    parser.add_argument("--repo", default=str(REPO))
    args = parser.parse_args(argv)
    repo = Path(args.repo).resolve()

    with tempfile.TemporaryDirectory(prefix="chronology-review-") as tmp:
        old = review.load_revision(repo, args.base, Path(tmp))
    new = working_tree(repo)

    fields = review.FIELD_SETS["full"]
    claims = review.diff_claims(old, new, fields)
    answerability = review.diff_answerability(old, new, fields)
    bindings = review.diff_bindings(old, new, full=True)
    gaps = review.diff_gaps(old, new)
    profiles = review.diff_profiles(old, new)

    surface = Surface()

    # 1. every factual claim changed in this lane
    for row in claims:
        surface.add(
            "claim", row["id"], changed_in_lane="yes", change=row["why"],
            why_in_review="the claim's own stored state changed in this lane",
        )
    # 2. every claim whose answerability moved, INCLUDING the profile-only
    #    ones no file diff can produce
    for row in answerability:
        surface.add(
            "claim", row["id"], changed_in_lane="yes",
            answerability_change=row["why"] + " (" + row["locus"] + ")",
            why_in_review=(
                "the claim's candidate eligibility changed: " + row["detail"]
                if row["detail"] else "the claim's candidate eligibility changed"),
        )
    # 3. every binding/scope changed
    for row in bindings:
        surface.add(
            "binding", row["id"], changed_in_lane="yes", change=row["why"],
            why_in_review="the binding's scope, note or sources changed in this lane",
        )
    # 3b. every gap row added, withdrawn or reworded. A gap row is what a verse
    #     ANSWERS WITH once the last answerable claim over it is preserved, so a
    #     lane that rules a claim inadmissible and a lane that writes the row the
    #     verse then falls to are doing one thing, and a review surface that
    #     carried only the first half would show a claim withdrawn and never show
    #     the sentence the consumer reads in its place.
    for row in gaps:
        surface.add(
            "gap", row["id"], changed_in_lane="yes",
            change=row["why"] + (f" ({row['detail']})" if row["detail"] else ""),
            why_in_review="the gap row a verse now answers with was added, "
                          "withdrawn or reworded in this lane",
        )
    for _row in profiles:
        surface.add(
            "contract", "src/sources/chronology/profiles.yaml",
            changed_in_lane="yes", change="profile semantics",
            why_in_review="the normalised profile semantics differ between the two sides",
        )

    # 4-6. whole-artifact families and the exception, from the head corpus.
    for locus, claim in sorted(new["claims"].items()):
        why = []
        if HOWLETT in claim["sources"]:
            why.append("Howlett whole-artifact ruling: every claim citing "
                       '"Biblical Chronology" is in the surface, not a sample')
        if SLOET in claim["sources"]:
            why.append("Sloet whole-artifact ruling: every claim citing "
                       '"Chronology of the Kings" is in the surface, not a sample')
        if claim.get("reporting_exception"):
            why.append("Ussher reporting exception: the narrowness of the one "
                       "named lift is only checkable claim by claim")
        if claim.get("answerability") == "preserved":
            why.append("preserved-only claim: reachable through the evidence "
                       "surface and excluded from every default answer")
        if claim.get("basis_class") == "unreviewed":
            why.append("STILL UNREVIEWED: the basis has not been classified "
                       "under this contract and this lane did not rule it")
        if not why:
            continue
        row = surface.add(
            "claim", locus,
            basis_class=claim.get("basis_class") or "-",
            answerability=claim.get("answerability") or "-",
            disposition=claim.get("disposition") or "-",
            source_record=";".join(claim["sources"]) or "-",
        )
        for reason in why:
            surface.add("claim", locus, why_in_review=reason)

    # fill basis/answerability on every claim row that has one at head
    for key, row in surface.rows.items():
        if row["case_type"] != "claim":
            continue
        claim = new["claims"].get(row["case_id"])
        if claim:
            row["basis_class"] = claim.get("basis_class") or "-"
            row["answerability"] = claim.get("answerability") or "-"
            row["disposition"] = claim.get("disposition") or "-"
            row["source_record"] = ";".join(claim["sources"]) or "-"
        else:
            row["why_in_review"].append(
                "WITHDRAWN OR RE-IDENTIFIED: this id does not resolve at head")

    # 7. the five named blockers, and the gates that watch the contract
    for key, (mf, fa, why) in BLOCKERS.items():
        case_type, case_id = key.split(":", 1)
        row = surface.add(case_type, case_id, why_in_review=why)
        ids = [i for i in (mf, fa) if i and i != "-"]
        if ids:
            have = [] if row["prior_review_ids"] == "-" else row["prior_review_ids"].split(";")
            row["prior_review_ids"] = ";".join(dict.fromkeys(have + ids))
    touched = {
        line[3:].strip().strip('"')
        for line in review._git(repo, "status", "--porcelain").splitlines()
    }
    for case_id, why in (
        ("scripts/chronology_review_diff.py",
         "semantic-diff gate: the differ must report a profile-policy change "
         "and enumerate the claims it moved, which it was blind to before"),
        ("scripts/_chronology.py",
         "the single candidate gate: admissibility is decided in _candidates(), "
         "BEFORE rank and before any ordering, and there is no second path"),
        ("guidance/scripture-chronology.md",
         "the contract in prose; profiles.yaml governs and this explains"),
        ("tools/tests/test_chronology.py",
         "the regressions: preserved-not-answered, refusal-is-not-a-date, "
         "own-voice-on-an-excluded-basis, the Ussher exception's narrowness, "
         "a profile change moving eligibility, and the four blocker queries"),
    ):
        surface.add("contract", case_id,
                    changed_in_lane="yes" if case_id in touched else "no",
                    why_in_review=why)

    rows = sorted(
        surface.rows.values(),
        key=lambda r: (r["case_type"], r["case_id"]),
    )
    for i, row in enumerate(rows, start=1):
        row["review_id"] = f"PC-{i:03d}"
        row["why_in_review"] = " | ".join(row["why_in_review"]) or "-"

    missing = [k for k in BLOCKERS if k not in surface.rows]
    if missing:
        raise SystemExit("the manifest lost a named blocker: " + ", ".join(missing))

    columns = ["review_id", "case_type", "case_id", "changed_in_lane", "change",
               "answerability_change", "basis_class", "answerability",
               "disposition", "source_record", "prior_review_ids", "why_in_review"]
    out = repo / CHRONOLOGY / "profile-contract-rereview-manifest.tsv"
    with out.open("w", newline="") as fh:
        fh.write(HEADER.format(base=review._git(repo, "rev-parse", args.base).strip(),
                               rows=len(rows)))
        writer = csv.DictWriter(fh, columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "-") for c in columns})
    print(f"ok\t{out.relative_to(repo)}\t{len(rows)} rows")
    return 0


HEADER = """\
# Profile-contract cold-review manifest for the Scripture chronology corpus.
#
# The complete review surface for a GENUINELY COLD review of the
# profile-contract correction lane: a new agent or session that performed
# none of the population, none of the audits, and none of these corrections.
# Every row is reviewed. Nothing is sampled and nothing is hand-picked.
#
# Derived by diffing the corpus at {base} -- loaded by ITS OWN loader --
# against the WORKING TREE loaded by the loader in it, as OBJECTS, so a
# reformat cannot hide a change; then unioned with four whole-population
# queries over the head corpus (every claim citing Howlett, every claim citing
# Sloet, every claim naming a reporting exception, every preserved claim, and
# every claim still carrying basis_class `unreviewed`), and with the five
# blockers by id and the contract and gate files by path, and with every gap
# row added, withdrawn or reworded, which is what a verse answers with once the
# last answerable claim standing over it has been preserved.
#
# Deduplicated on case_type + ':' + case_id. `why_in_review` keeps EVERY
# reason that reached a row, so a case that four clauses of the brief reach
# is one row that says so four times rather than four rows saying it once.
#
# Regenerate with `python3 scripts/build_profile_contract_manifest.py`.
# Rows: {rows}.
"""

if __name__ == "__main__":
    raise SystemExit(main())
