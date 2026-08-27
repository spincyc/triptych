#!/usr/bin/env python3
"""Acceptance checks for the 1962 Low Mass render contract.

These go beyond "the right string appears in a YAML file". They prove that the
compiled geometry cannot express the two failures that opened this lane: a
mirrored Missal, and a panel nobody declared.

Run from this directory:
    ./validate.py
"""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONTRACTS = ROOT / "contracts"
SKELETONS = ROOT / "skeletons"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class Failure(AssertionError):
    pass


def check_world_frame(world: dict) -> None:
    axes = world["world_frame"]
    if axes["x"]["negative"] != "gospelward" or axes["x"]["positive"] != "epistleward":
        raise Failure("the X axis must run gospelward-negative, epistleward-positive")
    if axes["y"]["positive"] != "altarward":
        raise Failure("the Y axis must run altarward-positive")
    if axes["z"]["positive"] != "upward":
        raise Failure("the Z axis must run upward-positive")
    named = {d["id"]: d["vector"] for d in world["directions"]}
    if named["gospelward"][0] >= 0:
        raise Failure("gospelward must have a negative X component")
    if named["epistleward"][0] <= 0:
        raise Failure("epistleward must have a positive X component")
    angles = world["yaw"]["reference_angles"]
    if angles["altarward"] != 90 or angles["gospelward"] != 180:
        raise Failure("the yaw reference angles do not match the axis definitions")


def check_camera_model(camera: dict) -> None:
    projections = {p["id"] for p in camera["projections"]}
    forbidden = {name.lower() for name in camera["forbidden_projection_names"]}
    for name in projections:
        if name.lower() in forbidden:
            raise Failure(f"projection {name!r} is a place name, not a projection")
    if "orthographic-plan" not in projections:
        raise Failure("an overhead view must exist as a real projection")
    positions = {p["id"] for p in camera["camera_positions"]}
    if "nave-centre" not in positions:
        raise Failure("the nave must exist as a camera position")
    if "nave" in projections:
        raise Failure('"nave" must never be a projection')
    for preset in camera["presets"]:
        if preset["projection"] not in projections:
            raise Failure(f"preset {preset['id']} names an unknown projection")
        if preset["position"] not in positions:
            raise Failure(f"preset {preset['id']} names an unknown camera position")
        required = (camera["frame_requirements"].get(preset["projection"]) or {}).get(
            "requires", []
        )
        frame = preset.get("frame") or {}
        for field in required:
            if field not in frame:
                raise Failure(
                    f"preset {preset['id']} uses {preset['projection']} "
                    f"without declaring {field}"
                )


def check_missal_rule(missal: dict) -> None:
    reading = missal["reading_orientation"]
    if reading["page_up_vector"][0] >= 0:
        raise Failure(
            "the Missal reading direction must be gospelward, so its X is negative"
        )
    if not reading["identical_on_both_sides"]:
        raise Failure("the Missal reading orientation must not depend on the side")
    if reading["page_up_yaw_deg"] == missal["mirror_test"]["forbidden_page_up_yaw_deg"]:
        raise Failure("the reading yaw equals the forbidden mirrored yaw")


def check_contracts(contracts: list[dict], camera: dict, missal: dict) -> dict:
    projections = {p["id"] for p in camera["projections"]}
    positions = {p["id"] for p in camera["camera_positions"]}
    expected_yaw = missal["reading_orientation"]["page_up_yaw_deg"]
    forbidden_yaw = missal["mirror_test"]["forbidden_page_up_yaw_deg"]
    seen_missal_sides: dict[str, set] = {}
    stats = {"ready": 0, "blocked": 0, "missal_scenes": 0, "panels": 0}

    for contract in contracts:
        plate = contract["plate_id"]

        # -- panels ------------------------------------------------------
        if not contract["panels"]:
            raise Failure(f"{plate}: has no panel")
        if contract.get("additional_panels") != "forbidden":
            raise Failure(f"{plate}: does not forbid additional panels")
        ids = [p["id"] for p in contract["panels"]]
        if len(ids) != len(set(ids)):
            raise Failure(f"{plate}: repeats a panel id")
        stats["panels"] += len(ids)
        for panel in contract["panels"]:
            cam = panel["camera"]
            if cam["projection"] not in projections:
                raise Failure(f"{plate}/{panel['id']}: unknown projection")
            if cam["position"] not in positions:
                raise Failure(f"{plate}/{panel['id']}: unknown camera position")
            if cam["projection"] == "orthographic-plan":
                frame = cam.get("frame") or {}
                if "page_top_world_direction" not in frame:
                    raise Failure(
                        f"{plate}/{panel['id']}: a plan view without a page top"
                    )

        # -- actors ------------------------------------------------------
        if [a["id"] for a in contract["actors"]] != ["priest", "AC1", "AC2"]:
            raise Failure(f"{plate}: actors are not priest, AC1, AC2 in order")
        for actor in contract["actors"]:
            vector = actor["body_facing_vector"]
            if abs((vector[0] ** 2 + vector[1] ** 2) ** 0.5 - 1.0) > 1e-6:
                raise Failure(f"{plate}/{actor['id']}: facing vector is not a unit vector")
            side = actor["side"]
            x = actor["position"][0]
            if side == "gospel" and x > 0:
                raise Failure(f"{plate}/{actor['id']}: gospel side must be x<=0")
            if side == "epistle" and x < 0:
                raise Failure(f"{plate}/{actor['id']}: epistle side must be x>=0")

        # side-orthographic panels must not invent depth separation
        for panel in contract["panels"]:
            if not panel["camera"].get("collapses_equal_depth"):
                continue
            by_depth: dict[float, set] = {}
            for actor in contract["actors"]:
                by_depth.setdefault(actor["position"][1], set()).add(
                    actor["depth_rank"]
                )
            for y, ranks in by_depth.items():
                if len(ranks) > 1 and len(by_depth) == 1:
                    raise Failure(
                        f"{plate}: a collapsing view separates actors at one depth"
                    )

        # -- objects -----------------------------------------------------
        for item in contract["objects"]:
            if item["id"] in ("missal", "missal-stand"):
                reading = item.get("reading")
                if not reading:
                    raise Failure(f"{plate}: {item['id']} carries no compiled reading")
                if reading["page_up_yaw_deg"] != expected_yaw:
                    raise Failure(
                        f"{plate}: {item['id']} reading yaw "
                        f"{reading['page_up_yaw_deg']} is not the canonical "
                        f"{expected_yaw}"
                    )
                if reading["page_up_yaw_deg"] == forbidden_yaw:
                    raise Failure(f"{plate}: {item['id']} is mirrored")
                if reading["page_up_vector"][0] >= 0:
                    raise Failure(
                        f"{plate}: {item['id']} does not read toward the Gospel side"
                    )
            if item["id"] == "missal":
                stats["missal_scenes"] += 1
                placement = item["placement_semantic"]
                side = (
                    "gospel"
                    if isinstance(placement, str) and "gospel" in placement.lower()
                    else "epistle"
                    if isinstance(placement, str) and "epistle" in placement.lower()
                    else "other"
                )
                seen_missal_sides.setdefault(side, set()).add(
                    item["reading"]["page_up_yaw_deg"]
                )
            if item.get("oriented") and item.get("position") is not None:
                if item.get("yaw_deg") is None:
                    raise Failure(
                        f"{plate}: {item['id']} is oriented and placed but has no yaw"
                    )

        # -- readiness ---------------------------------------------------
        readiness = contract["art_readiness"]
        if readiness["status"] not in ("ready", "blocked"):
            raise Failure(f"{plate}: unknown art_readiness status")
        if readiness["status"] == "blocked":
            stats["blocked"] += 1
            if not readiness.get("unresolved_cues"):
                raise Failure(f"{plate}: blocked without naming a cue")
        else:
            stats["ready"] += 1
            # the semantic-only lint: a render-ready scene may not depend on
            # uncompiled natural language for anything visible.
            for item in contract["objects"]:
                if item.get("unresolved_placement"):
                    raise Failure(
                        f"{plate}: art-ready but {item['id']} has an "
                        "unresolved placement"
                    )
                if item.get("oriented") and item.get("position") is not None:
                    if item.get("yaw_deg") is None:
                        raise Failure(
                            f"{plate}: art-ready but {item['id']} has only a "
                            "semantic orientation"
                        )

    # Ordered crossing choreography must survive compilation, not merely be
    # asserted in prose. Nearer the viewer is smaller y.
    by_plate = {c["plate_id"]: c for c in contracts}

    def depth_of(plate: str, actor_id: str) -> float:
        actor = next(a for a in by_plate[plate]["actors"] if a["id"] == actor_id)
        return actor["position"][1]

    if "LM-136C" in by_plate:
        if not depth_of("LM-136C", "AC2") < depth_of("LM-136C", "AC1"):
            raise Failure(
                "LM-136C: AC2 leads the first crossing and must compile nearer "
                "the viewer than AC1"
            )
    if "LM-136E" in by_plate:
        if not depth_of("LM-136E", "AC1") < depth_of("LM-136E", "AC2"):
            raise Failure(
                "LM-136E: AC1 leads the second crossing and must compile nearer "
                "the viewer than AC2"
            )

    # The whole point, stated as one assertion.
    if len(seen_missal_sides.get("gospel", set())) > 1:
        raise Failure("the Missal takes more than one reading yaw on the Gospel side")
    gospel = seen_missal_sides.get("gospel", set())
    epistle = seen_missal_sides.get("epistle", set())
    if gospel and epistle and gospel != epistle:
        raise Failure(
            f"the Missal reads differently by side: gospel={gospel} epistle={epistle}"
        )
    return stats


def check_skeletons(contracts: list[dict]) -> int:
    count = 0
    for contract in contracts:
        path = SKELETONS / f"{contract['plate_id']}.svg"
        if not path.is_file():
            raise Failure(f"{contract['plate_id']}: no skeleton")
        ET.parse(path)
        text = path.read_text(encoding="utf-8")
        drawn = set(re.findall(r"panel ([a-z0-9-]+)</text>", text))
        declared = {p["id"] for p in contract["panels"]}
        if drawn != declared:
            raise Failure(
                f"{contract['plate_id']}: skeleton panels {sorted(drawn)} differ "
                f"from the contract's {sorted(declared)}"
            )
        for forbidden in ("TOP VIEW", "TOP VIEW (NAVE)"):
            if forbidden in text.upper():
                raise Failure(f"{contract['plate_id']}: skeleton names {forbidden!r}")
        count += 1
    return count


AUTHORED = (
    "README.md",
    "world-frame.yaml",
    "camera-model.yaml",
    "object-model.yaml",
    "panel-contract.yaml",
    "missal-orientation.yaml",
    "frame-vocabulary.yaml",
    "placement-map.yaml",
    "readiness-policy.yaml",
    "_contract.py",
    "compile.py",
    "skeleton.py",
    "review.py",
    "validate.py",
    "underlay.py",
    "underlay-objects.yaml",
)


def check_authored_manifest() -> int:
    """Hash the authored inputs.

    The generated output — contracts/, skeletons/, review/ — is not hashed
    here: `compile.py --check`, `skeleton.py --check` and `review.py --check`
    prove it matches its inputs exactly, which is a stronger statement than a
    checksum and cannot go stale silently.
    """
    import hashlib

    listed = {}
    for line in (ROOT / "MANIFEST-AUTHORED.sha256").read_text(
        encoding="utf-8"
    ).splitlines():
        digest, name = line.split("  ", 1)
        listed[name] = digest
    if set(listed) != set(AUTHORED):
        raise Failure(
            f"MANIFEST-AUTHORED.sha256 covers {sorted(listed)}, "
            f"expected {sorted(AUTHORED)}"
        )
    for name, digest in listed.items():
        actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if actual != digest:
            raise Failure(f"authored input changed without a manifest update: {name}")
    return len(listed)


UNDERLAYS = ROOT / "underlays"


def check_underlays(contracts: list[dict]) -> int:
    """The conditioning drawings exist, parse, and carry no text.

    A label in the underlay would let a renderer read the scene instead of
    seeing it, which is precisely the failure this layer exists to end.
    """
    count = 0
    for contract in contracts:
        if contract["art_readiness"]["status"] != "ready":
            continue
        path = UNDERLAYS / contract["plate_id"] / "render-underlay.svg"
        if not path.is_file():
            raise Failure(f"{contract['plate_id']}: no render underlay")
        ET.parse(path)
        text = path.read_text(encoding="utf-8")
        for element in ("<text", "<tspan"):
            if element in text:
                raise Failure(
                    f"{contract['plate_id']}: the underlay carries {element}; "
                    "the conditioning drawing must have no readable labels"
                )
        groups = text.count("<g transform=")
        if groups != len(contract["panels"]):
            raise Failure(
                f"{contract['plate_id']}: underlay draws {groups} panels, "
                f"contract declares {len(contract['panels'])}"
            )
        count += 1
    return count


def check_projected_orientation(contracts: list[dict]) -> tuple[int, float, int]:
    """Prove the drawing embodies the compiled orientation, and shows it.

    Two separate failures, and the second is the one that hid. A yaw applied
    about the wrong local axis is a fidelity failure and shows up as a
    disagreement between the drawn page-up direction and the projection of the
    contract's own page-up vector. But a perfectly faithful yaw can still be
    invisible: seen at a grazing angle, a flat object's two principal axes
    collapse toward collinear, and the object then cannot look oriented at any
    yaw. Every earlier check passed while exactly that was true.
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("underlay", ROOT / "underlay.py")
    underlay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(underlay)

    library = load(ROOT / "underlay-objects.yaml")
    floor = float(
        library["local_frame_contract"]["legibility"]["minimum_axis_separation_deg"]
    )
    checked = 0
    worst = 180.0
    exempt = 0
    for contract in contracts:
        if contract["art_readiness"]["status"] != "ready":
            continue
        # A true side elevation collapses one horizontal axis on purpose: that
        # is what the view is for, and INV-GEO-03 requires it. Demanding that
        # an object's horizontal orientation stay legible there would be
        # demanding the view not be itself. Such scenes are exempt from the
        # legibility floor and counted, not silently skipped, so a scene that
        # needs orientation to read is known to need another declared panel.
        primary = contract["panels"][0]["camera"]
        if primary.get("collapses_equal_depth") or primary["projection"].endswith(
            "elevation-side"
        ):
            exempt += 1
            continue
        for item in contract["objects"]:
            if item["id"] not in ("missal", "burse", "paten", "missal-stand"):
                continue
            measured = underlay.projected_orientation(contract, item["id"])
            if measured is None:
                continue
            checked += 1
            if measured["fidelity_deg"] > 1.5:
                raise Failure(
                    f"{contract['plate_id']}: the drawn {item['id']} points "
                    f"{measured['page_up_deg']}deg but its compiled orientation "
                    f"projects to {measured['expected_deg']}deg — the model does "
                    "not embody the transform"
                )
            # Physical plausibility: a book on its stand is pitched toward the
            # priest, so its world page normal is not straight up. A normal of
            # exactly world-Z means the page plane was left horizontal and the
            # transform never reached it.
            if item["id"] == "missal":
                reading = item.get("reading") or {}
                # Whether the book is on a stand is a fact about its support,
                # not about a number that happens to be zero. Keying this off
                # the pitch let a contract disable the check by zeroing the very
                # value the check exists to police.
                carried = not reading.get("supported_by")
                published = reading.get("page_normal_world")
                normal = measured["world_page_normal"]
                if published and any(
                    abs(a - b) > 1e-3 for a, b in zip(published, normal)
                ):
                    raise Failure(
                        f"{contract['plate_id']}: the contract publishes a page "
                        f"normal of {published} but the drawn Missal resolves to "
                        f"{normal}; the contract and the drawing disagree about "
                        "how the book lies"
                    )
                horizontal = (normal[0] ** 2 + normal[1] ** 2) ** 0.5
                if not carried and horizontal < 0.15:
                    raise Failure(
                        f"{contract['plate_id']}: the Missal's world page normal "
                        f"is {normal}, effectively straight up. A book on its "
                        "stand faces the priest, not the ceiling; the page plane "
                        "has been left horizontal"
                    )
                if not carried and measured["pitch_deg"] <= 0.0:
                    raise Failure(
                        f"{contract['plate_id']}: a stand-supported Missal has no "
                        "pitch"
                    )
            worst = min(worst, measured["separation_deg"])
            if measured["separation_deg"] < floor:
                raise Failure(
                    f"{contract['plate_id']}: the {item['id']} projects only "
                    f"{measured['separation_deg']}deg from collinear, below the "
                    f"{floor}deg floor. The yaw is right and the picture cannot "
                    "show it; raise the camera rather than the yaw"
                )
    return checked, worst, exempt


def main() -> int:
    world = load(ROOT / "world-frame.yaml")
    camera = load(ROOT / "camera-model.yaml")
    missal = load(ROOT / "missal-orientation.yaml")
    readiness = load(ROOT / "art-readiness.yaml")

    check_world_frame(world)
    check_camera_model(camera)
    check_missal_rule(missal)

    contracts = [load(p) for p in sorted(CONTRACTS.glob("*.yaml"))]
    if not contracts:
        raise Failure("no compiled contracts found; run compile.py")
    stats = check_contracts(contracts, camera, missal)

    if stats["ready"] != readiness["totals"]["ready"]:
        raise Failure("art-readiness.yaml disagrees with the compiled contracts")
    boards = check_skeletons(contracts)
    drawings = check_underlays(contracts)
    oriented, worst, side_views = check_projected_orientation(contracts)
    hashed = check_authored_manifest()

    print(f"PASS: world frame, camera model and Missal rule "
          f"({hashed} checksummed authored inputs)")
    print(
        f"PASS: {len(contracts)} render contracts "
        f"({stats['ready']} art-ready, {stats['blocked']} blocked, "
        f"{stats['panels']} panels, {stats['missal_scenes']} Missal placements "
        f"all at one reading yaw)"
    )
    print(f"PASS: {boards} skeletons match their contracts' panel manifests")
    print(f"PASS: {drawings} render underlays, textless and panel-exact")
    print(
        f"PASS: {oriented} oriented objects embody their compiled transform "
        f"and stay legible (worst axis separation {worst:.1f}deg; "
        f"{side_views} side-elevation scenes exempt by design)"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as failure:
        print(f"FAIL: {failure}", file=sys.stderr)
        raise SystemExit(1)
