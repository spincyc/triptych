"""Four existing anniversary appointments; context-dependent Secrets stay unknown."""
from pathlib import Path
import copy
import hashlib
import json
import sys
import unittest
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"scripts"))
import _calendars as C
from _proper_latin import LatinKey, SURFACES, decision_for, read_sidecar
COMMON = "commune-dedicationis-ecclesiae"
FEASTS = ["dedicatione-archibasilicae-mi-salvatoris","dedicatione-basilicarum-ss-petri-pauli-apostolorum"]
digest = lambda s: hashlib.sha256(s.encode()).hexdigest()
canonical = lambda v: json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(",",":"))
DEFINITIONS = {'occasion-orations': {'families': ['Collect', 'Postcommunion'], 'options': {'anniversary': ['Collect', 'Postcommunion'], 'dedication-day': ['Collect (In ipso die Dedicationis)', 'Postcommunion (In ipso die Dedicationis)']}}, 'contextual-secret': {'families': ['Secret'], 'options': {'anniversary-in-church': ['Secret (In ecclesia ipsa dedicata)'], 'anniversary-outside-church': ['Secret (Extra ecclesiam ipsam dedicatam)'], 'dedication-day': ['Secret (In ipso die Dedicationis)']}}}
DISPOSITIONS = {'occasion-orations': {'state': 'selected', 'option': 'anniversary'}, 'contextual-secret': {'state': 'unresolved', 'candidates': ['anniversary-in-church', 'anniversary-outside-church']}}
COMMON_PROPERS_HASH = '4d7103cd7ced80936a4aab2610fb6a88c00f348232ca0affce308c9e3ea79cf0'
PERMISSIONS = {'Collect': 'db0081ffeb2c7c4b5d33c7263cbb5e1c95388cf9cc188c353724494e36ec9edd', 'Postcommunion': '1e1b68fc5e38031b05f00941ca103af2b647d82e7d660e744e462ee882a89dd6'}
COMMON_LEDGER_HASH = '607d872751cdbd01664709fd522b5120fae2697c94ea313a39c1d0a6c30c560d'
ORIGINAL_REFERRALS = {'dedicatione-archibasilicae-mi-salvatoris': {'mass': 'commune-dedicationis-ecclesiae', 'citation': 'Missa Terribilis, de Communi Dedicationis ecclesiae [39]'}, 'dedicatione-basilicarum-ss-petri-pauli-apostolorum': {'mass': 'commune-dedicationis-ecclesiae', 'citation': 'Missa Terribilis, de Communi Dedicationis ecclesiae [39]'}}

def orations(entries):
    return [(C.proper_family(p["name"]),p,o) for _,p,o in entries if C.proper_family(p["name"]) in {"Collect","Secret","Postcommunion"}]

class DedicationAnniversaryRolesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT/"src/sources/calendars","roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records,errors = read_sidecar(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)

    def test_two_axes_and_exact_anniversary_dispositions_have_no_invented_context(self):
        self.assertEqual(DEFINITIONS,self.index[COMMON]["common_sets"])
        for mass in FEASTS:
            ref = self.index[mass]["takes_from"]
            self.assertEqual(DISPOSITIONS,ref["common_sets"])
            self.assertEqual(ORIGINAL_REFERRALS[mass],{k:v for k,v in ref.items() if k!="common_sets"})
            self.assertFalse(self.index[mass].get("propers"))
            self.assertNotIn("appointment_facts",self.index[mass])
            self.assertNotIn("appointment_facts",ref)
            self.assertEqual({"anniversary-in-church","anniversary-outside-church"},
                             set(ref["common_sets"]["contextual-secret"]["candidates"]))

    def test_four_existing_common_appointments_and_two_secrets_fail_closed(self):
        count = 0
        for mass in FEASTS:
            entries,errors = C.resolve_propers(self.document,self.index[mass])
            self.assertEqual([],errors)
            prayers = orations(entries)
            self.assertEqual(["Collect","Postcommunion"],[family for family,_,_ in prayers])
            for family,p,origin in prayers:
                self.assertEqual(COMMON,origin["mass"])
                self.assertEqual(family,p["name"])
                self.assertEqual(PERMISSIONS[family],digest(p["text"]))
                key = LatinKey(COMMON,"",family,"","",1)
                self.assertTrue(decision_for(key,p["text"],self.records).permits(SURFACES))
                self.assertFalse(any(k.mass==mass for k in self.records))
                count += 1
        self.assertEqual(4,count)

    def test_all_common_bodies_and_their_ledger_rows_remain_byte_identical(self):
        self.assertEqual(COMMON_PROPERS_HASH,digest(canonical(self.index[COMMON]["propers"])))
        import tomllib
        rows = tomllib.loads((ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())["entries"]
        self.assertEqual(COMMON_LEDGER_HASH,digest(canonical([r for r in rows if r["mass"]==COMMON])))

    def test_unresolved_occasion_is_not_silently_anniversary_or_actual_dedication(self):
        for mass in FEASTS:
            doc = copy.deepcopy(self.document)
            m = C.mass_index(doc)[mass]
            m["takes_from"]["common_sets"]["occasion-orations"] = {
                "state":"unresolved","candidates":["anniversary","dedication-day"]}
            entries,errors = C.resolve_propers(doc,m)
            self.assertEqual([],errors)
            self.assertEqual([],orations(entries))

    def test_missing_secret_disposition_fails_closed_without_losing_known_roles(self):
        doc = copy.deepcopy(self.document)
        m = C.mass_index(doc)[FEASTS[0]]
        del m["takes_from"]["common_sets"]["contextual-secret"]
        entries,errors = C.resolve_propers(doc,m)
        self.assertTrue(any("disposition" in e for e in errors))
        self.assertEqual(["Collect","Postcommunion"],[f for f,_,_ in orations(entries)])

    def test_explicit_context_and_actual_day_are_distinct_synthetic_choices_only(self):
        for option in ["anniversary-in-church","anniversary-outside-church"]:
            doc = copy.deepcopy(self.document)
            m = C.mass_index(doc)[FEASTS[0]]
            m["takes_from"]["common_sets"]["contextual-secret"] = {"state":"selected","option":option}
            entries,errors = C.resolve_propers(doc,m)
            self.assertEqual([],errors)
            prayers = orations(entries)
            self.assertEqual(["Collect","Secret","Postcommunion"],[f for f,_,_ in prayers])
            secret = next(p for f,p,_ in prayers if f=="Secret")
            self.assertEqual(DEFINITIONS["contextual-secret"]["options"][option][0],secret["name"])
            for f,p,_ in prayers:
                if f!="Secret":
                    self.assertEqual(PERMISSIONS[f],digest(p["text"]))
        doc = copy.deepcopy(self.document)
        m = C.mass_index(doc)[FEASTS[0]]
        for group in ["occasion-orations","contextual-secret"]:
            m["takes_from"]["common_sets"][group] = {"state":"selected","option":"dedication-day"}
        entries,errors = C.resolve_propers(doc,m)
        self.assertEqual([],errors)
        self.assertEqual(3,len(orations(entries)))
        self.assertTrue(all("In ipso die Dedicationis" in p["name"] for _,p,_ in orations(entries)))
        self.assertEqual(DISPOSITIONS,self.index[FEASTS[0]]["takes_from"]["common_sets"])

    def test_unrelated_chants_are_identical_when_the_occasion_changes(self):
        for mass in FEASTS:
            entries,errors = C.resolve_propers(self.document,self.index[mass])
            self.assertEqual([],errors)
            doc = copy.deepcopy(self.document)
            m = C.mass_index(doc)[mass]
            m["takes_from"]["common_sets"]["occasion-orations"] = {
                "state":"unresolved","candidates":["anniversary","dedication-day"]}
            unknown,errors = C.resolve_propers(doc,m)
            self.assertEqual([],errors)
            other = lambda es:[(n,p,o) for n,p,o in es if C.proper_family(p["name"]) not in {"Collect","Secret","Postcommunion"}]
            self.assertEqual(other(entries),other(unknown))

if __name__ == "__main__":
    unittest.main()
