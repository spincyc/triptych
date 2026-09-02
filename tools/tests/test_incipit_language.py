"""An incipit is labelled Latin apparatus, not a requested-language text."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402


class IncipitOnlyMaterialTest(unittest.TestCase):
    def setUp(self):
        self.proper = {
            "name": "Entrance Antiphon",
            "source": "scripture",
            "incipit": "Ad te levavi",
            "verses": [{"ref": "Psalm 25:1-3"}],
        }

    def test_english_request_keeps_latin_language_and_incipit_extent(self):
        material = _calendars.incipit_only_of(self.proper, "en")

        self.assertEqual(
            material,
            {
                "text": "Ad te levavi",
                "language": "la",
                "extent": "incipit",
                "requested_language": "en",
                "note": "Latin incipit only; no en rendering recorded",
            },
        )

    def test_citation_does_not_turn_incipit_into_scripture_rendering(self):
        material = _calendars.incipit_only_of(self.proper, "en")

        self.assertEqual(material["extent"], "incipit")
        self.assertEqual(material["language"], "la")
        self.assertEqual(self.proper["verses"][0]["ref"], "Psalm 25:1-3")

    def test_latin_request_still_says_that_only_the_incipit_is_held(self):
        material = _calendars.incipit_only_of(self.proper, "la")

        self.assertEqual(material["note"], "Latin incipit only")
        self.assertEqual(material["requested_language"], "la")

    def test_requested_witness_is_named_without_supplying_words(self):
        material = _calendars.incipit_only_of(self.proper, "en", "licensed-edition")

        self.assertEqual(material["requested_witness"], "licensed-edition")
        self.assertEqual(
            material["note"],
            "Latin incipit only; no en rendering from licensed-edition recorded",
        )

    def test_no_incipit_has_no_apparatus(self):
        self.assertIsNone(
            _calendars.incipit_only_of(
                {"name": "First Reading", "source": "scripture"}, "en"
            )
        )

    def test_composed_incipit_belongs_to_typed_unavailable_path(self):
        self.assertIsNone(
            _calendars.incipit_only_of(
                {
                    "name": "Collect",
                    "source": "composed",
                    "incipit": "Da, quaesumus, omnipotens Deus",
                    "unavailable_translations": [
                        {"lang": "en", "reason": "rights-restricted"}
                    ],
                },
                "en",
            )
        )

    def test_selected_body_suppresses_incipit_apparatus(self):
        proper = {
            **self.proper,
            "text": "Corpus Latinum",
            "translations": [{"lang": "en", "text": "Tracked rendering"}],
        }

        self.assertIsNone(_calendars.incipit_only_of(proper, "en"))


if __name__ == "__main__":
    unittest.main()
