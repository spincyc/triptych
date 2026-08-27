#!/usr/bin/env python3
"""Generate deterministic render underlays from compiled render contracts.

The diagnostic skeleton is a coordinate schematic: it draws every object as the
same small square and lets a text label carry the meaning. That is right for
verification and wrong as visual conditioning — an image model working from it
must decide for itself which anonymous square was the open book, and in the
failed canary it decided wrongly.

The underlay is the answer: a projected line drawing in which the geometry
itself carries the meaning. An open Missal is a spread of two page planes with a
spine; a burse is a flat closed case; a chalice is a cup on a stem. A viewer who
reads no labels can name each one, and can see which side of the altar the book
stands on.

It is projected through the contract's own declared camera, so the compiled yaw
is embodied by the drawing rather than annotated beside it.

Usage:
    ./underlay.py --scene LM-001A --out DIR   # one scene, SVG and PNG
    ./underlay.py                             # every art-ready scene
    ./underlay.py --check                     # fail if tracked output is stale
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
CONTRACTS = ROOT / "contracts"
OUT = ROOT / "underlays"

# Fixed output geometry. The panel contract owns how many panels exist; this
# owns how large each one is, so the raster is reproducible.
PANEL_W, PANEL_H = 1024, 768
RASTER_SCALE = 2

# A neutral technical line style. No fill, no texture, no text: the conditioning
# raster must not depend on a font, and must carry no instruction a model could
# read instead of seeing.
STYLE = (
    "svg{background:#fff}"
    ".g{fill:none;stroke:#111;stroke-width:2.8;stroke-linejoin:round;"
    "stroke-linecap:round}"
    ".arch{fill:none;stroke:#111;stroke-width:2.0;stroke-linejoin:round}"
    ".fig{fill:none;stroke:#111;stroke-width:2.4;stroke-linejoin:round;"
    "stroke-linecap:round}"
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


# --------------------------------------------------------------------------
# projection
# --------------------------------------------------------------------------
def normalise(v):
    length = math.sqrt(sum(c * c for c in v)) or 1.0
    return [c / length for c in v]


def cross(a, b):
    return [
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    ]


def sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


class Camera:
    """A camera built from the contract's own declared fields.

    Nothing here is chosen by the underlay: projection, station point, target
    and up all come from the compiled panel, so the drawing cannot disagree
    with the contract about what is being looked at.
    """

    def __init__(self, panel: dict) -> None:
        camera = panel["camera"]
        self.projection = camera["projection"]
        self.eye = list(camera["position_xyz"])
        self.target = list(camera.get("target_xyz") or [0.0, 1.5, 1.42])
        up = [0.0, 0.0, 1.0]

        self.forward = normalise(sub(self.target, self.eye))
        self.right = normalise(cross(self.forward, up))
        self.up = normalise(cross(self.right, self.forward))

        # Framing is fixed per projection so the output is reproducible and the
        # altar fills a comparable share of every plate.
        self.perspective = self.projection in ("perspective", "detail-macro")
        # The preset owns its lens. A renderer that picks its own focal
        # length is choosing the composition the contract meant to fix.
        declared = camera.get("focal_length_px")
        default = 1520.0 if self.projection == "perspective" else 1500.0
        self.focal = float(declared) if declared else default
        # How close a thing may be and still be in shot. Only a station point
        # inside the sanctuary ever has anything nearer than this.
        self.near = 0.55 if self.perspective else -1e9
        self.ortho_scale = 250.0
        self.plan = self.projection == "orthographic-plan"

    def project(self, point):
        """World point to raw (x, y, depth), before the panel fits the frame.

        Fitting happens once per panel over all the geometry, so framing is
        derived from the scene rather than guessed, and nothing falls off the
        edge of a plate.
        """
        rel = sub(point, self.eye)
        x = dot(rel, self.right)
        y = dot(rel, self.up)
        depth = dot(rel, self.forward)
        if self.perspective:
            if depth <= 0.05:
                depth = 0.05
            scale = self.focal / depth
            return x * scale, -y * scale, depth
        return x * self.ortho_scale, -y * self.ortho_scale, depth


def yaw_rotate(point, yaw_deg):
    angle = math.radians(yaw_deg - 90.0)  # local +Y aligns with the object yaw
    c, s = math.cos(angle), math.sin(angle)
    x, y, z = point
    return [x * c - y * s, x * s + y * c, z]


def pitch_rotate(point, pitch_deg):
    """Tilt about the object's own spread axis, local +X.

    A Missal on an altar stand is inclined toward the priest: its far edge
    rises and its page plane turns to face him. Modelling the book flat and
    then raising the camera until the flat thing became readable was solving
    the wrong problem, so pitch lives here, in the object, where it belongs.

    Positive pitch lifts local +Y, the page-up axis, and swings the page
    normal from straight up toward the reader.
    """
    if not pitch_deg:
        return list(point)
    angle = math.radians(pitch_deg)
    c, s = math.cos(angle), math.sin(angle)
    x, y, z = point
    return [x, y * c - z * s, y * s + z * c]


def place(points, yaw_deg, origin, pitch_deg=0.0):
    """Local geometry to world: pitch about local X, then yaw about Z, then move.

    The order matters and is the repository convention: pitch is a property of
    how the object sits on its support, so it applies in the object's own
    frame, before the world yaw turns that support to face where it faces.
    """
    out = []
    for p in points:
        tilted = pitch_rotate(p, pitch_deg)
        rotated = yaw_rotate(tilted, yaw_deg if yaw_deg is not None else 90.0)
        out.append(
            [rotated[0] + origin[0], rotated[1] + origin[1], rotated[2] + origin[2]]
        )
    return out


def world_axis(local_axis, yaw_deg, pitch_deg=0.0):
    """A local direction carried through pitch and yaw into world space."""
    v = yaw_rotate(pitch_rotate(local_axis, pitch_deg), yaw_deg)
    length = math.sqrt(sum(c * c for c in v)) or 1.0
    return [round(c / length, 6) for c in v]


# --------------------------------------------------------------------------
# the sanctuary
# --------------------------------------------------------------------------
def box(cx, cy, cz, dx, dy, dz):
    """Axis-aligned box as a list of edge polylines."""
    x0, x1 = cx - dx / 2, cx + dx / 2
    y0, y1 = cy - dy / 2, cy + dy / 2
    z0, z1 = cz, cz + dz
    corners = {
        "a": [x0, y0, z0], "b": [x1, y0, z0], "c": [x1, y1, z0], "d": [x0, y1, z0],
        "e": [x0, y0, z1], "f": [x1, y0, z1], "g": [x1, y1, z1], "h": [x0, y1, z1],
    }
    k = corners
    return [
        [k["a"], k["b"], k["c"], k["d"], k["a"]],
        [k["e"], k["f"], k["g"], k["h"], k["e"]],
        [k["a"], k["e"]], [k["b"], k["f"]], [k["c"], k["g"]], [k["d"], k["h"]],
    ]


def step(cy, z, width, depth, rise):
    """One altar step, drawn as the faces a viewer in the nave actually sees.

    Full boxes gave every step a back edge and a hidden underside, and three of
    them stacked read as a flight of hollow crates rather than as the base of
    an altar. A step shows its riser and its tread; that is all it owes the
    drawing.
    """
    y0, y1 = cy - depth / 2, cy + depth / 2
    x0, x1 = -width / 2, width / 2
    return [
        [[x0, y0, z], [x1, y0, z], [x1, y0, z + rise], [x0, y0, z + rise], [x0, y0, z]],
        [[x0, y0, z + rise], [x0, y1, z + rise], [x1, y1, z + rise], [x1, y0, z + rise]],
    ]


SANCTUARY = None


def sanctuary():
    """The canonical sanctuary master, loaded once."""
    global SANCTUARY
    if SANCTUARY is None:
        SANCTUARY = load(ROOT / "sanctuary-master.yaml")
    return SANCTUARY


def altar_geometry():
    """The canonical sanctuary: floor, three steps, predella, and a massed altar.

    Built from sanctuary-master.yaml so every scene projects against the same
    thing. Which levels exist and in what order is structural; how tall each
    one is, how deep a tread runs, how far the first step stands back, and how
    the altar is massed above its mensa are all resolved there, because the
    structural values are ordinals rather than measurements.
    """
    m = sanctuary()
    lv = m["levels"]
    parts = []

    # The floor the actors stand on, drawn as a real region so that standing in
    # plano is visible rather than merely asserted.
    plano = m["in_plano"]
    half = plano["width"] / 2
    parts.append([
        [-half, plano["naveward_edge"], 0.0],
        [half, plano["naveward_edge"], 0.0],
        [half, plano["altarward_edge"], 0.0],
        [-half, plano["altarward_edge"], 0.0],
        [-half, plano["naveward_edge"], 0.0],
    ])

    # Three steps, set back from the actors, each drawn as riser and tread.
    st = m["steps"]
    y = st["first_leading_edge_y"]
    for index, width in enumerate(st["widths"]):
        z = lv["floor"] if index == 0 else lv[f"step_{index}"]
        rise = lv[f"step_{index + 1}"] - z
        parts += step(y + st["tread_depth"] / 2, z, width, st["tread_depth"], rise)
        y += st["tread_depth"]

    pr = m["predella"]
    parts += step(
        pr["leading_edge_y"] + pr["depth"] / 2, lv["step_3"], pr["width"],
        pr["depth"], lv["predella"] - lv["step_3"],
    )

    a = m["altar"]
    b = a["body"]
    parts += box(0.0, b["front_y"] + b["depth"] / 2, b["from_z"],
                 b["width"], b["depth"], b["to_z"] - b["from_z"])
    ms = a["mensa"]
    parts += box(0.0, b["front_y"] + b["depth"] / 2, lv["mensa"],
                 ms["width"], ms["depth"], ms["thickness"])

    # The altar's mass lives above the mensa, because below it the structural
    # frame allows only 0.35 against a mensa 2.34 wide.
    g = a["gradine"]
    parts += box(0.0, b["front_y"] + b["depth"] - 0.02, g["from_z"],
                 g["width"], g["depth"], g["to_z"] - g["from_z"])
    tb = a["tabernacle"]
    parts += box(0.0, b["front_y"] + b["depth"] - 0.04, tb["from_z"],
                 tb["width"], tb["depth"], tb["to_z"] - tb["from_z"])
    inset = tb["door_inset"]
    face = b["front_y"] + b["depth"] - 0.04 - tb["depth"] / 2
    parts.append([
        [-tb["width"] / 2 + inset, face, tb["from_z"] + inset],
        [tb["width"] / 2 - inset, face, tb["from_z"] + inset],
        [tb["width"] / 2 - inset, face, tb["to_z"] - inset],
        [-tb["width"] / 2 + inset, face, tb["to_z"] - inset],
        [-tb["width"] / 2 + inset, face, tb["from_z"] + inset],
    ])
    rd = a["reredos_hint"]
    parts += box(0.0, b["front_y"] + b["depth"] + 0.02, rd["from_z"],
                 rd["width"], 0.12, rd["to_z"] - rd["from_z"])

    # The cross and the standing candlesticks. Without them the modelled mass
    # is a cupboard on a slab; with them it is unmistakably an altar, and an
    # image editor cannot put the cross somewhere else.
    fx = m["fixed_anchors"]
    cross = fx["altar_cross"]
    shaft = 0.55
    arm = 0.20
    foot_z = cross[2]
    parts.append([[cross[0], cross[1], foot_z], [cross[0], cross[1], foot_z + shaft]])
    bar_z = foot_z + shaft * 0.66
    parts.append([[cross[0] - arm, cross[1], bar_z], [cross[0] + arm, cross[1], bar_z]])
    parts += box(cross[0], cross[1], foot_z, 0.16, 0.10, 0.06)
    for cx, cy, cz in fx["candlesticks"]:
        parts += box(cx, cy, cz, 0.09, 0.09, 0.06)            # foot
        parts.append([[cx, cy, cz + 0.06], [cx, cy, cz + 0.34]])   # stem
        parts += box(cx, cy, cz + 0.34, 0.07, 0.07, 0.05)     # bowl
        parts.append([[cx, cy, cz + 0.39], [cx, cy, cz + 0.58]])   # candle
    return parts


# --------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------
def mannequin(actor: dict, is_priest: bool):
    """A body envelope: head, shoulders, torso, and a base set by posture.

    Not anatomy. Blocking geometry, so a later model sees three people standing
    in exact places rather than three labelled circles, and can see which way
    each one faces.
    """
    posture = actor["posture"]
    bow = actor["bow"]
    yaw = actor["body_facing_yaw_deg"]

    shoulder = 0.30 if is_priest else 0.24
    hip = 0.26 if is_priest else 0.20
    head_r = 0.085

    kneeling = posture in ("kneeling", "kneeling-erect")
    genuflect = posture == "genuflecting"
    if kneeling:
        hip_z, shoulder_z = 0.42, 0.95
    elif genuflect:
        hip_z, shoulder_z = 0.55, 1.10
    else:
        hip_z, shoulder_z = 0.92, 1.42

    lean = {
        "none": 0.0, "head-slight": 0.02, "head-moderate": 0.04,
        "head-profound": 0.06, "body-medium": 0.16, "body-profound": 0.26,
    }.get(bow, 0.0)
    if posture in ("bowing-low-over-altar", "stooping"):
        lean = max(lean, 0.30)

    parts = []
    # A robed column, but a column with a waist, a hem and feet. The earlier
    # envelope tapered in one straight line from shoulder to a hem more than
    # twice the shoulder width, which draws a cone, not a vested man. The hem
    # is now held near shoulder width, and the alb, the cincture and the feet
    # are drawn separately so an illustrator can see where the body is inside
    # the vesture instead of guessing it.
    hem_z = 0.02 if not kneeling else hip_z - 0.30
    hem = (0.22 if is_priest else 0.15) if not kneeling else (0.24 if is_priest else 0.17)
    waist_z = hip_z + 0.06
    waist = hip / 2 + 0.02

    # The body has thickness. Drawn as a single flat outline it disappeared
    # whenever an actor faced along the view axis - a server turned gospelward
    # rendered as a vertical spike - because a cut-out seen edge-on has no
    # width. Two outlines a body-depth apart, tied together, give a figure that
    # reads from any yaw and tells an illustrator where the body actually is.
    depth = 0.20 if is_priest else 0.17

    def column(dy):
        return [
            [-shoulder / 2, lean + dy, shoulder_z],
            [-waist, lean * 0.6 + dy, waist_z],
            [-hem, lean * 0.35 + dy, hem_z],
            [hem, lean * 0.35 + dy, hem_z],
            [waist, lean * 0.6 + dy, waist_z],
            [shoulder / 2, lean + dy, shoulder_z],
            [-shoulder / 2, lean + dy, shoulder_z],
        ]

    for dy in (-depth / 2, depth / 2):
        parts.append(column(dy))
    for sx in (-1, 1):
        for z, half, spread in ((shoulder_z, shoulder / 2, 1.0),
                                (waist_z, waist, 0.6),
                                (hem_z, hem, 0.35)):
            parts.append([
                [sx * half, lean * spread - depth / 2, z],
                [sx * half, lean * spread + depth / 2, z],
            ])
    # the hem line, so the vesture reads as ending rather than fading out
    parts.append([[-hem, lean * 0.35, hem_z], [hem, lean * 0.35, hem_z]])
    # the cincture, which is where a viewer reads the waist and so the height
    parts.append([[-waist, lean * 0.6, waist_z], [waist, lean * 0.6, waist_z]])
    # shoulder line, which is what makes facing readable
    parts.append([[-shoulder / 2, lean, shoulder_z], [shoulder / 2, lean, shoulder_z]])
    if is_priest and not kneeling:
        # The chasuble: a shorter, wider over-garment falling to about the
        # knee. This, not a flared hem, is what distinguishes the priest.
        cz = hip_z - 0.16
        cw = shoulder / 2 + 0.17
        parts.append([
            [-shoulder / 2 - 0.02, lean, shoulder_z - 0.02],
            [-cw, lean * 0.5, cz],
            [cw, lean * 0.5, cz],
            [shoulder / 2 + 0.02, lean, shoulder_z - 0.02],
        ])
        parts.append([[-cw, lean * 0.5, cz], [cw, lean * 0.5, cz]])
    # head
    neck_z = shoulder_z + 0.06
    head_z = neck_z + head_r
    for plane in ("frontal", "sagittal"):
        ring = []
        for step in range(13):
            a = 2 * math.pi * step / 12
            c, s = head_r * math.cos(a), head_r * math.sin(a)
            if plane == "frontal":
                ring.append([c, lean * 1.25, head_z + s])
            else:
                ring.append([0.0, lean * 1.25 + c, head_z + s])
        parts.append(ring)
    parts.append([[0.0, lean, shoulder_z], [0.0, lean * 1.25, neck_z]])
    # a short nose-line so head facing is unambiguous
    parts.append([[0.0, lean * 1.25, head_z], [0.0, lean * 1.25 - 0.10, head_z - 0.01]])

    # base: how the robed column meets the floor tells the posture apart
    if kneeling:
        parts.append([
            [-hem, lean * 0.35, hem_z], [-hem - 0.02, -0.14, 0.0],
            [hem + 0.02, -0.14, 0.0], [hem, lean * 0.35, hem_z],
        ])
        parts.append([[-hem - 0.02, -0.14, 0.0], [hem + 0.02, -0.14, 0.0]])
        # Knees and toes, flat on the level. A kneeling figure met the floor
        # only through the fall of its cassock, which draws a shape resting on
        # nothing; these are the patches that actually bear the weight.
        for side in (-1, 1):
            kx = side * 0.085
            parts.append([
                [kx - 0.05, -0.02, 0.0], [kx + 0.05, -0.02, 0.0],
                [kx + 0.05, 0.10, 0.0], [kx - 0.05, 0.10, 0.0],
                [kx - 0.05, -0.02, 0.0],
            ])
            # Toes tucked under, not stretched back: kneeling erect the shin is
            # near vertical, so the foot's footprint sits close behind the knee
            # and stays on the same tread.
            parts.append([
                [kx - 0.04, -0.14, 0.0], [kx + 0.04, -0.14, 0.0],
                [kx + 0.04, -0.06, 0.0], [kx - 0.04, -0.06, 0.0],
                [kx - 0.04, -0.14, 0.0],
            ])
    elif genuflect:
        parts.append([[-hem, lean * 0.35, hem_z], [-hem - 0.04, -0.20, 0.0], [0.04, -0.20, 0.0]])
        parts.append([[hem, lean * 0.35, hem_z], [hem, 0.10, 0.24]])
        # The down knee and the standing foot: a genuflection rests on both.
        parts.append([
            [-0.13, -0.05, 0.0], [-0.03, -0.05, 0.0],
            [-0.03, 0.07, 0.0], [-0.13, 0.07, 0.0], [-0.13, -0.05, 0.0],
        ])
        parts.append([
            [0.03, -0.14, 0.0], [0.12, -0.14, 0.0],
            [0.12, 0.05, 0.0], [0.03, 0.05, 0.0], [0.03, -0.14, 0.0],
        ])
    else:
        # Two feet, flat on the plane the actor stands on and wholly within it.
        # A figure whose feet are a pair of ticks floats; a figure with soles
        # is planted, and a validator can check that the soles are on a level.
        for side in (-1, 1):
            tx = side * 0.075
            # A tapered sole: narrow at the heel, wider across the ball, and
            # turned very slightly outward as a standing foot is. Drawn as a
            # plain rectangle it read as a flat plate under the hem rather
            # than as a foot.
            splay = side * 0.012
            parts.append([
                [tx - 0.030, -0.150, 0.0],
                [tx + 0.030, -0.150, 0.0],
                [tx + 0.048 + splay, -0.020, 0.0],
                [tx + 0.040 + splay, 0.048, 0.0],
                [tx - 0.036 + splay, 0.048, 0.0],
                [tx - 0.046 + splay, -0.020, 0.0],
                [tx - 0.030, -0.150, 0.0],
            ])
            # ankle, joining the sole to the hem
            parts.append([[tx, -0.02, 0.0], [tx, lean * 0.35, hem_z]])

    # arms, placed by hand-state class rather than drawn in detail
    hands = actor["hands"]
    joined = hands.get("joined") or hands["left"].startswith("joined")
    hand_z = shoulder_z - 0.30
    hand_y = lean - 0.17
    for side in (-1, 1):
        state = hands["left"] if side < 0 else hands["right"]
        elbow = [side * (shoulder / 2 + 0.06), lean - 0.04, shoulder_z - 0.22]
        if "lifting" in state or "raising" in state:
            hand = [side * (shoulder / 2 + 0.20), lean + 0.05, shoulder_z - 0.26]
        elif state.startswith("extended") or state == "elevated":
            hand = [side * (shoulder / 2 + 0.20), lean - 0.20, shoulder_z + 0.06]
        elif joined:
            hand = [side * 0.05, hand_y, hand_z]
        else:
            hand = [side * 0.14, hand_y, hand_z]
        parts.append([[side * shoulder / 2, lean, shoulder_z - 0.02], elbow, hand])
    if joined:
        parts.append([[-0.05, hand_y, hand_z], [0.05, hand_y, hand_z]])

    origin = actor["position"]
    return [place(part, yaw, origin) for part in parts]


def round6(value: float) -> float:
    return round(float(value), 6)


def level_of(z: float) -> str | None:
    """Name the sanctuary level an elevation stands on, if it is one."""
    for name, value in sanctuary()["levels"].items():
        if isinstance(value, (int, float)) and abs(value - z) < 1e-6:
            return name
    return None


def foot_contacts(actor: dict, is_priest: bool) -> dict:
    """Where this actor's soles meet the sanctuary, and on what.

    A figure is planted or it floats, and the difference is checkable: every
    sole must lie flat on the level the actor was placed on, and must not
    overhang the tread it stands on into the riser in front of it.
    """
    origin = actor["position"]
    stands_on = level_of(origin[2])
    soles = []
    for part in mannequin(actor, is_priest):
        zs = [p[2] for p in part]
        if len(part) < 4 or max(zs) - min(zs) > 1e-6:
            continue  # not a flat sole
        if abs(zs[0] - origin[2]) > 1e-6:
            continue
        soles.append({
            "z": round6(zs[0]),
            "y_min": round6(min(p[1] for p in part)),
            "y_max": round6(max(p[1] for p in part)),
            "x_min": round6(min(p[0] for p in part)),
            "x_max": round6(max(p[0] for p in part)),
        })
    m = sanctuary()
    st = m["steps"]
    edges = [st["first_leading_edge_y"] + index * st["tread_depth"]
             for index in range(st["count"])]
    edges.append(m["predella"]["leading_edge_y"])
    return {
        "actor": actor["id"],
        "stands_on": stands_on,
        "level_z": round6(origin[2]),
        "soles": soles,
        "riser_leading_edges": [round6(e) for e in edges],
    }


# --------------------------------------------------------------------------
# scene assembly
# --------------------------------------------------------------------------
class Underlay:
    def __init__(self) -> None:
        self.library = load(ROOT / "underlay-objects.yaml")["objects"]

    def object_parts(self, item: dict):
        """Recognizable geometry for one compiled object, or None."""
        definition = self.library.get(item["id"])
        if not definition or item.get("position") is None:
            return None
        variants = definition["variants"]
        wanted = "default"
        state = str(item.get("state_after") or "").lower()
        placement = str(item.get("placement_semantic") or "").lower()
        if item["id"] == "missal":
            wanted = "closed" if "closed" in state else "open"
        elif "veil" in state and "veiled" in (definition.get("variants_extra") or {}):
            variants = definition["variants_extra"]
            wanted = "veiled"
        del placement
        variant = variants.get(wanted) or variants.get("default") or next(iter(variants.values()))
        if variant.get("alias_of"):
            variant = variants[variant["alias_of"]]
        yaw = item.get("yaw_deg")
        origin = item["position"]
        pitch = self.support_pitch(item["id"], wanted)
        return [place(part["points"] + ([part["points"][0]] if part.get("closed") else []),
                      yaw, origin, pitch)
                for part in variant["parts"]]

    def support_pitch(self, object_id: str, variant: str = "default") -> float:
        """The inclination this object sits at, resolved through its support.

        A book on a stand inherits the stand's support-plane pitch rather than
        declaring its own, so the two cannot drift apart. A book being carried
        is not on a stand and is not pitched by one.
        """
        definition = self.library.get(object_id) or {}
        support = definition.get("support") or {}
        states = support.get("states") or {}
        state = states.get(variant, states.get("default"))
        if state is not None and not state.get("supported", True):
            return 0.0
        parent_id = support.get("supported_by")
        if parent_id:
            parent = self.library.get(parent_id) or {}
            return float((parent.get("support") or {}).get("pitch_deg", 0.0))
        return float(support.get("pitch_deg", 0.0))

    def render_panel(self, contract: dict, panel: dict) -> str:
        camera = Camera(panel)
        drawable = []  # (depth, css class, projected points)

        framing = []  # the subject the crop is composed around

        def add(parts, css, frames=True):
            for part in parts:
                projected = [camera.project(p) for p in part]
                if not projected:
                    continue
                # Near-plane rejection. `project` clamps depth rather than
                # clipping, so a point just in front of the eye projects to an
                # enormous coordinate instead of disappearing. From the nave
                # nothing is ever that close and this changes nothing; from the
                # over-the-shoulder station the floor behind the camera and the
                # top of the reredos were being flung across the plate as two
                # diverging funnels, and the fit then zoomed out to contain
                # them. A part any of whose points is nearer than this is out
                # of shot, which is what a real close view does too.
                if min(p[2] for p in projected) < camera.near:
                    continue
                depth = sum(p[2] for p in projected) / len(projected)
                flat = [(p[0], p[1]) for p in projected]
                drawable.append((depth, css, flat))
                if frames:
                    framing.extend(flat)

        sanctuary_parts = altar_geometry()
        add(sanctuary_parts[:1], "arch", frames=False)   # the floor region
        add(sanctuary_parts[1:], "arch")
        for item in contract["objects"]:
            parts = self.object_parts(item)
            if parts:
                add(parts, "g")
        for actor in contract["actors"]:
            add(mannequin(actor, actor["id"] == "priest"), "fig")

        # Fit the whole scene into the panel with a fixed margin. Deterministic:
        # the same contract always yields the same frame.
        margin = 46.0
        xs = [x for x, _ in framing] or [x for _, _, pts in drawable for x, _ in pts]
        ys = [y for _, y in framing] or [y for _, _, pts in drawable for _, y in pts]
        # Leave a little floor below the feet so the figures are planted rather
        # than cropped at the ankle.
        ys.append(max(ys) + (max(ys) - min(ys)) * 0.10)
        if not xs:
            return ""
        span_x = max(xs) - min(xs) or 1.0
        span_y = max(ys) - min(ys) or 1.0
        scale = min((PANEL_W - 2 * margin) / span_x, (PANEL_H - 2 * margin) / span_y)
        offset_x = (PANEL_W - span_x * scale) / 2 - min(xs) * scale
        offset_y = (PANEL_H - span_y * scale) / 2 - min(ys) * scale

        # painter's algorithm: far things first
        drawable.sort(key=lambda row: -row[0])
        out = []
        for _, css, points in drawable:
            path = " ".join(
                ("M" if i == 0 else "L")
                + f"{x * scale + offset_x:.2f},{y * scale + offset_y:.2f}"
                for i, (x, y) in enumerate(points)
            )
            out.append(f'<path class="{css}" d="{path}"/>')
        return "\n".join(out)

    def render(self, contract: dict) -> str:
        panels = contract["panels"]
        width = PANEL_W * len(panels)
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
            f'height="{PANEL_H}" viewBox="0 0 {width} {PANEL_H}">',
            f'<rect width="100%" height="100%" fill="#ffffff"/>',
            f"<style>{STYLE}</style>",
            # Scene identity as non-rendered metadata only. Nothing in the
            # raster is text: the geometry has to carry the meaning.
            f"<!-- plate {contract['plate_id']} panels "
            f"{','.join(p['id'] for p in panels)} "
            f"baseline {contract['structural_baseline_commit']} -->",
        ]
        for index, panel in enumerate(panels):
            parts.append(f'<g transform="translate({index * PANEL_W},0)">')
            parts.append(self.render_panel(contract, panel))
            parts.append("</g>")
        parts.append("</svg>")
        return "\n".join(parts) + "\n"


def projected_orientation(contract: dict, object_id: str, panel_index: int = 0):
    """What an oriented object's local axes actually become on the page.

    This is the measurement the earlier checks were missing. Everything before
    it asked whether the world-space yaw was right, and the yaw was right; the
    picture was still unreadable, because an orientation that survives the
    transform can still die in the projection. Two axes of a flat object seen
    at a grazing angle collapse toward collinear, and once they do the object
    cannot look oriented at any yaw at all.

    Returns None when the object is absent or unoriented, otherwise:
      page_up_deg      the drawn page-up direction, in page degrees
      expected_deg     where the contract's own world page-up vector projects
      fidelity_deg     the disagreement between them
      separation_deg   how far the two principal axes are from collinear,
                       0 being a flat smear and 90 an ideal open corner
    """
    item = next((o for o in contract["objects"] if o["id"] == object_id), None)
    if item is None or item.get("position") is None or item.get("yaw_deg") is None:
        return None
    engine = Underlay()
    library = engine.library.get(object_id) or {}
    frame = library.get("local_frame") or {}
    page_up = frame.get("page_up_axis", [0.0, 1.0, 0.0])
    spread = frame.get("spread_axis", [1.0, 0.0, 0.0])
    normal = frame.get("page_normal", [0.0, 0.0, 1.0])

    state = str(item.get("state_after") or "").lower()
    variant = "carried" if "carried" in state or "hand" in str(
        item.get("placement_semantic") or ""
    ).lower() else ("closed" if "closed" in state else "open")
    pitch = engine.support_pitch(object_id, variant)

    camera = Camera(contract["panels"][panel_index])
    origin, yaw = item["position"], item["yaw_deg"]

    def page_angle(local_a, local_b):
        a = camera.project(place([local_a], yaw, origin, pitch)[0])
        b = camera.project(place([local_b], yaw, origin, pitch)[0])
        return math.degrees(math.atan2(-(b[1] - a[1]), b[0] - a[0]))

    reach = 0.18
    drawn = page_angle([-v * reach for v in page_up], [v * reach for v in page_up])
    across = page_angle([-v * reach for v in spread], [v * reach for v in spread])

    # How much of the page face actually reaches the page. A flat book seen
    # edge-on projects its spread to a sliver however faithful its yaw is, and
    # the area is what notices.
    corners = [
        place([[sx * 0.20, sy * 0.15, 0.0]], yaw, origin, pitch)[0]
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    ]
    flat = [camera.project(c) for c in corners]
    area = abs(sum(
        flat[i][0] * flat[(i + 1) % 4][1] - flat[(i + 1) % 4][0] * flat[i][1]
        for i in range(4)
    )) / 2.0

    reading = item.get("reading", {})
    # Compare the drawn axis against the PITCHED contract vector. The flat
    # `page_up_vector` states the approved reading orientation and is the thing
    # that must never mirror; it is not where the physical page-up points once
    # the book lies on its stand. Comparing the drawn axis to the flat one
    # would report a fault that is really just the pitch doing its job.
    world = reading.get("page_up_vector_pitched") or reading.get("page_up_vector")
    if pitch == 0.0:
        world = reading.get("page_up_vector") or world
    if world is None:
        # No published vector, so the expectation is built from the contract's
        # own yaw AND the support pitch it declares. Building it from the yaw
        # alone silently exempted every pitched object that does not publish a
        # vector: the drawing applied the pitch, the expectation did not, and
        # the difference was reported as the model failing to embody its
        # transform. The pitch is part of the transform.
        world = world_axis(page_up, yaw, pitch)
    here = camera.project(origin)
    there = camera.project([
        origin[0] + world[0] * reach,
        origin[1] + world[1] * reach,
        origin[2] + world[2] * reach,
    ])
    expected = math.degrees(math.atan2(-(there[1] - here[1]), there[0] - here[0]))

    gap = abs((drawn - across + 180.0) % 360.0 - 180.0)
    return {
        "pitch_deg": round(pitch, 4),
        "world_page_normal": world_axis(normal, yaw, pitch),
        "world_page_up": world_axis(page_up, yaw, pitch),
        "page_area_px": round(area, 2),
        "page_up_deg": round(drawn, 4),
        "expected_deg": round(expected, 4),
        "fidelity_deg": round(abs((drawn - expected + 180.0) % 360.0 - 180.0), 4),
        "separation_deg": round(min(gap, 180.0 - gap), 4),
    }


def rasterize(svg_path: Path, png_path: Path) -> None:
    subprocess.run(
        ["rsvg-convert", "--zoom", str(RASTER_SCALE),
         str(svg_path), "-o", str(png_path)],
        check=True, capture_output=True,
    )


def write(contract: dict, out: Path) -> tuple[Path, Path]:
    out.mkdir(parents=True, exist_ok=True)
    svg_path = out / "render-underlay.svg"
    png_path = out / "render-underlay.png"
    svg_path.write_text(Underlay().render(contract), encoding="utf-8")
    rasterize(svg_path, png_path)
    return svg_path, png_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.scene:
        contract = load(CONTRACTS / f"{args.scene}.yaml")
        svg_path, png_path = write(contract, args.out or (OUT / args.scene))
        print(f"wrote {svg_path.name} and {png_path.name}")
        return 0

    engine = Underlay()
    stale = []
    count = 0
    for path in sorted(CONTRACTS.glob("*.yaml")):
        contract = load(path)
        if contract["art_readiness"]["status"] != "ready":
            continue
        count += 1
        svg = engine.render(contract)
        target = OUT / contract["plate_id"] / "render-underlay.svg"
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != svg:
                stale.append(contract["plate_id"])
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(svg, encoding="utf-8")
    if args.check:
        if stale:
            print("stale underlays: " + ", ".join(stale[:8]), file=sys.stderr)
            return 1
        print(f"PASS: {count} art-ready underlays are current")
        return 0
    print(f"wrote {count} underlay drawings "
          "(rasters are produced on demand by art-seed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
