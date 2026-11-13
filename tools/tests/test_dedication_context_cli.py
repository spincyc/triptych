"""Typed location joins one exact Common Secret without changing other Propers."""

import copy
from contextlib import contextmanager
import json
import os
from importlib.machinery import SourceFileLoader
from pathlib import Path
import sys
import subprocess
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/tests"))
from _product_data import browser_data_root

rubrics = SourceFileLoader("dedication_cli_rubrics", str(ROOT / "tools/calendar-rubrics")).load_module()
today = SourceFileLoader("dedication_cli_today", str(ROOT / "tools/mass-today")).load_module()
days = SourceFileLoader("dedication_cli_days", str(ROOT / "tools/calendar-days")).load_module()


class DedicationContextCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = browser_data_root(ROOT)
        cls.structure = json.loads((cls.data / "structure/propers/roman-1962.json").read_text())
        index = days.load_calendar(rubrics.DEFAULT_ROOT, "roman-1962")
        years = days.build_years(index, [2026, 2027])
        days.with_fixed(index, [2026])
        cls.year = days.year_document(index, 2026, years)
        built, problems, _ = rubrics.build(rubrics.DEFAULT_ROOT, "roman-1962")
        if problems:
            raise AssertionError(problems)
        cls.rubrics = built[0]

    def selected(self, date, relation):
        result = rubrics.run_model({"cases": [{"id": "fixture", "date": date,
            "year": self.year, "rubrics": self.rubrics, "structure": self.structure,
            "dedicationLocation": relation}]})["results"][0]
        self.assertTrue(result["ok"], result.get("error"))
        return result["result"]

    def test_both_anniversaries_and_locations_preserve_exact_source_members(self):
        @contextmanager
        def products(*args, **kwargs):
            yield SimpleNamespace(data_root=self.data)

        for date in ("2026-11-09", "2026-11-18"):
            for relation, expected in (("in-dedicated-church", "Secret (In ecclesia ipsa dedicata)"),
                                       ("outside-dedicated-church", "Secret (Extra ecclesiam ipsam dedicatam)")):
                with self.subTest(date=date, location=relation):
                    derived = self.selected(date, relation)
                    selection = derived["options"][0]["dedicationSelection"]
                    source = next(row for row in self.structure["masses"] if row["key"] == selection["mass"])
                    common = next(row for row in self.structure["masses"] if row["key"] == selection["target"]["mass"])
                    before = copy.deepcopy(source["propers"])
                    mass = today._SourceMass(copy.deepcopy(source))
                    mass["_proper_source_indices"] = list(range(len(before)))
                    mass._ordinary_source_rows = [{"proper": proper, "sourceIndex": index}
                        for index, proper in enumerate(mass["propers"])]
                    owner = copy.deepcopy(common)
                    owner["_proper_source_indices"] = list(range(len(owner["propers"])))
                    owner["_ordinary_source_rows"] = [{"proper": proper, "sourceIndex": index}
                        for index, proper in enumerate(owner["propers"])]
                    with patch.object(today, "verified_products", products):
                        today.join_dedication_context(mass, owner, selection, derived)
                    self.assertEqual([proper for proper, origin in zip(mass["propers"], mass["proper_origins"])
                                      if origin["mass"] == mass["key"]], before)
                    added = [(proper, origin) for proper, origin in zip(mass["propers"], mass["proper_origins"])
                             if origin["mass"] == common["key"]]
                    self.assertEqual(len(added), 1)
                    self.assertEqual(added[0][0]["name"], expected)
                    self.assertEqual(added[0][0], common["propers"][added[0][1]["source_index"]])
                    self.assertEqual(mass["takes_from"]["common_sets"]["contextual-secret"],
                                     {"state": "selected", "option": selection["option"]})
                    self.assertEqual(selection["attestation"]["civilDate"], date)

    def test_unknown_location_and_other_day_are_refused_by_shared_model(self):
        cases = [{"id": date + relation, "date": date, "year": self.year,
                  "rubrics": self.rubrics, "structure": self.structure, "dedicationLocation": relation}
                 for date, relation in (("2026-11-09", "unknown"),
                                        ("2026-11-09", "dedication-day"),
                                        ("2026-11-10", "outside-dedicated-church"))]
        results = rubrics.run_model({"cases": cases})["results"]
        self.assertTrue(all(not row["ok"] for row in results))

    def test_unstated_location_keeps_other_oration_groups_and_exact_missing_context(self):
        result = rubrics.run_model({"cases": [{"id": "default", "date": "2026-11-09",
            "year": self.year, "rubrics": self.rubrics, "structure": self.structure}]})["results"][0]
        self.assertTrue(result["ok"], result.get("error"))
        branch = result["result"]["options"][0]
        self.assertNotIn("dedicationSelection", branch)
        descriptor = branch["unresolvedDedicationContext"]
        self.assertEqual(descriptor["civilDate"], "2026-11-09")
        held = {mass["key"]: mass for mass in self.structure["masses"]}
        masses = []
        for readable in branch["readable"]:
            mass = today._SourceMass(copy.deepcopy(held[readable["key"]]))
            mass["proper_appointment_facts"] = self.structure.get("proper_appointment_facts", {})
            mass._source_branch = branch
            mass._source_readable = readable
            mass._oration_source_rows = [{"proper": proper, "sourceIndex": index}
                                        for index, proper in enumerate(mass["propers"])]
            masses.append(mass)
        day = {"calendar": "roman-1962", "selected_mass": descriptor["mass"],
               "season": result["result"]["season"], "masses": masses}
        main = next(mass for mass in masses if mass["key"] == descriptor["mass"])
        context = today.oration_context_for(day, main, "2026-11-09")
        self.assertEqual(context["unresolvedDedicationContext"], descriptor)
        resolution = today.mass_events(None, main._oration_source_rows, None,
                                       proper_appointment_context={"calendar": "roman-1962",
                                           "mass": main["key"], "entrance": "day", "date": "2026-11-09",
                                           "season": day["season"], "facts": main["proper_appointment_facts"]},
                                       oration_context=context)
        grouped = [event["proper"]["name"] for event in resolution["events"] if event.get("orationGroups")]
        self.assertEqual(grouped, ["Collect", "Postcommunion"])

    @unittest.skipUnless(os.environ.get("TRIPTYCH_DEDICATION_CLI") == "1",
                         "set TRIPTYCH_DEDICATION_CLI=1 for live contextual CLI/browser parity")
    def test_live_contextual_cli_parity_and_forged_attestation_refusal(self):
        harness = r"""
          const fs=require('fs'),assert=require('assert/strict'),path=require('path');
          const root=process.argv[1],base=process.argv[2],date=process.argv[3],relation=process.argv[4],lang=process.argv[5];
          const read=p=>JSON.parse(fs.readFileSync(path.join(base,p),'utf8'));
          const M=require(root+'/src/web/browser/liturgy/assembly-model.js'),A=require(root+'/src/web/browser/liturgy/reader-state-adapters.js'),C=require(root+'/src/web/browser/liturgy/reader-state.js');
          const rubrics=read('structure/rubrics/roman-1962.json'),year=read('structure/calendar/roman-1962/2026.json');
          const structure=read('structure/propers/roman-1962.json'),ordinary=read('structure/ordinary/roman-1962.json');
          let derived=M.derive({date,rubrics,year});const choice=M.dedicationAnniversaryChoices({derived,rubrics,structure});
          const attestation={schema:'triptych-dedication-location/v1',calendar:choice.calendar,mass:choice.mass,formId:choice.formId,civilDate:date,territory:choice.territory,relation};
          derived=M.selectDedicationAnniversary({derived,rubrics,structure,attestation}).derived;
          const bible=lang==='la'?'clementine-vulgate':'douay-rheims';
          const request={schema:C.STATE_SCHEMA,entrance:'day',civilDate:date,edition:{id:'roman-1962'},calendar:{id:'roman-1962'},bible:{id:bible,numbering:'vulgate'},languages:{orations:lang,ordinary:lang},requestedMode:'missal',options:{ordinary:true,legitimate:{}},coverage:[],unresolvedChoices:[],sourceHooks:[]};
          let raw='';process.stdin.on('data',c=>raw+=c);process.stdin.on('end',()=>{
            const payload=JSON.parse(raw),browser=A.adaptDay({request,derived,structure,ordinary,rubrics}),cli=A.adaptCli({request,derived,structure,payload,rubrics});
            const event=e=>({id:e.id,kind:e.kind,sourceHooks:e.sourceHooks,selected:e.selected,orationGroups:e.orationGroups});
            assert.deepEqual(cli.events.map(event),browser.events.map(event));
            assert.ok(cli.events.some(e=>e.id.includes('/'+choice.target.mass+'/')));
            if(date==='2026-11-09') assert.equal(cli.events.filter(e=>e.orationGroups).length,3);
            for(const mutate of [m=>m.proper_origins.find(r=>r.mass===choice.target.mass).source_index=12,
              m=>m.dedication_selection.attestation.civilDate='2026-01-01',
              m=>m.takes_from.common_sets['contextual-secret']={state:'unresolved',candidates:['anniversary-in-church','anniversary-outside-church']}]) {
              const corrupt=JSON.parse(JSON.stringify(payload));mutate(corrupt.days[0].masses.find(m=>m.key===choice.mass));
              assert.throws(()=>A.adaptCli({request,derived,structure,payload:corrupt,rubrics}));
            }
          });
        """
        for date, relation, lang, bible in (("2026-11-09", "outside-dedicated-church", "en", "douay-rheims"),
                                            ("2026-11-18", "in-dedicated-church", "la", "clementine-vulgate")):
            with self.subTest(date=date, location=relation, language=lang):
                payload = subprocess.run([sys.executable, str(ROOT / "tools/mass-today"),
                    "--date", date, "--calendar", "roman-1962", "--dedication-location", relation,
                    "--lang", lang, "--bible", bible, "--ordinary", "--expanded", "--why", "--json"],
                    capture_output=True, text=True, cwd=ROOT)
                self.assertEqual(payload.returncode, 0, payload.stderr)
                result = subprocess.run(["node", "-e", harness, str(ROOT), str(self.data), date, relation, lang],
                    input=payload.stdout, capture_output=True, text=True, cwd=ROOT)
                self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
