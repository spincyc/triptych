"""Held 1962 Common appointments: distinct source units and seasonal selection."""
from __future__ import annotations

import copy
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
from tools.tests._source_recovery_assertions import assert_current_latin_body_or_gap

SOURCE = C.read_yaml(SOURCE_ROOT / "src/sources/calendars/roman-1962/propers.yaml")
INDEX = C.mass_index(SOURCE)
FACT_ID = "roman-1962-common-chant-regime"
NODE = shutil.which("node")
SEATING = Path(os.environ.get("TRIPTYCH_APPOINTMENT_SEATING", ROOT / "src/web/browser/liturgy/ordinary-seating.js"))


def proper(mass, name):
    return next(row for row in INDEX[mass]["propers"] if row["name"] == name)


def refs(row):
    return [(v["book"], [(r["begin"]["chapter"], r["begin"]["verse"], r["end"]["chapter"], r["end"]["verse"]) for r in v["ranges"]]) for v in row.get("verses", [])]


class CommonAppointments(unittest.TestCase):
    def test_source_fact_retains_advent_and_unknown_vigil_phase(self):
        fact = SOURCE["proper_appointment_facts"][FACT_ID]
        self.assertEqual(fact["edition"], "roman-1962")
        self.assertEqual(set(fact["values"]), {"advent", "regular", "tract", "paschal"})
        self.assertEqual(fact["season_values"]["advent"], "advent")
        self.assertEqual(fact["season_values"]["paschaltide"], "paschal")
        self.assertIsNone(fact["season_values"]["triduum"])
        self.assertEqual(C.validate_proper_appointment_facts(SOURCE["proper_appointment_facts"], "roman-1962"), SOURCE["proper_appointment_facts"])

    def test_distinct_regular_and_paschal_scripture_components(self):
        cases = {
            "commune-summorum-pontificum": (1, 2),
            "commune-confessoris-pontificis-2": (1, 2),
            "commune-confessoris-non-pontificis-1": (1, 2),
            "commune-confessoris-non-pontificis-2": (1, 2),
            "commune-abbatum": (1, 2),
            "commune-virginum-1": (1, 2),
            "commune-virginum-3": (1, 2),
            "commune-doctorum-non-pontificis": (1, 0),
        }
        for key, counts in cases.items():
            with self.subTest(mass=key):
                regular = proper(key, "Alleluia")
                paschal = proper(key, "Alleluia (Tempore paschali)")
                self.assertEqual((len(regular["verses"]), len(paschal.get("verses", []))), counts)
                self.assertEqual(regular["ordinary_disposition"]["option"], "regular")
                self.assertEqual(paschal["ordinary_disposition"]["option"], "paschal")
                self.assertEqual(regular["ordinary_disposition"]["anchor"], paschal["ordinary_disposition"]["anchor"])

    def test_uncited_and_partial_chants_keep_reviewed_whole_body_states(self):
        for key in ("commune-unius-martyris-2", "commune-plurimorum-martyrum-3"):
            row = proper(key, "Alleluia")
            self.assertEqual(row["source"], "composed")
            self.assertNotIn("verses", row)
            assert_current_latin_body_or_gap(self, key, "Alleluia", row)
        for key in ("commune-confessoris-pontificis-1", "commune-non-virginum-1", "commune-non-virginum-2"):
            row = proper(key, "Alleluia (Tempore paschali)")
            self.assertEqual(row["source"], "mixed")
            self.assertTrue(row["verses"])
            assert_current_latin_body_or_gap(self, key, "Alleluia (Tempore paschali)", row)

    def test_reviewed_body_and_typed_gap_reject_state_or_wording_corruption(self):
        key = "commune-unius-martyris-2"
        body = proper(key, "Alleluia")
        for corrupt in ({**body, "text": body["text"] + "Amen.\n"},
                        {k: v for k, v in body.items() if k != "text"}):
            with self.assertRaises(AssertionError):
                assert_current_latin_body_or_gap(self, key, "Alleluia", corrupt)
        key = "commune-confessoris-pontificis-1"
        gap = proper(key, "Alleluia (Tempore paschali)")
        self.assertEqual("unavailable", assert_current_latin_body_or_gap(
            self, key, "Alleluia (Tempore paschali)", gap))
        for corrupt in ({**gap, "text": "Invented source body."},
                        {**gap, "text_status": {**gap["text_status"], "reasons": []}}):
            with self.assertRaises(AssertionError):
                assert_current_latin_body_or_gap(self, key, "Alleluia (Tempore paschali)", corrupt)

    def test_virgin_two_borrows_exact_whole_chants_with_independent_appointment(self):
        key = "commune-virginum-2"
        for name in ("Alleluia", "Alleluia (Tempore paschali)"):
            row = proper(key, name)
            self.assertEqual(row["takes_from"], {"mass": "commune-virginum-4", "proper": name})
            self.assertNotIn("verses", row)
            self.assertNotIn("text", row)
        resolved, problems = C.resolve_propers(SOURCE, INDEX[key], appointments=True)
        self.assertEqual(problems, [])
        for _, row, origin in resolved:
            if row["name"] in ("Alleluia", "Alleluia (Tempore paschali)"):
                self.assertEqual(row["appointment_identity"]["mass"], key)
                self.assertEqual(origin["mass"], "commune-virginum-4")
                self.assertEqual(row["text"], proper("commune-virginum-4", row["name"])["text"])

    def test_doctor_replaces_exact_inherited_groups_once(self):
        key = "commune-doctorum-non-pontificis"
        replacements = INDEX[key]["takes_from"]["appointment_overrides"]
        self.assertEqual(len(replacements), 2)
        rows, problems = C.resolve_propers(SOURCE, INDEX[key], appointments=True)
        self.assertEqual(problems, [])
        chant_names = {"Gradual", "Alleluia", "Tract", "Alleluia (Tempore paschali)"}
        selected = [(row, origin) for _, row, origin in rows if row["name"] in chant_names]
        self.assertEqual([row["name"] for row, _ in selected], ["Gradual", "Alleluia", "Tract", "Alleluia (Tempore paschali)"])
        for row, _ in selected:
            self.assertEqual(row["appointment_identity"]["mass"], key)
            self.assertEqual(row["appointment_replacement"]["source_group"]["mass"], "commune-doctorum-pontificis")
        self.assertEqual(selected[-1][1]["mass"], "commune-doctorum-pontificis")

    def test_new_chant_targets_join_exact_source_names(self):
        targets = tomllib.loads((SOURCE_ROOT / "src/sources/inventories/missal-expected-targets-v1.toml").read_text())["targets"]
        targets = {row["id"]: row for row in targets}
        identities = {
            "common-popes:alleluia:2": "Alleluia (Tempore paschali)",
            "common-martyr-bishop-2:alleluia:1": "Alleluia",
            "common-martyrs-3:alleluia:1": "Alleluia",
            "common-confessor-bishop-1:alleluia:2": "Alleluia (Tempore paschali)",
            "common-confessor-bishop-2:alleluia:2": "Alleluia (Tempore paschali)",
            "common-confessor-1:alleluia:2": "Alleluia (Tempore paschali)",
            "common-confessor-2:alleluia:2": "Alleluia (Tempore paschali)",
            "common-abbots:alleluia:2": "Alleluia (Tempore paschali)",
            "common-virgin-martyr-1:alleluia:2": "Alleluia (Tempore paschali)",
            "common-virgin-martyr-2:alleluia:2": "Alleluia (Tempore paschali)",
            "common-virgin-1:alleluia:2": "Alleluia (Tempore paschali)",
            "common-woman-martyr:alleluia:2": "Alleluia (Tempore paschali)",
            "common-woman:alleluia:2": "Alleluia (Tempore paschali)",
        }
        # Keys are exact source identities, never inferred from their labels.
        for suffix, name in identities.items():
            with self.subTest(target=suffix):
                self.assertEqual(targets["roman-1962:body:" + suffix]["calendar_proper_name"], name)

    @unittest.skipUnless(NODE, "Node.js is unavailable")
    def test_shared_execution_selects_source_regimes_and_refuses_incompatible_option(self):
        cases = []
        for key in ("commune-summorum-pontificum", "commune-festorum-bmv", "commune-doctorum-non-pontificis"):
            entries, problems = C.resolve_propers(SOURCE, INDEX[key], appointments=True)
            self.assertEqual(problems, [])
            rows = [{"proper": {**row, "form_id": "main"}, "sourceIndex": i} for i, (_, row, _) in enumerate(entries)]
            group = proper(key, "Alleluia")["ordinary_disposition"]["group"]
            for season, expected in (("advent", "advent" if key == "commune-festorum-bmv" else "regular"), ("lent", "tract"), ("paschaltide", "paschal"), ("triduum", None)):
                cases.append({"rows": rows, "group": "main/" + group, "expected": expected,
                              "context": {"calendar": "roman-1962", "entrance": "day", "date": "2026-04-08", "season": season,
                                          "facts": SOURCE["proper_appointment_facts"], "choices": {}}})
            bad = copy.deepcopy(cases[-2])
            bad["context"]["choices"] = {"main/" + group: "regular"}
            bad["refuse"] = True
            cases.append(bad)
        code = """const S=require(process.argv[1]); let text=''; process.stdin.on('data',c=>text+=c); process.stdin.on('end',()=>{const cases=JSON.parse(text); const results=cases.map(c=>{try {const r=S.prepareProperAppointments(c.rows,c.context); S.unframedEvents(r.rows,()=>false,r.selections); return {selection:r.selections[c.group],unresolved:r.unresolved};} catch(e){return {error:e.message};}}); process.stdout.write(JSON.stringify(results));});"""
        result = subprocess.run([NODE, "-e", code, str(SEATING)], input=json.dumps(cases), text=True, capture_output=True, check=True)
        for case, outcome in zip(cases, json.loads(result.stdout)):
            with self.subTest(group=case["group"], season=case["context"]["season"], refuse=case.get("refuse")):
                if case.get("refuse"):
                    self.assertIn("contradicts source applicability", outcome["error"])
                else:
                    self.assertNotIn("error", outcome)
                    self.assertEqual(outcome["selection"]["option"], case["expected"])
                    if case["expected"] is None:
                        self.assertTrue(outcome["unresolved"])


if __name__ == "__main__":
    unittest.main()
