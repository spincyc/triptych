#!/usr/bin/env python3
"""Compare two corpus_browser_gate.mjs reports object for object.

The repository has no gate-comparison tool; V4 compared its two reports with an
ad-hoc script that is not recorded. This is the V4.1 equivalent, written to be
re-runnable by the reviewer. It ignores only the fields that cannot be equal
across two runs -- `generatedAt`, `root` (an absolute path), `durationMs` and
`browser`, which is FOUR and not the one the V4.1 record named -- and
compares every assertion by full identity AND by detail, not by count.

V16, THE V15 REVIEW: THREE FIGURES, THREE NAMES, AND NONE OF THEM IMPLIES
ANOTHER. The review's finding, in its own words: "`compare-gate.py` collapses
2,290 assertion rows to 17 diagnostic names while calling them 'assertion
objects'."

It did, and the collapse was silent. `walk()` yielded one tuple per assertion
row -- 2,290 of them -- and the caller poured those tuples into a DICT keyed
by identity. The gate names an assertion by its DIAGNOSTIC (`single-h1-element`,
`skip-link-targets-existing-element`), and there are seventeen diagnostics run
across 171 pages, so 2,290 rows arrived at 17 keys and 2,273 of them silently
overwrote an earlier one. The printed line then said `assertion objects, base:
17`, which is true of neither quantity: there are not 17 assertion objects,
and 17 is not a count of objects. A reader comparing that line against the
gate's own `assertions: 2290` has no way to reconcile them.

Nothing about the EQUALITY PROOF was wrong, and it is preserved unchanged:
`strip(base) == strip(head)` compares the whole report, minus the four named
volatile fields, as one object. That is the strongest statement available and
it does not depend on the walk at all.

What is reported now, separately and under names that cannot be confused:

  assertion rows              every assertion object in the report, counted
                              where it is found; the gate's own `counts`
                              figure is printed beside it and the two must
                              agree or the report is refused
  distinct diagnostic names   how many NAMES those rows carry -- the 17
  per-diagnostic row counts   so the reader can see the collapse rather than
                              being handed its result
  whole-report equality       the normalized comparison, unchanged

Usage: compare-gate.py BASE.json HEAD.json
"""
import json
import sys
from collections import Counter

VOLATILE = {"generatedAt", "root", "durationMs", "browser"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def walk(node, trail=()):
    """Yield (identity, name, status, detail) for every assertion row.

    ONE TUPLE PER ROW, AND THE IDENTITY IS THE TRAIL PLUS AN ORDINAL. V15
    built the identity from the diagnostic name alone, so 171 pages' worth of
    `single-h1-element` were one identity and 170 of them were discarded by
    the dict that consumed them. The ordinal is the row's position within its
    own `assertions` list, which is stable between two runs of the same gate
    over the same routes and is exactly what makes a row comparable to its
    twin in the other report.
    """
    if isinstance(node, dict):
        if "assertions" in node and isinstance(node["assertions"], list):
            for index, one in enumerate(node["assertions"]):
                if isinstance(one, dict):
                    name = (one.get("name") or one.get("id")
                            or one.get("label") or "")
                    yield ("/".join(trail + (str(name), str(index))),
                           str(name),
                           one.get("status") or one.get("result"),
                           one.get("detail") or one.get("message") or "")
        for key, value in node.items():
            if key in VOLATILE:
                continue
            if key == "assertions":
                continue        # already yielded above; do not descend twice
            step = str(node.get("route") or node.get("state") or key)
            yield from walk(value, trail + (step,))
    elif isinstance(node, list):
        for index, one in enumerate(node):
            yield from walk(one, trail + (str(index),))


def strip(node):
    if isinstance(node, dict):
        return {k: strip(v) for k, v in node.items() if k not in VOLATILE}
    if isinstance(node, list):
        return [strip(one) for one in node]
    return node


def declared_assertions(report):
    """The gate's OWN count of its assertion rows, or None.

    Printed beside the walked count so the two can be compared. A walk that
    disagrees with the report it walked is a walk that missed something, and
    a comparison built on it would be silently partial.
    """
    counts = report.get("counts") or report.get("totals") or {}
    value = counts.get("assertions")
    return value if isinstance(value, int) else None


def describe(label, report, stream):
    """Print the three figures for one report and return them."""
    rows = list(walk(report))
    names = Counter(name for _ident, name, _status, _detail in rows)
    declared = declared_assertions(report)
    print(f"{label} assertion rows (every assertion object): {len(rows)}",
          file=stream)
    print(f"{label} assertion rows the report itself declares: "
          f"{declared if declared is not None else '(not declared)'}",
          file=stream)
    print(f"{label} distinct diagnostic names: {len(names)}", file=stream)
    return rows, names, declared


def main(argv=None, stream=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    stream = stream or sys.stdout
    base_path, head_path = argv[0], argv[1]
    base, head = load(base_path), load(head_path)

    print("base summary:", json.dumps(base.get("summary", {}), sort_keys=True),
          file=stream)
    print("head summary:", json.dumps(head.get("summary", {}), sort_keys=True),
          file=stream)
    print("summary equal:", base.get("summary") == head.get("summary"),
          file=stream)

    base_rows, base_names, base_declared = describe("base", base, stream)
    head_rows, head_names, head_declared = describe("head", head, stream)

    # THE WALK IS PROVED AGAINST THE REPORT IT WALKED. If the gate says 2,290
    # and the walk finds 2,289, the comparison below is over a set this tool
    # cannot claim is the whole set, and saying so is worth more than a
    # verdict computed over it.
    mismatched = []
    for label, rows, declared in (("base", base_rows, base_declared),
                                  ("head", head_rows, head_declared)):
        if declared is not None and declared != len(rows):
            mismatched.append(
                f"{label}: the report declares {declared} assertion rows and "
                f"this walk found {len(rows)}; the row comparison below is "
                f"not over the whole report")
    for one in mismatched:
        print("REFUSING:", one, file=stream)

    # THE PER-DIAGNOSTIC BREAKDOWN, so the collapse is visible rather than
    # applied. V15 printed the collapsed number and nothing else.
    print("rows per diagnostic name (base):", file=stream)
    for name, count in sorted(base_names.items()):
        print(f"  {count:>6}  {name}", file=stream)

    base_by_id = {ident: (status, detail)
                  for ident, _name, status, detail in base_rows}
    head_by_id = {ident: (status, detail)
                  for ident, _name, status, detail in head_rows}
    # THE IDENTITY COUNT IS ITS OWN FIGURE TOO. It equals the row count when
    # every row is distinguishable, and saying both is how a reader learns
    # that it does rather than being asked to assume it.
    print("distinct row identities, base:", len(base_by_id), file=stream)
    print("distinct row identities, head:", len(head_by_id), file=stream)
    print("identity set equal:", set(base_by_id) == set(head_by_id),
          file=stream)
    print("base-only identities:",
          sorted(set(base_by_id) - set(head_by_id))[:20], file=stream)
    print("head-only identities:",
          sorted(set(head_by_id) - set(base_by_id))[:20], file=stream)
    print("diagnostic names only in base:",
          sorted(set(base_names) - set(head_names)), file=stream)
    print("diagnostic names only in head:",
          sorted(set(head_names) - set(base_names)), file=stream)

    shared = set(base_by_id) & set(head_by_id)
    changed_status = [i for i in shared
                      if base_by_id[i][0] != head_by_id[i][0]]
    changed_detail = [i for i in shared
                      if base_by_id[i][1] != head_by_id[i][1]]
    print("rows with changed status:", len(changed_status), file=stream)
    for one in sorted(changed_status)[:20]:
        print("  STATUS", one, base_by_id[one][0], "->", head_by_id[one][0],
              file=stream)
    print("rows with changed detail:", len(changed_detail), file=stream)
    for one in sorted(changed_detail)[:20]:
        print("  DETAIL", one, file=stream)
        print("    base:", base_by_id[one][1][:300], file=stream)
        print("    head:", head_by_id[one][1][:300], file=stream)

    # The strongest statement available: the whole report, minus volatile
    # fields, compared as one object. NAMED EXCLUSIONS: "identical" with an
    # unnamed remainder is a claim the reader cannot bound, so the verdict
    # line carries the exact fields the comparison set aside.
    #
    # UNCHANGED FROM V15, DELIBERATELY. This proof never depended on the walk,
    # and the review passed it; the walk's reporting is what was wrong.
    identical = strip(base) == strip(head)
    print("whole report identical under the named volatile exclusions ("
          + ", ".join(sorted(VOLATILE)) + "):", identical, file=stream)
    # AND THE THREE FIGURES ONE LAST TIME, ON ONE LINE, EACH NAMED. A reader
    # who reads only the verdict line reads all three or none.
    print(f"comparison: assertion_rows {len(base_rows)}, "
          f"distinct_diagnostic_names {len(base_names)}, "
          f"whole_report_equal {identical}", file=stream)
    if mismatched:
        return 2
    return 0 if identical else 1


if __name__ == "__main__":
    sys.exit(main())
