"""Direct CLI presentation consumes the actual shared ending/display result.

Generated source fixtures are selected only through the normal test data helper.
The test does not replace production source admission or verified-products gates.
"""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / "tools/tests"))
from _mass_today_native_fixture import load_today
from _product_data import browser_data_root

FIXTURE_SCRIPT = r"""const fs=require('fs'),assert=require('assert');
const C=require(process.argv[1]);
const structure=JSON.parse(fs.readFileSync(process.argv[2]));
const targets=[
 {kind:'display',target:['commune-unius-martyris-3','main','Postcommunion','all',1]},
 {kind:'display',target:['comm-s-mennae-martyris','main','Postcommunion','all',1]},
 {kind:'display',target:['s-matthiae-apostoli','main','Secret','all',1]},
 {kind:'own-witness-42',target:['advent-2','main','Collect','all',1]},
 {kind:'mixed-witness-50',target:['advent-ember-friday','main','Secret','all',1]},
 {kind:'roman-study-3',target:['beatae-mariae-virginis-reginae','main','Secret','all',1]},
 {kind:'osp-existing-34',target:['ash-wednesday','main','Oratio super populum','all',1]},
 {kind:'nativity-day-3',target:['nativitate-domini-octave','day','Collect','all',1]},
];
const cases=[];
for(const wanted of targets){
 const mass=structure.masses.find(m=>m.key===wanted.target[0]);
 const index=mass.propers.findIndex(p=>(p.conclusion_execution||[]).some(s=>C.canonical(s.target)===C.canonical(wanted.target)));
 assert(index>=0,wanted.target.join('/'));
 const proper=mass.propers[index],source=proper.conclusion_execution[0];
 for(const language of Object.keys(source.languages)){
  if(wanted.kind==='display'&&language!=='en')continue;
  const text=language==='la'?proper.text:proper.translations.find(t=>t.lang==='en'&&(t.source_id||'')===source.source_id).text;
  const member={id:`proper/roman-1962/${mass.key}/${String(index+1).padStart(3,'0')}`,target:source.target,source,text,language,witness:language==='en'?(source.source_id||null):null};
  for(const final of wanted.kind==='display'?[true,false]:[true]){
   let projected,scope;
   if(wanted.kind==='osp-existing-34'){
    const expected=source.context;
    projected=C.executeProperRite({calendar:'roman-1962',member,rite:{id:expected.rite_id,semanticRole:expected.semantic_role,ownConclusion:true,locus:expected.rite_locus,appointmentLocus:expected.appointment_locus,appointment:{mass:source.target[0],form_id:source.target[1],proper:source.target[2],occurrence:source.target[4]},sourceIndex:expected.source_index}});scope='proper-rite';
   }else{
    const groups=final?[{kind:'principal',position:1,conclusion_group:1,conclusion_final:true,slot:source.target[2],members:[member]}]:[{kind:'commemoration',position:2,conclusion_group:2,conclusion_final:false,slot:source.target[2],members:[member]},{kind:'commemoration',position:3,conclusion_group:2,conclusion_final:true,slot:source.target[2],members:[{...member,id:member.id+'/next'}]}];
    projected=C.executeDisplayGroup({calendar:'roman-1962',rule:C.GROUP_RULE,groups});
   }
   assert.equal(projected.state,'source-derived-complete',wanted.kind);
   const value=projected.members.find(m=>m.id===member.id);
   cases.push({kind:wanted.kind,language,final,proper,conclusion:{state:projected.state,execution_extent:projected.execution_extent,member:value,response:projected.response.provider_id===member.id?projected.response:null,...(scope?{scope}:{})}});
  }
 }
}
process.stdout.write(JSON.stringify(cases));
"""


class MassTodayConclusionPresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.today = load_today()
        helper = os.environ.get("TRIPTYCH_REVIEW_CONCLUSION_HELPER", str(ROOT / "src/web/browser/liturgy/oration-conclusions.js"))
        structure = browser_data_root(ROOT) / "structure/propers/roman-1962.json"
        result = subprocess.run(["node", "-e", FIXTURE_SCRIPT, helper, str(structure)],
                                cwd=ROOT, capture_output=True, text=True, check=True)
        cls.cases = json.loads(result.stdout)
        assert len(cls.cases) == 16

    def render(self, case, witness=None):
        return "\n".join(self.today.proper_lines(case["proper"], self.today.Style(), "  ",
            lang=case["language"], witness=witness, seat=None, why=False, conclusion=case["conclusion"]))

    @staticmethod
    def folded(value):
        return " ".join(value.split())

    def test_actual_display_and_source_qualifications(self):
        for case in self.cases:
            with self.subTest(kind=case["kind"], lang=case["language"], final=case["final"]):
                before = copy.deepcopy(case)
                member = case["conclusion"]["member"]
                marker = "Source quotation:" if "qualification" in member else "Source quotation and ending cue:"
                rendered = self.render(case)
                reading, quotation = rendered.split(marker, 1)
                if "qualification" in member:
                    self.assertNotIn("Source quotation and ending cue:", rendered)
                self.assertIn(self.folded(member["source_text"]), self.folded(quotation))
                self.assertIn(self.folded(member.get("display_text", member["priest_text"])), self.folded(reading))
                self.assertEqual(reading.count("R. Amen."), 1 if case["final"] else 0)
                if "qualification" in member:
                    self.assertIn(self.folded(member["qualification"]), self.folded(reading))
                if member.get("display_correction"):
                    self.assertIn(self.folded(member["display_correction"]["annotation"]), self.folded(reading))
                self.assertEqual(case, before)

    def test_unknown_qualifications_and_partial_display_refuse(self):
        new = next(case for case in self.cases if "qualification" in case["conclusion"]["member"])
        old = next(case for case in self.cases if case["kind"] == "display")
        mutations = {
            "missing-qualification": lambda member: member.pop("qualification"),
            "empty-qualification": lambda member: member.update(qualification=" "),
            "object-qualification": lambda member: member.update(qualification={}),
            "missing-fidelity": lambda member: member.pop("body_fidelity"),
            "array-fidelity": lambda member: member.update(body_fidelity=[]),
            "unknown-source-method": lambda member: member.update(source_method="unsupported"),
            "array-source-method": lambda member: member.update(source_method=[]),
            "missing-source-method": lambda member: member.pop("source_method"),
            "qualified-old-method": lambda member: member.update(source_method="roman-1962-rg115-conclusion-execution-20261112"),
            "changed-quotation": lambda member: member.update(source_text=member["source_text"] + " drift"),
        }
        for label, mutate in mutations.items():
            with self.subTest(control=label):
                case = copy.deepcopy(new)
                mutate(case["conclusion"]["member"])
                with self.assertRaises(self.today.Refused):
                    self.render(case)
        for field in ("display_text", "annotation"):
            with self.subTest(control="missing-" + field):
                case = copy.deepcopy(old)
                member = case["conclusion"]["member"]
                (member if field == "display_text" else member["display_correction"]).pop(field)
                with self.assertRaises(self.today.Refused):
                    self.render(case)
        case = copy.deepcopy(new)
        case["conclusion"]["execution_extent"]["method_id"] = "roman-1962-rg115-conclusion-execution-20261112"
        with self.assertRaises(self.today.Refused):
            self.render(case)

    def test_mixed_old_member_and_source_structure_remain_qualified(self):
        old = next(case for case in self.cases if case["kind"] == "display")
        case = copy.deepcopy(old)
        case["conclusion"]["execution_extent"]["method_id"] = "missal-finite-oration-conclusion-execution-20261112-v2"
        case["conclusion"]["member"]["source_method"] = "roman-1962-rg115-conclusion-execution-20261112"
        self.assertIn("Source-derived English for study;", self.render(case))
        case = copy.deepcopy(old)
        member = case["conclusion"]["member"]
        for row in case["proper"]["translations"]:
            if row.get("lang") == "en" and row.get("text") == member["source_text"]:
                row["text_structure"] = {"stanzas": [], "actions": []}
        text = self.render(case).split("Source quotation and ending cue:", 1)[0]
        self.assertIn(self.folded(member["priest_text"]), self.folded(text))
        self.assertIn("Editorial correction unavailable", text)
        case = copy.deepcopy(old)
        member = case["conclusion"]["member"]
        selected = next(row for row in case["proper"]["translations"]
                        if row.get("lang") == "en" and row.get("text") == member["source_text"])
        foreign = copy.deepcopy(selected)
        foreign.update(source_id="edition.unselected", text_structure={"stanzas": [], "actions": []})
        case["proper"]["translations"].insert(0, foreign)
        self.assertIn("Editorial reading with sourced conclusion", self.render(case, selected["source_id"]))


if __name__ == "__main__":
    unittest.main()
