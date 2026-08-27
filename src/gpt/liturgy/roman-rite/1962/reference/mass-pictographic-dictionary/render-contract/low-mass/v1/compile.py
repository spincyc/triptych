#!/usr/bin/env python3
"""Compile approved structural scenes into explicit render contracts.

Input:  the approved v0.21 structural corpus, plus the contract vocabularies.
Output: one compiled contract per scene, carrying resolved world geometry and
        no prose a renderer would have to interpret.

Usage:
    ./compile.py                 # write contracts/ and art-readiness.yaml
    ./compile.py --check         # fail if the tracked output is stale
    ./compile.py --scene LM-001A # print one contract to stdout
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _contract import (  # noqa: E402
    BASELINE_COMMIT,
    CONTRACT_VERSION,
    Contract,
    round6,
    vector_to_yaw,
    yaw_to_vector,
)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "contracts"
READINESS = ROOT / "art-readiness.yaml"


class Compiler:
    def __init__(self) -> None:
        self.c = Contract()
        policy = self.c.readiness_policy
        self.exceptions: dict[str, list[dict]] = {}
        for entry in policy["non_visible_cues"]:
            self.exceptions.setdefault(entry["scene_id"], []).append(entry)

    # -- readiness ---------------------------------------------------------
    def classify_cues(self, scene: dict) -> tuple[list[dict], list[dict]]:
        """Split a scene's unresolved cues into blocking and non-visible.

        Anything not explicitly classified non-visible blocks. That default is
        the whole safety property: an unclassified cue can never silently make
        a scene art-ready.
        """
        blocking, waived = [], []
        for cue in scene.get("unresolved") or []:
            match = None
            for entry in self.exceptions.get(scene["scene_id"], []):
                if entry["match"] in cue:
                    match = entry
                    break
            if match:
                waived.append({"cue": cue, "reason": match["reason"]})
            else:
                blocking.append({"cue": cue})
        return blocking, waived

    # -- panels ------------------------------------------------------------
    def compile_panels(self, scene: dict) -> list[dict]:
        panels = []
        preset_id = scene["camera"]["view"]
        panels.append(self.compile_panel("primary", preset_id))
        for extra in self.c.extra_panels.get(scene["scene_id"], []):
            panels.append(self.compile_panel(extra["id"], extra["camera"]))
        return panels

    def compile_panel(self, panel_id: str, preset_id: str) -> dict:
        preset = self.c.presets[preset_id]
        projection = self.c.projections[preset["projection"]]
        position = self.c.cam_positions[preset["position"]]
        panel = {
            "id": panel_id,
            "camera": {
                "preset": preset_id,
                "projection": preset["projection"],
                "projection_kind": projection["kind"],
                "position": preset["position"],
                "position_xyz": [round6(v) for v in position["position"]],
                "up": preset.get("up", "upward"),
                "focal_length_px": position.get("focal_length_px"),
            },
        }
        target_id = preset.get("target")
        if target_id:
            target = self.c.cam_targets[target_id]
            panel["camera"]["target"] = target_id
            panel["camera"]["target_xyz"] = [round6(v) for v in target["position"]]
        frame = preset.get("frame")
        if frame:
            panel["camera"]["frame"] = dict(frame)
        if preset.get("collapses_equal_depth"):
            panel["camera"]["collapses_equal_depth"] = True
        return panel

    # -- actors ------------------------------------------------------------
    # Two actors at the SAME DEPTH may differ in depth_rank: that is how the
    # corpus records who leads a crossing, whether or not they share an anchor.
    # The first post-ablution crossing puts both acolytes on one anchor; the
    # second puts them on opposite anchors at equal depth. Left symbolic, the
    # precedence is undrawable either way, so the rank resolves here to an
    # explicit naveward offset, recorded on the contract so a reviewer can see
    # it was derived and not invented.
    DEPTH_STEP = 0.16

    def depth_offsets(self, scene: dict) -> dict[str, float]:
        groups: dict[float, list] = {}
        for actor in scene["actors"]:
            depth = self.c.anchor_position(actor["anchor"])[1]
            groups.setdefault(depth, []).append(actor)
        offsets = {}
        for members in groups.values():
            if len(members) < 2:
                continue
            ranks = {m["depth_rank"] for m in members}
            if len(ranks) < 2:
                continue
            lowest = min(ranks)
            for member in members:
                offsets[member["id"]] = round6(
                    (member["depth_rank"] - lowest) * self.DEPTH_STEP
                )
        return offsets

    def compile_actors(self, scene: dict, panels: list[dict]) -> list[dict]:
        out = []
        panel_ids = [p["id"] for p in panels]
        offsets = self.depth_offsets(scene)
        for actor in scene["actors"]:
            yaw, how = self.c.resolve_facing(actor, scene)
            position = self.c.anchor_position(actor["anchor"])
            offset = offsets.get(actor["id"])
            if offset:
                position = [position[0], round6(position[1] + offset), position[2]]
            record = {
                "id": actor["id"],
                "role": actor["role"],
                "anchor": actor["anchor"],
                "position": position,
                "side": actor["side"],
                "depth_rank": actor["depth_rank"],
                "posture": actor["posture"],
                "bow": actor["bow"],
                "body_facing_yaw_deg": round6(yaw),
                "body_facing_vector": yaw_to_vector(yaw),
                "facing_semantic": actor["facing"],
                "facing_derivation": how,
                "gaze": actor["gaze"],
                "hands": {
                    "joined": actor["hands"]["joined"],
                    "left": actor["hands"]["left"],
                    "right": actor["hands"]["right"],
                },
                "gestures": list(actor.get("gestures") or []),
                "panel_visibility": panel_ids,
            }
            if offset is not None:
                record["depth_offset_naveward"] = offset
                record["depth_offset_note"] = (
                    "derived from depth_rank because this actor shares an "
                    "anchor with another; smaller rank stands nearer the viewer"
                )
            path = actor.get("path")
            if path and path.get("to"):
                record["path"] = {
                    "from": path.get("from"),
                    "from_xyz": self.c.anchor_position(path["from"])
                    if path.get("from")
                    else None,
                    "via": list(path.get("via") or []),
                    "via_xyz": [
                        self.c.anchor_position(step) for step in path.get("via") or []
                    ],
                    "to": path["to"],
                    "to_xyz": self.c.anchor_position(path["to"]),
                    "settles_at": actor["anchor"],
                    "note": path.get("note", ""),
                }
            out.append(record)
        return out

    # -- objects -----------------------------------------------------------
    def compile_objects(self, scene: dict, panels: list[dict]) -> tuple[list, list]:
        out, unresolved = [], []
        panel_ids = [p["id"] for p in panels]
        for item in scene.get("objects") or []:
            object_id = item["id"]
            definition = self.c.object_defs[object_id]
            position, kind, note = self.c.resolve_placement(item["placement"])
            record = {
                "id": object_id,
                "placement_semantic": item["placement"],
                "placement_kind": kind,
                "scale_class": definition["scale_class"],
                "oriented": definition["oriented"],
                "orientation_semantic": item.get("orientation"),
                "state_after": item.get("state_after"),
                "handled_by": item["handled_by"],
                "panel_visibility": panel_ids,
            }
            if kind == "absent":
                record["visible"] = False
                record["position"] = None
                record["absent_reason"] = note
            elif kind == "actor-held":
                record["parent_transform"] = note
                record["position"] = None
            elif position is not None:
                record["position"] = position
            else:
                record["position"] = None

            if definition["oriented"]:
                yaw, rule_id, why = self.c.resolve_yaw(object_id, position, scene)
                record["orientation_rule"] = rule_id
                if yaw is not None:
                    record["yaw_deg"] = round6(yaw)
                    record["facing_vector"] = yaw_to_vector(yaw)
                if why:
                    record["orientation_note"] = why
                if object_id in ("missal", "missal-stand"):
                    missal = self.c.missal["reading_orientation"]
                    support = self.c.missal.get("support") or {}
                    carried = "carried" in str(item.get("state_after") or "").lower() \
                        or "hand" in str(item["placement"]).lower()
                    record["reading"] = {
                        "page_up_yaw_deg": missal["page_up_yaw_deg"],
                        "page_up_vector": missal["page_up_vector"],
                        "support_pitch_deg": 0.0 if carried else float(
                            support.get("pitch_deg", 0.0)
                        ),
                        "supported_by": None if carried else support.get("supported_by"),
                        "page_up_vector_pitched": (
                            missal["page_up_vector"] if carried
                            else missal.get("page_up_vector_pitched")
                        ),
                        "page_normal_world": (
                            [0.0, 0.0, 1.0] if carried
                            else missal.get("page_normal_world")
                        ),
                        "spine_yaw_deg": round6(
                            (missal["page_up_yaw_deg"] - 90.0) % 360.0
                        ),
                        "reading_edge_yaw_deg": round6(
                            (missal["page_up_yaw_deg"] + 180.0) % 360.0
                        ),
                        "page_normal": [0.0, 0.0, 1.0],
                        "priest_facing_yaw_deg": missal["priest_facing_yaw_deg"],
                        "priest_facing_vector": missal["priest_facing_vector"],
                        "semantic_direction": missal["semantic_direction"],
                        "identical_on_both_sides": True,
                    }
            if kind in ("unresolved", "unplaced"):
                record["unresolved_placement"] = True
                record["unplaced_reason"] = note or item["placement"]
                if definition.get("render_critical"):
                    unresolved.append(
                        f"{object_id}: placement not resolvable to world geometry "
                        f"({item['placement']!r})"
                    )
            out.append(record)
        return out, unresolved

    # -- one scene ---------------------------------------------------------
    def compile_scene(self, scene_id: str) -> dict:
        scene = self.c.scene(scene_id)
        row = next(
            r for r in self.c.inventory["scenes"] if r["scene_id"] == scene_id
        )
        panels = self.compile_panels(scene)
        actors = self.compile_actors(scene, panels)
        objects, geometry_gaps = self.compile_objects(scene, panels)
        blocking, waived = self.classify_cues(scene)

        frame_gaps = [
            f"undetermined reference frame: {entry['phrase']!r} — "
            f"{entry['human_must_decide']}"
            for entry in self.c.undetermined.get(scene_id, [])
        ]
        reasons = [entry["cue"] for entry in blocking] + geometry_gaps + frame_gaps
        readiness = {
            "status": "blocked" if reasons else "ready",
        }
        if reasons:
            readiness["unresolved_cues"] = reasons
        if waived:
            readiness["waived_cues"] = waived

        contract = {
            "render_contract_version": CONTRACT_VERSION,
            "plate_id": scene_id,
            "scene_ids": [scene_id],
            "structural_baseline_commit": BASELINE_COMMIT,
            "structural_sources": [
                f"structural/low-mass/v0.21/scenes/{row['file']}",
                "structural/low-mass/v0.21/scenes/inventory.yaml",
            ],
            "title": scene["title"],
            "order": row["order"],
            "cluster": scene["cluster"],
            "condition": scene["condition"],
            "world_frame": {
                "reference": "world-frame.yaml",
                "x": {"positive": "epistleward", "negative": "gospelward"},
                "y": {"positive": "altarward", "negative": "naveward"},
                "z": {"positive": "upward", "negative": "downward"},
                "units": "dimensionless-synthetic",
                "yaw_zero": "epistleward",
                "yaw_increases": "counter-clockwise seen from above",
            },
            "art_readiness": readiness,
            "panels": panels,
            "additional_panels": "forbidden",
            "actors": actors,
            "objects": objects,
            "visible_invariants": list(scene["invariants"]),
            "blocked_cues": reasons,
        }
        return contract

    def compile_all(self) -> tuple[dict[str, dict], dict]:
        contracts = {sid: self.compile_scene(sid) for sid in self.c.scene_ids}
        ready = [s for s, c in contracts.items()
                 if c["art_readiness"]["status"] == "ready"]
        blocked = [s for s, c in contracts.items()
                   if c["art_readiness"]["status"] == "blocked"]
        readiness = {
            "schema": "triptych.mass_pictographic.art_readiness",
            "version": CONTRACT_VERSION,
            "structural_baseline_commit": BASELINE_COMMIT,
            "generated_by": "compile.py",
            "note": (
                "Derived from the corpus's own unresolved cues and "
                "readiness-policy.yaml. Never edit by hand; run compile.py."
            ),
            "totals": {
                "scenes": len(contracts),
                "ready": len(ready),
                "blocked": len(blocked),
            },
            "ready_scenes": sorted(ready),
            "blocked_scenes": [
                {
                    "scene_id": sid,
                    "unresolved_cues": contracts[sid]["art_readiness"][
                        "unresolved_cues"
                    ],
                }
                for sid in sorted(blocked)
            ],
        }
        return contracts, readiness


def dump(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail if tracked output is stale")
    parser.add_argument("--scene", help="print one compiled contract")
    args = parser.parse_args()

    compiler = Compiler()

    if args.scene:
        print(dump(compiler.compile_scene(args.scene)), end="")
        return 0

    contracts, readiness = compiler.compile_all()

    expected = compiler.c.readiness_policy["expected"]
    actual = {
        "ready_scenes": readiness["totals"]["ready"],
        "blocked_scenes": readiness["totals"]["blocked"],
    }
    for key, value in actual.items():
        if expected[key] != value:
            print(
                f"readiness drift: policy expects {key}={expected[key]}, "
                f"corpus yields {value}",
                file=sys.stderr,
            )
            return 1

    OUT.mkdir(exist_ok=True)
    stale = []
    for scene_id, contract in contracts.items():
        target = OUT / f"{scene_id}.yaml"
        text = dump(contract)
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != text:
                stale.append(target.name)
        else:
            target.write_text(text, encoding="utf-8")

    text = dump(readiness)
    if args.check:
        if READINESS.read_text(encoding="utf-8") != text:
            stale.append(READINESS.name)
        tracked = {p.name for p in OUT.glob("*.yaml")}
        orphans = tracked - {f"{s}.yaml" for s in contracts}
        if orphans:
            stale.extend(sorted(orphans))
        if stale:
            print("stale compiled output: " + ", ".join(stale[:8])
                  + (f" (+{len(stale) - 8} more)" if len(stale) > 8 else ""),
                  file=sys.stderr)
            return 1
        print(f"PASS: {len(contracts)} compiled contracts are current "
              f"({readiness['totals']['ready']} art-ready, "
              f"{readiness['totals']['blocked']} blocked)")
        return 0

    READINESS.write_text(text, encoding="utf-8")
    print(f"compiled {len(contracts)} render contracts "
          f"({readiness['totals']['ready']} art-ready, "
          f"{readiness['totals']['blocked']} blocked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
