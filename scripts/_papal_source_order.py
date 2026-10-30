"""Replay explicitly reviewed note-column byte slices; never infer source words."""
from __future__ import annotations

import hashlib
from pathlib import Path
import re

SCHEMA = "triptych-papal-source-order/v1"
REQUIRED = {"schema", "source_artifact_id", "source_path", "source_sha256",
            "physical_line_ranges", "note_groups"}


class SourceOrderError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise SourceOrderError(message)


def _integer(value):
    return type(value) is int


def _range(value, low, high):
    _require(isinstance(value, list) and len(value) == 2
             and all(_integer(n) for n in value), "range requires two integers")
    a, b = value
    _require(low <= a <= b <= high, "range escapes source bounds")
    return a, b


def derive(spec: dict, root: Path) -> tuple[bytes, dict]:
    _require(isinstance(spec, dict) and REQUIRED <= set(spec)
             and not set(spec) - REQUIRED - {"expected_sha256"}
             and spec.get("schema") == SCHEMA, "unsupported source-order schema or fields")
    _require(isinstance(spec.get("source_artifact_id"), str)
             and re.fullmatch(r"artifact\.[a-z0-9.-]+", spec["source_artifact_id"]),
             "source artifact identity required")
    path_value = spec.get("source_path")
    _require(isinstance(path_value, str) and path_value and not Path(path_value).is_absolute()
             and ".." not in Path(path_value).parts and "\\" not in path_value,
             "source path must be repository-relative")
    root = root.resolve()
    path = (root / path_value).resolve()
    _require(path.is_relative_to(root), "source path escapes root")
    source = path.read_bytes()
    expected = spec.get("source_sha256")
    _require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected), "source SHA-256 required")
    _require(hashlib.sha256(source).hexdigest() == expected, "source SHA-256 mismatch")
    source.decode("utf-8")
    lines = source.split(b"\n")
    if lines[-1] == b"":
        lines.pop()
    selections = spec.get("physical_line_ranges")
    _require(isinstance(selections, list) and selections, "nonempty source selections required")
    selected = []
    last = 0
    for selection in selections:
        a, b = _range(selection, 1, len(lines))
        _require(a > last, "source selections overlap or reverse")
        selected.extend(range(a, b + 1))
        last = b
    selected_set = set(selected)
    groups = spec.get("note_groups")
    _require(isinstance(groups, list) and groups, "explicit note groups required")
    compiled, occupied, group_ids = {}, set(), set()
    for group in groups:
        _require(isinstance(group, dict), "note group must be an object")
        _require(set(group) == {"id", "geometry_basis", "physical_line_range", "slices", "order", "block_starts"},
                 "note group fields differ from schema")
        group_id = group.get("id")
        _require(isinstance(group_id, str) and group_id and group_id not in group_ids, "unique note group identity required")
        group_ids.add(group_id)
        _require(isinstance(group.get("geometry_basis"), str) and group["geometry_basis"].strip(),
                 "native geometry review basis required")
        a, b = _range(group.get("physical_line_range"), 1, len(lines))
        required_lines = set(range(a, b + 1))
        _require(required_lines <= selected_set, "note group escapes source selection")
        _require(not occupied & required_lines, "note groups overlap")
        occupied.update(required_lines)
        slices = group.get("slices")
        _require(isinstance(slices, list) and slices, "explicit source slices required")
        units, spans = {}, {n: [] for n in required_lines}
        for unit in slices:
            _require(isinstance(unit, dict), "source slice must be an object")
            _require(set(unit) == {"id", "physical_line", "byte_range"}, "slice fields differ from schema")
            identity, number = unit.get("id"), unit.get("physical_line")
            _require(isinstance(identity, str) and identity and identity not in units, "unique slice identity required")
            _require(_integer(number) and number in required_lines, "slice escapes note group")
            start, end = _range(unit.get("byte_range"), 0, len(lines[number - 1]))
            value = lines[number - 1][start:end]
            try:
                value.decode("utf-8")
                lines[number - 1][:start].decode("utf-8")
                lines[number - 1][end:].decode("utf-8")
            except UnicodeError as error:
                raise SourceOrderError("slice splits a UTF-8 character") from error
            _require(start < end or not lines[number - 1], "empty slice of a nonempty line")
            units[identity] = value
            spans[number].append((start, end))
        for number, values in spans.items():
            cursor = 0
            _require(values, "source line omitted from slices")
            for start, end in sorted(values):
                _require(start == cursor, "source slices overlap or leave a gap")
                cursor = end
            _require(cursor == len(lines[number - 1]), "source slice coverage incomplete")
            _require(len(values) == 1 or all(start < end for start, end in values), "duplicate empty slices")
        order = group.get("order")
        _require(isinstance(order, list) and all(isinstance(v, str) for v in order)
                 and len(order) == len(units) and len(set(order)) == len(order)
                 and set(order) == set(units), "order must use every slice exactly once")
        starts = group.get("block_starts", [])
        _require(isinstance(starts, list) and all(isinstance(v, str) for v in starts)
                 and len(set(starts)) == len(starts) and set(starts) <= set(units), "invalid block-start slices")
        text = b"\n"
        for identity in order:
            if identity in starts:
                text += b"\n"
            text += units[identity] + b"\n"
        compiled[a] = (b, text + b"\n")
    result, index = [], 0
    while index < len(selected):
        number = selected[index]
        if number in compiled:
            end, text = compiled[number]
            result.append(text)
            index += end - number + 1
        else:
            result.append(lines[number - 1] + b"\n")
            index += 1
    output = b"".join(result)
    if "expected_sha256" in spec:
        _require(spec["expected_sha256"] == hashlib.sha256(output).hexdigest(), "output SHA-256 mismatch")
    return output, {"schema": SCHEMA, "source_sha256": expected,
                    "output_sha256": hashlib.sha256(output).hexdigest(),
                    "selected_physical_lines": len(selected), "note_groups": len(groups),
                    "limitations": "Explicit source-unit preservation and permutation only; native geometry and note ownership require separate review."}


def _unique(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def main(argv=None, examples=None):
    import argparse
    import json
    from _tooling import with_examples
    parser = argparse.ArgumentParser(prog="papal-source-order", description=__doc__)
    verbs = parser.add_subparsers(dest="command", required=True)
    for name in ("derive", "check"):
        command = verbs.add_parser(name, description="Explicit source-unit preservation; native geometry requires separate review.")
        command.add_argument("--spec", required=True, type=Path)
        command.add_argument("--out", required=True, type=Path)
        command.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
        command.add_argument("--json", action="store_true")
        if examples:
            with_examples(command, examples[name])
    if examples:
        with_examples(parser, (examples["derive"][0], examples["check"][0]))
    args = parser.parse_args(argv)
    try:
        try:
            raw_spec = args.spec.read_bytes()
            spec = json.loads(raw_spec, object_pairs_hook=_unique)
        except (OSError, json.JSONDecodeError) as error:
            raise SourceOrderError("source-order spec is not readable JSON") from error
        data, result = derive(spec, args.root)
        result["spec_sha256"] = hashlib.sha256(raw_spec).hexdigest()
        output = args.out.resolve()
        root = args.root.resolve()
        allowed = any(output.is_relative_to(root / part) for part in (".scratch", "build"))
        if args.command == "derive" and not allowed:
            raise SourceOrderError("derivation output must remain under root .scratch or build")
        if output == args.spec.resolve():
            raise SourceOrderError("output cannot replace specification")
        if args.command == "check":
            if not output.is_file() or output.read_bytes() != data:
                raise SourceOrderError("retained output differs from replay")
        elif output.exists():
            if output.read_bytes() != data:
                raise SourceOrderError("refusing to overwrite differing output")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
        result["status"] = "pass"
        print(json.dumps(result, sort_keys=True) if args.json else "source-order replay PASS: " + result["output_sha256"])
        return 0
    except (SourceOrderError, OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        result = {"status": "error", "error": str(error)}
        print(json.dumps(result, sort_keys=True) if args.json else "papal-source-order: " + str(error))
        return 1
