#!/usr/bin/env python3
"""Regression checks for the pitched Missal, and for the camera it freed.

`test_projected_orientation.py` guards two properties of an oriented object:
fidelity (the drawn page-up agrees with the contract's own world page-up) and
legibility (the two projected principal axes stay clear of collinear). Both
held, and the Missal was still unreadable in the underlay.

The diagnosis that preceded this file was projective degeneracy, and the
remedy applied was to raise the nave camera — from eye 2.35 to 3.60 — until a
FLAT book's axes separated. That was solving the wrong problem. A real altar
Missal does not lie flat: it rests on an inclined stand and is pitched toward
the priest, and a book modelled flat can only ever be seen edge-on from the
nave. The principle this file exists to keep is therefore:

    do not move the camera to compensate for an inadequately modelled object.

So the stand became a real support carrying a declared `support.pitch_deg`,
the Missal declares `support.supported_by: missal-stand` and inherits that
pitch (except while it is carried), `place()` applies pitch about local +X
before yaw about Z, and the compiled contract publishes `support_pitch_deg`,
`supported_by`, `page_up_vector_pitched` and `page_normal_world`. The camera
went back to a publication height of eye 1.85 at 4.2 out, where the properly
pitched book is legible.

One real bug was fixed on the way. The fidelity measurement built its expected
direction from `[origin.x + v.x*r, origin.y + v.y*r, origin.z]` — it dropped
the vector's Z term, which was exactly zero while the book was flat and stops
being zero the moment pitch exists. It reported a spurious ~29 degree error.
`test_fidelity_z_regression` recomputes that old expression and pins how badly
it disagrees, so the dropped Z cannot come back unnoticed.

Every test here is written to fail if the property it guards breaks; the
negative cases (a grazing camera, a flattened page plane, the old Z-dropping
arithmetic) exist because a check that cannot fail guards nothing.
"""

from __future__ import annotations

import copy
import importlib.util
import math
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
CAMERA_MODEL = LAYER / "camera-model.yaml"
MISSAL_RULE = LAYER / "missal-orientation.yaml"
VALIDATE = LAYER / "validate.py"

# The Missal open on the Epistle side, at positive world X.
EPISTLE = "LM-001A"
# The same book at the Gospel corner, at negative world X, reading identically.
GOSPEL = "LM-033A"

# "Indistinguishable from exact", for claims that a quantity is untouched.
EXACT_DEG = 0.01
# The fidelity budget. Deliberately tighter than validate.py's 1.5deg: these
# two scenes measure 0.0, and this file should not follow the validator down
# if the validator ever loosens.
FIDELITY_TOLERANCE_DEG = 1.0

# A vector comparison tolerance. The contract stores its vectors rounded to six
# places and `world_axis` rounds to six places, so they agree exactly today;
# compare with a tolerance so the assertion is about geometry, not formatting.
VECTOR_TOLERANCE = 1e-6

# The floor under a Missal's projected page face, in square page pixels.
#
# Justification, not a magic number. `page_area_px` measures a fixed 0.40 x
# 0.30 local rectangle through the panel's own camera, so it is comparable
# between objects in one scene. At the publication camera the pitched Missal
# measures 1722 (Epistle) and 2121 (Gospel) square pixels, while the flat burse
# beside it — the object the failed canary confused it with — measures 447.
# 800 sits well clear of the flat case and less than half of the smallest
# measured pitched case, so it separates "a book presenting a face" from "a
# book seen as a sliver" without pinning either measurement.
PAGE_AREA_FLOOR_PX = 800.0

# A floor-level nave station, roughly a kneeler's eye. The pitched book is
# still drawn faithfully from here and its axes collapse below the legibility
# floor: pitch improves the model, it does not abolish a degenerate view.
GRAZING_CAMERA_XYZ = [0.0, -4.2, 0.40]
# Near mensa height. Recorded because it does NOT breach the floor any more —
# see test_a_grazing_camera_still_fails.
MENSA_HEIGHT_CAMERA_XYZ = [0.0, -4.2, 1.36]

# A publication viewpoint sits below this; a quasi-overhead one does not.
PUBLICATION_HEIGHT_CEILING_M = 2.5

# The claim in the camera note that this lane must not lose.
CAMERA_PRINCIPLE = "the camera was being moved to compensate for the object"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def module_at(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MissalPitchTests(unittest.TestCase):
    """The Missal is pitched on its stand, and the drawing knows it."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.underlay = module_at(LAYER / "underlay.py", "_test_pitch_underlay")
        cls.validate = module_at(VALIDATE, "_test_pitch_validate")
        cls.library = load(OBJECT_LIBRARY)
        cls.objects = cls.library["objects"]
        cls.camera_model = load(CAMERA_MODEL)
        cls.missal_rule = load(MISSAL_RULE)
        cls.floor = float(
            cls.library["local_frame_contract"]["legibility"][
                "minimum_axis_separation_deg"
            ]
        )
        # The stand's declared inclination, read from the file rather than
        # written down here: this suite must follow the authored value.
        cls.stand_pitch = float(
            cls.objects["missal-stand"]["support"]["pitch_deg"]
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

    def measure(self, contract: dict, object_id: str = "missal") -> dict:
        measured = self.underlay.projected_orientation(contract, object_id)
        self.assertIsNotNone(
            measured,
            f"{contract['plate_id']}/{object_id}: nothing measurable; the "
            "object is absent, unplaced or unoriented",
        )
        return measured

    def assertVectorEqual(self, got, want, msg: str) -> None:
        self.assertEqual(len(got), len(want), msg)
        for index, (a, b) in enumerate(zip(got, want)):
            self.assertAlmostEqual(
                a, b, delta=VECTOR_TOLERANCE,
                msg=f"{msg} (component {index}: {got} vs {want})",
            )

    def art_ready_perspective(self):
        """Art-ready scenes the legibility floor actually applies to."""
        for plate, contract in sorted(self.contracts.items()):
            if contract["art_readiness"]["status"] != "ready":
                continue
            primary = contract["panels"][0]["camera"]
            if primary.get("collapses_equal_depth") or primary[
                "projection"
            ].endswith("elevation-side"):
                continue
            yield plate, contract

    # -- 1: the Missal is pitched ----------------------------------------
    def test_missal_is_pitched_on_both_sides(self):
        """The drawn Missal carries the stand's declared inclination.

        The number is read from `underlay-objects.yaml`, so changing the
        stand's pitch changes what this test demands. What it will not accept
        is no pitch at all: a flat book is the state the whole lane exists to
        undo.
        """
        self.assertGreater(
            self.stand_pitch, 0.0,
            f"{OBJECT_LIBRARY.name}: the missal-stand declares a pitch of "
            f"{self.stand_pitch}deg. A stand with no inclination is not a "
            "stand, and the Missal it carries is back to lying flat",
        )
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                measured = self.measure(self.contract(plate))
                self.assertAlmostEqual(
                    measured["pitch_deg"], self.stand_pitch, places=4,
                    msg=f"{plate}: the Missal is drawn at "
                        f"{measured['pitch_deg']}deg of pitch but its stand "
                        f"declares {self.stand_pitch}deg",
                )
                self.assertGreater(measured["pitch_deg"], 0.0)

    # -- 2: the page normal is not vertical ------------------------------
    def test_page_normal_is_not_vertical_and_matches_the_contract(self):
        """A book on its stand faces the priest, not the ceiling.

        Two claims, and the second is what keeps the pipeline honest: the
        renderer's derived normal and the compiled contract's published
        `reading.page_normal_world` must be the same vector, or the picture
        and the contract are describing different books.
        """
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                measured = self.measure(self.contract(plate))
                normal = measured["world_page_normal"]

                horizontal = math.hypot(normal[0], normal[1])
                self.assertGreater(
                    horizontal, 0.15,
                    f"{plate}: the Missal's world page normal {normal} has a "
                    f"horizontal component of only {horizontal:.4f}. That is "
                    "a page plane left effectively horizontal",
                )
                self.assertNotEqual(
                    [round(c, 6) for c in normal], [0.0, 0.0, 1.0],
                    f"{plate}: the world page normal is exactly world-Z; the "
                    "support pitch never reached the transform",
                )
                length = math.sqrt(sum(c * c for c in normal))
                self.assertAlmostEqual(
                    length, 1.0, delta=VECTOR_TOLERANCE,
                    msg=f"{plate}: the page normal {normal} is not a unit "
                        f"vector (length {length})",
                )

                declared = self.item(self.contract(plate), "missal")["reading"][
                    "page_normal_world"
                ]
                self.assertVectorEqual(
                    normal, declared,
                    f"{plate}: the renderer derives page normal {normal} "
                    f"while the contract publishes {declared}; the drawing "
                    "and the contract disagree about the page plane",
                )

    def test_every_placed_missal_agrees_with_its_contract_normal(self):
        """The same agreement, across the whole art-ready corpus.

        `validate.py` derives the page normal from the object library and
        never reads the contract's own `page_normal_world`, so a compiled
        contract could publish a normal the drawing does not have and the
        acceptance run would not notice. This is the check that would.
        """
        checked = 0
        for plate, contract in self.art_ready_perspective():
            item = next(
                (o for o in contract["objects"] if o["id"] == "missal"), None
            )
            if item is None or item.get("position") is None:
                continue
            reading = item.get("reading") or {}
            if not reading.get("supported_by"):
                continue
            measured = self.measure(copy.deepcopy(contract))
            checked += 1
            with self.subTest(plate=plate):
                self.assertVectorEqual(
                    measured["world_page_normal"],
                    reading["page_normal_world"],
                    f"{plate}: drawn page normal "
                    f"{measured['world_page_normal']} against compiled "
                    f"{reading['page_normal_world']}",
                )
                self.assertVectorEqual(
                    measured["world_page_up"],
                    reading["page_up_vector_pitched"],
                    f"{plate}: drawn pitched page-up "
                    f"{measured['world_page_up']} against compiled "
                    f"{reading['page_up_vector_pitched']}",
                )
        self.assertGreater(
            checked, 100,
            f"only {checked} stand-supported Missal placements measured; the "
            "corpus-wide guard is not covering the corpus",
        )

    # -- 3: the pitch belongs to the stand -------------------------------
    def test_pitch_is_inherited_from_the_stand_not_declared_by_the_book(self):
        """The hierarchy is real, so book and stand cannot drift apart.

        Declaring the same angle twice is how two numbers become two different
        numbers. The book names its support; the support owns the angle.
        """
        engine = self.underlay.Underlay()
        self.assertAlmostEqual(
            engine.support_pitch("missal", "open"),
            engine.support_pitch("missal-stand"),
            places=6,
            msg="the Missal's resolved pitch differs from its stand's",
        )

        support = self.objects["missal"]["support"]
        self.assertEqual(
            support.get("supported_by"), "missal-stand",
            "the Missal must name the stand it rests on; without the "
            "reference the inheritance below is a coincidence",
        )
        self.assertNotIn(
            "pitch_deg", support,
            "the Missal declares its own pitch_deg. Two authored copies of "
            "one physical angle is exactly the drift this structure removes",
        )

        # Move the stand and the book must follow. Patched in memory on a deep
        # copy of the loaded library: the file on disk is never touched.
        moved = self.underlay.Underlay()
        moved.library = copy.deepcopy(moved.library)
        altered = self.stand_pitch + 11.0
        moved.library["missal-stand"]["support"]["pitch_deg"] = altered
        self.assertAlmostEqual(
            moved.support_pitch("missal", "open"), altered, places=6,
            msg="the stand's pitch changed and the Missal's did not; the "
                "book is not really inheriting anything",
        )
        # And the untouched engine is unchanged, so the patch was local.
        self.assertAlmostEqual(
            engine.support_pitch("missal", "open"), self.stand_pitch, places=6
        )
        self.assertAlmostEqual(
            float(load(OBJECT_LIBRARY)["objects"]["missal-stand"]["support"][
                "pitch_deg"
            ]),
            self.stand_pitch, places=6,
            msg=f"{OBJECT_LIBRARY.name} was modified on disk by a test",
        )

    # -- 4: a carried book is on nobody's stand --------------------------
    def test_a_carried_missal_is_not_pitched(self):
        """A book in someone's hands is not on a stand."""
        engine = self.underlay.Underlay()
        self.assertEqual(
            engine.support_pitch("missal", "carried"), 0.0,
            "a carried Missal resolved a support pitch; it is being held, "
            "not stood on anything",
        )

        carried = [
            (plate, contract)
            for plate, contract in sorted(self.contracts.items())
            for o in contract["objects"]
            if o["id"] == "missal"
            and "hand" in str(o.get("placement_semantic") or "").lower()
        ]
        self.assertTrue(
            carried,
            "no corpus scene places the Missal in anyone's hands, so this "
            "test measures nothing",
        )
        self.assertIn(
            "LM-032B", [plate for plate, _ in carried],
            "LM-032B is the crossing with the Missal carried between sides; "
            "if it no longer reads that way this test has lost its subject",
        )
        for plate, contract in carried:
            with self.subTest(plate=plate):
                reading = self.item(contract, "missal")["reading"]
                self.assertEqual(
                    reading["support_pitch_deg"], 0.0,
                    f"{plate}: a Missal held in the hands compiles a support "
                    f"pitch of {reading['support_pitch_deg']}deg",
                )
                self.assertIsNone(
                    reading["supported_by"],
                    f"{plate}: a carried Missal names "
                    f"{reading['supported_by']!r} as its support",
                )

    # -- 5: placement changes, orientation and pitch do not --------------
    def test_epistle_and_gospel_differ_only_in_placement(self):
        """One book, one reading orientation, one pitch, two positions.

        INV-MISSAL-01 as geometry: the side of the altar is a translation and
        nothing else. Everything about how the book sits is identical; only
        where it sits differs, and the X components have opposite signs.
        """
        epistle = self.item(self.contract(EPISTLE), "missal")
        gospel = self.item(self.contract(GOSPEL), "missal")

        self.assertEqual(
            epistle["yaw_deg"], gospel["yaw_deg"],
            "the Missal reads at one yaw on both sides; a difference here is "
            "the mirrored book INV-MISSAL-01 forbids",
        )
        self.assertEqual(
            epistle["reading"]["support_pitch_deg"],
            gospel["reading"]["support_pitch_deg"],
            "the same stand tilts the book by different amounts on the two "
            "sides of the same altar",
        )
        self.assertVectorEqual(
            epistle["reading"]["page_normal_world"],
            gospel["reading"]["page_normal_world"],
            "the page normal differs between the Epistle and Gospel sides",
        )
        self.assertVectorEqual(
            epistle["reading"]["page_up_vector_pitched"],
            gospel["reading"]["page_up_vector_pitched"],
            "the pitched page-up vector differs between the two sides",
        )

        self.assertNotEqual(
            epistle["position"], gospel["position"],
            "the two placements are the same point; there is nothing to "
            "compare",
        )
        self.assertGreater(
            epistle["position"][0], 0.0,
            "the Epistle-side Missal must sit at positive world X",
        )
        self.assertLess(
            gospel["position"][0], 0.0,
            "the Gospel-side Missal must sit at negative world X",
        )

        # The measured drawing agrees: same world axes, same pitch.
        measured = {
            plate: self.measure(self.contract(plate))
            for plate in (EPISTLE, GOSPEL)
        }
        self.assertVectorEqual(
            measured[EPISTLE]["world_page_normal"],
            measured[GOSPEL]["world_page_normal"],
            "the drawn page normal differs between the two sides",
        )
        self.assertVectorEqual(
            measured[EPISTLE]["world_page_up"],
            measured[GOSPEL]["world_page_up"],
            "the drawn pitched page-up differs between the two sides",
        )
        self.assertEqual(
            measured[EPISTLE]["pitch_deg"], measured[GOSPEL]["pitch_deg"]
        )

        # Same object, same variant: an open book both times. The two variants
        # carry different part counts, so this pins the variant without
        # re-deriving the renderer's own selection rule.
        engine = self.underlay.Underlay()
        variants = self.objects["missal"]["variants"]
        parts = {
            plate: engine.object_parts(
                self.item(self.contract(plate), "missal")
            )
            for plate in (EPISTLE, GOSPEL)
        }
        self.assertEqual(
            len(parts[EPISTLE]), len(parts[GOSPEL]),
            "the same book is drawn with different numbers of parts on the "
            "two sides of the altar",
        )
        self.assertEqual(
            len(parts[EPISTLE]), len(variants["open"]["parts"]),
            "the Missal is not being drawn as the open-book variant",
        )
        self.assertNotEqual(
            len(variants["open"]["parts"]), len(variants["closed"]["parts"]),
            "the open and closed variants have the same part count, so the "
            "assertion above no longer identifies which one was used",
        )

    # -- 6: fidelity survives the pitch ----------------------------------
    def test_fidelity_holds_with_pitch_applied(self):
        """The drawn page-up matches the contract's PITCHED vector.

        Comparing against the flat `page_up_vector` would report a fault that
        is really the pitch doing its job; comparing against
        `page_up_vector_pitched` is the honest question, and it must agree.
        """
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                measured = self.measure(self.contract(plate))
                self.assertLess(
                    measured["fidelity_deg"], FIDELITY_TOLERANCE_DEG,
                    f"{plate}: the drawn Missal points "
                    f"{measured['page_up_deg']}deg while its compiled pitched "
                    f"page-up projects to {measured['expected_deg']}deg",
                )

    # -- 7: the dropped-Z regression -------------------------------------
    def test_fidelity_z_regression(self):
        """The old expected direction dropped the vector's Z term.

        `projected_orientation` used to build its expected point as

            [origin.x + v.x*reach, origin.y + v.y*reach, origin.z]

        which is the vector's shadow on the horizontal plane through the
        object's origin, not the vector. While the book was flat, v.z was 0
        and the two coincided. The moment pitch existed the shadow diverged,
        and the measurement reported a fault in a drawing that was correct.

        This test recomputes the old expression and pins how far wrong it is.
        If the dropped Z ever returns, the correct path still agrees here and
        the recorded gap explains why the difference is not noise.
        """
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                contract = self.contract(plate)
                measured = self.measure(contract)
                item = self.item(contract, "missal")
                origin = item["position"]
                world = item["reading"]["page_up_vector_pitched"]
                self.assertNotAlmostEqual(
                    world[2], 0.0, delta=1e-3,
                    msg=f"{plate}: the pitched page-up vector {world} has no "
                        "Z component, so dropping Z would be harmless and "
                        "this regression tests nothing",
                )

                camera = self.underlay.Camera(contract["panels"][0])
                reach = 0.18  # projected_orientation's own probe length
                here = camera.project(origin)
                # The defect, verbatim: origin[2] instead of the Z term.
                there = camera.project([
                    origin[0] + world[0] * reach,
                    origin[1] + world[1] * reach,
                    origin[2],
                ])
                stale = math.degrees(
                    math.atan2(-(there[1] - here[1]), there[0] - here[0])
                )
                stale_error = abs(
                    (measured["page_up_deg"] - stale + 180.0) % 360.0 - 180.0
                )

                self.assertGreater(
                    stale_error, 10.0,
                    f"{plate}: the Z-dropping expression disagrees with the "
                    f"drawn axis by only {stale_error:.4f}deg. It used to "
                    "report a large spurious error; if it no longer can, this "
                    "regression no longer guards the fix",
                )
                self.assertLess(
                    measured["fidelity_deg"], EXACT_DEG,
                    f"{plate}: the corrected computation disagrees with the "
                    f"drawing by {measured['fidelity_deg']}deg; it should be "
                    "indistinguishable from exact",
                )

    # -- 8: readability at the publication camera ------------------------
    def test_readable_at_the_publication_camera(self):
        """Eye 1.85 at 4.2 out, and the pitched book reads from there.

        This is the claim that let the camera come back down. If it fails, the
        temptation to raise the camera again returns, and the answer is still
        to model the object, not to move the viewpoint.
        """
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                contract = self.contract(plate)
                self.assertEqual(
                    contract["panels"][0]["camera"]["position"], "nave-centre",
                    f"{plate}: the primary panel is not at the publication "
                    "camera, so this measurement is about some other view",
                )
                measured = self.measure(contract)
                self.assertGreaterEqual(
                    measured["separation_deg"], self.floor,
                    f"{plate}: the Missal's axes project "
                    f"{measured['separation_deg']}deg from collinear, below "
                    f"the {self.floor}deg floor declared in "
                    f"{OBJECT_LIBRARY.name}",
                )
                self.assertGreater(
                    measured["page_area_px"], 0.0,
                    f"{plate}: the Missal projects no page area at all",
                )
                self.assertGreater(
                    measured["page_area_px"], PAGE_AREA_FLOOR_PX,
                    f"{plate}: the Missal presents only "
                    f"{measured['page_area_px']} square page pixels, at or "
                    f"below the {PAGE_AREA_FLOOR_PX} floor. A book seen as a "
                    "sliver is the failure this lane fixed",
                )

    # -- 9: legibility is still refusable --------------------------------
    def test_a_grazing_camera_still_fails(self):
        """Pitch improves the model; it does not abolish a degenerate view.

        From a floor-level nave station the pitched book is drawn exactly
        where the contract points and still cannot be read: its axes collapse
        below the floor. The gate must keep biting, or "the camera is fine
        now" becomes an argument that no camera can ever be wrong.

        Recorded alongside: a station at mensa height no longer breaches the
        floor. Before the pitch a level view was fatal; that headroom is what
        the pitch bought, and it is asserted here so that losing it is a test
        failure rather than a quiet regression.
        """
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                grazing = self.contract(plate)
                grazing["panels"][0]["camera"]["position_xyz"] = list(
                    GRAZING_CAMERA_XYZ
                )
                measured = self.measure(grazing)
                self.assertLess(
                    measured["separation_deg"], self.floor,
                    f"{plate}: at eye {GRAZING_CAMERA_XYZ} the Missal's axes "
                    f"still separate by {measured['separation_deg']}deg, at "
                    f"or above the {self.floor}deg floor; the legibility gate "
                    "would not catch a degenerate view",
                )
                self.assertLess(
                    measured["fidelity_deg"], EXACT_DEG,
                    f"{plate}: lowering the camera moved fidelity to "
                    f"{measured['fidelity_deg']}deg. A degenerate view is a "
                    "faithful transform in an unreadable picture, so this no "
                    "longer reproduces the failure it is written for",
                )

                # The headroom the pitch bought.
                level = self.contract(plate)
                level["panels"][0]["camera"]["position_xyz"] = list(
                    MENSA_HEIGHT_CAMERA_XYZ
                )
                at_mensa = self.measure(level)
                self.assertGreaterEqual(
                    at_mensa["separation_deg"], self.floor,
                    f"{plate}: at eye {MENSA_HEIGHT_CAMERA_XYZ}, essentially "
                    f"mensa height, the pitched Missal separates by only "
                    f"{at_mensa['separation_deg']}deg. A book on an inclined "
                    "stand should survive a level view; a flat one could not",
                )

                # And the publication camera is better than either.
                published = self.measure(self.contract(plate))
                self.assertGreater(
                    published["separation_deg"], measured["separation_deg"],
                    f"{plate}: the publication camera reads the Missal no "
                    "better than a floor-level station",
                )

    # -- 10: the camera says what it means -------------------------------
    def test_camera_semantics_are_documented_and_stable(self):
        """The nave camera declares what it is, and why it did not move.

        The fields below are this lane's record. A bare `position` invites the
        next reader to nudge it; a declared height, distance, focal length,
        projection hint and semantic make it a stated viewpoint that has to be
        argued with.
        """
        positions = {
            entry["id"]: entry
            for entry in self.camera_model["camera_positions"]
        }
        self.assertIn(
            "nave-centre", positions,
            f"{CAMERA_MODEL.name} declares no nave-centre camera",
        )
        nave = positions["nave-centre"]

        for field in (
            "position",
            "height_m_equivalent",
            "distance_from_altar",
            "focal_length_px",
            "projection_hint",
            "semantic",
            "note",
        ):
            self.assertIn(
                field, nave,
                f"nave-centre no longer declares {field!r}; the camera is "
                "back to being a bare triple of numbers",
            )

        self.assertEqual(
            nave["semantic"], "publication-nave-front",
            f"nave-centre declares semantic {nave['semantic']!r}; it is a "
            "publication viewpoint, not a literal eye and not an engineering "
            "overhead",
        )
        self.assertEqual(len(nave["position"]), 3)
        self.assertAlmostEqual(
            nave["position"][2], float(nave["height_m_equivalent"]), places=6,
            msg=f"nave-centre sits at z={nave['position'][2]} while declaring "
                f"a height of {nave['height_m_equivalent']}",
        )
        self.assertLess(
            float(nave["height_m_equivalent"]), PUBLICATION_HEIGHT_CEILING_M,
            f"nave-centre stands at {nave['height_m_equivalent']}m. Above "
            f"{PUBLICATION_HEIGHT_CEILING_M}m it is a quasi-overhead view, "
            "which is what raising the camera to 2.35 and 3.60 produced",
        )
        self.assertIn(
            CAMERA_PRINCIPLE, nave["note"],
            "the nave-centre note no longer records that the camera was "
            "being moved to compensate for the object. That sentence is the "
            "whole reason the height came back down",
        )

        # The compiled contracts actually stand where the model says.
        for plate in (EPISTLE, GOSPEL):
            with self.subTest(plate=plate):
                camera = self.contract(plate)["panels"][0]["camera"]
                self.assertEqual(camera["position"], "nave-centre")
                self.assertVectorEqual(
                    camera["position_xyz"], nave["position"],
                    f"{plate}: compiled to eye {camera['position_xyz']} while "
                    f"{CAMERA_MODEL.name} declares {nave['position']}",
                )

    # -- 11: the validator enforces the pitch ----------------------------
    def test_validator_enforces_the_page_plane(self):
        """`check_projected_orientation` rejects a Missal left horizontal.

        Deep copies only: the check takes its contract list as an argument, so
        nothing on disk is touched.
        """
        clean = [self.contract(EPISTLE), self.contract(GOSPEL)]
        checked, worst, exempt = self.validate.check_projected_orientation(clean)
        self.assertGreater(
            checked, 0, "the validator was given nothing to measure"
        )
        self.assertGreaterEqual(worst, self.floor)
        self.assertEqual(exempt, 0)

        # A Missal whose page plane is drawn horizontal while its contract
        # still declares stand support. This is the physical fault the lane
        # added the check for.
        flattened = self.contract(EPISTLE)
        flat_item = self.item(flattened, "missal")
        flat_item["state_after"] = "Open, carried flat in the hands."
        flat_item["reading"]["page_normal_world"] = [0.0, 0.0, 1.0]
        with self.assertRaises(self.validate.Failure) as caught:
            self.validate.check_projected_orientation([flattened])
        message = str(caught.exception).lower()
        self.assertTrue(
            "page plane" in message or "page normal" in message,
            f"the validator refused the flattened Missal without naming the "
            f"page plane or the normal: {caught.exception}",
        )

        # A recorded gap, pinned so it cannot widen unnoticed. The validator
        # derives the normal from the object library and reads only
        # `reading.support_pitch_deg` to decide whether the book is carried,
        # so a contract that publishes a vertical `page_normal_world` and a
        # zero pitch for a stand-supported book is treated as carried and
        # passes. `test_every_placed_missal_agrees_with_its_contract_normal`
        # is what catches that today. Written to accept either outcome: if the
        # validator is taught to read the published normal, this still passes.
        lying = self.contract(EPISTLE)
        lying_item = self.item(lying, "missal")
        lying_item["reading"]["page_normal_world"] = [0.0, 0.0, 1.0]
        lying_item["reading"]["support_pitch_deg"] = 0.0
        try:
            self.validate.check_projected_orientation([lying])
        except self.validate.Failure:
            pass  # the gap has been closed; nothing further to say
        else:
            measured = self.measure(self.contract(EPISTLE))
            self.assertNotEqual(
                [round(c, 6) for c in measured["world_page_normal"]],
                [0.0, 0.0, 1.0],
                "the validator accepted a Missal declaring a vertical page "
                "normal AND the drawing now agrees with it; the page plane "
                "really has been left horizontal",
            )

        # Nothing above disturbed the real contracts.
        self.assertNotEqual(
            self.item(self.contract(EPISTLE), "missal")["reading"][
                "page_normal_world"
            ],
            [0.0, 0.0, 1.0],
        )

    # -- 12: composition sanity ------------------------------------------
    def test_composition_reads_from_projected_geometry(self):
        """The plate composes, measured in projected geometry, not pixels.

        Deliberately coarse. Absolute pixel positions move whenever the panel
        fit changes and would make this a tripwire rather than a check; these
        are relations that must hold however the frame is fitted.
        """
        contract = self.contract(EPISTLE)
        camera = self.underlay.Camera(contract["panels"][0])
        geometry = self.underlay.altar_geometry()

        # The first altar step is the first `step()` call: a riser and a
        # tread. Its topmost projected point is the top of that step; page Y
        # grows downward, so "below" is a larger Y.
        first_step = geometry[0] + geometry[1]
        step_top_y = min(camera.project(p)[1] for p in first_step)

        depths = set()
        for actor in contract["actors"]:
            with self.subTest(actor=actor["id"]):
                parts = self.underlay.mannequin(
                    actor, actor["id"] == "priest"
                )
                lowest_y = max(
                    camera.project(p)[1] for part in parts for p in part
                )
                self.assertGreater(
                    lowest_y, step_top_y,
                    f"{actor['id']}'s lowest drawn point projects to y="
                    f"{lowest_y:.2f}, at or above the first step's top at "
                    f"y={step_top_y:.2f}; the figure is floating on the steps "
                    "rather than standing before them",
                )
            depths.add(actor["position"][1])
        self.assertEqual(
            len(contract["actors"]), 3,
            "this scene is the priest and two acolytes at the foot",
        )
        self.assertEqual(
            len(depths), 1,
            f"the three actors stand at depths {sorted(depths)}; at the foot "
            "of the altar they share one line",
        )

        # A pitched open book presents more face than a flat closed case, and
        # `page_area_px` measures the same local rectangle for both, so the
        # comparison is about inclination rather than about size.
        missal = self.measure(self.contract(EPISTLE), "missal")
        burse = self.measure(self.contract(EPISTLE), "burse")
        self.assertEqual(
            burse["pitch_deg"], 0.0,
            "the burse has acquired a pitch; it is a flat case on the mensa",
        )
        self.assertGreater(
            missal["page_area_px"], burse["page_area_px"],
            f"the Missal projects {missal['page_area_px']} square pixels of "
            f"face against the flat burse's {burse['page_area_px']}. The open "
            "book on its stand must present more, or the canary's confusion "
            "between the two is back",
        )


if __name__ == "__main__":
    unittest.main()
