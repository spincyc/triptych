#!/usr/bin/env python3
"""Regression checks for the declared two-server Low-Mass model."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
OWNER = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides"
)


class LowMassModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ceremony = (OWNER / "shared/low-mass-ceremony.tex").read_text()
        self.diagrams = (OWNER / "shared/low-mass-diagrams.tex").read_text()
        self.movement = (OWNER / "shared/low-mass-movement.tex").read_text()
        self.diagrams += self.movement
        self.inventory = (OWNER / "research/ceremonial-inventory.md").read_text()

    def macro(self, name: str) -> str:
        """Read one TeX definition while retaining nested groups."""
        marker = rf"\newcommand{{\{name}}}"
        start = self.diagrams.index(marker) + len(marker)
        start = self.diagrams.index("{", start)
        depth, end = 1, start + 1
        while depth:
            if self.diagrams[end] == "{":
                depth += 1
            elif self.diagrams[end] == "}":
                depth -= 1
            end += 1
        return self.diagrams[start + 1 : end - 1]

    def test_gospel_second_never_climbs_and_first_returns_after_start(self) -> None:
        self.assertIn(r"\emph{In illo tempore}", self.ceremony)
        self.assertNotIn("same step level", self.ceremony)
        self.assertNotIn("Second G/Step2", self.inventory)
        for name in ("LMMoveMissalLift", "LMMoveMissalDescent", "LMMoveMissalCentre",
                     "LMMoveMissalAscent", "LMMoveMissalPlaced", "LMMoveMissalStepDown",
                     "LMSceneGospel", "LMMoveGospelDescent", "LMMoveGospelCentre",
                     "LMMoveGospelCross", "LMMoveGospelReturned"):
            body = self.macro(name)
            second = re.findall(r"\\ASGStandingServer\{[^}]+\}\{([^}]+)\}\{SECOND", body)
            self.assertEqual(second, ["11.3"], name + " must leave Second on the floor")
        self.assertIn(r"\ASGStandingServer{29}{22.5}{FIRST}", self.macro("LMSceneGospel"))
        self.assertIn(r"\LMMoveBookRear{50}{11.3}{FIRST}", self.macro("LMMoveMissalCentre"))
        self.assertIn(r"\ASGServerFacingLeft{75}{11.3}{FIRST}", self.macro("LMMoveGospelReturned"))
        self.assertIn("First E/Base/Floor, Second unchanged", self.inventory)

    def test_offertory_formation_and_first_only_ablutions_are_explicit(self) -> None:
        self.assertIn("Side by side on Step 2", self.ceremony)
        self.assertIn("First serves all three pours", self.ceremony, "The First-only allocation must remain explicit")
        self.assertIn("base of the wine-cruet handle", self.ceremony)
        self.assertIn("turns the handle toward the priest", self.ceremony)
        self.assertIn("The priest has blessed the water", self.ceremony)
        self.assertIn("chalice resting on the altar", self.ceremony)
        stages = ("LMSceneWinePurification", "LMSceneFingerWine", "LMSceneFingerWater")
        self.assertEqual(sorted(stages, key=self.ceremony.index), list(stages))
        self.assertIn("C/Pred for wine purification → E/Step2 for finger ablution", self.inventory)

    def test_action_enlargements_reuse_the_complete_sanctuary(self) -> None:
        for scene, detail, art in (
            ("LMSceneWinePurification", "LMWinePurificationDetail", "LMWinePurificationArt"),
            ("LMSceneFingerWine", "LMFingerWineDetail", "LMFingerWineArt"),
            ("LMSceneFingerWater", "LMFingerWaterDetail", "LMFingerWaterArt"),
            ("LMSceneLavaboAction", "LMLavaboActionDetail", "LMLavaboArt"),
            ("LMSceneHostElevation", "LMHostElevationDetail", "LMHostElevationArt"),
            ("LMSceneChaliceElevation", "LMChaliceElevationDetail", "LMChaliceElevationArt"),
        ):
            self.assertIn("\\" + art, self.macro(scene))
            self.assertIn(r"\LMSceneEnlargement", self.macro(detail))
            self.assertNotIn("\\" + art, self.macro(detail))
            self.assertNotIn(r"\includegraphics", self.macro(detail))
            self.assertEqual(len(re.findall(r"ASG-ART-[^}]+\.png", self.macro(art))), 1)
        self.assertIn(r"\ASGSaveScene{\LMPositionWidth}{\ASGLowCandles #1}", self.macro("LMPositionScene"))
        self.assertIn(r"\ASGShowSavedScene", self.macro("LMPositionScene"))
        self.assertIn(r"\ASGSceneViewport", self.macro("LMSceneEnlargement"))
        # A shared actor PNG alone did not preserve architecture. The viewport
        # must reuse the same assembled box and may not load any image itself.
        shared = (OWNER / "shared/sanctuary-scenes.tex").read_text()
        viewport = shared.split(r"\newcommand{\ASGSceneViewport}", 1)[1].split(r"\newcommand", 1)[0]
        self.assertIn(r"\ASGShowSavedScene", viewport)
        self.assertNotIn(r"\includegraphics", viewport)
        self.assertIn("058-finger-ablution-wine-no-altar", self.macro("LMFingerWineArt"))
        self.assertIn("059-finger-ablution-water-no-altar", self.macro("LMFingerWaterArt"))

    def test_last_gospel_and_exit_depict_actual_facing_and_object(self) -> None:
        self.assertIn(r"\LMPriestFacingLeft", self.macro("LMSceneLastGospel"))
        self.assertIn("GOSPEL CARD", self.macro("LMSceneLastGospel"))
        self.assertIn(r"\LMChaliceBearer", self.macro("LMSceneRecess"))
        self.assertNotIn("First pours wine;\\nSecond pours water", self.ceremony)

    def test_coordinated_veil_and_book_exchange_has_no_cover_wait(self) -> None:
        self.assertIn("First takes the folded veil", self.ceremony, "First retains the veil assignment")
        self.assertIn("Second takes the Missal and stand", self.ceremony, "Second retains the book assignment")
        ordered = ("LMMoveExchangeTaken", "LMMoveExchangeYield", "LMMoveExchangeClear",
                   "LMMoveExchangeBookPlaced", "LMMoveExchangeVeilPlaced",
                   "LMMoveExchangeEmptyDescent", "LMMoveExchangeCentre", "LMMoveExchangeReturn")
        self.assertEqual(sorted(ordered, key=self.ceremony.index), list(ordered))
        self.assertNotRegex(self.ceremony, r"[Ww]ait until the (?:priest has )?(?:covered the chalice|chalice is covered)")

    def test_corrected_low_mass_plates_replace_superseded_assets(self) -> None:
        shared_scene = (OWNER / "shared/sanctuary-scenes.tex").read_text()
        self.assertIn("shared/sanctuary-scenes}", self.diagrams)
        self.assertIn("ASG-ART-032-sanctuary-master.png", shared_scene)
        self.assertIn(r"\ASGSaveScene{\LMPositionWidth}", self.diagrams)
        for moment in ("WinePresentation", "WaterPresentation", "WinePurification", "FingerWine", "FingerWater", "ElevationReturn", "BookReturnComplete", "Recess"):
            self.assertIn(r"\newcommand{\LMScene" + moment + "}", self.diagrams)
            self.assertIn(r"\LMScene" + moment, self.ceremony)
        for asset in (
            "ASG-ART-012-lm-gospel-stations",
            "ASG-ART-013-lm-offertory-cruets",
            "ASG-ART-017-lm-mc-first-ablution",
            "ASG-ART-018-lm-mc-ablution",
            "ASG-ART-019-lm-book-and-veil-return",
            "ASG-ART-027-lm-gospel-opening",
            "ASG-ART-028-lm-offertory-formation",
            "ASG-ART-029-lm-first-only-ablutions",
            "ASG-ART-031-lm-veil-missal-exchange",
        ):
            self.assertNotIn(asset, self.diagrams)


if __name__ == "__main__":
    unittest.main()
