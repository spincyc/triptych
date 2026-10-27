"""An identified historical witness keeps its full research in source Study."""
from __future__ import annotations

import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BROWSER_CORE = ROOT / "src/web/browser/shared/browser-core.js"

CONTRACT = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = process.argv[2], code = process.argv[3], check = process.argv[4];
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
Object.assign(globalThis, {document: dom.document, window: globalThis,
  location: {search: '', hash: '', pathname: '/'},
  history: {replaceState() {}, pushState() {}}, addEventListener() {}});
vm.runInThisContext(fs.readFileSync(code, 'utf8'));
const T = globalThis.Triptych;
const witness = 'edition.gaspar-lefebvre.daily-missal-with-vespers.saint-andre-lohmann-1925';
const structure = JSON.parse(fs.readFileSync(path.join(root,
  'src/web/data/structure/propers/roman-1962.json'), 'utf8'));
const proper = (key, role) => structure.masses.find(m => m.key === key).propers.find(p => p.name === role);
const flat = node => dom.read(node).map(b => b.runs.map(r => r.text).join('')).join('\n');

if (check === 'read') {
  const owner = proper('easter-sunday', 'Collect');
  const selected = T.orationFor(owner, 'en', witness);
  assert.ok(selected.text && selected.caution.includes('"method_path"'));
  const node = T.renderProper(owner, {}, null, {orations: 'en', translationWitness: witness});
  const text = flat(node);
  assert.ok(text.includes(selected.text), 'the literal prayer remains readable');
  assert.ok(text.includes('early version dated to 1925 by its catalogue'));
  assert.ok(text.includes('Its prayer translator is unnamed.'));
  assert.equal(text.includes('whole OCR'), false);
  assert.equal(text.includes('whole-OCR'), false);
  assert.equal(text.includes('"method_path"'), false, 'routine research stays closed in Read');
  const disclosure = node.querySelector('.translation-apparatus');
  assert.ok(disclosure && !disclosure.hasAttribute('open'));
  assert.ok(disclosure.querySelectorAll('p').some(p => p.textContent === selected.caution),
    'the complete caution is retained byte for byte in the disclosure');
}

if (check === 'study') {
  for (const [key, role] of [['easter-sunday', 'Collect'],
    ['comm-s-sabinae-martyris', 'Collect'], ['comm-s-sabinae-martyris', 'Secret']]) {
    const selected = T.orationFor(proper(key, role), 'en', witness);
    assert.ok(selected.text && selected.caution);
    const node = T.translationCredits(selected, {expanded: true});
    const disclosure = node.querySelector('.translation-apparatus');
    assert.ok(disclosure && disclosure.hasAttribute('open'));
    assert.ok(disclosure.querySelectorAll('p').some(p => p.textContent === selected.caution),
      key + ' ' + role + ' retains its complete entry-specific caution');
    assert.ok(flat(node).includes(selected.caution));
  }
}

if (check === 'boundaries') {
  const selected = T.orationFor(proper('easter-sunday', 'Collect'), 'en', witness);
  const marked = {...selected, notice: 'Required acknowledgement control'};
  const node = T.translationCredits(marked);
  const notice = node.querySelector('.translation-notice');
  assert.equal(notice.textContent, marked.notice);
  assert.equal(notice.closest('details'), null, 'required notice remains outside the closed disclosure');
  assert.ok(flat(node).includes(marked.notice));
  const unknown = {source: 'edition.fixture.unclassified', caution: 'Unclassified caution control'};
  const unclassified = T.translationCredits(unknown);
  assert.equal(unclassified.querySelector('details'), null);
  assert.ok(flat(unclassified).includes(unknown.caution), 'generic fallback is unchanged');
  for (const source of [
    'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945',
    'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861']) {
    const previous = T.translationCredits({source, caution: 'Existing witness control'});
    assert.ok(previous.querySelector('.translation-apparatus'));
    assert.ok(flat(previous).includes('Historical lay translation; not approved for liturgical use.'));
  }
}
"""


@unittest.skipUnless(shutil.which("node"), "node is required for the production DOM contract")
class LefebvreTranslationPresentationTests(unittest.TestCase):
    def check_contract(self, check: str) -> None:
        done = subprocess.run(
            [shutil.which("node"), "-", str(ROOT), str(BROWSER_CORE), check],
            input=CONTRACT, capture_output=True, text=True, cwd=ROOT, timeout=30,
        )
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_read_preserves_literal_prayer_and_closes_full_research(self) -> None:
        self.check_contract("read")

    def test_study_preserves_complete_easter_and_sabina_cautions(self) -> None:
        self.check_contract("study")

    def test_notices_unclassified_cautions_and_previous_witnesses_stay_visible(self) -> None:
        self.check_contract("boundaries")


if __name__ == "__main__":
    unittest.main()
