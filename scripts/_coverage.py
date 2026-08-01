#!/usr/bin/env python3
"""What each held commentary work covers of a book, and where it does not.

THE HOLE THIS CLOSES. Three things were already recorded and never compared.
The discovery index names works on chapters (L1). The fragment edge holds
extents on chapters (L3). Nothing subtracted one from the other, so
`catena check` could report 1,351 fragments and say nothing whatever about
where they are not. A major work held on a sliver of what it comments on
passed every gate in the repository, and the first thing to notice was a
person reading the site and asking why Augustine reaches Genesis 3 and stops.

THE DISTINCTION THAT MAKES THE NUMBER USEFUL. A difference between named and
held is not a defect. De Genesi ad litteram genuinely ends at Genesis 3, so
4-50 is not missing from it; De civitate Dei expounds Cain and Abel at length
and is held on nothing past Genesis 2, which is missing. The two are
indistinguishable from the index and the fragments alone, and no amount of
derivation separates them: something has to state how far the work itself
reaches. `src/sources/commentary/work-extents.yaml` is that statement, each
row sourced, and this module subtracts it. Where a work has no row there, the
difference is reported as UNEXAMINED — the work item is to establish the
extent, not to go acquiring.

WHAT IS DERIVED AND WHAT IS STORED. Everything here is derived. No chapter
list is written to disk, nothing restates the index or the edge, and the
work-to-alias-group mapping is read off the fragments themselves rather than
kept as a second table — `guidance/the-shape.md` §2. The only stored thing is
the extent, which cannot be derived from anything.

A GAP IS NOT A BUILD FAILURE. An unacquired work is not a defect and this
never fails on one. What does fail is an extent record that contradicts
itself or the holding: a row naming no work, an extent past the end of the
book, or — the one that matters — an extent a held fragment of the same work
already reaches past, which means either the extent or the fragment is wrong
and no report standing on both can be trusted.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, NamedTuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _catena  # noqa: E402

ROOT = _catena.ROOT
SCHEMA = "triptych-commentary-work-extents/v1"
# The report is not the record: a consumer that pins one must not be handed the
# other, and the two move for different reasons.
REPORT_SCHEMA = "triptych-commentary-coverage/v1"
EXTENTS_RELATIVE = Path("src/sources/commentary/work-extents.yaml")

EXTENT_FIELDS = {
    "work_id",
    "token",
    "first_chapter",
    "first_verse",
    "last_chapter",
    "last_verse",
    "within",
    "basis",
}

# How to read a chapter inside a recorded extent that holds nothing. The
# vocabulary is closed because it decides whether a number is a work item, and
# an unrecognised value would silently become the permissive reading.
CONTINUOUS = "continuous"
SELECTIVE = "selective"
WITHIN = (CONTINUOUS, SELECTIVE)

# The four things a (work, book) pair can be, worst first. `gap` is the only
# one that asserts something is missing; the rest each say precisely how much
# less than that is known, which is the whole point of having four.
GAP = "gap"
UNEXAMINED = "unexamined"
NOT_ESTABLISHED = "not-established"
COMPLETE = "complete"
STATUS_ORDER = (GAP, UNEXAMINED, NOT_ESTABLISHED, COMPLETE)
STATUS_RANK = {status: rank for rank, status in enumerate(STATUS_ORDER)}

STATUS_NOTE = {
    GAP: "acquisition stopped inside the work's own extent",
    UNEXAMINED: "no extent recorded, so nothing can say whether this is a gap",
    NOT_ESTABLISHED: "inside a selective work, so this may be its own silence",
    COMPLETE: "the work's extent is held entire",
}


class WorkExtent(NamedTuple):
    """How far a work reaches into one book, as recorded and sourced."""

    work_id: str
    token: str
    first_chapter: int
    first_verse: int
    last_chapter: int
    last_verse: int
    within: str
    basis: str

    def chapters(self) -> set[int]:
        return set(range(self.first_chapter, self.last_chapter + 1))


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------


def load_extents(root: Path = ROOT) -> dict[str, Any]:
    data = _catena._load_yaml(root / EXTENTS_RELATIVE)
    if not isinstance(data, dict):
        raise _catena.CatenaError(f"{EXTENTS_RELATIVE}: not a mapping")
    if data.get("schema") != SCHEMA:
        raise _catena.CatenaError(
            f"{EXTENTS_RELATIVE}: declares schema {data.get('schema')!r}, "
            f"expected {SCHEMA!r}"
        )
    return data


def extents(root: Path = ROOT) -> dict[tuple[str, str], WorkExtent]:
    """Every recorded extent, keyed by work and book. Malformed rows are dropped.

    Dropping rather than raising is deliberate: `validate` reports every reason
    a row is unusable, and a caller that has run it knows the set is clean. A
    caller that has not gets the rows that are certainly well formed and a
    coverage report that says `unexamined` for the rest, which is the honest
    reading of a row nothing could parse.
    """
    found: dict[tuple[str, str], WorkExtent] = {}
    for row in load_extents(root).get("extents") or ():
        parsed = _parse(row)
        if parsed is not None:
            found.setdefault((parsed.work_id, parsed.token), parsed)
    return found


def _parse(row: Any) -> WorkExtent | None:
    if not isinstance(row, dict) or set(row) != EXTENT_FIELDS:
        return None
    try:
        return WorkExtent(
            work_id=str(row["work_id"]),
            token=str(row["token"]),
            first_chapter=int(row["first_chapter"]),
            first_verse=int(row["first_verse"]),
            last_chapter=int(row["last_chapter"]),
            last_verse=int(row["last_verse"]),
            within=str(row["within"]),
            basis=str(row["basis"]),
        )
    except (TypeError, ValueError):
        return None


def validate(root: Path = ROOT) -> list[str]:
    """Every reason the extent record cannot be subtracted, deterministically.

    None of these is a gap. A gap is a fact about the corpus and is reported;
    everything here is a fact about the record itself, and a report standing on
    a record that contradicts the fragments it is subtracted from would be the
    fluent wrong answer this repository exists to refuse.
    """
    errors: list[str] = []
    where = EXTENTS_RELATIVE.as_posix()
    data = load_extents(root)

    declared = data.get("numbering")
    if declared != _catena._projection.CANONICAL:
        errors.append(
            f"{where}: numbering is {declared!r}; an extent is a canonical address "
            f"and {_catena._projection.CANONICAL!r} is the only one (Rule 3)"
        )

    rows = data.get("extents")
    if not isinstance(rows, list) or not rows:
        errors.append(f"{where}: extents must be a nonempty list")
        return sorted(errors)

    sources = _catena.load_sources(root)
    ceilings = {book["token"]: book["last_chapter"] for book in _catena.canon(root)}
    reach = _held_reach(root)

    seen: set[tuple[str, str]] = set()
    for ordinal, row in enumerate(rows, start=1):
        label = f"{where}: extents[{ordinal}]"
        if not isinstance(row, dict):
            errors.append(f"{label} must be a mapping")
            continue
        unknown = sorted(set(row) - EXTENT_FIELDS)
        missing = sorted(EXTENT_FIELDS - set(row))
        if unknown:
            errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
        if missing:
            errors.append(f"{label} is missing: {', '.join(missing)}")
            continue
        parsed = _parse(row)
        if parsed is None:
            errors.append(f"{label} has a field of the wrong type")
            continue

        label = f"{where}: {parsed.work_id} on {parsed.token}"
        key = (parsed.work_id, parsed.token)
        if key in seen:
            errors.append(f"{label} is recorded twice")
        seen.add(key)

        if parsed.work_id not in sources.works:
            errors.append(f"{label} names no work record in the source library")
        if parsed.within not in WITHIN:
            errors.append(
                f"{label} declares within={parsed.within!r}; it must be one of "
                f"{', '.join(WITHIN)}, because that is what decides whether an "
                f"unheld chapter inside the extent is a gap"
            )
        # An extent is a claim about a book and carries its basis exactly as
        # `composed` carries `composed_basis`. A row without one asserts a
        # boundary nobody can walk back to a page.
        if not parsed.basis.strip():
            errors.append(f"{label} states no basis for the extent it claims")

        errors.extend(_bounds_errors(root, label, parsed, ceilings))

        # The one contradiction worth failing a build over. If a fragment of
        # this work already reaches past the extent, then either the extent is
        # short or the fragment is misplaced, and subtracting the one from the
        # other would report a clean corpus either way.
        held = reach.get(key)
        if held is not None:
            first, last = held
            if first < (parsed.first_chapter, parsed.first_verse):
                errors.append(
                    f"{label} begins at {parsed.first_chapter}:{parsed.first_verse}, "
                    f"but a held fragment of it begins at {first[0]}:{first[1]}"
                )
            if last > (parsed.last_chapter, parsed.last_verse):
                errors.append(
                    f"{label} ends at {parsed.last_chapter}:{parsed.last_verse}, "
                    f"but a held fragment of it ends at {last[0]}:{last[1]}"
                )
    return sorted(errors)


def _bounds_errors(
    root: Path, label: str, extent: WorkExtent, ceilings: dict[str, int]
) -> list[str]:
    errors: list[str] = []
    if extent.token not in ceilings:
        errors.append(
            f"{label} names book {extent.token!r}, which the canonical edition "
            f"does not carry"
        )
        return errors
    if (extent.first_chapter, extent.first_verse) > (
        extent.last_chapter,
        extent.last_verse,
    ):
        errors.append(f"{label} ends before it begins")
    for chapter in (extent.first_chapter, extent.last_chapter):
        if chapter < 1 or chapter > ceilings[extent.token]:
            errors.append(
                f"{label} names {extent.token} {chapter}, past the canonical last "
                f"chapter {ceilings[extent.token]}"
            )
            return errors
    for chapter, verse in (
        (extent.first_chapter, extent.first_verse),
        (extent.last_chapter, extent.last_verse),
    ):
        ceiling = _catena._verse_ceiling(root, extent.token, chapter)
        if ceiling is not None and (verse < 1 or verse > ceiling):
            errors.append(
                f"{label} names {extent.token} {chapter}:{verse}, past the canonical "
                f"last verse {ceiling}"
            )
    return errors


# ---------------------------------------------------------------------------
# What is held, and what is named
# ---------------------------------------------------------------------------


def _held(root: Path) -> tuple[
    dict[tuple[str, str], set[int]],
    dict[tuple[str, str], int],
    dict[str, set[tuple[str, str]]],
]:
    """Chapters held, fragments held, and the alias groups a work answers to.

    The last of these is the reason nothing here needs a lookup table. Every
    fragment carries both identities — `work_id` from the source library and
    `work_alias` from the harvest — and `catena check` already refuses a
    fragment whose two identities name different people. So the join between
    the index's identity space and the library's is read off the fragments that
    already reconcile them, and there is no second copy of it to disagree.
    """
    chapters: dict[tuple[str, str], set[int]] = {}
    counts: dict[tuple[str, str], int] = {}
    aliases: dict[str, set[tuple[str, str]]] = {}
    for fragment in _catena.load_edges(root).get("fragments") or ():
        extent = _catena._extent(fragment.get("extent"))
        if extent is None:
            continue
        work_id = str(fragment.get("work_id") or "")
        key = (work_id, extent.token)
        chapters.setdefault(key, set()).update(
            range(extent.first_chapter, extent.last_chapter + 1)
        )
        counts[key] = counts.get(key, 0) + 1
        alias = fragment.get("work_alias")
        if isinstance(alias, dict):
            aliases.setdefault(work_id, set()).add(
                (str(alias.get("author")), str(alias.get("work")))
            )
    return chapters, counts, aliases


def _held_reach(root: Path) -> dict[tuple[str, str], tuple[tuple[int, int], tuple[int, int]]]:
    """The first and last canonical point a work's held fragments reach, per book."""
    reach: dict[tuple[str, str], tuple[tuple[int, int], tuple[int, int]]] = {}
    for fragment in _catena.load_edges(root).get("fragments") or ():
        extent = _catena._extent(fragment.get("extent"))
        if extent is None:
            continue
        key = (str(fragment.get("work_id") or ""), extent.token)
        first = (extent.first_chapter, extent.first_verse)
        last = (extent.last_chapter, extent.last_verse)
        if key in reach:
            held_first, held_last = reach[key]
            reach[key] = (min(held_first, first), max(held_last, last))
        else:
            reach[key] = (first, last)
    return reach


def _named(root: Path, wanted: set[tuple[str, str]]) -> dict[tuple[str, str], set[int]]:
    """Chapters the discovery index names each alias group on, keyed by group and book.

    Only the groups asked for are collected: the index names 579 distinct works
    and this report is about the ones acquisition has begun on. Every other row
    of the index is the acquisition list, which `discover` already answers, and
    restating it here would be a second answer to a settled question.
    """
    aliases = _catena._load_yaml(root / _catena.ALIASES_RELATIVE)
    title_of: dict[tuple[str, str], tuple[str, str]] = {}
    for group in aliases.get("groups") or ():
        key = (str(group.get("author")), str(group.get("work")))
        if key not in wanted:
            continue
        for title in group.get("titles") or ():
            title_of[(key[0], str(title))] = key

    token_of = {book["name"]: book["token"] for book in _catena.canon(root)}
    named: dict[tuple[str, str], set[int]] = {}
    index = _catena._load_yaml(root / _catena.INDEX_RELATIVE)
    for entry in index.get("passages") or ():
        # A row declaring its own numbering declares a DIFFERENT one, and the
        # works under it are about other text. `leads_for_book` drops those for
        # the same reason: counting one as coverage of the chapter it spells
        # would attribute a work to a passage it never addressed.
        if entry.get("numbering"):
            continue
        book, _, chapter = str(entry.get("passage") or "").rpartition(" ")
        if not chapter.isdigit() or book not in token_of:
            continue
        for work in entry.get("works") or ():
            key = title_of.get(
                (str(work.get("author")), str(work.get("title") or "").lower())
            )
            if key is not None:
                named.setdefault((key[0], key[1], token_of[book]), set()).add(int(chapter))
    return named


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------


def coverage(root: Path = ROOT, token: str | None = None) -> dict[str, Any]:
    """Every (work, book) acquisition has begun on, with what is not held.

    A row exists where the work holds a fragment on the book, or where the
    index names it there, or where an extent is recorded for it — restricted
    throughout to works this project holds something of somewhere. A work held
    nowhere is not under-covered, it is unacquired, and that is a different
    report.
    """
    chapters, counts, aliases = _held(root)
    recorded = extents(root)
    sources = _catena.load_sources(root)
    books = {book["token"]: book for book in _catena.canon(root)}
    groups = {group for sets in aliases.values() for group in sets}
    named = _named(root, groups)

    pairs: set[tuple[str, str]] = set(chapters) | set(recorded)
    for work_id, group_keys in aliases.items():
        for author, work in group_keys:
            for key in named:
                if key[0] == author and key[1] == work:
                    pairs.add((work_id, key[2]))
    if token is not None:
        pairs = {pair for pair in pairs if pair[1] == token}

    rows: list[dict[str, Any]] = []
    for work_id, book_token in sorted(pairs):
        if book_token not in books:
            continue
        work = sources.works.get(work_id) or {}
        held = chapters.get((work_id, book_token), set())
        names: set[int] = set()
        for author, alias_work in aliases.get(work_id, set()):
            names |= named.get((author, alias_work, book_token), set())
        extent = recorded.get((work_id, book_token))

        if extent is None:
            expected = set(names)
            status = UNEXAMINED
            beyond: set[int] = set()
        else:
            expected = extent.chapters()
            beyond = names - expected
            shortfall = expected - held
            if not shortfall:
                status = COMPLETE
            elif extent.within == SELECTIVE:
                status = NOT_ESTABLISHED
            else:
                status = GAP

        rows.append(
            {
                "work_id": work_id,
                "author": str(work.get("responsible") or ""),
                "work": str(work.get("title") or ""),
                "token": book_token,
                "book": books[book_token]["name"],
                "chapters_in_book": int(books[book_token]["last_chapter"]),
                "fragments": counts.get((work_id, book_token), 0),
                "named": sorted(names),
                "held": sorted(held),
                "extent": (
                    None
                    if extent is None
                    else {
                        "first_chapter": extent.first_chapter,
                        "first_verse": extent.first_verse,
                        "last_chapter": extent.last_chapter,
                        "last_verse": extent.last_verse,
                        "within": extent.within,
                    }
                ),
                "expected": sorted(expected),
                "missing": sorted(expected - held),
                # The independent signal, kept beside the derived one. Where an
                # extent is recorded the index is no longer the authority on
                # reach, but it is still a second witness, and a chapter it
                # names that the extent excludes is one of them being wrong.
                "named_not_held": sorted(names - held),
                "named_beyond_extent": sorted(beyond),
                "status": status,
                "note": STATUS_NOTE[status],
            }
        )

    rows.sort(
        key=lambda row: (
            -len(row["missing"]),
            STATUS_RANK[row["status"]],
            row["work_id"],
            row["token"],
        )
    )
    by_status = {status: 0 for status in STATUS_ORDER}
    for row in rows:
        by_status[row["status"]] += 1
    return {
        "schema": REPORT_SCHEMA,
        "numbering": _catena._projection.CANONICAL,
        "rows": rows,
        "totals": {
            "works": len({row["work_id"] for row in rows}),
            "rows": len(rows),
            "by_status": by_status,
            "chapters_missing": sum(len(row["missing"]) for row in rows),
            "extents_recorded": len([row for row in rows if row["extent"]]),
            "extents_unrecorded": len([row for row in rows if not row["extent"]]),
        },
    }


def summary_line(root: Path = ROOT) -> str:
    """One line for `make check`, naming the verb that expands it.

    A gap never fails the build — an unacquired work is not a defect — but a
    build that says nothing about it is how the hole stayed open for as long as
    it did, so the count is printed on every run.
    """
    report = coverage(root)
    totals = report["totals"]
    by_status = totals["by_status"]
    return (
        f"coverage: {totals['works']} works held, "
        f"{by_status[GAP]} with a gap inside a recorded extent, "
        f"{by_status[UNEXAMINED]} with no extent recorded, "
        f"{totals['chapters_missing']} chapters not held; "
        f"see `tpt commentary-work-index coverage`"
    )


def main(argv: list[str] | None = None) -> int:
    """The build's line: refuse an unusable record, report a gap, never fail on one.

    Deliberately flagless. The question a build asks is fixed — is the extent
    record usable, and how much is not held — and the question a person asks is
    `commentary-work-index coverage`, which is where every option lives. Two
    entry points, one question each.
    """
    if argv:
        print(f"coverage: unexpected argument {argv[0]!r}", file=sys.stderr)
        return 2
    try:
        errors = validate()
    except _catena.CatenaError as error:
        print(f"coverage: {error}", file=sys.stderr)
        return 2
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(
            f"work-extents invalid: {len(errors)} error(s)", file=sys.stderr
        )
        return 1
    print(summary_line())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
