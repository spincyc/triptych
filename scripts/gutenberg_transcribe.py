#!/usr/bin/env python3
"""Derive the underlying text from a Project Gutenberg plain-text eBook.

The declared transformation behind every `web-transcription` artifact taken
from Project Gutenberg, and the counterpart of `scripts/wikisource_transcribe.py`.

Two things have to be separated and neither is optional. Gutenberg's own
permission page states that the vast majority of its eBooks "are in the public
domain in the US" and that "nobody can grant, or withhold, permission to do with
this item as you please" — but that is a statement about the **book**, not about
the file. The file is wrapped in Project Gutenberg's licence header and footer,
which carry the Project Gutenberg trademark and a set of conditions on its use.
So the download is retained as a hashed `remote` artifact and what is tracked is
this derivative, from which the wrapper has been removed, leaving only the text
whose rights the permission page actually settles.

The boundaries are the markers Gutenberg itself prints and are matched exactly,
not approximately. If either marker is missing the script refuses rather than
guessing where the book starts: a wrong boundary would silently prepend a
licence to a father's words or drop the opening of a treatise, and both would
read as the text.

    python3 scripts/gutenberg_transcribe.py EBOOK.txt --out BOOK.txt

Nothing here reaches the network and nothing here consults a model. The bytes
are already on disk, hashed, when this runs.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

START = re.compile(r"^\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$", re.M)
END = re.compile(r"^\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*\s*$", re.M)

_PUNCTUATION = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    " ": " ", " ": " ", " ": " ", " ": " ",
    "′": "'", "″": '"',
}
_SPACE = re.compile(r"[ \t]+")


# Older Gutenberg files print a colophon line INSIDE the two markers — "End of
# Project Gutenberg's Commentary on Genesis, Vol. I, by Martin Luther" — so a
# strip that trusted the markers alone would carry Gutenberg's own sentence into
# the text as though Luther had written it. Found by reading the tail of the
# first derivative rather than by expecting it.
COLOPHON = re.compile(
    r"^\s*End of (?:the )?Project Gutenberg(?:'s|™)?\b.*$", re.M | re.I
)


def strip_wrapper(text: str) -> str:
    """The book between Gutenberg's own two markers, or a refusal."""
    opening = START.search(text)
    if not opening:
        raise ValueError("no Project Gutenberg START marker; refusing to guess the boundary")
    closing = END.search(text, opening.end())
    if not closing:
        raise ValueError("no Project Gutenberg END marker; refusing to guess the boundary")
    body = text[opening.end():closing.start()]
    return COLOPHON.sub("", body)


def normalise(text: str) -> str:
    """One LF-terminated line per source paragraph, punctuation folded to ASCII.

    Paragraphs, not printed lines: the source is hard-wrapped at about seventy
    columns, and a line there is a typesetting accident rather than a unit of
    sense. `guidance/sources.md` requires that a search boundary be a physical
    line, so the unit has to be one the text actually has.
    """
    text = unicodedata.normalize("NFC", text)
    for glyph, plain in _PUNCTUATION.items():
        text = text.replace(glyph, plain)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    paragraphs = re.split(r"\n[ \t]*\n", text)
    lines = []
    for paragraph in paragraphs:
        folded = _SPACE.sub(" ", paragraph.replace("\n", " ")).strip()
        if folded:
            lines.append(folded)
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="the exact downloaded .txt.utf-8 bytes")
    parser.add_argument("--out", required=True)
    arguments = parser.parse_args(argv)

    raw = Path(arguments.source).read_text(encoding="utf-8")
    try:
        body = strip_wrapper(raw)
    except ValueError as error:
        print(f"{arguments.source}: {error}", file=sys.stderr)
        return 2
    derived = normalise(body)
    Path(arguments.out).write_text(derived, encoding="utf-8")
    print(
        f"{arguments.source}: {len(raw)} bytes in, {len(derived.encode())} out, "
        f"{derived.count(chr(10))} lines"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
