"""Where a paragraph opens, for an edition that does not say so itself.

No edition in this library carries paragraph structure in its verse text. Every
tracked verse file is one verse per row and nothing else, and a chapter set from
it runs on as a single block. That is not a storage decision anyone made here on
purpose: it is what the acquisitions kept, and the paragraph markers the sources
carried were discarded at the point of derivation, which the verse-text
artifacts' own `transformation` fields still record having done.

Two questions follow, and this module keeps them apart, because conflating them
is how a typesetter's guess comes to look like an edition's own printing.

**Where does the edition itself open a paragraph?** For most editions here,
nowhere: the answer is not unknown, it is that the printing has no such marks.
The King James is the exception. Its standardized text prints 2,970 pilcrows,
the first at Genesis 1:6 and the last at Acts 20:36, after which the printers
stopped and the remaining twenty-two books carry none. Those are the edition's
own marks, they are recorded in its `paragraph-marks` artifact under the
`printed` column, and where they exist nothing needs to be projected at all.

**Where do the witnesses agree a paragraph opens?** Everywhere else. The answer
is a projection in the sense of `guidance/versification.md` §8.0 — a set of
rules over witnesses rather than a set of verses somebody chose — and it is
derived and tracked, never composed here. A row exists only where every witness
that can carry the verse opens a prose paragraph there and at least two do. The
positions the witnesses divide on are refused and counted; they are not resolved
by a majority, because the measured disagreement between two modern English
typesettings of the same books is roughly three positions in four, and a break
resting on one witness alone would read as this edition's own.

The whole layer is optional at the point of use, and that is the reason it is a
layer. `--no-paragraphs` returns the unprojected text byte for byte, because a
mechanical review of an edition must be able to see the edition and not this
project's reading of it.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The shared projection lives beside the psalm concordance, under the
# Douay-Rheims Challoner artifacts, for the same reason that one does: it is
# keyed in the numbering this repository cites in, which is that edition's, and
# a cross-edition table that lived nowhere in particular would be a table
# nothing validated.
PROJECTION_ROOT = (
    ROOT / "src" / "sources" / "works" / "english-college-of-douay"
    / "douay-rheims-bible" / "editions" / "challoner-gutenberg-1581" / "artifacts"
)
# Every path below names an edition's *artifacts* directory, which is what the
# registry records and what `Edition.artifacts` holds. Taking the edition
# directory instead would silently glob nothing and report an edition with no
# printed marks, which is a real answer for six of the seven editions here and
# would therefore never look wrong.
PROJECTION_GLOB = "paragraph-projection-*/paragraph-projection.tsv"
MARKS_GLOB = "paragraph-marks-*/paragraph-marks.tsv"

# What a break is credited to, and what the volume prints about it.
PRINTED = "printed"
PROJECTED = "projected"


class ParagraphError(RuntimeError):
    """The paragraph tables do not describe what they claim to describe."""


def _one(root: Path, pattern: str, what: str) -> Path | None:
    found = sorted(root.glob(pattern))
    if len(found) > 1:
        raise ParagraphError(f"expected one {what} under {root}, found {len(found)}")
    return found[0] if found else None


def _rows(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = [name for name in columns if name not in (reader.fieldnames or [])]
        if missing:
            raise ParagraphError(f"{path}: no {', '.join(missing)} column")
        return list(reader)


def printed_marks(artifacts: Path) -> set[tuple[str, int, int]]:
    """The verses at which this edition's own printing opens a paragraph.

    An edition with no `paragraph-marks` artifact returns the empty set, and so
    does one whose table records only a transcriber's markers. Those two cases
    are deliberately indistinguishable to a caller: neither is an edition that
    prints a paragraph mark, and a caller that treated the second as evidence
    would be crediting eBible.org's compositor to the printers of 1769.
    """
    found = _one(artifacts, MARKS_GLOB, "paragraph-marks artifact")
    if found is None:
        return set()
    return {
        (row["book"], int(row["chapter"]), int(row["verse"]))
        for row in _rows(found, ("book", "chapter", "verse", "kind", "printed"))
        if row["kind"] == "prose" and row["printed"] == "pilcrow"
    }


# A position the witnesses concur on: a paragraph opens there. A position
# exactly one of them breaks at: nothing opens there, and the row exists so the
# disagreement can be counted instead of merely not appearing.
CONCURRING = "concurring"
DISPUTED = "disputed"


def projection() -> dict[tuple[str, int, int], tuple[str, str]]:
    """Every position the projection has an opinion about, and what it is.

    Keyed in the numbering the projection is written in. The value is the
    witnesses that broke there, semicolon separated, and the rule — so a break
    can be walked back to the editions that testified to it, and a refusal to
    the one that stood alone.
    """
    found = _one(PROJECTION_ROOT, PROJECTION_GLOB, "paragraph-projection artifact")
    if found is None:
        raise ParagraphError(f"no paragraph projection under {PROJECTION_ROOT}")
    rows = _rows(found, ("book", "chapter", "verse", "witnesses", "rule"))
    table: dict[tuple[str, int, int], tuple[str, str]] = {}
    for row in rows:
        key = (row["book"], int(row["chapter"]), int(row["verse"]))
        if key in table:
            raise ParagraphError(f"{found}: {key} appears twice")
        if not row["witnesses"]:
            raise ParagraphError(f"{found}: {key} names no witness")
        if row["rule"] not in (CONCURRING, DISPUTED):
            raise ParagraphError(f"{found}: {key} carries unknown rule {row['rule']!r}")
        table[key] = (row["witnesses"], row["rule"])
    return table


def witnesses() -> list[str]:
    """Every edition the projection rests on, named, in order."""
    seen: set[str] = set()
    for named, _rule in projection().values():
        seen.update(named.split(";"))
    return sorted(seen)


def disagreement() -> tuple[int, int]:
    """How often the witnesses concur, out of every position either breaks at.

    Derived from the table rather than restated beside it. The volume prints
    this figure, and a figure typed into the prose of a renderer is a second
    source of truth that will eventually disagree with the table it describes.
    """
    rules = [rule for _named, rule in projection().values()]
    return rules.count(CONCURRING), len(rules)


def breaks(artifacts: Path, bible) -> dict[tuple[str, int, int], str]:
    """Where this edition opens a paragraph, in this edition's own numbering.

    Two sources, and the value says which: the edition's own printed marks,
    which need no conversion because they are already in its numbers, and the
    projection, each row of which is carried into this edition by the same
    `carrier` every citation in this library is resolved through. A projected
    row this edition cannot carry is dropped rather than placed nearby.
    """
    found: dict[tuple[str, int, int], str] = {}
    for token, chapter, verse in printed_marks(artifacts):
        found[(token, chapter, verse)] = PRINTED
    for (token, chapter, verse), (_named, rule) in projection().items():
        if rule != CONCURRING:
            continue
        here = bible.carrier(token, chapter, verse)
        if here is None:
            continue
        key = (here[0], int(here[1]), int(here[2]))
        found.setdefault(key, PROJECTED)
    return found


def counts(found: dict[tuple[str, int, int], str]) -> dict[str, int]:
    """How many breaks a volume owes to each source, for the volume to print."""
    return {
        "breaks": len(found),
        "printed": sum(1 for value in found.values() if value == PRINTED),
        "projected": sum(1 for value in found.values() if value == PROJECTED),
    }
