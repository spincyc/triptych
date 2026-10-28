#!/usr/bin/python3
"""Source-bounded RG 110 groups count once and retain both literal owners."""
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import subprocess
import unittest

import yaml

from test_rg110_diagnostic import ROOT, SOURCE, run_model, tool

CODE = Path(os.environ.get("TRIPTYCH_RG110_TEST_CODE", ROOT))


class Rg110Assembly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = yaml.safe_load(SOURCE.read_text())
        cls.rubrics = json.loads((ROOT / "src/web/data/structure/rubrics/roman-1962.json").read_text())
        cls.rubrics["commemoration"] = copy.deepcopy(cls.source["commemoration"])
        cls.dates = ["2027-02-22", "2028-02-22", "2060-02-22", "2027-01-25", "2026-06-30",
                     "2026-02-22", "2026-01-25", "2030-06-30", "2026-06-29", "2027-02-23"]
        cls.inputs = {date: cls.case(date) for date in cls.dates}
        cls.results = run_model(list(cls.inputs.values()))
        loader = SourceFileLoader('_rg110_mass_propers', str(CODE / 'tools/mass-propers'))
        spec = spec_from_loader(loader.name, loader)
        owner = module_from_spec(spec)
        loader.exec_module(owner)
        owner.ROOT = CODE
        cls.relations = owner.oration_relations(
            (CODE if CODE != ROOT else ROOT) / 'src/sources/calendars', 'roman-1962')

    @classmethod
    def case(cls, date, identifier=None):
        year = json.loads((ROOT / f"src/web/data/structure/calendar/roman-1962/{date[:4]}.json").read_text())
        return {"id": identifier or date, "date": date, "year": year, "rubrics": copy.deepcopy(cls.rubrics)}

    def branch(self, date):
        row = self.results[date]
        self.assertNotIn("error", row)
        branch, = row["result"]["options"]
        return branch

    def assert_group(self, date, host, companion, low_count, sung_count, position=1):
        branch = self.branch(date)
        self.assertTrue(branch["settled"], branch["unsettled"])
        self.assertEqual(len(branch["orations"]["low_mass"]), low_count)
        self.assertEqual(len(branch["orations"]["sung_non_conventual"]), sung_count)
        group = branch["orations"]["low_mass"][position - 1]
        self.assertEqual(group["count"], 1)
        self.assertEqual(group["group"], "inseparable")
        self.assertEqual([m["of"] for m in group["members"]], [host, companion])
        self.assertEqual(group["slots"], ["Collect", "Secret", "Postcommunion"])
        self.assertIn("shared by both", group["conclusion"])
        self.assertEqual(next(row for row in branch["losers"] if row["id"] == companion)["disposition"], "attached")
        self.assertFalse(any(row["of"] == companion for row in branch["orations"]["low_mass"]))
        return branch

    def test_winning_chair_keeps_paul_beside_privileged_feria_and_at_sung_mass(self):
        self.assert_group("2027-02-22", "cathedrae-s-petri-apostoli", "comm-s-pauli-apostoli", 2, 2)

    def test_winning_chair_in_septuagesima_counts_once_in_both_series(self):
        self.assert_group("2028-02-22", "cathedrae-s-petri-apostoli", "comm-s-pauli-apostoli", 1, 1)

    def test_commemorated_host_is_admitted_as_a_group_but_not_revived_sung(self):
        branch = self.assert_group("2060-02-22", "cathedrae-s-petri-apostoli", "comm-s-pauli-apostoli", 2, 1, 2)
        self.assertEqual(branch["winner"]["nature"], "sunday")
        self.assertFalse(any(row.get("members") for row in branch["orations"]["sung_non_conventual"]))

    def test_reverse_orientation_and_distinct_june_pair(self):
        self.assert_group("2027-01-25", "conversione-s-pauli-apostoli", "comm-s-petri-apostoli", 1, 1)
        self.assert_group("2026-06-30", "commemoratione-s-pauli-apostoli", "comm-s-petri-apostoli-2", 1, 1)

    def test_omitted_hosts_do_not_acquire_companions(self):
        for date in ["2026-02-22", "2026-01-25", "2030-06-30"]:
            with self.subTest(date=date):
                branch = self.branch(date)
                self.assertTrue(branch["settled"])
                self.assertEqual({one["disposition"] for one in branch["losers"]}, {"omitted"})
                self.assertFalse(any(row.get("members") for row in branch["orations"]["low_mass"]))

    def test_joint_feast_and_unrelated_day_are_wholly_unchanged(self):
        for date in ["2026-06-29", "2027-02-23"]:
            control = copy.deepcopy(self.inputs[date])
            control["rubrics"]["commemoration"].pop("inseparable")
            self.assertEqual(self.results[date], run_model([control])[date])

    def test_orphan_cannot_manufacture_a_host_and_prior_refusal_remains_authoritative(self):
        orphan = self.case("2027-01-25", "orphan")
        orphan["year"]["days"][orphan["date"]] = [row for row in orphan["year"]["days"][orphan["date"]]
                                                       if row["key"] != "conversione-s-pauli-apostoli"]
        prior = self.case("2027-02-22", "prior")
        prior["rubrics"]["unsettled"].append({"what": "prior source refusal", "why": "unresolved occurrence",
            "scope": "occurrence", "when": {"candidate_key": "cathedrae-s-petri-apostoli"}})
        for identifier, got in run_model([orphan, prior]).items():
            branch, = got["result"]["options"]
            self.assertFalse(branch["settled"])
            self.assertIsNone(branch["winner"])
            self.assertEqual(branch["orations"], {"low_mass": [], "sung_non_conventual": []})
            if identifier == "prior": self.assertEqual([r["what"] for r in branch["unsettled"]], ["prior source refusal"])

    def test_source_and_runtime_reject_unknown_or_unsupported_execution(self):
        masses = tool.load_masses(ROOT / "src/sources/calendars", "roman-1962")
        self.assertEqual(tool.check_inseparable(self.source, masses, "fixture"), [])
        mutations = [lambda r: r["execution"].update(count=2),
                     lambda r: r.update(applied=False),
                     lambda r: r.update(applied="true"),
                     lambda r: r.update(applied="unknown"),
                     lambda r: r["execution"].update(count=True),
                     lambda r: r["execution"].update(scope="ritual"),
                     lambda r: r["execution"].update(slots=["Collect"]),
                     lambda r: r["pairs"][0].update(host="unknown"),
                     lambda r: r["pairs"][0].update(companion="cathedrae-s-petri-apostoli")]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                source = copy.deepcopy(self.source)
                mutate(source["commemoration"]["inseparable"])
                self.assertTrue(tool.check_inseparable(source, masses, "fixture"))
                case = self.case("2027-02-22", str(index))
                case["rubrics"]["commemoration"] = source["commemoration"]
                self.assertIn("error", run_model([case])[str(index)])

    def test_propers_relations_are_emitted_only_from_exact_source_pairs(self):
        pairs = self.source['commemoration']['inseparable']['pairs']
        self.assertEqual(set(self.relations), {p[k] for p in pairs for k in ['host', 'companion']})
        for pair in pairs:
            for key in ['host', 'companion']:
                self.assertEqual(self.relations[pair[key]], {**pair, 'scope': 'dated-mass-of-office',
                    'slots': ['Collect', 'Secret', 'Postcommunion']})

    def test_missing_principal_or_companion_slot_refuses_instead_of_losing_a_group_member(self):
        harness = r"""
const fs=require('fs'), root=process.argv[1], code=process.argv[2];
const A=require(code+'/src/web/browser/liturgy/reader-state-adapters.js');
const fixture=JSON.parse(fs.readFileSync(root+'/tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json'));
let raw='';process.stdin.on('data',s=>raw+=s);process.stdin.on('end',()=>{
 const derived=JSON.parse(raw), results=[];
 for(const key of ['cathedrae-s-petri-apostoli','comm-s-pauli-apostoli']) {
  const structure=JSON.parse(fs.readFileSync(root+'/src/web/data/structure/propers/roman-1962.json'));
  const mass=structure.masses.find(m=>m.key===key);mass.propers=mass.propers.filter(p=>p.name!=='Collect');
  const request=JSON.parse(JSON.stringify(fixture.requested));delete request.selectedReadableFormulary;request.civilDate=derived.date;
  try{A.adaptDay({request,derived,structure});results.push(false);}catch(error){results.push(/inseparable/.test(String(error)) || ['principal-oration-slot-unbound','oration-source-slot-unbound'].includes(error.code));}
 }
 process.stdout.write(JSON.stringify(results));
});
"""
        done = subprocess.run(['node','-e',harness,str(ROOT.resolve()),str(CODE.resolve())],
            input=json.dumps(self.results['2027-02-22']['result']),capture_output=True,text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(json.loads(done.stdout), [True, True])

    def test_direct_propers_preserves_raw_bodies_and_exposes_source_qualified_unknown_use(self):
        harness = r"""
const fs=require('fs'),vm=require('vm'),root=process.argv[1],code=process.argv[2],relations=JSON.parse(process.argv[3]);
const A=require(code+'/src/web/browser/liturgy/reader-state-adapters.js');
const dom=require(root+'/scripts/lectern/dom.js');globalThis.window=globalThis;globalThis.document=dom.document;
globalThis.location={search:''};globalThis.addEventListener=()=>{};
vm.runInThisContext(fs.readFileSync(code+'/src/web/browser/shared/browser-core.js','utf8'));
const structure=JSON.parse(fs.readFileSync(root+'/src/web/data/structure/propers/roman-1962.json'));
const ordinary=JSON.parse(fs.readFileSync(root+'/src/web/data/structure/ordinary/roman-1962.json'));
const fixture=JSON.parse(fs.readFileSync(root+'/tools/tests/fixtures/liturgy-reader-state/v1/propers-roman-1962-advent-1.json'));
for(const mass of structure.masses)if(relations[mass.key])mass.oration_relation=relations[mass.key];
const results=[];
for(const key of Object.keys(relations))for(const mode of ['read','missal','study']){
 const mass=structure.masses.find(m=>m.key===key),request=JSON.parse(JSON.stringify(fixture.requested));
 request.formulary={id:key,type:mass.kind};request.requestedMode=mode;request.options.ordinary=mode==='missal';
 if(mode==='missal')request.languages.ordinary='la';
 const result=A.adaptPropers({request,structure,ordinary:mode==='missal'?ordinary:null});
 const prayers=result.events.filter(e=>e.orationContext);
 const rendered=prayers.map(event=>{
  const proper=mass.propers.find(p=>p.name===event.editionSlotLabel);
  const section=Triptych.renderProper(proper,null,null,{orations:'la',orationContext:event.orationContext});
  return {holds:section.querySelectorAll('.inseparable-oration-context').length,groups:section.querySelectorAll('.inseparable-oration-group').length,
   text:dom.read(section).flatMap(b=>b.runs.map(r=>r.text)).join(' ')};
 });
 results.push({key,mode,prayers:prayers.length,unchanged:prayers.every(e=>e.selected.text===(mass.propers.find(p=>p.name===e.editionSlotLabel).text||null)),
  noAttachment:result.events.every(e=>!e.orationGroups),rendered,
  hold:result.explicitAbsences.some(a=>a.scope==='inseparable-oration-assembly'),
  unsupported:result.coverage.some(c=>c.scope==='inseparable-oration-assembly'&&c.state==='unsupported')});
}
process.stdout.write(JSON.stringify(results));
"""
        done = subprocess.run(['node', '-e', harness, str(ROOT.resolve()), str(CODE.resolve()), json.dumps(self.relations)],
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        for report in json.loads(done.stdout):
            with self.subTest(key=report['key'], mode=report['mode']):
                self.assertEqual(report['prayers'], 3)
                self.assertTrue(report['unchanged'] and report['noAttachment'] and report['hold'] and report['unsupported'])
                self.assertTrue(all(r['holds'] == 1 and r['groups'] == 0 and 'does not establish Office or votive use' in r['text'] for r in report['rendered']))

    def test_read_and_missal_keep_every_member_exact_and_do_not_fill_english_or_latin_holds(self):
        harness = r"""
const fs = require('fs'), vm = require('vm');
const root = process.argv[1], code = process.argv[2];
const A = require(code + '/src/web/browser/liturgy/reader-state-adapters.js');
const dom = require(root + '/scripts/lectern/dom.js');
globalThis.window = globalThis; globalThis.document = dom.document;
globalThis.location = { search: '' }; globalThis.addEventListener = () => {};
vm.runInThisContext(fs.readFileSync(code + '/src/web/browser/shared/browser-core.js', 'utf8'));
const structure = JSON.parse(fs.readFileSync(root + '/src/web/data/structure/propers/roman-1962.json'));
const ordinary = JSON.parse(fs.readFileSync(root + '/src/web/data/structure/ordinary/roman-1962.json'));
const fixture = JSON.parse(fs.readFileSync(root + '/tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json'));
let raw = ''; process.stdin.on('data', s => raw += s); process.stdin.on('end', () => {
  const reports = [];
  for (const derived of JSON.parse(raw)) for (const mode of ['read', 'missal']) for (const lang of ['la', 'en']) {
    const request = JSON.parse(JSON.stringify(fixture.requested));
    delete request.selectedReadableFormulary;
    request.civilDate = derived.date; request.requestedMode = mode;
    request.languages.orations = lang; request.options.ordinary = mode === 'missal';
    if (mode === 'missal') request.languages.ordinary = 'la';
    const result = A.adaptDay({request, derived, structure, ordinary: mode === 'missal' ? ordinary : null});
    const mass = structure.masses.find(m => m.key === result.resolved.formulary);
    const grouped = result.events.filter(e => e.orationGroups?.some(g => g.kind === 'inseparable')).map(e => ({...e, orationGroups: e.orationGroups.filter(g => g.kind === 'inseparable')}));
    const members = grouped.flatMap(e => e.orationGroups.flatMap(g => g.members));
    const exact = members.every(e => {
      const hook = e.sourceHooks.find(h => h.kind === 'proper-structure');
      const owner = structure.masses.find(m => hook.id.slice(0, hook.id.lastIndexOf('/')) === structure.calendar + '/' + m.key);
      const proper = owner.propers[Number(hook.id.slice(hook.id.lastIndexOf('/') + 1)) - 1];
      const text = lang === 'la' ? proper.text : (proper.translations || []).length === 1 ? proper.translations[0].text : null;
      return (e.selected.text || null) === (text || null);
    });
    const renderings = grouped.map(e => {
      const hook = e.sourceHooks.find(h => h.kind === 'proper-structure');
      const proper = mass.propers[Number(hook.id.slice(hook.id.lastIndexOf('/') + 1)) - 1];
      const section = Triptych.renderProper(proper, null, null, {orations: lang,
        orationGroups: e.orationGroups, eventId: e.id, structure});
      const text = dom.read(section).flatMap(b => b.runs.map(r => r.text)).join(' ').replace(/\s+/g, ' ');
      return {notes: section.querySelectorAll('.inseparable-oration-note').length,
        membersPresent: e.orationGroups.every(g => g.members.every(m => !m.selected.text || text.includes(m.selected.text.replace(/\s+/g, ' ').trim())))};
    });
    reports.push({date: derived.date, mode, lang, exact, grouped: grouped.length,
      memberCount: members.length, renderings,
      unavailable: members.filter(e => e.selected.availability === 'unavailable').length,
      coverage: Triptych.selectedCoverageUnits(result, structure).length,
      originalEvents: result.events.filter(e => e.kind === 'proper').length});
  }
  process.stdout.write(JSON.stringify(reports));
});
"""
        dates = ["2027-02-22", "2027-01-25", "2026-06-30", "2060-02-22"]
        done = subprocess.run(["node", "-e", harness, str(ROOT.resolve()), str(CODE.resolve())],
                              input=json.dumps([self.results[d]["result"] for d in dates]),
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        for report in json.loads(done.stdout):
            with self.subTest(date=report["date"], mode=report["mode"], lang=report["lang"]):
                self.assertTrue(report["exact"])
                self.assertEqual(report["grouped"], 3)
                self.assertEqual(report["memberCount"], 6)
                self.assertTrue(all(r["notes"] == 1 and r["membersPresent"] for r in report["renderings"]))
                self.assertGreaterEqual(report["coverage"], report["originalEvents"] + 3)
                if report["lang"] == "en" and report["date"] != "2060-02-22":
                    self.assertGreaterEqual(report["unavailable"], 3)

    def test_actual_lectern_bridge_consumes_the_same_group_in_read_missal_and_study(self):
        # The optional module root lets pre-admission review run the real bridge
        # with proposed code and source, while retaining canonical filenames.
        preload = r"""
const fs = require('fs'), path = require('path'), Module = require('module');
const root = process.argv[1], code = process.argv[2], rubrics = JSON.parse(process.argv[3]), relations = JSON.parse(process.argv[4]);
const read = fs.readFileSync, extension = Module._extensions['.js'];
function proposed(file) {
  if (typeof file !== 'string' || !file.startsWith(root + path.sep)) return file;
  const candidate = path.join(code, path.relative(root, file));
  return code !== root && fs.existsSync(candidate) && fs.statSync(candidate).isFile() ? candidate : file;
}
Module._extensions['.js'] = (mod, file) => {
  const candidate = proposed(file);
  if (candidate === file) return extension(mod, file);
  mod._compile(read(candidate, 'utf8'), file);
};
fs.readFileSync = function(file, options) {
  if (file === path.join(root, 'src/web/data/structure/rubrics/roman-1962.json')) {
    const body = JSON.stringify(rubrics);
    return typeof options === 'string' || options && options.encoding ? body : Buffer.from(body);
  }
  if (file === path.join(root, 'src/web/data/structure/propers/roman-1962.json')) {
    const structure = JSON.parse(read(file, 'utf8'));
    structure.masses.forEach(mass => { if (relations[mass.key]) mass.oration_relation = relations[mass.key]; });
    const body = JSON.stringify(structure);
    return typeof options === 'string' || options && options.encoding ? body : Buffer.from(body);
  }
  return read(proposed(file), options);
};
require(root + '/scripts/lectern/bridge.js');
"""
        commands = [
            {"id": "read", "adapter": "liturgy", "fn": "day", "args": ["roman-1962", "2027-02-22", {"orations": "la"}]},
            {"id": "missal", "adapter": "liturgy", "fn": "day", "args": ["roman-1962", "2027-02-22", {"orations": "la", "ordinary": True, "ordinaryLang": "la"}]},
            {"id": "english", "adapter": "liturgy", "fn": "day", "args": ["roman-1962", "2027-02-22", {"orations": "en"}]},
            {"id": "study", "adapter": "liturgy", "fn": "studyDay", "args": ["roman-1962", "2027-02-22", {"orations": "la"}]},
            {"id": "propers", "adapter": "liturgy", "fn": "propers", "args": ["roman-1962", "cathedrae-s-petri-apostoli", {"orations": "la", "ordinary": True, "ordinaryLang": "la"}]},
            {"id": "propers-study", "adapter": "liturgy", "fn": "studyPropers", "args": ["roman-1962", "cathedrae-s-petri-apostoli", {"orations": "la"}]},
        ]
        done = subprocess.run(["node", "-e", preload, str(ROOT.resolve()), str(CODE.resolve()), json.dumps(self.rubrics), json.dumps(self.relations)],
                              input="\n".join(json.dumps(command) for command in commands) + "\n",
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        replies = {row["id"]: row for row in map(json.loads, done.stdout.splitlines())}
        for identifier, reply in replies.items():
            self.assertTrue(reply["ok"], (identifier, reply.get("error")))
        def words(blocks):
            return " ".join(run["text"] for block in blocks for run in block["runs"])
        for identifier in ["read", "missal", "english"]:
            row, = replies[identifier]["value"]["rows"]
            prayers = [event for event in row["events"] if event.get("slot") in {"Collect", "Secret", "Postcommunion"}]
            self.assertEqual(len(prayers), 3)
            for prayer in prayers:
                text = words(prayer["blocks"])
                self.assertEqual(text.count("These two prayers count as one"), 1)
                if identifier != "english": self.assertIn("Pauli", text)
            self.assertTrue(row["branch"]["settled"])
        study = words(replies["study"]["value"][0]["blocks"])
        self.assertIn("two inseparable prayers count as one", study)
        direct = replies['propers']['value']
        self.assertTrue(any(a['scope'] == 'inseparable-oration-assembly' for a in direct['explicitAbsences']))
        for prayer in [e for e in direct['events'] if e.get('slot') in {'Collect', 'Secret', 'Postcommunion'}]:
            self.assertIn('does not establish Office or votive use', words(prayer['blocks']))
            self.assertNotIn('These two prayers count as one', words(prayer['blocks']))
        self.assertIn('Unresolved prayer assembly', words(replies['propers-study']['value']))


if __name__ == "__main__":
    unittest.main()
