#!/usr/bin/env python3
"""Ordinary element coverage and source offers use independent partitions."""
from __future__ import annotations

import copy
import unittest

if __package__:
    from .test_complete_missal_report import REPORT, fixture_reports
else:
    from test_complete_missal_report import REPORT, fixture_reports
from _missal_coverage import summarize, unit, validate_summary


def ordinary_fixture(*, multiple: bool, own: bool = False) -> tuple[dict, dict, dict]:
    reports = fixture_reports()
    for row in reports[2]["coverage"]:
        units = []
        for index in range(3):
            translations = []
            sources = [("en", "edition.english-a")] if index < 2 else []
            if index == 0:
                sources.append(("la", "edition.latin"))
                if multiple:
                    sources.append(("en", "edition.english-b"))
            for lang, source in sources:
                translations.append({
                    "lang": lang, "source_id": source, "text": "Synthetic body",
                    "relation": "own" if own else "antecedent",
                    "collation": "not-applicable" if own else "uncollated",
                    "rights": "public-domain",
                })
            identity = f"{row['calendar']}:ordinary:{index}"
            units.append(unit(
                {"translations": translations}, target_id=identity,
                occurrence_id=identity, component="ordinary-body",
            ))
        row["typed_coverage"] = summarize(units, "ordinary")
        row["witnesses"] = [
            {"lang": lang, "source_id": witness["id"], "held": witness["available"]}
            for language in row["typed_coverage"]["languages"]
            for lang in [language["lang"]]
            for witness in language["witnesses"]
        ]
        row["relation_coverage"] = [
            {"lang": "en", "relation": "own" if own else "antecedent",
             "collation": "not-applicable" if own else "uncollated",
             "count": 3 if multiple else 2},
            {"lang": "la", "relation": "own" if own else "antecedent",
             "collation": "not-applicable" if own else "uncollated",
             "count": 1},
        ]
    return reports


def english(row: dict) -> dict:
    return next(item for item in row["language_coverage"] if item["lang"] == "en")


class CompleteMissalSourceOffersTests(unittest.TestCase):
    def test_two_witnesses_of_one_element_do_not_inflate_modeled_or_held(self):
        reports = ordinary_fixture(multiple=True)
        original = copy.deepcopy(reports)
        report = REPORT.build_report(*reports)
        for family in report["families"]:
            slots = family["textual"]
            filled = slots["filled_text_slots"]
            language = next(row for row in filled["ordinary_language_coverage"]
                            if row["lang"] == "en")
            self.assertEqual((language["elements"], language["held"], language["missing"]),
                             (3, 2, 1))
            self.assertEqual(filled["ordinary_source_offers_by_language"], {"en": 3, "la": 1})
            self.assertEqual(slots["expected_text_slots"]["modeled_ordinary_elements"], 3)
            self.assertEqual(filled["ordinary_target_edition_held_by_language"], {"en": 0, "la": 0})
        for row in reports[2]["coverage"]:
            typed = next(item for item in row["typed_coverage"]["languages"]
                         if item["lang"] == "en")
            self.assertEqual(typed["exact_target"], 0)
        self.assertEqual(reports, original)

    def test_single_offer_report_matches_original_untyped_contract(self):
        reports = ordinary_fixture(multiple=False)
        legacy = copy.deepcopy(reports)
        for row in legacy[2]["coverage"]:
            del row["typed_coverage"]
        self.assertEqual(REPORT.build_report(*reports), REPORT.build_report(*legacy))

    def test_duplicate_own_witnesses_do_not_inflate_exact_target_elements(self):
        report = REPORT.build_report(*ordinary_fixture(multiple=True, own=True))
        for family in report["families"]:
            filled = family["textual"]["filled_text_slots"]
            self.assertEqual(filled["ordinary_source_offers_by_language"], {"en": 3, "la": 1})
            self.assertEqual(filled["ordinary_target_edition_held_by_language"], {"en": 2, "la": 1})
            self.assertEqual(filled["lower_bound"], 5 if family["calendar"] == "postconciliar" else 4)

    def test_fabricated_own_bucket_cannot_upgrade_antecedent_witnesses(self):
        reports = ordinary_fixture(multiple=True)
        reports[2]["coverage"][0]["relation_coverage"][0].update(
            relation="own", collation="not-applicable")
        with self.assertRaisesRegex(REPORT.Refused, "relation collation offers contradict typed witnesses"):
            REPORT.build_report(*reports)

    def test_held_and_missing_must_still_partition_modeled_elements(self):
        reports = ordinary_fixture(multiple=True)
        english(reports[2]["coverage"][0])["held"] = 3
        with self.assertRaisesRegex(REPORT.Refused, "does not partition elements"):
            REPORT.build_report(*reports)

    def test_balanced_held_inflation_disagrees_with_typed_unique_coverage(self):
        reports = ordinary_fixture(multiple=True)
        english(reports[2]["coverage"][0]).update(held=3, missing=0, absent=0)
        with self.assertRaisesRegex(REPORT.Refused, "does not match modeled and held elements"):
            REPORT.build_report(*reports)

    def test_witness_offer_tamper_is_not_accepted_as_extra_coverage(self):
        reports = ordinary_fixture(multiple=True)
        reports[2]["coverage"][0]["witnesses"][0]["held"] += 1
        with self.assertRaisesRegex(REPORT.Refused, "witness offers do not match typed coverage"):
            REPORT.build_report(*reports)

    def test_internally_valid_typed_offer_tamper_disagrees_with_witness_manifest(self):
        reports = ordinary_fixture(multiple=True)
        typed = reports[2]["coverage"][0]["typed_coverage"]
        language = next(row for row in typed["languages"] if row["lang"] == "en")
        witness = next(row for row in language["witnesses"] if row["id"] == "edition.english-a")
        witness.update(targets=1, available_targets=1, occurrences=1, available=1)
        typed["counts"]["witness_alternatives"] -= 1
        validate_summary(typed)
        with self.assertRaisesRegex(REPORT.Refused, "witness offers do not match typed coverage"):
            REPORT.build_report(*reports)

    def test_relation_buckets_partition_offers_exactly(self):
        reports = ordinary_fixture(multiple=True)
        reports[2]["coverage"][0]["relation_coverage"][0]["count"] += 1
        with self.assertRaisesRegex(REPORT.Refused, "relation buckets do not partition source offers"):
            REPORT.build_report(*reports)

    def test_missing_or_wrong_scope_typed_report_is_refused(self):
        for value in [None, {"schema": "invalid"}, "invalid"]:
            with self.subTest(value=value):
                reports = ordinary_fixture(multiple=True)
                reports[2]["coverage"][0]["typed_coverage"] = value
                with self.assertRaisesRegex(REPORT.Refused, "typed Ordinary coverage"):
                    REPORT.build_report(*reports)
        reports = ordinary_fixture(multiple=True)
        reports[2]["coverage"][0]["typed_coverage"]["scope"] = "propers"
        with self.assertRaisesRegex(REPORT.Refused, "must use ordinary scope"):
            REPORT.build_report(*reports)


if __name__ == "__main__":
    unittest.main()
