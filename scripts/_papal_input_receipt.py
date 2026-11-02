"""Mechanically attested extracts of immutable papal release inputs.

Rows keep their original indices. This metadata never impersonates the original
JSON byte stream or confers review approval. Full audits explicitly resolve and
compare the exact archived originals; ordinary readers open only these records.
"""
from __future__ import annotations

from collections import defaultdict
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import sys

import _snapshot_store

INDEX = "release/papal-documents/input-records.json"
DIRECTORY = "release/papal-documents/input-records"
RELEASE = "release/papal-documents.json"
SCHEMA = "triptych-papal-input-records/v1"
SHARD_SCHEMA = "triptych-papal-input-record/v1"
PROOF = "mechanically-attested-exact-original-extraction/v1"


class InputReceiptError(ValueError):
    pass


def _need(condition, message):
    if not condition:
        raise InputReceiptError(message)


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _bytes(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, f"duplicate input-record JSON key: {key}")
            result[key] = value
        return result

    def constant(value):
        raise InputReceiptError(f"non-finite input-record JSON value: {value}")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def _path(root, value):
    _need(isinstance(value, str) and value and "\\" not in value
          and not any(ord(char) < 32 for char in value), "invalid input-record path")
    path = PurePosixPath(value)
    _need(not path.is_absolute() and all(part not in {"", ".", ".."} for part in value.split("/")),
          "input-record path must be canonical and repository-relative")
    current = root
    for part in path.parts:
        current = current / part
        _need(not current.is_symlink(), "input-record paths must not traverse symlinks")
    return current


def _pin(raw, path):
    return {"path": path, "sha256": _sha(raw), "bytes": len(raw)}


def _same_ref(left, right):
    return all(left.get(key) == right.get(key) for key in ("path", "sha256", "bytes"))


def _shard_membership(root, pins, *, extra_owned=()):
    """Only the exact owned regular shard files may occupy this directory."""
    expected = {pin["path"] for pin in pins.values()} | set(extra_owned)
    directory = _path(root, DIRECTORY)
    actual = set()
    if directory.exists():
        _need(directory.is_dir(), "input-record shard directory is not a directory")
        for path in directory.iterdir():
            _need(not path.is_symlink() and path.is_file(),
                  "input-record shard directory contains a symlink or nonregular entry")
            actual.add(path.relative_to(root).as_posix())
    _need(actual == expected, "input-record physical shard membership differs from its owned index")


def _verified_pin(root, pin):
    path = _path(root, pin["path"])
    _need(path.is_file() and not path.is_symlink(), "owned input-record shard is not a regular file")
    raw = path.read_bytes()
    _need(_same_ref(_pin(raw, pin["path"]), pin), "owned input-record shard hash/size mismatch; preserved")
    return raw


def _closure(release):
    references, slots = {}, defaultdict(set)
    def add(ref, row=False):
        _need(isinstance(ref, dict), "release input reference must be an object")
        path = ref.get("path")
        _need(isinstance(path, str) and path.startswith("release/papal-documents/inputs/"),
              "release snapshot is outside the registered input directory")
        pin = {key: ref.get(key) for key in ("path", "sha256", "bytes")}
        _need(isinstance(pin["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"])
              and type(pin["bytes"]) is int and pin["bytes"] > 0, "invalid exact release input pins")
        _need(path not in references or _same_ref(references[path], pin), "conflicting release input pins")
        references[path] = pin
        if row:
            index = ref.get("row_index")
            _need(type(index) is int and index >= 0, "release input row_index must be a nonnegative integer")
            slots[path].add(index)
    add(release["source_plan"])
    for row in release["documents"]:
        add(row["manifest"], True)
        add(row["receipt"], True)
        add(row["review"]["audit"], True)
    for ref in release.get("evidence", []):
        if ref.get("path", "").startswith("release/papal-documents/inputs/"):
            add(ref)
    return references, {path: sorted(indices) for path, indices in sorted(slots.items())}


def render_records(root, release_bytes, *, originals=None):
    """Verify originals and return metadata writes; never install or approve.

    ``originals`` maps logical archive paths to new transaction input files.
    Existing originals resolve locally only; fetching is a separate operation.
    """
    root, originals = Path(root).resolve(), originals or {}
    release = _json(release_bytes)
    references, slots = _closure(release)
    inventory = {entry["path"]: {"path": entry["path"], "sha256": entry["sha256"], "bytes": entry["bytes"]}
                 for entry in _snapshot_store.load_index(root)["artifacts"]}
    inventory.update(references)
    output, records = {}, {}
    for logical, ref in sorted(inventory.items()):
        physical = originals.get(logical)
        if physical is None:
            physical = _snapshot_store.resolve(root, logical, fetch=False)
        raw = Path(physical).read_bytes()
        _need(_same_ref(_pin(raw, logical), ref), f"original snapshot hash/size mismatch: {logical}")
        if logical not in slots and logical != release["source_plan"]["path"]:
            continue
        data = _json(raw)
        _need(isinstance(data, dict) and isinstance(data.get("documents"), list),
              f"referenced snapshot has no documents array: {logical}")
        complete = logical == release["source_plan"]["path"]
        indices = range(len(data["documents"])) if complete else slots[logical]
        _need(all(index < len(data["documents"]) for index in indices), "release row index exceeds original snapshot")
        _need(all(isinstance(data["documents"][index], dict) for index in indices),
              "selected original document rows must be objects")
        shard = {"schema": SHARD_SCHEMA, "original": ref,
                 "header": {key: value for key, value in data.items() if key != "documents"},
                 "documents_count": len(data["documents"]), "complete_documents": complete,
                 "rows": {str(index): data["documents"][index] for index in indices}}
        target = f"{DIRECTORY}/{ref['sha256']}.json"
        body = _bytes(shard)
        output[target] = body
        records[logical] = _pin(body, target)
    index = {"schema": SCHEMA, "proof": PROOF, "editorial_approval": False,
             "release": _pin(release_bytes, RELEASE), "originals": inventory,
             "required_rows": slots, "records": records}
    output[INDEX] = _bytes(index)
    return output


def record(root, *, scratch=None):
    """Independently verify originals before atomically recording extracts."""
    root = Path(root).resolve()
    index_path = _path(root, INDEX)
    previous_bytes = index_path.read_bytes() if index_path.exists() else None
    previous = InputRecords(root, _previous_owner=True) if previous_bytes is not None else None
    _need((index_path.read_bytes() == previous_bytes) if previous_bytes is not None else not index_path.exists(),
          "input-record index changed during ownership preflight; preserved")
    old_pins = ({pin["path"]: pin for pin in previous.index["records"].values()}
                if previous is not None else {})
    if previous is None:
        _shard_membership(root, {})
    writes = render_records(root, _path(root, RELEASE).read_bytes())
    candidate = _json(writes[INDEX])
    new_paths = {pin["path"] for pin in candidate["records"].values()}
    obsolete = set(old_pins) - new_paths
    scratch = Path(scratch) if scratch is not None else root / ".scratch/papal-input-records"
    scratch.mkdir(parents=True, exist_ok=True)
    for relative, raw in writes.items():
        target = _path(root, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative == INDEX:
            _need((target.read_bytes() == previous_bytes) if previous_bytes is not None else not target.exists(),
                  "input-record index changed while recording; preserved")
            _need(_same_ref(_pin(_path(root, RELEASE).read_bytes(), RELEASE), candidate["release"]),
                  "release changed while recording input metadata")
        if relative in old_pins:
            _verified_pin(root, old_pins[relative])
        elif relative != INDEX:
            _need(not target.exists(), "recording would overwrite an unowned input-record shard")
        if target.exists() and target.read_bytes() == raw:
            continue
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=scratch, delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(raw)
            temporary.chmod(0o644)
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    # New metadata must independently validate before any obsolete old bytes
    # are removed. Only the previous valid index may grant temporary ownership.
    current = InputRecords(root, _extra_owned=obsolete)
    for logical in current.index["records"]:
        current._record(current.index["originals"][logical])
    for relative in obsolete:
        _verified_pin(root, old_pins[relative])
    for relative in sorted(obsolete):
        _verified_pin(root, old_pins[relative])
        _path(root, relative).unlink()
    _shard_membership(root, current.index["records"])
    return {"schema": SCHEMA, "proof": PROOF, "editorial_approval": False,
            "files": len(writes), "bytes": sum(map(len, writes.values())), "pruned": len(obsolete)}


class InputRecords:
    """Explicit original-header/row access, never a reconstructed JSON array."""
    def __init__(self, root, *, _previous_owner=False, _extra_owned=()):
        self.root = Path(root).resolve()
        self.sources = {"scripts/_papal_input_receipt.py", "scripts/_snapshot_store.py", "scripts/_artifact_store.py"}
        self.cache, self.legacy, self.legacy_pins = {}, {}, {}
        self._preloaded = {}
        path = _path(self.root, INDEX)
        self.index = None
        self.plan_path = None
        if not path.exists():
            return
        data = _json(path.read_bytes())
        fields = {"schema", "proof", "editorial_approval", "release", "originals", "required_rows", "records"}
        _need(isinstance(data, dict) and set(data) == fields and data["schema"] == SCHEMA
              and data["proof"] == PROOF and data["editorial_approval"] is False,
              "invalid papal input-record ownership envelope")
        _need(all(isinstance(data[key], dict) for key in ("release", "originals", "required_rows", "records")),
              "invalid papal input-record tables")
        _need(set(data["release"]) == {"path", "sha256", "bytes"}
              and data["release"]["path"] == RELEASE
              and isinstance(data["release"]["sha256"], str)
              and re.fullmatch(r"[0-9a-f]{64}", data["release"]["sha256"])
              and type(data["release"]["bytes"]) is int and data["release"]["bytes"] > 0,
              "invalid input-record release identity")
        release = None
        if not _previous_owner:
            raw = _path(self.root, RELEASE).read_bytes()
            _need(_same_ref(data["release"], _pin(raw, RELEASE)), "input records bind a different release")
            release = _json(raw)
            self.plan_path = release["source_plan"]["path"]
            refs, slots = _closure(release)
        _need(all(isinstance(indices, list) and all(type(index) is int and index >= 0 for index in indices)
                  and indices == sorted(set(indices)) for indices in data["required_rows"].values()),
              "input-record membership requires ordered unique integer row indices")
        if not _previous_owner:
            _need(slots == data["required_rows"], "input-record row membership differs from the complete release")
        for logical, ref in data["originals"].items():
            _need(isinstance(ref, dict) and set(ref) == {"path", "sha256", "bytes"} and ref["path"] == logical,
                  "invalid original input-record identity")
            _snapshot_store.validate_ref(self.root, ref, require_bytes=False)
        declared = {entry["path"]: {"path": entry["path"], "sha256": entry["sha256"], "bytes": entry["bytes"]}
                    for entry in _snapshot_store.load_index(self.root)["artifacts"]}
        _need((all(ref == declared.get(logical) for logical, ref in data["originals"].items())
               if _previous_owner else data["originals"] == declared),
              "input records differ from the complete snapshot delivery inventory")
        if not _previous_owner:
            for logical, ref in refs.items():
                _need(logical in data["originals"] and _same_ref(ref, data["originals"][logical]),
                      "input records omit or change release evidence")
            expected_records = set(slots) | {release["source_plan"]["path"]}
            _need(set(data["records"]) == expected_records, "input-record shard membership differs from the release")
        for logical, pin in data["records"].items():
            _need(isinstance(pin, dict) and set(pin) == {"path", "sha256", "bytes"}
                  and logical in data["originals"]
                  and isinstance(pin["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"])
                  and type(pin["bytes"]) is int and pin["bytes"] > 0
                  and pin["path"] == f"{DIRECTORY}/{data['originals'][logical]['sha256']}.json",
                  "invalid input-record shard path")
        _shard_membership(self.root, data["records"], extra_owned=_extra_owned)
        self.index = data
        self.sources.update({INDEX, _snapshot_store.INDEX_PATH})
        if _previous_owner:
            # A previous release can differ from the new current release.
            # Establish ownership from its strict envelope and every pinned
            # shard, rather than pretending that it is the current approval.
            for logical, pin in data["records"].items():
                body = _json(_verified_pin(self.root, pin))
                _need(isinstance(body, dict), "invalid previous input-record shard")
                self._preloaded[logical] = body
            complete = [logical for logical, body in self._preloaded.items()
                        if body.get("complete_documents") is True]
            _need(len(complete) == 1, "previous input records require one complete source plan")
            self.plan_path = complete[0]
            header = self._preloaded[self.plan_path].get("header")
            _need(isinstance(header, dict) and isinstance(header.get("selection_plan"), dict)
                  and header["selection_plan"].get("schema") == "triptych-papal-source-plan/v1",
                  "previous complete input record is not a source plan")
            _need(set(data["records"]) == set(data["required_rows"]) | {self.plan_path},
                  "previous input-record shard membership is invalid")
            for logical in data["records"]:
                self._record(data["originals"][logical])

    def validate_ref(self, ref):
        if self.index is not None:
            original = self.index["originals"].get(ref.get("path"))
            _need(original is not None and _same_ref(original, ref), "snapshot reference disagrees with input records")
            return original
        # Old local fixtures/checkouts have no delivery declaration. They may
        # use verified original bytes; a declared external never takes this path.
        _need(_snapshot_store.known_external(self.root, ref["path"]) is None,
              "external snapshot requires a recorded header/row extract")
        if ref["path"] not in self.legacy:
            raw = _path(self.root, ref["path"]).read_bytes()
            _need(_same_ref(_pin(raw, ref["path"]), ref), "local snapshot hash/size mismatch")
            self.legacy[ref["path"]] = _json(raw)
            self.legacy_pins[ref["path"]] = _pin(raw, ref["path"])
            self.sources.add(ref["path"])
        _need(_same_ref(self.legacy_pins[ref["path"]], ref), "conflicting local snapshot reference pins")
        return ref

    def _record(self, ref):
        self.validate_ref(ref)
        logical = ref["path"]
        if self.index is None:
            data = self.legacy[logical]
            _need(isinstance(data, dict) and isinstance(data.get("documents"), list), "snapshot requires documents[]")
            return {"header": {key: value for key, value in data.items() if key != "documents"},
                    "documents_count": len(data["documents"]), "complete_documents": True,
                    "rows": {str(index): row for index, row in enumerate(data["documents"])}}
        if logical not in self.cache:
            pin = self.index["records"].get(logical)
            _need(pin is not None, "snapshot has no retained header/row extract")
            if logical in self._preloaded:
                data = self._preloaded.pop(logical)
            else:
                raw = _path(self.root, pin["path"]).read_bytes()
                _need(_same_ref(_pin(raw, pin["path"]), pin), "input-record shard hash/size mismatch")
                data = _json(raw)
            _need(isinstance(data, dict) and set(data) == {"schema", "original", "header", "documents_count", "complete_documents", "rows"}
                  and data["schema"] == SHARD_SCHEMA and isinstance(data["original"], dict)
                  and set(data["original"]) == {"path", "sha256", "bytes"} and _same_ref(data["original"], ref)
                  and isinstance(data["header"], dict) and "documents" not in data["header"]
                  and type(data["documents_count"]) is int and data["documents_count"] >= 0
                  and type(data["complete_documents"]) is bool and isinstance(data["rows"], dict),
                  "invalid original header/row ownership envelope")
            _need(data["complete_documents"] == (logical == self.plan_path),
                  "only the original complete source plan may use complete row iteration")
            for index, row in data["rows"].items():
                _need(index.isascii() and index.isdigit() and str(int(index)) == index
                      and int(index) < data["documents_count"] and isinstance(row, dict),
                      "invalid original row index or row data")
            expected = (set(map(str, range(data["documents_count"]))) if data["complete_documents"]
                        else set(map(str, self.index["required_rows"].get(logical, []))))
            _need(set(data["rows"]) == expected, "input-record row closure is incomplete or enlarged")
            self.cache[logical] = data
            self.sources.add(pin["path"])
        return self.cache[logical]

    def header(self, ref):
        return self._record(ref)["header"]

    def row(self, ref, index):
        record = self._record(ref)
        _need(type(index) is int and 0 <= index < record["documents_count"], "invalid original row_index")
        _need(str(index) in record["rows"], "original row has no retained extraction")
        return record["rows"][str(index)]

    def plan_rows(self, ref):
        record = self._record(ref)
        _need(record["complete_documents"], "source-plan iteration requires complete original row coverage")
        return [record["rows"][str(index)] for index in range(record["documents_count"])]

    def inputs_for(self, *refs):
        paths = {"scripts/_papal_input_receipt.py", "scripts/_snapshot_store.py", "scripts/_artifact_store.py"}
        if self.index is None:
            return paths | {ref["path"] for ref in refs}
        return paths | {INDEX, _snapshot_store.INDEX_PATH} | {
            self.index["records"][ref["path"]]["path"] for ref in refs
        }

    def audit_originals(self, *, fetch=False):
        """Explicitly replay extraction against every exact original snapshot."""
        _need(self.index is not None, "there is no input-record extraction to audit")
        if fetch:
            _snapshot_store.hydrate(self.root, sorted(self.index["originals"]), fetch=True)
        for logical, ref in self.index["originals"].items():
            path = _snapshot_store.resolve(self.root, logical, fetch=False)
            raw = path.read_bytes()
            _need(_same_ref(_pin(raw, logical), ref), "original snapshot changed")
            if logical not in self.index["records"]:
                continue
            original = _json(raw)
            record = self._record(ref)
            _need(record["header"] == {k: v for k, v in original.items() if k != "documents"}
                  and record["documents_count"] == len(original["documents"])
                  and all(row == original["documents"][int(index)] for index, row in record["rows"].items()),
                  "input-record extraction differs from exact original bytes")
        return {"originals": len(self.index["originals"]), "records": len(self.index["records"])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("record", "check", "audit"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--fetch", action="store_true", help="explicitly fetch originals during audit")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        _need(not args.fetch or args.command == "audit", "--fetch is accepted only for an explicit original-byte audit")
        if args.command == "record":
            result = record(root)
        elif args.command == "audit":
            result = InputRecords(root).audit_originals(fetch=args.fetch)
        else:
            import _papal_install as installer
            installer.ROOT = installer.collection.ROOT = root
            result = installer.check_release_metadata()
            result.pop("uninstalled", None)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError) as error:
        print(f"papal input records: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
