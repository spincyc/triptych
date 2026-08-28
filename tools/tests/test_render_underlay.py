#!/usr/bin/env python3
"""Regression checks for the render underlay.

`test_render_contract.py` guards the room and `test_artistic_entry.py` guards
the door. This file guards the picture the artistic agent actually looks at.

The second canary failure was diagnostic: the compiled contract and the
deterministic skeleton were both correct, and the image model still drew the
Missal on the wrong side. The skeleton draws every object as the same small
square and lets a text label carry the meaning, so Missal, burse, chalice and
corporal were four identical squares and the actors were labelled circles. The
model had to decide which square was the open book, and it decided wrongly.

The underlay removes that hop: a projected line drawing in which the geometry
carries the meaning and there is no text at all. These tests assert the
properties that failure demands — no text, an object you can name from its
silhouette alone, a Missal that lands on the side the contract compiled and
does not mirror when it changes sides, actors with bodies, and a package that
ships the drawing as the mandatory edit source.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import itertools
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ElementTree
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "tools" / "pictographic"
DICTIONARY = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/mass-pictographic-dictionary"
)
LAYER = DICTIONARY / "render-contract/low-mass/v1"
CONTRACTS = LAYER / "contracts"
OBJECT_LIBRARY = LAYER / "underlay-objects.yaml"

CALENDAR = "roman-1962"
FORM = "low-mass"
# The canary: the Missal open on the Epistle side, at positive world X.
CANARY = "LM-001A"
# The same book at the Gospel corner, at negative world X, reading identically.
GOSPEL_SIDE = "LM-033A"

UNDERLAY_FILES = ("render-underlay.png", "render-underlay.svg")
SEED_FILES = UNDERLAY_FILES + (
    "render-contract.yaml",
    "skeleton.svg",
    "provenance.yaml",
    "ART-AGENT-INSTRUCTIONS.md",
    "WEB-AGENT-PROMPT.md",
    "PACKAGE-MANIFEST.yaml",
)

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
# A plate-sized line drawing; anything near-empty is not a conditioning image.
MIN_RASTER_BYTES = 20_000

COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
ELEMENT = re.compile(r"<([a-zA-Z][\w:-]*)")
PANEL_GROUP = re.compile(r'<g transform="translate\(-?\d+,-?\d+\)">')
# The six objects the failed canary confused with one another, plus the two the
# skeleton drew at the same size as the book.
DISTINCT_OBJECTS = ("missal", "burse", "chalice", "corporal", "paten", "pall")

RSVG = shutil.which("rsvg-convert")
NO_RSVG = "rsvg-convert is not installed; the underlay raster cannot be checked"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def module_at(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        capture_output=True, text=True, cwd=ROOT,
    )


def blocked_scenes() -> list[str]:
    """Every blocked scene the tooling lists, discovered rather than named."""
    result = run("readiness", CALENDAR, FORM, "--blocked")
    if result.returncode != 0:
        raise AssertionError(f"readiness failed: {result.stderr}")
    scenes = []
    for line in result.stdout.splitlines():
        if not line.startswith("  "):
            continue
        scene = line.strip().partition("  ")[0]
        if re.fullmatch(r"LM-[0-9]+[A-Z]?", scene):
            scenes.append(scene)
    return scenes


class RenderUnderlayTests(unittest.TestCase):
    """The canary underlay, rendered once, is the subject of several tests."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.underlay = module_at(LAYER / "underlay.py", "_test_render_underlay")
        cls.engine = cls.underlay.Underlay()
        cls.contracts = {
            plate: load(CONTRACTS / f"{plate}.yaml")
            for plate in (CANARY, GOSPEL_SIDE)
        }
        cls.library = load(OBJECT_LIBRARY)["objects"]
        cls.svg = cls.engine.render(cls.contracts[CANARY])

    # -- helpers ---------------------------------------------------------
    def contract(self, plate: str) -> dict:
        return self.contracts[plate]

    def item(self, plate: str, object_id: str) -> dict:
        return next(
            o for o in self.contract(plate)["objects"] if o["id"] == object_id
        )

    def actor(self, plate: str, actor_id: str) -> dict:
        return next(
            a for a in self.contract(plate)["actors"] if a["id"] == actor_id
        )

    def camera(self, plate: str):
        return self.underlay.Camera(self.contract(plate)["panels"][0])

    def projected_points(self, plate: str, parts) -> list[tuple[float, float]]:
        camera = self.camera(plate)
        return [(camera.project(p)[0], camera.project(p)[1])
                for part in parts for p in part]

    def object_points(self, plate: str, object_id: str):
        parts = self.engine.object_parts(self.item(plate, object_id))
        self.assertTrue(parts, f"{plate}/{object_id}: no underlay geometry")
        return self.projected_points(plate, parts)

    def mean_x(self, plate: str, object_id: str) -> float:
        xs = [x for x, _ in self.object_points(plate, object_id)]
        return sum(xs) / len(xs)

    def panel_centre_x(self, plate: str) -> float:
        """Page centre in projected coordinates, derived from the whole scene.

        `render_panel` fits everything it draws into the panel with equal
        margins, so the midpoint of the drawn extent is the centre of the
        finished page, and the fit is a positive scale plus a translation that
        cannot reorder anything.
        """
        contract = self.contract(plate)
        points = self.projected_points(plate, self.underlay.altar_geometry())
        for item in contract["objects"]:
            parts = self.engine.object_parts(item)
            if parts:
                points += self.projected_points(plate, parts)
        for actor in contract["actors"]:
            points += self.projected_points(
                plate, self.underlay.mannequin(actor, actor["id"] == "priest")
            )
        xs = [x for x, _ in points]
        return (min(xs) + max(xs)) / 2

    def library_variant(self, object_id: str) -> dict:
        variants = self.library[object_id]["variants"]
        for key in ("default", "open"):
            if key in variants:
                return variants[key]
        return next(iter(variants.values()))

    @staticmethod
    def variant_points(variant: dict) -> set:
        return {tuple(p) for part in variant["parts"] for p in part["points"]}

    @staticmethod
    def part_signature(parts) -> list[int]:
        return [len(part) for part in parts]

    @staticmethod
    def z_span(parts) -> float:
        zs = [p[2] for part in parts for p in part]
        return max(zs) - min(zs)

    # -- the canary renders ----------------------------------------------
    @unittest.skipUnless(RSVG, NO_RSVG)
    def test_the_canary_underlay_renders_one_panel_and_a_real_raster(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            out = Path(workspace)
            result = run("underlay", CALENDAR, FORM, CANARY, "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)

            svg_path = out / CANARY / "render-underlay.svg"
            png_path = out / CANARY / "render-underlay.png"
            self.assertTrue(svg_path.is_file(), result.stdout)
            self.assertTrue(png_path.is_file(), result.stdout)

            svg = svg_path.read_text(encoding="utf-8")
            ElementTree.fromstring(svg)
            self.assertEqual(len(self.contract(CANARY)["panels"]), 1)
            self.assertEqual(len(PANEL_GROUP.findall(svg)), 1)

            raster = png_path.read_bytes()
            self.assertTrue(raster.startswith(PNG_MAGIC), raster[:16])
            self.assertGreater(len(raster), MIN_RASTER_BYTES)

    # -- the property that forced the failure ----------------------------
    def test_the_conditioning_raster_carries_no_text_at_all(self) -> None:
        for plate in (CANARY, GOSPEL_SIDE):
            svg = self.engine.render(self.contract(plate))
            body = COMMENT.sub("", svg)
            self.assertNotIn("<text", body, plate)
            self.assertNotIn("<tspan", body, plate)
            self.assertNotIn("<text", svg, plate)
            self.assertNotIn("<tspan", svg, plate)
            self.assertNotIn("font", body, plate)

            # Scene identity is carried, but only as a comment: the plate id
            # must not survive into anything an image model could read.
            comments = COMMENT.findall(svg)
            self.assertTrue(comments, plate)
            self.assertIn(plate, " ".join(comments))
            self.assertNotIn(plate, body, plate)
            # ElementTree drops comments, so a parsed tree proves the same
            # thing structurally: no element carries the identity.
            tree = ElementTree.fromstring(svg)
            for element in tree.iter():
                self.assertIsInstance(element.tag, str)
                self.assertNotIn(plate, "".join(element.itertext()), plate)

    # -- the exact confusion that failed ---------------------------------
    def test_the_canary_missal_draws_on_the_epistle_half_of_the_page(self) -> None:
        missal = self.item(CANARY, "missal")
        burse = self.item(CANARY, "burse")
        self.assertEqual(missal["placement_semantic"], "mensa-epistle")
        self.assertGreater(missal["position"][0], 0, "the canary Missal is epistleward")
        self.assertLess(burse["position"][0], 0, "the burse is gospelward")

        centre = self.panel_centre_x(CANARY)
        missal_x = self.mean_x(CANARY, "missal")
        burse_x = self.mean_x(CANARY, "burse")

        self.assertGreater(
            missal_x, centre,
            "the Missal must be drawn on the page-right half of the panel",
        )
        self.assertGreater(
            missal_x, burse_x,
            "the Missal must be drawn epistleward of the burse",
        )
        self.assertLess(burse_x, centre)
        # Not a coincidence of rounding: the two are a plate apart.
        self.assertGreater(missal_x - burse_x, 100.0)

    def test_the_gospel_side_missal_draws_on_the_other_half_of_the_page(self) -> None:
        missal = self.item(GOSPEL_SIDE, "missal")
        self.assertEqual(missal["placement_semantic"], "mensa-gospel-corner")
        self.assertLess(missal["position"][0], 0, "this Missal is gospelward")

        centre = self.panel_centre_x(GOSPEL_SIDE)
        moved_x = self.mean_x(GOSPEL_SIDE, "missal")
        canary_x = self.mean_x(CANARY, "missal")

        self.assertLess(
            moved_x, centre,
            "the Gospel-side Missal must be drawn on the page-left half",
        )
        self.assertLess(
            moved_x, canary_x,
            "moving the book to the Gospel side must move its drawing",
        )
        self.assertLess(moved_x, self.mean_x(GOSPEL_SIDE, "burse"))

    def test_moving_the_missal_across_the_altar_does_not_mirror_it(self) -> None:
        canary = self.item(CANARY, "missal")
        moved = self.item(GOSPEL_SIDE, "missal")
        self.assertEqual(
            canary["reading"]["page_up_yaw_deg"],
            moved["reading"]["page_up_yaw_deg"],
        )
        self.assertEqual(canary["yaw_deg"], moved["yaw_deg"])

        canary_parts = self.engine.object_parts(canary)
        moved_parts = self.engine.object_parts(moved)
        self.assertEqual(len(canary_parts), len(moved_parts))
        self.assertEqual(
            self.part_signature(canary_parts), self.part_signature(moved_parts)
        )

        # The same variant, not a mirrored one. `object_parts` returns no
        # variant name, so the drawn geometry is matched against the library:
        # the open spread, never the closed slab.
        variants = self.library["missal"]["variants"]
        opened = [
            len(part["points"]) + (1 if part.get("closed") else 0)
            for part in variants["open"]["parts"]
        ]
        shut = [
            len(part["points"]) + (1 if part.get("closed") else 0)
            for part in variants["closed"]["parts"]
        ]
        self.assertNotEqual(opened, shut)
        for parts in (canary_parts, moved_parts):
            self.assertEqual(self.part_signature(parts), opened)

        # Same object, transformed: the two drawings differ only by placement.
        canary_local = [
            [(round(x - canary["position"][0], 9),
              round(y - canary["position"][1], 9),
              round(z - canary["position"][2], 9)) for x, y, z in part]
            for part in canary_parts
        ]
        moved_local = [
            [(round(x - moved["position"][0], 9),
              round(y - moved["position"][1], 9),
              round(z - moved["position"][2], 9)) for x, y, z in part]
            for part in moved_parts
        ]
        self.assertEqual(canary_local, moved_local)

    # -- object identity ---------------------------------------------------
    def test_materially_different_objects_do_not_share_geometry(self) -> None:
        for name in DISTINCT_OBJECTS:
            self.assertIn(name, self.library, name)
            self.assertTrue(self.library_variant(name)["parts"], name)

        for first, second in itertools.combinations(DISTINCT_OBJECTS, 2):
            one, other = self.library_variant(first), self.library_variant(second)
            self.assertNotEqual(one["parts"], other["parts"], f"{first}/{second}")
            self.assertTrue(
                self.variant_points(one).isdisjoint(self.variant_points(other)),
                f"{first} and {second} share geometry",
            )

        # The book against the case it was confused with.
        missal_open = self.library["missal"]["variants"]["open"]
        burse = self.library_variant("burse")
        self.assertNotEqual(len(missal_open["parts"]), len(burse["parts"]))
        self.assertTrue(
            self.variant_points(missal_open).isdisjoint(self.variant_points(burse))
        )

        # The vessel against a flat object: a chalice stands up, a paten lies
        # down, and no reader could take one for the other.
        chalice = self.library_variant("chalice")
        paten = self.library_variant("paten")
        self.assertNotEqual(len(chalice["parts"]), len(paten["parts"]))
        heights = {
            name: max(p[2] for part in self.library_variant(name)["parts"]
                      for p in part["points"])
            for name in ("chalice", "paten", "corporal", "pall")
        }
        self.assertGreater(heights["chalice"], 0.2)
        for flat in ("paten", "corporal", "pall"):
            self.assertLess(heights[flat], 0.05, flat)

    # -- actors ------------------------------------------------------------
    def test_actors_are_body_envelopes_and_not_labelled_circles(self) -> None:
        standing = self.actor(CANARY, "priest")
        kneeling = self.actor(GOSPEL_SIDE, "AC2")
        self.assertEqual(standing["posture"], "standing")
        self.assertEqual(kneeling["posture"], "kneeling")

        upright = self.underlay.mannequin(standing, True)
        knelt = self.underlay.mannequin(kneeling, False)
        for parts, who in ((upright, "standing"), (knelt, "kneeling")):
            self.assertGreaterEqual(len(parts), 6, who)
            self.assertGreaterEqual(
                sum(len(part) for part in parts), 20, who
            )

        upright_span = self.z_span(upright)
        self.assertGreater(upright_span, 1.2, "a standing figure has a body")
        self.assertLess(upright_span, 1.9)
        self.assertLess(
            self.z_span(knelt), upright_span,
            "a kneeling figure must not be as tall as a standing one",
        )
        self.assertNotEqual(
            self.part_signature(upright) + [round(upright_span, 6)],
            self.part_signature(knelt) + [round(self.z_span(knelt), 6)],
        )

        # Facing is geometry, not an annotation: only the yaw changes here.
        turned = copy.deepcopy(standing)
        turned["body_facing_yaw_deg"] = self.actor(GOSPEL_SIDE, "priest")[
            "body_facing_yaw_deg"
        ]
        self.assertNotEqual(
            standing["body_facing_yaw_deg"], turned["body_facing_yaw_deg"]
        )
        faced = self.underlay.mannequin(turned, True)
        self.assertEqual(self.part_signature(upright), self.part_signature(faced))
        self.assertNotEqual(
            self.projected_points(CANARY, upright),
            self.projected_points(CANARY, faced),
            "turning an actor must change the drawing",
        )

    # -- the altar ---------------------------------------------------------
    def test_the_altar_is_drawn_as_volumes_from_the_floor_to_the_mensa(self) -> None:
        parts = self.underlay.altar_geometry()
        master = self.underlay.sanctuary()
        # The sanctuary is no longer six volumes. It draws the floor region,
        # three steps, the predella, the altar body, the mensa, the gradine,
        # the tabernacle and its door, a reredos band, the altar cross and
        # four candlesticks — 104 polylines as measured. The floor below is
        # set well under that so this is not a tripwire on the massing, and
        # well above the old six-volume 18 so that losing the superstructure
        # is a failure rather than a smaller number nobody reads.
        self.assertGreaterEqual(len(parts), 60, len(parts))

        zs = [p[2] for part in parts for p in part]
        self.assertAlmostEqual(min(zs), 0.0, places=6)
        mensa_z = self.item(CANARY, "corporal")["position"][2]
        self.assertGreaterEqual(
            max(zs), mensa_z,
            "the altar must reach the surface its linen lies on",
        )
        # And it does not stop there: an altar is read from its superstructure,
        # so the drawing must reach the top of the crowning band the master
        # declares, not merely the slab.
        crown = float(master["altar"]["reredos_hint"]["to_z"])
        self.assertGreaterEqual(
            max(zs), crown,
            f"the drawn sanctuary stops at z={max(zs)}, below the {crown} the "
            "reredos band reaches. Without the mass above the mensa the altar "
            "reads as a cupboard on a slab",
        )

        levels = sorted({round(min(p[2] for p in part), 4) for part in parts})
        self.assertGreaterEqual(
            len(levels), 6,
            f"three steps, predella, body and mensa need distinct levels: {levels}",
        )
        self.assertEqual(levels[0], 0.0)

        # The cross and the candlesticks stand where sanctuary-master.yaml
        # puts them. They are what makes the mass unmistakably an altar, and
        # an anchor nothing checks is an anchor an editor can move.
        drawn = {
            (round(p[0], 4), round(p[1], 4)) for part in parts for p in part
        }
        anchors = master["fixed_anchors"]
        for label, anchor in (
            [("altar cross", anchors["altar_cross"])]
            + [("candlestick", c) for c in anchors["candlesticks"]]
        ):
            self.assertIn(
                (round(anchor[0], 4), round(anchor[1], 4)), drawn,
                f"nothing is drawn on the {label} anchor at "
                f"{anchor[0]}, {anchor[1]}",
            )
        heights = [
            max(p[2] for part in parts for p in part if
                round(p[0], 4) == round(c[0], 4)
                and round(p[1], 4) == round(c[1], 4))
            for c in anchors["candlesticks"]
        ]
        for height, candle in zip(heights, anchors["candlesticks"]):
            self.assertGreater(
                height, candle[2],
                f"the candlestick at {candle[:2]} is drawn flat on its "
                "anchor; a candlestick stands up",
            )

    # -- the panel ---------------------------------------------------------
    def test_a_one_panel_contract_draws_one_panel_and_no_furniture(self) -> None:
        contract = self.contract(CANARY)
        self.assertEqual(len(contract["panels"]), 1)
        self.assertEqual(contract["additional_panels"], "forbidden")
        self.assertEqual(len(PANEL_GROUP.findall(self.svg)), 1)
        self.assertEqual(self.svg.count("<g "), 1)

        body = COMMENT.sub("", self.svg)
        self.assertNotIn("<text", body)
        self.assertNotIn("<tspan", body)

        tags = Counter(ELEMENT.findall(body))
        self.assertEqual(
            set(tags), {"svg", "rect", "style", "g", "path"}, sorted(tags)
        )
        self.assertEqual(tags["svg"], 1)
        self.assertEqual(tags["g"], 1)
        self.assertEqual(tags["style"], 1)
        self.assertGreater(tags["path"], 20)

        # The one non-geometry mark is the full-bleed background.
        rects = re.findall(r"<rect[^>]*>", body)
        self.assertEqual(len(rects), 1, rects)
        self.assertIn('width="100%"', rects[0])
        self.assertIn('height="100%"', rects[0])

        root = ElementTree.fromstring(self.svg)
        width = self.underlay.PANEL_W * len(contract["panels"])
        self.assertEqual(root.get("width"), str(width))
        self.assertEqual(root.get("height"), str(self.underlay.PANEL_H))

    # -- determinism -------------------------------------------------------
    def test_rendering_the_same_scene_twice_is_byte_identical(self) -> None:
        contract = self.contract(CANARY)
        first = self.underlay.Underlay().render(contract)
        second = self.underlay.Underlay().render(contract)
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

        if not RSVG:
            self.skipTest(NO_RSVG)
        rasters = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as workspace:
                svg_path, png_path = self.underlay.write(contract, Path(workspace))
                self.assertEqual(svg_path.read_text(encoding="utf-8"), first)
                rasters.append(png_path.read_bytes())
        self.assertTrue(rasters[0].startswith(PNG_MAGIC))
        self.assertEqual(rasters[0], rasters[1])

    # -- fail closed -------------------------------------------------------
    def test_a_blocked_scene_leaves_no_underlay_behind(self) -> None:
        listing = blocked_scenes()
        self.assertTrue(listing, "the tooling listed no blocked scene")
        scene = listing[0]
        self.assertNotEqual(scene, CANARY)

        with tempfile.TemporaryDirectory() as workspace:
            out = Path(workspace)
            result = run(
                "art-seed", CALENDAR, FORM, scene, "--out", str(out),
                "--development",
            )
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn("REFUSED", result.stderr)
            self.assertFalse((out / scene).exists())
            self.assertEqual(list(out.iterdir()), [])
            self.assertEqual(list(out.rglob("render-underlay.png")), [])
            self.assertEqual(list(out.rglob("render-underlay.svg")), [])

    # -- the package the artistic agent receives ---------------------------
    @unittest.skipUnless(RSVG, NO_RSVG)
    def test_the_seed_package_ships_the_underlay_as_the_edit_source(self) -> None:
        with tempfile.TemporaryDirectory() as workspace:
            out = Path(workspace)
            result = run("art-seed", CALENDAR, FORM, CANARY, "--out", str(out),
                         "--development")
            self.assertEqual(result.returncode, 0, result.stderr)

            package = out / CANARY
            self.assertEqual(
                sorted(p.name for p in package.iterdir()), sorted(SEED_FILES)
            )
            for name in SEED_FILES:
                self.assertGreater((package / name).stat().st_size, 0, name)

            raster = (package / "render-underlay.png").read_bytes()
            self.assertTrue(raster.startswith(PNG_MAGIC))
            self.assertGreater(len(raster), MIN_RASTER_BYTES)
            svg = (package / "render-underlay.svg").read_text(encoding="utf-8")
            ElementTree.fromstring(svg)
            self.assertNotIn("<text", COMMENT.sub("", svg))

            provenance = load(package / "provenance.yaml")
            self.assertEqual(provenance["generation_mode"], "image-edit")
            self.assertEqual(
                provenance["render_underlay_source"], "render-underlay.png"
            )
            self.assertEqual(
                provenance["render_underlay_svg_source"], "render-underlay.svg"
            )
            self.assertEqual(
                provenance["render_underlay_sha256"],
                hashlib.sha256(raster).hexdigest(),
            )

            text = (package / "ART-AGENT-INSTRUCTIONS.md").read_text(
                encoding="utf-8"
            )
            flat = " ".join(text.split())
            self.assertIn("EDIT THE ATTACHED `render-underlay.png`", flat)
            self.assertIn("Do not create a fresh composition.", flat)
            self.assertIn("image EDIT", flat)
            self.assertIn("Do not use it as loose inspiration for a "
                          "text-to-image generation.", flat)
            self.assertIn("Do not substitute text-to-image generation.", flat)
            self.assertIn("the mandatory edit source", flat)


if __name__ == "__main__":
    unittest.main()
