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


def priestly_review_record() -> dict:
    claims = [dict(claim) for claim in VALID_RECORD["claims"]]
    claims[0]["evidence_state"] = "unverified-lead"
    artwork = [dict(VALID_RECORD["artwork"][0])]
    artwork[0]["review_state"] = "identity-checked"
    return {
        **VALID_RECORD,
        "workflow_state": "priestly-review-ready",
        "claims": claims,
        "artwork": artwork,
        "review_readiness": {
            "qualification": "Identity and artwork remain submitted for priestly review; this record is not publication-ready.",
            "disclosed_gaps": [
                {
                    "id": "gap-test-identity",
                    "kind": "claim",
                    "target_ids": ["clm-test-identity"],
                    "summary": "The identity claim remains an unverified lead.",
                },
                {
                    "id": "gap-test-artwork",
                    "kind": "artwork",
                    "target_ids": ["art-test"],
                    "summary": "The drawing has identity review only.",
                },
            ],
            "review_prompts": [
                {
                    "id": "prq-test-identity-art",
                    "question": "Are the identification and depicted form suitable for further development?",
                    "gap_ids": ["gap-test-identity", "gap-test-artwork"],
                    "target_ids": ["clm-test-identity", "art-test"],
                }
            ],
        },
    }


class ValidatorTests(unittest.TestCase):
    def validate(self, record: dict) -> Validator:
        check = validator()
        check.validate_record(Path("fixture.toml"), record)
        check.validate_cross_references()
        check.validate_priestly_review_gate()
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

    def test_qualified_unresolved_record_can_be_priestly_review_ready(self) -> None:
        self.assertEqual(self.validate(priestly_review_record()).problems, [])

    def test_priestly_review_ready_requires_targeted_claim_gap(self) -> None:
        record = priestly_review_record()
        record["review_readiness"]["disclosed_gaps"] = [
            record["review_readiness"]["disclosed_gaps"][1]
        ]
        record["review_readiness"]["review_prompts"][0]["gap_ids"] = [
            "gap-test-artwork"
        ]
        problems = self.validate(record).problems
        self.assertTrue(any("claim requires a targeted disclosed gap" in p.message for p in problems))

    def test_priestly_review_ready_requires_prompt_for_every_gap(self) -> None:
        record = priestly_review_record()
        record["review_readiness"]["review_prompts"][0]["gap_ids"] = [
            "gap-test-identity"
        ]
        problems = self.validate(record).problems
        self.assertTrue(any("has no review prompt" in p.message for p in problems))

    def test_priestly_review_ready_with_no_art_needs_object_art_gap(self) -> None:
        record = priestly_review_record()
        record["artwork"] = []
        record["review_readiness"]["disclosed_gaps"][1]["target_ids"] = [
            "obj-test"
        ]
        record["review_readiness"]["review_prompts"][0]["target_ids"] = [
            "clm-test-identity",
            "obj-test",
        ]
        self.assertEqual(self.validate(record).problems, [])

    def test_priestly_review_ready_is_not_selected_for_publication(self) -> None:
        check = self.validate(priestly_review_record())
        edition = next(
            entry
            for entry in check.editions["editions"]
            if entry["id"] == "ed-comprehensive"
        )
        self.assertEqual(check.selected(edition), [])

    def test_publication_ready_gate_still_rejects_unverified_claim(self) -> None:
        record = priestly_review_record()
        record["workflow_state"] = "publication-ready"
        problems = self.validate(record).problems
        self.assertTrue(
            any("not allowed for publication-ready object" in p.message for p in problems)
        )


if __name__ == "__main__":
    unittest.main()
