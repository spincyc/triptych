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

    ROWS = 1  # single bar row keeps the strip compact (max 4 content rows)

    def _layout(self, width: int) -> tuple[int, list[tuple[int, int]]]:
        """Return (stride, [(start_bin, end_bin), ...]) fitting in at most 2 bands."""
        band = max(10, width)
        total = len(self.cells)
        if not total:
            return 1, []
        if total <= band:
            return 1, [(0, total)]
        # Fold long books (e.g. Psalms 150) neatly into 2 balanced bands (4 rows max).
        stride = max(1, -(-total // (2 * band)))
        bins = -(-total // stride)
        if bins <= band:
            return stride, [(0, bins)]
        half = (bins + 1) // 2
        return stride, [(0, half), (half, bins)]

    def get_content_height(self, container, viewport, width: int) -> int:
        _, bands = self._layout(width)
        if len(bands) <= 1:
            return 3
        return 4

    def _axis_line(self, start_bin: int, end_bin: int, stride: int, band: int,
                   chosen_col: int | None, muted: str, pointer: str) -> Text:
        """Render chapter axis labels without dropping the final chapter (e.g. 50, 150)."""
        count = end_bin - start_bin
        total = len(self.cells)
        width = max(count, min(band, count + 3))
        chars = [" "] * width
        styles: list[Style | None] = [None] * width
        muted_style = Style.parse(muted)
        pointer_style = Style(color=pointer, bold=True)

        def write(col: int, text: str, style: Style) -> bool:
            if col < 0 or col + len(text) > width:
                return False
            if any(chars[i] != " " for i in range(col, col + len(text))):
                return False
            for i, ch in enumerate(text):
                chars[col + i] = ch
                styles[col + i] = style
            return True

        # Place the chosen pointer first when axis and pointer share a row.
        if chosen_col is not None and 0 <= chosen_col < width:
            chars[chosen_col] = "▲"
            styles[chosen_col] = pointer_style

        # Always try to place the last chapter of the book on the final band so 50 / 150 never drops.
        last_chapter = min(total, end_bin * stride)
        if last_chapter == total and (last_chapter % 10 == 0 or last_chapter >= 10):
            label = str(last_chapter)
            pos = count - 1
            if not write(pos, label, muted_style):
                # Right-align flush with the last cell of the band when at the edge.
                write(max(0, count - len(label)), label, muted_style)

        for offset in range(count):
            lo = (start_bin + offset) * stride + 1
            hi = min(total, lo + stride - 1)
            chapter = None
            if lo == 1:
                chapter = 1
            else:
                for cand in range(lo, hi + 1):
                    if cand % 10 == 0:
                        chapter = cand
                        break
            if chapter is None:
                continue
            label = str(chapter)
            # Keep at least 1 space before the next label already placed (e.g. final chapter).
            col = offset
            if chosen_col is not None and col == chosen_col:
                col = offset + 1
            if col + len(label) <= width:
                if col > 0 and chars[col - 1] != " " and chars[col - 1] != "▲":
                    continue
                if col + len(label) < width and chars[col + len(label)] != " ":
                    continue
                write(col, label, muted_style)

        axis = Text()
        for ch, st in zip(chars, styles):
            axis.append(ch, style=st)
        return axis

    def render(self) -> Text:
        out = Text()
        if not self.cells:
            return out
        band = self._band()
        stride, bands = self._layout(band)
        peak = max((cell.value for cell in self.cells), default=0)
        variables = self.app.theme_variables
        pointer = variables.get("hotkey", "#ff5f6d")
        muted = variables.get("muted", "#777777")
        levels = 8
        compact_bands = len(bands) > 1
        for start_bin, end_bin in bands:
            bar = Text()
            marks = Text()
            chosen_col: int | None = None
            for offset, bin_index in enumerate(range(start_bin, end_bin)):
                lo = bin_index * stride
                hi = min(len(self.cells), lo + stride)
                group = self.cells[lo:hi]
                value = max(cell.value for cell in group)
                faint = any(cell.faint for cell in group)
                broken = any(cell.broken for cell in group)
                chapter = self.chosen if (lo + 1 <= self.chosen <= hi) else lo + 1
                is_chosen = lo + 1 <= self.chosen <= hi
                if is_chosen:
                    chosen_col = offset
                click = Style.from_meta({"chapter": chapter})
                fraction = value / peak if peak and value else 0
                level = max(1, round(fraction * levels)) if value else 0
                tint = Style.parse(blend(METER_STOPS, fraction)) + click
                if broken:
                    bar.append("×", style=Style.parse(variables.get("error", "red")) + click)
                elif not value:
                    bar.append("·" if faint else " ", style=Style.parse(muted) + click)
                else:
                    bar.append(BLOCKS[min(8, level) - 1], style=tint)
                if not compact_bands:
                    marks.append("▲" if is_chosen else " ", style=Style(color=pointer, bold=True))
            axis = self._axis_line(
                start_bin, end_bin, stride, band,
                chosen_col if compact_bands else None,
                muted, pointer,
            )
            rows = (bar, axis) if compact_bands else (bar, marks, axis)
            for row in rows:
                out.append_text(row)
                out.append("\n")
        out.rstrip()
        return out

    def on_click(self, event) -> None:
        chapter = event.style.meta.get("chapter") if event.style else None
        if chapter:
            self.post_message(self.Picked(int(chapter)))
