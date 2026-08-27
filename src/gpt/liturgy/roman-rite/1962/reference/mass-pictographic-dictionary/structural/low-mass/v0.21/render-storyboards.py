#!/usr/bin/env python3
"""Render deterministic structural storyboards from the recovered scene corpus.

One SVG per section, laid out from `scenes/inventory.yaml` and the section
files. The output is a structural review projection, not a publication plate:
it carries labels on purpose, so that a reviewer can see at a glance whether
every scene is drawable. It is regenerated, never hand-edited.

Usage:
    ./render-storyboards.py            # write storyboards/
    ./render-storyboards.py --check    # fail if the tracked output is stale
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import yaml

ROOT = Path(__file__).resolve().parent
SCENES = ROOT / "scenes"
OUT = ROOT / "storyboards"
VERSION = "v0.1"

COLUMNS = 3
PANEL_W = 780
GUTTER = 24
MARGIN = 30
HEADER = 118
LINE = 25
PAD_TOP = 62
PAD_BOTTOM = 18

STYLE = (
    "text{fill:#000}.ser{font-family:serif}.sans{font-family:sans-serif}"
    ".title{font-size:33px;font-weight:bold}.h{font-size:20px}"
    ".s{font-size:15px}.tiny{font-size:12px}"
    ".box{fill:#fff;stroke:#000;stroke-width:2}"
)


def load(relative: str) -> dict:
    with (ROOT / relative).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def actor_line(actor: dict) -> str:
    hands = actor["hands"]
    grip = hands["left"] if hands["left"] == hands["right"] else (
        f"L {hands['left']} / R {hands['right']}"
    )
    bits = [actor["posture"], actor["anchor"], f"faces {actor['facing']}",
            f"eyes {actor['gaze']}", grip]
    if actor["bow"] != "none":
        bits.insert(1, f"bow {actor['bow']}")
    return f"{actor['id']}: " + " · ".join(bits)


def scene_lines(scene: dict) -> list[tuple[str, str]]:
    """Return (css class, text) pairs for one scene panel."""
    lines: list[tuple[str, str]] = []
    if scene["condition"] != "ALWAYS":
        lines.append(("tiny", f"ONLY WHEN {scene['condition']}"))
    cue = scene.get("text_cue")
    if cue:
        lines.append(("s", f"“{cue}” ({scene['voice']})"))
    for actor in scene["actors"]:
        lines.append(("tiny", actor_line(actor)))
        for gesture in actor.get("gestures") or []:
            lines.append(("tiny", f"    → {gesture}"))
        path = actor.get("path")
        if path and path.get("to"):
            route = " → ".join(
                [path.get("from") or "?"] + list(path.get("via") or []) + [path["to"]]
            )
            lines.append(("tiny", f"    path {route}"))
    for item in scene.get("objects") or []:
        text = f"{item['id']} @ {item['placement']}"
        if item.get("orientation") and item["orientation"] != "not-applicable":
            text += f" [{item['orientation']}]"
        if item["handled_by"] != "none":
            text += f" — by {item['handled_by']}"
        lines.append(("tiny", text))
    for bell in scene.get("bells") or []:
        lines.append(
            ("s", f"BELL {bell['actor']} ×{bell['count']} — {bell['cue']}")
        )
    for response in scene.get("responses") or []:
        lines.append(("tiny", f"{response['actor']}: “{response['text']}”"))
    for variant in scene.get("variants") or []:
        lines.append(("tiny", f"VARIANT [{variant['kind']}] {variant['description']}"))
    for item in scene.get("unresolved") or []:
        lines.append(("tiny", f"UNRESOLVED: {item}"))
    lines.append(("tiny", "invariants: " + ", ".join(scene["invariants"])))
    return lines


def wrap(text: str, width: int) -> list[str]:
    words, out, current = text.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) > width and current:
            out.append(current)
            current = ("    " if text.startswith("    ") else "") + word
        else:
            current = candidate
    if current:
        out.append(current)
    return out or [""]


def render_section(section: dict, scenes: list[dict]) -> str:
    panels = []
    for scene in scenes:
        body: list[tuple[str, str]] = []
        for css, text in scene_lines(scene):
            for piece in wrap(text, 96 if css == "tiny" else 78):
                body.append((css, piece))
        height = PAD_TOP + LINE * len(body) + PAD_BOTTOM
        panels.append((scene, body, height))

    rows = [panels[i:i + COLUMNS] for i in range(0, len(panels), COLUMNS)]
    width = MARGIN * 2 + PANEL_W * COLUMNS + GUTTER * (COLUMNS - 1)
    y = HEADER
    placed = []
    for row in rows:
        row_height = max(height for _, _, height in row)
        for index, (scene, body, _) in enumerate(row):
            x = MARGIN + index * (PANEL_W + GUTTER)
            placed.append((x, y, row_height, scene, body))
        y += row_height + GUTTER
    height = y + MARGIN

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f"<style>\n{STYLE}\n</style>",
        f'<text x="{width // 2}" y="46" text-anchor="middle" class="ser title">'
        f'{escape(section["id"].upper())}</text>',
        f'<text x="{width // 2}" y="80" text-anchor="middle" class="ser h">'
        f'{escape(section["title"])} · '
        f'{escape(section["scene_range"][0])}–{escape(section["scene_range"][1])}'
        f' · spoken 1962 Low Mass, two servers</text>',
    ]
    for x, y, row_height, scene, body in placed:
        parts.append(f'<g transform="translate({x},{y})">')
        parts.append(
            f'<rect width="{PANEL_W}" height="{row_height}" rx="10" class="box"/>'
        )
        parts.append(
            f'<text x="20" y="30" class="sans h">{escape(scene["scene_id"])}</text>'
        )
        parts.append(
            f'<text x="20" y="52" class="sans s">{escape(scene["title"])}</text>'
        )
        for index, (css, text) in enumerate(body):
            parts.append(
                f'<text x="20" y="{PAD_TOP + LINE * index + 12}" '
                f'class="sans {css}">{escape(text)}</text>'
            )
        parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="fail if the tracked storyboards are stale")
    args = parser.parse_args()

    inventory = load("scenes/inventory.yaml")
    OUT.mkdir(exist_ok=True)
    stale = []
    for section in inventory["sections"]:
        document = load(f"scenes/{section['file']}")
        svg = render_section(section, document["scenes"])
        target = OUT / f"{section['id']}-{VERSION}.svg"
        if args.check:
            if not target.is_file() or target.read_text(encoding="utf-8") != svg:
                stale.append(target.name)
        else:
            target.write_text(svg, encoding="utf-8")
    if args.check:
        if stale:
            print("stale storyboards: " + ", ".join(stale), file=sys.stderr)
            return 1
        print(f"PASS: {len(inventory['sections'])} storyboards are current")
    else:
        print(f"wrote {len(inventory['sections'])} storyboards to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
