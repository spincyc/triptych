"""Held OLM 1981 appointments, source paths and exact local alternatives."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import copy, os, sys, unittest, yaml
ROOT=Path(__file__).resolve().parents[2]
if not (ROOT/'tools').exists():ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'scripts'))
PROPERS=Path(os.environ.get('SUNDAY_SOURCE_CANDIDATE',ROOT/'src/sources/calendars/postconciliar/propers.yaml'))

def load(name,path):
    loader=SourceFileLoader(name,str(path));spec=spec_from_loader(name,loader)
    mod=module_from_spec(spec);sys.modules[name]=mod;loader.exec_module(mod);return mod

class SundaySourcePathsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=yaml.safe_load(PROPERS.read_text())
        cls.masses={m['key']:m for s in cls.doc['sections'].values() for m in s['masses']}
        cls.owner=load('_sunday_source_owner',Path(os.environ.get('SUNDAY_SOURCE_OWNER',ROOT/'scripts/_calendars.py')))
        cls.canon=load('_sunday_source_citations',ROOT/'tools/citations')
    def rows(self,key,name):return [p for p in self.masses[key]['propers']if p['name']==name]
    def relation(self,key,rid):return next(r for r in self.masses[key]['proper_source_paths']if r['id']==rid)
    def test_lenten_complete_courses_and_existing_lengths(self):
        for key,count in [('lent-3',7),('lent-4',6),('lent-5',6)]:
            with self.subTest(mass=key):
                relation=self.relation(key,key+'-readings');self.assertEqual(len(relation['paths']),count)
                for p in relation['paths']:
                    self.assertEqual(len(p['members']),5)
                    cycles={m['material_cycle']['cycle']for m in p['members']};self.assertEqual(len(cycles),1)
                    self.assertEqual({m['appointment']['mass']for m in p['members']},{key})
                    if p['standing']=='optional':
                        self.assertEqual(cycles,{'A'});self.assertEqual(p['calendar_cycles'],{'family':'sunday','in':['B','C']})
                    self.assertEqual(p['choices']['gospel'],'shorter'if 'gospel-shorter'in p['id']else'longer')
                self.assertEqual({p['choices']['gospel']for p in relation['paths']if p['standing']=='optional'},{'longer','shorter'})
        l3=self.relation('lent-3','lent-3-readings')['paths']
        self.assertEqual([(p['calendar_cycles']['in'],p['members'][0]['material_cycle']['cycle'])for p in l3 if p['choices']['first-reading']=='shorter'],[(['B'],'B')])
        self.assertFalse(any(p['choices']=={'first-reading':'shorter','gospel':'shorter'}for p in l3))
    def test_easter_six_pair_is_local_current_cycle_and_conditional(self):
        r=self.relation('easter-6','easter-6-readings');self.assertEqual(len(r['paths']),6)
        for p in r['paths']:
            optional=p['standing']=='optional';self.assertEqual(set(p['choices']),{'second-reading','gospel'})
            self.assertEqual(set(p['choices'].values()),{'easter-7'if optional else'native'})
            self.assertEqual({m['appointment']['occurrence']for m in p['members']},{2 if optional else 1})
            self.assertEqual({m['material_cycle']['cycle']for m in p['members']},set(p['calendar_cycles']['in']))
            if optional:self.assertEqual(p['when'],{'fact':'ascension-on-following-sunday','is':True})
            else:self.assertNotIn('when',p)
        for name in ['Second Reading','Gospel']:
            local=self.rows('easter-6',name)[1]
            donor=self.rows('easter-7',name)[0]
            self.assertEqual(local['cycles'],{c:{'verses':donor['cycles'][c]['verses']}for c in 'ABC'})
            self.assertEqual(local['source'],'scripture');self.assertNotIn('text',local)
    def test_single_seat_appointments_have_exact_refs_and_scope(self):
        palm="Gospel of the Lord's Entrance into Jerusalem"
        row=self.rows('palm-sunday',palm)[1]
        self.assertEqual(set(row['cycles']),{'B'});self.assertEqual(row['cycles']['B']['verses'],[self.canon.parse_citation('John 12:12-16')])
        r=self.relation('palm-sunday','palm-procession-gospel')
        self.assertEqual({m['appointment']['proper']for p in r['paths']for m in p['members']},{palm})
        self.assertEqual([p['ordinary_disposition']['option']for p in self.masses['palm-sunday']['propers']if p['name'].startswith('Passion of the Lord')],['longer','shorter'])
        second=self.rows('easter-sunday','Second Reading');self.assertEqual(len(second),2)
        self.assertEqual(second[0]['verses'],[self.canon.parse_citation('Colossians 3:1-4')])
        self.assertEqual(second[1]['verses'],[self.canon.parse_citation('1 Corinthians 5:6b-8')]);self.assertNotIn('cycles',second[1])
        gospel=self.rows('easter-sunday','Gospel');self.assertEqual(len(gospel),3)
        self.assertEqual(gospel[1]['cycles'],{c:{'verses':self.rows('easter-vigil','Gospel')[0]['cycles'][c]['verses']}for c in 'ABC'})
        self.assertEqual(gospel[2]['verses'],[self.canon.parse_citation('Luke 24:13-35')]);self.assertNotIn('cycles',gospel[2])
        p=self.relation('easter-sunday','easter-day-gospel')['paths'][-1]
        self.assertEqual(p['when'],{'fact':'mass-in-evening','is':True});self.assertEqual(p['members'][0]['appointment']['occurrence'],3)
        self.assertEqual(p['members'][0]['material_cycle'],{'family':None,'cycle':'all'})
        for mass in ['lent-3','lent-4','lent-5','easter-6','palm-sunday','easter-sunday']:
            for relation in self.masses[mass]['proper_source_paths']:
                self.assertNotIn('nativity',relation['id'])
    def test_canonical_owner_admits_exact_source_members(self):
        expected=[('lent-3',7),('lent-4',6),('lent-5',6),('easter-6',6),('palm-sunday',4),('easter-sunday',7)]
        for key,count in expected:
            with self.subTest(mass=key):
                relations=self.owner.public_proper_source_paths(self.doc,self.masses[key])
                self.assertEqual(sum(len(r['paths'])for r in relations),count)
                self.assertEqual({r['source_edition']for r in relations},{'postconciliar'})
                self.assertEqual(self.owner.ordinary_disposition_source_problems(key,'',self.masses[key]['propers']),[])
    def test_canonical_owner_refuses_missing_local_and_malformed_inactive_cycle(self):
        broken=copy.deepcopy(self.doc);masses={m['key']:m for s in broken['sections'].values()for m in s['masses']}
        m=masses['easter-sunday'];p=m['proper_source_paths'][1]['paths'][-1]
        p['members'][0]['appointment']['occurrence']=4
        with self.assertRaises(ValueError):self.owner.public_proper_source_paths(broken,m)
        broken=copy.deepcopy(self.doc);masses={m['key']:m for s in broken['sections'].values()for m in s['masses']}
        m=masses['lent-3'];next(p for p in m['propers']if p['name']=='First Reading')['cycles']['C']['unowned-field']=True
        with self.assertRaises(ValueError):self.owner.public_proper_source_paths(broken,m)

if __name__=='__main__':unittest.main()
