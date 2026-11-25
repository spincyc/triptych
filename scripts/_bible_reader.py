"""Read-only Bible edition text resolver and public manifest builder.

Shared by `tools/index-bible`, `_loci`, `_catena`, and commentary readers
without pulling `tools/index-bible`'s calendar-indexing (`mass-propers`) build
dependency into consumers that only read Bible editions or build manifests.
"""
from __future__ import annotations

import csv
from pathlib import Path
import re

from _bible_artifacts import select_book_index
from _bible_editions import EDITIONS, browser_print_offer
from _loci import NOT_CARRIED, RESOLVED_IN, Divergences as _SharedDivergences
from _projection import alias_rows, alias_table
from _psalms import addressing

ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "src" / "sources" / "works"
ELISION = " ... "
SPACING = re.compile(r"\s+")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sole(root: Path, prefix: str, suffix: str) -> Path:
    """The one file under a `<prefix>-<hash>/` artifact directory."""
    found = sorted(root.glob(f"{prefix}-*/*{suffix}"))
    if len(found) != 1:
        raise ValueError(f"expected exactly one {prefix} artifact under {root}, found {len(found)}")
    return found[0]


def normalize(name: str) -> str:
    return SPACING.sub(" ", name.replace(".", " ").strip()).casefold()


def load_books(artifacts: Path) -> dict[str, str]:
    """Map every name a calendar might print to this edition's book token."""
    selected = select_book_index(artifacts.parent)
    if selected is None:
        raise ValueError(f"no book-index artifact under {artifacts}")
    rows = read_tsv(selected)
    if not rows:
        raise ValueError("the edition's book index is empty")
    names: dict[str, str] = {}
    for row in rows:
        names[normalize(row["modern_name"])] = row["token"]
    for row in rows:
        token = row["token"]
        aliases = [token, row["douay_title"], *row["alternate_names"].split(";")]
        if token == "Ps":
            aliases.append("Psalm")
        for alias in aliases:
            key = normalize(alias)
            if key and key not in names:
                names[key] = token
    return names


def load_verses(artifacts: Path) -> dict[tuple[str, int, int], str]:
    verses: dict[tuple[str, int, int], str] = {}
    files = sorted(artifacts.glob("verse-text-*/*.tsv"))
    if not files:
        raise ValueError(f"no verse-text artifacts under {artifacts}")
    for path in files:
        for row in read_tsv(path):
            verses[(row["book"], int(row["chapter"]), int(row["verse"]))] = row["text"]
    return verses


def load_aliases(artifacts: Path):
    return alias_table(artifacts.parent)


class Bible:
    """One edition's text, addressed the way a citation addresses it."""

    def __init__(self, artifacts: Path) -> None:
        self.books = load_books(artifacts)
        self.verses = load_verses(artifacts)
        self.aliases = load_aliases(artifacts)
        self.alias_notes = {
            row.cited_locus: row.note
            for row in alias_rows(artifacts.parent)
            if not row.resolves_to
        }
        self.chapters: dict[tuple[str, int], tuple[int, int]] = {}
        for token, chapter, verse in self.verses:
            here = (token, chapter)
            low, high = self.chapters.get(here, (verse, verse))
            self.chapters[here] = (min(low, verse), max(high, verse))
        self._load_open_bounds()

    def _load_open_bounds(self) -> None:
        """Derive cited open bounds from this edition's native membership."""
        self.open_bounds: dict[tuple[str, int], tuple[int, int]] = {}
        recorded: dict[tuple[str, int], dict[int, tuple | None]] = {}
        for (token, chapter, verse), target in self.aliases.items():
            recorded.setdefault((token, chapter), {})[verse] = target
        for (token, chapter), aliases in recorded.items():
            bounds = self.chapters.get((token, chapter))
            if bounds is None:
                continue
            base, bound = bounds
            printed = {
                (token, chapter, verse)
                for verse in range(base, bound + 1)
                if (token, chapter, verse) in self.verses
            }
            if printed <= set(aliases.values()):
                self.open_bounds[(token, chapter)] = (min(aliases), max(aliases))
            elif any(target is not None and target[:2] != (token, chapter)
                     for target in aliases.values()):
                continue
            else:
                first = [verse for verse, target in aliases.items()
                         if target == (token, chapter, base)]
                last = [verse for verse, target in aliases.items()
                        if target == (token, chapter, bound)]
                self.open_bounds[(token, chapter)] = (
                    min([base, *first]), max([bound, *last])
                )

    def token(self, book: str) -> str | None:
        return self.books.get(normalize(book))

    def carrier(self, token: str, chapter: int, verse: int) -> tuple | None:
        here = (token, chapter, verse)
        if here in self.aliases:
            merged = self.aliases[here]
            return None if merged is None or merged not in self.verses else merged
        return here if here in self.verses else None

    def verse(self, token: str, chapter: int, verse: int) -> str | None:
        found = self.carrier(token, chapter, verse)
        return None if found is None else self.verses[found]

    def refusal(self, token: str, chapter: int, verse: int, bounds: tuple) -> str:
        base, bound = bounds
        if (token, chapter, verse) in self.aliases:
            note = self.alias_notes.get(f"{token}.{chapter}.{verse}")
            detail = f" ({note})" if note else ""
            return f"{token} {chapter}:{verse}{detail} {NOT_CARRIED}"
        if verse > bound:
            return (
                f"{token} {chapter}:{verse} is past {token} {chapter}:{bound}, the last "
                f"verse this edition prints in that chapter; record where this edition "
                f"carries it in its verse aliases, or correct the citation"
            )
        if verse < base:
            return (
                f"{token} {chapter}:{verse} is before {token} {chapter}:{base}, the first "
                f"verse this edition prints in that chapter; record where this edition "
                f"carries it in its verse aliases, or correct the citation"
            )
        return f"{token} {chapter}:{verse} is missing"

    def span(self, token: str, span: dict) -> tuple[list[str], str, tuple, tuple]:
        begin = span.get("begin") or {}
        end = span.get("end") or begin
        first = begin.get("chapter")
        last = end.get("chapter", first)
        if first is None:
            return [], "range has no chapter", (), ()
        texts: list[str] = []
        opened: tuple = ()
        closed: tuple = ()
        carried: tuple = ()
        for chapter in range(int(first), int(last) + 1):
            bounds = self.chapters.get((token, chapter))
            if bounds is None:
                recorded = sorted(
                    verse
                    for (held, held_chapter, verse) in self.aliases
                    if held == token and held_chapter == chapter
                )
                if not recorded:
                    return [], f"{token} has no chapter {chapter}", (), ()
                bounds = (recorded[0], recorded[-1])
            base, bound = self.open_bounds.get((token, chapter), bounds)
            low = begin.get("verse") if chapter == int(first) else None
            high = end.get("verse") if chapter == int(last) else None
            low = base if low is None else int(low)
            high = bound if high is None else int(high)
            for verse in range(low, high + 1):
                found = self.carrier(token, chapter, verse)
                if found is None:
                    return [], self.refusal(token, chapter, verse, bounds), (), ()
                closed = (chapter, verse)
                opened = opened or closed
                if found == carried:
                    continue
                carried = found
                texts.append(self.verses[found])
        return texts, "", opened, closed

    def passage(self, token: str, ranges: list) -> tuple[str, str]:
        parts: list[str] = []
        previous: tuple = ()
        for span in ranges:
            texts, problem, opened, closed = self.span(token, span)
            if problem:
                return "", problem
            if parts and opened:
                abuts = previous == (opened[0], opened[1] - 1)
                parts.append(" " if abuts else ELISION)
            parts.append(" ".join(texts))
            previous = closed or previous
        text = SPACING.sub(" ", "".join(parts)).strip()
        return text, "" if text else "no text found"


def other_numberings() -> tuple[str, ...]:
    return tuple(
        sorted(
            {str(edition["numbering"]) for edition in EDITIONS.values()} - {RESOLVED_IN}
        )
    )


class Divergences(_SharedDivergences):
    """Compatibility entry point using this repository's registered numbering set."""

    def __init__(
        self,
        calendar: str,
        document: dict,
        entries: list[dict],
        canon,
        numbering: str = RESOLVED_IN,
    ) -> None:
        super().__init__(
            calendar, document, entries, canon, numbering,
            numberings=other_numberings(),
        )


def manifest_document(servable) -> dict:
    """The public offer, using an explicit inventory of available editions."""
    offered = [
        {
            "id": name,
            "label": str(edition.get("label") or edition["edition"]),
            "edition": str(edition["edition"]),
            "source_id": str(edition["source_id"]),
            "print": browser_print_offer(name),
            "language": str(edition["language"]),
            "numbering": str(edition["numbering"]),
            "psalter": str(edition["psalter"]),
            "psalm_titles": str(edition["psalm_titles"]),
            "loci": addressing(str(edition["numbering"]), str(edition["psalm_titles"])),
            "rights": str(edition["rights"]),
        }
        for name, edition in sorted(
            EDITIONS.items(), key=lambda row: (row[1].get("rank", 999), row[0])
        )
        if edition["publishable"] and name in servable
    ]
    return {"bibles": offered}
