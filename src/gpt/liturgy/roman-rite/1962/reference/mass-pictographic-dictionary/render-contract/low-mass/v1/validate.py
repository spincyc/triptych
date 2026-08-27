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
    "sanctuary-master.yaml",
    "camera-calibration.py",
)


def check_foot_contact(contracts: list[dict]) -> tuple[int, int]:
    """Prove every figure stands on something.

    The blocking is only worth drawing if the feet meet the sanctuary. A sole
    must lie in the plane of the level its actor was placed on, and its centre
    must fall on that level's own tread rather than on the one below. A little
    overhang past a leading edge is allowed because it is real - altar steps
    are barely deeper than a foot, and a turned figure does project over the
    edge - but a sole that has left its tread altogether is a figure standing
    on air, which is what the earlier envelopes did without anyone noticing.

    Actors in transit are counted separately. A walking figure is mid-stride
    between two levels and is not standing on either.
    """
    underlay = underlay_module()
    master = underlay.sanctuary()
    steps = master["steps"]
    treads = {}
    edge = steps["first_leading_edge_y"]
    for index in range(steps["count"]):
        treads[f"step_{index + 1}"] = (edge, edge + steps["tread_depth"])
        edge += steps["tread_depth"]
    predella = master["predella"]
    treads["predella"] = (
        predella["leading_edge_y"],
        predella["leading_edge_y"] + predella["depth"],
    )
    region = master["in_plano"]["standing_region"]
    treads["floor"] = (region["y_min"], region["y_max"])

    soles = 0
    in_transit = 0
    for contract in contracts:
        for actor in contract.get("actors") or []:
            contact = underlay.foot_contacts(actor, actor["id"] == "priest")
            level = contact["stands_on"]
            if level is None:
                raise Failure(
                    f"{contract['plate_id']}: {actor['id']} stands at elevation "
                    f"{contact['level_z']}, which is not a sanctuary level"
                )
            if not contact["soles"]:
                raise Failure(
                    f"{contract['plate_id']}: {actor['id']} has no sole in the "
                    f"plane of {level}; the figure does not meet the floor"
                )
            if actor["posture"] == "walking":
                in_transit += len(contact["soles"])
                continue
            low, high = treads[level]
            allowance = (high - low) * float(
                master["foot_contact"]["max_overhang_fraction_of_tread"]
            )
            for sole in contact["soles"]:
                soles += 1

                centre = (sole["y_max"] + sole["y_min"]) / 2.0
                if not low - 1e-9 <= centre <= high + 1e-9:
                    raise Failure(
                        f"{contract['plate_id']}: {actor['id']} has a sole "
                        f"centred at {centre:.3f} on {level}, whose tread runs "
                        f"{low:.2f} to {high:.2f}; the foot is on another level"
                    )
                over = max(low - sole["y_min"], sole["y_max"] - high, 0.0)
                if over > allowance:
                    raise Failure(
                        f"{contract['plate_id']}: {actor['id']} overhangs "
                        f"{level} by {over:.3f}, past the {allowance:.3f} a "
                        f"tread {high - low:.2f} deep allows"
                    )
    return soles, in_transit


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


UNDERLAY_MODULE = None


def underlay_module():
    """underlay.py itself, loaded once.

    Every measurement below is taken from the drawing the artistic agent will
    actually receive, so it is taken with the renderer's own camera, sanctuary
    and figures. A validator that reimplemented the projection could only prove
    that its own arithmetic agreed with itself.
    """
    global UNDERLAY_MODULE
    if UNDERLAY_MODULE is None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("underlay", ROOT / "underlay.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        UNDERLAY_MODULE = module
    return UNDERLAY_MODULE


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
    underlay = underlay_module()

    library = load(ROOT / "underlay-objects.yaml")
    floor = float(
        library["local_frame_contract"]["legibility"]["minimum_axis_separation_deg"]
    )
    checked = 0
    worst = 180.0
    exempt = 0
    flat_exempt = 0
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
            # An object may declare that it has no readable axis while it lies
            # flat. That is a statement about the object, not a way round the
            # check: fidelity above is already enforced, the exemption dies the
            # moment the object is pitched or picked up, and the count is
            # printed so an exemption can never be silent.
            policy = (library["objects"].get(item["id"]) or {}).get("legibility") or {}
            if policy.get("exempt_when_flat") and measured["pitch_deg"] == 0.0:
                flat_exempt += 1
                continue
            worst = min(worst, measured["separation_deg"])
            if measured["separation_deg"] < floor:
                raise Failure(
                    f"{contract['plate_id']}: the {item['id']} projects only "
                    f"{measured['separation_deg']}deg from collinear, below the "
                    f"{floor}deg floor. The yaw is right and the picture cannot "
                    "show it; raise the camera rather than the yaw"
                )
    return checked, worst, exempt, flat_exempt


# `underlay.render_panel` leaves this much of the drawn extent as floor below
# the lowest thing it frames, so the figures are planted rather than cropped at
# the ankle. It is a literal there and a literal here; the two must move
# together, and `test_composition_guardrails.py` pins them to each other.
FRAME_BOTTOM_MARGIN = 0.10


def panel_composition(contract: dict, panel: dict) -> dict:
    """Measure one panel's drawn composition, in fractions of subject height.

    The subject is what `render_panel` composes the crop around: the sanctuary
    above the floor region, the placed objects, and the figures, plus the strip
    of floor it leaves below them. Every fraction is therefore taken against
    the same span the fit scales into the plate, which makes the numbers
    independent of PANEL_W, PANEL_H and the margin.

    Screen Y runs downward, so "higher in the plate" is a smaller number and a
    band's height is max minus min.
    """
    underlay = underlay_module()
    camera = underlay.Camera(panel)
    predella = float(underlay.sanctuary()["levels"]["predella"])

    def screen(part):
        return [camera.project(point)[:2] for point in part]

    # The sanctuary, split at the predella top into the two bands the
    # composition is argued about. The split is by world height, not by
    # position in the list, so it survives the altar being remassed.
    parts = underlay.altar_geometry()
    floor_region, built = parts[:1], parts[1:]
    step_parts, altar_parts = [], []
    for part in built:
        zs = [point[2] for point in part]
        if max(zs) <= predella + 1e-9:
            step_parts.append(part)
        elif min(zs) >= predella - 1e-9:
            altar_parts.append(part)
        else:
            raise Failure(
                f"{contract['plate_id']}/{panel['id']}: a sanctuary part spans "
                f"z {min(zs):.4f} to {max(zs):.4f}, across the predella top at "
                f"{predella:.4f}; the step band and the altar band are no "
                "longer separable and the composition cannot be measured"
            )
    if not step_parts or not altar_parts:
        raise Failure(
            f"{contract['plate_id']}/{panel['id']}: the sanctuary drew "
            f"{len(step_parts)} step parts and {len(altar_parts)} altar parts; "
            "a plate needs both bands"
        )

    # The framing set, exactly as render_panel builds it: the floor region is
    # drawn but never framed, because a region that runs off the plate would
    # decide the crop for the whole scene.
    # Only the vertical extent matters here: every threshold is a share of
    # height, and the fit's scale is uniform, so the horizontal span cancels.
    engine = underlay.Underlay()
    framing = [point[1] for part in built for point in screen(part)]
    for item in contract["objects"]:
        item_parts = engine.object_parts(item)
        if item_parts:
            framing += [point[1] for part in item_parts for point in screen(part)]

    actors = {}
    for actor in contract["actors"]:
        ys = [
            point[1]
            for part in underlay.mannequin(actor, actor["id"] == "priest")
            for point in screen(part)
        ]
        actors[actor["id"]] = (min(ys), max(ys))
        framing += ys
    if not actors:
        raise Failure(
            f"{contract['plate_id']}/{panel['id']}: no actor to measure against"
        )

    top, feet_line = min(framing), max(framing)
    frame_bottom = feet_line + (feet_line - top) * FRAME_BOTTOM_MARGIN
    subject = frame_bottom - top
    if subject <= 0:
        raise Failure(
            f"{contract['plate_id']}/{panel['id']}: the drawn subject has no "
            "height; nothing can be measured against it"
        )

    def band(band_parts):
        band_ys = [point[1] for part in band_parts for point in screen(part)]
        return (max(band_ys) - min(band_ys)) / subject

    # What makes an altar read as an altar is its superstructure. The altar
    # band alone cannot say so: the body runs from the predella to the mensa
    # and the resolved elevations guarantee it is tall, so that measure passes
    # comfortably even when everything above the mensa has been flattened to a
    # slab. The gradine, tabernacle, reredos, cross and candlesticks are the
    # part that can actually disappear, so they are the part worth measuring.
    mensa_z = float(underlay.sanctuary()["levels"]["mensa"])
    above = [part for part in altar_parts
             if min(point[2] for point in part) >= mensa_z - 1e-9]

    # Floor below the feet means drawn floor, not merely empty crop. Measuring
    # it against the crop alone would have been unfalsifiable: render_panel
    # allows its margin below whatever it frames, so the answer would be that
    # constant for every plate ever drawn. The floor region's naveward edge is
    # what actually decides whether a figure is planted on a floor or standing
    # at the lip of a staircase, so the measurement stops at whichever comes
    # first, the drawn edge or the crop.
    floor_edge = max(point[1] for part in floor_region for point in screen(part))
    lowest_foot = max(bottom for _, bottom in actors.values())
    tallest = max(actors.items(), key=lambda row: row[1][1] - row[1][0])
    return {
        "step_band": band(step_parts),
        "altar_band": band(altar_parts),
        "superstructure_band": band(above) if above else 0.0,
        "floor_below_feet": (min(frame_bottom, floor_edge) - lowest_foot) / subject,
        "actor_height": (tallest[1][1] - tallest[1][0]) / subject,
        "tallest_actor": tallest[0],
        "subject_height": subject,
    }


def check_composition(contracts: list[dict]) -> tuple[int, int, dict]:
    """The plate must read as a sanctuary, not as a staircase wearing an altar.

    Fidelity and legibility say nothing about proportion. A drawing can put
    every object exactly where the contract compiled it, keep every orientation
    readable, and still hand the artistic agent a picture in which the steps
    take two-thirds of the height, the altar is a band across the top, the
    figures are ankle-cropped and the whole thing reads as a flight of stairs.
    That is the plate this check refuses, and the thresholds it refuses it by
    are authored in sanctuary-master.yaml rather than chosen here, so a later
    change has to argue with a number.

    Only perspective panels shot from the nave are measured. A view whose eye
    already stands inside the sanctuary — the over-the-shoulder presets — shows
    neither the full step run nor the floor below the servers' feet by design,
    and holding it to a whole-sanctuary proportion would be demanding that it
    not be itself. Those panels are counted as exempt, never silently skipped.
    """
    master = load(ROOT / "sanctuary-master.yaml")
    limits = master["composition"]
    first_step = float(master["steps"]["first_leading_edge_y"])
    max_step = float(limits["max_step_band_fraction"])
    min_altar = float(limits["min_altar_band_fraction"])
    min_super = float(limits["min_superstructure_band_fraction"])
    min_floor = float(limits["min_floor_below_feet_fraction"])
    min_actor = float(limits["min_actor_height_fraction"])

    checked = 0
    exempt = 0
    worst = {
        "step_band": 0.0,
        "altar_band": 1.0,
        "superstructure_band": 1.0,
        "floor_below_feet": 1.0,
        "actor_height": 1.0,
    }
    for contract in contracts:
        if contract["art_readiness"]["status"] != "ready":
            continue
        plate = contract["plate_id"]
        for panel in contract["panels"]:
            camera = panel["camera"]
            if camera["projection"] != "perspective":
                continue
            if float(camera["position_xyz"][1]) >= first_step:
                exempt += 1
                continue
            checked += 1
            measured = panel_composition(contract, panel)
            where = f"{plate}/{panel['id']}"

            if measured["step_band"] > max_step:
                raise Failure(
                    f"{where}: the steps fill {measured['step_band']:.3f} of "
                    f"the drawn subject height, above the "
                    f"{max_step:.3f} ceiling "
                    "(sanctuary-master.yaml composition."
                    "max_step_band_fraction). The plate reads as a staircase "
                    "with an altar behind it"
                )
            if measured["altar_band"] < min_altar:
                raise Failure(
                    f"{where}: the altar fills only "
                    f"{measured['altar_band']:.3f} of the drawn subject "
                    f"height, below the {min_altar:.3f} floor "
                    "(sanctuary-master.yaml composition."
                    "min_altar_band_fraction). The subject of the plate is the "
                    "altar and it is not being given the plate"
                )
            if measured["superstructure_band"] < min_super:
                raise Failure(
                    f"{where}: everything above the mensa - gradine, "
                    f"tabernacle, reredos, cross and candlesticks - fills only "
                    f"{measured['superstructure_band']:.3f} of the drawn "
                    f"subject height, below the {min_super:.3f} floor "
                    "(sanctuary-master.yaml composition."
                    "min_superstructure_band_fraction). Without its "
                    "superstructure the altar reads as a table"
                )
            if measured["floor_below_feet"] < min_floor:
                raise Failure(
                    f"{where}: only {measured['floor_below_feet']:.3f} of the "
                    f"drawn subject height is floor below the lowest foot, "
                    f"under the {min_floor:.3f} floor (sanctuary-master.yaml "
                    "composition.min_floor_below_feet_fraction). The figures "
                    "stand at the lip of the staircase rather than on a floor"
                )
            if measured["actor_height"] < min_actor:
                raise Failure(
                    f"{where}: the tallest actor "
                    f"({measured['tallest_actor']}) stands "
                    f"{measured['actor_height']:.3f} of the drawn subject "
                    f"height, below the {min_actor:.3f} floor "
                    "(sanctuary-master.yaml composition."
                    "min_actor_height_fraction). The people are too small to "
                    "carry the ceremony the plate is about"
                )

            worst["step_band"] = max(worst["step_band"], measured["step_band"])
            for key in ("altar_band", "superstructure_band",
                        "floor_below_feet", "actor_height"):
                worst[key] = min(worst[key], measured[key])
    return checked, exempt, worst


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
    oriented, worst, side_views, flat_objects = check_projected_orientation(contracts)
    framed, inside_views, proportions = check_composition(contracts)
    soles, in_transit = check_foot_contact(contracts)
    print(
        f"PASS: {soles} soles rest on the level their actor stands on "
        f"({in_transit} more belong to actors in transit)"
    )
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
        f"{side_views} side-elevation scenes and {flat_objects} flat "
        f"unpitched objects exempt by design)"
    )
    print(
        f"PASS: {framed} nave perspective panels hold the authored composition "
        f"(worst step band {proportions['step_band']:.3f}, altar band "
        f"{proportions['altar_band']:.3f}, superstructure "
        f"{proportions['superstructure_band']:.3f}, floor below feet "
        f"{proportions['floor_below_feet']:.3f}, actor height "
        f"{proportions['actor_height']:.3f}; {inside_views} in-sanctuary "
        "panels exempt by design)"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as failure:
        print(f"FAIL: {failure}", file=sys.stderr)
        raise SystemExit(1)
