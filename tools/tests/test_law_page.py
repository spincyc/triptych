"""The law page's model: what it reads, and what it refuses to guess.

The page that serves the Code is the one place in this repository where a wrong
answer is a citation to the wrong law, so the tests here are about refusals
rather than about rendering. Three of them exist because the obvious
implementation is wrong:

  * a canon's number is never the last run of digits in an identifier. The
    generator writes `cic17-c-1012-1`, and the lazy reading of that is canon 1.
  * a lookup is exact. A citation this record does not carry is answered by
    saying so, not by offering the canon next to it.
  * two Codes number independently, so one number in two bodies of law is two
    canons and must never be gathered into one.

The model lives in the browser, so this replays it there, exactly as the catena
and the rubrics do.
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAGE = ROOT / "src/web/browser/law"
MODEL = PAGE / "code-model.js"
SCRIPT = PAGE / "law.js"
MARKUP = PAGE / "index.html"
FIXTURE = ROOT / "src/web/browser/fixture/structure/act-history/code-of-canon-law"

# The model asks the shared machinery for the station-kind rule and for nothing
# else, so the harness supplies that and no more: a shim that also supplied a
# DOM would let a model that had grown a DOM dependency pass.
HARNESS = """
const fs = require('fs');
global.window = { Triptych: { stationKind: {
  PROMULGATED: 'promulgated', PRINTED: 'printed', UNSTATED: 'unstated',
  stated: (rows) => (rows || []).some((row) => row && row.station_kind),
  of: (row, stated) => (row && row.station_kind) || (stated ? 'unstated' : 'promulgated')
} } };
new Function('window', fs.readFileSync(process.argv[1], 'utf8'))(global.window);
const C = global.window.TriptychCode;
const answer = (%s);
process.stdout.write(JSON.stringify(answer));
"""


def ask(expression: str) -> object:
    """Evaluate one expression against the browser's own model."""
    try:
        result = subprocess.run(
            ["node", "-e", HARNESS % expression, str(MODEL)],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:  # pragma: no cover - environment without node
        raise unittest.SkipTest("node is not installed") from None
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


def rows(*units: dict) -> str:
    return json.dumps(list(units))


class CitationTests(unittest.TestCase):
    """A canon lawyer arrives with a citation, in whichever form he writes it."""

    def test_every_written_form_of_one_citation_is_the_same_place(self) -> None:
        forms = ["1095", "c. 1095", "c 1095", "can. 1095", "canon 1095", "  1095  "]
        self.assertEqual(
            ask(f"{json.dumps(forms)}.map((form) => C.parseCitation(form))"),
            [{"canon": "1095", "paragraph": None}] * len(forms),
        )

    def test_a_cited_paragraph_survives_the_reading(self) -> None:
        forms = ["c. 1095 §2", "can. 1095, § 2", "1095.2", "1095 par. 2"]
        self.assertEqual(
            ask(f"{json.dumps(forms)}.map((form) => C.parseCitation(form))"),
            [{"canon": "1095", "paragraph": "2"}] * len(forms),
        )

    def test_what_is_not_a_citation_is_refused_rather_than_coerced(self) -> None:
        self.assertEqual(
            ask("['matrimonio', '', 'c. ', 'Liber VI'].map((f) => C.parseCitation(f))"),
            [None, None, None, None],
        )


class NumberTests(unittest.TestCase):
    """The number is read from the forms the generator writes, and no others."""

    def test_an_identifier_is_not_read_as_its_last_digits(self) -> None:
        # `cic17-c-1012-1` is canon 1012 §1. Read as a trailing number it is
        # canon 1, which is a citation to the wrong law.
        unit = {"unit": "cic17-c-1012-1", "slot": "can-1012-01", "name": "can. 1012 §1"}
        self.assertEqual(ask(f"C.numberOf({json.dumps(unit)})"),
                         {"canon": "1012", "paragraph": "1"})

    def test_each_written_form_alone_carries_the_number(self) -> None:
        self.assertEqual(
            ask("[C.numberOf({name: 'can. 1012 §1'}),"
                " C.numberOf({slot: 'can-1012-01'}),"
                " C.numberOf({unit: 'cic17-c-1012-1'}),"
                " C.numberOf({name: 'can. 6'})]"),
            [
                {"canon": "1012", "paragraph": "1"},
                {"canon": "1012", "paragraph": "1"},
                {"canon": "1012", "paragraph": "1"},
                {"canon": "6", "paragraph": None},
            ],
        )

    def test_a_row_that_is_not_a_canon_yields_no_number(self) -> None:
        # A liturgical slice drawn on this page must not have its prayers
        # reported as canons because a slug happens to end in a digit.
        unit = {"unit": "ordo.offertorium.lavabo", "slot": "psalmus-lavabo",
                "name": "Psalmus 50, 4"}
        self.assertEqual(ask(f"C.numberOf({json.dumps(unit)})"),
                         {"canon": None, "paragraph": None})


class GroupingTests(unittest.TestCase):
    """A canon is its paragraphs, and only its own."""

    PARAGRAPHS = (
        {"unit": "cic83-c-1095-1", "name": "can. 1095 §1", "mass": "cic83-lib-iv",
         "line": "johanno-pauline"},
        {"unit": "cic83-c-1095-2", "name": "can. 1095 §2", "mass": "cic83-lib-iv",
         "line": "johanno-pauline"},
        {"unit": "cic17-c-1095", "name": "can. 1095", "mass": "cic17-lib-iii",
         "line": "pio-benedictine"},
    )

    def test_the_paragraphs_of_one_canon_are_one_canon(self) -> None:
        found = ask(f"C.canons({rows(*self.PARAGRAPHS)})"
                    ".map((entry) => [entry.canon, entry.line, entry.rows.length])")
        self.assertIn(["1095", "johanno-pauline", 2], found)

    def test_two_codes_sharing_a_number_are_never_one_canon(self) -> None:
        found = ask(f"C.canons({rows(*self.PARAGRAPHS)}).length")
        self.assertEqual(found, 2)

    def test_a_lookup_is_exact_and_offers_no_neighbour(self) -> None:
        self.assertEqual(
            ask(f"C.find({rows(*self.PARAGRAPHS)}, {{canon: '1096', paragraph: null}}).length"),
            0,
        )

    def test_citing_a_paragraph_marks_it_and_drops_none_of_the_others(self) -> None:
        found = ask(f"C.find({rows(*self.PARAGRAPHS)}, {{canon: '1095', paragraph: '2'}})"
                    ".map((entry) => [entry.asked, entry.rows.length])")
        self.assertIn(["2", 2], found)


class VocabularyTests(unittest.TestCase):
    """The slice says what it is a history of; the page never assumes."""

    def test_a_law_slice_keeps_its_containers_under_its_own_key(self) -> None:
        self.assertEqual(
            ask("[C.readVocabulary({vocabulary: 'law', group_key: 'divisions',"
                " group_word: 'division', unit_word: 'canon'}).unit_word,"
                " C.groupsIn({divisions: [{division: 'cic83-lib-vi'}]}).length,"
                " C.groupOf({division: 'cic83-lib-vi'}),"
                " C.groupOf({mass: 'cic83-lib-vi'})]"),
            ["canon", 1, "cic83-lib-vi", "cic83-lib-vi"],
        )

    def test_a_slice_that_declares_nothing_is_read_as_the_missal_it_is(self) -> None:
        self.assertEqual(
            ask("[C.readVocabulary({}).unit_word, C.groupsIn({masses: [{mass: 'a'}]}).length]"),
            ["unit", 1],
        )


class SilenceTests(unittest.TestCase):
    """Three states, never two."""

    def test_words_withheld_and_words_never_read_are_different_states(self) -> None:
        self.assertEqual(
            ask("[C.bodyOf({text: 'Canon...'}).state,"
                " C.bodyOf({text: '', withheld: 'under copyright'}).state,"
                " C.bodyOf({text: ''}).state,"
                " C.bodyOf(null).state]"),
            ["present", "withheld", "unread", "unread"],
        )

    def test_the_establishing_act_survives_a_withholding(self) -> None:
        self.assertEqual(
            ask("C.bodyOf({text: '', withheld: 'x', established_at: 'mitis-iudex-2015'})"
                ".established"),
            "mitis-iudex-2015",
        )


class InterpretationTests(unittest.TestCase):
    """An interpretation settles a meaning and changes no word."""

    def test_an_interpretation_is_not_a_change(self) -> None:
        self.assertEqual(
            ask("[C.isInterpretation({state: 'interpreted'}),"
                " C.isInterpretation({state: 'changed'}),"
                " C.forceWords('declarative').indexOf('retroactive') !== -1,"
                " C.forceWords('restrictive').indexOf('not retroactive') !== -1]"),
            [True, False, True, True],
        )


class PageTests(unittest.TestCase):
    """The markup and the script have to agree about the page's controls."""

    def test_every_control_the_script_asks_for_is_in_the_markup(self) -> None:
        script = SCRIPT.read_text(encoding="utf-8")
        markup = MARKUP.read_text(encoding="utf-8")
        wanted = set(re.findall(r"getElementById\('([^']+)'\)", script))
        held = set(re.findall(r'\sid="([^"]+)"', markup))
        self.assertEqual(sorted(wanted - held), [])

    def test_the_page_makes_no_request_outside_the_data_root(self) -> None:
        for name in ("index.html", "law.js", "code-model.js", "law.css"):
            text = (PAGE / name).read_text(encoding="utf-8")
            self.assertNotIn("http://", text, name)
            self.assertNotIn("https://", text, name)

    def test_the_development_fixture_is_not_a_record_of_canon_law(self) -> None:
        # It is read by the page during development and must never be mistaken
        # for the slice the act-history lane writes, so it says what it is in
        # the one field the page prints whole.
        spine = json.loads((FIXTURE.parent / "code-of-canon-law.json").read_text("utf-8"))
        self.assertIn("DEVELOPMENT FIXTURE", spine["extent"])
        self.assertEqual(spine["vocabulary"], "law")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
