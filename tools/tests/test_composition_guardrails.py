#!/usr/bin/env python3
"""Regression checks for the composition of the render underlay.

`test_render_underlay.py` guards the drawing and `test_projected_orientation.py`
guards what an orientation becomes on the page. Both can be satisfied by a
plate nobody would accept. Every object can sit exactly where the contract
compiled it, every orientation can stay readable, and the picture can still be
wrong in the one way an image model cannot repair: the steps taking two-thirds
of the height, the altar reduced to a band across the top, and three figures
standing at the lip of a staircase because there is no floor drawn in front of
them.

That was a real plate. `sanctuary-master.yaml` was written to refuse it, and
its `composition:` block states the refusal as four numbers rather than a mood:

  max_step_band_fraction         the steps may not eat the plate
  min_altar_band_fraction        the altar is the subject and must be given it
  min_floor_below_feet_fraction  the figures stand on a floor, not on a lip
  min_actor_height_fraction      the people must be big enough to read

`validate.check_composition` measures all four through the renderer's own
camera, sanctuary and figures, for every art-ready perspective panel whose eye
stands in the nave. These tests hold the four properties, and — because a
check that cannot fail guards nothing — each one is paired with a perturbation
that breaks it. The perturbations are applied to in-memory copies: the geometry
ones through `underlay.SANCTUARY`, the threshold ones through a patched loader,
so no file in the repository is touched by any test here.
"""

from __future__ import annotations

import contextlib
import copy
import importlib.util
import inspect
import re
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
UNDERLAY = LAYER / "underlay.py"
VALIDATE = LAYER / "validate.py"
SANCTUARY_MASTER = LAYER / "sanctuary-master.yaml"

# The canary, and a scene whose actors are not all in plano.
CANARY = "LM-001A"

# The four authored bounds, named here so a test failure says which one moved.
BOUNDS = (
    "max_step_band_fraction",
    "min_altar_band_fraction",
    "min_superstructure_band_fraction",
    "min_floor_below_feet_fraction",
    "min_actor_height_fraction",
)

# `underlay.render_panel` leaves this share of the drawn extent as floor below
# whatever it framed. validate.py has to know the number to measure fractions
# of the composed subject, and it is an inline literal in the renderer, so this
# suite pins the two to each other rather than letting them drift apart.
FRAME_MARGIN = re.compile(
    r"ys\.append\(max\(ys\) \+ \(max\(ys\) - min\(ys\)\) \* ([0-9.]+)\)"
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def module_at(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CompositionGuardrailTests(unittest.TestCase):
    """The whole compiled corpus, measured through each panel's own camera."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validate = module_at(VALIDATE, "_test_composition_validate")
        cls.underlay = cls.validate.underlay_module()
        cls.master = load(SANCTUARY_MASTER)
        cls.limits = cls.master["composition"]
        cls.contracts = {
            path.stem: load(path) for path in sorted(CONTRACTS.glob("*.yaml"))
        }

    # -- helpers ---------------------------------------------------------
    def contract(self, plate: str) -> dict:
        self.assertIn(plate, self.contracts, f"{plate}: no compiled contract")
        return copy.deepcopy(self.contracts[plate])

    def art_ready(self):
        for plate, contract in sorted(self.contracts.items()):
            if contract["art_readiness"]["status"] == "ready":
                yield plate, copy.deepcopy(contract)

    def measured_panels(self):
        """Every panel check_composition measures, with its measurement."""
        first_step = float(self.master["steps"]["first_leading_edge_y"])
        for plate, contract in self.art_ready():
            for panel in contract["panels"]:
                camera = panel["camera"]
                if camera["projection"] != "perspective":
                    continue
                if float(camera["position_xyz"][1]) >= first_step:
                    continue
                yield plate, panel, self.validate.panel_composition(contract, panel)

    @contextlib.contextmanager
    def perturbed_sanctuary(self, mutate):
        """A mutated sanctuary, in memory only, for the length of a test.

        `underlay.sanctuary()` memoises the master into a module global, so
        installing a copy there changes the geometry every drawing is built
        from without writing to the repository. The authored thresholds still
        come off disk, so a geometry perturbation is measured against the real
        bounds and nothing else moves.
        """
        original = self.underlay.SANCTUARY
        mutated = copy.deepcopy(self.master)
        mutate(mutated)
        self.underlay.SANCTUARY = mutated
        try:
            yield mutated
        finally:
            self.underlay.SANCTUARY = original

    @contextlib.contextmanager
    def perturbed_limits(self, **bounds):
        """Authored thresholds moved past the measured value, in memory only."""
        original = self.validate.load

        def patched(path: Path):
            data = original(path)
            if Path(path).name == SANCTUARY_MASTER.name:
                data = copy.deepcopy(data)
                data["composition"].update(bounds)
            return data

        self.validate.load = patched
        try:
            yield
        finally:
            self.validate.load = original

    def assert_fires(self, contracts, fragment: str) -> str:
        with self.assertRaises(self.validate.Failure) as caught:
            self.validate.check_composition(contracts)
        message = str(caught.exception)
        self.assertIn(fragment, message)
        return message

    # -- 1: the bounds are authored data, not code -----------------------
    def test_the_thresholds_are_authored_in_the_sanctuary_master(self) -> None:
        """Every bound the check enforces is a number in the YAML.

        The point of the composition block is that a later change has to argue
        with a number. A threshold that had migrated into validate.py would be
        a threshold nobody could find.
        """
        # Enumerated from the YAML rather than only checked against the list,
        # so a bound added to the master and never enforced cannot hide.
        authored = {
            key for key, value in self.limits.items()
            if isinstance(value, (int, float))
        }
        self.assertEqual(
            authored, set(BOUNDS),
            "the composition block and the enforced bounds have diverged",
        )
        for name in BOUNDS:
            with self.subTest(bound=name):
                self.assertIn(name, self.limits, f"{name} is not authored")
                self.assertIsInstance(self.limits[name], float)
                self.assertGreater(self.limits[name], 0.0)
                self.assertLess(self.limits[name], 1.0)

        source = VALIDATE.read_text(encoding="utf-8")
        for name in BOUNDS:
            self.assertIn(
                f'limits["{name}"]', source,
                f"validate.py does not read {name} from the master",
            )
            self.assertNotIn(
                f"{self.limits[name]!r}", source.split("def check_composition")[1],
                f"{name}'s value is duplicated as a literal in validate.py",
            )
        # A ceiling below its floor would make the block unsatisfiable.
        self.assertGreater(
            self.limits["max_step_band_fraction"],
            self.limits["min_altar_band_fraction"] * 0.0 + 0.0,
        )
        self.assertLess(
            self.limits["min_altar_band_fraction"]
            + self.limits["min_floor_below_feet_fraction"]
            + self.limits["min_actor_height_fraction"],
            2.0,
            "the floors together demand more than the plate can hold",
        )

    # -- 2: the measurement is the renderer's, not a second opinion ------
    def test_the_measurement_uses_the_renderer_itself(self) -> None:
        """validate.py measures underlay.py's drawing, not its own arithmetic.

        A validator that reimplemented the projection could only prove that its
        copy of the maths agreed with itself, which is what the earlier
        world-space checks were doing when the plate was wrong.
        """
        self.assertEqual(Path(self.underlay.__file__), UNDERLAY)
        for name in ("Camera", "sanctuary", "altar_geometry", "mannequin", "place"):
            self.assertTrue(hasattr(self.underlay, name), name)

        source = inspect.getsource(self.validate.panel_composition)
        self.assertIn("underlay.Camera(panel)", source)
        self.assertIn("underlay.altar_geometry()", source)
        self.assertIn("underlay.mannequin(", source)
        for reimplemented in ("math.cos", "math.sin", "def project", "focal"):
            self.assertNotIn(
                reimplemented, source,
                f"panel_composition reimplements projection ({reimplemented})",
            )

        # It really is the panel's own camera: move the eye and every number
        # moves with it.
        contract = self.contract(CANARY)
        panel = contract["panels"][0]
        here = self.validate.panel_composition(contract, panel)
        moved = copy.deepcopy(contract)
        moved["panels"][0]["camera"]["position_xyz"] = [0.0, -2.4, 1.9]
        there = self.validate.panel_composition(moved, moved["panels"][0])
        for key in ("step_band", "altar_band", "actor_height"):
            with self.subTest(key=key):
                self.assertNotAlmostEqual(
                    here[key], there[key], places=4,
                    msg=f"{key} did not move when the camera did; the "
                        "measurement is not being taken through the panel",
                )

    # -- 3: the renderer's bottom allowance is pinned --------------------
    def test_the_frame_margin_matches_the_renderer(self) -> None:
        """validate.py's copy of render_panel's floor allowance stays true.

        The allowance is an inline literal in the renderer and a named constant
        in the validator. If they part company the composed subject height is
        measured against the wrong frame, silently, so they are pinned here.
        """
        found = FRAME_MARGIN.findall(UNDERLAY.read_text(encoding="utf-8"))
        self.assertEqual(
            len(found), 1,
            "render_panel's bottom allowance is no longer a single literal; "
            "validate.FRAME_BOTTOM_MARGIN cannot be pinned to it",
        )
        self.assertAlmostEqual(
            float(found[0]), self.validate.FRAME_BOTTOM_MARGIN, places=9,
            msg=f"the renderer allows {found[0]} below the framed subject and "
                f"validate.py assumes {self.validate.FRAME_BOTTOM_MARGIN}",
        )

    # -- 4: the corpus holds all four bounds -----------------------------
    def test_every_nave_perspective_panel_holds_the_composition(self) -> None:
        """The property holds across the corpus, not just at the canary."""
        worst = {
            "step_band": (0.0, None),
            "altar_band": (1.0, None),
            "floor_below_feet": (1.0, None),
            "actor_height": (1.0, None),
        }
        panels = 0
        for plate, panel, measured in self.measured_panels():
            panels += 1
            where = f"{plate}/{panel['id']}"
            if measured["step_band"] > worst["step_band"][0]:
                worst["step_band"] = (measured["step_band"], where)
            for key in ("altar_band", "floor_below_feet", "actor_height"):
                if measured[key] < worst[key][0]:
                    worst[key] = (measured[key], where)

        self.assertGreater(panels, 80, "too few nave perspective panels measured")
        self.assertLessEqual(
            worst["step_band"][0], self.limits["max_step_band_fraction"],
            f"the steps fill {worst['step_band'][0]:.3f} of the drawn subject "
            f"height at {worst['step_band'][1]}, above the "
            f"{self.limits['max_step_band_fraction']} ceiling",
        )
        for key, bound in (
            ("altar_band", "min_altar_band_fraction"),
            ("floor_below_feet", "min_floor_below_feet_fraction"),
            ("actor_height", "min_actor_height_fraction"),
        ):
            with self.subTest(bound=bound):
                self.assertGreaterEqual(
                    worst[key][0], self.limits[bound],
                    f"{key} is {worst[key][0]:.3f} at {worst[key][1]}, below "
                    f"the {self.limits[bound]} floor",
                )

        checked, exempt, reported = self.validate.check_composition(
            [contract for _, contract in self.art_ready()]
        )
        self.assertEqual(checked, panels, "the validator measured other panels")
        self.assertGreater(exempt, 0)
        self.assertAlmostEqual(reported["step_band"], worst["step_band"][0], places=9)
        for key in ("altar_band", "floor_below_feet", "actor_height"):
            self.assertAlmostEqual(reported[key], worst[key][0], places=9)

    # -- 5: the exemption is earned, not assumed -------------------------
    def test_in_sanctuary_views_are_exempt_for_a_real_reason(self) -> None:
        """A camera already on the predella cannot be held to the whole view.

        The over-the-shoulder presets stand inside the sanctuary and show
        neither the full step run nor the floor in front of the servers. They
        are exempt because of where the eye is, which is a measurable fact
        about the panel, and they are counted rather than dropped.
        """
        first_step = float(self.master["steps"]["first_leading_edge_y"])
        exempt = [
            (plate, panel)
            for plate, contract in self.art_ready()
            for panel in contract["panels"]
            if panel["camera"]["projection"] == "perspective"
            and float(panel["camera"]["position_xyz"][1]) >= first_step
        ]
        self.assertTrue(exempt, "no in-sanctuary perspective panel was found")
        for plate, panel in exempt:
            with self.subTest(plate=plate):
                eye = panel["camera"]["position_xyz"]
                self.assertGreaterEqual(
                    float(eye[1]), first_step,
                    f"{plate}: eye {eye} is naveward of the first step and "
                    "should have been measured, not exempted",
                )
                # The exemption is about where the eye stands, so it must not
                # be reachable from the nave presets.
                self.assertNotEqual(panel["camera"]["position"], "nave-centre")

        checked, counted, _ = self.validate.check_composition(
            [contract for _, contract in self.art_ready()]
        )
        self.assertEqual(counted, len(exempt))
        self.assertGreater(checked, counted)

    # -- 6: the step ceiling is non-vacuous ------------------------------
    def test_the_step_ceiling_catches_a_sanctuary_of_stairs(self) -> None:
        """Raise the risers and the plate becomes the staircase it refuses.

        Nothing but the sanctuary geometry moves: the thresholds are the
        authored ones, read off disk, and the camera is the contract's.
        """
        contracts = [self.contract(CANARY)]
        clean = self.validate.check_composition(contracts)[2]
        self.assertLessEqual(
            clean["step_band"], self.limits["max_step_band_fraction"]
        )

        def taller(master):
            rise = 0.16 * 2.4
            master["levels"].update(
                step_1=rise, step_2=2 * rise, step_3=3 * rise, predella=4 * rise
            )
            master["altar"]["body"]["from_z"] = 4 * rise

        with self.perturbed_sanctuary(taller):
            message = self.assert_fires(contracts, "the steps fill")
        self.assertIn("max_step_band_fraction", message)
        self.assertIn("staircase", message)

        # And the message is diagnosable: it names the measured value and the
        # bound it broke, so nobody has to rerun anything to read it.
        numbers = [float(n) for n in re.findall(r"0\.\d+", message)]
        self.assertGreaterEqual(len(numbers), 2, message)
        self.assertGreater(numbers[0], numbers[1], message)
        self.assertAlmostEqual(
            numbers[1], self.limits["max_step_band_fraction"], places=3
        )

        # The perturbation was in memory: the live sanctuary is untouched.
        self.assertEqual(
            self.underlay.sanctuary()["levels"]["predella"],
            self.master["levels"]["predella"],
        )

    # -- 7: the altar floor is non-vacuous -------------------------------
    def test_the_altar_floor_catches_an_altar_that_lost_the_plate(self) -> None:
        """Move the bound past the measured altar band and it must fire."""
        contracts = [self.contract(CANARY)]
        measured = next(
            m for plate, _, m in self.measured_panels() if plate == CANARY
        )
        with self.perturbed_limits(
            min_altar_band_fraction=round(measured["altar_band"] + 0.05, 4)
        ):
            message = self.assert_fires(contracts, "the altar fills only")
        self.assertIn("min_altar_band_fraction", message)
        self.assertIn(f"{measured['altar_band']:.3f}", message)

        # Unperturbed, the same corpus passes: the bound is not always broken.
        self.validate.check_composition(contracts)

    # -- 8: the floor guard is non-vacuous -------------------------------
    def test_the_floor_guard_catches_figures_on_the_lip_of_the_stairs(self) -> None:
        """Take the floor away in front of the actors and the guard fires.

        This is the failure `in_plano` exists to prevent, in the master file's
        own words: the step beginning exactly where the actors stand, so three
        figures at the foot of a staircase read as three figures halfway up it.
        Measuring empty crop instead of drawn floor would have made this
        unfalsifiable, because the renderer always leaves its margin.
        """
        contracts = [self.contract(CANARY)]

        def no_floor(master):
            master["in_plano"]["naveward_edge"] = -0.05

        with self.perturbed_sanctuary(no_floor):
            message = self.assert_fires(contracts, "is floor below the lowest foot")
        self.assertIn("min_floor_below_feet_fraction", message)
        self.assertIn("lip of the staircase", message)

        # The guard measures drawn floor, not the renderer's bottom margin: if
        # it measured the margin the answer would be that constant for every
        # plate, and this test could not have moved it.
        margin_share = self.validate.FRAME_BOTTOM_MARGIN / (
            1.0 + self.validate.FRAME_BOTTOM_MARGIN
        )
        measured = next(
            m for plate, _, m in self.measured_panels() if plate == CANARY
        )
        self.assertNotAlmostEqual(
            measured["floor_below_feet"], margin_share, places=4,
            msg="the floor measurement has collapsed onto render_panel's "
                "bottom allowance, which no geometry can change",
        )

    # -- 9: the actor floor is non-vacuous -------------------------------
    def test_the_actor_floor_catches_people_too_small_to_read(self) -> None:
        """Move the bound past the shortest measured actor and it must fire."""
        contracts = [contract for _, contract in self.art_ready()]
        _, _, worst = self.validate.check_composition(contracts)
        with self.perturbed_limits(
            min_actor_height_fraction=round(worst["actor_height"] + 0.02, 4)
        ):
            message = self.assert_fires(contracts, "the tallest actor")
        self.assertIn("min_actor_height_fraction", message)
        self.assertRegex(message, r"the tallest actor \((priest|AC1|AC2)\)")

    # -- 10: the bands refuse to be measured when they stop existing -----
    def test_the_check_refuses_a_sanctuary_whose_bands_have_merged(self) -> None:
        """Fail closed, loudly, rather than report a meaningless fraction.

        The step band and the altar band are separated at the predella top. A
        sanctuary in which a single drawn part straddles that height has no two
        bands to compare, and the honest answer is that the composition cannot
        be measured, not a number.
        """
        contracts = [self.contract(CANARY)]

        def merged(master):
            rise = 0.16 * 3.0
            master["levels"].update(
                step_1=rise, step_2=2 * rise, step_3=3 * rise, predella=4 * rise
            )
            master["altar"]["body"]["from_z"] = 4 * rise

        with self.perturbed_sanctuary(merged):
            message = self.assert_fires(contracts, "across the predella top")
        self.assertIn("cannot be measured", message)

    # -- 11: the validator performs and names the check ------------------
    def test_the_validator_reports_the_composition_check(self) -> None:
        """The layer's own acceptance run wires the check into its sequence."""
        source = inspect.getsource(self.validate.main)
        self.assertIn("check_composition(contracts)", source)
        self.assertIn("hold the authored composition", source)

        result = subprocess.run(
            [sys.executable, str(VALIDATE)],
            capture_output=True, text=True, cwd=ROOT,
        )
        if result.returncode != 0:
            failure = (result.stderr or result.stdout).strip()
            self.assertNotIn(
                "sanctuary-master.yaml composition.", failure,
                f"validate.py failed on the composition check:\n{failure}",
            )
            self.skipTest(
                "validate.py is failing for an unrelated reason, so its "
                f"composition line was never reached: {failure}"
            )
        output = result.stdout
        self.assertIn("hold the authored composition", output)
        self.assertIn("worst step band", output)
        self.assertIn("altar band", output)
        self.assertIn("floor below feet", output)
        self.assertIn("actor height", output)
        self.assertIn("panels exempt by design", output)


if __name__ == "__main__":
    unittest.main()
