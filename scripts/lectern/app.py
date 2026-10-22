"""The application shell: the top bar, the surfaces, the keys that move between them."""
from __future__ import annotations

import datetime as dt

from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import ContentSwitcher, Footer, Static

from .surface import Pending, Surface
from .theme import SURFACE_ACCENTS, THEMES
from .widgets import SUPERSCRIPT


KEY_NAMES = {
    "left_square_bracket": "[", "right_square_bracket": "]", "left_curly_bracket": "{",
    "right_curly_bracket": "}", "slash": "/", "question_mark": "?", "left": "←", "right": "→",
}


def surfaces() -> list[type[Surface]]:
    """The surfaces in the order the site lists them; the digit reaches each."""
    from .surfaces import ORDER

    return ORDER


class TopBar(Static):
    """The wordmark, the surfaces by number, and where the reader is."""

    DEFAULT_CSS = """
    TopBar { height: 1; background: $panel; color: $foreground; padding: 0 1; }
    """
    current = reactive("day")
    where = reactive("")

    def _tabs(self, short: bool) -> Text:
        variables = self.app.theme_variables
        bar = Text()
        bar.append("✠ ", style=f"bold {variables.get('day-color', SURFACE_ACCENTS['day'][0])}")
        bar.append("triptych " if not short else "", style="bold")
        for kind in surfaces():
            ident = kind.surface_id()
            accent = variables.get(f"{ident}-color", "#888888")
            chosen = ident == self.current
            name = kind.label.lower()
            if short and not chosen:
                name = name[:3]
            click = Style.from_meta({"@click": f"app.surface('{ident}')"})
            bar.append(" ")
            bar.append(kind.key.translate(SUPERSCRIPT), style=Style.parse(variables.get("hotkey", "red")) + click)
            label = f" {name} " if chosen else name
            bar.append(label, style=Style.parse(f"bold reverse {accent}" if chosen else accent) + click)
        return bar

    def render(self) -> Text:
        width = self.size.width - 2
        bar = self._tabs(short=False)
        if bar.cell_len > width:
            bar = self._tabs(short=True)
        if self.where:
            room = width - bar.cell_len - 2
            if room > 8:
                note = self.where if len(self.where) <= room else self.where[: room - 1] + "…"
                bar.append(" " * (room - len(note) + 2))
                bar.append(note, style="italic")
        return bar


class Help(ModalScreen[None]):
    """Every key, for the shell and for the surface in front of the reader."""

    DEFAULT_CSS = """
    Help { align: center middle; }
    Help > VerticalScroll {
        width: 76; max-width: 95%; height: auto; max-height: 90%;
        border: round $accent; background: $surface; padding: 1 2;
    }
    """
    BINDINGS = [Binding("escape,q,question_mark", "dismiss", "close")]

    def __init__(self, surface: Surface | None) -> None:
        super().__init__()
        self.surface = surface

    def compose(self) -> ComposeResult:
        from rich.console import Group
        from rich.table import Table

        hotkey = self.app.theme_variables.get("hotkey", "red")
        parts = []

        def section(title: str, rows) -> None:
            parts.append(Text(title, style="bold underline"))
            grid = Table.grid(padding=(0, 2))
            grid.add_column(style=f"bold {hotkey}", no_wrap=True, min_width=16)
            grid.add_column(ratio=1)
            for key, what in rows:
                grid.add_row(key, what)
            parts.append(grid)
            parts.append(Text(""))

        section("everywhere", (
            ("1 … 8", "switch surface: day, propers, catena, scripture, texts, sources, history, law"),
            ("tab, shift+tab", "move between panes"),
            ("ctrl+p", "command palette: every surface and action, searchable"),
            ("T", "next theme: triptych, vellum, compline"),
            ("?", "this help"),
            ("q, ctrl+c", "quit"),
        ))
        if self.surface is not None and self.surface.HELP:
            section(self.surface.label.lower(), self.surface.HELP)
        parts.append(Text(
            "Colour decorates; every state it marks is also written out in words or a marked glyph. "
            "Nothing is derived here: each view is read from the published data or asked of the "
            "browser's own models, as the site's pages ask them.",
            style="dim italic",
        ))
        with VerticalScroll() as box:
            box.border_title = "help"
            box.border_subtitle = "esc close"
            yield Static(Group(*parts))


def _surface_css() -> str:
    """Each surface's frames, cursor and scrollbars take its own accent."""
    rules = []
    for name in SURFACE_ACCENTS:
        tone = f"${name}-color"
        rules.append(f"""
    .{name} Panel, .{name} ScrollPanel {{
        border: round {tone} 55%;
        scrollbar-color: {tone} 45%; scrollbar-color-hover: {tone} 75%; scrollbar-color-active: {tone};
        scrollbar-background: $surface; scrollbar-size-vertical: 1;
    }}
    .{name} Panel:focus-within, .{name} ScrollPanel:focus, .{name} ScrollPanel:focus-within {{
        border: round {tone};
    }}
    .{name} OptionList {{
        scrollbar-color: {tone} 45%; scrollbar-color-hover: {tone} 75%; scrollbar-color-active: {tone};
        scrollbar-background: $surface;
    }}
    .{name} OptionList > .option-list--option-highlighted {{ background: {tone} 18%; color: $foreground; }}
    .{name} OptionList:focus > .option-list--option-highlighted {{
        background: {tone} 45%; color: $foreground; text-style: bold;
    }}""")
    return "".join(rules)


class TriptychApp(App[None]):
    """The reader."""

    TITLE = "triptych"
    CSS = """
    Screen { background: $background; }
    #surfaces { height: 1fr; }
    .pending { padding: 2 4; color: $text-muted; }
    Footer { background: $panel; }
    TopBar { link-style: none; link-style-hover: bold; link-background-hover: $panel-lighten-2; }
    Panel OptionList, Panel OptionList:focus, ScrollPanel OptionList, ScrollPanel OptionList:focus {
        border: none; padding: 0; background: transparent; background-tint: $foreground 0%;
        scrollbar-size-vertical: 1;
    }
    """ + _surface_css() + "".join(getattr(kind, "CSS", "") for kind in surfaces())
    BINDINGS = [
        Binding("q", "quit", "quit", show=False),
        Binding("question_mark", "help", "help"),
        Binding("T", "next_theme", "theme", show=False),
    ] + [
        Binding(str(number), f"surface_at({number})", show=False)
        for number in range(1, 10)
    ]

    def __init__(self, *, start: str = "day", intent: dict | None = None,
                 theme: str = "triptych", today: dt.date | None = None) -> None:
        super().__init__()
        # The date the reader calls today. A snapshot pins it, so that what it
        # draws depends on the arguments and never on the clock.
        self.today = today or dt.date.today()
        for palette in THEMES:
            self.register_theme(palette)
        self.theme = theme
        self.start = start
        self.intent = intent or {}

    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        with ContentSwitcher(id="surfaces", initial=None):
            for kind in surfaces():
                yield kind()
        yield Footer()

    def on_mount(self) -> None:
        self.action_surface(self.start, **self.intent)

    # --- moving between surfaces -------------------------------------------

    def current(self) -> Surface | None:
        switcher = self.query_one("#surfaces", ContentSwitcher)
        if switcher.current is None:
            return None
        return self.query_one(f"#{switcher.current}", Surface)

    def action_surface(self, ident: str, **intent) -> None:
        switcher = self.query_one("#surfaces", ContentSwitcher)
        switcher.current = ident
        surface = self.query_one(f"#{ident}", Surface)
        self.query_one(TopBar).current = ident
        surface.open(**intent)
        self.refresh_where()
        self.call_after_refresh(self._focus_into, surface)

    def _focus_into(self, surface: Surface) -> None:
        if self.focused is None or surface not in self.focused.ancestors_with_self:
            surface.refocus()

    def action_surface_at(self, number: int) -> None:
        order = surfaces()
        if 1 <= number <= len(order):
            self.action_surface(order[number - 1].surface_id())

    def refresh_where(self) -> None:
        surface = self.current()
        self.query_one(TopBar).where = surface.where() if surface else ""

    # --- the rest ------------------------------------------------------------

    def get_system_commands(self, screen):
        """Every surface, and every keyed action of the one in front, by name."""
        from textual.app import SystemCommand

        for kind in surfaces():
            ident = kind.surface_id()
            yield SystemCommand(f"open {ident}", f"key {kind.key}",
                                lambda ident=ident: self.action_surface(ident))
        surface = self.current()
        if surface is not None:
            for binding in surface.BINDINGS:
                if not isinstance(binding, Binding) or not binding.description:
                    continue
                key = KEY_NAMES.get(binding.key.split(",")[0], binding.key.split(",")[0])
                yield SystemCommand(f"{surface.surface_id()}: {binding.description}", f"key {key}",
                                    lambda action=binding.action, surface=surface: surface.run_action(action))
        for palette in THEMES:
            yield SystemCommand(f"theme: {palette.name}", "colours only; nothing they mark is lost",
                                lambda name=palette.name: setattr(self, "theme", name))
        yield SystemCommand("help", "key ?", self.action_help)
        yield SystemCommand("quit", "key q", self.exit)

    def action_help(self) -> None:
        self.push_screen(Help(self.current()))

    def action_next_theme(self) -> None:
        names = [palette.name for palette in THEMES]
        position = names.index(self.theme) if self.theme in names else -1
        self.theme = names[(position + 1) % len(names)]
        self.query_one(TopBar).refresh()
        self.notify(f"theme: {self.theme}", timeout=1.5)


__all__ = ["TriptychApp", "Pending"]
