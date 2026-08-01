#!/usr/bin/env python3
"""The canon of scripture: the books, their order, and how a path names them.

A PROJECT-GLOBAL FACT, HELD ONCE. Which books there are, what order they stand
in, what each is called, and how many chapters each has are properties of the
project's scripture. They are not properties of any one page, tool or corpus
that consumes them — the catena, the reading plan, the propers, the bible index
and the typesetter all need the same answers — so they live here and every
section is downstream of them.

This module was lifted out of `scripts/_catena.py`, where `canon()` had been
written because the catena was the first thing that needed to walk the whole
Bible. Leaving it there would have made one page the owner of a fact about
scripture, and every other consumer would have had to either import from the
catena, which is backwards, or grow its own copy, which is the restatement that
drifts. This repository has already paid for that: two copies of the same
propers diverged in five ways with nothing comparing them. `scripts/_corpus.py`
set the precedent earlier — four facts about a document, read from four files by
whoever needed them, lifted into one module that several tools now share.

NOTHING HERE VALIDATES. It reads the canonical edition's one tracked book index
and the chapter fragments that edition actually carries, and reports what they
say. The gates belong to the tools that own them.

## The path form, and why it is derived here

A book becomes a directory name in exactly one place, `path_form`, because the
name is derived from the canon and from nothing else. The convention is stated
in `guidance/web-data.md` and is one sentence: **anything with an inherent order
sorts in that order in a directory listing.**

    Gen    ->  01-gen        1Cor  ->  53-cor-1        Ps 150  ->  019-ps/150.json
                                                       Gen 1   ->  01-gen/001.json

- the **canon position** comes first, zero-padded, so a listing reads as the
  Bible rather than as the alphabet and Genesis stops sorting after Ezekiel;
- **lowercase**, because a capitalised path carries every capitalisation
  question with it — `Gen` and `gen` are one file on a case-insensitive
  filesystem and two on a case-sensitive one, and a rename that is clean on
  Linux arrives elsewhere as a collision. *Genesis* and *1 Corinthians* are
  display forms and belong in the text a reader sees;
- the **ordinal last**, so the books of one name group under that name and no
  component reads as a number that is not the canonical one;
- **chapters zero-padded to one width for every book**, derived from the longest
  book the index reports, so `9` sorts before `10` and a reader never has to
  know which book has how many chapters to predict a path.

The citation grammar is untouched by all of this. A citation still addresses
`Gen 1:1` and `1 Cor 13:4`; this governs paths and nothing else.

## What still composes its own paths

`src/sources/bibles/<edition>/chapters/Gen/1.json` predates the convention and
is capitalised, unnumbered and unpadded. Migrating it touches `index-bible`,
`typeset-bible`, the catena and the propers at once, so it is the outstanding
case and belongs in one coherent change rather than in pieces.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# The Clementine is the canonical Latin witness and declares `numbering:
# vulgate`, which is what `_projection.CANONICAL` projects into. Its book index
# is the project's statement of which books there are and in what order.
CANONICAL_BIBLE = "clementine-vulgate"
BIBLES_RELATIVE = Path("src/sources/bibles")

BOOK_NUMBER_WIDTH = 2

# `1Cor` -> `("1", "Cor")`.
ORDINAL_TOKEN = re.compile(r"\A(\d+)(.+)\Z")


class CanonError(RuntimeError):
    """The canon could not be read from the artifacts that state it."""


def book_index(root: Path = ROOT) -> list[dict[str, str]]:
    """The canonical edition's book index, read from its one tracked artifact."""
    found = sorted(
        (root / "src/sources/works").glob(
            "*/*/editions/*/artifacts/book-index-*/book-index.tsv"
        )
    )
    wanted = [path for path in found if "vulgata-clementina" in path.as_posix()]
    if len(wanted) != 1:
        raise CanonError(
            f"expected one Clementine book index under {root}, found {len(wanted)}"
        )
    with wanted[0].open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def books(root: Path = ROOT) -> list[dict[str, Any]]:
    """Every book of the canon in order, with its chapter count.

    Derived, never enumerated by hand: the order and the names come from the
    canonical edition's tracked book index, and the chapter count is how many
    chapter fragments that edition actually carries. Nothing in this repository
    enumerated the canon before the catena needed one — every other structure
    file covers only what a calendar or a reading plan happens to cite.
    """
    chapters_root = root / BIBLES_RELATIVE / CANONICAL_BIBLE / "chapters"
    if not chapters_root.is_dir():
        raise CanonError(f"{chapters_root}: the canonical edition has no chapters")
    found: list[dict[str, Any]] = []
    for record in book_index(root):
        token = (record.get("token") or "").strip()
        directory = chapters_root / token
        if not directory.is_dir():
            continue
        numbers = sorted(
            int(path.stem) for path in directory.glob("*.json") if path.stem.isdigit()
        )
        if not numbers:
            continue
        found.append(
            {
                "token": token,
                "name": (record.get("modern_name") or token).strip(),
                "title": (record.get("douay_title") or "").strip(),
                "testament": (record.get("testament") or "").strip(),
                "chapters": len(numbers),
                "last_chapter": numbers[-1],
            }
        )
    if not found:
        raise CanonError(f"{chapters_root}: no book of the canon could be enumerated")
    return found


def positions(root: Path = ROOT) -> dict[str, int]:
    """Each book token's one-based place in the canon."""
    return {book["token"]: number for number, book in enumerate(books(root), start=1)}


def chapter_width(root: Path = ROOT) -> int:
    """How many digits a chapter number is padded to, across the whole canon.

    Derived from the longest book rather than asserted, and ONE width for every
    book: a reader predicting a path must not have to know that the Psalter has
    150 chapters and Jude has one.
    """
    return len(str(max(int(book["last_chapter"]) for book in books(root))))


def _name_form(token: str) -> str:
    """`Gen` -> `gen`, `1Cor` -> `cor-1`. The name half of a path component."""
    match = ORDINAL_TOKEN.match(token)
    if match:
        return f"{match.group(2).lower()}-{match.group(1)}"
    return token.lower()


def path_forms(root: Path = ROOT) -> dict[str, str]:
    """Every book token's path component: `Gen` -> `01-gen`, `1Cor` -> `53-cor-1`.

    THE ONE PLACE A BOOK BECOMES A PATH. See this module's header for the four
    conventions and the reason behind each. The number is the book's position in
    `books()`, derived on every call and never typed: a hand-written table of 73
    name-to-number pairs beside a derived one is exactly the restatement that
    drifts. An edition that omits the deuterocanon or orders its books
    differently is a display concern; the path follows the project's canon.
    """
    return {
        book["token"]: f"{number:0{BOOK_NUMBER_WIDTH}d}-{_name_form(book['token'])}"
        for number, book in enumerate(books(root), start=1)
    }


def chapter_name(chapter: int, width: int) -> str:
    """`1` -> `001.json` at width 3. The one place a chapter becomes a filename."""
    return f"{int(chapter):0{width}d}.json"


def main(argv: list[str] | None = None) -> int:
    """Print the canon as JSON, with each book's path form, for a reader."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="canon", description="The books of the canon, their order and path forms."
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    forms = path_forms(root)
    rows = [dict(book, path=forms[book["token"]]) for book in books(root)]
    print(
        json.dumps(
            {"chapter_width": chapter_width(root), "books": rows},
            ensure_ascii=False,
            indent=1,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
