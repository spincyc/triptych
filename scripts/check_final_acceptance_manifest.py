#!/usr/bin/env python3
"""Prove `final-acceptance-manifest.tsv` is complete, and that it invented nothing.

A manifest that says "every case this lane changed" is an assertion, and an
assertion in a review artifact is worth what its check is worth. This runs the
check, in both directions, against a derivation rather than against a memory.

Three proofs, each a set difference:

  MISSING     every case in the production diff that no manifest row names.
              Must be empty, or the manifest is not complete.
  UNSUPPORTED every manifest row whose case is in no production diff and is not
              declared non-derivable. Must be empty, or the manifest names
              something that did not change.
  ORPHANED    every prior review id -- the 104 cold-audit findings, the 114
              targeted re-review findings, the 92 re-review manifest rows --
              that appears in no row's provenance columns. Must be empty, or a
              reviewer's finding has been dropped on the floor.

The first two use ONE identity, computed by one function from both sides:

    case_id = case_type + ":" + claim_or_scope_id

`claim_or_scope_id` is the production diff's own subject -- the claim id, the
`relation -> event` of a binding group, the `status @ scope` of a gap row, the
source-record id, or the file path. It is never empty, including for an
architecture case, where it holds the locus or the gate. Two rows with the same
`case_id` are one case; that is the whole of the deduplication rule, and it is
mechanical on purpose. A grouping that needs judgement -- "these five rows are
one defect" -- belongs in the non-unique `defect_class` column, where it can be
read and disagreed with, and never in the key a set difference is run against.

    python3 scripts/check_final_acceptance_manifest.py \\
        --manifest src/sources/chronology/final-acceptance-manifest.tsv \\
        --range 2330d63a5..214797e78 --range 214797e78..HEAD

Exit 0 when all three differences are empty; 1 otherwise, listing every case.
Nothing under `.scratch/` is read and nothing is written.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import chronology_review_diff as D  # noqa: E402

CHRON = "src/sources/chronology"
PRIOR_ID_SOURCES = (
    (f"{CHRON}/cold-audit-findings.tsv", "finding_id"),
    (f"{CHRON}/post-audit-rereview-findings.tsv", "review_id"),
    (f"{CHRON}/post-audit-rereview-manifest.tsv", "review_id"),
)

# A case that no corpus diff can produce, because it is not a change to the
# corpus: a locus the corpus deliberately says nothing about, a gate, an axis.
# A manifest row of this type is legitimate without a diff row behind it, and
# must say so in `derived_change`.
DECLARED = "declared"
RESULTS = {"PASS", "CHANGES_REQUIRED", "not-previously-reviewed"}
RUNNABLE = ("tools/tpt ", "python3 ", "make ", "git ")


def read_tsv(path: Path) -> tuple[list[str], list[dict]]:
    """A tracked review TSV: `#` comment lines, then a header, then rows."""
    lines = [l for l in path.read_text().splitlines() if not l.startswith("#")]
    reader = csv.DictReader(lines, delimiter="\t")
    return list(reader.fieldnames or []), [r for r in reader if any(r.values())]


def case_id(case_type: str, subject: str) -> str:
    return f"{case_type}:{subject}"


DIFF_TYPE = {"claim": "claim", "binding": "binding", "gap": "gap",
             "source-record": "source-record", "registry-asset": "source-record",
             "contract": "contract", "code": "code"}


def production_cases(repo: Path, ranges: list[str]) -> dict[str, dict]:
    """Every case a diff of the given ranges produces, keyed by case_id."""
    cases: dict[str, dict] = {}
    for spec in ranges:
        base, _, head = spec.partition("..")
        if not head:
            raise SystemExit(f"--range wants BASE..HEAD, got {spec!r}")
        sections = D.build(repo, base, head, D.SECTIONS, "full")
        for rows in sections.values():
            for row in rows:
                key = case_id(DIFF_TYPE[row["kind"]], row["id"])
                cases.setdefault(key, {"case_id": key, "ranges": [], "why": []})
                cases[key]["ranges"].append(spec)
                cases[key]["why"].append(row["why"])
    return cases


def prior_ids(repo: Path) -> set[str]:
    found: set[str] = set()
    for relative, column in PRIOR_ID_SOURCES:
        path = repo / relative
        if not path.exists():
            continue
        _, rows = read_tsv(path)
        found.update(r[column].strip() for r in rows if r.get(column))
    return {i for i in found if i}


SPLIT = re.compile(r"[;,]\s*")


def cited_ids(rows: list[dict]) -> set[str]:
    found: set[str] = set()
    for row in rows:
        for column in ("original_audit_ids", "original_rereview_ids"):
            value = (row.get(column) or "").strip()
            if value and value != "-":
                found.update(part.strip() for part in SPLIT.split(value) if part.strip())
    return found


REQUIRED = ("final_review_id", "case_type", "claim_or_scope_id", "diff_range",
            "derived_change", "defect_class", "original_audit_ids",
            "original_rereview_ids", "prior_result", "source_record",
            "source_locus", "production_files", "why_in_final_review",
            "review_requirements")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", default=str(REPO))
    parser.add_argument("--manifest",
                        default=f"{CHRON}/final-acceptance-manifest.tsv")
    parser.add_argument("--range", action="append", dest="ranges", required=True)
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    manifest = repo / args.manifest
    if not manifest.exists():
        print(f"no manifest at {args.manifest}", file=sys.stderr)
        return 1
    columns, rows = read_tsv(manifest)

    problems: list[str] = []
    for column in REQUIRED:
        if column not in columns:
            problems.append(f"column missing: {column}")
    for row in rows:
        rid = row.get("final_review_id")
        if not (row.get("claim_or_scope_id") or "").strip():
            problems.append(f"{rid}: empty claim_or_scope_id; every case names its "
                            f"subject, architecture cases included")
        if (row.get("prior_result") or "").strip() not in RESULTS:
            problems.append(f"{rid}: prior_result {row.get('prior_result')!r} is not "
                            f"one of {sorted(RESULTS)}")
        # A `declared` row is exempt from the diff, so it must carry its own
        # way of being reproduced; otherwise the exemption is a licence to
        # invent a case no check can reach.
        if (row.get("derived_change") or "").strip() == DECLARED:
            need = (row.get("review_requirements") or "").strip()
            if not any(need.startswith(p) for p in RUNNABLE):
                problems.append(f"{rid}: '{DECLARED}' case whose review_requirements "
                                f"names no runnable command (one of {list(RUNNABLE)})")

    manifest_cases: dict[str, list[dict]] = {}
    for row in rows:
        key = case_id(row["case_type"], row["claim_or_scope_id"])
        manifest_cases.setdefault(key, []).append(row)

    produced = production_cases(repo, args.ranges)

    missing = sorted(set(produced) - set(manifest_cases))
    unsupported = sorted(
        key for key, group in manifest_cases.items()
        if key not in produced
        and not all((r.get("derived_change") or "").strip() == DECLARED for r in group))
    orphaned = sorted(prior_ids(repo) - cited_ids(rows))

    for key in missing:
        problems.append(f"MISSING     {key}  ({'/'.join(produced[key]['why'])})")
    for key in unsupported:
        problems.append(f"UNSUPPORTED {key}  (no diff row, and not marked '{DECLARED}')")
    for identifier in orphaned:
        problems.append(f"ORPHANED    prior review id {identifier} is cited by no row")

    print(f"manifest rows          {len(rows)}")
    print(f"distinct cases         {len(manifest_cases)}")
    print(f"production-diff cases  {len(produced)}  over {len(args.ranges)} range(s)")
    print(f"prior review ids       {len(prior_ids(repo))}, "
          f"{len(cited_ids(rows) & prior_ids(repo))} cited")
    if problems:
        print()
        for line in problems:
            print(line)
        print(f"\n{len(problems)} problem(s)")
        return 1
    print("\ncomplete in both directions, and every prior review id is carried")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
