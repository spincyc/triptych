"""Find a canonical chapter with commentary in the shared holdings index."""
from __future__ import annotations

import re

from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Checkbox, Input, OptionList
from textual.widgets.option_list import Option

from .widgets import Ink


class CommentaryFinder(ModalScreen[tuple[str, int] | None]):
    DEFAULT_CSS = """
    CommentaryFinder { align: center middle; background: $background 65%; }
    CommentaryFinder > Vertical {
        width: 76; max-width: 96%; height: 85%; border: round $catena-color;
        background: $surface; padding: 0 1;
    }
    CommentaryFinder Input, CommentaryFinder Checkbox { height: 3; width: 1fr; }
    CommentaryFinder OptionList { height: 1fr; }
    """
    BINDINGS = [Binding("escape", "dismiss(None)", "cancel")]

    def __init__(self, books: list[dict]) -> None:
        super().__init__()
        self.books = books
        self.matches: list[tuple[str, int]] = []

    def compose(self) -> ComposeResult:
        with Vertical() as box:
            box.border_title = "Find commentary · opens a chapter in all voices"
            box.border_subtitle = "Tab move · Enter open · Esc close"
            yield Input(placeholder="Book or reference, e.g. Mark 10")
            yield Checkbox("Chapters with English excerpts")
            yield OptionList()

    def on_mount(self) -> None:
        self.filter_chapters()
        self.query_one(Input).focus()

    @on(Input.Changed)
    @on(Checkbox.Changed)
    def filter_chapters(self) -> None:
        query = self.query_one(Input).value.strip().casefold()
        reference = re.fullmatch(r"(.*?[^\d\s])\s*(\d+)", query)
        book_query = (reference[1] if reference else query).replace(" ", "")
        chapter = reference[2].lstrip("0") if reference else None
        english = self.query_one(Checkbox).value
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
