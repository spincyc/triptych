"""Keep source-established Common referrals as explicit unavailable chant roles."""
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
sys.path.insert(0, str(ROOT / "scripts"))
from _proper_latin import body_owners, sanitize_mass, STRUCTURE_SURFACES

CASES = {'saint-polycarp-bishop-martyr': (536, 333, '717,6', 383), 'saint-martin-i-pope-martyr': (551, 338, '717,6', 383), 'saint-lawrence-brindisi-priest-doctor-church': (602, 351, '729,8', 390), 'saints-pontian-pope-hippolytus-priest-martyrs': (620, 355, '717,6', 383), 'saint-john-chrysostom-bishop-doctor-church': (637, 359, '729,8', 390), 'saint-cecilia-virgin-martyr': (681, 370, '735,2', 391), 'saint-lucy-virgin-martyr': (692, 372, '735,2', 391)}
TARGET = "edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008"

class CommonAcclamationAppointmentsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(CALENDAR.read_text())
        cls.masses = {m['key']: m for b in cls.document['sections'].values() for m in b['masses']}

    def test_source_appointed_acclamations_remain_in_their_actual_seat(self):
        for key,(entry,page,common,common_page) in CASES.items():
            with self.subTest(mass=key):
                rows = self.masses[key]['propers']
                names = [r['name'] for r in rows]
                self.assertEqual(names[1:4], ['Responsorial Psalm', 'Gospel Acclamation', 'Gospel'])
                row = rows[2]
                self.assertEqual(row['source'], 'composed')
                self.assertEqual(row['text_status'], {'state':'unavailable','scope':'proper-body','reasons':[{'kind':'witness-gap','source_id':TARGET}]})
                self.assertIn(f'n. {entry}',row['notes'])
                self.assertIn(f'n. {common}',row['notes'])
                for field in ('text','verses','translations','incipit'):
                    self.assertNotIn(field,row)

    def test_never_adopted_bodies_create_no_fictitious_removed_body_owners(self):
        owners = [key for key,_,_ in body_owners(self.document) if key.mass in CASES and key.proper == 'Gospel Acclamation']
        self.assertEqual(owners, [])

    def test_publication_keeps_the_role_without_bible_or_chant_words(self):
        for key in CASES:
            with self.subTest(mass=key):
                mass = sanitize_mass(self.masses[key], {}, STRUCTURE_SURFACES)
                row, = [r for r in mass['propers'] if r['name']=='Gospel Acclamation']
                self.assertEqual(row['text_status']['scope'],'proper-body')
                self.assertFalse(row.get('text'))
                self.assertFalse(row.get('verses'))

if __name__ == '__main__':
    unittest.main()
