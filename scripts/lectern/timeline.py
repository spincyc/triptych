"""Box-drawn pictures that scroll: book states on a year axis, and the recorded lines.

Nothing here decides anything about history. The positions are the page's
model's (`M.stageLayout` x coordinates, `M.panelLayout` tracks), rescaled from
the page's pixels to columns; the connections are the record's transitions
and parent links, and nothing else draws a line. What this file adds is only
the terminal's grammar for them:

    ●  documented state / act        ◇  provisional lead       ○  printed
    ├──┤  date uncertainty (one event, not a period of use)
    ━  ─  ╌  ┄   evidence, strongest to weakest; a shared stretch of line
                 takes the weakest of the evidence it carries
    ▶ ▼ ▲  the arrow points at the receiving state
    ○ at a line's end: a continuation outside this view

Where two unrelated lines cross, the crossing is drawn as one line passing
over a gap in the other: a crossing without a marker asserts no connection.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rich.style import Style
from rich.text import Text
from textual.binding import Binding
from textual.geometry import Size
from textual.message import Message
from textual.scroll_view import ScrollView
from textual.strip import Strip

from .theme import SURFACE_ACCENTS, blend

U, D, L, R = 1, 2, 4, 8

# Evidence weights, strongest first. A shared cell takes the weakest.
HEAVY, SOLID, DASHED, DOTTED, DOUBLE = 0, 1, 2, 3, 4
STRAIGHT = {HEAVY: ("┃", "━"), SOLID: ("│", "─"), DASHED: ("╎", "╌"), DOTTED: ("┆", "┄"), DOUBLE: ("║", "═")}
LIGHT_JOINS = {D | R: "╭", D | L: "╮", U | R: "╰", U | L: "╯", U | D | R: "├", U | D | L: "┤",
               D | L | R: "┬", U | L | R: "┴", U | D | L | R: "┼"}
HEAVY_JOINS = {D | R: "┏", D | L: "┓", U | R: "┗", U | L: "┛", U | D | R: "┣", U | D | L: "┫",
               D | L | R: "┳", U | L | R: "┻", U | D | L | R: "╋"}
DOUBLE_JOINS = {D | R: "╔", D | L: "╗", U | R: "╚", U | L: "╝", U | D | R: "╠", U | D | L: "╣",
                D | L | R: "╦", U | L | R: "╩", U | D | L | R: "╬"}


def weight_of(style: dict) -> int:
    """The page's own stroke for a transition (`M.stageStyle`), in box glyphs:
    no dash is a solid line, heavier where the page draws it wider; a long
    dash is dashed; a short one dotted."""
    dash = str(style.get("dash") or "").split()
    if not dash:
        return HEAVY if (style.get("width") or 0) >= 3 else SOLID
    return DASHED if float(dash[0]) >= 4 else DOTTED


@dataclass(frozen=True)
class Palette:
    accent: str
    fg: str
    muted: str
    line: str
    rule: str
    warn: str
    err: str
    hot: str
    cursor: str
    idle: str

    @classmethod
    def of(cls, app, surface: str) -> "Palette":
        values = app.theme_variables
        dark = getattr(app.current_theme, "dark", True)
        accent = values.get(f"{surface}-color") or SURFACE_ACCENTS[surface][0 if dark else 1]
        fg = values.get("foreground", "#dddddd")
        bg = values.get("surface") or values.get("background", "#000000")
        return cls(
            accent=accent, fg=fg,
            muted=values.get("muted") or blend((bg, fg), 0.55),
            line=blend((bg, fg), 0.66), rule=values.get("rule") or blend((bg, fg), 0.3),
            warn=values.get("warning", "#e3a33b"), err=values.get("error", "#e05252"),
            hot=values.get("hotkey", "#ff5f6d"), cursor=blend((bg, accent), 0.34),
            idle=blend((bg, accent), 0.16),
        )


@dataclass
class Item:
    """A chosen thing in a picture: the rows it spans and what it is."""

    key: str
    kind: str
    top: int
    bottom: int


@dataclass
class Picture:
    lines: list[Text] = field(default_factory=list)
    items: list[Item] = field(default_factory=list)
    header: int = 0  # rows at the top that stay put while the rest scrolls (the year axis)


class Grid:
    """Cells of line work, with glyphs and text laid over them."""

    def __init__(self, rows: int, width: int) -> None:
        self.width = width
        self.lines: list[list[list | None]] = [[None] * width for _ in range(rows)]
        self.glyphs: dict[tuple[int, int], tuple[str, str]] = {}

    def inside(self, row: int, column: int) -> bool:
        return 0 <= row < len(self.lines) and 0 <= column < self.width

    def put(self, row: int, column: int, bits: int, weight: int, group: tuple) -> None:
        if not self.inside(row, column):
            return
        cell = self.lines[row][column]
        if cell is None:
            self.lines[row][column] = [bits, weight, {group}]
            return
        held, strength, groups = cell
        if any(one[0] == group[0] or one[1] == group[1] for one in groups):
            # The same transition's source or receiving state: a true fork or join.
            cell[0] = held | bits
            cell[1] = max(strength, weight)
            groups.add(group)
        elif bits & (L | R) and not held & (L | R):
            # An unrelated crossing: the horizontal passes over a gap.
            self.lines[row][column] = [bits, weight, {group}]

    def vertical(self, column: int, first: int, last: int, weight: int, group: tuple) -> None:
        """Rows `first`..`last` inclusive; nothing where the run is empty."""
        for row in range(first, last + 1):
            self.put(row, column, U | D, weight, group)

    def horizontal(self, row: int, first: int, last: int, weight: int, group: tuple) -> None:
        for column in range(first, last + 1):
            self.put(row, column, L | R, weight, group)

    def glyph(self, row: int, column: int, char: str, style: str) -> None:
        if self.inside(row, column):
            self.glyphs[(row, column)] = (char, style)

    def text(self, row: int, column: int, words: str, style: str) -> None:
        for offset, char in enumerate(words):
            self.glyph(row, column + offset, char, style)

    def free(self, row: int, first: int, last: int) -> bool:
        return all(self.inside(row, c) and self.lines[row][c] is None and (row, c) not in self.glyphs
                   for c in range(first, last + 1))

    def row(self, index: int, line_style: str) -> Text:
        out = Text(no_wrap=True, overflow="crop")
        for column in range(self.width):
            if (index, column) in self.glyphs:
                char, style = self.glyphs[(index, column)]
                out.append(char, style=style)
                continue
            cell = self.lines[index][column]
            if cell is None:
                out.append(" ")
                continue
            bits, weight, _ = cell
            if bits in (U | D, U, D):
                char = STRAIGHT[weight][0]
            elif bits in (L | R, L, R):
                char = STRAIGHT[weight][1]
            else:
                joins = HEAVY_JOINS if weight == HEAVY else DOUBLE_JOINS if weight == DOUBLE else LIGHT_JOINS
                char = joins.get(bits, "┼")
            out.append(char, style=line_style)
        return out


def _fit(words: str, width: int) -> str:
    if width <= 0:
        return ""
    return words if len(words) <= width else words[: max(0, width - 1)] + "…"


def _cell(text: Text, width: int) -> Text:
    """A Text cut or padded to exactly `width` cells."""
    text = text.copy()
    text.no_wrap = True
    text.overflow = "crop"
    if text.cell_len > width:
        text.truncate(width, overflow="ellipsis")
    if text.cell_len < width:
        text.append(" " * (width - text.cell_len))
    return text


# --------------------------------------------------------------------------
# Books through time
# --------------------------------------------------------------------------

ARROW_SAMPLE = {HEAVY: "━━▶", SOLID: "──▶", DASHED: "╌╌▶", DOTTED: "┄┄▶"}


def paint_timeline(model: dict, width: int, pal: Palette) -> Picture:
    """Dated book states, one row each, on the page's own year axis.

    Rows follow the model's lane order (by date within a lane, then the
    record's order); equal years share a column. A state's row carries its
    marker and its date bracket; a recorded transition is the only thing that
    draws a line, and it arrives from the left at the receiving state, or, where
    there is no room, from a row of its own beside it.
    """
    picture = Picture(header=2)
    width = max(40, width)
    label_width = max(18, min(46, width * 9 // 20))
    plot = width - label_width - 1
    if plot < 18:
        label_width = max(12, width - 19)
        plot = width - label_width - 1
    axis = model.get("axis") or {}
    x0, x1 = axis.get("x0", 0), axis.get("x1", 1)

    def col(x: float) -> int:
        if x1 <= x0:
            return 0
        return max(0, min(plot - 1, round((x - x0) / (x1 - x0) * (plot - 1))))

    lanes = model.get("lanes") or []
    edges = model.get("edges") or []
    nodes = {node["id"]: node for lane in lanes for node in lane["nodes"]}
    order = [node["id"] for lane in lanes for node in lane["nodes"]]
    position = {ident: index for index, ident in enumerate(order)}
    place = {ident: (col(n["x"]), col(n["x_start"]), col(n["x_end"])) for ident, n in nodes.items()}

    inside = [e for e in edges if e["from"] in nodes and e["to"] in nodes]
    # Which in-view transitions need a row of their own beside the receiving state.
    beside: dict[str, str] = {}
    for edge in inside:
        xs = place[edge["from"]][0]
        _, cs, _ = place[edge["to"]]
        if xs > cs - 2:
            beside[edge["id"]] = "above" if position[edge["from"]] < position[edge["to"]] else "below"

    # Rows, in order: (kind, payload).
    rows: list[tuple[str, dict]] = [("axis-label", {}), ("axis", {})]
    for lane in lanes:
        rows.append(("lane", lane))
        for node in lane["nodes"]:
            ident = node["id"]
            for edge in edges:
                if edge["to"] == ident and edge["from_outside"]:
                    rows.append(("from", edge))
            for edge in inside:
                if edge["to"] == ident and beside.get(edge["id"]) == "above":
                    rows.append(("arrive", edge))
            rows.append(("stage", node))
            for edge in inside:
                if edge["to"] == ident and beside.get(edge["id"]) == "below":
                    rows.append(("arrive", edge))
            for edge in edges:
                if edge["from"] == ident and edge["to_outside"]:
                    rows.append(("to", edge))
    if not order:
        rows.append(("empty", {}))

    at: dict[str, int] = {}
    arrive_at: dict[str, int] = {}
    outside_at: dict[str, int] = {}
    for index, (kind, payload) in enumerate(rows):
        if kind == "stage":
            at[payload["id"]] = index
        elif kind == "arrive":
            arrive_at[payload["id"]] = index
        elif kind in ("from", "to"):
            outside_at[payload["id"]] = index

    grid = Grid(len(rows), plot)
    line = pal.line
    arrow_style = f"bold {pal.accent}"

    def key_on(row: int, first: int, last: int, key: str) -> None:
        if last - first + 1 >= len(key) + 2:
            start = first + (last - first + 1 - len(key)) // 2
            grid.text(row, start, key, pal.muted)

    for edge in edges:
        weight = weight_of(edge.get("style") or {})
        group = (edge["from"], edge["to"])
        if edge["id"] in outside_at:
            row = outside_at[edge["id"]]
            xp = col(edge["from_x"] if edge["from_outside"] else edge["to_x"])
            if edge["from_outside"]:
                target = nodes.get(edge["to"])
                if not target:
                    continue
                cm = place[edge["to"]][0]
                if xp == cm:
                    grid.glyph(row, cm, "▼", arrow_style)
                    grid.glyph(row, cm + 1, "○", pal.muted)
                else:
                    grid.horizontal(row, min(xp, cm) + 1, max(xp, cm) - 1, weight, group)
                    grid.glyph(row, xp, "○", pal.muted)
                    grid.glyph(row, cm, "▼", arrow_style)
                    key_on(row, min(xp, cm) + 1, max(xp, cm) - 1, edge["key"])
            else:
                source = nodes.get(edge["from"])
                if not source:
                    continue
                xs = place[edge["from"]][0]
                top = at[edge["from"]]
                grid.vertical(xs, top + 1, row - 1, weight, group)
                if xp < xs:
                    xp = min(xp, xs - 2)
                    grid.put(row, xs, U | L, weight, group)
                    grid.horizontal(row, xp + 2, xs - 1, weight, group)
                    grid.glyph(row, xp + 1, "◀", arrow_style)
                    grid.glyph(row, xp, "○", pal.muted)
                    key_on(row, xp + 2, xs - 1, edge["key"])
                else:
                    xp = max(xp, xs + 2)
                    grid.put(row, xs, U | R, weight, group)
                    grid.horizontal(row, xs + 1, xp - 2, weight, group)
                    grid.glyph(row, xp - 1, "▶", arrow_style)
                    grid.glyph(row, xp, "○", pal.muted)
                    key_on(row, xs + 1, xp - 2, edge["key"])
            continue
        if edge["from"] not in nodes or edge["to"] not in nodes:
            continue
        xs = place[edge["from"]][0]
        cm, cs, _ = place[edge["to"]]
        top, bottom = at[edge["from"]], at[edge["to"]]
        down = bottom > top
        if edge["id"] in arrive_at:
            row = arrive_at[edge["id"]]
            if down:
                grid.vertical(xs, top + 1, row - 1, weight, group)
            else:
                grid.vertical(xs, row + 1, top - 1, weight, group)
            come = U if down else D
            arrow = "▼" if down else "▲"
            if xs == cm:
                grid.put(row, xs, come, weight, group)
            else:
                toward = R if cm > xs else L
                grid.put(row, xs, come | toward, weight, group)
                grid.horizontal(row, min(xs, cm) + 1, max(xs, cm) - 1, weight, group)
            grid.glyph(row, cm, arrow, arrow_style)
            continue
        if down:
            grid.vertical(xs, top + 1, bottom - 1, weight, group)
            grid.put(bottom, xs, U | R, weight, group)
        else:
            grid.vertical(xs, bottom + 1, top - 1, weight, group)
            grid.put(bottom, xs, D | R, weight, group)
        grid.horizontal(bottom, xs + 1, cs - 2, weight, group)
        grid.glyph(bottom, cs - 1, "▶", arrow_style)
        key_on(bottom, xs + 1, cs - 2, edge["key"])

    # Brackets, markers and the date beside each state, over the line work.
    for ident, node in nodes.items():
        row = at[ident]
        cm, cs, ce = place[ident]
        tone = pal.warn if node["status"] == "provisional" else pal.accent
        if ce > cs:
            for column in range(cs, ce + 1):
                grid.glyph(row, column, "─", tone)
            grid.glyph(row, cs, "◁" if node["clipped_start"] else "├", tone)
            grid.glyph(row, ce, "▷" if node["clipped_end"] else "┤", tone)
            # A marker clamped onto a clipped end would hide the clip; it steps inside.
            if node["clipped_start"] and cm == cs:
                cm = cs + 1
            if node["clipped_end"] and cm == ce:
                cm = max(cs, ce - 1)
        grid.glyph(row, cm, "◇" if node["status"] == "provisional" else "●", f"bold {tone}")
        said = " ".join(node.get("date_lines") or [f"{node['date_label']} · {node['date_kind']}"])
        room = plot - (ce + 2)
        if room >= 8 and grid.free(row, ce + 2, min(plot - 1, ce + 1 + min(room, len(said)))):
            grid.text(row, ce + 2, _fit(said, room), pal.muted)

    # The axis.
    ticks = axis.get("ticks") or []
    labels_row, rule_row = 0, 1
    for column in range(plot):
        grid.glyph(rule_row, column, "─", pal.rule)
    columns = [col(tick["x"]) for tick in ticks]
    spacing = min((b - a for a, b in zip(columns, columns[1:])), default=plot) or 1
    widest = max((len(str(tick["year"])) for tick in ticks), default=4)
    stride = max(1, -(-(widest + 1) // spacing))  # label every tick that has room, evenly
    last_end = -2
    for index, (tick, column) in enumerate(zip(ticks, columns)):
        grid.glyph(rule_row, column, "┬", pal.muted)
        if index % stride:
            continue
        words = str(tick["year"])
        start = max(0, min(plot - len(words), column - len(words) // 2))
        if start > last_end + 1:
            grid.text(labels_row, start, words, pal.muted)
            last_end = start + len(words) - 1

    for index, (kind, payload) in enumerate(rows):
        label = Text(no_wrap=True)
        if kind == "axis-label":
            label.append("Year · same scale in every lane", style=f"italic {pal.muted}")  # page: history.js:2992
        elif kind == "axis":
            label.append("brackets: date uncertainty", style=f"italic {pal.muted}")
        elif kind == "lane":
            label.append("▌", style=pal.accent)
            label.append(payload["label"], style=f"bold {pal.accent}")
            count = payload["count"]
            if grid.free(index, max(0, plot - len(count)), plot - 1):
                grid.text(index, max(0, plot - len(count)), count, f"italic {pal.muted}")
        elif kind == "stage":
            label.append(f"{payload['key']} ", style=pal.muted)
            label.append(payload["label"], style=f"italic {pal.fg}" if payload["status"] == "provisional" else pal.fg)
        elif kind == "arrive":
            label.append(f"  {payload['key']} ", style=pal.muted)
            label.append(f"{'▼' if position[payload['from']] < position[payload['to']] else '▲'} from {payload['from_key']}",
                         style=f"italic {pal.muted}")
        elif kind in ("from", "to"):
            label.append(f"  {payload['key']} ", style=pal.muted)
            label.append(payload["outside"]["label"], style=f"italic {pal.muted}")
        elif kind == "empty":
            label.append("No dated state in this window.", style=f"italic {pal.muted}")
        row = _cell(label, label_width)
        row.append(" ")
        row.append_text(grid.row(index, line))
        picture.lines.append(row)
        if kind == "stage":
            picture.items.append(Item(payload["id"], "stage", index, index + 1))
        elif kind in ("arrive", "from", "to"):
            picture.items.append(Item(payload["id"], "transition", index, index + 1))

    # The transitions in view, in words: kind, evidence, status, parentage.
    if edges:
        picture.lines.append(Text(""))
        head = Text(no_wrap=True)
        head.append("Transitions in this view", style=f"bold {pal.fg}")
        head.append(" · only recorded transitions connect states; date order supplies none",
                    style=f"italic {pal.muted}")
        picture.lines.append(_cell(head, width))
        for edge in edges:
            weight = weight_of(edge.get("style") or {})
            row = Text(no_wrap=True)
            row.append(f"{edge['key']}  ", style=pal.muted)
            row.append("○" if edge["from_outside"] else " ", style=pal.muted)
            row.append(edge["from_key"], style=pal.fg)
            row.append(" ")
            row.append(ARROW_SAMPLE.get(weight, "──▶"), style=pal.line)
            row.append(" ○" if edge["to_outside"] else " ", style=pal.muted)
            row.append(edge["to_key"], style=pal.fg)
            row.append(f"  {edge['kind']} · {edge['style'].get('label', '')} · {edge['status']} · "
                       f"parentage {edge['parentage']}", style=pal.muted)
            if edge.get("outside"):
                row.append(f" · {edge['outside']['label']}", style=f"italic {pal.muted}")
            index = len(picture.lines)
            picture.lines.append(_cell(row, width))
            picture.items.append(Item(edge["id"], "transition", index, index + 1))
    return picture


# --------------------------------------------------------------------------
# Recorded historical lines
# --------------------------------------------------------------------------

MAP_WEIGHTS = {
    "act-states-it": HEAVY, "book-states-it": HEAVY,  # an act or book states the parent link
    "attributed": SOLID,  # a cited scholarly attribution
    "use-continuity": DOTTED, "line-order": DOTTED,  # sequence only
}
STATION_MARKS = {"promulgated": "●", "printed": "○", "unstated": "◌"}


def paint_map(model: dict, width: int, pal: Palette) -> Picture:
    """The page's route panels (`M.panelLayout`): one per line, stations in date
    order downward, tracks across. Spacing separates stations, not years."""
    picture = Picture()
    width = max(40, width)
    for panel in model.get("panels") or []:
        tracks = max(1, panel["tracks"])
        rail = 2 + 2 * tracks
        rows: list[tuple[str, dict, str]] = [("head", panel, "")]
        node_row: dict[str, int] = {}
        for index, node in enumerate(panel["nodes"]):
            node_row[node["id"]] = len(rows)
            rows.append(("node", node, ""))
            for note in node["notes"]:
                rows.append(("note", node, note))
            if not node["notes"] and index < len(panel["nodes"]) - 1:
                rows.append(("gap", node, ""))
        grid = Grid(len(rows), rail)
        for edge in panel["edges"]:
            if edge["external"] or edge["from"] not in node_row or edge["to"] not in node_row:
                continue
            weight = DOUBLE if edge["reception"] else MAP_WEIGHTS.get(edge["evidence"], SOLID)
            group = (edge["from"], edge["to"])
            parent = next(n for n in panel["nodes"] if n["id"] == edge["from"])
            child = next(n for n in panel["nodes"] if n["id"] == edge["to"])
            pr, cr = node_row[edge["from"]], node_row[edge["to"]]
            if pr > cr:
                pr, cr = cr, pr
            cp, cc = 2 + 2 * parent["track"], 2 + 2 * child["track"]
            if cp == cc:
                grid.vertical(cc, pr + 1, cr - 1, weight, group)
                run = (cc, pr + 1, cr - 1)
            elif cp < cc:
                grid.horizontal(pr, cp + 1, cc - 1, weight, group)
                grid.put(pr, cc, L | D, weight, group)
                grid.vertical(cc, pr + 1, cr - 1, weight, group)
                run = (cc, pr + 1, cr - 1)
            else:
                grid.vertical(cp, pr + 1, cr - 1, weight, group)
                grid.put(cr, cp, U | L, weight, group)
                grid.horizontal(cr, cc + 1, cp - 1, weight, group)
                run = (cp, pr + 1, cr - 1)
            if edge["broken"] and run[2] >= run[1]:
                grid.glyph((run[1] + run[2]) // 2, run[0], "⋮", f"bold {pal.warn}")
        for index, (kind, node, note) in enumerate(rows):
            if kind == "node":
                column = 2 + 2 * node["track"]
                mark = "◉" if node["interchange"] else STATION_MARKS.get(node["kind"], "●")
                grid.glyph(index, column, mark, f"bold {pal.accent}")
        for index, (kind, payload, note) in enumerate(rows):
            out = Text(no_wrap=True)
            if kind == "head":
                out.append("╭─ ", style=pal.accent)
                out.append(payload["heading"], style=f"bold {pal.accent}")
                out.append(f"  {payload['note']}", style=f"italic {pal.muted}")
                picture.lines.append(_cell(out, width))
                continue
            rail_text = grid.row(index, pal.line)
            rail_text = Text("│", style=pal.rule) + rail_text[1:]
            out.append_text(rail_text)
            if kind == "node":
                out.append(f" {payload['date']} · {payload['kind']}  ", style=pal.muted)
                out.append(payload["title"], style=pal.fg if payload["kind"] == "promulgated" else f"italic {pal.fg}")
                out.append(f"  · {payload['count']}", style=pal.muted)
            elif kind == "note":
                out.append(f"   ↳ {note}", style=f"italic {pal.muted}")
            picture.lines.append(_cell(out, width))
            if kind == "node":
                at = len(picture.lines) - 1
                picture.items.append(Item(payload["id"], "station", at, at + 1))
        picture.lines.append(Text(""))
    return picture


# --------------------------------------------------------------------------
# Prose that wraps under its own indent
# --------------------------------------------------------------------------

# A paragraph that opens with one of these glyphs and a space hangs its
# continuation lines under the words, not under the glyph.
MARKERS = frozenset("⊘◌┃●◆◦·↳▸◀○◇◉→")


def _resolver():
    """Theme variables to concrete colours, read when drawn, so a change of
    theme follows. `$text-muted` is not a colour in Textual's table (it is
    `auto 60%`); it is read as the theme's `$muted`, as `widgets.Ink` reads it."""
    try:
        from textual._context import active_app

        variables = active_app.get().theme_variables
    except (LookupError, ImportError):
        variables = {}
    fg = variables.get("foreground", "#dddddd")
    bg = variables.get("surface") or variables.get("background", "#000000")
    cache: dict[str, Style] = {}

    def colour(name: str) -> str | None:
        if name == "text-muted":
            # As widgets.Ink does: the theme's own `$muted` is the muted ink.
            muted = variables.get("muted")
            if muted and muted.startswith("#"):
                return muted
            return blend((bg, fg), 0.6) if fg.startswith("#") and bg.startswith("#") else None
        value = variables.get(name)
        return value if value and value.startswith("#") else None

    def resolve(style: str) -> Style:
        if style not in cache:
            words = []
            for word in style.split():
                if word.startswith("$"):
                    found = colour(word[1:])
                    if found:
                        words.append(found)
                else:
                    words.append(word)
            try:
                cache[style] = Style.parse(" ".join(words)) if words else Style()
            except Exception:  # noqa: BLE001 - an unreadable style draws plain, never fails the page
                cache[style] = Style()
        return cache[style]

    return resolve


class Doc:
    """Text built like `Ink` (`doc(text, style)`, `doc.line(text, style)`), whose
    paragraphs wrap under their own leading indent. Styles may name theme
    variables; they are resolved only when the text is drawn."""

    def __init__(self) -> None:
        self.paragraphs: list[list[tuple[str, str]]] = []
        self.current: list[tuple[str, str]] = []

    def __call__(self, text: object, style: str = "") -> "Doc":
        text = str(text)
        if text:
            self.current.append((text, style))
        return self

    def line(self, text: object = "", style: str = "") -> "Doc":
        self(text, style)
        self.paragraphs.append(self.current)
        self.current = []
        return self

    def __bool__(self) -> bool:
        return bool(self.paragraphs or self.current)

    def content(self) -> "Doc":
        return self

    def __rich_console__(self, console, options):
        from rich.padding import Padding
        from rich.table import Table

        resolve = _resolver()
        for parts in self.paragraphs + ([self.current] if self.current else []):
            indent, marker, rest = self._split(parts)
            body = Text(no_wrap=False, overflow="fold")
            for words, style in rest:
                body.append(words, style=resolve(style))
            if marker is None:
                yield Padding(body, (0, 0, 0, indent)) if indent else body
                continue
            grid = Table.grid(padding=0)
            grid.add_column(width=len(marker[0]), no_wrap=True)
            grid.add_column(ratio=1, overflow="fold")  # a long identifier folds; nothing is cut off
            grid.add_row(Text(marker[0], style=resolve(marker[1])), body)
            yield Padding(grid, (0, 0, 0, indent)) if indent else grid

    @staticmethod
    def _split(parts: list[tuple[str, str]]):
        """Leading spaces become the indent; a leading marker glyph hangs."""
        indent = 0
        rest = list(parts)
        while rest:
            words, style = rest[0]
            stripped = words.lstrip(" ")
            indent += len(words) - len(stripped)
            if stripped:
                rest[0] = (stripped, style)
                break
            rest.pop(0)
        marker = None
        if rest:
            words, style = rest[0]
            if len(words) >= 2 and words[0] in MARKERS and words[1] == " ":
                marker = (words[:2], style)
                tail = words[2:]
                rest = ([(tail, style)] if tail else []) + rest[1:]
        return indent, marker, rest


# --------------------------------------------------------------------------
# The widget
# --------------------------------------------------------------------------

Painter = Callable[[dict, int, Palette], Picture]


class Drawing(ScrollView, can_focus=True, inherit_bindings=False):
    """A picture of rows with one item chosen, scrolled with the cursor.

    The surface hands it a model and a painter; it lays the picture out again
    whenever its width or the theme changes. Up and down move between items
    (stages, transitions, stations); Enter asks for the chosen one in full; a
    click chooses the item under it.
    """

    DEFAULT_CSS = """
    Drawing { height: 1fr; width: 1fr; scrollbar-size-vertical: 1; overflow-x: hidden; }
    """
    BINDINGS = [
        Binding("up", "move(-1)", "previous item", show=False),
        Binding("down", "move(1)", "next item", show=False),
        Binding("pageup", "page(-1)", "page up", show=False),
        Binding("pagedown", "page(1)", "page down", show=False),
        Binding("home", "edge(0)", "first item", show=False),
        Binding("end", "edge(-1)", "last item", show=False),
        Binding("enter", "open", "read in full", show=False),
    ]

    class Chosen(Message):
        """The cursor came to rest on an item."""

        def __init__(self, drawing: "Drawing", item: Item) -> None:
            super().__init__()
            self.drawing = drawing
            self.item = item

        @property
        def control(self) -> "Drawing":
            return self.drawing

    class Opened(Message):
        """The reader asked for the item whole (Enter, or a second click)."""

        def __init__(self, drawing: "Drawing", item: Item) -> None:
            super().__init__()
            self.drawing = drawing
            self.item = item

        @property
        def control(self) -> "Drawing":
            return self.drawing

    def __init__(self, painter: Painter, surface: str, **options) -> None:
        super().__init__(**options)
        self.painter = painter
        self.surface = surface
        self.model: dict | None = None
        self.picture = Picture()
        self.chosen = 0
        self._laid: tuple | None = None
        self._strips: dict[int, Strip] = {}

    # --- content ---------------------------------------------------------

    def show(self, model: dict, keep: str | None = None) -> None:
        self.model = model
        self._laid = None
        self._layout()
        self.chosen = 0
        if keep:
            for index, item in enumerate(self.picture.items):
                if item.key == keep:
                    self.chosen = index
                    break
        self.refresh()
        # The new height is known only once laid out; follow the cursor after that.
        self.call_after_refresh(self._follow, True)
        if self.picture.items:
            self.post_message(self.Chosen(self, self.picture.items[self.chosen]))

    def current(self) -> Item | None:
        if 0 <= self.chosen < len(self.picture.items):
            return self.picture.items[self.chosen]
        return None

    def choose(self, key: str) -> bool:
        for index, item in enumerate(self.picture.items):
            if item.key == key:
                self._set(index)
                return True
        return False

    def _layout(self) -> None:
        width = max(40, self.scrollable_content_region.width or self.size.width or 100)
        theme = self.app.theme
        if self._laid == (width, theme) or self.model is None:
            return
        self._laid = (width, theme)
        self.picture = self.painter(self.model, width, Palette.of(self.app, self.surface))
        self._strips.clear()
        self.virtual_size = Size(width, len(self.picture.lines))

    def on_resize(self) -> None:
        if self.model is not None:
            self._layout()
            self.refresh()

    # --- drawing ---------------------------------------------------------

    def render_line(self, y: int) -> Strip:
        self._layout()
        width = self.scrollable_content_region.width
        base = self.rich_style
        index = self._index(y)
        if index >= len(self.picture.lines):
            return Strip.blank(width, base)
        strip = self._strips.get(index)
        if strip is None:
            text = self.picture.lines[index]
            segments = list(text.render(self.app.console))
            strip = Strip(segments).crop_extend(0, width, None)
            self._strips[index] = strip
        item = self.current()
        if item and item.top <= index < item.bottom:
            pal = Palette.of(self.app, self.surface)
            strip = strip.apply_style(Style(bgcolor=pal.cursor if self.has_focus else pal.idle))
        return strip.apply_style(base).crop_extend(0, width, base)

    def _index(self, y: int) -> int:
        """The picture row drawn at screen row `y`: the header rows stay put."""
        header = self.picture.header
        return y if y < header else round(self.scroll_offset.y) + y

    # --- moving ----------------------------------------------------------

    def _set(self, index: int) -> None:
        if not self.picture.items:
            return
        index = max(0, min(len(self.picture.items) - 1, index))
        if index == self.chosen:
            return
        self.chosen = index
        self._follow()
        self.refresh()
        self.post_message(self.Chosen(self, self.picture.items[index]))

    def _follow(self, center: bool = False) -> None:
        item = self.current()
        if item is None:
            return
        height = max(1, self.scrollable_content_region.height)
        header = self.picture.header
        top = self.scroll_offset.y
        if center:
            self.scroll_to(y=max(0, item.top - header - (height - header) // 3), animate=False, immediate=True)
        elif item.top < top + header:
            self.scroll_to(y=max(0, item.top - header), animate=False, immediate=True)
        elif item.bottom > top + height:
            self.scroll_to(y=item.bottom - height, animate=False, immediate=True)

    def action_move(self, step: int) -> None:
        self._set(self.chosen + step)

    def action_page(self, step: int) -> None:
        height = max(1, self.scrollable_content_region.height)
        item = self.current()
        if item is None:
            return
        target = item.top + step * height
        best = min(range(len(self.picture.items)), key=lambda i: abs(self.picture.items[i].top - target))
        self._set(best)

    def action_edge(self, which: int) -> None:
        self._set(0 if which == 0 else len(self.picture.items) - 1)

    def action_open(self) -> None:
        item = self.current()
        if item:
            self.post_message(self.Opened(self, item))

    def on_click(self, event) -> None:
        index = self._index(event.y)
        for position, item in enumerate(self.picture.items):
            if item.top <= index < item.bottom:
                if position == self.chosen and event.chain >= 2:
                    self.action_open()
                self._set(position)
                return

    def on_focus(self) -> None:
        self.refresh()

    def on_blur(self) -> None:
        self.refresh()
