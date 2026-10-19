/* Browser-only mutations get fresh reports from the owning Python classifier. */
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { closeSync, mkdirSync, mkdtempSync, openSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve } from 'node:path';

const REBUILD = String.raw`
import json, sys
sys.path.insert(0, 'scripts')
import _missal_coverage as coverage
payload = json.load(sys.stdin)
metadata = {}
for language in (payload.get('coverage') or {}).get('languages', []):
    for witness in language.get('witnesses', []):
        for alias in witness.get('aliases', []) + [witness['id']]:
            metadata[alias] = witness

def classify(owner, path, source=None, family=None, cycle='all', component=None):
    previous = owner.get('coverage') or {}
    material = dict(owner)
    material['source'] = owner.get('source') or source
    languages = {row['lang']: row for row in previous.get('languages', [])}
    translations = []
    for row in owner.get('translations') or []:
        translated = dict(row)
        public = next((w for w in languages.get(row.get('lang'), {}).get('witnesses', [])
                       if (row.get('source_id') or '') in w.get('aliases', [])), None)
        if public:
            translated['coverage_relationship'] = public['relationship']
            translated['collation'] = public['collation']
        translations.append(translated)
    material['translations'] = translations
    owner['coverage'] = coverage.unit(material,
        target_id=previous.get('target_id') or coverage.identity('browser-fixture', *path),
        occurrence_id=coverage.identity('browser-fixture', *path),
        witnesses=metadata, cycle_family=family, cycle=cycle, component=component,
        latin_relation=languages.get('la', {}).get('relationship', 'unresolved'),
        ordinary_absences={lang: row['availability'] for lang, row in languages.items()}
        if component == 'ordinary-body' else None)

all_units = []
if 'masses' in payload:
    for mass in payload['masses']:
        for index, proper in enumerate(mass.get('propers') or []):
            children = [(family, cycle, child) for family in ('cycles', 'weekday_cycles')
                        for cycle, child in (proper.get(family) or {}).items()]
            path = [payload['calendar'], mass['key'], proper.get('form_id', 'main'), index]
            material = any(proper.get(key) for key in ('text', 'latin', 'citations', 'translations',
                           'unavailable_translations', 'untranslated', 'text_status'))
            if material or not children:
                classify(proper, path, proper.get('source'))
            else:
                proper['coverage'] = None
            for family, cycle, child in children:
                classify(child, path + [family, cycle], proper.get('source'), family, cycle)
        # JSON has copied the grouped legacy view. Rejoin to the same refreshed rows.
        for form in mass.get('forms') or []:
            form['propers'] = [row for row in mass['propers'] if row.get('form_id') == form['id']]
        units = coverage.proper_units(mass)
        mass['coverage'] = coverage.summarize(units, 'mass')
        all_units.extend(units)
    payload['coverage'] = coverage.summarize(all_units, 'calendar')
else:
    for section in payload.get('sections', []):
        for element in section.get('elements', []):
            classify(element, [payload['calendar'], 'ordinary', element['key']], component='ordinary-body')
            all_units.append(element['coverage'])
    payload['coverage'] = coverage.summarize(all_units, 'ordinary')
json.dump(payload, sys.stdout)
`;

export function refreshCoverage(payload, root) {
  const scratch = resolve(root, '.scratch');
  mkdirSync(scratch, { recursive: true });
  const directory = mkdtempSync(resolve(scratch, 'reader-coverage-fixture-'));
  const input = resolve(directory, 'input.json');
  const output = resolve(directory, 'output.json');
  const errors = resolve(directory, 'stderr.log');
  writeFileSync(input, typeof payload === 'string' ? payload : JSON.stringify(payload));
  const descriptors = [openSync(input, 'r'), openSync(output, 'w'), openSync(errors, 'w')];
  try {
    const result = spawnSync(process.env.TRIPTYCH_PYTHON || 'python3', ['-c', REBUILD], {
      cwd: root, stdio: descriptors, timeout: 60000
    });
    if (result.status !== 0) throw new Error(readFileSync(errors, 'utf8') ||
      result.error?.message || 'fixture coverage generation failed');
    return JSON.parse(readFileSync(output, 'utf8'));
  } finally {
    descriptors.forEach(closeSync);
    rmSync(directory, { recursive: true, force: true });
  }
}

export function readerTools(root) {
  const require = createRequire(import.meta.url);
  globalThis.window ||= { location: { search: '' } };
  require(resolve(root, 'src/web/browser/shared/browser-core.js'));
  return { T: window.Triptych,
    A: require(resolve(root, 'src/web/browser/liturgy/reader-state-adapters.js')) };
}

export function fixtureRequest(structure, mass, extra = {}) {
  return { schema: 'triptych-liturgy-reader-state/v1', entrance: 'propers', civilDate: null,
    edition: { id: structure.calendar }, formulary: { id: mass.key, type: mass.kind },
    bible: { id: 'douay-rheims', numbering: 'vulgate' }, languages: { orations: 'en' },
    requestedMode: 'read', options: { ordinary: false, legitimate: {} },
    coverage: [], unresolvedChoices: [], sourceHooks: [], ...extra };
}

// This path validates data and semantic selection without starting a server or Chromium.
export function verifyRealWitnesses(structure, root) {
  const { T, A } = readerTools(root);
  const caswall = 'edition.edward-caswall.lyra-catholica.london-1849';
  const alias = 'artifact.edward-caswall.lyra-catholica.london-1849.missal-sequences-en';
  const cummiskey = 'edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861';
  const sept15 = structure.masses.find(row => row.key === 'septem-dolorum-beatae-mariae-virginis');
  const sequence = sept15.propers.find(row => row.name === 'Sequence');
  assert.equal(sequence.translations.filter(row => row.lang === 'en').length, 2);
  assert.deepEqual(T.coverageWitnesses(sept15.coverage, 'en').map(row => row.id), [caswall]);
  for (const witness of [null, caswall, alias]) {
    const request = fixtureRequest(structure, sept15, {
      languages: { orations: 'en', ...(witness ? { translationWitness: witness } : {}) }
    });
    const result = A.adaptPropers({ request, structure });
    assert.ok(!result.unresolvedChoices.some(row => row.id.startsWith('translation-witness:')));
    assert.equal(T.orationFor(sequence, 'en', witness).missing, false);
  }
  const mass = structure.masses.find(row => row.key === 'commemoratione-omnium-fidelium-defunctorum');
  const base = fixtureRequest(structure, mass, { form: 'first' });
  const pending = A.adaptPropers({ request: base, structure });
  assert.ok(pending.unresolvedChoices.some(row => row.id.startsWith('translation-witness:')));
  const units = T.selectedCoverageUnits(pending, structure);
  const report = T.summarizeCoverage(units);
  const witnesses = T.coverageWitnesses(report, 'en');
  assert.equal(witnesses.length, 3);
  assert.deepEqual(witnesses.map(row => row.available).sort(), [1, 1, 3]);
  assert.ok(witnesses.every(row => /[13] of 6 uses/.test(row.label)));
  const rows = mass.forms.find(row => row.id === 'first').propers;
  for (const [witness, held, absent] of [[caswall, 1, 3], [cummiskey, 3, 1]]) {
    const request = { ...base, languages: { orations: 'en', translationWitness: witness } };
    const result = A.adaptPropers({ request, structure });
    assert.equal(result.events.filter(row => row.selected?.reason === 'absent-in-witness').length, absent);
    const bodyRows = rows.filter(row => row.coverage?.component === 'proper-body');
    const bodies = bodyRows.map(row => T.orationFor(row, 'en', witness));
    assert.equal(bodies.filter(row => !row.missing).length, held);
    assert.equal(bodies.filter(row => row.missing).length, 6 - held);
    assert.equal(bodies.filter(row => row.reason === 'rights-restricted').length, 2);
    assert.ok(bodies.filter(row => row.missing).every(row => row.text === null && !row.fallback));
    assert.match(T.coverageNoticeText(report, 'en', witness),
      new RegExp(held + '/6 uses available from the selected witness'));
  }
  const english = T.orationLanguagesOf(structure).find(row => row.lang === 'en');
  assert.equal(T.orationLanguageLabel(english),
    `English — ${english.available_targets} of ${english.targets} represented texts available`);
  return ['canonical-witness-aliases', 'partial-witness-no-fallback', 'report-language-labels'];
}
