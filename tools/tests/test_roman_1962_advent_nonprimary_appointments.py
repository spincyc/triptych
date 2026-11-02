"""Bounded page-image regressions for normal Advent and Epiphany propers."""
from __future__ import annotations

import copy
from hashlib import sha256
from pathlib import Path
import sys
import tomllib
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

DATA = ROOT / 'src/sources/calendars/roman-1962/propers.yaml'
ENGLISH = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'

# Independent image facts: AP87/p6 unit35, AP86/p5 unit25, AP95/unit94,
# AP121/p40 unit273, and AP116/p35 unit241's explicit votive-only clause.
EXPECTED_ORATIO_ORDER = ['Introit', 'Collect', 'First Lesson', 'First Gradual',
                         'Oratio', 'Second Lesson', 'Second Gradual', 'Gospel',
                         'Offertory', 'Secret', 'Communion', 'Postcommunion']
EXPECTED_HOLY_NAME_ORDER = ['Introit', 'Collect', 'Lesson', 'Gradual', 'Alleluia',
                           'Gospel', 'Offertory', 'Secret', 'Communion',
                           'Postcommunion']
NEW_BODIES = [('advent-3', 'Alleluia'), ('advent-ember-wednesday', 'Oratio'),
              ('mass-of-the-first-sunday-after-epiphany', 'Introit')]
# Later admitted whole Latin bodies (collated, permitted rows in
# src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml): 1f1be432b
# phase5-latin22, and 8d7e3b301 per
# workflows/reviews/missal-reader-completion-2026-10-26/latin-five-oratio-source-review.json.
# Their English absences became one confirmed entry each (eeab39fef core39 and
# da270a039 sanctoral-oratio-five, [[accepted]] in
# src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml).
ADMITTED_BODIES = {
    ('advent-3', 'Alleluia'): '0188d53c71815633e8cf11e8d8a245f74e98481cafb978ebe38348733b0b3ccc',
    ('advent-ember-wednesday', 'Oratio'): '74e442a42a44911f7dcfddf187a9ca60803e4cf8cd1eb0dd12e989bbc8d9e20a'}
ADMITTED_ENGLISH = {('advent-3', 'Alleluia'): 'lasance-1945',
                    ('advent-ember-wednesday', 'Oratio'): 'lefebvre-1925'}


def masses(document):
    return {mass['key']: mass for section in document['sections'].values()
            for mass in section['masses']}


def problems(document):
    by_key = masses(document)
    errors = []
    for key, expected in [('advent-ember-wednesday', EXPECTED_ORATIO_ORDER),
                          ('most-holy-name-of-jesus', EXPECTED_HOLY_NAME_ORDER)]:
        rows, failures = resolve_propers(document, by_key[key])
        if failures or [p['name'] for _, p, _ in rows] != expected:
            errors.append((key, 'source order or normal eligibility'))
    for mass, name in NEW_BODIES:
        target = next((p for p in by_key[mass]['propers'] if p['name'] == name), None)
        if target is None:
            errors.append((mass, name, 'missing required source unit'))
            continue
        expected_source = 'mixed' if name == 'Introit' else 'composed'
        if (mass, name) in ADMITTED_BODIES:
            if (target.get('source') != expected_source or 'text_status' in target
                    or sha256(target.get('text', '').encode('utf-8')).hexdigest()
                    != ADMITTED_BODIES[mass, name]):
                errors.append((mass, name, 'literal body disposition'))
        elif (target.get('source') != expected_source or 'text' in target
                or target.get('text_status') != {
                    'state': 'unavailable', 'scope': 'proper-body',
                    'reasons': [{'kind': 'no-exemplar'}]}):
            errors.append((mass, name, 'literal body disposition'))
        if name != 'Introit' and 'verses' in target:
            errors.append((mass, name, 'invented citation'))
    offertory = next(p for p in by_key['advent-4']['propers'] if p['name'] == 'Offertory')
    expected = [{'book': 'Luke', 'ranges': [{'begin': {'chapter': 1, 'verse': 28},
                                          'end': {'chapter': 1, 'verse': 28}}],
                 'ref': 'Luke 1:28'}]
    if offertory['verses'] != expected:
        errors.append(('advent-4', 'Offertory', 'printed citation'))
    introit = next(p for p in by_key['mass-of-the-first-sunday-after-epiphany']['propers']
                   if p['name'] == 'Introit')
    if [(v['book'], v['ranges']) for v in introit['verses']] != [
            ('Psalms', [{'begin': {'chapter': 99, 'verse': 1},
                         'end': {'chapter': 99, 'verse': 1}}])]:
        errors.append(('ferial Epiphany I', 'psalm companion'))
    return errors


class AdventNonprimaryAppointmentsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(DATA.read_text())
        cls.english = tomllib.loads(ENGLISH.read_text())

    def test_the_source_appointments_and_normal_course(self):
        self.assertEqual(problems(self.document), [])

    def test_each_new_literal_has_one_exact_english_whole_body_disposition(self):
        for mass, proper in NEW_BODIES:
            with self.subTest(mass=mass, proper=proper):
                rows = [r for r in self.english['untranslated']
                        if (r['mass'], r.get('form_id', 'main'), r['proper'],
                            r.get('cycle', 'all'), r.get('occurrence', 1),
                            r['lang'], r.get('extent', 'body'))
                        == (mass, 'main', proper, 'all', 1, 'en', 'body')]
                entries = [r for r in self.english['entries']
                           if (r['mass'], r.get('form_id', 'main'), r['proper'],
                               r.get('cycle', 'all'), r.get('occurrence', 1))
                           == (mass, 'main', proper, 'all', 1)]
                if (mass, proper) in ADMITTED_ENGLISH:
                    self.assertEqual(rows, [])
                    self.assertEqual(len(entries), 1)
                    self.assertEqual(([t['lang'] for t in entries[0]['translations']],
                                      entries[0]['witness'], entries[0]['collation_result']),
                                     (['en'], ADMITTED_ENGLISH[mass, proper], 'confirmed'))
                    continue
                self.assertEqual(entries, [])
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]['availability'], 'unavailable')
                self.assertEqual(rows[0]['reason'], {'kind': 'no-exemplar'})

    def test_missing_oratio_and_votive_branch_leak_are_detected(self):
        missing = copy.deepcopy(self.document)
        mass = masses(missing)['advent-ember-wednesday']
        mass['propers'] = [p for p in mass['propers'] if p['name'] != 'Oratio']
        # A removed required node is reported, without deriving a second order.
        self.assertTrue(problems(missing))
        leaked = copy.deepcopy(self.document)
        mass = masses(leaked)['most-holy-name-of-jesus']
        index = next(i for i, p in enumerate(mass['propers']) if p['name'] == 'Gospel')
        mass['propers'].insert(index, {'name': 'Tract', 'source': 'scripture',
            'verses': [{'book': 'Psalms', 'ranges': [
                {'begin': {'chapter': 79, 'verse': 20},
                 'end': {'chapter': 79, 'verse': 20}}], 'ref': 'Psalms 79:20'}],
            'ordinary_disposition': {'kind': 'conditional', 'group': 'holy-name-tract',
                'basis': 'A season-only condition cannot establish votive eligibility.',
                'when': {'fact': 'roman-1962-common-chant-regime', 'in': ['tract']}}})
        self.assertTrue(problems(leaked))

    def test_inferred_citation_is_detected(self):
        changed = copy.deepcopy(self.document)
        target = next(p for p in masses(changed)['advent-3']['propers']
                      if p['name'] == 'Alleluia')
        target['verses'] = [{'book': 'Psalms', 'ranges': [
            {'begin': {'chapter': 79, 'verse': 3},
             'end': {'chapter': 79, 'verse': 3}}], 'ref': 'Psalm 79:3'}]
        self.assertTrue(problems(changed))


if __name__ == '__main__':
    unittest.main()
