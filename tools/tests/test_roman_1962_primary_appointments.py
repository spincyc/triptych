"""Recover image-collated primary appointments lost by the text-layer pass.

This bounded fixture does not claim that the listed formularies, or the year's
calendar, have otherwise complete appointments or text.
"""
from __future__ import annotations

import copy
import re
import sys
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

DATA = ROOT / 'src/sources/calendars/roman-1962/propers.yaml'
RECORD = ROOT / 'src/sources/inventories/roman-1962-primary-appointment-collation-v1.toml'
EXPECTED_TARGETS = ROOT / 'src/sources/inventories/missal-expected-targets-v1.toml'
ARTIFACT = ROOT / ('src/sources/works/catholic-church/missale-romanum/editions/'
                   'vatican-typica-1962/artifacts/cmaa-facsimile-pdf/artifact.toml')

# Independently read page facts: mass, label, book, machine bounds, PDF page,
# printed page, marginal number, and the next existing node. Do not derive this
# expectation from the calendar, citation parser, or generated browser data.
EXPECTED = [
    ('annuntiatio-beatae-mariae-virginis', 'Lesson', 'Isaiah', [(7, 10, 7, 15)], 576, 495, 2325, 'Gradual'),
    ('nativitate-beatae-mariae-virginis', 'Gospel', 'Matthew', [(1, 1, 1, 16)], 732, 651, 3576, 'Offertory'),
    ('s-hermenegildi-martyris', 'Gospel', 'Luke', [(14, 26, 14, 33)], 585, 504, 2396, 'Offertory'),
    ('litania-maior', 'Lesson', 'Ezekiel', [(1, 10, 1, 14)], 591, 510, 2443, 'Alleluia'),
    ('s-petri-martyris', 'Epistle', '2 Timothy', [(2, 8, 2, 10), (3, 10, 3, 12)], 595, 514, 2472, 'Alleluia'),
    ('vigil-nativity-saint-john-baptist', 'Lesson', 'Jeremiah', [(1, 4, 1, 10)], 642, 561, 2860, 'Gradual'),
    ('vigil-nativity-saint-john-baptist', 'Gospel', 'Luke', [(1, 5, 1, 17)], 643, 562, 2862, 'Offertory'),
    ('nativitate-s-ioannis-baptistae', 'Lesson', 'Isaiah', [(49, 1, 49, 3), (49, 5, 49, 7)], 644, 563, 2869, 'Gradual'),
    ('s-hieronymi-aemiliani-confessoris', 'Lesson', 'Isaiah', [(58, 7, 58, 11)], 674, 593, 3106, 'Gradual'),
    ('s-laurentii-martyris', 'Epistle', '2 Corinthians', [(9, 6, 9, 10)], 703, 622, 3339, 'Gradual'),
    ('decollatione-s-ioannis-baptistae', 'Lesson', 'Jeremiah', [(1, 17, 1, 19)], 723, 642, 3497, 'Gradual'),
    ('s-stephani-regis-confessoris', 'Lesson', 'Sirach', [(31, 8, 31, 11)], 728, 647, 3547, 'Gradual'),
    ('s-matthaei-apostoli-evangelistae', 'Lesson', 'Ezekiel', [(1, 10, 1, 14)], 745, 664, 3681, 'Gradual'),
    ('s-teresiae-a-iesu-infante-virginis', 'Lesson', 'Isaiah', [(66, 12, 66, 14)], 755, 674, 3759, 'Gradual'),
    ('s-birgittae-viduae', 'Epistle', '1 Timothy', [(5, 3, 5, 10)], 761, 680, 3805, 'Gradual'),
    ('s-ioannis-cantii-confessoris', 'Epistle', 'James', [(2, 12, 2, 17)], 773, 692, 3905, 'Gradual'),
    ('s-martini-episcopi-confessoris', 'Gospel', 'Luke', [(11, 33, 11, 36)], 797, 716, 4080, 'Offertory'),
]


def masses(document):
    return {mass['key']: mass for section in document['sections'].values() for mass in section['masses']}


def bounds(proper):
    return [(entry['book'], [(r['begin']['chapter'], r['begin']['verse'],
                              r['end']['chapter'], r['end']['verse'])
                             for r in entry['ranges']])
            for entry in proper.get('verses', [])]


def appointment_problems(document):
    by_key = masses(document)
    problems = []
    for key, name, book, spans, *_ in EXPECTED:
        resolved, errors = resolve_propers(document, by_key[key])
        if errors:
            problems.append((key, name, 'resolution', errors))
            continue
        family = {'Lesson', 'Epistle'} if name in {'Lesson', 'Epistle'} else {'Gospel'}
        matches = [(form, proper, origin) for form, proper, origin in resolved
                   if proper['name'] in family]
        if len(matches) != 1:
            problems.append((key, name, 'family count', len(matches)))
            continue
        form, proper, origin = matches[0]
        if form or origin is not None or proper['name'] != name:
            problems.append((key, name, 'direct named appointment', (form, proper['name'], origin)))
        if proper.get('source') != 'scripture' or bounds(proper) != [(book, spans)]:
            problems.append((key, name, 'appointed ranges', bounds(proper)))
    return problems


class Roman1962PrimaryAppointmentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(DATA.read_text())
        cls.record = tomllib.loads(RECORD.read_text())
        cls.expected_targets = tomllib.loads(EXPECTED_TARGETS.read_text())
        cls.by_key = masses(cls.document)

    def test_the_collated_direct_primary_readings_resolve_exactly(self):
        self.assertEqual(appointment_problems(self.document), [])

    def test_the_primary_readings_keep_their_source_owned_order(self):
        for key, name, _, _, _, _, _, following in EXPECTED:
            with self.subTest(mass=key, proper=name):
                names = [p['name'] for p in self.by_key[key]['propers']]
                slot = names.index(name)
                self.assertLess(names.index('Collect'), slot)
                self.assertEqual(names[slot + 1], following)
                if name != 'Gospel':
                    self.assertLess(slot, names.index('Gospel'))

    def assert_citation_facts(self, document):
        by_key = masses(document)
        self.assertEqual(self.record['target'], DATA.relative_to(ROOT).as_posix())
        self.assertEqual(self.record['calendar'], 'roman-1962')
        for key, name, *_ in EXPECTED:
            propers = [p for p in by_key[key]['propers'] if p['name'] == name]
            self.assertEqual(len(propers), 1, (key, name))
            self.assertEqual(set(propers[0]), {'name', 'source', 'verses'}, (key, name))
            records = [row for row in self.record['appointments']
                       if (row['mass'], row['proper']) == (key, name)]
            self.assertEqual(len(records), 1, (key, name))
            self.assertEqual(records[0]['origin'], 'direct', (key, name))

    def assert_hermenegild_source_join(self, document, inventory):
        # This is the one repaired primary slot with a canonical printed-slot
        # join. The other sixteen additions retain their collation evidence;
        # this fixture does not invent expected-target joins for them.
        targets = {row['id']: row for row in inventory['targets']}
        target_id = 'roman-1962:sanctoral-form:p585-l24:slot:p585-l68:gospel'
        self.assertIn(target_id, targets)
        target = targets[target_id]
        parent_id = 'roman-1962:sanctoral-form:p585-l24'
        expected = {
            'kind': 'text-slot', 'identity_state': 'established',
            'parent_id': parent_id, 'calendar_proper_name': 'Gospel',
            'source_record': ARTIFACT.relative_to(ROOT).as_posix(),
            'source_locus': 'artifact p. 585 / printed p. 504, raw page-local line 68',
        }
        self.assertEqual({field: target.get(field) for field in expected}, expected)
        parent = targets[parent_id]
        self.assertEqual(parent['kind'], 'form')
        self.assertEqual(parent['identity_state'], 'established')
        key = 's-hermenegildi-martyris'
        self.assertEqual(parent['calendar_mass_key'], key)
        self.assertEqual(target.get('calendar_mass_key', key), key)
        self.assertEqual(target.get('form_id', parent.get('form_id', 'main')), 'main')
        self.assertEqual(target.get('calendar_proper_occurrence', 1), 1)
        own = [p for p in masses(document)[key]['propers'] if p['name'] == 'Gospel']
        self.assertEqual(len(own), 1)
        self.assertEqual(set(own[0]), {'name', 'source', 'verses'})
        self.assertEqual(own[0]['source'], 'scripture')
        self.assertEqual(bounds(own[0]), [('Luke', [(14, 26, 14, 33)])])
        row = next(row for row in self.record['appointments']
                   if (row['mass'], row['proper']) == (key, 'Gospel'))
        self.assertEqual((row['pdf_pages'], row['printed_pages'], row['marginal_number']),
                         ([585, 586], [504, 505], 2396))

    def test_the_additions_are_citation_facts_without_body_or_referral(self):
        self.assert_citation_facts(self.document)
        self.assert_hermenegild_source_join(self.document, self.expected_targets)
        self.assertNotIn('s-andreae-avellini-confessoris', {row[0] for row in EXPECTED})

    def test_the_source_join_rejects_wrong_coordinates_and_occurrence(self):
        target_id = 'roman-1962:sanctoral-form:p585-l24:slot:p585-l68:gospel'
        for field, wrong in (
            ('source_locus', 'artifact p. 586 / printed p. 505, raw page-local line 68'),
            ('source_record', RECORD.relative_to(ROOT).as_posix()),
            ('calendar_proper_occurrence', 2),
        ):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.expected_targets)
                target = next(row for row in changed['targets'] if row['id'] == target_id)
                target[field] = wrong
                with self.assertRaises(AssertionError):
                    self.assert_hermenegild_source_join(self.document, changed)

    def test_referral_body_and_lost_own_gospel_remain_detected(self):
        key = 's-hermenegildi-martyris'
        for defect in ('referral', 'body', 'omission'):
            with self.subTest(defect=defect):
                changed = copy.deepcopy(self.document)
                mass = masses(changed)[key]
                gospel = next(p for p in mass['propers'] if p['name'] == 'Gospel')
                if defect == 'referral':
                    gospel['takes_from'] = {
                        'mass': 'common-martyr-outside-easter-3', 'proper': 'Gospel'}
                elif defect == 'body':
                    gospel['body'] = 'An uncollated body must not enter this citation fact.'
                else:
                    mass['propers'].remove(gospel)
                with self.assertRaises(AssertionError):
                    self.assert_citation_facts(changed)
                with self.assertRaises(AssertionError):
                    self.assert_hermenegild_source_join(changed, self.expected_targets)

    def test_the_evidence_preserves_the_exact_appointment_loci(self):
        record_rows = {(r['mass'], r['proper']): r for r in self.record['appointments']}
        self.assertEqual(set(record_rows), {(r[0], r[1]) for r in EXPECTED})
        self.assertEqual(len(record_rows), len(self.record['appointments']))
        for key, name, _, _, pdf, printed, number, _ in EXPECTED:
            with self.subTest(mass=key, proper=name):
                row = record_rows[(key, name)]
                self.assertEqual(row['origin'], 'direct')
                self.assertEqual(row['pdf_pages'], [pdf] if number != 2396 and number != 2443 else [pdf, pdf + 1])
                self.assertEqual(row['printed_pages'], [printed] if number != 2396 and number != 2443 else [printed, printed + 1])
                self.assertEqual(row['marginal_number'], number)
                self.assertTrue(row['printed_head'])
                self.assertTrue(row['printed_reference'])
                self.assertTrue(row['raster_sha256'])
                self.assertTrue(all(re.fullmatch('[0-9a-f]{64}', sha) for sha in row['raster_sha256']))

    def test_the_evidence_names_the_registered_control_without_rights_promotion(self):
        artifact = tomllib.loads(ARTIFACT.read_text())
        self.assertEqual(self.record['artifact_id'], artifact['id'])
        self.assertEqual(self.record['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')
        self.assertEqual(self.record['artifact_byte_size'], 82815941)
        self.assertIn(self.record['artifact_sha256'], str(artifact))
        self.assertEqual(artifact['rights_status'], 'unresolved')
        self.assertIn('No new prayer or reading bodies', self.record['limits'])
        self.assertIn('no complete-formulary', self.record['limits'])

    def test_omission_and_lost_disjoint_range_are_detected(self):
        omitted = copy.deepcopy(self.document)
        key, name = EXPECTED[0][:2]
        mass = masses(omitted)[key]
        mass['propers'] = [p for p in mass['propers'] if p['name'] != name]
        self.assertEqual([(p[0], p[1], p[2]) for p in appointment_problems(omitted)],
                         [(key, name, 'family count')])
        truncated = copy.deepcopy(self.document)
        peter = masses(truncated)['s-petri-martyris']
        epistle = next(p for p in peter['propers'] if p['name'] == 'Epistle')
        epistle['verses'][0]['ranges'].pop()
        self.assertEqual([(p[0], p[1], p[2]) for p in appointment_problems(truncated)],
                         [('s-petri-martyris', 'Epistle', 'appointed ranges')])


if __name__ == '__main__':
    unittest.main()
