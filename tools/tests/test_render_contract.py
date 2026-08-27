#!/usr/bin/env python3
"""Regression checks for the 1962 Low Mass render contract.

Two artistic failures opened this lane: a mirrored Missal and an invented
"TOP VIEW (NAVE)" inset. These tests assert that both are now impossible to
express in the canonical output, independently of the layer's own validator.
"""

import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LAYER = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
    / "render-contract/low-mass/v1"
)
CONTRACTS = LAYER / "contracts"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class RenderContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contracts = {
            path.stem: load(path) for path in sorted(CONTRACTS.glob("*.yaml"))
        }
        cls.camera = load(LAYER / "camera-model.yaml")
        cls.missal = load(LAYER / "missal-orientation.yaml")
        cls.readiness = load(LAYER / "art-readiness.yaml")

    def objects(self, plate: str, object_id: str):
        return [o for o in self.contracts[plate]["objects"] if o["id"] == object_id]

    def actor(self, plate: str, actor_id: str) -> dict:
        return next(a for a in self.contracts[plate]["actors"] if a["id"] == actor_id)

    # -- the two failures ------------------------------------------------
    def test_the_missal_reads_the_same_way_on_both_sides(self) -> None:
        canonical = self.missal["reading_orientation"]["page_up_yaw_deg"]
        by_side: dict[str, set] = {}
        seen = 0
        for plate, contract in self.contracts.items():
            for item in self.objects(plate, "missal"):
                seen += 1
                yaw = item["reading"]["page_up_yaw_deg"]
                self.assertEqual(yaw, canonical, plate)
                self.assertLess(
                    item["reading"]["page_up_vector"][0], 0,
                    f"{plate}: the Missal must read gospelward",
                )
                placement = str(item["placement_semantic"]).lower()
                side = "gospel" if "gospel" in placement else (
                    "epistle" if "epistle" in placement else "other"
                )
                by_side.setdefault(side, set()).add(yaw)
        self.assertGreater(seen, 100)
        self.assertEqual(by_side.get("gospel"), by_side.get("epistle"))

    def test_the_mirrored_missal_yaw_never_occurs(self) -> None:
        forbidden = self.missal["mirror_test"]["forbidden_page_up_yaw_deg"]
        for plate in self.contracts:
            for item in self.objects(plate, "missal"):
                self.assertNotEqual(item["reading"]["page_up_yaw_deg"], forbidden, plate)

    def test_a_place_name_can_never_be_a_projection(self) -> None:
        projections = {p["id"] for p in self.camera["projections"]}
        forbidden = {n.lower() for n in self.camera["forbidden_projection_names"]}
        self.assertFalse(projections & forbidden)
        self.assertIn("orthographic-plan", projections)
        self.assertNotIn("nave", projections)
        for plate, contract in self.contracts.items():
            for panel in contract["panels"]:
                self.assertIn(panel["camera"]["projection"], projections, plate)

    def test_every_plate_closes_its_panel_list(self) -> None:
        for plate, contract in self.contracts.items():
            self.assertEqual(contract["additional_panels"], "forbidden", plate)
            ids = [p["id"] for p in contract["panels"]]
            self.assertTrue(ids, plate)
            self.assertEqual(len(ids), len(set(ids)), plate)

    def test_a_plan_panel_declares_its_page_top(self) -> None:
        for plate, contract in self.contracts.items():
            for panel in contract["panels"]:
                if panel["camera"]["projection"] == "orthographic-plan":
                    self.assertIn(
                        "page_top_world_direction",
                        panel["camera"].get("frame", {}),
                        plate,
                    )

    # -- approved choreography survives compilation ----------------------
    def test_the_crossings_compile_in_opposite_order(self) -> None:
        first, second = self.contracts["LM-136C"], self.contracts["LM-136E"]
        del first, second
        self.assertLess(
            self.actor("LM-136C", "AC2")["position"][1],
            self.actor("LM-136C", "AC1")["position"][1],
        )
        self.assertLess(
            self.actor("LM-136E", "AC1")["position"][1],
            self.actor("LM-136E", "AC2")["position"][1],
        )

    def test_sides_agree_with_the_world_axes(self) -> None:
        for plate, contract in self.contracts.items():
            for actor in contract["actors"]:
                if actor["side"] == "gospel":
                    self.assertLessEqual(actor["position"][0], 0, plate)
                if actor["side"] == "epistle":
                    self.assertGreaterEqual(actor["position"][0], 0, plate)

    # -- the art gate ----------------------------------------------------
    def test_art_ready_scenes_have_no_unresolved_visible_geometry(self) -> None:
        for plate, contract in self.contracts.items():
            if contract["art_readiness"]["status"] != "ready":
                continue
            for item in contract["objects"]:
                self.assertFalse(item.get("unresolved_placement"), plate)
                if item.get("oriented") and item.get("position") is not None:
                    self.assertIsNotNone(item.get("yaw_deg"), f"{plate}/{item['id']}")

    def test_every_blocked_scene_names_its_cue(self) -> None:
        blocked = 0
        for plate, contract in self.contracts.items():
            if contract["art_readiness"]["status"] == "blocked":
                blocked += 1
                self.assertTrue(
                    contract["art_readiness"]["unresolved_cues"], plate
                )
        self.assertEqual(blocked, self.readiness["totals"]["blocked"])

    def test_the_whole_corpus_is_accounted_for(self) -> None:
        totals = self.readiness["totals"]
        self.assertEqual(len(self.contracts), totals["scenes"])
        self.assertEqual(totals["ready"] + totals["blocked"], totals["scenes"])

    # -- the layer's own gates still pass --------------------------------
    def test_the_layer_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(LAYER / "validate.py")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_generated_output_is_current(self) -> None:
        for script, flag in (
            ("compile.py", "--check"),
            ("skeleton.py", "--check"),
            ("review.py", "--check"),
        ):
            result = subprocess.run(
                [sys.executable, str(LAYER / script), flag],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, f"{script}: {result.stderr}")

    def test_the_structural_choreography_is_not_revised_here(self) -> None:
        structural = (
            ROOT
            / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
            / "structural/low-mass/v0.21"
        )
        self.assertTrue((structural / "scenes/inventory.yaml").is_file())
        for contract in self.contracts.values():
            self.assertEqual(contract["structural_baseline_commit"], "d2e97b5ca")


if __name__ == "__main__":
    unittest.main()
