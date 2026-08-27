#!/usr/bin/env python3
"""Regression checks for what an oriented object becomes on the page.

`test_render_underlay.py` guards the drawing; this file guards the one
property the drawing could not be trusted about. The LM-001A canary showed the
Missal on the correct Epistle side and visibly mis-oriented: it read square to
the nave instead of embodying its compiled 135-degree yaw. The transform was
never wrong. The drawn page-up direction matched the projection of the
contract's own page-up vector to within a degree, and every earlier check
passed, because every earlier check compared world-space numbers and never
what reached the page.

The failure was projective degeneracy. The camera sat low enough that the
horizontal plane was seen at a grazing angle, so the book's two principal axes
projected to within about 22 degrees of collinear — a flat smear in which no
yaw can look like anything.

So there are two separate properties, and these tests hold both apart:

  fidelity    the drawn page-up agrees with the projection of the contract's
              own world page-up vector, so the model embodies the transform
  legibility  the two projected principal axes stay far enough from collinear
              that an orientation can be seen at all

Every test that guards a property is paired with one that breaks it, because a
check that cannot fail guards nothing. The mirrored-yaw case proves fidelity
would catch a wrong-axis transform; the lowered-camera case reproduces the
reported defect exactly — a perfect transform in an unreadable picture — which
is the whole reason the legibility floor had to exist.
"""

from __future__ import annotations

import copy
import importlib.util
import math
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
DICTIONARY = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
)
LAYER = DICTIONARY / "render-contract/low-mass/v1"
CONTRACTS = LAYER / "contracts"
OBJECT_LIBRARY = LAYER / "underlay-objects.yaml"
VALIDATE = LAYER / "validate.py"

# The canary: the Missal open on the Epistle side, at positive world X.
CANARY = "LM-001A"
# The same book at the Gospel corner, at negative world X, reading identically.
GOSPEL_SIDE = "LM-033A"

# The objects whose horizontal orientation carries meaning, and which
# validate.py therefore measures.
ORIENTED_OBJECTS = ("missal", "missal-stand", "burse", "paten")

# The fidelity threshold validate.py enforces. Kept as a literal here on
# purpose: if the validator ever loosens it, this file should keep failing
# rather than follow it down.
FIDELITY_TOLERANCE_DEG = 1.5
# "Indistinguishable from exact" — used where a test claims fidelity is
# untouched by a change, not merely inside tolerance.
EXACT_DEG = 0.01

# The camera at which the defect was reported: the nave-centre eye before it
# was raised to 3.6, and the original lower eye before that.
REPORTED_CAMERA_XYZ = [0.0, -3.6, 2.35]
ORIGINAL_CAMERA_XYZ = [0.0, -3.6, 1.6]

# A dot product of unit vectors is exact arithmetic on authored 0s and 1s, but
# compare with a tolerance so the contract is "parallel", not "equal strings".
AXIS_TOLERANCE = 1e-6


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def module_at(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unit(vector) -> list[float]:
    length = math.sqrt(sum(c * c for c in vector))
    if not length:
        raise AssertionError(f"a declared axis is the zero vector: {vector}")
    return [c / length for c in vector]


def dot(a, b) -> float:
    return sum(x * y for x, y in zip(unit(a), unit(b)))


def is_side_elevation(contract: dict) -> bool:
    """validate.py's exemption, matched exactly.

    A true side elevation collapses one horizontal axis on purpose; demanding
    legibility there would be demanding the view not be itself.
    """
    primary = contract["panels"][0]["camera"]
    return bool(
        primary.get("collapses_equal_depth")
        or primary["projection"].endswith("elevation-side")
    )


class ProjectedOrientationTests(unittest.TestCase):
    """Every compiled contract, measured through the contract's own camera."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.underlay = module_at(LAYER / "underlay.py", "_test_orientation_underlay")
        cls.validate = module_at(VALIDATE, "_test_orientation_validate")
        cls.library = load(OBJECT_LIBRARY)
        cls.floor = float(
            cls.library["local_frame_contract"]["legibility"][
                "minimum_axis_separation_deg"
            ]
        )
        cls.contracts = {
            path.stem: load(path) for path in sorted(CONTRACTS.glob("*.yaml"))
        }

    # -- helpers ---------------------------------------------------------
    def contract(self, plate: str) -> dict:
        """A private deep copy, so no test can perturb another."""
        self.assertIn(plate, self.contracts, f"{plate}: no compiled contract")
        return copy.deepcopy(self.contracts[plate])

    def item(self, contract: dict, object_id: str) -> dict:
        return next(o for o in contract["objects"] if o["id"] == object_id)

    def measure(self, contract: dict, object_id: str) -> dict:
        measured = self.underlay.projected_orientation(contract, object_id)
        self.assertIsNotNone(
            measured,
            f"{contract['plate_id']}/{object_id}: no measurable orientation; "
            "the object is absent, unplaced or unoriented",
        )
        return measured

    def art_ready(self):
        for plate, contract in sorted(self.contracts.items()):
            if contract["art_readiness"]["status"] == "ready":
                yield plate, contract

    # -- 1, 2: fidelity, both sides of the altar -------------------------
    def test_canary_missal_is_drawn_where_the_contract_points(self):
        """The drawn page-up matches the contract's own world page-up vector.

        This is the property the canary never actually violated, and the
        reason the real defect stayed hidden for so long.
        """
        measured = self.measure(self.contract(CANARY), "missal")
        self.assertLess(
            measured["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
            f"{CANARY}: the drawn Missal points {measured['page_up_deg']}deg "
            f"but its compiled page-up vector projects to "
            f"{measured['expected_deg']}deg",
        )

    def test_gospel_side_missal_is_translated_and_not_mirrored(self):
        """The same book at negative X reads by the same rule, not a mirror."""
        measured = self.measure(self.contract(GOSPEL_SIDE), "missal")
        self.assertLess(
            measured["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
            f"{GOSPEL_SIDE}: the drawn Missal points "
            f"{measured['page_up_deg']}deg but its compiled page-up vector "
            f"projects to {measured['expected_deg']}deg",
        )

        epistle = self.item(self.contract(CANARY), "missal")
        gospel = self.item(self.contract(GOSPEL_SIDE), "missal")
        self.assertEqual(
            epistle["reading"]["page_up_yaw_deg"],
            gospel["reading"]["page_up_yaw_deg"],
            "the Missal reads at one yaw on both sides of the altar; a "
            "difference here is the mirrored book the invariant forbids",
        )
        # And the two really are on opposite sides, or the comparison is empty.
        self.assertGreater(epistle["position"][0], 0.0)
        self.assertLess(gospel["position"][0], 0.0)

    # -- 3: fidelity is non-vacuous --------------------------------------
    def test_fidelity_catches_a_mirrored_yaw(self):
        """Break the transform and the fidelity measurement must notice.

        45 degrees is the forbidden mirrored value: the book turned toward the
        priest's right instead of his left.
        """
        mutated = self.contract(CANARY)
        self.item(mutated, "missal")["yaw_deg"] = 45.0
        measured = self.measure(mutated, "missal")
        self.assertGreater(
            measured["fidelity_deg"], 10 * FIDELITY_TOLERANCE_DEG,
            "a mirrored Missal yaw left fidelity at "
            f"{measured['fidelity_deg']}deg; the fidelity check cannot "
            "distinguish a wrong-axis transform and guards nothing",
        )
        # The original is untouched: the mutation was on a deep copy.
        self.assertEqual(self.item(self.contract(CANARY), "missal")["yaw_deg"], 135.0)

    # -- 4: legibility, both sides ---------------------------------------
    def test_missal_stays_legible_on_both_sides(self):
        """The two projected principal axes stay clear of collinear."""
        for plate in (CANARY, GOSPEL_SIDE):
            with self.subTest(plate=plate):
                measured = self.measure(self.contract(plate), "missal")
                self.assertGreaterEqual(
                    measured["separation_deg"], self.floor,
                    f"{plate}: the Missal's axes project "
                    f"{measured['separation_deg']}deg from collinear, below "
                    f"the {self.floor}deg floor declared in "
                    f"{OBJECT_LIBRARY.name}",
                )

    # -- 5: legibility is non-vacuous, and reproduces the report ---------
    def test_the_reported_camera_is_faithful_and_unreadable(self):
        """The heart of the suite: right transform, unreadable picture.

        Drop the nave-centre eye back to where the defect was reported and the
        Missal's fidelity does not move at all — it is still drawn exactly
        where the contract points — while its axes collapse below the floor.
        That is precisely what was seen and what nothing before could measure.
        """
        raised = self.measure(self.contract(CANARY), "missal")

        lowered = self.contract(CANARY)
        lowered["panels"][0]["camera"]["position_xyz"] = list(REPORTED_CAMERA_XYZ)
        reported = self.measure(lowered, "missal")

        self.assertLess(
            reported["fidelity_deg"], EXACT_DEG,
            "lowering the camera changed fidelity to "
            f"{reported['fidelity_deg']}deg; the reported defect was a "
            "faithful transform, so this test no longer reproduces it",
        )
        self.assertLess(
            reported["separation_deg"], self.floor,
            f"at eye {REPORTED_CAMERA_XYZ} the Missal's axes separate by "
            f"{reported['separation_deg']}deg, at or above the "
            f"{self.floor}deg floor; the legibility check would not have "
            "caught the failure it was written for",
        )
        self.assertGreater(
            raised["separation_deg"], reported["separation_deg"],
            "raising the camera did not improve axis separation",
        )

        deeper = self.contract(CANARY)
        deeper["panels"][0]["camera"]["position_xyz"] = list(ORIGINAL_CAMERA_XYZ)
        original = self.measure(deeper, "missal")
        self.assertLess(
            original["fidelity_deg"], EXACT_DEG,
            f"eye {ORIGINAL_CAMERA_XYZ} disturbed fidelity "
            f"({original['fidelity_deg']}deg); it should only flatten the view",
        )
        self.assertLess(
            original["separation_deg"], reported["separation_deg"],
            f"eye {ORIGINAL_CAMERA_XYZ} separates the axes by "
            f"{original['separation_deg']}deg, no worse than the "
            f"{reported['separation_deg']}deg at {REPORTED_CAMERA_XYZ}; a "
            "lower eye must flatten the horizontal plane further",
        )
        self.assertLess(original["separation_deg"], self.floor)

    # -- 6: every oriented object, every art-ready scene ------------------
    def test_every_oriented_object_in_every_art_ready_scene(self):
        """The property holds across the corpus, not just at the canary."""
        worst_separation = (180.0, None)
        checked = 0
        scenes = 0
        for plate, contract in self.art_ready():
            if is_side_elevation(contract):
                continue
            scenes += 1
            for item in contract["objects"]:
                if item["id"] not in ORIENTED_OBJECTS:
                    continue
                measured = self.underlay.projected_orientation(
                    copy.deepcopy(contract), item["id"]
                )
                if measured is None:  # unplaced or unoriented in this scene
                    continue
                checked += 1
                self.assertLess(
                    measured["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
                    f"{plate}: the drawn {item['id']} points "
                    f"{measured['page_up_deg']}deg but its compiled "
                    f"orientation projects to {measured['expected_deg']}deg",
                )
                if measured["separation_deg"] < worst_separation[0]:
                    worst_separation = (
                        measured["separation_deg"], f"{plate}/{item['id']}"
                    )
        self.assertGreater(scenes, 100, "too few art-ready scenes measured")
        self.assertGreater(checked, 100, "too few oriented objects measured")
        self.assertGreaterEqual(
            worst_separation[0], self.floor,
            f"worst axis separation {worst_separation[0]}deg at "
            f"{worst_separation[1]}, below the {self.floor}deg floor "
            f"(measured {checked} oriented objects in {scenes} scenes)",
        )

    # -- 7: the exemption is earned, not assumed -------------------------
    def test_side_elevations_are_exempt_for_a_real_reason(self):
        """Fidelity holds where legibility cannot, which is why they are out.

        The exemption is pinned to a measured property. If a side elevation
        ever stopped collapsing the Missal's axes, or ever stopped drawing it
        faithfully, this test would say so rather than let the exemption
        quietly widen to cover scenes that simply failed.
        """
        exempt = [
            (plate, contract)
            for plate, contract in self.art_ready()
            if is_side_elevation(contract)
        ]
        self.assertEqual(
            len(exempt), 2,
            "expected exactly the two art-ready side elevations; found "
            + (", ".join(plate for plate, _ in exempt) or "none"),
        )
        for plate, contract in exempt:
            with self.subTest(plate=plate):
                measured = self.measure(copy.deepcopy(contract), "missal")
                self.assertLess(
                    measured["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
                    f"{plate}: a side elevation is exempt from legibility, "
                    "never from fidelity, and the drawn Missal points "
                    f"{measured['page_up_deg']}deg against an expected "
                    f"{measured['expected_deg']}deg",
                )
                self.assertLess(
                    measured["separation_deg"], self.floor,
                    f"{plate}: the Missal's axes separate by "
                    f"{measured['separation_deg']}deg, at or above the "
                    f"{self.floor}deg floor, so this scene is not in fact "
                    "collapsing depth and does not need the exemption",
                )

    # -- 8: the local frame is data ---------------------------------------
    def test_local_axes_are_declared_data(self):
        """The object frame is authored in YAML, not implied by the code."""
        contract_block = self.library.get("local_frame_contract")
        self.assertIsNotNone(
            contract_block,
            f"{OBJECT_LIBRARY.name} declares no local_frame_contract",
        )
        orientation_axis = contract_block.get("orientation_axis")
        self.assertIsNotNone(
            orientation_axis, "local_frame_contract declares no orientation_axis"
        )
        self.assertEqual(len(orientation_axis), 3)

        objects = self.library["objects"]
        for object_id in ORIENTED_OBJECTS:
            with self.subTest(object_id=object_id):
                frame = objects[object_id].get("local_frame")
                self.assertIsNotNone(
                    frame, f"{object_id} carries no local_frame"
                )
                page_up = frame.get("page_up_axis")
                self.assertIsNotNone(
                    page_up, f"{object_id} declares no page_up_axis"
                )
                self.assertEqual(len(page_up), 3)
                # The compiled yaw points the object's local orientation axis,
                # so page-up must lie along it or the yaw means something else.
                self.assertAlmostEqual(
                    abs(dot(page_up, orientation_axis)), 1.0,
                    delta=AXIS_TOLERANCE,
                    msg=f"{object_id}: page_up_axis {page_up} is not parallel "
                        f"to the declared orientation_axis {orientation_axis}",
                )

        missal = objects["missal"]["local_frame"]
        # An open book's spine runs from the reader's near edge to the far
        # edge, so it lies along page-up rather than across it.
        self.assertAlmostEqual(
            abs(dot(missal["spine_axis"], missal["page_up_axis"])), 1.0,
            delta=AXIS_TOLERANCE,
            msg=f"the Missal's spine_axis {missal['spine_axis']} is not "
                f"parallel to its page_up_axis {missal['page_up_axis']}",
        )
        for other in ("page_up_axis", "spine_axis"):
            self.assertAlmostEqual(
                dot(missal["spread_axis"], missal[other]), 0.0,
                delta=AXIS_TOLERANCE,
                msg=f"the Missal's spread_axis {missal['spread_axis']} is not "
                    f"perpendicular to its {other} {missal[other]}",
            )

    # -- 9: the validator enforces both -----------------------------------
    def test_validator_reports_the_oriented_object_check(self):
        """The layer's own acceptance run performs, and names, the check."""
        result = subprocess.run(
            [sys.executable, str(VALIDATE)],
            capture_output=True, text=True, cwd=ROOT,
        )
        self.assertEqual(
            result.returncode, 0,
            f"validate.py failed:\n{result.stdout}\n{result.stderr}",
        )
        output = result.stdout
        self.assertIn("oriented objects", output)
        self.assertIn("embody their compiled transform", output)
        self.assertIn("axis separation", output)
        self.assertIn("side-elevation scenes exempt", output)

    def test_validator_rejects_illegible_and_infidelitous_scenes(self):
        """Called directly on mutated copies, the check must actually raise.

        The repo is never touched: `check_projected_orientation` takes the
        contract list as an argument, so a deep copy is enough.
        """
        clean = self.contract(CANARY)
        checked, worst, exempt = self.validate.check_projected_orientation([clean])
        self.assertGreater(
            checked, 0, "the canary offered the validator nothing to measure"
        )
        self.assertGreaterEqual(worst, self.floor)
        self.assertEqual(exempt, 0)

        illegible = self.contract(CANARY)
        illegible["panels"][0]["camera"]["position_xyz"] = list(REPORTED_CAMERA_XYZ)
        with self.assertRaises(self.validate.Failure) as caught:
            self.validate.check_projected_orientation([illegible])
        self.assertIn("from collinear", str(caught.exception))

        mirrored = self.contract(CANARY)
        self.item(mirrored, "missal")["yaw_deg"] = 45.0
        with self.assertRaises(self.validate.Failure) as caught:
            self.validate.check_projected_orientation([mirrored])
        self.assertIn("does not embody the transform", str(caught.exception))

        # A side elevation is counted as exempt, never silently dropped.
        side = next(
            copy.deepcopy(contract)
            for _, contract in self.art_ready()
            if is_side_elevation(contract)
        )
        checked, _, exempt = self.validate.check_projected_orientation([side])
        self.assertEqual((checked, exempt), (0, 1))


if __name__ == "__main__":
    unittest.main()
