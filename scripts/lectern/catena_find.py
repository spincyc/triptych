"""Find a canonical chapter with commentary in the shared holdings index."""
from __future__ import annotations

import re

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .widgets import Ink


class EnglishToggle(Static):
    """Explicit ☐ / ☑ toggle that keeps its distinction in --plain and takes 1 row."""

    can_focus = True
    value = reactive(False)
    BINDINGS = [Binding("space,enter", "toggle", "toggle", show=False)]

    class Changed(Message):
        def __init__(self, toggle: "EnglishToggle", value: bool) -> None:
            super().__init__()
            self.toggle = toggle
            self.value = value

    def __init__(self, label: str, **options) -> None:
        super().__init__("", **options)
        self.label_text = label

    def on_mount(self) -> None:
        self._redraw()

    def watch_value(self) -> None:
        self._redraw()

    def _redraw(self) -> None:
        mark = "☑" if self.value else "☐"
        ink = Ink()(mark, "bold $catena-color")(" " + self.label_text)
        self.update(ink.content())

    def action_toggle(self) -> None:
        self.value = not self.value
        self.post_message(self.Changed(self, self.value))

    def on_click(self) -> None:
        self.focus()
        self.action_toggle()


class CommentaryFinder(ModalScreen[tuple[str, int] | None]):
    DEFAULT_CSS = """
    CommentaryFinder { align: center middle; background: $background 65%; }
    CommentaryFinder > Vertical {
        width: 76; max-width: 96%; height: 85%; max-height: 95%;
        border: round $catena-color;
        background: $surface; padding: 0 1;
    }
    CommentaryFinder Input {
        border: none; height: 1; width: 1fr; padding: 0 1;
        background: $panel; margin: 0;
    }
    CommentaryFinder Input:focus { border: none; background: $catena-color 22%; }
    CommentaryFinder EnglishToggle {
        height: 1; width: 1fr; padding: 0 1; margin: 0 0 1 0;
    }
    CommentaryFinder EnglishToggle:focus { background: $catena-color 30%; text-style: bold; }
    CommentaryFinder OptionList {
        border: none; background: transparent; padding: 0; height: 1fr;
    }
    CommentaryFinder OptionList:focus { border: none; }
    """
    BINDINGS = [Binding("escape", "dismiss(None)", "cancel")]

    def __init__(self, books: list[dict]) -> None:
        super().__init__()
        self.books = books
        self.matches: list[tuple[str, int]] = []

    def compose(self) -> ComposeResult:
        with Vertical() as box:
            box.border_title = "Find commentary · opens a chapter in all voices"
            box.border_subtitle = "Tab move · Space filter · Enter open · Esc close"
            yield Input(placeholder="Book or reference, e.g. Mark 10")
            yield EnglishToggle("Chapters with English excerpts")
            yield OptionList()

    def on_mount(self) -> None:
        self.filter_chapters()
        self.query_one(Input).focus()

    @on(Input.Changed)
    @on(EnglishToggle.Changed)
    def filter_chapters(self) -> None:
        query = self.query_one(Input).value.strip().casefold()
        reference = re.fullmatch(r"(.*?[^\d\s])\s*(\d+)", query)
        book_query = (reference[1] if reference else query).replace(" ", "")
        chapter = reference[2].lstrip("0") if reference else None
        english = self.query_one(EnglishToggle).value
        self.matches.clear()
        options = []
        for book in self.books:
            names = (book["token"].casefold(), book["name"].casefold().replace(" ", ""))
            if not any(book_query in name for name in names):
                continue
            for row in book["chapters"]:
                if (chapter is not None and chapter != str(row["chapter"])) or (english and not row["english"]):
                    continue
                label = Ink()(f"{book['name']} {row['chapter']}", "bold $catena-color")
                count = row["fragments"]
                label(f"   {count} excerpt{'s' if count != 1 else ''} · {row['english']} in English")
                options.append(Option(label.content(), id=str(len(self.matches))))
                self.matches.append((book["token"], row["chapter"]))
        listing = self.query_one(OptionList)
        listing.clear_options()
        if options:
            listing.add_options(options)
            listing.highlighted = 0
        else:
            message = ("No indexed chapters match these filters." if self.books else
                       "This index lists no commentary chapters. Use g to open a Scripture reference.")
            listing.add_option(Option(message, disabled=True))

    def on_input_submitted(self) -> None:
        if len(self.matches) == 1:
            self.dismiss(self.matches[0])
        elif self.matches:
            self.query_one(OptionList).focus()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        if event.option.id is not None:
            self.dismiss(self.matches[int(event.option.id)])
