"""The pre-1955 Holy Week OCR stays a bounded composite witness.

The Internet Archive item once labelled as a 1920 printing combines a
1951--1954 body with a post-1970 appendix.  These tests join the act-history
description back to the canonical artifact manifest and refuse any local claim
that upgrades its identity, rights, storage, or evidentiary ceiling.
"""

from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import pathlib
import tomllib
import unittest

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "act-history"
HOLY_WEEK = ROOT / "src/sources/inventories/roman-holy-week-acts-v1.toml"
PROPERS = ROOT / "src/sources/calendars/roman-pre-1955/propers.yaml"
ARTIFACT = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions/vatican-typica-1920"
    / "artifacts/missale-romanum-1920-text-aa646196/artifact.toml"
)
WITNESS_ID = "missale-romanum-later-composite-pre-1955-body"
ARTIFACT_ID = (
    "artifact.catholic-church.missale-romanum.vatican-typica-1920."
    "missale-romanum-1920-text-aa646196"
)


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "pre1955_act_history_under_test", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class Pre1955HolyWeekWitnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tool = load_tool()
        self.data = self.tool.load(HOLY_WEEK)

    def witness(self, data: dict | None = None) -> dict:
        rows = (data or self.data)["witnesses"]
        return next(row for row in rows if row["id"] == WITNESS_ID)

    def assert_refused(self, field: str, value: str, message: str) -> None:
        data = copy.deepcopy(self.data)
        self.witness(data)[field] = value
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.check(data)
        self.assertIn(message, str(refused.exception))

    def test_composite_identity_and_ceiling_are_explicit(self) -> None:
        witness_ids = {row["id"] for row in self.data["witnesses"]}
        self.assertIn(WITNESS_ID, witness_ids)
        self.assertNotIn("missale-romanum-1920", witness_ids)
        source = HOLY_WEEK.read_text(encoding="utf-8")
        for stale_claim in (
            "The witnesses this tracer read for units are 1862, 1920 and 1962",
            "search of the 1920 and 1862 scans",
            "The 1920 has the full form quoted",
            "Transcribed from the 1920 text layer",
        ):
            self.assertNotIn(stale_claim, source)

        witness = self.witness()
        self.assertEqual(witness["artifact_id"], ARTIFACT_ID)
        self.assertEqual(witness["artifact_storage"], "remote")
        self.assertEqual(witness["rights"], "unresolved")
        self.assertEqual(witness["evidence_scope"], "structural-search-only")
        self.assertEqual(witness["target_edition_correspondence"], "unverified")
        self.assertIn("1951-1954", witness["printed"])
        self.assertIn("1970 or later", witness["printed"])
        self.assertIn("does not identify the physical printing", witness["attests_basis"])
        rendered = self.tool.render_witness(witness)
        self.assertIn("storage:    remote", rendered)
        self.assertIn("evidence:   structural-search-only", rendered)
        self.assertIn("target correspondence: unverified", rendered)

    def test_composite_matches_the_canonical_artifact_record(self) -> None:
        artifact = tomllib.loads(ARTIFACT.read_text(encoding="utf-8"))
        witness = self.witness()
        self.assertEqual(artifact["id"], witness["artifact_id"])
        self.assertEqual(artifact["sha256"], witness["artifact_sha256"])
        self.assertEqual(artifact["storage"], witness["artifact_storage"])
        self.assertEqual(artifact["rights_status"], witness["rights"])
        self.assertIn("THESE BYTES ARE NOT A 1920 PRINTING", artifact["rights_basis"])
        self.tool.check(self.data)

    def test_check_refuses_an_identity_or_rights_upgrade(self) -> None:
        cases = (
            ("artifact_id", "artifact.no-such-source", "is not a canonical source artifact"),
            ("artifact_sha256", "0" * 64, "does not match canonical source artifact"),
            ("artifact_storage", "tracked", "does not match canonical source artifact"),
            ("rights", "public-domain", "does not match canonical source artifact"),
        )
        for field, value, message in cases:
            with self.subTest(field=field):
                self.assert_refused(field, value, message)

    def test_check_refuses_a_structural_witness_claiming_exact_correspondence(self) -> None:
        self.assert_refused(
            "target_edition_correspondence",
            "verified",
            "structural-search-only evidence cannot claim verified target-edition correspondence",
        )
        self.assert_refused(
            "evidence_scope",
            "unbounded",
            "evidence_scope must be one of",
        )

    def test_propers_coverage_names_the_bounded_composite_witness(self) -> None:
        document = yaml.safe_load(PROPERS.read_text(encoding="utf-8"))
        evidence = next(
            row
            for row in document["recension_coverage"]["evidence"]
            if row["id"] == "roman-holy-week-structure"
        )
        self.assertIn(WITNESS_ID, evidence["witnesses"])
        self.assertNotIn("missale-romanum-1920", evidence["witnesses"])
        self.assertIn("later composite", evidence["basis"])
        self.assertIn("structural/search witness", evidence["basis"])
        self.assertIn("does not establish exact target-edition correspondence", evidence["basis"])


if __name__ == "__main__":
    unittest.main()
