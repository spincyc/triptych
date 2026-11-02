"""Exact Baruch Communion citation joins preserve each native Bible witness."""
from pathlib import Path
from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader,module_from_spec
import sys,unittest,os
ROOT=Path(os.environ.get('TRIPTYCH_REVIEW_ROOT') or Path(__file__).resolve().parents[2])
sys.path.insert(0,str(ROOT/'scripts'))
import _loci
loader=SourceFileLoader('baruch_index_bible',str(ROOT/'tools/index-bible'))
spec=spec_from_loader(loader.name,loader);B=module_from_spec(spec);loader.exec_module(B)
TARGETS=('world-english-bible-catholic','king-james-version','revised-version-1895')
class BaruchSourceJoins(unittest.TestCase):
 def test_standalone_communion_reaches_the_complete_native_terminal_clause(self):
  for name in TARGETS:
   with self.subTest(edition=name):
    bible=B.Bible(B.SOURCE_ROOT/B.EDITIONS[name]['artifacts'])
    self.assertEqual(bible.carrier('Bar',3,38),('Bar',3,37))
    self.assertEqual(bible.verse('Bar',3,38),bible.verses[('Bar',3,37)])
 def test_public_projection_preserves_native_verse_identity(self):
  departures,refused=_loci.edition_departures('Bar',{key:[{'chapter':3,'first':38,'last':38}] for key in ('vulgate','hebrew','hebrew-unnumbered-titles')},{})
  for name in TARGETS:
   with self.subTest(edition=name):
    self.assertEqual(departures.get(name),[{'chapter':3,'first':37,'last':37}])
    self.assertNotIn(name,refused)
 def test_no_unknown_tail_offset_or_text_rewrite_is_inferred(self):
  for name in TARGETS:
   with self.subTest(edition=name):
    bible=B.Bible(B.SOURCE_ROOT/B.EDITIONS[name]['artifacts'])
    self.assertIsNone(bible.carrier('Bar',3,39))
    self.assertEqual(bible.verse('Bar',3,37),bible.verses[('Bar',3,37)])
    text,problem,_,_=bible.span('Bar',{'begin':{'chapter':3,'verse':39},'end':{'chapter':3,'verse':39}})
    self.assertEqual(text,[]);self.assertIn('3:39',problem)
 def test_vulgate_witnesses_keep_their_own_terminal_verse(self):
  for name in ('douay-rheims','douay-rheims-american-1899','clementine-vulgate','catholic-public-domain-version'):
   with self.subTest(edition=name):
    bible=B.Bible(B.SOURCE_ROOT/B.EDITIONS[name]['artifacts'])
    self.assertEqual(bible.carrier('Bar',3,38),('Bar',3,38))
    self.assertEqual(bible.verse('Bar',3,38),bible.verses[('Bar',3,38)])
