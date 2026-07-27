#!/usr/bin/env python3
"""Unit tests for the Roman Sanctuary Dictionary inventory validator."""

from __future__ import annotations

import unittest
from pathlib import Path

from validate_inventory import DEFAULT_EDITIONS, DEFAULT_SCHEMA, Validator, load_toml


VALID_RECORD = {
    "schema_version": 1,
    "id": "obj-test",
    "workflow_state": "publication-ready",
    "preferred_english_name": "Test object",
    "latin_headword": "res probatoria",
    "categories": ["service-objects"],
    "periods": ["roman-1962-horizon"],
    "statuses": ["universal-roman"],
    "ceremonies": ["low-mass"],
    "presence": {"locations": ["sanctuary"], "contexts": ["Low Mass"]},
    "handling": {
        "ordinary_handlers": ["acolyte"],
        "server_relation": "handles",
    },
    "audience_relevance": {
        "altar_server": "required",
        "sacristan": "useful",
        "mc_trainer": "useful",
        "general_reader": "required",
        "pontifical": "exclude",
    },
    "claims": [
        {
            "id": f"clm-test-{kind}",
            "kind": kind,
            "text": f"Test {kind}.",
            "evidence_state": "checked-paraphrase",
            "source_ids": ["src-test"],
        }
        for kind in ("identity", "appearance", "liturgical-use", "ceremonial-presence")
    ],
    "sources": [
        {
            "id": "src-test",
            "binding": "test-binding",
            "locus": "test locus",
            "role": "governing-liturgical-book",
            "verification_state": "claim-verified",
        }
    ],
    "artwork": [
        {
            "id": "art-test",
            "view": "isolated",
            "asset": "assets/test.png",
            "review_state": "approved",
            "depicts": ["obj-test"],
            "scale_mode": "not-applicable",
        }
    ],
}


def validator() -> Validator:
    return Validator(load_toml(DEFAULT_SCHEMA), load_toml(DEFAULT_EDITIONS))


class ValidatorTests(unittest.TestCase):
    def validate(self, record: dict) -> Validator:
        check = validator()
        check.validate_record(Path("fixture.toml"), record)
        check.validate_cross_references()
        check.validate_publication_gate()
        return check

    def test_publication_ready_record_passes(self) -> None:
        self.assertEqual(self.validate(VALID_RECORD).problems, [])

    def test_unknown_field_is_rejected(self) -> None:
        record = dict(VALID_RECORD, mystery=True)
        problems = self.validate(record).problems
        self.assertTrue(any(p.field == "mystery" for p in problems))

    def test_broken_source_reference_is_rejected(self) -> None:
        record = {**VALID_RECORD, "claims": [dict(c) for c in VALID_RECORD["claims"]]}
        record["claims"][0]["source_ids"] = ["src-missing"]
        problems = self.validate(record).problems
        self.assertTrue(any("unknown local source" in p.message for p in problems))

    def test_unapproved_art_blocks_publication_ready(self) -> None:
        record = {**VALID_RECORD, "artwork": [dict(VALID_RECORD["artwork"][0])]}
        record["artwork"][0]["review_state"] = "generated"
        problems = self.validate(record).problems
        self.assertTrue(any("not allowed for publication-ready" in p.message for p in problems))

    def test_empty_artwork_allowed_before_publication_ready(self) -> None:
        record = {**VALID_RECORD, "workflow_state": "source-audited", "artwork": []}
        self.assertEqual(self.validate(record).problems, [])

    def test_empty_artwork_blocks_publication_ready(self) -> None:
        record = {**VALID_RECORD, "artwork": []}
        problems = self.validate(record).problems
        self.assertTrue(any("requires at least one artwork" in p.message for p in problems))

    def test_server_selection_includes_recognizes_only(self) -> None:
        record = {
            **VALID_RECORD,
            "handling": {
                "ordinary_handlers": ["priest"],
                "server_relation": "recognizes-only",
            },
        }
        check = self.validate(record)
        edition = next(e for e in check.editions["editions"] if e["id"] == "ed-altar-server")
        self.assertEqual(check.selected(edition), ["obj-test"])

    def test_excluded_relevance_is_not_selected(self) -> None:
        relevance = dict(VALID_RECORD["audience_relevance"], altar_server="exclude")
        check = self.validate({**VALID_RECORD, "audience_relevance": relevance})
        edition = next(e for e in check.editions["editions"] if e["id"] == "ed-altar-server")
        self.assertEqual(check.selected(edition), [])

    def test_historical_record_requires_chronology(self) -> None:
        record = {
            **VALID_RECORD,
            "statuses": ["historical-discontinued-before-1962"],
            "periods": ["medieval"],
        }
        problems = self.validate(record).problems
        self.assertTrue(any("chronology claim" in p.message for p in problems))

    def test_malformed_nested_record_reports_instead_of_crashing(self) -> None:
        record = {**VALID_RECORD, "claims": ["not-a-table"]}
        problems = self.validate(record).problems
        self.assertTrue(any(p.field == "claims[0]" for p in problems))

    def test_shared_multi_object_artwork_id_is_allowed(self) -> None:
        first = {**VALID_RECORD, "workflow_state": "source-audited"}
        second_art = dict(VALID_RECORD["artwork"][0])
        second_art["depicts"] = ["obj-test", "obj-second"]
        first_art = dict(second_art)
        first = {**first, "artwork": [first_art]}
        second = {
            **VALID_RECORD,
            "id": "obj-second",
            "workflow_state": "source-audited",
            "claims": [
                {**claim, "id": claim["id"].replace("test", "second")}
                for claim in VALID_RECORD["claims"]
            ],
            "artwork": [second_art],
        }
        check = validator()
        check.validate_record(Path("first.toml"), first)
        check.validate_record(Path("second.toml"), second)
        check.validate_cross_references()
        check.validate_publication_gate()
        self.assertEqual(check.problems, [])

    def test_conflicting_shared_artwork_definition_is_rejected(self) -> None:
        first = {**VALID_RECORD, "workflow_state": "source-audited"}
        second_art = dict(VALID_RECORD["artwork"][0])
        second_art["asset"] = "assets/different.png"
        second_art["depicts"] = ["obj-test", "obj-second"]
        first_art = dict(VALID_RECORD["artwork"][0])
        first_art["depicts"] = ["obj-test", "obj-second"]
        first = {**first, "artwork": [first_art]}
        second = {
            **VALID_RECORD,
            "id": "obj-second",
            "workflow_state": "source-audited",
            "claims": [
                {**claim, "id": claim["id"].replace("test", "second")}
                for claim in VALID_RECORD["claims"]
            ],
            "artwork": [second_art],
        }
        check = validator()
        check.validate_record(Path("first.toml"), first)
        check.validate_record(Path("second.toml"), second)
        self.assertTrue(any("shared artwork definition conflicts" in p.message for p in check.problems))


if __name__ == "__main__":
    unittest.main()
