#!/usr/bin/env python3
"""Draw the publication camera against its rejected alternatives.

A DEBUG artifact. It is not a panel, it is never part of an art-seed package,
and no artistic agent is shown it. It exists so that the choice of publication
camera can be argued about from pictures instead of from adjectives, and so
that a later change to the preset has to look at what it does to the plate.

The candidates are the ones this lane actually considered, including the two
the earlier lanes tried and rejected. Keeping the rejected ones drawn is the
point: the argument against raising the camera to rescue an object is much
easier to make when the raised camera is on the same sheet.

    ./camera-calibration.py [--check]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "review" / "camera-calibration-v1.svg"
SCENE = "LM-001A"

CELL_W, CELL_H = 460, 330
COLUMNS = 3
MARGIN, GUTTER = 28, 20
HEADER = 128


def underlay_module():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "_calibration_underlay", ROOT / "underlay.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CANDIDATES = [
    {
        "id": "nave-front-published",
        "position": [0.0, -5.6, 1.52],
        "focal": 1520.0,
        "verdict": "PUBLISHED",
        "note": "A standing eye in the nave, back far enough for a long lens.",
    },
    {
        "id": "nave-front-close",
        "position": [0.0, -4.2, 1.52],
        "focal": 1180.0,
        "verdict": "rejected",
        "note": "Same eye, too close: the figures crowd the altar off the plate.",
    },
    {
        "id": "nave-front-low",
        "position": [0.0, -5.6, 1.15],
        "focal": 1520.0,
        "verdict": "rejected",
        "note": "A child's eye. The mensa closes up and the steps stack.",
    },
    {
        "id": "head-height-1-85",
        "position": [0.0, -4.2, 1.85],
        "focal": 1180.0,
        "verdict": "rejected",
        "note": "The previous preset. Above every head, so the treads open out.",
    },
    {
        "id": "raised-2-35",
        "position": [0.0, -4.2, 2.35],
        "focal": 1180.0,
        "verdict": "rejected, and instructive",
        "note": "Raised once to make a flat Missal legible. Wrong instrument.",
    },
    {
        "id": "raised-3-60",
        "position": [0.0, -4.2, 3.60],
        "focal": 1180.0,
        "verdict": "rejected, and instructive",
        "note": "Raised again. By here the plate is an engineering overhead.",
    },
]


def render() -> str:
    underlay = underlay_module()
    contract = yaml.safe_load(
        (ROOT / "contracts" / f"{SCENE}.yaml").read_text(encoding="utf-8")
    )
    engine = underlay.Underlay()
    original = underlay.Camera.__init__

    rows = (len(CANDIDATES) + COLUMNS - 1) // COLUMNS
    width = MARGIN * 2 + COLUMNS * CELL_W + (COLUMNS - 1) * GUTTER
    height = HEADER + MARGIN + rows * (CELL_H + 62) + MARGIN

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        "<style>"
        "text{font-family:Georgia,serif;fill:#111}"
        ".t{font-size:20px}.s{font-size:13px;fill:#444}"
        ".id{font-size:14px}.v{font-size:12px;fill:#666}"
        ".pub{font-size:12px;fill:#111;font-weight:bold}"
        "rect.cell{fill:none;stroke:#bbb;stroke-width:1}"
        "rect.pubcell{fill:none;stroke:#111;stroke-width:2}"
        # The panels are drawn by underlay.py and styled by it. Restating the
        # rules here would let the sheet and the plate drift apart, and a
        # calibration sheet that does not draw what the plate draws is worse
        # than none.
        + underlay.STYLE +
        "</style>",
        f'<rect width="{width}" height="{height}" fill="#fff"/>',
        f'<text class="t" x="{MARGIN}" y="42">Publication camera calibration '
        f'&#8212; {escape(SCENE)}</text>',
        f'<text class="s" x="{MARGIN}" y="68">Debug artifact. Not a panel, '
        "never part of an art-seed package, never shown to an artistic "
        "agent.</text>",
        f'<text class="s" x="{MARGIN}" y="88">Every cell draws the same scene '
        "and the same sanctuary. Only the station point and the lens "
        "differ.</text>",
        f'<text class="s" x="{MARGIN}" y="108">The rejected raises are kept on '
        "the sheet on purpose: they are the argument against moving a camera "
        "to rescue an object.</text>",
    ]

    for index, candidate in enumerate(CANDIDATES):
        column, row = index % COLUMNS, index // COLUMNS
        x = MARGIN + column * (CELL_W + GUTTER)
        y = HEADER + MARGIN + row * (CELL_H + 62)

        panel = dict(contract["panels"][0])
        panel["camera"] = dict(panel["camera"])
        panel["camera"]["position_xyz"] = candidate["position"]
        panel["camera"]["focal_length_px"] = candidate["focal"]

        def patched(self, p, _focal=candidate["focal"], _init=original):
            _init(self, p)
            self.focal = _focal

        underlay.Camera.__init__ = patched
        try:
            body = engine.render_panel(contract, panel)
        finally:
            underlay.Camera.__init__ = original

        published = candidate["verdict"] == "PUBLISHED"
        cls = "pubcell" if published else "cell"
        out.append(f'<rect class="{cls}" x="{x}" y="{y}" '
                   f'width="{CELL_W}" height="{CELL_H}"/>')
        out.append(
            f'<svg x="{x}" y="{y}" width="{CELL_W}" height="{CELL_H}" '
            f'viewBox="0 0 {underlay.PANEL_W} {underlay.PANEL_H}" '
            f'preserveAspectRatio="xMidYMid meet">{body}</svg>'
        )
        eye = candidate["position"]
        out.append(
            f'<text class="id" x="{x}" y="{y + CELL_H + 20}">'
            f'{escape(candidate["id"])}</text>'
        )
        out.append(
            f'<text class="{"pub" if published else "v"}" x="{x}" '
            f'y="{y + CELL_H + 37}">eye {eye[2]:.2f}, {abs(eye[1]):.1f} back, '
            f'{candidate["focal"]:.0f}px &#8212; {escape(candidate["verdict"])}'
            "</text>"
        )
        out.append(
            f'<text class="v" x="{x}" y="{y + CELL_H + 54}">'
            f'{escape(candidate["note"])}</text>'
        )

    out.append("</svg>")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    svg = render()
    if args.check:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != svg:
            print(f"STALE: {OUT.name} does not match its inputs", file=sys.stderr)
            return 1
        print(f"current: {OUT.name}")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.name} ({len(CANDIDATES)} candidate cameras)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
