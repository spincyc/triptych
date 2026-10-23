"""The few visual pieces every surface shares: the box, the meter, the ink."""
from __future__ import annotations

from textual.containers import Vertical, VerticalScroll
from textual.widget import Widget

from .theme import METER_STOPS, blend

SUPERSCRIPT = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def literal(text: object) -> str:
    """Data, made safe to set inside markup: every bracket kept as itself.

    Textual's own `escape` leaves "[Basel]" alone, and its parser then reads it
    as a tag and drops the word; so every bracket is escaped, and a closing
    backslash is kept off the tag that follows it."""
    text = str(text).replace("[", "\\[")
    return text + " " if text.endswith("\\") else text


def count(number: int, word: str) -> str:
    """"1 edition", "2 editions": the number, and the word it agrees with."""
    return f"{number:,} {word if number == 1 else word + 's'}"


def titled(key: str | None, title: str) -> str:
    """A box title in the btop manner: the key that reaches it, then its name.

    The name is data, escaped: a catalogue title such as "([Basel] for
    Christoph Thum, 1510)" must not be read as markup and lose its words."""
    title = literal(title)
    if not key:
        return f"[b]{title}[/]"
    return f"[$hotkey]{key.translate(SUPERSCRIPT)}[/][b]{title}[/]"


class Panel(Vertical):
    """A rounded, titled box; the frame colour says which surface it belongs to."""

    DEFAULT_CSS = """
    Panel {
        border: round $rule;
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
        border: round $rule;
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


def meter(ink: "Ink", held: int, total: int, width: int) -> "Ink":
    """A btop meter in theme-aware cells; the count is always written beside it."""
    filled = round(min(1.0, held / total) * width) if total else 0
    for cell in range(width):
        # Empty cells take another glyph, so the count is legible without colour.
        if cell < filled:
            ink("■", blend(METER_STOPS, cell / max(1, width - 1)))
        else:
            ink("·", "$meter-empty")
    return ink


def fitted(parts: list[tuple[str, str]], width: int, ink: "Ink | None" = None) -> "Ink":
    """Runs of text cut to one line of `width` cells, the cut marked with an ellipsis."""
    ink = ink if ink is not None else Ink()
    room = width
    for text, style in parts:
        if room <= 0:
            break
        if len(text) > room:
            ink(text[: max(0, room - 1)] + "…", style)
            room = 0
        else:
            ink(text, style)
            room -= len(text)
    return ink


class Ink:
    """Builds theme-aware text: styles may name theme variables ($accent, $catena-color),
    which resolve when drawn and follow a change of theme."""

    def __init__(self) -> None:
        self.parts: list = []

    def __call__(self, text: object, style: str = "") -> "Ink":
        text = str(text)
        if text:
            # In a content style `$text-muted` resolves to an "auto" colour and
            # draws as plain white; the theme's own `$muted` is the muted ink.
            style = style.replace("$text-muted", "$muted")
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
