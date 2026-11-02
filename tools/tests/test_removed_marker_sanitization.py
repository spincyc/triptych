"""Invalid resident text cannot cross an explicitly unavailable Latin owner."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_latin as latin


class RemovedMarkerSanitizationTests(unittest.TestCase):
    def setUp(self):
        self.key = latin.LatinKey("fixture-owner", "", "Improperia", "", "", 1)
        self.marker = {
            **latin.REMOVED_TEXT_STATUS,
            "reasons": [{"kind": "rights-withheld"}],
        }

    def test_removed_marker_discards_any_resident_payload_without_losing_english(self):
        for payload in ("Fixture Latin.", {"private": "body"}, ["body"], None):
            with self.subTest(payload_type=type(payload).__name__):
                proper = {
                    "name": "Improperia", "text": payload,
                    "text_status": self.marker,
                    "translations": [{"lang": "en", "text": "Fixture English."}],
                }
                result = latin.sanitize_proper(proper, self.key, {}, ["web"])
                self.assertNotIn("text", result)
                self.assertEqual(result["translations"], proper["translations"])
                self.assertTrue(result["latin"]["withheld"])
                self.assertFalse(result["latin"]["available"])
                self.assertIn("text", proper, "sanitization must not mutate its input")

    def test_valid_removed_owner_and_unmarked_unresolved_owner_stay_unavailable(self):
        removed = latin.sanitize_proper(
            {"name": "Improperia", "text_status": self.marker}, self.key, {}, ["web"])
        self.assertNotIn("text", removed)
        self.assertTrue(removed["latin"]["withheld"])
        unmarked = latin.sanitize_proper(
            {"name": "Improperia", "text": "Fixture Latin."}, self.key, {}, ["web"])
        self.assertIsNone(unmarked["text"])
        self.assertTrue(unmarked["latin"]["withheld"])

    def test_held_unpublished_marker_keeps_its_existing_scrubbing(self):
        result = latin.sanitize_proper({
            "name": "Improperia", "text": "Fixture Latin.",
            "text_status": {"body_status": latin.HELD_UNPUBLISHED_BODY_STATUS},
        }, self.key, {}, ["web"])
        self.assertNotIn("text", result)
        self.assertTrue(result["latin"]["withheld"])

    def test_removed_marker_scrubs_nested_cycles_even_without_matching_records(self):
        owner = {"text": "Fixture Latin.", "text_status": self.marker}
        result = latin.sanitize_proper({
            "name": "Improperia", **owner,
            "cycles": {"A": dict(owner)}, "weekday_cycles": {"I": dict(owner)},
        }, self.key, {}, ["web", "download", "print", "cli", "corpus-data", "public-git"])
        for branch in (result, result["cycles"]["A"], result["weekday_cycles"]["I"]):
            self.assertNotIn("text", branch)
            self.assertTrue(branch["latin"]["withheld"])
            self.assertFalse(branch["latin"]["available"])

    def test_already_validated_permitted_record_keeps_its_body(self):
        body = "Fixture Latin."
        record = {
            "text_sha256": latin.text_sha256(body), "provenance_status": "collated",
            "publication_status": "permitted", "publication_basis": "public-domain",
            "surfaces": ["web"],
        }
        result = latin.sanitize_proper(
            {"name": "Improperia", "text": body}, self.key, {self.key: record}, ["web"])
        self.assertEqual(result["text"], body)
        self.assertFalse(result["latin"]["withheld"])


if __name__ == "__main__":
    unittest.main()
