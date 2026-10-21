"""Exact correlated source membership, material ownership and origin boundaries."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_SOURCE_PATH_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C

loader = importlib.machinery.SourceFileLoader("_source_path_checker", str(MODULE_ROOT / "tools/check-calendar-masses"))
spec = importlib.util.spec_from_loader(loader.name, loader)
CHECK = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = CHECK
loader.exec_module(CHECK)


def coordinate(name="Gospel", occurrence=1, mass="fixture", form_id="main"):
    return {"mass": mass, "form_id": form_id, "proper": name, "occurrence": occurrence}


def member(name="Gospel", occurrence=1, mass="fixture", form_id="main", family="cycles", cycle="A"):
    return {"appointment": coordinate(name, occurrence, mass, form_id), "material_cycle": {"family": family, "cycle": cycle}}


def proper(name, cycles=("A", "B", "C")):
    return {"name": name, "source": "scripture", "cycles": {cycle: {"verses": [{"ref": "Technical " + name + " " + cycle}]} for cycle in cycles}}


def path(identifier="principal-a", members=None, choices=None):
    return {"id": identifier, "standing": "principal", "calendar_cycles": {"family": "sunday", "in": ["A", "B", "C"]}, "choices": choices or {}, "members": members if members is not None else [member("Second Reading"), member()]}


def fixture():
    mass = {"key": "fixture", "name": "Technical source-path fixture", "registry": "fixture", "season": "lent", "propers": [proper("First Reading"), proper("Second Reading"), proper("Gospel")], "proper_source_paths": [{"id": "reading-set", "form_id": "main", "basis": "Technical exact source-membership fixture; no historical permission is asserted.", "paths": [path(), path("optional-b", [member("Second Reading", cycle="B"), member(cycle="B")])]}]}
    mass["proper_source_paths"][0]["paths"][1].update(standing="optional", calendar_cycles={"family": "sunday", "in": ["B"]})
    document = {"calendar": "postconciliar", "sections": {"seasonal": {"kind": "seasonal", "masses": [mass]}}}
    return document, mass


def grouped_fixture():
    document, mass = fixture()
    mass["propers"] = [proper("Gospel"), proper("Gospel")]
    for index, row in enumerate(mass["propers"]):
        row["ordinary_disposition"] = {"kind": "alternative", "group": "gospel", "option": "longer" if index == 0 else "shorter", "basis": "Technical exact same-seat group fixture"}
    mass["proper_source_paths"][0]["paths"] = [path("a-longer", [member()], {"gospel": "longer"}), path("a-shorter", [member(occurrence=2)], {"gospel": "shorter"})]
    return document, mass


class ProperSourcePathShapeTests(unittest.TestCase):
    def test_closed_shapes_and_course_material_pairs(self):
        _, mass = fixture()
        value = mass["proper_source_paths"]
        self.assertEqual(C.validate_proper_source_paths(value), value)
        mutations = [
            lambda r: r[0].update(source_edition="postconciliar"),
            lambda r: r[0]["paths"][0].update(default=True),
            lambda r: r[0]["paths"][0].update(standing="default"),
            lambda r: r[0]["paths"][0].update(calendar_cycles={"family": "sunday", "in": ["I"]}),
            lambda r: r[0]["paths"][0].update(calendar_cycles={"family": "weekday", "in": ["A"]}),
            lambda r: r[0]["paths"][0].update(calendar_cycles={"family": "sunday", "in": ["A", "A"]}),
            lambda r: r[0]["paths"][0].update(when={"fact": "evening", "is": 1}),
            lambda r: r[0]["paths"][0].update(when={"fact": "evening", "in": [True]}),
            lambda r: r[0]["paths"][0]["members"][0].update(material_cycle={"family": "cycles", "cycle": "I"}),
            lambda r: r[0]["paths"][0]["members"][0].update(material_cycle={"family": None, "cycle": "A"}),
        ]
        for mutate in mutations:
            bad = copy.deepcopy(value)
            mutate(bad)
            with self.subTest(value=bad), self.assertRaises(ValueError):
                C.validate_proper_source_paths(bad)

    def test_unique_relation_path_and_appointment_ids(self):
        _, mass = fixture()
        value = mass["proper_source_paths"]
        for mutate in (lambda r: r.append(copy.deepcopy(r[0])), lambda r: r[0]["paths"].append(copy.deepcopy(r[0]["paths"][0])), lambda r: r[0]["paths"][0]["members"].append(copy.deepcopy(r[0]["paths"][0]["members"][0]))):
            bad = copy.deepcopy(value); mutate(bad)
            with self.subTest(value=bad), self.assertRaises(ValueError):
                C.validate_proper_source_paths(bad)


class ProperSourcePathBindingTests(unittest.TestCase):
    def test_public_origin_and_union_guards_are_exact_and_source_is_unchanged(self):
        document, mass = fixture()
        snapshot = copy.deepcopy(document)
        rows, problems = C.resolve_propers(document, mass, appointments=True)
        self.assertEqual(problems, [])
        self.assertNotIn("appointment_identity", rows[0][1])
        self.assertEqual([p["appointment_identity"] for _, p, _ in rows[1:]], [coordinate("Second Reading"), coordinate()])
        self.assertEqual([p["source_path_relation"] for _, p, _ in rows[1:]], ["reading-set", "reading-set"])
        public = C.public_proper_source_paths(document, mass)
        self.assertEqual(public, [{**mass["proper_source_paths"][0], "source_edition": "postconciliar"}])
        self.assertEqual(document, snapshot)
        default, problems = C.resolve_propers(document, mass)
        self.assertEqual(problems, [])
        self.assertIs(default[0][1], mass["propers"][0])
        self.assertNotIn("appointment_identity", default[1][1])
        self.assertNotIn("source_path_relation", json.dumps(document))

    def test_same_name_occurrences_and_existing_long_short_ids_are_preserved(self):
        document, mass = grouped_fixture()
        rows, problems = C.resolve_propers(document, mass, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual([p["appointment_identity"]["occurrence"] for _, p, _ in rows], [1, 2])
        self.assertEqual([p["ordinary_disposition"]["option"] for _, p, _ in rows], ["longer", "shorter"])

    def test_missing_wrong_owner_form_and_material_landings_refuse(self):
        mutations = [
            lambda m: m["proper_source_paths"][0]["paths"][0]["members"][0]["appointment"].update(mass="other"),
            lambda m: m["proper_source_paths"][0]["paths"][0]["members"][0]["appointment"].update(form_id="other"),
            lambda m: m["proper_source_paths"][0]["paths"][0]["members"][0]["appointment"].update(occurrence=2),
            lambda m: m["proper_source_paths"][0]["paths"][0]["members"][0].update(material_cycle={"family": "weekday_cycles", "cycle": "I"}),
            lambda m: m["proper_source_paths"][0]["paths"][0]["members"][0].update(material_cycle={"family": None, "cycle": "all"}),
        ]
        for mutate in mutations:
            document, mass = fixture(); mutate(mass)
            with self.subTest(mass=mass):
                self.assertTrue(C.resolve_propers(document, mass)[1])

    def test_choice_namespace_tuple_and_full_bundle_are_checked(self):
        for mutation in ("collision", "unknown-group", "unknown-option", "missing-choice", "wrong-choice", "incomplete-bundle"):
            document, mass = grouped_fixture()
            relation = mass["proper_source_paths"][0]
            selected = relation["paths"][0]
            if mutation == "collision": relation["id"] = "gospel"
            elif mutation == "unknown-group": selected["choices"] = {"missing": "longer"}
            elif mutation == "unknown-option": selected["choices"] = {"gospel": "missing"}
            elif mutation == "missing-choice": selected["choices"] = {}
            elif mutation == "wrong-choice": selected["choices"] = {"gospel": "shorter"}
            else:
                extra = copy.deepcopy(mass["propers"][0]); extra["name"] = "Gospel fragment"
                mass["propers"].insert(1, extra)
            with self.subTest(mutation=mutation):
                self.assertTrue(C.resolve_propers(document, mass)[1])

    def test_relation_extents_are_disjoint(self):
        document, mass = fixture()
        other = copy.deepcopy(mass["proper_source_paths"][0]); other["id"] = "overlap"
        mass["proper_source_paths"].append(other)
        self.assertTrue(C.resolve_propers(document, mass)[1])

    def test_relation_cannot_leave_an_entire_group_option_unguarded(self):
        document, mass = grouped_fixture()
        third = copy.deepcopy(mass["propers"][0])
        third["ordinary_disposition"]["option"] = "other"
        mass["propers"].append(third)
        self.assertTrue(any("every raw member" in problem for problem in C.resolve_propers(document, mass)[1]))

    def test_relation_ids_are_scoped_to_exact_authored_forms(self):
        document, mass = fixture()
        mass.pop("propers")
        mass["forms"] = [{"id": form_id, "name": form_id.title(), "propers": [proper("Gospel")]} for form_id in ("day", "vigil")]
        mass["proper_source_paths"] = [{"id": "reading-set", "form_id": form_id, "basis": "Technical form namespace fixture", "paths": [path(members=[member(form_id=form_id)])]} for form_id in ("day", "vigil")]
        rows, problems = C.resolve_propers(document, mass, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual([p["appointment_identity"]["form_id"] for _, p, _ in rows], ["day", "vigil"])
        self.assertEqual(len(C.public_proper_source_paths(document, mass)), 2)

    def test_all_inactive_cycle_families_and_owners_validate_before_projection(self):
        for mutate in (lambda p: p.update(weekday_cycles={"I": {"verses": [{"ref": "Technical"}]}}), lambda p: p["cycles"].update(D={"verses": [{"ref": "Technical"}]}), lambda p: p["cycles"].update(C=None), lambda p: p["cycles"].update(C={}), lambda p: p["cycles"].update(C={"verses": "not a list"}), lambda p: p["cycles"].update(C={"verses": [{"ref": "Technical"}], "unexpected": True})):
            document, mass = fixture(); mutate(mass["propers"][0])
            # First Reading is not even a member of the selected relation.
            with self.subTest(proper=mass["propers"][0]):
                self.assertTrue(C.resolve_propers(document, mass)[1])

    def test_boolean_when_is_retained_without_resolving_or_manufacturing_facts(self):
        document, mass = fixture()
        mass["proper_source_paths"][0]["paths"][1]["when"] = {"fact": "prior-actual-use", "is": False}
        self.assertEqual(C.resolve_propers(document, mass)[1], [])
        public = C.public_proper_source_paths(document, mass)
        self.assertEqual(public[0]["paths"][1]["when"], {"fact": "prior-actual-use", "is": False})
        self.assertNotIn("conditionFacts", document)

    def test_material_selector_requires_a_held_nocycle_owner_and_valid_inactive_absence(self):
        document, mass = fixture()
        mass["propers"][2] = {"name": "Gospel", "source": "composed"}
        for selected in mass["proper_source_paths"][0]["paths"]:
            selected["members"][1]["material_cycle"] = {"family": None, "cycle": "all"}
        self.assertTrue(C.resolve_propers(document, mass)[1])
        document, mass = fixture()
        mass["propers"][0]["cycles"]["C"] = {"source": "composed", "text_status": {}}
        self.assertTrue(C.resolve_propers(document, mass)[1])


class ProperSourcePathReferenceTests(unittest.TestCase):
    def test_wrapper_membership_and_terminal_wording_owner_remain_distinct(self):
        document, mass = fixture()
        terminal = {"key": "wording", "propers": [proper("Gospel")]}
        document["sections"]["seasonal"]["masses"].append(terminal)
        mass["propers"][2] = {"name": "Gospel", "takes_from": {"mass": "wording", "proper": "Gospel"}}
        rows, problems = C.resolve_propers(document, mass, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual(rows[2][1]["appointment_identity"], coordinate())
        self.assertEqual(rows[2][1]["source_path_relation"], "reading-set")
        self.assertEqual(rows[2][2]["mass"], "wording")
        self.assertEqual(rows[2][1]["cycles"], terminal["propers"][0]["cycles"])

    def test_wording_borrow_does_not_inherit_target_path_guard(self):
        document, mass = fixture()
        local = {"key": "borrower", "propers": [{"name": "Gospel", "takes_from": {"mass": "fixture", "proper": "Gospel"}}]}
        document["sections"]["seasonal"]["masses"].append(local)
        rows, problems = C.resolve_propers(document, local, appointments=True)
        self.assertEqual(problems, [])
        self.assertNotIn("source_path_relation", rows[0][1])
        self.assertNotIn("appointment_identity", rows[0][1])
        self.assertEqual(rows[0][2]["mass"], "fixture")

    def test_whole_mass_does_not_rebind_relation_by_labels(self):
        document, mass = fixture()
        local = {"key": "borrower", "takes_from": {"mass": "fixture"}}
        document["sections"]["seasonal"]["masses"].append(local)
        self.assertTrue(any("exact authored relation" in problem for problem in C.resolve_propers(document, local)[1]))

    def test_wording_borrow_preserves_the_existing_legacy_group_contract(self):
        document, mass = grouped_fixture()
        mass["propers"][1]["name"] = "Gospel (vel)"
        mass["proper_source_paths"][0]["paths"][1]["members"][0]["appointment"] = coordinate("Gospel (vel)")
        local = {"key": "borrower", "propers": [{"name": name, "takes_from": {"mass": "fixture", "proper": name}} for name in ("Gospel", "Gospel (vel)")]}
        document["sections"]["seasonal"]["masses"].append(local)
        rows, problems = C.resolve_propers(document, local, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual([p["ordinary_disposition"]["option"] for _, p, _ in rows], ["longer", "shorter"])
        self.assertTrue(all("source_path_relation" not in p and "appointment_identity" not in p for _, p, _ in rows))

    def test_foreign_union_is_marked_and_original_edition_survives_multihop(self):
        document, mass = fixture()
        snapshot = copy.deepcopy(document)
        middle = C._apply_departures({"calendar": "foreign-middle", "sections": {}}, document, "postconciliar")
        target = C._apply_departures({"calendar": "foreign-target", "sections": {}}, middle, "foreign-middle")
        inherited = C.mass_index(target)["fixture"]
        rows, problems = C.resolve_propers(target, inherited, appointments=True)
        self.assertEqual(problems, [])
        self.assertNotIn("appointment_applicability", rows[0][1])
        for _, proper, _ in rows[1:]:
            self.assertEqual(proper["appointment_applicability"]["source_edition"], "postconciliar")
            self.assertEqual(proper["appointment_applicability"]["target_edition"], "foreign-target")
            self.assertEqual(proper["source_path_relation"], "reading-set")
        self.assertEqual(C.public_proper_source_paths(target, inherited)[0]["source_edition"], "postconciliar")
        self.assertEqual(document, snapshot)

    def test_foreign_grouped_union_preserves_bundle_diagnostics_and_guards(self):
        document, mass = grouped_fixture()
        target = C._apply_departures({"calendar": "foreign-target", "sections": {}}, document, "postconciliar")
        inherited = C.mass_index(target)["fixture"]
        rows, problems = C.resolve_propers(target, inherited, appointments=True)
        self.assertEqual(problems, [])
        self.assertEqual([p["ordinary_disposition"]["option"] for _, p, _ in rows], ["longer", "shorter"])
        self.assertTrue(all(p["appointment_applicability"]["source_edition"] == "postconciliar" for _, p, _ in rows))
        self.assertEqual(C.public_proper_source_paths(target, inherited)[0]["paths"], mass["proper_source_paths"][0]["paths"])

    def test_foreign_union_cannot_drop_its_unsupported_applicability_marker(self):
        document, mass = fixture()
        target = C._apply_departures({"calendar": "foreign-target", "sections": {}}, document, "postconciliar")
        inherited = C.mass_index(target)["fixture"]
        inherited["propers"][1].appointment_applicability = None
        self.assertTrue(any("unsupported applicability marker" in problem for problem in C.resolve_propers(target, inherited)[1]))

    def test_source_authored_derived_origin_or_guard_is_refused(self):
        for field, value in (("source_path_relation", "reading-set"), ("appointment_identity", coordinate())):
            document, mass = fixture(); mass["propers"][2][field] = value
            self.assertTrue(C.resolve_propers(document, mass)[1])
            problems = []
            CHECK.check_proper("fixture", mass["propers"][2], problems, calendar="postconciliar")
            self.assertTrue(any("unrecognised" in problem for problem in problems))
        document, mass = fixture(); mass["proper_source_paths"][0]["source_edition"] = "foreign"
        self.assertTrue(C.resolve_propers(document, mass)[1])

    def test_checker_accepts_mass_relation_field_and_rejects_malformed_shape(self):
        document, mass = fixture()
        problems = []; CHECK.check_entry(mass, 0, problems, "seasonal", "postconciliar")
        self.assertFalse(any("proper_source_paths" in problem and "unknown" in problem for problem in problems))
        mass["proper_source_paths"][0]["paths"][0]["when"] = {"fact": "evening", "is": "true"}
        problems = []; CHECK.check_entry(mass, 0, problems, "seasonal", "postconciliar")
        self.assertTrue(any("boolean" in problem for problem in problems))


if __name__ == "__main__":
    unittest.main()
