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

It owns the other half of that seam too: which header fields a companion may
*not* carry. A calendar directory describes one book, and the mass index is the
file that identifies it. A companion that retypes the identity is a second copy
with nothing comparing it to the first, which is what `restated_identity`
refuses.
"""
from __future__ import annotations

import re
from pathlib import Path

MASS_INDEX_SCHEMA = "triptych-calendar-masses/v1"
MASS_INDEX = "propers.yaml"

# Every other schema that legitimately sits in a calendar directory, with the
# tool that validates it. Adding a kind of calendar source means adding a line
# here and nowhere else.
COMPANION_SCHEMAS = {
    "triptych-calendar-rubrics/v1": "calendar-rubrics",
}

# The identity of the book a calendar's masses are printed in. Both fields
# belong to the mass index, because that is the file that transcribes the book;
# a companion source in the same directory names the same book but is not what
# identifies it, and reads these from the index instead of writing them out
# again. `restated_identity` refuses the second copy.
#
# `edition` identifies the printing bibliographically. `edition_short` is the
# name a reader would say — "1962 Missal" — because a select control has room
# for one of them and a reader has patience for one of them, and it is not the
# sixty-eight characters of "Missale Romanum, editio typica tertia 2008,
# reimpressio emendata 2008".
INDEX_OWNED = ("edition", "edition_short")

# A YAML top-level key sits at column zero, which is what makes this cheap scan
# equivalent to a parse for the one field it wants.
SCHEMA_LINE = re.compile(r"^schema:[ \t]*(?:['\"])?([^'\"\s#]+)", re.MULTILINE)
_HEADER_LINES: dict[str, re.Pattern[str]] = {}


def _header_line(field: str) -> re.Pattern[str]:
    if field not in _HEADER_LINES:
        _HEADER_LINES[field] = re.compile(
            rf"^{re.escape(field)}:[ \t]*(.+?)[ \t]*$", re.MULTILINE
        )
    return _HEADER_LINES[field]


def declared_schema(path: Path) -> str | None:
    """The `schema` a calendar source declares, or None if it declares none."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = SCHEMA_LINE.search(text)
    return found.group(1) if found else None


def header(path: Path, field: str) -> str | None:
    """A one-line top-level scalar a calendar source declares, or None."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    found = _header_line(field).search(text)
    return found.group(1).strip("'\"") if found else None


def index_header(root: Path, calendar: str, field: str) -> str | None:
    """A header field read from the calendar's mass index and nowhere else."""
    return header(root / calendar / MASS_INDEX, field)


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


def restated_identity(root: Path, calendar: str | None = None) -> list[str]:
    """Every companion source that writes out an identity the index owns.

    `edition` sat hand-typed in both files of both calendar directories — four
    copies of two strings, with nothing in the repository comparing them. They
    happened to agree; nothing made them agree. This same repository has held
    one census in three copies that all disagreed, and a README restating four
    totals its own table gave differently, so agreement between hand-typed
    copies is a fact about a moment and not a property of the data.

    So a companion carrying one of these fields fails here whether or not its
    value matches. The disagreement is the symptom; the second copy is the
    defect, and it is the only thing a check can catch before the drift.
    """
    problems: list[str] = []
    _, companions, _ = partition(root, calendar)
    for companion in companions:
        path = Path(companion["path"])
        index = root / path.parent.name / MASS_INDEX
        for field in INDEX_OWNED:
            found = header(path, field)
            if found is None:
                continue
            owned = header(index, field)
            if found == owned:
                problems.append(
                    f"{path}: restates {field} {found!r}, which {index} owns and "
                    f"{companion['owner']} reads from there. Delete the line: a copy "
                    "that agrees today is a disagreement that has not happened yet."
                )
            else:
                problems.append(
                    f"{path}: declares {field} {found!r} while {index} declares "
                    f"{owned!r}. Two files claim a different book for the same "
                    f"calendar; the mass index is the owner, and {companion['owner']} "
                    "reads it from there. Delete the line."
                )
    return problems
