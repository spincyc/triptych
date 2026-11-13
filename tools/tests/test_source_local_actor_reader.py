"""Finite historical actor offers retain selected publication ownership.

These are available source readings, never the default current-edition Mass.
The fixture is the normal complete generated Postconciliar source structure.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / "tools/tests"))
from _product_data import browser_data_root

SCRIPT = r"""
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const A=require(process.argv[1]),C=require(path.join(path.dirname(process.argv[1]),'reader-state.js'));
const source=JSON.parse(fs.readFileSync(process.argv[2]));
const targets=['lent-4','good-friday'];
function adapt(data,key,language,witness) {
 const mass=data.masses.find(m=>m.key===key);
 const request={schema:C.STATE_SCHEMA,entrance:'propers',civilDate:null,edition:{id:'postconciliar'},
  formulary:{id:key,type:mass.kind},bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:language},
  requestedMode:'read',options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 if(witness)request.languages.translationWitness=witness;
 return A.adaptPropers({request,structure:data});
}
function event(result) {return result.events.find(e=>e.sourceLocalActorOffer);}
const operation=process.argv[3];let checks=0;
for(const key of targets)for(const language of ['en','la']) {
 const original=source.masses.find(m=>m.key===key).propers.find(p=>p.source_local_actor_sequences);
 assert(original,'required finite source descriptor is missing');
 if(operation==='positive') {
  const before=JSON.stringify(source),result=adapt(source,key,language),row=event(result),offer=row.sourceLocalActorOffer;
  assert.equal(offer.state,'available');assert.equal(row.conclusionExecution,undefined);
  assert.equal(result.request.requestedMode,'read');assert.equal(result.events.some(e=>e.kind==='ordinary-element'),false);
  const execution=offer.languages[language];assert.equal(execution.state,'source-derived-complete');
  assert.equal(execution.execution_scope,'source-local-1970');assert.equal(execution.target_2008_authenticated,false);
  const text=language==='la'?original.text:original.translations.find(t=>t.lang==='en').text;
  assert.equal(execution.source_text,text);assert.equal(JSON.stringify(source),before);
  const response=execution.sequence.filter(s=>s.dialogue_role==='response');assert.equal(response.length,1);
  assert.equal(response[0].speaker,key==='good-friday'?null:'people');assert.equal(response[0].text,'Amen.');
  const actions=execution.sequence.filter(s=>s.kind==='action');assert.equal(actions.length,key==='good-friday'?1:0);
  if(actions.length){assert.equal(actions[0].text,null);assert.equal(actions[0].spoken_text,null);assert.equal(actions[0].participants,'all');}
  checks++;
 } else {
  const faults={
   'missing-owner':(p,o)=>{if(language==='la')delete p.latin.publication_owner;else delete p.translations.find(t=>t.lang==='en').publication_owner;},
   'foreign-owner':(p,o)=>o.passage_id+='-foreign',
   'wrong-target':(p,o)=>o.target[0]='other-mass',
   'wrong-language':(p,o)=>o.language=language==='la'?'en':'la',
   'extra-owner-field':(p,o)=>o.inferred=true,
   'changed-body':p=>{if(language==='la')p.text+=' drift';else p.translations.find(t=>t.lang==='en').text+=' drift';},
   'changed-source-role':p=>p.source_local_actor_sequences[0].qualification+=' altered',
   'foreign-coverage-target':p=>p.coverage.target_id+='foreign'
  };
  for(const [name,mutate]of Object.entries(faults)){
   const copy=structuredClone(source),proper=copy.masses.find(m=>m.key===key).propers.find(p=>p.source_local_actor_sequences);
   const owner=language==='la'?proper.latin.publication_owner:proper.translations.find(t=>t.lang==='en').publication_owner;
   mutate(proper,owner);const result=event(adapt(copy,key,language)).sourceLocalActorOffer.languages[language];
   assert.equal(result.state,'unresolved',name);assert.deepEqual(result.sequence,[],name);checks++;
  }
 }
}
process.stdout.write(JSON.stringify({checks}));
"""


class SourceLocalActorReaderTests(unittest.TestCase):
    def run_probe(self, operation):
        adapter = os.environ.get("TRIPTYCH_REVIEW_READER_ADAPTER", str(ROOT / "src/web/browser/liturgy/reader-state-adapters.js"))
        source = os.environ.get("TRIPTYCH_REVIEW_ACTOR_STRUCTURE")
        if source is None:
            source = str(browser_data_root(ROOT) / "structure/propers/postconciliar.json")
        done = subprocess.run(["node", "-e", SCRIPT, adapter, source, operation], cwd=ROOT,
                              capture_output=True, text=True, check=True)
        return json.loads(done.stdout)

    def test_historical_offers_preserve_quote_roles_and_default_current_mass(self):
        self.assertEqual(self.run_probe("positive")["checks"], 4)

    def test_body_owner_and_descriptor_changes_refuse_atomic_sequence(self):
        self.assertEqual(self.run_probe("negative")["checks"], 32)


if __name__ == "__main__":
    unittest.main()
