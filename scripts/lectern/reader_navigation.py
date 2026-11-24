"""Presentation positions over the reader owner's stable semantic event IDs."""
from __future__ import annotations

from bisect import bisect_right
from functools import lru_cache
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

from .dialogs import MissalSource, Pick, Reading
from .missal import witness_label, witness_readings
from .repo import ROOT
from .surface import Surface, shown
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


class MissalSurface(Surface):
    """The shared reading, navigation and settings controls of Day and Propers."""

    READING = ""
    BROWSE = ""

    def reading_panel(self):
        selector = "#day-compare" if getattr(self, "comparing", False) else self.READING
        return self.query_one(selector)

    def show_reading_pane(self) -> None:
        self.remove_class("navigation")
        self.add_class("focus")
        self.call_after_refresh(self.focus_reading_panel)

    def focus_reading_panel(self) -> None:
        panel = self.reading_panel()
        if shown(panel) and self.app.screen is self.screen:
            panel.focus(scroll_visible=False)

    def action_focus_reading(self) -> None:
        browsing = self.has_class("navigation") if self.has_class("compact") else not self.has_class("focus")
        if browsing:
            self.show_reading_pane()
        else:
            self.remove_class("focus")
            self.add_class("navigation")
            self.call_after_refresh(self.query_one(self.BROWSE).focus)

    def source_rows(self) -> list[dict]:
        raise NotImplementedError

    def action_missal_source(self) -> None:
        choices = []
        for row in self.source_rows():
            for name, link in witness_readings(row):
                title = f"{row['option']} · {name}" if row.get("option") else name
                choices.append((title, link))

        def display(index) -> None:
            if index is not None:
                title, link = choices[index]
                self.app.push_screen(MissalSource(title, link))

        if len(choices) == 1:
            display(0)
        elif choices:
            options = [(index, f"{name} · {witness_label(link)} · {link['locus']}")
                       for index, (name, link) in enumerate(choices)]
            self.app.push_screen(Pick("Source texts", options), display)

    def action_settings(self) -> None:
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        bible = next((one["label"] for one in self.bibles if one["id"] == self.bible), self.bible)
        options = [("calendar", f"Missal   {edition}"), ("missal", "Mode   " + ("Missal" if self.ordinary else "Read")),
                   ("choose", "Mass, form and source options")]
        sections = {0: "Celebration", len(options): "Prayers"}
        names = {"en": "English", "la": "Latin"}
        options.extend([("orations", "Oration language   " + names.get(self.orations, self.orations)),
                        ("bilingual", "Parallel Latin   " + ("on" if self.text_display == "latin-and-selected" else "off")),
                        ("witness", "Translation witness")])
        if self.ordinary:
            options.extend([("ordinary_language", "Ordinary language   " + names.get(self.ordinary_language, self.ordinary_language)),
                            ("rubrics", "Ordinary rubrics   " + ("shown" if self.rubrics else "hidden"))])
        sections[len(options)] = "Scripture"
        options.extend([("bible", f"Bible   {bible}"), ("companion", "Latin companion   " + (self.companion or "none"))])

        if any(link for row in self.source_rows() for _, link in witness_readings(row)):
            sections[len(options)] = "Sources"
            options.append(("missal_source", "Read source texts"))

        def picked(action) -> None:
            if action in ("calendar", "bible"):
                rows = self.calendars if action == "calendar" else self.bibles
                choices = [(one["id"], one["short"] if action == "calendar" else one["label"]) for one in rows]
                def apply(value) -> None:
                    if value is None:
                        return
                    if action == "calendar":
                        self.follow(calendar=value, browse=self.surface_id() == "propers")
                    else:
                        self.bible = value
                        self.reload_reading()
                self.app.push_screen(Pick("Missal" if action == "calendar" else "Bible", choices), apply)
            elif action:
                getattr(self, "action_" + action)()

        self.app.push_screen(Pick("Reading settings", options, sections=sections), picked)


class ReadingNavigation:
    """A semantic Contents list whose scroll coordinates belong to Textual.

    Prefix heights are measured by the same Content formatter the Static uses;
    no translated heading, source order or liturgical seat is reconstructed.
    """

    def __init__(self) -> None:
        self.entries: list[tuple[str, str, int]] = []
        self.ink: Ink | None = None
        self.identity: tuple | None = None
        self.saved: tuple[str | None, float] | None = None
        self.pending: str | None = None
        self.focused: tuple[str, float] | None = None

    def _height(self, end: int, text) -> int:
        # Measure a prefix only when navigating. Storing a fully styled copy
        # at every event made opening a long Missal quadratic in its length.
        assert self.ink is not None
        prefix = self.ink.content(end)
        return max(0, prefix.get_height(text.styles, max(1, text.content_size.width)) - 1)

    def current(self, box, text) -> str | None:
        if self.focused and abs(self.focused[1] - box.scroll_y) < 0.5:
            return self.focused[0]
        self.focused = None
        index = bisect_right(self.entries, box.scroll_y, key=lambda entry: self._height(entry[2], text))
        return self.entries[index - 1][0] if index else None

    def begin(self, identity: tuple, box, text) -> None:
        self.saved = (self.current(box, text), box.scroll_y) if identity == self.identity else None
        self.identity = identity
        self.entries = []
        self.ink = None
        self.focused = None

    def mark(self, ident: str, label: str, ink: Ink) -> None:
        self.ink = ink
        self.entries.append((ident, label, len(ink.parts)))

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
