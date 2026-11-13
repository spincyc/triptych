"""Actual dated groups use sourced conclusions atomically in both readers."""
import json
import subprocess
import unittest
from pathlib import Path

from tools.tests._product_data import browser_data_root

ROOT = Path(__file__).resolve().parents[2]


class OrationConclusionReaderTests(unittest.TestCase):
    def test_actual_group_projection_and_intermediate_drift(self):
        script = r"""
const fs=require('fs'),assert=require('assert/strict'),path=require('path');
const A=require('./src/web/browser/liturgy/reader-state-adapters'),M=require('./src/web/browser/liturgy/assembly-model');
const data=process.argv[1],read=p=>JSON.parse(fs.readFileSync(path.join(data,p)));
const structure=read('structure/propers/roman-1962.json'),rubrics=read('structure/rubrics/roman-1962.json'),year=read('structure/calendar/roman-1962/2026.json');
assert.ok(structure.masses.some(m=>m.propers.some(p=>p.conclusion_execution?.length)), 'prepare activated conclusion products');
function project(date,language,owner=structure){
 const request={schema:'triptych-liturgy-reader-state/v1',entrance:'day',civilDate:date,edition:{id:'roman-1962'},calendar:{id:'roman-1962'},
 bible:{id:'douay-rheims',numbering:'vulgate'},languages:{orations:language},requestedMode:'read',options:{ordinary:false,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
 return A.adaptDay({request,derived:M.derive({date,rubrics,year}),structure:owner,rubrics});
}
for(const language of ['en','la']){
 const positive=project('2026-03-27',language),event=positive.events.find(e=>e.editionSlotLabel==='Postcommunion');
 const group=event.conclusionGroups.find(g=>g.conclusion_group===2).languages[language];
 assert.equal(group.state,'source-derived-complete');assert.deepEqual(group.members.map(m=>m.role),['petition','conclusion-provider']);
 assert.equal(group.response.provider_id,group.members[1].id);
 assert.equal(event.orationGroups.filter(g=>g.conclusion_group===2).flatMap(g=>g.execution.unresolved).length,0);
 const negative=project('2026-01-19',language).events.find(e=>e.editionSlotLabel==='Postcommunion');
 assert.equal(negative.conclusionGroups.find(g=>g.conclusion_group===2).languages[language].state,'unresolved');
 assert.ok(negative.orationGroups.filter(g=>g.conclusion_group===2).every(g=>g.members.every(m=>!m.conclusionExecution)));
 const changed=structuredClone(structure),first=changed.masses.find(m=>m.key==='s-ioannis-damasceni-confessoris-ecclesiae-doctoris').propers.find(p=>p.name==='Postcommunion');
 if(language==='la')first.text+=' ';else first.translations.find(t=>t.lang==='en').text+=' ';
 const refused=project('2026-03-27',language,changed).events.find(e=>e.editionSlotLabel==='Postcommunion');
 assert.equal(refused.conclusionGroups.find(g=>g.conclusion_group===2).languages[language].state,'unresolved');
 assert.ok(refused.orationGroups.filter(g=>g.conclusion_group===2).every(g=>!g.members[0].conclusionExecution?.languages[language]));
}
console.log('PASS source-owned groups and changed-intermediate refusal');
"""
        done = subprocess.run(["node", "-e", script, str(browser_data_root(ROOT))], cwd=ROOT,
                              capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)

    def test_terminal_uses_the_same_derived_text_and_separate_response(self):
        requests = [{"id": index, "adapter": "liturgy", "fn": "day", "args": [
            "roman-1962", "2026-03-27", {"orations": language, "mass": "passion-friday"}]} for index, language in enumerate(("en", "la"))]
        done = subprocess.run(["node", str(ROOT / "scripts/lectern/bridge.js"), str(browser_data_root(ROOT))],
            input="".join(json.dumps(row) + "\n" for row in requests), capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        for line in done.stdout.splitlines():
            reply = json.loads(line)
            self.assertTrue(reply["ok"], reply)
            event = next(row for row in reply["value"]["rows"][0]["events"] if row.get("slot") == "Postcommunion")
            blocks = event["blocks"]
            self.assertTrue(any("conclusion-execution" in block["classes"] for block in blocks))
            self.assertTrue(any("conclusion-response" in block["classes"] for block in blocks))
            self.assertTrue(any("conclusion-source-quotation" in block["classes"] for block in blocks))

    def test_terminal_requires_the_same_authorized_mass_choice(self):
        requests = [{"id": index, "adapter": "liturgy", "fn": "day", "args": [
            "roman-1962", "2026-03-27", {"orations": "en", **options}]} for index, options in enumerate((
                {}, {"mass": "s-ioannis-damasceni-confessoris-ecclesiae-doctoris"}))]
        done = subprocess.run(["node", str(ROOT / "scripts/lectern/bridge.js"), str(browser_data_root(ROOT))],
            input="".join(json.dumps(row) + "\n" for row in requests), capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        for line in done.stdout.splitlines():
            reply = json.loads(line)
            self.assertTrue(reply["ok"], reply)
            row = reply["value"]["rows"][0]
            self.assertIsNone(row["resolved"])
            self.assertIsNone(row["mass"])
            self.assertEqual(row["events"], [])
            self.assertEqual(row["primaryDayChoice"], "seven-sorrows-where-devotions-are-held")
            choice = next(item for item in row["unresolvedChoices"] if item["id"] == row["primaryDayChoice"])
            self.assertEqual([item["id"] for item in choice["options"]], [
                "passion-friday", "comm-septem-dolorum-beatae-mariae-virginis"])
