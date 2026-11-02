#!/usr/bin/env python3
"""Replay exact source XML WORD rectangles without lexical correction."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parent
audit = json.loads((ROOT / "geometry-selection.json").read_text())
xml_bytes = (ROOT / audit["source_xml"]).read_bytes()
assert hashlib.sha256(xml_bytes).hexdigest() == audit["source_xml_sha256"]
objects = E.fromstring(xml_bytes).findall(".//OBJECT")
blocks = []
for page in audit["pages"]:
    obj = objects[page["page"] - 1]
    for para in obj.iter("PARAGRAPH"):
        text = []
        for line in para.iter("LINE"):
            words = []
            for word in line.iter("WORD"):
                raw = "".join(word.itertext())
                c = list(map(int, word.get("coords").split(",")))
                cx, cy = (c[0] + c[2]) / 2, (c[1] + c[3]) / 2
                if page["word_center_x_min"] <= cx <= page["word_center_x_max"] and page["word_center_y_min"] <= cy <= page["word_center_y_max"]:
                    words.append((raw, c))
            if words and re.fullmatch(r"\d{1,4}", " ".join(w[0] for w in words)) and min(min(w[1][1], w[1][3]) for w in words) > int(obj.get("height")) * .88:
                words = []
            if words:
                text.append(" ".join(w[0] for w in words))
        if text:
            blocks.append(" ".join(text))
output = ("\n\n".join(blocks) + "\n").encode()
assert hashlib.sha256(output).hexdigest() == audit["output_sha256"]
assert len(output) == audit["output_bytes"]
(ROOT / audit["output"]).write_bytes(output)
