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
        self.target = list(camera.get("target_xyz") or [0.0, 1.5, 1.0])
        up = [0.0, 0.0, 1.0]

        self.forward = normalise(sub(self.target, self.eye))
        self.right = normalise(cross(self.forward, up))
        self.up = normalise(cross(self.right, self.forward))

        # Framing is fixed per projection so the output is reproducible and the
        # altar fills a comparable share of every plate.
        self.perspective = self.projection in ("perspective", "detail-macro")
        self.focal = 1180.0 if self.projection == "perspective" else 1500.0
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


def place(points, yaw_deg, origin):
    out = []
    for p in points:
        rotated = yaw_rotate(p, yaw_deg if yaw_deg is not None else 90.0)
        out.append(
            [rotated[0] + origin[0], rotated[1] + origin[1], rotated[2] + origin[2]]
        )
    return out


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


def altar_geometry():
    """The full approved altar: three steps, predella, altar body and mensa.

    Drawn as volumes rather than lines so the image model does not have to
    invent how many steps there are or how deep they run.
    """
    parts = []
    # three full altar steps, each rising and receding
    for z, depth_centre, width in (
        (0.0, 0.175, 3.05), (0.25, 0.525, 2.90), (0.50, 0.875, 2.75)
    ):
        parts += box(0.0, depth_centre, z, width, 0.35, 0.25)
    # the predella
    parts += box(0.0, 1.28, 0.75, 2.60, 0.46, 0.25)
    # the altar body, standing on the predella
    parts += box(0.0, 1.60, 1.00, 2.10, 0.34, 0.35)
    # the mensa, oversailing the body
    parts += box(0.0, 1.60, 1.35, 2.34, 0.46, 0.06)
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
    # One body outline. The priest's chasuble falls wider than the servers'
    # cassock and surplice, which is what makes the elevation scenes legible
    # where the servers lift its lower edge.
    # Every actor here wears ankle-length vesture, so the body is a robed
    # column rather than a torso on two sticks. The priest's chasuble falls
    # wider than a server's cassock and surplice, which is what makes the
    # elevation scenes legible where the servers lift its lower edge.
    flare = 0.15 if is_priest else 0.06
    hem_z = 0.02 if not kneeling else hip_z - 0.30
    hem = hip / 2 + flare + (0.05 if not kneeling else 0.0)
    parts.append([
        [-shoulder / 2, lean, shoulder_z],
        [-hem, lean * 0.35, hem_z],
        [hem, lean * 0.35, hem_z],
        [shoulder / 2, lean, shoulder_z],
        [-shoulder / 2, lean, shoulder_z],
    ])
    parts.append([[-hem, lean * 0.35, hem_z], [hem, lean * 0.35, hem_z]])
    # shoulder line, which is what makes facing readable
    parts.append([[-shoulder / 2, lean, shoulder_z], [shoulder / 2, lean, shoulder_z]])
    # head
    neck_z = shoulder_z + 0.06
    head_z = neck_z + head_r
    ring = []
    for step in range(13):
        a = 2 * math.pi * step / 12
        ring.append([head_r * math.cos(a), lean * 1.25, head_z + head_r * math.sin(a)])
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
    elif genuflect:
        parts.append([[-hem, lean * 0.35, hem_z], [-hem - 0.04, -0.20, 0.0], [0.04, -0.20, 0.0]])
        parts.append([[hem, lean * 0.35, hem_z], [hem, 0.10, 0.24]])
    else:
        # a hint of feet below the hem, so the figure is planted
        parts.append([[-0.10, -0.03, hem_z], [-0.12, -0.12, 0.0]])
        parts.append([[0.10, -0.03, hem_z], [0.12, -0.12, 0.0]])

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
        return [place(part["points"] + ([part["points"][0]] if part.get("closed") else []),
                      yaw, origin)
                for part in variant["parts"]]

    def render_panel(self, contract: dict, panel: dict) -> str:
        camera = Camera(panel)
        drawable = []  # (depth, css class, projected points)

        def add(parts, css):
            for part in parts:
                projected = [camera.project(p) for p in part]
                if not projected:
                    continue
                depth = sum(p[2] for p in projected) / len(projected)
                drawable.append((depth, css, [(p[0], p[1]) for p in projected]))

        add(altar_geometry(), "arch")
        for item in contract["objects"]:
            parts = self.object_parts(item)
            if parts:
                add(parts, "g")
        for actor in contract["actors"]:
            add(mannequin(actor, actor["id"] == "priest"), "fig")

        # Fit the whole scene into the panel with a fixed margin. Deterministic:
        # the same contract always yields the same frame.
        margin = 46.0
        xs = [x for _, _, pts in drawable for x, _ in pts]
        ys = [y for _, _, pts in drawable for _, y in pts]
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
