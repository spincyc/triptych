"""What every surface is: a page of the site, opened lazily, reporting where it is."""
from __future__ import annotations

from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Static

NARROW = 110  # below this many columns a surface draws its side panes lean
WIDE = 160  # from this many, it gives them room


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
    BINDINGS = [Binding("f", "focus_reading", "focus", show=False)]
    #: The pane a reader's keys should reach first: the one that holds the reading.
    FIRST = ""

    def __init__(self, **options) -> None:
        super().__init__(id=self.surface_id(), **options)
        self.opened = False
        self.add_class(self.surface_id())

    @classmethod
    def surface_id(cls) -> str:
        return cls.label.lower()

    def open(self, **intent) -> None:
        """Called each time the surface is shown, with any intent carried to it
        (a date, a reference). The first call builds it."""
        if not self.opened:
            self.opened = True
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

        self.app.call_from_thread(current)

    def on_resize(self, event) -> None:
        self.set_class(event.size.width < NARROW, "narrow")
        self.set_class(event.size.width >= WIDE, "wide")

    def action_focus_reading(self) -> None:
        """Side panes away, the reading full width; again to bring them back."""
        self.toggle_class("focus")
        self.call_after_refresh(self.refocus)

    def refocus(self) -> None:
        """Keep the keys working: focus may not stay on a pane that was hidden."""
        focused = self.app.focused
        if focused is not None and self in focused.ancestors and shown(focused):
            return
        if self.FIRST:
            for widget in self.query(self.FIRST):
                if widget.focusable and shown(widget):
                    widget.focus()
                    return
        for widget in self.query("*"):
            if widget.focusable and shown(widget):
                widget.focus()
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
