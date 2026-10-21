"""Whole local Common-set replacement needs no inherited option selection."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import itertools
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_COMMON_OVERRIDE_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C


def checker():
    loader = importlib.machinery.SourceFileLoader("_common_override_checker", str(MODULE_ROOT / "tools/check-calendar-masses"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(MODULE_ROOT):
            setattr(module, key, ROOT / value.relative_to(MODULE_ROOT))
    module.ROOT = ROOT
    return module


CHECK = checker()
FAMILIES = ["Collect", "Secret", "Postcommunion"]


def composed(name, text):
    return {"name": name, "source": "composed", "text": text}


def fixture():
    common = {"key": "commune", "common_sets": {"orations": {
        "families": list(FAMILIES),
        # Deliberately reverse option declaration order. Positional anchors
        # follow the actual source rows rather than a chosen option.
        "options": {"c2": [name + " (altera)" for name in FAMILIES], "c1": list(FAMILIES)},
    }}, "propers": [
        composed("Introit", "Inherited Introit technical fixture"),
        composed("Collect", "Common Collect one technical fixture"),
        composed("Collect (altera)", "Common Collect two technical fixture"),
        composed("Epistle", "Inherited Epistle technical fixture"),
        composed("Secret", "Common Secret one technical fixture"),
        composed("Secret (altera)", "Common Secret two technical fixture"),
        composed("Communion", "Inherited Communion technical fixture"),
        composed("Postcommunion", "Common Postcommunion one technical fixture"),
        composed("Postcommunion (altera)", "Common Postcommunion two technical fixture"),
    ]}
    saint = {"key": "saint", "takes_from": {"mass": "commune"},
             "propers": [composed(name, "Own " + name + " technical fixture") for name in FAMILIES]}
    source = {"sections": {
        "common": {"kind": "common", "masses": [common]},
        "sanctoral": {"kind": "sanctoral", "masses": [saint]},
    }}
    return source, common, saint


def join(common, saint, kind="common"):
    return CHECK.common_reference_problems([(kind, common), ("sanctoral", saint)])


class CommonSetLocalOverrideTests(unittest.TestCase):
    def test_complete_local_families_replace_one_source_position_each_without_choosing_a_set(self):
        source, common, saint = fixture()
        snapshot = copy.deepcopy(source)
        anchors, families, problems = C._common_set_propers(common, saint["takes_from"], "fixture", set(FAMILIES))
        self.assertEqual(problems, [])
        self.assertEqual(families, set(FAMILIES))
        self.assertEqual([proper["name"] for proper in anchors], ["Introit", "Collect", "Epistle", "Secret", "Communion", "Postcommunion"])
        entries, problems = C.resolve_propers(source, saint)
        self.assertEqual(problems, [])
        self.assertEqual(join(common, saint), [])
        self.assertEqual([proper["name"] for _, proper, _ in entries], [proper["name"] for proper in anchors])
        for family, local in zip(FAMILIES, saint["propers"]):
            row = next(entry for entry in entries if entry[1]["name"] == family)
            self.assertIs(row[1], local)
            self.assertIsNone(row[2])
        self.assertFalse(any(proper.get("text", "").startswith("Common ") for _, proper, _ in entries))
        self.assertNotIn("common_sets", saint["takes_from"])
        self.assertEqual(source, snapshot)

    def test_each_partial_local_family_set_still_requires_a_common_disposition(self):
        for size in range(len(FAMILIES)):
            for present in itertools.combinations(FAMILIES, size):
                source, common, saint = fixture()
                saint["propers"] = [proper for proper in saint["propers"] if proper["name"] in present]
                with self.subTest(families=present):
                    self.assertTrue(C.resolve_propers(source, saint)[1])
                    self.assertTrue(join(common, saint))

    def test_explicit_empty_malformed_and_wrong_selectors_are_not_bypassed(self):
        bad = [None, [], {}, {"orations": None}, {"orations": {}},
               {"orations": {"state": "selected", "option": "c9"}},
               {"orations": {"state": "unresolved", "candidates": ["c3", "c4"]}},
               {"orations": {"state": "replaced"}},
               {"unknown": {"state": "selected", "option": "c1"}}]
        for selection in bad:
            source, common, saint = fixture()
            saint["takes_from"]["common_sets"] = selection
            with self.subTest(selection=selection):
                self.assertTrue(C.resolve_propers(source, saint)[1])
                shape = []
                CHECK.check_reference("fixture", saint["takes_from"], shape, on_proper=False)
                self.assertTrue(shape + join(common, saint))
        for disposition in ({"state": "selected", "option": "c1", "candidates": ["c1", "c2"]},
                            {"state": "unresolved", "candidates": ["c1", "c2"], "option": "c1"},
                            {"state": "selected", "option": "c1", "invented": True}):
            _, common, saint = fixture()
            saint["takes_from"]["common_sets"] = {"orations": disposition}
            problems = []
            CHECK.check_reference("fixture", saint["takes_from"], problems, on_proper=False)
            self.assertTrue(problems)

    def test_existing_valid_selected_and_unresolved_dispositions_still_work(self):
        for disposition in ({"state": "selected", "option": "c2"},
                            {"state": "unresolved", "candidates": ["c1", "c2"]}):
            source, common, saint = fixture()
            saint["takes_from"]["common_sets"] = {"orations": disposition}
            with self.subTest(disposition=disposition):
                entries, problems = C.resolve_propers(source, saint)
                self.assertEqual(problems, [])
                self.assertEqual(join(common, saint), [])
                self.assertEqual(sum(proper in saint["propers"] and owner is None for _, proper, owner in entries), 3)

    def test_one_fully_replaced_group_does_not_disposition_another_group(self):
        source, common, saint = fixture()
        common["common_sets"]["chant"] = {"families": ["Alleluia"], "options": {"one": ["Alleluia"], "two": ["Alleluia (altera)"]}}
        common["propers"].extend([composed("Alleluia", "One technical chant"), composed("Alleluia (altera)", "Other technical chant")])
        self.assertTrue(C.resolve_propers(source, saint)[1])
        self.assertTrue(join(common, saint))
        saint["takes_from"]["common_sets"] = {"chant": {"state": "selected", "option": "two"}}
        entries, problems = C.resolve_propers(source, saint)
        self.assertEqual(problems, [])
        self.assertEqual(join(common, saint), [])
        self.assertEqual(entries[-1][1]["name"], "Alleluia (altera)")

    def test_malformed_or_empty_family_declarations_do_not_enable_omission(self):
        for families in ([], None, {}, ["Collect", None], ["Collect", "Collect"], [""]):
            source, common, saint = fixture()
            common["common_sets"]["orations"]["families"] = families
            with self.subTest(families=families):
                self.assertTrue(C.resolve_propers(source, saint)[1])
                self.assertTrue(join(common, saint))
        for options in ({}, [], {"unknown": ["Missing Collect", "Missing Secret", "Missing Postcommunion"]}):
            source, common, saint = fixture()
            common["common_sets"]["orations"]["options"] = options
            with self.subTest(options=options):
                self.assertTrue(C.resolve_propers(source, saint)[1])

    def test_complete_local_families_do_not_allow_foreign_or_unknown_common_targets(self):
        source, common, saint = fixture()
        self.assertTrue(join(common, saint, kind="seasonal"))
        saint["takes_from"]["calendar"] = "another-calendar"
        problems = []
        CHECK.check_reference("fixture", saint["takes_from"], problems, on_proper=False)
        self.assertTrue(any("unknown field" in problem for problem in problems))
        saint["takes_from"] = {"mass": "foreign-calendar-common"}
        self.assertTrue(any("no entry" in problem for problem in C.resolve_propers(source, saint)[1]))
        saint["takes_from"] = {"mass": "commune", "common_sets": {"unknown": {"state": "selected", "option": "c1"}}}
        self.assertTrue(join(common, saint))
        self.assertTrue(C.resolve_propers(source, saint)[1])

    def test_duplicate_local_family_remains_a_source_gate_error(self):
        _, common, saint = fixture()
        saint["propers"].append(composed("Collect (another)", "Duplicate technical fixture"))
        self.assertTrue(any("repeat" in problem for problem in join(common, saint)))

    def test_local_family_consumed_by_an_exact_appointment_override_cannot_justify_omission(self):
        source, common, saint = fixture()
        anchor = {"mass": "commune", "form_id": "main", "proper": "Introit", "occurrence": 1}
        common["propers"].insert(1, composed("Introit (altera)", "Second Common Introit technical fixture"))
        for proper, option in zip(common["propers"][:2], ("first", "second")):
            proper["ordinary_disposition"] = {"kind": "alternative", "group": "introits", "option": option,
                                               "anchor": dict(anchor), "basis": "Technical exact replacement fixture."}
        saint["takes_from"]["appointment_overrides"] = [{"mass": "commune", "form_id": "main", "group": "introits", "state": "replaced",
            "by": [{"mass": "saint", "form_id": "main", "proper": "Collect", "occurrence": 1}],
            "basis": "Technical source-coordinate consumption fixture."}]
        entries, problems = C.resolve_propers(source, saint)
        self.assertTrue(any("disposition" in problem for problem in problems))
        self.assertTrue(join(common, saint))
        self.assertFalse(any(proper.get("text", "").startswith("Common ") for _, proper, _ in entries))
        self.assertEqual(C.common_set_local_override_families(saint), {"Secret", "Postcommunion"})

    def test_independent_exact_replacement_keeps_all_remaining_oration_families_eligible(self):
        source, common, saint = fixture()
        anchor = {"mass": "commune", "form_id": "main", "proper": "Gospel", "occurrence": 1}
        rows = []
        for name, option in (("Gospel", "first"), ("Gospel (altera)", "second")):
            proper = composed(name, "Common Gospel technical fixture")
            proper["ordinary_disposition"] = {"kind": "alternative", "group": "gospels", "option": option,
                                               "anchor": dict(anchor), "basis": "Technical exact replacement fixture."}
            rows.append(proper)
        common["propers"][4:4] = rows
        local_gospel = composed("Gospel", "Own Gospel technical fixture")
        saint["propers"].append(local_gospel)
        saint["takes_from"]["appointment_overrides"] = [{"mass": "commune", "form_id": "main", "group": "gospels", "state": "replaced",
            "by": [{"mass": "saint", "form_id": "main", "proper": "Gospel", "occurrence": 1}],
            "basis": "Technical independent replacement fixture."}]
        entries, problems = C.resolve_propers(source, saint)
        self.assertEqual(problems, [])
        self.assertEqual(join(common, saint), [])
        self.assertEqual(C.common_set_local_override_families(saint), set(FAMILIES))
        self.assertFalse(any(proper.get("text", "").startswith("Common ") for _, proper, _ in entries))
        self.assertEqual(sum(proper["name"] == "Gospel" for _, proper, _ in entries), 1)


if __name__ == "__main__":
    unittest.main()
