#!/usr/bin/env python3
"""Regression checks for the artistic entry path.

`test_render_contract.py` guards the room: the Missal yaw, the panel
vocabulary, the crossings. This file guards the door. `art-seed` is the only
sanctioned way to hand a scene to an artistic agent, so what it hands over must
be complete, self-consistent, deterministic, and impossible to obtain for a
scene the structural lane has blocked.
"""

import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "pictographic"
DICTIONARY = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
)
LAYER = DICTIONARY / "render-contract/low-mass/v1"
ARTISTIC = DICTIONARY / "artistic"
PROTOCOL = ARTISTIC / "RENDERING-PROTOCOL.md"
PROVENANCE_CONTRACT = ARTISTIC / "plate-provenance.yaml"

CALENDAR = "roman-1962"
FORM = "low-mass"
CANARY = "LM-001A"
PACKAGE_FILES = (
    "render-contract.yaml",
    "skeleton.svg",
    "provenance.yaml",
    "ART-AGENT-INSTRUCTIONS.md",
)
# The marker skeleton.py emits for each drawn panel.
PANEL_MARKER = re.compile(r"panel ([a-z0-9-]+)</text>")
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")
# Counts that the protocol promises to leave in tooling.
SCENE_COUNTS = re.compile(r"(?<![\w.-])(197|140|57)(?![\w.-])")
ESCAPE_FLAGS = ("--force", "--no-verify", "--skip-readiness", "--skip", "--override")


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


def seed(scene: str, out: Path) -> subprocess.CompletedProcess:
    return run("art-seed", CALENDAR, FORM, scene, "--out", str(out))


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def blocked_listing() -> list[tuple[str, str]]:
    """Every blocked scene the tooling lists, with its first unresolved cue."""
    result = run("readiness", CALENDAR, FORM, "--blocked")
    if result.returncode != 0:
        raise AssertionError(f"readiness failed: {result.stderr}")
    entries = []
    for line in result.stdout.splitlines():
        if not line.startswith("  "):
            continue
        scene, _, cue = line.strip().partition("  ")
        if re.fullmatch(r"LM-[0-9]+[A-Z]?", scene):
            entries.append((scene, cue.strip()))
    return entries


class ArtisticEntryTests(unittest.TestCase):
    """The canary package, seeded once, is the subject of several tests."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._workspace = tempfile.TemporaryDirectory()
        cls.out = Path(cls._workspace.name)
        cls.result = seed(CANARY, cls.out)
        cls.package = cls.out / CANARY
        cls.provenance_contract = load(PROVENANCE_CONTRACT)
        cls.missal = load(LAYER / "missal-orientation.yaml")
        cls.readiness = load(LAYER / "art-readiness.yaml")

    @classmethod
    def tearDownClass(cls) -> None:
        cls._workspace.cleanup()

    def contract(self) -> dict:
        return load(self.package / "render-contract.yaml")

    def provenance(self) -> dict:
        return load(self.package / "provenance.yaml")

    def instructions(self) -> str:
        return (self.package / "ART-AGENT-INSTRUCTIONS.md").read_text(encoding="utf-8")

    def required_field_ids(self) -> list[str]:
        return [f["id"] for f in self.provenance_contract["required_fields"]]

    def declared_values(self, field_id: str) -> list:
        for field in self.provenance_contract["required_fields"]:
            if field["id"] == field_id:
                return field["values"]
        raise AssertionError(f"{field_id} is not a required provenance field")

    # -- a ready scene seeds ---------------------------------------------
    def test_an_art_ready_scene_seeds_a_complete_package(self) -> None:
        self.assertEqual(self.result.returncode, 0, self.result.stderr)
        self.assertTrue(self.package.is_dir(), self.result.stderr)
        for name in PACKAGE_FILES:
            member = self.package / name
            self.assertTrue(member.is_file(), name)
            self.assertGreater(member.stat().st_size, 0, name)
        self.assertEqual(
            sorted(p.name for p in self.package.iterdir()), sorted(PACKAGE_FILES)
        )
        self.assertEqual(self.contract()["plate_id"], CANARY)

        skeleton = (self.package / "skeleton.svg").read_text(encoding="utf-8")
        self.assertTrue(skeleton.startswith("<svg"))
        ElementTree.fromstring(skeleton)

        provenance = self.provenance()
        for field in self.required_field_ids():
            self.assertIn(field, provenance)
            self.assertIsNotNone(provenance[field], field)

    # -- provenance is copied, not authored ------------------------------
    def test_the_provenance_is_copied_from_its_own_contract(self) -> None:
        contract, provenance = self.contract(), self.provenance()
        for field in (
            "plate_id",
            "structural_baseline_commit",
            "render_contract_version",
        ):
            self.assertEqual(provenance[field], contract[field], field)
        self.assertEqual(
            provenance["panel_manifest"], [p["id"] for p in contract["panels"]]
        )
        self.assertEqual(provenance["scene_ids"], list(contract["scene_ids"]))
        for gate in ("structure_review", "art_review"):
            self.assertEqual(provenance[gate], "PENDING", gate)
            self.assertIn(provenance[gate], self.declared_values(gate), gate)

    # -- the hard gate ----------------------------------------------------
    def test_a_blocked_scene_cannot_be_seeded(self) -> None:
        listing = blocked_listing()
        self.assertTrue(listing, "the tooling listed no blocked scene")
        scene, cue = listing[0]
        self.assertNotEqual(scene, CANARY)

        with tempfile.TemporaryDirectory() as workspace:
            out = Path(workspace)
            result = seed(scene, out)
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("REFUSED", result.stderr)
            self.assertIn("BLOCKED_FOR_ART", result.stderr)
            self.assertIn(cue, result.stderr)
            self.assertFalse((out / scene).exists())
            self.assertEqual(list(out.iterdir()), [])

    # -- the canary --------------------------------------------------------
    def test_the_canary_is_marked_and_draws_exactly_one_panel(self) -> None:
        provenance, contract = self.provenance(), self.contract()
        self.assertTrue(provenance["is_pipeline_canary"])
        self.assertEqual(len(provenance["panel_manifest"]), 1)
        self.assertEqual(provenance["additional_panels"], "forbidden")
        self.assertEqual(contract["additional_panels"], "forbidden")

        skeleton = (self.package / "skeleton.svg").read_text(encoding="utf-8")
        drawn = PANEL_MARKER.findall(skeleton)
        self.assertEqual(len(drawn), 1, drawn)
        self.assertEqual(drawn, provenance["panel_manifest"])

        missals = [o for o in contract["objects"] if o["id"] == "missal"]
        self.assertEqual(len(missals), 1)
        reading = missals[0]["reading"]
        self.assertEqual(
            reading["page_up_yaw_deg"],
            self.missal["reading_orientation"]["page_up_yaw_deg"],
        )
        self.assertLess(reading["page_up_vector"][0], 0)

        text = self.instructions()
        self.assertIn(CANARY, text)
        self.assertIn("PIPELINE CANARY", text)

    def test_a_non_canary_scene_is_not_marked_canary(self) -> None:
        other = next(
            s for s in self.readiness["ready_scenes"] if s != CANARY
        )
        with tempfile.TemporaryDirectory() as workspace:
            out = Path(workspace)
            result = seed(other, out)
            self.assertEqual(result.returncode, 0, result.stderr)
            provenance = load(out / other / "provenance.yaml")
            self.assertFalse(provenance["is_pipeline_canary"])
            text = (
                out / other / "ART-AGENT-INSTRUCTIONS.md"
            ).read_text(encoding="utf-8")
            self.assertNotIn("canary", text.lower())

    # -- the binding rule travels with the package -------------------------
    def test_the_instructions_carry_the_binding_rule(self) -> None:
        text = " ".join(self.instructions().split())
        self.assertIn(
            "Generate only from the supplied compiled render contract and "
            "deterministic skeleton.",
            text,
        )
        self.assertIn("Do not restage the scene.", text)
        self.assertIn("two independent decisions", text)
        self.assertIn("STRUCTURE: PASS | FAIL", text)
        self.assertIn("ART: PASS | FAIL", text)
        self.assertIn("A plate is approved only when both are PASS.", text)

    # -- determinism -------------------------------------------------------
    def test_seeding_the_same_scene_twice_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, \
                tempfile.TemporaryDirectory() as second:
            for workspace in (first, second):
                result = seed(CANARY, Path(workspace))
                self.assertEqual(result.returncode, 0, result.stderr)
            for name in PACKAGE_FILES:
                self.assertEqual(
                    (Path(first) / CANARY / name).read_bytes(),
                    (Path(second) / CANARY / name).read_bytes(),
                    name,
                )

    # -- fail closed, with no quiet way round it ---------------------------
    def test_the_entry_path_offers_no_force(self) -> None:
        helped = run("art-seed", "--help")
        self.assertEqual(helped.returncode, 0, helped.stderr)
        source = CLI.read_text(encoding="utf-8")
        for flag in ESCAPE_FLAGS:
            self.assertNotIn(flag, helped.stdout, flag)
            self.assertNotIn(flag, source, flag)

    # -- the durable protocol ----------------------------------------------
    def test_the_protocol_is_discoverable_and_internally_consistent(self) -> None:
        self.assertTrue(PROTOCOL.is_file())
        text = PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("`STRUCTURE`", text)
        self.assertIn("`ART`", text)
        self.assertIn("FORBIDDEN", text)
        self.assertIn("free-form image prompt", text)
        self.assertIn("structural YAML", text)
        self.assertIn("human prose summary", text)

        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            link = target.split("#", 1)[0]
            self.assertTrue(
                (PROTOCOL.parent / link).exists(), f"dangling link: {target}"
            )

        prose = "\n".join(
            line for line in text.splitlines() if not line.lstrip().startswith("|")
        )
        self.assertEqual(SCENE_COUNTS.findall(prose), [], "scene counts live in tooling")


if __name__ == "__main__":
    unittest.main()
