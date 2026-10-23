"""What every surface is: a page of the site, opened lazily, reporting where it is."""
from __future__ import annotations

from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Static

NARROW = 110  # below this many columns a surface draws its side panes lean
WIDE = 160  # from this many, it gives them room
COMPACT = 90  # below this, the Missal's text and navigation take turns


class Surface(Container):
    """One top-level view. It builds nothing until it is first shown."""

    DEFAULT_CSS = """
    Surface { height: 1fr; width: 1fr; layout: vertical; }
    """
    #: (key digit, id, label) — filled by each subclass.
    key = ""
    label = ""
    #: The help lines a reader sees for this surface under `?`.
    HELP: tuple[tuple[str, str], ...] = ()
    #: Rules that must outrank the shared frame rules: they join the app's own
    #: stylesheet, which a widget's DEFAULT_CSS never outranks. A surface hides
    #: its side panes under `.<id>.focus`, and leans them under `.<id>.narrow`.
    CSS = ""
    BINDINGS = [Binding("f", "focus_reading", "panes")]
    #: The pane a reader's keys should reach first: the one that holds the reading.
    FIRST = ""

    def __init__(self, **options) -> None:
        super().__init__(id=self.surface_id(), **options)
        self.opened = False
        self._initial_focus_pending = False
        self.add_class(self.surface_id())

    @classmethod
    def surface_id(cls) -> str:
        return cls.label.lower()

    def open(self, **intent) -> None:
        """Called each time the surface is shown, with any intent carried to it
        (a date, a reference). The first call builds it."""
        if not self.opened:
            self.opened = True
            self._initial_focus_pending = True
            # A date-first reader starts with the text; a formulary-first
            # visitor needs Browse until a formulary is explicitly opened.
            if self.surface_id() == "propers" and not intent.get("mass"):
                self.add_class("navigation")
            self.build()
        if intent:
            self.follow(**intent)

    def build(self) -> None:
        """Mount the surface's panes and start loading."""

    def deliver(self, callback, *args, **options) -> None:
        """From a worker's thread, hand its result to the screen — unless a newer
        request in the same exclusive group has superseded it. A cancelled
        thread worker runs on to its end; its answer must not land over the
        newer one, so it is checked here and again on the screen's own thread,
        where a newer request would have cancelled it."""
        from textual.worker import get_current_worker

        worker = get_current_worker()
        if worker.is_cancelled:
            return

        def current() -> None:
            if not worker.is_cancelled:
                callback(*args, **options)
                if self._initial_focus_pending and shown(self):
                    self.call_after_refresh(self.focus_initial)

        self.app.call_from_thread(current)

    def on_resize(self, event) -> None:
        self.set_class(event.size.width < NARROW, "narrow")
        self.set_class(event.size.width >= WIDE, "wide")
        self.set_class(event.size.width < COMPACT, "compact")
        self.set_class(event.size.height < 34, "short")
        if self.surface_id() in ("day", "propers"):
            self.call_after_refresh(self.refocus)

    def action_focus_reading(self) -> None:
        """Side panes away, the reading full width; again to bring them back."""
        if self.has_class("compact") and self.surface_id() in ("day", "propers"):
            self.toggle_class("navigation")
        else:
            self.toggle_class("focus")
        self.call_after_refresh(self.refocus)

    def show_reading_pane(self) -> None:
        """A deliberate selection brings its reading forward on a small screen."""
        self.remove_class("navigation")
        if self.has_class("compact"):
            self.call_after_refresh(self.refocus)

    def focus_initial(self) -> None:
        """Apply a declared initial target without replacing a surface's own focus.

        Mounting may finish after the shell's first frame. Surfaces that name
        FIRST retry on delivery; the others retain their explicit catalogue,
        lookup or view-specific focus and the zero-argument refocus hook.
        """
        if not self._initial_focus_pending:
            return
        if self.FIRST:
            self._refocus(prefer_first=True)
        else:
            self._initial_focus_pending = False
            focused = self.app.focused
            if focused is None or self not in focused.ancestors_with_self:
                self.refocus()

    def refocus(self) -> None:
        """Keep the keys working: focus may not stay on a pane that was hidden."""
        self._refocus()

    def _refocus(self, *, prefer_first: bool = False) -> None:
        focused = self.app.focused
        if not prefer_first and focused is not None and self in focused.ancestors and shown(focused):
            return
        first_widgets = list(self.query(self.FIRST)) if self.FIRST else []
        if first_widgets:
            for widget in first_widgets:
                if widget.focusable and shown(widget):
                    widget.focus()
                    self._initial_focus_pending = False
                    return
        for widget in self.query("*"):
            if widget.focusable and shown(widget):
                widget.focus()
                # The preferred pane may be deliberately hidden by the
                # compact reading layout. A visible fallback completes entry.
                if first_widgets:
                    self._initial_focus_pending = False
                return


    def follow(self, **intent) -> None:
        """Move to what another surface asked for."""

    def where(self) -> str:
        """A short statement of what is on screen, for the top bar."""
        return ""


def shown(widget) -> bool:
    """Displayed, and inside nothing that is not."""
    return all(getattr(node, "display", True) for node in widget.ancestors_with_self)


class Pending(Surface):
    """A surface that is not available, and why."""

    problem = ""

    def build(self) -> None:
        said = f"{self.label} could not be opened.\n\n{self.problem}" if self.problem \
            else f"{self.label}: not yet available"
        self.mount(Static(said, classes="pending", markup=False))
