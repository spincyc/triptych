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

The browser half runs the real `day.js` under node against the real generated
files, for the reason `calendar-rubrics check` runs `assembly-model.js` that
way: a Python re-implementation of the page would drift from the page.
"""

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "src" / "web" / "data" / "structure" / "ordinary"
DAY_JS = ROOT / "src" / "web" / "browser" / "liturgy" / "day.js"
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

    def test_the_index_names_every_calendar(self) -> None:
        listed = {row["calendar"] for row in load("index")["calendars"]}
        self.assertEqual(listed, set(self.files))


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

    def test_the_page_shows_one_prayer_and_states_what_it_withholds(self) -> None:
        run = subprocess.run(
            ["node", "-e", HARNESS],
            capture_output=True, text=True, cwd=ROOT, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        report = json.loads(run.stdout)
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


# A DOM small enough to write here and faithful enough to prove the join.
HARNESS = r"""
const fs = require('fs');
function node(tag) {
  return { tagName: tag, className: '', textContent: '', lang: null, hidden: false,
    children: [], attrs: {},
    appendChild(c) { this.children.push(c); return c; },
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelectorAll() { return []; }, addEventListener() {},
    text() { let o = this.textContent || '';
      for (const c of this.children) o += (c.text ? c.text() : String(c.data || '')); return o; } };
}
const ids = {};
global.document = { createElement: node, createTextNode: (t) => ({ data: t, text: () => t }),
  getElementById: (id) => (ids[id] = ids[id] || node('div')),
  body: { classList: { toggle() {} } }, addEventListener() {} };
global.window = {
  Triptych: {
    el(t, c, x) { const n = node(t); n.className = c || ''; n.textContent = x || ''; return n; },
    notice(x) { const n = node('p'); n.textContent = 'Not shown: ' + x; return n; },
    fillSelect(s, i) { s.filled = i; }, loadJSON: async () => ({}),
    readHash: () => new Map(), writeHash() {}, onHashChange() {}, onArrowStep() {},
    loadBibles: async () => ({ ok: false, message: 'stub' }), fillBibleSelect() {},
    setInlineNotice() {}, fail() {}, SOURCE_LANGUAGE: 'la', dataRoot: '',
    dataPath: (p) => p, titleCase: (s) => s },
  MassAssembly: { derive: () => ({}) }, matchMedia: null, addEventListener() {} };

let src = fs.readFileSync('src/web/browser/liturgy/day.js', 'utf8');
src = src.replace('  start();',
  '  global.__probe = { renderElement, elementShows, state };');
eval(src);
const P = global.__probe;
const pc = JSON.parse(fs.readFileSync('src/web/data/structure/ordinary/postconciliar.json', 'utf8'));
const tlm = JSON.parse(fs.readFileSync('src/web/data/structure/ordinary/roman-1962.json', 'utf8'));
const all = (f) => f.sections.flatMap((s) => s.elements);
const eps = all(pc).filter((e) => e.variant);
const shown = () => eps.filter((e) => P.elementShows(e, pc)).map((e) => e.variant);
const byDefault = shown();
P.state.variants['eucharistic-prayer'] = 'ep-iii';
const whenThird = shown();
P.state.variants = {};
process.stdout.write(JSON.stringify({
  shown_by_default: byDefault,
  shown_when_third_chosen: whenThird,
  kyrie: P.renderElement(all(pc).find((e) => e.key.endsWith('/kyrie')), pc).text(),
  prayer_one: P.renderElement(eps.find((e) => e.variant === 'ep-i'), pc).text(),
  te_igitur_1861: P.renderElement(all(tlm).find((e) => e.key === 'canon/te-igitur'), tlm).text()
}));
"""


if __name__ == "__main__":
    unittest.main()
