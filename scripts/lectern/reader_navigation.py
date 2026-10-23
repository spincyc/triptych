"""Presentation positions over the reader owner's stable semantic event IDs."""
from __future__ import annotations

from functools import lru_cache
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

from .dialogs import Pick, Reading
from .repo import ROOT
from .widgets import Ink


@lru_cache(maxsize=1)
def _site_url():
    """Use the publisher's URL owner, including its single declared origin."""
    loader = SourceFileLoader("_lectern_public_urls", str(ROOT / "tools" / "public-alpha"))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module.public_site_url


def share(surface, route: str) -> None:
    url = _site_url()(route)
    surface.app.copy_to_clipboard(url)
    ink = Ink().line("The canonical reader URL has been copied to the terminal clipboard.", "italic")
    ink.line().line(url)
    surface.app.push_screen(Reading("Share this reading", ink.content(), walks=False))


class ReadingNavigation:
    """A semantic Contents list whose scroll coordinates belong to Textual.

    Prefix heights are measured by the same Content formatter the Static uses;
    no translated heading, source order or liturgical seat is reconstructed.
    """

    def __init__(self) -> None:
        self.entries: list[tuple[str, str, object]] = []
        self.identity: tuple | None = None
        self.saved: tuple[str | None, float] | None = None
        self.pending: str | None = None
        self.focused: tuple[str, float] | None = None

    @staticmethod
    def _height(prefix, text) -> int:
        return max(0, prefix.get_height(text.styles, max(1, text.content_size.width)) - 1)

    def current(self, box, text) -> str | None:
        if self.focused and abs(self.focused[1] - box.scroll_y) < 0.5:
            return self.focused[0]
        self.focused = None
        return next((ident for ident, _, prefix in reversed(self.entries)
                     if self._height(prefix, text) <= box.scroll_y), None)

    def begin(self, identity: tuple, box, text) -> None:
        self.saved = (self.current(box, text), box.scroll_y) if identity == self.identity else None
        self.identity = identity
        self.entries = []
        self.focused = None

    def mark(self, ident: str, label: str, ink: Ink) -> None:
        self.entries.append((ident, label, ink.content()))

    def finish(self, surface, box, text) -> None:
        requested = self.pending
        self.pending = None
        saved = self.saved
        self.saved = None

        def restore() -> None:
            ident = requested or (saved[0] if saved else None)
            entry = next((one for one in self.entries if one[0] == ident), None)
            if entry:
                box.scroll_to(y=self._height(entry[2], text), animate=False, force=True, immediate=True)
                self.focused = (entry[0], box.scroll_y)
            else:
                box.scroll_to(y=saved[1] if saved and not requested else 0, animate=False, force=True, immediate=True)
            if requested and not entry:
                surface.app.notify("That semantic location is absent from this reading.", severity="warning")

        surface.call_after_refresh(restore)

    def choose(self, surface, box, text) -> None:
        if not self.entries:
            surface.app.notify("There are no liturgical units in this reading yet.")
            return
        current = self.current(box, text)
        options = [(ident, label + ("  ·  here" if ident == current else ""))
                   for ident, label, _ in self.entries]

        def picked(ident) -> None:
            if ident is None:
                return
            entry = next(one for one in self.entries if one[0] == ident)
            surface.show_reading_pane()

            def move() -> None:
                box.scroll_to(y=self._height(entry[2], text), animate=False, force=True, immediate=True)
                self.focused = (entry[0], box.scroll_y)

            surface.call_after_refresh(move)
            box.focus()

        surface.app.push_screen(Pick("Contents", options, "Source events in their liturgical order."), picked)
