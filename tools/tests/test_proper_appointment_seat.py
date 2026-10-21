"""An exact source seat qualifies anchored alternatives without renaming rows."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_MODULE_ROOT", ROOT))
TOOL_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_TOOL_ROOT", ROOT))
SOURCE_FILE = Path(os.environ.get("TRIPTYCH_APPOINTMENT_SOURCE_FILE", ROOT / "src/sources/calendars/roman-1962/propers.yaml"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C


def producer():
    loader = importlib.machinery.SourceFileLoader("_seat_producer", str(TOOL_ROOT / "tools/mass-propers"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


COMMON = "commune-unius-martyris-3"
GROUP = "unius-martyris-3-first-reading"
ANCHOR = {"mass": COMMON, "form_id": "main", "proper": "Lesson", "occurrence": 1}


def source_fixture():
    source = C.load_document(SOURCE_FILE.parent.parent, "roman-1962", effective=False)
    mass = C.mass_index(source)[COMMON]
    return source, mass


def group_members(mass):
    return [proper for proper in mass["propers"]
            if proper.get("ordinary_disposition", {}).get("group") == GROUP]


class ProperAppointmentSeatTests(unittest.TestCase):
    def test_actual_lesson_group_keeps_source_names_and_exact_appointment_identity(self):
        source, mass = source_fixture()
        snapshot = copy.deepcopy(mass)
        members = group_members(mass)
        self.assertEqual([proper["name"] for proper in members], ["Lesson", "Lesson (altera Epistola in Communi unius Martyris)"])
        self.assertEqual([proper["ordinary_disposition"]["seat"] for proper in members], ["reading-1", "reading-1"])
        self.assertEqual([proper["ordinary_disposition"]["anchor"] for proper in members], [ANCHOR, ANCHOR])
        self.assertEqual(members[0]["verses"][0]["ref"], "Wisdom 10:10-14")
        entries, problems = C.resolve_propers(source, mass, appointments=True)
        self.assertEqual(problems, [])
        appointed = [(proper, owner) for _, proper, owner in entries
                     if proper.get("ordinary_disposition", {}).get("group") == GROUP]
        self.assertEqual(appointed[0][0]["appointment_identity"], ANCHOR)
        alternative, owner = appointed[1]
        self.assertEqual(alternative["appointment_identity"], {**ANCHOR, "proper": members[1]["name"]})
        self.assertEqual(alternative["verses"][0]["ref"], "James 1:2-12")
        self.assertEqual(owner["mass"], "commune-unius-martyris-1")
        self.assertEqual(owner["proper"], "Epistle (altera in Communi unius Martyris)")
        self.assertEqual(mass, snapshot)

    def test_source_seat_is_transported_without_normalizing_the_disposition(self):
        _, mass = source_fixture()
        project = producer().public_ordinary_disposition
        for proper in group_members(mass):
            disposition = proper["ordinary_disposition"]
            with self.subTest(proper=proper["name"]):
                self.assertEqual(C.validate_ordinary_disposition(disposition), disposition)
                self.assertEqual(project(disposition), disposition)

    def test_seat_enum_and_closed_shapes_refuse_forged_or_cross_seat_values(self):
        _, mass = source_fixture()
        valid = group_members(mass)[0]["ordinary_disposition"]
        for seat in (None, False, 1, [], ["reading-1"], "", "reading-1 ", "reading-2", "gospel", "collect"):
            with self.subTest(seat=seat), self.assertRaisesRegex(ValueError, "seat"):
                C.validate_ordinary_disposition({**valid, "seat": seat})
        legacy = {key: value for key, value in valid.items() if key != "anchor"}
        conditional = {"kind": "conditional", "group": "condition", "basis": "Technical closed-shape fixture.", "when": {"fact": "fact", "in": ["held"]}, "seat": "reading-1"}
        unplaced = {"kind": "unplaced", "group": "before-mass", "region": "before-frame", "basis": "Technical closed-shape fixture.", "seat": "reading-1"}
        for disposition in (legacy, conditional, unplaced):
            with self.subTest(disposition=disposition), self.assertRaisesRegex(ValueError, "seat"):
                C.validate_ordinary_disposition(disposition)

    def test_every_member_must_declare_identical_seat_presence(self):
        source, mass = source_fixture()
        for changed in range(2):
            fixture = copy.deepcopy(source)
            local = C.mass_index(fixture)[COMMON]
            del group_members(local)[changed]["ordinary_disposition"]["seat"]
            with self.subTest(changed=changed):
                self.assertTrue(any("identical seat presence and value" in error
                                    for error in C.resolve_propers(fixture, local)[1]))

    def test_seat_does_not_relax_exact_anchor_membership(self):
        source, _ = source_fixture()
        for forged in ({**ANCHOR, "occurrence": 2}, {**ANCHOR, "mass": "commune-unius-martyris-1"}):
            fixture = copy.deepcopy(source)
            mass = C.mass_index(fixture)[COMMON]
            for proper in group_members(mass):
                proper["ordinary_disposition"]["anchor"] = dict(forged)
            with self.subTest(anchor=forged):
                self.assertTrue(any("anchor must be one exact member" in error
                                    for error in C.resolve_propers(fixture, mass)[1]))


if __name__ == "__main__":
    unittest.main()
