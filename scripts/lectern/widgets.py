"""The few visual pieces every surface shares: the box, the meter, the strip."""
from __future__ import annotations

from typing import Iterable, Sequence

from rich.text import Text
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from .theme import METER_STOPS, blend

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def titled(key: str | None, title: str) -> str:
    """A box title in the btop manner: the key that reaches it, then its name."""
    if not key:
        return f"[b]{title}[/]"
    return f"[$hotkey]{key.translate(SUPERSCRIPT)}[/][b]{title}[/]"


class Panel(Vertical):
    """A rounded, titled box; the frame colour says which surface it belongs to."""

    DEFAULT_CSS = """
    Panel {
        border: round $panel-lighten-2;
        border-title-color: $foreground;
        border-subtitle-color: $text-muted;
        padding: 0 1;
        height: 1fr;
    }
    Panel:focus-within { border: round $accent 80%; }
    """

    def __init__(self, *children: Widget, title: str = "", key: str | None = None,
                 subtitle: str = "", **options) -> None:
        super().__init__(*children, **options)
        self.border_title = titled(key, title)
        if subtitle:
            self.border_subtitle = subtitle

    def retitle(self, title: str, key: str | None = None) -> None:
        self.border_title = titled(key, title)


class ScrollPanel(VerticalScroll):
    """A Panel whose body scrolls; used for reading text."""

    DEFAULT_CSS = """
    ScrollPanel {
        border: round $panel-lighten-2;
        border-title-color: $foreground;
        border-subtitle-color: $text-muted;
        padding: 0 1;
        height: 1fr;
        scrollbar-size-vertical: 1;
    }
    ScrollPanel:focus, ScrollPanel:focus-within { border: round $accent 80%; }
    """

    def __init__(self, *children: Widget, title: str = "", key: str | None = None,
                 subtitle: str = "", **options) -> None:
        super().__init__(*children, **options)
        self.border_title = titled(key, title)
        if subtitle:
            self.border_subtitle = subtitle

    def retitle(self, title: str, key: str | None = None) -> None:
        self.border_title = titled(key, title)


def meter(fraction: float, width: int, *, empty: str = "#2a2d36") -> Text:
    """A btop meter: filled cells take the gradient colour of their position."""
    width = max(1, width)
    filled = round(min(1.0, max(0.0, fraction)) * width)
    bar = Text()
    for cell in range(width):
        if cell < filled:
            bar.append("■", style=blend(METER_STOPS, cell / max(1, width - 1)))
        else:
            bar.append("■", style=empty)
    return bar


def meter_line(label: str, held: int, total: int | None, width: int, *,
               label_width: int = 12, empty: str = "#2a2d36", unit: str = "") -> Text:
    """`label ■■■■□□□ 12/40`, with the count always printed beside the bar."""
    line = Text(f"{label[:label_width]:<{label_width}} ", style="bold")
    if total:
        line.append_text(meter(held / total, width, empty=empty))
        line.append(f" {held}/{total}{unit}")
    else:
        line.append("·" * width, style="dim")
        line.append(f" {held}{unit} (no denominator stated)", style="dim")
    return line


BLOCKS = " ▁▂▃▄▅▆▇█"


def strip(values: Sequence[float], *, width: int | None = None, top: float | None = None,
          colour: bool = True) -> Text:
    """One row of block glyphs, one per value, scaled to the largest.

    A zero is drawn as a dot, so "nothing here" never looks like "a little here".
    """
    values = list(values)
    if width and len(values) > width:
        bucket = len(values) / width
        values = [max(values[int(i * bucket): max(int(i * bucket) + 1, int((i + 1) * bucket))])
                  for i in range(width)]
    peak = top if top is not None else max(values, default=0)
    line = Text()
    for value in values:
        if not value:
            line.append("·", style="#3a3d48")
            continue
        fraction = value / peak if peak else 0
        glyph = BLOCKS[max(1, min(8, round(fraction * 8)))]
        line.append(glyph, style=blend(METER_STOPS, fraction) if colour else "")
    return line


class Busy(Static):
    """A one-line note that work is under way, with what is being asked."""

    DEFAULT_CSS = """
    Busy { color: $text-muted; height: auto; }
    """
    frame = reactive(0)
    SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

    def __init__(self, what: str = "", **options) -> None:
        super().__init__("", **options)
        self.what = what

    def on_mount(self) -> None:
        self.set_interval(0.08, self._tick)
        self._paint()

    def _tick(self) -> None:
        self.frame = (self.frame + 1) % len(self.SPIN)

    def watch_frame(self) -> None:
        self._paint()

    def _paint(self) -> None:
        self.update(Text.assemble((self.SPIN[self.frame], "bold"), "  ", self.what))


def lines(*rows: Iterable[Text | str]) -> Text:
    """Join renderables into one Text, one per line."""
    out = Text()
    first = True
    for row in rows:
        if not first:
            out.append("\n")
        first = False
        if isinstance(row, Text):
            out.append_text(row)
        else:
            out.append(str(row))
    return out


class Ink:
    """Builds theme-aware text: styles may name theme variables ($accent, $catena-color),
    which resolve when drawn and follow a change of theme."""

    def __init__(self) -> None:
        self.parts: list = []

    def __call__(self, text: object, style: str = "") -> "Ink":
        text = str(text)
        if text:
            self.parts.append((text, style) if style else text)
        return self

    def line(self, text: object = "", style: str = "") -> "Ink":
        self(text, style)
        self.parts.append("\n")
        return self

    def __bool__(self) -> bool:
        return bool(self.parts)

    def content(self):
        from textual.content import Content

        return Content.assemble(*self.parts)
