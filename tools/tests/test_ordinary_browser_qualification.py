"""A source-owned reading qualification stays beside its Ordinary words."""
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
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
globalThis.window = globalThis;
globalThis.document = dom.document;
globalThis.location = {search: '', hash: '', pathname: '/'};
globalThis.history = {replaceState() {}, pushState() {}};
globalThis.addEventListener = () => {};
for (const file of ['shared/browser-core.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(root, 'src/web/browser', file), 'utf8'));
}
globalThis.OrdinarySeating = require(path.join(root,
  'src/web/browser/liturgy/ordinary-seating.js'));
globalThis.LiturgyReaderStateAdapters = require(path.join(root,
  'src/web/browser/liturgy/reader-state-adapters.js'));
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/liturgy/day.js'), 'utf8'));
const sourceId = 'edition.synthetic.bilingual';
const english = {
  lang: 'en', source_id: sourceId, rights: 'public-domain',
  relation: 'antecedent', collation: 'uncollated',
  text: 'P. Historical source words.\nR. Source answer.',
  turns: [
    {text: 'P. Historical source words.', speaker: 'priest', printed_marker: 'P.'},
    {text: 'R. Source answer.', speaker: 'server', printed_marker: 'R.'}
  ],
  reading_note: 'Historical English; not the approved English of this Missal. The older response is retained.',
  note: 'Full source research: exact printed page, edition and uncollated difference.'
};
const latin = {lang: 'la', source_id: sourceId, rights: 'public-domain',
  relation: 'antecedent', collation: 'uncollated', text: 'Verba fontis.'};
const element = {key: 'synthetic/dialogue', kind: 'dialogue', name: 'Synthetic dialogue',
  translations: [english, latin], absent: {english: null, latin: null},
  note: 'Element research belongs to Study.'};
const file = {calendar: 'synthetic', languages: [
  {lang: 'en', held: 1, elements: 1, absent: 'english'},
  {lang: 'la', held: 1, elements: 1, absent: 'latin'}
], translations: [
  {source_id: sourceId, lang: 'en', label: 'Synthetic historical English witness'},
  {source_id: sourceId, lang: 'la', label: 'Synthetic Latin witness'}
], absences: []};
const renderer = TriptychOrdinaryRenderer;
function render(textDisplay = 'selected', why = false, row = element, context) {
  renderer.configure({ordinaryLang: 'en', textDisplay, why});
  return renderer.renderElement(row, file, undefined, context);
}
function bodies(node) {
  return node.querySelectorAll('.ordinary-dialogue').map(one => one.textContent);
}
"""


class OrdinaryBrowserQualification(unittest.TestCase):
    def run_case(self, source):
        result = subprocess.run(
            ["/usr/bin/node", "-e", HARNESS + source, str(ROOT)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_default_note_is_visible_separate_and_preserves_the_prayer(self):
        self.run_case(r"""
const node = render();
const note = node.querySelector('.ordinary-reading-note');
assert.equal(note.textContent, english.reading_note);
assert.equal(note.lang, 'en');
assert.equal(note.parentNode, node);
assert.equal(note.hasAttribute('hidden'), false);
assert.equal(node.querySelectorAll('details').length, 0);
assert.ok(node.childNodes.indexOf(note) < node.childNodes.indexOf(node.querySelector('.ordinary-dialogue')));
assert.equal(node.querySelector('.ordinary-reading-source').textContent,
  'Source: Synthetic historical English witness');
assert.equal(node.textContent.includes(english.note), false);
assert.equal(node.textContent.includes(element.note), false);
const unqualified = structuredClone(element);
delete unqualified.translations[0].reading_note;
assert.deepEqual(bodies(node), bodies(render('selected', false, unqualified)));
assert.equal(node.querySelector('.ordinary-dialogue').textContent.includes(english.reading_note), false);
""")

    def test_paired_notes_and_language_specific_source_labels_appear_once(self):
        self.run_case(r"""
const node = render('latin-and-selected');
const sides = node.querySelectorAll('.text-side');
assert.equal(sides.length, 2);
const en = sides.find(one => one.getAttribute('data-text-language') === 'en');
const la = sides.find(one => one.getAttribute('data-text-language') === 'la');
assert.equal(en.querySelectorAll('.ordinary-reading-note').length, 1);
assert.equal(la.querySelectorAll('.ordinary-reading-note').length, 0);
assert.equal(en.textContent.split('Source: Synthetic historical English witness').length - 1, 1);
assert.equal(la.textContent.split('Source: Synthetic Latin witness').length - 1, 1);
assert.equal(en.textContent.includes('Source: Synthetic Latin witness'), false);
assert.equal(la.textContent.includes(english.reading_note), false);
assert.ok(en.querySelector('.text-side-label').textContent.includes('historical antecedent'));
""")

    def test_study_retains_the_full_source_and_element_research(self):
        self.run_case(r"""
for (const mode of ['selected', 'latin-and-selected']) {
  const node = render(mode, true);
  assert.ok(node.textContent.includes(english.reading_note));
  assert.ok(node.textContent.includes(english.note));
  assert.ok(node.textContent.includes(element.note));
  assert.equal(bodies(node).join('').includes(english.note), false);
}
""")

    def test_inapplicable_source_reveals_neither_words_nor_qualification(self):
        self.run_case(r"""
const scoped = structuredClone(element);
scoped.translations[0].applicability = {kind: 'formulary', calendar: 'synthetic',
  formularies: ['easter-sunday'], basis: 'Synthetic day-only source.'};
for (const mode of ['selected', 'latin-and-selected']) {
  for (const context of [undefined, {calendar: 'synthetic', formulary: 'easter-vigil'}]) {
    const node = render(mode, true, scoped, context);
    assert.equal(node.textContent.includes('Historical source words.'), false);
    assert.equal(node.textContent.includes(english.reading_note), false);
    assert.equal(node.textContent.includes(english.note), false);
    assert.equal(node.textContent.includes('Source: Synthetic historical English witness'), false);
  }
  const node = render(mode, false, scoped, {calendar: 'synthetic', formulary: 'easter-sunday'});
  assert.ok(node.textContent.includes(english.reading_note));
  assert.ok(node.textContent.includes('Historical source words.'));
}
""")

    def test_lectern_receives_the_same_nonspoken_note(self):
        self.run_case(r"""
const blocks = dom.read(render());
const note = blocks.find(block => block.classes.includes('ordinary-reading-note'));
assert.ok(note);
assert.equal(note.runs.map(run => run.text).join(''), english.reading_note);
assert.equal(note.lang, 'en');
assert.equal(note.classes.includes('composed-note'), true);
assert.equal(note.classes.includes('ordinary-dialogue'), false);
assert.equal(note.classes.includes('dialogue-turn'), false);
""")

    def test_source_explicit_actors_keep_full_names_and_compact_cues(self):
        self.run_case(r"""
for (const [speaker, label, cue] of [
  ['bishop', 'Bishop', 'B'], ['communicant', 'Communicant', 'C'],
  ['deacon-or-priest', 'Deacon or priest', 'D/P'],
  ['lector', 'Reader', 'L'], ['deacon', 'Deacon', 'D'],
  ['priest', 'Priest', 'P'], ['server', 'Server', 'S'], ['all', 'All', 'All']
]) {
  const words = 'Literal source words.';
  const held = {lang: 'en', text: words, turns: [{speaker, text: words}]};
  const node = Triptych.ordinaryText({kind: 'dialogue'}, held);
  assert.equal(node.querySelector('.ordinary-turn').getAttribute('data-speaker'), speaker);
  assert.equal(node.querySelector('.visually-hidden').textContent, label);
  assert.equal(node.querySelector('.cue-mark').getAttribute('data-cue'), cue);
  assert.equal(node.querySelector('.ordinary-turn-text').textContent, words);
  assert.equal(node.querySelector('.ordinary-turn').hasAttribute('data-dialogue-role'), false);
  const terminal = dom.read(node).map(block => block.runs.map(run => run.text).join('')).join('');
  assert.ok(terminal.includes(cue + ' ' + words));
}
""")

    def test_opening_actor_cues_preserve_literal_text_and_existing_all_semantics(self):
        self.run_case(r"""
for (const [speaker, label, cue] of [
  ['bishop', 'Bishop', 'B'], ['communicant', 'Communicant', 'C'],
  ['deacon-or-priest', 'Deacon or priest', 'D/P'],
  ['lector', 'Reader', 'L'], ['deacon', 'Deacon', 'D'],
  ['priest', 'Priest', 'P'], ['server', 'Server', 'S']
]) {
  const words = 'Literal source words.';
  const node = Triptych.ordinaryText({kind: 'prayer', speaker}, {lang: 'en', text: words});
  assert.equal(node.querySelector('.visually-hidden').textContent, label);
  assert.equal(node.querySelector('.cue-mark').getAttribute('data-cue'), cue);
  assert.ok(node.textContent.endsWith(words));
  assert.equal(node.querySelector('.cue-mark').hasAttribute('data-dialogue-mark'), false);
}
for (const speaker of ['all', 'unclassified-actor']) {
  const node = Triptych.ordinaryText({kind: 'prayer', speaker}, {lang: 'en', text: 'Literal source words.'});
  assert.equal(node.querySelector('.cue-mark'), null);
  assert.equal(node.textContent, 'Literal source words.');
}
""")

    def test_new_actor_does_not_create_or_override_a_dialogue_role(self):
        self.run_case(r"""
const words = 'Amen.';
const held = {lang: 'en', text: words, turns: [
  {speaker: 'communicant', dialogue_role: 'response', text: words}
]};
const response = Triptych.ordinaryText({kind: 'dialogue'}, held);
assert.equal(response.querySelector('.visually-hidden').textContent, 'Response — Communicant');
assert.equal(response.querySelector('.cue-mark').getAttribute('data-cue'), '℟');
assert.equal(response.querySelector('.ordinary-turn-text').textContent, words);
for (const [speaker, label] of [['bishop', 'Bishop'], ['communicant', 'Communicant'],
  ['deacon-or-priest', 'Deacon or priest'], ['lector', 'Reader'], ['deacon', 'Deacon']]) {
  for (const [role, roleLabel, glyph] of [['versicle', 'Versicle', '℣'], ['response', 'Response', '℟']]) {
    const node = Triptych.ordinaryText({kind: 'dialogue'}, {
      lang: 'en', text: words, turns: [{speaker, dialogue_role: role, text: words}]
    });
    assert.equal(node.querySelector('.visually-hidden').textContent, roleLabel + ' — ' + label);
    assert.equal(node.querySelector('.cue-mark').getAttribute('data-cue'), glyph);
    assert.equal(node.querySelector('.ordinary-turn-text').textContent, words);
  }
}
const unknown = Triptych.ordinaryText({kind: 'dialogue'}, {
  lang: 'en', text: words, turns: [{speaker: 'unclassified-actor', text: words}]
});
assert.equal(unknown.querySelector('.cue-mark'), null);
for (const field of ['action', 'gloss']) {
  const note = Triptych.ordinaryText({kind: 'dialogue'}, {
    lang: 'en', text: words, turns: [{speaker: 'bishop', [field]: true, text: words}]
  });
  assert.equal(note.querySelector('.cue-mark'), null);
}
""")


if __name__ == "__main__":
    unittest.main()
