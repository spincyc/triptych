#!/usr/bin/env python3
"""Focused provenance checks for the postconciliar rubric source graph."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"
DOCUMENT = (
    "liturgy/roman-rite/postconciliar/"
    "roman-missal-third-edition-en-us-2011/reference/liturgical-calendar"
)
HTML_PASSAGE_ID = (
    "passage.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-vatican-web-2026-08-26.operative-occurrence-rule"
)
NOTITIAE_PASSAGE_ID = (
    "passage.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-notitiae-392-393.operative-occurrence-rule"
)
HTML_ARTIFACT_ID = (
    "artifact.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-vatican-web-2026-08-26.vatican-html-81fea8ec"
)
NOTITIAE_SEGMENT_ID = (
    "segment.congregation-for-divine-worship-and-the-discipline-of-the-sacraments."
    "notificatio-de-occurrentia-memoriae-immaculati-cordis-1998."
    "latin-notitiae-392-393.notitiae-page-157"
)
NOTITIAE_ARTIFACT_ID = (
    "artifact.holy-see.notitiae.volume-35-numbers-392-393-1999."
    "official-pdf-c42b1215"
)


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = importlib.machinery.SourceFileLoader(
        f"_postconciliar_{name.replace('-', '_')}", str(path)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SOURCE_LIBRARY = load_tool("source-library")
CALENDAR_RUBRICS = load_tool("calendar-rubrics")


class PostconciliarRubricSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = SOURCE_LIBRARY.load_library(ROOT)
        if cls.library.errors:
            raise AssertionError("; ".join(cls.library.errors))
        cls.rubrics = CALENDAR_RUBRICS.load_source(CALENDARS, "postconciliar")

    def test_every_rubric_witness_id_resolves_to_an_exact_controller(self) -> None:
        witnesses = self.rubrics["derived_from"]["witnesses"]
        self.assertTrue(witnesses)
        for witness in witnesses:
            source_id = witness["id"]
            with self.subTest(source_id=source_id):
                record = self.library.records.get(source_id)
                self.assertIsNotNone(record, f"unregistered rubric witness: {source_id}")
                self.assertIn(record.record_type, {"passage", "segment"})

    def test_notification_witnesses_name_both_checked_official_states(self) -> None:
        source_ids = {
            witness["id"]
            for witness in self.rubrics["derived_from"]["witnesses"]
        }
        self.assertTrue({HTML_PASSAGE_ID, NOTITIAE_PASSAGE_ID} <= source_ids)

    def test_notification_passages_pin_the_exact_restricted_artifacts(self) -> None:
        html_passage = self.library.records[HTML_PASSAGE_ID].data
        self.assertEqual(html_passage["artifact_id"], HTML_ARTIFACT_ID)
        self.assertEqual(
            html_passage["artifact_sha256"],
            "81fea8ec1679d73012474791d64e96103ef39cfba77e3914692804afb8e3c36e",
        )
        html_artifact = self.library.records[HTML_ARTIFACT_ID].data
        self.assertEqual(html_artifact["byte_size"], 3672)
        self.assertEqual(html_artifact["storage"], "restricted")
        self.assertEqual(html_artifact["rights_status"], "restricted")
        self.assertNotIn("path", html_artifact)

        notitiae_passage = self.library.records[NOTITIAE_PASSAGE_ID].data
        self.assertEqual(notitiae_passage["segment_id"], NOTITIAE_SEGMENT_ID)
        self.assertEqual(notitiae_passage["artifact_page_ranges"], [[63, 63]])
        segment = self.library.records[NOTITIAE_SEGMENT_ID].data
        self.assertEqual(segment["artifact_id"], NOTITIAE_ARTIFACT_ID)
        self.assertEqual(
            segment["artifact_sha256"],
            "c42b121575fe101de5e7dea0d78e583db921f4cc9af515476e2bcdf4c4285420",
        )

    def test_both_notification_passages_have_reviewed_publication_bindings(self) -> None:
        expected = {HTML_PASSAGE_ID, NOTITIAE_PASSAGE_ID}
        bindings = {
            binding.source_id: binding
            for binding in self.library.bindings
            if binding.document == DOCUMENT and binding.source_id in expected
        }
        self.assertEqual(set(bindings), expected)
        for source_id, binding in bindings.items():
            with self.subTest(source_id=source_id):
                self.assertIn("verified", binding.data["states"])
                self.assertEqual(binding.data["verified_on"], "2026-08-26")
                self.assertEqual(
                    binding.data["source_fingerprint"],
                    SOURCE_LIBRARY.source_fingerprint(self.library, source_id),
                )

    def test_public_rubrics_projection_does_not_expose_the_research_graph(self) -> None:
        built, problems, _ = CALENDAR_RUBRICS.build(CALENDARS, "postconciliar")
        self.assertEqual(problems, [])
        emitted = built[0]
        self.assertNotIn("derived_from", emitted)
        public_json = json.dumps(emitted, sort_keys=True)
        self.assertNotIn(HTML_PASSAGE_ID, public_json)
        self.assertNotIn(NOTITIAE_PASSAGE_ID, public_json)


if __name__ == "__main__":
    unittest.main()
