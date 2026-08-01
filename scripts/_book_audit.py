#!/usr/bin/env python3
"""Collate the whole-canon, book-level commentary audit from its own ledger.

The audit asks one question a book — "which pre-1900 commentaries treat this
book" — over the seventy-three books the canonical edition's tracked index
enumerates. It is a coarser question than the chapter-keyed discovery index
asks, and it is deliberately kept apart from it.

**Why a separate ledger.** `harvest promote` refuses a bare book key, and it is
right to: the index key space is chapter-addressed, so `Genesis` is "not a locus
this key space can parse". Recording book-level runs into the chapter ledger
would therefore have blocked every future promotion of the chapter index. It
would also have reintroduced the defect TASK-101 removed — an index answering
the same question at two granularities, where a book row and its fifty chapter
rows can disagree while both look complete. `guidance/catena.md` §3 settles the
direction: store the chapter and derive everything finer. A book row is coarser,
so it is not stored there at all.

What this file derives is therefore an audit, not an acquisition index: which
works the runs named for each book, how many independent runs agreed, and —
the part that must not be lost — which books were *not measured*, kept distinct
from books measured and found bare.

    python3 scripts/_book_audit.py --out src/sources/commentary/book-commentary-audit.yaml
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "src/sources/commentary/book-audit-ledger.yaml"
OUT = ROOT / "src/sources/commentary/book-commentary-audit.yaml"


def canon() -> list[dict[str, Any]]:
    """The canon, from the tool that enumerates it, never typed here.

    `scripts/_catena.py canon` reads the canonical edition's one tracked book
    index. A second list of seventy-three names beside it would be the
    restatement `guidance/the-shape.md` §2 forbids, and this file would be where
    the two first disagreed.
    """
    done = subprocess.run(
        [sys.executable, str(ROOT / "scripts/_catena.py"), "canon"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(done.stdout)


def collate(ledger: dict[str, Any], books: list[dict[str, Any]]) -> dict[str, Any]:
    runs = ledger.get("runs") or []
    # A work is identified by author and title exactly as the harvest does it,
    # because `work_id` is null on every harvested lead and string identity is
    # the only key there is. Two spellings of one work therefore count twice
    # here, and the count says so rather than implying a reconciliation nobody
    # performed.
    seen: dict[str, dict[tuple[str, str], dict[str, Any]]] = defaultdict(dict)
    runs_per_book: dict[str, int] = defaultdict(int)
    for run in runs:
        for book, works in (run.get("passages") or {}).items():
            runs_per_book[book] += 1
            for work in works or ():
                key = (str(work.get("author") or ""), str(work.get("title") or ""))
                entry = seen[book].setdefault(
                    key,
                    {
                        "author": key[0],
                        "title": key[1],
                        "date": work.get("death_year"),
                        "role": work.get("role"),
                        "runs": 0,
                    },
                )
                entry["runs"] += 1

    measured = []
    unmeasured = []
    for book in books:
        name = book["name"]
        if name not in runs_per_book:
            # Not "no commentary": no question asked. The two must never be
            # rendered or counted the same, which is the whole of principle 4 in
            # guidance/the-shape.md.
            unmeasured.append({"book": name, "token": book["token"], "reason": "not harvested"})
            continue
        total = runs_per_book[name]
        works = []
        for entry in seen[name].values():
            works.append(
                {
                    "author": entry["author"],
                    "title": entry["title"],
                    "date": entry["date"],
                    "role": entry["role"],
                    "runs": entry["runs"],
                    "confidence": round(entry["runs"] / total, 4),
                }
            )
        works.sort(key=lambda row: (-row["confidence"], row["author"], row["title"]))
        measured.append(
            {
                "book": name,
                "token": book["token"],
                "testament": book["testament"],
                "runs": total,
                "distinct_works": len(works),
                "corroborated": sum(1 for work in works if work["runs"] > 1),
                "works": works,
            }
        )
    return {"measured": measured, "unmeasured": unmeasured}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default=str(LEDGER))
    parser.add_argument("--out", default=str(OUT))
    parser.add_argument("--summary", action="store_true", help="print totals and write nothing")
    arguments = parser.parse_args(argv)

    import yaml

    ledger = yaml.safe_load(Path(arguments.ledger).read_text(encoding="utf-8"))
    books = canon()
    collated = collate(ledger, books)
    measured, unmeasured = collated["measured"], collated["unmeasured"]

    distinct = {
        (work["author"], work["title"])
        for book in measured
        for work in book["works"]
    }
    thin = [b["book"] for b in measured if b["distinct_works"] < 10]
    empty = [b["book"] for b in measured if b["distinct_works"] == 0]
    identical = len({run["run_id"] for run in ledger.get("runs") or []})

    totals = {
        "books_in_canon": len(books),
        "books_measured": len(measured),
        "books_unmeasured": len(unmeasured),
        "books_measured_and_empty": len(empty),
        "books_measured_and_thin": len(thin),
        "distinct_works": len(distinct),
        "attributions": sum(b["distinct_works"] for b in measured),
        "runs_recorded": identical,
    }

    if arguments.summary:
        print(yaml.safe_dump(totals, sort_keys=True, allow_unicode=True), end="")
        if empty:
            print("measured_and_empty: " + ", ".join(empty))
        if unmeasured:
            print("unmeasured: " + ", ".join(b["book"] for b in unmeasured))
        return 0

    document = {
        "schema": "triptych-book-commentary-audit/v1",
        "updated": "2026-08-01",
        "question": "which pre-1900 commentary works treat this book, asked once per book",
        "ledger": "src/sources/commentary/book-audit-ledger.yaml",
        "canon_source": "scripts/_catena.py canon, from the canonical edition's tracked book index",
        "granularity_note": (
            "Book-level. This is NOT the chapter-keyed discovery index and must not be "
            "merged into it: `harvest promote` refuses a bare book key because the index "
            "key space is chapter-addressed, and an index answering one question at two "
            "granularities is the defect TASK-101 removed."
        ),
        "unmeasured_note": (
            "`unmeasured` is a book nothing asked about. It is not a book with no "
            "commentary, and the two must never be added together."
        ),
        "totals": totals,
        "unmeasured": unmeasured,
        "books": measured,
    }
    out = Path(arguments.out)
    out.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    print(yaml.safe_dump(totals, sort_keys=True, allow_unicode=True), end="")
    print(f"written: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
