"""The surfaces, in the order the site's landing page lists them.

Each is imported on its own, so one that fails to load says so in its own
place and the rest still open.
"""
from __future__ import annotations

import importlib
import importlib.util
import traceback

from .. import SURFACES
from ..surface import Pending


def _broken(digit: str, name: str, problem: str) -> type[Pending]:
    return type(f"{name}Surface", (Pending,), {"key": digit, "label": name, "problem": problem})


def _load(digit: str, name: str, module: str):
    if importlib.util.find_spec(f"{__name__}.{module}") is None:
        return type(f"{name}Surface", (Pending,), {"key": digit, "label": name})
    try:
        found = getattr(importlib.import_module(f"{__name__}.{module}"), name)
    except Exception:  # noqa: BLE001 - the failure is shown where the surface would be
        return _broken(digit, name, traceback.format_exc(limit=3))
    return found


ORDER = [_load(*row) for row in SURFACES]
