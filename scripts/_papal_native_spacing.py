"""Project native PDF line whitespace onto an exactly matching retained witness.

This helper never infers words. Each selected nonblank source LF line must
uniquely match a native line after removing whitespace, unless an explicit
hash-pinned retention record preserves the original line. Legacy retention
requires zero matches; preserve_original:true also requires an exact
native_match_count and claims no native line identity. Source LF order, blank
lines, glyphs and range order remain unchanged. Native stream-order differences
require an explicit independently reviewed page disposition.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path
import re

from _tooling import Example, with_examples

SCHEMA = "triptych-papal-native-spacing/v1"
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
RECIPE_FIELDS = {"schema", "parent", "native_raw", "native_first_page", "selections",
    "output_sha256", "reviewed_stream_order_pages", "stream_order_difference_pages",
    "retained_source_lines", "helper", "native_pdf", "review", "source_id"}
RETAINED_FIELDS = {"source_line", "source_line_sha256", "native_page", "reason"}
PRESERVED_FIELDS = RETAINED_FIELDS | {"preserve_original", "native_match_count"}


class NativeSpacingError(ValueError):
    pass


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def nonspace(text: str) -> str:
    return "".join(char for char in text if not char.isspace())


def project(parent: bytes, native: bytes, first_page: int, selections: list,
            reviewed_stream_order_pages=(), retained_source_lines=()) -> tuple[bytes, list, list]:
    """Return whitespace-only bytes, exact line mapping, and stream differences."""
    try:
        source = parent.decode("utf-8").split("\n")
        if source[-1] == "":
            source.pop()  # A terminal LF is not an additional physical record.
        pages = native.decode("utf-8").split("\f")
        if pages[-1] == "":
            pages.pop()  # A terminal form feed is not a further PDF page.
    except UnicodeError as error:
        raise NativeSpacingError("inputs must be UTF-8") from error
    if (type(first_page) is not int or first_page < 1
            or not isinstance(selections, list) or not selections):
        raise NativeSpacingError("explicit first page and nonempty selections required")
    if (not isinstance(reviewed_stream_order_pages, (list, tuple))
            or any(type(n) is not int or n < 1 for n in reviewed_stream_order_pages)
            or len(set(reviewed_stream_order_pages)) != len(reviewed_stream_order_pages)):
        raise NativeSpacingError("reviewed stream-order pages must be unique positive integers")
    if not isinstance(retained_source_lines, (list, tuple)):
        raise NativeSpacingError("retained source lines require explicit records")
    retained = {}
    for entry in retained_source_lines:
        if (not isinstance(entry, dict)
                or set(entry) not in (RETAINED_FIELDS, PRESERVED_FIELDS)
                or type(entry["source_line"]) is not int or entry["source_line"] < 1
                or type(entry["native_page"]) is not int or entry["native_page"] < 1
                or not isinstance(entry["source_line_sha256"], str)
                or not DIGEST.fullmatch(entry["source_line_sha256"])
                or not isinstance(entry["reason"], str) or not entry["reason"].strip()
                or entry["source_line"] in retained):
            raise NativeSpacingError("retained source lines require unique, hash-pinned, reasoned records")
        if "preserve_original" in entry and (entry["preserve_original"] is not True
                or type(entry["native_match_count"]) is not int
                or entry["native_match_count"] < 0):
            raise NativeSpacingError("preserved source lines require true preserve_original and a nonnegative integer native_match_count")
        retained[entry["source_line"]] = entry
    retained_used = set()
    pieces, baseline, mapping, differences = [], [], [], []
    last_source, last_page = 0, 0
    for selection in selections:
        if not isinstance(selection, dict) or set(selection) != {"source_range", "native_page"}:
            raise NativeSpacingError("selection requires only source range and native page")
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
        for ordinal, text in enumerate(pages[page - first_page].split("\n"), 1):
            if text.strip():
                candidates[nonspace(text)].append((ordinal, text))
        chosen, original, native_order, used = [], [], [], set()
        for number in range(start, end + 1):
            line = source[number - 1]
            original.append(line)
            if not line.strip():
                if number in retained:
                    raise NativeSpacingError("retained source line cannot name a blank record")
                chosen.append(line)
                continue
            matches = candidates[nonspace(line)]
            if number in retained:
                entry = retained[number]
                if (entry["native_page"] != page
                        or entry["source_line_sha256"] != digest(line.encode())):
                    raise NativeSpacingError("retained source line page or SHA-256 mismatch")
                if "preserve_original" in entry:
                    if len(matches) != entry["native_match_count"]:
                        raise NativeSpacingError("preserved source line native_match_count mismatch")
                elif matches:
                    raise NativeSpacingError("retained source line must have zero native matches")
                retained_used.add(number)
                chosen.append(line)
                mapping.append({"source_line": number, "native_page": page,
                    "source_line_sha256": digest(line.encode()),
                    "recovered_line_sha256": digest(line.encode()),
                    "nonwhitespace_characters": len(nonspace(line)),
                    "origin": "retained-original", "retention_reason": entry["reason"]})
                if "preserve_original" in entry:
                    mapping[-1]["native_match_count"] = len(matches)
                continue
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
            if retained:
                mapping[-1]["origin"] = "native-whitespace"
        if native_order != sorted(native_order):
            differences.append(page)
        pieces.append("\n".join(chosen))
        baseline.append("\n".join(original))
    if retained_used != set(retained):
        raise NativeSpacingError("retained source line is outside the selected extent")
    if set(reviewed_stream_order_pages) != set(differences):
        raise NativeSpacingError("native stream-order difference requires exact independent page review")
    before = "\n\n".join(baseline) + "\n"
    result = "\n\n".join(pieces) + "\n"
    if nonspace(before) != nonspace(result):
        raise NativeSpacingError("non-whitespace characters or source order changed")
    return result.encode(), mapping, differences


def replay(recipe: dict, root: Path) -> tuple[bytes, list, list]:
    if not isinstance(recipe, dict) or recipe.get("schema") != SCHEMA:
        raise NativeSpacingError("unsupported native-spacing recipe")
    if set(recipe) - RECIPE_FIELDS:
        raise NativeSpacingError("unknown native-spacing recipe field")
    required = {"schema", "parent", "native_raw", "native_first_page", "selections",
        "output_sha256", "stream_order_difference_pages"}
    if not required <= set(recipe):
        raise NativeSpacingError("incomplete native-spacing recipe")
    values = []
    for key in ("parent", "native_raw"):
        owner = recipe[key]
        if (not isinstance(owner, dict) or set(owner) != {"path", "sha256", "artifact_id"}
                or not isinstance(owner["artifact_id"], str) or not owner["artifact_id"]
                or not isinstance(owner["path"], str) or not owner["path"]
                or Path(owner["path"]).is_absolute() or ".." in Path(owner["path"]).parts
                or "\\" in owner["path"] or Path(owner["path"]).as_posix() != owner["path"]
                or not isinstance(owner["sha256"], str) or not DIGEST.fullmatch(owner["sha256"])):
            raise NativeSpacingError("recipe inputs require exact artifact, relative path and SHA-256 records")
        path = (root / owner["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            raise NativeSpacingError("recipe input escapes root")
        data = path.read_bytes()
        if digest(data) != owner["sha256"]:
            raise NativeSpacingError(key + " SHA-256 mismatch")
        values.append(data)
    output, mapping, differences = project(*values, recipe["native_first_page"],
        recipe["selections"], recipe.get("reviewed_stream_order_pages", []),
        recipe.get("retained_source_lines", []))
    if digest(output) != recipe["output_sha256"]:
        raise NativeSpacingError("output SHA-256 mismatch")
    if differences != recipe.get("stream_order_difference_pages"):
        raise NativeSpacingError("native stream-order disposition differs")
    return output, mapping, differences


def main(argv=None):
    parser = with_examples(argparse.ArgumentParser(prog="papal-native-spacing", description=__doc__), EXAMPLES)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise NativeSpacingError("duplicate JSON key: " + key)
            value[key] = item
        return value
    recipe = json.loads(arguments.recipe.read_text(), object_pairs_hook=unique,
        parse_constant=lambda value: (_ for _ in ()).throw(NativeSpacingError("non-finite JSON number")))
    output, mapping, differences = replay(recipe, arguments.root)
    target = arguments.out.resolve()
    protected = {arguments.recipe.resolve(),
        *((arguments.root / recipe[key]["path"]).resolve() for key in ("parent", "native_raw"))}
    if target in protected or (target.exists() and any(target.samefile(p) for p in protected)):
        raise NativeSpacingError("output aliases a retained input or recipe")
    if not arguments.check:
        root = arguments.root.resolve()
        if not any(target.is_relative_to(root / name) for name in (".scratch", "build")):
            raise NativeSpacingError("derivation output must be under root .scratch or build")
    if arguments.check:
        if arguments.out.read_bytes() != output:
            raise NativeSpacingError("retained output differs from replay")
    elif arguments.out.exists() and arguments.out.read_bytes() != output:
        raise NativeSpacingError("refusing to overwrite differing bytes")
    else:
        arguments.out.write_bytes(output)
    print(json.dumps({"v": 1, "status": "pass", "sha256": digest(output),
        "matched_source_lines": sum(r.get("origin") != "retained-original" for r in mapping),
        "retained_source_lines": sorted(r["source_line"] for r in mapping if r.get("origin") == "retained-original"),
        "stream_order_difference_pages": differences}, sort_keys=True, separators=(",", ":")))
    return 0


# Captured output is populated from the real, read-only canonical recipe check.
EXAMPLES = (
    Example('tools/papal-native-spacing --recipe src/sources/works/holy-see/acta-sanctae-sedis/editions/1890-acta-ass-023/artifacts/rerum-novarum-native-spacing-recipe-dc192a445cd4/recipe.json --out src/sources/works/holy-see/acta-sanctae-sedis/editions/1890-acta-ass-023/artifacts/rerum-novarum-native-spacing-e1de8d5325c3/text.txt --check --json',
        ('{"matched_source_lines":1178,"retained_source_lines":[],"sha256":"e1de8d5325c3d76a8b7826d8ca0ecde983ef6849c3a8be8691efab7b90828dcf","status":"pass","stream_order_difference_pages":[647,648,651,653,654,656,662,664,670],"v":1}',),
        "Read-only replay of the retained Rerum novarum whitespace derivative."),
)

if __name__ == "__main__":
    raise SystemExit(main())
