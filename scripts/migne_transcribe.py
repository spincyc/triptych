#!/usr/bin/env python3
"""Derive Migne's Latin from a Latin Wikisource export, deterministically.

The declared transformation behind every `web-transcription` artifact taken from
Latin Wikisource, and the counterpart of `scripts/wikisource_transcribe.py`.
A separate script rather than a flag on that one, because the two printings are
laid out differently and a flag would have made one script's defaults a hazard
to the other's landed output:

    English Wikisource / NPNF   a page is one homily; the printing numbers
                                sections inside it as `1.`, `2.`, at the head of
                                a paragraph.
    Latin Wikisource / Migne    a page is a book or a whole work; the printing
                                divides it into `CAPUT` and prints its own column
                                numbers inline as `(0516C)`, and the wiki carries
                                a `{{titulus2}}` block, a `{{Liber}}` navigation
                                block and a Corpus Corporum provenance line that
                                no reader of Augustine should ever see.

WHAT THIS CORPUS IS. `guidance/catena.md` recorded that "the unencumbered Latin
is OCR wreckage and the clean Latin is encumbered", measuring Migne PL 34's
Internet Archive text layer at roughly one corrupted word in eight. That is true
of the scan and false of the corpus: Latin Wikisource carries the University of
Zurich's Corpus Corporum TEI encodings of Migne, keyed rather than scanned, under
CC BY-SA 4.0 markup over a public-domain 1841-1849 printing. So the Latin is both
clean and unencumbered, and the earlier finding was a property of one route.

WHAT IS REMOVED, AND WHY EACH. Nothing is corrected and nothing is added.

    the header, navigation and provenance templates   the wiki's, not Migne's
    `[[Patrologia Latina/34|...]]` and `[[Categoria:...]]`   the wiki's links
    the Corpus Corporum encoding note                  the encoder's, not the text's
    every `<ref>` body, comment, tag and wiki heading   the wiki's structure
    Migne's column markers `(0516C)`, `(PL 14 0123)`    apparatus, not prose

The column markers are the one debatable removal and it is recorded here rather
than left to be discovered: they are genuine locators into Migne's columns, and
they are also printed mid-sentence, so leaving them in would put a five-character
interruption into every third line of a father's argument. They are stripped from
the prose; the printing they locate is named on the artifact.

WHAT IS UNWRAPPED, AND WHY IT HAD TO BE. Removing every template whole is right
for a corpus whose only templates are furniture, and it was silently wrong for
the first corpus that carried prose inside one. Jerome's *Quaestiones Hebraicae
in Genesim* is about Hebrew and Greek words, and Latin Wikisource holds those
words in `{{Hebraica|...}}` and `{{Graeca|...}}`; its verse numbers are
`{{ancora+|2:8|8}}` and its transliterations `{{font-size|90%|BRESITH}}`. Under
whole-removal the work came out reading "(Vers. .) Et plantavit ... Pro paradiso,
in Hebraeo hortum habet: id est, ()." — deleted content, exit status zero, which
is this repository's named worst failure.

So a template whose name is in `_UNWRAP` yields one named parameter and every
other template is still removed whole. The list is closed and each entry says
which parameter is the prose, because a general rule ("keep the last parameter")
would print `{{titulus2}}`'s `Fons=` line as Bede's. Adding a corpus means
reading its template census first: `_template_census` prints one.

    python3 scripts/migne_transcribe.py EXPORT.xml --unit division --out OUT.txt

Nothing here reaches the network and nothing here consults a model: the bytes are
already on disk, hashed, when this runs. That separation is the point, and it is
why the same corpus that came back as a paraphrase through a model comes back
here as itself.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
import xml.etree.ElementTree as ElementTree
from pathlib import Path

# Footnotes first, and before anything splits on a blank line: a <ref> body can
# contain one, and a split performed first tears citations into paragraphs.
_REF = re.compile(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
_LINK = re.compile(r"\[\[([^\]|]*)\|([^\]]*)\]\]")
_BARE_LINK = re.compile(r"\[\[([^\]]*)\]\]")
_EXTERNAL_LINK = re.compile(r"\[(?:https?|ftp)://[^\s\]]*\s*([^\]]*)\]")
_QUOTES = re.compile(r"'''''|'''|''")
_SPACE = re.compile(r"\s+")

# A wiki heading. In this corpus it is either the printing's own division
# (`==LIBER TERTIUS.==`) or the page number the wiki gave the page (`==1==`);
# either way it is a marker and never prose.
# The heading is matched at the HEAD of a line and whatever follows it on that
# line is kept as text. `==LIBER QUINTUS.== sDe herba seu lignis disputatio.` is
# one line in this corpus, and a whole-line test misses it — which would number
# the ninth book eighth and put every book of Eustathius under the wrong one.
_HEADING = re.compile(r"^\s*(=+)\s*(.+?)\s*\1\s*(.*)$")

# `[[Categoria:...]]` and the Patrologia Latina navigation line are the wiki's
# own furniture. Matched before links are unwrapped, because after unwrapping
# they would be indistinguishable from a sentence.
_CATEGORY = re.compile(r"\[\[\s*Categoria\s*:[^\]]*\]\]", re.IGNORECASE)
_PL_NAVIGATION = re.compile(
    r"^'*\[\[\s*Patrologia Latina/\d+\s*\|[^\]]*\]\]'*\s*$", re.IGNORECASE
)

# Migne's column numbers, printed inline. `(0516C)` is the ordinary form,
# `(PL 14 0123)` the form Ambrose's transcriber used, and `131.0134A` the bare
# form Remigius's did.
_COLUMN = re.compile(r"\((?:PL\s+\d+\s+)?\d{3,4}\s*[A-D]?\)|\b\d{2,3}\.\d{4}[A-D]\b")

# The Corpus Corporum encoding note, which every page of this corpus carries and
# which is the encoder's statement about the file rather than any part of Migne.
_ENCODING_NOTE = re.compile(
    r"this file was encoded in TEI xml for the University of Zurich", re.IGNORECASE
)

# `CAPUT PRIMUM`, `CAPUT II`, `CAP. III` — the printing's own division inside a
# book. Matched only at the head of a paragraph, which is where Migne prints it.
_CAPUT = re.compile(
    r"^\s*(?:CAPUT|CAP\.)\s*(PRIMUM|[IVXLC]+|\d+)\b\s*\.?", re.IGNORECASE
)

_PUNCTUATION = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    " ": " ", " ": " ", " ": " ", " ": " ",
    "′": "'", "″": '"',
}

_ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def arabic(numeral: str) -> int | None:
    """`PRIMUM` and `XIV` alike as a number, or None if it is neither."""
    numeral = numeral.strip().upper()
    if numeral == "PRIMUM":
        return 1
    if numeral.isdigit():
        return int(numeral)
    if not numeral or any(character not in _ROMAN_VALUES for character in numeral):
        return None
    total = 0
    previous = 0
    for character in reversed(numeral):
        value = _ROMAN_VALUES[character]
        total = total - value if value < previous else total + value
        previous = max(previous, value)
    return total


# The templates that carry prose rather than furniture, and which positional
# parameter of each is the prose. Everything absent from this table is removed
# whole. `-1` is the last parameter: `{{font-size|90%|BRESITH}}` prints the
# transliteration and `{{ancora+|2:8|8}}` prints the verse number Migne prints,
# its first parameter being the wiki's own anchor target and not part of the
# printing.
_UNWRAP = {
    "hebraica": 1,      # {{Hebraica|בראשית}} — the Hebrew word under discussion
    "graeca": 1,        # {{Graeca|ἀπὸ ἀρχῆς}} — the Greek Jerome compares
    "font-size": -1,    # {{font-size|90%|BRESITH}} — Migne's small-capital forms
    "ancora+": -1,      # {{ancora+|2:8|8}} — the printed verse number
    "indent": 1,        # {{indent|...}} — an indented paragraph of the printing
    "falseblock": 1,    # {{FalseBlock|verse||-1}} — quoted verse, set as a block
}


def _split_parameters(body: str) -> list[str]:
    """A template body split on its top-level pipes, nesting respected."""

    parameters: list[str] = []
    current: list[str] = []
    depth = 0
    position = 0
    while position < len(body):
        pair = body[position:position + 2]
        if pair in ("{{", "[["):
            depth += 1
            current.append(pair)
            position += 2
            continue
        if pair in ("}}", "]]") and depth:
            depth -= 1
            current.append(pair)
            position += 2
            continue
        if body[position] == "|" and not depth:
            parameters.append("".join(current))
            current = []
            position += 1
            continue
        current.append(body[position])
        position += 1
    parameters.append("".join(current))
    return parameters


def templates_stripped(wikitext: str) -> str:
    """Every `{{...}}` resolved, counting braces rather than matching them.

    A regular expression cannot do this here. `{{titulus2|Scriptor=...|Fons=[...]}}`
    carries pipes and brackets, so the obvious pattern captures the tail of the
    template as though it were text and prints the encoder's metadata as
    Augustine's prose. Counting is exact and terminates.

    A template named in `_UNWRAP` resolves to one of its parameters, recursively,
    because a template may hold another. Every other template resolves to
    nothing, which is what furniture deserves.
    """
    out: list[str] = []
    position = 0
    while position < len(wikitext):
        if wikitext[position:position + 2] != "{{":
            out.append(wikitext[position])
            position += 1
            continue
        depth = 0
        cursor = position
        while cursor < len(wikitext):
            pair = wikitext[cursor:cursor + 2]
            if pair == "{{":
                depth += 1
                cursor += 2
                continue
            if pair == "}}":
                depth -= 1
                cursor += 2
                if not depth:
                    break
                continue
            cursor += 1
        else:
            # An unclosed `{{` runs to the end of the block; drop the rest
            # rather than printing a half-template as prose.
            break
        parameters = _split_parameters(wikitext[position + 2:cursor - 2])
        name = parameters[0].strip().lower()
        keep = _UNWRAP.get(name)
        if keep is not None and len(parameters) > 1:
            chosen = parameters[keep] if keep != -1 else parameters[-1]
            out.append(templates_stripped(chosen))
        position = cursor
    return "".join(out)


def _template_census(export: Path) -> dict[str, int]:
    """Every template name in an export, with its count.

    Read this before transcribing a corpus that has not been transcribed here
    before. A name absent from `_UNWRAP` is removed whole and silently, so a
    corpus that keeps prose in a template must be recognised before its bytes
    are kept, not after they are landed short.
    """
    census: dict[str, int] = {}
    root = ElementTree.parse(export).getroot()
    for page in root.findall(".//{*}page"):
        text = page.find("{*}revision").find("{*}text").text or ""
        for match in re.finditer(r"\{\{\s*([^|}\n]+)", text):
            name = match.group(1).strip()
            census[name] = census.get(name, 0) + 1
    return census


def clean(fragment: str) -> str:
    """One paragraph of wikitext as running prose, with nothing host-owned left."""
    text = _COMMENT.sub("", fragment)
    text = _REF.sub("", text)
    text = _CATEGORY.sub("", text)
    text = templates_stripped(text)
    text = _LINK.sub(r"\2", text)
    text = _BARE_LINK.sub(r"\1", text)
    text = _EXTERNAL_LINK.sub(r"\1", text)
    text = _TAG.sub("", text)
    text = _QUOTES.sub("", text)
    text = _COLUMN.sub("", text)
    text = html.unescape(text)
    text = "".join(_PUNCTUATION.get(character, character) for character in text)
    # NFC so a combining sequence and its precomposed form do not produce two
    # different files from the same reading.
    text = unicodedata.normalize("NFC", text)
    return _SPACE.sub(" ", text).strip()


def transcribe(export: Path, *, unit_from: str) -> tuple[str, list[dict]]:
    """The whole export as prose, plus what each line is and where it came from.

    `unit_from` says what the first half of a locator counts, and the two answers
    are not interchangeable:

        `page`      a multi-page work, one book to a wiki page — Augustine's
                    twelve books are twelve pages, and the page's own subpage
                    number is the book number.
        `division`  a single-page work the printing divides itself — Eustathius's
                    nine books stand under nine `==LIBER ...==` headings on one
                    page, and the page number would say `1` nine times.

    Guessing between them would give one of the two a locator naming nothing.
    """
    root = ElementTree.parse(export).getroot()
    lines: list[str] = []
    index: list[dict] = []
    for page in root.findall(".//{*}page"):
        title = page.find("{*}title").text or ""
        revision = page.find("{*}revision")
        tail = title.rsplit("/", 1)[-1]
        page_unit = arabic(tail) or 1
        division = 0
        unit = page_unit if unit_from == "page" else 0
        caput = 0
        first = len(lines) + 1
        headings: list[str] = []
        for block in re.split(r"\n\s*\n", revision.find("{*}text").text or ""):
            # A heading is taken off the block LINE BY LINE, not by testing the
            # block whole. `==1==\nLIBER PRIMUS.` is one block in this corpus,
            # and a whole-block test leaves the wiki's own page number standing
            # at the head of Augustine's first sentence.
            kept: list[str] = []
            for line in block.split("\n"):
                heading = _HEADING.match(line)
                if not heading:
                    kept.append(line)
                    continue
                division += 1
                headings.append(heading.group(2))
                if heading.group(3):
                    kept.append(heading.group(3))
                if unit_from == "division":
                    unit = division
                    caput = 0
            block = "\n".join(kept)
            if _PL_NAVIGATION.match(block.strip()) or _ENCODING_NOTE.search(block):
                continue
            rendered = clean(block)
            if not rendered:
                continue
            opening = _CAPUT.match(rendered)
            if opening:
                number = arabic(opening.group(1))
                if number is not None:
                    caput = number
                    rendered = rendered[opening.end():].lstrip(" .—-")
                    if not rendered:
                        continue
            # `0` before the first division, and it is not rounded up to `1`:
            # a preface standing before LIBER PRIMUS is not part of it, and
            # numbering it `1` would file the letter to Syncletica inside the
            # first book of the Hexaemeron.
            lines.append(f"{{{unit}.{caput}}} {rendered}")
        index.append(
            {
                "title": title,
                "revision": (revision.find("{*}id").text or "").strip(),
                "divisions": headings,
                "first_line": first,
                "last_line": len(lines),
            }
        )
    return "".join(line + "\n" for line in lines), index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("export", type=Path)
    parser.add_argument(
        "--unit",
        choices=("page", "division"),
        default="page",
        help="what the first half of a locator counts; see transcribe()",
    )
    parser.add_argument("--out", type=Path)
    parser.add_argument(
        "--census",
        action="store_true",
        help="print the export's template names and counts, and transcribe nothing",
    )
    arguments = parser.parse_args(argv)
    if arguments.census:
        for name, count in sorted(_template_census(arguments.export).items()):
            kept = _UNWRAP.get(name.lower())
            disposition = "removed whole" if kept is None else f"unwrapped to parameter {kept}"
            print(f"{count:6d}  {name}\t{disposition}")
        return 0
    text, index = transcribe(arguments.export, unit_from=arguments.unit)
    empty = [entry["title"] for entry in index if entry["last_line"] < entry["first_line"]]
    if empty:
        print(f"no prose parsed from: {'; '.join(empty)}", file=sys.stderr)
        return 1
    for entry in index:
        print(
            f"{entry['title']}\trev {entry['revision']}\t"
            f"lines {entry['first_line']}-{entry['last_line']}\t"
            f"{'; '.join(entry['divisions'])}",
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
