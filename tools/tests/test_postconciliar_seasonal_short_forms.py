"""Source-verified seasonal short readings retain literal boundaries and cycles."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec,spec_from_loader
import sys
import unittest
import yaml

ROOT=Path(__file__).resolve().parents[2]
PROPERS=ROOT/"src/sources/calendars/postconciliar/propers.yaml"
SOURCE_FACTS=[{'mass': 'palm-sunday',
  'form': 'main',
  'proper': 'Passion of the Lord',
  'group': 'passion-of-the-lord',
  'page': 80,
  'number': 38,
  'shorts': {'A': 'Matthew 27:11-54', 'B': 'Mark 15:1-39', 'C': 'Luke 23:1-49'}},
 {'mass': 'lent-1',
  'form': 'main',
  'proper': 'Second Reading',
  'group': 'second-reading',
  'page': 73,
  'number': 22,
  'shorts': {'A': 'Romans 5:12, 17-19'}},
 {'mass': 'lent-2',
  'form': 'main',
  'proper': 'Second Reading',
  'group': 'second-reading',
  'page': 74,
  'number': 27,
  'shorts': {'C': 'Philippians 3:20-4:1'}},
 {'mass': 'lent-3',
  'form': 'main',
  'proper': 'First Reading',
  'group': 'first-reading',
  'page': 75,
  'number': 29,
  'shorts': {'B': 'Exodus 20:1-3, 7-8, 12-17'}},
 {'mass': 'lent-3',
  'form': 'main',
  'proper': 'Gospel',
  'group': 'gospel',
  'page': 75,
  'number': 28,
  'shorts': {'A': 'John 4:5-15, 19b-26, 39a, 40-42'}},
 {'mass': 'lent-4',
  'form': 'main',
  'proper': 'Gospel',
  'group': 'gospel',
  'page': 76,
  'number': 31,
  'shorts': {'A': 'John 9:1, 6-9, 13-17, 34-38'}},
 {'mass': 'lent-5',
  'form': 'main',
  'proper': 'Gospel',
  'group': 'gospel',
  'page': 78,
  'number': 34,
  'shorts': {'A': 'John 11:3-7, 17, 20-27, 33b-45'}},
 {'mass': 'holy-family',
  'form': 'main',
  'proper': 'Gospel',
  'group': 'gospel',
  'page': 67,
  'number': 17,
  'shorts': {'B': 'Luke 2:22, 39-40'}},
 {'mass': 'easter-3',
  'form': 'main',
  'proper': 'Gospel',
  'group': 'gospel',
  'page': 88,
  'number': 48,
  'shorts': {'C': 'John 21:1-14'}},
 {'mass': 'lent-5-monday',
  'form': 'main',
  'proper': 'First Reading',
  'group': 'first-reading',
  'page': 192,
  'number': 251,
  'shorts': {'all': 'Daniel 13:41c-62'}},
 {'mass': 'ascension',
  'form': 'day',
  'proper': 'Second Reading',
  'group': 'second-reading',
  'page': 93,
  'number': 58,
  'shorts': {'B': 'Ephesians 4:1-7, 11-13'}}]

def load_tool(name):
    loader=SourceFileLoader("_seasonal_short_"+name.replace("-","_"),str(ROOT/"tools"/name))
    spec=spec_from_loader(loader.name,loader)
    mod=module_from_spec(spec)
    sys.modules[loader.name]=mod
    loader.exec_module(mod)
    return mod

class SeasonalScripturalShortFormsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=yaml.safe_load(PROPERS.read_text())
        cls.masses={m["key"]:m for s in cls.doc["sections"].values() for m in s["masses"]}
        cls.owner=load_tool("mass-propers")
        cls.citations=load_tool("citations")

    def rows(self,fact):
        mass=self.masses[fact["mass"]]
        holder=mass if fact["form"]=="main" else next(f for f in mass["forms"] if f["id"]==fact["form"])
        names=[p["name"] for p in holder["propers"]]
        i=names.index(fact["proper"])
        self.assertEqual(names[i+1],fact["proper"]+" (shorter form)")
        return holder["propers"][i:i+2]

    def test_source_short_forms_are_adjacent_non_cumulative_and_cycle_exact(self):
        for fact in SOURCE_FACTS:
            with self.subTest(mass=fact["mass"],form=fact["form"],proper=fact["proper"]):
                full,short=self.rows(fact)
                self.assertEqual(full["ordinary_disposition"]["option"],"longer")
                self.assertEqual(short["ordinary_disposition"]["option"],"shorter")
                for row in (full,short):
                    self.assertEqual(row["ordinary_disposition"]["kind"],"alternative")
                    self.assertEqual(row["ordinary_disposition"]["group"],fact["group"])
                self.assertEqual(full["ordinary_disposition"]["basis"],short["ordinary_disposition"]["basis"])
                self.assertEqual(short["source"],"scripture")
                self.assertNotIn("text",short)
                if "all" in fact["shorts"]:
                    self.assertNotIn("cycles",short)
                    owners={"all":short}
                else:
                    self.assertEqual(set(short["cycles"]),set(fact["shorts"]))
                    owners=short["cycles"]
                for cycle,ref in fact["shorts"].items():
                    self.assertEqual(owners[cycle]["verses"],[self.citations.parse_citation(ref)])

    def test_owning_citation_projection_preserves_shorter_boundaries(self):
        for fact in SOURCE_FACTS:
            _,short=self.rows(fact)
            for cycle,ref in fact["shorts"].items():
                entry=(short if cycle=="all" else short["cycles"][cycle])["verses"][0]
                projection=self.owner.citation_structure(entry,self.doc["psalm_numbering"],self.owner.book_tokens())
                self.assertIsNone(projection["unresolved"],(fact,projection))
                self.assertEqual(projection["ref"],ref)
                self.assertEqual(entry["ranges"],self.citations.parse_citation(ref)["ranges"])

    def test_part_verse_letters_survive_the_source_rows(self):
        expected={("lent-3","Gospel","A"):["b","a"],("lent-5","Gospel","A"):["b"],("lent-5-monday","First Reading","all"):["c"]}
        for key,parts in expected.items():
            fact=next(f for f in SOURCE_FACTS if (f["mass"],f["proper"],next(iter(f["shorts"])))==key)
            _,short=self.rows(fact)
            target=short if key[2]=="all" else short["cycles"][key[2]]
            actual=[endpoint["part"] for r in target["verses"][0]["ranges"] for endpoint in (r["begin"],r["end"]) if "part" in endpoint]
            self.assertEqual(list(dict.fromkeys(actual)),parts)

if __name__=="__main__": unittest.main()
