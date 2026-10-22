"""Small overlays: a question with one answer, and a page of text to read."""
from __future__ import annotations

from rich.console import RenderableType
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Input, Static

from .widgets import titled


class Ask(ModalScreen[str | None]):
    """One line of input; Enter answers, Escape declines."""

    DEFAULT_CSS = """
    Ask { align: center middle; }
    Ask > Vertical {
        width: 64; max-width: 95%; height: auto;
        border: round $accent; background: $surface; padding: 0 1;
    }
    Ask Static { color: $text-muted; padding: 0 0 1 0; }
    """
    BINDINGS = [Binding("escape", "decline", "cancel")]

    def __init__(self, title: str, hint: str = "", value: str = "") -> None:
        super().__init__()
        self.title_text = title
        self.hint = hint
        self.value = value

    def compose(self) -> ComposeResult:
        with Vertical() as box:
            box.border_title = titled(None, self.title_text)
            if self.hint:
                yield Static(self.hint)
            yield Input(value=self.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip() or None)

    def action_decline(self) -> None:
        self.dismiss(None)


class Reading(ModalScreen[str | None]):
    """A long text over the surface, scrolled with the usual keys.

    `n` and `p` ask the surface for the next or previous item, so a reader can
    walk a chain without closing the page.
    """

    DEFAULT_CSS = """
    Reading { align: center middle; }
    Reading > VerticalScroll {
        width: 96; max-width: 96%; height: 92%;
        border: round $accent; background: $surface; padding: 1 2;
        scrollbar-size-vertical: 1;
    }
    """
    BINDINGS = [
        Binding("escape,q", "dismiss(None)", "close"),
        Binding("n", "dismiss('next')", "next"),
        Binding("p", "dismiss('previous')", "previous"),
        Binding("s", "dismiss('source')", "source library"),
    ]

    def __init__(self, title: str, body: RenderableType, subtitle: str = "", *, walks: bool = True,
                 source: bool = False) -> None:
        super().__init__()
        self.title_text = title
        self.body = body
        self.subtitle = subtitle
        self.walks = walks
        self.source = source

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if action == "dismiss" and parameters in (("next",), ("previous",)):
            return self.walks
        if action == "dismiss" and parameters == ("source",):
            return self.source
        return True

    def compose(self) -> ComposeResult:
        with VerticalScroll() as box:
            box.border_title = self.title_text
            box.border_subtitle = self.subtitle or "esc close · n next · p previous"
            yield Static(self.body)

    def on_mount(self) -> None:
        self.query_one(VerticalScroll).focus()


class Pick(ModalScreen[str | None]):
    """One choice among named options; nothing is preselected for the reader."""

    DEFAULT_CSS = """
    Pick { align: center middle; }
    Pick > Vertical {
        width: 80; max-width: 95%; height: auto; max-height: 85%;
        border: round $accent; background: $surface; padding: 0 1;
    }
    Pick Static { color: $text-muted; padding: 0 0 1 0; }
    Pick OptionList { border: none; background: transparent; padding: 0; height: auto; max-height: 30; }
    Pick OptionList:focus { border: none; }
    """
    BINDINGS = [Binding("escape", "decline", "cancel")]

    def __init__(self, title: str, options: list[tuple[str, object]], hint: str = "") -> None:
        super().__init__()
        self.title_text = title
        self.options = options
        self.hint = hint

    def compose(self) -> ComposeResult:
        from textual.widgets import OptionList
        from textual.widgets.option_list import Option

        with Vertical() as box:
            box.border_title = titled(None, self.title_text)
            if self.hint:
                yield Static(self.hint)
            yield OptionList(*[Option(label, id=str(index)) for index, (_, label) in enumerate(self.options)])

    def on_option_list_option_selected(self, event) -> None:
        self.dismiss(self.options[int(event.option.id)][0])

    def action_decline(self) -> None:
        self.dismiss(None)
