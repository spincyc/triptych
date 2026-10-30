"""Applicability resolves disjoint Ordinary witnesses before a coequal choice."""
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
HARNESS = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = process.argv[1];
const A = require(path.join(root, 'src/web/browser/liturgy/reader-state-adapters.js'));
const C = require(path.join(root, 'src/web/browser/liturgy/reader-state.js'));
const calendar = 'roman-1962';
const march = 's-ioseph-sponsi-beatae-mariae-virginis';
const may = 's-ioseph-opificis-sponsi-beatae-mariae';
const context = formulary => ({calendar, formulary});
const scope = formulary => ({kind: 'formulary', calendar, formularies: [formulary],
  basis: 'Synthetic source-owned exact formulary scope.'});
const historical = {lang: 'en', source_id: 'edition.synthetic.march', rights: 'public-domain',
  text: 'Synthetic historical March wording.', relation: 'antecedent', collation: 'uncollated',
  applicability: scope(march), reading_note: 'Historical English, only for the named March formulary.'};
const study = {lang: 'en', source_id: 'edition.synthetic.may', rights: 'project-created',
  text: 'Synthetic study May wording.', relation: 'own', applicability: scope(may),
  reading_note: 'Project study English, only for the named May formulary; not approved.'};
const file = {calendar, languages: [
  {lang: 'en', held: 1, elements: 1, absent: 'english'},
  {lang: 'la', held: 1, elements: 1, absent: 'latin'}
], translations: [
  {source_id: historical.source_id, lang: 'en', label: 'Synthetic March historical witness'},
  {source_id: study.source_id, lang: 'en', label: 'Synthetic May study witness'}
], absences: []};
const element = rows => ({key: 'praefatio/synthetic-joseph', kind: 'prayer',
  name: 'Synthetic Joseph preface', translations: rows,
  absent: {english: null, latin: null}});
function select(rows, useContext, witness = null) {
  const result = A.selectOrdinaryTranslation(element(rows), file, 'en', witness, useContext);
  assert.deepEqual(C.validateSelectedMaterial(result), []);
  return result;
}
function reversed(rows) { return [rows, rows.slice().reverse()]; }
function unavailable(result, state) {
  assert.equal(result.availability, 'unavailable');
  assert.equal(result.reason, 'applicability-' + state);
  assert.equal(result.unavailableState, state === 'unresolved' ? 'unresolved' : 'unavailable');
  assert.equal(result.applicability.state, state);
  assert.equal(result.text, null);
  assert.equal(result.sourceId, null);
  assert.equal(result.rights, null);
}
"""


class OrdinaryScopedWitnessSelection(unittest.TestCase):
    def run_case(self, source):
        result = subprocess.run(
            ["/usr/bin/node", "-e", HARNESS + source, str(ROOT)],
            text=True, capture_output=True, check=False, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unique_applicable_witness_is_order_independent(self):
        self.run_case(r"""
for (const rows of reversed([historical, study])) {
  for (const [formulary, expected] of [[march, historical], [may, study]]) {
    const result = select(rows, context(formulary));
    assert.equal(result.availability, 'held');
    assert.equal(result.sourceId, expected.source_id);
    assert.equal(result.text, expected.text);
    assert.equal(result.rights, expected.rights);
    assert.deepEqual(result.applicability, {state: 'applicable', scope: expected.applicability,
      context: context(formulary)});
  }
}
""")

    def test_unknown_and_outside_contexts_have_distinct_text_free_diagnostics(self):
        self.run_case(r"""
for (const useContext of [undefined, null, {}, {calendar}, {...context(march), extra: true}]) {
  const results = reversed([historical, study]).map(rows => select(rows, useContext));
  results.forEach(result => unavailable(result, 'unresolved'));
  assert.deepEqual(results[0], results[1]);
  assert.equal(results[0].applicability.context, null);
  assert.equal(JSON.stringify(results[0]).includes(historical.text), false);
  assert.equal(JSON.stringify(results[0]).includes(study.text), false);
}
for (const useContext of [context('outside-both'), {calendar: 'roman-pre-1955', formulary: march}]) {
  const results = reversed([historical, study]).map(rows => select(rows, useContext));
  results.forEach(result => unavailable(result, 'inapplicable'));
  assert.deepEqual(results[0], results[1]);
  assert.deepEqual(results[0].applicability.context, useContext);
}
""")

    def test_unknown_scoped_competitor_blocks_an_unscoped_default(self):
        self.run_case(r"""
const unscoped = {...study};
delete unscoped.applicability;
for (const rows of reversed([historical, unscoped])) {
  unavailable(select(rows, undefined), 'unresolved');
  const outsideMarch = select(rows, context(may));
  assert.equal(outsideMarch.sourceId, unscoped.source_id);
  assert.equal(outsideMarch.text, unscoped.text);
  const coequal = select(rows, context(march));
  assert.equal(coequal.availability, 'choice-required');
  assert.equal(coequal.text, null);
  assert.deepEqual(coequal.unresolvedWitnesses, [historical.source_id, unscoped.source_id].sort());
}
""")

    def test_overlapping_applicable_witnesses_require_an_explicit_choice(self):
        self.run_case(r"""
const overlap = {...study, applicability: scope(march)};
const outside = {...study, source_id: 'edition.synthetic.outside', applicability: scope('outside')};
for (const rows of reversed([historical, overlap, outside])) {
  const result = select(rows, context(march));
  assert.equal(result.availability, 'choice-required');
  assert.equal(result.sourceId, null);
  assert.equal(result.text, null);
  assert.deepEqual(result.unresolvedWitnesses, [historical.source_id, overlap.source_id].sort());
  assert.equal(select(rows, context(march), historical.source_id).text, historical.text);
  assert.equal(select(rows, context(march), overlap.source_id).text, overlap.text);
}
""")

    def test_explicit_inapplicable_or_unknown_witness_never_falls_back(self):
        self.run_case(r"""
for (const rows of reversed([historical, study])) {
  unavailable(select(rows, context(march), study.source_id), 'inapplicable');
  unavailable(select(rows, context(may), historical.source_id), 'inapplicable');
  unavailable(select(rows, undefined, study.source_id), 'unresolved');
  assert.equal(select(rows, context(may), study.source_id).text, study.text);
  assert.throws(() => select(rows, context(may), 'edition.synthetic.missing'), /explicit Ordinary witness/);
}
const unscoped = {...study};
delete unscoped.applicability;
assert.equal(select([historical, unscoped], undefined, unscoped.source_id).text, unscoped.text);
""")

    def test_existing_unscoped_and_single_scoped_contracts_are_preserved(self):
        self.run_case(r"""
const unscoped = {...historical};
delete unscoped.applicability;
const second = {...study};
delete second.applicability;
const original = JSON.stringify([unscoped, second]);
assert.equal(select([unscoped], undefined).text, unscoped.text);
for (const rows of reversed([unscoped, second])) {
  const result = select(rows, undefined);
  assert.equal(result.availability, 'choice-required');
  assert.deepEqual(result.unresolvedWitnesses, [unscoped.source_id, second.source_id].sort());
}
assert.equal(JSON.stringify([unscoped, second]), original);
const single = select([historical], undefined);
unavailable(single, 'unresolved');
assert.deepEqual(single.applicability, {state: 'unresolved', scope: historical.applicability, context: null});
const absent = select([], undefined);
assert.equal(absent.availability, 'unavailable');
assert.equal(absent.absenceKey, 'language-not-held');
assert.equal(absent.reason, 'unavailable');
""")

    def test_malformed_scope_is_not_hidden_by_witness_order_or_selection(self):
        self.run_case(r"""
for (const applicability of [null, {}, [], {...scope(may), extra: true},
  {...scope(may), basis: ''}, {...scope(may), formularies: []}]) {
  const malformed = {...study, applicability};
  for (const rows of reversed([historical, malformed])) {
    assert.throws(() => select(rows, context(march)), /malformed Ordinary translation applicability/);
    assert.throws(() => select(rows, context(march), historical.source_id), /malformed Ordinary translation applicability/);
  }
}
""")

    def test_selected_paired_and_lectern_render_only_the_applicable_body_and_note(self):
        self.run_case(r"""
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
Object.assign(globalThis, {document: dom.document, window: globalThis,
  location: {search: '', hash: '', pathname: '/'},
  history: {replaceState() {}, pushState() {}}, addEventListener() {}});
vm.runInThisContext(fs.readFileSync(path.join(root, 'src/web/browser/shared/browser-core.js'), 'utf8'));
globalThis.OrdinarySeating = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
globalThis.LiturgyReaderStateAdapters = A;
vm.runInThisContext(fs.readFileSync(path.join(root, 'src/web/browser/liturgy/day.js'), 'utf8'));
const latin = {lang: 'la', source_id: 'edition.synthetic.latin', rights: 'public-domain', text: 'Verba Latina.'};
for (const rows of reversed([historical, study])) {
  for (const display of ['selected', 'latin-and-selected']) {
    TriptychOrdinaryRenderer.configure({ordinaryLang: 'en', textDisplay: display, why: false});
    for (const [formulary, expected, other] of [[march, historical, study], [may, study, historical]]) {
      const node = TriptychOrdinaryRenderer.renderElement(element([...rows, latin]), file, undefined, context(formulary));
      assert.ok(node.textContent.includes(expected.text));
      assert.equal(node.textContent.includes(other.text), false);
      assert.equal(node.querySelectorAll('.ordinary-reading-note').length, 1);
      assert.equal(node.querySelector('.ordinary-reading-note').textContent, expected.reading_note);
      assert.equal(node.textContent.includes(other.reading_note), false);
      const shown = dom.read(node).map(block => block.runs.map(run => run.text).join('')).join('\n');
      assert.ok(shown.includes(expected.reading_note));
      assert.equal(shown.includes(other.reading_note), false);
    }
    for (const useContext of [undefined, context('outside-both')]) {
      const node = TriptychOrdinaryRenderer.renderElement(element([...rows, latin]), file, undefined, useContext);
      assert.equal(node.textContent.includes(historical.text), false);
      assert.equal(node.textContent.includes(study.text), false);
      assert.equal(node.querySelectorAll('.ordinary-reading-note').length, 0);
    }
  }
}
""")

    def test_current_joseph_preface_selects_exact_source_in_both_readers(self):
        self.run_case(r"""
const parsed = JSON.parse(fs.readFileSync(process.env.TRIPTYCH_ORDINARY_DATA ||
  path.join(root, 'src/web/data/structure/ordinary/roman-1962.json'), 'utf8'));
const ordinary = parsed.ordinary ? parsed.ordinary[0] : parsed;
const preface = ordinary.sections.flatMap(section => section.elements || [])
  .find(row => row.key === 'praefatio/praefatio-sancto-ioseph');
assert.ok(preface);
const english = preface.translations.filter(row => row.lang === 'en');
assert.equal(english.length, 2);
const marchSource = english.find(row => row.source_id ===
  'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945');
const maySource = english.find(row => row.source_id ===
  'edition.triptych.english-completion-20261029-ordinary-joseph-preface-may1.study-english-20261030');
assert.ok(marchSource && maySource);
assert.equal(marchSource.rights, 'public-domain');
assert.equal(maySource.rights, 'project-created');
assert.deepEqual(marchSource.applicability.formularies, [march]);
assert.deepEqual(maySource.applicability.formularies, [may]);
const structure = JSON.parse(fs.readFileSync(path.join(root,
  'src/web/data/structure/propers/roman-1962.json'), 'utf8'));
function adapt(formulary, frame = ordinary) {
  const request = {schema: 'triptych-liturgy-reader-state/v1', entrance: 'propers', civilDate: null,
    edition: {id: calendar}, formulary: {id: formulary},
    bible: {id: 'douay-rheims', numbering: 'vulgate'},
    languages: {orations: 'la', ordinary: 'en'}, requestedMode: 'missal',
    options: {ordinary: true, legitimate: {}}, coverage: [], unresolvedChoices: [], sourceHooks: []};
  return A.adaptPropers({request, ordinary: frame, structure});
}
for (const [formulary, expected] of [[march, marchSource], [may, maySource]]) {
  const adapted = adapt(formulary);
  const event = adapted.events.find(row => row.id === 'ordinary-element/praefatio/praefatio-sancto-ioseph');
  assert.ok(event);
  assert.equal(event.selected.text, expected.text);
  assert.equal(event.selected.sourceId, expected.source_id);
}
const wrongRelations = structuredClone(ordinary);
wrongRelations.relation_coverage.find(row => row.lang === 'en').count += 1;
assert.throws(() => adapt(may, wrongRelations), /Ordinary relation grades contradict source offers/);
const wrongHeld = structuredClone(ordinary);
wrongHeld.language_coverage.find(row => row.lang === 'en').held -= 1;
wrongHeld.language_coverage.find(row => row.lang === 'en').missing += 1;
wrongHeld.language_coverage.find(row => row.lang === 'en').absent += 1;
assert.throws(() => adapt(may, wrongHeld), /Ordinary held elements contradict language coverage/);
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
Object.assign(globalThis, {document: dom.document, window: globalThis,
  location: {search: '', hash: '', pathname: '/'},
  history: {replaceState() {}, pushState() {}}, addEventListener() {}});
vm.runInThisContext(fs.readFileSync(path.join(root, 'src/web/browser/shared/browser-core.js'), 'utf8'));
globalThis.OrdinarySeating = require(path.join(root, 'src/web/browser/liturgy/ordinary-seating.js'));
globalThis.LiturgyReaderStateAdapters = A;
vm.runInThisContext(fs.readFileSync(path.join(root, 'src/web/browser/liturgy/day.js'), 'utf8'));
const clean = text => String(text).replace(/\s+/g, ' ').trim();
for (const translations of reversed(preface.translations)) {
  const row = {...preface, translations};
  for (const [formulary, expected, other] of [[march, marchSource, maySource], [may, maySource, marchSource]]) {
    const useContext = context(formulary);
    const selected = A.selectOrdinaryTranslation(row, ordinary, 'en', null, useContext);
    assert.deepEqual(C.validateSelectedMaterial(selected), []);
    assert.equal(selected.text, expected.text);
    assert.equal(selected.sourceId, expected.source_id);
    unavailable(A.selectOrdinaryTranslation(row, ordinary, 'en', other.source_id, useContext), 'inapplicable');
    for (const textDisplay of ['selected', 'latin-and-selected']) {
      TriptychOrdinaryRenderer.configure({ordinaryLang: 'en', textDisplay, why: false});
      const node = TriptychOrdinaryRenderer.renderElement(row, ordinary, undefined, useContext);
      assert.ok(clean(node.textContent).includes(clean(expected.text)));
      assert.equal(clean(node.textContent).includes(clean(other.text)), false);
      assert.equal(node.querySelectorAll('.ordinary-reading-note').length, 1);
      assert.equal(node.querySelector('.ordinary-reading-note').textContent, expected.reading_note);
      assert.equal(node.textContent.includes(other.reading_note), false);
      const terminal = dom.read(node).map(block => block.runs.map(run => run.text).join('')).join('\n');
      assert.ok(clean(terminal).includes(clean(expected.text)));
      assert.ok(terminal.includes(expected.reading_note));
      assert.equal(terminal.includes(other.reading_note), false);
    }
  }
  for (const useContext of [undefined, context('outside-both')]) {
    const selected = A.selectOrdinaryTranslation(row, ordinary, 'en', null, useContext);
    unavailable(selected, useContext ? 'inapplicable' : 'unresolved');
    for (const textDisplay of ['selected', 'latin-and-selected']) {
      TriptychOrdinaryRenderer.configure({ordinaryLang: 'en', textDisplay, why: false});
      const node = TriptychOrdinaryRenderer.renderElement(row, ordinary, undefined, useContext);
      for (const source of english) {
        assert.equal(clean(node.textContent).includes(clean(source.text)), false);
        assert.equal(node.textContent.includes(source.reading_note), false);
      }
    }
  }
}
""")


if __name__ == "__main__":
    unittest.main()
