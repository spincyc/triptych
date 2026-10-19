"""Shared Missal accounting: identities, uses, witnesses, and evidence axes."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _missal_coverage as coverage


def tool(name):
    loader = importlib.machinery.SourceFileLoader("coverage_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def english(report):
    return next(row for row in report["languages"] if row["lang"] == "en")


class CoverageTests(unittest.TestCase):
    def test_duplicate_witness_and_alias_do_not_inflate_targets_or_available_uses(self):
        witness = {"source_id": "edition.one", "artifact_id": "artifact.one", "label": "Witness"}
        owner = {"source": "composed", "translations": [
            {"lang": "en", "source_id": identifier, "rights": "public-domain", "text": "Body"}
            for identifier in ("edition.one", "artifact.one", "edition.one")
        ]}
        one = coverage.unit(owner, target_id="target", occurrence_id="one",
                            witnesses={"edition.one": witness, "artifact.one": witness})
        two = copy.deepcopy(one)
        two["occurrence_id"] = "two"
        report = coverage.summarize([one, two, one], "calendar")
        self.assertEqual(report["counts"], {"canonical_targets": 1, "occurrences": 2, "witness_alternatives": 1})
        self.assertEqual(english(report)["available"], 2)
        self.assertEqual(english(report)["available_targets"], 1)
        self.assertEqual(english(report)["witnesses"][0]["aliases"], ["artifact.one", "edition.one"])
        self.assertEqual(english(one)["publication_basis"], "public-domain")
        self.assertEqual(english(report)["witnesses"][0]["publication_bases"], ["public-domain"])
        self.assertNotIn('"rights":', json.dumps([one, report]))
        coverage.validate_summary(report)

    def test_private_metadata_alias_is_not_added_to_public_witnesses(self):
        one = coverage.unit({"translations": [{
            "lang": "en", "source_id": "edition.public", "text": "Held",
            "rights": "public-domain",
        }]}, target_id="target", occurrence_id="use", witnesses={
            "edition.public": {"source_id": "edition.public",
                               "artifact_id": "artifact.private"},
        })
        self.assertEqual(english(one)["witnesses"][0]["aliases"], ["edition.public"])
        self.assertNotIn("artifact.private", json.dumps(coverage.summarize([one], "mass")))

    def test_fidelity_rights_and_availability_remain_independent(self):
        rows = []
        for index, (relation, collation, rights) in enumerate((
            ("antecedent", "collated", "public-domain"),
            ("antecedent", "uncollated", "public-domain"),
            (None, None, "project-created"),
            (None, None, "public-domain"),
        )):
            rows.append(coverage.unit({"translations": [{
                "lang": "en", "text": "Held", "source_id": str(index),
                "relation": relation, "collation": collation, "rights": rights,
            }]}, target_id=str(index), occurrence_id=str(index)))
        report = coverage.summarize(rows, "ordinary")
        row = english(report)
        self.assertEqual(row["available"], 4)
        self.assertEqual(row["exact_target"], 0)
        self.assertEqual(row["relationships"]["historical-antecedent"], 2)
        self.assertEqual(row["relationships"]["study-translation"], 1)
        self.assertEqual(row["relationships"]["unresolved"], 1)
        self.assertEqual(row["collations"]["collated"], 1)
        coverage.validate_summary(report)

    def test_conflicting_alias_bodies_fail_instead_of_claiming_availability(self):
        witness = {"source_id": "edition.one", "artifact_id": "artifact.one"}
        with self.assertRaisesRegex(ValueError, "conflicting bodies"):
            coverage.unit({"translations": [
                {"lang": "en", "source_id": "edition.one", "text": "One"},
                {"lang": "en", "source_id": "artifact.one", "text": "Different"},
            ]}, target_id="target", occurrence_id="one",
                witnesses={"edition.one": witness, "artifact.one": witness})

    def test_bible_reconstruction_does_not_fill_composed_wording(self):
        one = coverage.unit({"source": "scripture", "citations": [{"ref": "Psalm 1"}]},
                            target_id="scripture", occurrence_id="scripture")
        report = coverage.summarize([one], "mass")
        self.assertEqual(english(report)["targets"], 0)
        self.assertEqual(english(report)["scripture_targets"], 1)
        self.assertEqual(english(report)["available"], 0)
        self.assertEqual(one["languages"][0]["relationship"], "bible-reconstruction")
        coverage.validate_summary(report)

    def test_exact_witness_is_counted_once_beside_an_antecedent_alternative(self):
        one = coverage.unit({"translations": [
            {"lang": "en", "text": "Exact", "source_id": "a", "relation": "own", "rights": "public-domain"},
            {"lang": "en", "text": "Earlier", "source_id": "b", "relation": "antecedent", "rights": "public-domain"},
        ]}, target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        self.assertEqual(english(report)["exact_target"], 1)
        self.assertEqual(english(report)["exact_target_targets"], 1)
        self.assertEqual(english(report)["relationships"]["unresolved"], 1)
        self.assertEqual(report["counts"]["witness_alternatives"], 2)

    def test_mixed_body_keeps_its_independent_bible_component(self):
        one = coverage.unit({"source": "mixed", "text": "Latin",
                             "citations": [{"ref": "Psalm 1"}]},
                            target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        self.assertEqual(report["counts"]["canonical_targets"], 1)
        self.assertEqual(report["counts"]["occurrences"], 1)
        self.assertEqual(english(report)["occurrences"], 1)
        self.assertEqual(english(report)["scripture_occurrences"], 1)
        self.assertEqual(english(report)["mixed_occurrences"], 1)
        self.assertNotEqual(one["scripture_component"]["target_id"], one["target_id"])
        coverage.validate_summary(report)

    def test_absence_dispositions_do_not_export_source_evidence(self):
        one = coverage.unit({
            "untranslated": [{"lang": "en", "state": "rights-restricted",
                               "artifact_sha256": "SECRET", "witness_artifact_id": "PRIVATE"}],
            "latin": {"state": "unavailable", "withheld": True, "private": "SECRET"},
        }, target_id="target", occurrence_id="one")
        self.assertEqual(english(one)["availability"], "not-publishable")
        self.assertEqual(english(one)["publication_basis"], "restricted")
        self.assertEqual(one["languages"][0]["availability"], "unresolved")
        self.assertNotIn("SECRET", json.dumps(one))
        self.assertNotIn("PRIVATE", json.dumps(one))
        other = coverage.unit({}, target_id="other", occurrence_id="other",
                              ordinary_absences={"la": "inapplicable", "en": "absent-in-witness"})
        self.assertEqual(other["languages"][0]["availability"], "inapplicable")
        self.assertEqual(english(other)["availability"], "absent-in-witness")

    def test_report_refuses_conflicting_occurrences_and_bad_partition(self):
        one = coverage.unit({}, target_id="target", occurrence_id="one")
        other = copy.deepcopy(one)
        other["target_id"] = "another"
        with self.assertRaisesRegex(ValueError, "conflicting"):
            coverage.summarize([one, other], "mass")
        report = coverage.summarize([one], "mass")
        english(report)["available"] = 1
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            coverage.validate_summary(report)

    def test_summary_validation_checks_witness_counts(self):
        one = coverage.unit({"translations": [{"lang": "en", "text": "Held",
                                               "source_id": "a", "rights": "public-domain"}]},
                            target_id="target", occurrence_id="one")
        report = coverage.summarize([one], "mass")
        report["counts"]["witness_alternatives"] = 999
        with self.assertRaisesRegex(ValueError, "witness alternatives"):
            coverage.validate_summary(report)
        report = coverage.summarize([one], "mass")
        english(report)["witnesses"][0]["available"] = 999
        with self.assertRaisesRegex(ValueError, "exceeds"):
            coverage.validate_summary(report)


class GeneratorCoverageTests(unittest.TestCase):
    def test_translation_only_sunday_and_weekday_owners_survive_generation(self):
        propers = tool("mass-propers")
        for family, cycle in (("cycles", "A"), ("weekday_cycles", "I")):
            for rights in ("public-domain", "licensed"):
                source = {"name": "Acclamation", "source": "composed", family: {
                    cycle: {"source": "composed", "translations": [{
                        "lang": "en", "text": "Public fixture", "source_id": "edition.a",
                        "rights": rights,
                    }]}
                }}
                document = {"psalm_numbering": "vulgate", "sections": {
                    "temporal": {"kind": "seasonal", "masses": [{"key": "owner", "propers": [source]}]}
                }}
                with self.subTest(family=family, rights=rights), \
                     mock.patch.object(propers, "load_calendar", return_value=document), \
                     mock.patch.object(propers, "translation_overlay", return_value=({}, {}, [], {})), \
                     mock.patch.object(propers, "publication_records", return_value=({}, [])), \
                     mock.patch.object(propers, "sanitize_proper", side_effect=lambda value, *args: value), \
                     mock.patch.object(propers._missal_coverage, "expectations", return_value={"state": "unresolved"}):
                    report = propers.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", {})
                child = report["masses"][0]["propers"][0][family][cycle]
                self.assertEqual(english(child["coverage"])["availability"],
                                 "available" if rights == "public-domain" else "not-publishable")
                self.assertEqual(report["coverage"]["counts"]["occurrences"], 1)
                self.assertEqual(english(report["coverage"])["available"],
                                 1 if rights == "public-domain" else 0)

    def test_generator_visits_nested_cycles_and_reuses_canonical_owner(self):
        propers = tool("mass-propers")
        source = {"name": "Acclamation", "cycles": {
            "A": {"source": "composed", "text": "Latin"},
            "B": {"source": "scripture", "verses": []},
        }}
        owner = {"key": "owner", "name": "Owner", "propers": [source]}
        borrowed = {"key": "borrowed", "name": "Borrowed", "takes_from": {"mass": "owner"}}
        document = {"calendar": "postconciliar", "psalm_numbering": "vulgate",
                    "sections": {"temporal": {"kind": "seasonal", "masses": [owner, borrowed]}}}
        # A citation is enough to make the scripture cycle a generated owner.
        source["cycles"]["B"]["verses"] = [{"book": "Psalms", "ranges": [], "ref": "Psalm 1"}]
        with mock.patch.object(propers, "load_calendar", return_value=document), \
             mock.patch.object(propers, "translation_overlay", return_value=({}, {}, [], {})), \
             mock.patch.object(propers, "publication_records", return_value=({}, [])), \
             mock.patch.object(propers, "sanitize_proper", side_effect=lambda value, *args: value), \
             mock.patch.object(propers, "citation_structure", return_value={"ref": "Psalm 1"}), \
             mock.patch.object(propers._missal_coverage, "expectations", return_value={"state": "unresolved"}):
            report = propers.calendar_structure(ROOT / "src/sources/calendars", "postconciliar", {})
        self.assertEqual(report["coverage"]["counts"]["canonical_targets"], 2)
        self.assertEqual(report["coverage"]["counts"]["occurrences"], 4)
        self.assertEqual(english(report["coverage"])["occurrences"], 2)
        self.assertEqual(english(report["coverage"])["scripture_occurrences"], 2)
        self.assertIsNone(report["masses"][0]["propers"][0]["coverage"])
        left, right = [coverage.proper_units(mass) for mass in report["masses"]]
        self.assertEqual(left[0]["target_id"], right[0]["target_id"])
        self.assertNotEqual(left[0]["occurrence_id"], right[0]["occurrence_id"])
        coverage.validate_summary(report["coverage"])


class RealCorpusCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.propers = tool("mass-propers")
        cls.files = {
            calendar: cls.propers.calendar_structure(
                ROOT / "src/sources/calendars", calendar, cls.propers.book_tokens()
            ) for calendar in ("roman-1962", "postconciliar", "roman-pre-1955")
        }

    def test_published_english_targets_agree_with_source_identity_census(self):
        for calendar, document in self.files.items():
            source = self.propers.english_coverage(ROOT / "src/sources/calendars", calendar)
            self.assertEqual(english(document["coverage"])["targets"], source["slots"], calendar)
            self.assertEqual(english(document["coverage"])["available_targets"], source["with_english"], calendar)
            coverage.validate_summary(document["coverage"])

    def test_pre1955_inheritance_is_not_promoted_to_target_wording(self):
        document = self.files["roman-pre-1955"]
        self.assertGreater(english(document["coverage"])["available"], 0)
        self.assertTrue(any(mass.get("recension") for mass in document["masses"]))
        self.assertTrue(all(row["exact_target"] == 0 for row in document["coverage"]["languages"]))

    def test_pentecost_19_keeps_all_seven_scripture_bearing_propers(self):
        mass = next(row for row in self.files["roman-1962"]["masses"] if row["key"] == "pentecost-19")
        report = english(mass["coverage"])
        self.assertEqual(sum(bool(row["citations"]) for row in mass["propers"]), 7)
        self.assertEqual(report["scripture_occurrences"], 7)
        self.assertEqual(report["mixed_occurrences"], 1)
        self.assertEqual(report["occurrences"], 4)


class ExpectedInventoryTests(unittest.TestCase):
    def inventory(self):
        return '''schema = "triptych-missal-expected-targets/v1"
as_of = "2026-10-19"
[[slices]]
id = "fixed"
calendar = "roman-1962"
recension_id = "roman-1962"
territory = "universal"
languages = ["la", "en"]
date_range = "edition snapshot"
source_refs = ["source.toml"]
enumeration_state = "complete-within-slice"
basis = "Independent calendar identities only"
[[targets]]
id = "feast"
slice_id = "fixed"
kind = "celebration"
calendar_mass_key = "feast"
identity_state = "established"
[[boundaries]]
id = "unclosed"
slice_id = "fixed"
kind = "text-slots"
state = "unenumerated"
'''

    def test_heterogeneous_inventory_does_not_become_text_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory())
            report = coverage.expectations(path, "roman-1962", [{"key": "feast"}])
        self.assertEqual(report["targets"][0]["state"], "represented")
        self.assertEqual(report["slices"][0]["kinds"], [{"kind": "celebration", "states": {"represented": 1}}])
        self.assertEqual(report["boundaries"][0]["state"], "unenumerated")
        self.assertNotIn("expected_text_slots", report)
        self.assertEqual(report["slices"][0]["source_refs"], ["source.toml"])

    def test_invalid_inventory_rows_fail_closed(self):
        mutations = (
            self.inventory().replace('slice_id = "fixed"', 'slice_id = "unknown"'),
            self.inventory().replace('kind = "celebration"', 'kind = "typo"'),
            self.inventory().replace('calendar_mass_key = "feast"', 'calendar_mass_key = 42'),
            self.inventory() + '\n[[targets]]\nid="feast"\nslice_id="fixed"\nkind="common"\nidentity_state="established"\n',
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            for value in mutations:
                path.write_text(value)
                with self.subTest(value=value), self.assertRaises(ValueError):
                    coverage.expectations(path, "roman-1962", [])

    def test_form_cycle_mapping_stays_inside_its_form_and_accepts_implicit_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "inventory.toml"
            path.write_text(self.inventory().replace('kind = "celebration"', 'kind = "form"\nform_id = "main"'))
            main = {"key": "feast", "propers": [{"form_id": "main"}]}
            self.assertEqual(coverage.expectations(path, "roman-1962", [main])["targets"][0]["state"], "represented")
            path.write_text(self.inventory().replace('kind = "celebration"',
                                                     'kind = "cycle"\nform_id = "vigil"\ncycle = "A"\ncycle_family = "sunday"'))
            mass = {"key": "feast", "forms": [{"id": "vigil"}, {"id": "day"}], "propers": [
                {"form_id": "day", "cycles": {"A": {"coverage": coverage.unit({}, target_id="t", occurrence_id="o", cycle="A", cycle_family="cycles")}}},
            ]}
            self.assertEqual(coverage.expectations(path, "roman-1962", [mass])["targets"][0]["state"], "not-represented")

    def test_source_calendar_keeps_missing_christmas_commemoration_visible(self):
        propers = tool("mass-propers")
        document = propers.load_calendar(ROOT / "src/sources/calendars", "roman-1962")
        report = coverage.expectations(
            ROOT / "src/sources/inventories/missal-expected-targets-v1.toml",
            "roman-1962", [mass for _, mass in propers.masses_of(document)],
        )
        fixed = [row for row in report["targets"]
                 if row["slice_id"] == "roman-1962-universal-fixed-calendar"]
        self.assertEqual(len(fixed), 336)
        self.assertEqual(sum(row["state"] == "represented" for row in fixed), 335)
        missing = [row for row in fixed if row["state"] == "not-represented"]
        self.assertEqual([row["id"] for row in missing],
                         ["roman-1962:commemoration:1962-12-25-comm"])


if __name__ == "__main__":
    unittest.main()
