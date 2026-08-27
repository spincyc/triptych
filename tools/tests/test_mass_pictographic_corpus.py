#!/usr/bin/env python3
"""Regression checks for the recovered 1962 Low Mass pictographic scene corpus.

The owner ships its own validator; this suite runs it, so the corpus is gated
by `make check-tests` and cannot drift unnoticed, and then asserts the locked
corrections separately from the validator that enforces them.
"""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNER = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
    / "structural/low-mass/v0.21"
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MassPictographicCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = _load("mass_pictographic_validate", OWNER / "validate.py")
        _, _, _, _, cls.scenes, _ = cls.validator.load_scene_corpus()
        cls.by_id = {scene["scene_id"]: scene for scene in cls.scenes}

    def actor(self, scene_id: str, actor_id: str) -> dict:
        return next(
            a for a in self.by_id[scene_id]["actors"] if a["id"] == actor_id
        )

    def rings(self, scene_id: str, actor_id: str) -> int:
        return sum(
            bell.get("count") or 0
            for bell in self.by_id[scene_id].get("bells") or []
            if bell["actor"] == actor_id
        )

    def test_owner_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(OWNER / "validate.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: recovered scene corpus", result.stdout)

    def test_storyboards_match_the_scene_corpus(self) -> None:
        result = subprocess.run(
            [sys.executable, str(OWNER / "render-storyboards.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_the_whole_low_mass_is_covered_in_order(self) -> None:
        orders = sorted(scene["order"] for scene in self.scenes)
        self.assertEqual(orders, list(range(1, len(self.scenes) + 1)))
        ordered = sorted(self.scenes, key=lambda scene: scene["order"])
        self.assertEqual(ordered[0]["scene_id"], "LM-001A")
        self.assertEqual(ordered[-1]["scene_id"], "LM-140C")
        self.assertNotIn("LM-137B", self.by_id)

    def test_ablutions_are_served_by_the_first_acolyte_alone(self) -> None:
        for scene_id in ("LM-136A", "LM-136B"):
            handlers = {
                item["handled_by"]
                for item in self.by_id[scene_id]["objects"]
                if item["id"] in {"wine-cruet", "water-cruet"}
            }
            self.assertNotIn("AC2", handlers)
        self.assertEqual(self.actor("LM-136B", "AC1")["anchor"], "step-3-epistle")

    def test_the_post_ablution_crossings_keep_their_order(self) -> None:
        first = self.by_id["LM-136C"]
        second = self.by_id["LM-136E"]
        self.assertLess(
            self.actor("LM-136C", "AC2")["depth_rank"],
            self.actor("LM-136C", "AC1")["depth_rank"],
        )
        self.assertLess(
            self.actor("LM-136E", "AC1")["depth_rank"],
            self.actor("LM-136E", "AC2")["depth_rank"],
        )
        self.assertNotIn(
            "AC1",
            {item["handled_by"] for item in first["objects"] if item["id"] == "missal"},
        )
        self.assertNotIn(
            "AC1",
            {item["handled_by"] for item in second["objects"] if item["id"] == "missal"},
        )

    def test_the_consecration_bell_profile_is_one_ring_at_each_cue(self) -> None:
        for scene_id in (
            "LM-098A", "LM-099A", "LM-100A", "LM-103A", "LM-103B", "LM-103C",
        ):
            self.assertEqual(self.rings(scene_id, "AC1"), 1, scene_id)
            self.assertEqual(self.rings(scene_id, "AC2"), 0, scene_id)
        self.assertEqual(self.rings("LM-134C", "AC1"), 3)
        self.assertFalse(self.by_id["LM-112C"].get("bells"))

    def test_the_missal_is_never_mirrored(self) -> None:
        for scene in self.scenes:
            for item in scene.get("objects") or []:
                if item["id"] == "missal":
                    self.assertIn(
                        item.get("orientation"),
                        {"priest-reads-facing-left", "not-applicable", None},
                        scene["scene_id"],
                    )

    def test_the_gloria_is_said_at_the_centre(self) -> None:
        for scene_id in ("LM-022A", "LM-022B", "LM-023A", "LM-024A"):
            self.assertEqual(self.actor(scene_id, "priest")["side"], "centre")

    def test_all_three_sign_themselves_at_the_indulgentiam(self) -> None:
        for actor_id in ("priest", "AC1", "AC2"):
            self.assertIn(
                "sign-of-the-cross",
                self.actor("LM-010A", actor_id)["gestures"],
            )

    def test_the_superseded_guides_are_fenced_where_a_reader_lands(self) -> None:
        guides = ROOT / "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides"
        for relative in (
            "shared/low-mass-ceremony.tex",
            "shared/low-mass-diagrams.tex",
            "research/scope.md",
            "research/ceremonial-inventory.md",
            "research/source-audit.md",
            "01-low-mass/research/staleness-review-2026-07-29.md",
        ):
            self.assertIn(
                "Historical / pre-v0.21",
                (guides / relative).read_text(encoding="utf-8"),
                relative,
            )


if __name__ == "__main__":
    unittest.main()
