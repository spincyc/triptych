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

# The historical nave-centre eyes, taken from camera-model.yaml's own history
# rather than invented: the view was authored at [0, -4.0, 1.6], raised to
# [0, -3.6, 2.35] when a flat Missal would not read, and raised again to
# [0, -3.6, 3.6]. The two below are the ones this file reproduces the report
# at, and they are now the values its body actually uses. The previous
# constants, [0, -4.2, 1.36] and [0, -4.2, 1.30], were never nave-centre
# positions at all, and the test that named them measured different numbers.
REPORTED_CAMERA_XYZ = [0.0, -3.6, 2.35]
ORIGINAL_CAMERA_XYZ = [0.0, -4.0, 1.6]

# A station on the publication camera's own centreline and distance, dropped
# to the sanctuary floor. This is what it now takes to make the PITCHED book
# illegible: at the publication eye it separates 29.73deg, and here 13.07,
# against a floor of 25. The historical eyes above cannot do it any more,
# because the book they were raised for was flat and this one is not.
GRAZING_CAMERA_XYZ = [0.0, -5.6, 0.40]

# A true side elevation collapses its view axis, and that is a measurable fact
# about the view rather than a label a panel awards itself. Measured in the
# two exempt scenes: a unit step along world X moves 16.32 page units where a
# unit step along Y or Z moves 249.7, a ratio of 0.0654. At the publication
# camera the same ratio is 0.998. The bound sits between them.
COLLAPSED_AXIS_RATIO = 0.10

# A dot product of unit vectors is exact arithmetic on authored 0s and 1s, but
# compare with a tolerance so the contract is "parallel", not "equal strings".
AXIS_TOLERANCE = 1e-6

# The object library may excuse an object from the legibility floor while it
# lies flat, on the ground that it has no orientation to communicate. That
# claim is measurable, and is measured here rather than believed: turn the
# object and see how much of its own drawn extent its projected bounding box
# moves. At 37 degrees of extra yaw the paten — the object that declares the
# exemption — shifts by 0.007 of its extent in the first scene that places it,
# while the Missal shifts by 0.086 there and 0.137 in the canary. 0.05 sits
# between them.
YAW_INVARIANCE_RATIO = 0.05
YAW_PROBE_DEG = 37.0


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

    def flat_exempt_ids(self) -> set:
        """Objects the library excuses the floor while they lie flat."""
        return {
            object_id
            for object_id, definition in self.library["objects"].items()
            if (definition.get("legibility") or {}).get("exempt_when_flat")
        }

    def first_scene_with(self, object_id: str):
        """The first art-ready perspective scene that places this object."""
        for plate, contract in self.art_ready():
            if is_side_elevation(contract):
                continue
            for item in contract["objects"]:
                if (
                    item["id"] == object_id
                    and item.get("position") is not None
                    and item.get("yaw_deg") is not None
                ):
                    return plate, copy.deepcopy(contract)
        raise AssertionError(
            f"no art-ready perspective scene places an oriented {object_id}"
        )

    def yaw_shift(self, contract: dict, object_id: str) -> float:
        """How far turning an object moves its drawn extent, relative to it.

        The projected bounding box of the object's own geometry, at its
        compiled yaw and at that yaw plus a probe angle. Divided by the box's
        own size, so the answer is about shape rather than about how large the
        object happens to be drawn.
        """
        camera = self.underlay.Camera(contract["panels"][0])
        engine = self.underlay.Underlay()
        item = self.item(contract, object_id)

        def box(yaw):
            turned = copy.deepcopy(item)
            turned["yaw_deg"] = yaw
            parts = engine.object_parts(turned)
            self.assertTrue(parts, f"{object_id} draws no geometry")
            points = [
                camera.project(point)[:2] for part in parts for point in part
            ]
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            return min(xs), max(xs), min(ys), max(ys)

        here = box(item["yaw_deg"])
        there = box(item["yaw_deg"] + YAW_PROBE_DEG)
        extent = (here[1] - here[0]) + (here[3] - here[2])
        self.assertGreater(
            extent, 0.0, f"the drawn {object_id} has no extent at all"
        )
        return max(abs(a - b) for a, b in zip(here, there)) / extent

    def collapsed_axis_ratio(self, contract: dict) -> float:
        """How much of the in-plane page scale the view axis still reaches.

        A side elevation looks across the sanctuary, so world X is the axis it
        collapses. Project a unit step along X and a unit step along each of
        the two axes that stay in the view plane, and take the ratio. Near
        zero is a collapsed axis; near one is a view that is not collapsing
        anything and has no business claiming the exemption.
        """
        camera = self.underlay.Camera(contract["panels"][0])
        origin = [0.0, 1.5, 1.55]

        def reach(step):
            here = camera.project(origin)
            there = camera.project(
                [origin[index] + step[index] for index in range(3)]
            )
            return math.hypot(there[0] - here[0], there[1] - here[1])

        in_plane = max(reach([0.0, 1.0, 0.0]), reach([0.0, 0.0, 1.0]))
        self.assertGreater(
            in_plane, 0.0, "the view plane has no scale at all"
        )
        return reach([1.0, 0.0, 0.0]) / in_plane

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

        # Reproduce the historical failure honestly. It needs BOTH halves of
        # it: the book modelled flat, as it then was, and the camera that was
        # later raised to compensate for that. With the Missal properly pitched
        # on its stand the same camera is perfectly readable, which is the
        # whole point of the lane that followed — so flattening the book is
        # what restores the conditions the legibility check was written for.
        lowered = self.contract(CANARY)
        lowered["panels"][0]["camera"]["position_xyz"] = list(
            REPORTED_CAMERA_XYZ
        )
        for item in lowered["objects"]:
            if item["id"] == "missal":
                item["reading"]["support_pitch_deg"] = 0.0
                item["reading"]["supported_by"] = None
                item["reading"]["page_up_vector_pitched"] = item["reading"][
                    "page_up_vector"
                ]
                item["state_after"] = "carried in the hand"
                item["placement_semantic"] = "in the priest's hand"
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
        deeper["panels"][0]["camera"]["position_xyz"] = list(
            ORIGINAL_CAMERA_XYZ
        )
        for item in deeper["objects"]:
            if item["id"] == "missal":
                item["reading"]["support_pitch_deg"] = 0.0
                item["reading"]["page_up_vector_pitched"] = item["reading"][
                    "page_up_vector"
                ]
                item["state_after"] = "carried in the hand"
                item["placement_semantic"] = "in the priest's hand"
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
        """The property holds across the corpus, not just at the canary.

        Fidelity is demanded of everything. Legibility is demanded of
        everything that has an orientation to show. An object may declare
        `legibility.exempt_when_flat` in the object library — the paten does,
        because a disc lying on the linen looks the same at every yaw — and
        that claim is not taken on trust: the exemption is counted, refused to
        the Missal, applied only while the object really is unpitched, and its
        premise is measured by turning the object and looking at what reaches
        the page. `test_the_flat_exemption_is_earned_and_narrow` is that
        measurement.
        """
        exempt_ids = self.flat_exempt_ids()
        worst_separation = (180.0, None)
        checked = 0
        scenes = 0
        flat_exempt = 0
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
                # The exemption never touches fidelity, and dies the moment
                # the object is pitched or picked up.
                if item["id"] in exempt_ids and measured["pitch_deg"] == 0.0:
                    flat_exempt += 1
                    continue
                if measured["separation_deg"] < worst_separation[0]:
                    worst_separation = (
                        measured["separation_deg"], f"{plate}/{item['id']}"
                    )
        self.assertGreater(scenes, 100, "too few art-ready scenes measured")
        self.assertGreater(checked, 100, "too few oriented objects measured")
        self.assertGreater(
            checked - flat_exempt, 100,
            f"only {checked - flat_exempt} of {checked} oriented objects were "
            f"held to the legibility floor; {flat_exempt} were excused as "
            "lying flat. An exemption that covers most of the corpus is not "
            "an exemption",
        )
        self.assertGreaterEqual(
            worst_separation[0], self.floor,
            f"worst axis separation {worst_separation[0]}deg at "
            f"{worst_separation[1]}, below the {self.floor}deg floor "
            f"(measured {checked} oriented objects in {scenes} scenes, "
            f"{flat_exempt} excused as lying flat)",
        )

    def test_the_flat_exemption_is_earned_and_narrow(self):
        """An object excused the floor must really look the same at any yaw.

        The exemption's own reason is a claim about the picture: "turn it on
        the corporal and nothing about it looks different". So turn it. If the
        drawing changes, the object does communicate an orientation and the
        floor is the check that says whether it communicates it legibly.

        Paired with the Missal, which fails the same measurement by an order
        of magnitude, so the probe cannot be passing everything.
        """
        exempt_ids = self.flat_exempt_ids()
        self.assertTrue(
            exempt_ids,
            "no object declares legibility.exempt_when_flat, so this test "
            "measures nothing; if the exemption has been withdrawn, the "
            "corpus check above should be holding every object to the floor",
        )
        self.assertNotIn(
            "missal", exempt_ids,
            "the Missal declares a flat-lying legibility exemption. A book "
            "that cannot show its reading orientation is this lane's defect, "
            "not an exception to it",
        )

        for object_id in sorted(exempt_ids):
            with self.subTest(object_id=object_id):
                declaration = self.library["objects"][object_id]["legibility"]
                self.assertTrue(
                    str(declaration.get("reason") or "").strip(),
                    f"{object_id} claims the exemption without a reason",
                )
                plate, contract = self.first_scene_with(object_id)
                shift = self.yaw_shift(contract, object_id)
                self.assertLess(
                    shift, YAW_INVARIANCE_RATIO,
                    f"{plate}: turning the {object_id} by {YAW_PROBE_DEG}deg "
                    f"moves its drawn extent by {shift:.4f} of itself. It "
                    "does show its orientation, so it is not entitled to be "
                    "excused from showing it legibly",
                )

        # The probe has teeth: the Missal moves far more than the bound.
        canary = self.contract(CANARY)
        missal_shift = self.yaw_shift(canary, "missal")
        self.assertGreater(
            missal_shift, YAW_INVARIANCE_RATIO,
            f"turning the Missal by {YAW_PROBE_DEG}deg moves its drawn extent "
            f"by only {missal_shift:.4f} of itself, inside the "
            f"{YAW_INVARIANCE_RATIO} bound. The probe would excuse the book "
            "as well, and it measures nothing",
        )

    # -- 7: the exemption is earned, not assumed -------------------------
    def test_side_elevations_are_exempt_for_a_real_reason(self):
        """Fidelity holds where legibility cannot, which is why they are out.

        The exemption is pinned to a measured property of the VIEW. It used to
        be pinned to the Missal instead — the book's axes had to collapse in
        an exempt scene — and that stopped being true when the book was
        pitched: it now separates 28.81deg in both side elevations, well above
        the floor, because pitch gives its page-up a vertical component that a
        horizontal projection cannot flatten. That is the pitch working, not
        the exemption failing, and reading it as a failure would have argued
        for taking the pitch away.

        What the exemption actually rests on is that the view collapses its
        own axis, so an object's horizontal orientation cannot be read there
        however well it is modelled. That is measured directly below. The
        widening the old test feared is guarded separately, by refusing to let
        a perspective panel claim the exemption at all: `validate.py` exempts
        on `collapses_equal_depth` OR a side-elevation projection, and the
        first of those is a flag any panel could set.
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
                primary = contract["panels"][0]["camera"]
                self.assertEqual(
                    primary["projection"], "orthographic-elevation-side",
                    f"{plate}: this scene is exempted from the legibility "
                    f"floor while drawing a {primary['projection']} panel. "
                    "The exemption belongs to a true side elevation; a "
                    "perspective panel carrying collapses_equal_depth would "
                    "be a failing scene excusing itself",
                )
                self.assertTrue(
                    primary.get("collapses_equal_depth"),
                    f"{plate}: a side elevation that does not declare "
                    "collapses_equal_depth is hiding what the view does",
                )

                # The exemption, earned: a unit step along the collapsed world
                # axis must reach the page as a small fraction of what the two
                # axes in the view plane reach.
                ratio = self.collapsed_axis_ratio(contract)
                self.assertLess(
                    ratio, COLLAPSED_AXIS_RATIO,
                    f"{plate}: a unit step along the view axis moves "
                    f"{ratio:.4f} of what a unit step in the view plane does. "
                    "This view is not collapsing depth, so nothing in it is "
                    "entitled to be excused from showing an orientation",
                )

                # Never exempt from fidelity, for any oriented object present.
                present = []
                for object_id in ORIENTED_OBJECTS:
                    item = self.underlay.projected_orientation(
                        copy.deepcopy(contract), object_id
                    )
                    if item is None:
                        continue
                    present.append((object_id, item))
                    self.assertLess(
                        item["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
                        f"{plate}: a side elevation is exempt from "
                        "legibility, never from fidelity, and the drawn "
                        f"{object_id} points {item['page_up_deg']}deg against "
                        f"an expected {item['expected_deg']}deg",
                    )
                self.assertTrue(
                    present,
                    f"{plate}: no oriented object is measurable here, so this "
                    "scene proves nothing about the exemption",
                )

                # And the record that replaces the old assertion: pitch does
                # real work even in the view that collapses depth. A
                # horizontal projection cannot flatten an axis with a vertical
                # component, so the Missal on its stand separates 26.44deg
                # here where the paten lying flat beside it separates 6.16.
                # The Missal's own margin over the 25deg floor is thin and
                # moves with the side camera, so what is asserted is the gap
                # between the inclined object and the flat one rather than the
                # absolute number.
                pitched = [
                    (name, item) for name, item in present
                    if item["pitch_deg"] > 0.0
                ]
                flat = [
                    (name, item) for name, item in present
                    if item["pitch_deg"] == 0.0
                ]
                self.assertTrue(
                    pitched and flat,
                    f"{plate}: this scene holds "
                    f"{sorted(name for name, _ in present)}, not both an "
                    "inclined and a flat oriented object, so the comparison "
                    "below measures nothing",
                )
                self.assertGreater(
                    min(item["separation_deg"] for _, item in pitched),
                    max(item["separation_deg"] for _, item in flat),
                    f"{plate}: the inclined objects "
                    f"{[(n, i['separation_deg']) for n, i in pitched]} read "
                    f"no better than the flat ones "
                    f"{[(n, i['separation_deg']) for n, i in flat]}. The "
                    "exemption is for a view that cannot show a horizontal "
                    "orientation; if pitch buys nothing here either, the "
                    "objects are back to being flat",
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
        # Every exemption is named and counted in the same line. A silent
        # exemption is how a floor stops being a floor.
        self.assertIn("side-elevation scenes", output)
        self.assertIn("flat unpitched objects", output)
        self.assertIn("exempt by design", output)

    def test_validator_rejects_illegible_and_infidelitous_scenes(self):
        """Called directly on mutated copies, the check must actually raise.

        The repo is never touched: `check_projected_orientation` takes the
        contract list as an argument, so a deep copy is enough.
        """
        clean = self.contract(CANARY)
        checked, worst, exempt, flat_exempt = (
            self.validate.check_projected_orientation([clean])
        )
        self.assertGreater(
            checked, 0, "the canary offered the validator nothing to measure"
        )
        self.assertGreaterEqual(worst, self.floor)
        self.assertEqual(exempt, 0)
        self.assertEqual(
            flat_exempt, 0,
            f"{flat_exempt} object(s) in {CANARY} took the flat-lying "
            "legibility exemption; the canary is the scene this whole file "
            "measures and nothing in it should be excused",
        )

        # Illegible. The historical eyes cannot produce this any more — the
        # book they were raised for was flat — so the check is made to bite
        # with a station at the sanctuary floor, where even the pitched book
        # collapses to 13.07deg.
        illegible = self.contract(CANARY)
        illegible["panels"][0]["camera"]["position_xyz"] = list(
            GRAZING_CAMERA_XYZ
        )
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
        checked, _, exempt, _flat = self.validate.check_projected_orientation(
            [side]
        )
        self.assertEqual((checked, exempt), (0, 1))


if __name__ == "__main__":
    unittest.main()
