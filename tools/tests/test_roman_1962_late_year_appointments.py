"""Page-based regressions for late-year 1962 normal Mass appointments."""
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _calendars as C

NORMAL = ['Introit','Collect','Epistle','Gradual','Alleluia','Gospel','Offertory','Secret','Communion','Postcommunion']
STEPHEN = 'second-day-within-octave-s-stephani'
INNOCENTS = 'fourth-day-within-octave-ss-innocentium'
JOHN = 's-ioannis-a-cruce-confessoris-ecclesiae'

class LateYearSourceAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = yaml.safe_load((ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())
        cls.masses = C.mass_index(cls.data)

    def resolved(self,key):
        rows,errors=C.resolve_propers(self.data,self.masses[key],appointments=True)
        self.assertEqual(errors,[])
        return rows

    def test_christmas_day_has_own_uncited_alleluia_before_gospel(self):
        # AP102/p21: unit135 is physically between Gradual134 and Gospel136.
        mass=self.masses['nativitate-domini-octave']
        day=next(f for f in mass['forms'] if f['id']=='day')
        self.assertEqual([p['name'] for p in day['propers']],NORMAL)
        proper=day['propers'][4]
        self.assertEqual(proper['source'],'composed')
        self.assertNotIn('verses',proper)
        self.assertTrue('text' in proper or proper.get('text_status',{}).get('scope')=='proper-body')

    def test_stephen_and_innocents_have_own_prayers_and_normal_order(self):
        # AP104/106 units152,161,164 and AP108/109 units182,191,194.
        wanted=[('Lesson' if n=='Epistle' else n) for n in NORMAL]
        for key in [STEPHEN,INNOCENTS]:
            with self.subTest(mass=key):
                rows=self.resolved(key)
                self.assertEqual([p['name'] for _,p,_ in rows],wanted)
                for name in ['Collect','Secret','Postcommunion']:
                    proper=next(p for _,p,_ in rows if p['name']==name)
                    self.assertEqual(proper['source'],'composed')
                    self.assertNotIn('takes_from',proper)

    def test_votive_tracts_do_not_enter_normal_annual_masses(self):
        # Explicit votive paragraphs at AP523 unit1913, AP105 unit157,
        # AP108 unit187 cannot be activated by a calendar season alone.
        for key in ['s-thomae-apostoli',STEPHEN,INNOCENTS]:
            with self.subTest(mass=key):
                names=[p['name'] for _,p,_ in self.resolved(key)]
                self.assertNotIn('Tract',names)
                self.assertEqual(names.count('Alleluia'),1)

    def test_four_graduals_keep_printed_second_verse_components(self):
        # AP512 unit1829; AP513 unit1840; AP517 unit1865; AP801 unit4115.
        required={
            's-francisci-xaverii-confessoris':('Psalms',91,3),
            's-petri-chrysologi-episcopi-confessoris-ecclesiae':('Sirach',44,20),
            's-ambrosii-episcopi-confessoris-ecclesiae-doctoris':('Sirach',44,20),
            's-gregorii-thaumaturgi-episcopi-confessoris':('Sirach',44,20),
        }
        for key,expected in required.items():
            with self.subTest(mass=key):
                proper=next(p for _,p,_ in self.resolved(key) if p['name']=='Gradual')
                actual={(v['book'],r['begin']['chapter'],r['begin']['verse']) for v in proper['verses'] for r in v['ranges']}
                self.assertIn(expected,actual)

    def test_introits_keep_the_printed_additional_components(self):
        # AP805 unit4144; AP104 unit151; AP108 unit181.
        required={
            's-clementis-i-papae-martyris':{('Isaiah',59,21),('Isaiah',56,7),('Psalms',111,1)},
            STEPHEN:{('Psalms',118,1)},
            INNOCENTS:{('Psalms',8,2)},
        }
        for key,expected in required.items():
            with self.subTest(mass=key):
                proper=next(p for _,p,_ in self.resolved(key) if p['name']=='Introit')
                actual={(v['book'],r['begin']['chapter'],r['begin']['verse']) for v in proper['verses'] for r in v['ranges']}
                self.assertLessEqual(expected,actual)

    def test_john_of_cross_uses_the_printed_c2_prayer_form(self):
        # AP806/p725 In medio[22]; AP807/p726 Secret4162/Post4164 C2.
        self.assertEqual(self.masses[JOHN]['takes_from']['mass'],'commune-doctorum-non-pontificis')
        rows=self.resolved(JOHN)
        for name in ['Secret','Postcommunion']:
            _,proper,provenance=next(r for r in rows if r[1]['name']==name)
            self.assertEqual(provenance['mass'],'commune-doctorum-non-pontificis')
        self.assertIsNone(next(r for r in rows if r[1]['name']=='Collect')[2])

if __name__=='__main__':
    unittest.main()
