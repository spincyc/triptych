"""Producer transport preserves exact source paths, all material, and origin."""
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
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_SOURCE_PATH_CORE", ROOT))
PRODUCER_ROOT = Path(os.environ.get("TRIPTYCH_SOURCE_PATH_PRODUCER", ROOT))
BASELINE_ROOT = Path(os.environ["TRIPTYCH_SOURCE_PATH_BASELINE"]) if os.environ.get("TRIPTYCH_SOURCE_PATH_BASELINE") else None
FIXTURE = Path(os.environ["TRIPTYCH_SOURCE_PATH_FIXTURE"]) if os.environ.get("TRIPTYCH_SOURCE_PATH_FIXTURE") else None
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(MODULE_ROOT / "scripts"))
import _calendars as C


def producer(path, name):
    loader = importlib.machinery.SourceFileLoader(name, str(path / "tools/mass-propers"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    for key, value in list(vars(module).items()):
        if isinstance(value, Path) and value.is_relative_to(path):
            setattr(module, key, ROOT / value.relative_to(path))
    module.ROOT = ROOT
    return module


MP = producer(PRODUCER_ROOT, "_source_path_producer")
OLD = producer(BASELINE_ROOT, "_source_path_producer_before") if BASELINE_ROOT else None


def fixture():
    source = C.load_document(ROOT / "src/sources/calendars", "postconciliar", effective=False)
    source = copy.deepcopy(source)
    # The tracked source after integration is the durable fixture. Before
    # integration, consume the source owner's exact frozen authored Mass.
    mass = C.read_yaml(FIXTURE) if FIXTURE is not None else C.mass_index(source)["lent-3"]
    source["sections"] = {"seasonal": {"kind": "seasonal", "masses": [mass]}}
    source.pop("citation_divergences", None)  # outside this one-Mass projection
    return source, mass


def structure(source, mod=MP):
    with patch.object(mod, "load_calendar", return_value=source):
        return mod.calendar_structure(ROOT / "src/sources/calendars", source["calendar"], mod.book_tokens())


def show(source, mass, mod=MP, foreign=False):
    args = argparse.Namespace(root=str(ROOT / "src/sources/calendars"), calendar=source["calendar"], mass=mass["key"],
                              lang="la", witness=None, bible=None, bible_root=str(ROOT / "src/sources/bibles"), form=None)
    with patch.object(mod, "load_calendar", return_value=source):
        if foreign:
            with patch.object(mod, "translation_overlay", return_value=({}, {}, [], {})), patch.object(mod, "publication_records", return_value=({}, [])):
                return mod.run_show_one(args)
        return mod.run_show_one(args)


def token(coordinate):
    return tuple(coordinate[field] for field in ("mass", "form_id", "proper", "occurrence"))


class ProperSourcePathProducerTests(unittest.TestCase):
    def test_actual_lent_three_structure_keeps_seven_paths_and_exact_union_guards(self):
        source, mass = fixture()
        before = copy.deepcopy(mass)
        built = structure(source)["masses"][0]
        relations = built[C.PROPER_SOURCE_PATHS]
        self.assertEqual(len(relations), 1)
        self.assertEqual(len(relations[0]["paths"]), 7)
        self.assertEqual(relations[0]["source_edition"], "postconciliar")
        self.assertEqual({key: value for key, value in relations[0].items() if key != "source_edition"}, mass[C.PROPER_SOURCE_PATHS][0])
        union = {token(member["appointment"]) for path in relations[0]["paths"] for member in path["members"]}
        guarded = [proper for proper in built["propers"] if C.SOURCE_PATH_RELATION in proper]
        self.assertEqual({token(proper["appointment_identity"]) for proper in guarded}, union)
        self.assertEqual({proper[C.SOURCE_PATH_RELATION] for proper in guarded}, {"lent-3-readings"})
        self.assertEqual([proper["name"] for proper in built["propers"]], [proper["name"] for proper in mass["propers"]])
        for raw, public in zip(mass["propers"], built["propers"]):
            self.assertEqual(set(raw.get("cycles") or {}), set(public.get("cycles") or {}))
        self.assertEqual(mass, before)

    def test_show_keeps_origin_and_appointed_guards_without_changing_raw_material(self):
        source, mass = fixture()
        before = copy.deepcopy(mass)
        payload = show(source, mass)
        self.assertEqual(payload["mass"][C.PROPER_SOURCE_PATHS][0]["source_edition"], "postconciliar")
        guarded = [row["proper"] for row in payload["appointed"] if C.SOURCE_PATH_RELATION in row["proper"]]
        self.assertEqual(len(guarded), 7)
        self.assertTrue(all(proper.get("appointment_identity") for proper in guarded))
        for raw, public in zip(mass["propers"], payload["mass"]["propers"]):
            self.assertEqual(raw.get("cycles"), public.get("cycles"))
        self.assertEqual(mass, before)

    def test_foreign_show_preserves_original_edition_before_publication_copy(self):
        source, _ = fixture()
        target = {"calendar": "foreign-target", "psalm_numbering": "hebrew", "sections": {}}
        foreign = C._apply_departures(target, source, "postconciliar")
        mass = C.mass_index(foreign)["lent-3"]
        payload = show(foreign, mass, foreign=True)
        self.assertEqual(payload["mass"][C.PROPER_SOURCE_PATHS][0]["source_edition"], "postconciliar")
        guarded = [row["proper"] for row in payload["appointed"] if C.SOURCE_PATH_RELATION in row["proper"]]
        self.assertEqual(len(guarded), 7)
        for proper in guarded:
            self.assertEqual(proper[C.APPOINTMENT_APPLICABILITY]["source_edition"], "postconciliar")
            self.assertEqual(proper[C.APPOINTMENT_APPLICABILITY]["target_edition"], "foreign-target")
        self.assertNotIn("source_edition", dict(mass[C.PROPER_SOURCE_PATHS][0]))

    def test_recursive_public_guard_uses_canonical_validator(self):
        value = {"forms": [{"propers": [{C.SOURCE_PATH_RELATION: "lent-3-readings"}]}]}
        with patch.object(C, "validate_source_path_relation", wraps=C.validate_source_path_relation) as validate:
            self.assertEqual(MP.rights_safe_copy(value), value)
            validate.assert_called_once_with("lent-3-readings")
        for invalid in (None, {}, [], "", "Lent-3", "lent-3/readings"):
            value["forms"][0]["propers"][0][C.SOURCE_PATH_RELATION] = invalid
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                MP.rights_safe_copy(value)

    def test_invalid_inactive_cycles_and_forged_origin_are_refused_before_publication(self):
        for problem in ("inactive-cycle", "source-origin"):
            source, mass = fixture()
            if problem == "inactive-cycle":
                row = next(row for row in mass["propers"] if row["name"] == "First Reading")
                row["cycles"]["D"] = copy.deepcopy(row["cycles"]["A"])
            else:
                mass[C.PROPER_SOURCE_PATHS][0]["source_edition"] = "forged-source"
            with self.subTest(problem=problem):
                with self.assertRaises(ValueError):
                    structure(source)
                with patch.object(MP, "sanitize_mass", side_effect=AssertionError("publication reached invalid source")), self.assertRaises(ValueError):
                    show(source, mass)

    def test_ordinary_payload_is_identical_to_baseline_when_relation_is_absent(self):
        source, mass = fixture()
        del mass[C.PROPER_SOURCE_PATHS]
        if OLD is not None:
            self.assertEqual(structure(source), structure(source, OLD))
            self.assertEqual(show(source, mass), show(source, mass, OLD))
        self.assertNotIn(C.PROPER_SOURCE_PATHS, show(source, mass)["mass"])
        self.assertFalse(any(C.SOURCE_PATH_RELATION in proper for proper in structure(source)["masses"][0]["propers"]))


if __name__ == "__main__":
    unittest.main()
