"""All Souls direct body owners, referred occurrences and historical source bounds."""
from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tomllib
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _calendars
import _missal_coverage as coverage
from _proper_latin import (LatinKey, STRUCTURE_SURFACES, publication_records,
                           sanitize_proper, text_sha256)

MASS = 'commemoratione-omnium-fidelium-defunctorum'
NAMES = {'Collect', 'Tract', 'Sequence', 'Offertory', 'Secret', 'Postcommunion'}
CALENDARS = ROOT / 'src/sources/calendars'
EXPECTED = {('first', 'Collect'): ('5e512755467527b255130a5e18e96e261eb8f535404a4c6aeef4456086f4d050', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-collect'), ('first', 'Tract'): ('9ae43a7ab151f037c2b390cb78b97a44d332a3446d77f9280e51cc63e432ff52', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-tract'), ('first', 'Sequence'): ('87f039a9c40447c9af9952efb4e3f1a5a3c2510b8e3d4b4516b6c2376f6008ef', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-sequence'), ('first', 'Offertory'): ('4be2836129c872cd10d52eea31131b2117ef8354ef5f9dd610e65017698be93e', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-offertory'), ('first', 'Secret'): ('1f931cc3bc7fe512b1cd91f1a94a3f7a91d55f510ba81df2742b40b8211f4c31', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-secret'), ('first', 'Postcommunion'): ('96e3dee4fec348be97089331b74a275daafce5eda19fd40a3073c49ca463a652', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-first-postcommunion'), ('second', 'Collect'): ('30e48e208401dc42d128140be8a04c58f12f20d89d9a5c9bcfb90bddfb53f054', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-second-collect'), ('second', 'Tract'): ('9ae43a7ab151f037c2b390cb78b97a44d332a3446d77f9280e51cc63e432ff52', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-second-tract'), ('second', 'Offertory'): ('4be2836129c872cd10d52eea31131b2117ef8354ef5f9dd610e65017698be93e', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-second-offertory'), ('second', 'Secret'): ('cd9140c844f1e30155d93be9993ac51e43630ac6a321fce42e5e33daa10e00a1', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-second-secret'), ('second', 'Postcommunion'): ('ba2b69434a3457a9642232323225ec0964e364632e5e138728912d7bf6efc600', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-second-postcommunion'), ('third', 'Collect'): ('86a4fd1f06fb14467594949b6255fab3dba90108de16013c464ebef4c4f3d16b', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-third-collect'), ('third', 'Tract'): ('9ae43a7ab151f037c2b390cb78b97a44d332a3446d77f9280e51cc63e432ff52', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-third-tract'), ('third', 'Offertory'): ('4be2836129c872cd10d52eea31131b2117ef8354ef5f9dd610e65017698be93e', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-third-offertory'), ('third', 'Secret'): ('b351e3fb080a86848e3596736761a340d2032b791034f8c2870b97f1a4b31c0e', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-third-secret'), ('third', 'Postcommunion'): ('abad7626ab3256d18b99f84e123d0c83632915aa45ccf74fb3f02fb7d57ec8cb', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-third-postcommunion')}
UNCHANGED_HASH = '9cc0c574f099c34eb7e10ee201bb06a587d827ea2c99ac10edb0b56459fe26ee'
ORDERS = {'first': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Tract', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'second': ['Introit', 'Collect', 'Lesson', 'Gradual', 'Tract', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'third': ['Introit', 'Collect', 'Lesson', 'Gradual', 'Tract', 'Sequence', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']}
ENGLISH_OWNERS_HASH = '7086db8b551a289c37f0432337fa182f3569d3850a5810196187910ab4517759'
HISTORICAL_ARTIFACT = 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-souls-twelve-bodies-la-checked-4a41c7e8'
PROJECTION_ARTIFACT = 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.all-souls-sixteen-bodies-871dadab'
HISTORICAL_MANIFEST = 'src/sources/works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/all-souls-twelve-bodies-la-checked-4a41c7e8/artifact.toml'
PROJECTION_MANIFEST = 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-20-editorial-projection/artifacts/all-souls-sixteen-bodies-871dadab/artifact.toml'
SOURCE_SPANS = {'first-collect': [1, 3], 'shared-tract': [5, 7], 'shared-sequence': [9, 83], 'shared-offertory': [85, 91], 'first-secret': [93, 95], 'first-postcommunion': [97, 99], 'second-collect': [101, 102], 'second-secret': [104, 106], 'second-postcommunion': [108, 109], 'third-collect': [111, 114], 'third-secret': [116, 119], 'third-postcommunion': [121, 124]}


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def unmodified(mass):
    return {
        'header': {k: v for k, v in mass.items() if k not in ('notes', 'forms')},
        'forms': [
            {'header': {k: v for k, v in f.items() if k != 'propers'},
             'propers': [p for p in f['propers'] if p.get('takes_from') or p['name'] not in NAMES]}
            for f in mass['forms']
        ],
    }


class AllSoulsBodyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load((CALENDARS / 'roman-1962/propers.yaml').read_text())
        cls.mass = next(m for s in cls.document['sections'].values()
                        for m in s['masses'] if m['key'] == MASS)
        cls.labels = {f['id']: f['name'] for f in cls.mass['forms']}
        cls.ids_by_label = {name: form for form, name in cls.labels.items()}
        cls.records, cls.record_problems = publication_records(CALENDARS, 'roman-1962')

    def test_sixteen_source_owned_bodies_have_exact_independent_permissions(self):
        self.assertEqual(self.record_problems, [])
        own = {}
        for form in self.mass['forms']:
            for proper in form['propers']:
                key = form['id'], proper['name']
                if key not in EXPECTED:
                    continue
                with self.subTest(form=form['id'], proper=proper['name']):
                    self.assertEqual(proper['source'], 'composed')
                    self.assertFalse({'takes_from', 'text_status', 'translations', 'verses'} & set(proper))
                    expected_hash, source_id = EXPECTED[key]
                    self.assertEqual(text_sha256(proper['text']), expected_hash)
                    latin_key = LatinKey(MASS, form['name'], proper['name'], occurrence=1)
                    record = self.records[latin_key]
                    self.assertNotIn('body_status', record)
                    self.assertEqual(record['text_sha256'], expected_hash)
                    self.assertEqual(record['source_id'], source_id)
                    self.assertEqual(record['provenance_status'], 'collated')
                    self.assertEqual(record['relationship'], 'editorial-projection-exact-to-target')
                    self.assertEqual(record['publication_status'], 'permitted')
                    self.assertEqual(record['publication_basis'], 'public-domain')
                    self.assertEqual(record['publication_source_ids'],
                                     [PROJECTION_ARTIFACT, HISTORICAL_ARTIFACT])
                    self.assertTrue(record['verification_source_id'].startswith(
                        'passage.catholic-church.missale-romanum.vatican-typica-1962.'))
                    public = sanitize_proper(proper, latin_key, self.records, STRUCTURE_SURFACES)
                    unit = coverage.unit(public, target_id=str(key), occurrence_id=str(key))
                    latin = next(r for r in unit['languages'] if r['lang'] == 'la')
                    self.assertEqual((latin['availability'], latin['relationship'],
                                      latin['collation'], latin['publication_basis']),
                                     ('available', 'exact-target', 'collated', 'public-domain'))
                    own[key] = record
        self.assertEqual(len(own), 16)
        self.assertEqual({form: sum(key[0] == form for key in own) for form in self.labels},
                         {'first': 6, 'second': 5, 'third': 5})

    def test_two_sequence_pointers_resolve_eighteen_occurrences_to_sixteen_owners(self):
        source = next(f for f in self.mass['forms'] if f['id'] == 'first')
        source_sequence = next(p for p in source['propers'] if p['name'] == 'Sequence')
        for form in self.mass['forms'][1:]:
            pointer = next(p for p in form['propers'] if p['name'] == 'Sequence')
            self.assertEqual(pointer, {'name': 'Sequence', 'takes_from': {
                'mass': MASS, 'form': self.labels['first'], 'proper': 'Sequence',
                'citation': 'Sequentia Dies irae, ut supra 706'}})
            self.assertNotIn(LatinKey(MASS, form['name'], 'Sequence', occurrence=1), self.records)
        resolved, errors = _calendars.resolve_propers(self.document, self.mass)
        self.assertEqual(errors, [])
        occurrences = [(form, p, origin) for form, p, origin in resolved if p['name'] in NAMES]
        self.assertEqual(len(occurrences), 18)
        self.assertEqual(sum(origin is not None for _, _, origin in occurrences), 2)
        for form, proper, origin in occurrences:
            form_id = self.ids_by_label[form]
            owner_form = 'first' if origin else form_id
            self.assertEqual(text_sha256(proper['text']), EXPECTED[owner_form, proper['name']][0])
            if origin:
                self.assertEqual(origin['mass'], MASS)
                self.assertEqual(origin['form'], self.labels['first'])
                self.assertEqual(origin['proper'], 'Sequence')
                self.assertEqual(proper['text'], source_sequence['text'])

    def test_source_payload_and_project_passages_own_distinct_exact_bytes(self):
        historical = tomllib.loads((ROOT / HISTORICAL_MANIFEST).read_text())
        projection = tomllib.loads((ROOT / PROJECTION_MANIFEST).read_text())
        self.assertEqual(historical['id'], HISTORICAL_ARTIFACT)
        self.assertEqual(historical['rights_status'], 'public-domain')
        self.assertEqual(historical['derived_from'],
            'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a')
        self.assertEqual(projection['id'], PROJECTION_ARTIFACT)
        self.assertEqual(projection['rights_status'], 'project-created')
        self.assertEqual(projection['projected_from'], [HISTORICAL_ARTIFACT,
            'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'])
        source_bytes, projected_bytes = (ROOT / historical['path']).read_bytes(), (ROOT / projection['path']).read_bytes()
        self.assertEqual(hashlib.sha256(source_bytes).hexdigest(), historical['sha256'])
        self.assertEqual(hashlib.sha256(projected_bytes).hexdigest(), projection['sha256'])
        self.assertEqual(len(source_bytes), historical['byte_size'])
        self.assertEqual(len(projected_bytes), projection['byte_size'])
        source_lines = source_bytes.decode().splitlines(keepends=True)
        source = {key: ''.join(source_lines[a-1:b]) for key, (a, b) in SOURCE_SPANS.items()}
        self.assertEqual(len(source), 12)
        self.assertTrue(source['first-collect'].endswith('Qui vivis.\n'))
        self.assertTrue(source['second-collect'].endswith('Per.\n'))
        self.assertTrue(source['first-secret'].endswith('Per Dóminum.\n'))
        self.assertIn('sepúlchra', source['shared-sequence'])
        self.assertNotIn('sepulchra', projected_bytes.decode())
        self.assertEqual(source['shared-tract'].count('℣.'), 2)
        self.assertEqual(source['shared-offertory'].count('℣.'), 1)
        self.assertEqual(source['shared-offertory'].count('*'), 1)
        self.assertEqual(source['shared-offertory'].count('Quam olim'), 2)
        self.assertNotIn('et regnas cum Deo Patre', source_bytes.decode())
        projected_lines = projected_bytes.decode().splitlines(keepends=True)
        for expected_hash, passage_id in EXPECTED.values():
            slug = passage_id.rsplit('.', 1)[-1]
            path = ROOT / 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-20-editorial-projection/passages' / (slug + '.toml')
            passage = tomllib.loads(path.read_text())
            self.assertEqual(passage['id'], passage_id)
            self.assertEqual(passage['artifact_id'], PROJECTION_ARTIFACT)
            self.assertEqual(passage['artifact_sha256'], projection['sha256'])
            a, b = passage['physical_line_ranges'][0]
            self.assertEqual(text_sha256(''.join(projected_lines[a-1:b])), expected_hash)

    def test_marks_written_repeats_sequence_order_and_adjacent_readings_are_preserved(self):
        self.assertEqual(digest(unmodified(self.mass)), UNCHANGED_HASH)
        self.assertEqual({f['id']: [p['name'] for p in f['propers']] for f in self.mass['forms']}, ORDERS)
        for form in self.mass['forms']:
            proper = {p['name']: p for p in form['propers']}
            tract, offertory = proper['Tract']['text'], proper['Offertory']['text']
            self.assertEqual(tract.count('V.'), 2)
            self.assertEqual(offertory.count('V.'), 1)
            self.assertEqual(offertory.count('*'), 1)
            self.assertEqual(offertory.count('Quam olim'), 2)
            self.assertTrue(' '.join(offertory.split()).endswith('Quam olim Abrahae promisisti et semini ejus.'))
        sequence = next(p for p in self.mass['forms'][0]['propers'] if p['name'] == 'Sequence')['text']
        incipits = ['Dies irae', 'Quantus tremor', 'Tuba, mirum', 'Mors stupebit',
                    'Liber scriptus', 'Judex ergo', 'Quid sum miser', 'Rex tremendae',
                    'Recordare, Jesu', 'Quaerens me', 'Juste Judex', 'Ingemisco,',
                    'Qui Mariam', 'Preces meae', 'Inter oves', 'Confutatis',
                    'Oro supplex', 'Lacrimosa dies', 'Huic ergo', 'Pie Jesu', 'Dona eis', 'Amen.']
        positions = [sequence.index(incipit) for incipit in incipits]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(sequence.endswith('Amen.\n'))
        self.assertNotIn('V.', sequence)
        self.assertNotIn('R.', sequence)

    def test_existing_english_positive_and_absence_owners_remain_exact(self):
        ledger = tomllib.loads((ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml').read_text())
        owners = {kind: [r for r in ledger[kind] if r['mass'] == MASS]
                  for kind in ('entries', 'untranslated')}
        self.assertEqual((len(owners['entries']), len(owners['untranslated'])), (4, 12))
        self.assertEqual(digest(owners), ENGLISH_OWNERS_HASH)
        for row in owners['untranslated']:
            self.assertEqual(row['availability'], 'unavailable')
            self.assertNotIn('text', row)
        loader = importlib.machinery.SourceFileLoader('all_souls_mass_propers', str(ROOT / 'tools/mass-propers'))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        propers = importlib.util.module_from_spec(spec)
        loader.exec_module(propers)
        for calendar in ('roman-1962', 'roman-pre-1955'):
            report = propers.english_coverage(CALENDARS, calendar)
            for axis in ('unaccounted', 'outside_the_ledger', 'unmatched_records', 'stale_translation_records'):
                self.assertEqual(report[axis], 0, (calendar, axis))


if __name__ == '__main__':
    unittest.main()
