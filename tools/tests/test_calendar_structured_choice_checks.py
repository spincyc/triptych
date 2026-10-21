"""Source menus retain printed order while every candidate remains checked."""
from __future__ import annotations

import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get("TRIPTYCH_APPOINTMENT_MODULE_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars as C


def checker(root, name):
    loader = SourceFileLoader(name, str(root / "tools/check-calendar-masses"))
    spec = spec_from_loader(loader.name, loader)
    result = module_from_spec(spec)
    sys.modules[spec.name] = result
    loader.exec_module(result)
    return result


CHECK = checker(MODULE_ROOT, "_structured_choice_checker")
SOURCE_CHECK = checker(ROOT, "_structured_choice_source_ordinals")
ORDER = SOURCE_CHECK.slot_ordinals("roman-1962")
SOURCE_FILE = ROOT / "src/sources/calendars/roman-1962/propers.yaml"
SOURCE = C.load_document(SOURCE_FILE.parent.parent, "roman-1962", effective=False)
UNAVAILABLE = (
    "s-gregorii-barbadici-episcopi-confessoris",
    "s-laurentii-brundusio-confessoris-ecclesiae-doctoris",
    "s-antonii-mariae-claret-episcopi-confessoris",
)
MENUS = (
    "commune-unius-martyris-1", "commune-unius-martyris-2",
    "commune-unius-martyris-3", "commune-unius-martyris-4",
    "commune-plurimorum-martyrum-1", "commune-plurimorum-martyrum-2",
    "commune-plurimorum-martyrum-3", "commune-martyrum-tempore-paschali-1",
    "commune-martyrum-tempore-paschali-2", "commune-virginum-2",
)


def common_rows(document, saint):
    index = C.mass_index(document)
    return [("sanctoral", saint),
            (CHECK.COMMON_KIND, index[saint["takes_from"]["mass"]])]


def late_group(mass):
    # The last source row is the separately printed alternate reading.
    group = mass["propers"][-1]["ordinary_disposition"]["group"]
    return [p for p in mass["propers"]
            if p.get("ordinary_disposition", {}).get("group") == group]


def order_problems(document, keys):
    # Keep the entire actual header and source index for fact validation.
    # Scope only the order walk, and its existing exception ledger, to these
    # named controls. No source candidates are filtered by applicability.
    selected = [(kind, mass) for kind, mass in SOURCE_CHECK.iter_masses(document)
                if mass["key"] in keys]
    fixture = {**document, CHECK.ORDER_EXCEPTIONS: [r for r in document.get(CHECK.ORDER_EXCEPTIONS, [])
                                                if r["mass"] in keys]}
    with patch.object(CHECK, "read_yaml", return_value=fixture), \
         patch.object(CHECK, "iter_masses", return_value=selected), \
         patch.object(CHECK, "slot_ordinals", return_value=ORDER):
        return CHECK.order_problems([SOURCE_FILE])


class StructuredChoiceSourceChecks(unittest.TestCase):
    def test_three_actual_unavailable_collect_joins_keep_the_source_header(self):
        index = C.mass_index(SOURCE)
        for key in UNAVAILABLE:
            with self.subTest(mass=key):
                saint = index[key]
                self.assertEqual([], CHECK.common_reference_problems(common_rows(SOURCE, saint), document=SOURCE))

    def test_unavailable_collect_does_not_erase_a_missing_or_invalid_fact(self):
        for change in ("missing", "wrong-edition"):
            document = copy.deepcopy(SOURCE)
            if change == "missing":
                del document[C.PROPER_APPOINTMENT_FACTS]
            else:
                for fact in document[C.PROPER_APPOINTMENT_FACTS].values():
                    fact["edition"] = "another-edition"
            saint = C.mass_index(document)[UNAVAILABLE[0]]
            with self.subTest(change=change):
                problems = CHECK.common_reference_problems(common_rows(document, saint), document=document)
                wanted = "unknown fact or enum value" if change == "missing" else "different edition"
                self.assertTrue(any(wanted in p for p in problems), problems)

    def test_ten_actual_late_menus_keep_their_source_names_and_order(self):
        snapshot = copy.deepcopy(SOURCE)
        for key in MENUS:
            with self.subTest(mass=key):
                self.assertEqual([], order_problems(SOURCE, {key}))
        self.assertEqual(snapshot, SOURCE)

    def test_a_misplaced_exact_anchor_is_still_wrong_order(self):
        document = copy.deepcopy(SOURCE)
        mass = C.mass_index(document)[MENUS[0]]
        members = late_group(mass)
        anchor_name = members[0]["ordinary_disposition"]["anchor"]["proper"]
        principal = next(p for p in members if p["name"] == anchor_name)
        mass["propers"].remove(principal)
        position = next(i for i, p in enumerate(mass["propers"]) if p["name"] == "Offertory")
        mass["propers"].insert(position + 1, principal)
        self.assertTrue(any("order the edition prints" in p for p in order_problems(document, {mass["key"]})))

    def test_an_ordinary_unannotated_order_error_remains_refused(self):
        document = copy.deepcopy(SOURCE)
        mass = C.mass_index(document)[MENUS[0]]
        secret = next(p for p in mass["propers"] if p["name"] == "Secret")
        mass["propers"].remove(secret)
        mass["propers"].insert(1, secret)
        self.assertTrue(any("order the edition prints" in p for p in order_problems(document, {mass["key"]})))

    def test_invalid_anchor_seat_basis_and_unknown_candidate_stay_errors(self):
        for mutation in ("anchor", "seat", "basis", "unknown-name", "cross-rank"):
            document = copy.deepcopy(SOURCE)
            mass = C.mass_index(document)[MENUS[2]]
            members = late_group(mass)
            if mutation == "anchor":
                for member in members:
                    member["ordinary_disposition"]["anchor"]["occurrence"] = 2
            elif mutation == "seat":
                del members[-1]["ordinary_disposition"]["seat"]
            elif mutation == "basis":
                members[-1]["ordinary_disposition"]["basis"] = "Conflicting technical source basis."
            else:
                members[-1]["name"] = "Unknown reading" if mutation == "unknown-name" else "Gospel (forged first reading)"
            with self.subTest(mutation=mutation):
                problems = order_problems(document, {mass["key"]})
                wanted = {"anchor": "anchor must be one exact member",
                          "seat": "identical seat presence and value",
                          "basis": "identical basis"}.get(mutation, "one edition-attested Proper order rank")
                self.assertTrue(any(wanted in p for p in problems), problems)

    def test_predicate_candidates_are_checked_without_selecting_an_option(self):
        for applicability in ("known-paschal", "known-tract", "unknown-fact", "unknown-enum"):
            document = copy.deepcopy(SOURCE)
            mass = C.mass_index(document)[MENUS[2]]
            members = late_group(mass)
            for member in members:
                member["ordinary_disposition"]["when"] = {"fact": "roman-1962-common-chant-regime", "in": ["paschal"]}
            if applicability == "known-tract":
                members[-1]["ordinary_disposition"]["when"]["in"] = ["tract"]
            elif applicability == "unknown-fact":
                members[-1]["ordinary_disposition"]["when"]["fact"] = "unheld-fact"
            elif applicability == "unknown-enum":
                members[-1]["ordinary_disposition"]["when"]["in"] = ["unheld-value"]
            if applicability.startswith("known-"):
                # Even an option unavailable in another season cannot carry
                # a Gospel into this source-qualified first-reading menu.
                members[-1]["name"] = "Gospel (forged first reading)"
            with self.subTest(applicability=applicability):
                problems = order_problems(document, {mass["key"]})
                wanted = "one edition-attested Proper order rank" if applicability.startswith("known-") else "unknown fact or enum value"
                self.assertTrue(any(wanted in p for p in problems), problems)


if __name__ == "__main__":
    unittest.main()
