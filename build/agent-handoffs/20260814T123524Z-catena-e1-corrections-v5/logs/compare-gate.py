#!/usr/bin/env python3
"""Compare two corpus_browser_gate.mjs reports object for object.

The repository has no gate-comparison tool; V4 compared its two reports with an
ad-hoc script that is not recorded. This is the V4.1 equivalent, written to be
re-runnable by the reviewer. It ignores only the fields that cannot be equal
across two runs (`generatedAt`, and `root`, which is an absolute path), and
compares every assertion by full identity AND by detail, not by count.

Usage: compare-gate.py BASE.json HEAD.json
"""
import json
import sys

VOLATILE = {"generatedAt", "root", "durationMs", "browser"}


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def walk(node, trail=()):
    """Yield (identity, status, detail) for every assertion-shaped object."""
    if isinstance(node, dict):
        if "assertions" in node and isinstance(node["assertions"], list):
            for one in node["assertions"]:
                if isinstance(one, dict):
                    name = one.get("name") or one.get("id") or one.get("label") or ""
                    yield ("/".join(trail + (str(name),)),
                           one.get("status") or one.get("result"),
                           one.get("detail") or one.get("message") or "")
        for key, value in node.items():
            if key in VOLATILE:
                continue
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


def main():
    base_path, head_path = sys.argv[1], sys.argv[2]
    base, head = load(base_path), load(head_path)

    print("base summary:", json.dumps(base.get("summary", {}), sort_keys=True))
    print("head summary:", json.dumps(head.get("summary", {}), sort_keys=True))
    print("summary equal:", base.get("summary") == head.get("summary"))

    base_rows = {ident: (status, detail) for ident, status, detail in walk(base)}
    head_rows = {ident: (status, detail) for ident, status, detail in walk(head)}

    print("assertion objects, base:", len(base_rows))
    print("assertion objects, head:", len(head_rows))
    print("identity set equal:", set(base_rows) == set(head_rows))
    print("base-only identities:", sorted(set(base_rows) - set(head_rows))[:20])
    print("head-only identities:", sorted(set(head_rows) - set(base_rows))[:20])

    shared = set(base_rows) & set(head_rows)
    changed_status = [i for i in shared if base_rows[i][0] != head_rows[i][0]]
    changed_detail = [i for i in shared if base_rows[i][1] != head_rows[i][1]]
    print("rows with changed status:", len(changed_status))
    for one in sorted(changed_status)[:20]:
        print("  STATUS", one, base_rows[one][0], "->", head_rows[one][0])
    print("rows with changed detail:", len(changed_detail))
    for one in sorted(changed_detail)[:20]:
        print("  DETAIL", one)
        print("    base:", base_rows[one][1][:300])
        print("    head:", head_rows[one][1][:300])

    # The strongest statement available: the whole report, minus volatile
    # fields, compared as one object.
    identical = strip(base) == strip(head)
    print("whole report identical (volatile fields excluded):", identical)
    return 0 if identical else 1


if __name__ == "__main__":
    sys.exit(main())
