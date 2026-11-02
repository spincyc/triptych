"""Locate prepared browser products for regression fixtures without generating them."""

from __future__ import annotations

import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = str(ROOT / "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)
PREPARE = "prepare browser products with `tools/browser-products build` before running real-data tests"


def browser_data_root(root: Path = ROOT) -> Path:
    """Return the committed product view, or an explicitly selected test fixture.

    TRIPTYCH_TEST_BROWSER_DATA_ROOT is solely a regression-fixture override. The
    ordinary browser cache location still follows TRIPTYCH_BROWSER_DATA_ROOT.
    Neither route generates products or falls back to the former tracked tree.
    """
    root = Path(root).resolve()
    override = os.environ.get("TRIPTYCH_TEST_BROWSER_DATA_ROOT")
    if override:
        selected = Path(override).expanduser()
        selected = selected if selected.is_absolute() else root / selected
    else:
        import _browser_products

        try:
            selected = _browser_products.committed_data_root(root)
        except _browser_products.ProductError as error:
            raise RuntimeError(f"{error}; {PREPARE}") from error
    if not selected.is_dir():
        raise RuntimeError(f"browser test data is absent at {selected}; {PREPARE}")
    return selected.resolve()


def data_path(relative: str | Path, root: Path = ROOT) -> Path:
    """Resolve a product-relative path against the prepared regression data."""
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"expected a browser-product-relative path: {relative}")
    return browser_data_root(root) / relative


if __name__ == "__main__":
    if len(sys.argv) > 2:
        raise SystemExit("usage: _product_data.py [REPOSITORY_ROOT]")
    try:
        print(browser_data_root(Path(sys.argv[1]) if len(sys.argv) == 2 else ROOT))
    except (RuntimeError, ValueError) as error:
        raise SystemExit(str(error)) from error
