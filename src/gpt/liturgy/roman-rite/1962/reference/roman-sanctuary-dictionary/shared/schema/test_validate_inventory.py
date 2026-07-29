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


def held_record_with_gaps() -> dict:
    return {
        **VALID_RECORD,
        "workflow_state": "held",
        "artwork": [],
        "unresolved_gaps": {
            "qualification": "The source boundary and representative artwork remain unresolved.",
            "gaps": [
                {
                    "id": "gap-test-scope",
                    "kind": "scope",
                    "target_ids": ["obj-test", "clm-test-identity"],
                    "summary": "The source does not establish the proposed universal scope.",
                },
                {
                    "id": "gap-test-artwork",
                    "kind": "artwork",
                    "target_ids": ["obj-test"],
                    "summary": "No checked representative artwork is registered.",
                },
            ],
        },
    }


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

    def test_artwork_render_owner_must_be_depicted(self) -> None:
        record = {**VALID_RECORD, "artwork": [dict(VALID_RECORD["artwork"][0])]}
        record["artwork"][0]["render_owner"] = "obj-other"
        problems = self.validate(record).problems
        self.assertTrue(any("render owner must appear in depicts" in p.message for p in problems))

    def test_artwork_render_owner_accepts_a_depicted_object(self) -> None:
        record = {**VALID_RECORD, "artwork": [dict(VALID_RECORD["artwork"][0])]}
        record["artwork"][0]["render_owner"] = "obj-test"
        self.assertEqual(self.validate(record).problems, [])

    def test_empty_artwork_allowed_before_publication_ready(self) -> None:
        record = {**VALID_RECORD, "workflow_state": "source-audited", "artwork": []}
        self.assertEqual(self.validate(record).problems, [])

    def test_text_only_mode_accepts_empty_artwork(self) -> None:
        record = {
            **VALID_RECORD,
            "workflow_state": "source-audited",
            "presentation_mode": "text-only",
            "artwork": [],
        }
        self.assertEqual(self.validate(record).problems, [])

    def test_text_only_mode_rejects_artwork(self) -> None:
        record = {**VALID_RECORD, "presentation_mode": "text-only"}
        problems = self.validate(record).problems
        self.assertTrue(any("must not register publication artwork" in p.message for p in problems))

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

    def test_practical_local_furnishing_is_valid_but_not_selected(self) -> None:
        record = {
            **VALID_RECORD,
            "workflow_state": "source-audited",
            "statuses": ["practical-local-furnishing"],
            "presentation_mode": "text-only",
            "artwork": [],
        }
        check = self.validate(record)
        self.assertEqual(check.problems, [])
        self.assertTrue(all(check.selected(edition) == [] for edition in check.editions["editions"]))

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

    def test_held_record_can_preserve_concrete_gaps(self) -> None:
        self.assertEqual(self.validate(held_record_with_gaps()).problems, [])

    def test_unresolved_gaps_require_nonempty_gap_list(self) -> None:
        record = held_record_with_gaps()
        record["unresolved_gaps"]["gaps"] = []
        problems = self.validate(record).problems
        self.assertTrue(any(p.field == "unresolved_gaps.gaps" for p in problems))

    def test_unresolved_gap_target_must_be_local(self) -> None:
        record = held_record_with_gaps()
        record["unresolved_gaps"]["gaps"][0]["target_ids"] = ["obj-other"]
        problems = self.validate(record).problems
        self.assertTrue(any("unknown or nonlocal target" in p.message for p in problems))

    def test_held_record_is_not_selected_for_publication(self) -> None:
        check = self.validate(held_record_with_gaps())
        edition = next(
            entry
            for entry in check.editions["editions"]
            if entry["id"] == "ed-comprehensive"
        )
        self.assertEqual(check.selected(edition), [])

    def test_publication_ready_gate_still_rejects_unverified_claim(self) -> None:
        claims = [dict(claim) for claim in VALID_RECORD["claims"]]
        claims[0]["evidence_state"] = "unverified-lead"
        record = {**VALID_RECORD, "claims": claims}
        problems = self.validate(record).problems
        self.assertTrue(
            any("not allowed for publication-ready object" in p.message for p in problems)
        )


if __name__ == "__main__":
    unittest.main()
