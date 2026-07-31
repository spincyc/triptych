"""Project each tracked edition into one canonical shape, by reference.

`guidance/versification.md` §8.0 settles the shape and the reasoning; this is the
derivation. The short version: a projection is a set of rules, not a set of
verses. The default rule is identity and writes nothing, so the size of a
projection measures how far its edition sits from the canon rather than how large
the edition is. Nothing here copies scripture, and no edition on disk is altered:
a caller resolves a canonical reference to a locus in the edition's own numbering
and then reads the edition's own tracked text.

Every row is derived from something already tracked and already validated — the
psalm concordance through `_psalms`, the deuterocanon concordance through
`_deuterocanon`, and each edition's own `verse-aliases.tsv` and `book-index.tsv`.
Nothing is hand-typed beside them, which is the rule the psalm concordance's own
history exists to enforce.

`tools/index-bible` reads its alias rules through `alias_table` here, so the
rules the resolver follows and the rules a projection reports are one set read by
one parser; `index-bible check` derives the whole projection and refuses the
edition if it will not derive. What is not routed through here is the psalter,
and §8.0 records why: that conversion already happens a step earlier, over ranges
rather than verses, and applying it twice would land on real text some way from
the words cited.

The six override kinds are the vocabulary of §8.0. Five of them say where the
text is; `displaced` says only that the boundary moved and deliberately does not
say where to, because no source this project can reach models that and a guess
would be the exact defect this apparatus exists to catch.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import NamedTuple

import _psalms

# The system a projection projects *into*. Vulgate, because both tracked
# calendars cite in it, most tracked editions declare it, and the psalm
# concordance is authored from it. It is a parameter rather than a constant so
# that the choice stays visible; changing it changes every projection.
CANONICAL = "vulgate"

# §8.0's vocabulary. `identity` is not here: identity writes no row at all.
OVERRIDES = (
    "renumber",     # same text, different numbers
    "merge",        # the edition joins what the canon divides
    "split",        # the edition divides what the canon joins
    "absent",       # the edition does not carry it
    "displaced",    # numbers agree, the text boundary does not
    "unrecorded",   # known to diverge, correspondence not established
)

# What each tracked alias kind means in the projection's vocabulary. The alias
# tables were written for a different purpose — telling `Bible.verse` where a
# cited locus stands — so the mapping is stated here rather than assumed, and an
# unknown kind raises instead of defaulting to something plausible.
ALIAS_KINDS = {
    "merged-verse": "merge",
    "renumbered": "renumber",
    "not-in-this-edition": "absent",
    "numbering-not-recorded": "unrecorded",
}


class Row(NamedTuple):
    """One divergence. `resolves_to` is empty for a refusal."""

    cited_locus: str
    resolves_to: str
    kind: str
    note: str


class Locus(NamedTuple):
    """A book token and a point inside it, as an edition's own text is keyed."""

    token: str
    chapter: int
    verse: int


class ProjectionError(RuntimeError):
    """A projection could not be derived, with the reason a maintainer can act on."""


def _artifact(edition_root: Path, prefix: str, name: str) -> Path | None:
    """The one artifact of a kind under an edition, or None if it has none."""
    found = sorted(edition_root.glob(f"artifacts/{prefix}-*/{name}"))
    if len(found) > 1:
        raise ProjectionError(
            f"{edition_root}: expected one {prefix} artifact, found {len(found)}"
        )
    return found[0] if found else None


def alias_rows(edition_root: Path) -> list[Row]:
    """Every divergence this edition's own alias table already records.

    Read rather than re-derived. The alias table is the edition's own statement
    about itself and its answer is final — including a recorded refusal, which is
    a row with an empty `resolves_to` and a kind that says why.
    """
    path = _artifact(edition_root, "verse-aliases", "verse-aliases.tsv")
    if path is None:
        return []
    rows: list[Row] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for line, record in enumerate(csv.DictReader(handle, delimiter="\t"), start=2):
            kind = (record.get("kind") or "").strip()
            if kind not in ALIAS_KINDS:
                raise ProjectionError(
                    f"{path}:{line}: alias kind {kind!r} has no projection meaning; "
                    f"add it to ALIAS_KINDS rather than letting it default"
                )
            rows.append(
                Row(
                    cited_locus=(record.get("cited_locus") or "").strip(),
                    resolves_to=(record.get("resolves_to") or "").strip(),
                    kind=ALIAS_KINDS[kind],
                    note=(record.get("note") or "").strip(),
                )
            )
    return rows


def point(value: str, where: str) -> Locus:
    """`Ps.115.10` as the resolver addresses it, or a refusal naming the file."""
    try:
        token, chapter, verse = value.rsplit(".", 2)
        return Locus(token, int(chapter), int(verse))
    except ValueError as exc:
        raise ProjectionError(f"{where}: {value!r} is not a book.chapter.verse locus") from exc


def alias_table(edition_root: Path) -> dict[Locus, Locus | None]:
    """This edition's alias rules keyed the way a resolver asks for them.

    The same rows `alias_rows` returns, addressed by locus instead of listed: a
    cited locus maps to the locus of this edition that carries it, or to None
    where the row is a refusal. It exists so that the projection and the
    resolver read one table through one parser. They read it through two before,
    and the resolver's ignored the `kind` column entirely, so a kind nobody had
    given a projection meaning still resolved there as an ordinary merge — one
    table, two answers, and no way to see the disagreement.

    An edition with no alias artifact is refused here although `alias_rows`
    tolerates it. The projection of an edition that records no departures is
    genuinely empty; a resolver's is not, because an absent table and a
    forgotten one read exactly alike, which is the reason `knox-bible` writes an
    empty one rather than none.
    """
    if _artifact(edition_root, "verse-aliases", "verse-aliases.tsv") is None:
        raise ProjectionError(f"{edition_root}: no verse-aliases artifact to resolve through")
    where = str(edition_root)
    return {
        point(row.cited_locus, where): (
            point(row.resolves_to, where) if row.resolves_to else None
        )
        for row in alias_rows(edition_root)
    }


def psalm_rows(numbering: str) -> list[Row]:
    """Psalm divergences between this edition's numbering and the canonical one.

    Derived from the tracked concordance through `_psalms`, never restated. An
    edition already in the canonical numbering diverges in no psalm and gets no
    rows, which is the identity default doing its job.
    """
    if numbering == CANONICAL:
        return []
    if numbering != "hebrew":
        raise ProjectionError(
            f"no psalm projection from {numbering!r} into {CANONICAL!r}; "
            f"the concordance carries vulgate, hebrew and english only"
        )
    rows: list[Row] = []
    for psalm in range(1, _psalms.LAST_PSALM + 1):
        first, last = _psalms.psalm_extent(psalm, CANONICAL)
        for verse in range(first, last + 1):
            try:
                target = _psalms.convert_point(psalm, verse, CANONICAL, numbering)
            except _psalms.NumberingError as exc:
                rows.append(Row(f"Ps.{psalm}.{verse}", "", "unrecorded", str(exc)))
                continue
            chapter, moved, why = target
            if (chapter, moved) != (psalm, verse):
                rows.append(Row(f"Ps.{psalm}.{verse}", f"Ps.{chapter}.{moved}", "renumber", why))
    return rows


def _non_uniform_psalms() -> list[int]:
    """The psalms the concordance flags, read from the table rather than named.

    Read here and not imported: `_psalms.ENGLISH_UNIFORM` is the string "yes",
    the column's affirmative value, and iterating it yields three letters. That
    produced `displaced=3` for every edition on the first run — a plausible
    number, uniform across editions, and wrong, which is this repository's
    signature defect arriving in new code. The count is 16 and it is derived.

    Where the concordance lives is `_psalms`' answer and is asked of it, not
    restated: a second spelling of that path is the same one-table-two-copies
    fault the concordance itself exists to prevent, and it would fail here while
    `_psalms` went on converting from the file it found.
    """
    found = sorted(_psalms.CONCORDANCE_ROOT.glob(_psalms.CONCORDANCE_GLOB))
    if len(found) != 1:
        raise ProjectionError(
            f"expected one psalm concordance under {_psalms.CONCORDANCE_ROOT}, "
            f"found {len(found)}"
        )
    path = found[0]
    flagged: set[int] = set()
    with path.open(encoding="utf-8", newline="") as handle:
        for record in csv.DictReader(handle, delimiter="\t"):
            if (record.get("english_offset_uniform") or "").strip() != _psalms.ENGLISH_UNIFORM:
                flagged.add(int(record["hebrew_psalm"]))
    return sorted(flagged)


def displaced_psalms() -> list[Row]:
    """The psalms whose body divides differently, recorded and not resolved.

    These are the sixteen the concordance flags `english_offset_uniform: no`, and
    the row says only that the boundary moves. Saying where would need a subverse
    address the concordance cannot hold — see `_psalms._concordance` — and no
    source this project can reach supplies one: TVTMS has a `StartDifferent`
    relation for exactly this and uses it three times in its whole file, never in
    the Psalms.
    """
    rows: list[Row] = []
    for psalm in _non_uniform_psalms():
        rows.append(
            Row(
                f"Ps.{psalm}",
                "",
                "displaced",
                "the body divides differently here; the verse numbers correspond "
                "and the boundary does not, and this table cannot say where it moves to",
            )
        )
    return rows


def project(edition_root: Path, numbering: str) -> list[Row]:
    """Every rule this edition needs, sorted, with identity written nowhere."""
    rows = alias_rows(edition_root) + psalm_rows(numbering) + displaced_psalms()
    for row in rows:
        if row.kind not in OVERRIDES:
            raise ProjectionError(f"{row.cited_locus}: unknown override {row.kind!r}")
        if row.resolves_to and row.kind in ("absent", "unrecorded", "displaced"):
            raise ProjectionError(
                f"{row.cited_locus}: a {row.kind} row must not resolve to anything"
            )
    return sorted(rows)


def divergence(rows: list[Row]) -> dict[str, int]:
    """How far this edition sits from the canon, counted by kind."""
    counts = {kind: 0 for kind in OVERRIDES}
    for row in rows:
        counts[row.kind] += 1
    counts["total"] = len(rows)
    return counts
