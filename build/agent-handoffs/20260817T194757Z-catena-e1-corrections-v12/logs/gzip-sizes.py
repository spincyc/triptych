#!/usr/bin/env python3
"""Measure the route's byte budgets exactly as the test suite enforces them.

gzip -9, mtime pinned to zero; `stripped` removes comments the same way
`without_comments` in `tools/tests/test_catena_wave_1.py` does. One
measurement, taken by one program, in the format the previous packages used.

Usage: gzip-sizes.py src/web/browser/catena
"""
import gzip
import re
import sys
from pathlib import Path


def gz(text: str) -> int:
    return len(gzip.compress(text.encode("utf-8"), 9, mtime=0))


def without_comments(text: str, *, script: bool = False) -> str:
    stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    if script:
        stripped = re.sub(r"^\s*//.*$", "", stripped, flags=re.M)
    return stripped


def main() -> int:
    root = Path(sys.argv[1])
    for name, script in (("catena.css", False), ("catena.js", True),
                         ("catena-model.js", True)):
        text = (root / name).read_text(encoding="utf-8")
        print(f"{name} whole {gz(text)} "
              f"stripped {gz(without_comments(text, script=script))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
