"""An explicit IGMR 363 prayer source never replaces weekday readings."""

import copy
import json
import os
import subprocess
import sys
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
rubrics = SourceFileLoader("weekday_rubrics", str(ROOT / "tools/calendar-rubrics")).load_module()
days = SourceFileLoader("weekday_days", str(ROOT / "tools/calendar-days")).load_module()
today = SourceFileLoader("weekday_today", str(ROOT / "tools/mass-today")).load_module()


class WeekdayOrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        built, problems, cls.sources = rubrics.build(rubrics.DEFAULT_ROOT, "postconciliar")
        if problems:
            raise AssertionError(problems)
        cls.rubrics = built[0]
        index = days.load_calendar(rubrics.DEFAULT_ROOT, "postconciliar")
        years = days.build_years(index, [2026, 2027])
        days.with_fixed(index, [2026])
        cls.year = days.year_document(index, 2026, years)
        document = rubrics._calendars.load_document(rubrics.DEFAULT_ROOT, "postconciliar", effective=True)
        cls.structure = {"calendar": "postconciliar", "masses": [mass
            for section in document["sections"].values() for mass in section.get("masses", [])]}

    def model(self, script):
        harness = "const assert=require('assert/strict'),m=require(process.argv[1]);let raw='';process.stdin.on('data',c=>raw+=c);process.stdin.on('end',()=>{const i=JSON.parse(raw);" + script + "});"
        result = subprocess.run(["node", "-e", harness, str(rubrics.MODEL)],
            input=json.dumps({"year": self.year, "rubrics": self.rubrics, "structure": self.structure}),
            text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_explicit_source_resolves_only_prayers_without_mutating_default(self):
        self.model("""
          const derived=m.derive({...i,date:'2026-01-12'}), before=JSON.stringify(derived);
          const choices=m.weekdayOrationChoices({...i,derived});
          assert.equal(derived.options[0].settled,false);
          assert.equal(choices.mass,'ot-1-monday');assert.equal(choices.complete,false);
          assert.equal(choices.options.length,32);
          assert.deepEqual(choices.unavailable.map(r=>r.id),['ot-1','ot-34','various-needs','collect-only']);
          const selected=m.selectWeekdayOrations({...i,derived,owner:'ot-2'});
          assert.equal(JSON.stringify(derived),before);
          assert.equal(selected.derived.options[0].settled,true);
          assert.equal(selected.derived.options[0].winner.key,'ot-1-monday');
          assert.equal(selected.derived.options[0].orations.all[0].source_key,'ot-2');
          assert.deepEqual(selected.derived.liturgicalYear.lectionary,derived.liturgicalYear.lectionary);
          assert.equal(m.weekdayOrationChoices({...i,derived:selected.derived}).options.length,32);
          assert.equal(m.selectWeekdayOrations({...i,derived:selected.derived,owner:'ot-3'}).selection.owner,'ot-3');
        """)

    def test_permission_never_applies_to_feast_sunday_other_season_or_bad_owner(self):
        self.model("""
          for(const date of ['2026-01-11','2026-02-02','2026-02-19','2026-04-06']) {
            const derived=m.derive({...i,date});
            assert.equal(m.weekdayOrationChoices({...i,derived}),null,date);
            assert.throws(()=>m.selectWeekdayOrations({...i,derived,owner:'ot-2'}));
          }
          const derived=m.derive({...i,date:'2026-01-12'});
          for(const owner of ['ot-1','ot-34','lent-1','saint-agnes-virgin-martyr',''])
            assert.throws(()=>m.selectWeekdayOrations({...i,derived,owner}));
          const bad=JSON.parse(JSON.stringify(derived));bad.options[0].unsettled.push({scope:'another-gap'});
          assert.equal(m.weekdayOrationChoices({...i,derived:bad}),null);
        """)

    def test_optional_memorial_requires_explicit_weekday(self):
        self.model("""
          const derived=m.derive({...i,date:'2026-07-20'});
          assert.equal(derived.options[0].choiceRequired,true);
          assert.equal(m.weekdayOrationChoices({...i,derived}),null);
          const result=m.selectWeekdayOrations({...i,derived,mass:'ot-16-monday',owner:'ot-3'});
          assert.equal(result.derived.options[0].choiceRequired,true);
          assert.equal(result.derived.options[0].winner,null);
          assert.equal(result.selection.mass,'ot-16-monday');
          assert.throws(()=>m.selectWeekdayOrations({...i,derived,mass:'saint-apollinaris-bishop-martyr',owner:'ot-3'}));
        """)

    def test_every_held_owner_preserves_each_ordinary_time_weekday_sequence(self):
        self.model("""
          const A=require(process.argv[1].replace('assembly-model.js','reader-state-adapters.js'));
          const derived=m.derive({...i,date:'2026-01-12'}),choices=m.weekdayOrationChoices({...i,derived});
          const weekdays=i.structure.masses.filter(row=>/^ot-\\d+-(monday|tuesday|wednesday|thursday|friday|saturday)$/.test(row.key));
          assert.equal(weekdays.length,204);
          for(const mass of weekdays) for(const owner of choices.options) {
            const sourceRows=mass.propers.map((proper,sourceIndex)=>({proper,sourceIndex}));
            let rows;try { rows=A.weekdayOrationRows(mass,sourceRows,i.structure,{mass:mass.key,owner:owner.id,slots:choices.slots}); }
            catch(error) { throw new Error(mass.key+' / '+owner.id+': '+error.message); }
            assert.deepEqual(rows.filter(row=>row.sourceMass===mass.key).map(row=>row.proper),mass.propers);
            assert.equal(rows.filter(row=>row.sourceMass===owner.id).length,3);
          }
        """)

    def test_source_validator_rejects_wrong_season_or_stale_unavailable_owner(self):
        source = copy.deepcopy(self.sources["postconciliar"])
        masses = rubrics.load_masses(rubrics.DEFAULT_ROOT, "postconciliar")
        assigned, _ = rubrics.assign(source, masses, "fixture")
        scope = next(row for row in source["implied"] if row["id"] == "ordinary-time-weekday")["appointed_mass"]["oration_scope"]
        scope["selection"]["season"] = "lent"
        self.assertTrue(rubrics.check_weekday_oration_selection(source, masses, assigned, "fixture"))
        scope["selection"]["season"] = "ordinary-time"
        scope["selection"]["unavailable"][0]["id"] = "ot-2"
        self.assertTrue(rubrics.check_weekday_oration_selection(source, masses, assigned, "fixture"))

    def test_cli_join_and_event_ids_preserve_exact_prayer_and_reading_owners(self):
        held = {mass["key"]: mass for mass in self.structure["masses"]}
        weekday = copy.deepcopy(held["ot-1-monday"]["propers"])
        sunday = copy.deepcopy(held["ot-2"]["propers"])
        mass = today._SourceMass({"key": "ot-1-monday", "propers": weekday,
                                  "_proper_source_indices": list(range(len(weekday)))})
        mass._ordinary_source_rows = [{"proper": row, "sourceIndex": index} for index, row in enumerate(weekday)]
        owner = {"propers": sunday, "_proper_source_indices": list(range(len(sunday))),
                 "_ordinary_source_rows": [{"proper": row, "sourceIndex": index} for index, row in enumerate(sunday)]}
        selection = {"mass": mass["key"], "owner": "ot-2", "slots": ["Collect", "Prayer over the Offerings", "Prayer after Communion"]}
        today.join_weekday_orations(mass, owner, selection, "postconciliar")
        self.assertEqual([row for row, origin in zip(mass["propers"], mass["proper_origins"])
                          if origin["mass"] == mass["key"]], weekday)
        selected = [(row, origin) for row, origin in zip(mass["propers"], mass["proper_origins"])
                    if origin["mass"] == "ot-2"]
        self.assertEqual([row["name"] for row, _ in selected], selection["slots"])
        for row, origin in selected:
            self.assertEqual(row, sunday[origin["source_index"]])
        events = today.expanded_event_projection("postconciliar", mass, None, mass["_proper_source_indices"], {})
        self.assertEqual([event["id"] for event in events], [
            f"proper/postconciliar/{origin['mass']}/{origin['source_index'] + 1:03d}"
            for origin in mass["proper_origins"]])

    @unittest.skipUnless(os.environ.get("TRIPTYCH_WEEKDAY_ORATION_CLI") == "1",
                         "set TRIPTYCH_WEEKDAY_ORATION_CLI=1 for live CLI/browser material parity")
    def test_live_cli_browser_parity_and_forged_owner_refusal(self):
        sys.path.insert(0, str(ROOT / "tools/tests"))
        from _product_data import browser_data_root
        data = browser_data_root(ROOT)
        harness = r"""
          const fs=require('fs'),assert=require('assert/strict'),path=require('path');
          const root=process.argv[1],base=process.argv[2],lang=process.argv[3];
          const read=p=>JSON.parse(fs.readFileSync(path.join(base,p),'utf8'));
          const M=require(root+'/src/web/browser/liturgy/assembly-model.js');
          const A=require(root+'/src/web/browser/liturgy/reader-state-adapters.js');
          const C=require(root+'/src/web/browser/liturgy/reader-state.js');
          const rubrics=read('structure/rubrics/postconciliar.json'),year=read('structure/calendar/postconciliar/2026.json');
          const structure=read('structure/propers/postconciliar.json'),ordinary=read('structure/ordinary/postconciliar.json');
          const initial=M.derive({date:'2026-01-12',rubrics,year});
          const derived=M.selectWeekdayOrations({derived:initial,rubrics,year,structure,owner:'ot-2'}).derived;
          const bible=lang==='la'?'clementine-vulgate':'douay-rheims';
          const request={schema:C.STATE_SCHEMA,entrance:'day',civilDate:'2026-01-12',edition:{id:'postconciliar'},
            calendar:{id:'postconciliar'},bible:{id:bible,numbering:'vulgate'},languages:{orations:lang,ordinary:lang},
            orationMass:'ot-2',requestedMode:'missal',options:{ordinary:true,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
          let raw='';process.stdin.on('data',c=>raw+=c);process.stdin.on('end',()=>{
            const payload=JSON.parse(raw),browser=A.adaptDay({request,derived,structure,ordinary}),cli=A.adaptCli({request,derived,structure,payload});
            const project=x=>x.events.map(e=>({id:e.id,kind:e.kind,sourceHooks:e.sourceHooks,selected:e.selected}));
            assert.deepEqual(project(cli),project(browser));assert.equal(cli.events.filter(e=>e.kind==='proper').length,7);
            for(const mutate of [m=>m.proper_origins[0].mass='ot-3',m=>m.proper_origins[0].source_index=0,m=>m.oration_selection.owner='ot-3']){
              const corrupt=JSON.parse(JSON.stringify(payload));mutate(corrupt.days[0].masses[0]);
              assert.throws(()=>A.adaptCli({request,derived,structure,payload:corrupt}));
            }
          });
        """
        for lang, bible in (("en", "douay-rheims"), ("la", "clementine-vulgate")):
            with self.subTest(language=lang):
                payload = subprocess.run([sys.executable, str(ROOT / "tools/mass-today"),
                    "--date", "2026-01-12", "--calendar", "postconciliar", "--oration-mass", "ot-2",
                    "--lang", lang, "--bible", bible, "--ordinary", "--expanded", "--why", "--json"],
                    capture_output=True, text=True, cwd=ROOT)
                self.assertEqual(payload.returncode, 0, payload.stderr)
                result = subprocess.run(["node", "-e", harness, str(ROOT), str(data), lang],
                    input=payload.stdout, capture_output=True, text=True, cwd=ROOT)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
