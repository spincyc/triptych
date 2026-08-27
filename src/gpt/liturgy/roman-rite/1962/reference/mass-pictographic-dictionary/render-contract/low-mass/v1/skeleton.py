#!/usr/bin/env python3
"""Generate deterministic skeleton SVGs from compiled render contracts.

A skeleton is not a drawing. It is the geometric truth a later artistic plate
must preserve: where every figure stands, which way each faces, where every
object sits and how it is turned, which paths are walked, and exactly which
panels exist.

The art generator may beautify a skeleton. It may not restage one.

Usage:
    ./skeleton.py                 # write skeletons/ for every scene
    ./skeleton.py --check         # fail if the tracked output is stale
    ./skeleton.py --scene LM-001A # write or print one
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parent
CONTRACTS = ROOT / "contracts"
OUT = ROOT / "skeletons"

PANEL_W, PANEL_H = 900, 620
MARGIN, GUTTER = 30, 26
HEADER = 150

STYLE = (
    "text{fill:#000;font-family:sans-serif}"
    ".t{font-size:26px;font-weight:bold;font-family:serif}"
    ".h{font-size:17px;font-weight:bold}.s{font-size:13px}.m{font-size:11px}"
    ".box{fill:#fff;stroke:#000;stroke-width:2}"
    ".stone{fill:#fff;stroke:#000;stroke-width:1.5}"
    ".actor{fill:#fff;stroke:#000;stroke-width:2.5}"
    ".obj{fill:#000}"
    ".face{stroke:#000;stroke-width:2.5;fill:none}"
    ".path{stroke:#000;stroke-width:1.6;fill:none;stroke-dasharray:7 5}"
    ".axis{stroke:#000;stroke-width:1;fill:none}"
    ".blocked{fill:#000}"
)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


class Panel:
    """Maps world coordinates onto one panel's page, per its projection."""

    def __init__(self, panel: dict, x: float, y: float) -> None:
        self.panel = panel
        self.ox, self.oy = x, y
        camera = panel["camera"]
        self.projection = camera["projection"]
        self.plan = self.projection == "orthographic-plan"
        self.side = self.projection == "orthographic-elevation-side"

    def project(self, position) -> tuple[float, float]:
        wx, wy, wz = position
        if self.plan:
            # page x = epistleward, page y = naveward, so altarward is page top
            return 450 + wx * 210, 330 - wy * 150
        if self.side:
            # looking across the sanctuary: page x = altarward, page y = up
            return 300 + wy * 210, 520 - wz * 210
        # front elevation: page x = epistleward, page y = up
        return 450 + wx * 240, 520 - wz * 210

    def facing_delta(self, vector) -> tuple[float, float]:
        vx, vy, _ = vector
        if self.plan:
            return vx * 46, -vy * 46
        if self.side:
            return vy * 46, 0.0
        return vx * 46, 0.0


def draw_altar(panel: Panel) -> list[str]:
    """Three full altar steps and the predella, in every panel."""
    out = []
    if panel.plan:
        for depth, half in ((0.25, 1.9), (0.75, 1.7), (1.25, 1.5), (1.5, 1.3)):
            x1, y1 = panel.project([-half, depth, 0])
            x2, y2 = panel.project([half, depth, 0])
            out.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="axis"/>'
            )
        x1, y1 = panel.project([-1.3, 1.5, 0])
        x2, y2 = panel.project([1.3, 1.9, 0])
        out.append(
            f'<rect x="{min(x1,x2):.1f}" y="{min(y1,y2):.1f}" '
            f'width="{abs(x2-x1):.1f}" height="{abs(y2-y1):.1f}" class="stone"/>'
        )
        return out
    # elevation: the steps, the predella, and the mensa
    for z, half in ((0.0, 1.85), (0.25, 1.65), (0.5, 1.45), (0.75, 1.25), (1.0, 1.05)):
        x1, y = panel.project([-half, 1.5, z])
        x2, _ = panel.project([half, 1.5, z])
        out.append(
            f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" class="stone"/>'
        )
    xl, ym = panel.project([-1.05, 1.5, 1.35])
    xr, _ = panel.project([1.05, 1.5, 1.35])
    out.append(
        f'<rect x="{xl:.1f}" y="{ym:.1f}" width="{xr-xl:.1f}" height="14" class="stone"/>'
    )
    return out


def draw_actor(panel: Panel, actor: dict) -> list[str]:
    px, py = panel.project(actor["position"])
    dx, dy = panel.facing_delta(actor["body_facing_vector"])
    reach = (dx * dx + dy * dy) ** 0.5
    out = [f'<circle cx="{px:.1f}" cy="{py:.1f}" r="15" class="actor"/>']
    if reach > 12.0:
        # a real in-plane component: draw the tick from the rim outward
        ux, uy = dx / reach, dy / reach
        out.append(
            f'<line x1="{px+ux*15:.1f}" y1="{py+uy*15:.1f}" '
            f'x2="{px+ux*40:.1f}" y2="{py+uy*40:.1f}" class="face"/>'
        )
    else:
        # facing is largely into or out of this panel's page; say so rather
        # than drawing a near-horizontal tick that would read as sideways
        out.append(
            f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" class="obj"/>'
        )
    out += [
        f'<text x="{px:.1f}" y="{py+30:.1f}" text-anchor="middle" class="m">'
        f'{escape(actor["id"])}</text>',
        f'<text x="{px:.1f}" y="{py-22:.1f}" text-anchor="middle" class="m">'
        f'{actor["body_facing_yaw_deg"]:.0f}&#176; d{actor["depth_rank"]}</text>',
    ]
    path = actor.get("path")
    if path and path.get("to_xyz"):
        points = [path["from_xyz"]] + list(path.get("via_xyz") or []) + [path["to_xyz"]]
        points = [p for p in points if p]
        if len(points) > 1:
            drawn = " ".join(
                "{:.1f},{:.1f}".format(*panel.project(p)) for p in points
            )
            out.append(f'<polyline points="{drawn}" class="path"/>')
            ex, ey = panel.project(points[-1])
            out.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="4" class="obj"/>')
    return out


def draw_object(panel: Panel, item: dict, dodge: dict) -> list[str]:
    if not item.get("position"):
        return []
    px, py = panel.project(item["position"])
    key = (round(px), round(py))
    level = dodge.get(key, 0)
    dodge[key] = level + 1
    out = [f'<rect x="{px-5:.1f}" y="{py-5:.1f}" width="10" height="10" class="obj"/>']
    if item.get("facing_vector"):
        dx, dy = panel.facing_delta(item["facing_vector"])
        out.append(
            f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px+dx*0.6:.1f}" '
            f'y2="{py+dy*0.6:.1f}" class="face"/>'
        )
    label = item["id"]
    if item.get("yaw_deg") is not None:
        label += f' {item["yaw_deg"]:.0f}°'
    out.append(
        f'<text x="{px+9:.1f}" y="{py-8-level*13:.1f}" class="m">'
        f'{escape(label)}</text>'
    )
    return out


def render(contract: dict) -> str:
    panels = contract["panels"]
    columns = min(len(panels), 2)
    rows = (len(panels) + columns - 1) // columns
    width = MARGIN * 2 + PANEL_W * columns + GUTTER * (columns - 1)
    height = HEADER + rows * (PANEL_H + GUTTER) + MARGIN + 90

    readiness = contract["art_readiness"]
    blocked = readiness["status"] == "blocked"

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f"<style>\n{STYLE}\n</style>",
        f'<text x="{width//2}" y="42" text-anchor="middle" class="t">'
        f'{escape(contract["plate_id"])} — RENDER SKELETON</text>',
        f'<text x="{width//2}" y="70" text-anchor="middle" class="s">'
        f'{escape(contract["title"])}</text>',
        f'<text x="{width//2}" y="92" text-anchor="middle" class="m">'
        f'world frame: +X epistleward / -X gospelward, +Y altarward, +Z up '
        f'· yaw 0° = epistleward, 90° = altarward · '
        f'structural baseline {escape(contract["structural_baseline_commit"])}</text>',
        f'<text x="{width//2}" y="112" text-anchor="middle" class="m">'
        f'panels: {len(panels)} ({escape(", ".join(p["id"] for p in panels))}) '
        f'· additional panels: {escape(contract["additional_panels"])} '
        f'· geometry is binding; an artist may beautify but not restage</text>',
    ]
    if blocked:
        cues = readiness.get("unresolved_cues") or []
        parts.append(
            f'<text x="{width//2}" y="136" text-anchor="middle" class="h blocked">'
            f'BLOCKED FOR ART — {len(cues)} unresolved cue(s); '
            f'see art-readiness.yaml</text>'
        )
    else:
        parts.append(
            f'<text x="{width//2}" y="136" text-anchor="middle" class="h">'
            f'ART-READY</text>'
        )

    for index, panel in enumerate(panels):
        col, row = index % columns, index // columns
        ox = MARGIN + col * (PANEL_W + GUTTER)
        oy = HEADER + row * (PANEL_H + GUTTER)
        camera = panel["camera"]
        parts.append(f'<g transform="translate({ox},{oy})">')
        parts.append(f'<rect width="{PANEL_W}" height="{PANEL_H}" rx="8" class="box"/>')
        parts.append(
            f'<text x="16" y="26" class="h">panel {escape(panel["id"])}</text>'
        )
        parts.append(
            f'<text x="16" y="46" class="s">projection '
            f'{escape(camera["projection"])} · position '
            f'{escape(camera["position"])}</text>'
        )
        frame = camera.get("frame") or {}
        if frame:
            bits = ", ".join(f"{k.replace('_world_direction','')}={v}"
                             for k, v in sorted(frame.items()))
            parts.append(f'<text x="16" y="64" class="m">page: {escape(bits)}</text>')
        if camera.get("collapses_equal_depth"):
            parts.append(
                '<text x="16" y="82" class="m">equal-depth actors collapse here '
                'and must not be separated</text>'
            )
        view = Panel(panel, ox, oy)
        parts.extend(draw_altar(view))
        dodge: dict = {}
        for item in contract["objects"]:
            parts.extend(draw_object(view, item, dodge))
        for actor in contract["actors"]:
            parts.extend(draw_actor(view, actor))
        parts.append("</g>")

    y = HEADER + rows * (PANEL_H + GUTTER) + 24
    for actor in contract["actors"]:
        parts.append(
            f'<text x="{MARGIN}" y="{y}" class="m">'
            f'{escape(actor["id"])}: {escape(actor["anchor"])} '
            f'{actor["position"]} · {escape(actor["posture"])} · bow '
            f'{escape(actor["bow"])} · faces {escape(actor["facing_semantic"])} '
            f'@ {actor["body_facing_yaw_deg"]:.0f}° · hands '
            f'{escape(actor["hands"]["left"])} | {escape(actor["hands"]["right"])}'
            f'</text>'
        )
        y += 18
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--scene")
    args = parser.parse_args()

    if args.scene:
        contract = load(CONTRACTS / f"{args.scene}.yaml")
        OUT.mkdir(exist_ok=True)
        (OUT / f"{args.scene}.svg").write_text(render(contract), encoding="utf-8")
        print(f"wrote skeleton for {args.scene}")
        return 0

    OUT.mkdir(exist_ok=True)
    stale = []
    written = 0
    for path in sorted(CONTRACTS.glob("*.yaml")):
        contract = load(path)
        svg = render(contract)
        target = OUT / f"{contract['plate_id']}.svg"
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != svg:
                stale.append(target.name)
        else:
            target.write_text(svg, encoding="utf-8")
            written += 1
    if args.check:
        tracked = {p.name for p in OUT.glob("*.svg")}
        expected = {f"{p.stem}.svg" for p in CONTRACTS.glob("*.yaml")}
        stale.extend(sorted(tracked - expected))
        if stale:
            print("stale skeletons: " + ", ".join(stale[:8]), file=sys.stderr)
            return 1
        print(f"PASS: {len(expected)} skeletons are current")
        return 0
    print(f"wrote {written} skeletons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
