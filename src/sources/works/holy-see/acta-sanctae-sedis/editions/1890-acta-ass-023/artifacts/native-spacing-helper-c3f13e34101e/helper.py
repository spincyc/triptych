"""Project native PDF line whitespace onto an exactly matching retained witness.

This helper never infers words. Every selected source LF line must match one
and only one native extraction line after removing whitespace. Source LF order,
blank lines, glyphs and range order remain unchanged. Native stream-order
differences require an explicit independently reviewed page disposition.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

SCHEMA = "triptych-papal-native-spacing/v1"


class NativeSpacingError(ValueError):
    pass


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def nonspace(text: str) -> str:
    return "".join(char for char in text if not char.isspace())


def project(parent: bytes, native: bytes, first_page: int, selections: list,
            reviewed_stream_order_pages=()) -> tuple[bytes, list, list]:
    """Return whitespace-only bytes, exact line mapping, and stream differences."""
    try:
        source = parent.decode("utf-8").split("\n")
        pages = native.decode("utf-8").split("\f")
    except UnicodeError as error:
        raise NativeSpacingError("inputs must be UTF-8") from error
    if type(first_page) is not int or first_page < 1 or not selections:
        raise NativeSpacingError("explicit first page and nonempty selections required")
    pieces, baseline, mapping, differences = [], [], [], []
    last_source, last_page = 0, 0
    for selection in selections:
        try:
            start, end = selection["source_range"]
            page = selection["native_page"]
        except (KeyError, TypeError, ValueError) as error:
            raise NativeSpacingError("selection requires source range and native page") from error
        if (any(type(n) is not int for n in (start, end, page))
                or not last_source < start <= end <= len(source)
                or not last_page < page or not 0 <= page - first_page < len(pages)):
            raise NativeSpacingError("ranges or pages overlap, reverse, or escape inputs")
        last_source, last_page = end, page
        candidates = collections.defaultdict(list)
        for ordinal, text in enumerate(pages[page - first_page].splitlines(), 1):
            if text.strip():
                candidates[nonspace(text)].append((ordinal, text))
        chosen, original, native_order, used = [], [], [], set()
        for number in range(start, end + 1):
            line = source[number - 1]
            original.append(line)
            if not line.strip():
                chosen.append(line)
                continue
            matches = candidates[nonspace(line)]
            if len(matches) != 1:
                raise NativeSpacingError(f"source LF {number}: expected one native line, found {len(matches)}")
            ordinal, replacement = matches[0]
            if ordinal in used:
                raise NativeSpacingError("a native line cannot witness multiple selected source lines")
            used.add(ordinal)
            native_order.append(ordinal)
            chosen.append(replacement)
            mapping.append({"source_line": number, "native_page": page,
                "native_raw_line": ordinal, "source_line_sha256": digest(line.encode()),
                "recovered_line_sha256": digest(replacement.encode()),
                "nonwhitespace_characters": len(nonspace(line))})
        if native_order != sorted(native_order):
            differences.append(page)
        pieces.append("\n".join(chosen))
        baseline.append("\n".join(original))
    if set(differences) - set(reviewed_stream_order_pages):
        raise NativeSpacingError("native stream-order difference requires independent page review")
    before = "\n\n".join(baseline) + "\n"
    result = "\n\n".join(pieces) + "\n"
    if nonspace(before) != nonspace(result):
        raise NativeSpacingError("non-whitespace characters or source order changed")
    return result.encode(), mapping, differences


def replay(recipe: dict, root: Path) -> tuple[bytes, list, list]:
    if recipe.get("schema") != SCHEMA:
        raise NativeSpacingError("unsupported native-spacing recipe")
    values = []
    for key in ("parent", "native_raw"):
        owner = recipe[key]
        path = (root / owner["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            raise NativeSpacingError("recipe input escapes root")
        data = path.read_bytes()
        if digest(data) != owner["sha256"]:
            raise NativeSpacingError(key + " SHA-256 mismatch")
        values.append(data)
    output, mapping, differences = project(*values, recipe["native_first_page"],
        recipe["selections"], recipe.get("reviewed_stream_order_pages", []))
    if digest(output) != recipe["output_sha256"]:
        raise NativeSpacingError("output SHA-256 mismatch")
    if differences != recipe.get("stream_order_difference_pages"):
        raise NativeSpacingError("native stream-order disposition differs")
    return output, mapping, differences


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args(argv)
    output, mapping, differences = replay(json.loads(arguments.recipe.read_text()), arguments.root)
    if arguments.check:
        if arguments.out.read_bytes() != output:
            raise NativeSpacingError("retained output differs from replay")
    elif arguments.out.exists() and arguments.out.read_bytes() != output:
        raise NativeSpacingError("refusing to overwrite differing bytes")
    else:
        arguments.out.write_bytes(output)
    print(json.dumps({"status": "pass", "sha256": digest(output),
        "matched_source_lines": len(mapping), "stream_order_difference_pages": differences}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
