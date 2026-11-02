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
from _proper_latin import LatinKey, publication_records, text_sha256

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
    ('s-hieronymi-aemiliani-confessoris', 'Alleluia'): [('Psalms', 111, 9, 111, 9)],
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
# Separate mixed/conditional course rows; the Annunciation owning test checks
# their exact model bounds, source anchor, English identity and execution.
NORMAL_COURSE = {
    ('annuntiatio-beatae-mariae-virginis', 'Gradual'): (576, 495, 2326),
    ('annuntiatio-beatae-mariae-virginis', 'Tract'): (576, 495, 2327),
    ('annuntiatio-beatae-mariae-virginis', 'Alleluia'): (576, 495, 2328),
}
# The bounded AP585/printed504 unit2392 is the own Paschal Introit.
# The later Common III wording reference is a different local occurrence.
OWN_OCCURRENCES = {('s-hermenegildi-martyris', 'Introit'): 1}
SOURCE = 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'
# Whole source-owned chant bodies, independently pinned.
CHANT_HASHES = {('nativitate-beatae-mariae-virginis', 'Introit'): 'ac1ab9d240f7cb3a0f088b80acb48167d61a16abc34d4fd96a865714ab886bc3', ('nativitate-beatae-mariae-virginis', 'Gradual'): '4896ee177aa0b456e960353ff0f5bbfa528a96a63aa9ea345fbbc9e3343845d8', ('nativitate-beatae-mariae-virginis', 'Alleluia'): 'a59d3ce0509fb1fe1b8066be8924a3e65a3235bbe0eca82c8e39465839533400', ('nativitate-beatae-mariae-virginis', 'Offertory'): '6a49511ddca9bbae452c505236e219da4e5f9796c6032e18180009776d3df9a2', ('nativitate-beatae-mariae-virginis', 'Communion'): '7083e0d7d8b0fcfa0708cfb40cfab85450b47d45cd1eb029bc930197e49ec979', ('s-laurentii-martyris', 'Alleluia'): '197f737fc1392463d519c814fd6813e91234acb56f4b9d82a1dd04e52a32d3e8', ('s-matthaei-apostoli-evangelistae', 'Alleluia'): 'fe78c111312d6329c2e9e48a5729be71eb761e56f84c15405459771f0aba4496', ('s-martini-episcopi-confessoris', 'Alleluia'): '4f67dbe69d5046af1293fde8dc2bbe69e20d265a9b97b92af33e5a7a7d234fd5'}
CHANT_PASSAGES = {('nativitate-beatae-mariae-virginis', 'Introit'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-bvm-nativity-introit', ('nativitate-beatae-mariae-virginis', 'Gradual'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-bvm-nativity-gradual', ('nativitate-beatae-mariae-virginis', 'Alleluia'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-bvm-nativity-alleluia', ('nativitate-beatae-mariae-virginis', 'Offertory'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-bvm-nativity-offertory', ('nativitate-beatae-mariae-virginis', 'Communion'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-bvm-nativity-communion', ('s-laurentii-martyris', 'Alleluia'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-laurence-alleluia', ('s-matthaei-apostoli-evangelistae', 'Alleluia'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-matthew-alleluia', ('s-martini-episcopi-confessoris', 'Alleluia'): 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-martin-alleluia'}
# Each former no-exemplar English absence became one confirmed received English
# entry: 1f1be432b (the Communion is the exact Cummiskey REUSE_TARGET pinned by
# test_roman_1962_english31_phase4) and eeab39fef
# (the other seven, Lasance 1945; [[accepted]] core193/core39 in
# src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml).
CHANT_ENGLISH = {key: 'lasance-1945' for key in CHANT_HASHES}
CHANT_ENGLISH['nativitate-beatae-mariae-virginis', 'Communion'] = 'cummiskey-1861'
HISTORICAL_ARTIFACT = 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.uncited-eight-chants-la-checked-d05badcc'
PROJECTION_ARTIFACT = 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.uncited-eight-chants-a4fbf91f'


# The serial July/August and Easter/Pentecost source packages extend this
# shared inventory by these exact47 page-collated appointments. Their source
# bodies/courses are checked in the dedicated source appointment regressions.
SERIAL_APPOINTMENTS = {('assumptione-beatae-mariae-virginis', 'Alleluia'): (709, 628, 3382),
 ('easter-thursday', 'Alleluia'): (418, 337, 1188),
 ('easter-tuesday', 'Alleluia'): (414, 333, 1166),
 ('holy-wednesday', 'Oratio'): (228, 147, 882),
 ('holy-wednesday', 'Oratio super populum'): (232, 151, 890),
 ('immaculati-cordis-beatae-mariae-virginis', 'Gradual'): (714, 633, 3427),
 ('immaculati-cordis-beatae-mariae-virginis', 'Offertory'): (715, 634, 3432),
 ('pentecost-ember-friday', 'Alleluia'): (446, 365, 1366),
 ('pentecost-ember-wednesday', 'Oratio'): (443, 362, 1344),
 ('pentecost-ember-wednesday', 'Second Alleluia'): (443, 362, 1346),
 ('pentecost-monday', 'Alleluia'): (439, 358, 1323),
 ('pentecost-thursday', 'Alleluia'): (445, 364, 1356),
 ('pentecost-tuesday', 'Alleluia'): (441, 360, 1333),
 ('rogation-mass', 'Alleluia'): (429, 348, 1266),
 ('rogation-mass', 'Alleluia (Tempore paschali)'): (429, 348, 1264),
 ('rogation-mass', 'Gradual'): (429, 348, 1265),
 ('rogation-mass', 'Tract'): (429, 348, 1267),
 ('s-apollinaris-episcopi-martyris', 'Introit'): (679, 598, 3143),
 ('s-bernardi-abbatis-ecclesiae-doctoris', 'Offertory'): (713, 632, 3416),
 ('s-caietani-confessoris', 'Alleluia'): (697, 616, 3287),
 ('s-caietani-confessoris', 'Gradual'): (697, 616, 3286),
 ('s-camilli-lellis-confessoris', 'Alleluia'): (671, 590, 3082),
 ('s-dominici-confessoris', 'Gradual'): (694, 613, 3262),
 ('s-ignatii-confessoris', 'Alleluia'): (689, 608, 3228),
 ('s-ignatii-confessoris', 'Gradual'): (689, 608, 3227),
 ('s-ignatii-confessoris', 'Introit'): (689, 608, 3224),
 ('s-ioannae-franciscae-fremiot-chantal-viduae', 'Postcommunion'): (714, 633, 3422),
 ('s-ioannae-franciscae-fremiot-chantal-viduae', 'Secret'): (713, 632, 3421),
 ('s-iosephi-calasanctii-confessoris', 'Alleluia'): (720, 639, 3472),
 ('s-irenaei-episcopi-martyris', 'Gradual'): (659, 578, 2975),
 ('s-laurentii-brundusio-confessoris-ecclesiae-doctoris', 'Collect'): (675, 594, 3117),
 ('s-ludovici-regis-confessoris', 'Alleluia'): (718, 637, 3459),
 ('s-ludovici-regis-confessoris', 'Gradual'): (718, 637, 3458),
 ('s-mariae-magdalenae-paenitentis', 'Alleluia'): (678, 597, 3137),
 ('s-marthae-virginis', 'Alleluia'): (686, 605, 3203),
 ('s-marthae-virginis', 'Communion'): (687, 606, 3208),
 ('ss-nazarii-celsi-martyrum-victoris-i', 'Gradual'): (685, 604, 3191),
 ('ss-septem-fratrum-martyrum-ac-ss', 'Alleluia'): (664, 583, 3015),
 ('vigil-assumption', 'Communion'): (707, 626, 3374),
 ('vigil-assumption', 'Gradual'): (706, 625, 3369),
 ('vigil-assumption', 'Offertory'): (706, 625, 3371),
 ('vigil-of-the-ascension', 'Alleluia'): (431, 350, 1276),
 ('visitatione-beatae-mariae-virginis', 'Alleluia'): (656, 575, 2954),
 ('visitatione-beatae-mariae-virginis', 'Communion'): (657, 576, 2959),
 ('visitatione-beatae-mariae-virginis', 'Gradual'): (656, 575, 2953),
 ('visitatione-beatae-mariae-virginis', 'Introit'): (655, 574, 2949),
 ('visitatione-beatae-mariae-virginis', 'Offertory'): (656, 575, 2956)}


def masses(document):
    return {m['key']: m for section in document['sections'].values() for m in section['masses']}


def bounds(proper):
    return [(v['book'], r['begin']['chapter'], r['begin']['verse'], r['end']['chapter'], r['end']['verse'])
            for v in proper.get('verses', []) for r in v['ranges']]


def citation_problems(document):
    by_key = masses(document)
    problems = []
    for (key, name), expected in EXPECTED.items():
        resolved, errors = resolve_propers(document, by_key[key], appointments=True)
        if errors:
            problems.append((key, name, 'resolution', errors))
            continue
        matches = [(form, p, origin) for form, p, origin in resolved if p['name'] == name]
        occurrence = OWN_OCCURRENCES.get((key, name))
        if occurrence is not None:
            # Require the one direct own unit as well as its exact derived
            # coordinate: a borrowed or duplicate own row cannot replace it.
            direct = [row for row in matches if row[2] is None]
            if len(direct) != 1:
                problems.append((key, name, 'direct count', len(direct)))
                continue
            coordinate = {'mass': key, 'form_id': 'main', 'proper': name,
                          'occurrence': occurrence}
            matches = [row for row in matches
                       if row[1].get('appointment_identity') == coordinate]
        if len(matches) != 1:
            problems.append((key, name, 'count', len(matches)))
            continue
        form, proper, origin = matches[0]
        if form or origin is not None or proper.get('source') != 'scripture' or bounds(proper) != expected:
            problems.append((key, name, 'direct ordered citation', bounds(proper)))
    return problems


def normal_feast_problems(document):
    """The printed own feast course excludes separately stated votive branches."""
    by_key = masses(document)
    problems = []
    expected_order = ['Introit', 'Collect', 'Lesson', 'Gradual', 'Alleluia',
                      'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']
    for key in ('s-hieronymi-aemiliani-confessoris', 's-laurentii-martyris'):
        resolved, errors = resolve_propers(document, by_key[key])
        names = [p['name'] for _, p, _ in resolved]
        wanted = ['Epistle' if name == 'Lesson' and key == 's-laurentii-martyris' else name
                  for name in expected_order]
        if errors or names != wanted:
            problems.append((key, 'normal source order', names, errors))
        if key == 's-hieronymi-aemiliani-confessoris':
            alleluia = [p for _, p, _ in resolved if p['name'] == 'Alleluia']
            if len(alleluia) != 1 or bounds(alleluia[0]) != [('Psalms', 111, 9, 111, 9)]:
                problems.append((key, 'normal Alleluia excludes votive Psalm111:1'))
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

    def test_uncited_chants_have_exact_historical_bodies(self):
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
                self.assertFalse({'verses', 'translations', 'takes_from', 'text_status'} & set(proper))
                self.assertEqual(text_sha256(proper['text']), CHANT_HASHES[key, name])
                records, problems = publication_records(ROOT / 'src/sources/calendars', 'roman-1962')
                self.assertEqual(problems, [])
                row = records[LatinKey(key, '', name, occurrence=1)]
                self.assertEqual(row['text_sha256'], CHANT_HASHES[key, name])
                self.assertEqual(row['source_id'], CHANT_PASSAGES[key, name])
                self.assertEqual(row['relationship'], 'editorial-projection-exact-to-target')
                self.assertEqual(row['publication_status'], 'permitted')
                self.assertEqual(row['publication_basis'], 'public-domain')
                self.assertEqual(row['publication_source_ids'], [PROJECTION_ARTIFACT, HISTORICAL_ARTIFACT])
                self.assertNotIn('Hic est sacerdos', proper['text'])

    def test_each_uncited_target_has_one_exact_english_disposition(self):
        for key, name in CHANT_HASHES:
            with self.subTest(mass=key, proper=name):
                def same(row):
                    return (row.get('mass'), row.get('form_id'), row.get('proper'), row.get('cycle'), row.get('occurrence')) == (key, 'main', name, 'all', 1)
                self.assertFalse(any(same(r) and r.get('lang') == 'en' for r in self.translations['untranslated']))
                rows = [r for r in self.translations.get('entries', []) if same(r)]
                self.assertEqual(len(rows), 1)
                self.assertEqual([t['lang'] for t in rows[0]['translations']], ['en'])
                self.assertEqual((rows[0]['witness'], rows[0]['collation_result']), (CHANT_ENGLISH[key, name], 'confirmed'))

    def test_the_evidence_is_exactly_bounded_to_the_repaired_targets(self):
        rows = {(r['mass'], r['proper']): r for r in self.evidence['appointments']}
        self.assertEqual(set(rows), set(EXPECTED) | set(UNCITED) | set(NORMAL_COURSE) | set(SERIAL_APPOINTMENTS))
        self.assertEqual(len(rows), len(self.evidence['appointments']))
        self.assertEqual(self.evidence['artifact_id'], SOURCE)
        self.assertEqual(self.evidence['artifact_sha256'], '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a')
        for identity, locus in SERIAL_APPOINTMENTS.items():
            with self.subTest(serial_target=identity):
                row = rows[identity]
                self.assertEqual((row['pdf_page'], row['printed_page'], row['marginal_number']), locus)
        for identity, locus in {**UNCITED, **NORMAL_COURSE}.items():
            with self.subTest(target=identity):
                row = rows[identity]
                self.assertEqual((row['pdf_page'], row['printed_page'], row['marginal_number']), locus)
                if identity in UNCITED:
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

    def test_normal_feast_courses_exclude_votive_chants(self):
        # CMAA AP674/p593 ordinary Alleluia; AP703/p622 nos3340-3342.
        self.assertEqual(normal_feast_problems(self.document), [])
        laurence = self.by_key['s-laurentii-martyris']
        names = [p['name'] for p in laurence['propers']]
        self.assertEqual(names[names.index('Gradual') + 1], 'Alleluia')
        self.assertNotIn('Tract', names)
        alleluia = next(p for p in laurence['propers'] if p['name'] == 'Alleluia')
        self.assertNotIn('text_status', alleluia)
        self.assertFalse({'verses', 'takes_from', 'translations'} & set(alleluia))
        chant_identity = ('s-laurentii-martyris', 'Alleluia')
        self.assertEqual(text_sha256(alleluia['text']), CHANT_HASHES[chant_identity])
        records, problems = publication_records(ROOT / 'src/sources/calendars', 'roman-1962')
        self.assertEqual(problems, [])
        body_source = records[LatinKey(chant_identity[0], '', chant_identity[1], occurrence=1)]
        self.assertEqual(body_source['source_id'], CHANT_PASSAGES[chant_identity])
        self.assertEqual(body_source['text_sha256'], CHANT_HASHES[chant_identity])
        self.assertEqual(body_source['publication_status'], 'permitted')

        self.assertIn('3347', alleluia['notes'])
        self.assertIn('In Missis votivis', alleluia['notes'])
        self.assertIn('not part of the normal feast', alleluia['notes'])
        identity = lambda row: (row.get('mass'), row.get('form_id'), row.get('proper'),
                                row.get('cycle'), row.get('occurrence'), row.get('lang'))
        target = ('s-laurentii-martyris', 'main', 'Alleluia', 'all', 1, 'en')
        self.assertFalse(any(identity(r) == target for r in self.translations['untranslated']))
        # eeab39fef: one confirmed Lasance entry for the normal-feast Alleluia only.
        english = [r for r in self.translations.get('entries', []) if identity(r)[:5] == target[:5]]
        self.assertEqual(len(english), 1)
        self.assertEqual(([t['lang'] for t in english[0]['translations']], english[0]['witness'],
                          english[0]['collation_result']), (['en'], 'lasance-1945', 'confirmed'))

    def test_votive_citations_and_extra_tract_are_detected(self):
        wrong_alleluia = copy.deepcopy(self.document)
        target = next(p for p in masses(wrong_alleluia)['s-hieronymi-aemiliani-confessoris']['propers']
                      if p['name'] == 'Alleluia')
        target['verses'][0]['ranges'][0] = {'begin': {'chapter': 111, 'verse': 1},
                                          'end': {'chapter': 111, 'verse': 1}}
        target['verses'][0]['ref'] = 'Psalm 111:1'
        self.assertTrue(normal_feast_problems(wrong_alleluia))
        extra_tract = copy.deepcopy(self.document)
        propers = masses(extra_tract)['s-laurentii-martyris']['propers']
        position = next(i for i, p in enumerate(propers) if p['name'] == 'Alleluia')
        propers.insert(position, {'name': 'Tract', 'source': 'scripture', 'verses': [{
            'book': 'Psalms', 'ranges': [{'begin': {'chapter': 20, 'verse': 3},
                                        'end': {'chapter': 20, 'verse': 4}}], 'ref': 'Psalm 20:3-4'}]})
        self.assertTrue(normal_feast_problems(extra_tract))

    def test_hermenegild_own_introit_and_common_reference_have_distinct_coordinates(self):
        key, name = 's-hermenegildi-martyris', 'Introit'
        resolved, errors = resolve_propers(self.document, self.by_key[key], appointments=True)
        self.assertEqual(errors, [])
        matches = [(proper, origin) for _, proper, origin in resolved if proper['name'] == name]
        self.assertEqual(len(matches), 2)
        by_occurrence = {proper['appointment_identity']['occurrence']: (proper, origin)
                         for proper, origin in matches}
        self.assertEqual(set(by_occurrence), {1, 2})
        own, own_origin = by_occurrence[1]
        borrowed, borrowed_origin = by_occurrence[2]
        self.assertEqual(own['appointment_identity'],
                         {'mass': key, 'form_id': 'main', 'proper': name, 'occurrence': 1})
        self.assertIsNone(own_origin)
        self.assertEqual(bounds(own), EXPECTED[(key, name)])
        self.assertEqual(borrowed_origin['mass'], 'commune-unius-martyris-3')
        self.assertNotEqual(bounds(borrowed), bounds(own))

    def test_wrong_missing_or_duplicate_own_introit_cannot_use_the_common(self):
        identity = ('s-hermenegildi-martyris', 'Introit')
        for defect in ('wrong-own', 'missing-own', 'duplicate-own'):
            mutated = copy.deepcopy(self.document)
            by_key = masses(mutated)
            propers = by_key[identity[0]]['propers']
            own_matches = [(i, p) for i, p in enumerate(propers)
                           if p['name'] == identity[1] and not p.get('takes_from')]
            self.assertEqual(len(own_matches), 1)
            index, own = own_matches[0]
            # Even a Common row with the expected citation cannot satisfy the
            # old direct-own source target when that own target is defective.
            donor = next(p for p in by_key['commune-unius-martyris-3']['propers']
                         if p['name'] == 'Introit')
            donor['verses'] = copy.deepcopy(own['verses'])
            if defect == 'wrong-own':
                own['verses'].pop()
            elif defect == 'missing-own':
                propers.pop(index)
            else:
                propers.insert(index + 1, copy.deepcopy(own))
            with self.subTest(defect=defect):
                problems = citation_problems(mutated)
                self.assertEqual([(p[0], p[1]) for p in problems], [identity])
                self.assertEqual(problems[0][2],
                                 'direct ordered citation' if defect == 'wrong-own' else 'direct count')

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

    def test_sedulius_introit_keeps_whole_mixed_extent_and_literal_cue(self):
        key, name = 'nativitate-beatae-mariae-virginis', 'Introit'
        proper = next(p for p in self.by_key[key]['propers'] if p['name'] == name)
        self.assertEqual(proper['source'], 'mixed')
        self.assertEqual(bounds(proper), [('Psalms', 44, 2, 44, 2)])
        self.assertEqual(text_sha256(proper['text']), CHANT_HASHES[key, name])
        body = ' '.join(proper['text'].split())
        self.assertTrue(body.startswith('Salve, sancta parens, enixa puerpera Regem:'))
        self.assertTrue(body.endswith('dico ego opera mea Regi. V. Gloria Patri.'))
        self.assertEqual(body.count('Salve, sancta parens'), 1)
        self.assertNotIn('Sicut erat', body)
        self.assertNotIn('translations', proper)
        self.assertNotIn('text_status', proper)
        self.assertIn('Sedulius', proper['notes'])

    def test_historical_source_and_projection_preserve_distinct_readings(self):
        historical = tomllib.loads((ROOT / 'src/sources/works/catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam/artifacts/uncited-eight-chants-la-checked-d05badcc/artifact.toml').read_text())
        projection = tomllib.loads((ROOT / 'src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-20-editorial-projection/artifacts/uncited-eight-chants-a4fbf91f/artifact.toml').read_text())
        self.assertEqual(historical['id'], HISTORICAL_ARTIFACT)
        self.assertEqual(historical['rights_status'], 'public-domain')
        self.assertEqual(historical['derived_from'],
            'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a')
        self.assertEqual(projection['id'], PROJECTION_ARTIFACT)
        self.assertEqual(projection['projected_from'], [HISTORICAL_ARTIFACT, SOURCE])
        self.assertNotIn('derived_from', projection)
        source = (ROOT / historical['path']).read_text()
        self.assertIn('Génitrix', source)
        self.assertNotIn('Génetrix', source)
        self.assertIn('Allelúja', source)
        gradual = next(p for p in self.by_key['nativitate-beatae-mariae-virginis']['propers']
                       if p['name'] == 'Gradual')
        self.assertIn('Genetrix', gradual['text'])
        self.assertNotIn('Genitrix', gradual['text'])
        self.assertIn('initial dated appointment-only review', self.evidence['limits'])


if __name__ == '__main__':
    unittest.main()
