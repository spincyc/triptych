"""Offline extraction of CCEL's Matthew/Mark Catena Aurea witnesses.

The output index is a finding aid, never a passage-verification receipt.
Source paragraph classes and printed verse labels are retained independently:
several scripture-class paragraphs contain commentary or malformed numbers.
"""

from __future__ import annotations

import hashlib
import re
import xml.etree.ElementTree as ET


METHOD = "catena-aurea-ccel-paragraphs-v1"


def extract(raw: bytes, book: str, expected_chapters: int) -> tuple[bytes, dict]:
    """Preserve chapter paragraphs in order and index native lemma groups.

    XML character data are joined in document order, whitespace collapsed,
    and one paragraph is written per LF-delimited line. No spelling or verse
    number is repaired. Page markers carry no character data. XML-generated
    navigation, front matter and back indexes are outside the chapter text.
    """
    root = ET.fromstring(raw)
    chapters = [d for d in root.iter("div2")
                if re.fullmatch(r"Chapter [0-9]+", d.get("title", ""))]
    numbers = [int(d.get("title").split()[-1]) for d in chapters]
    if numbers != list(range(1, expected_chapters + 1)):
        raise ValueError(f"chapter sequence mismatch: {numbers}")
    lines, records, blocks = [], [], []
    for chapter, div in zip(numbers, chapters):
        lines.append(div.get("title"))
        group = None
        comment_started = False
        for p in div.iter("p"):
            value = " ".join("".join(p.itertext()).split())
            if not value:
                continue
            lines.append(value)
            line = len(lines)
            label = re.match(r"^(?:Ver\.?\s*)?(\d+)(?:\s*[-–]\s*(\d+))?(?:[.:,]|\s)", value)
            is_lemma = p.get("class") == "scripture"
            record = {"xml_id": p.get("id"), "line": line,
                      "source_class": p.get("class"), "chapter": chapter}
            records.append(record)
            if is_lemma and (group is None or comment_started):
                if group is not None:
                    group["line_end"] = line - 1
                    blocks.append(group)
                group = {"chapter": chapter, "line_start": line,
                         "lemma_lines": [], "lemma_xml_ids": [],
                         "native_verse_labels": [], "unparsed_lemma_lines": [],
                         "state": "mechanical-candidate"}
                comment_started = False
            if group is None:
                raise ValueError(f"unheaded commentary in chapter {chapter}: {p.get('id')}")
            if is_lemma:
                group["lemma_lines"].append(line)
                group["lemma_xml_ids"].append(p.get("id"))
                if label:
                    group["native_verse_labels"].append(
                        [int(label[1]), int(label[2] or label[1])])
                else:
                    group["unparsed_lemma_lines"].append(line)
            else:
                comment_started = True
        if group is None:
            raise ValueError(f"chapter {chapter} has no scripture blocks")
        group["line_end"] = len(lines)
        blocks.append(group)
    text = ("\n".join(lines) + "\n").encode("utf-8")
    index = {"schema": "triptych-catena-aurea-candidates/v1", "method": METHOD,
             "book": book, "input_sha256": hashlib.sha256(raw).hexdigest(),
             "text_sha256": hashlib.sha256(text).hexdigest(),
             "chapter_count": len(chapters), "paragraph_count": len(records),
             "numbering": "native English lemma labels; no canonical projection asserted",
             "verification": "Mechanical boundaries only; no source inspection or Catena admission implied.",
             "paragraphs": records, "blocks": blocks}
    return text, index
