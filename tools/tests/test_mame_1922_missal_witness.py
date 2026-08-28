#!/usr/bin/env python3
"""Keep the exact Mame witness, page bounds, and target-edition gate honest."""

from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
EDITION_DIR = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "1922-tours-mame-editio-quarta-iuxta-typicam"
)
ARTIFACT_PATH = EDITION_DIR / "artifacts/ia-scan-pdf-9873693a/artifact.toml"
PASSAGES = EDITION_DIR / "passages"
CALENDAR = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
PROPERS_GUIDANCE = ROOT / "guidance/propers-for-agents.md"
ACQUISITION = (
    ROOT
    / "src/sources/inventories/postconciliar-sanctoral-acquisition-v1.toml"
)
STRUCTURE_EDITION = (
    ROOT
    / "src/web/data/structure/sources/editions/catholic-church/missale-romanum"
    / "1922-1922-tours-mame-editio-quarta-iuxta-typicam.json"
)

EDITION_ID = (
    "edition.catholic-church.missale-romanum."
    "1922-tours-mame-editio-quarta-iuxta-typicam"
)
ARTIFACT_ID = (
    "artifact.catholic-church.missale-romanum."
    "1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a"
)
DIGEST = "9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005"


def load(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


class Mame1922WitnessTests(unittest.TestCase):
    def test_exact_printing_is_not_misregistered_as_the_typical_edition(self) -> None:
        edition = load(EDITION_DIR / "edition.toml")

        self.assertEqual(edition["id"], EDITION_ID)
        self.assertEqual(edition["work_id"], "work.catholic-church.missale-romanum")
        self.assertEqual(edition["date"], "1922")
        self.assertIn("Alfred Mame", edition["publication"])
        self.assertIn("Editio quarta juxta typicam Vaticanam", edition["publication"])
        self.assertIn("not a typical edition", edition["authority"])
        self.assertNotEqual(
            edition["id"],
            "edition.catholic-church.missale-romanum.vatican-typica-1920",
        )

    def test_whole_pdf_identity_and_rights_are_exact(self) -> None:
        artifact = load(ARTIFACT_PATH)

        self.assertEqual(artifact["schema"], 2)
        self.assertEqual(artifact["id"], ARTIFACT_ID)
        self.assertEqual(artifact["edition_id"], EDITION_ID)
        self.assertEqual(artifact["storage"], "remote")
        self.assertEqual(artifact["rights_status"], "public-domain")
        self.assertEqual(artifact["rights_jurisdiction"], "United States")
        self.assertEqual(artifact["sha256"], DIGEST)
        self.assertEqual(artifact["byte_size"], 51_720_493)
        self.assertEqual(artifact["page_count"], 1_162)
        self.assertEqual(
            artifact["source_url"],
            "https://archive.org/download/missaleromanum0000unse/"
            "missaleromanum0000unse.pdf",
        )
        self.assertIn("before the pre-1931", artifact["rights_basis"])
        self.assertIn("not on Internet Archive availability", artifact["rights_basis"])

    def test_visual_passage_bounds_keep_universal_and_appendix_claims_apart(
        self,
    ) -> None:
        expected = {
            "title-imprint-and-conformity.toml": [[13, 13], [15, 15]],
            "may-20-to-25-universal-sanctoral.toml": [[712, 713]],
            "saint-bede-venerable.toml": [[715, 716]],
            "saint-rita-cascia-pro-aliquibus-locis.toml": [[1109, 1111]],
        }
        passages = {name: load(PASSAGES / name) for name in expected}

        for name, ranges in expected.items():
            with self.subTest(passage=name):
                passage = passages[name]
                self.assertEqual(passage["artifact_id"], ARTIFACT_ID)
                self.assertEqual(passage["artifact_sha256"], DIGEST)
                self.assertEqual(passage["artifact_page_ranges"], ranges)
                self.assertEqual(
                    passage["states"],
                    ["cataloged", "acquired", "inspected", "verified"],
                )
                self.assertEqual(passage["verified_on"], "2026-08-27")
                self.assertNotIn("text", passage)

        universal = passages["may-20-to-25-universal-sanctoral.toml"]["context"]
        rita = passages["saint-rita-cascia-pro-aliquibus-locis.toml"]["context"]
        bede = passages["saint-bede-venerable.toml"]["context"]
        self.assertIn("no 22 May entry", universal)
        self.assertIn("This is not an absence from the book", universal)
        self.assertIn("Missae pro aliquibus locis", rita)
        for oration in ("Collect", "Secret", "Postcommunion"):
            self.assertIn(oration, rita)
        self.assertIn("Collect, Secret, and Postcommunion", bede)
        for context in (rita, bede):
            self.assertIn("does not establish identity", context)

    def test_postconciliar_records_bind_findings_without_importing_prayers(self) -> None:
        calendar = CALENDAR.read_text(encoding="utf-8")
        calendar_data = yaml.safe_load(calendar)
        masses = {
            mass["key"]: mass
            for section in calendar_data["sections"].values()
            for mass in section["masses"]
        }
        acquisition = load(ACQUISITION)
        mame = next(
            row
            for row in acquisition["works"]
            if row["id"] == "missale-romanum-1922-mame"
        )

        self.assertEqual(mame["registered_as"], ARTIFACT_ID)
        self.assertTrue(mame["surveyed"])
        self.assertTrue(mame["redistributable"])
        self.assertFalse(mame["landed"])
        self.assertIn("Exact target-edition collation remains open", mame["why_not"])
        self.assertIn(
            "acquisition question for Bede and Rita is closed",
            acquisition["open_items"]["historical_oration_collation"],
        )
        rita_notes = masses["saint-rita-cascia-religious"]["notes"]
        bede_notes = masses["saint-bede-venerable-priest-doctor-church"]["notes"]
        fatima_notes = masses["our-lady-fatima"]["notes"]
        self.assertIn(
            "1922-tours-mame-editio-quarta-iuxta-typicam."
            "saint-rita-cascia-pro-aliquibus-locis",
            rita_notes,
        )
        self.assertIn(
            "1922-tours-mame-editio-quarta-iuxta-typicam.saint-bede-venerable",
            bede_notes,
        )
        self.assertNotIn("1922-tours-mame", fatima_notes)
        self.assertIn("No exact", fatima_notes)
        self.assertIn("exemplar is carried or acquired", fatima_notes)
        self.assertIn("no exact target-edition", rita_notes)
        self.assertIn("exemplar is carried", rita_notes)
        self.assertIn("no prayer body is imported", bede_notes)

    def test_browser_source_binding_is_identity_only(self) -> None:
        structure = json.loads(STRUCTURE_EDITION.read_text(encoding="utf-8"))

        self.assertEqual(structure["edition"]["id"], EDITION_ID)
        self.assertEqual(len(structure["passages"]), 4)
        self.assertEqual(
            {passage["artifact_id"] for passage in structure["passages"]},
            {ARTIFACT_ID},
        )
        for passage in structure["passages"]:
            self.assertFalse(passage["readable"])
            self.assertEqual(passage["withheld"], "storage")
            self.assertNotIn("text", passage)
            self.assertNotIn("text_path", passage)

    def test_guidance_closes_acquisition_without_claiming_target_collation(self) -> None:
        guidance = PROPERS_GUIDANCE.read_text(encoding="utf-8")

        self.assertIn(
            "31 of 53 now have a located public-domain historical source", guidance
        )
        self.assertIn("0 remain undecided as acquisition questions", guidance)
        self.assertIn("Target-edition\ncollation is a separate gate", guidance)
        self.assertIn("[79]-[81]", guidance)
        self.assertNotIn("WITH NO FULL-TEXT ARTIFACT", guidance)


if __name__ == "__main__":
    unittest.main()
