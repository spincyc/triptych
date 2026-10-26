"""Synthetic ownership controls: no source text or publication grant is added."""
import copy
import argparse
from importlib.machinery import SourceFileLoader
from pathlib import Path
from types import MappingProxyType
import os
import sys
import unittest
from unittest import mock

ROOT = Path(os.environ.get("AUDIT_REPOSITORY_ROOT", Path(__file__).resolve().parents[2])).resolve()
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
if os.environ.get("AUDIT_CALENDARS"):
    SourceFileLoader("_calendars", os.environ["AUDIT_CALENDARS"]).load_module()
if os.environ.get("AUDIT_PROPER_LATIN"):
    latin = SourceFileLoader("_proper_latin", os.environ["AUDIT_PROPER_LATIN"]).load_module()
    latin.TRUSTED_REPOSITORY = ROOT
from _proper_latin import LatinKey, STRUCTURE_SURFACES, SURFACES, sanitize_mass, text_sha256

TOOL = Path(os.environ.get("AUDIT_MASS_PROPERS", str(ROOT / "tools/mass-propers")))
P = SourceFileLoader("audit_source_identity_mass_propers", str(TOOL)).load_module()
P.ROOT = ROOT
BODY = "Synthetic public fixture body."


def source_document(rows, *, borrowed=False):
    masses = [{"key": "source", "name": "Synthetic source", "registry": "s", "propers": rows}]
    if borrowed:
        masses.append({"key": "borrower", "name": "Synthetic borrower", "registry": "b", "takes_from": {"mass": "source"}})
    return {"schema": "triptych-calendar-masses/v1", "calendar": "demo", "edition": "Synthetic", "psalm_numbering": "vulgate", "sections": {"one": {"kind": "seasonal", "masses": masses}}}


def record(body=BODY, *, permitted=True):
    return {"text_sha256": text_sha256(body), "provenance_status": "collated",
            "publication_status": "permitted" if permitted else "withheld",
            "publication_basis": "public-domain" if permitted else "restricted",
            "surfaces": sorted(SURFACES) if permitted else []}


def projected(document, records):
    with mock.patch.object(P, "load_calendar", return_value=document), \
         mock.patch.object(P, "oration_relations", return_value={}), \
         mock.patch.object(P, "translation_overlay", return_value=({}, {}, [], {})), \
         mock.patch.object(P, "publication_records", return_value=(records, [])), \
         mock.patch.object(P, "Divergences", return_value=object()):
        return P.calendar_structure(ROOT / "src/sources/calendars", "demo", {})["masses"]


def shown(document, records):
    arguments = argparse.Namespace(calendar="demo", mass="source", lang="la",
                                   root=str(ROOT / "src/sources/calendars"),
                                   bible=None, bible_root=str(ROOT / "src/sources/bibles"))
    with mock.patch.object(P, "load_calendar", return_value=document), \
         mock.patch.object(P, "translation_overlay", return_value=({}, {}, [], {})), \
         mock.patch.object(P, "publication_records", return_value=(records, [])):
        return P.run_show_one(arguments)


class SourceLatinIdentityTests(unittest.TestCase):
    def repeated(self):
        return [{"name": "Oratio", "source": "composed", "text": BODY},
                {"name": "Oratio", "source": "composed", "text": BODY}]

    def keys(self):
        return [LatinKey("source", "", "Oratio", occurrence=n) for n in (1, 2)]

    def cycle_rows(self, course, cycle):
        return [{"name": "Oratio", "source": "composed",
                 course: {cycle: {"source": "composed", "text": BODY}}}
                for _ in range(2)]

    def cycle_keys(self, course, cycle, form=""):
        return [LatinKey("source", form, "Oratio", course, cycle, n) for n in (1, 2)]

    def assert_cycle_cli_views(self, document, records, course, cycle, expected):
        built = shown(document, records)
        raw_rows = built["mass"].get("propers") or [
            p for form in built["mass"].get("forms") or [] for p in form["propers"]]
        self.assertEqual(expected, [p[course][cycle].get("text") for p in raw_rows])
        self.assertEqual(expected, [p["proper"][course][cycle].get("text") for p in built["appointed"]])

    def test_identical_words_keep_each_source_permission(self):
        rows = self.repeated()
        first, second = self.keys()
        records = {first: record(), second: record(permitted=False)}
        # The existing source-mass sanitizer is an independent exact-ordinal
        # control. Resolved public structures must reach the same decisions.
        raw = sanitize_mass(source_document(rows)["sections"]["one"]["masses"][0], records, STRUCTURE_SURFACES)
        self.assertEqual([BODY, None], [p.get("text") for p in raw["propers"]])
        built = projected(source_document(rows), records)
        self.assertEqual([BODY, None], [p.get("text") for p in built[0]["propers"]])

    def test_missing_owner_cannot_borrow_same_words_permission(self):
        _, second = self.keys()
        built = projected(source_document(self.repeated()), {second: record()})
        self.assertEqual([None, BODY], [p.get("text") for p in built[0]["propers"]])

    def test_stale_owner_cannot_borrow_same_words_permission(self):
        first, second = self.keys()
        built = projected(source_document(self.repeated()), {first: record("Different synthetic body."), second: record()})
        self.assertEqual([None, BODY], [p.get("text") for p in built[0]["propers"]])

    def test_scripture_occurrence_does_not_shift_latin_body_ordinal(self):
        rows = self.repeated()
        rows.insert(1, {"name": "Oratio", "source": "scripture", "verses": []})
        first, second = self.keys()
        built = projected(source_document(rows), {first: record(), second: record(permitted=False)})
        self.assertEqual([BODY, None, None], [p.get("text") for p in built[0]["propers"]])

    def test_whole_mass_borrow_keeps_source_permissions(self):
        first, second = self.keys()
        built = projected(source_document(self.repeated(), borrowed=True), {first: record(), second: record(permitted=False)})
        borrower = next(m for m in built if m["key"] == "borrower")
        self.assertEqual([BODY, None], [p.get("text") for p in borrower["propers"]])

    def test_cli_appointed_and_raw_copies_keep_same_source_permissions(self):
        first, second = self.keys()
        built = shown(source_document(self.repeated()), {first: record(), second: record(permitted=False)})
        self.assertEqual([BODY, None], [p["proper"].get("text") for p in built["appointed"]])
        self.assertEqual([BODY, None], [p.get("text") for p in built["mass"]["propers"]])

    def test_cli_missing_owner_cannot_borrow_same_words_permission(self):
        _, second = self.keys()
        built = shown(source_document(self.repeated()), {second: record()})
        self.assertEqual([None, BODY], [p["proper"].get("text") for p in built["appointed"]])

    def test_cli_still_requires_its_own_surface(self):
        first, _ = self.keys()
        web_only = record()
        web_only["surfaces"] = sorted(STRUCTURE_SURFACES)
        built = shown(source_document(self.repeated()[:1]), {first: web_only})
        self.assertIsNone(built["appointed"][0]["proper"]["text"])

    def test_qualified_wrapper_keeps_source_name_and_permission(self):
        first, second = self.keys()
        doc = source_document(self.repeated())
        doc["sections"]["one"]["masses"].append({
            "key": "borrower", "name": "Synthetic named borrower", "registry": "b",
            "propers": [{"name": "Oratio (borrowed)", "takes_from": {"mass": "source", "proper": "Oratio"}}],
        })
        built = projected(doc, {first: record(), second: record(permitted=False)})
        borrower = next(m for m in built if m["key"] == "borrower")
        self.assertEqual("Oratio (borrowed)", borrower["propers"][0]["name"])
        self.assertEqual("Oratio", borrower["propers"][0]["taken_from"]["proper"])
        self.assertEqual(BODY, borrower["propers"][0]["text"])

    def test_cycle_repetitions_keep_source_permissions(self):
        rows = [{"name": "Oratio", "source": "composed", "cycles": {"A": {"source": "composed", "text": BODY}}} for _ in range(2)]
        records = {LatinKey("source", "", "Oratio", "cycles", "A", n): record(permitted=n == 1) for n in (1, 2)}
        built = projected(source_document(rows), records)
        self.assertEqual([BODY, None], [p["cycles"]["A"].get("text") for p in built[0]["propers"]])

    def test_raw_and_appointed_cycles_keep_each_owner_permission(self):
        for course, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            with self.subTest(course=course):
                first, second = self.cycle_keys(course, cycle)
                self.assert_cycle_cli_views(source_document(self.cycle_rows(course, cycle)),
                                            {first: record(), second: record(permitted=False)},
                                            course, cycle, [BODY, None])

    def test_raw_cycle_sanitizer_keeps_mapping_input_contract(self):
        first, second = self.cycle_keys("cycles", "A")
        mass = source_document(self.cycle_rows("cycles", "A"))["sections"]["one"]["masses"][0]
        result = sanitize_mass(MappingProxyType(mass), {first: record(), second: record(permitted=False)}, STRUCTURE_SURFACES)
        self.assertEqual([BODY, None], [p["cycles"]["A"].get("text") for p in result["propers"]])

    def test_raw_and_appointed_cycles_refuse_missing_owner(self):
        for course, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            with self.subTest(course=course):
                _, second = self.cycle_keys(course, cycle)
                self.assert_cycle_cli_views(source_document(self.cycle_rows(course, cycle)),
                                            {second: record()}, course, cycle, [None, BODY])

    def test_raw_and_appointed_cycles_refuse_stale_owner(self):
        for course, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            with self.subTest(course=course):
                first, second = self.cycle_keys(course, cycle)
                self.assert_cycle_cli_views(source_document(self.cycle_rows(course, cycle)),
                                            {first: record("Other synthetic body."), second: record()},
                                            course, cycle, [None, BODY])

    def test_raw_and_appointed_cycle_surfaces_do_not_cross(self):
        for course, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            with self.subTest(course=course):
                first, second = self.cycle_keys(course, cycle)
                web, cli = record(), record()
                web["surfaces"], cli["surfaces"] = sorted(STRUCTURE_SURFACES), ["cli"]
                records = {first: web, second: cli}
                document = source_document(self.cycle_rows(course, cycle))
                self.assert_cycle_cli_views(document, records, course, cycle, [None, BODY])
                self.assertEqual([BODY, None], [p[course][cycle].get("text")
                                               for p in projected(document, records)[0]["propers"]])

    def test_named_form_cycles_keep_raw_and_appointed_owner_boundaries(self):
        for defect in (None, "missing", "stale", "surface"):
            with self.subTest(defect=defect):
                document = source_document([])
                mass = document["sections"]["one"]["masses"][0]
                mass.pop("propers")
                mass["forms"] = [{"id": "first", "name": "First form", "propers": self.cycle_rows("cycles", "A")},
                                 {"id": "second", "name": "Second form", "propers": self.cycle_rows("cycles", "A")}]
                a, b = self.cycle_keys("cycles", "A", "First form")
                c, d = self.cycle_keys("cycles", "A", "Second form")
                records = {a: record(), b: record(permitted=False), c: record(permitted=False), d: record()}
                expected = [BODY, None, None, BODY]
                if defect:
                    records[b] = record()
                    expected = [None, BODY, None, BODY]
                    if defect == "missing": records.pop(a)
                    elif defect == "stale": records[a] = record("Other synthetic body.")
                    else: records[a]["surfaces"] = sorted(STRUCTURE_SURFACES)
                self.assert_cycle_cli_views(document, records, "cycles", "A", expected)

    def test_cycle_scripture_owner_does_not_shift_latin_ordinal(self):
        rows = self.cycle_rows("cycles", "A")
        rows.insert(1, {"name": "Oratio", "cycles": {"A": {"source": "scripture", "verses": []}}})
        first, second = self.cycle_keys("cycles", "A")
        self.assert_cycle_cli_views(source_document(rows), {first: record(), second: record(permitted=False)},
                                    "cycles", "A", [BODY, None, None])

    def test_cycle_quarantine_keeps_the_canonical_body_ordinal(self):
        for held in (True, False):
            with self.subTest(held_unpublished=held):
                status = {"state": "unavailable", "scope": "proper-body",
                          "reasons": [{"kind": "rights-withheld", "source_id": "artifact.synthetic.restricted"}]}
                if held: status["body_status"] = "held-unpublished"
                rows = [{"name": "Oratio", "cycles": {"A": {"source": "composed", "text_status": status}}},
                        self.cycle_rows("cycles", "A")[0]]
                first, second = self.cycle_keys("cycles", "A")
                records = {first: record()} if held else {
                    first: {**record("Former private synthetic body.", permitted=False), "body_status": "removed"},
                    second: record(),
                }
                self.assert_cycle_cli_views(source_document(rows), records, "cycles", "A", [None, BODY])

    def test_named_forms_keep_separate_latin_occurrences(self):
        doc = source_document([])
        mass = doc["sections"]["one"]["masses"][0]
        mass.pop("propers")
        mass["forms"] = [{"id": "first", "name": "First form", "propers": self.repeated()},
                         {"id": "second", "name": "Second form", "propers": self.repeated()}]
        records = {LatinKey("source", label, "Oratio", occurrence=n): record(permitted=(label == "First form") == (n == 1))
                   for label in ("First form", "Second form") for n in (1, 2)}
        built = projected(doc, records)
        self.assertEqual([BODY, None, None, BODY], [p.get("text") for p in built[0]["propers"]])

    def test_never_published_owner_does_not_shift_latin_ordinal(self):
        status = {"state": "unavailable", "scope": "proper-body", "body_status": "held-unpublished",
                  "reasons": [{"kind": "rights-withheld", "source_id": "artifact.synthetic.restricted"}]}
        rows = [{"name": "Oratio", "source": "composed", "text_status": status}, self.repeated()[0]]
        first, _ = self.keys()
        built = projected(source_document(rows), {first: record()})
        self.assertEqual([None, BODY], [p.get("text") for p in built[0]["propers"]])
        self.assertTrue(built[0]["propers"][0]["latin"]["withheld"])

    def test_removed_owner_keeps_latin_ordinal(self):
        status = {"state": "unavailable", "scope": "proper-body",
                  "reasons": [{"kind": "rights-withheld", "source_id": "artifact.synthetic.restricted"}]}
        rows = [{"name": "Oratio", "source": "composed", "text_status": status}, self.repeated()[0]]
        first, second = self.keys()
        removed = {**record("Former synthetic private body.", permitted=False), "body_status": "removed"}
        built = projected(source_document(rows), {first: removed, second: record()})
        self.assertEqual([None, BODY], [p.get("text") for p in built[0]["propers"]])

    def test_missing_and_withheld_records_remain_absent(self):
        rows = [{"name": "Oratio", "source": "composed", "text": BODY}]
        first, _ = self.keys()
        for records in ({}, {first: record(permitted=False)}):
            with self.subTest(records=bool(records)):
                self.assertIsNone(projected(source_document(rows), records)[0]["propers"][0]["text"])

    def test_input_document_and_source_records_are_not_mutated(self):
        doc = source_document(self.repeated())
        first, second = self.keys()
        records = {first: record(), second: record(permitted=False)}
        before = copy.deepcopy((doc, records))
        projected(doc, records)
        self.assertEqual(before, (doc, records))


if __name__ == "__main__":
    unittest.main()
