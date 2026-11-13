"""Keep source-established Common referrals as explicit unavailable chant roles,
except the two whose Latin was separately adopted from reviewed sources."""
from pathlib import Path
import hashlib
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
sys.path.insert(0, str(ROOT / "scripts"))
from _proper_latin import LatinKey, body_owners, publication_records, sanitize_mass, STRUCTURE_SURFACES

CASES = {'saint-polycarp-bishop-martyr': (536, 333, '717,6', 383), 'saint-martin-i-pope-martyr': (551, 338, '717,6', 383), 'saint-lawrence-brindisi-priest-doctor-church': (602, 351, '729,8', 390), 'saints-pontian-pope-hippolytus-priest-martyrs': (620, 355, '717,6', 383), 'saint-john-chrysostom-bishop-doctor-church': (637, 359, '729,8', 390), 'saint-cecilia-virgin-martyr': (681, 370, '735,2', 391), 'saint-lucy-virgin-martyr': (692, 372, '735,2', 391)}
TARGET = "edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008"
# Two n. 729,8 referrals no longer stay unavailable: the accepted root adoption
# workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-seven-acclamations/
# root-adoption.json (2026-11-12, installed in 2927f34b6e) supplies their Latin
# from Pustet 1888, verified word-exact against each OLM 1981 appointment.
# Held here by body hash and verification passage only (no chant words).
LATIN_ADOPTED = {
    'saint-lawrence-brindisi-priest-doctor-church': 'passage.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.acclamation-semen-lawrence-brindisi-20261112',
    'saint-john-chrysostom-bishop-doctor-church': 'passage.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.acclamation-semen-john-chrysostom-20261112',
}
LATIN_ADOPTED_SHA256 = 'b4b8cc5177823122346529f2af2de0d5c7e93c90de73e948353426314bdab5a3'
LATIN_ADOPTED_SOURCE = 'passage.catholic-church.breviarium-romanum.pustet-ratisbon-pars-hiemalis-1888.english-completion-20261029-postconciliar-latin1888-semen-publish'

class CommonAcclamationAppointmentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(CALENDAR.read_text())
        cls.masses = {m['key']: m for b in cls.document['sections'].values() for m in b['masses']}

    def test_source_appointed_acclamations_remain_in_their_actual_seat(self):
        for key,(entry,page,common,common_page) in CASES.items():
            with self.subTest(mass=key):
                self.assert_source_appointed_acclamation(key, self.masses[key]['propers'])

    def assert_source_appointed_acclamation(self, key, rows):
        entry, page, common, common_page = CASES[key]
        expected = ['First Reading', 'Responsorial Psalm', 'Gospel Acclamation', 'Gospel']
        if key in ('saint-lawrence-brindisi-priest-doctor-church',
                   'saint-john-chrysostom-bishop-doctor-church'):
            expected.append('Gospel (shorter form)')
        if key == 'saint-john-chrysostom-bishop-doctor-church':
            # Later Antiphonary evidence adds the two antiphons, without
            # changing the Ordo's reading course or its shorter Gospel.
            self.assertIn('artifact page 132, printed page 124', self.masses[key]['notes'])
            expected = ['Entrance Antiphon', *expected, 'Communion Antiphon']
        self.assertEqual([row['name'] for row in rows], expected)
        row, = [row for row in rows if row['name'] == 'Gospel Acclamation']
        self.assertEqual(row['source'], 'composed')
        if key in LATIN_ADOPTED:
            self.assertNotIn('text_status', row)
            self.assertEqual(hashlib.sha256(row['text'].encode()).hexdigest(), LATIN_ADOPTED_SHA256)
        else:
            self.assertEqual(row['text_status'], {'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':TARGET}]})
            self.assertNotIn('text', row)
        self.assertIn(f'n. {entry}',row['notes'])
        self.assertIn(f'n. {common}',row['notes'])
        for field in ('verses','translations','incipit'):
            self.assertNotIn(field,row)

    def test_acclamation_seat_rejects_missing_duplicate_or_reordered_appointments(self):
        key = 'saint-john-chrysostom-bishop-doctor-church'
        rows = self.masses[key]['propers']
        missing = [row for row in rows if row['name'] != 'Gospel Acclamation']
        duplicate = [*rows[:4], rows[3], *rows[4:]]
        reordered = [*rows[:2], rows[3], rows[2], *rows[4:]]
        lost_shorter = [row for row in rows if row['name'] != 'Gospel (shorter form)']
        for label, altered in [('missing', missing), ('duplicate', duplicate),
                               ('reordered', reordered), ('lost-shorter-Gospel', lost_shorter)]:
            with self.subTest(alteration=label), self.assertRaises(AssertionError):
                self.assert_source_appointed_acclamation(key, altered)

    def test_never_adopted_bodies_create_no_fictitious_removed_body_owners(self):
        # Only the two reviewed Latin adoptions own a body, and each is present;
        # no never-adopted referral becomes a (removed) body owner.
        owners = [(key, state) for key,_,state in body_owners(self.document) if key.mass in CASES and key.proper == 'Gospel Acclamation']
        self.assertEqual(sorted(owners), sorted((LatinKey(mass, '', 'Gospel Acclamation', '', '', 1), 'present')
                                               for mass in LATIN_ADOPTED))

    def test_publication_keeps_the_role_without_bible_or_chant_words(self):
        records, problems = publication_records(ROOT / 'src/sources/calendars', 'postconciliar')
        self.assertEqual(problems, [])
        for key in CASES:
            with self.subTest(mass=key):
                mass = sanitize_mass(self.masses[key], {}, STRUCTURE_SURFACES)
                row, = [r for r in mass['propers'] if r['name']=='Gospel Acclamation']
                if key in LATIN_ADOPTED:
                    # Without its per-text record the adopted body is withheld.
                    self.assertTrue(row['latin']['withheld'])
                    published = sanitize_mass(self.masses[key], records, STRUCTURE_SURFACES)
                    shown, = [r for r in published['propers'] if r['name']=='Gospel Acclamation']
                    self.assertFalse(shown['latin']['withheld'])
                    self.assertEqual((shown['latin']['provenance']['source_id'],
                                      shown['latin']['provenance']['verification_source_id'],
                                      shown['latin']['text_sha256']),
                                     (LATIN_ADOPTED_SOURCE, LATIN_ADOPTED[key], LATIN_ADOPTED_SHA256))
                    self.assertFalse(shown.get('verses'))
                else:
                    self.assertEqual(row['text_status']['scope'],'proper-body')
                self.assertFalse(row.get('text'))
                self.assertFalse(row.get('verses'))

if __name__ == '__main__':
    unittest.main()
