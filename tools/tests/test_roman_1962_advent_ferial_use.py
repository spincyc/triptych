"""Four held Advent rubrics applied to actual selected calendar usages."""
from __future__ import annotations

import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_MODULE_ROOT", ROOT))
SOURCE_ROOT = Path(os.environ.get("TRIPTYCH_COMMON_SOURCE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C

_loader = importlib.machinery.SourceFileLoader("_advent_usage_publisher", str(MODULE_ROOT / "tools/mass-propers"))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
PUBLISHER = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = PUBLISHER
_loader.exec_module(PUBLISHER)

SOURCE = C.read_yaml(SOURCE_ROOT / "src/sources/calendars/roman-1962/propers.yaml")
INDEX = C.mass_index(SOURCE)
FACT_ID = "roman-1962-advent-sunday-alleluia-use"
CASES = {
    "advent-1": ("2026-11-29", ["2026-12-01", "2026-12-05"]),
    "advent-2": ("2026-12-06", ["2026-12-09", "2026-12-10", "2026-12-12"]),
    "advent-3": ("2026-12-13", ["2026-12-14", "2026-12-15", "2026-12-17"]),
    "advent-4": ("2026-12-20", ["2026-12-22", "2026-12-23"]),
}
# 2026-12-05 and 12-10 commemorate these saints. Since 8d7e3b301 the Day
# oration assembly binds each commemorated Collect to its exact source owner.
COMMEMORATIONS = ("comm-s-sabbae-abbatis", "comm-s-melchiadis-papae-martyris")

# Canonical source resolver supplies appointment identities and inherited
# metadata. The fixture keeps the actual held source bodies and references;
# the test does not author a second applicability resolver or Missal wording.
def structure():
    masses = []
    for key in [*CASES, "pentecost-2", *COMMEMORATIONS]:
        entries, problems = C.resolve_propers(SOURCE, INDEX[key], appointments=True)
        if problems:
            raise AssertionError(problems)
        rows = []
        for form, proper, _origin in entries:
            # Source-side absence reasons are audit metadata. Cross the same
            # recursive publication boundary as the actual CLI Proper carrier.
            row = PUBLISHER.rights_safe_copy(proper)
            row.update(form=form, form_id="main", cycles={}, translations=[])
            row["citations"] = [{"ref": verse["ref"]} for verse in row.get("verses", [])]
            rows.append(row)
        masses.append({"key": key, "kind": "sanctoral" if key in COMMEMORATIONS else "seasonal",
                       "propers": rows})
    return {"calendar": "roman-1962", "proper_appointment_facts": SOURCE["proper_appointment_facts"],
            "translations": [], "masses": masses}


HARNESS = r"""
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=process.argv[1], modules=process.argv[2];
const A=require(path.join(modules,'src/web/browser/liturgy/reader-state-adapters.js'));
const C=require(path.join(modules,'src/web/browser/liturgy/reader-state.js'));
const M=require(path.join(root,'src/web/browser/liturgy/assembly-model.js'));
const year=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/calendar/roman-1962/2026.json')));
const rubrics=JSON.parse(fs.readFileSync(path.join(root,'src/web/data/structure/rubrics/roman-1962.json')));
const clone=x=>JSON.parse(JSON.stringify(x));
const derive=date=>M.derive({date,year,rubrics});
function request(date,key,entrance='day') {
 const r={schema:C.STATE_SCHEMA,entrance,edition:{id:'roman-1962'},
 bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:'la'},requestedMode:'read',
 options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 if(entrance==='day'){r.civilDate=date;r.calendar={id:'roman-1962'};r.apparatus={why:false,rubrics:true};
 r.selectedReadableFormulary={id:key};}
 else{r.civilDate=null;r.formulary={id:key,type:'seasonal'};}
 return r;
}
const withoutRule=structure=>{const out=clone(structure);for(const mass of out.masses)
 for(const p of mass.propers)if(p.ordinary_disposition&&p.ordinary_disposition.group===mass.key+'-alleluia-use')
 delete p.ordinary_disposition;return out;};
const condition=(result,key)=>result.unresolvedChoices.filter(c=>c.id==='proper-condition/roman-1962/'+key+'/main/'+key+'-alleluia-use');
let raw='';process.stdin.on('data',chunk=>raw+=chunk);process.stdin.on('end',()=>{
 const input=JSON.parse(raw),s=input.structure,base=withoutRule(s),checks=[];
 if(input.mode==='private-status') {
  const target=s.masses.find(m=>m.key==='advent-3').propers.find(p=>p.name==='Alleluia');
  assert.deepEqual(target.text_status,{state:'unavailable',scope:'proper-body'});
  assert.equal(target.source,'composed');assert.deepEqual(target.citations,[]);
  target.text_status.reasons=[{kind:'no-exemplar'}];
  assert.throws(()=>A.adaptDay({request:request('2026-12-13','advent-3'),
   derived:derive('2026-12-13'),structure:s}),/text_status must use the exact public state\/scope shape/);
  checks.push({sourceAuditRefused:true});
 } else if(input.mode==='annual') {
  for(const [key,[sunday,ferias]] of Object.entries(input.cases))for(const date of [sunday,...ferias]) {
   const d=derive(date),b=d.options[0],w=b.winner,r=request(date,key);
   assert.equal(d.options.length,1);assert.equal(b.settled,true);
   const expected=A.adaptDay({request:r,derived:d,structure:base});
   const actual=A.adaptDay({request:r,derived:d,structure:s});
   const omitted=date!==sunday;
   if(omitted){assert.equal(w.nature,'feria');assert.equal(w.formulary.kind,'borrowed');
    assert.equal(w.formulary.key,key);assert.equal(w.formulary.rule.origin,'ferial');}
   else{assert.equal(w.nature,'sunday');assert.equal(w.key,key);assert.equal(w.formulary,null);
    assert.equal(b.candidates.find(c=>c.id===w.id).rule.origin,'temporal');}
   const removed=expected.events.filter(e=>e.editionSlotLabel==='Alleluia');
   assert.equal(removed.length,1);assert.equal(removed[0].id,'proper/roman-1962/'+key+'/005');
   assert.deepEqual(actual.events,omitted?expected.events.filter(e=>e.id!==removed[0].id):expected.events);
   assert(actual.events.some(e=>e.editionSlotLabel==='Gradual'));assert.equal(condition(actual,key).length,0);
   checks.push({date,key,omitted,ids:actual.events.map(e=>e.id)});
  }
 } else if(input.mode==='unknown') {
  for(const key of Object.keys(input.cases)) {
   const result=A.adaptPropers({request:request(null,key,'propers'),structure:s});
   assert.equal(result.calendarResult,null);assert.equal(result.events.some(e=>e.editionSlotLabel==='Alleluia'),false);
   assert.equal(condition(result,key).length,1);assert(result.events.some(e=>e.editionSlotLabel==='Gradual'));
   const forged=request(null,key,'propers');
   forged.properChoices={['proper-choice/roman-1962/'+key+'/main/'+key+'-alleluia-use']:'chant-present'};
   assert.throws(()=>A.adaptPropers({request:forged,structure:s}),/not held by the exact formulary and form/);
   checks.push({key,unknown:true});
  }
 } else if(input.mode==='negatives') {
  const unused=['2026-11-30','2026-12-02','2026-12-03','2026-12-04','2026-12-07',
   '2026-12-08','2026-12-11','2026-12-21','2026-12-24'];
  for(const date of unused){const d=derive(date),b=d.options[0],advertised=year.ferial_formulary[date][0].key;
   assert(['feast','vigil-or-octave-day'].includes(b.winner.nature));
   assert.equal(b.readable.some(r=>r.key===advertised),false);
   assert.throws(()=>A.adaptDay({request:request(date,advertised),derived:d,structure:s}),/not held on this Day branch/);
   checks.push({date,advertised,notReadable:true});}
  for(const date of ['2026-12-16','2026-12-18','2026-12-19']){const d=derive(date),b=d.options[0];
   assert.equal(b.winner.nature,'feria');assert.equal(b.winner.source,'index');assert.equal(b.winner.formulary,null);
   assert.throws(()=>A.adaptDay({request:request(date,'advent-3'),derived:d,structure:s}),/not held on this Day branch/);
   checks.push({date,ownEmber:true});}
  const mutations=[
   ['missing winner',b=>{b.winner=null;}], ['missing candidate',b=>{b.candidates=[];}],
   ['unsettled',b=>{b.settled=false;}], ['missing formulary',b=>{delete b.winner.formulary;}],
   ['mismatched key',b=>{b.winner.formulary.key='advent-2';}],
   ['forged origin',b=>{b.winner.formulary.rule.origin='temporal';}],
   ...['commemorated','additional','displaced'].map(state=>[state,b=>{b.readable[0].state=state;}])];
  for(const [name,mutate] of mutations){const d=derive('2026-12-01');mutate(d.options[0]);
   let result;try{result=A.adaptDay({request:request(d.date,'advent-1'),derived:d,structure:s});}
   catch(error){assert(!['TypeError','ReferenceError','SyntaxError'].includes(error.name),name+': '+error);
    assert.match(error.message,/owner|context|winner|branch|formulary|usage|applicability|canonical|candidate|readable/i);
    checks.push({name,rejected:true});continue;}
   assert.equal(result.events.some(e=>e.editionSlotLabel==='Alleluia'),false,name);
   assert.equal(condition(result,'advent-1').length,1,name);checks.push({name,unknown:true});}
 } else if(input.mode==='contrast') {
  const date='2026-06-08',key='pentecost-2',d=derive(date),w=d.options[0].winner,r=request(date,key);
  assert.equal(w.nature,'feria');assert.equal(w.formulary.kind,'borrowed');assert.equal(w.formulary.key,key);
  const actual=A.adaptDay({request:r,derived:d,structure:s}),expected=A.adaptDay({request:r,derived:d,structure:base});
  assert.deepEqual(actual.events,expected.events);assert(actual.events.some(e=>e.editionSlotLabel==='Alleluia'));
  assert(actual.events.some(e=>e.editionSlotLabel==='Gradual'));checks.push({date,key,alleluiaRetained:true});
 } else throw new Error('unknown source-fixture test mode');
 process.stdout.write(JSON.stringify({status:'pass',checks}));
});
"""


class AdventFerialUse(unittest.TestCase):
    def node(self, mode):
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        run = subprocess.run([node, "-e", HARNESS, str(ROOT), str(MODULE_ROOT)],
                             input=json.dumps({"mode": mode, "structure": structure(), "cases": CASES}),
                             text=True, capture_output=True, check=False)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "pass")
        return result["checks"]

    def test_source_fact_and_exact_four_local_conditional_rows(self):
        fact = SOURCE["proper_appointment_facts"][FACT_ID]
        self.assertEqual(set(fact), {"edition", "values", "usage_values", "basis"})
        self.assertEqual(fact["edition"], "roman-1962")
        self.assertEqual(fact["values"], ["chant-present", "chant-omitted"])
        self.assertEqual(fact["usage_values"], {"own-sunday": "chant-present", "borrowed-feria": "chant-omitted"})
        self.assertEqual(C.validate_proper_appointment_facts({FACT_ID: fact}, "roman-1962"), {FACT_ID: fact})
        coordinates = []
        for key, mass in INDEX.items():
            for index, proper in enumerate(mass.get("propers", [])):
                rule = proper.get("ordinary_disposition", {})
                if rule.get("when", {}).get("fact") == FACT_ID:
                    coordinates.append((key, index, proper["name"]))
                    self.assertEqual(rule["kind"], "conditional")
                    self.assertEqual(rule["group"], key + "-alleluia-use")
                    self.assertEqual(rule["when"], {"fact": FACT_ID, "in": ["chant-present"]})
                    self.assertEqual(set(rule), {"kind", "group", "basis", "when"})
        self.assertEqual(sorted(coordinates), [(key, 4, "Alleluia") for key in sorted(CASES)])
        for key in CASES:
            self.assertEqual(len(INDEX[key]["propers"]), 10)
            self.assertEqual(INDEX[key]["propers"][3]["name"], "Gradual")
            self.assertNotIn("ordinary_disposition", INDEX[key]["propers"][3])
            self.assertNotIn("Tract", [p["name"] for p in INDEX[key]["propers"]])
        self.assertEqual({key: [v["ref"] for v in INDEX[key]["propers"][4].get("verses", [])]
                          for key in CASES}, {"advent-1": ["Psalm 84:8"], "advent-2": ["Psalm 121:1"],
                                             "advent-3": [], "advent-4": []})
        # Held 1962 AP86 / printed p.5 L, unit25 (before Gospel26) has
        # no printed citation. The former Psalm79:3 was an inference, removed
        # by the held-page appointment correction. Its former body gap is
        # filled by the accepted Phase 5 Latin22 body (1f1be432b; ledger and
        # missal-source-batch-20261023 latin_current_bodies).
        alleluia = INDEX["advent-3"]["propers"][4]
        self.assertEqual(alleluia["source"], "composed")
        self.assertEqual(alleluia["incipit"], "Excita, Domine, potentiam tuam")
        self.assertEqual(hashlib.sha256(alleluia["text"].encode()).hexdigest(),
                         "0188d53c71815633e8cf11e8d8a245f74e98481cafb978ebe38348733b0b3ccc")
        self.assertNotIn("text_status", alleluia)
        self.assertEqual(hashlib.sha256(INDEX["advent-4"]["propers"][4]["text"].encode()).hexdigest(),
                         "b7d6fee93fb37223387643d18c0640604e0235b2e63e5813ad8755dfff0f7240")

    def test_source_inventory_exact_units_and_retained_after_pentecost_contrast(self):
        ledger = tomllib.loads((SOURCE_ROOT / "src/sources/inventories/roman-1962-advent-ferial-chant-appointments-v1.toml").read_text())
        self.assertEqual(ledger["fact_id"], FACT_ID)
        self.assertEqual(ledger["artifact_sha256"], "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a")
        self.assertEqual([(r["mass"], r["form_id"], r["proper"], r["occurrence"], r["source_index"], r["source_unit"], r["artifact_page"])
                          for r in ledger["appointments"]], [("advent-1", "main", "Alleluia", 1, 4, 5, 83),
                          ("advent-2", "main", "Alleluia", 1, 4, 15, 84), ("advent-3", "main", "Alleluia", 1, 4, 25, 86),
                          ("advent-4", "main", "Alleluia", 1, 4, 92, 95)])
        self.assertEqual([(r["artifact_page"], r["printed_page"], r["column"]) for r in ledger["source_contrasts"]], [(459, "378", "L")])

    def test_public_fixture_keeps_body_gap_and_refuses_source_audit_shape(self):
        before = copy.deepcopy(SOURCE)
        public = structure()
        for mass in public["masses"]:
            resolved, problems = C.resolve_propers(SOURCE, INDEX[mass["key"]], appointments=True)
            self.assertEqual(problems, [])
            for row, (_, proper, _) in zip(mass["propers"], resolved, strict=True):
                for field in ("name", "source", "text", "incipit", "verses",
                              "ordinary_disposition", "appointment_identity"):
                    self.assertEqual(row.get(field), proper.get(field), (mass["key"], field))
        self.assertEqual(SOURCE, before)
        self.assertEqual(self.node("private-status"), [{"sourceAuditRefused": True}])

    def test_all_ten_reuses_omit_only_alleluia_and_four_own_sundays_retain_it(self):
        checks = self.node("annual")
        self.assertEqual(len(checks), 14)
        self.assertEqual(sum(row["omitted"] for row in checks), 10)

    def test_undated_propers_retains_unknown_usage_instead_of_default_omission(self):
        self.assertEqual(len(self.node("unknown")), 4)

    def test_unused_formularies_own_embers_and_missing_or_mismatched_owner_are_not_proof(self):
        self.assertEqual(len(self.node("negatives")), 21)

    def test_after_pentecost_borrowed_feria_keeps_alleluia(self):
        self.assertEqual(self.node("contrast"), [{"date": "2026-06-08", "key": "pentecost-2", "alleluiaRetained": True}])


if __name__ == "__main__":
    unittest.main()
