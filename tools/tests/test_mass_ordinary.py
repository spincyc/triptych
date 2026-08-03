#!/usr/bin/env python3
"""Regression checks for the Ordinary layer, and for the page that shows it.

The interesting failures here are not crashes. They are a prayer served under
the wrong name and a licensed text served without the condition that makes it
lawful, and neither would raise anything.

Two of the checks below exist because of specific, recorded near-misses. The
1861 Canon and the postconciliar Eucharistic Prayer I differ at eleven places,
among them both consecratory forms, so serving the one as the other would put a
wrong text at the most consequential locus in the rite; `test_prayer_one_is_not
_the_1861_canon` holds that boundary. And the ELLC common texts are free only on
a stated condition, so `test_a_licensed_text_carries_its_acknowledgement` holds
the acknowledgement beside the words rather than in a footer.

The browser half runs the real `day.js` and `ordinary-seating.js` under node
against the real generated files, for the reason `calendar-rubrics check` runs
`assembly-model.js` that way: a Python re-implementation would drift from the
page.
"""

import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "web" / "data" / "structure" / "ordinary"
PROPERS = ROOT / "src" / "web" / "data" / "structure" / "propers"
DAY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "day.js"
DAY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "day.html"
FORMULARY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "liturgy.js"
FORMULARY_HTML = ROOT / "src" / "web" / "browser" / "liturgy" / "index.html"
TOOL = ROOT / "tools" / "mass-ordinary"

PUBLISHABLE = {"public-domain", "project-created", "licensed-free"}
NEEDS_ACKNOWLEDGEMENT = {"licensed-free"}


def load(name: str) -> dict:
    return json.loads((DATA / (name + ".json")).read_text(encoding="utf-8"))


def elements(file: dict):
    for section in file["sections"]:
        for element in section["elements"]:
            yield element


class OrdinaryStructure(unittest.TestCase):
    """What the generated files must say, whatever the page does with them."""

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written; run `tools/tpt mass-ordinary structure`")
        self.files = {row: load(row) for row in ("roman-1962", "postconciliar")}

    def test_every_element_has_text_or_a_stated_reason(self) -> None:
        """The one thing this layer must never emit is a silent gap."""
        for name, file in self.files.items():
            for element in elements(file):
                if not element["translations"]:
                    self.assertTrue(
                        element["absent"]["english"],
                        f"{name}: {element['key']} has no English and names no reason",
                    )

    def test_no_witness_reaches_the_page_without_publishable_rights(self) -> None:
        for name, file in self.files.items():
            for witness in file["translations"]:
                self.assertIn(witness["rights"], PUBLISHABLE, name)
            for element in elements(file):
                for translation in element["translations"] or []:
                    self.assertIn(translation["rights"], PUBLISHABLE,
                                  f"{name}: {element['key']}")

    def test_a_licensed_text_carries_its_acknowledgement(self) -> None:
        """Free use granted on a condition is not free use without the condition."""
        for name, file in self.files.items():
            for witness in file["translations"]:
                if witness["rights"] in NEEDS_ACKNOWLEDGEMENT:
                    self.assertTrue(witness["acknowledgement"],
                                    f"{name}: {witness['source_id']} states no acknowledgement")

    def test_element_keys_are_unique_across_sections(self) -> None:
        """The 1861 book says `Gloria Patri` twice; the keys must still differ."""
        for name, file in self.files.items():
            keys = [element["key"] for element in elements(file)]
            self.assertEqual(len(keys), len(set(keys)), name)

    def test_only_the_postconciliar_missal_offers_a_choice_of_prayer(self) -> None:
        """The 1962 Missal has one Canon, so it must offer nothing to choose."""
        self.assertEqual(self.files["roman-1962"]["variants"], [])
        groups = self.files["postconciliar"]["variants"]
        self.assertEqual([one["group"] for one in groups], ["eucharistic-prayer"])
        options = groups[0]["options"]
        self.assertEqual([one["id"] for one in options if one["default"]], ["ep-i"],
                         "the default is the first prayer the Missal itself prints")

    def test_prayer_one_is_not_the_1861_canon(self) -> None:
        """The divergence that makes this the worst possible substitution.

        The postconciliar Prayer I must carry no text at all, and must say in
        terms that the Canon this site serves under the 1962 Missal is a
        different prayer. Reproducing the 1861 English here would be silent,
        plausible, and wrong at both consecratory forms.
        """
        found = [one for one in elements(self.files["postconciliar"])
                 if one["variant"] == "ep-i"]
        self.assertEqual(len(found), 1)
        prayer = found[0]
        self.assertIsNone(prayer["translations"], "Prayer I must carry no English")
        self.assertTrue(prayer["absent"]["english"])
        self.assertIn("NOT THE CANON OF THE 1962 MISSAL", (prayer["note"] or "").upper())

    def test_every_language_names_the_side_that_records_its_absence(self) -> None:
        """A language on offer must be able to say why it is empty.

        The page offers the reader every language declared here, including ones
        no word of which is held, because choosing an empty language is how the
        reason for the emptiness becomes visible. That only works if the join
        holds: each language names one side of `absent`, every element carries
        exactly those sides, and a language holding nothing carries a reason on
        every element rather than on most of them.
        """
        for name, file in self.files.items():
            langs = [one["lang"] for one in file["languages"]]
            self.assertEqual(len(langs), len(set(langs)), name)
            sides = {one["absent"] for one in file["languages"]}
            self.assertEqual(len(sides), len(langs), f"{name}: two languages share a side")
            for element in elements(file):
                self.assertEqual(set(element["absent"]), sides, f"{name}: {element['key']}")
            for one in file["languages"]:
                held = sum(1 for element in elements(file)
                           for translation in (element["translations"] or [])
                           if translation["lang"] == one["lang"])
                self.assertEqual(one["held"], held, f"{name}: {one['lang']} miscounted")
                for element in elements(file):
                    if any(row["lang"] == one["lang"]
                           for row in (element["translations"] or [])):
                        continue
                    self.assertTrue(
                        element["absent"][one["absent"]],
                        f"{name}: {element['key']} is silent in {one['lang']} "
                        "and names no reason",
                    )

    def test_the_index_names_every_calendar(self) -> None:
        listed = {row["calendar"] for row in load("index")["calendars"]}
        self.assertEqual(listed, set(self.files))


class OrdinarySlots(unittest.TestCase):
    """Where a proper of the day sits in the frame.

    These hold the declaration, not the page. A seat that resolves to nothing,
    a proper claimed by two seats, or seats that run backwards would each put a
    prayer somewhere plausible and wrong without anything failing.
    """

    def setUp(self) -> None:
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written; run `tools/tpt mass-ordinary structure`")
        self.files = {row: load(row) for row in ("roman-1962", "postconciliar")}

    def test_every_seat_names_an_element_the_frame_shows(self) -> None:
        for name, file in self.files.items():
            keys = {element["key"]: element for element in elements(file)}
            for slot in file["slots"]:
                self.assertIn(slot["anchor"], keys, f"{name}: seat {slot['key']}")
                self.assertIsNone(
                    keys[slot["anchor"]]["variant"],
                    f"{name}: seat {slot['key']} would vanish with a choice of prayer",
                )
                self.assertIn(slot["where"], ("before", "after"), f"{name}: {slot['key']}")

    def test_a_proper_has_one_seat(self) -> None:
        for name, file in self.files.items():
            claimed = [proper for slot in file["slots"] for proper in slot["propers"]]
            self.assertEqual(len(claimed), len(set(claimed)), name)

    def test_the_seats_run_forward_through_the_frame(self) -> None:
        """The file's order is the order of the rite, and is checked to be."""
        for name, file in self.files.items():
            order = {element["key"]: index for index, element in enumerate(elements(file))}
            reached = -1
            for slot in file["slots"]:
                at = order[slot["anchor"]] + (1 if slot["where"] == "after" else 0)
                self.assertGreaterEqual(at, reached, f"{name}: seat {slot['key']} runs backwards")
                reached = at

    def test_a_seat_says_which_rubric_puts_it_there(self) -> None:
        for name, file in self.files.items():
            if not file["slots"]:
                continue
            self.assertTrue(file["slots_derived_from"],
                            f"{name}: seats are declared and no book is named for them")
            for slot in file["slots"]:
                self.assertTrue(slot["locus"], f"{name}: seat {slot['key']} cites nothing")

    def test_the_seats_name_propers_the_corpus_actually_carries(self) -> None:
        """A seat for a proper name no mass uses is a seat that never fills.

        Not a rights or a truth question — a spelling one, and exactly the kind
        that resolves successfully and does nothing.
        """
        for name, file in self.files.items():
            path = PROPERS / (name + ".json")
            if not path.is_file():
                self.skipTest("no propers layer written")
            corpus = json.loads(path.read_text(encoding="utf-8"))
            used = {proper.get("name")
                    for mass in corpus.get("masses", [])
                    for proper in mass.get("propers", [])}
            for slot in file["slots"]:
                for proper in slot["propers"]:
                    self.assertIn(proper, used, f"{name}: seat {slot['key']} awaits {proper!r}")


class OrdinaryTool(unittest.TestCase):
    """The generator refuses what it must refuse."""

    def test_written_files_are_current(self) -> None:
        run = subprocess.run(
            ["python3", str(TOOL), "check", "--json"],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertEqual(json.loads(run.stdout)["stale"], [],
                         "regenerate with `tools/tpt mass-ordinary structure`")


class OrdinaryPage(unittest.TestCase):
    """The real day.js, over the real files, under node.

    A stub DOM rather than a browser: what is being held is the join and the
    filtering, which are the parts that can be wrong without failing.
    """

    def setUp(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not installed")
        if not DATA.is_dir():
            self.skipTest("no ordinary layer written")

    def test_the_page_loads_the_shared_seating_before_its_renderer(self) -> None:
        page = DAY_HTML.read_text(encoding="utf-8")
        self.assertLess(
            page.index('<script src="ordinary-seating.js"></script>'),
            page.index('<script src="day.js"></script>'),
        )

    def test_reading_first_hierarchy_and_event_sequence(self) -> None:
        """Utility disclosures follow the title; the Mass itself is unchanged."""
        page = DAY_HTML.read_text(encoding="utf-8")
        title = page.index('id="celebration-title"')
        settings = page.index('id="settings-disclosure"')
        notices = page.index('id="notices-disclosure"')
        mass = page.index('id="reading"')
        self.assertLess(title, settings)
        self.assertLess(settings, notices)
        self.assertLess(notices, mass)

        for position in (settings, notices):
            opening = page[page.rfind("<details", 0, position):page.index(">", position) + 1]
            self.assertNotIn(" open", opening)

        settings_end = page.index("</details>", settings)
        self.assertLess(settings, page.index('id="controls"'))
        self.assertLess(page.index('id="controls"'), settings_end)
        self.assertLess(page.index('id="formulary-controls"'), settings_end)

        report = self.run_harness()
        sequence = report["pentecost_10_sequence"]
        digest = hashlib.sha256(
            json.dumps(sequence, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        self.assertEqual(len(sequence), 211)
        self.assertEqual(
            digest,
            "c1fe93220057c722c753d3af29c9fb111c162a2572304780c018a6fed2591c08",
        )

    def test_the_page_shows_one_prayer_and_states_what_it_withholds(self) -> None:
        report = self.run_harness()
        self.assertEqual(report["shown_by_default"], ["ep-i"])
        self.assertEqual(report["shown_when_third_chosen"], ["ep-iii"])
        self.assertIn("Lord, have mercy.", report["kyrie"])
        self.assertIn("English Language Liturgical Consultation (ELLC), and used by permission",
                      report["kyrie"])
        self.assertIn("Not shown: its English.", report["prayer_one"])
        self.assertIn("Not shown: its Latin.", report["prayer_one"])
        self.assertIn("Te igitur, clementissime Pater", report["prayer_one"])
        self.assertIn("WE therefore, humbly pray", report["te_igitur_1861"])
        self.assertNotIn("used by permission", report["te_igitur_1861"])

    def test_the_propers_are_read_in_the_order_the_mass_is_said(self) -> None:
        """The whole point of the frame, over the real Easter Sunday formulary.

        Not a spot check of two placements: the full reading order, so that a
        seat moved to a plausible neighbour fails here rather than serving a
        Mass whose parts are all present and in the wrong order.
        """
        report = self.run_harness()
        self.assertEqual(report["easter_1962"], [
            "Introit",
            "praeparatio/kyrie-eleison",
            "praeparatio/gloria-in-excelsis",
            "Collect",
            "Epistle",
            "Gradual", "Alleluia", "Sequence",
            "Gospel",
            "oblatio/credo-in-unum-deum",
            "Offertory",
            "Secret",
            "praefatio/praefatio-communis",
            "praefatio/sanctus",
            "canon/te-igitur",
            "canon/forma-corporis",
            "canon/forma-sanguinis",
            "communio/pater-noster",
            "communio/agnus-dei",
            "Communion",
            "Postcommunion",
            "conclusio/dominus-vobiscum-ite-missa-est",
        ])
        self.assertEqual(
            report["event_kinds"], ["begin_section", "ordinary_element", "proper"]
        )

    def test_a_day_the_frame_does_not_fit_is_said_so_and_not_rearranged(self) -> None:
        """Christmas carries four Masses; one Ordinary cannot hold them.

        The failure this guards is the attractive one: pouring all four into the
        frame would put four Collects under one Collect and read as a Mass that
        was never said. What must happen instead is that the frame takes the
        first, the rest follow it whole, and the page says why.
        """
        report = self.run_harness()
        self.assertTrue(report["nativity_broke"])
        self.assertEqual(report["nativity_seated"], 10)
        self.assertEqual(report["nativity_after"], 31)
        self.assertEqual(report["nativity_total"], 41, "nothing is dropped")

    def test_a_withheld_element_still_holds_the_place_of_its_proper(self) -> None:
        """Absence does not forfeit a seat.

        The postconciliar Collect is withheld under ICEL's licence. The day's
        Collect is still set down immediately after it, so a reader sees both
        what is withheld and what is not, at the moment each falls due.
        """
        report = self.run_harness()
        self.assertEqual(report["postconciliar_collect"],
                         ["ritus-initiales/collecta", "Collect"])

    def test_a_language_nobody_holds_is_offered_and_says_why(self) -> None:
        """The control's whole purpose, and the failure it must not have.

        Neither missal's Latin is here, and both are still offered: a reader who
        asks for the Latin must be told at every element under which recorded
        reason it is silent, not handed a page that has quietly gone blank. The
        two reasons are different reasons and must not be interchangeable —
        `latin-not-transcribed` is work nobody has done and `editio-typica` is a
        rights question nobody has settled.
        """
        report = self.run_harness()
        self.assertEqual(
            [one["lang"] for one in report["languages"]["postconciliar"]], ["en", "la"])
        self.assertEqual(
            [one["held"] for one in report["languages"]["postconciliar"]], [9, 0])
        self.assertEqual([one["held"] for one in report["languages"]["roman-1962"]], [195, 0])

        pater = report["kyrie_in_each"]
        self.assertIn("Our Father in heaven", pater["en"])
        self.assertNotIn("Our Father in heaven", pater["la"])
        self.assertIn("Not shown: its Latin.", pater["la"])
        self.assertIn("editio-typica", pater["la"])

        canon = report["te_igitur_in_each"]
        self.assertIn("WE therefore, humbly pray", canon["en"])
        self.assertNotIn("WE therefore, humbly pray", canon["la"])
        self.assertIn("Not shown: its Latin.", canon["la"])
        self.assertIn("latin-not-transcribed", canon["la"])
        self.assertNotIn("editio-typica", canon["la"])

    def test_the_reason_is_stated_once_and_referred_to_after_that(self) -> None:
        """Two copies of a reason are two reasons waiting to disagree.

        Printed in full at every element it covers, the 1861 Latin reason ran to
        195 copies of the same 400 characters the moment a reader asked for the
        Latin. It is stated in the preamble, with how far it reaches, and the
        elements name it.
        """
        report = self.run_harness()
        preamble = report["preamble_1962"]
        self.assertIn("latin-not-transcribed", preamble)
        self.assertIn("195 of 195 elements", preamble)
        self.assertIn("transcribed the English column only", preamble)
        self.assertNotIn("transcribed the English column only",
                         report["te_igitur_in_each"]["la"])

    def test_the_speaker_is_named_and_a_name_is_not_a_mark(self) -> None:
        """Who is speaking, in words, and never a ℣ standing over a response.

        SUPERSEDES a ruling of this same test, 2026-08-01. It formerly held that
        the Ordinary set ℟ for the book's "R.". The maintainer's complaint was
        that the priest's and the server's parts could not be told apart and
        that the ℣/℟ letters were doing that job badly; the proposed fix, to set
        the book's "P." as ℣, would have introduced an error, and the evidence
        is in the book's own rows:

            priest   P. I confess to Almighty God, &c.
            server   R. May Almighty God be merciful to thee…
            server   R. I confess to Almighty God…
            priest   P. May Almighty God be merciful unto you…

        "P." marks the PRIEST and "R." marks a RESPONSE — two axes, printed in
        one column. In the fourth row the priest's line IS the response, so a ℣
        there would say "versicle" over a response. And in two rubric elements
        "P." is not a speaker mark at all but an abbreviation inside running
        text. So each is now set as the word it abbreviates.

        The marks are not merely dropped, which is the part that is easy to get
        wrong: 28 of the 39 marked elements hold a two-party dialogue inside ONE
        element, whose `speaker` field names the first line only. A leading mark
        is redundant with the speaker and goes; an INTERIOR mark is the only
        record that the speaker changed, and stays.

        Both halves of the original ruling that still hold are kept: the initial
        that is not a mark, and ℣/℟ outside the Ordinary, where `versicled` is
        untouched and the propers still use them.
        """
        report = self.run_harness()
        held = report["versicles_1861"]
        self.assertIn("Priest", held, "the speaker is named, not lettered")
        self.assertIn("Response", held)
        self.assertNotIn("R. And with thy spirit", held,
                         "the raw mark is never left in the reading face")
        self.assertNotIn("℣", held, "a versicle mark must never stand over a response")
        # The leading mark repeats the element's own speaker and is dropped;
        # what follows it is the words, not another tag.
        self.assertNotIn("Priest Priest", held)
        self.assertIn("B. V. M.", report["virgin_1861"])
        self.assertNotIn("℣", report["virgin_1861"])

    def run_harness(self) -> dict:
        run = subprocess.run(
            ["node", "-e", HARNESS],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        return json.loads(run.stdout)


class FormularyPage(unittest.TestCase):
    """The direct-formulary entrance shares the reading-first page hierarchy."""

    def test_title_first_hierarchy_and_closed_utility_disclosures(self) -> None:
        page = FORMULARY_HTML.read_text(encoding="utf-8")
        title = page.index('id="formulary-title"')
        settings = page.index('id="settings-disclosure"')
        notices = page.index('id="notices-disclosure"')
        proper = page.index('id="reading"')
        self.assertLess(title, settings)
        self.assertLess(settings, notices)
        self.assertLess(notices, proper)

        for position in (settings, notices):
            opening = page[page.rfind("<details", 0, position):page.index(">", position) + 1]
            self.assertNotIn(" open", opening)

        settings_end = page.index("</details>", settings)
        notices_end = page.index("</details>", notices)
        self.assertLess(settings, page.index('id="controls"'))
        self.assertLess(page.index('id="controls"'), settings_end)
        self.assertLess(notices, page.index('id="banner"'))
        self.assertLess(page.index('id="banner"'), notices_end)
        self.assertLess(
            page.index('<link rel="stylesheet" href="liturgy.css">'),
            page.index('<link rel="stylesheet" href="day-missal.css">'),
        )

        source = FORMULARY_JS.read_text(encoding="utf-8")
        self.assertIn("noticesDisclosure.hidden = !shown", source)
        self.assertNotIn("noticesDisclosure.open = true", source)

    def test_renderer_keeps_each_missals_propers_in_source_order(self) -> None:
        expected = {
            "roman-1962": (
                "advent-1",
                10,
                "9b8a7c8c853d9363ebeb2c5aa9c19292f3af0dc3e240c209c49a892c06941ee6",
            ),
            "postconciliar": (
                "ot-18",
                11,
                "3747fa005cf696dca44389aae29904967e4960187a866ac72928b8963846b4fd",
            ),
        }
        for missal, (key, count, wanted_digest) in expected.items():
            file = json.loads((PROPERS / f"{missal}.json").read_text(encoding="utf-8"))
            mass = next(one for one in file["masses"] if one["key"] == key)
            names = [proper["name"] for proper in mass["propers"]]
            digest = hashlib.sha256(
                json.dumps(names, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            ).hexdigest()
            self.assertEqual(len(names), count, missal)
            self.assertEqual(digest, wanted_digest, missal)

        source = FORMULARY_JS.read_text(encoding="utf-8")
        traversal = source.index("for (const proper of propers)")
        self.assertLess(source.index("formularyTitle.textContent"), traversal)
        self.assertLess(source.index("formularyMeta.textContent"), traversal)
        self.assertIn("reading.appendChild(T.renderProper(proper", source[traversal:])

    def test_day_reading_missal_source_and_event_contract_remain_fixed(self) -> None:
        self.assertEqual(
            hashlib.sha256(DAY_HTML.read_bytes()).hexdigest(),
            "a6b8b827c7e91cb8817e44686baff355b11bd99f12ecf83c5513e375d5605edb",
        )
        self.assertEqual(
            hashlib.sha256(DAY_JS.read_bytes()).hexdigest(),
            "0804a64c85c6fca9226468766c0d012d918875ec71c2cd902bf333bc60387263",
        )
        page = DAY_HTML.read_text(encoding="utf-8")
        self.assertNotIn("annotation-control", page)
        self.assertNotIn("Annotation placeholder.", page)


# A DOM small enough to write here and faithful enough to prove the join.
#
# The shared machinery is the REAL browser-core.js and not a second stub of it.
# What is being held is the join, the filtering and the setting, and every one
# of those runs partly in code both pages share: a stub of `notice` or of
# `versicled` would pass while the page they actually load did something else.
# Only the things that reach the network or the URL are replaced.
HARNESS = r"""
const fs = require('fs');
function node(tag) {
  return { tagName: tag, className: '', textContent: '', lang: null, hidden: false,
    children: [], attrs: {}, style: {},
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelectorAll() { return []; }, addEventListener() {},
    text() { let o = this.textContent || '';
      for (const c of this.children) o += (c.text ? c.text() : String(c.data || '')); return o; } };
}
const ids = {};
global.document = { createElement: node, createTextNode: (t) => ({ data: t, text: () => t }),
  createDocumentFragment: () => node('#fragment'),
  getElementById: (id) => (ids[id] = ids[id] || node('div')),
  body: { classList: { toggle() {} }, appendChild() {} }, addEventListener() {} };
global.window = { location: { search: '' }, addEventListener() {},
  MassAssembly: { derive: () => ({}) }, matchMedia: null };
global.window.OrdinarySeating = require(
  './src/web/browser/liturgy/ordinary-seating.js');

eval(fs.readFileSync('src/web/browser/shared/browser-core.js', 'utf8'));
global.window.Triptych = Object.assign({}, global.window.Triptych, {
  fillSelect(s, i) { s.filled = i; }, loadJSON: async () => ({}),
  readHash: () => new Map(), writeHash() {}, onHashChange() {}, onArrowStep() {},
  loadBibles: async () => ({ ok: false, message: 'stub' }), fillBibleSelect() {},
  setInlineNotice() {}, fail() {}, statusLine() {} });

let src = fs.readFileSync('src/web/browser/liturgy/day.js', 'utf8');
src = src.replace('  start();',
  '  global.__probe = { renderElement, elementShows, state, ordinaryPreamble, ' +
  'seats, seatPropers, shownElements, massEvents };');
eval(src);
const P = global.__probe;
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));
const pc = read('src/web/data/structure/ordinary/postconciliar.json');
const tlm = read('src/web/data/structure/ordinary/roman-1962.json');
const all = (f) => f.sections.flatMap((s) => s.elements);
const eps = all(pc).filter((e) => e.variant);
const shown = () => eps.filter((e) => P.elementShows(e, pc)).map((e) => e.variant);
const byDefault = shown();
P.state.variants['eucharistic-prayer'] = 'ep-iii';
const whenThird = shown();
P.state.variants = {};

/* The frame with a real formulary poured into it, as one flat sequence: a
   proper by its name, an element by its key. This is what the page renders, in
   the order it renders it. */
function pour(file, calendar, key) {
  const mass = read('src/web/data/structure/propers/' + calendar + '.json')
    .masses.find((m) => m.key === key);
  const frame = P.shownElements(file);
  const placed = P.seatPropers(mass.propers || [], P.seats(file, frame));
  const events = P.massEvents(frame, placed);
  const out = [];
  for (const event of events) {
    if (event.kind === 'proper') out.push(event.proper.name);
    if (event.kind === 'ordinary_element') out.push(event.element.key);
  }
  const count = (placement) => events.filter(
    (event) => event.kind === 'proper' && event.placement === placement).length;
  const sequence = events.map((event) => {
    if (event.kind === 'begin_section') {
      return 'begin_section:' + event.section.key;
    }
    if (event.kind === 'ordinary_element') {
      return 'ordinary_element:' + event.element.key;
    }
    return 'proper:' + event.placement + ':' + event.proper.name;
  });
  return { order: out, broke: placed.broke, seated: count('seated'),
    before: count('before'), after: count('after'),
    kinds: Array.from(new Set(events.map((event) => event.kind))).sort(),
    sequence: sequence };
}

// Landmarks of the frame, one per position the reading order names. Anything
// not a landmark and not a proper is dropped, so the assertion is about order.
const MARKS = new Set(['praeparatio/kyrie-eleison', 'praeparatio/gloria-in-excelsis',
  'oblatio/credo-in-unum-deum', 'praefatio/praefatio-communis', 'praefatio/sanctus',
  'canon/te-igitur', 'canon/forma-corporis', 'canon/forma-sanguinis',
  'communio/pater-noster', 'communio/agnus-dei',
  'conclusio/dominus-vobiscum-ite-missa-est']);
const easter = pour(tlm, 'roman-1962', 'easter-sunday');
const pentecost10 = pour(tlm, 'roman-1962', 'pentecost-10');
const nativity = pour(pc, 'postconciliar', 'nativity');
const collect = pour(pc, 'postconciliar', 'easter-sunday').order;
const seat = collect.indexOf('ritus-initiales/collecta');

/* The same element read in each language the file declares, which is what the
   language control offers. Nothing is re-derived here: the languages come from
   the file, and the page is asked for each of them in turn. */
function inEach(file, key) {
  const element = all(file).find((e) => e.key === key);
  const out = {};
  for (const one of file.languages) {
    P.state.ordinaryLang = one.lang;
    out[one.lang] = P.renderElement(element, file).text();
  }
  P.state.ordinaryLang = null;
  return out;
}

process.stdout.write(JSON.stringify({
  shown_by_default: byDefault,
  shown_when_third_chosen: whenThird,
  languages: { postconciliar: pc.languages, 'roman-1962': tlm.languages },
  kyrie_in_each: inEach(pc, 'ritus-communionis/pater-noster'),
  te_igitur_in_each: inEach(tlm, 'canon/te-igitur'),
  preamble_1962: P.ordinaryPreamble(tlm).text(),
  versicles_1861: P.renderElement(
    all(tlm).find((e) => e.key === 'praeparatio/dominus-vobiscum'), tlm).text(),
  virgin_1861: P.renderElement(
    all(tlm).find((e) => e.key === 'oblatio/rubrica-collecta-concede'), tlm).text(),
  kyrie: P.renderElement(all(pc).find((e) => e.key.endsWith('/kyrie')), pc).text(),
  prayer_one: P.renderElement(eps.find((e) => e.variant === 'ep-i'), pc).text(),
  te_igitur_1861: P.renderElement(all(tlm).find((e) => e.key === 'canon/te-igitur'), tlm).text(),
  easter_1962: easter.order.filter((one) => MARKS.has(one) || one.indexOf('/') < 0),
  nativity_broke: nativity.broke,
  nativity_seated: nativity.seated,
  nativity_after: nativity.after,
  nativity_total: nativity.seated + nativity.before + nativity.after,
  postconciliar_collect: collect.slice(seat, seat + 2),
  event_kinds: easter.kinds,
  pentecost_10_sequence: pentecost10.sequence
}));
"""


if __name__ == "__main__":
    unittest.main()
