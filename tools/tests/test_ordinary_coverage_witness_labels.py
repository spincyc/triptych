"""Language is part of a bilingual edition's coverage witness metadata key."""
from copy import deepcopy
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
import subprocess
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _missal_coverage as coverage


def ordinary_tool():
    loader = importlib.machinery.SourceFileLoader('ordinary_label_fixture', str(ROOT / 'tools/mass-ordinary'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    tool = importlib.util.module_from_spec(spec)
    loader.exec_module(tool)
    tool._missal_coverage = coverage
    return tool


def language(report, lang):
    return next(row for row in report['languages'] if row['lang'] == lang)


class OrdinaryWitnessLabelTests(unittest.TestCase):
    def test_reader_bilingual_source_labels_use_the_selected_language(self):
        script = r'''
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const code = fs.readFileSync(process.argv[1], 'utf8');
const found = code.match(/function witnessNote\([^)]*\)\s*\{[\s\S]*?\n  \}/);
assert(found);
const select = vm.runInNewContext('('+found[0]+')');
const en = {source_id:'edition.synthetic',lang:'en',label:'Synthetic English witness'};
const la = {source_id:'edition.synthetic',lang:'la',label:'Synthetic Latin witness'};
for (const translations of [[en,la],[la,en]]) {
  const file = {translations};
  assert.equal(select(file,'edition.synthetic','en').label,en.label);
  assert.equal(select(file,'edition.synthetic','la').label,la.label);
  assert.equal(select(file,'edition.synthetic','fr'),null);
}
'''
        result = subprocess.run(['/usr/bin/node','-e',script,str(ROOT/'src/web/browser/liturgy/day.js')],
                                capture_output=True,text=True,check=False)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_language_qualified_metadata_keeps_both_labels_and_evidence(self):
        source = 'edition.synthetic-bilingual'
        owner = {'translations': [
            {'lang': lang, 'source_id': source, 'text': 'Synthetic '+lang,
             'relation': 'antecedent', 'collation': 'uncollated', 'rights': 'public-domain'}
            for lang in ['en', 'la']
        ]}
        metadata = {(lang, source): {'source_id': source, 'label': label, 'lang': lang}
                    for lang, label in [('en','Synthetic English witness'),('la','Synthetic Latin witness')]}
        unit = coverage.unit(owner, target_id='target', occurrence_id='use', witnesses=metadata)
        for lang, label in [('en','Synthetic English witness'),('la','Synthetic Latin witness')]:
            witness = language(unit, lang)['witnesses'][0]
            self.assertEqual(witness['label'], label)
            self.assertEqual(witness['id'], source)
            self.assertEqual(witness['relationship'], 'historical-antecedent')
            self.assertEqual(witness['collation'], 'uncollated')
        coverage.validate_summary(coverage.summarize([unit], 'ordinary'))

    def test_existing_source_id_metadata_and_aliases_remain_supported(self):
        source = 'edition.synthetic'
        unit = coverage.unit({'translations': [{'lang':'en','source_id':'artifact.synthetic',
            'text':'Synthetic held text','relation':'antecedent','rights':'public-domain'}]},
            target_id='target', occurrence_id='use', witnesses={'artifact.synthetic':{
                'source_id':source,'label':'Legacy identifier metadata'}})
        witness = language(unit,'en')['witnesses'][0]
        self.assertEqual(witness['label'],'Legacy identifier metadata')
        self.assertEqual(witness['id'],source)
        self.assertEqual(witness['aliases'],['artifact.synthetic',source])

    def test_ordinary_generator_does_not_overwrite_english_with_facing_latin_label(self):
        tool = ordinary_tool()
        source_id = 'edition.synthetic-bilingual'
        witnesses = {(source_id,lang):{'lang':lang,'label':label,'rights':'public-domain'}
                     for lang,label in [('en','Synthetic English witness'),('la','Synthetic Latin witness')]}
        element = {'key':'fixture/one','alternatives':[], 'absent':{'english':None,'latin':None},
                   'translations':[{'lang':lang,'source_id':source_id,'text':'Synthetic '+lang,
                                    'relation':'antecedent','collation':'uncollated','rights':'public-domain'}
                                   for lang in ['en','la']]}
        source = {'schema':tool.SCHEMA,'calendar':'roman-1962','title':'Synthetic frame',
                  'advisory':'Synthetic fixture only','derived_from':'Synthetic source',
                  'sections':[{'key':'fixture','name':'Synthetic section','elements':[{}]}]}
        original = deepcopy(element)
        with mock.patch.object(tool,'read_toml',return_value=source), \
             mock.patch.object(tool,'restricted_witness_table',return_value={}), \
             mock.patch.object(tool,'witness_table',return_value=witnesses), \
             mock.patch.object(tool,'absence_table',return_value={}), \
             mock.patch.object(tool,'variant_table',return_value=([],{})), \
             mock.patch.object(tool,'appointment_table',return_value={}), \
             mock.patch.object(tool,'from_inventory',return_value=[deepcopy(element)]), \
             mock.patch.object(tool,'slot_table',return_value=[]), \
             mock.patch.object(tool,'appointment_coverage'), \
             mock.patch.object(tool._calendars,'index_header',return_value='Synthetic edition'):
            report = tool.calendar_structure(ROOT/'src/sources',Path('roman-1962-ordo-missae-v1.toml'),{})
        child = report['sections'][0]['elements'][0]
        self.assertEqual(child['translations'],original['translations'])
        self.assertEqual(child['absent'],original['absent'])
        for lang,label in [('en','Synthetic English witness'),('la','Synthetic Latin witness')]:
            self.assertEqual(language(child['coverage'],lang)['witnesses'][0]['label'],label)
            summary = language(report['coverage'],lang)
            self.assertEqual(summary['witnesses'][0]['label'],label)
            self.assertEqual(summary['available'],1)
            self.assertEqual(summary['exact_target'],0)
        coverage.validate_summary(report['coverage'])


if __name__ == '__main__':
    unittest.main()
