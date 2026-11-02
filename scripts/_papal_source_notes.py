"""Exact LF-only paragraph boundaries at explicitly reviewed source positions.

This module does not identify notes, alter words, reorder text, admit sources,
or infer that a chosen range is a complete historical constituent. The caller
supplies an inspected selection and note bounds against an exact source hash.

JSON spec (triptych-papal-source-notes/v1): required source_artifact_id,
repository-relative source_path, source_sha256, physical_line_ranges and
note_line_ranges. Ranges are inclusive, one-based physical LF line pairs.
Optional expected_sha256 must be a lowercase 64-digit output hash when present.
Optional inline_note_boundaries is a nonempty ordered list of exact objects:
{physical_line, source_line_sha256, byte_offset, before_utf8, after_utf8}.
The hash covers the original LF-free line; the zero-based byte offset must be
an interior UTF-8 boundary. Nonempty LF-free anchors match the immediately
adjacent suffix and prefix. Each boundary inserts exactly two LF bytes;
note_line_ranges may be empty only with inline boundaries. Original bytes and
their order are retained. Review of note membership/geometry is separate.

With --json, success/mismatch is one compact stdout object with v=1, status,
source/output/spec hashes, byte/line/group counts and preservation flags.
Inline specs also report inline_boundary_count; source_note_groups includes
each inline boundary. Input errors emit one stderr object with v=1,
status=error, code=input and error. Exit codes: 0 match/derived, 1 check
mismatch, 64 invalid input or refused output. Derive never replaces an input,
specification or differing existing output; an identical output is untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-papal-source-notes/v1"
REQUIRED = {"schema", "source_artifact_id", "source_path", "source_sha256",
            "physical_line_ranges", "note_line_ranges"}
INLINE_FIELDS = {"physical_line", "source_line_sha256", "byte_offset", "before_utf8", "after_utf8"}
DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class SourceNotesError(ValueError):
    """The supplied exact source, ranges or output path is invalid."""


def sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _require(condition, message):
    if not condition:
        raise SourceNotesError(message)


def _unique(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _ranges(value, line_count, label, allow_empty=False):
    _require(isinstance(value, list) and (value or allow_empty), f"{label} must be a nonempty list")
    previous = 0
    for pair in value:
        _require(isinstance(pair, list) and len(pair) == 2
                 and all(type(number) is int for number in pair), f"{label} requires integer pairs")
        start, end = pair
        _require(previous < start <= end <= line_count,
                 f"{label} must be ordered, nonoverlapping and within the source")
        previous = end
    return value


def _inline_boundaries(value, lines, selections):
    _require(isinstance(value, list) and value, "inline_note_boundaries must be a nonempty list")
    result = {}
    previous = (0, 0)
    for entry in value:
        _require(isinstance(entry, dict) and set(entry) == INLINE_FIELDS,
                 "inline boundary fields differ from the schema")
        number, offset = entry["physical_line"], entry["byte_offset"]
        _require(type(number) is int and 1 <= number <= len(lines),
                 "inline physical_line must be an integer within the source")
        _require(any(start <= number <= end for start, end in selections),
                 "inline boundary is outside the selected extent")
        line = lines[number - 1]
        _require(type(offset) is int and 0 < offset < len(line),
                 "inline byte_offset must be an interior integer byte offset")
        _require(previous < (number, offset), "inline boundaries must be ordered and unique")
        previous = (number, offset)
        digest = entry["source_line_sha256"]
        _require(isinstance(digest, str) and DIGEST.fullmatch(digest),
                 "source_line_sha256 must be a bare SHA-256")
        _require(sha(line) == digest, "inline source line SHA-256 mismatch")
        try:
            line[:offset].decode("utf-8")
            line[offset:].decode("utf-8")
        except UnicodeError as error:
            raise SourceNotesError("inline byte_offset splits a UTF-8 character") from error
        anchors = []
        for field in ("before_utf8", "after_utf8"):
            anchor = entry[field]
            _require(isinstance(anchor, str) and bool(anchor.strip()) and "\n" not in anchor,
                     f"inline {field} must be a nonempty LF-free UTF-8 anchor")
            anchors.append(anchor.encode("utf-8"))
        _require(line[:offset].endswith(anchors[0]) and line[offset:].startswith(anchors[1]),
                 "inline boundary anchors do not match adjacent source bytes")
        result.setdefault(number, []).append(offset)
    for number, offsets in result.items():
        line = lines[number - 1]
        limits = [0, *offsets, len(line)]
        _require(all(line[a:b].decode("utf-8").strip() for a, b in zip(limits, limits[1:])),
                 "inline boundaries create a whitespace-only partition")
    return result


def derive(spec: dict, root: Path = ROOT) -> tuple[bytes, dict]:
    """Select exact LF records, inserting only empty LF records around notes."""
    _require(isinstance(spec, dict) and REQUIRED <= set(spec)
             and not set(spec) - REQUIRED - {"expected_sha256", "inline_note_boundaries"},
             "spec fields differ from the schema")
    _require(spec["schema"] == SCHEMA, f"expected {SCHEMA}")
    _require(isinstance(spec["source_artifact_id"], str)
             and re.fullmatch(r"artifact\.[a-z0-9.-]+", spec["source_artifact_id"]),
             "source_artifact_id must name the exact artifact")
    _require(isinstance(spec["source_sha256"], str) and DIGEST.fullmatch(spec["source_sha256"]),
             "source_sha256 must be a bare SHA-256")
    path = spec["source_path"]
    _require(isinstance(path, str) and path and not Path(path).is_absolute()
             and ".." not in Path(path).parts and "\\" not in path, "source_path must be repository-relative")
    root = root.resolve()
    source = (root / path).resolve()
    _require(source.is_relative_to(root), "source_path escapes the supplied root")
    raw = source.read_bytes()
    _require(sha(raw) == spec["source_sha256"], "source SHA-256 mismatch")
    raw.decode("utf-8")
    lines = raw.split(b"\n")
    if lines[-1] == b"":
        lines.pop()
    selections = _ranges(spec["physical_line_ranges"], len(lines), "physical_line_ranges")
    inline = (_inline_boundaries(spec["inline_note_boundaries"], lines, selections)
              if "inline_note_boundaries" in spec else {})
    notes = _ranges(spec["note_line_ranges"], len(lines), "note_line_ranges", allow_empty=bool(inline))
    for start, end in notes:
        _require(any(a <= start <= end <= b for a, b in selections),
                 "a note range is outside or crosses a gap in the selected extent")
        _require(any(line.strip() for line in lines[start - 1:end]), "a note range contains only whitespace")
    before, after = {a for a, b in notes}, {b for a, b in notes}
    pieces, baseline = [], []
    for start, end in selections:
        baseline.append(b"\n".join(lines[start - 1:end]))
        selected = []
        for number in range(start, end + 1):
            if number in before:
                selected.append(b"")
            line = lines[number - 1]
            offsets = [0, *inline.get(number, []), len(line)]
            selected.append(b"\n\n".join(line[a:b] for a, b in zip(offsets, offsets[1:])))
            if number in after:
                selected.append(b"")
        pieces.append(b"\n".join(selected))
    original = b"\n\n".join(baseline) + b"\n"
    payload = b"\n\n".join(pieces) + b"\n"
    _require(original.replace(b"\n", b"") == payload.replace(b"\n", b""), "selected non-LF bytes changed")
    if "expected_sha256" in spec:
        expected = spec["expected_sha256"]
        _require(isinstance(expected, str) and DIGEST.fullmatch(expected), "expected_sha256 must be a bare SHA-256")
        _require(sha(payload) == expected, "derived output SHA-256 differs from expected_sha256")
    report = {"schema": SCHEMA, "source_artifact_id": spec["source_artifact_id"],
              "source_sha256": spec["source_sha256"], "sha256": sha(payload), "bytes": len(payload),
              "physical_lines": len(payload.split(b"\n")) - 1,
              "source_note_groups": len(notes) + sum(map(len, inline.values())),
              "selected_non_lf_sha256": sha(original.replace(b"\n", b"")),
              "selected_non_lf_bytes_preserved": True, "source_order_preserved": True}
    if inline:
        report["inline_boundary_count"] = sum(map(len, inline.values()))
    return payload, report


def _aliases(target, other):
    return target == other.resolve() or (target.exists() and other.exists() and target.samefile(other))


def main(argv=None, examples=None):
    from _tooling import with_examples
    parser = argparse.ArgumentParser(prog="papal-source-notes", description=__doc__)
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name, description in (("derive", "write the exact whitespace-only derivative under .scratch/ or build/"),
                              ("check", "compare an existing derivative with the exact spec replay without writing")):
        command = verbs.add_parser(name, description=description, help=description)
        command.add_argument("--spec", type=Path, required=True, help=f"explicit {SCHEMA} JSON input")
        command.add_argument("--out", type=Path, required=True, help="derivative file to write or check")
        command.add_argument("--root", type=Path, default=ROOT, help="base for the repository-relative source_path")
        command.add_argument("--json", action="store_true", help="emit one compact JSON result")
        if examples:
            with_examples(command, examples[name])
    if examples:
        with_examples(parser, (examples["check"][0], examples["derive"][0]))
    args = parser.parse_args(argv)
    try:
        raw_spec = args.spec.read_bytes()
        spec = json.loads(raw_spec, object_pairs_hook=_unique)
        payload, report = derive(spec, args.root)
        report["spec_sha256"] = sha(raw_spec)
        target = args.out.resolve()
        source = args.root.resolve() / spec["source_path"]
        _require(not _aliases(target, source), "output cannot replace or alias the source")
        _require(not _aliases(target, args.spec), "output cannot replace or alias the specification")
        if args.verb == "derive":
            root = args.root.resolve()
            _require(target.is_relative_to(root / ".scratch") or target.is_relative_to(root / "build"),
                     "derive output must remain under the supplied root's .scratch/ or build/")
            if target.exists():
                _require(target.read_bytes() == payload, "refusing to overwrite differing output")
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(payload)
            report["status"] = "derived"
            code = 0
        else:
            actual = target.read_bytes() if target.is_file() else None
            report["status"] = "pass" if actual == payload else "mismatch"
            report["actual_sha256"] = sha(actual) if actual is not None else None
            code = 0 if actual == payload else 1
        if args.json:
            print(json.dumps(dict(report, v=1), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        else:
            print(f"{args.verb}: {report['status']}; {report['source_note_groups']} note groups; {report['sha256']}")
        return code
    except (OSError, ValueError, UnicodeError) as error:
        if args.json:
            print(json.dumps({"code": "input", "error": str(error), "status": "error", "v": 1},
                             sort_keys=True, separators=(",", ":")), file=sys.stderr)
        else:
            print(f"papal-source-notes: {error}", file=sys.stderr)
        return 64


if __name__ == "__main__":
    raise SystemExit(main())
