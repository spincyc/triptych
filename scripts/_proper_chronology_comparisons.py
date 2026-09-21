"""Strict authored selections for proper chronology profile comparisons.

This module reads only a leaf-owned selection file.  It reads no chronology
corpus data and resolves no claims; ``_proper_chronology`` remains the adapter
that sends the validated selection through the corpus query seam.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from pathlib import Path
from typing import NamedTuple

INPUT = "research/chronology-profile-comparisons.toml"
SCHEMA = 1
RECORD_TYPE = "proper-chronology-profile-comparisons"


class Selection(NamedTuple):
    key: str
    element_key: str
    profile: str
    relation: str
    subject: str


def load(
    document: str,
    root: Path,
    provider: str,
    default_profile: str,
    profiles: dict,
    elements: tuple,
) -> tuple[tuple[Selection, ...], tuple[tuple[str, str], ...]]:
    """Validate the optional file without merging any profile answers."""
    if not isinstance(provider, str) or not provider or any(
        part in {"", ".", ".."} for part in (provider, *document.split("/"))
    ):
        raise ValueError("profile comparisons require a canonical provider leaf")
    provider_root = (root / "src" / provider).resolve()
    leaf = (provider_root / document).resolve()
    if provider_root not in leaf.parents:
        raise ValueError("profile comparison document leaves its provider root")
    path = leaf / INPUT
    if not path.exists():
        return (), ()
    if provider not in {"gpt", "claude"}:
        raise ValueError("profile comparisons require the gpt or claude provider")
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"{INPUT}: must be a regular file")

    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ValueError(f"{INPUT}: {exc}") from exc
    allowed_top = {"schema", "record_type", "document", "comparisons"}
    if set(data) - allowed_top:
        raise ValueError(f"{INPUT}: unknown top-level fields")
    if (
        data.get("schema") != SCHEMA
        or data.get("record_type") != RECORD_TYPE
        or data.get("document") != document
    ):
        raise ValueError(
            f"{INPUT}: schema, record_type, or document does not match"
        )
    rows = data.get("comparisons")
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{INPUT}: comparisons must be nonempty")

    by_key = {element.key: element for element in elements}
    selections: list[Selection] = []
    seen_keys: set[str] = set()
    seen_values: set[tuple[str, str, str, str]] = set()
    allowed_row = {"key", "element", "profile", "relation", "subject"}
    for index, row in enumerate(rows, 1):
        where = f"{INPUT} comparison {index}"
        if not isinstance(row, dict) or set(row) != allowed_row:
            raise ValueError(f"{where}: requires exactly {sorted(allowed_row)}")
        key = row.get("key")
        element_key = row.get("element")
        profile = row.get("profile")
        relation = row.get("relation")
        subject = row.get("subject")
        if not isinstance(key, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", key
        ):
            raise ValueError(f"{where}: key is not canonical")
        if key in seen_keys:
            raise ValueError(f"{where}: duplicate key {key!r}")
        seen_keys.add(key)
        element = by_key.get(element_key) if isinstance(element_key, str) else None
        if element is None or not element.loci:
            raise ValueError(f"{where}: element is not appointed Scripture")
        if not all(isinstance(value, str) and value for value in (
            profile, relation, subject
        )):
            raise ValueError(f"{where}: profile, relation, and subject are required")
        profile_record = profiles.get(profile)
        if not profile_record or profile_record.get("kind") != "evidence":
            raise ValueError(f"{where}: profile must be an evidence profile")
        if profile == default_profile:
            raise ValueError(f"{where}: comparison repeats the default profile")
        selection = (element_key, profile, relation, subject)
        if selection in seen_values:
            raise ValueError(f"{where}: duplicate comparison selection")
        seen_values.add(selection)
        selections.append(Selection(key, element_key, profile, relation, subject))

    dependency = (
        path.relative_to(root).as_posix(),
        hashlib.sha256(path.read_bytes()).hexdigest(),
    )
    return tuple(selections), (dependency,)
