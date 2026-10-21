"""Bounded page-backed chant and reading-continuation appointments."""
from __future__ import annotations

import copy
import sys
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

DATA = ROOT / 'src/sources/calendars/roman-1962/propers.yaml'
TRANSLATIONS = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
EVIDENCE = ROOT / 'src/sources/inventories/roman-1962-chant-appointment-collation-v1.toml'

# Page-derived expected bounds, preserving source order. These expectations do
# not call the citation parser or read generated browser structure.
EXPECTED = {
    ('annuntiatio-beatae-mariae-virginis', 'Introit'): [('Psalms', 44, 13, 44, 13), ('Psalms', 44, 15, 44, 16), ('Psalms', 44, 2, 44, 2)],
    ('s-hermenegildi-martyris', 'Introit'): [('Psalms', 63, 3, 63, 3), ('Psalms', 63, 2, 63, 2)],
    ('litania-maior', 'Introit'): [('Psalms', 63, 3, 63, 3), ('Psalms', 63, 2, 63, 2)],
    ('litania-maior', 'Alleluia'): [('Psalms', 88, 6, 88, 6), ('Psalms', 20, 4, 20, 4)],
    ('s-petri-martyris', 'Introit'): [('Psalms', 63, 3, 63, 3), ('Psalms', 63, 2, 63, 2)],
    ('s-petri-martyris', 'Alleluia'): [('Psalms', 88, 6, 88, 6), ('Psalms', 20, 4, 20, 4)],
    ('vigil-nativity-saint-john-baptist', 'Introit'): [('Luke', 1, 13, 1, 13), ('Luke', 1, 15, 1, 15), ('Luke', 1, 14, 1, 14), ('Psalms', 20, 2, 20, 2)],
    ('nativitate-s-ioannis-baptistae', 'Communion'): [('Luke', 1, 76, 1, 76)],
    ('s-hieronymi-aemiliani-confessoris', 'Introit'): [('Lamentations', 2, 11, 2, 11), ('Psalms', 112, 1, 112, 1)],
    ('s-hieronymi-aemiliani-confessoris', 'Gradual'): [('Proverbs', 5, 16, 5, 16), ('Psalms', 111, 5, 111, 6)],
    ('s-hieronymi-aemiliani-confessoris', 'Communion'): [('James', 1, 27, 1, 27)],
    ('decollatione-s-ioannis-baptistae', 'Gradual'): [('Psalms', 91, 13, 91, 14), ('Psalms', 91, 3, 91, 3)],
    ('s-stephani-regis-confessoris', 'Gradual'): [('Psalms', 91, 13, 91, 13), ('Psalms', 91, 14, 91, 14), ('Psalms', 91, 3, 91, 3)],
    ('s-stephani-regis-confessoris', 'Alleluia'): [('James', 1, 12, 1, 12)],
    ('s-matthaei-apostoli-evangelistae', 'Gradual'): [('Psalms', 111, 1, 111, 2)],
    ('s-teresiae-a-iesu-infante-virginis', 'Introit'): [('Song of Songs', 4, 8, 4, 9), ('Psalms', 112, 1, 112, 1)],
    ('s-teresiae-a-iesu-infante-virginis', 'Gradual'): [('Matthew', 11, 25, 11, 25), ('Psalms', 70, 5, 70, 5)],
    ('s-birgittae-viduae', 'Alleluia'): [('Psalms', 44, 5, 44, 5)],
    ('s-birgittae-viduae', 'Communion'): [('Psalms', 44, 8, 44, 8)],
    ('s-ioannis-cantii-confessoris', 'Offertory'): [('Job', 29, 14, 29, 16)],
    ('s-martini-episcopi-confessoris', 'Lesson'): [('Sirach', 44, 16, 44, 27), ('Sirach', 45, 3, 45, 20)],
    ('s-martini-episcopi-confessoris', 'Gradual'): [('Sirach', 44, 16, 44, 16), ('Sirach', 44, 20, 44, 20)],
}
UNCITED = {
    ('nativitate-beatae-mariae-virginis', 'Gradual'): (732, 651, 3574),
    ('nativitate-beatae-mariae-virginis', 'Alleluia'): (732, 651, 3575),
    ('nativitate-beatae-mariae-virginis', 'Offertory'): (732, 651, 3577),
    ('nativitate-beatae-mariae-virginis', 'Communion'): (732, 651, 3580),
    ('s-matthaei-apostoli-evangelistae', 'Alleluia'): (745, 664, 3683),
    ('s-laurentii-martyris', 'Alleluia'): (703, 622, 3341),
    ('s-martini-episcopi-confessoris', 'Alleluia'): (797, 716, 4078),
}
SOURCE = 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'


def masses(document):
    return {m['key']: m for section in document['sections'].values() for m in section['masses']}


def bounds(proper):
    return [(v['book'], r['begin']['chapter'], r['begin']['verse'], r['end']['chapter'], r['end']['verse'])
            for v in proper.get('verses', []) for r in v['ranges']]


def citation_problems(document):
    by_key = masses(document)
    problems = []
    for (key, name), expected in EXPECTED.items():
        resolved, errors = resolve_propers(document, by_key[key])
        if errors:
            problems.append((key, name, 'resolution', errors))
            continue
        matches = [(form, p, origin) for form, p, origin in resolved if p['name'] == name]
        if len(matches) != 1:
            problems.append((key, name, 'count', len(matches)))
            continue
        form, proper, origin = matches[0]
        if form or origin is not None or proper.get('source') != 'scripture' or bounds(proper) != expected:
            problems.append((key, name, 'direct ordered citation', bounds(proper)))
    return problems


class Roman1962ChantAppointmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(DATA.read_text())
        cls.by_key = masses(cls.document)
        cls.translations = tomllib.loads(TRANSLATIONS.read_text())
        cls.evidence = tomllib.loads(EVIDENCE.read_text())

    def test_direct_citations_preserve_every_source_range_in_order(self):
        self.assertEqual(citation_problems(self.document), [])

    def test_uncited_chants_have_real_body_free_appointments(self):
        for key, name in UNCITED:
            with self.subTest(mass=key, proper=name):
                resolved, errors = resolve_propers(self.document, self.by_key[key])
                self.assertEqual(errors, [])
                matches = [(form, p, origin) for form, p, origin in resolved if p['name'] == name]
                self.assertEqual(len(matches), 1)
                form, proper, origin = matches[0]
                self.assertFalse(form)
                self.assertIsNone(origin)
                self.assertEqual(proper['source'], 'composed')
                self.assertFalse({'verses', 'text', 'translations', 'takes_from'} & set(proper))
                self.assertEqual(proper['text_status'], {'state': 'unavailable', 'scope': 'proper-body',
                    'reasons': [{'kind': 'witness-gap', 'source_id': SOURCE}]})

    def test_each_uncited_target_has_one_exact_english_absence(self):
        for key, name in UNCITED:
            with self.subTest(mass=key, proper=name):
                def same(row):
                    return (row.get('mass'), row.get('form_id'), row.get('proper'), row.get('cycle'), row.get('occurrence'), row.get('lang')) == (key, 'main', name, 'all', 1, 'en')
                rows = [r for r in self.translations['untranslated'] if same(r)]
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]['reason'], {'kind': 'no-exemplar'})
                self.assertEqual(rows[0]['extent'], 'body')
                self.assertEqual(rows[0]['availability'], 'unavailable')
                self.assertFalse(any(same(r) for r in self.translations.get('entries', [])))

    def test_the_evidence_is_exactly_bounded_to_the_repaired_targets(self):
        rows = {(r['mass'], r['proper']): r for r in self.evidence['appointments']}
        self.assertEqual(set(rows), set(EXPECTED) | set(UNCITED))
        self.assertEqual(len(rows), len(self.evidence['appointments']))
        self.assertEqual(self.evidence['artifact_id'], SOURCE)
        self.assertEqual(self.evidence['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')
        for identity, locus in UNCITED.items():
            with self.subTest(target=identity):
                row = rows[identity]
                self.assertEqual((row['pdf_page'], row['printed_page'], row['marginal_number']), locus)
                self.assertEqual(row['printed_references'], [])
        for row in rows.values():
            self.assertEqual(row['origin'], 'direct')
            self.assertGreater(row['pdf_page'], 0)
            self.assertTrue(row['raster_sha256'])
            for sha in row['raster_sha256']:
                self.assertRegex(sha, r'^[0-9a-f]{64}$')

    def test_source_owned_positions_and_vigil_course_remain_distinct(self):
        for (key, name) in set(EXPECTED) | set(UNCITED):
            names = [p['name'] for p in self.by_key[key]['propers']]
            with self.subTest(mass=key, proper=name):
                if name == 'Introit':
                    self.assertLess(names.index(name), names.index('Collect'))
                elif name == 'Communion':
                    self.assertLess(names.index('Secret'), names.index(name))
                    self.assertLess(names.index(name), names.index('Postcommunion'))
                elif name == 'Offertory':
                    self.assertLess(names.index('Gospel'), names.index(name))
                    self.assertLess(names.index(name), names.index('Secret'))
                else:
                    self.assertLess(names.index('Collect'), names.index(name))
                    self.assertLess(names.index(name), names.index('Gospel'))
        vigil = [p['name'] for p in self.by_key['vigil-nativity-saint-john-baptist']['propers']]
        self.assertNotIn('Alleluia', vigil)
        self.assertEqual(vigil[vigil.index('Gradual') + 1], 'Gospel')

    def test_lost_psalm_and_lesson_constituents_are_detected(self):
        for identity in [('s-petri-martyris', 'Alleluia'), ('s-martini-episcopi-confessoris', 'Lesson'),
                         ('annuntiatio-beatae-mariae-virginis', 'Introit')]:
            mutated = copy.deepcopy(self.document)
            key, name = identity
            proper = next(p for p in masses(mutated)[key]['propers'] if p['name'] == name)
            if identity == ('annuntiatio-beatae-mariae-virginis', 'Introit'):
                proper['verses'][0]['ranges'].pop()
            else:
                proper['verses'].pop()
            with self.subTest(target=identity):
                self.assertEqual([(p[0], p[1]) for p in citation_problems(mutated)], [identity])


if __name__ == '__main__':
    unittest.main()
