"""Lightweight user preferences for interactive lectern sessions.

Stored outside the repository under `$XDG_CONFIG_HOME/triptych/lectern.json`
(defaulting to `~/.config/triptych/lectern.json`). Snapshots and headless tests
bypass persistence so renders stay deterministic; storage errors are ignored so
the reader always works when the filesystem is read-only.
"""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

PREF_KEYS = (
    "theme",
    "calendar",
    "bible",
    "orations",
    "ordinary_language",
    "text_display",
    "rubrics",
    "companion",
)


def prefs_file(override: Path | None = None) -> Path:
    if override is not None:
        return override
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg) if xdg else (Path.home() / ".config")
    return base / "triptych" / "lectern.json"


def load_prefs(path: Path | None = None) -> dict[str, Any]:
    target = prefs_file(path)
    try:
        raw = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    if not isinstance(raw, dict):
        return {}
    return {key: raw[key] for key in PREF_KEYS if key in raw}


def save_prefs(values: dict[str, Any], path: Path | None = None) -> None:
    target = prefs_file(path)
    merged = load_prefs(path)
    for key, value in values.items():
        if key in PREF_KEYS:
            if value is None:
                merged.pop(key, None)
            else:
                merged[key] = value
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".lectern-", suffix=".tmp", dir=str(target.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(merged, handle, indent=2, sort_keys=True)
                handle.write("\n")
            os.replace(tmp, target)
        except OSError:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    except OSError:
        pass
