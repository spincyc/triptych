"""Exact source appointments, cues and finite seats for a ferial Proper rite."""
from copy import deepcopy
import importlib.machinery
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/mass-ordinary"
loader = importlib.machinery.SourceFileLoader("osp_mass_ordinary", str(TOOL))
spec = importlib.util.spec_from_loader(loader.name, loader)
M = importlib.util.module_from_spec(spec)
loader.exec_module(M)


class ProperRites(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = ROOT / "src/sources"
        cls.inventory = M.read_toml(cls.sources / "inventories/roman-1962-ordo-missae-v1.toml")
        cls.rite = next(row for row in cls.inventory["proper_rites"]
                        if row["id"] == "oratio-super-populum")

    def source(self):
        return {"calendar": "roman-1962", "proper_rites": [deepcopy(self.rite)]}

    def test_exact_declared_source_appointments_join(self):
        found = M.proper_rite_table(self.source(), self.sources, "test")
        self.assertEqual(found, [self.rite])
        # The named rows are counted from their owner, never from a hand-kept
        # total that could hide a restored appointment. The two literal Ember
        # Oratio coordinates remain an explicit, source-reviewed distinction.
        document = M._calendars.load_document(self.sources / "calendars", "roman-1962", effective=False)
        named = set()
        for section in document["sections"].values():
            for mass in section["masses"]:
                for form in mass.get("forms") or [{"id": "main", "propers": mass.get("propers", [])}]:
                    occurrence = 0
                    for proper in form["propers"]:
                        if proper.get("name") == "Oratio super populum":
                            occurrence += 1
                            named.add((mass["key"], form["id"], proper["name"], occurrence))
        declared = {(row["mass"], row["form_id"], row["proper"], row["occurrence"])
                    for row in found[0]["appointments"]}
        literal = {("lent-1-ember-saturday", "longer", "Oratio", 6),
                   ("lent-1-ember-saturday", "shorter", "Oratio", 2)}
        self.assertEqual(declared, named | literal)
        self.assertEqual([(r["form_id"], r["occurrence"]) for r in found[0]["appointments"]
                          if r["proper"] == "Oratio"], [("longer", 6), ("shorter", 2)])

    def test_absent_declaration_preserves_existing_calendars(self):
        self.assertEqual(M.proper_rite_table({"calendar": "postconciliar"}, self.sources, "test"), [])

    def test_closed_declaration_shape_and_role(self):
        alterations = [
            lambda s: s.update(calendar="postconciliar"),
            lambda s: s.update(proper_rites=[]),
            lambda s: s["proper_rites"][0].update(edition="postconciliar"),
            lambda s: s["proper_rites"][0].update(semantic_role="collect"),
            lambda s: s["proper_rites"][0].update(own_conclusion=False),
            lambda s: s["proper_rites"][0].update(locus="  "),
            lambda s: s["proper_rites"][0].update(default=True),
            lambda s: s["proper_rites"][0].update(appointments=[]),
            lambda s: s["proper_rites"].append(deepcopy(s["proper_rites"][0])),
        ]
        for alter in alterations:
            with self.subTest(alter=alter):
                s = self.source(); alter(s)
                with self.assertRaises(M.SourceError): M.proper_rite_table(s, self.sources, "test")

    def test_wrong_source_coordinates_and_nonterminal_oration_refused(self):
        alterations = [
            {"mass": "unheld-mass"}, {"form_id": "unheld-form"},
            {"proper": "Missing prayer"}, {"occurrence": 2},
            {"occurrence": True}, {"locus": ""}, {"unknown": "field"},
            {"proper": "Postcommunion"},
            {"mass": "lent-1-ember-saturday", "form_id": "longer", "proper": "Oratio", "occurrence": 1},
        ]
        for values in alterations:
            with self.subTest(values=values):
                s = self.source(); s["proper_rites"][0]["appointments"][0].update(values)
                with self.assertRaises(M.SourceError): M.proper_rite_table(s, self.sources, "test")

    def test_duplicate_appointment_and_conditional_source_refused(self):
        s = self.source(); s["proper_rites"][0]["appointments"].append(deepcopy(s["proper_rites"][0]["appointments"][0]))
        with self.assertRaises(M.SourceError): M.proper_rite_table(s, self.sources, "test")
        document = deepcopy(M._calendars.load_document(self.sources / "calendars", "roman-1962", effective=False))
        mass = next(m for section in document["sections"].values() for m in section["masses"] if m["key"] == "ash-wednesday")
        mass["propers"][-1]["ordinary_disposition"] = {"kind": "unplaced"}
        with patch.object(M._calendars, "load_document", return_value=document):
            with self.assertRaises(M.SourceError): M.proper_rite_table(self.source(), self.sources, "test")

    def parts(self):
        condition = {"kind": "include-when-proper-rite", "rite": self.rite["id"], "basis": self.rite["locus"]}
        compiled = M.element_conditions({"conditions": [condition]}, {}, "cue", "test")
        sections = [{"key": "conclusio", "elements": [
            {"key": "conclusio/postcommunion", "conditions": [], "alternatives": []},
            {"key": "conclusio/osp-cues", "conditions": compiled, "alternatives": []},
            {"key": "conclusio/final-greeting", "conditions": [], "alternatives": []},
        ]}]
        source = {"slots_derived_from": "held target rule", "slots": [
            {"key": "postcommunion", "after": "conclusio/postcommunion", "propers": ["Postcommunion"], "locus": "held rule"},
            {"key": "oratio-super-populum", "before": "conclusio/final-greeting", "rite": self.rite["id"], "locus": self.rite["locus"]},
        ]}
        return source, sections

    def test_one_finite_seat_one_cue_and_contextless_show(self):
        source, sections = self.parts()
        slots = M.slot_table(source, sections, "test", [self.rite])
        M.proper_rite_coverage([self.rite], slots, sections, "test")
        self.assertEqual(slots[-1]["propers"], [])
        self.assertFalse(slots[-1]["qualified"])
        self.assertEqual(slots[-1]["rite"], self.rite["id"])
        shown, unresolved = M.element_applicability(sections[0]["elements"][1], {})
        self.assertFalse(shown)
        self.assertEqual(unresolved[0]["unknown"], "unresolved")

    def test_mixed_or_unbound_slot_claim_refused(self):
        alterations = [lambda s: s["slots"][-1].update(propers=["Oratio"]),
                      lambda s: s["slots"][-1].update(qualified=False),
                      lambda s: s["slots"][-1].update(rite="unknown"),
                      lambda s: s["slots"][-1].update(before="missing-anchor"),
                      lambda s: s["slots"].append(dict(s["slots"][-1], key="second-osp"))]
        for alter in alterations:
            with self.subTest(alter=alter):
                source, sections = self.parts(); alter(source)
                with self.assertRaises(M.SourceError): M.slot_table(source, sections, "test", [self.rite])

    def test_missing_duplicate_nonadjacent_and_unknown_cue_refused(self):
        source, sections = self.parts(); slots = M.slot_table(source, sections, "test", [self.rite])
        for kind in ("missing", "duplicate", "nonadjacent", "unknown", "competing"):
            with self.subTest(kind=kind):
                edited = deepcopy(sections)
                elements = edited[0]["elements"]
                cue = elements[1]
                if kind == "missing": cue["conditions"] = []
                if kind == "duplicate": elements[0]["conditions"] = deepcopy(cue["conditions"])
                if kind == "nonadjacent": elements[0], elements[1] = elements[1], elements[0]
                if kind == "unknown": cue["conditions"][0]["rite"] = "unheld"
                if kind == "competing": cue["conditions"].append({"kind": "include-when-any"})
                with self.assertRaises(M.SourceError): M.proper_rite_coverage([self.rite], slots, edited, "test")

    def test_conditions_refuse_untyped_id_unknown_fields_and_empty_basis(self):
        for values in ({"rite": "bad id"}, {"rite": None}, {"default": True}, {"basis": " "}):
            with self.subTest(values=values):
                condition = {"kind": "include-when-proper-rite", "rite": self.rite["id"], "basis": "source"} | values
                with self.assertRaises(M.SourceError): M.element_conditions({"conditions": [condition]}, {}, "cue", "test")

    def test_every_form_routes_through_shared_source_aware_gate(self):
        ordinary = {"calendar": "roman-1962", "appointments": [], "proper_rites": [self.rite]}
        payload = {"masses": [{"key": "sample", "propers": [{"name": "Collect"}]}]}
        with patch.object(M, "check_appointment_seating", return_value=[]) as shared:
            result = M.check_calendar_seating(ordinary, payload)
            self.assertEqual(result["full_forms"], 1)
            self.assertEqual(shared.call_args.args[1][0]["mass"], "sample")
        with patch.object(M, "check_appointment_seating", return_value=[]) as shared:
            M.check_form_seating(ordinary, [{"name": "Collect"}], "test", full=True, mass="sample")
            self.assertEqual(shared.call_args.args[1][0]["mass"], "sample")

    def test_inserted_proper_rite_requires_actual_source_text(self):
        sources = self.sources
        inventory = M.read_toml(sources / "inventories/roman-1962-ordo-missae-v1.toml")
        owner = next(section for section in inventory["sections"]
                     if any(row.get("key") == "oratio-super-populum-cues" for row in section.get("inserted", [])))
        cue = next(row for row in owner["inserted"] if row["key"] == "oratio-super-populum-cues")
        section = {"key": owner["key"], "inserted": [deepcopy(cue)]}
        library = M.artifact_records(sources)
        witnesses = M.witness_table(inventory, library, "test")
        absences = M.absence_table(inventory, "test")
        target = cue["before"]

        def compile_one(value):
            return M.artifact_inserted(value, {target}, {}, absences, {}, {}, "test",
                                       witnesses=witnesses, library=library)

        before, after = compile_one(section)
        self.assertFalse(after)
        emitted = before[target][0]
        self.assertEqual({row["lang"] for row in emitted["translations"]}, {"en", "la"})
        self.assertEqual(emitted["conditions"][0]["kind"], "include-when-proper-rite")
        for fault in ("no-condition", "unknown-condition", "no-text", "unheld-artifact"):
            with self.subTest(fault=fault):
                broken = deepcopy(section)
                row = broken["inserted"][0]
                if fault == "no-condition": row.pop("conditions")
                if fault == "unknown-condition": row["conditions"][0]["kind"] = "assume-lent"
                if fault == "no-text":
                    row.pop("english"); row.pop("latin")
                    row["absent_english"] = "appointment-not-established"
                    row["absent_latin"] = "appointment-not-established"
                if fault == "unheld-artifact": row["english"]["artifact"] = "artifact.unheld"
                with self.assertRaises(M.SourceError): compile_one(broken)


if __name__ == "__main__":
    unittest.main(verbosity=2)
