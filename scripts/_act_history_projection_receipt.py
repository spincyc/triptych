#!/usr/bin/env python3
"""Check the exact identity of a mechanically replayed act-history projection.

``record`` independently builds into exclusive scratch space and refuses any
installed-byte drift before writing. It never installs or adopts generated
bytes. ``check`` hashes the complete recognized source, policy and generator
closure and every committed browser-product output; no timestamp can
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
                            / ".scratch/next-act-receipt"
                            / ("no-bytecode-" + os.urandom(16).hex()))

from _source_projection_receipt import ReceiptError, input_identity, output_identity


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = Path("src/sources/inventories/act-history-projection-receipt-v1.json")
PROJECTION = Path("structure/act-history")
SCRATCH = Path(".scratch/next-act-receipt")
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
    # SourceFileLoader.exec_module may accept timestamp-keyed bytecode. The
    # generator identity is the exact current source, so compile those bytes.
    path = ROOT / "tools/act-history"
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


@contextmanager
def _products(root: Path, *, cache_root: Path | None = None):
    """Hold authenticated private bytes, never a mutable cache pathname."""
    # The product store imports the shared receipt utilities; keep this import
    # lazy so the producer remains usable before any product descriptor exists.
    import _browser_products
    try:
        with _browser_products.verified_products(
            root, cache_root=cache_root, product_ids=["act-history"]
        ) as products:
            yield products
    except _browser_products.ProductError as error:
        raise ReceiptError(f"act-history browser products are unavailable or stale: {error}") from error


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
    scratch = root / SCRATCH
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
        "TRIPTYCH_CONTAINMENT_CACHE": "0",
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


def _replay(root: Path, out: Path) -> dict:
    """Cold-build the full family beneath an explicit aggregate data root.

    Other product families may already be present in ``out``. This family's
    subtree must be absent or empty: no old browser data, receipt or descriptor
    is read, and no existing family bytes are installed or adopted. Product
    recipes call this API directly and independently authenticate its outputs.
    """
    root = Path(root).resolve()
    out = Path(os.path.abspath(out))
    scratch = root / SCRATCH
    scratch.mkdir(parents=True, exist_ok=True)
    old_prefix, old_write = sys.pycache_prefix, sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    sys.pycache_prefix = str(scratch / ("no-bytecode-" + os.urandom(16).hex()))
    try:
        import _browser_products
        try:
            out = _browser_products.assert_working_output(root, out)
        except _browser_products.ProductError as error:
            raise ReceiptError(str(error)) from error
        tool = _tool()
        # Executable code remains this checkout's trusted tool; data may come
        # from the caller's clean checkout/fixture root.
        tool.ROOT = root
        tool.STRUCTURE_SOURCES = root / "src/sources/inventories"
        tool.SOURCE_ARTIFACTS = root / "src/sources/works"
        try:
            with tool._open_directory_path(out, create=True):
                target = out / PROJECTION
                if target.exists() or target.is_symlink():
                    with tool._open_directory_path(target, create=False) as (target_fd, _):
                        if os.listdir(target_fd):
                            raise ReceiptError("cold act-history output must be absent or empty")
                with tempfile.TemporaryDirectory(prefix="cold-caches-", dir=scratch) as held:
                    with _fresh_caches(tool, Path(held)):
                        built = tool.build_structure_projection(tool.structure_sources(), out)
        except tool.Problem as error:
            # Each trusted source load has its own exception class. Translate
            # here instead of asking a separately loaded caller to catch it.
            raise ReceiptError(f"independent projection replay failed: {error}") from error
        return {key: built[key] for key in SUMMARY_KEYS}
    finally:
        sys.pycache_prefix, sys.dont_write_bytecode = old_prefix, old_write


def _compare_replay(root: Path, target: Path, tool) -> dict:
    scratch = root / SCRATCH
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="replay-", dir=scratch) as held:
        out = Path(held) / "data"
        summary = _replay(root, out)
        with tool._open_directory_path(out / PROJECTION, create=False) as (built_fd, built_root):
            expected = tool.structure_files(built_fd, built_root)
        with tool._open_directory_path(target, create=False) as (target_fd, safe_target):
            actual = tool.structure_files(target_fd, safe_target)
        drifted = sorted(name for name in set(actual) | set(expected)
                         if actual.get(name) != expected.get(name))
        if drifted:
            raise ReceiptError("installed act-history projection has drifted at "
                               + ", ".join(drifted[:5])
                               + "; regenerate and review it before recording; no receipt written")
        return summary


def record(root: Path = ROOT, *, cache_root: Path | None = None) -> dict:
    """The only receipt writer always requires a successful independent replay."""
    tool = _tool()
    before = input_identity(root)
    with _products(root, cache_root=cache_root) as products:
        target = products.data_root / PROJECTION
        prior_outputs = output_identity(root, target)
        try:
            summary = _compare_replay(root, target, tool)
        except tool.Problem as error:
            raise ReceiptError(f"independent projection replay failed: {error}") from error
        outputs = output_identity(root, target)
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


def check(root: Path = ROOT, *, cache_root: Path | None = None) -> dict:
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
    with _products(root, cache_root=cache_root) as products:
        if output_identity(root, products.data_root / PROJECTION) != receipt["outputs"]:
            raise ReceiptError("projection output files have changed, are missing or are orphaned; run record")
        if input_identity(root) != before or _read_receipt(root, tool) != body:
            raise ReceiptError("projection inputs or receipt changed during checking")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "record"))
    parser.add_argument("--cache-root", type=Path, help="sealed browser-product cache; defaults to TRIPTYCH_BROWSER_DATA_ROOT or build/browser-data")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        receipt = (check if arguments.command == "check" else record)(cache_root=arguments.cache_root)
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
