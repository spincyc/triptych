#!/usr/bin/env python3
"""Replay one exact Acta constituent's whitespace-only note partition.

The original source is retained unchanged. This program selects the same
physical LF ranges and inserts an empty LF record before and after each
identified source-page note group. It changes no other byte in that selection.
No word, punctuation, reference mark, date or source order is corrected.
"""
import argparse
import hashlib
from pathlib import Path

SOURCE = 'src/sources/works/holy-see/acta-sanctae-sedis/editions/1893-acta-ass-026/artifacts/acta-historical-text-15a33cfd/historical.txt'
SOURCE_SHA256 = '15a33cfd01401e070c0b912e4154be4f7d163d6730ac8f1cd64ed6096d756d3d'
RANGES = [[5084, 5124], [5127, 5166], [5168, 5208], [5210, 5249], [5251, 5291], [5293, 5332], [5334, 5374], [5376, 5398]]
NOTE_RANGES = [[5166, 5166], [5208, 5208], [5373, 5374]]
OUTPUT_SHA256 = '7ab62b9810a84b23add5f7f8311c82b5fe032cd971f9ad5f5a2cd53ab384db9a'

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--root", type=Path, default=Path("."))
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
raw = (args.root / SOURCE).read_bytes()
assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "source SHA-256 mismatch"
lines = raw.split(b"\n")
before, after = {a for a, b in NOTE_RANGES}, {b for a, b in NOTE_RANGES}
pieces, baseline = [], []
for start, end in RANGES:
    baseline.append(b"\n".join(lines[start - 1:end]))
    selected = []
    for number in range(start, end + 1):
        if number in before:
            selected.append(b"")
        selected.append(lines[number - 1])
        if number in after:
            selected.append(b"")
    pieces.append(b"\n".join(selected))
expected = b"\n\n".join(baseline) + b"\n"
result = b"\n\n".join(pieces) + b"\n"
assert expected.replace(b"\n", b"") == result.replace(b"\n", b""), "non-LF bytes changed"
assert hashlib.sha256(result).hexdigest() == OUTPUT_SHA256, "replay output SHA-256 mismatch"
args.out.write_bytes(result)
print(OUTPUT_SHA256)
