#!/usr/bin/env python3
"""Check the exact identity of a mechanically replayed act-history projection.

``record`` independently builds into exclusive scratch space and refuses any
installed-byte drift before writing. It never installs or adopts generated
bytes. ``check`` hashes the complete recognized source, policy and generator
closure and every installed output; no timestamp or cached projection can
establish currentness. The tracked receipt is mechanical evidence, not a
content, rights or publication approval. The release checker must bind its
bytes along with the other reviewed source inputs.

The exhaustive gate remains ``tools/tpt act-history structure --check``.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

# A receipt must execute the source code whose bytes it records. -B alone
# suppresses writes but still accepts old timestamp-keyed bytecode. No file or
# directory is created at this unique prefix; repository imports compile .py.
if __name__ == "__main__":
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(Path(__file__).resolve().parents[1]
                            / ".scratch/act-history-perf"
                            / ("no-bytecode-" + os.urandom(16).hex()))

from _source_projection_receipt import ReceiptError, input_identity, output_identity


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = Path("src/sources/inventories/act-history-projection-receipt-v1.json")
PROJECTION = Path("src/web/data/structure/act-history")
SCHEMA = "triptych-act-history-projection-receipt/v1"
PROOF = "independent-replay-and-exact-installed-byte-comparison"
SUMMARY_KEYS = ("files", "slices", "stations", "lines", "default")


def _tool():
    # Only execute the tool in this checkout; an alternate data root cannot
    # replace trusted code. Kept separate so small mutation tests need no corpus.
    loader = importlib.machinery.SourceFileLoader(
        "_act_history_projection_receipt_tool", str(ROOT / "tools/act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise ReceiptError("cannot load the act-history generator")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def _read_receipt(root: Path, tool) -> bytes:
    path = root / RECEIPT
    try:
        with tool._open_directory_path(path.parent, create=False) as (parent_fd, parent):
            entry = tool._entry_stat(parent_fd, path.name)
            if entry is None or not stat.S_ISREG(entry.st_mode):
                raise ReceiptError(f"missing or nonregular projection receipt: {RECEIPT}; run record")
            return tool._read_structure_file(parent_fd, path.name, entry, parent / path.name)
    except (OSError, tool.Problem) as error:
        raise ReceiptError(f"cannot read projection receipt {RECEIPT}: {error}") from error


def _write_receipt(root: Path, tool, body: bytes) -> None:
    path = root / RECEIPT
    scratch = root / ".scratch/act-history-perf"
    with tool._open_directory_path(scratch, create=True) as (scratch_fd, _), \
            tool._open_directory_path(path.parent, create=False) as (parent_fd, _):
        entry = tool._entry_stat(parent_fd, path.name)
        if entry is not None and (not stat.S_ISREG(entry.st_mode) or entry.st_nlink != 1):
            raise ReceiptError(f"refusing nonregular or linked projection receipt: {RECEIPT}")
        name = f".{path.name}.{os.getpid()}.{os.urandom(8).hex()}.tmp"
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o644, dir_fd=scratch_fd)
        try:
            view = memoryview(body)
            while view:
                view = view[os.write(fd, view):]
            os.fsync(fd)
            os.replace(name, path.name, src_dir_fd=scratch_fd, dst_dir_fd=parent_fd)
        finally:
            os.close(fd)
            try:
                os.unlink(name, dir_fd=scratch_fd)
            except FileNotFoundError:
                pass


def _validate(receipt: object) -> dict:
    keys = {"schema", "proof", "generator", "editorial_approval", "inputs", "outputs", "summary"}
    if (not isinstance(receipt, dict) or set(receipt) != keys
            or receipt["schema"] != SCHEMA or receipt["proof"] != PROOF
            or receipt["generator"] != "tools/act-history structure --check"
            or receipt["editorial_approval"] is not False
            or not isinstance(receipt["inputs"], dict)
            or not isinstance(receipt["outputs"], dict)
            or not isinstance(receipt["summary"], dict)
            or set(receipt["summary"]) != set(SUMMARY_KEYS)):
        raise ReceiptError("unsupported or incomplete projection receipt; run record")
    outputs = receipt["outputs"]
    summary = receipt["summary"]
    if (not isinstance(outputs.get("files"), dict)
            or type(outputs.get("count")) is not int
            or outputs["count"] < 1 or outputs["count"] != len(outputs["files"])
            or summary["files"] != outputs["count"]):
        raise ReceiptError("incomplete projection output inventory; run record")
    return receipt


@contextmanager
def _fresh_caches(tool, scratch: Path):
    """Replay may reuse only caches first populated within this replay.

    This avoids inheriting a stat-keyed parse/graph cache when establishing a
    byte-identity receipt, while keeping repeated graph loads within the full
    replay affordable. The before/after source digest brackets all of them.
    """
    import _calendars
    import _proper_latin

    environment = {
        "TRIPTYCH_LIBRARY_CACHE_DIR": str(scratch / "library-cache"),
        "TRIPTYCH_LIBRARY_CACHE": "1",
        "TRIPTYCH_YAML_CACHE": "1",
        "TRIPTYCH_SOURCE_LIBRARY_CACHE": "1",
    }
    prior_env = {key: os.environ.get(key) for key in environment}
    prior_yaml = _calendars._YAML_CACHE
    prior_library = _proper_latin.SOURCE_LIBRARY_CACHE_DIR
    prior_memory = _proper_latin._SOURCE_LIBRARY_CACHE.copy()
    _proper_latin._SOURCE_LIBRARY_CACHE.clear()
    tool._SOURCE_ARTIFACT_RECORDS = None
    _calendars._YAML_CACHE = scratch / "yaml-cache"
    _proper_latin.SOURCE_LIBRARY_CACHE_DIR = scratch / "proper-library-cache"
    os.environ.update(environment)
    try:
        yield
    finally:
        _calendars._YAML_CACHE = prior_yaml
        _proper_latin.SOURCE_LIBRARY_CACHE_DIR = prior_library
        _proper_latin._SOURCE_LIBRARY_CACHE.clear()
        _proper_latin._SOURCE_LIBRARY_CACHE.update(prior_memory)
        for key, value in prior_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _replay(root: Path, tool) -> dict:
    scratch = root / ".scratch/act-history-perf"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="replay-", dir=scratch) as held:
        scratch_root = Path(held)
        with _fresh_caches(tool, scratch_root):
            built = tool.build_structure_projection(tool.structure_sources(), scratch_root / "data")
        target = root / PROJECTION
        with tool._open_directory_path(target, create=False) as (target_fd, safe_target):
            actual = tool.structure_files(target_fd, safe_target)
        expected = built["contents"]
        drifted = sorted(name for name in set(actual) | set(expected)
                         if actual.get(name) != expected.get(name))
        if drifted:
            raise ReceiptError("installed act-history projection has drifted at "
                               + ", ".join(drifted[:5])
                               + "; regenerate and review it before recording; no receipt written")
        return {key: built[key] for key in SUMMARY_KEYS}


def record(root: Path = ROOT) -> dict:
    """The only receipt writer always requires a successful independent replay."""
    tool = _tool()
    before = input_identity(root)
    prior_outputs = output_identity(root, root / PROJECTION)
    try:
        summary = _replay(root, tool)
    except tool.Problem as error:
        raise ReceiptError(f"independent projection replay failed: {error}") from error
    outputs = output_identity(root, root / PROJECTION)
    after = input_identity(root)
    if after != before:
        raise ReceiptError("projection inputs changed during independent replay; no receipt written")
    if outputs != prior_outputs:
        raise ReceiptError("projection outputs changed during independent replay; no receipt written")
    receipt = _validate({"schema": SCHEMA, "proof": PROOF,
                         "generator": "tools/act-history structure --check",
                         "editorial_approval": False,
                         "inputs": before, "outputs": outputs, "summary": summary})
    body = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    try:
        _write_receipt(root, tool, body)
    except tool.Problem as error:
        raise ReceiptError(f"cannot safely write projection receipt: {error}") from error
    return receipt


def check(root: Path = ROOT) -> dict:
    """Check a reviewed tracked receipt; never create, refresh or replay it."""
    tool = _tool()
    body = _read_receipt(root, tool)
    try:
        receipt = _validate(json.loads(body))
    except (UnicodeError, ValueError) as error:
        raise ReceiptError(f"invalid projection receipt: {error}") from error
    before = input_identity(root)
    if before != receipt["inputs"]:
        raise ReceiptError("projection source, generator or policy identity has changed; run record")
    if output_identity(root, root / PROJECTION) != receipt["outputs"]:
        raise ReceiptError("projection output files have changed, are missing or are orphaned; run record")
    if input_identity(root) != before or _read_receipt(root, tool) != body:
        raise ReceiptError("projection inputs or receipt changed during checking")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "record"))
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        receipt = (check if arguments.command == "check" else record)()
    except (ReceiptError, OSError, ValueError) as error:
        print(f"act-history projection receipt: {error}", file=sys.stderr)
        return 1
    if arguments.json:
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    else:
        print(f"{'current' if arguments.command == 'check' else 'recorded'}: "
              f"{receipt['outputs']['count']} act-history projection files; "
              f"{receipt['inputs']['count']} source/policy/generator identities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
