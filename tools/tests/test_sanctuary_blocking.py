#!/usr/bin/env python3
"""Regression checks for the sanctuary, the blocking, and the composition.

`test_render_underlay.py` guards what the picture contains. This file guards
what it looks like, which is a different question and the one that kept getting
missed.

The failure these tests come from: the canary underlay drew three coarse
figures in front of a large staircase with a thin slab at the top, and every
automated check in the layer passed while it did. The steps took 69 per cent of
the drawn height and the altar 20; the first step's leading edge sat at depth
0, exactly where the actors stood, so they had no floor in front of them at
all; and the figures met the ground only through the fall of their vesture.

Underneath it was an arithmetic problem, not a drawing problem. The approved
structural geometry spaces its sanctuary levels 0.25 apart, which is an
ordering device rather than a measurement. Taken as measurements those numbers
put the platform at 61 per cent of a standing actor and left 0.35 between the
predella and the mensa, and no camera can satisfy both. The layer now resolves
the ordinals to physical geometry, and these tests hold that resolution, the
blocking that rests on it, and the guards that measure the result.
"""

from __future__ import annotations

import importlib.util
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
STRUCTURAL = DICTIONARY / "structural/low-mass/v0.21"
LAYER = DICTIONARY / "render-contract/low-mass/v1"
MASTER = LAYER / "sanctuary-master.yaml"
CONTRACTS = LAYER / "contracts"

CANARY = "LM-001A"
# A scene on three levels at once: the priest at the predella, one server on
# step 3 and one on step 1. Single-level scenes cannot catch a depth mapping
# that puts an actor on the wrong tread.
THREE_LEVELS = "LM-035A"


def module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    sys.modules[name] = loaded
    spec.loader.exec_module(loaded)
    return loaded


def load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class SanctuaryMasterTests(unittest.TestCase):
    """The sanctuary is defined once, and defined as geometry."""

    @classmethod
    def setUpClass(cls):
        cls.master = load(MASTER)
        cls.geometry = load(STRUCTURAL / "scenes/geometry.yaml")

    def test_the_structural_levels_are_left_alone(self):
        """The resolution must not have edited the approved geometry."""
        levels = {row["id"]: row["z"] for row in self.geometry["levels"]}
        self.assertEqual(
            levels,
            {
                "plano": 0.0,
                "step-1": 0.25,
                "step-2": 0.50,
                "step-3": 0.75,
                "predella": 1.00,
            },
            "the structural level ordinals have changed; they are sealed",
        )
        self.assertEqual(self.geometry["mensa_positions"]["z"], 1.35)

    def test_every_structural_level_is_resolved(self):
        """A level nobody mapped would silently keep its ordinal."""
        mapped = {row["level"] for row in self.master["level_elevations"]["map"]}
        structural = {row["id"] for row in self.geometry["levels"]} | {"mensa"}
        self.assertEqual(mapped, structural)

    def test_the_resolution_preserves_order(self):
        """Monotonic, or the corpus's depth and height orderings break."""
        for key in ("level_elevations", "level_depths"):
            rows = self.master[key]["map"]
            source = [row.get("structural_z", row.get("structural_y")) for row in rows]
            resolved = [row.get("elevation", row.get("depth")) for row in rows]
            self.assertEqual(source, sorted(source), f"{key} source out of order")
            self.assertEqual(
                resolved, sorted(resolved), f"{key} is not monotonic"
            )

    def test_the_altar_is_taller_than_it_is_deep_in_steps(self):
        """The proportion the whole exercise was about.

        The platform must be a base for the altar rather than the subject of
        the plate. Read as measurements the sealed ordinals gave a platform at
        61 per cent of an actor; a real one is nearer 39.
        """
        levels = self.master["levels"]
        actor_height = 1.65  # the standing envelope in underlay.py
        platform = levels["predella"] / actor_height
        self.assertLess(
            platform, 0.48, f"the platform is {platform:.2f} of an actor's height"
        )
        table = levels["mensa"] - levels["predella"]
        self.assertGreater(
            table / actor_height,
            0.45,
            "a priest cannot work at an altar this low above his own predella",
        )

    def test_a_tread_is_deeper_than_its_riser(self):
        """Altar steps, not a ziggurat."""
        levels = self.master["levels"]
        riser = levels["step_1"] - levels["floor"]
        self.assertGreater(self.master["steps"]["tread_depth"], riser)

    def test_the_first_step_stands_clear_of_the_actors(self):
        """The original failure, as a number.

        The step began at depth 0, exactly where the actors stand, so three
        figures at the lip of a staircase read as three figures halfway up it.
        """
        plano = self.master["in_plano"]
        self.assertGreaterEqual(
            self.master["steps"]["first_leading_edge_y"],
            plano["minimum_margin_before_first_step"],
        )

    def test_the_altar_carries_a_superstructure(self):
        """What makes the modelled mass read as an altar rather than a table."""
        altar = self.master["altar"]
        mensa = self.master["levels"]["mensa"]
        for part in ("gradine", "tabernacle", "reredos_hint"):
            self.assertGreaterEqual(altar[part]["from_z"], mensa - 1e-9)
        self.assertGreater(altar["reredos_hint"]["to_z"] - mensa, 1.0)
        anchors = self.master["fixed_anchors"]
        self.assertGreater(anchors["altar_cross"][2], mensa)
        self.assertEqual(len(anchors["candlesticks"]), 4)

    def test_the_mensa_carries_the_corporal(self):
        """The bound that fixes how far the altar may retreat.

        The corporal's nave fold is authored at depth 1.38. If the altar face
        goes back past the mensa's reach, the linen hangs in mid-air.
        """
        altar = self.master["altar"]
        nave_edge = (
            altar["body"]["front_y"]
            + altar["body"]["depth"] / 2
            - altar["mensa"]["depth"] / 2
        )
        fold = load(LAYER / "frame-vocabulary.yaml")["mensa_depth"]["positions"]
        self.assertLessEqual(
            nave_edge, fold["corporal-front-centre"]["y"] - 1e-9
        )


class ResolvedContractTests(unittest.TestCase):
    """The resolution reaches the compiled contracts, not just the drawing."""

    @classmethod
    def setUpClass(cls):
        cls.master = load(MASTER)
        cls.canary = load(CONTRACTS / f"{CANARY}.yaml")
        cls.stacked = load(CONTRACTS / f"{THREE_LEVELS}.yaml")

    def test_actors_stand_at_resolved_elevations(self):
        elevations = set(
            row["elevation"] for row in self.master["level_elevations"]["map"]
        )
        for actor in self.stacked["actors"]:
            self.assertIn(
                actor["position"][2],
                elevations,
                f"{actor['id']} stands at an unresolved elevation",
            )

    def test_objects_on_the_mensa_use_the_resolved_mensa(self):
        mensa = self.master["levels"]["mensa"]
        resting = [
            item
            for item in self.canary["objects"]
            if item.get("position") and item["id"] in ("corporal", "burse")
        ]
        self.assertTrue(resting, "no mensa objects to check")
        for item in resting:
            self.assertAlmostEqual(item["position"][2], mensa, places=6)

    def test_the_three_levels_stay_ordered(self):
        """A monotonic mapping must not have reordered anybody."""
        by_id = {actor["id"]: actor["position"] for actor in self.stacked["actors"]}
        self.assertGreater(by_id["priest"][2], by_id["AC1"][2])
        self.assertGreater(by_id["AC1"][2], by_id["AC2"][2])
        self.assertGreater(by_id["priest"][1], by_id["AC1"][1])
        self.assertGreater(by_id["AC1"][1], by_id["AC2"][1])


class BlockingTests(unittest.TestCase):
    """Figures that read as people, and meet the floor."""

    @classmethod
    def setUpClass(cls):
        cls.underlay = module(LAYER / "underlay.py", "_blocking_underlay")
        cls.canary = load(CONTRACTS / f"{CANARY}.yaml")

    def actor(self, contract, actor_id):
        return next(a for a in contract["actors"] if a["id"] == actor_id)

    def test_a_figure_in_profile_still_has_width(self):
        """The spike.

        Drawn as one flat outline, an actor facing along the view axis
        collapsed to a vertical line. A server turned gospelward rendered as a
        spike and nothing complained.
        """
        actor = dict(self.actor(self.canary, "AC1"))
        widths = []
        for yaw in (90.0, 180.0):
            actor["body_facing_yaw_deg"] = yaw
            parts = self.underlay.mannequin(actor, False)
            points = [point for part in parts for point in part]
            widths.append(
                (
                    max(p[0] for p in points) - min(p[0] for p in points),
                    max(p[1] for p in points) - min(p[1] for p in points),
                )
            )
        for across, deep in widths:
            self.assertGreater(min(across, deep), 0.10,
                               "the envelope has no depth in one axis")

    def test_the_priest_is_distinguishable_from_a_server(self):
        priest = self.underlay.mannequin(self.actor(self.canary, "priest"), True)
        server = self.underlay.mannequin(self.actor(self.canary, "AC1"), False)
        self.assertGreater(len(priest), len(server),
                           "the priest carries no chasuble the servers lack")

    def test_every_posture_puts_a_flat_patch_on_its_level(self):
        """Standing, kneeling and genuflecting all have to rest on something."""
        actor = dict(self.actor(self.canary, "AC1"))
        for posture in ("standing", "kneeling", "genuflecting"):
            actor["posture"] = posture
            contact = self.underlay.foot_contacts(actor, False)
            self.assertTrue(
                contact["soles"],
                f"a {posture} figure meets the floor through nothing",
            )
            for sole in contact["soles"]:
                self.assertAlmostEqual(sole["z"], actor["position"][2], places=6)

    def test_the_canary_actors_stand_in_plano_clear_of_the_first_step(self):
        master = self.underlay.sanctuary()
        first_step = master["steps"]["first_leading_edge_y"]
        feet = 0
        for actor in self.canary["actors"]:
            contact = self.underlay.foot_contacts(
                actor, actor["id"] == "priest"
            )
            self.assertEqual(contact["stands_on"], "floor")
            for sole in contact["soles"]:
                feet += 1
                self.assertLess(
                    sole["y_max"],
                    first_step,
                    f"{actor['id']} has a foot on the first step",
                )
        self.assertEqual(feet, 6, "three actors did not produce six feet")


class NearPlaneTests(unittest.TestCase):
    """A close camera must clip, not fling geometry across the plate."""

    @classmethod
    def setUpClass(cls):
        cls.underlay = module(LAYER / "underlay.py", "_nearplane_underlay")
        # The priest bowing low over the altar, shot from inside the sanctuary.
        cls.close = load(CONTRACTS / "LM-016B.yaml")
        cls.nave = load(CONTRACTS / f"{CANARY}.yaml")

    def culled(self, contract):
        """(parts drawn, parts rejected as too near) for a panel."""
        camera = self.underlay.Camera(contract["panels"][0])
        engine = self.underlay.Underlay()
        parts = list(self.underlay.altar_geometry())
        for actor in contract["actors"]:
            parts += self.underlay.mannequin(actor, actor["id"] == "priest")
        for item in contract["objects"]:
            parts += engine.object_parts(item) or []
        drawn = rejected = 0
        for part in parts:
            nearest = min(camera.project(point)[2] for point in part)
            if nearest < camera.near:
                rejected += 1
            else:
                drawn += 1
        return drawn, rejected

    def test_a_close_panel_actually_culls_what_is_in_the_eye(self):
        """Measuring the drawing cannot see this, which is why it was missed.

        The panel is fitted, so geometry flung off the plate never appears as a
        large coordinate: the fit simply rescales until the absurd point is
        inside, and everything real collapses. The check has to be on what the
        camera rejects, not on what the numbers look like afterwards.
        """
        drawn, rejected = self.culled(self.close)
        self.assertGreater(
            rejected, 0, "the in-sanctuary panel culls nothing; the near plane "
            "is inert exactly where it is needed"
        )
        self.assertGreater(drawn, rejected, "the close panel culls most of itself")

    def test_the_near_plane_only_bites_on_perspective(self):
        camera = self.underlay.Camera(self.nave["panels"][0])
        self.assertGreater(camera.near, 0.0)
        for panel in self.nave["panels"]:
            if panel["camera"]["projection"].startswith("orthographic"):
                self.assertLess(self.underlay.Camera(panel).near, 0.0)

    def test_the_nave_view_loses_nothing_to_the_near_plane(self):
        """From the nave nothing is ever that close; the cull must be inert."""
        engine = self.underlay.Underlay()
        camera = self.underlay.Camera(self.nave["panels"][0])
        nearest = min(
            camera.project(point)[2]
            for part in self.underlay.altar_geometry()
            for point in part
        )
        self.assertGreater(
            nearest,
            camera.near,
            "the publication camera is clipping its own sanctuary",
        )


class CompositionTests(unittest.TestCase):
    """The measured plate, and proof the guards are not decorative."""

    @classmethod
    def setUpClass(cls):
        cls.validate = module(LAYER / "validate.py", "_blocking_validate")
        cls.master = load(MASTER)
        cls.canary = load(CONTRACTS / f"{CANARY}.yaml")

    def measured(self):
        return self.validate.panel_composition(
            self.canary, self.canary["panels"][0]
        )

    def test_the_canary_holds_every_authored_threshold(self):
        limits = self.master["composition"]
        measured = self.measured()
        self.assertLess(measured["step_band"], limits["max_step_band_fraction"])
        self.assertGreater(
            measured["altar_band"], limits["min_altar_band_fraction"]
        )
        self.assertGreater(
            measured["superstructure_band"],
            limits["min_superstructure_band_fraction"],
        )
        self.assertGreater(
            measured["floor_below_feet"], limits["min_floor_below_feet_fraction"]
        )
        self.assertGreater(
            measured["actor_height"], limits["min_actor_height_fraction"]
        )

    def test_the_staircase_plate_would_be_refused(self):
        """The picture that started this, as a number the guard rejects.

        The failing plate measured 0.69 of its height in steps against a 0.46
        ceiling, and 0.20 in altar against a 0.22 floor. Both are refused.
        """
        limits = self.master["composition"]
        self.assertGreater(0.69, limits["max_step_band_fraction"])
        self.assertLess(0.20, limits["min_altar_band_fraction"])

    def test_the_superstructure_guard_sits_where_it_bites(self):
        """A threshold below every reachable value is reassurance, not a check.

        Once the elevations are resolved the altar body is tall by
        construction, so the altar band alone passes even when everything above
        the mensa has been flattened onto it. The superstructure bound has to
        sit between what the sanctuary builds and what that flattening gives.
        """
        limits = self.master["composition"]
        built = self.measured()["superstructure_band"]
        flattened = 0.218  # measured with gradine, tabernacle and reredos on the mensa
        self.assertGreater(
            built, limits["min_superstructure_band_fraction"],
            "the built altar does not clear its own floor",
        )
        self.assertLess(
            flattened, limits["min_superstructure_band_fraction"],
            "a flattened altar would pass; the guard cannot fire",
        )


class VisualReviewGateTests(unittest.TestCase):
    """The gate that a machine cannot pass on anyone's behalf."""

    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(ROOT / "scripts"))
        cls.pictographic = module(
            ROOT / "scripts" / "_pictographic.py", "_blocking_pictographic"
        )
        cls.review = load(MASTER)["underlay_visual_review"]

    def test_the_review_names_the_canary_and_is_recorded(self):
        self.assertEqual(self.review["canary"], CANARY)
        self.assertEqual(self.review["status"], "approved")
        self.assertNotEqual(self.review["reviewed_geometry_digest"], "PENDING")

    def test_the_regression_scenes_exist_and_cover_the_hard_cases(self):
        """The canary alone cannot show a level change or a profile figure."""
        scenes = self.review["regression_scenes"]["scenes"]
        ids = [scene["id"] for scene in scenes]
        self.assertIn(CANARY, ids)
        self.assertIn(THREE_LEVELS, ids)
        levels = set()
        postures = set()
        for scene_id in ids:
            contract = load(CONTRACTS / f"{scene_id}.yaml")
            for actor in contract["actors"]:
                levels.add(actor["position"][2])
                postures.add(actor["posture"])
        self.assertGreaterEqual(
            len(levels), 4, "the set never leaves two sanctuary levels"
        )
        self.assertIn("kneeling", postures, "no kneeling figure is covered")
        self.assertIn("standing", postures)

    def test_the_digest_covers_everything_that_decides_the_picture(self):
        inputs = set(self.review["digest_inputs"])
        self.assertEqual(
            inputs,
            {
                "sanctuary-master.yaml",
                "camera-model.yaml",
                "underlay.py",
                "underlay-objects.yaml",
                "_contract.py",
            },
            "the digest does not cover everything that decides the picture: "
            "the sanctuary, the camera, the renderer, the object library and "
            "the compiler that places the actors",
        )

    def test_the_recorded_digest_matches_the_current_composition(self):
        current, _ = self.pictographic.composition_digest(LAYER)
        self.assertEqual(current, self.review["reviewed_geometry_digest"])

    def test_a_moved_composition_makes_art_seed_refuse(self):
        """Fail-closed, demonstrated rather than asserted.

        An approval must not outlive the picture it was given for. This edits
        the sanctuary in a scratch copy of the layer, so the repository is
        never left in the perturbed state.
        """
        import shutil
        import tempfile

        with tempfile.TemporaryDirectory() as scratch:
            copy = Path(scratch) / "v1"
            shutil.copytree(LAYER, copy)
            master = copy / "sanctuary-master.yaml"
            master.write_text(
                master.read_text(encoding="utf-8").replace(
                    "  tread_depth: 0.30", "  tread_depth: 0.31", 1
                ),
                encoding="utf-8",
            )
            moved, _ = self.pictographic.composition_digest(copy)
            self.assertNotEqual(
                moved,
                self.review["reviewed_geometry_digest"],
                "changing the sanctuary did not invalidate the review",
            )
            with self.assertRaises(self.pictographic.SeedRefused):
                self.pictographic.require_visual_review(copy, CANARY)


class LayerBatteryTests(unittest.TestCase):
    """The layer's own validator, run whole."""

    def test_the_validation_battery_passes(self):
        result = subprocess.run(
            [sys.executable, str(LAYER / "validate.py")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for expected in (
            "soles rest on the level their actor stands on",
            "hold the authored composition",
        ):
            self.assertIn(expected, result.stdout)

    def test_the_calibration_sheet_is_current_and_is_not_a_panel(self):
        result = subprocess.run(
            [sys.executable, str(LAYER / "camera-calibration.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        panels = load(LAYER / f"contracts/{CANARY}.yaml")["panels"]
        self.assertNotIn(
            "camera-calibration",
            {panel["id"] for panel in panels},
            "the debug sheet has become a declared panel",
        )


if __name__ == "__main__":
    unittest.main()
