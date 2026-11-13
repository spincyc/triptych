"""A Dedication Secret follows an attested location for one celebration."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _product_data import browser_data_root
rubrics = SourceFileLoader("dedication_rubrics_model", str(ROOT / "tools/calendar-rubrics")).load_module()
days = SourceFileLoader("dedication_days_model", str(ROOT / "tools/calendar-days")).load_module()


class DedicationContextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        built, problems, _ = rubrics.build(rubrics.DEFAULT_ROOT, "roman-1962")
        if problems:
            raise AssertionError(problems)
        cls.rubrics = built[0]
        index = days.load_calendar(rubrics.DEFAULT_ROOT, "roman-1962")
        years = days.build_years(index, [2026, 2027])
        days.with_fixed(index, [2026])
        cls.year = days.year_document(index, 2026, years)
        document = rubrics._calendars.load_document(rubrics.DEFAULT_ROOT, "roman-1962", effective=True)
        masses = rubrics._calendars.mass_index(document)
        rule = cls.rubrics["dedication_anniversary_context"]
        cls.structure = {"calendar": "roman-1962", "masses": []}
        for key in [*rule["keys"], rule["target"]["mass"]]:
            mass = copy.deepcopy(masses[key])
            resolved, errors = rubrics._calendars.resolve_propers(document, masses[key])
            if errors:
                raise AssertionError(errors)
            mass["propers"] = [proper for _, proper, _ in resolved]
            cls.structure["masses"].append(mass)

    def model(self, script, extra=None):
        harness = """
          const assert=require('assert/strict'),m=require(process.argv[1]);
          let raw=''; process.stdin.on('data',c=>raw+=c); process.stdin.on('end',()=>{
            const i=JSON.parse(raw),rule=i.rubrics.dedication_anniversary_context;
            const key=rule.keys[0],date='2026-11-09';
            const derived=m.derive({...i,date});
            const attest=(choices,relation)=>({schema:'triptych-dedication-location/v1',
              calendar:choices.calendar,mass:choices.mass,formId:choices.formId,
              civilDate:choices.civilDate,territory:choices.territory,relation});
        """ + script + "});"
        result = subprocess.run(
            ["node", "-e", harness, str(rubrics.MODEL)],
            input=json.dumps({"year": self.year, "rubrics": self.rubrics, "structure": self.structure, **(extra or {})}),
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_both_feasts_offer_conditions_without_selecting_or_reranking(self):
        self.model("""
          for (const [mass,date] of [[rule.keys[0],'2026-11-09'],[rule.keys[1],'2026-11-18']]) {
            const derived=m.derive({...i,date}), before=JSON.stringify(derived);
            const choices=m.dedicationAnniversaryChoices({...i,derived});
            assert.equal(choices.mass,mass);
            assert.deepEqual(choices.options.map(row=>row.id),['in-dedicated-church','outside-dedicated-church']);
            assert.equal(derived.options[0].dedicationSelection,undefined);
            assert.throws(()=>m.selectDedicationAnniversary({...i,derived}));
            for(const condition of choices.options) {
              const result=m.selectDedicationAnniversary({...i,derived,attestation:attest(choices,condition.id)});
              assert.equal(result.selection.option,condition.option);
              assert.equal(result.selection.proper,condition.proper);
              const unchanged=JSON.parse(JSON.stringify(result.derived));
              delete unchanged.options[0].dedicationSelection;
              assert.deepEqual(unchanged,derived);
            }
            assert.equal(JSON.stringify(derived),before);
          }
        """)

    def test_attestation_cannot_be_missing_stale_or_a_plain_preference(self):
        self.model("""
          const choices=m.dedicationAnniversaryChoices({...i,derived});
          const valid=attest(choices,'in-dedicated-church');
          for(const value of [null,'in-dedicated-church',{},
              {...valid,schema:'other'}, {...valid,calendar:'roman-pre-1955'},
              {...valid,civilDate:'2027-11-09'}, {...valid,mass:rule.keys[1]},
              {...valid,formId:'other'}, {...valid,territory:'another-branch'},
              {...valid,relation:'dedication-day'}, {...valid,confirmed:false}]) {
            assert.throws(()=>m.selectDedicationAnniversary({...i,derived,attestation:value}),JSON.stringify(value));
          }
        """)

    def test_unsettled_displaced_wrong_territory_or_coequal_mass_never_gains_context(self):
        self.model("""
          assert.equal(m.dedicationAnniversaryChoices({...i,derived:m.derive({...i,date:'2026-11-10'})}),null);
          assert.equal(m.dedicationAnniversaryChoices({...i,derived,formId:'other'}),null);
          assert.equal(m.dedicationAnniversaryChoices({...i,derived,territory:'not-held'}),null);
          assert.equal(m.dedicationAnniversaryChoices({...i,derived,mass:rule.target.mass}),null);
          for(const mutate of [
              d=>d.options[0].settled=false,
              d=>d.options[0].conditions.push({fact:'unknown'}),
              d=>d.options[0].unsettled.push({scope:'another-source-gap'}),
              d=>d.options[0].readable.forEach(row=>row.state='displaced')]) {
            const changed=JSON.parse(JSON.stringify(derived));mutate(changed);
            assert.equal(m.dedicationAnniversaryChoices({...i,derived:changed}),null);
          }
          const choice=JSON.parse(JSON.stringify(derived));choice.options[0].choiceRequired=true;
          choice.options[0].readable.forEach(row=>row.state='option');
          assert.equal(m.dedicationAnniversaryChoices({...i,derived:choice}),null);
          assert.equal(m.dedicationAnniversaryChoices({...i,derived:choice,mass:key}).mass,key);
          assert.equal(m.dedicationAnniversaryChoices({...i,derived:choice,mass:rule.keys[1]}),null);
          const territorial=JSON.parse(JSON.stringify(derived));
          territorial.options[0].option='first';
          territorial.options.push({...territorial.options[0],option:'second'});
          assert.equal(m.dedicationAnniversaryChoices({...i,derived:territorial}),null);
          const first=m.dedicationAnniversaryChoices({...i,derived:territorial,territory:'first'});
          assert.throws(()=>m.selectDedicationAnniversary({...i,derived:territorial,territory:'second',
            attestation:attest(first,'in-dedicated-church')}));
        """)

    def test_projection_preserves_each_source_row_and_inserts_only_the_appointed_secret(self):
        self.model("""
          for(const [key,date] of [[rule.keys[0],'2026-11-09'],[rule.keys[1],'2026-11-18']]) {
            const derived=m.derive({...i,date}),choices=m.dedicationAnniversaryChoices({...i,derived});
            const mass=i.structure.masses.find(row=>row.key===key);
            const common=i.structure.masses.find(row=>row.key===rule.target.mass);
            const properRows=mass.propers.map((proper,sourceIndex)=>({proper,sourceIndex}));
            const before=JSON.stringify(i.structure);
            assert.deepEqual(m.projectDedicationAnniversary({mass,properRows}),{mass,rows:properRows});
            for(const condition of choices.options) {
              const selected=m.selectDedicationAnniversary({...i,derived,attestation:attest(choices,condition.id)});
              const projected=m.projectDedicationAnniversary({...i,derived:selected.derived,mass,properRows,selection:selected.selection});
              assert.equal(projected.rows.length,properRows.length+1);
              assert.deepEqual(projected.rows.filter(row=>row.sourceMass===key).map(row=>row.proper),mass.propers);
              assert.deepEqual(projected.rows.filter(row=>row.sourceMass===key).map(row=>row.sourceProperIndex),properRows.map(row=>row.sourceIndex));
              const secret=projected.rows.filter(row=>row.sourceMass===common.key);
              assert.equal(secret.length,1);
              assert.equal(secret[0].proper.name,condition.proper);
              assert.deepEqual(secret[0].proper,common.propers[secret[0].sourceProperIndex]);
              assert.equal(projected.rows[secret[0].sourceIndex-1].proper.name,'Offertory');
              assert.equal(projected.rows[secret[0].sourceIndex+1].proper.name,'Communion');
              assert.deepEqual(projected.mass.takes_from.common_sets['contextual-secret'],{state:'selected',option:condition.option});
              assert.deepEqual(projected.mass.takes_from.common_sets['occasion-orations'],mass.takes_from.common_sets['occasion-orations']);
              assert.equal(JSON.stringify(i.structure),before);
              assert.throws(()=>m.projectDedicationAnniversary({...i,derived,mass,properRows,selection:{...selected.selection,option:'dedication-day'}}));
              assert.throws(()=>m.projectDedicationAnniversary({...i,derived,mass,properRows:properRows.slice().reverse(),selection:selected.selection}));
            }
          }
        """)


    def test_live_reader_projection_keeps_commemoration_and_unresolved_location_honest(self):
        data = browser_data_root(ROOT)
        structure = json.loads((data / "structure/propers/roman-1962.json").read_text())
        ordinary = json.loads((data / "structure/ordinary/roman-1962.json").read_text())
        request = json.loads((ROOT / "tools/tests/fixtures/liturgy-reader-state/v1/day-roman-1962-2026-08-02.json").read_text())["requested"]
        self.model("""
          const a=require(process.argv[1].replace('assembly-model.js','reader-state-adapters.js'));
          const s=require(process.argv[1].replace('assembly-model.js','ordinary-seating.js'));
          for(const date of ['2026-11-09','2026-11-18']) {
            const derived=m.derive({...i,date}),choices=m.dedicationAnniversaryChoices({...i,derived});
            for(const language of ['la','en']) for(const missal of [false,true]) {
              const request={...i.request,civilDate:date,selectedReadableFormulary:{id:choices.mass},
                languages:{orations:language,ordinary:language},requestedMode:missal?'missal':'read',
                options:{ordinary:missal,legitimate:{}}};
              const input={...i,request,derived};
              const unresolved=a.adaptDay(input);
              assert(unresolved.unresolvedChoices.some(row=>row.id.includes('contextual-secret')));
              assert(!unresolved.events.some(row=>row.editionSlotLabel&&row.editionSlotLabel.startsWith('Secret')));
              const originals=unresolved.events.filter(row=>row.kind==='proper').map(row=>row.id);
              for(const condition of choices.options) {
                const selected=m.selectDedicationAnniversary({...i,derived,attestation:attest(choices,condition.id)});
                const adapted=a.adaptDay({...input,derived:selected.derived});
                assert(!adapted.unresolvedChoices.some(row=>row.id.includes('contextual-secret')));
                const secret=adapted.events.find(row=>row.editionSlotLabel===condition.proper);
                assert(secret,condition.proper);assert.equal(secret.selected.availability,'held');
                assert(secret.id.includes('/'+choices.target.mass+'/'));
                assert.deepEqual(adapted.events.filter(row=>row.kind==='proper'&&row!==secret).map(row=>row.id),originals);
                if(date==='2026-11-09') {
                  const grouped=adapted.events.filter(row=>(row.orationGroups||[]).length);
                  assert.equal(grouped.length,3);
                  for(const row of grouped) {
                    const member=row.orationGroups[0].members[0];
                    assert(member.id.includes('/comm-s-theodori-martyris/'));
                    assert.equal(member.semanticSlot.identity.id,row.semanticSlot.identity.id);
                  }
                  assert.equal(unresolved.events.filter(row=>(row.orationGroups||[]).length).length,2);
                }
                assert.throws(()=>a.adaptDay({...input,derived:selected.derived,rubrics:{calendar:'roman-1962'}}));
              }
              // A plain source mismatch still fails; only the validated Common
              // descriptor permits this known unresolved Secret anchor.
              if(date==='2026-11-09') assert.throws(()=>a.adaptDay({...input,rubrics:{calendar:'roman-1962'}}),/unique principal source seat for Secret/);
            }
            if(date==='2026-11-09') {
              const mass=i.structure.masses.find(row=>row.key===choices.mass),branch=derived.options[0];
              const context={active:true,calendar:'roman-1962',mainKey:mass.key,date,season:derived.season,
                facts:i.structure.proper_appointment_facts,
                execution:branch.oration_execution,series:branch.orations.all||branch.orations.low_mass,principalCommonReference:mass.takes_from,
                owners:i.structure.masses.map(owner=>({key:owner.key,sourcePaths:owner.proper_source_paths||[],rows:owner.propers.map((proper,sourceIndex)=>({proper,sourceIndex}))}))};
              const rows=mass.propers.map((proper,sourceIndex)=>({proper,sourceIndex}));
              assert.equal(s.orationPlan(rows,{...context,unresolvedDedicationContext:choices}).length,2);
              assert.throws(()=>s.orationPlan(rows,{...context,unresolvedPrincipalSlots:['Secret']}));
              const other=i.structure.masses.find(row=>row.key==='advent-1');
              assert.throws(()=>s.orationPlan(other.propers.filter(row=>row.name!=='Secret'),{
                ...context,mainKey:other.key,principalCommonReference:other.takes_from,
                series:[{...context.series[0],source_key:other.key},...context.series.slice(1)],
                unresolvedDedicationContext:{...choices,mass:other.key}
              }),/principal source Common reference/);
              for(const bad of [{...choices,mass:'another-mass'},{...choices,civilDate:'2026-11-18'},
                  {id:choices.id},['Secret']]) {
                assert.throws(()=>s.orationPlan(rows,{...context,unresolvedDedicationContext:bad}));
              }
            }
          }
        """, {"structure": structure, "ordinary": ordinary, "request": request})


    def test_terminal_uses_the_same_attestation_and_refuses_silent_link_loss(self):
        data = browser_data_root(ROOT)
        scratch = ROOT / ".scratch/dedication-context"
        scratch.mkdir(parents=True, exist_ok=True)
        # The live browser fixture is immutable to this test. Its rubric and
        # calendar are replaced in a private view with today's source builds.
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            view = Path(temporary)
            for entry in data.iterdir():
                if entry.name != "structure":
                    (view / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
            (view / "structure/rubrics").mkdir(parents=True)
            (view / "structure/calendar/roman-1962").mkdir(parents=True)
            for entry in (data / "structure").iterdir():
                if entry.name not in {"rubrics", "calendar"}:
                    (view / "structure" / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
            for entry in (data / "structure/rubrics").iterdir():
                if entry.name != "roman-1962.json":
                    (view / "structure/rubrics" / entry.name).symlink_to(entry)
            (view / "structure/rubrics/roman-1962.json").write_text(json.dumps(self.rubrics))
            for entry in (data / "structure/calendar").iterdir():
                if entry.name != "roman-1962":
                    (view / "structure/calendar" / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
            for entry in (data / "structure/calendar/roman-1962").iterdir():
                if entry.name != "2026.json":
                    (view / "structure/calendar/roman-1962" / entry.name).symlink_to(entry)
            (view / "structure/calendar/roman-1962/2026.json").write_text(json.dumps(self.year))
            requests = []
            for key, date in zip(self.rubrics["dedication_anniversary_context"]["keys"], ["2026-11-09", "2026-11-18"]):
                requests.append({"id": date + "/default", "adapter": "liturgy", "fn": "day",
                                 "args": ["roman-1962", date, {"orations": "en"}]})
                for relation in ["in-dedicated-church", "outside-dedicated-church"]:
                    attestation = {"schema": "triptych-dedication-location/v1", "calendar": "roman-1962",
                                   "mass": key, "formId": "main", "civilDate": date, "territory": None, "relation": relation}
                    options = {"orations": "en", "dedicationAttestation": attestation}
                    requests.append({"id": date + "/" + relation, "adapter": "liturgy", "fn": "day",
                                     "args": ["roman-1962", date, options]})
                    requests.append({"id": date + "/" + relation + "/share", "adapter": "liturgy", "fn": "readerUrl",
                                     "args": ["day", "roman-1962", date, options]})
                    requests.append({"id": date + "/" + relation + "/compare", "adapter": "liturgy", "fn": "compare",
                                     "args": ["roman-1962", "roman-pre-1955", date, options]})
            done = subprocess.run(["node", str(ROOT / "scripts/lectern/bridge.js"), str(view)],
                                  input="".join(json.dumps(row) + "\n" for row in requests),
                                  text=True, capture_output=True, cwd=ROOT, timeout=60)
            self.assertEqual(done.returncode, 0, done.stderr)
            replies = {row["id"]: row for row in map(json.loads, done.stdout.splitlines())}
            self.assertEqual(set(replies), {row["id"] for row in requests})
            for request in requests:
                reply = replies[request["id"]]
                if request["fn"] == "readerUrl":
                    self.assertFalse(reply["ok"])
                    self.assertIn("location is not carried in a reader link", reply["error"])
                    continue
                self.assertTrue(reply["ok"], reply)
                if request["fn"] == "compare":
                    self.assertIn("Clear the stated celebration location", reply["value"]["refused"])
                    continue
                row, = reply["value"]["rows"]
                self.assertNotIn("failed", row)
                self.assertEqual(len(row["dedicationChoices"]["options"]), 2)
                if request["id"].endswith("/default"):
                    self.assertIsNone(row["dedicationSelection"])
                    self.assertTrue(any("contextual-secret" in choice["id"] for choice in row["unresolvedChoices"]))
                else:
                    expected = request["args"][2]["dedicationAttestation"]
                    self.assertEqual(row["dedicationSelection"]["attestation"], expected)
                    secret, = [event for event in row["events"] if (event.get("slot") or "").startswith("Secret")]
                    self.assertIn("/commune-dedicationis-ecclesiae/", secret["id"])
                    self.assertTrue(secret["blocks"])
                    self.assertIn("Celebration location stated:", row["notice"])


if __name__ == "__main__":
    unittest.main()
