#!/usr/bin/env python3
"""Shared model for the 1962 Low Mass render contract.

Loads the contract vocabularies and the approved structural corpus, and
resolves symbolic scene values into explicit world geometry. Every renderable
direction produced here is an absolute world vector; nothing downstream needs
to interpret prose.
"""

from __future__ import annotations

import math
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
STRUCTURAL = (ROOT / "../../../structural/low-mass/v0.21").resolve()
SCENES = STRUCTURAL / "scenes"

CONTRACT_VERSION = "1.0"
BASELINE_COMMIT = "d2e97b5ca"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def round6(value: float) -> float:
    """Keep compiled output deterministic and free of float noise."""
    return round(value + 0.0, 6)


def yaw_to_vector(yaw_deg: float) -> list[float]:
    radians = math.radians(yaw_deg)
    return [round6(math.cos(radians)), round6(math.sin(radians)), 0.0]


def vector_to_yaw(dx: float, dy: float) -> float:
    return round6(math.degrees(math.atan2(dy, dx)) % 360.0)


class Contract:
    """The render-contract vocabularies plus the approved structural corpus."""

    def __init__(self) -> None:
        self.world = load(ROOT / "world-frame.yaml")
        self.camera = load(ROOT / "camera-model.yaml")
        self.objects = load(ROOT / "object-model.yaml")
        self.panels = load(ROOT / "panel-contract.yaml")
        self.missal = load(ROOT / "missal-orientation.yaml")
        self.placements = load(ROOT / "placement-map.yaml")
        self.readiness_policy = load(ROOT / "readiness-policy.yaml")
        self.frames = load(ROOT / "frame-vocabulary.yaml")

        self.geometry = load(SCENES / "geometry.yaml")
        self.inventory = load(SCENES / "inventory.yaml")
        self.invariants = load(SCENES / "invariants.yaml")

        self.directions = {d["id"]: d["vector"] for d in self.world["directions"]}
        self.anchors = {a["id"]: a for a in self.geometry["anchors"]}
        self.mensa_z = self.geometry["mensa_positions"]["z"]
        self.mensa = {
            p["id"]: p for p in self.geometry["mensa_positions"]["positions"]
        }
        depth = self.frames["mensa_depth"]
        self.mensa_default_y = depth["default_y"]
        self.mensa_y = {k: v["y"] for k, v in depth["positions"].items()}
        self.undetermined: dict[str, list] = {}
        for entry in self.frames.get("undetermined_phrases") or []:
            for scene_id in entry["scenes"]:
                self.undetermined.setdefault(scene_id, []).append(entry)
        self.presets = {p["id"]: p for p in self.camera["presets"]}
        self.projections = {p["id"]: p for p in self.camera["projections"]}
        self.cam_positions = {p["id"]: p for p in self.camera["camera_positions"]}
        self.cam_targets = {t["id"]: t for t in self.camera["targets"]}
        self.object_defs = {o["id"]: o for o in self.objects["objects"]}
        self.orientation_rules = {
            r["id"]: r for r in self.objects["orientation_rules"]
        }
        self.blocking_cues = {
            entry["scene_id"]: entry
            for entry in self.readiness_policy.get("blocking_cues") or []
        }
        self.extra_panels: dict[str, list] = {}
        for entry in self.panels.get("declared_extra_panels") or []:
            for scene_id in entry["scene_ids"]:
                self.extra_panels.setdefault(scene_id, []).extend(entry["add"])

        self._scenes: dict[str, dict] = {}
        self._order: list[str] = []
        for section in self.inventory["sections"]:
            document = load(SCENES / section["file"])
            for scene in document["scenes"]:
                self._scenes[scene["scene_id"]] = scene
                self._order.append(scene["scene_id"])

    # -- corpus access ----------------------------------------------------
    @property
    def scene_ids(self) -> list[str]:
        return list(self._order)

    def scene(self, scene_id: str) -> dict:
        if scene_id not in self._scenes:
            raise KeyError(f"unknown scene {scene_id!r}")
        return self._scenes[scene_id]

    # -- geometry resolution ----------------------------------------------
    def anchor_position(self, anchor_id: str) -> list[float]:
        anchor = self.anchors[anchor_id]
        return [round6(anchor["x"]), round6(anchor["y"]), round6(anchor["z"])]

    def resolve_placement(self, placement) -> tuple[list[float] | None, str, str]:
        """Return (position, kind, note) for an object placement.

        `kind` is one of: anchor, mensa, mapped, actor-held, absent,
        unplaced, unresolved.
        An unresolved placement is never guessed; it blocks art instead.
        """
        if not isinstance(placement, str):
            return None, "unresolved", "placement is not a string"
        if placement in self.anchors:
            return self.anchor_position(placement), "anchor", ""
        if placement in self.mensa:
            spot = self.mensa[placement]
            return (
                [
                    round6(spot["x"]),
                    round6(self.mensa_y.get(placement, self.mensa_default_y)),
                    round6(self.mensa_z),
                ],
                "mensa",
                "",
            )
        mapped = (self.placements.get("map") or {}).get(placement)
        if mapped:
            disposition = mapped.get("disposition")
            if disposition == "held":
                return None, "actor-held", mapped["held_by"]
            if disposition == "positioned":
                return (
                    [round6(v) for v in mapped["position"]],
                    "mapped",
                    mapped.get("note", ""),
                )
            if disposition == "absent":
                # The object is not on the altar at all. Nothing to draw, and
                # nothing unresolved: the record fixes that it is gone.
                return None, "absent", mapped.get("note", "")
            if disposition == "unplaced":
                # Declared, and deliberately without coordinates. The approved
                # record declines to fix this, so it is not invented here.
                return None, "unplaced", mapped.get("note", "")
            raise AssertionError(
                f"placement-map.yaml: unknown disposition {disposition!r}"
            )
        return None, "unresolved", placement

    # -- facing resolution -------------------------------------------------
    DIRECTION_FACING = {
        "people": 270.0,
        "nave": 270.0,
        "gospel-side": 180.0,
        "gospel": 180.0,
        "epistle-side": 0.0,
        "credence": 0.0,
    }
    # Facing targets, resolved to real mensa positions so a yaw can be derived.
    TARGET_FACING = {
        "altar": "mensa-centre",
        "altar-cross": "altar-cross",
        "centre": "mensa-centre",
        "oblations": "corporal-back-centre",
        "host": "corporal-front-centre",
        "chalice": "corporal-back-centre",
        "last-gospel-card": "mensa-gospel-corner",
        "inward-to-centre": "mensa-centre",
    }

    def mensa_point(self, mensa_id: str) -> list[float]:
        spot = self.mensa[mensa_id]
        return [
            round6(spot["x"]),
            round6(self.mensa_y.get(mensa_id, self.mensa_default_y)),
            round6(self.mensa_z),
        ]

    def resolve_facing(self, actor: dict, scene: dict) -> tuple[float, str]:
        """Return (yaw_deg, how) for an actor's body facing."""
        facing = actor["facing"]
        here = self.anchor_position(actor["anchor"])

        if facing == "missal":
            # The approved reading rule fixes this, identically on both sides.
            return (
                float(self.missal["reading_orientation"]["priest_facing_yaw_deg"]),
                "missal-reading-invariant",
            )
        if facing in self.DIRECTION_FACING:
            return self.DIRECTION_FACING[facing], "world-direction"
        if facing in self.TARGET_FACING:
            target = self.mensa_point(self.TARGET_FACING[facing])
            dx, dy = target[0] - here[0], target[1] - here[1]
            if abs(dx) < 1e-9 and abs(dy) < 1e-9:
                return 90.0, "degenerate-toward-altar"
            return vector_to_yaw(dx, dy), "toward-target"
        if facing == "inward-to-priest":
            priest = next(a for a in scene["actors"] if a["id"] == "priest")
            target = self.anchor_position(priest["anchor"])
            dx, dy = target[0] - here[0], target[1] - here[1]
            if abs(dx) < 1e-9 and abs(dy) < 1e-9:
                return 90.0, "degenerate-toward-altar"
            return vector_to_yaw(dx, dy), "toward-actor"
        raise AssertionError(f"{scene['scene_id']}: unmapped facing {facing!r}")

    # -- object orientation ------------------------------------------------
    def resolve_yaw(self, object_id: str, position, scene: dict) -> tuple:
        """Return (yaw_deg or None, rule_id, note)."""
        definition = self.object_defs[object_id]
        rule_id = definition["orientation_rule"]
        if not definition["oriented"]:
            return None, rule_id, "rotationally symmetric for rendering"
        rule = self.orientation_rules[rule_id]

        if rule_id == "missal-reading":
            yaw = float(self.missal["reading_orientation"]["page_up_yaw_deg"])
            return yaw, rule_id, "identical on both sides by invariant"
        if rule.get("yaw_deg") is not None:
            return float(rule["yaw_deg"]), rule_id, ""
        if rule_id in ("faces-priest", "handle-to-priest"):
            priest = next(a for a in scene["actors"] if a["id"] == "priest")
            station = self.anchor_position(priest["anchor"])
            if position is None:
                return None, rule_id, "position unresolved"
            dx, dy = station[0] - position[0], station[1] - position[1]
            if abs(dx) < 1e-9 and abs(dy) < 1e-9:
                return 270.0, rule_id, "degenerate, faces the nave"
            return vector_to_yaw(dx, dy), rule_id, "turned toward the priest"
        return None, rule_id, "no yaw source"
