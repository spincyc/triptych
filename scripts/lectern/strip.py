"""A chapter strip: one cell per chapter of a book, btop's graph turned sideways."""
from __future__ import annotations

from dataclasses import dataclass

from rich.style import Style
from rich.text import Text
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget

from .theme import METER_STOPS, blend

BLOCKS = "▁▂▃▄▅▆▇█"


@dataclass(frozen=True)
class Cell:
    """What one chapter holds, as the surface reports it."""

    value: int  # how much of the measured thing it holds
    faint: bool = False  # holds something lesser (only leads, say)
    broken: bool = False  # its record could not be read


class ChapterStrip(Widget):
    """Bars for each chapter, the chosen one pointed at, numbered every tenth.

    A chapter with nothing is a blank, one with only something lesser a dot, and
    one whose record could not be read a cross: the three are never one glyph.
    """

    DEFAULT_CSS = """
    ChapterStrip { height: auto; min-height: 3; width: 1fr; }
    """
    chosen = reactive(1)

    class Picked(Message):
        def __init__(self, chapter: int) -> None:
            super().__init__()
            self.chapter = chapter

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.cells: list[Cell] = []

    def show(self, cells: list[Cell], chosen: int) -> None:
        self.cells = cells
        self.chosen = chosen
        self.refresh(layout=True)

    def watch_chosen(self) -> None:
        self.refresh()

    def _band(self) -> int:
        return max(10, self.size.width or 80)

    ROWS = 2  # bar rows: two give sixteen heights, as btop stacks its graphs

    def get_content_height(self, container, viewport, width: int) -> int:
        band = max(10, width)
        bands = max(1, -(-len(self.cells) // band))
        return bands * (self.ROWS + 2)

    def render(self) -> Text:
        out = Text()
        if not self.cells:
            return out
        band = self._band()
        peak = max((cell.value for cell in self.cells), default=0)
        variables = self.app.theme_variables
        pointer = variables.get("hotkey", "#ff5f6d")
        muted = variables.get("muted", "#777777")
        levels = 8 * self.ROWS
        for start in range(0, len(self.cells), band):
            chunk = self.cells[start : start + band]
            bars = [Text() for _ in range(self.ROWS)]
            marks, axis = Text(), Text()
            for offset, cell in enumerate(chunk):
                chapter = start + offset + 1
                click = Style.from_meta({"chapter": chapter})
                fraction = cell.value / peak if peak and cell.value else 0
                level = max(1, round(fraction * levels)) if cell.value else 0
                tint = Style.parse(blend(METER_STOPS, fraction)) + click
                for row in range(self.ROWS):
                    floor = (self.ROWS - 1 - row) * 8  # the bottom row is the last
                    if row == self.ROWS - 1 and cell.broken:
                        bars[row].append("×", style=Style.parse(variables.get("error", "red")) + click)
                    elif row == self.ROWS - 1 and not cell.value:
                        bars[row].append("·" if cell.faint else " ", style=Style.parse(muted) + click)
                    elif level > floor:
                        bars[row].append(BLOCKS[min(8, level - floor) - 1], style=tint)
                    else:
                        bars[row].append(" ", style=click)
                marks.append("▲" if chapter == self.chosen else " ", style=Style(color=pointer, bold=True))
            position = 0
            while position < len(chunk):
                chapter = start + position + 1
                label = str(chapter)
                if (chapter == 1 or chapter % 10 == 0) and position + len(label) <= len(chunk):
                    axis.append(label, style=muted)
                    position += len(label)
                    continue
                axis.append(" ")
                position += 1
            for row in (*bars, marks, axis):
                out.append_text(row)
                out.append("\n")
        out.rstrip()
        return out

    def on_click(self, event) -> None:
        chapter = event.style.meta.get("chapter") if event.style else None
        if chapter:
            self.post_message(self.Picked(int(chapter)))
