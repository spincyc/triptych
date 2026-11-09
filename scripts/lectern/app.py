"""The application shell: the top bar, the surfaces, the keys that move between them."""
from __future__ import annotations

import asyncio
import datetime as dt
from collections.abc import Awaitable, Callable

from rich.style import Style
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual import work
from textual.containers import Container, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import ContentSwitcher, Footer, LoadingIndicator, Static
from textual.worker import WorkerCancelled, get_current_worker

from . import bridge
from .repo import Refused
from .surface import Pending, Surface, shown
from .theme import SURFACE_ACCENTS, THEMES


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
    TopBar { height: 2; background: $background; color: $foreground; padding: 0 1; }
    """
    current = reactive("day")
    where = reactive("")

    def _tabs(self, short: bool) -> Text:
        variables = self.app.theme_variables
        bar = Text()
        bar.append("✠ ", style=f"bold {variables.get('day-color', SURFACE_ACCENTS['day'][0])}")
        bar.append("triptych  " if not short else "", style="bold")
        for kind in surfaces():
            ident = kind.surface_id()
            accent = variables.get(f"{ident}-color", "#888888")
            chosen = ident == self.current
            name = kind.label
            if short and not chosen:
                name = name[:3]
            click = Style.from_meta({"@click": f"app.surface('{ident}')"})
            label = f" {kind.key} {name} "
            style = f"bold {accent}" if chosen else variables.get("muted", "grey70")
            bar.append(label, style=Style.parse(style) + click)
        return bar

    def render(self) -> Text:
        width = max(1, self.size.width - 2)
        bar = self._tabs(short=False)
        if bar.cell_len > width:
            bar = self._tabs(short=True)
        if bar.cell_len > width:
            # Every section still has its digit and command-palette entry.
            # At very small widths the active identity outranks eight clipped tabs.
            label = next((kind.label for kind in surfaces() if kind.surface_id() == self.current), self.current)
            bar = Text(f"✠ {label}  ", style="bold")
            bar.append("1–8 sections · ctrl+p commands", style=self.app.theme_variables.get("muted", "grey70"))
        bar.truncate(width, overflow="ellipsis")
        bar.append("\n")
        if self.where:
            note = Text(self.where, style=self.app.theme_variables.get("muted", "grey70"))
            note.truncate(width, overflow="ellipsis")
            bar.append_text(note)
        return bar


class Help(ModalScreen[None]):
    """Every key, for the shell and for the surface in front of the reader."""

    DEFAULT_CSS = """
    Help { align: center middle; background: $background 65%; }
    Help > VerticalScroll {
        width: 76; max-width: 95%; height: auto; max-height: 90%;
        border: round $primary 65%; background: $surface; padding: 1 2;
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
            ("f", "show or hide navigation; on narrow screens, switch between navigation and reading"),
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
            if self.surface is not None and self.surface.surface_id() == "day":
                from .surfaces.day import legend_for

                yield Static("Calendar marks", classes="help-section")
                month = self.surface.months.get((self.surface.calendar, self.surface.date.strftime("%Y-%m")))
                yield Static(legend_for(month).content())


class ReaderFooter(Footer):
    """Keep Help and pane navigation visible, then fit the current commands.

    All bindings remain in Help and the command palette. The resting footer
    shows whole commands instead of clipping a label under the palette.
    """

    def compose(self) -> ComposeResult:
        widgets = list(super().compose())
        palette = [widget for widget in widgets if widget.has_class("-command-palette")]
        commands = [widget for widget in widgets if widget not in palette]
        commands.sort(key=lambda widget: {"help": 0, "focus_reading": 1}.get(getattr(widget, "action", ""), 2))
        room = (self.size.width or self.screen.size.width) - sum(
            len(getattr(widget, "key_display", "")) + len(getattr(widget, "description", "")) + 3
            for widget in palette
        )
        for widget in commands:
            needed = len(getattr(widget, "key_display", "")) + len(getattr(widget, "description", "")) + 2
            if needed <= room:
                yield widget
                room -= needed
        yield from palette

    async def on_resize(self) -> None:
        await self.recompose()


def _surface_css() -> str:
    """Each surface's frames, cursor and scrollbars take its own accent."""
    rules = []
    for name in SURFACE_ACCENTS:
        tone = f"${name}-color"
        rules.append(f"""
    .{name} Panel, .{name} ScrollPanel {{
        border: round $rule;
        scrollbar-color: {tone} 45%; scrollbar-color-hover: {tone} 75%; scrollbar-color-active: {tone};
        scrollbar-background: $surface; scrollbar-size-vertical: 1;
    }}
    .{name} Panel:focus-within, .{name} ScrollPanel:focus, .{name} ScrollPanel:focus-within {{
        border: round {tone} 65%;
    }}
    .{name} OptionList {{
        scrollbar-color: {tone} 45%; scrollbar-color-hover: {tone} 75%; scrollbar-color-active: {tone};
        scrollbar-background: $surface;
    }}
    .{name} OptionList > .option-list--option-highlighted {{ background: {tone} 18%; color: $foreground; }}
    .{name} OptionList:focus > .option-list--option-highlighted {{
        background: {tone} 45%; color: $foreground; text-style: bold;
    }}
    .-light-mode .{name} OptionList > .option-list--option-highlighted {{ background: {tone} 12%; }}
    .-light-mode .{name} OptionList:focus > .option-list--option-highlighted {{
        background: {tone} 22%; color: $foreground; text-style: bold;
    }}""")
    return "".join(rules)


class TriptychApp(App[None]):
    """The reader."""

    TITLE = "triptych"
    CSS = """
    Screen { background: $background; layers: reader loading; }
    #reader { layer: reader; width: 100%; height: 100%; }
    #reader.preparing { visibility: hidden; }
    #loading {
        layer: loading; width: 100%; height: 100%;
        align: center middle; background: $background;
    }
    #loading-box { width: 66; max-width: 90%; height: auto; max-height: 100%; padding: 1 2; }
    #loading-box.failed { height: 100%; }
    #loading-detail-scroll { height: auto; }
    #loading-box.failed #loading-detail-scroll { height: 1fr; }
    #loading Static { height: auto; text-align: center; }
    #loading-title { text-style: bold; color: $primary; margin-bottom: 1; }
    #loading LoadingIndicator { height: 2; margin: 1 0; }
    #loading-hint { color: $text-muted; margin-top: 1; }
    #surfaces { height: 1fr; }
    Surface { padding: 0 1; }
    .pending { padding: 2 4; color: $text-muted; }
    Footer { background: $panel; }
    Help .help-section { text-style: bold; margin-bottom: 1; }
    TopBar { link-style: none; link-style-hover: bold; link-background-hover: $panel-lighten-2; }
    Panel OptionList, Panel OptionList:focus, ScrollPanel OptionList, ScrollPanel OptionList:focus {
        border: none; padding: 0; background: transparent; background-tint: $foreground 0%;
        scrollbar-size-vertical: 1;
    }
    """ + _surface_css() + "".join(getattr(kind, "CSS", "") for kind in surfaces())
    BINDINGS = [
        Binding("q", "quit", "quit", show=False),
        Binding("ctrl+c", "quit", "quit", show=False, priority=True),
        Binding("question_mark", "help", "help"),
        Binding("T", "next_theme", "theme", show=False),
    ] + [
        Binding(str(number), f"surface_at({number})", show=False)
        for number in range(1, 10)
    ]

    def __init__(self, *, start: str = "day", intent: dict | None = None,
                 theme: str = "triptych", today: dt.date | None = None,
                 prepare: Callable[[], Awaitable[None]] | None = None) -> None:
        super().__init__()
        # The date the reader calls today. A snapshot pins it, so that what it
        # draws depends on the arguments and never on the clock.
        self.today = today or dt.date.today()
        for palette in THEMES:
            self.register_theme(palette)
        self.theme = theme
        self.start = start
        self.intent = intent or {}
        self._surface_focus = {}
        self.prepare = prepare
        self.starting = True
        self.startup_error: Refused | None = None
        self._startup_worker = None
        self._quitting = False

    def compose(self) -> ComposeResult:
        with Container(id="reader", classes="preparing", disabled=True):
            yield TopBar(id="topbar")
            with ContentSwitcher(id="surfaces", initial=None):
                for kind in surfaces():
                    yield kind()
            yield ReaderFooter(compact=True)
        with Container(id="loading"):
            with Vertical(id="loading-box"):
                yield Static("✠ triptych", id="loading-title")
                yield Static("Preparing your reading…", id="loading-status", markup=False)
                yield LoadingIndicator()
                with VerticalScroll(id="loading-detail-scroll", can_focus=False):
                    yield Static("The first load may take several minutes.", id="loading-detail", markup=False)
                yield Static("q / ctrl+c  cancel", id="loading-hint")

    def on_mount(self) -> None:
        # The first frame must be visible before verification can start.
        self.call_after_refresh(self._begin_startup)

    def _begin_startup(self) -> None:
        if not self._quitting:
            self._startup_worker = self._load_initial()

    @work
    async def _load_initial(self) -> None:
        if self.prepare is not None:
            self.query_one("#loading-status", Static).update("Preparing verified reading data…")
            try:
                await self.prepare()
            except (Refused, OSError) as error:
                self.startup_error = Refused(str(error))
                self.query_one("#loading-status", Static).update("The reading could not be opened.")
                self.query_one("#loading-detail", Static).update(str(error))
                self.query_one(LoadingIndicator).display = False
                self.query_one("#loading-hint", Static).update("q / ctrl+c  close")
                self.query_one("#loading-box").add_class("failed")
                detail = self.query_one("#loading-detail-scroll", VerticalScroll)
                detail.can_focus = True
                self.call_after_refresh(detail.focus)
                return
        self.query_one("#loading-status", Static).update(f"Opening {self.start.title()}…")
        self.query_one("#loading-detail", Static).update("Loading the initial reading.")
        self._open_surface(self.start, **self.intent)
        coordinator = get_current_worker()
        quiet = 0
        # Opening a surface may spawn another load when its first worker delivers.
        # A single wait_for_complete() captures only the workers already present.
        while quiet < 3:
            await asyncio.sleep(0.05)
            busy = any(worker is not coordinator and not worker.is_finished for worker in self.workers)
            quiet = 0 if busy or bridge.BRIDGE_PROCESS.waiting else quiet + 1
        reader = self.query_one("#reader")
        reader.disabled = False
        reader.remove_class("preparing")
        self.query_one("#loading").display = False
        self.starting = False
        if (surface := self.current()) is not None:
            surface._initial_focus_pending = True
            self.call_after_refresh(self._focus_into, surface, True)
        self.refresh_bindings()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        if self.starting and action != "quit":
            return False
        return super().check_action(action, parameters)

    async def action_quit(self) -> None:
        if self._quitting:
            return
        self._quitting = True
        if self.starting:
            self.query_one("#loading-status", Static).update("Closing…")
        if self._startup_worker is not None and not self._startup_worker.is_finished:
            self._startup_worker.cancel()
            try:
                await self._startup_worker.wait()
            except WorkerCancelled:
                pass
        self.workers.cancel_all()
        # Closing the bridge can wait for its verification thread; keep drawing.
        await asyncio.to_thread(bridge.BRIDGE_PROCESS.close)
        self.exit()

    # --- moving between surfaces -------------------------------------------

    def current(self) -> Surface | None:
        switcher = self.query_one("#surfaces", ContentSwitcher)
        if switcher.current is None:
            return None
        return self.query_one(f"#{switcher.current}", Surface)

    def action_surface(self, ident: str, **intent) -> None:
        if not self.starting:
            self._open_surface(ident, **intent)

    def _open_surface(self, ident: str, **intent) -> None:
        switcher = self.query_one("#surfaces", ContentSwitcher)
        previous = self.current()
        if previous is not None and self.focused is not None and previous in self.focused.ancestors:
            self._surface_focus[previous.surface_id()] = self.focused
        switcher.current = ident
        surface = self.query_one(f"#{ident}", Surface)
        first_open = not surface.opened
        self.query_one(TopBar).current = ident
        surface.open(**intent)
        self.refresh_where()
        self.call_after_refresh(self._focus_into, surface, first_open, not intent)

    def _focus_into(self, surface: Surface, first_open: bool = False, restore: bool = True) -> None:
        if self.starting:
            return
        if first_open:
            surface.focus_initial()
        elif (restore and (remembered := self._surface_focus.get(surface.surface_id())) is not None
              and remembered.is_attached and remembered.focusable and shown(remembered)):
            remembered.focus()
        elif self.focused is None or surface not in self.focused.ancestors_with_self:
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
        yield SystemCommand("quit", "key q", self.action_quit)

    def action_help(self) -> None:
        self.push_screen(Help(self.current()))

    def action_next_theme(self) -> None:
        names = [palette.name for palette in THEMES]
        position = names.index(self.theme) if self.theme in names else -1
        self.theme = names[(position + 1) % len(names)]
        self.query_one(TopBar).refresh()
        self.notify(f"theme: {self.theme}", timeout=1.5)


__all__ = ["TriptychApp", "Pending"]
