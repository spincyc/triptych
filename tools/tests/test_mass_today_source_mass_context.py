"""Appointment facts use the selected source Mass, separate from text owners."""
from __future__ import annotations

import argparse
import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
CORE = Path(os.environ.get("TRIPTYCH_MASS_VALUES_CORE", ROOT))
CLI = Path(os.environ.get("TRIPTYCH_MASS_VALUES_CLI", ROOT))
PRODUCER = Path(os.environ.get("TRIPTYCH_MASS_VALUES_PRODUCER", ROOT))
SOURCE_FILE = Path(os.environ.get("TRIPTYCH_MASS_VALUES_SOURCE", ROOT / "src/sources/calendars/roman-1962/propers.yaml"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(CORE / "scripts"))
import _calendars as C


def load_tool(name, base):
    loader = importlib.machinery.SourceFileLoader("_mass_context_" + name.replace("-", "_"), str(base / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(base):
            setattr(module, key, ROOT / value.relative_to(base))
    module.ROOT = ROOT
    return module


TODAY = load_tool("mass-today", CLI)
MP = load_tool("mass-propers", PRODUCER)
FACT = "roman-1962-non-virginum-2-subject"
COMMON = "commune-non-virginum-2"


def fixture():
    source = C.read_yaml(SOURCE_FILE)
    bindings = source[C.PROPER_APPOINTMENT_FACTS][FACT]["mass_values"]
    assert len(bindings) == 6
    mass = C.mass_index(source)[next(iter(bindings))]
    return source, mass


class SourceMassAppointmentContextTests(unittest.TestCase):
    def test_context_always_uses_selected_source_mass_and_preserves_owner_facts(self):
        source, selected = fixture()
        facts = copy.deepcopy(source[C.PROPER_APPOINTMENT_FACTS])
        index = C.mass_index(source)
        for mass in (selected, index[COMMON]):
            held = {**mass, C.PROPER_APPOINTMENT_FACTS: facts}
            snapshot = copy.deepcopy(held)
            predicates = {"date": "2026-03-09", "season": "lent", "mass": COMMON, "source_mass": "untrusted-restatement"}
            for choices in (None, []):
                with self.subTest(selected=mass["key"], choices=choices):
                    context = TODAY.proper_appointment_context_for("roman-1962", held, predicates, choices)
                    self.assertEqual(context["mass"], mass["key"])
                    self.assertEqual(context["facts"], facts)
                    self.assertEqual(context["choices"], {})
                    self.assertEqual(context["season"], "lent")
                    self.assertEqual(context["date"], predicates["date"])
                    self.assertNotIn("source_mass", context)
            self.assertEqual(held, snapshot)
        self.assertNotEqual(selected["key"], selected["takes_from"]["mass"])

    def test_choice_scope_remains_selected_mass_qualified_and_does_not_assert_eligibility(self):
        source, selected = fixture()
        mass = {**selected, C.PROPER_APPOINTMENT_FACTS: source[C.PROPER_APPOINTMENT_FACTS]}
        prefix = f"proper-choice/roman-1962/{mass['key']}/main/non-virginum-2-reading"
        option = next(row["ordinary_disposition"]["option"] for row in C.mass_index(source)[COMMON]["propers"]
                      if row.get("ordinary_disposition", {}).get("group") == "non-virginum-2-reading")
        request = prefix + "=" + option
        context = TODAY.proper_appointment_context_for("roman-1962", mass, {}, [request])
        self.assertEqual(context["mass"], selected["key"])
        self.assertEqual(context["choices"], {"main/non-virginum-2-reading": option})
        self.assertEqual(context["facts"], source[C.PROPER_APPOINTMENT_FACTS])
        for requests in ([request, request], [request.replace(selected["key"], COMMON)], [request.replace("roman-1962", "roman-pre-1955")]):
            with self.subTest(requests=requests), self.assertRaises(TODAY.Refused):
                TODAY.proper_appointment_context_for("roman-1962", mass, {}, requests)

    def test_existing_producer_transports_mass_bindings_without_a_new_schema_or_wording_owner(self):
        source, selected = fixture()
        source.pop("citation_divergences", None)  # unrelated global targets outside focused view
        common = C.mass_index(source)[COMMON]
        facts = copy.deepcopy(source[C.PROPER_APPOINTMENT_FACTS])
        self.assertEqual(C.validate_proper_appointment_facts(facts, "roman-1962", document=source), facts)
        with patch.object(MP, "load_calendar", return_value=source), patch.object(MP, "masses_of", return_value=[("common", common)]), patch.object(MP._oration_execution, "load_sources", return_value={}), patch.object(MP._name_execution, "load_name_sources", return_value={}), patch.object(C, "validate_proper_appointment_facts", wraps=C.validate_proper_appointment_facts) as validate:
            structure = MP.calendar_structure(ROOT / "src/sources/calendars", "roman-1962", MP.book_tokens())
            self.assertTrue(validate.called)
        self.assertEqual(structure[C.PROPER_APPOINTMENT_FACTS], facts)
        args = argparse.Namespace(root=str(ROOT / "src/sources/calendars"), calendar="roman-1962", mass=selected["key"],
                                  lang="la", witness=None, bible=None, bible_root=str(ROOT / "src/sources/bibles"), form=None)
        with patch.object(MP, "load_calendar", return_value=source):
            shown = MP.run_show_one(args)
        self.assertEqual(shown[C.PROPER_APPOINTMENT_FACTS], facts)
        daily = TODAY.propers_of("roman-1962", selected["key"], args, payload=shown)
        daily["key"] = selected["key"]
        self.assertEqual(daily[C.PROPER_APPOINTMENT_FACTS], facts)
        context = TODAY.proper_appointment_context_for("roman-1962", daily, {})
        self.assertEqual(context["mass"], selected["key"])
        inherited = [row for row in shown["appointed"] if row["proper"].get("ordinary_disposition", {}).get("group") == "non-virginum-2-reading"]
        self.assertEqual(len(inherited), 2)
        self.assertTrue(all(row["proper"]["appointment_identity"]["mass"] == COMMON for row in inherited))
        self.assertTrue(all(row["taken_from"]["mass"] != selected["key"] for row in inherited))
        self.assertNotIn(context["mass"], {row["proper"]["appointment_identity"]["mass"] for row in inherited})


if __name__ == "__main__":
    unittest.main()
