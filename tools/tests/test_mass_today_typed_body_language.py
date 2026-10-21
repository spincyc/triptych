"""A typed whole-body gap is not requested-language incipit capability."""
from __future__ import annotations
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import unittest

ROOT=Path(os.environ.get('TRIPTYCH_REVIEW_ROOT',Path(__file__).resolve().parents[2]))
MODULE_ROOT=Path(os.environ.get('TRIPTYCH_TYPED_BODY_CLI_ROOT',ROOT))
sys.path.insert(0,str(ROOT/'scripts'))
loader=importlib.machinery.SourceFileLoader('_typed_body_today',str(MODULE_ROOT/'tools/mass-today'))
spec=importlib.util.spec_from_loader(loader.name,loader)
TODAY=importlib.util.module_from_spec(spec);loader.exec_module(TODAY)

def gap():
    return {'name':'Technical prayer','source':'composed','incipit':'Technical Latin fragment',
            'text_status':{'state':'unavailable','scope':'proper-body'},
            'latin':{'state':'unavailable','held':False,'available':False,'withheld':True},
            'untranslated':[{'lang':'en','state':'no-english-exemplar'}]}

class TypedBodyLanguageTests(unittest.TestCase):
    def test_typed_gap_precedes_latin_incipit_for_unheld_requested_body(self):
        row=gap();before=copy.deepcopy(row)
        result=TODAY.language_projection(row,'en',None)
        self.assertEqual(result['status'],'absent')
        self.assertFalse(result['held'] or result['available'] or result['complete'])
        self.assertNotIn('incipit',result)
        self.assertEqual(result['reason'],TODAY.untranslated_reason(row))
        self.assertEqual(row,before)

    def test_held_requested_translation_survives_unavailable_latin(self):
        row=gap();row['translations']=[{'lang':'en','text':'Technical held English body.'}]
        result=TODAY.language_projection(row,'en',None)
        self.assertEqual(result['status'],'full-text')
        self.assertTrue(result['held'] and result['available'] and result['complete'])
        self.assertEqual(result['texts'],row['translations'])
        self.assertEqual(TODAY.language_projection(row,'la',None)['status'],'unavailable')

    def test_rights_absence_and_real_incipit_only_controls(self):
        for shape in ('ledger','public'):
            row=gap()
            if shape=='ledger':row['untranslated']=[{'lang':'en','state':'rights-restricted'}]
            else:row['unavailable_translations']=[{'lang':'en','state':'rights-restricted'}]
            with self.subTest(shape=shape):self.assertEqual(TODAY.language_projection(row,'en',None)['status'],'withheld')
        row={'name':'Technical fragment','source':'composed','incipit':'Technical Latin fragment'}
        self.assertEqual(TODAY.language_projection(row,'en',None)['status'],'incipit-only')
        row=gap();row['source']='scripture';row['verses']=[{'ref':'Technical reference','text':'Technical Bible body.'}]
        result=TODAY.language_projection(row,'en',{'id':'technical','language':'en'})
        self.assertEqual(result['status'],'scripture-delegated')
        row['source']='mixed'
        self.assertEqual(TODAY.language_projection(row,'en',{'id':'technical','language':'en'})['status'],'absent')

    def test_actual_lent_three_unavailable_prayers_keep_body_gap(self):
        C=TODAY._calendars
        source=C.load_document(ROOT/'src/sources/calendars','postconciliar',effective=False)
        mass=C.mass_index(source)['lent-3']
        for index,name in ((10,'Prayer over the Offerings'),(13,'Prayer after Communion'),(14,'Prayer over the People')):
            row=copy.deepcopy(mass['propers'][index])
            with self.subTest(index=index,name=name):
                self.assertEqual(row['name'],name)
                self.assertEqual({key: row['text_status'][key] for key in ('state','scope')},{'state':'unavailable','scope':'proper-body'})
                self.assertTrue(row.get('incipit'))
                row['untranslated']=[{'lang':'en','state':'no-english-exemplar'}]
                result=TODAY.language_projection(row,'en',None)
                self.assertEqual(result['status'],'absent')
                self.assertEqual(result['reason'],TODAY.untranslated_reason(row))

if __name__=='__main__':unittest.main()
