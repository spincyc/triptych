#!/usr/bin/env python3
"""Derive a father's Greek from a Patristic Text Archive TEI file.

The Greek counterpart of `scripts/migne_transcribe.py`, and the route by which
this library holds any Greek at all. `guidance/catena.md` §8 recorded the
Genesis survey's hardest negative — that Greek Wikisource carries no patristic
commentary on Genesis, that First1KGreek holds none of Basil, Chrysostom or
Gregory of Nyssa, and that Migne's PG on the Internet Archive is polytonic OCR
that is not usable text. The Patristic Text Archive of the Berlin-Brandenburg
Academy is the route that closes it: keyed TEI, per-file Creative Commons
licences stated in each file's own header, and Severian of Gabala's homilies on
the six days among them.

WHAT IS KEPT. The edition division's prose, paragraph by paragraph, prefixed by
a braced `{chapter.paragraph}` locator taken from the file's own CTS textpart
divisions. Quotations and editorial insertions are prose and stay. Person, place
and group names are prose and stay; only their annotation goes.

WHAT IS REMOVED, AND WHY EACH.

    `<ref/>` biblical pointers      the editors' apparatus, not Severian's words
    `<pb/>` `<lb/>` `<cb/>`         the page and line breaks of the source print
    `<note>` bodies                 the editors', including every variant note
    `<teiHeader>`                   metadata; the rights it states are recorded
                                    on the artifact rather than printed as text

The biblical pointers are the debatable removal and it is recorded here rather
than left to be discovered: they are the annotation this project reads to bound
each homily's scriptural extent, and they are also invisible in the printing
Severian preached from. They are stripped from the prose and read separately by
`--references`, which prints them and transcribes nothing.

    python3 scripts/pta_transcribe.py EDITION.xml --out OUT.txt

Nothing here reaches the network and nothing here consults a model. The bytes
are already on disk, hashed, when this runs.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
import xml.etree.ElementTree as ElementTree
from pathlib import Path

TEI = "{http://www.tei-c.org/ns/1.0}"

# Elements whose text belongs to the editors rather than to the author. `note`
# carries the apparatus; `ref` is the biblical pointer; the break markers carry
# the source printing's pagination.
_DISCARD = {"note", "ref", "pb", "lb", "cb", "milestone", "gap"}

_SPACE = re.compile(r"\s+")
_PUNCTUATION = {
    " ": " ", " ": " ", " ": " ", " ": " ",
}


def _prose(element: ElementTree.Element) -> str:
    """One element as running text, the editors' apparatus taken out."""
    parts: list[str] = []
    if element.text:
        parts.append(element.text)
    for child in element:
        tag = child.tag.replace(TEI, "")
        if tag not in _DISCARD:
            parts.append(_prose(child))
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def clean(text: str) -> str:
    text = "".join(_PUNCTUATION.get(character, character) for character in text)
    # NFC so a polytonic accent written as a combining sequence and the same
    # accent precomposed do not produce two different files from one reading.
    text = unicodedata.normalize("NFC", text)
    return _SPACE.sub(" ", text).strip()


def transcribe(path: Path) -> tuple[str, list[dict]]:
    """The edition division as prose, plus what each line is."""
    root = ElementTree.parse(path).getroot()
    body = root.find(f".//{TEI}body")
    if body is None:
        raise ValueError(f"{path}: no body")
    edition = body.find(f"./{TEI}div[@type='edition']")
    if edition is None:
        raise ValueError(f"{path}: no edition division")
    lines: list[str] = []
    index: list[dict] = []
    head = edition.find(f"./{TEI}head")
    if head is not None:
        rendered = clean(_prose(head))
        if rendered:
            lines.append(f"{{0.0}} {rendered}")
            index.append({"chapter": 0, "paragraph": 0, "line": len(lines)})
    for division in edition.findall(f"./{TEI}div[@type='textpart']"):
        chapter = division.get("n") or "0"
        for ordinal, paragraph in enumerate(division.findall(f"./{TEI}p"), 1):
            rendered = clean(_prose(paragraph))
            if not rendered:
                continue
            lines.append(f"{{{chapter}.{ordinal}}} {rendered}")
            index.append({"chapter": chapter, "paragraph": ordinal, "line": len(lines)})
    return "".join(line + "\n" for line in lines), index


def references(path: Path, book: str) -> list[tuple[str, str]]:
    """The editors' biblical pointers to one book, as `(chapter, locus)`.

    Read rather than printed. These are what bound a homily's extent, and they
    are the edition's own statement rather than this project's reading of the
    Greek — which is the distinction the whole source library turns on.
    """
    root = ElementTree.parse(path).getroot()
    found: list[tuple[str, str]] = []
    for division in root.iter(f"{TEI}div"):
        if division.get("type") != "textpart":
            continue
        chapter = division.get("n") or "0"
        for pointer in division.iter(f"{TEI}ref"):
            target = pointer.get("cRef") or ""
            parts = target.split(":")
            if len(parts) >= 4 and parts[1] == book:
                found.append((chapter, ":".join(parts[2:])))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("edition", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--references",
        metavar="BOOK",
        help="print the editors' biblical pointers to BOOK (e.g. Gn) and transcribe nothing",
    )
    arguments = parser.parse_args(argv)
    if arguments.references:
        for chapter, locus in references(arguments.edition, arguments.references):
            print(f"{chapter}\t{locus}")
        return 0
    text, index = transcribe(arguments.edition)
    if not index:
        print(f"no prose parsed from {arguments.edition}", file=sys.stderr)
        return 1
    print(
        f"{arguments.edition}\t{len(index)} paragraphs\t"
        f"chapters {index[0]['chapter']}-{index[-1]['chapter']}",
        file=sys.stderr,
    )
    if arguments.out:
        arguments.out.write_text(text, encoding="utf-8")
        print(f"{arguments.out}: {len(text.splitlines())} lines", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
