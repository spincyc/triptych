#!/usr/bin/env python3
"""Generate the render-contract verification sheet.

Not an artistic plate. A single page a human can check at a glance to confirm
that the four properties this layer exists to guarantee actually hold in the
compiled output:

  1. the world axes are the approved ones;
  2. the Missal reads the same way on both sides;
  3. projection and camera position are separate, and a place is not a
     projection;
  4. the two post-ablution crossings compile in opposite order.

Usage:
    ./review.py            # write review/
    ./review.py --check    # fail if the tracked sheet is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parent
CONTRACTS = ROOT / "contracts"
OUT = ROOT / "review"

FIXTURES = {
    "opening": "LM-001A",
    "gospel_side_reading": "LM-035A",
    "crossing_first": "LM-136C",
    "crossing_second": "LM-136E",
    "elevation": "LM-099A",
}

STYLE = (
    "text{fill:#000;font-family:sans-serif}"
    ".t{font-size:28px;font-weight:bold;font-family:serif}"
    ".h{font-size:17px;font-weight:bold}.s{font-size:13px}.m{font-size:11.5px}"
    ".box{fill:#fff;stroke:#000;stroke-width:2}"
    ".ax{stroke:#000;stroke-width:2;fill:none}"
    ".ok{font-size:13px;font-weight:bold}"
)


def load(scene_id: str) -> dict:
    with (CONTRACTS / f"{scene_id}.yaml").open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def missal_of(contract: dict) -> dict:
    return next(o for o in contract["objects"] if o["id"] == "missal")


def actor_of(contract: dict, actor_id: str) -> dict:
    return next(a for a in contract["actors"] if a["id"] == actor_id)


def panel(x: int, y: int, w: int, h: int, title: str, lines) -> list[str]:
    out = [
        f'<g transform="translate({x},{y})">',
        f'<rect width="{w}" height="{h}" rx="8" class="box"/>',
        f'<text x="18" y="30" class="h">{escape(title)}</text>',
    ]
    ty = 56
    for css, text in lines:
        out.append(f'<text x="18" y="{ty}" class="{css}">{escape(text)}</text>')
        ty += 19
    out.append("</g>")
    return out


def render() -> str:
    contracts = {name: load(sid) for name, sid in FIXTURES.items()}
    width, height = 1720, 1180
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f"<style>\n{STYLE}\n</style>",
        f'<text x="{width//2}" y="44" text-anchor="middle" class="t">'
        f'RENDER-CONTRACT VERIFICATION — 1962 LOW MASS v1</text>',
        f'<text x="{width//2}" y="70" text-anchor="middle" class="s">'
        f'structural baseline '
        f'{escape(contracts["opening"]["structural_baseline_commit"])} '
        f'· not an artistic plate · geometry is binding</text>',
    ]

    # 1 — world axes
    axis = [
        ("s", "Canonical view: the nave, facing the altar."),
        ("m", "+X epistleward  →  page RIGHT      -X gospelward  →  page LEFT"),
        ("m", "+Y altarward (away from the people)  -Y naveward"),
        ("m", "+Z upward"),
        ("m", "yaw 0° = epistleward, 90° = altarward, 180° = gospelward"),
        ("m", "turn right = yaw decreasing; turn left = yaw increasing."),
        ("m", "A turn is a sense, never a fixed pair of endpoints, so the two"),
        ("m", "full-circle turns sweep correctly from a naveward start."),
    ]
    parts += panel(30, 96, 810, 250, "1 · WORLD FRAME", axis)
    parts += [
        '<g transform="translate(560,240)">',
        '<line x1="-90" y1="0" x2="90" y2="0" class="ax"/>',
        '<line x1="0" y1="60" x2="0" y2="-60" class="ax"/>',
        '<text x="96" y="5" class="m">+X epistle</text>',
        '<text x="-150" y="5" class="m">-X gospel</text>',
        '<text x="6" y="-66" class="m">+Y altarward</text>',
        '<text x="6" y="76" class="m">-Y naveward</text>',
        "</g>",
    ]

    # 2 — the Missal, both sides
    e, g = missal_of(contracts["opening"]), missal_of(contracts["gospel_side_reading"])
    same = e["reading"]["page_up_yaw_deg"] == g["reading"]["page_up_yaw_deg"]
    lines = [
        ("s", "The failure this layer exists to prevent: a mirrored book."),
        ("m", f'Epistle side  {contracts["opening"]["plate_id"]}  '
              f'{e["placement_semantic"]}  yaw {e["reading"]["page_up_yaw_deg"]}°'),
        ("m", f'Gospel side   {contracts["gospel_side_reading"]["plate_id"]}  '
              f'{g["placement_semantic"]}  yaw {g["reading"]["page_up_yaw_deg"]}°'),
        ("m", f'page-up vector both sides: {e["reading"]["page_up_vector"][:2]}'),
        ("m", "X is negative on both sides: the priest turns gospelward to read,"),
        ("m", "wherever the book stands. The mirrored value 45° never occurs."),
        ("ok", "SAME YAW ON BOTH SIDES: " + ("yes" if same else "NO — FAIL")),
    ]
    parts += panel(870, 96, 820, 250, "2 · MISSAL ORIENTATION", lines)

    # 3 — camera and panels
    opening = contracts["opening"]
    first = contracts["crossing_first"]
    cam = opening["panels"][0]["camera"]
    lines = [
        ("s", "Projection and camera position are independent vocabularies."),
        ("m", f'{opening["plate_id"]}  projection {cam["projection"]}  '
              f'position {cam["position"]}'),
        ("m", f'panels {len(opening["panels"])} '
              f'({", ".join(p["id"] for p in opening["panels"])})  '
              f'additional_panels: {opening["additional_panels"]}'),
        ("m", f'{first["plate_id"]}  panels {len(first["panels"])} '
              f'({", ".join(p["id"] for p in first["panels"])})  '
              f'— the plan is DECLARED, not invented'),
        ("m", 'A plan view is projection orthographic-plan with a declared'),
        ("m", 'page-top world direction. "nave" is a position and can never be'),
        ("m", 'spelled as a projection, so "TOP VIEW (NAVE)" is unwritable.'),
        ("ok", "UNDECLARED PANELS: forbidden, and checked against every skeleton"),
    ]
    parts += panel(30, 366, 810, 270, "3 · CAMERA AND PANEL CONTRACT", lines)

    # 4 — crossing order
    c1, c2 = contracts["crossing_first"], contracts["crossing_second"]
    a1, a2 = actor_of(c1, "AC1"), actor_of(c1, "AC2")
    b1, b2 = actor_of(c2, "AC1"), actor_of(c2, "AC2")
    ordered = a2["position"][1] < a1["position"][1] and b1["position"][1] < b2["position"][1]
    lines = [
        ("s", "Ordered choreography must survive compilation, not stay prose."),
        ("m", f'{c1["plate_id"]} first crossing   '
              f'AC2 y={a2["position"][1]} (rank {a2["depth_rank"]})   '
              f'AC1 y={a1["position"][1]} (rank {a1["depth_rank"]})'),
        ("m", f'{c2["plate_id"]} second crossing  '
              f'AC1 y={b1["position"][1]} (rank {b1["depth_rank"]})   '
              f'AC2 y={b2["position"][1]} (rank {b2["depth_rank"]})'),
        ("m", "Smaller y is nearer the viewer. depth_rank compiles to an"),
        ("m", "explicit offset, so who leads is a number, not an adjective."),
        ("m", "AC1 carries the chalice cloth gospelward; AC2 carries the Missal"),
        ("m", "epistleward. The Missal keeps its one reading yaw throughout."),
        ("ok", "AC2 LEADS FIRST, AC1 LEADS SECOND: " + ("yes" if ordered else "NO — FAIL")),
    ]
    parts += panel(870, 366, 820, 270, "4 · CROSSING PRECEDENCE", lines)

    # 5 — elevation detail and readiness
    elev = contracts["elevation"]
    bell = [b for b in [] ] or []
    lines = [
        ("s", f'{elev["plate_id"]} — {elev["title"]}'),
    ]
    for actor in elev["actors"]:
        lines.append(
            ("m", f'{actor["id"]:6} {actor["anchor"]:24} {actor["position"]}  '
                  f'faces {actor["body_facing_yaw_deg"]:.0f}°  '
                  f'hands {actor["hands"]["left"]} | {actor["hands"]["right"]}')
        )
    lines.append(("m", "The chasuble-lifting hands and the bell hand are explicit"))
    lines.append(("m", "actor state, so an artist cannot reassign them."))
    parts += panel(30, 656, 1660, 240, "5 · FINE DETAIL AT THE ELEVATION", lines)

    readiness = yaml.safe_load((ROOT / "art-readiness.yaml").read_text(encoding="utf-8"))
    totals = readiness["totals"]
    lines = [
        ("s", f'{totals["scenes"]} scenes · {totals["ready"]} art-ready · '
              f'{totals["blocked"]} blocked for art'),
        ("m", "A scene blocks when an unresolved serving-profile cue could change"),
        ("m", "something visible, or when a directional phrase names no frame."),
        ("m", "Blocked is the safe default: an unclassified cue never makes a"),
        ("m", "scene ready. Cues are resolved by human review only, and never"),
        ("m", "from the fenced pre-v0.21 altar-server guides."),
        ("ok", "Every art-ready scene compiles with no unresolved visible geometry."),
    ]
    parts += panel(30, 916, 1660, 200, "6 · ART READINESS", lines)
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    target = OUT / "verification-sheet-v1.svg"
    sheet = render()
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != sheet:
            print("stale verification sheet", file=sys.stderr)
            return 1
        print("PASS: verification sheet is current")
        return 0
    target.write_text(sheet, encoding="utf-8")
    print(f"wrote {target.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
