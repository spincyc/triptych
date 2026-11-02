"""Project translations retain their declared attribution without a source ID."""
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
Object.assign(globalThis, {document: dom.document, window: globalThis,
  location: {search: '', hash: '', pathname: '/'},
  history: {replaceState() {}, pushState() {}}, addEventListener() {}});
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/shared/browser-core.js'), 'utf8'));
const T = Triptych;
const label = 'Triptych study English';
const caution = 'Original study translation; not approved for liturgical use or recitation.';
const translation = {lang: 'en', text: 'Synthetic study translation.',
  source_label: label, rights: 'project-created', caution};
const owner = {name: 'Synthetic Collect', source: 'composed',
  text: 'Verba Latina.', translations: [translation]};
const flat = node => dom.read(node).map(block => block.runs.map(run => run.text).join('')).join('\n');
"""


class ProjectStudyCredits(unittest.TestCase):
    def run_case(self, source):
        result = subprocess.run(
            ["/usr/bin/node", "-e", HARNESS + source, str(ROOT)],
            text=True, capture_output=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_project_label_and_caution_survive_selection_without_inventing_identity(self):
        self.run_case(r"""
const selected = T.orationFor(owner, 'en', null);
assert.equal(selected.source, null);
assert.equal(selected.sourceLabel, label);
assert.equal(selected.rights, 'project-created');
const node = T.translationCredits(selected);
assert.equal(node.querySelector('.translation-credit').textContent, 'Translation: ' + label);
assert.equal(node.querySelector('.translation-qualification').textContent, caution);
assert.equal(node.querySelector('details'), null);
assert.equal(selected.source, null);
assert.equal(Object.hasOwn(translation, 'source_id'), false);
assert.ok(flat(node).includes(label));
assert.ok(flat(node).includes(caution));
""")

    def test_selected_and_bilingual_rendering_show_one_project_credit(self):
        self.run_case(r"""
for (const textDisplay of ['selected', 'latin-and-selected']) {
  const node = T.renderProper(owner, {}, null, {orations: 'en', textDisplay});
  const credits = node.querySelectorAll('.translation-credit');
  assert.equal(credits.length, 1);
  assert.equal(credits[0].textContent, 'Translation: ' + label);
  assert.ok(flat(node).includes(translation.text));
  assert.ok(flat(node).includes(caution));
  assert.equal(flat(node).includes('Historical lay translation'), false);
  if (textDisplay === 'latin-and-selected') {
    const sides = node.querySelectorAll('.text-side');
    const latin = sides.find(side => side.getAttribute('data-text-language') === 'la');
    const english = sides.find(side => side.getAttribute('data-text-language') === 'en');
    assert.ok(latin.textContent.includes(owner.text));
    assert.equal(latin.querySelector('.translation-credit'), null);
    assert.equal(english.querySelectorAll('.translation-credit').length, 1);
  }
}
""")

    def test_missing_or_blank_label_does_not_invent_a_project_credit(self):
        self.run_case(r"""
for (const source of [null, '']) {
  for (const sourceLabel of [undefined, null, '', '   ']) {
    const selected = {source, sourceLabel, caution, notice: 'Required notice control.'};
    const node = T.translationCredits(selected);
    assert.equal(node.querySelector('.translation-credit'), null);
    assert.equal(node.querySelector('.translation-qualification').textContent, caution);
    assert.equal(node.querySelector('.translation-notice').textContent, selected.notice);
  }
}
""")

    def test_historical_and_unclassified_source_credits_keep_their_prior_meaning(self):
        self.run_case(r"""
const historical = T.translationCredits({
  source: 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861',
  sourceLabel: 'A full declared title', caution: 'Historical source research.'
});
assert.equal(historical.querySelector('.translation-credit').textContent,
  'Translation: The Roman Missal for the Laity (Cummiskey, 1861)');
assert.ok(historical.querySelector('.translation-apparatus'));
assert.ok(flat(historical).includes('Historical lay translation; not approved for liturgical use.'));
for (const sourceLabel of [null, 'Declared unclassified title']) {
  const source = 'edition.synthetic.unclassified';
  const node = T.translationCredits({source, sourceLabel, caution});
  assert.equal(node.querySelector('.translation-credit').textContent,
    'Translation: ' + (sourceLabel || source));
  assert.equal(node.querySelector('.translation-qualification').textContent, caution);
}
""")


if __name__ == "__main__":
    unittest.main()
