"""Small overlays: a question with one answer, and a page of text to read."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from rich.console import RenderableType
from textual.app import ComposeResult, SuspendNotSupported
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Input, Static

from .widgets import literal, titled


class Ask(ModalScreen[str | None]):
    """One line of input; Enter answers, Escape declines."""

    DEFAULT_CSS = """
    Ask { align: center middle; background: $background 65%; }
    Ask > Vertical {
        width: 64; max-width: 95%; height: auto;
        border: round $primary 65%; background: $surface; padding: 1 2;
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
            box.border_subtitle = "enter apply · esc cancel"
            if self.hint:
                yield Static(self.hint)
            yield Input(value=self.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Enter answers, even with nothing (an empty answer clears); only
        # Escape declines.
        self.dismiss(event.value.strip())

    def action_decline(self) -> None:
        self.dismiss(None)


class Reading(ModalScreen[str | None]):
    """A long text over the surface, scrolled with the usual keys.

    `n` and `p` ask the surface for the next or previous item, so a reader can
    walk a chain without closing the page.
    """

    DEFAULT_CSS = """
    Reading { align: center middle; background: $background 65%; }
    Reading > VerticalScroll {
        width: 96; max-width: 96%; height: 92%;
        border: round $primary 65%; background: $surface; padding: 1 3;
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
            box.border_title = titled(None, self.title_text)
            hint = "esc close · n next · p previous" if self.walks else "esc close"
            box.border_subtitle = literal(self.subtitle or hint)
            yield Static(self.body)

    def on_mount(self) -> None:
        self.query_one(VerticalScroll).focus()


def terminal_browser() -> str | None:
    for name in ("lynx", "w3m", "links", "elinks"):
        installed = shutil.which(name)
        if installed:
            return installed
        local = Path.home() / ".local" / "bin" / name
        if local.is_file() and os.access(local, os.X_OK):
            return str(local)
    return None


def browse_in_terminal(app, url: str) -> None:
    browser = terminal_browser()
    if browser:
        try:
            with app.suspend():
                subprocess.run([browser, url], check=False)
        except (OSError, SuspendNotSupported) as error:
            app.notify(str(error), severity="warning")


class MissalSource(Reading):
    """An identified external missal witness, usable by URL or keyboard."""

    BINDINGS = [Binding("o", "open_witness", "open source"), Binding("c", "copy_url", "copy URL"),
                Binding("t", "terminal_witness", "terminal browser")]

    def __init__(self, title: str, link: dict) -> None:
        from .missal import source_rights, witness_label
        from .widgets import Ink

        self.url = link["url"]
        ink = Ink().line(title, "bold").line(witness_label(link)).line(link["locus"])
        if link.get("rights_status"):
            ink.line(source_rights(link["rights_status"]), "$text-muted")
        if link.get("prayer_roles"):
            ink.line(" · ".join(link["prayer_roles"]))
        ink.line(link["source_id"], "$text-muted").line().line(self.url)
        hint = "o open · c copy URL" + (" · t terminal browser" if terminal_browser() else "")
        super().__init__("Missal source", ink.content(), hint + " · esc close", walks=False)

    def action_terminal_witness(self) -> None:
        browse_in_terminal(self.app, self.url)

    def action_open_witness(self) -> None:
        self.app.open_url(self.url)

    def action_copy_url(self) -> None:
        self.app.copy_to_clipboard(self.url)
        self.app.notify("Source URL copied")


class JanuaryReading(Reading):
    """A source-qualified January selection, including both external witnesses."""

    BINDINGS = [Binding("o", "open_source('latin_url')", "Latin missal"),
                Binding("a", "open_source('english_url')", "English antiphons"),
                Binding("e", "open_source('english_prayer_url')", "English missal"),
                Binding("t", "terminal_english", "English missal in terminal"),
                Binding("r", "open_source('rule_url')", "rubric")]

    def __init__(self, reading: dict, role: str | None = None) -> None:
        from .missal import blocks, source_rights
        from .widgets import Ink

        if role and role not in (reading.get("english_prayer_roles") or []):
            reading = {**reading, "english_prayer_url": None}
        self.reading = reading
        phase = {"before-epiphany": "before Epiphany", "after-epiphany": "after Epiphany"}[reading["phase"]]
        ink = Ink()
        for prayer in reading["prayers"]:
            if role is None or prayer["role"] == role:
                blocks(ink, prayer["blocks"])
                ink.line()
        for field, label in (("latin_url", "Latin missal prayers"), ("english_prayer_url", "U.S. English missal prayers"),
                             ("english_url", "English antiphons only"),
                             ("rule_url", reading["rule_locus"])):
            if reading.get(field):
                ink.line(label, "bold")
                source_id = reading.get({"latin_url": "latin_source_id", "english_url": "english_source_id",
                                         "english_prayer_url": "english_prayer_source_id"}.get(field))
                if source_id:
                    ink.line(source_id, "$text-muted")
                locus = {"english_url": "english_locus", "english_prayer_url": "english_prayer_locus"}.get(field)
                if reading.get(locus):
                    ink.line(reading[locus])
                if field == "english_prayer_url" and reading.get("english_prayer_rights_status"):
                    ink.line(source_rights(reading["english_prayer_rights_status"]), "$text-muted")
                ink.line(reading[field]).line()
        hint = "o Latin missal · a English antiphons · r rubric"
        if reading.get("english_prayer_url"):
            hint += " · e English missal" + (" · t terminal browser" if terminal_browser() else "")
        super().__init__(reading["label"] + " " + phase, ink.content(), hint + " · esc close", walks=False)

    def action_terminal_english(self) -> None:
        if self.reading.get("english_prayer_url"):
            browse_in_terminal(self.app, self.reading["english_prayer_url"])

    def action_open_source(self, field: str) -> None:
        if self.reading.get(field):
            self.app.open_url(self.reading[field])


class Pick(ModalScreen[str | None]):
    """One choice among named options; nothing is preselected for the reader."""

    DEFAULT_CSS = """
    Pick { align: center middle; background: $background 65%; }
    Pick > Vertical {
        width: 80; max-width: 95%; height: auto; max-height: 85%;
        border: round $primary 65%; background: $surface; padding: 1 2;
    }
    Pick Static { color: $text-muted; padding: 0 0 1 0; }
    Pick OptionList { border: none; background: transparent; padding: 0; height: 1fr; }
    Pick.reading-settings > Vertical { height: 17; max-height: 95%; padding: 0 1; }
    Pick OptionList:focus { border: none; }
    """
    BINDINGS = [Binding("escape", "decline", "cancel")]

    def __init__(self, title: str, options: list[tuple[object, object]], hint: str = "",
                 *, sections: dict[int, str] | None = None) -> None:
        super().__init__(classes="reading-settings" if sections else None)
        self.title_text = title
        self.options = options
        self.sections = sections or {}
        self.hint = hint

    def compose(self) -> ComposeResult:
        from textual.widgets import OptionList
        from textual.widgets.option_list import Option

        with Vertical() as box:
            # Give the option list the remaining viewport, including when a
            # narrow terminal wraps the hint or a choice onto multiple lines.
            if not self.sections:
                box.styles.height = min(34, max(8, len(self.options) + (7 if self.hint else 4)))
            box.border_title = titled(None, self.title_text)
            box.border_subtitle = "↑↓ choose · enter apply · esc cancel"
            if self.hint:
                yield Static(self.hint)
            items = []
            for index, (_, label) in enumerate(self.options):
                if index in self.sections:
                    items.append(Option(titled(None, self.sections[index]), disabled=True))
                items.append(Option(label, id=str(index)))
            yield OptionList(*items)

    def on_mount(self) -> None:
        from textual.widgets import OptionList

        # Nothing is offered as already chosen: Enter does nothing until the
        # reader has moved to an option.
        listing = self.query_one(OptionList)
        listing.focus()
        listing.highlighted = None

    def on_option_list_option_selected(self, event) -> None:
        self.dismiss(self.options[int(event.option.id)][0])

    def action_decline(self) -> None:
        self.dismiss(None)
