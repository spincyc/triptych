#!/usr/bin/env python3
"""Derive `final-acceptance-manifest.tsv` — the review surface for the cold lane.

The manifest is DERIVED, not hand-picked, because a hand-picked review surface
is exactly as complete as its author remembered to be. It is the union of two
production diffs, one per lane:

    2330d63a5..214797e78   the post-audit correction lane, which the targeted
                           cold re-review reviewed as 92 manifest rows
    214797e78..<head>      this repair lane, closing that review's 23 failures

deduplicated on `case_type + ":" + claim_or_scope_id`, with provenance joined
back from every prior review artifact so that no finding is dropped on the way.

Two facts about the join, both measured rather than assumed:

  * The 92 rows are NOT 92 cases. Two rows are duplicates of others (`RR-090`
    is `RR-031` seen again; `RR-077` is the seven Flood-to-Abram claim rows seen
    again as one hard case) and two rows are bundles (`RR-091` names two source
    records, `RR-092` names six). 92 - 2 + 6 = 96.
  * Four binding groups changed materially with no scope change, so the earlier
    manifest — which compared scope alone — could not see them. Two of the four
    are corrected misquotations of the tracked Douay, which is the class three
    auditors independently raised. This derivation compares the full field set.

`--check` re-derives and compares, so the file cannot drift from its own rule.
Prose columns are carried over from the tracked file when one exists, so a
re-run does not discard a reviewer-facing sentence someone wrote by hand.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import chronology_review_diff as D  # noqa: E402

CHRON = REPO / "src/sources/chronology"
OUT = CHRON / "final-acceptance-manifest.tsv"
DECLARED = "declared"

# The 23 rows the targeted cold re-review returned CHANGES_REQUIRED, which this
# repair lane closed. Listed so that a row carrying one of them is marked as a
# repaired failure rather than as a row that merely passed.
FAILED_ROWS = {
    "GUIDANCE-6", "RR-073", "RR-090", "RR-090-LEAD", "RR-091", "RR-091-LEAD",
    "RR-092", "RR-092-LEAD", "WD-A4-017", "MANIFEST-WHY", "RR-004", "RR-028",
    "RR-038", "RR-038-LEAD", "RR-045", "RR-054", "RR-062", "RR-067", "RR-075",
    "STALECOUNT", "STALEHEAD", "WD-F-021", "YAMLDUP",
}

COLUMNS = [
    "final_review_id", "case_type", "claim_or_scope_id", "diff_range",
    "derived_change", "defect_class", "original_audit_ids",
    "original_rereview_ids", "prior_result", "source_record", "source_locus",
    "production_files", "why_in_final_review", "review_requirements",
]

DIFF_TYPE = {"claim": "claim", "binding": "binding", "gap": "gap",
             "source-record": "source-record", "registry-asset": "source-record",
             "contract": "contract", "code": "code"}

# Rows of the 92 that name more than the one case their `identifier` spells out.
# Declared here rather than inferred, so that the expansion is checkable: a
# reviewer can open each id and see whether the row really covers it.
BUNDLES = {
    "RR-091": [
        "source-record:artifact.catholic-encyclopedia.alphabetical-index"
        ".newadvent-web-2026-08-27.index-g-064c6c3b",
        "source-record:artifact.catholic-encyclopedia.alphabetical-index"
        ".newadvent-web-2026-08-27.index-n-ef3ba0eb",
    ],
    "RR-092": [
        "source-record:artifact.catholic-encyclopedia.volume-6.new-york-1909"
        ".newadvent-06412b-bdfebbee",
        "source-record:artifact.catholic-encyclopedia.volume-6.new-york-1909"
        ".newadvent-06412c-57ecea11",
        "source-record:artifact.catholic-encyclopedia.volume-6.new-york-1909"
        ".newadvent-06413a-88aaf066",
        "source-record:artifact.catholic-encyclopedia.volume-6.new-york-1909"
        ".newadvent-06413c-a10d26f7",
        "source-record:artifact.catholic-encyclopedia.volume-9.new-york-1910"
        ".newadvent-09207a-e9463bc3",
        "source-record:artifact.catholic-encyclopedia.volume-11.new-york-1911"
        ".newadvent-11151a-aaa70339",
    ],
}


def read_tsv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    lines = [l for l in path.read_text(encoding="utf-8").splitlines()
             if not l.startswith("#")]
    return [r for r in csv.DictReader(lines, delimiter="\t") if any(r.values())]


def rereview_provenance() -> dict[str, list[str]]:
    """case_id -> the RR-nnn rows of the 92-row manifest that name it."""
    out: dict[str, list[str]] = {}
    for row in read_tsv(CHRON / "post-audit-rereview-manifest.tsv"):
        rid, kind, ident = row["review_id"], row["kind"], row["identifier"]
        keys = BUNDLES.get(rid)
        if keys is None:
            keys = [f"{kind}:{ident}"] if kind in DIFF_TYPE.values() else []
        for key in keys:
            out.setdefault(key, []).append(rid)
    return out


def _mentions(text: str, subject: str) -> bool:
    """Does a finding's own prose name this case?

    The prior artifacts do not share one key. The cold audit keys on
    `claim_id`, sometimes collapsed (`#0, #1, #2`); the re-review keys on a
    free-text `manifest_row` that may read `claim: event:x#0`, `gap:
    undated-in-tradition @ Gen`, or `hard-case:` and a sentence. Rather than
    invent a key none of them has, a finding is joined to a case when the
    case's own subject appears in the finding's text. It over-attributes
    rather than under-attributes, deliberately: a reviewer sent to one extra
    finding loses a minute, and a finding sent to nobody is the failure this
    manifest exists to prevent.
    """
    if not subject or len(subject) < 6:
        return False
    if subject in text:
        return True
    # A claim id collapsed onto a shared subject: `event:x#0, #1, #2`.
    holder, _, index = subject.rpartition("#")
    return bool(holder and index.isdigit()
                and holder in text and f"#{index}" in text)


def findings_provenance(cases: dict[str, dict]) -> tuple[
        dict[str, list[str]], dict[str, list[str]], dict[str, str], set[str]]:
    """case_id -> the prior findings that named it; plus every id that matched none."""
    subjects = {key: case["claim_or_scope_id"] for key, case in cases.items()}
    audit: dict[str, list[str]] = {}
    rere: dict[str, list[str]] = {}
    result: dict[str, str] = {}
    unmatched: set[str] = set()

    for row in read_tsv(CHRON / "cold-audit-findings.tsv"):
        fid = (row.get("finding_id") or "").strip()
        text = " ".join(str(v) for v in row.values() if v)
        hit = [k for k, s in subjects.items() if _mentions(text, s)]
        for key in hit:
            audit.setdefault(key, []).append(fid)
        if not hit and fid:
            unmatched.add(fid)

    for row in read_tsv(CHRON / "post-audit-rereview-findings.tsv"):
        rid = (row.get("review_id") or "").strip()
        text = " ".join(str(v) for v in row.values() if v)
        hit = [k for k, s in subjects.items() if _mentions(text, s)]
        for key in hit:
            rere.setdefault(key, []).append(rid)
            if (row.get("result") or "").strip() == "CHANGES_REQUIRED":
                result[key] = "CHANGES_REQUIRED"
            else:
                result.setdefault(key, "PASS")
        if not hit and rid:
            unmatched.add(rid)

    return audit, rere, result, unmatched


def derive(head: str) -> list[dict]:
    ranges = [f"2330d63a5..214797e78", f"214797e78..{head}"]
    cases: dict[str, dict] = {}
    for spec in ranges:
        base, _, top = spec.partition("..")
        for rows in D.build(REPO, base, top, D.SECTIONS, "full").values():
            for row in rows:
                key = f"{DIFF_TYPE[row['kind']]}:{row['id']}"
                slot = cases.setdefault(key, {
                    "case_type": DIFF_TYPE[row["kind"]],
                    "claim_or_scope_id": row["id"],
                    "ranges": [], "why": [], "locus": row.get("locus", ""),
                    "notes": row.get("notes", ""),
                })
                slot["ranges"].append(spec)
                slot["why"].append(row["why"])
    return cases


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    spec = args.head
    if args.check and spec == "HEAD" and OUT.exists():
        # A CHECK MUST NOT MOVE ITS OWN TARGET. The file pins the head it was
        # derived from; re-deriving against a later HEAD would report every
        # commit since as a difference, so the check would go red on work that
        # has nothing to do with it.
        found = re.search(r"# 214797e78\.\.(\S+) --", OUT.read_text(encoding="utf-8"))
        if found:
            spec = found.group(1)
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", spec],
                          capture_output=True, text=True, check=True).stdout.strip()
    cases = derive(head)
    rr = rereview_provenance()
    audit, rere, result, unmatched = findings_provenance(cases)
    kept = {r["claim_or_scope_id"]: r for r in read_tsv(OUT)}

    def emit(index, case_type, ident, drange, change, audit_ids, rere_ids,
             prior, locus="-"):
        old = kept.get(ident, {})
        return {
            "final_review_id": f"FA-{index:03d}",
            "case_type": case_type,
            "claim_or_scope_id": ident,
            "diff_range": drange,
            "derived_change": change,
            "defect_class": old.get("defect_class", "-"),
            "original_audit_ids": ";".join(dict.fromkeys(audit_ids)) or "-",
            "original_rereview_ids": ";".join(dict.fromkeys(rere_ids)) or "-",
            "prior_result": prior,
            "source_record": old.get("source_record", "-"),
            "source_locus": old.get("source_locus", locus or "-"),
            "production_files": old.get("production_files", "-"),
            "why_in_final_review": old.get("why_in_final_review", "-"),
            "review_requirements": old.get(
                "review_requirements",
                "python3 tools/tpt scripture-chronology validate"),
        }

    rows = []
    index = 0
    for key in sorted(cases):
        index += 1
        case = cases[key]
        rows.append(emit(
            index, case["case_type"], case["claim_or_scope_id"],
            ";".join(sorted(set(case["ranges"]))),
            ";".join(dict.fromkeys(case["why"])),
            audit.get(key, []), rr.get(key, []) + rere.get(key, []),
            result.get(key, "not-previously-reviewed"),
            case.get("locus") or "-"))

    # WHAT NO DIFF CAN PRODUCE. A finding may be about something the corpus
    # deliberately does not hold -- a locus it says nothing about, a whole-corpus
    # count, a gate, an axis -- or may have been withdrawn without changing a
    # byte. Such a finding has no diff row to attach to, and dropping it would
    # be exactly the silent loss this manifest is built to make impossible. It
    # gets a row of its own, marked `declared`, carrying a command the reviewer
    # can actually run.
    for fid in sorted(unmatched):
        index += 1
        is_audit = not fid.startswith(("RR-", "WD-", "MANIFEST", "STALE",
                                       "GUIDANCE", "YAMLDUP", "COVERAGE"))
        rows.append(emit(
            index, "architecture", f"prior-finding:{fid}", "-", DECLARED,
            [fid] if is_audit else [], [] if is_audit else [fid],
            "CHANGES_REQUIRED" if fid in FAILED_ROWS else "PASS"))

    buffer = io.StringIO()
    buffer.write(
        "# Final acceptance manifest for the Scripture chronology corpus.\n"
        "# The complete review surface for a GENUINELY COLD acceptance review:\n"
        "# a new agent or session that performed none of the population, the\n"
        "# first audit, the post-audit correction, the targeted re-review, or\n"
        "# the repair that closed its 23 failures. Every row is reviewed.\n"
        "#\n"
        f"# Derived from two production diffs -- 2330d63a5..214797e78 and\n"
        f"# 214797e78..{head} -- by loading each revision's corpus through its\n"
        "# OWN scripts/_chronology.py and diffing the loaded OBJECTS, so a\n"
        "# reformat cannot hide a change and a loader that has since tightened\n"
        "# cannot refuse to read the older side. Deduplicated on\n"
        "# case_type + ':' + claim_or_scope_id. Nothing is sampled and nothing\n"
        "# is hand-picked.\n"
        "#\n"
        "# Regenerate with `python3 scripts/build_final_acceptance_manifest.py`.\n"
        "# Prove complete with `python3 scripts/check_final_acceptance_manifest.py`,\n"
        "# which fails on any changed case this file omits, any row no diff\n"
        "# supports, and any prior review id no row cites.\n"
    )
    writer = csv.DictWriter(buffer, fieldnames=COLUMNS, delimiter="\t",
                            lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    text = buffer.getvalue()

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"{OUT.relative_to(REPO)} differs from a fresh derivation")
            return 1
        print(f"{OUT.relative_to(REPO)} is current: {len(rows)} cases")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"{OUT.relative_to(REPO)}: {len(rows)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
