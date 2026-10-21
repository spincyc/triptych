"""Four page-backed Common readings and their exact receiving appointments."""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
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

SOURCE = C.read_yaml(SOURCE_ROOT / "src/sources/calendars/roman-1962/propers.yaml")
INDEX = C.mass_index(SOURCE)
NODE = shutil.which("node")
SEATING = Path(os.environ.get("TRIPTYCH_APPOINTMENT_SEATING", ROOT / "src/web/browser/liturgy/ordinary-seating.js"))
OPERATIONS = (
    (4237, "commune-unius-martyris-1", "Epistle (altera in Communi unius Martyris)", "James", 1, 2, 12, ("commune-unius-martyris-1", "commune-unius-martyris-2", "commune-unius-martyris-3", "commune-unius-martyris-4")),
    (4271, "commune-plurimorum-martyrum-1", "Gospel (alterum in Communi plurimorum Martyrum)", "Matthew", 24, 3, 13, ("commune-plurimorum-martyrum-1", "commune-plurimorum-martyrum-2", "commune-plurimorum-martyrum-3")),
    (4305, "commune-martyrum-tempore-paschali-2", "Gospel (alterum in Communi Martyrum tempore paschali)", "John", 16, 20, 22, ("commune-martyrum-tempore-paschali-2", "commune-martyrum-tempore-paschali-1")),
    (4405, "commune-virginum-2", "Gospel (alterum)", "Matthew", 19, 3, 12, ("commune-virginum-2",)),
)


class CommonReadingAppointments(unittest.TestCase):
    def test_four_stored_source_units_have_exact_cited_bounds(self):
        for unit, mass, name, book, chapter, begin, end, _ in OPERATIONS:
            with self.subTest(unit=unit):
                row = next(p for p in INDEX[mass]["propers"] if p["name"] == name)
                self.assertEqual(row["source"], "scripture")
                self.assertNotIn("text", row)
                self.assertEqual(row["verses"][0]["book"], book)
                self.assertEqual(row["verses"][0]["ranges"], [{"begin": {"chapter": chapter, "verse": begin}, "end": {"chapter": chapter, "verse": end}}])
                self.assertIn(str(unit), row["notes"])

    def test_ten_receiving_wrappers_preserve_appointment_and_wording_owners(self):
        count = 0
        for unit, owner, stored_name, *_details, receivers in OPERATIONS:
            for mass in receivers:
                with self.subTest(unit=unit, mass=mass):
                    rows, problems = C.resolve_propers(SOURCE, INDEX[mass], appointments=True)
                    self.assertEqual(problems, [])
                    choices = [(row, origin) for _, row, origin in rows if row.get("ordinary_disposition", {}).get("option") == "unit-" + str(unit)]
                    self.assertEqual(len(choices), 1)
                    row, origin = choices[0]
                    self.assertEqual(row["appointment_identity"]["mass"], mass)
                    self.assertEqual(row["ordinary_disposition"]["anchor"]["mass"], mass)
                    self.assertNotIn("when", row["ordinary_disposition"])
                    if mass != owner:
                        self.assertEqual(origin["mass"], owner)
                        self.assertEqual(origin["proper"], stored_name)
                    count += 1
        self.assertEqual(count, 10)

    def test_common_three_qualifies_its_exact_lesson_without_renaming(self):
        mass = INDEX["commune-unius-martyris-3"]
        candidates = [p for p in mass["propers"] if p.get("ordinary_disposition", {}).get("group") == "unius-martyris-3-first-reading"]
        self.assertEqual([p["name"] for p in candidates], ["Lesson", "Lesson (altera Epistola in Communi unius Martyris)"])
        for row in candidates:
            self.assertEqual(row["ordinary_disposition"]["seat"], "reading-1")
            self.assertEqual(row["ordinary_disposition"]["anchor"], {"mass": mass["key"], "form_id": "main", "proper": "Lesson", "occurrence": 1})
        record = tomllib.loads((SOURCE_ROOT / "src/sources/inventories/roman-1962-common-reading-appointments-v1.toml").read_text())
        self.assertEqual(record["first_reading_seat_qualification"]["principal_source_unit"], 4217)

    def test_euphemia_keeps_its_source_fixed_gospel_and_no_common_gospel_menu(self):
        mass = INDEX["comm-ss-euphemiae-virginis-luciae-geminiani"]
        rows, problems = C.resolve_propers(SOURCE, mass, appointments=True)
        self.assertEqual(problems, [])
        gospels = [(p, origin) for _, p, origin in rows if p["name"].startswith("Gospel")]
        self.assertEqual(len(gospels), 1)
        row, origin = gospels[0]
        self.assertEqual(row["verses"][0]["book"], "Luke")
        self.assertEqual(row["verses"][0]["ranges"], [{"begin": {"chapter": 6, "verse": 17}, "end": {"chapter": 6, "verse": 23}}])
        self.assertIsNone(origin)
        self.assertNotIn("ordinary_disposition", row)
        self.assertEqual(row["appointment_replacement"]["source_group"]["id"], "plurimorum-martyrum-1-gospel")

    def test_printed_pool_parent_identity_is_preserved_without_false_mass_join(self):
        targets = {r["id"]: r for r in tomllib.loads((SOURCE_ROOT / "src/sources/inventories/missal-expected-targets-v1.toml").read_text())["targets"]}
        for suffix, parent in (("common-martyr-readings:epistle:1", "common-martyr-readings"), ("common-martyrs-readings:gospel:1", "common-martyrs-readings")):
            row = targets["roman-1962:body:" + suffix]
            self.assertEqual(row["parent_id"], "roman-1962:body:" + parent)
            self.assertEqual(targets[row["parent_id"]]["kind"], "common")
            self.assertNotIn("calendar_mass_key", row)
            self.assertNotIn("calendar_proper_name", row)
        self.assertEqual(targets["roman-1962:body:common-martyrs-paschal:gospel:2"]["calendar_proper_name"], OPERATIONS[2][2])
        self.assertEqual(targets["roman-1962:body:common-virgin-martyr-2:gospel:2"]["calendar_proper_name"], OPERATIONS[3][2])

    def test_all_inheriting_mass_references_remain_valid(self):
        failures = {}
        for key, mass in INDEX.items():
            _, problems = C.resolve_propers(SOURCE, mass, appointments=True)
            if problems:
                failures[key] = problems
        self.assertEqual(failures, {})

    @unittest.skipUnless(NODE, "Node.js is unavailable")
    def test_shared_unframed_execution_selects_only_the_explicit_reading(self):
        cases = []
        for unit, _owner, _name, *_details, receivers in OPERATIONS:
            for key in receivers:
                entries, problems = C.resolve_propers(SOURCE, INDEX[key], appointments=True)
                self.assertEqual(problems, [])
                rows = [{"proper": {**p, "form_id": "main"}, "sourceIndex": i} for i, (_, p, _) in enumerate(entries)]
                selected = next(r["proper"] for r in rows if r["proper"].get("ordinary_disposition", {}).get("option") == "unit-" + str(unit))
                group = selected["ordinary_disposition"]["group"]
                cases.append({"key": key, "unit": unit, "rows": rows, "group": group,
                              "context": {"calendar": "roman-1962", "entrance": "propers", "facts": SOURCE["proper_appointment_facts"], "choices": {"main/" + group: "unit-" + str(unit)}}})
        code = """const S=require(process.argv[1]);let input='';process.stdin.on('data',c=>input+=c);process.stdin.on('end',()=>{const out=JSON.parse(input).map(c=>{try{const r=S.prepareProperAppointments(c.rows,c.context);const events=S.unframedEvents(r.rows,()=>false,r.selections);const choice=events.find(e=>e.kind==='proper_choice'&&e.group===c.group);return {selection:r.selections['main/'+c.group],choice:choice||events.filter(e=>e.kind==='proper_choice').map(e=>({group:e.group,id:e.id}))};}catch(e){return {error:e.message};}});process.stdout.write(JSON.stringify(out));});"""
        result = subprocess.run([NODE, "-e", code, str(SEATING)], input=json.dumps(cases), text=True, capture_output=True, check=True)
        for case, outcome in zip(cases, json.loads(result.stdout)):
            with self.subTest(unit=case["unit"], mass=case["key"]):
                self.assertNotIn("error", outcome)
                self.assertEqual(outcome["selection"], {"state": "selected", "option": "unit-" + str(case["unit"])})


if __name__ == "__main__":
    unittest.main()
