"""Exact LF-only paragraph boundaries around explicitly reviewed note ranges.

This module does not identify notes, alter words, reorder text, admit sources,
or infer that a chosen range is a complete historical constituent. The caller
supplies an inspected selection and note bounds against an exact source hash.
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


def _ranges(value, line_count, label):
    _require(isinstance(value, list) and value, f"{label} must be a nonempty list")
    previous = 0
    for pair in value:
        _require(isinstance(pair, list) and len(pair) == 2
                 and all(type(number) is int for number in pair), f"{label} requires integer pairs")
        start, end = pair
        _require(previous < start <= end <= line_count,
                 f"{label} must be ordered, nonoverlapping and within the source")
        previous = end
    return value


def derive(spec: dict, root: Path = ROOT) -> tuple[bytes, dict]:
    """Select exact LF records, inserting only empty LF records around notes."""
    _require(isinstance(spec, dict) and REQUIRED <= set(spec)
             and not set(spec) - REQUIRED - {"expected_sha256"}, "spec fields differ from the schema")
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
    notes = _ranges(spec["note_line_ranges"], len(lines), "note_line_ranges")
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
            selected.append(lines[number - 1])
            if number in after:
                selected.append(b"")
        pieces.append(b"\n".join(selected))
    original = b"\n\n".join(baseline) + b"\n"
    payload = b"\n\n".join(pieces) + b"\n"
    _require(original.replace(b"\n", b"") == payload.replace(b"\n", b""), "selected non-LF bytes changed")
    expected = spec.get("expected_sha256")
    if expected is not None:
        _require(isinstance(expected, str) and DIGEST.fullmatch(expected), "expected_sha256 must be a bare SHA-256")
        _require(sha(payload) == expected, "derived output SHA-256 differs from expected_sha256")
    report = {"schema": SCHEMA, "source_artifact_id": spec["source_artifact_id"],
              "source_sha256": spec["source_sha256"], "sha256": sha(payload), "bytes": len(payload),
              "physical_lines": len(payload.split(b"\n")) - 1, "source_note_groups": len(notes),
              "selected_non_lf_sha256": sha(original.replace(b"\n", b"")),
              "selected_non_lf_bytes_preserved": True, "source_order_preserved": True}
    return payload, report


def main(argv=None):
    parser = argparse.ArgumentParser(prog="papal-source-notes", description=__doc__)
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name, description in (("derive", "write the exact whitespace-only derivative under .scratch/ or build/"),
                              ("check", "compare an existing derivative with the exact spec replay without writing")):
        command = verbs.add_parser(name, description=description, help=description)
        command.add_argument("--spec", type=Path, required=True, help=f"explicit {SCHEMA} JSON input")
        command.add_argument("--out", type=Path, required=True, help="derivative file to write or check")
        command.add_argument("--root", type=Path, default=ROOT, help="base for the repository-relative source_path")
        command.add_argument("--json", action="store_true", help="emit one compact JSON result")
    args = parser.parse_args(argv)
    try:
        raw_spec = args.spec.read_bytes()
        spec = json.loads(raw_spec, object_pairs_hook=_unique)
        payload, report = derive(spec, args.root)
        report["spec_sha256"] = sha(raw_spec)
        target = args.out.resolve()
        if args.verb == "derive":
            root = args.root.resolve()
            _require(target.is_relative_to(root / ".scratch") or target.is_relative_to(root / "build"),
                     "derive output must remain under the supplied root's .scratch/ or build/")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
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
