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

SOURCE = 'src/sources/works/holy-see/acta-apostolicae-sedis/editions/1914-acta-aas-006/artifacts/acta-historical-text-fb3b4bd1/historical.txt'
SOURCE_SHA256 = 'fb3b4bd1a8d41392dc06fc705d97bac09d7aee15780990391456a948f9ea3c67'
RANGES = [[26947, 26988], [26990, 27034], [27036, 27086], [27089, 27139], [27141, 27190], [27192, 27232], [27234, 27276], [27278, 27325], [27327, 27371], [27373, 27415], [27417, 27461], [27463, 27504], [27506, 27557], [27559, 27592]]
NOTE_RANGES = [[26983, 26988], [27031, 27034], [27077, 27086], [27130, 27139], [27181, 27190], [27275, 27276], [27320, 27325], [27368, 27371], [27414, 27415], [27458, 27461], [27504, 27504], [27548, 27557], [27590, 27590]]
OUTPUT_SHA256 = 'b9ec3e96fde193ae319d9139ae1f2d4fd123e8aef878896d9f41fff8a1977677'

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
