"""Three positively attested 2008 own Collect roles, without invented bodies."""
from __future__ import annotations

import copy
import json
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _missal_coverage as coverage

DATA = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
LEDGER = ROOT / "src/sources/inventories/postconciliar-proper-translations-v1.toml"
EXPECTED = ROOT / "src/sources/inventories/missal-expected-targets-v1.toml"
SEGMENT = "segment.holy-see.variationes-et-additiones-missalis-romani-2008.latin-notitiae-503-504.notitiae-pages-368-387"
CASES = {
    "saint-turibius-mogrovejo-bishop": ("03-23", 434, 737),
    "saint-maria-goretti-virgin-martyr": ("07-06", 464, 786),
    "dedication-basilica-saint-mary-major": ("08-05", 474, 799),
}

EXISTING_SUPPLEMENT_COLLECTS = {
    "postconciliar:2008:supplement:pio-collect": "saint-pius-pietrelcina-priest",
    "postconciliar:2008:supplement:juan-diego-collect": "saint-juan-diego-cuauhtlatoatzin",
    "postconciliar:2008:supplement:guadalupe-collect": "our-lady-guadalupe",
}


def target_id(date):
    return f"postconciliar.2002.sanctoral.{date}.1:collect:1"


def load_propers():
    loader = SourceFileLoader("_pc_collect_appointments", str(ROOT / "tools/mass-propers"))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module


class PostconciliarSanctoralCollectAppointmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(DATA.read_text())
        cls.masses = [mass for section in cls.document["sections"].values()
                      for mass in section["masses"]]
        cls.by_key = {mass["key"]: mass for mass in cls.masses}
        cls.ledger = tomllib.loads(LEDGER.read_text())
        cls.inventory = tomllib.loads(EXPECTED.read_text())
        cls.targets = {row["id"]: row for row in cls.inventory["targets"]}
        cls.propers = load_propers()

    def test_exact_own_collect_order_and_existing_reading_course(self):
        for key, (date, _, _) in CASES.items():
            with self.subTest(mass=key):
                mass = self.by_key[key]
                self.assertEqual(mass["date"], date)
                self.assertEqual(mass["text_status"]["state"], "partial")
                entries, problems = _calendars.resolve_propers(self.document, mass)
                self.assertEqual(problems, [])
                self.assertEqual([proper["name"] for _, proper, _ in entries],
                                 ["Collect", "First Reading", "Responsorial Psalm",
                                  "Gospel Acclamation", "Gospel"])
                self.assertTrue(all(origin is None for _, _, origin in entries))
                self.assertNotIn("takes_from", mass)
                self.assertNotIn("common_sets", mass)

    def test_appointment_proof_does_not_invent_text_or_publication_basis(self):
        for key, (date, ap, printed) in CASES.items():
            with self.subTest(mass=key):
                proper = self.by_key[key]["propers"][0]
                self.assertEqual(proper["source"], "composed")
                self.assertEqual(proper["text_status"], {
                    "state": "unavailable", "scope": "proper-body",
                    "reasons": [{"kind": "witness-gap", "source_id": SEGMENT}],
                })
                for field in ("text", "incipit", "translations", "publication_basis",
                              "body_sha256", "takes_from", "text_from"):
                    self.assertNotIn(field, proper)
                for locator in (date, str(ap), str(printed), target_id(date), "2008"):
                    self.assertIn(locator, proper["notes"])

    def test_exact_english_absences_answer_production_slot_identities(self):
        overlay, untranslated, stale, _ = self.propers.translation_overlay(
            "postconciliar", ROOT / "src/sources/calendars")
        self.assertEqual(stale, [])
        for key in CASES:
            with self.subTest(mass=key):
                mass = self.by_key[key]
                proper = mass["propers"][0]
                identity = self.propers.source_slot_identity(
                    self.document, mass, "", proper, None)
                self.assertEqual(identity, (key, "main", "Collect", 1))
                units = self.propers.coverage_slot_units(proper, identity)
                self.assertEqual(len(units), 1)
                identity, owner = units[0]
                self.assertIs(owner, proper)
                self.assertEqual(identity, (key, "main", "Collect", "all", 1))
                matches = self.propers.matching_untranslated_records(
                    proper, untranslated[self.propers.untranslated_key(identity)],
                    1, cycle="all", extent="body")
                self.assertEqual(len(matches), 1)
                row = matches[0]
                self.assertEqual(row["lang"], "en")
                self.assertEqual(row["availability"], "unavailable")
                self.assertEqual(row["reason"], {"kind": "no-exemplar"})
                self.assertNotIn("witness_passage_id", row)
                self.assertFalse(self.propers.translation_entry_for(
                    overlay, self.propers.overlay_key(mass, "", proper, None), identity))

    def test_source_hierarchy_preserved_and_exact_slots_join(self):
        states = {row["id"]: row["state"] for row in coverage.expectations(
            EXPECTED, "postconciliar", self.masses)["targets"]}
        for key, (date, _, _) in CASES.items():
            with self.subTest(mass=key):
                target = self.targets[target_id(date)]
                parent = self.targets[target["parent_id"]]
                self.assertEqual(parent["kind"], "collect-category")
                self.assertEqual(parent["identity_state"], "target-correspondence-unresolved")
                self.assertNotIn("calendar_mass_key", parent)
                self.assertEqual(target["calendar_mass_key"], key)
                self.assertEqual(target["form_id"], "main")
                self.assertEqual(target["calendar_proper_name"], "Collect")
                self.assertEqual(target["identity_state"], "established")
                self.assertEqual(states[target_id(date)], "represented")
                self.assertIn("notitiae-pages-368-387.toml", target["source_record"])

    def test_existing_supplement_collects_join_exact_roles_without_payload_change(self):
        states = {row["id"]: row["state"] for row in coverage.expectations(
            EXPECTED, "postconciliar", self.masses)["targets"]}
        for identifier, key in EXISTING_SUPPLEMENT_COLLECTS.items():
            with self.subTest(mass=key):
                target = self.targets[identifier]
                self.assertEqual(target["calendar_mass_key"], key)
                self.assertEqual(target["form_id"], "main")
                self.assertEqual(target["calendar_proper_name"], "Collect")
                self.assertEqual(states[identifier], "represented")
                mass = self.by_key[key]
                collect = next(p for p in mass["propers"] if p["name"] == "Collect")
                self.assertIn("official 2008 Supplementum", collect["notes"])
                self.assertFalse(collect.get("text"))
                damaged = copy.deepcopy(self.masses)
                owner = next(m for m in damaged if m["key"] == key)
                owner["propers"] = [p for p in owner["propers"] if p["name"] != "Collect"]
                changed = {row["id"]: row["state"] for row in coverage.expectations(
                    EXPECTED, "postconciliar", damaged)["targets"]}
                self.assertEqual(changed[identifier], "not-represented")

    def test_deleting_collect_or_selecting_foreign_form_cannot_borrow_readings(self):
        for key, (date, _, _) in CASES.items():
            for change in ("deleted", "foreign-form", "duplicate"):
                with self.subTest(mass=key, change=change):
                    damaged = copy.deepcopy(self.masses)
                    mass = next(m for m in damaged if m["key"] == key)
                    if change == "deleted":
                        mass["propers"] = mass["propers"][1:]
                    elif change == "foreign-form":
                        mass["forms"] = [{"id": "foreign", "propers": mass.pop("propers")}]
                    else:
                        mass["propers"].insert(0, copy.deepcopy(mass["propers"][0]))
                    states = {row["id"]: row["state"] for row in coverage.expectations(
                        EXPECTED, "postconciliar", damaged)["targets"]}
                    self.assertEqual(states[target_id(date)], "not-represented")
                    for other, (other_date, _, _) in CASES.items():
                        if other != key:
                            self.assertEqual(states[target_id(other_date)], "represented")

    def test_missing_collect_role_is_rejected_before_mass_form_classification(self):
        child = copy.deepcopy(self.targets[target_id("03-23")])
        parent = copy.deepcopy(self.targets[child["parent_id"]])
        slices = [s for s in self.inventory["slices"]
                  if s["id"] in {child["slice_id"], parent["slice_id"]}]
        child.pop("calendar_proper_name")
        lines = [f'schema = "{self.inventory["schema"]}"', "boundaries = []"]
        for section, rows in (("slices", slices), ("targets", [parent, child])):
            for row in rows:
                lines.append(f"[[{section}]]")
                lines.extend(f"{key} = {json.dumps(value, ensure_ascii=False)}"
                             for key, value in row.items())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing-role.toml"
            path.write_text("\n".join(lines) + "\n")
            for collect_present in (True, False):
                with self.subTest(collect_present=collect_present):
                    masses = copy.deepcopy(self.masses)
                    if not collect_present:
                        mass = next(m for m in masses
                                    if m["key"] == child["calendar_mass_key"])
                        mass["propers"] = [p for p in mass["propers"]
                                           if p["name"] != "Collect"]
                    with self.assertRaisesRegex(
                        ValueError, "Collect category join requires explicit"
                    ):
                        coverage.expectations(path, "postconciliar", masses)

    def test_collect_category_exception_requires_explicit_mass_form_and_collect(self):
        date = "03-23"
        child = copy.deepcopy(self.targets[target_id(date)])
        parent = copy.deepcopy(self.targets[child["parent_id"]])
        slice_row = next(s for s in self.inventory["slices"] if s["id"] == child["slice_id"])
        base = {"schema": self.inventory["schema"], "slices": [s for s in self.inventory["slices"]
                           if s["id"] in {child["slice_id"], parent["slice_id"]}],
                "targets": [parent, child], "boundaries": []}
        # Use a minimal TOML subset retaining the real parent/child relationship.
        def serial(document):
            lines = [f'schema = "{document["schema"]}"']
            for section in ("slices", "targets"):
                for row in document[section]:
                    lines.append(f"[[{section}]]")
                    for key, value in row.items():
                        lines.append(f"{key} = {json.dumps(value, ensure_ascii=False)}")
            lines.insert(1, "boundaries = []")
            return "\n".join(lines)
        mutations = (
            lambda d: d["targets"][1].pop("form_id"),
            lambda d: d["targets"][1].update(calendar_proper_name="Prayer over the Offerings"),
            lambda d: d["targets"][0].update(kind="cycle"),
            lambda d: d["targets"][0].update(calendar_mass_key="foreign"),
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(serial(base))
            self.assertEqual(coverage.expectations(path, "postconciliar", self.masses)
                             ["targets"][1]["state"], "represented")
            for mutation in mutations:
                damaged = copy.deepcopy(base)
                mutation(damaged)
                path.write_text(serial(damaged))
                with self.assertRaises(ValueError):
                    coverage.expectations(path, "postconciliar", self.masses)


if __name__ == "__main__":
    unittest.main()
