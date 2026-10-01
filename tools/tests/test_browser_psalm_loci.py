"""The propers browser reads the loci its edition actually prints.

Three defects of one kind, each a page rendering real Scripture at the wrong
place with nothing to say so, all left standing on 2026-09-25:

  1. An edition that leaves psalm titles unnumbered -- the King James, the
     Revised Version, the World English -- was handed the Hebrew loci, so
     wherever a psalm has a numbered heading it was one or two verses off:
     the Lent 1 *Miserere*, Hebrew 51:3-4, opened at "For I acknowledge my
     transgressions" (KJV 51:3) instead of "Have mercy upon me, O God".
  2. The Clementine's own verse-alias table was ignored, so Lent 2's
     responsorial psalm, Hebrew 116:10 (Vulgate 115:10), was served from the
     Clementine's 115:10 -- *in atriis domus Domini*, the psalm's LAST verse --
     where it prints *Credidi, propter quod locutus sum* at 115:1.
  3. A citation's reference line never said which psalm numbering it is
     written in, though one calendar cites in both.

No numbering logic ships to the browser, so the fix is in the data
(`tools/mass-propers structure`, `tools/index-bible manifest`) and the page only
takes the loci it is given. These tests run the shared browser core under node
against the tracked structure, manifest and chapter fragments.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src/web/data"
CORE = ROOT / "src/web/browser/shared/browser-core.js"
BIBLES = ROOT / "src/sources/bibles"

# A minimal document: enough for `renderCitation` to build its block, and a
# `text()` that flattens what it built the way a reader would see it.
RUNNER = r"""
const fs = require('node:fs');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));

function node(tag) {
  return {
    tagName: tag, className: '', children: [], attributes: {}, _text: '',
    appendChild(child) { this.children.push(child); return child; },
    setAttribute(name, value) { this.attributes[name] = String(value); },
    removeChild() {},
    get firstChild() { return this.children[0] || null; },
    set textContent(value) { this._text = String(value); this.children = []; },
    get textContent() { return this._text + this.children.map((c) => c.textContent).join(''); }
  };
}
global.document = {
  createElement: (tag) => node(tag),
  createDocumentFragment: () => node('#fragment'),
  createTextNode: (text) => ({ textContent: String(text) })
};
global.window = { location: { search: '' } };
require(input.core);
const T = global.window.Triptych;

function find(root, cls, out) {
  out = out || [];
  if (root && root.className && root.className.split(' ').includes(cls)) out.push(root);
  for (const child of (root && root.children) || []) find(child, cls, out);
  return out;
}

const output = {};
for (const [name, job] of Object.entries(input.jobs)) {
  if (job.op === 'loci') {
    output[name] = T.editionLoci(job.citation, job.bible);
  } else if (job.op === 'chapters') {
    output[name] = T.chaptersNeeded(
      [job.citation], T.lociKey(job.bible), job.bible.id);
  } else if (job.op === 'render') {
    const fragments = new Map(Object.entries(job.fragments));
    const block = T.renderCitation(job.citation, job.bible, fragments, job.sourceNumbering);
    output[name] = {
      ref: find(block, 'citation-ref').map((n) => n.textContent),
      numbering: find(block, 'citation-numbering').map((n) => n.textContent),
      verses: find(block, 'verse').map((n) => n.textContent.trim())
    };
  } else if (job.op === 'proper') {
    const fragments = new Map(Object.entries(job.fragments));
    const section = T.renderProper(job.proper, job.bible, fragments, { numbering: job.sourceNumbering });
    const refs = find(section, 'proper-ref');
    output[name] = {
      ref: refs.map((n) => n.textContent),
      nested: refs.map((n) => find(n, 'citation-numbering').map((m) => m.textContent))
    };
  } else if (job.op === 'meta') {
    output[name] = T.bibleMeta(job.bible);
  }
}
process.stdout.write(JSON.stringify(output));
"""


def node_available() -> bool:
    return shutil.which("node") is not None


def run(jobs: dict) -> dict:
    result = subprocess.run(
        ["node", "-e", RUNNER],
        input=json.dumps({"core": str(CORE), "jobs": jobs}),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def bible(edition: str) -> dict:
    manifest = json.loads((DATA / "bibles.json").read_text(encoding="utf-8"))
    for record in manifest["bibles"]:
        if record["id"] == edition:
            return record
    raise AssertionError(f"bibles.json does not offer {edition}")


def citation(calendar: str, mass: str, proper: str, ref: str) -> tuple[dict, str]:
    """A tracked structure citation, and the numbering its file declares."""
    payload = json.loads(
        (DATA / f"structure/propers/{calendar}.json").read_text(encoding="utf-8")
    )
    (found,) = [row for row in payload["masses"] if row["key"] == mass]
    owners = []
    for row in found["propers"]:
        if row["name"] != proper:
            continue
        owners.append(row)
        for course in ("cycles", "weekday_cycles"):
            owners.extend((row.get(course) or {}).values())
    for owner in owners:
        for cited in owner["citations"]:
            if cited["ref"] == ref:
                return cited, payload["numbering"]
    raise AssertionError(f"{calendar} {mass} {proper} cites no {ref}")


def fragment(edition: str, chapter: int) -> dict:
    data = json.loads((BIBLES / edition / "chapters/Ps" / f"{chapter}.json").read_text("utf-8"))
    return {"ok": True, "verses": data["verses"]}


def shape(answer: dict) -> list[tuple]:
    """The loci a page would fetch: book token, chapter, first and last verse."""
    if "loci" not in answer:
        raise AssertionError(answer.get("problem"))
    return [(row["book"], row["chapter"], row["first"], row["last"]) for row in answer["loci"]]


@unittest.skipUnless(node_available(), "node is required to run the shared browser core")
class TitleConventionTests(unittest.TestCase):
    """1. An edition that leaves psalm titles unnumbered reads its own loci."""

    def test_every_offered_edition_names_the_loci_it_reads(self) -> None:
        manifest = json.loads((DATA / "bibles.json").read_text(encoding="utf-8"))
        wanted = {
            ("vulgate", "numbered"): "vulgate",
            ("hebrew", "numbered"): "hebrew",
            ("hebrew", "unnumbered"): "hebrew-unnumbered-titles",
        }
        for record in manifest["bibles"]:
            with self.subTest(edition=record["id"]):
                self.assertEqual(
                    record.get("loci"), wanted[(record["numbering"], record["psalm_titles"])]
                )

    def test_the_lent_one_miserere_opens_at_have_mercy_in_the_king_james(self) -> None:
        cited, _ = citation(
            "postconciliar", "lent-1", "Responsorial Psalm", "Psalm 51:3-4, 5-6a, 12-13, 14, 17"
        )
        answers = run({
            edition: {"op": "loci", "citation": cited, "bible": bible(edition)}
            for edition in ("king-james-version", "revised-version-1895",
                            "world-english-bible-catholic", "douay-rheims")
        })
        for edition in ("king-james-version", "revised-version-1895",
                        "world-english-bible-catholic"):
            with self.subTest(edition=edition):
                self.assertEqual(shape(answers[edition])[0], ("Ps", 51, 1, 2))
        # A title-numbering edition still reads the Vulgate numbering it cites in.
        self.assertEqual(shape(answers["douay-rheims"])[0], ("Ps", 50, 3, 4))
        verses = run({"kjv": {
            "op": "render", "citation": cited, "bible": bible("king-james-version"),
            "fragments": {"Ps|51": json.loads(
                (BIBLES / "king-james-version/chapters/Ps/51.json").read_text("utf-8")
            ) | {"ok": True}},
            "sourceNumbering": "hebrew",
        }})["kjv"]["verses"]
        self.assertTrue(verses[0].startswith("1"), verses[0])
        self.assertIn("Have mercy upon me, O God", verses[0])

    def test_a_psalm_the_convention_cannot_carry_is_refused_with_its_reason(self) -> None:
        """Hebrew 29, whose body the concordance records as divided differently."""
        cited, _ = citation(
            "postconciliar", "baptism-of-the-lord", "Responsorial Psalm",
            "Psalm 29:1a, 2, 3ac-4, 3b, 9b-10",
        )
        answer = run({"kjv": {
            "op": "loci", "citation": cited, "bible": bible("king-james-version")
        }})["kjv"]
        self.assertNotIn("loci", answer)
        self.assertIn("divide Psalm 29 differently", answer["problem"])

    def test_the_heading_says_how_the_edition_numbers_its_psalms(self) -> None:
        metas = run({
            "kjv": {"op": "meta", "bible": bible("king-james-version")},
            "drb": {"op": "meta", "bible": bible("douay-rheims")},
        })
        self.assertIn("psalm titles unnumbered", " ".join(metas["kjv"]))
        self.assertNotIn("unnumbered", " ".join(metas["drb"]))


@unittest.skipUnless(node_available(), "node is required to run the shared browser core")
class EditionDepartureTests(unittest.TestCase):
    """2. An edition's own verse-alias table moves the loci it reads."""

    def test_lent_two_reads_credidi_in_the_clementine(self) -> None:
        cited, numbering = citation(
            "postconciliar", "lent-2", "Responsorial Psalm", "Psalm 116:10, 15, 16-17, 18-19"
        )
        answers = run({
            "loci": {"op": "loci", "citation": cited, "bible": bible("clementine-vulgate")},
            "douay": {"op": "loci", "citation": cited, "bible": bible("douay-rheims")},
            "chapters": {"op": "chapters", "citation": cited,
                         "bible": bible("clementine-vulgate")},
            "render": {
                "op": "render", "citation": cited, "bible": bible("clementine-vulgate"),
                "fragments": {"Ps|115": fragment("clementine-vulgate", 115)},
                "sourceNumbering": numbering,
            },
        })
        self.assertEqual(
            shape(answers["loci"]),
            [("Ps", 115, 1, 1), ("Ps", 115, 6, 6), ("Ps", 115, 7, 8), ("Ps", 115, 9, 10)],
        )
        # The witness the numbering is read from needs nothing moved.
        self.assertEqual(shape(answers["douay"])[0], ("Ps", 115, 10, 10))
        self.assertEqual(answers["chapters"], [{"book": "Ps", "chapter": 115}])
        verses = answers["render"]["verses"]
        self.assertIn("Credidi, propter quod locutus sum", verses[0])
        self.assertNotIn("in atriis domus Domini", verses[0])

    def test_a_verse_the_edition_divides_refuses_with_the_tables_reason(self) -> None:
        """Clementine Psalm 42:5 is split between its 4 and 5; no verse carries it whole."""
        cited = {
            "ref": "Psalm 42:4-6", "book": "Psalms", "token": "Ps", "numbering": "vulgate",
            "loci": {"vulgate": [{"chapter": 42, "first": 4, "last": 6}]},
            "refused": {"clementine-vulgate": "Ps 42:5 is recorded as not carried by this edition"},
            "unresolved": None,
        }
        answer = run({"c": {"op": "loci", "citation": cited,
                            "bible": bible("clementine-vulgate")}})["c"]
        self.assertEqual(answer.get("problem"), "Ps 42:5 is recorded as not carried by this edition")


@unittest.skipUnless(node_available(), "node is required to run the shared browser core")
class CitationNumberingTests(unittest.TestCase):
    """3. A psalm citation says which numbering it is written in."""

    def test_a_vulgate_antiphon_in_a_hebrew_missal_names_its_numbering(self) -> None:
        cited, numbering = citation(
            "postconciliar", "ot-25", "Communion Antiphon", "Psalm 118:4-5"
        )
        self.assertEqual(numbering, "hebrew")
        self.assertEqual(cited["numbering"], "vulgate")
        shown = run({"r": {
            "op": "render", "citation": cited, "bible": bible("douay-rheims"),
            "fragments": {"Ps|118": fragment("douay-rheims", 118)},
            "sourceNumbering": numbering,
        }})["r"]
        self.assertEqual(shown["numbering"], ["Vulgate numbering"])
        self.assertIn("Psalm 118:4-5", shown["ref"][0])

    def test_a_propers_heading_names_its_numbering_inside_its_reference(self) -> None:
        """Inside `.proper-ref`, so Contents, which strips the reference from a
        heading's label, strips the numbering with it."""
        cited, numbering = citation(
            "postconciliar", "ot-25", "Communion Antiphon", "Psalm 118:4-5"
        )
        shown = run({"p": {
            "op": "proper",
            "proper": {"name": "Communion Antiphon", "source": "scripture", "citations": [cited]},
            "bible": bible("douay-rheims"),
            "fragments": {"Ps|118": fragment("douay-rheims", 118)},
            "sourceNumbering": numbering,
        }})["p"]
        self.assertEqual(shown["nested"], [["Vulgate numbering"]])

    def test_a_reading_from_another_book_names_no_psalm_numbering(self) -> None:
        cited, numbering = citation("postconciliar", "lent-2", "Gospel", "Mark 9:2-10")
        self.assertNotIn("numbering", cited)
        shown = run({"r": {
            "op": "render", "citation": cited, "bible": bible("douay-rheims"),
            "fragments": {}, "sourceNumbering": numbering,
        }})["r"]
        self.assertEqual(shown["numbering"], [])


if __name__ == "__main__":
    unittest.main()
