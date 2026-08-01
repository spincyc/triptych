#!/usr/bin/env python3
"""Derive running prose from a MediaWiki export, deterministically.

The declared transformation behind every `web-transcription` artifact taken
from Wikisource. `guidance/sources.md` requires a transformation "exact enough
to re-run", and a paragraph of prose describing one is not: the pilot's own
transcription of Basil's first homily was assembled by hand from a
model-mediated route and split fourteen paragraphs where the printing has
eleven sections, because `<ref>` footnotes carry blank lines and a reader
splitting on blank lines splits inside a footnote. A script cannot make that
mistake twice.

Input is the exact bytes of one `Special:Export` document — a whole retrieval,
hashed, holding every page of the work. Output is one LF-terminated UTF-8 line
per source paragraph, each prefixed by a braced locator naming the page and the
printing's own section number, which is the convention the first landed
transcription set.

    python3 scripts/wikisource_transcribe.py EXPORT.xml --label Homily --roman

Nothing here reaches the network and nothing here consults a model: the bytes
are already on disk when this runs. That separation is the point.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
import xml.etree.ElementTree as ElementTree
from pathlib import Path

# Footnotes first, and before anything splits on a blank line: a <ref> body
# routinely contains one, so a paragraph split performed before this strip
# tears citations out into paragraphs of their own.
_REF = re.compile(r"<ref[^>]*>.*?</ref>|<ref[^>]*/>", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_TAG = re.compile(r"</?[a-zA-Z][^>]*>")
_LINK = re.compile(r"\[\[([^\]|]*)\|([^\]]*)\]\]")
_BARE_LINK = re.compile(r"\[\[([^\]]*)\]\]")
_TEMPLATE_PIPED = re.compile(r"\{\{[^{}|]*\|([^{}]*)\}\}")
_TEMPLATE_BARE = re.compile(r"\{\{[^{}]*\}\}")
_QUOTES = re.compile(r"'''''|'''|''")
# The printing numbers its own sections; the number heads the paragraph that
# opens one and is not part of the sentence.
_SECTION = re.compile(r"^(\d+)\s*\.\s*")
_SPACE = re.compile(r"\s+")
# A wiki heading is the host's structure, not the printing's. `==Footnotes==`
# stands at the foot of every page in this corpus and is not part of any
# section, so it would otherwise be carried onto the end of the last one.
_HEADING = re.compile(r"^\s*=+[^=]*=+\s*$")

_PUNCTUATION = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    " ": " ", " ": " ", " ": " ", " ": " ",
    "′": "'", "″": '"',
}

_ROMAN = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def roman(number: int) -> str:
    out = []
    for value, glyph in _ROMAN:
        while number >= value:
            out.append(glyph)
            number -= value
    return "".join(out)


def _header_stripped(wikitext: str) -> str:
    """Drop the leading `{{header ...}}`, which is navigation and not text."""
    if not wikitext.lstrip().startswith("{{header"):
        return wikitext
    start = wikitext.index("{{header")
    depth = 0
    for position in range(start, len(wikitext) - 1):
        pair = wikitext[position:position + 2]
        if pair == "{{":
            depth += 1
        elif pair == "}}":
            depth -= 1
            if depth == 0:
                return wikitext[position + 2:]
    return wikitext


def clean(fragment: str) -> str:
    """One paragraph of wikitext as running prose, with nothing host-owned left."""
    text = _COMMENT.sub("", fragment)
    text = _REF.sub("", text)
    text = _LINK.sub(r"\2", text)
    text = _BARE_LINK.sub(r"\1", text)
    # Templates nest one deep at most in this corpus; two passes settle them.
    for _ in range(2):
        text = _TEMPLATE_PIPED.sub(r"\1", text)
        text = _TEMPLATE_BARE.sub("", text)
    text = _TAG.sub("", text)
    text = _QUOTES.sub("", text)
    text = html.unescape(text)
    text = "".join(_PUNCTUATION.get(character, character) for character in text)
    # NFC so a combining sequence and its precomposed form do not produce two
    # different files from the same reading.
    text = unicodedata.normalize("NFC", text)
    return _SPACE.sub(" ", text).strip()


def paragraphs(wikitext: str) -> list[str]:
    body = _header_stripped(wikitext)
    out = []
    for block in re.split(r"\n\s*\n", _REF.sub("", body)):
        if _HEADING.match(block):
            continue
        rendered = clean(block)
        if rendered:
            out.append(rendered)
    return out


def transcribe(
    export: Path,
    *,
    label: str,
    use_roman: bool,
    sections: bool,
    drop: list[str],
) -> tuple[str, list[dict]]:
    """The whole export as prose, plus what each line is and where it came from.

    `sections` says whether the printing numbers subdivisions inside a page.
    Basil's homilies do and Gregory's chapters do not, and guessing would give
    one of them a locator that names nothing.
    """
    root = ElementTree.parse(export).getroot()
    dropped = [re.compile(pattern) for pattern in drop]
    lines: list[str] = []
    index: list[dict] = []
    for page in root.findall(".//{*}page"):
        title = page.find("{*}title").text or ""
        revision = page.find("{*}revision")
        number = title.rsplit("/", 1)[-1]
        digits = re.search(r"(\d+)", number)
        unit = roman(int(digits.group(1))) if (use_roman and digits) else (
            digits.group(1) if digits else number)
        section = "0"
        first = len(lines) + 1
        for block in paragraphs(revision.find("{*}text").text or ""):
            opening = _SECTION.match(block) if sections else None
            if opening:
                section = opening.group(1)
                block = block[opening.end():]
            # The printing's running head and its scriptural lemma stand before
            # the first numbered section. They are the editor's furniture and
            # the lemma is scripture, not exposition; neither is the author's
            # prose, so neither enters the transcription. The lemma is recorded
            # on the passage instead, where it says what the fragment is about
            # without pretending to be part of it.
            if not block or (sections and section == "0"):
                continue
            if any(pattern.fullmatch(block) for pattern in dropped):
                continue
            locator = f"{unit}.{section}" if sections else unit
            lines.append(f"{{{locator}}} {block}")
        # A page that yielded nothing is a parse failure, not an empty page, so
        # it is reported rather than skipped silently.
        index.append(
            {
                "title": title,
                "label": f"{label} {unit}",
                "revision": (revision.find("{*}id").text or "").strip(),
                "first_line": first,
                "last_line": len(lines),
            }
        )
    return "".join(line + "\n" for line in lines), index


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("export", type=Path)
    parser.add_argument("--label", default="Section")
    parser.add_argument("--roman", action="store_true",
                        help="number the unit in Roman numerals, as the printing does")
    parser.add_argument("--no-sections", dest="sections", action="store_false",
                        help="the printing numbers no subdivision inside a page")
    parser.add_argument("--drop", action="append", default=[],
                        help="drop a paragraph matching this pattern whole; repeatable")
    parser.add_argument("--out", type=Path)
    arguments = parser.parse_args(argv)
    text, index = transcribe(arguments.export, label=arguments.label,
                            use_roman=arguments.roman, sections=arguments.sections,
                            drop=arguments.drop)
    empty = [entry["title"] for entry in index if entry["last_line"] < entry["first_line"]]
    if empty:
        print(f"no prose parsed from: {'; '.join(empty)}", file=sys.stderr)
        return 2
    if arguments.out:
        arguments.out.parent.mkdir(parents=True, exist_ok=True)
        arguments.out.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    for entry in index:
        print(
            f"{entry['label']}\tlines {entry['first_line']}-{entry['last_line']}"
            f"\trev {entry['revision']}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
