#!/usr/bin/env python3
"""Where each fragment of a Migne commentary begins and ends in Genesis.

`guidance/catena.md` Rule 5 stores a fragment at the extent its author addressed
and derives the chapter view from that. For the Genesis commentaries Migne
prints, the author's extent is not a matter of judgement at all: the printing
states it. Angelomus and Remigius head every block with `VERS. 11-13.`, Jerome's
with `(Cap. II.—Vers. 8.)`, Alcuin cites `(Gen. II, 7)` inside his answers, and
Bede opens every paragraph with the Vulgate lemma itself. This module reads that
apparatus and nothing else. It consults no model, and it reaches no network.

WHY IT DOES NOT SIMPLY BELIEVE THE PRINTING. The apparatus is a reference like
any other and fails the same way — successfully and wrongly. Migne's CAPUT
markers are the chapter, and they are *missing* at Genesis 5 in both Angelomus
and Remigius, at Genesis 30 in Angelomus, at Genesis 43 in Remigius (where the
running head prints `XLIII.` in a form no CAPUT pattern matches) and at Genesis
50 in both. Trusting them alone would have filed Adam's genealogy under Cain's
chapter and Joseph's death under Jacob's blessing, with every check passing.

So each block carries two independent statements of where it stands, and they
are made to argue:

    the printing's own  `CAPUT V` + `VERS. 8.`
    the lemma's words   matched against the Clementine Vulgate by 3-grams

A block is `agreed` when both name one chapter. The lemma overrules the caput
only when the *printed verse number falls on the matched verse* AND that match
scores within a fifth of the block's best match anywhere in Genesis — one
without the other is how Mathusala's years reached Genesis 11 and Ismael's
naming reached Genesis 30 in earlier passes of this same file. Everything else
is `caput-printed` (Migne named the chapter here), `caput` (the transcriber's
carried CAPUT, unopposed), `carried` (no evidence and no movement) or `advanced`
(the named chapter has too few verses to hold the printed number). Every
fragment records which of these settled it.

Bede is the exception and needed a different instrument, because his printing
marks neither chapter nor verse. His blocks are fitted as a *chain*: the
best-scoring assignment of loci to paragraphs that never runs backwards. Reading
each paragraph on its own and keeping a running maximum — the obvious method —
produced a book claiming Genesis 1, 2 and 5 and never 3 or 4, because one
spurious match ratchets and fifty right ones cannot pull it back.

    python3 scripts/_lemmata.py TRANSCRIPTION.txt --rule angelomus
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENESIS = ROOT / "src/sources/bibles/clementine-vulgate/chapters/Gen"

# The blocks a printing marks, per corpus. `angelomus` and `remigius` head a
# block with Migne's own `VERS. n.`; `jerome` heads it with `(Cap. N.—Vers. n.)`;
# `alcuin` numbers questions and names his verse inside the answer; `bede` marks
# nothing and opens each paragraph with the lemma, so its blocks are found by
# the lemma alone.
RULES = ("angelomus", "remigius", "jerome", "alcuin", "bede")

_VERS = re.compile(
    r"^\|?\s*(?:\(\s*)?(?:CAP(?:UT)?\.?\s*([IVXLC]+|\d+)\s*\.?\s*[—\-–]*\s*)?"
    r"VERS?\.\s*(\d+)(?:\s*[-,]\s*(?:seq\.?|(\d+)))?",
    re.IGNORECASE,
)
_INTER = re.compile(r"^\|?\s*(?:\d+\s+)?INTER(?:ROGATIO)?\.?\s*(\d+)\s*\.", re.IGNORECASE)
_GEN_CITE = re.compile(
    r"\(\s*Gen(?:es)?\.?\s*([IVXLC]+|\d+)\s*,\s*(\d+)(?:\s*[-,]\s*(\d+))?", re.IGNORECASE
)
# The head of a block, once the printing's own marker is taken off it.
# A bare `XLIII.` before the verse marker is Migne's running head, not a
# statement about this block: at Remigius line 404 it stands over a lemma that
# is Genesis 42:1. It is taken off the head so the lemma can be matched, and it
# is never read as a chapter.
_MARKER = re.compile(
    r"^[^A-Za-z]*(?:CAP\w*\.?\s*)?(?:[IVXLC]+\s*\.)?\s*"
    r"(?:CAP\w*\.?\s*[IVXLC\d]+\s*[—\-–.]*)?\s*VERS?\.[\d\s,\-]*(?:seq\.?)?[\s.]*[—\-–]*",
    re.IGNORECASE,
)
_LOCATOR = re.compile(r"^\{(\d+)\.(\d+)\}\s*(.*)$")

_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def arabic(numeral: str | None) -> int | None:
    """`XIV` and `14` alike as a number, or None if it is neither."""
    if numeral is None:
        return None
    numeral = str(numeral).strip().upper()
    if numeral.isdigit():
        return int(numeral)
    if not numeral or any(character not in _ROMAN for character in numeral):
        return None
    total = 0
    previous = 0
    for character in reversed(numeral):
        value = _ROMAN[character]
        total = total - value if value < previous else total + value
        previous = max(previous, value)
    return total


def fold(text: str) -> list[str]:
    """A Latin string as comparable words.

    Migne, the Clementine and the Vetus Latina spell the same word four ways,
    so the fold is deliberately heavy: accents dropped, `ae`/`oe` to `e`, `j` to
    `i`, `v` to `u`, `y` to `i`. It exists to compare, never to print.
    """
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.replace("ae", "e").replace("oe", "e")
    text = text.replace("j", "i").replace("v", "u").replace("y", "i")
    return re.sub(r"[^a-z ]", " ", text).split()


def _grams(words: list[str], size: int = 3) -> set[tuple[str, ...]]:
    return {tuple(words[index:index + size]) for index in range(len(words) - size + 1)}


class Genesis:
    """The Clementine's Genesis, folded, with the 3-grams of every verse."""

    def __init__(self, directory: Path = GENESIS) -> None:
        self.verses: dict[tuple[int, int], list[str]] = {}
        self.last_verse: dict[int, int] = {}
        for chapter in range(1, 51):
            payload = json.loads((directory / f"{chapter}.json").read_text(encoding="utf-8"))
            for number, text in payload["verses"].items():
                self.verses[(chapter, int(number))] = fold(text)
                self.last_verse[chapter] = max(self.last_verse.get(chapter, 0), int(number))
        self.grams = {locus: _grams(words) for locus, words in self.verses.items()}

    def match(self, head: list[str], floor: float = 0.10) -> list[tuple[float, tuple[int, int]]]:
        """The loci whose words this head shares, best first."""
        wanted = _grams(head)
        if not wanted:
            return []
        found = []
        for locus, present in self.grams.items():
            shared = len(wanted & present)
            if shared:
                score = shared / max(1, min(len(wanted), len(present)))
                if score >= floor:
                    found.append((score, locus))
        found.sort(reverse=True)
        return found


def read(path: Path) -> list[tuple[int, int, int, str]]:
    """A transcription as `(line, unit, caput, prose)`, one per printed paragraph."""
    rows = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        found = _LOCATOR.match(line)
        if not found:
            raise ValueError(f"{path}:{number}: no locator")
        rows.append((number, int(found.group(1)), int(found.group(2)), found.group(3)))
    return rows


def blocks(rows, rule: str, genesis: Genesis) -> list[dict]:
    """The printing's own divisions, before any chapter is resolved.

    A block runs from its marker to the paragraph before the next marker, so the
    unmarked paragraphs that continue a lemma stay with the lemma they continue
    rather than becoming fragments addressing nothing.
    """
    found: list[dict] = []
    for number, _unit, caput, prose in rows:
        if rule in ("angelomus", "remigius", "jerome"):
            marker = _VERS.match(prose)
            if not marker:
                continue
            found.append(
                {
                    "line": number,
                    "caput": caput,
                    "marked_caput": arabic(marker.group(1)),
                    "first_verse": int(marker.group(2)),
                    "stated_last_verse": int(marker.group(3)) if marker.group(3) else None,
                    "prose": prose,
                }
            )
        elif rule == "alcuin":
            marker = _INTER.match(prose)
            if not marker:
                continue
            cites = [
                (arabic(chapter), int(first), int(last) if last else None)
                for chapter, first, last in _GEN_CITE.findall(prose)
            ]
            cites = [cite for cite in cites if cite[0] and 1 <= cite[0] <= 50]
            found.append(
                {
                    "line": number,
                    "caput": caput,
                    "marked_caput": None,
                    "question": int(marker.group(1)),
                    "cites": cites,
                    "first_verse": cites[0][1] if cites else None,
                    "stated_last_verse": None,
                    "prose": prose,
                }
            )
        elif rule == "bede":
            continue  # settled together, below, because the chain is the evidence
        else:
            raise ValueError(rule)
    if rule == "bede":
        found = _monotone_chain(rows, genesis)
    for current, following in zip(found, found[1:] + [{"line": rows[-1][0] + 1}]):
        current["last_line"] = following["line"] - 1
    return found


def _monotone_chain(rows, genesis: Genesis, floor: float = 0.18) -> list[dict]:
    """Bede's lemmata as one non-decreasing walk through Genesis.

    Bede's printing marks no chapter and no verse: every paragraph simply opens
    with the Vulgate lemma. Taking each paragraph's best match on its own and
    keeping the running maximum is what a first attempt does, and it is wrong in
    a way that is invisible — one spurious match at Genesis 5 ratchets the
    chapter up and the next fifty paragraphs, whose lemmata are plainly Genesis 3
    and 4, inherit it. Book I came out claiming Genesis 1, 2 and 5, and never 3
    or 4, while every verse number in it was right.

    A commentary that runs through a book in order is a *chain*, so the chain is
    what is fitted: the best-scoring assignment of loci to paragraphs that never
    moves backwards, by the usual dynamic programme. One bad match then loses to
    the fifty good ones around it instead of overruling them.
    """
    loci = sorted(genesis.verses)
    position = {locus: index for index, locus in enumerate(loci)}
    # `reach[index]` is the best total achievable by a chain whose last locus is
    # at or before `index`, and `held[index]` the choice that achieved it.
    reach = [0.0] * len(loci)
    held: list[tuple[int, int] | None] = [None] * len(loci)
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {}
    scored: dict[tuple[int, int], float] = {}
    for step, (_number, _unit, _caput, prose) in enumerate(rows):
        proposals = []
        for score, locus in genesis.match(fold(prose)[:25], floor=floor)[:6]:
            index = position[locus]
            proposals.append((index, reach[index] + score, held[index]))
        for index, total, predecessor in proposals:
            if total > reach[index]:
                reach[index] = total
                held[index] = (step, index)
                came_from[(step, index)] = predecessor
                scored[(step, index)] = total
        running = 0.0
        carried: tuple[int, int] | None = None
        for index in range(len(loci)):
            if reach[index] > running:
                running, carried = reach[index], held[index]
            else:
                reach[index], held[index] = running, carried
    chosen: dict[int, tuple[int, int]] = {}
    marker = held[-1]
    while marker is not None:
        step, index = marker
        chosen[step] = loci[index]
        marker = came_from[marker]
    found = []
    for step, (number, _unit, _caput, prose) in enumerate(rows):
        if step not in chosen:
            continue
        chapter, verse = chosen[step]
        found.append(
            {
                "line": number,
                "caput": chapter,
                "marked_caput": None,
                "first_verse": verse,
                "stated_last_verse": None,
                "prose": prose,
            }
        )
    return found


def resolve(found: list[dict], genesis: Genesis, rule: str) -> None:
    """Give every block its Genesis chapter, and say what settled it."""
    chapter = 1
    printed = None
    for block in found:
        if rule == "alcuin":
            block["chapter"] = block["cites"][0][0] if block["cites"] else None
            block["disposition"] = "cited" if block["cites"] else "no-verse-named"
            continue
        if block["marked_caput"] is not None:
            printed = block["marked_caput"]
        # What the printing says, carried forward from its last statement of it.
        # Jerome's page carries no CAPUT division at all, so `Cap. XVII.` printed
        # inside a lemma governs every quaestio until `Cap. XVIII.`; Angelomus
        # and Remigius carry Migne's CAPUT, which the transcriber already holds
        # until the next one.
        declared = block["marked_caput"] or (printed if rule == "jerome" else block["caput"])
        head = fold(_MARKER.sub("", block["prose"]))[:25]
        candidates = genesis.match(head)
        # The lemma overrules the printing only when the two halves of one match
        # agree: the best-scoring locus in Genesis must be in the chapter, and
        # the verse the printing numbered must be the verse that locus is. One
        # without the other is how Mathusala's years reached Genesis 11 and
        # Ismael's naming reached Genesis 30.
        confirming: dict[int, float] = {}
        for score, locus in candidates:
            if locus[1] == block["first_verse"]:
                confirming.setdefault(locus[0], score)
        leading_score = candidates[0][0] if candidates else 0.0
        # Near enough to the best match to be the same reading of it. Genesis is
        # full of verses that repeat each other's words a chapter apart, so the
        # confirmed chapter has to be competitive, not merely present.
        confirmed = sorted(c for c, score in confirming.items() if score >= leading_score * 0.8)
        leading = confirmed[0] if confirmed else None
        if rule == "bede":
            # Bede marks no caput at all, so the lemma is the only statement
            # there is and the block was found by it.
            chosen, how = max(block["caput"], chapter), "lemma"
        elif leading is not None and leading >= chapter and leading != declared:
            chosen, how = leading, "lemma-confirmed"
        elif declared is not None and declared >= chapter and block["first_verse"] <= genesis.last_verse[declared]:
            chosen = declared
            how = "agreed" if leading == declared else ("caput-printed" if block["marked_caput"] else "caput")
        else:
            chosen, how = chapter, "carried"
        # A chapter too short to hold the printed verse number is not the
        # chapter, whatever said so. Advance to the first that can hold it.
        while chosen < 50 and block["first_verse"] > genesis.last_verse[chosen]:
            chosen += 1
            how = "advanced"
        block["chapter"], block["disposition"] = chosen, how
        chapter = chosen


def extents(found: list[dict], rows, genesis: Genesis, rule: str) -> None:
    """Close each block's extent at the last verse its own paragraphs reach.

    The head marker opens the extent. What closes it is either the printing's
    own range (`VERS. 11-13`) or the furthest verse of the same chapter that a
    continuation paragraph's lemma lands on — never past the verse before the
    next block starts, because those words belong to the next block.
    """
    prose_by_line = {number: text for number, _unit, _caput, text in rows}
    for index, block in enumerate(found):
        if block.get("chapter") is None:
            block["last_verse"] = None
            continue
        chapter = block["chapter"]
        last = block["stated_last_verse"] or block["first_verse"]
        if rule == "alcuin":
            for cited_chapter, first, cited_last in block["cites"]:
                if cited_chapter == chapter:
                    last = max(last, cited_last or first)
            block["last_verse"] = min(last, genesis.last_verse[chapter])
            continue
        ceiling = genesis.last_verse[chapter]
        following = found[index + 1] if index + 1 < len(found) else None
        if following and following.get("chapter") == chapter:
            ceiling = max(block["first_verse"], following["first_verse"] - 1)
        for line in range(block["line"] + 1, block["last_line"] + 1):
            candidates = genesis.match(fold(prose_by_line[line])[:25], floor=0.25)
            for _score, locus in candidates[:1]:
                if locus[0] == chapter and block["first_verse"] <= locus[1] <= ceiling:
                    last = max(last, locus[1])
        block["last_verse"] = min(max(last, block["first_verse"]), ceiling)


def derive(path: Path, rule: str) -> list[dict]:
    genesis = Genesis()
    rows = read(path)
    found = blocks(rows, rule, genesis)
    resolve(found, genesis, rule)
    extents(found, rows, genesis, rule)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("transcription", type=Path)
    parser.add_argument("--rule", choices=RULES, required=True)
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    found = derive(arguments.transcription, arguments.rule)
    if arguments.json:
        json.dump(found, sys.stdout, ensure_ascii=False, indent=1)
        return 0
    for block in found:
        extent = (
            f"Gen {block['chapter']}:{block['first_verse']}-{block['last_verse']}"
            if block.get("chapter")
            else "no verse named"
        )
        print(
            f"{block['line']:5d}-{block['last_line']:<5d} {extent:20s} "
            f"{block['disposition']:16s} {block['prose'][:70]}"
        )
    print(f"{len(found)} blocks", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
