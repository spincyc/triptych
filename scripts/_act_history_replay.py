"""Cold act-history replay: the `act-history` browser-product family producer.

`_browser_product_recipes` runs `_replay` for the `act-history` family (see
`_browser_product_inputs.ADAPTERS`). It builds into an explicit aggregate data
root whose act-history subtree is absent or empty, with parse and graph caches
first populated inside this replay and no source bytecode, so no old
projection, descriptor or stat-keyed cache can seed the result. The
browser-product descriptor records and checks the bytes it produces.

The exhaustive gate remains ``tools/tpt act-history structure --check``.
"""
from __future__ import annotations

from contextlib import contextmanager
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
PROJECTION = Path("structure/act-history")
SCRATCH = Path(".scratch/act-history-replay")
SUMMARY_KEYS = ("files", "slices", "stations", "lines", "default")


class ReplayError(ValueError):
    """The cold act-history replay could not derive the complete family."""


def _tool():
    # Only execute the tool in this checkout; an alternate data root cannot
    # replace trusted code. Kept separate so small mutation tests need no corpus.
    loader = importlib.machinery.SourceFileLoader(
        "_act_history_replay_tool", str(ROOT / "tools/act-history")
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise ReplayError("cannot load the act-history generator")
    module = importlib.util.module_from_spec(spec)
    # SourceFileLoader.exec_module may accept timestamp-keyed bytecode. The
    # generator identity is the exact current source, so compile those bytes.
    path = ROOT / "tools/act-history"
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return module


@contextmanager
def _fresh_caches(tool, scratch: Path):
    """Replay may reuse only caches first populated within this replay.

    This avoids inheriting a stat-keyed parse/graph cache when establishing a
    byte-identical family, while keeping repeated graph loads within the full
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
    subtree must be absent or empty: no old browser data or descriptor
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
            raise ReplayError(str(error)) from error
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
                            raise ReplayError("cold act-history output must be absent or empty")
                with tempfile.TemporaryDirectory(prefix="cold-caches-", dir=scratch) as held:
                    with _fresh_caches(tool, Path(held)):
                        built = tool.build_structure_projection(tool.structure_sources(), out)
        except tool.Problem as error:
            # Each trusted source load has its own exception class. Translate
            # here instead of asking a separately loaded caller to catch it.
            raise ReplayError(f"independent projection replay failed: {error}") from error
        return {key: built[key] for key in SUMMARY_KEYS}
    finally:
        sys.pycache_prefix, sys.dont_write_bytecode = old_prefix, old_write


