#!/usr/bin/env python3
"""What may live under `src/sources/calendars`, and which tool owns each kind.

A calendar directory used to hold exactly one kind of file, so the tools that
read it discovered their inputs with `rglob("*.yaml")` and treated whatever they
found as a mass index. That was an accident of there being only one kind, not a
decision that there could only ever be one: the moment a second kind of
calendar-scoped source landed beside `propers.yaml`, every one of those globs
read it as a mass index and failed on its missing `sections`.

So discovery is by the declared schema, and it lives here once. A file whose
schema names a kind another tool owns is skipped and *reported as skipped*; a
file whose schema is recognised by nobody is a hard failure. Silently ignoring
an unclassifiable file would be worse than the noisy failure it replaces --- a
mass index with a mistyped schema string would simply stop being checked.
"""
from __future__ import annotations

import re
from pathlib import Path

MASS_INDEX_SCHEMA = "triptych-calendar-masses/v1"

# Every other schema that legitimately sits in a calendar directory, with the
# tool that validates it. Adding a kind of calendar source means adding a line
# here and nowhere else.
COMPANION_SCHEMAS = {
    "triptych-calendar-rubrics/v1": "calendar-rubrics",
}

# A YAML top-level key sits at column zero, which is what makes this cheap scan
# equivalent to a parse for the one field it wants.
SCHEMA_LINE = re.compile(r"^schema:[ \t]*(?:['\"])?([^'\"\s#]+)", re.MULTILINE)
EDITION_SHORT_LINE = re.compile(r"^edition_short:[ \t]*(.+?)[ \t]*$", re.MULTILINE)


def declared_schema(path: Path) -> str | None:
    """The `schema` a calendar source declares, or None if it declares none."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = SCHEMA_LINE.search(text)
    return found.group(1) if found else None


def edition_short(root: Path, calendar: str) -> str | None:
    """The short name of the book a calendar's masses are printed in.

    The name a reader would say — "1962 Missal" — as against the bibliographic
    `edition` that identifies the printing. A select control has room for one of
    them and a reader has patience for one of them, and it is not the sixty-eight
    characters of "Missale Romanum, editio typica tertia 2008, reimpressio
    emendata 2008".

    It is read from the mass index, which is the file that names the book, and
    from nowhere else. Two tools emit it to the browser and neither keeps a copy:
    a short name pasted into a second source is the restatement that drifts, and
    `edition` is already carried twice in this directory for want of one owner.
    """
    path = root / calendar / "propers.yaml"
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = EDITION_SHORT_LINE.search(text)
    return found.group(1).strip("'\"") if found else None


def partition(root: Path, calendar: str | None = None) -> tuple[list[Path], list[dict], list[str]]:
    """Split a calendar root into mass indexes, companions, and complaints.

    Returns `(indexes, companions, problems)`. `companions` records each file
    another tool owns, so a caller can say what it did not check rather than
    leaving the reader to infer it from a count.
    """
    if not root.is_dir():
        raise ValueError(f"missing calendar root: {root}")

    indexes: list[Path] = []
    companions: list[dict] = []
    problems: list[str] = []

    for path in sorted(root.rglob("*.yaml")):
        if calendar is not None and path.parent.name != calendar:
            continue
        schema = declared_schema(path)
        if schema == MASS_INDEX_SCHEMA:
            indexes.append(path)
        elif schema in COMPANION_SCHEMAS:
            companions.append(
                {
                    "path": path.as_posix(),
                    "schema": schema,
                    "owner": COMPANION_SCHEMAS[schema],
                }
            )
        else:
            problems.append(
                f"{path}: declares schema {schema!r}, which is neither the mass index "
                f"{MASS_INDEX_SCHEMA!r} nor a companion kind "
                f"({', '.join(sorted(COMPANION_SCHEMAS))}). A calendar source must "
                "declare a schema this repository recognises, so that a mistyped one "
                "fails instead of going unchecked."
            )

    return indexes, companions, problems
